# `allowed_classes` risolto — dal telaio alle classi, razza per razza

*Generato da `dati/analizza_allowed_classes.py`. La mappa e la regola stanno
in `dati/_classi_ammesse.py`: qui si applicano e si contano.*

---

## 0. La regola, e cosa produce

La decisione 58 (`telaio-apre-classe-filtra`) risolve le 17 etichette del PHB
2e in due tempi: **il telaio apre l'insieme, i requisiti della classe filtrano
dentro**. Due controlli in sequenza, non uno.

Il conto, in tre numeri: le 15 razze aprono **135 coppie razza+classe**, il
filtro ne toglie **42**, ne restano **93** — una media di **6.2 classi
accessibili per razza** su 17 del roster, 12 delle quali si prendono alla
creazione.

> **Razze con zero classi accessibili: 0**.

La sede e i dati tornano: nessuna etichetta dichiarata e non mappata, nessuna
classe nominata che non esista. Il riscontro dell'euristica non trova
accostamenti che la sede non porti gia' (§2b).

---

## 1. Le due sponde

**17 etichette** distinte, dichiarate dalle razze:

| etichetta 2e | razze che la concedono |
|---|--:|
| `Fighter` | 12 |
| `Holy Orders` | 11 |
| `Thief` | 9 |
| `High Sorcerer` | 6 |
| `Ranger` | 6 |
| `Barbarian` | 5 |
| `Bard` | 5 |
| `Cavalier` | 3 |
| `Mariner` | 3 |
| `Mage (Renegade)` | 2 |
| `Paladin` | 2 |
| `Druid (heathen)` | 2 |
| `Priest (heathen)` | 2 |
| `Illusionist` | 1 |
| `Tinker` | 1 |
| `Handler` | 1 |
| `Knight of Solamnia` | 1 |

**17 classi** nel roster, con il telaio 5e su cui ciascuna sta:

| nostra classe | nome inglese | gruppo | telaio 5e | stato | si entra da |
|---|---|---|---|---|---|
| `barbaro` | Barbarian | Warrior | `Fighter` | clonato | — |
| `cavaliere-corona` | Knight of the Crown | Warrior | `Fighter` | clonato | — |
| `cavaliere-rosa` | Knight of the Rose | Warrior | `Paladin` | clonato | `cavaliere-spada` |
| `cavaliere-spada` | Knight of the Sword | Warrior | `Paladin` | clonato | `cavaliere-corona` |
| `cavaliere` | Cavalier | Warrior | `Fighter` | clonato | — |
| `commoner` | Commoner | Normal | **nessuno** | in_sospeso | — |
| `con-artist` | Con Artist / Prestidigitator | Rogue | `Rogue` | clonato | — |
| `handler` | Handler | Rogue | **nessuno** | in_sospeso | — |
| `mago-alta-stregoneria` | Wizard of High Sorcery | Wizard | `Wizard` | clonato | — |
| `mago-rinnegato` | Renegade Wizard | Wizard | `Wizard` | clonato | — |
| `mago-veste-bianca` | Wizard of the White Robes | Wizard | **nessuno** | in_sospeso | `mago-alta-stregoneria` |
| `mago-veste-nera` | Wizard of the Black Robes | Wizard | **nessuno** | in_sospeso | `mago-alta-stregoneria` |
| `mago-veste-rossa` | Wizard of the Red Robes | Wizard | **nessuno** | in_sospeso | `mago-alta-stregoneria` |
| `mariner` | Mariner | Warrior | **nessuno** | in_sospeso | — |
| `sacerdote-eretico` | Heathen Priest | Priest | **nessuno** | in_sospeso | — |
| `sacerdote-ordini-sacri` | Priest of the Holy Orders of the Stars | Priest | `Cleric` | clonato | — |
| `tinker` | Tinker | Normal | **nessuno** | in_sospeso | — |

I telai trascritti sono 5 — `Cleric`, `Fighter`, `Paladin`, `Rogue`, `Wizard`
— e il roster ne usa 5 (`Cleric`, `Fighter`, `Paladin`, `Rogue`, `Wizard`). 8
nostre classi non hanno un telaio: per loro la decisione 58
(`telaio-apre-classe-filtra`) non cambia niente, perche' il telaio non puo'
aprire cio' su cui nessuno sta. Ci si arriva solo se un'etichetta le nomina. 5
classi non si prendono alla creazione: si entra da un'altra classe.

In coda ci sono 3 telai SRD non ancora trascritti (`Bard`, `Druid`, `Ranger`,
in `_srd51.CODA`): sono lavoro noto, non decisioni aperte — vedi §8.

---

## 2. La mappa, etichetta per etichetta

Due colonne, e non sono la stessa cosa. **Telaio**: editoriale — a quale
chassis 5e corrisponde l'etichetta, con la ragione accanto. **Nomina
direttamente**: di fonte — le nostre classi che l'etichetta nomina per nome o
che il manuale dichiara essere quella classe. Il telaio **si aggiunge** alla
seconda invece di sostituirsi: senza questa clausola l'etichetta `Mariner` non
aprirebbe il Marinaio, che non ha chassis.

| etichetta | razze | telaio | nomina direttamente | apre in tutto |
|---|--:|---|---|---|
| `Barbarian` | 5 | `Fighter` | `barbaro` | `barbaro`, `cavaliere`, `cavaliere-corona` |
| `Bard` | 5 | **nessuno** | — | **niente** |
| `Cavalier` | 3 | `Fighter` | `cavaliere` | `barbaro`, `cavaliere`, `cavaliere-corona` |
| `Druid (heathen)` | 2 | **nessuno** | `sacerdote-eretico` | `sacerdote-eretico` |
| `Fighter` | 12 | `Fighter` | — | `barbaro`, `cavaliere`, `cavaliere-corona` |
| `Handler` | 1 | `Rogue` | `handler` | `con-artist`, `handler` |
| `High Sorcerer` | 6 | `Wizard` | `mago-alta-stregoneria` | `mago-alta-stregoneria`, `mago-rinnegato` |
| `Holy Orders` | 11 | `Cleric` | `sacerdote-ordini-sacri` | `sacerdote-ordini-sacri` |
| `Illusionist` | 1 | `Wizard` | — | `mago-alta-stregoneria`, `mago-rinnegato` |
| `Knight of Solamnia` | 1 | `Paladin` | `cavaliere-corona`, `cavaliere-spada`, `cavaliere-rosa` | `cavaliere-corona`, `cavaliere-rosa`, `cavaliere-spada` |
| `Mage (Renegade)` | 2 | `Wizard` | `mago-rinnegato` | `mago-alta-stregoneria`, `mago-rinnegato` |
| `Mariner` | 3 | `Fighter` | `mariner` | `barbaro`, `cavaliere`, `cavaliere-corona`, `mariner` |
| `Paladin` | 2 | `Paladin` | — | `cavaliere-rosa`, `cavaliere-spada` |
| `Priest (heathen)` | 2 | `Cleric` | `sacerdote-eretico` | `sacerdote-eretico`, `sacerdote-ordini-sacri` |
| `Ranger` | 6 | **nessuno** | — | **niente** |
| `Thief` | 9 | `Rogue` | — | `con-artist` |
| `Tinker` | 1 | **nessuno** | `tinker` | `tinker` |

### Le ragioni, che sono di due tipi e restano distinte

| etichetta | ragione del telaio (editoriale) | ragione delle classi (di fonte) |
|---|---|---|
| `Barbarian` | guerriero senza addestramento cavalleresco; l'Ira e' un'invenzione della 3e, assente da Krynn | il nome inglese del Barbaro coincide con l'etichetta |
| `Bard` | il Bardo SRD esiste nella 5e ma non fra i telai trascritti: in coda | — |
| `Cavalier` | guerriero a cavallo, telaio marziale puro | il nome inglese del Cavaliere coincide con l'etichetta |
| `Druid (heathen)` | nessun telaio, e non serve: l'etichetta e' gia' coperta per nome dal Sacerdote Eretico, che di telaio non ne ha. Il Druido SRD servirebbe solo se il druido eretico risultasse una classe a se' (`_srd51.CODA`) | la scheda del Sacerdote Eretico dichiara gia' di essere entrambe le righe della tabella Class/Race Combinations, `Priest (heathen)` e `Druid (heathen)`; il capitolo delle classi definisce eretico anche il druido che viene da un altro mondo, perche' ignora gli dei della natura di Krynn |
| `Fighter` | e' il telaio, non una classe del nostro roster | — |
| `Handler` | abilita' del ladro applicate al baratto kender | il nome inglese dell'Handler coincide con l'etichetta |
| `High Sorcerer` | incantatore arcano a preparazione | `Wizard of High Sorcery` e' il nome inglese della classe |
| `Holy Orders` | incantatore divino, e' il nome 2e dell'ordine sacerdotale di Krynn | `Priest of the Holy Orders of the Stars` e' il nome inglese della classe; la tabella abbrevia |
| `Illusionist` | specialista arcano: nella 5e e' una sottoclasse del Mago, non una classe | — |
| `Knight of Solamnia` | l'ombrello dei tre ordini cavallereschi; due dei tre stanno su telaio Paladin | etichetta OMBRELLO: la tabella la porta come una riga sola e il capitolo dei Cavalieri di Solamnia descrive tre ordini in sequenza obbligata (decisione 5, `cavalieri-solamnia`). Apre tutti e tre; il filtro dell'ingresso lascia il solo Cavaliere della Corona |
| `Mage (Renegade)` | incantatore arcano fuori dagli Ordini | `Renegade Wizard` e' il nome inglese della classe |
| `Mariner` | guerriero di mare | il nome inglese del Marinaio coincide con l'etichetta. Senza questa riga l'etichetta `Mariner` non aprirebbe il Marinaio, che non ha chassis |
| `Paladin` | e' il telaio, non una classe del nostro roster | — |
| `Priest (heathen)` | incantatore divino fuori dagli Ordini | `Heathen Priest` e' il nome inglese della classe |
| `Ranger` | il Ranger SRD esiste nella 5e ma non fra i telai trascritti: in coda | — |
| `Thief` | e' il telaio, non una classe del nostro roster | — |
| `Tinker` | non ha un telaio 5e: e' un'invenzione di Krynn | il nome inglese del Tinker coincide con l'etichetta |

### 2b. Il riscontro dell'euristica

La prima versione di questo rapporto accostava etichette e classi per
somiglianza: nome uguale, oppure almeno una parola che distingue. Quella
euristica e' rimasta, come **controllo della sede**: cerca cio' che la mappa
scritta a mano potrebbe aver saltato.

Nessun accostamento sfugge alla sede: tutto cio' che l'euristica vede, la
mappa lo porta gia'.

Il verso opposto non e' un errore ed e' la parte interessante: la sede porta
accostamenti che l'euristica **non puo'** vedere, perche' non si reggono sui
nomi. `Knight of Solamnia` non somiglia a nessuno dei tre ordini, e li apre
tutti e tre. Ogni riga di questo tipo porta la propria fonte nella colonna qui
sopra: e' il prezzo di non decidere per somiglianza.

---

## 3. Primo tempo: cosa apre il telaio, e quanto allarga

Il prezzo della lettura per telaio va detto in numeri, non in prosa. Per ogni
classe: quante razze la **nominano** attraverso un'etichetta che la nomina
direttamente, e quante la **raggiungono** dopo che il telaio ha aperto e il
filtro ha stretto.

| nostra classe | telaio | la nominano | l'aprono | la raggiungono | scarto |
|---|---|--:|--:|--:|--:|
| `barbaro` | `Fighter` | 5 | 15 | 15 | +10 |
| `cavaliere-corona` | `Fighter` | 1 | 15 | 2 | +1 |
| `cavaliere-rosa` | `Paladin` | 1 | 6 | 0 | -1 |
| `cavaliere-spada` | `Paladin` | 1 | 6 | 0 | -1 |
| `cavaliere` | `Fighter` | 3 | 15 | 14 | +11 |
| `commoner` | — | 0 | 3 | 3 | +3 |
| `con-artist` | `Rogue` | 0 | 12 | 11 | +11 |
| `handler` | — | 1 | 4 | 1 | 0 |
| `mago-alta-stregoneria` | `Wizard` | 6 | 10 | 10 | +4 |
| `mago-rinnegato` | `Wizard` | 2 | 10 | 10 | +8 |
| `mago-veste-bianca` | — | 0 | 3 | 0 | 0 |
| `mago-veste-nera` | — | 0 | 3 | 0 | 0 |
| `mago-veste-rossa` | — | 0 | 3 | 0 | 0 |
| `mariner` | — | 3 | 6 | 6 | +3 |
| `sacerdote-eretico` | — | 2 | 5 | 5 | +3 |
| `sacerdote-ordini-sacri` | `Cleric` | 11 | 15 | 15 | +4 |
| `tinker` | — | 1 | 4 | 1 | 0 |

Le righe con lo scarto piu' alto sono la decisione 7 (`doppio-strato`) messa
alla prova: dove la fonte era piu' stretta, il telaio allarga, e allargare in
silenzio sarebbe stato il difetto. Le righe con scarto negativo dicono
un'altra cosa ancora: l'etichetta nomina la classe, e il filtro la toglie a
qualcuno che la nominava.

Le tre razze senza elenco (§7) contano come razze che aprono tutto: il loro
contributo alla colonna «l'aprono» non viene da un'etichetta ma dall'assenza
di preclusione.

---

## 4. Secondo tempo: cosa toglie il filtro

| motivo | cosa toglie | coppie razza+classe tolte |
|---|---|--:|
| `razza` | la classe e' riservata ad altre razze | 27 |
| `ingresso` | si entra da un'altra classe, non alla creazione | 21 |
| `caratteristica` | un minimo di classe supera il massimale razziale | 5 |

Il filtro toglie **42 coppie** su 135 aperte. Una coppia puo' essere tolta da
piu' motivi insieme, ed e' il motivo per cui la somma della colonna (53)
supera il numero delle coppie: sapere che una classe e' esclusa due volte e'
diverso dal saperla esclusa una, perche' togliere un vincolo non la
riaprirebbe.

**Due filtri non sono applicati, e non per dimenticanza.** L'*allineamento*:
nessuna razza ne dichiara uno, quindi e' un vincolo sulla scelta del giocatore
e non sulla coppia razza+classe — filtrarlo qui non toglierebbe niente a
nessuno. La *classe sociale*: la fonte la introduce come regola opzionale e
non le ha dato una controparte in `mechanics_5e`, e un filtro su un dato che
vive solo in `source_2e` applicherebbe una regola che non abbiamo adottato.
Entrambi sono scritti in `_classi_ammesse.py`, non solo qui.

---

## 5. La risposta: quante classi per razza, dopo il filtro

| razza | etichette dichiarate | aperte dal telaio | **accessibili** | quali |
|---|--:|--:|--:|---|
| `nano-aghar` | 4 | 5 | **2** | `barbaro`, `sacerdote-ordini-sacri` |
| `elfo-kagonesti` | 6 | 5 | **4** | `barbaro`, `cavaliere`, `con-artist`, `sacerdote-ordini-sacri` |
| `nano-collina` | 5 | 5 | **4** | `barbaro`, `cavaliere`, `con-artist`, `sacerdote-ordini-sacri` |
| `nano-montagna` | 4 | 5 | **4** | `barbaro`, `cavaliere`, `con-artist`, `sacerdote-ordini-sacri` |
| `elfo-dimernesti` | 4 | 6 | **5** | `barbaro`, `cavaliere`, `mago-alta-stregoneria`, `mago-rinnegato`, `sacerdote-ordini-sacri` |
| `elfo-silvanesti` | 6 | 8 | **5** | `barbaro`, `cavaliere`, `mago-alta-stregoneria`, `mago-rinnegato`, `sacerdote-ordini-sacri` |
| `elfo-qualinesti` | 7 | 7 | **6** | `barbaro`, `cavaliere`, `con-artist`, `mago-alta-stregoneria`, `mago-rinnegato`, `sacerdote-ordini-sacri` |
| `kender` | 8 | 7 | **6** | `barbaro`, `cavaliere`, `con-artist`, `handler`, `sacerdote-eretico`, `sacerdote-ordini-sacri` |
| `minotauro` | 5 | 7 | **6** | `barbaro`, `cavaliere`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `sacerdote-ordini-sacri` |
| `gnomo-minoi` | 5 | 8 | **7** | `barbaro`, `cavaliere`, `con-artist`, `mago-alta-stregoneria`, `mago-rinnegato`, `sacerdote-ordini-sacri`, `tinker` |
| `irda` | 7 | 10 | **7** | `barbaro`, `cavaliere`, `con-artist`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `sacerdote-ordini-sacri` |
| `elfo-dargonesti` | *(nessun elenco)* | 17 | **9** | `barbaro`, `cavaliere`, `commoner`, `con-artist`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `sacerdote-eretico`, `sacerdote-ordini-sacri` |
| `mezzelfo` | 11 | 11 | **9** | `barbaro`, `cavaliere`, `cavaliere-corona`, `con-artist`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `sacerdote-eretico`, `sacerdote-ordini-sacri` |
| `umano-barbaro` | *(nessun elenco)* | 17 | **9** | `barbaro`, `cavaliere`, `commoner`, `con-artist`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `sacerdote-eretico`, `sacerdote-ordini-sacri` |
| `umano` | *(nessun elenco)* | 17 | **10** | `barbaro`, `cavaliere`, `cavaliere-corona`, `commoner`, `con-artist`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `sacerdote-eretico`, `sacerdote-ordini-sacri` |

Il numero e' molto piu' basso di quello del telaio — 93 contro 135 — ed e' il
punto: il telaio da solo sarebbe stato una traduzione generosa, la sequenza lo
riporta dentro i vincoli che la fonte scrive sulle classi invece che sulle
razze.

Il minimo e 2 (`nano-aghar`), il massimo 10 (`umano`). **Nessuna razza resta a
zero**: non c'e' nessuna razza ingiocabile.

### 5b. Le etichette dichiarate che non aprono niente

Il conto per razza da solo non dice **quale porta si e' chiusa**: dice un
numero piu' basso. Queste sono le coppie razza+etichetta in cui la razza
dichiara un accesso e non ne ricava nessuna classe. Sono due casi diversi.

**11 coppie: l'etichetta non apre niente perche' il telaio e' in coda.** Bard
e Ranger, gia' contati in §8 come lavoro noto: la razza non ha perso
l'accesso, l'accesso non e' ancora stato scritto.

**3 coppie: l'etichetta apre, e il filtro toglie tutto.** Queste sono la parte
che va guardata, perche' non si smaltiscono battendo a macchina un telaio SRD.

| razza | etichetta | cosa apre | perche' non resta niente |
|---|---|---|---|
| `elfo-silvanesti` | `Paladin` | `cavaliere-rosa`, `cavaliere-spada` | ingresso; razza |
| `irda` | `Paladin` | `cavaliere-rosa`, `cavaliere-spada` | ingresso; razza |
| `nano-aghar` | `Thief` | `con-artist` | caratteristica |

Le due righe `Paladin` dicono la stessa cosa: il telaio Paladin e' trascritto,
ma le uniche nostre classi che ci stanno sopra sono due ordini solamnici, che
sono avanzamenti **e** sono riservati a umani e mezzelfi. Un Silvanesti o un
Irda che nella fonte poteva fare il paladino qui non ha dove andare: non manca
un telaio, manca una **classe** — un paladino di Krynn che non sia un
Cavaliere di Solamnia. La riga `Thief` dell'Aghar ha la stessa forma: sul
telaio Rogue il roster ha il solo Con Artist, che chiede Carisma 12 contro un
massimale razziale di 9. Nove razze dichiarano `Thief`, otto arrivano al Con
Artist, l'Aghar resta senza ladro.

### Le esclusioni, razza per razza

Cio' che il telaio ha aperto e il filtro ha tolto. Le classi che il telaio non
ha mai aperto non compaiono: non sono state escluse, non sono state proposte.

| razza | classe esclusa | motivi |
|---|---|---|
| `elfo-dargonesti` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `elfo-dargonesti` | `cavaliere-rosa` | ingresso (cavaliere-spada); razza (umano, mezzelfo) |
| `elfo-dargonesti` | `cavaliere-spada` | ingresso (cavaliere-corona); razza (umano, mezzelfo) |
| `elfo-dargonesti` | `handler` | razza (kender) |
| `elfo-dargonesti` | `mago-veste-bianca` | ingresso (mago-alta-stregoneria) |
| `elfo-dargonesti` | `mago-veste-nera` | ingresso (mago-alta-stregoneria) |
| `elfo-dargonesti` | `mago-veste-rossa` | ingresso (mago-alta-stregoneria) |
| `elfo-dargonesti` | `tinker` | razza (gnomo-minoi) |
| `elfo-dimernesti` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `elfo-kagonesti` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `elfo-qualinesti` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `elfo-silvanesti` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `elfo-silvanesti` | `cavaliere-rosa` | ingresso (cavaliere-spada); razza (umano, mezzelfo) |
| `elfo-silvanesti` | `cavaliere-spada` | ingresso (cavaliere-corona); razza (umano, mezzelfo) |
| `gnomo-minoi` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `irda` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `irda` | `cavaliere-rosa` | ingresso (cavaliere-spada); razza (umano, mezzelfo) |
| `irda` | `cavaliere-spada` | ingresso (cavaliere-corona); razza (umano, mezzelfo) |
| `kender` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `mezzelfo` | `cavaliere-rosa` | ingresso (cavaliere-spada) |
| `mezzelfo` | `cavaliere-spada` | ingresso (cavaliere-corona) |
| `minotauro` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `nano-aghar` | `cavaliere` | caratteristica (con 15 > 12); caratteristica (int 10 > 9); caratteristica (wis 10 > 9) |
| `nano-aghar` | `cavaliere-corona` | razza (umano, mezzelfo); caratteristica (wis 10 > 9) |
| `nano-aghar` | `con-artist` | caratteristica (cha 12 > 9) |
| `nano-collina` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `nano-montagna` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `umano` | `cavaliere-rosa` | ingresso (cavaliere-spada) |
| `umano` | `cavaliere-spada` | ingresso (cavaliere-corona) |
| `umano` | `handler` | razza (kender) |
| `umano` | `mago-veste-bianca` | ingresso (mago-alta-stregoneria) |
| `umano` | `mago-veste-nera` | ingresso (mago-alta-stregoneria) |
| `umano` | `mago-veste-rossa` | ingresso (mago-alta-stregoneria) |
| `umano` | `tinker` | razza (gnomo-minoi) |
| `umano-barbaro` | `cavaliere-corona` | razza (umano, mezzelfo) |
| `umano-barbaro` | `cavaliere-rosa` | ingresso (cavaliere-spada); razza (umano, mezzelfo) |
| `umano-barbaro` | `cavaliere-spada` | ingresso (cavaliere-corona); razza (umano, mezzelfo) |
| `umano-barbaro` | `handler` | razza (kender) |
| `umano-barbaro` | `mago-veste-bianca` | ingresso (mago-alta-stregoneria) |
| `umano-barbaro` | `mago-veste-nera` | ingresso (mago-alta-stregoneria) |
| `umano-barbaro` | `mago-veste-rossa` | ingresso (mago-alta-stregoneria) |
| `umano-barbaro` | `tinker` | razza (gnomo-minoi) |

---

## 6. Il verso opposto, ricalcolato

Una nostra classe che nessuna razza puo' prendere e' **ingiocabile**, e
finche' nessuno guarda la mappa dal lato delle classi non si vede. Con la
risoluzione in opera il conto cambia, e cambia per una ragione che la mappa da
sola non poteva vedere: le razze senza elenco (§7) aprono il roster intero,
quindi raggiungono anche classi che **nessuna etichetta nomina**.

| nostra classe | si entra da | razze che la raggiungono | quante |
|---|---|---|--:|
| `barbaro` | — | `elfo-dargonesti`, `elfo-dimernesti`, `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `gnomo-minoi`, `irda`, `kender`, `mezzelfo`, `minotauro`, `nano-aghar`, `nano-collina`, `nano-montagna`, `umano-barbaro`, `umano` | 15 |
| `cavaliere-corona` | — | `mezzelfo`, `umano` | 2 |
| `cavaliere-rosa` | `cavaliere-spada` | **NESSUNA** | 0 |
| `cavaliere-spada` | `cavaliere-corona` | **NESSUNA** | 0 |
| `cavaliere` | — | `elfo-dargonesti`, `elfo-dimernesti`, `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `gnomo-minoi`, `irda`, `kender`, `mezzelfo`, `minotauro`, `nano-collina`, `nano-montagna`, `umano-barbaro`, `umano` | 14 |
| `commoner` | — | `elfo-dargonesti`, `umano-barbaro`, `umano` | 3 |
| `con-artist` | — | `elfo-dargonesti`, `elfo-kagonesti`, `elfo-qualinesti`, `gnomo-minoi`, `irda`, `kender`, `mezzelfo`, `nano-collina`, `nano-montagna`, `umano-barbaro`, `umano` | 11 |
| `handler` | — | `kender` | 1 |
| `mago-alta-stregoneria` | — | `elfo-dargonesti`, `elfo-dimernesti`, `elfo-qualinesti`, `elfo-silvanesti`, `gnomo-minoi`, `irda`, `mezzelfo`, `minotauro`, `umano-barbaro`, `umano` | 10 |
| `mago-rinnegato` | — | `elfo-dargonesti`, `elfo-dimernesti`, `elfo-qualinesti`, `elfo-silvanesti`, `gnomo-minoi`, `irda`, `mezzelfo`, `minotauro`, `umano-barbaro`, `umano` | 10 |
| `mago-veste-bianca` | `mago-alta-stregoneria` | **NESSUNA** | 0 |
| `mago-veste-nera` | `mago-alta-stregoneria` | **NESSUNA** | 0 |
| `mago-veste-rossa` | `mago-alta-stregoneria` | **NESSUNA** | 0 |
| `mariner` | — | `elfo-dargonesti`, `irda`, `mezzelfo`, `minotauro`, `umano-barbaro`, `umano` | 6 |
| `sacerdote-eretico` | — | `elfo-dargonesti`, `kender`, `mezzelfo`, `umano-barbaro`, `umano` | 5 |
| `sacerdote-ordini-sacri` | — | `elfo-dargonesti`, `elfo-dimernesti`, `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `gnomo-minoi`, `irda`, `kender`, `mezzelfo`, `minotauro`, `nano-aghar`, `nano-collina`, `nano-montagna`, `umano-barbaro`, `umano` | 15 |
| `tinker` | — | `gnomo-minoi` | 1 |

5 classi su 17 non sono raggiunte da nessuna razza alla creazione, e contarle
insieme darebbe un numero falso:

| classe | si entra da | verdetto |
|---|---|---|
| `cavaliere-rosa` (Knight of the Rose) | `cavaliere-spada` | **avanzamento**, raggiungibile per la classe che lo richiede |
| `cavaliere-spada` (Knight of the Sword) | `cavaliere-corona` | **avanzamento**, raggiungibile per la classe che lo richiede |
| `mago-veste-bianca` (Wizard of the White Robes) | `mago-alta-stregoneria` | **avanzamento**, raggiungibile per la classe che lo richiede |
| `mago-veste-nera` (Wizard of the Black Robes) | `mago-alta-stregoneria` | **avanzamento**, raggiungibile per la classe che lo richiede |
| `mago-veste-rossa` (Wizard of the Red Robes) | `mago-alta-stregoneria` | **avanzamento**, raggiungibile per la classe che lo richiede |

- **5 sono avanzamenti**: non
  devono essere raggiunti dalle razze, ci si arriva dalla classe che li
  richiede. Le tre Vesti si prendono dal Mago dell'Alta Stregoneria, Spada e
  Rosa dal Cavaliere della Corona.
- **0 sono ingiocabili**:
  *(nessuna)*.
### Il verdetto che e' cambiato: `commoner`

La prima stesura di questo rapporto dava `commoner` **INGIOCABILE**: nessuna
etichetta lo nomina, ed era vero. Con la risoluzione in opera lo raggiungono 3
razze — le tre senza elenco — perche' un roster aperto per assenza di
preclusione arriva anche dove nessuna etichetta arriva. Il difetto non era nei
dati, era nella lettura: contare solo le etichette non vedeva le razze che non
ne hanno.

Il verso opposto e' stato controllato sulla fonte, ed e' la domanda che
contava: il Popolano e' una classe da personaggio o un profilo di PNG? Il
manuale lo tratta come classe da personaggio — il capitolo delle classi apre
la creazione di un popolano dalla scelta del mestiere, con i suoi tiri di
caratteristica e la sua progressione, e la regola opzionale sulla classe
sociale lo nomina come *classe da personaggio*. La sezione sui PNG e' un'altra
e non lo riguarda. Quindi la raggiungibilita' e' **corretta**, non un effetto
collaterale da correggere.

Resta un fatto della fonte, non un difetto nostro: la tabella Class/Race
Combinations non concede il Popolano a **nessuna** razza demiumana, mentre
concede il Tinker allo Gnomo. Un popolano non umano non esiste nel manuale.

- **0 avanzamenti orfani**.

---

## 7. Le 3 razze senza elenco, e due significati per un valore

| razza | applied | classes | accessibili dopo il filtro |
|---|---|---|--:|
| `elfo-dargonesti` | False | null | 9 |
| `umano-barbaro` | False | null | 9 |
| `umano` | False | null | 10 |

`applied: false` vuol dire **nessun elenco**, e l'assenza di un elenco ha due
cause che il valore non distingue:

- **Nessuna preclusione** — la tabella Class/Race Combinations elenca solo le
  razze demiumane e gli umani non vi compaiono affatto: non c'e' nessuna riga
  che precluda loro qualcosa. Il vincolo non esiste.
- **La fonte tace** — il Dargonesti non e' nella tabella, che elenca il solo
  Dimernesti. Non e' un vincolo assente, e' un dato mancante.

Il secondo caso portava la nota del primo: campo compilato, controllo che
passa, e la spiegazione di un altro. Ora ogni razza senza elenco ha la
**propria** nota, e `build_razze.nota_classi_ammesse` **rifiuta di generare**
una razza a elenco vuoto che non ne abbia una: la garanzia e' strutturale, non
affidata a chi rilegge.

La conseguenza sui numeri resta e va guardata: finche' il silenzio della fonte
viene letto come assenza di vincolo, il Dargonesti prende l'esito **piu' largo
possibile** — 9 classi — prodotto da un buco del manuale e non da una scelta.
La questione aperta e' scritta nel dato: ereditare le 4 voci del Dimernesti, o
lasciare il silenzio.

---

## 8. Cosa resta aperto, e cosa e' solo lavoro

Le due cose si somigliano e non sono la stessa: una voce in coda si smaltisce,
una domanda aperta va decisa. Confonderle gonfia il conto delle decisioni con
del lavoro gia' noto. Le 4 etichette senza telaio si dividono in tre casi, e
solo uno e' una domanda.

### Lavoro noto: 2 etichette che non aprono niente e hanno un telaio SRD in coda

| etichetta | telaio SRD in coda | razze che la dichiarano | quante |
|---|---|---|--:|
| `Bard` | `Bard` | `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `kender`, `mezzelfo` | 5 |
| `Ranger` | `Ranger` | `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `kender`, `mezzelfo`, `nano-collina` | 6 |

Il telaio esiste nell'SRD 5.1 e nessuno l'ha ancora trascritto: e' battitura,
non conversione. La coda sta in `_srd51.CODA`, accanto ai telai trascritti,
perche' e' li' che si guarda quando se ne aggiunge uno. Nota che trascrivere
il telaio non basta da solo: serve anche una classe di Krynn che ci stia
sopra, come per `Paladin` in §5b.

### Coperte lo stesso: 2 etichette senza telaio che aprono una classe per nome

| etichetta | apre | razze | perche' nessun telaio |
|---|---|---|---|
| `Druid (heathen)` | `sacerdote-eretico` | `kender`, `mezzelfo` | nessun telaio, e non serve: l'etichetta e' gia' coperta per nome dal Sacerdote Eretico, che di telaio non ne ha. Il Druido SRD servirebbe solo se il druido eretico risultasse una classe a se' (`_srd51.CODA`) |
| `Tinker` | `tinker` | `gnomo-minoi` | non ha un telaio 5e: e' un'invenzione di Krynn |

Non sono in coda e non sono una domanda: la classe c'e' e la razza la
raggiunge. Cio' che manca e' il telaio **sotto la classe**, che e' un'altra
questione — riguarda i privilegi di quella classe, non l'accesso a essa.

### Decisioni aperte: 0 etichette che non aprono niente e non hanno un telaio in coda

*(nessuna: ogni etichetta scoperta ha il suo telaio in coda)*

### Accostamenti da confermare: 1

| etichetta | classe aperta | su cosa si regge |
|---|---|---|
| `Druid (heathen)` | `sacerdote-eretico` | la scheda del Sacerdote Eretico dichiara gia' di essere entrambe le righe della tabella Class/Race Combinations, `Priest (heathen)` e `Druid (heathen)`; il capitolo delle classi definisce eretico anche il druido che viene da un altro mondo, perche' ignora gli dei della natura di Krynn |

Sono righe della sede marcate `da_confermare`: aprono una classe e aspettano
una lettura di merito. Restano visibili finche' qualcuno non le guarda — che
e' il contrario di un accostamento sciolto dentro un conteggio.
