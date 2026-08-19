#!/usr/bin/env python3
"""
RAPPORTO DIAGNOSTICO — soddisfacibilita' dei requisiti 2e sotto le regole 5e.

DOMANDA
    I requisiti di caratteristica estratti da Tales of the Lance presuppongono
    statistiche tirate con 3d6 su scala 3-18. In 5e con array standard
    (15,14,13,12,10,8) o point-buy a 27 punti il massimo pre-razziale e' 15.
    Alcuni requisiti possono quindi risultare impossibili, o forzare l'intera
    distribuzione delle caratteristiche.

MODELLO
    In AD&D 2e gli aggiustamenti razziali si applicano al tiro e il risultato
    deve cadere nell'intervallo min/max. Qui si assume lo stesso: i requisiti
    valgono sul punteggio FINALE, dopo gli aggiustamenti.

    - Array standard: 15,14,13,12,10,8 assegnati liberamente -> 720 permutazioni.
    - Point-buy 27: punteggi base da 8 a 15, costo 0/1/2/3/4/5/7/9, totale <= 27.

NON MODIFICA NULLA. E' solo un rapporto.

Uso:  python3 dati/analisi_soddisfacibilita.py [--md]
"""

import glob
import itertools
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
CAR = ["str", "dex", "con", "int", "wis", "cha"]

ARRAY_STD = (15, 14, 13, 12, 10, 8)
COSTO = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
BUDGET = 27


def carica(sub):
    return [json.load(open(p, encoding="utf-8"))
            for p in sorted(glob.glob(os.path.join(BASE, sub, "*.json")))]


def vincoli_razza(r):
    """(minimi, massimali, aggiustamenti) come dizionari per caratteristica."""
    s = r["source_2e"]
    lo = {c: (s["ability_requirements"][c]["min"] or 0) for c in CAR}
    hi = {c: (s["ability_requirements"][c]["max"] or 99) for c in CAR}
    adj = {c: (s["ability_adjustments"] or {}).get(c, 0) for c in CAR}
    return lo, hi, adj


def ok(base, lo, hi, adj, min_classe=None):
    """base = tupla di 6 punteggi pre-razziali, nell'ordine di CAR."""
    for i, c in enumerate(CAR):
        v = base[i] + adj[c]
        if v < lo[c] or v > hi[c]:
            return False
        if min_classe and v < min_classe.get(c, 0):
            return False
    return True


def conta_array(lo, hi, adj, min_classe=None):
    return sum(1 for p in itertools.permutations(ARRAY_STD)
               if ok(p, lo, hi, adj, min_classe))


def combinazioni_pointbuy():
    """Tutte le combinazioni di 6 punteggi 8-15 entro il budget."""
    out = []
    for t in itertools.product(range(8, 16), repeat=6):
        if sum(COSTO[v] for v in t) <= BUDGET:
            out.append(t)
    return out


PB = None


def conta_pointbuy(lo, hi, adj, min_classe=None):
    global PB
    if PB is None:
        PB = combinazioni_pointbuy()
    return sum(1 for t in PB if ok(t, lo, hi, adj, min_classe))


def analizza():
    razze = carica("razze")
    classi = carica("classi")

    righe = []
    for r in razze:
        lo, hi, adj = vincoli_razza(r)
        n_arr = conta_array(lo, hi, adj)
        n_pb = conta_pointbuy(lo, hi, adj)

        # classi ammesse a questa razza secondo la tabella del manuale
        voci = r["source_2e"].get("class_level_limits", [])
        nomi_tab = {v["class"] for v in voci}

        accessibili, impossibili = [], []
        for c in classi:
            # la classe e' disponibile alla razza?
            restr = c["source_2e"].get("race_restriction")
            if restr and r["id"] not in restr:
                continue
            # La tabella Class/Race Combinations elenca "Knight of Solamnia"
            # come voce unica: copre tutti e tre gli ordini, non solo la Corona.
            nomi_classe = {c["name"]["en"]}
            if c["order"] == "cavaliere-solamnia":
                nomi_classe.add("Knight of Solamnia")
            if nomi_tab and not (nomi_classe & nomi_tab):
                # la tabella non la elenca: gia' preclusa per decisione 2,
                # non e' un'impossibilita' matematica
                continue
            mc = c["source_2e"].get("ability_minimums") or {}
            a = conta_array(lo, hi, adj, mc)
            p = conta_pointbuy(lo, hi, adj, mc)
            if a == 0 and p == 0:
                impossibili.append((c["id"], mc))
            else:
                accessibili.append((c["id"], a, p))

        righe.append({
            "id": r["id"],
            "nome": r["name"]["it"],
            "array": n_arr,
            "pointbuy": n_pb,
            "min": {c: lo[c] for c in CAR if lo[c] > 0},
            "max": {c: hi[c] for c in CAR if hi[c] < 99},
            "adj": {c: adj[c] for c in CAR if adj[c]},
            "accessibili": accessibili,
            "impossibili": impossibili,
        })
    return righe, classi


def stampa(righe, classi, md=False):
    tot_pb = len(PB) if PB else 0
    print(f"Spazio di ricerca: 720 permutazioni dell'array standard, "
          f"{tot_pb:,} combinazioni point-buy entro 27 punti.\n".replace(",", "."))

    intest = "| razza | array std | point-buy | verdetto |"
    print(intest)
    print("|---|---:|---:|---|")
    for r in righe:
        if r["array"] == 0 and r["pointbuy"] == 0:
            v = "**IMPOSSIBILE**"
        elif r["array"] == 0:
            v = "**solo point-buy**"
        elif r["array"] <= 6:
            v = f"**quasi obbligata** ({r['array']} disposizioni)"
        elif r["array"] <= 24:
            v = "molto vincolata"
        else:
            v = "libera"
        print(f"| {r['nome'][:34]} | {r['array']:3}/720 | {r['pointbuy']:6}/{tot_pb} | {v} |")

    print("\n\n## Combinazioni razza+classe matematicamente impossibili\n")
    tot = 0
    for r in righe:
        for cid, mc in r["impossibili"]:
            req = ", ".join(f"{k.upper()} {v}" for k, v in mc.items())
            print(f"- **{r['nome']}** + `{cid}` — la classe richiede {req}")
            tot += 1
    if not tot:
        print("Nessuna: ogni combinazione ammessa dalla tabella del manuale resta raggiungibile.")

    print("\n\n## Difficolta' per classe (a prescindere dalla razza)\n")
    print("Quante razze possono accedere a ciascuna classe, fra quelle a cui la "
          "tabella del manuale la concede.\n")
    print("| classe | requisiti | razze ammesse | di cui raggiungibili |")
    print("|---|---|---:|---:|")
    for c in sorted(classi, key=lambda x: x["id"]):
        mc = c["source_2e"].get("ability_minimums") or {}
        if not mc:
            continue
        ammesse = raggiungibili = 0
        for r in righe:
            if any(cid == c["id"] for cid, _ in r["impossibili"]):
                ammesse += 1
            elif any(cid == c["id"] for cid, _, _ in r["accessibili"]):
                ammesse += 1
                raggiungibili += 1
        if not ammesse:
            continue
        req = " ".join(f"{k.upper()}{v}" for k, v in mc.items())
        segno = " ⚠" if raggiungibili < ammesse else ""
        print(f"| `{c['id']}` | {req} | {ammesse} | {raggiungibili}{segno} |")

    print("\n\n## Dettaglio per razza\n")
    for r in righe:
        print(f"### {r['nome']} (`{r['id']}`)")
        print(f"- minimi: {r['min'] or 'nessuno'}")
        print(f"- massimali: {r['max'] or 'nessuno'}")
        print(f"- aggiustamenti: {r['adj'] or 'nessuno'}")
        print(f"- distribuzioni valide: {r['array']}/720 array standard, "
              f"{r['pointbuy']}/{tot_pb} point-buy")
        if r["accessibili"]:
            peggiori = sorted(r["accessibili"], key=lambda x: x[1])[:4]
            print("- classi piu' vincolate: " + ", ".join(
                f"`{c}` ({a}/720)" for c, a, _ in peggiori))
        print()


def main():
    righe, classi = analizza()
    stampa(righe, classi, "--md" in sys.argv)
    rapporto_negativi()


# ==========================================================================
# COMPITO B — aggiustamenti negativi
#
# In 5e 2014 le razze hanno SOLO bonus positivi, per un totale che si aggira
# sempre su +3 (es. +2/+1, oppure +1 a tutte e sei per il mezzelfo variante).
# Gli aggiustamenti negativi della 2e non hanno equivalente: vanno decisi.
# ==========================================================================

STANDARD_5E = 3    # somma tipica dei bonus razziali in 5e 2014


def rapporto_negativi():
    razze = carica("razze")
    print("\n\n# COMPITO B — aggiustamenti negativi\n")
    print(f"In 5e 2014 le razze hanno solo bonus positivi, per un totale che si "
          f"aggira su **+{STANDARD_5E}**. Gli aggiustamenti negativi della 2e non "
          f"hanno equivalente.\n")
    print("| razza | negativi | massimale sulla stessa caratteristica | doppia penalita' | positivi | netto | scarto da +3 |")
    print("|---|---|---|---|---:|---:|---:|")

    for r in razze:
        s = r["source_2e"]
        adj = s["ability_adjustments"] or {}
        neg = {k: v for k, v in adj.items() if v < 0}
        pos = {k: v for k, v in adj.items() if v > 0}
        if not neg:
            continue

        voci_neg, voci_max, doppie = [], [], []
        for k, v in sorted(neg.items()):
            voci_neg.append(f"{k.upper()} {v:+d}")
            mx = s["ability_requirements"][k]["max"]
            if mx is not None and mx < 18:
                voci_max.append(f"{k.upper()} max {mx}")
                doppie.append(k.upper())
            else:
                voci_max.append("—")

        netto = sum(adj.values())
        print(f"| {r['name']['it'][:30]} | {', '.join(voci_neg)} | {', '.join(voci_max)} | "
              f"{', '.join(doppie) or 'no'} | "
              f"{', '.join(f'{k.upper()} {v:+d}' for k, v in sorted(pos.items())) or '—'} | "
              f"{netto:+d} | {netto - STANDARD_5E:+d} |")

    print("\n**Tutte le razze, anche quelle senza negativi, per confronto:**\n")
    print("| razza | aggiustamenti | netto | scarto da +3 |")
    print("|---|---|---:|---:|")
    for r in sorted(razze, key=lambda x: sum((x["source_2e"]["ability_adjustments"] or {}).values())):
        adj = r["source_2e"]["ability_adjustments"] or {}
        netto = sum(adj.values())
        testo = ", ".join(f"{k.upper()} {v:+d}" for k, v in sorted(adj.items())) or "nessuno"
        print(f"| {r['name']['it'][:34]} | {testo} | {netto:+d} | {netto - STANDARD_5E:+d} |")


if __name__ == "__main__":
    main()
