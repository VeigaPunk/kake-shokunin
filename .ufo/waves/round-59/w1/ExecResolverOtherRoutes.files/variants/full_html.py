#!/usr/bin/env python3
"""Cross-registry source-id resolver for the kake lane (round-57 capability; round-58: fence-aware registry, NUL-split revision paths).

Lists every `S###` id cited in `corpus/knowledge/**/*.md` that does not resolve in
the lane's own `corpus/SOURCES.md`, and names which sibling lane registry holds it.

CLI (the round-57 contract; its gate checks this tool against an independent reference):

    python3 -B scripts/id_resolver.py --root <lane dir> [--revision <rev>] [--fleet <fleet root>] [--selftest]

  - cited ids: every word-bounded `S` + 3 or more digits in each `corpus/knowledge/**/*.md`
    file; with `--revision` the paths come from `git ls-tree -r -z` (NUL split, so a git-quoted or
    non-ASCII name is read as itself) and the blobs through `git show`, never the working tree
    (the lane registry is read at the same revision, for the same reason).
  - registry ids: first cell of each table row (a one-cell row counts) of `corpus/SOURCES.md` under the
    exact heading `## Registry` (the section ends at the next `# ` or `## ` heading), 0 to 3 leading spaces
    before the pipe (the census parser's rule; 4 spaces is code). Fenced code blocks are CommonMark's:
    a line of 0 to 3 spaces then 3 or more backticks or 3 or more tildes opens a block that only a line of
    the same character, at least as long, with nothing but whitespace after it (0 to 3 spaces) or EOF closes;
    a heading or a table row inside such a block counts for nothing here (the census still counts it — the stated divergence).
  - siblings: every `<fleet>/*-shokunin/` other than the lane (by realpath); a sibling's
    registry is `git show HEAD:corpus/SOURCES.md` when the directory has a `.git` (no worktree fallback), else the file.
  - stdout: one `DANGLING <id> cited-by=<comma paths> owners=<comma lanes or -> url-match=<lanes or ->`
    line per dangling id, then `ids_cited=N ids_resolved=N dangling=N owned_elsewhere=N unowned=N`.
  - exit: 0 dangling == 0, 1 dangling > 0, 2 unevaluable (revision unresolved, `--fleet` not a directory,
    registry absent, no knowledge file), 64 usage.
  - `--selftest` prints a final `selftest: <passed>/<total>` and exits 0 iff all passed.

`url-match` names the sibling lanes whose registry URL for that id appears verbatim in one of
the citing files. Output is deterministic: ids, citing paths, owners and url-match are sorted.
"""
from __future__ import annotations

import argparse
import contextlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

ID_RE = re.compile(r"(?<![A-Za-z0-9_])S\d{3,}(?![A-Za-z0-9_])")
ROW_RE = re.compile(r"^ {0,3}\|\s*([^|]*?)\s*(?:\|(.*))?$")
ID_CELL_RE = re.compile(r"^S\d{3,}$")
URL_RE = re.compile(r"https?://[^\s|<>\"'`]+")
REGISTRY_HEADING_RE = re.compile(r"^##\s+Registry\s*$")
SECTION_END_RE = re.compile(r"^#{1,2}\s")
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
REGISTRY_REL = "corpus/SOURCES.md"
KNOWLEDGE_REL = "corpus/knowledge"
SELFTEST_PREFIX = "idresolver-selftest-"


class Result:
    __slots__ = ("status", "error", "cited", "registry", "dangling", "summary")

    def __init__(self, status, error, cited, registry, dangling, summary):
        self.status = status
        self.error = error
        self.cited = cited
        self.registry = registry
        self.dangling = dangling
        self.summary = summary


def _spawn(argv):
    # an inherited GIT_DIR / GIT_WORK_TREE / GIT_INDEX_FILE would redirect every git call (and the selftest's sandbox commits): never pass them on
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)


def _text(proc):
    return proc.stdout.decode("utf-8", "replace")


def _git(root, *args):
    return _spawn(["git", "-C", root, *args])


def _err(message):
    return Result(2, message, {}, {}, [], None)


def _nul_paths(data):
    """Paths of a `git ls-tree -z` listing: NUL separated, never C-quoted."""
    return [chunk.decode("utf-8", "replace") for chunk in data.split(b"\0") if chunk]


def _fence(line):
    """(char, length) when `line` opens a CommonMark fenced block, else None."""
    m = FENCE_OPEN_RE.match(line)
    if not m:
        return None
    run = m.group(1)
    if run[0] == "`" and "`" in m.group(2):  # a backtick fence's info string may not hold a backtick
        return None
    return run[0], len(run)


def _fence_closes(line, char, length):
    m = FENCE_CLOSE_RE.match(line)
    return bool(m) and m.group(1)[0] == char and len(m.group(1)) >= length


_HTML_BLOCK_TAGS = ("pre", "script", "style", "textarea", "details", "div", "figure", "section",
                     "table", "ul", "ol", "blockquote")


def _strip_html_blocks(text):
    """Remove HTML blocks (a start tag line opens one; it closes on the matching end tag or a blank line)."""
    out = []
    open_tag = None
    for raw in text.split("\n"):
        line = raw.rstrip("\r")
        if open_tag is not None:
            if re.search(r"</" + open_tag + r"\s*>", line) or not line.strip():
                open_tag = None
            continue
        m = re.match(r"^ {0,3}<(" + "|".join(_HTML_BLOCK_TAGS) + r")(\s|>|/)", line)
        if m:
            open_tag = m.group(1)
            if re.search(r"</" + open_tag + r"\s*>", line):
                open_tag = None
            continue
        out.append(line)
    return "\n".join(out)


def _strip_html_comments(text):
    """Remove HTML comments (CommonMark: a comment runs to the line holding `-->`)."""
    out = []
    in_comment = False
    for raw in text.split("\n"):
        line = raw.rstrip("\r")
        if in_comment:
            if "-->" in line:
                line = line.split("-->", 1)[1]
                in_comment = False
            else:
                continue
        while "<!--" in line:
            head, rest = line.split("<!--", 1)
            if "-->" in rest:
                line = head + rest.split("-->", 1)[1]
            else:
                line = head
                in_comment = True
                break
        out.append(line)
    return "\n".join(out)


def parse_registry(text):
    """Map id -> [urls] for rows of the `## Registry` section (0-3 leading spaces, outside fenced code)."""
    text = _strip_html_blocks(_strip_html_comments(text))
    rows = {}
    inside = False
    fence = None
    for raw in text.splitlines():
        line = raw.rstrip("\r")
        if fence is not None:  # a heading or a table row inside a fenced block counts for nothing
            if _fence_closes(line, *fence):
                fence = None
            continue
        fence = _fence(line)
        if fence is not None:
            continue
        if REGISTRY_HEADING_RE.match(line):
            inside = True
            continue
        if not inside:
            continue
        if SECTION_END_RE.match(line):
            inside = False
            continue
        m = ROW_RE.match(line)
        if not m:
            continue
        sid = m.group(1).strip()
        if not ID_CELL_RE.match(sid):
            continue
        source_cell = (m.group(2) or "").split("|", 1)[0]
        urls = [u.rstrip(".,;:") for u in URL_RE.findall(source_cell)]
        bucket = rows.setdefault(sid, [])
        for url in urls:
            if url not in bucket:
                bucket.append(url)
    return rows


def parse_cited(bodies):
    """Map id -> sorted repo-relative citing paths."""
    cited = {}
    for path, body in bodies.items():
        for sid in ID_RE.findall(body):
            cited.setdefault(sid, set()).add(path)
    return {sid: sorted(paths) for sid, paths in sorted(cited.items())}


def resolve_revision(root, revision):
    proc = _git(root, "rev-parse", "--verify", f"{revision}^{{commit}}")
    if proc.returncode != 0:
        return None
    return _text(proc).strip()


def lane_registry(root, revision):
    if revision:
        proc = _git(root, "show", f"{revision}:{REGISTRY_REL}")
        if proc.returncode != 0:
            return None, f"registry absent at {revision[:12]}: {REGISTRY_REL}"
        return _text(proc), None
    path = os.path.join(root, REGISTRY_REL)
    if not os.path.isfile(path):
        return None, f"registry absent: {REGISTRY_REL}"
    try:
        with open(path, "rb") as handle:
            return handle.read().decode("utf-8", "replace"), None
    except OSError as exc:
        return None, f"registry unreadable: {exc}"


def knowledge_bodies(root, revision):
    """Map repo-relative path -> text, read from the revision blobs or the working tree."""
    if revision:
        proc = _git(root, "ls-tree", "-r", "-z", "--name-only", revision)
        if proc.returncode != 0:
            return None, f"cannot list {revision[:12]}: {_text(proc).strip()}"
        rels = [rel for rel in _nul_paths(proc.stdout)
                if rel.startswith(KNOWLEDGE_REL + "/") and rel.endswith(".md")]
        bodies = {}
        for rel in rels:
            blob = _git(root, "show", f"{revision}:{rel}")
            if blob.returncode != 0:
                return None, f"cannot read {rel} at {revision[:12]}"
            bodies[rel] = _text(blob)
        if not bodies:
            return None, f"no knowledge file at {revision[:12]}"
        return bodies, None
    base = os.path.join(root, KNOWLEDGE_REL)
    root_real = os.path.realpath(root)

    def inside(path):  # a symlink must not carry a citation in from outside the lane (w2/SentinelRound F3)
        real = os.path.realpath(path)
        return real == root_real or real.startswith(root_real + os.sep)

    if not os.path.isdir(base) or not inside(base):
        return None, f"no knowledge file: {KNOWLEDGE_REL} absent"
    bodies = {}
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            full = os.path.join(dirpath, name)
            if not inside(full):
                continue
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            try:
                with open(full, "rb") as handle:
                    bodies[rel] = handle.read().decode("utf-8", "replace")
            except OSError as exc:
                return None, f"cannot read {rel}: {exc}"
    if not bodies:
        return None, f"no knowledge file: {KNOWLEDGE_REL}/**/*.md empty"
    return bodies, None


def sibling_dirs(root, fleet):
    out = []
    if not os.path.isdir(fleet):
        return out
    lane_real = os.path.realpath(root)
    for name in sorted(os.listdir(fleet)):
        if not name.endswith("-shokunin"):
            continue
        path = os.path.join(fleet, name)
        if not os.path.isdir(path):
            continue
        if os.path.realpath(path) == lane_real:
            continue
        out.append((name, path))
    return out


def sibling_registry(path):
    if os.path.exists(os.path.join(path, ".git")):  # the directory itself is a repository: its HEAD registry or nothing (a worktree file is not committed evidence)
        proc = _git(path, "show", f"HEAD:{REGISTRY_REL}")
        return parse_registry(_text(proc)) if proc.returncode == 0 else {}
    file_path = os.path.join(path, REGISTRY_REL)
    if os.path.isfile(file_path):
        try:
            with open(file_path, "rb") as handle:
                return parse_registry(handle.read().decode("utf-8", "replace"))
        except OSError:
            return {}
    return {}


def evaluate(root, revision=None, fleet=None):
    root = os.path.abspath(root)
    rev = None
    if revision:
        rev = resolve_revision(root, revision)
        if rev is None:
            return _err(f"revision {revision!r} unresolved in {root}")
    registry_text, err = lane_registry(root, rev)
    if err:
        return _err(err)
    bodies, err = knowledge_bodies(root, rev)
    if err:
        return _err(err)
    registry = parse_registry(registry_text)
    cited = parse_cited(bodies)
    dangling_ids = sorted(set(cited) - set(registry))
    fleet_root = os.path.abspath(fleet) if fleet else os.path.dirname(root)
    if not os.path.isdir(fleet_root):
        return _err(f"fleet root {fleet_root} is not a directory")
    sibling_regs = {}
    if dangling_ids:
        sibling_regs = {name: sibling_registry(path) for name, path in sibling_dirs(root, fleet_root)}
    rows = []
    for sid in dangling_ids:
        paths = cited[sid]
        owners = sorted(name for name, reg in sibling_regs.items() if sid in reg)
        matched = []
        for name in owners:
            urls = sibling_regs[name].get(sid, ())
            if any(url in bodies[path] for path in paths for url in urls):
                matched.append(name)
        rows.append((sid, paths, owners, matched))
    cited_n = len(cited)
    owned = sum(1 for row in rows if row[2])
    summary = (cited_n, cited_n - len(dangling_ids), len(dangling_ids), owned, len(rows) - owned)
    return Result(1 if dangling_ids else 0, None, cited, registry, rows, summary)


def render(result):
    lines = []
    for sid, paths, owners, matched in result.dangling:
        lines.append(
            f"DANGLING {sid} cited-by={','.join(paths)} "
            f"owners={','.join(owners) or '-'} url-match={','.join(matched) or '-'}"
        )
    cited_n, resolved, dangling, owned, unowned = result.summary
    lines.append(
        f"ids_cited={cited_n} ids_resolved={resolved} dangling={dangling} "
        f"owned_elsewhere={owned} unowned={unowned}"
    )
    return lines


# --------------------------------------------------------------------------- selftest

def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def _registry(rows, indent="", eol="\n"):
    body = (
        "# SOURCES\n## Registry\n"
        "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
    )
    for sid, source in rows:
        body += f"{indent}| {sid} | {source} | docs | A | s | a | x | mined | 2026-10-25 | 90d | — |\n"
    body += "## Paths\n\n- none\n"
    if eol != "\n":
        body = body.replace("\n", eol)
    return body


def _fleet(base, lane_rows, knowledge, siblings=None, lane_indent="", eol="\n"):
    for name, rows in sorted((siblings or {}).items()):
        _write(os.path.join(base, name, REGISTRY_REL), _registry(rows, eol=eol))
    lane = os.path.join(base, "demo-shokunin")
    if lane_rows is not None:
        _write(os.path.join(lane, REGISTRY_REL), _registry(lane_rows, indent=lane_indent, eol=eol))
    for rel, text in knowledge.items():
        _write(os.path.join(lane, KNOWLEDGE_REL, rel), text)
    return lane


def _git_ok(argv):
    proc = _spawn(argv)
    if proc.returncode != 0:
        raise AssertionError(f"git {' '.join(argv)}: {_text(proc).strip() or proc.stderr.decode('utf-8', 'replace').strip()}")
    return _text(proc)


def _repo(path):
    _git_ok(["git", "init", "-q", path])
    top = _git_ok(["git", "-C", path, "rev-parse", "--show-toplevel"]).strip()
    if os.path.realpath(top) != os.path.realpath(path):
        raise AssertionError(f"sandbox toplevel {top} != {path}")
    return path


def _commit(path, files, msg="selftest"):
    for rel, text in files.items():
        _write(os.path.join(path, rel), text)
    _git_ok(["git", "-C", path, "add", "-A"])
    _git_ok(["git", "-C", path, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
             "-c", "commit.gpgsign=false", "commit", "-q", "-m", msg])
    return _git_ok(["git", "-C", path, "rev-parse", "HEAD"]).strip()


@contextlib.contextmanager
def _tmpdir():
    base = tempfile.mkdtemp(prefix=SELFTEST_PREFIX)
    try:
        yield base
    finally:
        shutil.rmtree(base, ignore_errors=True)


def _check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def _summary(root, **kwargs):
    return evaluate(root, **kwargs)


def _case_indent(indent, sid):
    with _tmpdir() as base:
        lane = _fleet(base, [(sid, f"https://e.example/{sid}")], {"a.md": f"Cites {sid}.\n"}, lane_indent=indent)
        res = _summary(lane, fleet=base)
        _check(res.status == 0, f"status={res.status} error={res.error}")
        _check(res.summary == (1, 1, 0, 0, 0), f"summary={res.summary}")


def case_indent_0():
    _case_indent("", "S001")


def case_indent_2():
    _case_indent("  ", "S002")


def case_indent_3():
    _case_indent("   ", "S003")


def case_indent_4_is_code():
    with _tmpdir() as base:
        lane = _fleet(base, [("S004", "https://e.example/4")], {"a.md": "Cites S004.\n"}, lane_indent="    ")
        res = _summary(lane, fleet=base)
        _check(res.status == 1, f"status={res.status}")
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")
        _check(res.dangling[0][2] == [] and res.dangling[0][3] == [], f"row={res.dangling[0]}")


def case_crlf_registry():
    with _tmpdir() as base:
        lane = _fleet(base, [("S005", "https://e.example/5")], {"a.md": "Cites S005.\n"}, eol="\r\n")
        res = _summary(lane, fleet=base)
        _check(res.status == 0, f"status={res.status} error={res.error}")
        _check(res.summary == (1, 1, 0, 0, 0), f"summary={res.summary}")


def case_knowledge_markdown_table():
    with _tmpdir() as base:
        table = "| id | note |\n|---|---|\n| S001 | quoted in a table |\n"
        lane = _fleet(base, [("S001", "https://e.example/1")], {"t.md": table})
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 1, 0, 0, 0), f"summary={res.summary}")


def case_range_cites_endpoints_only():
    with _tmpdir() as base:
        rows = [("S011", "https://e.example/11"), ("S012", "https://e.example/12"), ("S013", "https://e.example/13")]
        lane = _fleet(base, rows, {"r.md": "Spans S011\u2013S013 only.\n"})
        res = _summary(lane, fleet=base)
        _check(sorted(res.cited) == ["S011", "S013"], f"cited={sorted(res.cited)}")
        _check(res.summary == (2, 2, 0, 0, 0), f"summary={res.summary}")


def _decoy_case(body):
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"d.md": body})
        res = _summary(lane, fleet=base)
        _check(res.summary == (0, 0, 0, 0, 0), f"summary={res.summary}")
        _check(res.status == 0, f"status={res.status}")


def case_decoy_short():
    _decoy_case("Too short: S12.\n")


def case_decoy_prefixed():
    _decoy_case("Not an id: AS500.\n")


def case_decoy_suffixed():
    _decoy_case("Not an id: S500x.\n")


def case_decoy_lowercase():
    _decoy_case("Not an id: s101.\n")


def case_four_digit_id():
    with _tmpdir() as base:
        lane = _fleet(base, [("S0300", "https://e.example/300")], {"a.md": "Cites S0300.\n"})
        res = _summary(lane, fleet=base)
        _check(sorted(res.cited) == ["S0300"], f"cited={sorted(res.cited)}")
        _check(res.summary == (1, 1, 0, 0, 0), f"summary={res.summary}")


def case_two_siblings_own():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S200.\n"},
                      siblings={"alpha-shokunin": [("S200", "https://a.example/200")],
                                "beta-shokunin": [("S200", "https://b.example/200")]})
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 0, 1, 1, 0), f"summary={res.summary}")
        _check(res.dangling[0][2] == ["alpha-shokunin", "beta-shokunin"], f"owners={res.dangling[0][2]}")


def case_unowned():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S777.\n"},
                      siblings={"alpha-shokunin": [("S101", "https://a.example/101")]})
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")
        _check(res.dangling[0][2] == [] and res.dangling[0][3] == [], f"row={res.dangling[0]}")


def case_lane_excluded_by_realpath():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        _repo(lane)
        first = _commit(lane, {
            REGISTRY_REL: _registry([("S001", "https://e.example/1")]),
            KNOWLEDGE_REL + "/a.md": "Cites S900.\n",
        })
        _commit(lane, {REGISTRY_REL: _registry([("S001", "https://e.example/1"), ("S900", "https://e.example/900")])})
        os.symlink(lane, os.path.join(base, "other-shokunin"))
        res = _summary(lane, revision=first, fleet=base)
        _check(res.status == 1, f"status={res.status} error={res.error}")
        _check(res.dangling and res.dangling[0][2] == [], f"owners={res.dangling}")
        _check(res.summary[4] == 1, f"summary={res.summary}")


def case_sibling_without_registry():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S777.\n"})
        os.makedirs(os.path.join(base, "gamma-shokunin", "corpus"))
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")


def case_unresolved_revision():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S001.\n"})
        res = _summary(lane, revision="0" * 40, fleet=base)
        _check(res.status == 2 and res.error, f"status={res.status} error={res.error}")


def case_missing_registry():
    with _tmpdir() as base:
        lane = _fleet(base, None, {"a.md": "Cites S001.\n"})
        res = _summary(lane, fleet=base)
        _check(res.status == 2 and "registry" in (res.error or ""), f"status={res.status} error={res.error}")


def case_no_knowledge_files():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {})
        res = _summary(lane, fleet=base)
        _check(res.status == 2 and "knowledge" in (res.error or ""), f"status={res.status} error={res.error}")


def case_revision_reads_old_blobs():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        _repo(lane)
        first = _commit(lane, {
            REGISTRY_REL: _registry([("S001", "https://e.example/1")]),
            KNOWLEDGE_REL + "/a.md": "Cites S001.\n",
        })
        second = _commit(lane, {
            REGISTRY_REL: _registry([("S002", "https://e.example/2")]),
            KNOWLEDGE_REL + "/a.md": "Cites S002.\n",
        })
        _check(first != second, "commits identical")
        old = _summary(lane, revision=first, fleet=base)
        _check(sorted(old.cited) == ["S001"] and old.summary == (1, 1, 0, 0, 0), f"old cited={sorted(old.cited)} summary={old.summary}")
        new = _summary(lane, revision=second, fleet=base)
        _check(sorted(new.cited) == ["S002"] and new.summary == (1, 1, 0, 0, 0), f"new cited={sorted(new.cited)} summary={new.summary}")
        short = _summary(lane, revision=first[:7], fleet=base)
        _check(sorted(short.cited) == ["S001"], f"short cited={sorted(short.cited)}")
        worktree = _summary(lane, fleet=base)
        _check(sorted(worktree.cited) == ["S002"], f"worktree cited={sorted(worktree.cited)}")


def case_usage_error():
    _check(main(["--root"]) == 64, "missing value for --root did not return 64")
    _check(main(["--bogus"]) == 64, "unknown option did not return 64")
    _check(main([]) == 64, "missing --root did not return 64")


def case_duplicate_citation_once():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "S777 then S777 again.\n"})
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")
        _check(res.dangling[0][1] == ["corpus/knowledge/a.md"], f"paths={res.dangling[0][1]}")


def case_citing_path_order():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")],
                      {"b.md": "S777\n", "a.md": "S777\n", "sub/c.md": "S777\n"})
        res = _summary(lane, fleet=base)
        _check(res.dangling[0][1] == ["corpus/knowledge/a.md", "corpus/knowledge/b.md", "corpus/knowledge/sub/c.md"],
               f"paths={res.dangling[0][1]}")


def case_exact_dangling_line():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "S777\n"})
        lines = render(_summary(lane, fleet=base))
        _check(lines[0] == "DANGLING S777 cited-by=corpus/knowledge/a.md owners=- url-match=-", f"line={lines[0]}")
        _check(lines[-1] == "ids_cited=1 ids_resolved=0 dangling=1 owned_elsewhere=0 unowned=1", f"line={lines[-1]}")


def case_gate_shaped_totals():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        registry = (
            "# SOURCES\n## Registry\n"
            "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n"
            "| S001 | t — https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | — |\n"
            "  | S002 | t — https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | — |\n"
            "## Paths\n\n- none\n"
        )
        _write(os.path.join(lane, REGISTRY_REL), registry)
        _write(os.path.join(base, "alpha-shokunin", REGISTRY_REL),
               _registry([("S101", "https://a.example/101"), ("S200", "https://a.example/200"), ("S0300", "https://a.example/300")]))
        _write(os.path.join(base, "beta-shokunin", REGISTRY_REL),
               _registry([("S200", "https://b.example/200")], indent="   "))
        _write(os.path.join(lane, KNOWLEDGE_REL, "good.md"),
               "Cites S001 and S002.\n")
        _write(os.path.join(lane, KNOWLEDGE_REL, "sub/bad.md"),
               "source: S101 — https://a.example/101\n\nHeld by alpha only: S101, quoted at https://a.example/101.\n"
               "Held by two siblings: S200.\nHeld by none: S777. A four-digit id S0300 is alpha's id.\n"
               "Decoys: S12, AS500, S500x, s101.\n")
        res = _summary(lane, fleet=base)
        _check(res.status == 1, f"status={res.status}")
        _check(res.summary == (6, 2, 4, 3, 1), f"summary={res.summary}")
        rows = {row[0]: row for row in res.dangling}
        _check(rows["S101"][1] == ["corpus/knowledge/sub/bad.md"], f"S101={rows['S101']}")
        _check(rows["S101"][2] == ["alpha-shokunin"] and rows["S101"][3] == ["alpha-shokunin"], f"S101={rows['S101']}")
        _check(rows["S200"][2] == ["alpha-shokunin", "beta-shokunin"] and rows["S200"][3] == [], f"S200={rows['S200']}")
        _check(rows["S0300"][2] == ["alpha-shokunin"] and rows["S0300"][3] == [], f"S0300={rows['S0300']}")
        _check(rows["S777"][2] == [] and rows["S777"][3] == [], f"S777={rows['S777']}")


def case_exit_zero_when_clean():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S001.\n"})
        _check(_summary(lane, fleet=base).status == 0, "clean run did not exit 0")


def case_exit_one_when_dangling():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S777.\n"})
        _check(_summary(lane, fleet=base).status == 1, "dangling run did not exit 1")


def case_url_match_present():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "S101 — see https://a.example/101 now.\n"},
                      siblings={"alpha-shokunin": [("S101", "https://a.example/101")]})
        res = _summary(lane, fleet=base)
        _check(res.dangling[0][2] == ["alpha-shokunin"], f"owners={res.dangling[0][2]}")
        _check(res.dangling[0][3] == ["alpha-shokunin"], f"url-match={res.dangling[0][3]}")


def case_url_match_absent():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "S101 without the link.\n"},
                      siblings={"alpha-shokunin": [("S101", "https://a.example/101")]})
        res = _summary(lane, fleet=base)
        _check(res.dangling[0][2] == ["alpha-shokunin"] and res.dangling[0][3] == [], f"row={res.dangling[0]}")


def case_url_match_one_of_two():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "S200 quoted at https://b.example/200.\n"},
                      siblings={"alpha-shokunin": [("S200", "https://a.example/200")],
                                "beta-shokunin": [("S200", "https://b.example/200")]})
        res = _summary(lane, fleet=base)
        _check(res.dangling[0][2] == ["alpha-shokunin", "beta-shokunin"], f"owners={res.dangling[0][2]}")
        _check(res.dangling[0][3] == ["beta-shokunin"], f"url-match={res.dangling[0][3]}")


def case_owners_sorted():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "S200\n"},
                      siblings={"beta-shokunin": [("S200", "https://b.example/200")],
                                "alpha-shokunin": [("S200", "https://a.example/200")]})
        res = _summary(lane, fleet=base)
        _check(res.dangling[0][2] == ["alpha-shokunin", "beta-shokunin"], f"owners={res.dangling[0][2]}")


def case_nested_knowledge_path():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"sub/deep/x.md": "S777\n"})
        res = _summary(lane, fleet=base)
        _check(res.dangling[0][1] == ["corpus/knowledge/sub/deep/x.md"], f"paths={res.dangling[0][1]}")


def case_registry_section_end():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        text = _registry([("S010", "https://e.example/10")])
        text += "| S011 | https://e.example/11 | docs | A | s | a | x | mined | 2026-10-25 | 90d | — |\n"
        _write(os.path.join(lane, REGISTRY_REL), text)
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), "Cites S010 and S011.\n")
        res = _summary(lane, fleet=base)
        _check(res.summary == (2, 1, 1, 0, 1), f"summary={res.summary}")
        _check([row[0] for row in res.dangling] == ["S011"], f"dangling={res.dangling}")


def case_decoy_trailing_underscore():
    _decoy_case("Not an id: S777_ and _S777 and S_777.\n")


def case_registry_cell_not_an_id():
    with _tmpdir() as base:
        lane = _fleet(base, [("S777x", "https://e.example/7")], {"a.md": "Cites S777.\n"})
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")


def case_registry_heading_with_trailing_text():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        _write(os.path.join(lane, REGISTRY_REL), _registry([("S010", "https://e.example/10")]).replace("## Registry", "## Registry (legacy)"))
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), "Cites S010.\n")
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")


def case_lone_cr_registry():
    with _tmpdir() as base:
        lane = _fleet(base, [("S010", "https://e.example/10")], {"a.md": "Cites S010.\n"}, eol="\r")
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 1, 0, 0, 0), f"summary={res.summary}")


def case_sibling_suffix_required():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S777.\n"},
                      siblings={"shokunin": [("S777", "https://x.example/7")], "fooshokunin": [("S777", "https://x.example/7")]})
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")


def case_sibling_head_not_dirty_worktree():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S777.\n"})
        sib = os.path.join(base, "alpha-shokunin")
        _repo(sib)
        _commit(sib, {REGISTRY_REL: _registry([("S777", "https://a.example/7")])})
        _write(os.path.join(sib, REGISTRY_REL), _registry([("S001", "https://a.example/1")]))  # uncommitted rewrite
        res = _summary(lane, fleet=base)
        _check(res.dangling[0][2] == ["alpha-shokunin"], f"owners={res.dangling}")


def case_sibling_repo_without_committed_registry():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S777.\n"})
        sib = os.path.join(base, "alpha-shokunin")
        _repo(sib)
        _commit(sib, {"README.md": "r\n"})
        _write(os.path.join(sib, REGISTRY_REL), _registry([("S777", "https://a.example/7")]))  # on disk, never committed
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")


def case_fleet_root_repo_does_not_own():
    with _tmpdir() as base:
        _repo(base)
        _commit(base, {REGISTRY_REL: _registry([("S777", "https://f.example/7")])})
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S777.\n"})
        os.makedirs(os.path.join(base, "alpha-shokunin"))
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")


def case_one_cell_registry_row():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        _write(os.path.join(lane, REGISTRY_REL), _registry([("S010", "https://e.example/10")]).replace("## Paths", "| S011\n## Paths"))
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), "Cites S010 and S011.\n")
        res = _summary(lane, fleet=base)
        _check(res.summary == (2, 2, 0, 0, 0), f"summary={res.summary}")


def case_missing_fleet_exits_2():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S777.\n"})
        res = _summary(lane, fleet=os.path.join(base, "no-such-fleet"))
        _check(res.status == 2 and "not a directory" in (res.error or ""), f"status={res.status} error={res.error}")


def case_revision_ignores_non_markdown():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        _repo(lane)
        rev = _commit(lane, {REGISTRY_REL: _registry([("S001", "https://e.example/1")]), KNOWLEDGE_REL + "/a.md": "Cites S001.\n",
                             KNOWLEDGE_REL + "/notes.json": '{"cites": "S777"}\n'})
        res = _summary(lane, revision=rev, fleet=base)
        _check(res.summary == (1, 1, 0, 0, 0), f"summary={res.summary}")


def case_url_match_scans_every_citing_file():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "S101 first file, no link.\n", "b.md": "S101 see https://a.example/101 here.\n"},
                      siblings={"alpha-shokunin": [("S101", "https://a.example/101")]})
        res = _summary(lane, fleet=base)
        _check(res.dangling[0][3] == ["alpha-shokunin"], f"row={res.dangling[0]}")


def case_url_match_ignores_registry_punctuation():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "S101 see https://a.example/101 here.\n"},
                      siblings={"alpha-shokunin": [("S101", "https://a.example/101.")]})
        res = _summary(lane, fleet=base)
        _check(res.dangling[0][3] == ["alpha-shokunin"], f"row={res.dangling[0]}")


def case_dangling_lines_in_id_order():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "S200 then S101 then S1000.\n"})
        res = _summary(lane, fleet=base)
        lines = render(res)
        _check([ln.split()[1] for ln in lines[:-1]] == ["S1000", "S101", "S200"], f"lines={lines}")


def case_git_env_is_scrubbed():
    saved = os.environ.get("GIT_DIR")
    os.environ["GIT_DIR"] = "/nonexistent/elsewhere/.git"
    try:
        with _tmpdir() as base:
            lane = os.path.join(base, "demo-shokunin")
            _repo(lane)
            rev = _commit(lane, {REGISTRY_REL: _registry([("S001", "https://e.example/1")]), KNOWLEDGE_REL + "/a.md": "Cites S001.\n"})
            res = _summary(lane, revision=rev, fleet=base)
            _check(res.status == 0, f"status={res.status} error={res.error}")
    finally:
        if saved is None:
            os.environ.pop("GIT_DIR", None)
        else:
            os.environ["GIT_DIR"] = saved


def case_symlink_out_of_the_lane_is_not_a_citation():
    with _tmpdir() as base:
        lane = _fleet(base, [("S001", "https://e.example/1")], {"a.md": "Cites S001.\n"})
        outside = os.path.join(base, "outside.md")
        _write(outside, "Cites S777.\n")
        os.symlink(outside, os.path.join(lane, KNOWLEDGE_REL, "ext.md"))
        res = _summary(lane, fleet=base)
        _check(res.summary == (1, 1, 0, 0, 0), f"summary={res.summary}")


def case_fenced_heading_before_registry():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        fenced = "```\n## Registry\n\n| S950 | https://e.example/950 |\n```\n\n"
        _write(os.path.join(lane, REGISTRY_REL), fenced + _registry([("S001", "https://e.example/1")]))
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), "Cites S001 and S950.\n")
        res = _summary(lane, fleet=base)
        _check(res.summary == (2, 1, 1, 0, 1), f"summary={res.summary}")
        _check([row[0] for row in res.dangling] == ["S950"], f"dangling={res.dangling}")


def _fenced_row_case(name, block, inside):
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        text = _registry([("S001", "https://e.example/1")]).replace("## Paths", block + "## Paths")
        _write(os.path.join(lane, REGISTRY_REL), text)
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), f"Cites S001 and {name}.\n")
        res = _summary(lane, fleet=base)
        want = (2, 1, 1, 0, 1) if inside else (2, 2, 0, 0, 0)
        _check(res.summary == want, f"summary={res.summary}")
        _check([row[0] for row in res.dangling] == ([name] if inside else []), f"dangling={res.dangling}")


def case_fenced_row_inside_registry_backticks():
    _fenced_row_case("S951", "```\n| S951 | https://e.example/951 | docs |\n```\n", True)


def case_fenced_row_inside_registry_tildes():
    _fenced_row_case("S952", "~~~\n| S952 | https://e.example/952 | docs |\n~~~\n", True)


def case_three_space_fence_opens():
    _fenced_row_case("S957", "   ```\n| S957 | https://e.example/957 | docs |\n   ```\n", True)


def case_fence_closed_by_a_longer_run():
    _fenced_row_case("S953", "````\nsample text\n``````\n| S953 | https://e.example/953 | docs |\n", False)


def case_row_after_closed_fence_resolves():
    _fenced_row_case("S956", "```\nsample text\n```\n| S956 | https://e.example/956 | docs |\n", False)


def case_shorter_run_does_not_close():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        text = _registry([("S001", "https://e.example/1")]).replace(
            "## Paths", "````\n| S958 | https://e.example/958 | docs |\n```\n| S959 | https://e.example/959 | docs |\n````\n## Paths")
        _write(os.path.join(lane, REGISTRY_REL), text)
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), "Cites S001, S958 and S959.\n")
        res = _summary(lane, fleet=base)
        _check(res.summary == (3, 1, 2, 0, 2), f"summary={res.summary}")
        _check([row[0] for row in res.dangling] == ["S958", "S959"], f"dangling={res.dangling}")


def case_unclosed_fence_swallows_the_rest():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        text = _registry([("S001", "https://e.example/1")]).replace(
            "## Paths", "```\n| S954 | https://e.example/954 | docs |\n## Paths\n\n| S955 | https://e.example/955 | docs |\n")
        _write(os.path.join(lane, REGISTRY_REL), text)
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), "Cites S001, S954 and S955.\n")
        res = _summary(lane, fleet=base)
        _check(res.summary == (3, 1, 2, 0, 2), f"summary={res.summary}")
        _check([row[0] for row in res.dangling] == ["S954", "S955"], f"dangling={res.dangling}")


def case_revision_reads_non_ascii_path():
    with _tmpdir() as base:
        lane = _repo(os.path.join(base, "demo-shokunin"))
        rev = _commit(lane, {REGISTRY_REL: _registry([("S001", "https://e.example/1")]),
                             KNOWLEDGE_REL + "/中文.md": "Cites S900.\n"})
        res = _summary(lane, revision=rev, fleet=base)
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")
        _check(res.dangling[0][1] == ["corpus/knowledge/中文.md"], f"paths={res.dangling[0][1]}")


def case_revision_reads_quote_character_path():
    with _tmpdir() as base:
        lane = _repo(os.path.join(base, "demo-shokunin"))
        rev = _commit(lane, {REGISTRY_REL: _registry([("S001", "https://e.example/1")]),
                             KNOWLEDGE_REL + '/a"b.md': "Cites S901.\n"})
        res = _summary(lane, revision=rev, fleet=base)
        _check(res.summary == (1, 0, 1, 0, 1), f"summary={res.summary}")
        _check(res.dangling[0][1] == ['corpus/knowledge/a"b.md'], f"paths={res.dangling[0][1]}")


def _cases():
    return [
        ("registry row at 0 leading spaces", case_indent_0),
        ("registry row at 2 leading spaces", case_indent_2),
        ("registry row at 3 leading spaces", case_indent_3),
        ("registry row at 4 spaces is code", case_indent_4_is_code),
        ("CRLF registry rows", case_crlf_registry),
        ("id cited inside a markdown table", case_knowledge_markdown_table),
        ("range S011-S013 cites endpoints only", case_range_cites_endpoints_only),
        ("decoy S12 is not an id", case_decoy_short),
        ("decoy AS500 is not an id", case_decoy_prefixed),
        ("decoy S500x is not an id", case_decoy_suffixed),
        ("decoy s101 is not an id", case_decoy_lowercase),
        ("four-digit id S0300 is an id", case_four_digit_id),
        ("id held by two siblings", case_two_siblings_own),
        ("id held by none", case_unowned),
        ("lane excluded from owners by realpath", case_lane_excluded_by_realpath),
        ("sibling without a registry", case_sibling_without_registry),
        ("unresolved revision exits 2", case_unresolved_revision),
        ("missing registry exits 2", case_missing_registry),
        ("no knowledge files exits 2", case_no_knowledge_files),
        ("revision reads old blobs not the worktree", case_revision_reads_old_blobs),
        ("usage error returns 64", case_usage_error),
        ("duplicate citation counted once", case_duplicate_citation_once),
        ("citing-path order stable", case_citing_path_order),
        ("exact DANGLING and summary lines", case_exact_dangling_line),
        ("gate-shaped fixture totals", case_gate_shaped_totals),
        ("exit 0 when clean", case_exit_zero_when_clean),
        ("exit 1 when dangling", case_exit_one_when_dangling),
        ("url-match when the row URL is quoted", case_url_match_present),
        ("url-match absent when no URL quoted", case_url_match_absent),
        ("url-match names one of two owners", case_url_match_one_of_two),
        ("owners sorted alphabetically", case_owners_sorted),
        ("nested knowledge path recorded", case_nested_knowledge_path),
        ("registry section ends at the next heading", case_registry_section_end),
        ("decoys S777_ _S777 S_777 are not ids", case_decoy_trailing_underscore),
        ("registry cell S777x is not a registry id", case_registry_cell_not_an_id),
        ("heading with trailing text is not the Registry section", case_registry_heading_with_trailing_text),
        ("lone-CR registry rows", case_lone_cr_registry),
        ("a directory without the -shokunin suffix is not a sibling", case_sibling_suffix_required),
        ("sibling read at HEAD, not at its dirty worktree", case_sibling_head_not_dirty_worktree),
        ("sibling repo without a committed registry owns nothing", case_sibling_repo_without_committed_registry),
        ("a fleet root that is a repository owns nothing for a plain sibling", case_fleet_root_repo_does_not_own),
        ("a one-cell registry row registers its id", case_one_cell_registry_row),
        ("missing fleet exits 2", case_missing_fleet_exits_2),
        ("non-markdown knowledge file at a revision is ignored", case_revision_ignores_non_markdown),
        ("url-match scans every citing file", case_url_match_scans_every_citing_file),
        ("url-match ignores punctuation after a registry URL", case_url_match_ignores_registry_punctuation),
        ("dangling lines render in id order", case_dangling_lines_in_id_order),
        ("an inherited GIT_DIR is not passed on", case_git_env_is_scrubbed),
        ("a symlink out of the lane carries no citation", case_symlink_out_of_the_lane_is_not_a_citation),
        ("a fenced block before the Registry heading opens nothing", case_fenced_heading_before_registry),
        ("a fenced row inside Registry (backticks) does not register", case_fenced_row_inside_registry_backticks),
        ("a fenced row inside Registry (tildes) does not register", case_fenced_row_inside_registry_tildes),
        ("a fence indented 3 spaces still opens", case_three_space_fence_opens),
        ("a longer closing run closes the fence", case_fence_closed_by_a_longer_run),
        ("a row after a closed fence resolves", case_row_after_closed_fence_resolves),
        ("a shorter run does not close the fence", case_shorter_run_does_not_close),
        ("an unclosed fence swallows the rest", case_unclosed_fence_swallows_the_rest),
        ("a non-ASCII knowledge path is read at a revision", case_revision_reads_non_ascii_path),
        ("a quote-character knowledge path is read at a revision", case_revision_reads_quote_character_path),
    ]


def run_selftest():
    cases = _cases()
    passed = 0
    for index, (name, func) in enumerate(cases, 1):
        try:
            func()
        except Exception as exc:  # noqa: BLE001 - selftest reports, never raises
            print(f"FAIL {index:02d} {name}: {type(exc).__name__}: {exc}")
        else:
            passed += 1
            print(f"ok   {index:02d} {name}")
    print(f"selftest: {passed}/{len(cases)}")
    return 0 if passed == len(cases) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="id_resolver.py",
        description="List cited source ids that do not resolve in the lane registry, naming sibling owners.",
    )
    parser.add_argument("--root", help="lane directory")
    parser.add_argument("--revision", help="git revision to read knowledge and registry from")
    parser.add_argument("--fleet", help="fleet root holding the sibling lanes (default: parent of --root)")
    parser.add_argument("--selftest", action="store_true", help="run the built-in fixture suite")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    if args.selftest:
        return run_selftest()
    if not args.root:
        print("usage: id_resolver.py --root <lane dir> [--revision <rev>] [--fleet <fleet root>]", file=sys.stderr)
        return 64
    if not os.path.isdir(args.root):
        print(f"id_resolver: unevaluable: root {args.root!r} is not a directory", file=sys.stderr)
        return 2
    result = evaluate(args.root, args.revision, args.fleet)
    if result.status == 2:
        print(f"id_resolver: unevaluable: {result.error}", file=sys.stderr)
        return 2
    for line in render(result):
        print(line)
    return result.status


if __name__ == "__main__":
    sys.exit(main())
