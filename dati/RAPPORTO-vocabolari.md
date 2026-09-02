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

> **2 vocabolari aperti su 8 esaminati**, piu' 3 con una sede sola.

---

## 1. Il quadro

| vocabolario | sedi | valori distinti | come e' tenuto fermo | stato |
|---|--:|--:|---|---|
| tipi di danno | 5 | 7 | schema | **chiuso** |
| condizioni | 3 | 15 | niente, valida_effetti.py, controllo 3 | **APERTO** — 1 sede scoperta su 3 |
| taglia | 2 | 6 | niente, schema | **APERTO** — 1 sede scoperta su 2 |
| tipo di creatura | 1 | 11 | niente | una sede sola |
| scuole di magia | 1 | 8 | schema | una sede sola, vincolata |
| categorie d'arma | 2 | 2 | schema, valida_effetti.py, controllo 4 | **chiuso** |
| categorie d'armatura | 2 | 4 | schema, valida_effetti.py, controllo 4 | **chiuso** |
| allineamento | 1 | 12 | niente | una sede sola |

---

## 2. Sede per sede

### tipi di danno

- `dati/oggetti/` → `mechanics_5e.weapon_5e.damage_type` — 4 valori distinti su 37 occorrenze, **schema**. `perforante`, `tagliente`, `contundente`, `nessuno`
- `dati/mostri/` → `mechanics_5e.*.effetto.attacco.danno[].tipo` — 1 valori distinti su 2 occorrenze, **schema**. `perforante`
- `dati/mostri/` → `mechanics_5e.damage_resistances[].tipo` — 4 valori distinti su 19 occorrenze, **schema**. `contundente`, `perforante`, `tagliente`, `da_fuoco`
- `dati/mostri/` → `mechanics_5e.damage_immunities[].tipo` — 3 valori distinti su 11 occorrenze, **schema**. `da_veleno`, `da_freddo`, `da_fuoco`
- `dati/mostri/` → `mechanics_5e.damage_vulnerabilities[].tipo` — 2 valori distinti su 3 occorrenze, **schema**. `da_freddo`, `da_fuoco`

### condizioni

- `dati/mostri/` → `mechanics_5e.condition_immunities[]` — 10 valori distinti su 35 occorrenze, **scoperta**. `charmed`, `poisoned`, `exhaustion`, `paralyzed`, `frightened`, `grappled`
- `dati/condizioni/` → `id` — 5 valori distinti su 5 occorrenze, **valida_effetti.py, controllo 3**. `incapacitato`, `incosciente`, `pietrificato`, `prono`, `trattenuto`
- `dati/mostri/` → `mechanics_5e.*.effetto.tiro_salvezza.*.condizioni[].id` — 2 valori distinti su 2 occorrenze, **valida_effetti.py, controllo 3**. `trattenuto`, `pietrificato`

### taglia

- `dati/mostri/` → `mechanics_5e.size` — 6 valori distinti su 52 occorrenze, **schema**. `Medium`, `Large`, `Tiny`, `Small`, `Gargantuan`, `Huge`
- `dati/razze/` → `mechanics_5e.size` — 2 valori distinti su 15 occorrenze, **scoperta**. `Medium`, `Small`

### tipo di creatura

- `dati/mostri/` → `mechanics_5e.type` — 11 valori distinti su 52 occorrenze, **scoperta**. `Beast`, `Monstrosity`, `Humanoid`, `Undead`, `Fiend`, `Aberration`

### scuole di magia

- `dati/incantesimi/` → `school` — 8 valori distinti su 319 occorrenze, **schema**. `Evocation`, `Transmutation`, `Conjuration`, `Abjuration`, `Enchantment`, `Divination`

### categorie d'arma

- `dati/oggetti/` → `mechanics_5e.weapon_5e.categoria` — 2 valori distinti su 37 occorrenze, **schema**. `da_guerra`, `semplice`
- `dati/classi/` → `mechanics_5e.structural.weapon_proficiencies.categorie[]` — 2 valori distinti su 6 occorrenze, **valida_effetti.py, controllo 4**. `semplice`, `da_guerra`

### categorie d'armatura

- `dati/oggetti/` → `mechanics_5e.armor_5e.categoria` — 4 valori distinti su 13 occorrenze, **schema**. `media`, `pesante`, `leggera`, `scudo`
- `dati/classi/` → `mechanics_5e.structural.armor_proficiencies.categorie[]` — 4 valori distinti su 12 occorrenze, **valida_effetti.py, controllo 4**. `leggera`, `media`, `pesante`, `scudo`

### allineamento

- `dati/mostri/` → `mechanics_5e.alignment` — 12 valori distinti su 52 occorrenze, **scoperta**. `Unaligned`, `Typically Chaotic Evil`, `Typically Lawful Evil`, `Typically Neutral Good`, `Typically Neutral Evil`, `Typically Chaotic Good`

---

## 3. I tre casi che restano aperti, e cosa costa chiuderli

**`condition_immunities` — lo stesso difetto dei tipi di danno, un anno piu'
avanti.** `dati/mostri/` dichiara le immunita' a condizione con i nomi inglesi
della 5e (10 distinti su 35 occorrenze: `charmed`, `poisoned`, `petrified`,
`prone`, `restrained`...), mentre `dati/condizioni/` — che decisione 48
(`condizioni-a-consumo`) dichiara sede unica — ha 5 id italiani. Il campo
`effetto` risolve contro la sede italiana e il controllo 3 lo verifica;
`condition_immunities` non risolve contro niente. E' **piu' grave** dei tipi
di danno, perche' li' le due sedi erano due trascrizioni e qui una delle due
e' una **sede dichiarata** che l'altra ignora.

Non si chiude senza una decisione, e le due strade costano cose diverse.
**Tradurre e basta** significa che le 10 condizioni citate dalle immunita'
diventano id italiani, e solo 3 di quegli id esistono in `dati/condizioni/`
(`pietrificato`, `prono`, `trattenuto`). Gli altri **7** non esistono
(`affascinato`, `afferrato`, `avvelenato`, `paralizzato`, `sfinimento`,
`spaventato`, `stordito`): o si accettano riferimenti che non risolvono, o si
creano 7 condizioni per anticipazione — cioe' si sconfessa il criterio di
decisione 48 (`condizioni-a-consumo`), applicato per la prima volta tre giorni
fa. **Restringere l'enum alle cinque esistenti** e' peggio: le schede
perderebbero informazione vera di fonte. La terza strada — un vocabolario
delle condizioni **separato** dalla cartella delle condizioni convertite, dove
l'id esiste come termine e la scheda meccanica arriva dopo — e' probabilmente
quella giusta e non e' una riga di enum: e' la stessa distinzione fra
*nominare* e *convertire* che il progetto fa gia' altrove.

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

**`tipo di creatura`, `allineamento`, `scuole di magia` — una sede sola.**
Nessuno dei tre e' rotto e nessuno dei tre e' al sicuro. Le scuole hanno un
enum e stanno bene. `mechanics_5e.type` dei mostri (11 valori distinti,
inglese maiuscolizzato) **non ha enum**: il giorno in cui un secondo file — un
modello, un incantesimo che filtra per tipo di creatura — nominera' gli stessi
termini, il difetto nasce li'. `mechanics_5e.alignment` (12 valori distinti)
**non e' un vocabolario affatto**: e' prosa, e ne porta la prova un valore
solo, «Typically Chaotic Evil (solo quando animata da un incantesimo malvagio;
altrimenti inanimata e innocua)». Vincolarlo a un enum vorrebbe dire buttare
via quella clausola o darle un campo — la stessa forma del problema che
`solo_se` ha risolto per le resistenze, e la stessa risposta gia' pronta.

---

*Nessuna decisione e' presa in questo documento oltre a quelle gia'
registrate. I tre casi aperti sono misurati, non chiusi: due di loro tirano
dentro un lavoro dichiarato a se' (le zone morte di schema, il criterio delle
condizioni), e chiuderli di straforo sarebbe la scorciatoia che questo
progetto paga sempre due volte.*
