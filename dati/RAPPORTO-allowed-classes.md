# `allowed_classes` risolto — dal telaio alle classi, razza per razza

*Generato da `dati/analizza_allowed_classes.py`. La mappa e la regola stanno
in `dati/_classi_ammesse.py`: qui si applicano e si contano.*

---

## 0. La regola, e cosa produce

La decisione 58 (`telaio-apre-classe-filtra`) risolve le 17 etichette del PHB
2e in due tempi: **il telaio apre l'insieme, i requisiti della classe filtrano
dentro**. Due controlli in sequenza, non uno.

Il conto, in tre numeri: le 15 razze aprono **168 coppie razza+classe**, il
filtro ne toglie **42**, ne restano **126** — una media di **8.4 classi
accessibili per razza** su 20 del roster, 15 delle quali si prendono alla
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

**20 classi** nel roster, con il telaio 5e su cui ciascuna sta:

| nostra classe | nome inglese | gruppo | telaio 5e | stato | si entra da |
|---|---|---|---|---|---|
| `barbaro` | Barbarian | Warrior | `Fighter` | clonato | — |
| `cavaliere-corona` | Knight of the Crown | Warrior | `Fighter` | clonato | — |
| `cavaliere-rosa` | Knight of the Rose | Warrior | `Paladin` | clonato | `cavaliere-spada` |
| `cavaliere-spada` | Knight of the Sword | Warrior | `Paladin` | clonato | `cavaliere-corona` |
| `cavaliere` | Cavalier | Warrior | `Fighter` | clonato | — |
| `commoner` | Commoner | Normal | **nessuno** | in_sospeso | — |
| `con-artist` | Con Artist / Prestidigitator | Rogue | `Rogue` | clonato | — |
| `guerriero` | Fighter | Warrior | `Fighter` | clonato | — |
| `handler` | Handler | Rogue | **nessuno** | in_sospeso | — |
| `ladro` | Thief | Rogue | `Rogue` | clonato | — |
| `mago-alta-stregoneria` | Wizard of High Sorcery | Wizard | `Wizard` | clonato | — |
| `mago-rinnegato` | Renegade Wizard | Wizard | `Wizard` | clonato | — |
| `mago-veste-bianca` | Wizard of the White Robes | Wizard | **nessuno** | in_sospeso | `mago-alta-stregoneria` |
| `mago-veste-nera` | Wizard of the Black Robes | Wizard | **nessuno** | in_sospeso | `mago-alta-stregoneria` |
| `mago-veste-rossa` | Wizard of the Red Robes | Wizard | **nessuno** | in_sospeso | `mago-alta-stregoneria` |
| `mariner` | Mariner | Warrior | **nessuno** | in_sospeso | — |
| `paladino` | Paladin | Warrior | `Paladin` | clonato | — |
| `sacerdote-eretico` | Heathen Priest | Priest | **nessuno** | in_sospeso | — |
| `sacerdote-ordini-sacri` | Priest of the Holy Orders of the Stars | Priest | `Cleric` | clonato | — |
| `tinker` | Tinker | Normal | **nessuno** | in_sospeso | — |

I telai trascritti sono 5 — `Cleric`, `Fighter`, `Paladin`, `Rogue`, `Wizard`
— e il roster ne usa 5 (`Cleric`, `Fighter`, `Paladin`, `Rogue`, `Wizard`). 8
nostre classi non hanno un telaio: per loro la decisione 58
(`telaio-apre-classe-filtra`) non cambia niente, perche' il telaio non puo'
aprire cio' su cui nessuno sta. Ci si arriva solo se un'etichetta le nomina. 5
classi non si prendono alla creazione: si entra da un'altra classe.

In coda ci sono 2 telai SRD non ancora trascritti (`Bard`, `Ranger`, in
`_srd51.CODA`): sono lavoro noto, non decisioni aperte — vedi §8.

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
| `Barbarian` | 5 | `Fighter` | `barbaro` | `barbaro`, `cavaliere`, `cavaliere-corona`, `guerriero` |
| `Bard` | 5 | **nessuno** | — | **niente** |
| `Cavalier` | 3 | `Fighter` | `cavaliere` | `barbaro`, `cavaliere`, `cavaliere-corona`, `guerriero` |
| `Druid (heathen)` | 2 | **nessuno** | `sacerdote-eretico` | `sacerdote-eretico` |
| `Fighter` | 12 | `Fighter` | `guerriero` | `barbaro`, `cavaliere`, `cavaliere-corona`, `guerriero` |
| `Handler` | 1 | `Rogue` | `handler` | `con-artist`, `handler`, `ladro` |
| `High Sorcerer` | 6 | `Wizard` | `mago-alta-stregoneria` | `mago-alta-stregoneria`, `mago-rinnegato` |
| `Holy Orders` | 11 | `Cleric` | `sacerdote-ordini-sacri` | `sacerdote-ordini-sacri` |
| `Illusionist` | 1 | `Wizard` | — | `mago-alta-stregoneria`, `mago-rinnegato` |
| `Knight of Solamnia` | 1 | `Paladin` | `cavaliere-corona`, `cavaliere-spada`, `cavaliere-rosa` | `cavaliere-corona`, `cavaliere-rosa`, `cavaliere-spada`, `paladino` |
| `Mage (Renegade)` | 2 | `Wizard` | `mago-rinnegato` | `mago-alta-stregoneria`, `mago-rinnegato` |
| `Mariner` | 3 | `Fighter` | `mariner` | `barbaro`, `cavaliere`, `cavaliere-corona`, `guerriero`, `mariner` |
| `Paladin` | 2 | `Paladin` | `paladino` | `cavaliere-rosa`, `cavaliere-spada`, `paladino` |
| `Priest (heathen)` | 2 | `Cleric` | `sacerdote-eretico` | `sacerdote-eretico`, `sacerdote-ordini-sacri` |
| `Ranger` | 6 | **nessuno** | — | **niente** |
| `Thief` | 9 | `Rogue` | `ladro` | `con-artist`, `ladro` |
| `Tinker` | 1 | **nessuno** | `tinker` | `tinker` |

### Le ragioni, che sono di due tipi e restano distinte

| etichetta | ragione del telaio (editoriale) | ragione delle classi (di fonte) |
|---|---|---|
| `Barbarian` | guerriero senza addestramento cavalleresco; l'Ira e' un'invenzione della 3e, assente da Krynn | il nome inglese del Barbaro coincide con l'etichetta |
| `Bard` | il Bardo SRD esiste nella 5e ma non fra i telai trascritti: in coda. E' anche una classe base 2e che il roster non ha: vedi CLASSI BASE 2e nel docstring | — |
| `Cavalier` | guerriero a cavallo, telaio marziale puro | il nome inglese del Cavaliere coincide con l'etichetta |
| `Druid (heathen)` | nessun telaio, e non serve: l'etichetta e' gia' coperta per nome dal Sacerdote Eretico, che di telaio non ne ha | CONFERMATO sulla fonte il 04/09/2026, non piu' un accostamento in attesa. Il capitolo Priest Group Classes ha due sole voci — Holy Orders of the Stars ed Heathen Priests — e nessuna terza voce per un druido: la scheda dell'eretico dichiara che sono eretici anche i druidi venuti da altri mondi, perche' non conoscono Chislev e Habbakuk. Le due righe `Druid (heathen)` e `Priest (heathen)` della tabella Class/Race Combinations si distinguono per il solo tetto di livello, che non applichiamo (decisione 4, `limiti-di-livello`): tolto quello, sono la stessa classe |
| `Fighter` | e' il telaio, e nomina anche la classe base 2e che gli sta sopra: vedi CLASSI BASE 2e nel docstring | il nome inglese del Guerriero coincide con l'etichetta. E' la classe base AD&D 2e che *Tales of the Lance* dichiara giocabile su Ansalon senza descriverla, trascritta dal PHB 2e con la decisione 59 (`classi-base-2e`) |
| `Handler` | abilita' del ladro applicate al baratto kender | il nome inglese dell'Handler coincide con l'etichetta |
| `High Sorcerer` | incantatore arcano a preparazione | `Wizard of High Sorcery` e' il nome inglese della classe |
| `Holy Orders` | incantatore divino, e' il nome 2e dell'ordine sacerdotale di Krynn | `Priest of the Holy Orders of the Stars` e' il nome inglese della classe; la tabella abbrevia |
| `Illusionist` | specialista arcano: nella 5e e' una sottoclasse del Mago, non una classe | — |
| `Knight of Solamnia` | l'ombrello dei tre ordini cavallereschi; due dei tre stanno su telaio Paladin | etichetta OMBRELLO: la tabella la porta come una riga sola e il capitolo dei Cavalieri di Solamnia descrive tre ordini in sequenza obbligata (decisione 5, `cavalieri-solamnia`). Apre tutti e tre; il filtro dell'ingresso lascia il solo Cavaliere della Corona |
| `Mage (Renegade)` | incantatore arcano fuori dagli Ordini | `Renegade Wizard` e' il nome inglese della classe |
| `Mariner` | guerriero di mare | il nome inglese del Marinaio coincide con l'etichetta. Senza questa riga l'etichetta `Mariner` non aprirebbe il Marinaio, che non ha chassis |
| `Paladin` | e' il telaio, e nomina anche la classe base 2e che gli sta sopra: vedi CLASSI BASE 2e nel docstring | il nome inglese del Paladino coincide con l'etichetta. E' la classe base AD&D 2e trascritta dal PHB 2e con la decisione 59 (`classi-base-2e`), e non un ordine solamnico: e' il paladino che la fonte concede al Silvanesti e all'Irda |
| `Priest (heathen)` | incantatore divino fuori dagli Ordini | `Heathen Priest` e' il nome inglese della classe |
| `Ranger` | il Ranger SRD esiste nella 5e ma non fra i telai trascritti: in coda. E' anche una classe base 2e che il roster non ha: vedi CLASSI BASE 2e nel docstring | — |
| `Thief` | e' il telaio, e nomina anche la classe base 2e che gli sta sopra: vedi CLASSI BASE 2e nel docstring | il nome inglese del Ladro coincide con l'etichetta. E' la classe base AD&D 2e trascritta dal PHB 2e con la decisione 59 (`classi-base-2e`), e non il Con Artist: il ladro comune non ha il minimo di Carisma che escludeva l'Aghar |
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
| `guerriero` | `Fighter` | 12 | 15 | 15 | +3 |
| `handler` | — | 1 | 4 | 1 | 0 |
| `ladro` | `Rogue` | 9 | 12 | 12 | +3 |
| `mago-alta-stregoneria` | `Wizard` | 6 | 10 | 10 | +4 |
| `mago-rinnegato` | `Wizard` | 2 | 10 | 10 | +8 |
| `mago-veste-bianca` | — | 0 | 3 | 0 | 0 |
| `mago-veste-nera` | — | 0 | 3 | 0 | 0 |
| `mago-veste-rossa` | — | 0 | 3 | 0 | 0 |
| `mariner` | — | 3 | 6 | 6 | +3 |
| `paladino` | `Paladin` | 2 | 6 | 6 | +4 |
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

Il filtro toglie **42 coppie** su 168 aperte. Una coppia puo' essere tolta da
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
| `nano-aghar` | 4 | 7 | **4** | `barbaro`, `guerriero`, `ladro`, `sacerdote-ordini-sacri` |
| `elfo-dimernesti` | 4 | 7 | **6** | `barbaro`, `cavaliere`, `guerriero`, `mago-alta-stregoneria`, `mago-rinnegato`, `sacerdote-ordini-sacri` |
| `elfo-kagonesti` | 6 | 7 | **6** | `barbaro`, `cavaliere`, `con-artist`, `guerriero`, `ladro`, `sacerdote-ordini-sacri` |
| `nano-collina` | 5 | 7 | **6** | `barbaro`, `cavaliere`, `con-artist`, `guerriero`, `ladro`, `sacerdote-ordini-sacri` |
| `nano-montagna` | 4 | 7 | **6** | `barbaro`, `cavaliere`, `con-artist`, `guerriero`, `ladro`, `sacerdote-ordini-sacri` |
| `elfo-silvanesti` | 6 | 10 | **7** | `barbaro`, `cavaliere`, `guerriero`, `mago-alta-stregoneria`, `mago-rinnegato`, `paladino`, `sacerdote-ordini-sacri` |
| `minotauro` | 5 | 8 | **7** | `barbaro`, `cavaliere`, `guerriero`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `sacerdote-ordini-sacri` |
| `elfo-qualinesti` | 7 | 9 | **8** | `barbaro`, `cavaliere`, `con-artist`, `guerriero`, `ladro`, `mago-alta-stregoneria`, `mago-rinnegato`, `sacerdote-ordini-sacri` |
| `kender` | 8 | 9 | **8** | `barbaro`, `cavaliere`, `con-artist`, `guerriero`, `handler`, `ladro`, `sacerdote-eretico`, `sacerdote-ordini-sacri` |
| `gnomo-minoi` | 5 | 10 | **9** | `barbaro`, `cavaliere`, `con-artist`, `guerriero`, `ladro`, `mago-alta-stregoneria`, `mago-rinnegato`, `sacerdote-ordini-sacri`, `tinker` |
| `irda` | 7 | 13 | **10** | `barbaro`, `cavaliere`, `con-artist`, `guerriero`, `ladro`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `paladino`, `sacerdote-ordini-sacri` |
| `elfo-dargonesti` | *(nessun elenco)* | 20 | **12** | `barbaro`, `cavaliere`, `commoner`, `con-artist`, `guerriero`, `ladro`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `paladino`, `sacerdote-eretico`, `sacerdote-ordini-sacri` |
| `mezzelfo` | 11 | 14 | **12** | `barbaro`, `cavaliere`, `cavaliere-corona`, `con-artist`, `guerriero`, `ladro`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `paladino`, `sacerdote-eretico`, `sacerdote-ordini-sacri` |
| `umano-barbaro` | *(nessun elenco)* | 20 | **12** | `barbaro`, `cavaliere`, `commoner`, `con-artist`, `guerriero`, `ladro`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `paladino`, `sacerdote-eretico`, `sacerdote-ordini-sacri` |
| `umano` | *(nessun elenco)* | 20 | **13** | `barbaro`, `cavaliere`, `cavaliere-corona`, `commoner`, `con-artist`, `guerriero`, `ladro`, `mago-alta-stregoneria`, `mago-rinnegato`, `mariner`, `paladino`, `sacerdote-eretico`, `sacerdote-ordini-sacri` |

Il numero e' molto piu' basso di quello del telaio — 126 contro 168 — ed e' il
punto: il telaio da solo sarebbe stato una traduzione generosa, la sequenza lo
riporta dentro i vincoli che la fonte scrive sulle classi invece che sulle
razze.

Il minimo e 4 (`nano-aghar`), il massimo 13 (`umano`). **Nessuna razza resta a
zero**: non c'e' nessuna razza ingiocabile.

### 5b. Le etichette dichiarate che non aprono niente

Il conto per razza da solo non dice **quale porta si e' chiusa**: dice un
numero piu' basso. Queste sono le coppie razza+etichetta in cui la razza
dichiara un accesso e non ne ricava nessuna classe. Sono due casi diversi.

**11 coppie: l'etichetta non apre niente perche' il telaio e' in coda.**
`Bard`, `Ranger`, gia' contate in §8 come lavoro noto: la razza non ha perso
l'accesso, l'accesso non e' ancora stato scritto.

**0 coppie: l'etichetta apre, e il filtro toglie tutto.** Erano tre fino al
04/09/2026 e sono la ragione per cui la decisione 59 (`classi-base-2e`)
esiste: un'etichetta che apre e poi non lascia niente e' una porta che il
manuale concede e il nostro roster chiude.


### Le cinque etichette che nominano una classe base 2e

La fonte lo dice per prima, e non e' una nostra classificazione. Il capitolo
delle classi di *Tales of the Lance* apre il gruppo dei guerrieri dichiarando
che su Ansalon si giocano le classi guerriere tipiche dell'AD&D 2e — fighter,
ranger e paladin — e che quelle **uniche** di Ansalon sono descritte di
seguito; il gruppo dei ladri ripete la forma, contando i bardi e i ladri fra
quelli comuni e riservando la descrizione ai due tipi propri di Krynn. I
gruppi Wizard e Priest non lo dicono, e infatti sono di Krynn.

Sono 5 etichette in questa condizione (`Bard`, `Fighter`, `Paladin`, `Ranger`,
`Thief`), dichiarate in tutto da 12 razze su 15. La sede e'
`_classi_ammesse.BASE_2E`; **quali di esse il roster abbia gia' non e' scritto
da nessuna parte: si deriva** da chi nomina una nostra classe
(`_classi_ammesse.base_2e_mancanti()`).

**3 trascritte** dalla decisione 59 (`classi-base-2e`), con i minimi della
Tabella 13 del PHB 2e e `mechanics_5e` che rimanda al chassis SRD senza
aggiungere nulla:

| etichetta | nostra classe | razze che la dichiarano e ci arrivano | quali |
|---|---|---|---|
| `Fighter` | `guerriero` | 12 | `elfo-dimernesti`, `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `gnomo-minoi`, `irda`, `kender`, `mezzelfo`, `minotauro`, `nano-aghar`, `nano-collina`, `nano-montagna` |
| `Paladin` | `paladino` | 2 | `elfo-silvanesti`, `irda` |
| `Thief` | `ladro` | 9 | `elfo-kagonesti`, `elfo-qualinesti`, `gnomo-minoi`, `irda`, `kender`, `mezzelfo`, `nano-aghar`, `nano-collina`, `nano-montagna` |

**2 ancora da trascrivere** (`Bard`, `Ranger`), e costano piu' delle prime
tre: per queste manca **anche** il telaio SRD, che e' in coda in `_srd51.CODA`
(§8). Le prime tre avevano il telaio gia' battuto a macchina e mancava la sola
classe.

**Il Con Artist non e' in questa condizione, ed e' un esito atteso.** Il
manuale lo apre a qualunque razza giocabile di Krynn e nella stessa riga gli
pone un minimo di Carisma 12; all'Aghar pone un massimale di Carisma 9. E' la
doppia penalita' della decisione 10 (`massimali-razziali`) che morde dove deve
mordere: fedelta' che funziona, non una porta da riaprire. 9 razze dichiarano
`Thief` e 8 arrivano al Con Artist; resta fuori `nano-aghar`. Chi rilegge fra
sei mesi trovi scritto qui che questa riga **non va sanata** — e che il ladro
comune, che l'Aghar ora prende, e' un'altra classe.

Il conto che ne segue va saputo: la razza piu' vincolata del roster e'
`nano-aghar`, con **4 classi accessibili** su 20 (`barbaro`, `guerriero`,
`ladro`, `sacerdote-ordini-sacri`), contro le 6 della seconda. Delle 4
etichette che dichiara, 0 restano nella condizione sopra. E' un numero che il
giocatore deve vedere **in creazione**, non scoprire dopo aver scelto la
razza.

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
| `guerriero` | — | `elfo-dargonesti`, `elfo-dimernesti`, `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `gnomo-minoi`, `irda`, `kender`, `mezzelfo`, `minotauro`, `nano-aghar`, `nano-collina`, `nano-montagna`, `umano-barbaro`, `umano` | 15 |
| `handler` | — | `kender` | 1 |
| `ladro` | — | `elfo-dargonesti`, `elfo-kagonesti`, `elfo-qualinesti`, `gnomo-minoi`, `irda`, `kender`, `mezzelfo`, `nano-aghar`, `nano-collina`, `nano-montagna`, `umano-barbaro`, `umano` | 12 |
| `mago-alta-stregoneria` | — | `elfo-dargonesti`, `elfo-dimernesti`, `elfo-qualinesti`, `elfo-silvanesti`, `gnomo-minoi`, `irda`, `mezzelfo`, `minotauro`, `umano-barbaro`, `umano` | 10 |
| `mago-rinnegato` | — | `elfo-dargonesti`, `elfo-dimernesti`, `elfo-qualinesti`, `elfo-silvanesti`, `gnomo-minoi`, `irda`, `mezzelfo`, `minotauro`, `umano-barbaro`, `umano` | 10 |
| `mago-veste-bianca` | `mago-alta-stregoneria` | **NESSUNA** | 0 |
| `mago-veste-nera` | `mago-alta-stregoneria` | **NESSUNA** | 0 |
| `mago-veste-rossa` | `mago-alta-stregoneria` | **NESSUNA** | 0 |
| `mariner` | — | `elfo-dargonesti`, `irda`, `mezzelfo`, `minotauro`, `umano-barbaro`, `umano` | 6 |
| `paladino` | — | `elfo-dargonesti`, `elfo-silvanesti`, `irda`, `mezzelfo`, `umano-barbaro`, `umano` | 6 |
| `sacerdote-eretico` | — | `elfo-dargonesti`, `kender`, `mezzelfo`, `umano-barbaro`, `umano` | 5 |
| `sacerdote-ordini-sacri` | — | `elfo-dargonesti`, `elfo-dimernesti`, `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `gnomo-minoi`, `irda`, `kender`, `mezzelfo`, `minotauro`, `nano-aghar`, `nano-collina`, `nano-montagna`, `umano-barbaro`, `umano` | 15 |
| `tinker` | — | `gnomo-minoi` | 1 |

5 classi su 20 non sono raggiunte da nessuna razza alla creazione, e contarle
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
| `elfo-dargonesti` | False | null | 12 |
| `umano-barbaro` | False | null | 12 |
| `umano` | False | null | 13 |

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
possibile** — 12 classi — prodotto da un buco del manuale e non da una scelta.

**La fonte non tace del tutto, e va detto qui perche' cambia i termini della
domanda.** Letto il 04/09/2026: il capitolo delle razze ha un paragrafo di
regole speciali per i PG Dimernesti **e** Dargonesti, e li' elenca cinque
classi che gli elfi del mare possono prendere — Cavalier, Paladin, Fighter,
High Sorcerer, Holy Orders. E' l'unico posto in cui il Dargonesti riceve un
elenco, e per il Dimernesti e' un **secondo** elenco accanto alla riga della
tabella. I due non coincidono: la riga della tabella non concede `Paladin`, il
paragrafo si'. La questione aperta resta scritta nel dato, ma le opzioni sono
tre e non due: ereditare le 4 voci del Dimernesti, leggere le cinque del
paragrafo, o lasciare il silenzio. Non e' deciso qui, ed e' registrato perche'
la seconda opzione non era in vista.

---

## 8. Cosa resta aperto, e cosa e' solo lavoro

Le due cose si somigliano e non sono la stessa: una voce in coda si smaltisce,
una domanda aperta va decisa. Confonderle gonfia il conto delle decisioni con
del lavoro gia' noto. Le 4 etichette senza telaio si dividono in tre casi, e
nessuno di essi e' oggi una domanda; una quarta voce, le classi base 2e,
taglia trasversalmente e non dipende dal telaio.

### Lavoro noto: 2 etichette che non aprono niente e hanno un telaio SRD in coda

| etichetta | telaio SRD in coda | razze che la dichiarano | quante |
|---|---|---|--:|
| `Bard` | `Bard` | `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `kender`, `mezzelfo` | 5 |
| `Ranger` | `Ranger` | `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `kender`, `mezzelfo`, `nano-collina` | 6 |

Il telaio esiste nell'SRD 5.1 e nessuno l'ha ancora trascritto: e' battitura,
non conversione. La coda sta in `_srd51.CODA`, accanto ai telai trascritti,
perche' e' li' che si guarda quando se ne aggiunge uno. Nota che trascrivere
il telaio non basta da solo: serve anche la classe che ci sta sopra, ed e'
esattamente la voce qui sotto.

### Lavoro noto, seconda voce: 2 etichette su 5 che nominano una classe base 2e ancora assente dal roster

| etichetta | telaio | cosa manca | razze che la dichiarano | quante |
|---|---|---|---|--:|
| `Bard` | *in coda* | telaio **e** classe | `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `kender`, `mezzelfo` | 5 |
| `Ranger` | *in coda* | telaio **e** classe | `elfo-kagonesti`, `elfo-qualinesti`, `elfo-silvanesti`, `kender`, `mezzelfo`, `nano-collina` | 6 |

Non e' una nostra classificazione: e' quello che *Tales of the Lance* dichiara
aprendo i gruppi Warrior e Rogue (§5b). Delle 5 etichette in questa
condizione, 3 sono state trascritte dalla decisione 59 (`classi-base-2e`) —
`Fighter`, `Paladin`, `Thief`, che avevano il telaio SRD gia' battuto a
macchina e costavano la sola classe — e con esse si sono chiuse le tre righe
svuotate di §5b. Le 2 che restano compaiono anche nella voce sopra e costano
telaio **e** classe: finche' la classe non c'e', l'etichetta apre il solo
insieme del telaio, che per queste due e' vuoto. Sede:
`_classi_ammesse.BASE_2E`, con la parte derivata in `base_2e_mancanti()`.

### Coperte lo stesso: 2 etichette senza telaio che aprono una classe per nome

| etichetta | apre | razze | perche' nessun telaio |
|---|---|---|---|
| `Druid (heathen)` | `sacerdote-eretico` | `kender`, `mezzelfo` | nessun telaio, e non serve: l'etichetta e' gia' coperta per nome dal Sacerdote Eretico, che di telaio non ne ha |
| `Tinker` | `tinker` | `gnomo-minoi` | non ha un telaio 5e: e' un'invenzione di Krynn |

Non sono in coda e non sono una domanda: la classe c'e' e la razza la
raggiunge. Cio' che manca e' il telaio **sotto la classe**, che e' un'altra
questione — riguarda i privilegi di quella classe, non l'accesso a essa.

### Decisioni aperte: 0 etichette che non aprono niente e non hanno un telaio in coda

*(nessuna: ogni etichetta scoperta ha il suo telaio in coda)*

### Accostamenti da confermare: 0

*(nessuno: l'ultimo, `Druid (heathen)` sul Sacerdote Eretico, e' stato
confermato sulla fonte il 04/09/2026 — la ragione sta in sede, non qui)*

Sono righe della sede marcate `da_confermare`: aprono una classe e aspettano
una lettura di merito. Restano visibili finche' qualcuno non le guarda — che
e' il contrario di un accostamento sciolto dentro un conteggio.
