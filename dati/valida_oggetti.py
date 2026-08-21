#!/usr/bin/env python3
"""
Valida dati/oggetti/*.json contro dati/schema/oggetto.schema.json ed esegue
controlli di coerenza che lo schema da solo non puo' esprimere: in
particolare l'esclusione reciproca fra source_2e e source_srd, che dipende
da source.source_edition (vedi la nota in cima allo schema).

Uso:  python3 dati/valida_oggetti.py
Esce con codice 1 se trova errori.
"""

import glob
import json
import os
import re
import sys

import jsonschema

BASE = os.path.dirname(os.path.abspath(__file__))
Validator = getattr(jsonschema, "Draft202012Validator", None) or jsonschema.Draft7Validator

DADO = re.compile(r"^\d+d\d+([+-]\d+)?$")
DADO_O_FISSO = re.compile(r"^(\d+d\d+([+-]\d+)?|\d+)$")


def coerenza(d, err):
    ed = d["source"]["source_edition"]
    ha_2e = "source_2e" in d
    ha_srd = "source_srd" in d

    if ed == "2e":
        if not ha_2e:
            err("source.source_edition e' '2e' ma manca source_2e")
        if ha_srd:
            err("source.source_edition e' '2e' ma e' presente anche source_srd (mutuamente esclusivi)")
        if "pages_pdf" not in d["source"]:
            err("source.source_edition e' '2e' ma manca source.pages_pdf")
        if ha_2e and not (d["source_2e"].get("weapon_table") or d["source_2e"].get("armor_table")
                           or d["source_2e"].get("magic_item_text") or d["source_2e"].get("creatura_legata_2e")):
            err("source_2e non compila nessuna delle sotto-tabelle (weapon_table/armor_table/magic_item_text/creatura_legata_2e)")
    elif ed == "SRD 5.1":
        if not ha_srd:
            err("source.source_edition e' 'SRD 5.1' ma manca source_srd")
        if ha_2e:
            err("source.source_edition e' 'SRD 5.1' ma e' presente anche source_2e (mutuamente esclusivi)")
        if "pages_pdf" in d["source"]:
            err("source.source_edition e' 'SRD 5.1' ma e' presente source.pages_pdf, che non si applica")
    else:
        err(f"source.source_edition sconosciuto: {ed!r}")

    m = d["mechanics_5e"]
    w = m.get("weapon_5e")
    if w and not DADO_O_FISSO.match(w["damage_dice"]):
        err(f"weapon_5e.damage_dice: formula '{w['damage_dice']}' non riconosciuta")

    if d["categoria"] == "arma" and not w:
        err("categoria 'arma' ma mechanics_5e.weapon_5e e' vuoto")
    if d["categoria"] in ("armatura", "scudo") and not m.get("armor_5e"):
        err(f"categoria '{d['categoria']}' ma mechanics_5e.armor_5e e' vuoto")

    if d["magico"] and m.get("rarity") is None:
        err("magico=true ma rarity e' null")


def main():
    schema = json.load(open(os.path.join(BASE, "schema", "oggetto.schema.json")))
    Validator.check_schema(schema)
    v = Validator(schema)

    files = sorted(glob.glob(os.path.join(BASE, "oggetti", "*.json")))
    if not files:
        print("nessun file in dati/oggetti/ — esegui prima build_oggetti.py")
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
        else:
            print(f"✓ {nome}")

    # creatura_legata deve referenziare un mostro esistente
    mostri_dir = os.path.join(BASE, "mostri")
    mostri_ids = {os.path.splitext(os.path.basename(p))[0]
                  for p in glob.glob(os.path.join(mostri_dir, "*.json"))} if os.path.isdir(mostri_dir) else set()
    for p in files:
        d = json.load(open(p, encoding="utf-8"))
        cl = d["mechanics_5e"].get("creatura_legata")
        if cl and mostri_ids and cl["monster_id"] not in mostri_ids:
            print(f"✗ {os.path.basename(p)}: creatura_legata.monster_id '{cl['monster_id']}' inesistente in dati/mostri/")
            totale_errori += 1

    print(f"\n{len(files)} file controllati, {totale_errori} errori.")
    return 1 if totale_errori else 0


if __name__ == "__main__":
    sys.exit(main())
