# Metodo di conversione — bestiario di Krynn (2e → 5e)

Prescrittivo, non diagnostico: dice COME convertire. Il PERCHÉ di ogni scelta
è in `dati/RAPPORTO-bestiario.md` — leggerlo una volta, poi usare questo per
ogni voce successiva. Regole confermate finora in
`feedback_conversione_bestiario.md` (memoria di sessione): questo documento
le riorganizza per l'uso, non le sostituisce.

## 1. I tre vincoli

1. **Ordinamento conservato, ma solo se si conserva il ruolo.** CA e potenza
   relativa 2e si possono portare in 5e finché la creatura resta quello che
   era in combattimento. Verificarlo *davvero* per ogni voce, non darlo per
   scontato: sul Kapak il ruolo era cambiato (assassino debole → duellante
   avvelenatore) e l'ordinamento si è rotto (GS 3 invece che il GS più basso
   previsto). Quando diverge, scrivere `ruolo_2e`/`ruolo_note`.
2. **I bonus numerici da tradurre in vantaggio, non gli effetti alla morte
   in sé.** Il vincolo riguarda cose come "+1 ai TS contro paura" → vantaggio
   (kender, Traag). Non si applica per riempire un vuoto che la fonte lascia
   deliberatamente vuoto: se il Traag "si scioglie in una pozza senza altro
   effetto", non si inventa un TS per farlo somigliare ai draconici veri.
3. **Danno per round almeno raddoppiato** rispetto al 2e (minimo osservato
   sui cinque draconici: ×1.6). Se sul caso specifico non regge, dichiarare
   la tensione nel campo `note`, non nasconderla.

## 2. Le categorie di conversione

- **`direct`, a indicazione di fonte** (la più solida, cercare SEMPRE prima
  delle altre): il testo 2e nomina o descrive l'equivalente 5e. Traag (la
  fonte cita la reach → lancia), Ogre di Krynn ("physically resemble the
  ogres of other worlds" → adozione diretta dell'Ogre SRD), Horax (il
  freddo "ha l'effetto di un incantesimo slow" → si copia *slow*),
  Shadowperson (l'ESP dichiarato di 2° livello → *detect thoughts*).
- **`direct`, per scelta nostra**: il 5e ha già un idioma adatto ma la fonte
  non lo nomina con quelle parole (es. "colpibile solo da armi magiche" →
  resistenza alle armi non magiche).
- **`adapted`, per analogia SRD singola**: un solo mostro SRD basta.
  Thanoi ≈ Merrow.
- **`adapted`, per analogia composta**: nessun mostro SRD singolo replica il
  profilo, si compone da più di uno. Kyrie = Giant Eagle (volo, CA) +
  Druid (PF, incantesimi minori).
- **Identità dichiarata dalla fonte**: quando il testo dice esplicitamente
  che la creatura è fisicamente uguale a una creatura standard, si adotta
  l'SRD di peso — non è pigrizia, è la conversione fedele. Ma cercare OGNI
  divergenza che la fonte dichiara e applicarla anche se scomoda (l'Ogre di
  Krynn non ha armi da tiro, perché la fonte dice che le evitano per
  cultura).

## 3. Regole ferme

- **L'unità di lavoro è la VOCE, non la creatura.** Una voce letta per
  intero — immagine di pagina, tutti gli statblock, verifica dei nomi — va
  convertita per intero nello stesso giro: tornarci dopo un `/clear`
  significa rileggerla da capo, e le varianti si gradano meglio a
  confronto diretto (il Centauro è venuto bene perché le quattro culture
  sono state graduate insieme). Tetto: oltre quattro creature per voce, ci
  si ferma a quattro e si lascia il resto in coda; voce singola, se ne
  prendono due come prima. Precedente: Avian, convertita in due giri prima
  della regola (Emre/Kingfisher) e dopo (Skyfisher/'Wari) — la differenza
  di costo fra i due giri è il motivo del cambio.
- **Il nome della voce è un contenitore editoriale del manuale, non una
  creatura.** Quando nessuna variante lo porta come proprio, tutte vanno
  registrate in `variante_di` e **nessuna** viene promossa arbitrariamente a
  "principale" solo per riempire il campo. Precedente: Centaur (of Krynn),
  quattro culture (Abanasiniano, Crystalmir, Endscape, Wendle), nessuna
  chiamata come la voce — stesso schema di Man (of Krynn), già nello schema
  prima del Centauro.

- Una capacità che la fonte **dichiara** ma senza resa 5e evidente va
  `pending`, **mai omessa in silenzio** — vale per incantesimi, tratti e
  varianti/sottospecie.
- **I Dadi Vita non bastano a classificare una voce, e nemmeno i PE da
  soli**: leggere lo statblock per intero prima di assegnare fascia o GS.
  Quando DV e XP divergono dalla fascia presunta, è il segnale che impone
  la lettura completa, non il verdetto.
- Prima di leggere una voce, cercare **"See below"** e le sue forme
  equivalenti (`Special`, `Varies`/`Variable`, `As creature or person
  mimicked`, o una clausola di `SPECIAL ATTACKS/DEFENSES` senza numero
  proprio) su tutti i campi di combattimento — non su `TREASURE`/
  `NO. APPEARING`, che restano dati di mondo. Se presente, la lettura
  completa non è opzionale.
- **Resistenza magica**: si registra in `magic_resistance_2e` con
  `applied: false` (decisione 27, gruppo C — rinviata alla Fase 2), mai
  applicata alla scheda.
- **Il riscontro 3.5** (`riscontro/3.5/`) è un indice, non una fonte: dice
  DOVE guardare per verificare una lettura già fatta sul 2e, non fornisce
  contenuto. Si consulta DOPO aver letto il 2e per intero, mai per copiarne
  la meccanica (spesso è più morbido del 2e).
- **Creatura contro entità** (decisione 32): nome proprio e storia propria →
  entità, fuori dal bestiario. Tipo/procedura ripetibile, anche se potente o
  legato a un oggetto magico → creatura, si converte come le altre.
  "Legato a un oggetto" non equivale a "unico".
- **La media fra grado difensivo e grado offensivo non è un compromesso, è
  la regola.** In 5e il Grado di Sfida è per definizione la media fra i due
  assi (DMG): un mostro con difesa 1/8 e offesa 1 dà GS 1/2 perché così si
  calcola, non perché ci si "incontra a metà strada". Non giustificare ogni
  divergenza fra difesa e offesa come tensione da annotare — è normale,
  quasi sempre lo è. La tensione vera, quella da scrivere in `note`, è solo
  quando il risultato non torna nemmeno facendo la media (Kapak: salto
  offensivo ×9.6 sulla fonte, non assorbibile da nessuna media).
- **I comportamenti di gruppo vanno al generatore di incontri, non persi.**
  Un'azione che la creatura fa solo in stormo/branco (es. il Calpestio del
  'Wari) va esclusa dal calcolo del GS del singolo — è corretto — ma
  registrata con destinazione `generatore_incontri`, stesso trattamento del
  morale (decisione 27, gruppo B). Un buco silenzioso qui è come un buco
  silenzioso su una capacità individuale: la regola ferma sulle capacità
  dichiarate (sopra) vale anche per i comportamenti collettivi.

### 3.1 Blocchi da filtro sull'output

**Procedura pratica — vale a prescindere dalla causa, che non è nota.**

- Il campo `raw` (e qualunque altro campo) può essere **omesso (null)** se un
  filtro automatico ne blocca la scrittura: si aggiunge una nota con voce e
  pagina per la riverifica, non si riformula per aggirare il filtro. Se il
  blocco si presenta su un campo diverso da `raw`, stessa regola: si scrive il
  valore convertito, si omette solo la trascrizione letterale, e si segnala
  quale campo e perché — non è un motivo per fermarsi, salvo che il blocco
  impedisca la scrittura della scheda anche senza quel campo.
- **Se il blocco si ripresenta a prescindere dal campo**, la voce si segna
  `bloccato` in coda invece di `da_fare`, con nota che dice che è un filtro
  sull'output e non un limite del metodo, che la voce è leggibile e analizzata
  ma non scrivibile in scheda, e **si passa alla voce successiva** — non si
  spezza la scrittura in parti più piccole né si riformula il contenuto per
  aggirarlo. Precedente: Haunt, Knight (Cavaliere Spettrale), bloccata così
  dopo Cavaliere della Morte nello stesso giro.
- **Quando si registra un blocco, registrare anche la FASE del turno in cui è
  arrivato**, non solo la voce: è l'unico dato che stiamo accumulando e che
  potrebbe un giorno distinguere fra le spiegazioni aperte (sotto).

Questa è una procedura di comportamento — funziona perché fa proseguire il
lavoro, non perché discenda da un meccanismo compreso. Nessuna delle righe
qui sopra presuppone di sapere cosa faccia scattare il filtro.

**Cosa è OSSERVATO.** Quattro volte il turno si è interrotto con un errore di
filtro sull'output. Il messaggio ("Output blocked by content filtering policy")
viene dal sistema, non è una nostra lettura. Il dato disponibile è questo:
l'errore, e il momento in cui è arrivato. Cosa lo abbia fatto scattare non è
visibile.

| # | occasione | fase del turno | contenuto in lavorazione |
|---|---|---|---|
| 1 | Haunt, Knight | in SCRITTURA, dopo lettura e analisi complete | non morto vincolato (Cavaliere Spettrale) |
| 2 | Wyndlass | in LETTURA/ANALISI, prima ancora di poter scrivere | non morto con molti tentacoli |
| 3 | Erba Scintillante (Shimmerweed) | a FINE TURNO, scheda già scritta e valida (172 righe, 0 errori schema), durante il riepilogo | pianta immobile, 1 pf, nessuna violenza |
| 4 | giro dei commit (21/08/2026) | a FINE TURNO, durante il riepilogo | operazioni git, nessun contenuto di manuale |

Due dei quattro (3 e 4) sono arrivati a turno praticamente concluso, con il
lavoro già fatto e salvato: il blocco ha colpito il riepilogo, non la
conversione.

**Cosa è IPOTIZZATO, non verificato.** Che la causa sia il contenuto della
creatura. È la lettura che veniva naturale dopo i primi due casi — entrambi
non morti minacciosi — ma i casi 3 e 4 la contraddicono: una pianta inerte e
una sequenza di comandi git non hanno nulla di plausibilmente problematico.

Restano aperte almeno tre spiegazioni, **nessuna testata**:

1. il modello in uso al momento del blocco;
2. la lunghezza o il carico della sessione — il giro dell'Erba Scintillante
   aveva già in contesto due letture integrali di file lunghi (questo metodo,
   la coda), due immagini di pagina, la ricerca di calibrazione per la voce
   successiva e una scheda da 172 righe;
3. la fase di fine turno in sé, cioè la produzione del riepilogo, dove due dei
   quattro blocchi sono arrivati.

Non c'è una prova che isoli nessuna delle tre, e non se ne può escludere una
quarta. Se fosse la (2), il rimedio sarebbe un `/clear` più frequente fra una
voce e l'altra — ma va inviato dall'utente, non è un'azione che il modello può
compiere su se stesso a metà turno. Indizio, non regola: da riverificare a
ogni nuovo caso.

**Primo giro con una variabile isolata di proposito (21/08/2026).** Il giro
Hatori + Ragno Botola è stato condotto su un modello diverso (Opus invece di
Sonnet), tenendo tutto il resto uguale: stesso metodo, stessa coda, due voci
in un giro, due immagini di pagina, due schede lunghe, riepilogo finale.
**Nessun blocco, in nessuna fase** — lettura, analisi, scrittura, validazione,
commit, riepilogo. Va scritto per quello che è: un turno pulito su una prova
sola. Non conferma l'ipotesi (1) — la maggior parte dei giri su Sonnet erano
anch'essi puliti, quindi un singolo esito pulito non discrimina fra le
spiegazioni — ma è la prima volta che una delle tre variabili viene mossa
deliberatamente invece di essere osservata a posteriori, ed è così che la
lista sopra potrà un giorno accorciarsi. Il valore sta nel disegno del test,
non nel risultato di questa esecuzione.

**Ipotesi caduta — la "categoria dei non morti".** Un giro precedente aveva
scritto qui che il filtro reagiva ai non morti con vincoli magici. Non regge:
i casi 3 e 4 non sono creature, e il Dreamwraith — non morto vincolato — ha
`raw` compilato (629 caratteri) e passato senza problemi, come il Fetch e lo
Scheletro Guerriero che ce l'hanno a null e sono passati comunque. Non usare
la materia della voce per prevedere dove il filtro scatterà.

**Precauzione, non previsione.** Sui non morti con vincoli magici (Scheletro
Guerriero, Cavaliere della Morte, Wichtlin) il campo `raw` si omette per
default fin dall'inizio. Il motivo che regge questa scelta **non** è l'ipotesi
caduta sopra, ma che la trascrizione integrale non serve comunque —
`abilities_text` porta già la meccanica — e tentarla costa un giro se si
blocca. È una scorciatoia a costo zero: se un giorno il `raw` di un non morto
passasse liscio, non ci sarebbe nulla da spiegare.

**Diagnostica sui campi di trascrizione**: non stampare mai a schermo il
contenuto di `raw` (o di campi analoghi) per controllare se sono popolati. Per
verificare se un campo è compilato, stampare un booleano o la sua lunghezza,
mai il testo. La ragione solida è che quel testo occupa contesto per tutta la
sessione senza motivo; che possa anche far scattare il filtro è solo una
cautela in più, coerente con quanto poco ne sappiamo.

## 4. La procedura, passo per passo

Praticata su undici conversioni (`dati/mostri/`); questi sono i passi, non
una checklist burocratica.

1. Estrarre il blocco `CLIMATE/TERRAIN`…`XP VALUE` per intero, non solo
   l'intestazione o il nome della voce.
2. Cercare "See below" e le sue forme equivalenti (regola ferma, sopra); se
   presenti, leggere subito la prosa collegata (`Combat`/`Habitat & Society`
   /`Ecology`).
3. Confrontare DV e XP con la fascia presunta; se divergono, rileggere
   prima di fissarla.
4. Verificare creatura contro entità.
5. Cercare un'indicazione di fonte esplicita (categoria 2 sopra) prima di
   cercare un analogo SRD per conto nostro.
6. Se serve un analogo, sceglierlo per **ruolo**, poi verificare che il
   ruolo 2e coincida col ruolo 5e prima di fidarsi dell'ordinamento CA/PE
   (vincolo 1).
7. Assegnare CA/PF dall'analogo o dalla mediana SRD del GS presunto; danno
   per round almeno raddoppiato (vincolo 3).
8. Se la fonte dichiara un effetto alla morte o identitario, riscriverlo con
   un TS (vincolo 2) — mai se la fonte dichiara l'assenza dell'effetto.
9. Registrare ogni capacità dichiarata con uno stato di conversione: mai un
   buco silenzioso.
10. **Controllo incrociato via XP2e.** Con il GS appena assegnato, confrontare
    l'XP2e della voce con la tabella in §6: cercare le creature già
    convertite con XP2e vicino e verificare che il loro GS sia nello stesso
    ordine di grandezza. Non è un ricalcolo — il GS resta quello derivato
    dalla media difesa/offesa (vincolo fermo, sopra) — ma una divergenza
    forte (XP2e vicino a creature di GS molto diverso) è un motivo per
    rileggere lo statblock prima di chiudere la scheda, non un errore
    automatico da correggere alla cieca. Aggiungere la nuova coppia
    (XP2e, GS) alla tabella una volta chiusa la scheda.
11. Compilare `morale_2e` (destinazione `ia_combattimento`) e
    `world_data_2e` (destinazione `generatore_incontri`) dai gruppi A/B
    della decisione 27.
12. Validare contro `dati/schema/mostro.schema.json`, poi rigenerare
    `dati/mostri.index.json` con `python3 dati/build_mostri_index.py`
    (derivato dal contenuto di `dati/mostri/`, non tenuto a mano).

## 5. Le categorie aperte

Tre tipi di voce che questo metodo non copriva, perché presuppongono uno
statblock fisso da convertire una volta sola. **Al 25/08/2026 ne resta aperto
uno**: le altre due sono chiuse dalle decisioni 34-36, e restano scritte qui
sotto perché la forma va riconosciuta anche dopo che il problema è risolto —
la prossima voce che la porta va inquadrata subito, non riscoperta.

### 5.1 Creature-modello — APERTA

Dreamshadow, Spectral Minion. Ogni campo della scheda 2e è dichiarato "as
creature or person mimicked" o "quelli della vita precedente": non hanno
statistiche proprie, le ereditano da un bersaglio. Serve un pacchetto di
regole che copia un bersaglio, non un singolo statblock — la conversione è di
un **meccanismo**, non di un valore. Restano `pending` di metodo, non solo di
contenuto, finché non si decide la forma di schema che le copre.

È l'unica delle tre che non si risolve con un filtro: lì la fonte dà un
vincolo e tace sul campione (§5.3), qui non c'è nemmeno il vincolo, perché il
campione è un'altra creatura scelta a runtime.

### 5.2 Famiglie di statblock — RISOLTA (decisioni 34 e 36, 25/08/2026)

Tylor, e con lui Dragon Amphi e Dragon Sea. La fonte non dà uno statblock ma
una **tabella di categorie d'età** con DV, CA e capacità propri per riga, sul
modello degli age category dei draghi. Il Tylor ne ha **otto**; Amphi e Sea
**dodici ciascuno**. Convertirle tutte avrebbe voluto dire 32 schede per tre
creature, quasi tutte inutilizzabili in arena.

**Quante se ne convertono.** Solo le righe dentro la finestra dell'arena,
indicativamente GS 1/4-4. Sul Tylor sono **due su otto**: la 3ª (Young → Tylor
Giovane, GS 2) e la 4ª (Juvenile → Tylor Adolescente, GS 3). Le due schede si
scrivono **nello stesso giro**, per la stessa ragione per cui le quattro
culture di Centauro sono venute bene: le varianti si gradano meglio a
confronto diretto.

**Come si sceglie il taglio.** Due confini, e nessuno dei due è a piacere.

- *In alto lo indica la fonte.* Si cerca un salto nei suoi stessi numeri. Sul
  Tylor l'XP passa da 975 alla 4ª categoria a 9.000 alla 5ª: fattore nove in
  un solo gradino. Il confine è quello, non un GS scelto da noi.
- *In basso lo decide ciò che la tabella tiene FISSO.* Sul Tylor il danno
  (1-10 coda / 1-20 morso) è identico su tutte e otto le categorie, cioè
  descrive l'adulto: fissare la scheda sulla 1ª avrebbe dato un cucciolo da
  1d6 punti ferita che morde per 1d20. È **esattamente la regola già ricavata
  sull'Hatori** (§5.4, criterio *b*), applicata qui a una famiglia invece che
  a una banda di Dadi Vita. È un argomento **osservato nella tabella**, non
  inferito: la colonna del danno è lì e non varia.

**Dove finisce il resto** (decisione 36): nel campo
`source_2e.age_categories` di `mostro.schema.json`, tabellare e
interrogabile, **non** riscritto in prosa dentro `abilities_text` — dodici
righe per dodici colonne in prosa sono illeggibili e perdono la struttura. Il
campo dichiara le colonne che *quella* voce usa (il Tylor non ha soffio, i
draghi sì) e marca `inferita: true` le colonne di cui trascriviamo i numeri ma
interpretiamo il significato — sul Tylor è `Hit Die Modifier`, che la fonte
stampa senza dire se valga per Dado Vita o sul totale. Ogni scheda derivata
porta la tabella **intera**, non solo la propria riga: la riga da sola non
direbbe dove la creatura sta nella progressione. Destinazione delle righe non
convertite: `generatore_incontri`, stesso trattamento dei dati di mondo del
gruppo A della decisione 27.

### 5.3 Incantatore a scelta del master — RISOLTA (decisione 35, 25/08/2026)

Tayling, e con lui il repertorio del Tylor e la metà accoppiata del Dragon
Astral. Il corpo ha uno statblock fisso, ma il repertorio di incantesimi non è
statuito: "Taylings can cast spells either as wizards or priests varying in
levels from 1-10", scelta rimandata a chi conduce la partita.

**La lettura che ha sbloccato il caso: la fonte non tace, dà il FILTRO e non
il campione.** Il Tayling fissa scuola (Alterazione) e sfera (Elementale) con
banda di livello 1-10; il Tylor fissa i conteggi di slot e il carattere
offensivo; il Dragon Astral fissa classe e livello. Sono specifiche precise a
cui manca solo l'estrazione.

Quindi **si modella come specifica di filtro, non come lista**: si registra
l'insieme accessibile secondo i vincoli della fonte, e la scelta concreta
avviene alla generazione dell'incontro. Non è invenzione di meccanica (vincolo
2 salvo): l'insieme è quello che la fonte delimita. **Conseguenza operativa: il
repertorio non resta `pending` e non è escluso dal calcolo del GS.** Entra come
capacità con insieme definito, e il GS che ne esce è chiuso, non provvisorio.

La macchina esisteva già e non è stata costruita per l'occasione: le sfere come
filtro di preparazione sono la decisione 24, implementate in
`dati/_sfere_5e.py`; la scuola è un campo indicizzato dei 319 incantesimi SRD
in `dati/incantesimi.index.json`. Vale la pena dire perché questo è più facile
nel nostro bersaglio che a tavolo: la 5e cartacea deve stampare una lista
fissa, un motore software pesca dall'insieme filtrato ogni volta.

Stessa forma per i **parametri non magici** lasciati aperti dalla fonte: la
resistenza elementare del Tylor (una sola, la fonte dichiara che non se ne
cumulano due ma non dice quale) è un parametro risolto alla generazione, non
una moltiplicazione di schede — cinque tylor identici con una riga diversa
sarebbero stati cinque file da mantenere.

**Cosa ha rivelato il filtro una volta applicato, che il `pending` nascondeva.**
Il GS del Tayling era 1/2 provvisorio, con la nota che prevedeva una salita a
GS 3-4 una volta fissato un repertorio (l'XP2e 2.000 lo accosta a Sivak, Skrit
e Spettro Onirico, tutti GS 4). Calcolato invece che presunto, **il GS resta
1/2**: la scuola di Alterazione e la sfera Elementale, filtrate sull'SRD,
selezionano utilità, movimento e controllo — non danno. La previsione era
sbagliata, e solo modellare il filtro poteva dirlo. È il caso che giustifica la
decisione 35 meglio di qualunque argomento di forma: un `pending` non è neutro,
è una stima nascosta.

### 5.4 Cosa NON è una categoria aperta: lo statblock a Dadi Vita variabili

L'Hatori Minore assomiglia a una famiglia di statblock e non lo è, e la
distinzione va tenuta ferma perché la prossima voce di questa forma non
finisca per sbaglio nella lista sopra. La colonna Lesser tiene **fissi** CA,
movimento, numero di attacchi e danno su tutta la banda, e fa variare solo i
Dadi Vita (1-5) — con THAC0 e XP che ne discendono e che infatti la fonte non
stampa (`Varies`, `Variable`). Il Tylor è un'altra cosa: lì ogni categoria
d'età ha CA e capacità **diverse**, cioè servono davvero più statblock. Qui
lo statblock è uno solo e a variare è la sola quantità di punti ferita.

La regola operativa che ne esce: **si fissa la scheda su un taglio della
banda e si registra il resto della banda come tratto**, mai lasciando
implicito quale taglio si sia scelto. Il taglio si prende, in quest'ordine:
(a) un punto che la **fonte stessa nomini** — sull'Hatori è il 5 DV, l'unico
citato nel testo (la soglia a cui i piccoli lasciano la madre) e per di più
confine con la colonna successiva; (b) in mancanza, il taglio **coerente
con le capacità fisse**, perché un danno fisso su tutta la banda descrive
l'esemplare adulto e non il cucciolo — fissare l'Hatori a 1 DV avrebbe dato
un mostro da sette punti ferita che morde per 3d6. Un punto intermedio scelto
da noi è l'ultima risorsa, non la prima. Gli altri tagli non si buttano: sul
`hatori-minore.json` stanno nel tratto "Crescita continua", con dadi e taglia
derivati con lo stesso metodo del taglio principale.

**Il criterio (b) ha retto fuori dal caso che l'ha prodotto**, ed è la ragione
per cui vale la pena averlo scritto: sul Tylor decide il confine basso della
finestra (§5.2), su una tabella di categorie invece che su una banda di Dadi
Vita. Stessa osservazione — un valore che la fonte tiene fisso descrive
l'adulto — applicata a una forma diversa.

### 5.5 Stato al 25/08/2026

Coda ordinaria esaurita per intero dal 21/08/2026 (fascia 4 chiusa con Hatori
Minore e Ragno Botola Gigante). Restano: **una** categoria aperta (§5.1, le
due creature-modello), i due blocchi da filtro sull'output (Haunt Knight,
Wyndlass — §3.1) e il contenuto di `fuori_fascia`.

`dati/mostri.coda.json` tiene l'indice in **due** blocchi, `categorie_aperte`
e `categorie_risolte`, e `verifica_coda.py` controlla che i tre luoghi che
descrivono la stessa cosa — lo `stato` per-voce, l'indice, e il testo di
questa sezione — non si sfasino: aperta → `stato: "categoria_aperta"`,
risolta → `stato: "fatto"`, nessun nome in entrambi i blocchi. Il controllo
esiste perché lo sfasamento è già successo (Spectral Minion, 21/08/2026:
elencato come creatura-modello nell'indice e in questa sezione, ma `da_fare`
nella propria fascia).

## 6. Osservazioni XP2e → GS

Indizio, non regola: cinque voci indipendenti e molto diverse fra loro —
Orso Glaciale, Phaethon Anziano, Disir, Servitore di Fuoco, Imp del Mare di
Sangue — condividono lo stesso XP2e (975) e sono tutte GS 3; altre tre — Draconico Sivak, Skrit,
Spettro Onirico — condividono XP2e (2.000) e GS 4, pur avendo profili di
danno per round molto diversi sulla carta (per lo Skrit è l'Enzima
Paralizzante a giustificare il salto, per lo Spettro Onirico la precisione
e l'effetto Terrore Onirico, non le armi). Il caso piu' istruttivo finora è
il Servitore di Fuoco: la fonte lo dichiara esplicitamente un elementale del
fuoco, il che avrebbe suggerito di adottarne di peso l'analogo SRD (GS 5) —
ma l'XP2e lo colloca chiaramente nel gruppo GS 3, ed è lì che è rimasto dopo
la rilettura. Non basta a fare una regola (sette osservazioni su due valori
soli), ma è coerente abbastanza da tenere una tabella e guardarla ogni volta
(passo 10 della procedura, sopra): se dopo una decina di voci il rapporto
tiene, l'XP2e diventa un secondo controllo indipendente dal calcolo
difesa/offesa; se non tiene, qui resta comunque la cronologia di perché si
è pensato che potesse tenere.

| XP2e | GS | Creatura |
|-----:|:--:|----------|
| — | 0 | Anziano Venerato |
| — | 1/2 | Sciame di Cavallette e Locuste |
| — | 1 | Sciame di Formiche di Velluto |
| — | 1/4 | 'Wari |
| 35 | 1/8 | Bambola Kani |
| 35 | 0 | Kingfisher |
| 65 | 1/4 | Cervo Selvatico |
| 65 | 1/4 | Gurik Cha'ahl |
| 120 | 2 | Centauro Abanasiniano |
| 120 | 1/2 | Centauro di Crystalmir |
| 120 | 2 | Centauro di Endscape |
| 120 | 1 | Centauro Wendle |
| 120 | 1/8 | Emre |
| 120 | 2 | Thanoi |
| 120 | 1/4 | Traag |
| 175 | 1/2 | Bakali |
| 175 | 1 | Cervo Gigante |
| 175 | 1/2 | Draconico Baaz |
| 175 | 2 | Ogre di Krynn |
| 175 | 1 | Orughi |
| 175 | 2 | Ombrolo (Shadowperson) |
| 270 | 1 | Horax |
| 270 | 1 | Jarak-Sinn |
| 270 | 1 | Phaethon |
| 270 | 1/2 | Skyfisher |
| 270 | 1 | Kalothagh |
| 420 | 2 | Ragno Botola Gigante |
| 650 | 3 | Draconico Kapak |
| 650 | 1 | Occhialato (Eyewing) |
| 650 | 2 | Tylor Giovane (3ª categoria) |
| 975 | 3 | Orso Glaciale |
| 975 | 3 | Phaethon Anziano |
| 975 | 3 | Disir |
| 975 | 3 | Servitore di Fuoco (Fire Minion) |
| 975 | 3 | Imp del Mare di Sangue |
| 975 | 3 | Tylor Adolescente (4ª categoria) |
| 1.400 | 2 | Draconico Bozak |
| 1.400 | 1 | Kyrie |
| 1.400 | 3 | Taylang |
| 1.400 | 3 | Wichtlin |
| 2.000 | 4 | Draconico Sivak |
| 2.000 | 4 | Skrit |
| 2.000 | 4 | Spettro Onirico (Dreamwraith) |
| 2.000 | 1/2* | Tayling |
| 3.000 | 6 | Fetch |
| 4.000 | 7 | Scheletro Guerriero |
| 4.000 | 7 | Yaggol |
| 5.000 | 8 | Cavaliere della Morte |
| 6.000 | 6 | Draconico Aurak |
| — | 5 | Hatori Minore |

\* Il GS 1/2 del Tayling **era** provvisorio e ora è chiuso (decisione 35,
25/08/2026): il repertorio non è più `pending` ed è entrato nel calcolo. La
riga non è cambiata — è la previsione che c'era scritta qui a essere stata
smentita. Diceva che il Tayling completo sarebbe salito in linea con le altre
voci a XP2e 2.000, tutte GS 4; applicando davvero il filtro della fonte
(scuola di Alterazione, sfera Elementale) sui 319 incantesimi SRD, l'insieme
accessibile risulta di utilità, movimento e controllo, senza artiglieria: il
GS resta 1/2. **L'asterisco resta perciò la riga più istruttiva della
tabella**, ma per il motivo opposto a quello per cui era stato messo — lo
scarto fra XP2e 2.000 e GS 1/2 è reale e permanente, non un segnaposto in
attesa di chiudersi. La formula degli XP della 2e prezzava "incantatore fino
al 10° livello" senza guardare quali incantesimi la stessa fonte gli
concedesse. La lezione che se ne ricava è registrata in fondo a questa
sezione, **"Il quarto esito"**: una divergenza può essere reale e permanente,
e allora misura il limite del controllo, non un lavoro da finire.

Nota di lettura: la dispersione a bassa XP (120→GS che va da 1/8 a 2, 175→GS
da 1/2 a 2) mostra che il rapporto non è affatto lineare nella fascia bassa,
dove il rumore editoriale sui piccoli mostri pesa di più. Il pattern più
netto è invece ai due estremi alti già osservati (975→3, 2.000→4): con
XP2e più alto la fonte sembra aver già fatto, a modo suo, la stessa media
difesa/offesa che la 5e formalizza. Yaggol e Scheletro Guerriero rafforzano
il pattern con una prima corrispondenza esatta derivata in modo indipendente
sullo stesso XP2e (4.000→GS7 per entrambi, non dedotta l'una dall'altra):
insieme alle quattro voci già convergenti su 975→GS3, sono cinque
corrispondenze su due valori distinti. Il Cavaliere della Morte (5.000→GS8)
chiude la revisione aperta in un giro precedente: il confronto con Lord Soth
ha portato ad abbassare la CA e a riscrivere l'incantesimo letale con una
salvezza, non a spostare il GS — la riga in tabella non cambia.

Il Taylang (1.400→GS3) è invece la prima voce dove il segnale punta nella
direzione OPPOSTA al profilo letto per intero: la stessa fascia di XP2e che
dà GS1-2 per Draconico Bozak e Kyrie non regge per lui — profilo martiale
nudo, tre attacchi per ~34 danni/round, THAC0 basso. Registrata con la
stessa evidenza delle convergenze: la smentita è un indizio quanto la
conferma, non un errore da correggere alla cieca (regola 10 della
procedura). Non invalida le corrispondenze già osservate agli estremi alti,
ma ne fissa il limite: il segnale è affidabile quando DV e XP non divergono
dalla fascia presunta (regola ferma, §3); sul Taylang divergono (HD8 alto
contro XP1.400 medio-basso), ed è esattamente lì che smette di esserlo.

Non è ancora una regola, ma non è più coincidenza: da riguardare quando le
corrispondenze arriveranno a una decina, per capire se ne emerge una
tabella di conversione utilizzabile prima ancora di leggere lo statblock.
Da riverificare quando la fascia 3 sarà più popolata.

Il Wichtlin (1.400→GS3) raggiunge il Taylang sullo stesso XP2e, ma per una
via opposta: non un profilo martiale nudo, bensì un pacchetto difensivo e
di controllo (resistenza alle armi non magiche, blocco quasi garantito con
paralisi 2d4 round, immunità multiple) che pesa più del danno grezzo
(~5/round dal solo veleno). Due voci indipendenti sullo stesso XP2e,
entrambe spinte a GS3 da un asse diverso da quello atteso — martiale una,
difensivo/controllo l'altra.

**Il limite del segnale, ora scritto esplicitamente**: XP2e↔GS regge come
ORDINE DI GRANDEZZA (predice la fascia di GS con un margine ragionevole), ma
non dice NULLA su come la creatura ci arriva — offesa nuda (Taylang) e
difesa/controllo (Wichtlin) producono la stessa lettura di tabella pur
essendo profili opposti in ogni altro senso. Il segnale conferma solo il
"quanto", mai il "come": la lettura completa dello statblock resta
obbligatoria per il "come" a prescindere da quanto la tabella torni pulita
(regola ferma, §3). Non è una scoperta che indebolisce la tabella — è la
sua natura, ora osservata due volte invece di presunta una.

Imp del Mare di Sangue (975→GS3) e Kalothagh (270→GS1), convertiti nello
stesso giro, mostrano i due lati della stessa medaglia. L'Imp ripete lo
schema Wichtlin: nessun profilo martiale (un solo tocco, 1d6), ma un
pacchetto difensivo pesante (resistenza alle armi non magiche, immunità
multiple, forma di nebbia quasi invulnerabile) che lo tiene a GS3 nonostante
l'offesa debole — sesta corrispondenza sui due valori alti della tabella. Il
Kalothagh invece è il primo caso di questo giro in cui il segnale funziona
SENZA una spiegazione nascosta da scoprire: nessuna resistenza magica
(dichiarata "Nil"), nessuna resistenza alle armi, complessità di
controllo/superficie tattica (quattro meccaniche distinte) ma non di
potenza — il GS1 di XP2e270 regge per il motivo più semplice possibile, la
voce non è più forte di quanto sembri. Utile da avere entrambi nello stesso
giro: il segnale non nasconde sempre qualcosa, a volte è solo corretto.

**Cosa significa per l'uso del segnale (passo 10 della procedura)**: fino al
Kalothagh, ogni voce dove si è guardata la tabella aveva poi rivelato
qualcosa — lo Skrit (l'Enzima Paralizzante dietro il salto a GS4), il
Taylang (il profilo martiale dietro la divergenza), il Wichtlin e l'Imp (il
pacchetto difensivo dietro l'offesa debole). Sarebbe stato facile leggerne
la regola sbagliata: che consultare la tabella significa aspettarsi una
sorpresa. Il Kalothagh smentisce quella lettura — controllato, non ha
rivelato nulla, il GS ovvio era quello giusto. Il segnale resta quindi
esattamente quello che il passo 10 dice fin dall'inizio: un INVITO A
CONTROLLARE, mai un annuncio che c'è un problema nascosto da trovare a ogni
costo. Sapere che a volte non c'è nulla sotto è parte della sua definizione
quanto sapere che a volte c'è: il controllo è dovuto sempre, la scoperta no.

**Le due categorie del Tylor, convertite lo stesso giorno, danno una conferma
e un caso limite.** L'Adolescente (975 → GS 3) è la **sesta** corrispondenza
sul valore più solido della tabella, e vale più delle precedenti per come è
arrivata: il GS era già 3 dal calcolo difesa/offesa prima che si guardasse la
tabella, quindi il passo 10 ha confermato senza influenzare. Il Giovane (650 →
GS 2) cade invece sul valore più ambiguo che la tabella abbia: 650 porta già
Draconico Kapak a GS 3 e Occhialato a GS 1, e il nuovo GS 2 si infila
esattamente fra i due. Non è una smentita e non è una conferma — è la misura
di quanto largo sia il margine a quel valore, che è l'informazione utile.
Utile anche perché le due righe vengono dalla **stessa creatura**: due
categorie d'età della stessa voce, con lo stesso danno e lo stesso ruolo,
separate da un gradino di GS e da 325 punti esperienza di fonte. Fin qui la
tabella aveva confrontato creature diverse fra loro; qui confronta una
creatura con se stessa, ed è il caso in cui il rumore editoriale ha meno
spazio per entrare.

**Il terzo esito: il segnale può mancare del tutto.** L'Hatori Minore è la
prima riga con `—` in colonna XP2e non perché il valore sia ignoto a noi, ma
perché la fonte *rifiuta di stamparlo*: `XP VALUE: Variable`, con rimando
alle Tabelle 31-32 del DMG 2e, perché dipende dai Dadi Vita del singolo
esemplare — stessa ragione di `THAC0: Varies` sulla stessa riga. Il passo 10
non aveva materiale su cui girare. Fin qui la casistica aveva due esiti (il
segnale conferma, come sul Kalothagh; oppure diverge e rivela qualcosa, come
su Taylang e Wichtlin): conviene scrivere il terzo prima che qualcuno lo
scambi per una dimenticanza. **Assenza non è divergenza** — non chiede una
spiegazione e non è un motivo per rileggere lo statblock. Le altre righe `—`
della tabella sono cosa diversa: lì l'XP2e semplicemente non è stato
riportato in scheda, qui è la fonte a dichiarare che un numero unico non
esiste.

**Il quarto esito: la divergenza può essere REALE E PERMANENTE.** Il Tayling
(2.000 → GS 1/2) è lo scarto più largo della tabella — quattro gradini sotto
le altre tre voci con lo stesso XP2e, tutte GS 4 — e **non è un segnale da
indagare: è già stato indagato**. Il repertorio non è più `pending`, è stato
calcolato applicando davvero il filtro della fonte (§5.3), e il risultato è
che il filtro stesso — scuola di Alterazione, sfera Elementale — seleziona
utilità, movimento e controllo, non danno. Sotto non c'è niente da trovare: i
due numeri misurano cose diverse. L'XP2e prezza la pericolosità complessiva
secondo la 2e, che pesava il controllo tattico molto più di quanto faccia il
calcolo del grado in 5e, e prezzava "incantatore fino al 10° livello" come
categoria senza guardare quali incantesimi la stessa fonte gli concedesse.

**Cosa lo distingue dal secondo esito**, ed è il punto per cui vale la pena
scriverlo a parte: su Taylang, Wichtlin e Imp la divergenza si è *chiusa* — la
lettura completa ha trovato l'asse che la spiegava (martiale, difensivo,
difensivo) e i due numeri sono tornati a dire la stessa cosa per vie diverse.
Qui la lettura completa è stata fatta e la divergenza **è rimasta**. È la
differenza fra un segnale che nasconde qualcosa e un segnale che sta misurando
un'altra grandezza.

**Conseguenza operativa sul passo 10**: quando una divergenza sopravvive alla
lettura completa si registra come definitiva e **non riapre la scheda**.
L'asterisco in tabella non è un promemoria di lavoro da finire — è il limite
del controllo XP2e↔GS, scritto dove si guarda la tabella invece che in una
nota di metodo che nessuno rilegge. Fin qui il passo 10 aveva sempre chiesto
qualcosa (controlla, e a volte correggi); questo è il primo caso in cui non
chiede di correggere nulla e serve solo a dire fin dove il segnale arriva.
