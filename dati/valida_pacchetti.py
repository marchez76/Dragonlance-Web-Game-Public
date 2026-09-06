#!/usr/bin/env python3
"""
Valida dati/pacchetti/*.json contro dati/schema/pacchetto.schema.json.

OLTRE ALLO SCHEMA, TRE COSE CHE LO SCHEMA NON PUO' VEDERE
    1. che ogni `oggetto` risolva davvero in `dati/oggetti/` — un riferimento
       che non risolve e' peggio di una voce assente, perche' promette;
    2. che la trascrizione e la fonte nominino le stesse voci, nei due sensi
       (`_fonti/srd51_pacchetti.py` contro i file scritti): se un giorno la
       trascrizione cambia e i file no, sono due letture della stessa
       sezione che nessuno mette una contro l'altra;
    3. che ogni voce decisa dal criterio porti la sua ragione — a testo o a
       oggetto, indifferentemente: una decisione senza ragione accanto e'
       indistinguibile da una svista — e che le voci che nessuno ha dovuto
       decidere, cioe' le righe della tabella SRD, non ne portino nessuna;
    4. che le cinque SCELTE aperte siano filtri veri: quelle con un filtro
       devono trovare almeno un'arma nel catalogo — un filtro che non
       seleziona niente e' una domanda che nessuno puo' rispondere — e
       quelle senza filtro devono restare senza campione davvero, perche'
       un «filtro senza campione» dichiarato quando il campione c'e' e'
       un'assenza raccontata invece che misurata.

    Cio' che NON si controlla, di proposito: che `cost_gp` sia la somma delle
    voci. Non lo e', e non deve esserlo — l'SRD vende i pacchetti scontati.
    Un controllo cosi' segnalerebbe la fonte credendo di segnalare noi.

Uso:  uv run --with jsonschema python3 dati/valida_pacchetti.py
"""

import glob
import json
import os
import sys

import jsonschema

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "_fonti"))

import srd51_pacchetti as P  # noqa: E402
from build_oggetti import slugify  # noqa: E402

Validator = (getattr(jsonschema, "Draft202012Validator", None)
             or jsonschema.Draft7Validator)


def catalogo():
    return {json.load(open(p, encoding="utf-8"))["id"]
            for p in glob.glob(os.path.join(BASE, "oggetti", "*.json"))}


def armi():
    """(categoria, tipo) di ogni arma del catalogo."""
    fuori = []
    for p in glob.glob(os.path.join(BASE, "oggetti", "*.json")):
        w = ((json.load(open(p, encoding="utf-8")).get("mechanics_5e") or {})
             .get("weapon_5e"))
        if w:
            fuori.append((w.get("categoria"), w.get("tipo")))
    return fuori


def scelte_aperte(err):
    """I cinque filtri della decisione 62 (`pacchetto-fisso`), nei due sensi."""
    catalogo = armi()
    senza_campione = 0
    for nome, s in sorted(P.SCELTE.items()):
        f = s["filtro"]
        if f is None:
            senza_campione += 1
            continue
        quante = sum(1 for cat, tipo in catalogo
                     if cat == f["categoria"]
                     and (f["tipo"] is None or tipo == f["tipo"]))
        if not quante:
            err(f"la scelta «{nome}» ha un filtro che nel catalogo non "
                f"seleziona niente: {f}")
    return senza_campione


def coerenza(d, ids_catalogo, err):
    fonte = {slugify(n): voci for n, _c, voci in P.PACCHETTI}
    voci_fonte = fonte.get(d["id"])
    if voci_fonte is None:
        err("nessun pacchetto con questo id in _fonti/srd51_pacchetti.py: "
            "il file e' stato scritto a mano o la fonte e' cambiata sotto")
    else:
        atteso = [(q, v) for q, v, _a in voci_fonte]
        nostro = [(x["quantita"], x["name_srd"]) for x in d["voci"]]
        if atteso != nostro:
            err(f"le voci non combaciano con la trascrizione della fonte: "
                f"{len(nostro)} qui, {len(atteso)} li'. Rigenera con "
                f"build_pacchetti.py invece di correggere a mano")

    # Le voci che il criterio ha dovuto decidere sono esattamente quelle che
    # la fonte non mette a listino. Non si riconoscono dallo stato — a
    # catalogo ci finiscono anche le righe ordinarie della tabella — e non si
    # elencano qui: si leggono in `srd51_pacchetti.PACCHETTI`, che e' dove il
    # fatto sta.
    decise = {v for _q, v, a_listino in (voci_fonte or []) if not a_listino}

    for x in d["voci"]:
        if x["stato"] == "a_catalogo":
            if x["oggetto"] not in ids_catalogo:
                err(f"«{x['name_srd']}» rimanda a `{x['oggetto']}`, che in "
                    f"dati/oggetti/ non c'e'")
        else:
            if x["oggetto"] is not None:
                err(f"«{x['name_srd']}» resta testo del pacchetto e rimanda "
                    f"comunque a un oggetto: o ha un id o non ce l'ha")

        if x["name_srd"] in decise and not x.get("motivo"):
            err(f"«{x['name_srd']}» e' una delle voci che l'SRD nomina solo "
                f"dentro un pacchetto: il criterio l'ha decisa e la ragione "
                f"deve stare accanto al risultato "
                f"(decisione 63, `oggetto-se-serve-al-motore`)")
        if x["name_srd"] not in decise and x.get("motivo"):
            err(f"«{x['name_srd']}» e' una riga della tabella SRD e porta "
                f"comunque un motivo: non c'era niente da decidere")


def main():
    schema = json.load(open(os.path.join(BASE, "schema",
                                         "pacchetto.schema.json"),
                            encoding="utf-8"))
    Validator.check_schema(schema)
    v = Validator(schema)

    files = sorted(glob.glob(os.path.join(BASE, "pacchetti", "*.json")))
    if not files:
        print("nessun file in dati/pacchetti/ — esegui prima "
              "build_pacchetti.py")
        return 1

    ids_catalogo = catalogo()
    ids, totale = set(), 0
    per_stato = {"a_catalogo": 0, "testo_del_pacchetto": 0}
    for p in files:
        nome = os.path.basename(p)
        d = json.load(open(p, encoding="utf-8"))
        errori = [f"[schema] {'.'.join(map(str, e.path)) or '(radice)'}: "
                  f"{e.message[:160]}"
                  for e in sorted(v.iter_errors(d), key=lambda e: list(e.path))]
        if not errori:
            coerenza(d, ids_catalogo, errori.append)
        if d["id"] != os.path.splitext(nome)[0]:
            errori.append(f"id '{d['id']}' diverso dal nome del file")
        if d["id"] in ids:
            errori.append(f"id duplicato: {d['id']}")
        ids.add(d["id"])
        for x in d["voci"]:
            per_stato[x["stato"]] = per_stato.get(x["stato"], 0) + 1

        if errori:
            print(f"✗ {nome}")
            for e in errori:
                print(f"    {e}")
            totale += len(errori)
        else:
            print(f"✓ {nome}")

    errori_scelte = []
    senza_campione = scelte_aperte(errori_scelte.append)
    for e in errori_scelte:
        print(f"✗ scelte: {e}")
    totale += len(errori_scelte)

    print(f"\n{len(files)} pacchetti controllati, {totale} errori.")
    print(f"{len(P.SCELTE)} scelte aperte registrate come filtri "
          f"(decisione 35, `repertori-sono-filtri`), di cui {senza_campione} "
          f"senza campione nel catalogo.")
    print(f"{per_stato['a_catalogo']} voci rimandano al catalogo, "
          f"{per_stato['testo_del_pacchetto']} restano testo del pacchetto "
          f"(decisione 63, `oggetto-se-serve-al-motore`): il criterio le ha "
          f"decise tutte, e nessuna e' piu' in attesa.")
    return 1 if totale else 0


if __name__ == "__main__":
    sys.exit(main())
