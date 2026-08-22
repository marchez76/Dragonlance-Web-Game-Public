# Attribuzione SRD 5.1

Parte del materiale in questo repository deriva dal **System Reference
Document 5.1** ("SRD 5.1"), distribuito da Wizards of the Coast LLC sotto
licenza **Creative Commons Attribution 4.0 International** (CC-BY-4.0).

La licenza richiede l'attribuzione. Questo file la fornisce.

---

## Attribuzione richiesta

> This work includes material taken from the System Reference Document 5.1
> ("SRD 5.1") by Wizards of the Coast LLC and available at
> https://dnd.wizards.com/resources/systems-reference-document.
> The SRD 5.1 is licensed under the Creative Commons Attribution 4.0
> International License available at
> https://creativecommons.org/licenses/by/4.0/legalcode.

---

## Quali file derivano dall'SRD 5.1

| file | cosa contiene |
|---|---|
| `dati/_srd51.py` | Tabelle di classe: privilegi livello per livello, dado vita e tiri salvezza competenti di Fighter, Wizard, Cleric, Paladin, Rogue. |
| `dati/_sfere_5e.py` | La lista incantesimi base del chierico (105 voci), usata come dominio del filtro delle sfere 2e. Le sfere assegnate e le note sono nostre; i nomi, i livelli e le scuole vengono dall'SRD. |
| `dati/_fonti/srd51_mostri.py` | Bestiario completo: 322 creature (tutti i gradi di sfida dell'SRD 5.1), con taglia, tipo, classe armatura, punti ferita e velocità. |
| `dati/_fonti/srd51_equipaggiamento.py` | Equipaggiamento ordinario per l'arena (Fase 2): 37 armi, 13 armature/scudo e 28 voci di attrezzatura d'avventura, con danno, tipo di danno, proprietà, CA, requisito di Forza, svantaggio a Furtività, costo e peso. |
| `dati/_fonti/srd51_incantesimi.py` | Lista incantesimi completa dell'SRD 5.1: 319 voci, tutte le 8 classi (non solo il chierico), con livello, scuola, componenti, tempo di lancio, gittata, durata e testo integrale dell'effetto. |

I valori sono trascritti verbatim. Ogni file dichiara nella propria
intestazione l'endpoint da cui provengono. `dati/build_oggetti.py` legge
`srd51_equipaggiamento.py` e genera `dati/oggetti/*.json`: quei JSON generati
non sono in questo repository pubblico (vedi sotto, `dati/oggetti/` è
comunque escluso perché condivide la cartella con oggetti magici trascritti
dai manuali 2e), ma la fonte da cui sono generati sì. `dati/build_incantesimi.py`
genera invece `dati/incantesimi/*.json` **in questo stesso repository
pubblico**: a differenza di `dati/oggetti/`, quella cartella non condivide
spazio con alcun caso a `source_2e` (`incantesimo.schema.json` non ne ha uno),
quindi non c'è testo di manuale da proteggere e i JSON generati restano qui.

## Come sono stati ottenuti

Tramite l'API pubblica di [Open5e](https://open5e.com). Due endpoint diversi:

- `api.open5e.com/v1/...` con `document__slug=wotc-srd` — usato per bestiario,
  classi, sfere, armi e armature. Espone l'SRD 5.1 in forma strutturata.
- `api.open5e.com/v2/items/` con `document__key=srd-2014` — usato per
  l'attrezzatura d'avventura, che il v1 non copre con un endpoint proprio.
  Il parametro di filtro non esclude dai risultati il materiale del 5.2/2024
  (stesso dominio, documento diverso): è stato necessario un filtro a valle
  su `document.key == "srd-2014"` per isolare la fonte corretta.

Open5e distribuisce quel materiale sotto la stessa licenza CC-BY-4.0.

**Verifica dell'edizione (21-22/08/2026).** Il v1 espone un solo documento
Wizards of the Coast (`wotc-srd`, versione 5.1: l'SRD 5.2/2024 non esiste in
v1) — il rischio di contaminazione fra edizioni che si è posto per
l'attrezzatura (v2) è strutturalmente impossibile per tutto ciò che passa da
v1: bestiario, classi, sfere, armi, armature, incantesimi. Verificato anche
empiricamente su tutte e 322 le voci del bestiario, tutte e 319 le voci degli
incantesimi e sulle classi interrogate singolarmente: `document__slug` e
`document__title` uniformi su ogni risultato, nessuna voce fuori posto.

I nomi italiani (`name.it`) in tutti questi file sono traduzioni di lavoro
nostre, non una traduzione ufficiale licenziata: stesso trattamento già in
uso per i nomi di razze, classi e mostri nel repository privato.

---

## Cosa NON è coperto da questa licenza

Il resto del repository non deriva dall'SRD e non è coperto da CC-BY-4.0.

In particolare, **nessun contenuto tratto dai manuali AD&D 2e o da
*Dragonlance: Shadow of the Dragon Queen* si trova in questo repository
pubblico.** Quel materiale — le trascrizioni in `source_2e`, i testi estratti,
i PDF — sta in un repository privato separato, per la ragione spiegata nel
`.gitignore`: è trascrizione fedele di opere protette, e la fedeltà che lo
rende utile al progetto è esattamente ciò che lo rende non pubblicabile.

I rapporti presenti qui citano quei manuali per numero di pagina e ne
discutono le scelte di design, ma non ne riproducono il testo oltre le brevi
citazioni necessarie all'argomentazione.

---

## Marchi

Dungeons & Dragons, D&D, Dragonlance e i relativi loghi sono marchi di Wizards
of the Coast LLC. Questo progetto non è affiliato con Wizards of the Coast né
approvato da essa. È un lavoro personale, non commerciale.
