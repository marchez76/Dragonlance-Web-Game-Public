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


# --------------------------------------------------------------------------
# DA PROSA A NUMERI — le proprieta' delle armi e la formula di CA.
#
# Il RAPPORTO-personaggio (§2, §5.2) misura il buco: la categoria dell'arma
# e' assente su 37 armi su 37, la gittata pure, e 10 proprieta' distinte
# portano un numero annegato nel testo ("versatile (1d10)", "ammunition
# (range 150/600)") per 21 occorrenze. La gittata di un'arma a distanza si
# poteva ottenere solo con un'espressione regolare a runtime, cioe' il motore
# avrebbe dovuto interpretare la prosa a ogni turno.
#
# La conversione avviene QUI, nel generatore, e non a valle sui JSON gia'
# scritti: e' il punto 2 di CLAUDE.md, ed e' gia' costato tre sfasamenti al
# progetto. La lista `properties` della fonte NON viene rimossa — resta la
# trascrizione fedele dell'SRD, e `dati/valida_effetti.py` la rilegge per
# verificare che la struttura qui sotto continui a dire la stessa cosa.
# --------------------------------------------------------------------------

CATEGORIA_ARMA = {
    "Simple Melee Weapons": ("semplice", "mischia"),
    "Simple Ranged Weapons": ("semplice", "distanza"),
    "Martial Melee Weapons": ("da_guerra", "mischia"),
    "Martial Ranged Weapons": ("da_guerra", "distanza"),
}

_GITTATA = re.compile(r"\(range\s+(\d+)\s*/\s*(\d+)\)")
_VERSATILE = re.compile(r"versatile\s*\((\d+d\d+)\)")

PORTATA_BASE_FT = 5.0
PORTATA_REACH_FT = 10.0


def proprieta_strutturate(props, tipo):
    """Le `properties` dell'SRD in campi. La prosa resta accanto, intatta."""
    testo = " ".join(props).lower()
    g = _GITTATA.search(testo)
    v = _VERSATILE.search(testo)
    ha = lambda k: any(p.lower().startswith(k) for p in props)

    reach = ha("reach")
    return {
        "finesse": ha("finesse"),
        "leggera": ha("light"),
        "pesante": ha("heavy"),
        "due_mani": ha("two-handed"),
        "portata_estesa": reach,
        "ricarica": ha("loading"),
        "munizioni": ha("ammunition"),
        "lanciabile": ha("thrown"),
        "speciale": ha("special"),
        "versatile_dadi": v.group(1) if v else None,
        # La gittata appartiene sia alle armi da lancio sia a quelle a
        # munizioni: la stessa parentesi, due proprieta' diverse.
        "gittata_ft": ({"normale": float(g.group(1)), "lunga": float(g.group(2))}
                       if g else None),
        # Portata solo per la mischia. 5 piedi e' il valore implicito della
        # 5e, che la tabella non stampa perche' e' il default: reso esplicito
        # qui perche' un motore non puo' leggere un valore che non c'e'.
        "portata_ft": (None if tipo != "mischia"
                       else (PORTATA_REACH_FT if reach else PORTATA_BASE_FT)),
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
        categoria, tipo = CATEGORIA_ARMA[cat_2014]
        d["mechanics_5e"]["weapon_5e"] = {
            "categoria": categoria,
            "tipo": tipo,
            "damage_dice": dice,
            "damage_type": dtype if dtype is not None else "nessuno",
            "properties": props,
            "proprieta_5e": proprieta_strutturate(props, tipo),
            "weight_lb": weight,
            "cost_gp": cost,
            "conversion_status": "direct",
            "source": "SRD 5.1",
            "note": ", ".join(note) if note else None,
        }
        docs.append((id_, d))
    return docs


_CA_BASE = re.compile(r"^(\d+)")
_CA_MAXDEX = re.compile(r"max\s+(\d+)")
_CA_BONUS = re.compile(r"^\+(\d+)$")


def ca_strutturata(ac_string, categoria):
    """`ac_formula` in campi. Delle 13 voci solo 4 portano un numero secco:
    8 sono formule da interpretare ("14 + Dex modifier (max 2)") e lo scudo
    e' un modificatore ("+2"). Interpretarle a ogni turno era il difetto
    misurato in RAPPORTO-personaggio §5.2."""
    testo = ac_string.strip()
    bonus = _CA_BONUS.match(testo)
    if bonus:
        # Lo scudo non ha una CA propria: somma alla CA di chi lo porta.
        return {"ca_base": None, "bonus_ca": int(bonus.group(1)),
                "applica_mod_dex": False, "mod_dex_max": None}
    base = _CA_BASE.match(testo)
    if not base:
        raise ValueError(f"ac_formula non riconosciuta: {ac_string!r}")
    dex = "dex modifier" in testo.lower()
    cap = _CA_MAXDEX.search(testo.lower())
    return {
        "ca_base": int(base.group(1)),
        "bonus_ca": None,
        "applica_mod_dex": dex,
        # None con applica_mod_dex true = nessun tetto (armature leggere).
        # E' una distinzione vera: 0 significherebbe "il Dex non conta".
        "mod_dex_max": int(cap.group(1)) if cap else None,
    }


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
            "categoria": cat,
            "ac_formula": ac_string,
            "ca_5e": ca_strutturata(ac_string, cat),
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
