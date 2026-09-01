# Lo schema Personaggio — rapporto diagnostico

*Generato da `dati/analizza_personaggio.py` il 2026-09-01.*

> **Diagnostico.** Misura la forma del problema prima di progettarlo. **Non
> decide niente**: non propone uno schema, non scioglie le tre decisioni
> sospese, non tocca `dati/`. Ogni numero è derivato dai JSON; le letture sono
> marcate con un blocco citato e datato.
>
> Il corpus letto è di **506 file** per **1,84 MB**:
> 15 razze, 17 classi, 21 divinità,
> 319 incantesimi, 79 oggetti,
> 52 mostri, 3 modelli.

---

## 0. Perché questo schema è diverso dagli altri

Razza, classe, divinità, mostro, oggetto e modello descrivono **cose che non
cambiano**: sono trascrizione più conversione, e la loro storia è la storia
delle nostre revisioni, non della partita. Un personaggio è la prima entità del
progetto la cui vita è **dentro** la partita.

La differenza si misura, e il numero è netto. Delle grandezze che servono a far
combattere un personaggio, 9 su 27 sono coperte da un
campo pieno, 6 da un campo compilato solo
in parte, e **12 non hanno alcun campo in nessuno schema**
(tabella in §2). Ma la
divisione interessante non è quella: è che **nessuna delle sei entità esistenti
ha un solo campo che cambi durante una partita**. Non è una lacuna da riempire:
è che quella dimensione non è mai stata modellata, perché finora non serviva.

---

## 1. Cosa serve a un personaggio

Tre insiemi, distinti da **chi scrive il valore e quando**.

### 1.1 Scelto in creazione — scritto una volta dal giocatore

Sono le decisioni che nessun file può contenere, perché sono la risposta a un
filtro che i file lasciano aperto. La decisione 35 (`repertori-sono-filtri`) ha già dato il nome alla
cosa: *la fonte dà il filtro e non il campione*. Il personaggio è il posto
dove i filtri vengono **risolti**.

| dato | l'insieme da cui si sceglie | dove sta il filtro oggi |
|---|---|---|
| Razza | 15 voci | `razze.index.json` |
| Classe di partenza | 12 su 17 (le altre 5 hanno `entry_level` > 1) | `classi/*.json` → `mechanics_5e.entry_level` |
| Sei punteggi grezzi | 3 metodi, default `4d6-scarta-minore` | `motore/generazione.py` |
| Assegnazione dei punteggi | libera, fissata o parziale a seconda della razza | `generazione.genera()` → `assegnazione_libera` |
| Aggiustamenti fissi | 1 razza con `editorial_values` (umano-barbaro, decisione 20, `tappo-barbaro`) | `razze/*.json` → `mechanics_5e.ability_adjustments` |
| Scelte lasciate aperte dai tratti | 4 tratti su 15 razze (elfo-dargonesti, umano) | **nessun campo**: la scelta è descritta in prosa dentro il tratto |
| Allineamento | vincolato in 10 classi su 17 | `classi/*.json` → `source_2e.alignment_restriction` (prosa libera) |
| Divinità | 21 voci, solo per le classi sacerdotali | `divinita.index.json` |
| Veste | 3 (Bianca, Rossa, Nera), giurata al 3° livello | `classi/mago-veste-*.json` → `prerequisite_class` |
| Epoca | 5 valori di `valid_eras` | strato editoriale, decisione 12 (`valid-eras`) |
| Competenze di abilità | — | **nessun filtro esiste**: le 18 abilità 5e non sono nei dati |
| Equipaggiamento iniziale | 7 vincoli dichiarati su 17 classi | `mechanics_5e.structural.starting_equipment.constraints` |

### 1.2 Derivato — nessuno lo scrive, si ricalcola

Un valore derivato **non è stato di personaggio**: è una funzione dello stato.
Se finisce nella scheda come campo scrivibile diventa l'ennesima struttura che
descrive una cosa già descritta altrove — il difetto che questo progetto ha
già visto quattro volte.

| grandezza | da cosa si calcola |
|---|---|
| Modificatore di caratteristica | `(punteggio − 10) // 2` |
| Bonus di competenza | solo dal livello: `mechanics_5e.structural.attack_progression.values` |
| Punti ferita massimi | dado vita della classe × livello + mod. COS × livello |
| Classe armatura | `oggetti/*.json` → `armor_5e.ac_formula` + mod. DES + scudo |
| Iniziativa | mod. DES |
| Tiri salvezza | mod. + competenza dalle due di `mechanics_5e.chassis.saving_throws` |
| CD degli incantesimi | 8 + competenza + mod. della caratteristica da incantatore |
| Bonus di attacco | mod. (FOR o DES) + competenza se competente |
| Velocità, taglia, scurovisione | `razze/*.json` → `speed_ft`, `size`, `darkvision_ft` |
| Lista incantesimi accessibile | classe → chassis → `incantesimi.index.json` → filtro sfere per i sacerdoti |
| Carico | somma di `weight_lb` dell'inventario, contro FOR |

### 1.3 Mutevole — cambia durante il gioco

Qui la scala del tempo si spacca in due da sola, e non è una scelta di
progetto: è il ritmo con cui i valori cambiano.

| dato | cambia ogni | esiste in qualche file oggi? |
|---|---|---|
| Punti esperienza e livello | sessione | no |
| Grado cavalleresco raggiunto | sessione | no (decisione 5, `cavalieri-solamnia`) |
| Veste giurata | una volta, al 3° | no (decisione 6, `maghi-delle-torri`) |
| Inventario, equipaggiato, sintonizzato | sessione | no |
| Incantesimi preparati | riposo lungo | no |
| Dadi vita spesi | riposo breve | no |
| Punti ferita correnti e temporanei | **turno** | no |
| Slot spesi per livello | **turno** | no |
| Usi limitati dei privilegi | **turno** | no |
| Condizioni attive | **turno** | no |
| Concentrazione su un incantesimo | **turno** | il campo `concentration` esiste sull'incantesimo, non sul lanciatore |
| Azione / azione bonus / reazione consumate | **turno** | no |
| Posizione e ordine di iniziativa | **turno** | no |
| Tiri salvezza contro morte | **turno** | no |

> **Lettura interpretativa** — registrata il 2026-09-01. Non è derivata dai dati.
>
> **Cosa i dati impongono, prima di qualunque scelta di progetto.** La colonna
> "cambia ogni" si divide in due gruppi senza che nessuno l'abbia deciso:
> 8 righe su 14 cambiano *entro un turno*, le altre
> 6 cambiano su tempi più lunghi — riposo, sessione, o una volta sola in
> tutta la carriera. Non è una tassonomia elegante imposta ai dati: è quello che
> si osserva elencandoli.
>
> Il fatto che pesa di più è nell'ultima colonna: **13 di quelle
> 14 righe non hanno oggi alcuna casa.** Non sono modellate male:
> non sono modellate affatto. Tutte e sei le entità esistenti sono state scritte
> per essere *lette*.
>
> La conseguenza pratica è che lo schema Personaggio non può essere derivato per
> analogia dagli altri cinque, come è stato fatto per oggetto (decisione 33, `schema-oggetti`) e
> modello (decisione 38, `schema-modelli`). Quei due riusavano l'architettura a doppio strato
> perché descrivevano, come gli altri, materiale di fonte convertito. Un
> personaggio non ha una fonte da cui essere convertito: **non c'è un
> `source_2e` di un personaggio**. Il doppio strato, qui, per la prima volta non
> si applica — e questo va detto prima di progettare, non scoperto a metà.

---

## 2. Cosa i nostri dati non coprono

La colonna `stato` non è un giudizio: è misurata sondando il campo in ogni
entità reale.

| grandezza | campo | stato | su cosa |
|---|---|:-:|---|
| Modificatori di caratteristica | — | **assente** | nessun campo lo porta |
| Aggiustamenti razziali | `values` | parziale **13/15** | razze |
| Tetti di crescita | `caps` | **15/15** | razze |
| Vincoli di creazione | `limits` | **15/15** | razze |
| Taglia | `size` | **15/15** | razze |
| Velocità | `speed_ft` | **15/15** | razze |
| Scurovisione | `darkvision_ft` | parziale **11/15** | razze |
| Linguaggi | `languages` | parziale **1/15** | razze |
| Dado vita | `hit_die` | parziale **9/17** | classi |
| Tiri salvezza competenti | `saving_throws` | parziale **9/17** | classi |
| Bonus di competenza per livello | `values` | **17/17** | classi |
| Tabella dei punti esperienza | `system` | **assente** (0/17) | classi |
| Privilegi di classe con meccanica 5e | — | **assente** | nessun campo lo porta |
| Competenze di abilità (le 18 della 5e) | — | **assente** | nessun campo lo porta |
| Competenze in armi e armature | — | **assente** | nessun campo lo porta |
| Pacchetto di equipaggiamento iniziale | `source_wealth` | parziale **4/17** | classi |
| Slot incantesimi 5e | — | **assente** | nessun campo lo porta |
| Lista incantesimi per classe | `classes` | **319/319** | incantesimi |
| Filtro delle sfere per divinità | `mechanics_5e` | **assente** (0/21) | divinità |
| Danno delle armi | `damage_dice` | **37/37** | armi |
| Categoria dell'arma (semplice/da guerra, mischia/distanza) | `categoria` | **assente** (0/37) | armi |
| Gittata dell'arma | `range_ft` | **assente** (0/37) | armi |
| Classe armatura dell'armatura | `ac_formula` | **13/13** | armature e scudi |
| Categoria dell'armatura (leggera/media/pesante) | `categoria` | **assente** (0/13) | armature e scudi |
| Tiro salvezza di un incantesimo | `saving_throw` | **assente** (0/319) | incantesimi |
| Danno di un incantesimo | `damage` | **assente** (0/319) | incantesimi |
| Concentrazione | `concentration` | **319/319** | incantesimi |

### 2.1 I privilegi di classe

Dei **43 fra privilegi e impedimenti** delle 17 classi:
**40** `pending`,
**2** `direct`,
**1** `source_only`.
La decisione 23 (`principio-del-clone`) autorizza il clone del chassis, **non** l'invenzione di
meccanica 5e per i privilegi: il numero non scende scrivendoli.

Ma il buco vero sta un livello più sotto. Il chassis è in `dati/_srd51.py`, che
contiene **5 classi SRD** (Cleric, Fighter, Paladin, Rogue, Wizard)
e di ciascuna **3 campi**: `features`, `hit_dice`, `saves`.
`features` è la **colonna Features della tabella**, cioè i *nomi* dei privilegi
livello per livello. Non c'è una riga di meccanica: nessuna descrizione di
Second Wind, nessuna tabella di slot, nessuna lista di competenze, nessuna
sottoclasse, nessun pacchetto d'equipaggiamento.

> **Lettura interpretativa** — registrata il 2026-09-01. Non è derivata dai dati.
>
> "Clonato" oggi vuol dire **abbiamo registrato quali privilegi ha il Fighter**,
> non **abbiamo le regole del Fighter**. È esattamente il rapporto che c'è fra un
> indice e un testo, ed è stato corretto registrarlo così: `_srd51.py` dichiara
> in testa di essere la colonna Features "senza riscritture".
>
> Il punto è che il conto dei `pending` misura il lavoro sbagliato. Anche
> azzerando tutti e 40 i pending — cioè convertendo
> ogni privilegio *di Krynn* — un Cavaliere della Corona resterebbe ingiocabile,
> perché gli mancherebbero i privilegi del **Fighter**, che non sono `pending`:
> non sono mai stati contati.

### 2.2 Le otto classi senza chassis

**8 classi su 17** non hanno chassis, per decisione:
`commoner`, `handler`, `mago-veste-bianca`, `mago-veste-nera`, `mago-veste-rossa`, `mariner`, `sacerdote-eretico`, `tinker`.
Non hanno dado vita 5e, né tiri salvezza, né progressione. Nessuna di loro può
oggi produrre un personaggio giocabile, nemmeno vuoto.
Le 9 che ce l'hanno usano
Cleric ×1, Fighter ×3, Paladin ×2, Rogue ×1, Wizard ×2.

Su 3 classi il chassis **cambia il dado vita** rispetto
alla fonte (`con-artist` d6→1d8, `mago-alta-stregoneria` 1d4→1d6, `mago-rinnegato` 1d4→1d6).
È corretto e voluto, ma dice una cosa che serve allo schema: sui punti ferita
**la fonte non è autoritativa, lo è il chassis**.

### 2.3 La tabella dei punti esperienza

`structural.xp_table.applied` è `false` in **17
classi su 17** — cioè in tutte. Le progressioni 2e restano in
`source_2e` come dato storico, e **la tabella 5e che doveva sostituirle non
esiste in nessun file**. Un personaggio sale di livello e nessun dato del
progetto dice a quanti punti esperienza.

### 2.4 Le competenze

Nei dati ci sono **42 voci** di competenza in armi e **66** di
competenza non-d'arma, tutte in inglese e tutte dal sistema **a slot** della 2e
che l'incompatibilità 4 della decisione 23 (`principio-del-clone`) ha abolito. Del sistema che l'ha
sostituito — competenza per categoria, più le 18 abilità della 5e — nei dati
non c'è nulla: né l'elenco delle abilità, né quante ne concede una classe, né
quali. E gli oggetti non portano la categoria su cui la competenza si
appoggerebbe: `weapon_5e` non ha un campo categoria (semplice / da guerra) e
`armor_5e` non ha leggera / media / pesante.

Il caso più netto è l'Umano. La decisione 19 (`compensazione-umano`) lo compensa con tre tratti che
sono tutti **scelte**: un +1 a due caratteristiche, una competenza di abilità,
un linguaggio. Sono 4 in tutto i tratti razziali che lasciano una
scelta al giocatore (elfo-dargonesti, umano), e per nessuno dei tre
dell'Umano esiste oggi né l'insieme da cui pescare né il campo in cui scrivere
il risultato: la scelta vive come prosa dentro `traits[].mechanics_5e`.

### 2.5 La valuta

**4 classi su 17** dichiarano una ricchezza
iniziale, espressa in **pezzi d'acciaio** (`stl`). Tutti gli oggetti portano
`cost_gp`, in **pezzi d'oro**. Nessun campo, in nessuno schema, dichiara il
cambio fra le due. Oggi un personaggio non può comprare il proprio
equipaggiamento perché non esiste un'aritmetica che colleghi il suo borsello
al listino.

### 2.6 Gli incantesimi

I 319 incantesimi hanno livello, scuola, classi, componenti,
tempo di lancio, gittata, durata, rituale e concentrazione — tutti
strutturati. Non hanno **nessun campo per il tiro salvezza, il danno, l'area o
il bersaglio**: quelle informazioni stanno dentro `descrizione`, in prosa
inglese dell'SRD. Il motore d'arena può dire *quali* incantesimi un personaggio
conosce, e non può risolverne nemmeno uno.

Manca inoltre **la tabella degli slot 5e**. Le uniche tabelle di slot nel
progetto sono 2e: `source_2e.spell_progression`, presente in
4 classi su 17.

### 2.7 I giunti che non sono agganciati

Tre legami esistono come intenzione ma non come chiave.

- **`allowed_classes` → classi.** Le razze dichiarano
  17 etichette distinte, prese dalla tabella
  Class/Race Combinations. **Nessuna è un id.** Solo
  **5** coincidono con il `name.en` di una nostra classe
  (Barbarian, Cavalier, Handler, Mariner, Tinker); le altre 12 vanno
  mappate a mano, e **6** non condividono nemmeno una
  parola con una nostra classe (Bard, Fighter, Illusionist, Paladin, Ranger, Thief).
  Fra queste c'è **l'etichetta più frequente di tutte**, `Fighter`,
  concessa da 12 razze su 15: la tabella del
  manuale elenca il roster generico della 2e, di cui il progetto ha convertito
  solo le voci proprie di Krynn. E **12 classi su
  17** non sono nominate da nessuna etichetta.
- **classe → incantesimi.** Il catalogo elenca le classi in `classes` con i
  nomi SRD (Wizard, Cleric…), non con i nostri id. Il ponte è
  `mechanics_5e.chassis.srd_class`, che però è `null` per
  8 classi.
- **divinità → incantesimi.** Tutte e 21 le divinità hanno
  `mechanics_5e` a **`null`**: il filtro delle sfere (decisione 24, `sfere-sacerdotali`) vive
  interamente in `dati/_sfere_5e.py`, cioè in codice, non nei dati.

> **Lettura interpretativa** — registrata il 2026-09-01. Non è derivata dai dati.
>
> I tre giunti hanno la stessa forma e non è un caso: il legame è sempre scritto
> come **etichetta leggibile**, mai come chiave. Finché i dati servivano a essere
> consultati la differenza non si vedeva; un motore di creazione la incontra al
> primo passo, perché "quali classi può fare un Nano delle Colline" è
> letteralmente la prima domanda che deve rispondere.
>
> Va detto con precisione che cosa manca, perché non è la stessa cosa nei tre
> casi. Su `allowed_classes` non manca un campo: manca **una decisione**. Alcune
> etichette denotano una nostra classe scritta in altro modo, altre nominano
> classi generiche della 2e che il progetto non ha e per le quali non esiste
> nulla da agganciare. Stabilire quale sia quale è lavoro di conversione, e
> scriverlo qui al posto tuo sarebbe la stessa scorciatoia che la decisione 26 (`criterio-tracciabilita`)
> respinge altrove: un dato non verificabile che entra perché sembra ovvio.

---

## 3. Le tre decisioni sospese

Riportate, non sciolte.

### 3.1 Il Barbaro: razza o background

**Cosa dice la fonte.** *Tales of the Lance* tratta "Barbarian" in due
capitoli: come cultura umana e come classe. Le due voci non coincidono. La
scheda razziale dichiara
5 vincoli di caratteristica
(COS min 12, DES min 8/max 16, INT max 18, FOR min 10, SAG min 8),
la voce di classe dichiara 4 minimi
(COS 12, DES 8, FOR 10, SAG 8).
La decisione 11 (`barbaro-vincoli`) ha applicato l'**unione** dei due set. Il manuale registra
1 ambiguità dichiarata su questa classe.

**Lo stato attuale.** `umano-barbaro` è l'unica razza il cui blocco
`ability_caps` dichiara **2 tetti su 6**
(DES 16, INT 18), ed è la sola fra le 15 con aggiustamenti
puramente editoriali: COS +1, FOR +1,
con `source_values` vuoto
— cioè **nessun aggiustamento viene dalla fonte**. Porta
2 tratti.

**Cosa resta aperto.** La decisione 20 (`tappo-barbaro`) elenca già le quattro conseguenze del
passaggio a background, e sono tutte verificabili nei dati:

| conseguenza | misura oggi |
|---|---|
| Il roster razziale scende | 15 → 14 voci |
| Il tetto DES 16 perde la sede | nessuno schema del progetto ha un contenitore `background` |
| Il Monte Carlo sull'Aghar barbaro perde l'oggetto | la combinazione misurata allo 0,249% è razza × classe |
| I due aggiustamenti editoriali vanno rimotivati | COS +1, FOR +1, oggi giustificati come pagamento del tetto DES 16 |

Le opzioni sul tavolo restano tre: **tenere** il tappo (nessun costo, il
difetto resta), **convertire a background** (richiede uno schema che non
esiste), **tenere la razza e spostare solo i tratti**. Nessuna è preferita qui.

### 3.2 I tetti di crescita

**Cosa dicono i dati.** Su 90 caselle
(15 razze × 6 caratteristiche),
**84 tetti dichiarati sono sotto il soffitto 20 della
5e**. In media una razza perde **15,0 punti** sul soffitto complessivo
di 120.

| razza | somma dei tetti | punti sottratti al soffitto 5e | tetti dichiarati |
|---|---:|---:|:-:|
| Nano Sozzo (Aghar) | 75 | 45 | 6/6 |
| Gnomo (Minoi) | 102 | 18 | 6/6 |
| Nano delle Colline (Neidar) | 102 | 18 | 6/6 |
| Elfo Kagonesti | 103 | 17 | 6/6 |
| Kender | 105 | 15 | 6/6 |
| Nano delle Montagne (Hylar / Daewar) | 106 | 14 | 6/6 |
| Irda (Alto Ogre) | 108 | 12 | 6/6 |
| Mezzelfo | 108 | 12 | 6/6 |
| Minotauro | 108 | 12 | 6/6 |
| Umano | 108 | 12 | 6/6 |
| Elfo Dargonesti (Elfo degli Abissi) | 109 | 11 | 6/6 |
| Elfo Dimernesti (Elfo dei Bassifondi) | 109 | 11 | 6/6 |
| Elfo Qualinesti | 109 | 11 | 6/6 |
| Elfo Silvanesti | 109 | 11 | 6/6 |
| Barbaro | 114 | 6 | 2/6 |

Le caselle che il manuale non dichiara sono contate al soffitto 20:
il Barbaro risulta quindi il meno limitato solo perché
4 dei suoi 6 tetti **non esistono**, non
perché siano alti. È la stessa asimmetria della sezione 3.1.

**Cosa mette in tensione.** I chassis concedono da **5** a
**7** Ability Score Improvement (Fighter è il più
generoso), cioè fino a **14 punti** da distribuire in
vent'anni di carriera:
Cleric 5, Fighter 7, Paladin 5, Rogue 6, Wizard 5.
Il tetto morde di sicuro, e la decisione dice *che* morde, non *cosa succede
quando morde*.

**Cosa la fonte non dice.** In AD&D 2e i massimali erano limiti di
**generazione**: il sistema non aveva un meccanismo di aumento paragonabile
agli ASI, quindi il caso "un aumento sfonda il tetto" **non esiste nel manuale
sorgente**. Non c'è una risposta da trascrivere: è una questione che nasce
dalla conversione.

**Dove il buco è già visibile nel codice.**
`generazione.tetto_crescita()` restituisce **20** quando il manuale
non dichiara un massimale — e 1 razza
(umano-barbaro) ha tetti dichiarati solo su
alcune caratteristiche. La funzione dice qual è il tetto; **nessuna funzione,
in nessun modulo, dice cosa fare del punto che lo supera.**

Le opzioni restano almeno quattro: il punto **si perde**; si **travasa** su
un'altra caratteristica; il tetto è **morbido** e la 5e vince; l'ASI diventa
un **talento** — che però oggi è impossibile, perché nel progetto non esiste
alcun catalogo di talenti.

### 3.3 La generazione delle caratteristiche

`motore/generazione.py` esiste: **267 righe**, **13
funzioni pubbliche** (`applica_aggiustamenti()`, `carica_classe()`, `carica_razza()`, `esiste_assegnazione()`, `formule_razziali()`, `genera()`, `intervalli()`, `metodi_praticabili()`, `tetto_crescita()`, `tira_4d6_scarta_minore()`, `tira_formula()`, `valida()`, `valida_pointbuy()`).

**Cosa copre.** I 3 metodi
(`4d6-scarta-minore`, `array-standard`, `point-buy`) con default
`4d6-scarta-minore`; le formule razziali per singola caratteristica, comprese le
sei dell'Aghar e la Forza del Kender; gli aggiustamenti; l'unione dei vincoli
razza + classe; la validazione; la soddisfacibilità (`esiste_assegnazione`,
`metodi_praticabili`); il tetto di crescita.

**Cosa manca.**

| buco | cosa succede oggi |
|---|---|
| Nessuna funzione **assegna** i valori | `esiste_assegnazione` dice *se* una disposizione legale esiste, poi la butta via |
| Il point-buy non si compone con le formule razziali | `genera()` solleva un'eccezione per il point-buy; il Kender ha la FOR fissata da formula e non c'è una via che le combini |
| Nessun aggancio ai tetti di conversione | il modulo legge `source_2e` 6 volte e `mechanics_5e` 0: scavalca lo strato di conversione e va dritto alla fonte |
| `genera()` restituisce tre forme diverse | dict, lista, o dict di due chiavi, con un terzo stato `parziale`: chi chiama deve ramificare |
| Copre un passo su molti | punti ferita, competenze, equipaggiamento, incantesimi, denaro iniziale: nessuno di questi passa di qui |
| La numerazione delle decisioni era sfasata — CHIUSA | il modulo cita ora le decisioni 8 (`generazione-caratteristiche`), 9 (`aggiustamenti-negativi`), 10 (`massimali-razziali`), 11 (`barbaro-vincoli`), verificate da `verifica_decisioni.py` — vedi §3.4 |

> **Lettura interpretativa** — registrata il 2026-09-01. Non è derivata dai dati.
>
> Sul terzo punto vale la pena fermarsi, perché è l'unico che sia un difetto e
> non un lavoro non ancora fatto. Il modulo legge `source_2e` e non
> `mechanics_5e` — e oggi non se ne accorge nessuno, perché i due strati
> combaciano: il confronto campo per campo su 90 caselle dà
> **0 divergenze** sui tetti e **0** sui vincoli di
> creazione.
>
> Combaciano perché `build_razze.py` li scrive entrambi dalla stessa fonte. È il
> punto 2 di CLAUDE.md che funziona: la coerenza è tenuta dal generatore, non
> dalla disciplina di chi legge. Ma vuol dire che il giorno in cui una revisione
> toccherà un tetto **in `mechanics_5e`** — che è per definizione lo strato
> rivedibile — il motore continuerà a leggere il valore vecchio senza segnalare
> niente.

### 3.4 Una nota che riguarda tutte e tre: la numerazione — CHIUSA

Le tre questioni sospese si citano per numero, e i numeri **non erano
stabili**. Il progetto contiene **977 rimandi a una decisione in
109 file**, di cui **288 nella fascia 1-12** — che è
esattamente dove stavano le tre questioni di questa sezione.

Erano sfasati perché il numero è un ordinale dell'elenco, e l'elenco è
cambiato: file scritti in momenti diversi hanno continuato a citare il numero
della propria vintage, senza che nulla li riallineasse. Lette una per una, le
288 citazioni della fascia bassa hanno dato questa corrispondenza —
**senza uno scarto costante**, e con lo stesso numero giusto in un file e
sbagliato in un altro:

| numero citato allora | contenuto citato | id | numero vero |
|---|---|---|:-:|
| «2» | i minimi di caratteristica sono vincoli meccanici | `vincoli-caratteristica` | **3** |
| «3» | i limiti di livello aboliti | `limiti-di-livello` | **4** |
| «4» | i limiti di livello aboliti | `limiti-di-livello` | **4** — coincideva |
| «9» | il default è 4d6 scarta il minore | `generazione-caratteristiche` | **8** |
| «10» | gli aggiustamenti negativi si tengono | `aggiustamenti-negativi` | **9** |
| «11» | i massimali valgono anche in crescita | `massimali-razziali` | **10** |
| «12» | il Barbaro tiene entrambi i set di vincoli | `barbaro-vincoli` | **11** |
| «23» | il principio del clone | `principio-del-clone` | **23** — coincideva |

**Chiusa il 2026-09-01, e non correggendo i numeri.** Correggerli sarebbe
stato il quinto giro di vigilanza su una struttura che si sfasa da sola. La
causa è che il numero di un rimando è un **derivato scritto a mano**, cioè
esattamente ciò che il punto 3 di CLAUDE.md vieta ovunque tranne che qui.

Quindi: l'elenco canonico è passato in `decisioni.py`, ogni decisione ha preso
un `id` stabile che non cambierà mai, e la forma di un rimando è ora
«decisione 10 (`massimali-razziali`)» — l'id è la chiave, il numero gli sta
accanto come derivato. `verifica_decisioni.py` verifica la coppia in tutto il
progetto e con `--correggi` riscrive i numeri a partire dagli id.

Stato oggi: **977 rimandi verificati, 0 sfasati,
0 con id ignoto, 0 ancora senza id**. Rinumerare
adesso costa un comando.

---

## 4. La questione strutturale: riferimento o copia

### 4.1 Il precedente, misurato

Il progetto ha già una coppia di strutture che descrivono la stessa cosa:
`_sfere_5e.LISTA_BASE` (105 voci: nome, livello, scuola) e il
catalogo `dati/incantesimi/` (319 voci). Si incrociano **per nome
inglese**, non per id.

Confronto fatto adesso, su 3 campi per voce:
**0 voci assenti dal catalogo**,
**0 divergenze di livello**,
**0 di scuola**. Le
37 voci marcate `Cleric` nel catalogo e non presenti in
`LISTA_BASE` sono esattamente gli incantesimi di Dominio, che il modulo
dichiara di escludere.

I due insiemi sono dunque **perfettamente allineati** — e fino al
01/09/2026 **nessuno lo verificava**: `verifica_sfere.py` leggeva
`LISTA_BASE` e `dati/divinita/`, e non apriva mai `dati/incantesimi/`.

Ora lo verifica. Il confronto sta in `verifica_sfere.confronta_catalogo()`,
è **bloccante**, e questa sezione non lo rifà: ne riporta l'esito
(0 divergenze). Il quarto controllo è sull'**insieme** degli
esclusi di Dominio — 37 nomi dichiarati in
`_sfere_5e.ESCLUSI_DI_DOMINIO` — e non sul loro numero, perché un
incantesimo che entra mentre un altro esce lascerebbe il conteggio fermo.

> **Lettura interpretativa** — registrata il 2026-09-01. Non è derivata dai dati.
>
> **L'allineamento perfetto è il dato interessante, non quello rassicurante.**
> Le quattro divergenze già viste in questo progetto non sono nate da distrazione:
> sono nate da strutture che combaciavano il giorno in cui sono state scritte.
> Questa era la quinta di quelle strutture, e stava al giorno uno: per questo
> il confronto è stato aggiunto invece di limitarsi a registrare che oggi
> combaciano.
>
> Da qui viene l'argomento sulla domanda posta, e non da una preferenza di stile.

### 4.2 Proposta: riferimento per id, con tre eccezioni nominate

**Il personaggio referenzia per id e non copia valori.** Non perché la copia
sfasi in astratto, ma per una ragione che si misura sui dati di oggi:
**40 privilegi su 43 sono `pending`**
e 8 classi su 17 non hanno chassis. Le classi
*cambieranno*, molto e presto. Un personaggio che ne avesse copiato i valori
resterebbe fermo alla versione del giorno in cui è stato creato, e — questo è
il punto — **senza saperlo**: non c'è modo di distinguere un valore copiato
apposta da uno rimasto indietro.

Il costo del riferimento, che è reale, è quello nominato nella domanda: il
personaggio dipende da file esterni. Ma il rischio non è la dipendenza — è la
dipendenza **non datata**. Tre correttivi, tutti già in uso altrove nel
progetto:

1. **Impronta del corpus.** Il personaggio registra contro quale versione dei
   dati è stato costruito. Un personaggio più vecchio di una revisione diventa
   così **rilevabile**, invece di essere reinterpretato in silenzio. È la stessa
   funzione che `pages_pdf` svolge per la trascrizione: non conserva il dato,
   conserva il modo di ritrovarlo.
2. **Si copia solo ciò che risolve un filtro.** Quando la fonte dà un insieme
   e il giocatore ne sceglie un elemento, quella scelta **non esiste in nessun
   file** e deve stare sul personaggio: l'assegnazione dei sei punteggi, il
   +1/+1 dell'umano, l'arma scelta fra "Sword (any)", le competenze. È la
   decisione 39 (`bersaglio-legale-filtro`) applicata al PG: *il bersaglio legale è un filtro*, e il
   campione si fissa alla generazione. Non è una copia dei dati — è il
   complemento dei dati.
3. **I derivati non si scrivono.** Nessun campo `ca`, `pf_max`, `bonus_attacco`
   scrivibile nella scheda: si ricalcolano. Uno stato che si può ricostruire e
   che viene invece salvato è, per definizione, una struttura in più che
   descrive una cosa già descritta.

Resta una tensione onesta da segnalare, non da risolvere qui: i punti ferita
**massimi** sono un derivato, ma se tirati a ogni livello (invece che a media
fissa) sono anche un evento irripetibile, e allora vanno salvati i *tiri*, non
il totale. Lo stesso vale per la ricchezza iniziale, se tirata.

---

## 5. Il vincolo dell'arena

### 5.1 Non è un problema di velocità

Il corpus intero è **506 file per 1,84 MB**. Caricato una
volta all'avvio e indicizzato per id, ci sta in memoria senza discussione: gli
indici `*.index.json` esistono già e fanno esattamente questo mestiere.
**A ogni turno non va letto nessun file.** La domanda "quanto velocemente" ha
una risposta noiosa, ed è quella giusta.

### 5.2 È un problema di forma

Il problema è che i valori che servono a ogni turno, in buona parte, **non
esistono come numeri**.

Quello che è già numero, sui 52 mostri:

| grandezza | copertura |
|---|:-:|
| `armor_class.value` | **52/52** |
| `hit_points.average` | **52/52** |
| `abilities` | **52/52** |
| `speed.walk` | **52/52** |
| `challenge_rating.value` | **52/52** |
| `passive_perception` | **52/52** |

Quello che è prosa: **405 blocchi di meccanica in tutto** —
257 fra azioni, tratti e reazioni dei mostri,
105 tratti razziali, 43 privilegi di classe.
Il campo si chiama `mechanics_5e` ed è una **stringa in italiano**: un'azione
di attacco è scritta nella forma *"+N a colpire, portata N piedi, un bersaglio,
N (NdN+N) danni di un certo tipo"*. Tutto quello che serve c'è; nulla di quello
che serve è un campo. Leggibile da una persona, non da un motore.

Anche dove il dato è strutturato, il numero è spesso **dentro** una stringa:

- `armor_5e.ac_formula` — solo 4 armature portano un
  numero secco; **8 portano una formula** da interpretare
  (`"14 + Dex modifier (max 2)"`) e 1 un modificatore
  (lo scudo).
- `weapon_5e.properties` — 17 proprietà distinte, di cui
  **10 contengono un numero** annegato nel testo, per
  21 occorrenze in tutto (`"versatile (1d10)"`,
  `"ammunition (range 150/600)"`). La gittata di un'arma a distanza si può oggi
  ottenere solo con un'espressione regolare.
- Gli incantesimi non hanno campi per danno e tiro salvezza (§2.6).

### 5.3 Cosa il motore deve poter fare a ogni turno

| operazione | legge | scrive | praticabile oggi? |
|---|---|---|---|
| Ordine di iniziativa | mod. DES dei partecipanti | l'ordine | **sì** |
| Attacco con arma | bonus attacco, CA del bersaglio, dadi di danno | PF del bersaglio | **no**: la CA del bersaglio c'è, il bonus d'attacco no — sul PG manca la competenza, sul mostro è dentro la prosa |
| Attacco di un mostro | il blocco `actions` | PF del bersaglio | **no**: è prosa |
| Lancio di un incantesimo | slot disponibili, CD, effetto | slot spesi, PF, condizioni | **no**: l'effetto non è strutturato |
| Uso di un privilegio | usi rimasti, effetto | usi consumati | **no**: 40 privilegi su 43 sono `pending` |
| Condizioni e concentrazione | condizioni attive | condizioni attive | **no**: non esiste un elenco delle condizioni |
| Decisione dell'IA | ruolo e morale della creatura | l'intenzione | **sì**: `ruolo` su 52/52, `morale_2e` su 52/52 |

I 9 ruoli già assegnati
(bruto 13, fante 10, bestia 10, assassino 8, incantatore 3, artiglieria 3, non-combattente 2, sciame 2, comandante 1) e il morale
della decisione 27 (`sette-campi-2e`) sono, oggi, la parte dell'arena messa meglio: l'IA sa cosa
vuole fare una creatura molto prima che il motore sappia risolverne l'attacco.

> **Lettura interpretativa** — registrata il 2026-09-01. Non è derivata dai dati.
>
> **La scheda non è progettata male: è progettata per un altro uso.** Tutte e sei
> le entità sono documenti di conversione — devono mostrare cosa dice la fonte,
> cosa ne abbiamo fatto e perché. Per quello servono la prosa, la nota, lo stato
> di conversione, la provenienza. Un motore di combattimento vuole l'opposto:
> numeri, senza contesto.
>
> Sono due usi legittimi degli stessi fatti, e il progetto ha già il modo di
> tenerli insieme senza duplicarli: **`dati/*.index.json`**. Un indice non è una
> seconda verità, è una proiezione derivata dalla prima, rigenerata dal
> generatore — il punto 2 di CLAUDE.md. La domanda che lo schema Personaggio
> dovrà affrontare non è quindi "riferimento o copia" soltanto, ma anche se
> l'arena legga le schede o una **proiezione di combattimento** derivata da esse.
>
> Il criterio per distinguere le due cose esiste già ed è verificabile: se un
> valore può essere ricalcolato dai file, è una proiezione e va rigenerata; se
> non può, è stato ed è del personaggio.
>
> Va detto anche il rovescio, perché è il costo dell'intera sezione: finché i
> 405 blocchi di meccanica restano prosa, **nessuna proiezione può
> derivarli**. Trasformarli in numeri non è un lavoro di formato, è la stessa
> conversione dei `pending` vista da un'altra angolazione — e riguarda anche i
> 257 blocchi dei mostri, che oggi risultano "convertiti".

---

## In sintesi

| domanda | risposta breve |
|---|---|
| 1. Cosa serve | su 27 grandezze: 9 coperte, 6 parziali, 12 senza alcun campo; e nessuna entità esistente ha un campo che cambi in partita |
| 2. Cosa manca | i privilegi del chassis (non contati fra i 40 `pending`), la tabella PE 5e (17/17 non applicata), le competenze 5e, gli slot 5e, l'effetto degli incantesimi, il cambio stl/gp |
| 3. Le tre sospese | riportate con fonte e opzioni, non sciolte |
| 4. Riferimento o copia | riferimento per id, più impronta del corpus, più le sole scelte che risolvono un filtro; i derivati non si scrivono |
| 5. Arena | 1,84 MB stanno in memoria: il vincolo non è la velocità ma che 405 blocchi di meccanica sono prosa |

---

*Nessuna decisione è presa in questo documento. Le tre questioni della sezione
3 restano aperte, e lo schema non è progettato.*
