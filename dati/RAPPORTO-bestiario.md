# Il bestiario di Krynn — diagnostica

*Generato da `dati/analizza_bestiario.py` il 2026-08-19.*

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

> **Lettura interpretativa** — registrata il 2026-08-19. Non e' derivata dai dati.
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


> **Lettura interpretativa** — registrata il 2026-08-19. Non e' derivata dai dati.
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

> **Lettura interpretativa** — registrata il 2026-08-19. Non e' derivata dai dati.
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

> **Lettura interpretativa** — registrata il 2026-08-19. Non e' derivata dai dati.
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

> **Lettura interpretativa** — registrata il 2026-08-19. Non e' derivata dai dati.
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
| voci dell'MC Appendix | **57** |
| creature vere (statblock distinti) | **68** |
| di cui schede di razze già in `dati/razze/` | 13 |
| di cui razze e culture fuori dal roster | 4 |
| **creature da convertire** | **48** |

**6 voci hanno lo statblock su più colonne**: una voce, più creature.

| voce | pag. | creature |
|---|---:|---|
| **Avian** | 4 | 4 — Emre, Kingfisher, Skyfisher, 'Wari |
| **Dragon, Astral** | 20 | 2 — Astral Dragon (unmated), Astral Dragon (mated pair) |
| **Man (of Krynn)** | 59 | 4 — Ice Folk, Knights of Solamnia, Plainsmen, Rebels |
| **Shadowperson** | 71 | 2 — Shadowperson, Revered Ancient One |
| **Stag** | 78 | 3 — Wild Stag, Giant Stag, The White Stag |
| **Tayling** | 79 | 2 — Tayling, Taylang |

**8 nomi di voce erano sbagliati** nel testo estratto, non solo i quattro
verificati per primi. Il dettaglio completo — testo estratto, nome reale, pagina,
causa — è nella tabella più sotto.

> **Lettura interpretativa** — registrata il 2026-08-19. Non e' derivata dai dati.
>
> **L'estrazione non ha solo sbagliato i nomi: ha perso dei dati.** In tre voci
> le colonne di destra sono sparite del tutto — `Avian` aveva quattro uccelli e
> ne restavano due, `Stag` tre cervi e ne restava uno, `Man (of Krynn)` quattro
> culture e ne restavano due. Sono **sette creature** che dal testo estratto non
> esistevano affatto.
>
> Il conteggio passa così da 57 voci a **68** creature vere. Non è un
> aggiustamento marginale: è il 24% in più, e cambia la stima di quanto lavoro
> c'è davanti.
>
> Due ritrovamenti che vale la pena segnalare. Il **Cervo Bianco**, una delle tre
> colonne di `Stag`, non è una bestia: è unico, di allineamento legale buono,
> vale 2.000 punti esperienza e ha capacità magiche — è una creatura sacra, e dal
> testo estratto non risultava. Il **Drago Astrale** ha due statblock ma è una
> specie sola in due stati, il solitario e la coppia accoppiata da 35 dadi vita
> che il manuale tratta come singola creatura.

---

## Parte 5 — da dove iniziare

Le **48 creature** da convertire, tolte le 13 schede di razze giocanti già
coperte da `dati/razze/` e le 4 razze fuori roster. **Proposta, non decisione.**

Ricostruito sull'elenco completo dopo il ricontaggio voce per voce. I **cinque
draconici non sono in questa lista**: hanno già un precedente ufficiale
completo, analizzato nelle parti 2-4 sopra. Restano **41 creature**
su **35 voci** nelle cinque fasce, più il Cervo Bianco fuori fascia.

### Prima — servono subito all'arena (4)

| creatura | perché | analogo SRD |
|---|---|---|
| Traag (proto-draconico) | Completa la famiglia dei draconici, l'unica su cui abbiamo un precedente ufficiale. E' il gradino piu' basso: serve all'arena come avversario iniziale. | sì — Kobold / Goblin |
| Warrior, Skeleton | Non morto generico di basso livello, il riempitivo classico dell'arena. Ha l'analogo SRD piu' diretto di tutto il roster. | sì — Skeleton |
| Thanoi (Walrus Man) | Umanoide bestiale di fascia bassa, identitario del nord di Krynn. | sì — Gnoll / Lizardfolk |
| Kyrie | Umanoidi alati, avversari volanti di fascia bassa: l'arena ha bisogno di bersagli in volo presto. | sì — Harpy / Hippogriff |

### Seconda — riempitivi di fascia bassa e media (8 voci, 13 creature)

| creatura | perché | analogo SRD |
|---|---|---|
| Horax | Bestia da branco, utile a riempire incontri senza tattica complessa. | sì — Giant Wasp / Giant Spider |
| Skrit | Come sopra, fascia bassissima. | sì — Giant Centipede |
| Wichtlin | Non morto elfico, identitario e di fascia media. | sì — Wight / Specter |
| Fetch | Non morto mutaforma di fascia media. | sì — Shadow / Ghost |
| Spectral Minion | Non morto evocato, fascia media. | sì — Specter |
| Shadowperson | Non morto elfico di fascia media. La voce contiene anche il Revered Ancient One, il suo anziano — quasi tutto `Nil`: non combatte, va convertito come comparsa non nella scheda dell'avversario. | parziale — Shadow / Specter |
| Avian (Emre, Kingfisher, Skyfisher, 'Wari) | Quattro varianti sotto una sola voce: uccelli o umanoidi alati acquatici di Krynn. Ruolo e taglia esatti non ancora verificati sull'immagine di pagina — segnaposto di fascia bassa. | da verificare — probabile Hawk / Giant Owl |
| Stag (Wild Stag, Giant Stag) | I due cervi normali della voce Stag: bestie da branco pulite. Il terzo abitante della voce, il Cervo Bianco, e' trattato a parte, fuori fascia — vedi sotto. | sì — Elk / Giant Elk |

### Terza — identitari ma senza analogo pulito (9 voci, 10 creature)

| creatura | perché | analogo SRD |
|---|---|---|
| Dreamshadow | Non morto psichico: identitario ma senza analogo pulito. | no |
| Dreamwraith | Come sopra, fascia piu' alta. | no |
| Fireshadow | Creatura elementale di Krynn, nessun analogo diretto. | no |
| Fire Minion | Come sopra. | parziale — Magmin |
| Tylor | Mostruosita' grande e identitaria, fascia medio-alta. | parziale — Chimera |
| Knight, Death | **Il Cavaliere della Morte**: e' Lord Soth, cioe' l'antagonista simbolo del setting. SotDQ ha lo statblock di Soth come PERSONAGGIO, che puo' servire da riferimento ma non e' la scheda di specie. | parziale — Wight / Revenant, ma sottodimensionati |
| Haunt, Knight | Variante spettrale del precedente. | no |
| Yaggol | Sotto-razza degenerata dei mind flayer, con kit complesso (sei attacchi piu' un potere psichico) e la resistenza magica piu' alta del bestiario (50%). Identitario e costoso: nessun mostro SRD a GS 1/4-4 replica un mind-flayer minore. | no — Mind Flayer vero e' GS 7, fuori target |
| Tayling (+ Taylang) | Gemelli telepatici che nascono sempre in coppia: l'intelligente (Tayling) e il bestiale (Taylang). Nessun analogo SRD replica la coppia legata telepaticamente. | no |

### Quarta — nicchia (10)

| creatura | perché | analogo SRD |
|---|---|---|
| Gurik Cha-ahl | Creatura di nicchia. | no |
| Disir | Creatura di nicchia. | no |
| Kani Doll | Costrutto di nicchia. | parziale — Homunculus |
| Shimmerweed | Pianta, nicchia. | parziale — Shrieker |
| Wyndlass | Creatura acquatica di nicchia. | no |
| Kalothagh (Prickleback) | Bestia acquatica. | sì — Reef Shark |
| Anemone, Giant | Bestia acquatica. | parziale |
| Imp, Blood Sea | Diavoletto locale. | sì — Imp / Quasit |
| Eyewing | Bestia volante di nicchia. | no |
| Bear, Ice | Bestia. | sì — Polar Bear |

### Quinta — draghi, non servono alla Fase 2 (4)

| creatura | perché | analogo SRD |
|---|---|---|
| Dragon, Amphi | Drago: la Fase 2 non ne ha bisogno. | sì — draghi SRD |
| Dragon, Kodragon | Come sopra. | sì |
| Dragon, Sea | Come sopra. | sì |
| Dragon, Astral | Drago, come sopra. Due statblock nella voce (solitario e coppia accoppiata da 35 DV) ma una sola specie in due stati: contata come una riga, non due. | sì |

### Fuori fascia — non da arena (1)

**The White Stag.** Il terzo abitante della voce Stag (pag. 78). Non è una bestia: è unico, allineamento legale buono, 2.000 PE, con capacità magiche — una creatura sacra da incontro narrativo, non un avversario. Proposta: schedarlo quando esiste uno schema per creature uniche/da avventura (vicino allo schema Personaggio), non forzarlo nel bestiario da combattimento.


> **Lettura interpretativa** — registrata il 2026-08-19. Non e' derivata dai dati.
>
> **Il criterio è l'arena, non la completezza.** La Fase 2 è un motore di
> combattimento e ha bisogno di avversari fra GS 1/4 e GS 4, in quantità e con
> tattiche diverse fra loro. Non ha bisogno di draghi: un drago in arena è una
> sessione, non un banco di prova. Per questo la quinta fascia, ora che i nomi
> corrotti sono risolti, contiene solo draghi — compreso il Drago Astrale, che
> resta un drago anche se il manuale gli dedica due statblock per due stati
> della stessa specie.
>
> La prima fascia è scelta così: il **Traag** completa la famiglia dei draconici
> e quindi si converte con il precedente ufficiale ancora in mano; **Scheletro
> guerriero**, **Thanoi** e **Kyrie** coprono i tre ruoli che a un'arena servono
> subito — non morto generico, fante bestiale, avversario volante — e hanno tutti
> un analogo SRD diretto.
>
> La terza fascia è quella che costa di più, e va affrontata quando il metodo è
> rodato: sono creature identitarie senza analogo pulito, dove bisogna comporre.
> Il **Cavaliere della Morte** è il caso simbolo — è Lord Soth — e ha una
> particolarità utile: SotDQ ha lo statblock di Soth come personaggio, che serve
> da riferimento numerico anche se non è la scheda di specie. Lo **Yaggol** è il
> secondo caso costoso emerso dal ricontaggio: un derivato di mind flayer con
> kit complesso e la resistenza magica più alta del bestiario, senza analogo
> SRD nella fascia di grado utile alla Fase 2.
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

> **Lettura interpretativa** — registrata il 2026-08-19. Non e' derivata dai dati.
>
> **La causa è quasi sempre una sola, e non è un difetto delle pagine.**
> 6 casi su 8 sono voci con statblock a **più colonne**: una sola
> voce del manuale contiene due o più creature affiancate, ciascuna con la
> propria colonna di valori. L'estrattore, che lavora a due colonne di testo,
> legge i titoli delle colonne di fianco come se fossero una riga sola. Gli
> altri 2 hanno un'altra causa: `Minotaur (of Krynn)` prendeva
> l'intestazione di una colonna interna (`Blood Sea Minotaur`) come titolo
> della voce; `Yaggol` aveva semplicemente le lettere spaziate nello stampato.
>
> **Questo cambia il conteggio del bestiario.** Dietro le 6 voci a più colonne
> ci sono **17 creature**, non 6: `Man (of Krynn)` ne contiene quattro,
> `Avian` altrettante, `Stag` tre, `Tayling`, `Shadowperson` e `Dragon, Astral`
> due ciascuna. Il numero vero — **57 voci, 68 creature** — è quello
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
- ~~Conteggio vero delle creature dell'MC Appendix~~ → **57 voci,
  68 creature**, stabilito voce per voce sulle immagini di pagina —
  vedi "Il conteggio vero del bestiario" sopra.

> **Lettura interpretativa** — registrata il 2026-08-19. Non e' derivata dai dati.
>
> Nessuna delle tre resta aperta. Quello che resta, e non è bloccante per
> cominciare a convertire, è un disallineamento scoperto per strada: il
> generatore di `RAPPORTO-mostri.md` (`confronta_mostri.py`) conta le voci
> dell'MC Appendix rileggendo il testo estratto con un'altra regola (i blocchi
> `CLIMATE/TERRAIN:`), indipendente da questo ricontaggio verificato sulle
> immagini. Dà **55**, non 57. Non è lo stesso tipo di errore dei nomi
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

**Creatura di riferimento.** Lo Yaggol (MC Dragonlance Appendix, pag. 87) ha resistenza magica 50%, la piu' alta del bestiario: e' la creatura su cui questa decisione pesera' di piu', e va tenuta presente quando si valuta se ripristinarla.
