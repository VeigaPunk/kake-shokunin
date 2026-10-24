#!/usr/bin/env python3
"""Regression test for corpus knowledge paths that Git quoting mangles.

The citing-set gate enumerates ``corpus/knowledge`` files.  In ``--revision``
mode it reads that list from ``git ls-tree``; the historical text framing
(``ls-tree -r`` with newline records and a TAB split) cannot represent a
path containing a TAB or a NEWLINE, and it mangles non-ASCII paths under
``core.quotePath``.  This test builds an isolated Git repository whose
knowledge files are named with a plain name, a space, a TAB, a NEWLINE and
a non-ASCII name, and asserts that the gate reports exactly the same five
``(row, file)`` identities in working-tree mode and in ``--revision`` mode,
both with an empty ledger (red: five unadjudicated pairs) and with the
exact ledger written (green: no findings).

This is a consumer test: it drives the real gate binary through a
subprocess and asserts stable finding ids, exit codes and identities.  The
expected values are derived from the fixture this file constructs, never
captured from gate output.

Usage:

    python3 -B .ufo/waves/round-27/git_name_selftest.py \
        [--gate <path-to-citing_set.py>] [--tmpdir <dir>] [--keep] [--json]

Exit codes: 0 all cases passed, 1 a case failed, 2 could-not-evaluate
(gate absent, temporary directory unusable, repository setup failed),
64 usage.  The repository is created under /fast/scratch/hyaku/kake-r27/ with
an isolated Git configuration and an empty hooks directory; no live
repository is written, no network access is used, and the temporary tree is
removed afterwards unless --keep or a case failed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

EXIT_CLEAN = 0
EXIT_FAILED = 1
EXIT_CANNOT_EVALUATE = 2
EXIT_USAGE = 64

SCHEMA = "kake-citing-set-git-name-selftest-v1"
BASE_TMP = "/fast/scratch/hyaku/kake-r27"
ROW = "S001"
CORPUS_PREFIX = "corpus/knowledge/"
FILE_NAMES = (
    "alpha.md",
    "with space.md",
    "with\ttab.md",
    "with\nnewline.md",
    "naïve-Ω.md",
)
EXPECTED_IDENTITIES = frozenset((ROW, CORPUS_PREFIX + name) for name in FILE_NAMES)
FINDING_ID = "unadjudicated_citing_pair"


class SetupError(Exception):
    """The isolated repository could not be built."""


class Results:
    def __init__(self):
        self.cases = []

    def check(self, name, condition, detail=""):
        passed = bool(condition)
        self.cases.append({"name": name, "passed": passed, "detail": detail})
        return passed

    @property
    def failed(self):
        return [case for case in self.cases if not case["passed"]]


def isolated_env(home):
    """Git environment with no user/system configuration and no live hooks."""
    env = dict(os.environ)
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        env.pop(name, None)
    env.update(
        {
            "HOME": home,
            "XDG_CONFIG_HOME": os.path.join(home, "xdg"),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.path.join(home, "absent-gitconfig"),
            "GIT_ATTR_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_ASKPASS": "/bin/true",
            "GIT_AUTHOR_NAME": "kake git-name selftest",
            "GIT_AUTHOR_EMAIL": "git-name-selftest@example.invalid",
            "GIT_COMMITTER_NAME": "kake git-name selftest",
            "GIT_COMMITTER_EMAIL": "git-name-selftest@example.invalid",
            "GIT_AUTHOR_DATE": "2026-10-21T00:00:00+00:00",
            "GIT_COMMITTER_DATE": "2026-10-21T00:00:00+00:00",
        }
    )
    return env


def git(arguments, cwd, env):
    done = subprocess.run(
        ["git"] + list(arguments),
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if done.returncode != 0:
        detail = done.stderr.decode("utf-8", "replace").strip().splitlines()
        raise SetupError("git %s failed: %s" % (" ".join(arguments[:2]), detail[-1] if detail else done.returncode))
    return done


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def population_document():
    return {"round": 27, "rows": [{"id": ROW}]}


def ledger_document(pairs):
    return {"round": 27, "pairs": list(pairs)}


def build_repository(repo, env, results):
    """Create the isolated repository with the five awkwardly named files."""
    knowledge = os.path.join(repo, CORPUS_PREFIX.replace("/", os.sep))
    try:
        os.makedirs(knowledge)
    except OSError as exc:
        raise SetupError("cannot create corpus directory: %s" % exc)
    for name in FILE_NAMES:
        write_text(os.path.join(knowledge, name), "source: %s\n\ncites %s only.\n" % (ROW, ROW))
    write_text(os.path.join(repo, "population.json"), json.dumps(population_document(), indent=2) + "\n")
    write_text(os.path.join(repo, "ledger.json"), json.dumps(ledger_document([]), indent=2) + "\n")

    hooks = os.path.join(os.path.dirname(repo), "hooks")
    os.makedirs(hooks, exist_ok=True)
    git(["-c", "init.defaultBranch=main", "init", "--quiet"], repo, env)
    git(["config", "core.hooksPath", hooks], repo, env)
    git(["config", "commit.gpgsign", "false"], repo, env)
    git(["config", "core.quotePath", "true"], repo, env)
    git(["add", "-A"], repo, env)
    git(["commit", "--quiet", "-m", "git-name selftest base"], repo, env)
    revision = git(["rev-parse", "HEAD"], repo, env).stdout.decode("ascii", "replace").strip()
    results.check("repository-built", bool(revision), "commit %s" % revision[:12])
    return revision


def populate_ledger(repo, env):
    """Write the exact ledger for the five identities and commit it."""
    pairs = [{"row": ROW, "file": CORPUS_PREFIX + name} for name in FILE_NAMES]
    write_text(os.path.join(repo, "ledger.json"), json.dumps(ledger_document(pairs), indent=2) + "\n")
    git(["add", "-A"], repo, env)
    git(["commit", "--quiet", "-m", "git-name selftest exact ledger"], repo, env)
    return git(["rev-parse", "HEAD"], repo, env).stdout.decode("ascii", "replace").strip()


def run_gate(gate, repo, env, revision=None):
    command = [
        sys.executable,
        "-B",
        gate,
        "--root",
        repo,
        "--population",
        "population.json",
        "--ledger",
        "ledger.json",
        "--json",
    ]
    if revision is not None:
        command += ["--revision", revision]
    done = subprocess.run(command, cwd=repo, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = done.stdout.decode("utf-8", "replace")
    stderr = done.stderr.decode("utf-8", "replace")
    try:
        payload = json.loads(stdout)
    except ValueError:
        payload = None
    return {
        "exit": done.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "payload": payload,
    }


def identities(payload):
    return frozenset(
        (finding.get("row"), finding.get("file"))
        for finding in (payload or {}).get("findings", [])
        if isinstance(finding, dict) and finding.get("id") == FINDING_ID
    )


def finding_ids(payload):
    return tuple(
        finding.get("id")
        for finding in (payload or {}).get("findings", [])
        if isinstance(finding, dict)
    )


def assert_red(results, label, run):
    payload = run["payload"]
    results.check(
        label + "-json",
        isinstance(payload, dict) and all(key in payload for key in ("verdict", "citingPairs", "ledgerPairs", "findings")),
        "stdout=%s stderr=%s" % (run["stdout"][:200], run["stderr"][:200]),
    )
    results.check(label + "-exit", run["exit"] == EXIT_FAILED, "exit=%s" % run["exit"])
    if not isinstance(payload, dict):
        return None
    results.check(label + "-verdict", payload.get("verdict") == "failed", "verdict=%s" % payload.get("verdict"))
    results.check(label + "-ids", set(finding_ids(payload)) == {FINDING_ID}, "ids=%s" % (finding_ids(payload),))
    results.check(
        label + "-finding-count",
        len(payload.get("findings", [])) == len(FILE_NAMES),
        "findings=%s" % (len(payload.get("findings", [])),),
    )
    results.check(
        label + "-identity",
        identities(payload) == EXPECTED_IDENTITIES,
        "identities=%s" % sorted(str(item) for item in identities(payload)),
    )
    results.check(label + "-citing-pairs", payload.get("citingPairs") == len(FILE_NAMES), "citingPairs=%s" % payload.get("citingPairs"))
    results.check(label + "-ledger-pairs", payload.get("ledgerPairs") == 0, "ledgerPairs=%s" % payload.get("ledgerPairs"))
    return identities(payload)


def assert_green(results, label, run):
    payload = run["payload"]
    results.check(
        label + "-json",
        isinstance(payload, dict) and all(key in payload for key in ("verdict", "citingPairs", "ledgerPairs", "findings")),
        "stdout=%s stderr=%s" % (run["stdout"][:200], run["stderr"][:200]),
    )
    results.check(label + "-exit", run["exit"] == EXIT_CLEAN, "exit=%s" % run["exit"])
    if not isinstance(payload, dict):
        return
    results.check(label + "-verdict", payload.get("verdict") == "clean", "verdict=%s" % payload.get("verdict"))
    results.check(label + "-no-findings", payload.get("findings") == [], "findings=%s" % (payload.get("findings"),))
    results.check(label + "-citing-pairs", payload.get("citingPairs") == len(FILE_NAMES), "citingPairs=%s" % payload.get("citingPairs"))
    results.check(label + "-ledger-pairs", payload.get("ledgerPairs") == len(FILE_NAMES), "ledgerPairs=%s" % payload.get("ledgerPairs"))


def sha256_of(path):
    digest = hashlib.sha256()
    try:
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
    except OSError:
        return None
    return digest.hexdigest()


class UsageParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("git_name_selftest.py: " + message + "\n")
        raise SystemExit(EXIT_USAGE)


def build_parser():
    parser = UsageParser(prog="git_name_selftest.py", description=__doc__.splitlines()[0])
    parser.add_argument("--gate", help="path of the citing-set gate under test")
    parser.add_argument("--tmpdir", help="directory that receives the isolated repository")
    parser.add_argument("--keep", action="store_true", help="keep the temporary repository")
    parser.add_argument("--json", action="store_true", help="emit JSON (always on)")
    return parser


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    arguments = parser.parse_args(argv)
    default_gate = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
        "scripts",
        "citing_set.py",
    )
    gate = os.path.abspath(arguments.gate or default_gate)
    if not os.path.isfile(gate):
        summary = {
            "schema": SCHEMA,
            "verdict": "could-not-evaluate",
            "passed": False,
            "cases": 0,
            "failed": 0,
            "gate": gate,
            "detail": "gate_absent",
        }
        sys.stdout.write(json.dumps(summary, indent=2) + "\n")
        return EXIT_CANNOT_EVALUATE

    base = os.path.abspath(arguments.tmpdir or BASE_TMP)
    try:
        os.makedirs(base, exist_ok=True)
    except OSError as exc:
        summary = {
            "schema": SCHEMA,
            "verdict": "could-not-evaluate",
            "passed": False,
            "cases": 0,
            "failed": 0,
            "gate": gate,
            "detail": "tmpdir_unusable: %s" % exc,
        }
        sys.stdout.write(json.dumps(summary, indent=2) + "\n")
        return EXIT_CANNOT_EVALUATE

    results = Results()
    workdir = tempfile.mkdtemp(prefix="git-name-selftest-", dir=base)
    repo = os.path.join(workdir, "repo")
    env = isolated_env(workdir)
    detail = None
    try:
        os.makedirs(repo)
        revision = build_repository(repo, env, results)
        tree_run = run_gate(gate, repo, env)
        blob_run = run_gate(gate, repo, env, revision=revision)
        tree_ids = assert_red(results, "working-tree-empty-ledger", tree_run)
        blob_ids = assert_red(results, "revision-empty-ledger", blob_run)
        if tree_ids is not None and blob_ids is not None:
            results.check(
                "modes-agree-empty-ledger",
                tree_ids == blob_ids,
                "tree=%s blob=%s" % (sorted(str(item) for item in tree_ids), sorted(str(item) for item in blob_ids)),
            )

        second = populate_ledger(repo, env)
        tree_run = run_gate(gate, repo, env)
        blob_run = run_gate(gate, repo, env, revision=second)
        assert_green(results, "working-tree-exact-ledger", tree_run)
        assert_green(results, "revision-exact-ledger", blob_run)
    except SetupError as exc:
        detail = str(exc)
    except OSError as exc:
        detail = "os_error: %s" % exc
    finally:
        keep = arguments.keep or bool(results.failed) or detail is not None
        if keep:
            sys.stderr.write("git_name_selftest.py: temporary repository kept at %s\n" % workdir)
        else:
            shutil.rmtree(workdir, ignore_errors=True)

    failed = results.failed
    summary = {
        "schema": SCHEMA,
        "verdict": "clean" if not failed and detail is None else ("could-not-evaluate" if detail is not None else "failed"),
        "passed": not failed and detail is None,
        "cases": len(results.cases),
        "failed": len(failed),
        "gate": gate,
        "gateSha256": sha256_of(gate),
        "expectedIdentities": sorted([list(item) for item in EXPECTED_IDENTITIES]),
        "detail": detail,
        "results": results.cases,
    }
    sys.stdout.write(json.dumps(summary, indent=2) + "\n")
    if detail is not None:
        return EXIT_CANNOT_EVALUATE
    return EXIT_FAILED if failed else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
