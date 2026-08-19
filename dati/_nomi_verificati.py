#!/usr/bin/env python3
"""
Voci dell'MC Dragonlance Appendix con il nome corrotto dall'estrazione a
colonne, riverificate sulle IMMAGINI DI PAGINA.

METODO
    Lo stesso gia' usato per i tratti razziali del PHB 2e e per la ricchezza
    del Cavaliere: la pagina viene renderizzata a immagine e letta, invece di
    fidarsi del testo estratto.

ESITO
    Tutte e quattro leggibili. Nessuna voce resta sospesa.

LA CAUSA E' UNA SOLA, E NON E' UN DIFETTO DELLE PAGINE
    Tre casi su quattro sono voci con statblock a PIU' COLONNE: una sola voce
    del manuale contiene due o piu' creature affiancate, ciascuna con la propria
    colonna di valori. L'estrattore, che lavora a due colonne di testo, legge i
    titoli delle colonne di fianco come se fossero una sola riga.
    Il quarto e' un titolo con spaziatura fra le lettere.
"""

VERIFICATE = [
    {
        "estratto": "Y a g g o l",
        "corretto": "Yaggol",
        "pagina_pdf": 87,
        "causa": "titolo con spaziatura fra le lettere nel layout",
        "creature": ["Yaggol"],
        "nota": "Sotto-razza degenerata dei mind flayer. Statblock unico e "
                "leggibile (MC Dragonlance Appendix, pag. 87). "
                "E' la creatura con la resistenza magica piu' alta del "
                "bestiario: rilevante per la decisione 27 gruppo C.",
    },
    {
        "estratto": "Tayling Tayland",
        "corretto": "Tayling",
        "pagina_pdf": 79,
        "causa": "statblock a due colonne",
        "creature": ["Tayling", "Taylang"],
        "nota": "UNA voce, DUE creature: gemelli telepatici che nascono sempre "
                "in coppia, l'intelligente (Tayling, DV 4) e il bestiale "
                "(Taylang, DV 8). Il testo estratto leggeva \"Tayland\": "
                "sull'immagine e' **Taylang**. Le due colonne vanno separate "
                "in due mostri distinti.",
    },
    {
        "estratto": "Shadowperson Revered Ancient One",
        "corretto": "Shadowperson",
        "pagina_pdf": 71,
        "causa": "statblock a due colonne",
        "creature": ["Shadowperson", "Revered Ancient One"],
        "nota": "UNA voce, DUE creature: lo shadowperson comune (DV 3+1) e il "
                "Revered Ancient One, la cui colonna e' quasi tutta \"Nil\" "
                "perche' e' un anziano non combattente. La seconda va "
                "registrata ma probabilmente con ruolo `non-combattente`.",
    },
    {
        "estratto": "Ice Folk Knights of",
        "corretto": "Man (of Krynn)",
        "pagina_pdf": 59,
        "causa": "statblock a QUATTRO colonne",
        "creature": ["Ice Folk", "Knights of Solamnia", "Plainsmen", "Rebels"],
        "nota": "UNA voce, QUATTRO creature: e' la scheda \"Man (of Krynn)\", "
                "cioe' gli umani di Krynn nelle loro quattro varianti PNG. "
                "L'estrattore aveva preso i primi due titoli di colonna. "
                "Attenzione: sono PNG umani, non mostri — vanno trattati come "
                "le altre voci razziali gia' escluse dal conteggio.",
    },
]

# Altre voci con lo stesso difetto, individuate dallo stesso segnale (due
# valori di FREQUENCY sulla stessa riga). Non erano fra le quattro segnalate
# ma hanno la stessa causa e vanno riverificate prima di convertirle.
SOSPETTE_STESSA_CAUSA = [
    {"estratto": "Emre Kingfisher", "frequency": "Rare Uncommon",
     "nota": "Probabile voce \"Avian\" con due varianti, Emre e Kingfisher."},
    {"estratto": "Unmated Mated pair*", "frequency": "Very rare Very rare",
     "nota": "Frammento della voce \"Dragon, Amphi\": due colonne per "
             "esemplare solitario e coppia. Gia' escluso dal conteggio come "
             "non-nome."},
]


def totale_creature():
    """Quante creature stanno dietro le quattro voci verificate."""
    return sum(len(v["creature"]) for v in VERIFICATE)
