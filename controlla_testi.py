#!/usr/bin/env python3
"""
Cerca in Testi/ le pagine rimaste con le colonne fuse.

PERCHE' SERVE UN CONTROLLO DEDICATO
    Il primo controllo che avevo scritto cercava righe con sei o piu' spazi
    consecutivi, la firma tipica di pdftotext -layout. Ma quando il gutter non
    viene riconosciuto e la pagina viene estratta come colonna singola, le due
    colonne si saldano con spazi SINGOLI e quel controllo non le vede.
    Dava zero difetti su 1.116 pagine difettose.

    Questo controllo usa invece la geometria del testo: in una pagina estratta
    correttamente le righe sono lunghe quanto una colonna; in una pagina fusa
    sono lunghe circa il doppio. Confrontando ogni pagina con la mediana del
    suo stesso libro il criterio funziona anche su impaginati diversi.

Uso:  python3 controlla_testi.py [--dettaglio]
Esce con codice 1 se trova pagine sospette.
"""

import glob
import os
import re
import statistics
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SOGLIA = 1.55   # una pagina lunga oltre 1,55 volte la mediana del libro


def analizza(percorso):
    t = open(percorso, encoding="utf-8", errors="replace").read()
    if t.startswith("[[origine: OCR]]"):
        return None
    pezzi = re.split(r"\[\[p\.(\d+)\]\]", t)[1:]
    mediane = []
    for i in range(0, len(pezzi) - 1, 2):
        righe = [len(r) for r in pezzi[i + 1].split("\n") if len(r.strip()) > 40]
        if len(righe) >= 6:
            mediane.append((int(pezzi[i]), statistics.median(righe)))
    if len(mediane) < 10:
        return None
    base = statistics.median([m for _, m in mediane])
    fuse = [p for p, m in mediane if m > base * SOGLIA]
    return base, fuse, len(mediane)


def main():
    dettaglio = "--dettaglio" in sys.argv
    esiti = []
    for f in sorted(glob.glob(os.path.join(BASE, "Testi", "*", "*.txt"))):
        r = analizza(f)
        if r is None:
            continue
        base, fuse, tot = r
        esiti.append((len(fuse), tot, os.path.basename(f)[:-4], base, fuse))

    analizzate = sum(e[1] for e in esiti)
    difettose = sum(e[0] for e in esiti)
    sporchi = [e for e in esiti if e[0]]

    print(f"{len(esiti)} file analizzati, {analizzate:,} pagine".replace(",", "."))
    if not difettose:
        print("nessuna pagina con colonne fuse")
        return 0

    print(f"{difettose:,} pagine sospette ({100*difettose/analizzate:.1f}%) "
          f"in {len(sporchi)} file".replace(",", "."))
    for n, tot, nome, base, fuse in sorted(sporchi, reverse=True)[:20]:
        print(f"   {n:4}/{tot:4}  {nome[:44]:44} riga tipica {base:.0f} car")
        if dettaglio:
            print(f"          pagine: {', '.join(map(str, fuse[:25]))}"
                  + (" …" if len(fuse) > 25 else ""))
    return 1


if __name__ == "__main__":
    sys.exit(main())
