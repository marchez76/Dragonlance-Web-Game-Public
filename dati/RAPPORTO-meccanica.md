# Dove vive la meccanica — misura e proposta, non decisione

*Generato da `dati/analizza_meccanica.py`.*

---

## 0. La domanda, e perche' e' una sola

Delle 17 lacune che la prima fetta verticale ha dichiarato, tre pesano piu'
delle altre e sono la stessa cosa vista da tre lati:

- il personaggio non e' un dato — `attacco` e' un **campo** sul mostro e una
  **funzione** sul personaggio;
- le regole di sistema non hanno sede — d20 + bonus contro CA, 20 critico, 1
  mancato stanno in un file Python;
- un innesco non ha un campo — il motore riconosce il Death Throes **dal
  nome**.

Tutte e tre dicono che c'e' meccanica che vive nel codice invece che nei dati.
Questo documento **non decide**: misura e propone. La decisione e' di
progetto, e la quarta domanda — quanto costa cambiare rotta adesso contro dopo
trenta mostri strutturati — e' la ragione per cui va presa ora e non quando
sara' comoda.

---

## 1. QUALE meccanica sta nei dati e quale nel codice

Il criterio non puo' essere «tutto nei dati»: la risoluzione del d20 e' la
stessa per ogni creatura e non guadagna niente a diventare un dato. Ma non
puo' nemmeno essere «tutto cio' che non varia sta nel codice», perche' il
codice **ha gia' ripetuto se stesso** — la misura e' al §2.

**Proposta: tre domande in ordine, e la prima che risponde decide.**

1. **Varia da portatore a portatore?** → **DATO DI CONTENUTO.** Il danno di
   un'arma, la CD di un tiro salvezza, quali condizioni impone un tratto, e
   **quando un tratto scatta**. Un innesco varia — alla morte, quando si
   viene colpiti, all'inizio del turno — quindi e' un dato, e riconoscerlo
   dal nome e' fragile *per costruzione*, non per pigrizia.
2. **Non varia: e' un valore o una procedura?** Un **valore o una tabella**
   che la fonte stampa — il bonus di competenza per livello, il
   modificatore da punteggio, i moltiplicatori di resistenza e vulnerabilita'
   — e' un **DATO DI SISTEMA**. Una **procedura** — tira, confronta, applica,
   passa il turno — e' **CODICE**.
3. **E' una procedura: quali nomi pronuncia?** I termini che nomina — tipi di
   danno, condizioni, tipi di azione — devono venire da un **vocabolario
   condiviso** e non essere stringhe scritte nel codice. E' gia' la regola di
   decisione 49 (`vocabolario-italiano`), e vale anche quando il consumatore e' il
   motore invece di uno schema.

Applicato a cio' che oggi vive nel codice, il criterio taglia cosi':

| natura | quante | destinazioni proposte |
|---|---|---|
| PROCEDURA | 9 | codice — ma i suoi ingressi sono del Personaggio; codice, con i moltiplicatori come dato di sistema; codice, in una sede dichiarata |
| TABELLA | 4 | dato di sistema; dato di sistema — gia' scritta due volte |
| VARIABILE | 2 | DATO — IA di combattimento, la casella di decisione 27 (`sette-campi-2e`); DATO — un campo `innesco` sul blocco |

Riga per riga:

| regola | oggi in | natura | dove andrebbe |
|---|---|---|---|
| risoluzione dell'attacco: d20 + bonus contro CA, 20 critico, 1 mancato | `motore/combattimento.py` → `def risolvi_attacco` | PROCEDURA | codice, in una sede dichiarata |
| vantaggio e svantaggio: due dadi, il migliore o il peggiore | `motore/combattimento.py` → `def d20` | PROCEDURA | codice, in una sede dichiarata |
| resistenza dimezza, vulnerabilita' raddoppia, immunita' annulla | `motore/combattimento.py` → `def applica_difese` | PROCEDURA | codice, con i moltiplicatori come dato di sistema |
| punti ferita: massimo al 1° livello, media ai successivi | `motore/combattimento.py` → `def pg_fetta` | PROCEDURA | codice — ma i suoi ingressi sono del Personaggio |
| Classe Armatura: base + Destrezza (con tetto) + scudo + stile | `motore/combattimento.py` → `def pg_fetta` | PROCEDURA | codice — ma i suoi ingressi sono del Personaggio |
| iniziativa: modificatore di Destrezza | `motore/combattimento.py` → `def scontro` | PROCEDURA | codice, in una sede dichiarata |
| struttura del round ed economia delle azioni | `motore/combattimento.py` → `def turno` | PROCEDURA | codice, in una sede dichiarata |
| fine dello scontro: quando una parte non puo' piu' agire | `motore/combattimento.py` → `def scontro` | PROCEDURA | codice, in una sede dichiarata |
| a 0 punti ferita: il mostro muore, il personaggio cade incosciente | `motore/combattimento.py` → `def applica_danno` | PROCEDURA | codice, in una sede dichiarata |
| modificatore di caratteristica: (punteggio - 10) diviso 2 | `motore/combattimento.py` → `def mod` | TABELLA | dato di sistema — gia' scritta due volte |
| bonus di competenza per livello | `dati/_srd51.py` → `COMPETENZA` | TABELLA | dato di sistema — gia' scritta due volte |
| bonus di competenza dal grado sfida | `dati/valida_effetti.py` → `def competenza_da_cr` | TABELLA | dato di sistema — gia' scritta due volte |
| CD di un tiro salvezza: 8 + competenza + modificatore | `dati/valida_effetti.py` → `def cd_attese` | TABELLA | dato di sistema |
| quali tratti scattano alla morte del portatore | `motore/combattimento.py` → `TRATTI_ALLA_MORTE` | VARIABILE | DATO — un campo `innesco` sul blocco |
| quando usare una risorsa (sotto meta' dei punti ferita) | `motore/combattimento.py` → `def agisci` | VARIABILE | DATO — IA di combattimento, la casella di decisione 27 (`sette-campi-2e`) |

---

## 2. Serve una SEDE per le regole di sistema?

**Si', per le tabelle. No, per le procedure — a una condizione.**

La prova non e' un'opinione: **il codice ha gia' ripetuto se stesso**, ed e'
lo stesso difetto che il progetto ha chiuso otto volte nei dati, solo che qui
nessuno schema e nessun validatore guarda.

| formula di sistema | scritta in | volte |
|---|---|---|
| modificatore di caratteristica | `dati/valida_effetti.py`, `motore/combattimento.py` | 2 |
| bonus di competenza | `dati/_srd51.py`, `dati/valida_effetti.py` | 2 |

Sono formule identiche, scritte in file che **nessuna esecuzione mette uno
contro l'altro**: se un giorno una venisse corretta e l'altra no, non lo
direbbe nessuno. E' la nona struttura doppia del progetto, ed e' la prima che
vive nel **codice** invece che nei dati — cioe' dove non arrivano ne' gli
schemi ne' i validatori, che sono gli unici strumenti con cui le otto
precedenti sono state chiuse.

**Le tabelle diventano un dato.** Una sede sola — `dati/sistema/`, con il suo
schema — per il bonus di competenza (per livello **e** per grado sfida, che
sono due letture della stessa tabella), il modificatore di caratteristica, la
formula della CD, i moltiplicatori di resistenza e vulnerabilita', le soglie
del 20 e dell'1 naturale. Non e' un terzo tipo di dato accanto a contenuto e
personaggio: e' **lo stesso tipo di dato**, con una cartella in piu' — e per
il progetto significa schema, validatore e riconfronto, cioe' gli strumenti
che gia' esistono.

**Le procedure restano codice, ma non basta dichiararlo.** Dichiarare una sede
e' esattamente cio' che decisione 41 (`sconfessione-condivisa`) ha gia' fatto
per la procedura di sconfessione delle illusioni: «la casa naturale di una
regola di sistema e' uno schema di regole che il progetto non ha ancora». Da
allora la sede promessa ha accumulato **tre inquilini in attesa** — la
sconfessione, il *mindspin* e i Dragon Orbs — e adesso un quarto, che e' la
risoluzione dell'attacco. Una sede dichiarata e mai costruita e' una lista
d'attesa.

La condizione perche' il codice sia una sede legittima e' la stessa che ha
reso accettabile il campo `effetto`: **un riconfronto automatico**. Li' e'
`valida_effetti.py` che mette prosa e struttura una contro l'altra; qui
sarebbe un controllo che rifiuta la stessa formula scritta due volte, e che
oggi avrebbe gia' trovato due casi. Senza quel controllo, «le procedure stanno
nel codice» e' una descrizione, non una regola.

---

## 3. Come si rappresenta il personaggio perche' `attacco` sia la stessa cosa

Il fatto da cui partire: sul mostro `attacco` e' **letto**, sul personaggio e'
**composto** da razza + classe + oggetto + stile. Le due strade ovvie rompono
ciascuna qualcosa di gia' deciso.

- **Far memorizzare `attacco` al personaggio** significa scrivere a mano un
  derivato, che decisione 7 (`doppio-strato`) e CLAUDE.md 3 vietano per una ragione
  gia' pagata quattro volte: si sfasa al primo cambio d'arma o di livello.
- **Far derivare `attacco` al mostro** significa inventare derivazioni che la
  fonte non da'. La prova e' gia' nel corpus e ha un id:
  decisione 50 (`cd-origine-dichiarata`) — la CD 11 del Baaz e' **stampata** e
  combacia col conto per caso, e delle 35 CD del bestiario 6 col conto non
  tornano affatto.

**Proposta: cio' che e' condiviso non e' il campo, e' la LETTURA.**

- La **forma della risposta** e' gia' definita e non cambia:
  `effetto.attacco` di `effetto.schema.json`. Vale per il mostro e per il
  personaggio.
- Il **mostro** porta la risposta come dato, con la sua origine dichiarata —
  esattamente come `cd_origine` fa per la CD. Un `bonus_colpire` letto dalla
  scheda e uno che tornerebbe col conto non sono la stessa cosa, e oggi si
  scrivono uguali.
- Il **personaggio** non porta la risposta: porta gli **ingressi** che non
  sono derivabili — razza, classe, livello, punteggi, equipaggiato, scelte
  fatte — e nient'altro. Ogni campo che si puo' ricavare da quelli **non
  esiste** nello schema Personaggio, che e' la forma piu' forte del divieto:
  la stessa che decisione 39 (`bersaglio-legale-filtro`) ha usato rendendo
  impossibile e non solo sconsigliato fissare un ospite.
- Il **motore** ha **una** funzione `attacco_di(combattente)` che torna
  quella forma: sul mostro la legge, sul personaggio la compone. Chi la usa
  non sa quale dei due casi ha davanti, ed e' questo il senso di «la stessa
  cosa da entrambe le parti».

`motore/combattimento.pg_fetta()` e' oggi la misura di quanto manca: ogni sua
riga che calcola invece di leggere e' una lacuna gia' registrata dall'arena —
i punti ferita al 1° livello, il bonus d'iniziativa, la competenza applicata
all'arma, la Classe Armatura, l'attacco. Non sono cinque problemi: sono cinque
pezzi della stessa procedura, che oggi vive in una funzione di un modulo del
motore e che nello schema Personaggio diventerebbe una **procedura dichiarata
con ingressi dichiarati**.

---

## 4. Cosa costa cambiare rotta ora, e cosa costa dopo

Il costo di un cambio di forma di `effetto` e' il numero di blocchi da
riscrivere, e i blocchi non costano tutti uguale: quelli **generati** si
rifanno con un comando, quelli **scritti a mano** vanno riletti insieme alla
prosa che li accompagna, perche' il controllo 2 di `valida_effetti.py`
pretende che le due dicano la stessa cosa.

| famiglia | blocchi | con `effetto` | come si rifanno |
|---|---|---|---|
| mostri | 257 | 5 | a mano |
| razze | 105 | 0 | a mano |
| classi (features) | 43 | 0 | a mano |
| classi (chassis, generati) | 15 | 15 | con un comando |

**Adesso: 5 blocchi scritti a mano portano `effetto`** — tutti sui mostri, su
2 schede delle 52 convertite; razze e privilegi di classe non ne hanno ancora
nessuno. Piu' 15 generati da `_srd51.py`, che si rifanno con un comando e
quindi non entrano nel costo.

**Dopo trenta mostri strutturati:** il bestiario converte in media 4,9 blocchi
per scheda, quindi trenta schede sono circa **148 blocchi in piu'**, tutti
scritti a mano — circa **30 volte** il lavoro di oggi. E il moltiplicatore e'
la parte ottimista: un blocco di mostro non e' una riga di JSON ma una
**decisione di conversione** con la sua prosa accanto e la sua pagina di
manuale alle spalle, quindi riaprirlo significa riaprire la fonte.

Il verso della lezione e' pero' importante, perche' il progetto ne ha gia'
imparata una **opposta**: decisione 38 (`schema-modelli`) ha aspettato di
avere tre creature prima di disegnare lo schema dei modelli, e decisione 43
(`barbaro-rimandato`) ha rifiutato di disegnare uno schema su un caso solo. Le
due lezioni non si contraddicono se si separa **disegnare** da **convertire in
volume**:

- si disegna quando ci sono **abbastanza casi** — e per le tre domande qui
  sopra i casi ci sono gia': due mostri strutturati, 17 lacune
  misurate, due formule di sistema gia' duplicate, tre inquilini in attesa
  della sede promessa da decisione 41 (`sconfessione-condivisa`);
- si converte in volume **dopo** che la forma e' ferma.

Ne segue la sola raccomandazione operativa di questo documento: **non
convertire i trenta mostri prima di aver deciso dove vive la meccanica.** Oggi
il costo di sbagliare forma e' 5 blocchi; fra trenta schede e' 153, e la
differenza non e' recuperabile con nessuno script.

---

## 5. Cosa questo documento NON tocca

Le tre zone morte di schema — classi, razze, divinita' — restano aperte, e
vanno chiuse **sapendo** dove vive la meccanica, non prima: chiudere uno
schema attorno a una forma che sta per cambiare significa chiuderlo due volte.
La misura di quelle tre sta in `dati/RAPPORTO-zona-morta-classi.md`.

---

*Nessuna decisione e' presa qui. Le tre proposte — il criterio a tre domande,
`dati/sistema/` per le tabelle con un controllo anti-duplicazione per le
procedure, il Personaggio che porta solo gli ingressi — sono proposte, e la
scelta e' di chi legge.*
