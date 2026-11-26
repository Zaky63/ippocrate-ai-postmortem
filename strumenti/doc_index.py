#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Maurizio Acampora
"""
doc_index.py — Generate navigational indexes for the file-per-entry documentation.

Reads the one-file-per-entry
sources under docs/decisions/ and docs/backlog/, validates their flat front-matter against
closed vocabularies, and (re)generates five derived files:

    docs/decisions/INDEX.md            reverse-chronological table + superseded map
    docs/decisions/_ALL_DECISIONS.md   single-file concatenation (one copy + one grep)
    docs/backlog/INDEX.md              open-by-severity / deferred (closed entries excluded)
    docs/backlog/INDEX_CHIUSI.md       closed + superseded, by closing date descending
    docs/backlog/_ALL_BACKLOG.md       single-file concatenation, by number descending

Index titles are DISPLAY-truncated to INDEX_TITLE_MAX characters: the index is read at the
start of every session and its length is a recurring cost. The full
title stays in the entry file and in the _ALL_ concatenation; truncation never touches sources.

Determinism: every generated file is a PURE FUNCTION of the source files. The header carries a
deterministic source-hash (NOT a wall-clock timestamp) so that regenerating without source
changes produces byte-identical output — which is exactly what makes --check meaningful.
For the same reason the "recently closed" window is anchored to the most recent closed date
found in the corpus, not to wall-clock "now".

Modes:
    python3 scripts/doc_index.py           (re)generate the five files
    python3 scripts/doc_index.py --check   regenerate in memory, compare with the files on
                                           disk (read as text, newlines normalized); exit 0
                                           if identical, exit 1 listing the
                                           divergences (use in CI / pre-push)

Validation failures (unknown/illegal vocabulary values, id != filename, missing required
keys, closed-date missing where the status requires one, superseded without a resolvable
superseded_by, duplicate id) print the offending file and value to stderr and exit 1 in
BOTH modes; no output is written when validation fails.

stdlib-only: os, sys, re, hashlib, datetime, collections. No external dependency, no PyYAML.
Code and identifiers in English; user-facing strings in the generated files in Italian.
"""

import os
import sys
import re
import hashlib
from datetime import date
from collections import Counter, defaultdict

# --------------------------------------------------------------------------- paths
# Derived from the script location, never from the cwd.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECISIONS_DIR = os.path.join(REPO_ROOT, "docs", "decisions")
BACKLOG_DIR = os.path.join(REPO_ROOT, "docs", "backlog")

DECISIONS_INDEX = os.path.join(DECISIONS_DIR, "INDEX.md")
DECISIONS_ALL = os.path.join(DECISIONS_DIR, "_ALL_DECISIONS.md")
BACKLOG_INDEX = os.path.join(BACKLOG_DIR, "INDEX.md")
BACKLOG_INDEX_CLOSED = os.path.join(BACKLOG_DIR, "INDEX_CHIUSI.md")
BACKLOG_ALL = os.path.join(BACKLOG_DIR, "_ALL_BACKLOG.md")

# --------------------------------------------------------------------------- vocabularies
# Backlog id prefixes: replace them with the ones used by your own project.
BACKLOG_PREFIXES = ("IP-FIX", "IP-OP")
BACKLOG_PREFIX_ALT = "|".join(re.escape(p) for p in BACKLOG_PREFIXES)

DECISION_ID_RE = re.compile(r"^D-\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")
BACKLOG_ID_RE = re.compile(rf"^({BACKLOG_PREFIX_ALT})-R?\d+[a-z]?$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TRAILING_NUM_RE = re.compile(r"-R?(\d+)[a-z]?$")

BACKLOG_STATUS = {"open", "deferred", "closed", "superseded"}
BACKLOG_STATUS_NEEDS_CLOSED = {"closed", "superseded"}
BACKLOG_SEVERITY = {"alta", "media", "bassa"}

DECISION_KEYS = {"id", "date", "title", "supersedes", "fix"}
DECISION_LIST_KEYS = {"supersedes", "fix"}
BACKLOG_KEYS = {"id", "status", "severity", "opened", "closed", "decisions", "superseded_by", "title"}
BACKLOG_LIST_KEYS = {"decisions"}

# "Recently closed" window, measured from the most recent closed date IN THE CORPUS (not
# wall-clock now) so the output stays a pure function of the sources (see module docstring).
RECENT_WINDOW_DAYS = 30

# Display cap for titles in INDEX files (the index is read at the start of every session, so
# its length is a recurring cost). Hard cut, not
# sentence-aware: titles use ':' as a hinge and a sentence cut left dangling stumps.
INDEX_TITLE_MAX = 200
ELLIPSIS = "…"

GEN_LINE = ("> **GENERATO da `scripts/doc_index.py` — NON EDITARE A MANO.** "
            "Rigenerare con `python3 scripts/doc_index.py`.")


# --------------------------------------------------------------------------- front-matter parser
def parse_front_matter(text, list_keys, warnings, fname):
    """Parse the flat front-matter block. Returns (meta_dict, body_str) or (None, text) if the
    block is missing/unterminated. Only keys in `list_keys` are parsed as inline `[a, b]` lists;
    all other bracketed values are kept as plain strings (avoids misreading a bracketed title)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    meta = {}
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if ":" not in raw:
            warnings.append(f"{fname}: front-matter line without ':' ignored -> {raw.strip()!r}")
            continue
        key, _, val = raw.partition(":")  # split on FIRST colon: lets 'title' contain colons
        key = key.strip()
        val = val.strip()
        if key in list_keys and val.startswith("[") and val.endswith("]"):
            items = [x.strip() for x in val[1:-1].split(",")]
            meta[key] = [x for x in items if x]
        else:
            meta[key] = val
    body = "\n".join(lines[end + 1:])
    return meta, body


# --------------------------------------------------------------------------- validation
def _require_iso(fname, key, val, errors):
    if not val:
        return
    if not ISO_DATE_RE.match(val):
        errors.append(f"{fname}: '{key}' is not ISO YYYY-MM-DD -> {val!r}")
        return
    try:
        date.fromisoformat(val)
    except ValueError:
        errors.append(f"{fname}: '{key}' is not a valid calendar date -> {val!r}")


def _validate_decision(fname, stem, meta, errors):
    _id = meta.get("id", "")
    if not _id:
        errors.append(f"{fname}: missing required 'id'")
    else:
        if not DECISION_ID_RE.match(_id):
            errors.append(f"{fname}: 'id' does not match D-YYYY-MM-DD-slug -> {_id!r}")
        if _id != stem:
            errors.append(f"{fname}: 'id' ({_id}) does not match filename stem ({stem})")
    if not meta.get("date"):
        errors.append(f"{fname}: missing required 'date'")
    else:
        _require_iso(fname, "date", meta["date"], errors)
    if not meta.get("title"):
        errors.append(f"{fname}: missing required 'title'")
    for lk in DECISION_LIST_KEYS:
        if lk in meta and not isinstance(meta[lk], list):
            errors.append(f"{fname}: '{lk}' must be an inline list [a, b] -> {meta[lk]!r}")


def _validate_backlog(fname, stem, meta, errors):
    _id = meta.get("id", "")
    if not _id:
        errors.append(f"{fname}: missing required 'id'")
    else:
        if not BACKLOG_ID_RE.match(_id):
            errors.append(f"{fname}: 'id' does not match {' / '.join(p + '-NN' for p in BACKLOG_PREFIXES)} -> {_id!r}")
        if _id != stem:
            errors.append(f"{fname}: 'id' ({_id}) does not match filename stem ({stem})")
    status = meta.get("status", "")
    if not status:
        errors.append(f"{fname}: missing required 'status'")
    elif status not in BACKLOG_STATUS:
        errors.append(f"{fname}: illegal 'status' -> {status!r} (allowed: {sorted(BACKLOG_STATUS)})")
    sev = meta.get("severity", "")
    if not sev:
        errors.append(f"{fname}: missing required 'severity'")
    elif sev not in BACKLOG_SEVERITY:
        errors.append(f"{fname}: illegal 'severity' -> {sev!r} (allowed: {sorted(BACKLOG_SEVERITY)})")
    if not meta.get("opened"):
        errors.append(f"{fname}: missing required 'opened'")
    else:
        _require_iso(fname, "opened", meta["opened"], errors)
    if status in BACKLOG_STATUS_NEEDS_CLOSED:
        if not meta.get("closed"):
            errors.append(f"{fname}: status '{status}' requires a 'closed' date")
        else:
            _require_iso(fname, "closed", meta["closed"], errors)
    elif meta.get("closed"):
        _require_iso(fname, "closed", meta["closed"], errors)
    if status == "superseded" and not meta.get("superseded_by"):
        errors.append(f"{fname}: status 'superseded' requires a 'superseded_by' pointer")
    for lk in BACKLOG_LIST_KEYS:
        if lk in meta and not isinstance(meta[lk], list):
            errors.append(f"{fname}: '{lk}' must be an inline list [a, b] -> {meta[lk]!r}")


def validate_backlog_corpus(entries, errors):
    """Cross-file check: every 'superseded_by' must name an id that exists in the corpus.
    Cannot live in _validate_backlog, which sees one entry at a time."""
    have = {e["id"] for e in entries}
    for e in entries:
        target = e["meta"].get("superseded_by")
        if target and target not in have:
            errors.append(f"{e['fname']}: 'superseded_by' names an entry that does not exist -> {target!r}")


# --------------------------------------------------------------------------- loading
def load_sources(directory, kind, errors, warnings):
    """Load and validate all entry files in `directory`. Generated files (INDEX*.md and
    anything starting with '_') are skipped. Returns a list of entry dicts."""
    if not os.path.isdir(directory):
        errors.append(f"directory not found: {directory}")
        return []
    if kind == "decision":
        list_keys, known_keys, validator = DECISION_LIST_KEYS, DECISION_KEYS, _validate_decision
    else:
        list_keys, known_keys, validator = BACKLOG_LIST_KEYS, BACKLOG_KEYS, _validate_backlog

    entries = []
    seen_ids = {}
    for fname in sorted(os.listdir(directory)):
        if not fname.endswith(".md"):
            continue
        if fname.startswith("INDEX") or fname.startswith("_"):
            continue  # generated aggregates / indexes (INDEX.md, INDEX_CHIUSI.md) are not sources
        path = os.path.join(directory, fname)
        stem = fname[:-3]
        try:
            with open(path, encoding="utf-8") as fh:
                raw = fh.read()
        except Exception as e:
            errors.append(f"{fname}: cannot read ({e})")
            continue
        meta, body = parse_front_matter(raw, list_keys, warnings, fname)
        if meta is None:
            errors.append(f"{fname}: missing or unterminated front-matter block")
            continue
        for k in meta:
            if k not in known_keys:
                warnings.append(f"{fname}: unknown front-matter key '{k}' (ignored)")
        validator(fname, stem, meta, errors)
        _id = meta.get("id") or stem
        if _id in seen_ids:
            errors.append(f"{fname}: duplicate id '{_id}' (also in {seen_ids[_id]})")
        else:
            seen_ids[_id] = fname
        entries.append({"id": _id, "meta": meta, "body": body, "raw": raw, "fname": fname})
    return entries


# --------------------------------------------------------------------------- helpers
def source_hash(entries):
    """Deterministic fingerprint of a source corpus (sorted by id over raw file bytes)."""
    h = hashlib.sha256()
    for e in sorted(entries, key=lambda x: x["id"]):
        h.update(e["id"].encode("utf-8"))
        h.update(b"\0")
        h.update(e["raw"].encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:12]


def header(source_count, shash):
    return f"{GEN_LINE}\n<!-- source-hash: {shash} · sorgenti: {source_count} -->"


def _backlog_num(entry):
    m = TRAILING_NUM_RE.search(entry["id"])
    return int(m.group(1)) if m else -1


def _backlog_prefix(entry):
    for p in BACKLOG_PREFIXES:
        if entry["id"].startswith(p + "-"):
            return p
    return BACKLOG_PREFIXES[0]


def _sort_decisions(entries):
    # 'date' sorts correctly as a lexicographic string; id is a deterministic tiebreak.
    return sorted(entries, key=lambda e: (e["meta"]["date"], e["id"]), reverse=True)


def _sort_backlog(entries):
    return sorted(entries, key=lambda e: (_backlog_num(e), _backlog_prefix(e)), reverse=True)


def _cell(text):
    return (text or "").replace("|", "\\|")


def _short_title(text, limit=INDEX_TITLE_MAX):
    """Display-only truncation for index tables. Strips one enclosing pair of double quotes
    (front-matter titles are usually quoted), cuts at `limit` characters, closes a backtick
    span left open by the cut so the table row still renders, and appends an ellipsis."""
    t = (text or "").strip()
    if len(t) >= 2 and t[0] == '"' and t[-1] == '"':
        t = t[1:-1]
    if len(t) <= limit:
        return t
    t = t[:limit].rstrip()
    if t.count("`") % 2 == 1:
        t += "`"
    return t + ELLIPSIS


def _display_title(entry):
    """Best-effort display title (display only; does not affect validation or source-hash).
    Prefer an explicit 'title'; else the first heading line of the body, id prefix stripped."""
    t = entry["meta"].get("title")
    if t:
        return t
    for line in entry["body"].splitlines():
        s = line.strip()
        if s.startswith("#"):
            s = s.lstrip("#").strip()
            return re.sub(rf"^({BACKLOG_PREFIX_ALT})-R?\d+[a-z]?\s*[—:\-]\s*", "", s)
        if s:
            break
    return ""


# --------------------------------------------------------------------------- builders
def build_decisions_index(entries):
    shash = source_hash(entries)
    ordered = _sort_decisions(entries)
    have = {e["id"] for e in entries}
    superseded_by = defaultdict(list)
    for e in entries:
        for target in e["meta"].get("supersedes", []) or []:
            superseded_by[target].append(e["id"])

    lines = [header(len(entries), shash), "",
             "# Decisioni — indice", "",
             f"{len(entries)} voci. Ordine cronologico inverso. Sorgenti in `docs/decisions/<id>.md`.", "",
             "| id | data | titolo | stato |",
             "|---|---|---|---|"]
    for e in ordered:
        _id = e["id"]
        if _id in superseded_by:
            ptrs = ", ".join(f"[{s}](./{s}.md)" for s in sorted(superseded_by[_id]))
            stato = f"superata → {ptrs}"
        else:
            stato = "vigente"
        lines.append(f"| [{_id}](./{_id}.md) | {e['meta']['date']} | {_cell(_short_title(e['meta'].get('title')))} | {stato} |")

    lines += ["", "## Superate", ""]
    if superseded_by:
        for target in sorted(superseded_by):
            ptrs = ", ".join(f"[{s}](./{s}.md)" for s in sorted(superseded_by[target]))
            link = f"[{target}](./{target}.md)" if target in have else f"`{target}` (fuori corpus)"
            lines.append(f"- {link} → superata da {ptrs}")
    else:
        lines.append("_Nessuna voce superata._")
    return "\n".join(lines).rstrip() + "\n"


def build_backlog_index(entries):
    shash = source_hash(entries)
    counts = Counter(e["meta"].get("status", "?") for e in entries)
    by_status = defaultdict(list)
    for e in entries:
        by_status[e["meta"].get("status", "?")].append(e)

    def table(items):
        rows = ["| id | severità | aperto | chiuso | titolo |", "|---|---|---|---|---|"]
        for e in items:
            rows.append(
                f"| [{e['id']}](./{e['id']}.md) | {e['meta'].get('severity', '')} | "
                f"{e['meta'].get('opened', '')} | {e['meta'].get('closed', '')} | "
                f"{_cell(_short_title(_display_title(e)))} |")
        return rows

    n_closed = sum(counts[s] for s in BACKLOG_STATUS_NEEDS_CLOSED)
    lines = [header(len(entries), shash), "",
             "# Backlog — indice", "",
             f"{len(entries)} voci. Sorgenti in `docs/backlog/<id>.md`. "
             f"Le {n_closed} voci chiuse/superate stanno in [`INDEX_CHIUSI.md`](./INDEX_CHIUSI.md).", "",
             "**Per stato:** " + " · ".join(f"{s}: {counts[s]}" for s in sorted(counts)), ""]

    lines += ["## Aperti", ""]
    open_items = by_status.get("open", [])
    if open_items:
        for sev in ("alta", "media", "bassa"):
            grp = _sort_backlog([e for e in open_items if e["meta"].get("severity") == sev])
            if grp:
                lines += [f"### severità {sev}", ""] + table(grp) + [""]
    else:
        lines += ["_Nessuna voce aperta._", ""]

    lines += ["## Rimandate", ""]
    df = _sort_backlog(by_status.get("deferred", []))
    lines += (table(df) + [""]) if df else ["_Nessuna._", ""]

    return "\n".join(lines).rstrip() + "\n"


def build_backlog_closed_index(entries):
    """Closed + superseded entries, most recent closing date first. Kept OUT of INDEX.md so the
    opening read carries only what is still actionable. The
    'recently closed' window (anchored to the corpus, not to wall-clock) opens the file."""
    shash = source_hash(entries)
    closed = [e for e in entries
              if e["meta"].get("status") in BACKLOG_STATUS_NEEDS_CLOSED
              and e["meta"].get("closed") and ISO_DATE_RE.match(e["meta"]["closed"])]
    closed.sort(key=lambda e: (e["meta"]["closed"], _backlog_num(e), _backlog_prefix(e)), reverse=True)
    anchor = closed[0]["meta"]["closed"] if closed else None

    def table(items):
        rows = ["| id | severità | aperto | chiuso | stato | titolo |", "|---|---|---|---|---|---|"]
        for e in items:
            rows.append(
                f"| [{e['id']}](./{e['id']}.md) | {e['meta'].get('severity', '')} | "
                f"{e['meta'].get('opened', '')} | {e['meta'].get('closed', '')} | "
                f"{e['meta'].get('status', '')} | {_cell(_short_title(_display_title(e)))} |")
        return rows

    lines = [header(len(entries), shash), "",
             "# Backlog — voci chiuse", "",
             f"{len(closed)} voci chiuse o superate su {len(entries)}. Ordine per data di chiusura "
             f"decrescente. Le voci aperte stanno in [`INDEX.md`](./INDEX.md).", ""]
    if not closed:
        lines += ["_Nessuna voce chiusa._", ""]
        return "\n".join(lines).rstrip() + "\n"

    anchor_d = date.fromisoformat(anchor)
    recent = [e for e in closed
              if 0 <= (anchor_d - date.fromisoformat(e["meta"]["closed"])).days <= RECENT_WINDOW_DAYS]
    older = [e for e in closed if e not in recent]
    lines += ["## Chiuse di recente", "",
              f"_Ultimi {RECENT_WINDOW_DAYS} giorni rispetto alla chiusura più recente nel backlog ({anchor})._", ""]
    lines += (table(recent) + [""]) if recent else ["_Nessuna._", ""]
    lines += ["## Chiuse in precedenza", ""]
    lines += (table(older) + [""]) if older else ["_Nessuna._", ""]
    return "\n".join(lines).rstrip() + "\n"


def build_all(entries, kind):
    shash = source_hash(entries)
    if kind == "decision":
        ordered = _sort_decisions(entries)
        title = "Tutte le decisioni (concatenazione per grep)"
    else:
        ordered = _sort_backlog(entries)
        title = "Tutto il backlog (concatenazione per grep)"
    prefix = f"{header(len(entries), shash)}\n\n# {title}\n"
    joined = "\n\n---\n\n".join(e["raw"].strip() for e in ordered)
    body = prefix + ("\n" + joined if joined else "")
    return body.rstrip() + "\n"


# --------------------------------------------------------------------------- main
def main():
    check = "--check" in sys.argv[1:]
    errors, warnings = [], []
    decisions = load_sources(DECISIONS_DIR, "decision", errors, warnings)
    backlog = load_sources(BACKLOG_DIR, "backlog", errors, warnings)
    validate_backlog_corpus(backlog, errors)

    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print(f"\n{len(errors)} validation error(s). No output written.", file=sys.stderr)
        sys.exit(1)

    targets = {
        DECISIONS_INDEX: build_decisions_index(decisions),
        DECISIONS_ALL: build_all(decisions, "decision"),
        BACKLOG_INDEX: build_backlog_index(backlog),
        BACKLOG_INDEX_CLOSED: build_backlog_closed_index(backlog),
        BACKLOG_ALL: build_all(backlog, "backlog"),
    }

    if check:
        diffs = []
        for path, content in targets.items():
            rel = os.path.relpath(path, REPO_ROOT)
            try:
                with open(path, encoding="utf-8") as fh:
                    on_disk = fh.read()
            except FileNotFoundError:
                diffs.append(f"{rel}: missing on disk")
                continue
            if on_disk != content:
                diffs.append(f"{rel}: differs from generated output")
        if diffs:
            for d in diffs:
                print(f"CHECK FAIL: {d}", file=sys.stderr)
            print(f"\n{len(diffs)} file(s) out of date. Run: python3 scripts/doc_index.py", file=sys.stderr)
            sys.exit(1)
        print(f"--check OK: {len(targets)} files match (decisioni: {len(decisions)}, backlog: {len(backlog)}).")
        sys.exit(0)

    for path, content in targets.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    print(f"Generated {len(targets)} files (decisioni: {len(decisions)}, backlog: {len(backlog)}).")
    for path in targets:
        print(f"  - {os.path.relpath(path, REPO_ROOT)}")


if __name__ == "__main__":
    main()
