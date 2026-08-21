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
- Il campo `raw` (e qualunque altro campo) può essere **omesso (null)** se
  un filtro automatico ne blocca la scrittura: si aggiunge una nota con
  voce e pagina per la riverifica, non si riformula per aggirare il filtro.
  **Per i non morti con vincoli magici** (anime imprigionate, maledizioni,
  controllo/possesso — Scheletro Guerriero, Cavaliere della Morte, Wichtlin e
  Dreamwraith gia' convertiti cosi'; Spectral Minion resta in coda ma come
  categoria aperta, §5, non come voce ordinaria) il campo `raw` si omette **per
  default fin dall'inizio**, invece di tentarlo e ripiegare dopo: è la parte
  che si blocca più spesso su questa famiglia (due casi su due finora), e la
  trascrizione integrale non è comunque necessaria — `abilities_text` porta
  già la meccanica. Se il blocco si presenta su un campo diverso da `raw`,
  stessa regola: si scrive il valore convertito, si omette solo la
  trascrizione letterale, e si segnala quale campo e perché — non è un
  motivo per fermarsi, salvo che il blocco impedisca la scrittura della
  scheda anche senza quel campo (vedi sotto, voce `bloccato`).
  **Se il blocco si ripresenta a prescindere dal campo** (non è quindi un
  problema del campo `raw` ma della voce stessa in quel momento), la voce si
  segna `bloccato` in coda invece di `da_fare`, con nota che spiega che è un
  filtro sull'output e non un limite del metodo, che la voce è leggibile e
  analizzata ma non scrivibile in scheda, e si passa alla voce successiva —
  non si spezza la scrittura in parti più piccole né si riformula il
  contenuto per aggirarlo. Precedente: Haunt, Knight (Cavaliere Spettrale),
  bloccata così dopo Cavaliere della Morte nello stesso giro.
  **Diagnostica sui campi di trascrizione**: non stampare mai a schermo il
  contenuto di `raw` (o di campi analoghi) per controllare se sono popolati
  — un comando diagnostico che li stampa può da solo far scattare lo stesso
  filtro che si sta cercando di aggirare scrivendo la scheda. Per verificare
  se un campo è compilato, stampare un booleano o la sua lunghezza, mai il
  testo. Vale anche a prescindere dal filtro: quel testo occupa contesto
  per tutta la sessione senza motivo.
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

Tre tipi di voce che questo metodo non copre ancora, perché presuppongono
uno statblock fisso da convertire una volta sola:

- **Creature-modello** (Dreamshadow, Spectral Minion): ogni campo della
  scheda 2e è dichiarato "as creature or person mimicked" o "quelli della
  vita precedente" — non ha statistiche proprie, le eredita da un
  bersaglio. Serve un pacchetto di regole che copia un bersaglio, non un
  singolo statblock: la conversione è di un meccanismo, non di un valore.
- **Famiglie di statblock** (Tylor): la fonte dà una tabella di più
  categorie d'età con DV/CA/capacità diverse per ciascuna, sullo stesso
  modello degli age category dei draghi. Serve più di un GS: una mini-
  famiglia di statblock imparentati, non una conversione singola.
- **Incantatore a scelta del master** (Tayling): il corpo ha uno statblock
  fisso, ma il repertorio di incantesimi non è statuito dalla fonte —
  "Taylings can cast spells either as wizards or priests varying in levels
  from 1-10", scelta esplicitamente rimandata a chi conduce la partita. Non
  è una lacuna da colmare per analogia (vincolo 2: non si inventa
  meccanica 5e per riempire un vuoto che la fonte lascia deliberatamente
  aperto) e non è nemmeno una creatura-modello (le statistiche fisiche sono
  fisse, solo il repertorio magico è indeterminato) né una famiglia di
  statblock (non ci sono categorie discrete, è un intervallo di livello con
  scelta libera di scuola/sfera). Il GS assegnato in questi casi resta
  PROVVISORIO ed esclude la capacità dal calcolo, con nota esplicita (vedi
  `dati/mostri/tayling.json`, `mechanics_5e.challenge_rating.note`) —
  finché non si decide come rendere in scheda un repertorio non fissato:
  un pacchetto rappresentativo scelto da noi, una tabella di repertori
  precompilati, o un campo esplicitamente aperto lasciato al tavolo.
  Verificata la coda al 2026-08-21: nessun'altra voce condivideva questa
  forma (Wyndlass, Wichtlin, Imp Blood Sea, Kalothagh avevano tutte
  statblock e capacità fissate dalla fonte — le ultime tre convertite nei
  giri successivi con esito confermato, Wyndlass bloccata in lettura/analisi
  prima di poter verificare) — resta un caso isolato. Fascia 3 ordinaria
  esaurita al 21/08/2026: restano solo le tre categorie aperte (Dreamshadow,
  Spectral Minion, Tylor) e i due blocchi (Haunt Knight, Wyndlass).
  CORREZIONE: la coda aveva segnato Spectral Minion `da_fare` invece di
  `categoria_aperta` nonostante il metodo lo classificasse gia' qui come
  creatura-modello — allineata il 21/08/2026, `verifica_coda.py` ora
  controlla anche questo disallineamento (vedi commento nello script).

Tutte e tre restano `pending` di metodo, non solo di contenuto, finché non
si decide la forma dello schema che le copre.

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
| 650 | 3 | Draconico Kapak |
| 650 | 1 | Occhialato (Eyewing) |
| 975 | 3 | Orso Glaciale |
| 975 | 3 | Phaethon Anziano |
| 975 | 3 | Disir |
| 975 | 3 | Servitore di Fuoco (Fire Minion) |
| 975 | 3 | Imp del Mare di Sangue |
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

\* GS 1/2 del Tayling è PROVVISORIO, non chiuso come le altre righe: il
repertorio di incantesimi "a scelta del master" (§5, terza categoria
aperta) resta PENDING ed è escluso dal calcolo. Il GS del Tayling completo
salirà probabilmente in linea con le altre voci a XP2e 2.000 (tutte GS4)
una volta fissato un repertorio rappresentativo.

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
