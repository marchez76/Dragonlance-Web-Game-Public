#!/usr/bin/env python3
"""
SRD 5.1 (CC-BY 4.0) — bestiario completo, tutti i gradi di sfida.

PERCHE' L'INTERO BESTIARIO
    Il modulo nasceva limitato ai cinque gradi di sfida dei draconici
    ufficiali di Shadow of the Dragon Queen (Baaz 1/2, Bozak 2, Kapak 3,
    Sivak 4, Aurak 6). Serviva a calibrare quella sola conversione.

    La Fase 2 deve pero' calibrare la conversione per analogia di 48
    creature dell'MC Appendix, non piu' cinque: il campione di GS che
    servira' non e' ancora noto (dipende da statistiche che quelle 48
    creature non hanno finche' non sono convertite), quindi il sottoinsieme
    va completato all'intero bestiario invece di indovinare quali gradi
    aggiungere in anticipo.

FONTE
    api.open5e.com, endpoint /v1/monsters/, document__slug = wotc-srd.
    Campi: nome, taglia, tipo, CA, PF, velocita', GS. Trascritti verbatim.
    L'intero bestiario ha 322 voci: sono tutte qui.
"""

# (nome, taglia, tipo, CA, PF, velocita', GS)
MOSTRI = [
    # ---- GS 0 ----
    ("Awakened Shrub", "Small", "Plant", 9, 10, "20", "0"),
    ("Baboon", "Small", "Beast", 12, 3, "30, climb 30", "0"),
    ("Badger", "Tiny", "Beast", 10, 3, "20, burrow 5", "0"),
    ("Bat", "Tiny", "Beast", 12, 1, "5, fly 30", "0"),
    ("Cat", "Tiny", "Beast", 12, 2, "40, climb 30", "0"),
    ("Commoner", "Medium", "Humanoid", 10, 4, "30", "0"),
    ("Crab", "Tiny", "Beast", 11, 2, "20, swim 20", "0"),
    ("Deer", "Medium", "Beast", 13, 4, "50", "0"),
    ("Eagle", "Small", "Beast", 12, 3, "10, fly 60", "0"),
    ("Frog", "Tiny", "Beast", 11, 1, "20, swim 20", "0"),
    ("Giant Fire Beetle", "Small", "Beast", 13, 4, "30", "0"),
    ("Goat", "Medium", "Beast", 10, 4, "40", "0"),
    ("Hawk", "Tiny", "Beast", 13, 1, "10, fly 60", "0"),
    ("Homunculus", "Tiny", "Construct", 13, 5, "20, fly 40", "0"),
    ("Hyena", "Medium", "Beast", 11, 5, "50", "0"),
    ("Jackal", "Small", "Beast", 12, 3, "40", "0"),
    ("Lemure", "Medium", "Fiend", 7, 13, "15", "0"),
    ("Lizard", "Tiny", "Beast", 10, 2, "20, climb 20", "0"),
    ("Octopus", "Small", "Beast", 12, 3, "5, swim 30", "0"),
    ("Owl", "Tiny", "Beast", 11, 1, "5, fly 60", "0"),
    ("Quipper", "Tiny", "Beast", 13, 1, "swim 40", "0"),
    ("Rat", "Tiny", "Beast", 10, 1, "20", "0"),
    ("Raven", "Tiny", "Beast", 12, 1, "10, fly 50", "0"),
    ("Scorpion", "Tiny", "Beast", 11, 1, "10", "0"),
    ("Sea Horse", "Tiny", "Beast", 11, 1, "swim 20", "0"),
    ("Shrieker", "Medium", "Plant", 5, 13, "0", "0"),
    ("Spider", "Tiny", "Beast", 12, 1, "20, climb 20", "0"),
    ("Vulture", "Medium", "Beast", 10, 5, "10, fly 50", "0"),
    ("Weasel", "Tiny", "Beast", 13, 1, "30", "0"),

    # ---- GS 1/8 ----
    ("Bandit", "Medium", "Humanoid", 12, 11, "30", "1/8"),
    ("Blood Hawk", "Small", "Beast", 12, 7, "10, fly 60", "1/8"),
    ("Camel", "Large", "Beast", 9, 15, "50", "1/8"),
    ("Cultist", "Medium", "Humanoid", 12, 9, "30", "1/8"),
    ("Flying Snake", "Tiny", "Beast", 14, 5, "30, fly 60, swim 30", "1/8"),
    ("Giant Crab", "Medium", "Beast", 15, 13, "30, swim 30", "1/8"),
    ("Giant Rat", "Small", "Beast", 12, 7, "30", "1/8"),
    ("Giant Rat (Diseased)", "Small", "Beast", 12, 7, "30", "1/8"),
    ("Giant Weasel", "Medium", "Beast", 13, 9, "40", "1/8"),
    ("Guard", "Medium", "Humanoid", 16, 11, "30", "1/8"),
    ("Kobold", "Small", "Humanoid", 12, 5, "30", "1/8"),
    ("Mastiff", "Medium", "Beast", 12, 5, "40", "1/8"),
    ("Merfolk", "Medium", "Humanoid", 11, 11, "10, swim 40", "1/8"),
    ("Mule", "Medium", "Beast", 10, 11, "40", "1/8"),
    ("Noble", "Medium", "Humanoid", 15, 9, "30", "1/8"),
    ("Poisonous Snake", "Tiny", "Beast", 13, 2, "30, swim 30", "1/8"),
    ("Pony", "Medium", "Beast", 10, 11, "40", "1/8"),
    ("Stirge", "Tiny", "Beast", 14, 2, "10, fly 40", "1/8"),
    ("Tribal Warrior", "Medium", "Humanoid", 12, 11, "30", "1/8"),

    # ---- GS 1/4 ----
    ("Acolyte", "Medium", "Humanoid", 10, 9, "30", "1/4"),
    ("Axe Beak", "Large", "Beast", 11, 19, "50", "1/4"),
    ("Blink Dog", "Medium", "Fey", 13, 22, "40", "1/4"),
    ("Boar", "Medium", "Beast", 11, 11, "40", "1/4"),
    ("Constrictor Snake", "Large", "Beast", 12, 13, "30, swim 30", "1/4"),
    ("Draft Horse", "Large", "Beast", 10, 19, "40", "1/4"),
    ("Dretch", "Small", "Fiend", 11, 18, "20", "1/4"),
    ("Drow", "Medium", "Humanoid", 15, 13, "30", "1/4"),
    ("Elk", "Large", "Beast", 10, 13, "50", "1/4"),
    ("Flying Sword", "Small", "Construct", 17, 17, "fly 50 (hover)", "1/4"),
    ("Giant Badger", "Medium", "Beast", 10, 13, "30, burrow 10", "1/4"),
    ("Giant Bat", "Large", "Beast", 13, 22, "10, fly 60", "1/4"),
    ("Giant Centipede", "Small", "Beast", 13, 4, "30, climb 30", "1/4"),
    ("Giant Frog", "Medium", "Beast", 11, 18, "30, swim 30", "1/4"),
    ("Giant Lizard", "Large", "Beast", 12, 19, "30, climb 30", "1/4"),
    ("Giant Owl", "Large", "Beast", 12, 19, "5, fly 60", "1/4"),
    ("Giant Poisonous Snake", "Medium", "Beast", 14, 11, "30, swim 30", "1/4"),
    ("Giant Wolf Spider", "Medium", "Beast", 13, 11, "40, climb 40", "1/4"),
    ("Goblin", "Small", "Humanoid", 15, 7, "30", "1/4"),
    ("Grimlock", "Medium", "Humanoid", 11, 11, "30", "1/4"),
    ("Panther", "Medium", "Beast", 12, 13, "50, climb 40", "1/4"),
    ("Pseudodragon", "Tiny", "Dragon", 13, 7, "15, fly 60", "1/4"),
    ("Riding Horse", "Large", "Beast", 10, 13, "60", "1/4"),
    ("Skeleton", "Medium", "Undead", 13, 13, "30", "1/4"),
    ("Sprite", "Tiny", "Fey", 15, 2, "10, fly 40", "1/4"),
    ("Steam Mephit", "Small", "Elemental", 10, 21, "30, fly 30", "1/4"),
    ("Swarm of Bats", "Medium", "Beast", 12, 22, "fly 30", "1/4"),
    ("Swarm of Rats", "Medium", "Beast", 10, 24, "30", "1/4"),
    ("Swarm of Ravens", "Medium", "Beast", 12, 24, "10, fly 50", "1/4"),
    ("Violet Fungus", "Medium", "Plant", 5, 18, "5", "1/4"),
    ("Wolf", "Medium", "Beast", 13, 11, "40", "1/4"),
    ("Zombie", "Medium", "Undead", 8, 22, "20", "1/4"),

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
    ("Swarm of Beetles", "Medium", "Beast", 12, 22, "20, burrow 5, climb 20", "1/2"),
    ("Swarm of Centipedes", "Medium", "Beast", 12, 22, "20, climb 20", "1/2"),
    ("Swarm of Insects", "Medium", "Beast", 12, 22, "20, climb 20", "1/2"),
    ("Swarm of Spiders", "Medium", "Beast", 12, 22, "20, climb 20", "1/2"),
    ("Swarm of Wasps", "Medium", "Beast", 12, 22, "5, fly 30", "1/2"),
    ("Thug", "Medium", "Humanoid", 11, 32, "30", "1/2"),
    ("Warhorse", "Large", "Beast", 11, 19, "60", "1/2"),
    ("Warhorse Skeleton", "Large", "Undead", 13, 22, "60", "1/2"),
    ("Worg", "Large", "Monstrosity", 13, 26, "50", "1/2"),

    # ---- GS 1 ----
    ("Animated Armor", "Medium", "Construct", 18, 33, "25", "1"),
    ("Brass Dragon Wyrmling", "Medium", "Dragon", 16, 16, "30, burrow 15, fly 60", "1"),
    ("Brown Bear", "Large", "Beast", 11, 34, "40, climb 30", "1"),
    ("Bugbear", "Medium", "Humanoid", 16, 27, "30", "1"),
    ("Copper Dragon Wyrmling", "Medium", "Dragon", 16, 22, "30, climb 30, fly 60", "1"),
    ("Death Dog", "Medium", "Monstrosity", 12, 39, "40", "1"),
    ("Dire Wolf", "Large", "Beast", 14, 37, "50", "1"),
    ("Dryad", "Medium", "Fey", 11, 22, "30", "1"),
    ("Duergar", "Medium", "Humanoid", 16, 26, "25", "1"),
    ("Ghoul", "Medium", "Undead", 12, 22, "30", "1"),
    ("Giant Eagle", "Large", "Beast", 13, 26, "10, fly 80", "1"),
    ("Giant Hyena", "Large", "Beast", 12, 45, "50", "1"),
    ("Giant Octopus", "Large", "Beast", 11, 52, "10, swim 60", "1"),
    ("Giant Spider", "Large", "Beast", 14, 26, "30, climb 30", "1"),
    ("Giant Toad", "Large", "Beast", 11, 39, "20, swim 40", "1"),
    ("Giant Vulture", "Large", "Beast", 10, 22, "10, fly 60", "1"),
    ("Harpy", "Medium", "Monstrosity", 11, 38, "20, fly 40", "1"),
    ("Hippogriff", "Large", "Monstrosity", 11, 19, "40, fly 60", "1"),
    ("Imp", "Tiny", "Fiend", 13, 10, "20, fly 40", "1"),
    ("Lion", "Large", "Beast", 12, 26, "50", "1"),
    ("Quasit", "Tiny", "Fiend", 13, 7, "40", "1"),
    ("Specter", "Medium", "Undead", 12, 22, "fly 50 (hover)", "1"),
    ("Spy", "Medium", "Humanoid", 12, 27, "30", "1"),
    ("Swarm of Quippers", "Medium", "Beast", 13, 28, "swim 40", "1"),
    ("Tiger", "Large", "Beast", 12, 37, "40", "1"),

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
    ("Werewolf", "Medium", "Humanoid", 11, 58, "30 (40 ft. in wolf form)", "3"),
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
    ("Wereboar", "Medium", "Humanoid", 10, 78, "30 (40 ft. in boar form)", "4"),
    ("Weretiger", "Medium", "Humanoid", 12, 120, "30 (40 ft. in tiger form)", "4"),

    # ---- GS 5 ----
    ("Air Elemental", "Large", "Elemental", 15, 90, "fly 90 (hover)", "5"),
    ("Barbed Devil", "Medium", "Fiend", 15, 110, "30", "5"),
    ("Bulette", "Large", "Monstrosity", 17, 94, "40, burrow 40", "5"),
    ("Earth Elemental", "Large", "Elemental", 17, 126, "30, burrow 30", "5"),
    ("Fire Elemental", "Large", "Elemental", 13, 102, "50", "5"),
    ("Flesh Golem", "Medium", "Construct", 9, 93, "30", "5"),
    ("Giant Crocodile", "Huge", "Beast", 14, 85, "30, swim 50", "5"),
    ("Giant Shark", "Huge", "Beast", 13, 126, "swim 50", "5"),
    ("Gladiator", "Medium", "Humanoid", 16, 112, "30", "5"),
    ("Gorgon", "Large", "Monstrosity", 19, 114, "40", "5"),
    ("Half-Red Dragon Veteran", "Medium", "Humanoid", 18, 65, "30", "5"),
    ("Hill Giant", "Huge", "Giant", 13, 105, "40", "5"),
    ("Night Hag", "Medium", "Fiend", 17, 112, "30", "5"),
    ("Otyugh", "Large", "Aberration", 14, 114, "30", "5"),
    ("Roper", "Large", "Monstrosity", 20, 93, "10, climb 10", "5"),
    ("Salamander", "Large", "Elemental", 15, 90, "30", "5"),
    ("Shambling Mound", "Large", "Plant", 15, 136, "20, swim 20", "5"),
    ("Triceratops", "Huge", "Beast", 13, 95, "50", "5"),
    ("Troll", "Large", "Giant", 15, 84, "30", "5"),
    ("Unicorn", "Large", "Celestial", 12, 67, "50", "5"),
    ("Vampire Spawn", "Medium", "Undead", 15, 82, "30", "5"),
    ("Water Elemental", "Large", "Elemental", 14, 114, "30, swim 90", "5"),
    ("Werebear", "Medium", "Humanoid", 10, 135, "30 (40 ft., climb 30 ft. in bear or hybrid form)", "5"),
    ("Wraith", "Medium", "Undead", 13, 67, "fly 60 (hover)", "5"),
    ("Xorn", "Medium", "Elemental", 19, 73, "20, burrow 20", "5"),

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

    # ---- GS 7 ----
    ("Giant Ape", "Huge", "Beast", 12, 157, "40, climb 40", "7"),
    ("Oni", "Large", "Giant", 16, 110, "30, fly 30", "7"),
    ("Shield Guardian", "Large", "Construct", 17, 142, "30", "7"),
    ("Stone Giant", "Huge", "Giant", 17, 126, "40", "7"),
    ("Young Black Dragon", "Large", "Dragon", 18, 127, "40, fly 80, swim 40", "7"),
    ("Young Copper Dragon", "Large", "Dragon", 17, 119, "40, climb 40, fly 80", "7"),

    # ---- GS 8 ----
    ("Assassin", "Medium", "Humanoid", 15, 78, "30", "8"),
    ("Cloaker", "Large", "Aberration", 14, 78, "10, fly 40", "8"),
    ("Frost Giant", "Huge", "Giant", 15, 138, "40", "8"),
    ("Hezrou", "Large", "Fiend", 16, 136, "30", "8"),
    ("Hydra", "Huge", "Monstrosity", 15, 172, "30, swim 30", "8"),
    ("Spirit Naga", "Large", "Monstrosity", 15, 75, "40", "8"),
    ("Tyrannosaurus Rex", "Huge", "Beast", 13, 136, "50", "8"),
    ("Young Bronze Dragon", "Large", "Dragon", 18, 142, "40, fly 80, swim 40", "8"),
    ("Young Green Dragon", "Large", "Dragon", 18, 136, "40, fly 80, swim 40", "8"),

    # ---- GS 9 ----
    ("Bone Devil", "Large", "Fiend", 19, 142, "40, fly 40", "9"),
    ("Clay Golem", "Large", "Construct", 14, 133, "20", "9"),
    ("Cloud Giant", "Huge", "Giant", 14, 200, "40", "9"),
    ("Fire Giant", "Huge", "Giant", 18, 162, "30", "9"),
    ("Glabrezu", "Large", "Fiend", 17, 157, "40", "9"),
    ("Treant", "Huge", "Plant", 16, 138, "30", "9"),
    ("Young Blue Dragon", "Large", "Dragon", 18, 152, "40, burrow 40, fly 80", "9"),
    ("Young Silver Dragon", "Large", "Dragon", 18, 168, "40, fly 80", "9"),

    # ---- GS 10 ----
    ("Aboleth", "Large", "Aberration", 17, 135, "10, swim 40", "10"),
    ("Deva", "Medium", "Celestial", 17, 136, "30, fly 90", "10"),
    ("Guardian Naga", "Large", "Monstrosity", 18, 127, "40", "10"),
    ("Stone Golem", "Large", "Construct", 17, 178, "30", "10"),
    ("Young Gold Dragon", "Large", "Dragon", 18, 178, "40, fly 80, swim 40", "10"),
    ("Young Red Dragon", "Large", "Dragon", 18, 178, "40, climb 40, fly 80", "10"),

    # ---- GS 11 ----
    ("Behir", "Huge", "Monstrosity", 17, 168, "50, climb 40", "11"),
    ("Chain Devil", "Medium", "Fiend", 16, 85, "30", "11"),
    ("Djinni", "Large", "Elemental", 17, 161, "30, fly 90", "11"),
    ("Efreeti", "Large", "Elemental", 17, 200, "40, fly 60", "11"),
    ("Gynosphinx", "Large", "Monstrosity", 17, 136, "40, fly 60", "11"),
    ("Horned Devil", "Large", "Fiend", 18, 178, "20, fly 60", "11"),
    ("Remorhaz", "Huge", "Monstrosity", 17, 195, "30, burrow 20", "11"),
    ("Roc", "Gargantuan", "Monstrosity", 15, 248, "20, fly 120", "11"),

    # ---- GS 12 ----
    ("Archmage", "Medium", "Humanoid", 12, 99, "30", "12"),
    ("Erinyes", "Medium", "Fiend", 18, 153, "30, fly 60", "12"),

    # ---- GS 13 ----
    ("Adult Brass Dragon", "Huge", "Dragon", 18, 172, "40, burrow 40, fly 80", "13"),
    ("Adult White Dragon", "Huge", "Dragon", 18, 200, "40, burrow 30, fly 80, swim 40", "13"),
    ("Nalfeshnee", "Large", "Fiend", 18, 184, "20, fly 30", "13"),
    ("Rakshasa", "Medium", "Fiend", 16, 110, "40", "13"),
    ("Storm Giant", "Huge", "Giant", 16, 230, "50, swim 50", "13"),
    ("Vampire", "Medium", "Undead", 16, 144, "30", "13"),

    # ---- GS 14 ----
    ("Adult Black Dragon", "Huge", "Dragon", 19, 195, "40, fly 80, swim 40", "14"),
    ("Adult Copper Dragon", "Huge", "Dragon", 18, 184, "40, climb 40, fly 80", "14"),
    ("Ice Devil", "Large", "Fiend", 18, 180, "40", "14"),

    # ---- GS 15 ----
    ("Adult Bronze Dragon", "Huge", "Dragon", 19, 212, "40, fly 80, swim 40", "15"),
    ("Adult Green Dragon", "Huge", "Dragon", 19, 207, "40, fly 80, swim 40", "15"),
    ("Mummy Lord", "Medium", "Undead", 17, 97, "20", "15"),
    ("Purple Worm", "Gargantuan", "Monstrosity", 18, 247, "50, burrow 30", "15"),

    # ---- GS 16 ----
    ("Adult Blue Dragon", "Huge", "Dragon", 19, 225, "40, burrow 30, fly 80", "16"),
    ("Adult Silver Dragon", "Huge", "Dragon", 19, 243, "40, fly 80", "16"),
    ("Iron Golem", "Large", "Construct", 20, 210, "30", "16"),
    ("Marilith", "Large", "Fiend", 18, 189, "40", "16"),
    ("Planetar", "Large", "Celestial", 19, 200, "40, fly 120", "16"),

    # ---- GS 17 ----
    ("Adult Gold Dragon", "Huge", "Dragon", 19, 256, "40, fly 80, swim 40", "17"),
    ("Adult Red Dragon", "Huge", "Dragon", 19, 256, "40, climb 40, fly 80", "17"),
    ("Androsphinx", "Large", "Monstrosity", 17, 199, "40, fly 60", "17"),
    ("Dragon Turtle", "Gargantuan", "Dragon", 20, 341, "20, swim 40", "17"),

    # ---- GS 19 ----
    ("Balor", "Huge", "Fiend", 19, 262, "40, fly 80", "19"),

    # ---- GS 20 ----
    ("Ancient Brass Dragon", "Gargantuan", "Dragon", 20, 297, "40, burrow 40, fly 80", "20"),
    ("Ancient White Dragon", "Gargantuan", "Dragon", 20, 333, "40, burrow 40, fly 80, swim 40", "20"),
    ("Pit Fiend", "Large", "Fiend", 19, 300, "30, fly 60", "20"),

    # ---- GS 21 ----
    ("Ancient Black Dragon", "Gargantuan", "Dragon", 22, 367, "40, fly 80, swim 40", "21"),
    ("Ancient Copper Dragon", "Gargantuan", "Dragon", 21, 350, "40, climb 40, fly 80", "21"),
    ("Lich", "Medium", "Undead", 17, 135, "30", "21"),
    ("Solar", "Large", "Celestial", 21, 243, "50, fly 150", "21"),

    # ---- GS 22 ----
    ("Ancient Bronze Dragon", "Gargantuan", "Dragon", 22, 444, "40, fly 80, swim 40", "22"),
    ("Ancient Green Dragon", "Gargantuan", "Dragon", 21, 385, "40, fly 80, swim 40", "22"),

    # ---- GS 23 ----
    ("Ancient Blue Dragon", "Gargantuan", "Dragon", 22, 481, "40, burrow 40, fly 80", "23"),
    ("Ancient Silver Dragon", "Gargantuan", "Dragon", 22, 487, "40, fly 80", "23"),
    ("Kraken", "Gargantuan", "Monstrosity", 18, 472, "20, swim 60", "23"),

    # ---- GS 24 ----
    ("Ancient Gold Dragon", "Gargantuan", "Dragon", 22, 546, "40, fly 80, swim 40", "24"),
    ("Ancient Red Dragon", "Gargantuan", "Dragon", 22, 546, "40, climb 40, fly 80", "24"),

    # ---- GS 30 ----
    ("Tarrasque", "Gargantuan", "Monstrosity", 25, 676, "40", "30"),
]

# L'SRD completo: coincide con len(MOSTRI), non piu' un sottoinsieme.
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
