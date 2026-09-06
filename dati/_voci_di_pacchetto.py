#!/usr/bin/env python3
"""Le sette voci che l'SRD nomina solo dentro un pacchetto, e cosa diventano.

UNICA SEDE. `build_oggetti.py` deve sapere quali di esse diventano oggetti,
`build_pacchetti.py` deve sapere come scrivere la voce, e
`analizza_equipaggiamento.py` deve poterle contare. Tre lettori: se ognuno
tenesse il proprio elenco sarebbe la struttura doppia di sempre, nella forma
piu' innocua e piu' facile — sette nomi corti che oggi combaciano.

IL CRITERIO, che vale ben oltre queste sette
    UN OGGETTO ESISTE SE IL MOTORE DEVE SAPERNE QUALCOSA.

    La corda che lega il campanello si': lo scassinatore la tende attraverso
    un corridoio, e il motore deve sapere che c'e', quanto e' lunga, che si
    puo' tagliare. La cassetta delle elemosine no: nessuna regola la
    interroga, nessun tiro la nomina, nessuno stato di gioco cambia se c'e' o
    non c'e'. Non e' una questione di importanza narrativa — la cassetta puo'
    essere il centro di una sessione intera — ma di ARITMETICA: il motore o
    ne calcola qualcosa, o la trasporta come parola.

    La conseguenza e' che una voce non promossa a oggetto non si perde. Resta
    nel pacchetto come testo, con la sua quantita' e il suo nome: e' scritta
    sulla scheda e la si puo' leggere, semplicemente nessun conto la
    attraversa.

    Il criterio e' registrato in `decisioni.py` e in
    `dati/METODO-conversione-equipaggiamento.md`, che e' dove sta il metodo.
    Qui c'e' la sua PRIMA APPLICAZIONE, voce per voce, con la ragione
    accanto al risultato.

TRE ESITI, NON DUE
    `oggetto`      — entra in `dati/oggetti/`. Prezzo e peso restano `null`:
                     la tabella dell'SRD non li da', e inventarli sarebbe un
                     numero nostro spacciato per fonte.
    `equivalenza`  — la fonte nomina la stessa cosa altrove e con un altro
                     nome, che a listino c'e'. Non si crea niente: si
                     RISOLVE. E' il caso di «Vestments» -> «Robes».
    `testo`        — resta dentro il pacchetto come parola.

LA PROVA DEGLI INCANTESIMI, e perche' non e' il criterio ma un suo strumento
    Per l'incenso e il turibolo la domanda «il motore deve saperne qualcosa?»
    non si risponde guardando il pacchetto: si risponde guardando gli
    incantesimi, perche' un componente materiale che la fonte NOMINA e' una
    cosa di cui il motore deve tenere conto. La prova e' quindi eseguita, non
    ricordata: `nominata_da_incantesimi()` legge `dati/incantesimi/` a ogni
    import e l'esito registrato qui deve combaciare — se un domani il corpus
    cambia, l'assert parla.

    Cio' che la prova NON e': il criterio generale. Applicata a tappeto
    prenderebbe anche la sabbia — misurato da `nominate_ma_testo()`, non
    ricordato — e dietro la sabbia mezzo listino di
    ingredienti, perche' l'SRD dichiara che una borsa dei componenti copre
    ogni componente senza costo. La borsa e' gia' a catalogo ed e' cio' di
    cui il motore deve sapere; il singolo pizzico no. Per l'incenso e il
    turibolo la prova serve perche' li' la domanda era proprio se
    l'oggetto liturgico avesse una vita fuori dal pacchetto, e la risposta
    era nei dati.
"""

import glob
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "_fonti"))

import srd51_pacchetti as PK  # noqa: E402

INCANTESIMI = os.path.join(BASE, "incantesimi")

SEZIONE_SRD = "v1/sections/equipment-packs"


def _pacchetto_di(nome_voce):
    """Il pacchetto che nomina la voce. Derivato, non ricopiato."""
    for nome, _costo, voci in PK.PACCHETTI:
        if any(v == nome_voce for _q, v, _a in voci):
            return nome
    return None


def _materiali():
    """(id_incantesimo, componente materiale) per chi ne ha uno."""
    fuori = []
    for f in sorted(glob.glob(os.path.join(INCANTESIMI, "*.json"))):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        md = (d.get("components") or {}).get("material_desc")
        if md:
            fuori.append((d["id"], md))
    return fuori


def con_costo_o_consumo(termine):
    """Gli incantesimi che nominano `termine` e il cui blocco di componenti
    porta un costo o un consumo.

    Sono i casi che contano davvero, perche' l'SRD dichiara che la borsa dei
    componenti copre ogni componente SENZA costo: un ingrediente costato o
    consumato il giocatore deve procurarselo, quindi il motore deve saperlo
    contare. Il resto lo copre la borsa, che e' gia' a catalogo.

    LA PROVA E' GROSSOLANA E LO DICHIARA: guarda il blocco dei componenti,
    non il singolo ingrediente, e un blocco puo' attribuire il costo a un
    ingrediente diverso da quello cercato — in *Guards and Wards* i 10 mo
    sono della verga d'argento, non dell'incenso. Non si affina indovinando
    la sintassi di una frase inglese: si dichiara il limite e si usa il
    numero per quello che e', un ordine di grandezza a favore della
    promozione, non una prova.
    """
    costoso = re.compile(r"\bgp\b|consume", re.I)
    ids = set(nominata_da_incantesimi(termine))
    return [i for i, md in _materiali() if i in ids and costoso.search(md)]


def nominata_da_incantesimi(termine):
    """Gli incantesimi che nominano `termine` fra i componenti MATERIALI.

    Solo li': la descrizione di un incantesimo nomina di tutto — «a string
    of insults» in *Vicious Mockery* non e' spago — e cercare nella prosa
    darebbe una risposta che sembra misurata e non lo e'.
    """
    rx = re.compile(r"\b" + re.escape(termine) + r"\w*\b", re.I)
    return [i for i, md in _materiali() if rx.search(md)]


# --------------------------------------------------------------------------
# LE SETTE, con la ragione accanto al risultato. `termine` e' la parola su
# cui la prova degli incantesimi si esegue: sta qui anche per le voci in cui
# non decide, perche' una prova che si puo' rifare su tutte e sette e' una
# misura, e una che si esegue solo dove conviene e' un'illustrazione.
# --------------------------------------------------------------------------
VOCI = {
    "String (10 feet)": {
        "esito": "oggetto",
        "termine": "string",
        "name_it": "Spago (3 metri)",
        "ragione":
            "E' l'esempio stesso del criterio: la corda che lega il "
            "campanello. Lo scassinatore la tende, la lega, la taglia — sono "
            "tre cose che il motore deve poter sapere, e nessuna di esse e' "
            "narrazione. La decide il criterio, non la prova degli "
            "incantesimi, che pure la conferma ({n} incantesimi la nominano "
            "come componente).",
    },
    "Block of incense": {
        "esito": "oggetto",
        "termine": "incense",
        "name_it": "Blocco d'incenso",
        "ragione":
            "La prova degli incantesimi: {n} incantesimi dell'SRD nominano "
            "l'incenso fra i componenti materiali, e in {k} di essi il blocco "
            "dei componenti porta un costo o un consumo — cioe' proprio i "
            "casi che la borsa dei componenti NON copre e che il motore deve "
            "contare. Ha una vita fuori dal pacchetto.",
    },
    "Censer": {
        "esito": "testo",
        "termine": "censer",
        "name_it": None,
        "ragione":
            "La stessa prova, esito opposto: nessun incantesimo dell'SRD "
            "nomina il turibolo. E' il contenitore in cui l'incenso brucia, "
            "e il motore non ne calcola niente. Resta testo del pacchetto, "
            "dove si legge benissimo.",
    },
    "Vestments": {
        "esito": "equivalenza",
        "termine": "vestment",
        "name_it": None,
        "ragione":
            "Non e' una voce da creare: la tabella dell'attrezzatura ha gia' "
            "«Robes», con prezzo e peso propri, e le due parole nominano la "
            "stessa cosa. L'equivalenza sta in `srd51_pacchetti.EQUIVALENZE` "
            "accanto alle altre letture della stessa forma. E' l'unica delle "
            "sette a cui ha risposto la fonte invece che noi.",
    },
    "Alms box": {
        "esito": "testo",
        "termine": "alms",
        "name_it": None,
        "ragione":
            "L'altro esempio del criterio, quello negativo: nessuna regola "
            "la interroga, nessun tiro la nomina, nessuno stato cambia se "
            "c'e'. Puo' essere il centro di una sessione e restare comunque "
            "una parola per il motore.",
    },
    "Little bag of sand": {
        "esito": "testo",
        "termine": "sand",
        "name_it": None,
        "ragione":
            "Nel Pacchetto dello studioso la sabbia asciuga l'inchiostro: "
            "nessun conto la attraversa. LA PROVA DEGLI INCANTESIMI LA "
            "PRENDEREBBE — {n} incantesimi la nominano — ed e' la ragione per "
            "cui quella prova e' uno strumento del criterio e non il "
            "criterio: di quei {n} ne portano un costo o un consumo {k}, "
            "quindi la borsa dei componenti li copre tutti, e cio' di cui il "
            "motore deve sapere e' la borsa. E' anche la differenza esatta "
            "con l'incenso, che un costo ce l'ha. La tensione e' misurata da "
            "`nominate_ma_testo()` invece che taciuta.",
    },
    "Small knife": {
        "esito": "testo",
        "termine": "knife",
        "name_it": None,
        "ragione":
            "Il coltellino dello studioso taglia le penne e apre i sigilli. "
            "Non e' un'arma — l'SRD non gli da' ne' dado di danno ne' "
            "proprieta' — e promuoverlo a oggetto vorrebbe dire inventargli "
            "una scheda d'arma che la fonte non scrive. Nessun incantesimo "
            "lo nomina.",
    },
}


def esito_di(nome_srd):
    return VOCI[nome_srd]["esito"]


def ragione_di(nome_srd):
    """La ragione, col conteggio degli incantesimi interpolato.

    Il `{n}` nelle ragioni non e' un vezzo: un numero battuto a mano dentro
    una motivazione si sfasa il giorno in cui il corpus cambia, e resta li' a
    giustificare una decisione con una misura che non e' piu' vera
    (CLAUDE.md 3). Qui il numero si rifa' a ogni lettura.
    """
    v = VOCI[nome_srd]
    return v["ragione"].format(
        n=len(nominata_da_incantesimi(v["termine"])),
        k=len(con_costo_o_consumo(v["termine"])))


def oggetti():
    """Le voci che diventano oggetti, pronte per `build_oggetti.py`."""
    return [
        (nome, v["name_it"], _pacchetto_di(nome))
        for nome, v in VOCI.items() if v["esito"] == "oggetto"
    ]


def nominate_ma_testo():
    """Voci lasciate a testo che un incantesimo nomina lo stesso.

    Non e' un errore da correggere: e' lo scarto fra il criterio e uno dei
    suoi strumenti, e questo progetto misura gli scarti invece di
    ricordarseli.
    """
    return {nome: nominata_da_incantesimi(v["termine"])
            for nome, v in VOCI.items()
            if v["esito"] == "testo" and nominata_da_incantesimi(v["termine"])}


# --------------------------------------------------------------------------
# LE INVARIANTI, all'import.
# --------------------------------------------------------------------------

_SENZA_LISTINO = {v for _n, _c, voci in PK.PACCHETTI
                  for _q, v, a_listino in voci if not a_listino}
_SCARTO = _SENZA_LISTINO ^ set(VOCI)
assert not _SCARTO, (
    f"le voci senza listino dei pacchetti e quelle decise qui non "
    f"coincidono: {sorted(_SCARTO)}. Una voce senza listino e senza esito e' "
    f"una domanda che nessuno pone; un esito senza voce e' una decisione su "
    f"niente.")

# La prova degli incantesimi decide DUE voci, e su quelle deve tornare. Le
# altre cinque non sono decise da lei e non le si chiede di tornare: sarebbe
# un controllo che pretende una coincidenza, cioe' il modo piu' rapido per
# farlo spegnere.
for _nome in ("Block of incense", "Censer"):
    _n = len(nominata_da_incantesimi(VOCI[_nome]["termine"]))
    _atteso = VOCI[_nome]["esito"] == "oggetto"
    assert (_n > 0) == _atteso, (
        f"{_nome}: la prova degli incantesimi dice {_n} e l'esito registrato "
        f"dice {VOCI[_nome]['esito']}. Il corpus e' cambiato sotto una "
        f"decisione che poggiava su di esso.")

# Cio' che separa l'incenso dalla sabbia non e' che un incantesimo li nomini
# — li nominano entrambi — ma che uno dei due porti un costo. Se un domani la
# sabbia ne prendesse uno, questa decisione andrebbe rifatta invece che
# ereditata.
assert not con_costo_o_consumo("sand"), (
    "la sabbia ha preso un componente con costo: la ragione per cui resta "
    "testo del pacchetto non regge piu', e va rifatta invece che ereditata")

for _nome, _v in VOCI.items():
    if _v["esito"] == "oggetto":
        assert _v["name_it"], f"{_nome}: un oggetto vuole un nome italiano"
        assert PK.canonico(_nome) not in PK.indice_completo(), (
            f"{_nome} e' a listino: allora non e' una voce da creare, e' una "
            f"voce da adottare in `srd51_equipaggiamento.ATTREZZATURA`")
    if _v["esito"] == "equivalenza":
        _c = PK.canonico(_nome)
        assert _c != _nome and _c in PK.indice_completo(), (
            f"{_nome}: l'esito dice equivalenza ma "
            f"`srd51_pacchetti.EQUIVALENZE` non la porta, o porta un nome "
            f"che l'indice SRD non ha")
