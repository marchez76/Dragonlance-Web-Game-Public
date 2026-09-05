#!/usr/bin/env python3
"""
Valida dati/classi/*.json contro lo schema, piu' controlli di coerenza interna
e CONTROLLO INCROCIATO con dati/razze/*.json.

Il controllo incrociato e' il piu' utile: le razze e le classi sono state
estratte da due tabelle diverse dello stesso manuale, quindi devono raccontare
la stessa storia. Se una razza dichiara di poter fare il Tinker ma il Tinker
dichiara di essere riservato agli gnomi, una delle due trascrizioni e' sbagliata.

Uso:  python3 dati/valida_classi.py
"""

import copy
import glob
import json
import os
import sys

import jsonschema

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import _chassis_5e as _CH  # noqa: E402
import _classi_ammesse as _CA  # noqa: E402
import _schemi as S  # noqa: E402
Validator = getattr(jsonschema, "Draft202012Validator", None) or jsonschema.Draft7Validator

# Nomi della tabella Class/Race Combinations -> id delle nostre classi.
#
# NON SI SCRIVE QUI. Questa mappa era la DODICESIMA struttura doppia del
# progetto: la stessa corrispondenza etichetta 2e -> nostra classe viveva qui
# e in `analizza_allowed_classes.py`, ed era gia' divergente il giorno in cui
# e' stata trovata — qui `Knight of Solamnia` valeva il solo Cavaliere della
# Corona, di la' i tre ordini. Nessuna esecuzione metteva le due copie una
# contro l'altra, quindi la divergenza non poteva emergere da sola.
#
# La sede e' `_classi_ammesse.ETICHETTE`, decisione 58 (`telaio-apre-classe-filtra`).
# Qui si legge il solo campo che serve al
# controllo incrociato: le classi che l'etichetta NOMINA. Il telaio non
# c'entra — questo controllo confronta due tabelle del manuale fra loro, non
# la conversione 5e.
MAPPA_TABELLA = {e: v.classi for e, v in _CA.ETICHETTE.items() if v.classi}


def coerenza(d, err):
    s = d["source_2e"]

    for k, v in s["ability_minimums"].items():
        if not (1 <= v <= 25):
            err(f"minimo {k} = {v} implausibile")

    prog = s.get("progression") or []
    if prog:
        if prog[0]["level"] != s["entry_level"]:
            err(f"la progressione parte dal livello {prog[0]['level']} "
                f"ma entry_level e' {s['entry_level']}")
        if prog[0]["xp"] != 0:
            err(f"la progressione non parte da 0 PE ma da {prog[0]['xp']}")
        for a, b in zip(prog, prog[1:]):
            if b["level"] != a["level"] + 1:
                err(f"salto di livello nella progressione: {a['level']} -> {b['level']}")
            if b["xp"] <= a["xp"]:
                err(f"i PE non crescono fra il livello {a['level']} e il {b['level']}")

    sp = s.get("spell_progression")
    if sp:
        livelli = sorted(int(k) for k in sp)
        for a, b in zip(livelli, livelli[1:]):
            if b != a + 1:
                err(f"salto nella tabella incantesimi: {a} -> {b}")
        larghezze = {len(v) for v in sp.values()}
        if len(larghezze) != 1:
            err(f"la tabella incantesimi ha righe di lunghezza diversa: {larghezze}")
        # il totale degli incantesimi non deve mai diminuire salendo di livello
        for a, b in zip(livelli, livelli[1:]):
            if sum(sp[str(b)]) < sum(sp[str(a)]):
                err(f"gli incantesimi totali calano fra il livello {a} e il {b}")

    if s.get("xp_bonus"):
        ab = s["xp_bonus"]["ability"]
        minimo = s["ability_minimums"].get(ab)
        if minimo is not None and s["xp_bonus"]["threshold"] < minimo:
            err(f"la soglia del bonus PE ({s['xp_bonus']['threshold']}) "
                f"e' sotto il minimo richiesto per {ab} ({minimo})")


def incrociato(classi, razze, err):
    """La tabella Class/Race Combinations delle razze deve concordare
    con le restrizioni di razza dichiarate dalle classi."""
    per_id = {c["id"]: c for c in classi}

    for r in razze:
        for voce in r["source_2e"].get("class_level_limits", []):
            nominate = MAPPA_TABELLA.get(voce["class"], ())
            # Un'etichetta ombrello ne nomina piu' di una: la contraddizione
            # c'e' solo se le esclude TUTTE. `Knight of Solamnia` concessa al
            # mezzelfo non e' una contraddizione perche' un ordine dei tre lo
            # ammette, e sarebbe diventata tale con una mappa a una voce sola.
            ammesse = []
            for cid in nominate:
                c = per_id.get(cid)
                if c is None:
                    err(f"{r['id']}: la tabella cita '{voce['class']}' ma la "
                        f"classe {cid} non esiste")
                    continue
                restr = c["source_2e"].get("race_restriction")
                if not restr or r["id"] in restr:
                    ammesse.append(cid)
            if nominate and not ammesse:
                err(f"CONTRADDIZIONE: la razza {r['id']} puo' prendere "
                    f"'{voce['class']}' (tetto {voce['limit']}) ma nessuna "
                    f"delle classi che l'etichetta nomina "
                    f"({', '.join(nominate)}) l'ammette")

    # e viceversa: una classe riservata a una razza deve comparire fra i suoi limiti
    per_razza = {r["id"]: {v["class"] for v in r["source_2e"].get("class_level_limits", [])}
                 for r in razze}
    # Una classe puo' essere nominata da PIU' etichette (`Priest (heathen)` e
    # `Druid (heathen)` sono lo stesso Sacerdote Eretico): il rovescio della
    # mappa e' quindi un insieme, e non un valore solo. Con un dizionario
    # rovesciato una delle due etichette spariva in silenzio.
    inverso = {}
    for e, cids in MAPPA_TABELLA.items():
        for cid in cids:
            inverso.setdefault(cid, set()).add(e)
    for c in classi:
        restr = c["source_2e"].get("race_restriction")
        nomi_tab = inverso.get(c["id"])
        if not restr or not nomi_tab:
            continue
        for rid in restr:
            if rid not in per_razza:
                err(f"{c['id']}: race_restriction cita la razza inesistente '{rid}'")
            elif not per_razza[rid]:
                # Gli umani non compaiono nella tabella Class/Race Combinations
                # perche' in 2e non hanno limiti di livello: assenza attesa, non errore.
                continue
            elif not (nomi_tab & per_razza[rid]):
                err(f"{c['id']} e' riservata a {rid}, ma nessuna delle etichette "
                    f"che la nominano ({', '.join(sorted(nomi_tab))}) compare "
                    f"fra i class_level_limits di quella razza")

    # le catene di ordini devono essere ben formate
    for c in classi:
        rq = c.get("requires_class")
        if rq and rq not in per_id:
            err(f"{c['id']}: requires_class punta a '{rq}' che non esiste")
        if c.get("tier") and c["tier"] > 1 and not rq:
            err(f"{c['id']}: tier {c['tier']} senza requires_class")


# --------------------------------------------------------------------------
# IL CONTROLLO SI METTE ALLA PROVA — stesso schema di `_sistema.COPIE_PIANTATE`
# e di `_schemi.prova_di_se_stesso`.
#
# Su un repository pulito un controllo incrociato rotto e uno funzionante
# tacciono uguale, e questo e' appena stato riscritto per leggere la mappa da
# `_classi_ammesse` invece che da una copia sua. Prima di dichiarare che non
# ci sono contraddizioni, gliene si mettono davanti due piantate apposta e una
# somiglianza legittima che NON deve segnalare.
# --------------------------------------------------------------------------

def _senza_ombrello(classi, razze):
    """Somiglianza legittima: il mezzelfo dichiara `Knight of Solamnia`, che
    nomina tre ordini. Due dei tre lo ammettono e uno no. Con una mappa a un
    valore solo questo caso poteva diventare un falso allarme."""
    return classi, razze


def _kender_tinker(classi, razze):
    r = copy.deepcopy(razze)
    next(x for x in r if x["id"] == "kender")["source_2e"][
        "class_level_limits"].append({"class": "Tinker", "limit": None})
    return classi, r


def _eretico_riservato(classi, razze):
    c = copy.deepcopy(classi)
    next(x for x in c if x["id"] == "sacerdote-eretico")["source_2e"][
        "race_restriction"] = ["minotauro"]
    return c, razze


PIANTATI = [
    ("una razza dichiara un'etichetta riservata a un'altra razza", _kender_tinker, True),
    ("una classe e' riservata a una razza che non la dichiara", _eretico_riservato, True),
    ("etichetta ombrello ammessa da due ordini su tre", _senza_ombrello, False),
]


def prova_di_se_stesso(classi, razze):
    """Lista di fallimenti della prova. Vuota = il controllo vede e tace
    quando deve."""
    fuori = []
    for nome, muta, atteso in PIANTATI:
        c, r = muta(classi, razze)
        errori = []
        incrociato(c, r, errori.append)
        if bool(errori) != atteso:
            fuori.append(
                f"{nome}: atteso {'un errore' if atteso else 'silenzio'}, "
                f"ottenuto {'un errore' if errori else 'silenzio'}")
    return fuori


def main():
    # IL VALIDATORE VIENE DA `_schemi`, non piu' costruito qui.
    # Dal 04/09/2026 `chassis_features[].conversion_status` non e' piu' una
    # stringa libera ma un `$ref` a `vocabolari.schema.json`: un `$ref` fra
    # file non si risolve senza registro, e un validatore senza registro non
    # sbaglia rumorosamente — lascia passare tutto e il vocabolario sembra
    # applicato. Per questo il registro arriva dalla sede, e i tre controlli
    # sotto provano che il riferimento risolva davvero.
    schema = S.carica("classe.schema.json")
    v = S.validatore("classe.schema.json", schema)

    schemi_errori = 0
    for m in S.verifica_riferimenti():
        print(f"\u2717 {m}")
        schemi_errori += 1
    _visti, _quanti, prova = S.prova_di_se_stesso()
    for m in prova:
        print(f"\u2717 {m}")
        schemi_errori += 1
    for m in S.verifica_origine():
        print(f"\u2717 {m}")
        schemi_errori += 1

    files = sorted(glob.glob(os.path.join(BASE, "classi", "*.json")))
    classi = [json.load(open(p, encoding="utf-8")) for p in files]
    razze = [json.load(open(p, encoding="utf-8"))
             for p in sorted(glob.glob(os.path.join(BASE, "razze", "*.json")))]

    # I RIMANDI AL CHASSIS, dal 04/09/2026.
    # Un privilegio della fonte la cui meccanica 5e e' gia' quella del chassis
    # porta un rimando invece di `null` (decisione 23, `principio-del-clone`,
    # e _chassis_5e). Un rimando vale solo se il bersaglio esiste: qui si
    # rifa' sui file la prova che la sede fa in costruzione, perche' il
    # bersaglio sta in un elenco SRD che puo' cambiare dopo che il file e'
    # stato scritto — e una copia che combacia il giorno in cui nasce e'
    # esattamente la forma che questo progetto ha visto sfasarsi dodici volte.
    for m in _CH.verifica_rimandi(classi):
        print(f"\u2717 {m}")
        schemi_errori += 1

    totale = schemi_errori
    for p, d in zip(files, classi):
        errori = []
        for e in sorted(v.iter_errors(d), key=lambda e: list(e.path)):
            errori.append(f"[schema] {'.'.join(map(str, e.path)) or '(radice)'}: {e.message[:120]}")
        if not errori:
            coerenza(d, errori.append)
        if errori:
            totale += len(errori)
            print(f"✗ {os.path.basename(p)}")
            for e in errori:
                print(f"    {e}")
        else:
            print(f"✓ {os.path.basename(p)}")

    print("\n--- il controllo incrociato si mette alla prova ---")
    fuori = prova_di_se_stesso(classi, razze)
    if fuori:
        totale += len(fuori)
        for e in fuori:
            print(f"    ✗ {e}")
    else:
        print(f"    ✓ {len(PIANTATI)} casi: "
              f"{sum(1 for _n, _m, a in PIANTATI if a)} difetti piantati visti, "
              f"{sum(1 for _n, _m, a in PIANTATI if not a)} somiglianza legittima taciuta")

    print("\n--- controllo incrociato razze/classi ---")
    incr = []
    incrociato(classi, razze, incr.append)
    if incr:
        totale += len(incr)
        for e in incr:
            print(f"    ✗ {e}")
    else:
        print("    ✓ nessuna contraddizione fra le due tabelle")

    print(f"\n{len(files)} classi e {len(razze)} razze controllate, {totale} errori.")
    return 1 if totale else 0


if __name__ == "__main__":
    sys.exit(main())
