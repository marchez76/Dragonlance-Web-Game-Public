#!/usr/bin/env python3
"""
Dove vive la meccanica: nel codice o nei dati. La decisione, e la sua misura.

PERCHE' ESISTE
    La prima fetta verticale ha dichiarato diciassette lacune, e tre di
    quelle erano la stessa cosa vista da tre lati: il personaggio non era un
    dato, le regole di sistema non avevano sede, un innesco non aveva un
    campo. Tutte e tre dicevano che c'era meccanica che viveva nel codice
    invece che nei dati.

    Fino al 02/09/2026 questo documento MISURAVA e PROPONEVA, e lo diceva.
    Le tre proposte sono state accettate: sono la decisione 51
    (`criterio-meccanica`), la decisione 52 (`attacco-unica-lettura`) e la
    decisione 53 (`condizioni-vocabolario-srd`). Da allora il documento
    registra la decisione presa e ne misura l'effetto — cosa la sede
    contiene, cosa il controllo anti-duplicazione vede e cosa NON vede,
    quali lacune si sono chiuse e quale si e' aperta.

COSA MISURA, E COSA NO
    Misurabile: quanti blocchi portano struttura e quanti prosa, quante
    tabelle di sistema hanno una sede e quanti ingressi coprono, quante
    copie il controllo trova nel codice e quante ne riconosce fra quelle
    piantate apposta, quanti blocchi costerebbe cambiare forma oggi e
    quanti dopo.
    Non misurabile e quindi dichiarato: il criterio. Sta nella tabella
    REGOLE_NEL_CODICE, che elenca a mano cio' che vive nel codice, dove
    vive e se e' chiuso. Ogni riga nomina una funzione, e lo script
    VERIFICA che la funzione esista davvero: una tabella scritta a mano che
    nessuno riconfronta e' un'altra struttura doppia, e sarebbe la decima.

Uso:  python3 dati/analizza_meccanica.py
"""
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

import _sistema as SIS  # noqa: E402
from decisioni import cita  # noqa: E402

MOTORE = os.path.join(RADICE, "motore")

# --------------------------------------------------------------------------
# Cio' che oggi vive nel codice, dichiarato riga per riga.
#
# (etichetta, file, simbolo, che cosa e', dove vive, stato)
#
# `simbolo` deve esistere davvero nel file: e' l'unico modo perche' questa
# tabella non diventi una descrizione che invecchia da sola. `che cosa e'`
# usa il criterio della decisione 51 (`criterio-meccanica`): PROCEDURA (si
# fa), TABELLA (si legge), VARIABILE (cambia da portatore a portatore,
# quindi e' un dato di contenuto). `stato` dice se la casella e' chiusa o
# se resta una lacuna aperta, e le lacune aperte le dichiara l'arena: il
# nome fra apici deve comparire in `dati/RAPPORTO-arena.md`.
# --------------------------------------------------------------------------
REGOLE_NEL_CODICE = [
    # --- PROCEDURE: restano codice, ed e' la risposta del criterio ---------
    ("risoluzione dell'attacco: d20 + bonus contro CA, 20 critico, 1 mancato",
     "motore/combattimento.py", "def risolvi_attacco", "PROCEDURA",
     "codice; le sue tre soglie sono dati di sistema", "chiusa"),
    ("vantaggio e svantaggio: due dadi, il migliore o il peggiore",
     "motore/combattimento.py", "def d20", "PROCEDURA", "codice", "chiusa"),
    ("l'attacco: campo sul mostro, composizione sul personaggio",
     "motore/combattimento.py", "def attacco_di", "PROCEDURA",
     "codice, una lettura sola per entrambi i lati", "chiusa"),
    ("resistenza dimezza, vulnerabilita' raddoppia, immunita' annulla",
     "motore/combattimento.py", "def applica_difese", "PROCEDURA",
     "codice; moltiplicatori e ordine sono dati di sistema", "chiusa"),
    ("un'immunita' a condizione si confronta per id",
     "motore/combattimento.py", "def applica_esito", "PROCEDURA",
     "codice; i nomi vengono dal vocabolario condiviso", "chiusa"),
    ("punti ferita: massimo al 1° livello, media ai successivi",
     "motore/combattimento.py", "def pf_di", "PROCEDURA",
     "codice, con gli ingressi del Personaggio", "chiusa"),
    ("Classe Armatura: base + Destrezza (con tetto) + scudo + stile",
     "motore/combattimento.py", "def ca_di", "PROCEDURA",
     "codice, con gli ingressi del Personaggio", "chiusa"),
    ("struttura del round ed economia delle azioni",
     "motore/combattimento.py", "def turno", "PROCEDURA", "codice", "chiusa"),
    ("iniziativa: modificatore di Destrezza",
     "motore/combattimento.py", "def scontro", "PROCEDURA",
     "codice, ma nessun campo porta il bonus", "aperta — lacuna `iniziativa`"),
    ("fine dello scontro: quando una parte non puo' piu' agire",
     "motore/combattimento.py", "def scontro", "PROCEDURA",
     "codice, ma la definizione non e' dichiarata da nessun dato",
     "aperta — lacuna `fine-dello-scontro`"),
    ("a 0 punti ferita: il mostro muore, il personaggio cade incosciente",
     "motore/combattimento.py", "def applica_danno", "PROCEDURA",
     "codice; i tiri salvezza contro morte non sono modellati",
     "aperta — lacuna `tiri-salvezza-contro-morte`"),

    # --- TABELLE: sono diventate dati, e un controllo lo tiene fermo -------
    ("modificatore di caratteristica",
     "dati/_sistema.py", "def modificatore", "TABELLA",
     "`dati/sistema/modificatore-caratteristica.json`", "chiusa"),
    ("bonus di competenza per livello",
     "dati/_sistema.py", "def competenza", "TABELLA",
     "`dati/sistema/bonus-competenza.json`, lettura `per_livello`", "chiusa"),
    ("bonus di competenza dal grado sfida",
     "dati/_sistema.py", "def competenza_da_grado_sfida", "TABELLA",
     "la STESSA tabella, lettura `per_grado_sfida`", "chiusa"),
    ("CD di un tiro salvezza: 8 + competenza + modificatore",
     "dati/_sistema.py", "def cd_salvezza", "TABELLA",
     "`dati/sistema/cd-tiro-salvezza.json`, con gli addendi riferiti per id",
     "chiusa"),
    ("moltiplicatori delle difese, e il loro ordine di applicazione",
     "dati/_sistema.py", "MOLTIPLICATORI", "TABELLA",
     "`dati/sistema/moltiplicatori-difesa.json`", "chiusa"),
    ("soglie del 20 e dell'1 naturale",
     "dati/_sistema.py", "CRITICO_NATURALE", "TABELLA",
     "`dati/sistema/soglie-d20.json`", "chiusa"),

    # --- VARIABILI: sono dati di contenuto, e non hanno ancora un campo ----
    ("quali tratti scattano alla morte del portatore",
     "motore/combattimento.py", "TRATTI_ALLA_MORTE", "VARIABILE",
     "DATO — un campo `innesco` sul blocco",
     "aperta — lacuna `innesco-non-dichiarato`"),
    ("quando usare una risorsa (sotto meta' dei punti ferita)",
     "motore/combattimento.py", "def agisci", "VARIABILE",
     "DATO — IA di combattimento, la casella di "
     "decisione 27 (`sette-campi-2e`)",
     "aperta — lacuna `quando-usare-una-risorsa`"),
    ("da dove viene il bonus di attacco di un mostro",
     "motore/combattimento.py", "def attacco_di", "VARIABILE",
     "DATO — `bonus_origine` accanto a `bonus_colpire`, "
     "decisione 54 (`origine-e-un-dato`)",
     "chiusa"),
]


# --------------------------------------------------------------------- misure

def carica(cartella):
    for f in sorted(glob.glob(os.path.join(BASE, cartella, "*.json"))):
        yield os.path.basename(f), json.load(open(f, encoding="utf-8"))


CHIAVI_BLOCCO = ("actions", "traits", "reactions", "bonus_actions",
                 "legendary_actions")


def blocchi():
    """(prosa, struttura) per cartella, con lo stesso conteggio di
    analizza_personaggio.d_arena(): mostri + razze + features di classe.
    Contarli diversamente qui darebbe due numeri per la stessa cosa."""
    fuori = {}
    tot_m = eff_m = 0
    for _, d in carica("mostri"):
        for k in CHIAVI_BLOCCO:
            for b in (d["mechanics_5e"].get(k) or []):
                tot_m += 1
                eff_m += 1 if b.get("effetto") else 0
    fuori["mostri"] = (tot_m, eff_m)

    tot_r = eff_r = 0
    for _, d in carica("razze"):
        for b in (d["mechanics_5e"].get("traits") or []):
            tot_r += 1
            eff_r += 1 if b.get("effetto") else 0
    fuori["razze"] = (tot_r, eff_r)

    tot_c = eff_c = 0
    for _, d in carica("classi"):
        for b in (d["mechanics_5e"].get("features") or []):
            tot_c += 1
            eff_c += 1 if b.get("effetto") else 0
    fuori["classi (features)"] = (tot_c, eff_c)

    # I privilegi del chassis stanno a parte: sono GENERATI da _srd51.py,
    # e questo cambia il costo di rifarli. Contarli insieme agli altri
    # gonfierebbe il costo di un cambio di forma.
    tot_ch = eff_ch = 0
    for _, d in carica("classi"):
        for b in (d["mechanics_5e"].get("chassis_features") or []):
            tot_ch += 1
            eff_ch += 1 if b.get("effetto") else 0
    fuori["classi (chassis, generati)"] = (tot_ch, eff_ch)
    return fuori


def mostri_e_blocchi():
    n = m = 0
    con_effetto = set()
    for nome, d in carica("mostri"):
        n += 1
        for k in CHIAVI_BLOCCO:
            for b in (d["mechanics_5e"].get(k) or []):
                m += 1
                if b.get("effetto"):
                    con_effetto.add(nome)
    return n, m, len(con_effetto)


def verifica_tabella(lacune):
    """REGOLE_NEL_CODICE riconfrontata con il codice e con l'arena.

    Due controlli, e sono la ragione per cui una tabella scritta a mano e'
    ammessa qui: ogni `simbolo` deve esistere davvero nel file, e ogni
    `stato` che nomina una lacuna deve nominarne una che l'arena dichiara
    davvero. Senza il secondo, una lacuna chiusa resterebbe scritta come
    aperta e questo documento direbbe il falso senza che nulla lo dica."""
    mancanti = []
    testi = {}
    for _, percorso, simbolo, _, _, stato in REGOLE_NEL_CODICE:
        if percorso not in testi:
            testi[percorso] = open(os.path.join(RADICE, percorso),
                                   encoding="utf-8").read()
        if simbolo not in testi[percorso]:
            mancanti.append(f"{percorso}: '{simbolo}' non esiste piu'")
        for nome in re.findall(r"lacuna `([^`]+)`", stato):
            if lacune and nome not in lacune:
                mancanti.append(f"{percorso}: la lacuna '{nome}' non e' piu' "
                                f"dichiarata dall'arena")
    return mancanti


def sede(dove):
    """La sede in una parola, ricavata dalla destinazione dichiarata.

    Serve alla tabella di sintesi: elencare li' tutte le destinazioni per
    esteso darebbe una cella di trecento caratteri che nessuno legge, e
    riscriverle a mano darebbe due elenchi da tenere allineati."""
    if dove.startswith("codice"):
        return "codice"
    if dove.startswith("DATO"):
        return "dato di contenuto — il campo non esiste ancora"
    return "`dati/sistema/`"


def sede_di_sistema():
    """Cosa contiene `dati/sistema/`, e quanti ingressi copre.

    Contato espandendo le letture invece di leggere il numero di fasce:
    una tabella di sedici fasce che copre trenta punteggi dice due cose
    diverse, e quella che interessa e' la seconda."""
    righe = []
    ingressi = 0
    for dato_id, d in sorted(SIS.DATI.items()):
        letture = d.get("letture") or []
        n = sum(len(SIS._espandi(dato_id, l["id"])) for l in letture)
        ingressi += n
        righe.append((dato_id, d["genere"],
                      ", ".join(f"`{l['id']}`" for l in letture) or "—",
                      n or "—"))
    return righe, ingressi


def copie_di_sistema():
    """Le tabelle di sistema riscritte fuori dalla loro sede.

    NON e' un secondo rilevatore: chiama quello di `dati/_sistema.py`, che
    e' la sede unica anche del controllo. Scriverne uno qui — come questo
    file faceva fino al 02/09/2026, con due espressioni regolari proprie —
    darebbe due misure della stessa cosa che possono divergere, cioe' una
    struttura doppia dentro il documento che le misura."""
    copie, marcite = SIS.copie_nel_codice()
    provate = 0
    for _etichetta, finto in SIS.COPIE_FINTE:
        provate += 1 if SIS.copie_in("finto.py", finto)[0] else 0
    return copie, marcite, provate, len(SIS.COPIE_FINTE)


# Gli `\s+` al posto degli spazi non sono pigrizia: il rapporto dell'arena
# e' prosa a capo fisso con dentro numeri interpolati, quindi la stessa
# frase cambia punto di a capo appena una cifra cresce. Tollerare il ritorno
# a capo evita un allarme che non riguarda il dato; NON tollerare il testo
# diverso resta il punto, e la frase deve restare quella.
COINCIDENZE = re.compile(
    r"dei\s+\*\*(\d+) bonus di\s+attacco\*\*.*?"
    r"\*\*(\d+) tornano col conto\*\*\s+e\s+(\d+) no", re.S)


def coincidenze_arena():
    """Quante volte il bonus d'attacco letto e quello rifatto col conto
    coincidono. Letti dal rapporto dell'arena, che li misura.

    Se il rapporto c'e' ma la frase non si trova, questo script si FERMA
    invece di cavarsela con una prosa generica: un numero che sparisce da
    un documento senza che nessuno se ne accorga e' il difetto che CLAUDE.md
    3 vieta, e sostituirlo con «la maggior parte» sarebbe il modo elegante
    di commetterlo."""
    p = os.path.join(BASE, "RAPPORTO-arena.md")
    if not os.path.exists(p):
        return None
    m = COINCIDENZE.search(open(p, encoding="utf-8").read())
    if not m:
        sys.exit("RAPPORTO-arena.md non dice piu' quante volte il bonus "
                 "d'attacco coincide col conto: la frase e' cambiata, e "
                 "questo rapporto la cita.")
    return tuple(int(x) for x in m.groups())


def lacune_arena():
    """Le lacune che l'arena dichiara, lette dal rapporto che genera.

    Lette e non ricopiate: il rapporto e' generato, e riscrivere qui i suoi
    numeri sarebbe il derivato scritto a mano di CLAUDE.md 3."""
    p = os.path.join(BASE, "RAPPORTO-arena.md")
    if not os.path.exists(p):
        return []
    testo = open(p, encoding="utf-8").read()
    return re.findall(r"^\*\*\d+\. `([^`]+)`\*\*", testo, re.M)


# ------------------------------------------------------------------ rapporto

_VOCE = re.compile(r"^(- |\d+\. )")


def _riflow_elenco(righe, larghezza):
    """Un elenco puntato riavvolto voce per voce.

    Serve perche' alcune voci sono INTERPOLATE — l'elenco dei limiti del
    controllo viene da `_sistema.LIMITI` — e una voce interpolata arriva su
    una riga sola o spezzata dove capita. Lasciarla com'e' darebbe righe da
    trecento caratteri accanto a righe da settanta."""
    voci, corrente = [], []
    for r in righe:
        if _VOCE.match(r) and corrente:
            voci.append(corrente)
            corrente = []
        corrente.append(r.strip())
    if corrente:
        voci.append(corrente)
    fuori = []
    for v in voci:
        testo = " ".join(v)
        marca = _VOCE.match(testo).group(1)
        fuori.append(textwrap.fill(
            testo[len(marca):], width=larghezza, initial_indent=marca,
            subsequent_indent=" " * len(marca), break_long_words=False,
            break_on_hyphens=False))
    return "\n".join(fuori)


def riflow(testo, larghezza=78):
    fuori = []
    for blocco in testo.split("\n\n"):
        righe = blocco.split("\n")
        if any(r.lstrip().startswith(("|", "#", ">", "*Generato"))
               or r.startswith("    ") or r.strip() in ("---", "")
               for r in righe):
            fuori.append(blocco)
            continue
        if _VOCE.match(righe[0]):
            fuori.append(_riflow_elenco(righe, larghezza))
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
    lac = lacune_arena()
    coinc = coincidenze_arena()
    mancanti = verifica_tabella(lac)
    if mancanti:
        sys.exit("REGOLE_NEL_CODICE non corrisponde piu' al progetto:\n  "
                 + "\n  ".join(mancanti))

    b = blocchi()
    n_mostri, n_blocchi_mostri, mostri_strutturati = mostri_e_blocchi()
    copie, marcite, riconosciute, piantate = copie_di_sistema()
    tabelle, ingressi_coperti = sede_di_sistema()
    letti = len([f for f in SIS._sorgenti()
                 if os.path.relpath(f, RADICE) != "dati/_sistema.py"])

    # Il totale "prosa" del progetto esclude i chassis generati, come in
    # analizza_personaggio.d_arena(): sono l'unica famiglia che si rifa' con
    # un comando invece che a mano.
    tot_scritti = sum(t for k, (t, _) in b.items() if "chassis" not in k)
    eff_scritti = sum(e for k, (_, e) in b.items() if "chassis" not in k)
    tot_generati, eff_generati = b["classi (chassis, generati)"]

    media = n_blocchi_mostri / n_mostri
    proiezione = round(30 * media)

    per_natura = {}
    for etichetta, percorso, simbolo, natura, dove, stato in REGOLE_NEL_CODICE:
        per_natura.setdefault(natura, []).append(
            (etichetta, percorso, simbolo, dove, stato))
    aperte = [r for v in per_natura.values() for r in v
              if r[4] != "chiusa"]
    aperte_dato = [r for r in aperte if r[3].startswith("DATO")]

    testo = f"""# Dove vive la meccanica — la decisione presa, e cosa il controllo vede

*Generato da `dati/analizza_meccanica.py`.*

---

## 0. La domanda, e come e' stata chiusa

Delle 17 lacune che la prima fetta verticale ha dichiarato, tre
pesavano piu' delle altre ed erano la stessa cosa vista da tre lati:

- il personaggio non era un dato — `attacco` era un **campo** sul mostro e
  una **funzione** sul personaggio;
- le regole di sistema non avevano sede — d20 + bonus contro CA, 20 critico,
  1 mancato stavano in un file Python;
- un innesco non ha un campo — il motore riconosce il Death Throes **dal
  nome**.

Le prime due sono chiuse: {cita('criterio-meccanica')} dice dove vive la
meccanica, {cita('attacco-unica-lettura')} dice che `attacco` si legge una
volta sola. La terza resta aperta ed e' la lacuna `innesco-non-dichiarato`.

Questo documento non e' piu' una proposta: e' la **misura della decisione
presa**. Le due domande a cui risponde adesso sono diverse da prima — cosa il
controllo anti-duplicazione riesce a vedere (§2), e cosa e' cambiato nel
registro delle lacune (§3).

---

## 1. QUALE meccanica sta nei dati e quale nel codice

Il criterio non poteva essere «tutto nei dati»: la risoluzione del d20 e' la
stessa per ogni creatura e non guadagna niente a diventare un dato. Ma non
poteva nemmeno essere «tutto cio' che non varia sta nel codice», perche' il
codice **aveva gia' ripetuto se stesso**.

La regola e' {cita('criterio-meccanica')}: **tre domande in ordine, e la
prima che risponde decide.**

1. **Varia da portatore a portatore?** → **DATO DI CONTENUTO.** Il danno di
   un'arma, la CD di un tiro salvezza, quali condizioni impone un tratto, e
   **quando un tratto scatta**. Un innesco varia — alla morte, quando si
   viene colpiti, all'inizio del turno — quindi e' un dato, e riconoscerlo
   dal nome e' fragile *per costruzione*, non per pigrizia.
2. **Non varia: e' un valore o una procedura?** Un **valore o una tabella**
   che la fonte stampa — il bonus di competenza per livello, il
   modificatore da punteggio, i moltiplicatori di resistenza e vulnerabilita'
   — e' un **DATO DI SISTEMA**. Una **procedura** — tira, confronta, applica,
   passa il turno — e' **CODICE**.
3. **E' una procedura: quali nomi pronuncia?** I termini che nomina — tipi di
   danno, condizioni, tipi di azione — devono venire da un **vocabolario
   condiviso** e non essere stringhe scritte nel codice. E' gia' la regola di
   {cita('vocabolario-italiano')}, e vale anche quando il consumatore e' il
   motore invece di uno schema. E' la domanda che ha portato a
   {cita('condizioni-vocabolario-srd')}: le condizioni che un mostro dichiara
   di ignorare sono nomi, e i nomi vengono dal vocabolario anche quando il
   motore non sa ancora applicarli.

Applicato a cio' che vive nel codice, il criterio taglia cosi':

{tabella(["natura", "quante", "chiuse", "aperte", "sede"],
         [[n, len(v), sum(1 for x in v if x[4] == "chiusa"),
           sum(1 for x in v if x[4] != "chiusa"),
           "; ".join(sorted({sede(x[3]) for x in v}))]
          for n, v in per_natura.items()])}

Riga per riga:

{tabella(["regola", "vive in", "natura", "dove", "stato"],
         [[e, f"`{p}` → `{s}`", n, d, st]
          for n, v in per_natura.items() for e, p, s, d, st in v])}

Le {len(aperte)} righe aperte non sono un difetto del criterio: sono il
criterio che le ha **nominate**. {len(aperte_dato)} di esse dicono la stessa
cosa — un dato che dovrebbe esistere e non esiste: l'innesco di un tratto, la
politica d'uso di una risorsa, l'origine del bonus d'attacco di un mostro — e
nessuna delle {len(aperte_dato)} si chiude scrivendo codice.

---

## 2. La sede delle regole di sistema, e il controllo che la tiene ferma

`dati/sistema/` esiste, con il suo schema e il suo validatore. Contiene
{len(tabelle)} dati che coprono **{ingressi_coperti} ingressi**:

{tabella(["dato di sistema", "genere", "letture", "ingressi"],
         [[f"`{i}`", g, l, n] for i, g, l, n in tabelle])}

Il bonus di competenza e' **una tabella con due letture** — per livello del
personaggio e per grado sfida del mostro — e questa e' la prova che la sede
serviva: prima erano due scritture in due file, e nessuna esecuzione le
metteva una contro l'altra.

**La sede da sola non chiude niente.** Spostare una formula dal codice a un
JSON impedisce la divergenza solo se qualcosa impedisce che venga
*riscritta* altrove. Le otto strutture doppie che il progetto ha chiuso nei
dati sono state chiuse da schemi e validatori; la nona vive nel **codice**,
dove non arrivava ne' l'uno ne' l'altro. Il controllo anti-duplicazione di
`dati/_sistema.py`, eseguito da `dati/valida_sistema.py`, e' il primo
controllo del progetto che guarda il codice invece dei dati.

### Cosa il controllo VEDE

Legge **{letti} sorgenti Python** (la sede stessa esclusa: li' le tabelle
devono esserci) e li guarda in due modi.

- **Per forma.** L'espressione, riconosciuta sul codice **tokenizzato**:
  stringhe, commenti e f-string vengono scartati prima di guardare. Non e' un
  dettaglio di implementazione — questo stesso documento *descrive* la
  formula della CD, ed e' il suo mestiere. Un controllo che segnalasse la
  prosa griderebbe al lupo, e un controllo che grida al lupo viene spento.
- **Per valori.** La tabella espansa a mano: una corsa di almeno
  {SIS.CORSA_MINIMA} interi consecutivi con almeno {SIS.DISTINTI_MINIMI}
  valori distinti, separati **solo da punteggiatura**. Il vincolo dei
  separatori e' la regola decisiva: `dati/_sfere_5e.py` ha una colonna di
  livelli d'incantesimo che per caso comincia come il bonus di competenza, e
  prima di quella regola veniva segnalata.
- **Le eccezioni, e la loro morte.** {len(SIS.ECCEZIONI)} occorrenza e'
  permessa — la sonda di `valida_sistema.py`, che ricalcola la tabella con la
  formula stampata dalla fonte per confrontarla riga per riga. E' un
  riconfronto, non una copia. Un'eccezione dichiarata che non trova piu' il
  suo marcatore viene segnalata **come una copia**: un permesso che non
  protegge piu' niente e' peggio di nessun permesso.
- **Se stesso.** A ogni giro gli si piantano davanti {piantate} copie
  costruite apposta e {len(SIS.NON_COPIE_FINTE)} sorgenti che gli somigliano
  senza esserlo, e si pretende che veda le prime e non i secondi. Oggi ne
  riconosce **{riconosciute} su {piantate}**. Serve perche' su un repository
  pulito un rilevatore rotto e uno funzionante tacciono allo stesso modo, e
  la differenza si scopre il giorno in cui serviva.

Sul codice di oggi trova **{len(copie)} copie** e
**{len(marcite)} eccezioni marcite**. Non e' un risultato scontato: quando e'
stato acceso ne trovava cinque — il modificatore di caratteristica in
`dati/valida_effetti.py` e in `motore/combattimento.py`, il bonus di
competenza in `dati/_srd51.py` e in `dati/valida_effetti.py`, la CD del tiro
salvezza ancora in `valida_effetti.py`. Sono le occorrenze che leggono la
sede adesso.

### Cosa il controllo NON vede

{chr(10).join('- ' + l for l in SIS.LIMITI)}

Questo elenco vive in `dati/_sistema.py` e non solo qui, perche' chi aggiunge
una formula legge quel file e non questo rapporto. Va letto insieme al
risultato: **un controllo di cui non si conosce il bordo viene creduto piu'
di quanto valga**, e un controllo creduto troppo e' esattamente il modo in
cui una struttura doppia torna a formarsi sotto la protezione di qualcosa che
non la guarda.

Il quarto limite merita una riga in piu' perche' non e' teorico: un mostro
che si portasse **gia' sommato** il proprio bonus d'attacco non ripete
nessuna formula, e questo controllo non se ne accorgerebbe. E' la stessa
lacuna che `attacco_di()` misura dall'altro lato, ed e' il §3.

---

## 3. `attacco_di()`: una lettura sola, e cosa ha spostato nel registro

Il fatto da cui si partiva: sul mostro `attacco` era **letto**, sul
personaggio era **composto** da razza + classe + oggetto + stile. Le due
strade ovvie rompevano ciascuna qualcosa di gia' deciso — far memorizzare
`attacco` al personaggio significa scrivere a mano un derivato, che
{cita('doppio-strato')} e CLAUDE.md 3 vietano; far derivare `attacco` al
mostro significa inventare derivazioni che la fonte non da', e la prova ha
gia' un id: {cita('cd-origine-dichiarata')}.

La risposta e' {cita('attacco-unica-lettura')}: **cio' che e' condiviso non
e' il campo, e' la LETTURA.** La forma della risposta e' `effetto.attacco` di
`effetto.schema.json` e non cambia; il **mostro** la porta come dato; il
**personaggio** porta solo gli **ingressi** non derivabili — razza, classe,
livello, punteggi, equipaggiato, scelte — e ogni campo ricavabile da quelli
**non esiste** nella sua forma, che e' la versione piu' forte del divieto: la
stessa che {cita('bersaglio-legale-filtro')} ha usato rendendo impossibile e
non solo sconsigliato fissare un ospite. Il **motore** ha una funzione
`attacco_di(combattente, azione)` che torna quella forma: sul mostro la
legge, sul personaggio la compone, e chi la chiama non sa quale dei due casi
ha davanti.

Il registro delle lacune e' passato da **17 a {len(lac)}**: tre chiuse, una
aperta e richiusa nello stesso giro.

- **Chiusa `attacco-del-pg`** — il personaggio non calcola piu' l'attacco in
  una funzione del motore: lo compone dagli ingressi, con la stessa lettura
  del mostro.
- **Chiusa `regole-di-sistema`** — le soglie del 20 e dell'1 naturale, i
  moltiplicatori delle difese, il modificatore e la competenza vengono da
  `dati/sistema/`. La sede che {cita('sconfessione-condivisa')} aveva
  promesso e mai costruito ha smesso di essere una lista d'attesa.
- **`attacco-origine-non-dichiarata`: aperta guardando i due lati insieme,
  chiusa nello stesso giro** — ed e' il modo giusto di leggerla. Un
  `bonus_colpire` **letto dalla scheda** e uno che **tornerebbe col conto**
  si scrivono uguali, che e' lo stesso difetto che
  {cita('cd-origine-dichiarata')} aveva chiuso per la CD. Al secondo caso in
  due giri la regola e' stata scritta una volta per tutte invece di essere
  riapplicata: {cita('origine-e-un-dato')}, di cui `cd_origine` e
  `bonus_origine` sono le due applicazioni. La lacuna del motore non e'
  sparita: e' diventata **condizionata al dato**, e scatta esattamente sugli
  attacchi che non dichiarano l'origine. Oggi nessuno dei due strutturati,
  domani il terzo se lo si struttura senza compilarla.

L'arena misura quanto pesa: dei {coinc[0]} bonus d'attacco che il bestiario
scrive in prosa, {coinc[1]} tornano col conto e {coinc[2]} no. Il numero che
conta non e' {coinc[1]}: e' che **{coinc[1]} coincidenze non sono
{coinc[1]} conferme**. La CD 11 del Baaz e' stampata dalla fonte *e* torna
col conto, quindi un controllo che confronta letto e derivato non l'avrebbe
mai segnalata — non perche' fosse corretta, ma perche' letto e derivato sono
indistinguibili quando coincidono. Contare le coincidenze invece di fidarsene
e' la differenza fra verificare e credere, ed e' la ragione per cui il rimedio
e' un `bonus_origine` e non un controllo piu' furbo: nessun controllo puo'
essere abbastanza furbo da distinguere due numeri uguali.

E la domanda giusta non era se {coinc[0] - coinc[2]} su {coinc[0]} bastasse:
era **quanti altri campi hanno questa forma**. Sono quattro ancora scoperti —
il bonus di danno, i bonus di abilita', la percezione passiva, e le CD ancora
in prosa — misurati nella sezione 4 di `RAPPORTO-arena.md`. Il caso che
insegna di piu' e' la **percezione passiva**, dove il conto torna il **cento
per cento** delle volte: e' il campo dove fidarsi del conto e' piu'
pericoloso, non meno.

---

## 4. Cosa costa cambiare rotta ora, e cosa costa dopo

Il costo di un cambio di forma di `effetto` e' il numero di blocchi da
riscrivere, e i blocchi non costano tutti uguale: quelli **generati** si
rifanno con un comando, quelli **scritti a mano** vanno riletti insieme alla
prosa che li accompagna, perche' il controllo 2 di `valida_effetti.py`
pretende che le due dicano la stessa cosa.

{tabella(["famiglia", "blocchi", "con `effetto`", "come si rifanno"],
         [[k, t, e, "a mano" if "chassis" not in k else "con un comando"]
          for k, (t, e) in b.items()])}

**Adesso: {eff_scritti} blocchi scritti a mano portano `effetto`** — tutti
sui mostri, su {mostri_strutturati} schede delle {n_mostri} convertite; razze
e privilegi di classe non ne hanno ancora nessuno. Piu' {eff_generati}
generati da `_srd51.py`, che si rifanno con un comando e quindi non entrano
nel costo.

**Dopo trenta mostri strutturati:** il bestiario converte in media
{f"{media:.1f}".replace(".", ",")} blocchi per scheda, quindi trenta schede sono circa
**{proiezione} blocchi in piu'**, tutti scritti a mano — circa
**{proiezione / max(eff_scritti, 1):.0f} volte** il lavoro di oggi. E il
moltiplicatore e' la parte ottimista: un blocco di mostro non e' una riga di
JSON ma una **decisione di conversione** con la sua prosa accanto e la sua
pagina di manuale alle spalle, quindi riaprirlo significa riaprire la fonte.

Il verso della lezione e' pero' importante, perche' il progetto ne ha gia'
imparata una **opposta**: {cita('schema-modelli')} ha aspettato di avere tre
creature prima di disegnare lo schema dei modelli, e
{cita('barbaro-rimandato')} ha rifiutato di disegnare uno schema su un caso
solo. Le due lezioni non si contraddicono se si separa **disegnare** da
**convertire in volume**: si disegna quando ci sono abbastanza casi, si
converte in volume dopo che la forma e' ferma.

E' la ragione per cui la forma e' stata decisa adesso, con {len(lac)} lacune
misurate e due mostri strutturati, invece che dopo: oggi il costo di
sbagliare forma e' {eff_scritti} blocchi; fra trenta schede sarebbe
{proiezione + eff_scritti}, e la differenza non e' recuperabile con nessuno
script.

---

## 5. Cosa questo documento NON tocca

Le tre zone morte di schema — classi, razze, divinita' — restano aperte. La
decisione 51 (`criterio-meccanica`) e' la condizione che mancava per
chiuderle: uno schema disegnato attorno a una forma che sta per cambiare si
chiude due volte. La misura di quelle tre sta in
`dati/RAPPORTO-zona-morta-classi.md`.

Il volume del bestiario resta fermo: i blocchi ancora senza `effetto` si
convertono dopo il registro delle lacune, non prima.

---

*Le tre decisioni sono prese e hanno un id: {cita('criterio-meccanica')},
{cita('attacco-unica-lettura')}, {cita('condizioni-vocabolario-srd')}. Cio'
che resta di questo documento e' la misura del loro effetto — e il bordo del
controllo che le tiene ferme, che e' la parte da rileggere quando qualcuno
scrivera' la prossima formula.*
"""
    return riflow(testo)


if __name__ == "__main__":
    out = os.path.join(BASE, "RAPPORTO-meccanica.md")
    testo = rapporto()
    with open(out, "w", encoding="utf-8") as f:
        f.write(testo)
    print(f"scritto {out} ({len(testo.splitlines())} righe)")
