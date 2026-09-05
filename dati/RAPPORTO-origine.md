# L'origine di un valore — una sede, una forma, e cosa resta fuori

*Generato da `dati/analizza_origine.py`.*

---

## 0. Il difetto, e perche' era invisibile

Il progetto ha inventato il campo "origine di un valore" **quattro volte**
senza accorgersene. Tre volte sotto lo stesso nome — `conversion_status` piu'
`source` su `armor_class`, su `hit_points`, su `challenge_rating`, 156
dichiarazioni su 52 schede di mostro — e la quarta sotto un nome nuovo,
`cd_origine` con `cd_derivazione`, subito seguita dalla quinta,
`bonus_origine`. Decima struttura doppia del progetto, e in una forma che
nessuno dei controlli precedenti poteva vedere: non due file che divergono, ma
**lo stesso concetto con quattro nomi**.

Era invisibile per una ragione precisa. Una struttura doppia si scopre quando
le due copie si sfasano, e qui le copie non potevano sfasarsi perche' nessuno
le confrontava: ognuna viveva in un campo diverso, e ogni campo era coerente
con se stesso. Il difetto non stava nei dati — stava nel fatto che i dati
erano giusti quattro volte separate.

La decisione 54 (`origine-e-un-dato`) lo aveva visto e dichiarato aperto,
rimandando l'unificazione al momento in cui un campo ancora scoperto avesse
dovuto portare l'origine davvero. La decisione 55 (`origine-sede-unica`) e'
quel momento: ogni campo nuovo sarebbe stato la quinta reinvenzione.

---

## 1. Quante dichiarazioni ci sono, e di che tipo

846 dichiarazioni di origine nei dati, su 5 famiglie.

| famiglia | livello scheda | livello elemento | totale |
|---|--:|--:|--:|
| mostri | 52 | 416 | 468 |
| oggetti | 92 | 51 | 143 |
| modelli | 3 | 29 | 32 |
| razze | 15 | 105 | 120 |
| classi | 20 | 63 | 83 |
| **totale** | **182** | **664** | **846** |

> Cartelle di dati non guardate da questo controllo: `condizioni`, `divinita`, `incantesimi`, `pacchetti`. Vanno aggiunte a `CARTELLE` o dichiarate senza origine.

---

## 2. Un nome per due concetti — e la prova non e' una lettura

`conversion_status` nomina due cose diverse, e la parte utile e' che non serve
leggere le descrizioni per dimostrarlo. Il discriminante e' un conteggio: a
livello di **scheda** il campo `source` non c'e' **mai** (182 su 182); a
livello di **elemento** c'e' **sempre** (664 su 664). Due popolazioni che non
si toccano.

Anche i vocabolari sono disgiunti, ed e' la seconda prova:

| livello | significato | vocabolario usato nei dati |
|---|---|---|
| scheda | a che punto e' **questa scheda** | `clonato` (12), `compilato` (162), `in_sospeso` (8) |
| elemento | da dove viene **questo valore** | `adapted` (357), `derived` (1), `direct` (220), `pending` (54), `source_only` (32) |

Le classi usano `clonato` e `in_sospeso` dove le altre famiglie usano
`compilato`: e' un terzo vocabolario di scheda, non un'origine.

**Questo non e' stato unificato**, ed e' la prima cosa che resiste. Rinominare
il campo di scheda tocca le 182 schede piu' i generatori `build_*.py` che lo
scrivono: e' un giro suo, che va misurato e fatto con un controllo davanti,
non infilato dentro l'unificazione dell'origine. Finche' non e' fatto, il
rischio non e' teorico — e' che qualcuno legga `compilato` come un'origine, o
che un controllo sull'origine cominci a contare le schede.

---

## 3. La sede, e il fatto che una copia era gia' divergente

`conversion_status` e `provenienza` erano definiti **tre volte** in `$defs` —
`mostro`, `oggetto`, `modello` — e la copia di `oggetto` aveva **gia'** sette
voci contro cinque. La struttura doppia aveva gia' cominciato a sfasarsi, e
nessun dato la denunciava: un enum ricopiato valida benissimo finche' le copie
coincidono, e quando smettono di coincidere valida ancora, solo in modo
diverso in ogni file.

Oggi la sede e' `vocabolari.schema.json` — la stessa della decisione 49
(`vocabolario-italiano`) — e gli schemi la riferiscono:

| definizione | voci | schemi che la riferiscono |
|---|---|---|
| `conversion_status` | 5 | `modello.schema.json`, `mostro.schema.json`, `oggetto.schema.json`, `razza.schema.json` |
| `provenienza` | 8 | `classe.schema.json`, `modello.schema.json`, `mostro.schema.json`, `oggetto.schema.json` |

L'elenco delle provenienze e' l'**unione** delle tre copie (8 voci): `PHB 2e`,
`DMG 2e`, `MC - Dragonlance Appendix`, `Tales of the Lance`, `SotDQ (ufficiale
5e)`, `SRD 5.1`, `regola di sistema`, `conversione editoriale nostra`. La
fusione **allarga** il vincolo dei singoli schemi — `oggetto` accetta ora
valori che prima non accettava. E' il prezzo dichiarato di una sede sola, non
un effetto collaterale scoperto dopo.

### Il controllo si mette alla prova

Questo difetto non si vede dai dati: si vede solo guardando gli schemi. E su
un repository pulito un rilevatore rotto e uno funzionante **tacciono
uguale**. Quindi il rilevatore non si dichiara funzionante, si mette davanti
difetti costruiti apposta: 3 su 3 difetti piantati riconosciuti, 0 errori
nella prova, 0 problemi reali negli schemi.

I tre difetti piantati sono un enum ridigitato fuori sede, un `$defs`
condiviso che non e' un `$ref` alla sede, e un `conversion_status` senza
`source` accanto. Accanto stanno due somiglianze **legittime** che il
controllo non deve segnalare: e' la meta' che conta, perche' un rilevatore che
segnala tutto e' silenzioso quanto uno che non segnala niente.

---

## 4. La forma: il prefisso ERA il difetto

Il nome unico non e' un nome nuovo. `conversion_status` piu' `source` reggeva
da mesi su tre campi e 156 dichiarazioni: **si estende, non si sostituisce** —
ed e' il motivo per cui il rinominare temuto sulle 52 schede **non e'
servito**.

La traduzione dell'enum piu' giovane in quello piu' vecchio:

| `cd_origine` (2 campi, giovane) | `conversion_status` (3 campi, in opera) |
|---|---|
| `fonte` | `direct` |
| `stimata` | `adapted` |
| `derivata` | **`derived`** — l'unico che mancava |

`derived` e' l'unico valore che l'enum in opera non aveva, e non e' un
sinonimo di nessun altro: un valore derivato non e' `direct` (nessuno l'ha
stampato) ne' `adapted` (nessuno l'ha scelto). Ed e' **l'unico dei cinque che
un controllo puo' rifare**, il che lo rende l'unico che vale la pena
distinguere.

### L'oggetto, e perche' i prefissi non scalavano

Un valore e la sua origine viaggiano nello **stesso oggetto**:

    "bonus_colpire": {
      "value": 5,
      "conversion_status": "derived",
      "source": "regola di sistema",
      "note": "..."
    }

Che e' esattamente cio' che `armor_class` gia' era. La forma piatta a prefisso
— `cd_origine`, `bonus_origine` — non e' solo piu' brutta: **e' il
meccanismo** con cui il campo si e' reinventato quattro volte. `attacco` porta
due numeri che hanno ciascuno un'origine, `bonus_colpire` e `danno[].bonus`, e
ogni numero nuovo pretende un prefisso nuovo, che nessuno riconosce come lo
stesso campo.

Con l'incapsulamento l'origine **non puo' piu' mancare**, e non perche' un
controllo la pretende: perche' non c'e' un posto dove scrivere il valore senza
di essa. La clausola condizionale che obbligava il campo di origine e' stata
**cancellata** — la garanzia e' diventata strutturale, e una garanzia
strutturale non ha bisogno di essere ricordata.

Schemi che usano la forma incapsulata: `effetto.schema.json`. Valori gia'
scritti in questa forma nei dati: 3.

---

## 5. Cosa NON si e' lasciato unificare

### 5a. `source` come stringa libera in razze e classi

105 dichiarazioni di livello elemento portano un `source` che l'enum della
sede **non accetta**. La domanda utile non e' quante sono, ma quanto sono
lontane — e la risposta cambia il lavoro che serve:

| famiglia | valore o prefisso | casi | decomponibile? |
|---|---|--:|---|
| `razze` | `PHB 2e` | 70 | si', e' l'enum piu' un dettaglio |
| `classi` | `SRD 5.1` | 20 | si', e' l'enum piu' un dettaglio |
| `razze` | `MC - Dragonlance Appendix` | 11 | si', e' l'enum piu' un dettaglio |
| `razze` | *(stringa non riprodotta)* | 3 | no |
| `razze` | *(stringa non riprodotta)* | 1 | no |

**101 su 105 cominciano con un valore dell'enum.** Non sono un vocabolario
diverso: sono lo stesso valore piu' un dettaglio — il capitolo, la pagina
stampata, il fatto che sia stato letto da immagine. La fusione quindi non e'
bloccata, e' **decomposta**: `source` (enum, vincolato) piu' un campo di
dettaglio (stringa libera). Solo 4 non cominciano con nessun valore dell'enum,
e sono le uniche che chiedono davvero una decisione.

Perche' non e' stato fatto qui: quel dettaglio porta **piu'** informazione di
quella che l'enum trattiene, e buttarlo per uniformare sarebbe una perdita
netta. Decomporlo e' un giro suo, con il suo controllo.

### 5b. La zona morta: origine scritta, nessuno schema che la vincoli

| famiglia | schema | dichiarazioni di elemento | `conversion_status` dichiarati dallo schema | …di cui legati al vocabolario | vincolate? |
|---|---|--:|--:|--:|---|
| mostri | `mostro.schema.json` | 416 | 4 | 4 | si' |
| oggetti | `oggetto.schema.json` | 51 | 3 | 3 | si' |
| modelli | `modello.schema.json` | 29 | 2 | 2 | si' |
| razze | `razza.schema.json` | 105 | 2 | 2 | si' |
| classi | `classe.schema.json` | 63 | 2 | 2 | si' |

Il caso peggiore non e' un campo assente: e' un campo **scritto che sembra
validato e non lo e'**. Dove la colonna dice NO, l'origine e' scritta nei dati
con la stessa diligenza di tutte le altre, e nessun controllo la guarda: puo'
portare un valore che l'enum non prevede senza che niente lo dica. Sono **0
dichiarazioni** fra razze e classi. E' la stessa forma della zona morta gia'
misurata in `RAPPORTO-zona-morta-classi.md`, su un campo diverso — segno che
il difetto sta nello schema di quelle famiglie, non nel campo. Il costo di
chiuderla e' misurato li', in §5.

**Il rilevatore era rotto e diceva di no, il 04/09/2026.** La prima versione
cercava le stringhe `"conversion_status"` e `"enum"` nello stesso FILE invece
che nello stesso nodo, e `classe.schema.json` le contiene entrambe in due
punti che non c'entrano l'uno con l'altro: la famiglia risultava vincolata
mentre non vincola niente. Un rilevatore che dichiara chiusa una zona morta
aperta e' peggio di nessun rilevatore, perche' il numero che stampa viene
creduto. Ora si guarda il nodo, e il `$ref` locale verso la sede si segue fino
in fondo — che e' esattamente la forma che la decisione 55
(`origine-sede-unica`) ha dato al vincolo, e che un rilevatore fermo al primo
salto avrebbe chiamato scoperta.

### 5c. Il vocabolario di scheda delle classi

Le classi dichiarano `clonato` e `in_sospeso` dove le altre famiglie
dichiarano `compilato`. Sono stati di scheda, non origini, e restano fuori
dall'unificazione per la ragione di §2: sono l'altro concetto.

---

## 6. I campi che hanno la forma del difetto e non dichiarano ancora nulla

La forma ora esiste; applicarla dove manca e' lavoro di dati. Questi sono i
campi il cui valore puo' venire **sia** dalla fonte **sia** da una formula del
sistema — la condizione esatta in cui l'origine non e' deducibile:

| campo | dove | casi | torna col conto | dichiara l'origine? |
|---|---|--:|--:|---|
| `bonus_colpire` | prosa dei blocchi | 94 | 85 (90%) | no |
| bonus di danno | prosa dei blocchi | 110 | 96 (87%) | no |
| `skills[].bonus` | scheda | 18 | 16 (88%) | no |
| `passive_perception` | scheda | 52 | 52 (100%) | no |
| `hit_points.average` | scheda | 51 | 48 (94%) | si', nella forma unica |

**`passive_perception` e' il caso che insegna, e non perche' sia il piu'
grave.** Il conto torna il **cento per cento** delle volte, e proprio per
questo di **nessuna** delle 52 si sa se sia stata letta dalla fonte o
calcolata. La coincidenza perfetta non e' una conferma: e' **assenza totale di
informazione**. Un campo dove il conto torna sempre e' il posto peggiore in
cui fidarsi del conto — ed e' anche il posto dove un controllo basato sul
conto sembrera' per sempre soddisfatto.

Il verso opposto vale come regola: `hit_points.average` e' l'unico della
tabella che l'origine ce l'ha gia', ed e' anche l'unico che **non torna
sempre**. Non e' una coincidenza: l'origine e' stata scritta li' perche' li'
lo scarto si vedeva.

---

## 7. Dove il difetto non puo' esistere

Un campo che porta solo **ingressi** non ha questa forma. `saving_throws`
dichiara quali competenze il portatore ha, non il numero che ne segue: non
c'e' niente da confondere, perche' il numero non e' scritto da nessuna parte e
quindi non puo' contraddire il conto.

E' la stessa forma che la decisione 52 (`attacco-unica-lettura`) ha imposto al
personaggio, e la regola che ne segue e' la piu' utile di tutto il giro:
**un campo che si puo' non scrivere e' meglio di un campo la cui origine si
deve dichiarare**. Dichiarare l'origine e' il rimedio dove il valore *deve*
stare scritto — non il primo posto dove guardare.
