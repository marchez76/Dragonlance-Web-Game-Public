import pdfplumber, sys, re

def gutter(pg):
    """Trova il gutter reale: la colonna verticale piu' larga senza parole, vicino al centro."""
    ws = pg.extract_words()
    if not ws: return pg.width/2
    W = int(pg.width)
    occ = [0]*(W+1)
    for w in ws:
        for x in range(max(0,int(w['x0'])), min(W,int(w['x1']))+1):
            occ[x] = 1
    lo, hi = int(W*0.35), int(W*0.65)
    best, run_s = None, None
    for x in range(lo, hi+1):
        if occ[x] == 0:
            if run_s is None: run_s = x
        else:
            if run_s is not None:
                if best is None or (x-run_s) > (best[1]-best[0]): best = (run_s, x)
                run_s = None
    if run_s is not None and (best is None or (hi-run_s) > (best[1]-best[0])): best = (run_s, hi)
    return (best[0]+best[1])/2 if best else pg.width/2

def page_cols(pg):
    g = gutter(pg)
    out = []
    for x0, x1 in ((0, g), (g, pg.width)):
        t = pg.crop((x0, 0, x1, pg.height)).extract_text(x_tolerance=1.5) or ""
        out.append(t)
    return out, g

if __name__ == "__main__":
    pdf, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    with pdfplumber.open(pdf) as p:
        for i in range(a, min(b, len(p.pages))):
            cols, g = page_cols(p.pages[i])
            print(f"\n{'='*70}\n[[PAGINA PDF {i}]] gutter={g:.0f}\n{'='*70}")
            for j, c in enumerate(cols):
                print(f"\n--- col {j} ---\n{c}")
