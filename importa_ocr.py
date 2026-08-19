#!/usr/bin/env python3
"""
Porta in Testi/ i manuali recuperati con OCR.

Le scansioni pure non hanno layer di testo: colstep.py le salta e restano
alla pipeline OCR (ocrstep.py). Quelle gia' recuperate hanno pero' il testo
in Estratti/, in ordine di lettura corretto — l'OCR lavora sull'immagine
renderizzata, quindi non soffre del problema delle colonne fuse.

Questo script le copia in Testi/ con un'intestazione che ne dichiara l'origine,
cosi' Testi/ diventa l'unica cartella da consultare.

Uso:  python3 importa_ocr.py [--prova]
"""

import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
STATO = os.path.join(BASE, ".colstep_state", "stato.json")

# Vocabolario minimo per stimare quanto un testo somigli all'inglese.
# Serve a smascherare i layer di testo corrotti: alcuni PDF hanno una font map
# rotta e pdftotext ne ricava testo cifrato ("]SYV GLEVEGXIV" invece di
# "YOUR CHARACTER"). Il layer esiste, quindi ha_layer_testo lo accetta, ma il
# contenuto e' inservibile: la versione OCR in Estratti/ e' molto migliore.
COMUNI = set("""the of and to a in is it that for on with as was be by are this from or an at not have has
had they you all can will one would there their which we but his her its our more when who been into if
character level spell damage attack armor class creature magic dungeon master player rules table
""".split())

SOGLIA_SCARSA = 15.0    # sotto questa percentuale il testo e' sospetto
SCARTO_MINIMO = 5.0     # quanto deve essere migliore l'OCR per preferirlo

INTESTAZIONE = (
    "[[origine: OCR]]\n"
    "# Testo ricavato via OCR dall'immagine renderizzata, non dal layer di testo\n"
    "# del PDF (che manca). Non ha il problema delle colonne fuse, ma puo'\n"
    "# contenere errori di riconoscimento tipici dell'OCR su stampe d'epoca.\n"
    "# I marcatori di pagina [[p.N]] non sono disponibili per questi file.\n\n"
)


def qualita(percorso):
    """Percentuale di parole inglesi comuni. Testo buono: 25-35%. Sotto il 10%
    il layer di testo e' quasi certamente corrotto."""
    if not os.path.exists(percorso):
        return None
    t = open(percorso, encoding="utf-8", errors="replace").read()
    parole = re.findall(r"[a-z']{2,}", t.lower())
    if not parole:
        return 0.0
    return 100.0 * sum(1 for w in parole if w in COMUNI) / len(parole)


def preferisci_ocr(prova=False):
    """Sostituisce i testi estratti illeggibili con la loro versione OCR.

    Alcuni PDF hanno un layer di testo presente ma corrotto: l'estrazione
    riesce e produce un file, che pero' e' spazzatura. Se in Estratti/ esiste
    una versione OCR nettamente migliore, quella vince."""
    sostituiti = []
    for cart in ("Dragonlance", "Core", "3.0_3.5"):
        d = os.path.join(BASE, "Testi", cart)
        if not os.path.isdir(d):
            continue
        for nome in sorted(os.listdir(d)):
            if not nome.endswith(".txt"):
                continue
            nuovo = os.path.join(d, nome)
            vecchio = os.path.join(BASE, "Estratti", cart, nome)
            if open(nuovo, encoding="utf-8", errors="replace").read(20).startswith("[[origine"):
                continue
            qn, qv = qualita(nuovo), qualita(vecchio)
            if qv is None or qn is None:
                continue
            if qn < SOGLIA_SCARSA and qv > qn + SCARTO_MINIMO:
                if not prova:
                    with open(vecchio, encoding="utf-8", errors="replace") as a, \
                         open(nuovo, "w", encoding="utf-8") as b:
                        b.write(INTESTAZIONE)
                        b.write(a.read())
                sostituiti.append((f"{cart}/{nome[:-4]}", qn, qv))
    return sostituiti


def main():
    prova = "--prova" in sys.argv
    if not os.path.exists(STATO):
        print("nessuno stato: esegui prima colstep.py")
        return 1

    stato = json.load(open(STATO, encoding="utf-8"))
    scans = [k for k, v in stato["fatti"].items() if v.get("senza_testo")]

    copiati, mancanti = [], []
    for chiave in sorted(scans):
        cart = os.path.dirname(chiave)
        nome = os.path.splitext(os.path.basename(chiave))[0]
        sorgente = os.path.join(BASE, "Estratti", cart, nome + ".txt")
        destino = os.path.join(BASE, "Testi", cart, nome + ".txt")

        if not os.path.exists(sorgente) or os.path.getsize(sorgente) < 2000:
            mancanti.append(f"{cart}/{nome}")
            continue
        if os.path.exists(destino):
            continue
        if not prova:
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            with open(sorgente, encoding="utf-8", errors="replace") as a, \
                 open(destino, "w", encoding="utf-8") as b:
                b.write(INTESTAZIONE)
                b.write(a.read())
        copiati.append(f"{cart}/{nome}")

    print(f"{len(copiati)} manuali OCR importati in Testi/ (scansioni senza layer di testo)")
    for c in copiati:
        print("   ✓", c)

    sost = preferisci_ocr(prova)
    print(f"\n{len(sost)} testi illeggibili sostituiti con la versione OCR:")
    for n, qn, qv in sost:
        print(f"   ✓ {n[:46]:46} {qn:4.1f}% -> {qv:4.1f}% di parole inglesi")

    print(f"\n{len(mancanti)} scansioni ancora senza testo, da passare a ocrstep.py:")
    for m in mancanti:
        print("   …", m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
