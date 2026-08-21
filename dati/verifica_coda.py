#!/usr/bin/env python3
"""
Verifica che dati/mostri.coda.json non sdoppi una voce a piu' colonne di
dati/_bestiario_mc.py (il registro verificato sulle immagini) in due voci
separate della coda, e che non contraddica dati/METODO-conversione-mostri.md
sulle categorie aperte.

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

    Stesso difetto, forma diversa, trovato il 21/08/2026: lo Spectral Minion
    era gia' elencato come creatura-modello nel blocco `categorie_aperte` di
    questo stesso file E in METODO-conversione-mostri.md §5, ma la sua voce
    dentro "coda" portava ancora `stato: "da_fare"` — due strutture (il
    campo `stato` per-voce e l'indice `categorie_aperte`) che descrivono la
    stessa cosa e si erano sfasate, esattamente come gli sdoppiamenti sopra.
    `verifica_categorie_aperte()` controlla anche questo, cosi' un nuovo
    disallineamento non passa inosservato.

COSA CONTROLLA
    1. Sdoppiamento voce/fascia: per ogni voce del registro con piu' di una
       creatura (colonne multiple), verifica che le sue creature non
       compaiano sparse su piu' fasce distinte della sezione "coda". Una
       creatura fuori target puo' legittimamente finire in "fuori_fascia"
       (schema Hatori/Spider): non e' un errore, e' segnalata solo a titolo
       informativo.

       Non verifica "convertite": le voci gia' convertite non portano il
       nome 2e originale (solo id/name_it), quindi il confronto non e'
       automatico. Sdoppiamenti gia' avvenuti li' (es. Shadowperson/Revered
       Ancient One, Ogre/Orughi) restano un limite noto di questo script,
       documentato nel rapporto della sessione che li ha trovati.

    2. Coerenza `stato` vs categorie aperte: ogni voce elencata nel blocco
       `categorie_aperte` di questo file deve avere `stato: "categoria_aperta"`
       nella propria fascia (eccetto le eccezioni gia' risolte in
       ECCEZIONI_RISOLTE, es. Tayling — statblock fisico fisso, GS
       provvisorio, `stato: "fatto"` per scelta esplicita di METODO §5).
       Ogni voce con `stato: "categoria_aperta"` deve comparire nel blocco
       `categorie_aperte`, non solo nella propria fascia (altrimenti e' una
       categoria aperta non indicizzata). Infine ogni nome citato in
       `categorie_aperte` deve comparire per intero anche nel testo della
       sezione "## 5. Le categorie aperte" di METODO-conversione-mostri.md:
       un controllo debole (sottostringa, non semantico) ma sufficiente a
       cogliere un nome tolto o rinominato da un lato e non dall'altro.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _bestiario_mc import VOCI

CODA_PATH = Path(__file__).parent / "mostri.coda.json"
METODO_PATH = Path(__file__).parent / "METODO-conversione-mostri.md"

# Voci elencate in "categorie_aperte" ma gia' risolte con una decisione
# esplicita, quindi legittimamente `stato: "fatto"` invece di
# `categoria_aperta`. Aggiungere qui SOLO quando METODO-conversione-mostri.md
# §5 documenta la decisione presa (non basta che la voce sia stata scritta).
ECCEZIONI_RISOLTE = {
    "Tayling",  # incantatore a scelta del master: statblock fisico fisso,
                # GS provvisorio — vedi METODO §5, terza categoria aperta.
}


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


def carica_sezione_metodo_5():
    """Estrae il testo di '## 5. Le categorie aperte' da METODO, fino al
    prossimo titolo '## '. Ritorna stringa vuota se il file/sezione manca
    (chi chiama tratta questo come un fallimento del controllo, non come
    'nessuna sezione da controllare')."""
    if not METODO_PATH.exists():
        return ""
    testo = METODO_PATH.read_text(encoding="utf-8")
    m = re.search(r"## 5\. Le categorie aperte\n(.*?)\n## ", testo, re.DOTALL)
    return m.group(1) if m else ""


def verifica_categorie_aperte():
    """Controlla che `stato` per-voce e l'indice `categorie_aperte` (dentro
    mostri.coda.json) e il testo di METODO §5 raccontino la stessa storia.
    Le tre strutture sono mantenute a mano e possono sfasarsi indipendente-
    mente l'una dall'altra: e' successo con lo Spectral Minion il
    21/08/2026 (vedi docstring del modulo)."""
    coda = carica_coda()
    errori = []

    stato_per_voce = {}
    for fascia in coda["coda"]:
        for voce in fascia["voci"]:
            stato_per_voce[voce["voce"]] = voce["stato"]

    nomi_indicizzati = set()
    for gruppo in coda.get("categorie_aperte", []):
        for nome in gruppo["voci"]:
            nomi_indicizzati.add(nome)
            stato = stato_per_voce.get(nome)
            if stato is None:
                errori.append(
                    f"CATEGORIA APERTA '{nome}' (gruppo '{gruppo['nome']}') "
                    f"non ha una voce corrispondente in 'coda': impossibile "
                    f"verificarne lo stato."
                )
            elif nome in ECCEZIONI_RISOLTE:
                if stato != "fatto":
                    errori.append(
                        f"'{nome}' e' in ECCEZIONI_RISOLTE (categoria aperta "
                        f"gia' decisa) ma il suo stato in coda e' '{stato}', "
                        f"non 'fatto': la risoluzione documentata in METODO "
                        f"§5 non e' (piu'?) applicata alla coda."
                    )
            elif stato != "categoria_aperta":
                errori.append(
                    f"'{nome}' e' elencata in 'categorie_aperte' (gruppo "
                    f"'{gruppo['nome']}') ma il suo stato in coda e' "
                    f"'{stato}', non 'categoria_aperta': la coda contraddice "
                    f"la classificazione del metodo."
                )

    for nome, stato in stato_per_voce.items():
        if stato == "categoria_aperta" and nome not in nomi_indicizzati:
            errori.append(
                f"'{nome}' ha stato 'categoria_aperta' in coda ma non "
                f"compare in nessun gruppo di 'categorie_aperte': categoria "
                f"aperta non indicizzata."
            )

    sezione_metodo = carica_sezione_metodo_5()
    if not sezione_metodo:
        errori.append(
            "Impossibile leggere '## 5. Le categorie aperte' da "
            f"{METODO_PATH.name}: controllo incrociato con la coda saltato."
        )
    else:
        for gruppo in coda.get("categorie_aperte", []):
            for nome in gruppo["voci"]:
                if nome not in sezione_metodo:
                    errori.append(
                        f"'{nome}' e' in 'categorie_aperte' (gruppo "
                        f"'{gruppo['nome']}') ma il nome non compare nel "
                        f"testo di METODO §5: nome cambiato o voce tolta da "
                        f"un lato senza aggiornare l'altro."
                    )

    return errori


if __name__ == "__main__":
    errori, informativi = verifica()
    errori_categorie = verifica_categorie_aperte()

    if informativi:
        print("INFO (probabilmente gia' convertite, fuori portata dello script):")
        for msg in informativi:
            print(f"  - {msg}")
        print()

    tutti_errori = errori + errori_categorie
    if tutti_errori:
        print("ERRORI:")
        for msg in tutti_errori:
            print(f"  - {msg}")
        sys.exit(1)

    print("OK: nessuna voce a piu' colonne risulta sdoppiata fra fasce diverse della coda.")
    print("OK: stato per-voce, indice 'categorie_aperte' e METODO §5 sono coerenti.")
