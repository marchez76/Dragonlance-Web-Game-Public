#!/usr/bin/env python3
"""
Valida dati/condizioni/*.json contro dati/schema/condizione.schema.json.

I controlli di coerenza sulla catena `implica` e sui riferimenti che le
condizioni ricevono dai blocchi stanno in dati/valida_effetti.py, dove ci
sono anche i blocchi che le citano: verificare un riferimento richiede
entrambi i capi, e tenerli in due file separati vorrebbe dire leggere le
condizioni due volte da due posti — la forma esatta di struttura doppia che
questa cartella esiste per evitare.

Uso:  python3 dati/valida_condizioni.py
"""

import glob
import json
import os
import sys

import jsonschema

BASE = os.path.dirname(os.path.abspath(__file__))
Validator = getattr(jsonschema, "Draft202012Validator", None) or jsonschema.Draft7Validator


def coerenza(d, err):
    # La prosa e le clausole sono due viste della stessa regola: se una
    # condizione ne dichiara una sola, non e' meta' scritta, e' incoerente.
    if not d["effetti"]:
        err("nessuna clausola in `effetti`: una condizione senza clausole "
            "non e' applicabile da un motore, e' solo un nome")
    if len(d["mechanics_5e"].split()) < 5:
        err("la prosa e' troppo corta per essere la regola: resta la forma "
            "autoritativa per una persona e va scritta per intero")

    # Le clausole limitate a certe caratteristiche devono nominarle.
    for e in d["effetti"]:
        if e["clausola"] == "fallisce_tiri_salvezza" and not e.get("caratteristiche"):
            err("`fallisce_tiri_salvezza` senza `caratteristiche`: fallire "
                "TUTTI i tiri salvezza e' un'altra regola, e nessuna "
                "condizione della 5e la usa")

    if d["id"] in (d.get("implica") or []):
        err("implica se stessa")


def main():
    schema = json.load(open(os.path.join(BASE, "schema", "condizione.schema.json"),
                            encoding="utf-8"))
    Validator.check_schema(schema)
    v = Validator(schema)

    files = sorted(glob.glob(os.path.join(BASE, "condizioni", "*.json")))
    if not files:
        print("nessun file in dati/condizioni/ — esegui prima build_condizioni.py")
        return 1

    ids, totale = set(), 0
    for p in files:
        nome = os.path.basename(p)
        d = json.load(open(p, encoding="utf-8"))
        errori = [f"[schema] {'.'.join(map(str, e.path)) or '(radice)'}: {e.message[:160]}"
                  for e in sorted(v.iter_errors(d), key=lambda e: list(e.path))]
        if not errori:
            coerenza(d, errori.append)
        if d["id"] != os.path.splitext(nome)[0]:
            errori.append(f"id '{d['id']}' diverso dal nome del file")
        if d["id"] in ids:
            errori.append(f"id duplicato: {d['id']}")
        ids.add(d["id"])

        if errori:
            print(f"✗ {nome}")
            for e in errori:
                print(f"    {e}")
            totale += len(errori)
        else:
            print(f"✓ {nome}")

    print(f"\n{len(files)} condizioni controllate, {totale} errori.")
    return 1 if totale else 0


if __name__ == "__main__":
    sys.exit(main())
