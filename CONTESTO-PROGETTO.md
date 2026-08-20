# Dragonlance Web GDR — contesto di progetto

*Generato da `genera_contesto.py` il 2026-08-20.*

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

**Dati strutturati**: 15 razze, 17 classi, 21 divinità, validate a zero errori. 105 tratti razziali, 0 in sospeso, 3 di conversione editoriale nostra.

---

## Le 33 decisioni prese

Ordine cronologico. Questa è la storia completa delle scelte: non serve
ricostruirla dalle sezioni.

1. **Motore** — 5e come chassis meccanico; le altre edizioni sono fonte di contenuto e lore.
2. **Edizione di riferimento** — PHB **2014**, non 2024. La 2024 rende le specie numericamente neutre, incompatibile con la decisione 3.
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
19. **Compensazione dell'umano** — L'umano aveva zero tratti e zero aggiustamenti perché in 2e era pagato dall'assenza di limiti di livello, che la decisione 4 ha abolito. Compensato con +1 a due caratteristiche a scelta, una competenza e un linguaggio, marcati come conversione editoriale.
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
30. **Precedenza fra Tales of the Lance e MC Appendix** — Prima volta che due fonti 2e si contraddicono su un tratto di personaggio giocante: dove **divergono**, prevale **Tales of the Lance**, perché è il capitolo dedicato ai PG mentre l'Appendice descrive la creatura dal punto di vista del Dungeon Master. Il criterio vale solo per la divergenza, non per l'integrazione: dove l'Appendice dichiara qualcosa su cui Tales of the Lance tace, la decisione 18 resta intatta. Applicata ai due casi kender in conflitto (bonus armi da tiro, condizione sulla Sorpresa): entrambi restano registrati come divergenza e non si applicano.
31. **Soglia degli incantesimi innati dei Dargonesti** — **Opzione C**: tre soglie scalate (3°, 5°, 7°) invece del 10° unico della fonte o di una soglia bassa unica. Il 10° livello 2e non era "tardi" — era metà carriera in un sistema che arrivava al 20° e oltre: copiarlo senza riscalarlo tradisce la sostanza pur conservando la cifra, lo stesso errore già segnalato per i valori XP del bestiario. Concentrare i tre incantesimi in un'unica soglia bassa perderebbe la gradualità che la fonte aveva scelto. Le tre soglie, leggermente più tarde del tiefling PHB 2014 (1°/3°/5°) per conservare lo scarto di "metà carriera" dentro la fascia giocabile, rientrano comunque nella decisione 16: dove la 5e ha già un equivalente per i tratti razziali con incantesimi, si copia quel modello. Il 10° livello della fonte resta intatto in `source_2e`, non riscritto.
32. **Creatura contro entità nel bestiario** — **Riformulata** dopo un primo tentativo scorretto (che confondeva "legato a un oggetto" con "unico"). Il criterio è: ha un **nome proprio e una storia** → entità (es. il Cavaliere della Morte è, nella tradizione del setting, un individuo particolare — ma la voce dell'Appendice stessa descrive un **tipo** ripetibile, "a Knight of Solamnia, cursed...", non un nome). È un **tipo/procedura ripetibile**, anche se potente e vincolato a un oggetto magico → creatura, si converte come le altre al suo vero grado di sfida. Il Warrior Skeleton (uno stregone lega l'anima di un guerriero potente a un diadema: procedura ripetibile, diademi e guerrieri diversi) è quindi una creatura, non un'entità unica. Il diadema di controllo non va rimandato alla Fase 3: è materiale da arena giocabile (raggio, condizione di perdita, inseguimento a velocità doppia), non colore descrittivo. La categoria entità resta per ora **vuota**: nessuna delle 62 voci lette ci è ricaduta, il criterio ha retto respingendo l'unica candidata.
33. **Schema oggetti a parte** — `dati/schema/oggetto.schema.json`, stessa architettura a doppio strato di razze/classi/mostri. Il diadema dello Scheletro Guerriero non poteva restare dentro il mostro: è riutilizzabile su guerrieri diversi (decisione 32), quindi appartiene a sé quanto una spada appartiene a chi la impugna. Lo schema copre tre casi, non uno: equipaggiamento ordinario (armi/armature/attrezzatura — il buco più urgente per l'arena, dove oggi mancano perfino i danni di una spada lunga), oggetti magici, e oggetti con una creatura legata. Il diadema è il primo caso concreto, non il modello: gli altri due casi restano da popolare. Nel mostro resta un riferimento all'oggetto (`mechanics_5e.oggetti_collegati` di mostro.schema.json), non l'oggetto stesso.

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

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
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

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
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

## Le 17 classi

| id | classe | gruppo | note |
|---|---|---|---|
| `barbaro` | Barbaro | Warrior | — |
| `cavaliere-corona` | Cavaliere della Corona | Warrior | grado 1 dell'ordine; solo umano/mezzelfo; Lawful Good |
| `cavaliere-rosa` | Cavaliere della Rosa | Warrior | grado 3 dell'ordine; si entra al 4°; solo umano/mezzelfo; Lawful Good |
| `cavaliere-spada` | Cavaliere della Spada | Warrior | grado 2 dell'ordine; si entra al 3°; solo umano/mezzelfo; Lawful Good |
| `cavaliere` | Cavaliere | Warrior | Qualunque allineamento buono |
| `commoner` | Popolano | Normal | — |
| `con-artist` | Truffatore / Prestigiatore | Rogue | — |
| `handler` | Handler | Rogue | solo kender |
| `mago-alta-stregoneria` | Mago dell'Alta Stregoneria | Wizard | Determinato dalla veste: Bianca=buono, Rossa=neutrale, Nera=malvagio. L'allineamento va dichiarato al 3° livello, prima del Test. |
| `mago-rinnegato` | Mago Rinnegato | Wizard | — |
| `mago-veste-bianca` | Mago delle Vesti Bianche | Wizard | si entra al 3°; Buono |
| `mago-veste-nera` | Mago delle Vesti Nere | Wizard | si entra al 3°; Malvagio |
| `mago-veste-rossa` | Mago delle Vesti Rosse | Wizard | si entra al 3°; Neutrale |
| `mariner` | Marinaio | Warrior | Qualunque tranne Legale Buono |
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
| Marinaio | Warrior | d10 | del gruppo | — | 1 | 1 | **indeciso** |
| Mago dell'Alta Stregoneria | Wizard | 1d4 | propria, 25 liv. | sì | 3 | 4 | `Wizard` |
| Mago Rinnegato | Wizard | 1d4 | propria, 25 liv. | sì | 1 | 2 | `Wizard` |
| Mago delle Vesti Bianche | Wizard | 1d4 | del gruppo | — | 0 | 1 | **indeciso** |
| Mago delle Vesti Nere | Wizard | 1d4 | del gruppo | — | 0 | 1 | **indeciso** |
| Mago delle Vesti Rosse | Wizard | 1d4 | del gruppo | — | 0 | 1 | **indeciso** |
| Sacerdote Eretico | Priest | 1d8 | propria, 25 liv. | — | 0 | 2 | **indeciso** |
| Sacerdote degli Ordini Sacri delle Stelle | Priest | 1d8 | propria, 25 liv. | sì | 0 | 1 | `Cleric` |
| Truffatore / Prestigiatore | Rogue | d6 | del gruppo | — | 1 | 1 | `Rogue` |
| Handler | Rogue | d6 | del gruppo | — | 0 | 3 | **indeciso** |
| Popolano | Normal | d6 | propria, 25 liv. | — | 0 | 0 | **indeciso** |
| Tinker | Normal | d6 | propria, 25 liv. | — | 0 | 1 | **indeciso** |

Su 17 classi: **19 privilegi** e **24 impedimenti**. Solo 7 privilegi sono
agganciati a un livello esplicito; per gli altri 12 la fonte non dice quando si
ottengano.

- **8 classi non hanno tabella di esperienza propria** e rimandano al gruppo: Barbaro, Cavaliere, Truffatore / Prestigiatore, Handler, Mago delle Vesti Bianche, Mago delle Vesti Nere, Mago delle Vesti Rosse, Marinaio.
- **8 classi non hanno alcun privilegio**: Popolano, Handler, Mago delle Vesti Bianche, Mago delle Vesti Nere, Mago delle Vesti Rosse, Sacerdote Eretico, Sacerdote degli Ordini Sacri delle Stelle, Tinker.
- **9 classi hanno più impedimenti che privilegi.**
- Le tabelle arrivano al **25° livello**, cinque oltre il tetto della 5e.
- **Nessuna classe ha una tabella di THAC0 o di tiri salvezza**: valgono quelle di
  gruppo del PHB 2e, che non sono ancora nei dati.

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> Le classi di Krynn non sono classi nel senso della 5e: sono profili di
> restrizione appoggiati sulle classi base della 2e. Convertirle non è un lavoro di
> traduzione ma di riempimento — non c'è quasi nulla da tradurre. È la ragione della
> decisione 23.

### Chassis applicati (decisione 23)

**9 classi su 17** sono cloni meccanici di una classe SRD 5.1: Cleric ×1, Fighter ×3, Paladin ×2, Rogue ×1, Wizard ×2.
**8 restano senza chassis**, per decisione: Popolano, Handler, Mago delle Vesti Bianche, Mago delle Vesti Nere, Mago delle Vesti Rosse, Marinaio, Sacerdote Eretico, Tinker.

Le sette incompatibilità strutturali sono risolte in `mechanics_5e.structural`,
uguali per tutte le classi: tabella PE unica, bonus di competenza al posto del
THAC0, cinque categorie di tiro salvezza mappate sulle sei caratteristiche,
competenze per categoria, pacchetti fissi, troncamento al 20°, titoli
descrittivi.

Stato dei 43 privilegi e impedimenti della fonte:
**2** `direct`, **40** `pending`, **1** `source_only`.
I `pending` sono il lavoro che resta: la decisione 23 autorizza il clone del
chassis, non l'invenzione di meccanica 5e per i privilegi.

---

## Sfere sacerdotali (decisione 24)

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

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
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

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
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

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
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

## Divergenze da SotDQ (decisione 25)

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

Rapporto completo in `dati/RAPPORTO-bestiario.md`. **4 creature convertite** in `dati/mostri/` (le altre restano da fare: vedi "Il conteggio vero del bestiario" e "Parte 5" nel rapporto per il numero, che non è ancora definitivo).

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

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
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
> Applicare quell'euristica alle 42 creature restanti sposterebbe il tempo
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

### I sette campi senza corrispettivo, risolti (decisione 27)

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
decisione 27.

**Validato sui cinque draconici**, l'unico caso in cui entrambi gli strati sono
già noti da fonte: cinque su cinque conformi, zero errori. `dati/mostri/` non
esiste ancora — la validazione è un test dello schema, non una conversione.

### Il conteggio vero, rifatto voce per voce

Il numero ricavato dal testo estratto era sbagliato. Rifatto sulle immagini di
pagina:

| | |
|---|---:|
| voci dell'MC Appendix | **65** |
| creature vere (statblock distinti) | **83** |
| schede di razze già in `dati/razze/` | 14 |
| razze e culture fuori dal roster | 4 |
| **creature da convertire** | **62** |

**13 voci hanno lo statblock su più colonne** — una voce, più creature:

| voce | pag. | creature |
|---|---:|---|
| **Avian** | 4 | 4 — Emre, Kingfisher, Skyfisher, 'Wari |
| **Dragon, Astral** | 20 | 2 — Astral Dragon (unmated), Astral Dragon (mated pair) |
| **Man (of Krynn)** | 59 | 4 — Ice Folk, Knights of Solamnia, Plainsmen, Rebels |
| **Shadowperson** | 71 | 2 — Shadowperson, Revered Ancient One |
| **Stag** | 78 | 3 — Wild Stag, Giant Stag, The White Stag |
| **Tayling** | 79 | 2 — Tayling, Taylang |
| **Beast, Undead** | 6 | 2 — Stahnk, Gholor |
| **Hatori** | 46 | 2 — Lesser Hatori, Greater Hatori |
| **Insect Swarm** | 50 | 2 — Velvet Ant Swarm, Grasshopper and Locust Swarm |
| **Lizard Man (of Krynn)** | 57 | 2 — Jarak-Sinn, Bakali |
| **Ogre (of Krynn)** | 65 | 2 — Ogre, Orughi |
| **Phaethon** | 69 | 2 — Phaethon, Elder Phaethon |
| **Spider (of Krynn)** | 77 | 2 — Whisper Spider, Giant Trap Door Spider |

**8 nomi di voce erano sbagliati** nel testo estratto, non i quattro noti.

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> **L'estrazione non ha solo sbagliato i nomi: ha perso dei dati.** In tre voci
> le colonne di destra sono sparite del tutto — `Avian` aveva quattro uccelli e ne
> restavano due, `Stag` tre cervi e ne restava uno, `Man (of Krynn)` quattro
> culture e ne restavano due. Sono sette creature che dal testo estratto non
> esistevano.
>
> Il conteggio passa da 65 a **83**: il 28% in più. Fra i ritrovamenti c'è il
> **Cervo Bianco**, che non è una bestia ma una creatura sacra unica da 2.000 punti
> esperienza, con capacità magiche.
>
> **L'ordine di lavorazione proposto va rivisto**: è stato formulato prima del
> ricontaggio e non contiene le sette creature nuove.

---

## Materiale esterno — chiuso (decisione 26)

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

## Questioni aperte

### Richiedono una decisione

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> - **Il PHB 5e 2014 non è fra i PDF**: la cartella contiene solo edizioni 2024.
>   Alternativa disponibile: `2014.5e.tools`, che espone il materiale 2014 come
>   JSON strutturato (repo GitHub `5etools-mirror-3/5etools-2014-src`).
> - **Shadow of the Dragon Queen** continua a mancare: resta l'unica fonte 5e
>   ufficiale su Krynn, e da essa dipende l'unico tratto ancora provvisorio.
> - **Il Barbaro ha doppia natura**: il manuale lo tratta sia come cultura umana
>   sia come classe. La decisione 20 gli ha dato un tappo reversibile; la
>   conversione a background va decisa insieme allo schema Personaggio.
> - **Il Qualinesti ha un tratto che registra un'assenza.** L'Appendice non
>   dichiara alcuna capacità per quel ramo, e il posto è tenuto da una voce
>   `source_only` senza meccanica. Nelle tabelle conta come un tratto
>   dell'Appendice pur non concedendo nulla: è un artefatto di rappresentazione,
>   non un beneficio. Da decidere se tenerlo come registrazione esplicita o
>   toglierlo e lasciare il conteggio a zero.

### Ambiguità delle fonti, registrate e non risolte

- **elfo-qualinesti** (razza): DECISIONE 22. L'Appendice Mostruosa non dichiara alcuna capacita' per il ramo Qualinesti, a differenza di Kagonesti (scatto in linea retta, pag. 35 stampata) e Silvanesti (veleno degli arcieri, pag. 34). La voce Qualinesti (pag. 33) descrive solo temperamento e armi preferite: "Qualinesti are more aggressive than Silvanesti but not as tactically sophisticated... Long swords, bows, and spears are among their preferred weapons." Tutte e tre le voci rimandano al PHB 2e per le capacita' elfiche ("have all of the special abilities of elves listed in the 2nd Edition Player's Handbook"). E' un esito, non una lacuna: i Qualinesti si distinguono dagli altri due rami per aggiustamenti e requisiti, non per capacita'. Nessuna differenza forzata.
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
