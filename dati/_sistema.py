#!/usr/bin/env python3
"""
I dati di sistema, letti dalla loro sede unica.

PERCHE' QUESTO FILE NON CONTIENE LE TABELLE
    Stanno in `dati/sistema/*.json` e QUI SI LEGGONO, non si ridigitano. E'
    la stessa scelta di `dati/_vocabolari.py`, per la stessa ragione:
    ridigitare darebbe due copie da tenere allineate a mano, cioe' il
    difetto che la sede unica esiste per chiudere.

COSA CHIUDE
    La NONA struttura doppia del progetto, misurata in
    `dati/RAPPORTO-meccanica.md`: il modificatore di caratteristica scritto
    in `dati/valida_effetti.py` e in `motore/combattimento.py`, il bonus di
    competenza in `dati/_srd51.py` e in `dati/valida_effetti.py`. Formule
    identiche, in file che nessuna esecuzione metteva uno contro l'altro.

    Le otto precedenti erano fra file di DATI, dove arrivano schemi e
    validatori. Questa e' la prima che vive nel CODICE, dove non arrivava
    niente — ed e' la ragione per cui la sede da sola non basta e serve il
    controllo di `copie_nel_codice()` qui sotto. Senza quel controllo «le
    tabelle stanno in dati/sistema/» e' una descrizione, non una regola: e'
    lo stesso argomento con cui `valida_effetti.py` ha reso accettabile il
    campo `effetto`.

COSA ESPONE
    modificatore(punteggio)            la tabella dei modificatori
    competenza(livello)                il bonus di competenza per livello
    competenza_da_grado_sfida(gs)      la stessa tabella, letta per GS
    cd_salvezza(competenza, mod)       8 + competenza + modificatore
    MOLTIPLICATORI / ORDINE_DIFESE     resistenza, vulnerabilita', immunita'
    CRITICO_NATURALE / FALLIMENTO_NATURALE
    ARRAY_STANDARD / COSTO_ACQUISTO / BUDGET_ACQUISTO / TIRO_CARATTERISTICA
                                       i tre metodi di generazione
    copie_nel_codice()                 il controllo anti-duplicazione

    Il valore di ritorno viene SEMPRE dalla tabella: nessuna funzione qui
    dentro ricalcola la formula. Se un giorno la 5e cambiasse una fascia,
    cambierebbe il JSON e nient'altro.
"""

import glob
import io
import json
import os
import re
import tokenize

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
CARTELLA = os.path.join(BASE, "sistema")


def _carica():
    fuori = {}
    for f in sorted(glob.glob(os.path.join(CARTELLA, "*.json"))):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        fuori[d["id"]] = d
    return fuori


DATI = _carica()


# --------------------------------------------------------------- le letture

def _lettura(dato_id, lettura_id):
    for l in DATI[dato_id]["letture"]:
        if l["id"] == lettura_id:
            return l
    raise KeyError(f"{dato_id}: nessuna lettura '{lettura_id}'")


def _in_fascia(dato_id, valore):
    for f in DATI[dato_id]["fasce"]:
        if f["da"] <= valore <= f["a"]:
            return f["valore"]
    return None


def _leggi(dato_id, lettura_id, ingresso):
    """Il valore della tabella, con il dominio della lettura fatto valere.

    Un ingresso fuori dominio SOLLEVA invece di tornare un valore di
    ripiego: un livello 0 o un punteggio 40 sono un errore di chi chiama, e
    un motore che li accettasse in silenzio produrrebbe numeri plausibili e
    sbagliati — la forma di difetto che l'arena esiste per non ripetere."""
    l = _lettura(dato_id, lettura_id)
    basso, alto = l["dominio"]
    if not (basso <= ingresso <= alto):
        raise ValueError(
            f"{dato_id}/{lettura_id}: {l['ingresso']} {ingresso} fuori dal "
            f"dominio dichiarato [{basso}, {alto}]")
    sotto = l.get("sotto_il_minimo")
    if sotto and ingresso < sotto["soglia"]:
        return sotto["valore"]
    v = _in_fascia(dato_id, ingresso)
    if v is None:
        raise ValueError(
            f"{dato_id}: nessuna fascia contiene {ingresso}. Il dominio "
            f"della lettura '{lettura_id}' e' piu' largo delle fasce")
    return v


def modificatore(punteggio):
    """Il modificatore di un punteggio di caratteristica."""
    return _leggi("modificatore-caratteristica", "per_punteggio", punteggio)


def competenza(livello):
    """Il bonus di competenza di un personaggio di quel livello."""
    return _leggi("bonus-competenza", "per_livello", livello)


def _grado_sfida_intero(gs):
    """Il grado sfida come intero. «1/2», 0.5 e 0 stanno sotto la prima
    fascia: la lettura per grado sfida lo dichiara in `sotto_il_minimo`."""
    if isinstance(gs, str):
        gs = gs.strip()
        if "/" in gs:
            a, b = gs.split("/", 1)
            gs = float(a) / float(b)
        else:
            gs = float(gs)
    return int(gs)


def competenza_da_grado_sfida(gs):
    """Il bonus di competenza di un mostro di quel grado sfida.

    Non e' una seconda tabella: e' la seconda LETTURA della stessa, e la
    differenza (i gradi frazionari) e' un campo del dato, non un ramo
    scritto qui."""
    try:
        n = _grado_sfida_intero(gs)
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    return _leggi("bonus-competenza", "per_grado_sfida", n)


def cd_salvezza(bonus_competenza, modificatore_caratteristica):
    """La CD di un tiro salvezza: la base della formula piu' gli addendi.

    La base non e' scritta qui — e' `base` in cd-tiro-salvezza.json — e gli
    addendi arrivano gia' calcolati da chi chiama, perche' sono gli stessi
    due dati di sistema che la formula RIFERISCE per id."""
    return DATI["cd-tiro-salvezza"]["base"] + bonus_competenza \
        + modificatore_caratteristica


# ------------------------------------------------- moltiplicatori e soglie

MOLTIPLICATORI = {m["difesa"]: m for m in DATI["moltiplicatori-difesa"]["moltiplicatori"]}
ORDINE_DIFESE = tuple(DATI["moltiplicatori-difesa"]["ordine_di_applicazione"])


def applica_moltiplicatore(danno, difesa):
    """Il danno dopo una difesa, con l'arrotondamento che il dato dichiara."""
    m = MOLTIPLICATORI[difesa]
    n = danno * m["moltiplicatore"]
    return int(n) if m["arrotondamento"] == "per_difetto" else int(round(n))


_SOGLIE = {s["id"]: s["valore"] for s in DATI["soglie-d20"]["soglie"]}
CRITICO_NATURALE = _SOGLIE["critico_naturale"]
FALLIMENTO_NATURALE = _SOGLIE["fallimento_naturale"]


# ------------------------------------------- i metodi di generazione (PHB 2014)
#
# PRIMO DATO DI QUESTA CARTELLA CHE NON VIENE DALL'SRD: la generazione delle
# caratteristiche il documento SRD 5.1 non la contiene affatto. Il perche'
# resti pubblicabile sta nella `note` del JSON e nel .gitignore, dichiarato
# li' e non qui.
#
# Il DEFAULT non e' fra questi: e' la
# decisione 8 (`generazione-caratteristiche`) e sta con il motore. Qui c'e' cosa i
# metodi sono, non quale si usa.

def _metodo(metodo_id):
    for m in DATI["generazione-caratteristiche"]["metodi"]:
        if m["id"] == metodo_id:
            return m
    raise KeyError(f"nessun metodo di generazione '{metodo_id}'")


ARRAY_STANDARD = tuple(_metodo("array-standard")["valori"])
COSTO_ACQUISTO = {c["punteggio"]: c["costo"]
                  for c in _metodo("punti-acquisto")["costi"]}
BUDGET_ACQUISTO = _metodo("punti-acquisto")["budget"]
TIRO_CARATTERISTICA = _metodo("tiro-4d6-scarta-minore")
PUNTEGGI = _metodo("array-standard")["punteggi"]


# ------------------------------------------------ controllo anti-duplicazione

# I sorgenti in cui una copia puo' nascere. Non e' tutto il repository: e'
# il codice Python del progetto, che e' l'unico posto dove il controllo puo'
# davvero guardare. Cosa resta fuori sta scritto in `LIMITI` piu' sotto, e
# va letto: un controllo di cui non si conosce il bordo viene creduto piu'
# di quanto valga.
SORGENTI = ("dati/*.py", "motore/*.py", "*.py")

# --------------------------------------------------------------------------
# A. PER FORMA. Una formula ricopiata cambia nome, non forma: quindi si
#    cerca l'espressione e non l'identificatore. Ogni riga qui sotto ha
#    trovato almeno un caso vero il 02/09/2026.
# --------------------------------------------------------------------------
#
#    I token arrivano separati da spazi (`int ( n )` e non `int(n)`),
#    perche' il codice viene ricomposto dal tokenizzatore e non letto riga
#    per riga: T qui sotto e' «un termine qualunque», spazi compresi, e
#    tenerlo corto e pigro evita che un'espressione regolare si allarghi a
#    meta' file. La prima versione di queste righe non aveva gli spazi e
#    per questo mancava `max(2, 2 + (int(n) - 1) // 4)` — che era una delle
#    due copie da trovare. Ora e' fra le COPIE_FINTE, cosi' non puo'
#    tornare a sfuggire in silenzio.
_T = r"[\w\.\[\]'\"()\s]{1,40}?"
FORME = {
    "modificatore-caratteristica": [
        r"\(\s*" + _T + r"\s*-\s*10\s*\)\s*//\s*2",
        r"\(\s*" + _T + r"\s*-\s*10\s*\)\s*/\s*2",
        r"[\w\.\[\]'\"]+\s*//\s*2\s*-\s*5\b",
    ],
    "bonus-competenza": [
        r"2\s*\+\s*\(\s*" + _T + r"\s*-\s*1\s*\)\s*//\s*4",
        r"\(\s*" + _T + r"\s*-\s*1\s*\)\s*//\s*4\s*\+\s*2",
    ],
    "cd-tiro-salvezza": [
        r"\b8\s*\+\s*[\w\.\[\]'\"()\s]{0,20}?(?:pb|comp|prof)",
    ],
}

# --------------------------------------------------------------------------
# B. PER VALORI. Una tabella si copia anche SENZA la formula, scrivendone
#    i valori uno per uno: `{1: 2, 2: 2, 3: 2, ...}`. La forma non c'e'
#    piu', i valori si'. Si cerca il piu' lungo tratto di interi letterali
#    del file che coincida con un tratto della tabella espansa.
#
#    DUE SOGLIE, non una, e la seconda e' quella che conta. La lunghezza da
#    sola non basta: il bonus di competenza e' fatto di corse lunghe dello
#    stesso numero (2, 2, 2, 2, 3, 3, 3, 3...), e in `dati/_sfere_5e.py` la
#    colonna dei livelli d'incantesimo produce per caso otto valori
#    identici a un tratto della tabella. Non e' una copia: e' un'altra
#    tabella che comincia allo stesso modo. Serve quindi anche un minimo di
#    valori DISTINTI dentro la corsa — un tratto vero della tabella cambia
#    valore almeno due volte, una coincidenza di solito no.
# --------------------------------------------------------------------------
CORSA_MINIMA = 10
DISTINTI_MINIMI = 3

# LE SFILZE CORTE, e sono l'altra meta' del controllo. Una tabella di trenta
# righe si riconosce da un tratto di dieci valori; l'array standard ne ha 6 e
# il listino dell'acquisto a punti 8, quindi con la sola CORSA_MINIMA i due
# dati aggiunti il 05/09/2026 sarebbero entrati nella sede senza che nessuno
# potesse vederne una copia — cioe' la sede sarebbe stata una descrizione, che
# e' esattamente cio' che questo file esiste per evitare.
#
# La regola per loro e' piu' stretta, non piu' larga: si segnala solo la
# sfilza ripetuta PER INTERO. Sei valori di seguito uguali a `15, 14, 13, 12,
# 10, 8` non sono una coincidenza; i primi tre di quella stessa sfilza si',
# e con una soglia proporzionale lo sarebbero stati.
LUNGHEZZA_CORTA = CORSA_MINIMA

# --------------------------------------------------------------------------
# LE ECCEZIONI, DICHIARATE. Un'occorrenza e' permessa solo se sta in questa
# tabella, e ogni voce deve trovarsi davvero: un'eccezione dichiarata e non
# trovata e' un'eccezione marcita, e il controllo la segnala come segnala
# una copia. E' la stessa invariante a due sensi degli `assert` di
# `_vocabolari.py`.
#
# (percorso, marcatore sulla riga) -> perche'
# --------------------------------------------------------------------------
ECCEZIONI = {
    ("dati/valida_sistema.py", "SONDA"):
        "la sonda che ricalcola la tabella con la formula stampata dalla "
        "fonte e la confronta fascia per fascia. E' l'unica occorrenza "
        "permessa, ed e' un RICONFRONTO, non una copia: senza di essa una "
        "tabella di trenta righe battuta a mano non ha nessuno che la "
        "verifichi. Stessa forma della sonda 'slashing' di _schemi.py.",
}


def _sorgenti():
    fuori = []
    for schema in SORGENTI:
        for f in glob.glob(os.path.join(RADICE, schema)):
            fuori.append(f)
    return sorted(set(fuori))


def _espandi(dato_id, lettura_id):
    l = _lettura(dato_id, lettura_id)
    basso, alto = l["dominio"]
    return [_leggi(dato_id, lettura_id, i) for i in range(basso, alto + 1)]


# I token che NON sono codice: stringhe, commenti, e i pezzi letterali di
# una f-string. Il controllo guarda il codice e non la prosa, e la ragione
# non e' un dettaglio di implementazione: `dati/analizza_meccanica.py` e
# `dati/valida_effetti.py` DESCRIVONO la formula della CD dentro un
# docstring, ed e' il loro mestiere. Segnalarle sarebbe il controllo che
# grida al lupo — cioe' il controllo che qualcuno spegne.
_NON_CODICE = {"STRING", "COMMENT", "FSTRING_START", "FSTRING_MIDDLE",
               "FSTRING_END", "NL", "NEWLINE", "INDENT", "DEDENT",
               "ENDMARKER", "ENCODING"}


def _token_di_codice(testo):
    """[(riga, tipo, stringa)] dei soli token di codice."""
    fuori = []
    try:
        for t in tokenize.generate_tokens(io.StringIO(testo).readline):
            if tokenize.tok_name.get(t.type) in _NON_CODICE:
                continue
            fuori.append((t.start[0], tokenize.tok_name.get(t.type), t.string))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        # Un sorgente che non si tokenizza non si nasconde: si dichiara.
        return None
    return fuori


def _piatto(token):
    """Il codice come testo continuo, piu' la mappa offset -> riga."""
    pezzi, mappa, pos = [], [], 0
    for riga, _tipo, s in token:
        pezzi.append(s)
        mappa.append((pos, riga))
        pos += len(s) + 1
    return " ".join(pezzi), mappa


def _riga_di(mappa, offset):
    riga = mappa[0][1] if mappa else 0
    for pos, r in mappa:
        if pos > offset:
            break
        riga = r
    return riga


def _gruppi_di_interi(token):
    """Le SFILZE di interi letterali: numeri separati solo da punteggiatura.

    Il gruppo si spezza appena fra due numeri compare un nome o una
    stringa, e questa e' la parte che rende il controllo utilizzabile.
    Una tabella copiata a mano e' una sfilza — `{1: 2, 2: 2, 3: 2, ...}`,
    `[2, 2, 2, 2, 3, ...]` — cioe' numeri e punteggiatura. Una colonna di
    numeri dentro altro NON lo e': in `dati/_sfere_5e.py` i livelli
    d'incantesimo formano per caso dieci valori identici a un tratto del
    bonus di competenza, ma fra un numero e l'altro ci sono il nome
    dell'incantesimo e la sua scuola. Senza questa regola il controllo
    segnalerebbe quel file, e un controllo che segnala il file sbagliato
    viene spento — e' successo abbastanza spesso da essere una regola di
    progetto.

    Di ogni gruppo si guardano anche i posti PARI e i posti DISPARI presi
    da soli: `{1: 2, 2: 2, 3: 2}` mette le chiavi in mezzo ai valori, e la
    tabella dei valori vive li' dentro a passo due."""
    gruppi, corrente = [], []
    for i, (_riga, tipo, s) in enumerate(token):
        if tipo == "NUMBER" and s.isdigit():
            n = int(s)
            if i and token[i - 1][2] == "-":
                prima = token[i - 2][2] if i >= 2 else "("
                if prima in "([{,=:+-*/%<>" or prima in ("return", "and", "or"):
                    n = -n
            corrente.append(n)
        elif tipo == "OP" and s in ",:[]{}()-+":
            continue
        else:
            if len(corrente) >= 2:
                gruppi.append(corrente)
            corrente = []
    if len(corrente) >= 2:
        gruppi.append(corrente)

    fuori = []
    for g in gruppi:
        fuori.extend([g, g[0::2], g[1::2]])
    return fuori


def _sequenze():
    """Le sfilze di interi che un sorgente potrebbe aver ricopiato.

    Torna [(dato_id, etichetta, valori)]. Due sorgenti, non uno: le LETTURE
    di una tabella espansa sul loro dominio (trenta valori, la forma
    riconosciuta dal 02/09/2026) e i METODI di generazione, che sono sfilze
    corte e gia' scritte per esteso nel dato.

    Dei costi dell'acquisto a punti si dichiara il solo listino dei COSTI e
    non la colonna dei punteggi: `8, 9, 10, 11, 12, 13, 14, 15` e' una
    progressione qualunque e segnalarla vorrebbe dire gridare al lupo su
    ogni `range` scritto per esteso. Il gruppo interleaved di un dizionario
    `{8: 0, 9: 1, ...}` resta comunque coperto, perche' `_gruppi_di_interi`
    ne offre anche i posti dispari, cioe' i costi."""
    fuori = []
    for dato_id, d in DATI.items():
        for l in d.get("letture") or []:
            fuori.append((dato_id, l["id"], _espandi(dato_id, l["id"])))
        for m in d.get("metodi") or []:
            if m.get("valori"):
                fuori.append((dato_id, m["id"], list(m["valori"])))
            if m.get("costi"):
                fuori.append((dato_id, m["id"] + "/costi",
                              [c["costo"] for c in m["costi"]]))
    return fuori


def _corsa_comune(interi, tabella):
    """Il piu' lungo tratto contiguo comune, e quanti valori distinti ha."""
    migliore, distinti = 0, 0
    for i in range(len(interi)):
        for j in range(len(tabella)):
            n = 0
            while (i + n < len(interi) and j + n < len(tabella)
                   and interi[i + n] == tabella[j + n]):
                n += 1
            if n > migliore:
                migliore, distinti = n, len(set(tabella[j:j + n]))
    return migliore, distinti


def copie_in(percorso, testo):
    """Le copie dentro UN sorgente. Torna (copie, eccezioni_usate).

    Prende il testo invece del percorso perche' cosi' il controllo si puo'
    PROVARE su un sorgente finto: `valida_sistema.py` gli pianta davanti
    una copia costruita apposta e pretende che la veda. Un controllo che
    nessuno mette alla prova e' un controllo di cui si sa solo che non
    grida — che non e' la stessa cosa che funzionare."""
    copie, viste = [], set()
    token = _token_di_codice(testo)
    if token is None:
        return [("(tutti)", percorso, 0, "illeggibile",
                 "il sorgente non si tokenizza: il controllo non ha potuto "
                 "guardarci dentro")], viste
    codice, mappa = _piatto(token)
    righe = testo.split("\n")

    # A. per forma
    for dato_id, patterns in FORME.items():
        for p in patterns:
            for m in re.finditer(p, codice):
                n = _riga_di(mappa, m.start())
                riga = righe[n - 1] if 0 < n <= len(righe) else ""
                permessa = [(pf, marcatore) for (pf, marcatore) in ECCEZIONI
                            if pf == percorso and marcatore in riga]
                if permessa:
                    viste.update(permessa)
                    continue
                copie.append((dato_id, percorso, n, "forma", riga.strip()))

    # B. per valori
    gruppi = _gruppi_di_interi(token)
    for dato_id, etichetta, tabella in _sequenze():
        # Una sfilza piu' corta della soglia si segnala solo INTERA: vedi
        # LUNGHEZZA_CORTA. Le altre si segnalano su un tratto.
        richiesta = (len(tabella) if len(tabella) < LUNGHEZZA_CORTA
                     else CORSA_MINIMA)
        lunga = distinti = 0
        for g in gruppi:
            n, quanti = _corsa_comune(g, tabella)
            if n > lunga:
                lunga, distinti = n, quanti
        if lunga >= richiesta and distinti >= DISTINTI_MINIMI:
            copie.append((dato_id, percorso, 0, "valori",
                          f"{lunga} valori consecutivi ({distinti} "
                          f"distinti) di '{etichetta}'"))
    return copie, viste


def copie_nel_codice():
    """Le tabelle di sistema riscritte fuori dalla loro sede.

    Torna (copie, eccezioni_marcite). Ogni copia e'
    (dato_id, percorso, numero_di_riga, come_e'_stata_vista, testo)."""
    copie, viste = [], set()
    for f in _sorgenti():
        percorso = os.path.relpath(f, RADICE)
        if percorso == "dati/_sistema.py":
            continue
        with open(f, encoding="utf-8") as fh:
            testo = fh.read()
        trovate, usate = copie_in(percorso, testo)
        copie.extend(trovate)
        viste.update(usate)
    marcite = [f"{p}: '{m}' non compare piu'" for (p, m) in ECCEZIONI
               if (p, m) not in viste]
    return copie, marcite


# Le copie finte con cui il controllo viene messo alla prova a ogni giro.
# Una per famiglia: la formula riscritta con un altro nome, la tabella
# espansa a mano, la tabella espansa come dizionario (chiavi in mezzo ai
# valori). Se una di queste smette di essere vista, il controllo si e'
# rotto senza dirlo — che e' il modo in cui i controlli muoiono.
COPIE_FINTE = [
    ("formula ricopiata sotto un altro nome",
     "def bonus_di_tiro(p):\n    return (p - 10) // 2\n"),
    ("formula del bonus di competenza ricopiata",
     "def grado(x):\n    return 2 + (x - 1) // 4\n"),
    ("formula del bonus di competenza con un ripiego attorno",
     "def da_cr(n):\n    return 2 if n < 1 else max(2, 2 + (int(n) - 1) // 4)\n"),
    ("tabella espansa come lista",
     "PB = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6]\n"),
    ("tabella espansa come dizionario, chiavi in mezzo ai valori",
     "PB = {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4, 10: 4,\n"
     "      11: 4, 12: 4, 13: 5, 14: 5, 15: 5, 16: 5}\n"),
    ("array standard ricopiato",
     "ARRAY_STD = (15, 14, 13, 12, 10, 8)\n"),
    ("listino dell'acquisto a punti ricopiato come dizionario",
     "COSTO = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}\n"),
]

# I sorgenti finti che NON devono essere segnalati. Servono a misurare
# l'altro errore, quello che spegne un controllo: `dati/_sfere_5e.py` ha
# una colonna di livelli d'incantesimo che per caso comincia come il bonus
# di competenza, e prima della regola dei gruppi veniva segnalata.
NON_COPIE_FINTE = [
    ("una colonna di numeri dentro altro, non una tabella",
     'S = [s("Aid", 2, "Abjuration"), s("Bless", 2, "Enchantment"),\n'
     '     s("Silence", 2, "Illusion"), s("Warding Bond", 2, "Abjuration"),\n'
     '     s("Zone of Truth", 2, "Enchantment"), s("Fear", 3, "Illusion"),\n'
     '     s("Fly", 3, "Transmutation"), s("Haste", 3, "Transmutation"),\n'
     '     s("Revivify", 3, "Necromancy"), s("Banishment", 4, "Abjuration")]\n'),
    ("la formula descritta in prosa, che e' il mestiere dei rapporti",
     'NOTA = "la CD di un tiro salvezza e\' 8 + competenza + modificatore"\n'
     '# il modificatore e\' (punteggio - 10) // 2, e qui e\' un commento\n'),
    ("una sfilza corta che comincia come l'array standard e non lo e'",
     "SOGLIE = (15, 14, 13, 12, 10, 9, 7)\n"),
    ("i primi valori dell'array standard dentro un'altra sfilza",
     "TAGLIE = [15, 14, 13]\n"),
]


# --------------------------------------------------------------------------
# COSA QUESTO CONTROLLO NON PUO' VEDERE. Scritto qui e non solo nel rapporto
# perche' chi aggiunge una formula legge questo file, non il rapporto.
# --------------------------------------------------------------------------
LIMITI = [
    "una riscrittura algebrica: `punteggio // 2 - 5` e' coperto perche' e' "
    "elencato, ma `(p + (-10)) >> 1` o un `round()` con un mezzo punto no. "
    "L'equivalenza fra due espressioni non si decide con un'espressione "
    "regolare, e fingere il contrario darebbe un controllo che rassicura.",
    "un'altra lingua: il giorno in cui il motore avra' un lato web, la "
    "stessa formula in JavaScript passera' inosservata. I sorgenti scanditi "
    "sono quelli di SORGENTI, cioe' Python. "
    "E' L'UNICO LIMITE DI QUESTO ELENCO CHE RIGUARDA LA FASE 2, ed e' il primo "
    "vincolo del progetto a guardare avanti invece che indietro: gli altri "
    "dicono cosa questo controllo non vede oggi, questo dice quando "
    "smettera' di vedere abbastanza. LA CONDIZIONE, scritta perche' non "
    "venga riletta troppo tardi: quando si scrivera' il primo codice fuori "
    "da Python, questa riga va riletta PRIMA di scriverlo e non dopo. "
    "Riletta dopo non e' una rilettura: e' una struttura doppia gia' nata, "
    "e per giunta la decima, in una lingua dove nessuno dei controlli "
    "esistenti arriva. Non si risolve ora — non c'e' ancora una riga di "
    "JavaScript da scandire, e un rilevatore scritto contro codice che non "
    "esiste e' un rilevatore mai messo alla prova, che e' il difetto che "
    "COPIE_PIANTATE esiste per evitare.",
    "la prosa: una formula scritta a parole dentro un `description` di "
    "schema, dentro una nota di un JSON o dentro un documento non e' un "
    "letterale e non viene letta.",
    "un derivato precalcolato nei DATI: un mostro che si porti gia' sommato "
    "il proprio bonus di attacco non ripete nessuna formula, e questo "
    "controllo non se ne accorge — e' esattamente la lacuna che "
    "`attacco_di()` misura dall'altro lato. Chiusa in parte il 03/09/2026 "
    "dalla decisione 54 (`origine-e-un-dato`): il valore precalcolato resta "
    "invisibile a QUESTO controllo, ma adesso deve dichiarare se e' letto o "
    "calcolato, e quella dichiarazione un altro controllo la verifica. Due "
    "controlli che guardano lo stesso difetto da due lati, nessuno dei due "
    "sufficiente da solo.",
    "un numero SOLO: il budget dell'acquisto a punti e' un intero e basta, "
    "e un intero non forma una sfilza. Un `27` riscritto altrove non viene "
    "visto da nessuno dei due lati del controllo — ne' per forma, perche' "
    "non e' un'espressione, ne' per valori, perche' `_gruppi_di_interi` "
    "raccoglie da due numeri in su. E' il limite piu' facile da incontrare "
    "di questo elenco, ed e' dichiarato qui perche' chi aggiunge una costante "
    "singola alla cartella sappia che la sede la ospita ma non la protegge.",
    "una tabella copiata parzialmente: sotto i "
    f"{CORSA_MINIMA} valori consecutivi la corsa non scatta, salvo per le "
    "sfilze piu' corte della soglia, che si segnalano intere. E' una soglia "
    "scelta, e le soglie scelte sbagliano da un lato: qui sbagliano "
    "lasciando passare, che e' il lato giusto per un controllo che deve "
    "restare acceso.",
]
