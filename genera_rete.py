#!/usr/bin/env python3
"""
Genera .claude/settings.json e RETE-domini-permessi.md dal registro qui sotto.

PERCHE' UN GENERATORE E NON DUE FILE SCRITTI A MANO
    Stessa ragione di `genera_contesto.py`: due elenchi mantenuti a mano si
    desincronizzano. Qui la sorgente di verita' e' REGISTRO; il file di
    configurazione che il sandbox legge e il documento che leggi tu sono
    entrambi derivati da quello. Non possono divergere.

COME FUNZIONA L'ALLOWLIST, E DOVE NON FUNZIONA AFFATTO
    L'ambiente LOCALE (Linux, CachyOS): il sandbox della shell non ha rete
    diretta,
    tutto passa da un proxy che gira fuori dal sandbox e decide dominio per
    dominio. Senza allowlist, al primo accesso a un host nuovo parte una
    richiesta di conferma; con l'allowlist i domini elencati passano.
    E' l'ambiente per cui questo file e' stato scritto il 18/08/2026. Che sia
    Linux (CachyOS) e' dichiarato da Marco il 22/09/2026, e va scritto perche'
    fino a quel giorno il file non nominava nessun sistema: chi legge un
    documento di rete senza sapere su che macchina vale finisce per
    indovinarlo, ed e' esattamente cio' che era successo.

    L'ambiente REMOTO (Claude Code on the web, container effimero): questa
    allowlist NON GOVERNA NIENTE. La rete e' decisa dalla policy
    dell'environment, fuori dal progetto e non modificabile da qui. Misurato
    il 22/09/2026, e il risultato e' il peggiore possibile per un'allowlist:

        api.open5e.com   CONNECT tunnel failed, 403   BLOCCATO
        pypi.org         200
        github.com       400 (risponde: raggiungibile)
        raw.githubusercontent.com  301

    Cioe' passa tutto tranne l'UNICO dominio che il progetto usi davvero — la
    fonte di dati/_srd51.py, _sfere_5e.py e _fonti/srd51_*.py. Nel frattempo
    l'elenco qui sotto continua a dichiararlo permesso.

    PERCHE' E' SCRITTO QUI E NON SOLO NEL DOCUMENTO. Un'allowlist che non
    governa niente e' peggio di un'allowlist assente: quella assente si vede,
    questa rassicura. E' la stessa forma del difetto che la decisione 58
    (`telaio-apre-classe-filtra`) ha chiuso altrove — un campo che si dichiara
    applicato senza essere applicabile — qui trovata in un file di
    configurazione invece che in un dato.

    NON E' UN ERRORE DA CORREGGERE cambiando i domini: l'elenco e' giusto per
    l'ambiente locale, dove resta in vigore. Cio' che mancava era dire QUALE
    ambiente descrive.

SCOPE: DI PROGETTO, NON UTENTE
    Il file generato e' `.claude/settings.json` DENTRO la cartella di progetto,
    quindi vale solo qui. E' voluto: l'allowlist resta accanto al progetto che
    la giustifica, e si legge insieme al resto.
    Per estenderla a tutti i progetti va copiata in ~/.claude/settings.json,
    che pero' sta fuori dal sandbox e non e' raggiungibile da qui.

REGOLA D'INGRESSO
    Un dominio nuovo si aggiunge SOLO dopo averlo chiesto. Ogni voce porta il
    motivo, la data e chi l'ha autorizzata. Un dominio senza motivo scritto e'
    un dominio che fra sei mesi nessuno sa perche' c'e'.

Uso:  python3 genera_rete.py
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# LA DATA E' UN DATO, NON L'OROLOGIO. Era `date.today()`, e questo rendeva il
# generatore NON RIPRODUCIBILE: rigenerare senza cambiare niente produceva
# comunque un diff, cioe' rumore indistinguibile da una modifica vera. Il
# difetto si e' manifestato il 22/09/2026 durante una semplice verifica — lo
# script e' stato eseguito per controllare che girasse, e ha sporcato l'albero.
# Un generatore che si dichiara sorgente di verita' deve dare lo stesso file a
# parita' di ingressi: ora la data si aggiorna quando si tocca il REGISTRO,
# come ogni altra voce.
AGGIORNATO = "2026-09-22"

# --------------------------------------------------------------------------
# REGISTRO — sorgente di verita'.
# (dominio, categoria, motivo, data, autorizzato_da, gia_usato)
# --------------------------------------------------------------------------
REGISTRO = [
    # ---- pacchetti Python ----
    ("pypi.org", "pacchetti",
     "Indice dei pacchetti Python. Serve a `pip install`.",
     "2026-08-18", "Marco", False),
    ("files.pythonhosted.org", "pacchetti",
     "Dove PyPI ospita gli archivi veri: senza questo `pip` risolve il nome "
     "ma non scarica nulla.",
     "2026-08-18", "Marco", False),

    # ---- pacchetti JavaScript ----
    ("registry.npmjs.org", "pacchetti",
     "Registro npm. Servira' in Fase 2 se il motore di combattimento avra' "
     "una parte in JavaScript.",
     "2026-08-18", "Marco", False),
    ("*.npmjs.org", "pacchetti",
     "Sottodomini del registro npm, usati per gli archivi.",
     "2026-08-18", "Marco", False),

    # ---- codice sorgente ----
    ("github.com", "codice",
     "Cloni di repository. E' il dominio da cui si sarebbe preso PCGen "
     "quando serviva un riscontro sulle conversioni 3.5.",
     "2026-08-18", "Marco", False),
    ("*.githubusercontent.com", "codice",
     "Dove GitHub serve i file grezzi: senza questo `git clone` funziona ma "
     "il download diretto di un singolo file no.",
     "2026-08-18", "Marco", False),

    # ---- fonti di regole ----
    ("api.open5e.com", "fonti",
     "SRD 5.1 in forma strutturata, licenza CC-BY. E' la fonte da cui vengono "
     "le tabelle di classe in `dati/_srd51.py`, la lista incantesimi del "
     "chierico in `dati/_sfere_5e.py` e i mostri in "
     "`dati/_fonti/srd51_mostri.py`. UNICO dominio di questo elenco gia' "
     "usato davvero.",
     "2026-08-18", "Marco", True),
]

CATEGORIE = {
    "pacchetti": "Gestori di pacchetti",
    "codice": "Repository di codice",
    "fonti": "Fonti di regole",
}

# Domini valutati e NON inclusi. Registrati perche' la domanda non si
# riapra, e perche' un rifiuto motivato vale quanto un permesso.
ESCLUSI = [
    ("*", "Aperto a tutto. Scartato: il proxy decide in base al nome host "
          "dichiarato dal client e NON ispeziona il TLS, quindi con `*` "
          "qualunque cosa giri nel sandbox raggiunge qualunque host — "
          "compresi i pacchetti di terzi che `pip install` esegue, che hanno "
          "accesso in lettura a questa cartella. La differenza pratica con "
          "l'elenco sopra e' vicina a zero."),
    ("5e.tools", "Mirror comunitario di manuali protetti. La decisione 26 (`criterio-tracciabilita`) "
                 "esclude gia' quel materiale come non tracciabile: non ha "
                 "senso aprirgli la rete."),
]


def genera_settings():
    return {
        "sandbox": {
            "network": {
                "allowedDomains": [d for d, *_ in REGISTRO]
            }
        }
    }


def genera_documento():
    per_cat = {}
    for d, cat, motivo, data, chi, usato in REGISTRO:
        per_cat.setdefault(cat, []).append((d, motivo, data, chi, usato))

    blocchi = []
    for cat, etichetta in CATEGORIE.items():
        if cat not in per_cat:
            continue
        blocchi.append(f"### {etichetta}\n")
        blocchi.append("| dominio | perché | dal | autorizzato da | già usato |")
        blocchi.append("|---|---|---|---|:-:|")
        for d, motivo, data, chi, usato in per_cat[cat]:
            blocchi.append(f"| `{d}` | {motivo} | {data} | {chi} | "
                           f"{'sì' if usato else '—'} |")
        blocchi.append("")

    usati = sum(1 for *_, u in REGISTRO if u)

    return f"""# Domini di rete permessi

*Generato da `genera_rete.py` il {AGGIORNATO}. Non modificare a mano: la sorgente è
il registro dentro lo script, da cui derivano sia questo documento sia
`.claude/settings.json`.*

**{len(REGISTRO)} domini permessi**, di cui **{usati}** effettivamente usato finora.

---

## Due ambienti, e questo elenco ne governa uno solo

**In locale** (Linux, CachyOS) la shell non ha rete diretta: il traffico passa da un
proxy che gira fuori dal sandbox e decide dominio per dominio. Senza allowlist
ogni host nuovo fa scattare una richiesta di conferma; con l'allowlist i domini
qui sotto passano senza chiedere. È l'ambiente per cui questo file è nato.

**In remoto** (Claude Code sul web, container effimero) **questo elenco non
governa niente.** La rete è decisa dalla policy dell'environment, fuori dal
progetto. Misurato il 22/09/2026:

| dominio | esito dall'ambiente remoto |
|---|---|
| `api.open5e.com` | **403 al CONNECT — bloccato** |
| `pypi.org` | 200 |
| `github.com` | 400 (risponde, raggiungibile) |
| `raw.githubusercontent.com` | 301 |

Passa tutto tranne l'unico dominio che il progetto usi davvero. La tabella qui
sotto continua a dichiararlo permesso, e da lì non lo è: **il permesso è di
questo file, il divieto è dell'ambiente, e vince l'ambiente.**

Non è una riga da correggere — l'elenco è giusto dove è in vigore. Quello che
mancava era dire *quale* ambiente descrive.

**Cosa questo NON cambia:** il recupero di contenuti dal web continua a passare
dagli strumenti di fetch, non dalla shell. L'allowlist serve a `pip`, `npm`,
`git` — non a leggere pagine con `curl`. Quella non è una configurazione, è una
regola di comportamento e resta valida a prescindere.

---

## Domini permessi

{chr(10).join(blocchi)}

---

## Valutati e non inclusi

| dominio | perché no |
|---|---|
{chr(10).join(f"| `{d}` | {m} |" for d, m in ESCLUSI)}

---

## Regola d'ingresso

**Un dominio nuovo si aggiunge solo dopo averlo chiesto.** Se durante il lavoro
serve un host che non è in elenco, la sequenza è:

1. mi fermo e ti dico quale serve e per cosa;
2. se dici sì, aggiungo la voce al registro in `genera_rete.py` con motivo,
   data e la tua autorizzazione;
3. rigenero questo documento e `.claude/settings.json`.

Un dominio senza motivo scritto è un dominio che fra sei mesi nessuno sa
perché c'è.

---

## Ambito

`.claude/settings.json` sta **dentro la cartella di progetto**, quindi vale
solo qui. È voluto: l'allowlist resta accanto al progetto che la giustifica.

Per estenderla a tutti i progetti va copiata in `~/.claude/settings.json`, che
però sta fuori dal sandbox e non è raggiungibile da questa sessione: quella
copia devi farla tu.
"""


def main():
    d = os.path.join(BASE, ".claude")
    os.makedirs(d, exist_ok=True)

    p_set = os.path.join(d, "settings.json")
    with open(p_set, "w", encoding="utf-8") as f:
        json.dump(genera_settings(), f, ensure_ascii=False, indent=2)
        f.write("\n")

    p_doc = os.path.join(BASE, "RETE-domini-permessi.md")
    open(p_doc, "w", encoding="utf-8").write(genera_documento())

    # il documento e la configurazione devono elencare gli stessi domini
    letti = json.load(open(p_set, encoding="utf-8"))
    dom_set = letti["sandbox"]["network"]["allowedDomains"]
    dom_reg = [d for d, *_ in REGISTRO]
    assert dom_set == dom_reg, "settings.json e registro divergono"
    testo = open(p_doc, encoding="utf-8").read()
    mancanti = [x for x in dom_reg if f"`{x}`" not in testo]
    assert not mancanti, f"domini assenti dal documento: {mancanti}"

    print(f"scritto {p_set}")
    print(f"scritto {p_doc}")
    print(f"{len(dom_reg)} domini, coerenti fra registro, configurazione e documento.")
    for x in dom_reg:
        print(f"    {x}")


if __name__ == "__main__":
    main()
