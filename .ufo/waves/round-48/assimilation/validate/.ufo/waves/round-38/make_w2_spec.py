#!/usr/bin/env python3
"""Write the round-38 wave-2 spec (w2-spec.json) next to this file. Usage: make_w1_spec.py REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
DECL = "b0ab7f606d1f61fb6b850785866ba71583f629cc"
BASE = "af43a50fa399881eead9381d835b78a015e277a6"
SB = "/fast/scratch/hyaku/kake-r38w2"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = """Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, record tool, version, channel and reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via uv tool, npx or an official binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart."""

CONTEXT = f"""# Goal
Kake round 38, wave 2 (falsify). The L1 (KakeR38) holds integration; you are one leaf ATTACK seat. Lane repo: {L}. Lane axes: operability and freshness (web properties and publishing). Every item names what it attacks; try to show the landed work is wrong, overstated or harmful, with reproducible evidence. Time box: 30 minutes; a partial report (first line `PARTIAL:`) beats none.

# What landed (tip {REV}; base {BASE})
Read `git -C {L} show {REV}:SCORECARD.md | sed -n '/^## Round 37 — closure correction/,$p'` and `git -C {L} log --oneline {BASE}..{REV}`.
- C1 declared at {DECL} (counter v2 `.ufo/waves/round-38/sealed_count.py`, `met: passed >= 19 of 20 sealed cases`), WITHDRAWN before any build at 2dab7f31 after the control call (receipts `.ufo/waves/round-38/verification/control-*.json`, `mutref/`).
- C2 declared at 2dab7f31: `scripts/robots_audit.py` gains rules (h), (i), (k); counter v3 `.ufo/waves/round-38/sealed_count_v3.py`; predicate `met: passed >= 20 of 20 sealed cases`. Build 3ed8e15c (tool sha256 f4d057c4…baace); keys revealed at 99357694 (`.ufo/waves/round-38/sealed/cases.json` v2, `cases_v3.json` v3 — now public). Receipts `verification/c2-*.json`: 8 of 20 at base, 20 of 20 at 3ed8e15c. Revision mode refuses revisions that hold the key; use `--revision <rev> --key-revision 99357694` for pre-reveal revisions or `--tool-file F --key-revision 99357694` for files.
- Non-claim: selftest 194 fixtures, source_recheck caps, `.ufo/waves/round-38/criteria/` checks, `pinned_selftest.py`, harm receipts `verification/harm/`, SOURCES S098–S101, knowledge-entry round-38 section, QUALITY round-38 (j)–(n), PROVINCE/README/SKILL appends, lesson `corpus/lessons/round-38.md`, LOG.
- Wave-1 reports: `.ufo/waves/round-38/w1/`; control-call reports `.ufo/waves/round-38/ctl/`; retained tools `.ufo/waves/round-38/retained/`. Round-37 closure: `corpus/lessons/round-37-verifier-spotcheck.md`.

# Bounds
- You are a leaf: no subagents, no swarm, no admission or verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report; deliverables stay in your sandbox with absolute paths and sha256 in the report.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git (show, log, ls-tree, diff) is fine. Never run any jj command at /home/vgpnk/Projects/shokunin. Counters and selftests that write temp files run from a sandbox clone (`git clone -q {L} {SB}/<YourName>/clone && git -C {SB}/<YourName>/clone checkout -q {REV}`; export TMPDIR={SB}/<YourName>/tmp). Unset GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE first. Cap every run with `timeout` (≤900 s), ≤8 parallel processes, memory via `prlimit --as=4000000000` for blow-up inputs; kill any process tree you started before returning.
- Owned sites: no requests to the operator's web properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json). Network only for items naming a public URL; GET only; never pass a bot challenge.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: one-line report saying so; do not rephrase. Message only agent://KakeR38 for blockers; never agent://all. Plain English.

# Result
Report under 70 lines: what you attacked, exact commands with exit codes, observed outputs, evidence pointers (path:line, hash), verdict per attacked statement (holds / overstated / wrong). An unrun check has not passed.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, BASE=BASE)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
BOTH = ["operability", "freshness"]
K = "--key-revision 99357694"
V3 = ".ufo/waves/round-38/sealed_count_v3.py"
ACC = "Verdict per attacked statement with commands, exits and pointers."

def rv(name, role, axes, target, change):
    return item(name, role, axes, target, change, ACC)

ITEMS = [
    rv("RerunC2Receipts", "reviewer", OP, "C2's measured receipts `.ufo/waves/round-38/verification/c2-keyrev-at-*.json` (8, 8, 8, 20, refused).",
       "- In a sandbox clone at {REV}, re-run `python3 -B " + V3 + " --root <clone> --revision <rev> " + K + "` for af43a50f, b0ab7f60, 2dab7f31, 3ed8e15c, 99357694; diff each against the committed receipt (ignore nothing but key order). Confirm counterSha256 equals `sha256sum " + V3 + "` and toolSha256 equals the tool blob at each rev."),
    rv("RerunControlsV3", "reviewer", OP, "The C2 control, ablation and mutant receipts `verification/v3/*.json` and `w1attack/CtlExampleK.json`.",
       "- Re-score every tool file under `.ufo/waves/round-38/retained/` (controls/, private/reference.py, private/ablations/, MutRefPass/mutants/) with `--tool-file F " + K + "`; match each against its receipt by toolSha256; list mismatches and any receipt without a retained tool."),
    rv("RerunC1Withdrawal", "reviewer", OP, "C1's withdrawal facts: v2 receipts `verification/control-*.json`, `mutref/`, `pre/` under `.ufo/waves/round-38/sealed_count.py` with key `cases.json` (v2 pin 8b3fac55…).",
       "- Re-score under v2 with `--key-revision 99357694` the retained tools; confirm 29 of 42 mutants met, 13 at 20, which control receipts met. Check the SCORECARD sentences in 'Round 38 — control call results' against them and say which are overstated."),
    rv("AuditKeyV3", "reviewer", OP, "The revealed C2 key `.ufo/waves/round-38/sealed/cases_v3.json` and the declaration's description of it (SCORECARD 'Round 38 — C2 declared', key bullet).",
       "- Verify: 20 cases, bullets c/d/j/u/r 4 each; 43 excluded ASCII characters each alone in its own check at the six positions claimed; each listed added check exists; every run states checksEvaluated and it equals the non-check_invalid count; every (c)/(d)/(u)/(r) case has a finding and a holding check. Script it; paste counts."),
    rv("CriticKeyExpectations", "critic", OP, "Every expectation in `.ufo/waves/round-38/sealed/cases_v3.json`.",
       "- Re-derive each run's expected exit, verdict, findings and checksEvaluated by hand from the round-37 contract plus (h), (i), (k) and the C2 clarifications (do not run any tool first). List each run where the key disagrees with your reading, with the sentence you rely on; only then run the reference `.ufo/waves/round-38/retained/private/reference.py` to see whether it shares the error."),
    rv("ReviewToolDiff", "reviewer", OP, "The C2 build: `git diff {BASE} 3ed8e15c -- scripts/robots_audit.py`.",
       "- Review each hunk against (h), (i), (k) and the round-37 contract: the 15-digit long-integer sentinel, parse_constant, the forbidden-ASCII regex (exactly 43 chars?), normalize-before-compare, docstring readings. Construct inputs where the tool departs from the contract text; run them."),
    rv("SentinelBuild", "sentinel", OP, "The built tool `scripts/robots_audit.py` at 3ed8e15c under adversarial manifests.",
       "- Re-run the wave-1 inputs `/fast/scratch/hyaku/kake-r38w1/SentinelManifestDoS/inputs/` with its run.sh on the build, then add: deep nesting (100k `[`), 64 MiB of mixed long numbers, 100k checks with 43-char URLs, huge exponents, a NUL in robots path, NaN inside nested arrays. Report crashes, tracebacks, timeouts (>20 s), memory errors."),
    rv("MutBuildTool", "mutation-tester", OP, "The built tool's (h), (i), (k) code at 3ed8e15c versus its two instruments (selftest 194 and the v3 key).",
       "- Write 25–40 single-point mutants of the (h)/(i)/(k) code in {sb}/mutants/; run `python3 -B scripts/robots_audit_selftest.py --tool M` and `python3 -B " + V3 + " --root <clone> --tool-file M " + K + "` on each. Table: mutant, selftest result, v3 passed, survivors of both."),
    rv("DiffToolVsIndependent", "reviewer", OP, "Agreement between the build (3ed8e15c) and wave-1 `ExecIndependent`'s blind implementation `/fast/scratch/hyaku/kake-r38w1/ExecIndependent/independent_robots_audit.py` (ee78ba46…).",
       "- Differential fuzz ≥5000 generated manifests stressing (h), (i), (k) and (c)/(d); report every disagreement with a minimal input and which side the contract supports. Also score the independent file with the v3 counter (`--tool-file`)."),
    rv("AblateBuilds", "mutation-tester", OP, "The C2 declaration's claim that the four 20-of-20 control-call tools are builds (all three rules), not controls (wave-1 `CriticControlReceipts` remedy).",
       "- For each of `.ufo/waves/round-38/retained/controls/{{CtlLabelShortcut-delegate_ceiling,CtlBaseWrapper-care,CriticPredicate-rulepatch,CriticPredicate-rulepatch_pct}}.py`, make three ablations removing (h), (i) or (k) only; score all 12 with v3 (`--tool-file`). A rule-removed tool that still scores 20 would be a class-(6) control meeting the predicate: name it."),
    rv("CriticReclassification", "critic", OP, "Whether C2's pre-named control classes are a post-hoc reclassification of controls that already met (round-37 closure: 'a disposition that reclassifies the control is not an option unless the declaration named that class beforehand').",
       "- Build the strongest case each way from the SCORECARD text, commit times (`git log --format='%h %cI' {BASE}..{REV}`) and receipt times. Then say what a closure following the round-37 ruling would most likely decide, and what evidence would change it."),
    rv("CriticAxisFit", "critic", OP, "C2's axis naming and claim sizing after data (prompt /home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-38.md §6 item 9).",
       "- Is 'operability (tool repair)' the surface changed? Is any of (c)/(d) re-scoring a held rule counted as the move? Do the measured-results and lesson texts use universal clauses the counter does not enumerate? Quote each."),
    rv("ReviewSelftest194", "reviewer", OP, "The 57 new fixtures of `scripts/robots_audit_selftest.py` at {REV}.",
       "- Check each new fixture's expectation against the contract sentence it names; run the selftest on the build, base, the independent implementation and the round-37 shortcut; list wrong or tolerant fixtures."),
    rv("MutSelftestSurvivors", "mutation-tester", OP, "Wave-1 `MutBaseSelftest` survivors (10 of 25 mutants passed the 137 selftest) against the 194 selftest.",
       "- Re-create those mutants from `.ufo/waves/round-38/w1/MutBaseSelftest.md` (or its sandbox `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/`), apply them to the build tool where they still apply, and run the 194 selftest; list which survive now."),
    rv("ReviewCcCheck", "reviewer", OP, "`.ufo/waves/round-38/criteria/control_consequence_check.py` (QUALITY (j) check) and the L1's narrowing to claim-named receipts.",
       "- Read it; construct verification dirs where it gives a false pass or false fail (renamed control, claim receipt named otherwise, met mismatching passed); run its selftest and its red/green receipts in `criteria/receipts/`."),
    rv("MutCcCheck", "mutation-tester", OP, "The QUALITY (j) check's sensitivity.",
       "- 10–15 single-point mutants of `control_consequence_check.py`; for each, does `--selftest` or the round-37 red run (exit 1) change? Table of survivors."),
    rv("ReviewTimelineCheck", "reviewer", OP, "`.ufo/waves/round-38/criteria/timeline_check.py` and its receipts `criteria/receipts/timeline-*.txt`; the claim that round-38 control receipts landed 58 s before wave-1 dispatch.",
       "- Re-run it; check what time it reads (commit time vs author time; is `w1-dispatched-at.txt` authenticated?). Cross-check with the omp task dispatch time if any record exists in the lane (`w1-dispatch.json`)."),
    rv("ReviewPinnedSelftest", "reviewer", OP, "`.ufo/waves/round-38/pinned_selftest.py` and `verification/harm/*.json`, `verification/postfix/r37-postfix-selftest-pinned.json` (QUALITY (l)).",
       "- Verify each receipt's toolSha256 against `git cat-file -p <toolRevision>:<toolPath> | sha256sum`; try to make the runner record a wrong pin."),
    rv("ReviewRecheckCaps", "reviewer", BOTH, "`git diff {BASE} {REV} -- scripts/source_recheck.py scripts/source_recheck_hardening_selftest.py` (16 MiB body cap, MemoryError handling).",
       "- Review against the round-36 contract; re-run hardening 9/9, selftest 106/106 and the round-36 counter (`.ufo/waves/round-36/sealed_count.py --tool-file scripts/source_recheck.py --key-revision fd1fb723`)."),
    rv("SentinelRecheckCaps", "sentinel", BOTH, "The body cap in `scripts/source_recheck.py` at {REV}.",
       "- Try to bypass it: a body path that is a symlink to /dev/zero, a FIFO, a file that grows after stat, a sparse 2 GiB file, many 15 MiB bodies in one manifest. Report crashes and memory use under prlimit."),
] + [
    rv(f"ReopenGate{sid}", "scout", FR, f"The round-38 Gate line for {sid} in `corpus/lessons/round-38.md` and its SOURCES.md row.",
       f"- GET {url} yourself; locate the quoted sentence exactly (section, line); compare access facts (status, sha256 where given) and the row's scope/anchor/teaches cells with the page. Verdict: quote present verbatim? row accurate?")
    for sid, url in [("S034", "https://www.rfc-editor.org/rfc/rfc8259.txt"), ("S098", "https://www.rfc-editor.org/rfc/rfc3986.txt"),
                     ("S099", "https://www.rfc-editor.org/rfc/rfc9309.html"), ("S100", "https://docs.python.org/3/library/json.html"),
                     ("S101", "https://url.spec.whatwg.org/")]
] + [
    rv("ReviewSourcesRows", "reviewer", FR, "SOURCES rows S098–S101 and the S034 used-by change at {REV} against /home/vgpnk/Projects/shokunin/CORPUS.md 'SOURCES.md — where a shokunin learns'.",
       "- Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`; check each row's cells, the 'every change logged old→new' rule in the lesson, and whether mined rows are really cited by the knowledge entry."),
    rv("ReviewKnowledgeEntry", "reviewer", OP, "The 'Round 38 amendments' section of `corpus/knowledge/robots-txt-rules.md` and its new source line.",
       "- Each sentence vs its cited row/section and vs the built tool's behaviour (run the tool on an input per sentence). Flag overstated or unsourced sentences."),
    rv("ReviewLessonNumbers", "reviewer", OP, "Every number and pointer in `corpus/lessons/round-38.md`.",
       "- Re-derive each from receipts or git; list mismatches."),
    rv("ReviewScorecardR38", "reviewer", OP, "SCORECARD round-38 sections (closure correction, C1 declaration, control call results, C2 declared, measured results).",
       "- Every number vs receipts; every 'before any build' ordering claim vs commit times; any rewrite of earlier lines (`git diff {BASE} {REV} -- SCORECARD.md`)."),
    rv("ReviewQualityProvince", "reviewer", OP, "QUALITY round-38 criteria (j)–(n), PROVINCE 'Round-38 robots audit repair step', README r38 row, SKILL round-38 amendment.",
       "- Accuracy vs receipts; each criterion's red/green claims re-run."),
    rv("ReviewHarm", "reviewer", BOTH, "No-harm statement: base {BASE} vs tip {REV}.",
       "- `git diff --numstat {BASE} {REV} -- SCORECARD.md SKILL.md PROVINCE.md LOG.md SHONEN.md corpus/` (deletions?); in clones of both, run every `scripts/*selftest*.py` (read usage lines) and the round-36/37 counters in --tool-file mode; table base vs tip."),
    rv("ReviewContainment", "reviewer", OP, "Seat containment this round.",
       "- `git -C /home/vgpnk/Projects/shokunin status --porcelain` filtered for kake/round-38 content; `git -C {L} status --porcelain`; lane files changed outside reports by seats (compare commit contents to the L1's commits); list any seat report disclosing out-of-bound actions (grep reports for 'DISCLOSURE', 'test -d', 'ls /fast')."),
    rv("ReviewRealRun", "reviewer", BOTH, "The built tool on real inputs.",
       "- Run `scripts/robots_audit.py` at 3ed8e15c on the round-37 real-run manifest (`.ufo/waves/round-37/realrun/`) and on wave-1 `ExecRealRunPrep`'s manifest (`/fast/scratch/hyaku/kake-r38w1/ExecRealRunPrep/realrun/` if present); compare with base; justify each changed result from the contract."),
    rv("RevengerReadings", "revenger", OP, "The build's own readings (docstring) versus the C2 clarifications and the independent implementation's readings.",
       "- Extract each reading from the build docstring and from `/fast/scratch/hyaku/kake-r38w1/ExecIndependent/` report; list where they choose differently (e.g. 15 vs 4000 digit sentinel, bare `%`, `/robots.txt?`, dot segments) and show an input for each."),
]

spec = {
    "wave": "kake-r38-w2",
    "milestone": "r38-falsify",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-38/w2",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w2-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
