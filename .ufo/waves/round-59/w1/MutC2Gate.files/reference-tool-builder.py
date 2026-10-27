#!/usr/bin/env python3
"""Build a scratch reference implementation of the seven C2 route fixes on top of the
contract-commit tool (45a92b6). SCRATCH ONLY — the lane is never touched.

The reference tool exists so the frozen 21-case gate can be measured against a GREEN tool
(a mutation score against a tool that already fails 8 cases says little).
"""
from __future__ import annotations

import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kake-r59/MutC2Gate"
FIX = os.path.join(S, "fix")
TOOL = "scripts/id_resolver.py"


def patch(src: str) -> str:
    def sub(old, new, count=1):
        nonlocal src
        n = src.count(old)
        assert n == count, (n, count, old[:70])
        src = src.replace(old, new)

    # 1. constants: HTML comment, setext underline
    sub('FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \\t]*$")',
        'FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \\t]*$")\n'
        'HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)\n'
        'SETEXT_RE = re.compile(r"^ {0,3}(?:-{3,}|={3,})\\s*$")')

    # 2. parse_registry: strip HTML comments, end the section at a setext heading
    sub('''    rows = {}
    inside = False
    fence = None
    for raw in text.splitlines():
        line = raw.rstrip("\\r")
        if fence is not None:  # a heading or a table row inside a fenced block counts for nothing
            if _fence_closes(line, *fence):
                fence = None
            continue''',
        '''    rows = {}
    inside = False
    fence = None
    prev_text = None  # the previous non-blank line, for a setext heading
    text = HTML_COMMENT_RE.sub("", text)  # a row inside an HTML comment registers nothing
    for raw in text.splitlines():
        line = raw.rstrip("\\r")
        if fence is not None:  # a heading or a table row inside a fenced block counts for nothing
            if _fence_closes(line, *fence):
                fence = None
            continue''')

    sub('''        if SECTION_END_RE.match(line):
            inside = False
            continue
        m = ROW_RE.match(line)
        if not m:
            continue''',
        '''        if SETEXT_RE.match(line) and prev_text is not None and not prev_text.lstrip().startswith("|"):
            inside = False  # a setext heading (`Text` then `---`) ends the section
            prev_text = None
            continue
        if SECTION_END_RE.match(line):
            inside = False
            continue
        prev_text = line if line.strip() else prev_text
        m = ROW_RE.match(line)
        if not m:
            continue''')

    # 3. K10: follow an in-lane symlinked knowledge directory (containment still enforced)
    sub('for dirpath, dirnames, filenames in os.walk(base):',
        'for dirpath, dirnames, filenames in os.walk(base, followlinks=True):')

    # 4. K11 + K13: read the revision through ls-tree/cat-file, resolving a symlink inside the tree
    sub('''    if revision:
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
        return bodies, None''',
        '''    if revision:
        proc = _git(root, "ls-tree", "-r", "-z", revision)
        if proc.returncode != 0:
            return None, f"cannot list {revision[:12]}: {_text(proc).strip()}"
        entries = {}
        for chunk in proc.stdout.split(b"\\0"):
            if not chunk:
                continue
            meta, _, name = chunk.partition(b"\\t")
            fields = meta.split()
            if len(fields) != 3:
                continue
            entries[name] = (fields[0], fields[1], fields[2])
        bodies = {}
        for name in sorted(entries):
            mode, _typ, sha = entries[name]
            rel = name.decode("utf-8", "surrogateescape")
            if not rel.startswith(KNOWLEDGE_REL + "/") or not rel.endswith(".md"):
                continue
            if mode == b"120000":  # a committed symlink: resolve it inside the tree, never read its target string
                target = _blob(root, sha)
                if target is None:
                    return None, f"cannot read {rel} at {revision[:12]}"
                resolved = _resolve_in_tree(entries, rel, target)
                if resolved is None:
                    continue  # a link that leaves the tree carries no citation
                content = _blob(root, entries[resolved][2])
                if content is None:
                    return None, f"cannot read {resolved!r} at {revision[:12]}"
            else:
                content = _blob(root, sha)
                if content is None:
                    return None, f"cannot read {rel} at {revision[:12]}"
            bodies[rel] = content.decode("utf-8", "replace")
        if not bodies:
            return None, f"no knowledge file at {revision[:12]}"
        return bodies, None''')

    # 5. helpers: _blob and _resolve_in_tree
    sub('''def _nul_paths(data):''',
        '''def _blob(root, sha):
    """The bytes of a blob, addressed by sha (never by path: a path may not be UTF-8)."""
    proc = _git(root, "cat-file", "blob", sha.decode("ascii"))
    if proc.returncode != 0:
        return None
    return proc.stdout


def _resolve_in_tree(entries, rel, target):
    """The tree path a committed symlink points at, or None when it leaves the tree."""
    text = target.decode("utf-8", "replace").strip()
    if not text or text.startswith("/"):
        return None
    base = posixpath.dirname(rel)
    resolved = posixpath.normpath(posixpath.join(base, text))
    if resolved.startswith("..") or resolved.startswith("/"):
        return None
    key = os.fsencode(resolved)
    if key in entries and entries[key][0] != b"120000":
        return key
    return None


def _nul_paths(data):''')

    # 6. import posixpath
    sub('import os\nimport re\n', 'import os\nimport posixpath\nimport re\n')

    # 7. K12: a registry symlinked out of the lane is refused
    sub('''    path = os.path.join(root, REGISTRY_REL)
    if not os.path.isfile(path):
        return None, f"registry absent: {REGISTRY_REL}"
    try:''',
        '''    path = os.path.join(root, REGISTRY_REL)
    if not os.path.isfile(path):
        return None, f"registry absent: {REGISTRY_REL}"
    root_real = os.path.realpath(root)
    reg_real = os.path.realpath(path)
    if reg_real != root_real and not reg_real.startswith(root_real + os.sep):
        return None, f"registry outside the lane: {REGISTRY_REL}"
    try:''')

    # 8. K14: a --root below a repository toplevel is unevaluable (revision mode: git would read the ancestor)
    sub('''def evaluate(root, revision=None, fleet=None):
    root = os.path.abspath(root)
    rev = None
    if revision:
        rev = resolve_revision(root, revision)''',
        '''def evaluate(root, revision=None, fleet=None):
    root = os.path.abspath(root)
    rev = None
    if revision:
        top = _git(root, "rev-parse", "--show-toplevel")
        if top.returncode == 0:
            toplevel = os.path.realpath(_text(top).strip())
            if toplevel != os.path.realpath(root):
                return _err(f"root {root} is not the toplevel of its repository")
        rev = resolve_revision(root, revision)''')

    # 9. P6: the selftest must hold at least 66 cases -> the extra cases live in ref_cases.py (spliced in main())
    sub('''        ("a quote-character knowledge path is read at a revision", case_revision_reads_quote_character_path),
    ]''', '''        ("a quote-character knowledge path is read at a revision", case_revision_reads_quote_character_path),
    ] + EXTRA_CASES''')

    return src


def main():
    path = os.path.join(FIX, TOOL)
    pristine = subprocess.run(["git", "-C", FIX, "show", "45a92b64ac8a0f82dba369100e30682f14de81fb:" + TOOL],
                              capture_output=True)
    assert pristine.returncode == 0, pristine.stderr.decode()
    src = pristine.stdout.decode("utf-8")
    out = patch(src)
    with open(os.path.join(S, "ref_cases.py"), encoding="utf-8") as fh:
        cases_src = fh.read()
    anchor = "def _cases():"
    assert out.count(anchor) == 1
    out = out.replace(anchor, "NL = chr(10)\n" + cases_src + "\n" + anchor)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)
    print("patched", path, len(src), "->", len(out))
    r = subprocess.run([sys.executable, "-B", path, "--selftest"], capture_output=True, text=True)
    print("selftest rc", r.returncode)
    print(r.stdout[-3000:])
    print(r.stderr[-2000:])


if __name__ == "__main__":
    main()
