# Domini di rete permessi

*Generato da `genera_rete.py` il 2026-08-18. Non modificare a mano: la sorgente è
il registro dentro lo script, da cui derivano sia questo documento sia
`.claude/settings.json`.*

**7 domini permessi**, di cui **1** effettivamente usato finora.

---

## Come funziona

La shell **non ha rete diretta**: nessun `/etc/resolv.conf`, solo l'interfaccia
di loopback. Tutto il traffico passa da due proxy che girano **fuori** dal
sandbox — HTTP su `:3128`, SOCKS5 su `:1080` — e il proxy decide dominio per
dominio.

Senza allowlist ogni host nuovo fa scattare una richiesta di conferma. Con
l'allowlist i domini qui sotto passano senza chiedere.

**Cosa questo NON cambia:** il recupero di contenuti dal web continua a passare
dagli strumenti di fetch, non dalla shell. L'allowlist serve a `pip`, `npm`,
`git` — non a leggere pagine con `curl`. Quella non è una configurazione, è una
regola di comportamento e resta valida a prescindere.

---

## Domini permessi

### Gestori di pacchetti

| dominio | perché | dal | autorizzato da | già usato |
|---|---|---|---|:-:|
| `pypi.org` | Indice dei pacchetti Python. Serve a `pip install`. | 2026-08-18 | Marco | — |
| `files.pythonhosted.org` | Dove PyPI ospita gli archivi veri: senza questo `pip` risolve il nome ma non scarica nulla. | 2026-08-18 | Marco | — |
| `registry.npmjs.org` | Registro npm. Servira' in Fase 2 se il motore di combattimento avra' una parte in JavaScript. | 2026-08-18 | Marco | — |
| `*.npmjs.org` | Sottodomini del registro npm, usati per gli archivi. | 2026-08-18 | Marco | — |

### Repository di codice

| dominio | perché | dal | autorizzato da | già usato |
|---|---|---|---|:-:|
| `github.com` | Cloni di repository. E' il dominio da cui si sarebbe preso PCGen quando serviva un riscontro sulle conversioni 3.5. | 2026-08-18 | Marco | — |
| `*.githubusercontent.com` | Dove GitHub serve i file grezzi: senza questo `git clone` funziona ma il download diretto di un singolo file no. | 2026-08-18 | Marco | — |

### Fonti di regole

| dominio | perché | dal | autorizzato da | già usato |
|---|---|---|---|:-:|
| `api.open5e.com` | SRD 5.1 in forma strutturata, licenza CC-BY. E' la fonte da cui vengono le tabelle di classe in `dati/_srd51.py`, la lista incantesimi del chierico in `dati/_sfere_5e.py` e i mostri in `dati/_fonti/srd51_mostri.py`. UNICO dominio di questo elenco gia' usato davvero. | 2026-08-18 | Marco | sì |


---

## Valutati e non inclusi

| dominio | perché no |
|---|---|
| `*` | Aperto a tutto. Scartato: il proxy decide in base al nome host dichiarato dal client e NON ispeziona il TLS, quindi con `*` qualunque cosa giri nel sandbox raggiunge qualunque host — compresi i pacchetti di terzi che `pip install` esegue, che hanno accesso in lettura a questa cartella. La differenza pratica con l'elenco sopra e' vicina a zero. |
| `5e.tools` | Mirror comunitario di manuali protetti. La decisione 26 esclude gia' quel materiale come non tracciabile: non ha senso aprirgli la rete. |

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
