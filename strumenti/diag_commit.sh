#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Maurizio Acampora
# diag_commit.sh — ciclo canonico di commit per i prodotti di un giro di misura.
#
# Il progetto ha due percorsi di commit, distinti per COSA si committa. Questo è il
# percorso dei prodotti di un giro di misura (referti, script diagnostici); l'altro è
# quello della documentazione governata e del codice applicativo, del gemello
# `doc_commit.sh`.
#
# Esiste per una ragione sola: l'ordine dei comandi non deve più essere scritto a mano.
# L'assistente IA che progettava in chat ha riscritto a mano, in un briefing, la sequenza
# git di questo percorso, con `pull --rebase` in testa, dove fallisce sempre. Lo script del
# gemello non arrivava qui perché questo percorso ha un ciclo proprio: nessun indice,
# `git add` limitato a due percorsi, lo lancia l'assistente che esegue (Claude Code).
#
# Uso:
#   scripts/diag_commit.sh --expect N -m "messaggio" [--deliver <file>]... <file> [<file> ...]
#
#   <file>            prodotto del giro: SOLO sotto docs/report/ o scripts/diag/
#   --expect N        numero esatto di file attesi in stage
#   --deliver <file>  file dell'altro percorso che il giro consegna NON committato (es. codice
#                     applicativo modificato durante il giro, che aspetta il commit di una
#                     persona). Ripetibile. Niente `pull --rebase` a tree sporco, niente
#                     stash, ma `fetch` + verifica che origin/$BRANCH sia già in HEAD.
#
# Ambiente:
#   DIAG_COMMIT_BRANCH  ramo su cui si committa e si pusha (default: main)
#   DIAG_VERIFIER       percorso dello script che verifica i referti (vedi cancello 3);
#                       senza, nessun referto si committa da qui
#   DIAG_PYTHON         interprete che lancia il verificatore (default: .venv/bin/python
#                       sotto la radice del repo)
#
# Contratto del verificatore: riceve il percorso di un referto, riesegue i comandi che il
# referto esibisce ed esce 0 solo se uscita ed exit coincidono con quelli dichiarati nel
# referto; altrimenti esce diverso da 0 e stampa perché. Lo script del verificatore non fa
# parte di questa copia: chi la usa porta il proprio.
#
# Lezione di un ramo rimosso: nel progetto originale lo script committava anche un artefatto
# di prova congelato, ma solo se la decisione che lo registrava era già in HEAD e se le impronte
# del codice a inizio e fine corsa coincidevano con il codice sul disco: un artefatto si
# committa solo se l'ha prodotto il codice che si ha in mano.
#
# Cosa fa, in quest'ordine e senza possibilità di alterarlo:
#   1. CANCELLO di perimetro: ogni file passato sta sotto docs/report/ o scripts/diag/
#   2. CANCELLO sul tree: nulla di modificato o non tracciato oltre ai file passati e
#      a quelli dichiarati con --deliver
#   3. CANCELLO del verificatore: ogni referto passato (docs/report/*.md) passa dal
#      verificatore indicato in DIAG_VERIFIER, che RIESEGUE i comandi esibiti e confronta
#      uscita ed `exit=`. Un blocco difforme, senza exit, non analizzabile o non
#      interpretato ferma qui, a stage vuoto. Se fra i file c'è un referto e DIAG_VERIFIER è
#      vuota o non punta a un file, ci si ferma qui: il cancello resta chiuso.
#      Gira dopo il cancello sul tree (si rieseguono stringhe scritte da un modello: solo su
#      un tree già dichiarato) e prima del git add (si ferma senza nulla da ripulire).
#      L'uscita del verificatore è in terminale per intero: un cancello che ferma senza
#      dire perché insegna ad aggirarlo. Nessun file di uscita dal verificatore da qui: è un
#      prodotto che il giro decide di consegnare, non un effetto collaterale del commit.
#   4. git add esplicito dei soli file passati (mai -A, mai -u)
#   5. mostra git diff --cached --stat
#   6. CANCELLO: il numero di file in stage deve essere esattamente N
#   7. git commit
#   8. senza --deliver: git pull --rebase origin $BRANCH   <-- ad albero pulito, non prima
#      con --deliver:   git fetch origin + origin/$BRANCH deve essere antenato di HEAD
#   9. git push origin $BRANCH
#  10. git status --short: vuoto, oppure ESATTAMENTE le righe dei file in --deliver
#
# Qualunque passo fallisca, la catena si ferma: nessun push parziale.
# Conflitto al rebase su un file che l'assistente non ha scritto: non si risolve, si segnala.

set -euo pipefail

# Ramo su cui si committa e si pusha; si cambia con la variabile d'ambiente DIAG_COMMIT_BRANCH (default: main).
BRANCH="${DIAG_COMMIT_BRANCH:-main}"
PERIMETRO=("docs/report/" "scripts/diag/")
REFERTI_DIR="docs/report/"

muori() { printf '\n[diag_commit] ERRORE: %s\n' "$1" >&2; exit 1; }

EXPECT=""
MSG=""
FILES=()
DELIVER=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --expect)  EXPECT="${2:-}";        shift 2 ;;
    -m)        MSG="${2:-}";           shift 2 ;;
    --deliver) DELIVER+=("${2:-}");    shift 2 ;;
    -*)        muori "opzione sconosciuta: $1" ;;
    *)         FILES+=("$1");          shift ;;
  esac
done

[[ -n "$EXPECT" ]] || muori "manca --expect N (numero di file attesi in stage)"
[[ "$EXPECT" =~ ^[0-9]+$ ]] || muori "--expect vuole un numero, ricevuto: $EXPECT"
[[ -n "$MSG" ]] || muori "manca -m \"messaggio di commit\""

[[ ${#FILES[@]} -gt 0 ]] || muori "nessun file da committare"

# La radice del repo, non la directory corrente.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || muori "$ROOT non e' un repo git"

VERIFICATORE="${DIAG_VERIFIER:-}"
PY="${DIAG_PYTHON:-$ROOT/.venv/bin/python}"

RAMO_CORRENTE="$(git rev-parse --abbrev-ref HEAD)"
[[ "$RAMO_CORRENTE" == "$BRANCH" ]] || muori "ramo corrente '$RAMO_CORRENTE', atteso '$BRANCH'"

# Percorsi normalizzati: relativi alla radice, senza "./" iniziale.
normalizza() { local p="$1"; p="${p#./}"; printf '%s' "$p"; }
for i in "${!FILES[@]}";   do FILES[$i]="$(normalizza "${FILES[$i]}")";     done
for i in "${!DELIVER[@]}"; do DELIVER[$i]="$(normalizza "${DELIVER[$i]}")"; done

in_elenco() { # $1 = percorso, $2... = elenco
  local cerco="$1"; shift
  local x
  for x in "$@"; do [[ "$x" == "$cerco" ]] && return 0; done
  return 1
}

printf '[diag_commit] radice: %s\n' "$ROOT"
printf '[diag_commit] 1/10 cancello di perimetro\n'
for f in "${FILES[@]}"; do
  [[ -e "$f" ]] || muori "file inesistente: $f (percorso relativo alla radice del repo?)"
  ok=0
  for p in "${PERIMETRO[@]}"; do [[ "$f" == "$p"* ]] && ok=1; done
  [[ $ok -eq 1 ]] || muori "fuori perimetro di questo percorso di commit: $f (ammessi solo ${PERIMETRO[*]}) — un file governato non si committa da qui"
done
for d in "${DELIVER[@]}"; do
  [[ -n "$d" ]] || muori "--deliver senza percorso"
  if in_elenco "$d" "${FILES[@]}"; then
    muori "$d e' sia fra i file da committare sia in --deliver: deciderne uno"
  fi
done

printf '[diag_commit] 2/10 cancello sul tree\n'
# Ogni riga di `git status --porcelain` deve riferirsi a un file passato o dichiarato.
# Altrimenti il giro ha sul tree qualcosa che nessuno ha dichiarato: ci si ferma.
FUORI=()
while IFS= read -r riga; do
  [[ -n "$riga" ]] || continue
  percorso="${riga:3}"
  percorso="${percorso##* -> }"   # rinomine: tiene la destinazione
  if ! in_elenco "$percorso" "${FILES[@]}" && ! in_elenco "$percorso" "${DELIVER[@]}"; then
    FUORI+=("$riga")
  fi
done < <(git status --porcelain --untracked-files=all)
if [[ ${#FUORI[@]} -gt 0 ]]; then
  printf '%s\n' "${FUORI[@]}" >&2
  muori "sul tree ci sono modifiche non dichiarate (sopra). Non sono del giro: fermarsi e segnalare, non committarle e non ripulirle"
fi

printf '[diag_commit] 3/10 cancello del verificatore sui referti\n'
REFERTI=()
for f in "${FILES[@]}"; do
  [[ "$f" == "$REFERTI_DIR"*.md ]] && REFERTI+=("$f")
done
if [[ ${#REFERTI[@]} -eq 0 ]]; then
  printf '[diag_commit] nessun referto fra i file passati: il verificatore non ha nulla da rieseguire\n'
else
  [[ -n "$VERIFICATORE" && -f "$VERIFICATORE" ]] || muori "manca il verificatore: imposta DIAG_VERIFIER con il percorso di uno script che, dato un referto, riesegue i comandi esibiti ed esce 0 solo se coincidono (ricevuto: '${VERIFICATORE}'). Senza verificatore nessun referto si committa da qui"
  command -v "$PY" >/dev/null 2>&1 || muori "manca l'interprete $PY: imposta DIAG_PYTHON (default: .venv/bin/python sotto la radice; nessun ripiego su python3 di sistema)"
  for r in "${REFERTI[@]}"; do
    printf '[diag_commit] verificatore su %s\n' "$r"
    if ! "$PY" "$VERIFICATORE" "$r"; then
      muori "il verificatore ha fermato $r (sopra: blocchi difformi, senza exit=, non analizzabili o non interpretati). Nulla in stage, nulla committato. Si corregge il referto — o l'edit che ha reso vera l'uscita esibita — e si rilancia. Un comando irriproducibile si ESCLUDE per nome nel verificatore, con la ragione: non si riscrive il blocco perche' passi"
    fi
  done
fi

printf '[diag_commit] 4/10 git add esplicito\n'
git add -- "${FILES[@]}"

printf '[diag_commit] 5/10 contenuto dello stage\n'
git diff --cached --stat

printf '[diag_commit] 6/10 cancello sul numero di file\n'
IN_STAGE="$(git diff --cached --name-only | wc -l | tr -d ' ')"
if [[ "$IN_STAGE" -ne "$EXPECT" ]]; then
  printf '\n[diag_commit] in stage: %s, attesi: %s\n' "$IN_STAGE" "$EXPECT" >&2
  git diff --cached --name-only >&2
  git reset -q -- "${FILES[@]}" 2>/dev/null || true
  muori "il numero di file in stage non e' quello atteso — nulla e' stato committato, stage ripulito. Uno stage sotto l'atteso vuol dire che un file passato non ha modifiche: leggerlo da disco prima di concludere"
fi

printf '[diag_commit] 7/10 commit\n'
git commit -m "$MSG"

if [[ ${#DELIVER[@]} -eq 0 ]]; then
  printf '[diag_commit] 8/10 pull --rebase (ad albero pulito)\n'
  if ! git pull --rebase origin "$BRANCH"; then
    printf '\n[diag_commit] il rebase si è fermato. Il commit locale esiste, il push NON è stato fatto.\n' >&2
    printf '[diag_commit] se il conflitto e'"'"' su un file che l'"'"'assistente non ha scritto: NON risolverlo, `git rebase --abort` e segnalare nel referto.\n' >&2
    muori "conflitto o rebase interrotto"
  fi
else
  printf '[diag_commit] 8/10 fetch + verifica (eccezione --deliver: niente rebase a tree sporco, niente stash)\n'
  git fetch origin "$BRANCH"
  if ! git merge-base --is-ancestor "origin/$BRANCH" HEAD; then
    printf '\n[diag_commit] origin/%s ha commit che HEAD non contiene. Il commit locale esiste, il push NON è stato fatto.\n' "$BRANCH" >&2
    muori "remoto divergente con file in consegna sul tree: fermarsi e segnalare — il rebase lo fa una persona dopo aver committato i file in consegna"
  fi
  printf '[diag_commit] origin/%s e'"'"' gia'"'"' in HEAD: nulla da tirare, si procede al push. Il commit è già fatto: riportarlo a chi ha chiesto il giro.\n' "$BRANCH"
fi

printf '[diag_commit] 9/10 push\n'
git push origin "$BRANCH"

printf '[diag_commit] 10/10 stato finale\n'
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
  printf '[diag_commit] sul tree restano, come dichiarato, i file in consegna:\n'
  git status --short
fi

printf '[diag_commit] fatto. %s file, ramo %s.\n' "$EXPECT" "$BRANCH"
