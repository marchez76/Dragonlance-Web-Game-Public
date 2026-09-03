# L'arena della fetta verticale — i dati usati per la prima volta

*Generato da `motore/arena.py` il 2026-09-03.*

---

## 0. Cosa è stato provato

Tre anni di conversione hanno prodotto dati validati da ogni lato: schemi,
validatori incrociati, verifica degli strati, confronto fra prosa e struttura.
Nessuno di quei controlli chiede la sola cosa che conta — che con questi dati
si possa giocare un turno.

`motore/combattimento.py` lo chiede. Legge `mechanics_5e...effetto` dei mostri,
`dati/condizioni/`, `dati/oggetti/` e i privilegi del chassis, e gioca uno
scontro a turni con iniziativa, azioni, danno, morte e condizioni.

**Non misura chi vince. Misura le lacune.** Ogni volta che il motore ha
bisogno di qualcosa che i dati non portano, lo dichiara e va avanti con
un'assunzione scritta. Senza quel registro un simulatore mente: gira sempre,
perché ogni valore assente diventa uno zero e ogni regola assente diventa un
ramo che non si prende. È la stessa forma del difetto che la categoria d'arma
ha reso visibile — un buco che sembra un dato.

> **Lo scontro gira. Con 15 lacune dichiarate.**

---

## 1. Cosa è stato strutturato

`mostro.schema.json` aveva `additionalProperties: false` su `elemento_5e` e
nessun campo `effetto`: **lo strato strutturato non era nemmeno esprimibile
sui mostri.** Aperto, con la stessa forma e la stessa nota del campo omonimo
in `classe.schema.json`.

| creatura | gruppo | blocco | `effetto` |
|---|---|---|---|
| Traag | traits | Dissoluzione post mortem | — |
| Traag | traits | Furia cieca | — |
| Traag | actions | Attacchi Multipli | **multiattacco** |
| Traag | actions | Lancia | **attacco** |
| Draconico Baaz | traits | Controlled Fall | — |
| Draconico Baaz | traits | Death Throes | **tiro_salvezza** |
| Draconico Baaz | traits | Draconic Devotion | — |
| Draconico Baaz | actions | Multiattack | **multiattacco** |
| Draconico Baaz | actions | Shortsword | **attacco** |

**5 blocchi su 9** hanno una meccanica leggibile da un
motore. Gli altri 4 restano prosa — ed è già un risultato, perché
prima della fetta erano prosa tutti e 9, su 257 del bestiario.

### Due estensioni di schema, entrambe imposte da un caso — ora decisione 46 (`multiattacco-riferisce`) e decisione 47 (`salvezza-a-due-tempi`)

`multiattacco` — il blocco *Attacchi Multipli* dice una cosa meccanica e non
aveva nessun campo in cui dirla: la sua sola forma era la frase «effettua due
attacchi con X». Nel bestiario sono **18 blocchi su 128 azioni**,
e un motore che li ignorasse dimezzerebbe il danno per round di ognuno di quei
mostri senza che nessun controllo se ne accorga. Il campo riferisce l'azione
ripetuta per nome e non ne ricopia i numeri; `valida_effetti.py` verifica che
il nome esista nello stesso statblock.

`tiro_salvezza.fallimento_ripetuto` — il Death Throes del Baaz è un effetto a
**due tempi**: il primo fallimento trattiene mentre la pietrificazione
comincia, il secondo la compie. Lo schema aveva `ripetibile`, che dice *quando*
si ritira e non *cosa succede*. Senza il campo nuovo, le due condizioni di quel
tratto diventano una sola — cioè il tratto perde metà di sé senza che nessun
controllo se ne accorga.

### Due condizioni nuove, per lo stesso motivo — decisione 48 (`condizioni-a-consumo`)

`trattenuto` e `pietrificato` non esistevano. `build_condizioni.py` dichiarava
il criterio — *si aggiungono quando un blocco convertito le riferisce davvero* —
e questa è la prima volta che il criterio si applica invece di essere
enunciato. Sono cinque, non quindici.

`pietrificato` porta con sé una domanda che il motore ha dovuto risolvere: una
creatura pietrificata **non è morta**, ha ancora i suoi punti ferita e resiste
a tutti i danni. La condizione di fine scontro non può quindi essere «ogni
avversario a 0 punti ferita», ed è una definizione che nessun dato dichiara.

---

## 2. Gli scenari

| scenario | esiti su 1000 scontri | round medi | PG pietrificato |
|---|---|--:|--:|
| Cavaliere della Corona contro Traag | eroi 82%, mostri 17% | 2,5 | 0,0% |
| Cavaliere della Corona contro Baaz | eroi 75%, nessuno 13%, mostri 10% | 4,9 | 13,4% |
| Cavaliere della Corona contro Traag e Baaz | mostri 62%, eroi 32%, nessuno 5% | 4,5 | 5,7% |

«nessuno» è l'esito in cui il personaggio uccide il Baaz e il Death Throes lo
pietrifica: entrambe le parti fuori dallo scontro, nessuna morta. È il caso che
un motore scritto sull'assunzione «vince chi resta in piedi» non saprebbe
classificare.

---

## 3. Le 15 lacune

Ognuna è un punto in cui il motore ha supplito ai dati. Sono l'esito vero di
questa prova.

**1. `difese-del-pg`** — resistenze e immunita' del personaggio

> il mostro le porta in `damage_resistances`, `damage_immunities`, `damage_vulnerabilities`; il personaggio non ha nessun campo dove averle, e nessuna regola che le componga da razza e classe. Qui e' senza difese, che oggi e' vero per un Cavaliere della Corona umano ma lo e' per assenza di dato, non per verifica

**2. `condizione-modificatore`** — stile «Duello»: la condizione di applicazione è prosa

> «arma da mischia in una mano sola, nessun'altra arma impugnata» — il motore la considera sempre vera perché non c'è nessun campo che dica come verificarla

**3. `pf-primo-livello`** — punti ferita del personaggio

> massimo al 1° livello e media ai successivi: e' la regola 5e, ma nessun campo dei dati la dichiara — il dado vita c'e', la procedura che lo usa no

**4. `blocco-senza-effetto:traag:Dissoluzione post mortem`** — Traag: il blocco «Dissoluzione post mortem» non ha `effetto`

> il motore lo ignora. L'assenza di `effetto` non distingue «non ha meccanica» da «non e' ancora strutturato»: sono due cose diverse e nei dati si scrivono uguali

**5. `blocco-senza-effetto:traag:Furia cieca`** — Traag: il blocco «Furia cieca» non ha `effetto`

> il motore lo ignora. L'assenza di `effetto` non distingue «non ha meccanica» da «non e' ancora strutturato»: sono due cose diverse e nei dati si scrivono uguali

**6. `iniziativa`** — il bonus di iniziativa

> calcolato qui come modificatore di Destrezza. Nessun campo lo porta, ne' sul mostro ne' sulla classe

**7. `fine-dello-scontro`** — quando finisce uno scontro

> qui: quando una delle due parti non ha piu' nessuno che possa agire. Non e' un dato — ed e' la definizione che il Baaz mette alla prova, perche' una creatura pietrificata non e' morta, ha ancora i suoi punti ferita

**8. `morale-non-letto`** — il morale dei mostri non entra nello scontro

> la decisione 27 (`sette-campi-2e`) lo destina all'IA di combattimento e ogni mostro lo porta in `morale_2e`; qui nessuno lo legge, e i mostri combattono fino alla morte. Il Traag e' il caso peggiore: il suo morale ha due stati (8 prima dello scontro, nessun controllo dopo), e ignorarlo cancella il suo tratto identitario

**9. `nessuna-posizione`** — portata e gittata sono campi popolati e mai letti

> il motore non ha una griglia ne' distanze: ogni combattente e' a portata di ogni altro. `portata_ft` e `gittata_ft` esistono nei dati e questo scontro non li usa — un'arma a distanza e una da mischia si comportano uguale

**10. `quando-usare-una-risorsa`** — «Recuperare il fiato»: i dati dicono cosa fa e quanti usi ha

> non dicono QUANDO usarlo. La politica («sotto meta' dei punti ferita») e' del motore, non dei dati: e' materia dell'IA di combattimento, la stessa casella in cui la decisione 27 (`sette-campi-2e`) ha messo il morale

**11. `tiri-salvezza-contro-morte`** — il personaggio a 0 punti ferita

> resta incosciente e fuori dallo scontro. I tiri salvezza contro morte non sono modellati: la nota di dati/condizioni/incosciente.json lo dichiara gia' — sono una procedura del Personaggio, e il Personaggio non c'e'

**12. `blocco-senza-effetto:draconico-baaz:Controlled Fall`** — Draconico Baaz: il blocco «Controlled Fall» non ha `effetto`

> il motore lo ignora. L'assenza di `effetto` non distingue «non ha meccanica» da «non e' ancora strutturato»: sono due cose diverse e nei dati si scrivono uguali

**13. `blocco-senza-effetto:draconico-baaz:Draconic Devotion`** — Draconico Baaz: il blocco «Draconic Devotion» non ha `effetto`

> il motore lo ignora. L'assenza di `effetto` non distingue «non ha meccanica» da «non e' ancora strutturato»: sono due cose diverse e nei dati si scrivono uguali

**14. `innesco-non-dichiarato`** — «Death Throes» si innesca alla morte del portatore

> nessun campo lo dice: `azione: nessuna` significa «non costa un'azione», non «scatta a 0 punti ferita». Il motore riconosce il tratto DAL NOME, che e' l'unico appiglio che i dati offrono

**15. `bersagli-dell-area`** — «Death Throes» colpisce «ogni creatura entro 5 piedi»

> il motore lo applica a tutti gli AVVERSARI: non c'e' posizione, non c'e' distanza, e l'area non ha un campo (la prosa dice 5 piedi, `effetto` non ha dove metterlo). Ne segue un errore di regola dichiarato: la fonte dice «ogni creatura», quindi anche gli alleati del Baaz, e qui non li colpisce

---

## 4. Cosa si è rotto, in ordine di peso

**`attacco` era due cose con lo stesso nome — chiusa.** Sul mostro era un
campo letto dalla scheda, sul personaggio una funzione di
`motore/combattimento.py`: due cose diverse che si chiamavano uguale, ed è la
lacuna che il primo scontro ha reso visibile. Chiusa con
decisione 52 (`attacco-unica-lettura`): ciò che i due lati condividono non è il
campo, è la **lettura**. `attacco_di(combattente)` torna la forma
`effetto.attacco` da entrambe le parti — sul mostro la legge, sul personaggio
la compone — e chi la chiama non sa quale dei due casi ha davanti. Il
personaggio porta solo gli **ingressi** (razza, classe, livello, punteggi,
equipaggiato, scelte): ogni campo ricavabile da quelli non *può* esistere, il
costruttore solleva. Classe Armatura, punti ferita, bonus di attacco e danno
restano composti dal motore, ma adesso sono composti **una volta sola e per
tutti e due**.

**Il numero che nessuno può verificare — chiusa, e generalizzata.** Un
`bonus_colpire` letto dalla scheda e uno rifatto col conto (competenza +
modificatore) si scrivono identici, e `attacco_di()` non aveva modo di sapere
quale dei due stesse leggendo. È misurato, non supposto: dei **94 bonus di
attacco** che il bestiario scrive in prosa, **85 tornano col conto**
e 9 no. Le coincidenze non sono conferme — il
bonus della Spada corta del Baaz è **stampato dalla fonte** *e* torna col
conto, esattamente come la sua CD 11, e nessun controllo poteva vederlo.

Al secondo caso in due giri la regola è stata scritta una volta per tutte
invece di essere riapplicata a mano: decisione 54 (`origine-e-un-dato`). Quando un
valore può essere **sia letto dalla fonte sia calcolato dal sistema**, la sua
origine è un **campo**, non una deduzione. `cd_origine` e `bonus_origine` ne
sono le due applicazioni, non due decisioni imparentate. Il campo è nello
schema, il controllo 6 di `dati/valida_effetti.py` lo pretende ovunque
`bonus_colpire` non sia nullo, e la lacuna del motore non è sparita: è
diventata **condizionata al dato**, e scatta esattamente sugli attacchi che
non la dichiarano. Oggi sono zero perché i due strutturati la portano
(2 su 2), e tornerà da sola quando si strutturerà il terzo
senza compilarla.

**Quanti altri campi hanno questa forma — la misura, non la stima.** La
domanda che conta non è se `bonus_colpire` sia a posto adesso, ma quanti altri
valori si scrivono uguali che siano letti o calcolati. Sono **4
ancora scoperti**, e il quinto è il caso che insegna di più:

| campo | dove | casi | tornano col conto | dichiara l'origine |
|---|---|--:|--:|---|
| `bonus_colpire` | prosa dei blocchi | 94 | 85 (90%) | no |
| bonus di danno | prosa dei blocchi | 110 | 96 (87%) | no |
| `skills[].bonus` | scheda | 18 | 16 (88%) | no |
| `passive_perception` | scheda | 52 | 52 (100%) | no |
| `hit_points.average` | scheda | 51 | 48 (94%) | si', con altro nome |

`passive_perception` è il caso che spiega perché la percentuale non è una
diagnosi: **52 su 52** tornano col conto, il cento per cento, e
proprio per questo di nessuna si sa se sia stata letta o calcolata. Un campo dove il conto torna sempre è il posto **peggiore** in cui
fidarsi del conto, non il migliore.

`hit_points.average` è l'altro estremo, e va detto perché è la scoperta più
utile del giro: l'origine lì **è già dichiarata**, sotto un altro nome —
`conversion_status` e `source`, che `armor_class` e `challenge_rating` portano
allo stesso modo. Il progetto aveva già inventato questo campo **tre volte**
senza accorgersi che era lo stesso campo, e la decisione 54 (`origine-e-un-dato`)
lo scrive come una regola sola. Unificare i tre nomi è un rinominare che tocca 52
schede e uno schema già committato: **non fatto ora, e dichiarato aperto**.

`saving_throws` non è nell'elenco e non è una dimenticanza: porta solo
`proficient`, cioè **quali competenze** il portatore ha e non il numero che ne
segue. Un campo che porta ingressi non può avere questo difetto — ed è la
stessa forma che la decisione 52 (`attacco-unica-lettura`) ha imposto al
personaggio.

**Non c'è una sede per le regole di sistema — chiusa.** *d20 + bonus contro la
Classe Armatura, 20 naturale critico, 1 naturale mancato d'ufficio* stava in
un file Python e in nessun dato. Il criterio a tre domande
(decisione 51 (`criterio-meccanica`)) l'ha tagliata in due: i **numeri** — il 20 e
l'1 naturale, i moltiplicatori di resistenza e vulnerabilità, il modificatore
di caratteristica, il bonus di competenza, la base della CD — sono ora dati di
sistema in `dati/sistema/`, con schema e validatore; la **procedura** che li
usa resta codice, che è la risposta e non più una mancanza. La condizione
perché quella risposta valga era un riconfronto automatico, e c'è:
`dati/valida_sistema.py` rifiuta la stessa tabella riscritta altrove, e a
metterlo in piedi ha trovato subito i cinque punti in cui era già successo.

**Un innesco non ha un campo.** `azione: nessuna` significa *non costa
un'azione*, non *scatta a 0 punti ferita*. Il motore riconosce il Death Throes
**dal nome**, che è l'unico appiglio che i dati offrono. Ogni tratto che
scatta a una condizione — alla morte, quando si viene colpiti, all'inizio del
turno — oggi è indistinguibile da un tratto passivo.

**Non c'è posizione.** `portata_ft` e `gittata_ft` sono campi popolati e mai
letti: senza distanze un'arma da mischia e una a distanza si comportano
uguale. La conseguenza si vede sul Death Throes, che la fonte dichiara «ogni
creatura entro 5 piedi» e che il motore applica a tutti gli avversari e a
nessun alleato — un errore di regola, dichiarato.

**L'assenza di `effetto` dice due cose diverse.** *Non ha meccanica* e *non è
ancora strutturato* si scrivono uguali. `esito.nessuno` esiste proprio per
questa distinzione, un livello più in basso; al livello del blocco non c'è.
La *Dissoluzione post mortem* del Traag è il caso: la fonte dichiara
esplicitamente che non succede niente, e nei dati è indistinguibile da un
blocco non convertito.

**Il morale non entra in campo.** La decisione 27 (`sette-campi-2e`) lo destina
all'IA di combattimento e ogni mostro lo porta in `morale_2e`. Nessuno lo
legge, e i mostri combattono fino alla morte — «irrealistico, e macchinoso da
giocare», dice quella stessa decisione. Il Traag è il caso peggiore: il suo
morale ha due stati, e ignorarlo cancella il suo tratto identitario.

**Due vocabolari per i tipi di danno — chiusa.** Alla prima esecuzione
`dati/oggetti/` li portava in inglese (`slashing`, dall'SRD) e `dati/mostri/`
in italiano (`perforante`), nessuno dei due schemi li vincolava e nessun
validatore poteva vederlo perché nessuno dei due era sbagliato dal proprio
lato. Era l'ottava struttura doppia del progetto, e non è stata trovata
ispezionando i dati: è stata trovata usandoli. Chiusa con
decisione 49 (`vocabolario-italiano`) — vocabolario unico in
`dati/schema/vocabolari.schema.json`, riferito per `$ref` e mai ricopiato — e
il motore adesso **confronta davvero** il tipo di danno con resistenze,
immunità e vulnerabilità (`applica_difese`).

**Nessuno dei tre scenari lo esercita**, e va detto invece che lasciato
credere: né il Traag né il Baaz hanno difese per tipo, e il personaggio non ha
un campo dove averne. Il ramo esiste e in questa arena non si prende, che è
un'altra cosa dall'aver funzionato. Provato quindi a parte, e non su casi
costruiti: le schede sono cercate nel bestiario, una per forma
(Bakali, Bambola Kani, Cervo Selvatico Wichtlin).

| scheda e difesa | 10 danni diventano | come è stato letto |
|---|---|---|
| Cervo Selvatico Wichtlin — resistenza a `contundente` (da_attacchi_non_magici) | arma non magica: **5** | 5 contundente, resistente |
| Cervo Selvatico Wichtlin — resistenza a `contundente` (da_attacchi_non_magici) | arma magica: **10** | 10 contundente |
| Bambola Kani — immunità a `da_veleno` | 10 danni: **0** | 10 da_veleno annullati (immune) |
| Bakali — vulnerabilità a `da_freddo` | 10 danni: **20** | 20 da_freddo, vulnerabile |

Le due righe che contano sono le prime: la stessa arma, se magica, passa la
resistenza. E lì c'è la lacuna nuova che ha preso il posto di quella chiusa —
**nessun campo dice se un attacco è magico**. Sull'arma di un personaggio c'è
`magico`; sull'azione di un mostro non c'è niente, e il motore assume *non
magico*, cioè l'assunzione favorevole al difensore.

**Le immunità a condizione: due sedi che non si parlavano — chiusa.**
`dati/mostri/` dichiarava le immunità con i nomi inglesi della 5e
(`charmed`, `poisoned`) mentre `dati/condizioni/` — che
decisione 48 (`condizioni-a-consumo`) dichiara sede unica — ha id italiani. Stesso
difetto dei tipi di danno, con l'aggravante che qui una delle due sedi era
**già dichiarata unica** e l'altra la ignorava: nessuna immunità del
bestiario poteva essere rispettata da nessun motore.

Tradurre e basta non bastava, ed è la ragione per cui questo caso era rimasto
aperto: delle condizioni citate dalle immunità solo tre esistono in
`dati/condizioni/`, e crearne altre sette per anticipazione avrebbe
sconfessato decisione 48 (`condizioni-a-consumo`) tre giorni dopo averla presa.
La strada è quella dei repertori (decisione 35 (`repertori-sono-filtri`)): l'insieme
delle condizioni SRD è **chiuso e noto**, quindi il vocabolario è completo —
**15 termini** — mentre il catalogo ne converte **5**. Le altre
10 non sono condizioni inesistenti: sono una **lacuna del nostro
catalogo**, che è cosa diversa, e non si scrive da nessuna parte — si deriva
dai file presenti nella cartella. decisione 53 (`condizioni-vocabolario-srd`).

Nel bestiario: **35 immunità su 11 schede**, di cui
**29 nominano una condizione che il motore non sa ancora applicare**.
Quel numero non è un errore da correggere, è una distanza da conoscere — e il
motore la **dichiara** (lacuna `condizione-non-modellata`) invece di
ignorarla, perché un'immunità saltata in silenzio è indistinguibile da
un'immunità rispettata.

Anche qui nessuno dei tre scenari esercita il ramo — né il Traag né il Baaz
dichiara immunità a condizione — quindi è provato a parte, su schede cercate
nel bestiario e non costruite:

| scheda e immunità | esito | come è stato letto |
|---|---|---|
| Sciame di Cavallette e Locuste — immune a `pietrificato` | la condizione e' **respinta** | Sciame di Cavallette e Locuste e' immune a «pietrificato»: non si applica. |
| Bambola Kani — immune a `sfinimento` | il motore **la dichiara** | `dati/condizioni/sfinimento.json` non esiste: il termine c'e', la scheda meccanica no |

---

*Le quattro estensioni sono ora registrate come decisioni —
decisione 45 (`effetto-sul-blocco-mostro`), decisione 46 (`multiattacco-riferisce`),
decisione 47 (`salvezza-a-due-tempi`), decisione 48 (`condizioni-a-consumo`) — insieme alle
due che questa esecuzione ha imposto: decisione 49 (`vocabolario-italiano`) e
decisione 50 (`cd-origine-dichiarata`). Erano la condizione perché lo scontro
esistesse; restano scelte di progetto, e senza un id fra sei mesi nessuno
saprebbe perché `effetto` sta su `elemento_5e` invece che altrove.*
