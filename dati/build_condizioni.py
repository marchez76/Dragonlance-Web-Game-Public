#!/usr/bin/env python3
"""
Genera dati/condizioni/*.json — le condizioni della 5e, sede unica.

PERCHE' ESISTE QUESTA CARTELLA
    Il RAPPORTO-personaggio (§5.3) registra "Condizioni e concentrazione" fra
    le operazioni che il motore d'arena non puo' fare, con la motivazione:
    *non esiste un elenco delle condizioni*. Non e' che manchi un campo: le
    condizioni erano citate solo in prosa dentro le schede che le applicano —
    `spaventato`, `avvelenato`, `paralizzato`, `afferrato` compaiono in
    italiano dentro `mechanics_5e` di vari mostri, ciascuna scritta con le
    parole di quella scheda.

    Quattro copie della stessa regola sono quattro copie che divergono. La
    decisione 41 (`sconfessione-condivisa`) ha gia' deciso come si tratta il
    caso — una regola condivisa si scrive una volta e gli altri la riferiscono
    per id — e aveva registrato che mancava una sede per le regole di sistema.
    Questa e' quella sede, per il secondo caso della stessa forma.

PERCHE' PUBBLICA
    Le condizioni sono un istituto della 5e e vengono dall'SRD 5.1, CC-BY
    (LICENSE-SRD.md). Nessun `source_2e`, nessun testo di manuale: stessa
    posizione di `dati/incantesimi/`, per la stessa ragione.

QUANTE CE NE SONO QUI, E PERCHE' NON TUTTE
    Tre, non le quindici dell'SRD: quelle che servono alla prima fetta
    verticale, piu' quella che le due implicano. Strutturare le altre dodici
    adesso significherebbe scriverle senza un caso che le eserciti, che e'
    il modo in cui un dato entra senza essere verificato. Le altre si
    aggiungono quando un blocco convertito le riferisce davvero — a partire
    da `spaventato`, `avvelenato`, `paralizzato` e `afferrato`, che i mostri
    gia' citano in prosa e che sono percio' le prime della coda.

Uso:  python3 dati/build_condizioni.py
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "condizioni")

FONTE = {
    "source_edition": "SRD 5.1",
    "source_book": "Player's Handbook (SRD 5.1), Appendix A: Conditions",
}

CONDIZIONI = [
    {
        "id": "incapacitato",
        "name": {"en": "Incapacitated", "it": "Incapacitato"},
        "api_ref": "srd/conditions/incapacitated",
        "mechanics_5e": "Una creatura incapacitata non puo' compiere azioni "
                        "ne' reazioni.",
        "effetti": [
            {"clausola": "non_puo_agire"},
            {"clausola": "non_puo_reagire"},
        ],
        "implica": [],
        "fine": None,
        "note": "La piu' piccola delle tre e la piu' riferita: non si applica "
                "quasi mai da sola, ma paralizzato, stordito e incosciente la "
                "comportano tutte. E' esattamente il caso per cui serve una "
                "sede unica — scritta dentro ciascuna delle tre, sarebbe la "
                "stessa regola in tre copie.",
    },
    {
        "id": "prono",
        "name": {"en": "Prone", "it": "Prono"},
        "api_ref": "srd/conditions/prone",
        "mechanics_5e": "Una creatura prona puo' muoversi solo strisciando, a "
                        "meno che non si rialzi ponendo fine alla condizione. "
                        "Ha svantaggio ai propri tiri per colpire. Un attacco "
                        "contro di lei ha vantaggio se chi attacca e' entro "
                        "1,5 metri, svantaggio altrimenti.",
        "effetti": [
            {"clausola": "movimento_strisciando"},
            {"clausola": "svantaggio_attacchi_propri"},
            {"clausola": "attacchi_contro_entro_5ft_vantaggio"},
            {"clausola": "attacchi_contro_oltre_5ft_svantaggio"},
        ],
        "implica": [],
        "fine": "Rialzarsi, spendendo meta' del proprio movimento.",
        "note": "La condizione che un combattimento ordinario produce piu' "
                "spesso, e la sola delle tre che non passi da un tiro "
                "salvezza contro morte.",
    },
    {
        "id": "incosciente",
        "name": {"en": "Unconscious", "it": "Incosciente"},
        "api_ref": "srd/conditions/unconscious",
        "mechanics_5e": "Una creatura incosciente e' incapacitata, non puo' "
                        "muoversi ne' parlare ed e' inconsapevole di cio' che "
                        "la circonda. Lascia cadere quello che tiene e cade "
                        "prona. Fallisce automaticamente i tiri salvezza su "
                        "Forza e Destrezza. Gli attacchi contro di lei hanno "
                        "vantaggio, e ogni attacco che la colpisce da entro "
                        "1,5 metri e' un colpo critico.",
        "effetti": [
            {"clausola": "inconsapevole"},
            {"clausola": "velocita_zero"},
            {"clausola": "lascia_cadere_oggetti"},
            {"clausola": "fallisce_tiri_salvezza", "caratteristiche": ["str", "dex"]},
            {"clausola": "vantaggio_attacchi_contro"},
            {"clausola": "colpo_critico_entro_5ft"},
        ],
        "implica": ["incapacitato", "prono"],
        "fine": "Recuperare almeno 1 punto ferita, o essere stabilizzata e "
                "riprendere i sensi.",
        "note": "E' lo stato in cui un personaggio entra a 0 punti ferita, "
                "quindi la porta d'ingresso dei tiri salvezza contro morte. "
                "I tiri salvezza contro morte NON sono modellati qui: sono "
                "una procedura del personaggio, non una clausola di questa "
                "condizione, e restano scoperti finche' lo schema Personaggio "
                "non esiste.",
    },
]


def documento(c):
    return {
        "id": c["id"],
        "name": c["name"],
        "source": dict(FONTE, api_ref=c["api_ref"]),
        "mechanics_5e": c["mechanics_5e"],
        "effetti": c["effetti"],
        "implica": c["implica"],
        "fine": c["fine"],
        "note": c["note"],
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    for c in CONDIZIONI:
        p = os.path.join(OUT, c["id"] + ".json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(documento(c), f, ensure_ascii=False, indent=2)
            f.write("\n")
    print(f"{len(CONDIZIONI)} condizioni scritte in {OUT}")


if __name__ == "__main__":
    main()
