#!/usr/bin/env python3
"""
Valida dati/incantesimi/*.json contro dati/schema/incantesimo.schema.json.

Uso:  python3 dati/valida_incantesimi.py
Esce con codice 1 se trova errori.
"""

import glob
import json
import os
import sys

import jsonschema

BASE = os.path.dirname(os.path.abspath(__file__))
Validator = getattr(jsonschema, "Draft202012Validator", None) or jsonschema.Draft7Validator


def coerenza(d, err):
    if d["source"]["source_edition"] != "SRD 5.1":
        err(f"source_edition inatteso: {d['source']['source_edition']!r}")
    if not d["classes"]:
        err("classes vuoto")
    c = d["components"]
    if not (c["verbal"] or c["somatic"] or c["material"]):
        err("components: nessuna componente richiesta (v/s/m tutte false)")
    if c["material"] and not c["material_desc"] and not d["note"]:
        err("components.material=true ma material_desc e' vuoto, senza una nota che lo spieghi")
    if not c["material"] and c["material_desc"]:
        err("components.material=false ma material_desc e' valorizzato")


def main():
    schema = json.load(open(os.path.join(BASE, "schema", "incantesimo.schema.json")))
    Validator.check_schema(schema)
    v = Validator(schema)

    files = sorted(glob.glob(os.path.join(BASE, "incantesimi", "*.json")))
    if not files:
        print("nessun file in dati/incantesimi/ — esegui prima build_incantesimi.py")
        return 1

    ids, totale_errori = set(), 0
    for p in files:
        nome = os.path.basename(p)
        d = json.load(open(p, encoding="utf-8"))
        errori = []

        for e in sorted(v.iter_errors(d), key=lambda e: list(e.path)):
            errori.append(f"[schema] {'.'.join(map(str, e.path)) or '(radice)'}: {e.message[:160]}")

        if not errori:
            coerenza(d, errori.append)

        if d["id"] in ids:
            errori.append(f"id duplicato: {d['id']}")
        ids.add(d["id"])
        if d["id"] + ".json" != nome:
            errori.append(f"il nome del file non corrisponde all'id ({d['id']})")

        if errori:
            totale_errori += len(errori)
            print(f"✗ {nome}")
            for e in errori:
                print(f"    {e}")

    print(f"\n{len(files)} file controllati, {totale_errori} errori.")
    return 1 if totale_errori else 0


if __name__ == "__main__":
    sys.exit(main())
