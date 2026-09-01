#!/usr/bin/env python3
"""
`source_2e` contro `mechanics_5e`: i due strati di razze e classi.

SESTA STRUTTURA DOPPIA DEL PROGETTO
    I due strati della decisione 7 (`doppio-strato`) descrivono le stesse
    grandezze — vincoli di caratteristica, massimali, aggiustamenti, formule
    di generazione, minimi di classe — e nessuno li confrontava. Sono
    scritti dalla stessa passata di `build_razze.py` / `build_classi.py`,
    quindi il giorno uno coincidono per costruzione. Il giorno due no: e' il
    modo esatto in cui sono nate le altre cinque divergenze del progetto.

PERCHE' UNA DIVERGENZA NON E' SEMPRE UN ERRORE
    `mechanics_5e` e' lo strato **rivedibile**: puo' e deve discostarsi
    dalla fonte quando una decisione lo impone. Il controllo non e' quindi
    "i due strati sono identici" — sarebbe falso e renderebbe inutile il
    doppio strato — ma:

        ogni scarto dallo strato di fonte e' DICHIARATO come tale.

    Un aggiustamento aggiunto da noi vive in `editorial_values` con la sua
    `editorial_note`; `values` e' il netto e deve tornare come somma dei
    due. Uno scarto che comparisse dentro `values` senza essere dichiarato
    da nessuna parte e' il difetto che questo file cerca: indistinguibile da
    una revisione legittima quando lo si guarda, e invisibile finche'
    qualcuno non lo guarda.

    Il caso reale che esiste gia' e' l'Umano Barbaro: `values` porta +1 a
    Forza e Costituzione che `source_2e` non ha: il tappo della
    decisione 20 (`tappo-barbaro`), confermato dalla
    decisione 43 (`barbaro-rimandato`). E' dichiarato, quindi passa. Ed e'
    la prova che serviva questo file: fino al 02/09/2026
    `motore/generazione.py` leggeva `source_2e` e quel +1 lo scartava in
    silenzio, tanto che l'Umano Barbaro risultava incompatibile con
    Cavaliere e Cavaliere della Rosa usando array standard o point-buy —
    due combinazioni legittime, rifiutate da un motore che leggeva lo
    strato sbagliato.

LA NORMALIZZAZIONE E' IL PUNTO DELICATO
    I due strati non portano gli stessi valori nella stessa FORMA, e
    confonderlo produrrebbe divergenze inventate:
      - `source_2e.ability_requirements` ha sempre sei caratteristiche, con
        `min`/`max` eventualmente `null`;
      - `ability_constraints.limits` **omette** le caratteristiche del tutto
        prive di vincoli (l'Umano Barbaro ne omette una);
      - `ability_caps.caps` porta **solo i massimali dichiarati** (due su
        sei per l'Umano Barbaro), e la casella assente non e' un buco: e' la
        caratteristica libera, che per la decisione 44
        (`tetto-punto-perduto`) resta al 20 della 5e;
      - `source_2e.ability_generation` include la voce generica `all: 3d6`
        che lo strato 5e non riporta, perche' il default di casa e' un
        altro (decisione 8, `generazione-caratteristiche`).

    Ogni confronto qui sotto normalizza le due forme PRIMA di confrontarle,
    e la normalizzazione e' scritta una volta sola.

Uso:
    python3 dati/verifica_strati.py          # esce != 0 se ci sono divergenze
    python3 dati/verifica_strati.py -v       # elenca anche gli scarti dichiarati
"""

import glob
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from decisioni import cita  # noqa: E402

CAR = ["str", "dex", "con", "int", "wis", "cha"]
TETTO_5E = 20
CHIAVE_GENERICA = "all"


# --------------------------------------------------------------- caricamento

def carica(cartella):
    out = []
    for f in sorted(glob.glob(os.path.join(BASE, "dati", cartella, "*.json"))):
        out.append(json.load(open(f, encoding="utf-8")))
    return out


# ------------------------------------------------------------ normalizzazioni

def req_fonte(entita):
    """`source_2e.ability_requirements` in forma canonica {car: (min, max)},
    con i null gia' risolti: nessun minimo = 3, nessun massimo = None."""
    req = entita["source_2e"].get("ability_requirements") or {}
    out = {}
    for c in CAR:
        v = req.get(c) or {}
        out[c] = (v.get("min") or 3, v.get("max"))
    return out


def limiti_5e(entita):
    """`ability_constraints.limits` nella STESSA forma di req_fonte().
    La chiave assente e' la caratteristica senza vincoli."""
    lim = ((entita.get("mechanics_5e") or {}).get("ability_constraints")
           or {}).get("limits") or {}
    out = {}
    for c in CAR:
        v = lim.get(c) or {}
        out[c] = (v.get("min") or 3, v.get("max"))
    return out


def tetti_5e(entita):
    """`ability_caps.caps` come {car: tetto}, con il 20 della 5e sulle
    caselle che il manuale non massimalizza."""
    caps = ((entita.get("mechanics_5e") or {}).get("ability_caps")
            or {}).get("caps") or {}
    return {c: caps.get(c) if caps.get(c) is not None else TETTO_5E
            for c in CAR}


def dado(v):
    """`d10` e `1d10` sono lo stesso dado scritto in due modi. Senza questa
    normalizzazione il confronto segnalerebbe 8 cambi di dado vita dove il
    RAPPORTO-personaggio §2.2 ne conta 3: cinque sarebbero pura notazione,
    e cinque falsi positivi bastano a far ignorare l'intero controllo."""
    if not v:
        return None
    v = str(v).strip().lower()
    return "1" + v if v.startswith("d") else v


def formule_fonte(entita):
    gen = entita["source_2e"].get("ability_generation") or {}
    return {k: v for k, v in gen.items() if k != CHIAVE_GENERICA and k in CAR}


def formule_5e(entita):
    gen = ((entita.get("mechanics_5e") or {}).get("generation") or {})
    return {k: v for k, v in (gen.get("dice_formulas") or {}).items()
            if k in CAR}


# ------------------------------------------------------------------ controlli

def confronta_razza(r):
    """(divergenze, scarti_dichiarati) per una razza."""
    rid = r["id"]
    div, dichiarati = [], []
    m = r.get("mechanics_5e")
    if not m:
        return [(rid, "strato-assente", "mechanics_5e nullo")], []

    fonte, cinque = req_fonte(r), limiti_5e(r)

    # 1. i vincoli di creazione, caratteristica per caratteristica
    for c in CAR:
        if fonte[c] != cinque[c]:
            div.append((rid, "vincolo", f"{c}: fonte {fonte[c]} / 5e {cinque[c]}"))

    # 2. i tetti di crescita contro i massimali della fonte.
    #    decisione 44 (`tetto-punto-perduto`): massimale assente => 20.
    tetti = tetti_5e(r)
    for c in CAR:
        atteso = fonte[c][1] if fonte[c][1] is not None else TETTO_5E
        if tetti[c] != atteso:
            div.append((rid, "tetto",
                        f"{c}: dalla fonte ci si aspetta {atteso}, "
                        f"ability_caps dice {tetti[c]}"))

    # 3. tetto mai piu' basso del minimo richiesto: renderebbe la
    #    caratteristica insoddisfacibile e nessuno se ne accorgerebbe
    #    finche' un giocatore non ci sbatte in creazione.
    for c in CAR:
        if tetti[c] < cinque[c][0]:
            div.append((rid, "intervallo-vuoto",
                        f"{c}: minimo {cinque[c][0]} sopra il tetto {tetti[c]}"))

    # 4. aggiustamenti: il netto deve tornare, e lo scarto dalla fonte deve
    #    essere dichiarato come editoriale, con la sua nota.
    adj = m.get("ability_adjustments") or {}
    valori = adj.get("values") or {}
    da_fonte = adj.get("source_values") or {}
    editoriali = adj.get("editorial_values") or {}
    vero_fonte = r["source_2e"].get("ability_adjustments") or {}

    if da_fonte != vero_fonte:
        div.append((rid, "aggiustamento-fonte",
                    f"source_values {da_fonte} != source_2e {vero_fonte}"))
    somma = {c: da_fonte.get(c, 0) + editoriali.get(c, 0)
             for c in set(da_fonte) | set(editoriali)}
    somma = {c: v for c, v in somma.items() if v}
    if valori != somma:
        div.append((rid, "aggiustamento-netto",
                    f"values {valori} != source_values+editorial_values {somma}"))
    if editoriali and not adj.get("editorial_note"):
        div.append((rid, "scarto-non-dichiarato",
                    f"editorial_values {editoriali} senza editorial_note"))
    elif editoriali:
        dichiarati.append((rid, "aggiustamento editoriale",
                           ", ".join(f"{c} {v:+d}" for c, v in sorted(editoriali.items()))))

    # 5. formule di generazione
    ff, f5 = formule_fonte(r), formule_5e(r)
    if ff != f5:
        div.append((rid, "formule", f"fonte {ff} / 5e {f5}"))

    return div, dichiarati


def confronta_classe(c):
    """(divergenze, scarti_dichiarati) per una classe."""
    cid = c["id"]
    div, dichiarati = [], []
    m = c.get("mechanics_5e")
    if not m:
        return [(cid, "strato-assente", "mechanics_5e nullo")], []

    # 1. minimi di caratteristica
    fonte = c["source_2e"].get("ability_minimums") or {}
    am = m.get("ability_minimums") or {}
    cinque = am.get("values") or {}
    if fonte != cinque:
        div.append((cid, "minimi", f"fonte {fonte} / 5e {cinque}"))
    if cinque and not am.get("applied"):
        div.append((cid, "minimi-non-applicati",
                    "ability_minimums.values pieno ma applied non e' true: "
                    "il motore li applica comunque"))

    # 2. il dado vita del chassis prevale sulla fonte (RAPPORTO-personaggio
    #    §2.2), ma solo se il chassis lo dichiara davvero.
    ch = m.get("chassis") or {}
    if ch.get("srd_class"):
        hd_ch, hd_cl = dado(ch.get("hit_die")), dado(m.get("hit_die"))
        if hd_ch and hd_cl and hd_ch != hd_cl:
            div.append((cid, "dado-vita",
                        f"chassis {hd_ch} / mechanics_5e.hit_die {hd_cl}"))
        hd_fonte = dado(c["source_2e"].get("hit_die"))
        if hd_fonte and hd_ch and hd_fonte != hd_ch:
            dichiarati.append((cid, "dado vita dal chassis",
                               f"fonte {hd_fonte} -> {hd_ch}"))
    return div, dichiarati


# --------------------------------------------------------------------- report

def verifica():
    razze, classi = carica("razze"), carica("classi")
    div, dichiarati = [], []
    for r in razze:
        d, s = confronta_razza(r)
        div += d
        dichiarati += s
    for c in classi:
        d, s = confronta_classe(c)
        div += d
        dichiarati += s
    misure = {"razze": len(razze), "classi": len(classi),
              "divergenze": len(div), "scarti_dichiarati": len(dichiarati)}
    return div, dichiarati, misure


def main(argv):
    verbose = "-v" in argv
    div, dichiarati, misure = verifica()

    print(f"Strati confrontati: {misure['razze']} razze, "
          f"{misure['classi']} classi.")
    print(f"Scarti dichiarati: {misure['scarti_dichiarati']}. "
          f"Divergenze: {misure['divergenze']}.")

    if verbose and dichiarati:
        print("\nScarti dichiarati (leciti: lo strato 5e e' rivedibile):")
        for chi, tipo, det in dichiarati:
            print(f"  {chi:22} {tipo:26} {det}")

    if div:
        print("\nDIVERGENZE — uno scarto non dichiarato fra i due strati:")
        for chi, tipo, det in div:
            print(f"  {chi:22} {tipo:22} {det}")
        print(f"\nLo strato 5e e' rivedibile ({cita('doppio-strato')}), ma "
              "ogni scarto va dichiarato dove si vede.")
        return 1

    print("\nNessuna divergenza: i due strati dicono la stessa cosa dove "
          "devono, e dove differiscono lo dichiarano.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
