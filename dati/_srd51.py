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

COSA C'E' DA OGGI, E PERCHE' L'INTESTAZIONE SOPRA NON BASTAVA PIU'
    02/09/2026. Fino a ieri questo file conteneva SOLO la colonna Features,
    cioe' i NOMI dei privilegi livello per livello, e lo dichiarava. Il
    RAPPORTO-personaggio (§2.1) ha misurato cosa significa: «"clonato" oggi
    vuol dire abbiamo registrato quali privilegi ha il Fighter, non abbiamo
    le regole del Fighter» — il rapporto fra un indice e un testo. E ha
    registrato la conseguenza che conta: azzerando anche tutti e 40 i
    privilegi `pending` di Krynn, un Cavaliere della Corona resterebbe
    ingiocabile, perche' gli mancano i privilegi del **Fighter**, che non
    sono `pending` — non sono mai stati contati.

    Da qui in avanti il file porta anche COMPETENZE e PRIVILEGI, per la sola
    parte esercitata dalla prima fetta verticale. Restano dei nomi tutti gli
    altri: il criterio e' che un privilegio si scrive quando un caso lo usa,
    non per riempire la tabella.

    La prosa e' NOSTRA, in italiano, non il testo SRD ricopiato: le regole
    sono fatti e si descrivono con parole proprie (CLAUDE.md 1). Accanto a
    ogni prosa c'e' `effetto`, la stessa regola in campi, nella forma di
    dati/schema/effetto.schema.json, e dati/valida_effetti.py verifica che
    le due dicano la stessa cosa.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _sistema  # noqa: E402

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

# Bonus di competenza: identico per tutte le classi, e LETTO dalla sua sede
# unica, `dati/sistema/bonus-competenza.json`. Fino al 02/09/2026 la formula
# stava scritta qui e una seconda volta in `dati/valida_effetti.py`, in due
# file che nessuna esecuzione metteva uno contro l'altro: meta' della nona
# struttura doppia del progetto, e la prima che vivesse nel codice.
# Il nome resta, perche' i consumatori sono molti; cio' che cambia e' da
# dove viene il numero. Decisione 51 (`criterio-meccanica`).
COMPETENZA = {l: _sistema.competenza(l) for l in range(1, 21)}

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


# --------------------------------------------------------------------------
# COMPETENZE del chassis, SRD 5.1.
#
# Il buco che chiudono e' quello di RAPPORTO-personaggio §2.4: nei dati c'e'
# il sistema a SLOT della 2e (42 voci d'arma, 66 non-d'arma) che
# l'incompatibilita' 4 della decisione 23 (`principio-del-clone`) ha abolito,
# e del sistema che l'ha sostituito non c'era nulla. La nota della stessa
# incompatibilita' dichiarava "competenza per categoria" e poi non scriveva
# nessuna categoria: una regola annunciata e mai messa in un campo.
#
# Le categorie d'arma e d'armatura a cui questi valori si riferiscono sono
# quelle di `weapon_5e.categoria` e `armor_5e.categoria` in dati/oggetti/.
# I due estremi combaciano per costruzione, e valida_effetti.py lo verifica:
# una competenza che nominasse una categoria inesistente sarebbe una
# competenza in niente.
# --------------------------------------------------------------------------
COMPETENZE = {
    "Fighter": {
        "armature": ["leggera", "media", "pesante", "scudo"],
        "armi": ["semplice", "da_guerra"],
        "strumenti": [],
        "tiri_salvezza": ["str", "con"],
        "abilita": {
            "quante": 2,
            "fra": ["Acrobazia", "Addestrare Animali", "Atletica", "Storia",
                    "Intuizione", "Intimidire", "Percezione", "Sopravvivenza"],
        },
    },
}

# Categorie ammesse, per il controllo incrociato con dati/oggetti/.
CATEGORIE_ARMA = ("semplice", "da_guerra")
CATEGORIE_ARMATURA = ("leggera", "media", "pesante", "scudo")


# --------------------------------------------------------------------------
# PRIVILEGI del chassis, con la meccanica e non solo il nome.
#
# Solo quelli che la prima fetta verticale esercita davvero: i tre del
# Fighter ai livelli 1 e 2. Sono i privilegi che un Cavaliere della Corona
# ha al grado d'ingresso, e sono esattamente quelli che la fonte di Krynn
# NON gli da': il manuale gli concede un permesso (la specializzazione
# nelle armi 2e, `source_only`) e un impedimento sociale, cioe' zero
# privilegi utilizzabili in combattimento. Senza questi tre, il grado
# d'ingresso dell'ordine solamnico entra in un'arena con un tiro d'attacco
# e nient'altro.
# --------------------------------------------------------------------------
PRIVILEGI = {
    ("Fighter", "Fighting Style"): {
        "nome_it": "Stile di combattimento",
        "livello": 1,
        "prosa": "Al 1° livello si adotta uno stile di combattimento fra "
                 "quelli disponibili alla classe. Lo stesso stile non si "
                 "puo' scegliere due volte.",
        "effetto": {
            "azione": "nessuna",
            "scelta": {
                "quante": 1,
                "fra": ["arciere", "difesa", "duello", "arma-grande",
                        "protezione", "due-armi"],
                "ripetibile": False,
            },
            "nota": "SEDE PROVVISORIA, DICHIARATA — stessa forma del rinvio "
                    "della decisione 41 (`sconfessione-condivisa`). Qui c'e' "
                    "il FILTRO, non il campione: la "
                    "decisione 35 (`repertori-sono-filtri`) ha gia' stabilito "
                    "che e' cosi' "
                    "che si registra una fonte che offre una scelta. Ma i sei "
                    "stili non hanno ancora una sede propria dove portare "
                    "ciascuno il proprio effetto, e finche' non ce l'hanno "
                    "un motore sa che va scelto uno stile e non sa cosa "
                    "faccia. Due dei sei sono resi qui sotto in "
                    "`STILI_COMBATTIMENTO` perche' la fetta li esercita; gli "
                    "altri quattro sono nomi. Quando la sede esistera', "
                    "questi id diventeranno riferimenti a essa: un blocco da "
                    "spostare, non una riscrittura.",
        },
    },
    ("Fighter", "Second Wind"): {
        "nome_it": "Recuperare il fiato",
        "livello": 1,
        "prosa": "Con un'azione bonus si recuperano punti ferita pari a 1d10 "
                 "piu' il proprio livello da guerriero. Va poi completato un "
                 "riposo breve o lungo prima di poterlo rifare.",
        "effetto": {
            "azione": "azione_bonus",
            "guarigione": {"dadi": "1d10", "piu_livello_classe": True,
                           "bonus": None},
            "risorsa": {"usi": 1, "ricarica": "riposo_breve", "nota": None},
        },
    },
    ("Fighter", "Action Surge"): {
        "nome_it": "Impeto d'azione",
        "livello": 2,
        "prosa": "Nel proprio turno si puo' compiere un'azione aggiuntiva, "
                 "oltre a quella normale e all'eventuale azione bonus. Va poi "
                 "completato un riposo breve o lungo prima di poterlo rifare. "
                 "Dal 17° livello gli usi diventano due, ma resta un solo uso "
                 "per turno.",
        "effetto": {
            "azione": "nessuna",
            "risorsa": {
                "usi": {"per_livello": {str(l): (2 if l >= 17 else 1)
                                        for l in range(2, 21)}},
                "ricarica": "riposo_breve",
                "nota": "Un solo uso per turno anche quando se ne hanno due.",
            },
            "modificatori": [
                {"bersaglio": "azioni_per_turno", "valore": 1,
                 "condizione_di_applicazione": "nel turno in cui viene usato"},
            ],
        },
    },
}

# I due stili che la fetta esercita davvero: un Cavaliere della Corona porta
# armatura e ha lancia e spada corta obbligate dalla fonte, quindi Difesa e
# Duello sono gli unici due che puo' applicare a quell'equipaggiamento.
# Arciere, Arma grande, Protezione e Combattere con due armi restano NOMI:
# scriverli senza un caso che li usi e' il modo in cui un dato entra senza
# essere verificato.
STILI_COMBATTIMENTO = {
    "difesa": {
        "nome_it": "Difesa",
        "prosa": "Finche' si indossa un'armatura si ottiene +1 alla Classe "
                 "Armatura.",
        "effetto": {
            "azione": "nessuna",
            "modificatori": [
                {"bersaglio": "ca", "valore": 1,
                 "condizione_di_applicazione": "mentre si indossa un'armatura"},
            ],
        },
    },
    "duello": {
        "nome_it": "Duello",
        "prosa": "Quando si impugna un'arma da mischia in una mano sola e "
                 "nessun'altra arma, si ottiene +2 ai tiri per i danni con "
                 "quell'arma.",
        "effetto": {
            "azione": "nessuna",
            "modificatori": [
                {"bersaglio": "danno", "valore": 2,
                 "condizione_di_applicazione": "arma da mischia in una mano "
                                               "sola, nessun'altra arma "
                                               "impugnata"},
            ],
        },
    },
}

STILI_SENZA_EFFETTO = ("arciere", "arma-grande", "protezione", "due-armi")


def privilegi_chassis(srd_class):
    """I privilegi del chassis di cui si ha la meccanica, non solo il nome."""
    return {nome: dati for (cls, nome), dati in PRIVILEGI.items()
            if cls == srd_class}
