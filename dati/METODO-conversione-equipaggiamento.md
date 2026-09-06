# Metodo di conversione — equipaggiamento (SRD 5.1 e 2e → catalogo)

Prescrittivo, non diagnostico: dice COME si decide una voce di
equipaggiamento. Il PERCHÉ delle scelte già fatte sta in
`dati/RAPPORTO-equipaggiamento.md`. Gemello di
`dati/METODO-conversione-mostri.md`, con cui condivide la forma — vincoli,
categorie, procedura — e non i contenuti.

Esiste perché la decisione 62 (`pacchetto-fisso`) ha lasciato sette voci da
«guardare nel merito», e guardarle nel merito una per una avrebbe prodotto
sette giudizi a occhio: non riproducibili, e quindi da rifare alla prossima
voce. Il criterio qui sotto le ha decise tutte e sette, e decide anche quelle
che arriveranno.

## 1. Il criterio

> **UN OGGETTO ESISTE SE IL MOTORE DEVE SAPERNE QUALCOSA.**
>
> La corda che lega il campanello sì, la cassetta delle elemosine no.

Non è un criterio di importanza narrativa né di prezzo. È una sola domanda:
**esiste un conto del sistema che debba attraversare questa voce?** Peso
trasportato, tiro, componente materiale, valore in acciaio, competenza,
ingombro — uno qualunque basta. Se nessuno la attraversa, la voce non diventa
un oggetto.

**Cosa NON significa.** Non significa che la voce sparisce. Una voce che
resta testo si legge sulla scheda con il suo nome e la sua quantità: quello
che le manca è un `id` che nessuno avrebbe risolto. La perdita sarebbe il
contrario — creare un oggetto che nessun conto usa, e poi mantenerlo.

## 2. I tre esiti

Non due. La distinzione fra il primo e il secondo è ciò che impedisce di
creare un doppione del catalogo credendo di colmare un buco.

| esito | quando | conseguenza |
|---|---|---|
| `oggetto` | il motore deve saperne qualcosa | entra in `dati/oggetti/` con un id proprio |
| `equivalenza` | la fonte la nomina **già altrove** con un altro nome | non è una voce nuova: è una trascrizione diversa. Si registra in `EQUIVALENZE` della fonte, e la voce risolve sull'oggetto che esiste |
| `testo` | nessun conto la attraversa | resta nel pacchetto con quantità e nome, `oggetto: null` |

`Vestments` è `Robes`: due parole della stessa fonte per la stessa cosa.
L'unica cosa che mancava davvero erano il prezzo e il peso, che si **leggono
sulla fonte** — non si ricordano, non si stimano. Letti da
`api.open5e.com/v2/items/srd_robes/` il 05/09/2026, con la data accanto al
dato.

## 3. Lo strumento non è il criterio

Per una voce che potrebbe essere un componente materiale, la domanda «il
motore deve saperne qualcosa?» si risolve con una prova sul corpus degli
incantesimi. **La prova giusta non è la prima che viene in mente.**

- Prova ingenua: «un incantesimo la nomina». Promuove anche il sacchetto di
  sabbia — sei incantesimi lo nominano, e nessuno di essi ha bisogno che il
  motore lo sappia, perché il borsello dei componenti lo copre.
- Prova che decide: **la regola 5e del borsello**. Il borsello copre i
  componenti materiali *senza costo*; ciò che porta un costo o viene
  consumato va procurato a parte. Solo di quello il motore deve sapere
  qualcosa.

Con la seconda: incenso 7, sabbia 0. L'incenso diventa oggetto, la sabbia
resta testo.

**Lo scarto fra le due letture si espone, non si nasconde.**
`_voci_di_pacchetto.nominate_ma_testo()` stampa le voci che la prova ingenua
avrebbe promosso, e un `assert` tiene fermo che la sabbia non porti costi. Un
corpus che cambiasse farebbe rumore invece di lasciare marcire il
ragionamento.

Regola generale, di cui questa è un'istanza: **quando una prova approssima un
criterio, si dichiara la prova, si misura lo scarto e lo si assicura con un
invariante.** Una prova senza scarto misurato è un'opinione con un numero
accanto.

## 4. Trascrivere ≠ convertire

Due verbi, due lavori diversi, e confonderli è il modo in cui una voce 2e
finisce nel catalogo con numeri inventati e nessuno che lo dica.

- **TRASCRIVERE** — la fonte è l'SRD 5.1. La voce ha già danno, proprietà,
  categoria, prezzo, peso: si copiano. Le voci nominate dalla
  decisione 62 (`pacchetto-fisso`) sono tutte così. Il rischio qui è la svista, non il giudizio.
- **CONVERTIRE** — la fonte è 2e. Un'arma 2e **non ha** danno 5e, proprietà
  5e né categoria 5e finché qualcuno non gliele dà. Il rischio qui è
  spacciare per fonte ciò che è nostro.

La conversione segue il doppio strato della decisione 7 (`doppio-strato`),
esattamente come i mostri:

1. `source_2e` fedele e immutabile — nome, danno 2e, peso e costo 2e, pagina.
2. `mechanics_5e` dichiaratamente nostro.
3. **L'ancoraggio si dichiara riga per riga.** Ogni arma convertita nomina
   l'arma SRD su cui si appoggia e perché quella: stessa categoria d'uso,
   stesso danno 2e, stessa collocazione. Un ancoraggio assunto e non scritto
   è un numero senza padre.
4. Dove l'ancoraggio non regge, la tensione va in `note`, non nascosta.

**Primo caso registrato**: le tre armi del Marinaio — `Cutlass`,
`Belaying Pin`, `Gaff Hook` — decisione 65 (`equipaggiamento-da-convertire`).
Sono l'eccezione anche in un altro senso: costano tre voci nuove **a
prescindere dal chassis**, quindi non aspettano la questione aperta
(`chassis-mariner`) come le altre composizioni.

## 5. La procedura, per una voce nuova

1. **La fonte la elenca a listino?** Sì → si trascrive, fine.
2. **La fonte la nomina altrove con un altro nome?** Sì → `equivalenza`, e la
   riga va in `EQUIVALENZE` della fonte, non in un caso speciale a valle.
3. **Un conto del sistema deve attraversarla?** Se la risposta ha bisogno di
   una prova (componenti materiali, ingombro, valore), la prova si scrive,
   si esegue sul corpus e si misura lo scarto — §3.
4. Sì → `oggetto`, con `name_it` e la ragione **interpolata dai numeri**, mai
   scritta a mano (CLAUDE.md, punto 3). No → `testo`.
5. L'esito si registra in `dati/_voci_di_pacchetto.py`, che è la sede unica.
   **Il modulo solleva su una voce senza listino che nessuno abbia deciso**:
   non esiste uno stato «da decidere» che sopravviva a una rigenerazione.

## 6. Dove sta cosa

| cosa | dove |
|---|---|
| il criterio e i tre esiti, eseguibili | `dati/_voci_di_pacchetto.py` |
| le voci SRD a listino | `dati/_fonti/srd51_equipaggiamento.py` |
| pacchetti ed equivalenze | `dati/_fonti/srd51_pacchetti.py` |
| generazione del catalogo | `dati/build_oggetti.py` |
| controlli | `dati/valida_oggetti.py`, `dati/valida_pacchetti.py` |
| diagnostica e misure | `dati/analizza_equipaggiamento.py` → `dati/RAPPORTO-equipaggiamento.md` |
