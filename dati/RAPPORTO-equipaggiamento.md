# L'equipaggiamento iniziale — due economie dichiarate insieme

Classi: **20**. Oggetti a catalogo: **79**.

| misura | valore |
|---|---:|
| classi che dichiarano `pacchetto_fisso_5e` | 20/20 |
| pacchetti effettivamente scritti | 0 |
| classi con una formula di ricchezza | 4/20 |
| classi con vincoli sull'equipaggiamento | 4/20 |
| classi con equipaggiamento imposto dalle competenze | 7/20 |

Il campo dichiara il pacchetto fisso per tutte e 20 le classi e ne contiene zero. Accanto, nello stesso blocco, 4 classi portano una formula di ricchezza, che e' il dato dell'altra economia:

| classe | ricchezza dichiarata dalla fonte |
|---|---|
| `barbaro` | 3d4x10 stl (1d4x10 per i barbari del ghiaccio) |
| `cavaliere` | 5d4x10 stl |
| `commoner` | 2d4x10 stl |
| `tinker` | 2d4x10 stl |

E 4 classi portano vincoli — quante regole, non quali: il testo sta nei dati privati.

| classe | vincoli |
|---|---:|
| `barbaro` | 2 |
| `cavaliere-corona` | 1 |
| `cavaliere` | 3 |
| `mariner` | 1 |


## Strada A — il pacchetto fisso

**Quanti pacchetti servono.** Uno per classe, cioe' 20, ma non 20 da inventare: 12 classi hanno un chassis SRD e 8 no.

| origine | classi | elenchi da scrivere |
|---|---:|---|
| l'SRD stampa gia' l'elenco del chassis | 12 | 5 elenchi, uno per telaio: `Cleric`, `Fighter`, `Paladin`, `Rogue`, `Wizard` |
| nessun chassis: l'elenco va composto | 8 | 8, uno per classe: `commoner`, `handler`, `mago-veste-bianca`, `mago-veste-nera`, `mago-veste-rossa`, `mariner`, `sacerdote-eretico`, `tinker` |

| telaio SRD | classi che ne ereditano l'elenco |
|---|---|
| `Cleric` | `sacerdote-ordini-sacri` |
| `Fighter` | `barbaro`, `cavaliere`, `cavaliere-corona`, `guerriero` |
| `Paladin` | `cavaliere-rosa`, `cavaliere-spada`, `paladino` |
| `Rogue` | `con-artist`, `ladro` |
| `Wizard` | `mago-alta-stregoneria`, `mago-rinnegato` |

**I pacchetti nominati** dai 5 elenchi sono **5** dei 7 che l'SRD stampa. Sono nell'SRD: non vanno inventati, vanno trascritti.

| pacchetto | costo (SRD) | voci | di cui fuori dal listino SRD |
|---|---:|---:|---:|
| Burglar's Pack | 16 | 14 | 1 |
| Dungeoneer's Pack | 12 | 9 | 0 |
| Explorer's Pack | 10 | 8 | 0 |
| Priest's Pack | 19 | 10 | 4 |
| Scholar's Pack | 40 | 7 | 2 |

**Cosa manca al catalogo** per scrivere quei 5 pacchetti e i 5 elenchi: le voci nominate sono **42**, e **13** non sono a catalogo.

| voce nominata dall'SRD e assente dal catalogo |
|---|
| Bedroll |
| Bell |
| Blanket |
| Book |
| Candle |
| Component Pouch |
| Hammer |
| Ink (1 ounce bottle) |
| Ink pen |
| Mess Kit |
| Parchment (one sheet) |
| Rations (1 day) |
| Spellbook |

A queste si aggiungono **7** voci che l'SRD nomina solo DENTRO la descrizione di un pacchetto e che la tabella dell'attrezzatura non elenca affatto — non hanno prezzo ne' peso propri, quindi non sono «mancanti dal catalogo»: sono da decidere, oggetti o testo del pacchetto.

- Alms box
- Block of incense
- Censer
- Little bag of sand
- Small knife
- String (10 feet)
- Vestments

E **5** voci non sono oggetti ma SCELTE aperte dentro una famiglia — non mancano dal catalogo, mancano dall'interfaccia: sono domande da porre al giocatore.

- arma da guerra
- arma da mischia semplice
- arma semplice
- focus arcano
- simbolo sacro

**Cosa questa strada NON risolve.** I vincoli della fonte (4 classi) mordono sul pacchetto e non sul tiro: il blocco lo dichiara gia'. Ma un vincolo come «non puo' portare armature piu' pesanti di X» e' una regola sul COMPRARE, e su un pacchetto fisso o e' gia' rispettato — e allora non serve — o va applicato riscrivendo il pacchetto per quella classe, che e' un pacchetto in piu' da comporre. Le 4 formule di ricchezza, su questa strada, non servono a niente e restano dato di fonte.


## Strada B — il borsello da spendere

**L'aritmetica c'e' gia' e non e' il problema.** decisione 42 (`cambio-acciaio-oro`) ha dato al progetto i due numeri e le due destinazioni: il fattore di listino vale 1 — 1 pezzo d'acciaio = 1 unita' di listino (i nostri cost_gp) — quindi un `cost_gp` del catalogo si legge come prezzo in acciaio senza conversione. Il cambio del mondo (40) non entra in un listino, ed e' gia' scritto che non ci entra.

**Dove sta il prezzo, e non e' dove il codice lo cerca.** `_valuta.prezzo_in_acciaio()` prende un `cost_gp`. Nel catalogo quel campo esiste per **50** oggetti su **79** — armi e armature, che hanno una sottosezione `weapon_5e` / `armor_5e`. Per **28** il prezzo c'e' ma dentro una STRINGA di `mechanics_5e.note` («Peso X lb, costo Y mo»), che e' prosa e non un campo; per **1** non c'e' affatto.

| dove sta il prezzo | oggetti | leggibile da `prezzo_in_acciaio()` |
|---|---:|---|
| campo `cost_gp` in `weapon_5e`/`armor_5e` | 50 | si' |
| stringa dentro `mechanics_5e.note` | 28 | no |
| nessun prezzo | 1 | no (`diadema-anima-legata`) |

`build_oggetti.py` lo dichiara in un commento — «l'attrezzatura non ha `weapon_5e`/`armor_5e`: costo e peso restano dentro `source_srd`/`mechanics_5e.note`, lo schema non ne prevede una sottosezione: la Fase 2 doveva coprire il combattimento, non l'inventario» — quindi non e' una svista nascosta. E' pero' il pezzo piu' grosso del conto di questa strada, e resta invisibile finche' qualcuno non prova a comprare una torcia: decisione 42 (`cambio-acciaio-oro`) ha dato l'aritmetica a un campo che per l'attrezzatura non esiste.

**Quante voci mancano al catalogo.** L'SRD stampa **128** voci fra attrezzatura, munizioni e strumenti; il catalogo ne ha adottate **28** e ne mancano **100**. Non e' una svista: `_fonti/srd51_equipaggiamento.py` dichiara di aver preso «cio' che serve al combattimento e all'esplorazione, non ogni voce della tabella». Su questa strada quel confine non regge piu', perche' un personaggio che compra puo' comprare qualunque riga del listino.

| categoria SRD | voci | a catalogo | mancanti |
|---|---:|---:|---:|
| adventuring-gear | 89 | 23 | 66 |
| ammunition | 4 | 4 | 0 |
| tools | 35 | 1 | 34 |

(Armi e armature non compaiono qui: il catalogo le ha tutte, 37 armi e 13 fra armature e scudo.)

**Da dove viene la ricchezza per le altre classi.** La formula esiste per **4** classi su 20; per le altre **16** la fonte 2e non ne stampa una. E l'SRD 5.1 non offre un ripiego: la tabella «Starting Wealth by Class» del PHB 2014 non e' fra le sezioni dell'SRD (cercata su tutte e 45 il 05/09/2026). Le classi senza formula sono:

- `cavaliere-corona` — telaio `Fighter`
- `cavaliere-rosa` — telaio `Paladin`
- `cavaliere-spada` — telaio `Paladin`
- `con-artist` — telaio `Rogue`
- `guerriero` — telaio `Fighter`
- `handler` — nessun chassis
- `ladro` — telaio `Rogue`
- `mago-alta-stregoneria` — telaio `Wizard`
- `mago-rinnegato` — telaio `Wizard`
- `mago-veste-bianca` — nessun chassis
- `mago-veste-nera` — nessun chassis
- `mago-veste-rossa` — nessun chassis
- `mariner` — nessun chassis
- `paladino` — telaio `Paladin`
- `sacerdote-eretico` — nessun chassis
- `sacerdote-ordini-sacri` — telaio `Cleric`

Tre modi di chiudere questo buco, e nessuno e' gratis: derivarla dal chassis (ma 8 classi non ne hanno uno), trascriverla dal PHB 2014 (decisione 2 (`edizione-phb-2014`) lo ammette come edizione di riferimento, e il dato sarebbero venti formule di dado), o deciderne una nostra, che e' strato editoriale e va dichiarato tale (decisione 7 (`doppio-strato`)).


## Le due strade, una accanto all'altra

| | pacchetto fisso | borsello |
|---|---|---|
| cosa c'e' gia' | il campo lo dichiara in 20/20 classi | l'aritmetica del listino (decisione 42 (`cambio-acciaio-oro`)) |
| cosa manca di dato | i pacchetti (zero scritti) e le voci di catalogo che li compongono | le voci di catalogo e la ricchezza per 16 classi su 20 |
| cosa manca di decisione | come si compone il pacchetto delle classi senza chassis | da dove viene la ricchezza dove la fonte tace |
| cosa fa con i vincoli della fonte | li rispetta per costruzione, ma ogni vincolo e' un pacchetto in piu' | li applica come filtro sull'acquisto, una volta sola |
| cosa fa con le 4 formule di ricchezza | le ignora: restano dato di fonte non usato | le usa, ed e' l'unico posto del progetto dove servono |
| serve un prezzo leggibile? | no: il pacchetto e' un elenco, non una spesa | si', e oggi lo e' per 50 oggetti su 79 |

Le voci di catalogo mancanti sono in buona parte le STESSE per le due strade: e' la parte del lavoro che nessuna delle due evita. Cio' che le distingue davvero e' un campo — il prezzo — e una decisione: da dove viene la ricchezza dove la fonte tace.
