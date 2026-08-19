# Progetto: Gioco Web D&D Dragonlance — Documento di Riferimento

*Documento vivo — da aggiornare man mano che si prendono nuove decisioni. Ultima revisione: 12 agosto 2026.*

---

## STATO ATTUALE (12 agosto 2026)

**Fase 0 quasi chiusa.** Libreria ri-estratta a colonne separate: 100 manuali su 140, 13.791 pagine, 61 milioni di caratteri in `Testi/`. Restano 22 scansioni in coda OCR, nessuna bloccante.

**Dati strutturati pronti e validati a zero errori**: 15 razze, 17 classi, 21 divinità in `dati/`, tutte da *Tales of the Lance* (AD&D 2e). Schema a doppio strato: `source_2e` fedele al manuale, `mechanics_5e` con le regole di validazione già applicate (vincoli di caratteristica e classi precluse) e i tratti 5e ancora da compilare.

**Materiale 5e arrivato**, ma solo in edizione **2024** (PHB, DMG, Monster Manual): il PHB 2014 scelto come riferimento non è fra i PDF. In compenso è disponibile `2014.5e.tools`, che espone tutto il materiale 2014 come **JSON strutturato** — metro di conversione migliore dei PDF. *Shadow of the Dragon Queen* resta assente.

**Prossimo passo**: compilare `mechanics_5e` (tratti, taglia, velocità) usando i dati 2014 come riferimento, poi lo schema Personaggio.

---

## 1. Visione generale del progetto

Un gioco web basato sull'ambientazione Dragonlance, costruito a partire da una libreria personale di manuali PDF (di proprietà dell'utente, in copia cartacea) da cui estrarre regole, personaggi, mostri, oggetti, razze, ecc.

### Roadmap a fasi

1. **Fase 0 — Fondamenta dati**: pipeline di estrazione PDF → schema dati strutturato (mostri, incantesimi, oggetti, razze, classi)
2. **Fase 1 — Creazione personaggio**: wizard web che usa il DB per creare PG con tutte le regole applicate
3. **Fase 2 — Arena di test**: motore di combattimento per validare regole, incantesimi, mostri, oggetti in condizioni "live"
4. **Fase 3 — DM system a nodi**: editor di avventure con struttura a nodi (scene, bivi, incontri)
5. **Fase 4 — Obiettivo finale**: applicazione che converte moduli cartacei Dragonlance in avventure in solitario giocabili, sfruttando l'infrastruttura delle fasi precedenti (probabile uso di LLM per bozza automatica + revisione manuale)

### Uso previsto

Progetto **privato, uso personale** (utente + eventuale gruppo di gioco). L'utente possiede legalmente tutti i manuali cartacei di riferimento. Nessuna distribuzione pubblica o monetizzazione prevista — questo abbassa sensibilmente i rischi di copyright e permette di essere meno parsimoniosi nell'estrazione di testo (descrizioni complete, non solo dati numerici).

---

## 2. Strategia sul regolamento "omnibus" multi-edizione

**Obiettivo**: prendere il meglio da ogni edizione (mostri, incantesimi, oggetti, razze, classi) creando un regolamento omnibus.

**Decisione chiave**: le edizioni D&D non differiscono solo nei numeri ma nella struttura meccanica (THAC0 vs bonus di attacco vs bonus di competenza; saving throw per categoria vs per abilità/caratteristica; sistema di magia vanciano puro vs slot semplificati). Costruire un motore multi-sistema nativo è sconsigliato come punto di partenza (rischio di anni di lavoro sull'infrastruttura senza mai arrivare a giocare).

**Approccio scelto**: **5ª edizione come motore meccanico (chassis)**, altre edizioni come **fonte di contenuto/lore**, convertito nella matematica 5e.

> Principio guida: *"Il motore usa la matematica 5e (bonus competenza, saving throw su caratteristica, sistema di slot). Il contenuto (razze, classi, mostri iconici) viene ricostruito per rispettare l'identità narrativa/meccanica originale, non convertito meccanicamente 1:1."*

### Decisioni del 12 agosto 2026

**Edizione di riferimento: PHB 5e 2014, non 2024.**
La 2024 rende le specie numericamente neutre, spostando i bonus di caratteristica sul background. È incompatibile con la decisione successiva: se le specie non portano numeri, non c'è nulla da vincolare. La 2014, con i bonus ancorati alla razza, regge l'impianto voluto.

**Vincoli rigidi di caratteristica: sì, in stile 2e.**
Requisiti minimi, massimali razziali e classi precluse a certi popoli sono replicati come vincoli **meccanici applicati dal sistema** in fase di creazione del personaggio, non affidati alla narrazione. Sono già estratti in `source_2e` e ora presenti anche in `mechanics_5e` come regole di validazione.

**Limiti di livello per demiumani: no, non si applicano.**
Nessuna razza ha un tetto di livello. È la meccanica 2e più universalmente abbandonata dalle edizioni successive, blocca le campagne lunghe e contraddice il principio già fissato per i Cavalieri (potere sempre monotono crescente, mai regressioni né tetti).

Distinzione mantenuta netta nei dati:

- i limiti **restano** in `source_2e.class_level_limits`, perché la tabella del manuale dice quello;
- in `mechanics_5e` il campo `level_limits.applied` è `false` con una nota esplicita, così è chiaro che l'assenza è deliberata e non una dimenticanza di conversione;
- resta invece applicata la **preclusione**: una classe assente dalla tabella non è disponibile a quella razza.

### Decisioni del 12 agosto 2026 (secondo giro)

**Generazione delle caratteristiche: si tira.** Metodo di default **4d6 scarta il minore**, già ufficiale in 5e 2014; array standard e point-buy restano alternative.

Motivazione: i requisiti della 2e presuppongono caratteristiche su scala 3-18. In 2e qualificarsi come Cavalier era raro *per design*, non impossibile. Il point-buy non sa esprimere la rarità — appiattisce tutto a un budget uguale per tutti, quindi ciò che era raro diventa impossibile. Avendo scelto vincoli rigidi in stile 2e, si adotta anche la generazione che li rende sensati.

I requisiti **non vengono ammorbiditi**. In creazione, se il metodo scelto rende irraggiungibile una combinazione razza+classe, il sistema **segnala e propone il tiro, senza bloccare**. L'Aghar usa i dadi propri del manuale: non è più un caso fuori scala da gestire come eccezione, ma una variante del metodo di generazione.

**Aggiustamenti negativi: si tengono.** Il netto da +0 a +2 contro il +3 della 5e non va pareggiato. Le razze di Krynn non verranno mai mescolate con quelle del PHB: il sistema è chiuso, conta solo l'equilibrio interno. Si conserva anche la ridondanza fra aggiustamento negativo e massimale sulla stessa caratteristica, perché è del manuale.

**Massimali razziali: si tengono tutti**, applicati sia in creazione sia come **tetti di crescita**. Da non confondere con i limiti di livello, che restano non applicati: un massimale limita quanto può salire un punteggio, non a che livello si ferma il personaggio.

**Barbaro: vale l'unione dei due set di vincoli.** Si applicano DEX max 16 e INT max 18 della scheda razziale, oltre ai minimi della voce di classe. La proposta di scartare i massimali si fondava sul fatto che sotto point-buy non mordono; con il tiro dei dadi un 18 contro un tetto a 16 è un vincolo reale, quindi la premessa è caduta. La variante "barbaro come background" resta accantonata allo schema Personaggio.

### Scoperta importante: materiale ufficiale 5e già esistente

**Dragonlance: Shadow of the Dragon Queen** (Wizards of the Coast, 2022) è un manuale ufficiale 5e ambientato a Krynn. Contiene:
- **Kender come razza giocabile ufficiale** (taglia Small, vantaggio/immunità contro paura, tratto firma "Taunt" come azione bonus) — usabile come base diretta, risparmia lavoro di conversione
- **Nessun'altra nuova razza giocabile** (Draconici, Irda, Gully Dwarves restano da ricostruire come homebrew se si vogliono giocabili — nel manuale ufficiale i Draconici restano mostri/nemici)
- Gestione dei Cavalieri di Solamnia via feat (approccio criticato dalla community per permettere di "saltare" da Corona a Rosa senza percorso — vedi sezione 4, la nostra soluzione evita questo problema)

**Azione consigliata**: procurarsi questo manuale come fonte primaria per la conversione 5e degli elementi Dragonlance, da integrare con le edizioni precedenti per lore/dettaglio.

---

## 3. Schema dati — campi trasversali decisi

Ogni entità estratta (razza, classe, mostro, oggetto, incantesimo, divinità, ordine cavalleresco...) deve prevedere questi campi trasversali, oltre ai dati specifici della categoria:

```json
{
  "source_edition": "string",        // es. "2e", "3.5e", "5e-SotDQ", "homebrew"
  "source_book": "string",           // manuale di provenienza
  "homebrew_conversion": true/false, // true se ricostruito/adattato manualmente per fedeltà narrativa
  "valid_eras": ["string"]           // epoche in cui l'elemento è narrativamente valido (vedi sezione 5)
}
```

### Il doppio strato `source_2e` / `mechanics_5e`

Ogni entità è divisa in due blocchi:

- **`source_2e`** — dati grezzi fedeli al manuale. Requisiti, aggiustamenti, formule, limiti di livello, abilità speciali. Si tocca solo per correggere errori di trascrizione.
- **`mechanics_5e`** — la conversione. Contiene già le regole di validazione (vincoli di caratteristica, classi precluse); tratti, taglia e velocità sono da compilare.

**Motivazione.** L'audit della libreria ha mostrato che le fonti Dragonlance sono tutte AD&D 2e (26 volumi) o SAGA (10 volumi, senza statistiche utilizzabili): **non esiste materiale 5e su Krynn**, e *Shadow of the Dragon Queen* continua a mancare. La conversione sarà quindi interamente nostra e andrà rivista più volte. Ancorare il grezzo alla fonte permette di rifare la conversione quante volte serve **senza mai riaprire i PDF**, e rende verificabile ogni numero risalendo alla pagina originale tramite `pages_pdf`.

Corollario operativo: i file in `dati/razze/`, `dati/classi/` e `dati/divinita/` sono **generati** dagli script `build_*.py`, che sono l'unica sorgente di verità. Non vanno modificati a mano.

### Stato

`dati/schema/` contiene `razza`, `classe` e `divinita`. Popolate e validate a zero errori: **15 razze, 17 classi, 21 divinità**. Vedi `dati/LEGGIMI.md`.

Restano da scrivere: **Personaggio**, Incantesimo, Mostro, Oggetto.

---

## 4. Elementi iconici — lista di lavoro

### Roster razziale: solo i clan giocabili

*Tales of the Lance* riserva esplicitamente ai PNG i clan nanici **Klar, Theiwar, Daergar e Zhakar** (capitolo Dwarf, nota sui clan giocabili). Il roster estratto in `dati/razze/` li esclude di conseguenza. I nani giocabili sono quindi Hylar/Daewar (montagna), Neidar (collina) e Aghar (sozzi).

### Razze (da trattare con cura manuale, non conversione automatica)
- **Kender** — fonte ufficiale 5e disponibile (Shadow of the Dragon Queen), da usare come base
- **Draconici** (Baaz, Kapak, Bozak, Sivak, Aurak) — non giocabili ufficialmente in 5e, restano mostri nel manuale ufficiale; se si vogliono giocabili, servono conversione homebrew (effetti particolari alla morte da preservare)
- **Irda** — cambiaforma/illusione, homebrew necessario
- **Gully Dwarves (Aghar)** — caratterizzazione comica/sociale, homebrew necessario
- **Minotauri di Dragonlance** — cultura marziale specifica (nota: esistono statistiche minotauro "generiche" in *Mythic Odysseys of Theros*, utilizzabili come punto di partenza per la conversione)

### Classi/percorsi iconici
- **Cavalieri di Solamnia** — vedi sezione dedicata (5.1)
- **Maghi delle Torri di Alta Stregoneria** — legame allineamento/scuola (Rossa=neutrale, Bianca=buono, Nera=malvagio), il Test come rito di passaggio, vincolo forte da modellare come classe/sottoclasse con restrizioni integrate
- **Cavalieri di Takhisis/Neraka** — controparte oscura dei Cavalieri di Solamnia (epoche successive)

### Mostri/PNG simbolo
- Draghi cromatici e metallici legati alla Guerra della Lancia
- NPC storici (Kitiara, Raistlin, ecc.) — da decidere se trattarli come PNG giocabili o solo lore

### Oggetti/artefatti
- Bastone di Magius (Raistlin)
- Lancia dei Draghi (Dragonlance) — arma che dà il nome alla saga
- Oggetti minori legati agli Ordini Cavallereschi

---

## 5. Sistema epoche (`valid_eras`)

> **`valid_eras` è uno strato editoriale, non un dato di fonte.** *Tales of the Lance* è ambientato alla Guerra della Lancia e non ragiona per epoche: il campo è una nostra inferenza dal canone e ogni entità lo dichiara esplicitamente nelle note. Nei dati sono applicate **due sole restrizioni**: gli **Irda**, che si estinguono di fatto con la Guerra del Caos, e gli **Ordini Sacri con le 21 divinità**, che non concedono incantesimi in `age_of_despair` né in `age_of_mortals_post_chaos`. Tutto il resto è valido in ogni epoca finché non arrivano fonti migliori.

**Decisione chiave**: dato che l'obiettivo finale è convertire moduli di *qualsiasi* epoca Dragonlance, non si fissa un'unica epoca di ambientazione. Ogni elemento vincolante (classi/sottoclassi, divinità, appartenenze, oggetti iconici) riceve un tag di epoche valide. Ogni avventura riceve un tag `era`. Al momento della selezione del personaggio per un'avventura, il sistema segnala (soft warning, non blocco rigido) eventuali incompatibilità — es. un Chierico di Mishakal non è coerente con un'avventura ambientata prima della Guerra della Lancia.

### Enum epoche proposto

| Chiave | Periodo | Note meccaniche principali |
|---|---|---|
| `pre_cataclysm` | Terza Era, prima del Cataclisma | Uso raro, utile per materiale su Huma |
| `age_of_despair` | Dopo il Cataclisma, prima della Guerra della Lancia | **Niente Cherici buoni** (solo pochi Cherici malvagi di Takhisis), niente Misticismo, Cavalieri di Solamnia esistono ma perseguitati |
| `war_of_lance` | Guerra della Lancia in poi (fino alla Guerra del Caos) | Cherici disponibili, Cavalieri riabilitati, Draconici esistono (nascono in questo periodo) |
| `age_of_mortals_post_chaos` | Dopo la Guerra del Caos | Dèi assenti di nuovo, Misticismo sostituisce la magia divina classica, magia delle Torri cambia natura |
| `post_war_of_souls` | Dèi tornati | Situazione "restaurata" con differenze (es. nuovo patrono dei Cavalieri, Shinare, accanto a Kiri-Jolith) |

**Nota su Cleric**: è la classe più vincolata dall'epoca — praticamente non disponibile per PG buoni/neutrali in `age_of_despair` e nella prima parte di `age_of_mortals_post_chaos`.

**Da fare**: verificare disponibilità/adattamento per Sorcerer, Warlock, Monk, Druid nelle varie epoche (non ancora ricercato in dettaglio).

---

## 5.1 Design dettagliato — Cavalieri di Solamnia

### Riferimento storico (2e)
- Ogni cavaliere parte come Cavaliere della Corona
- Può fare domanda per la Spada al 3° livello come Corona; per la Rosa al 4° livello come Spada
- Può restare a un ordine indefinitamente senza avanzare
- Rosa richiede caratteristiche elevate (Forza/Costituzione 15, Destrezza 12, Intelligenza 10 nella versione storica) + prove specifiche (viaggio di 500 miglia/30 giorni, prova di saggezza, testimoni)
- **Meccanica 2e da NON portare in 5e**: avanzare a un ordine superiore resettava l'esperienza a zero (pur mantenendo i PF) — penalizzante e sconsigliato in ottica 5e moderna

### Errore da evitare (osservato nel manuale ufficiale)
Shadow of the Dragon Queen gestisce l'accesso agli ordini tramite feat, permettendo teoricamente di raggiungere la Rosa al 4° livello senza mai passare per Corona/Spada — criticato dalla community per incoerenza con la lore. **La nostra soluzione (sequenzialità obbligata) evita questo problema.**

### Design scelto (in evoluzione)

**Decisione aperta**: classe standalone (clone del Fighter con meccaniche Corona già dal 1° livello) invece di sottoclasse al 3° livello — scelta di creazione del personaggio fin dall'inizio, non archetipo scelto dopo 2 livelli "generici".

**Struttura per tier** (Corona → Spada → Rosa):
- Corona: feature dal 1° livello della classe
- Spada: sblocco a un livello soglia (es. 7°) SE completata una "Quest della Spada" + prerequisiti di caratteristiche; altrimenti si continua semplicemente come Corona potenziato (nessuna penalità, nessun livello morto)
- Rosa: stesso meccanismo a un livello soglia superiore (es. 10°-11°), richiede status Spada + quest + caratteristiche più alte
- Avanzamento **non retroattivo**: la feature si attiva dal momento del completamento della quest, non si ricalcola all'indietro
- Potere del personaggio resta sempre monotono crescente (mai perdita di PF/feature come in 2e)

**Sinergia con Fase 3 (DM a nodi)**: le "Quest della Spada" e "Quest della Rosa" sono ottimi candidati come primi moduli di test per l'editor di avventure a nodi — obiettivo narrativo chiaro, non semplici flag booleani.

### Conferma dai dati estratti (agosto 2026)

L'estrazione di `Tales of the Lance` conferma il design sopra col dato in mano:

- I tre ordini hanno **tabelle di avanzamento separate che ripartono da 0 PE**: Corona dal 1° livello, Spada dal 3°, Rosa dal 4°. L'azzeramento dell'esperienza è quindi reale e documentato, non ricordato.
- I requisiti crescono lungo la sequenza: Corona For 10/Cos 10/Sag 10, Spada For 12/Sag 13, Rosa For 15/Cos 15/Des 12/Sag 13. **La sequenzialità obbligata non è un'invenzione nostra**: è ciò che la 2e faceva già, e che *Shadow of the Dragon Queen* ha perso passando ai feat.
- I Cavalieri della Spada ottengono incantesimi dal 6° livello e le capacità del Paladino al livello corrente. **Gli incantesimi vengono da Kiri-Jolith, non da Paladine**, perché fu il dio della guerra santa a ispirare l'ordine, benché Paladine resti il dio più venerato dai cavalieri. Il legame ordine-divinità è quindi meccanico, non solo narrativo: Kiri-Jolith concede fra i suoi poteri anche `+1 agli attacchi contro avversari malvagi` (vedi `dati/divinita/kiri-jolith.json`).
- Il mezzelfo è l'unica razza non umana ammessa ai Cavalieri, con tetto al 10° livello.
- Il manuale non dice se un Cavaliere della Rosa conservi gli incantesimi acquisiti come Spada: nodo aperto per la conversione.

**Deciso il 12 agosto 2026 — il principio NON si estende ai Maghi delle Torri.** Il caso non è simmetrico. Un Cavaliere nasce già della Corona al 1° livello; un Mago non giura a una Veste al 1° livello, lo fa al **Test dell'Alta Stregoneria**, al 3°. Forzare la scelta al 1° sarebbe *meno* fedele alla fonte, non più coerente. Modellazione confermata: `mago-alta-stregoneria` come classe base, le tre Vesti come affiliazione dichiarata a `entry_level` 3, con progressione e incantesimi ereditati dalla classe base.

---

## 5.2 Fonti esterne — community e materiale semi-ufficiale

Prima di ricostruire da zero contenuti (razze, classi, oggetti, mostri), vale la pena controllare queste fonti: buona parte del lavoro di conversione/reconciliazione multi-edizione è già stata affrontata dalla community.

### Dragonlance Nexus (dragonlancenexus.com)
Hub della community più organizzato per Dragonlance, con team di design riconosciuto (include Timothy Shiflet "Aelfwyn", Trampas "Dragonhelm" Whiteman, Chuck Martinell, Ed Mekeel). Sezioni utili:
- Categoria **D&D 5e Classes & Subclasses**: sottoclassi custom (es. Academy Sorcerer — sottoclasse Sorcerer legata all'Accademia di Stregoneria, risposta diretta alla "crisi d'identità" del Sorcerer in Dragonlance; Sylvan Mages — Warlock patto Archfey; Goodfellow of Branchala — Bard College of Satire)
- Rubrica **"Classes of Krynn"** (di Aelfwyn) e **"Races (Species) of Krynn"** (di Dragonhelm) — colonne dedicate proprio ai temi che ci servono
- Prodotto commerciale **Tasslehoff's Pouches of Everything** (DM's Guild) — sourcebook pensato esplicitamente per supportare il gioco in ogni epoca di Krynn, molto allineato al nostro sistema `valid_eras`
- Conversioni di moduli esistenti (es. Tyranny of Dragons → Ansalon/Taladas, Princes of the Apocalypse) — utili come riferimento per la Fase 4 (conversione moduli)
- Sezione **Bestiario 5e** con mostri custom

### Raistlin's Guide to Krynn (Pablo Moro et al., PDF su EN World, v2.3)
Conversione 5e completa e organica, con filosofia dichiarata: modificare il meno possibile le regole core 5e, riusando classi/razze esistenti reskin-nate. Contiene:
- Razze disponibili con tratti completi (Draconici con le 5 sottorazze — Baaz/Kapak/Bozak/Sivak/Aurak, inclusi talenti per l'arma a soffio; Nani con le varianti di clan; Kender con sottorazza "Vera"/"Afflitta"; Umani con etnie e lingue)
- **Framework delle 5 fonti di magia**, una per classe incantatrice: Cleric=dèi (Sacre Ordini delle Stelle), Druid=dèi della natura, Sorcerer=essenza di Krynn, Wizard=Magia delle Lune (con sistema di modificatori legato alle fasi lunari), Warlock=patto (storicamente Cavalieri della Spina/Neraka)
- **Background "Mystic"**: soluzione narrativa per personaggi con poteri simil-divini senza appartenenza religiosa organizzata — utile alternativa/integrazione al blocco rigido di Cleric per `age_of_despair`
- Statblock completi per mostri (5 sottorazze di Draconici, Dragonspawn, Thanoi, Ogre Titan)
- Oggetti magici iconici già statuati (Dragonlance/Lancia di Huma, Bastone di Magius, Bastone di Cristallo Blu, Dragonarmor, Nightbringer, Wyrmsbane, Wyrmslayer)
- Lista delle fazioni principali di Krynn con suddivisioni interne (Cavalieri di Solamnia: Corona/Spada/Rosa; Maghi di Alta Stregoneria: Bianca/Rossa/Nera; Cavalieri di Neraka: Giglio/Spina/Teschio; Legion of Steel; Sacre Ordini delle Stelle; Armate di Draghi)

### Conversioni di Kentti (wiki personale)
Documento dedicato "Dragonlance Classes 5e.pdf" con classi e fazioni di Krynn — da verificare in dettaglio se serve un secondo punto di vista sulle classi.

### Sourcebook 3e/3.5e "quasi ufficiali" (Sovereign Press/Margaret Weis Productions) — utili se reperibili fisicamente
- **Races of Ansalon** — catalogo razze più esaustivo esistente (vedi sezione 4)
- **Age of Mortals** — razze, classi, magia, mostri e geografia della Quinta Era
- **Towers of High Sorcery** — Maghi di Alta Stregoneria
- **Holy Orders of the Stars** (3.5e) — chierici, chiese, divinità
- **Knightly Orders of Ansalon** — Cavalieri di Solamnia, Cavalieri Oscuri, Legion of Steel

### Conferma importante: il sistema epoche è canone ufficiale, non un'invenzione nostra
Il **Dragonlance Campaign Setting** (3e, 2003) — il compendio ufficiale più completo per la 3e — dedica un intero capitolo a spiegare la magia attraverso le epoche di Krynn: epoche in cui manca la magia arcana, altre in cui manca la divina, altre in cui mancano entrambe. Il nostro sistema `valid_eras` è quindi allineato al modo in cui il setting stesso gestisce da sempre la disponibilità di classi/magia — non un compromesso tecnico inventato da noi.

### Il concetto "Mystic" — tre implementazioni diverse da confrontare
Ricorre in più fonti come soluzione al problema "potere divino senza dèi presenti/organizzati", ma con meccaniche diverse a seconda della fonte — da decidere quale adottare (o come sintetizzarle) per l'Omnibus:
1. **Dragonlance Campaign Setting (3e, ufficiale)**: prestige class, paragonabile al Favored Soul di 3e ma con sapore di Krynn
2. **Raistlin's Guide to Krynn (fan, 5e)**: background — percorso narrativo per canalizzare energia divina senza appartenenza religiosa organizzata
3. **Dragonhelm's Guide to the Sorcerers of Krynn (Trampas Whiteman, ottobre 2025)**: sottoclasse Sorcerer "Divine Soul" — i mystics sono sorcerer la cui scintilla è di origine divina

### Sourcebook fondativi (probabilmente già posseduti in copia cartacea)
- **Dragonlance Adventures** (1987, TSR, AD&D 1e/2e, 128 pagine) — manuale fondativo originale: razze/mostri nativi di Krynn (Draconici, Gully Dwarves, Shadowpeople, Dreamwraiths, Spectral Minions, Thanoi), opzioni per Cavalieri di Solamnia, Kender, Gnomi, Maghi di Alta Stregoneria. Probabilmente la fonte "più pura" da cui partire nella Fase 0, essendo il testo originale da cui derivano le edizioni successive
- **Dragonlance Campaign Setting** (2003, 3e, 288 pagine) — compendio più completo per la 3e: razze, prestige class, talenti, incantesimi, mostri, mappe, con trattazione dettagliata delle epoche magiche (vedi sopra)
- **Mists of Krynn** (DL15, 1988, modulo avventura AD&D) — approfondimento su razze (Kender, Gully Dwarves, Shadow People, Draconici) e avventure ambientate prima/durante/dopo la Guerra della Lancia, livelli 0-15 — buon riferimento per la Fase 4 (conversione moduli), essendo già strutturato su più epoche

### Sviluppo da monitorare: "D&D Icons"
Al Gen Con 2026 (30 luglio 2026) Wizards of the Coast ha annunciato ufficialmente il ritorno di Dragonlance in D&D tramite una nuova iniziativa chiamata "D&D Icons", con il coinvolgimento diretto di Margaret Weis e Tracy Hickman per "ristabilire il canone e rilanciare" l'ambientazione. Dettagli sui contenuti non ancora resi noti al momento della stesura di questo documento — annuncio successivo al mio ultimo aggiornamento di conoscenza, quindi da verificare periodicamente per eventuali nuovi materiali ufficiali 5e che potrebbero ridurre ulteriormente il lavoro di conversione.

---

## 6. Note su strumenti/modello di lavoro

- Fasi di design/decisioni strutturali (riconciliazione regole, schema dati, trade-off architetturali): beneficiano di un livello di ragionamento più alto (Opus o thinking/effort elevato)
- Fasi di implementazione/coding: Sonnet è il riferimento principale per lavoro di codice
- Estrazione/pulizia dati di massa (parsing ripetitivo di statblock): valutare un modello più leggero (Haiku) per volumi alti, riservando modelli più potenti alle eccezioni difficili

---

## 7. Prossimi passi aperti (non ancora decisi/completati)

### Deciso il 12 agosto 2026

- [x] ~~PHB 5e 2014 o 2024~~ → **2014**, per compatibilità con i vincoli rigidi di caratteristica
- [x] ~~Vincoli rigidi di caratteristica~~ → **sì**, come regole meccaniche in `mechanics_5e`
- [x] ~~Limiti di livello per demiumani~~ → **no**, restano solo in `source_2e` come dato di fonte
- [x] ~~Pattern classe standalone per i Maghi delle Torri~~ → **no**, le Vesti restano affiliazione al 3° livello
- [x] ~~Ri-estrazione della libreria~~ → **fatta**, con due regressioni intercettate e risolte

### Ancora aperto

- [~] Schema JSON completo — **Razza, Classe e Divinità fatte** (`dati/schema/`), 15 + 17 + 21 entità validate. Restano **Personaggio**, Incantesimo, Mostro, Oggetto
- [ ] **Il PHB 5e 2014 non è fra i PDF**: la cartella `Manuali/D&D 5e/` contiene solo edizioni 2024. Da decidere se usare `2014.5e.tools` (JSON strutturato, più comodo dei PDF) come metro di conversione, o procurarsi i PDF 2014
- [ ] Compilare `mechanics_5e` con tratti, taglia e velocità — i vincoli di validazione sono già dentro
- [ ] Procurarsi *Shadow of the Dragon Queen*: resta l'unica fonte 5e ufficiale su Krynn e continua a mancare
- [ ] Estrarre le sfere per dio erano l'ultima questione aperta sui sacerdoti: **fatto**, vedi `dati/divinita/`
- [ ] Smaltire le 22 scansioni in `ocr_queue.txt` (nessuna bloccante)
- [ ] Decidere come modellare il Barbaro, che il manuale tratta sia come cultura umana sia come classe

