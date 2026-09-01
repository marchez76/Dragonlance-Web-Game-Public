#!/usr/bin/env python3
"""
Generazione delle caratteristiche — modulo isolato.

DECISIONE 8 (`generazione-caratteristiche`, 12 agosto 2026)
    Metodo di default: **4d6 scarta il minore**, ufficiale in 5e 2014.
    Array standard e point-buy restano disponibili come alternative.

    Motivazione: i requisiti della 2e presuppongono caratteristiche tirate su
    scala 3-18. In 2e qualificarsi come Cavalier era raro PER DESIGN, non
    impossibile. Il point-buy non sa esprimere la rarita': appiattisce tutto a
    un budget uguale per tutti, quindi cio' che era raro diventa impossibile.
    Avendo scelto vincoli rigidi in stile 2e, si adotta anche la generazione
    che li rende sensati.

DECISIONE 10 (`massimali-razziali`)
    I massimali razziali si applicano sia in creazione sia come tetti di
    crescita. NON sono i limiti di livello (decisione 4 (`limiti-di-livello`), non applicati): un
    massimale limita quanto puo' salire un punteggio, non a che livello si
    ferma il personaggio.

DECISIONE 44 (`tetto-punto-perduto`)
    Un aumento che sfonderebbe il tetto e' PERDUTO: non travasato, non
    ammorbidito. Il giocatore deve pero' VEDERE il tetto prima di spendere,
    non scoprirlo dopo: `anteprima_aumento()` esiste per questo.

COMPORTAMENTO IN CREAZIONE
    Se il metodo scelto rende irraggiungibile una combinazione razza+classe,
    il sistema **segnala e propone il tiro**. Non blocca.

DA QUALE STRATO LEGGE QUESTO MODULO
    Da `mechanics_5e`, sempre. Mai da `source_2e`.

    Fino al 02/09/2026 leggeva `source_2e`, e non si vedeva: `build_razze.py`
    scrive i due strati dalla stessa fonte nella stessa passata, quindi oggi
    i valori coincidono. Ma `mechanics_5e` e' lo strato **rivedibile** per
    definizione (decisione 7, `doppio-strato`): il giorno che una revisione
    tocca un tetto li' dentro, un motore che legge `source_2e` usa il valore
    vecchio **senza segnalare nulla**. E' la forma esatta delle cinque
    divergenze gia' costate al progetto: due strutture allineate il giorno
    uno che nessuno riconfronta il giorno due.

    Le due letture non sono nemmeno intercambiabili nella forma. `source_2e`
    porta sempre sei caratteristiche con `min`/`max` eventualmente `null`;
    `mechanics_5e.ability_constraints.limits` **omette** le caratteristiche
    prive di vincoli e `ability_caps.caps` porta **solo i massimali
    dichiarati dal manuale** (l'Umano Barbaro ne ha 2 su 6). La chiave
    assente non e' un buco: e' la caratteristica libera, che per la
    decisione 44 (`tetto-punto-perduto`) resta al 20 della 5e.

    Il controllo che i due strati non divergano e' `dati/verifica_strati.py`,
    da eseguire come i `valida_*.py`.

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

# Le voci "all: 3d6" della fonte non sono una regola speciale: sono il default
# generico della 2e, riportato dal manuale ("Create all abilities by rolling
# 3d6"). Il default di casa e' ora 4d6 scarta il minore, quindi lo strato di
# conversione non le riporta affatto: `generation.dice_formulas` contiene solo
# le formule per singola caratteristica, che sono regole vere — i dadi propri
# dell'Aghar e la Forza del Kender (2d6+4).

# Tetto di crescita di una caratteristica che il manuale non massimalizza.
# decisione 44 (`tetto-punto-perduto`): la casella non dichiarata non eredita
# un tetto razziale, resta al 20 della 5e.
TETTO_5E = 20


# ---------------------------------------------------- lettura dello strato 5e

class StratoMancante(KeyError):
    """`mechanics_5e` assente o non compilato.

    Errore esplicito e non fallback silenzioso su `source_2e`: ripiegare
    sulla fonte e' proprio il difetto corretto il 02/09/2026 (vedi
    l'intestazione). Meglio fermarsi che generare un personaggio con i
    numeri dello strato sbagliato senza dirlo a nessuno."""


def strato(entita, cosa=""):
    """`mechanics_5e` di una razza o di una classe, o StratoMancante.

    Controlla che lo strato ci sia, NON che sia completo. Il completamento
    si misura sul blocco che serve, non su uno stato globale: le razze sono
    tutte `compilato`, ma le classi usano `clonato` (ha un chassis SRD) e
    `in_sospeso` (non ce l'ha), e una classe senza chassis ha comunque i
    suoi minimi di caratteristica scritti e verificabili. Confondere "non ha
    un chassis" con "non se ne puo' leggere niente" farebbe fallire meta'
    del roster su una domanda a cui i dati rispondono. Chi ha bisogno del
    chassis lo chiede a `senza_chassis()`."""
    m = entita.get("mechanics_5e")
    if not m:
        raise StratoMancante(
            f"{entita.get('id', '?')}: mechanics_5e assente"
            + (f" (serviva {cosa})" if cosa else "")
            + " — il motore legge lo strato di conversione, non source_2e")
    return m


def senza_chassis(classe):
    """La classe ha un chassis SRD su cui poggiare, o no?

    Le 8 classi `in_sospeso` non hanno dado vita 5e ne' tiri salvezza ne'
    progressione: se ne possono leggere i vincoli di creazione, ma non ci si
    puo' costruire sopra un personaggio giocabile."""
    ch = strato(classe, "il chassis").get("chassis") or {}
    return not ch.get("srd_class")


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
    """Formule per singola caratteristica, dallo strato di conversione.
    Restituisce {} se la razza usa il metodo standard."""
    gen = (strato(razza, "le formule di generazione").get("generation") or {})
    df = gen.get("dice_formulas") or {}
    return {k: v for k, v in df.items() if k in CAR}


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

def aggiustamenti(razza):
    """Aggiustamenti razziali NETTI, dallo strato di conversione.

    `values` e' il netto applicato: la somma di `source_values` (quello che
    dice il manuale) e `editorial_values` (quello che abbiamo aggiunto noi).
    Il motore vuole il netto — leggere `source_2e.ability_adjustments` non
    era equivalente e su una razza gia' non lo e': l'Umano Barbaro porta un
    +1 a Forza e Costituzione che esiste **solo** nello strato 5e, il tappo
    della decisione 20 (`tappo-barbaro`), confermato come tappo dalla
    decisione 43 (`barbaro-rimandato`). Letto da `source_2e` valeva zero, e
    il motore lo scartava in silenzio."""
    adj = strato(razza, "gli aggiustamenti razziali").get("ability_adjustments")
    return (adj or {}).get("values") or {}


def applica_aggiustamenti(punteggi, razza):
    """Somma gli aggiustamenti razziali. DECISIONE 9 (`aggiustamenti-negativi`): i negativi si tengono."""
    adj = aggiustamenti(razza)
    return {c: punteggi[c] + adj.get(c, 0) for c in CAR}


def intervalli(razza, classe=None):
    """Intervallo ammesso per ciascuna caratteristica, DOPO gli aggiustamenti.

    Unisce i requisiti razziali con i minimi di classe. DECISIONE 11 (`barbaro-vincoli`): per il
    Barbaro vale l'unione dei due set, non l'uno o l'altro."""
    # `limits` omette le caratteristiche senza vincoli e conserva i null
    # interni: la chiave assente e' la caratteristica libera, non un buco.
    lim = (strato(razza, "i vincoli di creazione").get("ability_constraints")
           or {}).get("limits") or {}
    lo, hi = {}, {}
    for c in CAR:
        v = lim.get(c) or {}
        lo[c] = v.get("min") or 3
        hi[c] = v.get("max") or 99
    if classe:
        minimi = (strato(classe, "i minimi di classe").get("ability_minimums")
                  or {})
        for c, v in (minimi.get("values") or {}).items():
            if c in lo:
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

    DECISIONE 10 (`massimali-razziali`): i massimali valgono anche in avanzamento. Non vanno confusi
    con i limiti di livello, che restano non applicati (decisione 4, `limiti-di-livello`)."""
    caps = (strato(razza, "i tetti di crescita").get("ability_caps")
            or {}).get("caps") or {}
    mx = caps.get(caratteristica)
    return mx if mx is not None else TETTO_5E


def anteprima_aumento(punteggi, razza, spesa):
    """Cosa succede DAVVERO spendendo `spesa` = {caratteristica: punti}.

    DECISIONE 44 (`tetto-punto-perduto`). Il punto che sfonda il tetto e'
    perduto: non travasa altrove, non alza il tetto. Ma il giocatore deve
    vederlo **prima** di spendere, non scoprirlo dopo — quindi questa
    funzione non applica niente, calcola e basta, e chi la chiama ha in mano
    l'avviso da mostrare. Il sistema segnala, non blocca in silenzio: se il
    giocatore vuole comunque buttare il punto, e' una sua scelta informata.

    Restituisce (nuovi_punteggi, avvisi, punti_perduti)."""
    nuovi, avvisi, perduti = dict(punteggi), [], 0
    for c, punti in spesa.items():
        if c not in CAR:
            raise ValueError(f"caratteristica sconosciuta: {c!r}")
        tetto = tetto_crescita(razza, c)
        prima = nuovi[c]
        dopo = min(prima + punti, tetto)
        perso = (prima + punti) - dopo
        nuovi[c] = dopo
        if perso:
            perduti += perso
            avvisi.append(
                f"{NOMI_CAR[c]}: {prima} + {punti} sfonda il massimale "
                f"razziale di {tetto}. "
                f"{'Il punto e\' perduto' if perso == 1 else f'{perso} punti sono perduti'}"
                f": non si travasa su un'altra caratteristica "
                f"(decisione 44, `tetto-punto-perduto`).")
    return nuovi, avvisi, perduti


def caratteristiche_al_tetto(punteggi, razza):
    """Quali caratteristiche non possono piu' salire, e a che tetto.

    Serve all'interfaccia di avanzamento: e' l'informazione che la
    decisione 44 (`tetto-punto-perduto`) impone di mostrare PRIMA della
    spesa, cosi' che spendere su una casella chiusa sia una scelta e non
    una sorpresa."""
    return {c: tetto_crescita(razza, c) for c in CAR
            if punteggi[c] >= tetto_crescita(razza, c)}


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
    lo segnala e propone il tiro, senza bloccare (decisione 8, `generazione-caratteristiche`)."""
    lo, hi = intervalli(razza, classe)
    adj = aggiustamenti(razza)
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
