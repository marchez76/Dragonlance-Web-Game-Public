#!/usr/bin/env python3
"""
SRD 5.1 (CC-BY 4.0) — mostri, sottoinsieme per gradi di sfida 1/2, 2, 3, 4 e 6.

PERCHE' SOLO QUESTI GRADI
    Sono i cinque GS dei draconici ufficiali di Shadow of the Dragon Queen:
    Baaz 1/2, Bozak 2, Kapak 3, Sivak 4, Aurak 6. Servono a calibrare la
    conversione per analogia (parte 4 di RAPPORTO-bestiario.md).

FONTE
    api.open5e.com, endpoint /v1/monsters/, document__slug = wotc-srd.
    Campi: nome, taglia, tipo, CA, PF, velocita', GS. Trascritti verbatim.
    L'SRD completo ha 322 voci; qui ce ne sono quelle dei cinque GS.
"""

# (nome, taglia, tipo, CA, PF, velocita', GS)
MOSTRI = [
    # ---- GS 1/2 ----
    ("Ape", "Medium", "Beast", 12, 19, "30, climb 30", "1/2"),
    ("Black Bear", "Medium", "Beast", 11, 19, "40, climb 30", "1/2"),
    ("Cockatrice", "Small", "Monstrosity", 11, 27, "20, fly 40", "1/2"),
    ("Crocodile", "Large", "Beast", 12, 19, "20, swim 20", "1/2"),
    ("Darkmantle", "Small", "Monstrosity", 11, 22, "10, fly 30", "1/2"),
    ("Deep Gnome (Svirfneblin)", "Small", "Humanoid", 15, 16, "20", "1/2"),
    ("Dust Mephit", "Small", "Elemental", 12, 17, "30, fly 30", "1/2"),
    ("Giant Goat", "Large", "Beast", 11, 19, "40", "1/2"),
    ("Giant Sea Horse", "Large", "Beast", 13, 16, "swim 40", "1/2"),
    ("Giant Wasp", "Medium", "Beast", 12, 13, "10, fly 50", "1/2"),
    ("Gnoll", "Medium", "Humanoid", 15, 22, "30", "1/2"),
    ("Gray Ooze", "Medium", "Ooze", 8, 22, "10, climb 10", "1/2"),
    ("Hobgoblin", "Medium", "Humanoid", 18, 11, "30", "1/2"),
    ("Ice Mephit", "Small", "Elemental", 11, 21, "30, fly 30", "1/2"),
    ("Lizardfolk", "Medium", "Humanoid", 15, 22, "30, swim 30", "1/2"),
    ("Magma Mephit", "Small", "Elemental", 11, 22, "30, fly 30", "1/2"),
    ("Magmin", "Small", "Elemental", 14, 9, "30", "1/2"),
    ("Orc", "Medium", "Humanoid", 13, 15, "30", "1/2"),
    ("Reef Shark", "Medium", "Beast", 12, 22, "swim 40", "1/2"),
    ("Rust Monster", "Medium", "Monstrosity", 14, 27, "40", "1/2"),
    ("Sahuagin", "Medium", "Humanoid", 12, 22, "30, swim 40", "1/2"),
    ("Satyr", "Medium", "Fey", 14, 31, "40", "1/2"),
    ("Scout", "Medium", "Humanoid", 13, 16, "30", "1/2"),
    ("Shadow", "Medium", "Undead", 12, 16, "40", "1/2"),
    ("Thug", "Medium", "Humanoid", 11, 32, "30", "1/2"),
    ("Warhorse", "Large", "Beast", 11, 19, "60", "1/2"),
    ("Warhorse Skeleton", "Large", "Undead", 13, 22, "60", "1/2"),
    ("Worg", "Large", "Monstrosity", 13, 26, "50", "1/2"),

    # ---- GS 2 ----
    ("Ankheg", "Large", "Monstrosity", 14, 39, "30, burrow 10", "2"),
    ("Awakened Tree", "Huge", "Plant", 13, 59, "20", "2"),
    ("Azer", "Medium", "Elemental", 17, 39, "30", "2"),
    ("Bandit Captain", "Medium", "Humanoid", 15, 65, "30", "2"),
    ("Berserker", "Medium", "Humanoid", 13, 67, "30", "2"),
    ("Black Dragon Wyrmling", "Medium", "Dragon", 17, 33, "30, fly 60, swim 30", "2"),
    ("Bronze Dragon Wyrmling", "Medium", "Dragon", 17, 32, "30, fly 60, swim 30", "2"),
    ("Centaur", "Large", "Monstrosity", 12, 45, "50", "2"),
    ("Cult Fanatic", "Medium", "Humanoid", 13, 22, "30", "2"),
    ("Druid", "Medium", "Humanoid", 11, 27, "30", "2"),
    ("Ettercap", "Medium", "Monstrosity", 13, 44, "30, climb 30", "2"),
    ("Gargoyle", "Medium", "Elemental", 15, 52, "30, fly 60", "2"),
    ("Gelatinous Cube", "Large", "Ooze", 6, 84, "15", "2"),
    ("Ghast", "Medium", "Undead", 13, 36, "30", "2"),
    ("Giant Boar", "Large", "Beast", 12, 42, "40", "2"),
    ("Giant Constrictor Snake", "Huge", "Beast", 12, 60, "30, swim 30", "2"),
    ("Giant Elk", "Huge", "Beast", 15, 42, "60", "2"),
    ("Gibbering Mouther", "Medium", "Aberration", 9, 67, "10, swim 10", "2"),
    ("Green Dragon Wyrmling", "Medium", "Dragon", 17, 38, "30, fly 60, swim 30", "2"),
    ("Grick", "Medium", "Monstrosity", 14, 27, "30, climb 30", "2"),
    ("Griffon", "Large", "Monstrosity", 12, 59, "30, fly 80", "2"),
    ("Hunter Shark", "Large", "Beast", 12, 45, "swim 40", "2"),
    ("Merrow", "Large", "Monstrosity", 13, 45, "10, swim 40", "2"),
    ("Mimic", "Medium", "Monstrosity", 12, 58, "15", "2"),
    ("Minotaur Skeleton", "Large", "Undead", 12, 67, "40", "2"),
    ("Ochre Jelly", "Large", "Ooze", 8, 45, "10, climb 10", "2"),
    ("Ogre", "Large", "Giant", 11, 59, "40", "2"),
    ("Ogre Zombie", "Large", "Undead", 8, 85, "30", "2"),
    ("Pegasus", "Large", "Celestial", 12, 59, "60, fly 90", "2"),
    ("Plesiosaurus", "Large", "Beast", 13, 68, "20, swim 40", "2"),
    ("Polar Bear", "Large", "Beast", 12, 42, "40, swim 30", "2"),
    ("Priest", "Medium", "Humanoid", 13, 27, "25", "2"),
    ("Rhinoceros", "Large", "Beast", 11, 45, "40", "2"),
    ("Rug of Smothering", "Large", "Construct", 12, 33, "10", "2"),
    ("Saber-Toothed Tiger", "Large", "Beast", 12, 52, "40", "2"),
    ("Sea Hag", "Medium", "Fey", 14, 52, "30, swim 40", "2"),
    ("Silver Dragon Wyrmling", "Medium", "Dragon", 17, 45, "30, fly 60", "2"),
    ("Swarm of Poisonous Snakes", "Medium", "Beast", 14, 36, "30, swim 30", "2"),
    ("Wererat", "Medium", "Humanoid", 12, 33, "30", "2"),
    ("White Dragon Wyrmling", "Medium", "Dragon", 16, 32, "30, burrow 15, fly 60, swim 30", "2"),
    ("Will-o'-Wisp", "Tiny", "Undead", 19, 22, "fly 50 (hover)", "2"),

    # ---- GS 3 ----
    ("Basilisk", "Medium", "Monstrosity", 12, 52, "20", "3"),
    ("Bearded Devil", "Medium", "Fiend", 13, 52, "30", "3"),
    ("Blue Dragon Wyrmling", "Medium", "Dragon", 17, 52, "30, burrow 15, fly 60", "3"),
    ("Doppelganger", "Medium", "Monstrosity", 14, 52, "30", "3"),
    ("Giant Scorpion", "Large", "Beast", 15, 52, "40", "3"),
    ("Gold Dragon Wyrmling", "Medium", "Dragon", 17, 60, "30, fly 60, swim 30", "3"),
    ("Green Hag", "Medium", "Fey", 17, 82, "30", "3"),
    ("Hell Hound", "Medium", "Fiend", 15, 45, "50", "3"),
    ("Killer Whale", "Huge", "Beast", 12, 90, "swim 60", "3"),
    ("Knight", "Medium", "Humanoid", 18, 52, "30", "3"),
    ("Manticore", "Large", "Monstrosity", 14, 68, "30, fly 50", "3"),
    ("Minotaur", "Large", "Monstrosity", 14, 76, "40", "3"),
    ("Mummy", "Medium", "Undead", 11, 58, "20", "3"),
    ("Nightmare", "Large", "Fiend", 13, 68, "60, fly 90", "3"),
    ("Owlbear", "Large", "Monstrosity", 13, 59, "40", "3"),
    ("Phase Spider", "Large", "Monstrosity", 13, 32, "30, climb 30", "3"),
    ("Veteran", "Medium", "Humanoid", 17, 58, "30", "3"),
    ("Werewolf", "Medium", "Humanoid", 11, 58, "30", "3"),
    ("Wight", "Medium", "Undead", 14, 45, "30", "3"),
    ("Winter Wolf", "Large", "Monstrosity", 13, 75, "50", "3"),

    # ---- GS 4 ----
    ("Black Pudding", "Large", "Ooze", 7, 85, "20, climb 20", "4"),
    ("Chuul", "Large", "Aberration", 16, 93, "30, swim 30", "4"),
    ("Couatl", "Medium", "Celestial", 19, 97, "30, fly 90", "4"),
    ("Elephant", "Huge", "Beast", 12, 76, "40", "4"),
    ("Ettin", "Large", "Giant", 12, 85, "40", "4"),
    ("Ghost", "Medium", "Undead", 11, 45, "fly 40 (hover)", "4"),
    ("Lamia", "Large", "Monstrosity", 13, 97, "30", "4"),
    ("Red Dragon Wyrmling", "Medium", "Dragon", 17, 75, "30, climb 30, fly 60", "4"),
    ("Succubus/Incubus", "Medium", "Fiend", 15, 66, "30, fly 60", "4"),
    ("Wereboar", "Medium", "Humanoid", 10, 78, "30", "4"),
    ("Weretiger", "Medium", "Humanoid", 12, 120, "30", "4"),

    # ---- GS 6 ----
    ("Chimera", "Large", "Monstrosity", 14, 114, "30, fly 60", "6"),
    ("Drider", "Large", "Monstrosity", 19, 123, "30, climb 30", "6"),
    ("Invisible Stalker", "Medium", "Elemental", 14, 104, "50, fly 50 (hover)", "6"),
    ("Mage", "Medium", "Humanoid", 12, 40, "30", "6"),
    ("Mammoth", "Huge", "Beast", 13, 126, "40", "6"),
    ("Medusa", "Medium", "Monstrosity", 15, 127, "30", "6"),
    ("Vrock", "Large", "Fiend", 15, 104, "40, fly 60", "6"),
    ("Wyvern", "Large", "Dragon", 13, 110, "20, fly 80", "6"),
    ("Young Brass Dragon", "Large", "Dragon", 17, 110, "40, burrow 20, fly 80", "6"),
    ("Young White Dragon", "Large", "Dragon", 17, 133, "40, burrow 20, fly 80, swim 40", "6"),
]

# L'SRD completo, per i conteggi di contesto.
TOTALE_SRD = 322


def per_gs(gs):
    return [m for m in MOSTRI if m[6] == gs]


def statistiche(gs):
    """CA e PF mediani del grado di sfida: il metro per calibrare."""
    v = per_gs(gs)
    if not v:
        return None
    ca = sorted(m[3] for m in v)
    pf = sorted(m[4] for m in v)
    n = len(v)
    return {
        "n": n,
        "ca_min": ca[0], "ca_med": ca[n // 2], "ca_max": ca[-1],
        "pf_min": pf[0], "pf_med": pf[n // 2], "pf_max": pf[-1],
    }
