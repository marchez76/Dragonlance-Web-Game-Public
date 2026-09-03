#!/usr/bin/env python3
"""
I vocabolari condivisi, letti dalla loro sede unica.

PERCHE' QUESTO FILE NON CONTIENE L'ELENCO
    L'elenco sta in `dati/schema/vocabolari.schema.json` e QUI SI LEGGE, non
    si ridigita. Ridigitarlo darebbe due copie da tenere allineate a mano,
    che e' esattamente il difetto che il vocabolario unico chiude: una
    struttura doppia nuova, creata mentre si chiude l'ottava.

COSA CONTIENE INVECE
    La TRADUZIONE, che e' un'altra cosa dall'elenco. I termini dell'SRD sono
    inglesi perche' la fonte e' inglese; i nostri sono italiani perche' lo
    strato `mechanics_5e` e' nostro (decisione 7, `doppio-strato`). Il
    passaggio fra i due e' una tabella, ha una sola sede, ed e' questa. I
    generatori la usano; nessuno traduce a mano dentro un `build_*.py`.

    `assert` all'import: ogni valore prodotto dalla traduzione deve stare
    nell'enum dello schema, e ogni voce dell'enum tranne i segnaposto nostri
    deve avere un termine inglese che ci arrivi. Una traduzione che produce
    un termine fuori vocabolario e' il difetto di partenza rimesso in piedi
    da un altro lato, e va colta all'import e non a valle.
"""

import glob
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(BASE, "schema", "vocabolari.schema.json")

with open(SCHEMA, encoding="utf-8") as _f:
    _VOC = json.load(_f)["$defs"]

TIPI_DANNO = tuple(_VOC["tipo_danno"]["enum"])
QUALIFICATORI_DANNO = tuple(_VOC["qualificatore_danno"]["enum"])
CONDIZIONI = tuple(_VOC["condizione"]["enum"])

# Segnaposto nostri: stanno nell'enum e NON hanno un termine SRD che li
# generi, quindi vanno esclusi dal controllo di copertura sotto.
SEGNAPOSTO = ("nessuno",)

# --------------------------------------------------------------------------
# SRD 5.1 -> nostro. La chiave e' il termine come la fonte lo stampa,
# minuscolo; il valore e' la voce dell'enum.
# --------------------------------------------------------------------------
DA_SRD = {
    "bludgeoning": "contundente",
    "piercing": "perforante",
    "slashing": "tagliente",
    "acid": "da_acido",
    "cold": "da_freddo",
    "lightning": "da_fulmine",
    "fire": "da_fuoco",
    "force": "da_forza",
    "thunder": "da_tuono",
    "poison": "da_veleno",
    "necrotic": "necrotico",
    "psychic": "psichico",
    "radiant": "radiante",
}

# Le clausole che l'SRD stampa in coda a una resistenza, nella forma esatta
# in cui compaiono nelle schede che abbiamo. Non e' un elenco esaustivo
# della 5e: si allarga quando una scheda ne porta una nuova, come il
# criterio di dati/build_condizioni.py per le condizioni.
QUALIFICATORE_DA_SRD = {
    "from nonmagical attacks": "da_attacchi_non_magici",
    "from nonmagical, nonsilvered weapons": "da_armi_non_magiche_non_argentate",
}


def tipo_danno(termine_srd):
    """Il tipo di danno nostro a partire dal termine SRD. Solleva se non lo
    conosce: una traduzione mancante deve fermare il generatore, non passare
    come stringa inglese dentro lo strato italiano — che e' come il difetto
    e' nato."""
    chiave = (termine_srd or "").strip().lower()
    if chiave not in DA_SRD:
        raise KeyError(
            f"tipo di danno SRD sconosciuto: {termine_srd!r}. Aggiungilo a "
            f"DA_SRD in dati/_vocabolari.py, non tradurlo sul posto.")
    return DA_SRD[chiave]


def leggi_resistenza(riga):
    """Una riga di `damage_resistances` come l'SRD la stampa, in campi.

    «bludgeoning, piercing, and slashing from nonmagical attacks» e' UN
    elemento di array nei nostri dati, cioe' tre tipi e una clausola dentro
    una frase. Qui torna come lista di (tipo, qualificatore): e' la lettura
    che i dati non portavano, e la ragione per cui `damage_resistances` era
    un vocabolario solo all'apparenza.

    Torna [(tipo, qualificatore_o_None), ...].
    """
    testo = (riga or "").strip().lower()
    qualificatore = None
    for coda, valore in QUALIFICATORE_DA_SRD.items():
        if testo.endswith(coda):
            qualificatore = valore
            testo = testo[: -len(coda)].strip()
            break
    testo = testo.replace(" and ", " ").replace(",", " ")
    return [(tipo_danno(p), qualificatore) for p in testo.split() if p]


# --------------------------------------------------------------------------
# LE CONDIZIONI: un insieme chiuso, e un catalogo che lo copre in parte.
#
# `dati/mostri/` dichiarava le immunita' a condizione con i nomi inglesi
# della 5e mentre `dati/condizioni/` — che la
# decisione 48 (`condizioni-a-consumo`) dichiara sede unica — ha id
# italiani. Stesso
# difetto dei tipi di danno, e piu' grave: li' erano due trascrizioni, qui
# una delle due e' una SEDE DICHIARATA che l'altra ignorava.
#
# Tradurre e basta non bastava: delle dieci condizioni citate dalle
# immunita' solo tre esistono in `dati/condizioni/`, e creare le altre sette
# per anticipazione avrebbe sconfessato la
# decisione 48 (`condizioni-a-consumo`) tre giorni dopo averla presa. Restringere l'enum alle esistenti era peggio: le schede
# perdevano informazione vera di fonte.
#
# La strada e' quella dei repertori (decisione 35, `repertori-sono-filtri`):
# l'insieme delle condizioni SRD e' CHIUSO e NOTO, quindi il vocabolario e'
# completo — quindici — e le sette mancanti non sono condizioni inesistenti,
# sono una LACUNA DEL NOSTRO CATALOGO. Che e' cosa diversa, e si misura.
# --------------------------------------------------------------------------

CONDIZIONE_DA_SRD = {
    "blinded": "accecato",
    "charmed": "affascinato",
    "deafened": "assordato",
    "exhaustion": "sfinimento",
    "frightened": "spaventato",
    "grappled": "afferrato",
    "incapacitated": "incapacitato",
    "invisible": "invisibile",
    "paralyzed": "paralizzato",
    "petrified": "pietrificato",
    "poisoned": "avvelenato",
    "prone": "prono",
    "restrained": "trattenuto",
    "stunned": "stordito",
    "unconscious": "incosciente",
}


def condizione(termine_srd):
    """L'id italiano a partire dal termine SRD. Solleva se non lo conosce.

    Stessa regola di `tipo_danno()`: una traduzione mancante ferma il
    generatore invece di passare come stringa inglese dentro lo strato
    italiano, che e' esattamente come il difetto e' nato."""
    chiave = (termine_srd or "").strip().lower()
    if chiave not in CONDIZIONE_DA_SRD:
        raise KeyError(
            f"condizione SRD sconosciuta: {termine_srd!r}. Se e' davvero una "
            f"delle quindici, aggiungila a CONDIZIONE_DA_SRD; se non lo e', "
            f"non e' una condizione della 5e e va guardata due volte.")
    return CONDIZIONE_DA_SRD[chiave]


def condizioni_modellate():
    """Le condizioni che il catalogo `dati/condizioni/` porta davvero.

    DERIVATA dalla cartella, mai scritta a mano: un elenco a mano accanto a
    una cartella e' una struttura doppia, e questo file esiste per chiuderne
    una."""
    return tuple(sorted(
        os.path.splitext(os.path.basename(f))[0]
        for f in glob.glob(os.path.join(BASE, "condizioni", "*.json"))))


def condizioni_non_modellate():
    """I termini che il vocabolario nomina e il catalogo non converte ancora.

    Non e' un errore ed e' importante che non lo sia: e' la distanza fra
    NOMINARE e CONVERTIRE, e la decisione 48 (`condizioni-a-consumo`) vuole
    che si accorci quando un blocco convertito lo impone, non prima."""
    return tuple(x for x in CONDIZIONI if x not in condizioni_modellate())


# --------------------------------------------------------------------------
# Invarianti, verificate all'import.
# --------------------------------------------------------------------------
assert set(DA_SRD.values()) <= set(TIPI_DANNO), (
    "DA_SRD produce un tipo di danno che vocabolari.schema.json non dichiara: "
    f"{sorted(set(DA_SRD.values()) - set(TIPI_DANNO))}")

assert set(TIPI_DANNO) - set(SEGNAPOSTO) == set(DA_SRD.values()), (
    "l'enum e la traduzione non si coprono. Fuori dalla traduzione: "
    f"{sorted(set(TIPI_DANNO) - set(SEGNAPOSTO) - set(DA_SRD.values()))}")

assert set(QUALIFICATORE_DA_SRD.values()) == set(QUALIFICATORI_DANNO), (
    "i qualificatori dello schema e quelli tradotti non coincidono")

assert set(CONDIZIONE_DA_SRD.values()) == set(CONDIZIONI), (
    "l'enum delle condizioni e la traduzione non si coprono. Fuori dalla "
    f"traduzione: {sorted(set(CONDIZIONI) - set(CONDIZIONE_DA_SRD.values()))}; "
    f"fuori dall'enum: {sorted(set(CONDIZIONE_DA_SRD.values()) - set(CONDIZIONI))}")

assert set(condizioni_modellate()) <= set(CONDIZIONI), (
    "dati/condizioni/ porta un id che il vocabolario non nomina: "
    f"{sorted(set(condizioni_modellate()) - set(CONDIZIONI))}. Il catalogo "
    "puo' essere piu' POVERO del vocabolario, mai diverso")
