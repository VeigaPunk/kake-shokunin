#!/usr/bin/env python3
"""Round-59 w1 seat ExecResolverOtherRoutes — probe batch 2.

Adds:
  * routes not covered by batch 1: form-feed / U+2028 line-splitting inside a
    registry cell, fullwidth "S" lookalike, HTML blocks other than <pre>,
    a fake `## Registry` heading inside an HTML comment, list-item continuation
    rows at 3 spaces, ids inside URLs in knowledge code fences / HTML comments,
    a reference-style sibling row (url-match loss),
  * tool VARIANTS in scratch (the lane tool is never modified):
      narrow_html  : HTML-comment awareness only  (a plausible K8 fix)
      full_html    : HTML-block awareness for comments + pre/script/style/textarea/details
      ascii_ids    : [0-9] instead of \d in the id regexes
      lf_split     : splitlines("\n") instead of splitlines()
  * the same cases at --revision (git-committed blobs), since C2 is measured at a
    revision.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys

SEAT = "/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK = os.path.join(SEAT, "work2")
TOOL = os.path.join(SEAT, "tool", "id_resolver.py")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"

HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|\n")


def row(sid: str, url: str = "https://e.example/src", indent: str = "") -> str:
    return (f"{indent}| {sid} | fixture source — {url} | docs | A | scope | anchor | teaches | "
            f"mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n")


def reg(body: str) -> str:
    return "# Sources\n\n## Registry\n\n" + HDR + body


def write(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)


def build(case, registry: bytes, knowledge: dict[str, bytes], sibling: bytes | None = None):
    root = os.path.join(WORK, case)
    if os.path.exists(root):
        shutil.rmtree(root)
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    write(os.path.join(lane, "corpus", "SOURCES.md"), registry)
    for rel, body in knowledge.items():
        write(os.path.join(lane, "corpus", "knowledge", rel), body)
    if sibling is not None:
        write(os.path.join(fleet, "alpha-shokunin", "corpus", "SOURCES.md"), sibling)
    return fleet, lane


def commit(path: str) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    subprocess.run(["git", "-C", path, "init", "-q"], check=True, env=env)
    top = subprocess.run(["git", "-C", path, "rev-parse", "--show-toplevel"], capture_output=True,
                         env=env, text=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(path):
        raise RuntimeError("toplevel mismatch")
    subprocess.run(["git", "-C", path, "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", path, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                    "-c", "commit.gpgsign=false", "commit", "-q", "-m", "fixture"], check=True, env=env)
    return subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True,
                          env=env, text=True).stdout.strip()


def run_tool(tool: str, lane: str, fleet: str, revision: str | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C.UTF-8"
    argv = [sys.executable, "-B", tool, "--root", lane, "--fleet", fleet]
    if revision:
        argv += ["--revision", revision]
    p = subprocess.run(argv, capture_output=True, env=env, timeout=300)
    return {"exit": p.returncode, "out": (p.stdout + p.stderr).decode("utf-8", "replace").strip()}


def run_census(lane: str) -> dict:
    env = dict(os.environ)
    env["LC_ALL"] = "C.UTF-8"
    c = subprocess.run([CENSUS, "census", "--root", lane, lane], capture_output=True, env=env, timeout=300)
    v = subprocess.run([CENSUS, "validate", "--today", "2026-10-26", lane], capture_output=True, env=env, timeout=300)
    rows = None
    for line in c.stdout.decode("utf-8", "replace").splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[1] == "rows":
            rows = parts[2]
    findings = [ln for ln in v.stdout.decode("utf-8", "replace").splitlines() if "\tE" in ln]
    return {"rows": rows, "census_exit": c.returncode, "validate_exit": v.returncode, "findings": findings}


# --------------------------------------------------------------- variants ---
VARDIR = os.path.join(SEAT, "variants")
os.makedirs(VARDIR, exist_ok=True)
SRC = open(TOOL, encoding="utf-8").read()

NARROW_HTML = '''
_HTML_COMMENT_RE = re.compile(r"<!--")
'''
# --- narrow variant: strip HTML comments (block comments) before parsing rows
narrow = SRC.replace(
    '''def parse_registry(text):
    """Map id -> [urls] for rows of the `## Registry` section (0-3 leading spaces, outside fenced code)."""
    rows = {}''',
    '''def _strip_html_comments(text):
    """Remove HTML comments (CommonMark: a comment runs to the line holding `-->`)."""
    out = []
    in_comment = False
    for raw in text.split("\\n"):
        line = raw.rstrip("\\r")
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
    return "\\n".join(out)


def parse_registry(text):
    """Map id -> [urls] for rows of the `## Registry` section (0-3 leading spaces, outside fenced code)."""
    text = _strip_html_comments(text)
    rows = {}''')
assert narrow != SRC
open(os.path.join(VARDIR, "narrow_html.py"), "w", encoding="utf-8").write(narrow)

# --- full variant: narrow + HTML block elements that hide markdown content
full = narrow.replace(
    '''def _strip_html_comments(text):''',
    '''_HTML_BLOCK_TAGS = ("pre", "script", "style", "textarea", "details", "div", "figure", "section",
                     "table", "ul", "ol", "blockquote")


def _strip_html_blocks(text):
    """Remove HTML blocks (a start tag line opens one; it closes on the matching end tag or a blank line)."""
    out = []
    open_tag = None
    for raw in text.split("\\n"):
        line = raw.rstrip("\\r")
        if open_tag is not None:
            if re.search(r"</" + open_tag + r"\\s*>", line) or not line.strip():
                open_tag = None
            continue
        m = re.match(r"^ {0,3}<(" + "|".join(_HTML_BLOCK_TAGS) + r")(\\s|>|/)", line)
        if m:
            open_tag = m.group(1)
            if re.search(r"</" + open_tag + r"\\s*>", line):
                open_tag = None
            continue
        out.append(line)
    return "\\n".join(out)


def _strip_html_comments(text):''')
full = full.replace(
    '''    text = _strip_html_comments(text)
    rows = {}''',
    '''    text = _strip_html_blocks(_strip_html_comments(text))
    rows = {}''')
assert full != narrow
open(os.path.join(VARDIR, "full_html.py"), "w", encoding="utf-8").write(full)

# --- ascii variant: ASCII-only digits in the id regexes
ascii_ids = SRC.replace('r"(?<![A-Za-z0-9_])S\\d{3,}(?![A-Za-z0-9_])"', 'r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])"')
ascii_ids = ascii_ids.replace('r"^S\\d{3,}$"', 'r"^S[0-9]{3,}$"')
assert ascii_ids != SRC
open(os.path.join(VARDIR, "ascii_ids.py"), "w", encoding="utf-8").write(ascii_ids)

# --- lf variant: split only on LF (the census/gawk record separator)
lf_split = SRC.replace("for raw in text.splitlines():", 'for raw in text.split("\\n"):')
assert lf_split != SRC
open(os.path.join(VARDIR, "lf_split.py"), "w", encoding="utf-8").write(lf_split)

VARIANTS = {
    "current": TOOL,
    "narrow_html": os.path.join(VARDIR, "narrow_html.py"),
    "full_html": os.path.join(VARDIR, "full_html.py"),
    "ascii_ids": os.path.join(VARDIR, "ascii_ids.py"),
    "lf_split": os.path.join(VARDIR, "lf_split.py"),
}

# ------------------------------------------------------------------ cases ---
CASES = []


def case(name, registry: bytes, knowledge: dict[str, bytes], sibling: bytes | None = None,
         note: str = ""):
    CASES.append(dict(name=name, registry=registry, knowledge=knowledge, sibling=sibling, note=note))


b = lambda s: s.encode("utf-8")

case("R9_formfeed_in_registry_cell",
     reg(row("S941", "https://e.example/941")).replace("https://e.example/941", "https://e.example/94\x0c1"),
     {"ok.md": b("Cites S941.\n")},
     note="form feed (U+000C) inside the source cell: Python splitlines() breaks the line, gawk does not")

case("R9b_u2028_in_registry_cell",
     reg(row("S942", "https://e.example/942")).replace("https://e.example/942", "https://e.example/94 2"),
     {"ok.md": b("Cites S942.\n")},
     note="U+2028 line separator inside the source cell")

case("R9c_u2028_before_id_cell",
     reg(row("S943", "https://e.example/943")).replace("| S943 |", "| | S943 |"),
     {"ok.md": b("Cites S943.\n")},
     note="U+2028 immediately before the id cell")

case("R10_fullwidth_S_lookalike",
     reg(row("S944", "https://e.example/944")),
     {"ok.md": b("Cites S944 and Ｓ945.\n")},
     note="fullwidth S (U+FF33) citation: invisible to the id regex")

case("R11_html_script_block",
     reg(row("S946", "https://e.example/946") + "<script>\n" + row("S947", "https://e.example/947") + "</script>\n"),
     {"ok.md": b("Cites S946 and S947.\n")},
     note="<script> block row")

case("R11b_html_textarea_block",
     reg(row("S948", "https://e.example/948") + "<textarea>\n" + row("S949", "https://e.example/949") + "</textarea>\n"),
     {"ok.md": b("Cites S948 and S949.\n")},
     note="<textarea> block row")

case("R12_fake_registry_heading_in_html_comment",
     reg(row("S950", "https://e.example/950")) + "<!--\n## Registry\n\n" + row("S951", "https://e.example/951") + "-->\n",
     {"ok.md": b("Cites S950 and S951.\n")},
     note="a fake Registry heading inside an HTML comment opens a second section")

case("R13_list_item_3space_continuation_row",
     reg(row("S952", "https://e.example/952")) + "- a note\n   | S953 | fixture — https://e.example/953 | docs | A | s | a | t | mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n",
     {"ok.md": b("Cites S952 and S953.\n")},
     note="list item continuation row at 3 spaces")

case("R14_id_in_url_in_knowledge_code_fence",
     reg(row("S954", "https://e.example/954")),
     {"ok.md": b("Cites S954.\n\n```\nhttps://e.example/p/S955\n```\n")},
     note="id inside a URL inside a fenced code block in a knowledge file")

case("R14b_id_in_url_in_knowledge_html_comment",
     reg(row("S956", "https://e.example/956")),
     {"ok.md": b("Cites S956.\n\n<!-- https://e.example/p/S957 -->\n")},
     note="id inside a URL inside an HTML comment in a knowledge file")

case("R15_sibling_reference_style_row",
     reg(row("S958", "https://e.example/958")),
     {"ok.md": b("Cites S959 (https://e.example/959).\n")},
     sibling=reg(row("S959", "[the source][r1]") + "\n[r1]: https://e.example/959\n"),
     note="sibling row uses a reference-style link: sibling URL is not extracted -> url-match lost")

case("R16_registry_row_with_reference_style_link",
     reg(row("S960", "[the source][r1]") + "\n[r1]: https://e.example/960\n"),
     {"ok.md": b("Cites S960.\n")},
     note="lane row uses a reference-style link: URL not extracted (url-match uses siblings only)")

case("R17_knowledge_link_ref_def_with_id",
     reg(row("S961", "https://e.example/961")),
     {"ok.md": b("Cites S961.\n\n[S962]: https://e.example/962\n")},
     note="link reference definition in a knowledge file: S962 counted as a citation")

case("R18_registry_heading_trailing_hash_then_real_heading",
     b("# Sources\n\n## Registry ##\n\n" + HDR + row("S963", "https://e.example/963")) + b("\n## Registry\n\n" + row("S964", "https://e.example/964")),
     {"ok.md": b("Cites S963 and S964.\n")},
     note="a trailing-hash heading first, then a real Registry heading")


def main() -> int:
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(VARDIR, exist_ok=True)
    results = []
    for spec in CASES:
        fleet, lane = build(spec["name"], spec["registry"], spec["knowledge"], spec.get("sibling"))
        head = commit(lane)
        cen = run_census(lane)
        entry = {"case": spec["name"], "note": spec["note"], "census": cen, "runs": {}}
        for vname, vpath in VARIANTS.items():
            wt = run_tool(vpath, lane, fleet)
            rv = run_tool(vpath, lane, fleet, revision=head)
            entry["runs"][vname] = {"worktree": wt, "revision": rv}
        results.append(entry)
        print("=" * 78)
        print("CASE", spec["name"], "|", spec["note"])
        print("  census rows:", cen["rows"], "validate exit:", cen["validate_exit"], cen["findings"])
        for vname in VARIANTS:
            wt = entry["runs"][vname]["worktree"]
            rv = entry["runs"][vname]["revision"]
            print(f"  {vname:12s} wt exit={wt['exit']} | rev exit={rv['exit']}")
            for line in wt["out"].splitlines():
                print("      wt |", line)
            if rv["out"] != wt["out"] or rv["exit"] != wt["exit"]:
                for line in rv["out"].splitlines():
                    print("      rv |", line)
    with open(os.path.join(SEAT, "results2.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print("\nwrote results2.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
