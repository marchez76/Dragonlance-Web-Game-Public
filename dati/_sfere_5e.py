#!/usr/bin/env python3
"""
DECISIONE 24 — mappatura fra le sfere sacerdotali 2e e la lista incantesimi
del chierico 5e (SRD 5.1, CC-BY).

COME FUNZIONA IL FILTRO
    Le SFERE della divinita' governano quali incantesimi il chierico puo'
    preparare. Il DOMINIO 5e resta come sottoclasse e fornisce i privilegi di
    livello e gli incantesimi sempre preparati. Le due cose non si sostituiscono.

    Accesso MAGGIORE: tutti i livelli.
    Accesso MINORE:   solo fino al 3° livello di incantesimo, come in 2e.

DERIVAZIONE, il campo che va conservato
    "fonte"   l'incantesimo 5e ha un antenato 2e diretto e ne eredita la sfera.
              Esempio: Cure Wounds da "cure light wounds", sfera Healing.
    "nostra"  nessun antenato: classificato per effetto. E' un'attribuzione
              editoriale nostra e deve restare distinguibile.

    Il caso piu' massiccio di "nostra" sono i TRUCCHETTI: in AD&D 2e i
    sacerdoti non ne avevano affatto, quindi tutti e sette sono nostri.

FONTE DELLA LISTA
    SRD 5.1 via api.open5e.com (document__slug=wotc-srd). Lista base del
    chierico: 105 voci, 7 trucchetti piu' 98 incantesimi dal 1° al 9°.
    Gli incantesimi di dominio (37 nell'SRD) NON sono nella lista base: si
    ottengono col Dominio e non passano dal filtro delle sfere.
"""

# --------------------------------------------------------------------------
# Nomi canonici delle sfere. Il manuale usa due varianti per due sfere:
# "Plant"/"Plants" e "Necromantic"/"Necromancy". Sono la stessa sfera, e senza
# normalizzazione il filtro le tratterebbe come distinte.
# --------------------------------------------------------------------------
ALIAS = {
    "Plants": "Plant",
    "Necromancy": "Necromantic",
}

SFERE = [
    "All", "Animal", "Astral", "Charm", "Combat", "Creation", "Divination",
    "Elemental", "Guardian", "Healing", "Necromantic", "Plant", "Protection",
    "Summoning", "Sun", "Weather",
]


def norm(nome):
    return ALIAS.get(nome, nome)


# --------------------------------------------------------------------------
# (nome, livello, scuola, [sfere], derivazione, nota)
# --------------------------------------------------------------------------
def s(nome, liv, scuola, sfere, deriv, nota=None):
    return {"name": nome, "level": liv, "school": scuola,
            "spheres": [norm(x) for x in sfere], "derivation": deriv,
            "note": nota}


LISTA_BASE = [
    # ---- trucchetti: TUTTI nostri, la 2e non li aveva per i sacerdoti ----
    s("Guidance", 0, "Divination", ["Divination"], "nostra",
      "Trucchetto. La 2e non dava trucchetti ai sacerdoti: attribuzione per effetto."),
    s("Light", 0, "Evocation", ["Sun"], "nostra", "Trucchetto."),
    s("Mending", 0, "Transmutation", ["Creation"], "nostra", "Trucchetto."),
    s("Resistance", 0, "Abjuration", ["Protection"], "nostra", "Trucchetto."),
    s("Sacred Flame", 0, "Evocation", ["Combat"], "nostra",
      "Trucchetto. Unica offesa a volonta' del chierico 5e: la sfera Combat "
      "decide se una divinita' ce l'ha."),
    s("Spare the Dying", 0, "Necromancy", ["Necromantic"], "nostra", "Trucchetto."),
    s("Thaumaturgy", 0, "Transmutation", ["All"], "nostra",
      "Trucchetto. Manifestazione di potere divino senza effetto meccanico: "
      "assegnato ad All perche' non e' materia di alcuna sfera."),

    # ---- 1° livello ----
    s("Bane", 1, "Enchantment", ["All"], "fonte",
      "Inverso di bless, che in 2e e' sfera All."),
    s("Bless", 1, "Enchantment", ["All"], "fonte"),
    s("Command", 1, "Enchantment", ["Charm"], "fonte"),
    s("Create or Destroy Water", 1, "Transmutation", ["Elemental"], "fonte",
      "2e create water, Elemental (Acqua)."),
    s("Cure Wounds", 1, "Evocation", ["Healing"], "fonte", "2e cure light wounds."),
    s("Detect Evil and Good", 1, "Divination", ["All"], "fonte", "2e detect evil."),
    s("Detect Magic", 1, "Divination", ["Divination"], "fonte"),
    s("Detect Poison and Disease", 1, "Divination", ["Divination"], "fonte"),
    s("Guiding Bolt", 1, "Evocation", ["Combat"], "nostra",
      "Nessun antenato 2e. Classificato per effetto: attacco a distanza radiante."),
    s("Healing Word", 1, "Evocation", ["Healing"], "nostra",
      "La 2e non ha cure ad azione bonus. Famiglia cure, sfera Healing."),
    s("Inflict Wounds", 1, "Necromancy", ["Healing"], "fonte",
      "2e cause light wounds e' la forma INVERSA di cure light wounds: sfera "
      "Healing. E' la ragione della nota di Chemosh."),
    s("Protection from Evil and Good", 1, "Abjuration", ["Protection"], "fonte"),
    s("Purify Food and Drink", 1, "Transmutation", ["All"], "fonte"),
    s("Sanctuary", 1, "Abjuration", ["Protection"], "fonte"),
    s("Shield of Faith", 1, "Abjuration", ["Protection"], "nostra"),

    # ---- 2° livello ----
    s("Aid", 2, "Abjuration", ["Necromantic"], "fonte", "2e aid, sfera Necromantic."),
    s("Augury", 2, "Divination", ["Divination"], "fonte"),
    s("Blindness/Deafness", 2, "Necromancy", ["Necromantic"], "fonte",
      "2e cause blindness, inverso di cure blindness."),
    s("Calm Emotions", 2, "Enchantment", ["Charm"], "fonte", "2e remove fear."),
    s("Continual Flame", 2, "Evocation", ["Sun"], "fonte", "2e continual light."),
    s("Enhance Ability", 2, "Transmutation", ["All"], "nostra",
      "Nessun antenato sacerdotale. Potenziamento generico: assegnato ad All."),
    s("Find Traps", 2, "Divination", ["Divination"], "fonte"),
    s("Gentle Repose", 2, "Necromancy", ["Necromantic"], "fonte"),
    s("Hold Person", 2, "Enchantment", ["Charm"], "fonte"),
    s("Lesser Restoration", 2, "Abjuration", ["Healing", "Necromantic"], "fonte",
      "2e slow poison (Healing) e cure disease (Necromantic)."),
    s("Locate Object", 2, "Divination", ["Divination"], "fonte"),
    s("Prayer of Healing", 2, "Evocation", ["Healing"], "fonte"),
    s("Protection from Poison", 2, "Abjuration", ["Healing", "Protection"], "fonte",
      "2e neutralize poison, sfera Healing."),
    s("Silence", 2, "Illusion", ["Guardian"], "fonte",
      "2e silence 15' radius, sfera Guardian."),
    s("Spiritual Weapon", 2, "Evocation", ["Combat"], "fonte", "2e spiritual hammer."),
    s("Warding Bond", 2, "Abjuration", ["Protection", "Guardian"], "nostra"),
    s("Zone of Truth", 2, "Enchantment", ["Divination"], "fonte", "2e detect lie."),

    # ---- 3° livello ----
    s("Animate Dead", 3, "Necromancy", ["Necromantic"], "fonte"),
    s("Beacon of Hope", 3, "Abjuration", ["Healing"], "nostra"),
    s("Bestow Curse", 3, "Necromancy", ["Protection", "Necromantic"], "fonte",
      "Inverso di remove curse, che in 2e e' sfera Protection."),
    s("Clairvoyance", 3, "Divination", ["Divination"], "fonte"),
    s("Create Food and Water", 3, "Conjuration", ["Creation"], "fonte"),
    s("Daylight", 3, "Evocation", ["Sun"], "fonte"),
    s("Dispel Magic", 3, "Abjuration", ["All"], "fonte",
      "2e dispel magic e' sfera All: ogni sacerdote lo ha."),
    s("Glyph of Warding", 3, "Abjuration", ["Guardian"], "fonte"),
    s("Magic Circle", 3, "Abjuration", ["Protection"], "fonte",
      "2e protection from evil 10' radius."),
    s("Mass Healing Word", 3, "Evocation", ["Healing"], "nostra"),
    s("Meld into Stone", 3, "Transmutation", ["Elemental"], "fonte",
      "2e meld into stone, Elemental (Terra)."),
    s("Protection from Energy", 3, "Abjuration", ["Protection"], "fonte",
      "2e protection from fire e protection from lightning."),
    s("Remove Curse", 3, "Abjuration", ["Protection"], "fonte"),
    s("Revivify", 3, "Conjuration", ["Necromantic"], "nostra"),
    s("Sending", 3, "Evocation", ["Divination"], "nostra"),
    s("Speak with Dead", 3, "Necromancy", ["Necromantic"], "fonte"),
    s("Spirit Guardians", 3, "Conjuration", ["Combat"], "nostra"),
    s("Tongues", 3, "Divination", ["Divination"], "fonte"),
    s("Water Walk", 3, "Transmutation", ["Elemental"], "fonte",
      "2e water walk, Elemental (Acqua)."),

    # ---- 4° livello ----
    s("Banishment", 4, "Abjuration", ["Summoning"], "fonte",
      "2e abjure, sfera Summoning."),
    s("Control Water", 4, "Transmutation", ["Elemental"], "fonte",
      "2e lower water e part water."),
    s("Death Ward", 4, "Abjuration", ["Necromantic", "Protection"], "fonte",
      "2e negative plane protection, sfera Necromantic."),
    s("Divination", 4, "Divination", ["Divination"], "fonte"),
    s("Freedom of Movement", 4, "Abjuration", ["Charm"], "fonte",
      "2e free action e' nella sfera Charm, non in Protection."),
    s("Guardian of Faith", 4, "Conjuration", ["Guardian"], "nostra"),
    s("Locate Creature", 4, "Divination", ["Divination"], "fonte"),
    s("Stone Shape", 4, "Transmutation", ["Elemental"], "fonte"),

    # ---- 5° livello ----
    s("Commune", 5, "Divination", ["Divination"], "fonte"),
    s("Contagion", 5, "Necromancy", ["Necromantic"], "fonte",
      "2e cause disease, inverso di cure disease."),
    s("Dispel Evil and Good", 5, "Abjuration", ["Protection"], "fonte",
      "2e dispel evil."),
    s("Flame Strike", 5, "Evocation", ["Combat"], "fonte"),
    s("Geas", 5, "Enchantment", ["Charm"], "fonte", "2e quest."),
    s("Greater Restoration", 5, "Abjuration", ["Necromantic"], "fonte",
      "2e restoration, sfera Necromantic. NON Healing: e' il punto in cui la "
      "fonte e l'intuizione divergono."),
    s("Hallow", 5, "Evocation", ["Guardian", "Protection"], "nostra"),
    s("Insect Plague", 5, "Conjuration", ["Combat", "Animal"], "fonte",
      "2e insect plague, sfera Combat; la componente Animal e' nostra."),
    s("Legend Lore", 5, "Divination", ["Divination"], "nostra"),
    s("Mass Cure Wounds", 5, "Conjuration", ["Healing"], "fonte"),
    s("Planar Binding", 5, "Abjuration", ["Summoning"], "nostra"),
    s("Raise Dead", 5, "Necromancy", ["Necromantic"], "fonte"),
    s("Scrying", 5, "Divination", ["Divination"], "fonte"),

    # ---- 6° livello ----
    s("Blade Barrier", 6, "Evocation", ["Combat"], "fonte"),
    s("Create Undead", 6, "Necromancy", ["Necromantic"], "fonte"),
    s("Find the Path", 6, "Divination", ["Divination"], "fonte"),
    s("Forbiddance", 6, "Abjuration", ["Guardian"], "nostra"),
    s("Harm", 6, "Necromancy", ["Healing"], "fonte",
      "2e harm e' la forma inversa di heal: sfera Healing."),
    s("Heal", 6, "Evocation", ["Healing"], "fonte"),
    s("Heroes' Feast", 6, "Conjuration", ["Creation"], "fonte"),
    s("Planar Ally", 6, "Conjuration", ["Summoning"], "fonte",
      "2e aerial servant e conjure animals, sfera Summoning."),
    s("True Seeing", 6, "Divination", ["Divination"], "fonte"),
    s("Word of Recall", 6, "Conjuration", ["Summoning"], "fonte"),

    # ---- 7° livello ----
    s("Conjure Celestial", 7, "Conjuration", ["Summoning"], "nostra"),
    s("Divine Word", 7, "Evocation", ["Combat"], "fonte", "2e holy word."),
    s("Etherealness", 7, "Transmutation", ["Astral"], "nostra"),
    s("Fire Storm", 7, "Evocation", ["Elemental"], "fonte",
      "2e fire storm, Elemental (Fuoco)."),
    s("Plane Shift", 7, "Conjuration", ["Astral"], "fonte"),
    s("Regenerate", 7, "Transmutation", ["Necromantic"], "fonte"),
    s("Resurrection", 7, "Necromancy", ["Necromantic"], "fonte"),
    s("Symbol", 7, "Abjuration", ["Guardian"], "fonte"),

    # ---- 8° livello ----
    s("Antimagic Field", 8, "Abjuration", ["Protection"], "nostra"),
    s("Control Weather", 8, "Transmutation", ["Weather"], "fonte"),
    s("Earthquake", 8, "Evocation", ["Elemental"], "fonte",
      "2e earthquake, Elemental (Terra)."),
    s("Holy Aura", 8, "Abjuration", ["Sun", "Protection"], "nostra"),

    # ---- 9° livello ----
    s("Astral Projection", 9, "Necromancy", ["Astral"], "fonte", "2e astral spell."),
    s("Gate", 9, "Conjuration", ["Summoning"], "fonte"),
    s("Mass Heal", 9, "Conjuration", ["Healing"], "nostra"),
    s("True Resurrection", 9, "Necromancy", ["Necromantic"], "nostra"),
]

# --------------------------------------------------------------------------
# Incantesimi di DOMINIO dell'SRD 5.1. Non passano dal filtro delle sfere:
# si ottengono col Dominio e sono sempre preparati. Elencati per completezza
# e per poter dire quanto un Dominio compensa una sfera assente.
# --------------------------------------------------------------------------
DOMINI_SRD = {
    "Knowledge": ["Command", "Identify", "Augury", "Suggestion", "Nondetection",
                  "Speak with Dead", "Arcane Eye", "Confusion", "Legend Lore",
                  "Scrying"],
    "Life": ["Bless", "Cure Wounds", "Lesser Restoration", "Spiritual Weapon",
             "Beacon of Hope", "Revivify", "Death Ward", "Guardian of Faith",
             "Mass Cure Wounds", "Raise Dead"],
    "Light": ["Burning Hands", "Faerie Fire", "Flaming Sphere", "Scorching Ray",
              "Daylight", "Fireball", "Guardian of Faith", "Wall of Fire",
              "Flame Strike", "Scrying"],
    "Nature": ["Animal Friendship", "Speak with Animals", "Barkskin",
               "Spike Growth", "Plant Growth", "Wind Wall", "Dominate Beast",
               "Grasping Vine", "Insect Plague", "Tree Stride"],
    "Tempest": ["Fog Cloud", "Thunderwave", "Gust of Wind", "Shatter",
                "Call Lightning", "Sleet Storm", "Control Water", "Ice Storm",
                "Destructive Wave", "Insect Plague"],
    "Trickery": ["Charm Person", "Disguise Self", "Mirror Image",
                 "Pass without Trace", "Blink", "Dispel Magic", "Dimension Door",
                 "Polymorph", "Dominate Person", "Modify Memory"],
    "War": ["Divine Favor", "Shield of Faith", "Magic Weapon", "Spiritual Weapon",
            "Crusader's Mantle", "Spirit Guardians", "Freedom of Movement",
            "Stoneskin", "Flame Strike", "Hold Monster"],
}

# --------------------------------------------------------------------------
# DECISIONE 24 — Dominio 5e associato a ciascuna divinita'.
# Il Dominio non sostituisce le sfere: fornisce Incanalare Divinita' e i
# privilegi di sottoclasse, senza i quali il chierico 5e non ha nulla ai
# livelli 1, 2, 6, 8 e 17.
# Scelto sul Dominio 2014 piu' coerente con il portafoglio della divinita'.
# --------------------------------------------------------------------------
DOMINIO = {
    "branchala":  ("Life",      "Dio della musica e della vita; sfere Healing e Creation maggiori."),
    "chemosh":    ("Death",     "Signore dei non morti. Il Dominio Morte non e' nell'SRD 5.1: "
                                "e' del DMG. Segnalato, non risolto."),
    "chislev":    ("Nature",    "Dea della natura selvaggia; Animal, Plant, Weather ed Elemental maggiori."),
    "gilean":     ("Knowledge", "Il Libro; Divinazione maggiore e ruolo di archivista del mondo."),
    "habbakuk":   ("Nature",    "Re Pescatore; Animal ed Elemental maggiori."),
    "hiddukel":   ("Trickery",  "Principe delle Menzogne. Tre sole sfere: e' il caso piu' povero."),
    "kiri-jolith": ("War",      "Spada della Giustizia; Combat maggiore. E' il dio che concede "
                                "gli incantesimi ai Cavalieri della Spada."),
    "lunitari":   ("Knowledge", "Luna della magia neutrale; Divination e Astral maggiori."),
    "majere":     ("Knowledge", "Maestro della Mente; Charm, Divination e Astral maggiori."),
    "mishakal":   ("Life",      "Mano Guaritrice; otto sfere maggiori fra cui Healing."),
    "morgion":    ("Death",     "Vento Nero, dio della malattia. Stesso problema di Chemosh: "
                                "il Dominio Morte non e' nell'SRD."),
    "nuitari":    ("Knowledge", "Luna della magia nera; Divination e Astral maggiori."),
    "paladine":   ("Life",      "Signore dei Draghi; Healing, Protection e Sun maggiori."),
    "reorx":      ("Forge",     "La Forgia. Il Dominio Forgia non e' nell'SRD 5.1: e' di "
                                "Xanathar. Alternativa dentro l'SRD: Guerra. Segnalato."),
    "sargonnas":  ("War",       "Vendetta Oscura; Combat maggiore."),
    "shinare":    ("Trickery",  "Vittoria Alata, dea del commercio. Nessun Dominio 2014 copre "
                                "il commercio: Inganno e' un ripiego. Segnalato."),
    "sirrion":    ("Light",     "Fiamma Fluente; Elemental (Fuoco) e Combat maggiori."),
    "solinari":   ("Light",     "Luna della magia bianca; Combat e Divination maggiori."),
    "takhisis":   ("Trickery",  "Regina delle Tenebre. Il Dominio Morte sarebbe piu' coerente "
                                "ma non e' nell'SRD."),
    "zeboim":     ("Tempest",   "Mare Oscuro; Weather ed Elemental (Acqua) maggiori."),
    "zivilyn":    ("Knowledge", "Albero del Mondo; Divination e Astral maggiori, cinque sfere "
                                "tutte maggiori e nessuna minore."),
}

# Domini citati sopra che NON stanno nell'SRD 5.1.
DOMINI_FUORI_SRD = {"Death": "DMG 2014", "Forge": "Xanathar's Guide"}


def accessibili(sfere_divinita):
    """
    Incantesimi accessibili a una divinita'.
    sfere_divinita: lista di (nome_sfera, 'major'|'minor').
    Regola 2e: accesso minore = solo fino al 3° livello di incantesimo.
    I trucchetti seguono la sfera come gli altri: accessibili con entrambi.
    """
    maggiori = {norm(n) for n, a in sfere_divinita if a == "major"}
    minori = {norm(n) for n, a in sfere_divinita if a != "major"}
    out = []
    for inc in LISTA_BASE:
        sf = set(inc["spheres"])
        if sf & maggiori:
            out.append((inc, "major"))
        elif sf & minori and inc["level"] <= 3:
            out.append((inc, "minor"))
    return out
