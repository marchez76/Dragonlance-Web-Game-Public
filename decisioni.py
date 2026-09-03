"""Registro canonico delle decisioni di progetto.

UNICA SEDE. `genera_contesto.py` importa da qui: l'elenco non va duplicato
altrove, ne' ricopiato in un documento a mano. Chi aggiunge una decisione
tocca solo questo file.

PERCHE' ESISTE UN `id` OLTRE AL NUMERO
    Il numero e' un **ordinale di lettura**: dice dove sta la decisione
    nell'elenco cronologico, ed e' comodo per parlarne. Non e' una chiave:
    e' gia' cambiato, e i testi scritti sotto una numerazione precedente
    hanno continuato a citare il vecchio numero senza che nulla li
    riallineasse. Diagnosi in `dati/RAPPORTO-personaggio.md`, sezione 3.4.

    L'`id` e' la chiave: si sceglie una volta e non cambia mai piu', nemmeno
    se la decisione viene riformulata (la 32 lo e' stata) o se l'elenco
    venisse riordinato. Un rimando si scrive **per id**; il numero che gli
    sta accanto e' un derivato, e come ogni derivato di questo progetto non
    si scrive a mano ma si rigenera (CLAUDE.md, punto 3).

FORMA CANONICA DI UN RIMANDO
        decisione 10 (`massimali-razziali`)

    `verifica_decisioni.py` la controlla in tutto il progetto e, con
    `--correggi`, riscrive il numero a partire dall'id. Da qui in avanti una
    rinumerazione costa un comando, non sessanta file riletti a mano.
"""

from collections import namedtuple

Decisione = namedtuple("Decisione", "numero id titolo testo")

DECISIONI = [
    Decisione(
        1, 'motore-5e',
        'Motore',
        '5e come chassis meccanico; le altre edizioni sono fonte di '
        'contenuto e lore.'),
    Decisione(
        2, 'edizione-phb-2014',
        'Edizione di riferimento',
        'PHB **2014**, non 2024. La 2024 rende le specie numericamente '
        'neutre, incompatibile con la decisione 3 (`vincoli-caratteristica`).'),
    Decisione(
        3, 'vincoli-caratteristica',
        'Vincoli di caratteristica',
        'Minimi, massimali razziali e classi precluse sono regole '
        '**meccaniche** applicate in creazione PG, non affidate alla '
        'narrazione.'),
    Decisione(
        4, 'limiti-di-livello',
        'Limiti di livello per demiumani',
        '**Non si applicano.** Restano in `source_2e` come dato di fonte, '
        'con `level_limits.applied` a `false` e nota esplicita.'),
    Decisione(
        5, 'cavalieri-solamnia',
        'Cavalieri di Solamnia',
        'Sequenza obbligata Corona → Spada → Rosa, senza azzeramento '
        "dell'esperienza e senza tetti."),
    Decisione(
        6, 'maghi-delle-torri',
        'Maghi delle Torri',
        'NON classe standalone dal 1° livello: il giuramento alla Veste '
        'avviene al Test, al 3°. Le tre Vesti sono affiliazioni, non '
        'classi.'),
    Decisione(
        7, 'doppio-strato',
        'Schema a doppio strato',
        '`source_2e` fedele al manuale e immutabile, `mechanics_5e` '
        'rivedibile. I JSON sono generati da `build_*.py`.'),
    Decisione(
        8, 'generazione-caratteristiche',
        'Generazione delle caratteristiche',
        'Default **4d6 scarta il minore**; array standard e point-buy '
        'restano alternative. Se il metodo scelto rende irraggiungibile una '
        'combinazione, il sistema segnala e propone il tiro senza bloccare. '
        "L'Aghar usa i dadi propri del manuale."),
    Decisione(
        9, 'aggiustamenti-negativi',
        'Aggiustamenti negativi',
        'Si tengono, trascritti fedelmente, doppia penalità inclusa. Il '
        "sistema è chiuso: conta solo l'equilibrio interno."),
    Decisione(
        10, 'massimali-razziali',
        'Massimali razziali',
        'Si tengono tutti, applicati sia in creazione sia come **tetti di '
        'crescita**. Non sono i limiti di livello.'),
    Decisione(
        11, 'barbaro-vincoli',
        'Barbaro, vincoli',
        "Vale l'**unione** dei due set: massimali della scheda razziale più "
        'minimi della voce di classe.'),
    Decisione(
        12, 'valid-eras',
        '`valid_eras`',
        'Strato editoriale nostro, non dato di fonte. Due sole restrizioni '
        'applicate: Irda e Ordini Sacri con le divinità.'),
    Decisione(
        13, 'taglia',
        'Taglia',
        "Dedotta dall'altezza, la 2e non assegna categorie. Il Minotauro "
        'resta **Medium**: in 5e anche il Golia a 7-8 piedi è Medium.'),
    Decisione(
        14, 'infravisione',
        'Infravisione',
        'Dove il manuale la dichiara si converte in scurovisione; dove tace '
        'resta **assente per scelta**, non per dimenticanza.'),
    Decisione(
        15, 'tratti-trascrizione-integrale',
        'Tratti, trascrizione integrale',
        'Ogni tratto della voce 2e va in `mechanics_5e` con uno stato di '
        'conversione: `direct`, `adapted`, `pending`, `source_only`. Non si '
        'inventa meccanica 5e.'),
    Decisione(
        16, 'nove-tratti-phb2e',
        'I nove tratti del PHB 2e',
        'Dove il PHB 2014 ha già un equivalente si copia quello; dove la 5e '
        'ha eliminato un tratto si ripristina dalla 2e, malus inclusi. La '
        'fedeltà alla fonte prevale sulla convenzione 5e.'),
    Decisione(
        17, 'pending-krynn',
        'I tredici pending di Krynn',
        'Tutti convertiti. *Schernire* è marcato **provvisorio** in attesa '
        'di Shadow of the Dragon Queen; la *Specializzazione nelle armi* '
        'del Minotauro resta `source_only` perché la fonte concede un '
        'permesso, non un beneficio.'),
    Decisione(
        18, 'minotauro-irda-appendice',
        "Minotauro e Irda dall'Appendice",
        'Il capitolo razziale è avaro su queste due voci: si integra da `MC '
        "- Dragonlance Appendix` solo ciò che l'Appendice **dichiara**, con "
        'fonte marcata distintamente.'),
    Decisione(
        19, 'compensazione-umano',
        "Compensazione dell'umano",
        "L'umano aveva zero tratti e zero aggiustamenti perché in 2e era "
        "pagato dall'assenza di limiti di livello, che la decisione 4 (`limiti-di-livello`) ha "
        'abolito. Compensato con +1 a due caratteristiche a scelta, una '
        'competenza e un linguaggio, marcati come conversione editoriale.'),
    Decisione(
        20, 'tappo-barbaro',
        'Tappo al Barbaro',
        '+1 fissi a Forza e Costituzione, editoriali e reversibili. '
        '**Tappo, non soluzione**: la conversione a background resta la '
        'strada giusta e va decisa con lo schema Personaggio.'),
    Decisione(
        21, 'tre-elfi-terrestri',
        'I tre elfi terrestri',
        "Applicato il metodo della 18 alle tre voci dedicate dell'Appendice "
        '(pagg. 33-35). Esito parziale: due su tre hanno una capacità '
        'dichiarata, il Qualinesti nessuna.'),
    Decisione(
        22, 'tratto-fantasma-qualinesti',
        'Il tratto fantasma del Qualinesti',
        "Il segnaposto che registrava l'assenza è **rimosso**: non "
        'concedeva nulla ma contava nei totali, falsando ogni statistica a '
        "valle. L'informazione è passata fra le ambiguità di fonte, dove "
        'stanno le altre registrazioni dello stesso tipo.'),
    Decisione(
        23, 'principio-del-clone',
        'Il principio del clone',
        'Per le classi la fedeltà alla fonte non basta: le razze 2e sono '
        'ricche, le classi 2e sono povere e trascriverle produce gusci '
        'vuoti. Ogni classe di Krynn è un **clone meccanico** della classe '
        'base 5e corrispondente (SRD 5.1), con innestati sopra i privilegi '
        'e le restrizioni della fonte. Cinque classi restano senza chassis, '
        'per decisione.'),
    Decisione(
        24, 'sfere-sacerdotali',
        'Sfere sacerdotali',
        'Si tengono nella forma fedele: le **sfere** filtrano quali '
        'incantesimi il chierico può preparare, ripristinando la negazione '
        "d'accesso; il **Dominio** 5e resta come sottoclasse per i "
        'privilegi di livello. Ogni divinità è associata al Dominio 2014 '
        'più coerente.'),
    Decisione(
        25, 'statuto-sotdq',
        'Lo statuto di SotDQ',
        '*Shadow of the Dragon Queen* è materiale ufficiale 5e su Krynn: '
        '**quinta provenienza** nel campo fonte dei tratti di '
        '`mechanics_5e`, non un terzo strato. Non è autoritativo su tutto, '
        'perché non è la conversione ufficiale del materiale 2e ma un '
        'prodotto scritto da zero che ne condivide i nomi. Prevale su '
        '*Schernire*; altrove divergiamo, e le divergenze sono registrate.'),
    Decisione(
        26, 'criterio-tracciabilita',
        'Il criterio della tracciabilità',
        '**Qualsiasi materiale esterno che non porti con sé fonte e pagina '
        'è inutilizzabile**, a prescindere dal resto della sua qualità. '
        'Tutto il progetto si regge sulla tracciabilità: un dato non '
        'verificabile non entra. È un filtro che si applica in trenta '
        'secondi e risparmia analisi lunghe. Entrambi i lotti in `import/` '
        'sono respinti e chiusi.'),
    Decisione(
        27, 'sette-campi-2e',
        'I sette campi 2e senza corrispettivo',
        'Non erano un problema unico. **Gruppo A** — frequenza, numero, '
        'organizzazione, ciclo, dieta: dati di mondo, non di scheda, e '
        'diventano input del generatore di incontri in Fase 3. **Gruppo B** '
        '— il morale non è un campo ma un parametro di comportamento: '
        'senza, ogni scontro finisce con tutti i nemici morti, e diventa '
        "input dell'IA in arena. **Gruppo C** — la resistenza magica è "
        "l'unica vera decisione ed è **rinviata alla Fase 2**, perché i "
        'Gradi di Sfida su cui calibriamo presuppongono che non ci sia.'),
    Decisione(
        28, 'ogre-e-orughi-mostri',
        'Ogre e Orughi sono mostri',
        "La voce `Ogre (of Krynn)` dell'Appendice torna a categoria "
        "**creatura**, non `razza_altra`. L'asimmetria con Theiwar/Zakhar "
        '(clan nanici che il manuale riserva ai PNG giocabili) non regge '
        'per gli ogre comuni: non sono un clan riservato, sono avversari '
        "classici e servono all'arena. La parentela dichiarata con l'Irda "
        'resta nota di lore nella voce, non criterio di categoria. Vale il '
        'criterio della porta aperta: un mostro può sempre diventare razza '
        'in seguito, il contrario è più fastidioso.'),
    Decisione(
        29, 'traag-armi-manufatte',
        'Il Traag usa armi manufatte',
        'Segue il precedente ufficiale dei cinque draconici, che '
        'sostituiscono sistematicamente le armi naturali con armi manufatte '
        '(Baaz spada corta, Bozak tridente, Kapak pugnale, Sivak spada '
        "seghettata; solo l'Aurak conserva un attacco naturale). Il Traag "
        'riceve una **lancia**, scelta per coerenza con la fonte (tribù '
        'povere, non soldati regolari; il testo cita esplicitamente la '
        "reach fra i vantaggi di usare un'arma) e marcata `adapted` con "
        'provenienza editoriale, non di fonte 2e. Il Multiattacco diventa '
        'non ambiguo: due attacchi di lancia, non artigli **o** arma.'),
    Decisione(
        30, 'precedenza-totl-appendice',
        'Precedenza fra Tales of the Lance e MC Appendix',
        'Prima volta che due fonti 2e si contraddicono su un tratto di '
        'personaggio giocante: dove **divergono**, prevale **Tales of the '
        "Lance**, perché è il capitolo dedicato ai PG mentre l'Appendice "
        'descrive la creatura dal punto di vista del Dungeon Master. Il '
        "criterio vale solo per la divergenza, non per l'integrazione: dove "
        "l'Appendice dichiara qualcosa su cui Tales of the Lance tace, la "
        'decisione 18 (`minotauro-irda-appendice`) resta intatta. Applicata ai due casi kender in '
        'conflitto (bonus armi da tiro, condizione sulla Sorpresa): '
        'entrambi restano registrati come divergenza e non si applicano.'),
    Decisione(
        31, 'soglia-dargonesti',
        'Soglia degli incantesimi innati dei Dargonesti',
        '**Opzione C**: tre soglie scalate (3°, 5°, 7°) invece del 10° '
        'unico della fonte o di una soglia bassa unica. Il 10° livello 2e '
        'non era "tardi" — era metà carriera in un sistema che arrivava al '
        '20° e oltre: copiarlo senza riscalarlo tradisce la sostanza pur '
        'conservando la cifra, lo stesso errore già segnalato per i valori '
        "XP del bestiario. Concentrare i tre incantesimi in un'unica soglia "
        'bassa perderebbe la gradualità che la fonte aveva scelto. Le tre '
        'soglie, leggermente più tarde del tiefling PHB 2014 (1°/3°/5°) per '
        'conservare lo scarto di "metà carriera" dentro la fascia '
        'giocabile, rientrano comunque nella decisione 16 (`nove-tratti-phb2e`): dove la 5e ha '
        'già un equivalente per i tratti razziali con incantesimi, si copia '
        'quel modello. Il 10° livello della fonte resta intatto in '
        '`source_2e`, non riscritto.'),
    Decisione(
        32, 'creatura-contro-entita',
        'Creatura contro entità nel bestiario',
        '**Riformulata** dopo un primo tentativo scorretto (che confondeva '
        '"legato a un oggetto" con "unico"). Il criterio è: ha un **nome '
        'proprio e una storia** → entità (es. il Cavaliere della Morte è, '
        'nella tradizione del setting, un individuo particolare — ma la '
        'voce dell\'Appendice stessa descrive un **tipo** ripetibile, "a '
        'Knight of Solamnia, cursed...", non un nome). È un '
        '**tipo/procedura ripetibile**, anche se potente e vincolato a un '
        'oggetto magico → creatura, si converte come le altre al suo vero '
        "grado di sfida. Il Warrior Skeleton (uno stregone lega l'anima di "
        'un guerriero potente a un diadema: procedura ripetibile, diademi e '
        "guerrieri diversi) è quindi una creatura, non un'entità unica. Il "
        'diadema di controllo non va rimandato alla Fase 3: è materiale da '
        'arena giocabile (raggio, condizione di perdita, inseguimento a '
        'velocità doppia), non colore descrittivo. La categoria entità '
        'resta per ora **vuota**: nessuna delle 62 voci lette ci è '
        "ricaduta, il criterio ha retto respingendo l'unica candidata."),
    Decisione(
        33, 'schema-oggetti',
        'Schema oggetti a parte',
        '`dati/schema/oggetto.schema.json`, stessa architettura a doppio '
        'strato di razze/classi/mostri. Il diadema dello Scheletro '
        'Guerriero non poteva restare dentro il mostro: è riutilizzabile su '
        'guerrieri diversi (decisione 32, `creatura-contro-entita`), quindi appartiene a sé quanto '
        'una spada appartiene a chi la impugna. Lo schema copre tre casi, '
        'non uno: equipaggiamento ordinario (armi/armature/attrezzatura — '
        "il buco più urgente per l'arena, dove oggi mancano perfino i danni "
        'di una spada lunga), oggetti magici, e oggetti con una creatura '
        'legata. Il diadema è il primo caso concreto, non il modello: gli '
        'altri due casi restano da popolare. Nel mostro resta un '
        "riferimento all'oggetto (`mechanics_5e.oggetti_collegati` di "
        "mostro.schema.json), non l'oggetto stesso."),
    Decisione(
        34, 'categorie-eta',
        "Non tutte le categorie d'età si convertono",
        'Alcune voci del bestiario non danno uno statblock ma una **tabella '
        "di categorie d'età** con DV, CA e capacità propri per riga: il "
        'Tylor ne ha otto, Dragon Amphi e Dragon Sea dodici ciascuno — 32 '
        'schede per tre creature, quasi tutte inutilizzabili in arena. Si '
        "convertono **solo le righe dentro la finestra dell'arena**, "
        'indicativamente GS 1/4-4; le altre restano come dato completo, '
        'disponibili per incontri particolari e antagonisti nelle storie '
        'originali, stesso trattamento dei dati di mondo del gruppo A della '
        'decisione 27 (`sette-campi-2e`). **Il taglio non è a piacere**: in alto lo indica la '
        "fonte con un salto nei propri numeri (sul Tylor l'XP passa da 975 "
        'alla 4ª categoria a 9.000 alla 5ª, fattore nove in un gradino); in '
        'basso lo decide ciò che la tabella tiene fisso, perché un danno '
        "identico su tutte le categorie descrive l'adulto e renderebbe "
        'incoerente il cucciolo — è la stessa regola già ricavata '
        "sull'Hatori Minore, che qui ha retto fuori dal caso che l'aveva "
        'prodotta. Applicata al Tylor: due schede su otto righe, la 3ª e la '
        '4ª categoria, scritte nello stesso giro per graduarle a confronto.'),
    Decisione(
        35, 'repertori-sono-filtri',
        'I repertori rinviati sono filtri, non liste',
        'Quando la fonte rimanda una capacità "a scelta del master", **non '
        'tace: dà il filtro e non il campione**. Il Tayling fissa scuola '
        '(Alterazione) e sfera (Elementale) con banda di livello 1-10; il '
        'Tylor fissa i conteggi di slot e il carattere offensivo; la coppia '
        'accoppiata del Dragon Astral fissa classe e livello. Si modella '
        "quindi come **specifica di filtro**: si registra l'insieme "
        'accessibile secondo i vincoli della fonte, e la scelta concreta '
        "avviene alla generazione dell'incontro. Conseguenza operativa: il "
        'repertorio **non resta `pending` e non è escluso dal calcolo del '
        'Grado di Sfida** — entra come capacità con insieme definito. La '
        'macchina esisteva già: le sfere come filtro di preparazione sono '
        'la decisione 24 (`sfere-sacerdotali`, `dati/_sfere_5e.py`), la scuola è un campo '
        'indicizzato dei 319 incantesimi SRD. Stesso trattamento per i '
        "parametri non magici lasciati aperti, come l'unica resistenza "
        'elementare del Tylor: un parametro risolto alla generazione, non '
        'una moltiplicazione di schede. È più facile nel nostro bersaglio '
        'che a tavolo — la 5e cartacea deve stampare una lista fissa, un '
        "motore software pesca dall'insieme filtrato ogni volta. **Il primo "
        'esito ha già smentito una previsione**: il GS provvisorio del '
        'Tayling era dato in salita verso 3-4, e applicando davvero il '
        'filtro resta 1/2, perché Alterazione ed Elementale selezionano '
        'utilità e controllo, non danno. Un `pending` non è neutro: è una '
        'stima nascosta.'),
    Decisione(
        36, 'age-categories-strutturato',
        'Campo strutturato per le fasce non convertite',
        'Le righe che la decisione 34 (`categorie-eta`) non converte non vanno in '
        '`abilities_text`: la trascrizione in prosa perde la struttura, e '
        'Amphi e Sea arriveranno con dodici righe per una dozzina di '
        'colonne. Campo nuovo in `mostro.schema.json`, '
        '`source_2e.age_categories`, tabellare e interrogabile, '
        'dimensionato per reggere sia le otto righe del Tylor sia le dodici '
        'dei draghi. Dichiara le colonne che **quella** voce usa (il Tylor '
        'non ha soffio, i draghi sì) invece di fissarne un elenco valido '
        'per tutti, e marca `inferita: true` le colonne di cui trascriviamo '
        'i numeri ma interpretiamo il significato — sul Tylor è `Hit Die '
        'Modifier`, che la fonte stampa senza dire se valga per Dado Vita o '
        'sul totale. Ogni scheda derivata porta la tabella intera, non solo '
        'la propria riga. Stessa forma di estensione già fatta per `thac0` '
        "reso nullable sull'Hatori: lo schema si allarga quando una voce "
        'reale lo richiede, non prima.'),
    Decisione(
        37, 'coda-mostri-pubblica',
        '`dati/mostri.coda.json` è pubblico per scelta',
        'Tolto da `PERCORSI` in `git-privato.sh`. Il contenuto è analisi '
        'nostra più valori di statblock — che per il criterio della '
        'decisione sul testo dei manuali sono **fatti, non espressione** — '
        'e le due citazioni brevi rientrano nello standard già accettato. '
        'Il vero problema non era la riservatezza ma il **doppio '
        "tracciamento**: era l'unico file dell'intero progetto tracciato da "
        'entrambi i repository, quindi lo stesso file in due storie che '
        'divergono in silenzio. Riscrivere la storia privata per undici '
        'parole non è proporzionato: si smette di tracciarlo da qui in '
        "avanti. Verifica fatta su tutto l'elenco (`comm -12` fra le due "
        "liste di file tracciati): era l'unico caso, gli altri 25 percorsi "
        'sono coperti dal `.gitignore` pubblico. Il difetto si riforma se '
        'un percorso nuovo entra in `PERCORSI` senza essere escluso dal '
        'pubblico — è la stessa zona morta già vista con `dati/oggetti/`.'),
    Decisione(
        38, 'schema-modelli',
        'I modelli hanno schema proprio',
        '`dati/schema/modello.schema.json`, stesso criterio della '
        'decisione 33 (`schema-oggetti`) sugli oggetti: quando una cosa è applicabile a bersagli diversi '
        'non appartiene a nessuno di loro e prende schema proprio. Un '
        '**modello** non è una creatura — è un pacchetto di regole che si '
        'applica a un **ospite** e descrive quattro cose: cosa **eredita** '
        "dall'ospite, cosa **sovrascrive** con valore proprio, cosa "
        '**aggiunge** di suo, e quale insieme di ospiti è **legale**. Non '
        'poteva stare in `mostro.schema.json`, che pretende CA, punti '
        'ferita e Grado di Sfida: un modello non ha nessuno dei tre finché '
        'non gli si dà un ospite. Tre casi coperti, ed è la loro distanza a '
        'dare la forma allo schema: **Dreamshadow** eredita tutto e non ha '
        'guscio; **Spectral Minion** eredita il solo profilo di '
        'combattimento (Dadi Vita, attacco, danno) e tiene un guscio '
        'proprio (CA 2, colpibile solo da armi +1, resistenza magica 20%); '
        '**Dreamwraith** eredita sei righe — tre delle quali arrivano alla '
        'scheda — con CA e Dadi Vita *dichiarati invarianti dalla fonte*, e '
        'ha perciò anche una scheda di mostro. **Il Dreamwraith è stato il '
        'collaudo**: scritto per primo su una conversione già chiusa, fatta '
        'senza conoscere questo schema, ha retto senza forzarla e ha '
        'prodotto quattro campi che nessuno dei due casi nuovi avrebbe '
        'richiesto — `monster_id` (un modello può avere anche una scheda, e '
        'allora non la duplica), `destinazione` sulle voci ereditate (sei '
        'righe ereditate, tre in scheda e tre al generatore di incontri), '
        '`origine: terzo` (la resistenza magica non viene né dal modello né '
        "dall'ospite ma dal livello del sogno) e la forma `proprio` del "
        'grado. La scheda referenzia il modello con '
        '`mechanics_5e.modelli_collegati`, come già fa con gli oggetti. Il '
        'controllo della decisione 37 (`coda-mostri-pubblica`) sul doppio tracciamento è stato '
        'rifatto con `dati/modelli/` dentro: la cartella è esclusa dal '
        '`.gitignore` pubblico ed elencata in `PERCORSI` nello stesso '
        'commit che ha creato il primo file, come CLAUDE.md prescrive.'),
    Decisione(
        39, 'bersaglio-legale-filtro',
        'Il bersaglio legale è un filtro',
        'Si applica la decisione 35 (`repertori-sono-filtri`) senza aggiungere nulla. La fonte **dà '
        'il filtro e non il campione**: «umano o demiumano morto prima di '
        'aver compiuto un voto» per lo Spectral Minion, «creatura o persona '
        'nota al sognatore o a chiunque stia vivendo il sogno» per il '
        "Dreamshadow. Si registra l'insieme legale — in prosa e in criteri "
        'interrogabili — e la scelta concreta avviene alla generazione. Lo '
        'schema lo rende **strutturale invece che raccomandato**: i campi '
        '`campione` e `scelta_alla_generazione` accettano un solo valore '
        'ciascuno (`null` e `true`), quindi fissare qui un ospite scelto da '
        'noi è impossibile, non solo sconsigliato. Gli ospiti che la fonte '
        'nomina restano registrati a parte come `esempi_dalla_fonte`, che '
        'allargano il campo e non lo restringono.'),
    Decisione(
        40, 'modello-scarto-di-grado',
        'Un modello non ha grado, ha uno scarto',
        'Era la domanda senza precedente, e la risposta è che **il grado '
        "non gli appartiene**. Il Dreamshadow con l'aspetto di un ratto e "
        "quello con l'aspetto di un ogre sono la stessa cosa su bersagli "
        'diversi: assegnargli un Grado di Sfida significherebbe fissare '
        "l'ospite, cioè decidere ciò che la fonte lascia aperto — lo stesso "
        'errore che la decisione 34 (`categorie-eta`) ha evitato moltiplicando le schede per '
        "età. Si registra quindi la **modifica** al grado dell'ospite, non "
        'un valore assoluto, in tre forme che i tre casi hanno prodotto da '
        'soli. **Delta** (Dreamshadow): la fonte stessa ragiona per scarto '
        "— delle ventuno righe del blocco statistiche, `XP VALUE` è l'unica "
        "che non rimanda all'ospite, e ci scrive sopra «+ 10%». Un +10% non "
        'arriva a un quarto del salto più stretto fra due valori XP2e '
        'osservati nel bestiario (1.400 → 2.000, circa +43%): lo scarto di '
        "grado è **0**, ed è un'affermazione, non un'incertezza. **Non "
        'derivabile** (Spectral Minion): i due valori XP2e (975 e 1.400) '
        "restano confrontabili con la tabella del passo 10 e **l'uso è "
        'registrato** — servono a confermare che le sei fasce di '
        'comportamento hanno pesi diversi e che il taglio della fonte è '
        '3+3, non a derivare un grado, perché senza Dadi Vita non ci sono '
        "punti ferita e senza punti ferita non c'è grado. Il confronto dà "
        'anche un secondo motivo indipendente: la riga 975 della tabella è '
        "la più compatta del bestiario (ogni voce convertita con quell'XP è "
        'finita a GS 3), la riga 1.400 è fra le più larghe (GS 1, 2 e 3), '
        'quindi è proprio il valore alto dei due il meno informativo. '
        '**Proprio** (Dreamwraith): la fonte ha già chiuso il modello in '
        'una creatura, il grado è legittimo e abita la scheda. Il campo '
        '`usato_per_derivare_gs: false` obbliga a compilare '
        '`uso_dichiarato`, perché un valore di fonte registrato senza dire '
        'che uso se ne fa è una stima nascosta — la lezione della '
        'decisione 35 (`repertori-sono-filtri`), resa vincolo di schema.'),
    Decisione(
        41, 'sconfessione-condivisa',
        'La sconfessione è una regola condivisa',
        'La procedura di sconfessione delle illusioni (*Disbelieving '
        'Illusions*: quattro passi e una tabella di modificatori di '
        'concentrazione) è condivisa fra Dreamshadow e Dreamwraith, sta '
        'stampata nella voce del secondo, e il primo non si può scrivere '
        'senza. **Vive nel modello, non nelle due schede**: il Dreamwraith '
        'smette di portarla come rinvio aperto e la riferisce. È anche il '
        'motivo migliore per cui lo schema dei modelli deve esistere — è la '
        'prima cosa davvero condivisa fra due creature del bestiario. Si '
        'scrive una volta sola: un modello la porta come `definizione`, gli '
        'altri come `riferimento`, e il validatore rifiuta una seconda '
        'definizione dello stesso id. **Il modello porta un parametro, mai '
        "un valore fisso**: contro il Dreamwraith c'è una penalità di "
        "**−5** che contro il Dreamshadow non c'è, e i due differiscono "
        'anche su un secondo parametro (il Dreamshadow «cannot be '
        'disbelieved into non-existence», quindi sconfessarlo protegge chi '
        "ci riesce ma non lo elimina). Il −5 è stato riletto sull'immagine "
        "di pagina prima di scriverlo: l'OCR di quella voce perde i segni "
        'meno con regolarità, come già accaduto su `NO. APPEARING` e sul '
        "bonus d'iniziativa della stessa creatura. **Sede provvisoria, "
        'dichiarata**: la casa naturale di una regola di sistema è uno '
        'schema di regole che il progetto non ha ancora — lo stesso rinvio '
        'già registrato per il *mindspin* e i Dragon Orbs. Quando esisterà, '
        'la definizione trasloca e tutti i portatori diventano riferimenti: '
        'un blocco solo da spostare, non una riscrittura.'),
    Decisione(
        42, 'cambio-acciaio-oro',
        'Acciaio e oro: due campi, non una conversione',
        'Le fonti dichiarano **due regole distinte** che rispondono a '
        'domande diverse, e vanno registrate come **due campi separati**, '
        'non riconciliate in un numero solo. `cambio_monete` = **40:1** '
        "(un pezzo d'acciaio vale 40 monete d'oro, *Tales of the Lance*): "
        "e' il lore e l'economia interna di Krynn dopo il Cataclisma, dove "
        "l'acciaio e' il metallo scarso e l'oro l'ornamento. "
        '`fattore_listino` = **1:1**: e\' la lettura di un listino '
        'importato, e sei moduli d\'avventura sono concordi nel trattare '
        'il prezzo in oro della fonte come prezzo in acciaio. Due numeri '
        'diversi non sono una contraddizione da sciogliere: **collidono '
        'solo se si confondono i due usi.** E\' il trattamento della '
        'decisione 27 (`sette-campi-2e`) — un dato di fonte si registra con '
        'la **destinazione dichiarata**, mai come valore nudo. '
        'L\'accordo di sei moduli rende l\'1:1 una **regola editoriale '
        'stabile**, non una incoerenza isolata di un singolo modulo. Si '
        'registra anche il terzo numero visto nelle fonti — **10:1** in '
        'DLC2/DLC3 — come **variante nota** e non come errore, insieme alla '
        'clausola del manuale sulle **variazioni regionali** del cambio. '
        'CONSEGUENZA OPERATIVA: i nostri `cost_gp` vengono dall\'SRD 5.1, '
        'cioe\' da un listino importato, quindi si leggono con '
        '`fattore_listino` e **non si fa nessuna aritmetica** sul borsello '
        'iniziale in acciaio. Il 40:1 non entra mai in un prezzo: serve al '
        'tesoro, alla ricompensa e alla descrizione del mondo.'),
    Decisione(
        43, 'barbaro-rimandato',
        'Il Barbaro resta razza: rimandato, non respinto',
        'L\'Umano Barbaro **non si converte a background** adesso. Il '
        'motivo e\' di forma, non di merito: convertirlo richiederebbe uno '
        'schema dei background che il progetto **non ha**, e crearne uno '
        'ora per una razza sola significherebbe progettarlo **su un caso '
        'invece che sui casi** — lo stesso difetto che la '
        'decisione 38 (`schema-modelli`) ha evitato aspettando di avere tre '
        'creature da modellare. I background serviranno davvero con la '
        '**Fase 3**, insieme ai talenti che oggi mancano del tutto: allora '
        'ci sara\' materiale su cui disegnare lo schema, e la questione si '
        'riapre. Fino ad allora il Barbaro resta una voce di `dati/razze/` '
        'con i suoi tetti dichiarati. **La decisione e\' rimandata per '
        'mancanza di uno schema, non respinta nel merito**: '
        'l\'osservazione che il Barbaro sia piu\' un percorso culturale '
        'che una razza resta valida e va ripresa, non archiviata.'),
    Decisione(
        44, 'tetto-punto-perduto',
        'Tetti di crescita: il punto si perde',
        'Un aumento di caratteristica che sfonderebbe il massimale '
        'razziale e\' **perduto**. Non travasato su un\'altra '
        'caratteristica, non convertito in altro, non ammorbidito. E\' la '
        'lettura fedele della fonte — un massimale e\' un tetto, e '
        'sfondarlo non e\' previsto — ed e\' coerente con aver tenuto gli '
        'aggiustamenti negativi e le doppie penalita\' della '
        'decisione 9 (`aggiustamenti-negativi`): il sistema e\' **chiuso**, '
        'le razze di Krynn non si mescolano con quelle del PHB, e conta '
        'solo l\'equilibrio interno. Le alternative rompono ciascuna '
        'qualcosa di dichiarato: il **travaso** premia chi ha i tetti '
        'bassi, cioe\' trasforma una penalita\' in un vantaggio; il **tetto '
        'morbido** annulla la decisione 10 (`massimali-razziali`) invece di '
        'applicarla; la **compensazione con un talento** richiede un '
        'catalogo dei talenti che non esiste. VINCOLO DI INTERFACCIA: il '
        'giocatore deve **vedere il tetto prima di spendere l\'aumento**, '
        'non scoprirlo dopo averlo speso. Il sistema **segnala, non blocca '
        'in silenzio** — stessa forma della '
        'decisione 8 (`generazione-caratteristiche`) sui metodi di '
        'generazione irraggiungibili. Le caratteristiche per cui il manuale '
        '**non dichiara un massimale** non ereditano un tetto razziale: '
        'restano al **20** della 5e.'),
    Decisione(
        45, 'effetto-sul-blocco-mostro',
        'Lo strato strutturato vive sul blocco, anche sul mostro',
        '`effetto` sta accanto alla prosa **dentro il blocco**, e questo '
        'vale sul mostro come sulla classe. Non e\' una scelta nuova — '
        'effetto.schema.json la dichiarava gia\' per le classi — ma sui '
        'mostri non era nemmeno **esprimibile**: `mostro.schema.json` aveva '
        '`additionalProperties: false` su `elemento_5e` e nessun campo '
        '`effetto`, quindi lo strato che il progetto aveva scelto era '
        'vietato proprio dove sta il grosso della meccanica. Scoperto '
        'usando i dati, non ispezionandoli: la prima fetta verticale non '
        'poteva leggere l\'attacco di un mostro perche\' non c\'era dove '
        'scriverlo. **L\'alternativa respinta e\' una cartella '
        '`dati/effetti/`**: ripeterebbe il difetto gia\' visto sette volte '
        'nel progetto — due strutture che dicono la stessa cosa e che '
        'nessuno riconfronta. Qui il riconfronto e\' obbligatorio e '
        'automatico (`dati/valida_effetti.py`, controllo 2), ed e\' il '
        'pezzo che paga il costo del campo. **Non e\' un allargamento**: '
        'dei 9 blocchi dei due mostri della fetta ne hanno `effetto` 5, e '
        'gli altri 50 mostri restano prosa. Si struttura cio\' che un caso '
        'esercita.'),
    Decisione(
        46, 'multiattacco-riferisce',
        'Il multiattacco riferisce, non ricopia',
        'Il blocco *Attacchi Multipli* prende un campo suo, `multiattacco`, '
        'che dice **quante volte** si ripete **quale altra azione dello '
        'stesso statblock** — per nome, senza ricopiarne i numeri. Prima '
        'non aveva nessun campo: la sua unica forma era la frase «effettua '
        'due attacchi con X», e un motore che la ignori **dimezza il danno '
        'per round** di ogni mostro che ce l\'ha, senza che nessun '
        'controllo se ne accorga. Sono 18 blocchi su 128 azioni del '
        'bestiario, quindi non e\' un caso isolato. **Riferimento e non '
        'copia** per la stessa ragione della '
        'decisione 41 (`sconfessione-condivisa`): i numeri dell\'attacco '
        'hanno una sede sola, l\'azione riferita. `valida_effetti.py` '
        'verifica che il nome riferito esista davvero nello stesso '
        'statblock — un rimando che non risolve e\' peggio di una copia.'),
    Decisione(
        47, 'salvezza-a-due-tempi',
        'Un tiro salvezza ripetuto puo\' peggiorare, e allora ha un campo',
        '`tiro_salvezza.fallimento_ripetuto` registra l\'esito del secondo '
        'fallimento **dove e\' diverso dal primo**. Lo schema aveva gia\' '
        '`ripetibile`, che dice **quando** si ritira e non **cosa '
        'succede**: il Death Throes del Baaz e\' a due tempi — il primo '
        'fallimento trattiene mentre la pietrificazione comincia, il '
        'secondo la compie — e senza il campo nuovo le sue due condizioni '
        'diventano una sola, cioe\' il tratto perde meta\' di se\' senza '
        'che nessun controllo lo veda. **Campo facoltativo**: si scrive '
        'solo dove `ripetibile` c\'e\' e il secondo tempo differisce dal '
        'primo, altrimenti sarebbe una ripetizione. Il campo ha portato con '
        'se\' un punto cieco, chiuso nello stesso giro: '
        '`condizioni_citate()` non lo guardava, quindi la condizione del '
        'secondo tempo non sarebbe mai stata controllata.'),
    Decisione(
        48, 'condizioni-a-consumo',
        'Le condizioni si aggiungono quando un blocco le riferisce',
        'Il criterio era gia\' scritto in `dati/build_condizioni.py` e '
        'questa e\' la prima volta che **si applica** invece di essere '
        'enunciato: `trattenuto` e `pietrificato` sono nate perche\' il '
        'Death Throes del Baaz le riferisce davvero, non perche\' '
        'l\'appendice della 5e ne elenca quindici. Sono **cinque, non '
        'quindici**, e il numero e\' il punto: una cartella riempita per '
        'anticipazione e\' una cartella di dati che nessun caso ha mai '
        'messo alla prova. Le **sei clausole nuove** di '
        '`condizione.schema.json` sono parte della stessa decisione e non '
        'una decisione a parte: sono esattamente quelle che le due '
        'condizioni richiedevano, e nessuna in piu\'. `pietrificato` ha '
        'portato con se\' una domanda che nessun dato dichiarava — una '
        'creatura pietrificata **non e\' morta**, ha ancora i suoi punti '
        'ferita — e che ha costretto a riscrivere la condizione di fine '
        'scontro nel motore. E\' il segno che il criterio funziona: una '
        'condizione aggiunta a consumo porta con se\' il caso che la '
        'giustifica.'),
    Decisione(
        49, 'vocabolario-italiano',
        'I vocabolari condivisi hanno una sede sola, e la lingua e\' l\'italiano',
        'Un termine che compare in **due schemi** e che un motore deve '
        'confrontare non e\' una convenzione: e\' una struttura doppia in '
        'attesa di sfasarsi. L\'ottava del progetto sono stati i **tipi di '
        'danno** — `dati/oggetti/` diceva `slashing` (inglese, dall\'SRD) e '
        '`dati/mostri/` diceva `perforante`, nessuno dei due schemi li '
        'vincolava e **nessuno dei due era sbagliato dal proprio lato**, '
        'quindi nessun validatore poteva vederlo. Trovata **usando** i '
        'dati, non ispezionandoli: un motore che confronti il danno di '
        'un\'arma con la resistenza di un mostro li manca tutti. '
        'SEDE: `dati/schema/vocabolari.schema.json`, riferito con `$ref` '
        'dagli schemi che lo usano — **mai ricopiato**, perche\' un enum '
        'duplicato in tre schemi sarebbe una struttura doppia nuova, creata '
        'mentre si chiude l\'ottava. Il codice Python non lo ridigita: '
        '`dati/_vocabolari.py` legge quel file. '
        'LINGUA: **italiano**, e non per gusto. Ogni altro enum che il '
        'progetto possiede nello strato `mechanics_5e` e\' gia\' italiano '
        '(`mischia_arma`, `da_guerra`, `leggera`, `riposo_breve`, gli id di '
        '`dati/condizioni/`), e `mechanics_5e` e\' lo **strato nostro** '
        'della decisione 7 (`doppio-strato`): l\'inglese li\' dentro non '
        'era una scelta, era una stringa di fonte che `build_oggetti.py` '
        'copiava senza tradurre. La traduzione avviene **nel generatore**, '
        'una volta sola (CLAUDE.md 2), e l\'originale inglese resta dov\'e\' '
        'la fonte, in `dati/_fonti/srd51_equipaggiamento.py`. '
        'CONSEGUENZA CHE NON ERA UN ENUM: dal lato del mostro le '
        'resistenze non erano un vocabolario ma **prosa** — «bludgeoning, '
        'piercing, and slashing from nonmagical attacks» era **un** '
        'elemento di un array di stringhe. Vincolare solo la lingua avrebbe '
        'lasciato il confronto impossibile per forma invece che per lingua, '
        'quindi `damage_resistances`, `damage_immunities` e '
        '`damage_vulnerabilities` diventano voci `{tipo, solo_se}` e la '
        'clausola e\' anch\'essa un enum. '
        'NON CHIUSE, E DICHIARATE TALI: `condition_immunities` porta i nomi '
        'delle condizioni in inglese mentre `dati/condizioni/` li ha in '
        'italiano — stesso difetto, e chiuderlo obbliga a scegliere fra due '
        'strade che riguardano la decisione 48 (`condizioni-a-consumo`), '
        'quindi e\' una decisione a se\'. Misura e alternative in '
        '`dati/RAPPORTO-vocabolari.md`.'),
    Decisione(
        50, 'cd-origine-dichiarata',
        'Da dove viene una CD si dichiara, la derivabilita\' si calcola',
        'Un campo con due significati e\' inaffidabile da entrambi i lati, '
        'e `cd_derivata_da` ne aveva due: la sua descrizione diceva «come '
        'la CD e\' stata ottenuta, **quando non e\' un dato di fonte**», '
        'mentre il controllo 5 di `valida_effetti.py` pretendeva di '
        'riempirlo proprio per una CD **di fonte** non derivabile. Al suo '
        'posto due campi: **`cd_origine`** (`fonte` | `derivata` | '
        '`stimata`), obbligatorio ovunque ci sia una CD, e '
        '**`cd_derivazione`**, la prosa breve che dice da quale blocco e\' '
        'letta, con quale caratteristica torna il conto, o su quale '
        'precedente e\' stata stimata. La **derivabilita\' non e\' un '
        'campo**: e\' calcolabile, e il controllo la calcola invece di '
        'credere a cio\' che il dato ne afferma. '
        'IL CASO CHE LO DIMOSTRA. La CD 11 del Death Throes del Baaz e\' '
        'stampata nel blocco ufficiale SotDQ, e **combacia col conto**: 8 + '
        'il bonus di competenza + il modificatore di Costituzione del Baaz '
        'da\' esattamente 11, e proprio sulla caratteristica del tiro. Il '
        'vecchio controllo '
        'quindi **non l\'avrebbe mai segnalata** — non perche\' fosse a '
        'posto, ma perche\' una CD letta e una CD derivata erano '
        'indistinguibili quando i numeri coincidono. `cd_origine` registra '
        'che la coincidenza e\' una coincidenza. Il controllo la conta e '
        'non la segnala: sapere quante CD di fonte tornano col conto dice '
        'quanto vale il conto come prova, e la risposta e\' poco.'),
    Decisione(
        51, 'criterio-meccanica',
        'Dove vive la meccanica: tre domande, e la prima che risponde decide',
        'Il criterio, in ordine: **1)** varia da portatore a portatore? '
        '\u2192 **dato di contenuto** (il danno di un\'arma, la CD di un '
        'tiro salvezza, **quando un tratto scatta**). **2)** non varia: e\' '
        'un valore o una procedura? Un **valore o una tabella che la fonte '
        'stampa** e\' un **dato di sistema** e vive in `dati/sistema/`; una '
        '**procedura** \u2014 tira, confronta, applica, passa il turno \u2014 '
        'e\' **codice**. **3)** e\' una procedura: i nomi che pronuncia '
        'vengono da un vocabolario condiviso, mai da stringhe scritte nel '
        'codice (decisione 49, `vocabolario-italiano`, anche quando il '
        'consumatore e\' il motore invece di uno schema). '
        'CIO\' CHE LO HA IMPOSTO. La **nona struttura doppia** del '
        'progetto, e la prima che vive nel **codice** invece che nei dati: '
        'il modificatore di caratteristica scritto in `valida_effetti.py` e '
        'in `motore/combattimento.py`, il bonus di competenza in '
        '`_srd51.py` e in `valida_effetti.py`. Formule identiche in file '
        'che nessuna esecuzione metteva uno contro l\'altro. Le otto '
        'precedenti erano fra file di dati, dove arrivano schemi e '
        'validatori; qui non arrivava niente. '
        'SEDE: `dati/sistema/`, con `sistema.schema.json` e cinque dati \u2014 '
        'modificatore di caratteristica, bonus di competenza (per livello '
        '**e** per grado sfida, che sono due **letture** della stessa '
        'tabella e non due tabelle), formula della CD, moltiplicatori di '
        'resistenza/vulnerabilita\'/immunita\' con il loro **ordine di '
        'applicazione**, soglie del 20 e dell\'1 naturale. `dati/_sistema.py` '
        'le legge e non le ridigita, come `_vocabolari.py` fa con i '
        'vocabolari. '
        'LA PARTE CHE CONTA PIU\' DELLE TABELLE. Una sede non chiude niente '
        'da sola: chiude solo se qualcosa impedisce che la tabella venga '
        'riscritta altrove. `dati/valida_sistema.py` e\' il **primo '
        'controllo del progetto che guarda il codice** invece dei dati: '
        'rifiuta la stessa tabella riscritta **per forma** (l\'espressione, '
        'perche\' una formula ricopiata cambia nome e non forma) e **per '
        'valori** (la tabella espansa a mano). Legge il codice e non la '
        'prosa \u2014 tokenizza e scarta stringhe e commenti \u2014 perche\' '
        'un rapporto che DESCRIVE la formula fa il suo mestiere, e un '
        'controllo che grida al lupo viene spento. Si mette alla prova a '
        'ogni giro su copie piantate apposta e su sorgenti che somigliano a '
        'una copia senza esserlo: su un repository pulito un rilevatore '
        'rotto e uno funzionante tacciono uguale. **UN\'ECCEZIONE, '
        'dichiarata**: la sonda che ricalcola la tabella con la formula '
        'stampata dalla fonte e la confronta riga per riga \u2014 un '
        'riconfronto, non una copia, ed e\' cio\' che verifica trenta righe '
        'battute a mano. Un\'eccezione dichiarata e non piu\' trovata e\' '
        'segnalata come una copia. '
        'COSA IL CONTROLLO NON VEDE, scritto in `_sistema.LIMITI` e non solo '
        'in un rapporto: una riscrittura algebrica, un\'altra lingua (un '
        'domani il lato web), la prosa, un derivato **precalcolato nei '
        'dati**, e una tabella copiata sotto la soglia di dieci valori.'),
    Decisione(
        52, 'attacco-unica-lettura',
        'Cio\' che il mostro e il personaggio condividono non e\' il campo, e\' la lettura',
        '`attacco` era un **campo** sul mostro e una **funzione** sul '
        'personaggio: due cose diverse con lo stesso nome, ed e\' la lacuna '
        'che il primo scontro ha reso visibile. Le due strade ovvie '
        'rompevano ciascuna qualcosa di gia\' deciso \u2014 far memorizzare '
        'l\'attacco al personaggio e\' un derivato scritto a mano '
        '(decisione 7, `doppio-strato`, e CLAUDE.md 3), far derivare '
        'l\'attacco al mostro e\' inventare derivazioni che la fonte non '
        'da\' (decisione 50, `cd-origine-dichiarata`). '
        'SOLUZIONE: **una sola LETTURA**, `attacco_di(combattente)`, che '
        'torna la forma `effetto.attacco` gia\' definita \u2014 sul mostro la '
        'legge, sul personaggio la compone da arma, caratteristica, '
        'competenza e stile. Chi la chiama non sa quale dei due casi ha '
        'davanti, ed e\' questo il senso di «la stessa cosa da entrambe le '
        'parti»: anche la scelta di quale azione sia un attacco passa da li\' '
        'e non dal campo, perche\' sul personaggio quel campo non esiste. '
        'IL PERSONAGGIO PORTA SOLO GLI INGRESSI: razza, classe, livello, '
        'punteggi, equipaggiato, scelte. Ogni campo ricavabile da questi '
        '**non puo\'** esistere \u2014 il costruttore solleva, che e\' la forma '
        'piu\' forte del divieto, la stessa con cui la '
        'decisione 39 (`bersaglio-legale-filtro`) ha reso impossibile e '
        'non solo '
        'sconsigliato fissare un ospite. '
        'CIO\' CHE APRE. Un `bonus_colpire` **letto** dalla scheda e uno '
        '**rifatto col conto** si scrivono identici: manca un '
        '`bonus_origine`, esattamente come mancava `cd_origine` prima della '
        'decisione 50 (`cd-origine-dichiarata`). Misurato invece che supposto \u2014 misura al '
        '02/09/2026: dei 94 bonus di attacco che il bestiario scrive in '
        'prosa, 85 tornano col conto e 9 no, quindi la coincidenza non e\' '
        'una conferma. `motore/arena.py` la riconta a ogni giro, cosi\' il '
        'numero non invecchia in silenzio.'),
    Decisione(
        53, 'condizioni-vocabolario-srd',
        'Il vocabolario nomina tutte le condizioni SRD; il catalogo ne converte alcune',
        '`dati/mostri/` dichiarava le immunita\' a condizione con i nomi '
        'inglesi della 5e mentre `dati/condizioni/` \u2014 sede unica per la '
        'decisione 48 (`condizioni-a-consumo`) \u2014 ha id italiani. Stesso '
        'difetto dei tipi di danno, **piu\' grave**: li\' erano due '
        'trascrizioni, qui una delle due sedi era gia\' **dichiarata unica** '
        'e l\'altra la ignorava, quindi nessuna immunita\' del bestiario '
        'poteva essere rispettata da nessun motore. '
        'PERCHE\' NON BASTAVA TRADURRE. Delle condizioni citate dalle '
        'immunita\' solo tre esistevano nel catalogo: tradurre e basta '
        'avrebbe prodotto sette riferimenti che non risolvono, e crearle per '
        'anticipazione avrebbe sconfessato la '
        'decisione 48 (`condizioni-a-consumo`) tre giorni dopo '
        'averla presa. Restringere l\'enum alle esistenti era peggio: le '
        'schede perdevano informazione vera di fonte. '
        'SOLUZIONE, ed e\' la strada della '
        'decisione 35 (`repertori-sono-filtri`): l\'insieme delle condizioni SRD e\' '
        '**chiuso e noto**, quindi il vocabolario e\' **completo** \u2014 '
        'quindici termini in `vocabolari.schema.json`, riferiti per `$ref` da '
        '`mostro.schema.json` \u2014 mentre il catalogo ne converte cinque. Le '
        'altre dieci non sono condizioni **inesistenti**: sono una **lacuna '
        'del nostro catalogo**, che e\' cosa diversa. '
        'IL DIVARIO NON SI SCRIVE, SI DERIVA: quali siano modellate lo dice '
        'la cartella (`_vocabolari.condizioni_modellate()`), perche\' un '
        'elenco a mano accanto a una cartella sarebbe una struttura doppia '
        'nuova creata mentre se ne chiude un\'altra. '
        'IL MOTORE DEVE SAPERLO. Un\'immunita\' a una condizione che il '
        'catalogo non modella viene **dichiarata** come lacuna '
        '(`condizione-non-modellata`) e non ignorata in silenzio: ignorata, '
        'sarebbe indistinguibile da un\'immunita\' rispettata. Misura al '
        '02/09/2026: 35 immunita\' su 11 schede, di cui 29 nominano una '
        'condizione che il motore non sa ancora applicare. '
        'La traduzione dall\'SRD ha una sede sola '
        '(`_vocabolari.CONDIZIONE_DA_SRD`), con l\'invariante verificata '
        'all\'import: ogni id prodotto sta nell\'enum, e ogni voce dell\'enum '
        'ha un termine inglese che ci arriva.'),
]

PER_ID = {d.id: d for d in DECISIONI}
PER_NUMERO = {d.numero: d for d in DECISIONI}

# Invarianti del registro, verificate all'import: un id duplicato o un buco
# nella numerazione romperebbe in silenzio ogni rimando che ci si appoggia.
assert len(PER_ID) == len(DECISIONI), "id duplicato fra le decisioni"
assert [d.numero for d in DECISIONI] == list(range(1, len(DECISIONI) + 1)), \
    "la numerazione deve essere contigua e partire da 1"


def cita(id_decisione):
    """Il rimando in forma canonica, con il numero derivato dal registro."""
    return f"decisione {PER_ID[id_decisione].numero} (`{id_decisione}`)"
