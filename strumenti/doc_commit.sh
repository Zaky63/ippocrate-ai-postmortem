#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Maurizio Acampora
# doc_commit.sh — ciclo canonico di commit per la documentazione governata e il codice applicativo.
#
# Il progetto ha due percorsi di commit, distinti per COSA si committa. Questo è il
# percorso della documentazione governata (decisioni, voci di backlog, indici generati,
# documenti) e del codice applicativo. I prodotti di un giro di misura (referti, script
# diagnostici) seguono l'altro percorso, quello del gemello `diag_commit.sh`.
#
# Esiste per una ragione sola: l'ordine dei comandi non deve più essere scritto a mano.
# L'assistente IA che progettava in chat ha proposto quattro volte `git pull --rebase` in testa al ciclo, dove fallisce
# sempre — con le scritture non ancora committate git rifiuta di partire e l'intera
# catena `&&` si ferma. Tre note nel flusso di lavoro scritto non l'hanno impedito.
#
# I tre rami portati dal gemello `diag_commit.sh`, ciascuno adattato a questo percorso
# invece che copiato:
#   - il CANCELLO SUL TREE, che qui gira PRIMA della rigenerazione degli indici e ammette
#     i cinque generati per nome - perche' il flusso raccomandato
#     lancia `doc_index.py` a mano per calcolare l'--expect, e un cancello stretto
#     boccerebbe se stesso;
#   - la RIPULITURA DELLO STAGE all'arresto del cancello --expect, che qui agisce su file
#     passati E indici: lo stage di questo percorso contiene entrambi, e resettare i soli file
#     passati lascerebbe uno stage sporco che SEMBRA pulito a chi controlla;
#   - l'eccezione --deliver, che qui RIFIUTA i percorsi governati (vedi sotto).
#
# Uso:
#   scripts/doc_commit.sh --expect N -m "messaggio" [--deliver <file>]... <file> [<file> ...]
#
#   <file>            artefatto governato da committare: voci, documenti, codice. Puo' essere un file
#                     CANCELLATO dal tree, se e' tracciato in HEAD e non sta sotto docs/decisions/ ne'
#                     docs/backlog/ (le voci non si cancellano: si superano). Il commit porta la
#                     cancellazione; lo script le elenca prima del cancello sul numero.
#   --expect N        numero esatto di file attesi in stage, INDICI COMPRESI
#   --deliver <file>  file che resta sul tree NON committato, tipicamente lavoro
#                     applicativo in attesa di aggiudicazione. Ripetibile. Niente
#                     `pull --rebase` a tree sporco e niente stash: `fetch` + verifica
#                     che origin/$BRANCH sia gia' antenato di HEAD.
#                     RIFIUTATO sotto docs/decisions/ e docs/backlog/: una voce
#                     dichiarata «in consegna» resta sul tree, la rigenerazione la
#                     assorbe negli indici, e il commit porta gli indici SENZA il corpo.
#                     E' una patologia misurata in un caso reale:
#                     `--check` la vede verde qui e fallisce sul server dopo il pull.
#                     Le voci si committano prima del codice, sempre.
#
# Cosa fa, in quest'ordine e senza possibilita' di alterarlo:
#    1. CANCELLO sul tree: nulla di modificato o non tracciato oltre ai file passati,
#       a quelli dichiarati con --deliver e ai cinque indici generati
#    2. rigenera gli indici (doc_index.py)
#    3. git add esplicito dei file passati + degli indici modificati (mai -A, mai -u)
#    4. mostra git diff --cached --stat
#    5. CANCELLO: il numero di file in stage deve essere esattamente N
#    6. doc_index.py --check
#    7. git commit
#    8. senza --deliver: git pull --rebase origin $BRANCH   <-- ad albero pulito, non prima
#       con --deliver:   git fetch origin + origin/$BRANCH antenato di HEAD
#    9. git push origin $BRANCH
#   10. git status --short: vuoto, oppure ESATTAMENTE le righe dei file in --deliver
#
# Qualunque passo fallisca, la catena si ferma: nessun push parziale.
#
# Avvertenza sul passo 6, che NON copre la classe piu' insidiosa: `doc_index.py --check`
# confronta la rigenerazione DA DISCO con i file SU DISCO, quindi entrambi i lati vedono
# un corpo modificato e non committato e il confronto non puo' fallire. Quella classe la
# ferma il passo 1, non il 6.

set -euo pipefail

# Ramo su cui si committa e si pusha; si cambia con la variabile d'ambiente DOC_COMMIT_BRANCH (default: main).
BRANCH="${DOC_COMMIT_BRANCH:-main}"
INDICI=(
  "docs/decisions/INDEX.md"
  "docs/decisions/_ALL_DECISIONS.md"
  "docs/backlog/INDEX.md"
  "docs/backlog/INDEX_CHIUSI.md"   # generato da doc_index.py: va ammesso come gli altri
  "docs/backlog/_ALL_BACKLOG.md"
)
# Domini a indice: un file qui sotto e' un CORPO da cui i generati sono derivati, quindi
# non puo' essere messo «in consegna». Vedi --deliver.
DOMINI_GOVERNATI=("docs/decisions/" "docs/backlog/")

muori() { printf '\n[doc_commit] ERRORE: %s\n' "$1" >&2; exit 1; }

EXPECT=""
MSG=""
FILES=()
DELIVER=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --expect)  EXPECT="${2:-}";     shift 2 ;;
    -m)        MSG="${2:-}";        shift 2 ;;
    --deliver) DELIVER+=("${2:-}"); shift 2 ;;
    -*)        muori "opzione sconosciuta: $1" ;;
    *)         FILES+=("$1");       shift ;;
  esac
done

[[ -n "$EXPECT" ]] || muori "manca --expect N (numero di file attesi in stage, indici compresi)"
[[ "$EXPECT" =~ ^[0-9]+$ ]] || muori "--expect vuole un numero, ricevuto: $EXPECT"
[[ -n "$MSG" ]] || muori "manca -m \"messaggio di commit\""
[[ ${#FILES[@]} -gt 0 ]] || muori "nessun file da committare"

# La radice del repo, non la directory corrente: il cd mancato e' gia' costato una volta.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || muori "$ROOT non e' un repo git"

RAMO_CORRENTE="$(git rev-parse --abbrev-ref HEAD)"
[[ "$RAMO_CORRENTE" == "$BRANCH" ]] || muori "ramo corrente '$RAMO_CORRENTE', atteso '$BRANCH'"

# Percorsi normalizzati: relativi alla radice, senza "./" iniziale — altrimenti il
# confronto col percorso che `git status --porcelain` stampa non aggancia.
normalizza() { local p="$1"; p="${p#./}"; printf '%s' "$p"; }
for i in "${!FILES[@]}";   do FILES[$i]="$(normalizza "${FILES[$i]}")";     done
for i in "${!DELIVER[@]}"; do DELIVER[$i]="$(normalizza "${DELIVER[$i]}")"; done

in_elenco() { # $1 = percorso, $2... = elenco
  local cerco="$1"; shift
  local x
  for x in "$@"; do [[ "$x" == "$cerco" ]] && return 0; done
  return 1
}

CANCELLATI=()
for f in "${FILES[@]}"; do
  [[ -e "$f" ]] && continue
  # Un file assente dal disco e' una cancellazione solo se HEAD lo traccia.
  git cat-file -e "HEAD:$f" 2>/dev/null \
    || muori "file inesistente: $f (percorso relativo alla radice del repo? non e' nemmeno tracciato in HEAD)"
  for g in "${DOMINI_GOVERNATI[@]}"; do
    [[ "$f" == "$g"* ]] && muori "cancellazione rifiutata su $f — le voci di $g non si cancellano: si superano con una voce nuova o si chiudono."
  done
  CANCELLATI+=("$f")
done

for d in "${DELIVER[@]}"; do
  [[ -n "$d" ]] || muori "--deliver senza percorso"
  if in_elenco "$d" "${FILES[@]}"; then
    muori "$d e' sia fra i file da committare sia in --deliver: deciderne uno"
  fi
  for g in "${DOMINI_GOVERNATI[@]}"; do
    [[ "$d" == "$g"* ]] && muori "--deliver rifiutato su $d — e' un corpo di $g, da cui gli indici sono generati. Lasciandolo sul tree, il passo 2 lo assorbe negli indici e il commit porta gli indici SENZA il corpo: stato incoerente che si scopre sul server dopo il pull (caso misurato). Committare prima la voce, poi il resto."
  done
done

printf '[doc_commit] radice: %s\n' "$ROOT"
if [[ ${#CANCELLATI[@]} -gt 0 ]]; then
  printf '[doc_commit] cancellazioni dichiarate (%s): %s\n' "${#CANCELLATI[@]}" "${CANCELLATI[*]}"
fi

printf '[doc_commit] 1/10 cancello sul tree (prima della rigenerazione)\n'
# Ogni riga di `git status --porcelain` deve riferirsi a un file passato, a uno dichiarato
# in --deliver, o a uno dei cinque indici generati. Tutto il resto e' lavoro che nessuno
# ha dichiarato: se resta sul tree, il passo 2 lo fa entrare negli indici senza che il suo
# corpo entri nel commit.
FUORI=()
while IFS= read -r riga; do
  [[ -n "$riga" ]] || continue
  percorso="${riga:3}"
  percorso="${percorso##* -> }"   # rinomine: tiene la destinazione
  if ! in_elenco "$percorso" "${FILES[@]}" \
     && ! in_elenco "$percorso" "${DELIVER[@]}" \
     && ! in_elenco "$percorso" "${INDICI[@]}"; then
    FUORI+=("$riga")
  fi
done < <(git status --porcelain --untracked-files=all)
if [[ ${#FUORI[@]} -gt 0 ]]; then
  printf '%s\n' "${FUORI[@]}" >&2
  muori "sul tree ci sono modifiche non dichiarate (sopra). Se sono corpi di docs/decisions/ o docs/backlog/, vanno committati PRIMA, non lasciati li': gli indici li assorbirebbero. Se sono altro, passarli fra i file o dichiararli con --deliver."
fi

printf '[doc_commit] 2/10 rigenero gli indici\n'
python3 scripts/doc_index.py

printf '[doc_commit] 3/10 git add esplicito\n'
DA_AGGIUNGERE=("${FILES[@]}")
for idx in "${INDICI[@]}"; do
  # solo gli indici realmente modificati: aggiungerne uno pulito falserebbe il cancello.
  # E solo se non gia' passato a mano, per non contarlo due volte.
  if [[ -e "$idx" ]] && ! git diff --quiet -- "$idx" && ! in_elenco "$idx" "${FILES[@]}"; then
    DA_AGGIUNGERE+=("$idx")
  fi
done
git add -- "${DA_AGGIUNGERE[@]}"

printf '[doc_commit] 4/10 contenuto dello stage\n'
git diff --cached --stat

printf '[doc_commit] 5/10 cancello sul numero di file\n'
IN_STAGE="$(git diff --cached --name-only | wc -l | tr -d ' ')"
if [[ "$IN_STAGE" -ne "$EXPECT" ]]; then
  printf '\n[doc_commit] in stage: %s, attesi: %s\n' "$IN_STAGE" "$EXPECT" >&2
  git diff --cached --name-only >&2
  # Ripulitura su TUTTO cio' che questo giro ha messo in scena, indici compresi:
  # resettare i soli file passati lascerebbe uno stage sporco che sembra pulito.
  git reset -q -- "${DA_AGGIUNGERE[@]}" 2>/dev/null || true
  muori "il numero di file in stage non e' quello atteso — nulla e' stato committato, stage ripulito. Uno stage SOTTO l'atteso vuol dire che un file passato non ha modifiche: rileggerlo da disco prima di concludere. Uno stage SOPRA vuol dire che un indice si e' mosso piu' del previsto: leggere l'elenco qui sopra, non alzare il numero."
fi

printf '[doc_commit] 6/10 doc_index.py --check\n'
python3 scripts/doc_index.py --check

printf '[doc_commit] 7/10 commit\n'
git commit -m "$MSG"

if [[ ${#DELIVER[@]} -eq 0 ]]; then
  printf '[doc_commit] 8/10 pull --rebase (ad albero pulito)\n'
  if ! git pull --rebase origin "$BRANCH"; then
    printf '\n[doc_commit] il rebase si è fermato. Il commit locale esiste, il push NON è stato fatto.\n' >&2
    muori "conflitto o rebase interrotto: risolvere a mano, poi 'git push origin $BRANCH'"
  fi
else
  printf '[doc_commit] 8/10 fetch + verifica (eccezione --deliver: niente rebase a tree sporco, niente stash)\n'
  git fetch origin "$BRANCH"
  if ! git merge-base --is-ancestor "origin/$BRANCH" HEAD; then
    printf '\n[doc_commit] origin/%s ha commit che HEAD non contiene. Il commit locale esiste, il push NON è stato fatto.\n' "$BRANCH" >&2
    muori "remoto divergente con file in consegna sul tree: committare i file in consegna e poi rifare il rebase, oppure metterli da parte a mano — non da qui"
  fi
  printf '[doc_commit] origin/%s e'"'"' gia'"'"' in HEAD: nulla da tirare, si procede al push.\n' "$BRANCH"
fi

printf '[doc_commit] 9/10 push\n'
git push origin "$BRANCH"

printf '[doc_commit] 10/10 stato finale\n'
RESIDUO_FUORI=()
while IFS= read -r riga; do
  [[ -n "$riga" ]] || continue
  percorso="${riga:3}"
  percorso="${percorso##* -> }"
  in_elenco "$percorso" "${DELIVER[@]}" || RESIDUO_FUORI+=("$riga")
done < <(git status --porcelain --untracked-files=all)
if [[ ${#RESIDUO_FUORI[@]} -gt 0 ]]; then
  printf '%s\n' "${RESIDUO_FUORI[@]}" >&2
  muori "git status --short non e' vuoto oltre ai file in consegna: qualcosa e' rimasto fuori dal commit"
fi
if [[ ${#DELIVER[@]} -gt 0 ]]; then
  printf '[doc_commit] sul tree restano, come dichiarato, i file in consegna:\n'
  git status --short
fi

printf '[doc_commit] fatto. %s file, ramo %s.\n' "$EXPECT" "$BRANCH"
