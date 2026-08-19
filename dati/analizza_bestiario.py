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


def scheda_confronto(n):
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
        f"{b['azioni'][0][1]} |",
        f"| movimento | {a['movement']} | {b['speed']} |",
        f"| difese speciali | {a['special_defenses']} | "
        f"{b.get('extra', '—')} |",
        f"| resistenza magica | {a['magic_resistance']} | "
        f"**non esiste in 5e** |",
        f"| morale | {a['morale']} | **non esiste in 5e** |",
        f"| valore | {a['xp']:,} PE (formula 2e) | ".replace(",", ".")
        + f"Grado di Sfida **{b['cr']}** ({b['xp']:,} PE) |".replace(",", "."),
        "",
        f"**Effetto alla morte — la firma del draconico.**", "",
        f"*2e*: {a['morte']}", "",
        f"*5e*: {[t for t in b['tratti'] if t[0] == 'Death Throes'][0][1]}", "",
    ]
    r += ["**Azioni 5e**", ""]
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
# PARTE 5 — ordine di lavorazione proposto
# ==========================================================================
# (nome, fascia, motivo, analogo SRD evidente?)
PRIORITA = [
    ("Traag (proto-draconico)", 1,
     "Completa la famiglia dei draconici, l'unica su cui abbiamo un precedente "
     "ufficiale. E' il gradino piu' basso: serve all'arena come avversario "
     "iniziale.", "sì — Kobold / Goblin"),
    ("Warrior, Skeleton", 1,
     "Non morto generico di basso livello, il riempitivo classico dell'arena. "
     "Ha l'analogo SRD piu' diretto di tutto il roster.", "sì — Skeleton"),
    ("Thanoi (Walrus Man)", 1,
     "Umanoide bestiale di fascia bassa, identitario del nord di Krynn.",
     "sì — Gnoll / Lizardfolk"),
    ("Kyrie", 1,
     "Umanoidi alati, avversari volanti di fascia bassa: l'arena ha bisogno "
     "di bersagli in volo presto.", "sì — Harpy / Hippogriff"),
    ("Horax", 2,
     "Bestia da branco, utile a riempire incontri senza tattica complessa.",
     "sì — Giant Wasp / Giant Spider"),
    ("Skrit", 2, "Come sopra, fascia bassissima.", "sì — Giant Centipede"),
    ("Wichtlin", 2,
     "Non morto elfico, identitario e di fascia media.", "sì — Wight / Specter"),
    ("Fetch", 2, "Non morto mutaforma di fascia media.", "sì — Shadow / Ghost"),
    ("Spectral Minion", 2, "Non morto evocato, fascia media.", "sì — Specter"),
    ("Dreamshadow", 3,
     "Non morto psichico: identitario ma senza analogo pulito.", "no"),
    ("Dreamwraith", 3, "Come sopra, fascia piu' alta.", "no"),
    ("Fireshadow", 3, "Creatura elementale di Krynn, nessun analogo diretto.", "no"),
    ("Fire Minion", 3, "Come sopra.", "parziale — Magmin"),
    ("Tylor", 3,
     "Mostruosita' grande e identitaria, fascia medio-alta.", "parziale — Chimera"),
    ("Knight, Death", 3,
     "**Il Cavaliere della Morte**: e' Lord Soth, cioe' l'antagonista "
     "simbolo del setting. SotDQ ha lo statblock di Soth come PERSONAGGIO, "
     "che puo' servire da riferimento ma non e' la scheda di specie.",
     "parziale — Wight / Revenant, ma sottodimensionati"),
    ("Haunt, Knight", 3, "Variante spettrale del precedente.", "no"),
    ("Gurik Cha-ahl", 4, "Creatura di nicchia.", "no"),
    ("Disir", 4, "Creatura di nicchia.", "no"),
    ("Kani Doll", 4, "Costrutto di nicchia.", "parziale — Homunculus"),
    ("Shimmerweed", 4, "Pianta, nicchia.", "parziale — Shrieker"),
    ("Wyndlass", 4, "Creatura acquatica di nicchia.", "no"),
    ("Kalothagh (Prickleback)", 4, "Bestia acquatica.", "sì — Reef Shark"),
    ("Anemone, Giant", 4, "Bestia acquatica.", "parziale"),
    ("Imp, Blood Sea", 4, "Diavoletto locale.", "sì — Imp / Quasit"),
    ("Eyewing", 4, "Bestia volante di nicchia.", "no"),
    ("Bear, Ice", 4, "Bestia.", "sì — Polar Bear"),
    ("Wild Stage", 4, "Bestia.", "sì — Elk"),
    ("Dragon, Amphi", 5, "Drago: la Fase 2 non ne ha bisogno.", "sì — draghi SRD"),
    ("Dragon, Kodragon", 5, "Come sopra.", "sì"),
    ("Dragon, Sea", 5, "Come sopra.", "sì"),
    ("Y a g g o l", 5, "Nome corrotto nell'estrazione: da riverificare prima.", "no"),
    ("Tayling Tayland", 5, "Nome corrotto nell'estrazione: da riverificare.", "no"),
    ("Ice Folk Knights of", 5, "Nome corrotto: e' una voce Man/Knight spezzata.", "no"),
    ("Shadowperson Revered Ancient One", 5,
     "Nome corrotto: due voci fuse dall'estrazione.", "no"),
]

# Le voci razziali dell'MC Appendix: NON sono mostri da convertire, sono le
# schede PNG delle razze giocanti che abbiamo gia' in dati/razze/.
VOCI_RAZZIALI = [
    "Dwarf, Hill (Neidar)", "Dwarf, Mountain (Hylar)", "Dwarf, Theiwar",
    "Dwarf, Zakhar", "Elf, Half", "Elf, High-Qualinesti",
    "Elf, High-Silvanesti", "Elf, Wild-Kagonesti", "Elf, Sea-Dargonesti",
    "Elf, Sea-Dimernesti", "Gnome, Tinker (Minoi)", "Kender",
    "Ogre, High (Irda)", "Blood Sea Minotaur", "Emre Kingfisher",
    "Yeti-kin, Saqualaminoi",
]


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

    tab_nomi = "\n".join(
        f"| `{v['estratto']}` | **{v['corretto']}**"
        + (f" (+{len(v['creature'])-1} varianti)" if len(v['creature']) > 1 else "")
        + f" | {v['pagina_pdf']} | {v['causa']} |"
        for v in NV.VERIFICATE)

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
    for nome, f, motivo, an in PRIORITA:
        per_fascia[f].append((nome, motivo, an))
    NOMI_FASCIA = {1: "Prima — servono subito all'arena",
                   2: "Seconda — riempitivi di fascia bassa e media",
                   3: "Terza — identitari ma senza analogo pulito",
                   4: "Quarta — nicchia",
                   5: "Quinta — non servono alla Fase 2, o da riverificare"}
    blocchi_prio = []
    for f in sorted(per_fascia):
        blocchi_prio.append(f"### {NOMI_FASCIA[f]} ({len(per_fascia[f])})\n")
        blocchi_prio.append("| creatura | perché | analogo SRD |\n|---|---|---|")
        for nome, motivo, an in per_fascia[f]:
            blocchi_prio.append(f"| {nome} | {motivo} | {an} |")
        blocchi_prio.append("")

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

{chr(10).join(scheda_confronto(n) for n in D.ORDINE_5E)}

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

Il sottoinsieme SRD usato è in `dati/_fonti/srd51_mostri.py`: {len(SRD.MOSTRI)} creature
sui {SRD.TOTALE_SRD} totali, limitate ai cinque gradi di sfida che servono.

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

**{BS['nomi_sbagliati']} nomi di voce erano sbagliati** nel testo estratto, non quattro come si
credeva. Le altre quattro emerse ora: `Emre Kingfisher` era **Avian**,
`Unmated Mated pair*` era **Dragon, Astral**, `Blood Sea Minotaur` era
**Minotaur (of Krynn)**, `Wild Stage` era **Stag**.

{interpretativo(f'''**L'estrazione non ha solo sbagliato i nomi: ha perso dei dati.** In tre voci
le colonne di destra sono sparite del tutto — `Avian` aveva quattro uccelli e
ne restavano due, `Stag` tre cervi e ne restava uno, `Man (of Krynn)` quattro
culture e ne restavano due. Sono **sette creature** che dal testo estratto non
esistevano affatto.

Il conteggio passa così da {len(mc)} a **{BS['creature']}**. Non è un aggiustamento marginale: è
il 24% in più, e cambia la stima di quanto lavoro c'è davanti.

Due ritrovamenti che vale la pena segnalare. Il **Cervo Bianco**, una delle tre
colonne di `Stag`, non è una bestia: è unico, di allineamento legale buono,
vale 2.000 punti esperienza e ha capacità magiche — è una creatura sacra, e dal
testo estratto non risultava. Il **Drago Astrale** ha due statblock ma è una
specie sola in due stati, il solitario e la coppia accoppiata da 35 dadi vita
che il manuale tratta come singola creatura.''')}

---

## Parte 5 — da dove iniziare

Le **{BS['da_convertire']} creature** da convertire, tolte le {BS['razza_nostra']} schede di razze giocanti già
coperte da `dati/razze/` e le {BS['razza_altra']} razze fuori roster. **Proposta, non decisione.**

L'ordine qui sotto è quello formulato prima del ricontaggio: **va rivisto**,
perché sette creature nuove non erano nell'elenco.

{chr(10).join(blocchi_prio)}

{interpretativo('''**Il criterio è l'arena, non la completezza.** La Fase 2 è un motore di
combattimento e ha bisogno di avversari fra GS 1/4 e GS 4, in quantità e con
tattiche diverse fra loro. Non ha bisogno di draghi: un drago in arena è una
sessione, non un banco di prova.

La prima fascia è scelta così: il **Traag** completa la famiglia dei draconici
e quindi si converte con il precedente ufficiale ancora in mano; **Scheletro
guerriero**, **Thanoi** e **Kyrie** coprono i tre ruoli che a un'arena servono
subito — non morto generico, fante bestiale, avversario volante — e hanno tutti
un analogo SRD diretto.

La terza fascia è quella che costa di più, e va affrontata quando il metodo è
rodato: sono creature identitarie senza analogo pulito, dove bisogna comporre.
Il **Cavaliere della Morte** è il caso simbolo — è Lord Soth — e ha una
particolarità utile: SotDQ ha lo statblock di Soth come personaggio, che serve
da riferimento numerico anche se non è la scheda di specie.

Quattro voci della quinta fascia hanno il nome corrotto dall'estrazione a
colonne. Vanno riverificate sulle pagine originali prima di qualunque lavoro:
non si converte una creatura di cui non si sa il nome.''')}

---

## I quattro nomi corrotti — verificati

Riletti sulle immagini di pagina, con lo stesso metodo dei tratti razziali del
PHB 2e. **Tutti e quattro leggibili: nessuna voce resta sospesa.**

| testo estratto | nome reale | pag. PDF | causa |
|---|---|---:|---|
{tab_nomi}

{interpretativo(f'''**La causa è una sola, e non è un difetto delle pagine.** Tre casi su quattro
sono voci con statblock a **più colonne**: una sola voce del manuale contiene
due o più creature affiancate, ciascuna con la propria colonna di valori.
L'estrattore, che lavora a due colonne di testo, legge i titoli delle colonne
di fianco come se fossero una riga sola. Il quarto è semplicemente un titolo
con le lettere spaziate.

**Questo cambia il conteggio del bestiario.** Dietro le quattro voci ci sono
**{NV.totale_creature()} creature**, non quattro: `Man (of Krynn)` ne contiene quattro,
`Tayling` e `Shadowperson` due ciascuna. Lo stesso segnale — due valori di
`FREQUENCY` sulla stessa riga — ne individua altre {len(NV.SOSPETTE_STESSA_CAUSA)} con lo stesso difetto.
Il numero di creature dell'MC Appendix è quindi **maggiore delle {len(mc)} voci
contate**, e va stabilito voce per voce prima di pianificare davvero.

Due correzioni puntuali che l'immagine ha prodotto: il gemello bestiale del
Tayling si chiama **Taylang**, non "Tayland" come leggeva il testo estratto; e
`Man (of Krynn)` è una scheda di **PNG umani**, quindi va con le voci razziali
già escluse dal conteggio dei mostri, non fra le creature da convertire.

Un dato utile emerso per strada: lo **Yaggol** ha resistenza magica **50%**, la
più alta del bestiario. È la creatura su cui la decisione 27 gruppo C peserà di
più.''')}

---

## Cosa manca prima di poter convertire

Delle tre cose che mancavano, **due sono fatte**.

- ~~Schema del mostro~~ → `dati/schema/mostro.schema.json`, validato sui cinque
  draconici.
- ~~Verifica dei quattro nomi corrotti~~ → tutti e quattro leggibili, vedi sopra.
- **Decisione sui sette campi senza corrispettivo** → decisione 27, sotto: due
  gruppi chiusi, uno rinviato con motivo.

{interpretativo(f'''Resta una cosa sola, e non è una decisione: **il conteggio vero delle creature
dell'MC Appendix**. Le {len(mc)} voci contate non sono {len(mc)} creature, perché almeno
{len(NV.VERIFICATE) + len(NV.SOSPETTE_STESSA_CAUSA)} voci ne contengono più d'una su colonne affiancate. Prima di stabilire
un ordine di lavorazione definitivo va fatto un passaggio voce per voce che
separi le colonne — è lo stesso lavoro dei quattro nomi, esteso a tutto il
bestiario, e si fa con le immagini di pagina.

Non è bloccante per cominciare: le creature della prima fascia proposta hanno
tutte una voce singola. È bloccante per sapere quante sono in totale.''')}

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
"""
    out = os.path.join(BASE, "RAPPORTO-bestiario.md")
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
