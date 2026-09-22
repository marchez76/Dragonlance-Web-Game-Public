#!/usr/bin/env python3
"""
Controlla che questo ambiente possa eseguire il progetto, PRIMA di scoprirlo
a meta' di un'esecuzione lunga.

COSA CONTROLLA
    1. La versione di Python, letta da pyproject.toml e non riscritta qui.
    2. Che OGNI sorgente .py compili con l'interprete in uso. E' il controllo
       che mancava: il 22/09/2026 sette file su 71 non compilavano su 3.11 —
       fra cui `motore/generazione.py`, cioe' il motore — e nessuno se n'era
       accorto perche' nessuno li aveva mai compilati tutti insieme.
    3. Le dipendenze Python dichiarate in pyproject.toml.
    4. Gli strumenti esterni attesi nel PATH. NON bloccanti: servono solo agli
       script che li usano, e l'ambiente remoto ne e' privo per costruzione.

PERCHE' NON BASTA `python3 qualcosa.py`
    Un SyntaxError in un modulo si vede solo quando QUALCUNO lo importa. I
    sette file rotti stavano in rami che le prove ordinarie non percorrevano:
    il progetto girava, e intanto non compilava. Un controllo che li compila
    tutti trasforma un guasto latente in un guasto immediato, che e' l'unica
    forma in cui si ripara.

DEVE GIRARE ANCHE DOVE IL PROGETTO NON GIRA
    Questo file e' scritto in sintassi compatibile con Python 3.6: e' l'unico
    del progetto che debba funzionare su un interprete TROPPO VECCHIO, perche'
    il suo compito e' proprio dirti che lo e'. Un controllo di versione che
    esplode per un errore di sintassi non ha controllato niente.

Uso:  python3 verifica_ambiente.py
"""

import glob
import io
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
problemi = []
avvisi = []


def versione_minima():
    """Legge requires-python da pyproject.toml. SEDE UNICA: non si riscrive."""
    testo = open(os.path.join(BASE, "pyproject.toml"), encoding="utf-8").read()
    m = re.search(r'requires-python\s*=\s*"[><=~^]*\s*(\d+)\.(\d+)', testo)
    if not m:
        problemi.append("pyproject.toml non dichiara requires-python")
        return None
    return int(m.group(1)), int(m.group(2))


def sorgenti():
    """I .py del progetto. Da git se possibile, altrimenti dal disco."""
    try:
        out = subprocess.check_output(["git", "ls-files", "*.py"], cwd=BASE)
        f = [p for p in out.decode("utf-8").split("\n") if p.strip()]
        if f:
            return sorted(f)
    except Exception:
        pass
    return sorted(os.path.relpath(p, BASE)
                  for p in glob.glob(os.path.join(BASE, "**", "*.py"),
                                     recursive=True))


def main():
    print("Ambiente: Python %d.%d.%d in %s"
          % (sys.version_info[0], sys.version_info[1], sys.version_info[2],
             sys.executable))

    # --- 1. versione ------------------------------------------------------
    minima = versione_minima()
    if minima:
        attuale = (sys.version_info[0], sys.version_info[1])
        etichetta = "%d.%d" % minima
        if attuale < minima:
            problemi.append(
                "Python %d.%d non basta: il progetto richiede >= %s.\n"
                "        Questo interprete NON puo' eseguire il progetto.\n"
                "        Se %s e' installato, chiamalo per nome: python%s"
                % (attuale[0], attuale[1], etichetta, etichetta, etichetta))
        else:
            print("  versione       ok (richiesta >= %s)" % etichetta)

    # --- 2. compilazione di ogni sorgente ---------------------------------
    # compile() in MEMORIA, non py_compile: quello scrive un .pyc, e scrivere
    # e' un modo di fallire che non ha niente a che vedere con la sintassi.
    # Primo tentativo di questo controllo: cfile=os.devnull, che ha dato 71
    # file "rotti" su 71 — tutti FileExistsError, nessuno un errore vero. Un
    # controllo che sbaglia in questa direzione e' peggio di nessun controllo:
    # segnala un guasto che non c'e' e insegna a non fidarsi dell'esito.
    rotti = []
    elenco = sorgenti()
    for rel in elenco:
        percorso = os.path.join(BASE, rel)
        try:
            f = io.open(percorso, encoding="utf-8")
            try:
                sorgente = f.read()
            finally:
                f.close()
            compile(sorgente, percorso, "exec")
        except SyntaxError as e:
            rotti.append("%s:%s  %s" % (rel, e.lineno, (e.msg or "")[:60]))
        except Exception as e:
            rotti.append("%s (%s)" % (rel, type(e).__name__))
    if rotti:
        problemi.append(
            "%d sorgenti su %d non compilano con questo interprete:\n        %s"
            % (len(rotti), len(elenco), "\n        ".join(rotti)))
    else:
        print("  sorgenti       ok (%d file compilano)" % len(elenco))

    # --- 3. dipendenze ----------------------------------------------------
    testo = open(os.path.join(BASE, "pyproject.toml"), encoding="utf-8").read()
    blocco = re.search(r"dependencies\s*=\s*\[(.*?)\]", testo, re.S)
    mancanti = []
    if blocco:
        for nome in re.findall(r'"\s*([A-Za-z0-9_.-]+)', blocco.group(1)):
            try:
                __import__(nome.replace("-", "_"))
            except ImportError:
                mancanti.append(nome)
    if mancanti:
        problemi.append(
            "dipendenze non installate: %s\n"
            "        Rimedio senza installare niente:  uv run --with %s <script>"
            % (", ".join(mancanti), " --with ".join(mancanti)))
    else:
        print("  dipendenze     ok")

    # --- 4. strumenti esterni (non bloccanti) -----------------------------
    sezione = re.search(r"\[tool\.dragonlance\.strumenti-esterni\](.*?)(\n\[|\Z)",
                        testo, re.S)
    if sezione:
        for nome, motivo in re.findall(r'^([a-z0-9_-]+)\s*=\s*"(.*)"',
                                       sezione.group(1), re.M):
            trovato = any(os.access(os.path.join(d, nome), os.X_OK)
                          for d in os.environ.get("PATH", "").split(os.pathsep) if d)
            if not trovato:
                avvisi.append("%s assente dal PATH — %s" % (nome, motivo[:90]))
        if not avvisi:
            print("  strumenti      ok")

    # --- esito ------------------------------------------------------------
    for a in avvisi:
        print("\n  AVVISO   " + a)
    for p in problemi:
        print("\n  ERRORE   " + p)
    if problemi:
        print("\n%d problema/i bloccante/i." % len(problemi))
        return 1
    print("\nAmbiente idoneo." + (" %d avviso/i." % len(avvisi) if avvisi else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
