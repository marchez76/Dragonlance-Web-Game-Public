# Dove vive la meccanica — la decisione presa, e cosa il controllo vede

*Generato da `dati/analizza_meccanica.py`.*

---

## 0. La domanda, e come e' stata chiusa

Delle 17 lacune che la prima fetta verticale ha dichiarato, tre pesavano piu'
delle altre ed erano la stessa cosa vista da tre lati:

- il personaggio non era un dato — `attacco` era un **campo** sul mostro e una
  **funzione** sul personaggio;
- le regole di sistema non avevano sede — d20 + bonus contro CA, 20 critico, 1
  mancato stavano in un file Python;
- un innesco non ha un campo — il motore riconosce il Death Throes **dal
  nome**.

Le prime due sono chiuse: decisione 51 (`criterio-meccanica`) dice dove vive
la meccanica, decisione 52 (`attacco-unica-lettura`) dice che `attacco` si
legge una volta sola. La terza resta aperta ed e' la lacuna
`innesco-non-dichiarato`.

Questo documento non e' piu' una proposta: e' la **misura della decisione
presa**. Le due domande a cui risponde adesso sono diverse da prima — cosa il
controllo anti-duplicazione riesce a vedere (§2), e cosa e' cambiato nel
registro delle lacune (§3).

---

## 1. QUALE meccanica sta nei dati e quale nel codice

Il criterio non poteva essere «tutto nei dati»: la risoluzione del d20 e' la
stessa per ogni creatura e non guadagna niente a diventare un dato. Ma non
poteva nemmeno essere «tutto cio' che non varia sta nel codice», perche' il
codice **aveva gia' ripetuto se stesso**.

La regola e' decisione 51 (`criterio-meccanica`): **tre domande in ordine, e
la prima che risponde decide.**

1. **Varia da portatore a portatore?** → **DATO DI CONTENUTO.** Il danno di
   un'arma, la CD di un tiro salvezza, quali condizioni impone un tratto, e
   **quando un tratto scatta**. Un innesco varia — alla morte, quando si viene
   colpiti, all'inizio del turno — quindi e' un dato, e riconoscerlo dal nome
   e' fragile *per costruzione*, non per pigrizia.
2. **Non varia: e' un valore o una procedura?** Un **valore o una tabella**
   che la fonte stampa — il bonus di competenza per livello, il modificatore
   da punteggio, i moltiplicatori di resistenza e vulnerabilita' — e' un
   **DATO DI SISTEMA**. Una **procedura** — tira, confronta, applica, passa il
   turno — e' **CODICE**.
3. **E' una procedura: quali nomi pronuncia?** I termini che nomina — tipi di
   danno, condizioni, tipi di azione — devono venire da un **vocabolario
   condiviso** e non essere stringhe scritte nel codice. E' gia' la regola di
   decisione 49 (`vocabolario-italiano`), e vale anche quando il consumatore
   e' il motore invece di uno schema. E' la domanda che ha portato a decisione
   53 (`condizioni-vocabolario-srd`): le condizioni che un mostro dichiara di
   ignorare sono nomi, e i nomi vengono dal vocabolario anche quando il motore
   non sa ancora applicarli.

Applicato a cio' che vive nel codice, il criterio taglia cosi':

| natura | quante | chiuse | aperte | sede |
|---|---|---|---|---|
| PROCEDURA | 11 | 8 | 3 | codice |
| TABELLA | 6 | 6 | 0 | `dati/sistema/` |
| VARIABILE | 3 | 0 | 3 | dato di contenuto — il campo non esiste ancora |

Riga per riga:

| regola | vive in | natura | dove | stato |
|---|---|---|---|---|
| risoluzione dell'attacco: d20 + bonus contro CA, 20 critico, 1 mancato | `motore/combattimento.py` → `def risolvi_attacco` | PROCEDURA | codice; le sue tre soglie sono dati di sistema | chiusa |
| vantaggio e svantaggio: due dadi, il migliore o il peggiore | `motore/combattimento.py` → `def d20` | PROCEDURA | codice | chiusa |
| l'attacco: campo sul mostro, composizione sul personaggio | `motore/combattimento.py` → `def attacco_di` | PROCEDURA | codice, una lettura sola per entrambi i lati | chiusa |
| resistenza dimezza, vulnerabilita' raddoppia, immunita' annulla | `motore/combattimento.py` → `def applica_difese` | PROCEDURA | codice; moltiplicatori e ordine sono dati di sistema | chiusa |
| un'immunita' a condizione si confronta per id | `motore/combattimento.py` → `def applica_esito` | PROCEDURA | codice; i nomi vengono dal vocabolario condiviso | chiusa |
| punti ferita: massimo al 1° livello, media ai successivi | `motore/combattimento.py` → `def pf_di` | PROCEDURA | codice, con gli ingressi del Personaggio | chiusa |
| Classe Armatura: base + Destrezza (con tetto) + scudo + stile | `motore/combattimento.py` → `def ca_di` | PROCEDURA | codice, con gli ingressi del Personaggio | chiusa |
| struttura del round ed economia delle azioni | `motore/combattimento.py` → `def turno` | PROCEDURA | codice | chiusa |
| iniziativa: modificatore di Destrezza | `motore/combattimento.py` → `def scontro` | PROCEDURA | codice, ma nessun campo porta il bonus | aperta — lacuna `iniziativa` |
| fine dello scontro: quando una parte non puo' piu' agire | `motore/combattimento.py` → `def scontro` | PROCEDURA | codice, ma la definizione non e' dichiarata da nessun dato | aperta — lacuna `fine-dello-scontro` |
| a 0 punti ferita: il mostro muore, il personaggio cade incosciente | `motore/combattimento.py` → `def applica_danno` | PROCEDURA | codice; i tiri salvezza contro morte non sono modellati | aperta — lacuna `tiri-salvezza-contro-morte` |
| modificatore di caratteristica | `dati/_sistema.py` → `def modificatore` | TABELLA | `dati/sistema/modificatore-caratteristica.json` | chiusa |
| bonus di competenza per livello | `dati/_sistema.py` → `def competenza` | TABELLA | `dati/sistema/bonus-competenza.json`, lettura `per_livello` | chiusa |
| bonus di competenza dal grado sfida | `dati/_sistema.py` → `def competenza_da_grado_sfida` | TABELLA | la STESSA tabella, lettura `per_grado_sfida` | chiusa |
| CD di un tiro salvezza: 8 + competenza + modificatore | `dati/_sistema.py` → `def cd_salvezza` | TABELLA | `dati/sistema/cd-tiro-salvezza.json`, con gli addendi riferiti per id | chiusa |
| moltiplicatori delle difese, e il loro ordine di applicazione | `dati/_sistema.py` → `MOLTIPLICATORI` | TABELLA | `dati/sistema/moltiplicatori-difesa.json` | chiusa |
| soglie del 20 e dell'1 naturale | `dati/_sistema.py` → `CRITICO_NATURALE` | TABELLA | `dati/sistema/soglie-d20.json` | chiusa |
| quali tratti scattano alla morte del portatore | `motore/combattimento.py` → `TRATTI_ALLA_MORTE` | VARIABILE | DATO — un campo `innesco` sul blocco | aperta — lacuna `innesco-non-dichiarato` |
| quando usare una risorsa (sotto meta' dei punti ferita) | `motore/combattimento.py` → `def agisci` | VARIABILE | DATO — IA di combattimento, la casella di decisione 27 (`sette-campi-2e`) | aperta — lacuna `quando-usare-una-risorsa` |
| da dove viene il bonus di attacco di un mostro | `motore/combattimento.py` → `def attacco_di` | VARIABILE | DATO — un `bonus_origine` accanto a `bonus_colpire` | aperta — lacuna `attacco-origine-non-dichiarata` |

Le 6 righe aperte non sono un difetto del criterio: sono il criterio che le ha
**nominate**. 3 di esse dicono la stessa cosa — un dato che dovrebbe esistere
e non esiste: l'innesco di un tratto, la politica d'uso di una risorsa,
l'origine del bonus d'attacco di un mostro — e nessuna delle 3 si chiude
scrivendo codice.

---

## 2. La sede delle regole di sistema, e il controllo che la tiene ferma

`dati/sistema/` esiste, con il suo schema e il suo validatore. Contiene 5 dati
che coprono **81 ingressi**:

| dato di sistema | genere | letture | ingressi |
|---|---|---|---|
| `bonus-competenza` | tabella | `per_livello`, `per_grado_sfida` | 51 |
| `cd-tiro-salvezza` | formula | — | — |
| `modificatore-caratteristica` | tabella | `per_punteggio` | 30 |
| `moltiplicatori-difesa` | moltiplicatori | — | — |
| `soglie-d20` | soglie | — | — |

Il bonus di competenza e' **una tabella con due letture** — per livello del
personaggio e per grado sfida del mostro — e questa e' la prova che la sede
serviva: prima erano due scritture in due file, e nessuna esecuzione le
metteva una contro l'altra.

**La sede da sola non chiude niente.** Spostare una formula dal codice a un
JSON impedisce la divergenza solo se qualcosa impedisce che venga *riscritta*
altrove. Le otto strutture doppie che il progetto ha chiuso nei dati sono
state chiuse da schemi e validatori; la nona vive nel **codice**, dove non
arrivava ne' l'uno ne' l'altro. Il controllo anti-duplicazione di
`dati/_sistema.py`, eseguito da `dati/valida_sistema.py`, e' il primo
controllo del progetto che guarda il codice invece dei dati.

### Cosa il controllo VEDE

Legge **58 sorgenti Python** (la sede stessa esclusa: li' le tabelle devono
esserci) e li guarda in due modi.

- **Per forma.** L'espressione, riconosciuta sul codice **tokenizzato**:
  stringhe, commenti e f-string vengono scartati prima di guardare. Non e' un
  dettaglio di implementazione — questo stesso documento *descrive* la formula
  della CD, ed e' il suo mestiere. Un controllo che segnalasse la prosa
  griderebbe al lupo, e un controllo che grida al lupo viene spento.
- **Per valori.** La tabella espansa a mano: una corsa di almeno 10 interi
  consecutivi con almeno 3 valori distinti, separati **solo da
  punteggiatura**. Il vincolo dei separatori e' la regola decisiva:
  `dati/_sfere_5e.py` ha una colonna di livelli d'incantesimo che per caso
  comincia come il bonus di competenza, e prima di quella regola veniva
  segnalata.
- **Le eccezioni, e la loro morte.** 1 occorrenza e' permessa — la sonda di
  `valida_sistema.py`, che ricalcola la tabella con la formula stampata dalla
  fonte per confrontarla riga per riga. E' un riconfronto, non una copia.
  Un'eccezione dichiarata che non trova piu' il suo marcatore viene segnalata
  **come una copia**: un permesso che non protegge piu' niente e' peggio di
  nessun permesso.
- **Se stesso.** A ogni giro gli si piantano davanti 5 copie costruite apposta
  e 2 sorgenti che gli somigliano senza esserlo, e si pretende che veda le
  prime e non i secondi. Oggi ne riconosce **5 su 5**. Serve perche' su un
  repository pulito un rilevatore rotto e uno funzionante tacciono allo stesso
  modo, e la differenza si scopre il giorno in cui serviva.

Sul codice di oggi trova **0 copie** e **0 eccezioni marcite**. Non e' un
risultato scontato: quando e' stato acceso ne trovava cinque — il modificatore
di caratteristica in `dati/valida_effetti.py` e in `motore/combattimento.py`,
il bonus di competenza in `dati/_srd51.py` e in `dati/valida_effetti.py`, la
CD del tiro salvezza ancora in `valida_effetti.py`. Sono le occorrenze che
leggono la sede adesso.

### Cosa il controllo NON vede

- una riscrittura algebrica: `punteggio // 2 - 5` e' coperto perche' e'
  elencato, ma `(p + (-10)) >> 1` o un `round()` con un mezzo punto no.
  L'equivalenza fra due espressioni non si decide con un'espressione regolare,
  e fingere il contrario darebbe un controllo che rassicura.
- un'altra lingua: il giorno in cui il motore avra' un lato web, la stessa
  formula in JavaScript passera' inosservata. I sorgenti scanditi sono quelli
  di SORGENTI, cioe' Python.
- la prosa: una formula scritta a parole dentro un `description` di schema,
  dentro una nota di un JSON o dentro un documento non e' un letterale e non
  viene letta.
- un derivato precalcolato nei DATI: un mostro che si porti gia' sommato il
  proprio bonus di attacco non ripete nessuna formula, e questo controllo non
  se ne accorge — e' esattamente la lacuna che `attacco_di()` misura
  dall'altro lato.
- una tabella copiata parzialmente: sotto i 10 valori consecutivi la corsa non
  scatta. E' una soglia scelta, e le soglie scelte sbagliano da un lato: qui
  sbagliano lasciando passare, che e' il lato giusto per un controllo che deve
  restare acceso.

Questo elenco vive in `dati/_sistema.py` e non solo qui, perche' chi aggiunge
una formula legge quel file e non questo rapporto. Va letto insieme al
risultato: **un controllo di cui non si conosce il bordo viene creduto piu' di
quanto valga**, e un controllo creduto troppo e' esattamente il modo in cui
una struttura doppia torna a formarsi sotto la protezione di qualcosa che non
la guarda.

Il quarto limite merita una riga in piu' perche' non e' teorico: un mostro che
si portasse **gia' sommato** il proprio bonus d'attacco non ripete nessuna
formula, e questo controllo non se ne accorgerebbe. E' la stessa lacuna che
`attacco_di()` misura dall'altro lato, ed e' il §3.

---

## 3. `attacco_di()`: una lettura sola, e cosa ha spostato nel registro

Il fatto da cui si partiva: sul mostro `attacco` era **letto**, sul
personaggio era **composto** da razza + classe + oggetto + stile. Le due
strade ovvie rompevano ciascuna qualcosa di gia' deciso — far memorizzare
`attacco` al personaggio significa scrivere a mano un derivato, che decisione
7 (`doppio-strato`) e CLAUDE.md 3 vietano; far derivare `attacco` al mostro
significa inventare derivazioni che la fonte non da', e la prova ha gia' un
id: decisione 50 (`cd-origine-dichiarata`).

La risposta e' decisione 52 (`attacco-unica-lettura`): **cio' che e' condiviso
non e' il campo, e' la LETTURA.** La forma della risposta e' `effetto.attacco`
di `effetto.schema.json` e non cambia; il **mostro** la porta come dato; il
**personaggio** porta solo gli **ingressi** non derivabili — razza, classe,
livello, punteggi, equipaggiato, scelte — e ogni campo ricavabile da quelli
**non esiste** nella sua forma, che e' la versione piu' forte del divieto: la
stessa che decisione 39 (`bersaglio-legale-filtro`) ha usato rendendo
impossibile e non solo sconsigliato fissare un ospite. Il **motore** ha una
funzione `attacco_di(combattente, azione)` che torna quella forma: sul mostro
la legge, sul personaggio la compone, e chi la chiama non sa quale dei due
casi ha davanti.

Il registro delle lacune e' passato da **17 a 16**: due chiuse, una aperta.

- **Chiusa `attacco-del-pg`** — il personaggio non calcola piu' l'attacco in
  una funzione del motore: lo compone dagli ingressi, con la stessa lettura
  del mostro.
- **Chiusa `regole-di-sistema`** — le soglie del 20 e dell'1 naturale, i
  moltiplicatori delle difese, il modificatore e la competenza vengono da
  `dati/sistema/`. La sede che decisione 41 (`sconfessione-condivisa`) aveva
  promesso e mai costruito ha smesso di essere una lista d'attesa.
- **Aperta `attacco-origine-non-dichiarata`** — ed e' informazione, non un
  passo indietro. Guardando i due lati insieme si vede una cosa che prima
  nessuno guardava: un `bonus_colpire` **letto dalla scheda** e uno che
  **tornerebbe col conto** oggi si scrivono uguali. E' lo stesso difetto che
  decisione 50 (`cd-origine-dichiarata`) ha chiuso per la CD, sull'altro
  campo.

L'arena misura quanto pesa: dei 94 bonus d'attacco che il bestiario scrive in
prosa, 85 tornano col conto e 9 no. Il numero che conta non e' 85: e' che **85
coincidenze non sono 85 conferme**. La CD 11 del Baaz e' stampata dalla fonte
*e* torna col conto, quindi un controllo che confronta letto e derivato non
l'avrebbe mai segnalata — non perche' fosse corretta, ma perche' letto e
derivato sono indistinguibili quando coincidono. Contare le coincidenze invece
di fidarsene e' la differenza fra verificare e credere, ed e' la ragione per
cui la lacuna nuova chiede un `bonus_origine` e non un controllo piu' furbo.

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
volume**: si disegna quando ci sono abbastanza casi, si converte in volume
dopo che la forma e' ferma.

E' la ragione per cui la forma e' stata decisa adesso, con 16 lacune misurate
e due mostri strutturati, invece che dopo: oggi il costo di sbagliare forma e'
5 blocchi; fra trenta schede sarebbe 153, e la differenza non e' recuperabile
con nessuno script.

---

## 5. Cosa questo documento NON tocca

Le tre zone morte di schema — classi, razze, divinita' — restano aperte. La
decisione 51 (`criterio-meccanica`) e' la condizione che mancava per
chiuderle: uno schema disegnato attorno a una forma che sta per cambiare si
chiude due volte. La misura di quelle tre sta in
`dati/RAPPORTO-zona-morta-classi.md`.

Il volume del bestiario resta fermo: i blocchi ancora senza `effetto` si
convertono dopo il registro delle lacune, non prima.

---

*Le tre decisioni sono prese e hanno un id: decisione 51 (`criterio-meccanica`),
decisione 52 (`attacco-unica-lettura`), decisione 53 (`condizioni-vocabolario-srd`). Cio'
che resta di questo documento e' la misura del loro effetto — e il bordo del
controllo che le tiene ferme, che e' la parte da rileggere quando qualcuno
scrivera' la prossima formula.*
