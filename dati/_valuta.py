#!/usr/bin/env python3
"""
Acciaio e oro: due regole distinte, due campi, una destinazione dichiarata.

DECISIONE 42 (`cambio-acciaio-oro`)
    Le fonti danno piu' di un numero e la tentazione e' sceglierne uno. E'
    la tentazione sbagliata: i numeri rispondono a domande diverse, e
    collidono solo se si confondono i due usi. Si registrano tutti, ciascuno
    con l'uso a cui serve — il trattamento della
    decisione 27 (`sette-campi-2e`), dove un dato di fonte entra con la
    destinazione dichiarata e mai come valore nudo.

    Il buco che chiudono e' misurato in RAPPORTO-personaggio §2.5: poche
    classi dichiarano una ricchezza iniziale in pezzi
    d'acciaio, tutti gli oggetti portano `cost_gp` in pezzi d'oro, e nessun
    campo in nessuno schema diceva il rapporto fra le due. Un personaggio
    non poteva comprare il proprio equipaggiamento perche' non esisteva
    un'aritmetica che collegasse il borsello al listino.

PERCHE' UN MODULO E NON UN CAMPO DI SCHEMA
    Non e' un dato di una razza, di una classe o di un oggetto: e' una
    regola del mondo, che vale per tutti e non appartiene a nessuno.
    Metterla in uno schema vorrebbe dire ripeterla su ogni entita' che la
    usa, che e' esattamente la forma di struttura doppia che
    dati/condizioni/ e la decisione 41 (`sconfessione-condivisa`) esistono
    per evitare. Sede unica, riferita da chi serve.
"""

# --------------------------------------------------------------------------
# IL CAMBIO DEL MONDO — lore ed economia interna di Krynn.
# --------------------------------------------------------------------------
CAMBIO_MONETE = {
    "valore": 40,
    "forma": "1 pezzo d'acciaio = 40 monete d'oro",
    "fonte": "Tales of the Lance (2e)",
    "uso": "lore ed economia interna: tesori, ricompense, descrizione del "
           "mondo, il prezzo che un personaggio SENTE nominare in gioco.",
    "non_uso": "NON entra mai in un prezzo di listino. Applicarlo ai nostri "
               "cost_gp darebbe un'aritmetica falsa in entrambe le "
               "direzioni.",
    "motivo": "Dopo il Cataclisma l'acciaio e' il metallo scarso e l'oro "
              "l'ornamento: il rapporto e' un fatto del mondo, non una "
              "tabella di conversione.",
}

# --------------------------------------------------------------------------
# IL FATTORE DI LISTINO — come si legge un prezzo importato.
# --------------------------------------------------------------------------
FATTORE_LISTINO = {
    "valore": 1,
    "forma": "1 pezzo d'acciaio = 1 unita' di listino (i nostri cost_gp)",
    "fonte": "sei moduli d'avventura Dragonlance, concordi",
    "uso": "leggere un listino importato. I nostri cost_gp vengono "
           "dall'SRD 5.1, cioe' da un listino scritto per un altro mondo: "
           "il prezzo in oro della fonte si legge come prezzo in acciaio, "
           "senza aritmetica.",
    "motivo": "L'accordo di sei moduli lo rende una regola editoriale "
              "stabile, non l'incoerenza isolata di un singolo modulo. E' "
              "il numero che serve quando un Cavaliere spende i suoi "
              "5d4x10 stl iniziali sulla tabella dell'equipaggiamento.",
}

# --------------------------------------------------------------------------
# VARIANTI NOTE — registrate perche' esistono, non perche' si applicano.
#
# Un numero di fonte che non si adotta va scritto lo stesso: cancellarlo
# significa che la prossima volta che qualcuno lo incontra nel manuale non
# sa se sia gia' stato valutato o sia sfuggito. E' lo stesso motivo per cui
# source_2e conserva i limiti di livello che la
# decisione 4 (`limiti-di-livello`) non applica.
# --------------------------------------------------------------------------
VARIANTI = [
    {
        "valore": 10,
        "forma": "1 pezzo d'acciaio = 10 monete d'oro",
        "fonte": "DLC2 / DLC3",
        "applicata": False,
        "nota": "Terzo numero visto nelle fonti. Registrato come variante "
                "nota e non come errore: e' una lettura diversa dello "
                "stesso rapporto, non uno sbaglio di stampa.",
    },
]

# Clausola del manuale: il cambio non e' uniforme su Ansalon.
VARIAZIONI_REGIONALI = {
    "dichiarata_dalla_fonte": True,
    "fonte": "Tales of the Lance (2e)",
    "applicata": False,
    "nota": "Il manuale dichiara che il cambio varia da regione a regione. "
            "La clausola e' registrata ma NON applicata: applicarla "
            "richiederebbe un dato per regione che la fonte non da'. E' un "
            "filtro senza campione, nel senso della "
            "decisione 35 (`repertori-sono-filtri`) — e finche' resta tale "
            "va detto che c'e', non risolto a occhio.",
}


def prezzo_in_acciaio(cost_gp):
    """Il prezzo di listino di un oggetto, in pezzi d'acciaio.

    Nessuna moltiplicazione, ed e' il punto: la funzione esiste per essere
    l'unico posto in cui il rapporto viene applicato, cosi' che il giorno
    che qualcuno pensasse di usare il 40 lo trovi gia' deciso qui invece di
    deciderlo di nuovo, diversamente, in fondo a un'altra funzione."""
    if cost_gp is None:
        return None
    return cost_gp * FATTORE_LISTINO["valore"]


# --------------------------------------------------------------------------
# DOVE STA IL PREZZO DI UN OGGETTO — una domanda sola, un posto solo.
#
# Le sezioni di `mechanics_5e` che portano un listino sono tre e SI ESCLUDONO
# a vicenda: `weapon_5e` per le armi, `armor_5e` per armature e scudo,
# `attrezzatura_5e` per il resto (decisione 62, `pacchetto-fisso`). Tre
# sezioni non sono tre sedi: nessun valore e' scritto due volte, e questa e'
# l'unica funzione che sa quali sono. Chi cerca un prezzo passa di qui, e il
# giorno in cui nascesse una quarta sezione si aggiunge una riga qui e non in
# ogni chiamante — che e' esattamente com'e' andata quando le sezioni erano
# due e l'attrezzatura non ne aveva nessuna.
# --------------------------------------------------------------------------

SEZIONI_DI_LISTINO = ("weapon_5e", "armor_5e", "attrezzatura_5e")


def listino(oggetto):
    """La sezione che porta prezzo e peso, o None se l'oggetto non ne ha."""
    m = oggetto.get("mechanics_5e") or {}
    for sezione in SEZIONI_DI_LISTINO:
        blocco = m.get(sezione)
        if blocco and blocco.get("cost_gp") is not None:
            return blocco
    return None


def prezzo_di(oggetto):
    """Il prezzo di un oggetto del catalogo, in pezzi d'acciaio.

    None quando l'oggetto non ha prezzo, ed e' un caso vero e non un difetto:
    il diadema dello Scheletro Guerriero e' un oggetto magico di fonte 2e, e
    la fonte non gliene da' uno."""
    blocco = listino(oggetto)
    return None if blocco is None else prezzo_in_acciaio(blocco["cost_gp"])


def peso_di(oggetto):
    """Il peso di un oggetto del catalogo, in libbre, o None."""
    blocco = listino(oggetto)
    return None if blocco is None else blocco.get("weight_lb")
