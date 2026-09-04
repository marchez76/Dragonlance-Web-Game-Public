# `allowed_classes` — la mappa fra 17 etichette 2e e 17 nostre classi

*Generato da `dati/analizza_allowed_classes.py`. **Questo documento non
decide**: porta la mappa perche' la decisione si prenda guardandola.*

---

## 0. Perche' non manca un campo

`allowed_classes` c'e', e' compilato su 12 razze su 15, e non gli manca
niente. Manca il **ponte**: le razze dichiarano le classi con le etichette del
PHB 2e, il roster e' nato da un'altra strada, e fra i due elenchi non esiste
una regola di traduzione scritta da nessuna parte. Finche' non c'e', la prima
domanda della creazione di un personaggio — *quali classi puo' prendere questa
razza* — non ha una risposta calcolabile.

Il caso che lo mostra meglio e' `Fighter`: e' l'etichetta piu' concessa (12
razze su 15) e nel roster **non esiste una classe con quel nome**. Il roster
ha Cavaliere, Barbaro, Marinaio — tutte cose che un guerriero fa — e nessun
guerriero generico. Quindi o `Fighter` non nomina una classe ma un **telaio**,
e allora la traduzione passa per i chassis, oppure 12 razze concedono una
classe che non esiste.

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

I telai disponibili sono 5 — `Cleric`, `Fighter`, `Paladin`, `Rogue`, `Wizard`
— e sono quelli, non tutti quelli della 5e: sono i cinque di cui abbiamo
trascritto i privilegi. Di questi il roster ne usa 5 (`Cleric`, `Fighter`,
`Paladin`, `Rogue`, `Wizard`). 8 nostre classi non hanno ancora un telaio, e 5
non si prendono alla creazione: si entra da un'altra classe, quindi non e'
dalle razze che devono essere raggiunte.

---

## 2. La mappa, etichetta per etichetta

Tre vie di copertura, in ordine di costo crescente. **Nome**: il nome inglese
di una nostra classe coincide con l'etichetta, e non c'e' niente da decidere.
**Parole**: condivide almeno una parola che distingue, e va confermata a
occhio una volta. **Telaio**: nessuna parola in comune, ma la nostra classe
sta sul telaio 5e che l'etichetta nomina — e vale **solo** se si decide che
l'etichetta nomina un telaio e non una classe. **Scoperta**: nessuna delle
tre.

| etichetta | razze | via | per nome / parole | parole in comune | in piu' se e' un telaio | telaio |
|---|--:|---|---|---|---|---|
| `Barbarian` | 5 | nome | `barbaro` | — | `cavaliere-corona`, `cavaliere` | `Fighter` |
| `Bard` | 5 | scoperta | — | — | — | **nessuno** |
| `Cavalier` | 3 | nome | `cavaliere` | — | `barbaro`, `cavaliere-corona` | `Fighter` |
| `Druid (heathen)` | 2 | parole | `sacerdote-eretico` | `heathen` | — | **nessuno** |
| `Fighter` | 12 | telaio | — | — | `barbaro`, `cavaliere-corona`, `cavaliere` | `Fighter` |
| `Handler` | 1 | nome | `handler` | — | `con-artist` | `Rogue` |
| `High Sorcerer` | 6 | parole | `mago-alta-stregoneria` | `high` | `mago-rinnegato` | `Wizard` |
| `Holy Orders` | 11 | parole | `sacerdote-ordini-sacri` | `holy`, `orders` | — | `Cleric` |
| `Illusionist` | 1 | telaio | — | — | `mago-alta-stregoneria`, `mago-rinnegato` | `Wizard` |
| `Knight of Solamnia` | 1 | telaio | — | — | `cavaliere-rosa`, `cavaliere-spada` | `Paladin` |
| `Mage (Renegade)` | 2 | parole | `mago-rinnegato` | `renegade` | `mago-alta-stregoneria` | `Wizard` |
| `Mariner` | 3 | nome | `mariner` | — | `barbaro`, `cavaliere-corona`, `cavaliere` | `Fighter` |
| `Paladin` | 2 | telaio | — | — | `cavaliere-rosa`, `cavaliere-spada` | `Paladin` |
| `Priest (heathen)` | 2 | parole | `sacerdote-eretico` | `heathen` | `sacerdote-ordini-sacri` | `Cleric` |
| `Ranger` | 6 | scoperta | — | — | — | **nessuno** |
| `Thief` | 9 | telaio | — | — | `con-artist` | `Rogue` |
| `Tinker` | 1 | nome | `tinker` | — | — | **nessuno** |

La colonna **in piu' se e' un telaio** non e' una via alternativa: e' cosa si
aggiungerebbe *oltre* alla copertura gia' trovata, se si decidesse che
l'etichetta nomina il telaio. Per `Barbarian` significa che l'accesso
passerebbe dal solo Barbaro a tre classi.

La colonna **parole in comune** e' li' perche' un accostamento per parole va
guardato, non contato. `Druid (heathen)` e `Heathen Priest` condividono
`heathen` e nient'altro: un druido e un sacerdote non sono la stessa cosa
nemmeno nella 2e, e questo e' l'accostamento piu' debole della tabella.

Conteggio per via: **nome** 5, **parole** 5, **telaio** 5, **scoperta** 2.

### Le ragioni del telaio, che sono editoriali e non derivate

| etichetta | telaio | perche' |
|---|---|---|
| `Barbarian` | `Fighter` | guerriero senza addestramento cavalleresco; l'Ira e' un'invenzione della 3e, assente da Krynn |
| `Bard` | **nessuno** | il Bardo SRD esiste nella 5e ma non fra i cinque telai che abbiamo trascritto |
| `Cavalier` | `Fighter` | guerriero a cavallo, telaio marziale puro |
| `Druid (heathen)` | **nessuno** | il Druido SRD esiste nella 5e ma non fra i cinque telai che abbiamo trascritto |
| `Fighter` | `Fighter` | e' il telaio, non una classe del nostro roster |
| `Handler` | `Rogue` | abilita' del ladro applicate al baratto kender |
| `High Sorcerer` | `Wizard` | incantatore arcano a preparazione |
| `Holy Orders` | `Cleric` | incantatore divino, e' il nome 2e dell'ordine sacerdotale di Krynn |
| `Illusionist` | `Wizard` | specialista arcano: nella 5e e' una sottoclasse del Mago, non una classe |
| `Knight of Solamnia` | `Paladin` | l'ombrello dei tre ordini cavallereschi; due dei tre stanno su telaio Paladin |
| `Mage (Renegade)` | `Wizard` | incantatore arcano fuori dagli Ordini |
| `Mariner` | `Fighter` | guerriero di mare |
| `Paladin` | `Paladin` | e' il telaio, non una classe del nostro roster |
| `Priest (heathen)` | `Cleric` | incantatore divino fuori dagli Ordini |
| `Ranger` | **nessuno** | il Ranger SRD esiste nella 5e ma non fra i cinque telai che abbiamo trascritto |
| `Thief` | `Rogue` | e' il telaio, non una classe del nostro roster |
| `Tinker` | **nessuno** | non ha un telaio 5e: e' un'invenzione di Krynn |

---

## 3. I tre casi che chiedono una decisione diversa

### 3a. Le etichette che il telaio salva — 5 su 17

Sono le etichette senza nessuna parola in comune col roster, ma con un telaio
che il roster usa. Se si decide che **un'etichetta 2e nomina un telaio**,
queste si risolvono tutte insieme e senza aggiungere classi:

| etichetta | razze | classi che il telaio le da' |
|---|--:|---|
| `Fighter` | 12 | `barbaro`, `cavaliere-corona`, `cavaliere` |
| `Illusionist` | 1 | `mago-alta-stregoneria`, `mago-rinnegato` |
| `Knight of Solamnia` | 1 | `cavaliere-rosa`, `cavaliere-spada` |
| `Paladin` | 2 | `cavaliere-rosa`, `cavaliere-spada` |
| `Thief` | 9 | `con-artist` |

Il prezzo di questa lettura va detto: `Fighter` concessa a una razza
diventerebbe l'accesso a **3 classi diverse** insieme, fra cui il Cavaliere
della Corona, che nella 2e ha restrizioni di razza sue. La traduzione per
telaio e' generosa, e dove la fonte era piu' stretta lo diventa in silenzio:
e' il punto in cui la decisione 7 (`doppio-strato`) chiede che lo scarto sia
dichiarato, non assorbito.

### 3b. Le etichette senza telaio — 4 su 17

| etichetta | razze | perche' nessun telaio |
|---|--:|---|
| `Bard` | 5 | il Bardo SRD esiste nella 5e ma non fra i cinque telai che abbiamo trascritto |
| `Druid (heathen)` | 2 | il Druido SRD esiste nella 5e ma non fra i cinque telai che abbiamo trascritto |
| `Ranger` | 6 | il Ranger SRD esiste nella 5e ma non fra i cinque telai che abbiamo trascritto |
| `Tinker` | 1 | non ha un telaio 5e: e' un'invenzione di Krynn |

Qui la domanda cambia forma. Per `Bard`, `Druid (heathen)`, `Ranger` il telaio
esiste nella 5e e **non l'abbiamo trascritto**: e' lavoro noto, non una
decisione di conversione. Per le altre non esiste affatto, e allora delle due
l'una — la razza perde quell'accesso, o manca una classe.

### 3c. Le etichette scoperte — 2 su 17

| etichetta | razze concedenti | telaio dichiarato |
|---|--:|---|
| `Bard` | 5 | **nessuno** |
| `Ranger` | 6 | **nessuno** |

---

## 4. Il verso opposto: le classi che nessuna razza puo' prendere

| nostra classe | telaio | si entra da | etichette che la raggiungono | per quale via |
|---|---|---|---|---|
| `barbaro` | `Fighter` | — | `Barbarian`, `Cavalier`, `Fighter`, `Mariner` | nome, telaio |
| `cavaliere-corona` | `Fighter` | — | `Barbarian`, `Cavalier`, `Fighter`, `Mariner` | telaio |
| `cavaliere-rosa` | `Paladin` | `cavaliere-spada` | `Knight of Solamnia`, `Paladin` | telaio |
| `cavaliere-spada` | `Paladin` | `cavaliere-corona` | `Knight of Solamnia`, `Paladin` | telaio |
| `cavaliere` | `Fighter` | — | `Barbarian`, `Cavalier`, `Fighter`, `Mariner` | nome, telaio |
| `commoner` | — | — | **NESSUNA** | — |
| `con-artist` | `Rogue` | — | `Handler`, `Thief` | telaio |
| `handler` | — | — | `Handler` | nome |
| `mago-alta-stregoneria` | `Wizard` | — | `High Sorcerer`, `Illusionist`, `Mage (Renegade)` | parole, telaio |
| `mago-rinnegato` | `Wizard` | — | `High Sorcerer`, `Illusionist`, `Mage (Renegade)` | parole, telaio |
| `mago-veste-bianca` | — | `mago-alta-stregoneria` | **NESSUNA** | — |
| `mago-veste-nera` | — | `mago-alta-stregoneria` | **NESSUNA** | — |
| `mago-veste-rossa` | — | `mago-alta-stregoneria` | **NESSUNA** | — |
| `mariner` | — | — | `Mariner` | nome |
| `sacerdote-eretico` | — | — | `Druid (heathen)`, `Priest (heathen)` | parole |
| `sacerdote-ordini-sacri` | `Cleric` | — | `Holy Orders`, `Priest (heathen)` | parole, telaio |
| `tinker` | — | — | `Tinker` | nome |

**4 classi su 17 non sono raggiunte da nessuna etichetta**, e non sono lo
stesso caso. Contarle insieme darebbe un numero falso:

| classe | si entra da | verdetto |
|---|---|---|
| `commoner` (Commoner) | — nessuna | **INGIOCABILE** |
| `mago-veste-bianca` (Wizard of the White Robes) | `mago-alta-stregoneria` | **avanzamento**, raggiungibile per la classe che lo richiede |
| `mago-veste-nera` (Wizard of the Black Robes) | `mago-alta-stregoneria` | **avanzamento**, raggiungibile per la classe che lo richiede |
| `mago-veste-rossa` (Wizard of the Red Robes) | `mago-alta-stregoneria` | **avanzamento**, raggiungibile per la classe che lo richiede |

- **3 sono avanzamenti**: non devono essere
  dichiarati dalle razze, ci si arriva dalla classe che li richiede — le tre
  Vesti si prendono dal Mago dell'Alta Stregoneria, che le razze raggiungono.
  Che `allowed_classes` non le nomini e' **giusto**, non un buco.
- **1** non e' raggiunta
  **da niente**: `commoner`.
- **0 avanzamenti orfani** — nessuno: ogni catena di ingresso comincia da una classe che almeno una razza concede.
  

Una classe raggiungibile da nessuna delle due vie e' **ingiocabile**, e non e'
un difetto astratto: e' una scheda scritta, validata e irraggiungibile. Vale
la pena saperlo **prima** di scrivere lo schema del Personaggio, perche' lo
schema non puo' dirlo — un campo `classe` valido non sa che nessuno potra'
sceglierlo. E la distinzione fra le due colonne e' esattamente il tipo di cosa
che uno schema non vede e un controllo si': la raggiungibilita' non e' una
proprieta' di un file, e' una proprieta' del **grafo** fra due famiglie.

---

## 5. Le 3 razze senza elenco, e una che non torna

| razza | applied | classes |
|---|---|---|
| `elfo-dargonesti` | False | null |
| `umano-barbaro` | False | null |
| `umano` | False | null |

Per gli umani il vuoto ha una ragione dichiarata e giusta: la decisione 3
(`vincoli-caratteristica`) preclude le classi assenti dalla tabella del
manuale, e il manuale gli umani non li elenca affatto — nessuna riga, quindi
nessuna preclusione. La nota nel dato dice esattamente questo.

**`elfo-dargonesti` porta lo stesso `applied: false` e la stessa nota, e la
nota non lo riguarda**: non e' una razza che il manuale non elenca, e la
ragione scritta accanto vale solo per gli umani. E' una nota copiata su un
caso che non e' quello, ed e' la forma piu' silenziosa della struttura doppia:
il campo e' compilato, il controllo passa, e la spiegazione e' di un altro. Va
sciolto guardando la fonte — o l'elfo Dargonesti ha un elenco che non e' stato
trascritto, o ha una ragione sua per non averlo, e in entrambi i casi la nota
va riscritta.

---

## 6. Cosa serve decidere, in ordine

1. **Un'etichetta 2e nomina una classe o un telaio?** E' la domanda che
   scioglie 5 etichette in un colpo e ne lascia
   4 aperte. Il sospetto che la risposta passi per i chassis
   e' confermato dai numeri: i chassis sono gia' il ponte fra le classi di
   Krynn e la 5e, e sono l'unica struttura che copre `Fighter`, `Paladin` e
   `Thief` senza inventare classi.
2. **Dove il telaio allarga, lo scarto si dichiara o si stringe?**
   Vedi §3a: `Fighter` per telaio da' accesso anche al Cavaliere della Corona.
3. **Le 4 etichette senza telaio**: la razza perde
   l'accesso, o manca una classe? Sono due risposte diverse per
   sottoinsiemi diversi (§3b).
4. **Le 1 classi davvero irraggiungibili**
   (`commoner`):
   si aggiunge un'etichetta che le raggiunga, o si accetta che siano PNG? Gli
   altri 3 silenzi sono avanzamenti e vanno
   bene cosi'.
5. **`elfo-dargonesti`**: la nota va riscritta comunque, qualunque sia la
   risposta alle altre quattro.
