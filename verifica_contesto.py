#!/usr/bin/env python3
"""
Verifica che CONTESTO-PROGETTO.md non contraddica i dati.

PERCHE' ESISTE
    Per tre volte di fila il documento si e' desincronizzato: le tabelle
    venivano rigenerate, la prosa scritta a mano no. La terza volta non
    riguardava piu' un numero ma le conclusioni. Separare derivato e
    interpretativo in `genera_contesto.py` risolve la causa; questo script
    verifica che la separazione tenga.

COSA FA
    Rilegge il documento generato, ne estrae ogni affermazione quantitativa
    con espressioni regolari e la confronta con i JSON e con i rapporti.
    Ogni controllo che fallisce e' un'incoerenza vera, non un avviso.

ECCEZIONE UNICA, DICHIARATA
    0,248% — probabilita' analitica dell'Aghar barbaro, calcolata a mano e
    confrontata nel testo con il valore simulato. E' l'unico numero del
    documento che non viene dai dati, ed e' etichettato come tale.

Uso:  python3 genera_contesto.py && python3 verifica_contesto.py
"""

import collections
import glob
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATI = os.path.join(BASE, "dati")
ECCEZIONI = {"0,248"}

esiti = []


def chk(nome, atteso, trovato):
    esiti.append((nome, atteso, trovato, atteso == trovato))


def carica(sub):
    return [json.load(open(p, encoding="utf-8"))
            for p in sorted(glob.glob(os.path.join(DATI, sub, "*.json")))]


def main():
    doc = open(os.path.join(BASE, "CONTESTO-PROGETTO.md"), encoding="utf-8").read()
    razze, classi, dei = carica("razze"), carica("classi"), carica("divinita")
    nomi = [r["name"]["it"] for r in razze]
    tratti = [(r, t) for r in razze for t in r["mechanics_5e"]["traits"]]
    tot = len(tratti)

    # --- tratti: stato, provenienza, distribuzione -----------------------
    st = collections.Counter(t["conversion_status"] for _, t in tratti)
    phb = sum(1 for _, t in tratti if "PHB 2e" in t["source"])
    mc = sum(1 for _, t in tratti if t["source"].startswith("MC -"))
    ed = sum(1 for _, t in tratti if t.get("editorial"))
    tol = tot - phb - mc - ed

    for s in ("direct", "adapted", "pending", "source_only"):
        m = re.search(rf"\| `{s}` \| (\d+) \| (\d+)% \|", doc)
        chk(f"stato {s}", st[s], int(m.group(1)))
        chk(f"quota {s}", round(100 * st[s] / tot), int(m.group(2)))
    sot = sum(1 for _, t in tratti if t["source"].startswith("SotDQ"))
    tol -= sot
    for lab, val in [(r"PHB 2e \(per rimando\)", phb), ("Tales of the Lance", tol),
                     ("MC Dragonlance Appendix", mc),
                     ("conversione editoriale nostra", ed),
                     (r"SotDQ \(ufficiale 5e\)", sot)]:
        m = re.search(rf"\| {lab} \| (\d+) \| (\d+)% \|", doc)
        chk(f"fonte {lab}", val, int(m.group(1)))
        chk(f"quota {lab}", round(100 * val / tot), int(m.group(2)))
    chk("somma fonti", tot, phb + tol + mc + ed + sot)
    chk("somma stati", tot, sum(st.values()))

    righe = re.findall(r"^\| (.+?) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| "
                       r"(\d+) \|$", doc, re.M)
    chk("righe per-razza", len(razze), len(righe))
    chk("somma per-razza", tot, sum(int(x[1]) for x in righe))
    for nome, t, p, tl, m_, e, s_ in righe:
        chk(f"riga {nome} somma", int(t),
            int(p) + int(tl) + int(m_) + int(e) + int(s_))
        r = [x for x in razze if x["name"]["it"] == nome][0]
        chk(f"riga {nome} totale", len(r["mechanics_5e"]["traits"]), int(t))
        chk(f"riga {nome} SotDQ",
            sum(1 for y in r["mechanics_5e"]["traits"]
                if y["source"].startswith("SotDQ")), int(s_))

    # --- titoli ----------------------------------------------------------
    chk("titolo tratti", tot, int(re.search(r"Tratti razziali — (\d+)", doc).group(1)))
    chk("titolo razze", len(razze), int(re.search(r"## Le (\d+) razze", doc).group(1)))
    chk("titolo classi", len(classi), int(re.search(r"## Le (\d+) classi", doc).group(1)))
    chk("titolo divinità", len(dei), int(re.search(r"## Le (\d+) divinità", doc).group(1)))

    # --- prosa interpretativa: i numeri devono essere interpolati --------
    m = re.search(r"Su (\d+) tratti, (\d+) vengono dal PHB 2e \((\d+)%\) e\n"
                  r"> (\d+) dalle fonti di Krynn \((\d+)%\)", doc)
    chk("prosa totale", tot, int(m.group(1)))
    chk("prosa PHB", phb, int(m.group(2)))
    chk("prosa quota PHB", round(100 * phb / tot), int(m.group(3)))
    # SotDQ e' materiale di Krynn a tutti gli effetti: entra nel conteggio.
    chk("prosa Krynn", tol + mc + sot, int(m.group(4)))
    chk("prosa quota Krynn", round(100 * (tol + mc + sot) / tot), int(m.group(5)))
    chk("prosa editoriali", ed,
        int(re.search(r"> I (\d+) tratti di conversione editoriale", doc).group(1)))
    m = re.search(r"roster va da (\d+) a (\d+)", doc)
    lung = [len(r["mechanics_5e"]["traits"]) for r in razze]
    chk("roster minimo", min(lung), int(m.group(1)))
    chk("roster massimo", max(lung), int(m.group(2)))

    # --- aggiustamenti al netto ------------------------------------------
    netti = {r["name"]["it"]:
             sum(r["mechanics_5e"]["ability_adjustments"]["source_values"].values())
             for r in razze}
    per_val = collections.Counter(netti.values())
    for n, c in per_val.items():
        m = re.search(r"^\| " + re.escape(f"{n:+d}") + r" \| (\d+) \| (.+?) \|$",
                      doc, re.M)
        chk(f"netto {n:+d} conteggio", c, int(m.group(1)))
        chk(f"netto {n:+d} elenco",
            sorted(k for k, v in netti.items() if v == n),
            sorted(m.group(2).split(", ")))
    chk("somma netti", len(razze), sum(per_val.values()))
    m = re.search(r"Il netto va da ([+-]\d+) a ([+-]\d+)", doc)
    chk("netto minimo", min(netti.values()), int(m.group(1)))
    chk("netto massimo", max(netti.values()), int(m.group(2)))

    # --- velocita' --------------------------------------------------------
    g = collections.defaultdict(list)
    for r in razze:
        g[(r["mechanics_5e"]["movement_2e"],
           r["mechanics_5e"]["speed_ft"])].append(r["name"]["it"])
    mvr = re.findall(r"^\| (\d+) \| (\d+) ft \| (.+?) \|$", doc, re.M)
    chk("righe MV", len(g), len(mvr))
    for mv, ft, nn in mvr:
        chk(f"MV {mv}", sorted(g[(int(mv), int(ft))]), sorted(nn.split(", ")))
    m = re.search(r"I tassi 2e distinti sono (\d+), i valori 5e utilizzabili (\d+)", doc)
    chk("tassi MV distinti", len({k[0] for k in g}), int(m.group(1)))
    chk("velocità distinte", len({k[1] for k in g}), int(m.group(2)))
    chk("tabella fisica", [], [r["id"] for r in razze if
        f"| {r['name']['it']} | {r['mechanics_5e']['size']} | "
        f"{r['mechanics_5e']['speed_ft']} ft |" not in doc])

    # --- forma meccanica delle classi ------------------------------------
    def priv(c):
        return c["source_2e"].get("special_benefits") or []

    def imp(c):
        return c["source_2e"].get("special_hindrances") or []

    def prog(c):
        return c["source_2e"].get("progression") or []

    tot_p = sum(len(priv(c)) for c in classi)
    tot_h = sum(len(imp(c)) for c in classi)
    con_liv = sum(1 for c in classi for b in priv(c)
                  if re.search(r"\d+°\s*livello", b["text"]))
    m = re.search(r"Su \d+ classi: \*\*(\d+) privilegi\*\* e \*\*(\d+) impedimenti\*\*\. "
                  r"Solo (\d+) privilegi sono\nagganciati a un livello esplicito; per "
                  r"gli altri (\d+) ", doc)
    chk("privilegi totali", tot_p, int(m.group(1)))
    chk("impedimenti totali", tot_h, int(m.group(2)))
    chk("privilegi con livello", con_liv, int(m.group(3)))
    chk("privilegi senza livello", tot_p - con_liv, int(m.group(4)))
    chk("somma privilegi", tot_p, con_liv + (tot_p - con_liv))

    m = re.search(r"\*\*(\d+) classi non hanno tabella di esperienza propria\*\* e "
                  r"rimandano al gruppo: (.+?)\.\n", doc)
    sp = [c for c in classi if not prog(c)]
    chk("classi senza tabella PE", len(sp), int(m.group(1)))
    chk("elenco senza tabella PE", sorted(c["name"]["it"] for c in sp),
        sorted(m.group(2).split(", ")))
    m = re.search(r"\*\*(\d+) classi non hanno alcun privilegio\*\*: (.+?)\.\n", doc)
    spr = [c for c in classi if not priv(c)]
    chk("classi senza privilegi", len(spr), int(m.group(1)))
    chk("elenco senza privilegi", sorted(c["name"]["it"] for c in spr),
        sorted(m.group(2).split(", ")))
    chk("classi in perdita",
        len([c for c in classi if len(imp(c)) > len(priv(c))]),
        int(re.search(r"\*\*(\d+) classi hanno più impedimenti che privilegi", doc).group(1)))
    chk("livello massimo",
        max(p["level"] for c in classi for p in prog(c)),
        int(re.search(r"arrivano al \*\*(\d+)° livello\*\*", doc).group(1)))

    righe_cl = re.findall(r"^\| (.+?) \| (Warrior|Wizard|Priest|Rogue|Normal) \| "
                          r"(\S+) \| (propria, \d+ liv\.|del gruppo) \| (sì|—) \| "
                          r"(\d+) \| (\d+) \| (`\w+`|\*\*indeciso\*\*) \|$", doc, re.M)
    chk("righe tabella classi", len(classi), len(righe_cl))
    for nome, grp, dv, pe, inc, p, h, ch in righe_cl:
        c = [x for x in classi if x["name"]["it"] == nome][0]
        atteso = c["mechanics_5e"]["chassis"]["srd_class"]
        chk(f"classe {nome} chassis",
            f"`{atteso}`" if atteso else "**indeciso**", ch)
    for nome, grp, dv, pe, inc, p, h, _ in righe_cl:
        c = [x for x in classi if x["name"]["it"] == nome][0]
        chk(f"classe {nome} gruppo", c["group"], grp)
        chk(f"classe {nome} DV", c["source_2e"]["hit_die"] or "—", dv)
        chk(f"classe {nome} privilegi", len(priv(c)), int(p))
        chk(f"classe {nome} impedimenti", len(imp(c)), int(h))
        chk(f"classe {nome} incantesimi",
            "sì" if c["source_2e"].get("spell_progression") else "—", inc)
        chk(f"classe {nome} PE",
            f"propria, {len(prog(c))} liv." if prog(c) else "del gruppo", pe)
    chk("somma privilegi in tabella", tot_p, sum(int(r[5]) for r in righe_cl))
    chk("somma impedimenti in tabella", tot_h, sum(int(r[6]) for r in righe_cl))

    # --- decisione 23: chassis e stati dei privilegi ----------------------
    clonate = [c for c in classi if c["mechanics_5e"]["chassis"]["srd_class"]]
    m = re.search(r"\*\*(\d+) classi su (\d+)\*\* sono cloni meccanici di una classe "
                  r"SRD 5\.1: (.+?)\.\n\*\*(\d+) restano senza chassis\*\*, per "
                  r"decisione: (.+?)\.\n", doc)
    chk("classi clonate", len(clonate), int(m.group(1)))
    chk("classi totali (clone)", len(classi), int(m.group(2)))
    chk("classi in sospeso", len(classi) - len(clonate), int(m.group(4)))
    chk("elenco in sospeso",
        sorted(c["name"]["it"] for c in classi
               if not c["mechanics_5e"]["chassis"]["srd_class"]),
        sorted(m.group(5).split(", ")))
    conta = collections.Counter(c["mechanics_5e"]["chassis"]["srd_class"]
                                for c in clonate)
    chk("elenco chassis",
        ", ".join(f"{k} ×{v}" for k, v in sorted(conta.items())), m.group(3))
    chk("somma chassis", len(clonate), sum(conta.values()))

    stati_f = collections.Counter(f["conversion_status"] for c in classi
                                  for f in c["mechanics_5e"]["features"])
    chk("privilegi e impedimenti mappati", tot_p + tot_h, sum(stati_f.values()))
    m = re.search(r"Stato dei (\d+) privilegi e impedimenti della fonte:\n(.+?)\.\n",
                  doc)
    chk("totale feature", tot_p + tot_h, int(m.group(1)))
    for n_, k in re.findall(r"\*\*(\d+)\*\* `(\w+)`", m.group(2)):
        chk(f"feature {k}", stati_f[k], int(n_))

    # --- decisione 24: filtro delle sfere ---------------------------------
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_sfere_5e", os.path.join(DATI, "_sfere_5e.py"))
    SF = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(SF)

    m = re.search(r"chierico SRD 5\.1 \((\d+) incantesimi, (\d+) trucchetti", doc)
    chk("lista SRD", len(SF.LISTA_BASE), int(m.group(1)))
    chk("trucchetti", sum(1 for i in SF.LISTA_BASE if i["level"] == 0), int(m.group(2)))
    chk("attribuzioni nostre",
        sum(1 for i in SF.LISTA_BASE if i["derivation"] == "nostra"),
        int(re.search(r"voci, (\d+) sono attribuzioni nostre", doc).group(1)))

    GUAR = {"Cure Wounds", "Healing Word", "Mass Healing Word", "Prayer of Healing",
            "Mass Cure Wounds", "Heal", "Mass Heal"}
    OFF = {"Sacred Flame", "Guiding Bolt", "Inflict Wounds", "Spiritual Weapon",
           "Spirit Guardians", "Flame Strike", "Blade Barrier", "Harm",
           "Divine Word", "Fire Storm", "Earthquake", "Insect Plague"}
    righe_sf = re.findall(r"^\| ([A-Z][\w' -]+?) \| (\d+) \| ([^|]+?) \| (sì|\*\*NO\*\*) \| "
                          r"(sì|\*\*NO\*\*) \| `(\w+)`[^|]*\|$", doc, re.M)
    chk("righe tabella sfere", len(dei), len(righe_sf))
    for nome, n_, vuoti, cure, off, dom in righe_sf:
        d = [x for x in dei if x["name"]["en"] == nome][0]
        acc = SF.accessibili([(x["name"], x["access"])
                              for x in d["source_2e"]["spheres"]])
        inc = {i["name"] for i, _ in acc}
        chk(f"sfere {nome} totale", len(acc), int(n_))
        chk(f"sfere {nome} cure", "sì" if inc & GUAR else "**NO**", cure)
        chk(f"sfere {nome} offesa", "sì" if inc & OFF else "**NO**", off)
        chk(f"sfere {nome} dominio", SF.DOMINIO[d["id"]][0], dom)
        per_liv = collections.Counter(i["level"] for i, _ in acc)
        att = [f"{l}°" for l in range(1, 10) if per_liv[l] == 0] or ["—"]
        chk(f"sfere {nome} vuoti", att, [x.strip() for x in vuoti.split(",")])

    # --- Monte Carlo: ogni percentuale deve esistere nel rapporto --------
    rep = open(os.path.join(DATI, "RAPPORTO-montecarlo.md"), encoding="utf-8").read()
    sez = doc.split("## Verifiche pre-conversione")[1].split("\n---")[0]
    chk("percentuali MC tracciabili", [],
        [p for p in re.findall(r"(\d+,\d+)%", sez)
         if p not in ECCEZIONI and p.replace(",", ".") not in rep])
    rr = re.findall(r"^\| ([^|]+?) \| (\d+,\d+)% \|$", sez, re.M)
    chk("righe razza MC", len(razze), len(rr))
    chk("nomi razza integri", [], [n for n, _ in rr if n not in nomi])
    chk("nomi cavalieri integri", [], [
        n for n, _, _ in re.findall(r"^\| ([^|]+?) \| `(cavaliere[\w-]*)` \| (\d+,\d+)% \|$",
                                    sez, re.M) if n not in nomi])
    chk("iterazioni", re.search(r"\*\*([\d.]+) iterazioni\*\*", rep).group(1),
        re.search(r"Monte Carlo, ([\d.]+) iterazioni", doc).group(1))

    # --- libreria ---------------------------------------------------------
    idx = json.load(open(os.path.join(BASE, "Testi", "indice.json"), encoding="utf-8"))
    ri = idx["riepilogo"]
    ps = collections.Counter(x.get("stato") for x in idx["manuali"])
    m = re.search(r"\*\*Libreria\*\*: (\d+)/(\d+) manuali estratti \((\d+)%\), "
                  r"([\d.]+) pagine, ([\d.]+) caratteri\. Restano (\d+) scansioni "
                  r"in coda OCR e (\d+) manuali", doc)
    chk("manuali pronti", ri["manuali_pronti"], int(m.group(1)))
    chk("manuali totali", ri["manuali_totali"], int(m.group(2)))
    chk("quota pronti", round(100 * ri["manuali_pronti"] / ri["manuali_totali"]),
        int(m.group(3)))
    chk("pagine", ri["pagine_pronte"], int(m.group(4).replace(".", "")))
    chk("caratteri", ri["caratteri_totali"], int(m.group(5).replace(".", "")))
    chk("coda OCR", ri["manuali_da_ocr"], int(m.group(6)))
    chk("non lavorati", ps["non_lavorato"], int(m.group(7)))
    chk("somma stati manuali", ri["manuali_totali"], sum(ps.values()))

    # --- bestiario (decisione 26 e diagnostica) ---------------------------
    spec = importlib.util.spec_from_file_location(
        "_draconici", os.path.join(DATI, "_draconici.py"))
    DR = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(DR)

    m = re.search(r"\*\*La scheda mostro 2e ha (\d+) campi\*\*: (\d+) passano "
                  r"diretti in 5e, (\d+) vanno\nconvertiti, \*\*(\d+) non hanno "
                  r"alcun corrispettivo\*\*", doc)
    tot_c, dir_c, conv_c, ass_c = (int(m.group(i)) for i in range(1, 5))
    chk("campi scheda 2e", tot_c, dir_c + conv_c + ass_c)

    m = re.search(r"ordine di potenza in 2e \(per PE\) \| (.+?) \|", doc)
    chk("ordine 2e", " → ".join(DR.ORDINE_2E), m.group(1))
    m = re.search(r"ordine di potenza in 5e \(per GS\) \| (.+?) \|", doc)
    chk("ordine 5e", " → ".join(DR.ORDINE_5E), m.group(1))
    chk("i due ordini differiscono", True, DR.ORDINE_2E != DR.ORDINE_5E)

    rap = {n: DR.CINQUE_E[n]["hp"] / DR.DUE_E[n]["hd"] for n in DR.ORDINE_5E}
    m = re.search(r"sta fra (\d+[.,]\d+) e 11 e su di lui\narriva a (\d+[.,]\d+)",
                  doc)
    chk("PF/DV minimo", round(min(rap.values()), 1),
        float(m.group(1).replace(",", ".")))
    chk("PF/DV massimo", round(max(rap.values()), 1),
        float(m.group(2).replace(",", ".")))
    chk("il massimo e' il Kapak", "Kapak", max(rap, key=rap.get))


    # --- decisione 27: i sette campi senza corrispettivo ------------------
    spec = importlib.util.spec_from_file_location(
        "_campi_2e", os.path.join(DATI, "_campi_2e.py"))
    C27 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(C27)
    righe_27 = re.findall(r"^\| \*\*([ABC])\*\* \| (\d+) \| (.+?) \| (.+?) \| "
                          r"(.+?) \|$", doc, re.M)
    chk("gruppi decisione 27", len(C27.GRUPPI), len(righe_27))
    chk("campi decisione 27 in totale", C27.totale_campi(),
        sum(int(r[1]) for r in righe_27))
    chk("campi 27 = campi assenti", ass_c, sum(int(r[1]) for r in righe_27))
    for k, n_, quali, esito, dest in righe_27:
        g = dict(C27.GRUPPI)[k]
        chk(f"gruppo {k} campi", len(g["campi"]), int(n_))
        chk(f"gruppo {k} esito", g["esito"], esito)
        chk(f"gruppo {k} elenco",
            sorted(g["campi"]),
            sorted(x.strip(" `") for x in quali.split(",")))

    # --- nomi corrotti verificati ----------------------------------------
    spec = importlib.util.spec_from_file_location(
        "_nomi_verificati", os.path.join(DATI, "_nomi_verificati.py"))
    NV = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(NV)
    # --- conteggio vero del bestiario -------------------------------------
    spec = importlib.util.spec_from_file_location(
        "_bestiario_mc", os.path.join(DATI, "_bestiario_mc.py"))
    BM = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(BM)
    st = BM.statistiche()

    m = re.search(r"voci dell'MC Appendix \| \*\*(\d+)\*\*", doc)
    chk("voci MC", st["voci"], int(m.group(1)))
    m = re.search(r"creature vere \(statblock distinti\) \| \*\*(\d+)\*\*", doc)
    chk("creature MC", st["creature"], int(m.group(1)))
    m = re.search(r"\*\*creature da convertire\*\* \| \*\*(\d+)\*\*", doc)
    chk("creature da convertire", st["da_convertire"], int(m.group(1)))
    chk("somma per categoria", st["creature"],
        sum(v["creature"] for v in st["per_cat"].values()))
    m = re.search(r"\*\*(\d+) voci hanno lo statblock su più colonne\*\*", doc)
    chk("voci multi-colonna", st["n_multi"], int(m.group(1)))
    m = re.search(r"\*\*(\d+) nomi di voce erano sbagliati\*\*", doc)
    chk("nomi sbagliati", st["nomi_sbagliati"], int(m.group(1)))
    righe_multi = re.findall(r"^\| \*\*(.+?)\*\* \| (\d+) \| (\d+) — (.+?) \|$",
                             doc, re.M)
    chk("righe multi-colonna", st["n_multi"], len(righe_multi))
    for nome, pag, n_, elenco in righe_multi:
        v = [x for x in st["multi"] if x[1] == nome][0]
        chk(f"multi {nome} pagina", v[0], int(pag))
        chk(f"multi {nome} creature", len(v[2]), int(n_))
        chk(f"multi {nome} elenco", v[2], [x.strip() for x in elenco.split(",")])
    chk("somma creature multi-colonna",
        sum(len(x[2]) for x in st["multi"]),
        sum(int(r[2]) for r in righe_multi))

    # --- decisione 26: criterio della tracciabilita' ----------------------
    spec = importlib.util.spec_from_file_location(
        "_criterio_fonti", os.path.join(DATI, "_criterio_fonti.py"))
    CF = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(CF)
    righe_lotti = re.findall(r"^\| `(import/[^`]+)` \| ([\d.]+) \| ([\d.]+) \| "
                             r"([\d.]+) \| \*\*(\w+)\*\* \|$", doc, re.M)
    chk("lotti respinti", len(CF.LOTTI_RESPINTI), len(righe_lotti))
    for perc, voci, f_, p_, esito in righe_lotti:
        l = [x for x in CF.LOTTI_RESPINTI if x["percorso"] == perc][0]
        chk(f"lotto {perc} voci", l["voci"], int(voci.replace(".", "")))
        chk(f"lotto {perc} fonte", l["con_fonte"], int(f_.replace(".", "")))
        chk(f"lotto {perc} pagina", l["con_pagina"], int(p_.replace(".", "")))
        chk(f"lotto {perc} esito", l["esito"], esito)

    # --- decisioni: numerazione contigua ---------------------------------
    # solo dentro la sezione delle decisioni: altrove ci sono elenchi numerati
    sez_dec = doc.split("decisioni prese", 1)[1].split("\n---", 1)[0]
    dec = [int(x) for x in re.findall(r"^(\d+)\. \*\*", sez_dec, re.M)]
    chk("decisioni contigue", list(range(1, len(dec) + 1)), dec)
    chk("titolo decisioni", len(dec),
        int(re.search(r"## Le (\d+) decisioni", doc).group(1)))

    # --- ogni tratto marcato deve comparire negli elenchi ------------------
    for r, t in tratti:
        etichetta = f"**{r['name']['it']}**: {t['name']}"
        if t.get("provisional"):
            chk(f"provvisorio {t['name']}", True, etichetta in doc)
        if t.get("editorial"):
            chk(f"editoriale {t['name']}", True, etichetta in doc)

    # --- i blocchi interpretativi devono essere marcati -------------------
    chk("blocchi interpretativi marcati",
        doc.count("Lettura interpretativa"),
        doc.count("Non e' derivata dai dati"))

    ko = [e for e in esiti if not e[3]]
    print(f"{len(esiti)} controlli, {len(ko)} incoerenze")
    for nome, a, b, _ in ko:
        print(f"  KO  {nome}\n      atteso:  {a}\n      trovato: {b}")
    return 1 if ko else 0


if __name__ == "__main__":
    sys.exit(main())
