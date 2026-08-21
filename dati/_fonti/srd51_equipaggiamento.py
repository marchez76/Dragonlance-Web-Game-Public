#!/usr/bin/env python3
"""
SRD 5.1 (CC-BY 4.0) — equipaggiamento ordinario: armi, armature, attrezzatura
d'avventura.

PERCHE' STA QUI
    Fase 2 aveva 50 mostri convertiti e nessun dato che dicesse quanti danni
    fa una spada lunga: senza equipaggiamento nessun combattimento e'
    simulabile. Questo modulo copre il buco, non l'inventario di una bottega:
    l'attrezzatura e' limitata a cio' che serve al combattimento e
    all'esplorazione (luce, corde, scasso, munizioni, contenitori), non ogni
    voce della tabella "Adventuring Gear" del Player's Handbook.

FONTE
    api.open5e.com. Due endpoint diversi per due ragioni diverse:
    - /v1/weapons/ e /v1/armor/, document__slug=wotc-srd: e' l'endpoint gia'
      usato per il bestiario (vedi srd51_mostri.py), verificato dare l'SRD
      5.1 (2014) e non il 5.2 (2024). Copre l'intera tabella Equipaggiamento:
      37 armi, 18 voci sotto "armor" di cui 13 sono armature/scudo vere (le
      altre 5 sono privilegi di classe o incantesimi che condividono
      l'endpoint: Draconic Resilience, Mage Armor, Unarmored, Unarmored
      Defense x2 — esclusi, non sono equipaggiamento).
    - /v2/items/, document__key=srd-2014: l'endpoint v1 non ha un endpoint
      equipaggiamento generico. Filtrato per fonte (il parametro
      document__key non esclude il 5.2 dai risultati: e' stato necessario
      un filtro a valle su document.key == "srd-2014", verificato contando
      237 voci proprie su 440 restituite).

    Il campo peso delle armature manca nell'endpoint v1 (stringa vuota per
    tutte e 13 le voci): recuperato da /v2/items/?category=armor, dove e'
    popolato e coincide fra le voci "srd-2014" e "srd-2024" (stesso valore,
    l'equipaggiamento mondano non e' cambiato fra le due edizioni) — non e'
    un valore inventato, e' lo stesso dato letto da un endpoint diverso.

    api_ref sotto e' lo slug/key usato per la query, per poter riverificare
    senza ripetere la ricerca.

DUE ANOMALIE DI DATI, NON DI FONTE
    - Blowgun ("1" piercing) e Net ("0", nessun tipo di danno): non hanno un
      dado di danno normale. Il fucile a canne (Blowgun) infligge 1 danno
      fisso, la rete (Net) non infligge danno (arma di controllo). Trascritti
      cosi' come l'API li restituisce, non forzati in una notazione "NdM".
    - Sling bullets: il campo desc dell'API segnala "Technically their cost
      is 20 for 4cp" (errore di battitura del Player's Handboook riportato
      pari pari da Open5e, non nostro).
"""

# (name_en, name_it, categoria_arma, damage_dice, damage_type, properties, cost_gp, weight_lb, api_ref)
ARMI = [
    ("Battleaxe", "Ascia da battaglia", "Martial Melee Weapons", "1d8", "slashing", ["versatile (1d10)"], 10.0, 4.0, "v1/weapons/battleaxe"),
    ("Blowgun", "Cerbottana", "Martial Ranged Weapons", "1", "piercing", ["ammunition (range 25/100)", "loading"], 10.0, 1.0, "v1/weapons/blowgun"),
    ("Club", "Randello", "Simple Melee Weapons", "1d4", "bludgeoning", ["light"], 0.1, 2.0, "v1/weapons/club"),
    ("Crossbow, hand", "Balestra a mano", "Martial Ranged Weapons", "1d6", "piercing", ["ammunition (range 30/120)", "light", "loading"], 75.0, 3.0, "v1/weapons/crossbow-hand"),
    ("Crossbow, heavy", "Balestra pesante", "Martial Ranged Weapons", "1d10", "piercing", ["ammunition (range 100/400)", "heavy", "loading", "two-handed"], 50.0, 18.0, "v1/weapons/crossbow-heavy"),
    ("Crossbow, light", "Balestra leggera", "Simple Ranged Weapons", "1d8", "piercing", ["ammunition (range 80/320)", "loading", "two-handed"], 25.0, 5.0, "v1/weapons/crossbow-light"),
    ("Dagger", "Pugnale", "Simple Melee Weapons", "1d4", "piercing", ["finesse", "light", "thrown (range 20/60)"], 2.0, 1.0, "v1/weapons/dagger"),
    ("Dart", "Freccetta", "Simple Ranged Weapons", "1d4", "piercing", ["finesse", "thrown (range 20/60)"], 0.05, 0.25, "v1/weapons/dart"),
    ("Flail", "Flagello", "Martial Melee Weapons", "1d8", "bludgeoning", [], 10.0, 2.0, "v1/weapons/flail"),
    ("Glaive", "Falcione", "Martial Melee Weapons", "1d10", "slashing", ["heavy", "reach", "two-handed"], 20.0, 6.0, "v1/weapons/glaive"),
    ("Greataxe", "Ascia bipenne", "Martial Melee Weapons", "1d12", "slashing", ["heavy", "two-handed"], 30.0, 7.0, "v1/weapons/greataxe"),
    ("Greatclub", "Clava", "Simple Melee Weapons", "1d8", "bludgeoning", ["two-handed"], 0.2, 10.0, "v1/weapons/greatclub"),
    ("Greatsword", "Spadone", "Martial Melee Weapons", "2d6", "slashing", ["heavy", "two-handed"], 50.0, 6.0, "v1/weapons/greatsword"),
    ("Halberd", "Alabarda", "Martial Melee Weapons", "1d10", "slashing", ["heavy", "reach", "two-handed"], 20.0, 6.0, "v1/weapons/halberd"),
    ("Handaxe", "Accetta", "Simple Melee Weapons", "1d6", "slashing", ["light", "thrown (range 20/60)"], 5.0, 2.0, "v1/weapons/handaxe"),
    ("Javelin", "Giavellotto", "Simple Melee Weapons", "1d6", "piercing", ["thrown (range 30/120)"], 0.5, 2.0, "v1/weapons/javelin"),
    ("Lance", "Lancia da cavaliere", "Martial Melee Weapons", "1d12", "piercing", ["reach", "special"], 10.0, 6.0, "v1/weapons/lance"),
    ("Light hammer", "Martello leggero", "Simple Melee Weapons", "1d4", "bludgeoning", ["light", "thrown (range 20/60)"], 2.0, 2.0, "v1/weapons/light-hammer"),
    ("Longbow", "Arco lungo", "Martial Ranged Weapons", "1d8", "piercing", ["ammunition (range 150/600)", "heavy", "two-handed"], 50.0, 2.0, "v1/weapons/longbow"),
    ("Longsword", "Spada lunga", "Martial Melee Weapons", "1d8", "slashing", ["versatile (1d10)"], 15.0, 3.0, "v1/weapons/longsword"),
    ("Mace", "Mazza", "Simple Melee Weapons", "1d6", "bludgeoning", [], 5.0, 4.0, "v1/weapons/mace"),
    ("Maul", "Maglio", "Martial Melee Weapons", "2d6", "bludgeoning", ["heavy", "two-handed"], 10.0, 10.0, "v1/weapons/maul"),
    ("Morningstar", "Stella del mattino", "Martial Melee Weapons", "1d8", "piercing", [], 15.0, 4.0, "v1/weapons/morningstar"),
    ("Net", "Rete", "Martial Ranged Weapons", "0", None, ["special", "thrown (range 5/15)"], 1.0, 3.0, "v1/weapons/net"),
    ("Pike", "Picca", "Martial Melee Weapons", "1d10", "piercing", ["heavy", "reach", "two-handed"], 5.0, 18.0, "v1/weapons/pike"),
    ("Quarterstaff", "Bastone da combattimento", "Simple Melee Weapons", "1d6", "bludgeoning", ["versatile (1d8)"], 0.2, 4.0, "v1/weapons/quarterstaff"),
    ("Rapier", "Stocco", "Martial Melee Weapons", "1d8", "piercing", ["finesse"], 25.0, 2.0, "v1/weapons/rapier"),
    ("Scimitar", "Scimitarra", "Martial Melee Weapons", "1d6", "slashing", ["finesse", "light"], 25.0, 3.0, "v1/weapons/scimitar"),
    ("Shortbow", "Arco corto", "Simple Ranged Weapons", "1d6", "piercing", ["ammunition (range 80/320)", "two-handed"], 25.0, 2.0, "v1/weapons/shortbow"),
    ("Shortsword", "Spada corta", "Martial Melee Weapons", "1d6", "piercing", ["finesse", "light"], 10.0, 2.0, "v1/weapons/shortsword"),
    ("Sickle", "Falcetto", "Simple Melee Weapons", "1d4", "slashing", ["light"], 1.0, 2.0, "v1/weapons/sickle"),
    ("Sling", "Fionda", "Simple Ranged Weapons", "1d4", "bludgeoning", ["ammunition (range 30/120)"], 0.1, 0.0, "v1/weapons/sling"),
    ("Spear", "Lancia", "Simple Melee Weapons", "1d6", "piercing", ["thrown (range 20/60)", "versatile (1d8)"], 1.0, 3.0, "v1/weapons/spear"),
    ("Trident", "Tridente", "Martial Melee Weapons", "1d6", "piercing", ["thrown (range 20/60)", "versatile (1d8)"], 5.0, 4.0, "v1/weapons/trident"),
    ("War pick", "Piccone da guerra", "Martial Melee Weapons", "1d8", "piercing", [], 5.0, 2.0, "v1/weapons/war-pick"),
    ("Warhammer", "Martello da guerra", "Martial Melee Weapons", "1d8", "bludgeoning", ["versatile (1d10)"], 15.0, 2.0, "v1/weapons/warhammer"),
    ("Whip", "Frusta", "Martial Melee Weapons", "1d4", "slashing", ["finesse", "reach"], 2.0, 3.0, "v1/weapons/whip"),
]

# (name_en, name_it, categoria(leggera/media/pesante/scudo), ac_string, strength_requirement, stealth_disadvantage, cost_gp, weight_lb, api_ref)
ARMATURE = [
    ("Padded", "Imbottita", "leggera", "11 + Dex modifier", None, True, 5.0, 8.0, "v1/armor/padded"),
    ("Leather", "Di cuoio", "leggera", "11 + Dex modifier", None, False, 10.0, 10.0, "v1/armor/leather"),
    ("Studded Leather", "Di cuoio borchiata", "leggera", "12 + Dex modifier", None, False, 45.0, 13.0, "v1/armor/studded-leather"),
    ("Hide", "Di pelle", "media", "12 + Dex modifier (max 2)", None, False, 10.0, 12.0, "v1/armor/hide"),
    ("Chain Shirt", "Camicia di maglia", "media", "13 + Dex modifier (max 2)", None, False, 50.0, 20.0, "v1/armor/chain-shirt"),
    ("Scale mail", "Corazza a scaglie", "media", "14 + Dex modifier (max 2)", None, True, 50.0, 45.0, "v1/armor/scale-mail"),
    ("Breastplate", "Corazza", "media", "14 + Dex modifier (max 2)", None, False, 400.0, 20.0, "v1/armor/breastplate"),
    ("Half plate", "Mezza piastra", "media", "15 + Dex modifier (max 2)", None, True, 750.0, 40.0, "v1/armor/half-plate"),
    ("Ring mail", "Corazza ad anelli", "pesante", "14", None, True, 30.0, 40.0, "v1/armor/ring-mail"),
    ("Chain mail", "Cotta di maglia", "pesante", "16", 13, True, 75.0, 55.0, "v1/armor/chain-mail"),
    ("Splint", "A stecche", "pesante", "17", 15, True, 200.0, 60.0, "v1/armor/splint"),
    ("Plate", "Armatura a piastre", "pesante", "18", 15, True, 1500.0, 65.0, "v1/armor/plate"),
    ("Shield", "Scudo", "scudo", "+2", None, False, 10.0, 6.0, "v1/armor/shield"),
]

# (name_en, name_it, desc_en, cost_gp, weight_lb, api_ref)
ATTREZZATURA = [
    ("Torch", "Torcia", "A torch burns for 1 hour, providing bright light in a 20-foot radius and dim light for an additional 20 feet. If you make a melee attack with a burning torch and hit, it deals 1 fire damage.", 0.01, 1.0, "v2/items/srd_torch"),
    ("Tinderbox", "Acciarino", "This small container holds flint, fire steel, and tinder (usually dry cloth soaked in light oil) used to kindle a fire. Using it to light a torch (or anything else with abundant, exposed fuel) takes an action. Lighting any other fire takes 1 minute.", 0.5, 1.0, "v2/items/srd_tinderbox"),
    ("Lantern, Hooded", "Lanterna cieca", "A hooded lantern casts bright light in a 30-foot radius and dim light for an additional 30 feet. Once lit, it burns for 6 hours on a flask (1 pint) of oil. As an action, you can lower the hood, reducing the light to dim light in a 5-foot radius.", 5.0, 2.0, "v2/items/srd_lantern-hooded"),
    ("Lamp oil (flask)", "Olio da lampada (fiasca)", "Oil usually comes in a clay flask that holds 1 pint. As an action, you can splash the oil in this flask onto a creature within 5 feet of you or throw it up to 20 feet, shattering it on impact, treating it as an improvised weapon. If lit, the oil burns for 2 rounds and deals 5 fire damage to any creature that enters the area or ends its turn in the area.", 0.1, 1.0, "v2/items/srd_lamp-oil-flask"),
    ("Rope, hempen (50 feet)", "Corda di canapa (15 metri)", "Rope, whether made of hemp or silk, has 2 hit points and can be burst with a DC 17 Strength check.", 1.0, 10.0, "v2/items/srd_rope-hempen-50-feet"),
    ("Rope, silk (50 feet)", "Corda di seta (15 metri)", "Rope, whether made of hemp or silk, has 2 hit points and can be burst with a DC 17 Strength check.", 10.0, 5.0, "v2/items/srd_rope-silk-50-feet"),
    ("Grappling hook", "Rampino", "A grappling hook.", 2.0, 4.0, "v2/items/srd_grappling-hook"),
    ("Climber's Kit", "Kit da scalata", "A climber's kit includes special pitons, boot tips, gloves, and a harness. You can use the climber's kit as an action to anchor yourself; when you do, you can't fall more than 25 feet from the point where you anchored yourself, and you can't climb more than 25 feet away from that point without undoing the anchor.", 25.0, 12.0, "v2/items/srd_climbers-kit"),
    ("Piton", "Chiodo da roccia", "A piton for climbing.", 0.05, 0.25, "v2/items/srd_piton"),
    ("Ladder (10-foot)", "Scala a pioli (3 metri)", "A 10 foot ladder.", 0.1, 25.0, "v2/items/srd_ladder-10-foot"),
    ("Backpack", "Zaino", "A backpack. Capacity: 1 cubic foot/30 pounds of gear.", 2.0, 5.0, "v2/items/srd_backpack"),
    ("Pouch", "Borsa", "A cloth or leather pouch can hold up to 20 sling bullets or 50 blowgun needles, among other things. Capacity: 1/5 cubic foot/6 pounds of gear.", 0.5, 1.0, "v2/items/srd_pouch"),
    ("Sack", "Sacco", "A sack. Capacity: 1 cubic foot/30 pounds of gear.", 0.01, 0.5, "v2/items/srd_sack"),
    ("Chest", "Baule", "A chest. Capacity: 12 cubic feet/300 pounds of gear.", 5.0, 25.0, "v2/items/srd_chest"),
    ("Quiver", "Faretra", "A quiver can hold up to 20 arrows.", 1.0, 1.0, "v2/items/srd_quiver"),
    ("Waterskin", "Otre", "For drinking. Capacity: 4 pints liquid.", 0.2, 5.0, "v2/items/srd_waterskin"),
    ("Case, Crossbow Bolt", "Custodia per dardi", "This wooden case can hold up to twenty crossbow bolts.", 1.0, 1.0, "v2/items/srd_case-crossbow-bolt"),
    ("Crowbar", "Piede di porco", "Using a crowbar grants advantage to Strength checks where the crowbar's leverage can be applied.", 2.0, 5.0, "v2/items/srd_crowbar"),
    ("Healer's Kit", "Kit del guaritore", "This kit is a leather pouch containing bandages, salves, and splints. The kit has ten uses. As an action, you can expend one use of the kit to stabilize a creature that has 0 hit points, without needing to make a Wisdom (Medicine) check.", 5.0, 3.0, "v2/items/srd_healers-kit"),
    ("Manacles", "Manette", "These metal restraints can bind a Small or Medium creature. Escaping the manacles requires a successful DC 20 Dexterity check. Breaking them requires a successful DC 20 Strength check. Manacles have 15 hit points.", 2.0, 6.0, "v2/items/srd_manacles"),
    ("Caltrops (bag of 20)", "Tribolo (sacco da 20)", "As an action, you can spread a bag of caltrops to cover a square area that is 5 feet on a side. Any creature that enters the area must succeed on a DC 15 Dexterity saving throw or stop moving this turn and take 1 piercing damage.", 1.0, 2.0, "v2/items/srd_caltrops-bag-of-20"),
    ("Ball Bearings (bag of 1000)", "Sfere di metallo (sacco da 1000)", "As an action, you can spill these tiny metal balls from their pouch to cover a level, square area that is 10 feet on a side. A creature moving across the covered area must succeed on a DC 10 Dexterity saving throw or fall prone.", 1.0, 2.0, "v2/items/srd_ball-bearings-bag-of-1000"),
    ("Hunting Trap", "Tagliola", "When you use your action to set it, this trap forms a saw-toothed steel ring that snaps shut when a creature steps on a pressure plate in the center. A creature that steps on the plate must succeed on a DC 13 Dexterity saving throw or take 1d4 piercing damage and stop moving.", 5.0, 25.0, "v2/items/srd_hunting-trap"),
    ("Thieves' tools", "Arnesi da scasso", "This set of tools includes a small file, a set of lock picks, a small mirror mounted on a metal handle, a set of narrow-bladed scissors, and a pair of pliers. Proficiency with these tools lets you add your proficiency bonus to any ability checks you make to disarm traps or open locks.", 25.0, 1.0, "v2/items/srd_thieves-tools"),
    ("Arrow", "Freccia", "An arrow for a bow.", 0.05, 0.05, "v2/items/srd_arrow-bow"),
    ("Crossbow bolt", "Dardo da balestra", "Bolts to be used in a crossbow.", 0.05, 0.08, "v2/items/srd_crossbow-bolt"),
    ("Sling bullets", "Proiettili da fionda", "Sold in bags of 20.", 0.01, 0.075, "v2/items/srd_sling-bullets"),
    ("Blowgun needles", "Aghi da cerbottana", "Needles to be fired with a blowgun. Sold in bags of 50.", 0.02, 0.02, "v2/items/srd_blowgun-needles"),
]
