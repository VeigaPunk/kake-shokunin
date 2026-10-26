#!/usr/bin/env python3
"""Round-57 C1 counter — calibration: stated revision pins against the revision pins the receipts carry.

Version 1 was frozen at `b9a5d012f7fd`; version 2 (wave 1) read receipt bodies and anchored the pin; version 2.1 (after wave 2, before any claim was
measured; attacks `w2/ReviewerPinsV2.md`, `w2/CritCheatC1V2.md`, `w2/MutC1PinsV2.md`, `w2/CriticAxisWave2.md`, `w2/SentinelRound.md`) compares every commit with
its own parent (a merge resolution, a branched receipt and a rename out of the population and back are seen), counts a lost base receipt by name,
accepts a failed run as an honest body so C1 does not depend on C2 or C3 succeeding, pins the counters and the tool at a freeze commit, removes the
environment override, scrubs `GIT_*` variables and exits 2 on any crash. The predicate is unchanged.

Surface: the measurement receipts under `.ufo/waves/round-5[2-7]/{control,controls}/` that carry a `revision:`/`revision=` line (the revision a counter
was run against; the one JSON ladder that embeds old counters' printed tails is excluded), and the lane's statement "Measured revision: <rev>". A
report or SCORECARD says what was measured; the receipt says what the counter was actually run over. A later commit that rewrites the receipt's revision
line (a *relabel*) makes the stated pin and the run diverge (round-56 routed defect 1, `corpus/lessons/round-56-verifier-spotcheck.md` §6.1). History cannot be
rewritten, so a historical relabel is closed by disclosure: `receipt-errata.json` names it with the true values and the counter checks every entry against
git. A relabel of a receipt this round introduces is never disclosable: it must not occur.

Definitions (derived from `git` over the whole ancestry of the tip, topological order, renames followed without a size limit; never the working tree):
  receipt      a path in the population whose committed versions carry a 40-hex revision line (`"revision":` JSON form accepted).
  relabel      at a commit, a receipt's pin set differs from its first parent's (a merge counts only when its resolution is a value neither parent
               held; a re-added or moved-back path is compared with its last known pins) and both are non-empty, or the new one is empty; recorded as (path,
               from, to, commit) with the full 40-hex values.
  disclosed    an entry of `.ufo/waves/round-57/receipt-errata.json` equal to a relabel on all four fields (no duplicates).
  measured     `.ufo/waves/round-57/measured.json`: `revision` X, a 40-hex commit strictly after the commit that added this counter, and `countersFrozenAt` F, a
               40-hex commit with counter-intro <= F <= X such that this counter, the gate, the quote counter and `scripts/id_resolver.py` are byte-identical
               at the tip and at F. X is a strict ancestor of the commit that introduced each new receipt.
  new receipt  `.ufo/waves/round-57/controls/after-c<N>-*.txt`, N in 1, 2, 3; one file per N. Any other `after-*` file there is malformed; any other
               round-57 receipt must carry only 40-hex pins that are commits and strict ancestors of the commit that introduced it (`rerun-*` and `base-*`
               files are such receipts). Each new receipt carries exactly one `revision:` line equal to X.
  body         after-c2 and after-c3 start with their counter's report line (any outcome: a recorded failed run is calibrated) with the frozen predicate sentence
               and an `EXIT=` line consistent with `met=`. after-c1 carries `tip: <T0>` and starts with the line this counter prints for T0 with
               `--no-bodies` (a commit that holds all three receipts, descends from X, and is a strict ancestor of the commit that last wrote the body).

Counted values:
  undisclosed_relabels  relabels in receipts outside round 57 with no matching errata entry.
  phantom_errata        errata entries that match no relabel.
  deleted_receipts      base receipts (the 44 population paths at the base revision) absent at the tip, plus pinned receipts deleted and not re-added.
  new_relabelled        relabels of any round-57 file (merged branches included).
  new_unpinned          malformed, duplicated, unpinned or body-less new receipts; an unpinned or future-pinned round-57 receipt; a measured revision or counter
                        freeze that fails the rules above; a base revision (`28fa0b23…`) that is not an ancestor of the tip.
  new_receipts          valid new receipts among claims 1, 2, 3.
  scorecard_pin         1 when every `Measured revision:` line of the SCORECARD `## Round 57` sections (fenced blocks ignored) names X, and one exists.

Predicate (frozen in `contract.json`):

    met: undisclosed_relabels == 0 AND phantom_errata == 0 AND deleted_receipts == 0 AND new_relabelled == 0 AND new_unpinned == 0 AND new_receipts == 3 AND scorecard_pin == 1

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable (or any crash), 64 usage.
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

PREDICATE = ("met: undisclosed_relabels == 0 AND phantom_errata == 0 AND deleted_receipts == 0 AND new_relabelled == 0 "
             "AND new_unpinned == 0 AND new_receipts == 3 AND scorecard_pin == 1")
BASE_REV = "28fa0b23e699303725aba2727094531f5e44494d"
WAVE = ".ufo/waves/round-57"
COUNTER = f"{WAVE}/c57_receipt_pins.py"
FROZEN_FILES = (COUNTER, f"{WAVE}/c57_idresolver_gate.py", f"{WAVE}/c57_quote_truth.py", "scripts/id_resolver.py")
ERRATA = f"{WAVE}/receipt-errata.json"
MEASURED = f"{WAVE}/measured.json"
NEW_RE = re.compile(r"^\.ufo/waves/round-57/controls/after-c([123])-[^/]+\.txt$")
POP_RE = re.compile(r"^\.ufo/waves/round-5[2-7]/(control|controls)/[^/]+\.(txt|json)$")
EXCLUDE_RE = re.compile(r"-mutation-ladder\.json$")
REV_RE = re.compile(r'(?m)^[ \t]*"?revision"?[ \t]*[:=][ \t]*"?([0-9a-f]{40})\b')
HEX40 = re.compile(r"[0-9a-f]{40}")
BODY_FIRST = {
    "2": re.compile(r"^C2 id-resolver ([0-5])/5 met=(True|False)  \(met: gate_conditions_passed == 5 of 5\)$"),
    "3": re.compile(r"^C3 quote-truth ([0-8])/8 met=(True|False)  \(met: conditions_passed == 8 of 8\)$"),
}
FULL = {"2": 5, "3": 8}
SCRUB = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_NAMESPACE",
         "GIT_CEILING_DIRECTORIES", "GIT_DISCOVERY_ACROSS_FILESYSTEM", "GIT_PREFIX")


class Unevaluable(Exception):
    pass


def clean_env() -> dict:
    return {k: v for k, v in os.environ.items() if k not in SCRUB}


def _run(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", root, "-c", "core.quotePath=false", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=clean_env())


def git(root: str, *args: str) -> str:
    p = _run(root, *args)
    if p.returncode != 0:
        raise Unevaluable(f"git {' '.join(args)}: {p.stderr.decode('utf-8', 'replace').strip()}")
    return p.stdout.decode("utf-8", "replace")


def blob(root: str, rev: str, path: str) -> str | None:
    p = _run(root, "show", f"{rev}:{path}")
    return p.stdout.decode("utf-8", "replace") if p.returncode == 0 else None


def blob_bytes(root: str, rev: str, path: str) -> bytes | None:
    p = _run(root, "show", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None


def is_commit(root: str, rev: str) -> bool:
    return bool(HEX40.fullmatch(rev)) and _run(root, "cat-file", "-e", f"{rev}^{{commit}}").returncode == 0


def is_ancestor(root: str, anc: str, desc: str) -> bool:
    return _run(root, "merge-base", "--is-ancestor", anc, desc).returncode == 0


def in_pop(path: str) -> bool:
    return bool(POP_RE.match(path)) and not EXCLUDE_RE.search(path)


def load_json(text: str | None, what: str):
    if text is None:
        return None
    try:
        return json.loads(text)
    except ValueError as exc:
        raise Unevaluable(f"{what} is not JSON: {exc}")


def pins(text: str | None) -> set[str] | None:
    return None if text is None else set(REV_RE.findall(text))


def walk_history(root: str, tip: str):
    """Yield (commit, parents, records) oldest first over the whole ancestry. A merge's records are its diff against its first parent."""
    log = git(root, "log", "--topo-order", "--reverse", "--diff-merges=first-parent", "--name-status", "-M", "-l0", "--format=@@%H %P", tip)
    commit, parents, recs = None, [], []
    for line in log.split("\n"):
        if line.startswith("@@"):
            if commit is not None:
                yield commit, parents, recs
            fields = line[2:].split()
            commit, parents, recs = fields[0], fields[1:], []
        elif "\t" in line:
            parts = line.split("\t")
            recs.append((parts[0][0], *parts[1:]))
    if commit is not None:
        yield commit, parents, recs


def scan(root: str, tip: str):
    """Relabels, the population at the tip and the receipts that vanished."""
    present = {p for p in git(root, "ls-tree", "-r", "--name-only", tip).split("\n") if in_pop(p)}
    last: dict[str, set[str]] = {}  # last non-empty pin set ever seen per path: compares a re-added or moved-back path
    deleted: set[str] = set()
    relabels: list[tuple[str, str, str, str]] = []

    def record(path: str, prev: set[str] | None, cur: set[str], commit: str) -> None:
        if prev and cur != prev:
            for a in sorted(prev):
                for b in sorted(cur) or [""]:
                    if a != b:
                        relabels.append((path, a, b, commit))

    for commit, parents, recs in walk_history(root, tip):
        first = parents[0] if parents else None
        for rec in recs:
            status = rec[0]
            if status == "R":
                old, new = rec[1], rec[2]
                prev = pins(blob(root, first, old)) if first else None
                if prev:
                    last[old] = prev
                if in_pop(old) and not in_pop(new):
                    if prev:
                        deleted.add(old)
                    continue
                if not in_pop(new):
                    continue
                cur = pins(blob(root, commit, new)) or set()
                record(new, prev or last.get(new), cur, commit)
                if cur:
                    last[new] = cur
                deleted.discard(new)
                continue
            path = rec[1]
            if not in_pop(path):
                continue
            if status == "D":
                prev = pins(blob(root, first, path)) if first else None
                if prev:
                    last[path] = prev
                    deleted.add(path)
                continue
            cur = pins(blob(root, commit, path))
            if cur is None:
                continue
            prev = pins(blob(root, first, path)) if first else None
            if not prev:
                prev = last.get(path)  # a new life of a known path, or a pin that was stripped: compare with its last known pins
            if len(parents) > 1:  # a merge counts only when its resolution is a value no parent held
                held = [pins(blob(root, p, path)) for p in parents]
                if any(h == cur for h in held if h is not None):
                    prev = cur
            record(path, prev, cur, commit)
            if cur:
                last[path] = cur
            deleted.discard(path)
    gone = {p for p in deleted if p not in present}
    return present, relabels, gone


def last_commit(root: str, tip: str, path: str) -> str:
    return git(root, "log", "-1", "--format=%H", tip, "--", path).strip()


def first_add(root: str, tip: str, path: str) -> str:
    lines = [x for x in git(root, "log", "--topo-order", "--diff-filter=A", "--format=%H", tip, "--", path).strip().split("\n") if x]
    return lines[0] if lines else ""  # newest add: a deleted and re-added receipt counts from its current life


def oldest_add(root: str, tip: str, path: str) -> str:
    lines = [x for x in git(root, "log", "--topo-order", "--diff-filter=A", "--format=%H", tip, "--", path).strip().split("\n") if x]
    return lines[-1] if lines else ""


def parse_errata(root: str, tip: str) -> list[tuple[str, str, str, str]]:
    text = blob(root, tip, ERRATA)
    if text is None:
        return []
    data = load_json(text, ERRATA)
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise Unevaluable(f"{ERRATA}: not an object with an `entries` list")
    out = []
    for e in entries:
        if not (isinstance(e, dict) and all(isinstance(e.get(k), str) for k in ("path", "from", "to", "commit"))):
            raise Unevaluable(f"{ERRATA}: entry is not an object of four strings: {e!r}")
        out.append((e["path"], e["from"], e["to"], e["commit"]))
    if len(set(out)) != len(out):
        raise Unevaluable(f"{ERRATA}: duplicate entries")
    return out


def scorecard_section(sc: str) -> str:
    """Text of the `## Round 57` sections with fenced blocks removed (a quoted example is not a statement)."""
    lines, out, fenced, inside = sc.split("\n"), [], False, False
    for ln in lines:
        if re.match(r"^ {0,3}(```|~~~)", ln):
            fenced = not fenced
            continue
        if fenced:
            continue
        if re.match(r"^## ", ln):
            inside = bool(re.match(r"^## Round 57\b", ln))
        if inside:
            out.append(ln)
    return "\n".join(out)


LABEL_RE = re.compile(r"(?mi)^[ \t]*(?:[-*][ \t]+)?\*{0,2}Measured revision:?\*{0,2}[ \t]*:?[ \t]*(.*?)[ \t]*$")


def body_shape(num: str, first: str, body: list[str]) -> str:
    m = BODY_FIRST[num].match(first)
    if not m:
        return f"first line is not claim {num}'s report line: {first[:90]!r}"
    exits = [ln for ln in body if re.fullmatch(r"EXIT=\d+", ln.strip())]
    if len(exits) != 1:
        return f"expected exactly one EXIT= line, found {len(exits)}"
    passed, met_text = int(m.group(1)), m.group(2) == "True"
    if met_text != (passed == FULL[num]) or exits[0].strip() != ("EXIT=0" if met_text else "EXIT=1"):
        return f"report line and EXIT= disagree: {first[:60]!r} / {exits[0]!r}"
    return ""


def measure(root: str, tip: str, check_bodies: bool = True) -> dict:
    tip = git(root, "rev-parse", "--verify", f"{tip}^{{commit}}").strip()
    present, relabels, gone = scan(root, tip)
    old = [r for r in relabels if not r[0].startswith(f"{WAVE}/")]
    new_rel = [r for r in relabels if r[0].startswith(f"{WAVE}/")]
    entries = parse_errata(root, tip)
    undisclosed = sorted(set(old) - set(entries))
    phantom = sorted(set(entries) - set(old))
    notes: list[str] = []
    new_unpinned = 0
    base_ok = is_commit(root, BASE_REV) and is_ancestor(root, BASE_REV, tip)
    lost: set[str] = set()
    if base_ok:
        base_present = {p for p in git(root, "ls-tree", "-r", "--name-only", BASE_REV).split("\n") if in_pop(p)}
        lost = base_present - present
    else:
        new_unpinned += 1
        notes.append(f"base revision {BASE_REV[:12]} is not an ancestor of the tip (history replaced)")
    deleted_receipts = len(lost | {p for p in gone if p not in lost})
    mdata = load_json(blob(root, tip, MEASURED), MEASURED)
    measured_rev = None
    if mdata is not None:
        if not isinstance(mdata, dict) or not isinstance(mdata.get("revision"), str) or not isinstance(mdata.get("countersFrozenAt"), str):
            raise Unevaluable(f"{MEASURED}: not an object with string `revision` and `countersFrozenAt`")
        x, f = mdata["revision"], mdata["countersFrozenAt"]
        counter_intro = oldest_add(root, tip, COUNTER)
        problems = []
        if not (is_commit(root, x) and is_ancestor(root, x, tip)):
            problems.append("revision is not a 40-hex commit in the tip's ancestry")
        if not counter_intro or x == counter_intro or not is_ancestor(root, counter_intro, x):
            problems.append("revision is not strictly after the commit that added the counter")
        if not (is_commit(root, f) and counter_intro and is_ancestor(root, counter_intro, f) and is_ancestor(root, f, x)):
            problems.append("countersFrozenAt is not a commit between the counter's introduction and the measured revision")
        else:
            for p in FROZEN_FILES:
                a, b = blob_bytes(root, tip, p), blob_bytes(root, f, p)
                if a is None or a != b:
                    problems.append(f"{p} differs between the tip and countersFrozenAt")
        if problems:
            new_unpinned += len(problems)
            notes.extend(f"{MEASURED}: {p}" for p in problems)
        else:
            measured_rev = x
    new_paths = sorted(p for p in present if p.startswith(f"{WAVE}/") and os.path.basename(p).startswith("after-"))
    by_num: dict[str, list[str]] = {}
    for p in new_paths:
        m = NEW_RE.match(p)
        if not m:
            new_unpinned += 1
            notes.append(f"{p}: malformed `after-*` receipt name (expected after-c1|c2|c3-*.txt)")
        else:
            by_num.setdefault(m.group(1), []).append(p)
    for p in sorted(q for q in present if q.startswith(f"{WAVE}/") and not NEW_RE.match(q) and not os.path.basename(q).startswith("after-")):
        text = blob(root, tip, p) or ""
        found = REV_RE.findall(text)
        if found:
            intro = first_add(root, tip, p)
            for r in found:
                if not (is_commit(root, r) and intro and r != intro and is_ancestor(root, r, intro)):
                    new_unpinned += 1
                    notes.append(f"{p}: pin {r[:12]} is not a commit that strictly precedes the commit that introduced the receipt")
    valid: set[str] = set()
    for num, paths in sorted(by_num.items()):
        for extra in paths[1:]:
            new_unpinned += 1
            notes.append(f"{extra}: second receipt for claim {num} (a re-run lands as rerun-c{num}-*.txt)")
        path = paths[0]
        text = blob(root, tip, path) or ""
        lines = REV_RE.findall(text)
        intro = first_add(root, tip, path)
        ok = (len(lines) == 1 and measured_rev is not None and lines[0] == measured_rev and bool(intro)
              and measured_rev != intro and is_ancestor(root, measured_rev, intro))
        why = "" if ok else f"revisions={lines} measured={measured_rev} introduced={intro[:12]}"
        if ok and check_bodies:
            body = text.replace("\r\n", "\n").split("\n")
            first = body[0] if body else ""
            if num in BODY_FIRST:
                why = body_shape(num, first, body)
                ok = not why
            else:
                tips = re.findall(r"(?m)^[ \t]*tip:[ \t]*([0-9a-f]{40})[ \t]*$", text)
                t0 = tips[0] if len(tips) == 1 else None
                ok = t0 is not None and len([ln for ln in body if ln.strip() == "EXIT=0"]) == 1
                why = "" if ok else "body carries no single `tip: <40-hex>` line or not exactly one EXIT=0"
                if ok:
                    lc = last_commit(root, tip, path)
                    allthree = all(blob(root, t0, q) is not None for q in (by_num.get(n, [""])[0] for n in ("1", "2", "3")))
                    fine = (is_commit(root, t0) and is_ancestor(root, measured_rev, t0) and t0 != lc and is_ancestor(root, t0, lc) and allthree)
                    if not fine:
                        ok, why = False, f"tip {t0[:12]} is not a descendant of the measured revision holding all three receipts and a strict ancestor of the commit that wrote the body"
                    else:
                        rerun = measure(root, t0, check_bodies=False)
                        want = report_first_line(rerun)
                        ok = first == want
                        why = "" if ok else f"body line {first[:90]!r} != re-derived {want[:90]!r}"
        if ok:
            valid.add(num)
        else:
            new_unpinned += 1
            notes.append(f"{path}: {why}")
    sc = blob(root, tip, "SCORECARD.md") or ""
    labelled = [m.group(1).strip().strip("`*").strip() for m in LABEL_RE.finditer(scorecard_section(sc))]
    scorecard_pin = int(measured_rev is not None and bool(labelled) and all(x == measured_rev for x in labelled))
    v = {"tip": tip, "population": len(present), "relabels_old": len(old), "undisclosed_relabels": len(undisclosed),
         "phantom_errata": len(phantom), "deleted_receipts": deleted_receipts, "new_relabelled": len(new_rel),
         "new_unpinned": new_unpinned, "new_receipts": len(valid), "scorecard_pin": scorecard_pin,
         "undisclosed": undisclosed, "phantom": phantom, "notes": notes, "measured": measured_rev}
    v["met"] = met(v)
    return v


def met(v: dict) -> bool:
    return (v["undisclosed_relabels"] == 0 and v["phantom_errata"] == 0 and v["deleted_receipts"] == 0
            and v["new_relabelled"] == 0 and v["new_unpinned"] == 0 and v["new_receipts"] == 3 and v["scorecard_pin"] == 1)


KEYS = ("undisclosed_relabels", "phantom_errata", "deleted_receipts", "new_relabelled", "new_unpinned", "new_receipts", "scorecard_pin")


def report_first_line(v: dict) -> str:
    return "C1 receipt-pins " + " ".join(f"{k}={v[k]}" for k in KEYS) + f" met={met(v)}  ({PREDICATE})"


def report(v: dict) -> str:
    out = [report_first_line(v), f"  population={v['population']} relabels_in_history={v['relabels_old']} base={BASE_REV[:12]}"]
    for r in v["undisclosed"]:
        out.append(f"  UNDISCLOSED {r[0]} {r[1][:12]} -> {r[2][:12]} at {r[3][:12]}")
    for r in v["phantom"]:
        out.append(f"  PHANTOM {r[0]} {r[1][:12]} -> {r[2][:12]} at {r[3][:12]}")
    for n in v["notes"]:
        out.append(f"  UNPINNED {n}")
    out.append(f"  tip: {v['tip']}")
    return "\n".join(out)


# --------------------------------------------------------------------------- selftest
_ID = ["-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false"]


class Sandbox:
    def __init__(self):
        self.first = ""
        self.d = tempfile.mkdtemp(prefix="c57-pins-")
        subprocess.run(["git", "-C", self.d, "init", "-q", "-b", "main"], check=True, env=clean_env())
        top = subprocess.run(["git", "-C", self.d, "rev-parse", "--show-toplevel"], capture_output=True, text=True, env=clean_env()).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(self.d), "sandbox is not its own toplevel"

    def git(self, *args: str) -> str:
        p = subprocess.run(["git", "-C", self.d, *_ID, *args], capture_output=True, text=True, env=clean_env())
        if p.returncode != 0:
            raise RuntimeError(f"git {args}: {p.stderr}")
        return p.stdout.strip()

    def commit(self, files: dict[str, str | None], msg: str = "c") -> str:
        for p, t in files.items():
            full = os.path.join(self.d, p)
            if t is None:
                os.remove(full)
            else:
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "w") as fh:
                    fh.write(t)
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", msg)
        head = self.git("rev-parse", "HEAD")
        if not self.first:
            self.first = head
            globals()["BASE_REV"] = head  # the sandbox's own first commit plays the round base
        return head

    def close(self):
        shutil.rmtree(self.d, ignore_errors=True)


def _json(o) -> str:
    return json.dumps(o, indent=1)


def selftest() -> int:
    for k in SCRUB:
        os.environ.pop(k, None)
    saved = BASE_REV
    OLD = ".ufo/waves/round-56/controls/after-c1.txt"
    NEWP = {n: f".ufo/waves/round-57/controls/after-c{n}-x.txt" for n in (1, 2, 3)}
    C2 = "C2 id-resolver 5/5 met=True  (met: gate_conditions_passed == 5 of 5)"
    C2F = "C2 id-resolver 3/5 met=False  (met: gate_conditions_passed == 5 of 5)"
    C3 = "C3 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)"
    results: list[tuple[str, bool]] = []

    def scenario(name: str, build, want_met: bool | None, want: dict | None = None):
        sb = Sandbox()
        try:
            tip = build(sb)
            try:
                v = measure(sb.d, tip)
                ok = v["met"] == want_met and all(v.get(k) == x for k, x in (want or {}).items())
                detail = f"met={v['met']} " + " ".join(f"{k}={v[k]}" for k in KEYS)
                if not ok and v["notes"]:
                    detail += " | " + "; ".join(v["notes"])[:220]
            except Unevaluable as exc:
                ok, detail = want_met is None, f"unevaluable {str(exc)[:120]}"
            results.append((f"{name}: {detail}", ok))
        finally:
            sb.close()

    def rec(first: str, rev: str, code: int, extra: str = "") -> str:
        return f"{first}\n  revision: {rev}\n{extra}EXIT={code}\n"

    def honest(sb: Sandbox, *, old_relabel=False, errata=None, deleted_old=False, skip_new=None, new_rev=None, side_measured=False, bad_errata=None,
               extra_line=False, scorecard="ok", c1_body="derived", c2=(C2, 0), c3=(C3, 0), rewrite_new=False, measured_before_counter=False,
               malformed_name=False, dup_claim=False, measured_json=None, tip_inside=False, skip_measured_json=False, counter_edit=False,
               freeze_bad=None, x_is_intro=False, extra_files=None, quiet=None):
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n", "SCORECARD.md": "# s\n"}, "old receipt")
        if old_relabel:
            sb.commit({OLD: f"revision: {'b' * 40}\nEXIT=0\n"}, "relabel")
        if deleted_old:
            sb.commit({OLD: None}, "delete")
        pre_counter = sb.commit({f"{WAVE}/x": "x\n"}, "round 57 before the counter")
        intro = sb.commit({p: f"# {os.path.basename(p)} v1\n" for p in FROZEN_FILES}, "add the counters and the tool")
        F = sb.commit({f"{WAVE}/frozen": "counters frozen\n"}, "freeze the counters")
        X = intro if x_is_intro else sb.commit({f"{WAVE}/y": "y\n"}, "round 57 work")
        if counter_edit:
            F, X = F, sb.commit({FROZEN_FILES[2]: "# quote counter v2 (edited after the freeze)\n"}, "counter edited after the freeze")
        mrev = new_rev or X
        if measured_before_counter:
            mrev = pre_counter
        if side_measured:
            sb.git("checkout", "-q", "-b", "side")
            mrev = sb.commit({"side.txt": "s\n"}, "side")
            sb.git("checkout", "-q", "main")
        files: dict[str, str | None] = {}
        if not skip_measured_json:
            files[MEASURED] = measured_json if measured_json is not None else _json({"revision": mrev, "countersFrozenAt": freeze_bad or F})
        if errata is not None:
            files[ERRATA] = errata(sb)
        if bad_errata is not None:
            files[ERRATA] = bad_errata
        sc = {"ok": f"# s\n## Round 57 — measured\nMeasured revision: {mrev}\n",
              "negated": f"# s\n## Round 57 — measured\nNOT measured at {mrev[:12]}; no run\n",
              "other": f"# s\n## Round 57 — measured\nMeasured revision: {mrev}\nMeasured revision: {'9' * 40}\n",
              "bold": f"# s\n## Round 57 — measured\n- **Measured revision:** {mrev}\n",
              "abbrev": f"# s\n## Round 57 — measured\nMeasured revision: {mrev}\nMeasured revision: 9999999\n",
              "bold-other": f"# s\n## Round 57 — measured\nMeasured revision: {mrev}\n- **Measured revision:** {'9' * 40}\n",
              "fenced": f"# s\n## Round 57 — measured\nMeasured revision: {mrev}\n```text\n## Round 56 — quoted\nMeasured revision: {'9' * 40}\n```\n",
              "fenced-other": f"# s\n## Round 57 — measured\nMeasured revision: {mrev}\n```text\nMeasured revision: {'9' * 40}\n```\n",
              "none": "# s\n## Round 57 — measured\nnothing\n"}[scorecard]
        files["SCORECARD.md"] = sc
        bodies = {1: "pending\n", 2: rec(c2[0], mrev, c2[1], f"  revision: {mrev}\n" if extra_line else ""), 3: rec(c3[0], mrev, c3[1])}
        for n in (1, 2, 3):
            if skip_new == n:
                continue
            body = bodies[n]
            if n == 1:
                body = f"pending\n  revision: {mrev}\n" + (f"  revision: {mrev}\n" if extra_line else "") + "EXIT=0\n"
            files[NEWP[n]] = body
        if malformed_name:
            files[".ufo/waves/round-57/controls/after-c4-x.txt"] = f"revision: {mrev}\n"
        if dup_claim:
            files[".ufo/waves/round-57/controls/after-c2-second.txt"] = rec(C2, mrev, 0)
        if quiet is not None:
            files[".ufo/waves/round-57/controls/tooling.txt"] = quiet.replace("@MREV@", mrev)
        files.update(extra_files or {})
        t0 = sb.commit(files, "pins and receipts")
        if skip_new == 1:
            return t0
        if c1_body == "derived":
            try:
                v0 = measure(sb.d, t0, check_bodies=False)
            except Unevaluable:
                return t0  # malformed inputs: the unevaluable scenarios stop here
            first = report_first_line(v0)
            body = f"{first}\n  tip: {X if tip_inside else t0}\n  revision: {mrev}\nEXIT=0\n"
        else:
            body = c1_body.replace("@MREV@", mrev).replace("@T0@", t0)
        tip = sb.commit({NEWP[1]: body}, "c1 receipt written after the run")
        if rewrite_new:
            tip = sb.commit({NEWP[2]: rec(C2, "e" * 40, 0)}, "relabel new")
        return tip

    def err(sb):
        h = sb.git("log", "--format=%H", "-1", "--", OLD)
        return _json({"entries": [{"path": OLD, "from": "a" * 40, "to": "b" * 40, "commit": h}]})

    S = scenario
    S("honest, no relabel", lambda sb: honest(sb), True, {"new_receipts": 3, "scorecard_pin": 1})
    S("old relabel undisclosed", lambda sb: honest(sb, old_relabel=True), False, {"undisclosed_relabels": 1})
    S("old relabel disclosed with matching errata", lambda sb: honest(sb, old_relabel=True, errata=err), True)
    S("errata names nothing git shows", lambda sb: honest(sb, errata=err), False, {"phantom_errata": 1})
    S("errata wrong 'to'", lambda sb: honest(sb, old_relabel=True, errata=lambda s: err(s).replace("b" * 40, "d" * 40)), False, {"undisclosed_relabels": 1, "phantom_errata": 1})
    S("errata wrong commit", lambda sb: honest(sb, old_relabel=True, errata=lambda s: _json({"entries": [{"path": OLD, "from": "a" * 40, "to": "b" * 40, "commit": "f" * 40}]})), False,
      {"undisclosed_relabels": 1, "phantom_errata": 1})
    S("errata duplicate entries are malformed", lambda sb: honest(sb, old_relabel=True, errata=lambda s: _json({"entries": json.loads(err(s))["entries"] * 2})), None)
    S("errata entry of ints is malformed", lambda sb: honest(sb, bad_errata=_json({"entries": [{"path": 1, "from": 2, "to": 3, "commit": 4}]})), None)
    S("errata unparsable", lambda sb: honest(sb, bad_errata="{not json"), None)
    S("empty errata file is malformed", lambda sb: honest(sb, bad_errata=""), None)
    S("measured.json is a list", lambda sb: honest(sb, measured_json="[]"), None)
    S("measured.json lacks countersFrozenAt", lambda sb: honest(sb, measured_json='{"revision": "' + "a" * 40 + '"}'), None)
    S("receipt deleted", lambda sb: honest(sb, deleted_old=True), False, {"deleted_receipts": 1})
    S("new receipt relabelled", lambda sb: honest(sb, rewrite_new=True), False, {"new_relabelled": 1})
    S("new receipt missing claim 3 (claim 1 still records the unmet state it re-derived)", lambda sb: honest(sb, skip_new=3), False, {"new_receipts": 2})
    S("new receipt wrong revision", lambda sb: honest(sb, new_rev="9" * 40), False)
    S("measured revision is not an ancestor of the receipts", lambda sb: honest(sb, side_measured=True), False)
    S("measured revision predates the counter", lambda sb: honest(sb, measured_before_counter=True), False)
    S("measured revision is the counter's own introduction commit", lambda sb: honest(sb, x_is_intro=True), False)
    S("a counter edited after the freeze", lambda sb: honest(sb, counter_edit=True), False)
    S("countersFrozenAt is not a commit", lambda sb: honest(sb, freeze_bad="1" * 40), False)
    S("new receipt with two identical revision lines", lambda sb: honest(sb, extra_line=True), False)
    S("measured.json missing", lambda sb: honest(sb, skip_measured_json=True), False)
    S("SCORECARD omits the pin", lambda sb: honest(sb, scorecard="none"), False, {"scorecard_pin": 0})
    S("SCORECARD negates the run", lambda sb: honest(sb, scorecard="negated"), False, {"scorecard_pin": 0})
    S("SCORECARD names a second measured revision", lambda sb: honest(sb, scorecard="other"), False, {"scorecard_pin": 0})
    S("SCORECARD bold label form is read", lambda sb: honest(sb, scorecard="bold"), True, {"scorecard_pin": 1})
    S("SCORECARD abbreviated second pin is a contradiction", lambda sb: honest(sb, scorecard="abbrev"), False, {"scorecard_pin": 0})
    S("SCORECARD bold second pin is a contradiction", lambda sb: honest(sb, scorecard="bold-other"), False, {"scorecard_pin": 0})
    S("a fenced contradiction inside the section is ignored", lambda sb: honest(sb, scorecard="fenced"), True, {"scorecard_pin": 1})
    S("a fenced contradicting line does not truncate or fail", lambda sb: honest(sb, scorecard="fenced-other"), True, {"scorecard_pin": 1})
    S("malformed after-* name", lambda sb: honest(sb, malformed_name=True), False)
    S("second receipt for claim 2", lambda sb: honest(sb, dup_claim=True), False)
    S("claim 2 records a failed run honestly (valid shape; C1 does not need C2 to succeed)", lambda sb: honest(sb, c2=(C2F, 1)), True, {"new_receipts": 3})
    S("claim 2 report line and EXIT disagree", lambda sb: honest(sb, c2=(C2, 1)), False)
    S("claim 2 says 3/5 met=True", lambda sb: honest(sb, c2=("C2 id-resolver 3/5 met=True  (met: gate_conditions_passed == 5 of 5)", 0)), False)
    S("claim 3 body is a bare pin", lambda sb: honest(sb, c3=("x", 0)), False)
    S("claim 1 body is the base control copied", lambda sb: honest(
        sb, c1_body=f"C1 receipt-pins undisclosed_relabels=6 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0 met=False  ({PREDICATE})\n  tip: @T0@\n  revision: @MREV@\nEXIT=0\n"), False)
    S("claim 1 body without a tip line", lambda sb: honest(sb, c1_body="C1 receipt-pins met=True\n  revision: @MREV@\nEXIT=0\n"), False)
    S("claim 1 tip predates the receipts it is said to have scored", lambda sb: honest(sb, tip_inside=True), False)
    S("a quiet round-57 control carrying a fabricated pin", lambda sb: honest(sb, quiet="note\nrevision: " + "f" * 40 + "\n"), False)

    def eq_form(sb):
        sb.commit({OLD: f"revision={'a' * 40}\n"}, "r")
        sb.commit({OLD: f"revision={'b' * 40}\n"}, "relabel (= form)")
        return sb.commit({}, "tip")

    S("= form relabel detected", eq_form, False, {"undisclosed_relabels": 1})

    def json_form(sb):
        p = ".ufo/waves/round-56/controls/x.json"
        sb.commit({p: f'{{\n "revision": "{"a" * 40}"\n}}\n'}, "r")
        sb.commit({p: f'{{\n "revision": "{"b" * 40}"\n}}\n'}, "relabel (json)")
        return sb.commit({}, "tip")

    S("quoted JSON key relabel detected", json_form, False, {"undisclosed_relabels": 1})

    def keep_same(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\nA\n"}, "r")
        sb.commit({OLD: f"revision: {'a' * 40}\nB edited, same pin\n"}, "edit body only")
        return sb.commit({}, "tip")

    S("edit that keeps the pin is not a relabel", keep_same, False, {"undisclosed_relabels": 0})

    def strip_then_new(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.commit({OLD: "stripped\n"}, "strip the line")
        sb.commit({OLD: f"revision: {'b' * 40}\n"}, "new pin after the strip")
        return sb.commit({}, "tip")

    S("stripped then re-pinned yields two relabels", strip_then_new, False, {"undisclosed_relabels": 2})

    def second_pin(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.commit({OLD: f"revision: {'a' * 40}\nrevision: {'c' * 40}\n"}, "second pin added")
        return sb.commit({}, "tip")

    S("a receipt gaining a second pin is a relabel", second_pin, False, {"undisclosed_relabels": 1})

    def hex41(sb):
        sb.commit({OLD: f"revision: {'c' * 41}\n"}, "41-hex is not a pin")
        return sb.commit({}, "tip")

    S("a 41-hex revision line is not a pin", hex41, False, {"undisclosed_relabels": 0})

    def delete_readd(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.commit({OLD: None}, "delete")
        sb.commit({OLD: f"revision: {'b' * 40}\n"}, "re-add with another pin")
        return sb.commit({}, "tip")

    S("deleted then re-added with another pin is a relabel", delete_readd, False, {"undisclosed_relabels": 1, "deleted_receipts": 0})

    def delete_readd_same(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n"}, "r")
        sb.commit({OLD: None}, "delete")
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n"}, "re-add byte-identical")
        return sb.commit({}, "tip")

    S("deleted and re-added identically leaves no latch", delete_readd_same, False, {"deleted_receipts": 0, "undisclosed_relabels": 0})

    def rename_relabel(sb):
        body = "body body body body\n" * 12
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n" + body}, "r")
        sb.git("mv", OLD, ".ufo/waves/round-56/controls/moved.txt")
        sb.commit({".ufo/waves/round-56/controls/moved.txt": f"revision: {'b' * 40}\nEXIT=0\n" + body}, "move and relabel")
        return sb.commit({}, "tip")

    S("rename plus relabel in one commit is seen under the new path", rename_relabel, False, {"undisclosed_relabels": 1, "deleted_receipts": 1})

    def move_out(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n" + "body body body body\n" * 12}, "r")
        os.makedirs(os.path.join(sb.d, ".ufo/waves/round-56/notes"), exist_ok=True)
        sb.git("mv", OLD, ".ufo/waves/round-56/notes/moved.txt")
        sb.commit({}, "move out of the population")
        return sb.commit({}, "tip")

    S("a receipt moved out of the population counts as vanished", move_out, False, {"deleted_receipts": 1})

    def move_out_and_back(sb):  # ReviewerPinsV2 F3
        body = "body body body body\n" * 12
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n" + body}, "r")
        os.makedirs(os.path.join(sb.d, ".ufo/waves/round-56/notes"), exist_ok=True)
        sb.git("mv", OLD, ".ufo/waves/round-56/notes/moved.txt")
        sb.commit({}, "move out")
        sb.git("mv", ".ufo/waves/round-56/notes/moved.txt", OLD)
        sb.commit({OLD: f"revision: {'b' * 40}\nEXIT=0\nentirely different text\n"}, "move back, relabelled")
        return sb.commit({}, "tip")

    S("moved out and back with another pin is a relabel", move_out_and_back, False, {"undisclosed_relabels": 1})

    def merged_side(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.git("checkout", "-q", "-b", "side")
        sb.commit({OLD: f"revision: {'b' * 40}\n"}, "side relabel")
        sb.git("checkout", "-q", "main")
        sb.commit({"other.txt": "o\n"}, "main work")
        sb.git("merge", "-q", "--no-ff", "-m", "merge side", "side")
        return sb.commit({}, "tip")

    S("relabel on a merged side branch is recorded once, at its own commit", merged_side, False, {"undisclosed_relabels": 1})

    def merge_resolution(sb):  # ReviewerPinsV2 F1: the relabel happens inside the merge commit
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.git("checkout", "-q", "-b", "side")
        sb.commit({"side.txt": "s\n"}, "side work")
        sb.git("checkout", "-q", "main")
        sb.commit({"other.txt": "o\n"}, "main work")
        sb.git("merge", "-q", "--no-ff", "--no-commit", "side")
        with open(os.path.join(sb.d, OLD), "w") as fh:
            fh.write(f"revision: {'b' * 40}\n")
        sb.git("add", "-A")
        sb.git("commit", "-q", "-m", "merge side (resolution relabels)")
        return sb.commit({}, "tip")

    S("a relabel written inside a merge commit is seen", merge_resolution, False, {"undisclosed_relabels": 1})

    def branched(sb):  # ReviewerPinsV2 F2: two branches relabel differently; each `from` is its own parent's pin
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.git("checkout", "-q", "-b", "side")
        s = sb.commit({OLD: f"revision: {'b' * 40}\n"}, "side relabels to b")
        sb.git("checkout", "-q", "main")
        m = sb.commit({OLD: f"revision: {'c' * 40}\n"}, "main relabels to c")
        sb.git("merge", "-q", "--no-ff", "-X", "ours", "-m", "merge", "side")
        tip = sb.commit({}, "tip")
        entries = [{"path": OLD, "from": "a" * 40, "to": "b" * 40, "commit": s}, {"path": OLD, "from": "a" * 40, "to": "c" * 40, "commit": m}]
        return sb.commit({ERRATA: _json({"entries": entries})}, "disclose both")

    S("a branched receipt: each relabel is disclosable with its own parent's pin", branched, False, {"undisclosed_relabels": 0, "phantom_errata": 0})

    def new_on_side(sb):
        honest(sb)
        sb.git("checkout", "-q", "-b", "sideN")
        sb.commit({NEWP[3]: rec(C3, "a" * 40, 0)}, "side: wrong pin")
        sb.commit({NEWP[3]: rec(C3, sb.git("rev-parse", "main~2"), 0)}, "side: relabel to look right")
        sb.git("checkout", "-q", "main")
        sb.git("merge", "-q", "--no-ff", "-m", "merge sideN", "sideN")
        return sb.commit({}, "tip")

    S("a new receipt relabelled on a merged side branch is seen", new_on_side, False)

    def shortfall(sb):  # ReviewerPinsV2 F5: an added file must not mask a lost base receipt
        sb.commit({OLD: f"revision: {'a' * 40}\n", ".ufo/waves/round-56/controls/second.txt": f"revision: {'a' * 40}\n"}, "two receipts")
        sb.commit({".ufo/waves/round-56/controls/second.txt": None}, "lose one")
        sb.commit({".ufo/waves/round-56/controls/extra.txt": "no pin\n"}, "add an unrelated file")
        return sb.commit({}, "tip")

    S("an added receipt does not mask a lost base receipt", shortfall, False, {"deleted_receipts": 1})

    def nonascii(sb):  # ReviewerPinsV2 F10
        sb.commit({".ufo/waves/round-57/controls/after-c2-测试.txt": f"x\n"}, "non-ASCII second receipt")
        return honest(sb)

    S("a non-ASCII second receipt for a claim is seen", nonascii, False)

    def outside(sb):
        sb.commit({".ufo/waves/round-40/controls/x.txt": f"revision: {'a' * 40}\n"}, "r40")
        sb.commit({".ufo/waves/round-40/controls/x.txt": f"revision: {'b' * 40}\n"}, "r40 relabel")
        return honest(sb)

    S("round outside 52-57 is out of population", outside, True)

    def r54(sb):
        R54 = ".ufo/waves/round-54/controls/after-c1.txt"
        sb.commit({R54: f"revision: {'a' * 40}\n"}, "r54 receipt")
        sb.commit({R54: f"revision: {'b' * 40}\n"}, "r54 relabel")
        return honest(sb)

    S("round-54 relabel undisclosed", r54, False, {"undisclosed_relabels": 1})

    def nonclaim(sb):
        O = ".ufo/waves/round-57/controls/tooling.txt"
        sb.commit({O: f"revision: {'a' * 40}\n"}, "other receipt")
        sb.commit({O: f"revision: {'b' * 40}\n"}, "relabel other")
        return honest(sb)

    S("round-57 non-claim control relabelled", nonclaim, False, {"new_relabelled": 1, "undisclosed_relabels": 0})

    def ladder(sb):
        p = ".ufo/waves/round-52/control/c1-mutation-ladder.json"
        sb.commit({p: '{"old_tail": "  revision: ' + "a" * 40 + '"}\n'}, "ladder")
        sb.commit({p: '{"old_tail": "  revision: ' + "b" * 40 + '"}\n'}, "ladder rewrite")
        return honest(sb)

    S("the mutation-ladder JSON is excluded from the population", ladder, True)

    def ladder_pretty(sb):
        p = ".ufo/waves/round-52/control/c1-mutation-ladder.json"
        sb.commit({p: f'{{\n "revision": "{"a" * 40}"\n}}\n'}, "ladder")
        sb.commit({p: f'{{\n "revision": "{"b" * 40}"\n}}\n'}, "ladder rewrite")
        return honest(sb)

    S("the exclusion is by name, also for a bare pin line", ladder_pretty, True)

    # base anchor: the sandbox has no commit named BASE_REV unless set from its first commit; this one checks the failure itself
    sb0 = Sandbox()
    try:
        tip0 = honest(sb0)
        globals()["BASE_REV"] = "0" * 40
        v0 = measure(sb0.d, tip0)
        results.append((f"history without the base revision is flagged: new_unpinned={v0['new_unpinned']} met={v0['met']}",
                        (not v0["met"]) and any("history replaced" in n for n in v0["notes"])))
    finally:
        sb0.close()

    # CLI cases run the module in a child with the sandbox base set in-process (no environment override exists)
    me = os.path.abspath(__file__)
    driver = ("import importlib.util, sys; spec = importlib.util.spec_from_file_location('c57pins', sys.argv[1]); m = importlib.util.module_from_spec(spec); "
              "spec.loader.exec_module(m); m.BASE_REV = sys.argv[2]; sys.argv = ['c57'] + sys.argv[3:]; sys.exit(m.main())")

    def cli(name, build, extra, want_exit, want_text=None):
        sb = Sandbox()
        try:
            tip = build(sb) if build else None
            args = ["--root", sb.d] + ([] if tip is None else ["--revision", tip]) + extra
            p = subprocess.run([sys.executable, "-B", "-c", driver, me, globals()["BASE_REV"], *args], capture_output=True, text=True, env=clean_env())
            ok = p.returncode == want_exit and (want_text is None or want_text in p.stdout)
            results.append((f"CLI {name}: exit={p.returncode}", ok))
        finally:
            sb.close()

    cli("met repo exits 0", lambda sb: honest(sb), [], 0)
    cli("unmet repo exits 1", lambda sb: honest(sb, old_relabel=True), [], 1)
    cli("malformed errata exits 2", lambda sb: honest(sb, bad_errata="{not json"), [], 2)
    cli("usage error (no revision) exits 64", None, [], 64)
    cli("unknown flag exits 64", lambda sb: honest(sb), ["--no-such-flag"], 64)
    cli("unresolvable revision exits 2", None, ["--revision", "not-a-rev"], 2)
    cli("--no-bodies prints the re-derivation line the body must carry", lambda sb: honest(sb), ["--no-bodies"], 0, "C1 receipt-pins undisclosed_relabels=0")

    globals()["BASE_REV"] = saved
    ok = sum(1 for _, g in results if g)
    for name, g in results:
        print(("PASS " if g else "FAIL ") + name)
    print(f"c57 receipt-pins selftest: {ok}/{len(results)}")
    return 0 if ok == len(results) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Round-57 C1 counter (receipt revision pins)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", help="tip revision to measure")
    ap.add_argument("--no-bodies", action="store_true", help="skip the receipt-body checks (the line an after-c1 receipt must carry is printed this way at T0)")
    ap.add_argument("--selftest", action="store_true")
    try:
        args = ap.parse_args()
    except SystemExit as e:
        return 0 if e.code == 0 else 64
    try:
        if args.selftest:
            return selftest()
        if not args.revision:
            print("usage: --root <lane> --revision <rev> [--no-bodies] | --selftest", file=sys.stderr)
            return 64
        v = measure(os.path.abspath(args.root), args.revision, check_bodies=not args.no_bodies)
    except Unevaluable as exc:
        print(f"C1 receipt-pins unevaluable: {exc}")
        return 2
    except Exception as exc:  # a crash is unevaluable, never "not met"
        print(f"C1 receipt-pins unevaluable: {type(exc).__name__}: {exc}")
        return 2
    print(report(v))
    return 0 if v["met"] else 1


if __name__ == "__main__":
    sys.exit(main())
