#!/usr/bin/env python3
"""
Rigenera Testi/indice.json e ocr_queue.txt dallo stato reale del disco.

Sostituisce Estratti/indice.json, che riflette la vecchia estrazione a colonne
fuse e la cui coda OCR elenca ancora in testa manuali gia' completati.

Uso:  python3 indicizza.py
"""

import json
import os
import re
import subprocess
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
MANUALI = os.path.join(BASE, "Manuali")
TESTI = os.path.join(BASE, "Testi")
STATO = os.path.join(BASE, ".colstep_state", "stato.json")

EDIZIONE = {
    "Dragonlance": "Dragonlance (varie ed.)",
    "Core": "AD&D 2e",
    "3.0_3.5": "D&D 3.0/3.5",
}


def pagine_pdf(pdf):
    """Numero di pagine del PDF. Serve a ocrstep.py per sapere quando ha finito."""
    try:
        out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, timeout=20).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.M)
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def conta(percorso):
    if not os.path.exists(percorso):
        return 0, 0, None
    t = open(percorso, encoding="utf-8", errors="replace").read()
    pagine = len(re.findall(r"^\[\[p\.\d+\]\]", t, re.M))
    origine = "ocr" if t.startswith("[[origine: OCR]]") else "colonne"
    return len(t), pagine, origine


def main():
    stato = json.load(open(STATO, encoding="utf-8")) if os.path.exists(STATO) else {"fatti": {}}
    manuali, coda = [], []

    for cart in sorted(os.listdir(MANUALI)):
        d = os.path.join(MANUALI, cart)
        if not os.path.isdir(d):
            continue
        for nome in sorted(os.listdir(d)):
            if not nome.lower().endswith(".pdf"):
                continue
            titolo = os.path.splitext(nome)[0]
            pdf = os.path.join(d, nome)
            testo = os.path.join(TESTI, cart, titolo + ".txt")
            car, pag, origine = conta(testo)
            info = stato["fatti"].get(f"{cart}/{nome}", {})

            if origine:
                st = "pronto_ocr" if origine == "ocr" else "pronto"
            elif info.get("senza_testo"):
                st = "da_ocr"
            else:
                st = "non_lavorato"

            manuali.append({
                "file_pdf": f"Manuali/{cart}/{nome}",
                "file_testo": f"Testi/{cart}/{titolo}.txt" if origine else None,
                "titolo": titolo,
                "cartella": cart,
                "edizione": EDIZIONE.get(cart, cart),
                "mb_pdf": round(os.path.getsize(pdf) / 1048576),
                "stato": st,
                "origine_testo": origine,
                "pagine_marcate": pag,
                "caratteri_testo": car,
            })
            if st == "da_ocr":
                # ocrstep.py usa il secondo campo come NUMERO DI PAGINE per
                # sapere quando un manuale e' finito: va scritto quello, non i MB.
                coda.append((f"{cart}/{nome}", pagine_pdf(pdf),
                             round(os.path.getsize(pdf) / 1048576)))

    pronti = [m for m in manuali if m["stato"].startswith("pronto")]
    indice = {
        "progetto": "Dragonlance Web GDR Game",
        "aggiornato": date.today().isoformat(),
        "nota": ("Testi/ e' la fonte canonica: estrazione a colonne separate. "
                 "Estratti/ e' la vecchia estrazione con le colonne fuse riga per riga, "
                 "conservata solo come riferimento storico."),
        "riepilogo": {
            "manuali_totali": len(manuali),
            "manuali_pronti": len(pronti),
            "manuali_da_ocr": len(coda),
            "pagine_pronte": sum(m["pagine_marcate"] for m in pronti),
            "caratteri_totali": sum(m["caratteri_testo"] for m in pronti),
            "per_origine": {
                "colonne": sum(1 for m in pronti if m["origine_testo"] == "colonne"),
                "ocr": sum(1 for m in pronti if m["origine_testo"] == "ocr"),
            },
        },
        "manuali": manuali,
    }

    with open(os.path.join(TESTI, "indice.json"), "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # coda OCR ordinata dal piu' leggero, cosi' si svuota piu' in fretta
    with open(os.path.join(BASE, "ocr_queue.txt"), "w", encoding="utf-8") as f:
        f.write("# Scansioni senza layer di testo, da lavorare con ocrstep.py\n")
        f.write(f"# Rigenerata da indicizza.py il {date.today().isoformat()}\n")
        f.write("# Formato: <percorso>\\t<pagine>\\t<MB>. Il secondo campo e' usato\n")
        f.write("# da ocrstep.py per sapere quando un manuale e' completo.\n")
        f.write("# Ordinate dal PDF con meno pagine: la coda si accorcia prima.\n\n")
        for k, pag, mb in sorted(coda, key=lambda x: x[1]):
            f.write(f"{k}\t{pag}\t{mb}\n")

    r = indice["riepilogo"]
    print(f"Testi/indice.json — {r['manuali_pronti']}/{r['manuali_totali']} manuali pronti")
    print(f"  {r['pagine_pronte']:,} pagine, {r['caratteri_totali']:,} caratteri".replace(",", "."))
    print(f"  origine: {r['per_origine']['colonne']} a colonne, {r['per_origine']['ocr']} da OCR")
    print(f"ocr_queue.txt — {len(coda)} scansioni rimaste")


if __name__ == "__main__":
    main()
