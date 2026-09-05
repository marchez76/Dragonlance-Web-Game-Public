#!/usr/bin/env python3
"""
I dati di sistema contro il loro schema, contro la fonte, e contro il codice.

PERCHE' ESISTE — E' IL PEZZO CHE PAGA IL COSTO DI `dati/sistema/`
    Spostare una formula dal codice a un JSON non chiude niente da solo:
    chiude solo se qualcosa impedisce che venga riscritta altrove. Le otto
    strutture doppie che il progetto ha chiuso nei dati sono state chiuse da
    schemi e validatori; la nona vive nel CODICE, dove non arrivava nessuno
    dei due. Questo file e' il primo controllo del progetto che guarda il
    codice invece dei dati.

I CINQUE CONTROLLI
    1. FORMA. Ogni file di dati/sistema/ valido contro sistema.schema.json,
       con l'id uguale al nome del file.
    2. COPERTURA. Le fasce di una tabella coprono il dominio di ogni sua
       lettura, senza buchi e senza sovrapposizioni. Un buco darebbe un
       ingresso legale senza risposta, ed e' il difetto che una tabella
       battuta a mano produce piu' spesso.
    3. LA SONDA. La tabella ricalcolata con la formula che la fonte stampa,
       confrontata riga per riga. E' l'UNICA occorrenza permessa di quelle
       formule nel codice, ed e' dichiarata per nome in `_sistema.ECCEZIONI`:
       un riconfronto, non una copia. Senza, trenta righe battute a mano non
       hanno nessuno che le verifichi; con, un refuso si vede subito.
    4. PROSA CONTRO STRUTTURA. Ogni numero che la struttura dichiara deve
       comparire nella prosa accanto. E' il controllo 2 di valida_effetti.py
       applicato qui, per la stessa ragione: due scritture della stessa cosa
       divergono se nessuno le mette una contro l'altra.
    5. ANTI-DUPLICAZIONE. Nessuna tabella di sistema riscritta fuori dalla
       sua sede — ne' per forma (l'espressione) ne' per valori (la tabella
       espansa a mano). Cosa questo controllo NON vede sta in
       `_sistema.LIMITI`, e va letto: un controllo di cui non si conosce il
       bordo viene creduto piu' di quanto valga.

Uso:  python3 dati/valida_sistema.py       # esce != 0 se trova divergenze
      python3 dati/valida_sistema.py -v    # elenca anche cosa ha confrontato
"""

import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import _schemi as S  # noqa: E402
import _sistema as SIS  # noqa: E402


# --------------------------------------------------------------- 3. la sonda
#
# Le formule che la fonte stampa accanto alle tabelle. Vivono QUI e in
# nessun altro posto del progetto: `_sistema.ECCEZIONI` lo dichiara, e il
# controllo 5 verifica che la dichiarazione sia ancora vera. Il marcatore
# SONDA sulla riga e' cio' che il controllo cerca.

def _sonda_modificatore(punteggio):
    return (punteggio - 10) // 2  # SONDA: formula SRD del modificatore


def _sonda_competenza(n):
    return 2 + (n - 1) // 4  # SONDA: formula SRD del bonus di competenza


SONDE = {
    ("modificatore-caratteristica", "per_punteggio"): _sonda_modificatore,
    ("bonus-competenza", "per_livello"): _sonda_competenza,
    ("bonus-competenza", "per_grado_sfida"): _sonda_competenza,
}


# ------------------------------------------------------------------ controlli

def controlla_forma(err):
    v = S.validatore("sistema.schema.json")
    for dato_id, d in sorted(SIS.DATI.items()):
        for e in sorted(v.iter_errors(d), key=lambda e: list(e.path)):
            err(f"sistema/{dato_id}: [schema] "
                f"{'.'.join(map(str, e.path)) or '(radice)'}: {e.message[:200]}")
        atteso = os.path.join(SIS.CARTELLA, dato_id + ".json")
        if not os.path.exists(atteso):
            err(f"sistema/{dato_id}: l'id non corrisponde al nome del file")


def controlla_copertura(err):
    """Controllo 2. Nessun buco e nessuna sovrapposizione fra le fasce."""
    for dato_id, d in sorted(SIS.DATI.items()):
        fasce = d.get("fasce")
        if not fasce:
            continue
        ordinate = sorted(fasce, key=lambda f: f["da"])
        for prima, dopo in zip(ordinate, ordinate[1:]):
            if dopo["da"] <= prima["a"]:
                err(f"sistema/{dato_id}: le fasce {prima['da']}-{prima['a']} e "
                    f"{dopo['da']}-{dopo['a']} si sovrappongono")
            elif dopo["da"] != prima["a"] + 1:
                err(f"sistema/{dato_id}: buco fra {prima['a']} e {dopo['da']}: "
                    f"un ingresso legale senza risposta")
        for l in d["letture"]:
            basso, alto = l["dominio"]
            soglia = (l.get("sotto_il_minimo") or {}).get("soglia", basso)
            for i in range(soglia, alto + 1):
                if SIS._in_fascia(dato_id, i) is None:
                    err(f"sistema/{dato_id}/{l['id']}: nessuna fascia copre "
                        f"{l['ingresso']} {i}, che il dominio dichiara legale")
                    break


def controlla_sonda(err, verbose):
    """Controllo 3. La tabella contro la formula stampata dalla fonte."""
    provati = 0
    for (dato_id, lettura_id), formula in sorted(SONDE.items()):
        l = SIS._lettura(dato_id, lettura_id)
        basso, alto = l["dominio"]
        soglia = (l.get("sotto_il_minimo") or {}).get("soglia", basso)
        for i in range(soglia, alto + 1):
            letto = SIS._leggi(dato_id, lettura_id, i)
            atteso = formula(i)
            provati += 1
            if letto != atteso:
                err(f"sistema/{dato_id}/{lettura_id}: {l['ingresso']} {i} da' "
                    f"{letto} nella tabella e {atteso} con la formula della "
                    f"fonte")
        # Sotto la prima fascia la formula NON vale, e il dato lo dichiara:
        # provarla li' segnalerebbe come errore la sola cosa che la lettura
        # aggiunge alla tabella.
        if verbose:
            print(f"   sonda {dato_id}/{lettura_id}: {soglia}..{alto} "
                  f"confrontati con la formula della fonte")
    return provati


_NUMERO = re.compile(r"-?\d+")


def controlla_prosa(err):
    """Controllo 4. I numeri della struttura devono comparire nella prosa.

    Non tutti allo stesso modo, e la differenza e' dichiarata: di una
    TABELLA la prosa nomina gli estremi (il dominio e i valori agli
    estremi), non le trenta righe; di una FORMULA nomina la base; di
    moltiplicatori e soglie nomina ogni valore intero. Un moltiplicatore
    non intero (la resistenza, 0,5) la prosa lo dice a parole — «dimezza» —
    e li' il controllo cerca la parola invece del numero."""
    PAROLE = {0.5: ("dimezza", "meta'")}
    for dato_id, d in sorted(SIS.DATI.items()):
        prosa = d["mechanics_5e"]
        numeri = {int(x) for x in _NUMERO.findall(prosa)}

        def manca(n, _id=dato_id, _p=prosa):
            if int(n) not in numeri:
                err(f"sistema/{_id}: la struttura dichiara {n}, la prosa non "
                    f"lo nomina")

        if d["genere"] == "tabella":
            ordinate = sorted(d["fasce"], key=lambda f: f["da"])
            manca(ordinate[0]["valore"])
            manca(ordinate[-1]["valore"])
            for l in d["letture"]:
                for estremo in l["dominio"]:
                    manca(estremo)
        elif d["genere"] == "formula":
            manca(d["base"])
            for a in d["addendi"]:
                if a not in SIS.DATI:
                    err(f"sistema/{dato_id}: l'addendo '{a}' non e' un dato "
                        f"di sistema: un riferimento a niente")
        elif d["genere"] == "moltiplicatori":
            for m in d["moltiplicatori"]:
                v = m["moltiplicatore"]
                if float(v).is_integer():
                    manca(v)
                elif not any(p in prosa.lower() for p in PAROLE.get(v, ())):
                    err(f"sistema/{dato_id}: il moltiplicatore {v} non e' "
                        f"nella prosa, ne' come numero ne' a parole")
            dichiarate = {m["difesa"] for m in d["moltiplicatori"]}
            if dichiarate != set(d["ordine_di_applicazione"]):
                err(f"sistema/{dato_id}: l'ordine di applicazione non nomina "
                    f"le stesse difese dei moltiplicatori")
        elif d["genere"] == "soglie":
            for s in d["soglie"]:
                manca(s["valore"])
        elif d["genere"] == "metodi":
            # Di un metodo la prosa deve nominare OGNI numero, non gli
            # estremi: non e' una tabella di trenta righe, sono tre
            # procedure corte, e il numero che la prosa non nomina e'
            # esattamente quello che nessuno riconfronta piu'.
            for m in d["metodi"]:
                for campo in ("punteggi", "dadi", "facce",
                              "scarta_i_piu_bassi", "budget"):
                    if m.get(campo) is not None:
                        manca(m[campo])
                for v in m.get("valori") or []:
                    manca(v)
                for c in m.get("costi") or []:
                    manca(c["punteggio"])
                    manca(c["costo"])


def controlla_duplicazione(err):
    """Controllo 5. Nessuna copia fuori dalla sede — e il controllo funziona.

    Prima si prova il controllo, poi lo si usa. Su un repository pulito un
    rilevatore rotto e uno funzionante danno lo stesso risultato — silenzio
    — e la differenza si scopre il giorno in cui serviva. Quindi ogni giro
    gli si piantano davanti quattro copie costruite apposta e due sorgenti
    che gli somigliano senza esserlo, e si pretende di vedere le prime e
    non le seconde. E' la stessa forma della sonda 'slashing' in
    `_schemi.verifica_riferimenti()`."""
    for etichetta, finto in SIS.COPIE_FINTE:
        trovate, _ = SIS.copie_in("finto.py", finto)
        if not trovate:
            err(f"il controllo anti-duplicazione NON vede piu' una copia "
                f"piantata apposta ({etichetta}): e' rotto, e su un "
                f"repository pulito taceva lo stesso")
    for etichetta, finto in SIS.NON_COPIE_FINTE:
        trovate, _ = SIS.copie_in("finto.py", finto)
        if trovate:
            err(f"il controllo anti-duplicazione segnala cio' che non e' una "
                f"copia ({etichetta}): {trovate[0][4]}. Un controllo che "
                f"grida al lupo viene spento")

    copie, marcite = SIS.copie_nel_codice()
    for dato_id, percorso, riga, come, testo in copie:
        dove = f"{percorso}:{riga}" if riga else percorso
        err(f"{dove}: '{dato_id}' riscritto fuori dalla sua sede "
            f"(per {come}) — {testo}")
    for m in marcite:
        err(f"eccezione dichiarata e non trovata: {m}. Un'eccezione marcita "
            f"e' un permesso che non protegge piu' niente")
    return len(copie)


# --------------------------------------------------------------------- report

def main(argv):
    verbose = "-v" in argv
    errori = []

    def err(m):
        errori.append(m)

    controlla_forma(err)
    controlla_copertura(err)
    provati = controlla_sonda(err, verbose)
    controlla_prosa(err)
    controlla_duplicazione(err)

    print(f"\n{len(SIS.DATI)} dati di sistema validati "
          f"({', '.join(sorted(SIS.DATI))}).")
    print(f"{provati} ingressi confrontati con la formula stampata dalla "
          f"fonte.")
    sorgenti = len(SIS._sorgenti())
    print(f"{sorgenti} sorgenti Python letti dal controllo "
          f"anti-duplicazione, {len(SIS.ECCEZIONI)} eccezione dichiarata.")

    if verbose:
        print("\nCosa il controllo anti-duplicazione NON vede:")
        for l in SIS.LIMITI:
            print(f"  - {l}")

    if errori:
        print(f"\n{len(errori)} DIVERGENZE:")
        for e in errori:
            print(f"  {e}")
        return 1
    print("\nNessuna divergenza: le tabelle di sistema hanno una sede sola.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
