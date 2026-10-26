#!/usr/bin/env python3
"""Round-57 W2 — differential fixture generator for C2 (cross-registry id resolver).

Builds randomised and targeted fixture fleets under a scratch directory, runs

    A = <lane>/scripts/id_resolver.py                       (shipped, revision 4b8c7305)
    B = <lane>/.ufo/waves/round-57/w1/ExecResolverAlt.files/alt_resolver.py   (wave-1 oracle)

with identical argv/env/cwd on each fixture and diffs stdout and exit code. Every fixture is a
JSON spec (written to the results file) built by `build_spec`, so any disagreement can be rebuilt
from its spec alone.

Usage:
    python3 -B gen_and_diff.py --workdir <tmpdir> [--count 44] [--only NAME[,NAME...]]
    python3 -B gen_and_diff.py --workdir <tmpdir> --gate-ref T07_four_digit_sort
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
TOOL_A = os.path.join(LANE, "scripts/id_resolver.py")
TOOL_B = os.path.join(LANE, ".ufo/waves/round-57/w1/ExecResolverAlt.files/alt_resolver.py")
GATE = os.path.join(LANE, ".ufo/waves/round-57/c57_idresolver_gate.py")

HEADER = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |"
SEP = "|---|---|---|---|---|---|---|---|---|---|---|"
ROW = "{ind}| {sid} | {src} | docs | A | s | a | x | mined | 2026-10-25 | 90d | — |"
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/tmp"),
       "LC_ALL": "C.UTF-8", "PYTHONHASHSEED": "0"}


# --------------------------------------------------------------------------- spec rendering
def render_registry(spec: dict | None) -> str:
    if spec is None:
        return None
    indents = spec.get("indent", [0])
    if isinstance(indents, int):
        indents = [indents]
    lines = ["# SOURCES", spec.get("heading", "## Registry"), HEADER, SEP]
    h1_before = spec.get("h1_before")
    omit = spec.get("omit_closing_pipe")
    for i, (sid, src) in enumerate(spec.get("rows", [])):
        if h1_before is not None and i == h1_before:
            lines.append("# Appendix")
        ind = indents[i % len(indents)]
        if omit is not None and i == omit:
            lines.append(f"{' ' * ind}| {sid}")
        else:
            lines.append(ROW.format(ind=" " * ind, sid=sid, src=src))
    lines.append("")
    lines.append(spec.get("next_heading", "## Paths"))
    for sid, src in spec.get("after_paths", []):
        lines.append(ROW.format(ind="", sid=sid, src=src))
    text = "\n".join(lines) + "\n"
    if spec.get("crlf"):
        text = text.replace("\n", "\r\n")
    return text


def write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def repo_init(path: str) -> None:
    os.makedirs(path, exist_ok=True)
    p = git("init", "-q", path)
    assert p.returncode == 0, p.stderr.decode()
    top = git("-C", path, "rev-parse", "--show-toplevel")
    assert top.returncode == 0, top.stderr.decode()
    assert os.path.realpath(top.stdout.decode().strip()) == os.path.realpath(path), (top.stdout, path)


def repo_commit(path: str, msg: str) -> str:
    a = git("-C", path, "add", "-A")
    assert a.returncode == 0, a.stderr.decode()
    c = git("-C", path, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
            "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", msg)
    assert c.returncode == 0, c.stderr.decode()
    return git("-C", path, "rev-parse", "HEAD").stdout.decode().strip()


def build_spec(spec: dict, base: str) -> tuple[str, str, dict]:
    """Materialise one fixture; return (lane, fleet, {"revision": <sha|None>})."""
    root = os.path.join(base, "fixtures", spec["name"])
    shutil.rmtree(root, ignore_errors=True)
    fleet = os.path.join(root, "fleet")
    os.makedirs(fleet)
    if spec.get("fleet_git"):
        write(os.path.join(fleet, "corpus/SOURCES.md"),
              render_registry({"rows": spec["fleet_registry"], "indent": 0}))
        repo_init(fleet)
        repo_commit(fleet, "fleet root")
    lane = os.path.join(fleet, spec["lane"]["name"])
    lane_spec = spec["lane"]
    rev_info: dict = {"revision": None}

    def clear_knowledge() -> None:
        base_dir = os.path.join(lane, "corpus/knowledge")
        if not os.path.isdir(base_dir):
            return
        for dirpath, _dirnames, filenames in os.walk(base_dir):
            for name in filenames:
                os.unlink(os.path.join(dirpath, name))

    def write_lane(content: dict, clear: bool = False) -> None:
        if clear:
            clear_knowledge()
        reg = render_registry(content.get("registry"))
        if reg is not None:
            write(os.path.join(lane, "corpus/SOURCES.md"), reg)
        elif os.path.isfile(os.path.join(lane, "corpus/SOURCES.md")):
            os.unlink(os.path.join(lane, "corpus/SOURCES.md"))
        for rel, text in content.get("knowledge", {}).items():
            write(os.path.join(lane, rel), text)

    if lane_spec.get("git") and lane_spec.get("old"):
        write_lane(lane_spec["old"])
        repo_init(lane)
        old_sha = repo_commit(lane, "old")
        write_lane(lane_spec, clear=True)
        repo_commit(lane, "new")
        rev_info["revision"] = old_sha
    elif lane_spec.get("git"):
        write_lane(lane_spec)
        repo_init(lane)
        repo_commit(lane, "only")
        rev_info["revision"] = git("-C", lane, "rev-parse", "HEAD").stdout.decode().strip()
    else:
        write_lane(lane_spec)

    for sib in spec.get("siblings", []):
        path = os.path.join(fleet, sib["name"])
        kind = sib["kind"]
        if kind == "noreg":
            os.makedirs(path)
            continue
        reg = render_registry(sib.get("registry"))
        if reg is None:
            if kind in ("repo", "repo_headless"):
                write(os.path.join(path, "README.md"), "placeholder\n")
                repo_init(path)
                repo_commit(path, "placeholder")
            else:
                os.makedirs(path, exist_ok=True)
            continue
        if kind == "plain":
            write(os.path.join(path, "corpus/SOURCES.md"), reg)
        elif kind == "repo_stale":
            write(os.path.join(path, "corpus/SOURCES.md"), reg)
            repo_init(path)
            repo_commit(path, "registry")
            write(os.path.join(path, "corpus/SOURCES.md"),
                  render_registry(sib["worktree_registry"]))
        elif kind == "repo":
            write(os.path.join(path, "corpus/SOURCES.md"), reg)
            repo_init(path)
            repo_commit(path, "registry")
        elif kind == "repo_headless":
            # git repo whose HEAD does not carry the registry; the file exists only in the worktree
            write(os.path.join(path, "README.md"), "placeholder\n")
            repo_init(path)
            repo_commit(path, "placeholder")
            write(os.path.join(path, "corpus/SOURCES.md"), reg)
        else:
            raise AssertionError(f"unknown sibling kind {kind}")

    if spec.get("alias"):
        os.symlink(lane, os.path.join(fleet, spec["alias"]))
    return lane, fleet, rev_info


# --------------------------------------------------------------------------- fixture catalogue
def rand_specs(count: int, seed: int = 57) -> list[dict]:
    specs: list[dict] = []
    rng = random.Random(seed)
    words = ["alpha", "beta", "gamma", "delta", "omega", "tsuba", "koto", "suzu"]
    for idx in range(count):
        ids3 = [f"S{n}" for n in rng.sample(range(100, 1000), 12)]
        ids4 = [f"S{n}" for n in rng.sample(range(1000, 1400), 3)]
        pool = ids3 + ids4
        rng.shuffle(pool)
        lane_ids = pool[: rng.randint(1, 3)]
        rest = pool[len(lane_ids):]
        owned1, both, unowned, quoted = rest[0:2], rest[2:3], rest[3:5], rest[5:6]
        nsib = rng.randint(1, 3)
        sib_names = [f"{rng.choice(words)}{idx}{k}-shokunin" for k in range(nsib)]
        sib_specs = []
        for k, name in enumerate(sib_names):
            rows = []
            if k == 0:
                rows += [(i, f"https://{name}/{i}") for i in owned1 + both + quoted]
            elif k == 1:
                rows += [(i, f"https://{name}/{i}") for i in both]
            rows += [(f"S{rng.randint(2000, 2999)}", "https://filler.example/x") for _ in range(rng.randint(0, 2))]
            sib_specs.append({
                "name": name,
                "kind": rng.choice(["plain", "repo", "plain", "noreg" if k else "repo"]),
                "registry": {
                    "rows": rows,
                    "indent": rng.choice([0, 2, 3, [0, 2], [3, 0]]),
                    "crlf": rng.random() < 0.25,
                } if rows else None,
            })
        # knowledge: each mention gets a random decoration
        files: dict[str, list[str]] = {"corpus/knowledge/a.md": [], "corpus/knowledge/sub/b.md": [],
                                       "corpus/knowledge/sub/deep/c.md": []}
        order = ["a.md", "sub/b.md"]
        mentions = lane_ids + owned1 + both + unowned + quoted
        for n, sid in enumerate(mentions):
            target = files[f"corpus/knowledge/{order[n % 2]}"]
            style = rng.choice(["plain", "cjk", "url", "fence", "table", "plain", "dup"])
            if style == "plain":
                target.append(f"Cites {sid}.")
            elif style == "cjk":
                target.append(f"来源是{sid}的条目。")
            elif style == "url":
                target.append(f"见 https://example.test/{sid}/page 。")
            elif style == "fence":
                target.append("```\n" + sid + "\n```")
            elif style == "table":
                target.append(f"| {sid} | note |")
            else:
                target.append(f"Also {sid}.")
                files["corpus/knowledge/sub/deep/c.md"].append(f"Mentions {sid} again.")
        if rng.random() < 0.6:
            a, b = ids3[0], ids3[1]
            files["corpus/knowledge/a.md"].append(f"Spans {a}\u2013{b} only.")
            mentions += [a, b]
        if rng.random() < 0.4:
            files["corpus/knowledge/a.md"].append("Decoys: S12, AS500, S500x, s101, S_777, 1S888.")
        lane = {
            "name": f"lane{idx}-shokunin",
            "registry": {
                "rows": [(i, f"https://lane.example/{i}") for i in lane_ids],
                "indent": rng.choice([0, 2, 3, [0, 2, 3]]),
                "crlf": rng.random() < 0.2,
                "heading": "## Registry" if rng.random() < 0.85 else f"## Registry ({len(lane_ids)} rows)",
                "after_paths": [("S999", "not a registry row")],
                "h1_before": 1 if (rng.random() < 0.1 and len(lane_ids) > 1) else None,
            },
            "knowledge": {rel: "\n".join(lines) + "\n" for rel, lines in files.items() if lines},
            "git": rng.random() < 0.2,
        }
        if lane["git"]:
            lane["old"] = {
                "registry": {"rows": lane["registry"]["rows"][:-1],
                             "indent": lane["registry"]["indent"],
                             "crlf": lane["registry"]["crlf"],
                             "heading": lane["registry"]["heading"],
                             "after_paths": lane["registry"]["after_paths"]},
                "knowledge": lane["knowledge"],
            }
        specs.append({"name": f"R{idx:02d}", "lane": lane, "siblings": sib_specs,
                      "fleet_arg": rng.random() < 0.85, "alias": None})
    return specs


def sib(name: str, rows: list[tuple[str, str]], kind: str = "plain", indent=0, crlf=False) -> dict:
    return {"name": name, "kind": kind,
            "registry": {"rows": rows, "indent": indent, "crlf": crlf} if rows is not None else None}


def kn(n: int, text: str, rel: str = "corpus/knowledge/a.md") -> dict:
    return {rel: text}


def lane_of(rows, knowledge, indent=0, crlf=False, heading="## Registry", after=None, h1=None,
            omit=None, name="lane-shokunin", extra=None, old=None) -> dict:
    reg = {"rows": rows, "indent": indent, "crlf": crlf, "heading": heading,
           "after_paths": after if after is not None else [("S999", "not a registry row")],
           "h1_before": h1, "omit_closing_pipe": omit}
    lane = {"name": name, "registry": reg, "knowledge": knowledge}
    if extra:
        lane.update(extra)
    if old:
        lane["old"] = old
    return lane


def targeted_specs() -> list[dict]:
    L = "https://lane.example"
    out: list[dict] = []

    def add(name, lane, siblings=(), fleet_arg=True, alias=None):
        out.append({"name": name, "lane": lane, "siblings": list(siblings),
                    "fleet_arg": fleet_arg, "alias": alias})

    add("T01_indent0", lane_of([("S101", f"{L}/101")], kn(1, "Cites S101 and S501.\n")))
    add("T02_indent2", lane_of([("S101", f"{L}/101")], kn(1, "Cites S101 and S501.\n"), indent=2))
    add("T03_indent3", lane_of([("S101", f"{L}/101")], kn(1, "Cites S101 and S501.\n"), indent=3))
    add("T04_indent4_is_code", lane_of([("S101", f"{L}/101")], kn(1, "Cites S101.\n"), indent=4))
    add("T05_crlf_lane_registry", lane_of([("S101", f"{L}/101")], kn(1, "Cites S101.\n"), crlf=True))
    add("T06_crlf_sibling_registry",
        lane_of([("S101", f"{L}/101")], kn(1, "Cites S501.\n")),
        [sib("alpha-shokunin", [("S501", "https://a.example/501")], crlf=True)])
    add("T07_four_digit_sort",
        lane_of([("S101", f"{L}/101")], kn(1, "Cites S501 and S1000.\n")),
        [sib("alpha-shokunin", [("S1000", "https://a.example/1000"), ("S501", "https://a.example/501")])])
    add("T08_range_endpoints",
        lane_of([("S011", f"{L}/11"), ("S012", f"{L}/12"), ("S013", f"{L}/13")],
                kn(1, "Spans S011\u2013S013 only.\n")))
    add("T09_cjk_adjacent", lane_of([("S101", f"{L}/101")], kn(1, "来源是S501的条目。\n")))
    add("T10_id_inside_url", lane_of([("S101", f"{L}/101")], kn(1, "见 https://example.test/S501/page 。\n")))
    add("T11_id_in_code_fence", lane_of([("S101", f"{L}/101")], kn(1, "```\nS501\n```\n")))
    add("T12_sibling_git_repo", lane_of([("S101", f"{L}/101")], kn(1, "Cites S501.\n")),
        [sib("alpha-shokunin", [("S501", "https://a.example/501")], kind="repo")])
    add("T13_sibling_plain_dir", lane_of([("S101", f"{L}/101")], kn(1, "Cites S501.\n")),
        [sib("alpha-shokunin", [("S501", "https://a.example/501")], kind="plain")])
    add("T14_registry_heading_trailing_text",
        lane_of([("S101", f"{L}/101")], kn(1, "Cites S101.\n"), heading="## Registry (160 rows)"))
    add("T15_second_table_after_paths",
        lane_of([("S101", f"{L}/101")], kn(1, "Cites S101 and S999.\n"),
                after=[("S999", "not a registry row")]))
    add("T16_revision_git",
        lane_of([("S002", f"{L}/2")], kn(1, "Cites S002.\n"), extra={"git": True},
                old={"registry": {"rows": [("S001", f"{L}/1")], "indent": 0},
                     "knowledge": kn(1, "Cites S001 and S900.\n")}))
    add("T17_sibling_repo_headless_registry",
        lane_of([("S101", f"{L}/101")], kn(1, "Cites S501.\n")),
        [sib("alpha-shokunin", [("S501", "https://a.example/501")], kind="repo_headless")])
    add("T18_row_without_closing_pipe",
        lane_of([("S101", f"{L}/101"), ("S501", f"{L}/501")], kn(1, "Cites S101 and S501.\n"), omit=1))
    add("T19_h1_inside_registry",
        lane_of([("S101", f"{L}/101"), ("S501", f"{L}/501")], kn(1, "Cites S101 and S501.\n"), h1=1))
    add("T20_backtick_url_in_sibling_row",
        lane_of([("S101", f"{L}/101")], kn(1, "Cites S501 — see https://a.example/501 here.\n")),
        [sib("alpha-shokunin", [("S501", "`https://a.example/501`")])])
    add("T28_fleet_root_is_repo",
        lane_of([("S101", f"{L}/101")], kn(1, "Cites S501.\n")),
        [sib("alpha-shokunin", None, kind="noreg")])
    out[-1]["fleet_git"] = True
    out[-1]["fleet_registry"] = [("S501", "https://fleet.example/501")]
    add("T27_trailing_period_url_in_sibling_row",
        lane_of([("S101", f"{L}/101")], kn(1, "Cites S501 — see https://a.example/501 here.\n")),
        [sib("alpha-shokunin", [("S501", "https://a.example/501.")])])
    add("T21_alias_symlink_of_lane",
        lane_of([("S001", f"{L}/1"), ("S900", f"{L}/900")], kn(1, "Cites S900.\n"),
                extra={"git": True},
                old={"registry": {"rows": [("S001", f"{L}/1")], "indent": 0},
                     "knowledge": kn(1, "Cites S900.\n")}),
        [sib("alpha-shokunin", [("S777", "https://a.example/777")])], alias="other-shokunin")
    add("T22_default_fleet", lane_of([("S101", f"{L}/101")], kn(1, "Cites S501.\n")),
        [sib("alpha-shokunin", [("S501", "https://a.example/501")])], fleet_arg=False)
    add("T23_fleet_root_missing", lane_of([("S101", f"{L}/101")], kn(1, "Cites S501.\n")),
        [sib("alpha-shokunin", [("S501", "https://a.example/501")])])
    out[-1]["fleet_suffix"] = "/no-such-fleet"
    add("T24_resolved_only", lane_of([("S101", f"{L}/101")], kn(1, "Cites S101.\n")))
    add("T26_sibling_repo_stale_worktree",
        lane_of([("S101", f"{L}/101")], kn(1, "Cites S501.\n")),
        [{"name": "alpha-shokunin", "kind": "repo_stale",
          "registry": {"rows": [("S777", "https://a.example/777")], "indent": 0},
          "worktree_registry": {"rows": [("S501", "https://a.example/501")], "indent": 0}}])
    add("T25_sibling_without_registry", lane_of([("S101", f"{L}/101")], kn(1, "Cites S501.\n")),
        [sib("alpha-shokunin", None, kind="noreg")])
    return out


# --------------------------------------------------------------------------- running
def run_tool(tool: str, args: list[str], cwd: str) -> tuple[int, str, str]:
    p = subprocess.run([sys.executable, "-B", tool, *args], capture_output=True, cwd=cwd,
                       env=ENV, timeout=300)
    return p.returncode, p.stdout.decode("utf-8", "replace").replace("\r\n", "\n"), \
        p.stderr.decode("utf-8", "replace").replace("\r\n", "\n")


def split(out: str):
    lines = [ln for ln in out.split("\n") if ln]
    dang = [ln for ln in lines if ln.startswith("DANGLING ")]
    summary = lines[-1] if lines else ""
    return dang, summary


def classify(rc_a, out_a, rc_b, out_b) -> str:
    if rc_a == rc_b and out_a == out_b:
        return "agree"
    if out_a == out_b:
        return "exit-only"
    dang_a, summar_a = split(out_a)
    dang_b, summar_b = split(out_b)
    if summar_a == summar_b and sorted(dang_a) == sorted(dang_b):
        return "line-order"
    return "content"


def args_for(spec: dict, lane: str, fleet: str, rev: str | None) -> list[str]:
    args = ["--root", lane]
    if spec.get("fleet_arg", True):
        args += ["--fleet", fleet + spec.get("fleet_suffix", "")]
    if spec.get("lane", {}).get("git"):
        args += ["--revision", rev]
    return args


def gate_reference(lane: str, fleet: str, rev: str | None) -> tuple[int | None, str, str]:
    spec = importlib.util.spec_from_file_location("c57_gate", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        ref = mod.reference(lane, rev, fleet)
    except mod.Unevaluable as exc:
        return 2, "", f"unevaluable: {exc}"
    lines = []
    for i in sorted(ref["dang"]):
        cb, ow, um = ref["dang"][i]
        lines.append(f"DANGLING {i} cited-by={','.join(sorted(cb))} "
                     f"owners={','.join(sorted(ow)) or '-'} url-match={','.join(sorted(um)) or '-'}")
    lines.append("ids_cited={0} ids_resolved={1} dangling={2} owned_elsewhere={3} unowned={4}".format(*ref["summary"]))
    return (0 if ref["summary"][2] == 0 else 1), "\n".join(lines) + "\n", ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--count", type=int, default=44)
    ap.add_argument("--seed", type=int, default=57)
    ap.add_argument("--only")
    ap.add_argument("--gate-ref")
    ap.add_argument("--results", default=None)
    args = ap.parse_args()
    base = os.path.abspath(args.workdir)
    os.makedirs(base, exist_ok=True)

    specs = targeted_specs() + rand_specs(args.count, args.seed)
    if args.only:
        want = {x.strip() for x in args.only.split(",") if x.strip()}
        specs = [s for s in specs if s["name"] in want or s["name"].split("_")[0] in want]
    if not specs:
        print("no fixture selected", file=sys.stderr)
        return 64

    rows = []
    for spec in specs:
        lane, fleet, info = build_spec(spec, base)
        argv = args_for(spec, lane, fleet, info["revision"])
        cwd = os.path.join(base, "fixtures", spec["name"])
        rc_a, out_a, err_a = run_tool(TOOL_A, argv, cwd)
        rc_b, out_b, err_b = run_tool(TOOL_B, argv, cwd)
        verdict = classify(rc_a, out_a, rc_b, out_b)
        rec = {"fixture": spec["name"], "spec": spec, "argv": argv, "verdict": verdict,
               "a": {"rc": rc_a, "stdout": out_a, "stderr": err_a},
               "b": {"rc": rc_b, "stdout": out_b, "stderr": err_b}}
        if args.gate_ref == spec["name"] or args.gate_ref == "ALL":
            rc_g, out_g, err_g = gate_reference(lane, fleet, info["revision"])
            rec["gate_ref"] = {"rc": rc_g, "stdout": out_g, "stderr": err_g}
        rows.append(rec)
        flag = "OK  " if verdict == "agree" else "DIFF"
        print(f"{flag} {spec['name']:<38} A={rc_a} B={rc_b} {verdict}")
        if verdict != "agree" and not args.gate_ref:
            da, sa = split(out_a)
            db, sb = split(out_b)
            if sa != sb:
                print(f"     A summary: {sa}")
                print(f"     B summary: {sb}")
            only_a = [ln for ln in da if ln not in db]
            only_b = [ln for ln in db if ln not in da]
            for ln in only_a[:4]:
                print(f"     A only: {ln}")
            for ln in only_b[:4]:
                print(f"     B only: {ln}")
            if verdict == "exit-only":
                print(f"     stderr A: {err_a.strip()[:160]}")
                print(f"     stderr B: {err_b.strip()[:160]}")
    if args.gate_ref:
        for rec in rows:
            if args.gate_ref in ("ALL", rec["fixture"]):
                print("\n--- fixture", rec["fixture"], "argv:", " ".join(rec["argv"]))
                print("A (shipped) rc=%d\n%s" % (rec["a"]["rc"], rec["a"]["stdout"] or rec["a"]["stderr"]))
                print("B (oracle)  rc=%d\n%s" % (rec["b"]["rc"], rec["b"]["stdout"] or rec["b"]["stderr"]))
                g = rec["gate_ref"]
                print("GATE-REF    rc=%s\n%s" % (g["rc"], g["stdout"] or g["stderr"]))

    disagree = [r for r in rows if r["verdict"] != "agree"]
    print(f"\nfixtures={len(rows)} agreements={len(rows) - len(disagree)} disagreements={len(disagree)}")
    if args.results:
        with open(args.results, "w", encoding="utf-8") as fh:
            json.dump({"tool_a": TOOL_A, "tool_b": TOOL_B, "fixtures": rows}, fh, indent=1)
        print(f"results: {args.results}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
