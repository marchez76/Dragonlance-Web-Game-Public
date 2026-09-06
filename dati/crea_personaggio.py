#!/usr/bin/env python3
"""
Percorre la creazione di un personaggio e ne scrive la scheda.

NON E' UN ESEMPIO INVENTATO. Ogni passo qui sotto legge il filtro dai dati
prima di risolverlo, e stampa quello che ha letto: se un filtro non esiste,
si vede al passo in cui serviva e non a posteriori. E' lo stesso rapporto fra
prova e affermazione che il progetto usa altrove — la scheda che esce e' il
risultato, ma il valore sta nel percorso che la produce.

PERCHE' DUE PERSONAGGI E NON UNO
    Uno solo non basta a mettere sotto sforzo lo schema. `chierica-di-mishakal`
    e' un 1° livello e percorre la creazione intera: razza con tre scelte
    aperte (l'Umano della decisione 19, `compensazione-umano`), classe il cui
    vincolo di allineamento NON e' suo ma del dio
    (decisione 24, `sfere-sacerdotali`), e le cinque righe dell'elenco
    iniziale. `arcanista-dargonesti` e' un 7° livello, e serve a un solo
    scopo: l'unica scelta razziale di incantesimo che i dati portino arriva al
    7° livello e non alla creazione. Senza di lui il campo `al_livello`
    sarebbe sembrato inutile.

I TIRI SONO SEMI, NON NUMERI. Il generatore tira con un seme fisso: la scheda
si rigenera identica, e i sei punteggi restano DERIVATI da una procedura
invece che scritti a mano (CLAUDE.md, punto 3).

Uso:  uv run --with jsonschema python3 dati/crea_personaggio.py
"""

import glob
import hashlib
import json
import os
import random
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(RADICE, "motore"))

import _allineamenti as AL      # noqa: E402
import _sistema as sistema      # noqa: E402
import generazione as G         # noqa: E402

CARTELLA = os.path.join(BASE, "personaggi")
OGGI = "2026-09-06"
CAR = ["str", "dex", "con", "int", "wis", "cha"]


def passo(n, titolo):
    print(f"\n### {n}. {titolo}")


def letto(cosa, sede):
    print(f"    letto: {cosa}\n      da   {sede}")


def scelto(cosa):
    print(f"    scelto: {cosa}")


# --------------------------------------------------------------- l'impronta

def impronta():
    """Contro quale versione dei dati questa scheda e' stata costruita.

    Le cartelle che il personaggio RIFERISCE, e nient'altro. Non conserva il
    dato, conserva il modo di accorgersi che e' cambiato.
    """
    h = hashlib.sha256()
    for c in ("razze", "classi", "divinita", "oggetti", "pacchetti",
              "incantesimi", "sistema"):
        for p in sorted(glob.glob(os.path.join(BASE, c, "*.json"))):
            with open(p, "rb") as fh:
                h.update(os.path.basename(p).encode())
                h.update(fh.read())
    return h.hexdigest()[:16]


# ------------------------------------------------------- passi di creazione

def scegli_razza(rid):
    passo(1, "La razza")
    razza = G.carica_razza(rid)
    n = len(glob.glob(os.path.join(BASE, "razze", "*.json")))
    letto(f"{n} razze fra cui scegliere", "dati/razze/")
    scelto(f"{rid} — {razza['name']['it']}")
    return razza


def scegli_classe(razza, cid):
    passo(2, "La classe, contro il filtro che la razza impone")
    perc = G.percorsi(razza)
    aperte = [r[0] for r in perc if r[1]]
    letto(f"{len(aperte)} classi aperte su {len(perc)}",
          "motore/generazione.percorsi() — vedi "
          "decisione 58 (`telaio-apre-classe-filtra`)")
    assert cid in aperte, f"{cid} non e' aperta a {razza['id']}"
    classe = G.carica_classe(cid)
    liv = (classe["mechanics_5e"].get("entry_level") or 1)
    print(f"    entry_level = {liv}: "
          + ("classe di partenza" if liv == 1 else "NON di partenza"))
    scelto(f"{cid} — {classe['name']['it']}")
    return classe


def scegli_punteggi(razza, classe, seme):
    passo(3, "I sei punteggi")
    prat = G.metodi_praticabili(razza, classe)
    aperti = [m for m, ok in prat.items() if ok]
    letto(f"metodi praticabili: {', '.join(aperti)}",
          "dati/sistema/generazione-caratteristiche.json + "
          "decisione 60 (`metodo-non-filtra`)")
    metodo = "tiro-4d6-scarta-minore"
    rng = random.Random(seme)
    valori, libera = G.genera(razza, metodo, rng)
    assert libera is True, "questa razza non lascia l'assegnazione libera"
    lo, hi = G.intervalli(razza, classe)
    vincolate = {c: (lo[c], hi[c]) for c in CAR if lo[c] > 3 or hi[c] < 99}
    letto(f"tirati {sorted(valori, reverse=True)} con seme {seme}",
          f"generazione.genera(metodo={metodo})")
    letto(f"intervalli vincolati: {vincolate or 'nessuno'}",
          "generazione.intervalli() — decisione 3 (`vincoli-caratteristica`)")
    return metodo, valori, (lo, hi)


def assegna(valori, ordine, razza, lo, hi):
    """Assegna i valori tirati nell'ordine di priorita' chiesto."""
    restanti = sorted(valori, reverse=True)
    punteggi = {}
    for car in ordine:
        punteggi[car] = restanti.pop(0)
    agg = G.applica_aggiustamenti(punteggi, razza)
    for c in CAR:
        assert lo[c] <= agg[c] <= hi[c], (
            f"{c}={agg[c]} fuori dall'intervallo [{lo[c]}, {hi[c]}]")
    print(f"    assegnati (grezzi):  {punteggi}")
    print(f"    con aggiustamenti:   {agg}   <- LETTURA, non un campo della "
          f"scheda")
    return punteggi


def scegli_divinita(classe, did):
    passo(4, "La divinita', e con essa il filtro sull'allineamento")
    a = classe["mechanics_5e"].get("alignment_restriction") or {}
    print(f"    la classe NON porta l'insieme: applied={a.get('applied')}, "
          f"depends_on={a.get('depends_on')!r}")
    d = json.load(open(os.path.join(BASE, "divinita", f"{did}.json"),
                       encoding="utf-8"))
    testo = d["source_2e"]["priest_alignment"]
    insieme = sorted(AL._da_priest(testo))
    letto(f"priest_alignment = {testo!r} -> {insieme}",
          f"dati/divinita/{did}.json + _allineamenti._da_priest() — "
          f"decisione 61 (`allineamento-insieme`)")
    scelto(f"{did}; allineamento fra {len(insieme)} valori")
    return d, insieme


def elenco_iniziale(classe):
    passo(6, "L'elenco iniziale, riga per riga")
    righe = (classe["mechanics_5e"]["structural"]["starting_equipment"]
             ["scelte"])
    letto(f"{len(righe)} righe, ciascuna un'alternativa fra "
          f"{[len(r['alternative']) for r in righe]}",
          "mechanics_5e.structural.starting_equipment.scelte — "
          "decisione 62 (`pacchetto-fisso`)")
    for i, r in enumerate(righe):
        for j, alt in enumerate(r["alternative"]):
            voci = ", ".join(
                f"{v['quantita']}x {v['name_srd']}"
                + ("  [SCELTA]" if v["genere"] == "scelta" else "")
                + ("  [PACCHETTO]" if v["genere"] == "pacchetto" else "")
                for v in alt["voci"])
            print(f"      riga {i}, alternativa {j}: {voci}")
    return righe


def scheda(**campi):
    return campi


# ------------------------------------------------------------ i due percorsi

def chierica():
    print("\n" + "=" * 74)
    print("PERCORSO 1 — Umano / Sacerdote degli Ordini Sacri, 1° livello")
    print("=" * 74)

    razza = scegli_razza("umano")
    classe = scegli_classe(razza, "sacerdote-ordini-sacri")
    metodo, valori, (lo, hi) = scegli_punteggi(razza, classe, seme=1988)
    punteggi = assegna(valori, ["wis", "con", "str", "cha", "dex", "int"],
                       razza, lo, hi)
    dio, allineamenti = scegli_divinita(classe, "mishakal")
    allineamento = "legale_buono"
    assert allineamento in allineamenti

    passo(5, "Le tre scelte che l'Umano lascia aperte")
    tratti = {t["name"]: (t.get("mechanics_5e") or "")
              for t in razza["mechanics_5e"]["traits"]}
    for n in ("Adattabilita'", "Versatilita'", "Lingua franca"):
        letto(f"{n}: «{tratti[n]}»",
              "dati/razze/umano.json -> traits[].mechanics_5e  "
              "(PROSA: filtro non applicabile)")
    letto(f"{len(sistema.ABILITA)} abilita' fra cui scegliere",
          "dati/sistema/abilita.json — l'insieme che PRIMA non c'era")
    scelto("+1 SAG, +1 COS; abilita' medicine; lingua Solamnico")

    righe = elenco_iniziale(classe)
    prese = [(0, 0, []), (1, 0, []), (2, 1, [("arma semplice", "quarterstaff")]),
             (3, 0, []), (4, 0, [("simbolo sacro", None)])]
    print("    scelte:")
    for i, j, ris in prese:
        voci = ", ".join(v["name_srd"] for v in righe[i]["alternative"][j]["voci"])
        print(f"      riga {i} -> alternativa {j}: {voci}"
              + (f"   risolvendo {ris}" if ris else ""))

    return scheda(
        id="chierica-di-mishakal",
        nome="Ilenya di Xak Tsaroth",
        corpus={"generato_il": OGGI, "impronta": impronta()},
        razza="umano", classe="sacerdote-ordini-sacri", livello=1,
        punteggi=punteggi, metodo_punteggi=metodo,
        allineamento=allineamento, divinita="mishakal",
        lingue=[{"lingua": "Solamnico", "aperta_da": "razza:umano"}],
        scelte={
            "competenze_abilita": {
                "aperta_da": "razza:umano", "al_livello": 1,
                "filtro": {"sede": "dati/sistema/abilita.json",
                           "chiuso": True, "quante": None},
                "valori": ["medicine"]},
            "aumenti_caratteristica": {
                "aperta_da": "razza:umano", "al_livello": 1,
                "filtro": {"sede": "dati/razze/umano.json -> "
                                   "mechanics_5e.traits[]",
                           "chiuso": False, "quante": 2},
                "valori": [{"caratteristica": "wis", "valore": 1},
                           {"caratteristica": "con", "valore": 1}]},
            "equipaggiamento_iniziale": {
                "aperta_da": "classe:sacerdote-ordini-sacri", "al_livello": 1,
                "filtro": {"sede": "dati/classi/sacerdote-ordini-sacri.json "
                                   "-> mechanics_5e.structural."
                                   "starting_equipment.scelte",
                           "chiuso": True, "quante": len(righe)},
                "valori": [
                    {"riga": i, "alternativa": j,
                     **({"risolti": [{"voce": v, "oggetto": o}
                                     for v, o in ris]} if ris else {})}
                    for i, j, ris in prese]},
        },
        equipaggiato={"arma": "mace", "armatura": "scale-mail",
                      "scudo": "shield"},
        note=["Il simbolo sacro resta senza oggetto: il filtro non ha "
              "campioni a catalogo, ed e' l'unica delle cinque scelte aperte "
              "che non abbia un'alternativa nella stessa riga.",
              "L'assegnazione dei punteggi mette la Saggezza per prima: e' "
              "una scelta del giocatore, non un vincolo — il sacerdote non "
              "porta minimi di caratteristica applicati."])


def arcanista():
    print("\n" + "=" * 74)
    print("PERCORSO 2 — Elfo Dargonesti / Mago Rinnegato, 7° livello")
    print("=" * 74)

    razza = scegli_razza("elfo-dargonesti")
    classe = scegli_classe(razza, "mago-rinnegato")
    metodo, valori, (lo, hi) = scegli_punteggi(razza, classe, seme=351)
    punteggi = assegna(valori, ["int", "dex", "con", "wis", "cha", "str"],
                       razza, lo, hi)

    passo(4, "L'incantesimo razziale — e a che livello si sceglie davvero")
    t = [x for x in razza["mechanics_5e"]["traits"]
         if x["name"].startswith("Incantesimi innati")][0]
    letto(f"«{t['mechanics_5e'][:220]}...»",
          "dati/razze/elfo-dargonesti.json -> traits[]")
    print("    al 3° e al 5° la razza NOMINA l'incantesimo: li' non si "
          "sceglie niente, e scriverlo sulla scheda sarebbe una COPIA.")
    print("    al 7° l'incantesimo e' A SCELTA: e' l'unica scelta razziale "
          "di incantesimo che i dati portino, e non e' di creazione.")
    n_inc = len(glob.glob(os.path.join(BASE, "incantesimi", "*.json")))
    letto(f"{n_inc} incantesimi a catalogo (bersaglio del riferimento)",
          "dati/incantesimi/")
    scelto("misty-step, al 7° livello")

    righe = elenco_iniziale(classe)
    prese = []
    for i, r in enumerate(righe):
        ris = [(v["name_srd"], None) for v in r["alternative"][0]["voci"]
               if v["genere"] == "scelta"]
        prese.append((i, 0, ris))
    print("    scelte: la prima alternativa di ogni riga")

    return scheda(
        id="arcanista-dargonesti",
        nome="Tanis Ondalunga",
        corpus={"generato_il": OGGI, "impronta": impronta()},
        razza="elfo-dargonesti", classe="mago-rinnegato", livello=7,
        punteggi=punteggi, metodo_punteggi=metodo,
        allineamento="caotico_neutrale", divinita=None,
        lingue=[],
        scelte={
            "incantesimo_razziale": {
                "aperta_da": "razza:elfo-dargonesti", "al_livello": 7,
                "filtro": {"sede": "dati/razze/elfo-dargonesti.json -> "
                                   "traits[] (bersaglio: dati/incantesimi/)",
                           "chiuso": False, "quante": 1},
                "valori": ["misty-step"]},
            "equipaggiamento_iniziale": {
                "aperta_da": "classe:mago-rinnegato", "al_livello": 1,
                "filtro": {"sede": "dati/classi/mago-rinnegato.json -> "
                                   "mechanics_5e.structural."
                                   "starting_equipment.scelte",
                           "chiuso": True, "quante": len(righe)},
                "valori": [
                    {"riga": i, "alternativa": j,
                     **({"risolti": [{"voce": v, "oggetto": o}
                                     for v, o in ris]} if ris else {})}
                    for i, j, ris in prese]},
        },
        equipaggiato={"arma": "quarterstaff", "armatura": None,
                      "scudo": None},
        note=["Nessuna lingua scelta: la razza non lascia questa scelta "
              "aperta, e `languages` e' vuoto nei dati — questione aperta "
              "(`lingue-di-krynn`).",
              "7° livello e non 1°: l'unica scelta razziale di incantesimo "
              "che i dati portino arriva li', e un personaggio di 1° non "
              "avrebbe potuto esercitare il campo."])


def main():
    os.makedirs(CARTELLA, exist_ok=True)
    print("# Percorso di creazione — la scheda esce da qui, non viceversa")
    for costruisci in (chierica, arcanista):
        p = costruisci()
        percorso = os.path.join(CARTELLA, p["id"] + ".json")
        with open(percorso, "w", encoding="utf-8") as fh:
            json.dump(p, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        print(f"\n    scritto dati/personaggi/{p['id']}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
