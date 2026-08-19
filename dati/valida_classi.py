#!/usr/bin/env python3
"""
Valida dati/classi/*.json contro lo schema, piu' controlli di coerenza interna
e CONTROLLO INCROCIATO con dati/razze/*.json.

Il controllo incrociato e' il piu' utile: le razze e le classi sono state
estratte da due tabelle diverse dello stesso manuale, quindi devono raccontare
la stessa storia. Se una razza dichiara di poter fare il Tinker ma il Tinker
dichiara di essere riservato agli gnomi, una delle due trascrizioni e' sbagliata.

Uso:  python3 dati/valida_classi.py
"""

import glob
import json
import os
import sys

import jsonschema

BASE = os.path.dirname(os.path.abspath(__file__))
Validator = getattr(jsonschema, "Draft202012Validator", None) or jsonschema.Draft7Validator

# Nomi usati nella tabella Class/Race Combinations -> id delle nostre classi.
# Le voci non mappate sono classi standard del PHB 2e, senza scheda dedicata.
MAPPA_TABELLA = {
    "Knight of Solamnia": "cavaliere-corona",
    "Cavalier": "cavaliere",
    "Mariner": "mariner",
    "Barbarian": "barbaro",
    "High Sorcerer": "mago-alta-stregoneria",
    "Mage (Renegade)": "mago-rinnegato",
    "Holy Orders": "sacerdote-ordini-sacri",
    "Priest (heathen)": "sacerdote-eretico",
    "Druid (heathen)": "sacerdote-eretico",
    "Handler": "handler",
    "Tinker": "tinker",
}


def coerenza(d, err):
    s = d["source_2e"]

    for k, v in s["ability_minimums"].items():
        if not (1 <= v <= 25):
            err(f"minimo {k} = {v} implausibile")

    prog = s.get("progression") or []
    if prog:
        if prog[0]["level"] != s["entry_level"]:
            err(f"la progressione parte dal livello {prog[0]['level']} "
                f"ma entry_level e' {s['entry_level']}")
        if prog[0]["xp"] != 0:
            err(f"la progressione non parte da 0 PE ma da {prog[0]['xp']}")
        for a, b in zip(prog, prog[1:]):
            if b["level"] != a["level"] + 1:
                err(f"salto di livello nella progressione: {a['level']} -> {b['level']}")
            if b["xp"] <= a["xp"]:
                err(f"i PE non crescono fra il livello {a['level']} e il {b['level']}")

    sp = s.get("spell_progression")
    if sp:
        livelli = sorted(int(k) for k in sp)
        for a, b in zip(livelli, livelli[1:]):
            if b != a + 1:
                err(f"salto nella tabella incantesimi: {a} -> {b}")
        larghezze = {len(v) for v in sp.values()}
        if len(larghezze) != 1:
            err(f"la tabella incantesimi ha righe di lunghezza diversa: {larghezze}")
        # il totale degli incantesimi non deve mai diminuire salendo di livello
        for a, b in zip(livelli, livelli[1:]):
            if sum(sp[str(b)]) < sum(sp[str(a)]):
                err(f"gli incantesimi totali calano fra il livello {a} e il {b}")

    if s.get("xp_bonus"):
        ab = s["xp_bonus"]["ability"]
        minimo = s["ability_minimums"].get(ab)
        if minimo is not None and s["xp_bonus"]["threshold"] < minimo:
            err(f"la soglia del bonus PE ({s['xp_bonus']['threshold']}) "
                f"e' sotto il minimo richiesto per {ab} ({minimo})")


def incrociato(classi, razze, err):
    """La tabella Class/Race Combinations delle razze deve concordare
    con le restrizioni di razza dichiarate dalle classi."""
    per_id = {c["id"]: c for c in classi}

    for r in razze:
        for voce in r["source_2e"].get("class_level_limits", []):
            cid = MAPPA_TABELLA.get(voce["class"])
            if cid is None:
                continue
            c = per_id.get(cid)
            if c is None:
                err(f"{r['id']}: la tabella cita '{voce['class']}' ma la classe {cid} non esiste")
                continue
            restr = c["source_2e"].get("race_restriction")
            if restr and r["id"] not in restr:
                err(f"CONTRADDIZIONE: la razza {r['id']} puo' prendere '{voce['class']}' "
                    f"(tetto {voce['limit']}) ma la classe {cid} e' riservata a {restr}")

    # e viceversa: una classe riservata a una razza deve comparire fra i suoi limiti
    per_razza = {r["id"]: {v["class"] for v in r["source_2e"].get("class_level_limits", [])}
                 for r in razze}
    inverso = {v: k for k, v in MAPPA_TABELLA.items()}
    for c in classi:
        restr = c["source_2e"].get("race_restriction")
        nome_tab = inverso.get(c["id"])
        if not restr or not nome_tab:
            continue
        for rid in restr:
            if rid not in per_razza:
                err(f"{c['id']}: race_restriction cita la razza inesistente '{rid}'")
            elif not per_razza[rid]:
                # Gli umani non compaiono nella tabella Class/Race Combinations
                # perche' in 2e non hanno limiti di livello: assenza attesa, non errore.
                continue
            elif nome_tab not in per_razza[rid]:
                err(f"{c['id']} e' riservata a {rid}, ma '{nome_tab}' non compare "
                    f"fra i class_level_limits di quella razza")

    # le catene di ordini devono essere ben formate
    for c in classi:
        rq = c.get("requires_class")
        if rq and rq not in per_id:
            err(f"{c['id']}: requires_class punta a '{rq}' che non esiste")
        if c.get("tier") and c["tier"] > 1 and not rq:
            err(f"{c['id']}: tier {c['tier']} senza requires_class")


def main():
    schema = json.load(open(os.path.join(BASE, "schema", "classe.schema.json")))
    Validator.check_schema(schema)
    v = Validator(schema)

    files = sorted(glob.glob(os.path.join(BASE, "classi", "*.json")))
    classi = [json.load(open(p, encoding="utf-8")) for p in files]
    razze = [json.load(open(p, encoding="utf-8"))
             for p in sorted(glob.glob(os.path.join(BASE, "razze", "*.json")))]

    totale = 0
    for p, d in zip(files, classi):
        errori = []
        for e in sorted(v.iter_errors(d), key=lambda e: list(e.path)):
            errori.append(f"[schema] {'.'.join(map(str, e.path)) or '(radice)'}: {e.message[:120]}")
        if not errori:
            coerenza(d, errori.append)
        if errori:
            totale += len(errori)
            print(f"✗ {os.path.basename(p)}")
            for e in errori:
                print(f"    {e}")
        else:
            print(f"✓ {os.path.basename(p)}")

    print("\n--- controllo incrociato razze/classi ---")
    incr = []
    incrociato(classi, razze, incr.append)
    if incr:
        totale += len(incr)
        for e in incr:
            print(f"    ✗ {e}")
    else:
        print("    ✓ nessuna contraddizione fra le due tabelle")

    print(f"\n{len(files)} classi e {len(razze)} razze controllate, {totale} errori.")
    return 1 if totale else 0


if __name__ == "__main__":
    sys.exit(main())
