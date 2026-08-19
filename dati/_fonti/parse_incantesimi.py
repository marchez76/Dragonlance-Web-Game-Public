import re, json
T = open('/tmp/w/out/totl_classi.txt').read()

def spell_table(marker, primo, ultimo, n_liv, salta_header=1):
    i = T.index(marker)
    righe = T[i:i+4500].split("\n")
    # salta la riga d'intestazione "Level 1 2 3 4 5 6 7 ..."
    start = 0
    for k, ln in enumerate(righe):
        if re.search(r"(?i)\b(level|priest level|knight level)\b", ln) and re.search(r"\b1\s+2\s+3\b", ln):
            start = k + 1
            break
    out, atteso = {}, primo
    for ln in righe[start:]:
        toks = [t.rstrip("*") for t in ln.split()]
        if not toks or not toks[0].isdigit(): continue
        if toks == [str(x) for x in range(1, n_liv+1)]: continue  # riga di intestazione delle colonne
        lv = int(toks[0])
        if lv != atteso: continue
        vals = []
        for t in toks[1:]:
            if t in ("-", "—", "–"): vals.append(0)
            elif t.isdigit(): vals.append(int(t))
            else: break
        if not vals: continue
        out[lv] = (vals + [0]*n_liv)[:n_liv]
        atteso += 1
        if atteso > ultimo: break
    return out

w = spell_table("Wizard of High Sorcery Spell Progression", 1, 25, 9)
p = spell_table("Holy Orders Spell Progression", 1, 25, 7)
s = spell_table("Sword Knight Spells Table", 6, 18, 7)
for n,t in (("mago",w),("sacerdote",p),("cav-spada",s)):
    print(f"{n:10} livelli {min(t)}-{max(t)} ({len(t)} righe)")
    for lv in sorted(t)[:2]: print("   ",lv,t[lv])
    print("   ",max(t),t[max(t)])
json.dump({"mago":w,"sacerdote":p,"cavaliere-spada":s}, open('/tmp/w/spell.json','w'), indent=1)
