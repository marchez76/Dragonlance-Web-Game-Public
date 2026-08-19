# Estrazione dei manuali — stato all'11/08/2026

## Situazione

| | manuali | pagine |
|---|---:|---:|
| Libreria totale | 122 | 18.035 |
| **Testo pronto** | **100** | **14.199** |
| Ancora da OCR | 22 | ~3.200 |

66 milioni di caratteri in `Testi/`.

## `Testi/` è la fonte canonica, `Estratti/` è storia

I `.txt` in `Estratti/` erano stati prodotti con `pdftotext -layout`: su una
pagina a due colonne le righe delle due colonne finiscono **fuse sulla stessa
riga di testo**, con la descrizione dei nani mescolata alle statistiche delle
armi barbariche. Leggibili da un umano, inutilizzabili per il parsing.

Misurato su tre manuali campione: fra il **52% e il 77% delle righe lunghe**
avevano colonne fuse, con il conteggio parole conservato al 99,9–100,1% dopo
la ri-estrazione. Nessuna perdita di contenuto, solo la riorganizzazione
nell'ordine di lettura corretto.

`Estratti/` resta sul disco come riferimento storico. **Non usarla per il
parsing.**

## ⚠ La libreria va ri-macinata

La prima passata aveva due difetti, scoperti dopo averla completata.

**Colonne non riconosciute.** La soglia che decideva se una banda bianca fosse
un gutter era troppo alta (9 punti). In molte pagine la banda è più stretta
perché qualche parola della colonna sinistra sporge, e su altre non esiste
affatto perché un titolo a tutta larghezza attraversa il centro. Quelle pagine
venivano estratte come colonna singola e uscivano fuse — **1.116 pagine su
9.962, l'11%**.

Il controllo di qualità non se n'era accorto perché cercava righe separate da
sei o più spazi, la firma di `pdftotext -layout`. Ma le colonne saldate da un
mancato riconoscimento del gutter si uniscono con **spazi singoli**. Il
controllo dava zero difetti su 1.116 pagine difettose. Ora c'è
`controlla_testi.py`, che misura invece la lunghezza mediana delle righe
pagina per pagina: una pagina fusa è lunga circa il doppio delle altre dello
stesso libro.

**Lettere raddoppiate.** Molte stampe d'epoca ottengono il neretto
ridisegnando lo stesso glifo con un minimo scarto. `pdftotext` scartava i
doppioni, `pdfplumber` li conservava: il testo usciva `ffllaammee ssttrriikkee`
invece di `flame strike`. **7.075 occorrenze in 46 file**, tutte introdotte
dalla nuova estrazione. Si risolve con `dedupe_chars`, che però costa nove
volte tanto: viene quindi applicato solo alle pagine in cui il raddoppio è
effettivamente rilevato.

Entrambi i difetti sono corretti in `colstep.py`. **Tales of the Lance è già
stato ri-estratto** con la versione corretta: zero pagine fuse, zero
raddoppi, 0,20 s/pagina. Gli altri 99 manuali vanno rifatti:

```bash
rm -rf Testi .colstep_state       # oppure invalidare i singoli file
python3 colstep.py 39             # ripetere fino a esaurimento
python3 controlla_testi.py        # deve dire zero
python3 importa_ocr.py && python3 indicizza.py
```

## Struttura

```
Manuali/            122 PDF, 2,8 GB (sorgenti, mai modificati)
Testi/              100 .txt in ordine di lettura corretto
  └ indice.json     catalogo con stato e origine di ogni manuale
Estratti/           vecchia estrazione a colonne fuse — solo storico
colstep.py          ri-estrazione a colonne, incrementale
ocrstep.py          OCR per le scansioni, incrementale
importa_ocr.py      porta in Testi/ i manuali recuperati via OCR
indicizza.py        rigenera Testi/indice.json e ocr_queue.txt
ocr_queue.txt       coda OCR, dal PDF più leggero
```

### Formato di `Testi/*.txt`

```
[[p.57]]
...testo della colonna sinistra...
...testo della colonna destra...
```

Il marcatore usa l'**indice 0-based della pagina PDF** — lo stesso che finisce
nel campo `pages_pdf` dei dati strutturati in `dati/`. Permette di risalire
dalla riga di testo alla pagina originale per la verifica.

I file importati da OCR iniziano con `[[origine: OCR]]` e **non hanno
marcatori di pagina**: l'OCR lavora sull'immagine renderizzata e non conserva
la struttura.

## I due motori

Il sandbox termina ogni processo alla fine della singola chiamata e limita
ogni chiamata a 45 secondi: un job continuo non è possibile. Entrambi i motori
lavorano quindi per un budget di secondi, salvano lo stato pagina per pagina
ed escono. Rilanciandoli riprendono da dove si erano fermati.

```bash
python3 colstep.py 39            # ~39 secondi di ri-estrazione
python3 colstep.py 39 Dragonlance # solo quella cartella
python3 colstep.py --stato        # avanzamento senza lavorare
python3 ocrstep.py 41             # ~41 secondi di OCR
```

**Rendimento misurato**: la ri-estrazione a colonne ha macinato 14.851 pagine
in 47 minuti di calcolo, cioè 0,19 s/pagina medi — da 0,04 s/pagina sui moduli
leggeri a oltre 0,5 sui volumi da 80 MB. L'OCR è molto più lento: 0,8–2,8
s/pagina.

### Riconoscimento delle scansioni

`colstep.py` campiona dodici pagine distribuite su tutto il documento: se la
media è sotto i 100 caratteri per pagina, il PDF non ha layer di testo e viene
marcato `senza_testo` e lasciato alla pipeline OCR, senza produrre un file
vuoto. Sono 27 manuali su 122.

Cinque di questi erano già stati recuperati con OCR in una sessione
precedente: `importa_ocr.py` li ha portati in `Testi/` con l'intestazione che
ne dichiara l'origine. Restano 22 in coda.

## Cosa resta da fare

Le 22 scansioni in `ocr_queue.txt`, ordinate dal PDF più leggero. **Nessuna è
bloccante**: `Core/PHB Revised` e `Core/DMG Revised` duplicano `PHB.pdf` e
`DMG.pdf`, già disponibili in versione testo; il resto sono moduli
d'avventura, libri d'arte e mappe.

Dopo ogni sessione di OCR conviene eseguire `importa_ocr.py` e `indicizza.py`
per tenere allineati `Testi/` e la coda.

## Note di qualità

`Core/PHB.pdf` (AD&D 2ª ed.) ha un testo utilizzabile ma con imprecisioni
tipiche dell'OCR d'epoca: `THACO` con la lettera O al posto dello zero, numeri
di tabella errati (`Table 1` per `Table 7`). Va normalizzato in fase di
parsing, non serve rifare l'OCR.

Anche dopo la ri-estrazione, **le tabelle vanno verificate sull'immagine
renderizzata della pagina** prima di fidarsene. Il lavoro sulle razze e le
classi ha trovato per questa via tre difetti di impaginazione del manuale
stesso — non dell'estrazione. Vedi `dati/LEGGIMI.md`.

## Prossimo passo

Estrazione delle entità restanti in JSON strutturato: incantesimi, mostri,
oggetti, divinità. Razze e classi sono già fatte, in `dati/`.
