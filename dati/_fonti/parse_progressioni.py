import re, json, sys

T = open('/tmp/w/out/totl_classi.txt').read()

# righe tipo: "4 10,000 5 Scepter Knight"  /  "16 2,250,000 9+7"  / "10 250,000 10+2 Lord Warrior"
ROW = re.compile(r"^\s*(\d{1,2})\s+([\d,\.]+)\s+(\d{1,2}(?:\s*\+\s*\d{1,2})?)\s*(.*)$")

def tabella(marker, primo_livello, ultimo=25, dopo=0):
    """Estrae le righe di progressione che seguono `marker` nel testo."""
    i = T.index(marker, dopo)
    coda = T[i:i+7000].split("\n")
    out, atteso = [], primo_livello
    for ln in coda:
        m = ROW.match(ln)
        if not m:
            continue
        lv = int(m.group(1))
        if lv != atteso:
            continue
        xp = int(m.group(2).replace(",", "").replace(".", ""))
        hd = m.group(3).replace(" ", "")
        titolo = m.group(4).strip(" *")
        titolo = re.sub(r"\s+", " ", titolo) or None
        out.append({"level": lv, "xp": xp, "hit_dice": hd, "title": titolo})
        atteso += 1
        if atteso > ultimo:
            break
    return out, i

if __name__ == "__main__":
    spec = [
        ("corona",   "Crown Knights Minimum Scores", 1),
        ("spada",    "Sword Knights Minimum Scores", 3),
        ("rosa",     "Rose Knights Minimum Scores", 4),
        ("mago",     "Wizards of High Sorcery Advancement Table", 1),
        ("sacerdote","Priest Experience Hit Dice Title", 1),
        ("normale",  "Game Information for Normals", 1),
    ]
    res = {}
    for nome, marker, first in spec:
        rows, _ = tabella(marker, first)
        res[nome] = rows
        print(f"{nome:10} righe={len(rows):3}  liv {rows[0]['level']}-{rows[-1]['level']}  "
              f"xp finale={rows[-1]['xp']:,}  hd finale={rows[-1]['hit_dice']}")
    json.dump(res, open('/tmp/w/prog.json','w'), ensure_ascii=False, indent=1)
