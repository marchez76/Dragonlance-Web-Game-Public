#!/usr/bin/env python3
"""
Genera `dati/pacchetti/` dai dati SRD di `_fonti/srd51_pacchetti.py`.

COSA SCRIVE E COSA NO
    I pacchetti che i cinque elenchi di telaio NOMINANO davvero, non tutti e
    sette quelli che l'SRD stampa. Quali siano non e' scritto qui: si deriva
    da `EQUIPAGGIAMENTO`, perche' un elenco di cinque nomi accanto a un
    elenco che gia' li contiene sarebbe una struttura doppia in scala piccola
    — e la prima che si sfasa il giorno in cui un telaio nuovo nomina un
    sesto pacchetto (CLAUDE.md 3).

    Gli altri due — Diplomat's e Entertainer's — nominano nove voci che il
    catalogo non ha: scriverli vorrebbe dire o riferimenti che non risolvono
    o nove voci adottate per completezza. La cartella si riempie a consumo,
    come `dati/condizioni/` per la decisione 48 (`condizioni-a-consumo`).

LE VOCI RIFERISCONO, NON RICOPIANO
    Ogni voce porta l'id del catalogo, non prezzo e peso: quelli stanno in
    `dati/oggetti/` e da li' si leggono (`_valuta.prezzo_di()`). Il nome SRD
    resta accanto perche' la lettura sia verificabile senza aprire il
    catalogo.

    Le 7 voci che l'SRD nomina SOLO dentro la descrizione di un pacchetto —
    senza prezzo ne' peso — erano la domanda aperta che la
    decisione 62 (`pacchetto-fisso`) aveva lasciato tale. La
    decisione 63 (`oggetto-se-serve-al-motore`) la chiude, e non a una a
    una: da' il criterio e lo applica. Quale esito abbia preso ciascuna non
    e' scritto qui — sta in `_voci_di_pacchetto.VOCI`, unica sede, con la
    ragione accanto al risultato.

Uso:  python3 dati/build_pacchetti.py
"""

import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "_fonti"))

import srd51_pacchetti as P  # noqa: E402
import _voci_di_pacchetto as VP  # noqa: E402
from build_oggetti import slugify  # noqa: E402

OUT = os.path.join(BASE, "pacchetti")
SOURCE_BOOK = "Player's Handbook (SRD 5.1), sezione «Equipment Packs»"

# La resa italiana del nome. E' l'unica cosa che questo modulo aggiunge alla
# fonte, ed e' nostra: l'SRD non ha un'edizione italiana da cui copiarla.
NOMI_IT = {
    "Burglar's Pack": "Pacchetto dello scassinatore",
    "Diplomat's Pack": "Pacchetto del diplomatico",
    "Dungeoneer's Pack": "Pacchetto dell'esploratore di sotterranei",
    "Entertainer's Pack": "Pacchetto dell'intrattenitore",
    "Explorer's Pack": "Pacchetto dell'esploratore",
    "Priest's Pack": "Pacchetto del sacerdote",
    "Scholar's Pack": "Pacchetto dello studioso",
}

def _voce(quantita, nome, a_listino):
    """La voce come esce nel JSON, risolta.

    TRE STATI E NON DUE, ed e' la forma della decisione: `a_catalogo` quando
    la voce ha un id che risolve, `testo_del_pacchetto` quando il criterio ha
    deciso che non deve averne uno. Il vecchio `da_decidere` non c'e' piu'
    perche' non c'e' piu' niente da decidere: se un domani un pacchetto nuovo
    portasse una voce senza listino, il criterio la decide all'arrivo — e
    `_voci_di_pacchetto` solleva finche' non lo si e' fatto, invece di
    lasciarla passare come indecisa.
    """
    if a_listino:
        return {"quantita": quantita, "name_srd": nome,
                "oggetto": slugify(P.canonico(nome)), "stato": "a_catalogo",
                "motivo": None}
    esito = VP.esito_di(nome)
    ragione = VP.ragione_di(nome)
    if esito == "testo":
        return {"quantita": quantita, "name_srd": nome, "oggetto": None,
                "stato": "testo_del_pacchetto", "motivo": ragione}
    # `oggetto` e `equivalenza` finiscono tutt'e due a catalogo: la
    # differenza sta in COME ci sono arrivate — creando una voce nuova o
    # riconoscendone una che c'era gia' — e quella sta nel motivo.
    return {"quantita": quantita, "name_srd": nome,
            "oggetto": slugify(P.canonico(nome)), "stato": "a_catalogo",
            "motivo": ragione}


def nominati_dai_telai():
    """I pacchetti che gli elenchi delle cinque classi SRD nominano."""
    return {voce
            for righe in P.EQUIPAGGIAMENTO.values()
            for riga in righe
            for alternativa in riga
            for _q, voce, genere in alternativa
            if genere == P.PACCHETTO}


def documento(nome, costo, voci):
    return {
        "id": slugify(nome),
        "name": {"en": nome, "it": NOMI_IT[nome]},
        "source": {
            "source_edition": "SRD 5.1",
            "source_book": SOURCE_BOOK,
            "api_ref": "v1/sections/equipment-packs",
        },
        "cost_gp": costo,
        "voci": [_voce(q, v, a_listino) for q, v, a_listino in voci],
        "note": None,
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    servono = nominati_dai_telai()
    scritti = 0
    for nome, costo, voci in P.PACCHETTI:
        if nome not in servono:
            continue
        d = documento(nome, costo, voci)
        percorso = os.path.join(OUT, d["id"] + ".json")
        with open(percorso, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("scritto", os.path.basename(percorso))
        scritti += 1
    print(f"\n{scritti} pacchetti su {len(P.PACCHETTI)} trascritti dall'SRD: "
          f"sono quelli che i {len(P.EQUIPAGGIAMENTO)} elenchi di telaio "
          f"nominano.")


if __name__ == "__main__":
    main()
