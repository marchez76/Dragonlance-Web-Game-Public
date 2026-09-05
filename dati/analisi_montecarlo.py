#!/usr/bin/env python3
"""
RAPPORTO DIAGNOSTICO — probabilita' di qualificarsi con 4d6 scarta il minore.

DOMANDA (compito C, 12 agosto 2026)
    Adottata la decisione 8 (`generazione-caratteristiche`), la domanda non e' piu' *se* una combinazione
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

DA DOVE LEGGE, e perche' e' cambiato il 05/09/2026
    Le classi di una razza vengono da `dati/_classi_ammesse.py`, sede della
    decisione 58 (`telaio-apre-classe-filtra`); i vincoli vengono da
    `mechanics_5e` tramite `motore/generazione.py`. Fino a oggi questo file
    aveva una risoluzione propria delle coppie razza+classe e leggeva
    `source_2e` — le stesse due strutture doppie di
    `analisi_soddisfacibilita.py`, nello stesso punto e per la stessa
    ragione. Il confronto fra i due strati e' in coda al rapporto: la
    lettura nuova si mostra, non si assume.

NON MODIFICA NULLA.

Uso:  python3 dati/analisi_montecarlo.py [iterazioni] > dati/RAPPORTO-montecarlo.md
"""

import os
import sys

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
sys.path.insert(0, BASE)
sys.path.insert(0, RADICE)

import _classi_ammesse as CA        # noqa: E402
import verifica_strati as VS        # noqa: E402
from motore import generazione as G  # noqa: E402

CAR = G.CAR
N_DEFAULT = 200_000
SOGLIA_RARA = 1.0    # percentuale sotto la quale segnalare


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

    razze, classi = CA.razze(), CA.classi()
    per_id = {c["id"]: c for c in classi}
    tiro = tira_4d6(n, rng)

    print(f"# Probabilita' di qualificazione con 4d6 scarta il minore\n")
    print(f"Simulazione Monte Carlo, **{n:,} iterazioni** per combinazione.\n"
          .replace(",", "."))

    risultati = []
    for r in razze:
        adj = G.aggiustamenti(r)
        formule = G.formule_razziali(r)
        proprio = len(formule) == len(CAR)

        if proprio:
            colonne = {c: tira_formula(formule[c], n, rng) + adj.get(c, 0)
                       for c in CAR}
        else:
            base = tiro + np.array([adj.get(c, 0) for c in CAR])

        lo, hi = G.intervalli(r)
        lo_r = [lo[c] for c in CAR]
        hi_r = [hi[c] for c in CAR]

        p_razza = (soddisfa_fisso(colonne, lo_r, hi_r) if proprio
                   else soddisfa_libero(base, lo_r, hi_r)).mean() * 100

        # Le classi le decide la sede, non una seconda risoluzione. Passano
        # quelle che il telaio apre e il filtro lascia — e in piu' quelle
        # che il filtro toglie SOLO per l'ingresso, che sono i gradi
        # solamnici e le tre Vesti. La differenza e' reale: chi e' escluso
        # per razza o per un minimo oltre il proprio massimale non ha una
        # probabilita' bassa, non ne ha una affatto; chi e' escluso per
        # ingresso ci arriva in sequenza
        # (decisione 5, `cavalieri-solamnia`), e la domanda «quanto e' raro
        # qualificarsi come Cavaliere della Rosa» resta sensata. Le altre esclusioni
        # restano fuori.
        classi_r = []
        for pe in G.percorsi(r, classi):
            solo_ingresso = (not pe.ammessa
                             and all(k == "ingresso" for k, _ in pe.motivi))
            if not pe.ammessa and not solo_ingresso:
                continue
            lo_c, hi_c = G.intervalli(r, per_id[pe.classe])
            p = (soddisfa_fisso(colonne, [lo_c[c] for c in CAR],
                                [hi_c[c] for c in CAR]) if proprio
                 else soddisfa_libero(base, [lo_c[c] for c in CAR],
                                      [hi_c[c] for c in CAR])).mean() * 100
            classi_r.append((pe.classe, p))

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
    print("Le tabelle elencano le classi che il telaio apre e il filtro "
          "lascia passare, piu' quelle che il filtro toglie per il solo "
          "INGRESSO — i gradi solamnici e le tre Vesti, a cui si arriva in "
          "sequenza da un'altra classe. Una classe esclusa per razza o per "
          "un minimo oltre il massimale non compare: non ha una "
          "probabilita' bassa, non ne ha una.\n")
    for r, p, cl in risultati:
        print(f"### {r['name']['it']} — {p:.2f}% supera i soli vincoli razziali\n")
        print("| classe | qualificati |")
        print("|---|---:|")
        for cid, pc in cl:
            print(f"| `{cid}` | {pc:6.2f}% |")
        print()

    div, dichiarati, misure = VS.verifica()
    print("\n## I due strati a confronto\n")
    print(f"Le percentuali qui sopra sono calcolate su `mechanics_5e`. "
          f"`verifica_strati.py` confronta {misure['razze']} razze e "
          f"{misure['classi']} classi contro `source_2e`: scarti dichiarati "
          f"**{misure['scarti_dichiarati']}**, divergenze non dichiarate "
          f"**{misure['divergenze']}**. Uno scarto dichiarato cambia una "
          f"probabilita' di questo rapporto; una divergenza non dichiarata la "
          f"cambierebbe senza che nessuno se ne accorga, ed e' la ragione per "
          f"cui il confronto sta in coda al rapporto e non solo in un "
          f"validatore che nessuno guarda quando legge i numeri.\n")
    if dichiarati:
        print("| entita' | grandezza | scarto |")
        print("|---|---|---|")
        for chi, tipo, det in dichiarati:
            print(f"| {chi} | {tipo} | {det} |")
    for chi, tipo, det in div:
        print(f"- **DIVERGENZA NON DICHIARATA** {chi} — {tipo}: {det}")


if __name__ == "__main__":
    main()
