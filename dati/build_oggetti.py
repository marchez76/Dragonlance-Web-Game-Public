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

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "_fonti"))
sys.path.insert(0, BASE)
import srd51_equipaggiamento as SRD  # noqa: E402
import _voci_di_pacchetto as VP  # noqa: E402
import _vocabolari as VOC  # noqa: E402

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
            "attrezzatura_5e": None,
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
        # La traduzione avviene QUI, nel generatore, una volta sola. Prima il
        # termine SRD finiva tale e quale in `mechanics_5e` — inglese dentro
        # lo strato nostro, mentre dati/mostri/ diceva la stessa cosa in
        # italiano: l'ottava struttura doppia del progetto. Correggerla a
        # valle si sfaserebbe alla prima rigenerazione (CLAUDE.md 2).
        tipo_danno = "nessuno" if dtype is None else VOC.tipo_danno(dtype)
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
            "damage_type": tipo_danno,
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
        # PREZZO E PESO IN CAMPI, non dentro una frase
        # (decisione 62, `pacchetto-fisso`). Fino al 05/09/2026 questa riga
        # scriveva «Peso N lb, costo N mo» in `mechanics_5e.note`: due campi
        # letti dalla fonte, cuciti in una stringa italiana, e i campi
        # buttati. Erano 28 oggetti su 79 senza un prezzo leggibile, cioe'
        # senza niente a cui applicare l'aritmetica della
        # decisione 42 (`cambio-acciaio-oro`).
        d["mechanics_5e"]["attrezzatura_5e"] = {
            "cost_gp": cost,
            "weight_lb": weight,
        }
        docs.append((id_, d))
    return docs


# --------------------------------------------------------------------------
# LE VOCI CHE ESISTONO SOLO DENTRO UN PACCHETTO e che il criterio promuove a
# oggetto (decisione 63, `oggetto-se-serve-al-motore`). Quali siano non e'
# scritto qui: sta in `_voci_di_pacchetto.VOCI`, con la ragione di ciascuna.
#
# PREZZO E PESO RESTANO `null`, ed e' il punto. La tabella dell'attrezzatura
# non le elenca, quindi non c'e' un numero da leggere; scriverne uno
# plausibile sarebbe un valore nostro travestito da fonte, che e' esattamente
# cio' che la decisione 7 (`doppio-strato`) vieta. Il campo esiste e dichiara
# di non sapere — la stessa forma con cui `armor_5e.ac_formula` porta una
# formula invece di un numero, non un buco silenzioso. Chi somma un carico o
# un prezzo se ne accorge, e `_valuta.prezzo_di()` ha gia' il caso del
# `None`.
# --------------------------------------------------------------------------
def build_voci_di_pacchetto():
    docs = []
    for name_en, name_it, pacchetto in VP.oggetti():
        id_ = slugify(name_en)
        descrizione = (
            f"Voce che l'SRD 5.1 nomina solo dentro la descrizione del "
            f"{pacchetto} (sezione «Equipment Packs»): la tabella "
            f"dell'attrezzatura non la elenca, quindi non ha ne' prezzo ne' "
            f"peso propri.")
        d = base_doc(id_, name_en, name_it, "attrezzatura", descrizione,
                     VP.SEZIONE_SRD)
        d["mechanics_5e"]["attrezzatura_5e"] = {
            "cost_gp": None,
            "weight_lb": None,
        }
        d["mechanics_5e"]["note"] = [VP.ragione_di(name_en)]
        docs.append((id_, d))
    return docs


def main():
    os.makedirs(OUT, exist_ok=True)
    tutti = (build_armi() + build_armature() + build_attrezzatura()
             + build_voci_di_pacchetto())

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
