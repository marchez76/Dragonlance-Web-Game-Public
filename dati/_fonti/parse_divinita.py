#!/usr/bin/env python3
"""
Estrae i blocchi delle 21 divinita' da Testi/Dragonlance/Tales of the Lance.txt
(capitolo "Realms Above").

STRATEGIA
    Le intestazioni delle divinita' sono impaginate in modo incoerente: a volte
    su una riga, a volte su due, Chislev senza virgola, maiuscole e minuscole
    alternate nei titoli decorativi. Ancorarsi a quelle produce falsi positivi
    e voci mancanti.

    Ogni divinita' ha pero' una sezione "duties of the Priesthood" seguita da
    un blocco "Requirements:" con le sigle del formato Legends & Lore. Si
    ancora quindi ai blocchi Requirements e si attribuisce ciascuno alla
    divinita' il cui nome canonico compare piu' vicino sopra di esso.

    Il paragrafo Requirements e' spesso spezzato da un salto pagina: numero di
    pagina stampato e marcatore [[p.N]] finiscono in mezzo alla frase. Si
    lavora quindi su una copia ripulita del testo.

Produce dati/_fonti/divinita_2e.json.
"""
import json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(BASE, "Testi", "Dragonlance", "Tales of the Lance.txt")

FAMIGLIE = {
    "good":    ["Paladine", "Mishakal", "Majere", "Kiri-Jolith", "Habbakuk",
                "Branchala", "Solinari"],
    "evil":    ["Takhisis", "Sargonnas", "Morgion", "Chemosh", "Zeboim",
                "Hiddukel", "Nuitari"],
    "neutral": ["Gilean", "Sirrion", "Reorx", "Chislev", "Zivilyn", "Shinare",
                "Lunitari"],
}
NOMI = {n: f for f, l in FAMIGLIE.items() for n in l}
SIGLE = r"AB|PAL|WAL|WPN|WP|AR|SP|PW|TU"


def ricuci(s):
    s = s.replace("(cid:146)", "’").replace("(cid:147)", "“").replace("(cid:148)", "”")
    # "Crea- tion" -> "Creation", ma senza saldare i prefissi negativi
    # legittimi: "non- Evil" deve restare "non-Evil", non diventare "nonEvil".
    s = re.sub(r"\b(non|anti|semi|pre|post|self|re)-\s+(\w)", r"\1-\2", s, flags=re.I)
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    return re.sub(r"\s+", " ", s).strip()


def campo(testo, sigla):
    m = re.search(rf"\b(?:{sigla})\s+(.+?)(?=\s*;?\s*\b(?:{SIGLE})\b\s|\Z)", testo, re.S)
    if not m:
        return None
    return (ricuci(m.group(1)).rstrip(";,. ") or None)


def pulisci_testo(t):
    """Ricuce i salti pagina senza toccare le righe vuote che separano i
    paragrafi: quelle servono per delimitare il blocco Requirements.

    Un salto pagina nel testo estratto e' la sequenza
        <numero di pagina stampato>  [[p.N]]  <righe vuote>
    e va sostituita da un semplice a capo, altrimenti spezza a meta' le
    frasi che continuano sulla pagina successiva."""
    t = t.replace("(cid:146)", "’")
    t = re.sub(r"\n[ \t]*\d{1,3}[ \t]*\n\s*\[\[p\.\d+\]\][ \t]*\n[ \t]*\n?", "\n", t)
    t = re.sub(r"\n\s*\[\[p\.\d+\]\][ \t]*\n[ \t]*\n?", "\n", t)
    return t


def main():
    t = pulisci_testo(open(SRC, encoding="utf-8").read())
    sez = t[t.index("Gods of Good\n"):]

    # Il blocco Requirements non e' sempre chiuso da una riga vuota: a volte
    # la voce della divinita' successiva comincia subito sotto. Si accumulano
    # quindi le righe finche' non se ne incontra una che apre una nuova voce.
    STOP = re.compile(r"(greater|intermediate|lesser)\s+god\)|"
                      r"^(Gender|Home Plane|Description|duties of|Role-Playing)", re.I)

    # Le intestazioni vere: un nome canonico seguito entro poche decine di
    # caratteri da "(... God)". Attribuire ogni blocco Requirements al nome
    # piu' vicino sopra di esso non basta, perche' i nomi delle divinita'
    # ricorrono di continuo nel testo discorsivo: cosi' il blocco di Sirrion
    # finiva attribuito a Shinare.
    teste = []
    for nome in NOMI:
        # i titoli decorativi del manuale alternano maiuscole e minuscole
        # ("habbakuk, fisher king", "takhisis"), quindi si cerca senza
        # distinzione di caso
        for m in re.finditer(re.escape(nome), sez, re.I):
            coda = sez[m.end():m.end() + 120]
            g = re.search(r"\((greater|intermediate|lesser)\s+god\)", coda, re.I)
            if g:
                teste.append((m.start(), nome, g.group(1).lower()))
    teste.sort()

    dei, visti = [], set()
    for m in re.finditer(r"Requirements:", sez):
        righe = []
        for riga in sez[m.end():m.end() + 1600].split("\n"):
            if not riga.strip() or STOP.search(riga):
                break
            righe.append(riga)
        r = ricuci(" ".join(righe))
        if not re.search(r"\bSP\b", r) or not re.search(r"\b(PAL|WAL)\b", r):
            continue
        precedenti = [x for x in teste if x[0] < m.start()]
        if not precedenti:
            continue
        _, nome, rango = precedenti[-1]
        if nome in visti:
            continue
        visti.add(nome)

        dei.append({
            "nome": nome,
            "famiglia": NOMI[nome],
            "rango": rango,
            "allineamento_sacerdote": campo(r, "PAL"),
            "allineamento_fedeli": campo(r, "WAL"),
            "armi": campo(r, "WPN|WP"),
            "armature": campo(r, "AR"),
            "sfere": campo(r, "SP"),
            "poteri": campo(r, "PW"),
            "scacciare_non_morti": campo(r, "TU"),
            "requisiti_caratteristiche": campo(r, "AB"),
            "requisiti_grezzi": r,
        })

    ordine = [n for f in ("good", "evil", "neutral") for n in FAMIGLIE[f]]
    dei.sort(key=lambda d: ordine.index(d["nome"]))

    json.dump(dei, open(os.path.join(BASE, "dati", "_fonti", "divinita_2e.json"),
                        "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    mancano = [n for n in NOMI if n not in visti]
    print(f"{len(dei)}/21 divinita' estratte" + (f" — mancano: {mancano}" if mancano else ""))
    for d in dei:
        vuoti = [k for k in ("allineamento_sacerdote", "sfere", "armi") if not d[k]]
        print(f" {'!' if vuoti else ' '} {d['famiglia']:8} {d['rango'][:5]:5} "
              f"{d['nome'][:12]:12} {(d['sfere'] or '(nessuna)')[:56]}")
        if vuoti:
            print(f"      da controllare: {', '.join(vuoti)}")


if __name__ == "__main__":
    main()
