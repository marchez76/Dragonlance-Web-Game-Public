#!/usr/bin/env python3
"""
Genera dati/mostri.index.json leggendo dati/mostri/*.json.

L'indice era mantenuto a mano ed e' arrivato a sfasarsi (mancavano Kapak e
Sivak senza che nessuno se ne accorgesse): stesso difetto dei conteggi
scritti a mano nella prosa (CLAUDE.md, punto 3). Qui l'indice e' un derivato
del contenuto della cartella, non una lista tenuta in sincronia a parte.

Uso:  python3 dati/build_mostri_index.py
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
MOSTRI_DIR = os.path.join(BASE, "mostri")
OUT = os.path.join(BASE, "mostri.index.json")


def main():
    voci = []
    for nome_file in sorted(os.listdir(MOSTRI_DIR)):
        if not nome_file.endswith(".json"):
            continue
        with open(os.path.join(MOSTRI_DIR, nome_file), encoding="utf-8") as f:
            m = json.load(f)
        voci.append({
            "id": m["id"],
            "name_it": m["name"]["it"],
            "ruolo": m["ruolo"],
            "challenge_rating": m["mechanics_5e"]["challenge_rating"]["value"],
            "file": "mostri/" + nome_file,
        })

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"count": len(voci), "mostri": voci}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"{len(voci)} mostri indicizzati.")


if __name__ == "__main__":
    main()
