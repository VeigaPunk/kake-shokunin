#!/usr/bin/env python3
"""Round-57 C1 counter — calibration: stated revision pins against the revision pins the receipts carry.

Version 1 (frozen before any seat scored).

Surface: the measurement receipts under `.ufo/waves/round-5[2-7]/{control,controls}/` that carry a `revision:` or
`revision=` line (the revision a counter was run against). A report or SCORECARD says "measured at <rev>"; the receipt
says what the counter was actually run over. A later commit that rewrites the receipt's revision line (a *relabel*)
makes the stated pin and the run diverge (round-56 routed defect 1, `corpus/lessons/round-56-verifier-spotcheck.md` §6.1).
History cannot be rewritten, so a historical relabel is closed by disclosure: `receipt-errata.json` names it with the
true values and the counter checks every entry against git. A relabel of a receipt this round introduces is never
disclosable: it must not occur.

Definitions (all derived from `git` over the first-parent history of the tip, never the working tree):
  receipt      a path in the population above whose any committed version carries a 40-hex revision line.
  version      the blob of the path at each commit that touched it (oldest first).
  relabel      two consecutive versions whose revision sets are both non-empty and differ, or whose later version carries
               none; recorded as (path, from, to, commit) with the full 40-hex values and the later commit.
  disclosed    an entry of `.ufo/waves/round-57/receipt-errata.json` equal to a relabel on all four fields.
  new receipt  `.ufo/waves/round-57/controls/after-c<N>-*.txt`.
  pinned       the new receipt's one revision equals `.ufo/waves/round-57/measured.json` `revision`, and that revision is a
               strict ancestor of the commit that introduced the receipt.

Counted values:
  undisclosed_relabels  relabels in rounds 52-56 receipts with no matching errata entry.
  phantom_errata        errata entries that match no relabel (a disclosure of something git does not show).
  deleted_receipts      population paths deleted by any commit in the history (a vanished receipt cannot be checked).
  new_relabelled        relabels of any round-57 receipt.
  new_unpinned          new receipts that are not pinned, or carry zero or several revision values.
  new_receipts          distinct claim numbers N among the new receipts that are present (needs 1, 2 and 3).
  scorecard_pin         the tip SCORECARD.md section `## Round 57` names the measured revision (first 12 hex digits).

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
WAVE = ".ufo/waves/round-57"
ERRATA = f"{WAVE}/receipt-errata.json"
MEASURED = f"{WAVE}/measured.json"
NEW_RE = re.compile(r"^\.ufo/waves/round-57/controls/after-c([0-9]+)-[^/]+\.txt$")
POP_RE = re.compile(r"^\.ufo/waves/round-5[2-7]/(control|controls)/[^/]+\.(txt|json)$")
REV_RE = re.compile(r"(?m)^\s*revision\s*[:=]\s*([0-9a-f]{40})\b")
HEX40 = re.compile(r"[0-9a-f]{40}")


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


def measure(root: str, tip: str) -> dict:
    tip = git(root, "rev-parse", "--verify", f"{tip}^{{commit}}").strip()
    ls = git(root, "ls-tree", "-r", "--name-only", tip).split("\n")
    present = {p for p in ls if POP_RE.match(p)}
    log = git(root, "log", "--first-parent", "--name-status", "--no-renames", "--format=@@%H", tip)
    touched: dict[str, list[str]] = {}
    deleted: set[str] = set()
    commit = ""
    for line in log.split("\n"):
        if line.startswith("@@"):
            commit = line[2:]
        elif "\t" in line:
            status, path = line.split("\t", 1)
            if POP_RE.match(path):
                touched.setdefault(path, []).append(commit)
                if status.startswith("D"):
                    deleted.add(path)
    relabels: list[tuple[str, str, str, str]] = []
    new_present: dict[str, str] = {}
    new_relabelled = 0
    for path, commits in sorted(touched.items()):
        prev: set[str] = set()
        for c in reversed(commits):  # oldest first
            text = blob(root, c, path)
            if text is None:  # deleted at this commit
                prev = set()
                continue
            cur = set(REV_RE.findall(text))
            if prev and cur != prev:
                for a in sorted(prev):
                    for b in sorted(cur) or [""]:
                        if a != b:
                            relabels.append((path, a, b, c))
            prev = cur
    deleted_receipts = len([p for p in deleted if any(REV_RE.search(blob(root, c, p) or "") for c in touched[p])])
    old = [r for r in relabels if not NEW_RE.match(r[0]) and not r[0].startswith(f"{WAVE}/")]
    new_rel = [r for r in relabels if r[0].startswith(f"{WAVE}/")]
    new_relabelled = len(new_rel)
    errata_text = blob(root, tip, ERRATA)
    entries: set[tuple[str, str, str, str]] = set()
    if errata_text:
        try:
            for e in json.loads(errata_text).get("entries", []):
                entries.add((e["path"], e["from"], e["to"], e["commit"]))
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            raise Unevaluable(f"{ERRATA} unparsable: {exc}")
    undisclosed = sorted(set(old) - entries)
    phantom = sorted(entries - set(old))
    measured_text = blob(root, tip, MEASURED)
    measured_rev = None
    if measured_text:
        try:
            measured_rev = json.loads(measured_text).get("revision")
        except ValueError:
            measured_rev = None
    new_unpinned = 0
    new_nums: set[str] = set()
    notes: list[str] = []
    for path in sorted(p for p in present if NEW_RE.match(p)):
        num = NEW_RE.match(path).group(1)
        text = blob(root, tip, path) or ""
        revs = set(REV_RE.findall(text))
        intro = git(root, "log", "--first-parent", "--diff-filter=A", "--format=%H", tip, "--", path).strip().split("\n")[-1]
        ok = (len(revs) == 1 and measured_rev is not None and HEX40.fullmatch(str(measured_rev)) is not None
              and next(iter(revs)) == measured_rev and bool(intro) and measured_rev != intro
              and is_ancestor(root, measured_rev, intro))
        if ok:
            new_nums.add(num)
        else:
            new_unpinned += 1
            notes.append(f"{path}: revisions={sorted(revs)} measured={measured_rev} introduced={intro[:12]}")
    sc = blob(root, tip, "SCORECARD.md") or ""
    section = ""
    m = re.search(r"(?ms)^## Round 57\b.*?(?=^## |\Z)", sc)
    if m:
        section = m.group(0)
    scorecard_pin = int(bool(measured_rev) and isinstance(measured_rev, str) and len(measured_rev) >= 12 and measured_rev[:12] in section)
    new_receipts = len(new_nums & {"1", "2", "3"}) if len(new_nums) == 3 else len(new_nums)
    return {"tip": tip, "population": len(present), "relabels_old": len(old), "undisclosed_relabels": len(undisclosed),
            "phantom_errata": len(phantom), "deleted_receipts": deleted_receipts, "new_relabelled": new_relabelled,
            "new_unpinned": new_unpinned, "new_receipts": new_receipts, "scorecard_pin": scorecard_pin,
            "undisclosed": undisclosed, "phantom": phantom, "notes": notes}


def met(v: dict) -> bool:
    return (v["undisclosed_relabels"] == 0 and v["phantom_errata"] == 0 and v["deleted_receipts"] == 0
            and v["new_relabelled"] == 0 and v["new_unpinned"] == 0 and v["new_receipts"] == 3 and v["scorecard_pin"] == 1)


def report(v: dict) -> str:
    keys = ("undisclosed_relabels", "phantom_errata", "deleted_receipts", "new_relabelled", "new_unpinned", "new_receipts", "scorecard_pin")
    out = [f"C1 receipt-pins " + " ".join(f"{k}={v[k]}" for k in keys) + f" met={met(v)}  ({PREDICATE})",
           f"  population={v['population']} relabels_in_history={v['relabels_old']}"]
    for r in v["undisclosed"]:
        out.append(f"  UNDISCLOSED {r[0]} {r[1][:12]} -> {r[2][:12]} at {r[3][:12]}")
    for r in v["phantom"]:
        out.append(f"  PHANTOM {r[0]} {r[1][:12]} -> {r[2][:12]} at {r[3][:12]}")
    for n in v["notes"]:
        out.append(f"  UNPINNED {n}")
    out.append(f"  revision: {v['tip']}")
    return "\n".join(out)


# --------------------------------------------------------------------------- selftest
_ID = ["-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false"]


class Sandbox:
    def __init__(self):
        self.d = tempfile.mkdtemp(prefix="c57-pins-")
        subprocess.run(["git", "-C", self.d, "init", "-q"], check=True)
        top = subprocess.run(["git", "-C", self.d, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(self.d), "sandbox is not its own toplevel"

    def commit(self, files: dict[str, str | None], msg: str = "c") -> str:
        for p, t in files.items():
            full = os.path.join(self.d, p)
            if t is None:
                os.remove(full)
            else:
                os.makedirs(os.path.dirname(full), exist_ok=True)
                open(full, "w").write(t)
        subprocess.run(["git", "-C", self.d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.d, *_ID, "commit", "-q", "--allow-empty", "-m", msg], check=True)
        return subprocess.run(["git", "-C", self.d, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    def close(self):
        shutil.rmtree(self.d, ignore_errors=True)


def _json(o) -> str:
    return json.dumps(o, indent=1)


def selftest() -> int:
    OLD = ".ufo/waves/round-56/controls/after-c1.txt"
    NEWP = {n: f".ufo/waves/round-57/controls/after-c{n}-x.txt" for n in (1, 2, 3)}
    results: list[tuple[str, bool]] = []

    def scenario(name: str, build, want_met: bool | None, want: dict | None = None):
        sb = Sandbox()
        try:
            tip = build(sb)
            try:
                v = measure(sb.d, tip)
                ok = met(v) == want_met and all(v.get(k) == x for k, x in (want or {}).items())
                detail = f"met={met(v)} " + " ".join(f"{k}={v[k]}" for k in ("undisclosed_relabels", "phantom_errata", "deleted_receipts",
                                                                       "new_relabelled", "new_unpinned", "new_receipts", "scorecard_pin"))
            except Unevaluable as exc:
                ok, detail = want_met is None, f"unevaluable {exc}"
            results.append((f"{name}: {detail}", ok))
        finally:
            sb.close()

    def honest(sb: Sandbox, old_relabel: bool = False, errata=None, rewrite_new: bool = False, deleted_old: bool = False,
               skip_new: int | None = None, new_rev: str | None = None, measured: str | None = None, scorecard_pin: bool = True,
               side_measured: bool = False, bad_errata_json: bool = False, extra_line_dup: bool = False):
        r1 = sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n", "SCORECARD.md": "# s\n"}, "old receipt")
        if old_relabel:
            sb.commit({OLD: f"revision: {'b' * 40}\nEXIT=0\n"}, "relabel")
        if deleted_old:
            sb.commit({OLD: None}, "delete")
        base = sb.commit({f"{WAVE}/x": "x\n"}, "round 57 work")
        files: dict[str, str | None] = {}
        mrev = measured or base
        if side_measured:
            subprocess.run(["git", "-C", sb.d, "checkout", "-q", "-b", "side"], check=True)
            mrev = sb.commit({"side.txt": "s\n"}, "side")
            subprocess.run(["git", "-C", sb.d, "checkout", "-q", "-"], check=True)
        files[MEASURED] = _json({"revision": mrev})
        if errata is not None:
            files[ERRATA] = errata(r1, sb)
        if bad_errata_json:
            files[ERRATA] = "{not json"
        sc = f"# s\n## Round 57 — measured\nmeasured at {mrev}\n" if scorecard_pin else "# s\n## Round 57 — measured\nnothing\n"
        files["SCORECARD.md"] = sc
        pre = sb.commit(files, "pins")
        nr = {}
        for n in (1, 2, 3):
            if skip_new == n:
                continue
            rev = new_rev or mrev
            nr[NEWP[n]] = f"C{n} met=True\n  revision: {rev}\n" + (f"  revision: {'c' * 40}\n" if extra_line_dup else "") + "EXIT=0\n"
        tip = sb.commit(nr, "receipts")
        if rewrite_new:
            tip = sb.commit({NEWP[1]: f"C1 met=True\n  revision: {pre}\nEXIT=0\n"}, "relabel new")
        return tip

    def err(r1, sb):
        h = subprocess.run(["git", "-C", sb.d, "log", "--format=%H", "-1", "--", OLD], capture_output=True, text=True).stdout.strip()
        return _json({"entries": [{"path": OLD, "from": "a" * 40, "to": "b" * 40, "commit": h}]})

    scenario("honest, no relabel", lambda sb: honest(sb), True)
    scenario("old relabel undisclosed", lambda sb: honest(sb, old_relabel=True), False, {"undisclosed_relabels": 1})
    scenario("old relabel disclosed with matching errata", lambda sb: honest(sb, old_relabel=True, errata=err), True)
    scenario("errata names nothing git shows", lambda sb: honest(sb, errata=err), False, {"phantom_errata": 1})
    scenario("errata wrong 'to'", lambda sb: honest(sb, old_relabel=True, errata=lambda r, s: err(r, s).replace("b" * 40, "d" * 40)), False)
    scenario("errata wrong commit", lambda sb: honest(sb, old_relabel=True, errata=lambda r, s: err(r, s).replace(r, "e" * 40) if False else _json({"entries": [{"path": OLD, "from": "a" * 40, "to": "b" * 40, "commit": "f" * 40}]})), False)
    scenario("receipt deleted", lambda sb: honest(sb, deleted_old=True), False, {"deleted_receipts": 1})
    scenario("new receipt relabelled", lambda sb: honest(sb, rewrite_new=True), False, {"new_relabelled": 1})
    scenario("new receipt missing claim 3", lambda sb: honest(sb, skip_new=3), False, {"new_receipts": 2})
    scenario("new receipt wrong revision", lambda sb: honest(sb, new_rev="9" * 40), False, {"new_unpinned": 3})
    scenario("measured revision is not an ancestor of the receipts", lambda sb: honest(sb, side_measured=True), False, {"new_unpinned": 3})
    scenario("new receipt with two revision lines", lambda sb: honest(sb, extra_line_dup=True), False, {"new_unpinned": 3})
    scenario("measured.json names another commit", lambda sb: honest(sb, measured="8" * 40), False)
    scenario("SCORECARD omits the pin", lambda sb: honest(sb, scorecard_pin=False), False, {"scorecard_pin": 0})
    scenario("errata unparsable", lambda sb: honest(sb, bad_errata_json=True), None)

    def eq_form(sb):
        sb.commit({OLD: f"revision={'a' * 40}\n"}, "r")
        sb.commit({OLD: f"revision={'b' * 40}\n"}, "relabel (= form)")
        return sb.commit({}, "tip")

    scenario("= form relabel detected", eq_form, False, {"undisclosed_relabels": 1})

    def keep_same(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\nA\n"}, "r")
        sb.commit({OLD: f"revision: {'a' * 40}\nB edited, same pin\n"}, "edit body only")
        return sb.commit({}, "tip")

    scenario("edit that keeps the pin is not a relabel", keep_same, False, {"undisclosed_relabels": 0})

    def no_rev_after(sb):
        sb.commit({OLD: f"revision: {'a' * 40}\n"}, "r")
        sb.commit({OLD: "stripped\n"}, "strip the line")
        return sb.commit({}, "tip")

    scenario("pin line stripped later counts as relabel", no_rev_after, False, {"undisclosed_relabels": 1})

    def outside(sb):
        sb.commit({".ufo/waves/round-40/controls/x.txt": f"revision: {'a' * 40}\n"}, "r40")
        sb.commit({".ufo/waves/round-40/controls/x.txt": f"revision: {'b' * 40}\n"}, "r40 relabel")
        return honest(sb)

    scenario("round outside 52-57 is out of population", outside, True)

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
    except SystemExit:
        return 64
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
    return 0 if met(v) else 1


if __name__ == "__main__":
    sys.exit(main())
