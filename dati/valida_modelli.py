#!/usr/bin/env python3
"""
Valida dati/modelli/*.json contro dati/schema/modello.schema.json ed esegue i
controlli di coerenza che lo schema da solo non puo' esprimere.

Perche' servono controlli fuori dallo schema: JSON Schema sa dire com'e' fatto
UN file, non come due file si tengono. Qui i vincoli veri sono quasi tutti
incrociati — una regola condivisa definita in un modello e riferita da un
altro, un modello che punta a una scheda di mostro, i parametri di un
riferimento che devono rispettare il contratto della definizione.

Uso:  uv run --with jsonschema python3 dati/valida_modelli.py
Esce con codice 1 se trova errori.
"""

import glob
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

# Il validatore si costruisce QUI e non con un `jsonschema.Draft...(schema)`
# fatto in casa. Da quando `conversion_status` e `provenienza` hanno una sede
# sola — decisione 55 (`origine-sede-unica`) — modello.schema.json li riferisce
# con un `$ref` fra file, e un validatore senza registro non lo risolve: e'
# esattamente l'errore che questo file dava (`Unresolvable:
# vocabolari.schema.json#/$defs/conversion_status`). Il registro sta in
# `_schemi.py`, sede unica anche quello.
import _schemi as S


def coerenza_file(d, err):
    """Controlli interni a un singolo modello."""
    m = d["mechanics_5e"]

    # --- decisione 38 (`schema-modelli`): un campo o si eredita o si sovrascrive, mai entrambi.
    er = {v["campo"] for v in m["eredita"]}
    so = {v["campo"] for v in m["sovrascrive"]}
    for c in sorted(er & so):
        err(f"campo '{c}' e' insieme in `eredita` e in `sovrascrive`: decidere quale delle due")

    # --- `origine: terzo` obbliga a dire CHI e' il terzo.
    for v in m["sovrascrive"]:
        if v.get("origine") == "terzo" and not v.get("terzo"):
            err(f"sovrascrive['{v['campo']}']: origine e' 'terzo' ma il campo `terzo` e' vuoto")
        if v.get("origine", "modello") == "modello" and v.get("terzo"):
            err(f"sovrascrive['{v['campo']}']: `terzo` valorizzato ma origine non e' 'terzo'")

    # --- decisioni 33 (`schema-oggetti`) e 38 (`schema-modelli`): un modello con scheda propria non duplica i tratti.
    if d.get("monster_id") and m["aggiunge"]:
        err("monster_id e' valorizzato ma `aggiunge` non e' vuoto: i tratti stanno "
            "nella scheda del mostro, il modello la referenzia e non la ricopia")

    # --- decisione 40 (`modello-scarto-di-grado`), forma e conseguenze.
    sg = m["scarto_grado"]
    xp = sg["xp_2e"]
    if sg["forma"] == "proprio":
        if not d.get("monster_id"):
            err("scarto_grado.forma e' 'proprio' ma monster_id e' null: un grado proprio "
                "deve abitare una scheda di mostro, non il modello")
        if not sg.get("gs_proprio"):
            err("scarto_grado.forma e' 'proprio' ma gs_proprio e' vuoto")
    else:
        if sg.get("gs_proprio"):
            err(f"scarto_grado.gs_proprio valorizzato ma forma e' '{sg['forma']}': "
                "un modello senza profilo di combattimento fissato dalla fonte non ha un grado suo")
        if d.get("monster_id"):
            err(f"monster_id valorizzato ma scarto_grado.forma e' '{sg['forma']}': "
                "se esiste una scheda, il grado e' 'proprio'")

    # --- decisioni 35 (`repertori-sono-filtri`) e 40 (`modello-scarto-di-grado`): un valore di fonte registrato senza uso dichiarato
    #     e' una stima nascosta.
    if not xp["usato_per_derivare_gs"] and not xp["uso_dichiarato"]:
        err("scarto_grado.xp_2e: usato_per_derivare_gs e' false ma uso_dichiarato e' vuoto")

    forma_campi = {
        "modificatore": ("modificatore", ("valore", "valori_per_variante")),
        "assoluto": ("valore", ("modificatore", "valori_per_variante")),
        "assoluto_per_variante": ("valori_per_variante", ("modificatore", "valore")),
    }
    atteso, vietati = forma_campi[xp["forma"]]
    if xp.get(atteso) in (None, {}):
        err(f"scarto_grado.xp_2e: forma '{xp['forma']}' ma il campo '{atteso}' e' vuoto")
    for v in vietati:
        if xp.get(v) not in (None, {}):
            err(f"scarto_grado.xp_2e: forma '{xp['forma']}' ma e' valorizzato anche '{v}'")

    # --- le chiavi di valori_per_variante devono essere varianti vere.
    ids_var = {v["id"] for v in m.get("varianti", [])}
    for k in (xp.get("valori_per_variante") or {}):
        if k not in ids_var:
            err(f"scarto_grado.xp_2e.valori_per_variante: '{k}' non e' un id di `varianti`")
    if xp["forma"] == "assoluto_per_variante":
        for i in sorted(ids_var - set(xp.get("valori_per_variante") or {})):
            err(f"variante '{i}' senza XP in scarto_grado.xp_2e.valori_per_variante")

    # --- id di variante unici.
    visti = set()
    for v in m.get("varianti", []):
        if v["id"] in visti:
            err(f"id di variante duplicato: {v['id']}")
        visti.add(v["id"])

    # --- ruolo e campi della regola condivisa.
    for r in m.get("regole_condivise", []):
        if r["ruolo"] == "definizione":
            if r.get("definita_in"):
                err(f"regola '{r['id']}': ruolo 'definizione' ma `definita_in` e' valorizzato")
            if not r.get("testo_2e"):
                err(f"regola '{r['id']}': ruolo 'definizione' ma `testo_2e` e' vuoto")
        else:
            if not r.get("definita_in"):
                err(f"regola '{r['id']}': ruolo 'riferimento' ma `definita_in` e' vuoto")
            if r.get("testo_2e") or r.get("parametri_dichiarati"):
                err(f"regola '{r['id']}': un 'riferimento' non ricopia testo_2e ne' "
                    "parametri_dichiarati — quelli stanno nella definizione")


def coerenza_incrociata(modelli, err):
    """Controlli fra file: regole condivise, riferimenti alle schede."""
    definizioni = {}
    for mid, d in modelli.items():
        for r in d["mechanics_5e"].get("regole_condivise", []):
            if r["ruolo"] != "definizione":
                continue
            if r["id"] in definizioni:
                err(f"regola '{r['id']}' definita due volte: in "
                    f"'{definizioni[r['id']][0]}' e in '{mid}' — la definizione e' una sola")
            definizioni[r["id"]] = (mid, r)

    for mid, d in modelli.items():
        for r in d["mechanics_5e"].get("regole_condivise", []):
            dec = definizioni.get(r["id"])
            if r["ruolo"] == "riferimento":
                if dec is None:
                    err(f"{mid}: regola '{r['id']}' riferita ma mai definita")
                    continue
                if r["definita_in"] != dec[0]:
                    err(f"{mid}: regola '{r['id']}' dice di essere definita in "
                        f"'{r['definita_in']}', ma la definizione sta in '{dec[0]}'")
            if dec is None:
                continue
            attesi = {p["nome"] for p in dec[1].get("parametri_dichiarati", [])}
            dati = set(r["parametri"])
            for p in sorted(attesi - dati):
                err(f"{mid}: regola '{r['id']}' non da' un valore al parametro '{p}'")
            for p in sorted(dati - attesi):
                err(f"{mid}: regola '{r['id']}' da' il parametro '{p}', che la "
                    f"definizione in '{dec[0]}' non dichiara")

    mostri_dir = os.path.join(BASE, "mostri")
    mostri = ({os.path.splitext(os.path.basename(p))[0]
               for p in glob.glob(os.path.join(mostri_dir, "*.json"))}
              if os.path.isdir(mostri_dir) else set())
    for mid, d in modelli.items():
        if d.get("monster_id") and mostri and d["monster_id"] not in mostri:
            err(f"{mid}: monster_id '{d['monster_id']}' inesistente in dati/mostri/")


def main():
    schema = S.carica("modello.schema.json")
    v = S.validatore("modello.schema.json", schema)

    fuori = list(S.verifica_riferimenti())
    for m in fuori:
        print(f"\u2717 {m}")

    # LA SEDE DELL'ORIGINE, e la prova che il rilevatore ci vede. Un enum
    # ricopiato valida benissimo finche' le due copie coincidono: il difetto
    # non si vede dai dati, si vede solo guardando gli schemi. E su un
    # repository pulito un rilevatore rotto e uno funzionante tacciono uguale,
    # quindi `prova_di_se_stesso()` gli mette davanti difetti piantati.
    visti, quanti, prova = S.prova_di_se_stesso()
    fuori += prova
    for m in prova:
        print(f"\u2717 {m}")
    for m in S.verifica_origine():
        print(f"\u2717 {m}")
        fuori.append(m)

    files = sorted(glob.glob(os.path.join(BASE, "modelli", "*.json")))
    if not files:
        print("nessun file in dati/modelli/")
        return 1

    modelli, totale = {}, len(fuori)
    for p in files:
        nome = os.path.basename(p)
        d = json.load(open(p, encoding="utf-8"))
        errori = []

        for e in sorted(v.iter_errors(d), key=lambda e: list(e.path)):
            errori.append(f"[schema] {'.'.join(map(str, e.path)) or '(radice)'}: {e.message[:200]}")

        if not errori:
            coerenza_file(d, errori.append)

        if d["id"] + ".json" != nome:
            errori.append(f"il nome del file non corrisponde all'id ({d['id']})")
        if d["id"] in modelli:
            errori.append(f"id duplicato: {d['id']}")
        modelli[d["id"]] = d

        if errori:
            totale += len(errori)
            print(f"✗ {nome}")
            for e in errori:
                print(f"    {e}")
        else:
            print(f"✓ {nome}")

    incrociati = []
    coerenza_incrociata(modelli, incrociati.append)
    if incrociati:
        totale += len(incrociati)
        print("✗ controlli incrociati")
        for e in incrociati:
            print(f"    {e}")
    else:
        print("✓ controlli incrociati")

    print(f"\u2713 sede dell'origine: {visti}/{quanti} difetti piantati visti, "
          f"{len(fuori)} problemi negli schemi.")
    print(f"\n{len(files)} file controllati, {totale} errori.")
    return 1 if totale else 0


if __name__ == "__main__":
    sys.exit(main())
