#!/usr/bin/env python3
"""C2 counter — round 69, predicate frozen in .ufo/waves/round-69/contract.md
(and Amendment 1, which fixes the terms used here).

C2 is met iff
  python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root <lane> --revision <rev> --work <scratch dir>
prints ``tmp_literals=0 selftest_under_tmpdir=true offline_unchanged=true`` and exits 0.

Measurements, each on the revision's *committed* bytes (``git show`` for the
source, ``git archive`` for the tree that node runs in):

  tmp_literals          code lines (not ``//`` or ``*`` comment lines) matching
                        the quote-adjacent path literal regex ``['"`]/tmp``.
                        Help text and prose are not path literals and are not
                        counted (Amendment 1). Expected base value: 2.
  selftest_under_tmpdir run ``node scripts/freshness-sweep.mjs --selftest``
                        with TMPDIR and HOME set to two distinct fresh empty
                        dirs and KAKE_SELFTEST_DIR unset. True iff
                        ``kake-r16/selftest`` appears under TMPDIR, does not
                        appear under HOME, and is not a symlink (lstat).
  offline_unchanged     the ``--offline`` exit code AND its VERDICT line at
                        <revision> equal those of the base revision on this
                        host. The base ``--offline`` run is red on this host
                        (lowercase ``~/projects`` citations, unannotated and
                        unpinned) — host-bound debt routed to L0, not C2's to
                        cure — so the gate is read for *no regression*, never
                        for a green exit.

Exit: 0 iff tmp_literals == 0 and selftest_under_tmpdir and offline_unchanged.

Known residual, named and not claimed closed: with TMPDIR unset the default
selftest dir falls back to ``os.tmpdir()`` (POSIX ``/tmp``) — documented Node
behaviour (S436/S437), not a literal in the source.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

SCRIPT_REL = "scripts/freshness-sweep.mjs"
# Frozen base of round 69 (contract header); the offline comparison is taken
# against it unless --baseline says otherwise.
BASE_REVISION = "4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4"
TMP_LITERAL_RE = re.compile(r"['\"`]/tmp")
FIXTURE_REL = ("kake-r16", "selftest")


def run(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)


def count_tmp_literals(source):
    """Quote-adjacent /tmp path literals on code (non-comment) lines."""
    hits = []
    for no, line in enumerate(source.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("*"):
            continue
        if TMP_LITERAL_RE.search(line):
            hits.append((no, stripped[:78]))
    return hits


def materialise(root, revision, checkout):
    """Write the revision's committed tree into <checkout> (no worktree read)."""
    tar_path = checkout + ".tar"
    os.makedirs(checkout, exist_ok=True)
    with open(tar_path, "wb") as fh:
        proc = subprocess.run(
            ["git", "-C", root, "archive", "--format=tar", revision],
            stdout=fh, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        os.unlink(tar_path)
        raise SystemExit(
            f"git archive {revision} failed: "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}")
    with tarfile.open(tar_path) as tar:
        tar.extractall(checkout, filter="data")
    os.unlink(tar_path)
    return checkout


def verdict_line(stdout):
    for line in stdout.splitlines():
        if line.startswith("VERDICT:"):
            return line.strip()
    return None


def fixture_placement(tmp_root, home_root):
    """Where the selftest fixture landed: (under_tmp, under_home, symlink).

    ``under_tmp`` requires the fixture directory itself to exist under TMPDIR
    and NOT be a symlink (lstat), so a fixture redirected to HOME through a
    link cannot pass as "under TMPDIR".
    """
    fixture_tmp = os.path.join(tmp_root, *FIXTURE_REL)
    fixture_home = os.path.join(home_root, *FIXTURE_REL)
    under_tmp = os.path.lexists(fixture_tmp)
    symlink = under_tmp and os.path.islink(fixture_tmp)
    under_home = os.path.lexists(fixture_home)
    return under_tmp, under_home, symlink


def measure_offline(node, checkout):
    proc = run([node, SCRIPT_REL, "--offline"], cwd=checkout)
    return proc.returncode, verdict_line(proc.stdout)


def main():
    ap = argparse.ArgumentParser(description="round-69 C2 counter")
    ap.add_argument("--root", required=True, help="lane repository (git)")
    ap.add_argument("--revision", required=True, help="commit to measure")
    ap.add_argument("--work", required=True, help="scratch dir for checkout + fixtures")
    ap.add_argument("--baseline", default=BASE_REVISION,
                    help="revision the offline gate is compared against "
                         "(default: the round-69 frozen base)")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="c69-", dir=work)
    try:
        # ── tmp_literals (committed blob) ────────────────────────────────────
        source = run(["git", "-C", root, "show", f"{args.revision}:{SCRIPT_REL}"])
        if source.returncode != 0:
            raise SystemExit(
                f"git show {args.revision}:{SCRIPT_REL} failed: {source.stderr.strip()}")
        literals = count_tmp_literals(source.stdout)

        node = shutil.which("node")
        if not node:
            raise SystemExit("node not found on PATH")

        checkout = materialise(root, args.revision, os.path.join(scratch, "tree"))
        if not os.path.isfile(os.path.join(checkout, SCRIPT_REL)):
            raise SystemExit(f"{SCRIPT_REL} absent at {args.revision}")

        # ── selftest_under_tmpdir ────────────────────────────────────────────
        st_tmp = os.path.join(scratch, "tmp-root")
        st_home = os.path.join(scratch, "home-root")
        os.makedirs(st_tmp)
        os.makedirs(st_home)
        env = {k: v for k, v in os.environ.items()
               if k not in ("KAKE_SELFTEST_DIR", "KAKE_IN_SELFTEST")}
        env.update({"TMPDIR": st_tmp, "TMP": st_tmp, "TEMP": st_tmp, "HOME": st_home})
        st = run([node, os.path.join(checkout, SCRIPT_REL), "--selftest"],
                 cwd=checkout, env=env)
        under_tmp, under_home, symlink = fixture_placement(st_tmp, st_home)
        selftest_under_tmpdir = under_tmp and not symlink and not under_home
        st_summary = next((l.strip() for l in st.stdout.splitlines()
                           if l.startswith("selftest: ")), "")

        # ── offline_unchanged (same host, same ambient env) ──────────────────
        rev_code, rev_verdict = measure_offline(node, checkout)
        base_checkout = materialise(root, args.baseline,
                                    os.path.join(scratch, "baseline-tree"))
        base_code, base_verdict = measure_offline(node, base_checkout)
        offline_unchanged = rev_code == base_code and rev_verdict == base_verdict

        print(f"tmp_literals={len(literals)} "
              f"selftest_under_tmpdir={'true' if selftest_under_tmpdir else 'false'} "
              f"offline_unchanged={'true' if offline_unchanged else 'false'}")
        print(f"# revision {args.revision} · {SCRIPT_REL}")
        print(f"# tmp literal code lines (quote-adjacent, non-comment): "
              f"{[n for n, _ in literals] or 'none'}")
        for no, text in literals:
            print(f"#   {no}: {text}")
        print(f"# selftest exit {st.returncode} · {st_summary or 'no summary line'} · "
              f"fixture under TMPDIR={under_tmp} under HOME={under_home} "
              f"symlink={symlink}")
        print(f"# offline exit {rev_code} vs base {args.baseline[:8]} exit {base_code}"
              f" — unchanged={offline_unchanged}")
        print(f"#   rev  VERDICT: {rev_verdict or '(no VERDICT line)'}")
        print(f"#   base VERDICT: {base_verdict or '(no VERDICT line)'}")

        met = not literals and selftest_under_tmpdir and offline_unchanged
        return 0 if met else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
