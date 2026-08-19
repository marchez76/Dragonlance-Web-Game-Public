#!/usr/bin/env python3
"""
DECISIONE 23 — il principio del clone.

    Per le classi la fedelta' alla fonte non basta. Le razze 2e sono ricche e
    la trascrizione integrale ha prodotto voci piene; le classi 2e sono povere,
    e trascriverle fedelmente produce diciassette gusci vuoti.

    Ogni classe di Krynn e' un CLONE MECCANICO della classe base 5e
    corrispondente — dado vita, attacchi extra, aumenti di caratteristica,
    competenze, tutto identico — con innestati sopra i privilegi e le
    restrizioni della fonte ai livelli previsti.

    Non si inventa nulla: si copia il chassis dall'SRD 5.1 e ci si appoggia
    sopra la fonte.

CINQUE CLASSI RESTANO SENZA CHASSIS
    Popolano, Tinker, Sacerdote Eretico, Handler e Marinaio. Il rapporto le
    aveva segnalate come prive di candidato pulito e la decisione 23 le lascia
    esplicitamente indecise. Restano `in_sospeso`: proposte nel rapporto,
    nessuna applicata.

LE SETTE INCOMPATIBILITA' STRUTTURALI
    Discendono dalla scelta della 5e come chassis e sono applicate qui, in un
    punto solo, uguali per tutte le classi. Il dato 2e non viene cancellato:
    resta in `source_2e`.
"""

import _srd51 as R

DEC = "DECISIONE 23"

# --------------------------------------------------------------------------
# Chassis per classe. `None` = nessun candidato pulito, lasciato indeciso.
# --------------------------------------------------------------------------
CHASSIS = {
    "barbaro": ("Fighter",
                "NON Barbarian: l'Ira e' un'invenzione della 3e, assente sia da "
                "Krynn sia dal kit del 1989 da cui il Barbaro di Ansalon "
                "discende. Confermato dall'appendice di RAPPORTO-classi.md."),
    "cavaliere-corona": ("Fighter",
                         "Guerriero puro, nessuna magia al primo grado. La "
                         "sequenza verso Spada e Rosa (decisione 5) si innesta "
                         "sopra il chassis."),
    "cavaliere-spada": ("Paladin",
                        "La fonte dice esplicitamente \"capacita' della classe "
                        "Paladino al proprio livello\" e concede incantesimi "
                        "sacerdotali dal 6°. E' l'accoppiamento piu' pulito del "
                        "roster."),
    "cavaliere-rosa": ("Paladin",
                       "Prosegue il grado precedente. L'immunita' alla paura e' "
                       "gia' un privilegio del Paladino (Aura di Coraggio)."),
    "cavaliere": ("Fighter",
                  "Sei privilegi tutti di combattimento montato e reputazione. "
                  "In SRD l'unico archetipo marziale e' il Campione: il montato "
                  "resta scoperto e il codice comportamentale pure."),
    "mago-alta-stregoneria": ("Wizard", "Corrispondenza diretta."),
    "mago-rinnegato": ("Wizard",
                       "Stesso chassis, definito per sottrazione: e' il Mago "
                       "dell'Alta Stregoneria senza vincoli e senza bonus lunari."),
    "mago-veste-bianca": (None, "AFFILIAZIONE, non classe (decisione 6)."),
    "mago-veste-nera": (None, "AFFILIAZIONE, non classe (decisione 6)."),
    "mago-veste-rossa": (None, "AFFILIAZIONE, non classe (decisione 6)."),
    "sacerdote-ordini-sacri": ("Cleric",
                               "Corrispondenza diretta. Le sfere gia' estratte "
                               "diventano il filtro della decisione 24; il "
                               "Dominio resta come sottoclasse."),
    "con-artist": ("Rogue",
                   "Le quattro abilita' potenziate diventano competenze ed "
                   "Esperienza."),
    # ---- lasciate indecise dalla decisione 23 ----
    "commoner": (None, "Non e' una classe 5e. Da decidere."),
    "tinker": (None, "Non e' una classe 5e. Da decidere."),
    "sacerdote-eretico": (None, "Per definizione non ha potere. Da decidere."),
    "handler": (None, "Rogue senza attacco furtivo: il chassis c'e' ma svuotato. "
                      "Da decidere."),
    "mariner": (None, "Ibrido Fighter/Rogue: nessun candidato pulito. Da decidere."),
}

# Tutti i chassis usati sono trascritti in _srd51.py: Fighter, Wizard, Cleric,
# Paladin, Rogue.

# --------------------------------------------------------------------------
# Stato di conversione dei privilegi di fonte.
# Default: `pending`. La decisione 23 autorizza il clone del chassis, non
# l'invenzione di meccanica 5e per i privilegi: quella resta da fare.
# --------------------------------------------------------------------------
STATO_PRIVILEGI = {
    ("cavaliere-corona", "Specializzazione nelle armi"): (
        "source_only",
        "Stesso criterio della decisione 17.10 sul Minotauro: la fonte non "
        "concede un beneficio ma un PERMESSO — la facolta' di usare un "
        "sottosistema 2e ristretto. In un sistema che quel sottosistema non ce "
        "l'ha, il permesso non vale nulla. CONSEGUENZA REGISTRATA: il grado "
        "d'ingresso dell'intero ordine solamnico resta a ZERO privilegi "
        "dichiarati dalla fonte. Non e' un errore da correggere: e' cio' che "
        "dice il manuale, ed e' la ragione per cui serve la decisione 23."),
    ("cavaliere-spada", "Capacita' del paladino"): (
        "direct",
        "Assorbito dal chassis: se la classe E' un Paladino, il privilegio "
        "coincide con la classe stessa e non va convertito a parte."),
    ("cavaliere-rosa", "Immunita' alla paura"): (
        "direct",
        "Aura di Coraggio del Paladino, SRD 5.1, 10° livello. Il chassis lo "
        "concede gia'; resta da decidere se anticiparlo al 4°, che e' il "
        "livello d'ingresso del grado."),
}

DEFAULT_PRIVILEGIO = (
    "pending",
    "La decisione 23 autorizza il clone del chassis, non l'invenzione di "
    "meccanica 5e per i privilegi della fonte. Da convertire.")


def stato(class_id, nome):
    return STATO_PRIVILEGI.get((class_id, nome), DEFAULT_PRIVILEGIO)


# --------------------------------------------------------------------------
# LE SETTE INCOMPATIBILITA' STRUTTURALI, applicate uguali per tutti.
# --------------------------------------------------------------------------
def incompatibilita(c):
    s = c["s2e"]
    prog = s.get("progression") or []
    max_2e = max((p["level"] for p in prog), default=None)
    titoli = [{"level": p["level"], "title": p["title"]}
              for p in prog if p.get("title")]
    gruppo = c["group"]

    # 3 — le cinque categorie 2e mappate sulle sei caratteristiche.
    MAPPA_TS = {
        "Paralisi/Veleno/Magia della Morte": "con",
        "Bacchette/Bastoni/Verghe": "dex",
        "Pietrificazione/Polimorfismo": "con",
        "Soffio": "dex",
        "Incantesimi": "wis",
    }
    # Le due competenze coerenti col gruppo 2e: il gruppo che in 2e era forte
    # su una categoria diventa competente nella caratteristica corrispondente.
    COMPETENZE_GRUPPO = {
        "Warrior": ["str", "con"],
        "Wizard": ["int", "wis"],
        "Priest": ["wis", "cha"],
        "Rogue": ["dex", "int"],
        "Normal": ["dex", "con"],
    }
    wp = s.get("weapon_proficiencies") or {}

    return {
        "xp_table": {
            "applied": False,
            "note": "INCOMPATIBILITA' 1. Tabella unica 5e per tutti. Le "
                    "progressioni 2e restano in source_2e come dato storico: "
                    + (f"{len(prog)} livelli trascritti." if prog else
                       f"questa classe non ne aveva una propria, rimandava al gruppo {gruppo}."),
        },
        "attack_progression": {
            "system": "proficiency_bonus",
            "values": R.COMPETENZA,
            "note": "INCOMPATIBILITA' 2. Il THAC0 per gruppo sparisce: il bonus "
                    "di competenza e' uguale per chiunque. La differenza fra "
                    "gruppi si esprime con Attacco Extra e competenze.",
        },
        "saving_throws": {
            "system": "ability_saves_5e",
            "mapping_2e": MAPPA_TS,
            "proficient": COMPETENZE_GRUPPO[gruppo],
            "note": "INCOMPATIBILITA' 3. Le cinque categorie 2e sono mappate "
                    "sulle sei caratteristiche; le due competenze discendono "
                    f"dal gruppo 2e ({gruppo}).",
        },
        "weapon_proficiencies": {
            "system": "categorie_5e",
            "forced_equipment": wp.get("required") or [],
            "note": "INCOMPATIBILITA' 4. Gli slot di competenza spariscono: "
                    "competenza per categoria. Le armi obbligate della fonte "
                    "diventano equipaggiamento iniziale imposto, non slot.",
        },
        "starting_equipment": {
            "system": "pacchetto_fisso_5e",
            "source_wealth": s.get("starting_wealth"),
            "constraints": s.get("equipment_rules") or [],
            "note": "INCOMPATIBILITA' 5. Pacchetto fisso 5e. Le regole di "
                    "equipaggiamento della fonte diventano vincoli sul "
                    "pacchetto, non sul tiro della ricchezza.",
        },
        "level_cap": {
            "value": 20,
            "source_max": max_2e,
            "note": "INCOMPATIBILITA' 6. Troncamento al 20°. "
                    + (f"La fonte arrivava al {max_2e}°: i {max_2e - 20} livelli in piu' "
                       f"restano in source_2e." if max_2e and max_2e > 20 else
                       "Questa classe non aveva una tabella propria."),
        },
        "titles": {
            "descriptive_only": True,
            "values": titoli,
            "note": "INCOMPATIBILITA' 7. I titoli di livello si conservano come "
                    "dato descrittivo, mostrati nella scheda, senza effetto "
                    f"meccanico. {len(titoli)} titoli trascritti.",
        },
    }


def chassis(c):
    srd, motivo = CHASSIS[c["id"]]
    if srd is None:
        return {
            "srd_class": None,
            "status": "in_sospeso",
            "note": f"{DEC}. Nessun chassis applicato: {motivo}",
            "hit_die": None,
            "saving_throws": None,
            "features_from": None,
        }
    tab = R.TABELLE.get(srd)
    return {
        "srd_class": srd,
        "status": "clonato",
        "note": f"{DEC}. {motivo}",
        "hit_die": tab["hit_dice"] if tab else None,
        "saving_throws": tab["saves"].split(", ") if tab else None,
        "features_from": f"SRD 5.1 — {srd}",
        "table_transcribed": srd in R.TABELLE,
        "table_note": None if srd in R.TABELLE else
                      f"Tabella {srd} non ancora trascritta in _srd51.py: "
                      f"il chassis e' deciso, i privilegi livello per livello no.",
    }
