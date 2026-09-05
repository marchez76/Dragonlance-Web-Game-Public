# Dragonlance Web GDR — contesto di progetto

*Generato da `genera_contesto.py` il 2026-09-05.*

> **Come leggere questo documento.** Ogni numero, tabella e percentuale è
> **derivato dai JSON** al momento della generazione: se un dato cambia, cambia
> anche qui. Le letture e le conclusioni sono invece scritte a mano e marcate
> con un blocco citato e datato. Dove una frase interpretativa contiene un
> numero, quel numero è comunque interpolato dai dati.
>
> **Questo file è una fotografia.** La project knowledge non si sincronizza con
> la cartella di lavoro: quando i dati cambiano va rigenerato e **ricaricato a
> mano**, sostituendo la copia precedente.

---

## Stato

**Libreria**: 101/141 manuali estratti (72%), 14.017 pagine, 61.499.879 caratteri. Restano 22 scansioni in coda OCR e 18 manuali non ancora lavorati.

**Dati strutturati**: 15 razze, 20 classi, 21 divinità, validate a zero errori. 105 tratti razziali, 0 in sospeso, 3 di conversione editoriale nostra.

---

## Le 59 decisioni prese

Ordine cronologico. Questa è la storia completa delle scelte: non serve
ricostruirla dalle sezioni.

1. **Motore** — 5e come chassis meccanico; le altre edizioni sono fonte di contenuto e lore.
2. **Edizione di riferimento** — PHB **2014**, non 2024. La 2024 rende le specie numericamente neutre, incompatibile con la decisione 3 (`vincoli-caratteristica`).
3. **Vincoli di caratteristica** — Minimi, massimali razziali e classi precluse sono regole **meccaniche** applicate in creazione PG, non affidate alla narrazione.
4. **Limiti di livello per demiumani** — **Non si applicano.** Restano in `source_2e` come dato di fonte, con `level_limits.applied` a `false` e nota esplicita.
5. **Cavalieri di Solamnia** — Sequenza obbligata Corona → Spada → Rosa, senza azzeramento dell'esperienza e senza tetti.
6. **Maghi delle Torri** — NON classe standalone dal 1° livello: il giuramento alla Veste avviene al Test, al 3°. Le tre Vesti sono affiliazioni, non classi.
7. **Schema a doppio strato** — `source_2e` fedele al manuale e immutabile, `mechanics_5e` rivedibile. I JSON sono generati da `build_*.py`.
8. **Generazione delle caratteristiche** — Default **4d6 scarta il minore**; array standard e point-buy restano alternative. Se il metodo scelto rende irraggiungibile una combinazione, il sistema segnala e propone il tiro senza bloccare. L'Aghar usa i dadi propri del manuale.
9. **Aggiustamenti negativi** — Si tengono, trascritti fedelmente, doppia penalità inclusa. Il sistema è chiuso: conta solo l'equilibrio interno.
10. **Massimali razziali** — Si tengono tutti, applicati sia in creazione sia come **tetti di crescita**. Non sono i limiti di livello.
11. **Barbaro, vincoli** — Vale l'**unione** dei due set: massimali della scheda razziale più minimi della voce di classe.
12. **`valid_eras`** — Strato editoriale nostro, non dato di fonte. Due sole restrizioni applicate: Irda e Ordini Sacri con le divinità.
13. **Taglia** — Dedotta dall'altezza, la 2e non assegna categorie. Il Minotauro resta **Medium**: in 5e anche il Golia a 7-8 piedi è Medium.
14. **Infravisione** — Dove il manuale la dichiara si converte in scurovisione; dove tace resta **assente per scelta**, non per dimenticanza.
15. **Tratti, trascrizione integrale** — Ogni tratto della voce 2e va in `mechanics_5e` con uno stato di conversione: `direct`, `adapted`, `pending`, `source_only`. Non si inventa meccanica 5e.
16. **I nove tratti del PHB 2e** — Dove il PHB 2014 ha già un equivalente si copia quello; dove la 5e ha eliminato un tratto si ripristina dalla 2e, malus inclusi. La fedeltà alla fonte prevale sulla convenzione 5e.
17. **I tredici pending di Krynn** — Tutti convertiti. *Schernire* è marcato **provvisorio** in attesa di Shadow of the Dragon Queen; la *Specializzazione nelle armi* del Minotauro resta `source_only` perché la fonte concede un permesso, non un beneficio.
18. **Minotauro e Irda dall'Appendice** — Il capitolo razziale è avaro su queste due voci: si integra da `MC - Dragonlance Appendix` solo ciò che l'Appendice **dichiara**, con fonte marcata distintamente.
19. **Compensazione dell'umano** — L'umano aveva zero tratti e zero aggiustamenti perché in 2e era pagato dall'assenza di limiti di livello, che la decisione 4 (`limiti-di-livello`) ha abolito. Compensato con +1 a due caratteristiche a scelta, una competenza e un linguaggio, marcati come conversione editoriale.
20. **Tappo al Barbaro** — +1 fissi a Forza e Costituzione, editoriali e reversibili. **Tappo, non soluzione**: la conversione a background resta la strada giusta e va decisa con lo schema Personaggio.
21. **I tre elfi terrestri** — Applicato il metodo della 18 alle tre voci dedicate dell'Appendice (pagg. 33-35). Esito parziale: due su tre hanno una capacità dichiarata, il Qualinesti nessuna.
22. **Il tratto fantasma del Qualinesti** — Il segnaposto che registrava l'assenza è **rimosso**: non concedeva nulla ma contava nei totali, falsando ogni statistica a valle. L'informazione è passata fra le ambiguità di fonte, dove stanno le altre registrazioni dello stesso tipo.
23. **Il principio del clone** — Per le classi la fedeltà alla fonte non basta: le razze 2e sono ricche, le classi 2e sono povere e trascriverle produce gusci vuoti. Ogni classe di Krynn è un **clone meccanico** della classe base 5e corrispondente (SRD 5.1), con innestati sopra i privilegi e le restrizioni della fonte. Cinque classi restano senza chassis, per decisione.
24. **Sfere sacerdotali** — Si tengono nella forma fedele: le **sfere** filtrano quali incantesimi il chierico può preparare, ripristinando la negazione d'accesso; il **Dominio** 5e resta come sottoclasse per i privilegi di livello. Ogni divinità è associata al Dominio 2014 più coerente.
25. **Lo statuto di SotDQ** — *Shadow of the Dragon Queen* è materiale ufficiale 5e su Krynn: **quinta provenienza** nel campo fonte dei tratti di `mechanics_5e`, non un terzo strato. Non è autoritativo su tutto, perché non è la conversione ufficiale del materiale 2e ma un prodotto scritto da zero che ne condivide i nomi. Prevale su *Schernire*; altrove divergiamo, e le divergenze sono registrate.
26. **Il criterio della tracciabilità** — **Qualsiasi materiale esterno che non porti con sé fonte e pagina è inutilizzabile**, a prescindere dal resto della sua qualità. Tutto il progetto si regge sulla tracciabilità: un dato non verificabile non entra. È un filtro che si applica in trenta secondi e risparmia analisi lunghe. Entrambi i lotti in `import/` sono respinti e chiusi.
27. **I sette campi 2e senza corrispettivo** — Non erano un problema unico. **Gruppo A** — frequenza, numero, organizzazione, ciclo, dieta: dati di mondo, non di scheda, e diventano input del generatore di incontri in Fase 3. **Gruppo B** — il morale non è un campo ma un parametro di comportamento: senza, ogni scontro finisce con tutti i nemici morti, e diventa input dell'IA in arena. **Gruppo C** — la resistenza magica è l'unica vera decisione ed è **rinviata alla Fase 2**, perché i Gradi di Sfida su cui calibriamo presuppongono che non ci sia.
28. **Ogre e Orughi sono mostri** — La voce `Ogre (of Krynn)` dell'Appendice torna a categoria **creatura**, non `razza_altra`. L'asimmetria con Theiwar/Zakhar (clan nanici che il manuale riserva ai PNG giocabili) non regge per gli ogre comuni: non sono un clan riservato, sono avversari classici e servono all'arena. La parentela dichiarata con l'Irda resta nota di lore nella voce, non criterio di categoria. Vale il criterio della porta aperta: un mostro può sempre diventare razza in seguito, il contrario è più fastidioso.
29. **Il Traag usa armi manufatte** — Segue il precedente ufficiale dei cinque draconici, che sostituiscono sistematicamente le armi naturali con armi manufatte (Baaz spada corta, Bozak tridente, Kapak pugnale, Sivak spada seghettata; solo l'Aurak conserva un attacco naturale). Il Traag riceve una **lancia**, scelta per coerenza con la fonte (tribù povere, non soldati regolari; il testo cita esplicitamente la reach fra i vantaggi di usare un'arma) e marcata `adapted` con provenienza editoriale, non di fonte 2e. Il Multiattacco diventa non ambiguo: due attacchi di lancia, non artigli **o** arma.
30. **Precedenza fra Tales of the Lance e MC Appendix** — Prima volta che due fonti 2e si contraddicono su un tratto di personaggio giocante: dove **divergono**, prevale **Tales of the Lance**, perché è il capitolo dedicato ai PG mentre l'Appendice descrive la creatura dal punto di vista del Dungeon Master. Il criterio vale solo per la divergenza, non per l'integrazione: dove l'Appendice dichiara qualcosa su cui Tales of the Lance tace, la decisione 18 (`minotauro-irda-appendice`) resta intatta. Applicata ai due casi kender in conflitto (bonus armi da tiro, condizione sulla Sorpresa): entrambi restano registrati come divergenza e non si applicano.
31. **Soglia degli incantesimi innati dei Dargonesti** — **Opzione C**: tre soglie scalate (3°, 5°, 7°) invece del 10° unico della fonte o di una soglia bassa unica. Il 10° livello 2e non era "tardi" — era metà carriera in un sistema che arrivava al 20° e oltre: copiarlo senza riscalarlo tradisce la sostanza pur conservando la cifra, lo stesso errore già segnalato per i valori XP del bestiario. Concentrare i tre incantesimi in un'unica soglia bassa perderebbe la gradualità che la fonte aveva scelto. Le tre soglie, leggermente più tarde del tiefling PHB 2014 (1°/3°/5°) per conservare lo scarto di "metà carriera" dentro la fascia giocabile, rientrano comunque nella decisione 16 (`nove-tratti-phb2e`): dove la 5e ha già un equivalente per i tratti razziali con incantesimi, si copia quel modello. Il 10° livello della fonte resta intatto in `source_2e`, non riscritto.
32. **Creatura contro entità nel bestiario** — **Riformulata** dopo un primo tentativo scorretto (che confondeva "legato a un oggetto" con "unico"). Il criterio è: ha un **nome proprio e una storia** → entità (es. il Cavaliere della Morte è, nella tradizione del setting, un individuo particolare — ma la voce dell'Appendice stessa descrive un **tipo** ripetibile, "a Knight of Solamnia, cursed...", non un nome). È un **tipo/procedura ripetibile**, anche se potente e vincolato a un oggetto magico → creatura, si converte come le altre al suo vero grado di sfida. Il Warrior Skeleton (uno stregone lega l'anima di un guerriero potente a un diadema: procedura ripetibile, diademi e guerrieri diversi) è quindi una creatura, non un'entità unica. Il diadema di controllo non va rimandato alla Fase 3: è materiale da arena giocabile (raggio, condizione di perdita, inseguimento a velocità doppia), non colore descrittivo. La categoria entità resta per ora **vuota**: nessuna delle 62 voci lette ci è ricaduta, il criterio ha retto respingendo l'unica candidata.
33. **Schema oggetti a parte** — `dati/schema/oggetto.schema.json`, stessa architettura a doppio strato di razze/classi/mostri. Il diadema dello Scheletro Guerriero non poteva restare dentro il mostro: è riutilizzabile su guerrieri diversi (decisione 32, `creatura-contro-entita`), quindi appartiene a sé quanto una spada appartiene a chi la impugna. Lo schema copre tre casi, non uno: equipaggiamento ordinario (armi/armature/attrezzatura — il buco più urgente per l'arena, dove oggi mancano perfino i danni di una spada lunga), oggetti magici, e oggetti con una creatura legata. Il diadema è il primo caso concreto, non il modello: gli altri due casi restano da popolare. Nel mostro resta un riferimento all'oggetto (`mechanics_5e.oggetti_collegati` di mostro.schema.json), non l'oggetto stesso.
34. **Non tutte le categorie d'età si convertono** — Alcune voci del bestiario non danno uno statblock ma una **tabella di categorie d'età** con DV, CA e capacità propri per riga: il Tylor ne ha otto, Dragon Amphi e Dragon Sea dodici ciascuno — 32 schede per tre creature, quasi tutte inutilizzabili in arena. Si convertono **solo le righe dentro la finestra dell'arena**, indicativamente GS 1/4-4; le altre restano come dato completo, disponibili per incontri particolari e antagonisti nelle storie originali, stesso trattamento dei dati di mondo del gruppo A della decisione 27 (`sette-campi-2e`). **Il taglio non è a piacere**: in alto lo indica la fonte con un salto nei propri numeri (sul Tylor l'XP passa da 975 alla 4ª categoria a 9.000 alla 5ª, fattore nove in un gradino); in basso lo decide ciò che la tabella tiene fisso, perché un danno identico su tutte le categorie descrive l'adulto e renderebbe incoerente il cucciolo — è la stessa regola già ricavata sull'Hatori Minore, che qui ha retto fuori dal caso che l'aveva prodotta. Applicata al Tylor: due schede su otto righe, la 3ª e la 4ª categoria, scritte nello stesso giro per graduarle a confronto.
35. **I repertori rinviati sono filtri, non liste** — Quando la fonte rimanda una capacità "a scelta del master", **non tace: dà il filtro e non il campione**. Il Tayling fissa scuola (Alterazione) e sfera (Elementale) con banda di livello 1-10; il Tylor fissa i conteggi di slot e il carattere offensivo; la coppia accoppiata del Dragon Astral fissa classe e livello. Si modella quindi come **specifica di filtro**: si registra l'insieme accessibile secondo i vincoli della fonte, e la scelta concreta avviene alla generazione dell'incontro. Conseguenza operativa: il repertorio **non resta `pending` e non è escluso dal calcolo del Grado di Sfida** — entra come capacità con insieme definito. La macchina esisteva già: le sfere come filtro di preparazione sono la decisione 24 (`sfere-sacerdotali`, `dati/_sfere_5e.py`), la scuola è un campo indicizzato dei 319 incantesimi SRD. Stesso trattamento per i parametri non magici lasciati aperti, come l'unica resistenza elementare del Tylor: un parametro risolto alla generazione, non una moltiplicazione di schede. È più facile nel nostro bersaglio che a tavolo — la 5e cartacea deve stampare una lista fissa, un motore software pesca dall'insieme filtrato ogni volta. **Il primo esito ha già smentito una previsione**: il GS provvisorio del Tayling era dato in salita verso 3-4, e applicando davvero il filtro resta 1/2, perché Alterazione ed Elementale selezionano utilità e controllo, non danno. Un `pending` non è neutro: è una stima nascosta.
36. **Campo strutturato per le fasce non convertite** — Le righe che la decisione 34 (`categorie-eta`) non converte non vanno in `abilities_text`: la trascrizione in prosa perde la struttura, e Amphi e Sea arriveranno con dodici righe per una dozzina di colonne. Campo nuovo in `mostro.schema.json`, `source_2e.age_categories`, tabellare e interrogabile, dimensionato per reggere sia le otto righe del Tylor sia le dodici dei draghi. Dichiara le colonne che **quella** voce usa (il Tylor non ha soffio, i draghi sì) invece di fissarne un elenco valido per tutti, e marca `inferita: true` le colonne di cui trascriviamo i numeri ma interpretiamo il significato — sul Tylor è `Hit Die Modifier`, che la fonte stampa senza dire se valga per Dado Vita o sul totale. Ogni scheda derivata porta la tabella intera, non solo la propria riga. Stessa forma di estensione già fatta per `thac0` reso nullable sull'Hatori: lo schema si allarga quando una voce reale lo richiede, non prima.
37. **`dati/mostri.coda.json` è pubblico per scelta** — Tolto da `PERCORSI` in `git-privato.sh`. Il contenuto è analisi nostra più valori di statblock — che per il criterio della decisione sul testo dei manuali sono **fatti, non espressione** — e le due citazioni brevi rientrano nello standard già accettato. Il vero problema non era la riservatezza ma il **doppio tracciamento**: era l'unico file dell'intero progetto tracciato da entrambi i repository, quindi lo stesso file in due storie che divergono in silenzio. Riscrivere la storia privata per undici parole non è proporzionato: si smette di tracciarlo da qui in avanti. Verifica fatta su tutto l'elenco (`comm -12` fra le due liste di file tracciati): era l'unico caso, gli altri 25 percorsi sono coperti dal `.gitignore` pubblico. Il difetto si riforma se un percorso nuovo entra in `PERCORSI` senza essere escluso dal pubblico — è la stessa zona morta già vista con `dati/oggetti/`.
38. **I modelli hanno schema proprio** — `dati/schema/modello.schema.json`, stesso criterio della decisione 33 (`schema-oggetti`) sugli oggetti: quando una cosa è applicabile a bersagli diversi non appartiene a nessuno di loro e prende schema proprio. Un **modello** non è una creatura — è un pacchetto di regole che si applica a un **ospite** e descrive quattro cose: cosa **eredita** dall'ospite, cosa **sovrascrive** con valore proprio, cosa **aggiunge** di suo, e quale insieme di ospiti è **legale**. Non poteva stare in `mostro.schema.json`, che pretende CA, punti ferita e Grado di Sfida: un modello non ha nessuno dei tre finché non gli si dà un ospite. Tre casi coperti, ed è la loro distanza a dare la forma allo schema: **Dreamshadow** eredita tutto e non ha guscio; **Spectral Minion** eredita il solo profilo di combattimento (Dadi Vita, attacco, danno) e tiene un guscio proprio (CA 2, colpibile solo da armi +1, resistenza magica 20%); **Dreamwraith** eredita sei righe — tre delle quali arrivano alla scheda — con CA e Dadi Vita *dichiarati invarianti dalla fonte*, e ha perciò anche una scheda di mostro. **Il Dreamwraith è stato il collaudo**: scritto per primo su una conversione già chiusa, fatta senza conoscere questo schema, ha retto senza forzarla e ha prodotto quattro campi che nessuno dei due casi nuovi avrebbe richiesto — `monster_id` (un modello può avere anche una scheda, e allora non la duplica), `destinazione` sulle voci ereditate (sei righe ereditate, tre in scheda e tre al generatore di incontri), `origine: terzo` (la resistenza magica non viene né dal modello né dall'ospite ma dal livello del sogno) e la forma `proprio` del grado. La scheda referenzia il modello con `mechanics_5e.modelli_collegati`, come già fa con gli oggetti. Il controllo della decisione 37 (`coda-mostri-pubblica`) sul doppio tracciamento è stato rifatto con `dati/modelli/` dentro: la cartella è esclusa dal `.gitignore` pubblico ed elencata in `PERCORSI` nello stesso commit che ha creato il primo file, come CLAUDE.md prescrive.
39. **Il bersaglio legale è un filtro** — Si applica la decisione 35 (`repertori-sono-filtri`) senza aggiungere nulla. La fonte **dà il filtro e non il campione**: «umano o demiumano morto prima di aver compiuto un voto» per lo Spectral Minion, «creatura o persona nota al sognatore o a chiunque stia vivendo il sogno» per il Dreamshadow. Si registra l'insieme legale — in prosa e in criteri interrogabili — e la scelta concreta avviene alla generazione. Lo schema lo rende **strutturale invece che raccomandato**: i campi `campione` e `scelta_alla_generazione` accettano un solo valore ciascuno (`null` e `true`), quindi fissare qui un ospite scelto da noi è impossibile, non solo sconsigliato. Gli ospiti che la fonte nomina restano registrati a parte come `esempi_dalla_fonte`, che allargano il campo e non lo restringono.
40. **Un modello non ha grado, ha uno scarto** — Era la domanda senza precedente, e la risposta è che **il grado non gli appartiene**. Il Dreamshadow con l'aspetto di un ratto e quello con l'aspetto di un ogre sono la stessa cosa su bersagli diversi: assegnargli un Grado di Sfida significherebbe fissare l'ospite, cioè decidere ciò che la fonte lascia aperto — lo stesso errore che la decisione 34 (`categorie-eta`) ha evitato moltiplicando le schede per età. Si registra quindi la **modifica** al grado dell'ospite, non un valore assoluto, in tre forme che i tre casi hanno prodotto da soli. **Delta** (Dreamshadow): la fonte stessa ragiona per scarto — delle ventuno righe del blocco statistiche, `XP VALUE` è l'unica che non rimanda all'ospite, e ci scrive sopra «+ 10%». Un +10% non arriva a un quarto del salto più stretto fra due valori XP2e osservati nel bestiario (1.400 → 2.000, circa +43%): lo scarto di grado è **0**, ed è un'affermazione, non un'incertezza. **Non derivabile** (Spectral Minion): i due valori XP2e (975 e 1.400) restano confrontabili con la tabella del passo 10 e **l'uso è registrato** — servono a confermare che le sei fasce di comportamento hanno pesi diversi e che il taglio della fonte è 3+3, non a derivare un grado, perché senza Dadi Vita non ci sono punti ferita e senza punti ferita non c'è grado. Il confronto dà anche un secondo motivo indipendente: la riga 975 della tabella è la più compatta del bestiario (ogni voce convertita con quell'XP è finita a GS 3), la riga 1.400 è fra le più larghe (GS 1, 2 e 3), quindi è proprio il valore alto dei due il meno informativo. **Proprio** (Dreamwraith): la fonte ha già chiuso il modello in una creatura, il grado è legittimo e abita la scheda. Il campo `usato_per_derivare_gs: false` obbliga a compilare `uso_dichiarato`, perché un valore di fonte registrato senza dire che uso se ne fa è una stima nascosta — la lezione della decisione 35 (`repertori-sono-filtri`), resa vincolo di schema.
41. **La sconfessione è una regola condivisa** — La procedura di sconfessione delle illusioni (*Disbelieving Illusions*: quattro passi e una tabella di modificatori di concentrazione) è condivisa fra Dreamshadow e Dreamwraith, sta stampata nella voce del secondo, e il primo non si può scrivere senza. **Vive nel modello, non nelle due schede**: il Dreamwraith smette di portarla come rinvio aperto e la riferisce. È anche il motivo migliore per cui lo schema dei modelli deve esistere — è la prima cosa davvero condivisa fra due creature del bestiario. Si scrive una volta sola: un modello la porta come `definizione`, gli altri come `riferimento`, e il validatore rifiuta una seconda definizione dello stesso id. **Il modello porta un parametro, mai un valore fisso**: contro il Dreamwraith c'è una penalità di **−5** che contro il Dreamshadow non c'è, e i due differiscono anche su un secondo parametro (il Dreamshadow «cannot be disbelieved into non-existence», quindi sconfessarlo protegge chi ci riesce ma non lo elimina). Il −5 è stato riletto sull'immagine di pagina prima di scriverlo: l'OCR di quella voce perde i segni meno con regolarità, come già accaduto su `NO. APPEARING` e sul bonus d'iniziativa della stessa creatura. **Sede provvisoria, dichiarata**: la casa naturale di una regola di sistema è uno schema di regole che il progetto non ha ancora — lo stesso rinvio già registrato per il *mindspin* e i Dragon Orbs. Quando esisterà, la definizione trasloca e tutti i portatori diventano riferimenti: un blocco solo da spostare, non una riscrittura.
42. **Acciaio e oro: due campi, non una conversione** — Le fonti dichiarano **due regole distinte** che rispondono a domande diverse, e vanno registrate come **due campi separati**, non riconciliate in un numero solo. `cambio_monete` = **40:1** (un pezzo d'acciaio vale 40 monete d'oro, *Tales of the Lance*): e' il lore e l'economia interna di Krynn dopo il Cataclisma, dove l'acciaio e' il metallo scarso e l'oro l'ornamento. `fattore_listino` = **1:1**: e' la lettura di un listino importato, e sei moduli d'avventura sono concordi nel trattare il prezzo in oro della fonte come prezzo in acciaio. Due numeri diversi non sono una contraddizione da sciogliere: **collidono solo se si confondono i due usi.** E' il trattamento della decisione 27 (`sette-campi-2e`) — un dato di fonte si registra con la **destinazione dichiarata**, mai come valore nudo. L'accordo di sei moduli rende l'1:1 una **regola editoriale stabile**, non una incoerenza isolata di un singolo modulo. Si registra anche il terzo numero visto nelle fonti — **10:1** in DLC2/DLC3 — come **variante nota** e non come errore, insieme alla clausola del manuale sulle **variazioni regionali** del cambio. CONSEGUENZA OPERATIVA: i nostri `cost_gp` vengono dall'SRD 5.1, cioe' da un listino importato, quindi si leggono con `fattore_listino` e **non si fa nessuna aritmetica** sul borsello iniziale in acciaio. Il 40:1 non entra mai in un prezzo: serve al tesoro, alla ricompensa e alla descrizione del mondo.
43. **Il Barbaro resta razza: rimandato, non respinto** — L'Umano Barbaro **non si converte a background** adesso. Il motivo e' di forma, non di merito: convertirlo richiederebbe uno schema dei background che il progetto **non ha**, e crearne uno ora per una razza sola significherebbe progettarlo **su un caso invece che sui casi** — lo stesso difetto che la decisione 38 (`schema-modelli`) ha evitato aspettando di avere tre creature da modellare. I background serviranno davvero con la **Fase 3**, insieme ai talenti che oggi mancano del tutto: allora ci sara' materiale su cui disegnare lo schema, e la questione si riapre. Fino ad allora il Barbaro resta una voce di `dati/razze/` con i suoi tetti dichiarati. **La decisione e' rimandata per mancanza di uno schema, non respinta nel merito**: l'osservazione che il Barbaro sia piu' un percorso culturale che una razza resta valida e va ripresa, non archiviata.
44. **Tetti di crescita: il punto si perde** — Un aumento di caratteristica che sfonderebbe il massimale razziale e' **perduto**. Non travasato su un'altra caratteristica, non convertito in altro, non ammorbidito. E' la lettura fedele della fonte — un massimale e' un tetto, e sfondarlo non e' previsto — ed e' coerente con aver tenuto gli aggiustamenti negativi e le doppie penalita' della decisione 9 (`aggiustamenti-negativi`): il sistema e' **chiuso**, le razze di Krynn non si mescolano con quelle del PHB, e conta solo l'equilibrio interno. Le alternative rompono ciascuna qualcosa di dichiarato: il **travaso** premia chi ha i tetti bassi, cioe' trasforma una penalita' in un vantaggio; il **tetto morbido** annulla la decisione 10 (`massimali-razziali`) invece di applicarla; la **compensazione con un talento** richiede un catalogo dei talenti che non esiste. VINCOLO DI INTERFACCIA: il giocatore deve **vedere il tetto prima di spendere l'aumento**, non scoprirlo dopo averlo speso. Il sistema **segnala, non blocca in silenzio** — stessa forma della decisione 8 (`generazione-caratteristiche`) sui metodi di generazione irraggiungibili. Le caratteristiche per cui il manuale **non dichiara un massimale** non ereditano un tetto razziale: restano al **20** della 5e.
45. **Lo strato strutturato vive sul blocco, anche sul mostro** — `effetto` sta accanto alla prosa **dentro il blocco**, e questo vale sul mostro come sulla classe. Non e' una scelta nuova — effetto.schema.json la dichiarava gia' per le classi — ma sui mostri non era nemmeno **esprimibile**: `mostro.schema.json` aveva `additionalProperties: false` su `elemento_5e` e nessun campo `effetto`, quindi lo strato che il progetto aveva scelto era vietato proprio dove sta il grosso della meccanica. Scoperto usando i dati, non ispezionandoli: la prima fetta verticale non poteva leggere l'attacco di un mostro perche' non c'era dove scriverlo. **L'alternativa respinta e' una cartella `dati/effetti/`**: ripeterebbe il difetto gia' visto sette volte nel progetto — due strutture che dicono la stessa cosa e che nessuno riconfronta. Qui il riconfronto e' obbligatorio e automatico (`dati/valida_effetti.py`, controllo 2), ed e' il pezzo che paga il costo del campo. **Non e' un allargamento**: dei 9 blocchi dei due mostri della fetta ne hanno `effetto` 5, e gli altri 50 mostri restano prosa. Si struttura cio' che un caso esercita.
46. **Il multiattacco riferisce, non ricopia** — Il blocco *Attacchi Multipli* prende un campo suo, `multiattacco`, che dice **quante volte** si ripete **quale altra azione dello stesso statblock** — per nome, senza ricopiarne i numeri. Prima non aveva nessun campo: la sua unica forma era la frase «effettua due attacchi con X», e un motore che la ignori **dimezza il danno per round** di ogni mostro che ce l'ha, senza che nessun controllo se ne accorga. Sono 18 blocchi su 128 azioni del bestiario, quindi non e' un caso isolato. **Riferimento e non copia** per la stessa ragione della decisione 41 (`sconfessione-condivisa`): i numeri dell'attacco hanno una sede sola, l'azione riferita. `valida_effetti.py` verifica che il nome riferito esista davvero nello stesso statblock — un rimando che non risolve e' peggio di una copia.
47. **Un tiro salvezza ripetuto puo' peggiorare, e allora ha un campo** — `tiro_salvezza.fallimento_ripetuto` registra l'esito del secondo fallimento **dove e' diverso dal primo**. Lo schema aveva gia' `ripetibile`, che dice **quando** si ritira e non **cosa succede**: il Death Throes del Baaz e' a due tempi — il primo fallimento trattiene mentre la pietrificazione comincia, il secondo la compie — e senza il campo nuovo le sue due condizioni diventano una sola, cioe' il tratto perde meta' di se' senza che nessun controllo lo veda. **Campo facoltativo**: si scrive solo dove `ripetibile` c'e' e il secondo tempo differisce dal primo, altrimenti sarebbe una ripetizione. Il campo ha portato con se' un punto cieco, chiuso nello stesso giro: `condizioni_citate()` non lo guardava, quindi la condizione del secondo tempo non sarebbe mai stata controllata.
48. **Le condizioni si aggiungono quando un blocco le riferisce** — Il criterio era gia' scritto in `dati/build_condizioni.py` e questa e' la prima volta che **si applica** invece di essere enunciato: `trattenuto` e `pietrificato` sono nate perche' il Death Throes del Baaz le riferisce davvero, non perche' l'appendice della 5e ne elenca quindici. Sono **cinque, non quindici**, e il numero e' il punto: una cartella riempita per anticipazione e' una cartella di dati che nessun caso ha mai messo alla prova. Le **sei clausole nuove** di `condizione.schema.json` sono parte della stessa decisione e non una decisione a parte: sono esattamente quelle che le due condizioni richiedevano, e nessuna in piu'. `pietrificato` ha portato con se' una domanda che nessun dato dichiarava — una creatura pietrificata **non e' morta**, ha ancora i suoi punti ferita — e che ha costretto a riscrivere la condizione di fine scontro nel motore. E' il segno che il criterio funziona: una condizione aggiunta a consumo porta con se' il caso che la giustifica.
49. **I vocabolari condivisi hanno una sede sola, e la lingua e' l'italiano** — Un termine che compare in **due schemi** e che un motore deve confrontare non e' una convenzione: e' una struttura doppia in attesa di sfasarsi. L'ottava del progetto sono stati i **tipi di danno** — `dati/oggetti/` diceva `slashing` (inglese, dall'SRD) e `dati/mostri/` diceva `perforante`, nessuno dei due schemi li vincolava e **nessuno dei due era sbagliato dal proprio lato**, quindi nessun validatore poteva vederlo. Trovata **usando** i dati, non ispezionandoli: un motore che confronti il danno di un'arma con la resistenza di un mostro li manca tutti. SEDE: `dati/schema/vocabolari.schema.json`, riferito con `$ref` dagli schemi che lo usano — **mai ricopiato**, perche' un enum duplicato in tre schemi sarebbe una struttura doppia nuova, creata mentre si chiude l'ottava. Il codice Python non lo ridigita: `dati/_vocabolari.py` legge quel file. LINGUA: **italiano**, e non per gusto. Ogni altro enum che il progetto possiede nello strato `mechanics_5e` e' gia' italiano (`mischia_arma`, `da_guerra`, `leggera`, `riposo_breve`, gli id di `dati/condizioni/`), e `mechanics_5e` e' lo **strato nostro** della decisione 7 (`doppio-strato`): l'inglese li' dentro non era una scelta, era una stringa di fonte che `build_oggetti.py` copiava senza tradurre. La traduzione avviene **nel generatore**, una volta sola (CLAUDE.md 2), e l'originale inglese resta dov'e' la fonte, in `dati/_fonti/srd51_equipaggiamento.py`. CONSEGUENZA CHE NON ERA UN ENUM: dal lato del mostro le resistenze non erano un vocabolario ma **prosa** — «bludgeoning, piercing, and slashing from nonmagical attacks» era **un** elemento di un array di stringhe. Vincolare solo la lingua avrebbe lasciato il confronto impossibile per forma invece che per lingua, quindi `damage_resistances`, `damage_immunities` e `damage_vulnerabilities` diventano voci `{tipo, solo_se}` e la clausola e' anch'essa un enum. NON CHIUSE, E DICHIARATE TALI: `condition_immunities` porta i nomi delle condizioni in inglese mentre `dati/condizioni/` li ha in italiano — stesso difetto, e chiuderlo obbliga a scegliere fra due strade che riguardano la decisione 48 (`condizioni-a-consumo`), quindi e' una decisione a se'. Misura e alternative in `dati/RAPPORTO-vocabolari.md`.
50. **Da dove viene una CD si dichiara, la derivabilita' si calcola** — Un campo con due significati e' inaffidabile da entrambi i lati, e `cd_derivata_da` ne aveva due: la sua descrizione diceva «come la CD e' stata ottenuta, **quando non e' un dato di fonte**», mentre il controllo 5 di `valida_effetti.py` pretendeva di riempirlo proprio per una CD **di fonte** non derivabile. Al suo posto due campi: **`cd_origine`** (`fonte` | `derivata` | `stimata`), obbligatorio ovunque ci sia una CD, e **`cd_derivazione`**, la prosa breve che dice da quale blocco e' letta, con quale caratteristica torna il conto, o su quale precedente e' stata stimata. La **derivabilita' non e' un campo**: e' calcolabile, e il controllo la calcola invece di credere a cio' che il dato ne afferma. IL CASO CHE LO DIMOSTRA. La CD 11 del Death Throes del Baaz e' stampata nel blocco ufficiale SotDQ, e **combacia col conto**: 8 + il bonus di competenza + il modificatore di Costituzione del Baaz da' esattamente 11, e proprio sulla caratteristica del tiro. Il vecchio controllo quindi **non l'avrebbe mai segnalata** — non perche' fosse a posto, ma perche' una CD letta e una CD derivata erano indistinguibili quando i numeri coincidono. `cd_origine` registra che la coincidenza e' una coincidenza. Il controllo la conta e non la segnala: sapere quante CD di fonte tornano col conto dice quanto vale il conto come prova, e la risposta e' poco. GENERALIZZATA il 03/09/2026, quando lo stesso difetto e' ricomparso su `bonus_colpire`: questa non e' piu' una regola sulle CD ma la **prima applicazione** della decisione 54 (`origine-e-un-dato`), che vale per ogni valore che possa essere sia letto sia calcolato. Il campo e la sua forma non cambiano; cambia che non e' un caso singolo.
51. **Dove vive la meccanica: tre domande, e la prima che risponde decide** — Il criterio, in ordine: **1)** varia da portatore a portatore? → **dato di contenuto** (il danno di un'arma, la CD di un tiro salvezza, **quando un tratto scatta**). **2)** non varia: e' un valore o una procedura? Un **valore o una tabella che la fonte stampa** e' un **dato di sistema** e vive in `dati/sistema/`; una **procedura** — tira, confronta, applica, passa il turno — e' **codice**. **3)** e' una procedura: i nomi che pronuncia vengono da un vocabolario condiviso, mai da stringhe scritte nel codice (decisione 49, `vocabolario-italiano`, anche quando il consumatore e' il motore invece di uno schema). CIO' CHE LO HA IMPOSTO. La **nona struttura doppia** del progetto, e la prima che vive nel **codice** invece che nei dati: il modificatore di caratteristica scritto in `valida_effetti.py` e in `motore/combattimento.py`, il bonus di competenza in `_srd51.py` e in `valida_effetti.py`. Formule identiche in file che nessuna esecuzione metteva uno contro l'altro. Le otto precedenti erano fra file di dati, dove arrivano schemi e validatori; qui non arrivava niente. SEDE: `dati/sistema/`, con `sistema.schema.json` e cinque dati — modificatore di caratteristica, bonus di competenza (per livello **e** per grado sfida, che sono due **letture** della stessa tabella e non due tabelle), formula della CD, moltiplicatori di resistenza/vulnerabilita'/immunita' con il loro **ordine di applicazione**, soglie del 20 e dell'1 naturale. `dati/_sistema.py` le legge e non le ridigita, come `_vocabolari.py` fa con i vocabolari. LA PARTE CHE CONTA PIU' DELLE TABELLE. Una sede non chiude niente da sola: chiude solo se qualcosa impedisce che la tabella venga riscritta altrove. `dati/valida_sistema.py` e' il **primo controllo del progetto che guarda il codice** invece dei dati: rifiuta la stessa tabella riscritta **per forma** (l'espressione, perche' una formula ricopiata cambia nome e non forma) e **per valori** (la tabella espansa a mano). Legge il codice e non la prosa — tokenizza e scarta stringhe e commenti — perche' un rapporto che DESCRIVE la formula fa il suo mestiere, e un controllo che grida al lupo viene spento. Si mette alla prova a ogni giro su copie piantate apposta e su sorgenti che somigliano a una copia senza esserlo: su un repository pulito un rilevatore rotto e uno funzionante tacciono uguale. **UN'ECCEZIONE, dichiarata**: la sonda che ricalcola la tabella con la formula stampata dalla fonte e la confronta riga per riga — un riconfronto, non una copia, ed e' cio' che verifica trenta righe battute a mano. Un'eccezione dichiarata e non piu' trovata e' segnalata come una copia. COSA IL CONTROLLO NON VEDE, scritto in `_sistema.LIMITI` e non solo in un rapporto: una riscrittura algebrica, un'altra lingua (un domani il lato web), la prosa, un derivato **precalcolato nei dati**, e una tabella copiata sotto la soglia di dieci valori.
52. **Cio' che il mostro e il personaggio condividono non e' il campo, e' la lettura** — `attacco` era un **campo** sul mostro e una **funzione** sul personaggio: due cose diverse con lo stesso nome, ed e' la lacuna che il primo scontro ha reso visibile. Le due strade ovvie rompevano ciascuna qualcosa di gia' deciso — far memorizzare l'attacco al personaggio e' un derivato scritto a mano (decisione 7, `doppio-strato`, e CLAUDE.md 3), far derivare l'attacco al mostro e' inventare derivazioni che la fonte non da' (decisione 50, `cd-origine-dichiarata`). SOLUZIONE: **una sola LETTURA**, `attacco_di(combattente)`, che torna la forma `effetto.attacco` gia' definita — sul mostro la legge, sul personaggio la compone da arma, caratteristica, competenza e stile. Chi la chiama non sa quale dei due casi ha davanti, ed e' questo il senso di «la stessa cosa da entrambe le parti»: anche la scelta di quale azione sia un attacco passa da li' e non dal campo, perche' sul personaggio quel campo non esiste. IL PERSONAGGIO PORTA SOLO GLI INGRESSI: razza, classe, livello, punteggi, equipaggiato, scelte. Ogni campo ricavabile da questi **non puo'** esistere — il costruttore solleva, che e' la forma piu' forte del divieto, la stessa con cui la decisione 39 (`bersaglio-legale-filtro`) ha reso impossibile e non solo sconsigliato fissare un ospite. CIO' CHE APRE. Un `bonus_colpire` **letto** dalla scheda e uno **rifatto col conto** si scrivono identici: manca un `bonus_origine`, esattamente come mancava `cd_origine` prima della decisione 50 (`cd-origine-dichiarata`). Misurato invece che supposto — misura al 02/09/2026: dei 94 bonus di attacco che il bestiario scrive in prosa, 85 tornano col conto e 9 no, quindi la coincidenza non e' una conferma. `motore/arena.py` la riconta a ogni giro, cosi' il numero non invecchia in silenzio.
53. **Il vocabolario nomina tutte le condizioni SRD; il catalogo ne converte alcune** — `dati/mostri/` dichiarava le immunita' a condizione con i nomi inglesi della 5e mentre `dati/condizioni/` — sede unica per la decisione 48 (`condizioni-a-consumo`) — ha id italiani. Stesso difetto dei tipi di danno, **piu' grave**: li' erano due trascrizioni, qui una delle due sedi era gia' **dichiarata unica** e l'altra la ignorava, quindi nessuna immunita' del bestiario poteva essere rispettata da nessun motore. PERCHE' NON BASTAVA TRADURRE. Delle condizioni citate dalle immunita' solo tre esistevano nel catalogo: tradurre e basta avrebbe prodotto sette riferimenti che non risolvono, e crearle per anticipazione avrebbe sconfessato la decisione 48 (`condizioni-a-consumo`) tre giorni dopo averla presa. Restringere l'enum alle esistenti era peggio: le schede perdevano informazione vera di fonte. SOLUZIONE, ed e' la strada della decisione 35 (`repertori-sono-filtri`): l'insieme delle condizioni SRD e' **chiuso e noto**, quindi il vocabolario e' **completo** — quindici termini in `vocabolari.schema.json`, riferiti per `$ref` da `mostro.schema.json` — mentre il catalogo ne converte cinque. Le altre dieci non sono condizioni **inesistenti**: sono una **lacuna del nostro catalogo**, che e' cosa diversa. IL DIVARIO NON SI SCRIVE, SI DERIVA: quali siano modellate lo dice la cartella (`_vocabolari.condizioni_modellate()`), perche' un elenco a mano accanto a una cartella sarebbe una struttura doppia nuova creata mentre se ne chiude un'altra. IL MOTORE DEVE SAPERLO. Un'immunita' a una condizione che il catalogo non modella viene **dichiarata** come lacuna (`condizione-non-modellata`) e non ignorata in silenzio: ignorata, sarebbe indistinguibile da un'immunita' rispettata. Misura al 02/09/2026: 35 immunita' su 11 schede, di cui 29 nominano una condizione che il motore non sa ancora applicare. La traduzione dall'SRD ha una sede sola (`_vocabolari.CONDIZIONE_DA_SRD`), con l'invariante verificata all'import: ogni id prodotto sta nell'enum, e ogni voce dell'enum ha un termine inglese che ci arriva.
54. **L'origine di un valore e' un dato, non una deduzione** — PRINCIPIO. Quando un valore puo' essere **sia letto dalla fonte sia calcolato dal sistema**, la sua **origine va dichiarata in un campo**. Nessun controllo puo' dedurla dai numeri, perche' quando le due strade coincidono il valore letto e quello calcolato sono **indistinguibili** — e coincidono quasi sempre, che e' esattamente cio' che rende il difetto invisibile. Un valore che non dichiara la propria origine non e' verificabile: oggi puo' essere giusto e domani sfasarsi senza che nessuno se ne accorga. DUE APPLICAZIONI, NON DUE DECISIONI. La decisione 50 (`cd-origine-dichiarata`) e' la prima e riguarda le CD (`cd_origine` con `cd_derivazione`); `bonus_origine` con `bonus_derivazione` sul `bonus_colpire` di `effetto.attacco` e' la seconda. Stesso enum — `fonte` | `derivata` | `stimata` — stessa coppia di campi, stessa forma di controllo: una `derivata` deve tornare col conto e il controllo lo verifica, una `fonte` e una `stimata` no ma devono dire da dove vengono. La regola e' stata generalizzata al **secondo** caso e non al terzo: e' successo due volte in due giri, su campi diversi, e la seconda l'ha trovata il committente. LA DERIVABILITA' RESTA CALCOLATA, l'origine no. E' la stessa distinzione della decisione 50 (`cd-origine-dichiarata`): si dichiara cio' che non si puo' ricavare, e si ricava tutto il resto. Un campo `derivabile` sarebbe un derivato scritto a mano (CLAUDE.md 3). LA MISURA, al 03/09/2026, e' cio' che regge il principio invece di un'argomentazione. Dei **94 bonus di attacco** che il bestiario scrive in prosa **85 tornano col conto** competenza + caratteristica e 9 no; delle 35 CD in prosa 29 tornano e 6 no. Gli 85 e i 29 non sono conferme: il bonus della Spada corta del Baaz e' **stampato** nel blocco ufficiale SotDQ **e** torna col conto, come la sua CD 11, e nessuno dei due controlli poteva vederlo. I due attacchi oggi strutturati sono uno `fonte` (Baaz) e uno `derivata` (Traag) e si scrivono allo stesso modo: e' la dimostrazione su un caso vero, non un'ipotesi. I NOVE FUORI CONTO SONO IL GRUPPO CHE INSEGNA, e non sono nove errori. **Due** portano un addendo che la fonte dichiara e che la formula non ha un posto dove mettere — il +3 innato del Cavaliere della Morte e dello Scheletro Guerriero, che sono la stessa voce in due varianti. **Tre** sono l'arco lungo dei centauri, dove la 2e attribuisce alla specie un bonus con gli archi: un tratto di razza convertito, non uno scarto. **Quattro** — l'Orso Glaciale e lo Skyfisher, due attacchi ciascuno — non hanno nessuna nota che li spieghi. La lezione e' che il conto non fallisce dove il dato e' sbagliato: fallisce dove la **formula e' incompleta**, e le due cose si scrivono uguali finche' l'origine non e' un campo. QUANTI ALTRI CAMPI HANNO QUESTA FORMA — misurato, non stimato, ed e' il motivo per cui la decisione e' generale. Ancora scoperti: il **bonus di danno** in prosa (110 casi, 96 tornano col conto), i **bonus di abilita'** (18, 16 tornano), la **percezione passiva** (52, 52 tornano). Quest'ultima e' il caso limite che spiega il principio meglio di ogni altro: il conto torna il **cento per cento** delle volte, e proprio per questo di nessuna si sa se sia stata letta o calcolata. Un campo dove il conto torna sempre e' il posto **peggiore** in cui fidarsi del conto. IL PRECEDENTE INCONSAPEVOLE, che e' la scoperta piu' utile del giro: `armor_class`, `hit_points` e `challenge_rating` **dichiarano gia'** la propria origine, sotto un altro nome — `conversion_status` piu' `source`. Il progetto aveva inventato questo campo **tre volte** senza accorgersi che era lo stesso campo, e `cd_origine` era la quarta. Unificare i tre nomi e' un rinominare che tocca 52 schede e uno schema gia' committato: **non fatto ora, dichiarato aperto**, e il momento giusto sara' quando il primo dei campi ancora scoperti dovra' portare l'origine davvero. DOVE IL DIFETTO NON PUO' ESISTERE. Un campo che porta solo **ingressi** non ha questa forma: `saving_throws` dichiara quali competenze il portatore ha e non il numero che ne segue, quindi non c'e' niente da confondere. E' la stessa forma che la decisione 52 (`attacco-unica-lettura`) ha imposto al personaggio, e la regola che ne segue e' che **un campo che si puo' non scrivere e' meglio di un campo la cui origine si deve dichiarare**: dichiarare l'origine e' il rimedio dove il valore deve stare scritto, non il primo posto dove guardare.
55. **Un valore e la sua origine viaggiano insieme, e il vocabolario ha una sede sola** — IL DIFETTO. Il progetto aveva inventato il campo "origine" **quattro volte** senza accorgersene: `conversion_status` piu' `source` su `armor_class`, su `hit_points` e su `challenge_rating` — 156 dichiarazioni gia' in opera su 52 schede — e poi `cd_origine` con `cd_derivazione`, e poi `bonus_origine` con `bonus_derivazione`. Decima struttura doppia, e in una forma nuova: non due file che divergono, ma **lo stesso concetto con quattro nomi**. La decisione 54 (`origine-e-un-dato`) l'aveva vista e dichiarata aperta, rimandando l'unificazione al momento in cui il primo campo ancora scoperto avesse dovuto portare l'origine davvero. Quel momento e' arrivato: ogni campo nuovo sarebbe stata la quinta reinvenzione. SI ESTENDE, NON SI SOSTITUISCE. `conversion_status` piu' `source` reggeva da mesi su tre campi e su 156 dichiarazioni: e' quello a restare, ed e' il motivo per cui il rinominare temuto su 52 schede **non e' servito**. La traduzione dell'enum piu' giovane in quello piu' vecchio e' `fonte` -> `direct`, `stimata` -> `adapted`, `derivata` -> **`derived`**, che e' l'unico valore che l'enum piu' vecchio non aveva: un valore derivato non e' `direct` (nessuno l'ha stampato) ne' `adapted` (nessuno l'ha scelto), ed e' l'unico dei cinque che un controllo puo' **rifare**. LA FORMA E' UN OGGETTO, E IL PREFISSO ERA IL DIFETTO. Un valore e la sua origine stanno nello **stesso oggetto** — `{value, conversion_status, source, note}` — che e' esattamente cio' che `armor_class` gia' era. La forma piatta a prefisso (`cd_origine`, `bonus_origine`) non scala e **e' il meccanismo** con cui il campo si e' reinventato quattro volte: `attacco` porta due numeri che hanno ciascuno un'origine, `bonus_colpire` e `danno[].bonus`, e ogni numero nuovo pretendeva un prefisso nuovo. Con l'incapsulamento l'origine **non puo' piu' mancare** — non perche' un controllo la pretende, ma perche' non c'e' un posto dove scrivere il valore senza di essa. La clausola condizionale che obbligava il campo di origine e' stata cancellata: la garanzia e' diventata strutturale. LA SEDE. `conversion_status` e `provenienza` erano definiti **tre volte** in `$defs` (mostro, oggetto, modello) e la copia di `oggetto` era **gia' divergente** (sette voci contro cinque): la struttura doppia aveva gia' cominciato a sfasarsi senza che nessun dato la denunciasse, perche' un enum ricopiato valida benissimo finche' le copie coincidono. Ora i due vocabolari stanno in `vocabolari.schema.json` — la stessa sede della decisione 49 (`vocabolario-italiano`) — e i quattro schemi che li usano li riferiscono con un `$ref` fra file. L'elenco delle provenienze e' l'**unione** delle tre copie: la fusione allarga il vincolo dei singoli schemi, ed e' il prezzo dichiarato di una sede sola. Unico valore nuovo, `regola di sistema`, che accompagna sempre un `derived`. IL CONTROLLO SI METTE ALLA PROVA. Questo difetto non si vede dai dati e si vede solo guardando gli schemi, e su un repository pulito un rilevatore rotto e uno funzionante tacciono uguale: `prova_di_se_stesso()` gli mette davanti tre difetti piantati (un enum ridigitato fuori sede, un `$defs` condiviso che non e' un `$ref`, un `conversion_status` senza `source` accanto) e due somiglianze legittime che non deve segnalare. E' lo stesso schema di `COPIE_PIANTATE` in `_sistema.py`. COSA NON SI E' LASCIATO UNIFICARE, dichiarato e non nascosto. (a) `conversion_status` **e un nome per due concetti**: a livello di scheda vale "a che punto e' questa scheda" ({da_compilare, in_corso, compilato} nei mostri, negli oggetti, nei modelli e nelle razze; {clonato, in_sospeso} nelle classi), a livello di elemento dichiara l'origine di un valore. Rinominare tocca ~166 file piu' i generatori `build_*.py`: e' un giro suo, misurato e non fatto qui. (b) In razze e classi `source` e' una **stringa libera** che porta la citazione di pagina, non un enum: li' porta piu' informazione, ed e' la ragione per cui resiste alla fusione diretta. (c) `razza.schema.json` e `classe.schema.json` quasi non vincolano `mechanics_5e`: l'origine dichiarata in 105 tratti razziali e 43 privilegi di classe **non e' validata da nessuno**. Zona morta di schema, aperta. (d) Restano scoperti `danno[].bonus` (110 casi), `skills[].bonus` (18) e `passive_perception` (52 su 52 che tornano col conto, il caso che insegna): la forma ora esiste, applicarla e' lavoro di dati.
56. **Il Personaggio si progetta perche' il background si possa aggiungere dopo** — IL RINVIO CONFERMATO. Il Barbaro resta una **razza** e non diventa un background: tappo, non conversione. Ma delle tre decisioni sospese e' l'unica che tocca la **forma** dello schema e non il contenuto, e una forma sbagliata oggi si paga riscrivendo domani. LA PROVVISIONE. Lo schema Personaggio si progetta in modo che aggiungere un campo `background` piu' avanti sia **additivo**: nessun campo esistente cambia significato, nessun dato gia' scritto va riletto. In concreto: l'origine narrativa del personaggio non si deduce dalla razza ne' si incastra dentro di essa, e i tratti che oggi arrivano dalla razza non presuppongono nella loro forma che la razza sia la loro **unica** sorgente. Il campo **non si aggiunge ora** — si evita solo di precluderlo. PERCHE' NON BASTA DIRLO A VOCE. E' la stessa lezione delle dieci strutture doppie: un vincolo che vive solo nella testa di chi scrive non sopravvive alla sessione in cui e' stato pensato.
57. **Il limite della fetta verticale: la prossima parte dalla creazione, non dal combattimento** — IL LIMITE, INDIVIDUATO DAL METODO STESSO. L'arena misura cosa manca al motore **a un turno**, e il personaggio le arriva **gia' costruito**. Ne segue che nessuna lacuna della **creazione** puo' comparire in quella misura, per quanto la si affini: la fetta verticale non vede cio' che sta a monte del suo ingresso. Non e' una critica al metodo — e' il metodo che ha reso visibile il proprio limite, che e' il motivo per cui va **registrato** invece che ricordato. LA CONSEGUENZA. La **prossima fetta parte dalla creazione**, non dal combattimento. La prova che il limite era reale c'e' gia': `allowed_classes` non e' un campo che manca, e' una decisione che manca — 17 etichette del PHB 2e contro 17 nostre classi — e nessun giro d'arena poteva farla emergere, perche' l'arena riceve un personaggio a cui la classe e' gia' stata assegnata.
58. **`allowed_classes` si risolve per telaio, con il filtro in sequenza** — LA REGOLA. Un'etichetta del PHB 2e in `allowed_classes` non nomina una classe del nostro roster: nomina un **telaio**. Il telaio **apre** l'insieme — tutte le nostre classi che stanno su quel chassis 5e — e poi **i requisiti della classe filtrano dentro**. Due controlli in sequenza, non uno. Una razza che dichiara `Fighter` accede al gruppo delle classi su chassis Fighter; poi ogni classe del gruppo applica i propri vincoli. Il Cavaliere della Corona e' riservato a umani e mezzelfi: un nano che ha `Fighter` non ci arriva comunque — non perche' il telaio glielo neghi, ma perche' la classe lo filtra. E' la stessa forma gia' in uso nella decisione 24 (`sfere-sacerdotali`) (la sfera concede, il dominio filtra) e nella decisione 35 (`repertori-sono-filtri`) (il filtro delimita, la scelta avviene dopo). PERCHE' I CHASSIS. Sono gia' il ponte fra le classi di Krynn e la 5e, e sono l'unica struttura che copre `Fighter`, `Paladin` e `Thief` senza inventare classi: tre etichette che il roster non ha come nomi e che dodici, due e nove razze dichiarano. CIO' CHE IL TELAIO NON APRE, dichiarato perche' non si confonda con una dimenticanza. Il telaio non e' l'unica via: un'etichetta che nomina una nostra classe **per nome** (`Mariner`, `Tinker`, `Handler`), o che la fonte dichiara essere quella classe, la apre lo stesso, e il telaio **si aggiunge** invece di sostituirsi. Ogni accostamento di questo secondo tipo porta in sede la propria riga di fonte, e quelli ancora da confermare sono marcati tali: `Druid (heathen)` e `Priest (heathen)` sulla stessa classe sono in attesa, non risolti qui. Senza questa clausola l'etichetta `Mariner` non aprirebbe il Marinaio, che non ha chassis. `Knight of Solamnia` e' un'etichetta ombrello e apre tutti e tre gli ordini; il filtro dell'ingresso lascia poi il solo Cavaliere della Corona, che e' esattamente la sequenza obbligata della decisione 5 (`cavalieri-solamnia`). LA SEDE E IL PREZZO. La mappa e la risoluzione stanno in `dati/_classi_ammesse.py` — una sede sola, importata dal diagnostico e da chiunque debba rispondere alla prima domanda della creazione. Il prezzo e' reale e si paga in chiaro: dove la fonte era piu' stretta il telaio allarga, e lo scarto si dichiara invece di assorbirlo (decisione 7 (`doppio-strato`)).
59. **Le cinque classi base 2e si trascrivono, e il loro strato di Krynn e' vuoto** — IL MOTIVO CHE DECIDE E' UN'ESCLUSIONE FALSA, e non un vuoto da riempire per completezza. Il Con Artist chiede Carisma 12 contro il massimale 9 dell'Aghar, e quel filtro morde giusto: e' la doppia penalita' della decisione 10 (`massimali-razziali`) che fa il suo mestiere. Ma il ladro **base** chiede Destrezza 9 e l'Aghar la porta fino a 18, e la tabella Class/Race Combinations gli concede `Thief` fino all'ottavo livello. E' il primo caso in cui a togliere qualcosa non e' la fonte ma un buco del NOSTRO roster: tutte le altre esclusioni erano fedelta', questa era nostra. E colpiva la razza piu' stretta del roster, che prima di oggi aveva 2 classi accessibili su 17. LA FORMA, ED E' LA FONTE A DETTARLA. *Tales of the Lance* dichiara queste classi giocabili su Ansalon e non le descrive: l'Overview le elenca, le Class descriptions passano oltre, e il capitolo dei guerrieri scrive che su Ansalon si giocano le classi guerriere tipiche della 2e mentre quelle *uniche* di Ansalon vengono descritte di seguito. Il gruppo dei ladri ripete la forma. Lo strato di Krynn e' quindi **vuoto per dichiarazione**, non per trascrizione incompleta, e cio' che la tabella aggiunge — accesso razziale e tetto di livello — non appartiene alla classe: il primo vive gia' in `allowed_classes` delle razze, il secondo non si applica (decisione 4, `limiti-di-livello`). SI TRASCRIVONO percio' i soli minimi della Tabella 13 del PHB 2e (pag. 25 stampata, letta dall'immagine), e `mechanics_5e` e' il chassis SRD **con niente sopra**. Non e' una scorciatoia: e' cio' che la fonte dice, e **zero privilegi di fonte da convertire e' un dato**, non una lacuna. E' anche il primo posto del progetto dove il chassis della decisione 23 (`principio-del-clone`) non e' un accostamento editoriale ma un'identita': il Guerriero 2e e il Fighter SRD sono la stessa classe in due edizioni. IL SECONDO MANUALE DI FONTE NON E' UN PRECEDENTE NUOVO. La decisione 16 (`nove-tratti-phb2e`) l'ha gia' fatto per le razze: 70 tratti su 105 vengono dal PHB 2e per rimando, con la fonte marcata voce per voce. Le classi seguono la stessa strada, e ne segue la correzione che la rende possibile: **la fonte va per classe, non per file**. `build_classi.BOOK` era una costante di modulo, cioe' un dato di file, e non lo e' mai stato; ora e' un default, e chi viene da un altro manuale lo dichiara nel proprio campo `book`. L'ORDINE, E QUANTO COSTA CIASCUNA META'. Prime le tre a telaio gia' trascritto — Guerriero, Paladino, Ladro — che chiudono le tre esclusioni vere: `Paladin` al Silvanesti e all'Irda, `Thief` all'Aghar, le uniche tre coppie razza+etichetta che aprivano una porta e non lasciavano dentro niente. Bardo e Ranger dopo: per loro manca **anche** il telaio (`_srd51.CODA`), e le coppie che sbloccheranno non sono esclusioni ma classi non ancora scritte. LA MISURA, dopo le prime tre: le coppie razza+classe accessibili passano da 93 a 126 su 168 aperte, il filtro ne toglie 42 come prima, e l'Aghar passa da 2 a 4 classi — `barbaro`, `guerriero`, `ladro`, `sacerdote-ordini-sacri`. Il Con Artist gli resta precluso, ed e' giusto cosi': la porta riaperta e' quella del ladro comune.

---

## Le 15 razze

| id | razza | aggiustamenti | requisiti notevoli |
|---|---|---|---|
| `elfo-dargonesti` | Elfo Dargonesti (Elfo degli Abissi) | DES +1, FOR -1 | DES min 10 |
| `elfo-dimernesti` | Elfo Dimernesti (Elfo dei Bassifondi) | DES +1, FOR -1 | DES min 10 |
| `elfo-kagonesti` | Elfo Kagonesti | COS +1, DES +2, INT -3, FOR +1 | INT max 12 |
| `elfo-qualinesti` | Elfo Qualinesti | COS -1, DES +1 | — |
| `elfo-silvanesti` | Elfo Silvanesti | COS -1, DES +1 | INT min 10, CAR min 12 |
| `gnomo-minoi` | Gnomo (Minoi) | DES +2, FOR -1 | SAG max 12 |
| `irda` | Irda (Alto Ogre) | CAR +1, COS -3, DES +1, INT +1 | FOR min 12, COS max 15, COS min 12, SAG min 10, CAR min 15 |
| `kender` | Kender | DES +1 | FOR max 16, SAG max 16 |
| `mezzelfo` | Mezzelfo | DES +2 | — |
| `minotauro` | Minotauro | CAR -2, COS +2, FOR +2, SAG -2 | FOR min 12, COS min 12, SAG max 16, CAR max 16 |
| `nano-aghar` | Nano Sozzo (Aghar) | — | COS max 12, INT max 9, SAG max 9, CAR max 9 |
| `nano-collina` | Nano delle Colline (Neidar) | CAR -1, COS +1 | DES max 17, COS min 14, CAR max 12 |
| `nano-montagna` | Nano delle Montagne (Hylar / Daewar) | CAR -1, COS +1 | DES max 17, COS min 12, CAR max 16 |
| `umano-barbaro` | Barbaro | COS +1 *(ed.)*, FOR +1 *(ed.)* | FOR min 10, DES max 16, COS min 12 |
| `umano` | Umano | +1 a due caratteristiche a scelta del giocatore *(ed.)* | — |

*(ed.)* segnala una conversione editoriale nostra, non un dato di fonte.

Clan nanici esclusi perché il manuale li riserva ai PNG: Klar, Theiwar,
Daergar, Zhakar.

### Aggiustamenti di fonte, al netto

Solo i valori del manuale: le compensazioni editoriali sono escluse.

| netto | razze | quali |
|---:|---:|---|
| +2 | 1 | Mezzelfo |
| +1 | 3 | Elfo Kagonesti, Gnomo (Minoi), Kender |
| +0 | 11 | Barbaro, Elfo Dargonesti (Elfo degli Abissi), Elfo Dimernesti (Elfo dei Bassifondi), Elfo Qualinesti, Elfo Silvanesti, Irda (Alto Ogre), Minotauro, Nano Sozzo (Aghar), Nano delle Colline (Neidar), Nano delle Montagne (Hylar / Daewar), Umano |

**Doppia penalità** — aggiustamento negativo *e* massimale sulla stessa
caratteristica, conservata perché è del manuale:

- Elfo Kagonesti (INT -3, max 12)
- Irda (Alto Ogre) (COS -3, max 15)
- Minotauro (CAR -2, max 16)
- Minotauro (SAG -2, max 16)
- Nano delle Colline (Neidar) (CAR -1, max 12)
- Nano delle Montagne (Hylar / Daewar) (CAR -1, max 16)

> **Lettura interpretativa** — registrata il 2026-09-05. Non e' derivata dai dati.
>
> Il netto va da +0 a +2: nessuna razza raggiunge il +3 che la 5e
> 2014 assegna di norma. Non va pareggiato. Le razze di Krynn non vengono mescolate
> con quelle del PHB: il sistema è chiuso e conta solo l'equilibrio interno.

### Taglia, velocità, scurovisione

| razza | taglia | velocità | scurovisione |
|---|---|---:|---:|
| Elfo Dargonesti (Elfo degli Abissi) | Medium | 30 ft | 60 ft |
| Elfo Dimernesti (Elfo dei Bassifondi) | Medium | 30 ft | 60 ft |
| Elfo Kagonesti | Medium | 30 ft | 60 ft |
| Elfo Qualinesti | Medium | 30 ft | 60 ft |
| Elfo Silvanesti | Medium | 30 ft | 60 ft |
| Gnomo (Minoi) | Small | 25 ft | 60 ft |
| Irda (Alto Ogre) | Medium | 25 ft | assente |
| Kender | Small | 25 ft | 30 ft |
| Mezzelfo | Medium | 30 ft | 60 ft |
| Minotauro | Medium | 30 ft | assente |
| Nano Sozzo (Aghar) | Small | 25 ft | 60 ft |
| Nano delle Colline (Neidar) | Medium | 25 ft | 60 ft |
| Nano delle Montagne (Hylar / Daewar) | Medium | 25 ft | 60 ft |
| Barbaro | Medium | 30 ft | assente |
| Umano | Medium | 30 ft | assente |

La velocità è derivata dai **tassi MV della 2e**, non dalla taglia.

| MV 2e | velocità 5e | razze |
|---:|---:|---|
| 6 | 25 ft | Gnomo (Minoi), Nano Sozzo (Aghar), Nano delle Colline (Neidar), Nano delle Montagne (Hylar / Daewar) |
| 9 | 25 ft | Irda (Alto Ogre), Kender |
| 12 | 30 ft | Barbaro, Elfo Dargonesti (Elfo degli Abissi), Elfo Dimernesti (Elfo dei Bassifondi), Elfo Kagonesti, Elfo Qualinesti, Elfo Silvanesti, Mezzelfo, Minotauro, Umano |

> **Lettura interpretativa** — registrata il 2026-09-05. Non e' derivata dai dati.
>
> Derivare la velocità dalla taglia invertiva l'ordinamento della fonte: i nani
> finivano a 30 e i Kender a 25, cioè il nano correva più del Kender. La 5e stessa
> smentisce quella regola — il nano del PHB 2014 è Medium e va a 25, perché tratta
> la lentezza dei nani come tratto identitario. Nemmeno la proporzione funziona:
> 6/12 × 30 darebbe 15 piedi.
>
> I tassi 2e distinti sono 3, i valori 5e utilizzabili 2: un pareggio è
> inevitabile. L'ordinamento resta preservato in senso **debole** — nessuno supera
> chi in 2e era più veloce — ma il pareggio non si limita a conservare le
> uguaglianze esistenti, **ne crea una nuova**: Kender e Irda (MV 9) non erano
> uguali ai nani (MV 6) e adesso lo sono. Quella differenza viene collassata. È il
> prezzo di avere 3 valori di partenza e 2 di arrivo. I tassi originali
> restano in `movement_2e`.
>
> Sulla scurovisione: dove il manuale dichiara l'infravisione si converte con la
> portata indicata; dove tace resta assente **per scelta**, non per dimenticanza.
> Nell'Appendice Mostruosa il valore fra parentesi è quello *senza armatura*, e
> vale sia per la CA sia per il movimento.

---

## Le 20 classi

| id | classe | gruppo | note |
|---|---|---|---|
| `barbaro` | Barbaro | Warrior | — |
| `cavaliere-corona` | Cavaliere della Corona | Warrior | grado 1 dell'ordine; solo umano/mezzelfo; Lawful Good |
| `cavaliere-rosa` | Cavaliere della Rosa | Warrior | grado 3 dell'ordine; si entra al 4°; solo umano/mezzelfo; Lawful Good |
| `cavaliere-spada` | Cavaliere della Spada | Warrior | grado 2 dell'ordine; si entra al 3°; solo umano/mezzelfo; Lawful Good |
| `cavaliere` | Cavaliere | Warrior | Qualunque allineamento buono |
| `commoner` | Popolano | Normal | — |
| `con-artist` | Truffatore / Prestigiatore | Rogue | — |
| `guerriero` | Guerriero | Warrior | — |
| `handler` | Handler | Rogue | solo kender |
| `ladro` | Ladro | Rogue | — |
| `mago-alta-stregoneria` | Mago dell'Alta Stregoneria | Wizard | Determinato dalla veste: Bianca=buono, Rossa=neutrale, Nera=malvagio. L'allineamento va dichiarato al 3° livello, prima del Test. |
| `mago-rinnegato` | Mago Rinnegato | Wizard | — |
| `mago-veste-bianca` | Mago delle Vesti Bianche | Wizard | si entra al 3°; Buono |
| `mago-veste-nera` | Mago delle Vesti Nere | Wizard | si entra al 3°; Malvagio |
| `mago-veste-rossa` | Mago delle Vesti Rosse | Wizard | si entra al 3°; Neutrale |
| `mariner` | Marinaio | Warrior | Qualunque tranne Legale Buono |
| `paladino` | Paladino | Warrior | — |
| `sacerdote-eretico` | Sacerdote Eretico | Priest | — |
| `sacerdote-ordini-sacri` | Sacerdote degli Ordini Sacri delle Stelle | Priest | Coerente con la famiglia celeste del dio servito: Bene, Male o Neutralita'. |
| `tinker` | Tinker | Normal | solo gnomo-minoi |

I Cavalieri della Spada ricevono gli incantesimi da **Kiri-Jolith**, non da Paladine.

### Forma meccanica

Diagnostica completa in `dati/RAPPORTO-classi.md`. Qui la sintesi.

| classe | gruppo | DV 2e | tabella PE | inc. | priv. | imp. | chassis 5e |
|---|---|---|---|:-:|---:|---:|---|
| Barbaro | Warrior | d10 | del gruppo | — | 2 | 1 | `Fighter` |
| Cavaliere | Warrior | d10 | del gruppo | — | 6 | 4 | `Fighter` |
| Cavaliere della Corona | Warrior | d10 | propria, 25 liv. | — | 1 | 1 | `Fighter` |
| Cavaliere della Rosa | Warrior | d10 | propria, 22 liv. | — | 1 | 0 | `Paladin` |
| Cavaliere della Spada | Warrior | d10 | propria, 23 liv. | sì | 3 | 0 | `Paladin` |
| Guerriero | Warrior | — | del gruppo | — | 0 | 0 | `Fighter` |
| Marinaio | Warrior | d10 | del gruppo | — | 1 | 1 | **indeciso** |
| Paladino | Warrior | — | del gruppo | — | 0 | 0 | `Paladin` |
| Mago dell'Alta Stregoneria | Wizard | 1d4 | propria, 25 liv. | sì | 3 | 4 | `Wizard` |
| Mago Rinnegato | Wizard | 1d4 | propria, 25 liv. | sì | 1 | 2 | `Wizard` |
| Mago delle Vesti Bianche | Wizard | 1d4 | del gruppo | — | 0 | 1 | **indeciso** |
| Mago delle Vesti Nere | Wizard | 1d4 | del gruppo | — | 0 | 1 | **indeciso** |
| Mago delle Vesti Rosse | Wizard | 1d4 | del gruppo | — | 0 | 1 | **indeciso** |
| Sacerdote Eretico | Priest | 1d8 | propria, 25 liv. | — | 0 | 2 | **indeciso** |
| Sacerdote degli Ordini Sacri delle Stelle | Priest | 1d8 | propria, 25 liv. | sì | 0 | 1 | `Cleric` |
| Truffatore / Prestigiatore | Rogue | d6 | del gruppo | — | 1 | 1 | `Rogue` |
| Handler | Rogue | d6 | del gruppo | — | 0 | 3 | **indeciso** |
| Ladro | Rogue | — | del gruppo | — | 0 | 0 | `Rogue` |
| Popolano | Normal | d6 | propria, 25 liv. | — | 0 | 0 | **indeciso** |
| Tinker | Normal | d6 | propria, 25 liv. | — | 0 | 1 | **indeciso** |

Su 20 classi: **19 privilegi** e **24 impedimenti**. Solo 7 privilegi sono
agganciati a un livello esplicito; per gli altri 12 la fonte non dice quando si
ottengano.

- **11 classi non hanno tabella di esperienza propria** e rimandano al gruppo: Barbaro, Cavaliere, Truffatore / Prestigiatore, Guerriero, Handler, Ladro, Mago delle Vesti Bianche, Mago delle Vesti Nere, Mago delle Vesti Rosse, Marinaio, Paladino.
- **11 classi non hanno alcun privilegio**: Popolano, Guerriero, Handler, Ladro, Mago delle Vesti Bianche, Mago delle Vesti Nere, Mago delle Vesti Rosse, Paladino, Sacerdote Eretico, Sacerdote degli Ordini Sacri delle Stelle, Tinker.
- **9 classi hanno più impedimenti che privilegi.**
- Le tabelle arrivano al **25° livello**, cinque oltre il tetto della 5e.
- **Nessuna classe ha una tabella di THAC0 o di tiri salvezza**: valgono quelle di
  gruppo del PHB 2e, che non sono ancora nei dati.

> **Lettura interpretativa** — registrata il 2026-09-05. Non e' derivata dai dati.
>
> Le classi di Krynn non sono classi nel senso della 5e: sono profili di
> restrizione appoggiati sulle classi base della 2e. Convertirle non è un lavoro di
> traduzione ma di riempimento — non c'è quasi nulla da tradurre. È la ragione della
> decisione 23 (`principio-del-clone`).

### Chassis applicati (decisione 23, `principio-del-clone`)

**12 classi su 20** sono cloni meccanici di una classe SRD 5.1: Cleric ×1, Fighter ×4, Paladin ×3, Rogue ×2, Wizard ×2.
**8 restano senza chassis**, per decisione: Popolano, Handler, Mago delle Vesti Bianche, Mago delle Vesti Nere, Mago delle Vesti Rosse, Marinaio, Sacerdote Eretico, Tinker.

Le sette incompatibilità strutturali sono risolte in `mechanics_5e.structural`,
uguali per tutte le classi: tabella PE unica, bonus di competenza al posto del
THAC0, cinque categorie di tiro salvezza mappate sulle sei caratteristiche,
competenze per categoria, pacchetti fissi, troncamento al 20°, titoli
descrittivi.

Stato dei 43 privilegi e impedimenti della fonte:
**2** `direct`, **40** `pending`, **1** `source_only`.
I `pending` sono il lavoro che resta: la decisione 23 (`principio-del-clone`) autorizza il clone del
chassis, non l'invenzione di meccanica 5e per i privilegi.

---

## Sfere sacerdotali (decisione 24, `sfere-sacerdotali`)

Verifica completa in `dati/RAPPORTO-sfere.md`. Le sfere filtrano la lista del
chierico SRD 5.1 (105 incantesimi, 7 trucchetti compresi); il Dominio resta
come sottoclasse. Accesso minore: solo fino al 3° livello, come in 2e.

| divinità | incant. accessibili | livelli vuoti | guarigione | offesa | Dominio |
|---|---:|---|:-:|:-:|---|
| Branchala | 30 | 4°, 7° | sì | sì | `Life` |
| Chemosh | 42 | 8° | sì | sì | `Death` ⚠︎ |
| Chislev | 42 | — | sì | sì | `Nature` |
| Gilean | 66 | — | sì | sì | `Knowledge` |
| Habbakuk | 43 | 9° | sì | sì | `Nature` |
| Hiddukel | 47 | 8° | **NO** | **NO** | `Trickery` |
| Kiri-Jolith | 62 | — | sì | sì | `War` |
| Lunitari | 57 | 8° | sì | sì | `Knowledge` |
| Majere | 41 | 8° | **NO** | **NO** | `Knowledge` |
| Mishakal | 70 | — | sì | sì | `Life` |
| Morgion | 47 | 8° | sì | sì | `Death` ⚠︎ |
| Nuitari | 69 | 8° | sì | sì | `Knowledge` |
| Paladine | 53 | — | sì | sì | `Life` |
| Reorx | 55 | 9° | sì | sì | `Forge` ⚠︎ |
| Sargonnas | 44 | 8° | **NO** | sì | `War` |
| Shinare | 42 | 9° | **NO** | sì | `Trickery` |
| Sirrion | 50 | — | sì | sì | `Light` |
| Solinari | 65 | 8° | sì | sì | `Light` |
| Takhisis | 66 | — | sì | sì | `Trickery` |
| Zeboim | 33 | 9° | **NO** | sì | `Tempest` |
| Zivilyn | 44 | 8° | **NO** | **NO** | `Knowledge` |

- **6 divinità su 21 non hanno alcuna cura**: Hiddukel, Majere, Sargonnas, Shinare, Zeboim, Zivilyn.
- **3 non hanno alcuna offesa diretta**: Hiddukel, Majere, Zivilyn.
- **14 hanno almeno un livello di incantesimi completamente vuoto.**
- Delle 105 voci, 28 sono attribuzioni nostre e non ereditate da un
  antenato 2e: restano marcate `nostra` nel dato.

> **Lettura interpretativa** — registrata il 2026-09-05. Non e' derivata dai dati.
>
> 1 sfera 2e non trova un solo incantesimo nella lista base del chierico 5e:
> Plant. Animal ne trova 1, Weather 1. Non è un difetto della mappatura:
> la 5e ha spostato piante, animali e meteo sulla lista del **druido**. Le divinità
> della natura pagano un prezzo che non dipende da quanto erano ricche in 2e ma da
> dove la 5e ha messo quel materiale.

---

## Le 21 divinità

| divinità | famiglia | rango |
|---|---|---|
| Branchala (Song of Life) | good | intermediate |
| Chemosh (Lord of Death) | evil | intermediate |
| Chislev (the Beast) | neutral | intermediate |
| Gilean (the Void) | neutral | greater |
| Habbakuk (Fisher King) | good | intermediate |
| Hiddukel (Prince of Lies) | evil | intermediate |
| Kiri-Jolith (Sword of Justice) | good | intermediate |
| Lunitari (Veiled Maiden) | neutral | intermediate |
| Majere (Master of Mind) | good | intermediate |
| Mishakal (Healing Hand) | good | greater |
| Morgion (Black Wind) | evil | intermediate |
| Nuitari (Devouring Dark) | evil | intermediate |
| Paladine (the Dragon's Lord) | good | greater |
| Reorx (the Forge) | neutral | greater |
| Sargonnas (Dark Vengeance) | evil | greater |
| Shinare (Winged Victory) | neutral | intermediate |
| Sirrion (Flowing Flame) | neutral | intermediate |
| Solinari (Mighty Hand) | good | intermediate |
| Takhisis (Queen of Darkness) | evil | greater |
| Zeboim (Darkling Sea) | evil | intermediate |
| Zivilyn (World Tree) | neutral | intermediate |

I tre dei della magia coincidono con le tre Vesti: Solinari/Bianche,
Lunitari/Rosse, Nuitari/Nere.

---

## Verifiche pre-conversione

Rapporti completi in `dati/RAPPORTO-soddisfacibilita.md` (array e point-buy) e
`dati/RAPPORTO-montecarlo.md` (tiro dei dadi).

### Probabilità di qualificazione — Monte Carlo, 200.000 iterazioni

Sui soli vincoli razziali:

| razza | qualificati |
|---|---:|
| Irda (Alto Ogre) | 65,68% |
| Elfo Kagonesti | 91,14% |
| Nano delle Colline (Neidar) | 91,91% |
| Elfo Qualinesti | 92,04% |
| Gnomo (Minoi) | 92,84% |
| Mezzelfo | 94,30% |
| Minotauro | 96,42% |
| Elfo Silvanesti | 99,32% |
| Barbaro | 99,34% |
| Nano delle Montagne (Hylar / Daewar) | 99,63% |
| Kender | 99,85% |
| Elfo Dargonesti (Elfo degli Abissi) | 99,92% |
| Elfo Dimernesti (Elfo dei Bassifondi) | 99,92% |
| Nano Sozzo (Aghar) | 100,00% |
| Umano | 100,00% |

Percorsi cavallereschi (`cavaliere` è la classe generica, non un grado dell'Ordine):

| razza | classe | qualificati |
|---|---|---:|
| Nano delle Montagne (Hylar / Daewar) | `cavaliere` | 12,54% |
| Umano | `cavaliere` | 12,50% |
| Elfo Dargonesti (Elfo degli Abissi) | `cavaliere` | 12,46% |
| Elfo Dimernesti (Elfo dei Bassifondi) | `cavaliere` | 12,46% |
| Barbaro | `cavaliere` | 12,32% |
| Irda (Alto Ogre) | `cavaliere` | 1,23% |
| Umano | `cavaliere-corona` | 97,92% |
| Mezzelfo | `cavaliere-corona` | 92,95% |
| Mezzelfo | `cavaliere-rosa` | 33,36% |
| Umano | `cavaliere-rosa` | 27,53% |
| Umano | `cavaliere-spada` | 84,89% |
| Mezzelfo | `cavaliere-spada` | 83,33% |

Combinazioni sotto l'1%:

| razza | classe | qualificati | frequenza |
|---|---|---:|---:|
| Nano Sozzo (Aghar) | `barbaro` | 0,249% | 1 ogni 402 |

> **Lettura interpretativa** — registrata il 2026-09-05. Non e' derivata dai dati.
>
> **Perché si tira.** Sotto point-buy due percorsi erano matematicamente
> impossibili — il Cavaliere e il Cavaliere della Rosa — e il Nano Sozzo non aveva
> alcuna disposizione valida con l'array standard. Con 4d6 scarta il minore
> nessuno di questi è più impossibile: tornano rari, che è il comportamento
> originale della 2e. I requisiti non sono stati ammorbiditi.
>
> La **Corona** misura l'accesso all'intero percorso solamnico, non l'avanzamento:
> passa il 97,92% degli umani e il 92,95% dei mezzelfi. Diventare cavaliere
> è facile; diventare Cavaliere della Rosa no (27,53% e 33,36%).
>
> L'unica combinazione sotto l'1% ha un collo di bottiglia esatto e verificabile a
> mano: il barbaro richiede Costituzione 12 e l'Aghar tira la Costituzione con
> 3d4, quindi serve il massimo assoluto sui tre dadi, 1 possibilità su 64.
> Moltiplicata per gli altri requisiti dà lo 0,248% per via analitica — l'unico
> numero di questo documento calcolato a mano — contro lo
> 0,249% misurato dalla simulazione.
>
> La razza più selettiva sui soli vincoli è l'**Irda (Alto Ogre)** (65,68%).

---

## Tratti razziali — 105 in tutto

### Per stato di conversione

| stato | tratti | quota |
|---|---:|---:|
| `direct` | 35 | 33% |
| `adapted` | 58 | 55% |
| `pending` | 0 | 0% |
| `source_only` | 12 | 11% |

### Per provenienza

| fonte | tratti | quota |
|---|---:|---:|
| PHB 2e (per rimando) | 70 | 67% |
| Tales of the Lance | 20 | 19% |
| MC Dragonlance Appendix | 11 | 10% |
| conversione editoriale nostra | 3 | 3% |
| SotDQ (ufficiale 5e) | 1 | 1% |

### Per razza

| razza | totale | PHB 2e | Tales of the Lance | Appendice | editoriali | SotDQ |
|---|---:|---:|---:|---:|---:|---:|
| Elfo Dargonesti (Elfo degli Abissi) | 10 | 7 | 2 | 1 | 0 | 0 |
| Elfo Dimernesti (Elfo dei Bassifondi) | 9 | 7 | 2 | 0 | 0 | 0 |
| Gnomo (Minoi) | 9 | 8 | 1 | 0 | 0 | 0 |
| Nano Sozzo (Aghar) | 9 | 7 | 2 | 0 | 0 | 0 |
| Elfo Kagonesti | 8 | 7 | 0 | 1 | 0 | 0 |
| Elfo Silvanesti | 8 | 7 | 0 | 1 | 0 | 0 |
| Nano delle Colline (Neidar) | 8 | 7 | 1 | 0 | 0 | 0 |
| Nano delle Montagne (Hylar / Daewar) | 8 | 7 | 1 | 0 | 0 | 0 |
| Elfo Qualinesti | 7 | 7 | 0 | 0 | 0 | 0 |
| Kender | 7 | 0 | 5 | 1 | 0 | 1 |
| Mezzelfo | 7 | 6 | 1 | 0 | 0 | 0 |
| Minotauro | 6 | 0 | 1 | 5 | 0 | 0 |
| Irda (Alto Ogre) | 4 | 0 | 2 | 2 | 0 | 0 |
| Umano | 3 | 0 | 0 | 0 | 3 | 0 |
| Barbaro | 2 | 0 | 2 | 0 | 0 | 0 |

> **Lettura interpretativa** — registrata il 2026-09-05. Non e' derivata dai dati.
>
> Su 105 tratti, 70 vengono dal PHB 2e (67%) e
> 32 dalle fonti di Krynn (30%). La densità apparente di una
> razza misura quindi in buona parte l'appartenenza a una stirpe del PHB, non la
> profondità con cui il setting l'ha caratterizzata.
>
> I 3 tratti di conversione editoriale non sono di Krynn: sono nostri, marcati
> `editorial: True` e reversibili.
>
> Il roster va da 2 a 10 tratti per razza. Le razze native di Krynn — Kender,
> Minotauro, Irda — non ereditano nulla dal PHB e restano nella fascia bassa
> nonostante le integrazioni dall'Appendice.

### Tratti provvisori

Nessuno.

### Tratti di conversione editoriale

- **Umano**: Adattabilita'
- **Umano**: Versatilita'
- **Umano**: Lingua franca

---

## Divergenze da SotDQ (decisione 25, `statuto-sotdq`)

*Shadow of the Dragon Queen* è in libreria ed è estratto. Entra come **quinta
provenienza** nel campo fonte dei tratti di `mechanics_5e`, accanto a PHB 2e,
Tales of the Lance, MC Appendix e conversione editoriale nostra. Lo schema
resta a due strati: `source_2e` non si tocca mai.

Non è autoritativo su tutto: non è la conversione ufficiale del materiale 2e,
è un prodotto 5e scritto da zero che ne condivide i nomi. Le sue scelte sono
un'interpretazione parallela.

### Dove SotDQ prevale (2)

| id | soggetto | punto | ufficiale | nostro | governa |
|---|---|---|---|---|---|
| `kender-schernire` | kender | Schernire (Taunting) | SotDQ pag. 27: azione bonus, raggio 60 piedi, TS su Saggezza, usi limitati per riposo lungo. Meccanicamente pi… | Era: azione bonus, raggio 30 piedi, TS su Saggezza, nessun limite di usi. RITIRA… | dec. 25.A |
| `kender-nome-tratto` | kender | nome del secondo tratto | "Kender Aptitude" (pag. 27 stampata). | Nessun tratto corrispondente: la competenza a scelta non e' nel nostro roster ke… | dec. 25 — annotazione |

### Dove divergiamo (6)

| id | soggetto | punto | ufficiale | nostro | governa |
|---|---|---|---|---|---|
| `kender-aggiustamenti` | kender | aggiustamenti di caratteristica | Nessun aggiustamento fisso: "increase one of those scores by 2 and increase a different score by 1, or increas… | DES +1, dal capitolo razziale di Tales of the Lance. | dec. 2 |
| `kender-velocita` | kender | velocita' | 30 piedi. | 25 piedi, derivati dal tasso MV 9 della 2e. | dec. 13/14 (velocita' dai tassi MV) |
| `kender-scurovisione` | kender | scurovisione | Nessuna scurovisione. | 30 piedi, convertiti dall'infravisione dichiarata dalla 2e. | dec. 14 |
| `cavalieri-solamnia` | cavaliere-corona, cavaliere-spada, cavaliere-rosa | struttura dell'ordine | I Cavalieri di Solamnia sono un BACKGROUND piu' una catena di talenti (Squire of Solamnia, Knight of the Crown… | Tre classi in sequenza obbligata Corona -> Spada -> Rosa, con ingresso al 1°, 3°… | dec. 5 |
| `maghi-alta-stregoneria` | mago-alta-stregoneria, mago-veste-bianca/rossa/nera | struttura dell'ordine | Background "Mage of High Sorcery" piu' i talenti Initiate of High Sorcery e Adept of the White/Red/Black Robes… | Classe base Mago dell'Alta Stregoneria; le tre Vesti sono affiliazioni dichiarat… | dec. 6 |
| `divinita-sfere` | tutte e 21 | sfere e rango | Le stesse 21 divinita', con `province` (ambito narrativo) e `symbol`. Nessuna sfera, nessun rango. | Sfere maggiori e minori dalla 2e, piu' rango greater/intermediate/lesser. Il fil… | dec. 24 |

Registro interrogabile in `dati/_divergenze_sotdq.py`.

### Dove SotDQ è fonte unica (4)

Contenuto che in 2e non esiste: nessun conflitto possibile. **Registrato come
disponibile, non estratto.**

| id | cosa | stato |
|---|---|---|
| `lunar-sorcery` | Sottoclasse Lunar Sorcery per lo Stregone | disponibile, non estratto |
| `talenti-krynn` | Nove talenti: Divinely Favored, Initiate of High Sorcery, Adept of the Black/Red/White Robes, Squire of Solamnia, Knight of the Crown/Rose/Sword | disponibile, non estratto |
| `background-krynn` | Due background: Knight of Solamnia, Mage of High Sorcery | disponibile, non estratto |
| `mostri-sotdq` | Mostri e PNG di Krynn con statistiche 5e | disponibile, non estratto — vedi RAPPORTO-mostri.md |

---

## Il bestiario — diagnostica

Rapporto completo in `dati/RAPPORTO-bestiario.md`. **52 creature convertite** in `dati/mostri/` (le altre restano da fare: vedi "Il conteggio vero del bestiario" e "Parte 5" nel rapporto per il numero, che non è ancora definitivo).

**La scheda mostro 2e ha 21 campi**: 2 passano diretti in 5e, 12 vanno
convertiti, **7 non hanno alcun corrispettivo** — FREQUENCY, ORGANIZATION, ACTIVITY CYCLE, DIET, NO. APPEARING, MAGIC RESISTANCE, MORALE.

**I cinque draconici** sono le uniche creature con scheda in entrambe le
edizioni, quindi l'unico precedente di conversione verificabile.

| | |
|---|---|
| ordine di potenza in 2e (per PE) | Baaz → Kapak → Bozak → Sivak → Aurak |
| ordine di potenza in 5e (per GS) | Baaz → Bozak → Kapak → Sivak → Aurak |

**Bozak e Kapak si scambiano di posto.** Non è l'unico segnale: il Kapak rompe
anche il rapporto PF/DV, che sugli altri quattro sta fra 8.4 e 11 e su di lui
arriva a 13.0, e moltiplica il danno per round per 9.6 contro il ×1.6–×4.0
degli altri quattro.

### Perché la regola fallisce proprio sul Kapak

In 5e il **Grado di Sfida è la media fra componente difensiva e componente
offensiva**. Il Kapak ha **39 punti ferita contro una mediana SRD di 58** al
suo grado: sta *sotto* la mediana in difesa e ci arriva col danno, 24 per
round. È un cannone di vetro, e in 2e non lo era — era un assassino con **un**
attacco da 1-4.

`GS = DV − 2` presuppone che la creatura conservi il proprio profilo difensivo,
perché i dadi vita della 2e misurano solo la resistenza. **Il Kapak ha cambiato
asse.**

> **Lettura interpretativa** — registrata il 2026-09-05. Non e' derivata dai dati.
>
> **Non esiste una formula estraibile da cinque casi.** Una regolarità si
> intravede — grado di sfida uguale ai dadi vita meno due — e tiene per quattro
> draconici su cinque, ma il quinto non è un arrotondamento: è una
> riprogettazione.
>
> Una precisazione che i numeri impongono: il Kapak non è l'unico sotto la
> mediana difensiva. Lo sono quattro su cinque, e in modo crescente col grado —
> Bozak al 89%, Kapak e Sivak al 67%, Aurak al 59%. **I draconici sono una
> famiglia di creature fragili e offensive**, per scelta di design. Quello che è
> unico del Kapak è il **salto offensivo rispetto alla propria fonte**: gli altri
> sono stati riscalati, lui è stato ripensato.
>
> Applicare quell'euristica alle 43 creature restanti sposterebbe il tempo
> dalla conversione al debug. Quello che i cinque casi danno non è un algoritmo
> ma tre vincoli:
>
> 1. l'ordinamento si conserva **ma solo finché si conserva il ruolo** — il
>    controllo da fare prima di fidarsene è sul ruolo, non sui numeri;
> 2. l'effetto identitario va riscritto con un tiro salvezza;
> 3. i danni per round vanno almeno raddoppiati.
>
> La strada che i dati indicano è la **conversione per analogia** con l'SRD, non
> per calcolo.

### I sette campi senza corrispettivo, risolti (decisione 27, `sette-campi-2e`)

| gruppo | campi | quali | esito | destinazione |
|---|---:|---|---|---|
| **A** | 5 | `frequency`, `no_appearing`, `organization`, `activity_cycle`, `diet` | chiuso senza deliberare | `generatore_incontri`, Fase 3 |
| **B** | 1 | `morale` | chiuso senza deliberare | `ia_combattimento`, Fase 2 |
| **C** | 1 | `magic_resistance` | RINVIATA alla Fase 2 | in Fase 2 |

### Schema del mostro

`dati/schema/mostro.schema.json`, sul modello di razze e classi: `source_2e`
accoglie tutti e ventuno i campi della scheda 2e, `mechanics_5e` ha la forma di
uno statblock con stato di conversione e provenienza su ogni elemento. Due campi
nuovi rispetto alle razze: **`ruolo`**, che serve alla conversione per analogia e
all'IA di combattimento, e **`morale_2e`**, che porta il gruppo B della
decisione 27 (`sette-campi-2e`).

**Validato sui cinque draconici**, l'unico caso in cui entrambi gli strati sono
già noti da fonte: cinque su cinque conformi, zero errori. `dati/mostri/` non
esiste ancora — la validazione è un test dello schema, non una conversione.

### Il conteggio vero, rifatto voce per voce

Il numero ricavato dal testo estratto era sbagliato. Rifatto sulle immagini di
pagina:

| | |
|---|---:|
| voci dell'MC Appendix | **66** |
| creature vere (statblock distinti) | **87** |
| schede di razze già in `dati/razze/` | 14 |
| razze e culture fuori dal roster | 4 |
| **creature da convertire** | **66** |

**14 voci hanno lo statblock su più colonne** — una voce, più creature:

| voce | pag. | creature |
|---|---:|---|
| **Avian** | 4 | 4 — Emre, Kingfisher, Skyfisher, 'Wari |
| **Dragon, Astral** | 20 | 2 — Astral Dragon (unmated), Astral Dragon (mated pair) |
| **Man (of Krynn)** | 59 | 4 — Ice Folk, Knights of Solamnia, Plainsmen, Rebels |
| **Shadowperson** | 71 | 2 — Shadowperson, Revered Ancient One |
| **Stag** | 78 | 3 — Wild Stag, Giant Stag, The White Stag |
| **Tayling** | 79 | 2 — Tayling, Taylang |
| **Centaur (of Krynn)** | 7 | 4 — Centaur, Abanasinian, Centaur, Crystalmir, Centaur, Endscape, Centaur, Wendle |
| **Beast, Undead** | 6 | 2 — Stahnk, Gholor |
| **Hatori** | 46 | 2 — Lesser Hatori, Greater Hatori |
| **Insect Swarm** | 50 | 2 — Velvet Ant Swarm, Grasshopper and Locust Swarm |
| **Lizard Man (of Krynn)** | 57 | 2 — Jarak-Sinn, Bakali |
| **Ogre (of Krynn)** | 65 | 2 — Ogre, Orughi |
| **Phaethon** | 69 | 2 — Phaethon, Elder Phaethon |
| **Spider (of Krynn)** | 77 | 2 — Whisper Spider, Giant Trap Door Spider |

**8 nomi di voce erano sbagliati** nel testo estratto, non i quattro noti.

> **Lettura interpretativa** — registrata il 2026-09-05. Non e' derivata dai dati.
>
> **L'estrazione non ha solo sbagliato i nomi: ha perso dei dati.** In tre voci
> le colonne di destra sono sparite del tutto — `Avian` aveva quattro uccelli e ne
> restavano due, `Stag` tre cervi e ne restava uno, `Man (of Krynn)` quattro
> culture e ne restavano due. Sono sette creature che dal testo estratto non
> esistevano.
>
> Il conteggio passa da 66 a **87**: il 32% in più. Fra i ritrovamenti c'è il
> **Cervo Bianco**, che non è una bestia ma una creatura sacra unica da 2.000 punti
> esperienza, con capacità magiche.
>
> **L'ordine di lavorazione proposto va rivisto**: è stato formulato prima del
> ricontaggio e non contiene le sette creature nuove.

---

## Materiale esterno — chiuso (decisione 26, `criterio-tracciabilita`)

**Criterio generale, da applicare a qualunque lotto futuro:**

> Qualsiasi materiale esterno che non porti con se' FONTE e PAGINA e' inutilizzabile, a prescindere dal resto della sua qualita'.

Si applica in tre passi, e il primo di solito basta: (1) le voci dichiarano
fonte e pagina? (2) la copertura è sopra il 90%? (3) le sigle di fonte sono
più di una — allora è un corpus, non un documento.

| lotto | voci | con fonte | con pagina | esito |
|---|---:|---:|---:|---|
| `import/json-personali/` | 19.760 | 18.457 | 13.277 | **respinto** |
| `import/json-personali-veri/` | 19.288 | 0 | 0 | **respinto** |

In `import/json-personali/` ci sono **442 file JSON, 88 MB, 19.760 voci** da **146 sigle di fonte**. Inventario completo in `import/RAPPORTO-json-personali.md`.

**Statuto non deciso. Non è integrato, non è convertito, `dati/` non è stato toccato.**

Cosa contiene, in sintesi: 3.816 mostri, 549 incantesimi, 1.667 oggetti, 118 talenti, 101 background, 19 classi 5e con 138 sottoclassi. Include **Shadow of the Dragon Queen** (199 voci), l'unica fonte 5e ufficiale su Krynn, che finora risultava mancante.

Tre cose da sapere prima di decidere:

1. **Non è un'estrazione dai manuali cartacei**: è il dump della cartella dati di 5etools. Lo dice il `changelog.json`, che contiene il diario di sviluppo del sito fino alla versione 1.218.3.
2. **Non separa il dato di fonte dalle aggiunte dello strumento.** Nello stesso oggetto convivono i valori del manuale, indici generati per i filtri e metadati di prodotto. Il 10,7% delle voci è per giunta **derivato** con `_copy`, cioè non esiste come testo.
3. **Dove si sovrappone ai nostri dati, diverge.** L'unica razza in comune è il Kender, e diverge su velocità, aggiustamenti e forma di *Schernire*. Le 21 divinità hanno gli stessi nomi ma nessuna sfera.

### `import/json-personali-veri/` — verificato, respinto

7 file, 35 MB, 19.288 voci. I file dichiarano `"dataset_author": "marchez"` e `"custom handwritten dataset"`. **Non è l'SRD 5.1 e non è una trascrizione**: il perimetro è sforato in **9 categorie su 9** — 3.816 mostri contro i 325 dell'SRD, 138 sottoclassi contro 12, 160 avventure contro zero. Dentro `miscellaneous_data.json` c'è il **changelog di sviluppo di 5etools** con 607 voci fino alla versione 1.218.3, più i template del convertitore del sito. Verifica completa in `import/RAPPORTO-json-veri.md`.

**È lo stesso corpus di `json-personali/`**, riorganizzato in sette file con le chiavi rinominate: mostri, incantesimi, oggetti e sottoclassi coincidono voce per voce. La ripulitura ha cancellato `source` e `page` da tutte e 19.288 le voci, lasciando intatti gli indici interni al sito: **il lotto originale è preferibile a questo**. Resta dov'è.

### `Musica/` — accantonato

34 MP3, 118 MB, **4h 18m** di colonna sonora per *Shadow of the Dragon Queen*. **Non serve ora e non va integrata**: la Fase 2 è il motore di combattimento, l'audio viene molto dopo.

I metadati ID3 non dichiarano né autore né etichetta né provenienza: l'unico campo presente è l'identificativo del programma che ha codificato i file. Tutti e 34 i nomi contengono un identificativo video di undici caratteri fra parentesi quadre, e 12 titoli nominano **Connor Ragas** come autore. Nessuna lavorazione.

---

## Lo schema Personaggio — diagnostica pre-progetto

Rapporto completo in `dati/RAPPORTO-personaggio.md`, generato da
`dati/analizza_personaggio.py`. **Nessuno schema è stato scritto e nessuna
delle tre decisioni sospese è stata sciolta**: questa è la misura del
problema, non la soluzione.

### La differenza rispetto alle altre sei entità

Razza, classe, divinità, mostro, oggetto e modello descrivono dati immutabili.
Un personaggio è **stato che evolve**, e la differenza si misura: delle
14 grandezze che cambiano durante il gioco, **8
cambiano entro un singolo turno** e nessuna ha oggi un campo in cui stare.
Nessuna delle sei entità esistenti ha un solo campo che cambi in partita.

Un personaggio non ha inoltre una fonte da cui essere convertito: **non esiste
un `source_2e` di un personaggio**. Il doppio strato della decisione 7 (`doppio-strato`), riusato
senza attriti per oggetto (33) e modello (38), qui per la prima volta non si
applica.

### Cosa manca per costruirne uno

Su 27 grandezze necessarie a giocare, **11
sono coperte da un campo pieno, 6 solo in parte e
10 non hanno alcun campo in nessuno schema**.

| buco | misura |
|---|---|
| Privilegi di classe `pending` | 40 su 43 |
| Privilegi del **chassis** SRD | `dati/_srd51.py` porta 5 classi × 3 campi: i *nomi* dei privilegi, non le regole |
| Classi senza chassis | 8 su 20 |
| Tabella dei punti esperienza 5e | `xp_table.applied` è `false` in 20/20, e la sostituta non esiste |
| Competenze 5e | né le 18 abilità, né quante ne concede una classe, né la categoria delle armi e delle armature |
| Slot incantesimi 5e | assenti: le uniche tabelle di slot nel progetto sono 2e |
| Effetto degli incantesimi | nessun campo per tiro salvezza, danno, area: sta in `descrizione`, in prosa |
| Cambio fra le valute | 4/20 classi dichiarano una ricchezza in **stl**, gli oggetti costano in **gp**, nessun campo lega le due |
| `allowed_classes` → classi | 17 etichette, di cui 8 coincidono con un `name.en`: il legame esiste come parola, non come chiave |

### Le tre decisioni sospese

Riportate nel rapporto con fonte e opzioni, **non decise**.

1. **Barbaro razza o background** (decisione 20, `tappo-barbaro`). Le quattro conseguenze già
   elencate dalla decisione sono tutte verificabili nei dati.
2. **Tetti di crescita** (decisione 10, `massimali-razziali`). 84 tetti su
   90 stanno sotto il soffitto 20 della 5e, e il chassis più
   generoso (Fighter) concede 7 aumenti di
   caratteristica. La decisione dice *che* il tetto morde, non *cosa succede al
   punto che lo supera* — e la fonte non può dirlo, perché in AD&D 2e il caso
   non esisteva.
3. **Generazione** (decisione 8, `generazione-caratteristiche`). `motore/generazione.py` copre i tre metodi e
   la soddisfacibilità; non assegna i valori, non compone il point-buy con le
   formule razziali, e legge `source_2e` invece di `mechanics_5e`.

### Il vincolo dell'arena

Il corpus intero pesa **1,94 MB**: sta in memoria, e a ogni turno non
serve leggere alcun file. Il vincolo non è la velocità — è che
**380 blocchi di meccanica su 405 sono
ancora solo prosa italiana** e non numeri, su un totale di
257 fra azioni e tratti dei mostri, 105 tratti
razziali e 43 privilegi di classe. I 25 che
portano anche un campo `effetto` sono la fetta verticale: i privilegi del
chassis Fighter e le azioni dei due mostri con cui l'arena gira davvero
(`motore/arena.py`, `dati/RAPPORTO-arena.md`).

---

## Questioni aperte

### Richiedono una decisione

> **Lettura interpretativa** — registrata il 2026-09-05. Non e' derivata dai dati.
>
> - **Il PHB 5e 2014 non e' fra i PDF** (`phb-2014-assente`). La cartella contiene solo edizioni 2024. Alternativa disponibile: `2014.5e.tools`, che espone il materiale 2014 come JSON strutturato (repo GitHub `5etools-mirror-3/5etools-2014-src`).
> - ***Shadow of the Dragon Queen* continua a mancare** (`sotdq-assente`). Resta l'unica fonte 5e ufficiale su Krynn, e da essa dipende l'unico tratto ancora provvisorio.
> - **Il Barbaro ha doppia natura** (`barbaro-background`). Il manuale lo tratta sia come cultura umana sia come classe. La decisione 20 (`tappo-barbaro`) gli ha dato un tappo reversibile; la conversione a background va decisa insieme allo schema Personaggio. Le quattro conseguenze sono misurate in `dati/RAPPORTO-personaggio.md`. La decisione 56 (`personaggio-additivo`) non la scioglie: garantisce solo che deciderla dopo non costi una riscrittura.
> - **Cosa succede a un aumento che sfonda un tetto razziale** (`aumento-oltre-tetto`). La decisione 10 (`massimali-razziali`) applica i massimali anche in crescita ma non dice come si comporta l'aumento respinto: si perde, si travasa, o il tetto cede. La fonte non ha una risposta da trascrivere — in AD&D 2e il caso non si poneva.
> - **Il Qualinesti ha un tratto che registra un'assenza** (`qualinesti-tratto-vuoto`). L'Appendice non dichiara alcuna capacita' per quel ramo, e il posto e' tenuto da una voce `source_only` senza meccanica. Nelle tabelle conta come un tratto dell'Appendice pur non concedendo nulla: e' un artefatto di rappresentazione, non un beneficio. Da decidere se tenerlo come registrazione esplicita o toglierlo e lasciare il conteggio a zero.
> - **Il Cavaliere della Rosa e l'Aura di Coraggio** (`rosa-aura-di-coraggio`). L'immunita' alla paura che la fonte 2e concede al grado e' gia' un privilegio del chassis Paladino, e `mechanics_5e` la porta come rimando verificabile invece che come `null`. Il chassis pero' la concede molto piu' tardi del livello a cui si entra nel grado: da decidere se anticiparla all'ingresso, lasciarla dov'e', o dichiarare che il grado non la concede affatto finche' il chassis non arriva. I due livelli stanno nel dato — `_chassis_5e.STATO_PRIVILEGI` e la tabella SRD del Paladino — e non si ricopiano qui. E' un caso particolare di questione aperta (`gradi-solamnici-forma`).
> - **Come si rappresentano i tre gradi solamnici in 5e** (`gradi-solamnici-forma`). La decisione 5 (`cavalieri-solamnia`) ha fissato la sequenza obbligata Corona → Spada → Rosa, ma non la forma che prende in un sistema che non ha il concetto di grado: classe unica con stadi interni, tre sottoclassi in sequenza (che la 5e non prevede), o classe base piu' un sistema di gradi separato. Le tre opzioni sono in `dati/RAPPORTO-classi.md` §3.9, ed e' l'unica delle nove incompatibilita' strutturali rimasta senza esito.
> - **Il livello delle Vesti contro il livello della sottoclasse** (`vesti-livello-sottoclasse`). La decisione 6 (`maghi-delle-torri`) colloca il giuramento alla Veste al livello del Test; la 5e assegna la sottoclasse del Mago un livello prima. Lo scarto e' di un livello solo — si sposta il Test, si tiene la sottoclasse vuota per un livello, o si accetta lo scarto — e finche' non e' deciso le tre Vesti restano affiliazioni senza un aggancio meccanico. Diagnosi in `dati/RAPPORTO-classi.md` §2.
> - **Il Dargonesti e le classi che la fonte non gli assegna** (`dargonesti-senza-elenco`). La tabella Class/Race Combinations elenca il solo Dimernesti; le Gaming Notes equiparano le due razze per requisiti e aggiustamenti e tacciono sulle classi. Oggi `allowed_classes.applied` e' `false`, che la decisione 58 (`telaio-apre-classe-filtra`) legge come assenza di vincolo e apre il roster intero: l'esito piu' largo possibile, prodotto da un buco della fonte e non da una scelta. Le opzioni sono tre e non due — ereditare l'elenco del Dimernesti, leggere le classi che il paragrafo sugli elfi del mare elenca davvero, o lasciare il silenzio. Misura in `dati/RAPPORTO-allowed-classes.md`.
> - **Che chassis 5e dare al Popolano** (`chassis-commoner`). Non e' una classe 5e. Da decidere. Sede: `dati/_chassis_5e.CHASSIS["commoner"]` — la ragione si legge li' e non si ricopia qui.
> - **Che chassis 5e dare al Tinker** (`chassis-tinker`). Non e' una classe 5e. Da decidere. Sede: `dati/_chassis_5e.CHASSIS["tinker"]` — la ragione si legge li' e non si ricopia qui.
> - **Che chassis 5e dare al Sacerdote Eretico** (`chassis-sacerdote-eretico`). Per definizione non ha potere. Da decidere. Sede: `dati/_chassis_5e.CHASSIS["sacerdote-eretico"]` — la ragione si legge li' e non si ricopia qui.
> - **Che chassis 5e dare all'Handler** (`chassis-handler`). Rogue senza attacco furtivo: il chassis c'e' ma svuotato. Da decidere. Sede: `dati/_chassis_5e.CHASSIS["handler"]` — la ragione si legge li' e non si ricopia qui.
> - **Che chassis 5e dare al Marinaio** (`chassis-mariner`). Ibrido Fighter/Rogue: nessun candidato pulito. Da decidere. Sede: `dati/_chassis_5e.CHASSIS["mariner"]` — la ragione si legge li' e non si ricopia qui.

### Ambiguità delle fonti, registrate e non risolte

- **elfo-qualinesti** (razza): DECISIONE 22 (`tratto-fantasma-qualinesti`). L'Appendice Mostruosa non dichiara alcuna capacita' per il ramo Qualinesti, a differenza di Kagonesti (scatto in linea retta, pag. 35 stampata) e Silvanesti (veleno degli arcieri, pag. 34). La voce Qualinesti (pag. 33) descrive solo temperamento e armi preferite: "Qualinesti are more aggressive than Silvanesti but not as tactically sophisticated... Long swords, bows, and spears are among their preferred weapons." Tutte e tre le voci rimandano al PHB 2e per le capacita' elfiche ("have all of the special abilities of elves listed in the 2nd Edition Player's Handbook"). E' un esito, non una lacuna: i Qualinesti si distinguono dagli altri due rami per aggiustamenti e requisiti, non per capacita'. Nessuna differenza forzata.
- **gnomo-minoi** (razza): Il manuale non fornisce eta' adulta ne' longevita' per gli gnomi: rimanda al PHB 2e.
- **irda** (razza): Il manuale non dichiara infravisione per gli Irda ne' rimanda al PHB.
- **irda** (razza): Altezza e peso sono dati senza distinzione di genere. Trascritti fedelmente.
- **irda** (razza): Longevita': il testo dice "500-year lifespans" ma la formula e' 5d10+550, che da' 555-600 anni. Incoerenza del manuale; trascritta la formula.
- **mezzelfo** (razza): Il manuale non fornisce altezza, peso ne' eta' per i mezzelfi: rimanda al Player's Handbook 2e.
- **minotauro** (razza): Il manuale non fornisce peso, eta' adulta ne' longevita' per i minotauri.
- **minotauro** (razza): Non e' dichiarata infravisione, benche' i minotauri delle fonti generiche AD&D ne abbiano. Lasciato null: il manuale non lo dice e non rimanda al PHB.
- **nano-aghar** (razza): L'altezza e' data come valore unico (1d6+44, circa 4 piedi) senza distinzione di genere, mentre il peso e' differenziato. Trascritto fedelmente.
- **umano** (razza): Le etnie umane di Krynn (Solamnici, Ergothiani, Khur, Nordmaariani, Abanasinici...) non hanno statistiche distinte in questo manuale. Restano differenze puramente narrative finche' non arriva Races of Ansalon.
- **barbaro** (classe): Il manuale tratta "Barbarian" sia come cultura razziale (capitolo People of Ansalon) sia come classe (questo capitolo). I minimi coincidono nei due punti tranne che qui manca il tetto di Destrezza 16 e il tetto di Intelligenza 18 presenti nella scheda razziale.
- **cavaliere-rosa** (classe): Il manuale non chiarisce se un Cavaliere della Rosa conservi gli incantesimi acquisiti come Cavaliere della Spada. Nodo da sciogliere nella conversione 5e.
- **cavaliere-spada** (classe): La tabella incantesimi parte dal livello 6 di cavaliere, ma il manuale non dice esplicitamente che i livelli 3-5 sono privi di incantesimi: si deduce dall'assenza di righe.
- **cavaliere-spada** (classe): La tabella incantesimi stampata e' disallineata in tre righe: il livello 9 ha cinque colonne invece di sette, e i livelli 14 e 15 ne hanno sei. Verificato sull'immagine originale: il difetto e' di impaginazione del manuale. Le righe sono state lette da sinistra a destra, ottenendo 9=[3,2,0,0,0,0,0], 14=[7,5,2,1,1,1,0], 15=[8,6,3,2,1,1,0]. La lettura e' coerente con le righe 13 e 16, che sono allineate correttamente, e mantiene la progressione monotona.
- **cavaliere** (classe): La ricchezza iniziale nel testo estratto compare come "564x10 stl", chiaramente corrotta. Il manuale rimanda alla ricchezza base del gruppo Warrior, che in AD&D 2e e' 5d4x10 stl. Valore ricostruito, non letto: da confermare sull'originale.
- **mago-alta-stregoneria** (classe): Nella tabella di avanzamento il valore del 3° livello e' stampato "5.000" con un punto invece della virgola. Interpretato come 5.000 PE, coerente con la progressione.
- **mago-rinnegato** (classe): Il manuale non dice esplicitamente che i rinnegati sono esenti dalle restrizioni di scuola: e' una deduzione dal fatto che quelle restrizioni sono definite come regola d'ordine. Da confermare con Towers of High Sorcery.
- **sacerdote-eretico** (classe): Il manuale non fornisce una progressione di incantesimi per gli eretici: e' coerente con il fatto che non hanno potere reale, ma non e' detto esplicitamente che non ne abbiano alcuno.
- **sacerdote-ordini-sacri** (classe): Il manuale rimanda al PHB 2e e al Tome of Magic per le tabelle degli incantesimi. Le sfere consentite a ciascun dio sono ora estratte: vedi dati/divinita/.
- **chemosh** (divinità): La sfera Guarigione e' annotata nel manuale con un inciso invece che con il consueto asterisco: "Healing* (usually the reverse spell form)". L'inciso e' conservato nel campo note della sfera.
- **reorx** (divinità): L'unica voce del capitolo che dichiara WAL (allineamento dei fedeli) invece di PAL (allineamento del sacerdote): "AB Standard; WAL Any; ...". Verificato sull'estratto, non e' un errore di trascrizione. Da decidere se intendere "qualunque allineamento" anche per i sacerdoti.
- **sirrion** (divinità): La sfera Elementale porta un inciso restrittivo invece dell'asterisco: "Elemental (heat and fire spells only)".

---

## Struttura della cartella

```
CLAUDE.md                          regole di comportamento per le sessioni AI
dragonlance-project-reference.md   documento di design
divisione-del-lavoro.md            chi fa cosa fra questo ambiente e Cowork
CONTESTO-PROGETTO.md               questo file (generato)
RETE-domini-permessi.md            allowlist di rete del sandbox (generato)
.claude/settings.json              la stessa allowlist, in forma eseguibile
git-privato.sh                     wrapper per il repository privato
.git/         repo PUBBLICO — documenti, script, schemi, moduli SRD
.git-private/ repo PRIVATO — dati/ con source_2e, trascrizione dei manuali
manuali-mancanti.md                manuali da procurare
LEGGIMI-estrazione.md              pipeline di estrazione
Manuali/     PDF sorgenti      Testi/    testi estratti a colonne separate
import/      materiale esterno, statuto non deciso o respinto — mai in dati/
Musica/      colonna sonora, ACCANTONATA: inventariata e non lavorata
Estratti/    vecchia estrazione a colonne fuse, solo storico
riscontro/   materiale di consultazione (3.5), non fonte di verità
dati/        schema/ razze/ classi/ divinita/ + build_*.py e valida_*.py
motore/      generazione.py — tiro delle caratteristiche e validazione
```
