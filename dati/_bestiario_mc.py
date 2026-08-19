#!/usr/bin/env python3
"""
Registro definitivo delle voci dell'MC Dragonlance Appendix.

PERCHE' ESISTE
    Il conteggio ricavato dal testo estratto era sbagliato per due motivi che
    si sommano:

    1. Alcune voci hanno lo statblock su PIU' COLONNE — una voce, piu'
       creature. L'estrattore a due colonne legge le intestazioni affiancate
       come una riga sola, e in tre casi ha perso del tutto le colonne di
       destra: `Avian` aveva quattro uccelli e ne restavano due, `Stag` tre
       cervi e ne restava uno, `Man (of Krynn)` quattro culture e ne
       restavano due.

    2. Otto voci avevano il NOME sbagliato, perche' l'estrattore prendeva le
       intestazioni di colonna al posto del titolo, oppure perche' il titolo
       era stampato con le lettere spaziate.

    Il testo estratto non basta a contare. Ogni voce marcata `verificata`
    qui sotto e' stata riletta sull'IMMAGINE della pagina.

CATEGORIE
    `razza_nostra`   scheda PNG di una razza giocante che abbiamo gia' in
                     dati/razze/. Non e' un mostro da convertire.
    `razza_altra`    scheda di razza o cultura non nel nostro roster
                     (clan nanici riservati ai PNG, ogre comuni).
    `creatura`       mostro vero, da convertire.
"""

# (pagina_pdf, nome_entrata, [creature], categoria, verificata_su_immagine, nota)
VOCI = [
    # ---- voci con statblock a PIU' COLONNE, tutte verificate su immagine ----
    (4, "Avian", ["Emre", "Kingfisher", "Skyfisher", "'Wari"], "creatura", True,
     "QUATTRO colonne. L'estrazione ne aveva salvate due e chiamava la voce "
     "\"Emre Kingfisher\". Skyfisher e 'Wari erano persi del tutto."),
    (20, "Dragon, Astral", ["Astral Dragon (unmated)", "Astral Dragon (mated pair)"],
     "creatura", True,
     "DUE colonne, ma sono la stessa specie in due stati: il drago astrale "
     "solitario e la coppia accoppiata, che il manuale tratta come una singola "
     "creatura da 35 DV. Due statblock, una specie. Il nome dell'entrata era "
     "andato perso: l'estrazione la chiamava \"Unmated Mated pair*\"."),
    (59, "Man (of Krynn)",
     ["Ice Folk", "Knights of Solamnia", "Plainsmen", "Rebels"],
     "razza_nostra", True,
     "QUATTRO colonne. Sono le culture umane di Krynn come PNG: corrispondono "
     "a `umano` in dati/razze/. L'estrazione ne aveva due e chiamava la voce "
     "\"Ice Folk Knights of\"."),
    (63, "Minotaur (of Krynn)", ["Blood Sea Minotaur"], "razza_nostra", True,
     "UNA colonna sola, ma il nome era sbagliato: l'estrazione prendeva "
     "l'intestazione di colonna \"Blood Sea Minotaur\" come titolo."),
    (71, "Shadowperson", ["Shadowperson", "Revered Ancient One"], "creatura", True,
     "DUE colonne: la creatura e il suo anziano, la cui colonna e' quasi tutta "
     "\"Nil\" perche' non combatte."),
    (78, "Stag", ["Wild Stag", "Giant Stag", "The White Stag"], "creatura", True,
     "TRE colonne. L'estrazione ne aveva una sola, con refuso: \"Wild Stage\". "
     "Il Cervo Bianco e' unico, di allineamento legale buono e da 2.000 PE: "
     "non e' una bestia ma una creatura sacra."),
    (79, "Tayling", ["Tayling", "Taylang"], "creatura", True,
     "DUE colonne: i gemelli telepatici, l'intelligente e il bestiale. "
     "L'estrazione leggeva \"Tayland\": sull'immagine e' Taylang."),
    (87, "Yaggol", ["Yaggol"], "creatura", True,
     "Colonna singola. Il titolo era stampato con le lettere spaziate e "
     "l'estrazione dava \"Y a g g o l\"."),

    # ---- voci a colonna singola, nome corretto nel testo estratto ----
    (3, "Anemone, Giant", ["Giant Anemone"], "creatura", False, None),
    (5, "Bear, Ice", ["Ice Bear"], "creatura", False, None),
    (9, "Disir", ["Disir"], "creatura", False, None),
    (10, "Draconian (proto-), Traag", ["Traag"], "creatura", False, None),
    (12, "Draconian, Aurak", ["Aurak Draconian"], "creatura", False, None),
    (13, "Draconian, Baaz", ["Baaz Draconian"], "creatura", False, None),
    (14, "Draconian, Bozak", ["Bozak Draconian"], "creatura", False, None),
    (15, "Draconian, Kapak", ["Kapak Draconian"], "creatura", False, None),
    (16, "Draconian, Sivak", ["Sivak Draconian"], "creatura", False, None),
    (19, "Dragon, Amphi", ["Amphi Dragon"], "creatura", False, None),
    (21, "Dragon, Kodragon", ["Kodragon"], "creatura", False, None),
    (23, "Dragon, Sea", ["Sea Dragon"], "creatura", False, None),
    (24, "Dreamshadow", ["Dreamshadow"], "creatura", False, None),
    (25, "Dreamwraith", ["Dreamwraith"], "creatura", False, None),
    (29, "Dwarf, Hill (Neidar)", ["Hill Dwarf"], "razza_nostra", False, None),
    (30, "Dwarf, Mountain (Hylar)", ["Mountain Dwarf"], "razza_nostra", False, None),
    (31, "Dwarf, Theiwar", ["Theiwar"], "razza_altra", False,
     "Clan nanico che Tales of the Lance riserva ai PNG: escluso dal roster."),
    (32, "Dwarf, Zakhar", ["Zakhar"], "razza_altra", False,
     "Come sopra."),
    (33, "Elf, High-Qualinesti", ["Qualinesti"], "razza_nostra", False, None),
    (34, "Elf, High-Silvanesti", ["Silvanesti"], "razza_nostra", False, None),
    (35, "Elf, Wild-Kagonesti", ["Kagonesti"], "razza_nostra", False, None),
    (36, "Elf, Half", ["Half-Elf"], "razza_nostra", False, None),
    (37, "Elf, Sea-Dargonesti", ["Dargonesti"], "razza_nostra", False, None),
    (38, "Elf, Sea-Dimernesti", ["Dimernesti"], "razza_nostra", False, None),
    (39, "Eyewing", ["Eyewing"], "creatura", False, None),
    (40, "Fetch", ["Fetch"], "creatura", False, None),
    (41, "Fire Minion", ["Fire Minion"], "creatura", False,
     "Falso positivo del rilevatore: verificata su immagine, colonna singola."),
    (42, "Fireshadow", ["Fireshadow"], "creatura", False, None),
    (43, "Gnome, Tinker (Minoi)", ["Tinker Gnome"], "razza_nostra", False, None),
    (45, "Gurik Cha-ahl", ["Gurik Cha-ahl"], "creatura", False, None),
    (47, "Haunt, Knight", ["Knight Haunt"], "creatura", False, None),
    (48, "Horax", ["Horax"], "creatura", False, None),
    (49, "Imp, Blood Sea", ["Blood Sea Imp"], "creatura", False, None),
    (51, "Kalothagh (Prickleback)", ["Kalothagh"], "creatura", False, None),
    (52, "Kani Doll", ["Kani Doll"], "creatura", False, None),
    (53, "Kender", ["Kender"], "razza_nostra", False, None),
    (55, "Knight, Death", ["Death Knight"], "creatura", False,
     "E' Lord Soth. SotDQ ne ha lo statblock come PERSONAGGIO, non come specie."),
    (56, "Kyrie", ["Kyrie"], "creatura", False, None),
    (65, "Ogre (of Krynn)", ["Ogre"], "razza_altra", False,
     "Ogre comune di Krynn, non gli Irda."),
    (67, "Ogre, High (Irda)", ["Irda"], "razza_nostra", False, None),
    (73, "Shimmerweed", ["Shimmerweed"], "creatura", False, None),
    (74, "Skrit", ["Skrit"], "creatura", False, None),
    (75, "Spectral Minion", ["Spectral Minion"], "creatura", False, None),
    (81, "Thanoi (Walrus Man)", ["Thanoi"], "creatura", False, None),
    (83, "Tylor", ["Tylor"], "creatura", False, None),
    (84, "Warrior, Skeleton", ["Skeleton Warrior"], "creatura", False, None),
    (85, "Wichtlin", ["Wichtlin"], "creatura", False, None),
    (86, "Wyndlass", ["Wyndlass"], "creatura", False, None),
    (88, "Yeti-kin, Saqualaminoi", ["Saqualaminoi"], "razza_altra", False,
     "Stirpe di yeti, non nel roster giocante."),
]

# Nomi che il testo estratto dava sbagliati, e il nome vero.
NOMI_CORRETTI = {
    "Emre Kingfisher": "Avian",
    "Unmated Mated pair*": "Dragon, Astral",
    "Ice Folk Knights of": "Man (of Krynn)",
    "Blood Sea Minotaur": "Minotaur (of Krynn)",
    "Shadowperson Revered Ancient One": "Shadowperson",
    "Wild Stage": "Stag",
    "Tayling Tayland": "Tayling",
    "Y a g g o l": "Yaggol",
}


def statistiche():
    voci = len(VOCI)
    creature = sum(len(c) for _, _, c, _, _, _ in VOCI)
    per_cat = {}
    for _, _, c, cat, _, _ in VOCI:
        per_cat.setdefault(cat, {"voci": 0, "creature": 0})
        per_cat[cat]["voci"] += 1
        per_cat[cat]["creature"] += len(c)
    multi = [(p, n, c, nota) for p, n, c, _, _, nota in VOCI if len(c) > 1]
    verificate = [(p, n) for p, n, _, _, v, _ in VOCI if v]
    return {
        "voci": voci, "creature": creature, "per_cat": per_cat,
        "multi": multi, "n_multi": len(multi),
        "verificate": verificate, "n_verificate": len(verificate),
        "nomi_sbagliati": len(NOMI_CORRETTI),
        "da_convertire": per_cat.get("creatura", {}).get("creature", 0),
    }
