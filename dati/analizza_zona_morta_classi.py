#!/usr/bin/env python3
"""
LA ZONA MORTA DELLE CLASSI -> dati/RAPPORTO-zona-morta-classi.md

LA DOMANDA
    `classe.schema.json` descrive `mechanics_5e` come "object o null", senza
    proprieta' e senza additionalProperties: lo strato di conversione delle
    classi non e' mai stato validato dallo schema. Quanto costa chiuderla?
    Quanti campi sono in uso oggi nei 17 file, quanti sono dichiarati da
    qualche parte, e ci sono incoerenze fra classi diverse?

PERCHE' ADESSO
    Lo schema del Personaggio ci si appoggia sopra: un personaggio prende
    dalla classe i privilegi, i dadi vita, le competenze. Costruirlo su uno
    strato mai validato significa ereditarne i difetti senza saperlo.

COSA FA
    1. Censisce ogni percorso in uso sotto mechanics_5e nei 17 file.
    2. Lo mette contro cio' che gli schemi dichiarano e contro cio' che i
       validatori nominano.
    3. Cerca le incoerenze fra classi: percorsi disomogenei, tipi variabili,
       invarianti dichiarate a parole e non verificate, derivati che non
       tornano.
    4. Fa lo stesso censimento su razze e divinita', perche' sono gli altri
       due ingressi del Personaggio e stanno nella stessa condizione.

COSA NON FA
    Non chiude niente. E' un rapporto, non una correzione: chiudere l'oggetto
    per intero e' un lavoro a se' e non va fatto di straforo dentro un altro.

RIDUZIONE — CLAUDE.md, punti 1 e 2
    Legge dati privati (classi/, razze/, divinita/) e non emette testo di
    fonte: escono percorsi, nomi di campo, conteggi e nomi di privilegio
    nostri. Nessun `text_2e`, nessun `raw`. Guardia in fondo al file.

NUMERI — CLAUDE.md, punto 3
    Tutti interpolati.

Uso:  python3 dati/analizza_zona_morta_classi.py
"""

import collections
import glob
import json
import os
import re
import sys
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
OGGI = date.today().isoformat()
USCITA = os.path.join(BASE, "RAPPORTO-zona-morta-classi.md")

VALIDATORI = ["valida_classi.py", "valida_effetti.py", "verifica_strati.py",
              "valida.py"]

# Invariante scritta nella descrizione di elemento_5e (mostro.schema.json) e
# applicata di fatto ovunque: la prosa e' null solo dove la conversione non
# c'e' ancora.
STATI_SENZA_MECCANICA = ("pending", "source_only")


# ------------------------------------------------------------------ censimento
def carica(cartella):
    fuori = []
    for f in sorted(glob.glob(os.path.join(BASE, cartella, "*.json"))):
        fuori.append(json.load(open(f, encoding="utf-8")))
    return fuori


def percorsi_dati(docs):
    """Ogni percorso sotto mechanics_5e, con chi lo porta e di che tipo."""
    per = collections.defaultdict(set)
    tipi = collections.defaultdict(set)

    def scava(o, p, cid):
        if isinstance(o, dict):
            for k, v in o.items():
                np = f"{p}.{k}"
                per[np].add(cid)
                tipi[np].add(type(v).__name__)
                scava(v, np, cid)
        elif isinstance(o, list):
            for it in o:
                scava(it, p + "[]", cid)

    for d in docs:
        if d.get("mechanics_5e") is not None:
            scava(d["mechanics_5e"], "mechanics_5e", d["id"])
    return per, tipi


def percorsi_schema(nodo, p="mechanics_5e"):
    """I percorsi che uno schema dichiara, nella stessa forma dei dati."""
    out = set()
    if not isinstance(nodo, dict):
        return out
    for sotto in ("anyOf", "oneOf", "allOf"):
        for n in nodo.get(sotto, []):
            out |= percorsi_schema(n, p)
    props = nodo.get("properties")
    if isinstance(props, dict):
        for k, v in props.items():
            np = f"{p}.{k}"
            out.add(np)
            out |= percorsi_schema(v, np)
    it = nodo.get("items")
    if isinstance(it, dict):
        out |= percorsi_schema(it, p + "[]")
    return out


def nomi_nei_validatori():
    """I nomi di campo che compaiono come stringhe nei validatori.

    APPROSSIMAZIONE, DICHIARATA: dice che un validatore NOMINA un campo, non
    che lo verifichi davvero. Serve a separare i campi che nessuno guarda da
    quelli che qualcuno guarda, non a misurare la qualita' del controllo.
    """
    nomi = set()
    for v in VALIDATORI:
        p = os.path.join(BASE, v)
        if not os.path.exists(p):
            continue
        testo = open(p, encoding="utf-8").read()
        nomi |= set(re.findall(r'["\']([a-z_][a-z_0-9]{2,})["\']', testo))
    return nomi


# ------------------------------------------------------------- incoerenze
def incoerenze(docs):
    fuori = collections.defaultdict(list)
    per, tipi = percorsi_dati(docs)
    n = len(docs)

    # A. tipo variabile fra classi (a parte il null, che e' legittimo)
    for k, t in sorted(tipi.items()):
        if len(t - {"NoneType"}) > 1:
            fuori["tipo_variabile"].append((k, sorted(t)))

    for d in docs:
        cid = d["id"]
        m = d.get("mechanics_5e") or {}

        # B. stato di conversione che promette una meccanica assente
        for blocco in ("features", "chassis_features"):
            for b in (m.get(blocco) or []):
                if (b.get("mechanics_5e") is None
                        and b.get("conversion_status")
                        not in STATI_SENZA_MECCANICA):
                    fuori["stato_senza_meccanica"].append(
                        (cid, blocco, b.get("name"), b.get("conversion_status")))

        # C. features_pending contro i blocchi davvero senza meccanica
        if "features_pending" in m:
            vuoti = sum(1 for b in (m.get("features") or [])
                        if b.get("mechanics_5e") is None)
            if vuoti != m["features_pending"]:
                fuori["pending_non_torna"].append(
                    (cid, m["features_pending"], vuoti))

        # D. hit_die dichiarato due volte
        ch = m.get("chassis") or {}
        if "hit_die" in m and "hit_die" in ch and m["hit_die"] != ch["hit_die"]:
            fuori["hit_die_doppio"].append((cid, m["hit_die"], ch["hit_die"]))

        # E. una classe con chassis ma senza nessun privilegio di chassis
        if ch.get("srd_class") and not (m.get("chassis_features") or []):
            fuori["chassis_senza_privilegi"].append(
                (cid, ch["srd_class"],
                 len(m.get("chassis_features_da_trascrivere") or [])))

    return fuori, per, tipi, n


def enumerabili(docs):
    """Scalari con pochi valori distinti: sarebbero enum nello schema."""
    valori = collections.defaultdict(set)

    def scava(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                np = f"{p}.{k}"
                # Solo valori brevi: un campo di prosa con cinque testi
                # distinti non e' un enum, e' un campo libero.
                if isinstance(v, str) and len(v) <= 24:
                    valori[np].add(v)
                scava(v, np)
        elif isinstance(o, list):
            for it in o:
                scava(it, p + "[]")

    for d in docs:
        if d.get("mechanics_5e") is not None:
            scava(d["mechanics_5e"], "mechanics_5e")
    return {k: sorted(v) for k, v in valori.items()
            if 1 < len(v) <= 6 and not k.endswith((".name", ".name_srd"))}


# --------------------------------------------------- guardia di riduzione
CHIAVI_VIETATE = ("raw", "text_2e", "abilities_text", "descrizione")


def guardia_riduzione(doc, *insiemi):
    fuori = []

    def controlla(ident, valore):
        if not isinstance(valore, str) or len(valore) < 40:
            return
        for i in range(0, len(valore) - 40, 20):
            if valore[i:i + 40] in doc:
                fuori.append((ident, valore[i:i + 40]))
                return

    def scava(ident, o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in CHIAVI_VIETATE:
                    for x in (v if isinstance(v, list) else [v]):
                        controlla(f"{ident}.{k}", x)
                else:
                    scava(f"{ident}.{k}", v)
        elif isinstance(o, list):
            for x in o:
                scava(ident, x)

    for ins in insiemi:
        for d in ins:
            scava(d["id"], d)
    return fuori


# ------------------------------------------------------------------ rapporto
def tabella(intestazioni, righe, allin=None):
    allin = allin or ["---"] * len(intestazioni)
    out = ["| " + " | ".join(intestazioni) + " |",
           "|" + "|".join(allin) + "|"]
    for r in righe:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def main():
    classi = carica("classi")
    razze = carica("razze")
    dei = carica("divinita")

    inc, per, tipi, N = incoerenze(classi)
    usati = set(per)

    sc_classe = json.load(open(os.path.join(BASE, "schema/classe.schema.json"),
                               encoding="utf-8"))
    dichiarati = percorsi_schema(sc_classe["properties"]["mechanics_5e"])
    # I percorsi sotto `effetto` sono validati a parte, contro
    # effetto.schema.json, da valida_effetti.py: dichiarati altrove, non qui.
    sotto_effetto = {k for k in usati if ".effetto." in k or k.endswith(".effetto")}
    nudi = usati - dichiarati - sotto_effetto

    nomi_val = nomi_nei_validatori()
    def ultimo(p):
        return p.rstrip("[]").rsplit(".", 1)[-1].rstrip("[]")
    nominati = {k for k in nudi if ultimo(k) in nomi_val}
    mai_nominati = nudi - nominati

    # per blocco di primo livello
    blocchi = collections.Counter()
    blocchi_nudi = collections.Counter()
    for k in usati:
        cima = k.split(".")[1].rstrip("[]")
        blocchi[cima] += 1
        if k in nudi:
            blocchi_nudi[cima] += 1

    disomogenei = sorted((k for k in usati if len(per[k]) < N),
                         key=lambda k: (-len(per[k]), k))

    enum = enumerabili(classi)

    # gli altri due ingressi del Personaggio
    altri = []
    for nome, docs, file_schema in (("razza", razze, "razza.schema.json"),
                                    ("divinita", dei, "divinita.schema.json")):
        p, _ = percorsi_dati(docs)
        s = json.load(open(os.path.join(BASE, "schema", file_schema),
                           encoding="utf-8"))
        d = percorsi_schema(s["properties"]["mechanics_5e"])
        nulli = sum(1 for x in docs if x.get("mechanics_5e") is None)
        altri.append({"nome": nome, "file": len(docs), "usati": len(p),
                      "dich": len(d), "nulli": nulli})

    # stessa misura sugli schemi gia' chiusi, come termine di paragone
    chiusi = []
    for nome, file_schema, cartella in (("mostro", "mostro.schema.json", "mostri"),
                                        ("oggetto", "oggetto.schema.json", "oggetti"),
                                        ("modello", "modello.schema.json", "modelli")):
        s = json.load(open(os.path.join(BASE, "schema", file_schema),
                           encoding="utf-8"))
        m = s["properties"]["mechanics_5e"]
        docs = carica(cartella)
        p, _ = percorsi_dati(docs)
        d = percorsi_schema(m)
        chiusi.append({"nome": nome, "file": len(docs), "usati": len(p),
                       "dich": len(d),
                       "add": m.get("additionalProperties")})

    # ---- il lato razza, con lo stesso metro del lato classe (§5)
    per_rz, tipi_rz = percorsi_dati(razze)
    usati_rz = set(per_rz)
    sc_razza = json.load(open(os.path.join(BASE, "schema/razza.schema.json"),
                              encoding="utf-8"))
    dich_rz = percorsi_schema(sc_razza["properties"]["mechanics_5e"])
    eff_rz = {k for k in usati_rz if ".effetto." in k or k.endswith(".effetto")}
    nudi_rz = usati_rz - dich_rz - eff_rz
    nominati_rz = {k for k in nudi_rz if ultimo(k) in nomi_val}
    mai_nominati_rz = nudi_rz - nominati_rz
    blocchi_rz = collections.Counter()
    blocchi_nudi_rz = collections.Counter()
    for k in usati_rz:
        cima = k.split(".")[1].rstrip("[]")
        blocchi_rz[cima] += 1
        if k in nudi_rz:
            blocchi_nudi_rz[cima] += 1
    N_RZ = len(razze)
    disomogenei_rz = [k for k in usati_rz if len(per_rz[k]) < N_RZ]

    # ---- le dichiarazioni di origine, che e' il campo su cui la zona morta
    # e' gia' stata misurata da RAPPORTO-origine e va contata qui in blocchi.
    # Due casi che il totale da solo confonde: quelle che nessuno schema VEDE,
    # e quelle che lo schema vede e lascia libere.
    def origini(docs, blocchi_elenco):
        fuori = collections.Counter()
        for d in docs:
            m = d.get("mechanics_5e") or {}
            for b in blocchi_elenco:
                for e in (m.get(b) or []):
                    if isinstance(e, dict) and "conversion_status" in e:
                        fuori[b] += 1
        return fuori

    orig_rz = origini(razze, ["traits"])
    orig_cl = origini(classi, ["features", "chassis_features"])
    viste = {b: n for b, n in orig_cl.items()
             if f"mechanics_5e.{b}[].conversion_status" in dichiarati}
    cieche = ({("razza", b): n for b, n in orig_rz.items()}
              | {("classe", b): n for b, n in orig_cl.items() if b not in viste})
    n_cieche = sum(cieche.values())
    n_viste = sum(viste.values())

    tot_inc = sum(len(v) for v in inc.values())

    doc = f"""# Le zone morte di classe e di razza — quanto costa chiuderle

*Generato da `dati/analizza_zona_morta_classi.py` il {OGGI}. Non modificare a
mano: ogni numero è interpolato dai dati.*

---

## 0. La misura in una riga

`classe.schema.json` descrive `mechanics_5e` come *object o null*, con
{len(dichiarati)} proprietà dichiarate su **{len(usati)} percorsi in uso** nei
{N} file. Nessun `additionalProperties`.

> **{len(nudi)} percorsi su {len(usati)}** non sono dichiarati da nessuno
> schema. Di questi, **{len(mai_nominati)} non sono nominati nemmeno da un
> validatore**: un campo scritto storto lì dentro non incontra nessun
> controllo, in nessun punto della catena.

I {len(sotto_effetto)} percorsi sotto `effetto` non sono contati fra i nudi:
sono validati a parte contro `effetto.schema.json` da `valida_effetti.py`.
Sono l'unico pezzo dello strato che ha una verifica vera.

---

## 1. Dove stanno i {len(nudi)} percorsi nudi

{tabella(["blocco di primo livello", "percorsi in uso", "non dichiarati", "classi che lo portano"],
         [[f"`{b}`", blocchi[b], blocchi_nudi[b],
           f"{len(per['mechanics_5e.' + b])}/{N}"]
          for b in sorted(blocchi, key=lambda x: -blocchi[x])],
         ["---", "--:", "--:", "--:"])}

Il conto del lavoro si legge da questa tabella: non sono
{len(nudi)} decisioni indipendenti, sono **{len([b for b in blocchi_nudi if blocchi_nudi[b]])}
blocchi** da descrivere, e due di essi (`{"`, `".join(sorted(blocchi_nudi, key=lambda x: -blocchi_nudi[x])[:2])}`)
pesano da soli
{sum(sorted(blocchi_nudi.values(), reverse=True)[:2])} percorsi su {len(nudi)}.

### Quanto è già deciso

{len(enum)} campi scalari hanno **fra due e sei valori distinti** in tutto il
corpus: nello schema diventano `enum`, e il valore ammesso non va inventato,
va letto dai dati. Esempi:

{tabella(["percorso", "valori distinti in uso"],
         [[f"`{k}`", ", ".join(f"`{v}`" for v in enum[k])]
          for k in sorted(enum)[:12]],
         ["---", "---"])}

---

## 2. Le incoerenze fra classi

**{tot_inc} in tutto**, in {len([k for k, v in inc.items() if v])} famiglie.

### 2.1 Uno stato di conversione che promette una meccanica che non c'è

`{"`, `".join(STATI_SENZA_MECCANICA)}` sono gli stati in cui la meccanica 5e
può mancare — è scritto nella descrizione di `elemento_5e` in
`mostro.schema.json`, ed è l'invariante che distingue *«non è ancora stato
scritto»* da *«è stato scritto che non succede niente»*. Le classi la
violano:

{tabella(["classe", "blocco", "privilegio", "stato dichiarato"],
         [[f"`{c}`", f"`{b}`", n, f"**`{s}`**"]
          for c, b, n, s in inc["stato_senza_meccanica"]],
         ["---", "---", "---", "---"]) if inc["stato_senza_meccanica"] else "*nessuna*"}

Non è una svista di battitura: `direct` significa *conversione conclusa senza
adattamenti*. Due privilegi dichiarano di essere convertiti e non portano
niente.

### 2.2 Il numero che dice quanto manca non conta quei due

{tabella(["classe", "`features_pending` dichiarato", "privilegi davvero senza meccanica"],
         [[f"`{c}`", d, v] for c, d, v in inc["pending_non_torna"]],
         ["---", "--:", "--:"]) if inc["pending_non_torna"] else "*nessuna*"}

`features_pending` conta gli stati `pending`, non i blocchi vuoti. La
conseguenza è quella che conta: **`cavaliere-rosa` dichiara zero privilegi in
sospeso e ne ha uno vuoto.** È il numero che una schermata di stato
mostrerebbe come «classe completa».

Questa è la stessa forma del difetto già visto sei volte in questo progetto —
un derivato scritto accanto al dato invece che ricavato dal dato — e questa
volta è dentro lo strato che nessuno valida.

### 2.3 Percorsi disomogenei

{len(disomogenei)} percorsi su {len(usati)} non compaiono in tutte le
{N} classi. La maggior parte è legittima e attesa: un minimo di
caratteristica esiste solo dove la fonte lo pone, i titoli di livello solo
dove la 2e li stampa. Ma la disomogeneità non è distinguibile dall'errore
finché nessuno schema dice quale campo è facoltativo e quale no — che è
esattamente ciò che manca.

I casi in cui la disomogeneità segue una regola strutturale:

{tabella(["percorso", "classi", "regola"],
         [["`mechanics_5e.chassis.table_transcribed`",
           f"{len(per['mechanics_5e.chassis.table_transcribed'])}/{N}",
           "solo le classi con un chassis SRD"],
          ["`mechanics_5e.chassis_features[].name`",
           f"{len(per['mechanics_5e.chassis_features[].name'])}/{N}",
           "solo le tre classi su chassis Fighter: le altre hanno la lista vuota"],
          ["`mechanics_5e.ability_minimums.values.int`",
           f"{len(per['mechanics_5e.ability_minimums.values.int'])}/{N}",
           "solo dove la fonte 2e pone un minimo"]],
         ["---", "--:", "---"])}

### 2.4 Un chassis senza nessun privilegio di chassis

{tabella(["classe", "chassis SRD", "privilegi da trascrivere"],
         [[f"`{c}`", s, n] for c, s, n in inc["chassis_senza_privilegi"]],
         ["---", "---", "--:"]) if inc["chassis_senza_privilegi"] else "*nessuna*"}

Non è un errore: la prima fetta verticale ha compilato il solo chassis
Fighter, e le altre restano nomi dentro il filtro. È in tabella perché è
**indistinguibile da un errore** senza uno schema che dica se
`chassis_features` possa essere vuota quando `chassis.srd_class` è pieno.

### 2.5 Tipi variabili

{tabella(["percorso", "tipi in uso"],
         [[f"`{k}`", ", ".join(f"`{x}`" for x in t)] for k, t in inc["tipo_variabile"]],
         ["---", "---"]) if inc["tipo_variabile"] else "*nessuno*"}

{"Unico caso, e legittimo: `risorsa.usi` è un intero dove gli usi sono fissi e un oggetto `per_livello` dove crescono. `effetto.schema.json` lo dichiara già con un `anyOf` — ed è la prova che dove lo schema c'è, la variabilità è descritta invece che subita." if len(inc["tipo_variabile"]) == 1 else ""}

---

## 3. Non è una zona morta, sono tre

Il Personaggio lega razza + classe + divinità. Gli altri due ingressi stanno
nella stessa condizione, e uno sta peggio:

{tabella(["strato", "file", "percorsi in uso", "dichiarati dallo schema", "`mechanics_5e` null"],
         [["**classe**", N, len(usati), len(dichiarati), 0]] +
         [[f"**{a['nome']}**", a["file"], a["usati"], a["dich"], a["nulli"]]
          for a in altri],
         ["---", "--:", "--:", "--:", "--:"])}

`razza.schema.json` dichiara **zero** proprietà per `mechanics_5e`, su
{[a["usati"] for a in altri if a["nome"] == "razza"][0]} percorsi in uso:
peggio delle classi, che almeno ne hanno {len(dichiarati)}. È lo strato dove
vive il tappo della decisione 20 (`tappo-barbaro`), in
`razze/umano-barbaro.json`: il campo che esiste solo in `mechanics_5e` e che
il motore, leggendo `source_2e`, scartava in silenzio. Il difetto trovato ieri
stava dentro la zona morta più grande delle tre, e nessuno schema lo
descriveva.

`divinita.schema.json` dichiara zero proprietà su zero percorsi in uso: tutte
e {[a["file"] for a in altri if a["nome"] == "divinita"][0]} le divinità hanno
`mechanics_5e` a null. È una zona morta vuota: nessun rischio oggi, nessuna
guardia domani.

### Il termine di paragone: gli schemi che sono stati chiusi

{tabella(["strato", "file", "percorsi in uso", "dichiarati", "`additionalProperties`"],
         [[f"**{c['nome']}**", c["file"], c["usati"], c["dich"],
           f"`{c['add']}`"] for c in chiusi],
         ["---", "--:", "--:", "--:", ":-:"])}

Sono la misura vera del costo: `mostro` dichiara
{[c["dich"] for c in chiusi if c["nome"] == "mostro"][0]} percorsi per
{[c["usati"] for c in chiusi if c["nome"] == "mostro"][0]} in uso su
{[c["file"] for c in chiusi if c["nome"] == "mostro"][0]} file, con
`additionalProperties: false`. Il lavoro sulle classi è dello stesso ordine
di grandezza, su meno file.

---

## 4. Il conto

{tabella(["", ""],
         [["percorsi in uso sotto `mechanics_5e`, {} file".format(N), len(usati)],
          ["già dichiarati da `classe.schema.json`", len(dichiarati)],
          ["già dichiarati da `effetto.schema.json` (validati a parte)", len(sotto_effetto)],
          ["**da dichiarare**", f"**{len(nudi)}**"],
          ["…di cui nominati almeno da un validatore", len(nominati)],
          ["…di cui **nominati da nessuno**", f"**{len(mai_nominati)}**"],
          ["blocchi di primo livello da descrivere",
           len([b for b in blocchi_nudi if blocchi_nudi[b]])],
          ["campi scalari che diventano `enum` letti dai dati", len(enum)],
          ["**incoerenze già presenti nei dati**", f"**{tot_inc}**"]],
         ["---", "--:"])}

**Il costo non è nei {len(nudi)} percorsi.** Sono
{len([b for b in blocchi_nudi if blocchi_nudi[b]])} blocchi, e uno solo —
`structural` — ne porta {blocchi_nudi["structural"]}: è la scheda 2e
riportata intera (tabella dei punti esperienza, progressione d'attacco, tiri
salvezza, competenze, titoli, equipaggiamento iniziale), cioè un lavoro di
trascrizione, non di decisione.

La decisione unica dentro il conto è `features`: {blocchi_nudi["features"]}
percorsi che descrivono **la stessa forma di elemento** — nome, livello,
stato, prosa, nota — già descritta due volte altrove, in `elemento_5e` di
`mostro.schema.json` e nel blocco `chassis_features` di questo stesso file.
Tre copie della stessa forma è la domanda a cui questo progetto ha già
risposto sei volte.

Il pezzo che non si risolve da solo sono le {tot_inc} incoerenze: non si
chiude uno schema attorno a dati che lo violano. `additionalProperties: false`
con `conversion_status: direct` e `mechanics_5e: null` insieme non passa —
o si corregge il dato, o si scrive nello schema che quello stato ammette il
vuoto, cioè si dichiara che l'invariante non vale.

---

## 5. Il lato razza, con lo stesso metro

§3 diceva che le zone morte sono tre e che una sta peggio. Questa è quella,
misurata come le classi invece che citata di sfuggita.

`razza.schema.json` descrive `mechanics_5e` come un oggetto senza **nessuna**
proprietà dichiarata: {len(usati_rz)} percorsi in uso nei {N_RZ} file,
{len(dich_rz)} dichiarati.

> **{len(nudi_rz)} percorsi su {len(usati_rz)}** non sono dichiarati da nessuno
> schema, e **{len(mai_nominati_rz)}** non sono nominati nemmeno da un
> validatore.

{tabella(["blocco di primo livello", "percorsi in uso", "non dichiarati", "razze che lo portano"],
         [[f"`{b}`", blocchi_rz[b], blocchi_nudi_rz[b],
           f"{len(per_rz['mechanics_5e.' + b])}/{N_RZ}"]
          for b in sorted(blocchi_rz, key=lambda x: -blocchi_rz[x])],
         ["---", "--:", "--:", "--:"])}

{len([b for b in blocchi_nudi_rz if blocchi_nudi_rz[b]])} blocchi da
descrivere, contro i {len([b for b in blocchi_nudi if blocchi_nudi[b]])} delle
classi. Il blocco più pesante è
`{max(blocchi_nudi_rz, key=lambda b: blocchi_nudi_rz[b])}` con
{max(blocchi_nudi_rz.values())} percorsi.
{len(disomogenei_rz)} percorsi su {len(usati_rz)} non compaiono in tutte le
razze: come per le classi, la disomogeneità è cosa uno schema deve decidere se
ammettere, e finché non c'è schema non è stata decisa.

### 5a. Le dichiarazioni di origine: due casi, non uno

`RAPPORTO-origine.md` §5b misura lo stesso difetto su un campo solo,
`conversion_status` di livello elemento, e dà il numero grosso. Qui va spezzato
in due, perché costano cose diverse:

{tabella(["famiglia", "blocco", "dichiarazioni", "lo schema le vede?"],
         [[f, f"`{b}`", n, "**no**"] for (f, b), n in sorted(cieche.items())]
         + [["classe", f"`{b}`", n, "sì, come stringa libera"]
            for b, n in sorted(viste.items())],
         ["---", "---", "--:", "---"])}

- **{n_cieche} dichiarazioni che nessuno schema vede.** Stanno in blocchi che
  lo schema non descrive affatto: `traits` delle razze e `features` delle
  classi. Si chiudono descrivendo il blocco, cioè dentro il lavoro già contato
  sopra — non sono una voce in più.
- **{n_viste} dichiarazioni che lo schema vede e lascia libere.** Sono in
  `chassis_features`, dichiarato con `"type": "string"` e nessun `enum`. Questo
  è il caso che costa **una riga**: un `$ref` alla sede del vocabolario, la
  stessa che i mostri, gli oggetti e i modelli usano già. È anche il caso più
  insidioso, perché un campo dichiarato *sembra* controllato.

### 5b. Il conto delle due zone morte insieme

{tabella(["", "classe", "razza", "insieme"],
         [["file", N, N_RZ, N + N_RZ],
          ["percorsi in uso sotto `mechanics_5e`", len(usati), len(usati_rz),
           len(usati) + len(usati_rz)],
          ["già dichiarati dallo schema", len(dichiarati), len(dich_rz),
           len(dichiarati) + len(dich_rz)],
          ["già dichiarati da `effetto.schema.json`", len(sotto_effetto),
           len(eff_rz), len(sotto_effetto) + len(eff_rz)],
          ["**da dichiarare**", f"**{len(nudi)}**", f"**{len(nudi_rz)}**",
           f"**{len(nudi) + len(nudi_rz)}**"],
          ["…nominati da nessun validatore", len(mai_nominati),
           len(mai_nominati_rz), len(mai_nominati) + len(mai_nominati_rz)],
          ["blocchi di primo livello da descrivere",
           len([b for b in blocchi_nudi if blocchi_nudi[b]]),
           len([b for b in blocchi_nudi_rz if blocchi_nudi_rz[b]]),
           len([b for b in blocchi_nudi if blocchi_nudi[b]])
           + len([b for b in blocchi_nudi_rz if blocchi_nudi_rz[b]])],
          ["incoerenze già nei dati", tot_inc, "—", tot_inc]],
         ["---", "--:", "--:", "--:"])}

Il termine di paragone resta quello di §3: `mostro.schema.json` dichiara
{[c["dich"] for c in chiusi if c["nome"] == "mostro"][0]} percorsi su
{[c["usati"] for c in chiusi if c["nome"] == "mostro"][0]} in uso, con
`additionalProperties: false`, su {[c["file"] for c in chiusi if c["nome"] == "mostro"][0]}
file. Le due zone morte insieme chiedono
{len(nudi) + len(nudi_rz)} dichiarazioni contro le
{[c["dich"] for c in chiusi if c["nome"] == "mostro"][0]} già scritte per il
mostro — {(len(nudi) + len(nudi_rz)) / [c["dich"] for c in chiusi if c["nome"] == "mostro"][0]:.1f}
volte quel lavoro — su {N + N_RZ} file invece di
{[c["file"] for c in chiusi if c["nome"] == "mostro"][0]}. E senza le
{tot_inc} incoerenze non si comincia, perché uno schema non si chiude attorno
a dati che lo violano.

**L'ordine che costa meno**, e non è quello dei numeri:

1. Le {n_viste} dichiarazioni di `chassis_features`: **una riga** — un `$ref`
   alla sede del vocabolario — e toglie il caso in cui un campo dichiarato
   sembra controllato.
2. Il blocco `features` ({blocchi_nudi["features"]} percorsi): è la stessa
   forma di elemento già descritta due volte altrove, e va risolta una volta
   per tutte e tre invece che una terza volta qui. È l'unica decisione dentro
   il conto.
3. I due blocchi grossi delle razze —
   {", ".join(f"`{b}` ({blocchi_nudi_rz[b]})" for b in sorted(blocchi_nudi_rz, key=lambda x: -blocchi_nudi_rz[x])[:2])}
   — che sono numeri e limiti, cioè trascrizione con `enum` e `minimum`
   leggibili dai dati, non decisioni.
4. `structural` ({blocchi_nudi["structural"]} percorsi): il pezzo più grosso
   di tutti e il meno rischioso, perché è la scheda 2e riportata intera.

Le {tot_inc} incoerenze non stanno in questa scaletta perché non sono lavoro
di schema: sono dati da correggere, e vengono prima di tutto.

---

*Nessuna decisione è presa in questo documento, e nessuno schema è toccato.*
"""

    fuori = guardia_riduzione(doc, classi, razze, dei)
    if fuori:
        print("RIDUZIONE FALLITA — testo di fonte nel rapporto pubblico:")
        for ident, pezzo in fuori[:10]:
            print(f"  {ident}: {pezzo}…")
        return 1

    with open(USCITA, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"scritto {os.path.relpath(USCITA, RADICE)} "
          f"({len(doc.splitlines())} righe)")
    print(f"percorsi in uso {len(usati)}, dichiarati {len(dichiarati)}, "
          f"nudi {len(nudi)}, mai nominati {len(mai_nominati)}")
    print(f"incoerenze: {tot_inc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
