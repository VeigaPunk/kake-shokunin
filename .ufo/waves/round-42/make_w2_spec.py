#!/usr/bin/env python3
"""Round-42 wave 2 (falsify): fresh seats attack the landed build, the frozen counter v3, the harm
evidence, the new SOURCES rows and the records. Usage: make_w2_spec.py REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
SB = "/fast/scratch/hyaku/kake-r42w2"
SH = "/fast/scratch/hyaku/kake-r42/shared"
W = f"{L}/.ufo/waves/round-42"
COUNTER = f"{W}/c42_count_v3.py"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = ("Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — "
           "read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool, version, channel and reason in your report). "
           "All pacman transactions are PAUSED host-wide (orchestrator ruling 2026-10-20): install via uv tool, npx or an official "
           "binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.")

CONTEXT = f"""# Goal
Kake round 42, wave 2 (falsify): attack what wave 1 and the L1 landed. The L1 (agent id KakeR42) is the only integrator; you are one leaf seat with one attack item. Lane repo: {L} (tip {REV}). Lane axes: operability and freshness. Ordinary software testing of a local, offline command-line tool that audits sitemap XML files.

# What landed (read {L}/SCORECARD.md sections "Round 42 — …", newest last)
- C1 (frozen at 1e1da697): the URL check of `{L}/scripts/sitemap_audit.py` was rewritten (build at 020bc457, tool sha256 914ebdee…; a byte-table scanner) to keep the round-41 tool's judgments (copy {SH}/tip41.py, sha256 50287ac6…) while costing at most 2.0x the round-40 tool's CPU (copy {SH}/base40.py, 4de35f8c…) on five timing shapes. Counter v3: {COUNTER} (sha256 ce2d5a0c…). Predicate: `met: the tool's exit code and output equal the round-41 tool's on every generated run, and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's`. Score WITHOUT --seed (random seed recorded).
- Kill rule (2): after the build is scored, any control that meets the predicate means C1 is NOT met. A control = a tool that judges some value differently from tip41 (give the witness value) or lowers measured CPU without doing the work. A tool equal to tip41 on every value is not a control.
- Harm rule H1–H5: selftest (235 fixtures, `python3 -B {L}/scripts/sitemap_audit_selftest.py --tool <tool>`), round-39 real run byte-equal (`jq -S . | sha256sum` → fd985a41…, inputs {L}/.ufo/waves/round-41/realrun/), cost (the ratios), H4 probe {W}/harm/h4_probe.py, H5 selftest under Python 3.10 (`~/.local/share/uv/python/cpython-3.10.22-linux-x86_64-gnu/bin/python3.10`).
- Frontier: SOURCES rows S120–S125 ({L}/corpus/SOURCES.md; S117–S119 restored to their committed cells), lesson {L}/corpus/lessons/round-42.md.

# Scoring a tool
`timeout 900 prlimit --as=8000000000 -- python3 -B {COUNTER} --root {L} --tool-file <tool> --label <YourName>-<suffix> --out {SB}/<YourName>/<suffix>.json` (exit 0 met, 1 not met, 2 cannot evaluate; ~90-150 s; at most 3 at once per seat).

# Bounds
- You are a leaf: no subagents, no swarm, no verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git is fine. Never run jj at /home/vgpnk/Projects/shokunin. Clone only into {SB}/<YourName>/ with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset.
- Cap every run with `timeout` (≤900 s), ≤8 parallel processes, `prlimit --as=8000000000`; bound every file you write (≤300 MB per seat; never append in a loop to a file Python imports; never point a log at sitecustomize.py or a .pth); kill every process tree you start before returning. Never run `du` or `find` over /fast/scratch as a whole.
- Network: only URLs your item names, GET only. Never request the operator's properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json).
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: a one-line report saying so; do not rephrase. Message only agent://KakeR42 for blockers; never agent://all. Plain English.

# Result
Report under 60 lines: first line MET / NOT MET for control seats, or the verdict on what you attacked; exact commands with exit codes; tool paths with sha256; findings with path:line; per checked statement holds / overstated / wrong. An unrun check has not passed. Time box: 25 minutes; a partial report (first line `PARTIAL:`) beats none.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, SH=SH, W=W, COUNTER=COUNTER)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
CTL_ACC = ("First line MET or NOT MET. Per tool: path, sha256, one-line change, receipt (seed, equalRuns, ratios, met), which run "
           "caught it, and for a meeting tool a witness value where its `_parse_url` or CLI output differs from tip41 (or none found).")


def mut(name, what):
    return item(name, "mutation-tester", OP,
                "Attacks: counter v3's power to catch one-member changes of the LANDED build in " + what,
                "- Copy {L}/scripts/sitemap_audit.py (the build) into {sb}/. Make ≥5 single-member mutants in that area (one class member, one table byte, one branch condition). Keep each mutant fast.\n- Score every mutant with the counter (no --seed). For a mutant that meets, search for a witness (compare its `_parse_url` with tip41's on values you choose).",
                CTL_ACC)


def ctl(name, what, how):
    return item(name, "executor", OP,
                "Attacks: counter v3 against a fresh control class: " + what,
                "- Build ≥3 variants in {sb}/ from {L}/scripts/sitemap_audit.py (the fast build) or {SH}/tip41.py. " + how +
                " Keep the skip; try hard to meet the predicate. Score each with the counter (no --seed).",
                CTL_ACC)


def reopen(name, rows, urls, what):
    return item(name, "scout", FR,
                "Attacks: SOURCES rows " + rows + " in {L}/corpus/SOURCES.md and their Gate lines in {L}/corpus/lessons/round-42.md.",
                "- GET " + urls + " ; record HTTP status, byte count and sha256; locate each quoted sentence of the rows and Gate lines with line numbers. " + what,
                "Per row: quote found verbatim yes/no (line), sha256 equal to the row yes/no, scope/teaches supported / overstated / wrong.")


ITEMS = [
    mut("MutBuildPath", "the path and pchar tables (`_TABLE_PCHAR`, `_path_ok`)."),
    mut("MutBuildQueryFragment", "query and fragment scanning (`_TABLE_QUERY`, the second `#`, `?`)."),
    mut("MutBuildAuthority", "userinfo, host and port scanning (`_TABLE_USERINFO`, `_TABLE_REGNAME`, `@`, `:` handling)."),
    mut("MutBuildIPLiteral", "the IP-literal table and bracket handling (`_TABLE_IP_LITERAL`, `[`/`]`)."),
    mut("MutBuildPercent", "the percent rule (`_BAD_PCT_RE`, where it is applied, hex case)."),
    mut("MutBuildNonAscii", "non-ASCII handling (UTF-8 encode with surrogatepass, bytes ≥0x80 accepted where unreserved stands, rejected in IP literals)."),
    mut("MutBuildScheme", "scheme scanning (`_TABLE_SCHEME`, first character, `://`)."),
    ctl("CtlFreshShape", "fast paths keyed on the v3 timing shapes (file size, entry count, value length, run without `/`).",
        "Read {COUNTER} shape_t1..t5 first; key a cheaper partial judgment on what you can observe."),
    ctl("CtlFreshPartial", "partial judgments that skip a rarely generated region (e.g. the middle of very long values, only one occurrence of a delimiter, only the first N bytes after `%`).",
        "Pick regions run E and runs A–D sample least."),
    ctl("CtlFreshMeasure", "lowering the recorded CPU without less work, against v3's runner (PR_SET_DUMPABLE 0, append-mode timing file).",
        "Try /proc access to the runner, signals, ptrace, a nested user namespace, writing to fds, threads; read RUNNER first."),
    ctl("CtlFreshCache", "precomputation or caching that survives random seeds (tables of common prefixes, per-host results).",
        "Seeds are random at scoring time."),
    item("RerunBuildA", "reviewer", OP, "Attacks: the L1's build receipts (`{W}/verification/build/c1-v3-020bc457-*.json`).",
         "- Re-run the counter on `--revision {REV}` twice (no --seed), into {sb}/; compare with the L1 receipts (equalRuns, ratios, counterSha256, toolSha256).",
         "Your receipts and whether the L1's hold."),
    item("RerunBuildB", "reviewer", OP, "Attacks: the T5 and T2 margins of the build (closest ratios to 2.0).",
         "- Re-run the counter on `--revision {REV}` twice more (no --seed) and report every ratio; state the largest ratio seen and its distance from 2.0.",
         "Receipts and the margin."),
    item("ReviewBuildFinal", "reviewer", OP, "Attacks: the final build bytes `{L}/scripts/sitemap_audit.py` at {REV} (QUALITY (t): fresh review of final bytes).",
         "- Read the whole URL section and `_parse_url`; compare with `git -C {L} show 1ef7a0e9:scripts/sitemap_audit.py`; look for any value class where the scanner and the round-41 regex disagree (reason from code, then confirm by running both `_parse_url`s on the values).",
         "Findings with path:line and confirmed witness values (or none)."),
    item("ReviewBuildDifferential", "reviewer", OP, "Attacks: 'keeps the round-41 tool's judgments' beyond the counter's generator.",
         "- Write your own generator in {sb}/ (different from the counter's: e.g. grammar-directed RFC 3986 random URIs, Unicode categories, very long and very short values) and compare build vs tip41 `_parse_url` on ≥1,000,000 values.",
         "Counts and every disagreement with values."),
    item("ReviewHarmSelftest", "reviewer", OP, "Attacks: H1 and H5 receipts (`{W}/verification/harm/selftest-*.txt`).",
         "- Re-run the selftest on the build and on tip41 under the host python3 and under Python 3.10.22; check the ten `r42_*` fixtures pass on both tools (guards only) and no `r41_*` result changed.",
         "Counts, exit codes, per-fixture differences."),
    item("ReviewHarmRealRun", "reviewer", OP, "Attacks: H2 (round-39 real run byte-equal).",
         "- Run the build on {L}/.ufo/waves/round-41/realrun/manifest.json from that directory; `jq -S . | sha256sum`; compare with fd985a41… and with tip41's output.",
         "Hashes, exit codes."),
    item("ReviewHarmH4", "reviewer", OP, "Attacks: H4 (`{W}/harm/h4_probe.py`, receipts `{W}/verification/harm/h4-*.json`).",
         "- Read the probe; re-run it on the build at two fresh seeds and at 924141; check validReject = 0 and newAccept = 0 and that the probe's oracle wheel sha256 is pinned.",
         "Counts per seed; probe defects with path:line."),
    item("ReviewCounterV3", "reviewer", OP, "Attacks: counter v3's new code (run E `cases_e`/`slot_value`, the T-shape defect placement, T4 renaming, RUNNER dumpable, append mode).",
         "- Read the diff `git -C {L} diff c23c145c 3490614 -- .ufo/waves/round-42/c42_count_v3.py` against c42_count_v2.py; generate runs with a few seeds by importing the module; check each docstring sentence.",
         "Per statement holds / overstated / wrong."),
    item("SentinelV3Timing", "reviewer", OP, "Attacks: v3 timing integrity (wave-1 SentinelCounterSandbox and CtlCpuHide forged CPU under v1).",
         "- Re-run the wave-1 forgers {L}/.ufo/waves/round-42/controls/w1/CtlCpuHide/ctl_fake_timing.py and controls/w1/SentinelCounterSandbox/timer_probe.py under v3; then try one new forging route (e.g. /proc/<runner>/fd via a different path, writing through /proc/<runner>/root, signal timing).",
         "Whether any route still forges, with receipts."),
    item("CriticKillRule", "critic", OP, "Attacks: the counter redesigns v1→v2→v3 before the build was scored, and the 'not a control' classification of the three v3-meeting mutants.",
         "- Read only; no code runs. Using SCORECARD round-42 sections and the round prompt §6.9 ({L}/../.ufo/prompts/kake-round-42.md), decide whether the redesigns are 'fix before data' or 'rule changed after data', whether the equivalence differential was frozen before use, and whether C1 should be exploratory.",
         "Per statement holds / overstated / wrong; the strongest closure attack."),
    item("CriticHarm", "critic", OP, "Attacks: no-harm under H1–H5 for the landed build and for the round-41 URL rule's admission (routed defect 2 of {L}/corpus/lessons/round-41-verifier-spotcheck.md).",
         "- Read only. Is H5 (added after the L1 saw the two builds' Python 3.10 results, before any counter scoring) a rule fitted to data? Does the round reprice the round-41 cost honestly? What harm is unpriced (memory, wall time, maintainability of a 200-line scanner)?",
         "Per clause holds / overstated / wrong."),
    item("CriticClaimSizing", "critic", OP, "Attacks: C1's sizing and axis naming against §6.9 and QUALITY (n), (o), (u).",
         "- Read only. Is the target one a do-nothing or a cheap shortcut meets? Universal clauses? Is 'operability, runnable cost' the surface changed?",
         "Per statement holds / overstated / wrong."),
    reopen("ReopenRFC3986Rows", "S117 and S120", "https://www.rfc-editor.org/rfc/rfc3986.txt",
           "Also: are S117's cells now byte-equal to `git -C {L} show 9e3c31d2:corpus/SOURCES.md` (except used-by)? Does S120 open with `supersedes S117 —`?"),
    reopen("ReopenPyPIRows", "S118, S119, S121, S122", "https://pypi.org/pypi/abnf/2.9.1/json and https://pypi.org/pypi/rfc3987/1.3.8/json",
           "Also check S118/S119 cells against 9e3c31d2 and the `supersedes` openers of S121/S122."),
    reopen("ReopenPythonRe", "S123", "https://docs.python.org/3/library/re.html", "Is S123 used by anything this round (the landed build does not use possessive quantifiers)? Say whether its used-by is honest."),
    reopen("ReopenRFC9844", "S124 and S125", "https://www.rfc-editor.org/rfc/rfc9844.txt and https://www.rfc-editor.org/rfc/rfc6874.txt and https://www.rfc-editor.org/info/rfc6874",
           "Is S125's rejection reason right? Does S124 support the zone-id behaviour as the SCORECARD and the tool comment state it?"),
    item("ReviewSourcesRule2", "reviewer", FR, "Attacks: the S117–S119 repair against CORPUS.md §SOURCES.md rule 2 (/home/vgpnk/Projects/shokunin/CORPUS.md and the canonical /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md).",
         "- `git -C {L} diff 1ef7a0e9 {REV} -- corpus/SOURCES.md`; decide whether reverting in-place edits to committed cells plus superseding rows follows the rule, and run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (read-only).",
         "Census output and exit; per row holds / wrong."),
    item("ReviewLesson", "reviewer", OP, "Attacks: {L}/corpus/lessons/round-42.md (Gate, row changes, Mistakes if present) — every pointer resolves and every quote matches.",
         "- Resolve each path:line and commit hash; re-read each quoted line.",
         "Per pointer resolves / broken."),
    item("ReviewQualityV", "reviewer", OP, "Attacks: the harm-rule criterion check `{W}/criteria/harm_rule_check.py` (to become QUALITY (v)).",
         "- Run it on round 41 (`git -C {L} show 1ef7a0e9:SCORECARD.md`, expect exit 1) and round 42 (lane SCORECARD, expect 0); then write two synthetic harm rules that should pass/fail and show whether the lexical check can be fooled.",
         "Exit codes and whether the check discriminates."),
    item("ReviewCommentFix", "reviewer", OP, "Attacks: routed defect 3 — the tool comment at `{L}/scripts/sitemap_audit.py:67-82` must match SKILL.md and the tool's behaviour.",
         "- Read the comment, `grep -n sitemap_audit {L}/SKILL.md`, and confirm each sentence by running the tool's `_parse_url` on values (zone ids `%eth0`, `%25eth0`, `%é`, `%en|0`, port 65536).",
         "Per sentence holds / wrong."),
    item("ReviewInfoBuild", "reviewer", OP, "Attacks: the L1's choice of build (ExecBuildIndependent) over ExecBuildRegex and the Python 3.10 evidence.",
         "- Run both builds' selftests under Python 3.10.22 and 3.11.17 (`~/.local/share/uv/python/cpython-3.11.17-linux-x86_64-gnu/bin/python3.11`); confirm the regex build fails only below 3.11; read `{W}/verification/build/info-execbuildregex.json`.",
         "Results and whether the choice was recorded before scoring (commit order)."),
    item("ScoutSiblingCost", "scout", OP, "Attacks: kake's URL rule vs sibling lanes' URL checks — does any sibling tool already copy the round-41 regex (and its cost)?",
         "- Read-only grep of /home/vgpnk/Projects/shokunin/*-shokunin/scripts for `_URI_RE`, `0010ffff`, `urlsplit` validators.",
         "Pointers and one line each."),
    item("ReviewMisroot", "reviewer", OP, "Attacks: the round's fleet-root hygiene.",
         "- Run `git -C /home/vgpnk/Projects/shokunin status --porcelain` and list any untracked file whose content names kake round 42 (read-only; do not move anything).",
         "The list (or none)."),
]

spec = {
    "wave": "kake-r42-w2",
    "milestone": "r42-falsify",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-42/w2",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w2-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
