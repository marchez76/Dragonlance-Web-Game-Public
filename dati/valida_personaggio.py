#!/usr/bin/env python3
"""
Valida dati/personaggi/*.json contro dati/schema/personaggio.schema.json.

PERCHE' QUESTO VALIDATORE FA PIU' DEGLI ALTRI
    Gli altri sei validano documenti di CONVERSIONE: la domanda e' se il
    documento dica fedelmente cio' che la fonte dice. Qui la domanda e'
    diversa, perche' un personaggio non ha una fonte — e' materiale
    prodotto, e cio' che va controllato e' che ogni sua scelta stia dentro
    il filtro che l'ha permessa (decisione 66, `schema-personaggio`).

    Nove controlli, e sono di tre specie:

    A. I RIFERIMENTI RISOLVONO. Razza, classe, divinita', pacchetto, oggetti
       equipaggiati, incantesimi scelti: un id che non risolve e' peggio di
       un campo assente, perche' promette. (1)

    B. LE SCELTE STANNO DENTRO IL LORO FILTRO. La classe e' di partenza (2),
       l'allineamento appartiene al sottoinsieme che la classe permette (3),
       le competenze di abilita' sono fra le diciotto (4), lo stile e' fra i
       privilegi del chassis (5), i punteggi piu' gli aumenti non superano
       il massimale razziale (6). Un filtro `chiuso: false` NON si controlla
       e lo si dichiara: e' una lacuna nota, e fingere di controllarla
       sarebbe peggio che non controllarla. (7)

    C. LO SCHEMA NON HA PRESO LA DERIVA. Nessun campo di primo livello e' un
       derivato secondo `motore/combattimento.DERIVATI` (8), e `genere`/`eta`
       restano ASSENTI finche' la questione aperta (`genere-eta-personaggio`)
       e' aperta (9). Il nono e' il controllo che rende il «posto segnalato e
       non riempito» una cosa eseguita e non una frase: il giorno in cui la
       questione viene decisa, questo controllo fallisce e chiede di
       riportare la decisione qui.

Uso:  uv run --with jsonschema python3 dati/valida_personaggio.py
"""

import glob
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.dirname(BASE))

import _allineamenti as AL  # noqa: E402
import _schemi as S        # noqa: E402
import _sistema as sistema  # noqa: E402
import decisioni as DEC     # noqa: E402

CARTELLA = os.path.join(BASE, "personaggi")

# I due campi che lo schema NON deve avere finche' la questione e' aperta.
POSTO_SEGNALATO = ("genere", "eta")


# ------------------------------------------------------------------ letture

def indice(cartella):
    fuori = {}
    for p in sorted(glob.glob(os.path.join(BASE, cartella, "*.json"))):
        with open(p, encoding="utf-8") as fh:
            d = json.load(fh)
        fuori[d["id"]] = d
    return fuori


def schede():
    fuori = []
    for p in sorted(glob.glob(os.path.join(CARTELLA, "*.json"))):
        with open(p, encoding="utf-8") as fh:
            fuori.append((os.path.basename(p), json.load(fh)))
    return fuori


# ------------------------------------------------------------- i controlli

def allineamenti_permessi(classe, divinita):
    """Il sottoinsieme dei nove permesso, o None se nessuno vincola.

    DUE SEDI, non una, ed e' la forma della
    decisione 61 (`allineamento-insieme`): il vincolo della classe e' un
    insieme dei nove quando `applied` e' vero; quando invece la classe
    dichiara `depends_on: "divinita"` l'insieme non e' suo, e' del dio — si
    legge `source_2e.priest_alignment` e lo si traduce nei nove con
    `_allineamenti._da_priest()`, che e' la stessa lettura usata per le
    classi e non una seconda.
    """
    a = ((classe.get("mechanics_5e") or {}).get("alignment_restriction") or {})
    if a.get("applied"):
        return set(a.get("values") or [])
    if a.get("depends_on") == "divinita" and divinita is not None:
        testo = (divinita.get("source_2e") or {}).get("priest_alignment")
        if testo:
            return set(AL._da_priest(testo))
    return None


def massimali(razza):
    m = ((razza.get("mechanics_5e") or {}).get("ability_maximums") or {})
    return {k: v for k, v in m.items() if isinstance(v, int)}


def _filtro_arma(nome, i, voce, ident, filtro, oggetti, e):
    """La voce risolta soddisfa davvero il filtro che la riga dichiara?

    E' il solo posto di questo file in cui un filtro viene APPLICATO invece
    che dichiarato, ed e' possibile perche' categoria e tipo dell'arma sono
    campi e non prosa. Dove il filtro e' `null` — «simbolo sacro» — non c'e'
    niente da applicare, e si tace invece di fingere.
    """
    if not filtro:
        return
    w = ((oggetti[ident].get("mechanics_5e") or {}).get("weapon_5e")) or {}
    for campo in ("categoria", "tipo"):
        atteso = filtro.get(campo)
        if atteso and w.get(campo) != atteso:
            e(f"equipaggiamento iniziale, riga {i}: «{voce}» chiede "
              f"{campo}={atteso}, ma `{ident}` ha {campo}={w.get(campo)!r}")


def controlla(nome, p, razze, classi, dei, oggetti, pacchetti, incantesimi,
              err, dichiara):
    def e(m):
        err(f"{nome}: {m}")

    # (1) i riferimenti risolvono
    if p["razza"] not in razze:
        e(f"razza `{p['razza']}` non risolve in dati/razze/")
    if p["classe"] not in classi:
        e(f"classe `{p['classe']}` non risolve in dati/classi/")
    if p.get("divinita") and p["divinita"] not in dei:
        e(f"divinita' `{p['divinita']}` non risolve in dati/divinita/")
    for ruolo, ident in (p.get("equipaggiato") or {}).items():
        if ident and ident not in oggetti:
            e(f"equipaggiato.{ruolo} = `{ident}` non risolve in dati/oggetti/")

    razza = razze.get(p["razza"])
    classe = classi.get(p["classe"])
    scelte = p.get("scelte") or {}

    # (2) la classe e' di partenza
    if classe is not None:
        liv = ((classe.get("mechanics_5e") or {}).get("entry_level") or 1)
        if liv > 1:
            e(f"classe `{p['classe']}` ha entry_level {liv}: non e' una "
              f"classe di partenza, e un personaggio non puo' nascerci "
              f"(decisione 64, `composizione-cinque-classi`)")

    # (3) l'allineamento sta nel sottoinsieme della classe
    if classe is not None:
        permessi = allineamenti_permessi(
            classe, dei.get(p.get("divinita")) if p.get("divinita") else None)
        if permessi is not None and p["allineamento"] not in permessi:
            e(f"allineamento `{p['allineamento']}` fuori dal sottoinsieme "
              f"che `{p['classe']}` permette ({', '.join(sorted(permessi))})")

    # (4) le competenze di abilita' sono fra le diciotto
    s = scelte.get("competenze_abilita")
    if s:
        for a in s["valori"]:
            if a not in sistema.ABILITA_PER_ID:
                e(f"competenza di abilita' `{a}`: non e' una delle "
                  f"{len(sistema.ABILITA)} abilita' di "
                  f"dati/sistema/abilita.json")

    # (5) lo stile e' fra i privilegi del chassis
    s = scelte.get("stile")
    if s and classe is not None:
        nomi = {f["name"] for f in
                ((classe.get("mechanics_5e") or {}).get("chassis_features")
                 or [])}
        for v in s["valori"]:
            if v not in nomi:
                e(f"stile `{v}` non e' fra i privilegi del chassis di "
                  f"`{p['classe']}`")

    # (5b) gli incantesimi risolvono
    s = scelte.get("incantesimo_razziale")
    if s:
        for v in s["valori"]:
            if v not in incantesimi:
                e(f"incantesimo `{v}` non risolve in dati/incantesimi/")
    s = scelte.get("equipaggiamento_iniziale")
    if s and classe is not None:
        righe = (((classe.get("mechanics_5e") or {}).get("structural") or {})
                 .get("starting_equipment") or {}).get("scelte") or []
        viste = set()
        for v in s["valori"]:
            i, j = v["riga"], v["alternativa"]
            viste.add(i)
            if i >= len(righe):
                e(f"equipaggiamento iniziale: la riga {i} non esiste "
                  f"(`{p['classe']}` ne ha {len(righe)})")
                continue
            alt = righe[i]["alternative"]
            if j >= len(alt):
                e(f"equipaggiamento iniziale, riga {i}: l'alternativa {j} "
                  f"non esiste (ne ha {len(alt)})")
                continue
            da_risolvere = [x["name_srd"] for x in alt[j]["voci"]
                            if x["genere"] == "scelta"]
            risolti = {r["voce"]: r["oggetto"] for r in (v.get("risolti") or [])}
            for nome_voce in da_risolvere:
                if nome_voce not in risolti:
                    e(f"equipaggiamento iniziale, riga {i}: la voce "
                      f"«{nome_voce}» e' una SCELTA e non e' stata risolta")
                    continue
                ident = risolti[nome_voce]
                if ident is None:
                    dichiara(f"{nome}: riga {i}, «{nome_voce}» e' rimasta "
                             f"senza oggetto: il filtro non ha campioni a "
                             f"catalogo, e il buco si vede")
                elif ident not in oggetti:
                    e(f"equipaggiamento iniziale, riga {i}: `{ident}` non "
                      f"risolve in dati/oggetti/")
                else:
                    _filtro_arma(nome, i, nome_voce, ident,
                                 [x for x in alt[j]["voci"]
                                  if x["name_srd"] == nome_voce][0].get("filtro"),
                                 oggetti, e)
            for r in risolti:
                if r not in da_risolvere:
                    e(f"equipaggiamento iniziale, riga {i}: «{r}» risolta ma "
                      f"l'alternativa {j} non la nomina")
            # il pacchetto e' UNA di queste righe, non una chiave a parte
            for x in alt[j]["voci"]:
                if x["genere"] == "pacchetto" and x["riferimento"] not in pacchetti:
                    e(f"equipaggiamento iniziale, riga {i}: il pacchetto "
                      f"`{x['riferimento']}` non risolve in dati/pacchetti/")
        mancanti = sorted(set(range(len(righe))) - viste)
        if mancanti:
            e(f"equipaggiamento iniziale: le righe {mancanti} dell'elenco di "
              f"`{p['classe']}` non sono state scelte — una riga saltata e' "
              f"un pezzo di equipaggiamento che il personaggio non ha e "
              f"nessuno sa perche'")

    # (6) punteggi + aumenti contro il massimale razziale
    if razza is not None:
        tetti = massimali(razza)
        aum = {}
        for v in (scelte.get("aumenti_caratteristica") or {}).get("valori", []):
            aum[v["caratteristica"]] = aum.get(v["caratteristica"], 0) + v["valore"]
        fissi = ((razza.get("mechanics_5e") or {})
                 .get("ability_adjustments") or {})
        for car, base in p["punteggi"].items():
            tot = base + aum.get(car, 0) + (fissi.get(car) or 0
                                            if isinstance(fissi, dict) else 0)
            if car in tetti and tot > tetti[car]:
                e(f"{car}: {tot} supera il massimale razziale {tetti[car]} "
                  f"di `{p['razza']}` (decisione 10, `massimali-razziali`)")

    # (6b) nessuna scelta e' stata fatta a un livello non ancora raggiunto
    for chiave, sc in sorted(scelte.items()):
        if sc["al_livello"] > p["livello"]:
            e(f"`scelte.{chiave}` dichiara di essere stata fatta al "
              f"{sc['al_livello']}° livello, ma il personaggio e' di "
              f"{p['livello']}°")

    # (7) i filtri che nessuno puo' applicare, dichiarati e non finti
    for chiave, s in sorted(scelte.items()):
        if not s["filtro"]["chiuso"]:
            dichiara(f"{nome}: `scelte.{chiave}` ha un filtro APERTO "
                     f"({s['filtro']['sede']}): l'insieme esiste nella fonte "
                     f"ma vive come prosa, quindi il valore scelto non e' "
                     f"controllabile")
    if p.get("lingue"):
        dichiara(f"{nome}: `lingue` non ha nessun insieme contro cui essere "
                 f"controllata — questione aperta (`lingue-di-krynn`)")


def controlla_schema_non_deriva(schema, err):
    """(8) e (9): lo schema non ha preso la deriva."""
    sys.path.insert(0, os.path.join(os.path.dirname(BASE), "motore"))
    import combattimento as C  # noqa: E402

    campi = set(schema["properties"])
    deriv = campi & set(C.DERIVATI)
    if deriv:
        err(f"schema: {', '.join(sorted(deriv))} sono derivati e non possono "
            f"essere campi di una scheda — "
            f"decisione 52 (`attacco-unica-lettura`)")

    aperta = "genere-eta-personaggio" in DEC.PER_ID_APERTA
    presenti = sorted(campi & set(POSTO_SEGNALATO))
    if aperta and presenti:
        err(f"schema: {', '.join(presenti)} sono stati aggiunti mentre la "
            f"questione aperta (`genere-eta-personaggio`) e' ancora aperta. "
            f"Il posto va segnalato, non riempito")
    if not aperta and not presenti:
        err("schema: la questione (`genere-eta-personaggio`) e' stata decisa "
            "e lo schema non e' stato aggiornato — se la decisione e' stata "
            "«non si registrano», va tolto questo controllo e detto perche'")
    return len(campi)


# ------------------------------------------------------------------- avvio

def main(argv):
    errori = []
    aperti = []

    schema = S.carica("personaggio.schema.json")
    val = S.validatore("personaggio.schema.json", schema)

    n_campi = controlla_schema_non_deriva(schema, errori.append)

    razze, classi = indice("razze"), indice("classi")
    dei, oggetti = indice("divinita"), indice("oggetti")
    pacchetti, incantesimi = indice("pacchetti"), indice("incantesimi")

    docs = schede()
    for nome, p in docs:
        errs = sorted(val.iter_errors(p), key=lambda x: list(x.path))
        for x in errs:
            errori.append(f"{nome}: {'.'.join(str(i) for i in x.path)}: "
                          f"{x.message}")
        if not errs:
            controlla(nome, p, razze, classi, dei, oggetti, pacchetti,
                      incantesimi, errori.append, aperti.append)
        print(("✗ " if errs else "✓ ") + nome)

    print()
    for m in errori:
        print("  ERRORE  " + m)
    for m in aperti:
        print("  APERTO  " + m)

    print(f"\n{len(docs)} personaggi controllati, {len(errori)} errori.")
    print(f"Lo schema ha {n_campi} campi di primo livello e nessuno di essi "
          f"e' un derivato; `genere` ed `eta` restano il posto segnalato e "
          f"non riempito.")
    if aperti:
        print(f"{len(aperti)} filtri dichiarati APERTI: non sono errori, sono "
              f"cio' che oggi nessuno puo' controllare.")
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
