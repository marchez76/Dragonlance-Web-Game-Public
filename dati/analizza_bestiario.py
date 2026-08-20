#!/usr/bin/env python3
"""
Genera dati/RAPPORTO-bestiario.md: diagnostica prima della conversione.

COSA E' E COSA NON E'
    Come RAPPORTO-classi.md per le classi: serve a vedere la forma del
    problema PRIMA di convertire. NON converte nulla, non tocca `dati/`,
    non propone statblock.

FONTI
    2e    MC - Dragonlance Appendix (TSR 1990), trascritto in _draconici.py
    5e    Shadow of the Dragon Queen (WotC 2022), Appendice B, idem
    SRD   SRD 5.1 CC-BY, sottoinsieme per GS in _fonti/srd51_mostri.py

REGOLA
    DERIVATO      ogni numero e ogni rapporto: calcolato dai dati.
    INTERPRETATIVO  letture, marcate e datate.

DUE USCITE
    RAPPORTO-bestiario.md            pubblico. Niente paragrafi di effetti
                                      alla morte, niente testo descrittivo di
                                      azioni/tratti SotDQ: parafrasati con
                                      riferimento di pagina.
    RAPPORTO-bestiario-completo.md   privato (escluso dal repo pubblico).
                                      Stesso documento, con il testo di
                                      fonte completo per riferimento interno.
    La riduzione e' una funzione del generatore (parametro `completo` di
    `scheda_confronto()`), non un intervento a posteriori: rigenerare non
    puo' piu' reintrodurre testo di fonte nel pubblico.

Uso:  python3 dati/analizza_bestiario.py
"""

import collections
import os
import sys
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "_fonti"))

import _bestiario_mc as BM
import _campi_2e as C27
import _draconici as D
import _nomi_verificati as NV
import confronta_mostri as CM
import srd51_mostri as SRD

OGGI = date.today().isoformat()


def mille(n):
    return f"{n:,}".replace(",", ".")


def interpretativo(testo):
    righe = testo.strip().split("\n")
    return (f"> **Lettura interpretativa** — registrata il {OGGI}. "
            f"Non e' derivata dai dati.\n>\n"
            + "\n".join(f"> {l}" if l else ">" for l in righe))


# ==========================================================================
# PARTE 1 — struttura della scheda 2e
# ==========================================================================
# (campo 2e, esempio, corrispettivo 5e, categoria)
# categoria: "diretto" | "conversione" | "assente"
CAMPI_2E = [
    ("CLIMATE/TERRAIN", "Any, but usually tropical/Forest, plain, urban",
     "`environment` (etichetta, nessun effetto meccanico)", "conversione"),
    ("FREQUENCY", "Uncommon", "—", "assente"),
    ("ORGANIZATION", "Band", "—", "assente"),
    ("ACTIVITY CYCLE", "Any", "—", "assente"),
    ("DIET", "Special", "—", "assente"),
    ("INTELLIGENCE", "Average (8-10)",
     "punteggio di Intelligenza singolo", "conversione"),
    ("TREASURE", "M, Q; (D, I, T)",
     "tabelle del tesoro della DMG, indicizzate per GS", "conversione"),
    ("ALIGNMENT", "Lawful or chaotic evil",
     "`alignment`, con la formula \"Typically\"", "diretto"),
    ("NO. APPEARING", "2-20", "—", "assente"),
    ("ARMOR CLASS", "4", "**Armor Class**, ma la scala si inverte", "conversione"),
    ("MOVEMENT", "6, Run 15, Glide 18", "**Speed** in piedi", "conversione"),
    ("HIT DICE", "2", "**Hit Points** con formula di dadi", "conversione"),
    ("THAC0", "19", "bonus di attacco per singolo attacco", "conversione"),
    ("NO. OF ATTACKS", "2 or 1", "**Multiattack** nelle azioni", "conversione"),
    ("DAMAGE/ATTACK", "1-4/1-4 or by weapon",
     "danno per attacco, con media stampata", "conversione"),
    ("SPECIAL ATTACKS", "Poison", "azioni e tratti", "conversione"),
    ("SPECIAL DEFENSES", "+2 bonus to saves",
     "resistenze, immunita', tiri salvezza competenti", "conversione"),
    ("MAGIC RESISTANCE", "20%", "—", "assente"),
    ("SIZE", "M (5' tall)", "**Size**, categoria", "diretto"),
    ("MORALE", "Elite (13)", "—", "assente"),
    ("XP VALUE", "175",
     "**Challenge**, con PE derivati dal GS e non viceversa", "conversione"),
]


def parte1():
    per_cat = collections.Counter(c[3] for c in CAMPI_2E)
    tab = "\n".join(
        f"| `{c[0]}` | {c[1]} | {c[2]} | "
        f"{ {'diretto': 'diretto', 'conversione': 'da convertire', 'assente': '**assente in 5e**'}[c[3]] } |"
        for c in CAMPI_2E)
    assenti = [c[0] for c in CAMPI_2E if c[3] == "assente"]
    return tab, per_cat, assenti


# ==========================================================================
# PARTE 2 — confronto puntuale
# ==========================================================================
def dpr_2e(nome):
    """Danno medio per round secondo la 2e, dalla riga DAMAGE/ATTACK."""
    tab = {"Baaz": 2 * 2.5, "Kapak": 2.5, "Bozak": 2 * 2.5,
           "Sivak": 3.5 + 3.5 + 7.0, "Aurak": 2 * 6.5}
    return tab[nome]


def dpr_5e(nome):
    """Danno medio per round dal Multiattacco ufficiale, opzione migliore."""
    tab = {"Baaz": 2 * 4, "Kapak": 2 * (5 + 7), "Bozak": 2 * 10,
           "Sivak": 2 * 13 + 8, "Aurak": 3 * 8}
    return tab[nome]


# Versione RIDOTTA delle azioni/tratti/nota di fonte, per il pubblico: solo
# valori numerici e riferimenti di pagina, mai il testo descrittivo di SotDQ
# o dell'MC Appendix (entrambi manuali protetti, SotDQ commerciale quanto il
# 2e). La versione completa resta disponibile via `completo=True`, privata.
AZIONI_RIDOTTE = {
    "Baaz": "Multiattack (due attacchi); Shortsword +3 a colpire, 4 (1d6+1) perforanti.",
    "Bozak": "Multiattack (Tridente ×2 o Scariche elettriche ×2); Trident +4 a "
             "colpire, 5 (1d6+2) perforanti (6, 1d8+2 a due mani); Lightning "
             "Discharge +4 a distanza, 60 ft, 10 (3d6) fulmine; Spellcasting "
             "CD 12, quattro incantesimi 1/giorno ciascuno.",
    "Kapak": "Multiattack (Pugnale ×2, con TS su Costituzione CD 12 o "
             "veleno+paralisi se entrambi colpiscono); Dagger +5 a colpire, "
             "5 (1d4+3) perforanti + 7 (2d6) veleno.",
    "Sivak": "Multiattack (Spada seghettata ×2 + Coda); Serrated Sword +6 a "
             "colpire, 13 (2d8+4) taglienti; Tail +6 a colpire, 8 (1d8+4) "
             "contundenti (TS Forza CD 14 o prono su bersagli Grandi o più "
             "piccoli); Shape Theft — reazione: illusione della forma "
             "dell'ucciso, dopo aver ucciso un Umanoide Medio o più piccolo.",
    "Aurak": "Multiattack (Squarcio + Raggio di energia, tre attacchi); Rend "
             "+5 a colpire, 8 (1d12+2) taglienti; Energy Ray +6 a distanza, "
             "60 ft, 8 (1d10+3) forza; Noxious Breath (ricarica 5-6, cono "
             "15 ft, TS Costituzione CD 14, 21/6d6 veleno + sfinimento); "
             "Spellcasting CD 14, incantesimi a volontà e a usi giornalieri.",
}
TRATTI_RIDOTTI = {
    "Baaz": "Controlled Fall (riduce i danni da caduta); Draconic Devotion "
            "(vantaggio ai tiri per colpire vicino a un drago non ostile).",
    "Bozak": "Glide (riduce i danni da caduta, sposta 2 ft orizzontali per "
             "ft di discesa).",
    "Kapak": "Glide (come il Bozak).",
    "Sivak": None,
    "Aurak": "Aura of Command: i draconici vicini resistono meglio a charme "
             "e paura (SotDQ pag. 196).",
}
ATTACCHI_RIGA_RIDOTTA = {
    "Baaz": "Due attacchi con Spada corta.",
    "Bozak": "Due attacchi (Tridente, o due Scariche elettriche a distanza).",
    "Kapak": "Due attacchi con Pugnale (veleno e paralisi se entrambi colpiscono).",
    "Sivak": "Due attacchi con Spada seghettata più uno di Coda.",
    "Aurak": "Tre attacchi fra Squarcio e Raggio di energia.",
}
NOTE_RIDOTTE = {
    "Baaz": "dalle uova di draghi d'ottone (MC Dragonlance Appendix, voce "
            "Draconian, Baaz).",
    "Bozak": "dalle uova di draghi di bronzo, incantatori (MC Dragonlance "
             "Appendix, voce Draconian, Bozak).",
    "Kapak": "dalle uova di draghi di rame, assassini con percentuali "
             "innate da ladro (MC Dragonlance Appendix, voce Draconian, "
             "Kapak).",
    "Sivak": "dalle uova di draghi d'argento, gli unici che volano davvero "
             "(MC Dragonlance Appendix, voce Draconian, Sivak).",
    "Aurak": "dalle uova di draghi d'oro, gli unici senza ali (MC "
             "Dragonlance Appendix, voce Draconian, Aurak).",
}


def scheda_confronto(n, completo=False):
    """completo=True include i paragrafi degli effetti alla morte e il
    testo descrittivo di azioni/tratti/nota di fonte, presi da _draconici.py
    (privato, trascrizione di MC Appendix e SotDQ). completo=False (uscita
    pubblica) li sostituisce con parafrasi e riferimenti di pagina."""
    a, b = D.DUE_E[n], D.CINQUE_E[n]
    r = [f"### {n} Draconian", ""]
    r += [
        "| | AD&D 2e (MC Appendix) | D&D 5e (SotDQ pag. "
        f"{b['pagina']}) |",
        "|---|---|---|",
        f"| taglia | {a['size']} | {b['size']} |",
        f"| classe armatura | **{a['ac']}** (scala discendente) | "
        f"**{b['ac']}** ({b['ac_from']}, scala ascendente) |",
        f"| resistenza | {a['hd']} DV | {b['hp']} PF ({b['hp_formula']}) |",
        f"| attacco | TAC0 {a['thac0']} | bonus di competenza +{b['pb']} |",
        f"| attacchi | {a['attacks']} — {a['damage']} | "
        f"{b['azioni'][0][1] if completo else ATTACCHI_RIGA_RIDOTTA[n]} |",
        f"| movimento | {a['movement']} | {b['speed']} |",
        f"| difese speciali | {a['special_defenses']} | "
        f"{b.get('extra', '—')} |",
        f"| resistenza magica | {a['magic_resistance']} | "
        f"**non esiste in 5e** |",
        f"| morale | {a['morale']} | **non esiste in 5e** |",
        f"| valore | {a['xp']:,} PE (formula 2e) | ".replace(",", ".")
        + f"Grado di Sfida **{b['cr']}** ({b['xp']:,} PE) |".replace(",", "."),
        "",
    ]
    if completo:
        r += [
            f"**Effetto alla morte — la firma del draconico.**", "",
            f"*2e*: {a['morte']}", "",
            f"*5e*: {[t for t in b['tratti'] if t[0] == 'Death Throes'][0][1]}", "",
            "**Azioni 5e**", "",
        ]
        for nome, testo in b["azioni"]:
            r.append(f"- **{nome}.** {testo}")
        for nome, testo in b.get("reazioni", []):
            r.append(f"- **{nome}** *(reazione)*. {testo}")
        r.append("")
        r += ["**Altri tratti 5e**", ""]
        for nome, testo in b["tratti"]:
            if nome != "Death Throes":
                r.append(f"- **{nome}.** {testo}")
        r.append("")
        r += [f"**Nota di fonte 2e**: {a['note']}", ""]
    else:
        r += [
            "**Effetto alla morte**: vedi \"Cosa l'ufficiale ha reso, "
            "scartato e aggiunto\" più sotto.", "",
            f"**Azioni 5e**: {AZIONI_RIDOTTE[n]}", "",
        ]
        if TRATTI_RIDOTTI[n]:
            r += [f"**Altri tratti 5e**: {TRATTI_RIDOTTI[n]}", ""]
        r += [f"**Nota di fonte 2e**: {NOTE_RIDOTTE[n]}", ""]
    return "\n".join(r)


# resa delle capacita' 2e: (nome, esito, come)
RESA = {
    "Baaz": [
        ("Trasformazione in pietra alla morte", "reso",
         "Diventa `Death Throes` con gas pietrificante e TS su Costituzione. "
         "La 5e aggiunge un effetto ad AREA che la 2e non aveva."),
        ("Arma conficcata nella statua (prova di Destrezza -3)", "scartato",
         "Era un effetto sull'equipaggiamento di chi uccideva. La 5e non ha "
         "regole per armi bloccate."),
        ("Due attacchi con artigli 1-4/1-4", "trasformato",
         "Diventano due attacchi con SPADA CORTA. Le armi naturali sono "
         "sostituite da armi manufatte."),
        ("Resistenza magica 20%", "scartato", "La 5e non ha resistenza magica."),
        ("Travestimento sotto vesti e cappucci", "scartato",
         "Restava nel testo descrittivo, non era meccanica nemmeno in 2e."),
        ("Movimento 6 / Corsa 15 / Planata 18", "trasformato",
         "Diventa velocita' 30 fissa piu' il tratto `Controlled Fall`."),
        ("—", "aggiunto",
         "`Draconic Devotion`: vantaggio ai tiri per colpire se vede un Drago "
         "non ostile. Non c'e' nulla di simile in 2e."),
    ],
    "Bozak": [
        ("Esplosione delle ossa alla morte, 1d6 entro 10 piedi, nessun TS",
         "reso", "Diventa 2d8 danni da forza con TS su Destrezza CD 10. "
                 "Danno quasi triplicato, ma con tiro salvezza."),
        ("Avvizzimento in un round, esplosione il round dopo", "scartato",
         "I due tempi diventano istantanei: la 5e non ha effetti alla morte "
         "differiti."),
        ("Incantesimi da mago (7 nomi)", "reso in parte",
         "Restano enlarge/reduce, invisibility, stinking cloud, web. Spariscono "
         "burning hands, magic missile, shocking grasp, sostituiti da "
         "`Lightning Discharge` come attacco a distanza."),
        ("Volo Fl 6 (E)", "scartato",
         "Il volo vero e' tolto: resta solo `Glide`."),
        ("+2 ai tiri salvezza", "trasformato",
         "Diventano competenze in TS di Intelligenza, Saggezza e Carisma."),
        ("Resistenza magica 20%", "scartato", "Come sopra."),
    ],
    "Kapak": [
        ("Dissoluzione in pozza d'acido alla morte, 1d8/round, nessun TS",
         "reso", "Diventa acido addosso alle creature entro 5 piedi, 2d6 per "
                 "turno per 1 minuto, con TS su Destrezza CD 12 e possibilita' "
                 "di ripulirsi con un'azione."),
        ("L'acido distrugge tesoro e oggetti magici del Kapak", "scartato",
         "Era la penalita' che rendeva rischioso ucciderlo. Sparita."),
        ("Veleno come attacco speciale (saliva)", "reso",
         "Diventa 2d6 danni da veleno su ogni pugnale, piu' paralisi se "
         "entrambi gli attacchi colpiscono."),
        ("Abilita' da ladro a percentuale (15%/10%/20%)", "trasformato",
         "Diventano Furtivita' +7, Inganno +4, Percezione +3."),
        ("UN attacco per round, 1-4 danni", "trasformato",
         "Diventano DUE attacchi con pugnale. E' il cambiamento piu' grosso "
         "del roster."),
        ("—", "aggiunto",
         "Velocita' di scalata 40 piedi e immunita' ai danni da veleno: in 2e "
         "non c'erano."),
    ],
    "Sivak": [
        ("Assume la forma dell'uccisore per TRE GIORNI, poi fuliggine",
         "reso in parte",
         "Diventa un'immagine spettrale urlante che dura UN MINUTO e spaventa. "
         "Da inganno a lungo termine diventa effetto di paura tattico."),
        ("Se l'uccisore non e' umanoide, prende fuoco: 2d4 danni", "scartato",
         "Il ramo alternativo dell'effetto sparisce; resta solo la condizione "
         "sulla taglia."),
        ("Mutaforma permanente uccidendo un umanoide", "reso",
         "Diventa `Shape Theft` come REAZIONE, illusione che dura finche' "
         "il draconico muore o la termina."),
        ("Tre attacchi 1-6/1-6/2-12", "trasformato",
         "Diventano due spade seghettate piu' una coda che puo' far cadere "
         "proni. Il terzo attacco piu' forte diventa l'attacco di coda."),
        ("Volo Fl 24 (C)", "reso", "Diventa velocita' di volo 60 piedi. "
                                   "E' l'unico draconico che vola davvero in "
                                   "entrambe le edizioni."),
        ("Resistenza magica 20%, +2 ai TS", "trasformato",
         "Restano solo competenze in TS di Forza e Saggezza."),
    ],
    "Aurak": [
        ("Sfera di fulmini per 3 round, poi esplosione 3d6 senza TS",
         "reso in parte",
         "Diventa istantaneo: sfera che rimbalza su tre bersagli, 2d8 con TS su "
         "Destrezza CD 14 e stordimento. Sparisce la fase di tre round in cui "
         "l'Aurak morto continuava ad attaccare come mostro da 13 DV."),
        ("Invisibilita' a volonta'", "reso",
         "Resta come incantesimo `invisibility` a volonta'."),
        ("Polymorph self e change self 3/giorno", "reso in parte",
         "Resta solo `disguise self` 2/giorno."),
        ("Dimension door 3/giorno", "reso", "Diventa 2/giorno."),
        ("Vede attraverso ogni illusione, individua invisibili entro 40 piedi",
         "trasformato", "Diventa `truesight` 60 piedi, che e' piu' forte e piu' "
                        "semplice."),
        ("Soffio (SPECIAL ATTACKS: spells and breath, senza dettagli)", "reso",
         "Diventa `Noxious Breath`, cono di 15 piedi, 6d6 veleno piu' un "
         "livello di sfinimento. La 2e non ne dava i numeri: qui l'ufficiale "
         "ha INVENTATO, non convertito."),
        ("Resistenza magica 30%, +4 ai TS", "trasformato",
         "Diventano tre TS competenti e immunita' alla condizione affascinato."),
        ("—", "aggiunto",
         "`Aura of Command`: aura di comando sugli altri draconici. In 2e "
         "l'Aurak era un comandante nel testo, non nelle regole."),
    ],
}


# ==========================================================================
# PARTE 4 — analogie SRD
# ==========================================================================
ANALOGIE = {
    "Baaz": ("1/2", ["Lizardfolk", "Gnoll", "Hobgoblin", "Orc"],
             "fante di prima linea, in gruppo"),
    "Bozak": ("2", ["Cult Fanatic", "Gargoyle", "Berserker"],
              "incantatore di supporto in mischia"),
    "Kapak": ("3", ["Doppelganger", "Veteran", "Werewolf"],
              "assassino furtivo con veleno"),
    "Sivak": ("4", ["Ettin", "Chuul", "Succubus/Incubus"],
              "bruto Grande volante, truppa d'assalto"),
    "Aurak": ("6", ["Mage", "Medusa", "Drider"],
              "comandante incantatore"),
}


# ==========================================================================
# PARTE 5 — ordine di lavorazione proposto, sull'elenco delle creature da
# convertire (BM.statistiche()['da_convertire'], MAI un numero scritto qui:
# si sfaserebbe di nuovo, come e' gia' successo due volte).
# ==========================================================================
# I cinque draconici NON sono in questa lista: hanno gia' un precedente
# ufficiale completo, analizzato nelle parti 2-4.
#
# (nome, fascia, motivo, analogo SRD evidente?, n_creature nella voce)
#
# RICOSTRUITA dopo la rilettura di tutte le 62 voci sui blocchi statistiche
# reali (Dadi Vita, CA, THAC0, resistenze, PE), non sui nomi. La versione
# precedente era stata costruita per pattern-matching sul nome della voce
# prima di leggere lo statblock: ha funzionato per la maggior parte delle
# voci ma ha sbagliato platealmente su alcune. Il dettaglio di cosa si e'
# spostato e perche' e' nell'interpretativo subito sotto la tabella.
#
# Traag, Warrior Skeleton, Thanoi, Kyrie, Ogre (of Krynn), Orughi, Horax,
# Bear Ice, Fetch, Shadowperson (e il suo Revered Ancient One), Eyewing non
# sono piu' in questa lista: sono gia' stati convertiti (dati/mostri/traag.json,
# dati/mostri/scheletro-guerriero.json, dati/mostri/thanoi.json,
# dati/mostri/kyrie.json, dati/mostri/ogre-krynn.json,
# dati/mostri/orughi.json, dati/mostri/horax.json,
# dati/mostri/orso-glaciale.json, dati/mostri/fetch.json,
# dati/mostri/shadowperson.json,
# dati/mostri/anziano-venerato-ombrolo.json,
# dati/mostri/eyewing.json) — la prima fascia e' completa e
# la seconda e' a buon punto, coi due casi col riscontro 3.5 fatti con calma.
# I cinque draconici veri restano fuori come prima.

# ==========================================================================
# QUINTO SEGNALE — "See below" nei campi di combattimento delle 48 voci
# "creatura" dell'Appendice (BM.VOCI, categoria creatura). Trovato cercando
# la stringa su tutto il testo estratto e filtrando ai soli campi di
# combattimento (esclusi TREASURE/NO. APPEARING quando sono dati di mondo,
# gruppo A della decisione 27 — l'unica eccezione e' Haunt/Knight, dove
# TREASURE stesso resta "See below" e viene contato perche' non c'e' un
# valore alternativo dichiarato altrove).
#
# (voce, fascia_attuale o None se fuori fascia, [campi con "See below"])
# fascia_attuale e' la fascia della SOTTO-CREATURA flaggata, non
# necessariamente quella dell'intera voce quando la voce ne contiene piu'
# di una (es. Stag: solo il Cervo Bianco e' flaggato, fuori fascia; Insect
# Swarm: entrambe le colonne lo sono, riportata alla fascia piu' bassa delle
# due — la Velvet Ant, fascia 3, e' annotata a parte nel testo).
# ==========================================================================
SEGNALE_5 = [
    ("Anemone, Giant", 5,
     ["TREASURE", "NO. OF ATTACKS", "DAMAGE/ATTACK", "SPECIAL ATTACKS",
      "SPECIAL DEFENSES"]),
    ("Bear, Ice", 2, ["SPECIAL DEFENSES"]),
    ("Beast, Undead", 5, ["SPECIAL DEFENSES"]),
    ("Centaur (of Krynn)", 2, ["SPECIAL DEFENSES"]),
    ("Dreamshadow", 3, ["MAGIC RESISTANCE"]),
    ("Dreamwraith", 3, ["MAGIC RESISTANCE"]),
    ("Eyewing", 2, ["SPECIAL DEFENSES"]),
    ("Fireshadow", 5, ["SPECIAL ATTACKS"]),
    ("Haunt, Knight", 3, ["TREASURE"]),
    ("Imp, Blood Sea", 3, ["MAGIC RESISTANCE"]),
    ("Insect Swarm", 2,
     ["NO. APPEARING", "HIT DICE", "THAC0", "DAMAGE/ATTACK", "SIZE",
      "XP VALUE"]),
    ("Kalothagh (Prickleback)", 4, ["SPECIAL DEFENSES"]),
    ("Knight, Death", 3,
     ["SPECIAL ATTACKS", "SPECIAL DEFENSES", "MAGIC RESISTANCE"]),
    ("Lizard Man (of Krynn)", 2, ["SPECIAL DEFENSES"]),
    ("Shadowperson", 2, ["SPECIAL ATTACKS", "SPECIAL DEFENSES"]),
    ("Spectral Minion", 3, ["SPECIAL ATTACKS"]),
    ("Stag", None, ["SPECIAL DEFENSES"]),
    ("Warrior, Skeleton", 1, ["SPECIAL ATTACKS", "SPECIAL DEFENSES"]),
    ("Wichtlin", 3, ["DAMAGE/ATTACK", "SPECIAL ATTACKS", "MAGIC RESISTANCE"]),
]

PRIORITA = [
    ("Centaur (of Krynn)", 2,
     "Trovata il 20 agosto 2026 (compito 1, verifica Half-Ogre/Centaur): "
     "4 DV, CA 5, nessuna resistenza fuori scala — profilo base pulito di "
     "fascia bassa-media, come Thanoi. Quattro sotto-specie nominate "
     "(Abanasinian, Crystalmir, Endscape, Wendle) con differenze di "
     "comportamento non ancora estratte per intero: la conversione base "
     "puo' partire dal profilo generico, le sotto-specie vanno lette a "
     "parte. CONFERMATA dal quinto segnale (20 agosto 2026): SPECIAL "
     "DEFENSES \"See below\" si risolve nel +2 ai tiri salvezza degli "
     "Abanasiniani (\"extremely robust\"), gia' anticipato come dettaglio "
     "di sotto-specie da estrarre in sede di conversione — nessuna "
     "sorpresa, segnale confermato ma causa gia' nota.",
     "sì — Centaur SRD", 4),
    ("Skrit", 3,
     "CORRETTA dopo lettura del testo completo (20 agosto 2026): la prima "
     "rilettura l'aveva confermata in seconda fascia guardando solo i DV "
     "(6) e la CA (3), lo stesso errore che il metodo aveva gia' imparato a "
     "evitare sullo Scheletro Guerriero. Il testo pieno rivela XP 2.000 (non "
     "da riempitivo) e un attacco velenoso in due fasi che nessun header "
     "riassume: paralisi con TS su veleno ogni round di aggancio (penalita' "
     "-1 cumulativa), poi dissoluzione dei tessuti (10 PF/ora) curabile "
     "SOLO con rigenerazione o guarigione naturale, non con magia curativa "
     "normale. Identitaria e costosa da rendere fedelmente, non un "
     "riempitivo pulito.",
     "parziale — nessun mostro SRD replica la dissoluzione curabile solo per rigenerazione", 1),
    ("Avian (Emre, Kingfisher, Skyfisher, 'Wari)", 2,
     "Quattro varianti sotto una sola voce: uccelli o umanoidi alati "
     "acquatici di Krynn. Le due lette (Emre 3 DV, Kingfisher 1 DV) sono "
     "di fascia bassa pulita; Skyfisher e 'Wari restano da verificare "
     "sull'immagine di pagina (colonne perse dall'estrazione).",
     "sì per le due note — probabile Hawk / Giant Owl", 4),
    ("Stag (Wild Stag, Giant Stag)", 2,
     "I due cervi normali della voce Stag: 3 e 5 DV, bestie da branco "
     "pulite. Il terzo abitante della voce, il Cervo Bianco, e' trattato a "
     "parte, fuori fascia — vedi sotto.", "sì — Elk / Giant Elk", 2),
    ("Lizard Man (Jarak-Sinn, Bakali)", 2,
     "Umanoidi rettili tribali, fascia bassa-media pulita: i jarak-sinn "
     "(piu' numerosi, 2+1 DV) e i bakali (2+1 DV), loro progenitori piu' "
     "rari. Voce nuova, trovata nella seconda passata. Il quinto segnale "
     "(20 agosto 2026) trova SPECIAL DEFENSES \"See below\" su ENTRAMBE le "
     "colonne, mai controllato prima (la coerenza precedente era solo "
     "sugli XP): per i jarak-sinn e' la coda distaccabile a volonta' "
     "(chi la afferra resta con la coda mentre il jarak-sinn fugge; "
     "ricresce in 1d4+8 settimane) — un meccanismo di fuga che il "
     "Lizardfolk SRD non replica; per i bakali e' una VULNERABILITA' al "
     "freddo (1 danno extra per dado da attacchi a base di freddo) piu' "
     "una membrana nittitante (+1 ai TS contro accecamento). Fascia "
     "confermata bassa-media (XP 270/175 restano modesti), ma la "
     "conversione dovra' rendere questi tre dettagli invece di limitarsi "
     "al Lizardfolk di peso.", "sì — Lizardfolk", 2),
    ("Phaethon", 2,
     "Umanoide alato dei monti, 4 DV, nessuna resistenza: GS basso-medio "
     "confermato, alternativa a Kyrie come avversario volante. Voce nuova.",
     "parziale — nessun analogo diretto SRD", 1),
    ("Insect Swarm, Grasshopper and Locust", 2,
     "Sciame di insetti, minaccia bassa per individuo, utile come "
     "ostacolo/ambientazione in arena. Voce nuova.", "sì — Swarm of Insects", 1),
    ("Disir", 2,
     "5 DV, tre attacchi (2d4/2d4/2d6, danno non banale) e resistenza al "
     "fuoco: spostata dalla quarta fascia, e' un fante bestiale pulito, non "
     "una curiosita' di nicchia.", "parziale — Bugbear / Lizardfolk potenziato", 1),
    ("Gurik Cha-ahl", 2,
     "2 DV, statistiche modeste: spostata dalla quarta fascia, e' un "
     "riempitivo bassissimo, non una curiosita'.", "no", 1),
    ("Kani Doll", 2,
     "2 DV, CA 10 (nessuna protezione), costrutto che non controlla mai il "
     "morale: spostata dalla quarta fascia, filler bassissimo.",
     "parziale — Homunculus", 1),

    ("Dreamshadow", 3,
     "STRUTTURALMENTE DIVERSA DALLE ALTRE: ogni campo della scheda 2e "
     "(CA, DV, THAC0, danno, taglia...) e' dichiarato \"as creature or "
     "person mimicked\" — non ha statistiche proprie, le eredita da chi "
     "imita. Non si converte come le altre 60: serve un mostro-modello "
     "(un pacchetto di regole che copia il bersaglio) piu' che uno "
     "statblock fisso.", "no — richiede un modello diverso, non un analogo", 1),
    ("Dreamwraith", 3,
     "8 DV, statistiche proprie fisse (a differenza del Dreamshadow "
     "gemello): fascia media confermata.", "no", 1),
    ("Fire Minion", 3,
     "6 DV, immunita' al fuoco: fascia media confermata, l'analogo proposto "
     "resta debole rispetto ai DV reali.", "parziale — Magmin, sottodimensionato", 1),
    ("Tylor", 3,
     "STRUTTURALMENTE COMPLESSA: la fonte da' una tabella di 6 categorie "
     "d'eta' con DV, CA e soffio diversi per ciascuna (da 1d6 DV/CA4 a "
     "5d10 DV/CA-1), sullo stesso modello degli age category dei draghi. "
     "Serve piu' di un GS, non uno: da trattare come una mini-famiglia "
     "di statblock imparentati, non una singola conversione.",
     "parziale — Chimera, solo per la categoria piu' alta", 1),
    ("Knight, Death", 3,
     "**Il Cavaliere della Morte**. CORREZIONE dopo la rilettura: la fonte "
     "descrive un TIPO ripetibile (\"a Knight of Solamnia, cursed by the "
     "gods...\"), non un individuo nominato — coerente con la decisione 32 "
     "(criterio: nome proprio e storia, non vincolo a un oggetto). "
     "\"E' Lord Soth\" era un'identificazione della sessione precedente, non "
     "un dato della voce: la fonte non nomina Soth. Va convertito come "
     "CREATURA al suo grado reale (9 DV, 75% di resistenza magica — la "
     "seconda piu' alta del bestiario dopo il 90% dello Scheletro "
     "Guerriero, correzione al primato che il rapporto attribuiva "
     "erroneamente allo Yaggol), non trattato come scheda unica di Soth. "
     "SotDQ ha lo statblock di Soth come PERSONAGGIO specifico: resta "
     "un riferimento per un'istanza particolarmente potente dello stesso "
     "tipo, non la fonte di questa conversione.",
     "parziale — stesso profilo dello Scheletro Guerriero: guardiano "
     "d'elite a offesa singola", 1),
    ("Haunt, Knight", 3,
     "8 DV, CA \"2 o migliore\" (molto protetta), non scacciabile dai "
     "chierici Legali Buoni: fascia media-alta confermata, coerente con la "
     "collocazione precedente.", "no", 1),
    ("Phaethon, Elder", 3,
     "Variante piu' forte del Phaethon base (6 DV contro 4), con un "
     "accenno di resistenza magica (5%): identitario, da comporre insieme "
     "al Phaethon. Voce nuova.", "no", 1),
    ("Insect Swarm, Velvet Ant", 3,
     "Sciame con veleno e formula di dimensione variabile: meccanica piu' "
     "complessa del semplice sciame. Voce nuova.",
     "parziale — Swarm of Insects, senza il veleno", 1),
    ("Yaggol", 3,
     "Sotto-razza degenerata dei mind flayer, con kit complesso (sei "
     "attacchi piu' un potere psichico). CORREZIONE: 50% di resistenza "
     "magica NON e' la piu' alta del bestiario come diceva il rapporto — "
     "lo Scheletro Guerriero ne ha 90%, il Cavaliere della Morte 75%. "
     "Resta comunque identitario e costoso: nessun mostro SRD a GS 1/4-4 "
     "replica un mind-flayer minore.",
     "no — Mind Flayer vero e' GS 7, fuori target", 1),
    ("Tayling (+ Taylang)", 3,
     "Gemelli telepatici che nascono sempre in coppia: l'intelligente "
     "(Tayling, 4 DV) e il bestiale (Taylang, 8 DV — fascia media, non "
     "bassa: attenzione a non sottostimarlo convertendo la coppia). "
     "Nessun analogo SRD replica il legame telepatico.", "no", 2),
    ("Spectral Minion", 3,
     "SPOSTATA dalla seconda fascia: Dadi Vita \"Varies\", colpibile solo "
     "da armi +1 o migliori, 20% di resistenza magica, e SEI varianti "
     "nominate con valori di PE diversi (Philosopher/Reveler/Searcher a "
     "975, Guardian/Warrior/Berserker a 1.400) sotto un'unica voce: piu' "
     "vicina a una famiglia di sotto-tipi che a un singolo riempitivo.",
     "sì per il profilo generale — Specter", 1),
    ("Wyndlass", 3,
     "SPOSTATA dalla quarta fascia (\"nicchia\") dopo la rilettura: 12 DV, "
     "THAC0 9 (molto buono), UNDICI attacchi (dieci tentacoli piu' morso, "
     "danno 1-10 per tentacolo) e 5.000 PE — nello stesso ordine di "
     "grandezza del Cavaliere della Morte e dello Scheletro Guerriero, non "
     "una curiosita' acquatica di basso profilo.",
     "parziale — Hydra per il numero di attacchi, ma senza rigenerazione", 1),
    ("Wichtlin", 3,
     "SPOSTATA dalla seconda fascia dopo lettura completa (quinto segnale, "
     "20 agosto 2026: DAMAGE/ATTACK, SPECIAL ATTACKS e MAGIC RESISTANCE "
     "tutti \"See below\"). Non e' un riempitivo: elfo non morto con due "
     "attacchi di contatto distinti (mano sinistra paralizza 2d4 round, "
     "mano destra avvelena per 2d6), immune a veleno/paralisi/sonno/"
     "charme/hold/incantesimi da freddo, colpibile solo da armi magiche "
     "+1, danneggiato dall'acqua santa (2d4/fiala), turnabile come "
     "spettro. Se era un incantatore in vita, lancia a meta' livello. Un "
     "elfo ucciso da un wichtlin diventa un wichtlin in sette giorni se "
     "non resuscitato: e' un effetto di CONTAGIO, non solo un mostro "
     "singolo. Include una variante montata (\"Wichtlin Wild Stag\") con "
     "meccanica di paralisi propria. Identitaria e costosa quanto lo "
     "Skrit, non un riempitivo di seconda fascia.",
     "parziale — Specter per il profilo generale, nessuno replica il "
     "contagio ne' il doppio tocco paralisi/veleno", 1),
    ("Imp, Blood Sea", 3,
     "SPOSTATA dalla quarta fascia (\"nicchia\") dopo lettura completa "
     "(quinto segnale, 20 agosto 2026: MAGIC RESISTANCE \"See below\", "
     "che non si risolve in una percentuale ma nell'elenco di immunita' "
     "sotto): 5+3 DV, polimorfismo a volonta' fra forma fisica (CA 4, "
     "tocco gelido 1d6) e forma di nebbia (CA 1, vola, ma solo 1 punto di "
     "danno da contatto e nessuna azione fisica), colpibile solo da armi "
     "magiche, immune a sonno/charme/incantesimi da freddo/paralisi/"
     "veleno, 10% di possibilita' di generare una copia di se stesso se "
     "colpito da un fulmine. La fascia \"nicchia\" descriveva "
     "l'ambientazione (il Mare di Sangue), non la meccanica: stesso "
     "equivoco gia' corretto su Bear Ice/Disir/Eyewing nella direzione "
     "opposta, qui va nella direzione di un identitario vero, non di un "
     "riempitivo.",
     "parziale — Imp/Quasit per il polimorfismo, ma nessuno replica la "
     "scissione da fulmine", 1),

    ("Shimmerweed", 4,
     "1 punto ferita, immobile, un solo attacco (confusione): a malapena "
     "una creatura da combattimento, piu' vicina a un ostacolo ambientale "
     "che a un avversario. Resta di nicchia per questo, non perche' sia "
     "debole in senso convenzionale.", "parziale — Shrieker", 1),
    ("Kalothagh (Prickleback)", 4, "4+4 DV, attacco a distanza con aculei: bestia acquatica di nicchia.", "sì — Reef Shark", 1),
    ("Hatori, Lesser", 4,
     "Predatore del deserto a Dadi Vita variabili (1-5): complesso da "
     "fissare a un singolo GS, ma il taglio piu' basso rientra nel target.",
     "no", 1),
    ("Spider, Giant Trap Door", 4,
     "Ragno imboscatore di taglia Large, 4+4 DV: sopra la fascia bassa ma non "
     "enorme. Voce nuova, trovata nella seconda passata.", "parziale — Giant Spider", 1),

    ("Dragon, Amphi", 5, "Drago: la Fase 2 non ne ha bisogno.", "sì — draghi SRD", 1),
    ("Dragon, Kodragon", 5, "Come sopra.", "sì", 1),
    ("Dragon, Sea", 5, "Come sopra.", "sì", 1),
    ("Dragon, Astral", 5,
     "Drago, come sopra. Due statblock nella voce (solitario e coppia "
     "accoppiata da 35 DV) ma una sola specie in due stati: contata come "
     "una riga, non due.", "sì", 1),
    ("Hatori, Greater", 5,
     "Variante adulta dell'Hatori, 6-20 DV: fuori target quanto un drago, "
     "serve oltre la Fase 2. Voce nuova.", "no", 1),
    ("Beast, Undead (Stahnk, Gholor)", 5,
     "24 Dadi Vita ciascuno (12+12): fuori target quanto un drago. Voce "
     "nuova, trovata nella seconda passata — mancava del tutto dal "
     "ricontaggio precedente.", "no", 2),
    ("Spider, Whisper", 5,
     "16 Dadi Vita (8+8): fuori target quanto un drago. Voce nuova.", "no", 1),
    ("Anemone, Giant", 5,
     "SPOSTATA dalla quarta fascia (\"nicchia\"): 16 Dadi Vita, THAC0 5 "
     "(fra i migliori del bestiario) e 12.000 PE — piu' del doppio "
     "dell'Aurak Draconian (6.000, GS 6), il piu' potente dei cinque "
     "ufficiali. \"Bestia acquatica\" descriveva l'ambiente, non la "
     "potenza: e' una delle creature piu' forti dell'intero bestiario.",
     "no — fuori target quanto un drago", 1),
    ("Fireshadow", 5,
     "SPOSTATA dalla terza fascia: 13+3 Dadi Vita (circa 16, la stessa "
     "soglia dei draghi e degli altri fuori-target), Gargantuan da 30 "
     "piedi, evocabile solo da un chierico malvagio di 8° livello o "
     "superiore, 11.000 PE — secondo valore piu' alto del bestiario dopo "
     "l'Anemone Gigante. Non e' un \"identitario da comporre\" a fascia "
     "media, e' fuori target quanto un drago.",
     "no — fuori target", 1),
]

# Fuori dalle cinque fasce di combattimento: non e' materiale da arena.
FUORI_FASCIA = [
    ("The White Stag", "Il terzo abitante della voce Stag (pag. 78). Non è "
     "una bestia: è unico, allineamento legale buono, 2.000 PE, con "
     "capacità magiche — una creatura sacra da incontro narrativo, non un "
     "avversario. Proposta: schedarlo quando esiste uno schema per "
     "creature uniche/da avventura (vicino allo schema Personaggio), non "
     "forzarlo nel bestiario da combattimento."),
]

# Le voci razziali dell'MC Appendix (razza_nostra + razza_altra): NON sono
# mostri da convertire. Derivata da BM invece che ricopiata a mano, per non
# sfasarsi di nuovo come il resto del bestiario: era ferma a 16 voci con due
# nomi corrotti (Blood Sea Minotaur, Emre Kingfisher) mai aggiornati dopo il
# ricontaggio.
VOCI_RAZZIALI = [v[1] for v in BM.VOCI if v[3] in ("razza_nostra", "razza_altra")]


def main():
    tab1, cat1, assenti = parte1()
    mc = CM.mostri_mc()
    sot = CM.mostri_sotdq()
    kmc = {CM.chiave(x): x for x in mc}
    ks = {CM.chiave(x): x for x in sot}
    solo_mc = [kmc[k] for k in sorted(set(kmc) - set(ks))]

    # --- rapporti derivati ---
    righe_num = []
    for n in D.ORDINE_5E:
        a, b = D.DUE_E[n], D.CINQUE_E[n]
        righe_num.append(
            f"| {n} | {a['hd']} | {b['hp']} | {b['hp']/a['hd']:.1f} | "
            f"{a['ac']} | {b['ac']} | {a['thac0']} | {b['cr']} | "
            f"{D.cr_num(b['cr']) - a['hd']:+.1f} | {a['xp']:,} | {b['xp']:,} |"
            .replace(",", "."))
    rapporti = [D.CINQUE_E[n]["hp"] / D.DUE_E[n]["hd"] for n in D.ORDINE_5E]
    diff_cr = [D.cr_num(D.CINQUE_E[n]["cr"]) - D.DUE_E[n]["hd"]
               for n in D.ORDINE_5E]
    dpr = [(n, dpr_2e(n), dpr_5e(n), dpr_5e(n) / dpr_2e(n))
           for n in D.ORDINE_5E]

    blocchi_resa = "\n".join(
        f"### {n}\n\n| capacità 2e | esito | come |\n|---|---|---|\n"
        + "\n".join(f"| {c} | **{e}** | {come} |" for c, e, come in RESA[n])
        + "\n"
        for n in D.ORDINE_5E)

    # Tabella dei nomi corrotti: UNA fonte sola, _bestiario_mc.NOMI_CORRETTI
    # incrociato con VOCI per pagina e causa. Prima c'erano due elenchi
    # indipendenti (questo e NV.VERIFICATE, fermo a 4 voci su 8) che si sono
    # sfasati: la causa dell'incoerenza 2, risolta unificando la fonte.
    voce_per_nome = {v[1]: v for v in BM.VOCI}
    causa_extra = {v["estratto"]: v["causa"] for v in NV.VERIFICATE}
    tab_nomi = "\n".join(
        f"| `{estratto}` | **{corretto}**"
        + (f" (+{len(voce_per_nome[corretto][2]) - 1} varianti)"
           if len(voce_per_nome[corretto][2]) > 1 else "")
        + f" | {voce_per_nome[corretto][0]} | "
        + f"{causa_extra.get(estratto) or voce_per_nome[corretto][5]} |"
        for estratto, corretto in sorted(BM.NOMI_CORRETTI.items(),
                                          key=lambda kv: voce_per_nome[kv[1]][0]))
    n_creature_multi = sum(len(v[2]) for v in BM.VOCI if len(v[2]) > 1)

    NOMI_G = {"A": "dati di mondo", "B": "morale", "C": "resistenza magica"}
    tab_27 = "\n".join(
        f"| **{k}** — {NOMI_G[k]} | {len(g['campi'])} | {g['esito']} | "
        f"{'`' + g['destinazione'] + '`, Fase ' + str(g['fase']) if g['destinazione'] else 'da decidere in Fase ' + str(g['fase'])} |"
        for k, g in C27.GRUPPI)

    _bs = BM.statistiche()
    BS = {"voci": _bs["voci"], "creature": _bs["creature"],
          "n_multi": _bs["n_multi"], "nomi_sbagliati": _bs["nomi_sbagliati"],
          "da_convertire": _bs["da_convertire"],
          "razza_nostra": _bs["per_cat"]["razza_nostra"]["voci"],
          "razza_altra": _bs["per_cat"]["razza_altra"]["voci"]}
    tab_multi = "\n".join(
        f"| **{n}** | {p} | {len(c)} — {', '.join(c)} |"
        for p, n, c, _ in _bs["multi"])

    # --- quinto segnale: conteggio derivato da SEGNALE_5, mai scritto a mano
    n_voci_creatura = len([v for v in BM.VOCI if v[3] == "creatura"])
    n_flag = len(SEGNALE_5)
    quota_flag = round(100 * n_flag / n_voci_creatura)
    per_fascia_5 = collections.Counter(f for _, f, _ in SEGNALE_5)
    NOMI_FASCIA_5 = {1: "prima", 2: "seconda", 3: "terza", 4: "quarta",
                     5: "quinta", None: "fuori fascia"}
    dist_5 = ", ".join(
        f"{per_fascia_5[f]} in {NOMI_FASCIA_5[f]}"
        for f in [1, 2, 3, 4, 5, None] if per_fascia_5[f])
    n_basse_medie = per_fascia_5[2] + per_fascia_5[3]
    quota_basse_medie = round(100 * n_basse_medie / n_flag)
    tab_segnale_5 = "\n".join(
        f"| {v} | {NOMI_FASCIA_5[f]} | {', '.join('`' + c + '`' for c in campi)} |"
        for v, f, campi in SEGNALE_5)

    tab_srd = []
    for n in D.ORDINE_5E:
        gs, analoghi, ruolo = ANALOGIE[n]
        st = SRD.statistiche(gs)
        b = D.CINQUE_E[n]
        tab_srd.append(
            f"| {n} | {gs} | {ruolo} | {b['ac']} / {b['hp']} | "
            f"{st['ca_med']} / {st['pf_med']} | {', '.join(analoghi)} |")

    # --- il profilo difensivo contro la mediana del proprio grado ---------
    prof = []
    for n in D.ORDINE_5E:
        b = D.CINQUE_E[n]
        st = SRD.statistiche(b["cr"])
        quota = 100 * b["hp"] / st["pf_med"]
        prof.append((n, b["cr"], b["hp"], st["pf_med"], quota,
                     dpr_5e(n), dpr_5e(n) / dpr_2e(n)))
    tab_prof = "\n".join(
        f"| {n} | {gs} | {pf} | {med} | {q:.0f}% | {d:.0f} | ×{r:.1f} |"
        for n, gs, pf, med, q, d, r in prof)
    kapak = [p for p in prof if p[0] == "Kapak"][0]

    per_fascia = collections.defaultdict(list)
    for nome, f, motivo, an, nc in PRIORITA:
        per_fascia[f].append((nome, motivo, an, nc))
    NOMI_FASCIA = {1: "Prima — servono subito all'arena",
                   2: "Seconda — riempitivi di fascia bassa e media",
                   3: "Terza — identitari ma senza analogo pulito",
                   4: "Quarta — nicchia",
                   5: "Quinta — fuori target (draghi e alti Dadi Vita), non servono alla Fase 2"}
    blocchi_prio = []
    tot_righe = tot_creature = 0
    for f in sorted(per_fascia):
        righe_f = per_fascia[f]
        creature_f = sum(nc for _, _, _, nc in righe_f)
        tot_righe += len(righe_f)
        tot_creature += creature_f
        etichetta = (f"{len(righe_f)} voci, {creature_f} creature" if creature_f != len(righe_f)
                     else f"{len(righe_f)}")
        blocchi_prio.append(f"### {NOMI_FASCIA[f]} ({etichetta})\n")
        blocchi_prio.append("| creatura | perché | analogo SRD |\n|---|---|---|")
        for nome, motivo, an, nc in righe_f:
            blocchi_prio.append(f"| {nome} | {motivo} | {an} |")
        blocchi_prio.append("")
    blocchi_prio.append(
        f"### Fuori fascia — non da arena ({len(FUORI_FASCIA)})\n")
    for nome, motivo in FUORI_FASCIA:
        blocchi_prio.append(f"**{nome}.** {motivo}\n")

    USCITE = [(False, os.path.join(BASE, "RAPPORTO-bestiario.md")),
              (True, os.path.join(BASE, "RAPPORTO-bestiario-completo.md"))]
    for completo, out in USCITE:
      doc = f"""# Il bestiario di Krynn — diagnostica

*Generato da `dati/analizza_bestiario.py` il {OGGI}.*

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
{tab1}

**{cat1['diretto']} campi diretti, {cat1['conversione']} da convertire, {cat1['assente']} senza alcun corrispettivo in 5e.**

I {cat1['assente']} senza corrispettivo: {', '.join('`' + x + '`' for x in assenti)}.

{interpretativo(f'''Un terzo abbondante della scheda 2e — {cat1['assente']} campi su {len(CAMPI_2E)} — non ha dove andare.
Ma le due metà del problema non si somigliano.

`FREQUENCY`, `NO. APPEARING`, `ORGANIZATION` e `ACTIVITY CYCLE` servivano al
Dungeon Master per popolare il mondo: quante ne incontri, in che gruppi, di
giorno o di notte. La 5e ha spostato quella funzione dalle schede alle tabelle
d'incontro. **Non è informazione persa, è informazione trasferita**, e per un
gioco da tavolo digitale è materiale utile al generatore di incontri anche se
non entra nello statblock.

`MAGIC RESISTANCE` e `MORALE` sono un'altra cosa: erano meccanica di
risoluzione, e la 5e li ha eliminati per scelta di design. La resistenza magica
percentuale è diventata vantaggio ai tiri salvezza; il morale è diventato una
regola opzionale del DM. Qui una decisione va presa, perché nel 2e i draconici
avevano tutti resistenza magica e toglierla li indebolisce.

`XP VALUE` è il caso più insidioso: esiste in entrambe le edizioni ma vuol dire
il contrario. In 2e i punti esperienza sono calcolati dalla scheda; in 5e sono
derivati dal Grado di Sfida, che è la vera misura. Copiare il numero sarebbe
sbagliato in modo silenzioso.''')}

---

## Parte 2 — i cinque draconici, confronto puntuale

Le uniche creature con scheda in entrambe le edizioni. Sono anche le creature
identitarie di Krynn, quindi il campione non è casuale: è il migliore possibile.

{chr(10).join(scheda_confronto(n, completo) for n in D.ORDINE_5E)}

---

## Cosa l'ufficiale ha reso, scartato e aggiunto

{blocchi_resa}

{interpretativo('''Tre regolarità nel modo di rendere, che valgono per tutti e cinque.

**Le armi naturali diventano armi manufatte.** Baaz, Bozak, Kapak e Sivak in 2e
attaccavano con artigli e morso; in 5e hanno spada corta, tridente, pugnale e
spada seghettata. Solo l'Aurak conserva un attacco naturale (`Rend`). È una
scelta di caratterizzazione — sono soldati, non bestie — e non una necessità
tecnica.

**L'effetto alla morte guadagna un tiro salvezza e perde il tempo.** In 2e
quattro effetti su cinque colpivano senza tiro salvezza, e due si svolgevano in
più round: il Bozak avvizziva un round e poi esplodeva, l'Aurak restava attivo
come sfera di fulmini per tre round. In 5e tutto è istantaneo e tutto ha un
tiro salvezza. La 5e non ha una grammatica per gli effetti differiti.

**Ciò che colpiva l'equipaggiamento sparisce.** L'arma conficcata nella statua
del Baaz, l'acido del Kapak che distruggeva tesoro e oggetti magici: entrambe
tolte. Erano le regole che rendevano *costoso* uccidere un draconico, e la 5e
non le sostituisce con niente.''')}

---

## Parte 3 — esiste una regolarità?

| draconico | DV 2e | PF 5e | PF/DV | CA 2e | CA 5e | TAC0 | GS | GS−DV | PE 2e | PE 5e |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(righe_num)}

### Punti ferita

Il rapporto PF/DV va da **{min(rapporti):.1f}** a **{max(rapporti):.1f}**, media {sum(rapporti)/len(rapporti):.1f}.
Non è costante e non decresce in modo ordinato: il Kapak, che ha 3 DV, ne ha
{D.CINQUE_E['Kapak']['hp']/D.DUE_E['Kapak']['hd']:.1f} per dado, più di tutti gli altri.

### Grado di sfida

**GS = DV − 2 per quattro draconici su cinque.** Bozak, Sivak e Aurak lo
rispettano esattamente; il Baaz sarebbe a GS 0, e 1/2 è il valore più vicino
possibile. **Il Kapak lo rompe**: 3 DV e GS 3, cioè GS = DV.

### L'inversione, che è il dato più interessante

L'ordine di potenza cambia fra le due edizioni:

| | dal più debole al più forte |
|---|---|
| **2e**, per punti esperienza | {' → '.join(D.ORDINE_2E)} |
| **5e**, per grado di sfida | {' → '.join(D.ORDINE_5E)} |

Il Bozak in 2e vale {mille(D.DUE_E['Bozak']['xp'])} PE contro i {mille(D.DUE_E['Kapak']['xp'])} del Kapak, quindi è più forte.
In 5e il Bozak è GS {D.CINQUE_E['Bozak']['cr']} e il Kapak GS {D.CINQUE_E['Kapak']['cr']}: **si sono scambiati di posto**.

### Classe armatura

| | Baaz | Kapak | Bozak | Sivak | Aurak |
|---|---:|---:|---:|---:|---:|
| CA 2e (scende) | {D.DUE_E['Baaz']['ac']} | {D.DUE_E['Kapak']['ac']} | {D.DUE_E['Bozak']['ac']} | {D.DUE_E['Sivak']['ac']} | {D.DUE_E['Aurak']['ac']} |
| CA 5e (sale) | {D.CINQUE_E['Baaz']['ac']} | {D.CINQUE_E['Kapak']['ac']} | {D.CINQUE_E['Bozak']['ac']} | {D.CINQUE_E['Sivak']['ac']} | {D.CINQUE_E['Aurak']['ac']} |

L'**ordinamento è preservato** — chi era meglio protetto in 2e lo è anche in 5e —
ma non c'è una formula: Baaz e Kapak hanno la stessa CA 2e (4) e finiscono a 14 e 15.

### Economia delle azioni

| draconico | danno medio/round 2e | danno medio/round 5e | rapporto |
|---|---:|---:|---:|
{chr(10).join(f"| {n} | {d2:.1f} | {d5:.1f} | ×{r:.1f} |" for n, d2, d5, r in dpr)}

{interpretativo(f'''**La risposta alla domanda è no: cinque casi non bastano.**

Sul grado di sfida una regolarità si intravede — GS = DV − 2 tiene per quattro
su cinque — ma il quinto non è un arrotondamento: il Kapak sta due gradi sopra
dove la regola lo metterebbe. E non è un caso isolato, perché è **lo stesso
draconico** che rompe anche il rapporto PF/DV ({max(rapporti):.1f} contro una media di {sum(rapporti)/len(rapporti):.1f}) e
che moltiplica il danno per {max(r for _, _, _, r in dpr):.1f} contro il ×{min(r for _, _, _, r in dpr):.1f} del piu' conservativo.

Il Kapak non è un'anomalia dei numeri: è una **riprogettazione**. In 2e era un
assassino con un attacco debole e il veleno come minaccia; in 5e è diventato un
duellante con due pugnali avvelenati che paralizza. L'ufficiale non ha
convertito la creatura, l'ha ridisegnata attorno al suo ruolo narrativo.

Se estraessi da qui la formula «GS = DV − 2, PF = DV × 10» e la applicassi alle
cinquanta creature restanti, funzionerebbe finché le creature somigliano al loro
ruolo 2e e sbaglierebbe di due gradi ogni volta che il ruolo va ripensato.
Con cinquanta conversioni davanti, un'euristica che sbaglia su un caso su
cinque non fa risparmiare tempo: lo sposta dalla conversione al debug.

Quello che **si può** portare via da questi cinque casi non è una formula ma
tre vincoli:

1. l'**ordinamento** di CA e di potenza si conserva, **ma solo finché si
   conserva il ruolo**. Si può usare la fonte 2e per decidere chi è più forte
   di chi, e poi assegnare i numeri guardando la 5e — finché la creatura resta
   quello che era. Quando il ruolo viene ripensato, l'ordinamento non è più
   garantito: è quello che è successo al Kapak, che in 2e era dietro al Bozak e
   in 5e gli è passato davanti. Il controllo da fare prima di fidarsi
   dell'ordinamento è quindi sul **ruolo**, non sui numeri;
2. l'effetto identitario va conservato ma **riscritto con un tiro salvezza**,
   perché è così che la 5e esprime «succede qualcosa quando muore»;
3. i danni per round vanno **almeno raddoppiati** rispetto alla 2e — il minimo
   osservato è ×{min(r for _, _, _, r in dpr):.1f} — perché in 5e i personaggi hanno molti più punti ferita.

Sono tre vincoli, non un algoritmo. Il metodo che i dati suggeriscono è quello
della parte 4: conversione per analogia, non per calcolo.''')}

---

## Parte 4 — calibrazione sull'SRD

Per ciascun draconico ufficiale, i mostri SRD 5.1 di pari grado di sfida e ruolo
comparabile. Il confronto con la mediana del grado dice se l'ufficiale ha
costruito creature nella norma o fuori.

| draconico | GS | ruolo | CA/PF del draconico | mediana SRD del GS | analoghi SRD per ruolo |
|---|---|---|---|---|---|
{chr(10).join(tab_srd)}

Il bestiario SRD usato è in `dati/_fonti/srd51_mostri.py`: {len(SRD.MOSTRI)} creature,
l'intero SRD 5.1 (era limitato a 110 creature su cinque gradi di sfida; completato
perché la Fase 2 calibrerà anche le altre 48 creature dell'Appendice, di gradi
ancora ignoti).

### Il profilo difensivo, che è il pezzo che spiega il Kapak

In 5e il **Grado di Sfida è la media fra componente difensiva e componente
offensiva**. Una creatura può stare a un grado alto con pochi punti ferita, se
il danno la tira su da sola.

| draconico | GS | PF | mediana SRD del grado | quota | danno/round | ×rispetto al 2e |
|---|---|---:|---:|---:|---:|---:|
{tab_prof}

{interpretativo(f'''**Il Kapak ha {kapak[2]} punti ferita contro una mediana di {kapak[3]} al suo grado: il {kapak[4]:.0f}%.**
Sta *sotto* la mediana in difesa e ci arriva col danno — {kapak[5]:.0f} per round. È un
cannone di vetro, e in 2e non lo era: era un assassino con **un** attacco da 1-4.

**Ecco perché `GS = DV − 2` fallisce proprio su di lui.** Quella regola
presuppone che la creatura conservi il proprio profilo difensivo, perché i dadi
vita della 2e misurano solo la resistenza. Il Kapak ha cambiato asse: i dadi
vita dicono ancora "creatura da 3 DV", ma il grado di sfida risponde a un
danno che in 2e non c'era.

**Una precisazione che i numeri impongono, e che rafforza il punto invece di
indebolirlo.** Il Kapak non è l'unico sotto la mediana difensiva: lo sono
quattro draconici su cinque, e in modo crescente col grado — Bozak all'{[p for p in prof if p[0]=='Bozak'][0][4]:.0f}%,
Kapak e Sivak al {kapak[4]:.0f}%, Aurak al {[p for p in prof if p[0]=='Aurak'][0][4]:.0f}%. **I draconici sono una famiglia di
creature fragili e offensive**, per scelta di design: colpiscono forte, muoiono
in fretta, e alla morte esplodono addosso a chi li ha uccisi. È coerente.

Quello che è **unico** del Kapak non è quindi la fragilità, ma il **salto
offensivo rispetto alla propria fonte**: ×{kapak[6]:.1f} contro il ×{min(p[6] for p in prof if p[0]!='Kapak'):.1f}–×{max(p[6] for p in prof if p[0]!='Kapak'):.1f} degli altri
quattro. Gli altri sono stati riscalati; lui è stato **ripensato**.''')}

{interpretativo(f'''**Sopra la mediana in armatura, sotto in punti ferita.** È lo stesso profilo
visto sopra, letto sui due assi: la CA dei draconici sta sempre a pari o sopra
la mediana del grado ({D.CINQUE_E['Baaz']['ac']} contro {SRD.statistiche('1/2')['ca_med']} per il Baaz, {D.CINQUE_E['Aurak']['ac']} contro {SRD.statistiche('6')['ca_med']} per l'Aurak),
i punti ferita sempre sotto tranne il Baaz. Sono creature difficili da colpire
ma che cadono presto.

Il Baaz è comunque **identico al Lizardfolk** — CA 15 e 22 PF contro CA 14 e 22 —
e questo è il punto che conta: **la conversione per analogia è praticabile**. Per quasi ogni
draconico esiste almeno un mostro SRD dello stesso grado e dello stesso ruolo
con numeri molto vicini, e dove non c'è un analogo perfetto ce n'è uno
ragionevole.

L'eccezione è il **Kapak**: al GS 3 l'SRD non ha un assassino furtivo con
veleno. Il Doppelganger ha il profilo di furtività ma non il veleno,
l'Assassin vero è al GS 8. È un vuoto del catalogo, non un errore nostro, e
significa che per quel ruolo bisognerà comporre invece che copiare.''')}

---

## Il conteggio vero del bestiario

Il numero ricavato dal testo estratto era sbagliato, e la verifica sulle
immagini di pagina lo ha rifatto voce per voce.

| | |
|---|---:|
| voci dell'MC Appendix | **{BS['voci']}** |
| creature vere (statblock distinti) | **{BS['creature']}** |
| di cui schede di razze già in `dati/razze/` | {BS['razza_nostra']} |
| di cui razze e culture fuori dal roster | {BS['razza_altra']} |
| **creature da convertire** | **{BS['da_convertire']}** |

**{BS['n_multi']} voci hanno lo statblock su più colonne**: una voce, più creature.

| voce | pag. | creature |
|---|---:|---|
{tab_multi}

**{BS['nomi_sbagliati']} nomi di voce erano sbagliati** nel testo estratto, non solo i quattro
verificati per primi. Il dettaglio completo — testo estratto, nome reale, pagina,
causa — è nella tabella più sotto.

{interpretativo(f'''**L'estrazione non ha solo sbagliato i nomi: ha perso dei dati.** In tre voci
le colonne di destra sono sparite del tutto — `Avian` aveva quattro uccelli e
ne restavano due, `Stag` tre cervi e ne restava uno, `Man (of Krynn)` quattro
culture e ne restavano due. Sono **sette creature** che dal testo estratto non
esistevano affatto.

Il conteggio passa così da {BS['voci']} voci a **{BS['creature']}** creature vere. Non è un
aggiustamento marginale: è il {round(100 * (BS['creature'] / BS['voci'] - 1))}% in più, e cambia la stima di quanto lavoro
c'è davanti.

Due ritrovamenti che vale la pena segnalare. Il **Cervo Bianco**, una delle tre
colonne di `Stag`, non è una bestia: è unico, di allineamento legale buono,
vale 2.000 punti esperienza e ha capacità magiche — è una creatura sacra, e dal
testo estratto non risultava. Il **Drago Astrale** ha due statblock ma è una
specie sola in due stati, il solitario e la coppia accoppiata da 35 dadi vita
che il manuale tratta come singola creatura.''')}

{interpretativo(f'''**Questo numero non è un fatto acquisito: è la stima migliore ottenuta finora,
e va detto invece di presentare {BS['creature']} come definitivo.** Il conteggio "definitivo"
è già stato smentito tre volte in quattro giri — 55 → 68 → 83 → {BS['creature']} — e le voci a
colonne multiple sono emerse in passate successive, non in una sola: non
c'è garanzia che siano finite.

**I segnali usati, in ordine di scoperta:**

1. *Duplicazione di un campo sulla stessa riga.* Le prime quattro voci
   corrotte (`Yaggol`, `Tayling`, `Shadowperson`, `Man (of Krynn)`) sono state
   trovate perché il testo estratto riportava DUE valori di `FREQUENCY` sulla
   stessa riga (es. "Rare Uncommon"): un sintomo meccanico di colonne
   affiancate lette come una riga sola.
2. *La stessa duplicazione estesa a più campi.* La seconda passata ha
   allargato la ricerca a valori ripetuti su un numero qualunque di campi
   della scheda 2e, non solo `FREQUENCY`: ha trovato `Beast, Undead`
   (otto campi ripetuti) e altre voci che il primo segnale, più stretto, non
   intercettava.
3. *Rilettura manuale, voce per voce, sulle immagini di pagina.* Non un
   segnale automatico ma la verifica finale: ogni voce dell'elenco sopra è
   stata riletta sull'immagine, non solo sul testo estratto.
4. *Controllo dei salti nella sequenza di pagina — di natura diversa dai
   primi tre, e per questo ha trovato quello che loro non potevano.* I
   segnali 1-3 cercano tutti un'anomalia LEGGIBILE dentro il testo estratto
   di una voce: due valori sulla stessa riga, un'etichetta senza i due
   punti, un valore duplicato. Presuppongono cioè che la voce si lasci
   leggere almeno in parte. Il quarto segnale non cerca un difetto dentro le
   voci: elenca le pagine di tutte le voci già note e cerca i punti dove il
   numero salta più di un'unità — "dove mancano pagine fra due voci note",
   non "cosa c'è di storto in questa voce". Per questo è l'UNICO controllo
   che non dipende dal riuscire a leggere l'entrata mancante, ed è l'unico
   che poteva trovare `Centaur (of Krynn)` (pagg. 7-8, nel salto fra `Beast,
   Undead` a pag. 6 e `Disir` a pag. 9): la sua intestazione ha i NOMI DEI
   CAMPI corrotti (\"CUMATf.iTERRAIN\" invece di \"CLIMATE/TERRAIN\",
   \"THACO;\" invece di \"THAC0:\"), non solo i valori o il titolo — non
   c'era nulla da confrontare, quindi invisibile ai segnali 1-3 per
   costruzione, non per sfortuna. La maggior parte degli altri salti erano
   continuazioni legittime di voci già catalogate (una voce lunga due
   pagine); uno ha portato anche a verificare una voce di dragoni
   (`Dragon, Othlorx`, pag. 22) che non necessitava aggiunta: descrive
   varianti comportamentali di draghi standard già coperti (\"physically
   identical to the existing dragon forms\"), non un nuovo statblock.
5. *Ricerca di "See below" su tutti i campi di tutte le voci — di natura
   diversa dai primi quattro quanto il quarto lo era dai primi tre, ma nella
   direzione opposta.* I segnali 1-4 cercano voci MANCANTI o mal titolate:
   presuppongono che qualcosa nel testo estratto sia rotto o assente. Il
   quinto non cerca niente che manchi — cerca, dentro voci già lette e già
   classificate, i campi che la SCHEDA STESSA rimanda al testo perché "la
   riga della tabella non basta a descriverli". In AD&D 2e "See below" è
   dichiarazione dell'autore, non difetto di estrazione: la tabella ha uno
   spazio fisso, e quando non basta il manuale rimanda alla prosa. Trovato
   applicandolo prima ancora di leggere per intero le tre voci segnalate
   dall'audit dei Punti Esperienza (Wichtlin, Eyewing, Imp Blood Sea, tutte
   e tre con almeno un campo "See below"): il segnale vero dietro quell'audit
   non erano i PE alti in sé, ma la presenza di questi campi rimandati — i PE
   sono l'effetto (il manuale li conta nel totale), non la causa. A
   differenza dei segnali 1-4, questo si applica PRIMA di leggere una voce
   per intero, come segnale di priorità: fra le {n_voci_creatura} voci
   "creatura" dell'Appendice, **{n_flag} ({quota_flag}%)** hanno almeno un
   campo "See below" in un dato di combattimento (non nei campi di mondo
   `TREASURE`/`NO. APPEARING`, sempre esclusi dallo statblock per la
   decisione 27 gruppo A — l'unica eccezione è `Haunt, Knight`, dove
   `TREASURE` stesso resta "See below" senza un valore alternativo
   dichiarato altrove, e va comunque letto). Distribuzione sulle fasce
   attuali: {dist_5}. Tutte già lette per intero in questa sessione (elenco
   completo più sotto): tre nella seconda fascia (Bear Ice, Centaur,
   Eyewing) risolvono in un'immunità o un bonus singolo senza cambiare
   fascia, una (Lizard Man) rivela tre dettagli di fuga/vulnerabilità nuovi
   restando comunque di fascia bassa, due (Wichtlin, Imp Blood Sea) erano
   proprio le voci arrivate dall'audit sui PE e si sono confermate
   identitarie. La concentrazione nelle fasce basse-medie (seconda e terza,
   **{n_basse_medie} voci su {n_flag}, il {quota_basse_medie}%**) conferma
   l'aspettativa che l'ha motivato: è lì che un campo rimandato al testo può
   far più danno, perché è lì che ci si fida di più della prima impressione.

   | voce | fascia | campi "See below" |
   |---|---|---|
   {tab_segnale_5}

**Un limite dichiarato del quinto segnale**: non cattura tutto cio' che
richiede lettura completa. Lo Skrit (fascia 3, capacita' "jellification" mai
quantificata in nessun campo) e il Tylor (`SPECIAL DEFENSES: Special`, sei
categorie d'eta' con statistiche diverse) sono identitari quanto Wichtlin ma
il loro campo critico non dice "See below": dice un nome ("jellification") o
la parola "Special" senza rimando esplicito. Il quarto vincolo del metodo
(leggere lo statblock intero prima di classificare, mai dedotto da un solo
segnale) resta la rete di sicurezza; il quinto segnale e' un modo piu' economico
di decidere DA DOVE cominciare a leggere, non un sostituto della lettura.

**Segnali NON usati**, e quindi punti dove un ulteriore giro potrebbe ancora
trovare qualcosa: nessun controllo automatico ha confrontato il numero di
voci trovate con un indice o sommario del manuale (l'MC Appendix, formato
Monstrous Compendium a fogli sciolti, non ne ha uno stampato); nessun
controllo ha verificato che OGNI voce, non solo quelle già sospette, abbia un
blocco statistiche internamente coerente (es. `NO. OF ATTACKS` e
`DAMAGE/ATTACK` con lo stesso numero di elementi); e non è stata fatta una
rilettura sistematica di TUTTE le pagine a immagine, solo di quelle già
segnalate da un sintomo testuale, da un salto di pagina, o da un campo
rimandato al testo — quindi un difetto che non lascia nessuno dei tre
sintomi (un'intestazione corrotta ma su una pagina consecutiva, senza salto,
senza "See below") resta strutturalmente invisibile a tutti e cinque i
segnali usati finora.

Il conteggio delle voci (48 creatura, {BS['creature']} creature) non e'
cambiato con il quinto segnale: cerca dentro voci gia' contate, non ne
aggiunge. Il rapporto deve comunque dirlo, non nasconderlo dietro un
elenco di segnali che sembra chiuso.''')}

---

## Parte 5 — da dove iniziare

Le **{BS['da_convertire']} creature** da convertire, tolte le {BS['razza_nostra']} schede di razze giocanti già
coperte da `dati/razze/` e le {BS['razza_altra']} razze fuori roster. **Proposta, non decisione.**

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
con calma). Restano **{tot_creature} creature** su **{tot_righe} voci** nelle
cinque fasce, più il Cervo Bianco fuori fascia.

{chr(10).join(blocchi_prio)}

{interpretativo('''**Le fasce sono state ricostruite leggendo i 62 blocchi statistiche, non i
nomi delle voci.** La versione precedente aveva scelto la prima fascia (compresi
lo Scheletro Guerriero come "riempitivo generico" e l'Anemone Gigante come
"nicchia") prima di leggere gli statblock per intero: ha funzionato per la
maggioranza delle voci, ma ha sbagliato platealmente su alcune.

**8 voci hanno cambiato fascia** dopo la rilettura, quasi sempre verso l'alto:

- **Anemone Gigante**: quarta fascia (\"nicchia\") → **quinta** (fuori target).
  16 Dadi Vita, THAC0 5, **12.000 PE — più del doppio dell'Aurak Draconian**
  (6.000, il più forte dei cinque ufficiali). La sorpresa più grande del
  ricontaggio: era classificata come bestia acquatica minore ed è una delle
  creature più potenti dell'intero bestiario.
- **Fireshadow**: terza fascia → **quinta**. 13+3 DV (≈16, la stessa soglia
  degli altri fuori-target), Gargantuan, 11.000 PE — secondo valore più alto
  del bestiario.
- **Wyndlass**: quarta fascia (\"nicchia\") → **terza** (identitaria, costosa).
  12 DV, THAC0 9, **undici attacchi**, 5.000 PE — stesso ordine di grandezza
  del Cavaliere della Morte e dello Scheletro Guerriero, non una curiosità
  acquatica.
- **Fetch**: seconda fascia → **terza**. 9 DV, drena 2 livelli per colpo,
  invisibile a chiunque tranne la vittima designata: molto più pericoloso di
  quanto \"non morto mutaforma di fascia media\" suggerisse.
- **Spectral Minion**: seconda fascia → **terza**. Colpibile solo da armi
  magiche, sei varianti nominate con PE diversi sotto un'unica voce: una
  famiglia di sotto-tipi, non un riempitivo semplice.
- **Bear Ice, Disir, Eyewing, Gurik Cha-ahl, Kani Doll**: quarta fascia
  (\"nicchia\") → **seconda**. Nella direzione opposta: erano trattate come
  curiosità di nicchia e sono in realtà riempitivi puliti di fascia bassa,
  senza nulla di anomalo nella scheda.

**2 voci in più hanno cambiato fascia il 20 agosto 2026**, dopo l'audit sui
Punti Esperienza e il quinto segnale (ricerca di \"See below\"; dettaglio
sopra, \"Il conteggio vero del bestiario\"):

- **Wichtlin**: seconda fascia → **terza** (identitaria, costosa). Doppio
  tocco di contatto (paralisi + veleno), immunità multiple, contagio su
  elfi uccisi in sette giorni, variante montata: molto più di un
  riempitivo, nello stesso modo in cui lo era risultato lo Skrit.
- **Imp, Blood Sea**: quarta fascia (\"nicchia\") → **terza** (identitaria,
  costosa). Polimorfismo fisico/nebbia, immunità multiple, scissione da
  fulmine: la fascia \"nicchia\" descriveva l'ambientazione (il Mare di
  Sangue), non la meccanica — lo stesso equivoco di Bear Ice/Disir/Eyewing,
  ma nella direzione opposta.

L'**Eyewing**, letto per intero nello stesso giro, e' rimasto in seconda
fascia (il campo rimandato al testo si risolveva in una sola immunita' al
freddo) ed e' stato **convertito**: vedi `dati/mostri/eyewing.json`.

**2 voci hanno una correzione di lettura, non di fascia:**

- **Yaggol**: il rapporto diceva che il suo 50% di resistenza magica fosse il
  più alto del bestiario. **Non lo è**: lo Scheletro Guerriero ne ha 90%, il
  Cavaliere della Morte 75%. Corretto ovunque compaia.
- **Cavaliere della Morte**: la sessione precedente lo identificava con Lord
  Soth. La voce dell'Appendice descrive però un **tipo** ("a Knight of
  Solamnia, cursed by the gods..."), non un individuo nominato — la fonte non
  cita mai Soth. Applicando il criterio della decisione 32 (nome proprio e
  storia, non vincolo a un oggetto), il Cavaliere della Morte è una
  **creatura**, non un'entità: si converte al suo grado reale come le altre,
  e il suo statblock è strutturalmente quasi gemello dello Scheletro
  Guerriero (9 DV, THAC0 11, un solo attacco con bonus fisso, resistenza
  magica altissima). Lord Soth, se e quando serve come antagonista con nome
  proprio, resta un'istanza particolare dello stesso tipo — non la fonte di
  questa voce.

**La categoria ENTITÀ, per ora, è vuota.** Fra le 62 voci lette non ce n'è
una che abbia nome proprio e storia propria dichiarati dalla fonte stessa
(il Cavaliere della Morte era l'unica candidata, ed è ricaduta in creatura).
Non è un difetto della categoria: il criterio della decisione 32 ha retto al
primo caso a cui è stato applicato, respingendolo. Resta nello schema e nel
metodo per il giorno in cui una voce ci ricadrà davvero — un nome proprio
dichiarato dalla fonte, non un'identificazione fatta da noi.

**Il Tylor non è un problema aperto: è lavoro rimandato.** Sei categorie
d'età con Dadi Vita, CA e soffio diversi, sullo stesso schema degli age
category dei draghi — esattamente il caso per cui lo schema del mostro ha
già `name.variante_di`. Si converte come una famiglia di statblock collegati
da quel campo (una voce per categoria d'età, ciascuna con il proprio GS),
non come un singolo mostro: non serve una decisione, serve solo farlo
quando tocca al Tylor.

**Il Dreamshadow è un problema diverso, non un'altra voce complicata.** Ogni
campo della sua scheda — CA, DV, THAC0, danno, taglia, perfino l'allineamento
— è dichiarato "as creature or person mimicked": la voce non ha statistiche
proprie da nessuna parte. Non è una creatura a cui manca un analogo SRD, è
una **regola di trasformazione** applicata a un'altra creatura o persona: il
metodo per analogia non si applica perché non c'è nulla a cui applicarlo, il
bersaglio cambia scheda ogni volta che il Dreamshadow ne imita una diversa.
Registrato qui come categoria a parte, non forzato in uno statblock: è il
primo caso del genere nel bestiario, e probabilmente non l'ultimo — conviene
riconoscerli quando emergono invece di inventargli un GS di comodo.

**I Dadi Vita non bastano a classificare una voce — vale anche per i Punti
Esperienza, e non erano stati controllati sistematicamente.** Lo Scheletro
Guerriero e lo Skrit sono stati classificati male nello stesso modo: fascia
dedotta da DV/CA senza guardare gli XP dichiarati. In 2e gli XP sono il
giudizio del manuale sulla pericolosità complessiva, non un derivato dei
Dadi Vita. Ripassata la lista confrontando XP dichiarati e fascia assegnata:
un controllo di minuti, non di ore.

**Voci dove gli XP non tornano con la fascia — RISOLTE il 20 agosto 2026
con la lettura completa** (vedi anche il quinto segnale, sopra, che ha
trovato lo stesso terzetto cercando "See below" invece degli XP): il numero
impone la lettura completa prima di convertire, non è un verdetto automatico
(lo Skrit era anche lui "solo un numero" finché non si è letto il resto).

- **Wichtlin**: LETTO PER INTERO, SPOSTATO in terza fascia (era seconda).
  Non un riempitivo: doppio tocco paralisi/veleno, immunità multiple,
  contagio su elfi uccisi, variante montata. Dettaglio nella voce di terza
  fascia, sopra.
- **Eyewing**: LETTO PER INTERO, CONVERTITO in seconda fascia (fascia
  confermata). `SPECIAL DEFENSES: See below` si risolve nella sola
  immunità al freddo: il segnale era acceso ma la causa era semplice, come
  già per il Kyrie. Vedi `dati/mostri/eyewing.json`.
- **Imp, Blood Sea**: LETTO PER INTERO, SPOSTATO in terza fascia (era
  quarta). Polimorfismo fisico/nebbia, immunità multiple, scissione da
  fulmine: la fascia "nicchia" descriveva l'ambientazione, non la
  meccanica. Dettaglio nella voce di terza fascia, sopra.
- **Kyrie** (già convertito, GS 1): XP 1.400 in 2e, lo stesso ordine di
  grandezza del Wichtlin e del Bozak Draconian ufficiale (GS 2). La
  conversione già fatta assegna GS 1 sul danno per round dichiarato (un
  solo attacco, mai più di 1d8) e sull'assenza di resistenze: il numero
  resta un segnale da tenere presente, non un errore accertato — a
  differenza dello Skrit, qui il danno base *è* stato letto per intero e
  *è* modesto. Segnalato, non ritoccato.

Verificati sugli XP e poi CORRETTI da una lettura più a fondo (il quinto
segnale, sopra, non l'audit sugli XP): **Lizard Man** (Jarak-Sinn 270,
Bakali 175 — XP bassi, fascia confermata, ma `SPECIAL DEFENSES: See below`
su entrambe le colonne nasconde la coda distaccabile del jarak-sinn e la
vulnerabilità al freddo del bakali, mai controllate perché gli XP sembravano
chiudere la questione) e **Centaur (of Krynn)** (stesso schema: fascia
confermata, il campo risolve nel +2 ai tiri salvezza degli Abanasiniani, già
previsto come dettaglio di sotto-specie da estrarre in conversione). Insect
Swarm resta verificato coerente sulla fascia (XP "See below" per entrambe le
varianti: non c'è un numero fisso da confrontare, la fascia distingue sulla
base del veleno dichiarato) ma porta anch'esso più campi "See below" del
previsto — vedi il quinto segnale.

**Il criterio resta l'arena, non la completezza**, e non cambia: la Fase 2 ha
bisogno di avversari fra GS 1/4 e GS 4, in quantità e con tattiche diverse. La
quinta fascia contiene ora sette voci invece di cinque (Anemone Gigante e
Fireshadow si aggiungono ai draghi), e non ne serve nessuna alla Fase 2. **La
prima fascia è completa**: Traag (GS 1/4), Scheletro Guerriero (GS 7, al suo
vero grado, non a quello presunto), Thanoi (GS 2) e Kyrie (GS 1) sono tutti
convertiti. Il Thanoi ha avuto un riscontro in più: le statistiche 3.5 del
lotto Dragonlance Campaign Setting (`riscontro/3.5/`, consultazione, non
fonte) assegnano CR 2 in modo indipendente, confermando la stima fatta sulla
sola scheda 2e più l'analogia SRD.

Il **Cervo Bianco** resta fuori da tutte e cinque le fasce: non è un
avversario, è una creatura sacra unica da incontro narrativo. Forzarlo in una
fascia da combattimento travisirebbe cosa è.''')}

---

## Gli {BS['nomi_sbagliati']} nomi corrotti — verificati

Riletti sulle immagini di pagina, con lo stesso metodo dei tratti razziali del
PHB 2e. I primi quattro erano stati verificati in un primo giro; il
ricontaggio voce per voce ne ha trovati altri quattro con la stessa causa.
**Tutti e {BS['nomi_sbagliati']} leggibili: nessuna voce resta sospesa.**

| testo estratto | nome reale | pag. PDF | causa |
|---|---|---:|---|
{tab_nomi}

{interpretativo(f'''**La causa è quasi sempre una sola, e non è un difetto delle pagine.**
{BS['n_multi']} casi su {BS['nomi_sbagliati']} sono voci con statblock a **più colonne**: una sola
voce del manuale contiene due o più creature affiancate, ciascuna con la
propria colonna di valori. L'estrattore, che lavora a due colonne di testo,
legge i titoli delle colonne di fianco come se fossero una riga sola. Gli
altri {BS['nomi_sbagliati'] - BS['n_multi']} hanno un'altra causa: `Minotaur (of Krynn)` prendeva
l'intestazione di una colonna interna (`Blood Sea Minotaur`) come titolo
della voce; `Yaggol` aveva semplicemente le lettere spaziate nello stampato.

**Questo cambia il conteggio del bestiario.** Dietro le {BS['n_multi']} voci a più colonne
ci sono **{n_creature_multi} creature**, non {BS['n_multi']}: `Man (of Krynn)` ne contiene quattro,
`Avian` altrettante, `Stag` tre, `Tayling`, `Shadowperson` e `Dragon, Astral`
due ciascuna. Il numero vero — **{BS['voci']} voci, {BS['creature']} creature** — è quello
stabilito qui sopra in "Il conteggio vero del bestiario", voce per voce sulle
immagini di pagina: non resta più nulla da chiarire su questo fronte.

Due correzioni puntuali che l'immagine ha prodotto: il gemello bestiale del
Tayling si chiama **Taylang**, non "Tayland" come leggeva il testo estratto; e
`Man (of Krynn)` è una scheda di **PNG umani**, quindi va con le voci razziali
già escluse dal conteggio dei mostri, non fra le creature da convertire.''')}

---

## Cosa manca prima di poter convertire

Delle tre cose che mancavano, **sono fatte tutte e tre**.

- ~~Schema del mostro~~ → `dati/schema/mostro.schema.json`, validato sui cinque
  draconici.
- ~~Verifica degli {BS['nomi_sbagliati']} nomi corrotti~~ → tutti leggibili, vedi sopra.
- ~~Decisione sui sette campi senza corrispettivo~~ → decisione 27, sotto: due
  gruppi chiusi, uno rinviato con motivo.
- ~~Conteggio vero delle creature dell'MC Appendix~~ → **{BS['voci']} voci,
  {BS['creature']} creature**, stabilito voce per voce sulle immagini di pagina —
  vedi "Il conteggio vero del bestiario" sopra.

{interpretativo(f'''Nessuna delle tre resta aperta. Quello che resta, e non è bloccante per
cominciare a convertire, è un disallineamento scoperto per strada: il
generatore di `RAPPORTO-mostri.md` (`confronta_mostri.py`) conta le voci
dell'MC Appendix rileggendo il testo estratto con un'altra regola (i blocchi
`CLIMATE/TERRAIN:`), indipendente da questo ricontaggio verificato sulle
immagini. Dà **55**, non {BS['voci']}. Non è lo stesso tipo di errore dei nomi
corrotti — è un secondo modo di contare, mai riconciliato col primo dopo il
ricontaggio. Va allineato a questa fonte prima di fidarsi del suo numero, ma
non impedisce di cominciare a convertire: la prima fascia non dipende da lui.''')}

---

## Decisione 27 — i sette campi senza corrispettivo

Non erano un problema unico. Si dividono in tre gruppi, e due si sono chiusi
senza deliberare.

| gruppo | campi | esito | destinazione |
|---|---|---|---|
{tab_27}

### Gruppo A — dati di mondo, non di scheda

{C27.GRUPPO_A['motivo']}

Campi: {', '.join('`' + c + '`' for c in C27.GRUPPO_A['campi'])}.
Restano in `source_2e`, e nello schema sono raccolti anche in
`mechanics_5e.world_data_2e` con `destinazione: {C27.GRUPPO_A['destinazione']}`.
Nessuna conversione, nessuna decisione: la destinazione è registrata perché la
questione non venga riaperta.

### Gruppo B — il morale non è un campo, è un parametro

{C27.GRUPPO_B['motivo']}

Nello schema è `mechanics_5e.morale_2e`, con valore, etichetta della fonte e
`destinazione: {C27.GRUPPO_B['destinazione']}`. **Non entra nello statblock.**

### Gruppo C — resistenza magica, rinviata

{C27.GRUPPO_C['motivo']}

**Perché la decisione 16 non si applica.** {C27.GRUPPO_C['perche_non_vale_la_16']}

**Il problema di traduzione.** {C27.GRUPPO_C['problema_di_traduzione']}

Il valore percentuale resta in `source_2e` e in
`mechanics_5e.magic_resistance_2e` con `applied: false`.
**Quando si decide:** {C27.GRUPPO_C['quando_si_decide']}

**Creatura di riferimento.** {C27.GRUPPO_C['creatura_di_riferimento']}
"""
      open(out, "w", encoding="utf-8").write(doc)
      testo = open(out, encoding="utf-8").read()
      print(f"scritto {out} ({len(testo):,} caratteri)".replace(",", "."))
    print(f"campi 2e: {dict(cat1)}")
    print(f"PF/DV: min {min(rapporti):.1f} max {max(rapporti):.1f} "
          f"media {sum(rapporti)/len(rapporti):.1f}")
    print(f"GS-DV: {diff_cr}")
    print(f"solo MC: {len(solo_mc)}, di cui voci razziali {len(VOCI_RAZZIALI)}")
    return cat1


if __name__ == "__main__":
    main()
