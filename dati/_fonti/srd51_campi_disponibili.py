#!/usr/bin/env python3
"""
Inventario dei CAMPI che le fonti strutturate offrono, e dove finiscono da noi.

PERCHE' STA QUI
    "La categoria d'arma non era un dato mancante, era un dato scartato."
    Un parser che butta nella prosa un campo che la fonte da' strutturato
    produce qualcosa che SEMBRA una lacuna della fonte: nessun validatore lo
    prende, perche' il dato formalmente non manca. E' un difetto invisibile
    per costruzione, e l'unico modo di vederlo e' mettere l'elenco dei campi
    della fonte accanto all'elenco dei campi nostri.

    Gli altri moduli di questa cartella trascrivono i VALORI. Questo
    trascrive i NOMI DEI CAMPI e, per ciascuno, dichiara la destinazione
    nei nostri dati. E' la sola cosa che rende misurabile lo scarto: un
    campo di fonte senza destinazione dichiarata e' uno scarto, e va detto
    perche'.

COME SI LEGGE UNA VOCE
    nome_del_campo: (destinazione, motivo)

    destinazione e' una di queste tre cose:
      - un percorso puntato dentro il JSON che produciamo
        (`mechanics_5e.weapon_5e.damage_dice`): dati/analizza_campi_scartati.py
        VERIFICA che quel percorso esista davvero nei file prodotti. Una
        destinazione dichiarata e non trovata e' un errore, non una svista:
        significa che questo elenco e' andato fuori sincrono con i dati.
      - META: intestazione di licenza e provenienza dell'API, non un dato di
        gioco. Non e' uno scarto.
      - SCARTATO: la fonte lo da', noi non lo prendiamo. Il motivo dice se e'
        una scelta o una dimenticanza.

    Le destinazioni sono percorsi RELATIVI al documento prodotto, con `[]`
    dove si attraversa una lista.

SONDE E DATA DI LETTURA
    Ogni endpoint dichiara il record usato come sonda e il giorno in cui e'
    stato letto. L'elenco dei campi e' quello di quel record: un campo che
    l'API aggiungesse domani non comparirebbe qui, e va bene cosi' — questa
    e' una fotografia datata, come tutte le trascrizioni di questa cartella.

DUE ENDPOINT CHE NON LEGGIAMO
    v2/creatures e v2/spells sono elencati in fondo e hanno tutte le
    destinazioni a SCARTATO per costruzione: non li leggiamo affatto. Non
    sono un'accusa. La scelta di stare su v1 e' documentata
    (srd51_incantesimi.py: v1 ha un solo documento Wizards, quindi non puo'
    mischiare edizioni; v2 si', e srd51_equipaggiamento.py ha dovuto
    filtrare a valle). Stanno qui perche' la misura richiesta e' "quanti
    campi disponibili non estraiamo", e un campo disponibile su un altro
    endpoint della stessa API resta disponibile.
"""

META = "META"
SCARTATO = "SCARTATO"

# --------------------------------------------------------------- v1/weapons
# Sonda: api.open5e.com/v1/weapons/longsword/  — letto il 2026-09-02
V1_WEAPONS = {
    "letto_il": "2026-09-02",
    "sonda": "v1/weapons/longsword",
    "usato_da": "_fonti/srd51_equipaggiamento.py ARMI -> dati/oggetti/",
    "campione": "dati/oggetti/longsword.json",
    "campi": {
        "name":                 ("name.en", None),
        "slug":                 ("source_srd.api_ref", "trascritto come api_ref"),
        "category":             ("mechanics_5e.weapon_5e.categoria",
                                 "IL CASO DEL RITROVAMENTO: la fonte lo dava "
                                 "strutturato, build_oggetti.py lo buttava "
                                 "nella prosa della descrizione. Corretto il "
                                 "01/09/2026."),
        "cost":                 ("mechanics_5e.weapon_5e.cost_gp", None),
        "damage_dice":          ("mechanics_5e.weapon_5e.damage_dice", None),
        "damage_type":          ("mechanics_5e.weapon_5e.damage_type", None),
        "weight":               ("mechanics_5e.weapon_5e.weight_lb", None),
        "properties":           ("mechanics_5e.weapon_5e.properties",
                                 "l'endpoint v1 le da' come stringhe, non "
                                 "come campi: qui il parsing e' legittimo, "
                                 "non c'e' altra forma da leggere. Ma vedi "
                                 "v2/items, dove ci sono anche i booleani."),
        "document__slug":       (META, None),
        "document__title":      (META, None),
        "document__license_url": (META, None),
        "document__url":        (META, None),
    },
}

# ----------------------------------------------------------------- v1/armor
# Sonda: api.open5e.com/v1/armor/chain-mail/  — letto il 2026-09-02
V1_ARMOR = {
    "letto_il": "2026-09-02",
    "sonda": "v1/armor/chain-mail",
    "usato_da": "_fonti/srd51_equipaggiamento.py ARMATURE -> dati/oggetti/",
    "campione": "dati/oggetti/chain-mail.json",
    "campi": {
        "name":                 ("name.en", None),
        "slug":                 ("source_srd.api_ref", None),
        "category":             ("mechanics_5e.armor_5e.categoria",
                                 "tradotto: Heavy Armor -> pesante"),
        "ac_string":            ("mechanics_5e.armor_5e.ac_formula", None),
        "base_ac":              (SCARTATO,
                                 "STESSO DIFETTO DELLA CATEGORIA D'ARMA, "
                                 "ANCORA APERTO: ca_5e.ca_base viene da "
                                 "build_oggetti.ca_strutturata(), che rilegge "
                                 "ac_string con l'espressione regolare "
                                 "_CA_BASE. Il numero e' un campo della fonte."),
        "plus_dex_mod":         (SCARTATO,
                                 "ca_5e.applica_mod_dex e' ricavato cercando "
                                 "'Dex modifier' nella stringa."),
        "plus_max":             (SCARTATO,
                                 "ca_5e.mod_dex_max e' ricavato con "
                                 "l'espressione regolare _CA_MAXDEX su "
                                 "'(max 2)'."),
        "plus_flat_mod":        (SCARTATO,
                                 "ca_5e.bonus_ca e' ricavato con _CA_BONUS. "
                                 "E' il campo che regge lo scudo."),
        "plus_con_mod":         (SCARTATO,
                                 "nessuna delle 13 armature vere lo usa: vale "
                                 "solo per Unarmored Defense del Barbaro, che "
                                 "non e' un'armatura. Scarto senza costo, ma "
                                 "e' un campo disponibile."),
        "plus_wis_mod":         (SCARTATO,
                                 "come sopra, per il Monaco."),
        "strength_requirement": ("mechanics_5e.armor_5e.strength_requirement", None),
        "stealth_disadvantage": ("mechanics_5e.armor_5e.stealth_disadvantage", None),
        "cost":                 ("mechanics_5e.armor_5e.cost_gp", None),
        "weight":               ("mechanics_5e.armor_5e.weight_lb",
                                 "vuoto su v1 per tutte e 13: recuperato da "
                                 "v2/items, gia' documentato nel modulo."),
        "document__slug":       (META, None),
        "document__title":      (META, None),
        "document__license_url": (META, None),
        "document__url":        (META, None),
    },
}

# ----------------------------------------------------------------- v2/items
# Sonda: api.open5e.com/v2/items/srd_longsword/  — letto il 2026-09-02
V2_ITEMS = {
    "letto_il": "2026-09-02",
    "sonda": "v2/items/srd_longsword",
    "usato_da": ("_fonti/srd51_equipaggiamento.py ATTREZZATURA -> dati/oggetti/; "
                 "per le armi e' l'endpoint NON letto"),
    "campione": "dati/oggetti/torch.json",
    "campi": {
        "name":             ("name.en", None),
        "key":              ("source_srd.api_ref", None),
        "desc":             ("source_srd.descrizione",
                             "solo per l'attrezzatura; per armi e armature la "
                             "descrizione e' scritta da noi."),
        "cost":             (SCARTATO,
                             "TERZO CASO DELLA STESSA FORMA, ANCORA APERTO. "
                             "Armi e armature hanno cost_gp in un campo; le 28 "
                             "voci di attrezzatura no: build_oggetti.py scrive "
                             "prezzo e peso dentro una frase italiana di "
                             "mechanics_5e.note ('Peso 1.0 lb, costo 0.01 mo'). "
                             "Il campo esiste alla fonte e finisce in prosa. "
                             "E' il buco che la decisione 42 (`cambio-acciaio-oro`) "
                             "NON chiude: il rapporto "
                             "acciaio/oro ora c'e', ma su 28 oggetti non c'e' "
                             "un prezzo leggibile a cui applicarlo."),
        "weight":           (SCARTATO, "stessa nota di cost."),
        "weight_unit":      (SCARTATO, "sempre 'lb', assunto implicito."),
        "category":         (SCARTATO,
                             "l'oggetto {name, key} che dice se e' Weapon, "
                             "Armor, Adventuring Gear. La nostra `categoria` "
                             "e' decisa dal ramo di build_oggetti.py che sta "
                             "girando, non letta."),
        "size":             (SCARTATO, "taglia dell'oggetto."),
        "weapon.is_simple":  (SCARTATO,
                              "booleano. La nostra weapon_5e.categoria "
                              "(semplice/da_guerra) e' ricavata cercando "
                              "'Simple' nella stringa category di v1."),
        "weapon.is_martial": (SCARTATO, "come sopra."),
        "weapon.is_improvised": (SCARTATO, "arma improvvisata."),
        "weapon.distance_unit": (SCARTATO, "sempre 'feet'."),
        "weapon.properties[].property": (SCARTATO,
                              "ogni proprieta' e' un oggetto {property, "
                              "detail}: il nome e il suo parametro sono gia' "
                              "separati. proprieta_strutturate() in "
                              "build_oggetti.py separa gli stessi due pezzi "
                              "con due espressioni regolari su v1."),
        "weapon.properties[].detail": (SCARTATO,
                              "il parametro: '1d10' per versatile, la gittata "
                              "per ammunition. E' il numero che oggi "
                              "estraiamo dal testo."),
        "weapon.damage_dice": (SCARTATO, "gia' preso da v1."),
        "weapon.damage_type": (SCARTATO, "gia' preso da v1."),
        "armor":            (SCARTATO, "null sulle armi; sulle armature ha i "
                             "campi strutturati gia' contati in v1/armor."),
        "document":         (META, None),
        "crossreferences":  (SCARTATO, "rimandi ad altre voci."),
    },
}

# ---------------------------------------------------------------- v1/spells
# Sonda: api.open5e.com/v1/spells/fireball/  — letto il 2026-09-02
V1_SPELLS = {
    "letto_il": "2026-09-02",
    "sonda": "v1/spells/fireball",
    "usato_da": "_fonti/srd51_incantesimi.py -> dati/incantesimi/",
    "campione": "dati/incantesimi/fireball.json",
    "campi": {
        "name":             ("name.en", None),
        "slug":             ("source.api_ref", None),
        "desc":             ("descrizione", None),
        "higher_level":     ("a_livelli_superiori", None),
        "range":            ("range", None),
        "target_range_sort": (SCARTATO,
                             "LA GITTATA IN NUMERO. Noi teniamo la stringa "
                             "'150 feet'; la fonte da' anche 150 come intero. "
                             "Un motore che deve sapere se il bersaglio e' a "
                             "tiro oggi deve leggere la stringa."),
        "components":       (SCARTATO,
                             "la stringa 'V, S, M'. Ridondante: i tre "
                             "booleani sotto la coprono, ed e' quella che "
                             "prendiamo."),
        "requires_verbal_components":   ("components.verbal", None),
        "requires_somatic_components":  ("components.somatic", None),
        "requires_material_components": ("components.material", None),
        "material":         ("components.material_desc", None),
        "can_be_cast_as_ritual": ("ritual", None),
        "ritual":           (SCARTATO, "il duplicato testuale 'no'/'yes' del "
                             "booleano sopra. Scarto senza costo."),
        "duration":         ("duration", None),
        "concentration":    (SCARTATO, "duplicato testuale, come ritual."),
        "requires_concentration": ("concentration", None),
        "casting_time":     ("casting_time", None),
        "level":            (SCARTATO, "'3rd-level': la forma testuale."),
        "level_int":        ("level", None),
        "spell_level":      (SCARTATO, "terzo duplicato dello stesso numero."),
        "school":           ("school", None),
        "dnd_class":        ("classes",
                             "scelta documentata: spell_lists omette il "
                             "Paladino su 76 voci."),
        "spell_lists":      (SCARTATO,
                             "scarto DELIBERATO e gia' documentato: il campo "
                             "e' incompleto alla fonte."),
        "archetype":        (SCARTATO,
                             "'Cleric: Light, Warlock: Fiend' — quali "
                             "sottoclassi ottengono l'incantesimo. Non serve "
                             "finche' non ci sono sottoclassi."),
        "circles":          (SCARTATO, "circoli druidici. Come archetype."),
        "page":             (SCARTATO,
                             "'phb 241'. Rimando di pagina alla fonte: e' il "
                             "campo che il progetto tratta come tracciabilita' "
                             "ovunque (convenzione delle pagine, CLAUDE.md 4) "
                             "e qui non viene preso."),
        "document__slug":       (META, None),
        "document__title":      (META, None),
        "document__license_url": (META, None),
        "document__url":        (META, None),
    },
}

# -------------------------------------------------------------- v1/monsters
# Sonda: api.open5e.com/v1/monsters/goblin/  — letto il 2026-09-02
#
# ATTENZIONE ALLA NATURA DI QUESTO ENDPOINT: non e' la fonte dei nostri
# mostri (quella e' l'MC Dragonlance Appendix, 2e) ma il RISCONTRO su cui si
# calibrano le conversioni per analogia. Lo scarto qui non e' "dato perso":
# e' "riscontro non disponibile". Vale comunque contarlo, perche' il
# riscontro che serve alla Fase 2 e' proprio quello che non abbiamo preso.
V1_MONSTERS = {
    "letto_il": "2026-09-02",
    "sonda": "v1/monsters/goblin",
    "usato_da": "_fonti/srd51_mostri.py -> riscontro di calibrazione",
    "campione": None,   # non produce file: e' una tabella in memoria
    "campi": {
        "name":         ("MOSTRI[].nome", None),
        "size":         ("MOSTRI[].taglia", None),
        "type":         ("MOSTRI[].tipo", None),
        "armor_class":  ("MOSTRI[].ca", None),
        "hit_points":   ("MOSTRI[].pf", None),
        "speed":        ("MOSTRI[].velocita", None),
        "challenge_rating": ("MOSTRI[].gs", None),
        "slug":         (SCARTATO, "identificatore."),
        "desc":         (SCARTATO, None),
        "subtype":      (SCARTATO, None),
        "group":        (SCARTATO, None),
        "alignment":    (SCARTATO, None),
        "armor_desc":   (SCARTATO, "'leather armor, shield': da cosa viene la CA."),
        "hit_dice":     (SCARTATO, "'2d6'. La formula dei PF, che per i nostri "
                                   "mostri scriviamo a mano in hit_points.formula."),
        "strength":     (SCARTATO, "LE SEI CARATTERISTICHE. abilities_note di "
                                   "ogni nostro mostro spiega che la 2e non le "
                                   "assegna e vanno stimate: la mediana per "
                                   "grado di sfida, che renderebbe la stima "
                                   "verificabile, e' in questo endpoint."),
        "dexterity":    (SCARTATO, "come sopra."),
        "constitution": (SCARTATO, "come sopra."),
        "intelligence": (SCARTATO, "come sopra."),
        "wisdom":       (SCARTATO, "come sopra."),
        "charisma":     (SCARTATO, "come sopra."),
        "strength_save":     (SCARTATO, None),
        "dexterity_save":    (SCARTATO, None),
        "constitution_save": (SCARTATO, None),
        "intelligence_save": (SCARTATO, None),
        "wisdom_save":       (SCARTATO, None),
        "charisma_save":     (SCARTATO, None),
        "perception":   (SCARTATO, None),
        "skills":       (SCARTATO, "oggetto {stealth: 6}."),
        "damage_vulnerabilities": (SCARTATO, None),
        "damage_resistances":     (SCARTATO, None),
        "damage_immunities":      (SCARTATO, None),
        "condition_immunities":   (SCARTATO, None),
        "senses":       (SCARTATO, "'darkvision 60 ft., passive Perception 9'."),
        "languages":    (SCARTATO, None),
        "cr":           (SCARTATO, "il grado di sfida in decimale (0.25). Noi "
                                   "teniamo la stringa '1/4' e ordiniamo i "
                                   "mostri riconvertendola."),
        "actions":      (SCARTATO,
                         "IL BLOCCO CHE SERVE ALLA FETTA. Ogni azione porta "
                         "gia' name, desc, attack_bonus, damage_dice, "
                         "damage_bonus: il bonus di attacco e i dadi di danno "
                         "sono campi, non prosa. E' esattamente la forma che "
                         "manca ai nostri mostri per far girare uno scontro."),
        "bonus_actions":     (SCARTATO, "stessa forma di actions."),
        "reactions":         (SCARTATO, "stessa forma di actions."),
        "legendary_actions": (SCARTATO, "{name, desc}."),
        "legendary_desc":    (SCARTATO, None),
        "special_abilities": (SCARTATO, "{name, desc}: i tratti."),
        "spell_list":        (SCARTATO, None),
        "page_no":           (SCARTATO, "pagina di fonte."),
        "environments":      (SCARTATO,
                              "l'elenco degli ambienti. E' il dato del GRUPPO "
                              "A della decisione 27 (`sette-campi-2e`), quello "
                              "che la 5e ha spostato dalla scheda alle tabelle "
                              "d'incontro: qui c'e', in forma di lista."),
        "img_main":          (SCARTATO, None),
        "v2_converted_path": (SCARTATO, "il rimando alla voce v2 della stessa "
                                        "creatura, dove gli attacchi sono "
                                        "scomposti in campi."),
        "document__slug":       (META, None),
        "document__title":      (META, None),
        "document__license_url": (META, None),
        "document__url":        (META, None),
    },
}

# ------------------------------------------------- due endpoint mai letti
# Sonda: api.open5e.com/v2/creatures/srd_goblin/  — letto il 2026-09-02
V2_CREATURES = {
    "letto_il": "2026-09-02",
    "sonda": "v2/creatures/srd_goblin",
    "usato_da": None,
    "campione": None,
    "mai_letto": True,
    "campi": {k: (SCARTATO, m) for k, m in [
        ("key", None), ("name", None), ("document", None), ("type", None),
        ("size", None), ("challenge_rating", None),
        ("proficiency_bonus", "il bonus di competenza gia' calcolato."),
        ("speed", None), ("speed_all", None), ("category", None),
        ("subcategory", None), ("alignment", None), ("languages", None),
        ("armor_class", None), ("armor_detail", None), ("hit_points", None),
        ("hit_dice", None), ("experience_points", None),
        ("ability_scores", "le sei caratteristiche in un oggetto."),
        ("modifiers", "i sei modificatori gia' calcolati."),
        ("initiative_bonus", "il bonus di iniziativa."),
        ("saving_throws", None), ("saving_throws_all", None),
        ("skill_bonuses", None), ("skill_bonuses_all", None),
        ("passive_perception", None), ("resistances_and_immunities", None),
        ("normal_sight_range", None), ("darkvision_range", None),
        ("blindsight_range", None), ("tremorsense_range", None),
        ("truesight_range", None),
        ("actions", "OGNI AZIONE HA UN ARRAY `attacks` CON I CAMPI: "
                    "to_hit_mod, reach, range, long_range, damage_die_count, "
                    "damage_die_type, damage_bonus, damage_type, "
                    "extra_damage_*, distance_unit, target_creature_only. "
                    "Piu' action_type, usage_limits, legendary_action_cost."),
        ("traits", None), ("creaturesets", None), ("environments", None),
        ("illustration", None), ("crossreferences", None),
    ]},
}

# Sonda: api.open5e.com/v2/spells/  — letto il 2026-09-02
V2_SPELLS = {
    "letto_il": "2026-09-02",
    "sonda": "v2/spells/ (primo risultato)",
    "usato_da": None,
    "campione": None,
    "mai_letto": True,
    "campi": {k: (SCARTATO, m) for k, m in [
        ("key", None), ("name", None), ("document", None), ("desc", None),
        ("higher_level", None), ("school", None), ("classes", None),
        ("level", None), ("casting_time", None), ("reaction_condition", None),
        ("duration", None), ("concentration", None), ("ritual", None),
        ("verbal", None), ("somatic", None), ("material", None),
        ("material_specified", None), ("material_cost", None),
        ("material_consumed", None),
        ("range", "la gittata come numero."),
        ("range_text", None), ("range_unit", None),
        ("target_type", None), ("target_count", None),
        ("saving_throw_ability", "IL TIRO SALVEZZA COME CAMPO. Oggi si legge "
                                 "dalla prosa di `descrizione`."),
        ("attack_roll", "booleano: l'incantesimo richiede un tiro per colpire."),
        ("damage_roll", "IL DANNO COME CAMPO ('8d6')."),
        ("damage_types", "l'array dei tipi di danno."),
        ("shape_type", "la forma dell'area (sfera, cono, linea)."),
        ("shape_size", "la sua misura."),
        ("shape_size_unit", None),
        ("casting_options", "le varianti a slot superiore, scomposte."),
        ("crossreferences", None),
    ]},
}

ENDPOINT = [
    ("v1/weapons",   V1_WEAPONS),
    ("v1/armor",     V1_ARMOR),
    ("v2/items",     V2_ITEMS),
    ("v1/spells",    V1_SPELLS),
    ("v1/monsters",  V1_MONSTERS),
    ("v2/creatures", V2_CREATURES),
    ("v2/spells",    V2_SPELLS),
]


def conta(voce):
    """(totale, estratti, scartati, metadata) per un endpoint."""
    campi = voce["campi"]
    est = sum(1 for d, _ in campi.values() if d not in (META, SCARTATO))
    sca = sum(1 for d, _ in campi.values() if d == SCARTATO)
    met = sum(1 for d, _ in campi.values() if d == META)
    return len(campi), est, sca, met


# ------------------------------------------------------------------ armature
# I sei campi strutturati della CA per le 13 armature vere dell'SRD, letti da
# api.open5e.com/v1/armor/?document__slug=wotc-srd il 2026-09-02 (18 voci
# restituite, 5 delle quali non sono equipaggiamento e sono escluse qui come
# in srd51_equipaggiamento.py).
#
# PERCHE' TRASCRITTI: sono i campi che build_oggetti.ca_strutturata() rifa'
# con tre espressioni regolari. Averli permette di provare l'affermazione
# invece di dichiararla: analizza_campi_scartati.py li mette contro il nostro
# ca_5e, campo per campo.
#
# slug: (base_ac, plus_dex_mod, plus_flat_mod, plus_max, ac_string)
CA_STRUTTURATA_SRD = {
    "padded":          (11, True,  0, 0, "11 + Dex modifier"),
    "leather":         (11, True,  0, 0, "11 + Dex modifier"),
    "studded-leather": (12, True,  0, 0, "12 + Dex modifier"),
    "hide":            (12, True,  0, 2, "12 + Dex modifier (max 2)"),
    "chain-shirt":     (13, True,  0, 2, "13 + Dex modifier (max 2)"),
    "scale-mail":      (14, True,  0, 2, "14 + Dex modifier (max 2)"),
    "breastplate":     (14, True,  0, 2, "14 + Dex modifier (max 2)"),
    "half-plate":      (15, True,  0, 2, "15 + Dex modifier (max 2)"),
    "ring-mail":       (14, False, 0, 0, "14"),
    "chain-mail":      (16, False, 0, 0, "16"),
    "splint":          (17, False, 0, 0, "17"),
    "plate":           (18, False, 0, 0, "18"),
    "shield":          (0,  False, 2, 0, "0 +2"),
}
