#!/usr/bin/env python3
"""
Generazione delle caratteristiche — modulo isolato.

DECISIONE 9 (12 agosto 2026)
    Metodo di default: **4d6 scarta il minore**, ufficiale in 5e 2014.
    Array standard e point-buy restano disponibili come alternative.

    Motivazione: i requisiti della 2e presuppongono caratteristiche tirate su
    scala 3-18. In 2e qualificarsi come Cavalier era raro PER DESIGN, non
    impossibile. Il point-buy non sa esprimere la rarita': appiattisce tutto a
    un budget uguale per tutti, quindi cio' che era raro diventa impossibile.
    Avendo scelto vincoli rigidi in stile 2e, si adotta anche la generazione
    che li rende sensati.

DECISIONE 11
    I massimali razziali si applicano sia in creazione sia come tetti di
    crescita. NON sono i limiti di livello (decisione 4, non applicati): un
    massimale limita quanto puo' salire un punteggio, non a che livello si
    ferma il personaggio.

COMPORTAMENTO IN CREAZIONE
    Se il metodo scelto rende irraggiungibile una combinazione razza+classe,
    il sistema **segnala e propone il tiro**. Non blocca.

Uso come libreria:
    from motore.generazione import genera, valida, METODI
"""

import json
import os
import random
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATI = os.path.join(BASE, "dati")

CAR = ["str", "dex", "con", "int", "wis", "cha"]
NOMI_CAR = {"str": "Forza", "dex": "Destrezza", "con": "Costituzione",
            "int": "Intelligenza", "wis": "Saggezza", "cha": "Carisma"}

ARRAY_STANDARD = [15, 14, 13, 12, 10, 8]
COSTO_POINTBUY = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
BUDGET_POINTBUY = 27

METODI = ("4d6-scarta-minore", "array-standard", "point-buy")
METODO_DEFAULT = "4d6-scarta-minore"

# Le voci "all: 3d6" nei dati non sono una regola speciale: sono il default
# generico della 2e, riportato dal manuale ("Create all abilities by rolling
# 3d6"). Il default di casa e' ora 4d6 scarta il minore, quindi vengono
# ignorate. Restano invece valide le formule dichiarate per singola
# caratteristica, che sono regole vere: i dadi propri dell'Aghar e la Forza
# del Kender (2d6+4).
CHIAVE_GENERICA = "all"


# --------------------------------------------------------------------- dadi

_DADO = re.compile(r"^(\d+)d(\d+)(?:\s*([+-])\s*(\d+))?$")


def tira_formula(formula, rng=random):
    """Tira una formula tipo '4d4+2' o '3d4'."""
    m = _DADO.match(formula.replace(" ", ""))
    if not m:
        raise ValueError(f"formula non riconosciuta: {formula!r}")
    n, facce = int(m.group(1)), int(m.group(2))
    tot = sum(rng.randint(1, facce) for _ in range(n))
    if m.group(3):
        tot += int(m.group(4)) * (1 if m.group(3) == "+" else -1)
    return tot


def tira_4d6_scarta_minore(rng=random):
    d = sorted(rng.randint(1, 6) for _ in range(4))
    return sum(d[1:])


# ---------------------------------------------------------------- generazione

def formule_razziali(razza):
    """Formule per singola caratteristica dichiarate dal manuale, escluse le
    voci generiche. Restituisce {} se la razza usa il metodo standard."""
    gen = (razza["source_2e"].get("ability_generation") or {})
    return {k: v for k, v in gen.items() if k != CHIAVE_GENERICA and k in CAR}


def genera(razza, metodo=METODO_DEFAULT, rng=random):
    """Genera sei punteggi GREZZI, prima degli aggiustamenti razziali.

    Restituisce (valori, assegnazione_libera):
      - se assegnazione_libera e' True i valori vanno distribuiti a piacere
        fra le caratteristiche;
      - se e' False i valori sono gia' legati a una caratteristica precisa,
        perche' il manuale prescrive dadi diversi per ciascuna (Aghar).
    """
    formule = formule_razziali(razza)

    if len(formule) == len(CAR):
        # tutte e sei prescritte: nessuna liberta' di assegnazione
        return {c: tira_formula(formule[c], rng) for c in CAR}, False

    if metodo == "array-standard":
        base = list(ARRAY_STANDARD)
    elif metodo == "point-buy":
        raise ValueError("il point-buy non si tira: usa valida_pointbuy() "
                         "sull'assegnazione scelta dal giocatore")
    else:
        base = [tira_4d6_scarta_minore(rng) for _ in CAR]

    if not formule:
        return base, True

    # formule parziali (Kender: solo la Forza): quelle caratteristiche sono
    # fissate, le restanti restano liberamente assegnabili
    fissi = {c: tira_formula(f, rng) for c, f in formule.items()}
    liberi = base[:len(CAR) - len(fissi)]
    return {"fissi": fissi, "liberi": liberi}, "parziale"


def valida_pointbuy(assegnazione):
    """Verifica costo e intervallo di un'assegnazione point-buy."""
    problemi = []
    for c in CAR:
        v = assegnazione.get(c)
        if v is None or v not in COSTO_POINTBUY:
            problemi.append(f"{NOMI_CAR[c]}: {v} fuori dall'intervallo 8-15 del point-buy")
    if problemi:
        return problemi
    costo = sum(COSTO_POINTBUY[assegnazione[c]] for c in CAR)
    if costo > BUDGET_POINTBUY:
        problemi.append(f"costo {costo} superiore al budget di {BUDGET_POINTBUY}")
    return problemi


# ------------------------------------------------------------- aggiustamenti

def applica_aggiustamenti(punteggi, razza):
    """Somma gli aggiustamenti razziali. DECISIONE 10: i negativi si tengono."""
    adj = razza["source_2e"].get("ability_adjustments") or {}
    return {c: punteggi[c] + adj.get(c, 0) for c in CAR}


def intervalli(razza, classe=None):
    """Intervallo ammesso per ciascuna caratteristica, DOPO gli aggiustamenti.

    Unisce i requisiti razziali con i minimi di classe. DECISIONE 12: per il
    Barbaro vale l'unione dei due set, non l'uno o l'altro."""
    req = razza["source_2e"]["ability_requirements"]
    lo = {c: (req[c]["min"] or 3) for c in CAR}
    hi = {c: (req[c]["max"] or 99) for c in CAR}
    if classe:
        for c, v in (classe["source_2e"].get("ability_minimums") or {}).items():
            lo[c] = max(lo[c], v)
    return lo, hi


def valida(punteggi_finali, razza, classe=None):
    """Elenco dei vincoli violati. Lista vuota = personaggio valido."""
    lo, hi = intervalli(razza, classe)
    fuori = []
    for c in CAR:
        v = punteggi_finali[c]
        if v < lo[c]:
            fuori.append(f"{NOMI_CAR[c]} {v}: serve almeno {lo[c]}")
        elif v > hi[c]:
            fuori.append(f"{NOMI_CAR[c]} {v}: il massimo per questa razza e' {hi[c]}")
    return fuori


def tetto_crescita(razza, caratteristica):
    """Massimale oltre il quale la caratteristica non puo' salire.

    DECISIONE 11: i massimali valgono anche in avanzamento. Non vanno confusi
    con i limiti di livello, che restano non applicati (decisione 4)."""
    mx = razza["source_2e"]["ability_requirements"][caratteristica]["max"]
    return mx if mx is not None else 20


# ------------------------------------------------- supporto alla creazione PG

def esiste_assegnazione(valori, lo, hi):
    """C'e' un modo di distribuire `valori` rispettando tutti gli intervalli?

    Greedy corretto per questa struttura: si ordinano le caratteristiche per
    massimale crescente e a ciascuna si assegna il valore ammissibile piu'
    piccolo disponibile. Chi ha il tetto piu' basso sceglie per primo, quindi
    non gli viene sottratto un valore che solo lui poteva usare."""
    disponibili = sorted(valori)
    for c in sorted(CAR, key=lambda x: hi[x]):
        scelto = None
        for i, v in enumerate(disponibili):
            if lo[c] <= v <= hi[c]:
                scelto = i
                break
        if scelto is None:
            return False
        disponibili.pop(scelto)
    return True


def metodi_praticabili(razza, classe=None):
    """Quali metodi possono produrre un personaggio valido.

    Serve alla creazione PG: se il metodo scelto non e' praticabile il sistema
    lo segnala e propone il tiro, senza bloccare (decisione 9)."""
    lo, hi = intervalli(razza, classe)
    adj = razza["source_2e"].get("ability_adjustments") or {}
    # gli intervalli sono sui punteggi finali: si riportano ai grezzi
    lo_g = {c: lo[c] - adj.get(c, 0) for c in CAR}
    hi_g = {c: hi[c] - adj.get(c, 0) for c in CAR}

    # Se il manuale prescrive dadi per tutte e sei le caratteristiche (Aghar),
    # non c'e' scelta di metodo: quella razza si tira e basta.
    if len(formule_razziali(razza)) == len(CAR):
        return {"dadi-propri": True, "array-standard": False, "point-buy": False,
                "4d6-scarta-minore": False}

    out = {}
    out["array-standard"] = esiste_assegnazione(ARRAY_STANDARD, lo_g, hi_g)
    out["point-buy"] = any(
        esiste_assegnazione(t, lo_g, hi_g)
        for t in _combinazioni_pointbuy())
    # col tiro il massimo e' 18 per caratteristica: praticabile se gli
    # intervalli grezzi sono tutti non vuoti dentro 3-18
    out["4d6-scarta-minore"] = all(
        max(3, lo_g[c]) <= min(18, hi_g[c]) for c in CAR)
    return out


_PB = None


def _combinazioni_pointbuy():
    global _PB
    if _PB is None:
        import itertools
        _PB = [t for t in itertools.product(range(8, 16), repeat=6)
               if sum(COSTO_POINTBUY[v] for v in t) <= BUDGET_POINTBUY]
    return _PB


# ------------------------------------------------------------------ caricamento

def carica_razza(rid):
    return json.load(open(os.path.join(DATI, "razze", rid + ".json"), encoding="utf-8"))


def carica_classe(cid):
    return json.load(open(os.path.join(DATI, "classi", cid + ".json"), encoding="utf-8"))


if __name__ == "__main__":
    rng = random.Random(1)
    print("Metodi disponibili:", ", ".join(METODI), f"(default: {METODO_DEFAULT})\n")
    for rid in ("umano", "nano-aghar", "kender", "irda"):
        r = carica_razza(rid)
        v, libera = genera(r, rng=rng)
        print(f"{r['name']['it'][:28]:28} {v}  assegnazione libera: {libera}")
    print()
    for rid, cid in (("umano", "cavaliere"), ("mezzelfo", "cavaliere-rosa"),
                     ("nano-aghar", "barbaro"), ("umano-barbaro", "barbaro")):
        r, c = carica_razza(rid), carica_classe(cid)
        m = metodi_praticabili(r, c)
        praticabili = [k for k, ok in m.items() if ok] or ["nessuno"]
        print(f"{rid:14} + {cid:16} praticabile con: {', '.join(praticabili)}")
