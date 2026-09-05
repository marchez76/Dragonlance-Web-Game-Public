#!/usr/bin/env python3
"""
DECISIONE 58 (`telaio-apre-classe-filtra`) — da un'etichetta del PHB 2e alle
nostre classi, in due tempi.

LA FORMA, IN UNA RIGA
    Il telaio APRE l'insieme, i requisiti della classe FILTRANO dentro. Due
    controlli in sequenza, non uno. E' la stessa macchina della decisione 24
    (`sfere-sacerdotali`) — la sfera concede, il dominio filtra — e della
    decisione 35 (`repertori-sono-filtri`) — il filtro delimita, la scelta
    avviene dopo.

PERCHE' UNA SEDE SOLA
    La mappa etichetta -> telaio viveva dentro `analizza_allowed_classes.py`,
    cioe' dentro un diagnostico. Un diagnostico e' il posto sbagliato per una
    regola che la creazione del personaggio dovra' applicare davvero: la
    seconda lettura avrebbe ricopiato la mappa, e la copia sarebbe stata la
    dodicesima struttura doppia del progetto. Qui la mappa sta una volta e il
    diagnostico la importa.

COSA E' EDITORIALE E COSA E' DI FONTE, tenuto distinto per campo
    `telaio`  EDITORIALE. A quale chassis 5e corrisponde un'etichetta 2e e'
              una scelta nostra: `ragione` la porta accanto, una per riga.
    `classi`  DI FONTE. Le nostre classi che l'etichetta nomina direttamente,
              o perche' il nome coincide, o perche' il manuale dice che sono
              quella classe. `fonte` dice quale delle due, e dove.
    `da_confermare`  un accostamento di `classi` che regge sui nomi e che la
              fonte non ha ancora confermato nel merito. Non e' un difetto:
              e' una riga che aspetta una lettura, e finche' aspetta si vede.

I FILTRI CHE SEPARANO E QUELLI CHE NO
    Applicati (`filtra`): l'ingresso da un'altra classe, la restrizione di
    razza, i minimi di caratteristica contro i massimali razziali.
    NON applicati, e non per dimenticanza:
      - allineamento: nessuna razza ne dichiara uno. E' un vincolo sulla
        scelta del giocatore, non sulla coppia razza+classe, e filtrarlo qui
        non toglierebbe nessuna classe a nessuna razza.
      - classe sociale (`social_class_minimum`): la fonte la introduce come
        REGOLA OPZIONALE e non le ha dato una controparte in `mechanics_5e`.
        Un filtro su un dato che vive solo in `source_2e` applicherebbe una
        regola che non abbiamo adottato.

CLASSI BASE 2e — CINQUE ETICHETTE NOMINANO ANCHE UNA CLASSE CHE NON ABBIAMO
    Letto sulla fonte il 04/09/2026, e non e' un'ipotesi nostra: *Tales of
    the Lance* apre il capitolo dei guerrieri dicendo che su Ansalon si
    giocano le classi guerriere tipiche dell'AD&D 2e — fighter, ranger e
    paladin — e che quelle *uniche* di Ansalon sono descritte di seguito.
    Il gruppo dei ladri dice la stessa cosa con altre parole: oltre ai bardi
    e ai ladri comuni, Krynn ne ha due tipi propri (Handler e Con Artist).
    I gruppi Wizard e Priest NON lo dicono, e infatti sono di Krynn: il
    manuale arriva a precisare che negli Ordini Sacri non ci sono chierici
    come li definisce il PHB 2e.

    Conseguenza: cinque etichette — `Fighter`, `Paladin`, `Ranger`, `Thief`,
    `Bard` — non nominano solo un telaio, nominano anche una classe base 2e
    che si gioca su Krynn e che il nostro roster non ha trascritto. Non e'
    una contraddizione della fonte, ed e' esattamente la ragione per cui il
    Silvanesti e l'Irda dichiarano `Paladin` senza arrivare a nessuna nostra
    classe: il paladino che la fonte concede loro e' quello del PHB 2e, non
    un ordine solamnico.

    Cio' che questo modulo puo' dire e' dove sta il buco, non come si chiude:
    la classe base va trascritta come le altre, e finche' non c'e' l'etichetta
    apre il solo insieme del telaio. Le tre righe qui sotto lo dichiarano
    invece di lasciar credere che il telaio esaurisca l'etichetta.

UN MASSIMALE MANCANTE NON E' UN MASSIMALE A ZERO
    `ability_caps.caps` elenca solo le caratteristiche che il manuale limita:
    dove la voce manca non c'e' tetto, e il minimo di classe e' raggiungibile.
    Trattare l'assenza come uno zero renderebbe ingiocabile mezzo roster.
"""

import glob
import json
import os
from collections import namedtuple

BASE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# LA MAPPA — una riga per etichetta, con la sua ragione accanto.
#
#   telaio         chassis 5e che l'etichetta nomina, o None se non ne ha uno
#                  fra quelli trascritti. `None` non vuol dire "senza
#                  corrispondenza": vedi CODA in `_srd51.py`.
#   classi         nostre classi aperte direttamente dall'etichetta.
#   ragione        perche' quel telaio (editoriale).
#   fonte          perche' quelle classi (di fonte). Vuoto se `classi` e' vuoto.
#   da_confermare  accostamenti di `classi` in attesa di una lettura di merito.
# --------------------------------------------------------------------------
Etichetta = namedtuple("Etichetta", "telaio classi ragione fonte da_confermare")

# Le etichette che nominano ANCHE una classe base 2e. Vedi CLASSI BASE 2e nel
# docstring: non e' una nostra classificazione, e' quello che la fonte
# dichiara aprendo i gruppi Warrior e Rogue. Sta qui e non nel rapporto
# perche' i consumatori sono due e il dato e' uno solo.
#
# L'elenco e' un FATTO DI FONTE e non si muove: cinque etichette nominano una
# classe base, oggi come il giorno in cui e' stato letto. Cio' che si muove e'
# QUALI di esse il roster abbia gia' trascritto, e quello non si scrive —
# si deriva da `ETICHETTE` (CLAUDE.md 3). Fino al 05/09/2026 le due cose
# erano la stessa riga, e la riga diceva "assente dal roster": una frase vera
# per cinque etichette su cinque, che sarebbe diventata falsa per tre il
# giorno dopo senza che nulla la denunciasse.
BASE_2E = ("Bard", "Fighter", "Paladin", "Ranger", "Thief")


def base_2e_mancanti():
    """Le etichette di BASE_2E la cui classe base il roster non ha ancora.

    Derivata: un'etichetta di BASE_2E che non nomina nessuna nostra classe e'
    un'etichetta la cui classe base manca. Le tre trascritte dalla
    decisione 59 (`classi-base-2e`) escono da qui da sole."""
    return tuple(e for e in BASE_2E if not ETICHETTE[e].classi)


def _e(telaio, classi=(), ragione="", fonte="", da_confermare=()):
    return Etichetta(telaio, tuple(classi), ragione, fonte, tuple(da_confermare))


ETICHETTE = {
    "Barbarian": _e(
        "Fighter", ["barbaro"],
        "guerriero senza addestramento cavalleresco; l'Ira e' un'invenzione "
        "della 3e, assente da Krynn",
        "il nome inglese del Barbaro coincide con l'etichetta"),
    "Bard": _e(
        None, [],
        "il Bardo SRD esiste nella 5e ma non fra i telai trascritti: in coda. "
        "E' anche una classe base 2e che il roster non ha: vedi CLASSI BASE "
        "2e nel docstring"),
    "Cavalier": _e(
        "Fighter", ["cavaliere"],
        "guerriero a cavallo, telaio marziale puro",
        "il nome inglese del Cavaliere coincide con l'etichetta"),
    "Druid (heathen)": _e(
        None, ["sacerdote-eretico"],
        "nessun telaio, e non serve: l'etichetta e' gia' coperta per nome "
        "dal Sacerdote Eretico, che di telaio non ne ha",
        "CONFERMATO sulla fonte il 04/09/2026, non piu' un accostamento in "
        "attesa. Il capitolo Priest Group Classes ha due sole voci — Holy "
        "Orders of the Stars ed Heathen Priests — e nessuna terza voce per un "
        "druido: la scheda dell'eretico dichiara che sono eretici anche i "
        "druidi venuti da altri mondi, perche' non conoscono Chislev e "
        "Habbakuk. Le due righe `Druid (heathen)` e `Priest (heathen)` della "
        "tabella Class/Race Combinations si distinguono per il solo tetto di "
        "livello, che non applichiamo (decisione 4, `limiti-di-livello`): "
        "tolto quello, sono la stessa classe"),
    "Fighter": _e(
        "Fighter", ["guerriero"],
        "e' il telaio, e nomina anche la classe base 2e che gli sta sopra: "
        "vedi CLASSI BASE 2e nel docstring",
        "il nome inglese del Guerriero coincide con l'etichetta. E' la "
        "classe base AD&D 2e che *Tales of the Lance* dichiara giocabile su "
        "Ansalon senza descriverla, trascritta dal PHB 2e con la "
        "decisione 59 (`classi-base-2e`)"),
    "Handler": _e(
        "Rogue", ["handler"],
        "abilita' del ladro applicate al baratto kender",
        "il nome inglese dell'Handler coincide con l'etichetta"),
    "High Sorcerer": _e(
        "Wizard", ["mago-alta-stregoneria"],
        "incantatore arcano a preparazione",
        "`Wizard of High Sorcery` e' il nome inglese della classe"),
    "Holy Orders": _e(
        "Cleric", ["sacerdote-ordini-sacri"],
        "incantatore divino, e' il nome 2e dell'ordine sacerdotale di Krynn",
        "`Priest of the Holy Orders of the Stars` e' il nome inglese della "
        "classe; la tabella abbrevia"),
    "Illusionist": _e(
        "Wizard", [],
        "specialista arcano: nella 5e e' una sottoclasse del Mago, non una "
        "classe"),
    "Knight of Solamnia": _e(
        "Paladin", ["cavaliere-corona", "cavaliere-spada", "cavaliere-rosa"],
        "l'ombrello dei tre ordini cavallereschi; due dei tre stanno su "
        "telaio Paladin",
        "etichetta OMBRELLO: la tabella la porta come una riga sola e il "
        "capitolo dei Cavalieri di Solamnia descrive tre ordini in sequenza "
        "obbligata (decisione 5, `cavalieri-solamnia`). Apre tutti e tre; il "
        "filtro dell'ingresso lascia il solo Cavaliere della Corona"),
    "Mage (Renegade)": _e(
        "Wizard", ["mago-rinnegato"],
        "incantatore arcano fuori dagli Ordini",
        "`Renegade Wizard` e' il nome inglese della classe"),
    "Mariner": _e(
        "Fighter", ["mariner"],
        "guerriero di mare",
        "il nome inglese del Marinaio coincide con l'etichetta. Senza questa "
        "riga l'etichetta `Mariner` non aprirebbe il Marinaio, che non ha "
        "chassis"),
    "Paladin": _e(
        "Paladin", ["paladino"],
        "e' il telaio, e nomina anche la classe base 2e che gli sta sopra: "
        "vedi CLASSI BASE 2e nel docstring",
        "il nome inglese del Paladino coincide con l'etichetta. E' la classe "
        "base AD&D 2e trascritta dal PHB 2e con la "
        "decisione 59 (`classi-base-2e`), e non un ordine solamnico: e' il "
        "paladino che la fonte concede al Silvanesti e all'Irda"),
    "Priest (heathen)": _e(
        "Cleric", ["sacerdote-eretico"],
        "incantatore divino fuori dagli Ordini",
        "`Heathen Priest` e' il nome inglese della classe"),
    "Ranger": _e(
        None, [],
        "il Ranger SRD esiste nella 5e ma non fra i telai trascritti: in "
        "coda. E' anche una classe base 2e che il roster non ha: vedi CLASSI "
        "BASE 2e nel docstring"),
    "Thief": _e(
        "Rogue", ["ladro"],
        "e' il telaio, e nomina anche la classe base 2e che gli sta sopra: "
        "vedi CLASSI BASE 2e nel docstring",
        "il nome inglese del Ladro coincide con l'etichetta. E' la classe "
        "base AD&D 2e trascritta dal PHB 2e con la "
        "decisione 59 (`classi-base-2e`), e non il Con Artist: il ladro "
        "comune non ha il minimo di Carisma che escludeva l'Aghar"),
    "Tinker": _e(
        None, ["tinker"],
        "non ha un telaio 5e: e' un'invenzione di Krynn",
        "il nome inglese del Tinker coincide con l'etichetta"),
}


# --------------------------------------------------------------------------
# Lettura dei dati. Le due famiglie si leggono qui e non si ridigitano.
# --------------------------------------------------------------------------

def _carica(cartella):
    out = []
    for f in sorted(glob.glob(os.path.join(BASE, cartella, "*.json"))):
        out.append(json.load(open(f, encoding="utf-8")))
    return out


def razze():
    return _carica("razze")


def classi():
    return _carica("classi")


# --------------------------------------------------------------------------
# PRIMO TEMPO — il telaio apre.
# --------------------------------------------------------------------------

def apre(etichetta, cl):
    """Le classi che un'etichetta 2e apre: quelle che nomina piu' quelle che
    stanno sul suo telaio. L'unione, non l'alternativa: il telaio si aggiunge
    alla copertura diretta invece di sostituirsi."""
    e = ETICHETTE.get(etichetta)
    if e is None:
        raise KeyError(f"etichetta 2e non mappata: {etichetta!r}")
    ids = set(e.classi)
    if e.telaio:
        ids |= {c["id"] for c in cl
                if ((c.get("mechanics_5e") or {}).get("chassis") or {}
                    ).get("srd_class") == e.telaio}
    return ids


def aperte(razza, cl):
    """Le classi aperte a una razza, prima del filtro.

    `allowed_classes.applied` a false significa NESSUNA PRECLUSIONE — la
    tabella della fonte non elenca quella razza — e allora si apre il roster
    intero. E' il caso degli umani, ed e' la ragione per cui una classe che
    nessuna etichetta nomina puo' comunque essere raggiungibile."""
    ac = (razza.get("mechanics_5e") or {}).get("allowed_classes") or {}
    if not ac.get("applied"):
        return {c["id"] for c in cl}, None
    ids = set()
    for et in (ac.get("classes") or []):
        ids |= apre(et, cl)
    return ids, list(ac.get("classes") or [])


# --------------------------------------------------------------------------
# SECONDO TEMPO — i requisiti della classe filtrano.
# --------------------------------------------------------------------------

# Nome del filtro -> cosa toglie. Serve al rapporto, che conta per motivo:
# un insieme che si stringe senza dire perche' non e' verificabile.
MOTIVI = {
    "ingresso": "si entra da un'altra classe, non alla creazione",
    "razza": "la classe e' riservata ad altre razze",
    "caratteristica": "un minimo di classe supera il massimale razziale",
}


def filtra(razza, classe):
    """I motivi per cui `classe` NON e' accessibile a `razza`. Lista vuota =
    accessibile. Piu' motivi insieme sono tenuti tutti: sapere che una classe
    e' esclusa due volte e' diverso dal saperla esclusa una."""
    m5 = classe.get("mechanics_5e") or {}
    motivi = []

    prereq = classe.get("requires_class") or m5.get("prerequisite_class")
    if prereq:
        motivi.append(("ingresso", prereq))

    rr = m5.get("race_restriction") or {}
    if rr.get("applied") and razza["id"] not in (rr.get("races") or []):
        motivi.append(("razza", ", ".join(rr.get("races") or [])))

    caps = ((razza.get("mechanics_5e") or {}).get("ability_caps") or {}
            ).get("caps") or {}
    am = m5.get("ability_minimums") or {}
    if am.get("applied"):
        for ab, minimo in sorted((am.get("values") or {}).items()):
            tetto = caps.get(ab)
            if tetto is not None and minimo is not None and tetto < minimo:
                motivi.append(("caratteristica", f"{ab} {minimo} > {tetto}"))
    return motivi


def accessibili(razza, cl):
    """(ammesse, escluse) per una razza. `ammesse` sono id ordinati;
    `escluse` e' [(id, motivi)] per chi il telaio ha aperto e il filtro ha
    tolto — le classi che il telaio non ha mai aperto non compaiono, perche'
    non sono state escluse: non sono state proposte."""
    ids, _et = aperte(razza, cl)
    per_id = {c["id"]: c for c in cl}
    ammesse, escluse = [], []
    for i in sorted(ids):
        motivi = filtra(razza, per_id[i])
        if motivi:
            escluse.append((i, motivi))
        else:
            ammesse.append(i)
    return ammesse, escluse


# --------------------------------------------------------------------------
# GUARDIA — la mappa e i dati devono nominare le stesse cose.
#
# Una mappa che nomina un'etichetta che nessuna razza dichiara, o una classe
# che il roster non ha, e' una mappa che ha smesso di corrispondere ai dati
# senza che niente lo dicesse. E' il modo in cui le strutture doppie di questo
# progetto si sono sfasate ogni volta: combaciando il giorno in cui sono state
# scritte.
# --------------------------------------------------------------------------

def verifica():
    """Lista di incoerenze fra `ETICHETTE` e i dati. Vuota = tutto torna."""
    rz, cl = razze(), classi()
    ids = {c["id"] for c in cl}
    dichiarate = set()
    for r in rz:
        ac = (r.get("mechanics_5e") or {}).get("allowed_classes") or {}
        dichiarate |= set(ac.get("classes") or [])

    problemi = []
    for et in sorted(dichiarate - set(ETICHETTE)):
        problemi.append(f"etichetta dichiarata dalle razze e non mappata: {et}")
    for et in sorted(set(ETICHETTE) - dichiarate):
        problemi.append(f"etichetta mappata che nessuna razza dichiara: {et}")
    for et, e in sorted(ETICHETTE.items()):
        for c in e.classi:
            if c not in ids:
                problemi.append(f"{et}: nomina una classe inesistente: {c}")
        for c in e.da_confermare:
            if c not in e.classi:
                problemi.append(f"{et}: da_confermare fuori da classi: {c}")
        if e.classi and not e.fonte:
            problemi.append(f"{et}: apre classi per nome e non dice da dove")
    for et in sorted(set(BASE_2E) - set(ETICHETTE)):
        problemi.append(f"BASE_2E nomina un'etichetta non mappata: {et}")
    for et in sorted(set(BASE_2E) - dichiarate):
        problemi.append(f"BASE_2E nomina un'etichetta che nessuna razza "
                        f"dichiara: {et}")
    return problemi


if __name__ == "__main__":
    _problemi = verifica()
    for _p in _problemi:
        print("PROBLEMA:", _p)
    print(f"{len(ETICHETTE)} etichette mappate, {len(_problemi)} incoerenze.")
