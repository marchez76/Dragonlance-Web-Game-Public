#!/usr/bin/env python3
"""
DECISIONE 26 — il criterio della tracciabilita'.

    QUALSIASI MATERIALE ESTERNO CHE NON PORTI CON SE' FONTE E PAGINA E'
    INUTILIZZABILE, a prescindere dal resto della sua qualita'.

PERCHE'
    Tutto il progetto si regge sulla tracciabilita'. Un dato di cui non si puo'
    dire da quale manuale e da quale pagina viene non e' verificabile, quindi
    non entra. Non e' una questione di fiducia in chi lo ha prodotto: e' che
    senza fonte non esiste il modo di controllarlo, ne' oggi ne' fra sei mesi.

    E' un filtro che si applica in trenta secondi e risparmia analisi lunghe.
    I due lotti in import/ hanno richiesto due giri di verifica ciascuno; con
    questo criterio il secondo si sarebbe chiuso in un conteggio.

COME SI APPLICA
    Su un lotto nuovo, nell'ordine:
      1. le voci dichiarano `source` (o equivalente) e `page`? Se no, FINE.
      2. la percentuale di copertura e' alta? Sotto il 90% e' sospetta.
      3. le sigle di fonte sono piu' di una? Allora e' un corpus, non un
         documento, e va valutato manuale per manuale.
    Il passo 1 da solo respinge o promuove.

NOTA DA CONSERVARE, perche' e' istruttiva
    La "ripulitura" del secondo lotto ha cancellato `source` e `page` da tutte
    e 19.288 le voci, lasciando intatti `senseTags`, `languageTags`,
    `traitTags` e `referenceSources`, che sono indici interni al sito da cui i
    dati provenivano. Ha rimosso l'unica cosa che ci serviva e conservato
    l'unica che non serve. Chi ripulisce dei dati senza sapere a cosa servono
    toglie quasi sempre la parte utile.

STATO DEI DUE LOTTI: RESPINTI ENTRAMBI.
    Non si toccano, non si integrano, non si consultano.
"""

CRITERIO = (
    "Qualsiasi materiale esterno che non porti con se' FONTE e PAGINA e' "
    "inutilizzabile, a prescindere dal resto della sua qualita'.")

LOTTI_RESPINTI = [
    {
        "percorso": "import/json-personali/",
        "voci": 19760,
        "con_fonte": 18457,
        "con_pagina": 13277,
        "esito": "respinto",
        "motivo": "Dichiara fonte e pagina nel 93% delle voci, quindi passa il "
                  "criterio 1. Respinto al passo 3: 146 sigle di fonte, cioe' "
                  "un corpus di manuali ridistribuito, non una raccolta "
                  "verificabile. Fonde inoltre il dato di fonte con gli indici "
                  "generati dallo strumento, senza separazione possibile.",
        "rapporto": "import/RAPPORTO-json-personali.md",
    },
    {
        "percorso": "import/json-personali-veri/",
        "voci": 19288,
        "con_fonte": 0,
        "con_pagina": 0,
        "esito": "respinto",
        "motivo": "Respinto al passo 1: ZERO voci dichiarano la fonte, ZERO la "
                  "pagina. E' lo stesso corpus del lotto precedente con le "
                  "chiavi rinominate e i marcatori parzialmente rimossi. "
                  "Strettamente peggiore dell'originale.",
        "rapporto": "import/RAPPORTO-json-veri.md",
    },
]

# Cio' che il criterio NON esclude: materiale che dichiara la fonte anche se
# viene da fuori. E' il caso dell'SRD 5.1, che citiamo per endpoint e campo.
AMMESSI_PER_CONFRONTO = [
    {
        "cosa": "SRD 5.1 (CC-BY 4.0)",
        "dove": "dati/_srd51.py, dati/_sfere_5e.py, dati/_fonti/srd51_mostri.py",
        "perche": "Documento unico, licenza esplicita, ogni valore trascritto "
                  "verbatim con l'endpoint di provenienza dichiarato nel file.",
    },
]


def verdetto(voci, con_fonte, con_pagina, n_sigle=None):
    """Applica il criterio a un lotto. Restituisce (esito, motivo)."""
    if not voci:
        return "respinto", "nessuna voce leggibile"
    q_f = con_fonte / voci
    q_p = con_pagina / voci
    if con_fonte == 0 or con_pagina == 0:
        return "respinto", ("non dichiara la fonte" if not con_fonte
                            else "non dichiara la pagina")
    if q_f < 0.9 or q_p < 0.9:
        return "sospetto", (f"copertura parziale: fonte {round(100*q_f)}%, "
                            f"pagina {round(100*q_p)}%")
    if n_sigle and n_sigle > 1:
        return "da valutare per manuale", (
            f"{n_sigle} sigle di fonte: e' un corpus, non un documento")
    return "ammissibile", "dichiara fonte e pagina su tutte le voci"
