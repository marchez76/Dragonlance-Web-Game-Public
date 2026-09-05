#!/usr/bin/env python3
"""
RAPPORTO DIAGNOSTICO — l'equipaggiamento iniziale: due economie, un campo.

DOMANDA
    Venti classi su venti dichiarano `structural.starting_equipment.system =
    "pacchetto_fisso_5e"`. Nessun pacchetto esiste. Alcune portano accanto,
    nello stesso blocco, una formula di ricchezza iniziale in pezzi
    d'acciaio, che appartiene all'altra economia — quella in cui il
    personaggio COMPRA invece di ricevere. Il campo dichiara una strada e
    ne porta i resti di un'altra.

    Le due strade non sono equivalenti e non costano lo stesso. Questo
    rapporto misura cosa comporta ciascuna. NON SCEGLIE: la scelta e' una
    decisione, e questo e' un rapporto.

NON MODIFICA NULLA.

Uso:  python3 dati/analizza_equipaggiamento.py > dati/RAPPORTO-equipaggiamento.md
"""

import glob
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "_fonti"))
sys.path.insert(0, RADICE)

import srd51_pacchetti as SRDP      # noqa: E402
import _valuta as VAL               # noqa: E402
from decisioni import cita          # noqa: E402


def carica(sub):
    return [json.load(open(p, encoding="utf-8"))
            for p in sorted(glob.glob(os.path.join(BASE, sub, "*.json")))]


def slugify(name):
    """La stessa di `build_oggetti.py`: gli id del catalogo nascono cosi'."""
    s = name.lower().replace("'", "").replace(",", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


_NOTA_PREZZO = re.compile(r"costo\s+[\d.]+\s*mo", re.I)


def blocco(c):
    return ((c.get("mechanics_5e") or {}).get("structural") or {}
            ).get("starting_equipment") or {}


def chassis(c):
    return ((c.get("mechanics_5e") or {}).get("chassis") or {}).get("srd_class")


# ==========================================================================
# LO STATO
# ==========================================================================

def stato(classi, oggetti):
    ids = {o["id"] for o in oggetti}
    sistemi, con_ricchezza, con_vincoli, con_forzato = {}, [], [], []
    for c in classi:
        b = blocco(c)
        sistemi[b.get("system")] = sistemi.get(b.get("system"), 0) + 1
        if b.get("source_wealth"):
            con_ricchezza.append((c["id"], b["source_wealth"]))
        if b.get("constraints"):
            con_vincoli.append((c["id"], len(b["constraints"])))
        forz = (((c.get("mechanics_5e") or {}).get("structural") or {}
                 ).get("weapon_proficiencies") or {}).get("forced_equipment")
        if forz:
            con_forzato.append((c["id"], forz))
    return {
        "sistemi": sistemi,
        "ricchezza": con_ricchezza,
        "vincoli": con_vincoli,
        "forzato": con_forzato,
        "pacchetti_esistenti": sum(1 for c in classi if blocco(c).get("items")),
        "catalogo": ids,
    }


def stampa_stato(classi, oggetti, s):
    print("# L'equipaggiamento iniziale — due economie dichiarate insieme\n")
    print(f"Classi: **{len(classi)}**. Oggetti a catalogo: "
          f"**{len(oggetti)}**.\n")
    print("| misura | valore |")
    print("|---|---:|")
    for sistema, n in sorted(s["sistemi"].items()):
        print(f"| classi che dichiarano `{sistema}` | {n}/{len(classi)} |")
    print(f"| pacchetti effettivamente scritti | {s['pacchetti_esistenti']} |")
    print(f"| classi con una formula di ricchezza | "
          f"{len(s['ricchezza'])}/{len(classi)} |")
    print(f"| classi con vincoli sull'equipaggiamento | "
          f"{len(s['vincoli'])}/{len(classi)} |")
    print(f"| classi con equipaggiamento imposto dalle competenze | "
          f"{len(s['forzato'])}/{len(classi)} |")

    print(f"\nIl campo dichiara il pacchetto fisso per tutte e "
          f"{len(classi)} le classi e ne contiene zero. Accanto, nello "
          f"stesso blocco, {len(s['ricchezza'])} classi portano una formula "
          f"di ricchezza, che e' il dato dell'altra economia:\n")
    print("| classe | ricchezza dichiarata dalla fonte |")
    print("|---|---|")
    for cid, w in s["ricchezza"]:
        print(f"| `{cid}` | {w} |")
    if s["vincoli"]:
        print(f"\nE {len(s['vincoli'])} classi portano vincoli — quante "
              f"regole, non quali: il testo sta nei dati privati.\n")
        print("| classe | vincoli |")
        print("|---|---:|")
        for cid, n in s["vincoli"]:
            print(f"| `{cid}` | {n} |")


# ==========================================================================
# STRADA A — IL PACCHETTO FISSO
# ==========================================================================

def strada_pacchetto(classi, s):
    print("\n\n## Strada A — il pacchetto fisso\n")

    con, senza = [], []
    for c in classi:
        (con if chassis(c) else senza).append(c)
    telai = sorted({chassis(c) for c in con})

    print(f"**Quanti pacchetti servono.** Uno per classe, cioe' "
          f"{len(classi)}, ma non {len(classi)} da inventare: "
          f"{len(con)} classi hanno un chassis SRD e "
          f"{len(senza)} no.\n")
    print("| origine | classi | elenchi da scrivere |")
    print("|---|---:|---|")
    print(f"| l'SRD stampa gia' l'elenco del chassis | {len(con)} | "
          f"{len(telai)} elenchi, uno per telaio: "
          f"{', '.join('`' + t + '`' for t in telai)} |")
    print(f"| nessun chassis: l'elenco va composto | {len(senza)} | "
          f"{len(senza)}, uno per classe: "
          f"{', '.join('`' + c['id'] + '`' for c in senza)} |")

    coperte = {}
    for c in con:
        coperte.setdefault(chassis(c), []).append(c["id"])
    print("\n| telaio SRD | classi che ne ereditano l'elenco |")
    print("|---|---|")
    for t in telai:
        print(f"| `{t}` | {', '.join('`' + x + '`' for x in sorted(coperte[t]))} |")

    # quali pacchetti i cinque elenchi nominano
    usati = set()
    for t in telai:
        for scelta in SRDP.EQUIPAGGIAMENTO.get(t, []):
            for alt in scelta:
                for _q, voce, genere in alt:
                    if genere == SRDP.PACCHETTO:
                        usati.add(voce)
    costi = SRDP.costi()
    print(f"\n**I pacchetti nominati** dai {len(telai)} elenchi sono "
          f"**{len(usati)}** dei {len(SRDP.PACCHETTI)} che l'SRD stampa. "
          f"Sono nell'SRD: non vanno inventati, vanno trascritti.\n")
    print("| pacchetto | costo (SRD) | voci | di cui fuori dal listino SRD |")
    print("|---|---:|---:|---:|")
    voci_pacchetti = SRDP.voci_di_pacchetto()
    for p in sorted(usati):
        voci = voci_pacchetti[p]
        fuori = sum(1 for _q, _n, a in voci if not a)
        print(f"| {p} | {costi[p]:.0f} | {len(voci)} | {fuori} |")

    # cosa manca al catalogo per comporli
    servono, mancano, categorie = set(), set(), set()
    fuori_listino = set()
    for t in telai:
        for scelta in SRDP.EQUIPAGGIAMENTO.get(t, []):
            for alt in scelta:
                for _q, voce, genere in alt:
                    if genere == SRDP.CATEGORIA:
                        categorie.add(voce)
                    elif genere == SRDP.OGGETTO:
                        servono.add(voce)
    for p in sorted(usati):
        for _q, voce, a_listino in voci_pacchetti[p]:
            if a_listino:
                servono.add(voce)
            else:
                fuori_listino.add(voce)
    for voce in servono:
        if slugify(voce) not in s["catalogo"]:
            mancano.add(voce)

    print(f"\n**Cosa manca al catalogo** per scrivere quei "
          f"{len(usati)} pacchetti e i {len(telai)} elenchi: "
          f"le voci nominate sono **{len(servono)}**, e "
          f"**{len(mancano)}** non sono a catalogo.\n")
    if mancano:
        print("| voce nominata dall'SRD e assente dal catalogo |")
        print("|---|")
        for v in sorted(mancano):
            print(f"| {v} |")
    print(f"\nA queste si aggiungono **{len(fuori_listino)}** voci che l'SRD "
          f"nomina solo DENTRO la descrizione di un pacchetto e che la "
          f"tabella dell'attrezzatura non elenca affatto — non hanno prezzo "
          f"ne' peso propri, quindi non sono «mancanti dal catalogo»: sono "
          f"da decidere, oggetti o testo del pacchetto.\n")
    for v in sorted(fuori_listino):
        print(f"- {v}")
    print(f"\nE **{len(categorie)}** voci non sono oggetti ma SCELTE aperte "
          f"dentro una famiglia — non mancano dal catalogo, mancano "
          f"dall'interfaccia: sono domande da porre al giocatore.\n")
    for v in sorted(categorie):
        print(f"- {v}")

    print(f"\n**Cosa questa strada NON risolve.** I vincoli della fonte "
          f"({len(s['vincoli'])} classi) mordono sul pacchetto e non sul "
          f"tiro: il blocco lo dichiara gia'. Ma un vincolo come «non puo' "
          f"portare armature piu' pesanti di X» e' una regola sul "
          f"COMPRARE, e su un pacchetto fisso o e' gia' rispettato — e "
          f"allora non serve — o va applicato riscrivendo il pacchetto per "
          f"quella classe, che e' un pacchetto in piu' da comporre. "
          f"Le {len(s['ricchezza'])} formule di ricchezza, su questa "
          f"strada, non servono a niente e restano dato di fonte.")


# ==========================================================================
# STRADA B — IL BORSELLO
# ==========================================================================

def strada_borsello(classi, oggetti, s):
    print("\n\n## Strada B — il borsello da spendere\n")

    print(f"**L'aritmetica c'e' gia' e non e' il problema.** "
          f"{cita('cambio-acciaio-oro')} ha dato al progetto i due numeri e "
          f"le due destinazioni: il fattore di listino vale "
          f"{VAL.FATTORE_LISTINO['valore']} — {VAL.FATTORE_LISTINO['forma']} "
          f"— quindi un `cost_gp` del catalogo si legge come prezzo in "
          f"acciaio senza conversione. Il cambio del mondo "
          f"({VAL.CAMBIO_MONETE['valore']}) non entra in un listino, ed e' "
          f"gia' scritto che non ci entra.\n")

    # DOVE STA IL PREZZO, e non e' dove `_valuta.py` presume. La funzione
    # `prezzo_in_acciaio(cost_gp)` vuole un `cost_gp`; il catalogo ce l'ha
    # come CAMPO solo per armi e armature. Per l'attrezzatura il prezzo vive
    # dentro una stringa di `mechanics_5e.note` — «Peso 1.0 lb, costo 0.01
    # mo» — che nessuna funzione puo' leggere senza un'espressione regolare.
    # `build_oggetti.py` lo dichiara in un commento, quindi non e' una
    # svista nascosta; e' pero' la voce piu' pesante del conto di questa
    # strada, ed e' invisibile finche' non si prova a comprare qualcosa.
    campo, in_nota, muti = [], [], []
    for o in oggetti:
        m = o.get("mechanics_5e") or {}
        if ((m.get("weapon_5e") or {}).get("cost_gp") is not None
                or (m.get("armor_5e") or {}).get("cost_gp") is not None):
            campo.append(o["id"])
        elif any(_NOTA_PREZZO.search(n) for n in (m.get("note") or [])):
            in_nota.append(o["id"])
        else:
            muti.append(o["id"])

    print(f"**Dove sta il prezzo, e non e' dove il codice lo cerca.** "
          f"`_valuta.prezzo_in_acciaio()` prende un `cost_gp`. Nel catalogo "
          f"quel campo esiste per **{len(campo)}** oggetti su "
          f"**{len(oggetti)}** — armi e armature, che hanno una "
          f"sottosezione `weapon_5e` / `armor_5e`. Per **{len(in_nota)}** "
          f"il prezzo c'e' ma dentro una STRINGA di `mechanics_5e.note` "
          f"(«Peso X lb, costo Y mo»), che e' prosa e non un campo; per "
          f"**{len(muti)}** non c'e' affatto.\n")
    print("| dove sta il prezzo | oggetti | leggibile da `prezzo_in_acciaio()` |")
    print("|---|---:|---|")
    print(f"| campo `cost_gp` in `weapon_5e`/`armor_5e` | {len(campo)} | si' |")
    print(f"| stringa dentro `mechanics_5e.note` | {len(in_nota)} | no |")
    print(f"| nessun prezzo | {len(muti)} | no"
          + (f" ({', '.join('`' + x + '`' for x in muti)})" if muti else "")
          + " |")
    print(f"\n`build_oggetti.py` lo dichiara in un commento — «l'attrezzatura "
          f"non ha `weapon_5e`/`armor_5e`: costo e peso restano dentro "
          f"`source_srd`/`mechanics_5e.note`, lo schema non ne prevede una "
          f"sottosezione: la Fase 2 doveva coprire il combattimento, non "
          f"l'inventario» — quindi non e' una svista nascosta. E' pero' il "
          f"pezzo piu' grosso del conto di questa strada, e resta invisibile "
          f"finche' qualcuno non prova a comprare una torcia: "
          f"{cita('cambio-acciaio-oro')} ha dato l'aritmetica a un campo che "
          f"per l'attrezzatura non esiste.\n")

    indice = SRDP.indice_completo()
    adottate = {SRDP.canonico(o["name"]["en"]) for o in oggetti}
    mancanti_per_cat = {}
    for cat, voci in SRDP.INDICE_SRD.items():
        mancanti_per_cat[cat] = sorted(v for v in voci if v not in adottate)

    tot_mancanti = sum(len(v) for v in mancanti_per_cat.values())
    print(f"**Quante voci mancano al catalogo.** L'SRD stampa "
          f"**{len(indice)}** voci fra attrezzatura, munizioni e strumenti; "
          f"il catalogo ne ha adottate "
          f"**{len(indice) - tot_mancanti}** e ne mancano "
          f"**{tot_mancanti}**. Non e' una svista: "
          f"`_fonti/srd51_equipaggiamento.py` dichiara di aver preso «cio' "
          f"che serve al combattimento e all'esplorazione, non ogni voce "
          f"della tabella». Su questa strada quel confine non regge piu', "
          f"perche' un personaggio che compra puo' comprare qualunque riga "
          f"del listino.\n")
    print("| categoria SRD | voci | a catalogo | mancanti |")
    print("|---|---:|---:|---:|")
    for cat, voci in sorted(SRDP.INDICE_SRD.items()):
        m = len(mancanti_per_cat[cat])
        print(f"| {cat} | {len(voci)} | {len(voci) - m} | {m} |")
    print(f"\n(Armi e armature non compaiono qui: il catalogo le ha tutte, "
          f"{sum(1 for o in oggetti if o['categoria'] in ('arma',))} armi e "
          f"{sum(1 for o in oggetti if o['categoria'] in ('armatura', 'scudo'))} "
          f"fra armature e scudo.)\n")

    print(f"**Da dove viene la ricchezza per le altre classi.** La formula "
          f"esiste per **{len(s['ricchezza'])}** classi su {len(classi)}; "
          f"per le altre **{len(classi) - len(s['ricchezza'])}** la fonte 2e "
          f"non ne stampa una. E l'SRD 5.1 non offre un ripiego: la tabella "
          f"«Starting Wealth by Class» del PHB 2014 non e' fra le sezioni "
          f"dell'SRD (cercata su tutte e 45 il 05/09/2026). Le classi senza "
          f"formula sono:\n")
    con = {cid for cid, _ in s["ricchezza"]}
    for c in classi:
        if c["id"] not in con:
            print(f"- `{c['id']}`"
                  + (f" — telaio `{chassis(c)}`" if chassis(c) else
                     " — nessun chassis"))
    print(f"\nTre modi di chiudere questo buco, e nessuno e' gratis: "
          f"derivarla dal chassis (ma {sum(1 for c in classi if not chassis(c))} "
          f"classi non ne hanno uno), trascriverla dal PHB 2014 "
          f"({cita('edizione-phb-2014')} lo ammette come edizione di "
          f"riferimento, e il dato sarebbero venti formule di dado), o "
          f"deciderne una nostra, che e' strato editoriale e va dichiarato "
          f"tale ({cita('doppio-strato')}).")


# ==========================================================================
# IL CONFRONTO
# ==========================================================================

def confronto(classi, oggetti, s):
    print("\n\n## Le due strade, una accanto all'altra\n")
    print("| | pacchetto fisso | borsello |")
    print("|---|---|---|")
    print(f"| cosa c'e' gia' | il campo lo dichiara in "
          f"{len(classi)}/{len(classi)} classi | l'aritmetica del listino "
          f"({cita('cambio-acciaio-oro')}) |")
    print(f"| cosa manca di dato | i pacchetti (zero scritti) e le voci di "
          f"catalogo che li compongono | le voci di catalogo e la ricchezza "
          f"per {len(classi) - len(s['ricchezza'])} classi su {len(classi)} |")
    print("| cosa manca di decisione | come si compone il pacchetto delle "
          "classi senza chassis | da dove viene la ricchezza dove la fonte "
          "tace |")
    print("| cosa fa con i vincoli della fonte | li rispetta per "
          "costruzione, ma ogni vincolo e' un pacchetto in piu' | li "
          "applica come filtro sull'acquisto, una volta sola |")
    print(f"| cosa fa con le {len(s['ricchezza'])} formule di ricchezza | le "
          "ignora: restano dato di fonte non usato | le usa, ed e' l'unico "
          "posto del progetto dove servono |")
    con_campo = sum(
        1 for o in oggetti
        if (((o.get("mechanics_5e") or {}).get("weapon_5e") or {}
             ).get("cost_gp") is not None
            or ((o.get("mechanics_5e") or {}).get("armor_5e") or {}
                ).get("cost_gp") is not None))
    print(f"| serve un prezzo leggibile? | no: il pacchetto e' un elenco, "
          f"non una spesa | si', e oggi lo e' per {con_campo} oggetti su "
          f"{len(oggetti)} |")
    print("\nLe voci di catalogo mancanti sono in buona parte le STESSE "
          "per le due strade: e' la parte del lavoro che nessuna delle due "
          "evita. Cio' che le distingue davvero e' un campo — il prezzo — e "
          "una decisione: da dove viene la ricchezza dove la fonte tace.")


def main():
    classi, oggetti = carica("classi"), carica("oggetti")
    s = stato(classi, oggetti)
    stampa_stato(classi, oggetti, s)
    strada_pacchetto(classi, s)
    strada_borsello(classi, oggetti, s)
    confronto(classi, oggetti, s)


if __name__ == "__main__":
    main()
