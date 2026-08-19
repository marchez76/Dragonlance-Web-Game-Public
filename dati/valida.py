#!/usr/bin/env python3
"""
Valida dati/razze/*.json contro dati/schema/razza.schema.json ed esegue
controlli di coerenza che lo schema da solo non puo' esprimere.

Uso:  python3 dati/valida.py
Esce con codice 1 se trova errori.
"""

import glob
import json
import os
import re
import sys

import jsonschema

BASE = os.path.dirname(os.path.abspath(__file__))
DADO = re.compile(r"^\d+d\d+([+-]\d+)?$|^\d+[+-]\d+d\d+$")

# Draft-7 basta: lo schema non usa keyword esclusive di 2020-12.
Validator = getattr(jsonschema, "Draft202012Validator", None) or jsonschema.Draft7Validator


def coerenza(d, err):
    s = d["source_2e"]

    # min <= max
    for k, v in s["ability_requirements"].items():
        lo, hi = v.get("min"), v.get("max")
        if lo is not None and hi is not None and lo > hi:
            err(f"{k}: min {lo} > max {hi}")
        for label, n in (("min", lo), ("max", hi)):
            if n is not None and not (1 <= n <= 25):
                err(f"{k}.{label} = {n} fuori dal range plausibile 1-25")

    # formule di dado ben formate
    ph = s.get("physical") or {}
    for campo in ("height_in", "weight_lb"):
        for genere, f in (ph.get(campo) or {}).items():
            if f is not None and not DADO.match(f):
                err(f"{campo}.{genere}: formula '{f}' non riconosciuta")
    mf = ((ph.get("age") or {}).get("max_formula"))
    if mf is not None and not DADO.match(mf):
        err(f"age.max_formula: formula '{mf}' non riconosciuta")

    for g in (s.get("ability_generation") or {}).values():
        if not DADO.match(g):
            err(f"ability_generation: formula '{g}' non riconosciuta")

    # nessun limite di livello duplicato
    visti = set()
    for e in s.get("class_level_limits", []):
        key = (e["group"], e["class"])
        if key in visti:
            err(f"limite di livello duplicato: {key}")
        visti.add(key)
        if e["limit"] is not None and not (1 <= e["limit"] <= 30):
            err(f"limite {e['class']} = {e['limit']} implausibile")

    # una razza giocabile deve avere almeno una classe, tranne gli umani
    # (che in 2e non compaiono nella tabella perche' non hanno limiti)
    # Una razza giocabile senza limiti di livello va spiegata: o e' un umano
    # (che in 2e non compare nella tabella), o l'assenza e' documentata fra le
    # note di fonte o le questioni aperte.
    if d["playable"] and d["category"] != "human" and not s.get("class_level_limits"):
        spiegato = s.get("open_questions") or any(
            "class_level_limits" in n or "NOTA DI FONTE" in n for n in s.get("notes", []))
        if not spiegato:
            err("razza giocabile senza class_level_limits e senza una nota che lo spieghi")

    # gli aggiustamenti devono riguardare caratteristiche note
    for k in (s.get("ability_adjustments") or {}):
        if k not in ("str", "dex", "con", "int", "wis", "cha"):
            err(f"ability_adjustments: caratteristica sconosciuta '{k}'")


def main():
    schema = json.load(open(os.path.join(BASE, "schema", "razza.schema.json")))
    Validator.check_schema(schema)
    v = Validator(schema)

    files = sorted(glob.glob(os.path.join(BASE, "razze", "*.json")))
    if not files:
        print("nessun file in dati/razze/ — esegui prima build_razze.py")
        return 1

    ids, totale_errori = set(), 0
    for p in files:
        nome = os.path.basename(p)
        d = json.load(open(p, encoding="utf-8"))
        errori = []

        for e in sorted(v.iter_errors(d), key=lambda e: list(e.path)):
            errori.append(f"[schema] {'.'.join(map(str, e.path)) or '(radice)'}: {e.message[:120]}")

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
        else:
            print(f"✓ {nome}")

    # i riferimenti parent devono esistere
    for p in files:
        d = json.load(open(p, encoding="utf-8"))
        if d["parent"] and d["parent"] not in ids:
            print(f"✗ {os.path.basename(p)}: parent '{d['parent']}' inesistente")
            totale_errori += 1

    print(f"\n{len(files)} file controllati, {totale_errori} errori.")
    return 1 if totale_errori else 0


if __name__ == "__main__":
    sys.exit(main())
