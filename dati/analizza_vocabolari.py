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
# le sedi: il controllo 3 verifica gli id di condizione citati da `effetto` e
# NON tocca `condition_immunities`, che e' proprio la sede rotta.
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


# Corrispondenza fra i nomi inglesi delle immunita' a condizione e gli id di
# dati/condizioni/. SERVE SOLO A CONTARE quante condizioni mancherebbero se si
# traducesse il campo: NON e' una traduzione adottata da nessuna parte, e
# nessun dato la usa. Scritta qui perche' l'alternativa era stimare a occhio
# la sovrapposizione, e una stima a occhio dentro un rapporto di misura e'
# esattamente il difetto che il rapporto denuncia.
COND_EN_IT = {
    "blinded": "accecato", "charmed": "affascinato", "deafened": "assordato",
    "exhaustion": "sfinimento", "frightened": "spaventato",
    "grappled": "afferrato", "incapacitated": "incapacitato",
    "invisible": "invisibile", "paralyzed": "paralizzato",
    "petrified": "pietrificato", "poisoned": "avvelenato", "prone": "prono",
    "restrained": "trattenuto", "stunned": "stordito",
    "unconscious": "incosciente",
}


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

    # Quante condizioni mancherebbero davvero: le immunita' inglesi tradotte,
    # meno quelle che dati/condizioni/ ha gia'.
    imm_en = set(misure["condizioni"][0][2])
    id_it = set(misure["condizioni"][1][2])
    ignote = sorted(imm_en - set(COND_EN_IT))
    if ignote:
        # Un nome inglese fuori tabella farebbe scendere il conteggio senza
        # dirlo: il rapporto direbbe "ne mancano N" con N sbagliato.
        sys.exit(f"immunita' a condizione fuori da COND_EN_IT: {ignote}. "
                 f"Aggiungile alla tabella prima di rigenerare il rapporto.")
    tradotte = {COND_EN_IT[c] for c in imm_en if c in COND_EN_IT}
    gia_presenti = sorted(tradotte & id_it)
    mancanti = sorted(tradotte - id_it)

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

**`condition_immunities` — lo stesso difetto dei tipi di danno, un anno piu'
avanti.** `dati/mostri/` dichiara le immunita' a condizione con i nomi
inglesi della 5e ({len(misure['condizioni'][0][2])} distinti su
{sum(misure['condizioni'][0][2].values())} occorrenze: `charmed`, `poisoned`,
`petrified`, `prone`, `restrained`...), mentre `dati/condizioni/` — che
{cita('condizioni-a-consumo')} dichiara sede unica — ha
{len(misure['condizioni'][1][2])} id italiani. Il campo `effetto` risolve
contro la sede italiana e il controllo 3 lo verifica; `condition_immunities`
non risolve contro niente. E' **piu' grave** dei tipi di danno, perche' li'
le due sedi erano due trascrizioni e qui una delle due e' una **sede
dichiarata** che l'altra ignora.

Non si chiude senza una decisione, e le due strade costano cose diverse.
**Tradurre e basta** significa che le {len(imm_en)} condizioni citate dalle
immunita' diventano id italiani, e solo {len(gia_presenti)} di quegli id
esistono in `dati/condizioni/` ({', '.join('`' + c + '`' for c in gia_presenti)}).
Gli altri **{len(mancanti)}** non esistono
({', '.join('`' + c + '`' for c in mancanti)}): o si accettano riferimenti che
non risolvono, o si creano {len(mancanti)} condizioni per anticipazione — cioe'
si sconfessa il criterio di {cita('condizioni-a-consumo')}, applicato per la
prima volta tre giorni fa. **Restringere l'enum alle cinque esistenti** e' peggio: le
schede perderebbero informazione vera di fonte. La terza strada — un
vocabolario delle condizioni **separato** dalla cartella delle condizioni
convertite, dove l'id esiste come termine e la scheda meccanica arriva dopo —
e' probabilmente quella giusta e non e' una riga di enum: e' la stessa
distinzione fra *nominare* e *convertire* che il progetto fa gia' altrove.

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
