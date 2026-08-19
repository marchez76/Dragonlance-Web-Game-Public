#!/usr/bin/env python3
"""
Genera dati/RAPPORTO-classi.md: diagnostica sulle 17 classi di Krynn.

COSA E' E COSA NON E'
    E' un rapporto DIAGNOSTICO, come RAPPORTO-soddisfacibilita.md per le razze.
    Serve a vedere la forma del problema prima di convertire. NON compila
    `mechanics_5e`, non propone conversioni, non decide nulla.

REGOLA, la stessa del generatore di contesto
    DERIVATO      ogni numero, tabella, conteggio: viene dai JSON.
    INTERPRETATIVO  letture e confronti: scritti a mano, marcati nel documento.

FONTE DEI CONFRONTI 5e
    SRD 5.1 (CC-BY), tabelle di classe trascritte verbatim in `_srd51.py`.
    Non e' piu' materiale a memoria: e' una fonte, con la stessa dignita' dei
    JSON di Krynn.

DUE USCITE
    RAPPORTO-classi.md            pubblico. Le schede per classe mostrano lo
                                   STATO di conversione dei privilegi, non il
                                   loro testo: e' trascrizione 2e e non va nel
                                   repository pubblico.
    RAPPORTO-classi-completo.md   privato (escluso dal repo pubblico). Stesso
                                   documento, con il testo sintetico dei
                                   privilegi per riferimento interno.
    La riduzione e' una funzione del generatore (parametro `completo` di
    `scheda()`), non un intervento a posteriori sul file: rigenerare non puo'
    piu' reintrodurre testo di fonte nel pubblico.

Uso:  python3 analizza_classi.py
"""

import collections
import glob
import json
import os
import re
from datetime import date

import _srd51 as R

BASE = os.path.dirname(os.path.abspath(__file__))
OGGI = date.today().isoformat()

GRUPPI = ["Warrior", "Wizard", "Priest", "Rogue", "Normal"]
CAR_IT = {"str": "FOR", "dex": "DES", "con": "COS",
          "int": "INT", "wis": "SAG", "cha": "CAR"}

# --------------------------------------------------------------------------
# Conteggi 5e: derivati dall'SRD 5.1 trascritto in _srd51.py. Non a memoria.
# Esclusi gli Aumenti dei Punteggi di Caratteristica, uguali per tutti.
# --------------------------------------------------------------------------
CINQUE_E = {
    nome: {
        "privilegi": R.n_privilegi(nome),
        "asi": R.n_asi(nome),
        "dettaglio": R.privilegi(nome),
        "dado_vita": R.TABELLE[nome]["hit_dice"],
        "tiri_salvezza": R.TABELLE[nome]["saves"],
    }
    for nome in R.TABELLE
}

# Accoppiamenti scelti per il confronto puntuale del punto 1.
CONFRONTI = [
    ("cavaliere-corona", "Fighter", "guerriero"),
    ("mago-alta-stregoneria", "Wizard", "mago"),
    ("sacerdote-ordini-sacri", "Cleric", "sacerdote"),
]


def interpretativo(testo):
    righe = testo.strip().split("\n")
    return (f"> **Lettura interpretativa** — registrata il {OGGI}. "
            f"Non e' derivata dai dati.\n>\n"
            + "\n".join(f"> {l}" if l else ">" for l in righe))


def carica():
    return [json.load(open(p, encoding="utf-8"))
            for p in sorted(glob.glob(os.path.join(BASE, "classi", "*.json")))]


# ==========================================================================
# DERIVATO
# ==========================================================================

def privilegi(c):
    return c["source_2e"].get("special_benefits") or []


def impedimenti(c):
    return c["source_2e"].get("special_hindrances") or []


def livello_citato(testo):
    """Il privilegio e' agganciato a un livello? Cerca '<n>° livello'."""
    return bool(re.search(r"\d+°\s*livello", testo))


def prog(c):
    return c["source_2e"].get("progression") or []


def stato_privilegio(c, nome):
    """conversion_status del privilegio/impedimento dai dati mechanics_5e."""
    for f in c["mechanics_5e"].get("features") or []:
        if f["name"] == nome:
            return f.get("conversion_status") or "—"
    return "—"


def scheda(c, completo=False):
    """Blocco per singola classe. Tutto derivato.

    completo=True include il testo sintetico (150 caratteri) del privilegio,
    trascritto dalla fonte 2e: SOLO per la versione privata. completo=False
    (default, uscita pubblica) lo sostituisce con lo stato di conversione,
    che e' informazione nostra e non riproduce il manuale."""
    s = c["source_2e"]
    P, H = privilegi(c), impedimenti(c)
    pr = prog(c)
    xp = [p["xp"] for p in pr]
    righe = [f"### {c['name']['it']} — `{c['id']}`", ""]

    mini = ", ".join(f"{CAR_IT[k]} {v}" for k, v in sorted((s["ability_minimums"] or {}).items())) or "nessuno"
    righe += [
        f"| campo | valore |",
        f"|---|---|",
        f"| gruppo 2e | {c['group']} |",
        f"| dado vita | {s['hit_die'] or '—'} |",
        f"| minimi di caratteristica | {mini} |",
        f"| livello d'ingresso | {s['entry_level']}{'' if s['entry_level'] == 1 else '  (non si comincia da qui)'} |",
        f"| classe prerequisito | {c['requires_class'] or '—'} |",
        f"| allineamento | {s['alignment_restriction'] or 'nessuna restrizione'} |",
        f"| razze ammesse | {', '.join(s['race_restriction']) if s['race_restriction'] else 'tutte'} |",
        f"| ricchezza iniziale | {s.get('starting_wealth') or 'non dichiarata (eredita dal gruppo)'} |",
        f"| pagine PDF | {', '.join(str(p) for p in c['source']['pages_pdf'])} |",
        "",
    ]

    # tabella PE
    if pr:
        mono = all(xp[i] <= xp[i + 1] for i in range(len(xp) - 1))
        salti = [(pr[i + 1]["level"], xp[i + 1] - xp[i]) for i in range(len(xp) - 1)]
        raddoppi = sum(1 for _, d in salti if d > 0)
        righe.append(
            f"**Punti esperienza**: tabella presente, {len(pr)} livelli "
            f"(dal {pr[0]['level']}° al {pr[-1]['level']}°), "
            f"{'monotona crescente' if mono else '**NON monotona**'}. "
            f"Da {xp[0]:,} a {xp[-1]:,} PE.".replace(",", "."))
        titoli = [p for p in pr if p.get("title")]
        if titoli:
            righe.append(f"Titoli di livello: {len(titoli)} su {len(pr)} "
                         f"(fino al {titoli[-1]['level']}°).")
    else:
        righe.append("**Punti esperienza**: nessuna tabella propria. "
                     f"Il manuale rimanda alle tabelle standard del gruppo {c['group']}.")
    righe.append("")

    # THAC0 e tiri salvezza
    testo_tot = json.dumps(c, ensure_ascii=False)
    righe.append(
        f"**THAC0**: {'citato nel testo della classe' if 'THAC0' in testo_tot else 'non citato'}, "
        f"nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo "
        f"{c['group']}.")
    righe.append(
        "**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una "
        f"per classe: valgono le cinque categorie del gruppo {c['group']}.")
    righe.append("")

    # incantesimi
    sp = s.get("spell_progression")
    if sp:
        liv = sorted(int(k) for k in sp)
        gradi = max(len([x for x in v if x]) for v in sp.values())
        righe.append(f"**Incantesimi**: tabella presente, dal {liv[0]}° al {liv[-1]}° "
                     f"livello di classe, fino al {gradi}° grado di incantesimo.")
    else:
        righe.append("**Incantesimi**: nessuna progressione propria.")
    righe.append("")

    # privilegi
    con_liv = sum(1 for b in P if livello_citato(b["text"]))
    # chassis applicato dalla decisione 23
    ch = c["mechanics_5e"]["chassis"]
    if ch["srd_class"]:
        righe.append(f"**Chassis 5e (decisione 23)**: clone di **{ch['srd_class']}** "
                     f"(SRD 5.1), dado vita {ch['hit_die']}, tiri salvezza "
                     f"{', '.join(ch['saving_throws'])}. {ch['note'].split('. ', 1)[-1]}")
    else:
        righe.append(f"**Chassis 5e (decisione 23)**: nessuno, lasciato indeciso. "
                     f"{ch['note'].split(': ', 1)[-1]}")
    righe.append("")

    righe.append(f"**Privilegi**: {len(P)}, di cui {con_liv} agganciati a un livello "
                 f"esplicito. **Impedimenti**: {len(H)}. Da convertire: "
                 f"{c['mechanics_5e']['features_pending']}.")
    righe.append("")
    if P:
        terza = "testo sintetico" if completo else "stato conversione"
        righe.append(f"| privilegio | livello | {terza} |")
        righe.append("|---|---|---|")
        for b in P:
            m = re.search(r"(\d+)°\s*livello", b["text"])
            terzo = (f"{b['text'].split('.')[0][:150]}." if completo
                     else stato_privilegio(c, b["name"]))
            righe.append(f"| {b['name']} | {m.group(1) + '°' if m else '—'} | {terzo} |")
        righe.append("")
    if H:
        terza = "testo sintetico" if completo else "stato conversione"
        righe.append(f"| impedimento | {terza} |")
        righe.append("|---|---|")
        for h in H:
            terzo = (f"{h['text'].split('.')[0][:150]}." if completo
                     else stato_privilegio(c, h["name"]))
            righe.append(f"| {h['name']} | {terzo} |")
        righe.append("")

    # armi, armature
    wp = s.get("weapon_proficiencies") or {}
    req = wp.get("required") or []
    eq = s.get("equipment_rules") or []
    righe.append(f"**Armi obbligate**: {', '.join(req) if req else 'nessuna'}.")
    if eq:
        righe.append("**Regole di equipaggiamento**:")
        for e in eq:
            righe.append(f"- {e}")
    else:
        righe.append("**Regole di equipaggiamento**: nessuna dichiarata.")
    righe.append("")

    oq = s.get("open_questions") or []
    if oq:
        righe.append("**Ambiguità di fonte registrate**:")
        for q in oq:
            righe.append(f"- {q}")
        righe.append("")
    return "\n".join(righe)


def tabella_sintesi(classi):
    r = ["| classe | gruppo | DV | PE | inc. | priv. | imp. | ingresso | vincoli |",
         "|---|---|---|---|:-:|---:|---:|---:|---|"]
    for c in sorted(classi, key=lambda x: (GRUPPI.index(x["group"]), x["id"])):
        s = c["source_2e"]
        pr = prog(c)
        v = []
        if s["alignment_restriction"]:
            v.append("allineamento")
        if s["race_restriction"]:
            v.append("razza")
        nmin = len(s["ability_minimums"] or {})
        if nmin:
            v.append(f"{nmin} minimo" if nmin == 1 else f"{nmin} minimi")
        r.append(
            f"| {c['name']['it']} | {c['group']} | {s['hit_die'] or '—'} | "
            f"{str(len(pr)) + ' liv.' if pr else 'gruppo'} | "
            f"{'sì' if s.get('spell_progression') else '—'} | "
            f"{len(privilegi(c))} | {len(impedimenti(c))} | "
            f"{s['entry_level']}° | {', '.join(v) or '—'} |")
    return "\n".join(r)


def statistiche(classi):
    tot_p = sum(len(privilegi(c)) for c in classi)
    tot_h = sum(len(impedimenti(c)) for c in classi)
    con_liv = sum(1 for c in classi for b in privilegi(c) if livello_citato(b["text"]))
    senza_prog = [c for c in classi if not prog(c)]
    senza_priv = [c for c in classi if not privilegi(c)]
    per_gruppo = collections.defaultdict(list)
    for c in classi:
        per_gruppo[c["group"]].append(c)
    return {
        "tot_p": tot_p, "tot_h": tot_h, "con_liv": con_liv,
        "media_p": round(tot_p / len(classi), 1),
        "media_h": round(tot_h / len(classi), 1),
        "senza_prog": senza_prog, "senza_priv": senza_priv,
        "per_gruppo": per_gruppo,
        "max_p": max(classi, key=lambda c: len(privilegi(c))),
        "max_h": max(classi, key=lambda c: len(impedimenti(c))),
        "in_perdita": sorted(
            (c for c in classi if len(impedimenti(c)) > len(privilegi(c))),
            key=lambda c: (len(privilegi(c)) - len(impedimenti(c)), c["id"])),
        "senza_livello": sum(1 for c in classi for b in privilegi(c)
                             if not livello_citato(b["text"])),
        "tab_gruppi": "\n".join(
            f"| {g} | {len(per_gruppo[g])} | "
            f"{sum(len(privilegi(c)) for c in per_gruppo[g])} | "
            f"{round(sum(len(privilegi(c)) for c in per_gruppo[g]) / len(per_gruppo[g]), 1)} | "
            f"{sum(len(impedimenti(c)) for c in per_gruppo[g])} |"
            for g in GRUPPI if per_gruppo[g]),
    }


def confronto_puntuale(classi):
    """Tabella livello per livello Krynn contro 5e 2014."""
    per_id = {c["id"]: c for c in classi}
    blocchi = []
    for cid, cls5e, etichetta in CONFRONTI:
        c = per_id[cid]
        d = CINQUE_E[cls5e]
        # livelli a cui la classe di Krynn concede qualcosa.
        # I privilegi che non dichiarano un livello NON vengono assegnati al 1°:
        # la fonte tace, e assumere sarebbe inventare. Vanno in una riga a parte.
        liv_krynn = collections.defaultdict(list)
        senza_liv = []
        for b in privilegi(c):
            m = re.search(r"(\d+)°\s*livello", b["text"])
            if m:
                liv_krynn[int(m.group(1))].append(b["name"])
            else:
                senza_liv.append(b["name"])
        sp = c["source_2e"].get("spell_progression")
        if sp:
            liv_krynn[min(int(k) for k in sp)].append("primi incantesimi")
        liv5e = {l: t for l, t in d["dettaglio"]}
        tutti = sorted(set(liv_krynn) | set(liv5e))
        righe = [f"#### {c['name']['it']} contro {cls5e} (SRD 5.1, {etichetta})", "",
                 f"Dado vita: {c['source_2e']['hit_die']} contro {d['dado_vita']}. "
                 f"Tiri salvezza {cls5e}: {d['tiri_salvezza']}.", "",
                 f"| livello | {c['name']['it']} | {cls5e} SRD 5.1 |", "|---:|---|---|"]
        for l in tutti:
            righe.append(f"| {l}° | {', '.join(liv_krynn.get(l, [])) or '—'} | "
                         f"{liv5e.get(l, '—')} |")
        if senza_liv:
            righe.append(f"| *non dichiarato* | {', '.join(senza_liv)} | — |")
        righe += ["",
                  f"Livelli a cui {c['name']['it']} concede qualcosa: "
                  f"**{len(liv_krynn)}**, contro **{len(liv5e)}** del {cls5e}. "
                  f"Privilegi totali: **{len(privilegi(c))}** contro "
                  f"**{d['privilegi']}** (piu' {d['asi']} aumenti di caratteristica, "
                  f"che la 2e non ha)"
                  + (f"; {len(senza_liv)} privilegio di Krynn non dichiara a che "
                     f"livello si ottenga." if len(senza_liv) == 1 else
                     f"; {len(senza_liv)} privilegi di Krynn non dichiarano a che "
                     f"livello si ottengano." if senza_liv else "."), ""]
        blocchi.append("\n".join(righe))
    return "\n".join(blocchi)


# ==========================================================================
# DOCUMENTO
# ==========================================================================

def main():
    classi = carica()
    S = statistiche(classi)
    n = len(classi)

    doc = f"""# Rapporto diagnostico sulle {n} classi di Krynn

*Generato da `dati/analizza_classi.py` il {OGGI}.*

> **Cos'è.** Una diagnosi, non una conversione. Serve a vedere la forma del
> problema prima di compilare `mechanics_5e`, come `RAPPORTO-soddisfacibilita.md`
> ha fatto per le razze. Nessuna decisione è presa qui.
>
> **Come leggere.** Ogni numero e ogni tabella su Krynn è derivato dai JSON in
> `dati/classi/`. Le letture sono scritte a mano e marcate con un blocco citato
> e datato.
>
> **Fonte 5e.** SRD 5.1 (CC-BY), tabelle di classe trascritte verbatim in
> `dati/_srd51.py`. I confronti sono derivati da lì, non scritti a memoria.

---

## Sintesi

{tabella_sintesi(classi)}

**PE**: "gruppo" significa che la classe non ha una tabella propria e rimanda a
quella standard del suo gruppo. **priv.** = privilegi speciali, **imp.** =
impedimenti.

### Per gruppo

| gruppo | classi | privilegi | media | impedimenti |
|---|---:|---:|---:|---:|
{S['tab_gruppi']}

Su {n} classi: **{S['tot_p']} privilegi** in tutto (media {S['media_p']}), di cui
**{S['con_liv']}** agganciati a un livello esplicito, e **{S['tot_h']} impedimenti**
(media {S['media_h']}).

**{len(S['senza_prog'])} classi su {n} non hanno una tabella di esperienza propria**:
{', '.join(c['name']['it'] for c in S['senza_prog'])}.

**{len(S['senza_priv'])} classi su {n} non hanno alcun privilegio**:
{', '.join(c['name']['it'] for c in S['senza_priv'])}.

---

## 1. Densità

{confronto_puntuale(classi)}

{interpretativo(f'''Le classi di Krynn non sono classi nel senso della 5e: sono **profili di
restrizione** appoggiati sulle classi base della 2e. Su {S['tot_p']} privilegi totali solo
{S['con_liv']} sono agganciati a un livello esplicito; per gli altri {S['senza_livello']} la fonte non dice
quando si ottengano. La curva di avanzamento è quindi quasi piatta: ciò che un
personaggio guadagna salendo di livello viene dalla tabella del gruppo 2e, non
dalla classe di Krynn.

**{len(S['in_perdita'])} classi su {n} hanno più impedimenti che privilegi**, cioè tolgono più di quanto
diano: {', '.join(c['name']['it'] + f" ({len(privilegi(c))} contro {len(impedimenti(c))})" for c in S['in_perdita'])}.
Il caso limite è l'**{S['in_perdita'][0]['name']['it']}**. Non è un errore di trascrizione: il manuale
definisce alcune di queste classi per ciò che non possono fare.

Il **{S['max_h']['name']['it']}** è il rovescio: {len(privilegi(S['max_h']))} privilegi e {len(impedimenti(S['max_h']))} impedimenti, il valore più alto
del roster in entrambe le colonne. È la sola classe con un contenuto meccanico
paragonabile a una classe 5e, e lo paga con il codice cavalleresco.

All'estremo opposto ci sono {len(S['senza_priv'])} classi con zero privilegi. Popolano e Tinker
sono del gruppo Normal e non dovrebbero averne; le tre Vesti sono vuote perché
sono affiliazioni e non classi, il che è coerente con la decisione 6. Restano i due
sacerdoti e l'Handler, che invece dovrebbero avere un contenuto e non ce l'hanno:
per i sacerdoti tutto il contenuto meccanico sta nelle sfere delle divinità, già
estratte in `dati/divinita/`; per l'Handler il manuale spende tre impedimenti e
nessun beneficio, cioè definisce un ladro per ciò che non sa fare.

La conseguenza pratica: convertire queste classi in 5e non è un lavoro di
traduzione ma di **riempimento**. Non c'è quasi nulla da tradurre, e la fedeltà
alla fonte (decisione 16) qui non basta a produrre una classe giocabile.''')}

---

## 2. Chassis 5e

*Analisi svolta prima della decisione 23, che l'ha poi adottata. I chassis sono
ora applicati nei dati: vedi `mechanics_5e.chassis` in `dati/classi/*.json`.*

Per ciascuna classe di Krynn, la classe base 5e più vicina come chassis.

| classe di Krynn | chassis 5e 2014 | perché |
|---|---|---|
| Barbaro | Fighter, **non** Barbarian | Il Barbarian 5e è costruito sull'Ira, che la 2e non ha. Il barbaro di Krynn è un guerriero con competenze ambientali: il Fighter regge meglio, con l'ambiente spostato su background/competenze. |
| Cavaliere della Corona | Fighter | Specializzazione nelle armi e progressione da guerriero puro. Nessuna magia al 1° grado. |
| Cavaliere della Spada | Paladin | La fonte rimanda esplicitamente alle capacità della classe Paladino, e concede incantesimi da sacerdote dal 6°. È l'accoppiamento più pulito del roster. |
| Cavaliere della Rosa | Paladin | Prosegue il grado precedente; l'immunità alla paura è già un privilegio del Paladin 5e (Aura di Coraggio, 10°). |
| Cavaliere | Fighter con Stile Difesa, oppure Cavalier (sottoclasse) | Sei privilegi tutti di combattimento montato e reputazione. La sottoclasse Cavalier del PHB 2014 copre il montato; il codice comportamentale resta scoperto. |
| Marinaio | Fighter/Rogue ibrido — **nessun candidato pulito** | Guerriero con quattro abilità da ladro. In 5e sarebbe multiclasse o una sottoclasse dedicata: entrambe le strade sono decisioni, non conversioni. |
| Mago dell'Alta Stregoneria | Wizard | Corrispondenza diretta. Le fasi lunari non hanno equivalente e vanno inventate o scartate. |
| Mago Rinnegato | Wizard | Stesso chassis, definito per sottrazione: è il Mago dell'Alta Stregoneria senza vincoli e senza bonus lunari. |
| Vesti Bianche / Rosse / Nere | **nessuno — non sono classi** | Decisione 6: affiliazioni dichiarate al Test, al 3° livello, sopra la classe base. In 5e il posto naturale è la sottoclasse (Tradizione Arcana), che però in 5e si sceglie al 2°, non al 3°. |
| Sacerdote degli Ordini Sacri | Cleric | Corrispondenza diretta, con le sfere già estratte da mappare sui Domini. |
| Sacerdote Eretico | **nessuno** | Per definizione non ha potere reale. In 5e non esiste una classe che non faccia nulla: o diventa un background, o una variante di Cleric senza incantesimi, o sparisce. |
| Truffatore | Rogue | Le quattro abilità potenziate diventano competenze ed Esperienza. |
| Handler | Rogue senza attacco furtivo | Chassis giusto, ma l'assenza dell'attacco furtivo svuota il Rogue 5e del suo motore di danno. |
| Popolano | **nessuno** | Non è una classe 5e. O PNG, o background. |
| Tinker | **nessuno** | Stessa situazione del Popolano, con in più il tema tecnologico gnomesco. Artificer esiste ma non è nel PHB 2014. |

{interpretativo('''Su quindici voci, sei hanno un chassis pulito (i due maghi, il Cleric, i due gradi
paladinici, il Rogue truffatore); tre non hanno alcun candidato perché non sono
classi (Popolano, Tinker, Vesti); tre sono classi 5e svuotate del loro motore
(Handler senza attacco furtivo, Sacerdote Eretico senza incantesimi, Barbaro senza
Ira); tre richiedono una decisione di struttura (Marinaio ibrido, Cavaliere,
Cavaliere della Corona come Fighter senza sottoclasse).

Il caso più interessante è il **Barbaro**: la classe 5e che porta il suo nome è
quella sbagliata. L'Ira è un'invenzione della 3e, non un tratto del barbaro di
Krynn né del kit del 1989. Chiamare Barbarian il Barbaro di Ansalon importerebbe
in blocco una meccanica che la fonte non ha.

Il secondo è il **conflitto sul livello delle Vesti**: la decisione 6 le colloca al
3° perché lì avviene il Test, ma la 5e assegna la sottoclasse del Wizard al 2°. Il
disallineamento è di un livello solo, ma va deciso: si sposta il Test al 2°, si
tiene la sottoclasse vuota per un livello, o si accetta uno scarto.''')}

---

## 3. Incompatibilità strutturali

Sistemi 2e senza equivalente in 5e. Richiedevano una **decisione**, non una
conversione. **Le prime sette sono state decise e applicate**: la scelta adottata
è indicata sotto ciascuna, e vive in `mechanics_5e.structural` in ogni classe.
Le ultime due restano aperte.

Per ciascuno: cosa faceva, perché la 5e l'ha eliminato, opzioni, esito.

### 3.1 Tabelle di esperienza differenziate per classe

**Cosa faceva.** Ogni classe 2e aveva la propria soglia di PE. Le classi
considerate più potenti salivano più lentamente: era il bilanciamento, spalmato
sul tempo di gioco invece che sulle capacità.

**Perché la 5e l'ha eliminato.** Una sola tabella per tutti. Con il gruppo che
avanza insieme, tabelle differenziate producevano personaggi di livello diverso
nella stessa squadra — l'effetto che la 5e considerava peggiore del problema che
risolveva.

**Opzioni.** (a) Tabella unica 5e, e le progressioni 2e restano in `source_2e`
come dato storico. (b) Tabella unica ma con moltiplicatore di PE per classe,
conservando l'ordinamento relativo senza sfasare i livelli. (c) Conservare le
tabelle 2e, accettando gruppi disallineati.

**DECISO** — opzione (a): tabella unica 5e. Le progressioni 2e restano in
`source_2e` come dato storico.
### 3.2 Progressione THAC0 per gruppo

**Cosa faceva.** Warrior migliorava di 1 per livello, Priest e Rogue circa 2 ogni
3 livelli, Wizard 1 ogni 3. La capacità di colpire era la differenza principale
fra i gruppi.

**Perché la 5e l'ha eliminato.** Il bonus di competenza è identico per tutti e
cresce da +2 a +6. La differenziazione è passata alle competenze nelle armi,
all'Attacco Extra e alle sottoclassi.

**Opzioni.** (a) Bonus di competenza standard; la differenza fra gruppi si esprime
con Attacco Extra e competenze. (b) Bonus di competenza standard più un bonus di
gruppo separato, che ricrea lo scarto 2e ma rompe la matematica dei GS 5e.
(c) Ripristinare scale differenziate, con lo stesso problema in forma peggiore.

**DECISO** — opzione (a): bonus di competenza standard. La differenza fra gruppi
si esprime con Attacco Extra e competenze.
### 3.3 Le cinque categorie di tiro salvezza

**Cosa faceva.** Paralisi/Veleno/Magia della Morte, Bacchette, Pietrificazione,
Soffio, Incantesimi. Erano proprietà della classe e del livello, non delle
caratteristiche: un guerriero di 9° aveva buoni tiri perché era un guerriero.

**Perché la 5e l'ha eliminato.** Sei tiri su caratteristica, con competenza in due
sole, decise dalla classe. Il vantaggio è che l'effetto dice quale caratteristica
usare; il costo è che il livello non migliora più i tiri non competenti.

**Opzioni.** (a) Mappare le cinque categorie sulle sei caratteristiche
(Paralisi/Veleno→COS, Bacchette→DES, Pietrificazione→COS o FOR, Soffio→DES,
Incantesimi→SAG) e assegnare a ogni classe le due competenze coerenti col gruppo
2e. (b) Conservare le cinque categorie come sistema parallelo, incompatibile con
tutto il resto della 5e. (c) Ibrido: competenze 5e più un bonus che cresce col
livello sulle categorie in cui il gruppo 2e era forte.

**Nota:** nessuna delle {n} classi ha una tabella di tiri salvezza estratta. Il
manuale non ne stampa una per classe di Krynn: valgono quelle di gruppo del PHB 2e,
che non sono ancora nei dati.

**DECISO** — opzione (a): le cinque categorie sono mappate sulle sei
caratteristiche (Paralisi/Veleno→COS, Bacchette→DES, Pietrificazione→COS,
Soffio→DES, Incantesimi→SAG), e ogni classe riceve le due competenze coerenti
col gruppo 2e.
### 3.4 Slot di competenza nelle armi

**Cosa faceva.** Un numero finito di slot, spesi per diventare competenti in
un'arma; spenderne due dava specializzazione, con bonus a colpire e ai danni.
Guerrieri ne avevano molti, maghi pochissimi. Le armi non competenti davano
penalità.

**Perché la 5e l'ha eliminato.** Competenza per categoria (armi semplici, armi da
guerra), concessa in blocco dalla classe. Nessuna specializzazione, sostituita
dai talenti opzionali.

**Opzioni.** (a) Competenze per categoria 5e; le armi obbligate della fonte
(lancia e spada per i cavalieri, ascia bipenne e spada bastarda per il barbaro)
diventano equipaggiamento iniziale imposto invece che slot. (b) Ricreare la
specializzazione come talento dedicato — è già così nel PHB 2014 con Maestro
d'Armi. (c) Sistema a slot parallelo, che duplica le competenze 5e.

**Da notare:** la specializzazione nelle armi è dichiarata come **privilegio** per
il Cavaliere della Corona e per il Minotauro. Se la specializzazione sparisce, i
due perdono un privilegio: va sostituito o registrato come perdita.

**DECISO** — opzione (a): competenze per categoria 5e. Le armi obbligate della
fonte diventano equipaggiamento iniziale imposto.
### 3.5 Ricchezza iniziale per gruppo

**Cosa faceva.** Ogni gruppo tirava una formula in monete (Warrior 5d4×10,
Rogue 2d6×10, e così via), poi comprava l'equipaggiamento. Il tiro produceva
personaggi di partenza diseguali.

**Perché la 5e l'ha eliminato.** Pacchetto di equipaggiamento fisso per classe e
background, con l'oro come alternativa opzionale. Elimina il tiro e la
disuguaglianza iniziale.

**Opzioni.** (a) Pacchetti fissi 5e, con le regole di equipaggiamento della fonte
convertite in vincoli sul pacchetto (il marinaio senza armature metalliche, il
barbaro senza armature pesanti, il cavaliere obbligato all'armatura migliore).
(b) Tiro 2e conservato, coerente con la decisione 8 che ha già scelto i dadi per
le caratteristiche. (c) Pacchetto fisso più tiro opzionale.

**Da notare:** solo 4 classi su {n} dichiarano una ricchezza iniziale propria; le
altre rimandano al gruppo. E una delle quattro, il Cavaliere, ha il valore
**ricostruito e non letto** (vedi le sue ambiguità di fonte).

**DECISO** — opzione (a): pacchetti fissi 5e, con le regole di equipaggiamento
della fonte convertite in vincoli sul pacchetto.
### 3.6 Livelli oltre il 20°

**Cosa faceva.** Le tabelle di Krynn arrivano al **25° livello**.

**Perché è un problema.** La 5e si ferma al 20°, e la matematica dei gradi sfida è
tarata su quel tetto.

**Opzioni.** (a) Troncare al 20°, conservando in `source_2e` i cinque livelli in
più. (b) Epic Boons oltre il 20°, che nel 2014 sono materiale della DMG.
(c) Comprimere 25 livelli 2e in 20 livelli 5e, riscalando le soglie.

**DECISO** — opzione (a): troncamento al 20°. I cinque livelli in più restano in
`source_2e`.
### 3.7 Titoli di livello

**Cosa faceva.** Ogni livello aveva un titolo (Novice of Swords, Blade Knight,
Master Clerist...). Era colore, ma anche struttura sociale dell'ordine.

**Perché la 5e l'ha eliminato.** Nessun titolo, in nessuna classe.

**Opzioni.** (a) Conservarli come dato descrittivo, mostrato nella scheda ma senza
effetto meccanico. (b) Legarli a un sistema di reputazione o grado nell'ordine.
(c) Scartarli.

**DECISO** — opzione (a): conservati come dato descrittivo, mostrati nella
scheda, senza effetto meccanico.
### 3.8 Sfere sacerdotali contro Domini

**Cosa faceva.** Ogni divinità concedeva accesso maggiore o minore a un elenco di
sfere; l'incantesimo era disponibile se la sfera lo era.

**Perché la 5e l'ha eliminato.** Il Cleric ha una lista unica più un Dominio che
aggiunge incantesimi sempre preparati. L'accesso non si nega più: si concede.

**Opzioni.** (a) Mappare le sfere sui Domini 2014 (Conoscenza, Guerra, Vita, Luce,
Natura, Tempesta, Inganno), con perdita di granularità. (b) Conservare le sfere
come filtro sulla lista 5e, ripristinando la negazione di accesso — coerente con
la decisione 16, che dà la precedenza alla fonte. (c) Ibrido: Dominio per gli
incantesimi bonus, sfere per i divieti.

**Materiale già pronto**: le sfere delle 21 divinità sono estratte in
`dati/divinita/`, con accesso maggiore e minore distinti.

### 3.9 Ordine obbligato dei gradi solamnici

**Cosa faceva.** Corona → Spada → Rosa, con ingresso al 1°, 3° e 4° livello.

**Perché è un problema.** La decisione 5 lo ha già confermato come sequenza
obbligata senza azzeramenti. In 5e non esiste un meccanismo di "grado" che cambi
la classe a metà percorso: la struttura più vicina è la sottoclasse, ma se ne
sceglie una sola.

**Opzioni.** (a) Classe unica con tre stadi interni, sbloccati al livello
previsto. (b) Tre sottoclassi in sequenza, che la 5e non prevede. (c) Classe base
più un sistema di gradi d'ordine separato dalla classe.

---

## Cosa manca ai dati

{interpretativo(f'''Prima di poter compilare `mechanics_5e` per le classi mancano tre cose che non
sono decisioni ma estrazioni:

1. **Le tabelle di gruppo del PHB 2e** — PE, THAC0 e tiri salvezza per Warrior,
   Wizard, Priest e Rogue. {len(S['senza_prog'])} classi su {n} vi rimandano, e senza quelle tabelle
   quelle classi non hanno progressione alcuna nei dati. Il PHB 2e è in libreria
   ma il suo testo estratto è degradato: le tabelle andranno lette dalle immagini
   di pagina, come già fatto per i tratti razziali.

2. **La ricchezza iniziale del Cavaliere**, che è ricostruita e non letta.

3. **Il PHB 5e 2014** resta fuori libreria, ma non è più bloccante: l'SRD 5.1
   copre classi base, privilegi livello per livello e liste incantesimi, ed è
   ridistribuibile. Del PHB servirebbero solo le sottoclassi fuori SRD — fra
   cui i Domini Morte e Forgia, che servono a tre divinità.''')}

---

## Appendice — il Barbaro alla fonte completa

Confronto fra le tre fonti disponibili in libreria. Serve a distinguere cosa dei
tratti di Ansalon è specifico di Krynn e cosa è tradizione del barbaro 2e, come la
decisione 16 ha fatto col PHB per elfi e nani. **Non riorganizza il Barbaro**: la
decisione 20 resta in piedi e la conversione a background resta rimandata.

### Le tre fonti

| fonte | anno | cos'è il barbaro | dove |
|---|---|---|---|
| `PHBR1 - The Complete Fighter's Handbook` | 1989 | **kit** del guerriero, non classe | Warrior Kits, pagg. 18-19 |
| `PHBR14 - The Complete Barbarian's Handbook` | 1995 | **classe autonoma** (barbarian fighter e shaman) | tutto il manuale, 130 pagg. |
| `Tales of the Lance` | 1992 | **razza/cultura** e **classe**, in due capitoli distinti | People of Ansalon e Classes of Ansalon |

### Cosa dice il kit del 1989 (PHBR1)

Il barbaro è un guerriero con un kit. Non ha tabella di esperienza, né dado vita,
né tiri salvezza propri: è un Fighter. Il kit aggiunge:

- competenze d'arma obbligate — Ascia bipenne, Spada bastarda;
- competenza bonus non d'arma — Resistenza;
- vincolo sull'armatura: niente più pesante di splint/banded/bronze plate finché
  non ha viaggiato nel mondo esterno;
- **+3 alle reazioni** quando il tiro è già favorevole (8 o meno), e **−3** quando
  è già sfavorevole (14 o più);
- ricchezza da guerriero (5d4×10 mo) che deve spendere quasi tutta prima di
  cominciare, restando con 3 mo o meno.

**Non c'è nulla** su terreno natio, nostalgia, tracciare, o limiti di Intelligenza
e Carisma.

### Cosa aggiunge il manuale del 1995 (PHBR14)

Qui il barbaro diventa classe, con due varianti: **barbarian fighter** e **shaman**.
Il fighter ha:

- **tabella di esperienza propria**, più lenta del guerriero standard, fino al 20°;
- **dado vita d12** — nove dadi, poi +3 fissi per livello;
- **movimento base 15**, contro il 12 dell'umano standard, e +3 al movimento da
  ingombro;
- **abilità fisiche a percentuale che crescono col livello**: salto, balzo,
  arrampicata (30%→95%), rilevamento degli attacchi alle spalle (5%→95%);
- **armature limitate a Hide (CA 6)**, armi solo di pietra, legno, osso;
- attacchi multipli come il guerriero, più regola per le due armi;
- **Homeland Terrain**, che concede gratis quattro competenze nel terreno natio —
  Sopravvivenza, Nascondersi, Seguire tracce, Conoscenza degli animali — più
  **−2 alla sorpresa dei nemici**;
- **limiti di Intelligenza e Carisma**: nessun massimale fisso, ma una penalità da
  −2 a −6 alle prove di INT e CAR **fuori dal territorio natio**;
- **penalità di reazione** fino a −6, cumulativa per igiene, aspetto, linguaggio,
  comportamento, e **mai riducibile sotto −1**;
- ricchezza in prodotti animali invece che in monete;
- avversione alla magia: la magia di casa è accettata, quella del mondo esterno è
  un presagio orribile.

### Il confronto con Tales of the Lance

| elemento | PHBR1 1989 | PHBR14 1995 | Tales of the Lance | verdetto |
|---|---|---|---|---|
| Terreno natio come meccanica | assente | **Homeland Terrain**, 4 competenze gratis | *Figlio del proprio territorio*: Sopravvivenza, Tracciare, Cacciare | **tradizione 2e**, non Krynn |
| Malus fuori dal territorio | assente | −2/−6 a INT e CAR nell'outworld | *Nostalgia del territorio*: −1 a tutti i tiri per 1d6 giorni | **stessa idea, meccanica diversa**: Krynn la fa temporanea e generale, PHBR14 permanente e mirata |
| Tetto all'Intelligenza | assente | nessun tetto, solo penalità sulle prove | **INT max 18, DES max 16** sulla scheda razziale | **specifico di Krynn** |
| Reazione | +3/−3 | fino a −6, mai sotto −1 | *Magnetismo selvaggio* +3 / *Rovescio* −3 | **il kit del 1989**, ripreso alla lettera |
| Armi obbligate | **Ascia bipenne, Spada bastarda** | armi di pietra/legno/osso, elenco di undici | **Ascia bipenne, Spada bastarda** | **il kit del 1989**, identiche |
| Vincolo sull'armatura | niente oltre splint/banded/bronze plate | niente oltre Hide (CA 6) | niente oltre splint/banded/bronze plate | **il kit del 1989**, identico |
| Dado vita | d10 (guerriero) | **d12** | d10 | **Krynn segue il kit**, non il manuale del 1995 |
| Tabella di esperienza | quella del guerriero | **propria, più lenta** | quella del guerriero | **Krynn segue il kit** |
| Movimento | normale | **15** | normale | **Krynn segue il kit** |
| Abilità fisiche a percentuale | assenti | salto, arrampicata, attacchi alle spalle | assenti | **solo PHBR14** |
| Immunità al freddo | assente | assente | **barbari del ghiaccio** | **specifico di Krynn** |
| Quattro gruppi culturali | assente | terreno a scelta libera | montagna, pianura, ghiaccio, mare | **specifico di Krynn** |

{interpretativo('''**Il Barbaro di Krynn discende dal kit del 1989, non dalla classe del 1995.**
La prova non è un'impressione: Tales of the Lance obbliga alle **stesse due armi**
del kit — Ascia bipenne e Spada bastarda, che il kit presenta come le armi
tipiche del barbaro da narrativa fantasy — e ripete **lo stesso identico
vincolo sull'armatura**, splint/banded/bronze plate. Aggiungi dado vita d10,
tabella di esperienza del guerriero, movimento normale e il +3/−3 alle reazioni,
e la derivazione è completa. Tales of the Lance esce nel 1992, in mezzo alle due
fonti, e usa quella che esisteva.

Questo spiega la doppia natura che la decisione 12 aveva registrato come
ambiguità della fonte: **non è un'ambiguità, è un residuo**. Il barbaro di Krynn è
un kit del guerriero che il manuale ha collocato in due capitoli — cultura e
classe — perché la 2e del 1992 non aveva ancora una classe barbaro da citare.
Questo rafforza, senza deciderla, la strada del background già indicata dalla
decisione 20: un kit non è una classe, ed è esattamente ciò che in 5e diventa un
background più una sottoclasse.

Due tratti sono **davvero di Krynn** e non hanno riscontro in nessuna delle due
fonti generali: l'**immunità al freddo dei barbari del ghiaccio** e i **quattro
gruppi culturali**. Un terzo, il **tetto a Intelligenza 18 e Destrezza 16**, è di
Krynn come *numero*: PHBR14 tratta la stessa idea come penalità situazionale
anziché come massimale.

E uno è **tradizione 2e travestita da Krynn**: il legame col terreno natio. Sia il
manuale del 1995 sia Tales of the Lance concedono competenze gratuite nel proprio
ambiente. Per la decisione 16, questo andrebbe convertito guardando alla forma
generale del tratto, non a quella particolare di Krynn.

**Una cosa che PHBR14 ha e noi no**: la *nostalgia del territorio* di Krynn dura
1d6 giorni e poi passa. Il malus di PHBR14 è permanente e colpisce solo INT e CAR
nell'outworld — cioè è **il vero corrispettivo meccanico del tetto
all'Intelligenza**, non del malus temporaneo. Se un giorno si volesse rimuovere il
tetto DES 16 senza perdere l'identità del barbaro, la penalità situazionale di
PHBR14 sarebbe la sostituzione naturale. Non è una proposta: è materiale.''')}

### Ambiguità trovate, da registrare

- **Il testo estratto di `PHBR1 - The Complete Fighter's Handbook` ha le colonne
  fuse.** Le righe delle due colonne si alternano ("reaction. Bur because he's /
  Fighter or Ranger"), quindi il manuale è leggibile solo per frammenti. Non ha
  compromesso questo confronto — le voci del kit sono riconoscibili — ma va
  ri-estratto prima di usarlo come fonte.
- **PHBR14 nomina Krynn una sola volta** e la DRAGONLANCE tre: due esempi di
  terreno natio (le Grandi Paludi) e una nota sui **Kagonesti come elfi barbari**.
  Non contiene materiale su Krynn oltre a questo: non è una fonte di setting.
- **PHBR14 cita i Kagonesti come esempio di elfi barbari**, insieme agli elfi
  silvani in generale. È una menzione di colore, senza meccanica: non incide
  sulle decisioni 21 e 22.
"""

    classi_ord = sorted(classi, key=lambda x: (GRUPPI.index(x["group"]), x["id"]))

    # PUBBLICO: senza testo sintetico dei privilegi, solo stato di conversione.
    out = os.path.join(BASE, "RAPPORTO-classi.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
        f.write("\n---\n\n## Schede per classe\n\n")
        for c in classi_ord:
            f.write(scheda(c, completo=False) + "\n---\n\n")

    # PRIVATO: con il testo sintetico. Mai nel pubblico: e' trascrizione 2e.
    out_completo = os.path.join(BASE, "RAPPORTO-classi-completo.md")
    with open(out_completo, "w", encoding="utf-8") as f:
        f.write(doc)
        f.write("\n---\n\n## Schede per classe (completo, con testo di fonte)\n\n")
        for c in classi_ord:
            f.write(scheda(c, completo=True) + "\n---\n\n")

    for p in (out, out_completo):
        testo = open(p, encoding="utf-8").read()
        print(f"scritto {p} ({len(testo):,} caratteri)".replace(",", "."))
    return S


if __name__ == "__main__":
    main()
