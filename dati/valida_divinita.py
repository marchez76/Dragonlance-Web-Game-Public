#!/usr/bin/env python3
"""
Valida dati/divinita/*.json contro lo schema, con controlli di coerenza e
controllo incrociato con le classi.

Uso:  python3 dati/valida_divinita.py
"""

import glob
import json
import os
import re
import sys

import jsonschema

BASE = os.path.dirname(os.path.abspath(__file__))
Validator = getattr(jsonschema, "Draft202012Validator", None) or jsonschema.Draft7Validator

# Sfere di incantesimi sacerdotali di AD&D 2e (PHB + Tome of Magic).
SFERE_NOTE = {
    "All", "Animal", "Astral", "Charm", "Combat", "Creation", "Divination",
    "Elemental", "Guardian", "Healing", "Necromantic", "Necromancy", "Plant",
    "Plants", "Protection", "Summoning", "Sun", "Weather", "Chaos", "Law",
    "Numbers", "Thought", "Time", "Travelers", "War", "Wards",
}


def coerenza(d, err):
    s = d["source_2e"]

    if not s["priest_alignment"] and not s["worshipper_alignment"]:
        err("ne' PAL ne' WAL: nessun vincolo di allineamento dichiarato")

    nomi = [sf["name"] for sf in s["spheres"]]
    if not nomi:
        err("nessuna sfera")
    if "All" not in nomi:
        err("manca la sfera All: in 2e ogni sacerdote vi ha accesso")
    if len(nomi) != len(set(nomi)):
        err(f"sfere duplicate: {[n for n in nomi if nomi.count(n) > 1]}")
    for n in nomi:
        if n not in SFERE_NOTE:
            err(f"sfera non riconosciuta: '{n}'")

    # l'ordine sacro deve seguire la famiglia celeste
    atteso = {"good": "Order of Good", "evil": "Order of Evil",
              "neutral": "Order of Neutrality"}[d["family"]]
    if d["holy_order"] != atteso:
        err(f"holy_order '{d['holy_order']}' non coerente con family '{d['family']}'")

    # l'allineamento del sacerdote deve seguire la famiglia
    pal = (s["priest_alignment"] or "").lower()
    if pal:
        # "Any non-Evil" contiene la parola evil ma significa l'opposto:
        # le negazioni vanno rimosse prima di cercare l'allineamento.
        pos = re.sub(r"\bnon-?\s*(evil|good|lawful|chaotic)\b", " ", pal)
        if d["family"] == "good" and "evil" in pos:
            err(f"divinita' del Bene con sacerdoti '{s['priest_alignment']}'")
        if d["family"] == "evil" and "good" in pos:
            err(f"divinita' del Male con sacerdoti '{s['priest_alignment']}'")


def incrociato(dei, classi, err):
    fam = {}
    for d in dei:
        fam.setdefault(d["family"], []).append(d["name"]["en"])
    for f, attesi in (("good", 7), ("evil", 7), ("neutral", 7)):
        if len(fam.get(f, [])) != attesi:
            err(f"famiglia '{f}': {len(fam.get(f, []))} divinita' invece di {attesi}")

    sacerdote = next((c for c in classi if c["id"] == "sacerdote-ordini-sacri"), None)
    if sacerdote is None:
        err("classe sacerdote-ordini-sacri assente: impossibile incrociare")
        return

    # le epoche in cui gli dei concedono poteri devono coincidere con quelle
    # in cui la classe da sacerdote e' giocabile
    ep_classe = set(sacerdote["valid_eras"])
    for d in dei:
        if set(d["valid_eras"]) != ep_classe:
            err(f"{d['id']}: valid_eras {sorted(d['valid_eras'])} diverse da quelle "
                f"di sacerdote-ordini-sacri {sorted(ep_classe)}")
            break

    # i tre dei della magia devono corrispondere alle tre vesti
    lune = {"solinari": "mago-veste-bianca", "lunitari": "mago-veste-rossa",
            "nuitari": "mago-veste-nera"}
    per_id = {c["id"] for c in classi}
    for dio, veste in lune.items():
        if not any(d["id"] == dio for d in dei):
            err(f"divinita' della magia '{dio}' mancante")
        if veste not in per_id:
            err(f"classe '{veste}' mancante, ma esiste il dio '{dio}'")


def main():
    schema = json.load(open(os.path.join(BASE, "schema", "divinita.schema.json")))
    Validator.check_schema(schema)
    v = Validator(schema)

    files = sorted(glob.glob(os.path.join(BASE, "divinita", "*.json")))
    dei = [json.load(open(p, encoding="utf-8")) for p in files]
    classi = [json.load(open(p, encoding="utf-8"))
              for p in sorted(glob.glob(os.path.join(BASE, "classi", "*.json")))]

    totale = 0
    for p, d in zip(files, dei):
        errori = []
        for e in sorted(v.iter_errors(d), key=lambda e: list(e.path)):
            errori.append(f"[schema] {'.'.join(map(str, e.path)) or '(radice)'}: {e.message[:120]}")
        if not errori:
            coerenza(d, errori.append)
        if errori:
            totale += len(errori)
            print(f"✗ {os.path.basename(p)}")
            for e in errori:
                print(f"    {e}")
        else:
            print(f"✓ {os.path.basename(p)}")

    print("\n--- controllo incrociato divinita'/classi ---")
    incr = []
    incrociato(dei, classi, incr.append)
    if incr:
        totale += len(incr)
        for e in incr:
            print(f"    ✗ {e}")
    else:
        print("    ✓ pantheon coerente con le classi")

    print(f"\n{len(files)} divinita' controllate, {totale} errori.")
    return 1 if totale else 0


if __name__ == "__main__":
    sys.exit(main())
