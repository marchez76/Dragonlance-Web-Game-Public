#!/usr/bin/env python3
"""
Il campo `effetto` contro la prosa che gli sta accanto.

PERCHE' ESISTE — E' IL PEZZO CHE PAGA IL COSTO DI `effetto`
    Aggiungere una struttura accanto a una prosa che dice la stessa cosa
    crea una struttura doppia, e questo progetto ne ha gia' viste sei
    sfasarsi in silenzio. La settima non e' stata evitata scrivendo meglio:
    e' stata evitata rendendo il riconfronto automatico e bloccante. Senza
    questo file il campo `effetto` non andava aggiunto affatto.

    Il caso che lo motiva e' concreto e gia' nel corpus: la CD 11 della
    presenza terrificante compare in DUE schede — tylor-giovane e
    tylor-adolescente — scritta due volte in prosa, con la nota che dichiara
    che la difficolta' NON cresce fra le due categorie. Due copie non
    verificate divergono sempre; questa e' verificata (controllo 5).

I CINQUE CONTROLLI
    1. FORMA. Ogni `effetto` valido contro dati/schema/effetto.schema.json.
    2. PROSA CONTRO STRUTTURA. Ogni numero che la struttura dichiara deve
       comparire nella prosa accanto, e i dadi e le CD che la prosa nomina
       devono comparire nella struttura. E' il controllo che coglie la
       revisione fatta da un lato solo.
    3. RIFERIMENTI. Ogni condizione citata per id esiste in dati/condizioni/,
       e la catena `implica` si risolve. Un id che non risolve e' un
       riferimento a niente, che e' peggio di una copia.
    4. I DUE ESTREMI DELLA COMPETENZA. Le categorie nominate dalle competenze
       di classe esistono davvero come `categoria` in dati/oggetti/. Una
       competenza in una categoria inesistente e' una competenza in niente.
    5. LE CD DICHIARATE DEVONO ESSERE SPIEGATE. Ogni CD in `effetto` porta
       `cd_origine` — `fonte`, `derivata` o `stimata` — e il controllo si
       comporta diversamente per ognuna: una `derivata` deve tornare col
       conto 8 + competenza + una caratteristica del portatore, una `fonte`
       e una `stimata` no ma devono dire in `cd_derivazione` da dove
       vengono. E' la distinzione fra una CD letta e una CD scelta: il
       metodo di conversione la impone gia' per i mostri (osservato contro
       ipotizzato) e qui diventa un campo.

       DUE INFORMAZIONI, DUE CAMPI. Fino al 02/09/2026 ce n'era uno solo,
       `cd_derivata_da`, e portava una contraddizione: la sua descrizione
       diceva «come la CD e' stata ottenuta, QUANDO NON E' UN DATO DI
       FONTE», mentre questo controllo pretendeva di riempirlo proprio per
       una CD di fonte non derivabile. La CD 11 del Death Throes del Baaz e'
       quel caso: stampata nel blocco ufficiale SotDQ e non derivabile dal
       conto, quindi o si violava la descrizione o si violava il controllo.
       Un campo con due significati e' inaffidabile da entrambi i lati.
       `cd_origine` dice DA COSA viene la CD; la derivabilita' non e' un
       campo perche' e' calcolabile, e questo controllo la calcola invece di
       fidarsi di quello che il dato ne afferma.

       Il controllo vale sui blocchi che hanno gia' una struttura, non su
       tutto il bestiario in prosa. La misura, presa il 02/09/2026 sui 52
       mostri: delle 35 CD scritte in prosa, 29 sono derivabili e 6 no —
       il Cavaliere della Morte (2), l'Erba Scintillante, il Jarak-Sinn, il
       Ragno Botola e lo Skyfisher. Non sono errori: sono CD dichiarate
       dalla fonte o stimate, e le rispettive note lo dicono. Ma lo dicono
       in prosa, dove nessun controllo le legge — ed e' esattamente il buco
       che `cd_origine` chiude man mano che quei blocchi si strutturano.
       Renderlo bloccante adesso su blocchi ancora in prosa segnalerebbe
       sei casi corretti, e un controllo che grida al lupo viene spento.

       LA COINCIDENZA E' UN'INFORMAZIONE, NON UN ERRORE. Una CD di fonte
       puo' tornare col conto per caso: 29 delle 35 CD in prosa lo fanno, e
       fra quelle ce ne sono certamente di stampate. Il controllo la
       registra e non la segnala — una CD `fonte` che coincide non e'
       sbagliata, ma sapere quante sono dice quanto vale il conto come
       prova, e la risposta e' poco.

QUANTO VALE OGNI CONTROLLO — detto per non sopravvalutarlo
    Sui blocchi generati da un build_*.py, prosa e struttura escono dalla
    stessa passata: li' il controllo 2 non verifica due autori indipendenti,
    verifica che nessuno abbia toccato il file A VALLE del generatore — che
    e' il punto 2 di CLAUDE.md, e nel progetto e' gia' successo tre volte.
    Sui blocchi scritti a mano — i mostri, i privilegi di fonte — la prosa e
    la struttura hanno davvero due autori diversi, e li' il confronto e'
    genuino. Sono due utilita' diverse e conviene saperlo.

Uso:  python3 dati/valida_effetti.py       # esce != 0 se trova divergenze
      python3 dati/valida_effetti.py -v    # elenca anche cosa ha confrontato
"""

import collections
import glob
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import _schemi as S  # noqa: E402
import _srd51 as R  # noqa: E402

DADO = re.compile(r"\b(\d+d\d+)\b")
CD = re.compile(r"\bCD\s*(\d+)\b")


# ------------------------------------------------------------------ caricamento

def carica(cartella):
    out = []
    for f in sorted(glob.glob(os.path.join(BASE, cartella, "*.json"))):
        out.append((os.path.basename(f), json.load(open(f, encoding="utf-8"))))
    return out


def blocchi_con_effetto():
    """(origine, blocco, portatore) per ogni blocco che porta un `effetto`.

    Cerca dove i blocchi stanno davvero, non dove si suppone che stiano:
    classi (features e chassis_features), mostri (actions/traits/reactions),
    razze (traits), modelli. Un blocco nuovo in un posto non elencato qui
    passerebbe inosservato, quindi la lista va tenuta insieme agli schemi."""
    fonti = [
        ("classi", ["mechanics_5e.features", "mechanics_5e.chassis_features"]),
        ("razze", ["mechanics_5e.traits"]),
        ("mostri", ["mechanics_5e.actions", "mechanics_5e.traits",
                    "mechanics_5e.reactions", "mechanics_5e.legendary_actions"]),
        ("modelli", ["mechanics_5e.features", "mechanics_5e.abilities"]),
    ]
    out = []
    for cartella, percorsi in fonti:
        for nome, d in carica(cartella):
            for percorso in percorsi:
                nodo = d
                for chiave in percorso.split("."):
                    nodo = (nodo or {}).get(chiave) if isinstance(nodo, dict) else None
                for b in (nodo or []):
                    if isinstance(b, dict):
                        out.append((f"{cartella}/{nome}::{percorso.split('.')[-1]}",
                                    b, d))
    return out


# ------------------------------------------------- 1. forma  2. prosa/struttura

def numeri_struttura(eff):
    """I numeri che la struttura dichiara: dadi e CD."""
    dadi, cd = set(), set()

    def danni(lista):
        for x in (lista or []):
            if x.get("dadi"):
                dadi.add(x["dadi"])

    att = eff.get("attacco") or {}
    danni(att.get("danno"))
    ts = eff.get("tiro_salvezza") or {}
    if ts.get("cd") is not None:
        cd.add(int(ts["cd"]))
    for esito in ("fallimento", "successo", "fallimento_ripetuto"):
        danni((ts.get(esito) or {}).get("danno"))
    gua = eff.get("guarigione") or {}
    if gua.get("dadi"):
        dadi.add(gua["dadi"])
    return dadi, cd


def confronta_prosa(prosa, eff, err):
    """Controllo 2. I dadi e le CD devono comparire da entrambe le parti."""
    if not prosa:
        err("effetto presente ma mechanics_5e (la prosa) e' vuota: la "
            "struttura non e' la forma autoritativa, e' la sua lettura")
        return
    dadi_s, cd_s = numeri_struttura(eff)
    dadi_p = set(DADO.findall(prosa))
    cd_p = {int(x) for x in CD.findall(prosa)}

    for d in sorted(dadi_s - dadi_p):
        err(f"la struttura dichiara i dadi {d}, la prosa non li nomina")
    for d in sorted(dadi_p - dadi_s):
        err(f"la prosa nomina i dadi {d}, la struttura non li porta")
    for c in sorted(cd_s - cd_p):
        err(f"la struttura dichiara CD {c}, la prosa non la nomina")
    for c in sorted(cd_p - cd_s):
        err(f"la prosa nomina CD {c}, la struttura non la porta")

    # I modificatori numerici: il valore deve comparire nella prosa.
    for m in (eff.get("modificatori") or []):
        v = m.get("valore")
        if isinstance(v, int) and v != 0:
            segno = f"+{v}" if v > 0 else str(v)
            if segno not in prosa and str(abs(v)) not in prosa:
                err(f"modificatore {m['bersaglio']} {segno}: la prosa non lo nomina")

    # Il multiattacco: quante volte, e quale azione ripete.
    ma = eff.get("multiattacco") or {}
    if ma:
        n = ma["quanti"]
        parole = {2: ("due", "2"), 3: ("tre", "3"), 4: ("quattro", "4")}
        if not any(w in prosa.lower() for w in parole.get(n, (str(n),))):
            err(f"multiattacco da {n}: la prosa non lo dice")

    # Gli usi di una risorsa a numero fisso.
    ris = eff.get("risorsa") or {}
    if isinstance(ris.get("usi"), int):
        n = ris["usi"]
        parole = {1: ("una volta", "un uso", "rifarlo", "riposo")}
        if str(n) not in prosa and not any(w in prosa.lower()
                                           for w in parole.get(n, ())):
            err(f"risorsa a {n} usi: la prosa non lo dice")


# ------------------------------------------------------ 3. riferimenti/condizioni

def condizioni_citate(eff):
    out = set()
    ts = eff.get("tiro_salvezza") or {}
    # `fallimento_ripetuto` va incluso o la condizione del secondo tempo non
    # verrebbe mai controllata: e' il campo nuovo, ed e' esattamente dove un
    # controllo dimenticato lascia passare un id inesistente.
    for esito in ("fallimento", "successo", "fallimento_ripetuto"):
        for c in ((ts.get(esito) or {}).get("condizioni") or []):
            out.add(c["id"])
    return out


def controlla_condizioni(err_globale):
    """Controllo 3, lato cartella: la catena `implica` si risolve, e nessuna
    condizione ridichiara le clausole di quella che implica (sarebbe la copia
    che la sede unica esiste per impedire)."""
    cond = {d["id"]: d for _, d in carica("condizioni")}
    for cid, d in sorted(cond.items()):
        proprie = {tuple(sorted(e.items())) for e in d["effetti"]
                   if not isinstance(e.get("caratteristiche"), list)}
        for altro in d.get("implica") or []:
            if altro not in cond:
                err_globale(f"condizioni/{cid}: implica '{altro}', che non "
                            f"esiste in dati/condizioni/")
                continue
            ripetute = proprie & {tuple(sorted(e.items()))
                                  for e in cond[altro]["effetti"]
                                  if not isinstance(e.get("caratteristiche"), list)}
            for r in sorted(ripetute):
                err_globale(f"condizioni/{cid}: ridichiara '{dict(r)['clausola']}', "
                            f"gia' portata da '{altro}' che implica. La sede "
                            f"unica serve proprio a non ripeterla")
    return cond


def nomi_dei_blocchi(portatore):
    """I `name` di tutti i blocchi del portatore, per risolvere un rimando."""
    m = portatore.get("mechanics_5e") or {}
    fuori = set()
    for k in ("traits", "actions", "bonus_actions", "reactions",
              "legendary_actions", "features", "chassis_features"):
        for b in (m.get(k) or []):
            if isinstance(b, dict) and b.get("name"):
                fuori.add(b["name"])
    return fuori


# ---------------------------------------------- 4. i due estremi della competenza

def controlla_competenze(err_globale):
    """Le categorie nominate dalle classi devono esistere in dati/oggetti/."""
    armi, armature = set(), set()
    for _, o in carica("oggetti"):
        m = o.get("mechanics_5e") or {}
        if (m.get("weapon_5e") or {}).get("categoria"):
            armi.add(m["weapon_5e"]["categoria"])
        if (m.get("armor_5e") or {}).get("categoria"):
            armature.add(m["armor_5e"]["categoria"])

    for atteso, viste, cosa in ((set(R.CATEGORIE_ARMA), armi, "arma"),
                                (set(R.CATEGORIE_ARMATURA), armature, "armatura")):
        for c in sorted(atteso - viste):
            err_globale(f"_srd51 dichiara la categoria d'{cosa} '{c}', che "
                        f"nessun oggetto porta: una competenza in quella "
                        f"categoria sarebbe una competenza in niente")
        for c in sorted(viste - atteso):
            err_globale(f"dati/oggetti/ usa la categoria d'{cosa} '{c}', che "
                        f"_srd51 non dichiara")

    for nome, d in carica("classi"):
        st = ((d.get("mechanics_5e") or {}).get("structural") or {})
        for chiave, viste, cosa in (("weapon_proficiencies", armi, "arma"),
                                    ("armor_proficiencies", armature, "armatura")):
            for c in (st.get(chiave) or {}).get("categorie") or []:
                if c not in viste:
                    err_globale(f"classi/{nome}: competenza in {cosa} '{c}', "
                                f"categoria che nessun oggetto porta")
    return len(armi), len(armature)


# --------------------------------------------- 5. le CD dichiarate vanno spiegate

def competenza_da_cr(cr):
    """Bonus di competenza dal grado sfida, tabella 5e."""
    try:
        n = float(cr)
    except (TypeError, ValueError):
        return 2
    return 2 if n < 1 else max(2, 2 + (int(n) - 1) // 4)


def cd_attese(portatore):
    """Le CD che le caratteristiche del portatore possono generare."""
    m = portatore.get("mechanics_5e") or {}
    ab = m.get("abilities") or {}
    if not ab:
        return None
    pb = competenza_da_cr((m.get("challenge_rating") or {}).get("value"))
    return {8 + pb + (v - 10) // 2 for v in ab.values()}


def controlla_cd(eff, portatore, err):
    """Controllo 5, su un blocco che ha gia' la struttura.

    Torna l'origine dichiarata e se la CD combacia col conto, per la
    misura finale: la coincidenza fra una CD di fonte e il conto e' un
    dato sul valore del conto, non un errore."""
    ts = eff.get("tiro_salvezza") or {}
    cd = ts.get("cd")
    if cd is None:
        return None
    origine = ts.get("cd_origine")
    if not origine:
        err(f"CD {cd} senza `cd_origine`: da dove viene una CD non si "
            f"deduce, si dichiara")
        return None

    if origine in ("fonte", "stimata") and not ts.get("cd_derivazione"):
        err(f"CD {cd} dichiarata `{origine}` e `cd_derivazione` vuoto: una "
            f"CD che non si deriva dal conto e non dice da dove viene e' "
            f"una stima nascosta")

    attese = cd_attese(portatore)
    if attese is None:
        return (origine, None)
    combacia = cd in attese
    if origine == "derivata" and not combacia:
        err(f"CD {cd} dichiarata `derivata` ma non e' 8 + competenza + una "
            f"caratteristica del portatore (attese: {sorted(attese)}): "
            f"o l'origine e' un'altra, o il numero e' sbagliato")
    return (origine, combacia)


# --------------------------------------------------------------------- report

def main(argv):
    verbose = "-v" in argv
    v = S.validatore("effetto.schema.json")

    errori = []
    def err_globale(m):
        errori.append(m)

    # Il vocabolario condiviso e' applicato solo se il `$ref` fra file
    # risolve davvero: provato, non assunto.
    for m in S.verifica_riferimenti():
        err_globale(m)

    cond = controlla_condizioni(err_globale)
    n_armi, n_armature = controlla_competenze(err_globale)

    con_effetto = 0
    con_cd = 0
    origini = collections.Counter()
    coincidenze = 0
    for origine, b, portatore in blocchi_con_effetto():
        eff = b.get("effetto")
        if not eff:
            continue
        con_effetto += 1
        etichetta = f"{origine} '{b.get('name', '?')}'"

        def err(m, _e=etichetta):
            errori.append(f"{_e}: {m}")

        for e in sorted(v.iter_errors(eff), key=lambda e: list(e.path)):
            err(f"[schema] {'.'.join(map(str, e.path)) or '(radice)'}: {e.message[:160]}")

        confronta_prosa(b.get("mechanics_5e"), eff, err)
        if (eff.get("tiro_salvezza") or {}).get("cd") is not None:
            con_cd += 1
            esito = controlla_cd(eff, portatore, err)
            if esito:
                origini[esito[0]] += 1
                if esito[0] == "fonte" and esito[1]:
                    coincidenze += 1

        for cid in sorted(condizioni_citate(eff)):
            if cid not in cond:
                err(f"cita la condizione '{cid}', che non esiste in "
                    f"dati/condizioni/")

        ma = eff.get("multiattacco") or {}
        if ma and ma.get("azione") not in nomi_dei_blocchi(portatore):
            err(f"il multiattacco ripete l'azione '{ma['azione']}', che il "
                f"portatore non ha: un riferimento a niente")

    # Anche le condizioni stesse hanno prosa e clausole da tenere allineate.


    print(f"\n{con_effetto} blocchi con `effetto` confrontati con la loro prosa.")
    print(f"{len(cond)} condizioni, {n_armi} categorie d'arma e "
          f"{n_armature} d'armatura incrociate con le competenze.")
    per_origine = ", ".join(f"{n} {o}" for o, n in sorted(origini.items())) or "nessuna"
    print(f"{con_cd} CD dichiarate nella struttura ({per_origine}); "
          f"{coincidenze} di fonte combaciano comunque col conto "
          f"8 + competenza + caratteristica.")

    if errori:
        print(f"\n{len(errori)} DIVERGENZE fra prosa e struttura:")
        for e in errori:
            print(f"  {e}")
        return 1
    print("\nNessuna divergenza: la prosa e la struttura dicono la stessa cosa.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
