# Istruzioni di progetto

Contratto di comportamento, non documentazione. Per il progetto vedi
`CONTESTO-PROGETTO.md` (stato e le 30 decisioni). Se una regola qui sotto
viene ignorata, il danno è reale, non stilistico.

## 1. Due repository, e cosa non deve mai uscire

**Pubblico** (`.git`): documenti, script, schemi.
**Privato** (`.git-private`, wrapper `git-privato.sh`): `Manuali/`, `Testi/`,
`Estratti/`, `import/`, `Musica/`, `riscontro/`,
`dati/razze|classi|divinita|mostri/`, `dati/RAPPORTO-*-completo.md`.

**Meccanismo.** `.git-private` è un secondo repository Git nella STESSA
cartella di lavoro del pubblico, non un archivio a parte: stesso albero di
file, due storie separate. Si tocca **solo** tramite `git-privato.sh`
(comandi `aggiungi`, `elenco`, o qualunque sottocomando `git` passato come
argomento), **mai con `git` diretto** — un `git add`/`git commit` invocato
senza il wrapper opera sul `.git` pubblico e può far filtrare testo di
manuale nella storia pubblica. Se una sessione futura incontra la cartella
`.git-private` senza questo contesto, il rischio è trattarla come residuo da
ripulire o ricominciare a tracciarla dal pubblico: è esattamente l'incidente
che l'uso del wrapper evita.

Il testo dei manuali non va **mai** nel pubblico. Criterio da applicare prima
di ogni commit pubblico, su ogni file toccato: **"questo file riproduce testo
dei manuali?"**

Le regole di gioco in sé sono fatti e si possono descrivere con parole
proprie — dado vita, requisiti, quali armi può usare una classe. Ciò che è
protetto è la **forma** del manuale: il testo, la scelta delle parole, la
prosa descrittiva. Citazioni brevi sono lecite solo quando il punto è la
forma esatta (es. documentare un refuso di stampa) — mai per riprodurre una
descrizione.

## 2. La riduzione avviene nel generatore

Mai con `sed` o modifiche a valle: si sfasa alla prima rigenerazione — è
già successo tre volte. I generatori che toccano dati privati producono
**due uscite** dalla stessa analisi: `RAPPORTO-*.md` (pubblico, ridotto) e
`RAPPORTO-*-completo.md` (privato, con testo di fonte), con la riduzione
come parametro del generatore (`completo=True/False`), verificato campo per
campo — non assunto.

## 3. Numeri derivati, mai scritti a mano

Ogni conteggio nella prosa dei documenti generati va interpolato dai dati.
Un numero scritto a mano si sfasa alla prossima rigenerazione: è già
costato quattro giri di incoerenze in questo progetto.

## 4. Convenzione delle pagine

Due numeri diversi convivono, non sono intercambiabili:

- **Indice PDF, 0-based** (`pages_pdf` nei JSON, `pagina` in
  `_bestiario_mc.py`, i marcatori `[[p.N]]` di `colstep.py`) — per aprirlo
  con `pdftoppm` o un lettore PDF (1-based) va usato **indice+1**. È l'unico
  numero disponibile per l'MC Dragonlance Appendix, che non stampa numeri di
  pagina (formato Monstrous Compendium a fogli sciolti).
- **Pagina stampata** (`"pag. N stampata"`) — solo per manuali che la
  stampano davvero (*Tales of the Lance*, *Shadow of the Dragon Queen*).
  Mai per l'MC Appendix: non esiste un numero stampato da citare lì.

Dettaglio completo in `dati/LEGGIMI.md`, sezione "Indici di pagina".

## 5. Ambienti

Tutto il lavoro — rete, git, PDF, immagini di pagina, generatori, rapporti,
conversioni — è su Claude Code. Cowork resta solo per OCR di massa delle
scansioni in coda e **non tocca git**. Dettaglio in `divisione-del-lavoro.md`.

## 6. Rimandi

- `CONTESTO-PROGETTO.md` — stato del progetto e le 30 decisioni.
- `dati/RAPPORTO-*.md` — diagnostiche generate.
- `dati/LEGGIMI.md` — struttura dei dati e convenzione delle pagine.
- `divisione-del-lavoro.md` — chi fa cosa.
