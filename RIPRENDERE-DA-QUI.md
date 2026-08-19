# Riprendere da qui — 11 agosto 2026, sera

## Fatto oggi

**Dati strutturati** (`dati/`), tutti validati a zero errori:

- 15 razze, 17 classi, 21 divinità — da *Tales of the Lance* (AD&D 2e)
- schema a doppio strato: `source_2e` fedele al manuale, `mechanics_5e` ancora
  `null` in attesa del PHB 5e
- validatori con controllo incrociato: razze↔classi, divinità↔classi

**Libreria** (`Testi/`): 100 manuali su 122 estratti a colonne separate,
14.199 pagine.

## Da fare per primo, domani

### 1. Ri-macinare la libreria — è la cosa che blocca il resto

La prima passata aveva due difetti scoperti dopo averla completata (dettagli
in `LEGGIMI-estrazione.md`): 1.116 pagine con colonne ancora fuse e 7.075
sequenze di lettere raddoppiate. **Entrambi corretti in `colstep.py`**, ma
solo *Tales of the Lance* è stato rifatto con la versione buona.

```bash
rm -rf Testi .colstep_state
python3 colstep.py 39          # ripetere ~70 volte (45 s max per chiamata)
python3 controlla_testi.py     # deve dire zero
python3 importa_ocr.py && python3 indicizza.py
```

Nota: `Testi/Dragonlance/Tales of the Lance.txt` è già corretto, ma tanto vale
rifare tutto da pulito.

### 2. Poi, in ordine di utilità

- **Compilare `mechanics_5e`** per razze, classi e divinità — appena arriva il
  PHB 5e. Prima però va deciso **2014 o 2024**: la 2024 sposta i bonus di
  caratteristica dalla specie al background, il che semplifica molto le razze
  di Krynn.
- **Schema Personaggio**: lega razza + classe + divinità. È il pezzo che manca
  per far girare il wizard di creazione.
- Restano da estrarre: incantesimi, mostri, oggetti.

## Domande aperte che aspettano una tua decisione

1. **PHB 5e 2014 o 2024** — vedi sopra.
2. **Requisiti di caratteristica come vincolo di classe.** In 2e le restrizioni
   sono codificate nei numeri: i Kagonesti hanno Int massima 12 e infatti non
   hanno classi da mago; i minotauri non hanno classi da ladro. Da decidere se
   in 5e replicare questo o lasciarlo alla narrazione.
3. **Cavaliere della Rosa e incantesimi** — il manuale non dice se conservi
   quelli acquisiti come Cavaliere della Spada.

## Manuali da procurare

`manuali-mancanti.md`. I tre bloccanti: **PHB 5e**, **Shadow of the Dragon
Queen**, **Monster Manual 5e**. Il migliore fra i Dragonlance: **Races of
Ansalon**. A costo zero: **Raistlin's Guide to Krynn** (PDF gratuito su EN
World) e il **Dragonlance Nexus**.

## Mappa dei file

```
dragonlance-project-reference.md   documento vivo di design
manuali-mancanti.md                lista di recupero
LEGGIMI-estrazione.md              pipeline di estrazione e suoi difetti
dati/LEGGIMI.md                    dati strutturati, cosa contengono
colstep.py  ocrstep.py             i due motori, incrementali
controlla_testi.py                 controllo qualità dei testi
indicizza.py  importa_ocr.py       manutenzione dell'indice
```
