#!/usr/bin/env python3
"""
DECISIONE 23 (`principio-del-clone`) — il principio del clone.

    Per le classi la fedelta' alla fonte non basta. Le razze 2e sono ricche e
    la trascrizione integrale ha prodotto voci piene; le classi 2e sono povere,
    e trascriverle fedelmente produce diciassette gusci vuoti.

    Ogni classe di Krynn e' un CLONE MECCANICO della classe base 5e
    corrispondente — dado vita, attacchi extra, aumenti di caratteristica,
    competenze, tutto identico — con innestati sopra i privilegi e le
    restrizioni della fonte ai livelli previsti.

    Non si inventa nulla: si copia il chassis dall'SRD 5.1 e ci si appoggia
    sopra la fonte.

CINQUE CLASSI RESTANO SENZA CHASSIS
    Popolano, Tinker, Sacerdote Eretico, Handler e Marinaio. Il rapporto le
    aveva segnalate come prive di candidato pulito e la decisione 23 (`principio-del-clone`) le lascia
    esplicitamente indecise. Restano `in_sospeso`: proposte nel rapporto,
    nessuna applicata. Dal 05/09/2026 ciascuna ha anche un id nel registro
    delle questioni aperte, per poter essere citata da fuori.

TRE CLASSI DOVE IL CHASSIS NON E' UN ACCOSTAMENTO MA UN'IDENTITA'
    Guerriero, Paladino e Ladro sono le classi base AD&D 2e che la
    decisione 59 (`classi-base-2e`) ha trascritto dal PHB. Per tutte le altre
    voci di `CHASSIS` la `ragione` argomenta un accostamento fra una classe di
    Krynn e un chassis 5e; per queste tre non c'e' niente da argomentare,
    perche' sono la stessa classe in due edizioni. Da non confondere con le
    classi di Krynn che condividono il loro telaio: il Cavaliere della Spada
    sta su Paladin ed e' un ordine solamnico, il Con Artist sta su Rogue ed e'
    il ladro proprio di Krynn.

LE SETTE INCOMPATIBILITA' STRUTTURALI
    Discendono dalla scelta della 5e come chassis e sono applicate qui, in un
    punto solo, uguali per tutte le classi. Il dato 2e non viene cancellato:
    resta in `source_2e`.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "_fonti"))

import _srd51 as R
import srd51_pacchetti as PK  # noqa: E402

DEC = "DECISIONE 23 (`principio-del-clone`)"

# --------------------------------------------------------------------------
# Chassis per classe. `None` = nessun candidato pulito, lasciato indeciso.
# --------------------------------------------------------------------------
CHASSIS = {
    "barbaro": ("Fighter",
                "NON Barbarian: l'Ira e' un'invenzione della 3e, assente sia da "
                "Krynn sia dal kit del 1989 da cui il Barbaro di Ansalon "
                "discende. Confermato dall'appendice di RAPPORTO-classi.md."),
    "cavaliere-corona": ("Fighter",
                         "Guerriero puro, nessuna magia al primo grado. La "
                         "sequenza verso Spada e Rosa (decisione 5, `cavalieri-solamnia`) si innesta "
                         "sopra il chassis."),
    "cavaliere-spada": ("Paladin",
                        "La fonte dice esplicitamente \"capacita' della classe "
                        "Paladino al proprio livello\" e concede incantesimi "
                        "sacerdotali dal 6°. E' l'accoppiamento piu' pulito del "
                        "roster."),
    "cavaliere-rosa": ("Paladin",
                       "Prosegue il grado precedente. L'immunita' alla paura e' "
                       "gia' un privilegio del Paladino (Aura di Coraggio)."),
    "cavaliere": ("Fighter",
                  "Sei privilegi tutti di combattimento montato e reputazione. "
                  "In SRD l'unico archetipo marziale e' il Campione: il montato "
                  "resta scoperto e il codice comportamentale pure."),
    "mago-alta-stregoneria": ("Wizard", "Corrispondenza diretta."),
    "mago-rinnegato": ("Wizard",
                       "Stesso chassis, definito per sottrazione: e' il Mago "
                       "dell'Alta Stregoneria senza vincoli e senza bonus lunari."),
    "mago-veste-bianca": (None, "AFFILIAZIONE, non classe (decisione 6, `maghi-delle-torri`)."),
    "mago-veste-nera": (None, "AFFILIAZIONE, non classe (decisione 6, `maghi-delle-torri`)."),
    "mago-veste-rossa": (None, "AFFILIAZIONE, non classe (decisione 6, `maghi-delle-torri`)."),
    "sacerdote-ordini-sacri": ("Cleric",
                               "Corrispondenza diretta. Le sfere gia' estratte "
                               "diventano il filtro della decisione 24 (`sfere-sacerdotali`); il "
                               "Dominio resta come sottoclasse."),
    "con-artist": ("Rogue",
                   "Le quattro abilita' potenziate diventano competenze ed "
                   "Esperienza."),
    # ---- classi base 2e, decisione 59 (`classi-base-2e`) ----
    # Qui il chassis NON e' un accostamento editoriale: e' la stessa classe.
    # Il Guerriero 2e e il Fighter SRD sono la medesima classe in due
    # edizioni, e lo stesso vale per le altre due. La `ragione` accanto e'
    # percio' piu' corta di tutte: non c'e' niente da argomentare.
    "guerriero": ("Fighter",
                  "Identita', non accostamento: e' la stessa classe in due "
                  "edizioni. Lo strato di Krynn e' vuoto per dichiarazione "
                  "della fonte (decisione 59, `classi-base-2e`)."),
    "paladino": ("Paladin",
                 "Identita', non accostamento. Da non confondere con i "
                 "Cavalieri della Spada e della Rosa, che stanno sullo "
                 "stesso telaio ma sono ordini di Krynn."),
    "ladro": ("Rogue",
              "Identita', non accostamento. Da non confondere con il Con "
              "Artist, che e' il ladro proprio di Krynn e porta minimi suoi."),
    # ---- lasciate indecise dalla decisione 23 (`principio-del-clone`) ----
    # Ciascuna ha un id nel registro delle questioni aperte (`decisioni.APERTE`)
    # dal 05/09/2026: `chassis-commoner`, `chassis-tinker`,
    # `chassis-sacerdote-eretico`, `chassis-handler`, `chassis-mariner`. Il
    # registro porta l'id e rimanda QUI per la ragione — erano gia' dichiarate,
    # quello che mancava era il modo di citarle da un altro testo.
    "commoner": (None, "Non e' una classe 5e. Da decidere."),
    "tinker": (None, "Non e' una classe 5e. Da decidere."),
    "sacerdote-eretico": (None, "Per definizione non ha potere. Da decidere."),
    "handler": (None, "Rogue senza attacco furtivo: il chassis c'e' ma svuotato. "
                      "Da decidere."),
    "mariner": (None, "Ibrido Fighter/Rogue: nessun candidato pulito. Da decidere."),
}

# Tutti i chassis usati sono trascritti in _srd51.py: Fighter, Wizard, Cleric,
# Paladin, Rogue.

# --------------------------------------------------------------------------
# Stato di conversione dei privilegi di fonte.
# Default: `pending`. La decisione 23 (`principio-del-clone`) autorizza il clone del chassis, non
# l'invenzione di meccanica 5e per i privilegi: quella resta da fare.
#
# IL TERZO CAMPO E' UN RIMANDO, ed e' nato il 04/09/2026 da due incoerenze
# vere su dodici segnalate. Due privilegi della fonte dichiaravano
# `conversion_status: direct` con `mechanics_5e: null`, cioe' dicevano
# insieme «la conversione e' conclusa» e «non c'e' niente»: l'invariante di
# `elemento_5e` — la meccanica manca solo dove la conversione non c'e'
# ancora — risultava violata. Non era un difetto di quei due privilegi. La
# loro meccanica 5e ESISTE e non e' scritta li' perche' e' quella del
# chassis: mancava al campo il modo di dire «sta altrove».
#
# Fra le due strade si e' scelta la seconda:
#   (a) uno stato di conversione nuovo — un termine in piu' nel vocabolario
#       condiviso con mostri, oggetti e modelli, per un caso che riguarda le
#       sole classi e conta due occorrenze. Sarebbe stata la quinta volta che
#       il progetto reinventa lo stesso concetto sotto un nome nuovo.
#   (b) riempire il campo che gia' c'e'. `mechanics_5e` porta il rimando,
#       `direct` torna vero, e il vocabolario condiviso non si muove.
#
# Un rimando e' un DATO e non una nota perche' e' verificabile: il privilegio
# del chassis o sta nella tabella SRD o non ci sta. `_srd51.livello_privilegio`
# risponde, `rimando_a_privilegio()` fallisce in costruzione se il bersaglio
# non esiste, e `verifica_rimandi()` rifa' la prova sui file gia' scritti —
# perche' un rimando che risolve il giorno in cui e' scritto e' esattamente
# la forma di copia che questo progetto ha gia' visto sfasarsi dodici volte.
#
# Il livello NON si scrive qui: si legge dalla tabella SRD (CLAUDE.md 3). La
# nota nemmeno — la prosa del rimando e' derivata da `prosa_rimando()`, e
# quello che la nota diceva in piu' era una domanda aperta, che il 04/09/2026
# e' uscita di qui ed e' entrata nel registro (CONTESTO-PROGETTO.md,
# "Questioni aperte"). Una decisione che vive solo in una nota di campo e'
# una decisione che nessuno prende.
# --------------------------------------------------------------------------

def rimando_a_privilegio(srd_class, name_srd, nome_it):
    """Rimando a UN privilegio del chassis, con il livello letto dalla fonte."""
    livello = R.livello_privilegio(srd_class, name_srd)
    if livello is None:
        raise KeyError(
            f"rimando a un privilegio che il chassis {srd_class} non concede: "
            f"{name_srd!r}. Il bersaglio di un rimando si verifica, non si "
            f"assume: vedi _srd51.TABELLE[{srd_class!r}]['features'].")
    return {"riferimento_a": "privilegio_chassis", "srd_class": srd_class,
            "name_srd": name_srd, "name": nome_it, "level": livello}


def rimando_al_chassis(srd_class):
    """Rimando al chassis INTERO: il privilegio coincide con la classe."""
    if srd_class not in R.TABELLE:
        raise KeyError(f"rimando a un chassis non trascritto: {srd_class!r}")
    return {"riferimento_a": "chassis", "srd_class": srd_class,
            "name_srd": None, "name": None, "level": None}


def prosa_rimando(rim):
    """La nota di un privilegio che rimanda, derivata dal rimando stesso."""
    if rim["riferimento_a"] == "chassis":
        return (f"RIMANDO AL CHASSIS. La classe E' un {rim['srd_class']}: il "
                f"privilegio coincide con la classe stessa e non va "
                f"convertito a parte. La meccanica non e' assente, sta nel "
                f"chassis clonato dalla decisione 23 (`principio-del-clone`).")
    return (f"RIMANDO AL CHASSIS. Il privilegio e' gia' concesso da "
            f"{rim['name']} ({rim['srd_class']} SRD 5.1, "
            f"{rim['level']}° livello): la meccanica non si riscrive qui.")


STATO_PRIVILEGI = {
    ("cavaliere-corona", "Specializzazione nelle armi"): (
        "source_only",
        "Stesso criterio della decisione 17.10 (`pending-krynn`) sul Minotauro: la fonte non "
        "concede un beneficio ma un PERMESSO — la facolta' di usare un "
        "sottosistema 2e ristretto. In un sistema che quel sottosistema non ce "
        "l'ha, il permesso non vale nulla. CONSEGUENZA REGISTRATA: il grado "
        "d'ingresso dell'intero ordine solamnico resta a ZERO privilegi "
        "dichiarati dalla fonte. Non e' un errore da correggere: e' cio' che "
        "dice il manuale, ed e' la ragione per cui serve la decisione 23 (`principio-del-clone`).",
        None),
    ("cavaliere-spada", "Capacita' del paladino"): (
        "direct", None, rimando_al_chassis("Paladin")),
    ("cavaliere-rosa", "Immunita' alla paura"): (
        "direct", None,
        rimando_a_privilegio("Paladin", "Aura of Courage", "Aura di Coraggio")),
}

DEFAULT_PRIVILEGIO = (
    "pending",
    "La decisione 23 (`principio-del-clone`) autorizza il clone del chassis, non l'invenzione di "
    "meccanica 5e per i privilegi della fonte. Da convertire.",
    None)


def stato(class_id, nome):
    """(conversion_status, nota, mechanics_5e) di un privilegio della fonte.

    La nota di un rimando NON sta nella tabella: si deriva dal rimando, cosi'
    che non possa dire una cosa mentre il dato ne dice un'altra."""
    st, nota, rim = STATO_PRIVILEGI.get((class_id, nome), DEFAULT_PRIVILEGIO)
    return st, (nota if nota is not None else prosa_rimando(rim)), rim


def verifica_rimandi(docs):
    """I rimandi dei file gia' scritti risolvono? Lista vuota = si'.

    Ripete sui dati la prova che `rimando_a_privilegio()` fa in costruzione.
    Le due non sono ridondanti: la prima protegge chi genera, la seconda chi
    legge un file generato mesi fa da un elenco SRD che intanto e' cambiato.
    """
    problemi = []
    for d in docs:
        m = d.get("mechanics_5e") or {}
        proprio = ((m.get("chassis") or {}).get("srd_class"))
        for b in (m.get("features") or []):
            rim = b.get("mechanics_5e")
            if not isinstance(rim, dict) or "riferimento_a" not in rim:
                continue
            eti = f"{d['id']}: {b.get('name')}"
            if rim["srd_class"] != proprio:
                problemi.append(
                    f"{eti}: rimanda al chassis {rim['srd_class']} ma la "
                    f"classe sta su {proprio}")
            if rim["riferimento_a"] == "chassis":
                if rim["srd_class"] not in R.TABELLE:
                    problemi.append(f"{eti}: chassis non trascritto")
                continue
            if rim["riferimento_a"] != "privilegio_chassis":
                problemi.append(f"{eti}: rimando di tipo sconosciuto "
                                f"{rim['riferimento_a']!r}")
                continue
            liv = R.livello_privilegio(rim["srd_class"], rim["name_srd"])
            if liv is None:
                problemi.append(
                    f"{eti}: rimanda a {rim['name_srd']!r}, che il chassis "
                    f"{rim['srd_class']} non concede")
            elif liv != rim["level"]:
                problemi.append(
                    f"{eti}: il rimando dice {rim['level']}° livello, la "
                    f"tabella SRD dice {liv}°")
    return problemi


# --------------------------------------------------------------------------
# LE SETTE INCOMPATIBILITA' STRUTTURALI, applicate uguali per tutti.
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# L'EQUIPAGGIAMENTO INIZIALE — decisione 62 (`pacchetto-fisso`).
#
# La scelta e' il PACCHETTO e non il borsello, e questa funzione e' il punto
# in cui la scelta diventa dato. Non inventa niente: l'elenco viene dal
# telaio SRD (`srd51_pacchetti.EQUIPAGGIAMENTO`), che e' trascritto, e le sue
# voci RIFERISCONO il catalogo e i pacchetti per id invece di ricopiarli.
#
# LE OTTO CLASSI SENZA CHASSIS NON HANNO UN ELENCO, e non e' una dimenticanza
# che si tappa con un elenco plausibile: comporre un pacchetto per una classe
# che nessun telaio 5e copre e' una scelta editoriale, e la
# decisione 62 (`pacchetto-fisso`) dice esplicitamente che va PROPOSTA prima
# di essere scritta. `da_comporre: true` e' quel vuoto reso visibile — stessa forma
# dell'`in_sospeso` che la decisione 23 (`principio-del-clone`) usa per i
# chassis mancanti, e per la stessa ragione.
#
# TRE GENERI DI VOCE, e la distinzione conta perche' cambia chi le risolve:
# `oggetto` va letto in dati/oggetti/, `pacchetto` in dati/pacchetti/,
# `scelta` non si risolve affatto — e' un filtro che l'interfaccia deve porre
# come domanda (decisione 35, `repertori-sono-filtri`).
# --------------------------------------------------------------------------

def _slug(nome):
    """Lo stesso slug di build_oggetti/build_pacchetti, senza importarlo:
    quel modulo scrive file, e importarlo da qui accoppierebbe la lettura
    del chassis alla generazione del catalogo."""
    fuori = []
    for ch in nome.lower().replace("'", "").replace(",", ""):
        fuori.append(ch if ch.isalnum() else "-")
    return "-".join(x for x in "".join(fuori).split("-") if x)


def _voce(quantita, nome, genere):
    if genere == PK.PACCHETTO:
        return {"quantita": quantita, "name_srd": nome, "genere": "pacchetto",
                "riferimento": _slug(nome), "filtro": None}
    if genere == PK.CATEGORIA:
        return {"quantita": quantita, "name_srd": nome, "genere": "scelta",
                "riferimento": None, "filtro": PK.SCELTE[nome]["filtro"]}
    return {"quantita": quantita, "name_srd": nome, "genere": "oggetto",
            "riferimento": _slug(nome), "filtro": None}


def equipaggiamento_iniziale(c, s):
    srd, _ = CHASSIS[c["id"]]
    righe = PK.EQUIPAGGIAMENTO.get(srd)
    return {
        "system": "pacchetto_fisso_5e",
        # NON SI RICOPIA LA FONTE NELLO STRATO NOSTRO. Fino al 05/09/2026
        # questi due campi portavano la stringa di `source_2e` per intero —
        # la formula di ricchezza e le regole di equipaggiamento — cioe' la
        # stessa struttura doppia che la
        # decisione 61 (`allineamento-insieme`) ha appena chiuso su
        # `alignment_restriction`, e che la
        # decisione 4 (`limiti-di-livello`) evita da sempre sui
        # limiti di livello: `applied: false` piu' la SEDE, mai il valore
        # duplicato. Chi vuole la formula la legge dove sta.
        "source_wealth": {
            "applied": False,
            "sede": "source_2e.starting_wealth",
            "presente": s.get("starting_wealth") is not None,
            "note": "La formula di ricchezza 2e resta dato di fonte e NON si "
                    "applica: la decisione 62 (`pacchetto-fisso`) sceglie il "
                    "pacchetto, e su questa strada la formula non serve a "
                    "niente. La fonte ne da' una a 4 classi su 20, quindi "
                    "l'altra strada avrebbe dovuto inventarne 16.",
        },
        "constraints": {
            "applied": False,
            "sede": "source_2e.equipment_rules",
            "quante": len(s.get("equipment_rules") or []),
            "note": "Le regole di equipaggiamento della fonte mordono sul "
                    "pacchetto e non sul tiro, ma COME mordano non e' "
                    "deciso: un vincolo come «non puo' portare armature piu' "
                    "pesanti di X» su un pacchetto fisso o e' gia' rispettato "
                    "— e allora non serve — o chiede un pacchetto riscritto "
                    "per quella classe, che e' un pacchetto in piu' da "
                    "comporre. La decisione 62 (`pacchetto-fisso`) lo "
                    "registra come conseguenza non risolta, e finche' non lo "
                    "e' il campo dichiara di non essere applicato invece di "
                    "ricopiare la prosa qui.",
        },
        "telaio": srd,
        "da_comporre": righe is None,
        "scelte": None if righe is None else [
            {"alternative": [{"voci": [_voce(*v) for v in alternativa]}
                             for alternativa in riga]}
            for riga in righe
        ],
        "note": "INCOMPATIBILITA' 5. Pacchetto fisso 5e "
                "(decisione 62, `pacchetto-fisso`). Le regole di "
                "equipaggiamento della fonte diventano vincoli sul "
                "pacchetto, non sul tiro della ricchezza, e la formula di "
                "ricchezza 2e resta in `source_wealth` come dato di fonte "
                "NON applicato — stessa forma della "
                "decisione 4 (`limiti-di-livello`)."
                + ("" if righe is not None else
                   " Questa classe non ha chassis 5e: l'elenco va COMPOSTO, "
                   "e comporlo e' una proposta da portare, non un dato da "
                   "scrivere di propria iniziativa."),
    }


def incompatibilita(c):
    s = c["s2e"]
    prog = s.get("progression") or []
    max_2e = max((p["level"] for p in prog), default=None)
    titoli = [{"level": p["level"], "title": p["title"]}
              for p in prog if p.get("title")]
    gruppo = c["group"]

    # 3 — le cinque categorie 2e mappate sulle sei caratteristiche.
    MAPPA_TS = {
        "Paralisi/Veleno/Magia della Morte": "con",
        "Bacchette/Bastoni/Verghe": "dex",
        "Pietrificazione/Polimorfismo": "con",
        "Soffio": "dex",
        "Incantesimi": "wis",
    }
    # Le due competenze coerenti col gruppo 2e: il gruppo che in 2e era forte
    # su una categoria diventa competente nella caratteristica corrispondente.
    COMPETENZE_GRUPPO = {
        "Warrior": ["str", "con"],
        "Wizard": ["int", "wis"],
        "Priest": ["wis", "cha"],
        "Rogue": ["dex", "int"],
        "Normal": ["dex", "con"],
    }
    wp = s.get("weapon_proficiencies") or {}
    srd, _ = CHASSIS[c["id"]]
    comp = R.COMPETENZE.get(srd) if srd else None

    return {
        "xp_table": {
            "applied": False,
            "note": "INCOMPATIBILITA' 1. Tabella unica 5e per tutti. Le "
                    "progressioni 2e restano in source_2e come dato storico: "
                    + (f"{len(prog)} livelli trascritti." if prog else
                       f"questa classe non ne aveva una propria, rimandava al gruppo {gruppo}."),
        },
        "attack_progression": {
            "system": "proficiency_bonus",
            "values": R.COMPETENZA,
            "note": "INCOMPATIBILITA' 2. Il THAC0 per gruppo sparisce: il bonus "
                    "di competenza e' uguale per chiunque. La differenza fra "
                    "gruppi si esprime con Attacco Extra e competenze.",
        },
        "saving_throws": {
            "system": "ability_saves_5e",
            "mapping_2e": MAPPA_TS,
            "proficient": COMPETENZE_GRUPPO[gruppo],
            "note": "INCOMPATIBILITA' 3. Le cinque categorie 2e sono mappate "
                    "sulle sei caratteristiche; le due competenze discendono "
                    f"dal gruppo 2e ({gruppo}).",
        },
        "weapon_proficiencies": {
            "system": "categorie_5e",
            "forced_equipment": wp.get("required") or [],
            # Le categorie sono la parte che questa nota annunciava dal
            # giorno uno senza mai scriverla: "competenza per categoria" e
            # poi nessuna categoria in nessun campo. Vengono dal chassis,
            # perche' e' il chassis a concedere le competenze 5e (la fonte
            # 2e concedeva slot, che qui non esistono piu').
            "categorie": comp["armi"] if comp else None,
            "note": "INCOMPATIBILITA' 4. Gli slot di competenza spariscono: "
                    "competenza per categoria. Le armi obbligate della fonte "
                    "diventano equipaggiamento iniziale imposto, non slot."
                    + ("" if comp else
                       " Senza chassis non ci sono categorie da concedere: "
                       "questa classe non ha competenze 5e."),
        },
        "armor_proficiencies": {
            "system": "categorie_5e",
            "categorie": comp["armature"] if comp else None,
            "note": "Stessa incompatibilita' 4, lato armature. Le categorie "
                    "nominate qui sono quelle di armor_5e.categoria in "
                    "dati/oggetti/: valida_effetti.py verifica che i due "
                    "estremi combacino, perche' una competenza che nominasse "
                    "una categoria inesistente sarebbe una competenza in "
                    "niente.",
        },
        "skill_proficiencies": {
            "system": "scelta_5e",
            "scelta": comp["abilita"] if comp else None,
            "note": "La fonte 2e dava competenze non-d'arma a slot; la 5e da' "
                    "un numero di abilita' da scegliere dentro una lista. E' "
                    "un FILTRO, non una lista risolta "
                    "(decisione 35, `repertori-sono-filtri`): la scelta vive "
                    "sul personaggio. "
                    "Le 18 abilita' della 5e non hanno ancora una sede "
                    "propria nei dati — RAPPORTO-personaggio §2.4 — quindi "
                    "qui sono nomi italiani, non id.",
        },
        "starting_equipment": equipaggiamento_iniziale(c, s),
        "level_cap": {
            "value": 20,
            "source_max": max_2e,
            "note": "INCOMPATIBILITA' 6. Troncamento al 20°. "
                    + (f"La fonte arrivava al {max_2e}°: i {max_2e - 20} livelli in piu' "
                       f"restano in source_2e." if max_2e and max_2e > 20 else
                       "Questa classe non aveva una tabella propria."),
        },
        "titles": {
            "descriptive_only": True,
            "values": titoli,
            "note": "INCOMPATIBILITA' 7. I titoli di livello si conservano come "
                    "dato descrittivo, mostrati nella scheda, senza effetto "
                    f"meccanico. {len(titoli)} titoli trascritti.",
        },
    }


def features_chassis(c):
    """I privilegi che vengono dal CHASSIS, non dalla fonte di Krynn.

    Stanno in una lista separata da `features` per una ragione che il
    RAPPORTO-personaggio §2.1 ha misurato: i due insiemi hanno provenienza
    diversa e si contano diversamente. I 40 privilegi `pending` sono quelli
    della fonte 2e, in attesa di una resa 5e; questi non sono `pending` —
    non erano mai stati contati affatto, perche' esistevano solo come nomi
    in una colonna di tabella. Mescolarli farebbe sparire proprio la
    distinzione che serve: quanti privilegi restano da CONVERTIRE (fonte) e
    quanti da TRASCRIVERE (chassis).

    Vuota per le classi senza chassis, che e' il modo giusto di dire che
    quelle otto non hanno privilegi 5e di nessun tipo."""
    srd, _ = CHASSIS[c["id"]]
    if srd is None:
        return []
    out = []
    for nome, d in sorted(R.privilegi_chassis(srd).items(),
                          key=lambda kv: (kv[1]["livello"], kv[0])):
        out.append({
            "name": d["nome_it"],
            "name_srd": nome,
            "kind": "privilegio_chassis",
            "source": f"SRD 5.1 — {srd}",
            "level": d["livello"],
            "conversion_status": "direct",
            "mechanics_5e": d["prosa"],
            "effetto": d["effetto"],
            "note": None,
        })
        # Le opzioni di una scelta stanno accanto al privilegio che le offre,
        # non altrove: un `fra: [sei id]` che non risolve a niente e' un
        # filtro senza insieme. Le due che hanno un effetto entrano; le
        # altre quattro restano nomi dentro la scelta, e la differenza si
        # vede confrontando i due elenchi invece di doverla ricordare.
        for oid in (d.get("effetto", {}).get("scelta", {}) or {}).get("fra", []):
            st = R.STILI_COMBATTIMENTO.get(oid)
            if not st:
                continue
            out.append({
                "name": st["nome_it"],
                "name_srd": oid,
                "kind": "opzione_chassis",
                "opzione_di": d["nome_it"],
                "source": f"SRD 5.1 — {srd}",
                "level": d["livello"],
                "conversion_status": "direct",
                "mechanics_5e": st["prosa"],
                "effetto": st["effetto"],
                "note": None,
            })
    return out


def privilegi_chassis_non_trascritti(c):
    """Quanti privilegi il chassis concede senza che se ne abbia la meccanica.

    E' il numero che mancava: `features_pending` contava solo la fonte, e un
    Cavaliere della Corona con zero pending sarebbe rimasto ingiocabile lo
    stesso. Contarli qui li rende visibili nella scheda invece che in una
    lettura del rapporto."""
    srd, _ = CHASSIS[c["id"]]
    if srd is None or srd not in R.TABELLE:
        return None
    scritti = set(R.privilegi_chassis(srd))
    mancanti = []
    for liv, riga in sorted(R.TABELLE[srd]["features"].items()):
        for nome in [x.strip() for x in riga.split(",") if x.strip()]:
            base = nome.split(" (")[0].strip()
            if base == R.ASI or base in scritti:
                continue
            mancanti.append({"level": liv, "name": nome})
    return mancanti


def chassis(c):
    srd, motivo = CHASSIS[c["id"]]
    if srd is None:
        return {
            "srd_class": None,
            "status": "in_sospeso",
            "note": f"{DEC}. Nessun chassis applicato: {motivo}",
            "hit_die": None,
            "saving_throws": None,
            "features_from": None,
        }
    tab = R.TABELLE.get(srd)
    return {
        "srd_class": srd,
        "status": "clonato",
        "note": f"{DEC}. {motivo}",
        "hit_die": tab["hit_dice"] if tab else None,
        "saving_throws": tab["saves"].split(", ") if tab else None,
        "features_from": f"SRD 5.1 — {srd}",
        "table_transcribed": srd in R.TABELLE,
        "table_note": None if srd in R.TABELLE else
                      f"Tabella {srd} non ancora trascritta in _srd51.py: "
                      f"il chassis e' deciso, i privilegi livello per livello no.",
    }
