# Gli strumenti

Questa cartella raccoglie gli strumenti nati lavorando a ippocrate.ai, ripuliti da tutto ciò che riguardava solo quel
progetto. Lo studio racconta perché sono nati (capitolo 2) e che cosa resta del progetto (capitolo 10); qui si dice
come si usano.

| strumento | che cosa fa |
|---|---|
| [`doc_index.py`](./doc_index.py) | rigenera gli indici di decisioni e backlog a partire dai file delle singole voci, e con `--check` dice se gli indici salvati sono rimasti indietro |
| [`doc_commit.sh`](./doc_commit.sh) | fa i commit di voci, indici, documenti e codice in un ordine fisso, e si ferma se i file in stage non sono quelli attesi |
| [`diag_commit.sh`](./diag_commit.sh) | il gemello per i prodotti di una misura: referti e script diagnostici, con un cancello che fa rieseguire i comandi del referto prima del commit |
| [`skill/voce-doc/`](./skill/voce-doc/SKILL.md) | le istruzioni per Claude Code su come si scrive, si aggiorna e si committa una voce |
| [`cc-bridge/`](./cc-bridge/README.md) | un server MCP in un solo file Python: dalla chat di Claude si lancia e si segue un lavoro di Claude Code sul proprio computer |

Servono Python 3, bash 4.4 o successivo e git; nient'altro. Li abbiamo provati con Python 3.12 e bash 5.2, su Linux
(anche in WSL); con la bash 3.2 che macOS installa di serie gli script di commit possono fermarsi su una variabile non
definita. Per cc-bridge servono anche WSL2, Claude Code e Claude
Desktop: tutto è spiegato nel suo README.

Il codice è distribuito con licenza MIT ([`LICENSE`](./LICENSE)); il testo dello studio con licenza CC BY 4.0.

## Le convenzioni, in una pagina

Gli strumenti danno per scontate poche regole. Sono le stesse che abbiamo usato per otto mesi.

**Un file per voce.** Le decisioni stanno in `docs/decisions/`, una per file; le voci di backlog in `docs/backlog/`,
una per file. Il nome del file, senza `.md`, è l'id della voce:

- decisione: `D-AAAA-MM-GG-parole-chiave`, per esempio `D-2026-01-24-commit-con-script`;
- voce di backlog: un prefisso e un numero, per esempio `IP-FIX-2`. I prefissi predefiniti sono `IP-FIX` e `IP-OP`, e
  si cambiano nella costante `BACKLOG_PREFIXES` di `doc_index.py`.

**Una testata semplice.** In cima a ogni file c'è un blocco fra due righe `---`, con una chiave per riga. Le liste si
scrivono su una riga sola, fra parentesi quadre.

| | chiavi obbligatorie | chiavi facoltative |
|---|---|---|
| decisione | `id`, `date`, `title` | `supersedes: [D-…]`, `fix: [IP-FIX-…]` |
| voce di backlog | `id`, `status`, `severity`, `opened` | `closed`, `superseded_by`, `decisions: [D-…]`, `title` |

`status` vale `open`, `deferred`, `closed` o `superseded`; `severity` vale `alta`, `media` o `bassa`. Una voce chiusa
o superata vuole la data `closed`; una voce superata vuole anche `superseded_by`, che deve puntare a una voce
esistente. Le date sono nella forma `AAAA-MM-GG`. Un valore fuori da questi elenchi ferma lo script.

**Una voce chiusa non si riscrive.** Se una decisione cambia, se ne scrive una nuova che la supera (`supersedes`). Se
una riga diventa falsa, si smentisce con una nota in coda. Il registro serve proprio perché il passato resta com'era.

**Gli indici non si scrivono a mano.** Li genera `doc_index.py`: cinque file, che possono stare in un commit insieme
alle voci da cui nascono.

**Due percorsi di commit**, distinti per che cosa si committa. Voci, indici, documenti e codice passano da
`doc_commit.sh`. Referti (`docs/report/`) e script di misura (`scripts/diag/`) passano da `diag_commit.sh`. Le voci si
committano prima del codice che le attua.

**Chi fa che cosa.** Da noi una persona decideva, l'assistente in chat scriveva le voci e i briefing, e Claude Code
eseguiva e committava. Gli strumenti non lo impongono: funzionano anche se fate tutto da soli.

## Una prova in cinque minuti

Questi comandi creano un repository di prova in `/tmp`, con un remoto finto accanto, e vi fanno usare i tre script
sulle voci della cartella [`esempio/`](./esempio/). Non toccano nient'altro. Servono un terminale Linux (anche WSL) e
git configurato con nome ed email.

```bash
# dove avete scaricato questo repository
STRUMENTI=/percorso/di/ippocrate-ai-postmortem/strumenti

# il repository di prova e il suo remoto finto
mkdir -p /tmp/prova-strumenti && cd /tmp/prova-strumenti
git init -q --bare remoto.git
git clone -q remoto.git lavoro && cd lavoro
git checkout -q -b main

# gli script e le voci d'esempio
mkdir -p scripts
cp "$STRUMENTI"/doc_index.py "$STRUMENTI"/doc_commit.sh "$STRUMENTI"/diag_commit.sh scripts/
chmod +x scripts/*.sh
cp -r "$STRUMENTI"/esempio/docs .

# gli indici: si generano, e --check dice se sono aggiornati
python3 scripts/doc_index.py
python3 scripts/doc_index.py --check

# il primo commit, a mano: è l'unico
git add scripts docs
git commit -q -m "avvio"
git push -q -u origin main
```

Il `git clone` di un repository vuoto avvisa che il repository è vuoto: è normale. `doc_index.py` scrive cinque file
e `--check` risponde `--check OK: 5 files match (decisioni: 2, backlog: 2).`

**1. Una decisione nuova.**

```bash
cat > docs/decisions/D-2026-02-01-la-mia-prima-voce.md <<'EOF'
---
id: D-2026-02-01-la-mia-prima-voce
date: 2026-02-01
title: La mia prima decisione registrata
---

**Contesto**: provo gli strumenti.
**Decisione**: tengo le decisioni in un file ciascuna.
EOF

python3 scripts/doc_index.py
git status --short --untracked-files=all
```

`git status` mostra tre righe: la voce nuova e i due indici delle decisioni che si sono mossi. Quel numero, contato e
non stimato, è quello che si passa allo script:

```bash
scripts/doc_commit.sh --expect 3 -m "docs: la mia prima voce" docs/decisions/D-2026-02-01-la-mia-prima-voce.md
```

Lo script elenca i suoi dieci passi e chiude con `[doc_commit] fatto. 3 file, ramo main.`

**2. Chiudere una voce, lasciando fuori dal commit un file di lavoro.** Chiudiamo `IP-FIX-1` e, intanto, teniamo sul
tree un file di codice che non è ancora pronto.

```bash
sed -i 's/^status: open$/status: closed/' docs/backlog/IP-FIX-1.md
sed -i 's/^opened: 2026-01-12$/opened: 2026-01-12\nclosed: 2026-02-02/' docs/backlog/IP-FIX-1.md
echo "print('lavoro in corso')" > app.py

python3 scripts/doc_index.py
git status --short --untracked-files=all
```

Le righe ora sono cinque: `app.py`, la voce e i tre indici del backlog. `app.py` non va nel commit: si dichiara con
`--deliver`, quindi i file attesi sono quattro. Prima, per vedere il cancello, sbagliamo apposta:

```bash
scripts/doc_commit.sh --expect 3 --deliver app.py -m "docs: chiusa IP-FIX-1" docs/backlog/IP-FIX-1.md
```

Lo script si ferma al passo 5 (`in stage: 4, attesi: 3`), non committa niente e ripulisce lo stage. Il messaggio
spiega anche che cosa vuol dire uno stage sopra o sotto l'atteso: il numero non si alza per far passare il cancello,
si capisce perché è diverso. Qui l'errore era nostro:

```bash
scripts/doc_commit.sh --expect 4 --deliver app.py -m "docs: chiusa IP-FIX-1" docs/backlog/IP-FIX-1.md
```

Questa volta il commit va. Con `--deliver` lo script non fa il `pull --rebase`, che con un file non committato sul tree
fallirebbe: controlla invece che il remoto sia già contenuto nel commit locale, poi fa il push. Alla fine sul tree
resta solo `app.py`, come dichiarato.

**3. Il percorso delle misure.** Uno script di misura si committa con il gemello; `app.py` è ancora sul tree, e va
dichiarato anche qui.

```bash
mkdir -p scripts/diag
printf '#!/usr/bin/env bash\necho "misura: ok"\n' > scripts/diag/misura.sh
scripts/diag_commit.sh --expect 1 --deliver app.py -m "diag: script di misura" scripts/diag/misura.sh
```

Un referto, invece, senza un verificatore non passa:

```bash
mkdir -p docs/report
printf '# Referto di prova\n' > docs/report/referto-1.md
scripts/diag_commit.sh --expect 1 --deliver app.py -m "diag: referto" docs/report/referto-1.md
```

Lo script si ferma al cancello 3 e dice di impostare `DIAG_VERIFIER`. È il comportamento voluto: un referto riporta
comandi e uscite, e prima di entrare nel registro qualcuno deve averli rieseguiti. Il verificatore non è in questa
cartella; che cosa deve fare è scritto più sotto.

Per buttare via tutto: `rm -rf /tmp/prova-strumenti`.

## Gli strumenti, uno per uno

### `doc_index.py`

**Da dove nasce.** Quando le decisioni sono passate da un unico file di migliaia di righe a un file ciascuna, serviva
qualcosa che ne ricomponesse la mappa: e che la ricomponesse ogni volta da capo, invece di affidarla alla memoria di chi
scrive.

**Che cosa fa.** Legge le voci di `docs/decisions/` e `docs/backlog/`, controlla le testate e genera cinque file:

| file | contenuto |
|---|---|
| `docs/decisions/INDEX.md` | le decisioni dalla più recente, con quelle superate e da chi |
| `docs/decisions/_ALL_DECISIONS.md` | tutte le decisioni in un file solo, da copiare o da cercare |
| `docs/backlog/INDEX.md` | le voci aperte per gravità e quelle rimandate |
| `docs/backlog/INDEX_CHIUSI.md` | le voci chiuse o superate, dalla chiusura più recente |
| `docs/backlog/_ALL_BACKLOG.md` | tutto il backlog in un file solo |

L'uscita dipende solo dai file delle voci: niente orari, niente date di oggi. Per questo `--check` ha senso: rigenera
tutto in memoria e lo confronta, carattere per carattere, con quello che c'è sul disco (i fine riga si leggono come
testo, quindi un file con i fine riga di Windows non conta come diverso).

**Uso.** `python3 scripts/doc_index.py` rigenera; `python3 scripts/doc_index.py --check` controlla ed esce con 1 se
qualcosa non torna. Lo script va in `scripts/`, e cerca `docs/` nella cartella sopra la sua, da qualunque cartella lo
si lanci.

**Come si adatta.** I prefissi del backlog stanno in `BACKLOG_PREFIXES`. I titoli negli indici si accorciano a
`INDEX_TITLE_MAX` caratteri, perché un indice si rilegge all'inizio di ogni sessione di lavoro con l'assistente e la
sua lunghezza è un costo che si ripete; il titolo intero resta nella voce.

**Che cosa non fa.** Non legge YAML: la testata è piatta, una chiave per riga. I testi degli indici sono in italiano, e
così i valori di `severity`. Non modifica mai le voci.

### `doc_commit.sh`

**Da dove nasce.** Da un errore che tornava: la sequenza dei comandi git, riscritta a mano, metteva il
`pull --rebase` in testa, dove con modifiche non committate fallisce sempre. Scriverlo nelle regole non è bastato. Una
regola che si legge e si viola non sta nel posto sbagliato: sta nella forma sbagliata. Serviva uno strumento che
quell'ordine lo eseguisse da sé.

**Che cosa fa.** In dieci passi, in un ordine che non si può cambiare:

1. controlla che sul tree non ci sia niente di modificato oltre ai file passati, a quelli dichiarati con `--deliver`
   e agli indici;
2. rigenera gli indici;
3. aggiunge allo stage solo i file passati e gli indici che si sono mossi (mai `git add -A`);
4. mostra lo stage;
5. si ferma se i file in stage non sono esattamente `N`;
6. lancia `doc_index.py --check`;
7. fa il commit;
8. fa il `pull --rebase` ad albero pulito (con `--deliver`, al suo posto, controlla che il remoto sia già contenuto
   nel commit locale);
9. fa il push;
10. controlla che sul tree non sia rimasto niente oltre ai file dichiarati con `--deliver`.

Se un passo fallisce, la catena si ferma: nessun push a metà.

**Uso.**

```bash
scripts/doc_commit.sh --expect N -m "messaggio" [--deliver <file>]... <file> [<file> ...]
```

`N` conta anche gli indici, e si misura con `python3 scripts/doc_index.py` seguito da
`git status --short --untracked-files=all`, senza contare i file dichiarati con `--deliver`. Una voce si può modificare
o aggiungere; non si può cancellare: le voci si superano. Un altro file tracciato si può cancellare passandolo fra i
file.

**Come si adatta.** Il ramo si sceglie con la variabile `DOC_COMMIT_BRANCH` (predefinito `main`); il remoto è `origin`.

**Che cosa non fa.** Non risolve i conflitti di un rebase: si ferma e lascia il commit locale, senza push. Non accetta
`--deliver` su una voce: una voce lasciata fuori dal commit finirebbe negli indici senza il suo corpo.

### `diag_commit.sh`

**Da dove nasce.** Dallo stesso errore, ricomparso nei briefing di misura: `doc_commit.sh` non bastava, perché i
prodotti di una misura hanno un ciclo loro, senza indici.

**Che cosa fa.** Dieci passi, come il gemello, ma senza gli indici: niente rigenerazione e niente `--check`. In più ha
due cancelli suoi. Il primo accetta solo file sotto `docs/report/` e `scripts/diag/` (la costante `PERIMETRO`); il
terzo fa passare ogni referto, cioè ogni file `docs/report/*.md`, da un verificatore, prima di metterlo in stage.

**Uso.**

```bash
scripts/diag_commit.sh --expect N -m "messaggio" [--deliver <file>]... <file> [<file> ...]
```

**Come si adatta.** Con tre variabili: `DIAG_COMMIT_BRANCH` (il ramo, predefinito `main`), `DIAG_VERIFIER` (il percorso
del verificatore) e `DIAG_PYTHON` (l'interprete che lo lancia, predefinito `.venv/bin/python` nella radice del repo).

**Il verificatore.** Non è incluso, perché quello che usavamo conosceva i comandi di un solo progetto. Il contratto è
semplice: riceve il percorso di un referto, riesegue i comandi che il referto mostra, ed esce con 0 solo se l'uscita e
il codice d'uscita coincidono con quelli dichiarati; altrimenti esce con un altro codice e stampa perché. Se
`DIAG_VERIFIER` non è impostata, nessun referto si committa. Il motivo è tutto qui: un modello che scrive un referto può
ricopiare male un'uscita, e un numero esibito da chi ha eseguito resta una parola finché qualcuno non lo rimisura.

**Che cosa non fa.** Non accetta file fuori dal perimetro, e non ha gli indici del gemello.

### La skill `voce-doc`

**Che cos'è.** Le istruzioni per Claude Code su come si crea o si aggiorna una voce: dove va il file, quali chiavi
servono, quale stato scegliere, come si rigenerano gli indici e come si fa il commit. Claude Code le legge da sé quando
il lavoro lo richiede.

**Uso.** Nella radice del vostro repository:

```bash
mkdir -p .claude/skills
cp -r "$STRUMENTI"/skill/voce-doc .claude/skills/
```

**Che cosa non fa.** È testo: nessun controllo la tiene allineata agli script. Se cambiate uno script, aggiornate anche
lei. L'ultima volta, prima di pubblicarla, l'abbiamo confrontata riga per riga con il codice.

### `cc-bridge`

Un server MCP che collega la chat di Claude a Claude Code: dalla chat si lancia un lavoro sul proprio computer, se ne
segue l'avanzamento e se ne legge l'esito. Ha un [README suo](./cc-bridge/README.md), con installazione, opzioni e
limiti.

## Il giro tipico

Ecco come stavano insieme, in una sera di lavoro.

1. In chat si discute un problema e si decide. La chat scrive la voce che registra la decisione.
2. Claude Code la committa con `doc_commit.sh`: prima la voce, poi, in un commit successivo, il codice che la attua.
3. Se serve una misura, Claude Code scrive lo script in `scripts/diag/` e il referto in `docs/report/`, e li committa
   con `diag_commit.sh`: il verificatore riesegue i comandi del referto prima che entri nel registro.
4. La chat segue tutto con cc-bridge, senza che nessuno copi e incolli fra una finestra e l'altra.
5. La sessione successiva, chiunque riparte dagli indici: che cosa è stato deciso, che cosa resta aperto.
