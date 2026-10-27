#!/usr/bin/env python3
"""Round-59 w1 seat ExecResolverOtherRoutes — probe further false-green routes of
scripts/id_resolver.py (beyond K1-K14).

Every case is a scratch fixture fleet under the seat scratch dir:
  <work>/<case>/fleet/kake-shokunin/corpus/{SOURCES.md,knowledge/*.md}
  <work>/<case>/fleet/alpha-shokunin/corpus/SOURCES.md   (optional sibling)

For each case we run:
  * the resolver (working-tree mode)  -> exit code + stdout
  * the lane census reference parser (scripts/sources-census.sh, read-only, fleet root)
    -> rows count + E-codes (the resolver's documented "census parser's rule")

Nothing here writes outside the seat scratch dir.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys

SEAT = "/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK = os.path.join(SEAT, "work")
TOOL = os.path.join(SEAT, "tool", "id_resolver.py")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
LANE_TOOL = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py"

HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|\n")


def row(sid: str, url: str = "https://e.example/src", indent: str = "") -> str:
    return (f"{indent}| {sid} | fixture source — {url} | docs | A | scope | anchor | teaches | "
            f"mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n")


def reg(body: str) -> str:
    return "# Sources\n\n## Registry\n\n" + HDR + body


def write(path: str, text: str, crlf: bool = False) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = text.replace("\n", "\r\n") if crlf else text
    with open(path, "wb") as fh:
        fh.write(data.encode("utf-8"))


def build(case: str, registry: str, knowledge: dict[str, str], sibling: str | None = None,
          crlf_registry: bool = False, crlf_knowledge: bool = False) -> tuple[str, str]:
    root = os.path.join(WORK, case)
    if os.path.exists(root):
        shutil.rmtree(root)
    fleet = os.path.join(root, "fleet")
    lane = os.path.join(fleet, "kake-shokunin")
    write(os.path.join(lane, "corpus", "SOURCES.md"), registry, crlf=crlf_registry)
    for rel, body in knowledge.items():
        write(os.path.join(lane, "corpus", "knowledge", rel), body, crlf=crlf_knowledge)
    if sibling is not None:
        write(os.path.join(fleet, "alpha-shokunin", "corpus", "SOURCES.md"), sibling)
    return fleet, lane


def run_resolver(lane: str, fleet: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C.UTF-8"
    p = subprocess.run([sys.executable, "-B", TOOL, "--root", lane, "--fleet", fleet],
                       capture_output=True, env=env, timeout=300)
    text = (p.stdout + p.stderr).decode("utf-8", "replace")
    return {"exit": p.returncode, "out": text.strip()}


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
    e_codes = [ln for ln in v.stdout.decode("utf-8", "replace").splitlines() if "\tE" in ln]
    return {"census_rows": rows, "census_exit": c.returncode, "validate_exit": v.returncode,
            "validate_findings": e_codes}


CASES: list[dict] = []


def case(name: str, registry: str, knowledge: dict[str, str], sibling: str | None = None, **kw) -> None:
    CASES.append(dict(name=name, registry=registry, knowledge=knowledge, sibling=sibling, **kw))


# --- route 1: CRLF registry -------------------------------------------------
case("R1_crlf_registry",
     reg(row("S901", "https://e.example/901")),
     {"ok.md": "Cites S901.\n"},
     crlf_registry=True)

case("R1b_crlf_registry_and_knowledge",
     reg(row("S902", "https://e.example/902")),
     {"ok.md": "Cites S902.\n"},
     crlf_registry=True, crlf_knowledge=True)

# --- route 2: tab-indented rows -------------------------------------------
case("R2_tab_indented_row",
     reg(row("S903", "https://e.example/903", indent="\t")),
     {"ok.md": "Cites S903.\n"})

case("R2b_tab_indented_heading",
     "# Sources\n\n\t## Registry\n\n" + HDR + row("S904", "https://e.example/904"),
     {"ok.md": "Cites S904.\n"})

case("R2c_tab_inside_row_cells",
     reg(row("S905", "https://e.example/905").replace("| S905 |", "|\tS905\t|")),
     {"ok.md": "Cites S905.\n"})

# --- route 3: row inside an HTML block -------------------------------------
case("R3_html_pre_block",
     reg(row("S906", "https://e.example/906") + "<pre>\n" + row("S907", "https://e.example/907") + "</pre>\n"),
     {"ok.md": "Cites S906 and S907.\n"})

case("R3b_html_details_block",
     reg(row("S908", "https://e.example/908") + "<details>\n" + row("S909", "https://e.example/909") + "</details>\n"),
     {"ok.md": "Cites S908 and S909.\n"})

case("R3c_html_comment_block",
     reg(row("S910", "https://e.example/910") + "<!--\n" + row("S911", "https://e.example/911") + "-->\n"),
     {"ok.md": "Cites S910 and S911.\n"})

case("R3d_html_pre_before_registry",
     "<pre>\n" + row("S912", "https://e.example/912") + "</pre>\n\n" + reg(row("S913", "https://e.example/913")),
     {"ok.md": "Cites S912 and S913.\n"})

# --- route 4: link reference definition ------------------------------------
case("R4_link_ref_def_in_registry",
     reg(row("S914", "https://e.example/914") + "[ref1]: https://e.example/ref1\n"),
     {"ok.md": "Cites S914 and S915.\n"})

case("R4b_link_ref_def_in_knowledge",
     reg(row("S916", "https://e.example/916")),
     {"ok.md": "Cites S916.\n\n[S999]: https://e.example/999\n"})

case("R4c_registry_row_with_reference_style_link",
     reg(row("S917", "[the source][r1]") + "\n[r1]: https://e.example/917\n"),
     {"ok.md": "Cites S917.\n"})

# --- route 5: list item holding a pipe row --------------------------------
case("R5_list_item_pipe_row",
     reg(row("S918", "https://e.example/918") + "- | S919 | fixture — https://e.example/919 | docs | A | s | a | t | mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n"),
     {"ok.md": "Cites S918 and S919.\n"})

case("R5b_list_item_indented_pipe_row",
     reg(row("S920", "https://e.example/920") + "- a note\n  | S921 | fixture — https://e.example/921 | docs | A | s | a | t | mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n"),
     {"ok.md": "Cites S920 and S921.\n"})

case("R5c_blockquote_pipe_row",
     reg(row("S922", "https://e.example/922") + "> | S923 | fixture — https://e.example/923 | docs | A | s | a | t | mined | 2026-10-26 | 90d | corpus/knowledge/ok.md |\n"),
     {"ok.md": "Cites S922 and S923.\n"})

# --- route 6: registry heading with trailing #s ---------------------------
case("R6_heading_trailing_hashes",
     "# Sources\n\n## Registry ##\n\n" + HDR + row("S924", "https://e.example/924"),
     {"ok.md": "Cites S924.\n"})

case("R6b_heading_trailing_hashes_second_occurrence",
     reg(row("S925", "https://e.example/925")) + "\n## Registry ##\n\n" + row("S926", "https://e.example/926"),
     {"ok.md": "Cites S925 and S926.\n"})

case("R6c_heading_lowercase_registry",
     "# Sources\n\n## registry\n\n" + HDR + row("S927", "https://e.example/927"),
     {"ok.md": "Cites S927.\n"})

# --- route 7: unicode lookalike S -----------------------------------------
case("R7_fullwidth_digits_id",
     reg(row("S９２８", "https://e.example/928")),
     {"ok.md": "Cites S９２８.\n"})

case("R7b_cyrillic_lookalike_S_in_knowledge",
     reg(row("S929", "https://e.example/929")),
     {"ok.md": "Cites S929 and Ѕ930.\n"})

case("R7c_cyrillic_lookalike_S_in_registry",
     reg(row("Ѕ931", "https://e.example/931")),
     {"ok.md": "Cites Ѕ931.\n"})

case("R7d_ascii_id_cited_with_lookalike_S",
     reg(row("S932", "https://e.example/932")),
     {"ok.md": "Cites Ѕ932.\n"})

# --- route 8: ids inside URLs in knowledge files ---------------------------
case("R8_id_inside_url_in_knowledge",
     reg(row("S933", "https://e.example/933")),
     {"ok.md": "Cites S933. See https://e.example/page/S934 for details.\n"})

case("R8b_id_inside_url_not_in_registry",
     reg(row("S935", "https://e.example/935")),
     {"ok.md": "Cites S935. Mirror https://e.example/x/S936 here.\n"})

case("R8c_id_inside_url_in_registry_source_cell",
     reg(row("S937", "https://e.example/S938")),
     {"ok.md": "Cites S937.\n"})

case("R8d_id_in_url_matches_sibling_registry_url",
     reg(row("S939", "https://e.example/939")),
     {"ok.md": "Cites S940 (https://e.example/940).\n"},
     sibling=reg(row("S940", "https://e.example/940")))


def main() -> int:
    os.makedirs(WORK, exist_ok=True)
    results = []
    for spec in CASES:
        fleet, lane = build(spec["name"], spec["registry"], spec["knowledge"], spec.get("sibling"),
                            crlf_registry=spec.get("crlf_registry", False),
                            crlf_knowledge=spec.get("crlf_knowledge", False))
        res = run_resolver(lane, fleet)
        cen = run_census(lane)
        results.append({"case": spec["name"], "resolver": res, "census": cen})
        print("=" * 78)
        print("CASE", spec["name"])
        print("  resolver exit:", res["exit"])
        for line in res["out"].splitlines():
            print("   |", line)
        print("  census rows:", cen["census_rows"], "census exit:", cen["census_exit"],
              "validate exit:", cen["validate_exit"])
        for f in cen["validate_findings"]:
            print("   !", f)
    out = os.path.join(SEAT, "results.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print("\nwrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
