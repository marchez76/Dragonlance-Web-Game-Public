#!/usr/bin/env python3
"""
Motore OCR incrementale a blocchi.

Il sandbox termina ogni processo alla fine della chiamata bash, quindi l'OCR
non puo' girare come job continuo: questo script lavora per un budget di
secondi e poi esce, salvando lo stato. Rilanciandolo riprende esattamente da
dove si era fermato.

    python3 ocrstep.py [budget_secondi]

Stato:
    /tmp/ocrpages/<slug>/p0001.txt      testo per singola pagina (disco VM)
    Estratti/<percorso>.txt.partial     mirror persistente (cartella utente)
    Estratti/<percorso>.txt             file finale, a manuale completato
    Estratti/<percorso>.ocrdone         marcatore di completamento
"""
import os, re, sys, time, glob, subprocess, shutil

# Il percorso della sessione cambia a ogni avvio del sandbox: si ricava dalla
# posizione dello script invece di cablarlo, altrimenti smette di funzionare
# alla sessione successiva.
BASE     = os.path.dirname(os.path.abspath(__file__))
MANUALI  = f"{BASE}/Manuali"
ESTRATTI = f"{BASE}/Estratti"
QUEUE    = f"{BASE}/ocr_queue.txt"
PAGEDIR  = "/tmp/ocrpages"
DPI      = 200
BATCH    = 16          # pagine renderizzate per invocazione di pdftoppm
                       # (sui PDF grossi ogni invocazione ri-analizza il file:
                       #  blocchi ampi ammortizzano quel costo)
WORKERS  = 2

BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 38.0
T0 = time.time()
left = lambda: BUDGET - (time.time() - T0)


def slug(rel):
    return re.sub(r"[^A-Za-z0-9]+", "_", rel[:-4]).strip("_")


def load_queue():
    """Legge ocr_queue.txt tollerando i due formati che si sono succeduti.

    La versione originale scriveva "<percorso>\\t<pagine>"; indicizza.py ora
    scrive "<percorso>\\t<MB> MB" e antepone righe di commento. Il secondo
    campo serve solo a titolo indicativo, quindi si estrae il primo numero
    disponibile e non si fallisce se manca."""
    out = []
    for line in open(QUEUE):
        line = line.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parti = line.split("\t")
        rel = parti[0].strip()
        num = 0
        if len(parti) > 1:
            m = re.search(r"\d+", parti[1])
            if m:
                num = int(m.group(0))
        out.append((rel, num))
    return out


def done_pages(sl):
    d = f"{PAGEDIR}/{sl}"
    if not os.path.isdir(d):
        return set()
    return {int(f[1:5]) for f in os.listdir(d) if re.fullmatch(r"p\d{4}\.txt", f)}


def recover_from_partial(rel, sl):
    """Se la VM si e' resettata, ricostruisce le pagine dal mirror .partial."""
    part = f"{ESTRATTI}/{rel[:-4]}.txt.partial"
    d = f"{PAGEDIR}/{sl}"
    if not os.path.isfile(part) or os.path.isdir(d):
        return
    os.makedirs(d, exist_ok=True)
    chunks = re.split(r"\n=== \[pag\. (\d+)\] ===\n", open(part, errors="ignore").read())
    for i in range(1, len(chunks) - 1, 2):
        open(f"{d}/p{int(chunks[i]):04d}.txt", "w").write(chunks[i + 1])


def write_mirror(rel, sl, total):
    d = f"{PAGEDIR}/{sl}"
    got = sorted(done_pages(sl))
    body = "".join(
        f"\n=== [pag. {p}] ===\n" + open(f"{d}/p{p:04d}.txt", errors="ignore").read()
        for p in got
    )
    target = f"{ESTRATTI}/{rel[:-4]}.txt"
    os.makedirs(os.path.dirname(target), exist_ok=True)
    if len(got) >= total:
        open(target, "w").write(body)
        open(target[:-4] + ".ocrdone", "w").write(f"{len(got)} pagine\n")
        # il mirror di lavoro non serve piu': il .txt finale lo sostituisce
        try:
            os.remove(target + ".partial")
        except OSError:
            pass
        return True
    open(target + ".partial", "w").write(body)
    return False


def ocr_batch(rel, sl, pages):
    """Renderizza e OCR-izza un gruppo di pagine contigue."""
    src = f"{MANUALI}/{rel}"
    d = f"{PAGEDIR}/{sl}"
    os.makedirs(d, exist_ok=True)
    tmp = f"/tmp/ocrwork/{sl}"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)
    lo, hi = pages[0], pages[-1]
    subprocess.run(["pdftoppm", "-r", str(DPI), "-gray", "-f", str(lo), "-l", str(hi),
                    src, f"{tmp}/pg"], capture_output=True, timeout=120)
    imgs = sorted(glob.glob(f"{tmp}/pg*.pgm"))
    env = dict(os.environ, OMP_THREAD_LIMIT="1")
    running, done = [], 0
    for img in imgs:
        n = int(re.search(r"pg-(\d+)\.pgm$", img).group(1))
        if n in done_pages(sl):
            os.remove(img); continue
        p = subprocess.Popen(["tesseract", img, f"{d}/p{n:04d}", "--psm", "3", "-l", "eng"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
        running.append((p, img))
        if len(running) >= WORKERS:
            q, qi = running.pop(0); q.wait(); os.remove(qi); done += 1
        if left() < 3:
            break
    for q, qi in running:
        q.wait()
        try: os.remove(qi)
        except OSError: pass
        done += 1
    shutil.rmtree(tmp, ignore_errors=True)
    return done


def main():
    os.makedirs(PAGEDIR, exist_ok=True)
    queue = load_queue()
    report, total_new = [], 0

    for rel, total in queue:
        if os.path.isfile(f"{ESTRATTI}/{rel[:-4]}.ocrdone"):
            continue
        if left() < 6:
            break
        sl = slug(rel)
        recover_from_partial(rel, sl)
        have = done_pages(sl)
        missing = [p for p in range(1, total + 1) if p not in have]
        if not missing:
            write_mirror(rel, sl, total)
            report.append(f"COMPLETATO {rel} ({total} pg)")
            continue

        new = 0
        while missing and left() > 6:
            batch = missing[:BATCH]
            # solo pagine contigue, altrimenti pdftoppm renderizza il buco
            contig = [batch[0]]
            for p in batch[1:]:
                if p == contig[-1] + 1:
                    contig.append(p)
                else:
                    break
            new += ocr_batch(rel, sl, contig)
            have = done_pages(sl)
            missing = [p for p in range(1, total + 1) if p not in have]

        total_new += new
        fin = write_mirror(rel, sl, total)
        got = len(done_pages(sl))
        report.append(
            f"{'COMPLETATO' if fin else 'in corso   '} {rel}: {got}/{total} pg (+{new})"
        )
        if not fin:
            break

    # riepilogo globale
    q_tot_pg = sum(p for _, p in queue)
    q_done_pg = 0
    for rel, total in queue:
        if os.path.isfile(f"{ESTRATTI}/{rel[:-4]}.ocrdone"):
            q_done_pg += total
        else:
            q_done_pg += len(done_pages(slug(rel)))
    el = time.time() - T0
    print("\n".join(report) if report else "nulla da fare")
    print(f"--- {total_new} pagine in {el:.0f}s"
          f"{f' ({el/total_new:.2f} s/pag)' if total_new else ''} ---")
    print(f"AVANZAMENTO TOTALE: {q_done_pg}/{q_tot_pg} pagine "
          f"({q_done_pg*100.0/q_tot_pg:.1f}%)")


if __name__ == "__main__":
    main()
