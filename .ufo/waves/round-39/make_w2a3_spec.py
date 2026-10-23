#!/usr/bin/env python3
"""Round-39 attempt-3 wave 2: the key-blind build seat plus fresh attack seats on wave 1's outputs.
Usage: make_w2a3_spec.py REV   (REV = lane commit holding every wave-1 control receipt)"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
DECL = "ceecb1b1f9093471eb0b17d2c9190e78bceb0b78"
SB = "/fast/scratch/hyaku/kake-r39a3w2"
W1 = "/fast/scratch/hyaku/kake-r39a3w1"
R1 = f"{L}/.ufo/waves/round-39/w1a3"
CONTRACT = f"{L}/.ufo/waves/round-39/c1-contract.md"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = ("Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — "
           "read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool, version, channel and reason in your report). "
           "All pacman transactions are PAUSED host-wide (orchestrator ruling 2026-10-20): install via uv tool, npx or an official "
           "binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.")

CONTEXT = f"""# Goal
Kake round 39 (attempt 3), wave 2: one key-blind BUILD seat writes the claimed tool from the contract alone, and fresh attack seats falsify what wave 1 produced (controls, mutants, the (j) check, source candidates, non-claim patches). The L1 (agent id KakeR39A3) is the only integrator and scorer; you are one leaf seat. Lane repo: {L} (tip {REV}). Lane axes: operability and freshness.

# The claim
C1 (capability, declared at {DECL}): a new tool `scripts/sitemap_audit.py` audits local sitemap and sitemap-index files against {CONTRACT} (sentences 1–34). A frozen counter scores tools against a SEALED 24-case key; every tool other than the build bytes is a control. Wave-1 reports: {R1}/<Seat>.md. Control receipts (totals only): {L}/.ufo/waves/round-39/verification/a3/*.json — read only `label`, `passed`, `met`, `toolSha256`; never the `rows` or `why` fields (they describe sealed cases).

# Key-blindness (binding)
Never read, list or search any path under /fast/scratch whose name contains `l1priv` or `sealed`, /fast/scratch/hyaku/kake-r39a2/, /fast/scratch/hyaku/kake-r39a3/, or any file named cases.json, build_key.py or make_key.py. Do not run the counter. The BUILD seat additionally never reads anything under /fast/scratch except its own sandbox, never reads {L}/.ufo/waves/round-39/a3-controls/, {L}/.ufo/waves/round-39/w1/, {R1}/, or any file named reference.py, sitemap_ref.py, sitemap_audit_ref.py or control.py.

# Bounds
- You are a leaf: no subagents, no swarm, no verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git is fine. Never run jj at /home/vgpnk/Projects/shokunin. Sandbox clones: `git clone -q {L} {SB}/<YourName>/clone` after unsetting GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE.
- Cap every run with `timeout` (≤600 s), ≤8 parallel processes, `prlimit --as=4000000000`; bound every file you write (≤200 MB per seat; never append in a loop to a file Python imports; never point a log at sitecustomize.py or a .pth); `df -h /fast` before writing >1 GB; kill every process tree you start before returning. Never run `du` or `find` over /fast/scratch as a whole.
- Network: only URLs your item names, GET only. Never request the operator's properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json).
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: a one-line report saying so; do not rephrase. Message only agent://KakeR39A3 for blockers; never agent://all. Plain English.

# Result
Report under 60 lines: what you checked or built, exact commands with exit codes, paths with sha256, findings with path:line, and per attacked statement: holds / overstated / wrong. An unrun check has not passed. Time box: 30 minutes (BUILD: 40); a partial report (first line `PARTIAL:`) beats none.
"""


def item(name, role, axes, target, change, acceptance="Per attacked statement: holds / overstated / wrong, with commands, exits and path:line."):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, DECL=DECL, W1=W1, R1=R1, CONTRACT=CONTRACT)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR, BOTH = ["operability"], ["freshness"], ["operability", "freshness"]

BUILD = item("BuildSitemapAudit", "executor", OP,
             "The claimed tool `scripts/sitemap_audit.py` and its public selftest `scripts/sitemap_audit_selftest.py`, written in {sb}/ only (the L1 copies them into the lane).",
             "- Read ONLY the contract {CONTRACT} and the retained sources {L}/.ufo/waves/round-39/sources/ (S102–S104). Implement every sentence 1–34 exactly; Python 3 standard library only; the tool runs as `/usr/bin/python3 -B sitemap_audit.py --manifest <path>` with only /usr, the manifest's directory (read-only) and a private /tmp visible; no network; one JSON document on stdout; exits per sentences 2, 3 and 34.\n"
             "- Write `sitemap_audit_selftest.py --tool <path>` that materializes ≥60 small fixtures (manifest + files) in a temp dir, runs the tool and checks exit, verdict, error and finding sets; every sentence 1–34 has a fixture and every rule (a)–(k) both polarities; prints `PASS n/N`, exit 0 only when all pass. Show it fails against a tool that prints nothing and against a constant-clean tool.\n"
             "- Add a header docstring citing the contract path and S102–S104. No code copied from any other file.",
             "Paths and sha256 of both files; selftest output against your tool and the two failing tools; a sentence→fixture map.")


def ITEMS_ATTACK():
    return json.loads((HERE / "w2a3-attacks.json").read_text())


spec = {
    "wave": "kake-r39a3-w2",
    "milestone": "r39-build-falsify-a3",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-39/w2a3",
    "context": CONTEXT,
    "items": [BUILD] + [item(**a) for a in ITEMS_ATTACK()],
}
(HERE / "w2a3-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(spec["items"]), "items")
