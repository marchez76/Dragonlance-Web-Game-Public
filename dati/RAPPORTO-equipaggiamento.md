# L'equipaggiamento iniziale — la strada presa, e cosa resta

decisione 62 (`pacchetto-fisso`) sceglie il **pacchetto fisso** contro il borsello da spendere. Questo rapporto misura cosa quella scelta ha chiuso e cosa resta aperto; il conto della strada non presa e' in fondo, perche' e' la misura che ha deciso.

| misura | prima | ora |
|---|---:|---:|
| pacchetti scritti | 0 | 5 |
| classi con un elenco di equipaggiamento | 0 | 12/20 |
| oggetti a catalogo | 79 | 92 |
| oggetti con un prezzo leggibile da un campo | 50 | 91 |
| voci di equipaggiamento che rimandano al catalogo | 0 | 125 |

Le 125 voci sono di tre generi, e la distinzione dice CHI le risolve: **75** rimandano a `dati/oggetti/`, **26** a `dati/pacchetti/`, e **24** non si risolvono affatto — sono filtri che l'interfaccia deve porre come domanda (decisione 35 (`repertori-sono-filtri`)).


## Cosa la decisione ha chiuso

**I 5 pacchetti sono trascritti, non composti.** L'SRD ne stampa 7; qui stanno quelli che i 5 elenchi di telaio nominano davvero. Gli altri due non sono stati saltati per fretta: nominano voci che il catalogo non ha, e scriverli darebbe riferimenti che non risolvono.

| pacchetto | costo SRD | voci | di cui da decidere |
|---|---:|---:|---:|
| Pacchetto dello scassinatore (`burglars-pack`) | 16 | 14 | 1 |
| Pacchetto dell'esploratore di sotterranei (`dungeoneers-pack`) | 12 | 9 |  |
| Pacchetto dell'esploratore (`explorers-pack`) | 10 | 8 |  |
| Pacchetto del sacerdote (`priests-pack`) | 19 | 10 | 4 |
| Pacchetto dello studioso (`scholars-pack`) | 40 | 7 | 2 |

**12 classi hanno l'elenco del proprio telaio.** Non 12 elenchi: 5, uno per telaio, e le classi che condividono un telaio ne condividono l'elenco — decisione 23 (`principio-del-clone`) letta sull'inventario.

| telaio SRD | classi | voci nell'elenco |
|---|---|---:|
| `Cleric` | `sacerdote-ordini-sacri` | 12 |
| `Fighter` | `barbaro`, `cavaliere`, `cavaliere-corona`, `guerriero` | 12 |
| `Paladin` | `cavaliere-rosa`, `cavaliere-spada`, `paladino` | 9 |
| `Rogue` | `con-artist`, `ladro` | 12 |
| `Wizard` | `mago-alta-stregoneria`, `mago-rinnegato` | 7 |

**Il prezzo dell'attrezzatura e' un campo.** Era dentro una frase italiana di `mechanics_5e.note` — «Peso N lb, costo N mo» — su 28 oggetti: due campi letti dalla fonte, cuciti in una stringa, e i campi buttati. Ora c'e' `attrezzatura_5e`, che sta accanto a `weapon_5e` e `armor_5e` senza duplicarli: le tre sezioni si escludono, e `_valuta.prezzo_di()` e' l'unico posto che sa quali sono. L'aritmetica di decisione 42 (`cambio-acciaio-oro`) ha finalmente un campo a cui applicarsi.


## Cosa resta aperto, e perche' non e' stato chiuso di slancio

**1. Le 8 classi senza chassis non hanno un elenco.** Nessun telaio 5e le copre, quindi non c'e' niente da trascrivere: comporre un pacchetto per loro e' una scelta editoriale, e decisione 62 (`pacchetto-fisso`) la vuole proposta prima che scritta. Il campo lo dichiara — `da_comporre: true` — invece di portare un elenco plausibile che nessuno ha approvato.

Cio' su cui una proposta potra' poggiare, e che e' gia' nei dati: le armi che la fonte IMPONE alla classe (`forced_equipment`, l'unica cosa che la fonte 2e dica sull'inventario di queste otto), il dado vita, e le regole di equipaggiamento che portano.

| classe | armi imposte dalla fonte | dado vita | ricchezza 2e | vincoli |
|---|---|---:|---|---:|
| `commoner` | — | d6 | si' |  |
| `handler` | — | d6 | — |  |
| `mago-veste-bianca` | — | 1d4 | — |  |
| `mago-veste-nera` | — | 1d4 | — |  |
| `mago-veste-rossa` | — | 1d4 | — |  |
| `mariner` | Cutlass, Belaying Pin, Gaff Hook | d10 | — | 1 |
| `sacerdote-eretico` | — | 1d8 | — |  |
| `tinker` | — | d6 | si' |  |

**2. Le 7 voci che esistono solo dentro un pacchetto.** L'SRD le nomina nella descrizione e la tabella dell'attrezzatura non le elenca: non hanno ne' prezzo ne' peso, quindi non sono voci MANCANTI dal catalogo. Diventano oggetti o restano testo del pacchetto, ed e' una domanda sul merito di ciascuna.

| voce | pacchetto |
|---|---|
| Alms box | `priests-pack` |
| Block of incense | `priests-pack` |
| Censer | `priests-pack` |
| Little bag of sand | `scholars-pack` |
| Small knife | `scholars-pack` |
| String (10 feet) | `burglars-pack` |
| Vestments | `priests-pack` |

**3. Due dei 5 filtri non hanno campione.** Le cinque scelte aperte sono registrate come filtri (decisione 35 (`repertori-sono-filtri`)) e tre di esse il catalogo sa gia' risolverle, perche' sono categorie d'arma. Le altre due — **focus arcano**, **simbolo sacro** — delimitano una famiglia di cui il catalogo non ha ancora nessun membro.

| scelta | filtro | nota |
|---|---|---|
| arma da guerra | `categoria=da_guerra` | qualunque arma da guerra, mischia o distanza |
| arma da mischia semplice | `categoria=semplice`, `tipo=mischia` | solo mischia, e la distinzione conta: l'alternativa nella stessa riga sono cinque giavellotti |
| arma semplice | `categoria=semplice` | qualunque arma semplice, mischia o distanza |
| focus arcano | — | l'SRD elenca sfera, cristallo, bacchetta, verga e bastone come focus arcani, e il catalogo non ne ha adottato nessuno: e' un FILTRO SENZA CAMPIONE. Le voci stanno nell'indice SRD (Orb, Crystal, Wooden staff) e adottarle e' una scelta, non un atto dovuto — con il pacchetto fisso l'alternativa nella stessa riga, il Component Pouch, e' a catalogo, quindi la creazione non si blocca |
| simbolo sacro | — | stesso caso del focus arcano: amuleto, emblema e reliquiario stanno nell'indice SRD e non nel catalogo. Qui pero' NON c'e' un'alternativa nella stessa riga — Cleric e Paladin lo ricevono insieme allo scudo o alla cotta di maglia, senza scelta — quindi e' l'unica delle cinque che lascia un buco vero dentro un pacchetto |

Delle due, il **simbolo sacro** e' l'unica che lascia un buco vero: il focus arcano ha un'alternativa a catalogo nella stessa riga (la borsa dei componenti), il simbolo sacro no — Chierico e Paladino lo ricevono senza scelta.

**4. Come mordono i vincoli della fonte.** 4 classi ne portano; su un pacchetto fisso un vincolo o e' gia' rispettato — e allora non serve — o chiede un pacchetto riscritto per quella classe. Quale dei due, non e' deciso: il campo dichiara `applied: false` e rimanda alla sede in `source_2e`, invece di ricopiare qui la prosa della fonte.

| classe | vincoli |
|---|---:|
| `barbaro` | 2 |
| `cavaliere-corona` | 1 |
| `cavaliere` | 3 |
| `mariner` | 1 |


## La strada non presa, e quanto sarebbe costata

Il borsello da spendere: il personaggio riceve una somma e compra. decisione 62 (`pacchetto-fisso`) l'ha scartata per tre ragioni, e sono tutte e tre numeri.

**Il dato dichiarava gia' l'altra strada.** 20/20 classi portano `system: "pacchetto_fisso_5e"`; la formula di ricchezza esiste per **4** su 20 (`barbaro`, `cavaliere`, `commoner`, `tinker`), e per le altre **16** la fonte 2e tace. L'SRD non offre ripiego: «Starting Wealth by Class» non e' fra le sue 45 sezioni (cercata il 05/09/2026).

**Il perimetro del catalogo.** Col pacchetto sono servite **13** voci nuove, contate e non stimate. Col borsello ne sarebbero servite **87**: chi compra puo' comprare qualunque riga, quindi il confine dichiarato da `_fonti/srd51_equipaggiamento.py` — «cio' che serve al combattimento e all'esplorazione, non ogni voce della tabella» — non avrebbe retto piu'.

| categoria SRD | voci | a catalogo | mancanti |
|---|---:|---:|---:|
| adventuring-gear | 89 | 36 | 53 |
| ammunition | 4 | 4 | 0 |
| tools | 35 | 1 | 34 |

(Armi e armature non compaiono qui: il catalogo le ha tutte, 37 armi e 13 fra armature e scudo.)

**Il verbo.** Il pacchetto si TRASCRIVE — 7 pacchetti e 5 elenchi stanno nell'SRD — mentre il borsello va COMPOSTO: dove la fonte tace, la ricchezza va decisa, e sarebbero state 16 decisioni editoriali da dichiarare tali (decisione 7 (`doppio-strato`)).

**Cio' che il borsello aveva dalla sua** era l'aritmetica: decisione 42 (`cambio-acciaio-oro`) fissa il fattore di listino a 1 — 1 pezzo d'acciaio = 1 unita' di listino (i nostri cost_gp) — quindi un `cost_gp` si legge come prezzo in acciaio senza conversione. Quel campo mancava all'attrezzatura, ed e' stato scritto lo stesso: e' il pezzo di quella strada che serviva anche a questa, e l'unico.
