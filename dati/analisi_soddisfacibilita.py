#!/usr/bin/env python3
"""
RAPPORTO DIAGNOSTICO — soddisfacibilita' dei requisiti sotto le regole 5e.

DOMANDA
    I requisiti di caratteristica estratti da Tales of the Lance presuppongono
    statistiche tirate con 3d6 su scala 3-18. Con l'array standard o con
    l'acquisto a punti il massimo pre-razziale e' 15. Alcuni requisiti possono
    quindi risultare impossibili, o forzare l'intera distribuzione.

MODELLO
    In AD&D 2e gli aggiustamenti razziali si applicano al tiro e il risultato
    deve cadere nell'intervallo min/max. Qui si assume lo stesso: i requisiti
    valgono sul punteggio FINALE, dopo gli aggiustamenti.

    Array standard: i sei valori assegnati liberamente -> 720 permutazioni.
    Acquisto a punti: punteggi base entro l'intervallo del listino, somma dei
    costi entro il budget. I numeri dei due metodi stanno in
    `dati/sistema/generazione-caratteristiche.json` e si leggono da li'.

DA DOVE LEGGE QUESTO RAPPORTO, e perche' e' cambiato il 05/09/2026
    1. LE CLASSI DI UNA RAZZA vengono da `dati/_classi_ammesse.py`, che e' la
       sede della decisione 58 (`telaio-apre-classe-filtra`). Fino a oggi
       questo file ne aveva una SECONDA risoluzione, scritta prima della
       sede e mai riportata su di essa: leggeva `class_level_limits` dalla
       tabella 2e e ne ricavava 87 coppie contro le 126 della sede, con la
       divergenza a due sensi — 63 coppie che la sede apre e questo file non
       vedeva, 12 che questo file apriva e la sede non apre. E' il caso
       previsto da CLAUDE.md 3: la sede era nata e il `grep` non aveva
       raggiunto questo file.

    2. I VINCOLI vengono da `mechanics_5e`, tramite `motore/generazione.py`.
       Fino a oggi venivano da `source_2e`: la stessa trappola chiusa nel
       motore il 02/09/2026, ancora in piedi qui. Non si vedeva perche' i
       `build_*.py` scrivono i due strati nella stessa passata, quindi oggi i
       valori coincidono quasi ovunque; ma `mechanics_5e` e' lo strato
       rivedibile (decisione 7, `doppio-strato`), e leggere la fonte vuol
       dire usare il valore vecchio senza segnalare nulla. Un caso esiste
       gia' ed e' misurato piu' sotto: l'Umano Barbaro porta in
       `mechanics_5e` un +1 che `source_2e` non ha.

    3. I NUMERI DEI METODI vengono da `dati/sistema/`. Erano scritti qui e
       di nuovo in `motore/generazione.py`.

    Le tre letture sono verificate dal rapporto stesso, non assunte: la
    sezione «I due strati a confronto» rifa' il confronto sulle grandezze
    che questo rapporto usa davvero.

NON MODIFICA NULLA. E' solo un rapporto.

Uso:  python3 dati/analisi_soddisfacibilita.py > dati/RAPPORTO-soddisfacibilita.md
"""

import itertools
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
sys.path.insert(0, BASE)
sys.path.insert(0, RADICE)

import _classi_ammesse as CA        # noqa: E402
import _sistema as SIS              # noqa: E402
import verifica_strati as VS        # noqa: E402
from decisioni import cita          # noqa: E402
from motore import generazione as G  # noqa: E402

CAR = G.CAR

ARRAY_STD = tuple(SIS.ARRAY_STANDARD)
COSTO = SIS.COSTO_ACQUISTO
BUDGET = SIS.BUDGET_ACQUISTO
PERMUTAZIONI = 720          # 6! — le disposizioni dell'array standard


# ==========================================================================
# I due conteggi. Contano DISPOSIZIONI, non praticabilita': `metodi_pra-
# ticabili()` dice se ne esiste almeno una, questi dicono quante sono, che e'
# la misura di quanto una combinazione sia stretta. Le due risposte non
# possono divergere — «zero disposizioni» e «metodo non praticabile» sono la
# stessa cosa — e la sezione finale del rapporto lo verifica invece di
# fidarsi.
# ==========================================================================

def ok(base, lo, hi, adj):
    """base = sei punteggi PRE-razziali, nell'ordine di CAR."""
    for i, c in enumerate(CAR):
        v = base[i] + adj.get(c, 0)
        if v < lo[c] or v > hi[c]:
            return False
    return True


def conta_array(lo, hi, adj):
    return sum(1 for p in itertools.permutations(ARRAY_STD)
               if ok(p, lo, hi, adj))


_PB = None


def combinazioni_acquisto():
    global _PB
    if _PB is None:
        basso, alto = min(COSTO), max(COSTO)
        _PB = [t for t in itertools.product(range(basso, alto + 1), repeat=len(CAR))
               if sum(COSTO[v] for v in t) <= BUDGET]
    return _PB


def conta_acquisto(lo, hi, adj):
    return sum(1 for t in combinazioni_acquisto() if ok(t, lo, hi, adj))


# ==========================================================================
# L'ANALISI
# ==========================================================================

def analizza():
    razze, classi = CA.razze(), CA.classi()
    per_id = {c["id"]: c for c in classi}
    righe = []

    for r in razze:
        lo, hi = G.intervalli(r)
        adj = G.aggiustamenti(r)
        formule = G.formule_razziali(r)

        voci = []
        for p in G.percorsi(r, classi):
            if not p.ammessa:
                voci.append({"id": p.classe, "ammessa": False,
                             "motivi": p.motivi})
                continue
            lo_c, hi_c = G.intervalli(r, per_id[p.classe])
            voci.append({
                "id": p.classe,
                "ammessa": True,
                "motivi": [],
                "metodi": p.metodi,
                "array": conta_array(lo_c, hi_c, adj),
                "acquisto": conta_acquisto(lo_c, hi_c, adj),
            })

        righe.append({
            "id": r["id"],
            "nome": r["name"]["it"],
            "array": conta_array(lo, hi, adj),
            "acquisto": conta_acquisto(lo, hi, adj),
            "min": {c: lo[c] for c in CAR if lo[c] > 3},
            "max": {c: hi[c] for c in CAR if hi[c] < 99},
            "adj": {c: v for c, v in adj.items() if v},
            "formule": formule,
            "voci": voci,
        })
    return righe, classi


def ammesse(riga):
    return [v for v in riga["voci"] if v["ammessa"]]


# ==========================================================================
# LA STAMPA
# ==========================================================================

def punto(n):
    return f"{n:,}".replace(",", ".")


def stampa(righe, classi):
    tot_pb = len(combinazioni_acquisto())
    n_coppie = sum(len(ammesse(r)) for r in righe)

    print(f"Spazio di ricerca: {PERMUTAZIONI} permutazioni dell'array "
          f"standard, {punto(tot_pb)} combinazioni di acquisto a punti entro "
          f"{BUDGET} punti.\n")
    print(f"Le coppie razza+classe aperte dal telaio e lasciate passare dal "
          f"filtro ({cita('telaio-apre-classe-filtra')}) sono "
          f"**{n_coppie}**, su {len(righe)} razze e {len(classi)} classi. "
          f"Sono quelle che questo rapporto misura: le classi che il telaio "
          f"non apre non compaiono, perche' non sono state escluse — non "
          f"sono state proposte.\n")

    print("| razza | array std | acquisto a punti | verdetto |")
    print("|---|---:|---:|---|")
    for r in righe:
        if r["formule"] and len(r["formule"]) == len(CAR):
            v = "**dadi propri del manuale**"
        elif r["array"] == 0 and r["acquisto"] == 0:
            v = "**IMPOSSIBILE**"
        elif r["array"] == 0:
            v = "**solo acquisto a punti**"
        elif r["array"] <= 6:
            v = f"**quasi obbligata** ({r['array']} disposizioni)"
        elif r["array"] <= 24:
            v = "molto vincolata"
        else:
            v = "libera"
        print(f"| {r['nome'][:34]} | {r['array']:3}/{PERMUTAZIONI} | "
              f"{r['acquisto']:6}/{tot_pb} | {v} |")

    sezione_metodo(righe)
    sezione_classi(righe, classi)
    sezione_dettaglio(righe, tot_pb)
    sezione_strati(righe)


def sezione_metodo(righe):
    """IL TERZO FILTRO. La misura che la
    decisione 58 (`telaio-apre-classe-filtra`) non poteva dare."""
    print(f"\n\n## Il metodo di generazione e' il terzo filtro\n")
    print(f"Il filtro di {cita('telaio-apre-classe-filtra')} confronta il "
          f"minimo di classe con il MASSIMALE RAZZIALE, cioe' con il "
          f"teoricamente raggiungibile. Non con cio' che il metodo scelto sa "
          f"produrre: l'array standard e l'acquisto a punti si fermano a "
          f"{max(COSTO)} pre-razziale, il tiro arriva a 18. Le coppie qui "
          f"sotto passano i primi due filtri e restano comunque "
          f"irraggiungibili con quel metodo.\n")

    # Le razze a dadi propri restano FUORI da questo conto, e non e' un
    # dettaglio: per loro il manuale prescrive sei formule e non c'e' nessuna
    # scelta di metodo da fare. Contarle come «precluse da tutti e tre»
    # scambierebbe l'assenza di scelta per un divieto, e gonfierebbe ogni
    # colonna della stessa quantita' — un numero piu' grande e meno vero.
    con_scelta, senza_scelta = [], []
    for r in righe:
        for v in ammesse(r):
            (senza_scelta if v["metodi"].get(G.DADI_PROPRI)
             else con_scelta).append((r["nome"], v))

    tot = len(con_scelta)
    print(f"Le coppie con una scelta di metodo da fare sono **{tot}**; le "
          f"altre **{len(senza_scelta)}** appartengono a razze per cui il "
          f"manuale prescrive sei formule di dado, dove non c'e' nessun "
          f"metodo da scegliere. Restano fuori dal conto.\n")

    print("| metodo | coppie precluse | su | classi coinvolte |")
    print("|---|---:|---:|---|")
    for m in G.METODI:
        coppie = [(n, v["id"]) for n, v in con_scelta if not v["metodi"].get(m)]
        cl = sorted({c for _, c in coppie})
        print(f"| `{m}` | {len(coppie)} | {tot} | "
              f"{', '.join('`' + c + '`' for c in cl) or '—'} |")

    senza = sorted((n, v["id"]) for n, v in con_scelta
                   if not v["metodi"].get(G.ARRAY)
                   and not v["metodi"].get(G.ACQUISTO))
    per_classe, aperte_per_classe = {}, {}
    for _n, cid in senza:
        per_classe[cid] = per_classe.get(cid, 0) + 1
    for n, v in con_scelta:
        aperte_per_classe[v["id"]] = aperte_per_classe.get(v["id"], 0) + 1

    print(f"\n**{len(senza)} coppie su {tot} non sono raggiungibili con "
          f"nessuno dei due metodi senza dadi**, e appartengono a "
          f"{len(per_classe)} classi soltanto:\n")
    print("| classe | coppie irraggiungibili | coppie aperte | resta |")
    print("|---|---:|---:|---|")
    for cid, n in sorted(per_classe.items()):
        tutta = ("**tutta la classe**" if n == aperte_per_classe[cid]
                 else f"{n} su {aperte_per_classe[cid]}")
        print(f"| `{cid}` | {n} | {aperte_per_classe[cid]} | {tutta}, e resta "
              f"solo il tiro |")

    print(f"\nNon e' un difetto: e' {cita('generazione-caratteristiche')} che "
          f"si manifesta. Era scritto che l'acquisto a punti non sa esprimere "
          f"la rarita' — appiattisce tutti sullo stesso budget — quindi cio' "
          f"che in 2e era raro diventa impossibile. Era una previsione; "
          f"questa e' la misura.\n")
    print("Le coppie, una per una:\n")
    for nome, cid in senza:
        print(f"- **{nome}** + `{cid}`")


def sezione_classi(righe, classi):
    print("\n\n## Difficolta' per classe\n")
    print("Quante razze arrivano a ciascuna classe, fra quelle a cui il "
          "telaio la apre, e con quanti metodi. La colonna «dadi propri» "
          "tiene a parte le razze che non scelgono un metodo: senza di essa "
          "comparirebbero come precluse da tutti e tre.\n")
    print("| classe | requisiti | razze aperte | passano il filtro | "
          "dadi propri | con array | con acquisto |")
    print("|---|---|---:|---:|---:|---:|---:|")
    for c in sorted(classi, key=lambda x: x["id"]):
        am = ((c.get("mechanics_5e") or {}).get("ability_minimums") or {})
        valori = (am.get("values") or {}) if am.get("applied") else {}
        aperte = passano = propri = con_array = con_acq = 0
        for r in righe:
            for v in r["voci"]:
                if v["id"] != c["id"]:
                    continue
                aperte += 1
                if not v["ammessa"]:
                    continue
                passano += 1
                if v["metodi"].get(G.DADI_PROPRI):
                    propri += 1
                    continue
                con_array += bool(v["metodi"].get(G.ARRAY))
                con_acq += bool(v["metodi"].get(G.ACQUISTO))
        if not aperte:
            continue
        scelgono = passano - propri
        req = " ".join(f"{k.upper()}{v}" for k, v in sorted(valori.items())) or "—"
        segno = " ⚠" if con_array < scelgono else ""
        print(f"| `{c['id']}` | {req} | {aperte} | {passano} | {propri} | "
              f"{con_array}/{scelgono}{segno} | {con_acq}/{scelgono} |")


def sezione_dettaglio(righe, tot_pb):
    print("\n\n## Dettaglio per razza\n")
    for r in righe:
        print(f"### {r['nome']} (`{r['id']}`)")
        print(f"- minimi: {r['min'] or 'nessuno'}")
        print(f"- massimali: {r['max'] or 'nessuno'}")
        print(f"- aggiustamenti applicati: {r['adj'] or 'nessuno'}")
        if r["formule"]:
            print(f"- formule proprie del manuale: {r['formule']}")
        print(f"- distribuzioni valide: {r['array']}/{PERMUTAZIONI} array "
              f"standard, {r['acquisto']}/{tot_pb} acquisto a punti")
        am = ammesse(r)
        if am:
            peggiori = sorted(am, key=lambda x: x["array"])[:4]
            print("- classi piu' vincolate: " + ", ".join(
                f"`{v['id']}` ({v['array']}/{PERMUTAZIONI})" for v in peggiori))
        escluse = [v for v in r["voci"] if not v["ammessa"]]
        if escluse:
            print("- aperte dal telaio e tolte dal filtro: " + ", ".join(
                f"`{v['id']}` ({v['motivi'][0][0]})" for v in escluse))
        print()


def sezione_strati(righe):
    """IL CONFRONTO. Spostare la lettura su `mechanics_5e` non basta: va
    mostrato che cosa cambia, altrimenti e' una modifica presa sulla parola."""
    print("\n\n## I due strati a confronto\n")
    div, dichiarati, misure = VS.verifica()
    print(f"`verifica_strati.py` confronta {misure['razze']} razze e "
          f"{misure['classi']} classi sulle stesse grandezze che questo "
          f"rapporto usa: vincoli, massimali, aggiustamenti, formule, minimi "
          f"di classe. Scarti dichiarati: **{misure['scarti_dichiarati']}**. "
          f"Divergenze non dichiarate: **{misure['divergenze']}**.\n")
    if dichiarati:
        print("Gli scarti dichiarati sono la ragione per cui questo rapporto "
              "legge lo strato 5e e non la fonte: letti da `source_2e` "
              "varrebbero zero, e sparirebbero dal conto senza che nulla lo "
              "segnali.\n")
        print("| entita' | grandezza | scarto |")
        print("|---|---|---|")
        for chi, tipo, det in dichiarati:
            print(f"| {chi} | {tipo} | {det} |")
    if div:
        print("\n**DIVERGENZE NON DICHIARATE** — vanno chiuse, i numeri qui "
              "sopra ne dipendono:\n")
        for chi, tipo, det in div:
            print(f"- {chi} — {tipo}: {det}")

    # La coerenza fra i due modi di rispondere alla stessa domanda.
    incoerenti, provate = [], 0
    for r in righe:
        for v in ammesse(r):
            # Le razze a dadi propri restano fuori, e non per comodita': per
            # loro il conteggio delle disposizioni risponde a una domanda che
            # non si pone — quante permutazioni dell'array sarebbero valide
            # per chi l'array non lo usa. Le due funzioni non sono in
            # disaccordo, stanno rispondendo a domande diverse.
            if v["metodi"].get(G.DADI_PROPRI):
                continue
            provate += 1
            if bool(v["array"]) != bool(v["metodi"].get(G.ARRAY)):
                incoerenti.append((r["nome"], v["id"], "array"))
            if bool(v["acquisto"]) != bool(v["metodi"].get(G.ACQUISTO)):
                incoerenti.append((r["nome"], v["id"], "acquisto"))
    print(f"\nControllo interno: «zero disposizioni» e «metodo non "
          f"praticabile» sono la stessa cosa detta da due funzioni diverse "
          f"— il conteggio di questo file e `metodi_praticabili()` del "
          f"motore. Coppie confrontate: {provate}. "
          f"Disaccordi: **{len(incoerenti)}**.")
    for nome, cid, quale in incoerenti:
        print(f"- {nome} + `{cid}` ({quale})")


# ==========================================================================
# COMPITO B — aggiustamenti negativi
#
# In 5e 2014 le razze hanno SOLO bonus positivi, per un totale che si aggira
# sempre su +3. Gli aggiustamenti negativi della 2e non hanno equivalente.
#
# QUI I DUE STRATI SI LEGGONO ENTRAMBI, ed e' voluto: la domanda e' quanto
# cio' che APPLICHIAMO si discosti da cio' che la fonte DICE, e serve saperlo
# per la 5e (`mechanics_5e`, il netto) e per la 2e (`source_2e`, il
# dichiarato). Leggerne uno solo risponderebbe a meta' domanda.
# ==========================================================================

STANDARD_5E = 3    # somma tipica dei bonus razziali in 5e 2014


def rapporto_negativi():
    razze = CA.razze()
    print("\n\n# COMPITO B — aggiustamenti negativi\n")
    print(f"In 5e 2014 le razze hanno solo bonus positivi, per un totale che "
          f"si aggira su **+{STANDARD_5E}**. Gli aggiustamenti negativi della "
          f"2e non hanno equivalente.\n")
    print("| razza | negativi | massimale sulla stessa caratteristica | "
          "doppia penalita' | positivi | netto | scarto da +3 |")
    print("|---|---|---|---|---:|---:|---:|")

    for r in razze:
        adj = G.aggiustamenti(r)
        neg = {k: v for k, v in adj.items() if v < 0}
        pos = {k: v for k, v in adj.items() if v > 0}
        if not neg:
            continue
        tetti = VS.tetti_5e(r)
        voci_neg, voci_max, doppie = [], [], []
        for k, v in sorted(neg.items()):
            voci_neg.append(f"{k.upper()} {v:+d}")
            mx = tetti.get(k)
            if mx is not None and mx < 18:
                voci_max.append(f"{k.upper()} max {mx}")
                doppie.append(k.upper())
            else:
                voci_max.append("—")
        netto = sum(adj.values())
        print(f"| {r['name']['it'][:30]} | {', '.join(voci_neg)} | "
              f"{', '.join(voci_max)} | {', '.join(doppie) or 'no'} | "
              f"{', '.join(f'{k.upper()} {v:+d}' for k, v in sorted(pos.items())) or '—'} | "
              f"{netto:+d} | {netto - STANDARD_5E:+d} |")

    print("\n**Tutte le razze, anche quelle senza negativi, e i due strati "
          "accanto:**\n")
    print("| razza | applicati (`mechanics_5e`) | netto | dichiarati "
          "(`source_2e`) | netto | scarto fra gli strati |")
    print("|---|---|---:|---|---:|---|")
    for r in sorted(razze, key=lambda x: sum(G.aggiustamenti(x).values())):
        adj = G.aggiustamenti(r)
        fonte = r["source_2e"].get("ability_adjustments") or {}
        n5, n2 = sum(adj.values()), sum(fonte.values())
        def testo(d):
            return ", ".join(f"{k.upper()} {v:+d}"
                             for k, v in sorted(d.items())) or "nessuno"
        scarto = ", ".join(
            f"{k.upper()} {adj.get(k, 0) - fonte.get(k, 0):+d}"
            for k in sorted(set(adj) | set(fonte))
            if adj.get(k, 0) != fonte.get(k, 0)) or "—"
        print(f"| {r['name']['it'][:34]} | {testo(adj)} | {n5:+d} | "
              f"{testo(fonte)} | {n2:+d} | {scarto} |")


def main():
    righe, classi = analizza()
    stampa(righe, classi)
    rapporto_negativi()


if __name__ == "__main__":
    main()
