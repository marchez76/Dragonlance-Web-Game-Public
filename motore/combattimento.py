#!/usr/bin/env python3
"""
Motore di combattimento — la prima volta che i dati vengono USATI.

PERCHE' ESISTE
    Tre anni di conversione hanno prodotto dati validati da ogni lato: schemi,
    validatori incrociati, verifica degli strati, confronto fra prosa e
    struttura. Nessuno di quei controlli chiede la sola cosa che conta: che
    con questi dati si possa giocare un turno. Questo modulo lo chiede.

    Non e' il motore d'arena della Fase 2. E' lo strumento che misura se i
    dati bastano, e per farlo deve essere severo in un modo particolare: dove
    un dato manca NON inventa in silenzio.

IL REGISTRO DELLE LACUNE — il pezzo che paga il costo di questo modulo
    Ogni volta che il motore ha bisogno di qualcosa che i dati non portano,
    chiama `lacuna()` e va avanti con un'assunzione DICHIARATA. Alla fine
    l'elenco delle lacune e' il risultato vero: uno scontro che gira senza
    lacune vuol dire che i dati bastano, uno che gira con dodici vuol dire
    che il motore ha riempito dodici buchi al posto loro.

    Senza questo registro un simulatore mente: gira sempre, perche' ogni
    valore assente diventa uno zero e ogni regola assente diventa un ramo
    che non si prende. E' la stessa forma del difetto che la categoria
    d'arma ha reso visibile — un buco che sembra un dato.

COSA LEGGE
    dati/mostri/*.json      mechanics_5e.actions[].effetto, traits[].effetto
    dati/condizioni/*.json  le clausole, e la catena `implica`
    dati/oggetti/*.json     weapon_5e, armor_5e
    dati/classi/*.json      chassis_features[].effetto, structural
    dati/razze/*.json       lo strato 5e, tramite motore.generazione

Uso:  python3 motore/arena.py
"""

import collections
import glob
import json
import os
import random
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATI = os.path.join(BASE, "dati")

sys.path.insert(0, DATI)
import _sistema as sistema  # noqa: E402
import _vocabolari as vocabolari  # noqa: E402

CAR = ["str", "dex", "con", "int", "wis", "cha"]

# Il nome del tratto che si innesca alla morte. NON e' un dato: nessun campo
# dello schema dice quando un tratto scatta, quindi il motore lo riconosce dal
# nome. E' registrato come lacuna a ogni scontro in cui conta.
TRATTI_ALLA_MORTE = {"Death Throes"}


# ------------------------------------------------------------ registro lacune
class Registro:
    def __init__(self):
        self.lacune = collections.OrderedDict()
        self.righe = []

    def lacuna(self, codice, cosa, assunzione):
        if codice not in self.lacune:
            self.lacune[codice] = (cosa, assunzione)

    def riga(self, testo):
        self.righe.append(testo)

    def stampa(self):
        return "\n".join(self.righe)


# --------------------------------------------------------------------- dadi
_DADO = re.compile(r"^(\d+)d(\d+)$")


def tira(dadi, rng):
    m = _DADO.match(dadi)
    n, f = int(m.group(1)), int(m.group(2))
    return sum(rng.randint(1, f) for _ in range(n))


def mod(punteggio):
    """Il modificatore, LETTO da dati/sistema/modificatore-caratteristica.json.

    Era `(punteggio - 10) // 2` scritto qui e una seconda volta in
    `dati/valida_effetti.py`: meta' della nona struttura doppia del
    progetto, e la prima a vivere nel codice invece che nei dati — cioe'
    dove non arrivavano ne' gli schemi ne' i validatori. Decisione 51
    (`criterio-meccanica`); il controllo che impedisce di riscriverla e'
    `dati/valida_sistema.py`."""
    return sistema.modificatore(punteggio)


def d20(rng, vantaggio=False, svantaggio=False):
    a = rng.randint(1, 20)
    if vantaggio == svantaggio:
        return a, ""
    b = rng.randint(1, 20)
    if vantaggio:
        return max(a, b), " (vantaggio)"
    return min(a, b), " (svantaggio)"


# ---------------------------------------------------------------- condizioni
def carica_condizioni():
    cond = {}
    for f in sorted(glob.glob(os.path.join(DATI, "condizioni", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        cond[d["id"]] = d
    return cond


CONDIZIONI = carica_condizioni()


def clausole(ids):
    """Tutte le clausole attive, risolvendo la catena `implica`."""
    viste, coda, fuori = set(), list(ids), []
    while coda:
        cid = coda.pop()
        if cid in viste or cid not in CONDIZIONI:
            continue
        viste.add(cid)
        fuori.extend(CONDIZIONI[cid]["effetti"])
        coda.extend(CONDIZIONI[cid].get("implica") or [])
    return fuori


def ha_clausola(ids, nome, caratteristica=None):
    for c in clausole(ids):
        if c["clausola"] != nome:
            continue
        car = c.get("caratteristiche")
        if car is None or caratteristica is None or caratteristica in car:
            return True
    return False


# ------------------------------------------------------------- combattenti
class Combattente:
    def __init__(self, nome, ca, pf, abilities, azioni, tratti,
                 squadra, competenza, giocante=False, difese=None,
                 immunita_condizione=()):
        self.nome = nome
        self.ca = ca
        self.pf_max = pf
        self.pf = pf
        self.ab = abilities
        self.azioni = azioni          # [(nome, effetto)]
        self.tratti = tratti          # [(nome, effetto)]
        self.squadra = squadra
        self.competenza = competenza
        self.giocante = giocante
        self.condizioni = set()
        # {"resistenze": [...], "immunita": [...], "vulnerabilita": [...]},
        # ogni voce {"tipo", "solo_se"} del vocabolario condiviso.
        self.difese = difese or {"resistenze": [], "immunita": [],
                                 "vulnerabilita": []}
        # Gli id del vocabolario condiviso
        # (decisione 53, `condizioni-vocabolario-srd`). Possono nominare
        # condizioni che il
        # catalogo non modella: e' una lacuna nostra, non un errore della
        # scheda, e il motore la dichiara invece di ignorarla.
        self.immunita_condizione = tuple(immunita_condizione)
        self.salvezze_in_sospeso = []  # [(descrizione, effetto_ts, fonte)]
        self.risorse = {}
        self.morto = False
        self.livello = 0
        self.arena_avversari = []

    def azione(self, nome):
        for n, e in self.azioni:
            if n == nome:
                return e
        return None

    def puo_agire(self):
        return (not self.morto) and not ha_clausola(self.condizioni, "non_puo_agire")

    def in_gioco(self):
        return self.puo_agire()

    def __repr__(self):
        return self.nome


# ----------------------------------------------------------- caricamento dati
def carica(cartella, ident):
    p = os.path.join(DATI, cartella, ident + ".json")
    return json.load(open(p, encoding="utf-8"))


def da_mostro(ident, squadra, reg):
    d = carica("mostri", ident)
    m = d["mechanics_5e"]
    nome = d["name"]["it"]

    azioni = [(b["name"], b.get("effetto")) for b in (m.get("actions") or [])]
    tratti = [(b["name"], b.get("effetto")) for b in (m.get("traits") or [])]

    for n, e in azioni + tratti:
        if e is None:
            reg.lacuna(
                f"blocco-senza-effetto:{ident}:{n}",
                f"{nome}: il blocco «{n}» non ha `effetto`",
                "il motore lo ignora. L'assenza di `effetto` non distingue "
                "«non ha meccanica» da «non e' ancora strutturato»: sono due "
                "cose diverse e nei dati si scrivono uguali")

    cr = (m.get("challenge_rating") or {}).get("proficiency_bonus")
    if cr is None:
        reg.lacuna(f"competenza:{ident}", f"{nome}: nessun bonus di competenza",
                   "assunto 2")
        cr = 2

    immuni = m.get("condition_immunities") or []
    ignote = [c for c in immuni if c not in CONDIZIONI]
    if ignote:
        reg.lacuna(
            "condizione-non-modellata",
            f"immunita' a condizioni che il catalogo non modella: "
            f"{', '.join(sorted(set(ignote)))}",
            "il vocabolario le NOMINA — l'insieme delle quindici condizioni "
            "SRD e' chiuso e noto — ma `dati/condizioni/` non le converte "
            "ancora, quindi il motore non saprebbe applicarle nemmeno a chi "
            "non e' immune. E' una lacuna del nostro catalogo, non una "
            "condizione inesistente, e la "
            "decisione 48 (`condizioni-a-consumo`) vuole che si chiuda "
            "quando un blocco "
            "convertito la impone. Il punto e' che il motore lo SA: "
            "un'immunita' a una condizione che non sa applicare, ignorata in "
            "silenzio, sarebbe indistinguibile da un'immunita' rispettata")

    return Combattente(
        nome=nome,
        ca=m["armor_class"]["value"],
        pf=m["hit_points"]["average"],
        abilities=dict(m["abilities"]),
        azioni=azioni, tratti=tratti, squadra=squadra, competenza=cr,
        difese={"resistenze": m.get("damage_resistances") or [],
                "immunita": m.get("damage_immunities") or [],
                "vulnerabilita": m.get("damage_vulnerabilities") or []},
        immunita_condizione=immuni)


# --------------------------------------------------------------- personaggio
#
# GLI INGRESSI, E NIENT'ALTRO. Sul mostro `attacco` e' un campo letto dalla
# scheda; sul personaggio era una funzione di questo modulo, e le due cose
# avevano lo stesso nome pur non essendo la stessa cosa. La risposta non e'
# far memorizzare l'attacco al personaggio — sarebbe un derivato scritto a
# mano, che CLAUDE.md 3 vieta per una ragione gia' pagata quattro volte — ne'
# far derivare l'attacco al mostro, che vorrebbe dire inventare derivazioni
# che la fonte non da'. Cio' che i due lati condividono non e' il CAMPO: e'
# la LETTURA, e si chiama `attacco_di()`.
#
# Il personaggio porta quindi solo cio' che non e' derivabile da nient'altro:
# razza, classe, livello, punteggi, cosa ha equipaggiato, quali scelte ha
# fatto. Ogni campo ricavabile da questi NON PUO' esistere qui dentro — non
# «e' sconsigliato», non puo': il costruttore solleva. E' la forma piu' forte
# del divieto, la stessa che ha reso impossibile e non solo sconsigliato
# fissare un ospite (decisione 39, `bersaglio-legale-filtro`).

INGRESSI = ("razza", "classe", "livello", "punteggi", "equipaggiato", "scelte")

# I nomi che un derivato prenderebbe. L'elenco non e' esaustivo e non puo'
# esserlo — nessun elenco di nomi vietati lo e' — ma copre cio' che oggi il
# motore calcola, che e' esattamente cio' che qualcuno sarebbe tentato di
# scrivere qui per non ricalcolarlo.
DERIVATI = ("ca", "classe_armatura", "pf", "punti_ferita", "pf_max",
            "attacco", "attacchi", "bonus_colpire", "danno", "competenza",
            "iniziativa", "tiri_salvezza", "velocita", "difese",
            "resistenze", "immunita", "vulnerabilita")


class Personaggio:
    """Gli ingressi di un personaggio. Nessun derivato, per costruzione."""

    def __init__(self, **campi):
        vietati = sorted(set(campi) & set(DERIVATI))
        if vietati:
            raise ValueError(
                f"{', '.join(vietati)}: sono derivati dagli ingressi e non "
                f"possono essere scritti su un Personaggio. Chi li vuole "
                f"chiede al motore di comporli — attacco_di(), ca_di(), "
                f"pf_di() — e non li memorizza: un derivato scritto si sfasa "
                f"al primo cambio d'arma o di livello")
        ignoti = sorted(set(campi) - set(INGRESSI))
        if ignoti:
            raise ValueError(f"ingressi sconosciuti: {', '.join(ignoti)}. "
                             f"Quelli previsti sono {', '.join(INGRESSI)}")
        mancanti = sorted(set(INGRESSI) - set(campi))
        if mancanti:
            raise ValueError(f"ingressi mancanti: {', '.join(mancanti)}")
        for k, v in campi.items():
            setattr(self, k, v)
        self._doc = {}

    # --- i documenti che gli ingressi nominano, letti una volta sola
    def documento(self, cartella, ident):
        chiave = (cartella, ident)
        if chiave not in self._doc:
            if cartella == "razze":
                self._doc[chiave] = generazione().carica_razza(ident)
            elif cartella == "classi":
                self._doc[chiave] = generazione().carica_classe(ident)
            else:
                self._doc[chiave] = carica(cartella, ident)
        return self._doc[chiave]

    def doc_classe(self):
        return self.documento("classi", self.classe)["mechanics_5e"]

    def doc_oggetto(self, ruolo):
        return self.documento("oggetti", self.equipaggiato[ruolo])

    def privilegi(self):
        """I privilegi del chassis che portano un `effetto`."""
        return {f["name"]: f["effetto"]
                for f in (self.doc_classe().get("chassis_features") or [])
                if f.get("effetto")}


def generazione():
    sys.path.insert(0, BASE)
    from motore import generazione as g
    return g


# ------------------------------------------------------ i derivati, composti

def competenza_di(p):
    return sistema.competenza(p.livello)


def _modificatori_dello_stile(p, reg):
    """(bonus al danno, bonus alla CA) dallo stile di combattimento scelto."""
    stile = (p.scelte or {}).get("stile")
    if not stile:
        return 0, 0
    privilegi = p.privilegi()
    if stile not in privilegi:
        raise KeyError(f"lo stile '{stile}' non e' fra i privilegi del "
                       f"chassis di {p.classe}")
    danno = ca = 0
    for m_ in (privilegi[stile].get("modificatori") or []):
        if m_["bersaglio"] == "danno":
            danno += m_["valore"]
        elif m_["bersaglio"] == "ca":
            ca += m_["valore"]
    if reg:
        reg.lacuna("condizione-modificatore",
                   f"stile «{stile}»: la condizione di applicazione è prosa",
                   f"«{(privilegi[stile]['modificatori'][0] or {}).get('condizione_di_applicazione')}» — "
                   "il motore la considera sempre vera perché non c'è nessun "
                   "campo che dica come verificarla")
    return danno, ca


def ca_di(p, reg=None):
    """Classe Armatura: armatura + Destrezza (col tetto) + scudo + stile."""
    ca5 = p.doc_oggetto("armatura")["mechanics_5e"]["armor_5e"]["ca_5e"]
    ca = ca5["ca_base"]
    if ca5["applica_mod_dex"]:
        m_dex = mod(p.punteggi["dex"])
        if ca5["mod_dex_max"] is not None:
            m_dex = min(m_dex, ca5["mod_dex_max"])
        ca += m_dex
    scudo = p.doc_oggetto("scudo")["mechanics_5e"]["armor_5e"]["ca_5e"]
    ca += scudo["bonus_ca"] or 0
    return ca + _modificatori_dello_stile(p, reg)[1]


def pf_di(p, reg=None):
    """Punti ferita: massimo al 1° livello, media ai successivi."""
    dv = p.doc_classe().get("hit_die")
    if not dv:
        if reg:
            reg.lacuna(f"hit_die:{p.classe}",
                       f"{p.classe}: nessun dado vita nello strato 5e",
                       "assunto 1d8")
        dv = "1d8"
    faccia = int(_DADO.match(dv).group(2))
    m_con = mod(p.punteggi["con"])
    if reg:
        reg.lacuna("pf-primo-livello",
                   "punti ferita del personaggio",
                   "massimo al 1° livello e media ai successivi: e' la regola "
                   "5e, ma nessun campo dei dati la dichiara — il dado vita "
                   "c'e', la procedura che lo usa no")
    return faccia + m_con + (p.livello - 1) * (faccia // 2 + 1 + m_con)


def competente_nell_arma(p, reg=None):
    arma = p.doc_oggetto("arma")["mechanics_5e"]["weapon_5e"]
    categorie = ((p.doc_classe().get("structural") or {})
                 .get("weapon_proficiencies") or {}).get("categorie") or []
    competente = arma["categoria"] in categorie
    if not competente and reg:
        reg.lacuna("competenza-arma",
                   f"{p.classe} non e' competente in armi "
                   f"«{arma['categoria']}»",
                   "il bonus di competenza non si somma")
    return competente


def _attacco_composto(p, reg=None):
    """L'attacco del personaggio, nella forma `effetto.attacco`.

    Composto da arma + caratteristica + competenza + stile, cioe' dagli
    ingressi e da nient'altro. Nessuno di questi numeri e' scritto da
    nessuna parte, ed e' il punto: se cambia l'arma o il livello, cambia
    qui e in nessun altro posto."""
    arma = p.doc_oggetto("arma")["mechanics_5e"]["weapon_5e"]
    car = "dex" if arma["proprieta_5e"]["finesse"] else "str"
    comp = competenza_di(p) if competente_nell_arma(p, reg) else 0
    bonus_danno = _modificatori_dello_stile(p, reg)[0]
    if reg:
        reg.lacuna("nessuna-posizione",
                   "portata e gittata sono campi popolati e mai letti",
                   "il motore non ha una griglia ne' distanze: ogni "
                   "combattente e' a portata di ogni altro. `portata_ft` e "
                   "`gittata_ft` esistono nei dati e questo scontro non li "
                   "usa — un'arma a distanza e una da mischia si comportano "
                   "uguale")
    return {
        "tipo": "mischia_arma" if arma["tipo"] == "mischia" else "distanza_arma",
        "bonus_colpire": mod(p.punteggi[car]) + comp,
        "portata_ft": arma["proprieta_5e"]["portata_ft"],
        "bersagli": 1,
        "danno": [{"dadi": arma["damage_dice"],
                   "bonus": mod(p.punteggi[car]) + bonus_danno,
                   "tipo": arma["damage_type"]}],
    }


# --------------------------------------------------------------- attacco_di
#
# LA LETTURA UNICA. Chi la chiama non sa se ha davanti un mostro o un
# personaggio, ed e' questo il senso di «la stessa cosa da entrambe le
# parti». La forma della risposta e' `effetto.attacco` di
# effetto.schema.json, che esisteva gia' e non cambia.

def attacco_di(combattente, azione=None, reg=None):
    """L'attacco di un combattente: sul mostro letto, sul personaggio composto.

    `azione` nomina il blocco da usare quando il portatore ne ha piu' d'uno
    (un mostro con morso e artigli); omesso, si prende il primo che porti un
    attacco. Torna `None` se non ce n'e' nessuno."""
    p = getattr(combattente, "personaggio", None)
    if p is not None:
        return _attacco_composto(p, reg)

    eff = combattente.azione(azione) if azione else None
    if eff is None:
        for _nome, e in combattente.azioni:
            if e and e.get("attacco"):
                eff = e
                break
    att = (eff or {}).get("attacco")
    # L'ORIGINE SI LEGGE, NON SI DEDUCE. Decisione 54 (`origine-e-un-dato`):
    # un bonus letto dalla scheda e uno rifatto col conto si scrivono
    # identici, quindi il motore non puo' ricavarla dai numeri. La lacuna
    # resta, ma adesso e' CONDIZIONATA AL DATO: scatta esattamente sugli
    # attacchi che non la dichiarano, non su tutti. Cosi' il conteggio delle
    # lacune misura quanto bestiario e' ancora scoperto invece di segnalare
    # per sempre un difetto gia' chiuso.
    if (att is not None and reg is not None
            and att.get("bonus_colpire") is not None
            and not att.get("bonus_origine")):
        reg.lacuna(
            "attacco-origine-non-dichiarata",
            "il bonus di attacco del mostro non dice da dove viene",
            "letto dalla scheda o rifatto col conto (competenza + "
            "modificatore) si scrivono uguali, e nessun controllo puo' "
            "distinguerli quando coincidono. Il campo esiste dalla "
            "decisione 54 (`origine-e-un-dato`) — `bonus_origine` accanto a "
            "`bonus_colpire` — e questo attacco non lo porta. Quanto "
            "bestiario sia ancora scoperto e' una misura, ed e' in "
            "`motore/arena.py` → `coincidenze_di_attacco()`")
    return att


def combattente_da(p, reg, nome="Personaggio", squadra="eroi"):
    """Il combattente che gioca il turno, DERIVATO dagli ingressi.

    Il Combattente e' stato di scontro — punti ferita correnti, condizioni,
    risorse spese — e non una scheda: ogni numero di scheda che porta viene
    da qui, cioe' da una funzione, e nessuno da un campo scritto a mano."""
    tratti = [(n, e) for n, e in p.privilegi().items()
              if e.get("guarigione") or e.get("risorsa")]

    reg.lacuna("difese-del-pg",
               "resistenze e immunita' del personaggio",
               "il mostro le porta in `damage_resistances`, "
               "`damage_immunities`, `damage_vulnerabilities`; il "
               "personaggio non ha nessun campo dove averle, e nessuna "
               "regola che le componga da razza e classe. Qui e' senza "
               "difese, che oggi e' vero per un Cavaliere della Corona "
               "umano ma lo e' per assenza di dato, non per verifica")

    pg = Combattente(
        nome=nome, ca=ca_di(p, reg), pf=pf_di(p, reg),
        abilities=dict(p.punteggi),
        # L'azione NON porta l'attacco: lo compone `attacco_di()` quando
        # serve. Un attacco memorizzato qui sarebbe di nuovo un derivato
        # scritto, buono finche' nessuno cambia arma.
        azioni=[("Attacco", {"azione": "azione"})],
        tratti=tratti, squadra=squadra, competenza=competenza_di(p),
        giocante=True)
    pg.personaggio = p
    pg.livello = p.livello
    pg.arma_magica = p.doc_oggetto("arma")["magico"]
    for nome_p, eff in tratti:
        ris = eff.get("risorsa") or {}
        usi = ris.get("usi")
        if isinstance(usi, dict):
            usi = usi["per_livello"].get(str(p.livello), 0)
        pg.risorse[nome_p] = usi or 0
    return pg


# ------------------------------------------------------------------ attacco
def applica_difese(contro, grezzi, reg, magico=None):
    """Il danno per tipo contro resistenze, immunita' e vulnerabilita'.

    E' il primo punto in cui il motore CONFRONTA un tipo di danno con una
    difesa, ed e' il confronto che fino al 02/09/2026 non poteva riuscire:
    l'arma diceva `slashing` (inglese, dall'SRD) e la scheda del mostro
    diceva `bludgeoning, piercing, and slashing from nonmagical attacks` —
    una frase dentro un array di stringhe. Ora i due lati parlano lo stesso
    vocabolario (dati/schema/vocabolari.schema.json) e la clausola e' un
    campo (`solo_se`), quindi il confronto e' un `==`.

    Torna (totale, righe_di_registro)."""

    def vale(voce):
        """La difesa si applica a questo colpo?"""
        if not voce.get("solo_se"):
            return True
        if magico is None:
            reg.lacuna(
                "attacco-magico-non-dichiarato",
                f"la difesa vale solo «{voce['solo_se']}» e non si sa se "
                f"l'attacco e' magico",
                "nessun campo dice se un attacco e' magico: sull'arma di un "
                "personaggio c'e' `magico`, sull'azione di un mostro non "
                "c'e' niente. Il motore assume NON magico, cioe' la "
                "condizione soddisfatta, che e' l'assunzione favorevole al "
                "difensore e va detta")
            return True
        return not magico

    def cerca(elenco, tipo):
        return any(v["tipo"] == tipo and vale(v) for v in elenco)

    # Il moltiplicatore di ogni difesa e il loro ORDINE vengono da
    # dati/sistema/moltiplicatori-difesa.json. L'ordine, in particolare,
    # era la sequenza delle righe di questa funzione: una regola scritta
    # in una posizione del codice, che e' la forma piu' silenziosa in cui
    # una regola possa vivere — non ha nemmeno un nome da cercare.
    CAMPO = {"immunita": "immunita", "vulnerabilita": "vulnerabilita",
             "resistenza": "resistenze"}
    PAROLA = {"immunita": "immune", "vulnerabilita": "vulnerabile",
              "resistenza": "resistente"}

    totale, righe = 0, []
    for n, tipo in grezzi:
        d = contro.difese
        if cerca(d["immunita"], tipo):
            righe.append(f"{n} {tipo} annullati (immune)")
            continue
        note = []
        for difesa in sistema.ORDINE_DIFESE:
            if difesa == "immunita":
                continue
            if cerca(d[CAMPO[difesa]], tipo):
                n = sistema.applica_moltiplicatore(n, difesa)
                note.append(PAROLA[difesa])
        righe.append(f"{n} {tipo}" + "".join(f", {x}" for x in note))
        totale += n
    return totale, righe


def risolvi_attacco(chi, contro, azione, reg, rng, magico=None):
    """Un attacco, dal tiro al danno. NON sa chi lo sta tirando.

    Prende il NOME dell'azione e non il suo `effetto`, perche' e'
    `attacco_di()` a sapere se quel nome va letto da una scheda o composto
    da un personaggio. Questa funzione vede solo la forma comune."""
    att = attacco_di(chi, azione, reg)
    etichetta = azione
    # Qui stava la lacuna `regole-di-sistema`, ed e' stata CHIUSA dal
    # criterio a tre domande (decisione 51, `criterio-meccanica`), non da una
    # riga di codice. Il taglio: i NUMERI di questa procedura — il 20 e l'1
    # naturale, i moltiplicatori delle difese, il modificatore e il bonus di
    # competenza — sono dati di sistema in dati/sistema/, con schema,
    # validatore e controllo anti-duplicazione; la PROCEDURA che li usa
    # (tira, somma, confronta con la CA, raddoppia i dadi sul critico) resta
    # codice perche' e' una procedura, e questa e' la risposta invece che una
    # mancanza. Toglierla dal registro non e' un'assoluzione: e' che una
    # lacuna che descrive lo stato deciso non e' piu' una lacuna, e lasciarla
    # gonfierebbe il conto con una voce che non chiede piu' niente.
    vant = ha_clausola(contro.condizioni, "vantaggio_attacchi_contro")
    svant = ha_clausola(chi.condizioni, "svantaggio_attacchi_propri")
    dado, nota = d20(rng, vant, svant)
    totale = dado + att["bonus_colpire"]
    critico = dado == sistema.CRITICO_NATURALE

    if not critico and (dado == sistema.FALLIMENTO_NATURALE
                        or totale < contro.ca):
        reg.riga(f"      {etichetta}: {dado}{nota}+{att['bonus_colpire']} = "
                 f"{totale} contro CA {contro.ca} — manca")
        return 0

    grezzi = []
    for d in att["danno"]:
        n = tira(d["dadi"], rng)
        if critico:
            n += tira(d["dadi"], rng)
        n += d.get("bonus") or 0
        grezzi.append((n, d["tipo"]))

    danno, pezzi = applica_difese(contro, grezzi, reg, magico=magico)

    if ha_clausola(contro.condizioni, "resistenza_a_tutti_i_danni"):
        danno = sistema.applica_moltiplicatore(danno, "resistenza")
        pezzi.append("dimezzato dalla resistenza")

    reg.riga(f"      {etichetta}: {dado}{nota}+{att['bonus_colpire']} = "
             f"{totale} contro CA {contro.ca} — "
             f"{'CRITICO, ' if critico else ''}colpisce, {danno} danni "
             f"({', '.join(pezzi)})")
    applica_danno(contro, danno, reg, rng)
    return danno


def applica_danno(chi, danno, reg, rng):
    chi.pf -= danno
    if chi.pf > 0:
        reg.riga(f"      {chi.nome}: {chi.pf}/{chi.pf_max} punti ferita")
        return
    chi.pf = 0
    if chi.giocante:
        chi.condizioni.add("incosciente")
        reg.riga(f"      {chi.nome} scende a 0 punti ferita: incosciente.")
        reg.lacuna("tiri-salvezza-contro-morte",
                   "il personaggio a 0 punti ferita",
                   "resta incosciente e fuori dallo scontro. I tiri salvezza "
                   "contro morte non sono modellati: la nota di "
                   "dati/condizioni/incosciente.json lo dichiara gia' — sono "
                   "una procedura del Personaggio, e il Personaggio non c'e'")
    else:
        chi.morto = True
        reg.riga(f"      {chi.nome} muore.")
        alla_morte(chi, reg, rng)


# -------------------------------------------------- tratti che scattano alla morte
def alla_morte(chi, reg, rng):
    for nome, eff in chi.tratti:
        if nome not in TRATTI_ALLA_MORTE:
            continue
        reg.lacuna("innesco-non-dichiarato",
                   f"«{nome}» si innesca alla morte del portatore",
                   "nessun campo lo dice: `azione: nessuna` significa «non "
                   "costa un'azione», non «scatta a 0 punti ferita». Il "
                   "motore riconosce il tratto DAL NOME, che e' l'unico "
                   "appiglio che i dati offrono")
        if eff is None:
            continue
        ts = eff.get("tiro_salvezza")
        if not ts:
            continue
        reg.riga(f"      → {nome} ({chi.nome})")
        reg.lacuna("bersagli-dell-area",
                   f"«{nome}» colpisce «ogni creatura entro 5 piedi»",
                   "il motore lo applica a tutti gli AVVERSARI: non c'e' "
                   "posizione, non c'e' distanza, e l'area non ha un campo "
                   "(la prosa dice 5 piedi, `effetto` non ha dove metterlo). "
                   "Ne segue un errore di regola dichiarato: la fonte dice "
                   "«ogni creatura», quindi anche gli alleati del Baaz, e "
                   "qui non li colpisce")
        for bersaglio in chi.arena_avversari:
            if bersaglio.morto or "pietrificato" in bersaglio.condizioni:
                continue
            tiro_salvezza(bersaglio, ts, chi, nome, reg, rng, primo=True)


def tiro_salvezza(chi, ts, fonte, nome_effetto, reg, rng, primo):
    car = ts["caratteristica"]
    svant = ha_clausola(chi.condizioni, "svantaggio_tiri_salvezza", car)
    auto_fallito = ha_clausola(chi.condizioni, "fallisce_tiri_salvezza", car)
    if auto_fallito:
        dado, nota, totale = 0, " (fallimento automatico)", 0
    else:
        dado, nota = d20(rng, False, svant)
        totale = dado + mod(chi.ab[car])
    ok = (not auto_fallito) and totale >= ts["cd"]
    reg.riga(f"      {chi.nome}, tiro salvezza {car.upper()} CD {ts['cd']}: "
             f"{dado}{nota}{'' if auto_fallito else '+' + str(mod(chi.ab[car]))}"
             f" = {totale} — {'superato' if ok else 'fallito'}")

    esito = ts.get("successo") if ok else (
        ts.get("fallimento") if primo else ts.get("fallimento_ripetuto"))
    applica_esito(chi, esito, reg)

    if ok:
        chi.salvezze_in_sospeso = [s for s in chi.salvezze_in_sospeso
                                   if s[0] != nome_effetto]
        for cid in list(chi.condizioni):
            if cid == "trattenuto":
                chi.condizioni.discard(cid)
                reg.riga(f"      {chi.nome} non e' piu' trattenuto.")
        return

    if primo and ts.get("ripetibile"):
        chi.salvezze_in_sospeso.append((nome_effetto, ts, ts["ripetibile"]))
        reg.riga(f"      → si ripete: {ts['ripetibile']}")


def applica_esito(chi, esito, reg):
    if not esito or esito.get("nessuno"):
        return
    for d in (esito.get("danno") or []):
        pass  # nessun danno in gioco nella fetta
    for c in (esito.get("condizioni") or []):
        nome = CONDIZIONI[c["id"]]["name"]["it"].lower()
        # L'immunita' si confronta per id, e il confronto e' un `==` solo
        # perche' i due lati parlano lo stesso vocabolario: prima del
        # 02/09/2026 la scheda diceva `petrified` e la condizione si
        # chiamava `pietrificato`, quindi nessuna immunita' del bestiario
        # poteva essere rispettata da nessun motore.
        if c["id"] in chi.immunita_condizione:
            reg.riga(f"      {chi.nome} e' immune a «{nome}»: non si applica.")
            continue
        chi.condizioni.add(c["id"])
        durata = f", {c['durata']}" if c.get("durata") else ""
        reg.riga(f"      {chi.nome} diventa {nome}{durata}.")


# --------------------------------------------------------------------- turno
def turno(chi, avversari, reg, rng):
    vivi = [a for a in avversari if a.in_gioco()]
    if not chi.puo_agire():
        stato = ", ".join(sorted(chi.condizioni)) or "fuori gioco"
        reg.riga(f"   {chi.nome}: non puo' agire ({stato})")
        fine_turno(chi, reg, rng)
        return
    if not vivi:
        return
    bersaglio = vivi[0]

    # azione bonus: Recuperare il fiato, se conviene
    for nome, eff in chi.tratti:
        if eff is None:
            continue
        gua = eff.get("guarigione")
        if not gua or chi.risorse.get(nome, 0) <= 0:
            continue
        if chi.pf > chi.pf_max // 2 or chi.pf <= 0:
            continue
        n = tira(gua["dadi"], rng) + (chi.livello if gua.get("piu_livello_classe") else 0)
        chi.risorse[nome] -= 1
        chi.pf = min(chi.pf_max, chi.pf + n)
        reg.riga(f"   {chi.nome} — azione bonus: {nome}, +{n} punti ferita "
                 f"({chi.pf}/{chi.pf_max})")
        reg.lacuna("quando-usare-una-risorsa",
                   f"«{nome}»: i dati dicono cosa fa e quanti usi ha",
                   "non dicono QUANDO usarlo. La politica («sotto meta' dei "
                   "punti ferita») e' del motore, non dei dati: e' materia "
                   "dell'IA di combattimento, la stessa casella in cui la "
                   "decisione 27 (`sette-campi-2e`) ha messo il morale")

    azioni_da_spendere = 1
    for nome, eff in chi.tratti:
        if eff is None:
            continue
        ris = eff.get("risorsa") or {}
        mods = eff.get("modificatori") or []
        if any(m["bersaglio"] == "azioni_per_turno" for m in mods) \
                and chi.risorse.get(nome, 0) > 0 and chi.pf <= chi.pf_max // 2:
            chi.risorse[nome] -= 1
            azioni_da_spendere += [m["valore"] for m in mods
                                   if m["bersaglio"] == "azioni_per_turno"][0]
            reg.riga(f"   {chi.nome} — {nome}: un'azione in piu' questo turno")

    for _ in range(azioni_da_spendere):
        if not bersaglio.in_gioco():
            vivi = [a for a in avversari if a.in_gioco()]
            if not vivi:
                break
            bersaglio = vivi[0]
        agisci(chi, bersaglio, reg, rng)

    fine_turno(chi, reg, rng)


def agisci(chi, bersaglio, reg, rng):
    scelta = None
    for nome, eff in chi.azioni:
        if eff and eff.get("multiattacco"):
            scelta = (nome, eff)
            break
    if scelta is None:
        # Quali azioni siano attacchi si chiede ad `attacco_di()`, non al
        # campo: sul personaggio quel campo non c'e' e l'attacco esiste
        # lo stesso. Era qui che le due parti si comportavano diverso.
        for nome, eff in chi.azioni:
            if attacco_di(chi, nome) is not None:
                scelta = (nome, eff)
                break
    if scelta is None:
        reg.riga(f"   {chi.nome}: nessuna azione strutturata da usare")
        return

    nome, eff = scelta
    if eff.get("multiattacco"):
        ma = eff["multiattacco"]
        reg.riga(f"   {chi.nome} — {nome}: {ma['quanti']} × {ma['azione']} "
                 f"contro {bersaglio.nome}")
        for _ in range(ma["quanti"]):
            if not bersaglio.in_gioco():
                break
            risolvi_attacco(chi, bersaglio, ma["azione"], reg, rng,
                            magico=getattr(chi, "arma_magica", None))
    else:
        reg.riga(f"   {chi.nome} — {nome} contro {bersaglio.nome}")
        risolvi_attacco(chi, bersaglio, nome, reg, rng,
                        magico=getattr(chi, "arma_magica", None))


def fine_turno(chi, reg, rng):
    for nome_effetto, ts, quando in list(chi.salvezze_in_sospeso):
        chi.salvezze_in_sospeso.remove((nome_effetto, ts, quando))
        reg.riga(f"      → {nome_effetto}: tiro ripetuto ({quando})")
        tiro_salvezza(chi, ts, None, nome_effetto, reg, rng, primo=False)


# -------------------------------------------------------------------- scontro
def scontro(eroi, mostri, reg, rng, max_round=30):
    tutti = eroi + mostri
    for c in tutti:
        c.arena_avversari = mostri if c.squadra == "eroi" else eroi
    for c in eroi:
        c.arena_avversari = mostri
    for c in mostri:
        c.arena_avversari = eroi

    iniziativa = []
    for c in tutti:
        d = rng.randint(1, 20)
        iniziativa.append((d + mod(c.ab["dex"]), d, c))
    iniziativa.sort(key=lambda t: (-t[0], -t[1], t[2].nome))
    reg.riga("Iniziativa:")
    for tot, d, c in iniziativa:
        reg.riga(f"   {tot:2d}  {c.nome}  (d20 {d} + DES {mod(c.ab['dex']):+d})")
    reg.lacuna("iniziativa",
               "il bonus di iniziativa",
               "calcolato qui come modificatore di Destrezza. Nessun campo lo "
               "porta, ne' sul mostro ne' sulla classe")

    reg.lacuna("fine-dello-scontro",
               "quando finisce uno scontro",
               "qui: quando una delle due parti non ha piu' nessuno che "
               "possa agire. Non e' un dato — ed e' la definizione che il "
               "Baaz mette alla prova, perche' una creatura pietrificata non "
               "e' morta, ha ancora i suoi punti ferita")
    for c in tutti:
        if getattr(c, "giocante", False):
            continue
        reg.lacuna("morale-non-letto",
                   "il morale dei mostri non entra nello scontro",
                   "la decisione 27 (`sette-campi-2e`) lo destina all'IA di "
                   "combattimento e ogni mostro lo porta in `morale_2e`; qui "
                   "nessuno lo legge, e i mostri combattono fino alla morte. "
                   "Il Traag e' il caso peggiore: il suo morale ha due stati "
                   "(8 prima dello scontro, nessun controllo dopo), e "
                   "ignorarlo cancella il suo tratto identitario")
            
    ordine = [c for _, _, c in iniziativa]
    for numero in range(1, max_round + 1):
        reg.riga(f"\n── Round {numero} " + "─" * 40)
        for c in ordine:
            if c.morto:
                continue
            avv = c.arena_avversari
            if not any(a.in_gioco() for a in avv):
                break
            turno(c, avv, reg, rng)
        eroi_vivi = any(c.in_gioco() for c in eroi)
        mostri_vivi = any(c.in_gioco() for c in mostri)
        if not eroi_vivi or not mostri_vivi:
            reg.riga("")
            if eroi_vivi and not mostri_vivi:
                esito = "eroi"
            elif mostri_vivi and not eroi_vivi:
                esito = "mostri"
            else:
                esito = "nessuno"
            return esito, numero
    return "tempo scaduto", max_round
