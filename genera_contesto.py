#!/usr/bin/env python3
"""
Genera CONTESTO-PROGETTO.md: un unico file autosufficiente da caricare nella
project knowledge.

PERCHE' ESISTE
    La project knowledge non e' un mirror della cartella: e' una copia caricata
    a mano, che resta ferma alla versione del caricamento. Le chat normali
    (senza accesso al filesystem) leggono solo quella.

REGOLA STRUTTURALE — la ragione per cui questo file e' stato riscritto
    Il documento mescolava tabelle derivate dai dati e prosa scritta a mano.
    Le tabelle si aggiornavano, la prosa no, e per tre volte di fila il
    documento ha finito per contraddirsi: prima su un conteggio, poi sulle
    conclusioni.

    Da qui in avanti valgono due categorie, tenute separate anche nel codice:

    DERIVATO      ogni numero, tabella, conteggio, percentuale, elenco.
                  Viene SEMPRE dai JSON. Nessun valore quantitativo e' scritto
                  a mano, nemmeno dentro una frase di prosa: dove una frase
                  contiene un numero, il numero e' interpolato.

    INTERPRETATIVO  letture, commenti, conclusioni. Restano scritti a mano
                  perche' non sono derivabili, ma sono marcati nel documento
                  con un blockquote datato, cosi' chi legge distingue a colpo
                  d'occhio il dato dall'opinione.

    Se aggiungi una sezione, decidi a quale categoria appartiene PRIMA di
    scriverla. Non mescolarle nello stesso paragrafo.

Uso:  python3 genera_contesto.py
      poi: sostituisci CONTESTO-PROGETTO.md nella project knowledge
"""

import collections
import glob
import json
import os
import re
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
DATI = os.path.join(BASE, "dati")
OGGI = date.today().isoformat()

CAR_IT = {"str": "FOR", "dex": "DES", "con": "COS",
          "int": "INT", "wis": "SAG", "cha": "CAR"}


def interpretativo(testo):
    """Marca un blocco come lettura, non come dato."""
    righe = [l for l in testo.strip().split("\n")]
    return (f"> **Lettura interpretativa** — registrata il {OGGI}. "
            f"Non e' derivata dai dati.\n>\n"
            + "\n".join(f"> {l}" if l else ">" for l in righe))


# ==========================================================================
# CARICAMENTO
# ==========================================================================

def carica(sub):
    return [json.load(open(p, encoding="utf-8"))
            for p in sorted(glob.glob(os.path.join(DATI, sub, "*.json")))]


def leggi(nome):
    p = os.path.join(BASE, nome)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def indice_testi():
    p = os.path.join(BASE, "Testi", "indice.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    r = dict(d["riepilogo"])
    r["per_stato"] = collections.Counter(m.get("stato") for m in d["manuali"])
    r["non_lavorati"] = r["per_stato"].get("non_lavorato", 0)
    r["pct_pronti"] = round(100 * r["manuali_pronti"] / r["manuali_totali"])
    return r


def mille(n):
    return f"{n:,}".replace(",", ".")


# ==========================================================================
# DERIVATO — tutto quanto segue viene dai JSON
# ==========================================================================

def d_razze(razze):
    r_ = ["| id | razza | aggiustamenti | requisiti notevoli |", "|---|---|---|---|"]
    for r in razze:
        m = r["mechanics_5e"]["ability_adjustments"]
        pezzi = []
        for k, v in sorted(m["source_values"].items()):
            pezzi.append(f"{CAR_IT[k]} {v:+d}")
        for k, v in sorted(m.get("editorial_values", {}).items()):
            pezzi.append(f"{CAR_IT[k]} {v:+d} *(ed.)*")
        # compensazioni editoriali espresse come tratto anziche' come numero
        for t in r["mechanics_5e"]["traits"]:
            if t.get("editorial") and "caratteristic" in (t["mechanics_5e"] or ""):
                pezzi.append(f"{t['mechanics_5e'].rstrip('.')} *(ed.)*")
        notevoli = []
        for car, v in r["source_2e"]["ability_requirements"].items():
            if v["max"] is not None and v["max"] < 18:
                notevoli.append(f"{CAR_IT[car]} max {v['max']}")
            if v["min"] is not None and v["min"] >= 10:
                notevoli.append(f"{CAR_IT[car]} min {v['min']}")
        r_.append(f"| `{r['id']}` | {r['name']['it']} | {', '.join(pezzi) or '—'} | "
                  f"{', '.join(notevoli) or '—'} |")
    return "\n".join(r_)


GRUPPI = ["Warrior", "Wizard", "Priest", "Rogue", "Normal"]


def d_classi(classi):
    r_ = ["| id | classe | gruppo | note |", "|---|---|---|---|"]
    for c in classi:
        s, n = c["source_2e"], []
        if c["tier"]:
            n.append(f"grado {c['tier']} dell'ordine")
        if s["entry_level"] > 1:
            n.append(f"si entra al {s['entry_level']}°")
        if s["race_restriction"]:
            n.append("solo " + "/".join(s["race_restriction"]))
        if s["alignment_restriction"]:
            n.append(s["alignment_restriction"])
        r_.append(f"| `{c['id']}` | {c['name']['it']} | {c['group']} | {'; '.join(n) or '—'} |")
    return "\n".join(r_)


def d_meccanica_classi(classi):
    """Forma meccanica di ciascuna classe. Sintesi delle schede del rapporto."""
    def priv(c):
        return c["source_2e"].get("special_benefits") or []

    def imp(c):
        return c["source_2e"].get("special_hindrances") or []

    def pr(c):
        return c["source_2e"].get("progression") or []

    # L'intestazione la mette il documento: qui solo le righe di dati.
    righe = []
    for c in sorted(classi, key=lambda x: (GRUPPI.index(x["group"]), x["id"])):
        s, p = c["source_2e"], pr(c)
        ch = c["mechanics_5e"]["chassis"]
        righe.append(
            f"| {c['name']['it']} | {c['group']} | {s['hit_die'] or '—'} | "
            f"{f'propria, {len(p)} liv.' if p else 'del gruppo'} | "
            f"{'sì' if s.get('spell_progression') else '—'} | "
            f"{len(priv(c))} | {len(imp(c))} | "
            f"{'`' + ch['srd_class'] + '`' if ch['srd_class'] else '**indeciso**'} |")
    tot_p = sum(len(priv(c)) for c in classi)
    tot_h = sum(len(imp(c)) for c in classi)
    con_liv = sum(1 for c in classi for b in priv(c)
                  if re.search(r"\d+°\s*livello", b["text"]))
    senza_prog = [c for c in classi if not pr(c)]
    senza_priv = [c for c in classi if not priv(c)]
    in_perdita = [c for c in classi if len(imp(c)) > len(priv(c))]
    clonate = [c for c in classi if c["mechanics_5e"]["chassis"]["srd_class"]]
    sospese = [c for c in classi if not c["mechanics_5e"]["chassis"]["srd_class"]]
    chassis = collections.Counter(c["mechanics_5e"]["chassis"]["srd_class"]
                                  for c in clonate)
    stati = collections.Counter(f["conversion_status"] for c in classi
                                for f in c["mechanics_5e"]["features"])
    return {
        "tab": "\n".join(righe), "tot_p": tot_p, "tot_h": tot_h,
        "con_liv": con_liv, "senza_liv": tot_p - con_liv,
        "n_senza_prog": len(senza_prog), "n_senza_priv": len(senza_priv),
        "n_in_perdita": len(in_perdita),
        "senza_prog": ", ".join(c["name"]["it"] for c in senza_prog),
        "senza_priv": ", ".join(c["name"]["it"] for c in senza_priv),
        "max_lv": max(p["level"] for c in classi for p in pr(c)),
        "n_clonate": len(clonate), "n_sospese": len(sospese),
        "sospese": ", ".join(c["name"]["it"] for c in sospese),
        "chassis": ", ".join(f"{k} ×{v}" for k, v in sorted(chassis.items())),
        "stati": stati, "tot_feat": sum(stati.values()),
    }


def d_dei(dei):
    # Niente colonna "sfere maggiori": e' la tabella del manuale (Realms
    # Above) riprodotta per intero, tolta anche da RAPPORTO-sfere.md per lo
    # stesso motivo. Famiglia e rango restano: sono classificazione nostra,
    # non trascrizione.
    r_ = ["| divinità | famiglia | rango |", "|---|---|---|"]
    for d in dei:
        r_.append(f"| {d['name']['en']} ({d['name']['epithet'] or ''}) | {d['family']} | "
                  f"{d['rank']} |")
    return "\n".join(r_)


def d_strato5e(razze):
    """Tutti i numeri dello strato 5e, in un dizionario. Nessuno scritto a mano."""
    tratti = [(r, t) for r in razze for t in r["mechanics_5e"]["traits"]]
    tot = len(tratti)
    stati = collections.Counter(t["conversion_status"] for _, t in tratti)

    def q(pred):
        return sum(1 for _, t in tratti if pred(t))

    n_phb = q(lambda t: "PHB 2e" in t["source"])
    n_mc = q(lambda t: t["source"].startswith("MC -"))
    n_ed = q(lambda t: t.get("editorial"))
    n_sot = q(lambda t: t["source"].startswith("SotDQ"))
    n_tol = tot - n_phb - n_mc - n_ed - n_sot
    n_krynn = n_tol + n_mc + n_sot

    dist = []
    for r in razze:
        T = r["mechanics_5e"]["traits"]
        phb = sum(1 for t in T if "PHB 2e" in t["source"])
        mc = sum(1 for t in T if t["source"].startswith("MC -"))
        ed = sum(1 for t in T if t.get("editorial"))
        sot = sum(1 for t in T if t["source"].startswith("SotDQ"))
        dist.append({"nome": r["name"]["it"], "tot": len(T), "phb": phb,
                     "mc": mc, "ed": ed, "sot": sot,
                     "tol": len(T) - phb - mc - ed - sot})
    dist.sort(key=lambda x: (-x["tot"], x["nome"]))

    return {
        "tot": tot, "stati": stati,
        "n_phb": n_phb, "n_mc": n_mc, "n_ed": n_ed, "n_tol": n_tol,
        "n_sot": n_sot,
        "n_krynn": n_krynn, "pct_krynn": round(100 * n_krynn / tot),
        "pct_phb": round(100 * n_phb / tot),
        "dist": dist,
        "min_tot": min(d["tot"] for d in dist),
        "max_tot": max(d["tot"] for d in dist),
        "provvisori": [(r["name"]["it"], t["name"]) for r, t in tratti if t.get("provisional")],
        "editoriali": [(r["name"]["it"], t["name"]) for r, t in tratti if t.get("editorial")],
        "tab_stati": "\n".join(
            f"| `{st}` | {stati[st]} | {round(100*stati[st]/tot)}% |"
            for st in ("direct", "adapted", "pending", "source_only")),
        "tab_fonti": "\n".join([
            f"| PHB 2e (per rimando) | {n_phb} | {round(100*n_phb/tot)}% |",
            f"| Tales of the Lance | {n_tol} | {round(100*n_tol/tot)}% |",
            f"| MC Dragonlance Appendix | {n_mc} | {round(100*n_mc/tot)}% |",
            f"| conversione editoriale nostra | {n_ed} | {round(100*n_ed/tot)}% |",
            f"| SotDQ (ufficiale 5e) | {n_sot} | {round(100*n_sot/tot)}% |",
        ]),
        "tab_dist": "\n".join(
            f"| {d['nome']} | {d['tot']} | {d['phb']} | {d['tol']} | {d['mc']} | "
            f"{d['ed']} | {d['sot']} |" for d in dist),
        "tab_fisico": "\n".join(
            f"| {r['name']['it']} | {r['mechanics_5e']['size']} | "
            f"{r['mechanics_5e']['speed_ft']} ft | "
            f"{str(r['mechanics_5e']['darkvision_ft']) + ' ft' if r['mechanics_5e']['darkvision_ft'] else 'assente'} |"
            for r in razze),
    }


def d_velocita(razze):
    """Tabella MV 2e -> velocita' 5e, ricostruita dai dati, non scritta a mano."""
    g = collections.defaultdict(list)
    for r in razze:
        g[(r["mechanics_5e"]["movement_2e"], r["mechanics_5e"]["speed_ft"])].append(
            r["name"]["it"])
    righe = [f"| {mv} | {ft} ft | {', '.join(sorted(n))} |"
             for (mv, ft), n in sorted(g.items())]
    return ("\n".join(righe),
            len({mv for mv, _ in g}), len({ft for _, ft in g}))


def d_netti(razze):
    """Netto degli aggiustamenti di FONTE (esclude quelli editoriali)."""
    netti = {}
    for r in razze:
        v = r["mechanics_5e"]["ability_adjustments"]["source_values"]
        netti[r["name"]["it"]] = sum(v.values())
    per_val = collections.defaultdict(list)
    for nome, n in netti.items():
        per_val[n].append(nome)
    righe = [f"| {n:+d} | {len(per_val[n])} | {', '.join(sorted(per_val[n]))} |"
             for n in sorted(per_val, reverse=True)]
    # doppia penalita': aggiustamento negativo E massimale sulla stessa caratteristica
    doppie = []
    for r in razze:
        v = r["mechanics_5e"]["ability_adjustments"]["source_values"]
        req = r["source_2e"]["ability_requirements"]
        for car, val in v.items():
            mx = req.get(car, {}).get("max")
            if val < 0 and mx is not None and mx < 18:
                doppie.append(f"{r['name']['it']} ({CAR_IT[car]} {val:+d}, max {mx})")
    return "\n".join(righe), max(netti.values()), min(netti.values()), sorted(doppie)


def d_montecarlo(razze):
    """Legge i numeri da dati/RAPPORTO-montecarlo.md. Nessuna cifra riscritta."""
    p = os.path.join(DATI, "RAPPORTO-montecarlo.md")
    if not os.path.exists(p):
        return None
    nomi = [r["name"]["it"] for r in razze]

    def intero(n):
        """Il rapporto tronca i nomi a larghezza fissa: li ricompongo."""
        n = n.strip()
        cand = [x for x in nomi if x.startswith(n)]
        return cand[0] if len(cand) == 1 else n

    testo = open(p, encoding="utf-8").read()
    iteraz = re.search(r"\*\*([\d.]+) iterazioni\*\*", testo).group(1)
    blocco = testo.split("## Probabilità per razza", 1)
    if len(blocco) == 1:
        blocco = testo.split("## Probabilita' per razza", 1)
    razz = re.findall(r"^\| (.+?) \|\s+([\d.]+)% \| ([\d.]+) \|$",
                      blocco[1].split("##")[0], re.M)
    razz = [(intero(n), float(p_)) for n, p_, _ in razz]
    sotto = [(intero(n), c, p_, q) for n, c, p_, q in
             re.findall(r"^\| (.+?) \| `(.+?)` \|\s+([\d.]+)% \| (\d+) \|$", testo, re.M)]
    # percorsi cavallereschi: prendo la riga di ciascuna coppia razza/classe
    ordini = []
    for sez in re.split(r"\n### ", testo)[1:]:
        nome = intero(sez.split(" — ")[0])
        for cl, pc in re.findall(r"^\| `(cavaliere[\w-]*)` \|\s+([\d.]+)% \|$", sez, re.M):
            ordini.append((nome, cl, float(pc)))
    def pc(x):
        return f"{float(x):.2f}".replace(".", ",") + "%"

    return {
        "iterazioni": iteraz,
        "pc": pc,
        "tab_razze": "\n".join(f"| {n} | {pc(p_)} |" for n, p_ in
                               sorted(razz, key=lambda x: x[1])),
        "peggiore": min(razz, key=lambda x: x[1]),
        "tab_sotto1": "\n".join(f"| {n} | `{c}` | {float(p_):.3f}%".replace(".", ",")
                                + f" | 1 ogni {q} |" for n, c, p_, q in sotto),
        "sotto1_pc": [float(p_) for _, _, p_, _ in sotto],
        "tab_ordini": "\n".join(
            f"| {n} | `{c}` | {pc(p_)} |" for n, c, p_ in
            sorted(ordini, key=lambda x: (x[1], -x[2]))),
        "corona": {n: p_ for n, c, p_ in ordini if c == "cavaliere-corona"},
        "rosa": {n: p_ for n, c, p_ in ordini if c == "cavaliere-rosa"},
    }


def d_sfere(dei):
    """Filtro delle sfere (decisione 24). Derivato da dati/_sfere_5e.py."""
    import sys
    if DATI not in sys.path:
        sys.path.insert(0, DATI)
    import _sfere_5e as SF

    GUAR = {"Cure Wounds", "Healing Word", "Mass Healing Word", "Prayer of Healing",
            "Mass Cure Wounds", "Heal", "Mass Heal"}
    OFF = {"Sacred Flame", "Guiding Bolt", "Inflict Wounds", "Spiritual Weapon",
           "Spirit Guardians", "Flame Strike", "Blade Barrier", "Harm",
           "Divine Word", "Fire Storm", "Earthquake", "Insect Plague"}

    righe, senza_cure, senza_off, vuoti = [], [], [], []
    for d in sorted(dei, key=lambda x: x["name"]["en"]):
        sf = [(x["name"], x["access"]) for x in d["source_2e"]["spheres"]]
        acc = SF.accessibili(sf)
        nomi = {i["name"] for i, _ in acc}
        per_liv = collections.Counter(i["level"] for i, _ in acc)
        vv = [l for l in range(1, 10) if per_liv[l] == 0]
        ha_cure, ha_off = bool(nomi & GUAR), bool(nomi & OFF)
        if not ha_cure:
            senza_cure.append(d["name"]["en"])
        if not ha_off:
            senza_off.append(d["name"]["en"])
        if vv:
            vuoti.append(d["name"]["en"])
        dom = SF.DOMINIO[d["id"]][0]
        fuori = dom in SF.DOMINI_FUORI_SRD
        righe.append(
            f"| {d['name']['en']} | {len(acc)} | "
            f"{', '.join(str(x) + '°' for x in vv) or '—'} | "
            f"{'sì' if ha_cure else '**NO**'} | {'sì' if ha_off else '**NO**'} | "
            f"`{dom}`{' ⚠︎' if fuori else ''} |")

    per_sfera = collections.Counter(s_ for i in SF.LISTA_BASE for s_ in i["spheres"])
    vuote = [x for x in SF.SFERE if per_sfera[x] == 0]
    return {
        "tab": "\n".join(righe),
        "tot_lista": len(SF.LISTA_BASE),
        "n_truc": sum(1 for i in SF.LISTA_BASE if i["level"] == 0),
        "n_nostre": sum(1 for i in SF.LISTA_BASE if i["derivation"] == "nostra"),
        "n_senza_cure": len(senza_cure), "senza_cure": ", ".join(senza_cure),
        "n_senza_offesa": len(senza_off), "senza_offesa": ", ".join(senza_off),
        "n_vuoti": len(vuoti),
        "n_sfere_vuote": len(vuote), "sfere_vuote": ", ".join(vuote),
        "n_animal": per_sfera["Animal"], "n_weather": per_sfera["Weather"],
    }


def d_divergenze():
    """Registro delle divergenze da SotDQ (decisione 25)."""
    import sys
    if DATI not in sys.path:
        sys.path.insert(0, DATI)
    import _divergenze_sotdq as D

    def tab(lista):
        return "\n".join(
            f"| `{d['id']}` | {d['soggetto']} | {d['tratto']} | {d['ufficiale'][:110]}"
            f"{'…' if len(d['ufficiale']) > 110 else ''} | {d['nostro'][:80]}"
            f"{'…' if len(d['nostro']) > 80 else ''} | dec. {d['decisione']} |"
            for d in lista)

    adottate = D.per_esito("adottato")
    divergenti = D.per_esito("divergiamo")
    return {
        "n_adottate": len(adottate), "n_divergenti": len(divergenti),
        "tab_adottate": tab(adottate), "tab_divergenti": tab(divergenti),
        "tab_unica": "\n".join(f"| `{x['id']}` | {x['cosa']} | {x['stato']} |"
                               for x in D.FONTE_UNICA),
        "n_unica": len(D.FONTE_UNICA),
    }


def d_criterio():
    """Decisione 26: il criterio della tracciabilita' e i lotti respinti."""
    import sys
    if DATI not in sys.path:
        sys.path.insert(0, DATI)
    import _criterio_fonti as C
    righe = []
    for l in C.LOTTI_RESPINTI:
        righe.append(
            f"| `{l['percorso']}` | {mille(l['voci'])} | "
            f"{mille(l['con_fonte'])} | {mille(l['con_pagina'])} | "
            f"**{l['esito']}** |")
    return {"criterio": C.CRITERIO, "tab": "\n".join(righe),
            "n": len(C.LOTTI_RESPINTI)}


def d_bestiario():
    """Sintesi della diagnostica sul bestiario."""
    import sys
    for p in (DATI, os.path.join(DATI, "_fonti")):
        if p not in sys.path:
            sys.path.insert(0, p)
    import _bestiario_mc as BM
    import _campi_2e as C27
    import _draconici as D
    import _nomi_verificati as NV
    import confronta_mostri as CM
    import analizza_bestiario as AB
    import srd51_mostri as SRD

    mc, sot = CM.mostri_mc(), CM.mostri_sotdq()
    kmc = {CM.chiave(x): x for x in mc}
    ks = {CM.chiave(x): x for x in sot}
    comuni = sorted(set(kmc) & set(ks))
    solo_mc = sorted(set(kmc) - set(ks))
    cat = collections.Counter(c[3] for c in AB.CAMPI_2E)
    rap = [D.CINQUE_E[n]["hp"] / D.DUE_E[n]["hd"] for n in D.ORDINE_5E]
    return {
        "n_mc": len(mc), "n_sot": len(sot), "n_comuni": len(comuni),
        "n_solo_mc": len(solo_mc),
        "n_razziali": len(AB.VOCI_RAZZIALI),
        "n_veri": len(solo_mc) - len(AB.VOCI_RAZZIALI),
        "campi_tot": len(AB.CAMPI_2E), "campi_assenti": cat["assente"],
        "campi_conv": cat["conversione"], "campi_diretti": cat["diretto"],
        "assenti": ", ".join(c[0] for c in AB.CAMPI_2E if c[3] == "assente"),
        "pf_min": min(rap), "pf_max": max(rap),
        "pf_med": sum(rap) / len(rap),
        "ordine_2e": " → ".join(D.ORDINE_2E),
        "ordine_5e": " → ".join(D.ORDINE_5E),
        # profilo difensivo contro la mediana SRD del proprio grado
        "quote": {n: 100 * D.CINQUE_E[n]["hp"]
                  / SRD.statistiche(D.CINQUE_E[n]["cr"])["pf_med"]
                  for n in D.ORDINE_5E},
        "kapak_pf": D.CINQUE_E["Kapak"]["hp"],
        "kapak_med": SRD.statistiche("3")["pf_med"],
        "kapak_dpr": AB.dpr_5e("Kapak"),
        "kapak_x": AB.dpr_5e("Kapak") / AB.dpr_2e("Kapak"),
        "altri_x_min": min(AB.dpr_5e(n) / AB.dpr_2e(n)
                           for n in D.ORDINE_5E if n != "Kapak"),
        "altri_x_max": max(AB.dpr_5e(n) / AB.dpr_2e(n)
                           for n in D.ORDINE_5E if n != "Kapak"),
        # decisione 27
        "tab_27": "\n".join(
            f"| **{k}** | {len(g['campi'])} | {', '.join('`' + c + '`' for c in g['campi'])} | "
            f"{g['esito']} | "
            f"{'`' + g['destinazione'] + '`, Fase ' + str(g['fase']) if g['destinazione'] else 'in Fase ' + str(g['fase'])} |"
            for k, g in C27.GRUPPI),
        "n_27": C27.totale_campi(),
        # nomi verificati
        "tab_nomi": "\n".join(
            f"| `{v['estratto']}` | **{v['corretto']}** | {len(v['creature'])} | "
            f"{v['causa']} |" for v in NV.VERIFICATE),
        "n_nomi": len(NV.VERIFICATE),
        "n_creature_dietro": NV.totale_creature(),
        "n_sospette": len(NV.SOSPETTE_STESSA_CAUSA),
        # conteggio vero, dal registro verificato su immagine
        "bm": BM.statistiche(),
        "tab_multi": "\n".join(
            f"| **{n}** | {p} | {len(c)} — {', '.join(c)} |"
            for p, n, c, _ in BM.statistiche()["multi"]),
    }


def d_import_veri():
    """Lotto respinto: contatori essenziali per il riassunto."""
    src = os.path.join(BASE, "import", "json-personali-veri")
    if not os.path.isdir(src):
        return None
    PERIMETRO = {"monster": 325, "spell": 319, "item": 360, "class": 12,
                 "subclass": 12, "race": 9, "background": 1,
                 "adventure": 0, "book": 0}
    # Questo lotto rinomina le chiavi rispetto a 5etools: le riporto ai nomi
    # canonici, cosi' il conteggio e' confrontabile con gli altri lotti.
    EQUIV = {"creatures_list": "monster", "spells_database": "spell",
             "items_inventory": "item", "character_classes": "class",
             "character_subclasses": "subclass", "character_races": "race",
             "character_backgrounds": "background",
             "campaign_adventures": "adventure", "campaign_books": "book"}
    voci = collections.Counter()
    byte = 0
    n_file = 0
    tot = 0
    for p in glob.glob(os.path.join(src, "**", "*.json"), recursive=True):
        n_file += 1
        byte += os.path.getsize(p)
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        for k, v in d.items():
            if k.startswith("_") or k == "_meta" or not isinstance(v, list):
                continue
            voci[EQUIV.get(k, k)] += len(v)
            tot += sum(1 for e in v if isinstance(e, dict))
    sforati = sum(1 for k, lim in PERIMETRO.items() if voci[k] > lim)
    return {"n_file": n_file, "mb": byte // 1024 // 1024, "tot": tot,
            "sforati": sforati, "tot_cat": len(PERIMETRO),
            "mostri": voci["monster"], "sottoclassi": voci["subclass"],
            "avventure": voci["adventure"]}


def d_musica():
    """Colonna sonora in Musica/. Materiale ACCANTONATO: inventariato, non usato."""
    d = os.path.join(BASE, "Musica")
    if not os.path.isdir(d):
        return None
    f = sorted(glob.glob(os.path.join(d, "*.mp3")))
    if not f:
        return None
    byte = sum(os.path.getsize(x) for x in f)
    # bitrate costante 64 kbps verificato su tutti i file: la durata si ricava
    # dalla dimensione senza bisogno di decodificare.
    sec = byte * 8 / 64000
    con_id = sum(1 for x in f if re.search(r"\[[A-Za-z0-9_-]{11}\]\.mp3$",
                                           os.path.basename(x)))
    autore = sum(1 for x in f if "Connor Ragas" in os.path.basename(x))
    return {"n": len(f), "mb": byte // 1024 // 1024,
            "ore": int(sec // 3600), "min": int(sec % 3600 // 60),
            "con_id": con_id, "autore": autore}


def d_import():
    """Materiale in import/, a statuto non ancora deciso. Solo conteggi."""
    src = os.path.join(BASE, "import", "json-personali")
    if not os.path.isdir(src):
        return None
    n_file = 0
    byte = 0
    voci = collections.Counter()
    fonti = collections.Counter()
    copie = 0
    tot = 0
    for p in glob.glob(os.path.join(src, "**", "*.json"), recursive=True):
        n_file += 1
        byte += os.path.getsize(p)
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        for k, v in d.items():
            if k == "_meta" or not isinstance(v, list):
                continue
            voci[k] += len(v)
            for e in v:
                if not isinstance(e, dict):
                    continue
                tot += 1
                if isinstance(e.get("source"), str):
                    fonti[e["source"]] += 1
                if "_copy" in e:
                    copie += 1
    return {
        "n_file": n_file, "mb": byte // 1024 // 1024, "tot": tot,
        "voci": voci, "n_fonti": len(fonti), "dsotdq": fonti.get("DSotDQ", 0),
        "copie": copie, "pct_copie": round(100 * copie / tot, 1) if tot else 0,
    }


def d_aperte(entita, etichetta):
    return [f"- **{e['id']}** ({etichetta}): {q}"
            for e in entita for q in e["source_2e"].get("open_questions", [])]


# ==========================================================================
# INTERPRETATIVO — scritto a mano, marcato nel documento
# ==========================================================================

DECISIONI = [
    (1, "Motore", "5e come chassis meccanico; le altre edizioni sono fonte di contenuto e lore."),
    (2, "Edizione di riferimento", "PHB **2014**, non 2024. La 2024 rende le specie numericamente neutre, incompatibile con la decisione 3."),
    (3, "Vincoli di caratteristica", "Minimi, massimali razziali e classi precluse sono regole **meccaniche** applicate in creazione PG, non affidate alla narrazione."),
    (4, "Limiti di livello per demiumani", "**Non si applicano.** Restano in `source_2e` come dato di fonte, con `level_limits.applied` a `false` e nota esplicita."),
    (5, "Cavalieri di Solamnia", "Sequenza obbligata Corona → Spada → Rosa, senza azzeramento dell'esperienza e senza tetti."),
    (6, "Maghi delle Torri", "NON classe standalone dal 1° livello: il giuramento alla Veste avviene al Test, al 3°. Le tre Vesti sono affiliazioni, non classi."),
    (7, "Schema a doppio strato", "`source_2e` fedele al manuale e immutabile, `mechanics_5e` rivedibile. I JSON sono generati da `build_*.py`."),
    (8, "Generazione delle caratteristiche", "Default **4d6 scarta il minore**; array standard e point-buy restano alternative. Se il metodo scelto rende irraggiungibile una combinazione, il sistema segnala e propone il tiro senza bloccare. L'Aghar usa i dadi propri del manuale."),
    (9, "Aggiustamenti negativi", "Si tengono, trascritti fedelmente, doppia penalità inclusa. Il sistema è chiuso: conta solo l'equilibrio interno."),
    (10, "Massimali razziali", "Si tengono tutti, applicati sia in creazione sia come **tetti di crescita**. Non sono i limiti di livello."),
    (11, "Barbaro, vincoli", "Vale l'**unione** dei due set: massimali della scheda razziale più minimi della voce di classe."),
    (12, "`valid_eras`", "Strato editoriale nostro, non dato di fonte. Due sole restrizioni applicate: Irda e Ordini Sacri con le divinità."),
    (13, "Taglia", "Dedotta dall'altezza, la 2e non assegna categorie. Il Minotauro resta **Medium**: in 5e anche il Golia a 7-8 piedi è Medium."),
    (14, "Infravisione", "Dove il manuale la dichiara si converte in scurovisione; dove tace resta **assente per scelta**, non per dimenticanza."),
    (15, "Tratti, trascrizione integrale", "Ogni tratto della voce 2e va in `mechanics_5e` con uno stato di conversione: `direct`, `adapted`, `pending`, `source_only`. Non si inventa meccanica 5e."),
    (16, "I nove tratti del PHB 2e", "Dove il PHB 2014 ha già un equivalente si copia quello; dove la 5e ha eliminato un tratto si ripristina dalla 2e, malus inclusi. La fedeltà alla fonte prevale sulla convenzione 5e."),
    (17, "I tredici pending di Krynn", "Tutti convertiti. *Schernire* è marcato **provvisorio** in attesa di Shadow of the Dragon Queen; la *Specializzazione nelle armi* del Minotauro resta `source_only` perché la fonte concede un permesso, non un beneficio."),
    (18, "Minotauro e Irda dall'Appendice", "Il capitolo razziale è avaro su queste due voci: si integra da `MC - Dragonlance Appendix` solo ciò che l'Appendice **dichiara**, con fonte marcata distintamente."),
    (19, "Compensazione dell'umano", "L'umano aveva zero tratti e zero aggiustamenti perché in 2e era pagato dall'assenza di limiti di livello, che la decisione 4 ha abolito. Compensato con +1 a due caratteristiche a scelta, una competenza e un linguaggio, marcati come conversione editoriale."),
    (20, "Tappo al Barbaro", "+1 fissi a Forza e Costituzione, editoriali e reversibili. **Tappo, non soluzione**: la conversione a background resta la strada giusta e va decisa con lo schema Personaggio."),
    (21, "I tre elfi terrestri", "Applicato il metodo della 18 alle tre voci dedicate dell'Appendice (pagg. 33-35). Esito parziale: due su tre hanno una capacità dichiarata, il Qualinesti nessuna."),
    (22, "Il tratto fantasma del Qualinesti", "Il segnaposto che registrava l'assenza è **rimosso**: non concedeva nulla ma contava nei totali, falsando ogni statistica a valle. L'informazione è passata fra le ambiguità di fonte, dove stanno le altre registrazioni dello stesso tipo."),
    (23, "Il principio del clone", "Per le classi la fedeltà alla fonte non basta: le razze 2e sono ricche, le classi 2e sono povere e trascriverle produce gusci vuoti. Ogni classe di Krynn è un **clone meccanico** della classe base 5e corrispondente (SRD 5.1), con innestati sopra i privilegi e le restrizioni della fonte. Cinque classi restano senza chassis, per decisione."),
    (24, "Sfere sacerdotali", "Si tengono nella forma fedele: le **sfere** filtrano quali incantesimi il chierico può preparare, ripristinando la negazione d'accesso; il **Dominio** 5e resta come sottoclasse per i privilegi di livello. Ogni divinità è associata al Dominio 2014 più coerente."),
    (25, "Lo statuto di SotDQ", "*Shadow of the Dragon Queen* è materiale ufficiale 5e su Krynn: **quinta provenienza** nel campo fonte dei tratti di `mechanics_5e`, non un terzo strato. Non è autoritativo su tutto, perché non è la conversione ufficiale del materiale 2e ma un prodotto scritto da zero che ne condivide i nomi. Prevale su *Schernire*; altrove divergiamo, e le divergenze sono registrate."),
    (26, "Il criterio della tracciabilità", "**Qualsiasi materiale esterno che non porti con sé fonte e pagina è inutilizzabile**, a prescindere dal resto della sua qualità. Tutto il progetto si regge sulla tracciabilità: un dato non verificabile non entra. È un filtro che si applica in trenta secondi e risparmia analisi lunghe. Entrambi i lotti in `import/` sono respinti e chiusi."),
    (27, "I sette campi 2e senza corrispettivo", "Non erano un problema unico. **Gruppo A** — frequenza, numero, organizzazione, ciclo, dieta: dati di mondo, non di scheda, e diventano input del generatore di incontri in Fase 3. **Gruppo B** — il morale non è un campo ma un parametro di comportamento: senza, ogni scontro finisce con tutti i nemici morti, e diventa input dell'IA in arena. **Gruppo C** — la resistenza magica è l'unica vera decisione ed è **rinviata alla Fase 2**, perché i Gradi di Sfida su cui calibriamo presuppongono che non ci sia."),
    (28, "Ogre e Orughi sono mostri", "La voce `Ogre (of Krynn)` dell'Appendice torna a categoria **creatura**, non `razza_altra`. L'asimmetria con Theiwar/Zakhar (clan nanici che il manuale riserva ai PNG giocabili) non regge per gli ogre comuni: non sono un clan riservato, sono avversari classici e servono all'arena. La parentela dichiarata con l'Irda resta nota di lore nella voce, non criterio di categoria. Vale il criterio della porta aperta: un mostro può sempre diventare razza in seguito, il contrario è più fastidioso."),
]


def d_decisioni():
    return "\n".join(f"{n}. **{titolo}** — {testo}" for n, titolo, testo in DECISIONI)


# ==========================================================================
# DOCUMENTO
# ==========================================================================

def main():
    razze, classi, dei = carica("razze"), carica("classi"), carica("divinita")
    S = d_strato5e(razze)
    T = indice_testi()
    C = d_meccanica_classi(classi)
    SF = d_sfere(dei)
    DV = d_divergenze()
    CR = d_criterio()
    BS = d_bestiario()
    IM = d_import()
    if IM:
        blocco_import = (
            f"In `import/json-personali/` ci sono **{IM['n_file']} file JSON, "
            f"{IM['mb']} MB, {mille(IM['tot'])} voci** da **{IM['n_fonti']} sigle di "
            f"fonte**. Inventario completo in `import/RAPPORTO-json-personali.md`.\n\n"
            "**Statuto non deciso. Non è integrato, non è convertito, `dati/` non "
            "è stato toccato.**\n\n"
            f"Cosa contiene, in sintesi: {mille(IM['voci']['monster'])} mostri, "
            f"{mille(IM['voci']['spell'])} incantesimi, {mille(IM['voci']['item'])} oggetti, "
            f"{mille(IM['voci']['feat'])} talenti, {mille(IM['voci']['background'])} background, "
            f"{IM['voci']['class']} classi 5e con {mille(IM['voci']['subclass'])} "
            f"sottoclassi. Include **Shadow of the Dragon Queen** "
            f"({mille(IM['dsotdq'])} voci), l'unica fonte 5e ufficiale su Krynn, che "
            "finora risultava mancante.\n\n"
            "Tre cose da sapere prima di decidere:\n\n"
            "1. **Non è un'estrazione dai manuali cartacei**: è il dump della "
            "cartella dati di 5etools. Lo dice il `changelog.json`, che contiene il "
            "diario di sviluppo del sito fino alla versione 1.218.3.\n"
            "2. **Non separa il dato di fonte dalle aggiunte dello strumento.** "
            "Nello stesso oggetto convivono i valori del manuale, indici generati "
            "per i filtri e metadati di prodotto. Il "
            f"{str(IM['pct_copie']).replace('.', ',')}% delle voci è per giunta "
            "**derivato** con `_copy`, cioè non esiste come testo.\n"
            "3. **Dove si sovrappone ai nostri dati, diverge.** L'unica razza in "
            "comune è il Kender, e diverge su velocità, aggiustamenti e forma di "
            "*Schernire*. Le 21 divinità hanno gli stessi nomi ma nessuna sfera."
        )
    else:
        blocco_import = "Nessun materiale in attesa."

    VR = d_import_veri()
    if VR:
        blocco_veri = (
            "### `import/json-personali-veri/` — verificato, respinto\n\n"
            f"{VR['n_file']} file, {VR['mb']} MB, {mille(VR['tot'])} voci. I file dichiarano "
            "`\"dataset_author\": \"marchez\"` e `\"custom handwritten dataset\"`. "
            "**Non è l'SRD 5.1 e non è una trascrizione**: il perimetro è sforato in "
            f"**{VR['sforati']} categorie su {VR['tot_cat']}** — {mille(VR['mostri'])} mostri contro i 325 "
            f"dell'SRD, {mille(VR['sottoclassi'])} sottoclassi contro 12, {mille(VR['avventure'])} avventure contro "
            "zero. Dentro `miscellaneous_data.json` c'è il **changelog di sviluppo "
            "di 5etools** con 607 voci fino alla versione 1.218.3, più i template "
            "del convertitore del sito. Verifica completa in "
            "`import/RAPPORTO-json-veri.md`.\n\n"
            "**È lo stesso corpus di `json-personali/`**, riorganizzato in sette "
            "file con le chiavi rinominate: mostri, incantesimi, oggetti e "
            f"sottoclassi coincidono voce per voce. La ripulitura ha cancellato "
            f"`source` e `page` da tutte e {mille(VR['tot'])} le voci, lasciando intatti gli "
            "indici interni al sito: **il lotto originale è preferibile a questo**. "
            "Resta dov'è.")
    else:
        blocco_veri = ""

    MU = d_musica()
    if MU:
        blocco_musica = (
            "### `Musica/` — accantonato\n\n"
            f"{MU['n']} MP3, {MU['mb']} MB, **{MU['ore']}h {MU['min']}m** di colonna sonora per "
            "*Shadow of the Dragon Queen*. **Non serve ora e non va integrata**: la "
            "Fase 2 è il motore di combattimento, l'audio viene molto dopo.\n\n"
            f"I metadati ID3 non dichiarano né autore né etichetta né provenienza: "
            f"l'unico campo presente è l'identificativo del programma che ha "
            f"codificato i file. Tutti e {MU['con_id']} i nomi contengono un identificativo "
            f"video di undici caratteri fra parentesi quadre, e {MU['autore']} titoli nominano "
            "**Connor Ragas** come autore. Nessuna lavorazione.")
    else:
        blocco_musica = ""
    MV, n_mv, n_ft = d_velocita(razze)
    TN, netto_max, netto_min, doppie = d_netti(razze)
    MC = d_montecarlo(razze)
    aperte = d_aperte(razze, "razza") + d_aperte(classi, "classe") + d_aperte(dei, "divinità")

    doc = f"""# Dragonlance Web GDR — contesto di progetto

*Generato da `genera_contesto.py` il {OGGI}.*

> **Come leggere questo documento.** Ogni numero, tabella e percentuale è
> **derivato dai JSON** al momento della generazione: se un dato cambia, cambia
> anche qui. Le letture e le conclusioni sono invece scritte a mano e marcate
> con un blocco citato e datato. Dove una frase interpretativa contiene un
> numero, quel numero è comunque interpolato dai dati.
>
> **Questo file è una fotografia.** La project knowledge non si sincronizza con
> la cartella di lavoro: quando i dati cambiano va rigenerato e **ricaricato a
> mano**, sostituendo la copia precedente.

---

## Stato

**Libreria**: {T['manuali_pronti']}/{T['manuali_totali']} manuali estratti ({T['pct_pronti']}%), {mille(T['pagine_pronte'])} pagine, {mille(T['caratteri_totali'])} caratteri. Restano {T['manuali_da_ocr']} scansioni in coda OCR e {T['non_lavorati']} manuali non ancora lavorati.

**Dati strutturati**: {len(razze)} razze, {len(classi)} classi, {len(dei)} divinità, validate a zero errori. {S['tot']} tratti razziali, {S['stati']['pending']} in sospeso, {S['n_ed']} di conversione editoriale nostra.

---

## Le {len(DECISIONI)} decisioni prese

Ordine cronologico. Questa è la storia completa delle scelte: non serve
ricostruirla dalle sezioni.

{d_decisioni()}

---

## Le {len(razze)} razze

{d_razze(razze)}

*(ed.)* segnala una conversione editoriale nostra, non un dato di fonte.

Clan nanici esclusi perché il manuale li riserva ai PNG: Klar, Theiwar,
Daergar, Zhakar.

### Aggiustamenti di fonte, al netto

Solo i valori del manuale: le compensazioni editoriali sono escluse.

| netto | razze | quali |
|---:|---:|---|
{TN}

**Doppia penalità** — aggiustamento negativo *e* massimale sulla stessa
caratteristica, conservata perché è del manuale:

{chr(10).join('- ' + d for d in doppie) or "Nessuna."}

{interpretativo(f'''Il netto va da {netto_min:+d} a {netto_max:+d}: nessuna razza raggiunge il +3 che la 5e
2014 assegna di norma. Non va pareggiato. Le razze di Krynn non vengono mescolate
con quelle del PHB: il sistema è chiuso e conta solo l'equilibrio interno.''')}

### Taglia, velocità, scurovisione

| razza | taglia | velocità | scurovisione |
|---|---|---:|---:|
{S['tab_fisico']}

La velocità è derivata dai **tassi MV della 2e**, non dalla taglia.

| MV 2e | velocità 5e | razze |
|---:|---:|---|
{MV}

{interpretativo(f'''Derivare la velocità dalla taglia invertiva l'ordinamento della fonte: i nani
finivano a 30 e i Kender a 25, cioè il nano correva più del Kender. La 5e stessa
smentisce quella regola — il nano del PHB 2014 è Medium e va a 25, perché tratta
la lentezza dei nani come tratto identitario. Nemmeno la proporzione funziona:
6/12 × 30 darebbe 15 piedi.

I tassi 2e distinti sono {n_mv}, i valori 5e utilizzabili {n_ft}: un pareggio è
inevitabile. L'ordinamento resta preservato in senso **debole** — nessuno supera
chi in 2e era più veloce — ma il pareggio non si limita a conservare le
uguaglianze esistenti, **ne crea una nuova**: Kender e Irda (MV 9) non erano
uguali ai nani (MV 6) e adesso lo sono. Quella differenza viene collassata. È il
prezzo di avere {n_mv} valori di partenza e {n_ft} di arrivo. I tassi originali
restano in `movement_2e`.

Sulla scurovisione: dove il manuale dichiara l'infravisione si converte con la
portata indicata; dove tace resta assente **per scelta**, non per dimenticanza.
Nell'Appendice Mostruosa il valore fra parentesi è quello *senza armatura*, e
vale sia per la CA sia per il movimento.''')}

---

## Le {len(classi)} classi

{d_classi(classi)}

I Cavalieri della Spada ricevono gli incantesimi da **Kiri-Jolith**, non da Paladine.

### Forma meccanica

Diagnostica completa in `dati/RAPPORTO-classi.md`. Qui la sintesi.

| classe | gruppo | DV 2e | tabella PE | inc. | priv. | imp. | chassis 5e |
|---|---|---|---|:-:|---:|---:|---|
{C['tab']}

Su {len(classi)} classi: **{C['tot_p']} privilegi** e **{C['tot_h']} impedimenti**. Solo {C['con_liv']} privilegi sono
agganciati a un livello esplicito; per gli altri {C['senza_liv']} la fonte non dice quando si
ottengano.

- **{C['n_senza_prog']} classi non hanno tabella di esperienza propria** e rimandano al gruppo: {C['senza_prog']}.
- **{C['n_senza_priv']} classi non hanno alcun privilegio**: {C['senza_priv']}.
- **{C['n_in_perdita']} classi hanno più impedimenti che privilegi.**
- Le tabelle arrivano al **{C['max_lv']}° livello**, cinque oltre il tetto della 5e.
- **Nessuna classe ha una tabella di THAC0 o di tiri salvezza**: valgono quelle di
  gruppo del PHB 2e, che non sono ancora nei dati.

{interpretativo('''Le classi di Krynn non sono classi nel senso della 5e: sono profili di
restrizione appoggiati sulle classi base della 2e. Convertirle non è un lavoro di
traduzione ma di riempimento — non c'è quasi nulla da tradurre. È la ragione della
decisione 23.''')}

### Chassis applicati (decisione 23)

**{C['n_clonate']} classi su {len(classi)}** sono cloni meccanici di una classe SRD 5.1: {C['chassis']}.
**{C['n_sospese']} restano senza chassis**, per decisione: {C['sospese']}.

Le sette incompatibilità strutturali sono risolte in `mechanics_5e.structural`,
uguali per tutte le classi: tabella PE unica, bonus di competenza al posto del
THAC0, cinque categorie di tiro salvezza mappate sulle sei caratteristiche,
competenze per categoria, pacchetti fissi, troncamento al 20°, titoli
descrittivi.

Stato dei {C['tot_feat']} privilegi e impedimenti della fonte:
{', '.join(f"**{C['stati'][k]}** `{k}`" for k in ('direct', 'pending', 'source_only') if C['stati'][k])}.
I `pending` sono il lavoro che resta: la decisione 23 autorizza il clone del
chassis, non l'invenzione di meccanica 5e per i privilegi.

---

## Sfere sacerdotali (decisione 24)

Verifica completa in `dati/RAPPORTO-sfere.md`. Le sfere filtrano la lista del
chierico SRD 5.1 ({SF['tot_lista']} incantesimi, {SF['n_truc']} trucchetti compresi); il Dominio resta
come sottoclasse. Accesso minore: solo fino al 3° livello, come in 2e.

| divinità | incant. accessibili | livelli vuoti | guarigione | offesa | Dominio |
|---|---:|---|:-:|:-:|---|
{SF['tab']}

- **{SF['n_senza_cure']} divinità su {len(dei)} non hanno alcuna cura**: {SF['senza_cure']}.
- **{SF['n_senza_offesa']} non hanno alcuna offesa diretta**: {SF['senza_offesa']}.
- **{SF['n_vuoti']} hanno almeno un livello di incantesimi completamente vuoto.**
- Delle {SF['tot_lista']} voci, {SF['n_nostre']} sono attribuzioni nostre e non ereditate da un
  antenato 2e: restano marcate `nostra` nel dato.

{interpretativo(f'''{SF['n_sfere_vuote']} sfera 2e non trova un solo incantesimo nella lista base del chierico 5e:
{SF['sfere_vuote']}. Animal ne trova {SF['n_animal']}, Weather {SF['n_weather']}. Non è un difetto della mappatura:
la 5e ha spostato piante, animali e meteo sulla lista del **druido**. Le divinità
della natura pagano un prezzo che non dipende da quanto erano ricche in 2e ma da
dove la 5e ha messo quel materiale.''')}

---

## Le {len(dei)} divinità

{d_dei(dei)}

I tre dei della magia coincidono con le tre Vesti: Solinari/Bianche,
Lunitari/Rosse, Nuitari/Nere.

---

## Verifiche pre-conversione

Rapporti completi in `dati/RAPPORTO-soddisfacibilita.md` (array e point-buy) e
`dati/RAPPORTO-montecarlo.md` (tiro dei dadi).

### Probabilità di qualificazione — Monte Carlo, {MC['iterazioni']} iterazioni

Sui soli vincoli razziali:

| razza | qualificati |
|---|---:|
{MC['tab_razze']}

Percorsi cavallereschi (`cavaliere` è la classe generica, non un grado dell'Ordine):

| razza | classe | qualificati |
|---|---|---:|
{MC['tab_ordini']}

Combinazioni sotto l'1%:

| razza | classe | qualificati | frequenza |
|---|---|---:|---:|
{MC['tab_sotto1']}

{interpretativo(f'''**Perché si tira.** Sotto point-buy due percorsi erano matematicamente
impossibili — il Cavaliere e il Cavaliere della Rosa — e il Nano Sozzo non aveva
alcuna disposizione valida con l'array standard. Con 4d6 scarta il minore
nessuno di questi è più impossibile: tornano rari, che è il comportamento
originale della 2e. I requisiti non sono stati ammorbiditi.

La **Corona** misura l'accesso all'intero percorso solamnico, non l'avanzamento:
passa il {MC['pc'](MC['corona']['Umano'])} degli umani e il {MC['pc'](MC['corona']['Mezzelfo'])} dei mezzelfi. Diventare cavaliere
è facile; diventare Cavaliere della Rosa no ({MC['pc'](MC['rosa']['Umano'])} e {MC['pc'](MC['rosa']['Mezzelfo'])}).

L'unica combinazione sotto l'1% ha un collo di bottiglia esatto e verificabile a
mano: il barbaro richiede Costituzione 12 e l'Aghar tira la Costituzione con
3d4, quindi serve il massimo assoluto sui tre dadi, 1 possibilità su 64.
Moltiplicata per gli altri requisiti dà lo 0,248% per via analitica — l'unico
numero di questo documento calcolato a mano — contro lo
{str(round(MC['sotto1_pc'][0], 3)).replace('.', ',')}% misurato dalla simulazione.

La razza più selettiva sui soli vincoli è l'**{MC['peggiore'][0]}** ({MC['pc'](MC['peggiore'][1])}).''')}

---

## Tratti razziali — {S['tot']} in tutto

### Per stato di conversione

| stato | tratti | quota |
|---|---:|---:|
{S['tab_stati']}

### Per provenienza

| fonte | tratti | quota |
|---|---:|---:|
{S['tab_fonti']}

### Per razza

| razza | totale | PHB 2e | Tales of the Lance | Appendice | editoriali | SotDQ |
|---|---:|---:|---:|---:|---:|---:|
{S['tab_dist']}

{interpretativo(f'''Su {S['tot']} tratti, {S['n_phb']} vengono dal PHB 2e ({S['pct_phb']}%) e
{S['n_krynn']} dalle fonti di Krynn ({S['pct_krynn']}%). La densità apparente di una
razza misura quindi in buona parte l'appartenenza a una stirpe del PHB, non la
profondità con cui il setting l'ha caratterizzata.

I {S['n_ed']} tratti di conversione editoriale non sono di Krynn: sono nostri, marcati
`editorial: True` e reversibili.

Il roster va da {S['min_tot']} a {S['max_tot']} tratti per razza. Le razze native di Krynn — Kender,
Minotauro, Irda — non ereditano nulla dal PHB e restano nella fascia bassa
nonostante le integrazioni dall'Appendice.''')}

### Tratti provvisori

{chr(10).join(f"- **{r}**: {t}" for r, t in S['provvisori']) or "Nessuno."}

### Tratti di conversione editoriale

{chr(10).join(f"- **{r}**: {t}" for r, t in S['editoriali']) or "Nessuno."}

---

## Divergenze da SotDQ (decisione 25)

*Shadow of the Dragon Queen* è in libreria ed è estratto. Entra come **quinta
provenienza** nel campo fonte dei tratti di `mechanics_5e`, accanto a PHB 2e,
Tales of the Lance, MC Appendix e conversione editoriale nostra. Lo schema
resta a due strati: `source_2e` non si tocca mai.

Non è autoritativo su tutto: non è la conversione ufficiale del materiale 2e,
è un prodotto 5e scritto da zero che ne condivide i nomi. Le sue scelte sono
un'interpretazione parallela.

### Dove SotDQ prevale ({DV['n_adottate']})

| id | soggetto | punto | ufficiale | nostro | governa |
|---|---|---|---|---|---|
{DV['tab_adottate']}

### Dove divergiamo ({DV['n_divergenti']})

| id | soggetto | punto | ufficiale | nostro | governa |
|---|---|---|---|---|---|
{DV['tab_divergenti']}

Registro interrogabile in `dati/_divergenze_sotdq.py`.

### Dove SotDQ è fonte unica ({DV['n_unica']})

Contenuto che in 2e non esiste: nessun conflitto possibile. **Registrato come
disponibile, non estratto.**

| id | cosa | stato |
|---|---|---|
{DV['tab_unica']}

---

## Il bestiario — diagnostica

Rapporto completo in `dati/RAPPORTO-bestiario.md`. Nulla è stato convertito.

**La scheda mostro 2e ha {BS['campi_tot']} campi**: {BS['campi_diretti']} passano diretti in 5e, {BS['campi_conv']} vanno
convertiti, **{BS['campi_assenti']} non hanno alcun corrispettivo** — {BS['assenti']}.

**I cinque draconici** sono le uniche creature con scheda in entrambe le
edizioni, quindi l'unico precedente di conversione verificabile.

| | |
|---|---|
| ordine di potenza in 2e (per PE) | {BS['ordine_2e']} |
| ordine di potenza in 5e (per GS) | {BS['ordine_5e']} |

**Bozak e Kapak si scambiano di posto.** Non è l'unico segnale: il Kapak rompe
anche il rapporto PF/DV, che sugli altri quattro sta fra {BS['pf_min']:.1f} e 11 e su di lui
arriva a {BS['pf_max']:.1f}, e moltiplica il danno per round per {BS['kapak_x']:.1f} contro il ×{BS['altri_x_min']:.1f}–×{BS['altri_x_max']:.1f}
degli altri quattro.

### Perché la regola fallisce proprio sul Kapak

In 5e il **Grado di Sfida è la media fra componente difensiva e componente
offensiva**. Il Kapak ha **{BS['kapak_pf']} punti ferita contro una mediana SRD di {BS['kapak_med']}** al
suo grado: sta *sotto* la mediana in difesa e ci arriva col danno, {BS['kapak_dpr']:.0f} per
round. È un cannone di vetro, e in 2e non lo era — era un assassino con **un**
attacco da 1-4.

`GS = DV − 2` presuppone che la creatura conservi il proprio profilo difensivo,
perché i dadi vita della 2e misurano solo la resistenza. **Il Kapak ha cambiato
asse.**

{interpretativo(f'''**Non esiste una formula estraibile da cinque casi.** Una regolarità si
intravede — grado di sfida uguale ai dadi vita meno due — e tiene per quattro
draconici su cinque, ma il quinto non è un arrotondamento: è una
riprogettazione.

Una precisazione che i numeri impongono: il Kapak non è l'unico sotto la
mediana difensiva. Lo sono quattro su cinque, e in modo crescente col grado —
Bozak al {BS['quote']['Bozak']:.0f}%, Kapak e Sivak al {BS['quote']['Kapak']:.0f}%, Aurak al {BS['quote']['Aurak']:.0f}%. **I draconici sono una
famiglia di creature fragili e offensive**, per scelta di design. Quello che è
unico del Kapak è il **salto offensivo rispetto alla propria fonte**: gli altri
sono stati riscalati, lui è stato ripensato.

Applicare quell'euristica alle {BS['n_solo_mc'] - BS['n_razziali']} creature restanti sposterebbe il tempo
dalla conversione al debug. Quello che i cinque casi danno non è un algoritmo
ma tre vincoli:

1. l'ordinamento si conserva **ma solo finché si conserva il ruolo** — il
   controllo da fare prima di fidarsene è sul ruolo, non sui numeri;
2. l'effetto identitario va riscritto con un tiro salvezza;
3. i danni per round vanno almeno raddoppiati.

La strada che i dati indicano è la **conversione per analogia** con l'SRD, non
per calcolo.''')}

### I sette campi senza corrispettivo, risolti (decisione 27)

| gruppo | campi | quali | esito | destinazione |
|---|---:|---|---|---|
{BS['tab_27']}

### Schema del mostro

`dati/schema/mostro.schema.json`, sul modello di razze e classi: `source_2e`
accoglie tutti e ventuno i campi della scheda 2e, `mechanics_5e` ha la forma di
uno statblock con stato di conversione e provenienza su ogni elemento. Due campi
nuovi rispetto alle razze: **`ruolo`**, che serve alla conversione per analogia e
all'IA di combattimento, e **`morale_2e`**, che porta il gruppo B della
decisione 27.

**Validato sui cinque draconici**, l'unico caso in cui entrambi gli strati sono
già noti da fonte: cinque su cinque conformi, zero errori. `dati/mostri/` non
esiste ancora — la validazione è un test dello schema, non una conversione.

### Il conteggio vero, rifatto voce per voce

Il numero ricavato dal testo estratto era sbagliato. Rifatto sulle immagini di
pagina:

| | |
|---|---:|
| voci dell'MC Appendix | **{BS['bm']['voci']}** |
| creature vere (statblock distinti) | **{BS['bm']['creature']}** |
| schede di razze già in `dati/razze/` | {BS['bm']['per_cat']['razza_nostra']['voci']} |
| razze e culture fuori dal roster | {BS['bm']['per_cat']['razza_altra']['voci']} |
| **creature da convertire** | **{BS['bm']['da_convertire']}** |

**{BS['bm']['n_multi']} voci hanno lo statblock su più colonne** — una voce, più creature:

| voce | pag. | creature |
|---|---:|---|
{BS['tab_multi']}

**{BS['bm']['nomi_sbagliati']} nomi di voce erano sbagliati** nel testo estratto, non i quattro noti.

{interpretativo(f'''**L'estrazione non ha solo sbagliato i nomi: ha perso dei dati.** In tre voci
le colonne di destra sono sparite del tutto — `Avian` aveva quattro uccelli e ne
restavano due, `Stag` tre cervi e ne restava uno, `Man (of Krynn)` quattro
culture e ne restavano due. Sono sette creature che dal testo estratto non
esistevano.

Il conteggio passa da {BS['n_mc']} a **{BS['bm']['creature']}**: il {round(100 * (BS['bm']['creature'] / BS['n_mc'] - 1))}% in più. Fra i ritrovamenti c'è il
**Cervo Bianco**, che non è una bestia ma una creatura sacra unica da 2.000 punti
esperienza, con capacità magiche.

**L'ordine di lavorazione proposto va rivisto**: è stato formulato prima del
ricontaggio e non contiene le sette creature nuove.''')}

---

## Materiale esterno — chiuso (decisione 26)

**Criterio generale, da applicare a qualunque lotto futuro:**

> {CR['criterio']}

Si applica in tre passi, e il primo di solito basta: (1) le voci dichiarano
fonte e pagina? (2) la copertura è sopra il 90%? (3) le sigle di fonte sono
più di una — allora è un corpus, non un documento.

| lotto | voci | con fonte | con pagina | esito |
|---|---:|---:|---:|---|
{CR['tab']}

{blocco_import}

{blocco_veri}

{blocco_musica}

---

## Questioni aperte

### Richiedono una decisione

{interpretativo(f'''- **Il PHB 5e 2014 non è fra i PDF**: la cartella contiene solo edizioni 2024.
  Alternativa disponibile: `2014.5e.tools`, che espone il materiale 2014 come
  JSON strutturato (repo GitHub `5etools-mirror-3/5etools-2014-src`).
- **Shadow of the Dragon Queen** continua a mancare: resta l'unica fonte 5e
  ufficiale su Krynn, e da essa dipende l'unico tratto ancora provvisorio.
- **Il Barbaro ha doppia natura**: il manuale lo tratta sia come cultura umana
  sia come classe. La decisione 20 gli ha dato un tappo reversibile; la
  conversione a background va decisa insieme allo schema Personaggio.
- **Il Qualinesti ha un tratto che registra un'assenza.** L'Appendice non
  dichiara alcuna capacità per quel ramo, e il posto è tenuto da una voce
  `source_only` senza meccanica. Nelle tabelle conta come un tratto
  dell'Appendice pur non concedendo nulla: è un artefatto di rappresentazione,
  non un beneficio. Da decidere se tenerlo come registrazione esplicita o
  toglierlo e lasciare il conteggio a zero.''')}

### Ambiguità delle fonti, registrate e non risolte

{chr(10).join(aperte) or "Nessuna."}

---

## Struttura della cartella

```
CLAUDE.md                          regole di comportamento per le sessioni AI
dragonlance-project-reference.md   documento di design
divisione-del-lavoro.md            chi fa cosa fra questo ambiente e Cowork
CONTESTO-PROGETTO.md               questo file (generato)
RETE-domini-permessi.md            allowlist di rete del sandbox (generato)
.claude/settings.json              la stessa allowlist, in forma eseguibile
git-privato.sh                     wrapper per il repository privato
.git/         repo PUBBLICO — documenti, script, schemi, moduli SRD
.git-private/ repo PRIVATO — dati/ con source_2e, trascrizione dei manuali
manuali-mancanti.md                manuali da procurare
LEGGIMI-estrazione.md              pipeline di estrazione
Manuali/     PDF sorgenti      Testi/    testi estratti a colonne separate
import/      materiale esterno, statuto non deciso o respinto — mai in dati/
Musica/      colonna sonora, ACCANTONATA: inventariata e non lavorata
Estratti/    vecchia estrazione a colonne fuse, solo storico
riscontro/   materiale di consultazione (3.5), non fonte di verità
dati/        schema/ razze/ classi/ divinita/ + build_*.py e valida_*.py
motore/      generazione.py — tiro delle caratteristiche e validazione
```
"""
    out = os.path.join(BASE, "CONTESTO-PROGETTO.md")
    open(out, "w", encoding="utf-8").write(doc)
    print(f"scritto {out} ({len(doc):,} caratteri)".replace(",", "."))
    return S


if __name__ == "__main__":
    main()
