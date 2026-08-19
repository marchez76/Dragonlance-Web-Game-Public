#!/usr/bin/env python3
"""
DECISIONE 27 — i sette campi della scheda 2e senza corrispettivo in 5e.

    Non sono un problema unico: si dividono in tre gruppi, e due si chiudono
    senza deliberare.

GRUPPO A — DATI DI MONDO, NON DI SCHEDA (5 campi)
    Frequenza, numero di apparizioni, organizzazione, ciclo di attivita', dieta.
    Non e' informazione persa ma TRASFERITA: la 5e ha spostato quella funzione
    dalle schede alle tabelle d'incontro. Restano in `source_2e` come dato
    fedele e diventano input del GENERATORE DI INCONTRI in Fase 3.
    Nessuna conversione, nessuna decisione: la destinazione d'uso e' registrata
    qui perche' la questione non venga riaperta.

GRUPPO B — MORALE (1 campo)
    Non e' un campo di scheda, e' un PARAMETRO DI COMPORTAMENTO. In 2e serviva
    al DM per decidere se i mostri fuggono; qui il DM e' il motore.
    Per un gioco in solitario e' prezioso: senza morale ogni scontro finisce con
    tutti i nemici morti fino all'ultimo, il che e' irrealistico e rende il
    combattimento macchinoso. Non va nello statblock: diventa parametro dell'IA
    dei mostri in Fase 2.

GRUPPO C — RESISTENZA MAGICA (1 campo)
    L'unica vera decisione, e si prende in Fase 2 con i numeri davanti.
    Vedi NOTA_MR sotto per il motivo per cui la decisione 16 non si applica.
"""

GRUPPO_A = {
    "campi": ["frequency", "no_appearing", "organization",
              "activity_cycle", "diet"],
    "esito": "chiuso senza deliberare",
    "destinazione": "generatore_incontri",
    "fase": 3,
    "motivo": (
        "La 5e non ha eliminato questi dati, li ha spostati: dalla scheda del "
        "mostro alle tabelle d'incontro. Sono informazione di mondo — quante ne "
        "incontri, in che gruppi, di giorno o di notte, cosa mangiano — e per un "
        "generatore di incontri automatico valgono esattamente quanto valevano "
        "per un Dungeon Master umano. Restano in source_2e come trascrizione "
        "fedele e vengono letti da li'."),
}

GRUPPO_B = {
    "campi": ["morale"],
    "esito": "chiuso senza deliberare",
    "destinazione": "ia_combattimento",
    "fase": 2,
    "motivo": (
        "Il morale non e' un campo di scheda ma un parametro di comportamento. "
        "In 2e diceva al DM quando i mostri fuggono; nel nostro caso il DM e' il "
        "motore, e senza questo parametro ogni scontro finisce con tutti i "
        "nemici morti fino all'ultimo — irrealistico, e macchinoso da giocare. "
        "Il valore della fonte si conserva e diventa input dell'IA del mostro "
        "nell'arena."),
}

GRUPPO_C = {
    "campi": ["magic_resistance"],
    "esito": "RINVIATA alla Fase 2",
    "destinazione": None,
    "fase": 2,
    "motivo": (
        "E' l'unica vera decisione dei sette, e va presa con i numeri davanti."),
    "perche_non_vale_la_16": (
        "La decisione 16 dice che dove la 5e ha eliminato qualcosa "
        "deliberatamente si ripristina dalla fonte. Qui non si applica, per "
        "un'asimmetria: quei ripristini riguardavano TRATTI RAZZIALI DI "
        "PERSONAGGI GIOCANTI, in un sistema chiuso dove conta solo l'equilibrio "
        "interno. La resistenza magica riguarda invece OGNI draconico di OGNI "
        "scontro, e i Gradi di Sfida su cui stiamo calibrando presuppongono che "
        "non ci sia. Aggiungerla significa che ogni incontro pesa piu' di quanto "
        "il suo GS dichiari, sistematicamente."),
    "problema_di_traduzione": (
        "Il 20% della 2e negava l'incantesimo DEL TUTTO, inclusi quelli senza "
        "tiro salvezza. Il tratto 5e piu' vicino, Magic Resistance, da' "
        "vantaggio ai tiri salvezza contro magia: piu' debole in un senso "
        "(non annulla nulla), molto piu' forte in un altro (vale su ogni "
        "incantesimo con TS, sempre). Non sono equivalenti. Non e' il caso del "
        "Kender, dove il +4 della fonte e il vantaggio 5e valevano davvero lo "
        "stesso."),
    "quando_si_decide": (
        "In arena, quando sapremo se i draconici senza resistenza magica "
        "risultano troppo fragili."),
    "creatura_di_riferimento": (
        "Lo Yaggol (MC Dragonlance Appendix, pag. 87) ha resistenza magica "
        "50%, la piu' alta del bestiario: e' la creatura su cui questa "
        "decisione pesera' di piu', e va tenuta presente quando si valuta "
        "se ripristinarla."),
}

GRUPPI = [("A", GRUPPO_A), ("B", GRUPPO_B), ("C", GRUPPO_C)]


def totale_campi():
    return sum(len(g["campi"]) for _, g in GRUPPI)
