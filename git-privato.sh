#!/usr/bin/env bash
# ==========================================================================
# Wrapper per il repository PRIVATO.
#
# PERCHE' SERVE
#     Una cartella puo' contenere un solo `.git`, e qui ce ne servono due:
#     il pubblico in `.git`, il privato in `.git-private`. Questo script
#     passa GIT_DIR e GIT_WORK_TREE al posto tuo.
#
#         ./git-privato.sh status
#         ./git-privato.sh log --oneline
#         ./git-privato.sh push
#
#     Per non digitarlo ogni volta:  alias gpriv='./git-privato.sh'
#
# PERCHE' UN ELENCO ESPLICITO E NON UN .gitignore
#     Git legge SEMPRE il `.gitignore` della cartella di lavoro, qualunque
#     GIT_DIR si usi, e quel file ha precedenza su `info/exclude`. Il
#     `.gitignore` alla radice serve al repo pubblico ed esclude proprio i
#     dati che il privato deve tracciare: le due regole si combattono.
#
#     Invece di aggirare la precedenza con negazioni fragili, il comando
#     `aggiungi` elenca i percorsi uno per uno e usa `git add -f`. Un file
#     nuovo non entra per caso: entra perche' qualcuno lo ha scritto qui.
#
# COSA STA NEL PRIVATO E COSA NO
#     SI'   i JSON di dati/, che contengono `source_2e` — trascrizione fedele
#           dei manuali — e i moduli che li generano. Circa 1,5 MB che
#           cambiano a ogni decisione: la cronologia serve davvero.
#     NO    Manuali/ (4,7 GB), Testi/ (60 MB, rigenerabili da colstep.py),
#           Estratti/, import/, Musica/. Sono 5 GB che non cambiano mai:
#           vanno in backup, non sotto controllo di versione.
#     NO    cio' che sta gia' nel repo pubblico: niente duplicazioni.
# ==========================================================================
set -euo pipefail
cd "$(dirname "$0")"

export GIT_DIR=.git-private
export GIT_WORK_TREE=.

# Percorsi tracciati dal repo privato. Aggiungerne uno e' una decisione:
# scrivilo qui, non affidarti a una regola generica.
PERCORSI=(
    dati/razze
    dati/classi
    dati/divinita
    dati/mostri
    dati/oggetti
    dati/razze.index.json
    dati/classi.index.json
    dati/divinita.index.json
    dati/mostri.index.json
    dati/mostri.coda.json
    dati/_tratti_phb2e.py
    dati/_tratti_mc.py
    dati/_draconici.py
    dati/_strato5e.py
    dati/build_razze.py
    dati/build_classi.py
    dati/build_divinita.py
    dati/_fonti/progressioni_2e.json
    dati/_fonti/incantesimi_2e.json
    dati/_fonti/divinita_2e.json
    dati/RAPPORTO-bestiario-completo.md
    dati/RAPPORTO-sfere-completo.md
    dati/RAPPORTO-classi-completo.md
    inventario_manuali.tsv
    riscontro
)

case "${1:-}" in
    aggiungi)
        # -f perche' il .gitignore della radice, che serve al pubblico,
        # esclude proprio questi percorsi.
        for p in "${PERCORSI[@]}"; do
            [ -e "$p" ] && git add -f "$p" || true
        done
        git status --short
        ;;
    elenco)
        printf '%s\n' "${PERCORSI[@]}"
        ;;
    "")
        echo "uso: $0 <comando git>   oppure   $0 aggiungi | elenco"
        exit 1
        ;;
    *)
        exec git "$@"
        ;;
esac
