Spazio di ricerca: 720 permutazioni dell'array standard. 191.587 combinazioni point-buy entro 27 punti.

| razza | array std | point-buy | verdetto |
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
| Nano Sozzo (Aghar) |   0/720 |   2560/191587 | **solo point-buy** |
| Nano delle Colline (Neidar) | 216/720 |  40811/191587 | libera |
| Nano delle Montagne (Hylar / Daewa | 480/720 | 106914/191587 | libera |
| Barbaro | 384/720 |  54715/191587 | libera |
| Umano | 720/720 | 191587/191587 | libera |


## Combinazioni razza+classe matematicamente impossibili

- **Elfo Dargonesti (Elfo degli Abissi)** + `cavaliere` — la classe richiede STR 15, DEX 15, CON 15, INT 10, WIS 10
- **Elfo Dimernesti (Elfo dei Bassifondi)** + `cavaliere` — la classe richiede STR 15, DEX 15, CON 15, INT 10, WIS 10
- **Irda (Alto Ogre)** + `cavaliere` — la classe richiede STR 15, DEX 15, CON 15, INT 10, WIS 10
- **Nano delle Montagne (Hylar / Daewar)** + `cavaliere` — la classe richiede STR 15, DEX 15, CON 15, INT 10, WIS 10
- **Barbaro** + `cavaliere` — la classe richiede STR 15, DEX 15, CON 15, INT 10, WIS 10
- **Umano** + `cavaliere-rosa` — la classe richiede STR 15, DEX 12, CON 15, INT 10, WIS 13
- **Umano** + `cavaliere` — la classe richiede STR 15, DEX 15, CON 15, INT 10, WIS 10


## Difficolta' per classe (a prescindere dalla razza)

Quante razze possono accedere a ciascuna classe, fra quelle a cui la tabella del manuale la concede.

| classe | requisiti | razze ammesse | di cui raggiungibili |
|---|---|---:|---:|
| `barbaro` | STR10 DEX8 CON12 WIS8 | 8 | 8 |
| `cavaliere` | STR15 DEX15 CON15 INT10 WIS10 | 6 | 0 ⚠ |
| `cavaliere-corona` | STR10 DEX8 CON10 INT7 WIS10 | 2 | 2 |
| `cavaliere-rosa` | STR15 DEX12 CON15 INT10 WIS13 | 2 | 1 ⚠ |
| `cavaliere-spada` | STR12 DEX9 CON10 INT9 WIS13 | 2 | 2 |
| `con-artist` | CHA12 | 3 | 3 |
| `mago-alta-stregoneria` | INT9 | 3 | 3 |
| `mago-rinnegato` | INT9 | 3 | 3 |
| `mago-veste-bianca` | INT9 | 3 | 3 |
| `mago-veste-nera` | INT9 | 3 | 3 |
| `mago-veste-rossa` | INT9 | 3 | 3 |
| `mariner` | STR12 DEX11 | 6 | 6 |
| `sacerdote-eretico` | WIS9 | 3 | 3 |
| `sacerdote-ordini-sacri` | WIS9 | 3 | 3 |


## Dettaglio per razza

### Elfo Dargonesti (Elfo degli Abissi) (`elfo-dargonesti`)
- minimi: {'str': 3, 'dex': 10, 'con': 3, 'int': 8, 'wis': 8, 'cha': 3}
- massimali: {'str': 18, 'dex': 19, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti: {'str': -1, 'dex': 1}
- distribuzioni valide: 600/720 array standard, 162336/191587 point-buy
- classi piu' vincolate: `barbaro` (216/720), `mariner` (288/720), `con-artist` (384/720), `mago-alta-stregoneria` (480/720)

### Elfo Dimernesti (Elfo dei Bassifondi) (`elfo-dimernesti`)
- minimi: {'str': 3, 'dex': 10, 'con': 3, 'int': 8, 'wis': 8, 'cha': 3}
- massimali: {'str': 18, 'dex': 19, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti: {'str': -1, 'dex': 1}
- distribuzioni valide: 600/720 array standard, 162336/191587 point-buy

### Elfo Kagonesti (`elfo-kagonesti`)
- minimi: {'str': 8, 'dex': 8, 'con': 8, 'int': 3, 'wis': 8, 'cha': 8}
- massimali: {'str': 18, 'dex': 19, 'con': 18, 'int': 12, 'wis': 18, 'cha': 18}
- aggiustamenti: {'str': 1, 'dex': 2, 'con': 1, 'int': -3}
- distribuzioni valide: 720/720 array standard, 191587/191587 point-buy
- classi piu' vincolate: `barbaro` (384/720)

### Elfo Qualinesti (`elfo-qualinesti`)
- minimi: {'str': 7, 'dex': 7, 'con': 7, 'int': 8, 'wis': 6, 'cha': 8}
- massimali: {'str': 18, 'dex': 19, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti: {'dex': 1, 'con': -1}
- distribuzioni valide: 720/720 array standard, 191587/191587 point-buy

### Elfo Silvanesti (`elfo-silvanesti`)
- minimi: {'str': 3, 'dex': 7, 'con': 6, 'int': 10, 'wis': 6, 'cha': 12}
- massimali: {'str': 18, 'dex': 19, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti: {'dex': 1, 'con': -1}
- distribuzioni valide: 384/720 array standard, 54715/191587 point-buy

### Gnomo (Minoi) (`gnomo-minoi`)
- minimi: {'str': 6, 'dex': 8, 'con': 8, 'int': 8, 'wis': 3, 'cha': 3}
- massimali: {'str': 18, 'dex': 18, 'con': 18, 'int': 18, 'wis': 12, 'cha': 18}
- aggiustamenti: {'str': -1, 'dex': 2}
- distribuzioni valide: 360/720 array standard, 134828/191587 point-buy
- classi piu' vincolate: `tinker` (360/720)

### Irda (Alto Ogre) (`irda`)
- minimi: {'str': 12, 'dex': 8, 'con': 12, 'int': 5, 'wis': 10, 'cha': 15}
- massimali: {'str': 18, 'dex': 19, 'con': 15, 'int': 19, 'wis': 18, 'cha': 19}
- aggiustamenti: {'dex': 1, 'con': -3, 'int': 1, 'cha': 1}
- distribuzioni valide: 8/720 array standard, 129/191587 point-buy
- classi piu' vincolate: `mariner` (4/720)

### Kender (`kender`)
- minimi: {'str': 6, 'dex': 8, 'con': 8, 'int': 6, 'wis': 3, 'cha': 6}
- massimali: {'str': 16, 'dex': 19, 'con': 18, 'int': 18, 'wis': 16, 'cha': 18}
- aggiustamenti: {'dex': 1}
- distribuzioni valide: 720/720 array standard, 191587/191587 point-buy
- classi piu' vincolate: `barbaro` (384/720), `handler` (720/720)

### Mezzelfo (`mezzelfo`)
- minimi: {'str': 3, 'dex': 6, 'con': 6, 'int': 4, 'wis': 3, 'cha': 3}
- massimali: {'str': 18, 'dex': 18, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti: {'dex': 2}
- distribuzioni valide: 720/720 array standard, 191587/191587 point-buy
- classi piu' vincolate: `cavaliere-rosa` (0/720), `cavaliere-spada` (108/720), `cavaliere-corona` (360/720), `mariner` (384/720)

### Minotauro (`minotauro`)
- minimi: {'str': 12, 'dex': 8, 'con': 12, 'int': 5, 'wis': 3, 'cha': 3}
- massimali: {'str': 20, 'dex': 18, 'con': 20, 'int': 18, 'wis': 16, 'cha': 16}
- aggiustamenti: {'str': 2, 'con': 2, 'wis': -2, 'cha': -2}
- distribuzioni valide: 480/720 array standard, 92359/191587 point-buy
- classi piu' vincolate: `mariner` (288/720), `barbaro` (360/720)

### Nano Sozzo (Aghar) (`nano-aghar`)
- minimi: {'str': 6, 'dex': 6, 'con': 3, 'int': 3, 'wis': 3, 'cha': 3}
- massimali: {'str': 18, 'dex': 18, 'con': 12, 'int': 9, 'wis': 9, 'cha': 9}
- aggiustamenti: nessuno
- distribuzioni valide: 0/720 array standard, 2560/191587 point-buy
- classi piu' vincolate: `barbaro` (0/720)

### Nano delle Colline (Neidar) (`nano-collina`)
- minimi: {'str': 9, 'dex': 3, 'con': 14, 'int': 3, 'wis': 3, 'cha': 3}
- massimali: {'str': 18, 'dex': 17, 'con': 19, 'int': 18, 'wis': 18, 'cha': 12}
- aggiustamenti: {'con': 1, 'cha': -1}
- distribuzioni valide: 216/720 array standard, 40811/191587 point-buy
- classi piu' vincolate: `barbaro` (216/720)

### Nano delle Montagne (Hylar / Daewar) (`nano-montagna`)
- minimi: {'str': 8, 'dex': 3, 'con': 12, 'int': 3, 'wis': 3, 'cha': 3}
- massimali: {'str': 18, 'dex': 17, 'con': 19, 'int': 18, 'wis': 18, 'cha': 16}
- aggiustamenti: {'con': 1, 'cha': -1}
- distribuzioni valide: 480/720 array standard, 106914/191587 point-buy

### Barbaro (`umano-barbaro`)
- minimi: {'str': 10, 'dex': 8, 'con': 12, 'wis': 8}
- massimali: {'dex': 16, 'int': 18}
- aggiustamenti: nessuno
- distribuzioni valide: 384/720 array standard, 54715/191587 point-buy
- classi piu' vincolate: `mariner` (144/720), `con-artist` (216/720), `mago-alta-stregoneria` (288/720), `mago-rinnegato` (288/720)

### Umano (`umano`)
- minimi: {'str': 3, 'dex': 3, 'con': 3, 'int': 3, 'wis': 3, 'cha': 3}
- massimali: {'str': 18, 'dex': 18, 'con': 18, 'int': 18, 'wis': 18, 'cha': 18}
- aggiustamenti: nessuno
- distribuzioni valide: 720/720 array standard, 191587/191587 point-buy
- classi piu' vincolate: `cavaliere-spada` (54/720), `mariner` (288/720), `cavaliere-corona` (360/720), `barbaro` (384/720)



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

**Tutte le razze, anche quelle senza negativi, per confronto:**

| razza | aggiustamenti | netto | scarto da +3 |
|---|---|---:|---:|
| Elfo Dargonesti (Elfo degli Abissi | DEX +1, STR -1 | +0 | -3 |
| Elfo Dimernesti (Elfo dei Bassifon | DEX +1, STR -1 | +0 | -3 |
| Elfo Qualinesti | CON -1, DEX +1 | +0 | -3 |
| Elfo Silvanesti | CON -1, DEX +1 | +0 | -3 |
| Irda (Alto Ogre) | CHA +1, CON -3, DEX +1, INT +1 | +0 | -3 |
| Minotauro | CHA -2, CON +2, STR +2, WIS -2 | +0 | -3 |
| Nano Sozzo (Aghar) | nessuno | +0 | -3 |
| Nano delle Colline (Neidar) | CHA -1, CON +1 | +0 | -3 |
| Nano delle Montagne (Hylar / Daewa | CHA -1, CON +1 | +0 | -3 |
| Barbaro | nessuno | +0 | -3 |
| Umano | nessuno | +0 | -3 |
| Elfo Kagonesti | CON +1, DEX +2, INT -3, STR +1 | +1 | -2 |
| Gnomo (Minoi) | DEX +2, STR -1 | +1 | -2 |
| Kender | DEX +1 | +1 | -2 |
| Mezzelfo | DEX +2 | +2 | -1 |


---

# COMPITO C — il Barbaro: proposta, non decisione

## Il nodo

La doppia natura e' gia' modellata: esistono sia la razza `umano-barbaro` sia la
classe `barbaro`. Resta da decidere quale set di vincoli valga, perche' i due
non coincidono:

| | STR | DEX | CON | INT | WIS |
|---|---|---|---|---|---|
| scheda razziale (*People of Ansalon*) | min 10 | min 8, **max 16** | min 12 | **max 18** | min 8 |
| voce di classe (*Classes of Ansalon*) | min 10 | min 8 | min 12 | — | min 8 |

I minimi coincidono. La differenza sta tutta nei **due massimali** che solo la
scheda razziale riporta.

## Il dato che cambia la domanda

**I due massimali non hanno alcun effetto alla creazione del personaggio.**

Verificato programmaticamente: con o senza massimali, le disposizioni valide
dell'array standard sono **384 su 720**, identiche. Il motivo e' aritmetico:
l'array standard arriva a 15 e il point-buy pure, mentre i tetti sono 16 e 18.
Nessuno dei due puo' essere raggiunto, quindi nessuno dei due puo' vincolare.

I massimali mordono **solo durante l'avanzamento**, quando gli aumenti di
caratteristica portano un punteggio oltre 16. Non sono un requisito d'accesso:
sono un **tetto alla crescita**.

## Perche' questo e' dirimente

Un tetto alla crescita e' esattamente la categoria di meccanica che la
**decisione 3** ha gia' respinto per i limiti di livello, con tre motivazioni
che valgono identiche qui:

1. e' la meccanica 2e piu' universalmente abbandonata dalle edizioni successive;
2. blocca le campagne lunghe;
3. contraddice il principio fissato per i Cavalieri — potere sempre monotono
   crescente, mai regressioni ne' tetti.

Applicare DEX max 16 significherebbe che un barbaro umano resta per sempre a
+3 di modificatore di Destrezza, mentre qualunque altro umano arriva a +5.
Su venti livelli e' una penalita' concreta, e sarebbe l'unica razza umana a
subirla.

## Proposta

**Far valere i vincoli della voce di classe, scartando i due massimali della
scheda razziale.** In concreto: `umano-barbaro` conserva i minimi (STR 10,
CON 12, WIS 8, DEX 8) e le abilita' speciali culturali, ma non i tetti.

Motivazione in una riga: i massimali sono tetti di crescita travestiti da
requisiti d'accesso, e la decisione 3 ha gia' stabilito che i tetti di crescita
non si applicano.

## Variante da considerare

Se l'obiettivo e' conservare il sapore culturale senza incoerenze meccaniche,
si puo' andare oltre: modellare `umano-barbaro` come **background** anziche'
come razza. Le sue abilita' speciali — competenza in Sopravvivenza nel clima
natio, affaticamento fuori dalla regione d'origine, bonus a Caccia e
Seguire Tracce — sono gia' oggi di forma tipicamente da background, non da
tratto razziale. L'umano resterebbe uno solo, numericamente coerente, e la
cultura barbarica diventerebbe una scelta ortogonale, combinabile anche con
classi diverse dal barbaro.

Questa strada risolve la duplicazione invece di arbitrarla, ma esce dallo
schema attuale (non esiste ancora un'entita' "background") e va quindi decisa
insieme allo schema Personaggio.

**La decisione resta tua.**
