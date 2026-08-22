#!/usr/bin/env python3
"""
Genera dati/incantesimi/*.json dai 319 incantesimi dell'SRD 5.1 in
_fonti/srd51_incantesimi.py.

A differenza di build_razze.py/build_classi.py/build_oggetti.py, questo
generatore non incorpora testo 2e: incantesimo.schema.json non ha un
source_2e da compilare, quindi dati/incantesimi/ non e' una zona da
proteggere come dati/oggetti/ — vedi la nota in cima allo schema e la
motivazione nel .gitignore.

Uso:  python3 dati/build_incantesimi.py
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_fonti"))
import srd51_incantesimi as SRD

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "incantesimi")

SOURCE_BOOK = "Player's Handbook (SRD 5.1)"


def slugify(name):
    s = name.lower().replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def build(row):
    (name_en, name_it, level, school, classes, ritual_caster_feat, casting_time,
     range_, duration, ritual, concentration, verbal, somatic, material,
     material_desc, desc, higher_level, api_ref) = row

    id_ = slugify(name_en)
    note = []
    if material and not material_desc:
        note.append(
            "components.material=true ma material_desc e' vuoto: gap dell'API "
            "(sia v1 sia v2 di api.open5e.com hanno il campo materiale vuoto per "
            "questo incantesimo), non un'omissione nostra. Non riempito a memoria: "
            "vedi dati/_fonti/srd51_incantesimi.py per la verifica incrociata fatta."
        )

    return id_, {
        "id": id_,
        "name": {"en": name_en, "it": name_it},
        "level": level,
        "school": school,
        "classes": classes,
        "ritual_caster_feat": ritual_caster_feat,
        "casting_time": casting_time,
        "range": range_,
        "duration": duration,
        "ritual": ritual,
        "concentration": concentration,
        "components": {
            "verbal": verbal,
            "somatic": somatic,
            "material": material,
            "material_desc": material_desc,
        },
        "source": {
            "source_edition": "SRD 5.1",
            "source_book": SOURCE_BOOK,
            "api_ref": api_ref,
        },
        "descrizione": desc,
        "a_livelli_superiori": higher_level,
        "note": note,
    }


def main():
    os.makedirs(OUT, exist_ok=True)

    visti = set()
    index = []
    for row in SRD.INCANTESIMI:
        id_, doc = build(row)
        if id_ in visti:
            sys.exit(f"id duplicato: {id_}")
        visti.add(id_)

        path = os.path.join(OUT, id_ + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
            f.write("\n")
        index.append({
            "id": id_,
            "name_it": doc["name"]["it"],
            "level": doc["level"],
            "school": doc["school"],
            "classes": doc["classes"],
            "file": "incantesimi/" + id_ + ".json",
        })
        print("scritto", path)

    with open(os.path.join(BASE, "incantesimi.index.json"), "w", encoding="utf-8") as f:
        json.dump({"count": len(index), "spells": index}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n{len(index)} incantesimi generati.")


if __name__ == "__main__":
    main()
