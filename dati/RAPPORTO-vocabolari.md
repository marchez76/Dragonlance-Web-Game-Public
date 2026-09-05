# I vocabolari condivisi — quali sono gia' rotti e quali reggono per fortuna

*Generato da `dati/analizza_vocabolari.py`.*

---

## 0. La domanda

L'ottava struttura doppia del progetto sono stati i tipi di danno, e non e'
stata trovata ispezionando i dati: e' stata trovata **usandoli**. Nessuno dei
due lati era sbagliato dal proprio — `slashing` e' il termine dell'SRD,
`perforante` e' l'italiano dello strato nostro — quindi nessuno schema e
nessun validatore poteva vederlo. Chiusa con decisione 49
(`vocabolario-italiano`).

La domanda che resta e' se altri vocabolari condivisi abbiano lo stesso
difetto. Non si risponde a memoria: si contano le **sedi** di ogni termine, si
guarda se uno schema lo vincola, e — questa e' la parte che un conteggio
ingenuo sbaglia — si guarda se un **controllo incrociato** lo tiene fermo
anche senza schema. Le categorie d'arma non sono vincolate dallo schema delle
classi eppure non divergono, perche' il controllo 4 di `valida_effetti.py`
mette le due sedi una contro l'altra. Contarle come rotte sarebbe falso.

Un vocabolario con **una sede sola** non e' sano: e' **non ancora esposto**.
Il difetto arriva col prossimo file che usa lo stesso termine.

> **0 vocabolari aperti su 8 esaminati**, piu' 2 con una sede sola.

---

## 1. Il quadro

| vocabolario | sedi | valori distinti | come e' tenuto fermo | stato |
|---|--:|--:|---|---|
| tipi di danno | 5 | 7 | schema | **chiuso** |
| condizioni | 3 | 12 | schema, valida_effetti.py, controllo 3 | **chiuso** |
| taglia | 2 | 6 | schema | **chiuso** |
| tipo di creatura | 1 | 11 | niente | una sede sola |
| scuole di magia | 1 | 8 | schema | una sede sola, vincolata |
| categorie d'arma | 2 | 2 | schema, valida_effetti.py, controllo 4 | **chiuso** |
| categorie d'armatura | 2 | 4 | schema, valida_effetti.py, controllo 4 | **chiuso** |
| allineamento | 2 | 9 | schema | **chiuso** |

---

## 2. Sede per sede

### tipi di danno

- `dati/oggetti/` → `mechanics_5e.weapon_5e.damage_type` — 4 valori distinti su 37 occorrenze, **schema**. `perforante`, `tagliente`, `contundente`, `nessuno`
- `dati/mostri/` → `mechanics_5e.*.effetto.attacco.danno[].tipo` — 1 valori distinti su 2 occorrenze, **schema**. `perforante`
- `dati/mostri/` → `mechanics_5e.damage_resistances[].tipo` — 4 valori distinti su 19 occorrenze, **schema**. `contundente`, `perforante`, `tagliente`, `da_fuoco`
- `dati/mostri/` → `mechanics_5e.damage_immunities[].tipo` — 3 valori distinti su 11 occorrenze, **schema**. `da_veleno`, `da_freddo`, `da_fuoco`
- `dati/mostri/` → `mechanics_5e.damage_vulnerabilities[].tipo` — 2 valori distinti su 3 occorrenze, **schema**. `da_freddo`, `da_fuoco`

### condizioni

- `dati/mostri/` → `mechanics_5e.condition_immunities[]` — 10 valori distinti su 35 occorrenze, **schema**. `affascinato`, `avvelenato`, `sfinimento`, `paralizzato`, `spaventato`, `afferrato`
- `dati/condizioni/` → `id` — 5 valori distinti su 5 occorrenze, **valida_effetti.py, controllo 3**. `incapacitato`, `incosciente`, `pietrificato`, `prono`, `trattenuto`
- `dati/mostri/` → `mechanics_5e.*.effetto.tiro_salvezza.*.condizioni[].id` — 2 valori distinti su 2 occorrenze, **valida_effetti.py, controllo 3**. `trattenuto`, `pietrificato`

### taglia

- `dati/mostri/` → `mechanics_5e.size` — 6 valori distinti su 52 occorrenze, **schema**. `Medium`, `Large`, `Tiny`, `Small`, `Gargantuan`, `Huge`
- `dati/razze/` → `mechanics_5e.size` — 2 valori distinti su 15 occorrenze, **schema**. `Medium`, `Small`

### tipo di creatura

- `dati/mostri/` → `mechanics_5e.type` — 11 valori distinti su 52 occorrenze, **scoperta**. `Beast`, `Monstrosity`, `Humanoid`, `Undead`, `Fiend`, `Aberration`

### scuole di magia

- `dati/incantesimi/` → `school` — 8 valori distinti su 319 occorrenze, **schema**. `Evocation`, `Transmutation`, `Conjuration`, `Abjuration`, `Enchantment`, `Divination`

### categorie d'arma

- `dati/oggetti/` → `mechanics_5e.weapon_5e.categoria` — 2 valori distinti su 37 occorrenze, **schema**. `da_guerra`, `semplice`
- `dati/classi/` → `mechanics_5e.structural.weapon_proficiencies.categorie[]` — 2 valori distinti su 8 occorrenze, **valida_effetti.py, controllo 4**. `semplice`, `da_guerra`

### categorie d'armatura

- `dati/oggetti/` → `mechanics_5e.armor_5e.categoria` — 4 valori distinti su 13 occorrenze, **schema**. `media`, `pesante`, `leggera`, `scudo`
- `dati/classi/` → `mechanics_5e.structural.armor_proficiencies.categorie[]` — 4 valori distinti su 16 occorrenze, **valida_effetti.py, controllo 4**. `leggera`, `media`, `pesante`, `scudo`

### allineamento

- `dati/mostri/` → `mechanics_5e.alignment.valori[]` — 8 valori distinti su 34 occorrenze, **schema**. `caotico_malvagio`, `legale_malvagio`, `neutrale_buono`, `neutrale_malvagio`, `caotico_buono`, `caotico_neutrale`
- `dati/classi/` → `mechanics_5e.alignment_restriction.values[]` — 9 valori distinti su 23 occorrenze, **schema**. `legale_buono`, `neutrale_buono`, `caotico_buono`, `legale_malvagio`, `neutrale_malvagio`, `caotico_malvagio`

---

## 3. I casi aperti, e cosa costa chiuderli

**`condition_immunities` — chiusa, e non traducendo e basta.** `dati/mostri/`
dichiarava le immunita' a condizione con i nomi inglesi della 5e mentre
`dati/condizioni/` — che decisione 48 (`condizioni-a-consumo`) dichiara sede
unica — ha id italiani: stesso difetto dei tipi di danno, e **piu' grave**,
perche' li' erano due trascrizioni e qui una delle due sedi era gia'
**dichiarata unica** e l'altra la ignorava. Nessuna immunita' del bestiario
poteva essere rispettata da nessun motore.

Tradurre e basta non bastava, ed e' la ragione per cui il caso era rimasto
aperto: delle condizioni citate dalle immunita' solo 3 avevano una scheda in
`dati/condizioni/` (`pietrificato`, `prono`, `trattenuto`), quindi o si
accettavano 7 riferimenti che non risolvono, o si creavano 7 condizioni per
anticipazione — cioe' si sconfessava decisione 48 (`condizioni-a-consumo`) tre
giorni dopo averla presa.

Chiusa con decisione 53 (`condizioni-vocabolario-srd`) per la strada dei
repertori (decisione 35 (`repertori-sono-filtri`)): l'insieme delle condizioni
SRD e' **chiuso e noto**, quindi il vocabolario e' **completo** — 15 termini
in `vocabolari.schema.json`, riferiti per `$ref` da `mostro.schema.json` —
mentre il catalogo ne converte 5. Le altre 10 non sono condizioni
**inesistenti**: sono una **lacuna del nostro catalogo**, che e' cosa diversa,
e non si scrive da nessuna parte — si deriva dai file presenti nella cartella.

Il divario resta, e adesso e' un numero invece che un dubbio: **35 immunita'**
nel bestiario, di cui **29** nominano una delle 10 condizioni che il motore
non sa ancora applicare (`accecato`, `affascinato`, `afferrato`, `assordato`,
`avvelenato`, `invisibile`, `paralizzato`, `sfinimento`, `spaventato`,
`stordito`). Il motore lo **dichiara** — lacuna `condizione-non-modellata` —
perche' un'immunita' saltata in silenzio e' indistinguibile da un'immunita'
rispettata.

**`taglia` — due sedi, una sola vincolata, d'accordo per fortuna.**
`mostro.schema.json` ha l'enum `Tiny…Gargantuan`; `razza.schema.json` dichiara
**zero proprieta'** sotto `mechanics_5e` (e' una delle tre zone morte gia'
misurate in `RAPPORTO-zona-morta-classi.md`), quindi la taglia delle razze non
e' vincolata da niente. Oggi i valori coincidono — 2 valori sulle razze, tutti
dentro l'enum dei mostri — ma per fortuna, non per struttura: e' esattamente
lo stato in cui erano i tipi di danno prima di divergere. Chiuderlo e' **una
riga**: il `$ref` al vocabolario condiviso da entrambi gli schemi. Non e'
stato fatto in questo giro perche' tocca `razza.schema.json`, cioe' apre una
delle tre zone morte, e quello e' un lavoro a se'.

**`tipo di creatura` e `scuole di magia` — una sede sola, e non e' la stessa
cosa che essere al sicuro.** Le scuole hanno un enum e stanno bene.
`mechanics_5e.type` dei mostri (11 valori distinti, inglese maiuscolizzato)
**non ha enum**: il giorno in cui un secondo file — un modello, un incantesimo
che filtra per tipo di creatura — nominera' gli stessi termini, il difetto
nasce li'.

**L'`allineamento` non e' piu' fra questi.** Quando questo documento e' nato
**non era un vocabolario affatto** — era prosa inglese dentro lo strato
italiano, e ne portava la prova un valore solo, «Typically Chaotic Evil (solo
quando animata da un incantesimo malvagio; altrimenti inanimata e innocua)» —
e' ora chiuso da decisione 61 (`allineamento-insieme`), e per la strada che
questo stesso paragrafo indicava: non buttare via la clausola ne' l'avverbio,
ma dare a ciascuno un campo. La stringa portava tre cose e nessuna
verificabile; ora `forma` dice se la fonte scrive «typically» o se usa uno dei
due termini che la 5e mette AL POSTO di un allineamento, `valori` porta gli id
del vocabolario, `note` la clausola. Le sedi che lo nominano sono ora 2,
vincolate dallo stesso `$ref`.

---

*Nessuna decisione e' presa in questo documento oltre a quelle gia'
registrate. I casi ancora aperti sono misurati, non chiusi: tirano dentro un
lavoro dichiarato a se' (le zone morte di schema), e chiuderli di straforo
sarebbe la scorciatoia che questo progetto paga sempre due volte.*
