---
name: voce-doc
description: >
  Usare quando si crea o aggiorna una DECISIONE o una voce di BACKLOG in un repo
  che usa il formato un-file-per-voce con doc_index.py e doc_commit.sh. Copre
  dove va il file, quali chiavi di front-matter servono, i vocabolari chiusi, e
  come rigenerare e validare gli indici prima del commit. NON usare per un
  vecchio registro unico tenuto come archivio.
---

<!-- SPDX-License-Identifier: MIT · Copyright (c) 2026 Maurizio Acampora -->

# Creare/aggiornare una voce di documentazione

> Data epistemica: 2026-11-25
>
> Nessun cancello controlla questa skill contro `doc_index.py` e `doc_commit.sh`: quando una
> regola cambia negli script, va aggiornata qui.

Lo stato del progetto vive **file-per-voce**. Ogni decisione e ogni item di backlog è un
file singolo; gli indici sono **autogenerati** e **validati** da `scripts/doc_index.py`.
Se il progetto ha un vecchio registro unico (un monolite di decisioni o di backlog),
resta come archivio e **non si edita**.

## 1. Decisione nuova → `docs/decisions/<id>.md`

- **`<id>` = nome file** (senza `.md`) e deve rispettare `^D-\d{4}-\d{2}-\d{2}-[a-z0-9-]+$`
  (es. `D-2026-07-08-esempio`). Cronologia inversa: la più recente in cima
  all'INDEX (lo ordina lo script, non serve farlo a mano).
- Front-matter **obbligatorio**: `id`, `date` (`YYYY-MM-DD`), `title`.
  Opzionali come **liste inline**: `supersedes: [D-...]`, `fix: [IP-FIX-NN]`.
- Il **corpo è la voce canonica** (contesto, decisione, conseguenze, riferimenti).
  Una volta chiusa è **immutabile**: una rettifica è una **voce nuova** con id
  successivo, oppure una **nota in coda** al corpo — mai una riscrittura. Vale anche
  per una riga che è diventata falsa: si smentisce in coda, non si corregge in loco.

```markdown
---
id: D-2026-07-08-esempio
date: 2026-07-08
title: Titolo conciso della decisione
supersedes: [D-2026-06-01-vecchia]
---

**Contesto**: ...
**Decisione**: ...
**Conseguenze**: ...
**Riferimenti**: ... (i briefing sono effimeri e non versionati: si citano per nome)
```

## 2. Item di backlog → `docs/backlog/<id>.md`

- **`<id>` = nome file** e deve rispettare `^(IP-FIX|IP-OP)-R?\d+[a-z]?$`
  (es. `IP-FIX-1`, `IP-FIX-2b`, `IP-FIX-R01`). I prefissi `IP-FIX` e `IP-OP` sono quelli
  predefiniti di `doc_index.py`: si cambiano in `BACKLOG_PREFIXES` (nello script) e, insieme,
  qui.
- Front-matter **obbligatorio**: `id`, `status`, `severity`, `opened` (`YYYY-MM-DD`).
  - `closed` (`YYYY-MM-DD`) **obbligatorio** se `status` ∈ {`closed`, `superseded`}.
  - `superseded_by: <id>` **obbligatorio** se `status: superseded`, e deve puntare a
    una voce **esistente** (lo script lo verifica). Chiave **singola**, non lista.
  - Opzionale: `decisions: [D-...]` (lista inline).
- **Lo stato vive SOLO nel front-matter.** Vocabolari **chiusi** (qualsiasi altro
  valore fa fallire `--check`):
  - `status`: `open` · `deferred` · `closed` · `superseded`
  - `severity`: `alta` · `media` · `bassa`
- Aggiornare un item = **editare il suo file** (di solito solo il front-matter).
  Il corpo è diario storico: si può appendere, non riscrivere il passato.

**Quale stato scegliere** (il vocabolario è volutamente di quattro valori, non di più):

| stato | quando |
|---|---|
| `open` | non finita. È il default, e include «cominciata ma non conclusa»: quello lo dice il corpo, non il front-matter |
| `deferred` | parcheggiata **deliberatamente**. Chi la mette dichiara nel corpo la **condizione di ritorno** |
| `closed` | finita. Il perché sta nel corpo |
| `superseded` | la voce finisce **ma la materia continua a essere tracciata in un'altra voce nominata**. Non «è stata smentita», non «il fatto è stato risolto altrove»: la domanda è *chi arriva qui deve andare a leggere da un'altra parte?* Se la risposta è no, è `closed` |

Nel backlog il puntatore (`superseded_by`) va **sulla voce che finisce**, mai sulla
successiva: un legame da scrivere su un file diverso da quello che si sta modificando, in
pratica, non viene scritto (è un caso osservato su un backlog reale). Per le decisioni vale
il contrario, e per la stessa ragione: `supersedes` sta sulla voce **nuova**, perché quella
superata è chiusa e non si tocca più.

```markdown
---
id: IP-FIX-1
status: open
severity: media
opened: 2026-07-08
---

Descrizione del problema, diario, note. (Nessun `[status]` nell'header — lo stato
è nel front-matter.)
```

## 3. Dopo OGNI modifica a `decisions/` o `backlog/` (obbligatorio)

Nello **stesso giro**, prima del push:

```bash
python3 scripts/doc_index.py            # rigenera INDEX.md, INDEX_CHIUSI.md + _ALL_*.md (5 file)
python3 scripts/doc_index.py --check    # deve stampare "--check OK" ed uscire 0
```

`--check` fallisce (exit 1) e blocca se: valore di vocabolario illegale, `id` ≠ nome
file, `id` che non rispetta il formato, chiave obbligatoria mancante, data non ISO o non
valida, `closed` mancante su `closed`/`superseded`, `superseded_by` mancante su
`superseded` o che punta a una voce inesistente, id duplicato, front-matter mancante o
non chiuso, chiave-lista non scritta come lista inline `[a, b]`. La validazione fallisce
anche senza `--check`: con errori, lo script non scrive niente. **Non editare a mano** `INDEX.md`/`_ALL_*.md` (sono autogenerati) né un
eventuale vecchio registro unico archiviato.

**Che cosa si muove, e perché** (misurato su un caso reale). A ogni edit di una
voce — anche una nota in coda, anche un carattere, a `status` invariato — si muovono
**tutti** gli autogenerati del dominio: `_ALL_*.md` perché concatena i file delle voci,
front-matter compreso; `INDEX.md` e
`INDEX_CHIUSI.md` perché la riga `<!-- source-hash: … -->` in testa è un'impronta sui
byte grezzi di tutte le voci (`doc_index.py`, funzione `source_hash`). Quindi l'atteso di
un commit di sola prosa è «voci + tutti gli indici del dominio», e un cancello scritto
come «nessun `INDEX` si muove perché nessuno stato è cambiato» è falso per
costruzione. `N` si misura comunque con `git status --short --untracked-files=all`, non
da questa regola.

**Due cancelli, un solo codice d'uscita.** `--check` verifica *anche* che i cinque
generati su disco coincidano con la rigenerazione. Quindi un `--check` rosso può
significare due cose diverse: front-matter non valido, **oppure** indici non
rigenerati dopo l'ultima modifica. Il messaggio le distingue — leggerlo, invece di
attribuire il rosso alla prima ipotesi. In particolare, chi aggiunge un file di prova
per esercitare un controllo deve **rigenerare prima di lanciare `--check`**, altrimenti
vede scattare il cancello sbagliato.

## 4. Commit

**Non si scrivono sequenze git a mano.** Il progetto ha due percorsi di commit, distinti
per cosa si committa. Quello della documentazione governata (voci, indici, documenti) e del
codice applicativo passa da:

```bash
scripts/doc_commit.sh --expect N -m "docs: <descrizione>" <file> [<file> ...]
```

Lo script contiene l'ordine dei comandi e i suoi cancelli: stato dell'albero prima
della rigenerazione, `git add` esplicito dei soli file passati più gli indici che si
sono davvero mossi, conteggio dello stage contro `N`, `--check`, commit, e **solo
allora** `pull --rebase` ad albero pulito, poi push, sul ramo indicato da
`DOC_COMMIT_BRANCH` (default `main`). Con `--deliver` (sotto) il `pull --rebase` non si fa:
lo script fa `fetch` e verifica che il remoto sia già contenuto in HEAD, perché un rebase a
tree sporco fallirebbe.

- **`N` si misura, non si stima**: lanciare `python3 scripts/doc_index.py` e
  `git status --short --untracked-files=all`, contare le righe, usare quel numero. Senza
  `--untracked-files=all` git mostra una cartella nuova come una riga sola, e `N` esce
  sottostimato. Se il cancello si ferma,
  leggere l'elenco che stampa — **non alzare `N`**.
- **`git pull --rebase` in testa a un ciclo fallisce sempre** (con le scritture non
  committate git rifiuta di partire): è la ragione per cui lo script esiste.
- File di lavoro applicativo che devono **restare** sull'albero si dichiarano con
  `--deliver <file>`, **mai** sotto `docs/decisions/` o `docs/backlog/`: una voce
  lasciata sul tree verrebbe assorbita negli indici e il commit porterebbe gli indici
  senza il corpo.
- **Voci prima del codice**: la decisione o l'item entra nel ramo in un commit, il
  codice che la implementa nel successivo.
- Il percorso gemello (referti in `docs/report/`, script in `scripts/diag/`) passa invece
  da `scripts/diag_commit.sh` (ramo: `DIAG_COMMIT_BRANCH`), e lo lancia Claude Code.

L'unica altra riga `git` ammessa è una **lettura** (`git status`, `git diff`,
`git log`) usata per misurare. Se una situazione sembra richiedere una sequenza
manuale, leggere prima il sorgente dello script: quasi sempre la copre già.

La **decisione** di aggiungere/chiudere una voce resta a una persona; l'assistente in chat
redige e valida; Claude Code committa. Claude Code può anche **redigere** le voci di
decisione che registrano un esito già ratificato in chat.
