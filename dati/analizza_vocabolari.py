#!/usr/bin/env python3
"""
I vocabolari condivisi fra due o piu' schemi, misurati.

PERCHE' ESISTE
    L'ottava struttura doppia del progetto — i tipi di danno in inglese in
    dati/oggetti/ e in italiano in dati/mostri/ — non e' stata trovata
    ispezionando i dati ma USANDOLI: nessuno dei due lati era sbagliato dal
    proprio, quindi nessun validatore poteva vederlo. La domanda che ne
    segue e' se altri vocabolari abbiano lo stesso difetto, e non si
    risponde a memoria: si contano le SEDI di ogni termine condiviso e si
    guarda se uno schema lo vincola.

    Un vocabolario e' a rischio quando ha PIU' DI UNA SEDE e nessun enum
    comune. Con una sede sola il difetto non e' presente — puo' arrivare
    col prossimo file che lo usa, ed e' questo che il rapporto misura:
    quali vocabolari sono gia' rotti, quali sono integri per fortuna e
    quali per struttura.

Uso:  python3 dati/analizza_vocabolari.py
"""

import glob
import json
import os
import sys
import textwrap
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.dirname(BASE))

import _vocabolari as V  # noqa: E402
from decisioni import cita  # noqa: E402

CARTELLE = ("razze", "classi", "divinita", "mostri", "oggetti", "incantesimi",
            "modelli", "condizioni")

# I vocabolari sotto osservazione: quelli nominati dalla domanda piu' quelli
# che il giro ha incontrato. La chiave e' il nome, il valore l'elenco dei
# percorsi (cartella, percorso sotto la radice del documento) in cui il
# termine compare come VALORE.
VOCABOLARI = {
    "tipi di danno": [
        ("oggetti", "mechanics_5e.weapon_5e.damage_type"),
        ("mostri", "mechanics_5e.*.effetto.attacco.danno[].tipo"),
        ("mostri", "mechanics_5e.damage_resistances[].tipo"),
        ("mostri", "mechanics_5e.damage_immunities[].tipo"),
        ("mostri", "mechanics_5e.damage_vulnerabilities[].tipo"),
    ],
    "condizioni": [
        ("mostri", "mechanics_5e.condition_immunities[]"),
        ("condizioni", "id"),
        ("mostri", "mechanics_5e.*.effetto.tiro_salvezza.*.condizioni[].id"),
    ],
    "taglia": [
        ("mostri", "mechanics_5e.size"),
        ("razze", "mechanics_5e.size"),
    ],
    "tipo di creatura": [
        ("mostri", "mechanics_5e.type"),
    ],
    "scuole di magia": [
        ("incantesimi", "school"),
    ],
    "categorie d'arma": [
        ("oggetti", "mechanics_5e.weapon_5e.categoria"),
        ("classi", "mechanics_5e.structural.weapon_proficiencies.categorie[]"),
    ],
    "categorie d'armatura": [
        ("oggetti", "mechanics_5e.armor_5e.categoria"),
        ("classi", "mechanics_5e.structural.armor_proficiencies.categorie[]"),
    ],
    "allineamento": [
        ("mostri", "mechanics_5e.alignment"),
    ],
}


# ------------------------------------------------------------------ lettura

def carica(cartella):
    for f in sorted(glob.glob(os.path.join(BASE, cartella, "*.json"))):
        yield os.path.basename(f), json.load(open(f, encoding="utf-8"))


def scendi(nodo, passi):
    """I valori a `passi` dentro `nodo`. `*` attraversa ogni chiave, `[]`
    ogni elemento di lista."""
    if not passi:
        if isinstance(nodo, str):
            yield nodo
        return
    testa, resto = passi[0], passi[1:]
    if testa.endswith("[]"):
        chiave = testa[:-2]
        sotto = nodo.get(chiave) if isinstance(nodo, dict) else None
        for v in (sotto or []):
            yield from scendi(v, resto)
        return
    if testa == "*":
        if isinstance(nodo, dict):
            for v in nodo.values():
                if isinstance(v, list):
                    for x in v:
                        yield from scendi(x, resto)
                else:
                    yield from scendi(v, resto)
        return
    if isinstance(nodo, dict):
        yield from scendi(nodo.get(testa), resto)


def valori(cartella, percorso):
    out = Counter()
    passi = percorso.split(".")
    for _, d in carica(cartella):
        for v in scendi(d, passi):
            out[v] += 1
    return out


# ------------------------------------------------------------------- schemi

def enum_dichiarati():
    """Ogni enum degli schemi, per percorso approssimato. Serve a dire se un
    vocabolario e' VINCOLATO o solo praticato."""
    fuori = defaultdict(list)
    for f in sorted(glob.glob(os.path.join(BASE, "schema", "*.json"))):
        nome = os.path.basename(f)
        d = json.load(open(f, encoding="utf-8"))

        def cammina(nodo, dove):
            if isinstance(nodo, dict):
                if "enum" in nodo and isinstance(nodo["enum"], list):
                    fuori[dove].append((nome, tuple(nodo["enum"])))
                if "$ref" in nodo:
                    fuori[dove].append((nome, ("$ref", nodo["$ref"])))
                for k, v in nodo.items():
                    prossimo = dove if k in ("properties", "$defs", "items",
                                             "anyOf", "allOf", "oneOf") else f"{dove}.{k}"
                    cammina(v, prossimo)
            elif isinstance(nodo, list):
                for v in nodo:
                    cammina(v, dove)

        cammina(d, "")
    return fuori


def vincolo(cartella, percorso, enums):
    """Lo schema di `cartella` vincola l'ultimo passo di `percorso`?"""
    schema = {"oggetti": "oggetto", "mostri": "mostro", "classi": "classe",
              "razze": "razza", "incantesimi": "incantesimo",
              "condizioni": "condizione", "modelli": "modello",
              "divinita": "divinita"}[cartella] + ".schema.json"
    ultimo = percorso.rstrip("[]").split(".")[-1].rstrip("[]")
    for dove, voci in enums.items():
        if not dove.endswith("." + ultimo):
            continue
        for nome, e in voci:
            if nome == schema:
                return ("$ref " + e[1]) if e[0] == "$ref" else "enum"
    # effetto.schema.json vale su ogni `effetto`, ovunque stia
    if ".effetto." in percorso:
        for dove, voci in enums.items():
            if dove.endswith("." + ultimo):
                for nome, e in voci:
                    if nome == "effetto.schema.json":
                        return ("$ref " + e[1]) if e[0] == "$ref" else "enum"
    return None


# ------------------------------------------------------------------ rapporto

# Controlli incrociati che gia' esistono FUORI dagli schemi, con le SEDI che
# ciascuno copre davvero. Vanno dichiarati qui o il rapporto mente per
# difetto: le categorie d'arma non sono vincolate dallo schema delle classi,
# ma il controllo 4 di dati/valida_effetti.py mette le due sedi una contro
# l'altra ed esce != 0 se divergono — un modo diverso di chiudere lo stesso
# buco, non un buco. Mente anche per eccesso se si scrive il controllo senza
# le sedi: fino al 02/09/2026 il controllo 3 verificava gli id di condizione
# citati da `effetto` e NON toccava `condition_immunities`, che era proprio
# la sede rotta. Ora quella sede e' vincolata dallo schema (`$ref` al
# vocabolario condiviso) e `valida_effetti.controlla_immunita_condizione()`
# ne misura il divario col catalogo: sono due cose diverse, e la seconda non
# e' un controllo di divergenza ma una misura, quindi non entra qui.
CONTROLLI = {
    ("mostri", "mechanics_5e.*.effetto.tiro_salvezza.*.condizioni[].id"):
        "valida_effetti.py, controllo 3",
    ("condizioni", "id"):
        "valida_effetti.py, controllo 3",
    ("classi", "mechanics_5e.structural.weapon_proficiencies.categorie[]"):
        "valida_effetti.py, controllo 4",
    ("classi", "mechanics_5e.structural.armor_proficiencies.categorie[]"):
        "valida_effetti.py, controllo 4",
    ("oggetti", "mechanics_5e.weapon_5e.categoria"):
        "valida_effetti.py, controllo 4",
    ("oggetti", "mechanics_5e.armor_5e.categoria"):
        "valida_effetti.py, controllo 4",
}


# La traduzione dai nomi SRD agli id italiani NON sta piu' qui. Fino al
# 02/09/2026 questo file ne portava una copia con la nota «serve solo a
# contare, nessun dato la usa»: da quando
# decisione 53 (`condizioni-vocabolario-srd`) l'ha adottata, quella copia
# sarebbe una struttura doppia nuova, creata dentro il rapporto che le
# misura. Si legge dalla sede unica.
DA_SRD_CONDIZIONE = V.CONDIZIONE_DA_SRD


def copertura(cartella, percorso, vinc):
    """Come questa sede e' tenuta ferma: schema, controllo, o niente."""
    if vinc:
        return "schema"
    if (cartella, percorso) in CONTROLLI:
        return CONTROLLI[(cartella, percorso)]
    return None


def main():
    enums = enum_dichiarati()
    misure = {}
    for nome, sedi in VOCABOLARI.items():
        presenti = []
        for cartella, percorso in sedi:
            v = valori(cartella, percorso)
            if not v:
                continue
            vinc = vincolo(cartella, percorso, enums)
            presenti.append((cartella, percorso, v, vinc,
                             copertura(cartella, percorso, vinc)))
        if presenti:
            misure[nome] = presenti

    def scoperte(presenti):
        return [p for p in presenti if p[4] is None]

    def stato(presenti):
        aperte = scoperte(presenti)
        if len(presenti) < 2:
            return ("una sede sola" if aperte
                    else "una sede sola, vincolata")
        if not aperte:
            return "**chiuso**"
        n = len(aperte)
        quante = "1 sede scoperta" if n == 1 else f"{n} sedi scoperte"
        return f"**APERTO** — {quante} su {len(presenti)}"

    # Il divario fra cio' che il vocabolario NOMINA e cio' che il catalogo
    # CONVERTE. Non si stima e non si scrive: si deriva dalle due sedi.
    imm = set(misure["condizioni"][0][2])
    id_it = set(misure["condizioni"][1][2])
    fuori_vocabolario = sorted(imm - set(V.CONDIZIONI))
    if fuori_vocabolario:
        sys.exit(f"immunita' a condizione fuori dal vocabolario: "
                 f"{fuori_vocabolario}. L'insieme SRD e' chiuso: o e' un "
                 f"refuso, o non e' una condizione.")
    gia_presenti = sorted(imm & id_it)
    mancanti = sorted(imm - id_it)
    non_modellate = V.condizioni_non_modellate()

    aperti = [n for n, p in misure.items() if len(p) > 1 and scoperte(p)]
    una_sede = [n for n, p in misure.items() if len(p) == 1]

    testa = f"""# I vocabolari condivisi — quali sono gia' rotti e quali reggono per fortuna

*Generato da `dati/analizza_vocabolari.py`.*

---

## 0. La domanda

L'ottava struttura doppia del progetto sono stati i tipi di danno, e non e'
stata trovata ispezionando i dati: e' stata trovata **usandoli**. Nessuno dei
due lati era sbagliato dal proprio — `slashing` e' il termine dell'SRD,
`perforante` e' l'italiano dello strato nostro — quindi nessuno schema e
nessun validatore poteva vederlo. Chiusa con {cita('vocabolario-italiano')}.

La domanda che resta e' se altri vocabolari condivisi abbiano lo stesso
difetto. Non si risponde a memoria: si contano le **sedi** di ogni termine, si
guarda se uno schema lo vincola, e — questa e' la parte che un conteggio
ingenuo sbaglia — si guarda se un **controllo incrociato** lo tiene fermo
anche senza schema. Le categorie d'arma non sono vincolate dallo schema delle
classi eppure non divergono, perche' il controllo 4 di `valida_effetti.py`
mette le due sedi una contro l'altra. Contarle come rotte sarebbe falso.

Un vocabolario con **una sede sola** non e' sano: e' **non ancora esposto**.
Il difetto arriva col prossimo file che usa lo stesso termine.

> **{len(aperti)} vocabolari aperti su {len(misure)} esaminati**, piu' {len(una_sede)} con una sede sola.

---

## 1. Il quadro

| vocabolario | sedi | valori distinti | come e' tenuto fermo | stato |
|---|--:|--:|---|---|
"""
    for nome, presenti in misure.items():
        tot = len(set().union(*[set(p[2]) for p in presenti]))
        come = ", ".join(sorted({(p[4] or "niente") for p in presenti}))
        testa += (f"| {nome} | {len(presenti)} | {tot} | {come} | "
                  f"{stato(presenti)} |\n")

    testa += "\n---\n\n## 2. Sede per sede\n"
    for nome, presenti in misure.items():
        testa += f"\n### {nome}\n\n"
        for cartella, percorso, v, vin, cop in presenti:
            campione = ", ".join(f"`{k}`" for k, _ in v.most_common(6))
            marchio = "scoperta" if cop is None else cop
            testa += (f"- `dati/{cartella}/` → `{percorso}` — "
                      f"{len(v)} valori distinti su {sum(v.values())} "
                      f"occorrenze, **{marchio}**. {campione}\n")

    testa += f"""
---

## 3. I tre casi che restano aperti, e cosa costa chiuderli

**`condition_immunities` — chiusa, e non traducendo e basta.**
`dati/mostri/` dichiarava le immunita' a condizione con i nomi inglesi della
5e mentre `dati/condizioni/` — che {cita('condizioni-a-consumo')} dichiara
sede unica — ha id italiani: stesso difetto dei tipi di danno, e **piu'
grave**, perche' li' erano due trascrizioni e qui una delle due sedi era gia'
**dichiarata unica** e l'altra la ignorava. Nessuna immunita' del bestiario
poteva essere rispettata da nessun motore.

Tradurre e basta non bastava, ed e' la ragione per cui il caso era rimasto
aperto: delle condizioni citate dalle immunita' solo
{len(gia_presenti)} avevano una scheda in `dati/condizioni/`
({', '.join('`' + c + '`' for c in gia_presenti)}), quindi o si accettavano
{len(mancanti)} riferimenti che non risolvono, o si creavano
{len(mancanti)} condizioni per anticipazione — cioe' si sconfessava
{cita('condizioni-a-consumo')} tre giorni dopo averla presa.

Chiusa con {cita('condizioni-vocabolario-srd')} per la strada dei repertori
({cita('repertori-sono-filtri')}): l'insieme delle condizioni SRD e' **chiuso
e noto**, quindi il vocabolario e' **completo** — {len(V.CONDIZIONI)} termini
in `vocabolari.schema.json`, riferiti per `$ref` da `mostro.schema.json` —
mentre il catalogo ne converte {len(V.condizioni_modellate())}. Le altre
{len(non_modellate)} non sono condizioni **inesistenti**: sono una **lacuna
del nostro catalogo**, che e' cosa diversa, e non si scrive da nessuna parte
— si deriva dai file presenti nella cartella.

Il divario resta, e adesso e' un numero invece che un dubbio:
**{sum(misure['condizioni'][0][2].values())} immunita'** nel bestiario, di cui
**{sum(n for c, n in misure['condizioni'][0][2].items() if c in non_modellate)}**
nominano una delle {len(non_modellate)} condizioni che il motore non sa
ancora applicare ({', '.join('`' + c + '`' for c in non_modellate)}). Il
motore lo **dichiara** — lacuna `condizione-non-modellata` — perche'
un'immunita' saltata in silenzio e' indistinguibile da un'immunita'
rispettata.

**`taglia` — due sedi, una sola vincolata, d'accordo per fortuna.**
`mostro.schema.json` ha l'enum `Tiny…Gargantuan`; `razza.schema.json`
dichiara **zero proprieta'** sotto `mechanics_5e` (e' una delle tre zone
morte gia' misurate in `RAPPORTO-zona-morta-classi.md`), quindi la taglia
delle razze non e' vincolata da niente. Oggi i valori coincidono —
{len(misure['taglia'][1][2])} valori sulle razze, tutti dentro l'enum dei
mostri — ma per fortuna, non per struttura: e' esattamente lo stato in cui
erano i tipi di danno prima di divergere. Chiuderlo e' **una riga**: il
`$ref` al vocabolario condiviso da entrambi gli schemi. Non e' stato fatto in
questo giro perche' tocca `razza.schema.json`, cioe' apre una delle tre zone
morte, e quello e' un lavoro a se'.

**`tipo di creatura`, `allineamento`, `scuole di magia` — una sede sola.**
Nessuno dei tre e' rotto e nessuno dei tre e' al sicuro. Le scuole hanno un
enum e stanno bene. `mechanics_5e.type` dei mostri
({len(misure['tipo di creatura'][0][2])} valori distinti, inglese
maiuscolizzato) **non ha enum**: il giorno in cui un secondo file — un
modello, un incantesimo che filtra per tipo di creatura — nominera' gli
stessi termini, il difetto nasce li'. `mechanics_5e.alignment`
({len(misure['allineamento'][0][2])} valori distinti) **non e' un
vocabolario affatto**: e' prosa, e ne porta la prova un valore solo, «Typically
Chaotic Evil (solo quando animata da un incantesimo malvagio; altrimenti
inanimata e innocua)». Vincolarlo a un enum vorrebbe dire buttare via quella
clausola o darle un campo — la stessa forma del problema che `solo_se` ha
risolto per le resistenze, e la stessa risposta gia' pronta.

---

*Nessuna decisione e' presa in questo documento oltre a quelle gia'
registrate. I tre casi aperti sono misurati, non chiusi: due di loro tirano
dentro un lavoro dichiarato a se' (le zone morte di schema, il criterio delle
condizioni), e chiuderli di straforo sarebbe la scorciatoia che questo
progetto paga sempre due volte.*
"""
    return testa, misure


def riflow(testo, larghezza=78):
    """Riavvolge i paragrafi di prosa a `larghezza`.

    Serve perche' la prosa e i numeri stanno nello stesso f-string: un
    conteggio interpolato spezza la riga dove capita, e il documento
    generato si legge peggio di uno scritto a mano. Tabelle, elenchi,
    titoli e citazioni restano come sono."""
    fuori = []
    for blocco in testo.split("\n\n"):
        righe = blocco.split("\n")
        if any(r.lstrip().startswith(("|", "- ", "#", ">", "*Generato"))
               or r.startswith("    ") or r.strip() in ("---", "")
               for r in righe):
            fuori.append(blocco)
            continue
        fuori.append(textwrap.fill(" ".join(r.strip() for r in righe),
                                   width=larghezza,
                                   break_long_words=False,
                                   break_on_hyphens=False))
    return "\n\n".join(fuori)


if __name__ == "__main__":
    testo, _ = main()
    testo = riflow(testo)
    out = os.path.join(BASE, "RAPPORTO-vocabolari.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(testo)
    print(f"scritto {out} ({len(testo.splitlines())} righe)")
