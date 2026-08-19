#!/usr/bin/env python3
"""
Verifica di giocabilita' del filtro delle sfere (decisione 24).

DA ESEGUIRE PRIMA DI ATTIVARE IL FILTRO.
    Il filtro nega l'accesso agli incantesimi fuori dalle sfere della divinita'.
    Prima di applicarlo bisogna sapere se ogni divinita' produce ancora un
    chierico giocabile. Questo script non risolve nulla: conta.

DUE USCITE
    RAPPORTO-sfere.md            pubblico. Le schede per divinita' NON
                                  elencano le sfere maggiori/minori: e' la
                                  tabella del capitolo Realms Above,
                                  riprodotta per intero se elencata.
    RAPPORTO-sfere-completo.md   privato (escluso dal repo pubblico). Stesso
                                  documento, con le sfere maggiori/minori per
                                  riferimento interno.
    La riduzione e' una funzione del generatore (parametro `completo` di
    `scheda_divinita()`), non un intervento a posteriori.

Uso:  python3 verifica_sfere.py
"""

import collections
import glob
import json
import os
from datetime import date

import _sfere_5e as S

BASE = os.path.dirname(os.path.abspath(__file__))
OGGI = date.today().isoformat()

# Soglie di praticabilita', dichiarate qui e non sparse nel testo.
SOGLIA_PER_LIVELLO = 3      # meno di 3 incantesimi a un livello = sotto soglia
LIVELLI = list(range(1, 10))

GUARIGIONE = {"Cure Wounds", "Healing Word", "Mass Healing Word",
              "Prayer of Healing", "Mass Cure Wounds", "Heal", "Mass Heal",
              "Lesser Restoration", "Greater Restoration", "Beacon of Hope",
              "Revivify", "Raise Dead", "Resurrection", "True Resurrection",
              "Regenerate", "Spare the Dying"}
GUARIGIONE_VERA = {"Cure Wounds", "Healing Word", "Mass Healing Word",
                   "Prayer of Healing", "Mass Cure Wounds", "Heal", "Mass Heal"}
OFFESA = {"Sacred Flame", "Guiding Bolt", "Inflict Wounds", "Spiritual Weapon",
          "Blindness/Deafness", "Spirit Guardians", "Flame Strike",
          "Insect Plague", "Blade Barrier", "Harm", "Divine Word",
          "Fire Storm", "Earthquake", "Contagion", "Bane", "Command",
          "Hold Person", "Bestow Curse", "Geas"}
OFFESA_DIRETTA = {"Sacred Flame", "Guiding Bolt", "Inflict Wounds",
                  "Spiritual Weapon", "Spirit Guardians", "Flame Strike",
                  "Blade Barrier", "Harm", "Divine Word", "Fire Storm",
                  "Earthquake", "Insect Plague"}


def carica():
    return [json.load(open(p, encoding="utf-8"))
            for p in sorted(glob.glob(os.path.join(BASE, "divinita", "*.json")))]


def analizza(d):
    sfere = [(x["name"], x["access"]) for x in d["source_2e"]["spheres"]]
    acc = S.accessibili(sfere)
    nomi = {i["name"] for i, _ in acc}
    per_liv = collections.Counter(i["level"] for i, _ in acc)
    vuoti = [l for l in LIVELLI if per_liv[l] == 0]
    scarsi = [l for l in LIVELLI if 0 < per_liv[l] < SOGLIA_PER_LIVELLO]
    dom, motivo = S.DOMINIO[d["id"]]
    return {
        "id": d["id"], "nome": d["name"]["en"], "famiglia": d["family"],
        "sfere_maj": sorted({S.norm(n) for n, a in sfere if a == "major"}),
        "sfere_min": sorted({S.norm(n) for n, a in sfere if a != "major"}),
        "tot": len(acc), "trucchetti": per_liv[0], "per_liv": per_liv,
        "vuoti": vuoti, "scarsi": scarsi, "nomi": nomi,
        "guarigione": sorted(nomi & GUARIGIONE_VERA),
        "guarigione_lato": sorted(nomi & (GUARIGIONE - GUARIGIONE_VERA)),
        "offesa": sorted(nomi & OFFESA_DIRETTA),
        "offesa_lato": sorted(nomi & (OFFESA - OFFESA_DIRETTA)),
        "dominio": dom, "motivo_dominio": motivo,
        "nostre": sum(1 for i, _ in acc if i["derivation"] == "nostra"),
    }


def scheda_divinita(a, tot_base, completo):
    """Scheda di una divinita'. completo=True include le sfere
    maggiori/minori (tabella del manuale): SOLO per la versione privata."""
    r = [f"### {a['nome']}", ""]
    if completo:
        r.append(f"Sfere maggiori: {', '.join(a['sfere_maj'])}. "
                  f"Minori: {', '.join(a['sfere_min']) or 'nessuna'}.")
        r.append("")
    r.append(f"**{a['tot']} incantesimi accessibili** su {tot_base} "
              f"({round(100 * a['tot'] / tot_base)}%), di cui {a['trucchetti']} trucchetti "
              f"e {a['nostre']} da attribuzione nostra.")
    r.append("")
    r.append("| livello | " + " | ".join(f"{l}°" for l in LIVELLI) + " |")
    r.append("|---|" + "---:|" * len(LIVELLI))
    r.append("| incantesimi | " + " | ".join(str(a["per_liv"][l]) for l in LIVELLI) + " |")
    r.append("")
    r.append(f"- Guarigione: {', '.join(a['guarigione']) or '**nessuna cura**'}")
    r.append(f"- Offesa diretta: {', '.join(a['offesa']) or '**nessuna**'}")
    r.append(f"- Dominio: **{a['dominio']}** — {a['motivo_dominio']}")
    r.append("")
    return "\n".join(r)


def interpretativo(testo):
    righe = testo.strip().split("\n")
    return (f"> **Lettura interpretativa** — registrata il {OGGI}. "
            f"Non e' derivata dai dati.\n>\n"
            + "\n".join(f"> {l}" if l else ">" for l in righe))


def main():
    dei = carica()
    A = sorted((analizza(d) for d in dei), key=lambda x: x["tot"])
    n = len(A)
    tot_base = len(S.LISTA_BASE)
    nostre = sum(1 for i in S.LISTA_BASE if i["derivation"] == "nostra")

    per_sfera = collections.Counter(sf for i in S.LISTA_BASE for sf in i["spheres"])
    mai = [x for x in S.SFERE if per_sfera[x] == 0]

    senza_guar = [a for a in A if not a["guarigione"]]
    senza_off = [a for a in A if not a["offesa"]]
    con_vuoti = [a for a in A if a["vuoti"]]
    con_scarsi = [a for a in A if a["scarsi"]]
    senza_truc = [a for a in A if a["trucchetti"] == 0]

    righe_sint = "\n".join(
        f"| {a['nome']} | {a['famiglia']} | {len(a['sfere_maj'])}M/{len(a['sfere_min'])}m | "
        f"{a['tot']} | {a['trucchetti']} | "
        f"{', '.join(str(x) + '°' for x in a['vuoti']) or '—'} | "
        f"{', '.join(str(x) + '°' for x in a['scarsi']) or '—'} | "
        f"{'sì' if a['guarigione'] else '**NO**'} | "
        f"{'sì' if a['offesa'] else '**NO**'} | `{a['dominio']}` |"
        for a in A)

    riga_scarsi = "\n".join(
        "- **{}** — livelli {}.".format(
            a["nome"],
            ", ".join("{}° ({})".format(x, a["per_liv"][x]) for x in a["scarsi"]))
        for a in con_scarsi)

    righe_liv = "\n".join(
        f"| {a['nome']} | " + " | ".join(str(a["per_liv"][l]) for l in LIVELLI)
        + f" | {a['tot'] - a['trucchetti']} |" for a in A)

    tab_sfere = "\n".join(
        f"| {sf} | {per_sfera[sf]} | "
        f"{sum(1 for i in S.LISTA_BASE if sf in i['spheres'] and i['derivation'] == 'fonte')} | "
        f"{sum(1 for d in dei for x in d['source_2e']['spheres'] if S.norm(x['name']) == sf)} |"
        for sf in S.SFERE)

    doc = f"""# Verifica di giocabilità del filtro delle sfere

*Generato da `dati/verifica_sfere.py` il {OGGI}.*

> **Cos'è.** Il conteggio richiesto prima di attivare il filtro della
> decisione 24. Non risolve nulla: non aggiunge sfere, non ammorbidisce il
> filtro, non concede eccezioni. Conta e basta.
>
> Ogni numero è derivato da `dati/divinita/*.json` e da `dati/_sfere_5e.py`.
> Le letture sono marcate e datate.

## Come è stato calcolato

Lista base del chierico **SRD 5.1**: **{tot_base} incantesimi**, {S.LISTA_BASE[0]['level']} trucchetti compresi
({sum(1 for i in S.LISTA_BASE if i['level'] == 0)} trucchetti e {tot_base - sum(1 for i in S.LISTA_BASE if i['level'] == 0)} incantesimi dal 1° al 9°). Gli incantesimi di **Dominio**
non entrano nel conteggio: si ottengono con la sottoclasse e non passano dal
filtro.

**Regola dell'accesso minore**: come in 2e, l'accesso minore concede solo
incantesimi **fino al 3° livello**. È applicata.

**Attribuzioni**: {tot_base - nostre} incantesimi ereditano la sfera da un antenato 2e diretto
(`fonte`); **{nostre} sono attribuzioni nostre** (`nostra`), classificate per effetto e
distinguibili nel dato.

---

## Sintesi

| divinità | famiglia | sfere | incant. | truc. | livelli vuoti | sotto soglia | guarigione | offesa | Dominio |
|---|---|---|---:|---:|---|---|:-:|:-:|---|
{righe_sint}

"Sotto soglia" = meno di {SOGLIA_PER_LIVELLO} incantesimi disponibili a quel livello.
"Guarigione" conta solo le cure vere (Cure Wounds e famiglia), non le
restorazioni. "Offesa" conta solo il danno diretto, non i controlli.

## Incantesimi per livello

| divinità | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° | totale |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{righe_liv}

---

## Il problema è nella mappa, non nelle divinità

| sfera 2e | incantesimi 5e | di cui da antenato | divinità che la possiedono |
|---|---:|---:|---:|
{tab_sfere}

{interpretativo(f'''**{len(mai)} sfera su {len(S.SFERE)} non trova un solo incantesimo nella lista base del chierico
5e: {', '.join(mai)}.** Animal ne trova {per_sfera['Animal']}, Weather {per_sfera['Weather']}. Non è un errore della
mappatura: è che la 5e ha spostato piante, animali e meteo sulla lista del
**druido**, che nel 2014 è una classe separata. In 2e quelle sfere erano
sacerdotali a pieno titolo.

La conseguenza è che le divinità della natura — Chislev, Zeboim, Habbakuk,
Branchala — pagano un prezzo che non dipende dalla loro ricchezza in 2e ma da
dove la 5e ha messo quel materiale. Chislev ha {len([a for a in A if a['id'] == 'chislev'][0]['sfere_maj'])} sfere maggiori, più di quasi
tutti, e tre di quelle sfere valgono in tutto {per_sfera['Animal'] + per_sfera['Plant'] + per_sfera['Weather']} incantesimi.

Questo è materiale per una decisione, non una decisione: le strade possibili
sono attingere alla lista del druido per quelle sfere, accettare lo squilibrio,
o compensare col Dominio. Non ne ho scelta nessuna.''')}

---

## Divinità sotto soglia

### Senza alcuna guarigione vera

{chr(10).join(f"- **{a['nome']}** ({a['famiglia']}) — {a['tot']} incantesimi in tutto. "
              f"Ripieghi disponibili: {', '.join(a['guarigione_lato']) or 'nessuno'}."
              for a in senza_guar) or "Nessuna."}

### Senza alcuna offesa diretta

{chr(10).join(f"- **{a['nome']}** — ripieghi di controllo: {', '.join(a['offesa_lato']) or 'nessuno'}."
              for a in senza_off) or "Nessuna."}

### Con livelli completamente vuoti

{chr(10).join(f"- **{a['nome']}** — vuoti ai livelli {', '.join(str(x) + '°' for x in a['vuoti'])}."
              for a in con_vuoti) or "Nessuna."}

### Con livelli sotto la soglia dei {SOGLIA_PER_LIVELLO} incantesimi

{riga_scarsi or "Nessuna."}

### Senza trucchetti

{chr(10).join(f"- **{a['nome']}**" for a in senza_truc) or "Nessuna."}

---

## Domini assegnati

| divinità | Dominio | nell'SRD 5.1 | motivo |
|---|---|:-:|---|
{chr(10).join(f"| {a['nome']} | {a['dominio']} | "
              f"{'no — ' + S.DOMINI_FUORI_SRD[a['dominio']] if a['dominio'] in S.DOMINI_FUORI_SRD else 'sì'} | "
              f"{a['motivo_dominio']} |" for a in sorted(A, key=lambda x: x['nome']))}

---

## Ambiguità di fonte trovate

- **Due sfere hanno due grafie nel dato**: `Plant`/`Plants` e
  `Necromantic`/`Necromancy`. Sono la stessa sfera. Senza normalizzazione il
  filtro le tratterebbe come distinte e toglierebbe incantesimi a chi le ha
  nella grafia minoritaria — riguarda Zivilyn (`Plant`), Chemosh (`Plant`) e
  Hiddukel (`Necromancy`). Normalizzate in `_sfere_5e.ALIAS`, non nei JSON:
  il dato di fonte resta com'è stato trascritto.
- **Due Domini assegnati non sono nell'SRD 5.1**: Morte (DMG 2014) per Chemosh,
  Morgion e — se si volesse — Takhisis; Forgia (Xanathar) per Reorx. Con solo
  l'SRD servono ripieghi.
- **Nessun Dominio 2014 copre il commercio**: Shinare è assegnata a Inganno per
  esclusione, non per coerenza.
"""
    attribuzioni = ["| incantesimo | liv. | scuola | sfere assegnate | perché |",
                     "|---|---:|---|---|---|"]
    for i in S.LISTA_BASE:
        if i["derivation"] == "nostra":
            attribuzioni.append(f"| {i['name']} | {i['level']} | {i['school']} | "
                                 f"{', '.join(i['spheres'])} | {i['note'] or 'classificato per effetto'} |")

    def scrivi(path, completo):
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc)
            f.write("\n---\n\n## Le attribuzioni nostre\n\n")
            f.write("Incantesimi 5e senza antenato 2e diretto, classificati per "
                    "effetto. Restano distinguibili nel dato con `derivation: nostra`.\n\n")
            f.write("\n".join(attribuzioni))
            f.write("\n\n---\n\n## Schede per divinità\n\n")
            for a in sorted(A, key=lambda x: x["nome"]):
                f.write(scheda_divinita(a, tot_base, completo) + "\n")

    # PUBBLICO: senza le sfere maggiori/minori (tabella del manuale).
    out = os.path.join(BASE, "RAPPORTO-sfere.md")
    scrivi(out, completo=False)

    # PRIVATO: con le sfere. Mai nel pubblico: e' la tabella di Realms Above.
    out_completo = os.path.join(BASE, "RAPPORTO-sfere-completo.md")
    scrivi(out_completo, completo=True)

    for p in (out, out_completo):
        testo = open(p, encoding="utf-8").read()
        print(f"scritto {p} ({len(testo):,} caratteri)".replace(",", "."))
    print(f"{n} divinità | senza cure: {len(senza_guar)} | senza offesa: {len(senza_off)} "
          f"| con livelli vuoti: {len(con_vuoti)} | sotto soglia: {len(con_scarsi)}")
    for a in A[:6]:
        print(f"   {a['nome']:12} {a['tot']:3} inc.  vuoti={a['vuoti']}  scarsi={a['scarsi']}")
    return A


if __name__ == "__main__":
    main()
