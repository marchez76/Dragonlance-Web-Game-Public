# L'arena della fetta verticale — i dati usati per la prima volta

*Generato da `motore/arena.py` il 2026-09-02.*

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

> **Lo scontro gira. Con 17 lacune dichiarate.**

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

## 3. Le 17 lacune

Ognuna è un punto in cui il motore ha supplito ai dati. Sono l'esito vero di
questa prova.

**1. `pf-primo-livello`** — punti ferita del personaggio

> massimo al 1° livello e media ai successivi: e' la regola 5e, ma nessun campo dei dati la dichiara — il dado vita c'e', la procedura che lo usa no

**2. `condizione-modificatore`** — stile «Duello»: la condizione di applicazione è prosa

> «arma da mischia in una mano sola, nessun'altra arma impugnata» — il motore la considera sempre vera perché non c'è nessun campo che dica come verificarla

**3. `nessuna-posizione`** — portata e gittata sono campi popolati e mai letti

> il motore non ha una griglia ne' distanze: ogni combattente e' a portata di ogni altro. `portata_ft` e `gittata_ft` esistono nei dati e questo scontro non li usa — un'arma a distanza e una da mischia si comportano uguale

**4. `attacco-del-pg`** — l'attacco del personaggio non esiste come dato

> composto qui da arma + caratteristica + competenza + stile. Sul mostro `attacco` e' un campo; sul personaggio e' una funzione di questo modulo, e vive solo qui

**5. `difese-del-pg`** — resistenze e immunita' del personaggio

> il mostro le porta in `damage_resistances`, `damage_immunities`, `damage_vulnerabilities`; il personaggio non ha nessun campo dove averle, e nessuna regola che le componga da razza e classe. Qui e' senza difese, che oggi e' vero per un Cavaliere della Corona umano ma lo e' per assenza di dato, non per verifica

**6. `blocco-senza-effetto:traag:Dissoluzione post mortem`** — Traag: il blocco «Dissoluzione post mortem» non ha `effetto`

> il motore lo ignora. L'assenza di `effetto` non distingue «non ha meccanica» da «non e' ancora strutturato»: sono due cose diverse e nei dati si scrivono uguali

**7. `blocco-senza-effetto:traag:Furia cieca`** — Traag: il blocco «Furia cieca» non ha `effetto`

> il motore lo ignora. L'assenza di `effetto` non distingue «non ha meccanica» da «non e' ancora strutturato»: sono due cose diverse e nei dati si scrivono uguali

**8. `iniziativa`** — il bonus di iniziativa

> calcolato qui come modificatore di Destrezza. Nessun campo lo porta, ne' sul mostro ne' sulla classe

**9. `fine-dello-scontro`** — quando finisce uno scontro

> qui: quando una delle due parti non ha piu' nessuno che possa agire. Non e' un dato — ed e' la definizione che il Baaz mette alla prova, perche' una creatura pietrificata non e' morta, ha ancora i suoi punti ferita

**10. `morale-non-letto`** — il morale dei mostri non entra nello scontro

> la decisione 27 (`sette-campi-2e`) lo destina all'IA di combattimento e ogni mostro lo porta in `morale_2e`; qui nessuno lo legge, e i mostri combattono fino alla morte. Il Traag e' il caso peggiore: il suo morale ha due stati (8 prima dello scontro, nessun controllo dopo), e ignorarlo cancella il suo tratto identitario

**11. `regole-di-sistema`** — la procedura di risoluzione di un attacco

> d20 + bonus contro la Classe Armatura, 20 naturale critico che raddoppia i dadi, 1 naturale mancato d'ufficio: e' scritta in questo file e in nessun dato. La decisione 41 (`sconfessione-condivisa`) ha gia' registrato che manca una sede per le regole di sistema, e dati/condizioni/ e' il primo caso: questo e' il secondo, e pesa piu' del primo

**12. `quando-usare-una-risorsa`** — «Recuperare il fiato»: i dati dicono cosa fa e quanti usi ha

> non dicono QUANDO usarlo. La politica («sotto meta' dei punti ferita») e' del motore, non dei dati: e' materia dell'IA di combattimento, la stessa casella in cui la decisione 27 (`sette-campi-2e`) ha messo il morale

**13. `tiri-salvezza-contro-morte`** — il personaggio a 0 punti ferita

> resta incosciente e fuori dallo scontro. I tiri salvezza contro morte non sono modellati: la nota di dati/condizioni/incosciente.json lo dichiara gia' — sono una procedura del Personaggio, e il Personaggio non c'e'

**14. `blocco-senza-effetto:draconico-baaz:Controlled Fall`** — Draconico Baaz: il blocco «Controlled Fall» non ha `effetto`

> il motore lo ignora. L'assenza di `effetto` non distingue «non ha meccanica» da «non e' ancora strutturato»: sono due cose diverse e nei dati si scrivono uguali

**15. `blocco-senza-effetto:draconico-baaz:Draconic Devotion`** — Draconico Baaz: il blocco «Draconic Devotion» non ha `effetto`

> il motore lo ignora. L'assenza di `effetto` non distingue «non ha meccanica» da «non e' ancora strutturato»: sono due cose diverse e nei dati si scrivono uguali

**16. `innesco-non-dichiarato`** — «Death Throes» si innesca alla morte del portatore

> nessun campo lo dice: `azione: nessuna` significa «non costa un'azione», non «scatta a 0 punti ferita». Il motore riconosce il tratto DAL NOME, che e' l'unico appiglio che i dati offrono

**17. `bersagli-dell-area`** — «Death Throes» colpisce «ogni creatura entro 5 piedi»

> il motore lo applica a tutti gli AVVERSARI: non c'e' posizione, non c'e' distanza, e l'area non ha un campo (la prosa dice 5 piedi, `effetto` non ha dove metterlo). Ne segue un errore di regola dichiarato: la fonte dice «ogni creatura», quindi anche gli alleati del Baaz, e qui non li colpisce

---

## 4. Cosa si è rotto, in ordine di peso

**Il personaggio non è un dato.** Sul mostro l'attacco è un campo; sul
personaggio è una funzione di `motore/combattimento.py`, e vive solo lì. Classe
Armatura, punti ferita, bonus di attacco, danno: tutti composti a runtime da
razza + classe + oggetto + stile di combattimento, con la procedura scritta nel
motore. È la lacuna più grande e non sorprende — lo schema Personaggio non
esiste. Sorprende *quanto* di ciò che serve non sia da nessuna parte: la regola
dei punti ferita al 1° livello, il bonus di iniziativa, la competenza applicata
all'arma.

**Non c'è una sede per le regole di sistema.** La decisione 41
(`sconfessione-condivisa`) l'aveva già registrato, e `dati/condizioni/` è stata
la prima risposta. Questo è il secondo caso e pesa di più: *d20 + bonus contro
la Classe Armatura, 20 naturale critico, 1 naturale mancato d'ufficio* sta
scritto in un file Python e in nessun dato. Lo stesso vale per la struttura del
round, l'economia delle azioni e la condizione di fine scontro.

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

---

*Le quattro estensioni sono ora registrate come decisioni —
decisione 45 (`effetto-sul-blocco-mostro`), decisione 46 (`multiattacco-riferisce`),
decisione 47 (`salvezza-a-due-tempi`), decisione 48 (`condizioni-a-consumo`) — insieme alle
due che questa esecuzione ha imposto: decisione 49 (`vocabolario-italiano`) e
decisione 50 (`cd-origine-dichiarata`). Erano la condizione perché lo scontro
esistesse; restano scelte di progetto, e senza un id fra sei mesi nessuno
saprebbe perché `effetto` sta su `elemento_5e` invece che altrove.*
