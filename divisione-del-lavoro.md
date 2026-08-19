# Divisione del lavoro

*19 agosto 2026. Sostituisce `stato-lavoro-cowork.md`: quel nome descriveva un
handoff verso Cowork che non è più la forma del lavoro. Il contenuto storico
resta in cronologia git, non qui.*

## Perché è cambiata

L'ambiente con accesso di rete (questo) ha superato un test di lettura delle
immagini di pagina con esito noto in anticipo: rendere pagina 87 dell'MC
Dragonlance Appendix, leggerla, e riportare titolo, resistenza magica e
struttura dello statblock. Il test è stato superato nel modo che conta di
più — leggendo la pagina *sbagliata* per primo (87 invece di 88, per uno
scarto di convenzione fra indice PDF 0-based e strumenti di rendering
1-based), accorgendosi da solo dell'errore, e correggendolo confrontando
l'immagine con il testo estratto. Un ambiente che non sa leggere le immagini
non avrebbe potuto scoprire quello scarto: è visibile solo mettendo a
confronto i due.

Da questo momento il lavoro che richiede di leggere un manuale — non solo di
elaborare dati già estratti — si consolida qui invece di restare diviso.

## Chi fa cosa, adesso

**Questo ambiente** (accesso di rete, lettura di immagini): rete, git,
download di fonti esterne, lettura di PDF e immagini di pagina, verifica di
trascrizioni sulle immagini, generatori e rapporti, conversioni 2e→5e,
qualunque compito da riga di comando.

**Cowork**: **solo OCR di massa**, se serve — le 22 scansioni ancora in coda
in `ocr_queue.txt`, dove conta il volume e non la precisione pagina per
pagina. Non tocca git: i commit restano qui. Non legge PDF per verificare
trascrizioni: quello è lavoro per questo ambiente, ora che sa farlo.

## Se la divisione cambia ancora

Il criterio per capire chi fa cosa non è "chi è più comodo usare", è "chi può
verificare l'affermazione che sta facendo". Un compito che richiede di
leggere un'immagine di pagina per sapere se un dato è corretto va qui. Un
compito che richiede di macinare volume senza bisogno di precisione pagina
per pagina (l'OCR di uno scanner) può restare a Cowork.
