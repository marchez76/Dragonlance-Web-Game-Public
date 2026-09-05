#!/usr/bin/env python3
"""
Controllo dei rimandi alle decisioni di progetto.

IL DIFETTO CHE CHIUDE
    I testi del progetto citano le decisioni per numero. Il numero e' un
    ordinale dell'elenco cronologico, e nella fascia bassa e' cambiato piu'
    volte: file scritti in momenti diversi hanno continuato a citare il
    numero della loro vintage, e **nulla li riallineava**, perche' l'elenco
    e' generato mentre le citazioni sono incorporate nei testi. Diagnosi
    misurata in `dati/RAPPORTO-personaggio.md`, sezione 3.4.

    E' la sesta struttura del progetto che si sfasa in silenzio. Le altre
    cinque sono state chiuse mettendo un controllo dove prima c'era la
    vigilanza; questa fa lo stesso.

LA FORMA CANONICA DI UN RIMANDO
        decisione 10 (`massimali-razziali`)

    Un numero, un id, sempre in quest'ordine e con l'id subito dopo. L'id
    e' la chiave e non cambia mai; **il numero e' un derivato**, e come ogni
    derivato di questo progetto non si scrive a mano ma si rigenera
    (CLAUDE.md, punto 3). Da qui in avanti rinumerare costa un comando:

        python3 verifica_decisioni.py --correggi

    Un rimando a piu' decisioni qualifica ogni numero separatamente
    («le decisioni 3 (`vincoli-caratteristica`) e 4 (`limiti-di-livello`)»).
    L'intervallo ha una forma propria, perche' scriverne gli estremi per
    esteso costerebbe quattro incisi in mezzo a una frase:

        decisioni 38-41 (da `schema-modelli` a `sconfessione-condivisa`)

    Verificata agli estremi: entrambi gli id devono stare nel registro ai
    numeri dichiarati. Un intervallo senza gli id non dice a cosa rimanda e
    vale come non qualificato.

COSA SEGNALA
    numero-sfasato   il numero non e' quello che il registro da' a quell'id.
                     E' l'errore che questo controllo esiste per prendere,
                     ed e' l'unico che `--correggi` sistema da solo.
    id-ignoto        l'id non esiste nel registro: refuso, o decisione
                     rinominata (e allora l'id andava tenuto).
    non-qualificata  un numero senza id accanto. Non e' verificabile: oggi
                     puo' essere giusto, e domani sfasarsi senza che nessuno
                     se ne accorga. E' esattamente il difetto di partenza.
    numero-orfano    un secondo numero appeso a un rimando qualificato senza
                     id proprio — «decisione 13 (`taglia`)/N». Non ha la
                     parola davanti ne' un id dietro, quindi nessuna delle
                     regole sopra lo vedrebbe: e' la forma in cui questo
                     stesso controllo si e' scoperto cieco, la prima volta
                     che e' stato eseguito su tutto il progetto.
"""

import os
import re
import sys

from decisioni import APERTE, DECISIONI, PER_ID, PER_ID_APERTA

BASE = os.path.dirname(os.path.abspath(__file__))

# Cartelle mai da leggere: repository, cache, e i 5 GB di fonti e derivati che
# non contengono rimandi e costerebbero solo tempo.
SALTA_DIR = {".git", ".git-private", "__pycache__", ".colstep_state",
             ".ocr_state", "Manuali", "Testi", "Estratti", "Musica",
             "riscontro", ".claude"}
ESTENSIONI = {".py", ".md", ".json", ".sh", ".tsv", ".txt"}

PAROLA = r"[Dd]ecision[ei]|DECISION[IE]"

# Un intervallo: due numeri e i due id agli estremi. Va cercato per primo,
# perche' il suo primo numero soddisfa anche il pattern del rimando singolo.
RE_INTERVALLO = re.compile(
    rf"(?:{PAROLA})\s+(?P<da>\d+)\s*[-–]\s*(?P<a>\d+)"
    r"(?:\s*\(\s*da\s+`(?P<id_da>[a-z0-9-]+)`\s+a\s+`(?P<id_a>[a-z0-9-]+)`\s*\))?"
)

# Un rimando singolo: la parola, il numero (con eventuale sotto-indice
# «17.3»), e subito dopo l'id fra apici inversi. Il separatore fra numero e
# id puo' essere una parentesi aperta o una virgola, perche' il rimando cade
# sia in mezzo alla prosa sia dentro un inciso gia' parentesizzato:
#     la decisione 5 (`cavalieri-solamnia`) rifiuta
#     ... non classe (decisione 6, `maghi-delle-torri`).
RE_RIMANDO = re.compile(
    rf"(?P<parola>{PAROLA})"
    r"\s+(?P<numero>\d+)(?P<sotto>\.\d+)?"
    r"(?:\s*[(,]\s*`(?P<id>[a-z0-9-]+)`\s*\)?)?"
)

# La stessa coppia numero+id senza la parola davanti: e' la forma che prende
# il secondo termine di un elenco — «le decisioni 3 (`vincoli-caratteristica`)
# e 4 (`limiti-di-livello`)». Si accetta solo se l'id e' del registro, che
# e' cio' che la distingue da una parentesi qualunque dopo un numero.
RE_SEGUITO = re.compile(r"(?<![\d.])(?P<numero>\d+)\s*\(\s*`(?P<id>[a-z0-9-]+)`\s*\)")

# Un numero appeso a un rimando gia' qualificato ma senza id proprio:
# «decisione 13 (`taglia`)/N». Non ha la parola davanti ne' l'id dietro, e
# quindi sfuggirebbe a tutte le regole precedenti.
RE_ORFANO = re.compile(r"`\)\s*[/–-]\s*(?P<numero>\d{1,2})(?![\d.]|\s*\()")

# Il rimando a una QUESTIONE APERTA. Non ha numero e non ne vuole uno: una
# questione aperta non ha un ordinale che qualcuno citi, quindi non c'e'
# nessun derivato che possa sfasarsi. Resta un solo modo di sbagliarla —
# nominare un id che non esiste — e succede in due casi: il refuso, e la
# questione che nel frattempo e' stata DECISA ed e' uscita da APERTE. Il
# secondo e' quello che conta: il rimando va riportato sulla decisione, e
# senza questo controllo resterebbe li' a indicare il nulla.
RE_APERTA = re.compile(r"question[ae]\s+apert[ae]\s*\(\s*`(?P<id>[a-z0-9-]+)`\s*\)")


def file_da_leggere():
    for base, dirs, files in os.walk(BASE):
        dirs[:] = sorted(d for d in dirs if d not in SALTA_DIR)
        for f in sorted(files):
            if os.path.splitext(f)[1] in ESTENSIONI:
                yield os.path.join(base, f)


def _e_una_data(testo, fine):
    """Il 25 di «decisione 35 (`repertori-sono-filtri`), 25/08/2026» e' una
    data, non un secondo rimando.

    Serve solo a non contare due volte lo stesso rimando quando la prosa gli
    mette accanto la data in cui e' stata presa."""
    return re.match(r"\s*\d{1,2}/\d{1,2}/\d{4}", testo[fine:]) is not None


def _giudica(numero, id_):
    if id_ is None:
        return "non-qualificata", None
    if id_ not in PER_ID:
        return "id-ignoto", None
    if PER_ID[id_].numero != numero:
        return "numero-sfasato", PER_ID[id_].numero
    return "ok", numero


def analizza(percorso):
    """I rimandi di un file, ciascuno con il suo esito.

    Un rimando e' una coppia numero+id: l'intervallo ne produce due, una alla
    volta, cosi' che `--correggi` possa riscriverne gli estremi separatamente.
    Le `voci` di ciascun rimando portano lo span del solo numero, non
    dell'intera espressione: e' l'unica cosa che la correzione tocca."""
    testo = open(percorso, encoding="utf-8").read()
    rel = os.path.relpath(percorso, BASE)
    esiti, coperti = [], set()

    def aggiungi(numero, id_, span, etichetta):
        esito, atteso = _giudica(numero, id_)
        esiti.append({"file": rel, "riga": testo.count("\n", 0, span[0]) + 1,
                      "numero": numero, "id": id_, "esito": esito,
                      "atteso": atteso, "inizio": span[0], "fine": span[1],
                      "testo": etichetta})

    for m in RE_INTERVALLO.finditer(testo):
        coperti.update(range(m.start(), m.end()))
        eti = " ".join(m.group(0).split())
        aggiungi(int(m.group("da")), m.group("id_da"), m.span("da"), eti)
        aggiungi(int(m.group("a")), m.group("id_a"), m.span("a"), eti)

    for m in RE_RIMANDO.finditer(testo):
        if m.start() in coperti or _e_una_data(testo, m.end()):
            continue
        coperti.update(range(m.start(), m.end()))
        aggiungi(int(m.group("numero")), m.group("id"), m.span("numero"),
                 " ".join(m.group(0).split()))

    for m in RE_SEGUITO.finditer(testo):
        if m.start() in coperti or m.group("id") not in PER_ID:
            continue
        aggiungi(int(m.group("numero")), m.group("id"), m.span("numero"),
                 " ".join(m.group(0).split()))

    for m in RE_ORFANO.finditer(testo):
        esiti.append({"file": rel, "riga": testo.count("\n", 0, m.start()) + 1,
                      "numero": int(m.group("numero")), "id": None,
                      "esito": "numero-orfano", "atteso": None,
                      "inizio": m.start("numero"), "fine": m.end("numero"),
                      "testo": " ".join(m.group(0).split())})

    for m in RE_APERTA.finditer(testo):
        esiti.append({"file": rel, "riga": testo.count("\n", 0, m.start()) + 1,
                      "numero": None, "id": m.group("id"),
                      "esito": "ok-aperta" if m.group("id") in PER_ID_APERTA
                               else "aperta-ignota",
                      "atteso": None,
                      "inizio": m.start("id"), "fine": m.end("id"),
                      "testo": " ".join(m.group(0).split())})

    esiti.sort(key=lambda e: e["inizio"])
    return testo, esiti


def correggi(percorso, testo, esiti):
    """Riscrive i numeri sfasati a partire dall'id. Solo quelli."""
    da_fare = [e for e in esiti if e["esito"] == "numero-sfasato"]
    if not da_fare:
        return 0
    for e in sorted(da_fare, key=lambda x: -x["inizio"]):
        testo = testo[:e["inizio"]] + str(e["atteso"]) + testo[e["fine"]:]
    open(percorso, "w", encoding="utf-8").write(testo)
    return len(da_fare)


def main():
    correzione = "--correggi" in sys.argv
    verboso = "-v" in sys.argv or "--tutti" in sys.argv

    conta = {"ok": 0, "numero-sfasato": 0, "id-ignoto": 0,
             "non-qualificata": 0, "numero-orfano": 0,
             "ok-aperta": 0, "aperta-ignota": 0}
    problemi, corretti, file_con = [], 0, set()

    for percorso in file_da_leggere():
        try:
            testo, esiti = analizza(percorso)
        except (UnicodeDecodeError, OSError):
            continue
        if not esiti:
            continue
        file_con.add(os.path.relpath(percorso, BASE))
        for e in esiti:
            conta[e["esito"]] += 1
            if e["esito"] not in ("ok", "ok-aperta"):
                problemi.append(e)
        if correzione:
            corretti += correggi(percorso, testo, esiti)

    tot = sum(conta.values())
    print(f"{tot} rimandi in {len(file_con)} file, contro le "
          f"{len(DECISIONI)} decisioni e le {len(APERTE)} questioni aperte "
          f"del registro.")
    print(f"  ok               {conta['ok']:>4}")
    print(f"  numero-sfasato   {conta['numero-sfasato']:>4}")
    print(f"  id-ignoto        {conta['id-ignoto']:>4}")
    print(f"  non-qualificata  {conta['non-qualificata']:>4}")
    print(f"  numero-orfano    {conta['numero-orfano']:>4}")
    print(f"  questioni aperte {conta['ok-aperta']:>4} "
          f"(id ignoti: {conta['aperta-ignota']})")

    if correzione:
        print(f"\ncorretti {corretti} numeri a partire dall'id.")

    mostra = [p for p in problemi if verboso or p["esito"] != "non-qualificata"]
    if mostra:
        print()
        for p in mostra[:80]:
            atteso = f" -> {p['atteso']}" if p["atteso"] else ""
            print(f"  {p['esito']:<16} {p['file']}:{p['riga']}  "
                  f"«{p['testo'].strip()}»{atteso}")
        if len(mostra) > 80:
            print(f"  ... e altri {len(mostra) - 80}")

    if conta["non-qualificata"] and not verboso:
        print(f"\n{conta['non-qualificata']} rimandi non qualificati "
              f"(-v per l'elenco): un numero senza id non e' verificabile.")

    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
