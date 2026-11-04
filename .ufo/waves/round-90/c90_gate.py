#!/usr/bin/env python3
"""Round-90 C2 counter: does the lane hold a cache-key conformance gate that refuses
the committed non-conforming population and admits the conforming one?

Frozen before data (`.ufo/waves/round-90/freeze.md`). At --revision the counter
extracts (git archive) the gate `scripts/cache_key_conformance.py` and a frozen
subject population whose blobs are pinned by sha256 below:

  positives (4): the shipped round-89 candidate as of the base revision, the L1
     reference candidate, and the two MutKey mutants M33/M36 that round 89 found
     equivalent;
  negatives (57): the 15 ExecControls adversarial stubs, the 5 round-89 shortcut
     controls, the 35 MutKey mutants other than M33/M36 (M37 included: '%' is a
     tchar, so its absent-name escape is observable), and the 2 frozen round-90
     sandbox negatives (oracle import via sys.path; exec of the counter source).

Each subject is copied beside its original under a random name with an appended
nonce comment (so a gate keyed on file names or file hashes cannot recognise it)
and scored by `python3 -B <gate> --candidate <copy> --seed <S> --work <scratch>`.
A subject is admitted iff the gate exits 0 and its last line ends `met=true`;
refused iff it exits 1 and its last line ends `met=false`; anything else is an error.

anti_table: the gate source must not contain any subject sha256 (first 12 hex) or
any subject file stem.

met <=> gate present AND population pins match AND positives admitted 4/4 AND
negatives refused 57/57 (false_admits == 0, errors == 0) AND anti_table ok.

Line 1: C2v90 revision=<sha> gate=present|absent positives=a/4 negatives_refused=b/57
        false_admits=c errors=d anti_table=ok|hit population=ok|drift seed=S met=true|false
Line 2: JSON details. Exit 0 iff met.
"""

import argparse
import concurrent.futures as cf
import hashlib
import io
import json
import os
import random
import shutil
import subprocess
import sys
import tarfile
import tempfile

GATE = "scripts/cache_key_conformance.py"
BASE = "209027f49959e2e2f0e16867a90a7bb38bbcd3f4"
W = ".ufo/waves/round-89/"
POSITIVES = ["scripts/cache_key.py@BASE", W + "w1/L1/cache_key.py",
             W + "w1/MutKey/mutants/M33-header-name-casefold.py",
             W + "w1/MutKey/mutants/M36-duplicate-member-deduped.py"]
NEGATIVES = (
    [W + "w1/ExecControls/adv-%s.py" % n for n in (
        "absent-empty", "bad-json", "cr-only", "lower-values", "member-ows", "missing-headers", "no-dup-vary",
        "no-name-escape", "no-sort", "no-uri-escape", "raw-sort", "sort-no-escape", "space-trim", "uri-only",
        "wildcard-ok")]
    + [W + "controls/ctl-%s.py" % n for n in ("constant-key", "naive-join", "oracle-import", "repr-key", "table")]
    + [W + "w1/MutKey/mutants/" + n for n in (
        "M01-member-name-not-lowered.py", "M02-header-stored-as-presented.py", "M03-member-order-unsorted.py",
        "M04-member-order-reversed.py", "M05-member-ows-not-trimmed.py", "M06-member-trim-wider-than-ows.py",
        "M07-value-ows-not-trimmed.py", "M08-value-trim-wider-than-ows.py", "M09-value-case-lowered.py",
        "M10-value-case-uppered.py", "M11-escape-percent-dropped.py", "M12-escape-GS-dropped.py",
        "M13-escape-FS-dropped.py", "M14-escape-RS-dropped.py", "M15-escape-US-dropped.py",
        "M16-escape-percent-last.py", "M17-absent-emits-empty.py", "M18-present-empty-emits-absent.py",
        "M19-wildcard-not-refused.py", "M20-wildcard-anywhere-refused.py", "M21-duplicate-member-not-refused.py",
        "M22-duplicate-header-not-refused.py", "M23-crlf-check-dropped.py", "M24-lf-check-dropped.py",
        "M25-header-token-check-dropped.py", "M26-vary-token-check-dropped.py", "M27-empty-vary-falls-through.py",
        "M28-layout-us-always.py", "M29-layout-comma-join.py", "M30-layout-rs-dropped.py",
        "M31-uri-not-escaped.py", "M32-value-internal-whitespace-collapsed.py", "M34-refusal-exits-zero.py",
        "M35-stdout-bare-key.py", "M37-absent-name-not-escaped.py")]
    + [".ufo/waves/round-90/frozen/neg-oracle-path-import.py", ".ufo/waves/round-90/frozen/neg-exec-source.py"]
)
PINS_FILE = ".ufo/waves/round-90/frozen/c2-population.sha256"


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True)


def extract(root, rev, paths, dest):
    p = git(root, "archive", "--format=tar", rev, "--", *paths)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode(errors="replace"))
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
        tf.extractall(dest, filter="data")


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def subject_paths():
    return [p.replace("@BASE", "") for p in POSITIVES] + NEGATIVES


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args(argv)
    root = os.path.realpath(a.root)
    rev = git(root, "rev-parse", "%s^{commit}" % a.revision).stdout.decode().strip()
    if not rev:
        print("C2v90 revision=? unresolved")
        return 2
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c90g-", dir=a.work)
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1, 2 ** 31)
    detail = {}
    if git(root, "cat-file", "-e", "%s:%s" % (rev, GATE)).returncode != 0:
        shutil.rmtree(work, ignore_errors=True)
        print("C2v90 revision=%s gate=absent positives=0/%d negatives_refused=0/%d false_admits=0 errors=0 "
              "anti_table=n/a population=n/a seed=%d met=false" % (rev, len(POSITIVES), len(NEGATIVES), seed))
        print(json.dumps(detail, sort_keys=True))
        return 1
    try:
        tree = os.path.join(work, "tree")
        os.mkdir(tree)
        # population: base candidate from BASE, everything else from --revision
        extract(root, rev, [p for p in subject_paths() if p != "scripts/cache_key.py"]
                + [".ufo/waves/round-89/c89_key.py", PINS_FILE], tree)
        basecand = git(root, "show", "%s:scripts/cache_key.py" % BASE).stdout
        bdir = os.path.join(tree, "base-candidate")
        os.mkdir(bdir)
        with open(os.path.join(bdir, "cache_key.py"), "wb") as fh:
            fh.write(basecand)
        located = {}
        for p in subject_paths():
            located[p] = os.path.join(bdir, "cache_key.py") if p == "scripts/cache_key.py" else os.path.join(tree, p)
        pins = {}
        with open(os.path.join(tree, PINS_FILE)) as fh:
            for line in fh:
                h, _, p = line.strip().partition("  ")
                pins[p] = h
        drift = [p for p in subject_paths() if pins.get(p) != sha(located[p])]
        detail["population_drift"] = drift
        gdir = os.path.join(work, "gate")
        os.mkdir(gdir)
        extract(root, rev, [GATE], gdir)
        gate = os.path.join(gdir, GATE)
        gsrc = open(gate, "rb").read().decode("utf-8", "replace")
        hits = []
        for p in subject_paths():
            stem = os.path.splitext(os.path.basename(p))[0]
            if sha(located[p])[:12] in gsrc:
                hits.append("sha:" + p)
            if stem != "cache_key" and stem in gsrc:
                hits.append("stem:" + p)
        detail["anti_table_hits"] = hits
        rng = random.SystemRandom()

        def score(p):
            src = located[p]
            nonce = "%016x" % rng.getrandbits(64)
            copy = os.path.join(os.path.dirname(src), "s_%s.py" % nonce)
            with open(src, "rb") as fh:
                data = fh.read()
            with open(copy, "wb") as fh:
                fh.write(data + b"\n# nonce " + nonce.encode() + b"\n")
            gw = os.path.join(work, "gw-" + nonce)
            os.mkdir(gw)
            try:
                r = subprocess.run([sys.executable, "-B", gate, "--candidate", copy, "--seed", str(seed),
                                    "--work", gw], capture_output=True, timeout=1800, cwd=gw)
            except subprocess.TimeoutExpired:
                return p, "error", "timeout"
            last = (r.stdout.decode("utf-8", "replace").strip().splitlines() or [""])[-1]
            if r.returncode == 0 and last.endswith("met=true"):
                return p, "admit", last
            if r.returncode == 1 and last.endswith("met=false"):
                return p, "refuse", last
            return p, "error", "rc=%d %s" % (r.returncode, last[:200])

        with cf.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            results = list(ex.map(score, subject_paths()))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    res = {p: (v, line) for p, v, line in results}
    pos = [p.replace("@BASE", "") for p in POSITIVES]
    pos_ok = sum(1 for p in pos if res[p][0] == "admit")
    neg_ok = sum(1 for p in NEGATIVES if res[p][0] == "refuse")
    false_admits = [p for p in NEGATIVES if res[p][0] == "admit"]
    errors = [p for p in subject_paths() if res[p][0] == "error"]
    detail.update({"false_admits": false_admits, "errors": {p: res[p][1] for p in errors},
                   "positives_not_admitted": {p: res[p][1] for p in pos if res[p][0] != "admit"},
                   "lines": {p: res[p][1] for p in subject_paths()}})
    met = (not drift and not hits and pos_ok == len(pos) and neg_ok == len(NEGATIVES))
    print("C2v90 revision=%s gate=present positives=%d/%d negatives_refused=%d/%d false_admits=%d errors=%d "
          "anti_table=%s population=%s seed=%d met=%s" % (
              rev, pos_ok, len(pos), neg_ok, len(NEGATIVES), len(false_admits), len(errors),
              "hit" if hits else "ok", "drift" if drift else "ok", seed, str(met).lower()))
    print(json.dumps(detail, sort_keys=True))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
