#!/usr/bin/env python3
"""append_guard.py — append-only correction guard for lane knowledge files.

Round-60 claim C2 surface (contract): a read-only tool that compares the
committed bytes of every in-scope regular blob at --base against --revision.

Rule per path P in scope that is a regular blob at base:
  * P missing at revision or not a regular blob there -> `deleted P`.
  * B = base lines, R = revision lines, split on b"\\n" as raw bytes with no
    decoding and no normalisation (a file ending in b"\\n" has no trailing
    empty line).  If B is not an ordered subsequence of R -> `changed P`.
  * Otherwise the unmatched R positions form maximal inserted runs.  A run
    after the last matched base line is an end-of-file append (allowed).
    Every other run must begin with a line holding a visible correction tag
    `\\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\\]` — visible means the
    match does not start inside an HTML comment (comment state is tracked
    across lines) and does not start inside a backtick code span (code spans
    are matched per line, opener and closer of equal backtick length).
    `untagged_insertion P:<line>` is reported iff NO alignment of B into R
    makes every non-EOF run begin with a tagged line — an existential rule,
    decided by DP over (base index, in-run state); <line> is the 1-based
    revision line of the first bad run of the leftmost alignment.

Exits: 0 clean, 1 findings, 2 could-not-evaluate (root not a repository
toplevel, revision unresolved, base not an ancestor of revision), 64 usage.
Committed bytes only: every read goes through `git ls-tree` / `git cat-file`;
the worktree is never touched and inherited GIT_* variables are scrubbed.
Stdlib only, python3 >= 3.10.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TAG_RE = re.compile(rb"\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]")
DEFAULT_SCOPE = ["corpus/knowledge/**/*.md"]
BLOB_MODES = {"100644", "100755"}
SUBMODULE_MODE = "160000"


# --------------------------------------------------------------------------- git plumbing

def _env() -> dict:
    env = os.environ.copy()
    for k in [k for k in env if k.startswith("GIT_")]:
        del env[k]
    return env


def git(root: str, *args: str) -> tuple[int, bytes]:
    proc = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=_env())
    return proc.returncode, proc.stdout


def toplevel(root: str) -> str | None:
    rc, out = git(root, "rev-parse", "--show-toplevel")
    if rc != 0:
        return None
    try:
        t = os.path.realpath(out.decode("utf-8", "surrogateescape").strip())
    except OSError:
        return None
    return t


def resolve(root: str, rev: str) -> str | None:
    rc, out = git(root, "rev-parse", "--verify", "--quiet", "--end-of-options",
                  f"{rev}^{{commit}}")
    if rc != 0:
        return None
    try:
        return out.decode("ascii").strip()
    except UnicodeDecodeError:
        return None


def is_ancestor(root: str, base: str, rev: str) -> bool:
    proc = subprocess.run(["git", "-C", root, "merge-base", "--is-ancestor",
                           "--", base, rev], env=_env())
    return proc.returncode == 0


def tree_entries(root: str, rev: str) -> dict[str, tuple[str, str]] | None:
    """path -> (mode, oid) for every blob/link/submodule at rev (recursive)."""
    rc, out = git(root, "ls-tree", "-r", rev)
    if rc != 0:
        return None
    entries: dict[str, tuple[str, str]] = {}
    for line in out.split(b"\n"):
        if not line:
            continue
        meta, _, path = line.partition(b"\t")
        mode, _, rest = meta.partition(b" ")
        _type, _, oid = rest.partition(b" ")
        entries[os.fsdecode(path)] = (os.fsdecode(mode), os.fsdecode(oid))
    return entries


def blob_bytes(root: str, oid: str) -> bytes | None:
    rc, out = git(root, "cat-file", "blob", oid)
    return out if rc == 0 else None


# --------------------------------------------------------------------------- line and scope model

def split_lines(content: bytes) -> list[bytes]:
    """Lines separated by b'\\n'; a trailing newline adds no empty line."""
    parts = content.split(b"\n")
    if parts and parts[-1] == b"":
        parts.pop()
    return parts


def scope_regex(pattern: str) -> re.Pattern:
    """fnmatch translation with `**` as cross-directory recursion."""
    out: list[str] = []
    i, n = 0, len(pattern)
    while i < n:
        c = pattern[i]
        if c == "*":
            if pattern.startswith("**/", i):
                out.append("(?:.*/)?")
                i += 3
            elif pattern.startswith("**", i):
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
            if j < n and pattern[j] == "!":
                j += 1
            if j < n and pattern[j] == "]":
                j += 1
            while j < n and pattern[j] != "]":
                j += 1
            if j >= n:
                out.append("\\[")
                i += 1
            else:
                stuff = pattern[i + 1:j].replace("\\", "\\\\")
                if pattern[i + 1] == "!":
                    stuff = "^" + stuff[1:]
                out.append("[" + stuff + "]")
                i = j + 1
        else:
            out.append(re.escape(c))
            i += 1
    return re.compile("(?s)" + "".join(out) + "\\Z")


def in_scope(path: str, scopes: list[re.Pattern]) -> bool:
    return any(rx.match(path) for rx in scopes)


# --------------------------------------------------------------------------- tag visibility

def _masked_ranges(line: bytes, comment_open: bool) -> tuple[bytes, bool]:
    """Visibility mask for one line; returns (mask, comment_open_after).

    mask[i] is b'\\x01' where the character is hidden by an HTML comment
    (state carried across lines) or by a same-line backtick code span.
    """
    n = len(line)
    mask = bytearray(n)
    i = 0
    in_comment = comment_open
    while i < n:
        if in_comment:
            c = line.find(b"-->", i)
            if c < 0:
                for k in range(i, n):
                    mask[k] = 1
                return bytes(mask), True
            for k in range(i, c + 3):
                mask[k] = 1
            i = c + 3
            in_comment = False
            continue
        b = line.find(b"`", i)
        c = line.find(b"<!--", i)
        if b >= 0 and (c < 0 or b < c):
            j = b + 1
            while j < n and line[j] == 0x60:  # '`'
                j += 1
            blen = j - b
            closer = line.find(b"`" * blen, j)
            if closer >= 0:
                for k in range(b, closer + blen):
                    mask[k] = 1
                i = closer + blen
            else:
                i = j  # unclosed backtick run is literal text
        elif c >= 0:
            e = line.find(b"-->", c)
            if e < 0:
                for k in range(c, n):
                    mask[k] = 1
                return bytes(mask), True
            for k in range(c, e + 3):
                mask[k] = 1
            i = e + 3
        else:
            break
    return bytes(mask), in_comment


def visibility_masks(lines: list[bytes]) -> list[bytes]:
    masks: list[bytes] = []
    comment_open = False
    for line in lines:
        mask, comment_open = _masked_ranges(line, comment_open)
        masks.append(mask)
    return masks


def line_is_tagged(line: bytes, mask: bytes) -> bool:
    """A tag on this line whose match does not start inside a hidden region."""
    for m in TAG_RE.finditer(line):
        if not mask[m.start()]:
            return True
    return False


# --------------------------------------------------------------------------- alignment

def leftmost_alignment(base: list[bytes], rev: list[bytes]) -> list[int] | None:
    """Greedy earliest-index subsequence match; None if B is not a subsequence."""
    out: list[int] = []
    j = 0
    n = len(rev)
    for line in base:
        while j < n and rev[j] != line:
            j += 1
        if j == n:
            return None
        out.append(j)
        j += 1
    return out


def first_untagged_run(rev: list[bytes], tagged: list[bool],
                       match: list[int]) -> int | None:
    """0-based index of the first line of the first non-EOF run that does not
    begin with a tagged line under the given alignment; None if all runs pass."""
    matched = set(match)
    last = match[-1] if match else -1
    j, n = 0, len(rev)
    while j < n:
        if j in matched:
            j += 1
            continue
        start = j
        while j < n and j not in matched:
            j += 1
        if start > last:  # run after the last matched base line -> EOF append
            continue
        if not tagged[start]:
            return start
    return None


def any_clean_alignment(base: list[bytes], rev: list[bytes],
                        tagged: list[bool]) -> bool:
    """Existential rule: True iff some alignment of B into R has every non-EOF
    run beginning with a tagged line.

    DP over states (i, in_run) while consuming rev left to right:
      * match    (i < m and r == B[i])  -> (i + 1, False)
      * insert   -> (i, True), allowed when
          - in_run            (continuing a run: interior lines are free), or
          - i == m            (every base line consumed: the run sits after the
                               last matched base line -> EOF append), or
          - r starts a run and is tagged.
    An empty base has no "last matched base line", so its run is an append
    (the byte-prefix rule's B == b"" special case).
    """
    m = len(base)
    states = {(0, False)}
    for j, r in enumerate(rev):
        nxt: set[tuple[int, bool]] = set()
        for i, in_run in states:
            if i < m and r == base[i]:
                nxt.add((i + 1, False))
            if in_run or i == m or tagged[j]:
                nxt.add((i, True))
        states = nxt
        if not states:
            return False
    return any(i == m for i, _ in states)


# --------------------------------------------------------------------------- measure

def evaluate(root: str, base: str, rev: str,
             scopes: list[re.Pattern]) -> tuple[int, list[tuple], int, str | None]:
    """Returns (exit, findings, files_checked, error)."""
    t = toplevel(root)
    if t is None or t != os.path.realpath(root):
        return 2, [], 0, f"--root {root} is not a repository toplevel"
    base_c = resolve(root, base)
    rev_c = resolve(root, rev)
    if base_c is None:
        return 2, [], 0, f"--base {base} does not resolve to a commit"
    if rev_c is None:
        return 2, [], 0, f"--revision {rev} does not resolve to a commit"
    if not is_ancestor(root, base_c, rev_c):
        return 2, [], 0, f"{base} is not an ancestor of {rev}"
    base_tree = tree_entries(root, base_c)
    rev_tree = tree_entries(root, rev_c)
    if base_tree is None or rev_tree is None:
        return 2, [], 0, "cannot read commit trees"
    findings: list[tuple[str, str, int | None]] = []
    files = 0
    for path in sorted(base_tree):
        mode, oid = base_tree[path]
        if mode not in BLOB_MODES or not in_scope(path, scopes):
            continue
        files += 1
        ent = rev_tree.get(path)
        if ent is None or ent[0] not in BLOB_MODES:
            findings.append(("deleted", path, None))
            continue
        bb = blob_bytes(root, oid)
        rb = blob_bytes(root, ent[1])
        if bb is None or rb is None:
            return 2, [], 0, f"cannot read blob for {path}"
        if bb == rb:
            continue
        B, R = split_lines(bb), split_lines(rb)
        match = leftmost_alignment(B, R)
        if match is None:
            findings.append(("changed", path, None))
            continue
        masks = visibility_masks(R)
        tagged = [line_is_tagged(R[j], masks[j]) for j in range(len(R))]
        if any_clean_alignment(B, R, tagged):
            continue
        bad = first_untagged_run(R, tagged, match)
        findings.append(("untagged_insertion", path,
                         (bad + 1) if bad is not None else None))
    findings.sort(key=lambda f: (f[1], f[0]))
    return (1 if findings else 0), findings, files, None


# --------------------------------------------------------------------------- output

def print_findings(findings: list[tuple], files: int) -> None:
    for kind, path, line in findings:
        suffix = f":{line}" if line is not None else ""
        print(f"{kind} {path}{suffix}")
    print(f"files={files} findings={len(findings)}")


# --------------------------------------------------------------------------- selftest

ST_TAG = "**[r60-correction 2026-10-27]**"


def _git(d: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    p = subprocess.run(["git", "-C", d, *args], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, env=_env())
    if check and p.returncode != 0:
        raise AssertionError(f"git {' '.join(args)}: {p.stderr.decode(errors='replace')}")
    return p


def _commit_all(d: str, msg: str) -> str:
    _git(d, "add", "-A")
    _git(d, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
         "commit", "--allow-empty", "-qm", msg)
    return _git(d, "rev-parse", "HEAD").stdout.decode().strip()


def _fixture(base_files: dict[str, bytes],
             ops: list[tuple] | None = None) -> tuple[str, str, str]:
    """A scratch repo with a base commit of base_files, then ops applied and a
    second commit.  ops: ('w', path, bytes) | ('rm', path) | ('mv', a, b) |
    ('ln', path, target).  Returns (dir, base_sha, rev_sha)."""
    d = tempfile.mkdtemp(prefix="ag-st-")
    _git(d, "init", "-q")
    for path, data in base_files.items():
        full = os.path.join(d, path)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "wb") as fh:
            fh.write(data)
    base = _commit_all(d, "base")
    for op in ops or []:
        if op[0] == "w":
            full = os.path.join(d, op[1])
            os.makedirs(os.path.dirname(full) or d, exist_ok=True)
            with open(full, "wb") as fh:
                fh.write(op[2])
        elif op[0] == "rm":
            os.remove(os.path.join(d, op[1]))
        elif op[0] == "mv":
            dst = os.path.join(d, op[2])
            os.makedirs(os.path.dirname(dst) or d, exist_ok=True)
            os.rename(os.path.join(d, op[1]), dst)
        elif op[0] == "ln":
            os.symlink(op[2], os.path.join(d, op[1]))
        elif op[0] == "chmod":
            os.chmod(os.path.join(d, op[1]), op[2])
    rev = _commit_all(d, "revision")
    assert _git(d, "rev-parse", "--show-toplevel").stdout.decode().strip() == \
        os.path.realpath(d), f"fixture toplevel mismatch in {d}"
    return d, base, rev


def _run(root: str, *args: str, env_extra: dict | None = None) -> tuple[int, str]:
    env = _env()
    if env_extra:
        env.update(env_extra)
    cmd = [sys.executable, "-B", os.path.abspath(__file__), "--root", root, *args]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       env=env, text=True)
    return p.returncode, p.stdout


def selftest() -> int:
    K = "corpus/knowledge/"
    base_body = b"# note\n\nalpha\nbeta\ngamma\nomega\n"
    cases: list[dict] = []

    def case(name: str, want_rc: int, want: list[tuple[str, str]] | None,
             base_files: dict[str, bytes] | None = None,
             ops: list[tuple] | None = None, argv: list | None = None,
             env: dict | None = None):
        cases.append(dict(name=name, want_rc=want_rc, want=want,
                          base_files=base_files or {K + "a.md": base_body},
                          ops=ops, argv=argv, env=env))

    # ---- contract K-cases ------------------------------------------------
    case("K1_eof_append", 0, [],
         ops=[("w", K + "a.md", base_body + b"new tail one\nnew tail two\n")])
    case("K2_tagged_midfile", 0, [],
         ops=[("w", K + "a.md",
               b"# note\n\nalpha\n" + ST_TAG.encode() + b" fix line 1\nfix line 2\nbeta\ngamma\nomega\n")])
    case("K3_untagged_midfile", 1, [("untagged_insertion", K + "a.md")],
         ops=[("w", K + "a.md", b"# note\n\nalpha\nrun1\nrun2\nbeta\ngamma\nomega\n")])
    case("K4_byte_changed", 1, [("changed", K + "a.md")],
         ops=[("w", K + "a.md", base_body.replace(b"alpha", b"alphx"))])
    case("K5_line_deleted", 1, [("changed", K + "a.md")],
         ops=[("w", K + "a.md", base_body.replace(b"beta\n", b""))])
    case("K6_file_deleted", 1, [("deleted", K + "a.md")],
         ops=[("rm", K + "a.md")])
    case("K7_file_renamed", 1, [("deleted", K + "a.md")],
         ops=[("mv", K + "a.md", K + "b.md")])
    case("K8_tag_on_second_line", 1, [("untagged_insertion", K + "a.md")],
         ops=[("w", K + "a.md",
               b"# note\n\nalpha\nlead-in\n" + ST_TAG.encode() + b" fix\nbeta\ngamma\nomega\n")])
    case("K9_tag_in_html_comment", 1, [("untagged_insertion", K + "a.md")],
         ops=[("w", K + "a.md",
               b"# note\n\nalpha\n<!-- [r60-correction 2026-10-27] -->\nfix\nbeta\ngamma\nomega\n")])
    case("K10_tag_in_code_span", 1, [("untagged_insertion", K + "a.md")],
         ops=[("w", K + "a.md",
               b"# note\n\nalpha\nsee `[r60-correction 2026-10-27]` here\nfix\nbeta\ngamma\nomega\n")])
    case("K11_new_file_added", 0, [],
         ops=[("w", K + "new.md", b"# brand new\n\nuntagged content\n")])
    case("K12_two_lines_swapped", 1, [("changed", K + "a.md")],
         ops=[("w", K + "a.md", base_body.replace(b"beta\ngamma", b"gamma\nbeta"))])
    case("K13_trailing_space", 1, [("changed", K + "a.md")],
         ops=[("w", K + "a.md", base_body.replace(b"alpha\n", b"alpha \n"))])
    case("K14_crlf", 1, [("changed", K + "a.md")],
         ops=[("w", K + "a.md", base_body.replace(b"\n", b"\r\n"))])
    case("K15_tag_alignment_rescues", 0, [],
         base_files={K + "a.md": b'a\n""\nb\n'},
         ops=[("w", K + "a.md", b'a\n[r60-correction 2026-10-27]\n""\n""\nb\n')])
    case("K16_untagged_duplicate", 1, [("untagged_insertion", K + "a.md")],
         base_files={K + "a.md": b"a\nb\nc\n"},
         ops=[("w", K + "a.md", b"a\nb\nb\nc\n")])
    case("K17_out_of_scope", 0, [],
         ops=[("w", "SKILL.md", b"totally rewritten\n")],
         base_files={K + "a.md": base_body, "SKILL.md": b"# original\n"})
    case("K18_symlink_replacement", 1, [("deleted", K + "a.md")],
         ops=[("rm", K + "a.md"), ("ln", K + "a.md", "b.md")])
    case("K19_binary_eof_append", 0, [],
         ops=[("w", K + "a.md", base_body + b"\xff\xfe")])
    case("K20_base_not_ancestor", 2, None, argv="not_ancestor")
    case("K21_missing_base_arg", 64, None, argv=["--revision", "HEAD"])
    case("K22_nested_rewrite", 1, [("changed", K + "sub/deep.md")],
         base_files={K + "sub/deep.md": b"# deep\n\nx\n"},
         ops=[("w", K + "sub/deep.md", b"# deep\n\ny\n")])

    # ---- supplementary cases ----------------------------------------------
    case("X1_empty_base_fills", 0, [],
         base_files={K + "a.md": b""},
         ops=[("w", K + "a.md", b"fresh content\nmore\n")])
    case("X2_prepend_tagged", 0, [],
         ops=[("w", K + "a.md",
               ST_TAG.encode() + b" prepended\nrest of run\n" + base_body)])
    case("X3_prepend_untagged", 1, [("untagged_insertion", K + "a.md")],
         ops=[("w", K + "a.md", b"prepended no tag\n" + base_body)])
    case("X4_midfile_plus_eof", 1, [("untagged_insertion", K + "a.md")],
         ops=[("w", K + "a.md",
               b"# note\n\nalpha\nbad run\nbeta\ngamma\nomega\nfree tail\n")])
    case("X5_bolded_tag_in_run", 0, [],
         ops=[("w", K + "a.md",
               b"# note\n\nalpha\n  " + ST_TAG.encode() + b" indented fix\nbeta\ngamma\nomega\n")])
    case("X6_tag_other_line_ignored", 1, [("untagged_insertion", K + "a.md")],
         ops=[("w", K + "a.md",
               b"# note\n\nalpha\nrun start\n" + ST_TAG.encode() + b"\nbeta\n" + ST_TAG.encode() + b" later run\ngamma\nomega\n")])
    case("X7_mode_change_only", 0, [],
         ops=[("w", K + "a.md", base_body)])  # content identical; mode not set by write
    case("X8_scope_arg_narrows", 0, [],
         ops=[("w", K + "a.md", b"rewritten\n")],
         argv="scope_other")
    case("X9_tag_after_midfile_comment_open", 1, [("untagged_insertion", K + "a.md")],
         ops=[("w", K + "a.md",
               b"# note\n\nalpha\n<!-- [r60-correction 2026-10-27]\nfix\nbeta\ngamma\nomega\n")])
    case("X10_root_is_subdir", 2, None, argv="root_subdir")
    case("X11_same_commit", 0, [], argv="same_commit")
    case("X12_git_env_scrubbed", 0, [], argv="same_commit",
         env={"GIT_DIR": "/nonexistent-selftest-dir"})
    case("X13_rescue_double_star", 0, [],
         base_files={K + "a.md": b"a\nx\nx\nc\n"},
         ops=[("w", K + "a.md",
               b"a\nx\n" + ST_TAG.encode() + b"\nx\nx\nc\n")])
    case("X14_tag_malformed_year", 1, [("untagged_insertion", K + "a.md")],
         ops=[("w", K + "a.md",
               b"# note\n\nalpha\n[r60-correction 26-10-27] fix\nbeta\ngamma\nomega\n")])
    case("X7_mode_change_only", 0, [],
         ops=[("chmod", K + "a.md", 0o755)])
    case("X15_json_output", 0, [], argv="json")


    passed, fails = 0, []
    for c in cases:
        argv = c["argv"]
        if argv == "not_ancestor":
            # one fixture for the repo; base is an unrelated orphan commit
            d = tempfile.mkdtemp(prefix="ag-st-")
            try:
                _git(d, "init", "-q")
                _git(d, "checkout", "-q", "--orphan", "side")
                with open(os.path.join(d, "x.md"), "wb") as fh:
                    fh.write(b"orphan\n")
                orphan = _commit_all(d, "orphan base")
                _git(d, "checkout", "-q", "--orphan", "main2")
                with open(os.path.join(d, "y.md"), "wb") as fh:
                    fh.write(b"tip\n")
                tip = _commit_all(d, "tip")
                rc, out = _run(d, "--base", orphan, "--revision", tip)
            finally:
                shutil.rmtree(d, ignore_errors=True)
        elif argv == "root_subdir":
            d, base, rev = _fixture(c["base_files"], c["ops"])
            try:
                rc, out = _run(os.path.join(d, "corpus"), "--base", base,
                               "--revision", rev)
            finally:
                shutil.rmtree(d, ignore_errors=True)
        elif argv == "scope_other":
            d, base, rev = _fixture(c["base_files"], c["ops"])
            try:
                rc, out = _run(d, "--base", base, "--revision", rev,
                               "--scope", "corpus/other/**/*.md")
            finally:
                shutil.rmtree(d, ignore_errors=True)
        elif argv == "json":
            d, base, rev = _fixture(c["base_files"], c["ops"])
            try:
                rc, out = _run(d, "--base", base, "--revision", rev, "--json")
                try:
                    doc = json.loads(out)
                    assert doc["exit"] == rc and doc["findings_count"] == \
                        len(doc["findings"]), f"bad json doc: {out[:140]}"
                except (ValueError, AssertionError) as e:
                    rc, out = 99, f"json parse: {e} | {out[:140]}"
            finally:
                shutil.rmtree(d, ignore_errors=True)
        elif argv == "same_commit":
            d, base, rev = _fixture(c["base_files"], c["ops"])
            try:
                rc, out = _run(d, "--base", base, "--revision", base,
                               env_extra=c["env"])
            finally:
                shutil.rmtree(d, ignore_errors=True)
        elif isinstance(argv, list):
            d, base, rev = _fixture(c["base_files"], c["ops"])
            try:
                rc, out = _run(d, *argv)
            finally:
                shutil.rmtree(d, ignore_errors=True)
        else:
            d, base, rev = _fixture(c["base_files"], c["ops"])
            try:
                rc, out = _run(d, "--base", base, "--revision", rev,
                               env_extra=c["env"])
            finally:
                shutil.rmtree(d, ignore_errors=True)
        ok = rc == c["want_rc"]
        detail = f"exit {rc} != {c['want_rc']} | {out.strip()[:140]}"
        if ok and c["want"] is not None:
            for kind, path in c["want"]:
                if f"{kind} {path}" not in out:
                    ok = False
                    detail = f"missing '{kind} {path}' in: {out.strip()[:140]}"
        if ok:
            passed += 1
        else:
            fails.append(f"{c['name']}: {detail}")
    print(f"append_guard selftest: {passed}/{len(cases)}")
    for line in fails:
        print("  FAIL", line)
    return 0 if passed == len(cases) else 1


# --------------------------------------------------------------------------- main

class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # usage errors -> exit 64
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        self.exit(64)


def main() -> int:
    ap = _Parser(description="append-only correction guard for knowledge files")
    ap.add_argument("--root")
    ap.add_argument("--base")
    ap.add_argument("--revision")
    ap.add_argument("--scope", action="append", default=None,
                    help="repo-relative glob; repeatable; default "
                         "corpus/knowledge/**/*.md")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    missing = [n for n in ("root", "base", "revision") if not getattr(args, n)]
    if missing:
        ap.print_usage(sys.stderr)
        print(f"{ap.prog}: error: required: " +
              " ".join(f"--{n}" for n in missing), file=sys.stderr)
        return 64
    scopes = [scope_regex(p) for p in (args.scope or DEFAULT_SCOPE)]
    code, findings, files, err = evaluate(args.root, args.base, args.revision,
                                          scopes)
    if args.json:
        print(json.dumps({
            "schema": "kake-r60-append-guard-v1",
            "root": args.root, "base": args.base, "revision": args.revision,
            "scope": args.scope or DEFAULT_SCOPE,
            "findings": [{"kind": k, "path": p,
                          **({"line": ln} if ln is not None else {})}
                         for k, p, ln in findings],
            "files": files, "findings_count": len(findings),
            **({"error": err} if err else {}),
            "exit": code}, indent=1, ensure_ascii=False))
    elif code == 2:
        print(f"append_guard: unevaluable: {err}", file=sys.stderr)
        print(f"files={files} findings={len(findings)}")
    else:
        print_findings(findings, files)
    return code


if __name__ == "__main__":
    sys.exit(main())
