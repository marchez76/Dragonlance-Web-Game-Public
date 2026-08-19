# Rapporto diagnostico sulle 17 classi di Krynn

*Generato da `dati/analizza_classi.py` il 2026-08-14.*

> **Cos'è.** Una diagnosi, non una conversione. Serve a vedere la forma del
> problema prima di compilare `mechanics_5e`, come `RAPPORTO-soddisfacibilita.md`
> ha fatto per le razze. Nessuna decisione è presa qui.
>
> **Come leggere.** Ogni numero e ogni tabella su Krynn è derivato dai JSON in
> `dati/classi/`. Le letture sono scritte a mano e marcate con un blocco citato
> e datato.
>
> **Fonte 5e.** SRD 5.1 (CC-BY), tabelle di classe trascritte verbatim in
> `dati/_srd51.py`. I confronti sono derivati da lì, non scritti a memoria.

---

## Sintesi

| classe | gruppo | DV | PE | inc. | priv. | imp. | ingresso | vincoli |
|---|---|---|---|:-:|---:|---:|---:|---|
| Barbaro | Warrior | d10 | gruppo | — | 2 | 1 | 1° | 4 minimi |
| Cavaliere | Warrior | d10 | gruppo | — | 6 | 4 | 1° | allineamento, 5 minimi |
| Cavaliere della Corona | Warrior | d10 | 25 liv. | — | 1 | 1 | 1° | allineamento, razza, 5 minimi |
| Cavaliere della Rosa | Warrior | d10 | 22 liv. | — | 1 | 0 | 4° | allineamento, razza, 5 minimi |
| Cavaliere della Spada | Warrior | d10 | 23 liv. | sì | 3 | 0 | 3° | allineamento, razza, 5 minimi |
| Marinaio | Warrior | d10 | gruppo | — | 1 | 1 | 1° | allineamento, 2 minimi |
| Mago dell'Alta Stregoneria | Wizard | 1d4 | 25 liv. | sì | 3 | 4 | 1° | allineamento, 1 minimo |
| Mago Rinnegato | Wizard | 1d4 | 25 liv. | sì | 1 | 2 | 1° | 1 minimo |
| Mago delle Vesti Bianche | Wizard | 1d4 | gruppo | — | 0 | 1 | 3° | allineamento, 1 minimo |
| Mago delle Vesti Nere | Wizard | 1d4 | gruppo | — | 0 | 1 | 3° | allineamento, 1 minimo |
| Mago delle Vesti Rosse | Wizard | 1d4 | gruppo | — | 0 | 1 | 3° | allineamento, 1 minimo |
| Sacerdote Eretico | Priest | 1d8 | 25 liv. | — | 0 | 2 | 1° | 1 minimo |
| Sacerdote degli Ordini Sacri delle Stelle | Priest | 1d8 | 25 liv. | sì | 0 | 1 | 1° | allineamento, 1 minimo |
| Truffatore / Prestigiatore | Rogue | d6 | gruppo | — | 1 | 1 | 1° | 1 minimo |
| Handler | Rogue | d6 | gruppo | — | 0 | 3 | 1° | razza |
| Popolano | Normal | d6 | 25 liv. | — | 0 | 0 | 1° | — |
| Tinker | Normal | d6 | 25 liv. | — | 0 | 1 | 1° | razza |

**PE**: "gruppo" significa che la classe non ha una tabella propria e rimanda a
quella standard del suo gruppo. **priv.** = privilegi speciali, **imp.** =
impedimenti.

### Per gruppo

| gruppo | classi | privilegi | media | impedimenti |
|---|---:|---:|---:|---:|
| Warrior | 6 | 14 | 2.3 | 7 |
| Wizard | 5 | 4 | 0.8 | 9 |
| Priest | 2 | 0 | 0.0 | 3 |
| Rogue | 2 | 1 | 0.5 | 4 |
| Normal | 2 | 0 | 0.0 | 1 |

Su 17 classi: **19 privilegi** in tutto (media 1.1), di cui
**7** agganciati a un livello esplicito, e **24 impedimenti**
(media 1.4).

**8 classi su 17 non hanno una tabella di esperienza propria**:
Barbaro, Cavaliere, Truffatore / Prestigiatore, Handler, Mago delle Vesti Bianche, Mago delle Vesti Nere, Mago delle Vesti Rosse, Marinaio.

**8 classi su 17 non hanno alcun privilegio**:
Popolano, Handler, Mago delle Vesti Bianche, Mago delle Vesti Nere, Mago delle Vesti Rosse, Sacerdote Eretico, Sacerdote degli Ordini Sacri delle Stelle, Tinker.

---

## 1. Densità

#### Cavaliere della Corona contro Fighter (SRD 5.1, guerriero)

Dado vita: d10 contro 1d10. Tiri salvezza Fighter: Strength, Constitution.

| livello | Cavaliere della Corona | Fighter SRD 5.1 |
|---:|---|---|
| 1° | — | Fighting Style, Second Wind |
| 2° | — | Action Surge (one use) |
| 3° | — | Martial Archetype |
| 5° | — | Extra Attack |
| 7° | — | Martial Archetype Feature |
| 9° | — | Indomitable (one use) |
| 10° | — | Martial Archetype Feature |
| 11° | — | Extra Attack (2) |
| 13° | — | Indomitable (two uses) |
| 15° | — | Martial Archetype Feature |
| 17° | — | Action Surge (two uses), Indomitable (three uses) |
| 18° | — | Martial Archetype Feature |
| 20° | — | Extra Attack (3) |
| *non dichiarato* | Specializzazione nelle armi | — |

Livelli a cui Cavaliere della Corona concede qualcosa: **0**, contro **13** del Fighter. Privilegi totali: **1** contro **15** (piu' 7 aumenti di caratteristica, che la 2e non ha); 1 privilegio di Krynn non dichiara a che livello si ottenga.

#### Mago dell'Alta Stregoneria contro Wizard (SRD 5.1, mago)

Dado vita: 1d4 contro 1d6. Tiri salvezza Wizard: Intelligence, Wisdom.

| livello | Mago dell'Alta Stregoneria | Wizard SRD 5.1 |
|---:|---|---|
| 1° | primi incantesimi | Spellcasting, Arcane Recovery |
| 2° | — | Arcane Tradition |
| 3° | Immunita' dei livelli bassi | — |
| 6° | Fasi lunari | Arcane Tradition Feature |
| 10° | — | Arcane Tradition Feature |
| 14° | — | Arcane Tradition Feature |
| 18° | — | Spell Mastery |
| 20° | — | Signature Spell |
| *non dichiarato* | Allineamenti lunari | — |

Livelli a cui Mago dell'Alta Stregoneria concede qualcosa: **3**, contro **7** del Wizard. Privilegi totali: **3** contro **8** (piu' 5 aumenti di caratteristica, che la 2e non ha); 1 privilegio di Krynn non dichiara a che livello si ottenga.

#### Sacerdote degli Ordini Sacri delle Stelle contro Cleric (SRD 5.1, sacerdote)

Dado vita: 1d8 contro 1d8. Tiri salvezza Cleric: Wisdom, Charisma.

| livello | Sacerdote degli Ordini Sacri delle Stelle | Cleric SRD 5.1 |
|---:|---|---|
| 1° | primi incantesimi | Spellcasting, Divine Domain |
| 2° | — | Channel Divinity (1/rest), Divine Domain Feature |
| 5° | — | Destroy Undead (CR 1/2) |
| 6° | — | Channel Divinity (2/rest), Divine Domain Feature |
| 8° | — | Destroy Undead (CR 1), Divine Domain Feature |
| 10° | — | Divine Intervention |
| 11° | — | Destroy Undead (CR 2) |
| 14° | — | Destroy Undead (CR 3) |
| 17° | — | Destroy Undead (CR 4), Divine Domain Feature |
| 18° | — | Channel Divinity (3/rest) |
| 20° | — | Divine Intervention improvement |

Livelli a cui Sacerdote degli Ordini Sacri delle Stelle concede qualcosa: **1**, contro **11** del Cleric. Privilegi totali: **0** contro **16** (piu' 5 aumenti di caratteristica, che la 2e non ha).


> **Lettura interpretativa** — registrata il 2026-08-14. Non e' derivata dai dati.
>
> Le classi di Krynn non sono classi nel senso della 5e: sono **profili di
> restrizione** appoggiati sulle classi base della 2e. Su 19 privilegi totali solo
> 7 sono agganciati a un livello esplicito; per gli altri 12 la fonte non dice
> quando si ottengano. La curva di avanzamento è quindi quasi piatta: ciò che un
> personaggio guadagna salendo di livello viene dalla tabella del gruppo 2e, non
> dalla classe di Krynn.
>
> **9 classi su 17 hanno più impedimenti che privilegi**, cioè tolgono più di quanto
> diano: Handler (0 contro 3), Sacerdote Eretico (0 contro 2), Mago dell'Alta Stregoneria (3 contro 4), Mago Rinnegato (1 contro 2), Mago delle Vesti Bianche (0 contro 1), Mago delle Vesti Nere (0 contro 1), Mago delle Vesti Rosse (0 contro 1), Sacerdote degli Ordini Sacri delle Stelle (0 contro 1), Tinker (0 contro 1).
> Il caso limite è l'**Handler**. Non è un errore di trascrizione: il manuale
> definisce alcune di queste classi per ciò che non possono fare.
>
> Il **Cavaliere** è il rovescio: 6 privilegi e 4 impedimenti, il valore più alto
> del roster in entrambe le colonne. È la sola classe con un contenuto meccanico
> paragonabile a una classe 5e, e lo paga con il codice cavalleresco.
>
> All'estremo opposto ci sono 8 classi con zero privilegi. Popolano e Tinker
> sono del gruppo Normal e non dovrebbero averne; le tre Vesti sono vuote perché
> sono affiliazioni e non classi, il che è coerente con la decisione 6. Restano i due
> sacerdoti e l'Handler, che invece dovrebbero avere un contenuto e non ce l'hanno:
> per i sacerdoti tutto il contenuto meccanico sta nelle sfere delle divinità, già
> estratte in `dati/divinita/`; per l'Handler il manuale spende tre impedimenti e
> nessun beneficio, cioè definisce un ladro per ciò che non sa fare.
>
> La conseguenza pratica: convertire queste classi in 5e non è un lavoro di
> traduzione ma di **riempimento**. Non c'è quasi nulla da tradurre, e la fedeltà
> alla fonte (decisione 16) qui non basta a produrre una classe giocabile.

---

## 2. Chassis 5e

*Analisi svolta prima della decisione 23, che l'ha poi adottata. I chassis sono
ora applicati nei dati: vedi `mechanics_5e.chassis` in `dati/classi/*.json`.*

Per ciascuna classe di Krynn, la classe base 5e più vicina come chassis.

| classe di Krynn | chassis 5e 2014 | perché |
|---|---|---|
| Barbaro | Fighter, **non** Barbarian | Il Barbarian 5e è costruito sull'Ira, che la 2e non ha. Il barbaro di Krynn è un guerriero con competenze ambientali: il Fighter regge meglio, con l'ambiente spostato su background/competenze. |
| Cavaliere della Corona | Fighter | Specializzazione nelle armi e progressione da guerriero puro. Nessuna magia al 1° grado. |
| Cavaliere della Spada | Paladin | La fonte dice esplicitamente "capacità della classe Paladino al proprio livello" e concede incantesimi da sacerdote dal 6°. È l'accoppiamento più pulito del roster. |
| Cavaliere della Rosa | Paladin | Prosegue il grado precedente; l'immunità alla paura è già un privilegio del Paladin 5e (Aura di Coraggio, 10°). |
| Cavaliere | Fighter con Stile Difesa, oppure Cavalier (sottoclasse) | Sei privilegi tutti di combattimento montato e reputazione. La sottoclasse Cavalier del PHB 2014 copre il montato; il codice comportamentale resta scoperto. |
| Marinaio | Fighter/Rogue ibrido — **nessun candidato pulito** | Guerriero con quattro abilità da ladro. In 5e sarebbe multiclasse o una sottoclasse dedicata: entrambe le strade sono decisioni, non conversioni. |
| Mago dell'Alta Stregoneria | Wizard | Corrispondenza diretta. Le fasi lunari non hanno equivalente e vanno inventate o scartate. |
| Mago Rinnegato | Wizard | Stesso chassis, definito per sottrazione: è il Mago dell'Alta Stregoneria senza vincoli e senza bonus lunari. |
| Vesti Bianche / Rosse / Nere | **nessuno — non sono classi** | Decisione 6: affiliazioni dichiarate al Test, al 3° livello, sopra la classe base. In 5e il posto naturale è la sottoclasse (Tradizione Arcana), che però in 5e si sceglie al 2°, non al 3°. |
| Sacerdote degli Ordini Sacri | Cleric | Corrispondenza diretta, con le sfere già estratte da mappare sui Domini. |
| Sacerdote Eretico | **nessuno** | Per definizione non ha potere reale. In 5e non esiste una classe che non faccia nulla: o diventa un background, o una variante di Cleric senza incantesimi, o sparisce. |
| Truffatore | Rogue | Le quattro abilità potenziate diventano competenze ed Esperienza. |
| Handler | Rogue senza attacco furtivo | Chassis giusto, ma l'assenza dell'attacco furtivo svuota il Rogue 5e del suo motore di danno. |
| Popolano | **nessuno** | Non è una classe 5e. O PNG, o background. |
| Tinker | **nessuno** | Stessa situazione del Popolano, con in più il tema tecnologico gnomesco. Artificer esiste ma non è nel PHB 2014. |

> **Lettura interpretativa** — registrata il 2026-08-14. Non e' derivata dai dati.
>
> Su quindici voci, sei hanno un chassis pulito (i due maghi, il Cleric, i due gradi
> paladinici, il Rogue truffatore); tre non hanno alcun candidato perché non sono
> classi (Popolano, Tinker, Vesti); tre sono classi 5e svuotate del loro motore
> (Handler senza attacco furtivo, Sacerdote Eretico senza incantesimi, Barbaro senza
> Ira); tre richiedono una decisione di struttura (Marinaio ibrido, Cavaliere,
> Cavaliere della Corona come Fighter senza sottoclasse).
>
> Il caso più interessante è il **Barbaro**: la classe 5e che porta il suo nome è
> quella sbagliata. L'Ira è un'invenzione della 3e, non un tratto del barbaro di
> Krynn né del kit del 1989. Chiamare Barbarian il Barbaro di Ansalon importerebbe
> in blocco una meccanica che la fonte non ha.
>
> Il secondo è il **conflitto sul livello delle Vesti**: la decisione 6 le colloca al
> 3° perché lì avviene il Test, ma la 5e assegna la sottoclasse del Wizard al 2°. Il
> disallineamento è di un livello solo, ma va deciso: si sposta il Test al 2°, si
> tiene la sottoclasse vuota per un livello, o si accetta uno scarto.

---

## 3. Incompatibilità strutturali

Sistemi 2e senza equivalente in 5e. Richiedevano una **decisione**, non una
conversione. **Le prime sette sono state decise e applicate**: la scelta adottata
è indicata sotto ciascuna, e vive in `mechanics_5e.structural` in ogni classe.
Le ultime due restano aperte.

Per ciascuno: cosa faceva, perché la 5e l'ha eliminato, opzioni, esito.

### 3.1 Tabelle di esperienza differenziate per classe

**Cosa faceva.** Ogni classe 2e aveva la propria soglia di PE. Le classi
considerate più potenti salivano più lentamente: era il bilanciamento, spalmato
sul tempo di gioco invece che sulle capacità.

**Perché la 5e l'ha eliminato.** Una sola tabella per tutti. Con il gruppo che
avanza insieme, tabelle differenziate producevano personaggi di livello diverso
nella stessa squadra — l'effetto che la 5e considerava peggiore del problema che
risolveva.

**Opzioni.** (a) Tabella unica 5e, e le progressioni 2e restano in `source_2e`
come dato storico. (b) Tabella unica ma con moltiplicatore di PE per classe,
conservando l'ordinamento relativo senza sfasare i livelli. (c) Conservare le
tabelle 2e, accettando gruppi disallineati.

**DECISO** — opzione (a): tabella unica 5e. Le progressioni 2e restano in
`source_2e` come dato storico.
### 3.2 Progressione THAC0 per gruppo

**Cosa faceva.** Warrior migliorava di 1 per livello, Priest e Rogue circa 2 ogni
3 livelli, Wizard 1 ogni 3. La capacità di colpire era la differenza principale
fra i gruppi.

**Perché la 5e l'ha eliminato.** Il bonus di competenza è identico per tutti e
cresce da +2 a +6. La differenziazione è passata alle competenze nelle armi,
all'Attacco Extra e alle sottoclassi.

**Opzioni.** (a) Bonus di competenza standard; la differenza fra gruppi si esprime
con Attacco Extra e competenze. (b) Bonus di competenza standard più un bonus di
gruppo separato, che ricrea lo scarto 2e ma rompe la matematica dei GS 5e.
(c) Ripristinare scale differenziate, con lo stesso problema in forma peggiore.

**DECISO** — opzione (a): bonus di competenza standard. La differenza fra gruppi
si esprime con Attacco Extra e competenze.
### 3.3 Le cinque categorie di tiro salvezza

**Cosa faceva.** Paralisi/Veleno/Magia della Morte, Bacchette, Pietrificazione,
Soffio, Incantesimi. Erano proprietà della classe e del livello, non delle
caratteristiche: un guerriero di 9° aveva buoni tiri perché era un guerriero.

**Perché la 5e l'ha eliminato.** Sei tiri su caratteristica, con competenza in due
sole, decise dalla classe. Il vantaggio è che l'effetto dice quale caratteristica
usare; il costo è che il livello non migliora più i tiri non competenti.

**Opzioni.** (a) Mappare le cinque categorie sulle sei caratteristiche
(Paralisi/Veleno→COS, Bacchette→DES, Pietrificazione→COS o FOR, Soffio→DES,
Incantesimi→SAG) e assegnare a ogni classe le due competenze coerenti col gruppo
2e. (b) Conservare le cinque categorie come sistema parallelo, incompatibile con
tutto il resto della 5e. (c) Ibrido: competenze 5e più un bonus che cresce col
livello sulle categorie in cui il gruppo 2e era forte.

**Nota:** nessuna delle 17 classi ha una tabella di tiri salvezza estratta. Il
manuale non ne stampa una per classe di Krynn: valgono quelle di gruppo del PHB 2e,
che non sono ancora nei dati.

**DECISO** — opzione (a): le cinque categorie sono mappate sulle sei
caratteristiche (Paralisi/Veleno→COS, Bacchette→DES, Pietrificazione→COS,
Soffio→DES, Incantesimi→SAG), e ogni classe riceve le due competenze coerenti
col gruppo 2e.
### 3.4 Slot di competenza nelle armi

**Cosa faceva.** Un numero finito di slot, spesi per diventare competenti in
un'arma; spenderne due dava specializzazione, con bonus a colpire e ai danni.
Guerrieri ne avevano molti, maghi pochissimi. Le armi non competenti davano
penalità.

**Perché la 5e l'ha eliminato.** Competenza per categoria (armi semplici, armi da
guerra), concessa in blocco dalla classe. Nessuna specializzazione, sostituita
dai talenti opzionali.

**Opzioni.** (a) Competenze per categoria 5e; le armi obbligate della fonte
(lancia e spada per i cavalieri, ascia bipenne e spada bastarda per il barbaro)
diventano equipaggiamento iniziale imposto invece che slot. (b) Ricreare la
specializzazione come talento dedicato — è già così nel PHB 2014 con Maestro
d'Armi. (c) Sistema a slot parallelo, che duplica le competenze 5e.

**Da notare:** la specializzazione nelle armi è dichiarata come **privilegio** per
il Cavaliere della Corona e per il Minotauro. Se la specializzazione sparisce, i
due perdono un privilegio: va sostituito o registrato come perdita.

**DECISO** — opzione (a): competenze per categoria 5e. Le armi obbligate della
fonte diventano equipaggiamento iniziale imposto.
### 3.5 Ricchezza iniziale per gruppo

**Cosa faceva.** Ogni gruppo tirava una formula in monete (Warrior 5d4×10,
Rogue 2d6×10, e così via), poi comprava l'equipaggiamento. Il tiro produceva
personaggi di partenza diseguali.

**Perché la 5e l'ha eliminato.** Pacchetto di equipaggiamento fisso per classe e
background, con l'oro come alternativa opzionale. Elimina il tiro e la
disuguaglianza iniziale.

**Opzioni.** (a) Pacchetti fissi 5e, con le regole di equipaggiamento della fonte
convertite in vincoli sul pacchetto (il marinaio senza armature metalliche, il
barbaro senza armature pesanti, il cavaliere obbligato all'armatura migliore).
(b) Tiro 2e conservato, coerente con la decisione 8 che ha già scelto i dadi per
le caratteristiche. (c) Pacchetto fisso più tiro opzionale.

**Da notare:** solo 4 classi su 17 dichiarano una ricchezza iniziale propria; le
altre rimandano al gruppo. E una delle quattro, il Cavaliere, ha il valore
**ricostruito e non letto** (vedi le sue ambiguità di fonte).

**DECISO** — opzione (a): pacchetti fissi 5e, con le regole di equipaggiamento
della fonte convertite in vincoli sul pacchetto.
### 3.6 Livelli oltre il 20°

**Cosa faceva.** Le tabelle di Krynn arrivano al **25° livello**.

**Perché è un problema.** La 5e si ferma al 20°, e la matematica dei gradi sfida è
tarata su quel tetto.

**Opzioni.** (a) Troncare al 20°, conservando in `source_2e` i cinque livelli in
più. (b) Epic Boons oltre il 20°, che nel 2014 sono materiale della DMG.
(c) Comprimere 25 livelli 2e in 20 livelli 5e, riscalando le soglie.

**DECISO** — opzione (a): troncamento al 20°. I cinque livelli in più restano in
`source_2e`.
### 3.7 Titoli di livello

**Cosa faceva.** Ogni livello aveva un titolo (Novice of Swords, Blade Knight,
Master Clerist...). Era colore, ma anche struttura sociale dell'ordine.

**Perché la 5e l'ha eliminato.** Nessun titolo, in nessuna classe.

**Opzioni.** (a) Conservarli come dato descrittivo, mostrato nella scheda ma senza
effetto meccanico. (b) Legarli a un sistema di reputazione o grado nell'ordine.
(c) Scartarli.

**DECISO** — opzione (a): conservati come dato descrittivo, mostrati nella
scheda, senza effetto meccanico.
### 3.8 Sfere sacerdotali contro Domini

**Cosa faceva.** Ogni divinità concedeva accesso maggiore o minore a un elenco di
sfere; l'incantesimo era disponibile se la sfera lo era.

**Perché la 5e l'ha eliminato.** Il Cleric ha una lista unica più un Dominio che
aggiunge incantesimi sempre preparati. L'accesso non si nega più: si concede.

**Opzioni.** (a) Mappare le sfere sui Domini 2014 (Conoscenza, Guerra, Vita, Luce,
Natura, Tempesta, Inganno), con perdita di granularità. (b) Conservare le sfere
come filtro sulla lista 5e, ripristinando la negazione di accesso — coerente con
la decisione 16, che dà la precedenza alla fonte. (c) Ibrido: Dominio per gli
incantesimi bonus, sfere per i divieti.

**Materiale già pronto**: le sfere delle 21 divinità sono estratte in
`dati/divinita/`, con accesso maggiore e minore distinti.

### 3.9 Ordine obbligato dei gradi solamnici

**Cosa faceva.** Corona → Spada → Rosa, con ingresso al 1°, 3° e 4° livello.

**Perché è un problema.** La decisione 5 lo ha già confermato come sequenza
obbligata senza azzeramenti. In 5e non esiste un meccanismo di "grado" che cambi
la classe a metà percorso: la struttura più vicina è la sottoclasse, ma se ne
sceglie una sola.

**Opzioni.** (a) Classe unica con tre stadi interni, sbloccati al livello
previsto. (b) Tre sottoclassi in sequenza, che la 5e non prevede. (c) Classe base
più un sistema di gradi d'ordine separato dalla classe.

---

## Cosa manca ai dati

> **Lettura interpretativa** — registrata il 2026-08-14. Non e' derivata dai dati.
>
> Prima di poter compilare `mechanics_5e` per le classi mancano tre cose che non
> sono decisioni ma estrazioni:
>
> 1. **Le tabelle di gruppo del PHB 2e** — PE, THAC0 e tiri salvezza per Warrior,
>    Wizard, Priest e Rogue. 8 classi su 17 vi rimandano, e senza quelle tabelle
>    quelle classi non hanno progressione alcuna nei dati. Il PHB 2e è in libreria
>    ma il suo testo estratto è degradato: le tabelle andranno lette dalle immagini
>    di pagina, come già fatto per i tratti razziali.
>
> 2. **La ricchezza iniziale del Cavaliere**, che è ricostruita e non letta.
>
> 3. **Il PHB 5e 2014** resta fuori libreria, ma non è più bloccante: l'SRD 5.1
>    copre classi base, privilegi livello per livello e liste incantesimi, ed è
>    ridistribuibile. Del PHB servirebbero solo le sottoclassi fuori SRD — fra
>    cui i Domini Morte e Forgia, che servono a tre divinità.

---

## Appendice — il Barbaro alla fonte completa

Confronto fra le tre fonti disponibili in libreria. Serve a distinguere cosa dei
tratti di Ansalon è specifico di Krynn e cosa è tradizione del barbaro 2e, come la
decisione 16 ha fatto col PHB per elfi e nani. **Non riorganizza il Barbaro**: la
decisione 20 resta in piedi e la conversione a background resta rimandata.

### Le tre fonti

| fonte | anno | cos'è il barbaro | dove |
|---|---|---|---|
| `PHBR1 - The Complete Fighter's Handbook` | 1989 | **kit** del guerriero, non classe | Warrior Kits, pagg. 18-19 |
| `PHBR14 - The Complete Barbarian's Handbook` | 1995 | **classe autonoma** (barbarian fighter e shaman) | tutto il manuale, 130 pagg. |
| `Tales of the Lance` | 1992 | **razza/cultura** e **classe**, in due capitoli distinti | People of Ansalon e Classes of Ansalon |

### Cosa dice il kit del 1989 (PHBR1)

Il barbaro è un guerriero con un kit. Non ha tabella di esperienza, né dado vita,
né tiri salvezza propri: è un Fighter. Il kit aggiunge:

- competenze d'arma obbligate — Ascia bipenne, Spada bastarda;
- competenza bonus non d'arma — Resistenza;
- vincolo sull'armatura: niente più pesante di splint/banded/bronze plate finché
  non ha viaggiato nel mondo esterno;
- **+3 alle reazioni** quando il tiro è già favorevole (8 o meno), e **−3** quando
  è già sfavorevole (14 o più);
- ricchezza da guerriero (5d4×10 mo) che deve spendere quasi tutta prima di
  cominciare, restando con 3 mo o meno.

**Non c'è nulla** su terreno natio, nostalgia, tracciare, o limiti di Intelligenza
e Carisma.

### Cosa aggiunge il manuale del 1995 (PHBR14)

Qui il barbaro diventa classe, con due varianti: **barbarian fighter** e **shaman**.
Il fighter ha:

- **tabella di esperienza propria**, più lenta del guerriero standard, fino al 20°;
- **dado vita d12** — nove dadi, poi +3 fissi per livello;
- **movimento base 15**, contro il 12 dell'umano standard, e +3 al movimento da
  ingombro;
- **abilità fisiche a percentuale che crescono col livello**: salto, balzo,
  arrampicata (30%→95%), rilevamento degli attacchi alle spalle (5%→95%);
- **armature limitate a Hide (CA 6)**, armi solo di pietra, legno, osso;
- attacchi multipli come il guerriero, più regola per le due armi;
- **Homeland Terrain**, che concede gratis quattro competenze nel terreno natio —
  Sopravvivenza, Nascondersi, Seguire tracce, Conoscenza degli animali — più
  **−2 alla sorpresa dei nemici**;
- **limiti di Intelligenza e Carisma**: nessun massimale fisso, ma una penalità da
  −2 a −6 alle prove di INT e CAR **fuori dal territorio natio**;
- **penalità di reazione** fino a −6, cumulativa per igiene, aspetto, linguaggio,
  comportamento, e **mai riducibile sotto −1**;
- ricchezza in prodotti animali invece che in monete;
- avversione alla magia: la magia di casa è accettata, quella del mondo esterno è
  un presagio orribile.

### Il confronto con Tales of the Lance

| elemento | PHBR1 1989 | PHBR14 1995 | Tales of the Lance | verdetto |
|---|---|---|---|---|
| Terreno natio come meccanica | assente | **Homeland Terrain**, 4 competenze gratis | *Figlio del proprio territorio*: Sopravvivenza, Tracciare, Cacciare | **tradizione 2e**, non Krynn |
| Malus fuori dal territorio | assente | −2/−6 a INT e CAR nell'outworld | *Nostalgia del territorio*: −1 a tutti i tiri per 1d6 giorni | **stessa idea, meccanica diversa**: Krynn la fa temporanea e generale, PHBR14 permanente e mirata |
| Tetto all'Intelligenza | assente | nessun tetto, solo penalità sulle prove | **INT max 18, DES max 16** sulla scheda razziale | **specifico di Krynn** |
| Reazione | +3/−3 | fino a −6, mai sotto −1 | *Magnetismo selvaggio* +3 / *Rovescio* −3 | **il kit del 1989**, ripreso alla lettera |
| Armi obbligate | **Ascia bipenne, Spada bastarda** | armi di pietra/legno/osso, elenco di undici | **Ascia bipenne, Spada bastarda** | **il kit del 1989**, identiche |
| Vincolo sull'armatura | niente oltre splint/banded/bronze plate | niente oltre Hide (CA 6) | niente oltre splint/banded/bronze plate | **il kit del 1989**, identico |
| Dado vita | d10 (guerriero) | **d12** | d10 | **Krynn segue il kit**, non il manuale del 1995 |
| Tabella di esperienza | quella del guerriero | **propria, più lenta** | quella del guerriero | **Krynn segue il kit** |
| Movimento | normale | **15** | normale | **Krynn segue il kit** |
| Abilità fisiche a percentuale | assenti | salto, arrampicata, attacchi alle spalle | assenti | **solo PHBR14** |
| Immunità al freddo | assente | assente | **barbari del ghiaccio** | **specifico di Krynn** |
| Quattro gruppi culturali | assente | terreno a scelta libera | montagna, pianura, ghiaccio, mare | **specifico di Krynn** |

> **Lettura interpretativa** — registrata il 2026-08-14. Non e' derivata dai dati.
>
> **Il Barbaro di Krynn discende dal kit del 1989, non dalla classe del 1995.**
> La prova non è un'impressione: Tales of the Lance obbliga alle **stesse due armi**
> del kit — Ascia bipenne e Spada bastarda, che nel kit sono dichiaratamente
> "le armi classiche del barbaro da narrativa" — e ripete **lo stesso identico
> vincolo sull'armatura**, splint/banded/bronze plate. Aggiungi dado vita d10,
> tabella di esperienza del guerriero, movimento normale e il +3/−3 alle reazioni,
> e la derivazione è completa. Tales of the Lance esce nel 1992, in mezzo alle due
> fonti, e usa quella che esisteva.
>
> Questo spiega la doppia natura che la decisione 12 aveva registrato come
> ambiguità della fonte: **non è un'ambiguità, è un residuo**. Il barbaro di Krynn è
> un kit del guerriero che il manuale ha collocato in due capitoli — cultura e
> classe — perché la 2e del 1992 non aveva ancora una classe barbaro da citare.
> Questo rafforza, senza deciderla, la strada del background già indicata dalla
> decisione 20: un kit non è una classe, ed è esattamente ciò che in 5e diventa un
> background più una sottoclasse.
>
> Due tratti sono **davvero di Krynn** e non hanno riscontro in nessuna delle due
> fonti generali: l'**immunità al freddo dei barbari del ghiaccio** e i **quattro
> gruppi culturali**. Un terzo, il **tetto a Intelligenza 18 e Destrezza 16**, è di
> Krynn come *numero*: PHBR14 tratta la stessa idea come penalità situazionale
> anziché come massimale.
>
> E uno è **tradizione 2e travestita da Krynn**: il legame col terreno natio. Sia il
> manuale del 1995 sia Tales of the Lance concedono competenze gratuite nel proprio
> ambiente. Per la decisione 16, questo andrebbe convertito guardando alla forma
> generale del tratto, non a quella particolare di Krynn.
>
> **Una cosa che PHBR14 ha e noi no**: la *nostalgia del territorio* di Krynn dura
> 1d6 giorni e poi passa. Il malus di PHBR14 è permanente e colpisce solo INT e CAR
> nell'outworld — cioè è **il vero corrispettivo meccanico del tetto
> all'Intelligenza**, non del malus temporaneo. Se un giorno si volesse rimuovere il
> tetto DES 16 senza perdere l'identità del barbaro, la penalità situazionale di
> PHBR14 sarebbe la sostituzione naturale. Non è una proposta: è materiale.

### Ambiguità trovate, da registrare

- **Il testo estratto di `PHBR1 - The Complete Fighter's Handbook` ha le colonne
  fuse.** Le righe delle due colonne si alternano ("reaction. Bur because he's /
  Fighter or Ranger"), quindi il manuale è leggibile solo per frammenti. Non ha
  compromesso questo confronto — le voci del kit sono riconoscibili — ma va
  ri-estratto prima di usarlo come fonte.
- **PHBR14 nomina Krynn una sola volta** e la DRAGONLANCE tre: due esempi di
  terreno natio (le Grandi Paludi) e una nota sui **Kagonesti come elfi barbari**.
  Non contiene materiale su Krynn oltre a questo: non è una fonte di setting.
- **PHBR14 cita i Kagonesti come esempio di elfi barbari** ("Barbarian elves tend
  to be wild elves or sylvan elves, such as the Kagonesti"). È una menzione di
  colore, senza meccanica: non incide sulle decisioni 21 e 22.

---

## Schede per classe

### Barbaro — `barbaro`

| campo | valore |
|---|---|
| gruppo 2e | Warrior |
| dado vita | d10 |
| minimi di caratteristica | COS 12, DES 8, FOR 10, SAG 8 |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | nessuna restrizione |
| razze ammesse | tutte |
| ricchezza iniziale | 3d4x10 stl (1d4x10 per i barbari del ghiaccio) |
| pagine PDF | 88 |

**Punti esperienza**: nessuna tabella propria. Il manuale rimanda alle tabelle standard del gruppo Warrior.

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Warrior.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Warrior.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: clone di **Fighter** (SRD 5.1), dado vita 1d10, tiri salvezza Strength, Constitution. NON Barbarian: l'Ira e' un'invenzione della 3e, assente sia da Krynn sia dal kit del 1989 da cui il Barbaro di Ansalon discende. Confermato dall'appendice di RAPPORTO-classi.md.

**Privilegi**: 2, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 1. Da convertire: 3.

| privilegio | livello | testo sintetico |
|---|---|---|
| Magnetismo selvaggio | — | Quando il tiro di reazione del barbaro e' 8 o meno (contando i bonus razziali e di Carisma), si sottrae un ulteriore +3, rendendo la reazione ancora p. |
| Immunita' al freddo (solo barbari del ghiaccio) | — | I barbari del ghiaccio sono immuni agli attacchi basati sul freddo, come il soffio del drago bianco e il cono di freddo. |

| impedimento | testo sintetico |
|---|---|
| Rovescio del magnetismo | Quando il tiro di reazione e' 14 o piu', si applica una penalita' di -3, peggiorando la reazione rispetto a quanto sarebbe stata. |

**Armi obbligate**: Battle Axe, Bastard Sword.
**Regole di equipaggiamento**:
- Non puo' acquistare armature piu' pesanti di splint, banded o bronze plate mail finche' non si e' avventurato nel mondo esterno.
- Puo' acquistare solo le armi comuni alla propria tribu'.

**Ambiguità di fonte registrate**:
- Il manuale tratta "Barbarian" sia come cultura razziale (capitolo People of Ansalon) sia come classe (questo capitolo). I minimi coincidono nei due punti tranne che qui manca il tetto di Destrezza 16 e il tetto di Intelligenza 18 presenti nella scheda razziale.

---

### Cavaliere — `cavaliere`

| campo | valore |
|---|---|
| gruppo 2e | Warrior |
| dado vita | d10 |
| minimi di caratteristica | COS 15, DES 15, INT 10, FOR 15, SAG 10 |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | Qualunque allineamento buono |
| razze ammesse | tutte |
| ricchezza iniziale | 5d4x10 stl |
| pagine PDF | 88, 89 |

**Punti esperienza**: nessuna tabella propria. Il manuale rimanda alle tabelle standard del gruppo Warrior.

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Warrior.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Warrior.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: clone di **Fighter** (SRD 5.1), dado vita 1d10, tiri salvezza Strength, Constitution. Sei privilegi tutti di combattimento montato e reputazione. In SRD l'unico archetipo marziale e' il Campione: il montato resta scoperto e il codice comportamentale pure.

**Privilegi**: 6, di cui 3 agganciati a un livello esplicito. **Impedimenti**: 4. Da convertire: 10.

| privilegio | livello | testo sintetico |
|---|---|---|
| Maestria con la lancia | 1° | Al 1° livello +1 a colpire in sella usando una lancia in cui e' competente. |
| Maestria con la spada | 3° | Al 3° livello +1 a colpire con un tipo di spada in cui e' competente. |
| Maestria con armi da cavaliere | 5° | Al 5° livello +1 a colpire con piccone, mazza o flagello, tutti di tipo da cavaliere. |
| Coraggio irradiato | — | Immune agli incantesimi di paura. |
| Resistenza mentale | — | +4 ai tiri salvezza contro ogni magia che influenza la mente: charm person, friends, hypnotism, sleep, irritation, ray of enfeeblement, scare, geas, c. |
| Reputazione | — | +3 alle reazioni da chiunque appartenga alla sua cultura, tranne malvagi e criminali, dai quali riceve -3. |

| impedimento | testo sintetico |
|---|---|
| Obbligo di caricare | Non puo' attaccare a distanza se puo' invece caricare e attaccare in mischia o in giostra. |
| Obbligo del nemico piu' forte | In ogni mischia deve attaccare il nemico piu' grande e dall'aspetto piu' potente. |
| Ossessione per l'armatura | Possiede sempre la migliore armatura possibile, con l'obiettivo di arrivare all'armatura completa a piastre. |
| Violazione del codice | Alla prima violazione, senso di colpa. |

**Armi obbligate**: Lance (any), Sword (any).
**Regole di equipaggiamento**:
- Inizia con almeno due armi, fra cui una lancia e una spada.
- Deve comprare l'armatura piu' costosa che puo' permettersi.
- Inizia con un cavallo gratuito: da guerra leggero, medio o pesante, a discrezione del DM.

**Ambiguità di fonte registrate**:
- La ricchezza iniziale nel testo estratto compare come "564x10 stl", chiaramente corrotta. Il manuale rimanda alla ricchezza base del gruppo Warrior, che in AD&D 2e e' 5d4x10 stl. Valore ricostruito, non letto: da confermare sull'originale.

---

### Cavaliere della Corona — `cavaliere-corona`

| campo | valore |
|---|---|
| gruppo 2e | Warrior |
| dado vita | d10 |
| minimi di caratteristica | COS 10, DES 8, INT 7, FOR 10, SAG 10 |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | Lawful Good |
| razze ammesse | umano, mezzelfo |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 83, 84, 85, 86, 87 |

**Punti esperienza**: tabella presente. 25 livelli (dal 1° al 25°). monotona crescente. Da 0 a 5.500.000 PE.
Titoli di livello: 11 su 25 (fino al 11°).

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Warrior.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Warrior.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: clone di **Fighter** (SRD 5.1), dado vita 1d10, tiri salvezza Strength, Constitution. Guerriero puro, nessuna magia al primo grado. La sequenza verso Spada e Rosa (decisione 5) si innesta sopra il chassis.

**Privilegi**: 1, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 1. Da convertire: 1.

| privilegio | livello | testo sintetico |
|---|---|---|
| Specializzazione nelle armi | — | I Cavalieri della Corona possono usare la specializzazione nelle armi. |

| impedimento | testo sintetico |
|---|---|
| Cavaliere sconosciuto | I cavalieri poco noti in una zona subiscono -4 alle reazioni dei PNG. |

**Armi obbligate**: Lance (any), Sword (any).
**Regole di equipaggiamento**:
- Un Cavaliere di Solamnia deve spendere i pezzi d'acciaio iniziali in almeno due armi: una lancia e una spada.

---

### Cavaliere della Rosa — `cavaliere-rosa`

| campo | valore |
|---|---|
| gruppo 2e | Warrior |
| dado vita | d10 |
| minimi di caratteristica | COS 15, DES 12, INT 10, FOR 15, SAG 13 |
| livello d'ingresso | 4  (non si comincia da qui) |
| classe prerequisito | cavaliere-spada |
| allineamento | Lawful Good |
| razze ammesse | umano, mezzelfo |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 85, 87 |

**Punti esperienza**: tabella presente. 22 livelli (dal 4° al 25°). monotona crescente. Da 0 a 9.000.000 PE.
Titoli di livello: 12 su 22 (fino al 15°).

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Warrior.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Warrior.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: clone di **Paladin** (SRD 5.1), dado vita 1d10, tiri salvezza Wisdom, Charisma. Prosegue il grado precedente. L'immunita' alla paura e' gia' un privilegio del Paladino (Aura di Coraggio).

**Privilegi**: 1, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 0. Da convertire: 0.

| privilegio | livello | testo sintetico |
|---|---|---|
| Immunita' alla paura | — | I Cavalieri della Rosa sono completamente immuni agli incantesimi di paura. |

**Armi obbligate**: Lance (any), Sword (any).
**Regole di equipaggiamento**: nessuna dichiarata.

**Ambiguità di fonte registrate**:
- Il manuale non chiarisce se un Cavaliere della Rosa conservi gli incantesimi acquisiti come Cavaliere della Spada. Nodo da sciogliere nella conversione 5e.

---

### Cavaliere della Spada — `cavaliere-spada`

| campo | valore |
|---|---|
| gruppo 2e | Warrior |
| dado vita | d10 |
| minimi di caratteristica | COS 10, DES 9, INT 9, FOR 12, SAG 13 |
| livello d'ingresso | 3  (non si comincia da qui) |
| classe prerequisito | cavaliere-corona |
| allineamento | Lawful Good |
| razze ammesse | umano, mezzelfo |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 85, 86, 87 |

**Punti esperienza**: tabella presente. 23 livelli (dal 3° al 25°). monotona crescente. Da 0 a 6.500.000 PE.
Titoli di livello: 11 su 23 (fino al 13°).

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Warrior.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Warrior.

**Incantesimi**: tabella presente, dal 6° al 18° livello di classe, fino al 7° grado di incantesimo.

**Chassis 5e (decisione 23)**: clone di **Paladin** (SRD 5.1), dado vita 1d10, tiri salvezza Wisdom, Charisma. La fonte dice esplicitamente "capacita' della classe Paladino al proprio livello" e concede incantesimi sacerdotali dal 6°. E' l'accoppiamento piu' pulito del roster.

**Privilegi**: 3, di cui 1 agganciati a un livello esplicito. **Impedimenti**: 0. Da convertire: 2.

| privilegio | livello | testo sintetico |
|---|---|---|
| Capacita' del paladino | — | I Cavalieri della Spada ottengono le capacita' della classe Paladino al proprio livello attuale. |
| Incantesimi sacerdotali | 6° | Ottengono incantesimi da sacerdote a partire dal 6° livello. |
| Magia di Kiri-Jolith | — | Usano gli incantesimi di Kiri-Jolith, benche' Paladine sia il dio piu' venerato dall'ordine. |

**Armi obbligate**: Lance (any), Sword (any).
**Regole di equipaggiamento**: nessuna dichiarata.

**Ambiguità di fonte registrate**:
- La tabella incantesimi parte dal livello 6 di cavaliere, ma il manuale non dice esplicitamente che i livelli 3-5 sono privi di incantesimi: si deduce dall'assenza di righe.
- La tabella incantesimi stampata e' disallineata in tre righe: il livello 9 ha cinque colonne invece di sette, e i livelli 14 e 15 ne hanno sei. Verificato sull'immagine originale: il difetto e' di impaginazione del manuale. Le righe sono state lette da sinistra a destra, ottenendo 9=[3,2,0,0,0,0,0], 14=[7,5,2,1,1,1,0], 15=[8,6,3,2,1,1,0]. La lettura e' coerente con le righe 13 e 16, che sono allineate correttamente, e mantiene la progressione monotona.

---

### Marinaio — `mariner`

| campo | valore |
|---|---|
| gruppo 2e | Warrior |
| dado vita | d10 |
| minimi di caratteristica | DES 11, FOR 12 |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | Qualunque tranne Legale Buono |
| razze ammesse | tutte |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 89 |

**Punti esperienza**: nessuna tabella propria. Il manuale rimanda alle tabelle standard del gruppo Warrior.

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Warrior.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Warrior.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: nessuno, lasciato indeciso. Ibrido Fighter/Rogue: nessun candidato pulito. Da decidere.

**Privilegi**: 1, di cui 1 agganciati a un livello esplicito. **Impedimenti**: 1. Da convertire: 2.

| privilegio | livello | testo sintetico |
|---|---|---|
| Abilita' da ladro | 1° | Il marinaio ottiene Climb Walls, Detect Noise, Hide in Shadows e Move Silently. |

| impedimento | testo sintetico |
|---|---|
| Reputazione da pirata | Nessun impedimento meccanico specifico, ma i pirati di successo si attirano addosso pirati rivali, cacciatori di taglie e altri individui poco raccoma. |

**Armi obbligate**: Cutlass, Belaying Pin, Gaff Hook.
**Regole di equipaggiamento**:
- I marinai non indossano armature metalliche: si impigliano nel sartiame e affogano chi cade in mare.

---

### Mago dell'Alta Stregoneria — `mago-alta-stregoneria`

| campo | valore |
|---|---|
| gruppo 2e | Wizard |
| dado vita | 1d4 |
| minimi di caratteristica | INT 9 |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | Determinato dalla veste: Bianca=buono, Rossa=neutrale, Nera=malvagio. L'allineamento va dichiarato al 3° livello, prima del Test. |
| razze ammesse | tutte |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 89, 90, 91, 92 |

**Punti esperienza**: tabella presente. 25 livelli (dal 1° al 25°). monotona crescente. Da 0 a 6.000.000 PE.
Titoli di livello: 1 su 25 (fino al 18°).

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Wizard.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Wizard.

**Incantesimi**: tabella presente, dal 1° al 25° livello di classe, fino al 9° grado di incantesimo.

**Chassis 5e (decisione 23)**: clone di **Wizard** (SRD 5.1), dado vita 1d6, tiri salvezza Intelligence, Wisdom. Corrispondenza diretta.

**Privilegi**: 3, di cui 2 agganciati a un livello esplicito. **Impedimenti**: 4. Da convertire: 7.

| privilegio | livello | testo sintetico |
|---|---|---|
| Fasi lunari | 6° | Ogni ordine trae potere dalla propria luna. |
| Allineamenti lunari | — | Solinari con Lunitari, oppure Nuitari con Lunitari: +1 ai tiri salvezza, +1 incantesimo, +1 al livello effettivo. |
| Immunita' dei livelli bassi | 3° | I maghi dal 1° al 3° livello non sono mai influenzati dalle fasi lunari: i loro incantesimi sono di potere troppo basso. |

| impedimento | testo sintetico |
|---|---|
| Il Test dell'Alta Stregoneria | Per progredire oltre il 3° livello il mago deve recarsi alla Torre di Wayreth, dichiarare un allineamento, giurare fedelta' a un ordine e affrontare i. |
| Cambio di ordine | Un mago puo' cambiare ordine dopo il Test, ma perde due livelli di esperienza e per un mese non e' influenzato dalla luna del nuovo ordine. |
| Scuole proibite | Le scuole non elencate come consentite sono accessibili solo in parte. |
| Incantesimi con nomi stranieri | Gli incantesimi che contengono il nome proprio di un personaggio esterno ad Ansalon non sono disponibili: Bigby, Drawmij, Elminster, Evard, Leomund, M. |

**Armi obbligate**: nessuna.
**Regole di equipaggiamento**: nessuna dichiarata.

**Ambiguità di fonte registrate**:
- Nella tabella di avanzamento il valore del 3° livello e' stampato "5.000" con un punto invece della virgola. Interpretato come 5.000 PE, coerente con la progressione.

---

### Mago Rinnegato — `mago-rinnegato`

| campo | valore |
|---|---|
| gruppo 2e | Wizard |
| dado vita | 1d4 |
| minimi di caratteristica | INT 9 |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | nessuna restrizione |
| razze ammesse | tutte |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 81, 92 |

**Punti esperienza**: tabella presente. 25 livelli (dal 1° al 25°). monotona crescente. Da 0 a 6.000.000 PE.
Titoli di livello: 1 su 25 (fino al 18°).

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Wizard.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Wizard.

**Incantesimi**: tabella presente, dal 1° al 25° livello di classe, fino al 9° grado di incantesimo.

**Chassis 5e (decisione 23)**: clone di **Wizard** (SRD 5.1), dado vita 1d6, tiri salvezza Intelligence, Wisdom. Stesso chassis, definito per sottrazione: e' il Mago dell'Alta Stregoneria senza vincoli e senza bonus lunari.

**Privilegi**: 1, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 2. Da convertire: 3.

| privilegio | livello | testo sintetico |
|---|---|---|
| Nessun vincolo di scuola | — | Non essendo legato a un ordine, il rinnegato non subisce le restrizioni sulle scuole proibite ne' il vincolo di allineamento delle vesti. |

| impedimento | testo sintetico |
|---|---|
| Braccato | I rinnegati sono braccati dai Maghi dell'Alta Stregoneria e messi di fronte alla scelta fra unirsi a un ordine o morire. |
| Nessun potere lunare | Non traendo potere da alcuna luna, il rinnegato non riceve i bonus di fase e di allineamento lunare. |

**Armi obbligate**: nessuna.
**Regole di equipaggiamento**: nessuna dichiarata.

**Ambiguità di fonte registrate**:
- Il manuale non dice esplicitamente che i rinnegati sono esenti dalle restrizioni di scuola: e' una deduzione dal fatto che quelle restrizioni sono definite come regola d'ordine. Da confermare con Towers of High Sorcery.

---

### Mago delle Vesti Bianche — `mago-veste-bianca`

| campo | valore |
|---|---|
| gruppo 2e | Wizard |
| dado vita | 1d4 |
| minimi di caratteristica | INT 9 |
| livello d'ingresso | 3  (non si comincia da qui) |
| classe prerequisito | mago-alta-stregoneria |
| allineamento | Buono |
| razze ammesse | tutte |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 91 |

**Punti esperienza**: nessuna tabella propria. Il manuale rimanda alle tabelle standard del gruppo Wizard.

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Wizard.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Wizard.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: nessuno, lasciato indeciso. AFFILIAZIONE, non classe (decisione 6).

**Privilegi**: 0, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 1. Da convertire: 1.

| impedimento | testo sintetico |
|---|---|
| Vincolo del Bene | Oltre al voto di sostenere la magia, la causa del Bene e' la sua preoccupazione centrale. |

**Armi obbligate**: nessuna.
**Regole di equipaggiamento**: nessuna dichiarata.

---

### Mago delle Vesti Nere — `mago-veste-nera`

| campo | valore |
|---|---|
| gruppo 2e | Wizard |
| dado vita | 1d4 |
| minimi di caratteristica | INT 9 |
| livello d'ingresso | 3  (non si comincia da qui) |
| classe prerequisito | mago-alta-stregoneria |
| allineamento | Malvagio |
| razze ammesse | tutte |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 91 |

**Punti esperienza**: nessuna tabella propria. Il manuale rimanda alle tabelle standard del gruppo Wizard.

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Wizard.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Wizard.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: nessuno, lasciato indeciso. AFFILIAZIONE, non classe (decisione 6).

**Privilegi**: 0, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 1. Da convertire: 1.

| impedimento | testo sintetico |
|---|---|
| Vincolo del Male | Abbracciano la causa del Male, ma non scagliano palle di fuoco a caso sui casolari dei contadini: attivita' simili abuserebbero della magia e la mette. |

**Armi obbligate**: nessuna.
**Regole di equipaggiamento**: nessuna dichiarata.

---

### Mago delle Vesti Rosse — `mago-veste-rossa`

| campo | valore |
|---|---|
| gruppo 2e | Wizard |
| dado vita | 1d4 |
| minimi di caratteristica | INT 9 |
| livello d'ingresso | 3  (non si comincia da qui) |
| classe prerequisito | mago-alta-stregoneria |
| allineamento | Neutrale |
| razze ammesse | tutte |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 91 |

**Punti esperienza**: nessuna tabella propria. Il manuale rimanda alle tabelle standard del gruppo Wizard.

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Wizard.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Wizard.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: nessuno, lasciato indeciso. AFFILIAZIONE, non classe (decisione 6).

**Privilegi**: 0, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 1. Da convertire: 1.

| impedimento | testo sintetico |
|---|---|
| Vincolo dell'Equilibrio | Oltre alla fedelta' ultima alla magia, il mago delle Vesti Rosse lavora per bilanciare Bene e Male. |

**Armi obbligate**: nessuna.
**Regole di equipaggiamento**: nessuna dichiarata.

---

### Sacerdote Eretico — `sacerdote-eretico`

| campo | valore |
|---|---|
| gruppo 2e | Priest |
| dado vita | 1d8 |
| minimi di caratteristica | SAG 9 |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | nessuna restrizione |
| razze ammesse | tutte |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 93 |

**Punti esperienza**: tabella presente. 25 livelli (dal 1° al 25°). monotona crescente. Da 0 a 4.400.000 PE.
Titoli di livello: 16 su 25 (fino al 18°).

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Priest.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Priest.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: nessuno, lasciato indeciso. Per definizione non ha potere. Da decidere.

**Privilegi**: 0, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 2. Da convertire: 2.

| impedimento | testo sintetico |
|---|---|
| Nessun potere reale | Sacerdoti provenienti da altri mondi o che venerano falsi dei. |
| Conversione | I sacerdoti di altri mondi perdono un livello convertendosi a una religione dello stesso allineamento e due cambiando allineamento. |

**Armi obbligate**: nessuna.
**Regole di equipaggiamento**: nessuna dichiarata.

**Ambiguità di fonte registrate**:
- Il manuale non fornisce una progressione di incantesimi per gli eretici: e' coerente con il fatto che non hanno potere reale, ma non e' detto esplicitamente che non ne abbiano alcuno.

---

### Sacerdote degli Ordini Sacri delle Stelle — `sacerdote-ordini-sacri`

| campo | valore |
|---|---|
| gruppo 2e | Priest |
| dado vita | 1d8 |
| minimi di caratteristica | SAG 9 |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | Coerente con la famiglia celeste del dio servito: Bene, Male o Neutralita'. |
| razze ammesse | tutte |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 92, 93, 94 |

**Punti esperienza**: tabella presente. 25 livelli (dal 1° al 25°). monotona crescente. Da 0 a 4.400.000 PE.
Titoli di livello: 16 su 25 (fino al 18°).

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Priest.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Priest.

**Incantesimi**: tabella presente, dal 1° al 25° livello di classe, fino al 7° grado di incantesimo.

**Chassis 5e (decisione 23)**: clone di **Cleric** (SRD 5.1), dado vita 1d8, tiri salvezza Wisdom, Charisma. Corrispondenza diretta. Le sfere gia' estratte diventano il filtro della decisione 24; il Dominio resta come sottoclasse.

**Privilegi**: 0, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 1. Da convertire: 1.

| impedimento | testo sintetico |
|---|---|
| Obbedienza | Gli dei di Krynn benedicono i propri sacerdoti con certi poteri, ma pretendono in cambio stretta obbedienza. |

**Armi obbligate**: nessuna.
**Regole di equipaggiamento**: nessuna dichiarata.

**Ambiguità di fonte registrate**:
- Il manuale rimanda al PHB 2e e al Tome of Magic per le tabelle degli incantesimi. Le sfere consentite a ciascun dio sono ora estratte: vedi dati/divinita/.

---

### Truffatore / Prestigiatore — `con-artist`

| campo | valore |
|---|---|
| gruppo 2e | Rogue |
| dado vita | d6 |
| minimi di caratteristica | CAR 12 |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | nessuna restrizione |
| razze ammesse | tutte |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 82, 94 |

**Punti esperienza**: nessuna tabella propria. Il manuale rimanda alle tabelle standard del gruppo Rogue.

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Rogue.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Rogue.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: clone di **Rogue** (SRD 5.1), dado vita 1d8, tiri salvezza Dexterity, Intelligence. Le quattro abilita' potenziate diventano competenze ed Esperienza.

**Privilegi**: 1, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 1. Da convertire: 2.

| privilegio | livello | testo sintetico |
|---|---|---|
| Abilita' specializzate | — | Il truffatore affina Pick Pockets, Move Silently, Hide in Shadows e Read Languages. |

| impedimento | testo sintetico |
|---|---|
| Abilita' sacrificate | Non puo' spendere piu' di dieci punti percentuali iniziali su ciascuna delle altre abilita' da ladro, e non piu' di cinque punti per livello guadagnat. |

**Armi obbligate**: Qualunque arma da ladro.
**Regole di equipaggiamento**: nessuna dichiarata.

---

### Handler — `handler`

| campo | valore |
|---|---|
| gruppo 2e | Rogue |
| dado vita | d6 |
| minimi di caratteristica | nessuno |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | nessuna restrizione |
| razze ammesse | kender |
| ricchezza iniziale | non dichiarata (eredita dal gruppo) |
| pagine PDF | 82, 94 |

**Punti esperienza**: nessuna tabella propria. Il manuale rimanda alle tabelle standard del gruppo Rogue.

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Rogue.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Rogue.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: nessuno, lasciato indeciso. Rogue senza attacco furtivo: il chassis c'e' ma svuotato. Da decidere.

**Privilegi**: 0, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 3. Da convertire: 3.

| impedimento | testo sintetico |
|---|---|
| Nessun attacco alle spalle | Gli handler non ricevono il bonus di attacco alle spalle: sono mossi dalla curiosita', non dalla sete di sangue. |
| Nessuna esperienza dal denaro | Gli handler non ricevono punti esperienza per il denaro trovato. |
| Seguaci limitati | Attirano soltanto seguaci handler, di norma giovani kender di curiosita' intensa. |

**Armi obbligate**: nessuna.
**Regole di equipaggiamento**: nessuna dichiarata.

---

### Popolano — `commoner`

| campo | valore |
|---|---|
| gruppo 2e | Normal |
| dado vita | d6 |
| minimi di caratteristica | nessuno |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | nessuna restrizione |
| razze ammesse | tutte |
| ricchezza iniziale | 2d4x10 stl |
| pagine PDF | 82, 94, 95 |

**Punti esperienza**: tabella presente. 25 livelli (dal 1° al 25°). monotona crescente. Da 0 a 17.000.000 PE.

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Normal.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Normal.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: nessuno, lasciato indeciso. Non e' una classe 5e. Da decidere.

**Privilegi**: 0, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 0. Da convertire: 0.

**Armi obbligate**: nessuna.
**Regole di equipaggiamento**: nessuna dichiarata.

---

### Tinker — `tinker`

| campo | valore |
|---|---|
| gruppo 2e | Normal |
| dado vita | d6 |
| minimi di caratteristica | nessuno |
| livello d'ingresso | 1 |
| classe prerequisito | — |
| allineamento | nessuna restrizione |
| razze ammesse | gnomo-minoi |
| ricchezza iniziale | 2d4x10 stl |
| pagine PDF | 82, 95 |

**Punti esperienza**: tabella presente. 25 livelli (dal 1° al 25°). monotona crescente. Da 0 a 17.000.000 PE.

**THAC0**: citato nel testo della classe, nessuna tabella propria in nessuna delle 17 classi — vale quella del gruppo Normal.
**Tiri salvezza**: nessuna tabella estratta. Il manuale non ne stampa una per classe: valgono le cinque categorie del gruppo Normal.

**Incantesimi**: nessuna progressione propria.

**Chassis 5e (decisione 23)**: nessuno, lasciato indeciso. Non e' una classe 5e. Da decidere.

**Privilegi**: 0, di cui 0 agganciati a un livello esplicito. **Impedimenti**: 1. Da convertire: 1.

| impedimento | testo sintetico |
|---|---|
| Progetti due volte condannati | Ogni progetto di questi gnomi ingegneri e' condannato due volte. |

**Armi obbligate**: nessuna.
**Regole di equipaggiamento**: nessuna dichiarata.

---

