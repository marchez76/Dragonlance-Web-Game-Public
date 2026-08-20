# Metodo di conversione — bestiario di Krynn (2e → 5e)

Prescrittivo, non diagnostico: dice COME convertire. Il PERCHÉ di ogni scelta
è in `dati/RAPPORTO-bestiario.md` — leggerlo una volta, poi usare questo per
ogni voce successiva. Regole confermate finora in
`feedback_conversione_bestiario.md` (memoria di sessione): questo documento
le riorganizza per l'uso, non le sostituisce.

## 1. I tre vincoli

1. **Ordinamento conservato, ma solo se si conserva il ruolo.** CA e potenza
   relativa 2e si possono portare in 5e finché la creatura resta quello che
   era in combattimento. Verificarlo *davvero* per ogni voce, non darlo per
   scontato: sul Kapak il ruolo era cambiato (assassino debole → duellante
   avvelenatore) e l'ordinamento si è rotto (GS 3 invece che il GS più basso
   previsto). Quando diverge, scrivere `ruolo_2e`/`ruolo_note`.
2. **I bonus numerici da tradurre in vantaggio, non gli effetti alla morte
   in sé.** Il vincolo riguarda cose come "+1 ai TS contro paura" → vantaggio
   (kender, Traag). Non si applica per riempire un vuoto che la fonte lascia
   deliberatamente vuoto: se il Traag "si scioglie in una pozza senza altro
   effetto", non si inventa un TS per farlo somigliare ai draconici veri.
3. **Danno per round almeno raddoppiato** rispetto al 2e (minimo osservato
   sui cinque draconici: ×1.6). Se sul caso specifico non regge, dichiarare
   la tensione nel campo `note`, non nasconderla.

## 2. Le categorie di conversione

- **`direct`, a indicazione di fonte** (la più solida, cercare SEMPRE prima
  delle altre): il testo 2e nomina o descrive l'equivalente 5e. Traag (la
  fonte cita la reach → lancia), Ogre di Krynn ("physically resemble the
  ogres of other worlds" → adozione diretta dell'Ogre SRD), Horax (il
  freddo "ha l'effetto di un incantesimo slow" → si copia *slow*),
  Shadowperson (l'ESP dichiarato di 2° livello → *detect thoughts*).
- **`direct`, per scelta nostra**: il 5e ha già un idioma adatto ma la fonte
  non lo nomina con quelle parole (es. "colpibile solo da armi magiche" →
  resistenza alle armi non magiche).
- **`adapted`, per analogia SRD singola**: un solo mostro SRD basta.
  Thanoi ≈ Merrow.
- **`adapted`, per analogia composta**: nessun mostro SRD singolo replica il
  profilo, si compone da più di uno. Kyrie = Giant Eagle (volo, CA) +
  Druid (PF, incantesimi minori).
- **Identità dichiarata dalla fonte**: quando il testo dice esplicitamente
  che la creatura è fisicamente uguale a una creatura standard, si adotta
  l'SRD di peso — non è pigrizia, è la conversione fedele. Ma cercare OGNI
  divergenza che la fonte dichiara e applicarla anche se scomoda (l'Ogre di
  Krynn non ha armi da tiro, perché la fonte dice che le evitano per
  cultura).

## 3. Regole ferme

- Una capacità che la fonte **dichiara** ma senza resa 5e evidente va
  `pending`, **mai omessa in silenzio** — vale per incantesimi, tratti e
  varianti/sottospecie.
- **I Dadi Vita non bastano a classificare una voce, e nemmeno i PE da
  soli**: leggere lo statblock per intero prima di assegnare fascia o GS.
  Quando DV e XP divergono dalla fascia presunta, è il segnale che impone
  la lettura completa, non il verdetto.
- Prima di leggere una voce, cercare **"See below"** e le sue forme
  equivalenti (`Special`, `Varies`/`Variable`, `As creature or person
  mimicked`, o una clausola di `SPECIAL ATTACKS/DEFENSES` senza numero
  proprio) su tutti i campi di combattimento — non su `TREASURE`/
  `NO. APPEARING`, che restano dati di mondo. Se presente, la lettura
  completa non è opzionale.
- Il campo `raw` (e qualunque altro campo) può essere **omesso (null)** se
  un filtro automatico ne blocca la scrittura: si aggiunge una nota con
  voce e pagina per la riverifica, non si riformula per aggirare il filtro.
- **Resistenza magica**: si registra in `magic_resistance_2e` con
  `applied: false` (decisione 27, gruppo C — rinviata alla Fase 2), mai
  applicata alla scheda.
- **Il riscontro 3.5** (`riscontro/3.5/`) è un indice, non una fonte: dice
  DOVE guardare per verificare una lettura già fatta sul 2e, non fornisce
  contenuto. Si consulta DOPO aver letto il 2e per intero, mai per copiarne
  la meccanica (spesso è più morbido del 2e).
- **Creatura contro entità** (decisione 32): nome proprio e storia propria →
  entità, fuori dal bestiario. Tipo/procedura ripetibile, anche se potente o
  legato a un oggetto magico → creatura, si converte come le altre.
  "Legato a un oggetto" non equivale a "unico".

## 4. La procedura, passo per passo

Praticata su undici conversioni (`dati/mostri/`); questi sono i passi, non
una checklist burocratica.

1. Estrarre il blocco `CLIMATE/TERRAIN`…`XP VALUE` per intero, non solo
   l'intestazione o il nome della voce.
2. Cercare "See below" e le sue forme equivalenti (regola ferma, sopra); se
   presenti, leggere subito la prosa collegata (`Combat`/`Habitat & Society`
   /`Ecology`).
3. Confrontare DV e XP con la fascia presunta; se divergono, rileggere
   prima di fissarla.
4. Verificare creatura contro entità.
5. Cercare un'indicazione di fonte esplicita (categoria 2 sopra) prima di
   cercare un analogo SRD per conto nostro.
6. Se serve un analogo, sceglierlo per **ruolo**, poi verificare che il
   ruolo 2e coincida col ruolo 5e prima di fidarsi dell'ordinamento CA/PE
   (vincolo 1).
7. Assegnare CA/PF dall'analogo o dalla mediana SRD del GS presunto; danno
   per round almeno raddoppiato (vincolo 3).
8. Se la fonte dichiara un effetto alla morte o identitario, riscriverlo con
   un TS (vincolo 2) — mai se la fonte dichiara l'assenza dell'effetto.
9. Registrare ogni capacità dichiarata con uno stato di conversione: mai un
   buco silenzioso.
10. Compilare `morale_2e` (destinazione `ia_combattimento`) e
    `world_data_2e` (destinazione `generatore_incontri`) dai gruppi A/B
    della decisione 27.
11. Validare contro `dati/schema/mostro.schema.json`, aggiungere la voce a
    `dati/mostri.index.json`.

## 5. Le categorie aperte

Due tipi di voce che questo metodo non copre ancora, perché presuppongono
uno statblock fisso da convertire una volta sola:

- **Creature-modello** (Dreamshadow, Spectral Minion): ogni campo della
  scheda 2e è dichiarato "as creature or person mimicked" o "quelli della
  vita precedente" — non ha statistiche proprie, le eredita da un
  bersaglio. Serve un pacchetto di regole che copia un bersaglio, non un
  singolo statblock: la conversione è di un meccanismo, non di un valore.
- **Famiglie di statblock** (Tylor): la fonte dà una tabella di più
  categorie d'età con DV/CA/capacità diverse per ciascuna, sullo stesso
  modello degli age category dei draghi. Serve più di un GS: una mini-
  famiglia di statblock imparentati, non una conversione singola.

Entrambe restano `pending` di metodo, non solo di contenuto, finché non si
decide la forma dello schema che le copre.
