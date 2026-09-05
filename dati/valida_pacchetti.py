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
    3. che ogni voce `da_decidere` porti il suo motivo, e che nessuna voce
       `a_catalogo` ne porti uno;
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

    for x in d["voci"]:
        if x["stato"] == "a_catalogo":
            if x["oggetto"] not in ids_catalogo:
                err(f"«{x['name_srd']}» rimanda a `{x['oggetto']}`, che in "
                    f"dati/oggetti/ non c'e'")
            if x.get("motivo"):
                err(f"«{x['name_srd']}» e' a catalogo e porta un motivo: il "
                    f"motivo serve solo a spiegare cosa resta da decidere")
        else:
            if x["oggetto"] is not None:
                err(f"«{x['name_srd']}» e' da decidere e rimanda comunque a "
                    f"un oggetto: o e' decisa o non lo e'")
            if not x.get("motivo"):
                err(f"«{x['name_srd']}» e' da decidere e non dice perche': "
                    f"indistinguibile da una voce dimenticata")


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
    ids, totale, da_decidere = set(), 0, 0
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
        da_decidere += sum(1 for x in d["voci"] if x["stato"] == "da_decidere")

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
    print(f"{da_decidere} voci in attesa di decisione: l'SRD le nomina solo "
          f"dentro la descrizione di un pacchetto e non da' loro ne' prezzo "
          f"ne' peso (decisione 62, `pacchetto-fisso`).")
    return 1 if totale else 0


if __name__ == "__main__":
    sys.exit(main())
