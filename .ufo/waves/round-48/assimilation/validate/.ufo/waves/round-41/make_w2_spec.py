#!/usr/bin/env python3
"""Round-41 wave 2 (falsify): fresh seats check what wave 1 and the L1 produced — the build, the kill-rule
record, the receipts, the new selftest fixtures, the criteria checks, the source rows and the counter v2
information. Usage: make_w2_spec.py BUILD_REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
SB = "/fast/scratch/hyaku/kake-r41w2"
W = f"{L}/.ufo/waves/round-41"
C1 = f"{W}/c1_count.py"
C2 = f"{W}/c1_count_v2.py"
CONTRACT = f"{L}/.ufo/waves/round-39/c1-contract.md"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = ("Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — "
           "read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool, version, channel and reason in your report). "
           "All pacman transactions are PAUSED host-wide (orchestrator ruling 2026-10-20): install via uv tool, npx or an official "
           "binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.")

CONTEXT = f"""# Goal
Kake round 41, wave 2 (falsify): fresh seats check what the round produced. The L1 (agent id KakeR41) is the only integrator; you are one leaf seat and you did not take part in wave 1. Lane repo: {L}; the build is landed at {REV}. Lane axes: operability and freshness. This is ordinary software review and testing of a local, offline command-line tool that audits sitemap XML files.

# What the round claims (read {L}/SCORECARD.md, sections starting "Round 41")
C1 (operability, exploratory): `{L}/scripts/sitemap_audit.py` now judges a `loc` (after the contract's sentence-21 whitespace strip) or a manifest `sitemapUrl` as written against the RFC 3986 `URI` grammar with an authority and a non-empty host, before `urlsplit` splits it (contract {CONTRACT}, sentences 4 and 22). Build tool sha256 0b485431…13edbf; base tool (round 40, 8eb121c8) sha256 4de35f8c…1460e. The frozen counter v1 {C1} (1434 generated cases labelled by the abnf 2.9.1 RFC 3986 grammar) was met by 15 of 141 wave-1 control receipts before the build, so kill rule (1) made C1 exploratory: its verdict will come from a non-author reviewer, not from the counter. Counter v2 {C2} is information for the next round only. Harm rule: the selftest passes every fixture at the build (198, with 15 new `r41_*`), and the round-39 real run is byte-equal (`jq -S . | sha256sum` = fd985a41867ed31b02ab03797562a1f01969aa3fc01c293eda145c2a7a4bc8a5; inputs retained in {W}/realrun/).

# Bounds
- You are a leaf: no subagents, no swarm, no verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git is fine. Never run jj at /home/vgpnk/Projects/shokunin. If you need a clone: `git clone -q {L} {SB}/<YourName>/clone` after unsetting GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE.
- Cap every run with `timeout` (≤900 s), ≤8 parallel processes, `prlimit --as=4000000000`; bound every file you write (≤200 MB per seat; never append in a loop to a file Python imports; never point a log at sitecustomize.py or a .pth); kill every process tree you start before returning. Never run `du` or `find` over /fast/scratch as a whole.
- Network: only URLs your item names, GET only. Never request the operator's properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json).
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: a one-line report saying so; do not rephrase. Message only agent://KakeR41 for blockers; never agent://all. Plain English.

# Result
Report under 60 lines: what you checked, exact commands with exit codes, findings with path:line and severity, and per checked statement: holds / overstated / wrong. An unrun check has not passed. Time box: 25 minutes; a partial report (first line `PARTIAL:`) beats none.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, W=W, C1=C1, C2=C2, CONTRACT=CONTRACT)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
RERUN = "The receipt path, passed, byField, byComponent, met, exit code; whether it matches the SCORECARD statement."

ITEMS = [
    item("RerunBuildV1Seeded", "reviewer", OP, "SCORECARD statement: the build scores 1434/1434 under counter v1 (`verification/build/c1-v1-at-eae5ae2c-41001.json`).",
         "- Run `timeout 900 python3 -B {C1} --root {L} --revision {REV} --seed 41001 --out {sb}/v1-41001.json` and compare with the committed receipt (passed, seed, toolSha256, counterSha256).", RERUN),
    item("RerunBuildV1Random", "reviewer", OP, "SCORECARD statement: the build meets counter v1 on any seed.",
         "- Run the counter v1 at {REV} three times without `--seed` (fresh random seeds), outputs in {sb}/.", RERUN),
    item("RerunBuildV2", "reviewer", OP, "SCORECARD statement: the build scores 1434 under counter v2 (information).",
         "- Run `timeout 900 python3 -B {C2} --root {L} --revision {REV} --out {sb}/v2-<n>.json` three times (random seeds).", RERUN),
    item("RerunBase", "reviewer", OP, "SCORECARD statement: the base 8eb121c8 does not meet (1028–1078 measured).",
         "- Run counter v1 and v2 at revision 8eb121c8, two random seeds each.", RERUN),
    item("RerunOracleCrosscheck", "reviewer", OP, "SCORECARD statement: the second oracle (rfc3987 1.3.8) agrees with the abnf oracle on every generated case (14,340 for v1 and v2).",
         "- Run `python3 -B {W}/oracle_crosscheck.py --seeds <10 new seeds> --out {sb}/x1.json` and the same with `--counter {C2}`; read the script and say whether its `fullmatch` and loc-strip handling are right.", "Totals and any disagreement values; findings with path:line."),
    item("RerunW1TallyV1", "reviewer", OP, "SCORECARD statement: 15 of 141 wave-1 receipts meet counter v1, all from live seats.",
         "- Count `jq -s 'map(select(.met))|length' {W}/verification/w1/*.json` and list the meeting labels; re-score five meeting and five non-meeting tools from {W}/controls/w1/ with {C1} (`--tool-file`) and compare; check {W}/w1-dispatch-log.txt for dead or refused seats.", "Counts, labels, re-score table, and whether any receipt belongs to a dead or refused seat."),
    item("RerunW1TallyV2", "reviewer", OP, "SCORECARD statement: under counter v2, 10 of 141 meet, and `terminal_pct`, `v1_shape`, `strip`, `delimiter_proxy`, `m07_query_hash` fail.",
         "- Count {W}/verification/w1v2/*.json; re-score those five tools from {W}/controls/w1/ with {C2} on two fresh seeds each.", "Counts and the re-score table."),
    item("ReviewBuildDiffFresh", "reviewer", OP, "The final build: `git -C {L} diff 8eb121c8 {REV} -- scripts/sitemap_audit.py` (fresh non-author review of the final bytes, sha256 0b485431…).",
         "- Check `_URI_RE` against RFC 3986 Appendix A (https://www.rfc-editor.org/rfc/rfc3986.txt) class by class; check that every caller of `_parse_url` keeps its behaviour for values the base accepted and RFC 3986 also accepts; name the sha256 of the bytes you reviewed.", "Findings with path:line and severity; the reviewed sha256."),
    item("ReviewBuildOutOfClass", "reviewer", OP, "The build's out-of-class statements in the SCORECARD kill-rule section and SKILL.md \"round-41 URL rule\": non-ASCII unchanged, IP-literal contents and ports above 65535 judged by urlsplit as before.",
         "- Write ≥20 out-of-class values (non-ASCII in each component, IPv6 with zone id, IPvFuture upper/lower `v`, port 65536, empty port, `http://h?`, `http://h#`, `http://h`) and run each through the base (`git show 8eb121c8:scripts/sitemap_audit.py`) and the build via small manifests.", "Table value → base / build / RFC 3986 (abnf oracle from {W}/oracle/); every difference listed."),
    item("ReviewBuildPerformance", "executor", OP, "Run time of the build's regular expression on long and adversarial values.",
         "- Time base and build on manifests with 2,047-character `loc` values built to stress backtracking (long runs of `%`, `@`, `:`, sub-delims, nested brackets), and on one file with 50,000 entries; cap each run at 120 s.", "Timing table base vs build; any super-linear case with the value shape."),
    item("ReviewBuildVsIndependent", "reviewer", OP, "Agreement of the build with the wave-1 independent build `/fast/scratch/hyaku/kake-r41w1/ExecIndependentBuild/indep.py` (read-only).",
         "- Generate ≥5,000 values (both counters' `generate` functions can be imported) plus your own edge cases; compare `_parse_url` of both tools and the abnf oracle.", "Disagreement counts by kind with example values."),
    item("MutSelftestRepertoire", "mutation-tester", OP, "The 15 new `r41_*` fixtures in `{L}/scripts/sitemap_audit_selftest.py`. Measures: whether they kill repertoire mutants of the build.",
         "- Copy the build to {sb}/; write ≥10 single-change mutants of `_URI_RE` character classes (drop or add one character in one component); run the selftest on each.", "Per mutant: change, selftest PASS line; survivors first."),
    item("MutSelftestStructure", "mutation-tester", OP, "The same fixtures. Measures: whether they kill structural mutants of the build.",
         "- ≥8 structural mutants (pct one hex, no end anchor, `+` to `*` on reg-name, userinfo allowing `@`, query allowing `#`, check applied after `.strip()`, check skipped for `sitemapUrl`, check skipped for `loc`); run the selftest on each.", "Per mutant: change, selftest PASS line; survivors first."),
    item("MutCriteriaLiveTally", "mutation-tester", OP, "The criteria check `{W}/criteria/live_tally_check.py` (QUALITY (s) draft): red on round 40, green on round 41.",
         "- Run it on round 40 (`--dispatch-log {L}/.ufo/waves/round-40/w1-dispatch-log.txt {L}/.ufo/waves/round-40/resid-dispatch-log.txt --receipts {L}/.ufo/waves/round-40/verification/w1`) and round 41 (`--dispatch-log {W}/w1-dispatch-log.txt --receipts {W}/verification/w1`); write ≥5 mutants of the checker and fixtures of your own (a dead seat named with/without suffix) in {sb}/.", "Exit codes on both rounds; mutants and whether your fixtures catch them."),
    item("MutCriteriaFreshReview", "mutation-tester", OP, "The criteria check `{W}/criteria/fresh_review_check.py` (QUALITY (t) draft): red on round 40's final tool 4de35f8c…, and what it says for round 41.",
         "- Run it on round 40 (`--tool-sha 4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e --reports {L}/.ufo/waves/round-40/w1 {L}/.ufo/waves/round-40/resid`); write ≥5 mutants and your own fixture directories in {sb}/; say whether a report that merely quotes a sha would pass it (weakness).", "Exit codes, mutants, weaknesses with severity."),
    item("ReviewHarmSelftest", "reviewer", OP, "Harm rule half 1: the selftest at the build passes 198/198; the base gives 188/198 with only `r41_*` red.",
         "- Run `python3 -B {L}/scripts/sitemap_audit_selftest.py --tool <tool>` for the build and for `git show 8eb121c8:scripts/sitemap_audit.py`; check `git diff 8eb121c8 {REV} -- scripts/sitemap_audit_selftest.py` removes no line.", "PASS lines, FAIL ids, diff line counts."),
    item("ReviewHarmRealRun", "reviewer", OP, "Harm rule half 2: the round-39 real run is byte-equal at the build.",
         "- In a copy of {W}/realrun/ in {sb}: `sha256sum -c SHA256SUMS`; run base and build with `--manifest manifest.json`; `jq -S . | sha256sum` both.", "Digests, exits; equal / differs."),
    item("ReviewHarmScope", "reviewer", OP, "No other lane surface changed by the round: `git -C {L} diff --stat 8eb121c8 {REV}` and `git -C {L} diff --diff-filter=DR --name-only 8eb121c8 {REV}`.",
         "- Check that only `scripts/sitemap_audit.py`, its selftest, SKILL.md, SCORECARD.md, corpus/SOURCES.md and `.ufo/waves/round-41/` changed, with no deleted line in SCORECARD.md, SOURCES.md or LOG.md (`^-[^-]`); run the robots selftest `python3 -B {L}/scripts/robots_audit_selftest.py --tool {L}/scripts/robots_audit.py` if it exists.", "Lists and counts; holds / wrong."),
    item("ReopenS117Fresh", "scout", FR, "Row S117 in {L}/corpus/SOURCES.md.",
         "- GET https://www.rfc-editor.org/rfc/rfc3986.txt ; compare sha256 with the row; locate every anchor the row names (line numbers) and check each `teaches` clause.", "Per clause: holds / overstated / wrong with located text."),
    item("ReopenS118Fresh", "scout", FR, "Row S118 (abnf 2.9.1).",
         "- GET https://pypi.org/pypi/abnf/2.9.1/json ; check the quoted summary and README sentence verbatim, the wheel digest against `sha256sum {W}/oracle/abnf-2.9.1-py3-none-any.whl`, and that the wheel contains `abnf/grammars/rfc3986.py`.", "Per clause: holds / overstated / wrong."),
    item("ReopenS119Fresh", "scout", FR, "Row S119 (rfc3987 1.3.8).",
         "- GET https://pypi.org/pypi/rfc3987/1.3.8/json ; check the summary quote, the digest, and the claim 'written independently of abnf' (authors, dates, licences).", "Per clause: holds / overstated / wrong."),
    item("ReopenS102Quote", "scout", FR, "The S102 quote the round cites: \"Please check to make sure that your URLs follow the RFC-3986 standard for URIs, the RFC-3987 standard for IRIs, and the XML standard.\"",
         "- GET https://www.sitemaps.org/protocol.html ; locate the sentence in the stripped text; compare the page sha256 with row S102 in {L}/corpus/SOURCES.md.", "Located text; holds / wrong."),
    item("CriticKillRuleRecord", "critic", OP, "SCORECARD section \"Round 41 — kill rule (1) fired on counter v1\".",
         "- Read only. Was kill rule (1) applied as written at abf457d0 (SCORECARD \"Round 41 — C1 counter candidate\")? Is any classification in the table used to rescue the counter? Is anything changed after the control data? Are the wave-1 corrections appended rather than edits?", "Per statement: holds / overstated / wrong with line numbers."),
    item("CriticExploratoryBetter", "critic", OP, "Whether the build is better than the round-40 tool on the URL rule, as an exploratory claim would need.",
         "- Read only (receipts and reports may be read). Weigh `verification/build/`, `verification/pre/`, `w1/ExecIndependentBuild.md`, `w1/ReviewReferenceDiff.md`, the selftest diff; name what the prior state lacked and what could make the change worse.", "Better / not better / unclear, with reasons and pointers."),
    item("CriticClaimSizing", "critic", OP, "The round's claim record against /home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-41.md §6 item 9 and AXES.md (exploratory claims).",
         "- Read only. Axis named by surface? Universal clauses? One predicate in plan, code and receipts? Was the pre-freeze control wave run before any build data?", "Per rule: holds / overstated / wrong."),
    item("ReviewSourcesRows", "reviewer", FR, "Rows S117–S119 in {L}/corpus/SOURCES.md and the census.",
         "- Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (exit code); check each row's columns against the registry header and CORPUS.md §SOURCES (fleet root /home/vgpnk/Projects/shokunin/CORPUS.md); check that retained bytes in {W}/sources/ match the row sha256s.", "Census output and exit; per row: conformant / defect."),
    item("ReviewSkillAmendment", "reviewer", OP, "SKILL.md section \"Sitemap file audit — round-41 URL rule\".",
         "- Check every sentence against the build's behaviour (run small manifests) and the SCORECARD; flag any admission or conformance overclaim.", "Per sentence: holds / overstated / wrong."),
    item("ReviewR40Correction", "reviewer", OP, "Round-40 spot-check routed defect 1: the round-40 tally restated as 26 of 72 live-seat receipts (wave-1 report `w1/ReviewR40Restatement.md`).",
         "- Recount from `git -C {L} archive 8eb121c8 .ufo/waves/round-40/verification/w1`; check that the round-41 SCORECARD/LOG carry the restatement as appended text once the L1 lands it (read {L}/LOG.md tail).", "Counts; holds / missing / wrong."),
    item("ReviewReceiptOrder", "reviewer", OP, "Commit order: pre-freeze section abf457d0 → wave-1 receipts and kill-rule record 9e3c31d2 → build {REV}.",
         "- `git -C {L} log --format='%H %cI %s' 8eb121c8..{REV}`; check that every `verification/w1/*.json` was added at 9e3c31d2 or earlier and the build file first changed at {REV}; compare with `w1-dispatch-log.txt` times.", "Timeline table; holds / wrong."),
    item("ReviewCounterV2Code", "reviewer", OP, "Counter v2 {C2} (information for the next round).",
         "- Review the diff `diff {C1} {C2}`: boundary insertion, empty components, IP literals, loc strip, environment; look for judging errors and any new label leak.", "Findings with path:line and severity."),
    item("SentinelBuildInput", "sentinel", OP, "The build's handling of untrusted sitemap and manifest input (read-only review; harmless local runs allowed in {sb}).",
         "- Check `_URI_RE` and its callers for crash paths (exceptions on odd code points, surrogates, very long values) and anything that could make the tool read or write outside the manifest directory.", "Findings with path:line and severity."),
    item("ScoutSiblingUrlDefect", "scout", OP, "The wave-1 connector table `{W}/w1/ConnectorSiblingOverlap.md`.",
         "- Re-open each row's file:line; confirm or refute 'shares the defect' for each, read-only.", "Per row: confirmed / refuted with the located code."),
    item("ReviewLessonDraftCheck", "reviewer", OP, "The QUALITY drafts (s) live-tally and (t) fresh-review the round will add, and the scribe draft `{W}/w1/ScribeLessonDraft.md`.",
         "- Check each proposed fix can fail: run the two checks in {W}/criteria/ on round 40 (expect exit 1) and on round 41 (live tally: expect exit 0); say what (t) needs to go green on round 41.", "Exit codes and per-draft verdict."),
]

spec = {
    "wave": "kake-r41-w2",
    "milestone": "r41-falsify",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-41/w2",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w2-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
