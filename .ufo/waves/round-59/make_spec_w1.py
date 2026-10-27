#!/usr/bin/env python3
"""Generate the round-59 single v2 wave (build + attack items together). Output: w1-spec.json beside this file."""
import json
import os
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = f"{LANE}/.ufo/waves/round-59"
R = f"{W}/w1"
SRC = f"{W}/sources"
KNOW = f"{LANE}/corpus/knowledge"
STAGED = "/home/vgpnk/Projects/shokuknow/merge/kake"
FLEET = "/home/vgpnk/Projects/shokunin"
BASE = "fd6303ce5c14b3f892dec586297a942ab6e4193b"
FREEZE = "45a92b64ac8a0f82dba369100e30682f14de81fb"
SCR = "/fast/scratch/hyaku/kake-r59"
GODSPEED = ("/skill:godspeed\n"
            "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n3. **Keep moves that improve any axis and harm none.**\n"
            "4. **Don't aim — let the frontier walk itself.**\n"
            "IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in "
            "parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.\n\n")

CONTEXT = (
    "/skill:godspeed\n"
    "Round-59 kake wave w1 (one v2 wave: build + attack items together). Lane repo: /home/vgpnk/Projects/shokunin/kake-shokunin. Your tools start at the "
    "FLEET root (/home/vgpnk/Projects/shokunin), not the lane: FIRST `mkdir -p /fast/scratch/hyaku/kake-r59/<your seat name> && cd` there; use absolute paths "
    "for every read and write; never use a relative redirect (`> x.out`) outside your scratch dir. Every `Report:` trailer path is relative to "
    "/home/vgpnk/Projects/shokunin/kake-shokunin — write it at /home/vgpnk/Projects/shokunin/kake-shokunin/<that path> (i.e. "
    "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/w1/<Seat>.md), never under the fleet root. Seats never mutate the fleet repo, sibling lanes, "
    "lane jj state or the lane Git index: write ONLY your own report file (and, if your assignment says so, files inside "
    "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/w1/<Seat>.files/), no other path; no `git add/commit/stash/checkout/reset/pull/push` "
    "in the lane, no jj mutation. Read-only git (show, log, ls-tree, rev-parse, diff) is fine. Scratch: every clone, fixture and work dir lives under "
    "/fast/scratch/hyaku/kake-r59/<your seat name>/ (pass it as TMPDIR / --work; `/tmp` only for files under 50 MB); use `git clone -q --shared` "
    "rather than full clones; delete your scratch dir before you finish (copy receipts into your .files/ first; `trap 'rm -rf -- \"$S\"' EXIT`). Fixture "
    "repos: `D=$(mktemp -d -p /fast/scratch/hyaku/kake-r59/<seat>) && git -C \"$D\" init -q`, every later git call names `-C \"$D\"`, verify "
    "`git -C \"$D\" rev-parse --show-toplevel` equals `$D` before the first commit, commit only with `-c user.name=selftest -c user.email=selftest@local`; "
    "never commit anywhere else. Domain source trees and /home/vgpnk/Projects/shokuknow are read-only (read files; never run campaign tools there); sibling lane "
    "repos are read-only. Round facts: frozen contract /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/contract.md (+ contract.json), base "
    f"revision {BASE}, contract commit {FREEZE}, access date 2026-10-27 (UTC; the round opened 2026-10-26 -03:00). Claims: C1 calibration — the "
    "SCORECARD.md axis table's evidence cells match committed state (counter .ufo/waves/round-59/c59_axis_evidence.py, base 16 mismatches); C2 operability — "
    "scripts/id_resolver.py closes seven disclosed false-green/robustness routes K8-K14 (counter .ufo/waves/round-59/c59_resolver_cases.py, base 13/21); C3 "
    "freshness (sourced) — the stale sentence in corpus/knowledge/crawler-identity.md line 31 (\"A user-agent string is the only thing a server log records "
    "about the crawler.\") corrected append-only, plus two Google crawler-identity entries on NEW rows S425 "
    "(https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers, staged S398) and S426 "
    "(https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests) (counter .ufo/waves/round-59/c59_quote_truth.py, base 0/9). "
    "Retained bodies: .ufo/waves/round-59/sources/S425.html, S426.html (+ receipts.json). Quote rule: every quote 6..25 whitespace tokens and <= 160 "
    "characters, a substring of ONE whitespace-collapsed text node of the retained body's article block (`class=\"devsite-article-body` .. "
    "`<devsite-content-footer`), page-unique; check with `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/span_tools.py "
    "{spans|check|window} <S425|S426> [span]`; ASCII double quotes only. Counters are VERSION 1: wave 1 attacks them before any claim is measured; no seat "
    "scores an after-state. Never fabricate: an unrun check is reported as unrun; mark unverified statements [INFERENCE]. No credentials, tokens, op:// refs or "
    "private URLs in any report. Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read "
    "/home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason). Pacman guard: all pacman transactions are "
    "PAUSED host-wide — never run pacman (no -S, -Sy, -Syu, -U, -R); install via `uv tool`/`npx`/an official binary in ~/.local/bin or report the need; never "
    "restart a host service. The host is loaded: generous timeouts, no retry loops. Report format: first line `# <your seat name>`, then the sections your "
    "assignment names, factual, under ~150 lines; last line `VERDICT: <one line>`. The L1 (KakeR59) holds the planner seat and integrates; you are a leaf: no "
    "subagent dispatch except an executor's single read-only labrat probe."
)

items = []


def add(name, role, text):
    items.append({"name": name, "role": role, "prompt": GODSPEED + text.replace("{W}", W).replace("{R}", R).replace("{LANE}", LANE)
                  .replace("{SRC}", SRC).replace("{KNOW}", KNOW).replace("{STAGED}", STAGED).replace("{FLEET}", FLEET)
                  .replace("{BASE}", BASE).replace("{SCR}", SCR).replace("{FREEZE}", FREEZE)})


# ---- C1 calibration --------------------------------------------------------------------------------
C1_CELL = (
    "Read {LANE}/SCORECARD.md lines 1-25 (the axis table) and every `## Round N` section that names the axis in a table row (rounds 50-58 at least), "
    "{LANE}/AXES.md is at {FLEET}/AXES.md (calibration = SCORECARD entries match observed repo state), and the C1 counter {W}/c59_axis_evidence.py "
    "(docstring: pointer/receipt/tally rules). Draft a REPLACEMENT evidence cell (the third cell only; the score cell stays as it is) that: names only "
    "repo-relative committed paths in backticks (check each with `git -C {LANE} cat-file -e {BASE}:<path>`); cites >= 2 committed receipts under "
    "`.ufo/waves/round-N/` of rounds whose SCORECARD `## Round N` section has a table row naming this axis; states each number as `A/B` only where that exact "
    "string occurs in a cited receipt (grep it); contains no `|` character; says plainly what the score rests on and what is legacy (the 10 is a legacy "
    "round-12/17 rating — do not inflate). Then run the counter's logic on your cell in a scratch copy: clone `git clone -q --shared {LANE} <scratch>/c`, "
    "replace the row's third cell with yours AND append the old cell verbatim under a `## Superseded axis-table evidence` heading at EOF, commit (selftest "
    "identity) and run `python3 -B {W}/c59_axis_evidence.py --root <scratch>/c --revision HEAD --json` (the other two rows stay red; report this row's "
    "detail). Report sections: `CELL:` (exact text in one fenced block), `POINTERS:` (path, exists), `TALLIES:` (tally, file, grep line), `COUNTER ROW DETAIL:`, "
    "`HONESTY NOTES:` (what the cell does not claim). Also write the cell to {R}/<Seat>.files/cell.txt.")
add("ScribeC1CellOperability", "scribe", "Claim C1, operability row (score 10, last change round 12). " + C1_CELL)
add("ScribeC1CellFreshness", "scribe", "Claim C1, freshness row (score 10, last change 17). " + C1_CELL)
add("ScribeC1CellCalibration", "scribe", "Claim C1, calibration row (score 2, last change 58; the round-58 receipt-rewrite ledger move; cite "
    "`.ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt` and other round-54..58 calibration receipts). " + C1_CELL)
add("ScribeC1Superseded", "scribe",
    "Claim C1: draft the append-only `## Superseded axis-table evidence (round 59)` section for {LANE}/SCORECARD.md: a dated preamble (why the cells were "
    "replaced: base counter `.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` — 16 mismatches, list them), then each of the three base evidence "
    "cells VERBATIM (copy the exact bytes of the third cell of lines 17, 18, 19 at {BASE}: `git -C {LANE} show {BASE}:SCORECARD.md | sed -n 17,19p`; the "
    "counter checks `bc[2] in outside` — byte-exact), each under its axis name, as an indented or quoted block that does NOT start with `|` (so it is not a "
    "table row). Verify byte-exactness with a python check in scratch and paste it. Report sections: `SECTION:` (one fenced block), `BYTE CHECK:`, "
    "`DEAD POINTERS:` (each unresolved pointer with why). Also write it to {R}/ScribeC1Superseded.files/section.md.")
add("ExecC1Selftest", "executor",
    "Claim C1: write the gate selftest for {W}/c59_axis_evidence.py (version 1 has a stub). Copy the counter to {R}/ExecC1Selftest.files/c59_axis_evidence.py "
    "and replace `selftest()` with a fixture kill matrix: each case builds a scratch git repo (rules in context) holding a SCORECARD.md (axis table + "
    "`## Round N` sections) and receipt files, commits a base and a measured revision, runs `measure()` and asserts the expected counts/met. Cases (>= 24): "
    "the real base shape (16 mismatches); a clean minimal-true table (met); emptied cells; /tmp, ~ and absolute pointers; a bare name not at root; a "
    "`file:LINE` beyond EOF; `:LINE` continuation after an unresolved file; brace expansion; a tree pointer (resolves, not a receipt); an off-axis receipt "
    "(round section without the axis); a tally absent from every cited blob; a tally present only in an uncited file; a score change on operability; a "
    "removed calibration row; reordered rows; superseded cell missing / altered by one byte / kept only inside the table; a `|` inside a code span; a "
    "duplicated header (first table wins); CRLF line endings; a symlinked receipt (decide: blob type is `blob` for symlinks in git — report what happens). "
    "Every case must FAIL on a mutant it targets (state which). Run it; paste the tally. Report sections: `CASES:` (name, expectation, result), `TALLY:`, "
    "`COUNTER DEFECTS FOUND:` (with proposed fixes), `DIFF:` (unified diff vs the frozen counter).")
add("CriticC1Cheat", "critic",
    "Attack C1's version-1 counter {W}/c59_axis_evidence.py: reach `met=True` in a scratch clone (rules in context) WITHOUT the cells truly matching committed "
    "state — e.g. a cell citing an on-axis receipt plus a tally that occurs in it by coincidence (`1/1`, a date fragment), an on_axis() hit from an unrelated "
    "table line that merely contains the axis word, pointers hidden from the regex (paths with spaces, unicode slashes, HTML `<code>` instead of backticks), "
    "dead paths written without backticks, the superseded check satisfied by a copy inside a code comment of an unrelated section, `scores_held` with a "
    "changed score written as `10 ` or `10.0`. For each: the cheat, the counter output, whether it is a true defect or a stated limit. Report sections: "
    "`CHEATS:`, `HOLES (fix proposals):`, `VERDICT:`.")
add("CriticC1Parse", "critic",
    "Attack the parsing of {W}/c59_axis_evidence.py: escaped pipes `\\|` in cells, code spans holding `|`, a header variant (`| Axis | Score | Evidence | Last "
    "change |`), a second axis table, leading spaces, trailing spaces after `|`, an HTML comment around a row, a row split across lines, a table moved below "
    "the round sections. Build each in a scratch clone and run the counter (rules in context). Classify: false green / false red / correct. Report sections: "
    "`CASES:`, `FALSE GREENS:`, `FIXES:`, `VERDICT:`.")
add("ExecC1BaseAudit", "executor",
    "Claim C1 base re-derivation WITHOUT importing the counter: from `git -C {LANE} show {BASE}:SCORECARD.md` lines 15-19, list every path-like token in each "
    "evidence cell by hand (and with your own regex), check each with `git cat-file -e {BASE}:<path>` / host existence (`ls`), list each `A/B` tally and grep "
    "the cited files for it. Compare with {W}/controls/base-c1-axis-evidence.txt (16 mismatches: 11 unresolved, 3 rows without receipt, 2 rows without a found "
    "tally). Note every disagreement (e.g. `corpus/claims` is described as dangling in prose; is counting it fair?). Report sections: `TOKENS:`, "
    "`TALLIES:`, `AGREEMENT:`, `DISAGREEMENTS:`.")
add("LabratC1Controls", "executor",
    "Hypothesis: the C1 v1 counter rejects the cheapest controls that skip the claimed work. In a scratch clone at {FREEZE} (rules in context) build and "
    "score, each as its own commit: (a) do-nothing; (b) three emptied evidence cells; (c) cells replaced by one random existing lane file path each (not a "
    "receipt); (d) cells citing an on-axis receipt but a fabricated tally `99/99`; (e) a correct-looking cell citing a receipt from a round with no claim on "
    "the axis; (f) the minimal-true control: each cell = one on-axis receipt + one tally from it, old cells appended verbatim at EOF. Record each run "
    "(`--json`). (f) is expected to MEET (it is the claimed work, minimal); say whether that is a counter hole or the claim's stated limit. Copy receipts to "
    "{R}/LabratC1Controls.files/. Report sections: `CONTROLS:` (control, counts, met), `READING:`, `VERDICT:`.")
add("ReviewerC1Contract", "reviewer",
    "Review claim C1 in {W}/contract.md against {FLEET}/AXES.md (calibration definition), {FLEET}/MISSION.md and the prompt rule 'A calibration claim must "
    "count mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state'. Questions: is the predicate the same sentence in "
    "contract.md, contract.json and the counter's PREDICATE; do the atoms measure self-assessment vs observed state; is the do-nothing control red for the "
    "right reason; what would make the after-state a calibration HARM (e.g. a cell that understates/overstates); is `superseded_kept` the right append-only "
    "guard. Report sections: `FINDINGS:` (severity, issue, fix), `VERDICT:`.")
add("ScoutC1Table", "scout",
    "Read-only: other calibration mismatches in {LANE}/SCORECARD.md beyond the evidence cells — `Last change` column vs the latest round that moved each "
    "score; the capabilities table rows (do their evidence commands still run? sample 4 with `--help`/selftest at {BASE} in a scratch clone); SHONEN.md "
    "boxes vs the round-58 report's SHONEN lines. Report only (not targets this round). Report sections: `LAST-CHANGE:`, `CAPABILITY ROWS:`, `SHONEN:`.")

# ---- C2 operability ---------------------------------------------------------------------------------
C2_FIX = (
    "Write a candidate {R}/<Seat>.files/id_resolver.py from {LANE}/scripts/id_resolver.py that closes K8-K14 of {W}/c59_resolver_cases.py (read its docstring "
    "and case code; the disclosed findings are in {LANE}/.ufo/waves/round-58/w1/ReviewerResolverOther.md, w1/SentinelCounters.md F2/F5/F6, "
    "r1/ReviewerResolverDiff.md F1): HTML-block comments (CommonMark HTML block type 2: `<!--` .. `-->`, may span lines) hide rows; a setext H1/H2 "
    "underline after a paragraph line ends the Registry section (like ATX H1/H2); in-lane symlinked knowledge directories are followed with cycle "
    "protection (out-of-lane ones stay refused); at `--revision`, read `ls-tree -r -z` WITH modes, resolve a 120000 entry's target inside the tree (in-lane "
    "only, else skip) and never parse a link target string as a body; the worktree registry is realpath-contained (outside the lane -> exit 2); non-UTF-8 "
    "names decode with surrogateescape (os.fsdecode) and render with a visible escape; `--root` must be its repository's toplevel (else exit 2). Add >= 7 "
    "selftest cases (one per route; tally must reach >= 66) and keep every existing case. Keep the round-57 G2 rule: the source must not name "
    "`c57_idresolver_gate`, `.ufo/` or `reference(`. Score it: shared clone of the lane at {FREEZE} under your scratch, copy the candidate to "
    "scripts/id_resolver.py, commit (selftest identity), run `python3 -B {W}/c59_resolver_cases.py --root <clone> --revision HEAD --work <scratch>/w --seed "
    "<N>` for 3 seeds, and run the tool's own `--selftest`; also `--revision <your commit>` on the real lane clone must stay `dangling=0` with ids_cited "
    "unchanged from the base (108). Report sections: `DIFF:` (unified), `GATE RUNS:`, `SELFTEST:`, `REAL LANE:`, `DESIGN NOTES:`.")
add("ExecResolverFix", "executor", "Claim C2, primary implementation. " + C2_FIX)
add("ExecResolverFix2", "executor", "Claim C2, second independent implementation (for differential comparison with another seat's candidate; do not "
    "coordinate). " + C2_FIX)
add("ExecC2GateSelftest", "executor",
    "Claim C2: port the round-58 gate selftest (seven scored control tools; `git -C {LANE} show {FREEZE}:.ufo/waves/round-58/c58_resolver_cases.py`, "
    "functions `_stub`, `_base_tool`, `_fixture_lane`, `_control`, `selftest`) to {W}/c59_resolver_cases.py (21 cases; version 1 has a stub). Copy the "
    "counter to {R}/ExecC2GateSelftest.files/c59_resolver_cases.py, port the controls with corrected expected scores for 21 cases (constant green, always "
    "exit 1, fence-drop, blanket dangling, tally liar, the base tool at {BASE} = 13/21, and a K8-K14 partial fix), add controls that pass K8-K14 by sniffing "
    "(e.g. a tool that exits 2 whenever any symlink exists, one that drops every line after any `---`) and assert they fail some case. Run the selftest; "
    "paste the tally. Report sections: `CONTROLS:` (control, expected, observed), `TALLY:`, `DIFF:`, `GATE DEFECTS:`.")
add("CriticC2Cheat", "critic",
    "Attack {W}/c59_resolver_cases.py version 1: write minimal WRONG tools that score 21/21 or close (case-sniffing: detect `<!--` lines and drop the next "
    "row only; treat every `---` as section end; exit 2 when SOURCES.md is a symlink regardless of target; follow every dir symlink including out-of-lane "
    "ones; print a fake selftest tally; read the gate's own expectations). Score each in a shared clone at {FREEZE} (commit the stub as "
    "scripts/id_resolver.py, selftest identity; --work in your scratch; >= 3 seeds). Report sections: `CHEATS:` (stub, tallies per seed), `HOLES:` (with a "
    "proposed case per hole), `VERDICT:`.")
add("CriticC2Semantics", "critic",
    "Attack the CONTRACT of K8-K14 in {W}/c59_resolver_cases.py: is each expectation the right behaviour for a source-id resolver whose job is 'list every "
    "cited id the lane registry lacks'? K8 (a commented-out row is not registered), K9 (setext H2 ends the section; what about a thematic break `---` after a "
    "blank line, or a table delimiter row?), K10 (follow in-lane dir symlinks: cycles, double counting), K11 (resolve committed symlinks in the tree vs skip "
    "them; worktree parity), K12 (exit 2 vs exit 1 for an out-of-lane registry), K13 (rendering of undecodable names), K14 (non-toplevel root = 2). For each: "
    "agree / disagree with argument and a markdown-spec or code reference. Report sections: `CASES:`, `CONTRACT RISKS:`, `VERDICT:`.")
add("ProbeCommonMark", "executor",
    "Hypothesis: the K8 and K9 fixture shapes of {W}/c59_resolver_cases.py render as the counter assumes. Install a CommonMark/GFM renderer without pacman "
    "(e.g. `uv tool install markdown-it-py` or `npx -y commonmark`/`npx -y marked`; read /home/vgpnk/.omp/agent/RULES.md first; record tool/version) and "
    "render: (a) a GFM table with a `<!--` / row / `-->` block after it; (b) a table, blank line, `Subsection` + `---`, blank line, a pipe row; (c) the same "
    "with `---` after a blank line (thematic break); (d) a row immediately after the table without a blank line. Report whether the commented row is "
    "invisible, whether (b) yields an <h2>, and what (d) does. Report sections: `TOOL:`, `RENDERS:` (input, output html), `READING:`, `VERDICT:`.")
add("MutC2Gate", "mutation-tester",
    "Mutation-test {W}/c59_resolver_cases.py by mutating the TOOL it scores: in a shared clone at {FREEZE} under your scratch apply >= 14 single-point "
    "mutants to scripts/id_resolver.py (ID_RE, ROW_RE indent, fence machine, section end, sibling owner sort, `--fleet` check, exit code on dangling, "
    "url-match, ls-tree -z parse, os.walk followlinks, realpath containment, selftest tally print), commit each (selftest identity) and run the gate; report "
    "which mutants the 21 cases kill (tally below the base 13/21 or changed) and which survive. Report sections: `MUTANTS:`, `SURVIVORS:`, `PROPOSED CASES:`.")
add("MutResolverSelftest", "mutation-tester",
    "Mutation-test the CURRENT tool's own selftest ({LANE}/scripts/id_resolver.py --selftest, 59 checks): copy to your scratch, >= 14 mutants on "
    "parse_registry, the fence machine, knowledge walk, revision path parse, sibling registry, evaluate, render; run the copy's --selftest per mutant. "
    "Survivors show where the selftest is blind; the C2 fix should add cases there. Report sections: `MUTANTS:`, `SURVIVORS:`, `CASES TO ADD:`.")
add("SentinelResolver", "sentinel",
    "Security review of the symlink and path handling the C2 fix must add to {LANE}/scripts/id_resolver.py (read the current code and the K10/K11/K12 "
    "cases): link cycles (DoS), a committed symlink chain inside the tree, `..` escapes in link targets, absolute link targets, a symlinked `corpus/` or "
    "`corpus/knowledge` itself, a registry symlink to a sibling lane, TOCTOU between realpath and open. Build fixtures in scratch (rules in context) and run "
    "the CURRENT tool on each to record base behaviour. Report sections: `VECTORS:` (fixture, base behaviour, required behaviour), `MUST-HAVES FOR THE FIX:`, "
    "`VERDICT:`.")
add("ExecResolverRealLane", "executor",
    "Claim C2 no-harm baseline: run the CURRENT tool `--revision <rev>` for the last 10 first-parent revisions of master (`git -C {LANE} rev-list "
    "--first-parent -10 master`) with `--fleet {FLEET}` and with an empty fleet dir, recording each summary; count symlinks (`git ls-tree -r master | grep "
    "-c ^120000`), HTML comments and setext underlines inside `## Registry` of corpus/SOURCES.md, non-UTF-8 names. These are the values a correct fix must "
    "reproduce on this lane. Report sections: `RUNS:`, `LANE FACTS:`, `EXPECTATION FOR THE FIX:`.")
add("ExecC2SeedSweep", "executor",
    "Claim C2 gate determinism: run `python3 -B {W}/c59_resolver_cases.py --root {LANE} --revision {BASE} --work {SCR}/ExecC2SeedSweep/w --seed <s>` for "
    "seeds 1, 2, 59, 1000, 424242 and once without a seed; record per-case PASS/FAIL (must be identical: 13/21), timings, leftover scratch dirs (the counter "
    "must remove its work dir), and behaviour under `GIT_DIR=/nonexistent` and `TMPDIR` unset. Report sections: `RUNS:`, `DETERMINISM:`, `HYGIENE:`.")
add("ReviewerC2Counter", "reviewer",
    "Code-review the derived C2 counter: `diff <(git -C {LANE} show {FREEZE}:.ufo/waves/round-58/c58_resolver_cases.py) {W}/c59_resolver_cases.py` and "
    "{W}/derive_c59_resolver_cases.py. Check: K13's bytes path is really non-UTF-8 in the committed tree; K14's ancestor really holds a green lane at its "
    "root so the base tool's exit 0 is the false green; K11's dangling link is committed as mode 120000; K12's outside registry is outside the fleet dir; "
    "the toplevel check in main(); the forbid/want regexes (e.g. `dangling=0\\b`); that a correct fix can pass all 21 (no contradiction between cases). "
    "Report sections: `FINDINGS:` (severity, line, fix), `VERDICT:`.")
add("CriticC2P6", "critic",
    "P6 of the C2 gate trusts a printed `selftest: N/N` (round-58 disclosed limit: a zero-test stub can print it). Design a P6 that a hollow tally cannot "
    "pass (e.g. the tool prints one `PASS <case-name>` line per case and the gate checks the names against `def case_*`/registered functions in the "
    "committed source and that a mutated copy goes red), then attack your own design. Prototype both in scratch against the base tool. Report sections: "
    "`DESIGN:`, `PROTOTYPE RUN:`, `SELF-ATTACK:`, `RECOMMENDATION:` (adopt for version 2 or carry as a limit).")
add("RevengerResolverIntent", "revenger",
    "Reverse-engineer the original intent of scripts/id_resolver.py from its round-57/58 history (`git -C {LANE} log --format='%h %s' -- "
    "scripts/id_resolver.py`, {LANE}/.ufo/waves/round-57/contract.md C2, round-58 contract C2, SKILL.md rows): what did it promise about worktree vs "
    "`--revision` parity, symlinks and markdown semantics? Judge whether K10/K11/K12/K14 expectations follow that intent or change it. Report sections: "
    "`INTENT:` (with file:line), `CASE ALIGNMENT:`, `VERDICT:`.")
add("ExecResolverOtherRoutes", "executor",
    "Hunt further false-green routes in the CURRENT tool beyond K1-K14 (reported limits, not targets this round): CRLF registry, tab-indented rows, a row "
    "inside an HTML `<pre>`/`<details>` block, a link reference definition, a list item holding a pipe row, a registry heading with trailing `#`s, Unicode "
    "lookalike `S`, ids inside URLs in knowledge files. Each as a scratch fixture (rules in context) with the expected-correct outcome. Report sections: "
    "`CASES:` (input, result, class), `TOP RISKS:`.")
add("ScribeC2SkillRows", "scribe",
    "Draft SKILL.md and SCORECARD capability-row text for C2 and the round-59 counters. Read {LANE}/SKILL.md gate registry rows for round 57/58 "
    "(`grep -n 'c58_\\|c57_\\|id_resolver' {LANE}/SKILL.md`) and the SCORECARD `Source-id resolver` capability row. Draft: three gate rows for "
    "c59_axis_evidence.py, c59_resolver_cases.py, c59_quote_truth.py (command, what it proves, selftest command, tally as `<N>/<N>` for the L1 to fill "
    "after the final run), an id_resolver row update naming the K8-K14 behaviours, and which round-58 rows become `historical` because their frozen inputs "
    "change this round (e.g. c58_quote_truth mirror pin = 162 rows; c58_resolver_cases P6 floor 55 still satisfied?). Report sections: `ROWS:`, "
    "`HISTORICAL:`, `CAPABILITY ROW:`.")

# ---- C3 freshness (sourced) -------------------------------------------------------------------------
C3_SHAPE = (
    "Required entry shape (house style: {KNOW}/baidu-spider-identification.md and {KNOW}/crawler-identity.md): line 1 `source: <id> — <url> — § <heading as "
    "printed> (Last updated <date printed on the page> UTC) — fetched 2026-10-27`, line 2 `verified-at: 2026-10-27`, line 3 `recheck: 180d — curl -fsSL "
    "--compressed '<url>' | grep -F -c '<short raw span>'` -> <count> (run the grep against the RETAINED body and report the count; pick a span that does "
    "not cross a source line break), line 4 `ground: <one line>`; blank line; H1; prose citing `[<id>]` below the header. Verbatim passages in `> \"...\"` "
    "lines (ASCII quotes), each a page-unique article-block span (span_tools `check` must say in_text_node True, unique True, within_ceilings True); at "
    "least 3 such spans, one containing the row's subject (S425: `IP address`; S426: `reverse DNS`). Anything the page does not state is [INFERENCE]. End "
    "with `Scope note:` (a claim about what the operator's page states; no crawl observed, no Google behaviour measured). Cross-link by plain path only to "
    "lane entries that exist (`ls {KNOW}`), e.g. crawler-identity.md, baidu-spider-identification.md; never cite an S-id the lane registry lacks (S425/S426 "
    "are being added this round). Also give `GATE LINE:` exactly `- <id> — <url> — accessed 2026-10-27 — § <heading> (Last updated <date> UTC) — quote: "
    "\"<6-25-token page-unique span carrying the subject>\" (<n> units; substring of one collapsed text node of the retained body, sha256 <from "
    "sources/receipts.json>, <bytes> bytes, HTTP 200)`, `REGISTRY ROW:` the 11-cell line (shape of the S423 row in {LANE}/corpus/SOURCES.md; cell 2 "
    "`Google for Developers — <title as printed in <title> before the first ` | `> — <url>`; kind docs; tier A; status mined; opened 2026-10-27; recheck "
    "180d; used-by as the contract's C4 states; anchor `§ <an h2/h3 heading of the article block> (Last updated <date> UTC)`; no `|` inside a cell), "
    "`SPAN CHECKS:` (span_tools output per quote), `OMITTED:` (page content not carried, with reason). Put the complete entry in ONE fenced block under "
    "`ENTRY:` and also write it to {R}/<Seat>.files/<entry file name>.")
add("EntrySignals", "scribe",
    "Claim C3. Draft `corpus/knowledge/crawler-identity-signals.md` for NEW row S425 (overview page, `Google Crawler (User Agent) Overview`, printed "
    "`Last updated 2026-06-12 UTC`). Read `python3 -B {W}/span_tools.py window S425` fully. Carry: the three identification signals (user-agent request "
    "header, source IP address, reverse DNS hostname of the source IP), that crawlers run from many machines/datacenters so logs may show several IP "
    "addresses, US egress and the fallback when US requests are blocked (if the page says so), and the pointer to the verification page. The staged "
    "candidate {STAGED}/knowledge/corpus/knowledge/crawler-identity-three-signals.md is reference ONLY (its quotes/dates prove nothing; it asserts that "
    "user-agent is 'the signal anyone can set', cross-operator claims about Baidu/Yahoo, and AdsBot ignoring `*`): keep only what S425's article block "
    "states; anything from another page needs its own row (the lane holds Baidu as S423 — cross-link the file, quote nothing from it). Do not reuse the "
    "staged file name. Row anchor: `§ Verify Google's crawlers and fetchers (Last updated 2026-06-12 UTC)` if that heading is in the block. used-by of S425 "
    "= this entry AND corpus/knowledge/crawler-identity.md (the correction tail cites it). " + C3_SHAPE)
add("EntryVerification", "scribe",
    "Claim C3. Draft `corpus/knowledge/googlebot-verification.md` for NEW row S426 (`Verify Requests from Google Crawlers and Fetchers`, printed "
    "`Last updated 2026-03-20 UTC`). Read `python3 -B {W}/span_tools.py window S426` fully. Carry: the two methods (manual command line, automatic IP-list "
    "match), the two-step procedure (reverse DNS on the accessing IP with `host`, domain must be googlebot.com / google.com / googleusercontent.com, then "
    "forward DNS on that name must return the original IP), the worked examples exactly as printed, the crawler-category table (common / special-case / "
    "user-triggered: their reverse-DNS masks and JSON range files) as far as the block prints it. Do not state what the page does not (e.g. no claim that "
    "user-agents are forged unless the page says so — check the opening paragraph). used-by of S426 = this entry only. Row anchor: an h2/h3 of the block "
    "(e.g. `§ Use command line tools (Last updated 2026-03-20 UTC)`). " + C3_SHAPE)
add("ScribeCorrectionTail", "scribe",
    "Claim C3 condition C9. Draft the append-only correction for {KNOW}/crawler-identity.md: the stale bullet is lines 31-34 (`- **A user-agent string is the "
    "only thing a server log records about the crawler.** Two` ...). The correction must be INSERTED lines only (no base line changed or deleted), placed "
    "directly after line 34 (within 8 base lines of line 31), and carry the house tag in the form `**[r59-correction 2026-10-27]**` (precedent: "
    "`grep -rn 'r54-correction' {KNOW}`), cite `[S425]`, and quote at least one S425 span carrying `IP address` that passes `python3 -B {W}/span_tools.py "
    "check S425 '<span>'` (e.g. the logs-may-show-several-IP-addresses sentence, and the three signals). Say exactly what was wrong: a server log records the "
    "requesting IP as well as the user-agent, and Google identifies its crawlers by user-agent, source IP and reverse DNS; the bullet's point about the "
    "Smartphone/Desktop subtype stays true; point to googlebot-verification.md. Also list every OTHER place in the lane that repeats the UA-only claim (`grep "
    "-rniE 'only thing a (server )?log|user-agent string is the only' {LANE}/corpus {LANE}/SKILL.md {LANE}/README.md`). Report sections: `INSERT AFTER LINE "
    "34:` (exact lines in one fenced block), `SPAN CHECKS:`, `DIFF CHECK:` (apply it in scratch and run `python3 -c` difflib to show only inserts), "
    "`OTHER OCCURRENCES:`. Write the lines also to {R}/ScribeCorrectionTail.files/insert.md.")
add("ScribeRegistryGate", "scribe",
    "Claim C3 / frontier step. Draft the two registry rows (S425, S426) and the round-59 lesson `## Gate` block independently of the entry scribes. Read "
    "{FLEET}/CORPUS.md section `SOURCES.md — where a shokunin learns` (row schema, 11 columns, status vocabulary, recheck forms), {LANE}/corpus/SOURCES.md "
    "(rows S423, S424 as the model), {LANE}/corpus/lessons/round-58.md `## Gate` and `## Assimilation` (the model), {W}/assimilation/ (reg-ids, staged-ids, "
    "collisions, quarantine-slice), {W}/sources/receipts.json, and staged row S398 in {STAGED}/SOURCES.append.md. Produce: `ROWS:` both 11-cell rows (as "
    "the entry shape in this wave: anchor `§ <h2/h3> (Last updated <date> UTC)`, status mined, opened 2026-10-27, recheck 180d, used-by S425 = "
    "corpus/knowledge/crawler-identity-signals.md, corpus/knowledge/crawler-identity.md; S426 = corpus/knowledge/googlebot-verification.md); `GATE:` one line "
    "per new row in the exact form `- <id> — <url> — accessed 2026-10-27 — <anchor cell> — quote: \"<span>\" (<n> units; substring of one collapsed text "
    "node of the retained body, sha256 <sha>, <bytes> bytes, HTTP 200)` (check each quote with span_tools), then the assimilation decisions: ADMIT theme "
    "`crawler identity verification signals` — staged S398 re-grounded as S425 (renumber by document; list which staged sentences are refused and why), "
    "S426 lane-found (cite the S425 href to it: grep the retained body); `ASSIMILATION:` id list counts, collision list, renumber map, quarantine statement "
    "(12 rows, held: the round-58 L0 question is unanswered); `REGISTRY CHANGES:` old->new lines. Write the block also to {R}/ScribeRegistryGate.files/gate.md.")
add("ScribeGroundMap", "scribe",
    "Claim C3 support. Read {LANE}/corpus/README.md (`## Coverage map` and `### Frontier ground map`), {LANE}/PROVINCE.md (crawler identity ground), "
    "`ls {KNOW}`. Draft exact old/new edits: (a) one coverage-map row per new entry (3-cell shape of existing rows; no `|` in cells); (b) the frontier ground "
    "map `Crawler identity` ground extended with the round-59 Google verification row; (c) whether PROVINCE.md needs a line change (quote the line). The "
    "round-55 counter `.ufo/waves/round-55/c55_readme_index.py` treats a pointer to a missing file as dangling: state the ordering the L1 must follow. Report "
    "sections: `CURRENT:` (verbatim lines), `PROPOSED EDITS:`, `ORDERING:`, `PROVINCE:`.")
add("ScoutStagedS398", "scout",
    "Read the staged entry {STAGED}/knowledge/corpus/knowledge/crawler-identity-three-signals.md and row S398 in {STAGED}/SOURCES.append.md. Check EVERY staged "
    "sentence against the retained S425 body (`python3 -B {W}/span_tools.py window S425`, and grep the full body): supported (with page span) / not on this "
    "page (e.g. Baidu/Yahoo cross-operator claims, 'the signal anyone can set', AdsBot and `*`) / wrong. Also check the staged recheck command and anchor. "
    "Report sections: `SENTENCES:` (staged sentence, verdict, page span or absence count), `REFUSED:`, `KEPT:`.")
add("ScoutRejectAmendment", "scout",
    "Screen the staged amendment {STAGED}/amendments/corpus/knowledge/crawler-identity.md (MERGE-REPORT says 'append, do not replace') against the lane's "
    "current {KNOW}/crawler-identity.md and row S263: is it new knowledge or a duplicate of what the lane already holds (compare sentence by sentence)? "
    "Re-open its cited source with curl and locate its quotes. Give a reject/admit decision line with reason and flip condition. Report sections: "
    "`COMPARISON:`, `SOURCE CHECK:`, `DECISION LINE:`.")
add("ScoutRejectYahooUA", "scout",
    "Screen the staged {STAGED}/knowledge/corpus/knowledge/yahoo-crawler-ua-carrier-survey.md (and its rows in {STAGED}/SOURCES.append.md) as a second "
    "candidate of the crawler-identity theme: re-open each cited source (curl), locate each quote, check PROVINCE fit ({LANE}/PROVINCE.md) and the lane's "
    "existing Yahoo! JAPAN crawler entries (`ls {KNOW} | grep yahoo`). Decision line (admit later / reject) with page evidence and flip. Report sections: "
    "`SOURCES:` (url, http, quote found?), `DECISION LINE:`.")
add("ExecSourceLive", "executor",
    "Re-open both C3 pages live (curl, UA `kake-shokunin-round59-recheck`, into your scratch) and compare the article-block text nodes (collapsed, as "
    "c59_quote_truth.py's text_segments) with the retained bodies {SRC}/S425.html and S426.html: identical? list differences. Confirm S425's article body "
    "links to the S426 URL (grep the href in the RETAINED body; print the line). Record HTTP status, final URL, sha256, `Last updated` line. Copy the "
    "fetched bodies' hashes (not the bodies) to {R}/ExecSourceLive.files/. Report sections: `FETCHES:`, `TEXT-NODE DIFF:`, `S425->S426 LINK:`, `VERDICT:`.")
add("ExecC3SelftestPort", "executor",
    "Claim C3: write the selftest for {W}/c59_quote_truth.py (version 1 is a stub). Model: the round-58 selftest (`git -C {LANE} show "
    "{FREEZE}:.ufo/waves/round-58/c58_quote_truth.py`, `selftest()` and `_build`), which builds a synthetic evidence set in a scratch git repo and runs "
    "`run_checks`. Port it to S425/S426 using spans that are real substrings of the retained bodies (span_tools), add C9 cases: stale line rewritten; stale "
    "line deleted; tail inserted 20 lines away; tail without the tag; tail without S425; tail quoting a span not in the page / not carrying `IP address` / "
    "curly quotes; a second copy of the stale line; plus English-specific cases: a span crossing a text-node boundary, a nav/TOC span outside the article "
    "block, a footer-only span, a 161-character span, a heading anchor that is not h2/h3. Write the copy to {R}/ExecC3SelftestPort.files/c59_quote_truth.py "
    "(only `selftest()` and helpers changed; `run_checks` byte-identical) and run it. Report sections: `CASES:` (>= 40, name, condition targeted, result), "
    "`TALLY:`, `COUNTER DEFECTS FOUND:`, `DIFF:`.")
add("ExecC3BaseControls", "executor",
    "Claim C3 cheap controls against version 1: in a scratch clone at {FREEZE} build evidence sets that should NOT meet 9/9 and score them: (a) entries "
    "made only of page-unique spans from the page's sidebar/TOC/feedback widget if any fall inside the block window; (b) two entries that quote true spans "
    "but whose prose asserts the opposite (record: a stated limit); (c) the correction tail placed as an HTML comment; (d) the stale line kept but the tail "
    "contradicting S425; (e) used-by listing extra files. Report which meet and why; propose fixes for genuine holes. Report sections: `CONTROLS:`, "
    "`HOLES:`, `VERDICT:`.")
add("CriticC3Cheat", "critic",
    "Attack {W}/c59_quote_truth.py version 1 (read derive_c59_quote_truth.py for what changed from round 58): find ways to reach 9/9 with false or junk "
    "content — whitespace collapse admitting spans that never appear as written; CHAR_CEILING 160 admitting multi-sentence spans; the article window "
    "(`class=\"devsite-article-body` to `<devsite-content-footer`) admitting non-article text; `Last updated` matched in a script/JSON text node; anchor "
    "headings matched by an h2 inside a code sample; C9's window/insert logic (insert into a neighbouring bullet, tag inside a code span, S425 cited only in "
    "an HTML comment). Build each in scratch (rules in context). Report sections: `CHEATS:` (cheat, result), `HOLES:`, `VERDICT:`.")
add("CriticEntryOverreach", "critic",
    "Prepare the must-not list for the two C3 entries and the correction: from the retained bodies (span_tools window S425/S426) list statements a drafter "
    "is likely to add that the pages do NOT make (e.g. 'user-agents are easily spoofed' — check S426's opening paragraph wording exactly; 'Google publishes "
    "IP ranges for Googlebot only'; 'reverse DNS alone is enough'; 'the log records only IP and UA'; anything about Bing/Baidu/Yahoo). For each give the "
    "exact page wording that bounds it. Report sections: `MUST-NOT:` (statement, page evidence), `QUALIFIERS TO KEEP:` (exact words), `VERDICT:`.")
add("ReviewerFidelityPrep", "reviewer",
    "Build a sentence-by-sentence reference for the C3 pages: for S425's `Verify Google's crawlers and fetchers` section and its IP-address paragraph, and "
    "all of S426's article block, list each sentence verbatim (collapsed) with a one-line faithful paraphrase and the qualifiers it carries (may, either, "
    "sufficient for most use cases, etc.). This is the yardstick residual reviewers will use. Report sections: `S425:`, `S426:`, `VERDICT:`. Also write it to "
    "{R}/ReviewerFidelityPrep.files/reference.md.")
add("ReviewerC3Derive", "reviewer",
    "Review {W}/derive_c59_quote_truth.py and the generated {W}/c59_quote_truth.py against the round-58 counter (`git -C {LANE} show "
    "{FREEZE}:.ufo/waves/round-58/c58_quote_truth.py`): is every change justified by the derive docstring; did any condition get weaker than round 58 "
    "(collapsed whitespace vs raw substring; 160 vs 40 characters; anchor uniqueness dropped for an h2/h3 match; date in a footer text node); is C9's "
    "difflib append-only test sound (what does SequenceMatcher do with repeated blank lines?); does main() pin both revisions once. Report sections: "
    "`FINDINGS:` (severity, line, fix), `WEAKENINGS:` (justified or not), `VERDICT:`.")
add("MutC3Counter", "mutation-tester",
    "Mutation-test the C9 condition and the English-page changes of {W}/c59_quote_truth.py: copy it to your scratch, write a minimal fixture set yourself "
    "(scratch git repo: base with the real crawler-identity.md bytes from {BASE}, a measured commit with a correct tail citing S425 and a true span; the "
    "retained bodies and receipts copied from {SRC}) and >= 16 single-point mutants (window 8 -> 80, `delete`/`replace` check removed, tag check removed, "
    "S425 regex loosened, TOPIC check removed, CHAR_CEILING raised, collapse removed, article end marker changed, headings regex h2 -> h[1-6], date check "
    "outside text nodes, USED_BY sorted() removed). Report sections: `FIXTURES:`, `MUTANTS:` (id, change, killed?), `SURVIVORS:`, `PROPOSED FIXTURES:`.")
add("ProbeBodyStability", "executor",
    "Hypothesis: the S425/S426 article text is stable across fetches while page chrome varies. Fetch each URL 3 times (spaced >= 30 s; UA "
    "`kake-shokunin-round59-probe`) into your scratch; compare full-body sha256 and the collapsed article text nodes; identify varying regions. Recommend a "
    "recheck grep span per page that does not cross a source line break. Report sections: `FETCHES:`, `VARIATION:`, `RECHECK SPANS:`, `VERDICT:`.")
add("ScoutCorpusBar", "scout",
    "Bar check for the C3 entries and correction: read {LANE}/corpus/QUALITY.md (criteria for new knowledge entries and for correction tails: quotes, "
    "renderings, [INFERENCE], scope note, cross-links, recheck form, append-only corrections) and {FLEET}/CORPUS.md rules 1-5. Produce a numbered checklist "
    "the L1 applies to each drafted file, each item with the criterion's file:line. Report sections: `CHECKLIST:`, `SOURCES:` (file:line).")
add("ScoutLaneCrawlerIdentity", "scout",
    "What does the lane already hold on crawler identity and verification? Read {KNOW}/crawler-identity.md, baidu-spider-identification.md, any Yahoo DNS "
    "entries, README coverage rows; list overlaps/duplication risks for the two new entries, and every other passage in the lane (corpus, SKILL.md, "
    "README.md, PROVINCE.md) that states or relies on the UA-only claim. Report sections: `HELD:`, `OVERLAP RISKS:`, `UA-ONLY OCCURRENCES:` (file:line, "
    "verbatim).")
add("ScribeLessonMistakes", "scribe",
    "Frontier step: draft `corpus/lessons/round-59.md` `## Mistakes` and matching QUALITY.md round-59 criteria. Read "
    "{LANE}/corpus/lessons/round-58-verifier-spotcheck.md §6 (D1-D3), the round-51..58 spot-checks for every time D1 was routed (`grep -n 'only thing a "
    "server log\\|crawler-identity' {LANE}/corpus/lessons/round-5*-verifier-spotcheck.md`), {LANE}/corpus/lessons/round-58.md `## Mistakes`, the tail of "
    "{LANE}/corpus/QUALITY.md (round-58 criteria style), {FLEET}/CORPUS.md (mistake row format: class · evidence pointer · captured-by · fix; a fix counts "
    "only once shown able to fail), {W}/controls/base-c1-axis-evidence.txt and base-c3-quote-truth.txt. Rows: (M1) a routed defect carried N rounds "
    "unrepaired (count N from the spot-checks; captured-by: none — no gate tracks routed-defect age; fix: C3 C9, red-before base 0/9); (M2) axis-table "
    "evidence cells citing `/tmp` and a removed source tree while the scores stayed 10 (captured-by: prompt §7.5 '/tmp is never citable' and kotodama Q14, "
    "not applied to SCORECARD; fix: C1, red-before 16 mismatches). Draft 2 QUALITY criteria each with an example that fails it. Report sections: "
    "`MISTAKES:` (markdown rows), `QUALITY:` (exact append text), `RED-BEFORE:` (command + output), `OPEN:`.")
add("ScribeConsiderthese", "scribe",
    "Assimilation duty (considerthese): ground ONE still-unimplemented proposal of {LANE}/considerthese/2026-10-26.md — proposal 3 (operator-decision "
    "queue) — through the lane's bar: open what it points at ({FLEET}/.ufo/l0-questions.md kake lines, the round-54..58 spot-checks' operator items, SHONEN "
    "promotion notes) and build the queue: item, first raised (round + pointer), rounds waited as of round 59, current state. Draft it as a lesson section "
    "`## Considerthese` for corpus/lessons/round-59.md citing `considerthese/2026-10-26.md` (2026-10-26). Report sections: `QUEUE:` (table), `SECTION:` "
    "(exact text), `NOT TAKEN:` (other proposals and why).")
add("ScribeSearchLog", "scribe",
    "Draft the round-59 lesson `## Search log (rule 5)` and `## Trend inputs` sections (model: {LANE}/corpus/lessons/round-58.md). Theme: crawler identity "
    "verification signals (assimilation from merge/kake/: staged crawler-identity-three-signals.md / S398; S426 lane-found via S425's link). Question, "
    "where looked, included (2), excluded (with reasons, from the scout seats' screening: the staged crawler-identity.md amendment and "
    "yahoo-crawler-ua-carrier-survey.md), stop rationale. Report sections: `SEARCH LOG:`, `TREND INPUTS:`.")
add("ExecValidateAppend", "executor",
    "Claim C3 C7 tooling: write {R}/ExecValidateAppend.files/validate_append.sh for round 59 from {LANE}/.ufo/waves/round-58/validate_append.sh (round-59 "
    "paths; mirror the whole working-tree corpus + the non-corpus used-by targets held rows name — derive that list from the registry's used-by cells, do "
    "not copy round 58's list blindly). Dry-run it against a scratch copy of the lane (NOT the lane: set LANE via an env var defaulting to the lane, run "
    "with LANE=<scratch copy>) with two draft rows S425/S426 appended and stub entry files, and show exit 0 and the last stdout line. Report sections: "
    "`SCRIPT:` (fenced), `DRY RUN:`, `USED-BY TARGETS:`.")

# ---- cross-claim, adjacency, no-harm ----------------------------------------------------------------
add("ConnSiblingOverlap", "connector",
    "Adjacency: which sibling lanes under {FLEET} (`ls -d {FLEET}/*-shokunin`) hold crawler identification/verification material (Googlebot reverse DNS, "
    "IP ranges) or a source-id resolver? grep their corpus/SOURCES.md and corpus/knowledge for overview-google-crawlers, verify-google-requests, "
    "`googlebot.com`, `id_resolver`. Report contested scope; nothing is absorbed. Report sections: `OVERLAPS:` (lane, file:line), `CONTESTED:`, `VERDICT:`.")
add("ConnCrossClaim", "connector",
    "Cross-claim pattern scan: C1, C2 and C3 each fix a 'claim the lane states vs what is observed' gap at a different surface (SCORECARD cells, tool output, "
    "knowledge prose). Check causal separability (can each be verified with the other two reverted?), shared weaknesses across the three counters (e.g. "
    "all trust committed files a seat could write; all exclude prose truth), and whether one counter's after-state could make another go red. Report "
    "sections: `SEPARABILITY:`, `SHARED WEAKNESSES:`, `INTERACTIONS:`, `VERDICT:`.")
add("ConnMistakeClasses", "connector",
    "Pattern across the lane's spot-checks rounds 50-58 ({LANE}/corpus/lessons/round-5*-verifier-spotcheck.md): list every routed defect, the round first "
    "routed, and the round closed (or open). Which classes recur (carried defects, receipt rewrites, stale pins, quote fidelity)? Report sections: "
    "`DEFECTS:` (table), `RECURRING CLASSES:`, `VERDICT:`.")
add("ConnFleetCalibration", "connector",
    "Fleet pattern (report only): in 5-6 sibling lanes' SCORECARD.md axis tables, how many evidence cells cite `/tmp`, `~`, absolute paths or files absent "
    "from their repo (`git -C <lane> cat-file -e HEAD:<path>`)? Use the same token rules as {W}/c59_axis_evidence.py (you may import its `pointers()`). "
    "Report sections: `LANES:` (lane, cells, dead pointers), `NOTE:`.")
add("ExecHistoricalGates", "executor",
    "No-harm baseline: in a shared clone at {BASE} under your scratch run the lane's earlier gates and record exit + summary line: "
    ".ufo/waves/round-58/c58_resolver_cases.py (--seed 58), c58_quote_truth.py, c58_receipt_rewrites.py; .ufo/waves/round-57/c57_idresolver_gate.py "
    "(--fleet {FLEET}); .ufo/waves/round-55/c55_readme_index.py; .ufo/waves/round-56/c56_selftally.py (slow); each with `--root <clone> --revision {BASE}` "
    "(read each --help/docstring for flags). Note which SKILL.md rows mark each historical. These are the base values the L1 compares the build against. "
    "Report sections: `RUNS:` (gate, exit, summary), `HISTORICAL MARKINGS:`, `PREDICTED HARMS:` (which gates the round-59 changes will turn red by design).")
add("ReviewerContract", "reviewer",
    "Review {W}/contract.md and contract.json as a whole: the same predicate sentence in contract, json and each counter's PREDICATE; base receipts match "
    "the stated before-values ({W}/controls/base-*.txt); causal separability; each do-nothing control; the D1/D2/D3 routing; the quarantine hold vs the "
    "prompt's §10 duty; the access-date choice (2026-10-27 UTC). Report sections: `FINDINGS:` (severity, issue, fix), `VERDICT:`.")
add("CriticAxisClaims", "critic",
    "Attack the axis naming of each claim against {FLEET}/AXES.md and the prompt rule 'name the axis by the surface the round changes, not by the number it "
    "produces': is C1 calibration (SCORECARD vs observed state) or operability; is C2 operability; is C3 freshness (a stale claim corrected against a "
    "re-opened live source) or coverage/expansion (two new entries)? Propose the honest label per claim. Report sections: `C1:`, `C2:`, `C3:`, `VERDICT:`.")
add("CriticControlsSizing", "critic",
    "Attack the sizing: can a do-nothing or near-do-nothing control reach any of the three predicates ({W}/contract.md; counters in {W})? Is each target "
    "something one round can land? Is any predicate a universal clause the counter does not enumerate? Build at least one cheap control per claim in "
    "scratch and score it. Report sections: `CONTROLS:` (claim, control, result), `SIZING:`, `VERDICT:`.")
add("SentinelCounters", "sentinel",
    "Integrity/security review of the three round-59 counters ({W}/c59_axis_evidence.py, c59_resolver_cases.py, c59_quote_truth.py): inherited GIT_* "
    "and other env (GIT_CONFIG_*, HOME, PYTHONPATH), hostile .git/config in a measured repo, symlinks in the measured tree (a SCORECARD.md symlink; a "
    "receipt symlink), argument injection via --revision (`--output=...`), hardcoded /tmp, leftover scratch, non-toplevel roots. Verify the round-58 D2 "
    "items are fixed forward (scrubbed env, resolved base/revision, toplevel root). Report sections: `FINDINGS:` (severity, counter:line, repro, fix), "
    "`D2 STATUS:`, `VERDICT:`.")
add("ExecCountersTmpScan", "executor",
    "Prompt §7.4 scan: list every committed lane tool/counter (scripts/*.py, scripts/*.mjs, .ufo/waves/round-5*/**/*.py) that writes under a hardcoded "
    "/tmp regardless of TMPDIR/--work (`grep -nE \"(/tmp|mkdtemp\\(dir=.?/tmp)\"`), with file:line and whether it honours TMPDIR. These are routed "
    "defects to record, not fixes this round. Report sections: `HITS:`, `CLEAN:`, `VERDICT:`.")
add("SimplifierCounters", "simplifier",
    "Read the three round-59 counters and the two derive scripts in {W}: find dead code, unused constants/imports, duplicated helpers, needless "
    "complexity introduced by derivation (e.g. code paths of round 58 that can never run for round 59). Proposals only (diff hunks), each with the "
    "behaviour-preservation argument. Report sections: `PROPOSALS:`, `KEEP:`, `VERDICT:`.")
add("ScoutOperatorLessons", "scout",
    "Read-only: any {LANE}/corpus/lessons/operator-*.md teaching not yet reflected in QUALITY.md/SKILL.md; and map the round-58 spot-check "
    "({LANE}/corpus/lessons/round-58-verifier-spotcheck.md §6 D1-D3, carried limits, §7 SHONEN note) to this round's contract ({W}/contract.md): what is "
    "addressed, what is carried, what is unaddressed. Report sections: `OPERATOR LESSONS:`, `SPOT-CHECK MAP:`, `UNADDRESSED:`.")
add("ExecLandedCheck", "executor",
    "Run `python3 -B {LANE}/scripts/landed_check.py --help` then check the round-58 report {FLEET}/.ufo/reports/round-58/kake.md with it against the lane "
    "(every cited hash an ancestor of master?), and the round-58 SCORECARD section's hashes. Report sections: `RUN:`, `RESULT:`, `VERDICT:`.")
add("LabratK12Contract", "executor",
    "Hypothesis: the current tool already exits 2 when `corpus/SOURCES.md` is missing or unreadable, so K12's 'out-of-lane registry -> exit 2' is "
    "consistent with its existing contract. Build scratch fixtures (rules in context): registry missing; registry a directory; registry a broken symlink; "
    "registry a symlink to an in-lane file; registry a symlink out of the lane. Run the CURRENT tool on each. Report sections: `RUNS:`, `READING:`, "
    "`VERDICT:`.")
add("ReviewerQuarantineHold", "reviewer",
    "Review the quarantine handling: {W}/assimilation/quarantine-slice (12 rows, byte-identical to round 58's), the round-58 lesson §Assimilation verdict "
    "table, the unanswered L0 line (`grep -n 'kake | round-58' {FLEET}/.ufo/l0-questions.md`) and the prompt's §10 quarantine bullet (non-wave-4 lanes: rows "
    "are 'not appendable until hand-checked this round'). Is holding all 12 again (L0 unanswered) conformant, or must this round re-hand-check them? "
    "Re-open 3 of the six `present` rows (S142, S161, S194) yourself (curl; locate the registered quote) to keep the verdicts fresh. Report sections: "
    "`RE-OPENED:` (row, url, quote found?), `CONFORMANCE:`, `VERDICT:`.")
add("ScribeQuarantineVerdicts", "scribe",
    "Re-hand-check the remaining quarantine rows this round (S143, S148, S154, S156, S178, S184, S193, S195, S206; the ReviewerQuarantineHold seat does S142, "
    "S161, S194): for each, open the cited source (registered URL/quote from {W}/assimilation/quarantine-slice and the register "
    "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md, READ-ONLY), locate the quote, and give a verdict (present / absent "
    "as registered / unverifiable-prose-class), dated 2026-10-27. Draft the lesson table `## Assimilation` quarantine rows in the round-58 shape. Report "
    "sections: `ROWS:` (row, url, located text, verdict), `TABLE:` (markdown).")

SPEC = {"reportDir": ".ufo/waves/round-59/w1", "maxLanes": 128, "context": CONTEXT, "items": items}
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
    json.dump(SPEC, open(out, "w"), indent=1, ensure_ascii=False)
    c = Counter(i["role"] for i in items)
    flash = sum(c[r] for r in ("executor", "labrat", "scribe", "sonic", "simplifier", "revenger", "sentinel"))
    attack = sum(c[r] for r in ("reviewer", "critic", "mutation-tester", "labrat"))
    print(len(items), dict(c), f"flash={flash} ({flash/len(items):.0%}) attack={attack} ({attack/len(items):.0%})")
