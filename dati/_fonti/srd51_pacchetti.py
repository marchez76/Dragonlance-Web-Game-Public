#!/usr/bin/env python3
"""
SRD 5.1 (CC-BY 4.0) — equipaggiamento iniziale di classe e pacchetti.

PERCHE' STA QUI, E COSA NON DECIDE
    `dati/_fonti/srd51_equipaggiamento.py` copre il LISTINO: armi, armature e
    l'attrezzatura che serve a combattere ed esplorare. Non copre cio' con cui
    un personaggio COMINCIA, che nella 5e e' una cosa distinta: ogni classe ha
    un elenco di scelte, e una di esse e' quasi sempre un «pacchetto», cioe'
    un insieme gia' composto che il manuale stampa a parte.

    Questo modulo trascrive quei due dati e basta. NON sceglie fra le due
    strade dell'equipaggiamento iniziale — pacchetto fisso o borsello da
    spendere — e non ne implementa nessuna: serve a MISURARE cosa costa
    ciascuna, che e' cio' che `dati/analizza_equipaggiamento.py` fa. La
    trascrizione e' utile in entrambi i casi, perche' anche la strada del
    borsello vuole a catalogo le voci che oggi mancano.

FONTE
    api.open5e.com, lo stesso dominio gia' usato per mostri, incantesimi ed
    equipaggiamento (RETE-domini-permessi.md). Due endpoint:
    - /v1/classes/?document__slug=wotc-srd, campo `equipment`: l'elenco di
      scelte che l'SRD stampa sotto ciascuna classe. Trascritto qui in campi
      per le SOLE cinque classi che ci servono, cioe' i cinque chassis che
      `dati/_chassis_5e.py` usa davvero.
    - /v1/sections/?document__slug=wotc-srd, sezione «Equipment Packs»: il
      contenuto dei sette pacchetti.
    Letti il 05/09/2026.

DUE FATTI DI FONTE CHE VALE LA PENA REGISTRARE, perche' cambiano il conto
    1. ALCUNI INGREDIENTI DEI PACCHETTI NON SONO VOCI DI LISTINO. Il testo dei
       pacchetti nomina cose che la tabella Adventuring Gear non elenca:
       spago, cassetta delle elemosine, blocchi d'incenso, turibolo, paramenti,
       un sacchettino di sabbia, un coltellino. Esistono solo dentro la
       descrizione del pacchetto. Chi compone i pacchetti da noi deve
       decidere se crearle come oggetti o lasciarle dentro il pacchetto come
       testo: e' una scelta, e sta segnata voce per voce con `a_listino`.
    2. L'SRD NON HA LA TABELLA DELLA RICCHEZZA INIZIALE. Il PHB 2014 stampa
       «Starting Wealth by Class» come alternativa al pacchetto; le sezioni
       dell'SRD 5.1 non la contengono (cercata il 05/09/2026 su tutte e 45).
       Per la strada del borsello, quindi, l'SRD non offre un ripiego: dove
       la fonte 2e non da' una formula, il numero va deciso.
"""

# --------------------------------------------------------------------------
# I PACCHETTI. (nome_en, costo_gp, [(quantita', voce, a_listino)])
#
# `a_listino` dice se la voce esiste nella tabella Adventuring Gear dell'SRD,
# cioe' se ha un prezzo e un peso propri. False = esiste solo dentro il testo
# del pacchetto.
# --------------------------------------------------------------------------
PACCHETTI = [
    ("Burglar's Pack", 16.0, [
        (1, "Backpack", True),
        (1, "Ball Bearings (bag of 1000)", True),
        (1, "String (10 feet)", False),
        (1, "Bell", True),
        (5, "Candle", True),
        (1, "Crowbar", True),
        (1, "Hammer", True),
        (10, "Piton", True),
        (1, "Lantern, Hooded", True),
        (2, "Lamp oil (flask)", True),
        (5, "Rations (1 day)", True),
        (1, "Tinderbox", True),
        (1, "Waterskin", True),
        (1, "Rope, hempen (50 feet)", True),
    ]),
    ("Diplomat's Pack", 39.0, [
        (1, "Chest", True),
        (2, "Case, Map or Scroll", True),
        (1, "Clothes, fine", True),
        (1, "Ink (1 ounce bottle)", True),
        (1, "Ink pen", True),
        (1, "Lamp", True),
        (2, "Lamp oil (flask)", True),
        (5, "Paper (one sheet)", True),
        (1, "Perfume (vial)", True),
        (1, "Sealing wax", True),
        (1, "Soap", True),
    ]),
    ("Dungeoneer's Pack", 12.0, [
        (1, "Backpack", True),
        (1, "Crowbar", True),
        (1, "Hammer", True),
        (10, "Piton", True),
        (10, "Torch", True),
        (1, "Tinderbox", True),
        (10, "Rations (1 day)", True),
        (1, "Waterskin", True),
        (1, "Rope, hempen (50 feet)", True),
    ]),
    ("Entertainer's Pack", 40.0, [
        (1, "Backpack", True),
        (1, "Bedroll", True),
        (2, "Clothes, costume", True),
        (5, "Candle", True),
        (5, "Rations (1 day)", True),
        (1, "Waterskin", True),
        (1, "Disguise Kit", True),
    ]),
    ("Explorer's Pack", 10.0, [
        (1, "Backpack", True),
        (1, "Bedroll", True),
        (1, "Mess Kit", True),
        (1, "Tinderbox", True),
        (10, "Torch", True),
        (10, "Rations (1 day)", True),
        (1, "Waterskin", True),
        (1, "Rope, hempen (50 feet)", True),
    ]),
    ("Priest's Pack", 19.0, [
        (1, "Backpack", True),
        (1, "Blanket", True),
        (10, "Candle", True),
        (1, "Tinderbox", True),
        (1, "Alms box", False),
        (2, "Block of incense", False),
        (1, "Censer", False),
        (1, "Vestments", False),
        (2, "Rations (1 day)", True),
        (1, "Waterskin", True),
    ]),
    ("Scholar's Pack", 40.0, [
        (1, "Backpack", True),
        (1, "Book", True),
        (1, "Ink (1 ounce bottle)", True),
        (1, "Ink pen", True),
        (10, "Parchment (one sheet)", True),
        (1, "Little bag of sand", False),
        (1, "Small knife", False),
    ]),
]


# --------------------------------------------------------------------------
# L'EQUIPAGGIAMENTO INIZIALE DELLE CINQUE CLASSI SRD che i nostri chassis
# usano. Ogni riga e' una SCELTA fra alternative; ogni alternativa e' una
# lista di voci. Le voci sono di tre generi, e la distinzione conta per il
# conto: `oggetto` e' un nome di listino, `pacchetto` un nome di PACCHETTI,
# `categoria` una scelta aperta dentro una famiglia (un'arma da guerra
# qualunque), che non e' una voce mancante ma una domanda da porre al
# giocatore.
# --------------------------------------------------------------------------
OGGETTO, PACCHETTO, CATEGORIA = "oggetto", "pacchetto", "categoria"

EQUIPAGGIAMENTO = {
    "Fighter": [
        [[(1, "Chain mail", OGGETTO)],
         [(1, "Leather", OGGETTO), (1, "Longbow", OGGETTO),
          (20, "Arrow", OGGETTO)]],
        [[(1, "arma da guerra", CATEGORIA), (1, "Shield", OGGETTO)],
         [(2, "arma da guerra", CATEGORIA)]],
        [[(1, "Crossbow, light", OGGETTO), (20, "Crossbow bolt", OGGETTO)],
         [(2, "Handaxe", OGGETTO)]],
        [[(1, "Dungeoneer's Pack", PACCHETTO)],
         [(1, "Explorer's Pack", PACCHETTO)]],
    ],
    "Rogue": [
        [[(1, "Rapier", OGGETTO)], [(1, "Shortsword", OGGETTO)]],
        [[(1, "Shortbow", OGGETTO), (1, "Quiver", OGGETTO),
          (20, "Arrow", OGGETTO)],
         [(1, "Shortsword", OGGETTO)]],
        [[(1, "Burglar's Pack", PACCHETTO)],
         [(1, "Dungeoneer's Pack", PACCHETTO)],
         [(1, "Explorer's Pack", PACCHETTO)]],
        [[(1, "Leather", OGGETTO), (2, "Dagger", OGGETTO),
          (1, "Thieves' tools", OGGETTO)]],
    ],
    "Wizard": [
        [[(1, "Quarterstaff", OGGETTO)], [(1, "Dagger", OGGETTO)]],
        [[(1, "Component Pouch", OGGETTO)],
         [(1, "focus arcano", CATEGORIA)]],
        [[(1, "Scholar's Pack", PACCHETTO)],
         [(1, "Explorer's Pack", PACCHETTO)]],
        [[(1, "Spellbook", OGGETTO)]],
    ],
    "Cleric": [
        [[(1, "Mace", OGGETTO)], [(1, "Warhammer", OGGETTO)]],
        [[(1, "Scale mail", OGGETTO)], [(1, "Leather", OGGETTO)],
         [(1, "Chain mail", OGGETTO)]],
        [[(1, "Crossbow, light", OGGETTO), (20, "Crossbow bolt", OGGETTO)],
         [(1, "arma semplice", CATEGORIA)]],
        [[(1, "Priest's Pack", PACCHETTO)],
         [(1, "Explorer's Pack", PACCHETTO)]],
        [[(1, "Shield", OGGETTO), (1, "simbolo sacro", CATEGORIA)]],
    ],
    "Paladin": [
        [[(1, "arma da guerra", CATEGORIA), (1, "Shield", OGGETTO)],
         [(2, "arma da guerra", CATEGORIA)]],
        [[(5, "Javelin", OGGETTO)],
         [(1, "arma da mischia semplice", CATEGORIA)]],
        [[(1, "Priest's Pack", PACCHETTO)],
         [(1, "Explorer's Pack", PACCHETTO)]],
        [[(1, "Chain mail", OGGETTO), (1, "simbolo sacro", CATEGORIA)]],
    ],
}


# --------------------------------------------------------------------------
# LE CINQUE SCELTE APERTE, e cosa delimita ciascuna.
#
# Non sono voci mancanti dal catalogo: sono domande da porre al giocatore,
# cioe' FILTRI nella forma della decisione 35 (`repertori-sono-filtri`) — il
# filtro delimita, la scelta avviene dopo. La decisione 62 (`pacchetto-fisso`)
# chiede di registrarle come tali invece di risolverle scegliendo una voce
# per comodita'.
#
# `filtro` e' scritto nel vocabolario del CATALOGO — `weapon_5e.categoria` e
# `weapon_5e.tipo` di `dati/oggetti/` — e non in quello inglese della fonte:
# un filtro si scrive nei termini di chi deve risolverlo, altrimenti la
# traduzione avviene in chi lo legge, cioe' in tanti posti quanti sono i
# lettori. `None` dice che il filtro esiste ma il catalogo non ha ancora
# nessun campione che lo soddisfi — e' un FILTRO SENZA CAMPIONE, lo stesso
# caso e lo stesso nome della clausola regionale in `_valuta.py`, e va detto
# invece di essere aggirato adottando tre voci al volo.
# `valida_pacchetti.py` verifica i due sensi contro il catalogo.
# --------------------------------------------------------------------------
SCELTE = {
    "arma da guerra": {
        "filtro": {"categoria": "da_guerra", "tipo": None},
        "nota": "qualunque arma da guerra, mischia o distanza",
    },
    "arma da mischia semplice": {
        "filtro": {"categoria": "semplice", "tipo": "mischia"},
        "nota": "solo mischia, e la distinzione conta: l'alternativa nella "
                "stessa riga sono cinque giavellotti",
    },
    "arma semplice": {
        "filtro": {"categoria": "semplice", "tipo": None},
        "nota": "qualunque arma semplice, mischia o distanza",
    },
    "focus arcano": {
        "filtro": None,
        "nota": "l'SRD elenca sfera, cristallo, bacchetta, verga e bastone "
                "come focus arcani, e il catalogo non ne ha adottato "
                "nessuno: e' un FILTRO SENZA CAMPIONE. Le voci stanno "
                "nell'indice SRD (Orb, Crystal, Wooden staff) e adottarle e' "
                "una scelta, non un atto dovuto — con il pacchetto fisso "
                "l'alternativa nella stessa riga, il Component Pouch, e' a "
                "catalogo, quindi la creazione non si blocca",
    },
    "simbolo sacro": {
        "filtro": None,
        "nota": "stesso caso del focus arcano: amuleto, emblema e reliquiario "
                "stanno nell'indice SRD e non nel catalogo. Qui pero' NON "
                "c'e' un'alternativa nella stessa riga — Cleric e Paladin lo "
                "ricevono insieme allo scudo o alla cotta di maglia, senza "
                "scelta — quindi e' l'unica delle cinque che lascia un buco "
                "vero dentro un pacchetto",
    },
}


def voci_di_pacchetto():
    """{nome_pacchetto: [(quantita', voce, a_listino)]}"""
    return {nome: voci for nome, _costo, voci in PACCHETTI}


def costi():
    return {nome: costo for nome, costo, _voci in PACCHETTI}


# --------------------------------------------------------------------------
# L'INDICE DELLE VOCI SRD che un equipaggiamento iniziale puo' nominare, per
# categoria della fonte. SOLO I NOMI: prezzi e pesi delle voci che abbiamo
# adottato stanno in `srd51_equipaggiamento.py`, e non si ripetono qui.
#
# PERCHE' SERVE UN INDICE E NON BASTA IL CATALOGO
#     `srd51_equipaggiamento.py` dichiara di coprire «non ogni voce della
#     tabella Adventuring Gear», e ha ragione a fermarsi dove si e' fermato:
#     serviva cio' che combatte ed esplora. Ma senza sapere quante siano le
#     voci in TUTTO, «ne mancano alcune» e' un'impressione e non un numero, e
#     questo progetto conta i numeri invece di ricordarli (CLAUDE.md 3).
#
# L'INVARIANTE, verificata all'import: ogni voce che il catalogo adotta deve
# comparire in questo indice. Se un giorno una voce del catalogo non fosse
# piu' qui dentro, l'indice sarebbe sfasato rispetto alla fonte da cui
# entrambi vengono — e sarebbero due trascrizioni della stessa tabella che
# nessuno mette una contro l'altra, cioe' il difetto di sempre.
# --------------------------------------------------------------------------
INDICE_SRD = {
    "adventuring-gear": (
        "Abacus", "Acid", "Acid (vial)", "Alchemist's Fire (Flask)",
        "Amulet", "Antitoxin (Vial)", "Backpack",
        "Ball Bearings (bag of 1000)", "Barrel", "Basket", "Bedroll",
        "Bell", "Blanket", "Block and Tackle", "Book", "Bottle, glass",
        "Bucket", "Caltrops (bag of 20)", "Candle", "Case, Crossbow Bolt",
        "Case, Map or Scroll", "Chain (10 feet)", "Chalk (1 piece)",
        "Chest", "Climber's Kit", "Clothes, Common", "Clothes, costume",
        "Clothes, fine", "Clothes, traveler's", "Component Pouch",
        "Crowbar", "Crystal", "Emblem", "Fishing Tackle",
        "Flask or tankard", "Grappling hook", "Hammer", "Hammer, sledge",
        "Healer's Kit", "Holy Water (flask)", "Hourglass", "Hunting Trap",
        "Ink (1 ounce bottle)", "Ink pen", "Jug or pitcher",
        "Ladder (10-foot)", "Lamp", "Lamp oil (flask)",
        "Lantern, Bullseye", "Lantern, Hooded", "Lock",
        "Magnifying Glass", "Manacles", "Mess Kit", "Mirror, steel",
        "Orb", "Paper (one sheet)", "Parchment (one sheet)",
        "Perfume (vial)", "Pick, miner's", "Piton", "Pole (10-foot)",
        "Pot, iron", "Pouch", "Quiver", "Ram, Portable",
        "Rations (1 day)", "Reliquary", "Robes", "Rope, hempen (50 feet)",
        "Rope, silk (50 feet)", "Sack", "Scale, Merchant's",
        "Sealing wax", "Shovel", "Signal whistle", "Soap", "Spellbook",
        "Spike, iron", "Sprig of mistletoe", "Spyglass", "Tent",
        "Tinderbox", "Torch", "Totem", "Vial", "Waterskin", "Whetstone",
        "Wooden staff",
    ),
    "ammunition": (
        "Arrow (bow)", "Blowgun needles", "Crossbow bolt",
        "Sling bullets",
    ),
    "tools": (
        "Alchemist's Supplies", "Bagpipes", "Brewer's Supplies",
        "Calligrapher's supplies", "Carpenter's Tools",
        "Cartographer's Tools", "Cobbler's Tools", "Cook's utensils",
        "Dice set", "Disguise kit", "Drum", "Dulcimer", "Flute",
        "Forgery kit", "Glassblower's Tools", "Herbalism Kit", "Horn",
        "Jeweler's Tools", "Leatherworker's Tools", "Lute", "Lyre",
        "Mason's Tools", "Navigator's tools", "Painter's Supplies",
        "Pan flute", "Playing card set", "Poisoner's kit",
        "Potter's tools", "Shawm", "Smith's tools", "Thieves' tools",
        "Tinker's tools", "Viol", "Weaver's tools", "Woodcarver's tools",
    ),
}


# Un nome che le due letture della stessa fonte scrivono in due modi, e la
# ragione accanto. La prima non e' un caso limite inventato: e' il primo
# controllo che l'invariante qui sotto ha fermato, appena scritta.
#
# LE DUE VOCI NON SONO LA STESSA COSA, e vale la pena dirlo perche' la
# struttura le tratta uguale. `Arrow` e' una differenza di TRASCRIZIONE: due
# endpoint della stessa fonte scrivono lo stesso nome in due modi.
# `Vestments` e' una LETTURA: la descrizione di un pacchetto e la tabella
# dell'attrezzatura usano due parole diverse, e siamo noi a dire che nominano
# la stessa cosa. La seconda si puo' sbagliare e la prima no — per questo
# porta la ragione per esteso, e per questo l'alternativa (creare un oggetto
# «Vestments» accanto a «Robes») e' scritta qui invece che dimenticata.
EQUIVALENZE = {
    "Arrow": "Arrow (bow)",   # /v2/items/ la stampa col qualificatore
                              # dell'arma; `srd51_equipaggiamento.py` l'ha
                              # adottata senza, perche' li' la freccia sta
                              # accanto ai dardi e agli aghi e il
                              # qualificatore non distingueva niente.

    # Il Pacchetto del sacerdote elenca «Vestments»; la tabella
    # dell'attrezzatura elenca «Robes», con prezzo e peso propri. Sono la
    # veste di chi officia e la veste, e la fonte non le distingue in nessun
    # punto: nessuna regola le tratta diversamente, nessuna delle due porta
    # meccanica. Leggerle come la stessa voce evita un oggetto nuovo dal
    # prezzo inventato; leggerle come due voci diverse costerebbe esattamente
    # quello. E' la sola delle sette voci senza listino a cui ha risposto la
    # fonte invece che noi — decisione 63 (`oggetto-se-serve-al-motore`).
    "Vestments": "Robes",
}


def canonico(nome):
    """Il nome come l'indice lo porta."""
    return EQUIVALENZE.get(nome, nome)


def indice_completo():
    return tuple(sorted(n for voci in INDICE_SRD.values() for n in voci))


import srd51_equipaggiamento as _EQ  # noqa: E402

_ADOTTATE = {canonico(n) for n, *_ in _EQ.ATTREZZATURA}
_MANCANTI = sorted(_ADOTTATE - set(indice_completo()))
assert not _MANCANTI, (
    "il catalogo adotta voci che l'indice SRD non nomina: "
    f"{_MANCANTI}. Le due trascrizioni vengono dalla stessa tabella e si "
    "sono sfasate.")

_USATE = {v for righe in EQUIPAGGIAMENTO.values() for riga in righe
          for alt in riga for _q, v, g in alt if g == CATEGORIA}
_SCARTO = _USATE ^ set(SCELTE)
assert not _SCARTO, (
    f"le scelte dichiarate e quelle usate dagli elenchi non coincidono: "
    f"{sorted(_SCARTO)}. Una scelta senza filtro e' una domanda che "
    "l'interfaccia non sa porre; un filtro senza scelta e' un permesso "
    "marcito.")

_FANTASMA = sorted(set(EQUIVALENZE.values()) - set(indice_completo()))
assert not _FANTASMA, (
    f"equivalenza verso un nome che l'indice non ha: {_FANTASMA}. "
    "Un'eccezione dichiarata e non trovata e' un'eccezione marcita.")
