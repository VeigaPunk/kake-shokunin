#!/usr/bin/env python3
"""landed_check.py -- compare commit hashes cited in a report against branch ancestry.

Usage
  python3 -B landed_check.py --report REPORT.md --repo GITDIR --branch NAME
  python3 -B landed_check.py --selftest

What it does
  * Extracts every 7-40 hex-digit token from the report (backticked or bare).
    Tokens embedded in a longer hex run are never matched, so a sha256-length
    64-hex digest is skipped by construction. An unresolvable hex token on a
    line that names a digest algorithm (`sha256`, `sha1`, `md5`, ...) is
    suppressed as a digest fragment rather than reported as an unknown commit.
  * Resolves each token to a commit object in REPO.
  * Prints one line per distinct cited commit, in report order:
        ANCESTOR|NOT-ANCESTOR|UNKNOWN <hash> <subject>
    then a final summary line:
        cited=N landed=N missing=N unknown=N

Exit codes
  0  every cited resolvable hash is an ancestor of BRANCH and at least one was
     resolvable (unresolvable tokens are tolerated and counted as unknown)
  1  at least one cited commit is NOT an ancestor of BRANCH
  2  unevaluable: repo/branch/report unusable, no resolvable hash cited, or an
     ancestry query failed for a resolvable commit
  64 usage error

Classification rules (deterministic, see LIMITS in the seat report)
  * token resolves to a commit      -> ancestry check
  * token resolves to a non-commit  -> not a commit citation, skipped silently
    object (blob/tree/tag peeled away)   (not counted as cited)
  * token resolves to nothing, but  -> digest fragment, skipped silently
    its line names a digest algorithm
  * token resolves to nothing       -> UNKNOWN, counted as cited and unknown

Stdlib only; no network; no writes outside the repositories it is pointed at.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

USAGE_EXIT = 64
MIN_HASH_LEN = 7
MAX_HASH_LEN = 40
DIGEST_LEN = 64

HEX_RUN = re.compile(
    r"(?<![0-9a-fA-F])[0-9a-fA-F]{%d,%d}(?![0-9a-fA-F])" % (MIN_HASH_LEN, MAX_HASH_LEN)
)
DIGEST_LABEL = re.compile(r"(?i)(?:sha[-_ ]?(?:1|256|512)|md5|blake2|digest)")


# --------------------------------------------------------------------------- git

def git(repo, *args, stdin=None):
    """Run a git command inside REPO; return the CompletedProcess."""
    return subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True,
        text=True,
        input=stdin,
    )


def is_git_dir(repo):
    if not repo or not os.path.isdir(repo):
        return False
    return git(repo, "rev-parse", "--git-dir").returncode == 0


def resolve_commit(repo, token):
    """Return the full commit oid TOKEN names, or None."""
    proc = git(repo, "rev-parse", "--verify", "--quiet", token + "^{commit}")
    if proc.returncode != 0:
        return None
    out = proc.stdout.strip()
    return out or None


def object_type(repo, token):
    """Return the object type TOKEN names (commit/tree/blob/tag), or None."""
    proc = git(repo, "cat-file", "-t", token)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def commit_subject(repo, oid):
    proc = git(repo, "log", "-1", "--format=%s", oid)
    if proc.returncode != 0:
        return "-"
    subject = proc.stdout.strip()
    return subject or "-"


def ancestry(repo, oid, branch):
    """True if OID is an ancestor of BRANCH, False if not, None if undeterminable."""
    proc = git(repo, "merge-base", "--is-ancestor", oid, branch)
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    return None


# ---------------------------------------------------------------------- extraction

def extract_tokens(text):
    """Return [(token, line_text)] for hash-shaped tokens, first occurrence only."""
    seen = set()
    out = []
    for match in HEX_RUN.finditer(text):
        token = match.group(0)
        if len(token) == DIGEST_LEN:
            continue
        key = token.lower()
        if key in seen:
            continue
        seen.add(key)
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.start())
        if line_end < 0:
            line_end = len(text)
        out.append((token, text[line_start:line_end]))
    return out


# ------------------------------------------------------------------------- analysis

class Result:
    __slots__ = ("lines", "summary", "exit_code", "cited", "landed", "missing",
                 "unknown", "undetermined", "suppressed_digests", "error")

    def __init__(self):
        self.lines = []
        self.summary = "cited=0 landed=0 missing=0 unknown=0"
        self.exit_code = 2
        self.cited = self.landed = self.missing = self.unknown = 0
        self.undetermined = 0
        self.suppressed_digests = 0
        self.error = None


def analyse(report_text, repo, branch):
    result = Result()
    if not is_git_dir(repo):
        result.error = "not a git repository: %s" % repo
        return result
    if not branch or git(repo, "rev-parse", "--verify", "--quiet", branch + "^{commit}").returncode != 0:
        result.error = "branch does not resolve to a commit: %s" % (branch or "<empty>")
        return result

    seen_commits = {}
    seen_unknown = set()
    for token, line_text in extract_tokens(report_text):
        oid = resolve_commit(repo, token)
        if oid is not None:
            if oid in seen_commits:
                continue
            seen_commits[oid] = token
            result.cited += 1
            state = ancestry(repo, oid, branch)
            subject = commit_subject(repo, oid)
            if state is True:
                result.landed += 1
                result.lines.append("ANCESTOR %s %s" % (token, subject))
            elif state is False:
                result.missing += 1
                result.lines.append("NOT-ANCESTOR %s %s" % (token, subject))
            else:
                result.unknown += 1
                result.undetermined += 1
                result.lines.append("UNKNOWN %s %s" % (token, subject))
            continue

        kind = object_type(repo, token)
        if kind is not None and kind != "commit":
            # A real object in this repo that is not a commit: not a commit citation.
            continue

        if DIGEST_LABEL.search(line_text):
            # Unresolvable hex on a line that names a digest algorithm: a digest
            # fragment, not a commit citation.
            result.suppressed_digests += 1
            continue

        key = token.lower()
        if key in seen_unknown:
            continue
        seen_unknown.add(key)
        result.cited += 1
        result.unknown += 1
        result.lines.append("UNKNOWN %s -" % token)

    result.summary = "cited=%d landed=%d missing=%d unknown=%d" % (
        result.cited, result.landed, result.missing, result.unknown)
    if result.missing:
        result.exit_code = 1
    elif result.landed == 0 or result.undetermined:
        result.exit_code = 2
    else:
        result.exit_code = 0
    return result


def check_report(report_path, repo, branch):
    result = Result()
    try:
        with open(report_path, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
    except OSError as exc:
        result.error = "cannot read report %s: %s" % (report_path, exc.strerror or exc)
        return result
    return analyse(text, repo, branch)


# --------------------------------------------------------------------------- selftest

def _run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def _init_repo():
    """Create a throwaway repo in mktemp -d and prove it is the toplevel."""
    directory = tempfile.mkdtemp(prefix="landed-check-")
    proc = _run(["git", "-C", directory, "init", "-q", "-b", "master"])
    assert proc.returncode == 0, "git init failed: %s" % proc.stderr.strip()
    top = _run(["git", "-C", directory, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(directory), (
        "temp repo toplevel %r != %r" % (top, directory))
    return directory


def _commit(directory, message, filename="f.txt", content=None):
    path = os.path.join(directory, filename)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(content if content is not None else message + "\n")
    _run(["git", "-C", directory, "add", "-A"])
    proc = _run(["git", "-C", directory, "-c", "user.name=selftest",
                 "-c", "user.email=selftest@local", "commit", "-q", "-m", message])
    assert proc.returncode == 0, "commit failed: %s" % proc.stderr.strip()
    return _run(["git", "-C", directory, "rev-parse", "HEAD"]).stdout.strip()


def _write_report(directory, text, name="report.md"):
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return path


def _object_format(directory):
    proc = _run(["git", "-C", directory, "rev-parse", "--show-object-format"])
    return (proc.stdout.strip() or "sha1")


def _write_blob(directory, content_bytes):
    proc = subprocess.run(["git", "-C", directory, "hash-object", "-w", "--stdin"],
                          input=content_bytes, capture_output=True)
    assert proc.returncode == 0, "hash-object failed"
    return proc.stdout.decode().strip()


def _ambiguous_blob_prefix(directory, length=7):
    """Write two blobs that share a `length`-hex prefix; return that prefix."""
    algorithm = _object_format(directory)
    digest = hashlib.sha256 if algorithm == "sha256" else hashlib.sha1
    seen = {}
    index = 0
    while True:
        content = ("ambiguous-blob-%d\n" % index).encode()
        header = b"blob %d\0" % len(content)
        oid = digest(header + content).hexdigest()
        prefix = oid[:length]
        if prefix in seen:
            first = seen[prefix]
            got_a = _write_blob(directory, first)
            got_b = _write_blob(directory, content)
            assert got_a.startswith(prefix) and got_b.startswith(prefix), "prefix mismatch"
            assert got_a != got_b, "blobs identical"
            listing = _run(["git", "-C", directory, "rev-parse", "--disambiguate=" + prefix])
            assert len(listing.stdout.split()) >= 2, "prefix is not ambiguous in this repo"
            return prefix
        seen[prefix] = content
        index += 1


def _fixtures():
    """Return [(name, builder)]; builder(dir) -> (report_path, repo, branch, expect)."""
    def honest(directory):
        first = _commit(directory, "first")
        second = _commit(directory, "second")
        report = _write_report(directory,
                               "Landed `%s` then `%s` and short %s.\n" % (first, second, second[:12]))
        return report, directory, "master", dict(code=0, cited=2, landed=2, missing=0, unknown=0)

    def side_branch(directory):
        base = _commit(directory, "base")
        _run(["git", "-C", directory, "checkout", "-q", "-b", "feat"])
        side = _commit(directory, "side work")
        _run(["git", "-C", directory, "checkout", "-q", "master"])
        report = _write_report(directory, "Landed `%s`, then claimed `%s`.\n" % (base, side))
        return report, directory, "master", dict(code=1, cited=2, landed=1, missing=1, unknown=0)

    def unknown_hash(directory):
        real = _commit(directory, "real")
        report = _write_report(directory, "Real %s, ghost %s.\n" % (real, "deadbeef" * 5))
        return report, directory, "master", dict(code=0, cited=2, landed=1, missing=0, unknown=1)

    def sha256_ignored(directory):
        real = _commit(directory, "real")
        digest = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        report = _write_report(directory, "Commit %s, digest %s.\n" % (real, digest))
        return report, directory, "master", dict(code=0, cited=1, landed=1, missing=0, unknown=0)

    def short_ambiguous(directory):
        real = _commit(directory, "real")
        prefix = _ambiguous_blob_prefix(directory)
        report = _write_report(directory, "Commit %s, prefix %s.\n" % (real, prefix))
        return report, directory, "master", dict(code=0, cited=2, landed=1, missing=0, unknown=1)

    def empty_report(directory):
        _commit(directory, "only")
        report = _write_report(directory, "")
        return report, directory, "master", dict(code=2, cited=0, landed=0, missing=0, unknown=0)

    def prose_only(directory):
        _commit(directory, "only")
        report = _write_report(directory, "Nothing was landed; no identifiers here at all.\n")
        return report, directory, "master", dict(code=2, cited=0, landed=0, missing=0, unknown=0)

    def branch_missing(directory):
        real = _commit(directory, "real")
        report = _write_report(directory, "Commit %s.\n" % real)
        return report, directory, "nope", dict(code=2, cited=0, landed=0, missing=0, unknown=0)

    def code_fence(directory):
        real = _commit(directory, "real")
        report = _write_report(directory, "```\n%s\n```\n" % real)
        return report, directory, "master", dict(code=0, cited=1, landed=1, missing=0, unknown=0)

    def duplicate_hash(directory):
        real = _commit(directory, "real")
        report = _write_report(directory,
                               "`%s` and `%s` and bare %s.\n" % (real, real[:12], real[:7]))
        return report, directory, "master", dict(code=0, cited=1, landed=1, missing=0, unknown=0)

    def non_commit_object(directory):
        real = _commit(directory, "real")
        blob = _run(["git", "-C", directory, "rev-parse", "HEAD:f.txt"]).stdout.strip()
        report = _write_report(directory, "Commit %s, blob %s.\n" % (real, blob))
        return report, directory, "master", dict(code=0, cited=1, landed=1, missing=0, unknown=0)

    def digest_labelled(directory):
        real = _commit(directory, "real")
        report = _write_report(directory, "Commit %s; sha256 2b146a72 rest.\n" % real)
        return report, directory, "master", dict(code=0, cited=1, landed=1, missing=0, unknown=0)

    def report_missing(directory):
        _commit(directory, "real")
        return os.path.join(directory, "absent.md"), directory, "master", dict(code=2)

    return [
        ("honest-report", honest),
        ("side-branch-hash", side_branch),
        ("unknown-hash", unknown_hash),
        ("sha256-token-ignored", sha256_ignored),
        ("short-hash-ambiguity", short_ambiguous),
        ("empty-report", empty_report),
        ("prose-only-report", prose_only),
        ("branch-missing", branch_missing),
        ("hash-inside-code-fence", code_fence),
        ("duplicate-hash-counted-once", duplicate_hash),
        ("non-commit-object-skipped", non_commit_object),
        ("digest-label-ignored", digest_labelled),
        ("report-missing", report_missing),
        ("usage-error", None),
    ]


def _expect(result, expect):
    problems = []
    if "code" in expect and result.exit_code != expect["code"]:
        problems.append("exit %s != %s" % (result.exit_code, expect["code"]))
    for key in ("cited", "landed", "missing", "unknown"):
        if key in expect and getattr(result, key) != expect[key]:
            problems.append("%s=%s != %s" % (key, getattr(result, key), expect[key]))
    if result.summary.split() != [
            "cited=%d" % result.cited, "landed=%d" % result.landed,
            "missing=%d" % result.missing, "unknown=%d" % result.unknown]:
        problems.append("summary line malformed: %r" % result.summary)
    return problems


def selftest():
    passed = 0
    failures = []
    fixtures = _fixtures()
    for name, builder in fixtures:
        directory = None
        try:
            if builder is None:
                proc = subprocess.run([sys.executable, "-B", os.path.abspath(__file__)],
                                      capture_output=True, text=True)
                problems = [] if proc.returncode == USAGE_EXIT else [
                    "exit %s != %s" % (proc.returncode, USAGE_EXIT)]
                result = None
            else:
                directory = _init_repo()
                report, repo, branch, expect = builder(directory)
                result = check_report(report, repo, branch)
                problems = _expect(result, expect)
        except Exception as exc:  # fixture construction failure is a fixture failure
            problems = ["fixture raised %s: %s" % (type(exc).__name__, exc)]
            result = None
        finally:
            if directory:
                shutil.rmtree(directory, ignore_errors=True)
        if problems:
            failures.append((name, problems))
            print("FAIL %s: %s" % (name, "; ".join(problems)))
            if result is not None:
                for line in result.lines:
                    print("     | %s" % line)
                print("     | %s (exit %d)" % (result.summary, result.exit_code))
        else:
            passed += 1
            print("PASS %s" % name)
    total = len(fixtures)
    print("selftest %d/%d" % (passed, total))
    return 0 if passed == total else 1


# ------------------------------------------------------------------------------ main

def build_parser():
    parser = argparse.ArgumentParser(
        prog="landed_check.py",
        description="Check that every commit hash a report cites is an ancestor of a branch.",
        add_help=True,
    )
    parser.add_argument("--report", help="report markdown to scan")
    parser.add_argument("--repo", help="git directory (worktree root) to resolve hashes in")
    parser.add_argument("--branch", help="branch (or revision) the hashes must be ancestors of")
    parser.add_argument("--selftest", action="store_true", help="run the built-in fixtures")
    return parser


def main(argv):
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return USAGE_EXIT if exc.code not in (0, None) else 0

    if args.selftest:
        return selftest()

    missing = [flag for flag, value in (("--report", args.report), ("--repo", args.repo),
                                        ("--branch", args.branch)) if not value]
    if missing:
        sys.stderr.write("usage error: missing %s\n" % ", ".join(missing))
        parser.print_usage(sys.stderr)
        return USAGE_EXIT

    result = check_report(args.report, args.repo, args.branch)
    for line in result.lines:
        print(line)
    print(result.summary)
    if result.suppressed_digests:
        sys.stderr.write("landed_check: suppressed %d digest-labelled non-commit token(s)\n"
                         % result.suppressed_digests)
    if result.error:
        sys.stderr.write("landed_check: %s\n" % result.error)
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
