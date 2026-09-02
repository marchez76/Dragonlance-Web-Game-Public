# La zona morta delle classi — quanto costa chiuderla

*Generato da `dati/analizza_zona_morta_classi.py` il 2026-09-02. Non modificare a
mano: ogni numero è interpolato dai dati.*

---

## 0. La misura in una riga

`classe.schema.json` descrive `mechanics_5e` come *object o null*, con
14 proprietà dichiarate su **162 percorsi in uso** nei
17 file. Nessun `additionalProperties`.

> **110 percorsi su 162** non sono dichiarati da nessuno
> schema. Di questi, **77 non sono nominati nemmeno da un
> validatore**: un campo scritto storto lì dentro non incontra nessun
> controllo, in nessun punto della catena.

I 39 percorsi sotto `effetto` non sono contati fra i nudi:
sono validati a parte contro `effetto.schema.json` da `valida_effetti.py`.
Sono l'unico pezzo dello strato che ha una verifica vera.

---

## 1. Dove stanno i 110 percorsi nudi

| blocco di primo livello | percorsi in uso | non dichiarati | classi che lo portano |
|---|--:|--:|--:|
| `structural` | 68 | 68 | 17/17 |
| `chassis_features` | 49 | 0 | 17/17 |
| `ability_minimums` | 10 | 10 | 17/17 |
| `features` | 9 | 9 | 17/17 |
| `chassis` | 9 | 9 | 17/17 |
| `level_limits` | 3 | 3 | 17/17 |
| `race_restriction` | 3 | 3 | 17/17 |
| `alignment_restriction` | 3 | 3 | 17/17 |
| `chassis_features_da_trascrivere` | 3 | 0 | 17/17 |
| `conversion_status` | 1 | 1 | 17/17 |
| `hit_die` | 1 | 1 | 17/17 |
| `entry_level` | 1 | 1 | 17/17 |
| `prerequisite_class` | 1 | 1 | 17/17 |
| `features_pending` | 1 | 1 | 17/17 |

Il conto del lavoro si legge da questa tabella: non sono
110 decisioni indipendenti, sono **12
blocchi** da descrivere, e due di essi (`structural`, `ability_minimums`)
pesano da soli
78 percorsi su 110.

### Quanto è già deciso

14 campi scalari hanno **fra due e sei valori distinti** in tutto il
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
| `mechanics_5e.hit_die` | `1d10`, `1d6`, `1d8` |

---

## 2. Le incoerenze fra classi

**12 in tutto**, in 4 famiglie.

### 2.1 Uno stato di conversione che promette una meccanica che non c'è

`pending`, `source_only` sono gli stati in cui la meccanica 5e
può mancare — è scritto nella descrizione di `elemento_5e` in
`mostro.schema.json`, ed è l'invariante che distingue *«non è ancora stato
scritto»* da *«è stato scritto che non succede niente»*. Le classi la
violano:

| classe | blocco | privilegio | stato dichiarato |
|---|---|---|---|
| `cavaliere-rosa` | `features` | Immunita' alla paura | **`direct`** |
| `cavaliere-spada` | `features` | Capacita' del paladino | **`direct`** |

Non è una svista di battitura: `direct` significa *conversione conclusa senza
adattamenti*. Due privilegi dichiarano di essere convertiti e non portano
niente.

### 2.2 Il numero che dice quanto manca non conta quei due

| classe | `features_pending` dichiarato | privilegi davvero senza meccanica |
|---|--:|--:|
| `cavaliere-corona` | 1 | 2 |
| `cavaliere-rosa` | 0 | 1 |
| `cavaliere-spada` | 2 | 3 |

`features_pending` conta gli stati `pending`, non i blocchi vuoti. La
conseguenza è quella che conta: **`cavaliere-rosa` dichiara zero privilegi in
sospeso e ne ha uno vuoto.** È il numero che una schermata di stato
mostrerebbe come «classe completa».

Questa è la stessa forma del difetto già visto sei volte in questo progetto —
un derivato scritto accanto al dato invece che ricavato dal dato — e questa
volta è dentro lo strato che nessuno valida.

### 2.3 Percorsi disomogenei

70 percorsi su 162 non compaiono in tutte le
17 classi. La maggior parte è legittima e attesa: un minimo di
caratteristica esiste solo dove la fonte lo pone, i titoli di livello solo
dove la 2e li stampa. Ma la disomogeneità non è distinguibile dall'errore
finché nessuno schema dice quale campo è facoltativo e quale no — che è
esattamente ciò che manca.

I casi in cui la disomogeneità segue una regola strutturale:

| percorso | classi | regola |
|---|--:|---|
| `mechanics_5e.chassis.table_transcribed` | 9/17 | solo le classi con un chassis SRD |
| `mechanics_5e.chassis_features[].name` | 3/17 | solo le tre classi su chassis Fighter: le altre hanno la lista vuota |
| `mechanics_5e.ability_minimums.values.int` | 9/17 | solo dove la fonte 2e pone un minimo |

### 2.4 Un chassis senza nessun privilegio di chassis

| classe | chassis SRD | privilegi da trascrivere |
|---|---|--:|
| `cavaliere-rosa` | Paladin | 16 |
| `cavaliere-spada` | Paladin | 16 |
| `con-artist` | Rogue | 16 |
| `mago-alta-stregoneria` | Wizard | 8 |
| `mago-rinnegato` | Wizard | 8 |
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
| **classe** | 17 | 162 | 14 | 0 |
| **razza** | 15 | 107 | 0 | 0 |
| **divinita** | 21 | 0 | 0 | 21 |

`razza.schema.json` dichiara **zero** proprietà per `mechanics_5e`, su
107 percorsi in uso:
peggio delle classi, che almeno ne hanno 14. È lo strato dove
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
| **mostro** | 52 | 147 | 90 | `False` |
| **oggetto** | 79 | 60 | 51 | `False` |
| **modello** | 3 | 108 | 82 | `False` |

Sono la misura vera del costo: `mostro` dichiara
90 percorsi per
147 in uso su
52 file, con
`additionalProperties: false`. Il lavoro sulle classi è dello stesso ordine
di grandezza, su meno file.

---

## 4. Il conto

|  |  |
|---|--:|
| percorsi in uso sotto `mechanics_5e`, 17 file | 162 |
| già dichiarati da `classe.schema.json` | 14 |
| già dichiarati da `effetto.schema.json` (validati a parte) | 39 |
| **da dichiarare** | **110** |
| …di cui nominati almeno da un validatore | 33 |
| …di cui **nominati da nessuno** | **77** |
| blocchi di primo livello da descrivere | 12 |
| campi scalari che diventano `enum` letti dai dati | 14 |
| **incoerenze già presenti nei dati** | **12** |

**Il costo non è nei 110 percorsi.** Sono
12 blocchi, e uno solo —
`structural` — ne porta 68: è la scheda 2e
riportata intera (tabella dei punti esperienza, progressione d'attacco, tiri
salvezza, competenze, titoli, equipaggiamento iniziale), cioè un lavoro di
trascrizione, non di decisione.

La decisione unica dentro il conto è `features`: 9
percorsi che descrivono **la stessa forma di elemento** — nome, livello,
stato, prosa, nota — già descritta due volte altrove, in `elemento_5e` di
`mostro.schema.json` e nel blocco `chassis_features` di questo stesso file.
Tre copie della stessa forma è la domanda a cui questo progetto ha già
risposto sei volte.

Il pezzo che non si risolve da solo sono le 12 incoerenze: non si
chiude uno schema attorno a dati che lo violano. `additionalProperties: false`
con `conversion_status: direct` e `mechanics_5e: null` insieme non passa —
o si corregge il dato, o si scrive nello schema che quello stato ammette il
vuoto, cioè si dichiara che l'invariante non vale.

*Nessuna decisione è presa in questo documento, e nessuno schema è toccato.*
