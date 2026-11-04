#!/usr/bin/env python3
"""Round-91 C1 counter: the routed round-90 instrument defects R90-A/B/C.

Frozen before data (`.ufo/waves/round-91/freeze.md`). Reads committed bytes at
--revision only; every judgement is re-derived, never read from prose.

Items:

A (R90-A, defect-queue shape: the round-90 counter admitted three forgery classes —
   a stale receipted revision, a case-variant token and a receipt with no execution).
   Closed iff, at --revision:
     - this counter is tracked at `.ufo/waves/round-91/c91_defects.py` and its own
       `--selftest` passes from the extracted copy (a junk or empty successor fails);
     - and, unless --skip-battery is given, the self-invoked battery over four fixture
       repositories reports: FA -> item B open, FB -> item B open, FC -> item C open,
       FD -> no item open. The fixtures are built here from --revision bytes; the
       positive fixture is the only one whose readings are all real.
B (R90-B: the tip gate was never re-mutated). Closed iff, at --revision,
   `.ufo/waves/round-91/integration/mutation-tip.txt` exists, its first line is
     `gate_sha256=<64 hex> mutants=<N> killed=<K> survivors=<S> met=true`
   with the digest equal to the blob sha256 of `scripts/cache_key_conformance.py`
   at that revision, N >= 20, K >= 18, S == N - K, and at least N distinct
   `M<nn> ` mutant lines below it.
C (R90-C: `run_controls.sh` no longer replays after the round-90 relocation).
   Closed iff, at --revision, `.ufo/waves/round-90/controls/run_controls.sh`
     - names the relocated file (`.ufo/waves/round-90/inherited/baseclean.out`) on
       every line that mentions `baseclean.out`, and never the bare lane-root copy;
     - takes its lane root from `${LANE:-...}` (so it can be replayed on a scratch
       clone and never writes into the real lane);
     - and, replayed by this counter on a scratch clone checked out at --revision
       with `ONLY=c1`, exits 0 and prints a final line `controls ok K/K` with K >= 9.

met <=> open == 0 over A, B, C. Output line 1:
  C1v91 revision=<sha> items=3 open=N closed=M met=true|false
line 2: JSON detail naming the open items and their reasons. Exit 0 iff met; 2 on
usage/selftest failure; 1 otherwise. Scratch: --work (required), removed on exit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = "5b20af16661040f383e9e84f85b838619857cb14"
SELF_PATH = ".ufo/waves/round-91/c91_defects.py"
SELFTEST_EXPECT = "selftest 6/6"
RECEIPT = ".ufo/waves/round-91/integration/mutation-tip.txt"
GATE = "scripts/cache_key_conformance.py"
SCRIPT = ".ufo/waves/round-90/controls/run_controls.sh"
INHERITED = ".ufo/waves/round-90/inherited/baseclean.out"
STALE_GATE_SHA = "2840f32e53317327fbaa6df3f8e02da06363e0fcda829270651a356192517591"
RECEIPT_RE = re.compile(
    r"^gate_sha256=([0-9a-f]{64}) mutants=(\d+) killed=(\d+) survivors=(\d+) met=true$")
MUTANT_RE = re.compile(r"^M\d{2} ")
SUMMARY_RE = re.compile(r"^controls ok (\d+)/(\d+)$")


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True)


def show(root, rev, path):
    p = git(root, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def tracked(root, rev, path):
    return bool(git(root, "ls-tree", "--name-only", rev, "--", path).stdout.strip())


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def item_a(root, rev, work, skip_battery, detail):
    if not tracked(root, rev, SELF_PATH):
        return False, "successor counter not tracked at the revision"
    blob = show(root, rev, SELF_PATH)
    probe = os.path.join(work, "probe.py")
    with open(probe, "wb") as fh:
        fh.write(blob)
    try:
        st = subprocess.run([sys.executable, "-B", probe, "--selftest"],
                            capture_output=True, timeout=300)
    except subprocess.TimeoutExpired:
        return False, "successor counter selftest timed out"
    st_out = st.stdout.decode("utf-8", "replace").strip()
    if st.returncode != 0 or SELFTEST_EXPECT not in st_out:
        return False, "successor counter selftest: rc=%d %r" % (st.returncode, st_out[:120])
    if skip_battery:
        detail["A_battery"] = "skipped"
        return True, ""
    counter = os.path.join(work, "c91_defects_at_rev.py")
    with open(counter, "wb") as fh:
        fh.write(blob)
    gate_sha = sha_bytes(show(root, rev, GATE) or b"")
    results = {}
    for name, kind in (("FA", "stale-digest"), ("FB", "case-variant"),
                       ("FC", "receipt-no-execution"), ("FD", "positive")):
        fx, fxrev = make_fixture(root, rev, work, name, kind, gate_sha)
        if fx is None:
            return False, "fixture %s could not be built" % name
        inner = os.path.join(work, "inner-" + name)
        os.makedirs(inner, exist_ok=True)
        try:
            p = subprocess.run([sys.executable, "-B", counter, "--root", fx,
                                "--revision", fxrev, "--work", inner, "--skip-battery"],
                               capture_output=True, timeout=1800)
        except subprocess.TimeoutExpired:
            return False, "fixture %s timed out" % name
        lines = p.stdout.decode("utf-8", "replace").strip().splitlines()
        head = lines[0] if lines else ""
        opened = []
        if len(lines) > 1:
            try:
                opened = json.loads(lines[1]).get("open_items", [])
            except ValueError:
                opened = []
        results[name] = {"head": head, "open": opened, "rc": p.returncode}
    detail["A_battery"] = results
    want = {"FA": ["B"], "FB": ["B"], "FC": ["C"], "FD": []}
    for name, items in want.items():
        got = results[name]["open"]
        if name == "FD":
            if got or results[name]["rc"] != 0:
                return False, "positive fixture not met: %s" % results[name]["head"]
        elif not items or items[0] not in got:
            return False, "forgery %s not refused on its item: %s" % (name, results[name]["head"])
    return True, ""


def make_fixture(root, rev, work, name, kind, gate_sha):
    fx = os.path.join(work, "fx-" + name)
    shutil.rmtree(fx, ignore_errors=True)
    p = subprocess.run(["git", "clone", "-q", "--shared", root, fx], capture_output=True)
    if p.returncode != 0:
        return None, None
    top = git(fx, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(fx):
        return None, None
    if git(fx, "checkout", "-q", "--detach", rev).returncode != 0:
        return None, None
    ident = ["-c", "user.name=fixture", "-c", "user.email=fixture@scratch.invalid"]

    def commit(msg):
        git(fx, *ident, "add", "-A")
        git(fx, *ident, "commit", "-qm", msg)
        return git(fx, "rev-parse", "HEAD").stdout.decode().strip()

    # the two real fixes, taken from the measured revision
    script = show(root, rev, SCRIPT)
    inherited = show(root, rev, INHERITED)
    if script is None or inherited is None:
        return None, None
    os.makedirs(os.path.join(fx, os.path.dirname(SCRIPT)), exist_ok=True)
    os.makedirs(os.path.join(fx, os.path.dirname(INHERITED)), exist_ok=True)
    body = script
    if kind == "receipt-no-execution":
        body = b"#!/usr/bin/env bash\nLANE=${LANE:-.}\necho \"controls ok 9/9\"\nexit 3\n"
    with open(os.path.join(fx, SCRIPT), "wb") as fh:
        fh.write(body)
    os.chmod(os.path.join(fx, SCRIPT), 0o755)
    with open(os.path.join(fx, INHERITED), "wb") as fh:
        fh.write(inherited)
    # the mutation receipt
    digest = STALE_GATE_SHA if kind == "stale-digest" else gate_sha
    key = "GATE_SHA256" if kind == "case-variant" else "gate_sha256"
    mutants = "\n".join("M%02d fixture mutant %d" % (i, i) for i in range(1, 22))
    receipt = "%s=%s mutants=21 killed=20 survivors=1 met=true\n%s\n" % (key, digest, mutants)
    os.makedirs(os.path.join(fx, os.path.dirname(RECEIPT)), exist_ok=True)
    with open(os.path.join(fx, RECEIPT), "w") as fh:
        fh.write(receipt)
    return fx, commit("fixture " + name)


def parse_receipt(line):
    """The frozen receipt predicate: form, floor and arithmetic. Returns (digest, N, K) or None."""
    m = RECEIPT_RE.match(line.strip())
    if not m:
        return None
    digest, mutants, killed, survivors = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
    if mutants < 20 or killed < 18:
        return None
    if survivors != mutants - killed:
        return None
    return digest, mutants, killed


def item_b(root, rev, detail):
    blob = show(root, rev, RECEIPT)
    if blob is None:
        return False, "mutation receipt absent"
    text = blob.decode("utf-8", "replace")
    lines = text.strip().splitlines()
    parsed = parse_receipt(lines[0]) if lines else None
    if parsed is None:
        return False, "receipt first line not in the frozen form"
    digest, mutants, killed = parsed
    gate_sha = sha_bytes(show(root, rev, GATE) or b"")
    if digest != gate_sha:
        return False, "receipt digest %s != tip gate blob %s" % (digest[:12], gate_sha[:12])
    ids = {l.split(" ")[0] for l in lines[1:] if MUTANT_RE.match(l)}
    detail["B_mutants_listed"] = len(ids)
    if len(ids) < mutants:
        return False, "only %d distinct mutant lines for mutants=%d" % (len(ids), mutants)
    return True, ""


def item_c(root, rev, work, detail):
    blob = show(root, rev, SCRIPT)
    if blob is None:
        return False, "run_controls.sh absent"
    text = blob.decode("utf-8", "replace")
    forbidden = re.compile(r'"\$LANE"/baseclean\.out|\$\{LANE\}/baseclean\.out|\$LANE/baseclean\.out')
    for i, line in enumerate(text.splitlines(), 1):
        if forbidden.search(line):
            return False, "line %d still copies the lane-root baseclean.out: %s" % (
                i, line.strip()[:80])
    if text.count(INHERITED) < 2:
        return False, "script copies the relocated file fewer than twice"
    if "LANE=${LANE:-" not in text:
        return False, "script does not take its lane root from ${LANE:-...}"
    clone = os.path.join(work, "clone")
    shutil.rmtree(clone, ignore_errors=True)
    p = subprocess.run(["git", "clone", "-q", "--shared", root, clone], capture_output=True)
    if p.returncode != 0:
        return False, "scratch clone failed"
    if git(clone, "checkout", "-q", "--detach", rev).returncode != 0:
        return False, "scratch clone checkout failed"
    script = os.path.join(clone, SCRIPT)
    env = dict(os.environ, LANE=clone, ONLY="c1", HYAKU_SCRATCH=os.path.join(work, "scr"))
    try:
        r = subprocess.run(["bash", script], cwd=clone, env=env, capture_output=True,
                           timeout=1800)
    except subprocess.TimeoutExpired:
        return False, "replay timed out"
    out = r.stdout.decode("utf-8", "replace").strip().splitlines()
    tail = out[-1] if out else ""
    detail["C_tail"] = tail
    if r.returncode != 0:
        return False, "replay exit=%d" % r.returncode
    m = SUMMARY_RE.match(tail)
    if not m:
        return False, "no `controls ok K/K` summary line"
    k, n = int(m.group(1)), int(m.group(2))
    if k != n or n < 9:
        return False, "summary %d/%d does not assert the full c1 battery" % (k, n)
    return True, ""


def selftest():
    bad = []
    good = "gate_sha256=%s mutants=21 killed=20 survivors=1 met=true" % ("a" * 64)
    for line, want in ((good, True),
                       ("GATE_SHA256=%s mutants=21 killed=20 survivors=1 met=true" % ("a" * 64), False),
                       ("gate_sha256=%s mutants=19 killed=18 survivors=1 met=true" % ("a" * 64), False),
                       ("gate_sha256=%s mutants=21 killed=20 survivors=2 met=true" % ("a" * 64), False),
                       ("gate_sha256=%s mutants=21 killed=20 survivors=1 met=false" % ("a" * 64), False),
                       ("gate_sha256=%s mutants=21 killed=17 survivors=4 met=true" % ("a" * 64), False)):
        got = parse_receipt(line) is not None
        if got != want:
            bad.append("receipt parser: %r -> %s" % (line[:40], got))
    if SUMMARY_RE.match("controls ok 9/9") is None:
        bad.append("summary parser misses the declared form")
    if SUMMARY_RE.match("controls ok 9/8") is None:
        bad.append("summary parser misses a partial form")
    for line in bad:
        print("selftest FAIL %s" % line)
    print("selftest %d/%d" % (6 - len(bad), 6))
    return 0 if not bad else 2


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--skip-battery", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.root and a.revision and a.work):
        ap.error("--root, --revision and --work are required unless --selftest")
    root = os.path.realpath(a.root)
    rev = git(root, "rev-parse", "%s^{commit}" % a.revision).stdout.decode().strip()
    if not rev:
        print("C1v91 revision=? unresolved")
        return 2
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c91d-", dir=a.work)
    detail = {"open_items": [], "reasons": {}}
    try:
        checks = (("A", lambda: item_a(root, rev, work, a.skip_battery, detail)),
                  ("B", lambda: item_b(root, rev, detail)),
                  ("C", lambda: item_c(root, rev, work, detail)))
        closed = 0
        for name, fn in checks:
            try:
                ok, why = fn()
            except Exception as exc:  # a broken counter must read open, never crash met
                ok, why = False, "counter error: %s" % exc
            if ok:
                closed += 1
            else:
                detail["open_items"].append(name)
                detail["reasons"][name] = why
    finally:
        shutil.rmtree(work, ignore_errors=True)
    met = not detail["open_items"]
    print("C1v91 revision=%s items=3 open=%d closed=%d met=%s"
          % (rev, len(detail["open_items"]), closed, str(met).lower()))
    print(json.dumps(detail, sort_keys=True))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
