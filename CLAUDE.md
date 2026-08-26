# Istruzioni di progetto

Contratto di comportamento, non documentazione. Per il progetto vedi
`CONTESTO-PROGETTO.md` (stato e le 33 decisioni). Se una regola qui sotto
viene ignorata, il danno è reale, non stilistico.

La lingua di lavoro è l'ITALIANO: commit, rapporti, commenti, e le risposte
in sessione. Vale da subito in ogni sessione nuova, non solo dopo che la
conversazione lo ha reso ovvio dal contesto.

## 1. Due repository, e cosa non deve mai uscire

**Pubblico** (`.git`): documenti, script, schemi.
**Privato** (`.git-private`, wrapper `git-privato.sh`): `Manuali/`, `Testi/`,
`Estratti/`, `import/`, `Musica/`, `riscontro/`,
`dati/razze|classi|divinita|mostri|oggetti/`, `dati/RAPPORTO-*-completo.md`.

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

**Cartella nuova sotto `dati/` che porterà `source_2e`: esclusione scritta
alla nascita, non quando qualcuno se ne accorge.** Precedente: `dati/oggetti/`
è nata con la decisione 33 (il diadema dello Scheletro Guerriero) ma non è
stata aggiunta al `.gitignore` pubblico in quel momento — è rimasta protetta
solo perché `git-privato.sh` la tracciava comunque (elenco `PERCORSI`), non
per struttura. Scoperta e corretta il 21/08/2026. Quando arriverà
l'equipaggiamento della Fase 2 ce ne saranno altre: il momento giusto per
aggiungere la cartella al `.gitignore` pubblico (sopra) E all'elenco
`PERCORSI` di `git-privato.sh` è quando si crea il primo file lì dentro, non
un controllo a posteriori.

**Precedente in prevenzione, non solo in correzione: 21/08/2026, stessa
sera.** Generando `dati/oggetti.index.json` (indice dell'equipaggiamento
appena estratto), la stessa zona morta si sarebbe riformata in una forma
nuova: il file rientra nell'esclusione pubblica generica (`dati/*.index.json`)
ma nessuna riga di `PERCORSI` lo menziona per nome. Questa volta la voce è
stata aggiunta a `PERCORSI` nello **stesso commit** che ha creato il file,
non tre giorni dopo. La regola sopra non è cambiata: quello che conta è che
la vigilanza descritta ha funzionato *prima* che il file restasse orfano,
non solo *dopo*. Vale come conferma che la regola scritta funziona da sola,
non come una regola nuova.

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

- `CONTESTO-PROGETTO.md` — stato del progetto e le 33 decisioni.
- `dati/RAPPORTO-*.md` — diagnostiche generate.
- `dati/LEGGIMI.md` — struttura dei dati e convenzione delle pagine.
- `divisione-del-lavoro.md` — chi fa cosa.

## tokenlean — CLI tools for AI agents

Use `tl <command>` for all operations. One tool, many subcommands.

### When to use tl vs. just reading the file

- **<150 lines**: Just read it — tl overhead costs more than the file itself
- **150-400 lines**: `tl symbols` first, then `tl snippet <name>` for specific functions
- **400+ lines**: Always `tl symbols` first — never read the whole file unless you truly need it all
- **Tests/builds/linters**: Always wrap with `tl run` — filters noise, saves hundreds of tokens

### Core commands

| Command | Purpose |
|---------|---------|
| `tl symbols <file>` | Function/class signatures without bodies |
| `tl snippet <name> <file>` | Extract one function/class by name |
| `tl impact <file>` | What depends on this file (run before modifying) |
| `tl run "<cmd>"` | Token-efficient command output (tests, builds, linters) |
| `tl guard` | Pre-commit check (secrets, TODOs, unused exports, circular deps) |
| `tl structure` | Project overview with token estimates |
| `tl browse <url>` | Fetch any URL as clean markdown |
| `tl context7 <lib> [query] -t N` | Latest library/framework docs |
| `tl component <file>` | React component profile (props, hooks, state) |
| `tl analyze <file>` | Composite file profile (symbols + deps + impact + complexity) |

### Rules

- **Before reading a source file**, run `tl symbols <file>` first. Only read the full file if you need implementation details.
- **Before modifying a file**, run `tl impact <file>` to understand what depends on it and what might break.
- **Before committing**, run `tl guard` to catch secrets, new TODOs, unused exports, and circular deps.
- **When running commands**, wrap with `tl run "<cmd>"` — it extracts only errors and key output.
- **When exploring an unfamiliar codebase**, start with `tl structure` before diving into files.
- **When you need library docs**, use `tl context7 <lib> [query] -t N` — your training data is stale.
- All commands support `-j` (JSON), `-q` (quiet), `-l N` (limit lines), `-t N` (limit tokens), and `--help`.
- Run `tl --help` for the full command list.

### More commands

**Understanding code:** `tl advise` Recommend the next tokenlean commands for a task | `tl api` Extract REST/GraphQL API endpoints | `tl blame` Compact per-line authorship | `tl context` Estimate token usage for files/directories | `tl deps` Show file imports and dependency tree | `tl docs` Extract JSDoc/TSDoc documentation | `tl entry` Find entry points (main, routes, handlers) | `tl env` Find environment variables used in codebase | `tl example` Find diverse usage examples of a symbol/pattern | `tl exports` Show public API surface of a module | `tl flow` Call graph: what calls this, what it calls | `tl history` Recent changes to a file (commits only) | `tl monorepo` Show monorepo package structure and cross-deps | `tl pack` Workflow context packs for review, debug, refactor, PRs, and onboarding | `tl quota` Check AI subscription quota usage | `tl routes` Extract routes from web frameworks | `tl schema` Extract database schema from ORMs | `tl scope` Show what symbols are in scope at a given line | `tl types` Extract full TypeScript type definitions

**Before changing code:** `tl complexity` Code complexity metrics for functions | `tl coverage` Quick test coverage info for files | `tl errors` Map error types and throw points | `tl hotspots` Find frequently changed files (git churn) | `tl lint-config` Summarize lint/format/type config rules | `tl related` Find tests, types, and importers of a file | `tl risk-assess` Quick risk score combining blast radius + complexity + tests | `tl style` Detect coding conventions from actual code | `tl test-map` Map source files to their test files | `tl unused` Find unused exports and unreferenced files

**Search and utilities:** `tl cache` Manage tokenlean cache (stats, clear) | `tl changelog` Generate changelog from commits | `tl commit-prep` Pre-commit context: status + diff stat + recent log | `tl diff` Summarize git changes with token estimates | `tl dupes` Find duplicate / near-duplicate functions across a codebase | `tl gh` Batch GitHub operations (issues, sub-issues, project boards) | `tl lookup` Find an existing function by name/intent before writing a new one | `tl name` Check name availability (npm, GitHub, domains) | `tl npm` Quick npm package lookup | `tl parallel` Run commands in parallel with structured results | `tl playwright` Extract content from JS-rendered pages via headless browser | `tl pr` Summarize PR/branch changes | `tl publish` Publish to npm, wait until installable, optionally reinstall globally | `tl push` Stage, commit, and push in one call | `tl reddit` Fetch Reddit post/comments as clean markdown | `tl search` Run pre-defined search patterns | `tl tail` Token-efficient log tailing and summarization | `tl test` Run tests relevant to changed files


