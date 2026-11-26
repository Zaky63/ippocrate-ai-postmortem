---
id: D-2026-01-10-un-file-per-voce
date: 2026-01-10
title: Ogni decisione e ogni voce di backlog in un file suo
---

**Contesto**: il registro unico delle decisioni era diventato troppo lungo da rileggere all'inizio di ogni sessione
di lavoro con l'assistente.

**Decisione**: una decisione per file in `docs/decisions/`, una voce per file in `docs/backlog/`. Gli indici li genera
`scripts/doc_index.py`; a mano non si scrivono.

**Conseguenze**: una voce chiusa non si riscrive. Se una decisione cambia, se ne scrive una nuova che la supera; se una
riga diventa falsa, si smentisce con una nota in coda.

**Riferimenti**: nessuno.
