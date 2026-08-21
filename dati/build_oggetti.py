#!/usr/bin/env python3
"""
Genera dati/oggetti/*.json per l'equipaggiamento ordinario (armi, armature,
attrezzatura d'avventura) a partire da _fonti/srd51_equipaggiamento.py.

Non tocca i file che non genera: il diadema (dati/oggetti/diadema-anima-legata.json)
e' scritto a mano, e' il caso "creatura legata" dello schema, non equipaggiamento
ordinario. Questo script copre solo gli oggetti con `source.source_edition ==
"SRD 5.1"` (vedi oggetto.schema.json, campo `source_srd`): niente conversione da
documentare, il dato nasce gia' in 5e.

Uso:  python3 dati/build_oggetti.py
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_fonti"))
import srd51_equipaggiamento as SRD

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "oggetti")

SOURCE_BOOK = "Player's Handbook (SRD 5.1)"


def slugify(name):
    s = name.lower()
    s = s.replace("'", "").replace(",", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def base_doc(id_, name_en, name_it, categoria, descrizione, api_ref):
    return {
        "id": id_,
        "name": {"en": name_en, "it": name_it},
        "categoria": categoria,
        "magico": False,
        "source": {
            "source_edition": "SRD 5.1",
            "source_book": SOURCE_BOOK,
        },
        "valid_eras": None,
        "source_srd": {
            "descrizione": descrizione,
            "api_ref": api_ref,
            "note": None,
        },
        "mechanics_5e": {
            "conversion_status": "compilato",
            "weapon_5e": None,
            "armor_5e": None,
            "rarity": None,
            "attunement": None,
            "proprieta_magiche": [],
            "creatura_legata": None,
            "note": [],
        },
    }


def build_armi():
    docs = []
    for name_en, name_it, cat_2014, dice, dtype, props, cost, weight, api_ref in SRD.ARMI:
        id_ = slugify(name_en)
        note = []
        if dice in ("0", "1"):
            note.append(
                "damage_dice non e' una formula NdM: il valore e' quello letto dall'SRD "
                "(vedi dati/_fonti/srd51_equipaggiamento.py, sezione anomalie)."
            )
        if dtype is None:
            note.append(
                "damage_type 'nessuno' e' un segnaposto nostro: la fonte non ne dichiara "
                "uno per quest'arma (Net, arma di controllo senza danno)."
            )
        d = base_doc(
            id_, name_en, name_it, "arma",
            f"Arma dell'SRD 5.1, tabella Equipaggiamento del Player's Handbook ({cat_2014}).",
            api_ref,
        )
        d["mechanics_5e"]["weapon_5e"] = {
            "damage_dice": dice,
            "damage_type": dtype if dtype is not None else "nessuno",
            "properties": props,
            "weight_lb": weight,
            "cost_gp": cost,
            "conversion_status": "direct",
            "source": "SRD 5.1",
            "note": ", ".join(note) if note else None,
        }
        docs.append((id_, d))
    return docs


def build_armature():
    docs = []
    for name_en, name_it, cat, ac_string, str_req, stealth_dis, cost, weight, api_ref in SRD.ARMATURE:
        id_ = slugify(name_en)
        categoria = "scudo" if cat == "scudo" else "armatura"
        d = base_doc(
            id_, name_en, name_it, categoria,
            f"Armatura dell'SRD 5.1, tabella Equipaggiamento del Player's Handbook (categoria: {cat}).",
            api_ref,
        )
        d["mechanics_5e"]["armor_5e"] = {
            "ac_formula": ac_string,
            "strength_requirement": str_req,
            "stealth_disadvantage": stealth_dis,
            "weight_lb": weight,
            "cost_gp": cost,
            "conversion_status": "direct",
            "source": "SRD 5.1",
            "note": None,
        }
        docs.append((id_, d))
    return docs


def build_attrezzatura():
    docs = []
    for name_en, name_it, desc, cost, weight, api_ref in SRD.ATTREZZATURA:
        id_ = slugify(name_en)
        d = base_doc(id_, name_en, name_it, "attrezzatura", desc, api_ref)
        d["mechanics_5e"]["note"] = [
            f"Peso {weight} lb, costo {cost} mo (SRD 5.1, direct)."
        ]
        # L'attrezzatura non ha weapon_5e/armor_5e: costo e peso restano
        # dentro source_srd/mechanics_5e.note, non c'e' una sottosezione
        # dedicata come per armi e armature (lo schema non ne prevede una:
        # la Fase 2 doveva coprire il combattimento, non l'inventario).
        docs.append((id_, d))
    return docs


def main():
    os.makedirs(OUT, exist_ok=True)
    tutti = build_armi() + build_armature() + build_attrezzatura()

    visti = set()
    for id_, _ in tutti:
        if id_ in visti:
            sys.exit(f"id duplicato: {id_}")
        visti.add(id_)

    index = []
    for id_, doc in tutti:
        path = os.path.join(OUT, id_ + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
            f.write("\n")
        index.append({
            "id": id_,
            "name_it": doc["name"]["it"],
            "categoria": doc["categoria"],
            "file": "oggetti/" + id_ + ".json",
        })
        print("scritto", path)

    # Il diadema e' scritto a mano e non generato qui, ma appartiene comunque
    # all'indice: senza, l'indice mentirebbe sul totale di oggetti disponibili.
    diadema_path = os.path.join(OUT, "diadema-anima-legata.json")
    if os.path.exists(diadema_path):
        with open(diadema_path, encoding="utf-8") as f:
            diadema = json.load(f)
        index.append({
            "id": diadema["id"],
            "name_it": diadema["name"]["it"],
            "categoria": diadema["categoria"],
            "file": "oggetti/diadema-anima-legata.json",
        })

    with open(os.path.join(BASE, "oggetti.index.json"), "w", encoding="utf-8") as f:
        json.dump({"count": len(index), "items": index}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n{len(tutti)} oggetti generati (+ 1 scritto a mano), {len(index)} nell'indice.")


if __name__ == "__main__":
    main()
