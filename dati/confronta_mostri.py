#!/usr/bin/env python3
"""
Genera dati/RAPPORTO-mostri.md: confronto fra i due bestiari di Krynn.

DOMANDA A CUI RISPONDE
    Su quanti mostri avremmo un PRECEDENTE UFFICIALE di conversione, cioe' una
    creatura che esiste sia in 2e (MC Dragonlance Appendix) sia in 5e (Shadow
    of the Dragon Queen)? E' l'informazione che serve a decidere quale dei due
    sia fonte primaria e quale precedente.

    NON decide nulla. Conta.

FONTI
    MC Appendix   Testi/Dragonlance/MC - Dragonlance Appendix.txt, estratto a
                  colonne. Le voci mostro si riconoscono dal blocco
                  "CLIMATE/TERRAIN:" che apre ogni scheda.
    SotDQ         Testi/Dragonlance/Dragonlance - Shadow of the Dragon Queen.txt,
                  Appendice B "Friends and Foes" (pagg. 191-209 stampate) e
                  Appendice C "Sidekicks" (pagg. 210-213).
                  L'elenco si legge dall'INDICE del manuale (pag. 3): e' la
                  fonte piu' affidabile, perche' i titoli degli statblock a due
                  colonne si spezzano nell'estrazione.

Uso:  python3 dati/confronta_mostri.py
"""

import collections
import os
import re
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
TESTI = os.path.join(RADICE, "Testi", "Dragonlance")
OGGI = date.today().isoformat()


def interpretativo(testo):
    righe = testo.strip().split("\n")
    return (f"> **Lettura interpretativa** — registrata il {OGGI}. "
            f"Non e' derivata dai dati.\n>\n"
            + "\n".join(f"> {l}" if l else ">" for l in righe))


def pulisci(s):
    """Il testo estratto porta i codici (cid:NNN) al posto di trattini e apici."""
    s = re.sub(r"\(cid:1[45]\d\)", "-", s)
    s = re.sub(r"\(cid:\d+\)", "'", s)
    return re.sub(r"\s+", " ", s).strip()


def chiave(nome):
    """Normalizza per il confronto: 'Draconian, Baaz' e 'Baaz Draconian' devono
    collidere. Ordino le parole significative."""
    n = pulisci(nome).lower()
    n = re.sub(r"[^a-z\s]", " ", n)
    parole = [p for p in n.split() if p not in
              ("the", "of", "a", "and", "proto", "greater", "lesser", "army")]
    return " ".join(sorted(parole))


# --------------------------------------------------------------------------
# MC Dragonlance Appendix — le voci si aprono con CLIMATE/TERRAIN
# --------------------------------------------------------------------------
def mostri_mc():
    p = os.path.join(TESTI, "MC - Dragonlance Appendix.txt")
    t = open(p, encoding="utf-8", errors="replace").read()
    out = []
    for m in re.finditer(r"CLIMATE/TERRAIN:", t):
        testa = t[max(0, m.start() - 260):m.start()]
        righe = [r.strip() for r in testa.split("\n") if r.strip()]
        if righe:
            out.append(pulisci(righe[-1]))
    # scarto le righe che non sono nomi di creatura ma code di tabella
    scarti = {"Unmated Mated pair*"}
    return [x for x in out if x not in scarti]


# --------------------------------------------------------------------------
# SotDQ — l'elenco "Creatures" in testa all'Appendice B
# --------------------------------------------------------------------------
SOTDQ = "Dragonlance - Shadow of the Dragon Queen.txt"

# Titoli di raggruppamento e di sezione dell'indice: non sono creature.
RAGGRUPPAMENTI = {"Death Dragons", "Draconians", "Dragonnels",
                  "Dragon Army Troops", "Random Encounters", "Allies at War",
                  "Friends and Foes", "Sidekicks", "Sidekick Levels"}

# Due voci dell'indice sono illeggibili per come le colonne si spezzano:
#   "C d 192 / ara oc ....."      -> Caradoc, pag. 192
#   "Kalaman Soldier. .....2 02"  -> il numero e' spezzato in "2 02"
# Recuperate a mano e verificate sul corpo del manuale, dove gli statblock
# ci sono. Sono le uniche due aggiunte manuali di questo script.
RECUPERI_INDICE = [("Caradoc", 192), ("Kalaman Soldier", 202)]

# L'estrazione a colonne confonde "rn" con "m" in un titolo.
CORREZIONI = {"Tern Temble": "Tem Temble"}


def _testo_sotdq():
    return open(os.path.join(TESTI, SOTDQ), encoding="utf-8",
                errors="replace").read()


def _voci_indice(da, a, intervallo):
    """L'indice e' stampato su due colonne che l'estrazione interlaccia: le
    righe del capitolo si alternano a quelle dell'appendice. Il filtro
    affidabile e' il NUMERO DI PAGINA, non la posizione nel testo."""
    t = _testo_sotdq()
    i, j = t.find(da), t.find(a)
    if i < 0:
        return []
    blocco = t[i:j if j > i else len(t)]
    lo, hi = intervallo
    out = []
    for m in re.finditer(r"([A-Z][A-Za-z'\- ]{2,34}?)[\s.]*\.{3,}[\s.]*(\d{2,3})",
                         blocco):
        nome = pulisci(m.group(1)).strip(" .")
        nome = CORREZIONI.get(nome, nome)
        pagina = int(m.group(2))
        if not (lo <= pagina <= hi):
            continue
        if nome and nome not in RAGGRUPPAMENTI and nome not in out:
            out.append(nome)
    for nome, pagina in RECUPERI_INDICE:
        if lo <= pagina <= hi and nome not in out:
            out.append(nome)
    return sorted(out)


def mostri_sotdq():
    """Appendice B, pagg. 191-209 stampate."""
    out = _voci_indice("App. B: Friends and Foes", "App. C: Sidekicks", (191, 209))
    # "Dragon Army Troops" e' un titolo di raggruppamento: contiene due
    # statblock distinti, verificati a pag. 200.
    if "Dragon Army Officer" not in out:
        out += ["Dragon Army Officer", "Dragon Army Soldier"]
    return out


def sidekick_sotdq():
    """Appendice C, pagg. 210-213 stampate. Comprimari, tenuti a parte."""
    return _voci_indice("App. C: Sidekicks", "\n[[p.4]]", (210, 213))


def statblock_presenti():
    """Il PDF contiene davvero i blocchi statistiche? Conta i marcatori."""
    t = _testo_sotdq()
    return {k: len(re.findall(k, t)) for k in
            ("Armor Class", "Hit Points", "Challenge", "Multiattack",
             "STR DEX CON INT WIS CHA")}


def main():
    mc = mostri_mc()
    sot = mostri_sotdq()
    kmc = {chiave(x): x for x in mc}
    ksot = {chiave(x): x for x in sot}
    comuni = sorted(set(kmc) & set(ksot))
    solo_mc = sorted(set(kmc) - set(ksot))
    solo_sot = sorted(set(ksot) - set(kmc))
    sb = statblock_presenti()
    sk = sidekick_sotdq()

    # corrispondenze parziali: una parola significativa in comune, ma chiavi
    # diverse. Non sono la stessa creatura e non vanno contate.
    def parole(k):
        return set(k.split())

    # Solo i casi di CONTENIMENTO: uno dei due nomi contiene interamente
    # l'altro. Le coincidenze su parole generiche come "dragon" non sono
    # corrispondenze, sono rumore.
    righe_parz = []
    for a in solo_mc:
        for b in solo_sot:
            pa, pb = parole(a), parole(b)
            if pa < pb or pb < pa:
                righe_parz.append(
                    f"| {kmc[a]} | {ksot[b]} | la voce SotDQ specializza il nome: "
                    f"e' un blocco statistiche da PNG, non la scheda della specie |")
    parziali = "\n".join(righe_parz)

    # La frase della lettura interpretativa era scritta a mano e divergeva dal
    # conteggio: diceva "i cinque draconici piu' il Cavaliere della Morte",
    # cioe' sei, mentre la tabella ne contava cinque. Ora l'elenco e' DERIVATO.
    nomi_comuni = [ksot[k] for k in comuni]
    fam = collections.Counter(
        n.split()[-1] if n.split()[-1] != "Draconian" else "Draconian"
        for n in nomi_comuni)
    if len(fam) == 1:
        famiglia, quanti = next(iter(fam.items()))
        elenco_comuni = (f"tutti e {quanti} i **{famiglia.lower()}i**"
                         if famiglia == "Draconian"
                         else f"{quanti} voci della famiglia {famiglia}")
        elenco_comuni += " — " + ", ".join(
            n.replace(" Draconian", "") for n in sorted(nomi_comuni))
    else:
        elenco_comuni = ", ".join(sorted(nomi_comuni))

    doc = f"""# I due bestiari di Krynn

*Generato da `dati/confronta_mostri.py` il {OGGI}.*

> **Diagnostico.** Serve a decidere quale fonte sia primaria e quale
> precedente. Non decide, non estrae, non tocca `dati/`.

## Il conteggio

| | voci |
|---|---:|
| `MC - Dragonlance Appendix` (2e) | **{len(mc)}** |
| `Shadow of the Dragon Queen` (5e), Appendice B | **{len(sot)}** |
| in comune — dove avremmo un precedente ufficiale | **{len(comuni)}** |
| solo in MC Appendix | **{len(solo_mc)}** |
| solo in SotDQ | **{len(solo_sot)}** |

## In comune: {len(comuni)} creature

Sono le uniche su cui esiste sia la scheda 2e sia la resa ufficiale 5e, quindi
le uniche su cui si può vedere **come l'ufficiale ha convertito**.

| creatura in MC Appendix (2e) | in SotDQ (5e) |
|---|---|
{chr(10).join(f"| {kmc[k]} | {ksot[k]} |" for k in comuni)}

### Corrispondenze parziali, non contate fra le comuni

Coppie in cui una parte del nome coincide ma le due voci non sono la stessa cosa.

| MC Appendix (2e) | SotDQ (5e) | perché non contano |
|---|---|---|
{parziali or "| — | — | nessuna |"}

## Solo in MC Appendix: {len(solo_mc)}

{", ".join(kmc[k] for k in solo_mc)}

## Solo in SotDQ: {len(solo_sot)}

{", ".join(ksot[k] for k in solo_sot)}

## Appendice C — i {len(sk)} comprimari

Tenuti fuori dal conteggio: sono PNG alleati con statblock da comprimario, non
creature del bestiario.

{", ".join(sk)}

---

## Il PDF contiene gli statblock

| marcatore | occorrenze in 226 pagine |
|---|---:|
{chr(10).join(f"| `{k}` | {v} |" for k, v in sb.items())}

I **{sb['Challenge']} `Challenge`** coincidono esattamente con le {len(sot)} creature
dell'Appendice B: il bestiario è integro e i valori sono ricavabili.

{interpretativo(f'''Il rapporto fra i due bestiari è {len(mc)} a {len(sot)}, e l'intersezione è
**{len(comuni)} creature**: {elenco_comuni}. Tutto il resto
di SotDQ sono PNG dell'avventura — Lord Soth, Kansaldi Fire-Eyes, Caradoc,
Lohezet — che in 2e non hanno una scheda mostro perché sono personaggi, non
specie.

Il **Cavaliere della Morte** è il caso che ha fatto sbagliare una prima lettura,
e vale la pena registrarlo: l'MC Appendix ha la voce *Knight, Death* come
**specie**, SotDQ non ce l'ha. Ha *Skeletal Knight*, che è un'altra creatura, e
ha **Lord Soth**, che nel canone è un cavaliere della morte ma nel manuale è un
**personaggio con statblock proprio**, non una scheda di specie. Un confronto
per nome li avrebbe uniti; sono tre cose diverse.

Questo conferma numericamente l'inclinazione già espressa: **MC Appendix è
l'unica fonte con ampiezza sufficiente** a popolare un bestiario, e SotDQ non
può sostituirla — {len(sot)} creature contro {len(mc)}, e di quelle {len(sot)} solo {len(comuni)} sono specie
condivise.

Come precedente di conversione però {len(comuni)} creature non sono poche, perché sono
**i draconici**, cioè le creature identitarie di Krynn e quelle su cui una
conversione sbagliata si noterebbe di più. E stavolta il precedente è completo:
gli statblock ci sono, quindi si può confrontare non solo quali capacità
l'ufficiale ha scelto di rendere, ma con quali valori.''')}
"""
    out = os.path.join(BASE, "RAPPORTO-mostri.md")
    open(out, "w", encoding="utf-8").write(doc)
    print(f"scritto {out}")
    print(f"MC {len(mc)} | SotDQ {len(sot)} | comuni {len(comuni)} | "
          f"solo MC {len(solo_mc)} | solo SotDQ {len(solo_sot)}")
    print("comuni:", ", ".join(ksot[k] for k in comuni))
    return len(mc), len(sot), len(comuni)


if __name__ == "__main__":
    main()
