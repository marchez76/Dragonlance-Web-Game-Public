#!/usr/bin/env python3
"""
Verifica che dati/mostri.coda.json non sdoppi una voce a piu' colonne di
dati/_bestiario_mc.py (il registro verificato sulle immagini) in due voci
separate della coda.

PERCHE' ESISTE
    mostri.coda.json nasce dalle fasce di RAPPORTO-bestiario.md, che
    ragionano per CREATURA; _bestiario_mc.py e' il registro verificato che
    ragiona per VOCE. Le due strutture derivano da fonti diverse e non sono
    mai state riconciliate automaticamente: il caso Phaethon (sdoppiato fra
    fascia 2 e fascia 3) e' stato trovato e corretto a mano il 2026-08-21,
    insieme a Insect Swarm, Hatori e Spider (of Krynn). Questo script non
    rigenera la coda (le note e le priorita' di fascia restano scelte
    umane), ma la VALIDA contro il registro cosi' un nuovo sdoppiamento non
    puo' passare inosservato — stesso principio di confronta_mostri.py, che
    ora legge il registro invece di contare per conto suo.

COSA CONTROLLA
    Per ogni voce del registro con piu' di una creatura (colonne multiple),
    verifica che le sue creature non compaiano sparse su piu' fasce distinte
    della sezione "coda". Una creatura fuori target puo' legittimamente
    finire in "fuori_fascia" (schema Hatori/Spider): non e' un errore, e'
    segnalata solo a titolo informativo.

    Non verifica "convertite": le voci gia' convertite non portano il nome
    2e originale (solo id/name_it), quindi il confronto non e' automatico.
    Sdoppiamenti gia' avvenuti li' (es. Shadowperson/Revered Ancient One,
    Ogre/Orughi) restano un limite noto di questo script, documentato nel
    rapporto della sessione che li ha trovati.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _bestiario_mc import VOCI

CODA_PATH = Path(__file__).parent / "mostri.coda.json"


def carica_coda():
    with open(CODA_PATH, encoding="utf-8") as f:
        return json.load(f)


def indice_creature_coda(coda):
    """Mappa nome-creatura (e nome-voce) -> [(fascia, voce_label), ...]."""
    indice = {}
    for fascia in coda["coda"]:
        n = fascia["fascia"]
        for voce in fascia["voci"]:
            etichette = set(voce.get("creature", [])) | {voce["voce"]}
            for etichetta in etichette:
                indice.setdefault(etichetta, []).append((n, voce["voce"]))
    return indice


def indice_creature_fuori_fascia(coda):
    presenti = set()
    for voce in coda.get("fuori_fascia", []):
        presenti.add(voce["voce"])
    return presenti


def verifica():
    coda = carica_coda()
    indice = indice_creature_coda(coda)
    fuori_fascia = indice_creature_fuori_fascia(coda)

    errori = []
    informativi = []

    for _pagina, nome_voce, creature, categoria, _verificata, _nota in VOCI:
        if categoria != "creatura" or len(creature) <= 1:
            continue

        fasce_trovate = set()
        creature_mancanti = []
        for c in creature:
            occorrenze = indice.get(c) or indice.get(nome_voce, [])
            if occorrenze:
                for fascia_n, _ in occorrenze:
                    fasce_trovate.add(fascia_n)
            elif c not in fuori_fascia:
                creature_mancanti.append(c)

        if len(fasce_trovate) > 1:
            errori.append(
                f"SDOPPIATA: '{nome_voce}' (registro: {creature}) compare "
                f"su {len(fasce_trovate)} fasce distinte della coda: "
                f"{sorted(fasce_trovate)}"
            )
        if creature_mancanti:
            informativi.append(
                f"'{nome_voce}': creature non trovate ne' in coda ne' in "
                f"fuori_fascia (forse gia' in 'convertite', fuori dalla "
                f"portata di questo controllo): {creature_mancanti}"
            )

    return errori, informativi


if __name__ == "__main__":
    errori, informativi = verifica()

    if informativi:
        print("INFO (probabilmente gia' convertite, fuori portata dello script):")
        for msg in informativi:
            print(f"  - {msg}")
        print()

    if errori:
        print("ERRORI:")
        for msg in errori:
            print(f"  - {msg}")
        sys.exit(1)

    print("OK: nessuna voce a piu' colonne risulta sdoppiata fra fasce diverse della coda.")
