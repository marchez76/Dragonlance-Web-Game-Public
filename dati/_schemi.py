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
    errori = []
    for nome, dove, documento in sonde:
        v = validatore(nome)
        messaggi = [e.message for e in v.iter_errors(documento)]
        if not any("slashing" in m for m in messaggi):
            errori.append(
                f"{nome}: '{dove}' non ha rifiutato 'slashing'. Il $ref a "
                f"vocabolari.schema.json non e' stato risolto: il "
                f"vocabolario sembra applicato e non lo e'")
    return errori
