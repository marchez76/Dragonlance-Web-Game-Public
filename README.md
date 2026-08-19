# Dragonlance Web GDR — conversione da AD&D 2e a D&D 5e

Progetto personale di conversione dell'ambientazione Dragonlance da AD&D 2ª
edizione a D&D 5ª edizione, per uso privato. Non affiliato né approvato da
Wizards of the Coast.

## Cosa contiene questo repository

Documenti di analisi, script di elaborazione e schemi:

- documenti di progetto e diagnostica (`CONTESTO-PROGETTO.md`,
  `dati/RAPPORTO-*.md`, `dati/DOSSIER-*.md`)
- script di build, validazione e generazione (`build_*.py`, `valida_*.py`,
  `genera_*.py`, `motore/`)
- schemi JSON che descrivono la *struttura* dei dati di gioco
  (`dati/schema/*.json`)
- un sottoinsieme dell'SRD 5.1, sotto licenza CC-BY-4.0 (`dati/_srd51.py`,
  `dati/_sfere_5e.py`, `dati/_fonti/srd51_mostri.py`)

## Cosa NON contiene, e perché

**Nessun testo dei manuali AD&D 2e o di *Shadow of the Dragon Queen*.** Le
trascrizioni fedeli (`source_2e`: requisiti, tabelle di avanzamento, testi
delle capacità, statblock) stanno in un repository privato separato, perché
derivano da manuali protetti posseduti in copia cartacea: la fedeltà che le
rende utili al progetto è la stessa che le rende non ridistribuibili.

I documenti di analisi qui presenti citano quei manuali per fonte e pagina e
ne discutono le scelte di design, ma non ne riproducono il contenuto oltre le
brevi citazioni necessarie ad argomentare un punto specifico (es. un refuso
di stampa).

## Licenza del materiale SRD 5.1

Il materiale derivato dal *System Reference Document 5.1* è distribuito da
Wizards of the Coast sotto licenza **Creative Commons Attribution 4.0
International** (CC-BY-4.0). Attribuzione completa in
[`LICENSE-SRD.md`](LICENSE-SRD.md).

Il resto del repository — documenti, script, schemi — non è coperto da
questa licenza ed è lavoro personale, non commerciale.
