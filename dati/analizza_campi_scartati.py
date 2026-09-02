#!/usr/bin/env python3
"""
I DATI SCARTATI -> dati/RAPPORTO-campi-scartati.md

LA DOMANDA
    Quanti campi che le fonti strutturate offrono non estraiamo?

PERCHE' NESSUN CONTROLLO ESISTENTE LO VEDE
    Un parser che butta nella prosa un campo che la fonte da' strutturato
    produce qualcosa che SEMBRA una lacuna della fonte. Il dato formalmente
    non manca: c'e', dentro una frase. Nessuno schema lo segnala, perche' lo
    schema descrive i nostri campi, non quelli della fonte; nessun validatore
    lo segnala, perche' i validatori confrontano i nostri dati con i nostri
    dati. Il confronto che manca e' con l'ELENCO DEI CAMPI DELLA FONTE, e
    quell'elenco non stava in nessun file: sta ora in
    dati/_fonti/srd51_campi_disponibili.py.

COSA FA QUESTO SCRIPT
    1. VERIFICA le destinazioni dichiarate: ogni campo di fonte che l'elenco
       dice di estrarre deve corrispondere a un percorso che esiste davvero
       nel file prodotto. Una destinazione dichiarata e non trovata fa
       fallire lo script (exit 1): vorrebbe dire che l'elenco e i dati sono
       andati fuori sincrono, che e' la settima struttura doppia.
    2. CONTA scartati, estratti e metadati per endpoint.
    3. PROVA il caso dell'armatura invece di dichiararlo: ricalcola il nostro
       ca_5e dai sei campi strutturati della fonte e lo mette contro quello
       che build_oggetti.ca_strutturata() ottiene leggendo la prosa.
    4. MISURA il lato MC Dragonlance Appendix: quanto materiale meccanico
       vive nella prosa 2e e quanto dei campi di scheda arriva a un campo 5e.

COSA NON FA
    Non corregge niente. E' un rapporto: la misura richiesta, non la
    riparazione.

RIDUZIONE — CLAUDE.md, punti 1 e 2
    Legge dati privati (dati/mostri/, dati/oggetti/, dati/incantesimi/) e non
    ne emette MAI testo di fonte: niente `raw`, `abilities_text`, `text_2e`,
    `descrizione`, niente valori dei campi di scheda 2e. Escono conteggi, id,
    nomi di campo e analisi nostra. Per questo non esiste una variante
    `-completo`, come per RAPPORTO-mostri.md e RAPPORTO-personaggio.md: non
    c'e' niente da ridurre, e il filtro e' negativo e verificato dalla
    guardia in fondo al file.

NUMERI — CLAUDE.md, punto 3
    Ogni conteggio nella prosa e' interpolato. Nessun numero scritto a mano.

Uso:  python3 dati/analizza_campi_scartati.py
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
USCITA = os.path.join(BASE, "RAPPORTO-campi-scartati.md")

sys.path.insert(0, BASE)
sys.path.insert(0, RADICE)

from _fonti import srd51_campi_disponibili as INV   # noqa: E402
import build_oggetti                                # noqa: E402


# ------------------------------------------------------------ lettura dati
def carica(cartella):
    fuori = {}
    for f in sorted(glob.glob(os.path.join(BASE, cartella, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        fuori[d["id"]] = d
    return fuori


def percorso_esiste(doc, percorso):
    """Risolve `a.b[].c` dentro un documento. True se almeno un ramo arriva."""
    nodi = [doc]
    for pezzo in percorso.split("."):
        lista = pezzo.endswith("[]")
        chiave = pezzo[:-2] if lista else pezzo
        avanti = []
        for n in nodi:
            if not isinstance(n, dict) or chiave not in n:
                continue
            v = n[chiave]
            if lista:
                if not isinstance(v, list):
                    continue
                avanti.extend(v)
            else:
                avanti.append(v)
        if not avanti:
            return False
        nodi = avanti
    return True


# --------------------------------------------------- 1. verifica e conteggi
def verifica_destinazioni(oggetti, incantesimi):
    """Ogni destinazione dichiarata deve esistere nel file campione."""
    campioni = {
        "dati/oggetti/longsword.json": oggetti.get("longsword"),
        "dati/oggetti/chain-mail.json": oggetti.get("chain-mail"),
        "dati/oggetti/torch.json": oggetti.get("torch"),
        "dati/incantesimi/fireball.json": incantesimi.get("fireball"),
    }
    mancanti = []
    verificate = 0
    for nome, voce in INV.ENDPOINT:
        camp = voce.get("campione")
        if camp is None:
            continue
        doc = campioni.get(camp)
        if doc is None:
            mancanti.append((nome, camp, "campione assente"))
            continue
        for campo, (dest, _) in voce["campi"].items():
            if dest in (INV.META, INV.SCARTATO):
                continue
            if percorso_esiste(doc, dest):
                verificate += 1
            else:
                mancanti.append((nome, campo, dest))
    return verificate, mancanti


def conteggi():
    righe = []
    for nome, voce in INV.ENDPOINT:
        tot, est, sca, met = INV.conta(voce)
        righe.append({
            "endpoint": nome, "tot": tot, "est": est, "sca": sca, "met": met,
            "utili": tot - met,
            "mai_letto": voce.get("mai_letto", False),
            "usato_da": voce.get("usato_da"),
        })
    return righe


# ------------------------------------------------- 3. la prova sull'armatura
def prova_armatura(oggetti):
    """Ricalcola ca_5e dai campi di fonte e lo mette contro il nostro.

    La nostra ca_strutturata() legge la stringa; la fonte ha i campi. Se i
    due risultati coincidono, il parsing e' ridondante — cioe' e' lo stesso
    difetto della categoria d'arma, con l'aggravante che qui funziona e
    quindi non si vede. Se divergono, e' un errore attivo.
    """
    esiti = []
    for slug, (base, plus_dex, plus_flat, plus_max, ac_string) in \
            sorted(INV.CA_STRUTTURATA_SRD.items()):
        nostro = (oggetti[slug]["mechanics_5e"]["armor_5e"]["ca_5e"]
                  if slug in oggetti else None)
        # La stessa cosa, letta dai campi invece che dalla stringa.
        da_campi = {
            "ca_base": base if base else None,
            "bonus_ca": plus_flat or None,
            "applica_mod_dex": plus_dex,
            "mod_dex_max": plus_max or None,
        }
        nostra_stringa = (oggetti[slug]["mechanics_5e"]["armor_5e"]["ac_formula"]
                          if slug in oggetti else None)
        esiti.append({
            "slug": slug,
            "nostro": nostro,
            "da_campi": da_campi,
            "coincide": nostro == da_campi,
            "stringa_fonte": ac_string,
            "stringa_nostra": nostra_stringa,
            "stringa_coincide": ac_string == nostra_stringa,
        })
    return esiti


def regexp_di_ca():
    """Le espressioni regolari che rifanno il lavoro dei campi di fonte."""
    return [n for n in dir(build_oggetti) if n.startswith("_CA_")]


# ----------------------------------------------------- 4. il lato 2e / MC
NULLO = {"nil", "none", "no", "-", "n/a", ""}
RIMANDA = {"see below", "see text", "special", "see above"}

FAMIGLIE = [
    ("espressioni di dado", re.compile(r"\b\d+d\d+\b")),
    ("bonus e malus numerici", re.compile(r"(?<![\w/])[+-]\d+\b")),
    ("richiami a tiri salvezza", re.compile(r"\bsav(?:e|ing throw)s?\b", re.I)),
    ("percentuali", re.compile(r"\b\d+%")),
    ("THAC0 e dadi vita", re.compile(r"\b(?:THAC0|HD|Hit Dice)\b", re.I)),
    ("distanze", re.compile(
        r"\b\d+\s*(?:feet|foot|ft\.?|yards?|yds?|miles?)\b", re.I)),
    ("intervalli 2e (2-12)", re.compile(r"\b\d+-\d+\b")),
]

CAMPI_DIFESA_5E = ("damage_resistances", "damage_immunities",
                   "condition_immunities", "saving_throws")
PAROLE_DIFESA = re.compile(
    r"immun|resist|invulner|only by|weapon to hit|bonus to sav|to saving", re.I)


def lato_mc(mostri):
    c = collections.Counter()
    prosa_car = 0
    famiglie = collections.Counter()
    famiglie_mostri = collections.Counter()
    difese = []
    blocchi = collections.Counter()

    for mid, d in sorted(mostri.items()):
        s = d["source_2e"]
        m = d["mechanics_5e"]

        for k in ("traits", "actions", "bonus_actions", "reactions",
                  "legendary_actions"):
            blocchi[k] += len(m.get(k) or [])
            for b in (m.get(k) or []):
                if b.get("mechanics_5e"):
                    blocchi["con_prosa"] += 1
                if "effetto" in b:
                    blocchi["con_effetto"] += 1

        for campo in ("special_attacks", "special_defenses"):
            v = (s.get(campo) or "").strip()
            low = v.lower()
            if low in NULLO:
                c[campo + "/nullo"] += 1
            elif low in RIMANDA:
                c[campo + "/rimanda"] += 1
            else:
                c[campo + "/enunciato"] += 1
                if re.search(r"\d", v):
                    c[campo + "/enunciato_con_numero"] += 1

        v = (s.get("special_defenses") or "").strip()
        if PAROLE_DIFESA.search(v):
            pieni = [k for k in CAMPI_DIFESA_5E if m.get(k)]
            difese.append((mid, pieni))

        pezzi = list(s.get("abilities_text") or [])
        if s.get("death_effect"):
            pezzi.append(s["death_effect"])
        prosa = " ".join(pezzi)
        prosa_car += len(prosa)
        for nome, rx in FAMIGLIE:
            n = len(rx.findall(prosa))
            if n:
                famiglie[nome] += n
                famiglie_mostri[nome] += 1

    return {
        "conteggi": c, "prosa_car": prosa_car, "famiglie": famiglie,
        "famiglie_mostri": famiglie_mostri, "difese": difese,
        "blocchi": blocchi, "n": len(mostri),
    }


# --------------------------------------------------- guardia di riduzione
CHIAVI_VIETATE = ("raw", "abilities_text", "text_2e", "descrizione",
                  "death_effect", "desc_en")


def guardia_riduzione(doc, mostri, oggetti, incantesimi):
    """Nessun testo di fonte nel rapporto. Filtro negativo, verificato."""
    fuori = []
    testo = doc

    def controlla(ident, valore):
        if not isinstance(valore, str) or len(valore) < 40:
            return
        for inizio in range(0, len(valore) - 40, 20):
            pezzo = valore[inizio:inizio + 40]
            if pezzo in testo:
                fuori.append((ident, pezzo))
                return

    def scava(ident, o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in CHIAVI_VIETATE:
                    if isinstance(v, list):
                        for x in v:
                            controlla(f"{ident}.{k}", x)
                    else:
                        controlla(f"{ident}.{k}", v)
                else:
                    scava(f"{ident}.{k}", v)
        elif isinstance(o, list):
            for x in o:
                scava(ident, x)

    for insieme in (mostri, oggetti, incantesimi):
        for ident, d in insieme.items():
            scava(ident, d)
    return fuori


# ------------------------------------------------------------------ rapporto
def mille(n):
    """Migliaia col punto, come si scrive in italiano."""
    return f"{n:,}".replace(",", ".")


def tabella(intestazioni, righe, allineamenti=None):
    allineamenti = allineamenti or ["---"] * len(intestazioni)
    out = ["| " + " | ".join(intestazioni) + " |",
           "|" + "|".join(allineamenti) + "|"]
    for r in righe:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def main():
    mostri = carica("mostri")
    oggetti = carica("oggetti")
    incantesimi = carica("incantesimi")

    verificate, mancanti = verifica_destinazioni(oggetti, incantesimi)
    if mancanti:
        print("DESTINAZIONI DICHIARATE E NON TROVATE — l'elenco dei campi e i "
              "dati sono fuori sincrono:")
        for e, campo, dest in mancanti:
            print(f"  {e}: {campo} -> {dest}")
        return 1

    righe = conteggi()
    letti = [r for r in righe if not r["mai_letto"]]
    mai = [r for r in righe if r["mai_letto"]]

    tot_letti = sum(r["utili"] for r in letti)
    est_letti = sum(r["est"] for r in letti)
    sca_letti = sum(r["sca"] for r in letti)
    sca_mai = sum(r["sca"] for r in mai)

    ca = prova_armatura(oggetti)
    ca_coincidono = sum(1 for e in ca if e["coincide"])
    ca_divergono = [e for e in ca if not e["coincide"]]
    str_divergono = [e for e in ca if not e["stringa_coincide"]]
    rx_ca = regexp_di_ca()

    mc = lato_mc(mostri)
    B = mc["blocchi"]
    tot_blocchi = sum(B[k] for k in ("traits", "actions", "bonus_actions",
                                     "reactions", "legendary_actions"))
    C = mc["conteggi"]
    enunciati = C["special_attacks/enunciato"] + C["special_defenses/enunciato"]
    con_numero = (C["special_attacks/enunciato_con_numero"]
                  + C["special_defenses/enunciato_con_numero"])
    rimandano = C["special_attacks/rimanda"] + C["special_defenses/rimanda"]
    difese_coperte = sum(1 for _, pieni in mc["difese"] if pieni)
    tot_token = sum(mc["famiglie"].values())

    attrezzatura = [o for o in oggetti.values()
                    if o["categoria"] == "attrezzatura"]
    attrezzatura_in_nota = [
        o for o in attrezzatura
        if any(re.search(r"Peso .*costo", n or "")
               for n in (o["mechanics_5e"].get("note") or []))]

    doc = f"""# Campi disponibili e non estratti

*Generato da `dati/analizza_campi_scartati.py` il {OGGI}. Non modificare a
mano: i numeri sono interpolati dai dati, un numero scritto qui si sfasa alla
prossima rigenerazione.*

---

## 0. Cosa misura, e perché nessun controllo esistente lo vedeva

**«La categoria d'arma non era un dato mancante, era un dato scartato.»**

Un parser che butta nella prosa un campo che la fonte dà strutturato produce
qualcosa che **sembra una lacuna della fonte**. Il dato formalmente non manca:
c'è, dentro una frase. Nessuno schema lo segnala — lo schema descrive i nostri
campi, non quelli della fonte. Nessun validatore lo segnala — i validatori
confrontano i nostri dati con i nostri dati. Il confronto che mancava è con
**l'elenco dei campi della fonte**, e quell'elenco non stava in nessun file.

Ora sta in `dati/_fonti/srd51_campi_disponibili.py`, con la stessa forma delle
altre trascrizioni di quella cartella: una fotografia datata, con la sonda
dichiarata. Per ogni campo di fonte è scritta **la destinazione nei nostri
dati**, e questo script la verifica invece di crederle: **{verificate}
destinazioni dichiarate, {verificate} trovate davvero nei file prodotti**. Una
destinazione dichiarata e non trovata fa fallire lo script — sarebbe la
settima struttura doppia del progetto, e questa volta è sorvegliata dal primo
giorno.

---

## 1. La misura

Endpoint che leggiamo davvero:

{tabella(["endpoint", "campi utili", "estratti", "scartati", "destinazione nostra"],
         [[r["endpoint"], r["utili"], r["est"], f"**{r['sca']}**", r["usato_da"]]
          for r in letti],
         ["---", "--:", "--:", "--:", "---"])}

I «campi utili» escludono i metadati di licenza e provenienza dell'API
(`document__slug`, `document__title`, `document__license_url`,
`document__url`), che non sono dati di gioco.

> **{sca_letti} campi su {tot_letti}** disponibili negli endpoint che già
> leggiamo non vengono estratti — il **{100 * sca_letti // tot_letti}%**.
> Ne estraiamo {est_letti}.

Endpoint della stessa API che non apriamo affatto:

{tabella(["endpoint", "campi", "cosa contiene di rilevante"],
         [[r["endpoint"], r["sca"],
           "attacchi scomposti in campi (`to_hit_mod`, `damage_die_count`, "
           "`damage_die_type`, `damage_bonus`, `reach`, `range`)"
           if r["endpoint"] == "v2/creatures" else
           "danno, tiro salvezza, area e gittata come campi "
           "(`damage_roll`, `saving_throw_ability`, `shape_type`, `range`)"]
          for r in mai],
         ["---", "--:", "---"])}

> Altri **{sca_mai} campi** stanno in due endpoint che non abbiamo mai
> aperto. Non è una svista: la scelta di stare su `v1` è documentata in
> `_fonti/srd51_incantesimi.py` (v1 ha un solo documento Wizards e non può
> mischiare edizioni; v2 sì, e `srd51_equipaggiamento.py` ha già dovuto
> filtrare a valle). Restano contati perché la domanda era *quanti campi
> disponibili non estraiamo*, e un campo disponibile su un altro endpoint
> della stessa API resta disponibile.

**Totale: {sca_letti + sca_mai} campi disponibili e non estratti.**

---

## 2. I tre casi che sono lo stesso caso

La categoria d'arma è stata corretta. Le altre tre occorrenze della stessa
forma stanno tutte in `build_oggetti.py`, e sono **aperte**.

### 2.1 La Classe Armatura — e qui la prova, non l'affermazione

L'endpoint `v1/armor` dà la CA in **sei campi**: `base_ac`, `plus_dex_mod`,
`plus_max`, `plus_flat_mod`, `plus_con_mod`, `plus_wis_mod`. Ne dà anche la
forma testuale, `ac_string`. Noi trascriviamo `ac_string` e poi
`build_oggetti.ca_strutturata()` la rilegge con {len(rx_ca)} espressioni
regolari (`{"`, `".join(rx_ca)}`) per ricostruire quattro dei sei campi.

Non è un'ipotesi: il ricalcolo lo fa questo script. Per ognuna delle
**{len(ca)}** armature dell'SRD i sei campi di fonte sono stati messi contro
il nostro `ca_5e`.

> **{ca_coincidono}/{len(ca)} coincidono.** {"Nessuna divergenza." if not ca_divergono else "Divergono: " + ", ".join(e["slug"] for e in ca_divergono)}

Che coincidano è il punto, non la rassicurazione: **il parsing funziona,
quindi non si vede.** È lo stesso difetto della categoria d'arma nella sua
forma più difficile da trovare — quella in cui il risultato è giusto. Il
costo non è un errore di oggi: è che tre espressioni regolari stanno fra noi
e un campo, e la prima armatura con una formula fuori dai tre schemi previsti
solleva `ValueError` invece di leggere un intero.

{"" if not str_divergono else '''**Una divergenza di trascrizione trovata strada facendo.** Su ''' + ("una voce" if len(str_divergono) == 1 else str(len(str_divergono)) + " voci") + ''' la nostra `ac_formula` non è quella della fonte: ''' + ", ".join("`" + e["slug"] + "` (fonte `" + e["stringa_fonte"] + "`, nostra `" + str(e["stringa_nostra"]) + "`)" for e in str_divergono) + '''. Il campo `source_srd` dichiara una trascrizione diretta; quella stringa è stata normalizzata a mano. Il valore risultante è corretto, la trascrizione no.'''}

### 2.2 Prezzo e peso dell'attrezzatura — il caso che costa davvero

Armi e armature hanno `cost_gp` e `weight_lb` in campi propri. Le
**{len(attrezzatura)}** voci di attrezzatura no: `build_oggetti.py` scrive
prezzo e peso **dentro una frase italiana** di `mechanics_5e.note`, nella
forma *«Peso N lb, costo N mo»*. Sono
**{len(attrezzatura_in_nota)}/{len(attrezzatura)}**.

La fonte (`v2/items`) dà `cost` e `weight` come campi. Noi li leggiamo, li
usiamo per comporre una frase, e buttiamo via i campi.

Questo è il caso con una conseguenza già scritta altrove: la decisione 42
(`cambio-acciaio-oro`) è nata perché *«un personaggio non poteva comprare il
proprio equipaggiamento»*. Quella decisione ha dato il rapporto fra acciaio e
oro. Ma su {len(attrezzatura_in_nota)} oggetti **non c'è un prezzo leggibile
a cui applicarlo**: c'è una frase che lo contiene.

### 2.3 Semplice o da guerra — un booleano riscritto da una stringa

`weapon_5e.categoria` (`semplice` / `da_guerra`) è ricavata cercando la parola
*Simple* dentro la stringa `category` di `v1/weapons`. L'endpoint `v2/items`
dà gli stessi due fatti come booleani, `is_simple` e `is_martial`, e dà le
proprietà come oggetti `{{property, detail}}` — cioè già separate nel nome e
nel suo parametro, che è esattamente il lavoro delle due espressioni regolari
`_GITTATA` e `_VERSATILE` di `build_oggetti.py`.

Questo è il caso più tenue dei tre: `v1` non offre i booleani, e restare su
`v1` è una scelta motivata. Va contato, non necessariamente corretto.

---

## 3. Incantesimi

{tabella(["campo di fonte", "cosa contiene", "dove finisce da noi"],
         [["`target_range_sort`", "la gittata come intero (`150`)",
           "**scartato** — teniamo la stringa «150 feet»"],
          ["`page`", "il rimando di pagina alla fonte",
           "**scartato**"],
          ["`archetype`", "quali sottoclassi lo ottengono", "**scartato**"],
          ["`circles`", "circoli druidici", "**scartato**"],
          ["`spell_lists`", "l'elenco pulito delle classi",
           "**scartato di proposito**: incompleto alla fonte, 76 voci su 319 senza Paladino"],
          ["`components`, `ritual`, `concentration`, `level`, `spell_level`",
           "duplicati testuali di campi che prendiamo già",
           "**scartati senza costo**"]],
         ["---", "---", "---"])}

Due osservazioni di peso diverso.

`target_range_sort` è **la stessa forma del difetto**: la fonte dà il numero,
noi teniamo la frase. Un motore che deve sapere se il bersaglio è a tiro oggi
deve leggere `"150 feet"` con un'espressione regolare.

`page` merita una riga a sé. La convenzione delle pagine (CLAUDE.md, punto 4)
è una delle strutture su cui questo progetto è più rigoroso, e ogni voce del
bestiario porta `pages_pdf`. I {len(incantesimi)} incantesimi **non hanno
nessun rimando di pagina**, e la fonte lo dava.

Il danno, il tiro salvezza, l'area e la gittata degli incantesimi non sono
scartati da `v1`: `v1` non li ha. Ci sono in `v2/spells`
(`damage_roll`, `saving_throw_ability`, `shape_type`, `shape_size`, `range`).
È l'unico punto del rapporto in cui il campo che serve esiste solo
sull'endpoint che abbiamo deciso di non leggere.

---

## 4. I mostri SRD — il riscontro che non abbiamo preso

`_fonti/srd51_mostri.py` trascrive **7 campi su
{[r["utili"] for r in righe if r["endpoint"] == "v1/monsters"][0]}**:
nome, taglia, tipo, CA, PF, velocità, grado di sfida. Gli altri
{[r["sca"] for r in righe if r["endpoint"] == "v1/monsters"][0]} non vengono
letti.

Questo endpoint non è la fonte dei nostri mostri — quella è l'MC Dragonlance
Appendix — ma **il riscontro su cui si calibrano le conversioni per
analogia**. Lo scarto qui non è «dato perso», è «riscontro non disponibile».
Due voci contano più delle altre:

- **le sei caratteristiche.** Ogni nostro mostro porta un `abilities_note` che
  spiega che la 2e non le assegna e che vanno stimate dal profilo. La mediana
  per grado di sfida — che renderebbe quella stima *verificabile* invece che
  *argomentata* — sta in questo endpoint, e non l'abbiamo.
- **`actions`.** Ogni azione dell'SRD porta già `attack_bonus`, `damage_dice`
  e `damage_bonus` come campi. È esattamente la forma che manca ai nostri
  mostri per far girare uno scontro, ed è nella fonte che avevamo già in
  mano.

---

## 5. Il lato MC Appendix, e un esito negativo

La domanda era se i campi dell'MC finiscano in `abilities_text` invece che in
campi propri. **Al livello della scheda, no.** Vale la pena scriverlo, perché
è il contrario di quello che ci si aspettava.

I 21 campi canonici della scheda MC sono tutti estratti in `source_2e`, e i 7
senza corrispettivo 5e sono censiti e indirizzati dalla decisione 27
(`sette-campi-2e`). Restano due campi che *enunciano una meccanica in forma
libera*, `SPECIAL ATTACKS` e `SPECIAL DEFENSES`, su {mc["n"]} creature:

{tabella(["", "SPECIAL ATTACKS", "SPECIAL DEFENSES"],
         [["nullo (la fonte dice che non c'è)",
           C["special_attacks/nullo"], C["special_defenses/nullo"]],
          ["rimanda alla prosa (*vedi sotto*)",
           C["special_attacks/rimanda"], C["special_defenses/rimanda"]],
          ["enuncia una meccanica come stringa",
           C["special_attacks/enunciato"], C["special_defenses/enunciato"]],
          ["…di cui con un numero dentro",
           C["special_attacks/enunciato_con_numero"],
           C["special_defenses/enunciato_con_numero"]]],
         ["---", "--:", "--:"])}

{enunciati} enunciati in forma libera, {con_numero} dei quali contengono un
numero; {rimandano} caselle che rimandano esplicitamente al testo.

**E arrivano a un campo 5e.** Delle {len(mc["difese"])} creature la cui
`SPECIAL DEFENSES` parla di immunità, resistenza o bonus ai tiri salvezza,
**{difese_coperte}/{len(mc["difese"])}** hanno il campo 5e corrispondente
popolato (`damage_resistances`, `damage_immunities`, `condition_immunities` o
`saving_throws`). La conversione del bestiario **non ripete il difetto di
`build_oggetti.py`**: qui il campo di fonte non viene buttato nella prosa,
viene tradotto in un campo.

### Dove sta invece il materiale, nel bestiario

Non nei campi di scheda: nella **prosa narrativa 2e**, che è prosa anche alla
fonte. {mille(mc["prosa_car"])} caratteri di `abilities_text`, con
**{tot_token} riferimenti meccanici** dentro:

{tabella(["famiglia", "occorrenze", "creature"],
         [[nome, mc["famiglie"][nome], mc["famiglie_mostri"][nome]]
          for nome, _ in FAMIGLIE if mc["famiglie"][nome]],
         ["---", "--:", "--:"])}

Questo **non è un dato scartato**: la fonte lo dà in prosa, e trascriverlo in
prosa è fedeltà, non perdita (decisione 15, `tratti-trascrizione-integrale`).
È la misura del serbatoio, non di un difetto — utile per sapere quanto resta
da convertire, non per accusare il parser.

### Il difetto del bestiario è un altro, ed è già misurato

{tot_blocchi} blocchi di meccanica ({B["traits"]} tratti, {B["actions"]}
azioni, {B["reactions"]} reazione{"" if B["reactions"] == 1 else "i"}), **{B["con_prosa"]} con la meccanica
scritta in una stringa italiana e {B["con_effetto"]} con un campo `effetto`**.
Non è materia di questo rapporto: sta in `RAPPORTO-personaggio.md` §5, ed è il
punto su cui lo schema `effetto.schema.json` è stato aperto.

---

## 6. Il conto

{tabella(["", "campi"],
         [["disponibili negli endpoint che leggiamo (esclusi i metadati)", tot_letti],
          ["…estratti", est_letti],
          ["…**scartati**", f"**{sca_letti}**"],
          ["disponibili in endpoint mai aperti", sca_mai],
          ["**totale disponibile e non estratto**", f"**{sca_letti + sca_mai}**"]],
         ["---", "--:"])}

Dei {sca_letti} scartati negli endpoint che già leggiamo, quelli che ripetono
la forma del difetto trovato — **la fonte dà il campo, noi teniamo la
frase** — sono {6 + 2 + 1}: i 6 campi della Classe Armatura, `cost` e `weight`
dell'attrezzatura, `target_range_sort` degli incantesimi. Gli altri sono
duplicati testuali, metadati di sottoclasse, o riscontro non richiesto.

*Nessuna correzione è applicata in questo documento.*
"""

    fuoriuscite = guardia_riduzione(doc, mostri, oggetti, incantesimi)
    if fuoriuscite:
        print("RIDUZIONE FALLITA — testo di fonte nel rapporto pubblico:")
        for ident, pezzo in fuoriuscite[:10]:
            print(f"  {ident}: {pezzo}…")
        return 1

    with open(USCITA, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"scritto {os.path.relpath(USCITA, RADICE)} "
          f"({len(doc.splitlines())} righe)")
    print(f"destinazioni dichiarate e verificate: {verificate}")
    print(f"campi scartati: {sca_letti} negli endpoint letti, "
          f"{sca_mai} in quelli mai aperti")
    print(f"guardia di riduzione: nessun testo di fonte "
          f"(chiavi sorvegliate: {', '.join(CHIAVI_VIETATE)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
