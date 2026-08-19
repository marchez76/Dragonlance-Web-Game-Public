#!/usr/bin/env python3
"""
Valida dati/schema/mostro.schema.json costruendo i cinque draconici IN MEMORIA.

PERCHE' IN MEMORIA E NON SU FILE
    Questo giro non converte mostri: prima lo schema, poi i nomi corrotti, poi
    la conversione. Costruire i cinque draconici serve a PROVARE LO SCHEMA, non
    a popolare `dati/mostri/`, che infatti non viene creata.

    I cinque sono l'unico caso in cui entrambi gli strati sono gia' noti da
    fonte: il 2e dall'MC Appendix, il 5e da Shadow of the Dragon Queen. Se lo
    schema li regge senza forzature, regge.

COSA VERIFICA
    1. conformita' allo schema JSON;
    2. copertura: quali campi restano vuoti, e se restano vuoti perche' la
       fonte 2e non li ha (allora e' un limite noto) o perche' lo schema e'
       sbagliato (allora va corretto);
    3. che i campi della decisione 27 finiscano dove devono.

Uso:  python3 dati/valida_mostri.py
Esce con codice 1 se trova errori.
"""

import json
import os
import sys

import jsonschema

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import _draconici as D

SCHEMA = os.path.join(BASE, "schema", "mostro.schema.json")
LIBRO_2E = "MC - Dragonlance Appendix"
FONTE_MC = "MC - Dragonlance Appendix"
FONTE_SOT = "SotDQ (ufficiale 5e)"

# Ruolo assegnato da noi. Dove 2e e 5e divergono lo diciamo.
RUOLI = {
    "Baaz":  ("fante", None, None),
    "Bozak": ("incantatore", None, None),
    "Kapak": ("assassino", "assassino",
              "In 2e era un assassino con UN attacco da 1-4 e il veleno come "
              "minaccia: profilo furtivo, danno basso. In 5e resta assassino di "
              "nome ma cambia asse: due pugnali avvelenati, 24 danni per round, "
              "39 PF contro una mediana SRD di 58 al GS 3. E' un cannone di "
              "vetro, e in 2e non lo era."),
    "Sivak": ("bruto", None, None),
    "Aurak": ("comandante", None, None),
}

# Le sei caratteristiche: la 2e non le da' ai mostri. Nei draconici le
# prendiamo dallo statblock ufficiale 5e, che e' fonte a pieno titolo.
ABILITIES = {
    "Baaz":  {"str": 13, "dex": 11, "con": 13, "int": 8,  "wis": 8,  "cha": 10},
    "Bozak": {"str": 14, "dex": 10, "con": 11, "int": 11, "wis": 10, "cha": 14},
    "Kapak": {"str": 11, "dex": 17, "con": 14, "int": 12, "wis": 13, "cha": 11},
    "Sivak": {"str": 18, "dex": 10, "con": 18, "int": 13, "wis": 10, "cha": 10},
    "Aurak": {"str": 13, "dex": 14, "con": 16, "int": 16, "wis": 11, "cha": 17},
}

SALVEZZA = {
    "Baaz": [], "Bozak": ["int", "wis", "cha"], "Kapak": ["dex"],
    "Sivak": ["str", "wis"], "Aurak": ["int", "wis", "cha"],
}

SENSI = {
    "Baaz": ["darkvision 60 ft."], "Bozak": ["darkvision 60 ft."],
    "Kapak": ["darkvision 60 ft."], "Sivak": ["darkvision 60 ft."],
    "Aurak": ["truesight 60 ft."],
}

PASSIVA = {"Baaz": 9, "Bozak": 10, "Kapak": 13, "Sivak": 10, "Aurak": 13}

ABILITA = {
    "Kapak": [("Deception", 4, None), ("Perception", 3, "—"),
              ("Stealth", 7, "move silently 15%, hide in shadows 10%")],
    "Aurak": [("Perception", 3, None)],
}

IMMUNITA_DANNO = {"Kapak": ["poison"]}
IMMUNITA_COND = {"Kapak": ["poisoned"], "Aurak": ["charmed"]}

MR = {"Baaz": 20, "Bozak": 20, "Kapak": 20, "Sivak": 20, "Aurak": 30}

MORALE_VAL = {"Baaz": 13, "Bozak": 13, "Kapak": 13, "Sivak": 14, "Aurak": 15}

PAGINE_2E = {"Baaz": 64, "Bozak": 69, "Kapak": 74, "Sivak": 78, "Aurak": 59}

NOTA_MR = (
    "DECISIONE 27, gruppo C: RINVIATA alla Fase 2. Il 20-30% della 2e negava "
    "l'incantesimo del tutto, inclusi quelli senza tiro salvezza; il tratto 5e "
    "piu' vicino da' vantaggio ai tiri salvezza contro magia — piu' debole in "
    "un senso, molto piu' forte in un altro, e comunque non equivalente. "
    "Inoltre i Gradi di Sfida su cui stiamo calibrando presuppongono che la "
    "resistenza magica non ci sia: aggiungerla farebbe pesare ogni incontro "
    "piu' del suo GS dichiarato, sistematicamente. Si decide in arena.")


def elemento(nome, testo_5e, stato, fonte, testo_2e=None, nota=None):
    return {"name": nome, "text_2e": testo_2e, "mechanics_5e": testo_5e,
            "conversion_status": stato, "source": fonte,
            "analogo_srd": None, "note": nota, "editorial": False,
            "provisional": None}


def costruisci(n):
    a, b = D.DUE_E[n], D.CINQUE_E[n]
    ruolo, ruolo_2e, ruolo_note = RUOLI[n]

    s2e = {
        "climate_terrain": a.get("climate", "Any, but usually tropical"),
        "frequency": a["frequency"],
        "organization": a["organization"],
        "activity_cycle": a["activity"],
        "diet": a["diet"],
        "intelligence": a["intelligence"],
        "treasure": a["treasure"],
        "alignment": a["alignment"],
        "no_appearing": a["no_appearing"],
        "armor_class": a["ac"],
        "armor_class_note": "Scala discendente della 2e.",
        "movement": a["movement"],
        "hit_dice": str(a["hd"]),
        "thac0": a["thac0"],
        "no_of_attacks": a["attacks"],
        "damage_per_attack": a["damage"],
        "special_attacks": a["special_attacks"],
        "special_defenses": a["special_defenses"],
        "magic_resistance": a["magic_resistance"],
        "size": a["size"],
        "morale": a["morale"],
        "xp_value": a["xp"],
        "abilities_text": [a["note"]],
        "death_effect": a["morte"],
        "notes": [],
        "open_questions": [],
        "raw": None,
    }

    tratti = [elemento(nome, testo, "direct", FONTE_SOT) for nome, testo in b["tratti"]]
    azioni = [elemento(nome, testo, "direct", FONTE_SOT) for nome, testo in b["azioni"]]
    reazioni = [elemento(nome, testo, "direct", FONTE_SOT)
                for nome, testo in b.get("reazioni", [])]
    # l'effetto alla morte esiste in entrambe le edizioni: lo colleghiamo
    for t in tratti:
        if t["name"] == "Death Throes":
            t["text_2e"] = a["morte"]
            t["note"] = ("Effetto identitario del draconico. In 2e colpiva "
                         "senza tiro salvezza; la 5e lo riscrive con un TS.")

    m5e = {
        "conversion_status": "compilato",
        "size": b["size"],
        "type": b["type"].split(" (")[0],
        "subtype": (b["type"].split(" (")[1].rstrip(")")
                    if " (" in b["type"] else None),
        "alignment": b["alignment"],
        "armor_class": {
            "value": b["ac"], "from": b["ac_from"], "ac_2e": a["ac"],
            "conversion_status": "direct", "source": FONTE_SOT,
            "analogo_srd": None,
            "note": f"CA 2e {a['ac']} (scala discendente) -> CA 5e {b['ac']}.",
        },
        "hit_points": {
            "average": b["hp"], "formula": b["hp_formula"],
            "hd_2e": str(a["hd"]),
            "conversion_status": "direct", "source": FONTE_SOT,
            "analogo_srd": None,
            "note": f"{a['hd']} DV in 2e -> {b['hp']} PF, "
                    f"rapporto {b['hp']/a['hd']:.1f} per dado.",
        },
        "speed": {
            "walk": int(b["speed"].split(" ft.")[0]),
            "fly": 60 if "fly" in b["speed"] else None,
            "swim": None,
            "climb": 40 if "climb" in b["speed"] else None,
            "burrow": None, "hover": False,
            "movement_2e": a["movement"],
            "note": None,
        },
        "abilities": ABILITIES[n],
        "abilities_note": ("La 2e non assegna le sei caratteristiche ai mostri: "
                           "questi valori vengono dallo statblock ufficiale 5e."),
        "saving_throws": {"proficient": SALVEZZA[n],
                          "note": f"In 2e: {a['special_defenses']}."},
        "skills": [{"name": nome, "bonus": bon, "from_2e": da}
                   for nome, bon, da in ABILITA.get(n, [])],
        "damage_resistances": [],
        "damage_immunities": IMMUNITA_DANNO.get(n, []),
        "damage_vulnerabilities": [],
        "condition_immunities": IMMUNITA_COND.get(n, []),
        "senses": SENSI[n],
        "passive_perception": PASSIVA[n],
        "languages": ["Common", "Draconic"],
        "challenge_rating": {
            "value": b["cr"], "xp": b["xp"], "proficiency_bonus": b["pb"],
            "conversion_status": "direct", "source": FONTE_SOT,
            "analogo_srd": None,
            "note": (ruolo_note if n == "Kapak" else
                     f"In 2e valeva {a['xp']} PE con la formula 2e, che NON si "
                     f"copia: i PE della 5e derivano dal GS."),
        },
        "traits": tratti,
        "actions": azioni,
        "bonus_actions": [],
        "reactions": reazioni,
        "legendary_actions": [],
        "morale_2e": {
            "value": MORALE_VAL[n], "label": a["morale"],
            "destinazione": "ia_combattimento",
            "note": ("DECISIONE 27, gruppo B. Senza morale ogni scontro finisce "
                     "con tutti i nemici morti fino all'ultimo: in un gioco in "
                     "solitario il DM e' il motore, e questo parametro gli "
                     "serve."),
        },
        "magic_resistance_2e": {
            "percent": MR[n], "applied": False, "note": NOTA_MR,
        },
        "world_data_2e": {
            "frequency": a["frequency"], "no_appearing": a["no_appearing"],
            "organization": a["organization"],
            "activity_cycle": a["activity"], "diet": a["diet"],
            "destinazione": "generatore_incontri",
        },
        "note": [],
    }

    return {
        "id": f"draconico-{n.lower()}",
        "name": {"en": f"{n} Draconian", "it": f"Draconico {n}",
                 "variante_di": "Draconians"},
        "ruolo": ruolo,
        "ruolo_note": ruolo_note,
        "ruolo_2e": ruolo_2e,
        "source": {
            "source_edition": "2e", "source_book": LIBRO_2E,
            "pages_pdf": [PAGINE_2E[n]], "pages_printed": [],
            "verified_on_image": False,
        },
        "valid_eras": None,
        "source_2e": s2e,
        "mechanics_5e": m5e,
    }


def copertura(doc, schema):
    """Quali proprieta' dello schema restano vuote."""
    vuoti = []

    def scendi(obj, spec, path=""):
        props = spec.get("properties", {})
        for k, sub in props.items():
            v = obj.get(k) if isinstance(obj, dict) else None
            p = f"{path}.{k}" if path else k
            if v in (None, [], {}, ""):
                vuoti.append(p)
            elif isinstance(v, dict) and "properties" in sub:
                scendi(v, sub, p)

    scendi(doc, schema)
    return vuoti


def main():
    schema = json.load(open(SCHEMA, encoding="utf-8"))
    val = jsonschema.Draft7Validator(schema)
    errori = 0
    tutti_vuoti = {}

    for n in D.ORDINE_5E:
        doc = costruisci(n)
        errs = sorted(val.iter_errors(doc), key=lambda e: list(e.path))
        if errs:
            errori += len(errs)
            print(f"✗ {n}")
            for e in errs[:6]:
                print(f"    {'/'.join(str(x) for x in e.path) or '(radice)'}: "
                      f"{e.message[:150]}")
        else:
            b = doc["mechanics_5e"]
            print(f"✓ {n:6} GS {b['challenge_rating']['value']:>3} | "
                  f"CA {b['armor_class']['value']} | "
                  f"{b['hit_points']['average']} PF | "
                  f"ruolo {doc['ruolo']:11} | "
                  f"tratti {len(b['traits'])} azioni {len(b['actions'])} "
                  f"reazioni {len(b['reactions'])}")
        tutti_vuoti[n] = copertura(doc, schema)

    print()
    comuni = set.intersection(*(set(v) for v in tutti_vuoti.values()))
    print(f"Campi vuoti su TUTTI e cinque ({len(comuni)}):")
    for c in sorted(comuni):
        print(f"    {c}")
    print()
    print("Verifiche della decisione 27:")
    d = costruisci("Baaz")
    b = d["mechanics_5e"]
    print(f"    gruppo A -> {b['world_data_2e']['destinazione']} "
          f"({len([k for k in b['world_data_2e'] if k != 'destinazione'])} campi)")
    print(f"    gruppo B -> {b['morale_2e']['destinazione']} "
          f"(valore {b['morale_2e']['value']}, etichetta \"{b['morale_2e']['label']}\")")
    print(f"    gruppo C -> applicata: {b['magic_resistance_2e']['applied']} "
          f"(valore conservato: {b['magic_resistance_2e']['percent']}%)")
    print(f"    i 21 campi 2e presenti: {len(d['source_2e']) - 5}/21 "
          f"piu' 5 campi nostri di servizio")

    print()
    if errori:
        print(f"{errori} errori di schema.")
        return 1
    print(f"{len(D.ORDINE_5E)}/5 draconici conformi allo schema, 0 errori.")
    print("NESSUN file scritto in dati/mostri/: questo e' un test dello schema, "
          "non una conversione.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
