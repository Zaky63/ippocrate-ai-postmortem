---
id: D-2026-01-24-commit-con-script
date: 2026-01-24
title: I commit della documentazione passano da doc_commit.sh
fix: [IP-FIX-2]
---

**Contesto**: la sequenza dei comandi git, riscritta a mano a ogni commit, metteva più volte il `pull --rebase` in
testa, dove fallisce sempre. Una nota nelle regole non è bastata a fermarlo (`IP-FIX-2`).

**Decisione**: i commit di voci, indici, documenti e codice si fanno con `scripts/doc_commit.sh`, che esegue i comandi
in un ordine che non si può alterare e si ferma se i file in stage non sono quelli attesi.

**Conseguenze**: a mano restano solo i comandi git che leggono (`git status`, `git diff`, `git log`).

**Riferimenti**: [D-2026-01-10-un-file-per-voce](./D-2026-01-10-un-file-per-voce.md).
