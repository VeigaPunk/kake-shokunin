#!/usr/bin/env python3
"""Round-59 w1 seat ExecResolverOtherRoutes — probe batch 9 (rigorous bytes).

All special characters are built with chr() so the exact code point is
guaranteed; every fixture prints its hex, so the evidence is checkable.

  G1  U+200B inside a cited id (zero-width space) -> is the citation seen?
  G2  U+200B inside a registry id cell -> does the row register?
  G3  Cyrillic U+0405 in place of ASCII S, in a citation and in an id cell.
  G4  HTML blocks beyond <pre>: <script>, <style>, <textarea>, <details>,
      <div>, <blockquote> -> does the row register? (narrow comment-only fix vs
      a full HTML-block fix, to show what a K8-shaped narrow fix leaves open)
  G5  the heading-indent divergence at --revision (git blobs).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

SEAT = "/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes"
WORK = os.path.join(SEAT, "work9")
TOOL = os.path.join(SEAT, "tool", "id_resolver.py")
NARROW = os.path.join(SEAT, "variants", "narrow_html.py")
FULL = os.path.join(SEAT, "variants", "full_html.py")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"

ZWSP = chr(0x200B)
CYR = chr(0x0405)
FW = chr(0xFF19)

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


def build(case, registry, knowledge, sibling=None):
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


def commit(path):
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


def run_tool(tool, lane, fleet, revision=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C.UTF-8"
    argv = [sys.executable, "-B", tool, "--root", lane, "--fleet", fleet]
    if revision:
        argv += ["--revision", revision]
    p = subprocess.run(argv, capture_output=True, env=env, timeout=300)
    return {"exit": p.returncode, "out": (p.stdout + p.stderr).decode("utf-8", "replace").strip()}


def run_census(lane):
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
    return {"rows": rows, "validate_exit": v.returncode, "findings": findings}


def show(name, note, kb_hex, cen, res):
    print("=" * 78)
    print("CASE", name, "|", note)
    print("  fixture hex:", kb_hex)
    print("  census rows:", cen["rows"], "validate exit:", cen["validate_exit"])
    for f in cen["findings"]:
        print("   !", f)
    print("  resolver exit:", res["exit"])
    for line in res["out"].splitlines():
        print("   |", line)


def main() -> int:
    os.makedirs(WORK, exist_ok=True)
    results = []

    # G1: zero-width space inside a cited id
    kb = f"Cites S{ZWSP}972 which is registered nowhere.\n".encode("utf-8")
    fleet, lane = build("G1_zwsp_cited_id", reg(row("S971", "https://e.example/971")),
                         {"ok.md": kb.decode("utf-8")})
    cen, res = run_census(lane), run_tool(TOOL, lane, fleet)
    show("G1_zwsp_cited_id", "U+200B between S and the digits of a cited id", kb.hex(), cen, res)
    results.append({"case": "G1", "hex": kb.hex(), "census": cen, "resolver": res})

    # G2: zero-width space inside a registry id cell
    kb = b"Cites S973.\n"
    fleet, lane = build("G2_zwsp_registry_id", reg(row(f"S{ZWSP}973", "https://e.example/973")),
                         {"ok.md": kb.decode("utf-8")})
    cen, res = run_census(lane), run_tool(TOOL, lane, fleet)
    show("G2_zwsp_registry_id", "U+200B inside the registry id cell", kb.hex(), cen, res)
    results.append({"case": "G2", "hex": kb.hex(), "census": cen, "resolver": res})

    # G3: Cyrillic lookalike S, in a citation and in an id cell
    kb = f"Cites {CYR}974 which is registered nowhere.\n".encode("utf-8")
    fleet, lane = build("G3a_cyrillic_cited", reg(row("S974", "https://e.example/974")),
                         {"ok.md": kb.decode("utf-8")})
    cen, res = run_census(lane), run_tool(TOOL, lane, fleet)
    show("G3a_cyrillic_cited", "Cyrillic U+0405 in place of ASCII S in a citation", kb.hex(), cen, res)
    results.append({"case": "G3a", "hex": kb.hex(), "census": cen, "resolver": res})

    kb = b"Cites S975.\n"
    fleet, lane = build("G3b_cyrillic_registry_id", reg(row(f"{CYR}975", "https://e.example/975")),
                         {"ok.md": kb.decode("utf-8")})
    cen, res = run_census(lane), run_tool(TOOL, lane, fleet)
    show("G3b_cyrillic_registry_id", "Cyrillic U+0405 in the registry id cell", kb.hex(), cen, res)
    results.append({"case": "G3b", "hex": kb.hex(), "census": cen, "resolver": res})

    # G4: HTML block tags, current vs narrow-comment fix vs full-HTML fix
    for tag, sid in (("script", "S976"), ("style", "S977"), ("textarea", "S978"),
                     ("details", "S979"), ("div", "S980"), ("blockquote", "S981")):
        body = reg(row("S975", "https://e.example/975") + f"<{tag}>\n" + row(sid, "https://e.example/" + sid) + f"</{tag}>\n")
        kb = f"Cites S975 and {sid}.\n".encode("utf-8")
        fleet, lane = build(f"G4_{tag}", body, {"ok.md": kb.decode("utf-8")})
        cen = run_census(lane)
        cur = run_tool(TOOL, lane, fleet)
        nar = run_tool(NARROW, lane, fleet)
        ful = run_tool(FULL, lane, fleet)
        print("=" * 78)
        print(f"CASE G4_html_{tag} | a row inside <{tag}> registers the id")
        print("  census rows:", cen["rows"], "validate exit:", cen["validate_exit"], cen["findings"])
        for label, r in (("current", cur), ("narrow_comment_fix", nar), ("full_html_fix", ful)):
            print(f"  {label:18s} exit={r['exit']} :: {r['out'].splitlines()[0] if r['out'] else ''}")
        results.append({"case": f"G4_{tag}", "census": cen, "current": cur, "narrow": nar, "full": ful})

    # G5: heading-indent divergence at a revision
    kb = b"Cites S982 and S983.\n"
    body = ("# Sources\n\n## Registry\n\n" + HDR + row("S982", "https://e.example/982") +
            "  ## Paths\n\n" + row("S983", "https://e.example/983"))
    fleet, lane = build("G5_indented_heading_revision", body, {"ok.md": kb.decode("utf-8")})
    head = commit(lane)
    cen = run_census(lane)
    rv = run_tool(TOOL, lane, fleet, head)
    show("G5_indented_heading_revision",
         "rows after an indented `## Paths` at a revision: census says outside, resolver registers",
         kb.hex(), cen, rv)
    results.append({"case": "G5", "census": cen, "revision": rv})

    with open(os.path.join(SEAT, "results9.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
