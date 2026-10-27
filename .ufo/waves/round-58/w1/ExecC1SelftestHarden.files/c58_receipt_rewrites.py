#!/usr/bin/env python3
"""Round-58 C1 counter — calibration: every post-commit change to a measurement receipt is disclosed with its true values.

Surface: the lane's measurement receipts — every path ever committed under `.ufo/waves/round-<N>/control/` or
`.ufo/waves/round-<N>/controls/` (any round, any file name) in the first-parent-free ancestry of the measured tip — and the
lane's own statement about them, the disclosure ledger `.ufo/waves/round-58/receipt-rewrites.json`. The round-57
spot-check (`corpus/lessons/round-57-verifier-spotcheck.md` §5 D1) found `controls/after-c1-receipt-pins.txt` committed as
`pending` and filled in a later commit while the report said no receipt was rewritten; the round-57 counter
(`c57_receipt_pins.py`) watched `revision:` lines only, so a result-line rewrite passed it.

Event: one (path, commit) pair where a commit in the tip's ancestry modifies (`M`), deletes (`D`) or re-adds after a
deletion (`A` of a path that existed before) a receipt path (`git log --no-renames --name-status`, so a rename is a
deletion plus an addition and the deletion is an event). The first addition of a path is not an event.

Ledger entry (JSON list under `"events"`): {"path", "commit" (40 hex), "status" (M|D|A), "fromBlob", "toBlob" (40 hex, or
null for the deleted/absent side), "kind" (relabel|fill|rerun|append|format|delete|readd), "note" (non-empty)}.
An entry matches an event when path, commit and status are equal AND fromBlob/toBlob equal the blob ids git shows for
the path at the commit's first parent and at the commit.

Counts:
  events            receipt events in the ancestry of the tip
  undisclosed       events no ledger entry matches
  phantom           ledger entries that match no event (wrong commit, wrong blob, invented path, duplicate)
  malformed         ledger entries missing a field, with an unknown kind, or an empty note
  wrong_kind        matched entries whose `kind` differs from the counter's classification of the event (`classify`):
                    D -> delete; re-added A -> readd; M: the new bytes extend the old -> append; equal after whitespace
                    normalisation -> format; every changed line carries a 40-hex revision or a `revision` key -> relabel;
                    the old bytes say `pending` and the new are longer -> fill; otherwise -> rerun
  unpointed         matched entries whose note names no evidence pointer: a repo-relative path that exists at the tip
                    or a 7-40 hex commit id that resolves in the lane (a bare note such as `x` does not disclose anything)
  new_rewritten     events on `.ufo/waves/round-58/control(s)/` paths (this round's receipts are never rewritten, disclosed or not)
  new_receipts      files `.ufo/waves/round-58/controls/after-c2-*.txt` and `after-c3-*.txt` present at the tip (the C1
                    receipt is written after this counter's run and is covered by `new_rewritten` at any later tip)

Predicate (frozen in `contract.json`):

    met: undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0 AND unpointed == 0
         AND new_rewritten == 0 AND new_receipts == 2

Exit codes: 0 met, 1 not met, 2 evidence unevaluable (tip unresolved, ledger present but not JSON), 64 usage.
CLI: --root <lane> --revision <tip> [--json] [--list] | --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PREDICATE = ("met: undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0 AND unpointed == 0 "
             "AND new_rewritten == 0 AND new_receipts == 2")
LEDGER = ".ufo/waves/round-58/receipt-rewrites.json"
POP_RE = re.compile(r"^\.ufo/waves/round-[0-9]+/(control|controls)/[^/]+$")
NEW_RE = re.compile(r"^\.ufo/waves/round-58/(control|controls)/")
NEW_RECEIPT_RE = re.compile(r"^\.ufo/waves/round-58/controls/after-c[23]-[^/]+\.txt$")
KINDS = ("relabel", "fill", "rerun", "append", "format", "delete", "readd")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
FIELDS = ("path", "commit", "status", "fromBlob", "toBlob", "kind", "note")


def clean_env() -> dict:
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(root: str, *args: str, check: bool = True) -> str:
    p = subprocess.run(["git", "-C", root, "-c", "core.quotePath=false", *args], capture_output=True, env=clean_env())
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.decode('utf-8', 'replace').strip()}")
    return p.stdout.decode("utf-8", "surrogateescape") if p.returncode == 0 else ""


def blob_id(root: str, rev: str, path: str) -> str | None:
    out = git(root, "ls-tree", "-z", rev, "--", path, check=False)
    for rec in out.split("\0"):
        if rec and "\t" in rec:
            meta, name = rec.split("\t", 1)
            if name == path and meta.split()[1] == "blob":
                return meta.split()[2]
    return None


def events(root: str, tip: str) -> list[dict]:
    """Oldest-first walk of every commit in the tip's ancestry that touches a receipt path."""
    out = git(root, "log", "--reverse", "--no-renames", "--full-history", "--diff-merges=first-parent", "--first-parent",
              "-z", "--name-status", "--format=%x01%H", tip, "--", ".ufo/waves")
    seen: set[str] = set()
    evs: list[dict] = []
    for chunk in out.split("\x01")[1:]:
        parts = chunk.split("\0")
        head = parts[0].strip("\n")
        commit = head.split("\n")[0].strip()
        rest = [p.strip("\n") for p in ([head.split("\n", 1)[1]] if "\n" in head else []) + parts[1:]]
        rest = [p for p in rest if p != ""]
        i = 0
        while i + 1 < len(rest):
            status, path = rest[i][:1], rest[i + 1]
            i += 2
            if not POP_RE.match(path):
                continue
            parent = f"{commit}^"
            if status == "A" and path not in seen:
                seen.add(path)
                continue
            seen.add(path)
            if status not in ("A", "M", "D"):
                status = "M"
            has_parent = git(root, "rev-parse", "--verify", "-q", parent, check=False).strip() != ""
            evs.append({"path": path, "commit": commit, "status": status,
                        "fromBlob": blob_id(root, parent, path) if has_parent else None,
                        "toBlob": blob_id(root, commit, path)})
    return evs


REVLINE_RE = re.compile(r"(?i)revision|\b[0-9a-f]{40}\b")
POINTER_PATH_RE = re.compile(r"(?<![\w/.-])(?:\./)?((?:\.ufo|corpus|scripts|SCORECARD\.md|SKILL\.md|LOG\.md)[\w./-]*)")
POINTER_HASH_RE = re.compile(r"(?<![0-9a-zA-Z])[0-9a-f]{7,40}(?![0-9a-zA-Z])")


def _text(root: str, blob: str | None) -> str:
    if not blob:
        return ""
    p = subprocess.run(["git", "-C", root, "cat-file", "blob", blob], capture_output=True, env=clean_env())
    return p.stdout.decode("utf-8", "surrogateescape")


def classify(status: str, old: str, new: str) -> str:
    if status == "D":
        return "delete"
    if status == "A":
        return "readd"
    if old and new.startswith(old):
        return "append"
    if " ".join(old.split()) == " ".join(new.split()):
        return "format"
    import difflib
    changed = [l[1:] for l in difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0)
               if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    if changed and all(REVLINE_RE.search(l) for l in changed if l.strip()):
        return "relabel"
    if "pending" in old.lower() and len(new) > len(old):
        return "fill"
    return "rerun"


def pointed(root: str, tip: str, note: str) -> bool:
    for m in POINTER_PATH_RE.finditer(note):
        path = m.group(1).rstrip(".,;:)")
        if subprocess.run(["git", "-C", root, "cat-file", "-e", f"{tip}:{path}"], capture_output=True, env=clean_env()).returncode == 0:
            return True
    for m in POINTER_HASH_RE.finditer(note):
        if subprocess.run(["git", "-C", root, "rev-parse", "--verify", "-q", f"{m.group(0)}^{{commit}}"],
                          capture_output=True, env=clean_env()).returncode == 0:
            return True
    return False


def measure(root: str, tip: str) -> dict:
    evs = events(root, tip)
    raw = git(root, "show", f"{tip}:{LEDGER}", check=False)
    ledger_present = raw != ""
    entries: list = []
    if ledger_present:
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"ledger {LEDGER} is not JSON: {exc}")
        entries = doc.get("events") if isinstance(doc, dict) else None
        if not isinstance(entries, list):
            raise ValueError(f"ledger {LEDGER} carries no `events` list")
    malformed, wellformed = [], []
    for n, e in enumerate(entries):
        bad = (not isinstance(e, dict) or any(f not in e for f in FIELDS) or e.get("kind") not in KINDS
               or not isinstance(e.get("note"), str) or not e.get("note", "").strip()
               or not isinstance(e.get("commit"), str) or not HEX40.match(e.get("commit", ""))
               or e.get("status") not in ("A", "M", "D")
               or any(e.get(k) is not None and not (isinstance(e.get(k), str) and HEX40.match(e[k])) for k in ("fromBlob", "toBlob"))
               or (e.get("status") == "M" and (e.get("fromBlob") is None or e.get("toBlob") is None))
               or (e.get("status") == "D" and (e.get("fromBlob") is None or e.get("toBlob") is not None))
               or (e.get("status") == "A" and (e.get("fromBlob") is not None or e.get("toBlob") is None)))
        (malformed if bad else wellformed).append(n if bad else e)
    key = lambda e: (e["path"], e["commit"], e["status"], e["fromBlob"], e["toBlob"])
    ev_keys = {key(e) for e in evs}
    used: set = set()
    phantom, wrong_kind, unpointed = [], [], []
    for e in wellformed:
        k = key(e)
        if k in ev_keys and k not in used:
            used.add(k)
            if e["kind"] != classify(e["status"], _text(root, e["fromBlob"]), _text(root, e["toBlob"])):
                wrong_kind.append(e)
            if not pointed(root, tip, e["note"]):
                unpointed.append(e)
        else:
            phantom.append(e)
    undisclosed = [e for e in evs if key(e) not in used]
    tree = git(root, "ls-tree", "-r", "-z", "--name-only", tip, "--", ".ufo/waves/round-58/controls").split("\0")
    new_receipts = sorted(p for p in tree if NEW_RECEIPT_RE.match(p))
    new_rewritten = [e for e in evs if NEW_RE.match(e["path"])]
    v = {"events": len(evs), "undisclosed": len(undisclosed), "phantom": len(phantom), "malformed": len(malformed),
         "wrong_kind": len(wrong_kind), "unpointed": len(unpointed), "new_rewritten": len(new_rewritten), "new_receipts": len(new_receipts), "ledger_present": ledger_present,
         "ledger_entries": len(entries),
         "_undisclosed": undisclosed, "_phantom": phantom, "_wrong_kind": wrong_kind, "_unpointed": unpointed, "_malformed": malformed, "_new_rewritten": new_rewritten,
         "_new_receipts": new_receipts}
    v["met"] = (v["undisclosed"] == 0 and v["phantom"] == 0 and v["malformed"] == 0 and v["wrong_kind"] == 0
                and v["unpointed"] == 0 and v["new_rewritten"] == 0 and v["new_receipts"] == 2)
    return v


KEYS = ("events", "undisclosed", "phantom", "malformed", "wrong_kind", "unpointed", "new_rewritten", "new_receipts")


def report(v: dict, tip: str, listing: bool) -> str:
    lines = ["C1 receipt-rewrites " + " ".join(f"{k}={v[k]}" for k in KEYS) + f" met={v['met']}  ({PREDICATE})"]
    for label, k in (("UNDISCLOSED", "_undisclosed"), ("PHANTOM", "_phantom"), ("WRONG-KIND", "_wrong_kind"), ("UNPOINTED", "_unpointed"), ("NEW-REWRITTEN", "_new_rewritten")):
        for e in v[k]:
            lines.append(f"  {label} {e['status']} {e['path']} at {e['commit'][:12]} {(e['fromBlob'] or '-')[:12]} -> {(e['toBlob'] or '-')[:12]}")
    for n in v["_malformed"]:
        lines.append(f"  MALFORMED ledger entry #{n}")
    if listing:
        lines.append(f"  new receipts: {', '.join(v['_new_receipts']) or '-'}")
    lines.append(f"  ledger: {LEDGER} {'present' if v['ledger_present'] else 'absent'} ({v['ledger_entries']} entries)")
    lines.append(f"  revision: {tip}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- selftest (version 1, minimal; wave 1 hardens it)

_ID = ["-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false"]


def _commit(d: str, files: dict, deletes: tuple = (), msg: str = "c") -> str:
    for rel, text in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(text, bytes):
            with open(p, "wb") as fh:
                fh.write(text)
        else:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)
    for rel in deletes:
        os.remove(os.path.join(d, rel))
    subprocess.run(["git", "-C", d, "add", "-A"], check=True, env=clean_env())
    subprocess.run(["git", "-C", d, *_ID, "commit", "-q", "--allow-empty", "-m", msg], check=True, env=clean_env())
    return git(d, "rev-parse", "HEAD").strip()


def _link(d: str, rel: str, target: str) -> None:
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.lexists(p):
        os.remove(p)
    os.symlink(target, p)


def _repo(scratch: str) -> str:
    d = tempfile.mkdtemp(prefix="c58-rr-", dir=scratch)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=clean_env())
    if os.path.realpath(git(d, "rev-parse", "--show-toplevel").strip()) != os.path.realpath(d):
        raise RuntimeError("fixture repo toplevel mismatch")
    _commit(d, {".ufo/evidence.md": "fixture evidence\n"})
    return d


def _ledger(entries: list) -> dict:
    return {LEDGER: json.dumps({"events": entries}, indent=1)}


def _entry(d: str, path: str, commit: str, status: str, kind: str = "fill", **over) -> dict:
    e = {"path": path, "commit": commit, "status": status, "fromBlob": blob_id(d, f"{commit}^", path),
         "toBlob": blob_id(d, commit, path), "kind": kind, "note": "see .ufo/evidence.md"}
    e.update(over)
    return e


def selftest() -> int:
    scratch = os.environ.get("TMPDIR") or tempfile.gettempdir()
    checks: list[tuple[str, bool]] = []
    R = ".ufo/waves/round-57/controls/after-c1-x.txt"
    N2, N3 = ".ufo/waves/round-58/controls/after-c2-a.txt", ".ufo/waves/round-58/controls/after-c3-b.txt"
    made: list[str] = []
    try:
        # 1 undisclosed fill is counted
        d = _repo(scratch); made.append(d)
        _commit(d, {R: "pending\n"}); c = _commit(d, {R: "met=True\n"})
        _commit(d, {N2: "ok\n", N3: "ok\n"})
        v = measure(d, "HEAD")
        checks.append(("undisclosed fill counted", v["undisclosed"] == 1 and v["events"] == 1 and not v["met"]))
        # 2 disclosed with true blobs -> met
        _commit(d, _ledger([_entry(d, R, c, "M")]))
        v = measure(d, "HEAD")
        checks.append(("true disclosure meets", v["met"] and v["undisclosed"] == 0 and v["phantom"] == 0))
        # 3 wrong blob in ledger -> phantom + undisclosed
        _commit(d, _ledger([_entry(d, R, c, "M", toBlob="0" * 40)]))
        v = measure(d, "HEAD")
        checks.append(("wrong blob is phantom", v["phantom"] == 1 and v["undisclosed"] == 1 and not v["met"]))
        # 4 invented entry -> phantom
        _commit(d, _ledger([_entry(d, R, c, "M"), {**_entry(d, R, c, "M"), "commit": "1" * 40}]))
        v = measure(d, "HEAD")
        checks.append(("invented entry is phantom", v["phantom"] == 1 and not v["met"]))
        # 5 duplicate entry -> phantom
        _commit(d, _ledger([_entry(d, R, c, "M"), _entry(d, R, c, "M")]))
        v = measure(d, "HEAD")
        checks.append(("duplicate entry is phantom", v["phantom"] == 1 and not v["met"]))
        # 6 unknown kind / empty note -> malformed
        _commit(d, _ledger([_entry(d, R, c, "M", kind="rerun")]))
        v = measure(d, "HEAD")
        checks.append(("false kind (rerun for a pending fill) counted", v["wrong_kind"] == 1 and not v["met"]))
        _commit(d, _ledger([_entry(d, R, c, "M", note="x")]))
        v = measure(d, "HEAD")
        checks.append(("pointer-free note counted", v["unpointed"] == 1 and not v["met"]))
        _commit(d, _ledger([_entry(d, R, c, "M", note="see corpus/absent.md")]))
        v = measure(d, "HEAD")
        checks.append(("note naming an absent path counted", v["unpointed"] == 1 and not v["met"]))
        _commit(d, _ledger([_entry(d, R, c, "M", note=f"fill landed in {c[:12]}")]))
        v = measure(d, "HEAD")
        checks.append(("note naming a resolvable commit meets", v["met"]))
        checks.append(("classify relabel/append/format", classify("M", "revision: " + "a" * 40 + "\nmet\n", "revision: " + "b" * 40 + "\nmet\n") == "relabel"
                       and classify("M", "a\n", "a\nb\n") == "append" and classify("M", "a  b\n", "a b\n") == "format"
                       and classify("M", "met=False\n", "met=True\n") == "rerun"))
        _commit(d, _ledger([_entry(d, R, c, "M", kind="oops")]))
        v = measure(d, "HEAD")
        checks.append(("unknown kind malformed", v["malformed"] == 1 and not v["met"]))
        _commit(d, _ledger([_entry(d, R, c, "M", note=" ")]))
        v = measure(d, "HEAD")
        checks.append(("empty note malformed", v["malformed"] == 1 and not v["met"]))
        # 7 round-58 receipt rewrite is never acceptable, even disclosed
        c2 = _commit(d, {N2: "ok again\n"})
        _commit(d, _ledger([_entry(d, R, c, "M"), _entry(d, N2, c2, "M", kind="rerun")]))
        v = measure(d, "HEAD")
        checks.append(("round-58 rewrite fails even disclosed", v["new_rewritten"] == 1 and v["undisclosed"] == 0 and not v["met"]))
        # 8 deletion and rename are events
        d = _repo(scratch); made.append(d)
        Q = ".ufo/waves/round-40/control/base.txt"
        _commit(d, {Q: "a\n", N2: "ok\n", N3: "ok\n"})
        c = _commit(d, {Q.replace("base", "base2"): "a\n"}, deletes=(Q,))
        v = measure(d, "HEAD")
        checks.append(("rename is a deletion event", v["events"] == 1 and v["_undisclosed"][0]["status"] == "D"))
        c3 = _commit(d, {Q: "b\n"})
        v = measure(d, "HEAD")
        checks.append(("re-add after delete is an event", v["events"] == 2))
        _commit(d, _ledger([_entry(d, Q, c, "D", kind="delete"), _entry(d, Q, c3, "A", kind="readd")]))
        v = measure(d, "HEAD")
        checks.append(("delete and readd disclosed meets", v["met"]))
        # 9 missing new receipt -> not met; non-receipt path ignored
        d = _repo(scratch); made.append(d)
        _commit(d, {N2: "ok\n", ".ufo/waves/round-57/w1/x.md": "a\n"})
        _commit(d, {".ufo/waves/round-57/w1/x.md": "b\n"})
        v = measure(d, "HEAD")
        checks.append(("missing C3 receipt not met; non-receipt ignored", v["new_receipts"] == 1 and v["events"] == 0 and not v["met"]))
        # 10 non-JSON ledger is unevaluable
        _commit(d, {LEDGER: "{not json"})
        try:
            measure(d, "HEAD"); checks.append(("non-JSON ledger unevaluable", False))
        except ValueError:
            checks.append(("non-JSON ledger unevaluable", True))
        # ---- wave-1 hardening: merge shape, quoted paths, binary, revert, null blob, subdirectory, symlink, pointers
        # 11 a merge that brings a branch receipt change in: one event, at the merge, against the first parent
        d = _repo(scratch); made.append(d)
        trunk = git(d, "symbolic-ref", "--short", "HEAD").strip()
        _commit(d, {R: "pending\n", N2: "ok\n", N3: "ok\n"})
        git(d, "checkout", "-q", "-b", "feat")
        branch_c = _commit(d, {R: "met=True\n"})
        git(d, "checkout", "-q", trunk)
        _commit(d, {"other.txt": "x\n"})
        subprocess.run(["git", "-C", d, *_ID, "merge", "-q", "--no-ff", "-m", "merge feat", "feat"],
                       check=True, env=clean_env(), capture_output=True)
        merge_c = git(d, "rev-parse", "HEAD").strip()
        v = measure(d, "HEAD"); ev = v["_undisclosed"]
        checks.append(("merge sees the branch receipt change once, at the merge, against the first parent",
                       v["events"] == 1 and len(ev) == 1 and ev[0]["commit"] == merge_c and branch_c != merge_c
                       and ev[0]["status"] == "M" and ev[0]["fromBlob"] == blob_id(d, f"{merge_c}^", R)
                       and ev[0]["fromBlob"] != ev[0]["toBlob"]))
        _commit(d, _ledger([_entry(d, R, merge_c, "M")]))
        checks.append(("merge change disclosed by the merge commit meets", measure(d, "HEAD")["met"]))
        # 12 a merge whose tree equals the first parent hides no event, though the second parent differs
        d = _repo(scratch); made.append(d)
        trunk = git(d, "symbolic-ref", "--short", "HEAD").strip()
        _commit(d, {R: "pending\n", N2: "ok\n", N3: "ok\n"})
        git(d, "checkout", "-q", "-b", "feat")
        _commit(d, {R: "branch\n"})
        git(d, "checkout", "-q", trunk)
        _commit(d, {"other.txt": "x\n"})
        subprocess.run(["git", "-C", d, *_ID, "merge", "-q", "-s", "ours", "-m", "merge feat", "feat"],
                       check=True, env=clean_env(), capture_output=True)
        v = measure(d, "HEAD")
        checks.append(("merge that discards the branch change is not an event", v["events"] == 0 and v["met"]))
        # 13 both parents change the receipt, the resolution is a third value: one event per commit, no double count
        d = _repo(scratch); made.append(d)
        trunk = git(d, "symbolic-ref", "--short", "HEAD").strip()
        _commit(d, {R: "a\n", N2: "ok\n", N3: "ok\n"})
        git(d, "checkout", "-q", "-b", "feat")
        _commit(d, {R: "b\n"})
        git(d, "checkout", "-q", trunk)
        main_c = _commit(d, {R: "c\n"})
        subprocess.run(["git", "-C", d, *_ID, "merge", "-q", "feat"], env=clean_env(), capture_output=True)
        merge_c = _commit(d, {R: "d\n"}, msg="merge")
        v = measure(d, "HEAD"); ev = v["_undisclosed"]
        checks.append(("conflicting merge counted once, against the first parent",
                       v["events"] == 2 and len(ev) == 2 and ev[-1]["commit"] == merge_c
                       and ev[-1]["fromBlob"] == blob_id(d, f"{merge_c}^", R)
                       and len({(e["commit"], e["fromBlob"], e["toBlob"]) for e in ev}) == 2))
        _commit(d, _ledger([_entry(d, R, main_c, "M", kind="rerun"), _entry(d, R, merge_c, "M", kind="rerun")]))
        checks.append(("both sides of a conflicting merge disclosed meet", measure(d, "HEAD")["met"]))
        # 14 a receipt path with a space and one with non-ASCII characters
        d = _repo(scratch); made.append(d)
        SP, U = ".ufo/waves/round-50/controls/after c1 spaced.txt", ".ufo/waves/round-50/controls/after-c1-\u30ec\u30b7\u30fc\u30c8.txt"
        _commit(d, {SP: "pending\n", U: "pending\n", N2: "ok\n", N3: "ok\n"})
        c = _commit(d, {SP: "met=True\n", U: "met=True\n"})
        v = measure(d, "HEAD")
        checks.append(("paths with a space and non-ASCII characters are events",
                       v["events"] == 2 and sorted(e["path"] for e in v["_undisclosed"]) == sorted([SP, U])))
        _commit(d, _ledger([_entry(d, SP, c, "M"), _entry(d, U, c, "M")]))
        checks.append(("space and non-ASCII receipts disclosed meet", measure(d, "HEAD")["met"]))
        # 15 a binary receipt rewrite: distinct bytes stay distinct and classify rerun
        d = _repo(scratch); made.append(d)
        B = ".ufo/waves/round-51/controls/after-c1-bin.txt"
        _commit(d, {B: b"\x00\xff\x01binary\n", N2: "ok\n", N3: "ok\n"})
        c = _commit(d, {B: b"\x00\xfe\x01binary\n"})
        old, new = _text(d, blob_id(d, f"{c}^", B)), _text(d, blob_id(d, c, B))
        checks.append(("binary byte change stays distinguishable and classifies rerun",
                       old != new and blob_id(d, f"{c}^", B) != blob_id(d, c, B) and classify("M", old, new) == "rerun"))
        _commit(d, _ledger([_entry(d, B, c, "M", kind="append")]))
        v = measure(d, "HEAD")
        checks.append(("binary byte change called append is a wrong kind", v["wrong_kind"] == 1 and not v["met"]))
        _commit(d, _ledger([_entry(d, B, c, "M", kind="rerun")]))
        checks.append(("binary byte change disclosed as rerun meets", measure(d, "HEAD")["met"]))
        # 16 a receipt changed and reverted is two events
        d = _repo(scratch); made.append(d)
        Z = ".ufo/waves/round-52/controls/after-c1-z.txt"
        _commit(d, {Z: "pending\n", N2: "ok\n", N3: "ok\n"})
        c1 = _commit(d, {Z: "met=True\n"})
        c2 = _commit(d, {Z: "pending\n"})
        v = measure(d, "HEAD")
        checks.append(("change and revert are two events", v["events"] == 2 and [e["commit"] for e in v["_undisclosed"]] == [c1, c2]))
        _commit(d, _ledger([_entry(d, Z, c1, "M")]))
        v = measure(d, "HEAD")
        checks.append(("a revert disclosed only once leaves one undisclosed", v["undisclosed"] == 1 and not v["met"]))
        _commit(d, _ledger([_entry(d, Z, c1, "M"), _entry(d, Z, c2, "M", kind="rerun")]))
        checks.append(("change and revert disclosed meet", measure(d, "HEAD")["met"]))
        # 17 a modification entry with a null fromBlob is structurally impossible
        d = _repo(scratch); made.append(d)
        _commit(d, {R: "pending\n", N2: "ok\n", N3: "ok\n"})
        c = _commit(d, {R: "met=True\n"})
        _commit(d, _ledger([_entry(d, R, c, "M", fromBlob=None)]))
        v = measure(d, "HEAD")
        checks.append(("modification with a null fromBlob is malformed, not phantom",
                       v["malformed"] == 1 and v["phantom"] == 0 and not v["met"]))
        # 18 a file below controls/ (a subdirectory) is outside the population by design
        d = _repo(scratch); made.append(d)
        _commit(d, {N2: "ok\n", N3: "ok\n"})
        _commit(d, {".ufo/waves/round-58/controls/sub/nested.txt": "a\n"})
        _commit(d, {".ufo/waves/round-58/controls/sub/nested.txt": "b\n"})
        v = measure(d, "HEAD")
        checks.append(("a controls/ subdirectory file is outside the population",
                       v["events"] == 0 and v["new_rewritten"] == 0 and v["new_receipts"] == 2 and v["met"]))
        # 19 a symlink receipt: the rewrite is an event carrying the link blob
        d = _repo(scratch); made.append(d)
        S = ".ufo/waves/round-53/controls/after-c1-link.txt"
        _commit(d, {N2: "ok\n", N3: "ok\n"})
        _link(d, S, ".ufo/evidence.md")
        _commit(d, {})
        _link(d, S, "LOG.md")
        c2 = _commit(d, {})
        v = measure(d, "HEAD"); ev = v["_undisclosed"]
        checks.append(("a symlink receipt rewrite is an event with the link blob",
                       v["events"] == 1 and len(ev) == 1 and ev[0]["commit"] == c2 and ev[0]["status"] == "M"
                       and ev[0]["toBlob"] == blob_id(d, c2, S) and _text(d, ev[0]["fromBlob"]) == ".ufo/evidence.md"))
        _commit(d, _ledger([_entry(d, S, c2, "M", kind="rerun")]))
        checks.append(("symlink receipt disclosed meets", measure(d, "HEAD")["met"]))
        # 20 evidence pointers: backticks, markdown punctuation and a ./ prefix resolve; in-word text does not
        d = _repo(scratch); made.append(d)
        _commit(d, {"corpus/README.md": "frontier\n"})
        pointing = ["see `.ufo/evidence.md`", "see .ufo/evidence.md.", "see (.ufo/evidence.md)",
                    "see .ufo/evidence.md,", "see .ufo/evidence.md; then", "see **.ufo/evidence.md**",
                    "see [evidence](corpus/README.md)", "see ./corpus/README.md"]
        checks.append(("pointers in backticks, before punctuation or with ./ resolve",
                       all(pointed(d, "HEAD", n) for n in pointing)))
        checks.append(("in-word, absent and bare pointers do not resolve",
                       not pointed(d, "HEAD", "xyz.ufo/evidence.md") and not pointed(d, "HEAD", "see corpus/absent.md")
                       and not pointed(d, "HEAD", "x")))
    finally:
        for d in made:
            shutil.rmtree(d, ignore_errors=True)
    for name, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'} {name}")
    passed = sum(ok for _, ok in checks)
    print(f"c58 receipt-rewrites selftest: {passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


def main() -> int:
    class _P(argparse.ArgumentParser):
        def error(self, message):
            print(f"usage error: {message}", file=sys.stderr)
            raise SystemExit(64)

    ap = _P(description="Round-58 C1 counter (receipt rewrites disclosed)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.revision:
        print("usage: --revision is required unless --selftest is used", file=sys.stderr)
        return 64
    tip = git(a.root, "rev-parse", "--verify", "-q", f"{a.revision}^{{commit}}", check=False).strip()
    if not tip:
        print(f"unevaluable: revision {a.revision!r} does not resolve in {a.root!r}\nEXIT=2")
        return 2
    try:
        v = measure(a.root, tip)
    except (ValueError, RuntimeError) as exc:
        print(f"unevaluable: {exc}\n  revision: {tip}\nEXIT=2")
        return 2
    code = 0 if v["met"] else 1
    if a.json:
        print(json.dumps({"schema": "kake-r58-c1-receipt-rewrites-v1", "predicate": PREDICATE, "revision": tip,
                          **{k: v[k] for k in KEYS}, "met": v["met"], "undisclosedEvents": v["_undisclosed"],
                          "phantomEntries": v["_phantom"], "exit": code}, indent=1))
        return code
    print(report(v, tip, a.list))
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
