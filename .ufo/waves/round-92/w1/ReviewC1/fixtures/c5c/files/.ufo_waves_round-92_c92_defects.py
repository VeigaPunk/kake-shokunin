#!/usr/bin/env python3
"""Round-92 C1 counter: the routed round-91 instrument defects K91-1/2/4/5.

Frozen before data (`.ufo/waves/round-92/freeze.md`). Reads committed bytes at
--revision only; every judgement is re-derived, never read from prose.

Items (claim mapping is stated in `freeze.md`):

A (K91-1: a receipt with no execution was admitted). Closed iff, at --revision,
  `.ufo/waves/round-92/integration/mutation-tip.txt` carries the declared first
  line (digest == the gate blob at that revision, N >= 20, K >= 18, S == N-K,
  met=true), `.ufo/waves/round-92/integration/mutation-tip.log` carries exactly
  one line per listed mutant with a distinct `M<nn>` id and a verdict, and the
  committed runner `.ufo/waves/round-92/integration/mutate-tip.py` **executes**
  here: the counter runs it for `base` and for the first listed mutant in a
  scratch clone and requires the unmutated run to survive, the mutant's observed
  verdict to equal the log line, and the two runs to differ — a runner that
  prints canned lines fails the third condition.
B (K91-2: no registry row). Closed iff `SKILL.md` at --revision carries a row that
  names `.ufo/waves/round-92/c92_defects.py`, its `--revision` command and its
  `met` predicate.
C (K91-5: a replay counted checks without asserting their labels). Closed iff the
  committed `.ufo/waves/round-92/controls/run_controls.sh`, replayed by this
  counter on a scratch clone at --revision with `ONLY=c1`, exits 0 and prints
  exactly the nine declared label lines.

Top-level conjuncts (K91-4: membership instead of exact sets):
  - battery: five fixture revisions built here from --revision bytes (never read
    from the repo) must each read an **exact** open set and, for the negative
    fixtures, a declared reason substring;
  - differential: the frozen round-91 counter must accept the canned-runner
    fixture that this counter refuses;
  - self: the counter blob at --revision must equal the digest pinned in
    `.ufo/waves/round-92/frozen/c1-self.sha256`.

met <=> A and B and C closed AND battery exact AND differential ok AND self ok.
Output line 1:
  C1v92 revision=<sha> items=3 open=N closed=M battery=K/5 differential=ok|fail
        self=ok|hit met=true|false
line 2: JSON detail. Exit 0 iff met; 2 on usage/selftest failure; 1 otherwise.
Scratch: --work (required), removed on exit.
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

BASE = "e143faff1b86aad172dd87696da900c70347b8b2"
SELF_PATH = ".ufo/waves/round-92/c92_defects.py"
SELF_PIN = ".ufo/waves/round-92/frozen/c1-self.sha256"
RECEIPT = ".ufo/waves/round-92/integration/mutation-tip.txt"
LOG = ".ufo/waves/round-92/integration/mutation-tip.log"
RUNNER = ".ufo/waves/round-92/integration/mutate-tip.py"
GATE = "scripts/cache_key_conformance.py"
SKILL = "SKILL.md"
SCRIPT = ".ufo/waves/round-92/controls/run_controls.sh"
FROZEN91 = ".ufo/waves/round-91/c91_defects.py"
LABELS = (
    "base-open=2",
    "base-met=false",
    "base-exit=1",
    "carrier-open=0",
    "carrier-met=true",
    "carrier-exit=0",
    "selftest=12/12",
    "noharm=0",
    "self=ok",
)
LABEL_RE = re.compile(r"^(?:base-open|base-met|base-exit|carrier-open|carrier-met|"
                      r"carrier-exit|selftest|noharm|self)=")
RECEIPT_RE = re.compile(
    r"^gate_sha256=([0-9a-f]{64}) mutants=(\d+) killed=(\d+) survivors=(\d+) met=true$")
LOG_RE = re.compile(r"^(M\d{2}) verdict=(killed|survived) rc=(\d+)$")
VERDICT_RE = re.compile(r"^verdict=(killed|survived) rc=(\d+)$")


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True)


def show(root, rev, path):
    p = git(root, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def tracked(root, rev, path):
    return bool(git(root, "ls-tree", "--name-only", rev, "--", path).stdout.strip())


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def clone_at(root, rev, dest):
    shutil.rmtree(dest, ignore_errors=True)
    p = subprocess.run(["git", "clone", "-q", "--shared", root, dest], capture_output=True)
    if p.returncode != 0:
        return False
    top = git(dest, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(dest):
        return False
    # a clone of a detached-HEAD repo carries no local branch; pin master to the
    # root's master so the replay harness resolves the same carrier revision
    master = git(root, "rev-parse", "refs/heads/master").stdout.decode().strip()
    if master:
        git(dest, "update-ref", "refs/heads/master", master)
    return git(dest, "checkout", "-q", "--detach", rev).returncode == 0


def item_a(root, rev, work, detail):
    blob = show(root, rev, RECEIPT)
    if blob is None:
        return False, "mutation receipt absent"
    lines = blob.decode("utf-8", "replace").strip().splitlines()
    m = RECEIPT_RE.match(lines[0].strip()) if lines else None
    if not m:
        return False, "receipt first line not in the declared form"
    digest, n, k, s = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
    if n < 20 or k < 18 or s != n - k:
        return False, "receipt floors not met (mutants=%d killed=%d survivors=%d)" % (n, k, s)
    gate_sha = sha_bytes(show(root, rev, GATE) or b"")
    if digest != gate_sha:
        return False, "receipt digest %s != gate blob %s" % (digest[:12], gate_sha[:12])
    log = show(root, rev, LOG)
    if log is None:
        return False, "execution log absent"
    verdicts = {}
    for line in log.decode("utf-8", "replace").splitlines():
        mm = LOG_RE.match(line.strip())
        if mm:
            verdicts[mm.group(1)] = (mm.group(2), int(mm.group(3)))
    detail["A_log_mutants"] = len(verdicts)
    if len(verdicts) != n:
        return False, "execution log lists %d mutants, receipt claims %d" % (len(verdicts), n)
    killed = sum(1 for v, _ in verdicts.values() if v == "killed")
    if killed != k:
        return False, "execution log kills %d mutants, receipt claims %d" % (killed, k)
    runner = show(root, rev, RUNNER)
    if runner is None:
        return False, "mutation runner absent"
    clone = os.path.join(work, "exec")
    if not clone_at(root, rev, clone):
        return False, "scratch clone for the runner failed"
    runner_path = os.path.join(clone, RUNNER)
    if not os.path.exists(runner_path):
        return False, "runner missing from the scratch clone"
    sampled = sorted(verdicts)[0]
    observed = {}
    for target in ("base", sampled):
        try:
            p = subprocess.run([sys.executable, "-B", runner_path, "--mutant", target],
                               cwd=clone, capture_output=True, timeout=900,
                               env=dict(os.environ, HYAKU_SCRATCH=os.path.join(work, "sc")))
        except subprocess.TimeoutExpired:
            return False, "runner timed out on %s" % target
        out = p.stdout.decode("utf-8", "replace").strip().splitlines()
        last = out[-1] if out else ""
        vm = VERDICT_RE.match(last)
        if not vm:
            return False, "runner printed no verdict line for %s: %r" % (target, last[:80])
        observed[target] = (vm.group(1), int(vm.group(2)))
    detail["A_observed"] = {"base": observed["base"], sampled: observed[sampled]}
    if observed["base"] != ("survived", 0):
        return False, "unmutated run did not survive cleanly: %r" % (observed["base"],)
    if observed["base"] == observed[sampled]:
        return False, "base and mutant runs do not differ (canned output)"
    if observed[sampled] != verdicts[sampled]:
        return False, "sampled mutant %s observed %r, log claims %r" % (
            sampled, observed[sampled], verdicts[sampled])
    return True, ""


def item_b(root, rev, detail):
    blob = show(root, rev, SKILL)
    if blob is None:
        return False, "SKILL.md absent"
    rows = [l for l in blob.decode("utf-8", "replace").splitlines() if "c92_defects.py" in l]
    detail["B_rows"] = len(rows)
    for row in rows:
        if "--revision" in row and "met" in row:
            return True, ""
    return False, "no registry row names c92_defects.py with its --revision command and met predicate"


def item_c(root, rev, work, detail):
    if show(root, rev, SCRIPT) is None:
        return False, "control harness absent"
    clone = os.path.join(work, "replay")
    if not clone_at(root, rev, clone):
        return False, "scratch clone for the replay failed"
    script = os.path.join(clone, SCRIPT)
    env = dict(os.environ, LANE=clone, ONLY="c1",
               HYAKU_SCRATCH=os.path.join(work, "scr"),
               TMPDIR=os.path.join(work, "tmp"))
    os.makedirs(env["TMPDIR"], exist_ok=True)
    try:
        r = subprocess.run(["bash", script], cwd=clone, env=env, capture_output=True,
                           timeout=1800)
    except subprocess.TimeoutExpired:
        return False, "replay timed out"
    out = r.stdout.decode("utf-8", "replace").splitlines()
    got = [l.strip() for l in out if LABEL_RE.match(l.strip())]
    detail["C_labels"] = got[:12]
    if r.returncode != 0:
        return False, "replay exit=%d" % r.returncode
    if sorted(got) != sorted(LABELS):
        missing = [l for l in LABELS if l not in got]
        extra = [l for l in got if l not in LABELS]
        return False, "label set differs (missing=%r extra=%r)" % (missing[:3], extra[:3])
    return True, ""


def build_fixture(root, rev, work, name, kind):
    """A fixture revision cloned from --revision with one artifact broken."""
    fx = os.path.join(work, "fx-" + name)
    if not clone_at(root, rev, fx):
        return None, None
    ident = ["-c", "user.name=fixture", "-c", "user.email=fixture@scratch.invalid"]

    def commit(msg):
        git(fx, *ident, "add", "-A")
        git(fx, *ident, "commit", "-qm", msg)
        return git(fx, "rev-parse", "HEAD").stdout.decode().strip()

    receipt = show(root, rev, RECEIPT)
    log = show(root, rev, LOG)
    runner = show(root, rev, RUNNER)
    script = show(root, rev, SCRIPT)
    if kind == "positive":
        return fx, rev
    if receipt is None:
        return None, None
    if kind == "stale-digest":
        text = receipt.decode().replace(RECEIPT_RE.match(
            receipt.decode().splitlines()[0].strip()).group(1), "0" * 64, 1)
        with open(os.path.join(fx, RECEIPT), "w") as fh:
            fh.write(text)
    elif kind == "canned-runner":
        with open(os.path.join(fx, RUNNER), "w") as fh:
            fh.write("#!/usr/bin/env python3\nimport sys\n"
                     "print('verdict=survived rc=0')\n")
    elif kind == "no-registry-row":
        path = os.path.join(fx, SKILL)
        with open(path) as fh:
            text = fh.read()
        kept = [l for l in text.splitlines() if "c92_defects.py" not in l]
        with open(path, "w") as fh:
            fh.write("\n".join(kept) + "\n")
    elif kind == "wrong-labels":
        with open(os.path.join(fx, SCRIPT), "w") as fh:
            fh.write("#!/usr/bin/env bash\n"
                     "for n in base-open base-met base-exit carrier-open carrier-met "
                     "carrier-exit selftest noharm self; do echo \"$n=WRONG\"; done\nexit 0\n")
        os.chmod(os.path.join(fx, SCRIPT), 0o755)
    else:
        return None, None
    if log is None or runner is None or script is None:
        return None, None
    return fx, commit("fixture " + name)


BATTERY = (
    # (fixture name, kind, exact open set, required reason substring or "")
    ("FA", "stale-digest", {"A"}, "digest"),
    ("FB", "canned-runner", {"A"}, "do not differ"),
    ("FC", "no-registry-row", {"B"}, "registry row"),
    ("FD", "wrong-labels", {"C"}, "label set"),
    ("FE", "positive", set(), ""),
)


def battery(root, rev, work, detail, differential):
    counter = os.path.join(work, "c92_at_rev.py")
    with open(counter, "wb") as fh:
        fh.write(show(root, rev, SELF_PATH) or b"")
    results = {}
    exact = 0
    for name, kind, want, needle in BATTERY:
        fx, fxrev = build_fixture(root, rev, work, name, kind)
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
        opened, reasons = [], {}
        if len(lines) > 1:
            try:
                js = json.loads(lines[1])
                opened = js.get("open_items", [])
                reasons = js.get("reasons", {})
            except ValueError:
                pass
        results[name] = {"head": head, "open": opened, "reasons": reasons}
        if set(opened) != want:
            return False, "fixture %s open set %r != declared %r" % (
                name, sorted(opened), sorted(want))
        if needle:
            text = " ".join(reasons.values())
            if needle not in text:
                return False, "fixture %s reason %r lacks %r" % (name, text[:120], needle)
        if kind == "positive" and p.returncode != 0:
            return False, "positive fixture not met: %s" % head
        exact += 1
    detail["battery"] = results
    # differential: the frozen round-91 counter accepts the canned-runner fixture
    frozen = os.path.join(work, "c91_frozen.py")
    blob = show(root, rev, FROZEN91)
    if blob is None:
        return False, "frozen round-91 counter absent"
    with open(frozen, "wb") as fh:
        fh.write(blob)
    fx, fxrev = build_fixture(root, rev, work, "FB-diff", "canned-runner")
    if fx is None:
        return False, "differential fixture could not be built"
    inner = os.path.join(work, "inner-diff")
    os.makedirs(inner, exist_ok=True)
    try:
        p = subprocess.run([sys.executable, "-B", frozen, "--root", fx, "--revision", fxrev,
                            "--work", inner, "--skip-battery"], capture_output=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return False, "frozen counter timed out on the differential fixture"
    head = (p.stdout.decode("utf-8", "replace").strip().splitlines() or [""])[0]
    differential["c91_on_FB"] = head
    if "met=true" not in head:
        return False, "the frozen round-91 counter already refuses the canned runner: %s" % head
    return True, ""


def selftest():
    """Every check is counted; the denominator is len(checks), never a literal."""
    checks = []

    def case(desc, got, want):
        checks.append((desc, got == want, got, want))

    good = "gate_sha256=%s mutants=21 killed=20 survivors=1 met=true" % ("a" * 64)
    case("receipt good", bool(RECEIPT_RE.match(good)), True)
    case("receipt case-variant key",
         bool(RECEIPT_RE.match(good.replace("gate_sha256", "GATE_SHA256"))), False)
    case("receipt floor mutants",
         bool(RECEIPT_RE.match("gate_sha256=%s mutants=19 killed=18 survivors=1 met=true"
                               % ("a" * 64))), True)
    case("receipt met=false",
         bool(RECEIPT_RE.match(good.replace("met=true", "met=false"))), False)
    case("log line good", bool(LOG_RE.match("M01 verdict=killed rc=1")), True)
    case("log line no rc", bool(LOG_RE.match("M01 verdict=killed")), False)
    case("verdict line good", bool(VERDICT_RE.match("verdict=survived rc=0")), True)
    case("verdict line canned", bool(VERDICT_RE.match("verdict=survived")), False)
    case("label regex matches a label", bool(LABEL_RE.match("carrier-open=0")), True)
    case("label regex ignores prose", bool(LABEL_RE.match("carrier open 0")), False)
    case("declared labels are distinct", len(set(LABELS)), len(LABELS))
    case("label count", len(LABELS), 9)
    bad = [c for c in checks if not c[1]]
    for desc, _, got, want in bad:
        print("selftest FAIL %s: got %r want %r" % (desc, got, want))
    print("selftest %d/%d" % (len(checks) - len(bad), len(checks)))
    return 0 if not bad else 2


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--skip-battery", action="store_true")
    ap.add_argument("--skip-replay", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.root and a.revision and a.work):
        ap.error("--root, --revision and --work are required unless --selftest")
    root = os.path.realpath(a.root)
    rev = git(root, "rev-parse", "%s^{commit}" % a.revision).stdout.decode().strip()
    if not rev:
        print("C1v92 revision=? unresolved")
        return 2
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c92d-", dir=a.work)
    detail = {"open_items": [], "reasons": {}}
    differential = {}
    try:
        self_ok = False
        pin = show(root, rev, SELF_PIN)
        blob = show(root, rev, SELF_PATH)
        if pin is not None and blob is not None:
            self_ok = pin.decode("utf-8", "replace").strip() == sha_bytes(blob)
        detail["self_pin"] = "ok" if self_ok else "hit"
        checks = [("A", lambda: item_a(root, rev, work, detail)),
                  ("B", lambda: item_b(root, rev, detail))]
        if not a.skip_replay:
            checks.append(("C", lambda: item_c(root, rev, work, detail)))
        else:
            detail["C_replay"] = "skipped"
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
        battery_ok, battery_why = True, ""
        if not a.skip_battery:
            try:
                battery_ok, battery_why = battery(root, rev, work, detail, differential)
            except Exception as exc:
                battery_ok, battery_why = False, "battery error: %s" % exc
            if not battery_ok:
                detail["reasons"]["battery"] = battery_why
        else:
            detail["battery"] = "skipped"
        detail["differential"] = differential
        met = (not detail["open_items"]) and battery_ok and self_ok
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("C1v92 revision=%s items=3 open=%d closed=%d battery=%s differential=%s self=%s "
          "met=%s" % (rev, len(detail["open_items"]), closed,
                      "skipped" if a.skip_battery else ("exact" if battery_ok else "hit"),
                      "ok" if battery_ok else "fail",
                      "ok" if self_ok else "hit", str(met).lower()))
    print(json.dumps(detail, sort_keys=True))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
