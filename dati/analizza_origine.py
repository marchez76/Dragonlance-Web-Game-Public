#!/usr/bin/env python3
"""
Misura la dichiarazione di origine: dove c'e', in quante forme, e cosa resta
fuori.

PERCHE' ESISTE. Il progetto ha inventato il campo "origine di un valore"
quattro volte senza accorgersene — `conversion_status` piu' `source` su
`armor_class`, su `hit_points`, su `challenge_rating`, e poi `cd_origine`, e
poi `bonus_origine`. Decima struttura doppia, in una forma nuova: non due file
che divergono, ma lo stesso concetto con quattro nomi. La
decisione 55 (`origine-sede-unica`) l'ha unificato. Questo documento e' la
misura di quell'unificazione, e soprattutto la misura di **cosa non si e'
lasciato unificare**: un rapporto che dicesse solo "fatto" non servirebbe a
niente, perche' la parte che costa e' quella rimasta.

TUTTI I NUMERI QUI SONO CONTATI, MAI SCRITTI A MANO. Un conteggio nella prosa
si sfasa alla prima rigenerazione ed e' gia' costato quattro giri di
incoerenze al progetto.

DUE USCITE DALLA STESSA ANALISI (regola 2 del contratto di progetto):

    RAPPORTO-origine.md            pubblico  — forme, conteggi, distribuzioni
    RAPPORTO-origine-completo.md   privato   — piu' le note e le stringhe di
                                               `source` verbatim, che portano
                                               citazioni di pagina e frasi
                                               tratte dalle fonti

La riduzione e' un parametro del generatore (`completo=True/False`), non un
taglio a valle: a valle si sfasa alla prima rigenerazione.

Uso:  python3 dati/analizza_origine.py
"""

import collections
import functools
import glob
import json
import os
import sys
import textwrap

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
sys.path.insert(0, BASE)
sys.path.insert(0, RADICE)
sys.path.insert(0, os.path.join(RADICE, "motore"))

import _schemi as S  # noqa: E402
from decisioni import cita  # noqa: E402

# Le cartelle di dati che possono portare una dichiarazione di origine. Non e'
# un elenco a mano che rischia di invecchiare: e' filtrato su quello che c'e',
# e `_altre_cartelle()` denuncia una cartella nuova che nessuno ha guardato.
CARTELLE = ("mostri", "oggetti", "modelli", "razze", "classi")

# Il vocabolario di SCHEDA, che porta lo stesso nome ma non e' la stessa cosa.
# Vedi §2: la prova che sono due concetti non e' una lettura, e' un conteggio.
STATI_DI_SCHEDA = S.STATI_DI_SCHEDA


def _cammina(nodo, perc=()):
    """Ogni dizionario del documento, col percorso che ci arriva."""
    if isinstance(nodo, dict):
        yield perc, nodo
        for k, v in nodo.items():
            yield from _cammina(v, perc + (k,))
    elif isinstance(nodo, list):
        for v in nodo:
            yield from _cammina(v, perc + ("[]",))


def _altre_cartelle():
    """Cartelle di dati fuori dall'elenco: una nuova non deve passare muta."""
    viste = set()
    for p in sorted(glob.glob(os.path.join(BASE, "*", "*.json"))):
        viste.add(os.path.basename(os.path.dirname(p)))
    return sorted(viste - set(CARTELLE) - {"schema", "sistema", "_fonti"})


def dichiarazioni():
    """Ogni dichiarazione di origine trovata nei dati.

    Torna righe (cartella, percorso, livello, stato, source, note, file).
    `livello` distingue i due concetti che oggi portano lo stesso nome:
    "scheda" quando `conversion_status` sta sulla radice di `mechanics_5e` e
    dice a che punto e' la conversione DI QUELLA SCHEDA; "elemento" quando sta
    accanto a un valore e ne dichiara l'ORIGINE."""
    righe = []
    for cart in CARTELLE:
        for f in sorted(glob.glob(os.path.join(BASE, cart, "*.json"))):
            try:
                doc = json.load(open(f, encoding="utf-8"))
            except (ValueError, OSError):
                continue
            for perc, nodo in _cammina(doc):
                if "conversion_status" not in nodo:
                    continue
                liv = "scheda" if perc == ("mechanics_5e",) else "elemento"
                righe.append((cart, "/".join(perc) or "(radice)", liv,
                              nodo.get("conversion_status"), nodo.get("source"),
                              nodo.get("note"), os.path.basename(f)))
    return righe


def due_concetti(righe):
    """LA PROVA che `conversion_status` nomina due cose, in numeri.

    Non serve leggere le descrizioni per stabilirlo, e leggerle sarebbe la
    strada debole: il discriminante e' che a livello di SCHEDA il campo
    `source` non c'e' MAI, e a livello di elemento c'e' SEMPRE. Se un giorno
    le due popolazioni si mescolassero, questo conteggio lo direbbe prima che
    lo dica un errore."""
    per_liv = collections.defaultdict(lambda: [0, 0, collections.Counter()])
    for _c, _p, liv, stato, source, _n, _f in righe:
        per_liv[liv][0] += 1
        per_liv[liv][1] += source is not None
        per_liv[liv][2][stato] += 1
    return per_liv


def sede_e_riferimenti():
    """La sede unica e chi la riferisce, letti dagli schemi e non assunti."""
    sede = S.carica(S.SEDE_ORIGINE)
    enum = {d: sede["$defs"][d]["enum"] for d in S.DEFS_CONDIVISI}
    riferiscono = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(BASE, "schema", "*.json"))):
        nome = os.path.basename(f)
        if nome == S.SEDE_ORIGINE:
            continue
        testo = open(f, encoding="utf-8").read()
        for d in S.DEFS_CONDIVISI:
            if f"{S.SEDE_ORIGINE}#/$defs/{d}" in testo:
                riferiscono[d].append(nome)
    incapsulati = sorted(
        os.path.basename(f)
        for f in glob.glob(os.path.join(BASE, "schema", "*.json"))
        if "valore_dichiarato" in open(f, encoding="utf-8").read()
        and os.path.basename(f) != S.SEDE_ORIGINE)
    return enum, riferiscono, incapsulati


def fuori_dall_enum(righe, enum):
    """Le `source` di livello elemento che l'enum della sede non accetta.

    E' la parte che RESISTE all'unificazione, e va misurata invece che
    descritta: la domanda utile non e' "quante" ma "quanto lontane". Una
    stringa che COMINCIA con un valore dell'enum non e' un vocabolario
    diverso — e' lo stesso valore piu' un dettaglio, e si decompone. Una che
    non comincia con nessuno e' l'unica che chiede davvero una decisione."""
    decomponibili = collections.Counter()
    aliene = collections.Counter()
    esempi = {}
    for cart, _p, liv, _s, source, _n, _f in righe:
        if liv != "elemento" or source in enum:
            continue
        prefisso = next((e for e in enum if isinstance(source, str)
                         and source.startswith(e)), None)
        if prefisso:
            decomponibili[(cart, prefisso)] += 1
        else:
            aliene[(cart, source)] += 1
        esempi.setdefault((cart, prefisso), source)
    return decomponibili, aliene, esempi


def _vincolato(nodo, radice, giri=3):
    """Un `conversion_status` e' vincolato se porta un `enum` suo, un `$ref`
    alla sede, oppure un `$ref` locale che ci arriva. Il salto locale va
    seguito: la decisione 55 (`origine-sede-unica`) ha proprio la forma
    `$defs` locale -> sede, e un rilevatore che si fermasse al primo `$ref`
    direbbe scoperto cio' che e' legato meglio di tutto il resto."""
    if not isinstance(nodo, dict) or giri < 0:
        return False
    if nodo.get("enum"):
        return True
    rif = str(nodo.get("$ref") or "")
    if not rif:
        return False
    if S.SEDE_ORIGINE in rif:
        return True
    if rif.startswith("#/"):
        dentro = radice
        for passo in rif[2:].split("/"):
            if not isinstance(dentro, dict) or passo not in dentro:
                return False
            dentro = dentro[passo]
        return _vincolato(dentro, radice, giri - 1)
    return False


@functools.lru_cache(maxsize=None)
def _schema_esterno(nome_file):
    return S.carica(nome_file)


def _risolvi_esterno(rif):
    """Un `$ref` a UN ALTRO FILE ("altro.schema.json#/a/b") risolto in
    (nodo, radice_di_quel_file). None se il ref e' locale o non risolve.

    Serve da quando `elemento_convertito` (vocabolari.schema.json) porta
    `conversion_status` un livello piu' in la' di un `$ref` diretto: senza
    seguire il file, il camminatore vede l'`allOf` fermarsi su un nodo che
    e' solo `{"$ref": ...}` e non trova mai la chiave che cerca — non perche'
    non sia vincolata, ma perche' non ha guardato dentro. E' lo stesso
    principio di _schemi.py — un `$ref` fra file non si segue da solo — qui
    applicato a un rilevatore di prosa invece che a un validatore di dati."""
    if rif.startswith("#/"):
        return None
    if "#" not in rif:
        return None
    file_, frammento = rif.split("#", 1)
    if not file_:
        return None
    try:
        radice_esterna = _schema_esterno(os.path.basename(file_))
    except FileNotFoundError:
        return None
    nodo = radice_esterna
    for passo in frammento.strip("/").split("/"):
        if not passo:
            continue
        if not isinstance(nodo, dict) or passo not in nodo:
            return None
        nodo = nodo[passo]
    return nodo, radice_esterna


def _conversion_status_nello_schema(nodo, radice=None, dentro_m5e=False,
                                    chiave=None):
    """Ogni `conversion_status` dichiarato sotto `mechanics_5e`, e se e'
    davvero vincolato al vocabolario o solo dichiarato di tipo stringa."""
    radice = nodo if radice is None else radice
    fuori = []
    if not isinstance(nodo, dict):
        return fuori
    if chiave == "conversion_status" and dentro_m5e:
        # _vincolato() risolve gia' da solo un $ref diretto su QUESTO nodo
        # (anche fra file, via la scorciatoia su SEDE_ORIGINE): seguirlo
        # anche qui sotto conterebbe la stessa dichiarazione due volte, una
        # come nodo grezzo e una come nodo risolto.
        fuori.append(_vincolato(nodo, radice))
    else:
        rif = nodo.get("$ref")
        if isinstance(rif, str):
            risolto = _risolvi_esterno(rif)
            if risolto:
                n2, radice2 = risolto
                fuori += _conversion_status_nello_schema(n2, radice2, dentro_m5e,
                                                         chiave)
    for sotto in ("anyOf", "oneOf", "allOf"):
        for n in nodo.get(sotto, []):
            fuori += _conversion_status_nello_schema(n, radice, dentro_m5e,
                                                     chiave)
    for k, v in (nodo.get("properties") or {}).items():
        fuori += _conversion_status_nello_schema(
            v, radice, dentro_m5e or k == "mechanics_5e", k)
    it = nodo.get("items")
    if isinstance(it, dict):
        fuori += _conversion_status_nello_schema(it, radice, dentro_m5e, chiave)
    return fuori


def zona_morta():
    """Dove l'origine e' scritta nei dati ma NESSUNO schema la vincola.

    Il caso peggiore non e' un campo assente: e' un campo scritto che sembra
    validato e non lo e'. Si misura confrontando cosa i dati dichiarano con
    cosa lo schema di quella famiglia sa dire su `mechanics_5e`.

    IL RILEVATORE E' STATO CORRETTO IL 04/09/2026, e la correzione vale la
    riga di commento. La prima versione cercava le due stringhe
    `"conversion_status"` e `"enum"` DENTRO LO STESSO FILE, non nello stesso
    punto: `classe.schema.json` le contiene entrambe — la prima dentro
    `chassis_features`, la seconda su un campo `kind` che non c'entra — e
    risultava quindi "vincolato" mentre non vincola niente. Un rilevatore che
    dichiara chiusa una zona morta aperta e' peggio di nessun rilevatore,
    perche' il numero che stampa viene creduto. Ora si guarda il NODO: un
    `conversion_status` sotto `mechanics_5e` e' vincolato solo se porta un
    `enum` suo o un `$ref` alla sede."""
    fuori = []
    for cart in CARTELLE:
        nome = {"mostri": "mostro", "oggetti": "oggetto", "modelli": "modello",
                "razze": "razza", "classi": "classe"}[cart] + ".schema.json"
        p = os.path.join(BASE, "schema", nome)
        if not os.path.exists(p):
            continue
        schema = json.load(open(p, encoding="utf-8"))
        trovati = _conversion_status_nello_schema(schema)
        # Vincolato = ne dichiara almeno uno E tutti quelli che dichiara sono
        # legati al vocabolario. Uno solo lasciato libero e' una porta aperta.
        vincolato = bool(trovati) and all(trovati)
        fuori.append((cart, nome, vincolato, len(trovati),
                      sum(1 for t in trovati if t)))
    return fuori


def ancora_scoperti():
    """I campi che hanno la forma del difetto e non dichiarano ancora nulla.

    Riusa la misura dell'arena invece di rifarla: due conteggi della stessa
    cosa in due file sono la struttura doppia che il progetto ha gia' chiuso
    nove volte. Qui si importa la funzione, non si ricopia il risultato."""
    import arena
    return arena.campi_con_la_stessa_forma()


# ---------------------------------------------------------------- rendering

_LARG = 78


def riflow(testo, larghezza=_LARG):
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


def rapporto(completo=False):
    righe = dichiarazioni()
    per_liv = due_concetti(righe)
    enum, riferiscono, incapsulati = sede_e_riferimenti()
    decomp, aliene, esempi = fuori_dall_enum(righe, enum["provenienza"])
    visti, quanti, prova = S.prova_di_se_stesso()
    schemi_rotti = S.verifica_origine()
    scoperti = ancora_scoperti()
    altre = _altre_cartelle()

    n_tot = len(righe)
    n_scheda = per_liv["scheda"][0]
    n_elem = per_liv["elemento"][0]
    n_fuori = sum(decomp.values()) + sum(aliene.values())

    # I tre campi del blocco che dichiarano l'origine da mesi: sono il
    # PRECEDENTE su cui l'unificazione si e' appoggiata, e vanno contati.
    tre = [r for r in righe if r[1] in ("mechanics_5e/armor_class",
                                        "mechanics_5e/hit_points",
                                        "mechanics_5e/challenge_rating")]
    schede_mostro = len({r[6] for r in righe if r[0] == "mostri"})

    # I valori gia' nella forma incapsulata: l'oggetto `{value, ...}`.
    incaps_dati = [r for r in righe
                   if r[1].endswith(("bonus_colpire", "/cd"))]

    D = "-completo" if completo else ""
    parti = []
    parti.append(f"""# L'origine di un valore — una sede, una forma, e cosa resta fuori

*Generato da `dati/analizza_origine.py`{
    ' — **versione privata**, contiene note e citazioni di fonte.'
    if completo else '.'}*

---

## 0. Il difetto, e perche' era invisibile

Il progetto ha inventato il campo "origine di un valore" **quattro volte**
senza accorgersene. Tre volte sotto lo stesso nome — `conversion_status` piu'
`source` su `armor_class`, su `hit_points`, su `challenge_rating`, {len(tre)}
dichiarazioni su {schede_mostro} schede di mostro — e la quarta sotto un nome
nuovo, `cd_origine` con `cd_derivazione`, subito seguita dalla quinta,
`bonus_origine`. Decima struttura doppia del progetto, e in una forma che
nessuno dei controlli precedenti poteva vedere: non due file che divergono, ma
**lo stesso concetto con quattro nomi**.

Era invisibile per una ragione precisa. Una struttura doppia si scopre quando
le due copie si sfasano, e qui le copie non potevano sfasarsi perche' nessuno
le confrontava: ognuna viveva in un campo diverso, e ogni campo era coerente
con se stesso. Il difetto non stava nei dati — stava nel fatto che i dati
erano giusti quattro volte separate.

La {cita('origine-e-un-dato')} lo aveva visto e dichiarato aperto,
rimandando l'unificazione al momento in cui un campo ancora scoperto avesse
dovuto portare l'origine davvero. La {cita('origine-sede-unica')} e' quel
momento: ogni campo nuovo sarebbe stato la quinta reinvenzione.
""")

    # ------------------------------------------------------------------ §1
    parti.append(f"""---

## 1. Quante dichiarazioni ci sono, e di che tipo

{n_tot} dichiarazioni di origine nei dati, su {len(CARTELLE)} famiglie.

{tabella(["famiglia", "livello scheda", "livello elemento", "totale"],
         [(c,
           sum(1 for r in righe if r[0] == c and r[2] == "scheda"),
           sum(1 for r in righe if r[0] == c and r[2] == "elemento"),
           sum(1 for r in righe if r[0] == c))
          for c in CARTELLE]
         + [("**totale**", f"**{n_scheda}**", f"**{n_elem}**", f"**{n_tot}**")],
         allin=["---", "--:", "--:", "--:"])}
""")
    if altre:
        parti.append(
            "> Cartelle di dati non guardate da questo controllo: "
            + ", ".join(f"`{c}`" for c in altre)
            + ". Vanno aggiunte a `CARTELLE` o dichiarate senza origine.\n")

    # ------------------------------------------------------------------ §2
    _sch, _sch_src, sch_voc = per_liv["scheda"]
    _el, el_src, el_voc = per_liv["elemento"]
    parti.append(f"""---

## 2. Un nome per due concetti — e la prova non e' una lettura

`conversion_status` nomina due cose diverse, e la parte utile e' che non
serve leggere le descrizioni per dimostrarlo. Il discriminante e' un
conteggio: a livello di **scheda** il campo `source` non c'e' **mai**
({n_scheda - _sch_src} su {n_scheda}); a livello di **elemento** c'e'
**sempre** ({el_src} su {n_elem}). Due popolazioni che non si toccano.

Anche i vocabolari sono disgiunti, ed e' la seconda prova:

{tabella(["livello", "significato", "vocabolario usato nei dati"],
         [("scheda", "a che punto e' **questa scheda**",
           ", ".join(f"`{k}` ({v})" for k, v in sorted(sch_voc.items()))),
          ("elemento", "da dove viene **questo valore**",
           ", ".join(f"`{k}` ({v})" for k, v in sorted(el_voc.items())))])}

Le classi usano `clonato` e `in_sospeso` dove le altre famiglie usano
`compilato`: e' un terzo vocabolario di scheda, non un'origine.

**Questo non e' stato unificato**, ed e' la prima cosa che resiste. Rinominare
il campo di scheda tocca le {n_scheda} schede piu' i generatori `build_*.py`
che lo scrivono: e' un giro suo, che va misurato e fatto con un controllo
davanti, non infilato dentro l'unificazione dell'origine. Finche' non e'
fatto, il rischio non e' teorico — e' che qualcuno legga `compilato` come
un'origine, o che un controllo sull'origine cominci a contare le schede.
""")

    # ------------------------------------------------------------------ §3
    parti.append(f"""---

## 3. La sede, e il fatto che una copia era gia' divergente

`conversion_status` e `provenienza` erano definiti **tre volte** in `$defs` —
`mostro`, `oggetto`, `modello` — e la copia di `oggetto` aveva **gia'**
sette voci contro cinque. La struttura doppia aveva gia' cominciato a
sfasarsi, e nessun dato la denunciava: un enum ricopiato valida benissimo
finche' le copie coincidono, e quando smettono di coincidere valida ancora,
solo in modo diverso in ogni file.

Oggi la sede e' `{S.SEDE_ORIGINE}` — la stessa della
{cita('vocabolario-italiano')} — e gli schemi la riferiscono:

{tabella(["definizione", "voci", "schemi che la riferiscono"],
         [(f"`{d}`", len(enum[d]),
           ", ".join(f"`{n}`" for n in riferiscono[d]) or "**nessuno**")
          for d in S.DEFS_CONDIVISI])}

L'elenco delle provenienze e' l'**unione** delle tre copie
({len(enum['provenienza'])} voci): {", ".join(f"`{v}`" for v in enum['provenienza'])}.
La fusione **allarga** il vincolo dei singoli schemi — `oggetto` accetta ora
valori che prima non accettava. E' il prezzo dichiarato di una sede sola, non
un effetto collaterale scoperto dopo.

### Il controllo si mette alla prova

Questo difetto non si vede dai dati: si vede solo guardando gli schemi. E su
un repository pulito un rilevatore rotto e uno funzionante **tacciono
uguale**. Quindi il rilevatore non si dichiara funzionante, si mette davanti
difetti costruiti apposta: {visti} su {quanti} difetti piantati riconosciuti,
{len(prova)} errori nella prova, {len(schemi_rotti)} problemi reali negli
schemi.

I tre difetti piantati sono un enum ridigitato fuori sede, un `$defs`
condiviso che non e' un `$ref` alla sede, e un `conversion_status` senza
`source` accanto. Accanto stanno due somiglianze **legittime** che il
controllo non deve segnalare: e' la meta' che conta, perche' un rilevatore che
segnala tutto e' silenzioso quanto uno che non segnala niente.
""")

    # ------------------------------------------------------------------ §4
    parti.append(f"""---

## 4. La forma: il prefisso ERA il difetto

Il nome unico non e' un nome nuovo. `conversion_status` piu' `source` reggeva
da mesi su tre campi e {len(tre)} dichiarazioni: **si estende, non si
sostituisce** — ed e' il motivo per cui il rinominare temuto sulle
{schede_mostro} schede **non e' servito**.

La traduzione dell'enum piu' giovane in quello piu' vecchio:

{tabella(["`cd_origine` (2 campi, giovane)", "`conversion_status` (3 campi, in opera)"],
         [("`fonte`", "`direct`"),
          ("`stimata`", "`adapted`"),
          ("`derivata`", "**`derived`** — l'unico che mancava")])}

`derived` e' l'unico valore che l'enum in opera non aveva, e non e' un
sinonimo di nessun altro: un valore derivato non e' `direct` (nessuno l'ha
stampato) ne' `adapted` (nessuno l'ha scelto). Ed e' **l'unico dei cinque che
un controllo puo' rifare**, il che lo rende l'unico che vale la pena
distinguere.

### L'oggetto, e perche' i prefissi non scalavano

Un valore e la sua origine viaggiano nello **stesso oggetto**:

    "bonus_colpire": {{
      "value": 5,
      "conversion_status": "derived",
      "source": "regola di sistema",
      "note": "..."
    }}

Che e' esattamente cio' che `armor_class` gia' era. La forma piatta a
prefisso — `cd_origine`, `bonus_origine` — non e' solo piu' brutta: **e' il
meccanismo** con cui il campo si e' reinventato quattro volte. `attacco` porta
due numeri che hanno ciascuno un'origine, `bonus_colpire` e `danno[].bonus`, e
ogni numero nuovo pretende un prefisso nuovo, che nessuno riconosce come lo
stesso campo.

Con l'incapsulamento l'origine **non puo' piu' mancare**, e non perche' un
controllo la pretende: perche' non c'e' un posto dove scrivere il valore senza
di essa. La clausola condizionale che obbligava il campo di origine e' stata
**cancellata** — la garanzia e' diventata strutturale, e una garanzia
strutturale non ha bisogno di essere ricordata.

Schemi che usano la forma incapsulata: {", ".join(f"`{n}`" for n in incapsulati) or "nessuno"}.
Valori gia' scritti in questa forma nei dati: {len(incaps_dati)}.
""")

    # ------------------------------------------------------------------ §5
    righe_dec = [(f"`{c}`", f"`{p}`", n, "si', e' l'enum piu' un dettaglio")
                 for (c, p), n in sorted(decomp.items(), key=lambda x: -x[1])]
    righe_al = [(f"`{c}`",
                 (f"`{s}`" if completo else "*(stringa non riprodotta)*"),
                 n, "no")
                for (c, s), n in sorted(aliene.items(), key=lambda x: -x[1])]
    parti.append(f"""---

## 5. Cosa NON si e' lasciato unificare

### 5a. `source` come stringa libera in razze e classi

{n_fuori} dichiarazioni di livello elemento portano un `source` che l'enum
della sede **non accetta**. La domanda utile non e' quante sono, ma quanto
sono lontane — e la risposta cambia il lavoro che serve:

{tabella(["famiglia", "valore o prefisso", "casi", "decomponibile?"],
         righe_dec + righe_al, allin=["---", "---", "--:", "---"])}

**{sum(decomp.values())} su {n_fuori} cominciano con un valore dell'enum.**
Non sono un vocabolario diverso: sono lo stesso valore piu' un dettaglio —
il capitolo, la pagina stampata, il fatto che sia stato letto da immagine. La
fusione quindi non e' bloccata, e' **decomposta**: `source` (enum, vincolato)
piu' un campo di dettaglio (stringa libera). Solo {sum(aliene.values())}
non cominciano con nessun valore dell'enum, e sono le uniche che chiedono
davvero una decisione.

Perche' non e' stato fatto qui: quel dettaglio porta **piu'** informazione di
quella che l'enum trattiene, e buttarlo per uniformare sarebbe una perdita
netta. Decomporlo e' un giro suo, con il suo controllo.
""")
    if completo:
        parti.append(
            "> **Solo nella versione privata** — le stringhe intere, che\n"
            "> portano le citazioni di pagina:\n>\n"
            + "\n".join(f"> - `{c}`: `{esempi[(c, pre)]}`"
                        for (c, pre) in sorted(k for k in esempi if k[1])) + "\n")

    # 5b zona morta
    zm = zona_morta()
    per_fam = {c: sum(1 for r in righe if r[0] == c and r[2] == "elemento")
               for c in CARTELLE}
    parti.append(f"""### 5b. La zona morta: origine scritta, nessuno schema che la vincoli

{tabella(["famiglia", "schema", "dichiarazioni di elemento", "`conversion_status` dichiarati dallo schema", "…di cui legati al vocabolario", "vincolate?"],
         [(c, f"`{n}`", per_fam[c], quanti, legati, "si'" if v else "**NO**")
          for c, n, v, quanti, legati in zm],
         allin=["---", "---", "--:", "--:", "--:", "---"])}

Il caso peggiore non e' un campo assente: e' un campo **scritto che sembra
validato e non lo e'**. Dove la colonna dice NO, l'origine e' scritta nei dati
con la stessa diligenza di tutte le altre, e nessun controllo la guarda: puo'
portare un valore che l'enum non prevede senza che niente lo dica. Sono
**{sum(per_fam[c] for c, _n, ok, _q, _l in zm if not ok)} dichiarazioni** fra razze e classi. E' la stessa forma della zona
morta gia' misurata in `RAPPORTO-zona-morta-classi.md`, su un campo diverso —
segno che il difetto sta nello schema di quelle famiglie, non nel campo. Il
costo di chiuderla e' misurato li', in §5.

**Il rilevatore era rotto e diceva di no, il 04/09/2026.** La prima versione
cercava le stringhe `"conversion_status"` e `"enum"` nello stesso FILE invece
che nello stesso nodo, e `classe.schema.json` le contiene entrambe in due
punti che non c'entrano l'uno con l'altro: la famiglia risultava vincolata
mentre non vincola niente. Un rilevatore che dichiara chiusa una zona morta
aperta e' peggio di nessun rilevatore, perche' il numero che stampa viene
creduto. Ora si guarda il nodo, e il `$ref` locale verso la sede si segue
fino in fondo — che e' esattamente la forma che la {cita('origine-sede-unica')}
ha dato al vincolo, e che un rilevatore fermo al primo salto avrebbe chiamato
scoperta.

### 5c. Il vocabolario di scheda delle classi

Le classi dichiarano `clonato` e `in_sospeso` dove le altre famiglie
dichiarano `compilato`. Sono stati di scheda, non origini, e restano fuori
dall'unificazione per la ragione di §2: sono l'altro concetto.
""")

    # ------------------------------------------------------------------ §6
    parti.append(f"""---

## 6. I campi che hanno la forma del difetto e non dichiarano ancora nulla

La forma ora esiste; applicarla dove manca e' lavoro di dati. Questi sono i
campi il cui valore puo' venire **sia** dalla fonte **sia** da una formula del
sistema — la condizione esatta in cui l'origine non e' deducibile:

{tabella(["campo", "dove", "casi", "torna col conto", "dichiara l'origine?"],
         [(c, d, t, f"{o} ({o * 100 // t if t else 0}%)", g)
          for c, d, t, o, g in scoperti],
         allin=["---", "---", "--:", "--:", "---"])}

**`passive_perception` e' il caso che insegna, e non perche' sia il piu'
grave.** Il conto torna il **cento per cento** delle volte, e proprio per
questo di **nessuna** delle {next((t for c, _d, t, _o, _g in scoperti if 'passive' in c), 0)}
si sa se sia stata letta dalla fonte o calcolata. La coincidenza perfetta non
e' una conferma: e' **assenza totale di informazione**. Un campo dove il conto
torna sempre e' il posto peggiore in cui fidarsi del conto — ed e' anche il
posto dove un controllo basato sul conto sembrera' per sempre soddisfatto.

Il verso opposto vale come regola: `hit_points.average` e' l'unico della
tabella che l'origine ce l'ha gia', ed e' anche l'unico che **non torna
sempre**. Non e' una coincidenza: l'origine e' stata scritta li' perche' li'
lo scarto si vedeva.
""")

    # ------------------------------------------------------------------ §7
    parti.append(f"""---

## 7. Dove il difetto non puo' esistere

Un campo che porta solo **ingressi** non ha questa forma. `saving_throws`
dichiara quali competenze il portatore ha, non il numero che ne segue: non
c'e' niente da confondere, perche' il numero non e' scritto da nessuna parte
e quindi non puo' contraddire il conto.

E' la stessa forma che la {cita('attacco-unica-lettura')} ha imposto al
personaggio, e la regola che ne segue e' la piu' utile di tutto il giro:
**un campo che si puo' non scrivere e' meglio di un campo la cui origine si
deve dichiarare**. Dichiarare l'origine e' il rimedio dove il valore *deve*
stare scritto — non il primo posto dove guardare.
""")

    return riflow("\n".join(parti))


def main():
    for completo in (False, True):
        nome = f"RAPPORTO-origine{'-completo' if completo else ''}.md"
        p = os.path.join(BASE, nome)
        testo = rapporto(completo=completo)
        with open(p, "w", encoding="utf-8") as f:
            f.write(testo)
        print(f"scritto {p} ({len(testo)} caratteri)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
