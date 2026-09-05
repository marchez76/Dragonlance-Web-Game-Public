# Le zone morte di classe e di razza — quanto costa chiuderle

*Generato da `dati/analizza_zona_morta_classi.py` il 2026-09-05. Non modificare a
mano: ogni numero è interpolato dai dati.*

---

## 0. La misura in una riga

`classe.schema.json` descrive `mechanics_5e` come *object o null*, con
16 proprietà dichiarate su **167 percorsi in uso** nei
20 file. Nessun `additionalProperties`.

> **113 percorsi su 167** non sono dichiarati da nessuno
> schema. Di questi, **61 non sono nominati nemmeno da un
> validatore**: un campo scritto storto lì dentro non incontra nessun
> controllo, in nessun punto della catena.

I 39 percorsi sotto `effetto` non sono contati fra i nudi:
sono validati a parte contro `effetto.schema.json` da `valida_effetti.py`.
Sono l'unico pezzo dello strato che ha una verifica vera.

---

## 1. Dove stanno i 113 percorsi nudi

| blocco di primo livello | percorsi in uso | non dichiarati | classi che lo portano |
|---|--:|--:|--:|
| `structural` | 68 | 68 | 20/20 |
| `chassis_features` | 49 | 4 | 20/20 |
| `features` | 14 | 8 | 20/20 |
| `ability_minimums` | 10 | 10 | 20/20 |
| `chassis` | 9 | 9 | 20/20 |
| `level_limits` | 3 | 3 | 20/20 |
| `alignment_restriction` | 3 | 3 | 20/20 |
| `race_restriction` | 3 | 3 | 20/20 |
| `chassis_features_da_trascrivere` | 3 | 0 | 20/20 |
| `prerequisite_class` | 1 | 1 | 20/20 |
| `hit_die` | 1 | 1 | 20/20 |
| `entry_level` | 1 | 1 | 20/20 |
| `features_pending` | 1 | 1 | 20/20 |
| `conversion_status` | 1 | 1 | 20/20 |

Il conto del lavoro si legge da questa tabella: non sono
113 decisioni indipendenti, sono **13
blocchi** da descrivere, e due di essi (`structural`, `ability_minimums`)
pesano da soli
78 percorsi su 113.

### Quanto è già deciso

15 campi scalari hanno **fra due e sei valori distinti** in tutto il
corpus: nello schema diventano `enum`, e il valore ammesso non va inventato,
va letto dai dati. Esempi:

| percorso | valori distinti in uso |
|---|---|
| `mechanics_5e.alignment_restriction.value` | `Buono`, `Lawful Good`, `Malvagio`, `Neutrale` |
| `mechanics_5e.chassis.features_from` | `SRD 5.1 — Cleric`, `SRD 5.1 — Fighter`, `SRD 5.1 — Paladin`, `SRD 5.1 — Rogue`, `SRD 5.1 — Wizard` |
| `mechanics_5e.chassis.hit_die` | `1d10`, `1d6`, `1d8` |
| `mechanics_5e.chassis.srd_class` | `Cleric`, `Fighter`, `Paladin`, `Rogue`, `Wizard` |
| `mechanics_5e.chassis.status` | `clonato`, `in_sospeso` |
| `mechanics_5e.chassis_features[].effetto.azione` | `azione_bonus`, `nessuna` |
| `mechanics_5e.chassis_features[].effetto.modificatori[].bersaglio` | `azioni_per_turno`, `ca`, `danno` |
| `mechanics_5e.chassis_features[].kind` | `opzione_chassis`, `privilegio_chassis` |
| `mechanics_5e.conversion_status` | `clonato`, `in_sospeso` |
| `mechanics_5e.features[].conversion_status` | `direct`, `pending`, `source_only` |
| `mechanics_5e.features[].kind` | `impedimento`, `privilegio` |
| `mechanics_5e.features[].mechanics_5e.riferimento_a` | `chassis`, `privilegio_chassis` |

---

## 2. Le incoerenze fra classi

**9 in tutto**, in 2 famiglie, e
non sono una cosa sola. **9 sono stato dichiarato**: cose vere
dei dati che nessuno schema ammette ancora, e si chiudono scrivendo lo schema,
cioè dentro il lavoro di §5b. **0 sono difetti**: i dati dicono
una cosa falsa, e va corretto il dato.

La distinzione è nata da una lettura, non da un conteggio. Il 04/09/2026 le
famiglie erano quattro e il totale dodici, tutte nella stessa colonna. Divise:
sette di stato dichiarato, due difetti veri, e **tre segnalazioni false
prodotte da questo stesso rilevatore**, che chiedeva a `features_pending` un
conto che non è il suo. Un totale unico faceva sembrare il lavoro cinque volte
più grande di quello che era, e faceva pagare a un derivato corretto il prezzo
di un controllo sbagliato.

### 2.1 Uno stato di conversione che promette una meccanica che non c'è

`pending`, `source_only` sono gli stati in cui la meccanica 5e
può mancare — è scritto nella descrizione di `elemento_5e` in
`mostro.schema.json`, ed è l'invariante che distingue *«non è ancora stato
scritto»* da *«è stato scritto che non succede niente»*.

*nessuna*

**CHIUSA il 04/09/2026**, e la sezione resta perché l'invariante continui ad
avere un posto dove fallire. Le due violazioni erano privilegi della fonte con `direct`
e `mechanics_5e: null` insieme: dicevano nello stesso respiro *«conversione
conclusa»* e *«non c'è niente»*.

Non era un difetto dei due privilegi. La loro meccanica 5e **esiste** — è
quella del chassis Paladino, che li concede già — e non stava scritta lì
perché al campo mancava il modo di dire *sta altrove*. Un privilegio la cui
meccanica è il chassis non è un caso di provenienza: è un **rimando**.

Le strade erano due. Aggiungere uno stato di conversione nuovo avrebbe messo
un termine in più nel vocabolario condiviso con mostri, oggetti e modelli, per
un caso che riguarda le sole classi e conta due occorrenze — la quinta volta
che questo progetto reinventa lo stesso concetto sotto un nome nuovo. La
seconda riempie il campo che già c'è: `mechanics_5e` porta il rimando
(`riferimento_a`, `srd_class`, `name_srd`, `level`), `direct` torna vero, e il
vocabolario condiviso non si muove. È quella adottata.

Un rimando è un **dato e non una nota** perché è verificabile: il privilegio
del chassis o sta nella tabella SRD o non ci sta. `_chassis_5e` fallisce in
costruzione se il bersaglio non esiste, `verifica_rimandi()` rifà la prova sui
file già scritti, e `valida_classi.py` la esegue — perché un riferimento che
risolve il giorno in cui è scritto è esattamente la forma di copia che qui si
è già sfasata dodici volte.

### 2.2 Il numero che dice quanto manca, e il controllo che glielo chiedeva male

*nessuna*

**Le tre segnalazioni di questa famiglia erano false, e il difetto era del
rilevatore.** Corretto il 04/09/2026.

Il controllo confrontava `features_pending` con i blocchi **vuoti**, cioè con
i privilegi che hanno `mechanics_5e: null`. Ma vuoto e in sospeso non sono la
stessa cosa: `source_only` è vuoto per definizione — la fonte concede un
permesso che il nostro sistema non ha, e non c'è niente da convertire — e un
rimando al chassis non è vuoto affatto. `build_classi.py` il conto lo faceva
giusto, sugli stati `pending`; era la verifica a chiedergli un numero diverso
da quello che dichiara.

È il difetto più insidioso dei tre tipi visti oggi, perché **non fallisce:
segnala**. Un controllo rotto e uno funzionante tacciono uguale su un
repository pulito, ma un controllo rotto che parla costa la lettura di tutte
le altre segnalazioni — e in questo caso metteva `cavaliere-rosa` in una
tabella di difetti per un privilegio che difetto non era.

### 2.3 Percorsi disomogenei

75 percorsi su 167 non compaiono in tutte le
20 classi. La maggior parte è legittima e attesa: un minimo di
caratteristica esiste solo dove la fonte lo pone, i titoli di livello solo
dove la 2e li stampa. Ma la disomogeneità non è distinguibile dall'errore
finché nessuno schema dice quale campo è facoltativo e quale no — che è
esattamente ciò che manca.

I casi in cui la disomogeneità segue una regola strutturale:

| percorso | classi | regola |
|---|--:|---|
| `mechanics_5e.chassis.table_transcribed` | 12/20 | solo le classi con un chassis SRD |
| `mechanics_5e.chassis_features[].name` | 4/20 | solo le tre classi su chassis Fighter: le altre hanno la lista vuota |
| `mechanics_5e.ability_minimums.values.int` | 9/20 | solo dove la fonte 2e pone un minimo |

### 2.4 Un chassis senza nessun privilegio di chassis

| classe | chassis SRD | privilegi da trascrivere |
|---|---|--:|
| `cavaliere-rosa` | Paladin | 16 |
| `cavaliere-spada` | Paladin | 16 |
| `con-artist` | Rogue | 16 |
| `ladro` | Rogue | 16 |
| `mago-alta-stregoneria` | Wizard | 8 |
| `mago-rinnegato` | Wizard | 8 |
| `paladino` | Paladin | 16 |
| `sacerdote-ordini-sacri` | Cleric | 16 |

Non è un errore: la prima fetta verticale ha compilato il solo chassis
Fighter, e le altre restano nomi dentro il filtro. È in tabella perché è
**indistinguibile da un errore** senza uno schema che dica se
`chassis_features` possa essere vuota quando `chassis.srd_class` è pieno.

### 2.5 Tipi variabili

| percorso | tipi in uso |
|---|---|
| `mechanics_5e.chassis_features[].effetto.risorsa.usi` | `dict`, `int` |

Unico caso, e legittimo: `risorsa.usi` è un intero dove gli usi sono fissi e un oggetto `per_livello` dove crescono. `effetto.schema.json` lo dichiara già con un `anyOf` — ed è la prova che dove lo schema c'è, la variabilità è descritta invece che subita.

---

## 3. Non è una zona morta, sono tre

Il Personaggio lega razza + classe + divinità. Gli altri due ingressi stanno
nella stessa condizione, e uno sta peggio:

| strato | file | percorsi in uso | dichiarati dallo schema | `mechanics_5e` null |
|---|--:|--:|--:|--:|
| **classe** | 20 | 167 | 16 | 0 |
| **razza** | 15 | 107 | 69 | 0 |
| **divinita** | 21 | 0 | 0 | 21 |

`razza.schema.json` dichiara **zero** proprietà per `mechanics_5e`, su
107 percorsi in uso:
peggio delle classi, che almeno ne hanno 16. È lo strato dove
vive il tappo della decisione 20 (`tappo-barbaro`), in
`razze/umano-barbaro.json`: il campo che esiste solo in `mechanics_5e` e che
il motore, leggendo `source_2e`, scartava in silenzio. Il difetto trovato ieri
stava dentro la zona morta più grande delle tre, e nessuno schema lo
descriveva.

`divinita.schema.json` dichiara zero proprietà su zero percorsi in uso: tutte
e 21 le divinità hanno
`mechanics_5e` a null. È una zona morta vuota: nessun rischio oggi, nessuna
guardia domani.

### Il termine di paragone: gli schemi che sono stati chiusi

| strato | file | percorsi in uso | dichiarati | `additionalProperties` |
|---|--:|--:|--:|:-:|
| **mostro** | 52 | 160 | 90 | `False` |
| **oggetto** | 79 | 60 | 51 | `False` |
| **modello** | 3 | 108 | 82 | `False` |

Sono la misura vera del costo: `mostro` dichiara
90 percorsi per
160 in uso su
52 file, con
`additionalProperties: false`. Il lavoro sulle classi è dello stesso ordine
di grandezza, su meno file.

---

## 4. Il conto

|  |  |
|---|--:|
| percorsi in uso sotto `mechanics_5e`, 20 file | 167 |
| già dichiarati da `classe.schema.json` | 16 |
| già dichiarati da `effetto.schema.json` (validati a parte) | 39 |
| **da dichiarare** | **113** |
| …di cui nominati almeno da un validatore | 52 |
| …di cui **nominati da nessuno** | **61** |
| blocchi di primo livello da descrivere | 13 |
| campi scalari che diventano `enum` letti dai dati | 15 |
| incoerenze: **stato dichiarato**, da descrivere | **9** |
| incoerenze: **difetti**, da correggere | **0** |

**Il costo non è nei 113 percorsi.** Sono
13 blocchi, e uno solo —
`structural` — ne porta 68: è la scheda 2e
riportata intera (tabella dei punti esperienza, progressione d'attacco, tiri
salvezza, competenze, titoli, equipaggiamento iniziale), cioè un lavoro di
trascrizione, non di decisione.

La decisione unica dentro il conto è `features`: 8
percorsi che descrivono **la stessa forma di elemento** — nome, livello,
stato, prosa, nota — già descritta due volte altrove, in `elemento_5e` di
`mostro.schema.json` e nel blocco `chassis_features` di questo stesso file.
Tre copie della stessa forma è la domanda a cui questo progetto ha già
risposto sei volte.

Le incoerenze non sono un pezzo a parte del conto, e per metà del 04/09/2026
lo sono sembrate. Le 9 di stato dichiarato **sono** il lavoro
di schema, viste da un altro lato: un chassis SRD con `chassis_features` vuota
e un `risorsa.usi` che è intero o oggetto non sono dati sbagliati, sono dati
veri che nessuna dichiarazione ammette ancora. Chiuderle vuol dire scrivere
`anyOf` e condizioni, non toccare un file di classe.

Difetti da correggere prima non ce ne sono: il vincolo — `additionalProperties: false` non si mette sopra dati che lo violano — è già soddisfatto, e quello che resta è tutto lavoro di dichiarazione.

---

## 5. Il lato razza, con lo stesso metro

§3 diceva che le zone morte sono tre e che una sta peggio. Questa è quella,
misurata come le classi invece che citata di sfuggita.

`razza.schema.json` descrive `mechanics_5e` come un oggetto senza **nessuna**
proprietà dichiarata: 107 percorsi in uso nei 15 file,
69 dichiarati.

> **38 percorsi su 107** non sono dichiarati da nessuno
> schema, e **0** non sono nominati nemmeno da un
> validatore.

| blocco di primo livello | percorsi in uso | non dichiarati | razze che lo portano |
|---|--:|--:|--:|
| `ability_constraints` | 23 | 12 | 15/15 |
| `ability_adjustments` | 21 | 14 | 15/15 |
| `physical` | 12 | 0 | 15/15 |
| `generation` | 11 | 6 | 15/15 |
| `ability_caps` | 10 | 6 | 15/15 |
| `traits` | 9 | 0 | 15/15 |
| `traits_by_status` | 5 | 0 | 15/15 |
| `allowed_classes` | 4 | 0 | 15/15 |
| `level_limits` | 3 | 0 | 15/15 |
| `darkvision_note` | 1 | 0 | 15/15 |
| `speed_ft` | 1 | 0 | 15/15 |
| `size` | 1 | 0 | 15/15 |
| `movement_note` | 1 | 0 | 15/15 |
| `languages_note` | 1 | 0 | 15/15 |
| `movement_2e` | 1 | 0 | 15/15 |
| `languages` | 1 | 0 | 15/15 |
| `conversion_status` | 1 | 0 | 15/15 |
| `darkvision_ft` | 1 | 0 | 15/15 |

4 blocchi da
descrivere, contro i 13 delle
classi. Il blocco più pesante è
`ability_adjustments` con
14 percorsi.
27 percorsi su 107 non compaiono in tutte le
razze: come per le classi, la disomogeneità è cosa uno schema deve decidere se
ammettere, e finché non c'è schema non è stata decisa.

### 5a. Le dichiarazioni di origine: due casi, non uno

`RAPPORTO-origine.md` §5b misura lo stesso difetto su un campo solo,
`conversion_status` di livello elemento, e dà il numero grosso. Qui va spezzato
in due, perché costano cose diverse:

| famiglia | blocco | dichiarazioni | lo schema le vede? |
|---|---|--:|---|
| classe | `chassis_features` | 20 | **no** |
| classe | `features` | 43 | **no** |
| razza | `traits` | 105 | **no** |

- **168 dichiarazioni che nessuno schema vede.** Stanno in blocchi che
  lo schema non descrive affatto: `traits` delle razze e `features` delle
  classi. Si chiudono descrivendo il blocco, cioè dentro il lavoro già contato
  sopra — non sono una voce in più.
- **0 dichiarazioni che lo schema vede**, e di queste
  **0 lasciate libere**. Un campo dichiarato `"type": "string"` senza
  `enum` né `$ref` è il caso più insidioso di tutti, perché *sembra*
  controllato: non somiglia a una lacuna, e nessun conteggio di percorsi nudi
  lo trova. **Non ne resta nessuno.** `chassis_features` è stato agganciato alla sede del vocabolario il 04/09/2026, la stessa che i mostri, gli oggetti e i modelli usano già, ed è costato la riga che era stato previsto costasse. La verifica non è affidata alla lettura: `_schemi.verifica_riferimenti()` prova su questo schema che il termine abbandonato `fonte` venga davvero rifiutato — senza registro dei `$ref` un validatore non fallisce rumorosamente, lascia passare tutto.

### 5b. Il conto delle due zone morte insieme

|  | classe | razza | insieme |
|---|--:|--:|--:|
| file | 20 | 15 | 35 |
| percorsi in uso sotto `mechanics_5e` | 167 | 107 | 274 |
| già dichiarati dallo schema | 16 | 69 | 85 |
| già dichiarati da `effetto.schema.json` | 39 | 0 | 39 |
| **da dichiarare** | **113** | **38** | **151** |
| …nominati da nessun validatore | 61 | 0 | 61 |
| blocchi di primo livello da descrivere | 13 | 4 | 17 |
| incoerenze: stato dichiarato | 9 | — | 9 |
| incoerenze: difetti | 0 | — | 0 |

Il termine di paragone resta quello di §3: `mostro.schema.json` dichiara
90 percorsi su
160 in uso, con
`additionalProperties: false`, su 52
file. Le due zone morte insieme chiedono
151 dichiarazioni contro le
90 già scritte per il
mostro — 1.7
volte quel lavoro — su 35 file invece di
52. E non ci sono più difetti da correggere prima: i 9 che restano sono stato dichiarato, cioè questo stesso lavoro visto da un altro lato.

**L'ordine che costa meno**, e non è quello dei numeri:

1. ~~Le 0 dichiarazioni di `chassis_features`~~ — **fatto il 04/09/2026**: `$ref` alla sede del vocabolario, più la sonda che prova che il riferimento risolva. La voce resta in elenco perché il costo previsto e quello pagato coincidano in chiaro.
2. Il blocco `features` (8 percorsi): è la stessa
   forma di elemento già descritta due volte altrove, e va risolta una volta
   per tutte e tre invece che una terza volta qui. È l'unica decisione dentro
   il conto.
3. I due blocchi grossi delle razze —
   `ability_adjustments` (14), `ability_constraints` (12)
   — che sono numeri e limiti, cioè trascrizione con `enum` e `minimum`
   leggibili dai dati, non decisioni.
4. `structural` (68 percorsi): il pezzo più grosso
   di tutti e il meno rischioso, perché è la scheda 2e riportata intera.

Le 9 incoerenze di stato dichiarato non sono una voce in più
della scaletta: sono le stesse righe viste dal lato dei dati — `chassis_features`
vuota si descrive dentro il blocco `features`/`chassis_features`, `risorsa.usi`
è già descritto da `effetto.schema.json`. Difetti da correggere prima non ce ne sono più.

---

*Nessuna decisione è presa in questo documento, e nessuno schema è toccato.*
