# Il bestiario di Krynn — diagnostica

*Generato da `dati/analizza_bestiario.py` il 2026-08-20.*

> **Diagnostica, non conversione.** Serve a vedere la forma del problema prima
> di cominciare, come `RAPPORTO-classi.md` per le classi. Nessuno statblock è
> stato scritto, `dati/` non è stato toccato.
>
> Fonti: MC Dragonlance Appendix (2e), Shadow of the Dragon Queen (5e,
> pagg. 196-199 stampate), SRD 5.1 per la calibrazione.

---

## Parte 1 — cosa contiene una scheda mostro 2e

Struttura completa di una voce dell'MC Appendix, campo per campo, con l'esempio
reale del **Baaz**.

| campo 2e | esempio | corrispettivo 5e | esito |
|---|---|---|---|
| `CLIMATE/TERRAIN` | Any, but usually tropical/Forest, plain, urban | `environment` (etichetta, nessun effetto meccanico) | da convertire |
| `FREQUENCY` | Uncommon | — | **assente in 5e** |
| `ORGANIZATION` | Band | — | **assente in 5e** |
| `ACTIVITY CYCLE` | Any | — | **assente in 5e** |
| `DIET` | Special | — | **assente in 5e** |
| `INTELLIGENCE` | Average (8-10) | punteggio di Intelligenza singolo | da convertire |
| `TREASURE` | M, Q; (D, I, T) | tabelle del tesoro della DMG, indicizzate per GS | da convertire |
| `ALIGNMENT` | Lawful or chaotic evil | `alignment`, con la formula "Typically" | diretto |
| `NO. APPEARING` | 2-20 | — | **assente in 5e** |
| `ARMOR CLASS` | 4 | **Armor Class**, ma la scala si inverte | da convertire |
| `MOVEMENT` | 6, Run 15, Glide 18 | **Speed** in piedi | da convertire |
| `HIT DICE` | 2 | **Hit Points** con formula di dadi | da convertire |
| `THAC0` | 19 | bonus di attacco per singolo attacco | da convertire |
| `NO. OF ATTACKS` | 2 or 1 | **Multiattack** nelle azioni | da convertire |
| `DAMAGE/ATTACK` | 1-4/1-4 or by weapon | danno per attacco, con media stampata | da convertire |
| `SPECIAL ATTACKS` | Poison | azioni e tratti | da convertire |
| `SPECIAL DEFENSES` | +2 bonus to saves | resistenze, immunita', tiri salvezza competenti | da convertire |
| `MAGIC RESISTANCE` | 20% | — | **assente in 5e** |
| `SIZE` | M (5' tall) | **Size**, categoria | diretto |
| `MORALE` | Elite (13) | — | **assente in 5e** |
| `XP VALUE` | 175 | **Challenge**, con PE derivati dal GS e non viceversa | da convertire |

**2 campi diretti, 12 da convertire, 7 senza alcun corrispettivo in 5e.**

I 7 senza corrispettivo: `FREQUENCY`, `ORGANIZATION`, `ACTIVITY CYCLE`, `DIET`, `NO. APPEARING`, `MAGIC RESISTANCE`, `MORALE`.

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> Un terzo abbondante della scheda 2e — 7 campi su 21 — non ha dove andare.
> Ma le due metà del problema non si somigliano.
>
> `FREQUENCY`, `NO. APPEARING`, `ORGANIZATION` e `ACTIVITY CYCLE` servivano al
> Dungeon Master per popolare il mondo: quante ne incontri, in che gruppi, di
> giorno o di notte. La 5e ha spostato quella funzione dalle schede alle tabelle
> d'incontro. **Non è informazione persa, è informazione trasferita**, e per un
> gioco da tavolo digitale è materiale utile al generatore di incontri anche se
> non entra nello statblock.
>
> `MAGIC RESISTANCE` e `MORALE` sono un'altra cosa: erano meccanica di
> risoluzione, e la 5e li ha eliminati per scelta di design. La resistenza magica
> percentuale è diventata vantaggio ai tiri salvezza; il morale è diventato una
> regola opzionale del DM. Qui una decisione va presa, perché nel 2e i draconici
> avevano tutti resistenza magica e toglierla li indebolisce.
>
> `XP VALUE` è il caso più insidioso: esiste in entrambe le edizioni ma vuol dire
> il contrario. In 2e i punti esperienza sono calcolati dalla scheda; in 5e sono
> derivati dal Grado di Sfida, che è la vera misura. Copiare il numero sarebbe
> sbagliato in modo silenzioso.

---

## Parte 2 — i cinque draconici, confronto puntuale

Le uniche creature con scheda in entrambe le edizioni. Sono anche le creature
identitarie di Krynn, quindi il campione non è casuale: è il migliore possibile.

### Baaz Draconian

| | AD&D 2e (MC Appendix) | D&D 5e (SotDQ pag. 197) |
|---|---|---|
| taglia | M (5' tall) | Medium |
| classe armatura | **4** (scala discendente) | **14** (natural armor, scala ascendente) |
| resistenza | 2 DV | 22 PF (4d8 + 4) |
| attacco | TAC0 19 | bonus di competenza +2 |
| attacchi | 2 or 1 — 1-4/1-4 or by weapon | Due attacchi con Spada corta. |
| movimento | 6, Run 15, Glide 18 | 30 ft. |
| difese speciali | Nil | — |
| resistenza magica | 20% | **non esiste in 5e** |
| morale | Elite (13) | **non esiste in 5e** |
| valore | 175 PE (formula 2e) | Grado di Sfida **1/2** (100 PE) |

**Effetto alla morte**: vedi "Cosa l'ufficiale ha reso, scartato e aggiunto" più sotto.

**Azioni 5e**: Multiattack (due attacchi); Shortsword +3 a colpire, 4 (1d6+1) perforanti.

**Altri tratti 5e**: Controlled Fall (riduce i danni da caduta); Draconic Devotion (vantaggio ai tiri per colpire vicino a un drago non ostile).

**Nota di fonte 2e**: dalle uova di draghi d'ottone (MC Dragonlance Appendix, voce Draconian, Baaz).

### Bozak Draconian

| | AD&D 2e (MC Appendix) | D&D 5e (SotDQ pag. 198) |
|---|---|---|
| taglia | M (6'+ tall) | Medium |
| classe armatura | **2** (scala discendente) | **15** (natural armor, scala ascendente) |
| resistenza | 4 DV | 40 PF (9d8) |
| attacco | TAC0 17 | bonus di competenza +2 |
| attacchi | 2 or 1 — 1-4/1-4 or by weapon | Due attacchi (Tridente, o due Scariche elettriche a distanza). |
| movimento | 6, Run 15, Glide 18, Fl 6 (E) | 30 ft. |
| difese speciali | +2 bonus to saves | — |
| resistenza magica | 20% | **non esiste in 5e** |
| morale | Elite (13) | **non esiste in 5e** |
| valore | 1.400 PE (formula 2e) | Grado di Sfida **2** (450 PE) |

**Effetto alla morte**: vedi "Cosa l'ufficiale ha reso, scartato e aggiunto" più sotto.

**Azioni 5e**: Multiattack (Tridente ×2 o Scariche elettriche ×2); Trident +4 a colpire, 5 (1d6+2) perforanti (6, 1d8+2 a due mani); Lightning Discharge +4 a distanza, 60 ft, 10 (3d6) fulmine; Spellcasting CD 12, quattro incantesimi 1/giorno ciascuno.

**Altri tratti 5e**: Glide (riduce i danni da caduta, sposta 2 ft orizzontali per ft di discesa).

**Nota di fonte 2e**: dalle uova di draghi di bronzo, incantatori (MC Dragonlance Appendix, voce Draconian, Bozak).

### Kapak Draconian

| | AD&D 2e (MC Appendix) | D&D 5e (SotDQ pag. 198) |
|---|---|---|
| taglia | M (6' tall) | Medium |
| classe armatura | **4** (scala discendente) | **15** (natural armor, scala ascendente) |
| resistenza | 3 DV | 39 PF (6d8 + 12) |
| attacco | TAC0 17 | bonus di competenza +2 |
| attacchi | 1 — 1-4 | Due attacchi con Pugnale (veleno e paralisi se entrambi colpiscono). |
| movimento | 6, Run 15, Glide 18 | 40 ft., climb 40 ft. |
| difese speciali | Nil | Abilita': Inganno +4, Percezione +3, Furtivita' +7. Immunita' ai danni da veleno e alla condizione avvelenato. |
| resistenza magica | 20% | **non esiste in 5e** |
| morale | Elite (13) | **non esiste in 5e** |
| valore | 650 PE (formula 2e) | Grado di Sfida **3** (700 PE) |

**Effetto alla morte**: vedi "Cosa l'ufficiale ha reso, scartato e aggiunto" più sotto.

**Azioni 5e**: Multiattack (Pugnale ×2, con TS su Costituzione CD 12 o veleno+paralisi se entrambi colpiscono); Dagger +5 a colpire, 5 (1d4+3) perforanti + 7 (2d6) veleno.

**Altri tratti 5e**: Glide (come il Bozak).

**Nota di fonte 2e**: dalle uova di draghi di rame, assassini con percentuali innate da ladro (MC Dragonlance Appendix, voce Draconian, Kapak).

### Sivak Draconian

| | AD&D 2e (MC Appendix) | D&D 5e (SotDQ pag. 199) |
|---|---|---|
| taglia | L (9' tall) | Large |
| classe armatura | **1** (scala discendente) | **16** (natural armor, scala ascendente) |
| resistenza | 6 DV | 57 PF (6d10 + 24) |
| attacco | TAC0 15 | bonus di competenza +2 |
| attacchi | 3 or 1 — 1-6/1-6/2-12 or by weapon | Due attacchi con Spada seghettata più uno di Coda. |
| movimento | 6, Run 15, Glide 18, Fl 24 (C) | 30 ft., fly 60 ft. |
| difese speciali | +2 bonus to saves | — |
| resistenza magica | 20% | **non esiste in 5e** |
| morale | Elite (14) | **non esiste in 5e** |
| valore | 2.000 PE (formula 2e) | Grado di Sfida **4** (1.100 PE) |

**Effetto alla morte**: vedi "Cosa l'ufficiale ha reso, scartato e aggiunto" più sotto.

**Azioni 5e**: Multiattack (Spada seghettata ×2 + Coda); Serrated Sword +6 a colpire, 13 (2d8+4) taglienti; Tail +6 a colpire, 8 (1d8+4) contundenti (TS Forza CD 14 o prono su bersagli Grandi o più piccoli); Shape Theft — reazione: illusione della forma dell'ucciso, dopo aver ucciso un Umanoide Medio o più piccolo.

**Nota di fonte 2e**: dalle uova di draghi d'argento, gli unici che volano davvero (MC Dragonlance Appendix, voce Draconian, Sivak).

### Aurak Draconian

| | AD&D 2e (MC Appendix) | D&D 5e (SotDQ pag. 196) |
|---|---|---|
| taglia | M (7' tall) | Medium |
| classe armatura | **0** (scala discendente) | **17** (natural armor, scala ascendente) |
| resistenza | 8 DV | 67 PF (9d8 + 27) |
| attacco | TAC0 13 | bonus di competenza +3 |
| attacchi | 2 or 1 — 3-10 (x2) or spell | Tre attacchi fra Squarcio e Raggio di energia. |
| movimento | 15 | 35 ft. |
| difese speciali | +4 bonus to saves | TS Int +6, Sag +3, Car +6. Percezione +3. Immune alla condizione affascinato. |
| resistenza magica | 30% | **non esiste in 5e** |
| morale | Champion (15) | **non esiste in 5e** |
| valore | 6.000 PE (formula 2e) | Grado di Sfida **6** (2.300 PE) |

**Effetto alla morte**: vedi "Cosa l'ufficiale ha reso, scartato e aggiunto" più sotto.

**Azioni 5e**: Multiattack (Squarcio + Raggio di energia, tre attacchi); Rend +5 a colpire, 8 (1d12+2) taglienti; Energy Ray +6 a distanza, 60 ft, 8 (1d10+3) forza; Noxious Breath (ricarica 5-6, cono 15 ft, TS Costituzione CD 14, 21/6d6 veleno + sfinimento); Spellcasting CD 14, incantesimi a volontà e a usi giornalieri.

**Altri tratti 5e**: Aura of Command: i draconici vicini resistono meglio a charme e paura (SotDQ pag. 196).

**Nota di fonte 2e**: dalle uova di draghi d'oro, gli unici senza ali (MC Dragonlance Appendix, voce Draconian, Aurak).


---

## Cosa l'ufficiale ha reso, scartato e aggiunto

### Baaz

| capacità 2e | esito | come |
|---|---|---|
| Trasformazione in pietra alla morte | **reso** | Diventa `Death Throes` con gas pietrificante e TS su Costituzione. La 5e aggiunge un effetto ad AREA che la 2e non aveva. |
| Arma conficcata nella statua (prova di Destrezza -3) | **scartato** | Era un effetto sull'equipaggiamento di chi uccideva. La 5e non ha regole per armi bloccate. |
| Due attacchi con artigli 1-4/1-4 | **trasformato** | Diventano due attacchi con SPADA CORTA. Le armi naturali sono sostituite da armi manufatte. |
| Resistenza magica 20% | **scartato** | La 5e non ha resistenza magica. |
| Travestimento sotto vesti e cappucci | **scartato** | Restava nel testo descrittivo, non era meccanica nemmeno in 2e. |
| Movimento 6 / Corsa 15 / Planata 18 | **trasformato** | Diventa velocita' 30 fissa piu' il tratto `Controlled Fall`. |
| — | **aggiunto** | `Draconic Devotion`: vantaggio ai tiri per colpire se vede un Drago non ostile. Non c'e' nulla di simile in 2e. |

### Bozak

| capacità 2e | esito | come |
|---|---|---|
| Esplosione delle ossa alla morte, 1d6 entro 10 piedi, nessun TS | **reso** | Diventa 2d8 danni da forza con TS su Destrezza CD 10. Danno quasi triplicato, ma con tiro salvezza. |
| Avvizzimento in un round, esplosione il round dopo | **scartato** | I due tempi diventano istantanei: la 5e non ha effetti alla morte differiti. |
| Incantesimi da mago (7 nomi) | **reso in parte** | Restano enlarge/reduce, invisibility, stinking cloud, web. Spariscono burning hands, magic missile, shocking grasp, sostituiti da `Lightning Discharge` come attacco a distanza. |
| Volo Fl 6 (E) | **scartato** | Il volo vero e' tolto: resta solo `Glide`. |
| +2 ai tiri salvezza | **trasformato** | Diventano competenze in TS di Intelligenza, Saggezza e Carisma. |
| Resistenza magica 20% | **scartato** | Come sopra. |

### Kapak

| capacità 2e | esito | come |
|---|---|---|
| Dissoluzione in pozza d'acido alla morte, 1d8/round, nessun TS | **reso** | Diventa acido addosso alle creature entro 5 piedi, 2d6 per turno per 1 minuto, con TS su Destrezza CD 12 e possibilita' di ripulirsi con un'azione. |
| L'acido distrugge tesoro e oggetti magici del Kapak | **scartato** | Era la penalita' che rendeva rischioso ucciderlo. Sparita. |
| Veleno come attacco speciale (saliva) | **reso** | Diventa 2d6 danni da veleno su ogni pugnale, piu' paralisi se entrambi gli attacchi colpiscono. |
| Abilita' da ladro a percentuale (15%/10%/20%) | **trasformato** | Diventano Furtivita' +7, Inganno +4, Percezione +3. |
| UN attacco per round, 1-4 danni | **trasformato** | Diventano DUE attacchi con pugnale. E' il cambiamento piu' grosso del roster. |
| — | **aggiunto** | Velocita' di scalata 40 piedi e immunita' ai danni da veleno: in 2e non c'erano. |

### Sivak

| capacità 2e | esito | come |
|---|---|---|
| Assume la forma dell'uccisore per TRE GIORNI, poi fuliggine | **reso in parte** | Diventa un'immagine spettrale urlante che dura UN MINUTO e spaventa. Da inganno a lungo termine diventa effetto di paura tattico. |
| Se l'uccisore non e' umanoide, prende fuoco: 2d4 danni | **scartato** | Il ramo alternativo dell'effetto sparisce; resta solo la condizione sulla taglia. |
| Mutaforma permanente uccidendo un umanoide | **reso** | Diventa `Shape Theft` come REAZIONE, illusione che dura finche' il draconico muore o la termina. |
| Tre attacchi 1-6/1-6/2-12 | **trasformato** | Diventano due spade seghettate piu' una coda che puo' far cadere proni. Il terzo attacco piu' forte diventa l'attacco di coda. |
| Volo Fl 24 (C) | **reso** | Diventa velocita' di volo 60 piedi. E' l'unico draconico che vola davvero in entrambe le edizioni. |
| Resistenza magica 20%, +2 ai TS | **trasformato** | Restano solo competenze in TS di Forza e Saggezza. |

### Aurak

| capacità 2e | esito | come |
|---|---|---|
| Sfera di fulmini per 3 round, poi esplosione 3d6 senza TS | **reso in parte** | Diventa istantaneo: sfera che rimbalza su tre bersagli, 2d8 con TS su Destrezza CD 14 e stordimento. Sparisce la fase di tre round in cui l'Aurak morto continuava ad attaccare come mostro da 13 DV. |
| Invisibilita' a volonta' | **reso** | Resta come incantesimo `invisibility` a volonta'. |
| Polymorph self e change self 3/giorno | **reso in parte** | Resta solo `disguise self` 2/giorno. |
| Dimension door 3/giorno | **reso** | Diventa 2/giorno. |
| Vede attraverso ogni illusione, individua invisibili entro 40 piedi | **trasformato** | Diventa `truesight` 60 piedi, che e' piu' forte e piu' semplice. |
| Soffio (SPECIAL ATTACKS: spells and breath, senza dettagli) | **reso** | Diventa `Noxious Breath`, cono di 15 piedi, 6d6 veleno piu' un livello di sfinimento. La 2e non ne dava i numeri: qui l'ufficiale ha INVENTATO, non convertito. |
| Resistenza magica 30%, +4 ai TS | **trasformato** | Diventano tre TS competenti e immunita' alla condizione affascinato. |
| — | **aggiunto** | `Aura of Command`: aura di comando sugli altri draconici. In 2e l'Aurak era un comandante nel testo, non nelle regole. |


> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> Tre regolarità nel modo di rendere, che valgono per tutti e cinque.
>
> **Le armi naturali diventano armi manufatte.** Baaz, Bozak, Kapak e Sivak in 2e
> attaccavano con artigli e morso; in 5e hanno spada corta, tridente, pugnale e
> spada seghettata. Solo l'Aurak conserva un attacco naturale (`Rend`). È una
> scelta di caratterizzazione — sono soldati, non bestie — e non una necessità
> tecnica.
>
> **L'effetto alla morte guadagna un tiro salvezza e perde il tempo.** In 2e
> quattro effetti su cinque colpivano senza tiro salvezza, e due si svolgevano in
> più round: il Bozak avvizziva un round e poi esplodeva, l'Aurak restava attivo
> come sfera di fulmini per tre round. In 5e tutto è istantaneo e tutto ha un
> tiro salvezza. La 5e non ha una grammatica per gli effetti differiti.
>
> **Ciò che colpiva l'equipaggiamento sparisce.** L'arma conficcata nella statua
> del Baaz, l'acido del Kapak che distruggeva tesoro e oggetti magici: entrambe
> tolte. Erano le regole che rendevano *costoso* uccidere un draconico, e la 5e
> non le sostituisce con niente.

---

## Parte 3 — esiste una regolarità?

| draconico | DV 2e | PF 5e | PF/DV | CA 2e | CA 5e | TAC0 | GS | GS−DV | PE 2e | PE 5e |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baaz | 2 | 22 | 11.0 | 4 | 14 | 19 | 1/2 | -1.5 | 175 | 100 |
| Bozak | 4 | 40 | 10.0 | 2 | 15 | 17 | 2 | -2.0 | 1.400 | 450 |
| Kapak | 3 | 39 | 13.0 | 4 | 15 | 17 | 3 | +0.0 | 650 | 700 |
| Sivak | 6 | 57 | 9.5 | 1 | 16 | 15 | 4 | -2.0 | 2.000 | 1.100 |
| Aurak | 8 | 67 | 8.4 | 0 | 17 | 13 | 6 | -2.0 | 6.000 | 2.300 |

### Punti ferita

Il rapporto PF/DV va da **8.4** a **13.0**, media 10.4.
Non è costante e non decresce in modo ordinato: il Kapak, che ha 3 DV, ne ha
13.0 per dado, più di tutti gli altri.

### Grado di sfida

**GS = DV − 2 per quattro draconici su cinque.** Bozak, Sivak e Aurak lo
rispettano esattamente; il Baaz sarebbe a GS 0, e 1/2 è il valore più vicino
possibile. **Il Kapak lo rompe**: 3 DV e GS 3, cioè GS = DV.

### L'inversione, che è il dato più interessante

L'ordine di potenza cambia fra le due edizioni:

| | dal più debole al più forte |
|---|---|
| **2e**, per punti esperienza | Baaz → Kapak → Bozak → Sivak → Aurak |
| **5e**, per grado di sfida | Baaz → Bozak → Kapak → Sivak → Aurak |

Il Bozak in 2e vale 1.400 PE contro i 650 del Kapak, quindi è più forte.
In 5e il Bozak è GS 2 e il Kapak GS 3: **si sono scambiati di posto**.

### Classe armatura

| | Baaz | Kapak | Bozak | Sivak | Aurak |
|---|---:|---:|---:|---:|---:|
| CA 2e (scende) | 4 | 4 | 2 | 1 | 0 |
| CA 5e (sale) | 14 | 15 | 15 | 16 | 17 |

L'**ordinamento è preservato** — chi era meglio protetto in 2e lo è anche in 5e —
ma non c'è una formula: Baaz e Kapak hanno la stessa CA 2e (4) e finiscono a 14 e 15.

### Economia delle azioni

| draconico | danno medio/round 2e | danno medio/round 5e | rapporto |
|---|---:|---:|---:|
| Baaz | 5.0 | 8.0 | ×1.6 |
| Bozak | 5.0 | 20.0 | ×4.0 |
| Kapak | 2.5 | 24.0 | ×9.6 |
| Sivak | 14.0 | 34.0 | ×2.4 |
| Aurak | 13.0 | 24.0 | ×1.8 |

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> **La risposta alla domanda è no: cinque casi non bastano.**
>
> Sul grado di sfida una regolarità si intravede — GS = DV − 2 tiene per quattro
> su cinque — ma il quinto non è un arrotondamento: il Kapak sta due gradi sopra
> dove la regola lo metterebbe. E non è un caso isolato, perché è **lo stesso
> draconico** che rompe anche il rapporto PF/DV (13.0 contro una media di 10.4) e
> che moltiplica il danno per 9.6 contro il ×1.6 del piu' conservativo.
>
> Il Kapak non è un'anomalia dei numeri: è una **riprogettazione**. In 2e era un
> assassino con un attacco debole e il veleno come minaccia; in 5e è diventato un
> duellante con due pugnali avvelenati che paralizza. L'ufficiale non ha
> convertito la creatura, l'ha ridisegnata attorno al suo ruolo narrativo.
>
> Se estraessi da qui la formula «GS = DV − 2, PF = DV × 10» e la applicassi alle
> cinquanta creature restanti, funzionerebbe finché le creature somigliano al loro
> ruolo 2e e sbaglierebbe di due gradi ogni volta che il ruolo va ripensato.
> Con cinquanta conversioni davanti, un'euristica che sbaglia su un caso su
> cinque non fa risparmiare tempo: lo sposta dalla conversione al debug.
>
> Quello che **si può** portare via da questi cinque casi non è una formula ma
> tre vincoli:
>
> 1. l'**ordinamento** di CA e di potenza si conserva, **ma solo finché si
>    conserva il ruolo**. Si può usare la fonte 2e per decidere chi è più forte
>    di chi, e poi assegnare i numeri guardando la 5e — finché la creatura resta
>    quello che era. Quando il ruolo viene ripensato, l'ordinamento non è più
>    garantito: è quello che è successo al Kapak, che in 2e era dietro al Bozak e
>    in 5e gli è passato davanti. Il controllo da fare prima di fidarsi
>    dell'ordinamento è quindi sul **ruolo**, non sui numeri;
> 2. l'effetto identitario va conservato ma **riscritto con un tiro salvezza**,
>    perché è così che la 5e esprime «succede qualcosa quando muore»;
> 3. i danni per round vanno **almeno raddoppiati** rispetto alla 2e — il minimo
>    osservato è ×1.6 — perché in 5e i personaggi hanno molti più punti ferita.
>
> Sono tre vincoli, non un algoritmo. Il metodo che i dati suggeriscono è quello
> della parte 4: conversione per analogia, non per calcolo.

---

## Parte 4 — calibrazione sull'SRD

Per ciascun draconico ufficiale, i mostri SRD 5.1 di pari grado di sfida e ruolo
comparabile. Il confronto con la mediana del grado dice se l'ufficiale ha
costruito creature nella norma o fuori.

| draconico | GS | ruolo | CA/PF del draconico | mediana SRD del GS | analoghi SRD per ruolo |
|---|---|---|---|---|---|
| Baaz | 1/2 | fante di prima linea, in gruppo | 14 / 22 | 12 / 22 | Lizardfolk, Gnoll, Hobgoblin, Orc |
| Bozak | 2 | incantatore di supporto in mischia | 15 / 40 | 13 / 45 | Cult Fanatic, Gargoyle, Berserker |
| Kapak | 3 | assassino furtivo con veleno | 15 / 39 | 14 / 58 | Doppelganger, Veteran, Werewolf |
| Sivak | 4 | bruto Grande volante, truppa d'assalto | 16 / 57 | 12 / 85 | Ettin, Chuul, Succubus/Incubus |
| Aurak | 6 | comandante incantatore | 17 / 67 | 15 / 114 | Mage, Medusa, Drider |

Il bestiario SRD usato è in `dati/_fonti/srd51_mostri.py`: 322 creature,
l'intero SRD 5.1 (era limitato a 110 creature su cinque gradi di sfida; completato
perché la Fase 2 calibrerà anche le altre 48 creature dell'Appendice, di gradi
ancora ignoti).

### Il profilo difensivo, che è il pezzo che spiega il Kapak

In 5e il **Grado di Sfida è la media fra componente difensiva e componente
offensiva**. Una creatura può stare a un grado alto con pochi punti ferita, se
il danno la tira su da sola.

| draconico | GS | PF | mediana SRD del grado | quota | danno/round | ×rispetto al 2e |
|---|---|---:|---:|---:|---:|---:|
| Baaz | 1/2 | 22 | 22 | 100% | 8 | ×1.6 |
| Bozak | 2 | 40 | 45 | 89% | 20 | ×4.0 |
| Kapak | 3 | 39 | 58 | 67% | 24 | ×9.6 |
| Sivak | 4 | 57 | 85 | 67% | 34 | ×2.4 |
| Aurak | 6 | 67 | 114 | 59% | 24 | ×1.8 |

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> **Il Kapak ha 39 punti ferita contro una mediana di 58 al suo grado: il 67%.**
> Sta *sotto* la mediana in difesa e ci arriva col danno — 24 per round. È un
> cannone di vetro, e in 2e non lo era: era un assassino con **un** attacco da 1-4.
>
> **Ecco perché `GS = DV − 2` fallisce proprio su di lui.** Quella regola
> presuppone che la creatura conservi il proprio profilo difensivo, perché i dadi
> vita della 2e misurano solo la resistenza. Il Kapak ha cambiato asse: i dadi
> vita dicono ancora "creatura da 3 DV", ma il grado di sfida risponde a un
> danno che in 2e non c'era.
>
> **Una precisazione che i numeri impongono, e che rafforza il punto invece di
> indebolirlo.** Il Kapak non è l'unico sotto la mediana difensiva: lo sono
> quattro draconici su cinque, e in modo crescente col grado — Bozak all'89%,
> Kapak e Sivak al 67%, Aurak al 59%. **I draconici sono una famiglia di
> creature fragili e offensive**, per scelta di design: colpiscono forte, muoiono
> in fretta, e alla morte esplodono addosso a chi li ha uccisi. È coerente.
>
> Quello che è **unico** del Kapak non è quindi la fragilità, ma il **salto
> offensivo rispetto alla propria fonte**: ×9.6 contro il ×1.6–×4.0 degli altri
> quattro. Gli altri sono stati riscalati; lui è stato **ripensato**.

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> **Sopra la mediana in armatura, sotto in punti ferita.** È lo stesso profilo
> visto sopra, letto sui due assi: la CA dei draconici sta sempre a pari o sopra
> la mediana del grado (14 contro 12 per il Baaz, 17 contro 15 per l'Aurak),
> i punti ferita sempre sotto tranne il Baaz. Sono creature difficili da colpire
> ma che cadono presto.
>
> Il Baaz è comunque **identico al Lizardfolk** — CA 15 e 22 PF contro CA 14 e 22 —
> e questo è il punto che conta: **la conversione per analogia è praticabile**. Per quasi ogni
> draconico esiste almeno un mostro SRD dello stesso grado e dello stesso ruolo
> con numeri molto vicini, e dove non c'è un analogo perfetto ce n'è uno
> ragionevole.
>
> L'eccezione è il **Kapak**: al GS 3 l'SRD non ha un assassino furtivo con
> veleno. Il Doppelganger ha il profilo di furtività ma non il veleno,
> l'Assassin vero è al GS 8. È un vuoto del catalogo, non un errore nostro, e
> significa che per quel ruolo bisognerà comporre invece che copiare.

---

## Il conteggio vero del bestiario

Il numero ricavato dal testo estratto era sbagliato, e la verifica sulle
immagini di pagina lo ha rifatto voce per voce.

| | |
|---|---:|
| voci dell'MC Appendix | **66** |
| creature vere (statblock distinti) | **87** |
| di cui schede di razze già in `dati/razze/` | 14 |
| di cui razze e culture fuori dal roster | 4 |
| **creature da convertire** | **66** |

**14 voci hanno lo statblock su più colonne**: una voce, più creature.

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

**8 nomi di voce erano sbagliati** nel testo estratto, non solo i quattro
verificati per primi. Il dettaglio completo — testo estratto, nome reale, pagina,
causa — è nella tabella più sotto.

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> **L'estrazione non ha solo sbagliato i nomi: ha perso dei dati.** In tre voci
> le colonne di destra sono sparite del tutto — `Avian` aveva quattro uccelli e
> ne restavano due, `Stag` tre cervi e ne restava uno, `Man (of Krynn)` quattro
> culture e ne restavano due. Sono **sette creature** che dal testo estratto non
> esistevano affatto.
>
> Il conteggio passa così da 66 voci a **87** creature vere. Non è un
> aggiustamento marginale: è il 32% in più, e cambia la stima di quanto lavoro
> c'è davanti.
>
> Due ritrovamenti che vale la pena segnalare. Il **Cervo Bianco**, una delle tre
> colonne di `Stag`, non è una bestia: è unico, di allineamento legale buono,
> vale 2.000 punti esperienza e ha capacità magiche — è una creatura sacra, e dal
> testo estratto non risultava. Il **Drago Astrale** ha due statblock ma è una
> specie sola in due stati, il solitario e la coppia accoppiata da 35 dadi vita
> che il manuale tratta come singola creatura.

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> **Questo numero non è un fatto acquisito: è la stima migliore ottenuta finora,
> e va detto invece di presentare 87 come definitivo.** Il conteggio "definitivo"
> è già stato smentito tre volte in quattro giri — 55 → 68 → 83 → 87 — e le voci a
> colonne multiple sono emerse in passate successive, non in una sola: non
> c'è garanzia che siano finite.
>
> **I segnali usati, in ordine di scoperta:**
>
> 1. *Duplicazione di un campo sulla stessa riga.* Le prime quattro voci
>    corrotte (`Yaggol`, `Tayling`, `Shadowperson`, `Man (of Krynn)`) sono state
>    trovate perché il testo estratto riportava DUE valori di `FREQUENCY` sulla
>    stessa riga (es. "Rare Uncommon"): un sintomo meccanico di colonne
>    affiancate lette come una riga sola.
> 2. *La stessa duplicazione estesa a più campi.* La seconda passata ha
>    allargato la ricerca a valori ripetuti su un numero qualunque di campi
>    della scheda 2e, non solo `FREQUENCY`: ha trovato `Beast, Undead`
>    (otto campi ripetuti) e altre voci che il primo segnale, più stretto, non
>    intercettava.
> 3. *Rilettura manuale, voce per voce, sulle immagini di pagina.* Non un
>    segnale automatico ma la verifica finale: ogni voce dell'elenco sopra è
>    stata riletta sull'immagine, non solo sul testo estratto.
> 4. *Controllo dei salti nella sequenza di pagina — di natura diversa dai
>    primi tre, e per questo ha trovato quello che loro non potevano.* I
>    segnali 1-3 cercano tutti un'anomalia LEGGIBILE dentro il testo estratto
>    di una voce: due valori sulla stessa riga, un'etichetta senza i due
>    punti, un valore duplicato. Presuppongono cioè che la voce si lasci
>    leggere almeno in parte. Il quarto segnale non cerca un difetto dentro le
>    voci: elenca le pagine di tutte le voci già note e cerca i punti dove il
>    numero salta più di un'unità — "dove mancano pagine fra due voci note",
>    non "cosa c'è di storto in questa voce". Per questo è l'UNICO controllo
>    che non dipende dal riuscire a leggere l'entrata mancante, ed è l'unico
>    che poteva trovare `Centaur (of Krynn)` (pagg. 7-8, nel salto fra `Beast,
>    Undead` a pag. 6 e `Disir` a pag. 9): la sua intestazione ha i NOMI DEI
>    CAMPI corrotti ("CUMATf.iTERRAIN" invece di "CLIMATE/TERRAIN",
>    "THACO;" invece di "THAC0:"), non solo i valori o il titolo — non
>    c'era nulla da confrontare, quindi invisibile ai segnali 1-3 per
>    costruzione, non per sfortuna. La maggior parte degli altri salti erano
>    continuazioni legittime di voci già catalogate (una voce lunga due
>    pagine); uno ha portato anche a verificare una voce di dragoni
>    (`Dragon, Othlorx`, pag. 22) che non necessitava aggiunta: descrive
>    varianti comportamentali di draghi standard già coperti ("physically
>    identical to the existing dragon forms"), non un nuovo statblock.
> 5. *Ricerca di "See below" su tutti i campi di tutte le voci — di natura
>    diversa dai primi quattro quanto il quarto lo era dai primi tre, ma nella
>    direzione opposta.* I segnali 1-4 cercano voci MANCANTI o mal titolate:
>    presuppongono che qualcosa nel testo estratto sia rotto o assente. Il
>    quinto non cerca niente che manchi — cerca, dentro voci già lette e già
>    classificate, i campi che la SCHEDA STESSA rimanda al testo perché "la
>    riga della tabella non basta a descriverli". In AD&D 2e "See below" è
>    dichiarazione dell'autore, non difetto di estrazione: la tabella ha uno
>    spazio fisso, e quando non basta il manuale rimanda alla prosa. Trovato
>    applicandolo prima ancora di leggere per intero le tre voci segnalate
>    dall'audit dei Punti Esperienza (Wichtlin, Eyewing, Imp Blood Sea, tutte
>    e tre con almeno un campo "See below"): il segnale vero dietro quell'audit
>    non erano i PE alti in sé, ma la presenza di questi campi rimandati — i PE
>    sono l'effetto (il manuale li conta nel totale), non la causa. A
>    differenza dei segnali 1-4, questo si applica PRIMA di leggere una voce
>    per intero, come segnale di priorità: fra le 48 voci
>    "creatura" dell'Appendice, **19 (40%)** hanno almeno un
>    campo "See below" in un dato di combattimento (non nei campi di mondo
>    `TREASURE`/`NO. APPEARING`, sempre esclusi dallo statblock per la
>    decisione 27 gruppo A — l'unica eccezione è `Haunt, Knight`, dove
>    `TREASURE` stesso resta "See below" senza un valore alternativo
>    dichiarato altrove, e va comunque letto). Distribuzione sulle fasce
>    attuali: 1 in prima, 6 in seconda, 8 in terza, 3 in quinta, 1 in fuori fascia. Tutte già lette per intero in questa sessione (elenco
>    completo più sotto): tre nella seconda fascia (Bear Ice, Centaur,
>    Eyewing) risolvono in un'immunità o un bonus singolo senza cambiare
>    fascia, una (Lizard Man) rivela tre dettagli di fuga/vulnerabilità nuovi
>    restando comunque di fascia bassa, due (Wichtlin, Imp Blood Sea) erano
>    proprio le voci arrivate dall'audit sui PE e si sono confermate
>    identitarie. La concentrazione nelle fasce basse-medie (seconda e terza,
>    **14 voci su 19, il 74%**) conferma
>    l'aspettativa che l'ha motivato: è lì che un campo rimandato al testo può
>    far più danno, perché è lì che ci si fida di più della prima impressione.
>
>    | voce | fascia | campi "See below" |
>    |---|---|---|
>    | Anemone, Giant | quinta | `TREASURE`, `NO. OF ATTACKS`, `DAMAGE/ATTACK`, `SPECIAL ATTACKS`, `SPECIAL DEFENSES` |
> | Bear, Ice | seconda | `SPECIAL DEFENSES` |
> | Beast, Undead | quinta | `SPECIAL DEFENSES` |
> | Centaur (of Krynn) | seconda | `SPECIAL DEFENSES` |
> | Dreamshadow | terza | `MAGIC RESISTANCE` |
> | Dreamwraith | terza | `MAGIC RESISTANCE` |
> | Eyewing | seconda | `SPECIAL DEFENSES` |
> | Fireshadow | quinta | `SPECIAL ATTACKS` |
> | Haunt, Knight | terza | `TREASURE` |
> | Imp, Blood Sea | terza | `MAGIC RESISTANCE` |
> | Insect Swarm | seconda | `NO. APPEARING`, `HIT DICE`, `THAC0`, `DAMAGE/ATTACK`, `SIZE`, `XP VALUE` |
> | Kalothagh (Prickleback) | terza | `SPECIAL DEFENSES` |
> | Knight, Death | terza | `SPECIAL ATTACKS`, `SPECIAL DEFENSES`, `MAGIC RESISTANCE` |
> | Lizard Man (of Krynn) | seconda | `SPECIAL DEFENSES` |
> | Shadowperson | seconda | `SPECIAL ATTACKS`, `SPECIAL DEFENSES` |
> | Spectral Minion | terza | `SPECIAL ATTACKS` |
> | Stag | fuori fascia | `SPECIAL DEFENSES` |
> | Warrior, Skeleton | prima | `SPECIAL ATTACKS`, `SPECIAL DEFENSES` |
> | Wichtlin | terza | `DAMAGE/ATTACK`, `SPECIAL ATTACKS`, `MAGIC RESISTANCE` |
>
>    Un limite dichiarato, scoperto subito dopo aver registrato questa
>    tabella: il quinto segnale non cattura tutto cio' che richiede lettura
>    completa. Lo Skrit (fascia 3, capacita' "jellification" mai quantificata
>    in nessun campo) e il Tylor (`SPECIAL DEFENSES: Special`, sei categorie
>    d'eta' con statistiche diverse) sono identitari quanto Wichtlin ma il
>    loro campo critico non dice "See below": dice un nome inventato
>    ("jellification") o la parola "Special" senza rimando esplicito. Il
>    difetto e' nella formulazione — cercare una stringa specifica trova solo
>    quella variante — non nell'idea, ed e' quello che il sesto segnale
>    corregge.
> 6. *Generalizzazione del quinto: non la stringa "See below", ma qualunque
>    valore che non e' un dato.* Per ogni campo della scheda 2e la forma
>    attesa e' nota — un numero, una formula di dadi, o un valore standard di
>    scala per quel campo (es. `INTELLIGENCE: Low (5-7)`) — quindi il
>    controllo e' meccanizzabile: segnalare ciò che non la rispetta. Applicato
>    ai campi di combattimento (non `TREASURE`/`NO. APPEARING`, salvo dove
>    restano privi di alternativa come `Haunt, Knight`) con un classificatore
>    a due livelli — sentinelle esplicite (`Special`, `Varies`/`Variable`,
>    `As creature or person mimicked`, oltre a `See below`) sui campi
>    numerici, e una lista di termini catalogati (nomi di stati/effetti
>    standard del gioco: veleno, paralisi, immunità, resistenza, ecc.) sulle
>    clausole di `SPECIAL ATTACKS`/`SPECIAL DEFENSES`, dove ogni clausola
>    senza una cifra propria e senza corrispondenza nella lista viene
>    segnalata. Il sesto segnale trova **7 voci nuove** che il
>    quinto non pescava (compreso lo Skrit, il caso che l'ha motivato) più
>    **3 campi aggiuntivi** su voci già
>    segnalate dal quinto per un altro campo:
>
>    | voce | fascia | campo | valore | tipo |
>    |---|---|---|---|---|
>    | Disir | terza | `SPECIAL ATTACKS` | Pain | nuova voce |
> | Fire Minion | terza | `SPECIAL ATTACKS` | Fire | nuova voce |
> | Kani Doll | seconda | `SPECIAL ATTACKS` | Continuous attacks | nuova voce |
> | Skrit | terza | `SPECIAL ATTACKS` | jellification (in "Surprise, jellification") | nuova voce |
> | Tylor | terza | `SPECIAL DEFENSES` | Special | nuova voce |
> | Yaggol | terza | `SPECIAL ATTACKS` | Mind blast | nuova voce |
> | Avian | seconda | `SPECIAL ATTACKS` | Dive/Drop (Skyfisher), Trample ('Wari) | nuova voce |
> | Haunt, Knight | terza | `SPECIAL ATTACKS` | Horror | campo nuovo su voce gia' segnalata dal quinto |
> | Kalothagh (Prickleback) | terza | `SPECIAL ATTACKS` | Shoots spines | campo nuovo su voce gia' segnalata dal quinto |
> | Lizard Man (of Krynn) | seconda | `SPECIAL ATTACKS` | Venom (jarak-sinn, risolto), Squirt blood (bakali, MAI risolto nel testo estratto) | campo nuovo su voce gia' segnalata dal quinto |
>
>    Il quinto segnale resta nell'elenco, non sostituito: la storia di come
>    un controllo si è affinato — da una stringa letterale a una lista di
>    sentinelle, da una lista di sentinelle a un criterio sulla forma del
>    valore — è più utile della sola versione finale, perché mostra il
>    pattern da applicare la prossima volta che un segnale si rivela troppo
>    stretto.
>
> **Segnali NON usati**, e quindi punti dove un ulteriore giro potrebbe ancora
> trovare qualcosa: nessun controllo automatico ha confrontato il numero di
> voci trovate con un indice o sommario del manuale (l'MC Appendix, formato
> Monstrous Compendium a fogli sciolti, non ne ha uno stampato); nessun
> controllo ha verificato che OGNI voce, non solo quelle già sospette, abbia un
> blocco statistiche internamente coerente (es. `NO. OF ATTACKS` e
> `DAMAGE/ATTACK` con lo stesso numero di elementi); e non è stata fatta una
> rilettura sistematica di TUTTE le pagine a immagine, solo di quelle già
> segnalate da un sintomo testuale, da un salto di pagina, o da un campo il
> cui valore non è un dato — quindi un difetto che non lascia nessuno di
> questi sintomi (un'intestazione corrotta ma su una pagina consecutiva,
> senza salto, con ogni campo dalla forma regolare) resta strutturalmente
> invisibile a tutti e sei i segnali usati finora.
>
> Il conteggio delle voci (48 creatura, 87 creature) non e'
> cambiato con il quinto o il sesto segnale: cercano dentro voci gia' contate,
> non ne aggiungono. Il rapporto deve comunque dirlo, non nasconderlo dietro un
> elenco di segnali che sembra chiuso.

---

## Parte 5 — da dove iniziare

Le **66 creature** da convertire, tolte le 14 schede di razze giocanti già
coperte da `dati/razze/` e le 4 razze fuori roster. **Proposta, non decisione.**

I **cinque draconici, il Traag, lo Scheletro Guerriero, il Thanoi, il Kyrie,
l'Ogre di Krynn, l'Orughi, l'Horax, l'Orso Glaciale, il Fetch, l'Ombrolo, il
suo Anziano Venerato e l'Occhialato (Eyewing) non sono in questa lista**: i
primi cinque hanno già un
precedente ufficiale completo (parti 2-4 sopra), gli ultimi dodici sono già
stati convertiti (`dati/mostri/traag.json`,
`dati/mostri/scheletro-guerriero.json`, `dati/mostri/thanoi.json`,
`dati/mostri/kyrie.json`, `dati/mostri/ogre-krynn.json`,
`dati/mostri/orughi.json`, `dati/mostri/horax.json`,
`dati/mostri/orso-glaciale.json`, `dati/mostri/fetch.json`,
`dati/mostri/shadowperson.json`,
`dati/mostri/anziano-venerato-ombrolo.json`,
`dati/mostri/eyewing.json` — la prima fascia dell'arena è
completa e la seconda è a buon punto, coi due casi con precedente 3.5 fatti
con calma). Restano **47 creature** su **37 voci** nelle
cinque fasce, più il Cervo Bianco fuori fascia.

### Seconda — riempitivi di fascia bassa e media (8 voci, 16 creature)

| creatura | perché | analogo SRD |
|---|---|---|
| Centaur (of Krynn) | Trovata il 20 agosto 2026 (compito 1, verifica Half-Ogre/Centaur): 4 DV, CA 5, nessuna resistenza fuori scala — profilo base pulito di fascia bassa-media, come Thanoi. Quattro sotto-specie nominate (Abanasinian, Crystalmir, Endscape, Wendle) con differenze di comportamento non ancora estratte per intero: la conversione base puo' partire dal profilo generico, le sotto-specie vanno lette a parte. CONFERMATA dal quinto segnale (20 agosto 2026): SPECIAL DEFENSES "See below" si risolve nel +2 ai tiri salvezza degli Abanasiniani ("extremely robust"), gia' anticipato come dettaglio di sotto-specie da estrarre in sede di conversione — nessuna sorpresa, segnale confermato ma causa gia' nota. | sì — Centaur SRD |
| Avian (Emre, Kingfisher, Skyfisher, 'Wari) | Quattro varianti sotto una sola voce: uccelli o umanoidi alati acquatici di Krynn. LETTURA COMPLETA (compito 3, 20 agosto 2026, trovata dal sesto segnale): Emre (3 DV) e Kingfisher (1 DV) restano riempitivi puliti senza attacchi speciali. Skyfisher (4 DV, XP 270, Intelligenza Alta 13-14) ha "Dive/Drop": in picchiata +2 a colpire e danno raddoppiato, poi afferra con gli artigli (prova di Destrezza o resta agganciato, trasportato 1d4 round e lasciato cadere, 1d6 danni/round in volo; molla la preda a 10 danni subiti o oltre 200 libbre). 'Wari (3 DV) ha "Trample": se spaventati stampedono, 3d4 danni/round a chi si trova nel percorso. Nessuna sorpresa: entrambe le meccaniche sono singole, quantificate, fascia bassa confermata su tutte e quattro le varianti. | sì per Emre/Kingfisher — probabile Hawk / Giant Owl; Skyfisher richiede un aggancio in volo, nessun analogo SRD diretto |
| Stag (Wild Stag, Giant Stag) | I due cervi normali della voce Stag: 3 e 5 DV, bestie da branco pulite. Il terzo abitante della voce, il Cervo Bianco, e' trattato a parte, fuori fascia — vedi sotto. | sì — Elk / Giant Elk |
| Lizard Man (Jarak-Sinn, Bakali) | Umanoidi rettili tribali, fascia bassa-media pulita: i jarak-sinn (piu' numerosi, 2+1 DV) e i bakali (2+1 DV), loro progenitori piu' rari. Voce nuova, trovata nella seconda passata. Il quinto segnale (20 agosto 2026) trova SPECIAL DEFENSES "See below" su ENTRAMBE le colonne, mai controllato prima (la coerenza precedente era solo sugli XP): per i jarak-sinn e' la coda distaccabile a volonta' (chi la afferra resta con la coda mentre il jarak-sinn fugge; ricresce in 1d4+8 settimane) — un meccanismo di fuga che il Lizardfolk SRD non replica; per i bakali e' una VULNERABILITA' al freddo (1 danno extra per dado da attacchi a base di freddo) piu' una membrana nittitante (+1 ai TS contro accecamento). Fascia confermata bassa-media (XP 270/175 restano modesti), ma la conversione dovra' rendere questi tre dettagli invece di limitarsi al Lizardfolk di peso. SESTO SEGNALE (compito 3, 20 agosto 2026): anche SPECIAL ATTACKS aveva un campo non catalogato su ENTRAMBE le colonne. Per i jarak-sinn si risolve ("Venom": la saliva acida gia' letta sopra, danno da veleno se l'arma e' intinta). Per i bakali NO: "Squirt blood" non e' mai spiegato nel testo estratto — ne' nel paragrafo Combat condiviso ne' altrove nella voce. PENDING, non inventato: da riverificare sull'immagine di pagina (57) prima della conversione, stesso trattamento del campo `raw` bloccato da filtro (vincolo 5). | sì — Lizardfolk |
| Phaethon | Umanoide alato dei monti, 4 DV, nessuna resistenza: GS basso-medio confermato, alternativa a Kyrie come avversario volante. Voce nuova. | parziale — nessun analogo diretto SRD |
| Insect Swarm, Grasshopper and Locust | Sciame di insetti, minaccia bassa per individuo, utile come ostacolo/ambientazione in arena. Voce nuova. LETTURA COMPLETA (compito 3): i sei campi "See below" (dimensione, DV, THAC0, danno, taglia, PE) sono tutti la STESSA formula di scala — dimensione dello sciame per 1d100, poi 1 pf ogni 20 insetti, THAC0/danno derivati dalla dimensione. Morso 90% di probabilita'/round, 1 danno fisso, visione ridotta a 2d4 piedi nella nube. Nessun veleno per questa variante (a differenza della Velvet Ant, sotto): fascia bassa confermata, meccanica di scala non di combattimento. | sì — Swarm of Insects |
| Gurik Cha-ahl | 2 DV, statistiche modeste: spostata dalla quarta fascia, e' un riempitivo bassissimo, non una curiosita'. | no |
| Kani Doll | 2 DV, CA 10 (nessuna protezione), costrutto che non controlla mai il morale: spostata dalla quarta fascia, filler bassissimo. SESTO SEGNALE (compito 3): "Continuous attacks" si risolve in 1d4 danni al morso poi 1 danno/round finche' non e' distrutta o ha compiuto il suo scopo — stesso idioma dell'Aggancio dell'Horax, gia' convertito in 5e. Fascia bassa confermata, nessuna sorpresa. | parziale — Homunculus |

### Terza — identitari ma senza analogo pulito (17 voci, 18 creature)

| creatura | perché | analogo SRD |
|---|---|---|
| Skrit | CORRETTA dopo lettura del testo completo (20 agosto 2026): la prima rilettura l'aveva confermata in seconda fascia guardando solo i DV (6) e la CA (3), lo stesso errore che il metodo aveva gia' imparato a evitare sullo Scheletro Guerriero. Il testo pieno rivela XP 2.000 (non da riempitivo) e un attacco velenoso in due fasi che nessun header riassume: paralisi con TS su veleno ogni round di aggancio (penalita' -1 cumulativa), poi dissoluzione dei tessuti (10 PF/ora) curabile SOLO con rigenerazione o guarigione naturale, non con magia curativa normale. Identitaria e costosa da rendere fedelmente, non un riempitivo pulito. | parziale — nessun mostro SRD replica la dissoluzione curabile solo per rigenerazione |
| Disir | SPOSTATA dalla seconda fascia dopo lettura completa (compito 3, sesto segnale, 20 agosto 2026: SPECIAL ATTACKS "Pain" non catalogato). Non e' un fante bestiale pulito: tutti e tre gli attacchi (2d4/2d4/2d6) sono avvelenati dal gel che secernono. TS su veleno con penalita' CUMULATIVA per attacco riuscito (-1/artiglio, -2/morso, fino a -4 se colpito da tutti e tre); se fallito, dolore che paralizza progressivamente in 1d4+1 round con -1 THAC0 cumulativo per round fino alla paralisi, durata 1d4 turni. SPECIAL DEFENSES ("Fire resistance") si risolve in +4 ai TS contro il fuoco e -1 danno/dado da fonti di fuoco, dallo stesso gel. Una catena di penalita' progressive fino alla paralisi non ha equivalente SRD pulito: identitaria, non riempitivo. | parziale — nessun mostro SRD replica la paralisi progressiva a penalita' cumulativa |
| Dreamshadow | STRUTTURALMENTE DIVERSA DALLE ALTRE: ogni campo della scheda 2e (CA, DV, THAC0, danno, taglia...) e' dichiarato "as creature or person mimicked" — non ha statistiche proprie, le eredita da chi imita. Non si converte come le altre 60: serve un mostro-modello (un pacchetto di regole che copia il bersaglio) piu' che uno statblock fisso. LETTURA COMPLETA (compito 3): MAGIC RESISTANCE "See below" si risolve in una scala legata al livello del sogno "mindspin" che lo genera — 0% al primo livello, 10% al secondo, 20% al terzo (stessa scala del Dreamwraith gemello, sotto). Conferma la categoria a parte, nessun cambio. | no — richiede un modello diverso, non un analogo |
| Dreamwraith | 8 DV, statistiche proprie fisse (a differenza del Dreamshadow gemello): fascia media confermata. LETTURA COMPLETA (compito 3): MAGIC RESISTANCE "See below" e' la stessa scala 0/10/20% per livello di sogno del Dreamshadow. Aggiunge tocco gelido 1d10, bonus di iniziativa +1, e un sotto-tipo opzionale con capacita' di "disperazione" (TS su incantesimi o il personaggio si unisce al dreamwraith recitando la stessa litania, negabile solo con dispel magic o un discorso di speranza, 30% di riuscita base). Condivide con il Dreamshadow un intero sotto-sistema di "disbelief" (tempo di concentrazione -> modificatore) che la 5e non ha: da RENDERE, non da copiare 1:1, quando si convertira'. | no |
| Fire Minion | 6 DV, immunita' al fuoco: fascia media confermata, l'analogo proposto resta debole rispetto ai DV reali. LETTURA COMPLETA (compito 3, sesto segnale: SPECIAL ATTACKS "Fire" non catalogato): l'etichetta nascondeva un'AURA passiva (1d6 danni automatici, nessun tiro per colpire ne' TS, a chiunque entro 5 piedi) oltre alla spada 2d6. Immunita' al fuoco totale (le fiamme magiche CURANO invece di ferire), vulnerabilita' all'acqua (+1 danno/dado), e un vincolo ambientale: puo' restare lontano dal fuoco solo 1d6+1d6 ore prima di iniziare a subire 12 danni/turno finche' non torna o muore. Identitaria per l'aura e il vincolo, non solo per l'immunita'. | parziale — Magmin, sottodimensionato |
| Tylor | STRUTTURALMENTE COMPLESSA: la fonte da' una tabella di 6 categorie d'eta' con DV, CA e soffio diversi per ciascuna (da 1d6 DV/CA4 a 5d10 DV/CA-1), sullo stesso modello degli age category dei draghi. Serve piu' di un GS, non uno: da trattare come una mini-famiglia di statblock imparentati, non una singola conversione. LETTURA COMPLETA (compito 3, sesto segnale: SPECIAL DEFENSES "Special" non catalogato, il caso gemello dello Skrit): eredita UNA sola resistenza elementare (fuoco O freddo, mai entrambe) dal genitore draconico — scelta del DM alla creazione, non delle statistiche fisse. Nessun soffio ("Breath Weapon: Nil" per tutte le otto categorie d'eta' nella tabella): un tylor combatte solo con morso/coda e incantesimi. | parziale — Chimera, solo per la categoria piu' alta |
| Knight, Death | **Il Cavaliere della Morte**. CORREZIONE dopo la rilettura: la fonte descrive un TIPO ripetibile ("a Knight of Solamnia, cursed by the gods..."), non un individuo nominato — coerente con la decisione 32 (criterio: nome proprio e storia, non vincolo a un oggetto). "E' Lord Soth" era un'identificazione della sessione precedente, non un dato della voce: la fonte non nomina Soth. Va convertito come CREATURA al suo grado reale (9 DV, 75% di resistenza magica — la seconda piu' alta del bestiario dopo il 90% dello Scheletro Guerriero, correzione al primato che il rapporto attribuiva erroneamente allo Yaggol), non trattato come scheda unica di Soth. SotDQ ha lo statblock di Soth come PERSONAGGIO specifico: resta un riferimento per un'istanza particolarmente potente dello stesso tipo, non la fonte di questa conversione. CORREZIONE ULTERIORE dopo lettura completa (compito 3, 20 agosto 2026): NON e' strutturalmente "quasi gemello dello Scheletro Guerriero" come la nota precedente diceva — quello ha un solo attacco con bonus fisso e nessun incantesimo. Il Cavaliere della Morte e' anche un incantatore a 20° livello: aura di paura costante (5 piedi), detect magic/detect invisibility/wall of ice a volonta', dispel magic 2/giorno, power word blind/kill/stun 1/giorno (a scelta), symbol of fear o symbol of pain 1/giorno, fireball da 20 dadi 1/giorno. La resistenza magica al 75% RIFLETTE l'incantesimo addosso al lanciatore con un tiro percentuale di 11 o meno (riverificato a ogni incantesimo subito). Il grado reale e' quindi ben oltre GS7: la nota di priorita' precedente lo sottostimava. | no — nessun mostro SRD combina guardiano corazzato e incantatore a questo livello nello stesso statblock |
| Haunt, Knight | 8 DV, CA "2 o migliore" (molto protetta), non scacciabile dai chierici Legali Buoni: fascia media-alta confermata, coerente con la collocazione precedente. LETTURA COMPLETA (compito 3, sesto segnale: SPECIAL ATTACKS "Horror" non catalogato): un vero e proprio controllo di paura (1d20 <= Saggezza+livello del PG o -4 a tutti i tiri per la durata dello scontro, ripetuto a ogni uccisione), immunita' a sonno/charme/hold/paralisi/controllo mentale/freddo, individuazione della magia entro 50 piedi (attacca il nemico piu' magico), e un vincolo di rigenerazione: se non gli si versa acqua santa addosso dopo averlo ucciso, si riforma intatto alla prossima luna piena di Solinari. Identitario quanto un boss ricorrente, non un guardiano generico. | no |
| Phaethon, Elder | Variante piu' forte del Phaethon base (6 DV contro 4), con un accenno di resistenza magica (5%): identitario, da comporre insieme al Phaethon. Voce nuova. | no |
| Insect Swarm, Velvet Ant | Sciame con veleno e formula di dimensione variabile: meccanica piu' complessa del semplice sciame. Voce nuova. LETTURA COMPLETA (compito 3): dimensione 1d100x1.000, morso 80%/round per 1d4 danni, poi TS su veleno o dolore intenso con -2 a tutti i tiri per colpire/danno per 2d4 turni. Ogni punto di danno inflitto allo sciame uccide 1d20 insetti; a meta' sciame morto i superstiti si disperdono; se sterminato per intero, 975 PE (non per singolo insetto). Fascia confermata: identitaria per il debuff, non per la potenza bruta. | parziale — Swarm of Insects, senza il veleno |
| Yaggol | Sotto-razza degenerata dei mind flayer, con kit complesso (sei attacchi piu' un potere psichico). CORREZIONE: 50% di resistenza magica NON e' la piu' alta del bestiario come diceva il rapporto — lo Scheletro Guerriero ne ha 90%, il Cavaliere della Morte 75%. Resta comunque identitario e costoso: nessun mostro SRD a GS 1/4-4 replica un mind-flayer minore. LETTURA COMPLETA (compito 3, sesto segnale: SPECIAL ATTACKS "Mind blast" non catalogato, numeri mai estratti prima): raggio 10 piedi, TS su bacchetta o 3d6 danni psichici, immune ai propri simili (compresi gli illithid veri), un'ora di ricarica, storna l'utilizzatore per il round successivo (nessuna azione). I sei attacchi sono pugni + quattro tentacoli prensili (mind-flayer-style: si aggrappano al cervello in 1d4 round, poi 1d6 danni automatici/round; liberarsi costa una prova di Forza e 1d10 danni per tentacolo agganciato). | no — Mind Flayer vero e' GS 7, fuori target |
| Tayling (+ Taylang) | Gemelli telepatici che nascono sempre in coppia: l'intelligente (Tayling, 4 DV) e il bestiale (Taylang, 8 DV — fascia media, non bassa: attenzione a non sottostimarlo convertendo la coppia). Nessun analogo SRD replica il legame telepatico. | no |
| Spectral Minion | SPOSTATA dalla seconda fascia: Dadi Vita "Varies", colpibile solo da armi +1 o migliori, 20% di resistenza magica, e SEI varianti nominate con valori di PE diversi (Philosopher/Reveler/Searcher a 975, Guardian/Warrior/Berserker a 1.400) sotto un'unica voce: piu' vicina a una famiglia di sotto-tipi che a un singolo riempitivo. LETTURA COMPLETA (compito 3, sesto segnale: SPECIAL ATTACKS "See below" gia' noto dal quinto, qui risolto per intero): la fonte dichiara esplicitamente che Dadi Vita, attacco e danno di UNO spectral minion sono QUELLI DELLA SUA VITA PRECEDENTE — e' un TEMPLATE applicato a un umano/demiumano morto, non uno statblock fisso, come predetto dal precedente metodologico 7 sul Dreamshadow ("probabilmente non l'ultimo" caso di regola di trasformazione). Le sei varianti sono comportamenti (guardiano legato a un pegno, filosofo che discute finche' non tocca terra e assale, ricercatore in cerca di un oggetto, guerriero in duello eterno contro l'altra fazione, festaiolo che drena livelli con la revelry, berserker impazzito), non gradi di potenza diversi. | sì per il profilo generale — Specter |
| Wyndlass | SPOSTATA dalla quarta fascia ("nicchia") dopo la rilettura: 12 DV, THAC0 9 (molto buono), UNDICI attacchi (dieci tentacoli piu' morso, danno 1-10 per tentacolo) e 5.000 PE — nello stesso ordine di grandezza del Cavaliere della Morte e dello Scheletro Guerriero, non una curiosita' acquatica di basso profilo. | parziale — Hydra per il numero di attacchi, ma senza rigenerazione |
| Wichtlin | SPOSTATA dalla seconda fascia dopo lettura completa (quinto segnale, 20 agosto 2026: DAMAGE/ATTACK, SPECIAL ATTACKS e MAGIC RESISTANCE tutti "See below"). Non e' un riempitivo: elfo non morto con due attacchi di contatto distinti (mano sinistra paralizza 2d4 round, mano destra avvelena per 2d6), immune a veleno/paralisi/sonno/charme/hold/incantesimi da freddo, colpibile solo da armi magiche +1, danneggiato dall'acqua santa (2d4/fiala), turnabile come spettro. Se era un incantatore in vita, lancia a meta' livello. Un elfo ucciso da un wichtlin diventa un wichtlin in sette giorni se non resuscitato: e' un effetto di CONTAGIO, non solo un mostro singolo. Include una variante montata ("Wichtlin Wild Stag") con meccanica di paralisi propria. Identitaria e costosa quanto lo Skrit, non un riempitivo di seconda fascia. | parziale — Specter per il profilo generale, nessuno replica il contagio ne' il doppio tocco paralisi/veleno |
| Imp, Blood Sea | SPOSTATA dalla quarta fascia ("nicchia") dopo lettura completa (quinto segnale, 20 agosto 2026: MAGIC RESISTANCE "See below", che non si risolve in una percentuale ma nell'elenco di immunita' sotto): 5+3 DV, polimorfismo a volonta' fra forma fisica (CA 4, tocco gelido 1d6) e forma di nebbia (CA 1, vola, ma solo 1 punto di danno da contatto e nessuna azione fisica), colpibile solo da armi magiche, immune a sonno/charme/incantesimi da freddo/paralisi/veleno, 10% di possibilita' di generare una copia di se stesso se colpito da un fulmine. La fascia "nicchia" descriveva l'ambientazione (il Mare di Sangue), non la meccanica: stesso equivoco gia' corretto su Bear Ice/Eyewing nella direzione opposta (erano niente-di-che sotto l'etichetta di nicchia), qui va nella direzione di un identitario vero sotto la stessa etichetta. | parziale — Imp/Quasit per il polimorfismo, ma nessuno replica la scissione da fulmine |
| Kalothagh (Prickleback) | SPOSTATA dalla quarta fascia ("nicchia") dopo lettura completa (compito 3, sesto segnale: SPECIAL ATTACKS "Shoots spines" non catalogato, oltre a SPECIAL DEFENSES gia' "See below" dal quinto). 4+4 DV ma QUATTRO meccaniche distinte, non una: volata di aculei a distanza (fino a 4/round, gittata 90 piedi, veleno debole con TS+4 o 2 danni extra e -2 CA per 2d6 ore), 20% di possibilita' che l'aculeo resti conficcato (1d4 danni extra a rimuoverlo), un pericolo passivo per chi combatte in mischia (prova di Destrezza/ round o impalato per 1-2 danni, 50%/round di liberarsi), e una difesa "fa il morto" (si gonfia e galleggia a pancia in su sotto il 75% dei PF). Troppo stratificata per la seconda fascia, l'ambiente acquatico descriveva la nicchia, non la semplicita'. | parziale — Manticore acquatico, nessun analogo replica tutti e quattro gli effetti insieme |

### Quarta — nicchia (3)

| creatura | perché | analogo SRD |
|---|---|---|
| Shimmerweed | 1 punto ferita, immobile, un solo attacco (confusione): a malapena una creatura da combattimento, piu' vicina a un ostacolo ambientale che a un avversario. Resta di nicchia per questo, non perche' sia debole in senso convenzionale. | parziale — Shrieker |
| Hatori, Lesser | Predatore del deserto a Dadi Vita variabili (1-5): complesso da fissare a un singolo GS, ma il taglio piu' basso rientra nel target. | no |
| Spider, Giant Trap Door | Ragno imboscatore di taglia Large, 4+4 DV: sopra la fascia bassa ma non enorme. Voce nuova, trovata nella seconda passata. | parziale — Giant Spider |

### Quinta — fuori target (draghi e alti Dadi Vita), non servono alla Fase 2 (9 voci, 10 creature)

| creatura | perché | analogo SRD |
|---|---|---|
| Dragon, Amphi | Drago: la Fase 2 non ne ha bisogno. | sì — draghi SRD |
| Dragon, Kodragon | Come sopra. | sì |
| Dragon, Sea | Come sopra. | sì |
| Dragon, Astral | Drago, come sopra. Due statblock nella voce (solitario e coppia accoppiata da 35 DV) ma una sola specie in due stati: contata come una riga, non due. | sì |
| Hatori, Greater | Variante adulta dell'Hatori, 6-20 DV: fuori target quanto un drago, serve oltre la Fase 2. Voce nuova. | no |
| Beast, Undead (Stahnk, Gholor) | 24 Dadi Vita ciascuno (12+12): fuori target quanto un drago. Voce nuova, trovata nella seconda passata — mancava del tutto dal ricontaggio precedente. | no |
| Spider, Whisper | 16 Dadi Vita (8+8): fuori target quanto un drago. Voce nuova. | no |
| Anemone, Giant | SPOSTATA dalla quarta fascia ("nicchia"): 16 Dadi Vita, THAC0 5 (fra i migliori del bestiario) e 12.000 PE — piu' del doppio dell'Aurak Draconian (6.000, GS 6), il piu' potente dei cinque ufficiali. "Bestia acquatica" descriveva l'ambiente, non la potenza: e' una delle creature piu' forti dell'intero bestiario. | no — fuori target quanto un drago |
| Fireshadow | SPOSTATA dalla terza fascia: 13+3 Dadi Vita (circa 16, la stessa soglia dei draghi e degli altri fuori-target), Gargantuan da 30 piedi, evocabile solo da un chierico malvagio di 8° livello o superiore, 11.000 PE — secondo valore piu' alto del bestiario dopo l'Anemone Gigante. Non e' un "identitario da comporre" a fascia media, e' fuori target quanto un drago. | no — fuori target |

### Fuori fascia — non da arena (1)

**The White Stag.** Il terzo abitante della voce Stag (pag. 78). Non è una bestia: è unico, allineamento legale buono, 2.000 PE, con capacità magiche — una creatura sacra da incontro narrativo, non un avversario. Proposta: schedarlo quando esiste uno schema per creature uniche/da avventura (vicino allo schema Personaggio), non forzarlo nel bestiario da combattimento. LETTURA COMPLETA (compito 3): SPECIAL DEFENSES "See below" si risolve in "non puo' essere catturato, combatte fino alla morte" — se ucciso il corpo scompare e chi lo ha ucciso resta maledetto (+1 alla propria Classe Armatura nella scala 2e discendente, cioe' PEGGIORE, per sette giorni). Ha anche find the path e speak with animals a volonta' e bless 3/giorno. Conferma: fuori fascia, creatura da incontro narrativo, non da arena.


> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> **Le fasce sono state ricostruite leggendo i 62 blocchi statistiche, non i
> nomi delle voci.** La versione precedente aveva scelto la prima fascia (compresi
> lo Scheletro Guerriero come "riempitivo generico" e l'Anemone Gigante come
> "nicchia") prima di leggere gli statblock per intero: ha funzionato per la
> maggioranza delle voci, ma ha sbagliato platealmente su alcune.
>
> **8 voci hanno cambiato fascia** dopo la rilettura, quasi sempre verso l'alto:
>
> - **Anemone Gigante**: quarta fascia ("nicchia") → **quinta** (fuori target).
>   16 Dadi Vita, THAC0 5, **12.000 PE — più del doppio dell'Aurak Draconian**
>   (6.000, il più forte dei cinque ufficiali). La sorpresa più grande del
>   ricontaggio: era classificata come bestia acquatica minore ed è una delle
>   creature più potenti dell'intero bestiario.
> - **Fireshadow**: terza fascia → **quinta**. 13+3 DV (≈16, la stessa soglia
>   degli altri fuori-target), Gargantuan, 11.000 PE — secondo valore più alto
>   del bestiario.
> - **Wyndlass**: quarta fascia ("nicchia") → **terza** (identitaria, costosa).
>   12 DV, THAC0 9, **undici attacchi**, 5.000 PE — stesso ordine di grandezza
>   del Cavaliere della Morte e dello Scheletro Guerriero, non una curiosità
>   acquatica.
> - **Fetch**: seconda fascia → **terza**. 9 DV, drena 2 livelli per colpo,
>   invisibile a chiunque tranne la vittima designata: molto più pericoloso di
>   quanto "non morto mutaforma di fascia media" suggerisse.
> - **Spectral Minion**: seconda fascia → **terza**. Colpibile solo da armi
>   magiche, sei varianti nominate con PE diversi sotto un'unica voce: una
>   famiglia di sotto-tipi, non un riempitivo semplice.
> - **Bear Ice, Disir, Eyewing, Gurik Cha-ahl, Kani Doll**: quarta fascia
>   ("nicchia") → **seconda**. Nella direzione opposta: erano trattate come
>   curiosità di nicchia e sono in realtà riempitivi puliti di fascia bassa,
>   senza nulla di anomalo nella scheda.
>
> **2 voci in più hanno cambiato fascia il 20 agosto 2026**, dopo l'audit sui
> Punti Esperienza e il quinto segnale (ricerca di "See below"; dettaglio
> sopra, "Il conteggio vero del bestiario"):
>
> - **Wichtlin**: seconda fascia → **terza** (identitaria, costosa). Doppio
>   tocco di contatto (paralisi + veleno), immunità multiple, contagio su
>   elfi uccisi in sette giorni, variante montata: molto più di un
>   riempitivo, nello stesso modo in cui lo era risultato lo Skrit.
> - **Imp, Blood Sea**: quarta fascia ("nicchia") → **terza** (identitaria,
>   costosa). Polimorfismo fisico/nebbia, immunità multiple, scissione da
>   fulmine: la fascia "nicchia" descriveva l'ambientazione (il Mare di
>   Sangue), non la meccanica — lo stesso equivoco di Bear Ice/Eyewing,
>   ma nella direzione opposta.
>
> L'**Eyewing**, letto per intero nello stesso giro, e' rimasto in seconda
> fascia (il campo rimandato al testo si risolveva in una sola immunita' al
> freddo) ed e' stato **convertito**: vedi `dati/mostri/eyewing.json`.

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> ### Compito 3 — le restanti voci con campo rimandato, lette tutte prima di convertire altro
>
> | voce | fascia prima | fascia dopo | cosa nascondeva il campo rimandato |
> |---|---|---|---|
> | Disir | seconda | terza (**cambiata**) | Veleno progressivo: TS con penalita' cumulativa per attacco, poi paralisi in 1d4+1 round — non un fante bestiale pulito |
> | Kalothagh (Prickleback) | quarta | terza (**cambiata**) | Quattro meccaniche stratificate: volata di aculei velenosi, impalamento passivo in mischia, "fa il morto" sotto il 75% dei PF |
> | Fire Minion | terza | terza (regge) | Aura passiva 1d6 senza tiro ne' TS, vincolo ambientale (danno se lontano dal fuoco troppo a lungo) |
> | Dreamshadow | terza | terza (regge) | Resistenza magica a scala 0/10/20% per livello del sogno mindspin — struttura gia' nota confermata |
> | Dreamwraith | terza | terza (regge) | Sotto-sistema di disbelief condiviso col Dreamshadow, variante "disperazione" con TS su incantesimi |
> | Haunt, Knight | terza | terza (regge) | Controllo di paura (-4 a tutti i tiri), immunita' multiple, si riforma senza acqua santa sull'armatura |
> | Knight, Death | terza | terza (regge) | Incantatore a 20° livello con riflessione magica al 75%: sottostimato come "quasi gemello dello Scheletro Guerriero", corretto |
> | Spectral Minion | terza | terza (regge) | Template sulle statistiche della vita precedente, non uno statblock fisso — secondo caso dopo il Dreamshadow |
> | Insect Swarm, Grasshopper e Locust | seconda | seconda (regge) | Formula di scala dimensione/PF/danno, nessun veleno |
> | Insect Swarm, Velvet Ant | terza | terza (regge) | Stessa formula di scala, piu' un debuff da veleno/dolore |
> | Tylor | terza | terza (regge) | Eredita una sola resistenza elementare (fuoco o freddo) dal genitore; nessun soffio in nessuna categoria d'eta' |
> | Yaggol | terza | terza (regge) | Numeri esatti del Mind Blast (10 piedi, TS o 3d6, un'ora di ricarica) mai estratti prima |
> | Avian, Skyfisher e 'Wari | seconda | seconda (regge) | Dive/Drop (aggancio in volo) e Trample (calpestio da fuga): entrambe quantificate, nessuna sorpresa |
> | Lizard Man, Bakali | seconda | seconda (regge) | Venom risolto (saliva acida gia' nota); Squirt blood MAI spiegato nel testo estratto — pending |
> | Kani Doll | seconda | seconda (regge) | Continuous attacks = stesso idioma dell'Aggancio dell'Horax, gia' convertito |
> | The White Stag | fuori fascia | fuori fascia (regge) | Maledizione su chi lo uccide (+1 CA nella scala 2e, cioe' peggiore) piu' tre incantesimi a volonta'/giornalieri — conferma fuori fascia |
>
> 2 fasce cambiate su 16 voci lette: **Disir**
> (seconda -> terza, veleno progressivo con paralisi) e **Kalothagh** (quarta ->
> terza, quattro meccaniche stratificate). Le altre 14
> confermano la fascia gia' assegnata: il campo rimandato aggiungeva dettaglio,
> non cambiava il giudizio. Un caso resta aperto — **Lizard Man**, "Squirt
> blood" dei bakali — perche' il testo estratto non lo spiega da nessuna
> parte: registrato `pending`, non inventato, da riverificare sull'immagine di
> pagina prima della conversione (vincolo 5, come i campi bloccati da
> filtro).

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> **2 voci hanno una correzione di lettura, non di fascia:**
>
> - **Yaggol**: il rapporto diceva che il suo 50% di resistenza magica fosse il
>   più alto del bestiario. **Non lo è**: lo Scheletro Guerriero ne ha 90%, il
>   Cavaliere della Morte 75%. Corretto ovunque compaia.
> - **Cavaliere della Morte**: la sessione precedente lo identificava con Lord
>   Soth. La voce dell'Appendice descrive però un **tipo** ("a Knight of
>   Solamnia, cursed by the gods..."), non un individuo nominato — la fonte non
>   cita mai Soth. Applicando il criterio della decisione 32 (nome proprio e
>   storia, non vincolo a un oggetto), il Cavaliere della Morte è una
>   **creatura**, non un'entità: si converte al suo grado reale come le altre,
>   e il suo statblock è strutturalmente quasi gemello dello Scheletro
>   Guerriero (9 DV, THAC0 11, un solo attacco con bonus fisso, resistenza
>   magica altissima). Lord Soth, se e quando serve come antagonista con nome
>   proprio, resta un'istanza particolare dello stesso tipo — non la fonte di
>   questa voce.
>
> **La categoria ENTITÀ, per ora, è vuota.** Fra le 62 voci lette non ce n'è
> una che abbia nome proprio e storia propria dichiarati dalla fonte stessa
> (il Cavaliere della Morte era l'unica candidata, ed è ricaduta in creatura).
> Non è un difetto della categoria: il criterio della decisione 32 ha retto al
> primo caso a cui è stato applicato, respingendolo. Resta nello schema e nel
> metodo per il giorno in cui una voce ci ricadrà davvero — un nome proprio
> dichiarato dalla fonte, non un'identificazione fatta da noi.
>
> **Il Tylor non è un problema aperto: è lavoro rimandato.** Sei categorie
> d'età con Dadi Vita, CA e soffio diversi, sullo stesso schema degli age
> category dei draghi — esattamente il caso per cui lo schema del mostro ha
> già `name.variante_di`. Si converte come una famiglia di statblock collegati
> da quel campo (una voce per categoria d'età, ciascuna con il proprio GS),
> non come un singolo mostro: non serve una decisione, serve solo farlo
> quando tocca al Tylor.
>
> **Il Dreamshadow è un problema diverso, non un'altra voce complicata.** Ogni
> campo della sua scheda — CA, DV, THAC0, danno, taglia, perfino l'allineamento
> — è dichiarato "as creature or person mimicked": la voce non ha statistiche
> proprie da nessuna parte. Non è una creatura a cui manca un analogo SRD, è
> una **regola di trasformazione** applicata a un'altra creatura o persona: il
> metodo per analogia non si applica perché non c'è nulla a cui applicarlo, il
> bersaglio cambia scheda ogni volta che il Dreamshadow ne imita una diversa.
> Registrato qui come categoria a parte, non forzato in uno statblock: è il
> primo caso del genere nel bestiario, e probabilmente non l'ultimo — conviene
> riconoscerli quando emergono invece di inventargli un GS di comodo.
>
> **I Dadi Vita non bastano a classificare una voce — vale anche per i Punti
> Esperienza, e non erano stati controllati sistematicamente.** Lo Scheletro
> Guerriero e lo Skrit sono stati classificati male nello stesso modo: fascia
> dedotta da DV/CA senza guardare gli XP dichiarati. In 2e gli XP sono il
> giudizio del manuale sulla pericolosità complessiva, non un derivato dei
> Dadi Vita. Ripassata la lista confrontando XP dichiarati e fascia assegnata:
> un controllo di minuti, non di ore.
>
> **Voci dove gli XP non tornano con la fascia — RISOLTE il 20 agosto 2026
> con la lettura completa** (vedi anche il quinto segnale, sopra, che ha
> trovato lo stesso terzetto cercando "See below" invece degli XP): il numero
> impone la lettura completa prima di convertire, non è un verdetto automatico
> (lo Skrit era anche lui "solo un numero" finché non si è letto il resto).
>
> - **Wichtlin**: LETTO PER INTERO, SPOSTATO in terza fascia (era seconda).
>   Non un riempitivo: doppio tocco paralisi/veleno, immunità multiple,
>   contagio su elfi uccisi, variante montata. Dettaglio nella voce di terza
>   fascia, sopra.
> - **Eyewing**: LETTO PER INTERO, CONVERTITO in seconda fascia (fascia
>   confermata). `SPECIAL DEFENSES: See below` si risolve nella sola
>   immunità al freddo: il segnale era acceso ma la causa era semplice, come
>   già per il Kyrie. Vedi `dati/mostri/eyewing.json`.
> - **Imp, Blood Sea**: LETTO PER INTERO, SPOSTATO in terza fascia (era
>   quarta). Polimorfismo fisico/nebbia, immunità multiple, scissione da
>   fulmine: la fascia "nicchia" descriveva l'ambientazione, non la
>   meccanica. Dettaglio nella voce di terza fascia, sopra.
> - **Kyrie** (già convertito, GS 1): XP 1.400 in 2e, lo stesso ordine di
>   grandezza del Wichtlin e del Bozak Draconian ufficiale (GS 2). La
>   conversione già fatta assegna GS 1 sul danno per round dichiarato (un
>   solo attacco, mai più di 1d8) e sull'assenza di resistenze: il numero
>   resta un segnale da tenere presente, non un errore accertato — a
>   differenza dello Skrit, qui il danno base *è* stato letto per intero e
>   *è* modesto. Segnalato, non ritoccato.
>
> Verificati sugli XP e poi CORRETTI da una lettura più a fondo (il quinto
> segnale, sopra, non l'audit sugli XP): **Lizard Man** (Jarak-Sinn 270,
> Bakali 175 — XP bassi, fascia confermata, ma `SPECIAL DEFENSES: See below`
> su entrambe le colonne nasconde la coda distaccabile del jarak-sinn e la
> vulnerabilità al freddo del bakali, mai controllate perché gli XP sembravano
> chiudere la questione) e **Centaur (of Krynn)** (stesso schema: fascia
> confermata, il campo risolve nel +2 ai tiri salvezza degli Abanasiniani, già
> previsto come dettaglio di sotto-specie da estrarre in conversione). Insect
> Swarm resta verificato coerente sulla fascia (XP "See below" per entrambe le
> varianti: non c'è un numero fisso da confrontare, la fascia distingue sulla
> base del veleno dichiarato) ma porta anch'esso più campi "See below" del
> previsto — vedi il quinto segnale.
>
> **Il criterio resta l'arena, non la completezza**, e non cambia: la Fase 2 ha
> bisogno di avversari fra GS 1/4 e GS 4, in quantità e con tattiche diverse. La
> quinta fascia contiene ora sette voci invece di cinque (Anemone Gigante e
> Fireshadow si aggiungono ai draghi), e non ne serve nessuna alla Fase 2. **La
> prima fascia è completa**: Traag (GS 1/4), Scheletro Guerriero (GS 7, al suo
> vero grado, non a quello presunto), Thanoi (GS 2) e Kyrie (GS 1) sono tutti
> convertiti. Il Thanoi ha avuto un riscontro in più: le statistiche 3.5 del
> lotto Dragonlance Campaign Setting (`riscontro/3.5/`, consultazione, non
> fonte) assegnano CR 2 in modo indipendente, confermando la stima fatta sulla
> sola scheda 2e più l'analogia SRD.
>
> Il **Cervo Bianco** resta fuori da tutte e cinque le fasce: non è un
> avversario, è una creatura sacra unica da incontro narrativo. Forzarlo in una
> fascia da combattimento travisirebbe cosa è.

---

## Gli 8 nomi corrotti — verificati

Riletti sulle immagini di pagina, con lo stesso metodo dei tratti razziali del
PHB 2e. I primi quattro erano stati verificati in un primo giro; il
ricontaggio voce per voce ne ha trovati altri quattro con la stessa causa.
**Tutti e 8 leggibili: nessuna voce resta sospesa.**

| testo estratto | nome reale | pag. PDF | causa |
|---|---|---:|---|
| `Emre Kingfisher` | **Avian** (+3 varianti) | 4 | QUATTRO colonne. L'estrazione ne aveva salvate due e chiamava la voce "Emre Kingfisher". Skyfisher e 'Wari erano persi del tutto. |
| `Unmated Mated pair*` | **Dragon, Astral** (+1 varianti) | 20 | DUE colonne, ma sono la stessa specie in due stati: il drago astrale solitario e la coppia accoppiata, che il manuale tratta come una singola creatura da 35 DV. Due statblock, una specie. Il nome dell'entrata era andato perso: l'estrazione la chiamava "Unmated Mated pair*". |
| `Ice Folk Knights of` | **Man (of Krynn)** (+3 varianti) | 59 | statblock a QUATTRO colonne |
| `Blood Sea Minotaur` | **Minotaur (of Krynn)** | 63 | UNA colonna sola, ma il nome era sbagliato: l'estrazione prendeva l'intestazione di colonna "Blood Sea Minotaur" come titolo. |
| `Shadowperson Revered Ancient One` | **Shadowperson** (+1 varianti) | 71 | statblock a due colonne |
| `Wild Stage` | **Stag** (+2 varianti) | 78 | TRE colonne. L'estrazione ne aveva una sola, con refuso: "Wild Stage". Il Cervo Bianco e' unico, di allineamento legale buono e da 2.000 PE: non e' una bestia ma una creatura sacra. |
| `Tayling Tayland` | **Tayling** (+1 varianti) | 79 | statblock a due colonne |
| `Y a g g o l` | **Yaggol** | 87 | titolo con spaziatura fra le lettere nel layout |

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> **La causa è quasi sempre una sola, e non è un difetto delle pagine.**
> 14 casi su 8 sono voci con statblock a **più colonne**: una sola
> voce del manuale contiene due o più creature affiancate, ciascuna con la
> propria colonna di valori. L'estrattore, che lavora a due colonne di testo,
> legge i titoli delle colonne di fianco come se fossero una riga sola. Gli
> altri -6 hanno un'altra causa: `Minotaur (of Krynn)` prendeva
> l'intestazione di una colonna interna (`Blood Sea Minotaur`) come titolo
> della voce; `Yaggol` aveva semplicemente le lettere spaziate nello stampato.
>
> **Questo cambia il conteggio del bestiario.** Dietro le 14 voci a più colonne
> ci sono **35 creature**, non 14: `Man (of Krynn)` ne contiene quattro,
> `Avian` altrettante, `Stag` tre, `Tayling`, `Shadowperson` e `Dragon, Astral`
> due ciascuna. Il numero vero — **66 voci, 87 creature** — è quello
> stabilito qui sopra in "Il conteggio vero del bestiario", voce per voce sulle
> immagini di pagina: non resta più nulla da chiarire su questo fronte.
>
> Due correzioni puntuali che l'immagine ha prodotto: il gemello bestiale del
> Tayling si chiama **Taylang**, non "Tayland" come leggeva il testo estratto; e
> `Man (of Krynn)` è una scheda di **PNG umani**, quindi va con le voci razziali
> già escluse dal conteggio dei mostri, non fra le creature da convertire.

---

## Cosa manca prima di poter convertire

Delle tre cose che mancavano, **sono fatte tutte e tre**.

- ~~Schema del mostro~~ → `dati/schema/mostro.schema.json`, validato sui cinque
  draconici.
- ~~Verifica degli 8 nomi corrotti~~ → tutti leggibili, vedi sopra.
- ~~Decisione sui sette campi senza corrispettivo~~ → decisione 27, sotto: due
  gruppi chiusi, uno rinviato con motivo.
- ~~Conteggio vero delle creature dell'MC Appendix~~ → **66 voci,
  87 creature**, stabilito voce per voce sulle immagini di pagina —
  vedi "Il conteggio vero del bestiario" sopra.

> **Lettura interpretativa** — registrata il 2026-08-20. Non e' derivata dai dati.
>
> Nessuna delle tre resta aperta. Quello che resta, e non è bloccante per
> cominciare a convertire, è un disallineamento scoperto per strada: il
> generatore di `RAPPORTO-mostri.md` (`confronta_mostri.py`) conta le voci
> dell'MC Appendix rileggendo il testo estratto con un'altra regola (i blocchi
> `CLIMATE/TERRAIN:`), indipendente da questo ricontaggio verificato sulle
> immagini. Dà **55**, non 66. Non è lo stesso tipo di errore dei nomi
> corrotti — è un secondo modo di contare, mai riconciliato col primo dopo il
> ricontaggio. Va allineato a questa fonte prima di fidarsi del suo numero, ma
> non impedisce di cominciare a convertire: la prima fascia non dipende da lui.

---

## Decisione 27 — i sette campi senza corrispettivo

Non erano un problema unico. Si dividono in tre gruppi, e due si sono chiusi
senza deliberare.

| gruppo | campi | esito | destinazione |
|---|---|---|---|
| **A** — dati di mondo | 5 | chiuso senza deliberare | `generatore_incontri`, Fase 3 |
| **B** — morale | 1 | chiuso senza deliberare | `ia_combattimento`, Fase 2 |
| **C** — resistenza magica | 1 | RINVIATA alla Fase 2 | da decidere in Fase 2 |

### Gruppo A — dati di mondo, non di scheda

La 5e non ha eliminato questi dati, li ha spostati: dalla scheda del mostro alle tabelle d'incontro. Sono informazione di mondo — quante ne incontri, in che gruppi, di giorno o di notte, cosa mangiano — e per un generatore di incontri automatico valgono esattamente quanto valevano per un Dungeon Master umano. Restano in source_2e come trascrizione fedele e vengono letti da li'.

Campi: `frequency`, `no_appearing`, `organization`, `activity_cycle`, `diet`.
Restano in `source_2e`, e nello schema sono raccolti anche in
`mechanics_5e.world_data_2e` con `destinazione: generatore_incontri`.
Nessuna conversione, nessuna decisione: la destinazione è registrata perché la
questione non venga riaperta.

### Gruppo B — il morale non è un campo, è un parametro

Il morale non e' un campo di scheda ma un parametro di comportamento. In 2e diceva al DM quando i mostri fuggono; nel nostro caso il DM e' il motore, e senza questo parametro ogni scontro finisce con tutti i nemici morti fino all'ultimo — irrealistico, e macchinoso da giocare. Il valore della fonte si conserva e diventa input dell'IA del mostro nell'arena.

Nello schema è `mechanics_5e.morale_2e`, con valore, etichetta della fonte e
`destinazione: ia_combattimento`. **Non entra nello statblock.**

### Gruppo C — resistenza magica, rinviata

E' l'unica vera decisione dei sette, e va presa con i numeri davanti.

**Perché la decisione 16 non si applica.** La decisione 16 dice che dove la 5e ha eliminato qualcosa deliberatamente si ripristina dalla fonte. Qui non si applica, per un'asimmetria: quei ripristini riguardavano TRATTI RAZZIALI DI PERSONAGGI GIOCANTI, in un sistema chiuso dove conta solo l'equilibrio interno. La resistenza magica riguarda invece OGNI draconico di OGNI scontro, e i Gradi di Sfida su cui stiamo calibrando presuppongono che non ci sia. Aggiungerla significa che ogni incontro pesa piu' di quanto il suo GS dichiari, sistematicamente.

**Il problema di traduzione.** Il 20% della 2e negava l'incantesimo DEL TUTTO, inclusi quelli senza tiro salvezza. Il tratto 5e piu' vicino, Magic Resistance, da' vantaggio ai tiri salvezza contro magia: piu' debole in un senso (non annulla nulla), molto piu' forte in un altro (vale su ogni incantesimo con TS, sempre). Non sono equivalenti. Non e' il caso del Kender, dove il +4 della fonte e il vantaggio 5e valevano davvero lo stesso.

Il valore percentuale resta in `source_2e` e in
`mechanics_5e.magic_resistance_2e` con `applied: false`.
**Quando si decide:** In arena, quando sapremo se i draconici senza resistenza magica risultano troppo fragili.

**Creatura di riferimento.** CORRETTO dopo la rilettura di tutte le 62 voci (vedi Parte 5): lo Yaggol NON ha la resistenza magica piu' alta del bestiario. La graduatoria vera e' Scheletro Guerriero 90% (MC Dragonlance Appendix, pag. 84), poi Cavaliere della Morte 75% (pag. 55), poi lo Yaggol 50% (pag. 87) — terzo, non primo. La nota precedente era scritta su un dato sbagliato, letto senza verificare le altre voci ad alta resistenza. E' lo Scheletro Guerriero la creatura su cui questa decisione pesera' di piu': a un grado di sfida molto piu' alto (GS 7 contro l'1/4-6 dei draconici), l'assenza del 90% conta molto di piu' che sui draconici o sullo stesso Yaggol.
