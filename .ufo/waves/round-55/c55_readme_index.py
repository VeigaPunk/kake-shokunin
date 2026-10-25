#!/usr/bin/env python3
"""Round-55 C1 counter (version 2) — calibration: the README coverage map against the knowledge tree.

Surface: `corpus/README.md` section `## Coverage map` is the lane's own statement of what
`corpus/knowledge/` holds ("An index row is a claim", CORPUS.md). This counter counts the
mismatches between that statement and the committed tree, reading committed bytes only
(`git ls-tree`, `git show`; no worktree reads, no network).

Version 2 (before any build was measured) folds in the wave-1 pre-data attacks
(`w1/CriticC1Contract.md` A1..A10 / WR1..WR6, `w1/MutC1Counter.md` M01..M16): constant-cell and
mega-row junk, population swaps, nested files, cross-reference-as-index, entry-edited-to-fit,
subject-mention false dangling, header-named columns, one authority per surface. The frozen
predicate sentence is unchanged.

Frozen predicate (the same sentence appears in `contract.md`, here and in every receipt):

    met: index_mismatches == 0 AND knowledge_files >= 46

`index_mismatches` = unindexed + multi + thin + duplicate + head_changed + deleted + dangling:

  unindexed  files (any depth) under `corpus/knowledge/` that no coverage-map row names, in its
             Entry cell, as `knowledge/<relative path>` (boundary: the next character is not
             [A-Za-z0-9_-] and not `.` followed by [A-Za-z0-9]).
  multi      coverage-map rows whose Entry cell names more than 2 distinct knowledge files.
  thin       rows naming a file whose Coverage cell has fewer than 5 whitespace tokens or shares
             no word with the file's own head (its H1 line plus first 1500 characters; 5+ letter
             ASCII words outside the stoplist and outside any word found in 40%+ of the knowledge
             files' heads, or a CJK bigram).
  duplicate  rows whose normalized Coverage cell repeats an earlier row's cell.
  head_changed files present at the base revision whose full base text is not preserved
             byte-for-byte as a prefix at the measured revision (entries change only by appended text).
  deleted    files present at the base revision and absent at the measured revision.
  dangling   backticked path tokens in the section (extensions md py mjs json sh txt csv yml yaml
             toml html xml, brace sets expanded) that resolve nowhere under corpus/,
             corpus/knowledge/, corpus/lessons/, the lane root at the revision; protocol file
             names (robots.txt, security.txt, ...) are exempt.

`knowledge_files >= 46` is the shrinkage guard: the tree held 46 knowledge files at the round base.
`## Coverage map` must occur exactly once; otherwise exit 2. Only the first contiguous table of the
section holds index rows (later tables, e.g. the frontier ground map, never index a file, but their
backticked pointers are still checked by `dangling`). The Entry and Coverage columns are found by
header name (fallback: second and last).

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable, 64 usage.
"""
from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile

PREDICATE = "met: index_mismatches == 0 AND knowledge_files >= 46"
FLOOR = 46
BASE_REV = "fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d"
README = "corpus/README.md"
KNOW_DIR = "corpus/knowledge/"
BASES = ("corpus/", "corpus/knowledge/", "corpus/lessons/", "")
EXTS = ("md", "py", "mjs", "json", "sh", "txt", "csv", "yml", "yaml", "toml", "html", "xml",
        "png", "svg", "jpg", "jpeg", "gif", "pdf", "log", "jsonl", "ndjson", "tsv")
PROTOCOL_NAMES = {"robots.txt", "security.txt", "sitemap.xml", "humans.txt", "ads.txt", "llms.txt"}
MAX_FILES_PER_ROW = 2
STOP = {"source", "knowledge", "verified", "recheck", "ground", "entry", "round", "notes", "about",
        "which", "their", "there", "these", "those", "other"}
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
REF_RE = re.compile(r"knowledge/([A-Za-z0-9_./-]+?\.(?:md|json))(?![A-Za-z0-9_-])(?!\.[A-Za-z0-9])")
TOKEN_RE = re.compile(r"`([^`\s]+)`|\]\(([^)\s]+)\)")
LINESUFFIX_RE = re.compile(r"(?::\d+(?:-\d+)?|#[^/]*)$")


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


def coverage_sections(text: str) -> list[str]:
    return re.findall(r"(?m)^## Coverage map[ \t]*\n(.*?)(?=^## |\Z)", text, re.S)


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
        if posixpath.normpath(posixpath.join(base, token)) in files:
            return True
    return False


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z0-9-]{4,}", text.lower()) if w not in STOP}


def bigrams(text: str) -> set[str]:
    chars = [c for c in text if CJK.match(c)]
    return {a + b for a, b in zip(chars, chars[1:])}


def h1_of(body: str) -> str | None:
    return next((ln for ln in body.splitlines() if ln.startswith("# ")), None)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def measure(root: str, rev: str, base_rev: str = BASE_REV) -> tuple[int, dict]:
    files = tree(root, rev)
    readme = show(root, rev, README)
    base_files = tree(root, base_rev)
    if files is None or readme is None or base_files is None:
        return 2, {"error": f"cannot read tree/{README} at {rev} or the base tree at {base_rev}"}
    sections = coverage_sections(readme)
    if len(sections) != 1:
        return 2, {"error": f"expected exactly one '## Coverage map' section, found {len(sections)}"}
    section = sections[0]
    lines: list[str] = []
    for ln in section.splitlines():
        if ln.startswith("|"):
            lines.append(ln)
        elif lines:
            break  # only the first contiguous table is the coverage map; later tables are not index rows
    if len(lines) < 2:
        return 2, {"error": "coverage map has no table"}
    header = [c.strip().lower() for c in lines[0].strip().strip("|").split("|")]
    e_idx = header.index("entry") if "entry" in header else 1
    c_idx = header.index("coverage") if "coverage" in header else -1
    rows = []
    for ln in lines[2:]:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        rows.append({"line": ln, "entry": cells[e_idx] if e_idx < len(cells) else "",
                     "cov": cells[c_idx] if c_idx < len(cells) else cells[-1]})
    know = sorted(p[len(KNOW_DIR):] for p in files if p.startswith(KNOW_DIR))
    base_know = sorted(p[len(KNOW_DIR):] for p in base_files if p.startswith(KNOW_DIR))
    pools = {rel: words((h1_of(b) or "") + "\n" + b[:1500])
             for rel in know for b in [show(root, rev, KNOW_DIR + rel) or ""]}
    freq: dict[str, int] = {}
    for pool in pools.values():
        for w in pool:
            freq[w] = freq.get(w, 0) + 1
    common = {w for w, k in freq.items() if know and k / len(know) >= 0.4}
    unindexed: list[str] = []
    thin: list[str] = []
    named_rows: dict[str, dict] = {}
    multi: list[str] = []
    for row in rows:
        refs = sorted(set(REF_RE.findall(row["entry"])))
        if len(refs) > MAX_FILES_PER_ROW:
            multi.append(row["entry"][:60])
        for ref in refs:
            named_rows.setdefault(ref, row)
    for rel in know:
        row = named_rows.get(rel)
        if row is None:
            unindexed.append(rel)
            continue
        body = show(root, rev, KNOW_DIR + rel) or ""
        head = (h1_of(body) or "") + "\n" + body[:1500]
        shared = ((words(row["cov"]) & pools[rel]) - common) or (bigrams(row["cov"]) & bigrams(head))
        if len(row["cov"].split()) < 5 or not shared:
            thin.append(rel)
    seen: set[str] = set()
    duplicate: list[str] = []
    for row in rows:
        key = norm(row["cov"])
        if key in seen:
            duplicate.append(row["cov"][:60])
        seen.add(key)
    head_changed: list[str] = []
    for rel in base_know:
        if (KNOW_DIR + rel) in files:
            old = show(root, base_rev, KNOW_DIR + rel) or ""
            new = show(root, rev, KNOW_DIR + rel) or ""
            if not new.startswith(old):
                head_changed.append(rel)
    deleted = [rel for rel in base_know if (KNOW_DIR + rel) not in files]
    dangling: list[str] = []
    toks = {a or b for a, b in TOKEN_RE.findall(section)}
    for tok in sorted(LINESUFFIX_RE.sub("", t) for t in toks):
        name = tok.rsplit("/", 1)[-1]
        has_ext = "." in name and name.rsplit(".", 1)[-1] in EXTS
        if name in PROTOCOL_NAMES or not has_ext:
            continue
        if any(ch in tok for ch in "<>*") or tok.startswith(("http://", "https://", "/")):
            continue
        for item in expand(tok):
            if not resolves(files, item):
                dangling.append(item)
    mismatches = (len(unindexed) + len(multi) + len(thin) + len(duplicate)
                  + len(head_changed) + len(deleted) + len(dangling))
    facts = {
        "knowledge_files": len(know),
        "coverage_rows": len(rows),
        "unindexed": unindexed, "multi": multi, "thin": thin, "duplicate": duplicate,
        "head_changed": head_changed, "deleted": deleted, "dangling": dangling,
        "index_mismatches": mismatches,
    }
    met = mismatches == 0 and len(know) >= FLOOR
    return (0 if met else 1), facts


# --------------------------------------------------------------------------- selftest

TERMS = ("unindexed", "multi", "thin", "duplicate", "head_changed", "deleted", "dangling")


def _fixture(files: dict[str, str], later: dict[str, str] | None = None,
             tip_know: dict[str, str] | None = None,
             gone: tuple[str, ...] = ()) -> tuple[str, str, str]:
    d = tempfile.mkdtemp(prefix="c55-idx-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    top = git(d, "rev-parse", "--show-toplevel")[1].strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise RuntimeError("fixture repo toplevel mismatch")

    def commit(batch: dict[str, str], msg: str) -> str:
        for rel, text in batch.items():
            tgt = os.path.join(d, rel)
            os.makedirs(os.path.dirname(tgt), exist_ok=True)
            with open(tgt, "w", encoding="utf-8") as fh:
                fh.write(text)
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                        "commit", "-q", "--allow-empty", "-m", msg], check=True)
        return git(d, "rev-parse", "HEAD")[1].strip()

    base = commit({k: v for k, v in files.items() if k.startswith(KNOW_DIR)}, "base")
    for rel in gone:  # committed at base, removed before the tip commit (`git add -A` records the deletion)
        os.remove(os.path.join(d, rel))
    tip = commit({**{k: v for k, v in files.items() if not k.startswith(KNOW_DIR)}, **(tip_know or {})}, "tip")
    if later:  # worktree edit after the commit: committed bytes must stay authoritative
        for rel, text in later.items():
            with open(os.path.join(d, rel), "w", encoding="utf-8") as fh:
                fh.write(text)
    return d, base, tip


def selftest() -> int:
    N = 46

    def body(i: int, h1: str | None = None) -> str:
        return f"# {h1 or f'Widget{i} cache invalidation rules'}\n\nsource: S900\n\nWidget{i} cache rules text.\n"

    def good(i: int) -> str:
        return f"| a{i} | `knowledge/e{i}.md` | Widget{i} cache invalidation rules described in full |"

    def readme(rows, extra="", head="| Area | Entry | Coverage |\n|---|---|---|\n"):
        return "# t\n\n## Coverage map\n\n" + head + "\n".join(rows) + "\n" + extra + "\n## Known gaps\n\nnone\n"

    ents = {f"{KNOW_DIR}e{i}.md": body(i) for i in range(N)}
    rows = [good(i) for i in range(N)]
    cases: dict[str, tuple] = {}

    def case(name, files, want, expect=None, later=None, tip_know=None, gone=()):
        cases[name] = (files, want, expect, later, tip_know, gone)

    case("pass", {**ents, README: readme(rows)}, 0, {"knowledge_files": N, "coverage_rows": N})
    case("fail_unindexed", {**ents, README: readme(rows[1:])}, 1, {"unindexed": 1})
    case("fail_floor_literal", {**{k: v for k, v in ents.items() if k != f"{KNOW_DIR}e0.md"},
                                README: readme(rows[1:])}, 1, {"deleted": 0})
    case("fail_thin_short", {**ents, README: readme(rows[:1] + ["| a1 | `knowledge/e1.md` | TBD |"] + rows[2:])}, 1, {"thin": 1})
    case("pass_five_tokens", {**ents, README: readme(
        ["| a0 | `knowledge/e0.md` | Widget0 cache invalidation rules verbatim |"] + rows[1:])}, 0)
    case("fail_thin_offtopic", {**ents, README: readme(
        rows[:1] + ["| a1 | `knowledge/e1.md` | totally unrelated gardening notes here |"] + rows[2:])}, 1, {"thin": 1})
    case("fail_thin_short_words", {**ents, README: readme(
        rows[:1] + ["| a1 | `knowledge/e1.md` | just text here and more |"] + rows[2:])}, 1, {"thin": 1})
    case("fail_thin_only_beyond_window", {**{k: v for k, v in ents.items() if k != f"{KNOW_DIR}e1.md"},
                                      f"{KNOW_DIR}e1.md": "# Plain heading\n\nsource: S900\n\n" + "filler block prose on unrelated matters. " * 40 + "zonkeys graze quietly.\n",
                                      README: readme(rows[:1] + ["| a1 | `knowledge/e1.md` | entirely different note about zonkeys |"] + rows[2:])}, 1, {"thin": 1})
    case("fail_common_words_only", {**ents, README: readme(
        rows[:1] + ["| a1 | `knowledge/e1.md` | cache invalidation rules described fully |"] + rows[2:])}, 1, {"thin": 1})
    case("fail_constant_cell", {**ents, README: readme(
        [f"| a{i} | `knowledge/e{i}.md` | source knowledge note filler text |" for i in range(N)])}, 1)
    case("fail_duplicate_cell", {**ents, README: readme(
        rows[:2] + ["| a2 | `knowledge/e2.md` | Widget1 cache invalidation rules described in full Widget2 |",
                    "| a3 | `knowledge/e3.md` | Widget1 cache invalidation rules described in full Widget2 |"] + rows[4:])}, 1, {"duplicate": 1})
    case("fail_mega_row", {**ents, README: readme(
        ["| all | " + " ".join(f"`knowledge/e{i}.md`" for i in range(N)) + " | Widget0 cache invalidation rules described in full |"])}, 1, {"multi": 1})
    case("pass_two_files_one_row", {**ents, README: readme(
        ["| a0 | `knowledge/e0.md` + `knowledge/e1.md` | Widget0 and Widget1 cache invalidation rules described in full |", rows[1]] + rows[2:])}, 0)
    case("fail_cross_reference_not_index", {**ents, README: readme(
        rows[1:] + ["| a0 | `knowledge/other.md` | Widget0 cache invalidation rules, see knowledge/e0.md |"])}, 1, {"unindexed": 1})
    case("fail_prefix_name", {**ents, README: readme(
        rows[:1] + ["| a1 | `knowledge/e1.md.bak` | Widget1 cache invalidation rules described in full |"] + rows[2:])}, 1, {"unindexed": 1})
    case("fail_nested_unindexed", {**ents, f"{KNOW_DIR}archive/stale.md": body(99), README: readme(rows)}, 1, {"unindexed": 1, "knowledge_files": N + 1})
    case("pass_nested_indexed", {**ents, f"{KNOW_DIR}archive/stale.md": body(99), README: readme(
        rows + ["| z | `knowledge/archive/stale.md` | Widget99 cache invalidation rules described in full |"])}, 0)
    case("fail_unindexed_json", {**ents, f"{KNOW_DIR}zz.json": '{"note": "x"}', README: readme(rows)}, 1, {"unindexed": 1})
    case("fail_dangling_md", {**ents, README: readme(rows, "See `knowledge/nope.md`.\n")}, 1, {"dangling": 1})
    case("fail_dangling_json", {**ents, README: readme(rows, "Snapshot: `data.json`.\n")}, 1, {"dangling": 1})
    case("pass_protocol_name_exempt", {**ents, README: readme(rows[:1] + [
        "| r | `knowledge/e1.md` | Widget1 cache invalidation rules, subject `robots.txt` and `security.txt` |"] + rows[2:])}, 0)
    case("pass_brace_expands", {**ents, "corpus/lessons/round-1.md": "x", "corpus/lessons/round-3.md": "x",
                                README: readme(rows, "See `round-{1,3}.md`.\n")}, 0)
    case("fail_brace_member_missing", {**ents, "corpus/lessons/round-1.md": "x", README: readme(rows, "See `round-{1,3}.md`.\n")}, 1, {"dangling": 1})
    case("pass_lane_root_base", {**ents, "notes.txt": "x", README: readme(rows, "Runbook: `notes.txt`.\n")}, 0)
    case("fail_swap_population", {**{k: v for k, v in ents.items() if k not in
                                       {f"{KNOW_DIR}e{i}.md" for i in range(10)}},
                                  **{f"{KNOW_DIR}stub{i}.md": "# Stub\n\nsource: none\n" for i in range(10)},
                                  README: readme(rows[10:] + [f"| s{i} | `knowledge/stub{i}.md` | Stub entry filler words" + f" more{i} |" for i in range(10)])}, 1, {"knowledge_files": N})
    case("fail_head_edited_to_fit", {**ents, README: readme(
        rows[:1] + ["| a1 | `knowledge/e1.md` | totally unrelated gardening notes here |"] + rows[2:])}, 1,
         {"head_changed": 1}, None, {f"{KNOW_DIR}e1.md": body(1, "Totally unrelated gardening notes")})
    case("pass_entry_appended_correction", {**ents, README: readme(rows)}, 0, {"head_changed": 0}, None,
         {f"{KNOW_DIR}e1.md": body(1) + "\n[r55-correction] appended text\n"})
    case("fail_two_sections", {**ents, README: readme(rows) + "\n## Coverage map\n\n| Area | Entry | Coverage |\n|---|---|---|\n"}, 2)
    case("fail_no_section", {**ents, README: "# t\n\n## Other\n\n| a | b | c |\n"}, 2)
    case("pass_columns_by_header", {**ents, README: readme(
        [f"| a{i} | Widget{i} cache invalidation rules described in full | `knowledge/e{i}.md` | S900 |" for i in range(N)],
        head="| Area | Coverage | Entry | Source |\n|---|---|---|---|\n")}, 0)
    case("pass_second_table_pointers_checked", {**ents, README: readme(rows, "\n### Map\n\n| G | R | E |\n|---|---|---|\n| x | r1 | `knowledge/e3.md` |\n")}, 0)
    case("fail_second_table_does_not_index", {**ents, README: readme(rows[1:], "\n### Map\n\n| G | Entry | Coverage |\n|---|---|---|\n| x | `knowledge/e0.md` | Widget0 cache invalidation rules described in full |\n")}, 1, {"unindexed": 1})
    case("fail_second_table_dangling", {**ents, README: readme(rows, "\n### Map\n\n| G | R | E |\n|---|---|---|\n| x | r1 | `knowledge/ghost.md` |\n")}, 1, {"dangling": 1})
    case("fail_deleted_base_file", {**ents, f"{KNOW_DIR}zz-old.md": body(98), README: readme(rows)}, 1,
         {"deleted": 1}, None, None, (f"{KNOW_DIR}zz-old.md",))
    case("fail_four_token_cell", {**ents, README: readme(
        rows[:1] + ["| a1 | `knowledge/e1.md` | Widget1 cache invalidation rules |"] + rows[2:])}, 1, {"thin": 1})
    case("fail_duplicate_sole_term", {**ents, README: readme(
        rows[:1] + ["| a1 | `knowledge/e1.md` | Widget1 and Widget2 cache invalidation rules described in full |",
                    "| a2 | `knowledge/e2.md` | Widget1 and Widget2 cache invalidation rules described in full |"] + rows[3:])}, 1,
         {"duplicate": 1, "thin": 0})
    case("fail_multi_sole_term", {**ents, README: readme(
        rows[:1] + ["| m | `knowledge/e1.md` `knowledge/e2.md` `knowledge/e3.md` | Widget1 Widget2 Widget3 cache invalidation rules described in full |"]
        + rows[4:])}, 1, {"multi": 1, "thin": 0})
    case("fail_body_truncated", {**ents, README: readme(rows)}, 1, {"head_changed": 1}, None,
         {f"{KNOW_DIR}e1.md": "# Widget1 cache invalidation rules\n"})
    case("fail_markdown_link_dangling", {**ents, README: readme(rows, "See [old map](knowledge/ghost-index.md).\n")}, 1, {"dangling": 1})
    case("fail_line_suffix_pointer_dangling", {**ents, README: readme(rows, "See `knowledge/nope.md:9999-10000`.\n")}, 1, {"dangling": 1})
    case("pass_line_suffix_pointer_resolves", {**ents, README: readme(rows, "See `knowledge/e1.md:3-4`.\n")}, 0)
    case("fail_image_pointer_dangling", {**ents, README: readme(rows, "See `knowledge/ghost.png`.\n")}, 1, {"dangling": 1})
    case("pass_head_only_committed_bytes", {**ents, README: readme(rows)}, 0, None,
         {README: readme(rows[:1] + ["| a1 | `knowledge/e1.md` | TBD |"] + rows[2:])})
    case("pass_cjk_bigram", {**{k: v for k, v in ents.items() if k != f"{KNOW_DIR}e0.md"},
                             f"{KNOW_DIR}e0.md": "# ヤフー ロボット 規則\n\nsource: S900\n",
                             README: readme(["| a0 | `knowledge/e0.md` | ロボット の 拒否 規則 と パターン 構文 |"] + rows[1:])}, 0)

    passed, fails = 0, []
    for name, (files, want, expect, later, tip_know, gone) in sorted(cases.items()):
        d, base, tip = _fixture(files, later, tip_know, gone)
        try:
            code, facts = measure(d, tip, base)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        ok = code == want
        if ok and expect and code != 2:
            for key, val in expect.items():
                got = facts[key] if isinstance(facts[key], int) else len(facts[key])
                if got != val:
                    ok = False
                    fails.append(f"{name}: fact {key} expected {val}, got {got}")
        if ok:
            passed += 1
        elif code != want:
            fails.append(f"{name}: expected {want}, got {code}" + (f" {facts.get('error', '')}" if code == 2 else
                         f" {({k: facts[k] for k in TERMS if facts[k]})}"))
    print(f"c55 readme-index selftest: {passed}/{len(cases)}")
    for line in fails:
        print("  FAIL", line)
    return 0 if passed == len(cases) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Round-55 C1 counter v2 (README coverage-map calibration)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.revision:
        print("usage: --revision is required unless --selftest is used", file=sys.stderr)
        return 64
    code, facts = measure(args.root, args.revision)
    if code == 2:
        print(f"C1 unevaluable: {facts.get('error')}")
        print("EXIT=2")
        return 2
    if args.json:
        print(json.dumps({"schema": "kake-r55-c1-readme-index-v2", "predicate": PREDICATE,
                          "revision": args.revision, "exit": code, **facts, "met": code == 0},
                         indent=1, ensure_ascii=False))
        return code
    print(f"C1 readme-index index_mismatches={facts['index_mismatches']} "
          f"knowledge_files={facts['knowledge_files']} met={code == 0}  ({PREDICATE})")
    print("  " + " ".join(f"{k}={len(facts[k])}" for k in TERMS) + f" coverage_rows={facts['coverage_rows']}")
    for key in TERMS:
        for item in facts[key]:
            print(f"    {key}: {item}")
    print(f"  revision: {args.revision}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
