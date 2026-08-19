# Verifica di giocabilità del filtro delle sfere

*Generato da `dati/verifica_sfere.py` il 2026-08-14.*

> **Cos'è.** Il conteggio richiesto prima di attivare il filtro della
> decisione 24. Non risolve nulla: non aggiunge sfere, non ammorbidisce il
> filtro, non concede eccezioni. Conta e basta.
>
> Ogni numero è derivato da `dati/divinita/*.json` e da `dati/_sfere_5e.py`.
> Le letture sono marcate e datate.

## Come è stato calcolato

Lista base del chierico **SRD 5.1**: **105 incantesimi**, 0 trucchetti compresi
(7 trucchetti e 98 incantesimi dal 1° al 9°). Gli incantesimi di **Dominio**
non entrano nel conteggio: si ottengono con la sottoclasse e non passano dal
filtro.

**Regola dell'accesso minore**: come in 2e, l'accesso minore concede solo
incantesimi **fino al 3° livello**. È applicata.

**Attribuzioni**: 77 incantesimi ereditano la sfera da un antenato 2e diretto
(`fonte`); **28 sono attribuzioni nostre** (`nostra`), classificate per effetto e
distinguibili nel dato.

---

## Sintesi

| divinità | famiglia | sfere | incant. | truc. | livelli vuoti | sotto soglia | guarigione | offesa | Dominio |
|---|---|---|---:|---:|---|---|:-:|:-:|---|
| Branchala | good | 6M/2m | 30 | 3 | 4°, 7° | 5°, 8°, 9° | sì | sì | `Life` |
| Zeboim | evil | 6M/1m | 33 | 4 | 9° | 4°, 5°, 6°, 7° | **NO** | sì | `Tempest` |
| Majere | good | 5M/2m | 41 | 3 | 8° | 9° | **NO** | **NO** | `Knowledge` |
| Chemosh | evil | 4M/2m | 42 | 3 | 8° | 4°, 6°, 9° | sì | sì | `Death` |
| Chislev | neutral | 7M/3m | 42 | 3 | — | 4°, 5°, 6°, 7°, 9° | sì | sì | `Nature` |
| Shinare | neutral | 5M/2m | 42 | 5 | 9° | 6°, 7°, 8° | **NO** | sì | `Trickery` |
| Habbakuk | good | 5M/2m | 43 | 3 | 9° | 7°, 8° | sì | sì | `Nature` |
| Sargonnas | evil | 5M/3m | 44 | 5 | 8° | 4°, 9° | **NO** | sì | `War` |
| Zivilyn | neutral | 5M/0m | 44 | 3 | 8° | 9° | **NO** | **NO** | `Knowledge` |
| Hiddukel | evil | 3M/3m | 47 | 4 | 8° | 4°, 5°, 7°, 9° | **NO** | **NO** | `Trickery` |
| Morgion | evil | 5M/1m | 47 | 3 | 8° | 4°, 7°, 9° | sì | sì | `Death` |
| Sirrion | neutral | 6M/1m | 50 | 3 | — | 8°, 9° | sì | sì | `Light` |
| Paladine | good | 7M/1m | 53 | 4 | — | 8°, 9° | sì | sì | `Life` |
| Reorx | neutral | 7M/2m | 55 | 5 | 9° | — | sì | sì | `Forge` |
| Lunitari | neutral | 6M/2m | 57 | 3 | 8° | 9° | sì | sì | `Knowledge` |
| Kiri-Jolith | good | 5M/3m | 62 | 5 | — | 4°, 7°, 8°, 9° | sì | sì | `War` |
| Solinari | good | 6M/2m | 65 | 5 | 8° | 9° | sì | sì | `Light` |
| Gilean | neutral | 6M/4m | 66 | 6 | — | 7°, 8°, 9° | sì | sì | `Knowledge` |
| Takhisis | evil | 5M/5m | 66 | 6 | — | 8°, 9° | sì | sì | `Trickery` |
| Nuitari | evil | 6M/3m | 69 | 5 | 8° | 9° | sì | sì | `Knowledge` |
| Mishakal | good | 8M/1m | 70 | 5 | — | 8° | sì | sì | `Life` |

"Sotto soglia" = meno di 3 incantesimi disponibili a quel livello.
"Guarigione" conta solo le cure vere (Cure Wounds e famiglia), non le
restorazioni. "Offesa" conta solo il danno diretto, non i controlli.

## Incantesimi per livello

| divinità | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° | totale |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Branchala | 8 | 7 | 5 | 0 | 1 | 3 | 0 | 2 | 1 | 27 |
| Zeboim | 8 | 4 | 9 | 2 | 1 | 1 | 1 | 3 | 0 | 29 |
| Majere | 7 | 8 | 5 | 4 | 5 | 4 | 3 | 0 | 2 | 38 |
| Chemosh | 8 | 8 | 8 | 1 | 5 | 2 | 5 | 0 | 2 | 39 |
| Chislev | 10 | 10 | 8 | 2 | 2 | 2 | 1 | 3 | 1 | 39 |
| Shinare | 9 | 8 | 9 | 3 | 3 | 2 | 1 | 2 | 0 | 37 |
| Habbakuk | 10 | 8 | 9 | 4 | 4 | 3 | 1 | 1 | 0 | 40 |
| Sargonnas | 9 | 7 | 8 | 2 | 4 | 3 | 4 | 0 | 2 | 39 |
| Zivilyn | 6 | 9 | 8 | 3 | 6 | 3 | 4 | 0 | 2 | 41 |
| Hiddukel | 9 | 12 | 12 | 2 | 2 | 3 | 2 | 0 | 1 | 43 |
| Morgion | 9 | 11 | 10 | 2 | 4 | 4 | 2 | 0 | 2 | 44 |
| Sirrion | 9 | 8 | 8 | 4 | 5 | 6 | 4 | 1 | 2 | 47 |
| Paladine | 12 | 10 | 10 | 3 | 4 | 3 | 3 | 2 | 2 | 49 |
| Reorx | 12 | 8 | 13 | 4 | 4 | 3 | 3 | 3 | 0 | 50 |
| Lunitari | 11 | 13 | 8 | 3 | 7 | 6 | 4 | 0 | 2 | 54 |
| Kiri-Jolith | 14 | 14 | 13 | 2 | 5 | 4 | 2 | 2 | 1 | 57 |
| Solinari | 13 | 12 | 13 | 3 | 7 | 6 | 4 | 0 | 2 | 60 |
| Gilean | 14 | 13 | 13 | 3 | 6 | 5 | 2 | 2 | 2 | 60 |
| Takhisis | 13 | 14 | 16 | 3 | 3 | 3 | 4 | 2 | 2 | 60 |
| Nuitari | 13 | 14 | 15 | 3 | 7 | 6 | 4 | 0 | 2 | 64 |
| Mishakal | 10 | 16 | 13 | 4 | 8 | 6 | 4 | 1 | 3 | 65 |

---

## Il problema è nella mappa, non nelle divinità

| sfera 2e | incantesimi 5e | di cui da antenato | divinità che la possiedono |
|---|---:|---:|---:|
| All | 7 | 5 | 21 |
| Animal | 1 | 1 | 6 |
| Astral | 3 | 2 | 12 |
| Charm | 5 | 5 | 10 |
| Combat | 8 | 5 | 13 |
| Creation | 3 | 2 | 9 |
| Divination | 17 | 14 | 12 |
| Elemental | 7 | 7 | 5 |
| Guardian | 7 | 3 | 12 |
| Healing | 12 | 8 | 15 |
| Necromantic | 17 | 14 | 7 |
| Plant | 0 | 0 | 5 |
| Protection | 15 | 9 | 11 |
| Summoning | 6 | 4 | 7 |
| Sun | 4 | 2 | 13 |
| Weather | 1 | 1 | 5 |

> **Lettura interpretativa** — registrata il 2026-08-14. Non e' derivata dai dati.
>
> **1 sfera su 16 non trova un solo incantesimo nella lista base del chierico
> 5e: Plant.** Animal ne trova 1, Weather 1. Non è un errore della
> mappatura: è che la 5e ha spostato piante, animali e meteo sulla lista del
> **druido**, che nel 2014 è una classe separata. In 2e quelle sfere erano
> sacerdotali a pieno titolo.
>
> La conseguenza è che le divinità della natura — Chislev, Zeboim, Habbakuk,
> Branchala — pagano un prezzo che non dipende dalla loro ricchezza in 2e ma da
> dove la 5e ha messo quel materiale. Chislev ha 7 sfere maggiori, più di quasi
> tutti, e tre di quelle sfere valgono in tutto 2 incantesimi.
>
> Questo è materiale per una decisione, non una decisione: le strade possibili
> sono attingere alla lista del druido per quelle sfere, accettare lo squilibrio,
> o compensare col Dominio. Non ne ho scelta nessuna.

---

## Divinità sotto soglia

### Senza alcuna guarigione vera

- **Zeboim** (evil) — 33 incantesimi in tutto. Ripieghi disponibili: nessuno.
- **Majere** (good) — 41 incantesimi in tutto. Ripieghi disponibili: nessuno.
- **Shinare** (neutral) — 42 incantesimi in tutto. Ripieghi disponibili: nessuno.
- **Sargonnas** (evil) — 44 incantesimi in tutto. Ripieghi disponibili: nessuno.
- **Zivilyn** (neutral) — 44 incantesimi in tutto. Ripieghi disponibili: Greater Restoration, Lesser Restoration, Raise Dead, Regenerate, Resurrection, Revivify, Spare the Dying, True Resurrection.
- **Hiddukel** (evil) — 47 incantesimi in tutto. Ripieghi disponibili: Lesser Restoration, Revivify, Spare the Dying.

### Senza alcuna offesa diretta

- **Majere** — ripieghi di controllo: Bane, Command, Geas, Hold Person.
- **Zivilyn** — ripieghi di controllo: Bane, Bestow Curse, Blindness/Deafness, Contagion.
- **Hiddukel** — ripieghi di controllo: Bane, Bestow Curse, Blindness/Deafness.

### Con livelli completamente vuoti

- **Branchala** — vuoti ai livelli 4°, 7°.
- **Zeboim** — vuoti ai livelli 9°.
- **Majere** — vuoti ai livelli 8°.
- **Chemosh** — vuoti ai livelli 8°.
- **Shinare** — vuoti ai livelli 9°.
- **Habbakuk** — vuoti ai livelli 9°.
- **Sargonnas** — vuoti ai livelli 8°.
- **Zivilyn** — vuoti ai livelli 8°.
- **Hiddukel** — vuoti ai livelli 8°.
- **Morgion** — vuoti ai livelli 8°.
- **Reorx** — vuoti ai livelli 9°.
- **Lunitari** — vuoti ai livelli 8°.
- **Solinari** — vuoti ai livelli 8°.
- **Nuitari** — vuoti ai livelli 8°.

### Con livelli sotto la soglia dei 3 incantesimi

- **Branchala** — livelli 5° (1), 8° (2), 9° (1).
- **Zeboim** — livelli 4° (2), 5° (1), 6° (1), 7° (1).
- **Majere** — livelli 9° (2).
- **Chemosh** — livelli 4° (1), 6° (2), 9° (2).
- **Chislev** — livelli 4° (2), 5° (2), 6° (2), 7° (1), 9° (1).
- **Shinare** — livelli 6° (2), 7° (1), 8° (2).
- **Habbakuk** — livelli 7° (1), 8° (1).
- **Sargonnas** — livelli 4° (2), 9° (2).
- **Zivilyn** — livelli 9° (2).
- **Hiddukel** — livelli 4° (2), 5° (2), 7° (2), 9° (1).
- **Morgion** — livelli 4° (2), 7° (2), 9° (2).
- **Sirrion** — livelli 8° (1), 9° (2).
- **Paladine** — livelli 8° (2), 9° (2).
- **Lunitari** — livelli 9° (2).
- **Kiri-Jolith** — livelli 4° (2), 7° (2), 8° (2), 9° (1).
- **Solinari** — livelli 9° (2).
- **Gilean** — livelli 7° (2), 8° (2), 9° (2).
- **Takhisis** — livelli 8° (2), 9° (2).
- **Nuitari** — livelli 9° (2).
- **Mishakal** — livelli 8° (1).

### Senza trucchetti

Nessuna.

---

## Domini assegnati

| divinità | Dominio | nell'SRD 5.1 | motivo |
|---|---|:-:|---|
| Branchala | Life | sì | Dio della musica e della vita; sfere Healing e Creation maggiori. |
| Chemosh | Death | no — DMG 2014 | Signore dei non morti. Il Dominio Morte non e' nell'SRD 5.1: e' del DMG. Segnalato, non risolto. |
| Chislev | Nature | sì | Dea della natura selvaggia; Animal, Plant, Weather ed Elemental maggiori. |
| Gilean | Knowledge | sì | Il Libro; Divinazione maggiore e ruolo di archivista del mondo. |
| Habbakuk | Nature | sì | Re Pescatore; Animal ed Elemental maggiori. |
| Hiddukel | Trickery | sì | Principe delle Menzogne. Tre sole sfere: e' il caso piu' povero. |
| Kiri-Jolith | War | sì | Spada della Giustizia; Combat maggiore. E' il dio che concede gli incantesimi ai Cavalieri della Spada. |
| Lunitari | Knowledge | sì | Luna della magia neutrale; Divination e Astral maggiori. |
| Majere | Knowledge | sì | Maestro della Mente; Charm, Divination e Astral maggiori. |
| Mishakal | Life | sì | Mano Guaritrice; otto sfere maggiori fra cui Healing. |
| Morgion | Death | no — DMG 2014 | Vento Nero, dio della malattia. Stesso problema di Chemosh: il Dominio Morte non e' nell'SRD. |
| Nuitari | Knowledge | sì | Luna della magia nera; Divination e Astral maggiori. |
| Paladine | Life | sì | Signore dei Draghi; Healing, Protection e Sun maggiori. |
| Reorx | Forge | no — Xanathar's Guide | La Forgia. Il Dominio Forgia non e' nell'SRD 5.1: e' di Xanathar. Alternativa dentro l'SRD: Guerra. Segnalato. |
| Sargonnas | War | sì | Vendetta Oscura; Combat maggiore. |
| Shinare | Trickery | sì | Vittoria Alata, dea del commercio. Nessun Dominio 2014 copre il commercio: Inganno e' un ripiego. Segnalato. |
| Sirrion | Light | sì | Fiamma Fluente; Elemental (Fuoco) e Combat maggiori. |
| Solinari | Light | sì | Luna della magia bianca; Combat e Divination maggiori. |
| Takhisis | Trickery | sì | Regina delle Tenebre. Il Dominio Morte sarebbe piu' coerente ma non e' nell'SRD. |
| Zeboim | Tempest | sì | Mare Oscuro; Weather ed Elemental (Acqua) maggiori. |
| Zivilyn | Knowledge | sì | Albero del Mondo; Divination e Astral maggiori, cinque sfere tutte maggiori e nessuna minore. |

---

## Ambiguità di fonte trovate

- **Due sfere hanno due grafie nel dato**: `Plant`/`Plants` e
  `Necromantic`/`Necromancy`. Sono la stessa sfera. Senza normalizzazione il
  filtro le tratterebbe come distinte e toglierebbe incantesimi a chi le ha
  nella grafia minoritaria — riguarda Zivilyn (`Plant`), Chemosh (`Plant`) e
  Hiddukel (`Necromancy`). Normalizzate in `_sfere_5e.ALIAS`, non nei JSON:
  il dato di fonte resta com'è stato trascritto.
- **Due Domini assegnati non sono nell'SRD 5.1**: Morte (DMG 2014) per Chemosh,
  Morgion e — se si volesse — Takhisis; Forgia (Xanathar) per Reorx. Con solo
  l'SRD servono ripieghi.
- **Nessun Dominio 2014 copre il commercio**: Shinare è assegnata a Inganno per
  esclusione, non per coerenza.

---

## Le attribuzioni nostre

Incantesimi 5e senza antenato 2e diretto, classificati per effetto. Restano distinguibili nel dato con `derivation: nostra`.

| incantesimo | liv. | scuola | sfere assegnate | perché |
|---|---:|---|---|---|
| Guidance | 0 | Divination | Divination | Trucchetto. La 2e non dava trucchetti ai sacerdoti: attribuzione per effetto. |
| Light | 0 | Evocation | Sun | Trucchetto. |
| Mending | 0 | Transmutation | Creation | Trucchetto. |
| Resistance | 0 | Abjuration | Protection | Trucchetto. |
| Sacred Flame | 0 | Evocation | Combat | Trucchetto. Unica offesa a volonta' del chierico 5e: la sfera Combat decide se una divinita' ce l'ha. |
| Spare the Dying | 0 | Necromancy | Necromantic | Trucchetto. |
| Thaumaturgy | 0 | Transmutation | All | Trucchetto. Manifestazione di potere divino senza effetto meccanico: assegnato ad All perche' non e' materia di alcuna sfera. |
| Guiding Bolt | 1 | Evocation | Combat | Nessun antenato 2e. Classificato per effetto: attacco a distanza radiante. |
| Healing Word | 1 | Evocation | Healing | La 2e non ha cure ad azione bonus. Famiglia cure, sfera Healing. |
| Shield of Faith | 1 | Abjuration | Protection | classificato per effetto |
| Enhance Ability | 2 | Transmutation | All | Nessun antenato sacerdotale. Potenziamento generico: assegnato ad All. |
| Warding Bond | 2 | Abjuration | Protection, Guardian | classificato per effetto |
| Beacon of Hope | 3 | Abjuration | Healing | classificato per effetto |
| Mass Healing Word | 3 | Evocation | Healing | classificato per effetto |
| Revivify | 3 | Conjuration | Necromantic | classificato per effetto |
| Sending | 3 | Evocation | Divination | classificato per effetto |
| Spirit Guardians | 3 | Conjuration | Combat | classificato per effetto |
| Guardian of Faith | 4 | Conjuration | Guardian | classificato per effetto |
| Hallow | 5 | Evocation | Guardian, Protection | classificato per effetto |
| Legend Lore | 5 | Divination | Divination | classificato per effetto |
| Planar Binding | 5 | Abjuration | Summoning | classificato per effetto |
| Forbiddance | 6 | Abjuration | Guardian | classificato per effetto |
| Conjure Celestial | 7 | Conjuration | Summoning | classificato per effetto |
| Etherealness | 7 | Transmutation | Astral | classificato per effetto |
| Antimagic Field | 8 | Abjuration | Protection | classificato per effetto |
| Holy Aura | 8 | Abjuration | Sun, Protection | classificato per effetto |
| Mass Heal | 9 | Conjuration | Healing | classificato per effetto |
| True Resurrection | 9 | Necromancy | Necromantic | classificato per effetto |

---

## Schede per divinità

### Branchala

**30 incantesimi accessibili** su 105 (29%), di cui 3 trucchetti e 9 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 8 | 7 | 5 | 0 | 1 | 3 | 0 | 2 | 1 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Harm, Inflict Wounds
- Dominio: **Life** — Dio della musica e della vita; sfere Healing e Creation maggiori.

### Chemosh

**42 incantesimi accessibili** su 105 (40%), di cui 3 trucchetti e 12 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 8 | 8 | 8 | 1 | 5 | 2 | 5 | 0 | 2 |

- Guarigione: Cure Wounds, Healing Word, Mass Healing Word, Prayer of Healing
- Offesa diretta: Blade Barrier, Divine Word, Flame Strike, Guiding Bolt, Inflict Wounds, Insect Plague, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Death** — Signore dei non morti. Il Dominio Morte non e' nell'SRD 5.1: e' del DMG. Segnalato, non risolto.

### Chislev

**42 incantesimi accessibili** su 105 (40%), di cui 3 trucchetti e 12 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 10 | 10 | 8 | 2 | 2 | 2 | 1 | 3 | 1 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Earthquake, Fire Storm, Guiding Bolt, Harm, Inflict Wounds, Insect Plague, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Nature** — Dea della natura selvaggia; Animal, Plant, Weather ed Elemental maggiori.

### Gilean

**66 incantesimi accessibili** su 105 (63%), di cui 6 trucchetti e 21 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 14 | 13 | 13 | 3 | 6 | 5 | 2 | 2 | 2 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Guiding Bolt, Harm, Inflict Wounds, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Knowledge** — Il Libro; Divinazione maggiore e ruolo di archivista del mondo.

### Habbakuk

**43 incantesimi accessibili** su 105 (41%), di cui 3 trucchetti e 9 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 10 | 8 | 9 | 4 | 4 | 3 | 1 | 1 | 0 |

- Guarigione: Cure Wounds, Healing Word, Mass Healing Word, Prayer of Healing
- Offesa diretta: Earthquake, Fire Storm, Inflict Wounds, Insect Plague
- Dominio: **Nature** — Re Pescatore; Animal ed Elemental maggiori.

### Hiddukel

**47 incantesimi accessibili** su 105 (45%), di cui 4 trucchetti e 14 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 9 | 12 | 12 | 2 | 2 | 3 | 2 | 0 | 1 |

- Guarigione: **nessuna cura**
- Offesa diretta: **nessuna**
- Dominio: **Trickery** — Principe delle Menzogne. Tre sole sfere: e' il caso piu' povero.

### Kiri-Jolith

**62 incantesimi accessibili** su 105 (59%), di cui 5 trucchetti e 20 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 14 | 14 | 13 | 2 | 5 | 4 | 2 | 2 | 1 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Blade Barrier, Divine Word, Flame Strike, Guiding Bolt, Harm, Inflict Wounds, Insect Plague, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **War** — Spada della Giustizia; Combat maggiore. E' il dio che concede gli incantesimi ai Cavalieri della Spada.

### Lunitari

**57 incantesimi accessibili** su 105 (54%), di cui 3 trucchetti e 17 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 11 | 13 | 8 | 3 | 7 | 6 | 4 | 0 | 2 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Blade Barrier, Divine Word, Flame Strike, Guiding Bolt, Harm, Inflict Wounds, Insect Plague, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Knowledge** — Luna della magia neutrale; Divination e Astral maggiori.

### Majere

**41 incantesimi accessibili** su 105 (39%), di cui 3 trucchetti e 9 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 7 | 8 | 5 | 4 | 5 | 4 | 3 | 0 | 2 |

- Guarigione: **nessuna cura**
- Offesa diretta: **nessuna**
- Dominio: **Knowledge** — Maestro della Mente; Charm, Divination e Astral maggiori.

### Mishakal

**70 incantesimi accessibili** su 105 (67%), di cui 5 trucchetti e 17 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 10 | 16 | 13 | 4 | 8 | 6 | 4 | 1 | 3 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Harm, Inflict Wounds
- Dominio: **Life** — Mano Guaritrice; otto sfere maggiori fra cui Healing.

### Morgion

**47 incantesimi accessibili** su 105 (45%), di cui 3 trucchetti e 12 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 9 | 11 | 10 | 2 | 4 | 4 | 2 | 0 | 2 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Harm, Inflict Wounds
- Dominio: **Death** — Vento Nero, dio della malattia. Stesso problema di Chemosh: il Dominio Morte non e' nell'SRD.

### Nuitari

**69 incantesimi accessibili** su 105 (66%), di cui 5 trucchetti e 21 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 13 | 14 | 15 | 3 | 7 | 6 | 4 | 0 | 2 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Blade Barrier, Divine Word, Flame Strike, Guiding Bolt, Harm, Inflict Wounds, Insect Plague, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Knowledge** — Luna della magia nera; Divination e Astral maggiori.

### Paladine

**53 incantesimi accessibili** su 105 (50%), di cui 4 trucchetti e 19 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 12 | 10 | 10 | 3 | 4 | 3 | 3 | 2 | 2 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Guiding Bolt, Harm, Inflict Wounds, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Life** — Signore dei Draghi; Healing, Protection e Sun maggiori.

### Reorx

**55 incantesimi accessibili** su 105 (52%), di cui 5 trucchetti e 18 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 12 | 8 | 13 | 4 | 4 | 3 | 3 | 3 | 0 |

- Guarigione: Cure Wounds, Healing Word, Mass Healing Word, Prayer of Healing
- Offesa diretta: Blade Barrier, Divine Word, Earthquake, Fire Storm, Flame Strike, Guiding Bolt, Inflict Wounds, Insect Plague, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Forge** — La Forgia. Il Dominio Forgia non e' nell'SRD 5.1: e' di Xanathar. Alternativa dentro l'SRD: Guerra. Segnalato.

### Sargonnas

**44 incantesimi accessibili** su 105 (42%), di cui 5 trucchetti e 13 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 9 | 7 | 8 | 2 | 4 | 3 | 4 | 0 | 2 |

- Guarigione: **nessuna cura**
- Offesa diretta: Blade Barrier, Divine Word, Flame Strike, Guiding Bolt, Insect Plague, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **War** — Vendetta Oscura; Combat maggiore.

### Shinare

**42 incantesimi accessibili** su 105 (40%), di cui 5 trucchetti e 15 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 9 | 8 | 9 | 3 | 3 | 2 | 1 | 2 | 0 |

- Guarigione: **nessuna cura**
- Offesa diretta: Guiding Bolt, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Trickery** — Vittoria Alata, dea del commercio. Nessun Dominio 2014 copre il commercio: Inganno e' un ripiego. Segnalato.

### Sirrion

**50 incantesimi accessibili** su 105 (48%), di cui 3 trucchetti e 16 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 9 | 8 | 8 | 4 | 5 | 6 | 4 | 1 | 2 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Blade Barrier, Divine Word, Earthquake, Fire Storm, Flame Strike, Guiding Bolt, Harm, Inflict Wounds, Insect Plague, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Light** — Fiamma Fluente; Elemental (Fuoco) e Combat maggiori.

### Solinari

**65 incantesimi accessibili** su 105 (62%), di cui 5 trucchetti e 20 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 13 | 12 | 13 | 3 | 7 | 6 | 4 | 0 | 2 |

- Guarigione: Cure Wounds, Heal, Healing Word, Mass Cure Wounds, Mass Heal, Mass Healing Word, Prayer of Healing
- Offesa diretta: Blade Barrier, Divine Word, Flame Strike, Guiding Bolt, Harm, Inflict Wounds, Insect Plague, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Light** — Luna della magia bianca; Combat e Divination maggiori.

### Takhisis

**66 incantesimi accessibili** su 105 (63%), di cui 6 trucchetti e 24 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 13 | 14 | 16 | 3 | 3 | 3 | 4 | 2 | 2 |

- Guarigione: Cure Wounds, Healing Word, Mass Healing Word, Prayer of Healing
- Offesa diretta: Guiding Bolt, Inflict Wounds, Sacred Flame, Spirit Guardians, Spiritual Weapon
- Dominio: **Trickery** — Regina delle Tenebre. Il Dominio Morte sarebbe piu' coerente ma non e' nell'SRD.

### Zeboim

**33 incantesimi accessibili** su 105 (31%), di cui 4 trucchetti e 8 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 8 | 4 | 9 | 2 | 1 | 1 | 1 | 3 | 0 |

- Guarigione: **nessuna cura**
- Offesa diretta: Earthquake, Fire Storm, Insect Plague
- Dominio: **Tempest** — Mare Oscuro; Weather ed Elemental (Acqua) maggiori.

### Zivilyn

**44 incantesimi accessibili** su 105 (42%), di cui 3 trucchetti e 9 da attribuzione nostra.

| livello | 1° | 2° | 3° | 4° | 5° | 6° | 7° | 8° | 9° |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| incantesimi | 6 | 9 | 8 | 3 | 6 | 3 | 4 | 0 | 2 |

- Guarigione: **nessuna cura**
- Offesa diretta: **nessuna**
- Dominio: **Knowledge** — Albero del Mondo; Divination e Astral maggiori, cinque sfere tutte maggiori e nessuna minore.

