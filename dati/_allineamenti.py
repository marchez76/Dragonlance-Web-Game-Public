#!/usr/bin/env python3
"""
L'ALLINEAMENTO — vocabolario unico, e le restrizioni come insiemi di valori.

LA FORMA, IN UNA RIGA
    Nove valori chiusi in un vocabolario; una restrizione di classe e' un
    SOTTOINSIEME di quei nove, non una frase. E' la stessa macchina della
    decisione 58 (`telaio-apre-classe-filtra`): dove prima c'era
    un'etichetta di prosa, ora c'e' un insieme e una regola che lo produce.

IL DIFETTO CHE CHIUDE, misurato e non ricordato
    Dieci classi su venti dichiaravano `alignment_restriction.applied` a
    `true`. Il campo accanto era una stringa di prosa, in due lingue
    diverse — «Lawful Good» e «Qualunque allineamento buono» nello stesso
    strato — e nessun vocabolario diceva quali fossero i valori leciti.
    Nessun motore poteva applicare quel vincolo: `applied: true` era una
    dichiarazione senza referente.

    E' peggio del caso `allowed_classes` prima della
    decisione 58 (`telaio-apre-classe-filtra`), e per un motivo preciso:
    li' il campo diceva onestamente di essere un'etichetta
    del PHB 2e, cioe' dichiarava di NON essere ancora risolto. Qui il campo
    dichiarava di esserlo. Un vincolo che si annuncia applicato e non e'
    applicabile e' peggio di un campo assente, perche' il campo assente si
    vede.

DUE VOCI SU DIECI NON SONO VALORI: SONO REGOLE
    «Determinato dalla veste» e «coerente con la famiglia celeste del dio
    servito» non nominano un insieme di allineamenti: nominano una FUNZIONE
    di un'altra scelta, che alla creazione non e' ancora stata fatta.
    Appiattirle su un insieme perderebbe proprio cio' che dicono. Restano
    quindi `applied: false` con la dipendenza dichiarata, e la forma che
    prenderanno e' una decisione da prendere, non un dato da scrivere: sta
    accanto alla decisione 35 (`repertori-sono-filtri`), dove il filtro
    delimita e la scelta avviene dopo.

    Finche' non e' presa, `applied` sta a `false`: la regola e' che il campo
    dichiara cio' che il motore sa davvero fare.

CHI ALTRO SCRIVE UN ALLINEAMENTO
    Cercato il giorno in cui questa sede nasce, non sei mesi dopo — e' la
    meta' del lavoro che CLAUDE.md 3 chiede quando si crea una sede unica.
    Tre altri scrittori, tutti gia' esistenti:

      dati/mostri/  `mechanics_5e.alignment`   prosa INGLESE nello strato
                                               italiano: lo stesso difetto
                                               che `_vocabolari.py` e' nato
                                               per chiudere sui tipi di danno
      dati/mostri/  `source_2e.alignment`      prosa 2e, strato di fonte:
                                               resta com'e', per costruzione
      dati/divinita/ `family`                  i soli assi morali, tre valori
      dati/divinita/ `source_2e.priest_alignment`  abbreviazioni 2e

    Nessuno dei quattro viene toccato qui, e la ragione non e' la fretta: il
    primo e' una conversione di 51 schede che va fatta nel suo generatore
    (CLAUDE.md 2), il secondo e' strato di fonte e non si tocca mai, il
    terzo e il quarto vivono nella
    decisione 35 (`repertori-sono-filtri`) e si muoveranno con essa.
    Cio' che questo modulo fa e' MISURARE la distanza — `fuori_vocabolario()`
    — perche' una struttura doppia misurata non e' chiusa ma non e' nemmeno
    invisibile, ed e' la differenza fra una sede che chiude e una che sposta.
"""

import json
import os
import re
from collections import namedtuple

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "schema", "vocabolari.schema.json"),
          encoding="utf-8") as _f:
    ALLINEAMENTI = tuple(json.load(_f)["$defs"]["allineamento"]["enum"])


# --------------------------------------------------------------------------
# I DUE ASSI. Non si deducono dall'id spezzandolo in due: `neutrale` da solo
# e' una parola sola e sarebbe un caso speciale dentro un parsing, cioe' una
# regola nascosta in una funzione. Qui la tabella e' esplicita e gli assert
# in coda pretendono che copra l'enum esattamente, in tutti e due i sensi.
# --------------------------------------------------------------------------
ORDINE = ("legale", "neutrale", "caotico")
MORALE = ("buono", "neutrale", "malvagio")

ASSI = {
    "legale_buono":       ("legale",   "buono"),
    "neutrale_buono":     ("neutrale", "buono"),
    "caotico_buono":      ("caotico",  "buono"),
    "legale_neutrale":    ("legale",   "neutrale"),
    "neutrale":           ("neutrale", "neutrale"),
    "caotico_neutrale":   ("caotico",  "neutrale"),
    "legale_malvagio":    ("legale",   "malvagio"),
    "neutrale_malvagio":  ("neutrale", "malvagio"),
    "caotico_malvagio":   ("caotico",  "malvagio"),
}


def insieme(ordine=None, morale=None):
    """Gli allineamenti che stanno su un asse, o su entrambi.

    DERIVATO da ASSI e mai scritto a mano: «i tre buoni» e' un elenco che
    esiste gia' e ricopiarlo sarebbe la struttura doppia in scala piccola.
    Senza argomenti torna tutti e nove."""
    return tuple(a for a in ALLINEAMENTI
                 if (ordine is None or ASSI[a][0] == ordine)
                 and (morale is None or ASSI[a][1] == morale))


def tranne(*esclusi):
    """Tutti gli allineamenti meno quelli nominati. Serve alle restrizioni
    che la fonte scrive per complemento («qualunque tranne...»): scriverne
    l'elenco positivo sarebbe una lettura in piu' fra la fonte e il dato."""
    for e in esclusi:
        if e not in ALLINEAMENTI:
            raise KeyError(f"allineamento sconosciuto: {e!r}")
    return tuple(a for a in ALLINEAMENTI if a not in esclusi)


# --------------------------------------------------------------------------
# LA TRADUZIONE. Stessa regola di `_vocabolari.tipo_danno()`: un termine che
# non si conosce ferma chi chiama, non passa come stringa inglese dentro lo
# strato italiano — che e' esattamente come il difetto nasce ogni volta.
# --------------------------------------------------------------------------
DA_TERMINE = {
    # SRD 5.1, sezione Alignment: nome esteso e sigla, che la fonte stampa
    # accanto.
    "lawful good": "legale_buono",         "lg": "legale_buono",
    "neutral good": "neutrale_buono",      "ng": "neutrale_buono",
    "chaotic good": "caotico_buono",       "cg": "caotico_buono",
    "lawful neutral": "legale_neutrale",   "ln": "legale_neutrale",
    "neutral": "neutrale",                 "n": "neutrale",
    "chaotic neutral": "caotico_neutrale", "cn": "caotico_neutrale",
    "lawful evil": "legale_malvagio",      "le": "legale_malvagio",
    "neutral evil": "neutrale_malvagio",   "ne": "neutrale_malvagio",
    "chaotic evil": "caotico_malvagio",    "ce": "caotico_malvagio",
    # Le forme italiane, che sono le nostre e non una traduzione della fonte.
    "legale buono": "legale_buono",
    "neutrale buono": "neutrale_buono",
    "caotico buono": "caotico_buono",
    "legale neutrale": "legale_neutrale",
    "neutrale puro": "neutrale",
    "caotico neutrale": "caotico_neutrale",
    "legale malvagio": "legale_malvagio",
    "neutrale malvagio": "neutrale_malvagio",
    "caotico malvagio": "caotico_malvagio",
}


def allineamento(termine):
    """L'id a partire da un termine della fonte. Solleva se non lo conosce."""
    chiave = re.sub(r"\s+", " ", (termine or "").strip().lower()).strip(".")
    if chiave not in DA_TERMINE:
        raise KeyError(
            f"allineamento sconosciuto: {termine!r}. Se e' davvero uno dei "
            f"nove, aggiungilo a DA_TERMINE in dati/_allineamenti.py; se non "
            f"lo e', non e' un allineamento e va guardato due volte.")
    return DA_TERMINE[chiave]


# --------------------------------------------------------------------------
# LE RESTRIZIONI DI CLASSE — la lettura, una riga per classe.
#
#   testo          la stringa che `source_2e.alignment_restriction` porta
#                  oggi. Non e' decorazione: e' l'invariante a due sensi
#                  (`verifica()` pretende che coincida), cosi' che una
#                  riformulazione della fonte non passi sotto una lettura
#                  scritta per la formulazione vecchia.
#   valori         il sottoinsieme dei nove. Vuoto se la voce e' una regola.
#   ragione        perche' quel sottoinsieme (editoriale, una per riga).
#   da_confermare  la lettura regge ma ne esiste una seconda plausibile che
#                  la fonte non ha ancora escluso. Non e' un difetto: e' una
#                  riga che aspetta una lettura, e finche' aspetta si vede.
#   dipende_da     per le voci che NON sono valori: da quale altra scelta
#                  dipende l'insieme. Con `dipende_da` valorizzato, `valori`
#                  e' vuoto e `applied` resta false.
# --------------------------------------------------------------------------
Restrizione = namedtuple("Restrizione",
                         "testo valori ragione da_confermare dipende_da")


def _r(testo, valori=(), ragione="", da_confermare="", dipende_da=None):
    return Restrizione(testo, tuple(valori), ragione, da_confermare, dipende_da)


RESTRIZIONI = {
    "cavaliere-corona": _r(
        "Lawful Good", ("legale_buono",),
        "la fonte nomina un allineamento singolo, non una famiglia: "
        "l'insieme ha un elemento solo"),
    "cavaliere-spada": _r(
        "Lawful Good", ("legale_buono",),
        "stesso caso del grado precedente"),
    "cavaliere-rosa": _r(
        "Lawful Good", ("legale_buono",),
        "stesso caso dei due gradi precedenti"),
    "cavaliere": _r(
        "Qualunque allineamento buono", insieme(morale="buono"),
        "«buono» e' l'asse morale, e l'asse morale ha tre valori: il "
        "vocabolario li deriva, non li elenca"),
    "mago-veste-bianca": _r(
        "Buono", insieme(morale="buono"),
        "stessa lettura del Cavaliere: la Veste Bianca chiede la famiglia "
        "buona, non un allineamento preciso"),
    "mago-veste-nera": _r(
        "Malvagio", insieme(morale="malvagio"),
        "speculare alla Veste Bianca sull'altro estremo dell'asse morale"),
    "mago-veste-rossa": _r(
        "Neutrale", insieme(morale="neutrale"),
        "«neutrale» come valore dell'asse MORALE: legale neutrale, neutrale, "
        "caotico neutrale",
        da_confermare=
        "e' l'unica delle tre Vesti dove la parola e' ambigua, perche' "
        "«neutrale» sta su tutti e due gli assi. La lettura scelta e' quella "
        "dell'asse morale (tre valori), coerente con le altre due Vesti che "
        "leggono la stessa posizione sullo stesso asse. La seconda lettura "
        "possibile e' «qualunque allineamento che abbia un neutrale», cioe' "
        "cinque valori: i tre di qui piu' neutrale buono e neutrale "
        "malvagio. Le due non si distinguono senza una riga della fonte, e "
        "la riga non e' stata ancora letta: la differenza vale due "
        "allineamenti su nove e va decisa, non indovinata."),
    "mariner": _r(
        "Qualunque tranne Legale Buono", tranne("legale_buono"),
        "la fonte lo scrive per complemento e qui resta un complemento: "
        "`tranne()` produce gli otto, e nessuna lettura si interpone"),

    # --- le due che sono REGOLE e non valori. `valori` vuoto, `applied` a
    #     false, e la dipendenza dichiarata invece che appiattita.
    "mago-alta-stregoneria": _r(
        "Determinato dalla veste: Bianca=buono, Rossa=neutrale, Nera=malvagio. "
        "L'allineamento va dichiarato al 3° livello, prima del Test.",
        dipende_da="veste",
        ragione="non e' un insieme: e' una funzione della Veste, che alla "
                "creazione non e' ancora scelta — la "
                "decisione 6 (`maghi-delle-torri`) colloca il giuramento al "
                "Test, al 3°. "
                "Le tre Vesti hanno gia' ciascuna il proprio insieme qui "
                "sopra: la forma che questa voce prendera' e' una decisione "
                "da prendere, non un dato da scrivere."),
    "sacerdote-ordini-sacri": _r(
        "Coerente con la famiglia celeste del dio servito: Bene, Male o "
        "Neutralita'.",
        dipende_da="divinita",
        ragione="non e' un insieme: e' una funzione del dio scelto. Il dato "
                "per risolverla esiste gia' — `family` su ciascuna delle 21 "
                "divinita', e `source_2e.priest_alignment`, che e' piu' "
                "preciso della famiglia — ma legarli qui vorrebbe dire "
                "decidere la forma del legame, che e' cosa diversa dal "
                "trascrivere un vincolo."),
}


# --------------------------------------------------------------------------
# LETTURA DEI DATI E MISURA DEGLI ALTRI SCRITTORI
# --------------------------------------------------------------------------

def _carica(cartella):
    import glob
    return [json.load(open(p, encoding="utf-8"))
            for p in sorted(glob.glob(os.path.join(BASE, cartella, "*.json")))]


def blocco(classe_id):
    """Il blocco `alignment_restriction` per lo strato 5e di una classe.

    Nessuna classe qui dentro? Nessuna restrizione: `applied` false e valori
    vuoti. E' il caso delle dieci classi che la fonte non vincola, e non va
    confuso con il caso `dipende_da`, dove una restrizione c'e' ma non e'
    ancora applicabile — `motivo_non_applicato` li distingue."""
    r = RESTRIZIONI.get(classe_id)
    if r is None:
        return {"applied": False, "values": [], "source_text": None,
                "depends_on": None, "motivo_non_applicato": None,
                "da_confermare": None}
    return {
        "applied": bool(r.valori),
        "values": list(r.valori),
        "source_text": r.testo,
        "depends_on": r.dipende_da,
        "motivo_non_applicato": (r.ragione if r.dipende_da else None),
        "da_confermare": r.da_confermare or None,
    }


_PULISCI = re.compile(r"^(typically|usually|often)\s+", re.I)

# I due termini che la 5e usa AL POSTO di un allineamento, e non sono un buco
# del vocabolario: `Unaligned` dice che la creatura non ha una bussola morale,
# `Any alignment` che la scheda non ne fissa una. Contarli come «fuori
# vocabolario» insieme alla prosa direbbe il falso in entrambe le direzioni:
# gonfierebbe la distanza da colmare e nasconderebbe i casi veri.
NON_ALLINEAMENTI_5E = ("unaligned", "any alignment")

# `family` delle divinita' non porta un allineamento: porta un valore
# dell'asse MORALE. Confrontarlo con i nove darebbe un falso positivo su
# `neutral`, che e' insieme un asse e un allineamento — l'unica parola che
# sta su tutti e due i piani, ed e' esattamente quella che si presterebbe.
MORALE_DA_SRD = {"good": "buono", "neutral": "neutrale", "evil": "malvagio"}


def fuori_vocabolario():
    """Quanto gli altri scrittori di allineamento distano da questo enum.

    NON converte niente: conta. Torna un dizionario per sorgente, con i
    termini che il vocabolario riconosce e quelli che non riconosce. Serve a
    tenere la distanza visibile fra il giorno in cui la sede nasce e il
    giorno in cui gli altri scrittori ci arrivano."""
    fuori = {}

    def censisci(nome, valori, vocabolario=None):
        dentro = non_dentro = 0
        propri, termini = {}, {}
        for v in valori:
            if not v:
                continue
            grezzo = _PULISCI.sub("", str(v).strip()).rstrip(".")
            chiave = re.sub(r"\s+", " ", grezzo.lower())
            if vocabolario is not None:
                if chiave in vocabolario:
                    dentro += 1
                else:
                    non_dentro += 1
                    termini[v] = termini.get(v, 0) + 1
                continue
            if chiave in NON_ALLINEAMENTI_5E:
                propri[v] = propri.get(v, 0) + 1
                continue
            try:
                allineamento(grezzo)
                dentro += 1
            except KeyError:
                non_dentro += 1
                termini[v] = termini.get(v, 0) + 1
        fuori[nome] = {
            "riconosciuti": dentro,
            "non_allineamenti_5e": dict(sorted(propri.items())),
            "non_riconosciuti": non_dentro,
            "termini_fuori": dict(sorted(termini.items())),
        }

    mostri = _carica("mostri")
    censisci("mostri/mechanics_5e.alignment",
             [(m.get("mechanics_5e") or {}).get("alignment") for m in mostri])
    censisci("mostri/source_2e.alignment",
             [(m.get("source_2e") or {}).get("alignment") for m in mostri])
    dei = _carica("divinita")
    censisci("divinita/family", [d.get("family") for d in dei],
             vocabolario=MORALE_DA_SRD)
    censisci("divinita/source_2e.priest_alignment",
             [(d.get("source_2e") or {}).get("priest_alignment") for d in dei])
    return fuori


# --------------------------------------------------------------------------
# GUARDIA — la lettura e i dati devono nominare le stesse cose.
# --------------------------------------------------------------------------

def verifica():
    """Lista di incoerenze fra RESTRIZIONI e i dati. Vuota = tutto torna."""
    classi = _carica("classi")
    problemi = []
    con_testo = {}
    for c in classi:
        t = (c.get("source_2e") or {}).get("alignment_restriction")
        if t:
            con_testo[c["id"]] = " ".join(str(t).split())

    for cid in sorted(set(con_testo) - set(RESTRIZIONI)):
        problemi.append(f"{cid}: la fonte porta una restrizione di "
                        f"allineamento e nessuna riga la legge")
    for cid in sorted(set(RESTRIZIONI) - set(con_testo)):
        problemi.append(f"{cid}: riga di lettura per una classe che nella "
                        f"fonte non ha restrizione di allineamento")
    for cid, r in sorted(RESTRIZIONI.items()):
        atteso = " ".join(r.testo.split())
        if cid in con_testo and con_testo[cid] != atteso:
            problemi.append(
                f"{cid}: la fonte dice {con_testo[cid]!r}, la riga e' stata "
                f"scritta per {atteso!r} — la lettura va rifatta, non "
                f"riallineata")
        for v in r.valori:
            if v not in ALLINEAMENTI:
                problemi.append(f"{cid}: valore fuori vocabolario: {v}")
        if r.valori and r.dipende_da:
            problemi.append(f"{cid}: ha insieme dei valori e una dipendenza; "
                            f"una restrizione o e' un insieme o e' una regola")
        if not r.valori and not r.dipende_da:
            problemi.append(f"{cid}: nessun valore e nessuna dipendenza: "
                            f"la riga non dice niente")
        if not r.ragione:
            problemi.append(f"{cid}: legge la fonte e non dice perche'")
    return problemi


# --------------------------------------------------------------------------
# Invarianti, verificate all'import.
# --------------------------------------------------------------------------
assert set(ASSI) == set(ALLINEAMENTI), (
    "gli assi e l'enum non si coprono. Fuori dagli assi: "
    f"{sorted(set(ALLINEAMENTI) - set(ASSI))}; fuori dall'enum: "
    f"{sorted(set(ASSI) - set(ALLINEAMENTI))}")

assert {a for a, _ in ASSI.values()} == set(ORDINE), "asse d'ordine incompleto"
assert {m for _, m in ASSI.values()} == set(MORALE), "asse morale incompleto"

assert len({ASSI[a] for a in ALLINEAMENTI}) == len(ALLINEAMENTI), \
    "due allineamenti sulla stessa coppia di assi"

assert set(DA_TERMINE.values()) == set(ALLINEAMENTI), (
    "la traduzione e l'enum non si coprono. Fuori dalla traduzione: "
    f"{sorted(set(ALLINEAMENTI) - set(DA_TERMINE.values()))}")


if __name__ == "__main__":
    _p = verifica()
    for _x in _p:
        print("PROBLEMA:", _x)
    print(f"{len(ALLINEAMENTI)} allineamenti, {len(RESTRIZIONI)} classi "
          f"vincolate, {len(_p)} incoerenze.")
    print()
    for _nome, _m in fuori_vocabolario().items():
        print(f"{_nome}: {_m['riconosciuti']} riconosciuti, "
              f"{sum(_m['non_allineamenti_5e'].values())} non-allineamenti "
              f"della 5e, {_m['non_riconosciuti']} fuori vocabolario")
        for _t, _n in _m["termini_fuori"].items():
            print(f"    {_n:3}  {_t}")
