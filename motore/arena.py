#!/usr/bin/env python3
"""
L'arena della fetta verticale: il primo scontro giocato con questi dati.

COSA FA
    Tre scenari, tutti con lo stesso personaggio — un Cavaliere della Corona
    di 2° livello, chassis Fighter, spada lunga e cotta di maglia:

      1. contro il Traag           (turni, multiattacco, danno, morte)
      2. contro il Baaz            (Death Throes, le sue due condizioni)
      3. contro Traag e Baaz insieme

    Di ciascuno stampa il registro completo di uno scontro con seme fissato,
    poi ripete lo scenario mille volte per vedere se l'esito e' stabile o se
    quel singolo registro era un caso fortunato.

COSA MISURA DAVVERO
    Non chi vince. Le LACUNE: ogni volta che il motore ha dovuto supplire a
    un dato assente lo ha dichiarato, e l'elenco in fondo e' il risultato.
    Uno scontro che gira non dimostra che i dati bastano; un elenco di lacune
    vuoto lo dimostrerebbe.

RIDUZIONE — CLAUDE.md, punti 1 e 2
    Un registro di combattimento contiene per forza i numeri di scheda dei
    mostri: Classe Armatura, punti ferita, bonus di attacco, dadi di danno.
    Per il Baaz quei numeri vengono da Shadow of the Dragon Queen, che e' un
    manuale protetto, e per il Traag dalla nostra conversione di una scheda
    dell'MC Appendix: e' esattamente il materiale che `.gitignore` tiene fuori
    dal repository pubblico. Quindi due uscite dalla stessa esecuzione, con la
    riduzione come parametro del generatore e non come taglio a valle:

      dati/RAPPORTO-arena.md           pubblico — metodo, lacune, statistiche
      dati/RAPPORTO-arena-completo.md  privato  — i registri per esteso

    La guardia in fondo verifica che nessuna riga di registro e nessun numero
    di scheda sia finito nel documento pubblico.

Uso:  python3 motore/arena.py            stampa a video ed emette i due rapporti
      python3 motore/arena.py --solo-video
"""

import os
import random
import re
import sys
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from motore import combattimento as C   # noqa: E402
from decisioni import cita  # noqa: E402

# Il personaggio della fetta. I punteggi sono l'array standard assegnato a
# mano; la scelta e' nostra, non un dato — un personaggio non ha ancora una
# sede in dati/.
PUNTEGGI = {"str": 15, "dex": 13, "con": 14, "int": 10, "wis": 12, "cha": 8}


# Gli INGRESSI del personaggio, e nient'altro: nessuna Classe Armatura,
# nessun punto ferita, nessun bonus di attacco. Tutto cio' che manca qui e'
# derivabile da cio' che c'e', e il motore lo deriva quando serve —
# decisione 52 (`attacco-unica-lettura`).
INGRESSI_EROE = dict(
    razza="umano", classe="cavaliere-corona", livello=2, punteggi=PUNTEGGI,
    equipaggiato={"arma": "longsword", "armatura": "chain-mail",
                  "scudo": "shield"},
    scelte={"stile": "Duello"})


def eroe(reg, nome="Sir Aldric"):
    return C.combattente_da(C.Personaggio(**INGRESSI_EROE), reg, nome=nome)


def scheda(c):
    return (f"{c.nome}: CA {c.ca}, {c.pf_max} punti ferita, "
            f"competenza +{c.competenza}, "
            + " ".join(f"{k.upper()} {v}" for k, v in c.ab.items()))


def qualunque(pg, mostri, esito):
    return True


def col_death_throes(pg, mostri, esito):
    """Il registro da stampare deve MOSTRARE i due tempi del tratto: non basta
    che il Baaz muoia, serve che il tiro salvezza fallisca due volte."""
    return "pietrificato" in pg.condizioni


SCENARI = [
    ("1. Cavaliere della Corona contro Traag", ["traag"], qualunque),
    ("2. Cavaliere della Corona contro Baaz", ["draconico-baaz"], col_death_throes),
    ("3. Cavaliere della Corona contro Traag e Baaz",
     ["traag", "draconico-baaz"], qualunque),
]


def gira(mostri_id, seme, reg=None):
    reg = reg or C.Registro()
    rng = random.Random(seme)
    pg = eroe(reg)
    mostri = [C.da_mostro(m, "mostri", reg) for m in mostri_id]
    esito, round_ = C.scontro([pg], mostri, reg, rng)
    return reg, esito, round_, pg, mostri


RIPETIZIONI = 1000


def esegui():
    """Una sola esecuzione completa: registri dimostrativi + statistiche."""
    seme = 20260902
    scenari = []
    lacune = C.Registro()
    for titolo, mostri_id, voluto in SCENARI:
        # Il seme del registro dimostrativo si cerca, non si sceglie a caso:
        # uno scontro in cui il ramo che si vuole mostrare non si prende non
        # dimostra niente. La ricerca e' dichiarata e il seme e' stampato.
        for tentativo in range(2000):
            reg, esito, round_, pg, mostri = gira(mostri_id, seme + tentativo)
            if voluto(pg, mostri, esito):
                break

        conteggio = collections_Counter()
        round_tot = 0
        pietrificati = 0
        for i in range(RIPETIZIONI):
            r2, e2, rd2, pg2, ms2 = gira(mostri_id, 10_000_000 + i)
            conteggio[e2] += 1
            round_tot += rd2
            if "pietrificato" in pg2.condizioni:
                pietrificati += 1
            for k, v in r2.lacune.items():
                lacune.lacuna(k, *v)

        scenari.append({
            "titolo": titolo, "mostri": mostri_id, "seme": seme + tentativo,
            "registro": reg, "esito": esito, "round": round_,
            "pg": pg, "schede": [pg] + mostri,
            "conteggio": conteggio, "round_medi": round_tot / RIPETIZIONI,
            "pietrificati": pietrificati,
        })
    return scenari, lacune


def collections_Counter():
    import collections
    return collections.Counter()


# ------------------------------------------------------------------ rapporti
def conta_multiattacchi():
    """Quanti blocchi di multiattacco ci sono nel bestiario, e quante azioni."""
    import glob
    import json
    n_multi = n_azioni = 0
    for f in sorted(glob.glob(os.path.join(BASE, "dati", "mostri", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for a in (d["mechanics_5e"].get("actions") or []):
            n_azioni += 1
            if re.search(r"attacchi multipli|multiattack", a["name"], re.I):
                n_multi += 1
    return n_multi, n_azioni


def blocchi_strutturati():
    """Cosa porta un `effetto` e cosa no, nei due mostri della fetta."""
    import json
    fuori = []
    for ident in ("traag", "draconico-baaz"):
        d = json.load(open(os.path.join(BASE, "dati", "mostri", ident + ".json"),
                           encoding="utf-8"))
        m = d["mechanics_5e"]
        for gruppo in ("traits", "actions", "bonus_actions", "reactions"):
            for b in (m.get(gruppo) or []):
                fuori.append((d["name"]["it"], gruppo, b["name"],
                              b.get("effetto") is not None,
                              sorted(k for k in (b.get("effetto") or {})
                                     if k not in ("nota", "azione"))))
    return fuori


def prova_delle_difese():
    """Il confronto fra tipo di danno e difesa, provato su casi veri.

    Serve perche' nessuno dei tre scenari lo esercita: ne' il Traag ne' il
    Baaz hanno difese per tipo, quindi `applica_difese` gira sempre sul ramo
    vuoto e "l'arena passa" non direbbe niente.

    Le schede NON sono scelte a mano: si cercano nel bestiario quelle che
    portano ciascuna forma — resistenza con clausola, immunita',
    vulnerabilita' — perche' una prova costruita su un caso inventato prova
    il codice e non i dati. Torna (righe, schede usate)."""
    import glob
    import json

    trovate = {"resistenze": None, "immunita": None, "vulnerabilita": None}
    for f in sorted(glob.glob(os.path.join(BASE, "dati", "mostri", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        m = d["mechanics_5e"]
        for chiave, campo in (("resistenze", "damage_resistances"),
                              ("immunita", "damage_immunities"),
                              ("vulnerabilita", "damage_vulnerabilities")):
            if trovate[chiave] is None and (m.get(campo) or []):
                trovate[chiave] = (os.path.splitext(os.path.basename(f))[0],
                                   m[campo][0])

    reg = C.Registro()
    righe = []
    usate = []
    for chiave, etichetta in (("resistenze", "resistenza"),
                              ("immunita", "immunità"),
                              ("vulnerabilita", "vulnerabilità")):
        if trovate[chiave] is None:
            righe.append([etichetta, "—", "nessuna scheda del bestiario la porta"])
            continue
        ident, voce = trovate[chiave]
        chi = C.da_mostro(ident, "mostri", reg)
        usate.append(chi.nome)
        clausola = voce.get("solo_se")
        for magico in ((False, True) if clausola else (False,)):
            tot, lette = C.applica_difese(chi, [(10, voce["tipo"])], reg,
                                          magico=magico)
            arma = ("arma magica" if magico else "arma non magica") if clausola \
                else "10 danni"
            righe.append([f"{chi.nome} — {etichetta} a `{voce['tipo']}`"
                          + (f" ({clausola})" if clausola else ""),
                          f"{arma}: **{tot}**", "; ".join(lette)])
    return righe, sorted(set(usate))


def coincidenze_di_attacco():
    """Quanti bonus di attacco del bestiario tornano col conto, e quanti no.

    E' la stessa misura che la decisione 50 (`cd-origine-dichiarata`) ha
    imposto per le CD, applicata all'altro numero che `attacco_di()` legge.
    Serve perche' un `bonus_colpire` LETTO dalla scheda e uno RIFATTO col
    conto (bonus di competenza + modificatore di caratteristica) si scrivono
    identici, e quando coincidono nessun controllo puo' distinguerli — e'
    esattamente la ragione per cui la CD 11 del Baaz era invisibile, ed e' il
    principio della decisione 54 (`origine-e-un-dato`).

    Contare le coincidenze e' quindi l'unica cosa onesta da fare: dice quanto
    vale il conto come prova, e la risposta e' che vale poco.

    I NOVE FUORI CONTO NON SONO NOVE ERRORI, e per la stessa ragione per cui
    gli 85 dentro non sono 85 conferme. Questa funzione li nomina e riporta
    il numero accanto ai numeri attesi; NON li classifica, perche'
    classificarli richiede di leggere da dove viene il bonus, e leggerlo da
    un dato e' precisamente cio' che l'origine dichiarata esiste per
    permettere. Dedurlo dalla prosa sarebbe la deduzione che la
    decisione 54 (`origine-e-un-dato`) vieta, travestita da controllo.

    Torna (totale, coincidenti, fuori, dichiarati) sui blocchi ancora in
    prosa, perche' e' li' che sta il bestiario: due soli attacchi sono
    strutturati, e `dichiarati` conta quelli il cui `bonus_colpire` e' gia'
    un `valore_dichiarato` invece di un intero nudo
    (decisione 55 (`origine-sede-unica`)."""
    import glob
    import json
    import sys as _sys
    _sys.path.insert(0, os.path.join(BASE, "dati"))
    import _sistema

    pat = re.compile(r"\+(\d+)\s*(?:a colpire|to hit)", re.I)
    tot, coincidenti, fuori, dichiarati = 0, 0, [], 0
    for f in sorted(glob.glob(os.path.join(BASE, "dati", "mostri", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        m = d["mechanics_5e"]
        ab = m.get("abilities") or {}
        cr = m.get("challenge_rating") or {}
        pb = cr.get("proficiency_bonus")
        if pb is None:
            pb = _sistema.competenza_da_grado_sfida(cr.get("value"))
        for gruppo in ("actions", "traits", "reactions", "legendary_actions"):
            for b in (m.get(gruppo) or []):
                att = (b.get("effetto") or {}).get("attacco") or {}
                if isinstance(att.get("bonus_colpire"), dict):
                    dichiarati += 1
                for n in pat.findall(b.get("mechanics_5e") or ""):
                    tot += 1
                    attese = ({pb + _sistema.modificatore(v)
                               for v in ab.values()}
                              if ab and pb is not None else set())
                    if int(n) in attese:
                        coincidenti += 1
                    else:
                        fuori.append((d["name"]["it"], b.get("name") or "?",
                                      int(n), sorted(attese)))
    return tot, coincidenti, fuori, dichiarati


def campi_con_la_stessa_forma():
    """Gli ALTRI campi in cui un valore letto e uno calcolato si scrivono uguali.

    La decisione 54 (`origine-e-un-dato`) e' generale, quindi la domanda
    giusta non e' «`bonus_colpire` e' a posto adesso?» ma «quanti altri campi
    hanno questa forma?». Questa funzione la misura invece di stimarla.

    Un campo entra nell'elenco se soddisfa DUE condizioni: il suo valore puo'
    venire sia dalla fonte sia da una formula del sistema, e le due strade
    producono lo stesso numero abbastanza spesso da rendere il difetto
    invisibile. Un campo che porta solo INGRESSI non ha il problema —
    `saving_throws` ne e' l'esempio: dichiara quali competenze il portatore
    ha e non il numero che ne segue, quindi non c'e' niente da confondere.

    Torna righe (campo, dove, totale, torna, dichiara_gia_origine)."""
    import glob
    import json
    import sys as _sys
    _sys.path.insert(0, os.path.join(BASE, "dati"))
    import _sistema

    files = sorted(glob.glob(os.path.join(BASE, "dati", "mostri", "*.json")))
    schede = [json.load(open(f, encoding="utf-8")) for f in files]

    def contesto(d):
        m = d["mechanics_5e"]
        ab = m.get("abilities") or {}
        cr = m.get("challenge_rating") or {}
        pb = cr.get("proficiency_bonus")
        if pb is None:
            pb = _sistema.competenza_da_grado_sfida(cr.get("value"))
        return m, ab, pb

    dado = re.compile(r"\((\d+)d(\d+)\s*([+-]\s*\d+)?\)")
    colpire = re.compile(r"\+\d+\s*(?:a colpire|to hit)", re.I)

    # bonus di danno in prosa: stessa forma del bonus di attacco, un addendo
    # in meno (il modificatore di caratteristica da solo, senza competenza).
    dan_tot = dan_ok = 0
    for d in schede:
        m, ab, pb = contesto(d)
        if not ab:
            continue
        mods = {_sistema.modificatore(v) for v in ab.values()} | {0}
        for gruppo in ("actions", "traits", "reactions", "legendary_actions"):
            for b in (m.get(gruppo) or []):
                txt = b.get("mechanics_5e") or ""
                if not colpire.search(txt):
                    continue
                for mm in dado.finditer(txt):
                    dan_tot += 1
                    dan_ok += int((mm.group(3) or "0").replace(" ", "")) in mods

    # percezione passiva: 10 + Saggezza, con o senza competenza.
    pp_tot = pp_ok = 0
    for d in schede:
        m, ab, pb = contesto(d)
        pp = m.get("passive_perception")
        if pp is None or not ab or pb is None:
            continue
        pp_tot += 1
        base = 10 + _sistema.modificatore(ab["wis"])
        pp_ok += pp in (base, base + pb, base + 2 * pb)

    # bonus di abilita': competenza (o doppia competenza) + caratteristica.
    ab_tot = ab_ok = 0
    for d in schede:
        m, ab, pb = contesto(d)
        if not ab or pb is None:
            continue
        attesi = ({pb + _sistema.modificatore(v) for v in ab.values()}
                  | {2 * pb + _sistema.modificatore(v) for v in ab.values()})
        for s in (m.get("skills") or []):
            if s.get("bonus") is None:
                continue
            ab_tot += 1
            ab_ok += s["bonus"] in attesi

    # punti ferita: la media dichiarata contro la formula di dadi scritta
    # accanto. Qui le due sedi sono nello STESSO campo, ed e' il caso in cui
    # il progetto la sua dichiarazione di origine ce l'ha gia'.
    pf_tot = pf_ok = 0
    for d in schede:
        hp = d["mechanics_5e"].get("hit_points") or {}
        av, fo = hp.get("average"), hp.get("formula")
        mm = re.match(r"(\d+)d(\d+)\s*([+-]\s*\d+)?$", (fo or "").replace(" ", ""))
        if av is None or not mm:
            continue
        pf_tot += 1
        n, faccia = int(mm.group(1)), int(mm.group(2))
        pf_ok += av == n * (faccia + 1) // 2 + int(mm.group(3) or 0)

    att_tot, att_ok, _fuori, _dich = coincidenze_di_attacco()
    return [
        ("`bonus_colpire`", "prosa dei blocchi", att_tot, att_ok, "no"),
        ("bonus di danno", "prosa dei blocchi", dan_tot, dan_ok, "no"),
        ("`skills[].bonus`", "scheda", ab_tot, ab_ok, "no"),
        ("`passive_perception`", "scheda", pp_tot, pp_ok, "no"),
        ("`hit_points.average`", "scheda", pf_tot, pf_ok,
         "si', nella forma unica"),
    ]


def prova_delle_immunita():
    """Le immunita' a condizione, provate su schede vere del bestiario.

    Serve per la stessa ragione della prova delle difese: nessuno dei tre
    scenari la esercita — ne' il Traag ne' il Baaz dichiara immunita' a
    condizione — quindi «l'arena passa» non direbbe niente su questo ramo.

    Prova le due meta' del problema: una condizione che il catalogo modella
    (l'immunita' si applica davvero) e una che non modella ancora (il motore
    lo dichiara invece di ignorarlo). Torna (righe, totali)."""
    import glob
    import json
    import sys as _sys
    _sys.path.insert(0, os.path.join(BASE, "dati"))
    import _vocabolari

    modellate = set(_vocabolari.condizioni_modellate())
    schede = {}
    n_voci = n_fuori = 0
    for f in sorted(glob.glob(os.path.join(BASE, "dati", "mostri", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        immuni = (d["mechanics_5e"].get("condition_immunities") or [])
        if not immuni:
            continue
        ident = os.path.splitext(os.path.basename(f))[0]
        schede[ident] = immuni
        n_voci += len(immuni)
        n_fuori += sum(1 for c in immuni if c not in modellate)

    def prima(condizione_modellata):
        for ident, immuni in schede.items():
            for c in immuni:
                if (c in modellate) == condizione_modellata:
                    return ident, c
        return None, None

    righe = []
    for modellata, etichetta in ((True, "modellata"), (False, "non modellata")):
        ident, cond = prima(modellata)
        if ident is None:
            righe.append([f"condizione {etichetta}", "—",
                          "nessuna scheda del bestiario ne porta una"])
            continue
        reg = C.Registro()
        chi = C.da_mostro(ident, "mostri", reg)
        if modellata:
            C.applica_esito(chi, {"condizioni": [{"id": cond}]}, reg)
            esito = ("respinta" if cond not in chi.condizioni else "APPLICATA")
            righe.append([f"{chi.nome} — immune a `{cond}`",
                          f"la condizione e' **{esito}**",
                          reg.righe[-1].strip() if reg.righe else "—"])
        else:
            dichiarata = "condizione-non-modellata" in reg.lacune
            righe.append([f"{chi.nome} — immune a `{cond}`",
                          "il motore **" + ("la dichiara" if dichiarata
                                            else "TACE") + "**",
                          "`dati/condizioni/" + cond + ".json` non esiste: "
                          "il termine c'e', la scheda meccanica no"])
    return righe, (len(schede), n_voci, n_fuori, len(modellate),
                   len(_vocabolari.CONDIZIONI))


def tabella(intestazioni, righe, allin=None):
    allin = allin or ["---"] * len(intestazioni)
    return "\n".join(
        ["| " + " | ".join(intestazioni) + " |",
         "|" + "|".join(allin) + "|"]
        + ["| " + " | ".join(str(x) for x in r) + " |" for r in righe])


def rapporto(scenari, lacune, completo):
    oggi = date.today().isoformat()
    blocchi = blocchi_strutturati()
    n_multi, n_azioni = conta_multiattacchi()
    con = [b for b in blocchi if b[3]]
    senza = [b for b in blocchi if not b[3]]
    righe_difese, schede_difese = prova_delle_difese()
    att_tot, att_coin, att_fuori, att_dich = coincidenze_di_attacco()
    forma = campi_con_la_stessa_forma()
    scoperti = [r for r in forma if r[4] == "no"]
    pp = [r for r in forma if "passive" in r[0]][0]
    righe_imm, (imm_schede, imm_voci, imm_fuori, n_mod, n_voc) = \
        prova_delle_immunita()

    esiti = []
    for s in scenari:
        n = sum(s["conteggio"].values())
        esiti.append([
            s["titolo"].split(". ", 1)[1],
            ", ".join(f"{k} {100 * v // n}%" for k, v in
                      sorted(s["conteggio"].items(), key=lambda x: -x[1])),
            f"{s['round_medi']:.1f}".replace(".", ","),
            f"{100 * s['pietrificati'] / n:.1f}".replace(".", ",") + "%",
        ])

    testa = f"""# L'arena della fetta verticale — i dati usati per la prima volta

*Generato da `motore/arena.py` il {oggi}.{" **VERSIONE COMPLETA, PRIVATA**: contiene i registri di combattimento con i numeri di scheda dei mostri." if completo else ""}*

---

## 0. Cosa è stato provato

Tre anni di conversione hanno prodotto dati validati da ogni lato: schemi,
validatori incrociati, verifica degli strati, confronto fra prosa e struttura.
Nessuno di quei controlli chiede la sola cosa che conta — che con questi dati
si possa giocare un turno.

`motore/combattimento.py` lo chiede. Legge `mechanics_5e...effetto` dei mostri,
`dati/condizioni/`, `dati/oggetti/` e i privilegi del chassis, e gioca uno
scontro a turni con iniziativa, azioni, danno, morte e condizioni.

**Non misura chi vince. Misura le lacune.** Ogni volta che il motore ha
bisogno di qualcosa che i dati non portano, lo dichiara e va avanti con
un'assunzione scritta. Senza quel registro un simulatore mente: gira sempre,
perché ogni valore assente diventa uno zero e ogni regola assente diventa un
ramo che non si prende. È la stessa forma del difetto che la categoria d'arma
ha reso visibile — un buco che sembra un dato.

> **Lo scontro gira. Con {len(lacune.lacune)} lacune dichiarate.**

---

## 1. Cosa è stato strutturato

`mostro.schema.json` aveva `additionalProperties: false` su `elemento_5e` e
nessun campo `effetto`: **lo strato strutturato non era nemmeno esprimibile
sui mostri.** Aperto, con la stessa forma e la stessa nota del campo omonimo
in `classe.schema.json`.

{tabella(["creatura", "gruppo", "blocco", "`effetto`"],
         [[m, g, n, ("**" + ", ".join(k) + "**") if ha else "—"]
          for m, g, n, ha, k in blocchi])}

**{len(con)} blocchi su {len(blocchi)}** hanno una meccanica leggibile da un
motore. Gli altri {len(senza)} restano prosa — ed è già un risultato, perché
prima della fetta erano prosa tutti e {len(blocchi)}, su 257 del bestiario.

### Due estensioni di schema, entrambe imposte da un caso — ora {cita('multiattacco-riferisce')} e {cita('salvezza-a-due-tempi')}

`multiattacco` — il blocco *Attacchi Multipli* dice una cosa meccanica e non
aveva nessun campo in cui dirla: la sua sola forma era la frase «effettua due
attacchi con X». Nel bestiario sono **{n_multi} blocchi su {n_azioni} azioni**,
e un motore che li ignorasse dimezzerebbe il danno per round di ognuno di quei
mostri senza che nessun controllo se ne accorga. Il campo riferisce l'azione
ripetuta per nome e non ne ricopia i numeri; `valida_effetti.py` verifica che
il nome esista nello stesso statblock.

`tiro_salvezza.fallimento_ripetuto` — il Death Throes del Baaz è un effetto a
**due tempi**: il primo fallimento trattiene mentre la pietrificazione
comincia, il secondo la compie. Lo schema aveva `ripetibile`, che dice *quando*
si ritira e non *cosa succede*. Senza il campo nuovo, le due condizioni di quel
tratto diventano una sola — cioè il tratto perde metà di sé senza che nessun
controllo se ne accorga.

### Due condizioni nuove, per lo stesso motivo — {cita('condizioni-a-consumo')}

`trattenuto` e `pietrificato` non esistevano. `build_condizioni.py` dichiarava
il criterio — *si aggiungono quando un blocco convertito le riferisce davvero* —
e questa è la prima volta che il criterio si applica invece di essere
enunciato. Sono cinque, non quindici.

`pietrificato` porta con sé una domanda che il motore ha dovuto risolvere: una
creatura pietrificata **non è morta**, ha ancora i suoi punti ferita e resiste
a tutti i danni. La condizione di fine scontro non può quindi essere «ogni
avversario a 0 punti ferita», ed è una definizione che nessun dato dichiara.

---

## 2. Gli scenari

{tabella(["scenario", "esiti su " + str(RIPETIZIONI) + " scontri", "round medi", "PG pietrificato"],
         esiti, ["---", "---", "--:", "--:"])}

«nessuno» è l'esito in cui il personaggio uccide il Baaz e il Death Throes lo
pietrifica: entrambe le parti fuori dallo scontro, nessuna morta. È il caso che
un motore scritto sull'assunzione «vince chi resta in piedi» non saprebbe
classificare.
"""

    if completo:
        for s in scenari:
            testa += f"""
---

## Registro — {s['titolo']}

Seme {s['seme']}. Esito: {s['esito']}, al round {s['round']}.

```
""" + "\n".join(scheda(c) for c in s["schede"]) + "\n\n" + s["registro"].stampa() + "\n```\n"

    testa += f"""
---

## 3. Le {len(lacune.lacune)} lacune

Ognuna è un punto in cui il motore ha supplito ai dati. Sono l'esito vero di
questa prova.

"""
    for i, (codice, (cosa, ass)) in enumerate(lacune.lacune.items(), 1):
        testa += f"**{i}. `{codice}`** — {cosa}\n\n> {ass}\n\n"

    # I NOVE, per nome e per numero: solo nel privato. Sono bonus di attacco
    # di schede di mostro, cioe' esattamente il materiale che CLAUDE.md 1
    # tiene fuori dal pubblico; il pubblico ne porta il CONTEGGIO e il
    # metodo, che sono analisi nostra. La riduzione e' un parametro di questo
    # generatore, non un taglio a valle (CLAUDE.md 2).
    nove = ""
    if completo and att_fuori:
        nove = ("\nI {n} che non tornano col conto, per nome:\n\n".format(
            n=len(att_fuori)) + tabella(
            ["scheda", "blocco", "in prosa", "attesi dal conto"],
            [[nome, blocco, f"+{b}",
              ", ".join(f"+{x}" for x in attesi) or "—"]
             for nome, blocco, b, attesi in att_fuori],
            ["---", "---", "--:", "---"]) + "\n\nNessuno dei {n} e' per questo un errore, come "
            "nessuno degli {c} dentro il conto e' per questo una conferma: "
            "sono i casi in cui il conto NON basta a spiegare il numero, e "
            "quello che manca — un addendo dichiarato dalla fonte, una "
            "stima nostra — sta scritto nella prosa accanto, dove nessun "
            "controllo lo legge. E' il buco che l'origine dichiarata chiude "
            "man mano che quei blocchi si strutturano.\n".format(
                n=len(att_fuori), c=att_coin))

    testa += f"""---

## 4. Cosa si è rotto, in ordine di peso

**`attacco` era due cose con lo stesso nome — chiusa.** Sul mostro era un
campo letto dalla scheda, sul personaggio una funzione di
`motore/combattimento.py`: due cose diverse che si chiamavano uguale, ed è la
lacuna che il primo scontro ha reso visibile. Chiusa con
{cita('attacco-unica-lettura')}: ciò che i due lati condividono non è il
campo, è la **lettura**. `attacco_di(combattente)` torna la forma
`effetto.attacco` da entrambe le parti — sul mostro la legge, sul personaggio
la compone — e chi la chiama non sa quale dei due casi ha davanti. Il
personaggio porta solo gli **ingressi** (razza, classe, livello, punteggi,
equipaggiato, scelte): ogni campo ricavabile da quelli non *può* esistere, il
costruttore solleva. Classe Armatura, punti ferita, bonus di attacco e danno
restano composti dal motore, ma adesso sono composti **una volta sola e per
tutti e due**.

**Il numero che nessuno può verificare — chiusa, e generalizzata.** Un
`bonus_colpire` letto dalla scheda e uno rifatto col conto (competenza +
modificatore) si scrivono identici, e `attacco_di()` non aveva modo di sapere
quale dei due stesse leggendo. È misurato, non supposto: dei **{att_tot} bonus di
attacco** che il bestiario scrive in prosa, **{att_coin} tornano col conto**
e {att_tot - att_coin} no. Le coincidenze non sono conferme — il
bonus della Spada corta del Baaz è **stampato dalla fonte** *e* torna col
conto, esattamente come la sua CD 11, e nessun controllo poteva vederlo.

Al secondo caso in due giri la regola è stata scritta una volta per tutte
invece di essere riapplicata a mano: {cita('origine-e-un-dato')}. Quando un
valore può essere **sia letto dalla fonte sia calcolato dal sistema**, la sua
origine è un **campo**, non una deduzione.

E al giro dopo si è scoperto che il campo esisteva già, tre volte, con un
altro nome: {cita('origine-sede-unica')}. `cd_origine` e `bonus_origine`
dicevano con `fonte` | `derivata` | `stimata` quello che `armor_class`,
`hit_points` e `challenge_rating` dicevano da mesi con `conversion_status` +
`source`. Un enum solo — con `derived` aggiunto, l'unico valore che il
vocabolario condiviso non aveva — una sede sola, e una forma sola: il
**valore e la sua origine nello stesso oggetto**. Il guadagno non è di
ordine: un `bonus_colpire` senza origine adesso non è vietato da una
clausola, è **inesprimibile**. La lacuna del motore resta condizionata al
dato e scatta sugli attacchi che portano ancora un intero nudo — oggi zero,
perché i due strutturati sono nella forma nuova ({att_dich} su {att_dich}).

**Quanti altri campi hanno questa forma — la misura, non la stima.** La
domanda che conta non è se `bonus_colpire` sia a posto adesso, ma quanti altri
valori si scrivono uguali che siano letti o calcolati. Sono **{len(scoperti)}
ancora scoperti**, e il quinto è il caso che insegna di più:

{tabella(["campo", "dove", "casi", "tornano col conto", "dichiara l'origine"],
         [[r[0], r[1], str(r[2]), f"{r[3]} ({100 * r[3] // r[2]}%)", r[4]]
          for r in forma], ["---", "---", "--:", "--:", "---"])}

`passive_perception` è il caso che spiega perché la percentuale non è una
diagnosi: **{pp[3]} su {pp[2]}** tornano col conto, il cento per cento, e
proprio per questo di nessuna si sa se sia stata letta o calcolata. Un campo dove il conto torna sempre è il posto **peggiore** in cui
fidarsi del conto, non il migliore.

`hit_points.average` è l'altro estremo, e va detto perché è la scoperta più
utile del giro: l'origine lì **era già dichiarata**, sotto un altro nome —
`conversion_status` e `source`, che `armor_class` e `challenge_rating`
portano allo stesso modo. Il progetto aveva inventato questo campo **tre
volte** senza accorgersi che era lo stesso campo, e `cd_origine` era la
quarta. Non è più aperto: {cita('origine-sede-unica')} ha fuso i quattro nomi
in uno e l'ha messo in una sede sola. Il rinominare temuto — 52 schede —
**non è servito**, e la ragione merita di essere registrata: si è esteso
l'enum che già reggeva invece di sostituirlo, quindi le tre colonne del
bestiario non sono state toccate e il costo è caduto sui **due** blocchi che
portavano il nome minoritario. Il dettaglio della misura è in
`dati/RAPPORTO-origine.md`.

`saving_throws` non è nell'elenco e non è una dimenticanza: porta solo
`proficient`, cioè **quali competenze** il portatore ha e non il numero che ne
segue. Un campo che porta ingressi non può avere questo difetto — ed è la
stessa forma che la {cita('attacco-unica-lettura')} ha imposto al
personaggio.
{nove}
**Non c'è una sede per le regole di sistema — chiusa.** *d20 + bonus contro la
Classe Armatura, 20 naturale critico, 1 naturale mancato d'ufficio* stava in
un file Python e in nessun dato. Il criterio a tre domande
({cita('criterio-meccanica')}) l'ha tagliata in due: i **numeri** — il 20 e
l'1 naturale, i moltiplicatori di resistenza e vulnerabilità, il modificatore
di caratteristica, il bonus di competenza, la base della CD — sono ora dati di
sistema in `dati/sistema/`, con schema e validatore; la **procedura** che li
usa resta codice, che è la risposta e non più una mancanza. La condizione
perché quella risposta valga era un riconfronto automatico, e c'è:
`dati/valida_sistema.py` rifiuta la stessa tabella riscritta altrove, e a
metterlo in piedi ha trovato subito i cinque punti in cui era già successo.

**Un innesco non ha un campo.** `azione: nessuna` significa *non costa
un'azione*, non *scatta a 0 punti ferita*. Il motore riconosce il Death Throes
**dal nome**, che è l'unico appiglio che i dati offrono. Ogni tratto che
scatta a una condizione — alla morte, quando si viene colpiti, all'inizio del
turno — oggi è indistinguibile da un tratto passivo.

**Non c'è posizione.** `portata_ft` e `gittata_ft` sono campi popolati e mai
letti: senza distanze un'arma da mischia e una a distanza si comportano
uguale. La conseguenza si vede sul Death Throes, che la fonte dichiara «ogni
creatura entro 5 piedi» e che il motore applica a tutti gli avversari e a
nessun alleato — un errore di regola, dichiarato.

**L'assenza di `effetto` dice due cose diverse.** *Non ha meccanica* e *non è
ancora strutturato* si scrivono uguali. `esito.nessuno` esiste proprio per
questa distinzione, un livello più in basso; al livello del blocco non c'è.
La *Dissoluzione post mortem* del Traag è il caso: la fonte dichiara
esplicitamente che non succede niente, e nei dati è indistinguibile da un
blocco non convertito.

**Il morale non entra in campo.** La decisione 27 (`sette-campi-2e`) lo destina
all'IA di combattimento e ogni mostro lo porta in `morale_2e`. Nessuno lo
legge, e i mostri combattono fino alla morte — «irrealistico, e macchinoso da
giocare», dice quella stessa decisione. Il Traag è il caso peggiore: il suo
morale ha due stati, e ignorarlo cancella il suo tratto identitario.

**Due vocabolari per i tipi di danno — chiusa.** Alla prima esecuzione
`dati/oggetti/` li portava in inglese (`slashing`, dall'SRD) e `dati/mostri/`
in italiano (`perforante`), nessuno dei due schemi li vincolava e nessun
validatore poteva vederlo perché nessuno dei due era sbagliato dal proprio
lato. Era l'ottava struttura doppia del progetto, e non è stata trovata
ispezionando i dati: è stata trovata usandoli. Chiusa con
{cita('vocabolario-italiano')} — vocabolario unico in
`dati/schema/vocabolari.schema.json`, riferito per `$ref` e mai ricopiato — e
il motore adesso **confronta davvero** il tipo di danno con resistenze,
immunità e vulnerabilità (`applica_difese`).

**Nessuno dei tre scenari lo esercita**, e va detto invece che lasciato
credere: né il Traag né il Baaz hanno difese per tipo, e il personaggio non ha
un campo dove averne. Il ramo esiste e in questa arena non si prende, che è
un'altra cosa dall'aver funzionato. Provato quindi a parte, e non su casi
costruiti: le schede sono cercate nel bestiario, una per forma
({", ".join(schede_difese)}).

{tabella(["scheda e difesa", "10 danni diventano", "come è stato letto"], righe_difese, ["---", "---", "---"])}

Le due righe che contano sono le prime: la stessa arma, se magica, passa la
resistenza. E lì c'è la lacuna nuova che ha preso il posto di quella chiusa —
**nessun campo dice se un attacco è magico**. Sull'arma di un personaggio c'è
`magico`; sull'azione di un mostro non c'è niente, e il motore assume *non
magico*, cioè l'assunzione favorevole al difensore.

**Le immunità a condizione: due sedi che non si parlavano — chiusa.**
`dati/mostri/` dichiarava le immunità con i nomi inglesi della 5e
(`charmed`, `poisoned`) mentre `dati/condizioni/` — che
{cita('condizioni-a-consumo')} dichiara sede unica — ha id italiani. Stesso
difetto dei tipi di danno, con l'aggravante che qui una delle due sedi era
**già dichiarata unica** e l'altra la ignorava: nessuna immunità del
bestiario poteva essere rispettata da nessun motore.

Tradurre e basta non bastava, ed è la ragione per cui questo caso era rimasto
aperto: delle condizioni citate dalle immunità solo tre esistono in
`dati/condizioni/`, e crearne altre sette per anticipazione avrebbe
sconfessato {cita('condizioni-a-consumo')} tre giorni dopo averla presa.
La strada è quella dei repertori ({cita('repertori-sono-filtri')}): l'insieme
delle condizioni SRD è **chiuso e noto**, quindi il vocabolario è completo —
**{n_voc} termini** — mentre il catalogo ne converte **{n_mod}**. Le altre
{n_voc - n_mod} non sono condizioni inesistenti: sono una **lacuna del nostro
catalogo**, che è cosa diversa, e non si scrive da nessuna parte — si deriva
dai file presenti nella cartella. {cita('condizioni-vocabolario-srd')}.

Nel bestiario: **{imm_voci} immunità su {imm_schede} schede**, di cui
**{imm_fuori} nominano una condizione che il motore non sa ancora applicare**.
Quel numero non è un errore da correggere, è una distanza da conoscere — e il
motore la **dichiara** (lacuna `condizione-non-modellata`) invece di
ignorarla, perché un'immunità saltata in silenzio è indistinguibile da
un'immunità rispettata.

Anche qui nessuno dei tre scenari esercita il ramo — né il Traag né il Baaz
dichiara immunità a condizione — quindi è provato a parte, su schede cercate
nel bestiario e non costruite:

{tabella(["scheda e immunità", "esito", "come è stato letto"], righe_imm, ["---", "---", "---"])}

---

*Le quattro estensioni sono ora registrate come decisioni —
{cita('effetto-sul-blocco-mostro')}, {cita('multiattacco-riferisce')},
{cita('salvezza-a-due-tempi')}, {cita('condizioni-a-consumo')} — insieme alle
due che questa esecuzione ha imposto: {cita('vocabolario-italiano')} e
{cita('cd-origine-dichiarata')}. Erano la condizione perché lo scontro
esistesse; restano scelte di progetto, e senza un id fra sei mesi nessuno
saprebbe perché `effetto` sta su `elemento_5e` invece che altrove.*
"""
    return testa


def guardia_riduzione(pubblico, scenari):
    """Nessuna riga di registro e nessun numero di scheda nel pubblico."""
    fuori = []
    for s in scenari:
        for riga in s["registro"].righe:
            r = riga.strip()
            if len(r) > 25 and r in pubblico:
                fuori.append(("registro", r[:60]))
        for c in s["schede"]:
            if getattr(c, "giocante", False):
                continue
            for etichetta, valore in (("CA", c.ca), ("PF", c.pf_max)):
                if re.search(rf"{c.nome}[^\n]*\b{valore}\b", pubblico):
                    fuori.append((f"{c.nome} {etichetta}", str(valore)))
    return fuori


PUBBLICO = os.path.join(BASE, "dati", "RAPPORTO-arena.md")
PRIVATO = os.path.join(BASE, "dati", "RAPPORTO-arena-completo.md")


def main(argv):
    scenari, lacune = esegui()

    for s in scenari:
        print("\n" + "=" * 72)
        print(s["titolo"])
        print("=" * 72 + "\n")
        for c in s["schede"]:
            print(scheda(c))
        print()
        print(s["registro"].stampa())
        print(f"\nEsito: {s['esito']}, al round {s['round']}. Seme: {s['seme']}")
        n = sum(s["conteggio"].values())
        print(f"{n} ripetizioni: "
              + ", ".join(f"{k} {v} ({100 * v // n}%)" for k, v in
                          sorted(s["conteggio"].items(), key=lambda x: -x[1]))
              + f"; durata media {s['round_medi']:.1f} round")
        if s["pietrificati"]:
            print(f"personaggio pietrificato dal Death Throes: "
                  f"{s['pietrificati']}/{n}")

    print("\n" + "=" * 72)
    print(f"LACUNE — {len(lacune.lacune)} cose che il motore ha supplito ai dati")
    print("=" * 72)
    for i, (codice, (cosa, ass)) in enumerate(lacune.lacune.items(), 1):
        print(f"\n{i:2d}. [{codice}]\n    {cosa}\n    → {ass}")

    if "--solo-video" in argv:
        return 0

    doc_pubblico = rapporto(scenari, lacune, completo=False)
    fuori = guardia_riduzione(doc_pubblico, scenari)
    if fuori:
        print("\nRIDUZIONE FALLITA — materiale di scheda nel rapporto pubblico:")
        for che, pezzo in fuori[:10]:
            print(f"  {che}: {pezzo}")
        return 1
    open(PUBBLICO, "w", encoding="utf-8").write(doc_pubblico)
    open(PRIVATO, "w", encoding="utf-8").write(
        rapporto(scenari, lacune, completo=True))
    print(f"\nscritto dati/RAPPORTO-arena.md ({len(doc_pubblico.splitlines())} righe)")
    print("scritto dati/RAPPORTO-arena-completo.md (privato, con i registri)")
    print("guardia di riduzione: nessuna riga di registro, nessun numero di "
          "scheda dei mostri nel pubblico")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
