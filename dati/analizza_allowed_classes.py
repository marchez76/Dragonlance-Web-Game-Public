#!/usr/bin/env python3
"""
La mappa di `allowed_classes`: 17 etichette del PHB 2e contro 17 nostre classi.

PERCHE' ESISTE. Le razze dichiarano quali classi possono prendere, e lo
dichiarano con le **etichette del manuale 2e**. Il nostro roster e' un altro
elenco, nato da un'altra strada. Fra i due non c'e' un ponte: `Fighter` e'
concessa da quasi tutte le razze e non ha nulla cui agganciarsi, perche' il
roster ha Cavaliere, Barbaro e Marinaio ma non un guerriero generico.

QUESTO DOCUMENTO NON DECIDE. Porta la mappa perche' la decisione si prenda
guardandola: per ciascuna etichetta, quale nostra classe la copre, per quale
via, e a che prezzo. Le tre vie sono tenute separate perche' costano cose
diverse — una coincidenza di nome non chiede niente a nessuno, una copertura
per chassis chiede di stabilire che l'etichetta nomina un **telaio** e non una
classe, e un'etichetta senza copertura chiede di scegliere fra togliere
l'accesso alla razza e aggiungere una classe.

IL VERSO OPPOSTO E' PARTE DELLA DOMANDA, non un'aggiunta: una nostra classe
che nessuna razza dichiara di poter prendere e' una classe **ingiocabile**, e
finche' nessuno guarda la mappa dal lato delle classi non si vede.

COSA E' DERIVATO E COSA E' EDITORIALE, dichiarato perche' non si confonda:
- i conteggi, le etichette, il roster, i chassis: **letti dai dati**;
- la somiglianza fra un'etichetta e un nome: **calcolata** sulle parole;
- a quale telaio 5e corrisponde un'etichetta 2e: **editoriale**, in
  `TELAIO_DELL_ETICHETTA`, una riga per etichetta con la sua ragione.

Uso:  python3 dati/analizza_allowed_classes.py
"""

import collections
import glob
import json
import os
import re
import sys
import textwrap

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
sys.path.insert(0, BASE)
sys.path.insert(0, RADICE)

import _srd51 as SRD  # noqa: E402
from decisioni import cita  # noqa: E402

# Parole che non distinguono: compaiono in mezzo roster e in mezze etichette,
# quindi un accostamento che si regge solo su queste non e' un accostamento.
VUOTE = {"of", "the", "and", "a", "stars", "wizard", "priest", "knight"}

# A QUALE TELAIO 5e CORRISPONDE UN'ETICHETTA 2e — editoriale, e per questo
# scritto in chiaro con la ragione accanto invece che dedotto in silenzio.
# `None` vuol dire che il telaio non esiste fra quelli che abbiamo: e' un
# fatto diverso da "l'etichetta non ha corrispondenza", e va tenuto distinto.
TELAIO_DELL_ETICHETTA = {
    "Barbarian": ("Fighter", "guerriero senza addestramento cavalleresco; l'Ira "
                             "e' un'invenzione della 3e, assente da Krynn"),
    "Bard":      (None, "il Bardo SRD esiste nella 5e ma non fra i cinque "
                        "telai che abbiamo trascritto"),
    "Cavalier":  ("Fighter", "guerriero a cavallo, telaio marziale puro"),
    "Druid (heathen)": (None, "il Druido SRD esiste nella 5e ma non fra i "
                              "cinque telai che abbiamo trascritto"),
    "Fighter":   ("Fighter", "e' il telaio, non una classe del nostro roster"),
    "Handler":   ("Rogue", "abilita' del ladro applicate al baratto kender"),
    "High Sorcerer": ("Wizard", "incantatore arcano a preparazione"),
    "Holy Orders": ("Cleric", "incantatore divino, e' il nome 2e dell'ordine "
                              "sacerdotale di Krynn"),
    "Illusionist": ("Wizard", "specialista arcano: nella 5e e' una "
                              "sottoclasse del Mago, non una classe"),
    "Knight of Solamnia": ("Paladin", "l'ombrello dei tre ordini cavallereschi; "
                                      "due dei tre stanno su telaio Paladin"),
    "Mage (Renegade)": ("Wizard", "incantatore arcano fuori dagli Ordini"),
    "Mariner":   ("Fighter", "guerriero di mare"),
    "Paladin":   ("Paladin", "e' il telaio, non una classe del nostro roster"),
    "Priest (heathen)": ("Cleric", "incantatore divino fuori dagli Ordini"),
    "Ranger":    (None, "il Ranger SRD esiste nella 5e ma non fra i cinque "
                        "telai che abbiamo trascritto"),
    "Thief":     ("Rogue", "e' il telaio, non una classe del nostro roster"),
    "Tinker":    (None, "non ha un telaio 5e: e' un'invenzione di Krynn"),
}


def _parole(s):
    return {p for p in re.split(r"[^a-z]+", (s or "").lower()) if p} - VUOTE


def razze():
    """(id, allowed_classes) per ogni razza, in ordine."""
    out = []
    for f in sorted(glob.glob(os.path.join(BASE, "razze", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        out.append((d["id"], (d.get("mechanics_5e") or {}).get("allowed_classes") or {}))
    return out


def classi():
    """(id, nome inglese, telaio, gruppo, stato, requires_class).

    `requires_class` non e' un dettaglio: una classe che si prende **da**
    un'altra non e' raggiunta dalle razze e non per questo e' ingiocabile —
    ci si arriva passando per la classe che la richiede. Confondere i due
    casi farebbe contare come irraggiungibili le tre Vesti, che sono avanzamenti
    del Mago dell'Alta Stregoneria."""
    out = []
    for f in sorted(glob.glob(os.path.join(BASE, "classi", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        m = d.get("mechanics_5e") or {}
        out.append((d["id"], (d.get("name") or {}).get("en") or d["id"],
                    (m.get("chassis") or {}).get("srd_class"),
                    d.get("group"), m.get("conversion_status"),
                    d.get("requires_class")))
    return out


def etichette(rz):
    """Ogni etichetta 2e con quante razze la concedono."""
    c = collections.Counter()
    for _r, ac in rz:
        for e in (ac.get("classes") or []):
            c[e] += 1
    return c


def copertura(et, cl):
    """Per ogni etichetta: chi la copre per nome, chi per telaio, e il verso.

    Tre vie, tenute separate perche' non costano lo stesso:
      "nome"   il nome inglese di una nostra classe coincide con l'etichetta;
      "parole" condivide almeno una parola che distingue (non `of`, `the`...);
      "telaio" nessuna parola in comune, ma la nostra classe sta sul telaio
               5e che l'etichetta nomina — vale SOLO se si decide che
               l'etichetta nomina un telaio e non una classe.
    Un'etichetta puo' essere coperta per piu' vie insieme: quella che conta e'
    la piu' economica, ed e' l'ordine in cui sono elencate."""
    righe = []
    for e in sorted(et):
        telaio, ragione = TELAIO_DELL_ETICHETTA.get(e, (None, "non classificata"))
        pe = _parole(e)
        nome = [c for c in cl if (c[1] or "").lower() == e.lower()]
        parole = [c for c in cl if c not in nome and _parole(c[1]) & pe]
        comuni = sorted(set().union(*[_parole(c[1]) & pe for c in parole])
                        ) if parole else []
        per_telaio = [c for c in cl
                      if c not in nome and c not in parole
                      and telaio and c[2] == telaio]
        via = ("nome" if nome else "parole" if parole
               else "telaio" if per_telaio else "scoperta")
        righe.append((e, et[e], via, nome, parole, per_telaio, telaio,
                      ragione, comuni))
    return righe


def ingiocabili(cop, cl):
    """Le nostre classi che nessuna etichetta raggiunge, per nessuna via."""
    raggiunte = collections.defaultdict(set)
    for e, _n, _v, nome, parole, tel, _t, _r, _p in cop:
        for c in nome:
            raggiunte[c[0]].add((e, "nome"))
        for c in parole:
            raggiunte[c[0]].add((e, "parole"))
        for c in tel:
            raggiunte[c[0]].add((e, "telaio"))
    return [(c, sorted(raggiunte[c[0]])) for c in cl], raggiunte


# ---------------------------------------------------------------- rendering

def riflow(testo, larghezza=78):
    fuori = []
    for blocco in testo.split("\n\n"):
        righe = blocco.split("\n")
        if any(r.lstrip().startswith(("|", "#", ">", "-", "*Generato"))
               or r.startswith("    ") or r.strip() in ("---", "")
               for r in righe):
            fuori.append(blocco)
            continue
        fuori.append(textwrap.fill(" ".join(r.strip() for r in righe),
                                   width=larghezza, break_long_words=False,
                                   break_on_hyphens=False))
    return "\n\n".join(fuori)


def tabella(intestazioni, righe, allin=None):
    allin = allin or ["---"] * len(intestazioni)
    return "\n".join(
        ["| " + " | ".join(intestazioni) + " |",
         "|" + "|".join(allin) + "|"]
        + ["| " + " | ".join(str(x) for x in r) + " |" for r in righe])


def rapporto():
    rz = razze()
    cl = classi()
    et = etichette(rz)
    cop = copertura(et, cl)
    per_classe, raggiunte = ingiocabili(cop, cl)

    n_raz = len(rz)
    applicate = [r for r, ac in rz if ac.get("applied")]
    non_applicate = [(r, ac) for r, ac in rz if not ac.get("applied")]
    telai = sorted(SRD.TABELLE)
    telai_usati = sorted({c[2] for c in cl if c[2]})

    per_via = collections.Counter(v for _e, _n, v, _a, _b, _c, _t, _r, _p in cop)
    scoperte = [r for r in cop if r[2] == "scoperta"]
    senza_telaio = [r for r in cop if r[6] is None]
    mute = [c for c in cl if not raggiunte[c[0]]]
    # DUE COSE DIVERSE, e contarle insieme darebbe un numero falso: una classe
    # che si prende DA un'altra non deve essere raggiunta dalle razze — ci si
    # arriva per la classe che la richiede. Restano ingiocabili solo quelle
    # che non sono raggiunte NE' dalle razze NE' da un avanzamento.
    avanzamenti = [c for c in mute if c[5]]
    irraggiungibili = [c for c in mute if not c[5]]
    # ...e un avanzamento e' davvero raggiungibile solo se la classe da cui si
    # entra lo e' a sua volta. La catena si risale finche' regge.
    ok = {c[0] for c in cl if raggiunte[c[0]]}
    cresce = True
    while cresce:
        cresce = False
        for c in avanzamenti:
            if c[0] not in ok and c[5] in ok:
                ok.add(c[0])
                cresce = True
    orfani = [c for c in avanzamenti if c[0] not in ok]

    P = []
    P.append(f"""# `allowed_classes` — la mappa fra {len(et)} etichette 2e e {len(cl)} nostre classi

*Generato da `dati/analizza_allowed_classes.py`. **Questo documento non
decide**: porta la mappa perche' la decisione si prenda guardandola.*

---

## 0. Perche' non manca un campo

`allowed_classes` c'e', e' compilato su {len(applicate)} razze su {n_raz}, e
non gli manca niente. Manca il **ponte**: le razze dichiarano le classi con le
etichette del PHB 2e, il roster e' nato da un'altra strada, e fra i due
elenchi non esiste una regola di traduzione scritta da nessuna parte. Finche'
non c'e', la prima domanda della creazione di un personaggio — *quali classi
puo' prendere questa razza* — non ha una risposta calcolabile.

Il caso che lo mostra meglio e' `Fighter`: e' l'etichetta piu' concessa
({et.get('Fighter', 0)} razze su {n_raz}) e nel roster **non esiste una classe
con quel nome**. Il roster ha Cavaliere, Barbaro, Marinaio — tutte cose che un
guerriero fa — e nessun guerriero generico. Quindi o `Fighter` non nomina una
classe ma un **telaio**, e allora la traduzione passa per i chassis, oppure
{et.get('Fighter', 0)} razze concedono una classe che non esiste.
""")

    # ------------------------------------------------------------------ §1
    P.append(f"""---

## 1. Le due sponde

**{len(et)} etichette** distinte, dichiarate dalle razze:

{tabella(["etichetta 2e", "razze che la concedono"],
         [(f"`{e}`", n) for e, n in et.most_common()],
         allin=["---", "--:"])}

**{len(cl)} classi** nel roster, con il telaio 5e su cui ciascuna sta:

{tabella(["nostra classe", "nome inglese", "gruppo", "telaio 5e", "stato", "si entra da"],
         [(f"`{i}`", n, g or "—", f"`{t}`" if t else "**nessuno**", s,
           f"`{rq}`" if rq else "—")
          for i, n, t, g, s, rq in cl])}

I telai disponibili sono {len(telai)} — {", ".join(f"`{t}`" for t in telai)} —
e sono quelli, non tutti quelli della 5e: sono i cinque di cui abbiamo
trascritto i privilegi. Di questi il roster ne usa {len(telai_usati)}
({", ".join(f"`{t}`" for t in telai_usati)}).
{len([c for c in cl if not c[2]])} nostre classi non hanno ancora un telaio, e
{len([c for c in cl if c[5]])} non si prendono alla creazione: si entra da
un'altra classe, quindi non e' dalle razze che devono essere raggiunte.
""")

    # ------------------------------------------------------------------ §2
    def elenco(cs):
        return ", ".join(f"`{c[0]}`" for c in cs) or "—"

    P.append(f"""---

## 2. La mappa, etichetta per etichetta

Tre vie di copertura, in ordine di costo crescente. **Nome**: il nome inglese
di una nostra classe coincide con l'etichetta, e non c'e' niente da decidere.
**Parole**: condivide almeno una parola che distingue, e va confermata a
occhio una volta. **Telaio**: nessuna parola in comune, ma la nostra classe
sta sul telaio 5e che l'etichetta nomina — e vale **solo** se si decide che
l'etichetta nomina un telaio e non una classe. **Scoperta**: nessuna delle
tre.

{tabella(["etichetta", "razze", "via", "per nome / parole", "parole in comune",
          "in piu' se e' un telaio", "telaio"],
         [(f"`{e}`", n, v, elenco(nome + parole),
           ", ".join(f"`{w}`" for w in pw) or "—", elenco(tel),
           f"`{t}`" if t else "**nessuno**")
          for e, n, v, nome, parole, tel, t, _r, pw in cop],
         allin=["---", "--:", "---", "---", "---", "---", "---"])}

La colonna **in piu' se e' un telaio** non e' una via alternativa: e' cosa si
aggiungerebbe *oltre* alla copertura gia' trovata, se si decidesse che
l'etichetta nomina il telaio. Per `Barbarian` significa che l'accesso
passerebbe dal solo Barbaro a tre classi.

La colonna **parole in comune** e' li' perche' un accostamento per parole va
guardato, non contato. `Druid (heathen)` e `Heathen Priest` condividono
`heathen` e nient'altro: un druido e un sacerdote non sono la stessa cosa
nemmeno nella 2e, e questo e' l'accostamento piu' debole della tabella.

Conteggio per via: {", ".join(f"**{v}** {n}" for v, n in per_via.most_common())}.

### Le ragioni del telaio, che sono editoriali e non derivate

{tabella(["etichetta", "telaio", "perche'"],
         [(f"`{e}`", f"`{t}`" if t else "**nessuno**", r)
          for e, _n, _v, _a, _b, _c, t, r, _p in cop])}
""")

    # ------------------------------------------------------------------ §3
    P.append(f"""---

## 3. I tre casi che chiedono una decisione diversa

### 3a. Le etichette che il telaio salva — {per_via.get('telaio', 0)} su {len(et)}

Sono le etichette senza nessuna parola in comune col roster, ma con un telaio
che il roster usa. Se si decide che **un'etichetta 2e nomina un telaio**,
queste si risolvono tutte insieme e senza aggiungere classi:

{tabella(["etichetta", "razze", "classi che il telaio le da'"],
         [(f"`{e}`", n, elenco(tel))
          for e, n, v, _a, _b, tel, _t, _r, _p in cop if v == "telaio"],
         allin=["---", "--:", "---"]) if per_via.get("telaio") else "*(nessuna)*"}

Il prezzo di questa lettura va detto: `Fighter` concessa a una razza
diventerebbe l'accesso a **{len([c for c in cl if c[2] == 'Fighter'])} classi
diverse** insieme, fra cui il Cavaliere della Corona, che nella 2e ha
restrizioni di razza sue. La traduzione per telaio e' generosa, e dove la
fonte era piu' stretta lo diventa in silenzio: e' il punto in cui la
{cita('doppio-strato')} chiede che lo scarto sia dichiarato, non assorbito.

### 3b. Le etichette senza telaio — {len(senza_telaio)} su {len(et)}

{tabella(["etichetta", "razze", "perche' nessun telaio"],
         [(f"`{e}`", n, r) for e, n, _v, _a, _b, _c, t, r, _p in cop if t is None],
         allin=["---", "--:", "---"])}

Qui la domanda cambia forma. Per {", ".join(f"`{e}`" for e, _n, _v, _a, _b, _c, t, _r, _p in cop if t is None and _parole(e) & {"bard", "druid", "ranger"})}
il telaio esiste nella 5e e **non l'abbiamo trascritto**: e' lavoro noto, non
una decisione di conversione. Per le altre non esiste affatto, e allora
delle due l'una — la razza perde quell'accesso, o manca una classe.

### 3c. Le etichette scoperte — {len(scoperte)} su {len(et)}

{tabella(["etichetta", "razze concedenti", "telaio dichiarato"],
         [(f"`{e}`", n, f"`{t}`" if t else "**nessuno**")
          for e, n, _v, _a, _b, _c, t, _r, _p in scoperte],
         allin=["---", "--:", "---"]) if scoperte else "*(nessuna: ogni etichetta ha almeno una via)*"}
""")

    # ------------------------------------------------------------------ §4
    P.append(f"""---

## 4. Il verso opposto: le classi che nessuna razza puo' prendere

{tabella(["nostra classe", "telaio", "si entra da", "etichette che la raggiungono",
          "per quale via"],
         [(f"`{c[0]}`", f"`{c[2]}`" if c[2] else "—",
           f"`{c[5]}`" if c[5] else "—",
           ", ".join(f"`{e}`" for e, _v in vs) or "**NESSUNA**",
           ", ".join(sorted({v for _e, v in vs})) or "—")
          for c, vs in per_classe])}

**{len(mute)} classi su {len(cl)} non sono raggiunte da nessuna etichetta**, e
non sono lo stesso caso. Contarle insieme darebbe un numero falso:

{tabella(["classe", "si entra da", "verdetto"],
         [(f"`{c[0]}` ({c[1]})",
           f"`{c[5]}`" if c[5] else "— nessuna",
           ("**avanzamento**, raggiungibile per la classe che lo richiede"
            if c[5] and c[0] in ok else
            "**avanzamento orfano**: anche la classe da cui si entra e' muta"
            if c[5] else "**INGIOCABILE**"))
          for c in mute])}

- **{len(avanzamenti) - len(orfani)} sono avanzamenti**: non devono essere
  dichiarati dalle razze, ci si arriva dalla classe che li richiede — le tre
  Vesti si prendono dal Mago dell'Alta Stregoneria, che le razze raggiungono.
  Che `allowed_classes` non le nomini e' **giusto**, non un buco.
- **{len(irraggiungibili)}** {"non e' raggiunta" if len(irraggiungibili) == 1 else "non sono raggiunte"}
  **da niente**: {", ".join(f"`{c[0]}`" for c in irraggiungibili) or "*(nessuna)*"}.
- **{len(orfani)} avanzamenti orfani**{":" if orfani else " — nessuno: ogni catena di ingresso comincia da una classe che almeno una razza concede."}
  {(", ".join(f"`{c[0]}`" for c in orfani) + " — la catena di ingresso c'e', ma comincia da una classe che nessuna razza concede.") if orfani else ""}

Una classe raggiungibile da nessuna delle due vie e' **ingiocabile**, e non e'
un difetto astratto: e' una scheda scritta, validata e irraggiungibile. Vale
la pena saperlo **prima** di scrivere lo schema del Personaggio, perche' lo
schema non puo' dirlo — un campo `classe` valido non sa che nessuno potra'
sceglierlo. E la distinzione fra le due colonne e' esattamente il tipo di cosa
che uno schema non vede e un controllo si': la raggiungibilita' non e' una
proprieta' di un file, e' una proprieta' del **grafo** fra due famiglie.
""")

    # ------------------------------------------------------------------ §5
    P.append(f"""---

## 5. Le {len(non_applicate)} razze senza elenco, e una che non torna

{tabella(["razza", "applied", "classes"],
         [(f"`{r}`", str(ac.get("applied")),
           "null" if ac.get("classes") is None else str(ac.get("classes")))
          for r, ac in non_applicate])}

Per gli umani il vuoto ha una ragione dichiarata e giusta: la
{cita('vincoli-caratteristica')} preclude le classi assenti dalla tabella del
manuale, e il manuale gli umani non li elenca affatto — nessuna riga, quindi
nessuna preclusione. La nota nel dato dice esattamente questo.

**`elfo-dargonesti` porta lo stesso `applied: false` e la stessa nota, e la
nota non lo riguarda**: non e' una razza che il manuale non elenca, e la
ragione scritta accanto vale solo per gli umani. E' una nota copiata su un
caso che non e' quello, ed e' la forma piu' silenziosa della struttura doppia:
il campo e' compilato, il controllo passa, e la spiegazione e' di un altro. Va
sciolto guardando la fonte — o l'elfo Dargonesti ha un elenco che non e' stato
trascritto, o ha una ragione sua per non averlo, e in entrambi i casi la nota
va riscritta.

---

## 6. Cosa serve decidere, in ordine

1. **Un'etichetta 2e nomina una classe o un telaio?** E' la domanda che
   scioglie {per_via.get('telaio', 0)} etichette in un colpo e ne lascia
   {len(senza_telaio)} aperte. Il sospetto che la risposta passi per i chassis
   e' confermato dai numeri: i chassis sono gia' il ponte fra le classi di
   Krynn e la 5e, e sono l'unica struttura che copre `Fighter`, `Paladin` e
   `Thief` senza inventare classi.
2. **Dove il telaio allarga, lo scarto si dichiara o si stringe?**
   Vedi §3a: `Fighter` per telaio da' accesso anche al Cavaliere della Corona.
3. **Le {len(senza_telaio)} etichette senza telaio**: la razza perde
   l'accesso, o manca una classe? Sono due risposte diverse per
   sottoinsiemi diversi (§3b).
4. **Le {len(irraggiungibili) + len(orfani)} classi davvero irraggiungibili**
   ({", ".join(f"`{c[0]}`" for c in irraggiungibili + orfani) or "nessuna"}):
   si aggiunge un'etichetta che le raggiunga, o si accetta che siano PNG? Gli
   altri {len(avanzamenti) - len(orfani)} silenzi sono avanzamenti e vanno
   bene cosi'.
5. **`elfo-dargonesti`**: la nota va riscritta comunque, qualunque sia la
   risposta alle altre quattro.
""")

    return riflow("\n".join(P))


def main():
    p = os.path.join(BASE, "RAPPORTO-allowed-classes.md")
    testo = rapporto()
    with open(p, "w", encoding="utf-8") as f:
        f.write(testo)
    print(f"scritto {p} ({len(testo)} caratteri)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
