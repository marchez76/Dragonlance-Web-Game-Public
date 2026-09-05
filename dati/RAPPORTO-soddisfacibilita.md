Spazio di ricerca: 720 permutazioni dell'array standard, 191.587 combinazioni di acquisto a punti entro 27 punti.

Le coppie razza+classe aperte dal telaio e lasciate passare dal filtro (decisione 58 (`telaio-apre-classe-filtra`)) sono **126**, su 15 razze e 20 classi. Sono quelle che questo rapporto misura: le classi che il telaio non apre non compaiono, perche' non sono state escluse — non sono state proposte.

| razza | array std | acquisto a punti | verdetto |
|---|---:|---:|---|
| Elfo Dargonesti (Elfo degli Abissi | 600/720 | 162336/191587 | libera |
| Elfo Dimernesti (Elfo dei Bassifon | 600/720 | 162336/191587 | libera |
| Elfo Kagonesti | 720/720 | 191587/191587 | libera |
| Elfo Qualinesti | 720/720 | 191587/191587 | libera |
| Elfo Silvanesti | 384/720 |  54715/191587 | libera |
| Gnomo (Minoi) | 360/720 | 134828/191587 | libera |
| Irda (Alto Ogre) |   8/720 |    129/191587 | molto vincolata |
| Kender | 720/720 | 191587/191587 | libera |
| Mezzelfo | 720/720 | 191587/191587 | libera |
| Minotauro | 480/720 |  92359/191587 | libera |
| Nano Sozzo (Aghar) |   0/720 |   2560/191587 | **dadi propri del manuale** |
| Nano delle Colline (Neidar) | 216/720 |  40811/191587 | libera |
| Nano delle Montagne (Hylar / Daewa | 480/720 | 106914/191587 | libera |
| Barbaro | 384/720 |  89543/191587 | libera |
| Umano | 720/720 | 191587/191587 | libera |


## Il metodo di generazione e' il terzo filtro

Il filtro di decisione 58 (`telaio-apre-classe-filtra`) confronta il minimo di classe con il MASSIMALE RAZZIALE, cioe' con il teoricamente raggiungibile. Non con cio' che il metodo scelto sa produrre: l'array standard e l'acquisto a punti si fermano a 15 pre-razziale, il tiro arriva a 18. Le coppie qui sotto passano i primi due filtri e restano comunque irraggiungibili con quel metodo.

Le coppie con una scelta di metodo da fare sono **122**; le altre **4** appartengono a razze per cui il manuale prescrive sei formule di dado, dove non c'e' nessun metodo da scegliere. Restano fuori dal conto.

| metodo | coppie precluse | su | classi coinvolte |
|---|---:|---:|---|
| `tiro-4d6-scarta-minore` | 0 | 122 | — |
| `array-standard` | 19 | 122 | `cavaliere`, `paladino` |
| `punti-acquisto` | 16 | 122 | `cavaliere`, `paladino` |

**16 coppie su 122 non sono raggiungibili con nessuno dei due metodi senza dadi**, e appartengono a 2 classi soltanto:

| classe | coppie irraggiungibili | coppie aperte | resta |
|---|---:|---:|---|
| `cavaliere` | 10 | 14 | 10 su 14, e resta solo il tiro |
| `paladino` | 6 | 6 | **tutta la classe**, e resta solo il tiro |

Non e' un difetto: e' decisione 8 (`generazione-caratteristiche`) che si manifesta. Era scritto che l'acquisto a punti non sa esprimere la rarita' — appiattisce tutti sullo stesso budget — quindi cio' che in 2e era raro diventa impossibile. Era una previsione; questa e' la misura.

Le coppie, una per una:

- **Barbaro** + `paladino`
- **Elfo Dargonesti (Elfo degli Abissi)** + `cavaliere`
- **Elfo Dargonesti (Elfo degli Abissi)** + `paladino`
- **Elfo Dimernesti (Elfo dei Bassifondi)** + `cavaliere`
- **Elfo Qualinesti** + `cavaliere`
- **Elfo Silvanesti** + `cavaliere`
- **Elfo Silvanesti** + `paladino`
- **Gnomo (Minoi)** + `cavaliere`
- **Irda (Alto Ogre)** + `cavaliere`
- **Irda (Alto Ogre)** + `paladino`
- **Kender** + `cavaliere`
- **Mezzelfo** + `paladino`
- **Nano delle Colline (Neidar)** + `cavaliere`
- **Nano delle Montagne (Hylar / Daewar)** + `cavaliere`
- **Umano** + `cavaliere`
- **Umano** + `paladino`


## Difficolta' per classe

Quante razze arrivano a ciascuna classe, fra quelle a cui il telaio la apre, e con quanti metodi. La colonna «dadi propri» tiene a parte le razze che non scelgono un metodo: senza di essa comparirebbero come precluse da tutti e tre.

| classe | requisiti | razze aperte | passano il filtro | dadi propri | con array | con acquisto |
|---|---|---:|---:|---:|---:|---:|
| `barbaro` | CON12 DEX8 STR10 WIS8 | 15 | 15 | 1 | 14/14 | 14/14 |
| `cavaliere` | CON15 DEX15 INT10 STR15 WIS10 | 15 | 14 | 0 | 1/14 ⚠ | 4/14 |
| `cavaliere-corona` | CON10 DEX8 INT7 STR10 WIS10 | 15 | 2 | 0 | 2/2 | 2/2 |
| `cavaliere-rosa` | CON15 DEX12 INT10 STR15 WIS13 | 6 | 0 | 0 | 0/0 | 0/0 |
| `cavaliere-spada` | CON10 DEX9 INT9 STR12 WIS13 | 6 | 0 | 0 | 0/0 | 0/0 |
| `commoner` | — | 3 | 3 | 0 | 3/3 | 3/3 |
| `con-artist` | CHA12 | 12 | 11 | 0 | 11/11 | 11/11 |
| `guerriero` | STR9 | 15 | 15 | 1 | 14/14 | 14/14 |
| `handler` | — | 4 | 1 | 0 | 1/1 | 1/1 |
| `ladro` | DEX9 | 12 | 12 | 1 | 11/11 | 11/11 |
| `mago-alta-stregoneria` | INT9 | 10 | 10 | 0 | 10/10 | 10/10 |
| `mago-rinnegato` | INT9 | 10 | 10 | 0 | 10/10 | 10/10 |
| `mago-veste-bianca` | INT9 | 3 | 0 | 0 | 0/0 | 0/0 |
| `mago-veste-nera` | INT9 | 3 | 0 | 0 | 0/0 | 0/0 |
| `mago-veste-rossa` | INT9 | 3 | 0 | 0 | 0/0 | 0/0 |
| `mariner` | DEX11 STR12 | 6 | 6 | 0 | 6/6 | 6/6 |
| `paladino` | CHA17 CON9 STR12 WIS13 | 6 | 6 | 0 | 0/6 ⚠ | 0/6 |
| `sacerdote-eretico` | WIS9 | 5 | 5 | 0 | 5/5 | 5/5 |
| `sacerdote-ordini-sacri` | WIS9 | 15 | 15 | 1 | 14/14 | 14/14 |
| `tinker` | — | 4 | 1 | 0 | 1/1 | 1/1 |


## Dettaglio per razza

### Elfo Dargonesti (Elfo degli Abissi) (`elfo-dargonesti`)
- minimi: {'dex': 10, 'int': 8, 'wis': 8}
- massimali: {'str': 18, 'dex': 19, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti applicati: {'str': -1, 'dex': 1}
- distribuzioni valide: 600/720 array standard, 162336/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `paladino` (0/720), `barbaro` (216/720), `mariner` (288/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza), `cavaliere-rosa` (ingresso), `cavaliere-spada` (ingresso), `handler` (razza), `mago-veste-bianca` (ingresso), `mago-veste-nera` (ingresso), `mago-veste-rossa` (ingresso), `tinker` (razza)

### Elfo Dimernesti (Elfo dei Bassifondi) (`elfo-dimernesti`)
- minimi: {'dex': 10, 'int': 8, 'wis': 8}
- massimali: {'str': 18, 'dex': 19, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti applicati: {'str': -1, 'dex': 1}
- distribuzioni valide: 600/720 array standard, 162336/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `barbaro` (216/720), `guerriero` (480/720), `mago-alta-stregoneria` (480/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza)

### Elfo Kagonesti (`elfo-kagonesti`)
- minimi: {'str': 8, 'dex': 8, 'con': 8, 'wis': 8, 'cha': 8}
- massimali: {'str': 18, 'dex': 19, 'con': 18, 'int': 12, 'wis': 18, 'cha': 18}
- aggiustamenti applicati: {'str': 1, 'con': 1, 'dex': 2, 'int': -3}
- distribuzioni valide: 720/720 array standard, 191587/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `barbaro` (384/720), `con-artist` (480/720), `sacerdote-ordini-sacri` (600/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza)

### Elfo Qualinesti (`elfo-qualinesti`)
- minimi: {'str': 7, 'dex': 7, 'con': 7, 'int': 8, 'wis': 6, 'cha': 8}
- massimali: {'str': 18, 'dex': 19, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti applicati: {'dex': 1, 'con': -1}
- distribuzioni valide: 720/720 array standard, 191587/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `barbaro` (288/720), `con-artist` (480/720), `guerriero` (600/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza)

### Elfo Silvanesti (`elfo-silvanesti`)
- minimi: {'dex': 7, 'con': 6, 'int': 10, 'wis': 6, 'cha': 12}
- massimali: {'str': 18, 'dex': 19, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti applicati: {'dex': 1, 'con': -1}
- distribuzioni valide: 384/720 array standard, 54715/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `paladino` (0/720), `barbaro` (108/720), `guerriero` (288/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza), `cavaliere-rosa` (ingresso), `cavaliere-spada` (ingresso)

### Gnomo (Minoi) (`gnomo-minoi`)
- minimi: {'str': 6, 'dex': 8, 'con': 8, 'int': 8}
- massimali: {'str': 18, 'dex': 18, 'con': 18, 'int': 18, 'wis': 12, 'cha': 18}
- aggiustamenti applicati: {'str': -1, 'dex': 2}
- distribuzioni valide: 360/720 array standard, 134828/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `barbaro` (180/720), `sacerdote-ordini-sacri` (240/720), `con-artist` (264/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza)

### Irda (Alto Ogre) (`irda`)
- minimi: {'str': 12, 'dex': 8, 'con': 12, 'int': 5, 'wis': 10, 'cha': 15}
- massimali: {'str': 18, 'dex': 19, 'con': 15, 'int': 19, 'wis': 18, 'cha': 19}
- aggiustamenti applicati: {'con': -3, 'dex': 1, 'int': 1, 'cha': 1}
- distribuzioni valide: 8/720 array standard, 129/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `paladino` (0/720), `mariner` (4/720), `barbaro` (8/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza), `cavaliere-rosa` (ingresso), `cavaliere-spada` (ingresso)

### Kender (`kender`)
- minimi: {'str': 6, 'dex': 8, 'con': 8, 'int': 6, 'cha': 6}
- massimali: {'str': 16, 'dex': 19, 'con': 18, 'int': 18, 'wis': 16, 'cha': 18}
- aggiustamenti applicati: {'dex': 1}
- formule proprie del manuale: {'str': '2d6+4'}
- distribuzioni valide: 720/720 array standard, 191587/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `barbaro` (384/720), `con-artist` (480/720), `guerriero` (600/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza)

### Mezzelfo (`mezzelfo`)
- minimi: {'dex': 6, 'con': 6, 'int': 4}
- massimali: {'str': 18, 'dex': 18, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti applicati: {'dex': 2}
- distribuzioni valide: 720/720 array standard, 191587/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `paladino` (0/720), `cavaliere-corona` (360/720), `barbaro` (384/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-rosa` (ingresso), `cavaliere-spada` (ingresso)

### Minotauro (`minotauro`)
- minimi: {'str': 12, 'dex': 8, 'con': 12, 'int': 5}
- massimali: {'str': 20, 'dex': 18, 'con': 20, 'int': 18, 'wis': 16, 'cha': 16}
- aggiustamenti applicati: {'str': 2, 'con': 2, 'wis': -2, 'cha': -2}
- distribuzioni valide: 480/720 array standard, 92359/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (2/720), `mariner` (288/720), `sacerdote-ordini-sacri` (288/720), `barbaro` (360/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza)

### Nano Sozzo (Aghar) (`nano-aghar`)
- minimi: {'str': 6, 'dex': 6}
- massimali: {'str': 18, 'dex': 18, 'con': 12, 'int': 9, 'wis': 9, 'cha': 9}
- aggiustamenti applicati: nessuno
- formule proprie del manuale: {'str': '4d4+2', 'dex': '4d4+2', 'con': '3d4', 'int': '2d4+1', 'wis': '2d4+1', 'cha': '2d4+1'}
- distribuzioni valide: 0/720 array standard, 2560/191587 acquisto a punti
- classi piu' vincolate: `barbaro` (0/720), `guerriero` (0/720), `ladro` (0/720), `sacerdote-ordini-sacri` (0/720)
- aperte dal telaio e tolte dal filtro: `cavaliere` (caratteristica), `cavaliere-corona` (razza), `con-artist` (caratteristica)

### Nano delle Colline (Neidar) (`nano-collina`)
- minimi: {'str': 9, 'con': 14}
- massimali: {'str': 18, 'dex': 17, 'con': 19, 'int': 18, 'wis': 18, 'cha': 12}
- aggiustamenti applicati: {'con': 1, 'cha': -1}
- distribuzioni valide: 216/720 array standard, 40811/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `con-artist` (36/720), `ladro` (168/720), `sacerdote-ordini-sacri` (168/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza)

### Nano delle Montagne (Hylar / Daewar) (`nano-montagna`)
- minimi: {'str': 8, 'con': 12}
- massimali: {'str': 18, 'dex': 17, 'con': 19, 'int': 18, 'wis': 18, 'cha': 16}
- aggiustamenti applicati: {'con': 1, 'cha': -1}
- distribuzioni valide: 480/720 array standard, 106914/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `con-artist` (216/720), `barbaro` (384/720), `guerriero` (384/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza)

### Barbaro (`umano-barbaro`)
- minimi: {'str': 10, 'dex': 8, 'con': 12, 'wis': 8}
- massimali: {'dex': 16, 'int': 18}
- aggiustamenti applicati: {'str': 1, 'con': 1}
- distribuzioni valide: 384/720 array standard, 89543/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `paladino` (0/720), `mariner` (144/720), `con-artist` (216/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-corona` (razza), `cavaliere-rosa` (ingresso), `cavaliere-spada` (ingresso), `handler` (razza), `mago-veste-bianca` (ingresso), `mago-veste-nera` (ingresso), `mago-veste-rossa` (ingresso), `tinker` (razza)

### Umano (`umano`)
- minimi: nessuno
- massimali: {'str': 18, 'dex': 18, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti applicati: nessuno
- distribuzioni valide: 720/720 array standard, 191587/191587 acquisto a punti
- classi piu' vincolate: `cavaliere` (0/720), `paladino` (0/720), `mariner` (288/720), `cavaliere-corona` (360/720)
- aperte dal telaio e tolte dal filtro: `cavaliere-rosa` (ingresso), `cavaliere-spada` (ingresso), `handler` (razza), `mago-veste-bianca` (ingresso), `mago-veste-nera` (ingresso), `mago-veste-rossa` (ingresso), `tinker` (razza)



## I due strati a confronto

`verifica_strati.py` confronta 15 razze e 20 classi sulle stesse grandezze che questo rapporto usa: vincoli, massimali, aggiustamenti, formule, minimi di classe. Scarti dichiarati: **4**. Divergenze non dichiarate: **0**.

Gli scarti dichiarati sono la ragione per cui questo rapporto legge lo strato 5e e non la fonte: letti da `source_2e` varrebbero zero, e sparirebbero dal conto senza che nulla lo segnali.

| entita' | grandezza | scarto |
|---|---|---|
| umano-barbaro | aggiustamento editoriale | con +1, str +1 |
| con-artist | dado vita dal chassis | fonte 1d6 -> 1d8 |
| mago-alta-stregoneria | dado vita dal chassis | fonte 1d4 -> 1d6 |
| mago-rinnegato | dado vita dal chassis | fonte 1d4 -> 1d6 |

Controllo interno: «zero disposizioni» e «metodo non praticabile» sono la stessa cosa detta da due funzioni diverse — il conteggio di questo file e `metodi_praticabili()` del motore. Coppie confrontate: 122. Disaccordi: **0**.


# COMPITO B — aggiustamenti negativi

In 5e 2014 le razze hanno solo bonus positivi, per un totale che si aggira su **+3**. Gli aggiustamenti negativi della 2e non hanno equivalente.

| razza | negativi | massimale sulla stessa caratteristica | doppia penalita' | positivi | netto | scarto da +3 |
|---|---|---|---|---:|---:|---:|
| Elfo Dargonesti (Elfo degli Ab | STR -1 | — | no | DEX +1 | +0 | -3 |
| Elfo Dimernesti (Elfo dei Bass | STR -1 | — | no | DEX +1 | +0 | -3 |
| Elfo Kagonesti | INT -3 | INT max 12 | INT | CON +1, DEX +2, STR +1 | +1 | -2 |
| Elfo Qualinesti | CON -1 | — | no | DEX +1 | +0 | -3 |
| Elfo Silvanesti | CON -1 | — | no | DEX +1 | +0 | -3 |
| Gnomo (Minoi) | STR -1 | — | no | DEX +2 | +1 | -2 |
| Irda (Alto Ogre) | CON -3 | CON max 15 | CON | CHA +1, DEX +1, INT +1 | +0 | -3 |
| Minotauro | CHA -2, WIS -2 | CHA max 16, WIS max 16 | CHA, WIS | CON +2, STR +2 | +0 | -3 |
| Nano delle Colline (Neidar) | CHA -1 | CHA max 12 | CHA | CON +1 | +0 | -3 |
| Nano delle Montagne (Hylar / D | CHA -1 | CHA max 16 | CHA | CON +1 | +0 | -3 |

**Tutte le razze, anche quelle senza negativi, e i due strati accanto:**

| razza | applicati (`mechanics_5e`) | netto | dichiarati (`source_2e`) | netto | scarto fra gli strati |
|---|---|---:|---|---:|---|
| Elfo Dargonesti (Elfo degli Abissi | DEX +1, STR -1 | +0 | DEX +1, STR -1 | +0 | — |
| Elfo Dimernesti (Elfo dei Bassifon | DEX +1, STR -1 | +0 | DEX +1, STR -1 | +0 | — |
| Elfo Qualinesti | CON -1, DEX +1 | +0 | CON -1, DEX +1 | +0 | — |
| Elfo Silvanesti | CON -1, DEX +1 | +0 | CON -1, DEX +1 | +0 | — |
| Irda (Alto Ogre) | CHA +1, CON -3, DEX +1, INT +1 | +0 | CHA +1, CON -3, DEX +1, INT +1 | +0 | — |
| Minotauro | CHA -2, CON +2, STR +2, WIS -2 | +0 | CHA -2, CON +2, STR +2, WIS -2 | +0 | — |
| Nano Sozzo (Aghar) | nessuno | +0 | nessuno | +0 | — |
| Nano delle Colline (Neidar) | CHA -1, CON +1 | +0 | CHA -1, CON +1 | +0 | — |
| Nano delle Montagne (Hylar / Daewa | CHA -1, CON +1 | +0 | CHA -1, CON +1 | +0 | — |
| Umano | nessuno | +0 | nessuno | +0 | — |
| Elfo Kagonesti | CON +1, DEX +2, INT -3, STR +1 | +1 | CON +1, DEX +2, INT -3, STR +1 | +1 | — |
| Gnomo (Minoi) | DEX +2, STR -1 | +1 | DEX +2, STR -1 | +1 | — |
| Kender | DEX +1 | +1 | DEX +1 | +1 | — |
| Mezzelfo | DEX +2 | +2 | DEX +2 | +2 | — |
| Barbaro | CON +1, STR +1 | +2 | nessuno | +0 | CON +1, STR +1 |
