---
id: IP-FIX-2
status: closed
severity: alta
opened: 2026-01-20
closed: 2026-01-24
decisions: [D-2026-01-24-commit-con-script]
title: Il pull --rebase in testa al ciclo fa fallire i commit
---

Con modifiche non ancora committate sul tree, `git pull --rebase` rifiuta di partire e l'intera catena di comandi si
ferma. È successo più volte, nonostante una nota nelle regole.

2026-01-24: chiusa con `D-2026-01-24-commit-con-script`: l'ordine dei comandi lo esegue uno script, non lo si scrive
più a mano.
