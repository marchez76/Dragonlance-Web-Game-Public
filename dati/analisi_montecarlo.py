#!/usr/bin/env python3
"""
RAPPORTO DIAGNOSTICO — probabilita' di qualificarsi con 4d6 scarta il minore.

DOMANDA (compito C, 12 agosto 2026)
    Adottata la decisione 9, la domanda non e' piu' *se* una combinazione
    razza+classe sia possibile, ma **quanto e' rara**. In 2e qualificarsi come
    Cavalier era raro per design: serve sapere quali percorsi restano da eroe
    raro e quali sono ordinari.

MODELLO
    - Si tirano sei punteggi con 4d6 scarta il minore, liberamente assegnabili.
    - L'Aghar usa i dadi propri prescritti dal manuale, fissi per caratteristica:
      per lui non c'e' liberta' di assegnazione.
    - Gli aggiustamenti razziali si sommano al tiro; i requisiti valgono sul
      punteggio finale.
    - Una combinazione e' soddisfatta se ESISTE un modo di assegnare i sei
      valori che rispetti tutti i vincoli di razza e di classe.

    Il controllo di esistenza usa un greedy corretto per questa struttura: si
    ordinano le caratteristiche per massimale crescente e a ciascuna si assegna
    il valore ammissibile piu' piccolo disponibile. Chi ha il tetto piu' basso
    sceglie per primo, quindi non gli viene sottratto un valore che solo lui
    poteva usare.

NON MODIFICA NULLA.

Uso:  python3 dati/analisi_montecarlo.py [iterazioni]
"""

import glob
import json
import os
import sys

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
CAR = ["str", "dex", "con", "int", "wis", "cha"]
N_DEFAULT = 200_000
SOGLIA_RARA = 1.0    # percentuale sotto la quale segnalare


def carica(sub):
    return [json.load(open(p, encoding="utf-8"))
            for p in sorted(glob.glob(os.path.join(BASE, sub, "*.json")))]


def tira_4d6(n, rng):
    """n x 6 punteggi con 4d6 scarta il minore."""
    d = rng.integers(1, 7, size=(n, 6, 4))
    d.sort(axis=2)
    return d[:, :, 1:].sum(axis=2)


def tira_formula(formula, n, rng):
    import re
    m = re.match(r"^(\d+)d(\d+)(?:([+-])(\d+))?$", formula.replace(" ", ""))
    nd, facce = int(m.group(1)), int(m.group(2))
    tot = rng.integers(1, facce + 1, size=(n, nd)).sum(axis=1)
    if m.group(3):
        tot = tot + int(m.group(4)) * (1 if m.group(3) == "+" else -1)
    return tot


def soddisfa_libero(valori, lo, hi):
    """valori: N x 6 (assegnabili liberamente). lo/hi: liste di 6 soglie."""
    n = valori.shape[0]
    V = np.sort(valori, axis=1)
    usato = np.zeros_like(V, dtype=bool)
    vivo = np.ones(n, dtype=bool)
    # chi ha il massimale piu' basso sceglie per primo
    for c in sorted(range(6), key=lambda i: hi[i]):
        amm = (~usato) & (V >= lo[c]) & (V <= hi[c])
        ha = amm.any(axis=1)
        vivo &= ha
        primo = amm.argmax(axis=1)
        usato[np.arange(n), primo] |= ha
    return vivo


def soddisfa_fisso(colonne, lo, hi):
    """colonne: dict caratteristica -> array N. Nessuna liberta' di assegnazione."""
    vivo = None
    for i, c in enumerate(CAR):
        v = colonne[c]
        ok = (v >= lo[i]) & (v <= hi[i])
        vivo = ok if vivo is None else (vivo & ok)
    return vivo


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else N_DEFAULT
    rng = np.random.default_rng(20260812)

    razze, classi = carica("razze"), carica("classi")
    tiro = tira_4d6(n, rng)

    print(f"# Probabilita' di qualificazione con 4d6 scarta il minore\n")
    print(f"Simulazione Monte Carlo, **{n:,} iterazioni** per combinazione.\n"
          .replace(",", "."))

    risultati = []
    for r in razze:
        s = r["source_2e"]
        req = s["ability_requirements"]
        adj = s.get("ability_adjustments") or {}
        formule = {k: v for k, v in (s.get("ability_generation") or {}).items()
                   if k != "all" and k in CAR}
        proprio = len(formule) == len(CAR)

        if proprio:
            colonne = {c: tira_formula(formule[c], n, rng) + adj.get(c, 0) for c in CAR}
        else:
            base = tiro + np.array([adj.get(c, 0) for c in CAR])

        lo_r = [req[c]["min"] or 3 for c in CAR]
        hi_r = [req[c]["max"] or 99 for c in CAR]

        p_razza = (soddisfa_fisso(colonne, lo_r, hi_r) if proprio
                   else soddisfa_libero(base, lo_r, hi_r)).mean() * 100

        nomi_tab = {v["class"] for v in s.get("class_level_limits", [])}
        classi_r = []
        for c in classi:
            restr = c["source_2e"].get("race_restriction")
            if restr and r["id"] not in restr:
                continue
            nomi = {c["name"]["en"]}
            if c["order"] == "cavaliere-solamnia":
                nomi.add("Knight of Solamnia")
            if nomi_tab and not (nomi & nomi_tab):
                continue
            mc = c["source_2e"].get("ability_minimums") or {}
            lo_c = [max(lo_r[i], mc.get(cc, 0)) for i, cc in enumerate(CAR)]
            p = (soddisfa_fisso(colonne, lo_c, hi_r) if proprio
                 else soddisfa_libero(base, lo_c, hi_r)).mean() * 100
            classi_r.append((c["id"], p))

        risultati.append((r, p_razza, sorted(classi_r, key=lambda x: x[1])))

    print("## Probabilita' per razza (solo vincoli razziali)\n")
    print("| razza | qualificati | 1 personaggio ogni |")
    print("|---|---:|---:|")
    for r, p, _ in sorted(risultati, key=lambda x: x[1]):
        ogni = f"{100/p:,.1f}".replace(",", ".") if p > 0 else "—"
        print(f"| {r['name']['it'][:34]} | {p:6.2f}% | {ogni} |")

    print("\n\n## Combinazioni sotto l'1% — le classi da eroe raro\n")
    rare = []
    for r, _, cl in risultati:
        for cid, p in cl:
            if p < SOGLIA_RARA:
                rare.append((p, r["name"]["it"], cid))
    if rare:
        print("| razza | classe | qualificati | 1 ogni |")
        print("|---|---|---:|---:|")
        for p, nome, cid in sorted(rare):
            ogni = f"{100/p:,.0f}".replace(",", ".") if p > 0 else "mai"
            print(f"| {nome[:28]} | `{cid}` | {p:6.3f}% | {ogni} |")
    else:
        print("Nessuna combinazione sotto l'1%.")

    print("\n\n## Dettaglio per razza\n")
    for r, p, cl in risultati:
        print(f"### {r['name']['it']} — {p:.2f}% supera i soli vincoli razziali\n")
        print("| classe | qualificati |")
        print("|---|---:|")
        for cid, pc in cl:
            print(f"| `{cid}` | {pc:6.2f}% |")
        print()


if __name__ == "__main__":
    main()
