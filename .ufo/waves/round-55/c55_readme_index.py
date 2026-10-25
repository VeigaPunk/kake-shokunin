#!/usr/bin/env python3
"""Round-55 C1 counter — calibration: the README coverage map against the knowledge tree.

Surface: `corpus/README.md` section `## Coverage map` is the lane's own statement of what
`corpus/knowledge/` holds ("An index row is a claim", CORPUS.md). This counter counts the
mismatches between that statement and the committed tree, reading committed bytes only
(`git ls-tree`, `git show`; no worktree reads, no network).

Frozen predicate (the same sentence appears in `contract.md`, here and in every receipt):

    met: index_mismatches == 0 AND knowledge_files >= 46

`index_mismatches` = unindexed + thin + dangling, where, over the coverage-map section only:

  unindexed  files under `corpus/knowledge/` that no coverage-map row names as
             `knowledge/<basename>` (exact basename; the next character is not
             [A-Za-z0-9_.-]).
  thin       indexed files whose first naming row has a coverage cell (last cell) with fewer
             than 5 whitespace tokens, or sharing no 5+ letter word with the file's H1 line
             plus its first 1500 characters.
  dangling   backticked path tokens in the section (extensions md py mjs json sh txt, brace
             sets expanded, `../` normalised) that resolve nowhere under the candidate bases
             corpus/, corpus/knowledge/, corpus/lessons/, the lane root, at the revision.

`knowledge_files >= 46` is the deletion guard: the tree held 46 knowledge files at the round
base, so shrinking the population cannot meet the predicate.

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable, 64 usage.
"""
from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import subprocess
import sys
import tempfile

PREDICATE = "met: index_mismatches == 0 AND knowledge_files >= 46"
FLOOR = 46
README = "corpus/README.md"
KNOW_DIR = "corpus/knowledge/"
BASES = ("corpus/", "corpus/knowledge/", "corpus/lessons/", "")
EXTS = ("md", "py", "mjs", "json", "sh", "txt")
TOKEN_RE = re.compile(r"`([^`\s]+\.(?:" + "|".join(EXTS) + r"))`")


def git(root: str, *args: str) -> tuple[int, str]:
    proc = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True)
    return proc.returncode, proc.stdout


def show(root: str, rev: str, path: str) -> str | None:
    rc, out = git(root, "show", f"{rev}:{path}")
    return out if rc == 0 else None


def tree(root: str, rev: str) -> set[str] | None:
    rc, out = git(root, "ls-tree", "-r", "--name-only", rev)
    return set(out.splitlines()) if rc == 0 else None


def coverage_section(text: str) -> str | None:
    m = re.search(r"(?m)^## Coverage map\s*\n(.*?)(?=^## )", text, re.S)
    return m.group(1) if m else None


def expand(token: str) -> list[str]:
    m = re.search(r"\{([^{}]*)\}", token)
    if not m:
        return [token]
    out: list[str] = []
    for alt in m.group(1).split(","):
        out.extend(expand(token[:m.start()] + alt.strip() + token[m.end():]))
    return out


def resolves(files: set[str], token: str) -> bool:
    for base in BASES:
        cand = posixpath.normpath(posixpath.join(base, token))
        if cand in files:
            return True
    return False


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-z][a-z0-9-]{4,}", text.lower()))


def measure(root: str, rev: str) -> tuple[int, dict]:
    files = tree(root, rev)
    readme = show(root, rev, README)
    if files is None or readme is None:
        return 2, {"error": f"cannot read tree or {README} at {rev}"}
    section = coverage_section(readme)
    if section is None:
        return 2, {"error": "no '## Coverage map' section"}
    rows = [ln for ln in section.splitlines() if ln.startswith("|")][2:]
    know = sorted(p for p in files if p.startswith(KNOW_DIR) and "/" not in p[len(KNOW_DIR):])
    unindexed: list[str] = []
    thin: list[str] = []
    for path in know:
        base = path[len(KNOW_DIR):]
        pat = re.compile(r"knowledge/" + re.escape(base) + r"(?![A-Za-z0-9_.-])")
        hit = next((r for r in rows if pat.search(r)), None)
        if hit is None:
            unindexed.append(base)
            continue
        cells = [c.strip() for c in hit.strip().strip("|").split("|")]
        cov = cells[-1] if cells else ""
        body = show(root, rev, path) or ""
        h1 = next((ln for ln in body.splitlines() if ln.startswith("# ")), "")
        shared = words(cov) & words(h1 + "\n" + body[:1500])
        if len(cov.split()) < 5 or not shared:
            thin.append(base)
    dangling: list[str] = []
    for tok in sorted(set(TOKEN_RE.findall(section))):
        for item in expand(tok):
            if not resolves(files, item):
                dangling.append(item)
    mismatches = len(unindexed) + len(thin) + len(dangling)
    facts = {
        "knowledge_files": len(know),
        "coverage_rows": len(rows),
        "unindexed": unindexed,
        "thin": thin,
        "dangling": dangling,
        "index_mismatches": mismatches,
    }
    met = mismatches == 0 and len(know) >= FLOOR
    return (0 if met else 1), facts


# --------------------------------------------------------------------------- selftest


def _fixture(files: dict[str, str]) -> tuple[str, str]:
    d = tempfile.mkdtemp(prefix="c55-idx-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    rc, top = git(d, "rev-parse", "--show-toplevel")
    if os.path.realpath(top.strip()) != os.path.realpath(d):
        raise RuntimeError("fixture repo toplevel mismatch")
    for rel, text in files.items():
        tgt = os.path.join(d, rel)
        os.makedirs(os.path.dirname(tgt), exist_ok=True)
        with open(tgt, "w", encoding="utf-8") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                    "commit", "-q", "-m", "fixture"], check=True)
    return d, git(d, "rev-parse", "HEAD")[1].strip()


def selftest() -> int:
    import shutil
    entry = "# Widget cache invalidation rules\n\nsource: S900\n\nWidget cache rules text.\n"
    entries = {f"corpus/knowledge/e{i}.md": entry.replace("Widget", f"Widget{i}") for i in range(FLOOR)}
    def readme(rows, extra=""):
        head = "# t\n\n## Coverage map\n\n| Area | Entry | Coverage |\n|---|---|---|\n"
        return head + "\n".join(rows) + "\n" + extra + "\n## Known gaps\n\nnone\n"
    good_rows = [f"| a{i} | `knowledge/e{i}.md` | Widget{i} cache invalidation rules described in full |"
                 for i in range(FLOOR)]
    cases = {
        "pass": (dict(entries, **{README: readme(good_rows)}), 0),
        "fail_unindexed": (dict(entries, **{README: readme(good_rows[1:])}), 1),
        "fail_thin_short": (dict(entries, **{README: readme(
            good_rows[:1] + ["| a1 | `knowledge/e1.md` | TBD |"] + good_rows[2:])}), 1),
        "fail_thin_offtopic": (dict(entries, **{README: readme(
            good_rows[:1] + ["| a1 | `knowledge/e1.md` | totally unrelated gardening notes here |"]
            + good_rows[2:])}), 1),
        "fail_prefix_name": (dict(entries, **{README: readme(
            good_rows[:1] + ["| a1 | `knowledge/e1.md.bak` | Widget1 cache invalidation rules in full |"]
            + good_rows[2:])}), 1),
        "fail_dangling": (dict(entries, **{README: readme(good_rows, "See `knowledge/nope.md`.\n")}), 1),
        "pass_brace_expands": (dict(entries, **{"corpus/lessons/round-1.md": "x", "corpus/lessons/round-3.md": "x",
                                                README: readme(good_rows, "See `round-{1,3}.md`.\n")}), 0),
        "fail_brace_member_missing": (dict(entries, **{"corpus/lessons/round-1.md": "x",
                                                       README: readme(good_rows, "See `round-{1,3}.md`.\n")}), 1),
        "fail_deleted_population": ({k: v for k, v in entries.items() if k != "corpus/knowledge/e0.md"}
                                    | {README: readme(good_rows[1:])}, 1),
        "fail_no_section": (dict(entries, **{README: "# t\n\n## Other\n\n| a | b | c |\n"}), 2),
    }
    passed = 0
    fails: list[str] = []
    for name, (files, want) in sorted(cases.items()):
        d, rev = _fixture(files)
        try:
            code, _facts = measure(d, rev)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if code == want:
            passed += 1
        else:
            fails.append(f"{name}: expected {want}, got {code}")
    print(f"c55 readme-index selftest: {passed}/{len(cases)}")
    for line in fails:
        print("  FAIL", line)
    return 0 if passed == len(cases) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Round-55 C1 counter (README coverage-map calibration)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.revision:
        ap.error("--revision is required unless --selftest is used")
    code, facts = measure(args.root, args.revision)
    if code == 2:
        print(f"C1 unevaluable: {facts.get('error')}")
        print("EXIT=2")
        return 2
    if args.json:
        print(json.dumps({"schema": "kake-r55-c1-readme-index-v1", "predicate": PREDICATE,
                          "revision": args.revision, **facts, "met": code == 0},
                         indent=1, ensure_ascii=False))
    else:
        print(f"C1 readme-index index_mismatches={facts['index_mismatches']} "
              f"knowledge_files={facts['knowledge_files']} met={code == 0}  ({PREDICATE})")
        print(f"  unindexed={len(facts['unindexed'])} thin={len(facts['thin'])} "
              f"dangling={len(facts['dangling'])} coverage_rows={facts['coverage_rows']}")
        for key in ("unindexed", "thin", "dangling"):
            for item in facts[key]:
                print(f"    {key}: {item}")
        print(f"  revision: {args.revision}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
