#!/usr/bin/env python3
"""
Ri-estrazione a colonne della libreria — motore incrementale ripartibile.

PERCHE'
    I .txt in Estratti/ sono stati prodotti con pdftotext -layout: le due
    colonne di pagina finiscono fuse riga per riga, con il testo di una
    colonna mescolato a quello dell'altra. Sono leggibili da un umano ma
    inaffidabili per il parsing automatico.

    Questo script ritaglia ogni pagina lungo il gutter reale, estrae le
    colonne separatamente e le concatena nell'ordine di lettura corretto.

COME
    Il sandbox termina ogni processo alla fine della singola chiamata, quindi
    non e' possibile un job continuo. Come ocrstep.py, questo motore lavora
    per un budget di secondi, salva lo stato pagina per pagina e poi esce.
    Rilanciandolo riprende esattamente da dove si era fermato.

        python3 colstep.py 120     ~120 secondi di lavoro
        python3 colstep.py 120 Dragonlance    solo quella cartella
        python3 colstep.py --stato            avanzamento senza lavorare

FORMATO DI USCITA
    Testi/<cartella>/<nome>.txt con marcatori di pagina:

        [[p.57]]
        ...testo della colonna sinistra...
        ...testo della colonna destra...

    Il marcatore usa l'indice 0-based della pagina PDF, lo stesso che
    finisce nel campo `pages_pdf` dei dati strutturati.
"""

import json
import os
import re
import sys
import time

import pdfplumber

BASE = os.path.dirname(os.path.abspath(__file__))
MANUALI = os.path.join(BASE, "Manuali")
USCITA = os.path.join(BASE, "Testi")
STATO_DIR = os.path.join(BASE, ".colstep_state")
STATO = os.path.join(STATO_DIR, "stato.json")

# Ordine di lavorazione: prima cio' che serve prima.
PRIORITA = ["Dragonlance", "Core", "3.0_3.5"]

# Larghezza minima in punti perche' una banda bianca verticale conti come
# possibile gutter. Tenuta bassa di proposito: in molti impaginati d'epoca la
# banda fra le colonne e' strettissima, perche' qualche parola della colonna
# sinistra sporge. Una soglia alta faceva scambiare quelle pagine per
# colonna singola, producendo testo fuso senza accorgersene.
BANDA_MIN = 3

# Quanto puo' allontanarsi il gutter di una pagina da quello tipico del libro.
SCARTO_MAX = 45


# ---------------------------------------------------------------- colonne

def bande_vuote(pg, lo_f=0.30, hi_f=0.70):
    """Bande verticali prive di parole nella fascia centrale della pagina.
    Restituisce [(centro, larghezza), ...] e l'elenco delle parole."""
    parole = pg.extract_words()
    if len(parole) < 40:
        return [], parole
    W = int(pg.width)
    occ = bytearray(W + 2)
    for w in parole:
        for x in range(max(0, int(w["x0"])), min(W, int(w["x1"])) + 1):
            occ[x] = 1
    lo, hi = int(W * lo_f), int(W * hi_f)
    out, inizio = [], None
    for x in range(lo, hi + 1):
        if not occ[x]:
            if inizio is None:
                inizio = x
        elif inizio is not None:
            if x - inizio >= BANDA_MIN:
                out.append(((inizio + x) / 2, x - inizio))
            inizio = None
    if inizio is not None and hi - inizio >= BANDA_MIN:
        out.append(((inizio + hi) / 2, hi - inizio))
    return out, parole


def gutter_libro(p, campione=14):
    """Gutter tipico del libro. Gli impaginati RPG hanno una gabbia costante,
    quindi conviene stimarla una volta sola su un campione di pagine: da' un
    riferimento con cui validare le stime pagina per pagina, che da sole
    sbagliano su tabelle e illustrazioni a tutta pagina."""
    n = len(p.pages)
    passo = max(1, n // campione)
    cand = []
    for i in range(0, n, passo):
        try:
            b, _ = bande_vuote(p.pages[i])
        except Exception:
            continue
        if b:
            cand.append(max(b, key=lambda t: t[1])[0])
    if len(cand) < 3:
        return None
    cand.sort()
    return cand[len(cand) // 2]


def due_colonne(parole, g, tol=2.0):
    """Verifica geometrica: a sinistra e a destra di g c'e' testo a
    sufficienza e quasi nessuna parola attraversa la linea."""
    sx = sum(1 for w in parole if w["x1"] <= g + tol)
    dx = sum(1 for w in parole if w["x0"] >= g - tol)
    attraversano = len(parole) - sx - dx
    return (sx > len(parole) * 0.20
            and dx > len(parole) * 0.20
            and attraversano < len(parole) * 0.06)


def gutter_per_attraversamenti(parole, W, G):
    """Ripiego per le pagine senza alcuna banda completamente vuota.

    Basta un titolo a tutta larghezza, una didascalia o un fregio che
    attraversi il centro perche' non esista nessuna colonna di pixel bianchi
    da cima a fondo. La pagina resta pero' a due colonne: si cerca allora
    l'ascissa attraversata dal minor numero di parole, e la si accetta se
    quelle poche sono trascurabili."""
    if G is None:
        return None
    lo, hi = int(max(0, G - SCARTO_MAX)), int(min(W, G + SCARTO_MAX))
    migliore, min_att = None, None
    for x in range(lo, hi + 1):
        att = sum(1 for w in parole if w["x0"] < x < w["x1"])
        if min_att is None or att < min_att or (att == min_att and abs(x - G) < abs(migliore - G)):
            migliore, min_att = x, att
    if migliore is None:
        return None
    if due_colonne(parole, migliore, tol=2.0):
        return float(migliore)
    return None


def trova_gutter(pg, G=None):
    """Gutter della pagina, o None se e' a colonna singola.
    Fra le bande vuote sceglie quella piu' vicina al gutter del libro e la
    convalida geometricamente; se non ce ne sono, ripiega sul conteggio
    delle parole attraversate."""
    bande, parole = bande_vuote(pg)
    if not parole:
        return None
    if bande:
        if G is not None:
            cand = sorted(bande, key=lambda t: abs(t[0] - G))
        else:
            cand = sorted(bande, key=lambda t: -t[1])
        for centro, _larg in cand[:3]:
            if G is not None and abs(centro - G) > SCARTO_MAX:
                continue
            if due_colonne(parole, centro):
                return centro
    return gutter_per_attraversamenti(parole, pg.width, G)


# Quattro caratteri raddoppiati di fila non esistono in nessuna lingua reale:
# e' la firma dei glifi ridisegnati per simulare il neretto.
RADDOPPIO = re.compile(r"(?:(\w)\1){4,}")


def _e_raddoppio(s):
    """Distingue "ffllaammee" (raddoppio vero) da "qqqqqqqq" (filetto
    decorativo). Nel primo caso le lettere della sequenza sono diverse fra
    loro, nel secondo e' sempre la stessa ripetuta."""
    lettere = [s[i] for i in range(0, len(s), 2)]
    return len(set(lettere)) >= 3


def sdoppia(t):
    """Ricompone le sequenze a caratteri raddoppiati.

    Va applicata dopo dedupe_chars, che risolve solo i doppioni perfettamente
    sovrapposti: quando il glifo di rinforzo ha uno scarto reale, i due
    caratteri restano distinti e sopravvivono all'estrazione."""
    def fix(m):
        s = m.group(0)
        return s[::2] if _e_raddoppio(s) else s
    return RADDOPPIO.sub(fix, t)


def _estrai(pg, G):
    g = trova_gutter(pg, G)
    if g is None:
        return (pg.extract_text(x_tolerance=1.5) or "").strip()
    pezzi = []
    for x0, x1 in ((0, g), (g, pg.width)):
        t = pg.crop((x0, 0, x1, pg.height)).extract_text(x_tolerance=1.5) or ""
        t = t.strip()
        if t:
            pezzi.append(t)
    return "\n".join(pezzi)


def testo_pagina(pg, G=None):
    """Testo della pagina in ordine di lettura, colonne separate.

    Molte stampe d'epoca ottengono il neretto ridisegnando lo stesso glifo con
    un minimo scarto. pdftotext scartava i doppioni, pdfplumber li conserva e
    il testo esce come "ffllaammee ssttrriikkee" invece di "flame strike".

    dedupe_chars risolve, ma costa quasi dieci volte tanto: si applica quindi
    solo alle pagine in cui il raddoppio viene effettivamente rilevato."""
    t = _estrai(pg, G)
    if t and RADDOPPIO.search(t):
        try:
            t2 = _estrai(pg.dedupe_chars(tolerance=1), G)
            if t2 and not RADDOPPIO.search(t2):
                return t2
            if t2:
                t = t2      # dedupe migliora comunque, anche se non risolve tutto
        except Exception:
            pass
        t = sdoppia(t)
    return t


# ------------------------------------------------------------------ stato

def carica_stato():
    if os.path.exists(STATO):
        with open(STATO, encoding="utf-8") as f:
            return json.load(f)
    return {"fatti": {}, "pagine_totali": 0, "secondi_totali": 0.0}


def salva_stato(s):
    os.makedirs(STATO_DIR, exist_ok=True)
    tmp = STATO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATO)


def lavoro(filtro=None):
    """Elenco (cartella, nomefile) da lavorare, in ordine di priorita'."""
    out = []
    for cart in PRIORITA:
        d = os.path.join(MANUALI, cart)
        if not os.path.isdir(d):
            continue
        if filtro and filtro.lower() not in cart.lower():
            continue
        for nome in sorted(os.listdir(d)):
            if nome.lower().endswith(".pdf"):
                out.append((cart, nome))
    return out


# ------------------------------------------------------------------ passo

def ha_layer_testo(p, campione=12, soglia=100):
    """True se il PDF ha un layer di testo utilizzabile.

    Le scansioni pure non ne hanno: estrarle produrrebbe file vuoti.
    Vanno lasciate alla pipeline OCR (ocrstep.py), non a questa.
    Campiona pagine distribuite su tutto il documento perche' molti manuali
    hanno le prime pagine quasi bianche."""
    n = len(p.pages)
    if n == 0:
        return False
    passo = max(1, n // campione)
    indici = list(range(0, n, passo))[:campione]
    tot = 0
    for i in indici:
        try:
            tot += len((p.pages[i].extract_text() or "").strip())
        except Exception:
            pass
    return (tot / max(1, len(indici))) >= soglia


def elabora(cart, nome, stato, scadenza):
    """Lavora un PDF finche' finisce o scade il budget.
    Restituisce (pagine_fatte, completato)."""
    chiave = f"{cart}/{nome}"
    info = stato["fatti"].get(chiave, {"pagina": 0, "completo": False})
    if info["completo"] or info.get("senza_testo"):
        return 0, True

    pdf = os.path.join(MANUALI, cart, nome)
    parziale = os.path.join(STATO_DIR, chiave.replace("/", "__") + ".part")
    os.makedirs(STATO_DIR, exist_ok=True)

    fatte = 0
    try:
        with pdfplumber.open(pdf) as p:
            if info["pagina"] == 0 and not ha_layer_testo(p):
                stato["fatti"][chiave] = {"pagina": 0, "completo": False, "senza_testo": True}
                if os.path.exists(parziale):
                    os.remove(parziale)
                return 0, False
            totale = len(p.pages)
            # il gutter del libro si stima una volta e si riusa: e' il
            # riferimento con cui validare le stime pagina per pagina
            G = info.get("gutter")
            if G is None:
                G = gutter_libro(p)
                info["gutter"] = G
            # se ripartiamo da zero, azzera il parziale
            modo = "a" if info["pagina"] > 0 and os.path.exists(parziale) else "w"
            with open(parziale, modo, encoding="utf-8") as out:
                for i in range(info["pagina"], totale):
                    if time.time() > scadenza:
                        break
                    try:
                        t = testo_pagina(p.pages[i], G)
                    except Exception as e:
                        t = ""
                        print(f"    ! pagina {i}: {type(e).__name__}")
                    out.write(f"\n[[p.{i}]]\n{t}\n")
                    out.flush()
                    info["pagina"] = i + 1
                    fatte += 1
                completo = info["pagina"] >= totale
    except Exception as e:
        print(f"    ! {chiave}: {type(e).__name__} — {e}")
        stato["fatti"][chiave] = {"pagina": info["pagina"], "completo": False,
                                  "errore": f"{type(e).__name__}: {e}"[:200]}
        return fatte, False

    info["completo"] = completo
    stato["fatti"][chiave] = info

    if completo:
        finale = os.path.join(USCITA, cart, os.path.splitext(nome)[0] + ".txt")
        os.makedirs(os.path.dirname(finale), exist_ok=True)
        os.replace(parziale, finale)

    return fatte, completo


def riepilogo(stato):
    lav = lavoro()
    completi = sum(1 for c, n in lav if stato["fatti"].get(f"{c}/{n}", {}).get("completo"))
    senza = sum(1 for c, n in lav if stato["fatti"].get(f"{c}/{n}", {}).get("senza_testo"))
    pagine = stato["pagine_totali"]
    print(f"\n  {completi}/{len(lav)} manuali completi — {pagine:,} pagine lavorate "
          f"in {stato['secondi_totali']/60:.1f} min".replace(",", "."))
    if senza:
        print(f"  {senza} scansioni senza layer di testo, lasciate alla pipeline OCR")
    per_cart = {}
    for c, n in lav:
        k = stato["fatti"].get(f"{c}/{n}", {})
        per_cart.setdefault(c, [0, 0, 0])
        per_cart[c][1] += 1
        if k.get("completo"):
            per_cart[c][0] += 1
        if k.get("senza_testo"):
            per_cart[c][2] += 1
    for c, (fatti, tot, sz) in per_cart.items():
        print(f"    {c:12} {fatti:3}/{tot}" + (f"   ({sz} da OCR)" if sz else ""))
    errori = {k: v["errore"] for k, v in stato["fatti"].items() if v.get("errore")}
    if errori:
        print(f"\n  {len(errori)} manuali con errore:")
        for k, e in list(errori.items())[:10]:
            print(f"    {k}: {e[:90]}")


def main():
    args = [a for a in sys.argv[1:]]
    stato = carica_stato()

    if "--stato" in args:
        riepilogo(stato)
        return

    budget = int(args[0]) if args and args[0].isdigit() else 60
    filtro = args[1] if len(args) > 1 else None
    scadenza = time.time() + budget
    avvio = time.time()

    pagine = 0
    for cart, nome in lavoro(filtro):
        if time.time() > scadenza:
            break
        chiave = f"{cart}/{nome}"
        prima = stato["fatti"].get(chiave, {}).get("pagina", 0)
        if stato["fatti"].get(chiave, {}).get("completo"):
            continue
        fatte, completo = elabora(cart, nome, stato, scadenza)
        pagine += fatte
        if fatte:
            segno = "✓" if completo else "…"
            print(f"  {segno} {chiave}: {prima} -> {prima+fatte}")
        salva_stato(stato)

    trascorso = time.time() - avvio
    stato["pagine_totali"] += pagine
    stato["secondi_totali"] += trascorso
    salva_stato(stato)

    print(f"\n{pagine} pagine in {trascorso:.0f}s"
          + (f" ({trascorso/pagine:.2f} s/pagina)" if pagine else ""))
    riepilogo(stato)


if __name__ == "__main__":
    main()
