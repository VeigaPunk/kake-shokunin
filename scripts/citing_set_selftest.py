#!/usr/bin/env python3
"""Fixture runner for the citing-set gate (round-27, C2 operability).

Contract under test (``.ufo/waves/round-27/contract.json``):

    gate     python3 -B scripts/citing_set.py --root <dir> [--revision <commit>]
             --population <relative-json> --ledger <relative-json> [--json]
    fixtures scripts/fixtures/citing-set/<case>/{corpus/knowledge/*,population.json,
             ledger.json,expected.json}

Expectation format (``expected.json``)
--------------------------------------
The ``findings`` list is in one of two forms, never mixed within one case:

  * legacy: one string per finding, the finding id only::

        {"exit": 1, "findings": ["citation_range_invalid"]}

  * object: one object per finding::

        {"exit": 2, "findings": [{"id": "input_invalid", "reason": "corpus_empty"}]}

In the object form a finding may omit ``reason`` or carry ``"reason": null``;
an observed finding without a reason compares as ``None``.  The runner compares
the sorted multiset of ``(id, reason)`` pairs exactly; in the legacy form it
compares the sorted multiset of ids only.  The exit code is compared exactly in
both forms.  A case whose entries mix strings and objects is a malformed
oracle and fails the run instead of being skipped.

Per-case setup (``case.json``, optional)
----------------------------------------
A fixture case may carry a ``case.json`` that describes how the case tree is
built at run time.  When present, the case directory is copied into
``<tmpdir>/citing-set-selftest/cases/<case>/`` first and every step runs on
that copy; the committed fixture is never mutated, and Git-hostile artifacts
(a FIFO, an empty directory, a disposable repository) are created in the copy:

    {
      "description": "one human-readable line",
      "root": "sub",
      "argv": ["--revision", "HEAD"],
      "setup": [
        {"op": "fifo", "path": "population.json"},
        {"op": "mkdir", "path": "corpus/knowledge"},
        {"op": "git_init"},
        {"op": "git_commit", "message": "fixture"}
      ]
    }

``root`` (default ".") is the subdirectory of the copy used as the gate's
``--root``; ``argv`` entries are appended to the gate command line.
Supported setup ops:

  mkdir      create a directory (parents included)
  fifo       replace the file at ``path`` with a FIFO
  git_init   initialize a Git repository at the copy root
  git_commit stage everything and commit; it must follow a git_init in the
             same setup list (Git identity is set by the runner; the
             environment is isolated: inherited GIT_* variables are dropped,
             GIT_CONFIG_GLOBAL is pinned to /dev/null, GIT_CEILING_DIRECTORIES
             is the copy's parent, and every command names --git-dir and
             --work-tree inside the copy)

Containment (round 31).  The runner refuses, as a failed case, before the gate
is started:

  * an ``argv`` token that is not a value (a token starting with "-") unless
    it is ``--name`` or ``--name=value`` where ``name`` is a non-empty prefix
    of exactly one of root, revision, population or ledger and of no other
    gate option (json, selftest, help): so ``--selftest`` and its
    abbreviations, which would make the gate run scripts copied from the
    fixture, are refused, and so is an ambiguous prefix such as ``--r``;
  * a case directory that contains an entry named ``.git`` at any depth;
  * a ``git_commit`` step with no earlier ``git_init``;
  * an ``expected.json`` that is a symlink, not a regular file, or larger
    than 1 MiB (it is opened with O_NOFOLLOW, O_NONBLOCK and O_NOCTTY, so a
    FIFO at ``expected.json`` cannot block that read; a setup ``fifo`` step on
    a file Git reads, such as ``.gitattributes``, can still block ``git add``
    until the case timeout);
  * a symlink in the fixture directory, dot-named or not (a symlinked case
    is a failed case, never a silent skip).

The hostile specs probe five routed shapes (N1, N2, N3, N5, N6) and, since
round 32, which layer refuses a ``git_commit`` with no earlier ``git_init``
(P6, mutant m3: the load-time check in ``load_case_setup`` must refuse before
the apply-time re-check in ``apply_setup`` is reached).  The Git pins named
above (--git-dir/--work-tree, GIT_CEILING_DIRECTORIES for setup and gate) are
not separately probed: a runner without them still passes the hostile
selftest and the round-31 C1 counter.  A ``--tmpdir`` whose resolved
scratch path contains os.pathsep is refused (could not evaluate), because Git
cannot escape that separator in GIT_CEILING_DIRECTORIES.

``scripts/citing_set_hostile_selftest.py`` checks these refusals against the
hostile specs in ``scripts/fixtures/citing-set-hostile/``; since round 33 P6
names the refusing layer by the runner's ``code`` (``reason_code``), not by
message text.

This runner is a pure oracle.  For every fixture case it starts one gate
subprocess and compares two observable outcomes with the frozen expectation:

  * the process exit code, exactly; and
  * the finding multiset (ids, or (id, reason) pairs for object expectations).

It never rewrites an expectation, never mutates a fixture, never edits the
repository and never contacts the network.  A case whose ``expected.json`` is
missing, unparsable or malformed fails the run instead of being skipped, and a
fixture directory that is absent or empty can never report success.

Summary (one JSON object on stdout)::

    {"verdict": "clean"|"failed"|"could-not-evaluate",
     "cases": <int>, "failed": <int>, "results": [{"case": ..., "passed": ...}]}

``cases`` is the number of discovered fixture cases.  ``failed`` counts
unsatisfied obligations: one per failing case, or one when the run could not be
evaluated at all, so ``failed == 0`` is only ever true for a run that may pass.

Each result row and each case failure entry carries ``reason`` (human text,
free to change) and ``code`` (stable, or null where no code is assigned).
Since round 33 the setup refusals carry codes: ``setup_commit_before_init``
(load-time check in ``load_case_setup``), ``setup_commit_without_repo``
(apply-time re-check in ``apply_setup``) and ``setup_failed`` (any other
apply-time setup failure).  Other refusals report ``code`` null.

Exit codes: 0 every case matched, 1 at least one case mismatched,
2 the run could not be evaluated (gate absent, fixture directory absent/empty).
"""
from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_CANNOT_EVALUATE = 2

DEFAULT_TMPDIR = "/fast/scratch/hyaku/kake-r27"
CONTRACT_MINIMUM_CASES = 12
DEFAULT_TIMEOUT_SECONDS = 120.0
TAIL_BYTES = 800

CASE_SETUP_FILE = "case.json"
CASE_SETUP_MAX_BYTES = 65536
CASE_SETUP_MAX_OPS = 64
EXPECTED_MAX_BYTES = 1048576
SETUP_OPS = ("mkdir", "fifo", "git_init", "git_commit")
GATE_VALUE_OPTIONS = ("root", "revision", "population", "ledger")
GATE_OTHER_OPTIONS = ("json", "selftest", "help")
GIT_IDENTITY = {
    "GIT_AUTHOR_NAME": "citing-set-selftest",
    "GIT_AUTHOR_EMAIL": "citing-set-selftest@invalid",
    "GIT_COMMITTER_NAME": "citing-set-selftest",
    "GIT_COMMITTER_EMAIL": "citing-set-selftest@invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
}


# --------------------------------------------------------------------------
# argument handling
# --------------------------------------------------------------------------
def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="citing_set_selftest.py",
        description="Run the citing-set gate over every fixture case and compare exact outcomes.",
    )
    parser.add_argument("--root", default=None, help="repository root (default: parent of this script's directory)")
    parser.add_argument("--fixtures", default=None, help="fixture directory (default: <root>/scripts/fixtures/citing-set)")
    parser.add_argument("--gate", default=None, help="gate script (default: <root>/scripts/citing_set.py)")
    parser.add_argument("--tmpdir", default=DEFAULT_TMPDIR, help="scratch directory exported as TMPDIR to gate subprocesses")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS, help="per-case gate timeout in seconds")
    parser.add_argument("--min-cases", type=int, default=0, help="fail when fewer than this many fixture cases exist")
    parser.add_argument("--json", action="store_true", help="accepted for interface symmetry; the summary is always JSON")
    parser.add_argument("--selftest", action="store_true", help="accepted so the gate may delegate this runner verbatim")
    args, unknown = parser.parse_known_args(argv)
    return args, unknown


def resolve_paths(args):
    script = Path(__file__).resolve()
    root = Path(args.root).expanduser().resolve() if args.root else script.parents[1]
    gate = Path(args.gate).expanduser().resolve() if args.gate else root / "scripts" / "citing_set.py"
    fixtures = Path(args.fixtures).expanduser().resolve() if args.fixtures else root / "scripts" / "fixtures" / "citing-set"
    return root, gate, fixtures


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------
def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def tail(text, limit=TAIL_BYTES):
    if text is None:
        return ""
    if len(text) <= limit:
        return text
    return "..." + text[-limit:]


def child_env(tmpdir):
    """Environment for gate subprocesses: scratch TMPDIR and an isolated HOME."""
    env = dict(os.environ)
    scratch = Path(tmpdir).expanduser()
    home = scratch / "citing-set-selftest" / "home"
    try:
        scratch.mkdir(parents=True, exist_ok=True)
        home.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    env["TMPDIR"] = str(scratch)
    env["TMP"] = str(scratch)
    env["TEMP"] = str(scratch)
    env["HOME"] = str(home)
    env["KAKE_SELFTEST"] = "citing-set-selftest"
    return env


def parse_report(stdout):
    """Return the gate's JSON report object, or raise ValueError."""
    text = (stdout or "").strip()
    if not text:
        raise ValueError("gate produced no stdout")
    try:
        report = json.loads(text)
    except ValueError:
        report = None
    if isinstance(report, dict):
        return report
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            candidate, _ = decoder.raw_decode(text, index)
        except ValueError:
            continue
        if isinstance(candidate, dict):
            return candidate
    raise ValueError("gate stdout is not a JSON object")


def finding_pairs(report):
    """Sorted multiset of (id, reason) pairs in a gate report.

    A finding without a usable ``id`` is kept as an opaque placeholder so that a
    malformed finding can never compare equal to an empty expectation; a
    finding without a used ``reason`` compares as ``None``.  A legacy string
    finding compares as (string, None).
    """
    findings = report.get("findings") if isinstance(report, dict) else None
    if findings is None:
        return []
    if not isinstance(findings, list):
        return [("<findings-not-a-list>", None)]
    pairs = []
    for item in findings:
        if isinstance(item, str):
            pairs.append((item, None))
        elif isinstance(item, dict):
            identifier = item.get("id")
            reason = item.get("reason")
            pairs.append(
                (
                    identifier if isinstance(identifier, str) else json.dumps(item, sort_keys=True),
                    reason if isinstance(reason, str) else None,
                )
            )
        else:
            pairs.append((json.dumps(item, sort_keys=True), None))
    return sorted(pairs, key=pair_order)


def pair_order(pair):
    """Total order for (id, reason) pairs; a missing reason (None) sorts first."""
    identifier, reason = pair
    return (identifier, reason is not None, reason or "")


def expectation_entries(expected):
    """Return (mode, entries) for an oracle ``expected``, or raise ValueError.

    ``mode`` is "ids" for the legacy all-strings form and "pairs" for the
    object form; ``entries`` is the sorted multiset the runner must match.
    """
    if not isinstance(expected, dict):
        raise ValueError("expected.json must be a JSON object")
    if "exit" not in expected:
        raise ValueError('expected.json must carry an integer "exit"')
    value = expected["exit"]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError('expected.json must carry an integer "exit"')
    findings = expected.get("findings")
    if not isinstance(findings, list):
        raise ValueError('expected.json must carry a list of finding entries in "findings"')
    if not findings:
        return "pairs", []
    kinds = set()
    for item in findings:
        if isinstance(item, str):
            kinds.add("ids")
        elif isinstance(item, dict) and isinstance(item.get("id"), str):
            kinds.add("pairs")
            reason = item.get("reason")
            if reason is not None and not isinstance(reason, str):
                raise ValueError('expected.json object finding "reason" must be a string or null')
        else:
            raise ValueError('expected.json "findings" must be all strings (legacy) or all {"id", "reason"} objects')
    if len(kinds) > 1:
        raise ValueError('expected.json "findings" must be all strings or all objects, not mixed')
    if "ids" in kinds:
        return "ids", sorted(findings)
    return "pairs", sorted(((item["id"], item.get("reason")) for item in findings), key=pair_order)


# --------------------------------------------------------------------------
# per-case setup (optional case.json)
# --------------------------------------------------------------------------
class CaseRefusal(ValueError):
    """A case refusal that carries a stable machine-readable ``code``.

    The runner reports ``code`` next to the human ``reason`` in each result
    row and failure entry, so a check can name the refusing layer without
    matching message text (round 33, round-32 routed item 2).
    """

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


class SetupRefusal(RuntimeError):
    """An apply-time setup refusal that carries a stable ``code``."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def load_case_setup(case_dir):
    """Load and validate the optional case.json; return None when absent."""
    path = case_dir / CASE_SETUP_FILE
    if not path.is_file():
        return None
    try:
        if path.is_symlink() or path.stat().st_size > CASE_SETUP_MAX_BYTES:
            raise ValueError("%s must be a regular file of at most %d bytes" % (CASE_SETUP_FILE, CASE_SETUP_MAX_BYTES))
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError("%s unreadable: %s" % (CASE_SETUP_FILE, exc))
    try:
        document = json.loads(raw)
    except ValueError as exc:
        raise ValueError("%s is not valid JSON: %s" % (CASE_SETUP_FILE, exc))
    if not isinstance(document, dict):
        raise ValueError("%s must be a JSON object" % CASE_SETUP_FILE)
    argv = document.get("argv", [])
    if not isinstance(argv, list) or not all(isinstance(item, str) for item in argv):
        raise ValueError('%s "argv" must be a list of strings' % CASE_SETUP_FILE)
    refused = argv_refusal(argv)
    if refused is not None:
        raise ValueError("%s argv refused: %s" % (CASE_SETUP_FILE, refused))
    root = document.get("root", ".")
    if not isinstance(root, str) or not root.strip() or not contained_relative(root):
        raise ValueError('%s "root" must be a non-empty relative path with no ".." part' % CASE_SETUP_FILE)
    setup = document.get("setup", [])
    if not isinstance(setup, list) or len(setup) > CASE_SETUP_MAX_OPS:
        raise ValueError('%s "setup" must be a list of at most %d steps' % (CASE_SETUP_FILE, CASE_SETUP_MAX_OPS))
    initialized = False
    for step in setup:
        if not isinstance(step, dict) or not isinstance(step.get("op"), str):
            raise ValueError('%s "setup" entries must be objects with a string "op"' % CASE_SETUP_FILE)
        if step["op"] not in SETUP_OPS:
            raise ValueError('%s names an unknown setup op %r' % (CASE_SETUP_FILE, step["op"]))
        if step["op"] in ("mkdir", "fifo"):
            if not isinstance(step.get("path"), str) or not step["path"].strip() or not contained_relative(step["path"]):
                raise ValueError('%s setup op %r needs a non-empty relative "path" with no ".." part' % (CASE_SETUP_FILE, step["op"]))
            if ".git" in step["path"].split("/"):
                raise ValueError('%s setup op %r may not create a .git path' % (CASE_SETUP_FILE, step["op"]))
        if step["op"] == "git_init":
            initialized = True
        if step["op"] == "git_commit" and not initialized:
            raise CaseRefusal("setup_commit_before_init", "%s setup op 'git_commit' needs an earlier 'git_init'" % CASE_SETUP_FILE)
    return {"argv": argv, "root": root, "setup": setup}


def argv_refusal(argv):
    """Return the first argv token outside the gate-option allowlist, or None.

    A token that does not start with "-" is a value.  An option token must be
    ``--name`` or ``--name=value`` where ``name`` is a non-empty prefix of
    exactly one valued gate option and of no other gate option, so argparse
    abbreviation can never reach ``--selftest``, ``--json`` or ``--help`` and
    an ambiguous prefix such as ``--r`` is refused here, not by the gate.
    """
    for token in argv:
        if not token.startswith("-"):
            continue
        name = token[2:].split("=", 1)[0] if token.startswith("--") else ""
        if (not name
                or sum(option.startswith(name) for option in GATE_VALUE_OPTIONS) != 1
                or any(option.startswith(name) for option in GATE_OTHER_OPTIONS)):
            return token
    return None


def dot_git_entry(case_dir):
    """Return the relative path of the first entry named .git in a case, or None."""
    for current, dirs, files in os.walk(case_dir, followlinks=False):
        for name in sorted(dirs + files):
            if name == ".git":
                return os.path.relpath(os.path.join(current, name), case_dir)
    return None


def read_expected(case_dir):
    """Read expected.json without following a symlink or blocking on a FIFO."""
    path = case_dir / "expected.json"
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOCTTY", 0)
    try:
        descriptor = os.open(str(path), flags)
    except OSError as exc:
        note = " (symlinks are refused)" if exc.errno == errno.ELOOP else ""
        raise ValueError("expected.json unreadable%s: %s" % (note, exc))
    try:
        status = os.fstat(descriptor)
        if not stat.S_ISREG(status.st_mode):
            raise ValueError("expected.json must be a regular file")
        if status.st_size > EXPECTED_MAX_BYTES:
            raise ValueError("expected.json must be at most %d bytes" % EXPECTED_MAX_BYTES)
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            data = handle.read(EXPECTED_MAX_BYTES + 1)
    finally:
        os.close(descriptor)
    if len(data) > EXPECTED_MAX_BYTES:
        raise ValueError("expected.json must be at most %d bytes" % EXPECTED_MAX_BYTES)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("expected.json is not UTF-8: %s" % exc)


def contained_relative(value):
    """True for a relative POSIX path with no '..' part and no NUL byte."""
    if "\x00" in value or value.startswith("/") or "\\" in value:
        return False
    return ".." not in value.split("/")


def inside(work_dir, relative):
    """Resolve ``relative`` under ``work_dir``; refuse anything that escapes it."""
    base = os.path.realpath(work_dir)
    target = os.path.realpath(os.path.join(base, relative))
    if target != base and not target.startswith(base + os.sep):
        raise RuntimeError("setup path escapes the case copy: %s" % relative)
    return Path(target)


def git_env(work_dir):
    """Isolated environment for setup Git commands in one case copy."""
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_IDENTITY)
    env["GIT_CEILING_DIRECTORIES"] = os.path.dirname(os.path.realpath(work_dir))
    return env


def git_command(work_dir, *args):
    """A Git command bound to the copy's own repository and work tree."""
    base = os.path.realpath(work_dir)
    return ["git", "--git-dir=" + os.path.join(base, ".git"), "--work-tree=" + base,
            "-c", "core.hooksPath=/dev/null", *args]


def run_command(command, cwd, env, timeout):
    try:
        done = subprocess.run(
            command,
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("setup command timed out: %s" % " ".join(command))
    if done.returncode != 0:
        raise RuntimeError(
            "setup command failed (%d): %s" % (done.returncode, tail(done.stderr or done.stdout))
        )
    return done


def apply_setup(work_dir, setup, timeout):
    env = git_env(work_dir)
    for step in setup:
        op = step["op"]
        if op == "mkdir":
            inside(work_dir, step["path"]).mkdir(parents=True, exist_ok=True)
        elif op == "fifo":
            target = inside(work_dir, step["path"])
            if target.exists() or target.is_symlink():
                target.unlink()
            os.mkfifo(target)
        elif op == "git_init":
            if (work_dir / ".git").exists() or (work_dir / ".git").is_symlink():
                raise RuntimeError("a fixture may not carry its own .git")
            run_command(git_command(work_dir, "init", "-q"), work_dir, env, timeout)
        elif op == "git_commit":
            if not (work_dir / ".git").is_dir() or (work_dir / ".git").is_symlink():
                raise SetupRefusal("setup_commit_without_repo", "git_commit needs the repository created by git_init")
            run_command(git_command(work_dir, "add", "-A"), work_dir, env, timeout)
            run_command(git_command(work_dir, "commit", "-q", "--no-verify",
                                    "-m", str(step.get("message", "fixture"))), work_dir, env, timeout)


def prepare_case(case_dir, cases_root, timeout):
    """Copy one case into the scratch tree and apply its setup.

    Returns (work_dir, setup) where ``setup`` is None when the case has no
    case.json.  The committed fixture is never written to.
    """
    try:
        setup = load_case_setup(case_dir)
    except ValueError as exc:
        return None, exc
    work_dir = cases_root / case_dir.name
    try:
        if work_dir.exists():
            shutil.rmtree(work_dir)
        shutil.copytree(case_dir, work_dir, symlinks=True)
    except (OSError, shutil.Error) as exc:
        return None, "case copy failed: %s" % exc
    if setup:
        try:
            apply_setup(work_dir, setup["setup"], timeout)
        except (OSError, RuntimeError) as exc:
            return None, CaseRefusal(getattr(exc, "code", "setup_failed"), "case setup failed: %s" % exc)
    return work_dir, setup


# --------------------------------------------------------------------------
# one fixture case
# --------------------------------------------------------------------------
def run_case(case_dir, gate, env, timeout, cases_root):
    row = {
        "case": case_dir.name,
        "ok": False,
        "passed": False,
        "reason": None,
        "code": None,
        "expected": None,
        "actual": None,
        "argv": None,
    }
    if case_dir.is_symlink():
        row["reason"] = "symlinked case directory refused"
        return row
    dot_git = dot_git_entry(case_dir)
    if dot_git is not None:
        row["reason"] = "fixture carries a .git entry, refused: %s" % dot_git
        return row
    try:
        raw = read_expected(case_dir)
    except ValueError as exc:
        row["reason"] = str(exc)
        return row
    try:
        expected = json.loads(raw)
    except ValueError as exc:
        row["reason"] = "expected.json is not valid JSON: %s" % exc
        return row
    try:
        mode, expected_entries = expectation_entries(expected)
    except ValueError as exc:
        row["reason"] = str(exc)
        return row
    row["expected"] = {"exit": expected["exit"], "findings": expected_entries, "mode": mode}

    work_dir, setup = prepare_case(case_dir, cases_root, timeout)
    if work_dir is None:
        row["reason"] = str(setup)
        row["code"] = getattr(setup, "code", None)
        return row
    root = work_dir
    if setup:
        try:
            root = inside(work_dir, setup["root"])
        except RuntimeError as exc:
            row["reason"] = str(exc)
            return row
    argv = [
        sys.executable,
        "-B",
        str(gate),
        "--root",
        str(root),
        "--population",
        "population.json",
        "--ledger",
        "ledger.json",
        "--json",
    ]
    if setup:
        argv.extend(setup["argv"])
    row["argv"] = argv
    try:
        run = subprocess.run(
            argv,
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        row["reason"] = "gate timed out after %gs" % timeout
        return row
    except OSError as exc:
        row["reason"] = "gate could not be started: %s" % exc
        return row

    try:
        report = parse_report(run.stdout)
    except ValueError as exc:
        row["reason"] = "gate stdout is not a JSON report: %s" % exc
        row["actual"] = {
            "exit": run.returncode,
            "stdout": tail(run.stdout),
            "stderr": tail(run.stderr),
        }
        return row

    if "findings" not in report:
        row["reason"] = "gate report carries no 'findings' array"
        row["actual"] = {"exit": run.returncode, "verdict": report.get("verdict"), "findings": None}
        return row
    if not isinstance(report["findings"], list):
        row["reason"] = "gate report 'findings' is not an array"
        row["actual"] = {"exit": run.returncode, "verdict": report.get("verdict"), "findings": None}
        return row

    observed_pairs = finding_pairs(report)
    if mode == "ids":
        observed = sorted(identifier for identifier, _ in observed_pairs)
    else:
        observed = observed_pairs
    row["actual"] = {
        "exit": run.returncode,
        "verdict": report.get("verdict"),
        "findings": observed,
        "mode": mode,
    }
    if run.returncode != expected["exit"]:
        row["reason"] = "exit mismatch: expected %d, observed %d" % (expected["exit"], run.returncode)
        return row
    if observed != expected_entries:
        row["reason"] = "finding mismatch: expected %s, observed %s" % (
            json.dumps(expected_entries),
            json.dumps(observed),
        )
        return row
    row["ok"] = True
    row["passed"] = True
    return row


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------
def emit(summary):
    print(json.dumps(summary, indent=2))


def main(argv=None):
    args, unknown = parse_args(list(sys.argv[1:] if argv is None else argv))
    root, gate, fixtures = resolve_paths(args)

    summary = {
        "schema": "kake-citing-set-selftest-v1",
        "verdict": "could-not-evaluate",
        "passed": False,
        "cases": 0,
        "failed": 0,
        "failedCases": 0,
        "caseNames": [],
        "contractMinimumCases": CONTRACT_MINIMUM_CASES,
        "meetsContractMinimum": False,
        "root": str(root),
        "runner": str(Path(__file__).resolve()),
        "runnerSha256": sha256_file(Path(__file__).resolve()),
        "gate": str(gate),
        "gateSha256": None,
        "fixtures": str(fixtures),
        "results": [],
        "failures": [],
        "notes": [],
    }
    if unknown:
        summary["notes"].append("ignored unknown arguments: %s" % " ".join(unknown))

    def cannot_evaluate(reason):
        summary["failures"].append({"case": None, "reason": reason})
        summary["failed"] = 1
        emit(summary)
        return EXIT_CANNOT_EVALUATE

    if not gate.is_file():
        return cannot_evaluate("gate script not found: %s" % gate)
    summary["gateSha256"] = sha256_file(gate)

    if not fixtures.is_dir():
        return cannot_evaluate("fixture directory not found: %s" % fixtures)

    cases = sorted(
        (path for path in fixtures.iterdir()
         if path.is_symlink() or (path.is_dir() and not path.name.startswith("."))),
        key=lambda path: path.name,
    )
    if not cases:
        return cannot_evaluate("fixture directory contains no case directories: %s" % fixtures)

    env = child_env(args.tmpdir)
    cases_root = Path(args.tmpdir).expanduser().resolve() / "citing-set-selftest" / "cases"
    if os.pathsep in str(cases_root):
        # Git splits GIT_CEILING_DIRECTORIES on os.pathsep with no escape, so
        # such a path would switch the ceiling off.
        return cannot_evaluate("scratch case tree path contains %r: %s" % (os.pathsep, cases_root))
    try:
        cases_root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return cannot_evaluate("cannot create scratch case tree %s: %s" % (cases_root, exc))
    env = {key: value for key, value in env.items() if key not in ("GIT_DIR", "GIT_WORK_TREE")}
    env["GIT_CEILING_DIRECTORIES"] = str(cases_root)

    for case_dir in cases:
        row = run_case(case_dir, gate, env, args.timeout, cases_root)
        summary["results"].append(row)
        if not row["ok"]:
            summary["failedCases"] += 1
            summary["failures"].append(
                {
                    "case": row["case"],
                    "reason": row["reason"],
                    "code": row["code"],
                    "expected": row["expected"],
                    "actual": row["actual"],
                }
            )

    summary["cases"] = len(cases)
    summary["caseNames"] = [case_dir.name for case_dir in cases]
    summary["failed"] = summary["failedCases"]
    summary["meetsContractMinimum"] = len(cases) >= CONTRACT_MINIMUM_CASES
    if not summary["meetsContractMinimum"]:
        summary["notes"].append(
            "fixture case count %d is below the contract minimum %d (run with --min-cases %d to enforce)"
            % (len(cases), CONTRACT_MINIMUM_CASES, CONTRACT_MINIMUM_CASES)
        )

    if summary["failedCases"]:
        summary["verdict"] = "failed"
        emit(summary)
        return EXIT_FAILED
    if args.min_cases and len(cases) < args.min_cases:
        summary["failures"].append(
            {
                "case": None,
                "reason": "fixture case count %d below required minimum %d" % (len(cases), args.min_cases),
            }
        )
        summary["failed"] = 1
        summary["verdict"] = "failed"
        emit(summary)
        return EXIT_FAILED

    summary["verdict"] = "clean"
    summary["passed"] = True
    emit(summary)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
