#!/usr/bin/env python3
"""
Diagnostica pre-schema del Personaggio -> dati/RAPPORTO-personaggio.md

COSA FA
    Misura la forma del problema prima di progettare lo schema: cosa un
    personaggio deve portare, cosa i dati esistenti gia' coprono, cosa manca,
    e cosa il motore d'arena dovrebbe poter leggere a ogni turno.

COSA NON FA
    Non decide, non propone schemi, non tocca dati/. E' un rapporto.

RIDUZIONE — CLAUDE.md, punto 1 e punto 2
    Legge dati privati (razze/, classi/, divinita/, mostri/, oggetti/) ma non
    ne emette MAI testo di fonte: nessun `text_2e`, nessuna `descrizione`,
    nessuna `raw`. Escono solo conteggi, id, nomi di campo e analisi nostra.
    Per questo non esiste una variante `-completo`: non c'e' niente da
    ridurre, come per RAPPORTO-mostri.md. L'unico filtro attivo e' negativo
    ed e' verificato dal guardiano in fondo al file (`guardia_riduzione`).

NUMERI — CLAUDE.md, punto 3
    Ogni conteggio nella prosa e' interpolato dai dati. Le letture sono
    marcate con un blocco citato e datato, come in genera_contesto.py.

Uso:  python3 dati/analizza_personaggio.py
"""

import collections
import glob
import inspect
import json
import os
import re
import sys
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
OGGI = date.today().isoformat()
USCITA = os.path.join(BASE, "RAPPORTO-personaggio.md")

sys.path.insert(0, BASE)
sys.path.insert(0, RADICE)

import _srd51                      # noqa: E402
import _sfere_5e as SF             # noqa: E402
import _vocabolari as V            # noqa: E402
from decisioni import PER_NUMERO   # noqa: E402
from motore import generazione     # noqa: E402

CAR = ["str", "dex", "con", "int", "wis", "cha"]
CAR_IT = {"str": "FOR", "dex": "DES", "con": "COS",
          "int": "INT", "wis": "SAG", "cha": "CAR"}
SOFFITTO_5E = 20        # tetto di punteggio della 5e 2014
PER_ASI = 2             # punti concessi da un Ability Score Improvement


def dec(x):
    """Decimale con la virgola, come nel resto dei documenti del progetto."""
    return str(x).replace(".", ",")


def interpretativo(testo):
    """Marca un blocco come lettura, non come dato. Stessa forma di
    genera_contesto.py: chi legge distingue il dato dall'opinione."""
    righe = testo.strip().split("\n")
    return (f"> **Lettura interpretativa** — registrata il {OGGI}. "
            f"Non è derivata dai dati.\n>\n"
            + "\n".join(f"> {l}" if l else ">" for l in righe))


# ==========================================================================
# CARICAMENTO
# ==========================================================================

def carica(sub):
    return [json.load(open(p, encoding="utf-8"))
            for p in sorted(glob.glob(os.path.join(BASE, sub, "*.json")))]


def prendi(d, percorso):
    """Segue un percorso puntato. Restituisce None se manca un anello."""
    cur = d
    for p in percorso.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def copertura(voci, percorso):
    """Quante voci hanno quel campo valorizzato (non None, non vuoto)."""
    n = 0
    for v in voci:
        x = prendi(v, percorso)
        if x is None:
            continue
        if isinstance(x, (list, dict, str)) and len(x) == 0:
            continue
        n += 1
    return n


def bollino(n, tot):
    if n == tot:
        return f"**{n}/{tot}**"
    if n == 0:
        return f"**assente** (0/{tot})"
    return f"parziale **{n}/{tot}**"


# ==========================================================================
# DERIVATO
# ==========================================================================

def d_corpus():
    """Peso e conteggio dell'intero corpus: serve alla domanda 5."""
    out = {}
    tot_file = tot_byte = 0
    for sub in ("razze", "classi", "divinita", "incantesimi", "oggetti",
                "mostri", "modelli"):
        percorsi = sorted(glob.glob(os.path.join(BASE, sub, "*.json")))
        byte = sum(os.path.getsize(p) for p in percorsi)
        out[sub] = (len(percorsi), byte)
        tot_file += len(percorsi)
        tot_byte += byte
    out["_tot"] = (tot_file, tot_byte)
    out["_mb"] = dec(round(tot_byte / 1024 / 1024, 2))
    return out


def d_copertura(razze, classi, dei, incantesimi, oggetti):
    """Per ogni grandezza che serve a giocare, dove sta il dato oggi.

    La colonna `stato` non e' scritta a mano: e' misurata sondando il campo
    nelle entita' reali. E' il cuore della sezione 2 del rapporto."""
    armi = [o for o in oggetti if o["categoria"] == "arma"]
    armature = [o for o in oggetti if o["categoria"] in ("armatura", "scudo")]
    righe = [
        # (grandezza, percorso sondato, insieme, etichetta insieme)
        ("Modificatori di caratteristica", None, None, None),
        ("Aggiustamenti razziali", "mechanics_5e.ability_adjustments.values",
         razze, "razze"),
        ("Tetti di crescita", "mechanics_5e.ability_caps.caps", razze, "razze"),
        ("Vincoli di creazione", "mechanics_5e.ability_constraints.limits",
         razze, "razze"),
        ("Taglia", "mechanics_5e.size", razze, "razze"),
        ("Velocità", "mechanics_5e.speed_ft", razze, "razze"),
        ("Scurovisione", "mechanics_5e.darkvision_ft", razze, "razze"),
        ("Linguaggi", "mechanics_5e.languages", razze, "razze"),
        ("Dado vita", "mechanics_5e.hit_die", classi, "classi"),
        ("Tiri salvezza competenti", "mechanics_5e.chassis.saving_throws",
         classi, "classi"),
        ("Bonus di competenza per livello",
         "mechanics_5e.structural.attack_progression.values", classi, "classi"),
        ("Tabella dei punti esperienza",
         "mechanics_5e.structural.xp_table.system", classi, "classi"),
        ("Privilegi di classe con meccanica 5e", None, None, None),
        ("Competenze di abilità (le 18 della 5e)", None, None, None),
        ("Competenze in armi e armature", None, None, None),
        ("Pacchetto di equipaggiamento iniziale",
         "mechanics_5e.structural.starting_equipment.source_wealth",
         classi, "classi"),
        ("Slot incantesimi 5e", None, None, None),
        ("Lista incantesimi per classe", "classes", incantesimi, "incantesimi"),
        ("Filtro delle sfere per divinità", "mechanics_5e", dei, "divinità"),
        ("Danno delle armi", "mechanics_5e.weapon_5e.damage_dice", armi, "armi"),
        ("Categoria dell'arma (semplice/da guerra, mischia/distanza)",
         "mechanics_5e.weapon_5e.categoria", armi, "armi"),
        ("Gittata dell'arma", "mechanics_5e.weapon_5e.range_ft", armi, "armi"),
        ("Classe armatura dell'armatura",
         "mechanics_5e.armor_5e.ac_formula", armature, "armature e scudi"),
        ("Categoria dell'armatura (leggera/media/pesante)",
         "mechanics_5e.armor_5e.categoria", armature, "armature e scudi"),
        ("Tiro salvezza di un incantesimo", "saving_throw", incantesimi,
         "incantesimi"),
        ("Danno di un incantesimo", "damage", incantesimi, "incantesimi"),
        ("Concentrazione", "concentration", incantesimi, "incantesimi"),
    ]
    out = []
    for nome, perc, insieme, etich in righe:
        if perc is None:
            out.append((nome, None, None, None, etich))
            continue
        # concentration e' un booleano: la copertura si misura sulla presenza
        # della chiave, non sulla verita' del valore
        if perc == "concentration":
            n = sum(1 for v in insieme if "concentration" in v)
        else:
            n = copertura(insieme, perc)
        out.append((nome, perc, n, len(insieme), etich))
    return out


def d_classi(classi):
    con_chassis = [c for c in classi if prendi(c, "mechanics_5e.chassis.srd_class")]
    senza = [c for c in classi if not prendi(c, "mechanics_5e.chassis.srd_class")]
    stati = collections.Counter(
        f["conversion_status"] for c in classi
        for f in c["mechanics_5e"]["features"])
    tot_feat = sum(stati.values())
    entry = [c for c in classi if (c["mechanics_5e"].get("entry_level") or 1) > 1]
    prereq = [c for c in classi if c["mechanics_5e"].get("prerequisite_class")]
    dv_diverso = [c for c in classi
                  if c["mechanics_5e"].get("hit_die")
                  and c["mechanics_5e"]["hit_die"].lstrip("1")
                  != (c["source_2e"].get("hit_die") or "").lstrip("1")]
    ricchezza = [c for c in classi if c["source_2e"].get("starting_wealth")]
    xp_applicata = sum(
        1 for c in classi
        if prendi(c, "mechanics_5e.structural.xp_table.applied"))
    vincoli_equip = sum(
        len(prendi(c, "mechanics_5e.structural.starting_equipment.constraints")
            or []) for c in classi)
    nwp = sum(len((c["source_2e"].get("nonweapon_proficiencies") or {}).get(k) or [])
              for c in classi for k in ("bonus", "required", "recommended"))
    wp = sum(len((c["source_2e"].get("weapon_proficiencies") or {}).get(k) or [])
             for c in classi for k in ("required", "recommended"))
    return {
        "tot": len(classi), "con_chassis": con_chassis, "senza": senza,
        "stati": stati, "tot_feat": tot_feat,
        "chassis_usati": collections.Counter(
            prendi(c, "mechanics_5e.chassis.srd_class") for c in con_chassis),
        "entry": entry, "prereq": prereq, "dv_diverso": dv_diverso,
        "ricchezza": ricchezza, "xp_applicata": xp_applicata,
        "vincoli_equip": vincoli_equip, "nwp": nwp, "wp": wp,
        "srd_classi": sorted(_srd51.TABELLE),
        "srd_campi": sorted(next(iter(_srd51.TABELLE.values())).keys()),
    }


def d_tetti(razze):
    """Quanto i tetti razziali mordono contro il soffitto 5e e contro gli ASI."""
    righe = []
    n_sotto = n_dichiarati = 0
    for r in razze:
        caps = r["mechanics_5e"]["ability_caps"]["caps"]
        n_dichiarati += len(caps)
        n_sotto += sum(1 for v in caps.values() if v < SOFFITTO_5E)
        somma = sum(caps.get(c, SOFFITTO_5E) for c in CAR)
        righe.append({
            "id": r["id"], "nome": r["name"]["it"], "caps": caps,
            "somma": somma, "sottratti": SOFFITTO_5E * len(CAR) - somma,
            "dichiarati": len(caps),
        })
    righe.sort(key=lambda x: -x["sottratti"])
    asi = {k: _srd51.n_asi(k) for k in sorted(_srd51.TABELLE)}
    return {
        "righe": righe, "n_sotto": n_sotto, "n_dichiarati": n_dichiarati,
        "tot_celle": len(razze) * len(CAR),
        "asi": asi,
        "asi_max": max(asi.values()), "asi_min": min(asi.values()),
        "asi_classe_max": max(asi, key=asi.get),
        "medio": dec(round(sum(x["sottratti"] for x in righe) / len(righe), 1)),
        "parziali": [x for x in righe if x["dichiarati"] < len(CAR)],
    }


def d_barbaro(razze, classi):
    r = next(x for x in razze if x["id"] == "umano-barbaro")
    c = next(x for x in classi if x["id"] == "barbaro")
    adj = r["mechanics_5e"]["ability_adjustments"]
    editoriali = [x for x in razze
                  if prendi(x, "mechanics_5e.ability_adjustments.editorial_values")]
    return {
        "razza": r, "classe": c,
        "caps": r["mechanics_5e"]["ability_caps"]["caps"],
        "min_classe": c["source_2e"]["ability_minimums"],
        "req_razza": {k: v for k, v in r["source_2e"]["ability_requirements"].items()
                      if v.get("min") is not None or v.get("max") is not None},
        "editoriali_valori": adj.get("editorial_values") or {},
        "fonte_valori": adj.get("source_values") or {},
        "n_tratti": len(r["mechanics_5e"]["traits"]),
        "n_razze": len(razze),
        "razze_editoriali": [x["id"] for x in editoriali],
        "n_ambiguita": len(c["source_2e"].get("open_questions") or []),
    }


def d_numerazione():
    """Stato dei rimandi alle decisioni, chiesto al controllo che li verifica.

    Non riconta per conto proprio: `verifica_decisioni.py` e' la sede del
    conteggio, e un secondo conteggio qui sarebbe la stessa struttura doppia
    che la sezione 4 di questo rapporto argomenta contro."""
    import verifica_decisioni as VD

    conta = collections.Counter()
    per_numero = collections.Counter()
    file_con = set()
    for percorso in VD.file_da_leggere():
        try:
            _, esiti = VD.analizza(percorso)
        except (UnicodeDecodeError, OSError):
            continue
        if not esiti:
            continue
        file_con.add(percorso)
        for e in esiti:
            conta[e["esito"]] += 1
            per_numero[e["numero"]] += 1
    return {"per_numero": per_numero, "tot": sum(conta.values()),
            "file": len(file_con),
            "bassa": sum(v for k, v in per_numero.items() if k <= 12),
            "ok": conta["ok"], "sfasati": conta["numero-sfasato"],
            "nudi": conta["non-qualificata"], "ignoti": conta["id-ignoto"]}


def d_scelte(razze):
    """Tratti la cui conversione lascia una scelta al giocatore.

    Sono il caso puro della sezione 4: la scelta esiste, l'insieme da cui
    pescare a volte no, e il valore risolto non ha oggi nessun campo."""
    voci = []
    for r in razze:
        for t in r["mechanics_5e"]["traits"]:
            m = t.get("mechanics_5e") or ""
            if re.search(r"a scelta|scegli", m, re.I):
                voci.append((r["id"], t["name"], t.get("editorial")))
    con_editorial = sum(1 for v in voci if v[2])
    return {"voci": voci, "n": len(voci), "editoriali": con_editorial,
            "razze": sorted({v[0] for v in voci})}


def d_generazione():
    """Cosa il modulo esistente copre davvero: ricavato per introspezione."""
    funzioni = [n for n, o in inspect.getmembers(generazione, inspect.isfunction)
                if o.__module__ == generazione.__name__ and not n.startswith("_")]
    sorgente = inspect.getsource(generazione)
    return {
        "metodi": list(generazione.METODI),
        "default": generazione.METODO_DEFAULT,
        "funzioni": sorted(funzioni),
        "n_funzioni": len(funzioni),
        "righe": len(sorgente.splitlines()),
        # il modulo legge lo strato di fonte, non quello di conversione
        "legge_source_2e": sorgente.count('["source_2e"]'),
        "legge_mechanics_5e": sorgente.count('["mechanics_5e"]'),
        "decisioni_citate": sorted(
            {int(m) for m in re.findall(r"DECISIONE (\d+)", sorgente)}),
    }


def d_coerenza_strati(razze):
    """I due strati descrivono gli stessi tetti. Divergono?"""
    div_cap = div_lim = 0
    for r in razze:
        caps = r["mechanics_5e"]["ability_caps"]["caps"]
        lim = r["mechanics_5e"]["ability_constraints"]["limits"]
        req = r["source_2e"]["ability_requirements"]
        for c in CAR:
            if caps.get(c) != req[c]["max"] and not (
                    caps.get(c) is None and req[c]["max"] is None):
                div_cap += 1
            atteso = {"min": req[c]["min"], "max": req[c]["max"]}
            presente = lim.get(c)
            if presente is None:
                if atteso["min"] is not None or atteso["max"] is not None:
                    div_lim += 1
            elif presente != atteso:
                div_lim += 1
    return {"div_cap": div_cap, "div_lim": div_lim,
            "celle": len(razze) * len(CAR)}


def d_sfere_vs_catalogo(incantesimi):
    """Le stesse voci descritte in due strutture: si incrociano per NOME.

    NON RICONFRONTA: chiede l'esito a `verifica_sfere.confronta_catalogo()`,
    che dal 01/09/2026 e' la sede del confronto. Un secondo confronto scritto
    qui sarebbe una sesta struttura doppia dentro la sezione che argomenta
    contro le strutture doppie."""
    import verifica_sfere as VS

    cat = {i["name"]["en"]: i for i in incantesimi}
    div, mis = VS.confronta_catalogo(cat)
    per_tipo = collections.defaultdict(list)
    for tipo, nome, _ in div:
        per_tipo[tipo].append(nome)
    nomi_lb = {v["name"] for v in SF.LISTA_BASE}
    nomi_cl = {i["name"]["en"] for i in incantesimi if "Cleric" in i["classes"]}
    return {
        "n_lista": mis["base"], "n_cat": mis["catalogo"],
        "n_cleric": mis["marcati_cleric"],
        "assenti": per_tipo["assente-dal-catalogo"],
        "div_liv": per_tipo["livello"], "div_scuola": per_tipo["scuola"],
        "campi_confrontati": 3, "divergenze": mis["divergenze"],
        "dichiarati": mis["dichiarati"],
        "solo_catalogo": sorted(nomi_cl - nomi_lb),
        "solo_lista": sorted(nomi_lb - nomi_cl),
    }


def d_arena(mostri, oggetti, razze, classi):
    """Quanto della meccanica e' numero e quanto e' prosa."""
    prosa_mostri = sum(
        len(m["mechanics_5e"].get(k) or [])
        for m in mostri
        for k in ("actions", "traits", "reactions", "bonus_actions",
                  "legendary_actions"))
    prosa_razze = sum(len(r["mechanics_5e"]["traits"]) for r in razze)
    prosa_classi = sum(len(c["mechanics_5e"]["features"]) for c in classi)
    # Quanti di quei blocchi portano ANCHE la struttura. Finche' e' zero la
    # frase "sono prosa e non numeri" e' vera; appena non lo e' piu', dirla
    # senza questo numero e' un derivato scritto a mano che si e' sfasato.
    con_effetto = sum(
        1
        for insieme, chiavi in ((mostri, ("actions", "traits", "reactions",
                                          "bonus_actions", "legendary_actions")),
                                (razze, ("traits",)),
                                (classi, ("features", "chassis_features")))
        for d in insieme
        for k in chiavi
        for b in (d["mechanics_5e"].get(k) or [])
        if b.get("effetto"))
    numerici_mostro = ["armor_class.value", "hit_points.average",
                       "abilities", "speed.walk",
                       "challenge_rating.value", "passive_perception"]
    cop = {p: copertura([m["mechanics_5e"] for m in mostri], p)
           for p in numerici_mostro}
    ca = collections.Counter()
    prop = collections.Counter()
    for o in oggetti:
        a = prendi(o, "mechanics_5e.armor_5e.ac_formula")
        if a:
            if "Dex" in a:
                ca["con_dex"] += 1
            elif a.strip().startswith(("+", "-")):
                ca["modificatore"] += 1
            else:
                ca["numero_secco"] += 1
        for p in (prendi(o, "mechanics_5e.weapon_5e.properties") or []):
            prop[p] += 1
    con_numero = sum(1 for k in prop if re.search(r"\d", k))
    occ_numero = sum(v for k, v in prop.items() if re.search(r"\d", k))
    return {
        "prosa_mostri": prosa_mostri, "prosa_razze": prosa_razze,
        "prosa_classi": prosa_classi,
        "prosa_tot": prosa_mostri + prosa_razze + prosa_classi,
        "con_effetto": con_effetto,
        "numerici": cop, "n_mostri": len(mostri),
        "ca": ca, "prop_distinte": len(prop), "prop_con_numero": con_numero,
        "prop_occ_numero": occ_numero,
        "ruoli": collections.Counter(m.get("ruolo") for m in mostri),
        "morale": copertura([m["mechanics_5e"] for m in mostri],
                            "morale_2e.value"),
    }


def d_allowed(razze, classi):
    """allowed_classes usa etichette 2e: si agganciano alle nostre classi?"""
    etichette = collections.Counter()
    for r in razze:
        for x in (prendi(r, "mechanics_5e.allowed_classes.classes") or []):
            etichette[x] += 1
    nomi_en = {c["name"]["en"] for c in classi}
    combacia = sorted(e for e in etichette if e in nomi_en)
    non_combacia = sorted(e for e in etichette if e not in nomi_en)

    # Misura piu' debole ma piu' onesta della coincidenza esatta: quali
    # etichette non condividono NEMMENO UNA PAROLA con una nostra classe.
    # Non stabilisce una mappatura (sarebbe una decisione): dice soltanto
    # dove una mappatura non puo' esistere per somiglianza.
    def parole(t):
        return {w for w in re.findall(r"[a-z]+", t.lower())
                if w not in {"of", "the", "any"}}

    lessico = set()
    for c in classi:
        lessico |= parole(c["name"]["en"]) | parole(c["id"])
    estranee = sorted(e for e in etichette if not (parole(e) & lessico))

    irraggiungibili = sorted(c["id"] for c in classi
                             if c["name"]["en"] not in etichette)
    senza_tabella = [r["id"] for r in razze
                     if prendi(r, "mechanics_5e.allowed_classes.classes") is None]
    return {"etichette": etichette, "combacia": combacia,
            "non_combacia": non_combacia, "estranee": estranee,
            "piu_frequente": etichette.most_common(1)[0],
            "irraggiungibili": irraggiungibili, "senza_tabella": senza_tabella}


# ==========================================================================
# GUARDIA DI RIDUZIONE — CLAUDE.md, punto 1
# ==========================================================================

CHIAVI_VIETATE = ("text_2e", "descrizione", "raw", "granted_powers",
                  "abilities_text")


def guardia_riduzione(testo, razze, classi, dei, mostri, oggetti):
    """Verifica campo per campo che nessun testo di fonte sia finito nel
    rapporto pubblico. Verificato, non assunto: e' il punto 2 di CLAUDE.md
    applicato al caso in cui la riduzione e' totale."""
    trovati = []
    for insieme in (razze, classi, dei, mostri, oggetti):
        for e in insieme:
            for blocco in _tutti_i_testi(e):
                # si cerca una porzione lunga: un frammento breve puo'
                # coincidere per caso con un nome di campo
                for pezzo in re.findall(r"[^.;\n]{40,}", blocco):
                    if pezzo.strip() in testo:
                        trovati.append((e.get("id"), pezzo.strip()[:60]))
    return trovati


def _tutti_i_testi(nodo):
    if isinstance(nodo, dict):
        for k, v in nodo.items():
            if k in CHIAVI_VIETATE and isinstance(v, str):
                yield v
            else:
                yield from _tutti_i_testi(v)
    elif isinstance(nodo, list):
        for v in nodo:
            yield from _tutti_i_testi(v)


# ==========================================================================
# DOCUMENTO
# ==========================================================================

# Lo stato che evolve, elencato una volta sola: la tabella della sezione 1.3 e
# i conteggi della lettura che la segue vengono entrambi da qui, cosi' non
# possono sfasarsi (CLAUDE.md, punto 3).
MUTEVOLI = [
    ("Punti esperienza e livello", "sessione", "no"),
    ("Grado cavalleresco raggiunto", "sessione", "no (decisione 5, `cavalieri-solamnia`)"),
    ("Veste giurata", "una volta, al 3°", "no (decisione 6, `maghi-delle-torri`)"),
    ("Inventario, equipaggiato, sintonizzato", "sessione", "no"),
    ("Incantesimi preparati", "riposo lungo", "no"),
    ("Dadi vita spesi", "riposo breve", "no"),
    ("Punti ferita correnti e temporanei", "**turno**", "no"),
    ("Slot spesi per livello", "**turno**", "no"),
    ("Usi limitati dei privilegi", "**turno**", "no"),
    ("Condizioni attive", "**turno**", "no"),
    ("Concentrazione su un incantesimo", "**turno**",
     "il campo `concentration` esiste sull'incantesimo, non sul lanciatore"),
    ("Azione / azione bonus / reazione consumate", "**turno**", "no"),
    ("Posizione e ordine di iniziativa", "**turno**", "no"),
    ("Tiri salvezza contro morte", "**turno**", "no"),
]
N_TURNO = sum(1 for _, r, _ in MUTEVOLI if "turno" in r)
N_FUORI = len(MUTEVOLI) - N_TURNO
N_SENZA_CASA = sum(1 for _, _, c in MUTEVOLI if c.startswith("no"))


def tabella(intestazioni, righe, allineamenti=None):
    a = allineamenti or ["---"] * len(intestazioni)
    out = ["| " + " | ".join(intestazioni) + " |", "|" + "|".join(a) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in righe]
    return "\n".join(out)


def main():
    razze = carica("razze")
    classi = carica("classi")
    dei = carica("divinita")
    incantesimi = carica("incantesimi")
    oggetti = carica("oggetti")
    mostri = carica("mostri")

    CP = d_corpus()
    CL = d_classi(classi)
    TT = d_tetti(razze)
    BB = d_barbaro(razze, classi)
    GN = d_generazione()
    CO = d_coerenza_strati(razze)
    SV = d_sfere_vs_catalogo(incantesimi)
    AR = d_arena(mostri, oggetti, razze, classi)
    AC = d_allowed(razze, classi)
    SC = d_scelte(razze)
    NU = d_numerazione()
    COP = d_copertura(razze, classi, dei, incantesimi, oggetti)

    # ---- tabella di copertura, sezione 2
    righe_cop = []
    for nome, perc, n, tot, etich in COP:
        if perc is None:
            righe_cop.append((nome, "—", "**assente**", "nessun campo lo porta"))
        else:
            righe_cop.append((nome, f"`{perc.split('.')[-1]}`",
                              bollino(n, tot), etich))

    n_assenti = sum(1 for r in righe_cop if r[2].startswith("**assente"))
    n_piene = sum(1 for r in righe_cop if r[2].startswith("**") and "/" in r[2]
                  and not r[2].startswith("**assente"))

    doc = f"""# Lo schema Personaggio — rapporto diagnostico

*Generato da `dati/analizza_personaggio.py` il {OGGI}.*

> **Diagnostico.** Misura la forma del problema prima di progettarlo. **Non
> decide niente**: non propone uno schema, non scioglie le tre decisioni
> sospese, non tocca `dati/`. Ogni numero è derivato dai JSON; le letture sono
> marcate con un blocco citato e datato.
>
> Il corpus letto è di **{CP['_tot'][0]} file** per **{CP['_mb']} MB**:
> {CP['razze'][0]} razze, {CP['classi'][0]} classi, {CP['divinita'][0]} divinità,
> {CP['incantesimi'][0]} incantesimi, {CP['oggetti'][0]} oggetti,
> {CP['mostri'][0]} mostri, {CP['modelli'][0]} modelli.

---

## 0. Perché questo schema è diverso dagli altri

Razza, classe, divinità, mostro, oggetto e modello descrivono **cose che non
cambiano**: sono trascrizione più conversione, e la loro storia è la storia
delle nostre revisioni, non della partita. Un personaggio è la prima entità del
progetto la cui vita è **dentro** la partita.

La differenza si misura, e il numero è netto. Delle grandezze che servono a far
combattere un personaggio, {n_piene} su {len(righe_cop)} sono coperte da un
campo pieno, {len(righe_cop) - n_piene - n_assenti} da un campo compilato solo
in parte, e **{n_assenti} non hanno alcun campo in nessuno schema**
(tabella in §2). Ma la
divisione interessante non è quella: è che **nessuna delle sei entità esistenti
ha un solo campo che cambi durante una partita**. Non è una lacuna da riempire:
è che quella dimensione non è mai stata modellata, perché finora non serviva.

---

## 1. Cosa serve a un personaggio

Tre insiemi, distinti da **chi scrive il valore e quando**.

### 1.1 Scelto in creazione — scritto una volta dal giocatore

Sono le decisioni che nessun file può contenere, perché sono la risposta a un
filtro che i file lasciano aperto. La decisione 35 (`repertori-sono-filtri`) ha già dato il nome alla
cosa: *la fonte dà il filtro e non il campione*. Il personaggio è il posto
dove i filtri vengono **risolti**.

{tabella(
    ["dato", "l'insieme da cui si sceglie", "dove sta il filtro oggi"],
    [
        ("Razza", f"{len(razze)} voci", "`razze.index.json`"),
        ("Classe di partenza",
         f"{CL['tot'] - len(CL['entry'])} su {CL['tot']} "
         f"(le altre {len(CL['entry'])} hanno `entry_level` > 1)",
         "`classi/*.json` → `mechanics_5e.entry_level`"),
        ("Sei punteggi grezzi",
         f"{len(GN['metodi'])} metodi, default `{GN['default']}`",
         "`motore/generazione.py`"),
        ("Assegnazione dei punteggi",
         "libera, fissata o parziale a seconda della razza",
         "`generazione.genera()` → `assegnazione_libera`"),
        ("Aggiustamenti fissi",
         f"{len(BB['razze_editoriali'])} razza con `editorial_values` "
         f"({', '.join(BB['razze_editoriali'])}, decisione 20, `tappo-barbaro`)",
         "`razze/*.json` → `mechanics_5e.ability_adjustments`"),
        ("Scelte lasciate aperte dai tratti",
         f"{SC['n']} tratti su {len(razze)} razze ({', '.join(SC['razze'])})",
         "**nessun campo**: la scelta è descritta in prosa dentro il tratto"),
        ("Allineamento",
         f"vincolato in {sum(1 for c in classi if c['source_2e'].get('alignment_restriction'))} classi su {CL['tot']}",
         "`classi/*.json` → `source_2e.alignment_restriction` (prosa libera)"),
        ("Divinità", f"{len(dei)} voci, solo per le classi sacerdotali",
         "`divinita.index.json`"),
        ("Veste", "3 (Bianca, Rossa, Nera), giurata al 3° livello",
         "`classi/mago-veste-*.json` → `prerequisite_class`"),
        ("Epoca", "5 valori di `valid_eras`", "strato editoriale, decisione 12 (`valid-eras`)"),
        ("Competenze di abilità", "—",
         "**nessun filtro esiste**: le 18 abilità 5e non sono nei dati"),
        ("Equipaggiamento iniziale",
         f"{CL['vincoli_equip']} vincoli dichiarati su {CL['tot']} classi",
         "`mechanics_5e.structural.starting_equipment.constraints`"),
    ])}

### 1.2 Derivato — nessuno lo scrive, si ricalcola

Un valore derivato **non è stato di personaggio**: è una funzione dello stato.
Se finisce nella scheda come campo scrivibile diventa l'ennesima struttura che
descrive una cosa già descritta altrove — il difetto che questo progetto ha
già visto quattro volte.

{tabella(
    ["grandezza", "da cosa si calcola"],
    [
        ("Modificatore di caratteristica", "`(punteggio − 10) // 2`"),
        ("Bonus di competenza",
         "solo dal livello: `mechanics_5e.structural.attack_progression.values`"),
        ("Punti ferita massimi",
         "dado vita della classe × livello + mod. COS × livello"),
        ("Classe armatura",
         "`oggetti/*.json` → `armor_5e.ac_formula` + mod. DES + scudo"),
        ("Iniziativa", "mod. DES"),
        ("Tiri salvezza",
         "mod. + competenza dalle due di `mechanics_5e.chassis.saving_throws`"),
        ("CD degli incantesimi",
         "8 + competenza + mod. della caratteristica da incantatore"),
        ("Bonus di attacco", "mod. (FOR o DES) + competenza se competente"),
        ("Velocità, taglia, scurovisione",
         "`razze/*.json` → `speed_ft`, `size`, `darkvision_ft`"),
        ("Lista incantesimi accessibile",
         "classe → chassis → `incantesimi.index.json` → filtro sfere per i sacerdoti"),
        ("Carico", "somma di `weight_lb` dell'inventario, contro FOR"),
    ])}

### 1.3 Mutevole — cambia durante il gioco

Qui la scala del tempo si spacca in due da sola, e non è una scelta di
progetto: è il ritmo con cui i valori cambiano.

{tabella(["dato", "cambia ogni", "esiste in qualche file oggi?"],
         [(n, r, c) for n, r, c in MUTEVOLI])}

{interpretativo(f'''
**Cosa i dati impongono, prima di qualunque scelta di progetto.** La colonna
"cambia ogni" si divide in due gruppi senza che nessuno l'abbia deciso:
{N_TURNO} righe su {len(MUTEVOLI)} cambiano *entro un turno*, le altre
{N_FUORI} cambiano su tempi più lunghi — riposo, sessione, o una volta sola in
tutta la carriera. Non è una tassonomia elegante imposta ai dati: è quello che
si osserva elencandoli.

Il fatto che pesa di più è nell'ultima colonna: **{N_SENZA_CASA} di quelle
{len(MUTEVOLI)} righe non hanno oggi alcuna casa.** Non sono modellate male:
non sono modellate affatto. Tutte e sei le entità esistenti sono state scritte
per essere *lette*.

La conseguenza pratica è che lo schema Personaggio non può essere derivato per
analogia dagli altri cinque, come è stato fatto per oggetto (decisione 33, `schema-oggetti`) e
modello (decisione 38, `schema-modelli`). Quei due riusavano l'architettura a doppio strato
perché descrivevano, come gli altri, materiale di fonte convertito. Un
personaggio non ha una fonte da cui essere convertito: **non c'è un
`source_2e` di un personaggio**. Il doppio strato, qui, per la prima volta non
si applica — e questo va detto prima di progettare, non scoperto a metà.
''')}

---

## 2. Cosa i nostri dati non coprono

La colonna `stato` non è un giudizio: è misurata sondando il campo in ogni
entità reale.

{tabella(["grandezza", "campo", "stato", "su cosa"], righe_cop,
         ["---", "---", ":-:", "---"])}

### 2.1 I privilegi di classe

Dei **{CL['tot_feat']} fra privilegi e impedimenti** delle {CL['tot']} classi:
**{CL['stati'].get('pending', 0)}** `pending`,
**{CL['stati'].get('direct', 0)}** `direct`,
**{CL['stati'].get('source_only', 0)}** `source_only`.
La decisione 23 (`principio-del-clone`) autorizza il clone del chassis, **non** l'invenzione di
meccanica 5e per i privilegi: il numero non scende scrivendoli.

Ma il buco vero sta un livello più sotto. Il chassis è in `dati/_srd51.py`, che
contiene **{len(CL['srd_classi'])} classi SRD** ({', '.join(CL['srd_classi'])})
e di ciascuna **{len(CL['srd_campi'])} campi**: {', '.join(f'`{c}`' for c in CL['srd_campi'])}.
`features` è la **colonna Features della tabella**, cioè i *nomi* dei privilegi
livello per livello. Non c'è una riga di meccanica: nessuna descrizione di
Second Wind, nessuna tabella di slot, nessuna lista di competenze, nessuna
sottoclasse, nessun pacchetto d'equipaggiamento.

{interpretativo(f'''
"Clonato" oggi vuol dire **abbiamo registrato quali privilegi ha il Fighter**,
non **abbiamo le regole del Fighter**. È esattamente il rapporto che c'è fra un
indice e un testo, ed è stato corretto registrarlo così: `_srd51.py` dichiara
in testa di essere la colonna Features "senza riscritture".

Il punto è che il conto dei `pending` misura il lavoro sbagliato. Anche
azzerando tutti e {CL['stati'].get('pending', 0)} i pending — cioè convertendo
ogni privilegio *di Krynn* — un Cavaliere della Corona resterebbe ingiocabile,
perché gli mancherebbero i privilegi del **Fighter**, che non sono `pending`:
non sono mai stati contati.
''')}

### 2.2 Le otto classi senza chassis

**{len(CL['senza'])} classi su {CL['tot']}** non hanno chassis, per decisione:
{', '.join('`' + c['id'] + '`' for c in CL['senza'])}.
Non hanno dado vita 5e, né tiri salvezza, né progressione. Nessuna di loro può
oggi produrre un personaggio giocabile, nemmeno vuoto.
Le {len(CL['con_chassis'])} che ce l'hanno usano
{', '.join(f'{k} ×{v}' for k, v in sorted(CL['chassis_usati'].items()))}.

Su {len(CL['dv_diverso'])} classi il chassis **cambia il dado vita** rispetto
alla fonte ({', '.join(f"`{c['id']}` {c['source_2e']['hit_die']}→{c['mechanics_5e']['hit_die']}" for c in CL['dv_diverso'])}).
È corretto e voluto, ma dice una cosa che serve allo schema: sui punti ferita
**la fonte non è autoritativa, lo è il chassis**.

### 2.3 La tabella dei punti esperienza

`structural.xp_table.applied` è `false` in **{CL['tot'] - CL['xp_applicata']}
classi su {CL['tot']}** — cioè in tutte. Le progressioni 2e restano in
`source_2e` come dato storico, e **la tabella 5e che doveva sostituirle non
esiste in nessun file**. Un personaggio sale di livello e nessun dato del
progetto dice a quanti punti esperienza.

### 2.4 Le competenze

Nei dati ci sono **{CL['wp']} voci** di competenza in armi e **{CL['nwp']}** di
competenza non-d'arma, tutte in inglese e tutte dal sistema **a slot** della 2e
che l'incompatibilità 4 della decisione 23 (`principio-del-clone`) ha abolito. Del sistema che l'ha
sostituito — competenza per categoria, più le 18 abilità della 5e — nei dati
non c'è nulla: né l'elenco delle abilità, né quante ne concede una classe, né
quali. E gli oggetti non portano la categoria su cui la competenza si
appoggerebbe: `weapon_5e` non ha un campo categoria (semplice / da guerra) e
`armor_5e` non ha leggera / media / pesante.

Il caso più netto è l'Umano. La decisione 19 (`compensazione-umano`) lo compensa con tre tratti che
sono tutti **scelte**: un +1 a due caratteristiche, una competenza di abilità,
un linguaggio. Sono {SC['n']} in tutto i tratti razziali che lasciano una
scelta al giocatore ({', '.join(SC['razze'])}), e per nessuno dei tre
dell'Umano esiste oggi né l'insieme da cui pescare né il campo in cui scrivere
il risultato: la scelta vive come prosa dentro `traits[].mechanics_5e`.

### 2.5 La valuta

**{len(CL['ricchezza'])} classi su {CL['tot']}** dichiarano una ricchezza
iniziale, espressa in **pezzi d'acciaio** (`stl`). Tutti gli oggetti portano
`cost_gp`, in **pezzi d'oro**. Nessun campo, in nessuno schema, dichiara il
cambio fra le due. Oggi un personaggio non può comprare il proprio
equipaggiamento perché non esiste un'aritmetica che colleghi il suo borsello
al listino.

### 2.6 Gli incantesimi

I {len(incantesimi)} incantesimi hanno livello, scuola, classi, componenti,
tempo di lancio, gittata, durata, rituale e concentrazione — tutti
strutturati. Non hanno **nessun campo per il tiro salvezza, il danno, l'area o
il bersaglio**: quelle informazioni stanno dentro `descrizione`, in prosa
inglese dell'SRD. Il motore d'arena può dire *quali* incantesimi un personaggio
conosce, e non può risolverne nemmeno uno.

Manca inoltre **la tabella degli slot 5e**. Le uniche tabelle di slot nel
progetto sono 2e: `source_2e.spell_progression`, presente in
{copertura(classi, 'source_2e.spell_progression')} classi su {CL['tot']}.

### 2.7 I giunti che non sono agganciati

Tre legami esistono come intenzione ma non come chiave.

- **`allowed_classes` → classi.** Le razze dichiarano
  {len(AC['etichette'])} etichette distinte, prese dalla tabella
  Class/Race Combinations. **Nessuna è un id.** Solo
  **{len(AC['combacia'])}** coincidono con il `name.en` di una nostra classe
  ({', '.join(AC['combacia'])}); le altre {len(AC['non_combacia'])} vanno
  mappate a mano, e **{len(AC['estranee'])}** non condividono nemmeno una
  parola con una nostra classe ({', '.join(AC['estranee'])}).
  Fra queste c'è **l'etichetta più frequente di tutte**, `{AC['piu_frequente'][0]}`,
  concessa da {AC['piu_frequente'][1]} razze su {len(razze)}: la tabella del
  manuale elenca il roster generico della 2e, di cui il progetto ha convertito
  solo le voci proprie di Krynn. E **{len(AC['irraggiungibili'])} classi su
  {CL['tot']}** non sono nominate da nessuna etichetta.
- **classe → incantesimi.** Il catalogo elenca le classi in `classes` con i
  nomi SRD (Wizard, Cleric…), non con i nostri id. Il ponte è
  `mechanics_5e.chassis.srd_class`, che però è `null` per
  {len(CL['senza'])} classi.
- **divinità → incantesimi.** Tutte e {len(dei)} le divinità hanno
  `mechanics_5e` a **`null`**: il filtro delle sfere (decisione 24, `sfere-sacerdotali`) vive
  interamente in `dati/_sfere_5e.py`, cioè in codice, non nei dati.

{interpretativo("""
I tre giunti hanno la stessa forma e non è un caso: il legame è sempre scritto
come **etichetta leggibile**, mai come chiave. Finché i dati servivano a essere
consultati la differenza non si vedeva; un motore di creazione la incontra al
primo passo, perché "quali classi può fare un Nano delle Colline" è
letteralmente la prima domanda che deve rispondere.

Va detto con precisione che cosa manca, perché non è la stessa cosa nei tre
casi. Su `allowed_classes` non manca un campo: manca **una decisione**. Alcune
etichette denotano una nostra classe scritta in altro modo, altre nominano
classi generiche della 2e che il progetto non ha e per le quali non esiste
nulla da agganciare. Stabilire quale sia quale è lavoro di conversione, e
scriverlo qui al posto tuo sarebbe la stessa scorciatoia che la decisione 26 (`criterio-tracciabilita`)
respinge altrove: un dato non verificabile che entra perché sembra ovvio.
""")}

---

## 3. Le tre decisioni sospese

Riportate, non sciolte.

### 3.1 Il Barbaro: razza o background

**Cosa dice la fonte.** *Tales of the Lance* tratta "Barbarian" in due
capitoli: come cultura umana e come classe. Le due voci non coincidono. La
scheda razziale dichiara
{len(BB['req_razza'])} vincoli di caratteristica
({', '.join(f"{CAR_IT[k]} " + '/'.join(f'{kk} {vv}' for kk, vv in v.items() if vv is not None) for k, v in sorted(BB['req_razza'].items()))}),
la voce di classe dichiara {len(BB['min_classe'])} minimi
({', '.join(f'{CAR_IT[k]} {v}' for k, v in sorted(BB['min_classe'].items()))}).
La decisione 11 (`barbaro-vincoli`) ha applicato l'**unione** dei due set. Il manuale registra
{BB['n_ambiguita']} ambiguità dichiarata su questa classe.

**Lo stato attuale.** `umano-barbaro` è l'unica razza il cui blocco
`ability_caps` dichiara **{len(BB['caps'])} tetti su {len(CAR)}**
({', '.join(f'{CAR_IT[k]} {v}' for k, v in sorted(BB['caps'].items()))}), ed è la sola fra le {len(razze)} con aggiustamenti
puramente editoriali: {', '.join(f'{CAR_IT[k]} {v:+d}' for k, v in sorted(BB['editoriali_valori'].items()))},
con `source_values` {'vuoto' if not BB['fonte_valori'] else BB['fonte_valori']}
— cioè **nessun aggiustamento viene dalla fonte**. Porta
{BB['n_tratti']} tratti.

**Cosa resta aperto.** La decisione 20 (`tappo-barbaro`) elenca già le quattro conseguenze del
passaggio a background, e sono tutte verificabili nei dati:

{tabella(["conseguenza", "misura oggi"], [
    ("Il roster razziale scende",
     f"{BB['n_razze']} → {BB['n_razze'] - 1} voci"),
    ("Il tetto DES 16 perde la sede",
     "nessuno schema del progetto ha un contenitore `background`"),
    ("Il Monte Carlo sull'Aghar barbaro perde l'oggetto",
     "la combinazione misurata allo 0,249% è razza × classe"),
    ("I due aggiustamenti editoriali vanno rimotivati",
     f"{', '.join(f'{CAR_IT[k]} {v:+d}' for k, v in sorted(BB['editoriali_valori'].items()))}, oggi giustificati come pagamento del tetto DES 16"),
])}

Le opzioni sul tavolo restano tre: **tenere** il tappo (nessun costo, il
difetto resta), **convertire a background** (richiede uno schema che non
esiste), **tenere la razza e spostare solo i tratti**. Nessuna è preferita qui.

### 3.2 I tetti di crescita

**Cosa dicono i dati.** Su {TT['tot_celle']} caselle
({len(razze)} razze × {len(CAR)} caratteristiche),
**{TT['n_sotto']} tetti dichiarati sono sotto il soffitto {SOFFITTO_5E} della
5e**. In media una razza perde **{TT['medio']} punti** sul soffitto complessivo
di {SOFFITTO_5E * len(CAR)}.

{tabella(["razza", "somma dei tetti", "punti sottratti al soffitto 5e", "tetti dichiarati"],
         [(r["nome"], r["somma"], r["sottratti"], f"{r['dichiarati']}/{len(CAR)}")
          for r in TT["righe"]],
         ["---", "---:", "---:", ":-:"])}

Le caselle che il manuale non dichiara sono contate al soffitto {SOFFITTO_5E}:
il {BB['razza']['name']['it']} risulta quindi il meno limitato solo perché
{len(CAR) - len(BB['caps'])} dei suoi {len(CAR)} tetti **non esistono**, non
perché siano alti. È la stessa asimmetria della sezione 3.1.

**Cosa mette in tensione.** I chassis concedono da **{TT['asi_min']}** a
**{TT['asi_max']}** Ability Score Improvement ({TT['asi_classe_max']} è il più
generoso), cioè fino a **{TT['asi_max'] * PER_ASI} punti** da distribuire in
vent'anni di carriera:
{', '.join(f'{k} {v}' for k, v in sorted(TT['asi'].items()))}.
Il tetto morde di sicuro, e la decisione dice *che* morde, non *cosa succede
quando morde*.

**Cosa la fonte non dice.** In AD&D 2e i massimali erano limiti di
**generazione**: il sistema non aveva un meccanismo di aumento paragonabile
agli ASI, quindi il caso "un aumento sfonda il tetto" **non esiste nel manuale
sorgente**. Non c'è una risposta da trascrivere: è una questione che nasce
dalla conversione.

**Dove il buco è già visibile nel codice.**
`generazione.tetto_crescita()` restituisce **{SOFFITTO_5E}** quando il manuale
non dichiara un massimale — e {len(TT['parziali'])} razza
({', '.join(r['id'] for r in TT['parziali'])}) ha tetti dichiarati solo su
alcune caratteristiche. La funzione dice qual è il tetto; **nessuna funzione,
in nessun modulo, dice cosa fare del punto che lo supera.**

Le opzioni restano almeno quattro: il punto **si perde**; si **travasa** su
un'altra caratteristica; il tetto è **morbido** e la 5e vince; l'ASI diventa
un **talento** — che però oggi è impossibile, perché nel progetto non esiste
alcun catalogo di talenti.

### 3.3 La generazione delle caratteristiche

`motore/generazione.py` esiste: **{GN['righe']} righe**, **{GN['n_funzioni']}
funzioni pubbliche** ({', '.join(f'`{f}()`' for f in GN['funzioni'])}).

**Cosa copre.** I {len(GN['metodi'])} metodi
({', '.join(f'`{m}`' for m in GN['metodi'])}) con default
`{GN['default']}`; le formule razziali per singola caratteristica, comprese le
sei dell'Aghar e la Forza del Kender; gli aggiustamenti; l'unione dei vincoli
razza + classe; la validazione; la soddisfacibilità (`esiste_assegnazione`,
`metodi_praticabili`); il tetto di crescita.

**Cosa manca.**

{tabella(["buco", "cosa succede oggi"], [
    ("Nessuna funzione **assegna** i valori",
     "`esiste_assegnazione` dice *se* una disposizione legale esiste, poi la butta via"),
    ("Il point-buy non si compone con le formule razziali",
     "`genera()` solleva un'eccezione per il point-buy; il Kender ha la FOR fissata da formula e non c'è una via che le combini"),
    ("Nessun aggancio ai tetti di conversione",
     f"il modulo legge `source_2e` {GN['legge_source_2e']} volte e `mechanics_5e` {GN['legge_mechanics_5e']}: scavalca lo strato di conversione e va dritto alla fonte"),
    ("`genera()` restituisce tre forme diverse",
     "dict, lista, o dict di due chiavi, con un terzo stato `parziale`: chi chiama deve ramificare"),
    ("Copre un passo su molti",
     "punti ferita, competenze, equipaggiamento, incantesimi, denaro iniziale: nessuno di questi passa di qui"),
    ("La numerazione delle decisioni era sfasata — CHIUSA",
     f"il modulo cita ora le decisioni {', '.join(f'{x} (`' + PER_NUMERO[x].id + '`)' for x in GN['decisioni_citate'])}, verificate da `verifica_decisioni.py` — vedi §3.4"),
])}

{interpretativo(f'''
Sul terzo punto vale la pena fermarsi, perché è l'unico che sia un difetto e
non un lavoro non ancora fatto. Il modulo legge `source_2e` e non
`mechanics_5e` — e oggi non se ne accorge nessuno, perché i due strati
combaciano: il confronto campo per campo su {CO['celle']} caselle dà
**{CO['div_cap']} divergenze** sui tetti e **{CO['div_lim']}** sui vincoli di
creazione.

Combaciano perché `build_razze.py` li scrive entrambi dalla stessa fonte. È il
punto 2 di CLAUDE.md che funziona: la coerenza è tenuta dal generatore, non
dalla disciplina di chi legge. Ma vuol dire che il giorno in cui una revisione
toccherà un tetto **in `mechanics_5e`** — che è per definizione lo strato
rivedibile — il motore continuerà a leggere il valore vecchio senza segnalare
niente.
''')}

### 3.4 Una nota che riguarda tutte e tre: la numerazione — CHIUSA

Le tre questioni sospese si citano per numero, e i numeri **non erano
stabili**. Il progetto contiene **{NU['tot']} rimandi a una decisione in
{NU['file']} file**, di cui **{NU['bassa']} nella fascia 1-12** — che è
esattamente dove stavano le tre questioni di questa sezione.

Erano sfasati perché il numero è un ordinale dell'elenco, e l'elenco è
cambiato: file scritti in momenti diversi hanno continuato a citare il numero
della propria vintage, senza che nulla li riallineasse. Lette una per una, le
{NU['bassa']} citazioni della fascia bassa hanno dato questa corrispondenza —
**senza uno scarto costante**, e con lo stesso numero giusto in un file e
sbagliato in un altro:

| numero citato allora | contenuto citato | id | numero vero |
|---|---|---|:-:|
| «2» | i minimi di caratteristica sono vincoli meccanici | `vincoli-caratteristica` | **3** |
| «3» | i limiti di livello aboliti | `limiti-di-livello` | **4** |
| «4» | i limiti di livello aboliti | `limiti-di-livello` | **4** — coincideva |
| «9» | il default è 4d6 scarta il minore | `generazione-caratteristiche` | **8** |
| «10» | gli aggiustamenti negativi si tengono | `aggiustamenti-negativi` | **9** |
| «11» | i massimali valgono anche in crescita | `massimali-razziali` | **10** |
| «12» | il Barbaro tiene entrambi i set di vincoli | `barbaro-vincoli` | **11** |
| «23» | il principio del clone | `principio-del-clone` | **23** — coincideva |

**Chiusa il 2026-09-01, e non correggendo i numeri.** Correggerli sarebbe
stato il quinto giro di vigilanza su una struttura che si sfasa da sola. La
causa è che il numero di un rimando è un **derivato scritto a mano**, cioè
esattamente ciò che il punto 3 di CLAUDE.md vieta ovunque tranne che qui.

Quindi: l'elenco canonico è passato in `decisioni.py`, ogni decisione ha preso
un `id` stabile che non cambierà mai, e la forma di un rimando è ora
«decisione 10 (`massimali-razziali`)» — l'id è la chiave, il numero gli sta
accanto come derivato. `verifica_decisioni.py` verifica la coppia in tutto il
progetto e con `--correggi` riscrive i numeri a partire dagli id.

Stato oggi: **{NU['ok']} rimandi verificati, {NU['sfasati']} sfasati,
{NU['ignoti']} con id ignoto, {NU['nudi']} ancora senza id**. Rinumerare
adesso costa un comando.

---

## 4. La questione strutturale: riferimento o copia

### 4.1 Il precedente, misurato

Il progetto ha già una coppia di strutture che descrivono la stessa cosa:
`_sfere_5e.LISTA_BASE` ({SV['n_lista']} voci: nome, livello, scuola) e il
catalogo `dati/incantesimi/` ({SV['n_cat']} voci). Si incrociano **per nome
inglese**, non per id.

Confronto fatto adesso, su {SV['campi_confrontati']} campi per voce:
**{len(SV['assenti'])} voci assenti dal catalogo**,
**{len(SV['div_liv'])} divergenze di livello**,
**{len(SV['div_scuola'])} di scuola**. Le
{len(SV['solo_catalogo'])} voci marcate `Cleric` nel catalogo e non presenti in
`LISTA_BASE` sono esattamente gli incantesimi di Dominio, che il modulo
dichiara di escludere.

I due insiemi sono dunque **perfettamente allineati** — e fino al
01/09/2026 **nessuno lo verificava**: `verifica_sfere.py` leggeva
`LISTA_BASE` e `dati/divinita/`, e non apriva mai `dati/incantesimi/`.

Ora lo verifica. Il confronto sta in `verifica_sfere.confronta_catalogo()`,
è **bloccante**, e questa sezione non lo rifà: ne riporta l'esito
({SV['divergenze']} divergenze). Il quarto controllo è sull'**insieme** degli
esclusi di Dominio — {SV['dichiarati']} nomi dichiarati in
`_sfere_5e.ESCLUSI_DI_DOMINIO` — e non sul loro numero, perché un
incantesimo che entra mentre un altro esce lascerebbe il conteggio fermo.

{interpretativo('''
**L'allineamento perfetto è il dato interessante, non quello rassicurante.**
Le quattro divergenze già viste in questo progetto non sono nate da distrazione:
sono nate da strutture che combaciavano il giorno in cui sono state scritte.
Questa era la quinta di quelle strutture, e stava al giorno uno: per questo
il confronto è stato aggiunto invece di limitarsi a registrare che oggi
combaciano.

Da qui viene l'argomento sulla domanda posta, e non da una preferenza di stile.
''')}

### 4.2 Proposta: riferimento per id, con tre eccezioni nominate

**Il personaggio referenzia per id e non copia valori.** Non perché la copia
sfasi in astratto, ma per una ragione che si misura sui dati di oggi:
**{CL['stati'].get('pending', 0)} privilegi su {CL['tot_feat']} sono `pending`**
e {len(CL['senza'])} classi su {CL['tot']} non hanno chassis. Le classi
*cambieranno*, molto e presto. Un personaggio che ne avesse copiato i valori
resterebbe fermo alla versione del giorno in cui è stato creato, e — questo è
il punto — **senza saperlo**: non c'è modo di distinguere un valore copiato
apposta da uno rimasto indietro.

Il costo del riferimento, che è reale, è quello nominato nella domanda: il
personaggio dipende da file esterni. Ma il rischio non è la dipendenza — è la
dipendenza **non datata**. Tre correttivi, tutti già in uso altrove nel
progetto:

1. **Impronta del corpus.** Il personaggio registra contro quale versione dei
   dati è stato costruito. Un personaggio più vecchio di una revisione diventa
   così **rilevabile**, invece di essere reinterpretato in silenzio. È la stessa
   funzione che `pages_pdf` svolge per la trascrizione: non conserva il dato,
   conserva il modo di ritrovarlo.
2. **Si copia solo ciò che risolve un filtro.** Quando la fonte dà un insieme
   e il giocatore ne sceglie un elemento, quella scelta **non esiste in nessun
   file** e deve stare sul personaggio: l'assegnazione dei sei punteggi, il
   +1/+1 dell'umano, l'arma scelta fra "Sword (any)", le competenze. È la
   decisione 39 (`bersaglio-legale-filtro`) applicata al PG: *il bersaglio legale è un filtro*, e il
   campione si fissa alla generazione. Non è una copia dei dati — è il
   complemento dei dati.
3. **I derivati non si scrivono.** Nessun campo `ca`, `pf_max`, `bonus_attacco`
   scrivibile nella scheda: si ricalcolano. Uno stato che si può ricostruire e
   che viene invece salvato è, per definizione, una struttura in più che
   descrive una cosa già descritta.

Resta una tensione onesta da segnalare, non da risolvere qui: i punti ferita
**massimi** sono un derivato, ma se tirati a ogni livello (invece che a media
fissa) sono anche un evento irripetibile, e allora vanno salvati i *tiri*, non
il totale. Lo stesso vale per la ricchezza iniziale, se tirata.

---

## 5. Il vincolo dell'arena

### 5.1 Non è un problema di velocità

Il corpus intero è **{CP['_tot'][0]} file per {CP['_mb']} MB**. Caricato una
volta all'avvio e indicizzato per id, ci sta in memoria senza discussione: gli
indici `*.index.json` esistono già e fanno esattamente questo mestiere.
**A ogni turno non va letto nessun file.** La domanda "quanto velocemente" ha
una risposta noiosa, ed è quella giusta.

### 5.2 È un problema di forma

Il problema è che i valori che servono a ogni turno, in buona parte, **non
esistono come numeri**.

Quello che è già numero, sui {AR['n_mostri']} mostri:

{tabella(["grandezza", "copertura"],
         [(f"`{k}`", bollino(v, AR['n_mostri'])) for k, v in AR["numerici"].items()],
         ["---", ":-:"])}

Quello che è prosa: **{AR['prosa_tot']} blocchi di meccanica in tutto** —
{AR['prosa_mostri']} fra azioni, tratti e reazioni dei mostri,
{AR['prosa_razze']} tratti razziali, {AR['prosa_classi']} privilegi di classe.
Il campo si chiama `mechanics_5e` ed è una **stringa in italiano**: un'azione
di attacco è scritta nella forma *"+N a colpire, portata N piedi, un bersaglio,
N (NdN+N) danni di un certo tipo"*. Leggibile da una persona, non da un motore.

Di quei blocchi, **{AR['con_effetto']} portano ora anche un campo `effetto`**
accanto alla prosa: i privilegi del chassis Fighter e le azioni dei due mostri
della fetta verticale. Restano **{AR['prosa_tot'] - AR['con_effetto']}** in cui
tutto quello che serve c'è e nulla di quello che serve è un campo.

Anche dove il dato è strutturato, il numero è spesso **dentro** una stringa:

- `armor_5e.ac_formula` — solo {AR['ca']['numero_secco']} armature portano un
  numero secco; **{AR['ca']['con_dex']} portano una formula** da interpretare
  (`"14 + Dex modifier (max 2)"`) e {AR['ca']['modificatore']} un modificatore
  (lo scudo).
- `weapon_5e.properties` — {AR['prop_distinte']} proprietà distinte, di cui
  **{AR['prop_con_numero']} contengono un numero** annegato nel testo, per
  {AR['prop_occ_numero']} occorrenze in tutto (`"versatile (1d10)"`,
  `"ammunition (range 150/600)"`). La gittata di un'arma a distanza si può oggi
  ottenere solo con un'espressione regolare.
- Gli incantesimi non hanno campi per danno e tiro salvezza (§2.6).

### 5.3 Cosa il motore deve poter fare a ogni turno

{tabella(["operazione", "legge", "scrive", "praticabile oggi?"], [
    ("Ordine di iniziativa", "mod. DES dei partecipanti", "l'ordine", "**sì**"),
    ("Attacco con arma", "bonus attacco, CA del bersaglio, dadi di danno",
     "PF del bersaglio",
     "**no**: la CA del bersaglio c'è, il bonus d'attacco no — sul PG manca la competenza, sul mostro è dentro la prosa"),
    ("Attacco di un mostro", "il blocco `actions`", "PF del bersaglio",
     "**no**: è prosa"),
    ("Lancio di un incantesimo", "slot disponibili, CD, effetto",
     "slot spesi, PF, condizioni", "**no**: l'effetto non è strutturato"),
    ("Uso di un privilegio", "usi rimasti, effetto", "usi consumati",
     f"**no**: {CL['stati'].get('pending', 0)} privilegi su {CL['tot_feat']} sono `pending`"),
    ("Condizioni e concentrazione", "condizioni attive", "condizioni attive",
     f"**in parte**: il catalogo ne converte {len(V.condizioni_modellate())} "
     f"delle {len(V.CONDIZIONI)} che il vocabolario nomina "
     f"(decisioni 48 (`condizioni-a-consumo`) e "
     f"53 (`condizioni-vocabolario-srd`)); la concentrazione non e' "
     f"modellata da nessuna parte"),
    ("Decisione dell'IA", "ruolo e morale della creatura", "l'intenzione",
     f"**sì**: `ruolo` su {AR['n_mostri']}/{AR['n_mostri']}, `morale_2e` su {AR['morale']}/{AR['n_mostri']}"),
])}

I {len(AR['ruoli'])} ruoli già assegnati
({', '.join(f'{k} {v}' for k, v in AR['ruoli'].most_common())}) e il morale
della decisione 27 (`sette-campi-2e`) sono, oggi, la parte dell'arena messa meglio: l'IA sa cosa
vuole fare una creatura molto prima che il motore sappia risolverne l'attacco.

{interpretativo(f'''
**La scheda non è progettata male: è progettata per un altro uso.** Tutte e sei
le entità sono documenti di conversione — devono mostrare cosa dice la fonte,
cosa ne abbiamo fatto e perché. Per quello servono la prosa, la nota, lo stato
di conversione, la provenienza. Un motore di combattimento vuole l'opposto:
numeri, senza contesto.

Sono due usi legittimi degli stessi fatti, e il progetto ha già il modo di
tenerli insieme senza duplicarli: **`dati/*.index.json`**. Un indice non è una
seconda verità, è una proiezione derivata dalla prima, rigenerata dal
generatore — il punto 2 di CLAUDE.md. La domanda che lo schema Personaggio
dovrà affrontare non è quindi "riferimento o copia" soltanto, ma anche se
l'arena legga le schede o una **proiezione di combattimento** derivata da esse.

Il criterio per distinguere le due cose esiste già ed è verificabile: se un
valore può essere ricalcolato dai file, è una proiezione e va rigenerata; se
non può, è stato ed è del personaggio.

Va detto anche il rovescio, perché è il costo dell'intera sezione: finché i
{AR['prosa_tot'] - AR['con_effetto']} blocchi di meccanica restano prosa, **nessuna proiezione può
derivarli**. Trasformarli in numeri non è un lavoro di formato, è la stessa
conversione dei `pending` vista da un'altra angolazione — e riguarda anche i
{AR['prosa_mostri']} blocchi dei mostri, che oggi risultano "convertiti".
''')}

---

## In sintesi

{tabella(["domanda", "risposta breve"], [
    ("1. Cosa serve",
     f"su {len(righe_cop)} grandezze: {n_piene} coperte, "
     f"{len(righe_cop) - n_piene - n_assenti} parziali, {n_assenti} senza "
     "alcun campo; e nessuna entità esistente ha un campo che cambi in partita"),
    ("2. Cosa manca",
     f"i privilegi del chassis (non contati fra i {CL['stati'].get('pending', 0)} `pending`), "
     f"la tabella PE 5e ({CL['tot'] - CL['xp_applicata']}/{CL['tot']} non applicata), "
     "le competenze 5e, gli slot 5e, l'effetto degli incantesimi, il cambio stl/gp"),
    ("3. Le tre sospese",
     "riportate con fonte e opzioni, non sciolte"),
    ("4. Riferimento o copia",
     "riferimento per id, più impronta del corpus, più le sole scelte "
     "che risolvono un filtro; i derivati non si scrivono"),
    ("5. Arena",
     f"{CP['_mb']} MB stanno in memoria: il vincolo non è la velocità ma che "
     f"{AR['prosa_tot'] - AR['con_effetto']} blocchi di meccanica su "
     f"{AR['prosa_tot']} sono ancora solo prosa"),
])}

---

*Nessuna decisione è presa in questo documento. Le tre questioni della sezione
3 restano aperte, e lo schema non è progettato.*
"""

    fuoriuscite = guardia_riduzione(doc, razze, classi, dei, mostri, oggetti)
    if fuoriuscite:
        print("RIDUZIONE FALLITA — testo di fonte nel rapporto pubblico:")
        for ident, pezzo in fuoriuscite[:10]:
            print(f"  {ident}: {pezzo}…")
        return 1

    with open(USCITA, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"scritto {os.path.relpath(USCITA, RADICE)} "
          f"({len(doc.splitlines())} righe)")
    print(f"guardia di riduzione: nessun testo di fonte "
          f"(chiavi sorvegliate: {', '.join(CHIAVI_VIETATE)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
