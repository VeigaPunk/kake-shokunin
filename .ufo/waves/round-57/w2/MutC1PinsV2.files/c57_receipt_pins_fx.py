#!/usr/bin/env python3
"""Round-57 C1 counter — calibration: stated revision pins against the revision pins the receipts carry.

Version 1 was frozen at `b9a5d012f7fd`. Version 2 (after wave 1, before any claim was measured; attacks `w1/CriticC1Counter.md`,
`w1/CritCheatC1.md`, `w1/ReviewerPinsCode.md`, `w1/MutC1Pins.md`, `w1/ExecPinsIndependent.md`, `w1/CriticControlsSizing.md`) reads receipt
bodies, anchors the pin to a revision where the run was possible, follows renames and merges, validates its inputs and asserts the
SCORECARD pin on a labelled line. The predicate is unchanged.

Surface: the measurement receipts under `.ufo/waves/round-5[2-7]/{control,controls}/` that carry a `revision:`/`revision=` line (the
revision a counter was run against; the one JSON ladder that embeds old counters' printed tails is excluded), and the lane's
statement "Measured revision: <rev>". A report or SCORECARD says what was measured; the receipt says what the counter was actually run
over. A later commit that rewrites the receipt's revision line (a *relabel*) makes the stated pin and the run diverge (round-56 routed
defect 1, `corpus/lessons/round-56-verifier-spotcheck.md` §6.1). History cannot be rewritten, so a historical relabel is closed by
disclosure: `receipt-errata.json` names it with the true values and the counter checks every entry against git. A relabel of a
receipt this round introduces is never disclosable: it must not occur.

Definitions (derived from `git` over the whole ancestry of the tip, topological order, renames followed, never the working tree):
  receipt      a path in the population whose committed versions carry a 40-hex revision line (`"revision":` JSON form accepted).
  relabel      two successive versions of a receipt (a rename keeps the history) whose pin sets are both non-empty and differ, or the
               later carries none; a pin that was stripped and later replaced yields a second relabel from the last non-empty pin.
               Recorded as (path, from, to, commit) with the full 40-hex values and the later commit.
  disclosed    an entry of `.ufo/waves/round-57/receipt-errata.json` equal to a relabel on all four fields (no duplicates).
  measured     `.ufo/waves/round-57/measured.json` `revision`: a 40-hex commit that descends from the commit that added this counter,
               and is a strict ancestor of the commit that introduced each new receipt.
  new receipt  `.ufo/waves/round-57/controls/after-c<N>-*.txt`, N in 1, 2, 3; one file per N; every other `after-*` file in that
               directory is malformed. Each carries exactly one `revision:` line equal to the measured revision.
  body         at the tip each new receipt must also be what a run printed: after-c2 and after-c3 start with their counter's report line
               `met=True` with the frozen predicate sentence and carry `EXIT=0`; after-c1 carries `tip: <T0>` (a commit that contains all three
               receipts, descends from the measured revision, and is a strict ancestor of the commit that last wrote after-c1), starts with
               the report line this counter prints for T0 (re-derived here without bodies) with `met=True`, and carries `EXIT=0`.
               A receipt that records a failed run, a copy of another claim's body or a bare pin line is not a run.

Counted values:
  undisclosed_relabels  relabels in receipts outside round 57 with no matching errata entry.
  phantom_errata        errata entries that match no relabel.
  deleted_receipts      pinned population paths that vanished (deleted and not re-added, or renamed out of the population), plus the shortfall
                        of the population against the 44 receipts present at the base (45 files, the one mutation-ladder JSON excluded).
  new_relabelled        relabels of any round-57 file (merged branches included).
  new_unpinned          malformed, duplicated, unpinned or body-less new receipts; a measured revision that does not descend from the counter's
                        introduction; a base revision (`28fa0b23…`) that is not an ancestor of the tip.
  new_receipts          valid new receipts among claims 1, 2, 3.
  scorecard_pin         1 when every `Measured revision:` line of the SCORECARD `## Round 57` sections names the measured revision (and one exists).

Predicate (frozen in `contract.json`):

    met: undisclosed_relabels == 0 AND phantom_errata == 0 AND deleted_receipts == 0 AND new_relabelled == 0 AND new_unpinned == 0 AND new_receipts == 3 AND scorecard_pin == 1

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable, 64 usage.
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
BASE_POPULATION = 44
if os.environ.get("KAKE_R57_PINS_TEST_BASE"):  # selftest only: "<rev>:<population>" for a sandbox whose history has no round-57 base
    BASE_REV, _pop = os.environ["KAKE_R57_PINS_TEST_BASE"].split(":")
    BASE_POPULATION = int(_pop)
WAVE = ".ufo/waves/round-57"
COUNTER = f"{WAVE}/c57_receipt_pins.py"
ERRATA = f"{WAVE}/receipt-errata.json"
MEASURED = f"{WAVE}/measured.json"
NEW_RE = re.compile(r"^\.ufo/waves/round-57/controls/after-c([123])-[^/]+\.txt$")
POP_RE = re.compile(r"^\.ufo/waves/round-5[2-7]/(control|controls)/[^/]+\.(txt|json)$")
EXCLUDE_RE = re.compile(r"-mutation-ladder\.json$")
REV_RE = re.compile(r'(?m)^[ \t]*"?revision"?[ \t]*[:=][ \t]*"?([0-9a-f]{40})\b')
HEX40 = re.compile(r"[0-9a-f]{40}")
BODY_FIRST = {
    "2": re.compile(r"^C2 id-resolver 5/5 met=True  \(met: gate_conditions_passed == 5 of 5\)$"),
    "3": re.compile(r"^C3 quote-truth 8/8 met=True  \(met: conditions_passed == 8 of 8\)$"),
}


class Unevaluable(Exception):
    pass


def git(root: str, *args: str) -> str:
    p = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise Unevaluable(f"git {' '.join(args)}: {p.stderr.decode('utf-8', 'replace').strip()}")
    return p.stdout.decode("utf-8", "replace")


def blob(root: str, rev: str, path: str) -> str | None:
    p = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout.decode("utf-8", "replace") if p.returncode == 0 else None


def is_ancestor(root: str, anc: str, desc: str) -> bool:
    return subprocess.run(["git", "-C", root, "merge-base", "--is-ancestor", anc, desc],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def in_pop(path: str) -> bool:
    return bool(POP_RE.match(path)) and not EXCLUDE_RE.search(path)


def load_json(text: str | None, what: str):
    if text is None:
        return None
    try:
        return json.loads(text)
    except ValueError as exc:
        raise Unevaluable(f"{what} is not JSON: {exc}")


def walk_history(root: str, tip: str):
    """Yield (commit, records) oldest first over the whole ancestry; records are (status, path) or (status, old, new) for renames."""
    log = git(root, "log", "--topo-order", "--reverse", "--name-status", "-M", "--format=@@%H", tip)
    commit, recs = None, []
    for line in log.split("\n"):
        if line.startswith("@@"):
            if commit is not None:
                yield commit, recs
            commit, recs = line[2:], []
        elif "\t" in line:
            parts = line.split("\t")
            recs.append((parts[0][0], *parts[1:]))
    if commit is not None:
        yield commit, recs


def scan(root: str, tip: str):
    """Relabels, deletions and the population at the tip."""
    present = {p for p in git(root, "ls-tree", "-r", "--name-only", tip).split("\n") if in_pop(p)}
    last: dict[str, set[str]] = {}
    deleted: set[str] = set()
    relabels: list[tuple[str, str, str, str]] = []

    def compare(path: str, prev: set[str], cur: set[str], commit: str) -> None:
        if prev and cur != prev:
            for a in sorted(prev):
                for b in sorted(cur) or [""]:
                    if a != b:
                        relabels.append((path, a, b, commit))

    for commit, recs in walk_history(root, tip):
        for rec in recs:
            status = rec[0]
            if status == "R":
                old, new = rec[1], rec[2]
                prev = last.pop(old, set())
                if in_pop(old) and not in_pop(new):
                    if prev:
                        deleted.add(old)
                    continue
                if in_pop(new):
                    text = blob(root, commit, new)
                    cur = set(REV_RE.findall(text or ""))
                    compare(new, prev, cur, commit)
                    last[new] = cur or prev
                    deleted.discard(new)
                continue
            path = rec[1]
            if not in_pop(path):
                continue
            if status == "D":
                if last.get(path):
                    deleted.add(path)
                continue
            text = blob(root, commit, path)
            if text is None:
                continue
            cur = set(REV_RE.findall(text))
            compare(path, last.get(path, set()), cur, commit)
            if cur or path not in last:
                last[path] = cur
            deleted.discard(path)
    gone = sorted(p for p in deleted if p not in present)
    return present, relabels, gone


def last_commit(root: str, tip: str, path: str) -> str:
    return git(root, "log", "-1", "--format=%H", tip, "--", path).strip()


def first_add(root: str, tip: str, path: str) -> str:
    lines = [x for x in git(root, "log", "--topo-order", "--diff-filter=A", "--format=%H", tip, "--", path).strip().split("\n") if x]
    return lines[0] if lines else ""  # newest add: a deleted and re-added receipt counts from its current life


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


def measure(root: str, tip: str, check_bodies: bool = True) -> dict:
    tip = git(root, "rev-parse", "--verify", f"{tip}^{{commit}}").strip()
    present, relabels, gone = scan(root, tip)
    old = [r for r in relabels if not r[0].startswith(f"{WAVE}/")]
    new_rel = [r for r in relabels if r[0].startswith(f"{WAVE}/")]
    entries = parse_errata(root, tip)
    undisclosed = sorted(set(old) - set(entries))
    phantom = sorted(set(entries) - set(old))
    outside = len([p for p in present if not p.startswith(f"{WAVE}/")])
    deleted_receipts = len(gone) + max(0, BASE_POPULATION - outside - len(gone))
    notes: list[str] = []
    new_unpinned = 0
    if not is_ancestor(root, BASE_REV, tip):
        new_unpinned += 1
        notes.append(f"base revision {BASE_REV[:12]} is not an ancestor of the tip (history replaced)")
    mdata = load_json(blob(root, tip, MEASURED), MEASURED)
    measured_rev = None
    if mdata is not None:
        if not isinstance(mdata, dict) or not isinstance(mdata.get("revision"), str):
            raise Unevaluable(f"{MEASURED}: not an object with a string `revision`")
        measured_rev = mdata["revision"] if HEX40.fullmatch(mdata["revision"]) else None
        if measured_rev is None:
            notes.append(f"{MEASURED}: revision is not 40-hex")
            new_unpinned += 1
    counter_intro = first_add(root, tip, COUNTER)
    if measured_rev is not None and (not counter_intro or not is_ancestor(root, counter_intro, measured_rev)):
        new_unpinned += 1
        notes.append(f"measured revision {measured_rev[:12]} does not descend from the commit that added the counter ({counter_intro[:12] or 'none'})")
    new_paths = sorted(p for p in present if p.startswith(f"{WAVE}/") and os.path.basename(p).startswith("after-"))
    by_num: dict[str, list[str]] = {}
    for p in new_paths:
        m = NEW_RE.match(p)
        if not m:
            new_unpinned += 1
            notes.append(f"{p}: malformed `after-*` receipt name (expected after-c1|c2|c3-*.txt)")
        else:
            by_num.setdefault(m.group(1), []).append(p)
    valid: set[str] = set()
    for num, paths in sorted(by_num.items()):
        for extra in paths[1:]:
            new_unpinned += 1
            notes.append(f"{extra}: second receipt for claim {num}")
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
                ok = bool(BODY_FIRST[num].match(first)) and "EXIT=0" in body
                why = "" if ok else f"body does not start with the claim's met=True report line / carries no EXIT=0: {first[:90]!r}"
            else:
                tips = re.findall(r"(?m)^[ \t]*tip:[ \t]*([0-9a-f]{40})[ \t]*$", text)
                t0 = tips[0] if len(tips) == 1 else None
                ok = t0 is not None and "EXIT=0" in body
                why = "" if ok else "body carries no single `tip: <40-hex>` line or no EXIT=0"
                if ok:
                    lc = last_commit(root, tip, path)
                    fine = (is_ancestor(root, measured_rev, t0) and t0 != lc and is_ancestor(root, t0, lc)
                            and all(blob(root, t0, q) is not None for q in (by_num.get(n, [""])[0] for n in ("1", "2", "3"))))
                    if not fine:
                        ok, why = False, f"tip {t0[:12]} is not a descendant of the measured revision holding all three receipts and a strict ancestor of the commit that wrote the body"
                    else:
                        rerun = measure(root, t0, check_bodies=False)
                        want = report_first_line(rerun)
                        ok = rerun["met"] and first == want
                        why = "" if ok else f"body line {first[:90]!r} != re-derived {want[:90]!r} (met={rerun['met']})"
        if ok:
            valid.add(num)
        else:
            new_unpinned += 1
            notes.append(f"{path}: {why}")
    sc = blob(root, tip, "SCORECARD.md") or ""
    section = "".join(m.group(0) for m in re.finditer(r"(?ms)^## Round 57\b.*?(?=^## Round (?!57\b)\d+|\Z)", sc))
    pins = re.findall(r"(?m)^[ \t]*(?:[-*][ \t]+)?Measured revision:[ \t]*`?([0-9a-f]{40})`?[ \t]*$", section)
    scorecard_pin = int(measured_rev is not None and bool(pins) and all(x == measured_rev for x in pins))
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
    out = [report_first_line(v), f"  population={v['population']} relabels_in_history={v['relabels_old']}"]
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
        self.d = tempfile.mkdtemp(prefix="c57-pins-")
        self.first = ""
        subprocess.run(["git", "-C", self.d, "init", "-q", "-b", "main"], check=True)
        top = subprocess.run(["git", "-C", self.d, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(self.d), "sandbox is not its own toplevel"

    def git(self, *args: str) -> str:
        p = subprocess.run(["git", "-C", self.d, *_ID, *args], capture_output=True, text=True)
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
                open(full, "w").write(t)
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
    global BASE_REV, BASE_POPULATION
    saved = (BASE_REV, BASE_POPULATION)
    OLD = ".ufo/waves/round-56/controls/after-c1.txt"
    NEWP = {n: f".ufo/waves/round-57/controls/after-c{n}-x.txt" for n in (1, 2, 3)}
    C2 = "C2 id-resolver 5/5 met=True  (met: gate_conditions_passed == 5 of 5)"
    C3 = "C3 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)"
    results: list[tuple[str, bool]] = []

    def scenario(name: str, build, want_met: bool | None, want: dict | None = None):
        sb = Sandbox()
        try:
            globals()["BASE_POPULATION"] = 1
            tip = build(sb)
            try:
                v = measure(sb.d, tip)
                ok = v["met"] == want_met and all(v.get(k) == x for k, x in (want or {}).items())
                detail = f"met={v['met']} " + " ".join(f"{k}={v[k]}" for k in KEYS)
                if not ok and v["notes"]:
                    detail += " | " + "; ".join(v["notes"])[:200]
            except Unevaluable as exc:
                ok, detail = want_met is None, f"unevaluable {str(exc)[:120]}"
            results.append((f"{name}: {detail}", ok))
        finally:
            sb.close()

    def honest(sb: Sandbox, *, old_relabel=False, errata=None, deleted_old=False, skip_new=None, new_rev=None, side_measured=False,
               bad_errata=None, extra_line=False, scorecard="ok", c1_body="derived", c2_body=C2 + "\n", c3_body=C3 + "\n",
               rewrite_new=False, measured_before_counter=False, extra_files=None, malformed_name=False, dup_claim=False,
               measured_json=None, tip_inside=False, skip_measured_json=False):
        r1 = sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n", "SCORECARD.md": "# s\n"}, "old receipt")
        if old_relabel:
            sb.commit({OLD: f"revision: {'b' * 40}\nEXIT=0\n"}, "relabel")
        if deleted_old:
            sb.commit({OLD: None}, "delete")
        pre_counter = sb.commit({f"{WAVE}/x": "x\n"}, "round 57 before the counter")
        sb.commit({COUNTER: "# counter\n"}, "add the counter")
        X = sb.commit({f"{WAVE}/y": "y\n"}, "round 57 work")
        mrev = new_rev or X
        if measured_before_counter:
            mrev = pre_counter
        if side_measured:
            sb.git("checkout", "-q", "-b", "side")
            mrev = sb.commit({"side.txt": "s\n"}, "side")
            sb.git("checkout", "-q", "main")
        files: dict[str, str | None] = {}
        if not skip_measured_json:
            files[MEASURED] = measured_json if measured_json is not None else _json({"revision": mrev})
        if errata is not None:
            files[ERRATA] = errata(sb)
        if bad_errata is not None:
            files[ERRATA] = bad_errata
        sc = {"ok": f"# s\n## Round 57 — measured\nMeasured revision: {mrev}\n",
              "negated": f"# s\n## Round 57 — measured\nNOT measured at {mrev[:12]}; no run\n",
              "other": f"# s\n## Round 57 — measured\nMeasured revision: {mrev}\nMeasured revision: {'9' * 40}\n",
              "none": "# s\n## Round 57 — measured\nnothing\n"}[scorecard]
        files["SCORECARD.md"] = sc
        for n in (1, 2, 3):
            if skip_new == n:
                continue
            rev = f"revision: {mrev}\n" + (f"revision: {mrev}\n" if extra_line else "")
            body = {1: "pending\n", 2: c2_body, 3: c3_body}[n]
            files[NEWP[n]] = body.rstrip("\n") + "\n  " + rev + ("EXIT=0\n" if "EXIT=0" not in body else "")
        if malformed_name:
            files[".ufo/waves/round-57/controls/after-c4-x.txt"] = f"revision: {mrev}\n"
        if dup_claim:
            files[".ufo/waves/round-57/controls/after-c2-second.txt"] = f"{C2}\n  revision: {mrev}\nEXIT=0\n"
        files.update(extra_files or {})
        t0 = sb.commit(files, "pins and receipts")
        if c1_body == "derived" and skip_new != 1:
            try:
                v0 = measure(sb.d, t0, check_bodies=False)
            except Unevaluable:
                return t0  # malformed inputs: the unevaluable scenarios stop here
            body = report_first_line(v0) + f"\n  tip: {t0}\n  revision: {mrev}\nEXIT=0\n"
            if tip_inside:  # the run is said to have happened before the receipts existed
                body = report_first_line(v0) + f"\n  tip: {X}\n  revision: {mrev}\nEXIT=0\n"
            tip = sb.commit({NEWP[1]: body}, "c1 receipt written after the run")
        elif c1_body != "derived" and skip_new != 1:
            tip = sb.commit({NEWP[1]: c1_body.replace("@MREV@", mrev).replace("@T0@", t0)}, "c1 receipt")
        else:
            tip = t0
        if rewrite_new:
            tip = sb.commit({NEWP[2]: f"{C2}\n  revision: {'e' * 40}\nEXIT=0\n"}, "relabel new")
        return tip

    def err(sb):
        h = sb.git("log", "--format=%H", "-1", "--", OLD)
        return _json({"entries": [{"path": OLD, "from": "a" * 40, "to": "b" * 40, "commit": h}]})

    scenario("honest, no relabel", lambda sb: honest(sb), True, {"new_receipts": 3, "scorecard_pin": 1})
    scenario("old relabel undisclosed", lambda sb: honest(sb, old_relabel=True), False, {"undisclosed_relabels": 1})
    scenario("old relabel disclosed with matching errata", lambda sb: honest(sb, old_relabel=True, errata=err), True)
    scenario("errata names nothing git shows", lambda sb: honest(sb, errata=err), False, {"phantom_errata": 1})
    scenario("errata wrong 'to'", lambda sb: honest(sb, old_relabel=True, errata=lambda s: err(s).replace("b" * 40, "d" * 40)), False,
             {"undisclosed_relabels": 1, "phantom_errata": 1})
    scenario("errata wrong commit", lambda sb: honest(sb, old_relabel=True, errata=lambda s: _json({"entries": [
        {"path": OLD, "from": "a" * 40, "to": "b" * 40, "commit": "f" * 40}]})), False, {"undisclosed_relabels": 1, "phantom_errata": 1})
    scenario("errata duplicate entries are malformed", lambda sb: honest(sb, old_relabel=True, errata=lambda s: _json(
        {"entries": json.loads(err(s))["entries"] * 2})), None)
    scenario("errata entry of ints is malformed (exit 2, not a traceback)", lambda sb: honest(
        sb, bad_errata=_json({"entries": [{"path": 1, "from": 2, "to": 3, "commit": 4}]})), None)
    scenario("errata unparsable", lambda sb: honest(sb, bad_errata="{not json"), None)
    scenario("empty errata file is malformed", lambda sb: honest(sb, bad_errata=""), None)
    scenario("measured.json is a list", lambda sb: honest(sb, measured_json="[]"), None)
    scenario("receipt deleted", lambda sb: honest(sb, deleted_old=True), False, {"deleted_receipts": 1})
    scenario("new receipt relabelled", lambda sb: honest(sb, rewrite_new=True), False, {"new_relabelled": 1})
    scenario("new receipt missing claim 3 (claim 1 cannot record a met run either)", lambda sb: honest(sb, skip_new=3), False, {"new_receipts": 1})
    scenario("new receipt wrong revision", lambda sb: honest(sb, new_rev="9" * 40), False)
    scenario("measured revision is not an ancestor of the receipts", lambda sb: honest(sb, side_measured=True), False)
    scenario("measured revision predates the counter", lambda sb: honest(sb, measured_before_counter=True), False)
    scenario("new receipt with two identical revision lines", lambda sb: honest(sb, extra_line=True), False)
    scenario("measured.json missing", lambda sb: honest(sb, skip_measured_json=True), False)
    scenario("SCORECARD omits the pin", lambda sb: honest(sb, scorecard="none"), False, {"scorecard_pin": 0})
    scenario("SCORECARD negates the run", lambda sb: honest(sb, scorecard="negated"), False, {"scorecard_pin": 0})
    scenario("SCORECARD names a second measured revision", lambda sb: honest(sb, scorecard="other"), False, {"scorecard_pin": 0})
    scenario("malformed after-* name", lambda sb: honest(sb, malformed_name=True), False)
    scenario("second receipt for claim 2", lambda sb: honest(sb, dup_claim=True), False)
    scenario("claim 2 body records a failed run", lambda sb: honest(sb, c2_body="C2 id-resolver 3/5 met=False  (met: gate_conditions_passed == 5 of 5)\nEXIT=1\n"), False)
    scenario("claim 3 body is a bare pin", lambda sb: honest(sb, c3_body="x\n"), False)
    scenario("claim 1 body records met=False (the base control copied)", lambda sb: honest(
        sb, c1_body=f"C1 receipt-pins undisclosed_relabels=6 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0 met=False  ({PREDICATE})\n  tip: @T0@\n  revision: @MREV@\nEXIT=0\n"), False)
    scenario("claim 1 body without a tip line", lambda sb: honest(sb, c1_body="C1 receipt-pins met=True\n  revision: @MREV@\nEXIT=0\n"), False)
    scenario("claim 1 tip predates the receipts it is said to have scored", lambda sb: honest(sb, tip_inside=True), False)


    # ---- mutation-kill fixtures (MutC1PinsV2, round-57 W2) ----
    def fx_shortfall(sb):  # kills outside-all-present: base population 2, only one receipt present at the tip
        globals()["BASE_POPULATION"] = 2
        return honest(sb)

    scenario("population shortfall against the base population counts", fx_shortfall, False, {"deleted_receipts": 1})

    def fx_moveout_unpinned(sb):  # kills rename-latch: a receipt that never carried a pin moves out of the population
        O2 = ".ufo/waves/round-55/controls/z.txt"
        sb.commit({O2: "no pin yet\n"}, "unpinned receipt")
        os.makedirs(os.path.join(sb.d, ".ufo/waves/round-55/notes"), exist_ok=True)
        sb.git("mv", O2, ".ufo/waves/round-55/notes/z.txt")
        sb.commit({}, "move the unpinned receipt out")
        return honest(sb)

    scenario("an unpinned receipt moved out of the population is not vanished", fx_moveout_unpinned, True)

    def fx_delete_unpinned(sb):  # kills delete-uncond: an unpinned receipt is deleted
        O2 = ".ufo/waves/round-55/controls/z.txt"
        sb.commit({O2: "no pin yet\n"}, "unpinned receipt")
        sb.commit({O2: None}, "delete the unpinned receipt")
        return honest(sb)

    scenario("an unpinned receipt deleted is not vanished", fx_delete_unpinned, True)

    def fx_rename_reuse(sb):  # kills rename-pop: the old name is re-added after a rename
        A = ".ufo/waves/round-56/controls/a.txt"
        B = ".ufo/waves/round-56/controls/b.txt"
        sb.commit({A: f"revision: {'a' * 40}\n"}, "r")
        sb.git("mv", A, B)
        sb.commit({}, "rename")
        sb.commit({A: f"revision: {'c' * 40}\n"}, "a new receipt reuses the old name")
        return honest(sb)

    scenario("a name reused after a rename starts its own history", fx_rename_reuse, True)

    def fx_rename_strip_repin(sb):  # kills rename-carry: a pin stripped by a rename, then re-pinned
        A = ".ufo/waves/round-56/controls/a.txt"
        B = ".ufo/waves/round-56/controls/b.txt"
        body = "x\n" * 200
        sb.commit({A: f"revision: {'a' * 40}\n{body}"}, "r")
        sb.git("mv", A, B)
        sb.commit({B: body}, "rename and strip the pin")
        sb.commit({B: f"revision: {'b' * 40}\n{body}"}, "re-pin under the new name")
        return honest(sb)

    scenario("a pin stripped by a rename and re-pinned yields two relabels", fx_rename_strip_repin, False, {"undisclosed_relabels": 2})

    def fx_second_pin_old(sb):  # kills compare-same-pin: a receipt gains a second pin while keeping the first
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.commit({OLD: f"revision: {'a' * 40}\nrevision: {'c' * 40}\n"}, "second pin added")
        return honest(sb)

    scenario("a receipt gaining a second pin yields two relabels", fx_second_pin_old, False, {"undisclosed_relabels": 2})

    def fx_hex41(sb):  # kills rev-bound: a 41-hex revision line is not a pin
        sb.commit({OLD: f"revision: {'c' * 41}\n"}, "41-hex is not a pin")
        return honest(sb)

    scenario("a 41-hex revision line is not a pin", fx_hex41, True)

    def fx_readd_draft_c2(sb):  # kills firstadd-oldest: after-c2 appears at the measured commit as a draft, is deleted, re-added at t0
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n", "SCORECARD.md": "# s\n"}, "old receipt")
        sb.commit({f"{WAVE}/x": "x\n"}, "round 57 before the counter")
        sb.commit({COUNTER: "# counter\n"}, "add the counter")
        X = sb.commit({f"{WAVE}/y": "y\n", NEWP[2]: f"{C2}\n  revision: pending\n"}, "round 57 work (draft receipt)")
        sb.commit({NEWP[2]: None}, "drop the draft")
        t0 = sb.commit({MEASURED: _json({"revision": X}),
                        "SCORECARD.md": f"# s\n## Round 57 — measured\nMeasured revision: {X}\n",
                        NEWP[1]: f"pending\n  revision: {X}\nEXIT=0\n",
                        NEWP[2]: f"{C2}\n  revision: {X}\nEXIT=0\n",
                        NEWP[3]: f"{C3}\n  revision: {X}\nEXIT=0\n"}, "pins and receipts")
        v0 = measure(sb.d, t0, check_bodies=False)
        body = report_first_line(v0) + f"\n  tip: {t0}\n  revision: {X}\nEXIT=0\n"
        return sb.commit({NEWP[1]: body}, "c1 receipt written after the run")

    scenario("a receipt re-added after a deleted draft counts from the re-add", fx_readd_draft_c2, True)

    def fx_counter_touched(sb):  # kills firstadd-alltouches: the counter file is edited after the run
        honest(sb)
        return sb.commit({COUNTER: "# counter v2\n"}, "counter edited after the run")

    scenario("the counter file edited after the run keeps its introduction commit", fx_counter_touched, True)

    def fx_body2_metfalse(sb):  # kills body2-metany: a met=False report line with EXIT=0 is not a run
        return honest(sb, c2_body="C2 id-resolver 5/5 met=False  (met: gate_conditions_passed == 5 of 5)\nEXIT=0\n")

    scenario("claim 2 body met=False with EXIT=0 is not a run", fx_body2_metfalse, False)

    def fx_c2_crlf(sb):  # kills body-crlf: CRLF endings are normalised before the body check
        return honest(sb, c2_body=C2 + "\r\n")

    scenario("claim 2 body with CRLF endings still matches the report line", fx_c2_crlf, True)

    def fx_late_c3(sb):  # kills tip-all3: claim 3 lands after the tip named by claim 1
        honest(sb, skip_new=3)
        mrev = sb.git("rev-parse", "HEAD~2")
        return sb.commit({NEWP[3]: f"{C3}\n  revision: {mrev}\nEXIT=0\n"}, "claim 3 lands after the run")

    scenario("claim 3 landing after the tip named by claim 1 fails the body", fx_late_c3, False, {"new_receipts": 2})

    def fx_errata_late(sb):  # kills tip-rerunmet: the state at t0 was not met, disclosure only came later
        honest(sb, old_relabel=True)
        h = sb.git("log", "--format=%H", "-1", "--", OLD)
        return sb.commit({ERRATA: _json({"entries": [{"path": OLD, "from": "a" * 40, "to": "b" * 40, "commit": h}]})}, "disclosed after the run")

    scenario("errata published after the t0 run keeps the c1 body invalid", fx_errata_late, False, {"new_receipts": 2})

    RLINE = ("C1 receipt-pins undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 "
             "new_receipts=3 scorecard_pin=1 met=True  (" + PREDICATE + ")")

    def fx_two_tips(sb):  # kills tip-multitip: exactly one tip line is required
        return honest(sb, c1_body=RLINE + "\n  tip: @T0@\n  tip: " + "a" * 40 + "\n  revision: @MREV@\nEXIT=0\n")

    scenario("a second tip line voids the c1 body", fx_two_tips, False, {"new_receipts": 2})

    def fx_side_copy(sb):  # kills tip-anc-dropped: t0 is on a side branch; the body predates the merge that brings it in
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n", "SCORECARD.md": "# s\n"}, "old receipt")
        sb.commit({f"{WAVE}/x": "x\n"}, "round 57 before the counter")
        cf = sb.commit({COUNTER: "# counter\n"}, "add the counter")
        sb.git("checkout", "-q", "-b", "side")
        t0 = sb.commit({MEASURED: _json({"revision": cf}),
                        "SCORECARD.md": f"# s\n## Round 57 — measured\nMeasured revision: {cf}\n",
                        NEWP[1]: f"pending\n  revision: {cf}\nEXIT=0\n",
                        NEWP[2]: f"{C2}\n  revision: {cf}\nEXIT=0\n",
                        NEWP[3]: f"{C3}\n  revision: {cf}\nEXIT=0\n"}, "receipts commit on a side branch")
        sb.git("checkout", "-q", "main")
        sb.commit({f"{WAVE}/y": "y\n"}, "round 57 work")
        v0 = measure(sb.d, t0, check_bodies=False)
        body = report_first_line(v0) + f"\n  tip: {t0}\n  revision: {cf}\nEXIT=0\n"
        sb.commit({NEWP[1]: body}, "c1 receipt written on main before the merge")
        sb.git("merge", "-q", "--no-ff", "-X", "ours", "-m", "merge side", "side")
        return sb.commit({}, "tip")

    scenario("a body last written on a side branch that lacks t0 fails", fx_side_copy, False, {"new_receipts": 2})

    def fx_bullet_pin(sb):  # kills sc-nobullet: a bulleted Measured revision: line counts
        honest(sb)
        mrev = sb.git("rev-parse", "HEAD~2")
        return sb.commit({"SCORECARD.md": f"# s\n## Round 57\n- Measured revision: {mrev}\n"}, "bulleted pin")

    scenario("a bulleted Measured revision line counts", fx_bullet_pin, True)

    def fx_measured_41(sb):  # kills measured-prefix: a 41-hex measured revision is not 40-hex
        honest(sb)
        mrev = sb.git("rev-parse", "HEAD~2")
        return sb.commit({MEASURED: _json({"revision": mrev + "0"})}, "41-hex measured revision")

    scenario("a 41-hex measured revision is rejected", fx_measured_41, False)

    def fx_errata_int_commit(sb):  # kills errata-3keys: a non-string commit field is malformed
        return honest(sb, old_relabel=True, errata=lambda s: _json(
            {"entries": [{"path": OLD, "from": "a" * 40, "to": "b" * 40, "commit": 7}]}))

    scenario("errata entry with a non-string commit is malformed", fx_errata_int_commit, None)

    def fx_backdated_side(sb):  # kills walk-topo: a backdated relabel on a side branch keeps topological order
        honest(sb)
        os.environ["GIT_AUTHOR_DATE"] = os.environ["GIT_COMMITTER_DATE"] = "2005-04-07T22:13:13"
        try:
            sb.git("checkout", "-q", "-b", "side2")
            h2 = sb.commit({OLD: f"revision: {'c' * 40}\nEXIT=0\n"}, "backdated relabel")
        finally:
            os.environ.pop("GIT_AUTHOR_DATE", None)
            os.environ.pop("GIT_COMMITTER_DATE", None)
        sb.git("checkout", "-q", "main")
        sb.git("merge", "-q", "--no-ff", "-m", "merge side2", "side2")
        return sb.commit({ERRATA: _json({"entries": [{"path": OLD, "from": "a" * 40, "to": "c" * 40, "commit": h2}]})}, "disclose")

    scenario("a backdated relabel on a side branch is found in topological order", fx_backdated_side, True)

    def fx_c4_valid(sb):  # kills newre-digit: after-c4 carries a valid body yet is not a claim
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n", "SCORECARD.md": "# s\n"}, "old receipt")
        sb.commit({f"{WAVE}/x": "x\n"}, "round 57 before the counter")
        sb.commit({COUNTER: "# counter\n"}, "add the counter")
        X = sb.commit({f"{WAVE}/y": "y\n"}, "round 57 work")
        t0 = sb.commit({MEASURED: _json({"revision": X}),
                        "SCORECARD.md": f"# s\n## Round 57 — measured\nMeasured revision: {X}\n",
                        NEWP[1]: f"pending\n  revision: {X}\nEXIT=0\n",
                        NEWP[2]: f"{C2}\n  revision: {X}\nEXIT=0\n",
                        NEWP[3]: f"{C3}\n  revision: {X}\nEXIT=0\n"}, "pins and receipts")
        v0 = measure(sb.d, t0, check_bodies=False)
        body = report_first_line(v0) + f"\n  tip: {t0}\n  revision: {X}\nEXIT=0\n"
        return sb.commit({NEWP[1]: body, ".ufo/waves/round-57/controls/after-c4-x.txt": body}, "c1 and c4 receipts written after the run")

    scenario("a valid-bodied after-c4 receipt is malformed, three claims stay", fx_c4_valid, False, {"new_unpinned": 1, "new_receipts": 3})


    def fx_ladder_pretty(sb):  # kills exclude-never: a ladder JSON with bare revision lines is excluded by name
        p = ".ufo/waves/round-52/control/c1-mutation-ladder.json"
        sb.commit({p: '{\n "revision": "' + "a" * 40 + '"\n}\n'}, "ladder")
        sb.commit({p: '{\n "revision": "' + "b" * 40 + '"\n}\n'}, "ladder rewrite")
        return honest(sb)

    scenario("the mutation-ladder JSON is excluded even with bare revision lines", fx_ladder_pretty, True)

    def fx_nonclaim_quiet(sb):  # kills newpaths-noafter: a quiet round-57 non-claim control is not an after-* receipt
        O = ".ufo/waves/round-57/controls/tooling.txt"
        sb.commit({O: f"revision: {'a' * 40}\n"}, "other receipt")
        return honest(sb)

    scenario("a quiet round-57 non-claim control stays out of the claims", fx_nonclaim_quiet, True)

    def fx_renames_off(sb):  # kills walk-M: rename detection is forced even with diff.renames=false
        body = "body body body body\n" * 12
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n" + body}, "r")
        sb.git("config", "diff.renames", "false")
        sb.git("mv", OLD, ".ufo/waves/round-56/controls/moved.txt")
        sb.commit({".ufo/waves/round-56/controls/moved.txt": f"revision: {'b' * 40}\nEXIT=0\n" + body}, "move and relabel")
        return honest(sb)

    scenario("a move plus relabel is seen with diff.renames=false", fx_renames_off, False, {"undisclosed_relabels": 1, "deleted_receipts": 0})

    def fx_base_population(sb):  # kills basepop-45: the shortfall is measured against this counter's own default
        n = int(re.search(r"BASE_POPULATION = (\d+)", open(os.path.abspath(__file__)).read()).group(1))
        globals()["BASE_POPULATION"] = n
        extra = {f".ufo/waves/round-56/controls/r{i}.txt": f"revision: {'0' * 39}{chr(97 + i % 26)}\n" for i in range(42)}
        sb.commit(extra, "42 more base receipts")
        return honest(sb)

    scenario("the base-population shortfall uses the counter's own default", fx_base_population, False, {"deleted_receipts": 1})

    def eq_form(sb):
        sb.commit({OLD: f"revision={'a' * 40}\n"}, "r")
        sb.commit({OLD: f"revision={'b' * 40}\n"}, "relabel (= form)")
        return sb.commit({}, "tip")

    scenario("= form relabel detected", eq_form, False, {"undisclosed_relabels": 1})

    def json_form(sb):
        p = ".ufo/waves/round-56/controls/x.json"
        sb.commit({p: f'{{\n "revision": "{"a" * 40}"\n}}\n'}, "r")
        sb.commit({p: f'{{\n "revision": "{"b" * 40}"\n}}\n'}, "relabel (json)")
        return sb.commit({}, "tip")

    scenario("quoted JSON key relabel detected", json_form, False, {"undisclosed_relabels": 1})

    def keep_same(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\nA\n"}, "r")
        sb.commit({OLD: f"revision: {'a' * 40}\nB edited, same pin\n"}, "edit body only")
        return sb.commit({}, "tip")

    scenario("edit that keeps the pin is not a relabel", keep_same, False, {"undisclosed_relabels": 0})

    def strip_then_new(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.commit({OLD: "stripped\n"}, "strip the line")
        sb.commit({OLD: f"revision: {'b' * 40}\n"}, "new pin after the strip")
        return sb.commit({}, "tip")

    scenario("stripped then re-pinned yields two relabels", strip_then_new, False, {"undisclosed_relabels": 2})

    def delete_readd(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.commit({OLD: None}, "delete")
        sb.commit({OLD: f"revision: {'b' * 40}\n"}, "re-add with another pin")
        return sb.commit({}, "tip")

    scenario("deleted then re-added with another pin is a relabel", delete_readd, False, {"undisclosed_relabels": 1, "deleted_receipts": 0})

    def rename_relabel(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n" + "body body body body\n" * 12}, "r")
        sb.git("mv", OLD, ".ufo/waves/round-56/controls/moved.txt")
        sb.commit({".ufo/waves/round-56/controls/moved.txt": f"revision: {'b' * 40}\nEXIT=0\n" + "body body body body\n" * 12}, "move and relabel")
        return sb.commit({}, "tip")

    scenario("rename plus relabel in one commit is seen under the new path", rename_relabel, False, {"undisclosed_relabels": 1, "deleted_receipts": 0})

    def move_out(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n" + "body body body body\n" * 12}, "r")
        os.makedirs(os.path.join(sb.d, ".ufo/waves/round-56/notes"), exist_ok=True)
        sb.git("mv", OLD, ".ufo/waves/round-56/notes/moved.txt")
        sb.commit({}, "move out of the population")
        return sb.commit({}, "tip")

    scenario("a receipt moved out of the population counts as vanished", move_out, False, {"deleted_receipts": 1})

    def delete_readd_same(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n"}, "r")
        sb.commit({OLD: None}, "delete")
        sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n"}, "re-add byte-identical")
        return sb.commit({}, "tip")

    scenario("deleted and re-added identically leaves no latch", delete_readd_same, False, {"deleted_receipts": 0, "undisclosed_relabels": 0})

    def merged_relabel(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.git("checkout", "-q", "-b", "side")
        sb.commit({OLD: f"revision: {'b' * 40}\n"}, "side relabel")
        sb.git("checkout", "-q", "main")
        sb.commit({"other.txt": "o\n"}, "main work")
        sb.git("merge", "-q", "--no-ff", "-m", "merge side", "side")
        return sb.commit({}, "tip")

    scenario("relabel on a merged side branch is seen at its own commit", merged_relabel, False, {"undisclosed_relabels": 1})

    def new_on_side(sb):
        t = honest(sb)
        sb.git("checkout", "-q", "-b", "sideN")
        sb.commit({NEWP[3]: f"{C3}\n  revision: {'a' * 40}\nEXIT=0\n"}, "side: wrong pin")
        sb.commit({NEWP[3]: f"{C3}\n  revision: {sb.git('rev-parse', 'main~2')}\nEXIT=0\n"}, "side: relabel to look right")
        sb.git("checkout", "-q", "main")
        sb.git("merge", "-q", "--no-ff", "-m", "merge sideN", "sideN")
        return sb.commit({}, "tip")

    scenario("a new receipt relabelled on a merged side branch is seen", new_on_side, False)

    def outside(sb):
        sb.commit({".ufo/waves/round-40/controls/x.txt": f"revision: {'a' * 40}\n"}, "r40")
        sb.commit({".ufo/waves/round-40/controls/x.txt": f"revision: {'b' * 40}\n"}, "r40 relabel")
        return honest(sb)

    scenario("round outside 52-57 is out of population", outside, True)

    def r54(sb):
        R54 = ".ufo/waves/round-54/controls/after-c1.txt"
        sb.commit({R54: f"revision: {'a' * 40}\n"}, "r54 receipt")
        sb.commit({R54: f"revision: {'b' * 40}\n"}, "r54 relabel")
        return honest(sb)

    scenario("round-54 relabel undisclosed", r54, False, {"undisclosed_relabels": 1})

    def nonclaim(sb):
        O = ".ufo/waves/round-57/controls/tooling.txt"
        sb.commit({O: f"revision: {'a' * 40}\n"}, "other receipt")
        sb.commit({O: f"revision: {'b' * 40}\n"}, "relabel other")
        return honest(sb)

    scenario("round-57 non-claim control relabelled", nonclaim, False, {"new_relabelled": 1, "undisclosed_relabels": 0})

    def ladder(sb):
        p = ".ufo/waves/round-52/control/c1-mutation-ladder.json"
        sb.commit({p: '{"old_tail": "  revision: ' + "a" * 40 + '"}\n'}, "ladder")
        sb.commit({p: '{"old_tail": "  revision: ' + "b" * 40 + '"}\n'}, "ladder rewrite")
        return honest(sb)

    scenario("the mutation-ladder JSON is excluded from the population", ladder, True)

    # base anchor: the sandbox has no commit named BASE_REV, so the anchor fails by construction in every scenario above unless the
    # global is set to the sandbox's own first commit; the scenarios set it through scenario(); this one checks the failure itself.
    sb0 = Sandbox()
    try:
        globals()["BASE_POPULATION"] = 1
        tip0 = honest(sb0)
        globals()["BASE_REV"] = "0" * 40
        v0 = measure(sb0.d, tip0)
        results.append((f"history without the base revision is flagged: new_unpinned={v0['new_unpinned']} met={v0['met']}", (not v0["met"]) and any("history replaced" in n for n in v0["notes"])))
    finally:
        sb0.close()

    # CLI exit codes (the selftest cannot reach main() otherwise)
    def cli(name, build, want_exit):
        sb = Sandbox()
        try:
            globals()["BASE_POPULATION"] = 1
            args = ["--root", sb.d]
            tip = build(sb) if build else None
            if tip:
                args += ["--revision", tip]
            p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), *args], capture_output=True, text=True,
                               env={**os.environ, "KAKE_R57_PINS_TEST_BASE": f"{globals()['BASE_REV']}:1"})
            results.append((f"CLI {name}: exit={p.returncode}", p.returncode == want_exit))
        finally:
            sb.close()

    cli("met repo exits 0", lambda sb: honest(sb), 0)
    cli("unmet repo exits 1", lambda sb: honest(sb, old_relabel=True), 1)
    cli("malformed errata exits 2", lambda sb: honest(sb, bad_errata="{not json"), 2)
    cli("usage error exits 64", None, 64)
    sbF = Sandbox()
    try:
        globals()["BASE_POPULATION"] = 1
        pF = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--root", sbF.d, "--no-such-flag"],
                            capture_output=True, text=True,
                            env={**os.environ, "KAKE_R57_PINS_TEST_BASE": f"{globals()['BASE_REV']}:1"})
        results.append((f"CLI unknown flag exits 64: exit={pF.returncode}", pF.returncode == 64))
    finally:
        sbF.close()

    globals()["BASE_REV"], globals()["BASE_POPULATION"] = saved
    ok = sum(1 for _, g in results if g)
    for name, g in results:
        print(("PASS " if g else "FAIL ") + name)
    print(f"c57 receipt-pins selftest: {ok}/{len(results)}")
    return 0 if ok == len(results) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Round-57 C1 counter (receipt revision pins)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", help="tip revision to measure")
    ap.add_argument("--selftest", action="store_true")
    try:
        args = ap.parse_args()
    except SystemExit as e:
        return 0 if e.code == 0 else 64
    if args.selftest:
        return selftest()
    if not args.revision:
        print("usage: --root <lane> --revision <rev> | --selftest", file=sys.stderr)
        return 64
    try:
        v = measure(os.path.abspath(args.root), args.revision)
    except Unevaluable as exc:
        print(f"C1 receipt-pins unevaluable: {exc}")
        return 2
    print(report(v))
    return 0 if v["met"] else 1


if __name__ == "__main__":
    sys.exit(main())
