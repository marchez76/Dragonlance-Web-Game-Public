#!/usr/bin/env python3
"""
SRD 5.1 (CC-BY 4.0) — tabelle di classe, trascritte verbatim.

PERCHE' STA QUI
    Il PHB 5e 2014 non e' fra i PDF, ma l'SRD 5.1 contiene le classi base con
    i privilegi livello per livello ed e' liberamente ridistribuibile. E' la
    fonte di formato del progetto: qualunque confronto con la 5e si fa su
    questo testo, non a memoria.

FONTE
    api.open5e.com, endpoint /v1/classes/<slug>/, campo `table`,
    document__slug = wotc-srd. Le stringhe sotto sono la colonna "Features"
    riga per riga, senza riscritture.

COSA NON C'E'
    Le sottoclassi (Martial Archetype, Arcane Tradition, Divine Domain)
    concedono privilegi propri ai livelli marcati. L'SRD ne include una per
    classe. Nei conteggi i privilegi di sottoclasse sono contati come UNA
    concessione per livello, non srotolati, perche' dipendono dalla
    sottoclasse scelta.
"""

# --------------------------------------------------------------------------
# Colonna "Features" dell'SRD, livello per livello. Stringa vuota = "-".
# --------------------------------------------------------------------------
TABELLE = {
    "Fighter": {
        "hit_dice": "1d10",
        "saves": "Strength, Constitution",
        "features": {
            1: "Fighting Style, Second Wind",
            2: "Action Surge (one use)",
            3: "Martial Archetype",
            4: "Ability Score Improvement",
            5: "Extra Attack",
            6: "Ability Score Improvement",
            7: "Martial Archetype Feature",
            8: "Ability Score Improvement",
            9: "Indomitable (one use)",
            10: "Martial Archetype Feature",
            11: "Extra Attack (2)",
            12: "Ability Score Improvement",
            13: "Indomitable (two uses)",
            14: "Ability Score Improvement",
            15: "Martial Archetype Feature",
            16: "Ability Score Improvement",
            17: "Action Surge (two uses), Indomitable (three uses)",
            18: "Martial Archetype Feature",
            19: "Ability Score Improvement",
            20: "Extra Attack (3)",
        },
    },
    "Wizard": {
        "hit_dice": "1d6",
        "saves": "Intelligence, Wisdom",
        "features": {
            1: "Spellcasting, Arcane Recovery",
            2: "Arcane Tradition",
            3: "", 4: "Ability Score Improvement", 5: "",
            6: "Arcane Tradition Feature",
            7: "", 8: "Ability Score Improvement", 9: "",
            10: "Arcane Tradition Feature",
            11: "", 12: "Ability Score Improvement", 13: "",
            14: "Arcane Tradition Feature",
            15: "", 16: "Ability Score Improvement", 17: "",
            18: "Spell Mastery",
            19: "Ability Score Improvement",
            20: "Signature Spell",
        },
    },
    "Cleric": {
        "hit_dice": "1d8",
        "saves": "Wisdom, Charisma",
        "features": {
            1: "Spellcasting, Divine Domain",
            2: "Channel Divinity (1/rest), Divine Domain Feature",
            3: "", 4: "Ability Score Improvement",
            5: "Destroy Undead (CR 1/2)",
            6: "Channel Divinity (2/rest), Divine Domain Feature",
            7: "",
            8: "Ability Score Improvement, Destroy Undead (CR 1), Divine Domain Feature",
            9: "",
            10: "Divine Intervention",
            11: "Destroy Undead (CR 2)",
            12: "Ability Score Improvement",
            13: "",
            14: "Destroy Undead (CR 3)",
            15: "", 16: "Ability Score Improvement",
            17: "Destroy Undead (CR 4), Divine Domain Feature",
            18: "Channel Divinity (3/rest)",
            19: "Ability Score Improvement",
            20: "Divine Intervention improvement",
        },
    },
    "Paladin": {
        "hit_dice": "1d10",
        "saves": "Wisdom, Charisma",
        "features": {
            1: "Divine Sense, Lay on Hands",
            2: "Fighting Style, Spellcasting, Divine Smite",
            3: "Divine Health, Sacred Oath",
            4: "Ability Score Improvement",
            5: "Extra Attack",
            6: "Aura of Protection",
            7: "Sacred Oath feature",
            8: "Ability Score Improvement",
            9: "",
            10: "Aura of Courage",
            11: "Improved Divine Smite",
            12: "Ability Score Improvement",
            13: "",
            14: "Cleansing Touch",
            15: "Sacred Oath feature",
            16: "Ability Score Improvement",
            17: "",
            18: "Aura improvements",
            19: "Ability Score Improvement",
            20: "Sacred Oath feature",
        },
    },
    "Rogue": {
        "hit_dice": "1d8",
        "saves": "Dexterity, Intelligence",
        "features": {
            1: "Expertise, Sneak Attack, Thieves' Cant",
            2: "Cunning Action",
            3: "Roguish Archetype",
            4: "Ability Score Improvement",
            5: "Uncanny Dodge",
            6: "Expertise",
            7: "Evasion",
            8: "Ability Score Improvement",
            9: "Roguish Archetype feature",
            10: "Ability Score Improvement",
            11: "Reliable Talent",
            12: "Ability Score Improvement",
            13: "Roguish Archetype Feature",
            14: "Blindsense",
            15: "Slippery Mind",
            16: "Ability Score Improvement",
            17: "Roguish Archetype Feature",
            18: "Elusive",
            19: "Ability Score Improvement",
            20: "Stroke of Luck",
        },
    },
}

# Bonus di competenza: identico per tutte le classi, SRD 5.1.
COMPETENZA = {l: 2 + (l - 1) // 4 for l in range(1, 21)}

ASI = "Ability Score Improvement"


def privilegi(classe):
    """Privilegi non-ASI, livello per livello. (livello, testo)"""
    f = TABELLE[classe]["features"]
    out = []
    for l in sorted(f):
        voci = [v.strip() for v in f[l].split(",") if v.strip()]
        voci = [v for v in voci if not v.startswith(ASI)]
        if voci:
            out.append((l, ", ".join(voci)))
    return out


def n_privilegi(classe):
    return sum(len(t.split(", ")) for _, t in privilegi(classe))


def n_asi(classe):
    return sum(1 for v in TABELLE[classe]["features"].values() if ASI in v)


def livelli_con_privilegi(classe):
    return len(privilegi(classe))
