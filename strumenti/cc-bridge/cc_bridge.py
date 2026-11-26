#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Maurizio Acampora
"""cc-bridge: server MCP (stdio) che fa parlare la chat di Claude con Claude Code CLI dentro WSL.

Un solo file, solo libreria standard (Python >= 3.8): niente pip, niente venv.

Strumenti offerti alla chat
  cc_run         lancia un task di Claude Code in un progetto, o continua una sessione esistente
  cc_status      attende/legge un job (avanzamento, esito); senza job_id elenca i job recenti
  cc_cancel      ferma un job
  cc_sessions    elenca le sessioni di CC del progetto, comprese quelle aperte da terminale
  cc_transcript  legge la parte recente di una sessione (prompt, risposte, strumenti usati)
  cc_info        configurazione e diagnostica

Come funziona
  Ogni task e' un processo `claude -p --output-format stream-json` staccato dal server
  (sopravvive al riavvio di Claude Desktop), con l'output su file in ~/.cache/cc-bridge/jobs/<id>/.
  La chat riceve un job_id e fa polling: nessuna chiamata dura piu' di --max-wait secondi.
  Le sessioni sono normali sessioni di Claude Code: `claude --resume <session_id>` in terminale
  riprende quella avviata dalla chat, e la chat puo' continuare una sessione nata in terminale.

Avvio da claude_desktop_config.json (Windows), esempio:
  "command": "wsl.exe",
  "args": ["-d", "Ubuntu-24.04", "-e", "/usr/bin/python3",
           "/home/<utente>/projects/cc-bridge/cc_bridge.py", "--roots", "/home/<utente>/projects/<progetto>"]
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
import traceback
import uuid
from collections import deque
from datetime import datetime
from pathlib import Path

VERSION = "1.0.5"

# Revisioni MCP dell'era "initialize" parlate da questo server. La 2026-07-28 (stateless) non e'
# implementata: i client nuovi la sondano con server/discover, ricevono -32601 e ripiegano su
# initialize, come prevede la specifica per i server stdio.
SUPPORTED_PROTOCOLS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")

MODE_FLAGS = {
    "plan": ["--permission-mode", "plan"],
    "edit": ["--permission-mode", "acceptEdits"],
    "auto": ["--permission-mode", "auto"],
    "full": ["--permission-mode", "bypassPermissions"],
}
MODE_RANK = {"plan": 0, "edit": 1, "auto": 2, "full": 3}
CLI_MODE_NAME = {"plan": "plan", "edit": "acceptEdits", "auto": "auto", "full": "bypassPermissions"}
EFFORTS = ("low", "medium", "high", "xhigh", "max")  # ultracode: si attiva scrivendolo nel prompt
PERMISSION_PROMPTS_MIN = (2, 1, 259)  # versione di claude da cui esiste --permission-prompts

# Avvertenza anteposta a ogni prompt che arriva dalla chat. Sta nel messaggio utente e non nel
# system prompt: se la sessione viene ripresa in terminale, i turni digitati da te restano
# interattivi, e il transcript distingue i turni arrivati dalla chat.
WRAP_OPEN, WRAP_CLOSE = "<cc-bridge>", "</cc-bridge>"
WRAPPER = (
    WRAP_OPEN + "\n"
    "This message comes from the user's chat assistant (Claude, in the Claude app) through "
    "cc-bridge, not from the user typing in this terminal. This turn runs non-interactively: "
    "nobody can answer questions or approve prompts until it ends. Do not ask; pick the most "
    "reasonable interpretation and state it. Reply in the language of the request. Unless the "
    "request or the project's instructions define a report format, end with a short report: "
    "what you did, files changed, commands run, what is left open.\n"
    + WRAP_CLOSE + "\n\n"
)

INSTRUCTIONS = (
    "cc-bridge connects you to Claude Code (CC) running in the user's WSL. CC works inside the "
    "project with its own CLAUDE.md, settings, hooks, subagents and MCP servers, and cannot see "
    "this chat. For work that edits files or runs commands, prefer a short prompt that points CC to a "
    "task file in the repo (e.g. 'Run docs/tasks/x.md, stop at its checks, end with a one-line "
    "outcome'), with the steps, commands and expected values in the file, where the user can review "
    "them. In auto mode CC's safety classifier judges each command in the light of the prompt: do not put "
    "encoded code (base64 and similar) or long instructions in the prompt, and prefer short separate "
    "commands to long && chains. If CC reports a command denied, do not resume the session asking for "
    "a variant or a workaround: tell the user the command and the reason, and let them decide (run it "
    "themselves, allow it in .claude/settings.json, or change the task). A denial whose text says the "
    "classifier gave no verdict is a transient failure of the check, not a judgment: CC may retry it once as-is, "
    "and it is not a denial to report. "
    "Flow: cc_run; if state=running, call cc_status(job_id) until it is done, telling the user "
    "briefly what CC is doing. Modes: plan = read-only analysis (default); edit = may edit files; "
    "auto = edits and commands reviewed by CC's safety classifier (use it when CC must run tests "
    "or builds); full = no permission checks, only if the user enabled it. cc_sessions and "
    "cc_transcript show what the user did in CC from the terminal; pass resume=<session id> to "
    "cc_run to continue a session (fork=true if it may still be open in a terminal). Jobs survive "
    "restarts: cc_status without job_id lists recent jobs. To wait for a long job in few calls, pass "
    "a large wait_seconds to cc_status: the bridge caps it to what this client tolerates and says so; "
    "if a call still ends in a client timeout, the job keeps running, call cc_status again."
)

# Attese lunghe. Una chiamata inoltrata da Claude Desktop (anche dalla chat collegata al PC) cade a
# 60 s e il risultato va perso: misurato il 2026-10-15, senza progressToken e senza
# notifications/cancelled. Per questo senza avanzamento l'attesa resta sotto --max-wait (50 s). Se un
# altro client chiede l'avanzamento (progressToken) il bridge lo manda ogni PROGRESS_EVERY secondi e
# concede fino a --max-wait-progress; se quel client annulla comunque la chiamata per timeout, il
# bridge registra il limite osservato in client.json e da li' in poi resta sotto.
PROGRESS_EVERY = float(os.environ.get("CC_BRIDGE_PROGRESS_EVERY", "10"))
MIN_LEARN_SECONDS = float(os.environ.get("CC_BRIDGE_MIN_LEARN", "20"))
CTX = threading.local()  # contesto della richiesta tools/call servita da questo thread
ACTIVE = {}  # id della richiesta (json) -> contesto, per notifications/cancelled
ACTIVE_LOCK = threading.Lock()
CLIENT = {"timeout": None, "learned_at": None, "progress_seen": None}

# Nome pubblico dell'id di sessione: resume (cc_run) e cc_session (cc_transcript). Alcuni proxy MCP
# tolgono dagli argomenti una chiave chiamata session_id; i vecchi nomi restano accettati come alias.
SESSION_ARG_NAMES = ("resume", "cc_session", "session", "session_id", "id")

CFG = None  # argparse.Namespace, impostato in main()
CLAUDE_BIN = None
_CLAUDE_VERSION = None
_VERSION_LOCK = threading.Lock()
JOBS = {}
JOBS_LOCK = threading.Lock()
RUN_LOCK = threading.Lock()  # conteggio dei job attivi e avvio di uno nuovo sono un'unica operazione
OUT_LOCK = threading.Lock()


class ToolError(Exception):
    """Errore restituito alla chat come esito del tool (isError=true)."""


class RpcError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


# --------------------------------------------------------------------------- utilita'

def log(*parts):
    print("[cc-bridge]", *parts, file=sys.stderr, flush=True)


def one_line(text, limit):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def clip(text, limit):
    text = str(text)
    if len(text) <= limit:
        return text
    return text[:limit] + "\n…[truncated: %d more characters]" % (len(text) - limit)


def clip_ends(text, limit):
    """Taglia nel mezzo: l'inizio e la fine (dove CC mette la riga d'esito) restano."""
    text = str(text)
    if len(text) <= limit:
        return text
    head = int(limit * 0.6)
    tail = limit - head
    return "%s\n…[%d characters omitted]…\n%s" % (text[:head], len(text) - limit, text[-tail:])


def session_arg(args):
    for key in SESSION_ARG_NAMES:
        value = args.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def clamp_int(value, default, lo, hi):
    try:
        value = int(value)
    except (TypeError, ValueError, OverflowError):
        return default
    return max(lo, min(hi, value))


def safe_mtime(path):
    try:
        return os.path.getmtime(str(path))
    except OSError:
        return 0.0


def fmt_secs(seconds):
    s = max(0, int(seconds))
    if s >= 3600:
        return "%dh%02dm" % (s // 3600, (s % 3600) // 60)
    if s >= 60:
        return "%dm%02ds" % (s // 60, s % 60)
    return "%ds" % s


def _to_dt(ts):
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts)
    text = str(ts).replace("Z", "+00:00")
    text = re.sub(r"\.(\d{6})\d+", r".\1", text)  # Python < 3.11 accetta al massimo 6 decimali
    return datetime.fromisoformat(text).astimezone()


def fmt_time(ts):
    try:
        return _to_dt(ts).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "?"


def fmt_hm(ts):
    try:
        return _to_dt(ts).strftime("%H:%M")
    except Exception:
        return "--:--"


def read_tail(path, limit):
    try:
        with open(str(path), "rb") as fh:
            fh.seek(0, os.SEEK_END)
            size = fh.tell()
            fh.seek(max(0, size - limit))
            return fh.read().decode("utf-8", "replace").strip()
    except OSError:
        return ""


UNC_RE = re.compile(r"^[\\/]{2}wsl(?:\$|\.localhost)[\\/][^\\/]+([\\/].*)?$", re.I)
WIN_RE = re.compile(r"^([A-Za-z]):(?:[\\/](.*))?$")


def to_linux_path(p):
    """Accetta anche percorsi Windows o UNC di WSL e li porta nello spazio Linux."""
    p = str(p).strip().strip('"').strip("'")
    if "\x00" in p:
        raise ToolError("Invalid path (contains a NUL byte).")
    m = UNC_RE.match(p)
    if m:
        return (m.group(1) or "/").replace("\\", "/")
    m = WIN_RE.match(p)
    if m:
        return "/mnt/%s/%s" % (m.group(1).lower(), (m.group(2) or "").replace("\\", "/"))
    return os.path.expanduser(p)


def roots():
    return [Path(to_linux_path(r)).resolve() for r in CFG.roots]


def within_roots(path):
    try:
        p = Path(path).resolve()
    except (OSError, RuntimeError, ValueError):
        return False
    return any(p == r or r in p.parents for r in roots())


def check_dir(cwd):
    p = Path(to_linux_path(cwd)).resolve()
    if not within_roots(p):
        raise ToolError(
            "%s is outside the allowed roots (%s). The user can widen them with --roots in "
            "claude_desktop_config.json." % (p, ", ".join(map(str, roots()))))
    if not p.is_dir():
        raise ToolError("Directory not found in WSL: %s" % p)
    return p


# --------------------------------------------------------------------------- claude CLI

def find_claude(explicit):
    if explicit:
        p = to_linux_path(explicit)
        return p if os.path.isfile(p) and os.access(p, os.X_OK) else None
    home = Path.home()
    cands = [str(home / ".local/bin/claude"), str(home / ".claude/local/claude")]
    found = shutil.which("claude")
    if found and not found.startswith("/mnt/"):  # mai il claude di Windows via interop
        cands.append(found)
    cands += [str(home / ".npm-global/bin/claude"), "/usr/local/bin/claude", "/usr/bin/claude"]
    cands += sorted(glob.glob(str(home / ".nvm/versions/node/*/bin/claude")), reverse=True)
    for c in cands:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


def child_env():
    env = dict(os.environ)
    extra = [os.path.dirname(CLAUDE_BIN)] if CLAUDE_BIN else []
    extra.append(str(Path.home() / ".local/bin"))
    env["PATH"] = os.pathsep.join(extra + [env.get("PATH") or "/usr/local/bin:/usr/bin:/bin"])
    env.pop("CLAUDECODE", None)  # altrimenti claude si crede annidato in un'altra sessione
    if CFG.claude_config_dir:  # claude deve scrivere le sessioni dove il bridge le legge
        env["CLAUDE_CONFIG_DIR"] = to_linux_path(CFG.claude_config_dir)
    if not CFG.keep_api_key:
        # con una chiave API nell'ambiente claude fatturerebbe sull'API invece dell'abbonamento
        env.pop("ANTHROPIC_API_KEY", None)
        env.pop("ANTHROPIC_AUTH_TOKEN", None)
    return env


def run_claude_quick(args, timeout=15):
    if not CLAUDE_BIN:
        return ""
    try:
        r = subprocess.run([CLAUDE_BIN] + args, capture_output=True, text=True, timeout=timeout,
                           env=child_env(), stdin=subprocess.DEVNULL)
        return (r.stdout or r.stderr or "").strip()
    except Exception as e:  # noqa: BLE001 - diagnostica, mai fatale
        return "error: %s" % e


def claude_version():
    """(tupla, testo) della versione di claude, calcolata una volta sola."""
    global _CLAUDE_VERSION
    with _VERSION_LOCK:
        if _CLAUDE_VERSION is None:
            out = run_claude_quick(["--version"])
            first = out.splitlines()[0] if out else ""
            m = re.search(r"(\d+)\.(\d+)\.(\d+)", first)
            _CLAUDE_VERSION = (tuple(int(x) for x in m.groups()) if m else None, first or "?")
        return _CLAUDE_VERSION


def auth_summary():
    out = run_claude_quick(["auth", "status"])
    try:
        data = json.loads(out)
    except ValueError:
        return one_line(out or "?", 200)
    bits = []
    for key in ("loggedIn", "authMethod", "subscriptionType", "email"):
        if key in data:
            bits.append("%s=%s" % (key, data[key]))
    return ", ".join(bits) or one_line(out, 200)


# --------------------------------------------------------------------------- sessioni di CC
# Il formato dei transcript e' interno a Claude Code e cambia tra versioni: la lettura e'
# difensiva e, se non trova nulla, suggerisce di chiedere a CC stesso (resume con fork).

SID_RE = re.compile(r"^[0-9A-Za-z][0-9A-Za-z_-]{7,80}$")
NOISE_PREFIXES = ("<command-", "<local-command", "Caveat:", "[Request interrupted", "<bash-",
                  "<task-notification", "<user-memory-input")
SYSREM_RE = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
WRAP_RE = re.compile(re.escape(WRAP_OPEN) + r".*?" + re.escape(WRAP_CLOSE) + r"\s*", re.S)
CMD_NAME_RE = re.compile(r"<command-name>\s*(.*?)\s*</command-name>", re.S)
CMD_ARGS_RE = re.compile(r"<command-args>(.*?)</command-args>", re.S)
PASTE_RE = re.compile(r"</?pasted_content\b[^>]*>")
SUMMARY_KEYS = ("command", "file_path", "path", "pattern", "url", "query", "description",
                "prompt", "notebook_path", "skill", "subject")


def projects_dir():
    base = CFG.claude_config_dir or os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude")
    return Path(to_linux_path(base)) / "projects"


def encode_project(path):
    # ~/.claude/projects/<cwd con i caratteri non alfanumerici sostituiti da "-">, max 200 caratteri
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))[:200]


def find_session(sid):
    sid = (sid or "").strip()
    if not sid:
        raise ToolError("Missing session id: pass cc_session=<id> to cc_transcript, resume=<id> to cc_run.")
    if not SID_RE.match(sid):
        raise ToolError("Invalid session id: %r" % sid)
    hits = glob.glob(str(projects_dir() / "*" / (sid + ".jsonl")))
    if not hits:
        return None
    hits.sort(key=safe_mtime, reverse=True)
    return Path(hits[0])


def message_text(entry):
    msg = entry.get("message")
    if not isinstance(msg, dict):
        return None
    content = msg.get("content")
    if isinstance(content, str):
        parts = [content]
    elif isinstance(content, list):
        parts = [b.get("text") or "" for b in content if isinstance(b, dict) and b.get("type") == "text"]
    else:
        return None
    return "\n".join(p for p in parts if p).strip() or None


def parse_user_text(text):
    """(testo leggibile o None, arrivato_dalla_chat, e'_un_comando_slash).

    I comandi digitati in terminale (/loop, /model...) sono registrati come
    <command-name>/loop</command-name><command-args>...</command-args>: diventano "/loop ...".
    """
    if not text:
        return None, False, False
    via_chat = WRAP_OPEN in text
    if text.lstrip().startswith(("<command-name>", "<command-message>")):
        m = CMD_NAME_RE.search(text)
        if m and m.group(1):
            name = m.group(1) if m.group(1).startswith("/") else "/" + m.group(1)
            a = CMD_ARGS_RE.search(text)
            args = (a.group(1) if a else "").strip()
            return (name + " " + args if args else name), via_chat, True
    text = PASTE_RE.sub("", SYSREM_RE.sub("", WRAP_RE.sub("", text))).strip()
    if not text or text.startswith(NOISE_PREFIXES):
        return None, via_chat, False
    return text, via_chat, False


ORIGIN_LABEL = {"chat": "CHAT->CC", "script": "SCRIPT", "terminal": "USER"}


def entry_origin(entry, via_chat):
    """Da dove arriva un prompt: chat (via cc-bridge), script (claude -p / SDK), terminale o altro."""
    if via_chat:
        return "chat"
    ep = str(entry.get("entrypoint") or "")
    if entry.get("promptSource") == "sdk" or ep.startswith("sdk"):
        return "script"
    if ep in ("", "cli"):
        return "terminal"
    return ep  # es. un'estensione IDE o l'app desktop


def origin_label(entry, via_chat):
    origin = entry_origin(entry, via_chat)
    label = ORIGIN_LABEL.get(origin, "USER[%s]" % origin)
    turn = entry.get("turnOrigin")
    if origin != "chat" and isinstance(turn, str) and turn not in ("human", "sdk"):
        label += "(%s)" % turn  # turno non digitato, es. un risveglio di /loop
    return label


def tool_summary(name, inp):
    name = name or "?"
    if isinstance(inp, dict):
        for key in SUMMARY_KEYS:
            v = inp.get(key)
            if isinstance(v, str) and v.strip():
                return "%s: %s" % (name, one_line(v, 160))
    return str(name)


def block_text(content):
    """Testo di un tool_result: stringa, oppure lista di blocchi {"type": "text"}."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "\n".join(str(b.get("text") or "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text").strip()
    return ""


def remember(store, key, value, limit=500):
    """Inserisce in un dizionario limitato: oltre `limit` voci esce la piu' vecchia."""
    if not isinstance(key, str):
        return
    store.pop(key, None)
    store[key] = value
    while len(store) > limit:
        store.pop(next(iter(store)))


# Il motivo di un rifiuto arriva a CC come testo del tool_result, con un'etichetta fra parentesi
# quadre (es. "[Auto-Mode Bypass]"). Il formato non e' documentato: se l'etichetta manca si mostra il testo.
REASON_TAG_RE = re.compile(r"\[([A-Z][A-Za-z0-9 ,.'/&+-]{2,60})\]")


def denial_reason(text):
    m = REASON_TAG_RE.search(text or "")
    return m.group(1).strip() if m else None


# Un verdetto mancato del classificatore non e' un giudizio: il testo stesso consente di riprovare una volta.
# Testo visto con claude 2.1.300 (giro del 2026-10-15): "The server-side auto mode classifier gave no verdict
# (error) ... This is a transient failure of the check, not a judgment about the action".
NO_VERDICT_RE = re.compile(r"gave no verdict|transient failure of the check", re.I)


def fingerprint(value):
    """Impronta dell'input di una chiamata, per riconoscere la stessa chiamata ripetuta com'era."""
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha1(raw.encode("utf-8", "replace")).hexdigest()[:16]


def iter_jsonl(chunk):
    for raw in chunk.splitlines():
        try:
            e = json.loads(raw)
        except ValueError:
            continue
        if isinstance(e, dict):
            yield e


def session_head(path, max_bytes=262144):
    info = {"cwd": None, "first": None, "title": None, "origin": None}
    try:
        with open(str(path), "rb") as fh:
            chunk = fh.read(max_bytes)
    except OSError:
        return info
    for e in iter_jsonl(chunk):
        if not info["cwd"] and isinstance(e.get("cwd"), str):
            info["cwd"] = e["cwd"]
        t = str(e.get("type") or "")
        if not info["title"]:
            if t == "summary" and isinstance(e.get("summary"), str):
                info["title"] = e["summary"].strip() or None
            elif "title" in t:
                for key in ("customTitle", "aiTitle", "title"):
                    if isinstance(e.get(key), str) and e[key].strip():
                        info["title"] = e[key].strip()
                        break
        if t == "user" and not e.get("isSidechain"):
            if info["origin"] is None:
                info["origin"] = entry_origin(e, False)
            if not info["first"] and not e.get("isMeta"):
                text, via, is_cmd = parse_user_text(message_text(e))
                if via:
                    info["origin"] = "chat"
                # come etichetta conta il primo prompt vero; /login, /clear e simili senza argomenti no
                if text and not (is_cmd and " " not in text):
                    info["first"] = text
        if info["cwd"] and info["first"] and info["title"]:
            break
    return info


def read_jsonl_tail(path, max_bytes):
    try:
        with open(str(path), "rb") as fh:
            fh.seek(0, os.SEEK_END)
            size = fh.tell()
            if size > max_bytes:
                fh.seek(size - max_bytes)
                fh.readline()  # scarta la riga troncata
            else:
                fh.seek(0)
            chunk = fh.read()
    except OSError:
        return []
    return list(iter_jsonl(chunk))


def tool_sessions(args):
    limit = clamp_int(args.get("limit"), 10, 1, 50)
    target = check_dir(args["cwd"]) if args.get("cwd") else None
    pdir = projects_dir()
    if not pdir.is_dir():
        return "No Claude Code sessions on this machine yet (%s does not exist)." % pdir
    bases = [target] if target is not None else roots()
    prefixes = [encode_project(b) for b in bases]
    subdirs = [d for d in pdir.iterdir() if d.is_dir()]
    dirs = [d for d in subdirs if any(d.name.startswith(p) for p in prefixes)] or subdirs
    files = [f for d in dirs for f in d.glob("*.jsonl")]
    files.sort(key=safe_mtime, reverse=True)
    rows = []
    for f in files:
        if len(rows) >= limit:
            break
        head = session_head(f)
        if not head["cwd"]:
            continue
        cwd = Path(head["cwd"]).resolve()
        if target is not None:
            if not (cwd == target or target in cwd.parents):
                continue
        elif not within_roots(cwd):
            continue
        label = head["title"] or head["first"] or "(no prompt)"
        rows.append("- %s | %s | started from %s | %s\n  %s" % (
            f.stem, fmt_time(safe_mtime(f)), head["origin"] or "?", head["cwd"], one_line(label, 160)))
    where = str(target) if target is not None else "the allowed roots"
    if not rows:
        return "No Claude Code sessions found under %s." % where
    return ("Claude Code sessions under %s, most recent activity first (session | last activity | origin | "
            "cwd). Read one with cc_transcript(cc_session=...), continue it with cc_run(resume=...), or in a "
            "terminal: claude --resume <session>\n" % where) + "\n".join(rows)


def tool_transcript(args):
    sid = session_arg(args) or ""
    f = find_session(sid)
    if f is None:
        raise ToolError("Session %s not found under %s." % (sid, projects_dir()))
    head = session_head(f)
    if not head["cwd"] or not within_roots(head["cwd"]):
        raise ToolError("Session %s belongs to a directory outside the allowed roots." % sid)
    last = clamp_int(args.get("last"), 30, 1, 300)
    with_tools = args.get("include_tools", True) is not False
    lines = []
    for e in read_jsonl_tail(f, 8 * 1024 * 1024):
        if e.get("isSidechain") or e.get("isMeta"):
            continue
        t = e.get("type")
        when = fmt_hm(e.get("timestamp"))
        if t == "user":
            text, via, _ = parse_user_text(message_text(e))
            if text:
                lines.append("[%s] %s: %s" % (when, origin_label(e, via), clip(text, 2000)))
        elif t == "assistant":
            content = (e.get("message") or {}).get("content")
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            for b in content if isinstance(content, list) else []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and str(b.get("text") or "").strip():
                    lines.append("[%s] CC: %s" % (when, clip(b["text"].strip(), 3000)))
                elif b.get("type") == "tool_use" and with_tools:
                    lines.append("        -> " + tool_summary(b.get("name"), b.get("input")))
    if not lines:
        return ("No readable messages in session %s. The transcript format is internal to Claude Code "
                "and may have changed: ask CC itself instead, e.g. cc_run(resume=\"%s\", fork=true, "
                "prompt=\"Summarize this session\")." % (sid, sid))
    shown = lines[-last:]
    header = ("Session %s | %s | last activity %s | showing %d of %d entries (USER = typed in the terminal, "
              "USER(x) = turn started by x, e.g. a /loop wakeup, CHAT->CC = sent through cc-bridge, "
              "SCRIPT = claude -p or SDK):"
              % (sid, head["cwd"], fmt_time(safe_mtime(f)), len(shown), len(lines)))
    return header + "\n" + "\n".join(shown)


# --------------------------------------------------------------------------- job

JOB_ID_RE = re.compile(r"^[0-9a-f]{12}$")


def jobs_root():
    return Path(to_linux_path(CFG.state_dir)) / "jobs"


def client_state_path():
    return Path(to_linux_path(CFG.state_dir)) / "client.json"


def load_client_state():
    try:
        data = json.loads(client_state_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    if isinstance(data.get("timeout"), (int, float)):
        CLIENT["timeout"] = data["timeout"]
        CLIENT["learned_at"] = data.get("learned_at")


def learn_client_timeout(elapsed):
    """Il client ha annullato una chiamata per timeout dopo `elapsed` secondi: d'ora in poi si resta sotto."""
    value = int(elapsed)
    if CLIENT["timeout"] is not None and CLIENT["timeout"] <= value:
        return
    CLIENT["timeout"] = value
    CLIENT["learned_at"] = time.time()
    try:
        client_state_path().write_text(json.dumps({"timeout": value, "learned_at": CLIENT["learned_at"]}),
                                       encoding="utf-8")
    except OSError:
        pass
    log("client timed out a call after %ds: waits now capped at %ds" % (value, wait_cap(True)[0]))


def wait_cap(has_progress):
    """(tetto in secondi, motivo)."""
    if has_progress:
        cap, why = CFG.max_wait_progress, "the client reports progress"
    else:
        cap, why = CFG.max_wait, ("this client does not ask for progress updates, and calls relayed by Claude "
                                  "Desktop end after 60 s")
    if CLIENT["timeout"] is not None:
        learned = max(5, int(CLIENT["timeout"]) - 8)
        if learned < cap:
            cap, why = learned, "this client timed out a call after %ds" % CLIENT["timeout"]
    return cap, why


def effective_wait(args):
    """(secondi da attendere, nota o None) per la chiamata in corso."""
    ctx = getattr(CTX, "req", None)
    cap, why = wait_cap(bool(ctx and ctx.get("token") is not None))
    want = clamp_int(args.get("wait_seconds"), CFG.default_wait, 0, 86400)
    if want > cap:
        return cap, "wait capped at %ds (%s)" % (cap, why)
    return want, None


class Cursor(object):
    """Legge out.jsonl in modo incrementale e ne tiene il riassunto."""

    def __init__(self):
        self.pos = 0
        self.buf = b""
        self.session_id = None
        self.model = None
        self.cli_mode = None
        self.key_source = None
        self.cc_version = None
        self.rate_limit = None
        self.seq = 0
        self.recent = deque(maxlen=10)  # (seq, testo): chi interroga vede solo le voci nuove
        self.tools = 0
        self.uses = {}  # tool_use_id -> (nome, riassunto) delle chiamate recenti
        self.calls = deque(maxlen=2000)  # (tool_use_id, nome, impronta dell'input), in ordine
        self.ok = {}  # tool_use_id delle chiamate con un esito senza errore
        self.errors = {}  # tool_use_id -> testo dell'errore che CC ha ricevuto (rifiuti compresi)
        self.live_denials = 0  # eventi permission_denied visti durante il giro
        self.result = None
        self.plan = None
        self.noise = deque(maxlen=5)

    def feed(self, path, final=False):
        try:
            with open(str(path), "rb") as fh:
                fh.seek(self.pos)
                data = fh.read()
        except OSError:
            data = b""
        self.pos += len(data)
        data = self.buf + data
        lines = data.split(b"\n")
        self.buf = b"" if final else lines.pop()
        for raw in lines:
            raw = raw.strip()
            if not raw:
                continue
            try:
                ev = json.loads(raw)
            except ValueError:
                self.noise.append(raw.decode("utf-8", "replace")[:300])
                continue
            if isinstance(ev, dict):
                self.handle(ev)

    def add(self, text):
        self.seq += 1
        self.recent.append((self.seq, text))

    def handle(self, ev):
        t = ev.get("type")
        if isinstance(ev.get("session_id"), str):
            self.session_id = ev["session_id"]
        sub = "(subagent) " if ev.get("parent_tool_use_id") else ""
        if t == "system":
            st = ev.get("subtype")
            if st == "init":
                self.model = ev.get("model") or self.model
                self.cli_mode = ev.get("permissionMode") or self.cli_mode
                self.key_source = ev.get("apiKeySource") or self.key_source
                self.cc_version = ev.get("claude_code_version") or self.cc_version
            elif st == "api_retry":
                self.add("! API retry %s/%s (%s)" % (
                    ev.get("attempt"), ev.get("max_retries"), ev.get("error")))
            elif st == "permission_denied":
                self.live_denials += 1
                why = next((str(ev[k]) for k in ("reason", "message", "decision_reason") if ev.get(k)), "")
                self.add("x denied: " + tool_summary(ev.get("tool_name"), ev.get("tool_input"))
                         + (" (%s)" % one_line(why, 160) if why else ""))
        elif t == "assistant":
            content = (ev.get("message") or {}).get("content")
            for b in content if isinstance(content, list) else []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and str(b.get("text") or "").strip():
                    self.add(sub + "* " + one_line(b["text"], 220))
                elif b.get("type") == "tool_use":
                    self.tools += 1
                    inp = b.get("input") if isinstance(b.get("input"), dict) else {}
                    if b.get("name") == "ExitPlanMode" and inp.get("plan"):
                        self.plan = str(inp["plan"])
                    summary = tool_summary(b.get("name"), inp)
                    remember(self.uses, b.get("id"), (b.get("name"), summary))
                    self.calls.append((b.get("id"), b.get("name"), fingerprint(b.get("input"))))
                    self.add(sub + "-> " + summary)
        elif t == "user":
            # esiti degli strumenti: si tengono solo gli errori, dove arrivano anche i rifiuti
            content = (ev.get("message") or {}).get("content")
            for b in content if isinstance(content, list) else []:
                if not (isinstance(b, dict) and b.get("type") == "tool_result"):
                    continue
                if not b.get("is_error"):
                    remember(self.ok, b.get("tool_use_id"), True, limit=2000)
                    continue
                text = block_text(b.get("content"))
                remember(self.errors, b.get("tool_use_id"), text[:2000])
                name, summary = self.uses.get(b.get("tool_use_id"), (None, "tool call"))
                if name != "ExitPlanMode":  # in plan e' negato sempre: non e' una notizia
                    self.add(sub + "x " + summary + " -> error: " + one_line(text or "(no text)", 160))
        elif t == "rate_limit_event" and isinstance(ev.get("rate_limit_info"), dict):
            self.rate_limit = ev["rate_limit_info"]
        elif t == "result":
            self.result = ev

    def usage_line(self):
        """Stato dei limiti d'uso dell'abbonamento, se CC lo ha riportato."""
        info = self.rate_limit
        if not info:
            return None
        windows = info.get("unifiedWindows") if isinstance(info.get("unifiedWindows"), dict) else {}
        bits = []
        for key, label in (("five_hour", "5-hour"), ("seven_day", "7-day")):
            w = windows.get(key)
            if isinstance(w, dict) and isinstance(w.get("utilization"), (int, float)):
                bits.append("%s window %d%%" % (label, round(w["utilization"] * 100)))
        status = info.get("status")
        if status and status != "allowed":
            bits.insert(0, "STATUS %s" % status)
        return ", ".join(bits) or None


def retry_outcome(cur, denial):
    """Se CC ha rifatto com'era la chiamata negata: "ran", "denied again", "no verdict again" o "no result";
    None se non l'ha rifatta."""
    tid = denial.get("tool_use_id")
    idx = next((i for i, c in enumerate(cur.calls) if c[0] == tid), None)
    if idx is None:
        return None
    _, name, fp = cur.calls[idx]
    for later_id, later_name, later_fp in list(cur.calls)[idx + 1:]:
        if later_name == name and later_fp == fp:
            if later_id in cur.ok:
                return "ran"
            if later_id in cur.errors:
                return "denied again" if NO_VERDICT_RE.search(cur.errors[later_id]) is None else "no verdict again"
            return "no result"
    return None


def denial_label(cur, denial):
    """(etichetta per il conteggio, verdetto mancato?, esito della ripetizione)."""
    why = cur.errors.get(denial.get("tool_use_id"))
    transient = bool(why and NO_VERDICT_RE.search(why))
    if transient:
        tag = "no verdict, transient"
    else:
        tag = denial_reason(why) or (one_line(why, 60) if why else "no reason in the output")
    outcome = retry_outcome(cur, denial)
    if outcome == "ran":
        tag += " -> ran on retry"
    elif outcome:
        tag += " -> retried: %s" % outcome
    return tag, transient, outcome


def save_meta(job):
    tmp = job["dir"] / "meta.json.tmp"
    tmp.write_text(json.dumps(scrub(job["meta"]), indent=1), encoding="utf-8")
    os.replace(str(tmp), str(job["dir"] / "meta.json"))


def load_job(job_id):
    job_id = (job_id or "").strip()
    if not JOB_ID_RE.match(job_id):
        raise ToolError("Invalid job_id: %r" % job_id)
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if job is None:
            jd = jobs_root() / job_id
            try:
                meta = json.loads((jd / "meta.json").read_text(encoding="utf-8"))
            except (OSError, ValueError):
                raise ToolError("Unknown job_id %s." % job_id)
            job = {"id": job_id, "dir": jd, "proc": None, "cursor": Cursor(), "meta": meta,
                   "lock": threading.Lock()}
            JOBS[job_id] = job
        return job


def proc_starttime(pid):
    """Istante di avvio del processo (campo 22 di /proc/<pid>/stat); None se assente o zombie."""
    try:
        with open("/proc/%d/stat" % pid, "rb") as fh:
            data = fh.read().decode("ascii", "replace")
        rest = data[data.rindex(")") + 2:].split()
        return None if rest[0] in ("Z", "X") else rest[19]
    except (OSError, ValueError, IndexError):
        return None


def is_alive(job):
    proc = job["proc"]
    if proc is not None:
        return proc.poll() is None
    meta = job["meta"]
    pid = meta.get("pid")
    if not pid or meta.get("ended"):
        return False
    if meta.get("starttime"):  # pid + istante di avvio: immune al riuso dei pid
        return proc_starttime(pid) == meta["starttime"]
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    try:
        with open("/proc/%d/cmdline" % pid, "rb") as fh:
            return b"claude" in fh.read()
    except OSError:
        return False


def live_jobs():
    """Job ancora in corso, compresi quelli lanciati da un'istanza precedente del server."""
    root = jobs_root()
    ids = [d.name for d in root.iterdir() if d.is_dir() and JOB_ID_RE.match(d.name)] if root.is_dir() else []
    live = []
    for job_id in ids:
        try:
            job = load_job(job_id)
        except ToolError:
            continue
        if not job["meta"].get("ended") and is_alive(job):
            live.append(job_id)
    return live


def snapshot(job):
    """Aggiorna lo stato del job e lo restituisce: running|done|error|failed|cancelled."""
    with job["lock"]:
        alive = is_alive(job)
        cur, meta = job["cursor"], job["meta"]
        out = job["dir"] / "out.jsonl"
        cur.feed(out, final=not alive)
        if not alive and "ended" not in meta:
            proc = job["proc"]
            meta["ended"] = time.time() if proc is not None else (safe_mtime(out) or time.time())
            if proc is not None:
                meta["exit_code"] = proc.returncode
            save_meta(job)
        if alive:
            return "running"
        if meta.get("cancelled"):
            return "cancelled"
        if cur.result is not None:
            res = cur.result
            failed = bool(res.get("is_error")) or res.get("subtype") not in (None, "success")
            return "error" if failed else "done"
        return "failed"


def last_activity(job):
    with job["lock"]:
        recent = job["cursor"].recent
        return recent[-1][1] if recent else "starting"


def send_progress(ctx, progress, total, message):
    params = {"progressToken": ctx["token"], "progress": round(progress, 1), "total": total}
    if message:
        params["message"] = one_line(message, 200)
    send({"jsonrpc": "2.0", "method": "notifications/progress", "params": params})


def wait_for(job, seconds):
    """Attende fino a `seconds`: manda l'avanzamento se il client lo chiede, smette se annulla."""
    ctx = getattr(CTX, "req", None)
    start = time.time()
    deadline = start + seconds
    next_ping = start + PROGRESS_EVERY
    while True:
        state = snapshot(job)
        now = time.time()
        if state != "running" or now >= deadline:
            return state
        if ctx is not None:
            if ctx["cancel"].is_set():
                return state
            if ctx.get("token") is not None and now >= next_ping:
                send_progress(ctx, now - start, seconds, last_activity(job))
                next_ping = now + PROGRESS_EVERY
            ctx["cancel"].wait(min(0.5, max(0.0, deadline - now)))
        else:
            time.sleep(0.5)


def render(job, state):
    with job["lock"]:  # un altro thread puo' star aggiornando lo stesso cursore
        return _render(job, state)


def _render(job, state):
    meta, cur = job["meta"], job["cursor"]
    res = cur.result or {}
    end = meta.get("ended") or time.time()
    lines = ["job_id: %s" % job["id"], "state: %s" % state,
             "elapsed: %s" % fmt_secs(end - meta.get("started", end)),
             "cwd: %s" % meta.get("cwd"), "mode: %s" % meta.get("mode")]
    if cur.session_id:
        lines.append("session: %s" % cur.session_id)
    wanted = CLI_MODE_NAME.get(meta.get("mode"))
    if cur.cli_mode and wanted and cur.cli_mode != wanted:
        lines.append("note: requested permission mode %s but Claude Code ran in %s (for example, auto "
                     "mode is not available for this model or account)." % (wanted, cur.cli_mode))
    if state == "running":
        if cur.live_denials:
            lines.insert(2, "denied so far: %d" % cur.live_denials)
        lines.append("progress: %d tool calls so far" % cur.tools)
        shown = job.get("shown_seq", 0)
        new = [text for seq, text in cur.recent if seq > shown]
        if new:
            lines.append("new activity since the last check:" if shown else "recent activity:")
            skipped = cur.seq - shown - len(new)
            if skipped > 0:
                lines.append("  (%d earlier events not shown)" % skipped)
            lines.extend("  " + t for t in new)
        elif shown:
            # la risposta precedente puo' essere andata persa (timeout del client): l'ultima voce si ripete
            last = cur.recent[-1][1] if cur.recent else "starting"
            lines.append("no new activity since the last check; latest: %s" % last)
        job["shown_seq"] = cur.seq
        if cur.result is not None:
            lines.append("latest result so far (Claude Code is still finishing background work):")
            lines.append(clip_ends(res.get("result") or "", 4000))
        lines.append('Still running: call cc_status(job_id="%s") to keep waiting, or cc_cancel to '
                     'stop it.' % job["id"])
        return "\n".join(lines), False
    stats = []
    if res.get("num_turns") is not None:
        stats.append("turns %s" % res["num_turns"])
    stats.append("tool calls %d" % cur.tools)
    if isinstance(res.get("total_cost_usd"), (int, float)):
        stats.append("cost estimate $%.2f (session total, API-equivalent)" % res["total_cost_usd"])
    if cur.model:
        stats.append("model %s" % cur.model)
    if isinstance(res.get("safety_stops"), int) and res["safety_stops"] > 0:
        stats.append("safety_stops %d" % res["safety_stops"])
    lines.append("stats: " + ", ".join(stats))
    # i comandi negati: il conteggio in testa, sotto lo stato; l'elenco con i motivi in fondo
    denials = [d for d in (res.get("permission_denials") or [])
               if isinstance(d, dict) and d.get("tool_name") != "ExitPlanMode"]
    labels = [denial_label(cur, d) for d in denials]
    if denials:
        tags = []
        for tag, _, _ in labels:
            if tag not in tags:
                tags.append(tag)
        lines.insert(2, "denied: %d (%s)" % (len(denials), "; ".join(tags)))
    usage = cur.usage_line()
    if usage:
        lines.append("subscription usage: %s" % usage)
    if cur.key_source and cur.key_source != "none":
        lines.append("billing: Claude Code authenticated with %s (API billing, not the subscription)."
                     % cur.key_source)
    text = res.get("result") if isinstance(res.get("result"), str) else ""
    if cur.plan and cur.plan.strip()[:200] not in text:
        lines.append("plan:")
        lines.append(clip_ends(cur.plan, CFG.max_output))
    if text:
        lines.append("result:")
        lines.append(clip_ends(text, CFG.max_output))
    elif state in ("failed", "error", "cancelled"):
        err = read_tail(job["dir"] / "err.log", 2000)
        if cur.noise:
            err = (err + "\n" + "\n".join(cur.noise)).strip()
        lines.append("exit code: %s" % meta.get("exit_code", "?"))
        lines.append("stderr: " + (err or "(empty)"))
    if cur.session_id:
        lines.append('continue from chat: cc_run(resume="%s", prompt=...)' % cur.session_id)
        lines.append("continue in a terminal: cd %s && claude --resume %s" % (
            shlex.quote(str(meta.get("cwd") or ".")), cur.session_id))
    if denials:
        lines.append("blocked by permissions, with the reason Claude Code was given:")
        for d, (_, _, outcome) in list(zip(denials, labels))[:15]:
            why = cur.errors.get(d.get("tool_use_id"))
            lines.append("  - " + tool_summary(d.get("tool_name"), d.get("tool_input")))
            lines.append("    reason: " + (one_line(why, 400) if why else "(not reported in the output)"))
            if outcome == "ran":
                lines.append("    then: Claude Code ran it again as-is, and it ran")
            elif outcome:
                lines.append("    then: Claude Code ran it again as-is: %s" % outcome)
        if len(denials) > 15:
            lines.append("  ... %d more" % (len(denials) - 15))
        if any(not transient for _, transient, _ in labels):
            lines.append("  (mode=%s) Do not resume the session asking for a variant or a workaround: show these "
                         "to the user, who decides: run them in a terminal, allow them in the project's "
                         ".claude/settings.json, or change the task." % meta.get("mode"))
        if any(transient for _, transient, _ in labels):
            lines.append("  Entries marked 'no verdict' were a transient failure of the check, not a judgment: "
                         "Claude Code may run them again once, as-is; they are not denials to report.")
    return "\n".join(lines), state in ("failed", "error")


def tool_run(args):
    t_call = time.time()
    prompt = scrub(str(args.get("prompt") or "")).strip()
    if not prompt:
        raise ToolError("prompt is required.")
    mode = str(args.get("mode") or "plan").strip()
    if mode not in MODE_FLAGS:
        raise ToolError("mode must be one of: plan, edit, auto, full.")
    if MODE_RANK[mode] > MODE_RANK[CFG.max_mode]:
        raise ToolError("mode=%s is above the ceiling set by the user (--max-mode %s). Use a lower mode, "
                        "or ask the user to raise --max-mode in claude_desktop_config.json."
                        % (mode, CFG.max_mode))
    if not CLAUDE_BIN:
        raise ToolError("Claude Code CLI not found in WSL: pass --claude /path/to/claude in the bridge "
                        "arguments, or install and log in to Claude Code in WSL.")
    effort = args.get("effort")
    if effort is not None and effort not in EFFORTS:
        raise ToolError("effort must be one of: %s." % ", ".join(EFFORTS))
    sid = session_arg(args)
    fork = bool(args.get("fork"))
    cwd = args.get("cwd")
    if sid and sid != "last":
        f = find_session(sid)
        if f is None:
            raise ToolError("Session %s not found." % sid)
        scwd = session_head(f)["cwd"]
        if not scwd:
            raise ToolError("Could not read the working directory of session %s." % sid)
        if cwd and Path(to_linux_path(cwd)).resolve() != Path(scwd).resolve():
            raise ToolError("Session %s belongs to %s, not %s." % (sid, scwd, cwd))
        cwd = scwd
    if not cwd:
        if len(CFG.roots) != 1:
            raise ToolError("cwd is required (unless resume is given or a single root is configured).")
        cwd = CFG.roots[0]
    wd = check_dir(cwd)
    with RUN_LOCK:
        job = start_job(wd, mode, prompt, sid, fork, args, effort)
    # l'attesa conta dall'inizio della chiamata, cosi' il totale resta sotto il tetto
    seconds, note = effective_wait(args)
    state = wait_for(job, max(0.0, seconds - (time.time() - t_call)))
    return with_note(render(job, state), state, note)


def start_job(wd, mode, prompt, sid, fork, args, effort):
    busy = live_jobs()
    if len(busy) >= CFG.max_jobs:
        raise ToolError("%d Claude Code jobs are already running (limit %d): %s. Wait for one to finish "
                        "or cancel it." % (len(busy), CFG.max_jobs, ", ".join(busy)))

    cmd = [CLAUDE_BIN, "-p", "--output-format", "stream-json", "--verbose"] + MODE_FLAGS[mode]
    vt, _ = claude_version()
    if vt and vt >= PERMISSION_PROMPTS_MIN:
        cmd += ["--permission-prompts", "none"]
    if sid == "last":
        cmd.append("--continue")
    elif sid:
        cmd += ["--resume", sid]
    if sid and fork:
        cmd.append("--fork-session")
    model = args.get("model") or CFG.model
    if model:
        cmd += ["--model", str(model)]
    if effort:
        cmd += ["--effort", effort]
    if args.get("max_turns"):
        cmd += ["--max-turns", str(clamp_int(args["max_turns"], 50, 1, 500))]

    job_id = uuid.uuid4().hex[:12]
    jd = jobs_root() / job_id
    jd.mkdir(parents=True)
    # il prompt passa da stdin: niente limiti di argv, e un "-" iniziale non diventa un'opzione
    (jd / "prompt.txt").write_text(prompt if CFG.no_preamble else WRAPPER + prompt, encoding="utf-8")
    meta = {"job_id": job_id, "cwd": str(wd), "mode": mode, "session_requested": sid, "fork": fork,
            "model": model, "effort": effort, "started": time.time(), "prompt": one_line(prompt, 300),
            "argv": cmd[1:]}
    with open(str(jd / "prompt.txt"), "rb") as fin, open(str(jd / "out.jsonl"), "wb") as fout, \
            open(str(jd / "err.log"), "wb") as ferr:
        # sessione propria: il job sopravvive se Claude Desktop chiude o riavvia il server
        proc = subprocess.Popen(cmd, cwd=str(wd), stdin=fin, stdout=fout, stderr=ferr,
                                env=child_env(), start_new_session=True, close_fds=True)
    meta["pid"] = proc.pid
    meta["starttime"] = proc_starttime(proc.pid)
    job = {"id": job_id, "dir": jd, "proc": proc, "cursor": Cursor(), "meta": meta,
           "lock": threading.Lock()}
    save_meta(job)
    with JOBS_LOCK:
        JOBS[job_id] = job
    log("job %s started: pid=%d cwd=%s mode=%s session=%s" % (job_id, proc.pid, wd, mode, sid or "new"))
    return job


def list_jobs(limit):
    root = jobs_root()
    dirs = [d for d in root.iterdir() if d.is_dir() and JOB_ID_RE.match(d.name)] if root.is_dir() else []
    dirs.sort(key=lambda d: safe_mtime(d / "prompt.txt"), reverse=True)
    rows = []
    for d in dirs[:limit]:
        try:
            job = load_job(d.name)
        except ToolError:
            continue
        state = snapshot(job)
        m = job["meta"]
        rows.append("- %s | %s | %s | %s | %s\n  %s" % (
            job["id"], state, fmt_time(m.get("started", 0)), m.get("mode"),
            job["cursor"].session_id or "-", one_line(m.get("prompt", ""), 160)))
    if not rows:
        return "No cc-bridge jobs yet."
    return ("Recent cc-bridge jobs, newest first (job_id | state | started | mode | session):\n"
            + "\n".join(rows))


def with_note(rendered, state, note):
    """Aggiunge la nota sul tetto d'attesa solo se il tetto ha davvero interrotto l'attesa."""
    text, is_error = rendered
    if note and state == "running":
        text += "\nnote: " + note
    return text, is_error


def tool_status(args):
    job_id = str(args.get("job_id") or "").strip()
    if not job_id:
        return list_jobs(clamp_int(args.get("limit"), 10, 1, 50))
    job = load_job(job_id)
    seconds, note = effective_wait(args)
    state = wait_for(job, seconds)
    return with_note(render(job, state), state, note)


def tool_cancel(args):
    job = load_job(str(args.get("job_id") or ""))
    if not is_alive(job):
        text, _ = render(job, snapshot(job))
        return "The job had already finished.\n" + text, False
    with job["lock"]:
        job["meta"]["cancelled"] = True
        save_meta(job)
    pid = job["meta"]["pid"]
    # SIGINT chiude il turno in modo ordinato; SIGTERM e SIGKILL solo se serve
    for sig, grace in ((signal.SIGINT, 5.0), (signal.SIGTERM, 3.0), (signal.SIGKILL, 2.0)):
        try:
            os.killpg(pid, sig)
        except ProcessLookupError:
            break
        except PermissionError:
            raise ToolError("Not allowed to signal process group %d." % pid)
        deadline = time.time() + grace
        while time.time() < deadline and is_alive(job):
            time.sleep(0.2)
        if not is_alive(job):
            break
    # processi del gruppo sopravvissuti al capo (es. comandi in background che ignorano SIGINT)
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(pid, sig)
        except (ProcessLookupError, PermissionError):
            break
        time.sleep(0.3)
    text, _ = render(job, snapshot(job))
    return text, False


def tool_info(args):
    vt, vtext = claude_version()
    unattended = bool(vt and vt >= PERMISSION_PROMPTS_MIN)
    lines = [
        "cc-bridge %s (python %s)" % (VERSION, sys.version.split()[0]),
        "claude: %s (%s)" % (CLAUDE_BIN or "NOT FOUND", vtext),
        "claude auth: %s" % (auth_summary() if CLAUDE_BIN else "-"),
        "allowed roots: %s" % ", ".join(map(str, roots())),
        "modes: default plan, ceiling %s" % CFG.max_mode,
        "default model: %s" % (CFG.model or "from Claude Code settings"),
        "permission prompts: %s" % ("none (unattended runs)" if unattended else
                                    "CLI older than 2.1.259: prompts are denied anyway in -p"),
        "ANTHROPIC_API_KEY passed to claude: %s" % ("yes" if CFG.keep_api_key else "no (subscription login)"),
        "sessions dir: %s" % projects_dir(),
        "jobs dir: %s (kept %d days)" % (jobs_root(), CFG.keep_days),
        "concurrent jobs: at most %d" % CFG.max_jobs,
        "waits per call: up to %ds when the client asks for progress updates, otherwise %ds (calls relayed "
        "by Claude Desktop end at 60 s: keep --max-wait below that)" % (CFG.max_wait_progress, CFG.max_wait),
        "this call asked for progress updates: %s" % ("yes" if CLIENT["progress_seen"] else "no"),
        "client timeout learned: %s" % (
            "%ds on %s (delete %s to forget it)" % (CLIENT["timeout"], fmt_time(CLIENT["learned_at"] or 0),
                                                     client_state_path())
            if CLIENT["timeout"] is not None else "none"),
        "effective cap for this client: %ds" % wait_cap(bool(CLIENT["progress_seen"]))[0],
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- MCP

TOOLS = [
    {
        "name": "cc_run",
        "title": "Run a Claude Code task",
        "description": (
            "Start a Claude Code (CC) task in a project inside the user's WSL, or continue an existing CC "
            "session. CC works autonomously with the repo and its own CLAUDE.md, settings, hooks, subagents "
            "and MCP servers, and cannot see this chat: give it a self-contained prompt; for work that edits "
            "files or runs commands, prefer a short prompt that points to a task file in the repo. Returns the "
            "result if CC finishes within wait_seconds, otherwise state=running and a job_id to poll with "
            "cc_status. Commands CC was denied are counted under the state and listed at the end, with the "
            "reason."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Task or message for Claude Code."},
                "cwd": {"type": "string", "description": (
                    "Project directory in WSL (Linux path). Optional when resume is given or when the "
                    "bridge has a single allowed root.")},
                "mode": {"type": "string", "enum": ["plan", "edit", "auto", "full"], "description": (
                    "plan (default) = read-only analysis. edit = may edit files; shell commands only if "
                    "allowed in CC's settings. auto = edits and commands reviewed by CC's safety classifier: "
                    "use it when CC must run tests or builds. full = no permission checks, only if the user "
                    "enabled it.")},
                "resume": {"type": "string", "description": (
                    "Continue this Claude Code session: its id (from cc_run, cc_sessions or the terminal), or "
                    "\"last\" for the most recent session in cwd.")},
                "fork": {"type": "boolean", "description": (
                    "With resume: continue in a copy with a new session id. Use it when the session may "
                    "still be open in a terminal.")},
                "model": {"type": "string", "description": (
                    "Optional model alias or name (e.g. sonnet, opus, fable). Default: CC settings.")},
                "effort": {"type": "string", "enum": list(EFFORTS), "description": (
                    "Optional effort level for this run. For an ultracode workflow, write the word "
                    "ultracode in the prompt instead.")},
                "max_turns": {"type": "integer", "minimum": 1, "maximum": 500,
                              "description": "Optional cap on agentic turns."},
                "wait_seconds": {"type": "integer", "minimum": 0, "description": (
                    "How long to wait before returning (default 25). The bridge caps it to what this client "
                    "tolerates (see cc_info) and says so in the reply.")},
            },
            "required": ["prompt"],
        },
        "annotations": {"readOnlyHint": False, "destructiveHint": True, "idempotentHint": False,
                        "openWorldHint": True},
    },
    {
        "name": "cc_status",
        "title": "Claude Code job status",
        "description": (
            "Wait for a Claude Code job started with cc_run and report it: recent activity while running, "
            "the final report when done. Without job_id, list recent jobs (they survive restarts)."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "job_id": {"type": "string", "description": "Job to check. Omit to list recent jobs."},
                "wait_seconds": {"type": "integer", "minimum": 0, "description": (
                    "Wait up to this long for the job to finish (default 25). For a long job pass a large value: "
                    "the bridge caps it to what this client tolerates and says so in the reply.")},
                "limit": {"type": "integer", "minimum": 1, "maximum": 50,
                          "description": "How many jobs to list when job_id is omitted (default 10)."},
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "cc_cancel",
        "title": "Stop a Claude Code job",
        "description": "Stop a running Claude Code job (graceful interrupt first, then terminate).",
        "inputSchema": {
            "type": "object",
            "properties": {"job_id": {"type": "string"}},
            "required": ["job_id"],
        },
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "openWorldHint": False},
    },
    {
        "name": "cc_sessions",
        "title": "List Claude Code sessions",
        "description": (
            "List recent Claude Code sessions in the allowed projects, including the ones the user ran in a "
            "terminal, with id, last activity, origin and first prompt. Use the ids with "
            "cc_transcript(cc_session=...) or cc_run(resume=...)."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "cwd": {"type": "string", "description": (
                    "Project directory (sessions in its subdirectories included). Omit for all allowed roots.")},
                "limit": {"type": "integer", "minimum": 1, "maximum": 50, "description": "Default 10."},
            },
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "cc_transcript",
        "title": "Read a Claude Code session",
        "description": (
            "Read the recent part of a Claude Code session: user prompts, Claude Code's replies and the tools "
            "it used. Use it to catch up on work the user did in the terminal before continuing it."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "cc_session": {"type": "string",
                               "description": "Claude Code session id (from cc_sessions or cc_run)."},
                "last": {"type": "integer", "minimum": 1, "maximum": 300,
                         "description": "How many entries from the end (default 30)."},
                "include_tools": {"type": "boolean", "description": "Show tool calls (default true)."},
            },
            "required": ["cc_session"],
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "cc_info",
        "title": "cc-bridge diagnostics",
        "description": (
            "Show the bridge configuration: claude binary, version and login, allowed roots, mode ceiling, "
            "limits. Use it first when something does not work."),
        "inputSchema": {"type": "object", "properties": {}},
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
]

HANDLERS = {
    "cc_run": tool_run,
    "cc_status": tool_status,
    "cc_cancel": tool_cancel,
    "cc_sessions": tool_sessions,
    "cc_transcript": tool_transcript,
    "cc_info": tool_info,
}


def scrub(obj):
    """Toglie i surrogati isolati (dati rotti nei transcript): i parser JSON rigorosi li rifiutano."""
    if isinstance(obj, str):
        try:
            obj.encode("utf-8")
            return obj
        except UnicodeEncodeError:
            return obj.encode("utf-8", "replace").decode("utf-8")
    if isinstance(obj, dict):
        return {k: scrub(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [scrub(v) for v in obj]
    return obj


def send(msg):
    # solo ASCII (niente U+2028 che spezzano le righe) e niente surrogati isolati
    data = (json.dumps(scrub(msg)) + "\n").encode("ascii")
    with OUT_LOCK:
        try:
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
        except (BrokenPipeError, ValueError):
            pass


def request_key(mid):
    return json.dumps(mid, sort_keys=True)


def call_tool(params, mid=None):
    """Esegue un tool; None se il client ha annullato la richiesta (allora non si risponde)."""
    name = params.get("name")
    args = params.get("arguments") if isinstance(params.get("arguments"), dict) else {}
    handler = HANDLERS.get(name) if isinstance(name, str) else None
    if handler is None:
        raise RpcError(-32602, "Unknown tool: %r" % (name,))
    meta = params.get("_meta") if isinstance(params.get("_meta"), dict) else {}
    token = meta.get("progressToken")
    ctx = {"token": token if isinstance(token, (str, int)) and not isinstance(token, bool) else None,
           "cancel": threading.Event(), "started": time.time()}
    CLIENT["progress_seen"] = ctx["token"] is not None
    key = request_key(mid)
    with ACTIVE_LOCK:
        ACTIVE[key] = ctx
    CTX.req = ctx
    try:
        out = handler(args)
        text, is_error = out if isinstance(out, tuple) else (out, False)
    except ToolError as e:
        text, is_error = str(e), True
    except Exception as e:  # noqa: BLE001 - un bug non deve far cadere il server
        log("tool %s failed: %s\n%s" % (name, e, traceback.format_exc()))
        text, is_error = "cc-bridge internal error in %s: %s" % (name, e), True
    finally:
        CTX.req = None
        with ACTIVE_LOCK:
            ACTIVE.pop(key, None)
    if ctx["cancel"].is_set():
        return None
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def on_cancelled(params):
    with ACTIVE_LOCK:
        ctx = ACTIVE.get(request_key(params.get("requestId")))
    if ctx is None:
        return
    ctx["cancel"].set()
    elapsed = time.time() - ctx["started"]
    reason = str(params.get("reason") or "")
    log("request cancelled by the client after %.0fs: %s" % (elapsed, reason or "no reason given"))
    if elapsed >= MIN_LEARN_SECONDS and re.search(r"time\s*d?\s*out|timeout", reason, re.I):
        learn_client_timeout(elapsed)


def dispatch(msg):
    mid = msg.get("id")
    method = msg.get("method")
    if not isinstance(method, str):
        return  # risposta a una richiesta che non abbiamo fatto
    params = msg.get("params") if isinstance(msg.get("params"), dict) else {}
    try:
        if method == "initialize":
            requested = str(params.get("protocolVersion") or "")
            version = requested if requested in SUPPORTED_PROTOCOLS else SUPPORTED_PROTOCOLS[0]
            result = {
                "protocolVersion": version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "cc-bridge", "title": "Claude Code bridge (WSL)", "version": VERSION},
                "instructions": INSTRUCTIONS,
            }
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            result = call_tool(params, mid)
            if result is None:
                return  # annullata dal client: niente risposta
        elif method == "resources/list":
            result = {"resources": []}
        elif method == "resources/templates/list":
            result = {"resourceTemplates": []}
        elif method == "prompts/list":
            result = {"prompts": []}
        elif method == "logging/setLevel":
            result = {}
        elif method == "notifications/cancelled":
            on_cancelled(params)
            return
        elif method.startswith("notifications/"):
            return
        else:
            raise RpcError(-32601, "Method not found: %s" % method)
    except RpcError as e:
        if mid is not None:
            send({"jsonrpc": "2.0", "id": mid, "error": {"code": e.code, "message": str(e)}})
        return
    except Exception as e:  # noqa: BLE001
        log("internal error on %s: %s\n%s" % (method, e, traceback.format_exc()))
        if mid is not None:
            send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": "Internal error: %s" % e}})
        return
    if mid is not None:
        send({"jsonrpc": "2.0", "id": mid, "result": result})


def serve():
    stdin = sys.stdin.buffer
    while True:
        raw = stdin.readline()
        if not raw:
            break
        raw = raw.strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except ValueError:
            send({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
            continue
        for m in (msg if isinstance(msg, list) else [msg]):
            if not isinstance(m, dict):
                continue
            if m.get("method") == "tools/call":
                # i tool possono attendere decine di secondi: non bloccano ping e altre chiamate
                threading.Thread(target=dispatch, args=(m,), daemon=True).start()
            else:
                dispatch(m)


def watch_parent(ppid):
    """Se wsl.exe se ne va senza chiudere stdin, il server non resta orfano. I job proseguono."""
    while True:
        time.sleep(5)
        if os.getppid() != ppid:
            log("parent process gone, exiting")
            os._exit(0)


def cleanup_jobs():
    root = jobs_root()
    if not root.is_dir():
        return
    limit = time.time() - CFG.keep_days * 86400
    for d in root.iterdir():
        if d.is_dir() and JOB_ID_RE.match(d.name) and safe_mtime(d / "prompt.txt") < limit:
            shutil.rmtree(str(d), ignore_errors=True)


def parse_args(argv):
    ap = argparse.ArgumentParser(
        prog="cc_bridge.py",
        description="Server MCP: la chat di Claude parla con Claude Code CLI in WSL.")
    ap.add_argument("--roots", nargs="+", default=[str(Path.home())], metavar="DIR",
                    help="cartelle in cui la chat puo' far lavorare CC (default: la home)")
    ap.add_argument("--max-mode", choices=list(MODE_FLAGS), default="auto",
                    help="modalita' piu' alta concessa alla chat (default: auto)")
    ap.add_argument("--claude", metavar="PATH", help="binario claude (default: ricerca automatica)")
    ap.add_argument("--model", help="modello di default dei task (default: impostazioni di CC)")
    ap.add_argument("--max-jobs", type=int, default=2, help="job contemporanei (default: 2)")
    ap.add_argument("--default-wait", type=int, default=25, help="attesa di default per chiamata, in s")
    ap.add_argument("--max-wait", type=int, default=50,
                    help="attesa massima per chiamata se il client non chiede l'avanzamento, in s")
    ap.add_argument("--max-wait-progress", type=int, default=600,
                    help="attesa massima per chiamata se il client chiede l'avanzamento, in s")
    ap.add_argument("--max-output", type=int, default=20000, help="caratteri massimi dell'esito")
    ap.add_argument("--state-dir", default=str(Path.home() / ".cache" / "cc-bridge"),
                    help="dove tenere i job (default: ~/.cache/cc-bridge)")
    ap.add_argument("--claude-config-dir", help="come CLAUDE_CONFIG_DIR (default: ~/.claude)")
    ap.add_argument("--keep-api-key", action="store_true",
                    help="lascia ANTHROPIC_API_KEY nell'ambiente di claude (fatturazione API)")
    ap.add_argument("--no-preamble", action="store_true",
                    help="non anteporre l'avvertenza cc-bridge ai prompt")
    ap.add_argument("--keep-days", type=int, default=14, help="giorni di conservazione dei job")
    ap.add_argument("--check", action="store_true", help="verifica la configurazione ed esce")
    return ap.parse_args(argv)


def main(argv=None):
    global CFG, CLAUDE_BIN
    CFG = parse_args(sys.argv[1:] if argv is None else argv)
    CFG.default_wait = max(0, min(CFG.default_wait, CFG.max_wait))
    CLAUDE_BIN = find_claude(CFG.claude)
    load_client_state()
    if CFG.check:
        print(tool_info({}))
        problems = []
        if not CLAUDE_BIN:
            problems.append("claude CLI not found (use --claude /path/to/claude)")
        problems += ["root does not exist: %s" % r for r in roots() if not r.is_dir()]
        print("OK" if not problems else "PROBLEMS:\n- " + "\n- ".join(problems))
        return 1 if problems else 0
    jobs_root().mkdir(parents=True, exist_ok=True)
    cleanup_jobs()
    threading.Thread(target=claude_version, daemon=True).start()  # pronta prima del primo cc_run
    threading.Thread(target=watch_parent, args=(os.getppid(),), daemon=True).start()
    log("v%s ready: claude=%s roots=%s max_mode=%s" % (
        VERSION, CLAUDE_BIN, ",".join(map(str, roots())), CFG.max_mode))
    try:
        serve()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
