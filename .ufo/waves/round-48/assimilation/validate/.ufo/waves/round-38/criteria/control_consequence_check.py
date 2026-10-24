#!/usr/bin/env python3
"""Control-consequence check for a round's verification receipts.

QUALITY (j): make the lane's withdrawal rule executable. The lane's rule (SCORECARD,
round-38 declaration) is: "A control that meets the predicate means this counter or
target is wrong ... no reclassification of the control is an option." Until now that
rule had no check; a seat had to notice by reading receipts (round-37 closure, routed
defect 3). This script reads a round's verification directory, groups every receipt by
the counter that produced it (``counterSha256``), marks a counter *tainted* when a
control receipt under it records ``met: true``, and reports a *violation* for every
non-control receipt (a claim measurement) that also records ``met: true`` under a
tainted counter -- i.e. a claim was measured on a counter a known shortcut already met.

Receipt-naming convention this check relies on
----------------------------------------------
* A receipt is a ``*.json`` file whose parsed value is a JSON object carrying a
  non-empty string ``counterSha256`` (the sha256 of the sealed counter file that scored
  it) and, normally, ``met`` (boolean; ``null`` is allowed and means "not evaluated").
  Other keys seen in the fleet (``claim``, ``predicate``, ``revision``, ``toolFile``,
  ``toolPresent``, ``toolSha256``, ``cases``, ``passed``, ``target``, ``perCase``) are
  not read here.
* Control receipts are the files a control seat writes, recognised by the rule the
  lane declared:
      - canonical: basename starts with ``control-`` or ``control_``, wherever the
        file sits (e.g. ``control-CtlC1Shortcut-followup.json``);
      - directory rule: the file sits under a path component named exactly
        ``controls`` or ``pre`` and its basename is a control name, i.e. starts with
        ``control``, ``ctl`` or ``critic``, optionally preceded by a round tag
        ``rNN-`` (e.g. ``pre/CtlC1Shortcut-followup-robots_audit.json``).
  A receipt outside ``controls``/``pre`` whose basename carries a control-seat prefix
  but does not start with ``control-`` (``v3/CtlBaseWrapper-care.json``,
  ``v3/CriticPredicate-rulepatch.json``) is **not** a control for the verdict: round-38
  C2's declaration records the full-rule tools under those names as builds, not
  controls. Such receipts are printed under ``note`` when they record ``met: true`` so
  the reader can see the counter was also met by control-named tools, and they never
  change the exit code.
* Everything else that is a receipt is a non-control receipt: claim measurements
  (``c1-at-<rev>.json``, ``c2-at-<rev>.json``, ``c2-evidence-*``), reference runs
  (``reference.json``, ``pre/reference.json``, ``independent-selftest-reference.json``),
  ablations (``ablations/*.json``) and mutation survivors (``mutref/M*.json``).
* Files that are not receipts (no ``counterSha256``, or JSON that is not an object) are
  listed as skipped and do not affect the exit code -- unless the file name says it is
  a receipt (control prefix or ``c<N>-``/``claim-`` claim prefix), in which case an
  unparsable or counter-less file is a malformed input and the run exits 2. Selftest
  transcripts beside the receipts (``*.exit``, ``robots-selftest-*``) therefore never
  change a verdict.

Exit codes
----------
  0  no tainted counter, or every tainted counter has no non-control receipt with
     ``met: true`` (a compliant verification directory);
  1  at least one violation: a non-control receipt with ``met: true`` under a counter
     whose control receipt(s) also record ``met: true``; the list is printed;
  2  the input cannot be read or evaluated: missing/unreadable directory, git listing
     or blob failure, a named receipt that is not JSON / not an object / has no
     ``counterSha256``, a receipt whose ``met`` is not a boolean or null, a control
     receipt without a boolean ``met``, or a directory with no receipts at all.

Usage
-----
  control_consequence_check.py --verification DIR [--root ROOT]
  control_consequence_check.py --root LANE --revision REV --verification DIR
  control_consequence_check.py --selftest

With ``--revision`` the directory is read from git at that revision (``DIR`` is
repo-relative, or absolute under ``--root``); every git call is read-only and runs with
``GIT_*`` environment variables stripped. The script writes nothing.

Read-only by construction: it opens files for reading, calls ``git ls-tree`` and
``git cat-file`` only, and never touches the working tree or an index.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROG = "control_consequence_check"
CONTROL_CANONICAL = re.compile(r"^control[-_]", re.IGNORECASE)
CONTROL_SEAT = re.compile(r"^(?:r\d+-)?(?:control|ctl|critic)", re.IGNORECASE)
CONTROL_DIR_NAMES = {"controls", "pre"}
CONTROL_OR_CLAIM = re.compile(r"^(?:control[-_]|(?:r\d+-)?(?:ctl|critic)|c\d+[-_]|claim[-_])",
                              re.IGNORECASE)
# Claim measurements: c<N>-... or claim-... receipts. Only these can violate (j); a reference,
# ablation or mutant receipt meeting a tainted counter is printed but is not a claim measured
# on that counter (round-38 L1 narrowing; round 38's withdrawn C1 left reference and mutant
# receipts at met=true on its tainted v2 counter with no claim measurement).
CLAIM_NAME = re.compile(r"^(?:c\d+[-_]|claim[-_])", re.IGNORECASE)


class InputError(Exception):
    """Input that cannot be read or evaluated (exit 2)."""


class Receipt:
    __slots__ = ("rel", "counter", "met", "passed", "cases", "target", "control",
                 "control_seat")

    def __init__(self, rel, counter, met, passed, cases, target, control, control_seat):
        self.rel = rel
        self.counter = counter
        self.met = met
        self.passed = passed
        self.cases = cases
        self.target = target
        self.control = control
        self.control_seat = control_seat

    def tally(self):
        if isinstance(self.passed, int) and isinstance(self.cases, int):
            return "passed %d/%d" % (self.passed, self.cases)
        if self.target is not None:
            return "target %r" % (self.target,)
        return "no tally"


def basename(rel):
    return rel.replace("\\", "/").rsplit("/", 1)[-1]


def is_control(rel):
    """Return (is_control, carries_control_seat_name) for one receipt path."""
    name = basename(rel)
    seat = bool(CONTROL_SEAT.match(name))
    if CONTROL_CANONICAL.match(name):
        return True, True
    parents = rel.replace("\\", "/").split("/")[:-1]
    if any(p.lower() in CONTROL_DIR_NAMES for p in parents):
        return seat, seat
    return False, seat


def parse_receipt(rel, raw):
    """Return (Receipt|None, skip_reason_or_None). Raise InputError when named."""
    named = bool(CONTROL_OR_CLAIM.match(basename(rel)))
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        if named:
            raise InputError("%s: receipt name, but not readable JSON (%s)" % (rel, exc))
        return None, "not JSON"
    if not isinstance(doc, dict):
        if named:
            raise InputError("%s: receipt name, but not a JSON object" % rel)
        return None, "not a JSON object"
    counter = doc.get("counterSha256")
    if not isinstance(counter, str) or not counter.strip():
        if named:
            raise InputError("%s: receipt name, but no counterSha256" % rel)
        return None, "no counterSha256"
    counter = counter.strip()
    met = doc.get("met")
    if met is not None and not isinstance(met, bool):
        raise InputError("%s: met is %s, not a boolean or null" % (rel, type(met).__name__))
    control, control_seat = is_control(rel)
    if control and not isinstance(met, bool):
        raise InputError("%s: control receipt without a boolean met; cannot evaluate" % rel)
    return Receipt(rel, counter, met, doc.get("passed"), doc.get("cases"),
                   doc.get("target"), control, control_seat), None


def read_tree(verification):
    """Yield (repo-relative-or-display rel, bytes) for every *.json below a directory."""
    root = Path(verification)
    if not root.exists():
        raise InputError("verification directory not found: %s" % verification)
    if not root.is_dir():
        raise InputError("verification path is not a directory: %s" % verification)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.endswith(".json"):
                continue
            path = Path(dirpath) / name
            rel = str(path.relative_to(root)).replace(os.sep, "/")
            try:
                raw = path.read_bytes()
            except OSError as exc:
                raise InputError("%s: cannot be read (%s)" % (rel, exc))
            yield rel, raw


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    try:
        return subprocess.run(["git", "-C", root, *args], capture_output=True,
                              env=env, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InputError("git %s failed: %s" % (args[0], exc))


def read_git(root, revision, verification):
    if revision.startswith("-"):
        raise InputError("revision may not start with '-': %s" % revision)
    rootp = Path(root)
    ver = Path(verification)
    if ver.is_absolute():
        try:
            ver = ver.resolve().relative_to(rootp.resolve())
        except ValueError:
            raise InputError("verification path is outside --root: %s" % verification)
    rel = str(ver).replace(os.sep, "/").rstrip("/")
    rev = git(root, "rev-parse", "--verify", "--quiet", "--end-of-options",
              revision + "^{commit}")
    if rev.returncode != 0:
        raise InputError("revision not found: %s" % revision)
    commit = rev.stdout.decode().strip()
    listing = git(root, "ls-tree", "-r", "-z", "--name-only", commit, "--", rel + "/")
    if listing.returncode != 0:
        raise InputError("verification path not in %s: %s" % (commit, rel))
    paths = [p for p in listing.stdout.decode("utf-8", "replace").split("\0")
             if p.endswith(".json")]
    for path in sorted(paths):
        blob = git(root, "cat-file", "blob", "%s:%s" % (commit, path))
        if blob.returncode != 0:
            raise InputError("cannot read %s at %s" % (path, commit))
        yield path[len(rel) + 1:] if path.startswith(rel + "/") else path, blob.stdout


def load(verification, root, revision):
    if revision:
        return list(read_git(root, revision, verification))
    return list(read_tree(verification))


def analyse(entries):
    receipts = []
    skipped = []
    for rel, raw in entries:
        receipt, reason = parse_receipt(rel, raw)
        if receipt is None:
            skipped.append((rel, reason))
        else:
            receipts.append(receipt)
    return receipts, skipped


def report(receipts, skipped, label, stream=sys.stdout):
    by_counter = {}
    for r in receipts:
        by_counter.setdefault(r.counter, []).append(r)
    tainted = {}
    for counter, group in by_counter.items():
        controls = [r for r in group if r.control and r.met is True]
        if controls:
            tainted[counter] = sorted(controls, key=lambda r: r.rel)
    violations = []
    for counter in sorted(tainted):
        for r in by_counter[counter]:
            if not r.control and r.met is True and CLAIM_NAME.match(basename(r.rel)):
                violations.append(r)
    violations.sort(key=lambda r: (r.counter, r.rel))

    out = stream.write
    out("%s\n" % PROG)
    out("verification: %s\n" % label)
    out("receipts: %d  controls: %d  non-control: %d  skipped: %d  counters: %d\n" % (
        len(receipts), sum(1 for r in receipts if r.control),
        sum(1 for r in receipts if not r.control), len(skipped), len(by_counter)))
    for rel, reason in skipped:
        out("skipped (not a receipt): %s (%s)\n" % (rel, reason))
    for counter in sorted(by_counter):
        group = by_counter[counter]
        out("\ncounter %s  receipts=%d%s\n" % (
            counter, len(group),
            "  TAINTED by %d control(s)" % len(tainted[counter]) if counter in tainted else ""))
        for r in tainted.get(counter, ()):
            out("  taint: %s  met=true  %s\n" % (r.rel, r.tally()))
        notes = [r for r in group if r.control_seat and not r.control and r.met is True]
        for r in sorted(notes, key=lambda r: r.rel):
            out("  note: %s  met=true  %s  (control-seat name outside controls/ and "
                "pre/, and not a control- prefixed file: not a control for this "
                "verdict)\n" % (r.rel, r.tally()))
        if counter in tainted:
            own = [r for r in group if not r.control and r.met is True]
            for r in sorted(own, key=lambda r: r.rel):
                kind = "VIOLATION" if CLAIM_NAME.match(basename(r.rel)) else "met (not a claim receipt)"
                out("  %s: %s  met=true  %s\n" % (kind, r.rel, r.tally()))
            if not own:
                out("  no non-control receipt has met=true\n")
        unknown = [r for r in group if r.met is None]
        if unknown:
            out("  met not evaluated: %s\n" % ", ".join(sorted(r.rel for r in unknown)))
    if violations:
        out("\nRESULT: FAIL exit=1  tainted_counters=%d  violations=%d\n" % (
            len(tainted), len(violations)))
        return 1
    out("\nRESULT: PASS exit=0  tainted_counters=%d  violations=0\n" % len(tainted))
    return 0


def run(verification, root):
    path = Path(verification)
    if not path.is_absolute() and root and root != ".":
        path = Path(root) / path
    verification = str(path)
    entries = load(verification, root, None)
    if not entries:
        raise InputError("no *.json receipts under: %s" % verification)
    receipts, skipped = analyse(entries)
    if not receipts:
        raise InputError("no receipts carry counterSha256 under: %s" % verification)
    return report(receipts, skipped, str(verification))


def selftest(tmp):
    """Construct red, green and unreadable directories; assert the exit codes."""
    cases = []

    def build(name, files):
        d = Path(tmp) / name
        d.mkdir()
        for fname, content in files.items():
            path = d / fname
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return str(d)

    def receipt(counter, met, passed=0, cases_=20):
        return json.dumps({"counterSha256": counter, "met": met, "passed": passed,
                           "cases": cases_, "target": 19}, sort_keys=True)

    good = build("good", {
        "control-shortcut.json": receipt("a" * 64, False, 7),
        "c1-at-deadbeef.json": receipt("a" * 64, True, 20),
        "reference.json": receipt("b" * 64, True, 20),
        "notes.txt": "ignored: not a receipt\n",
    })
    bad = build("bad", {
        "control-shortcut.json": receipt("c" * 64, True, 20),
        "c1-at-deadbeef.json": receipt("c" * 64, True, 20),
        "unrelated.json": receipt("d" * 64, True, 20),
    })
    seat_named = build("seat_named", {
        "v3/CtlWrapper.json": receipt("a" * 64, True, 20),
        "c1-at-deadbeef.json": receipt("a" * 64, True, 20),
    })
    pre_control = build("pre_control", {
        "pre/CtlShortcut.json": receipt("c" * 64, True, 20),
        "c1-at-deadbeef.json": receipt("c" * 64, True, 20),
    })
    malformed = build("malformed", {
        "control-shortcut.json": "{\"counterSha256\": \"e",
    })
    control_no_met = build("control_no_met", {
        "control-shortcut.json": json.dumps({"counterSha256": "f" * 64}),
        "c1-at-deadbeef.json": receipt("f" * 64, True, 20),
    })
    empty = build("empty", {"readme.txt": "no receipts here\n"})

    def run_dir(verification, capture=None):
        receipts, skipped = analyse(load(verification, None, None))
        stream = io.StringIO() if capture is not None else open(os.devnull, "w")
        try:
            got = report(receipts, skipped, verification, stream=stream)
        finally:
            if capture is None:
                stream.close()
        if capture is not None:
            capture.append(stream.getvalue())
        return got, receipts

    def expect(name, verification, wanted):
        got, receipts = run_dir(verification)
        cases.append((name, got == wanted, got, wanted))
        return receipts

    expect("compliant directory -> 0", good, 0)
    expect("tainted counter -> 1", bad, 1)
    receipts = expect("violation list", bad, 1)
    hits = [r.rel for r in receipts
            if not r.control and r.met is True and r.counter == "c" * 64]
    cases.append(("violation list names the claim receipt",
                  hits == ["c1-at-deadbeef.json"], hits, ["c1-at-deadbeef.json"]))
    expect("control-seat name outside controls/pre -> 0", seat_named, 0)
    captured = []
    run_dir(seat_named, captured)
    cases.append(("seat-named receipt noted, not tainting",
                  "note: v3/CtlWrapper.json" in captured[0]
                  and "TAINTED" not in captured[0],
                  "note printed" if "note: v3/CtlWrapper.json" in captured[0] else "no note",
                  "note printed"))
    expect("control-seat name under pre/ -> 1", pre_control, 1)
    for name, verification in (("malformed control -> 2", malformed),
                               ("control without met -> 2", control_no_met),
                               ("no receipts -> 2", empty)):
        try:
            receipts, skipped = analyse(load(verification, None, None))
            if not receipts:
                raise InputError("no receipts")
            stream = open(os.devnull, "w")
            try:
                got = report(receipts, skipped, verification, stream=stream)
                got = 1 if got else 0  # a directory that parses must not reach 0 here
            finally:
                stream.close()
            cases.append((name, False, got, 2))
        except InputError:
            cases.append((name, True, 2, 2))
    failed = [c for c in cases if not c[1]]
    for name, ok, got, wanted in cases:
        print("%s %-42s exit=%s (wanted %s)" % ("ok  " if ok else "FAIL", name, got, wanted))
    print("selftest: %d/%d ok" % (len(cases) - len(failed), len(cases)))
    return 0 if not failed else 2


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog=PROG,
        description="Fail when a claim measurement met its predicate on a counter a "
                    "control receipt already met (the lane's withdrawal rule, made "
                    "executable).")
    ap.add_argument("--verification", metavar="DIR",
                    help="round verification directory (filesystem path, or repo-relative "
                         "with --revision)")
    ap.add_argument("--root", default=".", metavar="ROOT", help="lane root (default .)")
    ap.add_argument("--revision", metavar="REV",
                    help="read the verification directory from git at REV (read-only)")
    ap.add_argument("--selftest", action="store_true",
                    help="build red, green and unreadable directories in a tempdir and "
                         "check the exit codes")
    a = ap.parse_args(argv)
    if a.selftest:
        tmp = tempfile.mkdtemp(prefix="control_consequence_check.")
        try:
            return selftest(tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    if not a.verification:
        ap.error("--verification DIR is required (or --selftest)")
    try:
        if a.revision:
            entries = load(a.verification, a.root, a.revision)
            label = "%s @ %s" % (a.verification, a.revision)
            if not entries:
                raise InputError("no *.json receipts under: %s" % a.verification)
            receipts, skipped = analyse(entries)
            if not receipts:
                raise InputError("no receipts carry counterSha256 under: %s" % a.verification)
            return report(receipts, skipped, label)
        return run(a.verification, a.root)
    except InputError as exc:
        print("%s: %s" % (PROG, exc), file=sys.stderr)
        return 2
    except Exception as exc:  # never a traceback; one line, exit 2
        print("%s: internal error: %s" % (PROG, exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
