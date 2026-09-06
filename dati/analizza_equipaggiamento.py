#!/usr/bin/env python3
"""
RAPPORTO DIAGNOSTICO — l'equipaggiamento iniziale: la strada presa e cosa resta.

COS'ERA E COS'E'
    Nella sua prima forma (05/09/2026, mattina) questo rapporto misurava DUE
    ECONOMIE dichiarate insieme: venti classi su venti dichiaravano
    `pacchetto_fisso_5e` e nessun pacchetto esisteva, mentre quattro
    portavano accanto una formula di ricchezza, che e' il dato dell'altra
    strada. Misurava cosa costasse ciascuna e non sceglieva.

    La decisione 62 (`pacchetto-fisso`) ha scelto. Questo rapporto misura
    ora cosa quella scelta ha chiuso e cosa ha lasciato aperto — comprese le
    due cose che la decisione vuole PROPOSTE e non scritte: l'elenco delle
    otto classi senza chassis e la sorte delle sette voci che l'SRD nomina
    solo dentro la descrizione di un pacchetto.

    Il conto della strada NON presa resta in fondo, e non per completezza:
    e' la misura che ha deciso, e va potuta rileggere senza fidarsi della
    memoria di chi l'ha scritta.

NON MODIFICA NULLA.

Uso:  python3 dati/analizza_equipaggiamento.py > dati/RAPPORTO-equipaggiamento.md
"""

import glob
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(BASE)
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "_fonti"))
sys.path.insert(0, RADICE)

import srd51_pacchetti as SRDP      # noqa: E402
import _valuta as VAL               # noqa: E402
import _voci_di_pacchetto as VP     # noqa: E402
from decisioni import cita, cita_aperta  # noqa: E402


# LA COLONNA «PRIMA» non e' derivabile: e' la misura di com'era il
# 05/09/2026 alle prime ore, prima che la decisione 62 (`pacchetto-fisso`)
# fosse applicata, e sta scritta nella prima versione di questo rapporto (in
# storia pubblica). Derivarla dai dati di oggi e' impossibile — i dati di
# oggi sono il dopo — e ricalcolarla per sottrazione («gli oggetti di adesso
# meno le 13 aggiunte») darebbe un numero che si sfasa alla prima voce
# aggiunta per un altro motivo. Sta qui come costante DICHIARATA, che e' la
# forma onesta di un dato storico.
PRIMA = {
    "pacchetti": 0,
    "classi_con_elenco": 0,
    "oggetti": 79,
    "con_prezzo": 50,
    "voci": 0,
}


def carica(sub):
    return [json.load(open(p, encoding="utf-8"))
            for p in sorted(glob.glob(os.path.join(BASE, sub, "*.json")))]


def blocco(c):
    return ((c.get("mechanics_5e") or {}).get("structural") or {}
            ).get("starting_equipment") or {}


def chassis(c):
    return ((c.get("mechanics_5e") or {}).get("chassis") or {}).get("srd_class")


def voci_di(c):
    for scelta in blocco(c).get("scelte") or []:
        for alternativa in scelta["alternative"]:
            for v in alternativa["voci"]:
                yield v


# ==========================================================================
# LO STATO
# ==========================================================================

def stato(classi, oggetti, pacchetti):
    def chi(c):
        return (blocco(c).get("composizione") or {}).get("chi")

    composte = [c for c in classi if chi(c) == "dal_telaio"]
    da_comporre = [c for c in classi if chi(c) == "da_comporre"]
    non_si_pone = [c for c in classi if chi(c) == "non_si_pone"]
    generi = {}
    for c in composte:
        for v in voci_di(c):
            generi[v["genere"]] = generi.get(v["genere"], 0) + 1
    senza_listino = [(p["id"], x["name_srd"], x["stato"], x["oggetto"])
                     for p in pacchetti for x in p["voci"]
                     if x["name_srd"] in VP.VOCI]
    con_prezzo = [o for o in oggetti if VAL.prezzo_di(o) is not None]
    return {
        "composte": composte,
        "da_comporre": da_comporre,
        "non_si_pone": non_si_pone,
        "generi": generi,
        "senza_listino": senza_listino,
        "con_prezzo": con_prezzo,
        "ricchezza": [c["id"] for c in classi
                      if blocco(c).get("source_wealth", {}).get("presente")],
        "vincoli": [(c["id"], blocco(c)["constraints"]["quante"])
                    for c in classi
                    if blocco(c).get("constraints", {}).get("quante")],
    }


def stampa_stato(classi, oggetti, pacchetti, s):
    print("# L'equipaggiamento iniziale — la strada presa, e cosa resta\n")
    print(f"{cita('pacchetto-fisso')} sceglie il **pacchetto fisso** contro "
          f"il borsello da spendere. Questo rapporto misura cosa quella "
          f"scelta ha chiuso e cosa resta aperto; il conto della strada non "
          f"presa e' in fondo, perche' e' la misura che ha deciso.\n")

    print("| misura | prima | ora |")
    print("|---|---:|---:|")
    print(f"| pacchetti scritti | {PRIMA['pacchetti']} | {len(pacchetti)} |")
    print(f"| classi con un elenco di equipaggiamento | "
          f"{PRIMA['classi_con_elenco']} | {len(s['composte'])}/{len(classi)} |")
    print(f"| oggetti a catalogo | {PRIMA['oggetti']} | {len(oggetti)} |")
    print(f"| oggetti con un prezzo leggibile da un campo | "
          f"{PRIMA['con_prezzo']} | {len(s['con_prezzo'])} |")
    print(f"| voci di equipaggiamento che rimandano al catalogo | "
          f"{PRIMA['voci']} | {sum(s['generi'].values())} |")

    print(f"\nLe {sum(s['generi'].values())} voci sono di tre generi, e la "
          f"distinzione dice CHI le risolve: **{s['generi'].get('oggetto', 0)}** "
          f"rimandano a `dati/oggetti/`, **{s['generi'].get('pacchetto', 0)}** "
          f"a `dati/pacchetti/`, e **{s['generi'].get('scelta', 0)}** non si "
          f"risolvono affatto — sono filtri che l'interfaccia deve porre come "
          f"domanda ({cita('repertori-sono-filtri')}).\n")


# ==========================================================================
# COSA E' STATO SCRITTO
# ==========================================================================

def scritto(classi, pacchetti, s):
    print("\n## Cosa la decisione ha chiuso\n")

    print(f"**I {len(pacchetti)} pacchetti sono trascritti, non composti.** "
          f"L'SRD ne stampa {len(SRDP.PACCHETTI)}; qui stanno quelli che i "
          f"{len(SRDP.EQUIPAGGIAMENTO)} elenchi di telaio nominano davvero. "
          f"Gli altri due non sono stati saltati per fretta: nominano voci "
          f"che il catalogo non ha, e scriverli darebbe riferimenti che non "
          f"risolvono.\n")
    print("| pacchetto | costo SRD | voci | di cui a testo |")
    print("|---|---:|---:|---:|")
    for p in pacchetti:
        aperte = sum(1 for x in p["voci"]
                     if x["stato"] == "testo_del_pacchetto")
        print(f"| {p['name']['it']} (`{p['id']}`) | {p['cost_gp']:g} | "
              f"{len(p['voci'])} | {aperte or ''} |")

    telai = {}
    for c in s["composte"]:
        telai.setdefault(blocco(c)["telaio"], []).append(c["id"])
    print(f"\n**{len(s['composte'])} classi hanno l'elenco del proprio "
          f"telaio.** Non {len(s['composte'])} elenchi: {len(telai)}, uno per "
          f"telaio, e le classi che condividono un telaio ne condividono "
          f"l'elenco — {cita('principio-del-clone')} letta sull'inventario.\n")
    print("| telaio SRD | classi | voci nell'elenco |")
    print("|---|---|---:|")
    for t, ids in sorted(telai.items()):
        n = sum(1 for _ in voci_di(next(c for c in s["composte"]
                                        if c["id"] == ids[0])))
        print(f"| `{t}` | {', '.join('`' + i + '`' for i in sorted(ids))} | "
              f"{n} |")

    print(f"\n**Il prezzo dell'attrezzatura e' un campo.** Era dentro una "
          f"frase italiana di `mechanics_5e.note` — «Peso N lb, costo N mo» "
          f"— su {PRIMA['oggetti'] - PRIMA['con_prezzo'] - 1} oggetti: due campi letti dalla fonte, cuciti in una "
          f"stringa, e i campi buttati. Ora c'e' `attrezzatura_5e`, che sta "
          f"accanto a `weapon_5e` e `armor_5e` senza duplicarli: le tre "
          f"sezioni si escludono, e `_valuta.prezzo_di()` e' l'unico posto "
          f"che sa quali sono. L'aritmetica di {cita('cambio-acciaio-oro')} "
          f"ha finalmente un campo a cui applicarsi.\n")


# ==========================================================================
# COSA RESTA APERTO
# ==========================================================================

def aperto(classi, oggetti, pacchetti, s):
    print("\n## Cosa resta aperto, e perche' non e' stato chiuso di slancio\n")

    print(f"**1. Le {len(s['da_comporre'])} classi che aspettano il "
          f"chassis.** Erano contate come "
          f"{len(s['da_comporre']) + len(s['non_si_pone'])} finche' si "
          f"guardava il solo campo `chassis`. Le altre "
          f"{len(s['non_si_pone'])} sono le Vesti, e per loro la domanda "
          f"**non si pone**: hanno `entry_level` "
          f"{sorted({(c.get('source_2e') or {}).get('entry_level') for c in s['non_si_pone']})[0]} "
          f"— {cita('maghi-delle-torri')} — quindi nessuno comincia la "
          f"carriera li' e l'equipaggiamento iniziale lo riceve la classe "
          f"con cui si parte. Non e' un'esclusione: e' un caso che non "
          f"esiste, ed e' emerso compilando il campo, non ispezionando lo "
          f"schema. {cita('composizione-cinque-classi')}.\n")
    print(f"Per le {len(s['da_comporre'])} vere, comporre l'elenco **prima** "
          f"di sapere il chassis vorrebbe dire decidere due volte la stessa "
          f"cosa: nella 5e l'elenco iniziale e' un attributo del telaio, e "
          f"sceglierlo a mano ora e' scegliere il telaio di nascosto. La "
          f"composizione si lega quindi alla questione aperta che tiene "
          f"ferma ciascuna, e la segue.\n")
    print("| classe | questione aperta | armi imposte dalla fonte | dado vita "
          "| ricchezza 2e | vincoli |")
    print("|---|---|---|---:|---|---:|")
    for c in sorted(s["da_comporre"], key=lambda x: x["id"]):
        b = blocco(c)
        forz = (((c.get("mechanics_5e") or {}).get("structural") or {}
                 ).get("weapon_proficiencies") or {}).get("forced_equipment")
        dado = (c.get("source_2e") or {}).get("hit_die")
        print(f"| `{c['id']}` | "
              f"{cita_aperta(b['composizione']['questione_aperta'])} | "
              f"{', '.join(forz) if forz else '—'} | "
              f"{dado or '—'} | "
              f"{'si\'' if b.get('source_wealth', {}).get('presente') else '—'} | "
              f"{b.get('constraints', {}).get('quante') or ''} |")

    forzate = {c["id"]: (((c.get("mechanics_5e") or {}).get("structural")
                          or {}).get("weapon_proficiencies")
                         or {}).get("forced_equipment") or []
               for c in s["da_comporre"]}
    con_armi = {k: v for k, v in forzate.items() if v}
    for cid, armi in sorted(con_armi.items()):
        print(f"\n**Il `{cid}` e' l'eccezione, e va tenuta separata.** "
              f"{', '.join(armi)} sono armi 2e senza equivalente SRD: "
              f"costano {len(armi)} voci nuove **a prescindere dal chassis**, "
              f"perche' nessun telaio 5e le porta e nessuna riga della "
              f"tabella dell'equipaggiamento le contiene. Non e' un elenco da "
              f"trascrivere e non e' un elenco da comporre — e' il primo "
              f"equipaggiamento da **convertire**, con lo stesso metodo dei "
              f"mostri — {cita('equipaggiamento-da-convertire')}: "
              f"`dati/METODO-conversione-equipaggiamento.md`.")

    a_catalogo = [x for x in s["senza_listino"] if x[2] == "a_catalogo"]
    a_testo = [x for x in s["senza_listino"] if x[2] != "a_catalogo"]
    print(f"\n**2. Le {len(VP.VOCI)} voci che esistono solo dentro un "
          f"pacchetto: CHIUSE.** Erano la domanda che "
          f"{cita('pacchetto-fisso')} aveva lasciato aperta. Non sono state "
          f"decise una per una a occhio: {cita('oggetto-se-serve-al-motore')} "
          f"da' il criterio — *un oggetto esiste se il motore deve saperne "
          f"qualcosa* — e le sette sono la sua prima applicazione. "
          f"{len(set(x[1] for x in a_catalogo))} hanno un id che risolve, "
          f"{len(set(x[1] for x in a_testo))} restano testo del pacchetto, "
          f"dove si leggono comunque: nessun conto le attraversa, ed e' "
          f"tutto cio' che cambia.\n")
    print("| voce | esito | ragione in breve |")
    print("|---|---|---|")
    for nome, v in sorted(VP.VOCI.items()):
        rif = next((x[3] for x in s["senza_listino"] if x[1] == nome), None)
        esito = {"oggetto": f"oggetto `{rif}`",
                 "equivalenza": f"risolta su `{rif}`",
                 "testo": "testo del pacchetto"}[v["esito"]]
        print(f"| {nome} | {esito} | {VP.ragione_di(nome).split('.')[0]}. |")

    tensione = VP.nominate_ma_testo()
    if tensione:
        righe = ", ".join(f"**{n}** ({len(ids)} incantesimi, di cui "
                          f"{len(VP.con_costo_o_consumo(VP.VOCI[n]['termine']))} "
                          f"con un costo)"
                          for n, ids in sorted(tensione.items()))
        print(f"\nLo scarto misurato, che il criterio non nasconde: "
              f"{righe}. La prova degli incantesimi — usata per decidere "
              f"l'incenso — presa da sola prenderebbe anche questa voce. Non "
              f"la prende perche' l'SRD dichiara che la borsa dei componenti "
              f"copre ogni componente **senza costo**, e la borsa e' gia' a "
              f"catalogo: cio' di cui il motore deve sapere e' la borsa. "
              f"`_voci_di_pacchetto.nominate_ma_testo()` lo rimisura a ogni "
              f"giro, cosi' che se un domani quella voce prendesse un costo "
              f"la decisione si rifaccia invece di essere ereditata.\n")

    senza = [n for n, x in sorted(SRDP.SCELTE.items()) if x["filtro"] is None]
    print(f"\n**3. Due dei {len(SRDP.SCELTE)} filtri non hanno campione.** Le "
          f"cinque scelte aperte sono registrate come filtri "
          f"({cita('repertori-sono-filtri')}) e tre di esse il catalogo sa "
          f"gia' risolverle, perche' sono categorie d'arma. Le altre due — "
          f"{', '.join('**' + n + '**' for n in senza)} — delimitano una "
          f"famiglia di cui il catalogo non ha ancora nessun membro.\n")
    print("| scelta | filtro | nota |")
    print("|---|---|---|")
    for nome, x in sorted(SRDP.SCELTE.items()):
        f = x["filtro"]
        reso = ("—" if f is None else
                f"`categoria={f['categoria']}`"
                + (f", `tipo={f['tipo']}`" if f["tipo"] else ""))
        print(f"| {nome} | {reso} | {x['nota']} |")

    print(f"\nDelle due, il **simbolo sacro** e' l'unica che lascia un buco "
          f"vero: il focus arcano ha un'alternativa a catalogo nella stessa "
          f"riga (la borsa dei componenti), il simbolo sacro no — Chierico e "
          f"Paladino lo ricevono senza scelta.\n")

    print(f"**4. Come mordono i vincoli della fonte.** {len(s['vincoli'])} "
          f"classi ne portano; su un pacchetto fisso un vincolo o e' gia' "
          f"rispettato — e allora non serve — o chiede un pacchetto "
          f"riscritto per quella classe. Quale dei due, non e' deciso: il "
          f"campo dichiara `applied: false` e rimanda alla sede in "
          f"`source_2e`, invece di ricopiare qui la prosa della fonte.\n")
    print("| classe | vincoli |")
    print("|---|---:|")
    for cid, n in s["vincoli"]:
        print(f"| `{cid}` | {n} |")


# ==========================================================================
# LA STRADA NON PRESA — la misura che ha deciso
# ==========================================================================

def non_presa(classi, oggetti, s):
    print("\n\n## La strada non presa, e quanto sarebbe costata\n")
    print(f"Il borsello da spendere: il personaggio riceve una somma e "
          f"compra. {cita('pacchetto-fisso')} l'ha scartata per tre ragioni, "
          f"e sono tutte e tre numeri.\n")

    print(f"**Il dato dichiarava gia' l'altra strada.** "
          f"{len(classi)}/{len(classi)} classi portano "
          f"`system: \"pacchetto_fisso_5e\"`; la formula di ricchezza esiste "
          f"per **{len(s['ricchezza'])}** su {len(classi)} "
          f"({', '.join('`' + c + '`' for c in s['ricchezza'])}), e per le "
          f"altre **{len(classi) - len(s['ricchezza'])}** la fonte 2e tace. "
          f"L'SRD non offre ripiego: «Starting Wealth by Class» non e' fra "
          f"le sue 45 sezioni (cercata il 05/09/2026).\n")

    indice = SRDP.indice_completo()
    adottate = {SRDP.canonico(o["name"]["en"]) for o in oggetti}
    mancanti = {cat: sorted(v for v in voci if v not in adottate)
                for cat, voci in SRDP.INDICE_SRD.items()}
    tot = sum(len(v) for v in mancanti.values())
    print(f"**Il perimetro del catalogo.** Col pacchetto sono servite "
          f"**{len(oggetti) - PRIMA['oggetti']}** voci nuove, contate e non "
          f"stimate. Col borsello ne sarebbero "
          f"servite **{tot}**: chi compra puo' comprare qualunque riga, "
          f"quindi il confine dichiarato da `_fonti/srd51_equipaggiamento.py` "
          f"— «cio' che serve al combattimento e all'esplorazione, non ogni "
          f"voce della tabella» — non avrebbe retto piu'.\n")
    print("| categoria SRD | voci | a catalogo | mancanti |")
    print("|---|---:|---:|---:|")
    for cat, voci in sorted(SRDP.INDICE_SRD.items()):
        m = len(mancanti[cat])
        print(f"| {cat} | {len(voci)} | {len(voci) - m} | {m} |")
    print(f"\n(Armi e armature non compaiono qui: il catalogo le ha tutte, "
          f"{sum(1 for o in oggetti if o['categoria'] == 'arma')} armi e "
          f"{sum(1 for o in oggetti if o['categoria'] in ('armatura', 'scudo'))} "
          f"fra armature e scudo.)\n")

    print(f"**Il verbo.** Il pacchetto si TRASCRIVE — {len(SRDP.PACCHETTI)} "
          f"pacchetti e {len(SRDP.EQUIPAGGIAMENTO)} elenchi stanno "
          f"nell'SRD — mentre il borsello va COMPOSTO: dove la fonte tace, "
          f"la ricchezza va decisa, e sarebbero state "
          f"{len(classi) - len(s['ricchezza'])} decisioni editoriali da "
          f"dichiarare tali ({cita('doppio-strato')}).\n")

    print(f"**Cio' che il borsello aveva dalla sua** era l'aritmetica: "
          f"{cita('cambio-acciaio-oro')} fissa il fattore di listino a "
          f"{VAL.FATTORE_LISTINO['valore']} — {VAL.FATTORE_LISTINO['forma']} "
          f"— quindi un `cost_gp` si legge come prezzo in acciaio senza "
          f"conversione. Quel campo mancava all'attrezzatura, ed e' stato "
          f"scritto lo stesso: e' il pezzo di quella strada che serviva "
          f"anche a questa, e l'unico.")


def main():
    classi = carica("classi")
    oggetti = carica("oggetti")
    pacchetti = carica("pacchetti")
    s = stato(classi, oggetti, pacchetti)
    stampa_stato(classi, oggetti, pacchetti, s)
    scritto(classi, pacchetti, s)
    aperto(classi, oggetti, pacchetti, s)
    non_presa(classi, oggetti, s)


if __name__ == "__main__":
    main()
