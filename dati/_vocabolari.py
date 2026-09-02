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

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(BASE, "schema", "vocabolari.schema.json")

with open(SCHEMA, encoding="utf-8") as _f:
    _VOC = json.load(_f)["$defs"]

TIPI_DANNO = tuple(_VOC["tipo_danno"]["enum"])
QUALIFICATORI_DANNO = tuple(_VOC["qualificatore_danno"]["enum"])

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
