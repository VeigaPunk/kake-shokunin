#!/usr/bin/env python3
"""Mutation harness for kake round-59 seat MutResolverSelftest.

Each mutant = one textual edit of a COPY of scripts/id_resolver.py in scratch.
Detector = the copy's own `--selftest` (59 checks). Killed = the selftest fails.
The lane file is never touched.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py"
SCRATCH = "/fast/scratch/hyaku/kake-r59/MutResolverSelftest"
WORK = os.path.join(SCRATCH, "work")

MUTANTS = [
    # id, area, description, old, new
    ("M01", "parse_registry", "registry row may carry 4 leading spaces (code row accepted)",
     'ROW_RE = re.compile(r"^ {0,3}\\|\\s*([^|]*?)\\s*(?:\\|(.*))?$")',
     'ROW_RE = re.compile(r"^ {0,4}\\|\\s*([^|]*?)\\s*(?:\\|(.*))?$")'),
    ("M02", "parse_registry", "registry id cell accepts 2 digits (S12 registers)",
     'ID_CELL_RE = re.compile(r"^S\\d{3,}$")',
     'ID_CELL_RE = re.compile(r"^S\\d{2,}$")'),
    ("M03", "parse_registry", "any level-1..6 heading ends the Registry section",
     'SECTION_END_RE = re.compile(r"^#{1,2}\\s")',
     'SECTION_END_RE = re.compile(r"^#{1,6}\\s")'),
    ("M04", "fence machine", "fence opener may be indented 4 spaces",
     'FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")',
     'FENCE_OPEN_RE = re.compile(r"^ {0,4}(`{3,}|~{3,})(.*)$")'),
    ("M05", "fence machine", "closing run must have exactly the opener length (longer run does not close)",
     "return bool(m) and m.group(1)[0] == char and len(m.group(1)) >= length",
     "return bool(m) and m.group(1)[0] == char and len(m.group(1)) == length"),
    ("M06", "fence machine", "closing run may use the other fence character",
     "return bool(m) and m.group(1)[0] == char and len(m.group(1)) >= length",
     "return bool(m) and len(m.group(1)) >= length"),
    ("M07", "fence machine", "backtick fence may carry a backtick in its info string",
     '    if run[0] == "`" and "`" in m.group(2):  # a backtick fence\'s info string may not hold a backtick\n        return None\n',
     ""),
    ("M08", "parse_registry", "registry URL keeps its trailing punctuation",
     'urls = [u.rstrip(".,;:") for u in URL_RE.findall(source_cell)]',
     'urls = list(URL_RE.findall(source_cell))'),
    ("M09", "parse_registry", "URLs are read from every cell of the row, not only the source cell",
     'source_cell = (m.group(2) or "").split("|", 1)[0]',
     'source_cell = (m.group(2) or "")'),
    ("M10", "knowledge walk", "symlinked knowledge file outside the lane is read",
     "            if not inside(full):\n                continue\n",
     ""),
    ("M11", "knowledge walk", ".markdown knowledge files are walked",
     '            if not name.endswith(".md"):\n                continue\n',
     '            if not (name.endswith(".md") or name.endswith(".markdown")):\n                continue\n'),
    ("M12", "knowledge walk", "cited path is relative to the knowledge dir, not the lane root",
     'rel = os.path.relpath(full, root).replace(os.sep, "/")',
     'rel = os.path.relpath(full, base).replace(os.sep, "/")'),
    ("M13", "knowledge walk", "knowledge dir symlinked out of the lane is accepted",
     "    if not os.path.isdir(base) or not inside(base):",
     "    if not os.path.isdir(base):"),
    ("M14", "revision path parse", "NUL-split revision paths are decoded with surrogateescape",
     'return [chunk.decode("utf-8", "replace") for chunk in data.split(b"\\0") if chunk]',
     'return [chunk.decode("utf-8", "surrogateescape") for chunk in data.split(b"\\0") if chunk]'),
    ("M15", "revision path parse", "revision paths split on newline instead of NUL",
     'return [chunk.decode("utf-8", "replace") for chunk in data.split(b"\\0") if chunk]',
     'return [chunk.decode("utf-8", "replace") for chunk in data.split(b"\\n") if chunk]'),
    ("M16", "revision path parse", "ls-tree listing drops --name-only (raw tree format)",
     'proc = _git(root, "ls-tree", "-r", "-z", "--name-only", revision)',
     'proc = _git(root, "ls-tree", "-r", "-z", revision)'),
    ("M17", "revision path parse", "revision resolves to a tree, not a commit",
     'proc = _git(root, "rev-parse", "--verify", f"{revision}^{{commit}}")',
     'proc = _git(root, "rev-parse", "--verify", f"{revision}^{{tree}}")'),
    ("M18", "revision path parse", "inherited GIT_* environment is passed to git",
     '    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}',
     '    env = dict(os.environ)'),
    ("M19", "sibling registry", "sibling repo without a committed registry falls back to its worktree file",
     "        return parse_registry(_text(proc)) if proc.returncode == 0 else {}",
     "        if proc.returncode == 0:\n            return parse_registry(_text(proc))\n        file_path = os.path.join(path, REGISTRY_REL)\n        if os.path.isfile(file_path):\n            with open(file_path, \"rb\") as handle:\n                return parse_registry(handle.read().decode(\"utf-8\", \"replace\"))\n        return {}"),
    ("M20", "sibling registry", "lane excluded from siblings by path string, not by realpath",
     "        if os.path.realpath(path) == lane_real:\n            continue",
     "        if path == root:\n            continue"),
    ("M21", "sibling registry", "sibling directory need not carry the -shokunin suffix",
     '        if not name.endswith("-shokunin"):\n            continue',
     '        if not name.endswith("shokunin"):\n            continue'),
    ("M22", "evaluate", "default fleet root is the grandparent of --root",
     "    fleet_root = os.path.abspath(fleet) if fleet else os.path.dirname(root)",
     "    fleet_root = os.path.abspath(fleet) if fleet else os.path.dirname(os.path.dirname(root))"),
    ("M23", "evaluate", "a missing fleet directory is not unevaluable",
     "    if not os.path.isdir(fleet_root):\n        return _err(f\"fleet root {fleet_root} is not a directory\")",
     ""),
    ("M24", "evaluate", "owned_elsewhere counts url-match owners, not registry owners",
     "    owned = sum(1 for row in rows if row[2])",
     "    owned = sum(1 for row in rows if row[3])"),
    ("M25", "evaluate", "url-match looks only at the first citing file",
     "            if any(url in bodies[path] for path in paths for url in urls):",
     "            if any(url in bodies[paths[0]] for url in urls):"),
    ("M26", "render", "empty owners print as an empty field instead of '-'",
     'f"owners={\',\'.join(owners) or \'-\'} url-match={\',\'.join(matched) or \'-\'}"',
     'f"owners={\',\'.join(owners)} url-match={\',\'.join(matched)}"'),
    ("M27", "render", "summary line field order swapped (ids_resolved before ids_cited)",
     'f"ids_cited={cited_n} ids_resolved={resolved} dangling={dangling} "',
     'f"ids_resolved={resolved} ids_cited={cited_n} dangling={dangling} "'),
    ("M28", "evaluate", "dangling ids are not sorted (set order kept)",
     "    dangling_ids = sorted(set(cited) - set(registry))",
     "    dangling_ids = list(set(cited) - set(registry))"),
    ("M29", "parse_registry", "registry row requires a leading pipe (indented rows dropped)",
     'ROW_RE = re.compile(r"^ {0,3}\\|\\s*([^|]*?)\\s*(?:\\|(.*))?$")',
     'ROW_RE = re.compile(r"^ {0,3}\\|\\s*([^|]*?)\\s*(?:\\|(.*))?$")\nROW_RE = re.compile(r"^\\|\\s*([^|]*?)\\s*(?:\\|(.*))?$")'),
    ("M30", "evaluate", "revision mode ignores the working tree entirely (registry read from HEAD)",
     '    registry_text, err = lane_registry(root, rev)',
     '    registry_text, err = lane_registry(root, None if rev else rev)'),
    ("M31", "knowledge walk", "revision mode accepts an empty knowledge set",
     '        if not bodies:\n            return None, f"no knowledge file at {revision[:12]}"\n',
     ""),
    ("M32", "parse_cited", "cited id needs no left word boundary",
     'ID_RE = re.compile(r"(?<![A-Za-z0-9_])S\\d{3,}(?![A-Za-z0-9_])")',
     'ID_RE = re.compile(r"S\\d{3,}(?![A-Za-z0-9_])")'),
    ("M33", "revision path parse", "revision knowledge prefix matched without the path separator",
     '        rels = [rel for rel in _nul_paths(proc.stdout)\n                if rel.startswith(KNOWLEDGE_REL + "/") and rel.endswith(".md")]',
     '        rels = [rel for rel in _nul_paths(proc.stdout)\n                if rel.startswith(KNOWLEDGE_REL) and rel.endswith(".md")]'),
    ("M34", "sibling registry", "a linked git worktree (.git as a file) is read from its worktree file",
     '    if os.path.exists(os.path.join(path, ".git")):',
     '    if os.path.isdir(os.path.join(path, ".git")):'),
    ("M35", "fence machine", "closing run may not carry trailing whitespace",
     'FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \\t]*$")',
     'FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})$")'),
    ("M36", "evaluate", "ids_resolved counts the registry size, not the resolved citations",
     "    summary = (cited_n, cited_n - len(dangling_ids), len(dangling_ids), owned, len(rows) - owned)",
     "    summary = (cited_n, len(registry), len(dangling_ids), owned, len(rows) - owned)"),
    ("M37", "render", "unowned count printed as the dangling count",
     'f"owned_elsewhere={owned} unowned={unowned}"',
     'f"owned_elsewhere={owned} unowned={dangling}"'),
    ("M38", "parse_registry", "a registry row with 4 leading spaces is a code row (indented rows ignored)",
     'ROW_RE = re.compile(r"^ {0,3}\\|\\s*([^|]*?)\\s*(?:\\|(.*))?$")',
     'ROW_RE = re.compile(r"^ {0,2}\\|\\s*([^|]*?)\\s*(?:\\|(.*))?$")'),
    ("M39", "knowledge walk", "the knowledge walk follows symlinked directories",
     "    for dirpath, dirnames, filenames in os.walk(base):",
     "    for dirpath, dirnames, filenames in os.walk(base, followlinks=True):"),
    ("M40", "knowledge walk", "compound: the walk follows symlinked directories and the per-file lane guard is dropped",
     [("    for dirpath, dirnames, filenames in os.walk(base):",
       "    for dirpath, dirnames, filenames in os.walk(base, followlinks=True):"),
      ("            if not inside(full):\n                continue\n", "")],
     None),
]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run_selftest(path):
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(WORK, "tmp")
    env["LC_ALL"] = "C.UTF-8"
    os.makedirs(env["TMPDIR"], exist_ok=True)
    p = subprocess.run([sys.executable, "-B", path, "--selftest"], capture_output=True,
                       env=env, cwd=WORK, timeout=600)
    out = p.stdout.decode("utf-8", "replace")
    m = re.findall(r"(?m)^selftest: (\d+)/(\d+)\s*$", out)
    fails = re.findall(r"(?m)^FAIL .*$", out)
    crash = "Traceback" in p.stderr.decode("utf-8", "replace")
    return {
        "rc": p.returncode,
        "tally": m[-1] if m else None,
        "fails": fails,
        "crash": crash,
        "stderr": p.stderr.decode("utf-8", "replace")[-300:],
    }


def main():
    os.makedirs(WORK, exist_ok=True)
    shutil.rmtree(os.path.join(WORK, "tmp"), ignore_errors=True)
    with open(SRC, "rb") as fh:
        base_bytes = fh.read()
    base_text = base_bytes.decode("utf-8")
    base_sha = hashlib.sha256(base_bytes).hexdigest()

    results = {"baseline": {}, "mutants": []}

    # detector sanity on pristine copy
    pristine = os.path.join(WORK, "pristine.py")
    with open(pristine, "w", encoding="utf-8", newline="") as fh:
        fh.write(base_text)
    results["baseline"] = {"path": pristine, "sha256": sha(pristine), **run_selftest(pristine)}
    print("BASELINE", results["baseline"]["rc"], results["baseline"]["tally"])

    for mid, area, desc, old, new in MUTANTS:
        if isinstance(old, list):
            edits = old
        else:
            edits = [(old, new)]
        bad = [o for o, _ in edits if base_text.count(o) != 1]
        if bad:
            results["mutants"].append({"id": mid, "area": area, "desc": desc,
                                       "error": f"anchor count {base_text.count(bad[0])}"})
            print(mid, "ANCHOR-ERROR", base_text.count(bad[0]))
            continue
        mutated = base_text
        for o, n in edits:
            mutated = mutated.replace(o, n, 1)
        path = os.path.join(WORK, f"{mid}.py")
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(mutated)
        r = run_selftest(path)
        killed = r["rc"] != 0
        results["mutants"].append({
            "id": mid, "area": area, "desc": desc, "sha256": sha(path),
            "rc": r["rc"], "tally": r["tally"], "killed": killed, "crash": r["crash"],
            "fails": r["fails"][:4], "stderr": r["stderr"],
        })
        print(mid, area, "KILLED" if killed else "SURVIVED", r["tally"],
              (r["fails"][:2] if killed else ""))

    # restore check: the lane source is untouched
    results["lane_sha256_after"] = sha(SRC)
    results["lane_unchanged"] = results["lane_sha256_after"] == base_sha
    with open(os.path.join(SCRATCH, "mutants.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print("LANE_UNCHANGED", results["lane_unchanged"], results["lane_sha256_after"])


if __name__ == "__main__":
    main()
