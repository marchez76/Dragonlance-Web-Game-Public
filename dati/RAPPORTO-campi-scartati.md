# Campi disponibili e non estratti

*Generato da `dati/analizza_campi_scartati.py` il 2026-09-02. Non modificare a
mano: i numeri sono interpolati dai dati, un numero scritto qui si sfasa alla
prossima rigenerazione.*

---

## 0. Cosa misura, e perché nessun controllo esistente lo vedeva

**«La categoria d'arma non era un dato mancante, era un dato scartato.»**

Un parser che butta nella prosa un campo che la fonte dà strutturato produce
qualcosa che **sembra una lacuna della fonte**. Il dato formalmente non manca:
c'è, dentro una frase. Nessuno schema lo segnala — lo schema descrive i nostri
campi, non quelli della fonte. Nessun validatore lo segnala — i validatori
confrontano i nostri dati con i nostri dati. Il confronto che mancava è con
**l'elenco dei campi della fonte**, e quell'elenco non stava in nessun file.

Ora sta in `dati/_fonti/srd51_campi_disponibili.py`, con la stessa forma delle
altre trascrizioni di quella cartella: una fotografia datata, con la sonda
dichiarata. Per ogni campo di fonte è scritta **la destinazione nei nostri
dati**, e questo script la verifica invece di crederle: **35
destinazioni dichiarate, 35 trovate davvero nei file prodotti**. Una
destinazione dichiarata e non trovata fa fallire lo script — sarebbe la
settima struttura doppia del progetto, e questa volta è sorvegliata dal primo
giorno.

---

## 1. La misura

Endpoint che leggiamo davvero:

| endpoint | campi utili | estratti | scartati | destinazione nostra |
|---|--:|--:|--:|---|
| v1/weapons | 8 | 8 | **0** | _fonti/srd51_equipaggiamento.py ARMI -> dati/oggetti/ |
| v1/armor | 14 | 8 | **6** | _fonti/srd51_equipaggiamento.py ARMATURE -> dati/oggetti/ |
| v2/items | 18 | 3 | **15** | _fonti/srd51_equipaggiamento.py ATTREZZATURA -> dati/oggetti/; per le armi e' l'endpoint NON letto |
| v1/spells | 26 | 16 | **10** | _fonti/srd51_incantesimi.py -> dati/incantesimi/ |
| v1/monsters | 46 | 7 | **39** | _fonti/srd51_mostri.py -> riscontro di calibrazione |

I «campi utili» escludono i metadati di licenza e provenienza dell'API
(`document__slug`, `document__title`, `document__license_url`,
`document__url`), che non sono dati di gioco.

> **70 campi su 112** disponibili negli endpoint che già
> leggiamo non vengono estratti — il **62%**.
> Ne estraiamo 42.

Endpoint della stessa API che non apriamo affatto:

| endpoint | campi | cosa contiene di rilevante |
|---|--:|---|
| v2/creatures | 38 | attacchi scomposti in campi (`to_hit_mod`, `damage_die_count`, `damage_die_type`, `damage_bonus`, `reach`, `range`) |
| v2/spells | 33 | danno, tiro salvezza, area e gittata come campi (`damage_roll`, `saving_throw_ability`, `shape_type`, `range`) |

> Altri **71 campi** stanno in due endpoint che non abbiamo mai
> aperto. Non è una svista: la scelta di stare su `v1` è documentata in
> `_fonti/srd51_incantesimi.py` (v1 ha un solo documento Wizards e non può
> mischiare edizioni; v2 sì, e `srd51_equipaggiamento.py` ha già dovuto
> filtrare a valle). Restano contati perché la domanda era *quanti campi
> disponibili non estraiamo*, e un campo disponibile su un altro endpoint
> della stessa API resta disponibile.

**Totale: 141 campi disponibili e non estratti.**

---

## 2. I tre casi che sono lo stesso caso

La categoria d'arma è stata corretta. Le altre tre occorrenze della stessa
forma stanno tutte in `build_oggetti.py`, e sono **aperte**.

### 2.1 La Classe Armatura — e qui la prova, non l'affermazione

L'endpoint `v1/armor` dà la CA in **sei campi**: `base_ac`, `plus_dex_mod`,
`plus_max`, `plus_flat_mod`, `plus_con_mod`, `plus_wis_mod`. Ne dà anche la
forma testuale, `ac_string`. Noi trascriviamo `ac_string` e poi
`build_oggetti.ca_strutturata()` la rilegge con 3 espressioni
regolari (`_CA_BASE`, `_CA_BONUS`, `_CA_MAXDEX`) per ricostruire quattro dei sei campi.

Non è un'ipotesi: il ricalcolo lo fa questo script. Per ognuna delle
**13** armature dell'SRD i sei campi di fonte sono stati messi contro
il nostro `ca_5e`.

> **13/13 coincidono.** Nessuna divergenza.

Che coincidano è il punto, non la rassicurazione: **il parsing funziona,
quindi non si vede.** È lo stesso difetto della categoria d'arma nella sua
forma più difficile da trovare — quella in cui il risultato è giusto. Il
costo non è un errore di oggi: è che tre espressioni regolari stanno fra noi
e un campo, e la prima armatura con una formula fuori dai tre schemi previsti
solleva `ValueError` invece di leggere un intero.

**Una divergenza di trascrizione trovata strada facendo.** Su una voce la nostra `ac_formula` non è quella della fonte: `shield` (fonte `0 +2`, nostra `+2`). Il campo `source_srd` dichiara una trascrizione diretta; quella stringa è stata normalizzata a mano. Il valore risultante è corretto, la trascrizione no.

### 2.2 Prezzo e peso dell'attrezzatura — il caso che costa davvero

Armi e armature hanno `cost_gp` e `weight_lb` in campi propri. Le
**28** voci di attrezzatura no: `build_oggetti.py` scrive
prezzo e peso **dentro una frase italiana** di `mechanics_5e.note`, nella
forma *«Peso N lb, costo N mo»*. Sono
**28/28**.

La fonte (`v2/items`) dà `cost` e `weight` come campi. Noi li leggiamo, li
usiamo per comporre una frase, e buttiamo via i campi.

Questo è il caso con una conseguenza già scritta altrove: la decisione 42
(`cambio-acciaio-oro`) è nata perché *«un personaggio non poteva comprare il
proprio equipaggiamento»*. Quella decisione ha dato il rapporto fra acciaio e
oro. Ma su 28 oggetti **non c'è un prezzo leggibile
a cui applicarlo**: c'è una frase che lo contiene.

### 2.3 Semplice o da guerra — un booleano riscritto da una stringa

`weapon_5e.categoria` (`semplice` / `da_guerra`) è ricavata cercando la parola
*Simple* dentro la stringa `category` di `v1/weapons`. L'endpoint `v2/items`
dà gli stessi due fatti come booleani, `is_simple` e `is_martial`, e dà le
proprietà come oggetti `{property, detail}` — cioè già separate nel nome e
nel suo parametro, che è esattamente il lavoro delle due espressioni regolari
`_GITTATA` e `_VERSATILE` di `build_oggetti.py`.

Questo è il caso più tenue dei tre: `v1` non offre i booleani, e restare su
`v1` è una scelta motivata. Va contato, non necessariamente corretto.

---

## 3. Incantesimi

| campo di fonte | cosa contiene | dove finisce da noi |
|---|---|---|
| `target_range_sort` | la gittata come intero (`150`) | **scartato** — teniamo la stringa «150 feet» |
| `page` | il rimando di pagina alla fonte | **scartato** |
| `archetype` | quali sottoclassi lo ottengono | **scartato** |
| `circles` | circoli druidici | **scartato** |
| `spell_lists` | l'elenco pulito delle classi | **scartato di proposito**: incompleto alla fonte, 76 voci su 319 senza Paladino |
| `components`, `ritual`, `concentration`, `level`, `spell_level` | duplicati testuali di campi che prendiamo già | **scartati senza costo** |

Due osservazioni di peso diverso.

`target_range_sort` è **la stessa forma del difetto**: la fonte dà il numero,
noi teniamo la frase. Un motore che deve sapere se il bersaglio è a tiro oggi
deve leggere `"150 feet"` con un'espressione regolare.

`page` merita una riga a sé. La convenzione delle pagine (CLAUDE.md, punto 4)
è una delle strutture su cui questo progetto è più rigoroso, e ogni voce del
bestiario porta `pages_pdf`. I 319 incantesimi **non hanno
nessun rimando di pagina**, e la fonte lo dava.

Il danno, il tiro salvezza, l'area e la gittata degli incantesimi non sono
scartati da `v1`: `v1` non li ha. Ci sono in `v2/spells`
(`damage_roll`, `saving_throw_ability`, `shape_type`, `shape_size`, `range`).
È l'unico punto del rapporto in cui il campo che serve esiste solo
sull'endpoint che abbiamo deciso di non leggere.

---

## 4. I mostri SRD — il riscontro che non abbiamo preso

`_fonti/srd51_mostri.py` trascrive **7 campi su
46**:
nome, taglia, tipo, CA, PF, velocità, grado di sfida. Gli altri
39 non vengono
letti.

Questo endpoint non è la fonte dei nostri mostri — quella è l'MC Dragonlance
Appendix — ma **il riscontro su cui si calibrano le conversioni per
analogia**. Lo scarto qui non è «dato perso», è «riscontro non disponibile».
Due voci contano più delle altre:

- **le sei caratteristiche.** Ogni nostro mostro porta un `abilities_note` che
  spiega che la 2e non le assegna e che vanno stimate dal profilo. La mediana
  per grado di sfida — che renderebbe quella stima *verificabile* invece che
  *argomentata* — sta in questo endpoint, e non l'abbiamo.
- **`actions`.** Ogni azione dell'SRD porta già `attack_bonus`, `damage_dice`
  e `damage_bonus` come campi. È esattamente la forma che manca ai nostri
  mostri per far girare uno scontro, ed è nella fonte che avevamo già in
  mano.

---

## 5. Il lato MC Appendix, e un esito negativo

La domanda era se i campi dell'MC finiscano in `abilities_text` invece che in
campi propri. **Al livello della scheda, no.** Vale la pena scriverlo, perché
è il contrario di quello che ci si aspettava.

I 21 campi canonici della scheda MC sono tutti estratti in `source_2e`, e i 7
senza corrispettivo 5e sono censiti e indirizzati dalla decisione 27
(`sette-campi-2e`). Restano due campi che *enunciano una meccanica in forma
libera*, `SPECIAL ATTACKS` e `SPECIAL DEFENSES`, su 52 creature:

|  | SPECIAL ATTACKS | SPECIAL DEFENSES |
|---|--:|--:|
| nullo (la fonte dice che non c'è) | 17 | 23 |
| rimanda alla prosa (*vedi sotto*) | 4 | 14 |
| enuncia una meccanica come stringa | 31 | 15 |
| …di cui con un numero dentro | 6 | 7 |

46 enunciati in forma libera, 13 dei quali contengono un
numero; 18 caselle che rimandano esplicitamente al testo.

**E arrivano a un campo 5e.** Delle 13 creature la cui
`SPECIAL DEFENSES` parla di immunità, resistenza o bonus ai tiri salvezza,
**13/13** hanno il campo 5e corrispondente
popolato (`damage_resistances`, `damage_immunities`, `condition_immunities` o
`saving_throws`). La conversione del bestiario **non ripete il difetto di
`build_oggetti.py`**: qui il campo di fonte non viene buttato nella prosa,
viene tradotto in un campo.

### Dove sta invece il materiale, nel bestiario

Non nei campi di scheda: nella **prosa narrativa 2e**, che è prosa anche alla
fonte. 123.662 caratteri di `abilities_text`, con
**350 riferimenti meccanici** dentro:

| famiglia | occorrenze | creature |
|---|--:|--:|
| espressioni di dado | 123 | 39 |
| bonus e malus numerici | 79 | 32 |
| richiami a tiri salvezza | 48 | 25 |
| percentuali | 36 | 15 |
| THAC0 e dadi vita | 27 | 15 |
| distanze | 19 | 11 |
| intervalli 2e (2-12) | 18 | 10 |

Questo **non è un dato scartato**: la fonte lo dà in prosa, e trascriverlo in
prosa è fedeltà, non perdita (decisione 15, `tratti-trascrizione-integrale`).
È la misura del serbatoio, non di un difetto — utile per sapere quanto resta
da convertire, non per accusare il parser.

### Il difetto del bestiario è un altro, ed è già misurato

257 blocchi di meccanica (128 tratti, 128
azioni, 1 reazione), **231 con la meccanica
scritta in una stringa italiana e 5 con un campo `effetto`**.
Non è materia di questo rapporto: sta in `RAPPORTO-personaggio.md` §5, ed è il
punto su cui lo schema `effetto.schema.json` è stato aperto.

---

## 6. Il conto

|  | campi |
|---|--:|
| disponibili negli endpoint che leggiamo (esclusi i metadati) | 112 |
| …estratti | 42 |
| …**scartati** | **70** |
| disponibili in endpoint mai aperti | 71 |
| **totale disponibile e non estratto** | **141** |

Dei 70 scartati negli endpoint che già leggiamo, quelli che ripetono
la forma del difetto trovato — **la fonte dà il campo, noi teniamo la
frase** — sono 9: i 6 campi della Classe Armatura, `cost` e `weight`
dell'attrezzatura, `target_range_sort` degli incantesimi. Gli altri sono
duplicati testuali, metadati di sottoclasse, o riscontro non richiesto.

*Nessuna correzione è applicata in questo documento.*
