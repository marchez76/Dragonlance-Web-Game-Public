#!/usr/bin/env python3
"""
DECISIONE 25 — registro delle divergenze da Shadow of the Dragon Queen.

PERCHE' ESISTE
    SotDQ e' materiale ufficiale 5e su Krynn, ma NON e' la conversione
    ufficiale del materiale 2e: e' un prodotto scritto da zero che ne condivide
    i nomi. Le sue scelte sono un'interpretazione parallela, non l'edizione
    autorizzata della nostra fonte. Quindi non prevale su tutto.

    Dove non prevale, la divergenza va REGISTRATA, non nascosta. Deve essere
    possibile elencare "dove divergiamo dall'ufficiale e perche'", che e'
    un'informazione utile di per se': dice a chi conosce SotDQ perche' il
    nostro Kender non e' il suo.

CAMPI
    id          chiave stabile, per interrogare
    ambito      razza / classe / divinita' / regola
    soggetto    a chi si applica
    ufficiale   cosa dice SotDQ
    nostro      cosa diciamo noi
    esito       "adottato" se SotDQ prevale, "divergiamo" altrimenti
    decisione   quale decisione del progetto governa il punto
    motivo      perche'
"""

FONTE = ("Dragonlance: Shadow of the Dragon Queen (WotC, 2022), 226 pagine, "
         "verificato sul PDF in libreria")

# --------------------------------------------------------------------------
# NOTA SULLA FONTE, da tenere presente quando si legge questo registro.
#
# Il primo PDF caricato in libreria era una versione RIDOTTA: 187 pagine
# invece di 226, con i corpi delle regole rimossi. Non conteneva il blocco
# KENDER TRAITS, i testi dei talenti, ne' un solo blocco statistiche
# (zero occorrenze di "Challenge" su 187 pagine).
#
# Il PDF corretto e' arrivato dopo e le divergenze qui sotto sono state
# riverificate su quello. Dove la verifica ha cambiato qualcosa e' segnato
# nel campo `verifica`.
# --------------------------------------------------------------------------

DIVERGENZE = [
    # ---------------- A) dove SotDQ PREVALE ----------------
    {
        "id": "kender-schernire",
        "ambito": "razza",
        "soggetto": "kender",
        "tratto": "Schernire (Taunting)",
        "esito": "adottato",
        "ufficiale": "SotDQ pag. 27: azione bonus, raggio 60 piedi, TS su "
                     "Saggezza, usi limitati per riposo lungo. Meccanicamente "
                     "più contenuta della nostra bozza (raggio maggiore ma "
                     "usi limitati contro nessun limite).",
        "nostro": "Era: azione bonus, raggio 30 piedi, TS su Saggezza, nessun "
                  "limite di usi. RITIRATA.",
        "decisione": "25.A",
        "motivo": "E' l'unico tratto che il progetto avesse marcato provvisorio, e "
                  "la nota diceva testualmente che aspettava questo manuale. "
                  "La forma nostra era piu' aderente al testo 2e, che non prevede "
                  "limiti giornalieri; quella ufficiale e' piu' bilanciata per la "
                  "5e. Si adotta l'ufficiale perche' colma esattamente il vuoto "
                  "che non potevamo colmare da soli, non perche' sia piu' fedele.",
        "verifica": "Blocco KENDER TRAITS, pag. 27 stampata. Trascrizione "
                    "confermata parola per parola sul PDF completo.",
        "reversibile": True,
    },
    {
        "id": "kender-nome-tratto",
        "ambito": "razza",
        "soggetto": "kender",
        "tratto": "nome del secondo tratto",
        "esito": "adottato",
        "ufficiale": "\"Kender Aptitude\" (pag. 27 stampata).",
        "nostro": "Nessun tratto corrispondente: la competenza a scelta non e' "
                  "nel nostro roster kender.",
        "decisione": "25 — annotazione",
        "motivo": "Registrato perche' e' un CONTROLLO SULLE FONTI DI SECONDA MANO: "
                  "il dump in import/json-personali/ chiama questo tratto "
                  "\"Kender Curiosity\", il manuale stampato lo chiama "
                  "\"Kender Aptitude\". Su un dettaglio verificabile il dump "
                  "diverge dalla carta. E' un motivo in piu' per preferire il PDF.",
        "verifica": "Pag. 27 stampata, verificata sul PDF completo.",
        "reversibile": False,
    },

    # ---------------- B) dove SotDQ NON prevale ----------------
    {
        "id": "kender-aggiustamenti",
        "ambito": "razza",
        "soggetto": "kender",
        "tratto": "aggiustamenti di caratteristica",
        "esito": "divergiamo",
        "ufficiale": "Nessun aggiustamento fisso: \"increase one of those scores by "
                     "2 and increase a different score by 1, or increase three "
                     "different scores by 1\" (pag. 15 stampata). E' il modello "
                     "LIGNAGGIO, in cui i punteggi li assegna il giocatore.",
        "nostro": "DES +1, dal capitolo razziale di Tales of the Lance.",
        "decisione": "2",
        "motivo": "Il modello lignaggio e' quello del PHB 2024, che la decisione 2 "
                  "ha respinto scegliendo il PHB 2014 perche' rende le specie "
                  "numericamente neutre e quindi incompatibile con la decisione 3. "
                  "Incompatibile alla radice, non per un numero.",
        "reversibile": False,
    },
    {
        "id": "kender-velocita",
        "ambito": "razza",
        "soggetto": "kender",
        "tratto": "velocita'",
        "esito": "divergiamo",
        "ufficiale": "30 piedi.",
        "nostro": "25 piedi, derivati dal tasso MV 9 della 2e.",
        "decisione": "13/14 (velocita' dai tassi MV)",
        "motivo": "La nostra velocita' non e' un numero scelto ma il risultato di "
                  "una regola di conversione applicata a tutto il roster. "
                  "Cambiarla per una sola razza romperebbe l'ordinamento.",
        "reversibile": False,
    },
    {
        "id": "kender-scurovisione",
        "ambito": "razza",
        "soggetto": "kender",
        "tratto": "scurovisione",
        "esito": "divergiamo",
        "ufficiale": "Nessuna scurovisione.",
        "nostro": "30 piedi, convertiti dall'infravisione dichiarata dalla 2e.",
        "decisione": "14",
        "motivo": "Dove il manuale 2e dichiara l'infravisione la convertiamo. "
                  "SotDQ non la nega: semplicemente non la concede, perche' "
                  "riscrive la razza da zero.",
        "reversibile": False,
    },
    {
        "id": "cavalieri-solamnia",
        "ambito": "classe",
        "soggetto": "cavaliere-corona, cavaliere-spada, cavaliere-rosa",
        "tratto": "struttura dell'ordine",
        "esito": "divergiamo",
        "ufficiale": "I Cavalieri di Solamnia sono un BACKGROUND piu' una catena di "
                     "talenti (Squire of Solamnia, Knight of the Crown, Knight of "
                     "the Sword, Knight of the Rose), disponibili come scelte "
                     "indipendenti al 4° livello e oltre.",
        "nostro": "Tre classi in sequenza obbligata Corona -> Spada -> Rosa, con "
                  "ingresso al 1°, 3° e 4° livello.",
        "decisione": "5",
        "motivo": "La forma ufficiale permette di diventare Cavaliere della Rosa "
                  "senza mai passare per Corona e Spada. E' precisamente cio' che "
                  "la decisione 5 rifiuta: la sequenza obbligata E' il contenuto "
                  "dell'ordine.",
        "reversibile": False,
    },
    {
        "id": "maghi-alta-stregoneria",
        "ambito": "classe",
        "soggetto": "mago-alta-stregoneria, mago-veste-bianca/rossa/nera",
        "tratto": "struttura dell'ordine",
        "esito": "divergiamo",
        "ufficiale": "Background \"Mage of High Sorcery\" piu' i talenti Initiate of "
                     "High Sorcery e Adept of the White/Red/Black Robes.",
        "nostro": "Classe base Mago dell'Alta Stregoneria; le tre Vesti sono "
                  "affiliazioni dichiarate al Test, al 3° livello.",
        "decisione": "6",
        "motivo": "Il trattamento a background e talenti non sostituisce la "
                  "struttura del Test, che nella fonte 2e e' un passaggio "
                  "obbligato e datato al 3° livello.",
        "reversibile": False,
    },
    {
        "id": "divinita-sfere",
        "ambito": "divinita'",
        "soggetto": "tutte e 21",
        "tratto": "sfere e rango",
        "esito": "divergiamo",
        "ufficiale": "Le stesse 21 divinita', con `province` (ambito narrativo) e "
                     "`symbol`. Nessuna sfera, nessun rango.",
        "nostro": "Sfere maggiori e minori dalla 2e, piu' rango "
                  "greater/intermediate/lesser. Il filtro della decisione 24 "
                  "poggia interamente su questo.",
        "decisione": "24",
        "motivo": "I nostri dati sono strettamente piu' ricchi. SotDQ vale come "
                  "riscontro dei nomi: coincidono tutti e ventuno. "
                  "`province` e `symbol` non confliggono con nulla e si possono "
                  "prendere.",
        "reversibile": False,
    },
]

# ---------------- C) dove SotDQ E' FONTE UNICA ----------------
# Contenuto che in 2e non esiste. Nessun conflitto possibile: SotDQ e'
# autoritativo per forza. REGISTRATO COME DISPONIBILE, NON ESTRATTO.
FONTE_UNICA = [
    {"id": "lunar-sorcery", "cosa": "Sottoclasse Lunar Sorcery per lo Stregone",
     "dove": "SotDQ cap. 1, pag. 18 stampata (solo il nome nel nostro PDF)",
     "stato": "disponibile, non estratto"},
    {"id": "talenti-krynn",
     "cosa": "Nove talenti: Divinely Favored, Initiate of High Sorcery, "
             "Adept of the Black/Red/White Robes, Squire of Solamnia, "
             "Knight of the Crown/Rose/Sword",
     "dove": "SotDQ cap. 1, pag. 18 stampata (solo i nomi nel nostro PDF)",
     "stato": "disponibile, non estratto"},
    {"id": "background-krynn",
     "cosa": "Due background: Knight of Solamnia, Mage of High Sorcery",
     "dove": "SotDQ cap. 1",
     "stato": "disponibile, non estratto"},
    {"id": "mostri-sotdq",
     "cosa": "Mostri e PNG di Krynn con statistiche 5e",
     "dove": "SotDQ Appendice B",
     "stato": "disponibile, non estratto — vedi RAPPORTO-mostri.md"},
]


def per_esito(esito):
    return [d for d in DIVERGENZE if d["esito"] == esito]


def per_ambito(ambito):
    return [d for d in DIVERGENZE if d["ambito"] == ambito]
