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

I valori sono trascritti verbatim. Ogni file dichiara nella propria
intestazione l'endpoint da cui provengono.

## Come sono stati ottenuti

Tramite l'API pubblica di [Open5e](https://open5e.com), interrogando
`api.open5e.com` con `document__slug=wotc-srd`, che espone il contenuto
dell'SRD 5.1 in forma strutturata. Open5e distribuisce quel materiale sotto la
stessa licenza CC-BY-4.0.

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
