#!/usr/bin/env python3
"""
Caricamento degli schemi con i riferimenti fra file risolti.

PERCHE' SERVE
    Da quando `dati/schema/vocabolari.schema.json` e' la sede unica dei
    vocabolari condivisi, gli altri schemi lo RIFERISCONO con
    `$ref: "vocabolari.schema.json#/$defs/..."` invece di ricopiarne gli
    enum. Un `$ref` fra file non si risolve da solo: `jsonschema` vuole un
    registro che sappia dove stanno gli altri schemi. Senza registro solleva
    `Unresolvable`, che e' rumoroso: non e' quello il rischio. Il rischio e'
    il registro che c'e' ma non copre la URI giusta — i nostri schemi usano
    DUE convenzioni di `$id`, e lo stesso `$ref` relativo diventa due URI
    diverse a seconda di chi lo scrive. Un alias mancante fa risolvere il
    riferimento da un lato e non dall'altro, e li' il vocabolario risulta
    applicato senza esserlo.

    Da qui `verifica_riferimenti()`, che ogni validatore chiama: prova su
    OGNI schema che lo riferisce un valore che l'enum condiviso deve
    rifiutare, e pretende che venga rifiutato davvero.
"""

import glob
import json
import os

import jsonschema
from referencing import Registry, Resource

BASE = os.path.dirname(os.path.abspath(__file__))
CARTELLA = os.path.join(BASE, "schema")

Validator = getattr(jsonschema, "Draft202012Validator", None) or jsonschema.Draft7Validator


# I nostri schemi usano DUE convenzioni di `$id`: la maggioranza
# `https://dragonlance-gdr.local/schema/<file>`, effetto e condizione il
# nome nudo. Un `$ref` relativo si risolve contro l'`$id` di chi lo scrive,
# quindi lo stesso riferimento diventa due URI diverse a seconda di chi
# riferisce. Ogni schema entra nel registro sotto ENTRAMBE le forme piu' il
# proprio `$id`: uniformare le convenzioni sarebbe piu' pulito e cambierebbe
# nove file per una ragione che non e' quella del giro, quindi il registro
# accetta l'una e l'altra e `verifica_riferimenti()` prova che risolvano.
PREFISSO = "https://dragonlance-gdr.local/schema/"


def _registro():
    reg = Registry()
    for f in sorted(glob.glob(os.path.join(CARTELLA, "*.json"))):
        with open(f, encoding="utf-8") as fh:
            contenuto = json.load(fh)
        risorsa = Resource.from_contents(contenuto)
        nome = os.path.basename(f)
        for uri in {nome, PREFISSO + nome, contenuto.get("$id") or nome}:
            reg = reg.with_resource(uri, risorsa)
    return reg


def carica(nome):
    """Lo schema `nome` (es. "mostro.schema.json") come dizionario."""
    with open(os.path.join(CARTELLA, nome), encoding="utf-8") as f:
        return json.load(f)


def validatore(nome, schema=None):
    """Un Validator per `nome`, con i riferimenti fra file risolti."""
    schema = carica(nome) if schema is None else schema
    Validator.check_schema(schema)
    return Validator(schema, registry=_registro())


def verifica_riferimenti():
    """Il `$ref` fra file e' davvero risolto? Torna un elenco di errori.

    Prova diretta e non affermazione. `slashing` e' il termine inglese che
    il vocabolario italiano deve rifiutare, ed e' esattamente il valore che
    i dati portavano prima che l'ottava struttura doppia fosse chiusa: se
    passa, il riferimento non e' stato risolto e il vocabolario sembra
    applicato senza esserlo. Vale su ogni schema che lo riferisce, perche'
    un registro dimenticato in UN validatore basta a riaprire il buco li'."""
    sonde = [
        ("effetto.schema.json", "danno.tipo",
         {"attacco": {"tipo": "mischia_arma", "danno": [{"tipo": "slashing"}]}}),
        ("oggetto.schema.json", "weapon_5e.damage_type",
         {"id": "x", "name": {"en": "X", "it": "X"}, "categoria": "arma",
          "magico": False,
          "source": {"source_edition": "SRD 5.1", "source_book": "b"},
          "mechanics_5e": {"conversion_status": "compilato",
                           "weapon_5e": {"damage_type": "slashing"}}}),
        ("mostro.schema.json", "damage_resistances[].tipo",
         {"mechanics_5e": {"damage_resistances": [{"tipo": "slashing"}]}}),
    ]
    # Le condizioni hanno la stessa forma di difetto e quindi la stessa
    # sonda, con il termine che i dati portavano prima del 02/09/2026:
    # `charmed`. Il vocabolario delle condizioni e' l'insieme SRD completo,
    # quindi rifiutare l'inglese e' esattamente cio' che deve fare — un
    # riferimento non risolto lo lascerebbe passare e l'enum sembrerebbe
    # applicato senza esserlo.
    sonde.append(
        ("mostro.schema.json", "condition_immunities[]",
         {"mechanics_5e": {"condition_immunities": ["charmed"]}}))
    # L'ORIGINE HA LA STESSA FORMA DI DIFETTO E QUINDI LA STESSA SONDA.
    # Dalla decisione 55 (`origine-sede-unica`) `conversion_status` e
    # `provenienza` stanno in vocabolari.schema.json e gli altri schemi li
    # riferiscono. `fonte` e' il termine del vocabolario ABBANDONATO — quello
    # che `cd_origine` usava — ed e' esattamente il valore che l'enum unico
    # deve rifiutare: se passa, il riferimento non e' stato risolto e i
    # quattro nomi sono tornati a essere due senza che nulla lo dica.
    sonde.append(
        ("mostro.schema.json", "armor_class.conversion_status",
         {"mechanics_5e": {"armor_class": {"value": 10,
                                           "conversion_status": "fonte",
                                           "source": "SRD 5.1"}}}))
    sonde.append(
        ("effetto.schema.json", "tiro_salvezza.cd.conversion_status",
         {"tiro_salvezza": {"caratteristica": "con",
                            "cd": {"value": 11,
                                   "conversion_status": "fonte",
                                   "source": "SRD 5.1"}}}))
    # LE CLASSI, dal 04/09/2026. `chassis_features[].conversion_status` era
    # dichiarato `"type": "string"` senza enum: un campo che SEMBRA
    # controllato e non lo e', ed e' il caso peggiore perche' non somiglia a
    # una lacuna. Ora e' un `$ref` alla sede, e questa sonda lo prova con lo
    # stesso termine abbandonato usato per gli altri.
    sonde.append(
        ("classe.schema.json", "mechanics_5e.chassis_features[].conversion_status",
         {"mechanics_5e": {"chassis_features": [
             {"name": "X", "kind": "privilegio_chassis", "level": 1,
              "conversion_status": "fonte", "mechanics_5e": "x"}]}}))
    # LE RAZZE, dal 05/09/2026: stessa chiusura di poco sopra, sullo stesso
    # campo con lo stesso nome ma sul lato razza (`traits` invece di
    # `chassis_features`).
    sonde.append(
        ("razza.schema.json", "mechanics_5e.traits[].conversion_status",
         {"mechanics_5e": {"traits": [
             {"name": "X", "source": "X", "text_2e": "x",
              "conversion_status": "fonte", "mechanics_5e": "x",
              "note": None, "provisional": None, "editorial": False}]}}))

    errori = []
    for nome, dove, documento in sonde:
        v = validatore(nome)
        messaggi = [e.message for e in v.iter_errors(documento)]
        testo = json.dumps(documento)
        atteso = ("charmed" if "charmed" in testo else
                  "fonte" if "fonte" in testo else "slashing")
        if not any(atteso in m for m in messaggi):
            errori.append(
                f"{nome}: '{dove}' non ha rifiutato '{atteso}'. Il $ref a "
                f"vocabolari.schema.json non e' stato risolto: il "
                f"vocabolario sembra applicato e non lo e'")
    return errori


# --------------------------------------------------------- la sede dell'origine
#
# PERCHE' ESISTE. Fino al 03/09/2026 la dichiarazione d'origine di un valore
# era scritta in QUATTRO modi: `conversion_status` + `source` in
# mostro.schema.json, in oggetto.schema.json e in modello.schema.json — tre
# copie dello stesso enum, di cui una gia' divergente (oggetto ne aveva sette
# voci, gli altri cinque) — e `cd_origine` + `bonus_origine` con un
# vocabolario tutto suo in effetto.schema.json. Nessuno dei quattro era
# sbagliato dal proprio lato, che e' la firma della struttura doppia: la
# decima del progetto, e la prima in cui le sedi erano quattro invece di due.
#
# Fonderle non basta. Una sede unica senza un controllo che la difenda e' una
# sede unica finche' qualcuno non ricopia l'enum «per non dipendere da un
# altro file», ed e' esattamente cosi' che sono nate le tre copie. Questo
# controllo e' il pezzo che paga il costo della fusione, come
# `valida_sistema.py` lo e' per le tabelle di sistema.

SEDE_ORIGINE = "vocabolari.schema.json"
DEFS_CONDIVISI = ("conversion_status", "provenienza")

# Lo stesso nome per due cose diverse, e va saputo: `conversion_status` al
# livello della SCHEDA (`mechanics_5e.conversion_status`) non dichiara
# l'origine di un valore — dice a che punto e' la conversione della scheda
# nel suo insieme, con un vocabolario suo (`da_compilare`, `in_corso`,
# `compilato`; `clonato` e `in_sospeso` nelle classi). Non e' il campo che
# questo controllo difende, e confonderli lo farebbe gridare al lupo.
STATI_DI_SCHEDA = {"da_compilare", "in_corso", "compilato",
                   "clonato", "in_sospeso"}


def _cammina(nodo, percorso=()):
    if isinstance(nodo, dict):
        yield percorso, nodo
        for k, v in nodo.items():
            yield from _cammina(v, percorso + (k,))
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            yield from _cammina(v, percorso + (str(i),))


# SI METTE ALLA PROVA. Su un insieme di schemi pulito un rilevatore rotto e
# uno funzionante tacciono allo stesso modo, e la differenza si scopre il
# giorno in cui serviva. E' la stessa ragione — e la stessa forma — delle
# COPIE_PIANTATE di `dati/_sistema.py`: tre difetti costruiti apposta, uno
# per pretesa, e due schemi che ci somigliano senza esserlo.
DIFETTI_PIANTATI = [
    ("enum ridigitato fuori dalla sede",
     {"$defs": {"conversion_status": {
         "enum": ["direct", "adapted", "derived", "pending", "source_only"]}}}),
    ("$defs condiviso che non rimanda alla sede",
     {"$defs": {"provenienza": {"type": "string"}}}),
    ("meta' della dichiarazione: `conversion_status` senza `source`",
     {"properties": {"armor_class": {"properties": {
         "value": {"type": "integer"},
         "conversion_status": {"$ref": "vocabolari.schema.json#/$defs/conversion_status"}}}}}),
]

INNOCENTI = [
    ("lo stato della SCHEDA, che ha un vocabolario suo e nessun `source`",
     {"properties": {"mechanics_5e": {"properties": {"conversion_status": {
         "enum": ["da_compilare", "in_corso", "compilato"]}}}}}),
    ("le due meta' insieme, riferite alla sede",
     {"properties": {"hit_points": {"properties": {
         "average": {"type": "integer"},
         "conversion_status": {"$ref": "vocabolari.schema.json#/$defs/conversion_status"},
         "source": {"$ref": "vocabolari.schema.json#/$defs/provenienza"}}}}}),
]


def _difetti_in(nome, schema):
    """I difetti d'origine di UNO schema gia' caricato. Vedi verifica_origine."""
    errori = []
    for percorso, nodo in _cammina(schema):
        enum = nodo.get("enum") if isinstance(nodo, dict) else None
        ultimo = percorso[-1] if percorso else ""

        # 1. l'enum ridigitato fuori dalla sede
        if (nome != SEDE_ORIGINE and enum
                and ultimo in DEFS_CONDIVISI + ("source",)
                and not (set(enum) & STATI_DI_SCHEDA)):
            errori.append(
                f"{nome}: '{'.'.join(percorso)}' ridigita l'enum "
                f"dell'origine ({enum}). La sede e' {SEDE_ORIGINE}: si "
                f"riferisce con $ref, non si ricopia "
                f"(decisione 55 (`origine-sede-unica`)")

        # 2. i $defs condivisi sono solo un rimando
        if (nome != SEDE_ORIGINE and len(percorso) == 2
                and percorso[0] == "$defs" and ultimo in DEFS_CONDIVISI):
            if "$ref" not in nodo:
                errori.append(
                    f"{nome}: $defs/{ultimo} non e' un $ref a {SEDE_ORIGINE}")
            elif SEDE_ORIGINE not in nodo["$ref"]:
                errori.append(
                    f"{nome}: $defs/{ultimo} rimanda a '{nodo['$ref']}' "
                    f"invece che a {SEDE_ORIGINE}")

        # 3. le due meta' della dichiarazione stanno insieme
        props = nodo.get("properties") if isinstance(nodo, dict) else None
        if isinstance(props, dict) and "conversion_status" in props:
            cs = props["conversion_status"]
            di_scheda = set((cs or {}).get("enum") or ()) & STATI_DI_SCHEDA
            if not di_scheda and "source" not in props:
                errori.append(
                    f"{nome}: '{'.'.join(percorso)}' dichiara "
                    f"`conversion_status` senza `source` accanto: meta' di "
                    f"una dichiarazione d'origine dice come e non dice da "
                    f"dove")
    return errori


def prova_di_se_stesso():
    """Il rilevatore vede i difetti piantati e tace sui due innocenti?

    Torna (visti, quanti, errori). Chiamato dai validatori insieme a
    `verifica_origine()`: un controllo di cui non si e' provata la vista
    viene creduto piu' di quanto valga."""
    errori, visti = [], 0
    for etichetta, schema in DIFETTI_PIANTATI:
        if _difetti_in("piantato.schema.json", schema):
            visti += 1
        else:
            errori.append(f"difetto piantato NON visto — {etichetta}")
    for etichetta, schema in INNOCENTI:
        for m in _difetti_in("innocente.schema.json", schema):
            errori.append(f"falso allarme su un caso lecito — {etichetta}: {m}")
    return visti, len(DIFETTI_PIANTATI), errori


def verifica_origine():
    """La dichiarazione d'origine ha una sede sola? Torna un elenco di errori.

    Tre pretese, e nessuna delle tre e' verificabile validando i dati: sono
    difetti degli SCHEMI, e uno schema che si ricopia un enum valida
    benissimo finche' le due copie coincidono.

    1. Nessuno schema tranne la sede definisce l'enum dell'origine. Chi lo
       ridigita crea la copia numero due.
    2. Dove un `$defs` porta uno dei due nomi condivisi, e' un `$ref` alla
       sede e nient'altro.
    3. `conversion_status` e `source` viaggiano insieme. Una meta' sola non
       e' una dichiarazione d'origine: dice come senza dire da dove, o il
       contrario."""
    errori = []
    for f in sorted(glob.glob(os.path.join(CARTELLA, "*.json"))):
        nome = os.path.basename(f)
        with open(f, encoding="utf-8") as fh:
            errori += _difetti_in(nome, json.load(fh))
    return errori
