#!/usr/bin/env python3
"""
L'arena della fetta verticale: il primo scontro giocato con questi dati.

COSA FA
    Tre scenari, tutti con lo stesso personaggio — un Cavaliere della Corona
    di 2° livello, chassis Fighter, spada lunga e cotta di maglia:

      1. contro il Traag           (turni, multiattacco, danno, morte)
      2. contro il Baaz            (Death Throes, le sue due condizioni)
      3. contro Traag e Baaz insieme

    Di ciascuno stampa il registro completo di uno scontro con seme fissato,
    poi ripete lo scenario mille volte per vedere se l'esito e' stabile o se
    quel singolo registro era un caso fortunato.

COSA MISURA DAVVERO
    Non chi vince. Le LACUNE: ogni volta che il motore ha dovuto supplire a
    un dato assente lo ha dichiarato, e l'elenco in fondo e' il risultato.
    Uno scontro che gira non dimostra che i dati bastano; un elenco di lacune
    vuoto lo dimostrerebbe.

RIDUZIONE — CLAUDE.md, punti 1 e 2
    Un registro di combattimento contiene per forza i numeri di scheda dei
    mostri: Classe Armatura, punti ferita, bonus di attacco, dadi di danno.
    Per il Baaz quei numeri vengono da Shadow of the Dragon Queen, che e' un
    manuale protetto, e per il Traag dalla nostra conversione di una scheda
    dell'MC Appendix: e' esattamente il materiale che `.gitignore` tiene fuori
    dal repository pubblico. Quindi due uscite dalla stessa esecuzione, con la
    riduzione come parametro del generatore e non come taglio a valle:

      dati/RAPPORTO-arena.md           pubblico — metodo, lacune, statistiche
      dati/RAPPORTO-arena-completo.md  privato  — i registri per esteso

    La guardia in fondo verifica che nessuna riga di registro e nessun numero
    di scheda sia finito nel documento pubblico.

Uso:  python3 motore/arena.py            stampa a video ed emette i due rapporti
      python3 motore/arena.py --solo-video
"""

import os
import random
import re
import sys
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from motore import combattimento as C   # noqa: E402

# Il personaggio della fetta. I punteggi sono l'array standard assegnato a
# mano; la scelta e' nostra, non un dato — un personaggio non ha ancora una
# sede in dati/.
PUNTEGGI = {"str": 15, "dex": 13, "con": 14, "int": 10, "wis": 12, "cha": 8}


def eroe(reg, nome="Sir Aldric"):
    return C.pg_fetta(
        razza_id="umano", classe_id="cavaliere-corona", livello=2,
        punteggi=PUNTEGGI, arma_id="longsword", armatura_id="chain-mail",
        scudo_id="shield", stile="Duello", reg=reg, nome=nome)


def scheda(c):
    return (f"{c.nome}: CA {c.ca}, {c.pf_max} punti ferita, "
            f"competenza +{c.competenza}, "
            + " ".join(f"{k.upper()} {v}" for k, v in c.ab.items()))


def qualunque(pg, mostri, esito):
    return True


def col_death_throes(pg, mostri, esito):
    """Il registro da stampare deve MOSTRARE i due tempi del tratto: non basta
    che il Baaz muoia, serve che il tiro salvezza fallisca due volte."""
    return "pietrificato" in pg.condizioni


SCENARI = [
    ("1. Cavaliere della Corona contro Traag", ["traag"], qualunque),
    ("2. Cavaliere della Corona contro Baaz", ["draconico-baaz"], col_death_throes),
    ("3. Cavaliere della Corona contro Traag e Baaz",
     ["traag", "draconico-baaz"], qualunque),
]


def gira(mostri_id, seme, reg=None):
    reg = reg or C.Registro()
    rng = random.Random(seme)
    pg = eroe(reg)
    mostri = [C.da_mostro(m, "mostri", reg) for m in mostri_id]
    esito, round_ = C.scontro([pg], mostri, reg, rng)
    return reg, esito, round_, pg, mostri


RIPETIZIONI = 1000


def esegui():
    """Una sola esecuzione completa: registri dimostrativi + statistiche."""
    seme = 20260902
    scenari = []
    lacune = C.Registro()
    for titolo, mostri_id, voluto in SCENARI:
        # Il seme del registro dimostrativo si cerca, non si sceglie a caso:
        # uno scontro in cui il ramo che si vuole mostrare non si prende non
        # dimostra niente. La ricerca e' dichiarata e il seme e' stampato.
        for tentativo in range(2000):
            reg, esito, round_, pg, mostri = gira(mostri_id, seme + tentativo)
            if voluto(pg, mostri, esito):
                break

        conteggio = collections_Counter()
        round_tot = 0
        pietrificati = 0
        for i in range(RIPETIZIONI):
            r2, e2, rd2, pg2, ms2 = gira(mostri_id, 10_000_000 + i)
            conteggio[e2] += 1
            round_tot += rd2
            if "pietrificato" in pg2.condizioni:
                pietrificati += 1
            for k, v in r2.lacune.items():
                lacune.lacuna(k, *v)

        scenari.append({
            "titolo": titolo, "mostri": mostri_id, "seme": seme + tentativo,
            "registro": reg, "esito": esito, "round": round_,
            "pg": pg, "schede": [pg] + mostri,
            "conteggio": conteggio, "round_medi": round_tot / RIPETIZIONI,
            "pietrificati": pietrificati,
        })
    return scenari, lacune


def collections_Counter():
    import collections
    return collections.Counter()


# ------------------------------------------------------------------ rapporti
def conta_multiattacchi():
    """Quanti blocchi di multiattacco ci sono nel bestiario, e quante azioni."""
    import glob
    import json
    n_multi = n_azioni = 0
    for f in sorted(glob.glob(os.path.join(BASE, "dati", "mostri", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for a in (d["mechanics_5e"].get("actions") or []):
            n_azioni += 1
            if re.search(r"attacchi multipli|multiattack", a["name"], re.I):
                n_multi += 1
    return n_multi, n_azioni


def blocchi_strutturati():
    """Cosa porta un `effetto` e cosa no, nei due mostri della fetta."""
    import json
    fuori = []
    for ident in ("traag", "draconico-baaz"):
        d = json.load(open(os.path.join(BASE, "dati", "mostri", ident + ".json"),
                           encoding="utf-8"))
        m = d["mechanics_5e"]
        for gruppo in ("traits", "actions", "bonus_actions", "reactions"):
            for b in (m.get(gruppo) or []):
                fuori.append((d["name"]["it"], gruppo, b["name"],
                              b.get("effetto") is not None,
                              sorted(k for k in (b.get("effetto") or {})
                                     if k not in ("nota", "azione"))))
    return fuori


def tabella(intestazioni, righe, allin=None):
    allin = allin or ["---"] * len(intestazioni)
    return "\n".join(
        ["| " + " | ".join(intestazioni) + " |",
         "|" + "|".join(allin) + "|"]
        + ["| " + " | ".join(str(x) for x in r) + " |" for r in righe])


def rapporto(scenari, lacune, completo):
    oggi = date.today().isoformat()
    blocchi = blocchi_strutturati()
    n_multi, n_azioni = conta_multiattacchi()
    con = [b for b in blocchi if b[3]]
    senza = [b for b in blocchi if not b[3]]

    esiti = []
    for s in scenari:
        n = sum(s["conteggio"].values())
        esiti.append([
            s["titolo"].split(". ", 1)[1],
            ", ".join(f"{k} {100 * v // n}%" for k, v in
                      sorted(s["conteggio"].items(), key=lambda x: -x[1])),
            f"{s['round_medi']:.1f}".replace(".", ","),
            f"{100 * s['pietrificati'] / n:.1f}".replace(".", ",") + "%",
        ])

    testa = f"""# L'arena della fetta verticale — i dati usati per la prima volta

*Generato da `motore/arena.py` il {oggi}.{" **VERSIONE COMPLETA, PRIVATA**: contiene i registri di combattimento con i numeri di scheda dei mostri." if completo else ""}*

---

## 0. Cosa è stato provato

Tre anni di conversione hanno prodotto dati validati da ogni lato: schemi,
validatori incrociati, verifica degli strati, confronto fra prosa e struttura.
Nessuno di quei controlli chiede la sola cosa che conta — che con questi dati
si possa giocare un turno.

`motore/combattimento.py` lo chiede. Legge `mechanics_5e...effetto` dei mostri,
`dati/condizioni/`, `dati/oggetti/` e i privilegi del chassis, e gioca uno
scontro a turni con iniziativa, azioni, danno, morte e condizioni.

**Non misura chi vince. Misura le lacune.** Ogni volta che il motore ha
bisogno di qualcosa che i dati non portano, lo dichiara e va avanti con
un'assunzione scritta. Senza quel registro un simulatore mente: gira sempre,
perché ogni valore assente diventa uno zero e ogni regola assente diventa un
ramo che non si prende. È la stessa forma del difetto che la categoria d'arma
ha reso visibile — un buco che sembra un dato.

> **Lo scontro gira. Con {len(lacune.lacune)} lacune dichiarate.**

---

## 1. Cosa è stato strutturato

`mostro.schema.json` aveva `additionalProperties: false` su `elemento_5e` e
nessun campo `effetto`: **lo strato strutturato non era nemmeno esprimibile
sui mostri.** Aperto, con la stessa forma e la stessa nota del campo omonimo
in `classe.schema.json`.

{tabella(["creatura", "gruppo", "blocco", "`effetto`"],
         [[m, g, n, ("**" + ", ".join(k) + "**") if ha else "—"]
          for m, g, n, ha, k in blocchi])}

**{len(con)} blocchi su {len(blocchi)}** hanno una meccanica leggibile da un
motore. Gli altri {len(senza)} restano prosa — ed è già un risultato, perché
prima della fetta erano prosa tutti e {len(blocchi)}, su 257 del bestiario.

### Due estensioni di schema, entrambe imposte da un caso

`multiattacco` — il blocco *Attacchi Multipli* dice una cosa meccanica e non
aveva nessun campo in cui dirla: la sua sola forma era la frase «effettua due
attacchi con X». Nel bestiario sono **{n_multi} blocchi su {n_azioni} azioni**,
e un motore che li ignorasse dimezzerebbe il danno per round di ognuno di quei
mostri senza che nessun controllo se ne accorga. Il campo riferisce l'azione
ripetuta per nome e non ne ricopia i numeri; `valida_effetti.py` verifica che
il nome esista nello stesso statblock.

`tiro_salvezza.fallimento_ripetuto` — il Death Throes del Baaz è un effetto a
**due tempi**: il primo fallimento trattiene mentre la pietrificazione
comincia, il secondo la compie. Lo schema aveva `ripetibile`, che dice *quando*
si ritira e non *cosa succede*. Senza il campo nuovo, le due condizioni di quel
tratto diventano una sola — cioè il tratto perde metà di sé senza che nessun
controllo se ne accorga.

### Due condizioni nuove, per lo stesso motivo

`trattenuto` e `pietrificato` non esistevano. `build_condizioni.py` dichiarava
il criterio — *si aggiungono quando un blocco convertito le riferisce davvero* —
e questa è la prima volta che il criterio si applica invece di essere
enunciato. Sono cinque, non quindici.

`pietrificato` porta con sé una domanda che il motore ha dovuto risolvere: una
creatura pietrificata **non è morta**, ha ancora i suoi punti ferita e resiste
a tutti i danni. La condizione di fine scontro non può quindi essere «ogni
avversario a 0 punti ferita», ed è una definizione che nessun dato dichiara.

---

## 2. Gli scenari

{tabella(["scenario", "esiti su " + str(RIPETIZIONI) + " scontri", "round medi", "PG pietrificato"],
         esiti, ["---", "---", "--:", "--:"])}

«nessuno» è l'esito in cui il personaggio uccide il Baaz e il Death Throes lo
pietrifica: entrambe le parti fuori dallo scontro, nessuna morta. È il caso che
un motore scritto sull'assunzione «vince chi resta in piedi» non saprebbe
classificare.
"""

    if completo:
        for s in scenari:
            testa += f"""
---

## Registro — {s['titolo']}

Seme {s['seme']}. Esito: {s['esito']}, al round {s['round']}.

```
""" + "\n".join(scheda(c) for c in s["schede"]) + "\n\n" + s["registro"].stampa() + "\n```\n"

    testa += f"""
---

## 3. Le {len(lacune.lacune)} lacune

Ognuna è un punto in cui il motore ha supplito ai dati. Sono l'esito vero di
questa prova.

"""
    for i, (codice, (cosa, ass)) in enumerate(lacune.lacune.items(), 1):
        testa += f"**{i}. `{codice}`** — {cosa}\n\n> {ass}\n\n"

    testa += """---

## 4. Cosa si è rotto, in ordine di peso

**Il personaggio non è un dato.** Sul mostro l'attacco è un campo; sul
personaggio è una funzione di `motore/combattimento.py`, e vive solo lì. Classe
Armatura, punti ferita, bonus di attacco, danno: tutti composti a runtime da
razza + classe + oggetto + stile di combattimento, con la procedura scritta nel
motore. È la lacuna più grande e non sorprende — lo schema Personaggio non
esiste. Sorprende *quanto* di ciò che serve non sia da nessuna parte: la regola
dei punti ferita al 1° livello, il bonus di iniziativa, la competenza applicata
all'arma.

**Non c'è una sede per le regole di sistema.** La decisione 41
(`sconfessione-condivisa`) l'aveva già registrato, e `dati/condizioni/` è stata
la prima risposta. Questo è il secondo caso e pesa di più: *d20 + bonus contro
la Classe Armatura, 20 naturale critico, 1 naturale mancato d'ufficio* sta
scritto in un file Python e in nessun dato. Lo stesso vale per la struttura del
round, l'economia delle azioni e la condizione di fine scontro.

**Un innesco non ha un campo.** `azione: nessuna` significa *non costa
un'azione*, non *scatta a 0 punti ferita*. Il motore riconosce il Death Throes
**dal nome**, che è l'unico appiglio che i dati offrono. Ogni tratto che
scatta a una condizione — alla morte, quando si viene colpiti, all'inizio del
turno — oggi è indistinguibile da un tratto passivo.

**Non c'è posizione.** `portata_ft` e `gittata_ft` sono campi popolati e mai
letti: senza distanze un'arma da mischia e una a distanza si comportano
uguale. La conseguenza si vede sul Death Throes, che la fonte dichiara «ogni
creatura entro 5 piedi» e che il motore applica a tutti gli avversari e a
nessun alleato — un errore di regola, dichiarato.

**L'assenza di `effetto` dice due cose diverse.** *Non ha meccanica* e *non è
ancora strutturato* si scrivono uguali. `esito.nessuno` esiste proprio per
questa distinzione, un livello più in basso; al livello del blocco non c'è.
La *Dissoluzione post mortem* del Traag è il caso: la fonte dichiara
esplicitamente che non succede niente, e nei dati è indistinguibile da un
blocco non convertito.

**Il morale non entra in campo.** La decisione 27 (`sette-campi-2e`) lo destina
all'IA di combattimento e ogni mostro lo porta in `morale_2e`. Nessuno lo
legge, e i mostri combattono fino alla morte — «irrealistico, e macchinoso da
giocare», dice quella stessa decisione. Il Traag è il caso peggiore: il suo
morale ha due stati, e ignorarlo cancella il suo tratto identitario.

**Due vocabolari per i tipi di danno.** `dati/oggetti/` li porta in inglese
(`slashing`, dall'SRD), `dati/mostri/` in italiano (`perforante`). Nessuno dei
due schemi li vincola. Un motore che confronti un tipo di danno con una
resistenza li manca tutti, e nessun validatore lo vede perché nessuno dei due
è sbagliato dal proprio lato. È una struttura doppia della stessa famiglia
delle sei già chiuse, e non è stata trovata ispezionando i dati: è stata
trovata usandoli.

---

*Nessuna decisione è presa in questo documento. Le due estensioni di schema e
le due condizioni nuove sono la condizione perché lo scontro esistesse, non
una scelta di progetto: senza, il Death Throes non era esprimibile e il
multiattacco non era leggibile.*
"""
    return testa


def guardia_riduzione(pubblico, scenari):
    """Nessuna riga di registro e nessun numero di scheda nel pubblico."""
    fuori = []
    for s in scenari:
        for riga in s["registro"].righe:
            r = riga.strip()
            if len(r) > 25 and r in pubblico:
                fuori.append(("registro", r[:60]))
        for c in s["schede"]:
            if getattr(c, "giocante", False):
                continue
            for etichetta, valore in (("CA", c.ca), ("PF", c.pf_max)):
                if re.search(rf"{c.nome}[^\n]*\b{valore}\b", pubblico):
                    fuori.append((f"{c.nome} {etichetta}", str(valore)))
    return fuori


PUBBLICO = os.path.join(BASE, "dati", "RAPPORTO-arena.md")
PRIVATO = os.path.join(BASE, "dati", "RAPPORTO-arena-completo.md")


def main(argv):
    scenari, lacune = esegui()

    for s in scenari:
        print("\n" + "=" * 72)
        print(s["titolo"])
        print("=" * 72 + "\n")
        for c in s["schede"]:
            print(scheda(c))
        print()
        print(s["registro"].stampa())
        print(f"\nEsito: {s['esito']}, al round {s['round']}. Seme: {s['seme']}")
        n = sum(s["conteggio"].values())
        print(f"{n} ripetizioni: "
              + ", ".join(f"{k} {v} ({100 * v // n}%)" for k, v in
                          sorted(s["conteggio"].items(), key=lambda x: -x[1]))
              + f"; durata media {s['round_medi']:.1f} round")
        if s["pietrificati"]:
            print(f"personaggio pietrificato dal Death Throes: "
                  f"{s['pietrificati']}/{n}")

    print("\n" + "=" * 72)
    print(f"LACUNE — {len(lacune.lacune)} cose che il motore ha supplito ai dati")
    print("=" * 72)
    for i, (codice, (cosa, ass)) in enumerate(lacune.lacune.items(), 1):
        print(f"\n{i:2d}. [{codice}]\n    {cosa}\n    → {ass}")

    if "--solo-video" in argv:
        return 0

    doc_pubblico = rapporto(scenari, lacune, completo=False)
    fuori = guardia_riduzione(doc_pubblico, scenari)
    if fuori:
        print("\nRIDUZIONE FALLITA — materiale di scheda nel rapporto pubblico:")
        for che, pezzo in fuori[:10]:
            print(f"  {che}: {pezzo}")
        return 1
    open(PUBBLICO, "w", encoding="utf-8").write(doc_pubblico)
    open(PRIVATO, "w", encoding="utf-8").write(
        rapporto(scenari, lacune, completo=True))
    print(f"\nscritto dati/RAPPORTO-arena.md ({len(doc_pubblico.splitlines())} righe)")
    print("scritto dati/RAPPORTO-arena-completo.md (privato, con i registri)")
    print("guardia di riduzione: nessuna riga di registro, nessun numero di "
          "scheda dei mostri nel pubblico")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
