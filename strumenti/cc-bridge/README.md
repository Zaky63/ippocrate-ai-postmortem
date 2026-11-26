# cc-bridge

cc-bridge è un server MCP che collega la chat di Claude (Claude Desktop) a Claude Code CLI (CC) in esecuzione in WSL: dalla chat si lancia un task di CC su un repository, se ne segue l'avanzamento e se ne legge l'esito, senza aprire un terminale. È pensato per chi sviluppa con CC dentro WSL2 e vuole usare la chat per impartire e controllare il lavoro. È nato dentro un progetto reale, raccontato in questo repo (capitolo 2): le regole di prudenza e i valori di default qui sotto vengono da lì, e le date di misura indicano quando ciascun fatto è stato verificato.

Un solo file Python, nessuna dipendenza (Python ≥ 3.8; Ubuntu 24.04 ha la 3.12).

La chat può:

- lanciare un task di CC su un progetto e riceverne l'esito (`cc_run`, `cc_status`);
- continuare una sessione di CC, anche una aperta da te in terminale, e viceversa (`claude --resume <id>`);
- vedere le sessioni recenti e il loro contenuto (`cc_sessions`, `cc_transcript`);
- fermare un task (`cc_cancel`) e fare diagnostica (`cc_info`).

CC lavora con tutto il suo contesto: `CLAUDE.md`, `.claude/settings.json` (modello, effort, permessi), hook, subagenti e server MCP del progetto.

## Installazione

**1. Copia e verifica** (se hai salvato i file altrove, cambia il percorso di `Downloads`)

In WSL2 (`~/projects/cc-bridge`):
```bash
mkdir -p ~/projects/cc-bridge
cp /mnt/c/Users/<utente-windows>/Downloads/cc_bridge.py /mnt/c/Users/<utente-windows>/Downloads/README.md ~/projects/cc-bridge/
python3 ~/projects/cc-bridge/cc_bridge.py --roots ~/projects/<progetto> --check
```
Deve chiudere con `OK` e mostrare il percorso di `claude`, la versione e `authMethod=claude.ai`.

In Windows (PowerShell) — stessa prova, lanciata come la lancerà Claude Desktop (la distro `Ubuntu-24.04` è un esempio: usa la tua, che elenchi con `wsl.exe -l`):
```powershell
wsl.exe -d Ubuntu-24.04 -e /usr/bin/python3 /home/<utente-wsl>/projects/cc-bridge/cc_bridge.py --roots /home/<utente-wsl>/projects/<progetto> --check
```

**2. Configura Claude Desktop**: in `%APPDATA%\Claude\claude_desktop_config.json`, dentro `"mcpServers"`, accanto agli eventuali altri server:
```json
"cc-bridge": {
  "command": "wsl.exe",
  "args": ["-d", "Ubuntu-24.04", "-e", "/usr/bin/python3",
           "/home/<utente-wsl>/projects/cc-bridge/cc_bridge.py",
           "--roots", "/home/<utente-wsl>/projects/<progetto>"]
}
```

**3.** Chiudi del tutto Claude Desktop (anche dall'area di notifica), riaprilo e in chat chiedi: «usa cc_info».

## Uso

| Chiedi in chat | Cosa succede |
|---|---|
| «Chiedi a CC dove il codice valida i dati in ingresso» | `cc_run` in `plan`: sola lettura |
| «Fai eseguire a CC le istruzioni in `docs/tasks/aggiorna-dipendenze.md`» | `cc_run` in `auto`: modifica, lancia i test, riporta |
| Censimenti e audit | `plan` + la parola `ultracode` nel prompt |
| «Cosa ho fatto in CC ieri sera?» | `cc_sessions` + `cc_transcript` |
| «Continua la sessione di ieri sera» | `cc_run(resume=…)`, con `fork` se è ancora aperta in terminale |

Un task più lungo dell'attesa (25 s) torna con `state: running` e un `job_id`: la chat continua con `cc_status`. Ogni esito termina con il comando per riprendere in terminale: `cd /home/<utente-wsl>/projects/<progetto> && claude --resume <id>`.

## Modalità

| mode | Cosa può fare CC |
|---|---|
| `plan` | leggere e analizzare (default) |
| `edit` | modificare file e usare comandi di filesystem (`mkdir`, `mv`, `cp`…); gli altri comandi solo se permessi in `.claude/settings.json` |
| `auto` | modificare e lanciare comandi; il classificatore di CC blocca ciò che va oltre la richiesta o tocca infrastruttura non riconosciuta |
| `full` | nessun controllo: spento finché non metti `--max-mode full` |

La chat sceglie la modalità a ogni corsa; il tetto lo fissi tu con `--max-mode` (default `auto`). Ciò che viene negato è contato sotto lo stato (`denied: N (motivi)`) ed elencato in fondo all'esito sotto *blocked by permissions*, ogni comando con il motivo che CC ha ricevuto.

## Scrivere i prompt

In `auto` il classificatore di sicurezza di CC giudica ogni comando alla luce del prompt; e la chiamata a `cc_run` può essere fermata dalla chat stessa prima di partire, se il prompt sembra un aggiramento. Le regole che hanno funzionato nel progetto da cui nasce il bridge (prove del 2026-10-16):

- Per un lavoro che modifica file o lancia comandi, un prompt di una riga che rimanda a un file del repo: «Esegui `docs/tasks/<compito>.md`, rispetta i controlli, chiudi con `esito=`». Passi, comandi e valori attesi stanno nel file, dove si rileggono e si controllano con lo sha.
- Niente codice codificato (base64 e simili) né istruzioni lunghe nel prompt.
- Comandi brevi e separati, ognuno con il suo atteso, invece di lunghe catene con `&&`: una catena può essere negata in blocco anche quando i singoli comandi passerebbero.
- Dopo un rifiuto, niente varianti. L'esito riporta il comando negato e il motivo; decidi tu se lanciarlo da terminale, permetterlo in `.claude/settings.json` o cambiare il compito. Riprendere la sessione chiedendo «fai invece così» è proprio lo schema che il classificatore blocca. Fa eccezione il verdetto mancato (sotto): lì il testo stesso consente di riprovare una volta, com'è.

## Opzioni

| Opzione | Default | |
|---|---|---|
| `--roots DIR…` | home | cartelle in cui la chat può far lavorare CC e di cui vede le sessioni |
| `--max-mode` | `auto` | tetto: `plan`, `edit`, `auto`, `full` |
| `--model` | settings di CC | modello di default dei task |
| `--max-jobs` | 2 | task contemporanei (conta anche quelli avviati prima di un riavvio) |
| `--default-wait` / `--max-wait` | 25 / 50 s | attesa per chiamata se il client non chiede l'avanzamento; con Claude Desktop restare sotto i 60 s |
| `--max-wait-progress` | 600 s | attesa per chiamata se il client chiede l'avanzamento (Claude Desktop non lo chiede) |
| `--keep-api-key` | no | lascia `ANTHROPIC_API_KEY` a CC (fatturazione API invece dell'abbonamento) |
| `--no-preamble` | no | non antepone l'avvertenza `<cc-bridge>` ai prompt |
| `--claude PATH` | ricerca automatica | binario `claude` (`~/.local/bin/claude`, nvm, npm…) |
| `--claude-config-dir` | `~/.claude` | come `CLAUDE_CONFIG_DIR` |
| `--state-dir` / `--keep-days` | `~/.cache/cc-bridge` / 14 | dove stanno i job e per quanto |

## Come funziona

- Ogni task è `claude -p --output-format stream-json --verbose --permission-mode <…> --permission-prompts none`, con il prompt su stdin, in un gruppo di processi proprio: sopravvive al riavvio di Claude Desktop finché WSL resta acceso. Stato e output in `~/.cache/cc-bridge/jobs/<job_id>/` (`out.jsonl`, `err.log`, `meta.json`).
- Ogni prompt dalla chat arriva a CC preceduto da un'avvertenza `<cc-bridge>`: turno non interattivo, niente domande, chiusura con un report (salvo formato definito dalla richiesta o dalle istruzioni del progetto). I turni che scrivi tu in terminale restano normali; in `cc_transcript` compaiono come `USER`, quelli della chat come `CHAT->CC`.
- L'esito riporta stato, turni, costo stimato (equivalente API), uso delle finestre 5 h / 7 giorni dell'abbonamento, comandi negati con il motivo, e avvisa se CC ha usato una chiave API o se la modalità richiesta non era disponibile. Durante il giro, gli strumenti finiti in errore compaiono fra le attività (`x <comando> -> error: …`).
- Il motivo di un rifiuto è il testo che CC riceve al posto dell'esito del comando; l'etichetta fra parentesi quadre (es. `Auto-Mode Bypass`) va nel conteggio sotto lo stato. Il formato non è documentato da Anthropic: se cambia, il bridge mostra il testo com'è, o «not reported». Verificato il 2026-10-17 su quattro giri reali del 15 e 16/10.
- Un verdetto mancato del classificatore («gave no verdict»: un guasto passeggero del controllo, non un giudizio) compare come `no verdict, transient`: CC può ripetere il comando una volta, com'è, e non è un rifiuto da riportare. Se CC ha rifatto com'era una chiamata negata, l'esito lo dice (`-> ran on retry`, oppure `retried: denied again`).
- `cc_cancel` manda SIGINT (chiusura ordinata del turno), poi SIGTERM e SIGKILL all'intero gruppo.
- **Attese.** Una chiamata inoltrata da Claude Desktop, anche dalla chat collegata al PC, cade a 60 s e il risultato va perso (misurato il 2026-10-15: Claude Desktop non chiede l'avanzamento e non avvisa il server quando chiude). Per questo ogni chiamata attende al massimo 50 s: non alzare `--max-wait` oltre 55. Un giro lungo si segue con più `cc_status`, che costano poco: ogni risposta riporta solo le attività nuove, e quando non ce ne sono ripete l'ultima, così anche dopo una risposta caduta si vede a che punto è CC. Il giro di CC prosegue comunque. Per altri client: se chiedono l'avanzamento, il bridge lo manda ogni 10 s e attende fino a `--max-wait-progress`; se annullano una chiamata per timeout, il bridge registra il limite in `~/.cache/cc-bridge/client.json` e da lì resta sotto (per dimenticarlo si cancella il file). `cc_info` mostra il tetto in vigore.
- Un esito più lungo di `--max-output` si taglia nel mezzo: inizio e fine, dove CC scrive la riga d'esito, restano.

## Limiti noti

- Un rifiuto deciso dalla chat stessa, prima che la chiamata parta, non arriva al bridge: il bridge non lo vede e non può mostrarne il motivo.
- Le sessioni avviate con `claude -p` non compaiono nel picker di `claude --resume` né in `claude --continue`: usa l'id.
- Riprendere senza `fork` una sessione aperta in un terminale intreccia i messaggi nello stesso transcript.
- Il formato dei transcript è interno a CC: `cc_transcript` è best-effort; se una versione futura lo cambia, lo segnala e propone di chiedere un riassunto a CC (resume con fork).
- La documentazione di CC annuncia che `--bare` diventerà il default di `claude -p`: in quel caso CC headless non leggerebbe più `CLAUDE.md` né userebbe il login dell'abbonamento, e il bridge andrà aggiornato.
- Protocollo MCP dell'era `initialize` (2025-11-25): i client 2026-07-28 lo negoziano da soli.

## Diagnostica

- In chat: «usa cc_info». L'uscita di `cc_info` e di `--check` mostra l'email dell'account con cui `claude` è collegato: toglila prima di incollare quell'uscita in un posto pubblico, per esempio una segnalazione su GitHub.
- Log del server: nella cartella log di Claude Desktop (`%APPDATA%\Claude\logs\`), file `mcp-server-cc-bridge.log`.
- Un job specifico: `~/.cache/cc-bridge/jobs/<job_id>/err.log`.

## Licenza

MIT (SPDX: `MIT`). Copyright (c) 2026 Maurizio Acampora.
