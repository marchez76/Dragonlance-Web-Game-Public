#!/usr/bin/env python3
"""
`allowed_classes` risolto -> dati/RAPPORTO-allowed-classes.md

COSA E' CAMBIATO RISPETTO ALLA PRIMA VERSIONE. La prima stesura portava la
MAPPA e non decideva: 17 etichette del PHB 2e contro 17 nostre classi, tre vie
di copertura, e il conto di cosa restava scoperto. La decisione 58
(`telaio-apre-classe-filtra`) l'ha presa: il telaio apre l'insieme, i
requisiti della classe filtrano dentro. Questo documento non porta piu' la
domanda, porta l'esito — e il prezzo dell'esito, che va dichiarato e non
assorbito (decisione 7, `doppio-strato`).

LA SEDE NON E' QUI. La mappa e la risoluzione stanno in
`dati/_classi_ammesse.py`. Qui si legge, si applica e si conta: un rapporto
che ridigitasse la mappa sarebbe la copia che il progetto ha gia' pagato
undici volte.

IL CONTROLLO SI METTE ALLA PROVA. L'euristica della prima versione — nome
uguale, parole in comune — non e' stata buttata: e' diventata un RISCONTRO. Se
trova un accostamento che la sede non porta, la sede ha un buco; se la sede
porta un accostamento che l'euristica non vede, quello e' un accostamento di
merito e deve avere la sua riga di fonte. Su una mappa scritta a mano un
riscontro assente e uno che tace si somigliano troppo.

COSA E' DERIVATO. Tutti i conteggi, gli elenchi, i motivi di esclusione:
letti dai dati. Cio' che e' editoriale sta in `_classi_ammesse.ETICHETTE`,
una riga per etichetta con la sua ragione accanto.

RIDUZIONE — CLAUDE.md, punti 1 e 2: legge dati privati (razze/, classi/) e
non emette testo di fonte. Escono id, nomi di classe, conteggi e motivi.

Uso:  python3 dati/analizza_allowed_classes.py
"""

import collections
import os
import re
import sys
import textwrap

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
sys.path.insert(0, BASE)
sys.path.insert(0, RADICE)

import _classi_ammesse as CA  # noqa: E402
import _srd51 as SRD  # noqa: E402
from decisioni import cita  # noqa: E402

# Parole che non distinguono: compaiono in mezzo roster e in mezze etichette,
# quindi un accostamento che si regge solo su queste non e' un accostamento.
VUOTE = {"of", "the", "and", "a", "stars", "wizard", "priest", "knight"}


def _parole(s):
    return {p for p in re.split(r"[^a-z]+", (s or "").lower()) if p} - VUOTE


# ------------------------------------------------------------------ lettura

def profilo(c):
    """(id, nome inglese, gruppo, telaio, stato, si-entra-da) di una classe."""
    m = c.get("mechanics_5e") or {}
    return (c["id"], (c.get("name") or {}).get("en") or c["id"],
            c.get("group"), (m.get("chassis") or {}).get("srd_class"),
            m.get("conversion_status"),
            c.get("requires_class") or m.get("prerequisite_class"))


def etichette(rz):
    """Ogni etichetta 2e con quante razze la concedono."""
    c = collections.Counter()
    for r in rz:
        ac = (r.get("mechanics_5e") or {}).get("allowed_classes") or {}
        for e in (ac.get("classes") or []):
            c[e] += 1
    return c


def riscontro_euristica(et, cl):
    """L'euristica della prima versione, ridotta a controllo della sede.

    Ritorna (trovati, mancanti): `trovati` e' cosa l'euristica accosta per
    nome o per parole, `mancanti` sono gli accostamenti che l'euristica vede e
    la sede NON porta. Un elemento in `mancanti` e' un buco della sede."""
    per_nome = {}
    trovati, mancanti = {}, []
    for e in sorted(et):
        pe = _parole(e)
        nome = [c["id"] for c in cl
                if ((c.get("name") or {}).get("en") or "").lower() == e.lower()]
        parole = [c["id"] for c in cl
                  if c["id"] not in nome and _parole((c.get("name") or {}).get("en")) & pe]
        trovati[e] = (nome, parole)
        per_nome[e] = set(nome) | set(parole)
        dichiarate = set(CA.ETICHETTE[e].classi)
        for c in sorted(per_nome[e] - dichiarate):
            mancanti.append((e, c))
    return trovati, mancanti


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
    rz, cl = CA.razze(), CA.classi()
    prof = [profilo(c) for c in cl]
    per_id = {p[0]: p for p in prof}
    et = etichette(rz)
    incoerenze = CA.verifica()
    _euristica, mancanti = riscontro_euristica(et, cl)

    n_raz, n_cl = len(rz), len(cl)
    telai = sorted(SRD.TABELLE)
    telai_usati = sorted({p[3] for p in prof if p[3]})
    senza_telaio = [p for p in prof if not p[3]]
    avanzamenti = [p for p in prof if p[5]]
    creabili = [p for p in prof if not p[5]]

    # ---- i due tempi, razza per razza
    esito = {}
    for r in rz:
        ammesse, escluse = CA.accessibili(r, cl)
        aperte, dich = CA.aperte(r, cl)
        esito[r["id"]] = (sorted(aperte), ammesse, escluse, dich)

    zero = [i for i, (_a, am, _e, _d) in esito.items() if not am]
    conteggi = sorted(((i, len(v[0]), len(v[1])) for i, v in esito.items()),
                      key=lambda t: (t[2], t[0]))
    tot_ammesse = sum(c[2] for c in conteggi)
    tot_aperte = sum(c[1] for c in conteggi)

    # ---- le etichette dichiarate che il filtro svuota
    # Una razza che dichiara un'etichetta e non ne ricava NESSUNA classe ha
    # perso quell'accesso per intero, e il conto per razza da solo non lo
    # mostra: mostra un numero piu' basso, non quale porta si e' chiusa.
    svuotate = []
    for r in rz:
        ac = (r.get("mechanics_5e") or {}).get("allowed_classes") or {}
        if not ac.get("applied"):
            continue
        ammesse = set(esito[r["id"]][1])
        for e in (ac.get("classes") or []):
            ap = CA.apre(e, cl)
            if not (ap & ammesse):
                svuotate.append((r["id"], e, sorted(ap)))
    vuote_alla_nascita = sorted({(e, ) for _r, e, ap in svuotate if not ap})
    svuotate_dal_filtro = [(r, e, ap) for r, e, ap in svuotate if ap]

    # ---- le etichette che nominano anche una classe base 2e
    # Lettura del 04/09/2026 sulla fonte, sede in `_classi_ammesse`, sezione
    # CLASSI BASE 2e. Cinque etichette non nominano solo un telaio: nominano
    # anche una classe del PHB 2e che Krynn gioca tale e quale e che il nostro
    # roster non ha. I numeri qui sotto si derivano, non si scrivono.
    def _dichiarano(e):
        return sorted(r["id"] for r in rz
                      if e in (((r.get("mechanics_5e") or {}
                                 ).get("allowed_classes") or {}
                                ).get("classes") or []))

    base_2e = sorted(CA.BASE_2E)
    dich_base = {e: _dichiarano(e) for e in base_2e}
    # Quali delle cinque il roster abbia gia' non si scrive: si chiede alla
    # sede, che lo deriva da ETICHETTE (decisione 59, `classi-base-2e`).
    base_manca = sorted(CA.base_2e_mancanti())
    base_fatte = [e for e in base_2e if e not in base_manca]
    # Chi ha guadagnato una classe dalla trascrizione: per ogni etichetta
    # trascritta, la classe base che nomina e le razze che ora ci arrivano.
    base_resa = [(e, c, sorted(i for i in dich_base[e] if c in esito[i][1]))
                 for e in base_fatte for c in CA.ETICHETTE[e].classi]
    thief_dich = dich_base["Thief"]
    thief_con = [i for i in thief_dich if "con-artist" in esito[i][1]]
    thief_senza = [i for i in thief_dich if i not in thief_con]

    # ---- il verso opposto, dopo il filtro
    raggiunta_da = collections.defaultdict(list)
    for i, (_a, am, _e, _d) in esito.items():
        for c in am:
            raggiunta_da[c].append(i)
    mute = [p for p in prof if not raggiunta_da[p[0]]]
    ok = set(raggiunta_da)
    cresce = True
    while cresce:
        cresce = False
        for p in mute:
            if p[0] not in ok and p[5] in ok:
                ok.add(p[0])
                cresce = True
    orfani = [p for p in mute if p[0] not in ok]

    # ---- il prezzo del telaio: chi la nomina contro chi la raggiunge
    nomina = collections.defaultdict(set)
    for r in rz:
        ac = (r.get("mechanics_5e") or {}).get("allowed_classes") or {}
        for e in (ac.get("classes") or []):
            for c in CA.ETICHETTE[e].classi:
                nomina[c].add(r["id"])

    # ---- i motivi di esclusione, contati
    motivi = collections.Counter()
    coppie_escluse = 0
    for _i, (_a, _am, escluse, _d) in esito.items():
        for _c, ms in escluse:
            coppie_escluse += 1
            for m, _dett in ms:
                motivi[m] += 1

    # ---- la coda dei telai
    # Le etichette senza telaio sono tre casi, non uno. Quella che apre lo
    # stesso una classe per nome NON e' in coda: e' coperta, e il telaio le
    # servirebbe solo per allargare.
    in_coda = {e: CA.ETICHETTE[e] for e in sorted(CA.ETICHETTE)
               if CA.ETICHETTE[e].telaio is None}
    coperte_senza_telaio = {e: v for e, v in in_coda.items() if CA.apre(e, cl)}
    aperte_a_niente = {e: v for e, v in in_coda.items() if not CA.apre(e, cl)}
    coda_nota = {e: v for e, v in aperte_a_niente.items()
                 if any(t.lower() in e.lower() for t in SRD.CODA)}
    coda_decisione = {e: v for e, v in aperte_a_niente.items()
                      if e not in coda_nota}
    razze_di = {e: sorted(r["id"] for r in rz
                          if e in (((r.get("mechanics_5e") or {}
                                     ).get("allowed_classes") or {}
                                    ).get("classes") or []))
                for e in in_coda}

    da_confermare = {e: v for e, v in sorted(CA.ETICHETTE.items())
                     if v.da_confermare}

    P = []

    # ------------------------------------------------------------------ §0
    P.append(f"""# `allowed_classes` risolto — dal telaio alle classi, razza per razza

*Generato da `dati/analizza_allowed_classes.py`. La mappa e la regola stanno
in `dati/_classi_ammesse.py`: qui si applicano e si contano.*

---

## 0. La regola, e cosa produce

La {cita('telaio-apre-classe-filtra')} risolve le
{len(et)} etichette del PHB 2e in due tempi: **il telaio apre l'insieme, i
requisiti della classe filtrano dentro**. Due controlli in sequenza, non uno.

Il conto, in tre numeri: le {n_raz} razze aprono **{tot_aperte} coppie
razza+classe**, il filtro ne toglie **{coppie_escluse}**, ne restano
**{tot_ammesse}** — una media di
**{tot_ammesse / n_raz:.1f} classi accessibili per razza** su
{n_cl} del roster, {len(creabili)} delle quali si prendono alla creazione.

> **Razze con zero classi accessibili: {len(zero)}**{"." if not zero else ": " + ", ".join(f"`{z}`" for z in zero) + " — una razza ingiocabile, da vedere subito."}

{"**La sede e i dati non tornano**: " + "; ".join(incoerenze) if incoerenze else "La sede e i dati tornano: nessuna etichetta dichiarata e non mappata, nessuna classe nominata che non esista."}
{"**L'euristica trova accostamenti che la sede non porta**: " + ", ".join(f"`{e}` -> `{c}`" for e, c in mancanti) if mancanti else "Il riscontro dell'euristica non trova accostamenti che la sede non porti gia' (§2b)."}
""")

    # ------------------------------------------------------------------ §1
    P.append(f"""---

## 1. Le due sponde

**{len(et)} etichette** distinte, dichiarate dalle razze:

{tabella(["etichetta 2e", "razze che la concedono"],
         [(f"`{e}`", n) for e, n in et.most_common()],
         allin=["---", "--:"])}

**{n_cl} classi** nel roster, con il telaio 5e su cui ciascuna sta:

{tabella(["nostra classe", "nome inglese", "gruppo", "telaio 5e", "stato", "si entra da"],
         [(f"`{i}`", n, g or "—", f"`{t}`" if t else "**nessuno**", s,
           f"`{rq}`" if rq else "—")
          for i, n, g, t, s, rq in prof])}

I telai trascritti sono {len(telai)} — {", ".join(f"`{t}`" for t in telai)} —
e il roster ne usa {len(telai_usati)}
({", ".join(f"`{t}`" for t in telai_usati)}).
{len(senza_telaio)} nostre classi non hanno un telaio: per loro la
{cita('telaio-apre-classe-filtra')} non cambia niente, perche' il telaio non
puo' aprire cio' su cui nessuno sta. Ci si arriva solo se un'etichetta le
nomina. {len(avanzamenti)} classi non si prendono alla creazione: si entra da
un'altra classe.

In coda ci sono {len(SRD.CODA)} telai SRD non ancora trascritti
({", ".join(f"`{t}`" for t in sorted(SRD.CODA))}, in `_srd51.CODA`): sono
lavoro noto, non decisioni aperte — vedi §8.
""")

    # ------------------------------------------------------------------ §2
    P.append(f"""---

## 2. La mappa, etichetta per etichetta

Due colonne, e non sono la stessa cosa. **Telaio**: editoriale — a quale
chassis 5e corrisponde l'etichetta, con la ragione accanto. **Nomina
direttamente**: di fonte — le nostre classi che l'etichetta nomina per nome o
che il manuale dichiara essere quella classe. Il telaio **si aggiunge** alla
seconda invece di sostituirsi: senza questa clausola l'etichetta `Mariner` non
aprirebbe il Marinaio, che non ha chassis.

{tabella(["etichetta", "razze", "telaio", "nomina direttamente", "apre in tutto"],
         [(f"`{e}`", et[e],
           f"`{CA.ETICHETTE[e].telaio}`" if CA.ETICHETTE[e].telaio else "**nessuno**",
           ", ".join(f"`{c}`" for c in CA.ETICHETTE[e].classi) or "—",
           ", ".join(f"`{c}`" for c in sorted(CA.apre(e, cl))) or "**niente**")
          for e in sorted(et)],
         allin=["---", "--:", "---", "---", "---"])}

### Le ragioni, che sono di due tipi e restano distinte

{tabella(["etichetta", "ragione del telaio (editoriale)", "ragione delle classi (di fonte)"],
         [(f"`{e}`", CA.ETICHETTE[e].ragione or "—",
           CA.ETICHETTE[e].fonte or "—")
          for e in sorted(et)])}

### 2b. Il riscontro dell'euristica

La prima versione di questo rapporto accostava etichette e classi per
somiglianza: nome uguale, oppure almeno una parola che distingue. Quella
euristica e' rimasta, come **controllo della sede**: cerca cio' che la mappa
scritta a mano potrebbe aver saltato.

{"**Accostamenti che l'euristica vede e la sede non porta**: " + ", ".join(f"`{e}` -> `{c}`" for e, c in mancanti) + ". Ognuno e' un buco della sede." if mancanti else "Nessun accostamento sfugge alla sede: tutto cio' che l'euristica vede, la mappa lo porta gia'."}

Il verso opposto non e' un errore ed e' la parte interessante: la sede porta
accostamenti che l'euristica **non puo'** vedere, perche' non si reggono sui
nomi. `Knight of Solamnia` non somiglia a nessuno dei tre ordini, e li apre
tutti e tre. Ogni riga di questo tipo porta la propria fonte nella colonna
qui sopra: e' il prezzo di non decidere per somiglianza.
""")

    # ------------------------------------------------------------------ §3
    P.append(f"""---

## 3. Primo tempo: cosa apre il telaio, e quanto allarga

Il prezzo della lettura per telaio va detto in numeri, non in prosa. Per ogni
classe: quante razze la **nominano** attraverso un'etichetta che la nomina
direttamente, e quante la **raggiungono** dopo che il telaio ha aperto e il
filtro ha stretto.

{tabella(["nostra classe", "telaio", "la nominano", "l'aprono", "la raggiungono", "scarto"],
         [(f"`{i}`", f"`{t}`" if t else "—",
           len(nomina[i]),
           sum(1 for _r, (ap, _am, _ex, _d) in esito.items() if i in ap),
           len(raggiunta_da[i]),
           (f"+{len(raggiunta_da[i]) - len(nomina[i])}"
            if len(raggiunta_da[i]) > len(nomina[i])
            else str(len(raggiunta_da[i]) - len(nomina[i]))))
          for i, _n, _g, t, _s, _rq in prof],
         allin=["---", "---", "--:", "--:", "--:", "--:"])}

Le righe con lo scarto piu' alto sono la {cita('doppio-strato')} messa alla
prova: dove la fonte era piu' stretta, il telaio allarga, e allargare in
silenzio sarebbe stato il difetto. Le righe con scarto negativo dicono
un'altra cosa ancora: l'etichetta nomina la classe, e il filtro la toglie a
qualcuno che la nominava.

{"Le tre razze senza elenco (§7) contano come razze che aprono tutto: il loro contributo alla colonna «l'aprono» non viene da un'etichetta ma dall'assenza di preclusione."}
""")

    # ------------------------------------------------------------------ §4
    P.append(f"""---

## 4. Secondo tempo: cosa toglie il filtro

{tabella(["motivo", "cosa toglie", "coppie razza+classe tolte"],
         [(f"`{m}`", CA.MOTIVI[m], n) for m, n in motivi.most_common()],
         allin=["---", "---", "--:"])}

Il filtro toglie **{coppie_escluse} coppie** su {tot_aperte} aperte. Una
coppia puo' essere tolta da piu' motivi insieme, ed e' il motivo per cui la
somma della colonna ({sum(motivi.values())}) supera il numero delle coppie:
sapere che una classe e' esclusa due volte e' diverso dal saperla esclusa una,
perche' togliere un vincolo non la riaprirebbe.

**Due filtri non sono applicati, e non per dimenticanza.** L'*allineamento*:
nessuna razza ne dichiara uno, quindi e' un vincolo sulla scelta del giocatore
e non sulla coppia razza+classe — filtrarlo qui non toglierebbe niente a
nessuno. La *classe sociale*: la fonte la introduce come regola opzionale e
non le ha dato una controparte in `mechanics_5e`, e un filtro su un dato che
vive solo in `source_2e` applicherebbe una regola che non abbiamo adottato.
Entrambi sono scritti in `_classi_ammesse.py`, non solo qui.
""")

    # ------------------------------------------------------------------ §5
    P.append(f"""---

## 5. La risposta: quante classi per razza, dopo il filtro

{tabella(["razza", "etichette dichiarate", "aperte dal telaio", "**accessibili**", "quali"],
         [(f"`{i}`",
           len(esito[i][3]) if esito[i][3] is not None else "*(nessun elenco)*",
           ap, f"**{am}**",
           ", ".join(f"`{c}`" for c in esito[i][1]))
          for i, ap, am in conteggi],
         allin=["---", "--:", "--:", "--:", "---"])}

Il numero e' molto piu' basso di quello del telaio — {tot_ammesse} contro
{tot_aperte} — ed e' il punto: il telaio da solo sarebbe stato una traduzione
generosa, la sequenza lo riporta dentro i vincoli che la fonte scrive sulle
classi invece che sulle razze.

Il minimo e {min(c[2] for c in conteggi)}
(`{conteggi[0][0]}`), il massimo {max(c[2] for c in conteggi)}
(`{conteggi[-1][0]}`).
{"**Nessuna razza resta a zero**: non c'e' nessuna razza ingiocabile." if not zero else "**Razze a zero: " + ", ".join(zero) + "**"}

### 5b. Le etichette dichiarate che non aprono niente

Il conto per razza da solo non dice **quale porta si e' chiusa**: dice un
numero piu' basso. Queste sono le coppie razza+etichetta in cui la razza
dichiara un accesso e non ne ricava nessuna classe. Sono due casi diversi.

**{len([1 for _r, _e, ap in svuotate if not ap])} coppie: l'etichetta non apre niente perche' il telaio e' in
coda.** {", ".join(f"`{e}`" for e in base_manca) if base_manca else "Nessuna"},
gia' contate in §8 come lavoro noto: la razza non ha perso l'accesso,
l'accesso non e' ancora stato scritto.

**{len(svuotate_dal_filtro)} coppie: l'etichetta apre, e il filtro toglie tutto.** {"""Erano tre fino al
04/09/2026 e sono la ragione per cui la decisione 59 (`classi-base-2e`)
esiste: un'etichetta che apre e poi non lascia niente e' una porta che il
manuale concede e il nostro roster chiude.""" if not svuotate_dal_filtro else """Queste sono la parte
che va guardata, perche' non si smaltiscono battendo a macchina un telaio
SRD."""}

{tabella(["razza", "etichetta", "cosa apre", "perche' non resta niente"],
         [(f"`{r}`", f"`{e}`", ", ".join(f"`{c}`" for c in ap),
           "; ".join(sorted({m for c in ap
                             for m, _d in CA.filtra(next(x for x in rz if x["id"] == r),
                                                   next(y for y in cl if y["id"] == c))})))
          for r, e, ap in svuotate_dal_filtro]).strip() if svuotate_dal_filtro else ""}
### Le cinque etichette che nominano una classe base 2e

La fonte lo dice per prima, e non e' una nostra classificazione. Il capitolo
delle classi di *Tales of the Lance* apre il gruppo dei guerrieri dichiarando
che su Ansalon si giocano le classi guerriere tipiche dell'AD&D 2e — fighter,
ranger e paladin — e che quelle **uniche** di Ansalon sono descritte di
seguito; il gruppo dei ladri ripete la forma, contando i bardi e i ladri fra
quelli comuni e riservando la descrizione ai due tipi propri di Krynn. I
gruppi Wizard e Priest non lo dicono, e infatti sono di Krynn.

Sono {len(base_2e)} etichette in questa condizione
({", ".join(f"`{e}`" for e in base_2e)}), dichiarate in tutto da
{len(set().union(*dich_base.values()))} razze su {n_raz}. La sede e'
`_classi_ammesse.BASE_2E`; **quali di esse il roster abbia gia' non e'
scritto da nessuna parte: si deriva** da chi nomina una nostra classe
(`_classi_ammesse.base_2e_mancanti()`).

**{len(base_fatte)} trascritte** dalla {cita('classi-base-2e')}, con i minimi
della Tabella 13 del PHB 2e e `mechanics_5e` che rimanda al chassis SRD senza
aggiungere nulla:

{tabella(["etichetta", "nostra classe", "razze che la dichiarano e ci arrivano", "quali"],
         [(f"`{e}`", f"`{c}`", str(len(chi)),
           ", ".join(f"`{i}`" for i in chi) if chi else "—")
          for e, c, chi in base_resa])}

**{len(base_manca)} ancora da trascrivere** ({", ".join(f"`{e}`" for e in base_manca) if base_manca else "nessuna"}), e
costano piu' delle prime tre: per queste manca **anche** il telaio SRD, che e'
in coda in `_srd51.CODA` (§8). Le prime tre avevano il telaio gia' battuto a
macchina e mancava la sola classe.

**Il Con Artist non e' in questa condizione, ed e' un esito atteso.** Il
manuale lo apre a qualunque razza giocabile di Krynn e nella stessa riga gli
pone un minimo di Carisma 12; all'Aghar pone un massimale di Carisma 9. E' la
doppia penalita' della {cita('massimali-razziali')} che morde dove deve
mordere: fedelta' che funziona, non una porta da riaprire.
{len(thief_dich)} razze dichiarano `Thief` e
{len(thief_con)} arrivano al Con Artist; {"resta fuori " + ", ".join(f"`{i}`" for i in thief_senza) if thief_senza else "nessuna resta fuori"}.
Chi rilegge fra sei mesi trovi scritto qui che questa riga **non va sanata** —
e che il ladro comune, che l'Aghar ora prende, e' un'altra classe.

Il conto che ne segue va saputo: la razza piu' vincolata del roster e'
`{conteggi[0][0]}`, con **{conteggi[0][2]} classi accessibili** su {n_cl}
({", ".join(f"`{c}`" for c in esito[conteggi[0][0]][1])}), contro le
{conteggi[1][2]} della seconda. Delle
{len(esito[conteggi[0][0]][3] or [])} etichette che dichiara,
{len([e for e in (esito[conteggi[0][0]][3] or []) if e in base_manca])} restano
nella condizione sopra. E' un numero che il giocatore deve vedere **in
creazione**, non scoprire dopo aver scelto la razza.

### Le esclusioni, razza per razza

Cio' che il telaio ha aperto e il filtro ha tolto. Le classi che il telaio non
ha mai aperto non compaiono: non sono state escluse, non sono state proposte.

{tabella(["razza", "classe esclusa", "motivi"],
         [(f"`{i}`", f"`{c}`",
           "; ".join(f"{m} ({d})" for m, d in ms))
          for i, (_a, _am, escluse, _d) in sorted(esito.items())
          for c, ms in escluse])}
""")

    # ------------------------------------------------------------------ §6
    P.append(f"""---

## 6. Il verso opposto, ricalcolato

Una nostra classe che nessuna razza puo' prendere e' **ingiocabile**, e finche'
nessuno guarda la mappa dal lato delle classi non si vede. Con la risoluzione
in opera il conto cambia, e cambia per una ragione che la mappa da sola non
poteva vedere: le razze senza elenco (§7) aprono il roster intero, quindi
raggiungono anche classi che **nessuna etichetta nomina**.

{tabella(["nostra classe", "si entra da", "razze che la raggiungono", "quante"],
         [(f"`{i}`", f"`{rq}`" if rq else "—",
           ", ".join(f"`{r}`" for r in raggiunta_da[i]) or "**NESSUNA**",
           len(raggiunta_da[i]))
          for i, _n, _g, _t, _s, rq in prof],
         allin=["---", "---", "---", "--:"])}

{len(mute)} classi su {n_cl} non sono raggiunte da nessuna razza alla
creazione, e contarle insieme darebbe un numero falso:

{tabella(["classe", "si entra da", "verdetto"],
         [(f"`{p[0]}` ({p[1]})", f"`{p[5]}`" if p[5] else "— nessuna",
           ("**avanzamento**, raggiungibile per la classe che lo richiede"
            if p[5] and p[0] in ok else
            "**avanzamento orfano**: anche la classe da cui si entra e' muta"
            if p[5] else "**INGIOCABILE**"))
          for p in mute]) if mute else "*(nessuna: ogni classe del roster e' raggiungibile)*"}

- **{len([p for p in mute if p[5] and p[0] in ok])} sono avanzamenti**: non
  devono essere raggiunti dalle razze, ci si arriva dalla classe che li
  richiede. Le tre Vesti si prendono dal Mago dell'Alta Stregoneria, Spada e
  Rosa dal Cavaliere della Corona.
- **{len([p for p in mute if not p[5]])} sono ingiocabili**:
  {", ".join(f"`{p[0]}`" for p in mute if not p[5]) or "*(nessuna)*"}.
### Il verdetto che e' cambiato: `commoner`

La prima stesura di questo rapporto dava `commoner` **INGIOCABILE**: nessuna
etichetta lo nomina, ed era vero. Con la risoluzione in opera lo raggiungono
{len(raggiunta_da['commoner'])} razze — le tre senza elenco — perche' un
roster aperto per assenza di preclusione arriva anche dove nessuna etichetta
arriva. Il difetto non era nei dati, era nella lettura: contare solo le
etichette non vedeva le razze che non ne hanno.

Il verso opposto e' stato controllato sulla fonte, ed e' la domanda che
contava: il Popolano e' una classe da personaggio o un profilo di PNG? Il
manuale lo tratta come classe da personaggio — il capitolo delle classi apre
la creazione di un popolano dalla scelta del mestiere, con i suoi tiri di
caratteristica e la sua progressione, e la regola opzionale sulla classe
sociale lo nomina come *classe da personaggio*. La sezione sui PNG e' un'altra
e non lo riguarda. Quindi la raggiungibilita' e' **corretta**, non un effetto
collaterale da correggere.

Resta un fatto della fonte, non un difetto nostro: la tabella Class/Race
Combinations non concede il Popolano a **nessuna** razza demiumana, mentre
concede il Tinker allo Gnomo. Un popolano non umano non esiste nel manuale.

- **{len(orfani)} avanzamenti orfani**{"." if not orfani else ": " + ", ".join(f"`{p[0]}`" for p in orfani) + " — la catena di ingresso c'e', ma comincia da una classe che nessuna razza raggiunge."}
""")

    # ------------------------------------------------------------------ §7
    senza_elenco = [(r["id"], (r.get("mechanics_5e") or {}
                               ).get("allowed_classes") or {})
                    for r in rz
                    if not ((r.get("mechanics_5e") or {}
                             ).get("allowed_classes") or {}).get("applied")]
    P.append(f"""---

## 7. Le {len(senza_elenco)} razze senza elenco, e due significati per un valore

{tabella(["razza", "applied", "classes", "accessibili dopo il filtro"],
         [(f"`{i}`", str(ac.get("applied")),
           "null" if ac.get("classes") is None else str(ac.get("classes")),
           len(esito[i][1]))
          for i, ac in senza_elenco],
         allin=["---", "---", "---", "--:"])}

`applied: false` vuol dire **nessun elenco**, e l'assenza di un elenco ha due
cause che il valore non distingue:

- **Nessuna preclusione** — la tabella Class/Race Combinations elenca solo le
  razze demiumane e gli umani non vi compaiono affatto: non c'e' nessuna riga
  che precluda loro qualcosa. Il vincolo non esiste.
- **La fonte tace** — il Dargonesti non e' nella tabella, che elenca il solo
  Dimernesti. Non e' un vincolo assente, e' un dato mancante.

Il secondo caso portava la nota del primo: campo compilato, controllo che
passa, e la spiegazione di un altro. Ora ogni razza senza elenco ha la
**propria** nota, e `build_razze.nota_classi_ammesse` **rifiuta di generare**
una razza a elenco vuoto che non ne abbia una: la garanzia e' strutturale, non
affidata a chi rilegge.

La conseguenza sui numeri resta e va guardata: finche' il silenzio della fonte
viene letto come assenza di vincolo, il Dargonesti prende l'esito **piu'
largo possibile** — {len(esito['elfo-dargonesti'][1])} classi — prodotto da un
buco del manuale e non da una scelta.

**La fonte non tace del tutto, e va detto qui perche' cambia i termini della
domanda.** Letto il 04/09/2026: il capitolo delle razze ha un paragrafo di
regole speciali per i PG Dimernesti **e** Dargonesti, e li' elenca cinque
classi che gli elfi del mare possono prendere — Cavalier, Paladin, Fighter,
High Sorcerer, Holy Orders. E' l'unico posto in cui il Dargonesti riceve un
elenco, e per il Dimernesti e' un **secondo** elenco accanto alla riga della
tabella. I due non coincidono: la riga della tabella non concede `Paladin`, il
paragrafo si'. La questione aperta resta scritta nel dato, ma le opzioni sono
tre e non due: ereditare le {len(esito['elfo-dimernesti'][3] or [])} voci del
Dimernesti, leggere le cinque del paragrafo, o lasciare il silenzio. Non e'
deciso qui, ed e' registrato perche' la seconda opzione non era in vista.
""")

    # ------------------------------------------------------------------ §8
    P.append(f"""---

## 8. Cosa resta aperto, e cosa e' solo lavoro

Le due cose si somigliano e non sono la stessa: una voce in coda si smaltisce,
una domanda aperta va decisa. Confonderle gonfia il conto delle decisioni con
del lavoro gia' noto. Le {len(in_coda)} etichette senza telaio si dividono in
tre casi, e nessuno di essi e' oggi una domanda; una quarta voce, le classi
base 2e, taglia trasversalmente e non dipende dal telaio.

### Lavoro noto: {len(coda_nota)} etichette che non aprono niente e hanno un telaio SRD in coda

{tabella(["etichetta", "telaio SRD in coda", "razze che la dichiarano", "quante"],
         [(f"`{e}`", ", ".join(f"`{t}`" for t in sorted(SRD.CODA)
                               if t.lower() in e.lower()),
           ", ".join(f"`{r}`" for r in razze_di[e]), len(razze_di[e]))
          for e in sorted(coda_nota)],
         allin=["---", "---", "---", "--:"]) if coda_nota else "*(nessuna)*"}

Il telaio esiste nell'SRD 5.1 e nessuno l'ha ancora trascritto: e' battitura,
non conversione. La coda sta in `_srd51.CODA`, accanto ai telai trascritti,
perche' e' li' che si guarda quando se ne aggiunge uno. Nota che trascrivere
il telaio non basta da solo: serve anche la classe che ci sta sopra, ed e'
esattamente la voce qui sotto.

### Lavoro noto, seconda voce: {len(base_manca)} etichette su {len(base_2e)} che nominano una classe base 2e ancora assente dal roster

{tabella(["etichetta", "telaio", "cosa manca", "razze che la dichiarano", "quante"],
         [(f"`{e}`",
           f"`{CA.ETICHETTE[e].telaio}`" if CA.ETICHETTE[e].telaio
           else "*in coda*",
           "la sola classe" if CA.ETICHETTE[e].telaio else "telaio **e** classe",
           ", ".join(f"`{r}`" for r in dich_base[e]), len(dich_base[e]))
          for e in base_manca],
         allin=["---", "---", "---", "---", "--:"])}

Non e' una nostra classificazione: e' quello che *Tales of the Lance* dichiara
aprendo i gruppi Warrior e Rogue (§5b). Delle {len(base_2e)} etichette in
questa condizione, {len(base_fatte)} sono state trascritte dalla
{cita('classi-base-2e')} — {", ".join(f"`{e}`" for e in base_fatte)}, che
avevano il telaio SRD gia' battuto a macchina e costavano la sola classe — e
con esse si sono chiuse le tre righe svuotate di §5b. Le
{len(base_manca)} che restano compaiono anche nella voce sopra e costano
telaio **e** classe: finche' la classe non c'e', l'etichetta apre il solo
insieme del telaio, che per queste due e' vuoto. Sede:
`_classi_ammesse.BASE_2E`, con la parte derivata in `base_2e_mancanti()`.

### Coperte lo stesso: {len(coperte_senza_telaio)} etichette senza telaio che aprono una classe per nome

{tabella(["etichetta", "apre", "razze", "perche' nessun telaio"],
         [(f"`{e}`", ", ".join(f"`{c}`" for c in sorted(CA.apre(e, cl))),
           ", ".join(f"`{r}`" for r in razze_di[e]), v.ragione)
          for e, v in sorted(coperte_senza_telaio.items())])
 if coperte_senza_telaio else "*(nessuna)*"}

Non sono in coda e non sono una domanda: la classe c'e' e la razza la
raggiunge. Cio' che manca e' il telaio **sotto la classe**, che e' un'altra
questione — riguarda i privilegi di quella classe, non l'accesso a essa.

### Decisioni aperte: {len(coda_decisione)} etichette che non aprono niente e non hanno un telaio in coda

{tabella(["etichetta", "razze che la dichiarano", "perche'"],
         [(f"`{e}`", ", ".join(f"`{r}`" for r in razze_di[e]), v.ragione)
          for e, v in sorted(coda_decisione.items())])
 if coda_decisione else "*(nessuna: ogni etichetta scoperta ha il suo telaio in coda)*"}

### Accostamenti da confermare: {len(da_confermare)}

{tabella(["etichetta", "classe aperta", "su cosa si regge"],
         [(f"`{e}`", ", ".join(f"`{c}`" for c in v.da_confermare), v.fonte)
          for e, v in da_confermare.items()]) if da_confermare else "*(nessuno: l'ultimo, `Druid (heathen)` sul Sacerdote Eretico, e' stato confermato sulla fonte il 04/09/2026 — la ragione sta in sede, non qui)*"}

Sono righe della sede marcate `da_confermare`: aprono una classe e aspettano
una lettura di merito. Restano visibili finche' qualcuno non le guarda — che
e' il contrario di un accostamento sciolto dentro un conteggio.
""")

    return riflow("\n".join(P))


def main():
    p = os.path.join(BASE, "RAPPORTO-allowed-classes.md")
    testo = rapporto()
    with open(p, "w", encoding="utf-8") as f:
        f.write(testo)
    print(f"scritto {p} ({len(testo)} caratteri)")
    for x in CA.verifica():
        print("PROBLEMA nella sede:", x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
