#!/usr/bin/env python3
"""Round-57 C2 counter — operability (capability acquisition): the cross-registry source-id resolver.

Version 1 was frozen at `b9a5d012f7fd` (an optional `--fleet` argument was added before dispatch). Version 2 (after wave 1, before any
claim was measured; attacks `w1/CriticC2Gate.md`, `w1/CritCheatC2.md`, `w1/CriticControlsSizing.md`, `w1/ReviewerGateCode.md`) makes the
gate a differential test: it carries its own reference implementation of the documented rule and compares the tool's output with
the reference over randomised fixtures and over the real revisions, instead of comparing with constants a stub can print. The
predicate and the five condition names are unchanged.

The capability (considerthese proposal 2, `considerthese/2026-10-25.md`): `scripts/id_resolver.py` lists every `S###` id cited in
`corpus/knowledge/**/*.md` that does not resolve in the lane's own `corpus/SOURCES.md`, and names which sibling registry holds it. Round 52
left five such ids (S367 S372 S373 S390 S409) that resolved only in kotodama-shokunin's registry; the round-53 verifier found them,
not the lane.

CLI contract the gate exercises (the tool may add options; these are fixed):

    python3 -B scripts/id_resolver.py --root <lane dir> [--revision <rev>] [--fleet <fleet root>] [--selftest]

  - cited ids: every token `S` + 3 or more digits NOT preceded or followed by an ASCII letter, digit or underscore (a CJK or
    fullwidth neighbour is a boundary) in each `corpus/knowledge/**/*.md` file; with `--revision` the files and the lane registry are
    read through `git show` at that revision, never the working tree. Registry ids: first cell of each table row of `corpus/SOURCES.md`
    under `## Registry` (up to the next `## ` heading), 0 to 3 leading spaces before the pipe (4 spaces is code and ignored); CRLF is
    tolerated. Ranges (`S011–S013`) cite only their two literal ids.
  - siblings: every `<fleet>/*-shokunin/` directory whose realpath differs from the lane's, read through `git show HEAD:corpus/SOURCES.md`
    when the directory has a `.git`, else the file; a sibling without a registry owns nothing; a sibling owns an id when a registry row has it.
  - stdout: one line per dangling id, sorted by id, `DANGLING <id> cited-by=<comma-joined repo-relative paths, / separators> owners=<comma-joined
    lane names or -> url-match=<comma-joined lane names or ->`, then a last line `ids_cited=<n> ids_resolved=<n> dangling=<n> owned_elsewhere=<n>
    unowned=<n>`. Lists are sorted; `-` is the empty set. `url-match` names the sibling lanes whose registry row for that id carries an
    http(s) URL that occurs verbatim in a citing file (compared by the gate on synthetic fixtures only).
  - exit: 0 when dangling == 0; 1 when dangling > 0; 2 unevaluable (revision unresolved, registry absent, no knowledge file); 64 usage.
    `--selftest` prints a last line `selftest: <passed>/<total>` (the only `selftest:` line) and exits 0 iff all passed.

Conditions (frozen in `contract.json`):

  G1 `scripts/id_resolver.py` exists at the measured revision.
  G2 its `--selftest`, run in a clean clone of the revision, exits 0 with one `selftest: N/N` line, N >= 16 (a smoke test, not evidence).
  G3 two gate-built randomised fixtures (fresh nonce, ids, lane and sibling names, indentation 0/2/3/4 spaces, a CRLF registry, a sibling
     without a registry, CJK-adjacent ids, ranges, decoys, a duplicate citation across files): the tool's lines, summary and exit equal the
     gate's reference output, each fixture class (one-sibling, two-sibling, unowned, resolved) is present, and the same fixtures with
     the dangling citations removed exit 0 with the reference summary.
  G4 red-before: over the lane revision `3994101` with the real fleet, the reference finds exactly the five ids S367 S372 S373 S390 S409
     owned by kotodama-shokunin (and the live ownership equals `sibling-snapshot.json`, else the gate is unevaluable); the tool's ids,
     cited-by paths, owners and summary equal the reference's and it exits 1.
  G5 green: over the measured revision itself, the reference reports dangling == 0 and ids_cited >= 100; the tool's lines and summary equal
     the reference's and it exits 0.

Predicate (frozen in `contract.json`):

    met: gate_conditions_passed == 5 of 5

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable, 64 usage.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

PREDICATE = "met: gate_conditions_passed == 5 of 5"
RED_REV = "3994101dba28896830604fd0b08c7f00faca8ed6"
RED_IDS = ["S367", "S372", "S373", "S390", "S409"]
RED_OWNER = "kotodama-shokunin"
TOOL = "scripts/id_resolver.py"
SNAPSHOT = ".ufo/waves/round-57/sibling-snapshot.json"
MIN_SELFTEST = 16
MIN_CITED = 100
ID_RE = re.compile(r"(?<![A-Za-z0-9_])S\d{3,}(?![A-Za-z0-9_])")
URL_RE = re.compile(r"https?://[^\s|<>\"'`]+")
SUMMARY = re.compile(r"^ids_cited=(\d+) ids_resolved=(\d+) dangling=(\d+) owned_elsewhere=(\d+) unowned=(\d+)$")
DANGLE = re.compile(r"^DANGLING (S\d{3,}) cited-by=(\S+) owners=(\S+) url-match=(\S+)$")


class Unevaluable(Exception):
    pass


def git(*args: str, cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def sandbox_clone(root: str, rev: str) -> str:
    d = tempfile.mkdtemp(prefix="c57-gate-")
    for cmd in (["clone", "-q", "--no-checkout", root, d], ["-C", d, "checkout", "-q", rev]):
        p = git(*cmd)
        if p.returncode != 0:
            shutil.rmtree(d, ignore_errors=True)
            raise Unevaluable(f"git {' '.join(cmd)}: {p.stderr.decode('utf-8', 'replace').strip()}")
    return d


def run_tool(clone: str, *args: str, timeout: int = 300) -> tuple[int, list[str], str]:
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/tmp"), "LC_ALL": "C.UTF-8", "PYTHONHASHSEED": "0"}
    p = subprocess.run([sys.executable, "-B", os.path.join(clone, TOOL), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       timeout=timeout, cwd=clone, env=env)
    out = p.stdout.decode("utf-8", "replace").replace("\r\n", "\n").strip()
    return p.returncode, (out.split("\n") if out else []), p.stderr.decode("utf-8", "replace")


def parse(lines: list[str]) -> tuple[dict[str, tuple[frozenset, frozenset, frozenset]], tuple[int, ...] | None, str]:
    """Strict: every line but the last is a DANGLING line (no duplicate id); the last is the one SUMMARY line; identities hold."""
    if not lines:
        return {}, None, "no output"
    dang: dict = {}
    for ln in lines[:-1]:
        m = DANGLE.match(ln)
        if not m:
            return {}, None, f"unexpected line before the summary: {ln[:80]!r}"
        if m.group(1) in dang:
            return {}, None, f"duplicate DANGLING id {m.group(1)}"
        dang[m.group(1)] = tuple(frozenset(() if v == "-" else v.split(",")) for v in m.groups()[1:])
    m = SUMMARY.match(lines[-1])
    if not m:
        return {}, None, f"last line is not the summary: {lines[-1][:80]!r}"
    summ = tuple(int(x) for x in m.groups())
    if summ[0] != summ[1] + summ[2] or summ[2] != len(dang) or summ[3] + summ[4] != summ[2]:
        return {}, None, f"summary identities fail: {summ} with {len(dang)} DANGLING lines"
    return dang, summ, ""


# ------------------------------------------------------------------ reference implementation (the documented rule)
def registry_rows(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    inside = False
    for line in text.replace("\r\n", "\n").split("\n"):
        if line.startswith("## ") or line.startswith("# "):
            inside = line.lower().startswith("## registry")
            continue
        if inside and re.match(r"^ {0,3}\|", line):
            cell = line.strip().strip("|").split("|")[0].strip()
            if re.fullmatch(r"S\d{3,}", cell):
                rows.setdefault(cell, []).append(line)
    return rows


def read_lane(root: str, rev: str | None) -> tuple[dict[str, str], str]:
    files: dict[str, str] = {}
    if rev:
        p = git("-C", root, "ls-tree", "-r", "--name-only", rev, "corpus/knowledge")
        if p.returncode != 0:
            raise Unevaluable(f"revision {rev} unresolved in {root}")
        for path in p.stdout.decode().split("\n"):
            if path.endswith(".md"):
                b = git("-C", root, "show", f"{rev}:{path}")
                files[path] = b.stdout.decode("utf-8", "replace")
        r = git("-C", root, "show", f"{rev}:corpus/SOURCES.md")
        if r.returncode != 0:
            raise Unevaluable("lane registry absent")
        return files, r.stdout.decode("utf-8", "replace")
    base = os.path.join(root, "corpus", "knowledge")
    for d, _dirs, names in os.walk(base):
        for n in names:
            if n.endswith(".md"):
                full = os.path.join(d, n)
                files[os.path.relpath(full, root).replace(os.sep, "/")] = open(full, encoding="utf-8", errors="replace").read()
    reg = os.path.join(root, "corpus", "SOURCES.md")
    if not os.path.isfile(reg):
        raise Unevaluable("lane registry absent")
    return files, open(reg, encoding="utf-8", errors="replace").read()


def read_siblings(root: str, fleet: str) -> dict[str, str]:
    out: dict[str, str] = {}
    me = os.path.realpath(root)
    for name in sorted(os.listdir(fleet)):
        full = os.path.join(fleet, name)
        if not name.endswith("-shokunin") or not os.path.isdir(full) or os.path.realpath(full) == me:
            continue
        if os.path.exists(os.path.join(full, ".git")):
            p = git("-C", full, "show", "HEAD:corpus/SOURCES.md")
            if p.returncode == 0:
                out[name] = p.stdout.decode("utf-8", "replace")
        elif os.path.isfile(os.path.join(full, "corpus", "SOURCES.md")):
            out[name] = open(os.path.join(full, "corpus", "SOURCES.md"), encoding="utf-8", errors="replace").read()
    return out


def reference(root: str, rev: str | None, fleet: str) -> dict:
    files, reg_text = read_lane(root, rev)
    if not files:
        raise Unevaluable("no knowledge file")
    registry = set(registry_rows(reg_text))
    cited: dict[str, set[str]] = {}
    for path, text in files.items():
        for i in ID_RE.findall(text):
            cited.setdefault(i, set()).add(path)
    sib = {n: registry_rows(t) for n, t in read_siblings(root, fleet).items()}
    dang = sorted(i for i in cited if i not in registry)
    lines = {}
    for i in dang:
        owners = sorted(n for n, rows in sib.items() if i in rows)
        urls = sorted(n for n in owners if any(u in files[p] for p in cited[i] for row in sib[n][i] for u in URL_RE.findall(row)))
        lines[i] = (frozenset(cited[i]), frozenset(owners), frozenset(urls))
    owned = sum(1 for i in dang if lines[i][1])
    summ = (len(cited), len(cited) - len(dang), len(dang), owned, len(dang) - owned)
    return {"dang": lines, "summary": summ, "cited": cited}


def compare(tool_lines, tool_summ, ref: dict, with_urls: bool) -> str:
    """'' when the tool's DANGLING lines and summary equal the reference's (url-match only when with_urls)."""
    if tool_summ != ref["summary"]:
        return f"summary {tool_summ} != reference {ref['summary']}"
    if sorted(tool_lines) != sorted(ref["dang"]):
        return f"dangling ids {sorted(tool_lines)} != reference {sorted(ref['dang'])}"
    for i, (cb, ow, um) in tool_lines.items():
        rcb, row, rum = ref["dang"][i]
        if cb != rcb or ow != row or (with_urls and um != rum):
            return f"{i}: cited-by/owners/url-match {sorted(cb)} {sorted(ow)} {sorted(um)} != reference {sorted(rcb)} {sorted(row)} {sorted(rum)}"
    return ""


# ------------------------------------------------------------------ randomised fixtures
def build_fixture(rng: random.Random, nonce: str, dangling: bool = True) -> tuple[str, str]:
    """Return (fleet root, lane dir). Classes: resolved, held by one sibling (+URL quoted), held by two, held by none."""
    fleet = tempfile.mkdtemp(prefix=f"c57-fixture-{nonce}-")
    pool = rng.sample(range(100, 999), 40)
    ids = [f"S{n}" for n in pool]
    lane_ids, a_only, ab_both, a_only_noquote, unowned, indented4, b_only = ids[0:3], ids[3:5], ids[5:6], ids[6:7], ids[7:8], ids[8:9], ids[9:10]
    wide = f"S0{rng.randint(100, 999)}"
    lane = os.path.join(fleet, f"demo{nonce}-shokunin")
    sa, sb, sc = (f"{nonce}a-shokunin", f"{nonce}b-shokunin", f"{nonce}c-shokunin")

    def reg(path: str, rows: list[tuple[str, str]], indents: list[int], crlf: bool = False) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        body = "# SOURCES\n## Registry\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
        for k, (sid, url) in enumerate(rows):
            body += f"{' ' * indents[k % len(indents)]}| {sid} | t — {url} | docs | A | s | a | x | mined | 2026-10-25 | 90d | — |\n"
        body += "\n## Paths\n| S999 | not a registry row |\n"
        if crlf:
            body = body.replace("\n", "\r\n")
        with open(path, "w", newline="") as f:
            f.write(body)

    reg(os.path.join(lane, "corpus/SOURCES.md"), [(i, f"https://lane.example/{i}") for i in lane_ids], [0, 2, 3])
    reg(os.path.join(fleet, sa, "corpus/SOURCES.md"),
        [(i, f"https://a.example/{i}") for i in a_only + ab_both + a_only_noquote + [wide]] + [(i, "https://a.example/x") for i in indented4], [0, 2], crlf=True)
    reg(os.path.join(fleet, sb, "corpus/SOURCES.md"), [(i, f"https://b.example/{i}") for i in ab_both + b_only], [3])
    # 4-space rows are code: rewrite the indented4 rows of sibling a with four leading spaces
    pa = os.path.join(fleet, sa, "corpus/SOURCES.md")
    txt = open(pa, newline="").read()
    for i in indented4:
        txt = re.sub(rf"(?m)^( *)\| {i} \|", f"    | {i} |", txt)
    open(pa, "w", newline="").write(txt)
    os.makedirs(os.path.join(fleet, sc), exist_ok=True)  # a sibling without a registry
    kn = os.path.join(lane, "corpus/knowledge")
    os.makedirs(os.path.join(kn, "sub/deep"), exist_ok=True)
    good = (f"source: {lane_ids[0]} — https://lane.example/{lane_ids[0]}\n\nCites {lane_ids[0]}, {lane_ids[1]} and (again) {lane_ids[1]}; range {lane_ids[1]}–{lane_ids[2]}.\n")
    open(os.path.join(kn, "good.md"), "w").write(good)
    bad = ""
    if dangling:
        bad = (f"Held by one sibling: {a_only[0]}, quoted at https://a.example/{a_only[0]}.\nAlso {a_only[1]} (no quote) and 是{a_only[1]}的.\n"
               f"Two siblings: {ab_both[0]}. One sibling, URL not quoted: {a_only_noquote[0]}.\nHeld by none: {unowned[0]}. Wide id {wide} sits in sibling a.\n"
               f"Four-space row only: {indented4[0]}. Row only in b: {b_only[0]}. Section-outside id: S999.\n"
               "Decoys that are not ids: S12, AS500, S500x, s101, S_777, 1S888.\n")
        open(os.path.join(kn, "sub/bad.md"), "w").write(bad)
        open(os.path.join(kn, "sub/deep/more.md"), "w").write(f"Duplicate across files: {unowned[0]} and {lane_ids[2]}.\n")
        open(os.path.join(kn, "sub/ignored.json"), "w").write('{"cites": "S888 S889"}\n')
    return fleet, lane


def tool_vs_reference(clone: str, lane: str, fleet: str, rev: str | None, with_urls: bool) -> tuple[bool, str, dict]:
    args = ["--root", lane, "--fleet", fleet] + (["--revision", rev] if rev else [])
    ref = reference(lane, rev, fleet)
    rc, lines, err = run_tool(clone, *args)
    dang, summ, why = parse(lines)
    if why:
        return False, f"tool output rejected: {why} (exit {rc})", ref
    diff = compare(dang, summ, ref, with_urls)
    want_rc = 1 if ref["summary"][2] else 0
    if diff:
        return False, diff, ref
    if rc != want_rc:
        return False, f"exit {rc}, expected {want_rc}", ref
    return True, f"exit={rc} summary={summ}", ref


def evaluate(root: str, rev: str, fleet_real: str) -> tuple[int, list[tuple[str, bool, str]]]:
    results: list[tuple[str, bool, str]] = []
    present = git("-C", root, "cat-file", "-e", f"{rev}:{TOOL}").returncode == 0
    results.append(("G1_tool_present", present, "" if present else f"{TOOL} absent at {rev[:12]}"))
    if not present:
        for name in ("G2_selftest", "G3_fixture", "G4_red_before", "G5_green"):
            results.append((name, False, "tool absent"))
        return 1, results
    tmp: list[str] = []
    try:
        clone = sandbox_clone(root, rev)
        tmp.append(clone)
        rc, out, err = run_tool(clone, "--selftest")
        sel = [ln for ln in out if ln.startswith("selftest:")]
        m = re.fullmatch(r"selftest: (\d+)/(\d+)", out[-1]) if out else None
        ok = bool(m) and len(sel) == 1 and rc == 0 and int(m.group(1)) == int(m.group(2)) >= MIN_SELFTEST and "Traceback" not in err
        results.append(("G2_selftest", ok, out[-1] if out else f"no output (exit {rc})"))

        ok3, notes = True, []
        for k in range(2):
            nonce = secrets.token_hex(3)
            rng = random.Random(secrets.randbits(64))
            fleet, lane = build_fixture(rng, nonce, dangling=True)
            clean_fleet, clean_lane = build_fixture(random.Random(secrets.randbits(64)), secrets.token_hex(3), dangling=False)
            tmp += [fleet, clean_fleet]
            good, note, ref = tool_vs_reference(clone, lane, fleet, None, True)
            classes_ok = (ref["summary"][3] >= 3 and ref["summary"][4] >= 2 and ref["summary"][1] >= 3
                          and any(len(v[1]) == 2 for v in ref["dang"].values()) and any(v[2] for v in ref["dang"].values()))
            good2, note2, ref2 = tool_vs_reference(clone, clean_lane, clean_fleet, None, True)
            good2 = good2 and ref2["summary"][2] == 0
            ok3 = ok3 and good and classes_ok and good2
            notes.append(f"fixture{k}: dirty {note}{'' if classes_ok else ' [fixture classes missing]'}; clean {note2}")
        results.append(("G3_fixture", ok3, "; ".join(notes)))

        # G4 red-before over the real fleet
        sib = read_siblings(root, fleet_real)
        sp = git("-C", root, "show", f"{rev}:{SNAPSHOT}")
        snap = json.loads(sp.stdout.decode()) if sp.returncode == 0 else None
        if not sib or snap is None:
            raise Unevaluable("no sibling registries under the fleet or no sibling snapshot")
        live = {i: sorted(n for n, t in sib.items() if i in registry_rows(t) and n != 'kake-shokunin') for i in RED_IDS}  # the lane's own registry is not a sibling's (a scratch-clone root sees it as one)
        if live != {i: sorted(v) for i, v in snap["owners"].items()}:
            raise Unevaluable(f"live sibling ownership {live} differs from the committed snapshot (sibling heads: " +
                              ", ".join(f"{n}={git('-C', os.path.join(fleet_real, n), 'rev-parse', '--short', 'HEAD').stdout.decode().strip()}" for n in sib) + ")")
        good4, note4, ref4 = tool_vs_reference(clone, root, fleet_real, RED_REV, False)
        red_ok = sorted(ref4["dang"]) == RED_IDS and all(RED_OWNER in v[1] for v in ref4["dang"].values()) and ref4["summary"][2] == 5
        results.append(("G4_red_before", good4 and red_ok, note4 + ("" if red_ok else f"; reference red set {sorted(ref4['dang'])}")))

        good5, note5, ref5 = tool_vs_reference(clone, root, fleet_real, rev, False)
        green_ok = ref5["summary"][2] == 0 and ref5["summary"][0] >= MIN_CITED
        results.append(("G5_green", good5 and green_ok, note5 + f"; reference ids_cited={ref5['summary'][0]}"))
    except (Unevaluable, subprocess.TimeoutExpired, OSError, ValueError) as exc:
        print(f"C2 id-resolver-gate unevaluable: {type(exc).__name__}: {exc}")
        return 2, results
    finally:
        for d in tmp:
            shutil.rmtree(d, ignore_errors=True)
    return (0 if all(r[1] for r in results) else 1), results


def main() -> int:
    ap = argparse.ArgumentParser(description="Round-57 C2 gate (cross-registry id resolver)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--fleet", help="fleet root holding the sibling lanes (default: the parent of --root)")
    try:
        args = ap.parse_args()
    except SystemExit as e:
        return 0 if e.code == 0 else 64
    if not args.revision:
        print("usage: --root <lane> --revision <rev>", file=sys.stderr)
        return 64
    root = os.path.abspath(args.root)
    p = git("-C", root, "rev-parse", "--verify", f"{args.revision}^{{commit}}")
    if p.returncode != 0:
        print(f"C2 id-resolver-gate unevaluable: revision {args.revision} unresolved")
        return 2
    rev = p.stdout.decode().strip()
    fleet = os.path.abspath(args.fleet) if args.fleet else os.path.dirname(root)
    code, results = evaluate(root, rev, fleet)
    if code == 2:
        return 2
    passed = sum(1 for r in results if r[1])
    print(f"C2 id-resolver {passed}/5 met={passed == 5}  ({PREDICATE})")
    for name, ok, note in results:
        print(f"  {name} {'PASS' if ok else 'FAIL'}" + (f"\n    - {note}" if note else ""))
    print(f"  revision: {rev}")
    return 0 if passed == 5 else 1


if __name__ == "__main__":
    sys.exit(main())
