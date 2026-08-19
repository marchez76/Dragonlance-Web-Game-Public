# Dati strutturati — razze, classi e divinità di Krynn

Fase 0. **15 razze**, **17 classi** e **21 divinità** estratte da *Tales of the
Lance* (AD&D 2e, TSR 1992), capitoli *People of Ansalon*, *Classes of Ansalon*
e *Realms Above*.

## Struttura

```
dati/
  schema/razza.schema.json    schema JSON della razza
  schema/classe.schema.json   schema JSON della classe
  razze/<id>.json             una razza per file, generato
  classi/<id>.json            una classe per file, generato
  razze.index.json            indici, generati
  classi.index.json
  build_razze.py              sorgente di verita': i numeri stanno qui
  build_classi.py
  valida.py                   validazione razze
  valida_classi.py            validazione classi + controllo incrociato
  _fonti/                     estrattori e tabelle parsate dai PDF
```

Rigenerare e verificare tutto:

```bash
python3 dati/build_razze.py    && python3 dati/valida.py
python3 dati/build_classi.py   && python3 dati/valida_classi.py
python3 dati/build_divinita.py && python3 dati/valida_divinita.py
```

**I file in `razze/` non vanno modificati a mano.** Sono generati. Ogni
correzione va fatta in `build_razze.py` e rigenerata, così resta un solo posto
in cui un numero può essere sbagliato.

## Il doppio strato

Ogni razza ha due blocchi:

- **`source_2e`** — dati grezzi fedeli al manuale. Requisiti di caratteristica,
  aggiustamenti, formule di generazione, altezza/peso/età, infravisione,
  limiti di livello per classe, abilità speciali. Si tocca solo per correggere
  errori di trascrizione.
- **`mechanics_5e`** — la conversione. Attualmente `null` per tutte e 15:
  serve il PHB 5e come metro di riferimento (vedi `manuali-mancanti.md`).

Il vantaggio: la conversione si può rifare quante volte serve senza mai
riaprire i PDF.

## Il roster

| id | razza | note |
|---|---|---|
| `umano` | Umano | baseline 2e, nessun limite |
| `umano-barbaro` | Barbaro | 4 gruppi culturali, stesse statistiche |
| `nano-montagna` | Hylar / Daewar | |
| `nano-collina` | Neidar | |
| `nano-aghar` | Nano Sozzo | generazione caratteristiche non standard |
| `elfo-silvanesti` | Silvanesti | Car minimo 12, il più alto del roster |
| `elfo-qualinesti` | Qualinesti | |
| `elfo-kagonesti` | Kagonesti | −3 Int, nessuna classe da mago |
| `elfo-dimernesti` | Elfo dei bassifondi | mutaforma lontra |
| `elfo-dargonesti` | Elfo degli abissi | mutaforma delfino |
| `mezzelfo` | Mezzelfo | 11 classi, unico non umano ammesso ai Cavalieri |
| `gnomo-minoi` | Gnomo | solo magia illusionista |
| `kender` | Kender | 6 abilità speciali, la razza più dettagliata |
| `minotauro` | Minotauro | unico con caratteristiche fino a 20 |
| `irda` | Irda | nessun limite di livello, Cos massima 15 |

I clan Klar, Theiwar, Daergar e Zhakar restano fuori: il manuale li riserva
esplicitamente ai PNG.

## Le classi

| gruppo | classi |
|---|---|
| Warrior | `cavaliere-corona`, `cavaliere-spada`, `cavaliere-rosa`, `barbaro`, `cavaliere`, `mariner` |
| Wizard | `mago-alta-stregoneria` + le tre vesti `bianca` / `rossa` / `nera`, `mago-rinnegato` |
| Priest | `sacerdote-ordini-sacri`, `sacerdote-eretico` |
| Rogue | `handler`, `con-artist` |
| Normal | `tinker`, `commoner` |

Guerriero, ranger, paladino, ladro, bardo e illusionista restano quelli del
PHB 2e: il manuale non li ridefinisce, li cita soltanto nella tabella dei
limiti di livello.

### I Cavalieri di Solamnia confermano il design della sezione 5.1

I tre ordini hanno **tabelle di avanzamento separate che ripartono da zero**:
la Corona dal 1° livello, la Spada dal 3°, la Rosa dal 4°. Passando di ordine
l'esperienza si azzera, pur mantenendo i punti ferita. È esattamente la
meccanica che il documento di riferimento segnala di non portare in 5e — ora è
documentata col dato in mano, non a memoria.

I requisiti crescono in modo netto lungo la sequenza: Corona For 10 / Cos 10,
Spada For 12 / Sag 13, Rosa For 15 / Cos 15 / Des 12. La sequenzialità del
nostro design è quindi già implicita nella fonte: non è un'invenzione nostra,
è il ripristino di ciò che la 2e faceva e che *Shadow of the Dragon Queen* ha
perso passando ai feat.

I Cavalieri della Spada ottengono incantesimi dal 6° livello — da Kiri-Jolith,
non da Paladine, perché fu il dio della guerra santa a ispirare l'ordine.

### Le vesti non sono classi separate

Bianca, Rossa e Nera condividono progressione e incantesimi di
`mago-alta-stregoneria`. Cambiano solo l'allineamento e le scuole consentite —
sei per la Bianca e la Rossa, sette per la Nera, unica ad avere Necromanzia.
`entry_level: 3` indica il livello a cui si dichiara l'ordine, prima del Test,
non l'inizio di una nuova tabella.

Dettaglio con implicazioni di gioco: Nuitari ha un'orbita di soli 8 giorni
contro i 28 di Lunitari e i 36 di Solinari. Le Vesti Nere cambiano condizione
molto più spesso delle altre due.

## Le 21 divinità

Sette per famiglia celeste, come vuole il canone, sovrintese dall'Alto Dio.

| famiglia | divinità |
|---|---|
| Bene | Paladine, Mishakal, Majere, Kiri-Jolith, Habbakuk, Branchala, Solinari |
| Male | Takhisis, Sargonnas, Morgion, Chemosh, Zeboim, Hiddukel, Nuitari |
| Neutralità | Gilean, Sirrion, Reorx, Chislev, Zivilyn, Shinare, Lunitari |

Sei sono divinità maggiori: Paladine, Mishakal, Takhisis, Sargonnas, Gilean,
Reorx. Per ciascuna sono estratti allineamento del sacerdote, armi e armature
consentite, **sfere di incantesimi** (con distinzione fra accesso maggiore e
minore, che nel manuale è resa con un asterisco), poteri concessi e capacità
di scacciare i non morti.

Questo chiude l'ultima domanda aperta sui sacerdoti: `sacerdote-ordini-sacri`
rimandava alla p. 176 del manuale per le sfere di ciascun dio.

**I tre dei della magia coincidono con le tre vesti**: Solinari fonda le Vesti
Bianche, Lunitari le Rosse, Nuitari le Nere. Il validatore verifica che a ogni
dio corrisponda la sua classe. Per diventare sacerdote di una di queste
divinità bisogna prima esserne mago: quello di Lunitari deve essere Veste Rossa
di almeno 5° livello, poi ricomincia dal 1° da sacerdote continuando a lanciare
incantesimi come mago di 5°.

`valid_eras` qui significa **le epoche in cui la divinità concede incantesimi**,
non quelle in cui esiste. Coincide con le epoche in cui la classe
`sacerdote-ordini-sacri` è giocabile, e il controllo incrociato lo verifica.

## Le tabelle lunghe non sono trascritte a mano

Le progressioni di livello (25 righe × 6 tabelle) e quelle degli incantesimi
sono **parsate programmaticamente** dal testo ri-estratto, non ribattute.
Gli script stanno in `_fonti/`. Ritrascrivere a mano ~350 righe di numeri
sarebbe stata la parte più fragile del lavoro.

## Verifica fatta

Le otto tabelle di requisiti razziali (barbari, nani, Aghar, elfi, gnomi,
kender, minotauri, Irda) sono state ricontrollate **sull'immagine renderizzata
della pagina originale**, non sul testo estratto — 96 valori, zero
discrepanze. Lo stesso per la tabella dei limiti di livello e per le
progressioni della Corona, della Spada e dei maghi.

`valida_classi.py` esegue anche un **controllo incrociato**: razze e classi
vengono da due tabelle diverse dello stesso manuale e devono raccontare la
stessa storia. Se una razza dichiarasse di poter fare il Tinker mentre il
Tinker si dichiara riservato agli gnomi, una delle due trascrizioni sarebbe
sbagliata. Al momento: nessuna contraddizione.

Questo perché gli `.txt` in `Estratti/` hanno le due colonne di pagina fuse
riga per riga e non sono affidabili per il parsing. I capitoli usati qui sono
stati ri-estratti con ritaglio per colonna, rilevando il gutter reale della
pagina invece di tagliare a metà.

## Indici di pagina — due convenzioni, non intercambiabili

Convivono due numeri diversi, e vanno tenuti separati per nome, non per valore:

- **Indice PDF, 0-based** (`pages_pdf` nei JSON; `pagina` in `_bestiario_mc.py`;
  i marcatori `[[p.N]]` di `colstep.py`) — la posizione della pagina nel file,
  contando da 0. Per aprirla con uno strumento 1-based (`pdftoppm`, un lettore
  PDF qualsiasi) va usato **indice+1**. È l'unico numero disponibile per l'MC
  Dragonlance Appendix, che non stampa numeri di pagina (formato Monstrous
  Compendium a fogli sciolti).
- **Pagina stampata** (citazioni nel testo, `"pag. N stampata"`) — il numero
  che compare davvero sulla pagina fisica, per i manuali che lo stampano:
  *Tales of the Lance* (indice PDF −2), *Shadow of the Dragon Queen* (indice
  PDF −1, offset verificato ma di lettura difficile per via dell'OCR del
  manuale). Non coincide con l'indice PDF: l'offset viene dal materiale
  iniziale non numerato (copertina, indice, crediti) e va verificato pagina
  per pagina la prima volta che si cita un manuale nuovo, non assunto.

**Mai scrivere "pag. N stampata" per l'MC Dragonlance Appendix**: non esiste un
numero stampato da citare. Per quella fonte, cita per **voce** ("MC
Dragonlance Appendix, voce «Nome»") o per indice PDF esplicitamente marcato
come tale — mai i due mescolati sotto la parola "stampata".

Errore trovato e corretto il 19/08/2026: `_tratti_mc.py` dichiarava
"stampata" un numero che era in realtà l'indice 0-based, in 9 citazioni
(Minotauro ×5, Irda ×2, Kagonesti ×1, Silvanesti ×1). I valori numerici
erano tutti corretti — verificati sulle immagini di pagina, zero discrepanze
— solo l'etichetta era falsa: nessuno di quei numeri era mai stato stampato
da nessuna parte. Corretto in un punto solo (`_tratti_mc.py`, blocco
`PAGINE`), che ora cita per voce; `dati/razze/*.json` rigenerati.

## Cosa è rimasto aperto

Ogni razza ha un campo `open_questions` con le ambiguità della fonte. Le tre
che contano:

1. **Elfi marini** — la tabella dei limiti di livello e il testo delle Gaming
   Notes si contraddicono: la tabella dà Fighter 16 / Cavalier 10 / High
   Sorcerer 10, il testo dice livelli illimitati con riduzione al 10° fuori
   dall'acqua, e include Paladin che la tabella non riporta. Verificato
   sull'originale: l'incoerenza è del manuale, non della trascrizione.
2. **Dargonesti** — assenti dalla tabella dei limiti di livello. Il campo è
   lasciato vuoto invece di copiare i Dimernesti: è un buco della fonte, non
   un dato.
3. **Resistenza magica dei kender** — «+1 ogni 3½ punti di Costituzione»: il
   manuale non dice se arrotondare per difetto o interpolare.
4. **Tabella incantesimi dei Cavalieri della Spada** — disallineata in stampa
   ai livelli 9, 14 e 15 (cinque o sei colonne invece di sette). Verificato
   sull'originale: è un difetto di impaginazione. Le righe sono state lette da
   sinistra a destra; il risultato è coerente con le righe adiacenti corrette
   e mantiene la progressione monotona.
5. **Ricchezza iniziale del Cavaliere** — il testo estratto dà «564x10 stl»,
   chiaramente corrotto. Ricostruito come `5d4x10` dalla regola base del gruppo
   Warrior in 2e. È l'unico valore del dataset **dedotto anziché letto**.

`valid_eras` è uno **strato editoriale nostro**, non un dato del manuale:
*Tales of the Lance* è ambientato alla Guerra della Lancia e non ragiona per
epoche. L'unica razza con epoche ristrette è l'Irda, che si estingue di fatto
con la Guerra del Caos.
