# Stato lavoro Cowork — handoff

*12 agosto 2026. Aggiornato dopo le cinque decisioni sulle domande aperte.*

---

## 1. Lavoro fatto / decisioni prese

### Ri-estrazione della libreria (compito A)

- Azzerato `Testi/` e lo stato, rimacinati **95 manuali / 14.047 pagine in 60 minuti** con `colstep.py` corretto.
- **Risultato richiesto**: pagine con colonne fuse **193 su 12.070 (1,6%)**, contro le 1.116 su 9.962 (11%) di prima. Occorrenze di lettere raddoppiate: **zero**.
- Le 193 residue non sono tutte difetti: il controllo segnala le pagine con righe anomalmente lunghe rispetto alla mediana del libro, e alcune sono tabelle o impaginati a colonna singola legittimi. Un campione verificato geometricamente ne conferma una parte come reali.

### Tre problemi trovati durante la ri-estrazione

- **Falsi positivi sui raddoppi**: il conteggio iniziale dava 2.142 occorrenze, ma `pqqqqqqqqqqq` è un filetto decorativo, non testo raddoppiato. Affinato il criterio (servono almeno 3 lettere *diverse* nella sequenza): i raddoppi veri erano **695 in 17 file**.
- **`dedupe_chars` non bastava**: su alcune pagine i glifi di rinforzo hanno uno scarto reale e non sono sovrapposti, quindi sopravvivono. Aggiunta `sdoppia()`, una correzione mirata sul testo, sicura perché quel pattern non esiste in nessuna lingua. Applicata ai file già estratti senza rimacinare. Raddoppi ora **zero**.
- **Due regressioni gravi**, intercettate confrontando la qualità con la vecchia estrazione: `MMI` passato da 25,9% a 14,5% di parole inglesi riconosciute, e **`PsionicsHandbook` dal 32,1% allo 0,3%**. Causa: quei PDF hanno un layer di testo *presente ma corrotto* (font map rotta, restituisce testo cifrato), che `ha_layer_testo` accettava. La versione OCR in `Estratti/` era molto migliore. Aggiunto a `importa_ocr.py` un controllo di qualità che preferisce l'OCR quando il testo estratto è illeggibile. Entrambe recuperate.

### Applicazione delle decisioni ai dati (decisioni 2, 3, 5)

- **Decisione 2** — aggiunto `mechanics_5e` a razze e classi con i vincoli come **regole di validazione applicate**: `ability_constraints` (min/max razziali), `ability_adjustments`, `allowed_classes` (le classi assenti dalla tabella sono precluse), `ability_minimums` e `alignment_restriction` per le classi.
- **Decisione 3** — i limiti di livello **restano** in `source_2e.class_level_limits`; in `mechanics_5e` il campo `level_limits.applied` è `false` con nota esplicita, così l'assenza è leggibile come deliberata.
- **Declassati** elfi marini e Dargonesti da `open_questions` a note di fonte, come richiesto: senza limiti di livello applicati la contraddizione non tocca più nulla di giocabile.
- **Decisione 5** — modellazione delle Vesti confermata e documentata: `mago-alta-stregoneria` classe base, le tre Vesti come affiliazione a `entry_level` 3.
- Aggiornato `valida.py`: la regola che pretendeva `open_questions` per una razza senza limiti di livello ora accetta anche una nota di fonte.

### Verifica della ricchezza del Cavaliere (compito C)

Renderizzata la pagina originale: **il manuale stampa davvero «564x10 stl»**. Non era un difetto di estrazione — è un refuso tipografico dell'originale (la `d` di `5d4` resa come `6`). Il valore resta marcato come dedotto, ma ora sappiamo che la deduzione riguarda un errore del manuale, non nostro. Le altre ambiguità (7-11) non sono state toccate.

### Documento di riferimento (compito B)

Le modifiche a §3, §5.1 e §7 **erano già sul disco** (il file era passato da 18.620 a 20.898 byte): la copia che risultava mancante è la cache read-only della project knowledge, sincronizzata prima. Ora il documento è a 25.195 byte e contiene tutto quanto richiesto, più la sezione **STATO ATTUALE** in cima.

### Novità arrivate durante il lavoro

- **Cartella `Manuali/D&D 5e/` con 18 PDF**. Tutti con layer di testo; le due copie «Inglês Alto Scan» hanno però OCR degradato, mentre le versioni semplici sono pulite.
- **Verificato `2014.5e.tools`**: è genuino ed è davvero la versione 2014, completa. Meglio ancora, i dati sono su GitHub (`5etools-mirror-3/5etools-2014-src`) come **JSON strutturato** con `size`, `speed`, `ability`, `traitTags` — un metro di conversione molto più comodo di 388 pagine di PDF.

---

## 2. Stato dei file

```
Dragonlance WEB GDR Game/
├── dragonlance-project-reference.md   documento vivo — AGGIORNATO (STATO ATTUALE, §2,§3,§4,§5,§5.1,§7)
├── stato-lavoro-cowork.md             questo file
├── RIPRENDERE-DA-QUI.md               nota di ripresa (parzialmente superata)
├── manuali-mancanti.md                12 manuali da procurare
├── LEGGIMI-estrazione.md              pipeline, difetti trovati, istruzioni
├── inventario_manuali.tsv             triage iniziale (preesistente)
├── ocr_queue.txt                      22 scansioni, dalla più leggera
│
├── colstep.py                ri-estrazione a colonne — CORRETTO (gutter + raddoppi)
├── ocrstep.py                OCR incrementale (preesistente)
├── controlla_testi.py        cerca le pagine con colonne fuse
├── importa_ocr.py            importa l'OCR + AGGIUNTO controllo di qualità
├── indicizza.py              rigenera Testi/indice.json e ocr_queue.txt
│
├── Manuali/                  140 PDF (122 + 18 nuovi in "D&D 5e/")
├── Estratti/                 vecchia estrazione a colonne fuse — SOLO STORICO
├── Testi/                    100 .txt a colonne separate + indice.json
│   └── Dragonlance/ 38   Core/ 30   3.0_3.5/ 32
│
└── dati/
    ├── LEGGIMI.md            cosa contengono, verifica fatta, questioni aperte
    ├── schema/               razza.schema.json, classe.schema.json, divinita.schema.json
    ├── build_razze.py        sorgente di verità — ora genera anche mechanics_5e
    ├── build_classi.py       idem
    ├── build_divinita.py     idem
    ├── valida.py             razze — regola sulle note di fonte aggiornata
    ├── valida_classi.py      classi + incrocio con le razze
    ├── valida_divinita.py    divinità + incrocio con le classi
    ├── razze/ 15   classi/ 17   divinita/ 21     JSON generati
    ├── *.index.json          tre indici
    └── _fonti/               estrattori e tabelle parsate (progressioni, incantesimi, divinità)
```

Validazione: **15 razze, 17 classi, 21 divinità — zero errori**, nessuna contraddizione fra le tabelle incrociate.

---

## 3. Deviazioni dal documento di riferimento

**Nessuna deviazione.** Le cinque decisioni ricevute sono state applicate alla lettera e recepite nel documento. Due aggiunte non richieste, entrambe difensive:

1. **Controllo di qualità in `importa_ocr.py`** — non era previsto, ma senza di esso due manuali sarebbero rimasti illeggibili nella libreria (`PsionicsHandbook` allo 0,3%). Confronta la percentuale di parole inglesi riconosciute e preferisce l'OCR quando il testo estratto è spazzatura.

2. **`sdoppia()` in `colstep.py`** — correzione dei caratteri raddoppiati a valle dell'estrazione, perché `dedupe_chars` non copre il caso dei glifi con scarto reale.

---

## 4. Domande aperte

### Richiedono una tua decisione

1. **Il PHB 5e 2014 non è fra i PDF.** La cartella `D&D 5e/` contiene solo edizioni **2024** dei core (PHB, DMG, Monster Manual), che la decisione 1 ha escluso. Tre strade:
   - usare **`2014.5e.tools`** come metro di conversione — i dati sono JSON strutturato, più affidabili e comodi dei PDF, e non richiedono estrazione;
   - procurarsi i PDF 2014;
   - riconsiderare la decisione 1 alla luce di ciò che è effettivamente disponibile.

   *Raccomandazione*: la prima. Convertire da JSON già strutturato elimina in blocco la classe di problemi che abbiamo appena passato due giorni a inseguire.

2. **Le 193 pagine ancora segnalate come sospette** (1,6%). Alcune sono falsi positivi (tabelle, impaginati a colonna singola). Vale la pena passarle a mano o si accetta il livello attuale? Nessuna cade nei capitoli già estratti in `dati/`.

3. **Il Barbaro ha doppia natura**: il manuale lo tratta sia come cultura umana (capitolo *People of Ansalon*) sia come classe (*Classes of Ansalon*). Ora esiste come entrambi nei dati. Da decidere come modellarlo nel wizard di creazione.

### Ambiguità delle fonti, registrate e non risolte

Tracciate nei campi `open_questions` dei rispettivi JSON. Come richiesto, non toccate.

4. **Resistenza magica dei kender** — «+1 ogni 3½ punti di Costituzione»: il manuale non dice se arrotondare per difetto o interpolare.
5. **Cavaliere della Rosa e incantesimi** — non è detto se conservi quelli acquisiti come Cavaliere della Spada.
6. **Reorx** — unica divinità che dichiara `WAL` invece di `PAL`. Verificato: non è un errore di trascrizione.
7. **Ricchezza iniziale del Cavaliere** — verificata sull'immagine: il manuale stampa «564x10 stl», refuso tipografico dell'originale. Ricostruito `5d4x10` dalla regola base del gruppo Warrior. Resta l'unico valore del dataset dedotto anziché letto.
8. **Tabella incantesimi dei Cavalieri della Spada** — disallineata in stampa ai livelli 9, 14 e 15. Letta da sinistra a destra; coerente con le righe adiacenti e monotona.
9. **Etnie umane di Krynn** — nessuna statistica distinta in questo manuale. Restano differenze narrative finché non arriva *Races of Ansalon*.
