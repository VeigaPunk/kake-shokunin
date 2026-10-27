#!/usr/bin/env python3
"""Append-only correction guard for knowledge files (round-60 claim C2).

Independent implementation ``ExecGuardTool2`` of contract claim C2
(``.ufo/waves/round-60/contract.md``). Read-only: every byte compared is a
committed blob read through ``git ls-tree`` / ``git cat-file``; the worktree,
the index and all external state are never touched. Inherited ``GIT_*``
variables (the ``git rev-parse --local-env-vars`` set) are scrubbed from every
git subprocess. ``--root`` must be a repository top level (checked with
``git rev-parse --show-prefix``). ``--base`` must be an ancestor of
``--revision`` (checked with ``git merge-base --is-ancestor``).

Usage:
    python3 -B scripts/append_guard.py --root <lane> --base <rev> --revision <rev>
        [--scope <glob> ...] [--json]
    python3 -B scripts/append_guard.py --selftest

Rule (contract C2), for every path P in scope that is a regular blob at base:

* P missing at revision, or not a regular blob there (symlink 120000, submodule
  160000, directory)                    -> finding ``deleted P``.
* Otherwise let B be the base lines and R the revision lines, each split on
  ``\\n`` as raw bytes (no decoding, no normalisation). If B is not an ordered
  subsequence of R                                        -> ``changed P``.
* Otherwise the unmatched R lines form maximal runs. A run after the last
  matched base line is an end-of-file append and is allowed. Every other run
  must begin with a line holding a *visible* correction tag
  ``[r<digits>-correction YYYY-MM-DD]`` — visible means outside an HTML comment
  (``<!--`` .. ``-->``) and outside a backtick code span or fence. P gets
  ``untagged_insertion P:<line>`` iff **no** alignment of B into R satisfies
  that (existential: a good alignment is enough; the tag check is folded into
  a DP over (matched base lines so far, open-run state)).

Paths new at revision are not checked; paths outside scope are not checked.

Output: one finding per line, ``<kind> <path>[:<line>]``, sorted by path, then
a summary line ``files=<n> findings=<k>`` where ``files`` counts the in-scope
paths examined at base and ``findings`` counts the finding lines (one per
flagged file in this implementation). ``--json`` replaces the text lines with
``{"files": n, "findings": k, "items": [{"kind", "path", "line"}...]}``.

Exit: 0 clean, 1 findings, 2 could-not-evaluate (root not a top level, base or
revision unresolvable, base not an ancestor of revision, git unreadable),
64 usage. ``--selftest`` builds throwaway fixture repositories under
``$TMPDIR`` (git init, selftest identity) and asserts exit code plus finding
kind/path on >= 24 cases including all contract K-cases; exits 0 iff all pass.

Lane readings where the contract leaves a point open
----------------------------------------------------
* ``files=<n>`` counts files *examined* (in-scope regular blobs at base),
  contract says only that the summary carries both fields.
* ``untagged_insertion`` reports the 1-based revision line of the first
  non-EOF run lacking a visible tag in the leftmost (earliest-match)
  embedding; the contract pins only kind + path.
* A tag counts when it appears anywhere on the run's first line outside
  masked regions, even after other text (K2's ``**[r60-correction ...]**``).
* Comment masking is file-wide (a comment may open in a base line and be
  closed by the first inserted line, making a later tag on that line visible),
  and comment delimiters inside code spans/fences are literal text.
* Backtick code spans pair runs of *equal* backtick length (CommonMark); an
  unmatched run is literal text. Lines that are backtick fences (>= 3
  backticks, optionally indented <= 3 spaces) mask their whole region, so a
  tag inside a fenced block is not visible.
* An untagged run may still close as an end-of-file append: open-run state is
  accepted when no base lines remain unmatched.
* ``corpus/knowledge/**/*.md`` uses ``**`` that crosses zero or more
  directories, so ``corpus/knowledge/x.md`` and
  ``corpus/knowledge/sub/x.md`` both match.
* A bare repository is a valid ``--root`` (``--show-prefix`` is empty there);
  a subdirectory of a worktree is not.

Python 3.10+, standard library only.
"""
from __future__ import annotations

import argparse
import bisect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

if sys.version_info < (3, 10):
    sys.stderr.write("append_guard: python >= 3.10 required\n")
    raise SystemExit(64)

TOOL_NAME = "append_guard.py"
DEFAULT_SCOPE = ("corpus/knowledge/**/*.md",)
TAG_RE = re.compile(rb"\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]")

# ``git rev-parse --local-env-vars``: inherited names that would let the
# caller point the subprocess at a different repository than --root.
GIT_LOCAL_ENV = (
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_CONFIG", "GIT_CONFIG_PARAMETERS",
    "GIT_CONFIG_COUNT", "GIT_OBJECT_DIRECTORY", "GIT_DIR", "GIT_WORK_TREE",
    "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_INDEX_FILE",
    "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE", "GIT_PREFIX",
    "GIT_SHALLOW_FILE", "GIT_COMMON_DIR",
)
GIT_SUBPROCESS_ENV = {k: v for k, v in os.environ.items() if k not in GIT_LOCAL_ENV}

REGULAR_MODES = frozenset((b"100644", b"100755"))
def split_lines(data: bytes) -> list:
    """Lines split on ``\\n`` as bytes. The trailing empty element a final
    newline produces is a separator artefact, not a line; dropping it is the
    only reading under which an appended line after the last real base line
    is an end-of-file append (contract K1)."""
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    return lines





class GuardError(Exception):
    """Could-not-evaluate condition (exit 2)."""


# --------------------------------------------------------------------------
# git plumbing (committed bytes only)
# --------------------------------------------------------------------------

def _git(root: bytes, args, *, check: bool = True) -> subprocess.CompletedProcess:
    try:
        done = subprocess.run(
            [b"git", b"-C", root] + list(args),
            env=GIT_SUBPROCESS_ENV,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise GuardError(f"git_unavailable: {type(exc).__name__}") from exc
    if check and done.returncode != 0:
        raise GuardError(
            "git_command_failed: " + " ".join(os.fsdecode(a) for a in args[:2]))
    return done


def require_toplevel(root: str) -> bytes:
    """Resolve --root to absolute bytes and require a repository top level."""
    root_b = os.fsencode(os.path.abspath(root))
    done = _git(root_b, [b"rev-parse", b"--show-prefix"], check=False)
    if done.returncode != 0 or done.stdout.rstrip(b"\n"):
        raise GuardError("root_not_toplevel: " + root)
    return root_b


def resolve_commit(root: bytes, rev: str, what: str) -> bytes:
    done = _git(
        root_b(root), [b"rev-parse", b"--verify", b"--quiet",
                       os.fsencode(rev + "^{commit}")],
        check=False)
    if done.returncode != 0:
        raise GuardError(f"{what}_unresolvable: {rev}")
    return done.stdout.strip()


def root_b(root) -> bytes:  # small helper so resolve_commit stays readable
    return root if isinstance(root, bytes) else os.fsencode(root)


def is_ancestor(root: bytes, base: bytes, rev: bytes) -> bool:
    done = _git(root, [b"merge-base", b"--is-ancestor", base, rev], check=False)
    return done.returncode == 0


def list_tree(root: bytes, commit: bytes) -> dict:
    """path (str) -> (mode bytes, oid bytes, type bytes) for the whole tree."""
    done = _git(root, [b"ls-tree", b"-rz", b"-t", commit])
    entries = {}
    for record in done.stdout.split(b"\0"):
        if not record:
            continue
        meta, sep, raw_path = record.partition(b"\t")
        if not sep:
            raise GuardError("ls-tree_parse_error")
        fields = meta.split()
        if len(fields) < 3:
            raise GuardError("ls-tree_parse_error")
        mode, kind, oid = fields[0], fields[1], fields[2]
        entries[os.fsdecode(raw_path)] = (mode, oid, kind)
    return entries


def read_blob(root: bytes, oid: bytes) -> bytes:
    return _git(root, [b"cat-file", b"blob", oid]).stdout


# --------------------------------------------------------------------------
# scope globbing
# --------------------------------------------------------------------------

def glob_to_regex(pattern: str) -> re.Pattern:
    """POSIX-path glob where ``**`` crosses zero or more directories."""
    out = ["(?:", ]
    i, n = 0, len(pattern)
    while i < n:
        c = pattern[i]
        if c == "*":
            if pattern[i + 1:i + 2] == "*":
                # ``**/`` also matches the empty prefix; a bare ``**`` matches
                # any run of characters.
                if pattern[i + 2:i + 3] == "/":
                    out.append("(?:[^/]*/)*")
                    i += 3
                else:
                    out.append(".*")
                    i += 2
            else:
                out.append("[^/]*")
                i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        elif c == "[":
            j = i + 1
            if pattern[j:j + 1] in ("!", "^"):
                j += 1
            if pattern[j:j + 1] == "]":
                j += 1
            while j < n and pattern[j] != "]":
                j += 1
            if j >= n:
                out.append("\\[")
                i += 1
            else:
                body = pattern[i + 1:j]
                if body.startswith("!"):
                    body = "^" + body[1:]
                out.append("[" + body + "]")
                i = j + 1
        else:
            out.append(re.escape(c))
            i += 1
    out.append(")")
    return re.compile("".join(out) + r"\Z", re.DOTALL)


def in_scope(path: str, matchers) -> bool:
    return any(m.match(path) for m in matchers)


# --------------------------------------------------------------------------
# visibility: HTML comments, backtick code spans and fences
# --------------------------------------------------------------------------

def visibility_mask(text: bytes) -> bytearray:
    """bytearray: 1 where a tag regex match would NOT be visible.

    Regions marked: fenced code blocks (whole lines that are backtick fences),
    backtick code spans (equal-length run pairs, CommonMark style, may span
    lines), and HTML comments (``<!--`` .. ``-->``). Comment delimiters inside
    code regions are literal; backtick runs inside comments are literal.
    """
    mask = bytearray(len(text))
    n = len(text)

    # Pass 1 — fenced code blocks. A fence line begins with <= 3 spaces then
    # >= 3 backticks; the closing fence line ends the region.
    in_fence = False
    pos = 0
    while pos <= n:
        end = text.find(b"\n", pos)
        if end == -1:
            end = n
        stripped = pos
        pad = 0
        while stripped < end and text[stripped:stripped + 1] == b" " and pad < 4:
            stripped += 1
            pad += 1
        bt = 0
        while stripped + bt < end and text[stripped + bt:stripped + bt + 1] == b"`":
            bt += 1
        is_fence = (pad <= 3 and bt >= 3 and
                    (in_fence or text[stripped + bt:end].find(b"`") == -1))
        if in_fence or is_fence:
            for k in range(pos, min(end + 1, n)):
                mask[k] = 1
            if is_fence:
                in_fence = not in_fence
        pos = end + 1

    # Pass 2 — backtick code spans on unmasked bytes. Runs of equal length
    # pair; the first later equal run closes. Unmatched runs are literal.
    runs = []
    pos = 0
    while pos < n:
        if mask[pos] or text[pos:pos + 1] != b"`":
            pos += 1
            continue
        end = pos
        while end < n and text[end:end + 1] == b"`":
            end += 1
        runs.append((pos, end))
        pos = end
    used = [False] * len(runs)
    for a, (s, e) in enumerate(runs):
        if used[a] or mask[s]:
            continue
        length = e - s
        for b in range(a + 1, len(runs)):
            s2, e2 = runs[b]
            if mask[s2]:
                continue
            if e2 - s2 == length:
                for k in range(s, e2):
                    mask[k] = 1
                used[b] = True
                break
        # no closer -> opener stays literal text

    # Pass 3 — HTML comments over unmasked bytes.
    pos = 0
    comment_start = -1
    while pos < n:
        if mask[pos]:
            pos += 1
            continue
        if comment_start < 0 and text.startswith(b"<!--", pos):
            comment_start = pos
            pos += 4
            continue
        if comment_start >= 0 and text.startswith(b"-->", pos):
            for k in range(comment_start, pos + 3):
                mask[k] = 1
            comment_start = -1
            pos += 3
            continue
        pos += 1
    if comment_start >= 0:
        for k in range(comment_start, n):
            mask[k] = 1
    return mask


def tagged_lines(text: bytes) -> set:
    """0-based revision line indexes holding >= 1 fully visible tag."""
    mask = visibility_mask(text)
    starts = [0]
    pos = text.find(b"\n")
    while pos != -1:
        starts.append(pos + 1)
        pos = text.find(b"\n", pos + 1)
    tagged = set()
    for m in TAG_RE.finditer(text):
        if any(mask[m.start():m.end()]):
            continue
        tagged.add(bisect.bisect_right(starts, m.start()) - 1)
    return tagged


# --------------------------------------------------------------------------
# alignment: subsequence check + existential tag DP (bitset over base lines)
# --------------------------------------------------------------------------

def is_subsequence(base_lines, rev_lines) -> bool:
    it = iter(rev_lines)
    try:
        for b in base_lines:
            while next(it) != b:
                pass
    except StopIteration:
        return False
    return True


def clean_alignment_exists(base_lines, rev_lines, tagged) -> bool:
    """Existential rule: some embedding of B into R where every non-EOF
    inserted run begins with a tagged line.

    Bitset DP over (base lines consumed, open-run mode): mode 0 = at a
    matched line / no open run, 1 = inside a run whose first line is tagged,
    2 = inside a run whose first line is untagged. An open mode-2 run can
    only continue (never match again); it is accepted only if it reaches
    end-of-file, i.e. it is the trailing append. O(nR * nB/word) time.
    """
    n_b = len(base_lines)
    if n_b == 0:
        return True  # no matched base lines -> everything is an EOF append
    # bit i of posmap[line] is set when base_lines[i] == line
    posmap = {}
    for i, b in enumerate(base_lines):
        posmap[b] = posmap.get(b, 0) | (1 << i)
    s0, s1, s2 = 1, 0, 0
    for j, line in enumerate(rev_lines):
        tagged_mask = -1 if j in tagged else 0  # all-ones when visible tag
        # consume as an inserted line: continue an open run with its mode,
        # or open a new run from mode 0 with this line's tag state.
        i1 = s1 | (s0 & tagged_mask)
        i2 = s2 | (s0 & ~tagged_mask)
        # match to the next base line (allowed from modes 0 and 1 only):
        matchable = posmap.get(line, 0)
        frontier = (s0 | s1)
        m = (frontier & matchable) << 1
        s0, s1, s2 = m, i1, i2
    top = 1 << n_b
    return bool((s0 | s1 | s2) & top)


def first_bad_run_line(base_lines, rev_lines, tagged) -> int:
    """1-based revision line of the first non-EOF run without a visible tag
    under the leftmost (earliest-match) embedding. Only called when
    ``clean_alignment_exists`` rejected, so such a run exists."""
    positions = {}
    for j, line in enumerate(rev_lines):
        positions.setdefault(line, []).append(j)
    matched = []
    cursor = 0
    for b in base_lines:
        idxs = positions.get(b, [])
        k = bisect.bisect_left(idxs, cursor)
        j = idxs[k]  # subsequence already proven -> k < len(idxs)
        matched.append(j)
        cursor = j + 1
    prev = -1
    for j in matched:
        gap_start = prev + 1
        if gap_start < j and gap_start not in tagged:
            return gap_start + 1
        prev = j
    return max(1, matched[-1] + 1) if matched else 1


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def evaluate(root: bytes, base: bytes, revision: bytes, matchers):
    """Return (findings, files_examined); findings = [(kind, path, line|None)]."""
    base_tree = list_tree(root, base)
    rev_tree = list_tree(root, revision)
    findings = []
    examined = 0
    for path in sorted(base_tree):
        mode, oid, kind = base_tree[path]
        if kind != b"blob" or mode not in REGULAR_MODES:
            continue  # rule applies only to paths that are regular blobs at base
        if not in_scope(path, matchers):
            continue
        examined += 1
        entry = rev_tree.get(path)
        if entry is None or entry[2] != b"blob" or entry[0] not in REGULAR_MODES:
            findings.append(("deleted", path, None))
            continue
        base_bytes = read_blob(root, oid)
        rev_bytes = read_blob(root, entry[1])
        if base_bytes == rev_bytes:
            continue
        base_lines = split_lines(base_bytes)
        rev_lines = split_lines(rev_bytes)
        if not is_subsequence(base_lines, rev_lines):
            findings.append(("changed", path, None))
            continue
        tagged = tagged_lines(rev_bytes)
        if clean_alignment_exists(base_lines, rev_lines, tagged):
            continue
        findings.append(("untagged_insertion", path,
                         first_bad_run_line(base_lines, rev_lines, tagged)))
    return findings, examined


def render_text(findings, examined) -> str:
    out = []
    for kind, path, line in sorted(findings, key=lambda f: f[1]):
        out.append(f"{kind} {path}" + (f":{line}" if line is not None else ""))
    out.append(f"files={examined} findings={len(findings)}")
    return "\n".join(out) + "\n"


def render_json(findings, examined) -> str:
    items = [{"kind": k, "path": p, "line": l} for k, p, l in
             sorted(findings, key=lambda f: f[1])]
    return json.dumps({"files": examined, "findings": len(findings),
                       "items": items}, indent=2, sort_keys=True) + "\n"


# --------------------------------------------------------------------------
# selftest: gate-style fixture repositories
# --------------------------------------------------------------------------

SELFTEST_ENV = {k: v for k, v in GIT_SUBPROCESS_ENV.items()
                if k not in ("HOME",)}
SELFTEST_ENV["GIT_CONFIG_NOSYSTEM"] = "1"


def _st_git(repo: str, args, env, check: bool = True):
    done = subprocess.run(["git", "-C", repo] + args, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and done.returncode != 0:
        raise RuntimeError(f"fixture git {args[:2]} failed: {done.stderr!r}")
    return done


def _st_commit(repo: str, files: dict, env):
    """Sync the worktree to exactly ``files`` and commit (or reuse HEAD)."""
    tracked = _st_git(repo, ["ls-files", "-z"], env).stdout.split(b"\0")
    wanted = set(files)
    for raw in tracked:
        if raw and os.fsdecode(raw) not in wanted:
            os.unlink(os.path.join(repo, os.fsdecode(raw)))
    for rel, data in files.items():
        target = os.path.join(repo, rel)
        if isinstance(data, tuple) and data[0] == "symlink":
            if os.path.lexists(target):
                os.unlink(target)
            os.symlink(data[1], target)
        else:
            os.makedirs(os.path.dirname(target) or repo, exist_ok=True)
            with open(target, "wb") as fh:
                fh.write(data)
    _st_git(repo, ["add", "-A"], env)
    staged = _st_git(repo, ["write-tree"], env).stdout.strip()
    have_head = _st_git(repo, ["rev-parse", "--verify", "-q", "HEAD"],
                        env, check=False).returncode == 0
    head_tree = (_st_git(repo, ["rev-parse", "HEAD^{tree}"], env)
                 .stdout.strip() if have_head else b"")
    if staged != head_tree:
        _st_git(repo, ["-c", "user.name=selftest", "-c",
                       "user.email=selftest@local", "commit", "-q", "-m", "c"],
                env)
    top = _st_git(repo, ["rev-parse", "--show-toplevel"], env).stdout
    if top.strip() != os.fsencode(os.path.realpath(repo)):
        raise RuntimeError("fixture toplevel mismatch")
    return _st_git(repo, ["rev-parse", "HEAD"], env).stdout.strip()


def _st_repo(work: str, name: str, base_files: dict, rev_files, env):
    repo = os.path.join(work, name)
    os.makedirs(repo)
    _st_git(repo, ["init", "-q"], env)
    base = _st_commit(repo, base_files, env)
    if isinstance(rev_files, dict):
        rev = os.fsdecode(_st_commit(repo, rev_files, env))
    else:
        rev = rev_files  # explicit revision spec (string) or None
    return repo, os.fsdecode(base), rev


def run_selftest(argv) -> int:
    KN = "corpus/knowledge/note.md"
    TAG = "[r60-correction 2026-10-27]"
    BASE = {KN: b"alpha\nbeta\ngamma\ndelta\n",
            "SKILL.md": b"# skill\n"}

    cases = []  # (id, builder-or-args, expected_exit, expected_findings)

    def repo_case(cid, base_files, rev_files, expect_exit, expect_findings,
                  extra=None, base_rev=None, rev_rev=None):
        cases.append((cid, base_files, rev_files, expect_exit,
                      expect_findings, extra or [], base_rev, rev_rev))

    A, B, C, D = b"alpha\n", b"beta\n", b"gamma\n", b"delta\n"

    repo_case("K1", BASE, {KN: b"alpha\nbeta\ngamma\ndelta\nnew line\n"},
              0, [])
    repo_case("K2", BASE,
              {KN: b"alpha\nbeta\n**" + TAG.encode() + b"** fix\nmore\ngamma\ndelta\n"},
              0, [])
    repo_case("K3", BASE,
              {KN: b"alpha\nbeta\nuntagged1\nuntagged2\ngamma\ndelta\n"},
              1, [("untagged_insertion", KN)])
    repo_case("K4", BASE, {KN: b"alpha\nb3ta\ngamma\ndelta\n"},
              1, [("changed", KN)])
    repo_case("K5", BASE, {KN: b"alpha\ngamma\ndelta\n"}, 1, [("changed", KN)])
    repo_case("K6", BASE, {"SKILL.md": b"# skill\n"}, 1, [("deleted", KN)])
    repo_case("K7", BASE,
              {"corpus/knowledge/renamed.md": b"alpha\nbeta\ngamma\ndelta\n",
               "SKILL.md": b"# skill\n"},
              1, [("deleted", KN)])
    repo_case("K8", BASE,
              {KN: b"alpha\nbeta\nplain\n" + TAG.encode() + b"\ngamma\ndelta\n"},
              1, [("untagged_insertion", KN)])
    repo_case("K9", BASE,
              {KN: b"alpha\nbeta\n<!-- " + TAG.encode() + b" -->\ngamma\ndelta\n"},
              1, [("untagged_insertion", KN)])
    repo_case("K10", BASE,
              {KN: b"alpha\nbeta\nnote `" + TAG.encode() + b"` tail\ngamma\ndelta\n"},
              1, [("untagged_insertion", KN)])
    repo_case("K11", BASE,
              dict(BASE, **{"corpus/knowledge/new.md": b"fresh\n"}), 0, [])
    repo_case("K12", BASE, {KN: b"beta\nalpha\ngamma\ndelta\n"},
              1, [("changed", KN)])
    repo_case("K13", BASE, {KN: b"alpha \nbeta\ngamma\ndelta\n"},
              1, [("changed", KN)])
    repo_case("K14", BASE, {KN: b"alpha\r\nbeta\r\ngamma\r\ndelta\r\n"},
              1, [("changed", KN)])
    repo_case("K15", {"corpus/knowledge/csv.md": b'a\n""\nb\n'},
              {"corpus/knowledge/csv.md": b'a\n' + TAG.encode() + b'\n""\n""\nb\n'},
              0, [])
    repo_case("K16", {"corpus/knowledge/dup.md": b"a\nb\nc\n"},
              {"corpus/knowledge/dup.md": b"a\nb\nb\nc\n"},
              1, [("untagged_insertion", "corpus/knowledge/dup.md")])
    repo_case("K17", BASE,
              {KN: b"alpha\nbeta\ngamma\ndelta\n", "SKILL.md": b"# rewritten\n"},
              0, [])
    repo_case("K18", BASE, {KN: ("symlink", "note-target"),
                            "SKILL.md": b"# skill\n"},
              1, [("deleted", KN)])
    repo_case("K19", BASE,
              {KN: b"alpha\nbeta\ngamma\ndelta\n\xff\xfe"}, 0, [])
    # K20: base is the LATER commit -> not an ancestor -> 2.
    repo_case("K20", BASE, {KN: b"alpha\nbeta\ngamma\ndelta\nnew\n"},
              2, None, base_rev="HEAD", rev_rev="HEAD~1")
    cases.append(("K21", "ARGS", ["--root"], 64, None))
    repo_case("K22", {"corpus/knowledge/sub/deep.md": b"x\ny\n"},
              {"corpus/knowledge/sub/deep.md": b"x\nZ\n"},
              1, [("changed", "corpus/knowledge/sub/deep.md")])

    # --- extra cases beyond the contract K-table -------------------------
    repo_case("E1", BASE,
              {KN: b"alpha\nbeta\n```\n" + TAG.encode() + b"\n```\ngamma\ndelta\n"},
              1, [("untagged_insertion", KN)])
    repo_case("E2", BASE,
              {KN: b"alpha\nbeta\nintro " + TAG.encode() + b" tail\nbody\ngamma\ndelta\n"},
              0, [])
    repo_case("E3", {"corpus/knowledge/c.md": b"open\n<!-- hidden\nbase\n"},
              {"corpus/knowledge/c.md":
               b"open\n<!-- hidden\nbase\n--> " + TAG.encode() + b"\nmore\n"},
              0, [])
    repo_case("E4", {"corpus/knowledge/empty.md": b""},
              {"corpus/knowledge/empty.md": b"any\ncontent\n"}, 0, [])
    repo_case("E5", BASE,
              {KN: b"alpha\n" + TAG.encode() + b"\nfix\nbeta\nbad1\nbad2\ngamma\ndelta\n"},
              1, [("untagged_insertion", KN)])
    repo_case("E6", BASE,
              {KN: b"alpha\nbeta\nx1\n" + TAG.encode() + b"\nx2\ngamma\ndelta\n"},
              1, [("untagged_insertion", KN)])
    repo_case("E7", BASE, {KN: b"alpha\nbeta\nuntagged\ngamma\ndelta\n"},
              0, [], extra=["--scope", "other/**/*.md"])
    repo_case("E8", BASE, dict(BASE), 0, [])  # base == revision content
    repo_case("E9", BASE, {KN: b"alpha\nbeta\n[r60-correction 2026-13-40]\ngamma\ndelta\n"},
              0, [])  # literal regex: months are not validated
    repo_case("E10", BASE, {KN: b"alpha\nbeta\n" + TAG.encode() + b"\nlead\nbody\ngamma\ndelta\n"},
              0, [])  # tag first, then untagged body lines: still clean
    cases.append(("E11", "ARGS", ["--root", "{repo}", "--base", "{base}",
                                  "--revision", "{rev}", "--json"], 0, "JSON"))
    cases.append(("E12", "ARGS", ["--root", "{repo}/corpus", "--base",
                                  "{base}", "--revision", "{rev}"], 2, None))
    cases.append(("E13", "ARGS", ["--root", "{repo}", "--base", "{base}",
                                  "--revision", "deadbeef" * 5], 2, None))
    cases.append(("E14", "ARGS", ["--root", "{repo}", "--base", "{base}",
                                  "--revision", "{rev}", "--bogus"], 64, None))

    work = tempfile.mkdtemp(prefix="append_guard_selftest_")
    env = dict(SELFTEST_ENV)
    env["HOME"] = work
    env["TMPDIR"] = work
    script = os.path.abspath(__file__)
    passed = failed = 0
    try:
        for entry in cases:
            cid, base_files = entry[0], entry[1]
            if base_files == "ARGS":
                _, _, args_tpl, expect, expect_findings = entry
                repo, base, rev = _st_repo(work, "argrepo_" + cid.lower(),
                                           BASE, dict(BASE), env)
                args = [a.format(repo=repo, base=base, rev=rev)
                        for a in args_tpl]
            else:
                _, bf, rf, expect, expect_findings, extra, base_rev, rev_rev = \
                    entry
                repo, base, rev = _st_repo(
                    work, "repo_" + cid.lower(), bf, rf, env)
                args = ["--root", repo, "--base", base_rev or base,
                        "--revision", rev_rev or rev] + extra
            done = subprocess.run(
                [sys.executable, "-B", script] + args,
                env=env, cwd=work, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            ok = done.returncode == expect
            if ok and expect_findings not in (None, "JSON"):
                lines = [l for l in done.stdout.decode("utf-8", "replace")
                         .splitlines() if l and not l.startswith("files=")]
                got = []
                for l in lines:
                    parts = l.split(" ", 1)
                    p = parts[1].split(":")[0]
                    got.append((parts[0], p))
                ok = got == list(expect_findings)
            if ok and expect_findings == "JSON":
                payload = json.loads(done.stdout)
                ok = (payload.get("files") == 1
                      and payload.get("findings") == 0)
            status = "PASS" if ok else "FAIL"
            if ok:
                passed += 1
            else:
                failed += 1
            sys.stdout.write(
                f"{status} {cid}: exit={done.returncode} want={expect}\n")
            if not ok:
                sys.stdout.write(
                    f"  stdout={done.stdout[:400]!r}\n"
                    f"  stderr={done.stderr[:400]!r}\n")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    sys.stdout.write(f"selftest: {passed} passed, {failed} failed, "
                     f"{len(cases)} cases\n")
    return 0 if failed == 0 else 1


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

class UsageParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        sys.stderr.write(f"{TOOL_NAME}: error: {message}\n")
        raise SystemExit(64)


def build_parser() -> UsageParser:
    p = UsageParser(prog=TOOL_NAME, description=__doc__.split("\n")[0])
    p.add_argument("--root")
    p.add_argument("--base")
    p.add_argument("--revision")
    p.add_argument("--scope", action="append", default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--selftest", action="store_true")
    return p


def main(argv) -> int:
    args = build_parser().parse_args(argv)
    if args.selftest:
        return run_selftest(argv)
    if not args.root or not args.base or not args.revision:
        sys.stderr.write(f"{TOOL_NAME}: --root, --base and --revision "
                         "are required\n")
        return 64
    try:
        root = require_toplevel(args.root)
        base = resolve_commit(root, args.base, "base")
        revision = resolve_commit(root, args.revision, "revision")
        if not is_ancestor(root, base, revision):
            raise GuardError("base_not_ancestor")
        matchers = [glob_to_regex(g) for g in (args.scope or DEFAULT_SCOPE)]
        findings, examined = evaluate(root, base, revision, matchers)
    except GuardError as exc:
        sys.stderr.write(f"{TOOL_NAME}: {exc}\n")
        return 2
    sys.stdout.write(render_json(findings, examined) if args.json
                     else render_text(findings, examined))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
