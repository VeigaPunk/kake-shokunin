#!/usr/bin/env python3
"""Generate the round-60 wave w2 (v1 policy, FALSIFY wave): fresh attack seats on what wave 1 produced, committed as build
B1 = 8b33fd24 with counters version 1 frozen at 1ea30590. Every item names the w1 product it attacks. Output: w2-spec.json."""
import json
import os
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = f"{LANE}/.ufo/waves/round-60"
R = f"{W}/w2"
SRC = f"{W}/sources"
KNOW = f"{LANE}/corpus/knowledge"
STAGED = "/home/vgpnk/Projects/shokuknow/merge/kake"
FLEET = "/home/vgpnk/Projects/shokunin"
BASE = "97cdc122379711c2b02a8970752c8782da3ac81d"
V1 = "1ea305904933ac0f57e84ac1e7a8207e486f577d"
B1 = "8b33fd248d126b48d838af5c38bc175850f41a09"
SCR = "/fast/scratch/hyaku/kake-r60"
GODSPEED = "/skill:godspeed\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md", encoding="utf-8").read() + "\n"

CONTEXT = (
    "/skill:godspeed\n"
    "Round-60 kake wave w2 (FALSIFY wave, the second of two v1 waves). Lane repo: " + LANE + ". Your tools start at the FLEET root ("
    + FLEET + "), not the lane: FIRST `mkdir -p " + SCR + "/<your seat name> && cd` there; use absolute paths for every read and write; "
    "never use a relative redirect outside your scratch dir. Every `Report:` trailer path is relative to " + LANE + " — write it at "
    + LANE + "/<that path> (i.e. " + R + "/<Seat>.md), never under the fleet root. Seats never mutate the fleet repo, sibling lanes, lane "
    "jj state or the lane Git index: write ONLY your own report file and files inside " + R + "/<Seat>.files/ — no other path; no `git "
    "add/commit/stash/checkout/reset/pull/push` and no jj mutation in the lane. Read-only git (show, log, ls-tree, rev-parse, diff, "
    "cat-file) is fine. Scratch: every clone, fixture and work dir lives under " + SCR + "/<your seat name>/ (pass it as TMPDIR / --work; "
    "`/tmp` only for files under 50 MB, never cited); use `git clone -q --shared` rather than full clones; delete your scratch dir before "
    "you finish (copy what you cite into your .files/ first; `trap 'rm -rf -- \"$S\"' EXIT`). Fixture repos and scratch commits: "
    "`D=$(mktemp -d -p " + SCR + "/<seat>) && git -C \"$D\" init -q` (or a `--shared` clone inside your scratch dir), every later git "
    "call names `-C \"$D\"`, verify `git -C \"$D\" rev-parse --show-toplevel` equals `$D` before the first commit, commit only with `-c "
    "user.name=selftest -c user.email=selftest@local`; never commit anywhere else. /home/vgpnk/Projects/shokuknow is read-only; sibling "
    "lane repos are read-only. Round facts: contract " + W + "/contract.md (+ contract.json; amendments A1-A9, A3a and stated limits at "
    "its end) — READ IT FIRST; base " + BASE + "; counters version 1 frozen at " + V1 + " (c60_gate_status.py, c60_guard_cases.py, "
    "c60_quote_truth.py + derive; base receipts and selftests under .ufo/waves/round-60/controls/); build B1 = " + B1 + " (scripts/append_guard.py, "
    "rows S427-S429 in corpus/SOURCES.md, corpus/knowledge/google-user-triggered-fetchers.md, corpus/knowledge/robots-txt-limits.md, the "
    "[r60-correction 2026-10-27] run in corpus/knowledge/googlebot-verification.md, SKILL.md § Round 60 gate-status ledger and registry "
    "additions plus three relabelled rows, corpus/lessons/round-60.md, corpus/QUALITY.md § Round-60 criteria, corpus/README.md rows). Wave-1 "
    "reports: " + W + "/w1/. Predicates (frozen): C1 `met: members == 28 AND mismatches == 0 AND scores_held == 3`; C2 `met: cases_passed == "
    "24 of 24`; C3 `met: conditions_passed == 9 of 9`. The counters are frozen, so you MAY run them at B1 in your own scratch clone; the L1 "
    "measures the claims itself at the final revision. Your job is to FALSIFY: find what is wrong, overclaimed, untested or broken, with "
    "the exact command and output that shows it; a version 2 of a counter may only tighten. Quote rule for sources: 6..25 whitespace "
    "tokens, <= 160 characters, a substring of ONE whitespace-collapsed text node of the retained body's article block, page-unique; retained "
    "bodies " + SRC + "/S427.html, S428.html, S429.html (+ receipts.json). Never fabricate: an unrun check is reported as unrun; mark "
    "unverified statements [INFERENCE]. No credentials, tokens, op:// refs or private URLs in any report. Tooling authorization (operator, "
    "2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, "
    "update-safety gate; record tool/version/channel/reason). Pacman guard: all pacman transactions are PAUSED host-wide — never run pacman "
    "(no -S, -Sy, -Syu, -U, -R); install via `uv tool`/`npx`/an official binary in ~/.local/bin or report the need; never restart a host "
    "service. The host is loaded: generous timeouts, no retry loops. Report format: first line `# <your seat name>`, then `ATTACKS:` "
    "(what you attacked), the sections your item names, factual, under ~150 lines (code in .files/); a `FINDINGS:` table (severity "
    "high/medium/low, target file:line, issue, evidence command, fix); last line `VERDICT: <one line>`. The L1 (KakeR60) holds the "
    "planner seat and integrates; you are a leaf: no subagent dispatch."
)

items = []


def add(name, role, text):
    for k, v in (("{W}", W), ("{R}", R), ("{LANE}", LANE), ("{SRC}", SRC), ("{KNOW}", KNOW), ("{STAGED}", STAGED), ("{FLEET}", FLEET),
                 ("{BASE}", BASE), ("{SCR}", SCR), ("{V1}", V1), ("{B1}", B1)):
        text = text.replace(k, v)
    items.append({"name": name, "role": role, "prompt": GODSPEED + "Attacks: " + text})


# ---- C1 -------------------------------------------------------------------------------------------
add("MutC1Counter", "mutation-tester",
    "{W}/c60_gate_status.py (C1 counter v1). Generate >= 25 mutants in a scratch copy (each mismatch class check, A2 bracket rule, A3 shape "
    "rule incl. the A3a SELF_CHECKOUT exception, A4 frozen blobs, A5 exit exactness, A6 duplicate rows, A7 scores), run the counter's "
    "`--selftest` per mutant and also the counter at B1 and at {BASE} per mutant. Report each mutant: killed by selftest? changes the B1 / base "
    "verdict? Survivors = blind spots; propose a selftest case per survivor. Sections: `MUTANTS:`, `SURVIVORS:`, `CASES TO ADD:`.")
add("ReviewerC1Counter", "reviewer",
    "{W}/c60_gate_status.py against contract § Claim C1 and amendments A2-A7, A3a, line by line: population regex and frozen set, row parse "
    "(fences, indented code, HTML comments, `\\|`), label words, pin rules, command rendering, env, timeouts, clone cleanup, exit codes, "
    "output. Every divergence between contract text and code is a finding. Sections: `DIVERGENCES:`, `FINDINGS:`.")
add("CriticC1CheatV1", "critic",
    "C1 at B1 with the FROZEN v1 counter. On scratch clones of B1 build the cheapest after-states that print `met=True` WITHOUT honest "
    "labels (e.g. a historical pin that is green for the wrong reason, a never-met label on a counter that was green once, a live label "
    "kept by editing a member's expected values without changing its blob, a registry row inside a construct the parser misreads, a Kind "
    "cell that tricks the word match). Run the counter on each; report which ones pass. Sections: `CHEATS:` (cheat, commit, counter "
    "output), `HOLES:`, `TIGHTENINGS:`.")
add("ReviewerC1Rows", "reviewer",
    "the 12 new member rows in {LANE}/SKILL.md § Round 60 gate-status ledger and registry additions (B1). For each row, read the counter's "
    "code and check every cell: the Entry command is the real CLI, the verdict map lists the exit codes the code actually uses, the "
    "self-test cell is real (run it if it exists), the pinned-values cell's paths exist at B1, the label is honest (run the command at B1 "
    "and at the pin). Sections: `ROWS:` (row, cell, issue), `FINDINGS:`.")
add("ReviewerC1Relabels", "reviewer",
    "the four label changes at B1: c53_gate_truth.py -> never met (pin fd91527a), receipt-pin-counter pin 32754df7 -> 20217f23, "
    "crawler-identity-quote-truth-counter -> historical (pin b322ccab), ops-debt-counter (c54_ops_debt.py) historical (pin a631cc02). Re-run each "
    "command at B1 and at the old and new pins in a scratch clone; was any member EVER green that is now labelled never met (try more "
    "revisions: `git log --format=%H -- .ufo/waves/round-53`)? Is 20217f23 the right pin and is the Kind text accurate? Sections: `RUNS:`, "
    "`FINDINGS:`.")
add("ReviewerC1Rerun", "reviewer",
    "the C1 counting command. Re-run `python3 -B .ufo/waves/round-60/c60_gate_status.py --root . --revision {B1} --jobs 4` in a `--shared` "
    "clone of the lane (cwd = clone) and also with `--root {LANE}` directly; compare per-member lines and the summary with each other and "
    "with the base receipt {W}/controls/base-c1-gate-status.txt; run the selftest; time it. Any nondeterminism (c57 reads live sibling "
    "registries) is a finding. Sections: `RUNS:`, `DIFF:`, `FINDINGS:`.")
add("SentinelC1Exec", "sentinel",
    "{W}/c60_gate_status.py execution safety: it executes 28 committed scripts from registry text. Check: no shell, argv rendering cannot "
    "inject, env scrubbing (try a lane-committed `sitecustomize.py`/`.pth` in the clone, PYTHONSTARTUP, a member writing outside its clone, "
    "a member that never exits, a member that forks a daemon), clone/scratch cleanup on SIGINT and on exceptions, nothing under /tmp. "
    "Sections: `ATTACKS RUN:`, `FINDINGS:`.")
add("CriticC1Fixtures", "critic",
    "the C1 counter with the independent wave-1 harness {W}/w1/ExecC1Fixtures.files/c60_gate_status_fixtures.py (54 cases, written before "
    "amendments A2-A7). The v1 counter freezes its member set (A4), so fixture lanes cannot reach `members == 28`; adapt the harness (in your "
    ".files/) to drive the counter's internal check function with a fixture member set (read how its selftest does it) and run all 54 "
    "clauses; report every case where the counter's class differs from the contract-derived expectation. Sections: `ADAPTATION:`, "
    "`DIVERGENCES:`, `FINDINGS:`.")
add("ScoutC1Population", "scout",
    "the C1 population at B1: list every counter-like file under .ufo/waves/round-4[0-9] and round-5[0-9] and round-60 (`git -C {LANE} ls-tree "
    "-r --name-only {B1} -- .ufo/waves | grep -E '/c[0-9]+_'`), confirm the 28 frozen members and blob ids, find any population-regex file "
    "outside the frozen set, and any committed counter the registry still lacks (rounds 40-47, round-60 counters); check the disclosure in "
    "contract.md and SKILL.md is accurate. Sections: `POPULATION:`, `UNREGISTERED:`, `FINDINGS:`.")
add("ReviewerLedgerProse", "reviewer",
    "{LANE}/SKILL.md § Round 60 gate-status ledger and registry additions (prose, label rules, historical-gate list) at B1 against the "
    "counter's actual behaviour and the rows' Kind cells: every statement true? the historical list complete and correct (each listed row "
    "labelled so, no labelled row missing)? Sections: `STATEMENTS:` (statement, true?, evidence), `FINDINGS:`.")
add("ReviewerSkillEdits", "reviewer",
    "the L1's in-place SKILL.md edits in B1 (`git -C {LANE} diff {V1} {B1} -- SKILL.md`): the three Kind relabels and the line-1215 "
    "wave-evidence-ledger cell change (a path replaced by the row name `ledger-mutation-ladder`). Do they break any gate that reads those "
    "cells — c52_wave_ledger.py, c52_gate_registry.py, c54_ops_debt.py, c56_selftally.py, scripts/corpus-contract.mjs, the freshness-sweep "
    "sidecar (corpus/knowledge/freshness-sidecar.json binds SKILL.md lines)? Run each at {V1} and {B1}. Sections: `RUNS:`, `FINDINGS:`.")

# ---- C2 -------------------------------------------------------------------------------------------
add("MutGuardTool", "mutation-tester",
    "{LANE}/scripts/append_guard.py at B1. Generate >= 30 mutants in scratch (tag regex, comment/code-span visibility, DP alignment, EOF run "
    "rule, deleted/symlink/submodule detection, scope glob, exit codes, GIT_* scrub, base-ancestor check), run the tool's `--selftest` (38 cases) "
    "and the C2 counter with `--tool <mutant>` (24 cases) per mutant. Report kills and survivors; propose cases. Sections: `MUTANTS:`, "
    "`SURVIVORS:`, `CASES TO ADD:`.")
add("MutC2Counter", "mutation-tester",
    "{W}/c60_guard_cases.py (C2 counter v1). Mutate its fixtures and its judge (exactness clause A8, finding regex, summary rule, per-case "
    "expectations, seed use, R1/R2 real-lane cases, missing-tool handling) and run its `--selftest` (6 controls) per mutant. Survivors = places "
    "the counter would accept a wrong tool. Sections: `MUTANTS:`, `SURVIVORS:`, `CASES TO ADD:`.")
add("ReviewerGuardCode", "reviewer",
    "{LANE}/scripts/append_guard.py at B1 against contract § Claim C2 clause by clause (CLI, default scope, exits, finding/summary format, "
    "committed bytes only, GIT_* scrub, toplevel check, base ancestry, the existential untagged_insertion rule, tag visibility outside HTML "
    "comments and backtick spans, EOF run, line splitting without normalisation). Report divergences with a reproducing fixture. Sections: "
    "`DIVERGENCES:`, `FINDINGS:`.")
add("CriticGuardDifferential", "critic",
    "the guard by differential fuzzing: generate >= 300 seeded random base/revision pairs (insertions with and without tags, duplicate lines, "
    "comments, code spans, deletions, swaps, CRLF, empty files) and compare {LANE}/scripts/append_guard.py with the independent "
    "{W}/w1/ExecGuardTool2.files/append_guard.py and with a brute-force oracle you write for the existential rule (small files). Every "
    "disagreement: minimal fixture, which one follows the contract text. Sections: `FUZZ:`, `DISAGREEMENTS:`, `FINDINGS:`.")
add("CriticGuardSemanticsV2", "critic",
    "the committed guard against the wave-1 semantic attacks {W}/w1/CriticC2Semantics.md K23-K36 and CR1-CR8 and "
    "{W}/w1/RevengerC55Intent.md P5-P7: build each fixture, run the tool at B1, and classify each as contract-conformant, a disclosed limit "
    "(contract § Stated limits) or an UNDISCLOSED gap. Sections: `CASES:` (id, fixture, tool result, class), `UNDISCLOSED:`, `FINDINGS:`.")
add("SentinelGuard", "sentinel",
    "{LANE}/scripts/append_guard.py robustness and safety at B1: `--scope` with `..`, absolute paths or globs escaping the repo, option "
    "injection through revision strings (`--revision=--output=x`), file names with newlines/quotes/non-UTF-8 (git quoting), very large or "
    "binary blobs (DP time/memory), symlinked repo, GIT_DIR/GIT_WORK_TREE in env, a revision that is a tag or tree id. Sections: `ATTACKS "
    "RUN:`, `FINDINGS:`.")
add("ReviewerC2Rerun", "reviewer",
    "the C2 counting command. Re-run `python3 -B .ufo/waves/round-60/c60_guard_cases.py --root . --revision {B1} --seed <s>` for three seeds "
    "(60, 1, 777) in a `--shared` clone; then run the tool on the real lane for every round range r50..B1 (`--base <round-N tip> --revision "
    "<round-N+1 tip>`, find tips from `git log --oneline`) and classify each finding as a true rewrite or a false red. Sections: `RUNS:`, "
    "`REAL HISTORY:`, `FINDINGS:`.")
add("CriticC2Fit", "critic",
    "the C2 claim framing: is a corpus append-only guard 'operability' for a web-properties/publishing lane (AXES.md operability: runnable "
    "artifacts)? Does it actually resolve routed defect R59-D1 (c55 head_changed collision) or only move it? Is the SCORECARD capability "
    "claim (append-only correction guard) honest given the stated limits? What does a do-nothing or trivial control score? Sections: "
    "`AXIS:`, `R59-D1:`, `CAPABILITY:`, `FINDINGS:`.")

# ---- C3 -------------------------------------------------------------------------------------------
add("ReviewerEntryUT", "reviewer",
    "{KNOW}/google-user-triggered-fetchers.md at B1, sentence by sentence against {SRC}/S428.html (article block): every statement "
    "supported by a span or marked as the lane's reading? every double-quoted span a substring of one text node, page-unique, 6..25 units? "
    "overreach beyond the page (e.g. about exceptions, spoofing, verification)? Sections: `SENTENCES:` (sentence, verdict, span), `FINDINGS:`.")
add("ReviewerEntryRL", "reviewer",
    "{KNOW}/robots-txt-limits.md at B1, sentence by sentence against {SRC}/S429.html (article block), and against what "
    "{KNOW}/robots-txt-rules.md already holds (duplication); check the staged-sentence refusals in {W}/w1/EntryRobotsLimits.md were honoured. "
    "Sections: `SENTENCES:`, `DUPLICATION:`, `FINDINGS:`.")
add("ReviewerCorrection", "reviewer",
    "the `[r60-correction 2026-10-27]` run in {KNOW}/googlebot-verification.md at B1 (`git -C {LANE} diff {BASE} {B1} -- "
    "corpus/knowledge/googlebot-verification.md`): is every sentence true to S428 and to the S426 cell it qualifies? overreach ('a publisher "
    "still cannot count on robots.txt...')? does it render inside the list item and outside the blockquote (check with a Markdown renderer "
    "such as `python3 -m markdown` or `npx marked` in scratch)? Sections: `SENTENCES:`, `RENDER:`, `FINDINGS:`.")
add("ReviewerRowsS427", "reviewer",
    "registry rows S427, S428, S429 in {LANE}/corpus/SOURCES.md at B1, cell by cell against the retained bodies: title, URL, kind, tier, "
    "scope (S427 must not overclaim for user-triggered fetchers), anchor (nearest preceding h1/h2/h3 of the Gate quote, amendment A1), "
    "teaches, status, opened, recheck, used-by; S427's `supersedes S425 —`; census at B1 (`{FLEET}/scripts/sources-census.sh validate "
    "--root {FLEET} kake` is lane-wide — run `--file` on a scratch copy of B1's registry instead). Sections: `ROWS:`, `CENSUS:`, `FINDINGS:`.")
add("MutC3Counter", "mutation-tester",
    "{W}/c60_quote_truth.py (C3 counter v1, 140-case selftest). Generate >= 25 mutants on the round-60 conditions (T1 scope regex, T2 was->now, "
    "T3 single run/block boundary, T4 fence/comment stripping, T6 receipts blob pin/effectiveUrl, T7 validate ancestry, T8 footer read, A1 "
    "anchor rule, used-by sets, subjects), run the selftest and the counter at B1 per mutant. Sections: `MUTANTS:`, `SURVIVORS:`, `CASES TO ADD:`.")
add("CriticC3CheatV1", "critic",
    "C3 at B1 with the FROZEN v1 counter: on scratch clones build after-states that meet 9/9 without the claimed work — e.g. an S427 scope "
    "that still overclaims in different words, an entry whose prose contradicts its true quotes, a correction that restates the stale "
    "wording, a quote from page chrome — and run the counter. Sections: `CHEATS:` (cheat, commit, result), `HOLES:`, `TIGHTENINGS:`.")
add("ReviewerC3Rerun", "reviewer",
    "the C3 counting command and the sources. Re-run `python3 -B .ufo/waves/round-60/c60_quote_truth.py --root . --revision {B1}` and its "
    "`--selftest` in a `--shared` clone; re-open the three URLs live (curl -sL --compressed), compare article text nodes with the retained "
    "bodies and confirm every Gate quote in {LANE}/corpus/lessons/round-60.md § Gate still occurs once. Sections: `RUNS:`, `LIVE:`, `FINDINGS:`.")
add("ScoutGateQuotes", "scout",
    "every double-quoted span in the two new entries, the correction run and the lesson Gate lines at B1: units, characters, single text "
    "node, page-unique, inside the article block (not nav/aside/footer); and every anchor heading named in rows/Gate/`source:` lines exists "
    "in the body and precedes its quote. Write a stdlib checker in .files/. Sections: `SPANS:` (file, span, result), `ANCHORS:`, `FINDINGS:`.")
add("CriticOverreachV2", "critic",
    "the landed C3 prose at B1 (two entries, correction, rows' teaches cells) against the wave-1 MUST-NOT list {W}/w1/CriticEntryOverreach.md "
    "(qualifiers `generally`, `may`, `with the ad publisher's permission`, `automatic crawls`, `might not`): every violation with file:line "
    "and the page wording that bounds it. Sections: `VIOLATIONS:`, `QUALIFIERS KEPT:`, `FINDINGS:`.")

# ---- frontier, lesson, no-harm, process -----------------------------------------------------------
add("ReviewerLesson", "reviewer",
    "{LANE}/corpus/lessons/round-60.md at B1: § Gate carries URL, access date and a <= 25-word located quote for every new row; § Mistakes "
    "rows (class vocabulary of {FLEET}/CORPUS.md, evidence pointers resolve at B1, red-before claims match the committed receipts under "
    "{W}/controls/); § Search log counts carry commands that reproduce; § Assimilation id lists match the files. Sections: `GATE:`, "
    "`MISTAKES:`, `COUNTS:`, `FINDINGS:`.")
add("ReviewerQuality", "reviewer",
    "{LANE}/corpus/QUALITY.md § Round-60 criteria at B1: each criterion cites a lesson, its falsifier command runs and does what it says, its "
    "'example that fails it' really fails (e.g. the `[r20-correction DATE: text]` spelling claim against scripts/append_guard.py). Run them. "
    "Sections: `CRITERIA:` (criterion, falsifier run, example run), `FINDINGS:`.")
add("CriticNoHarm", "critic",
    "no-harm. Enumerate every gate/tool row in {LANE}/SKILL.md (all `| Name | Kind | Entry command |` tables, including non-population "
    "tools: freshness-sweep, corpus-contract, id_resolver, canonical/base-path/link-preview/robots/sitemap/redirect/source-recheck audits, "
    "receipt replay, live/source snapshot selftests) and run each one's self-test or offline entry at {BASE} and at {B1} in scratch clones "
    "(skip anything needing network or authorization and say so). Any gate green at base and red at B1 is a harm finding unless the round "
    "relabelled it. Sections: `RUNS:` (gate, base, B1), `NEWLY RED:`, `FINDINGS:`.")
add("ReviewerREADME", "reviewer",
    "{LANE}/corpus/README.md changes at B1 (`git diff {BASE} {B1} -- corpus/README.md`): coverage-map rows true to the entries, frontier "
    "ground map row ids equal the entries' `used-by` rows, the base-absence sentences true (`git cat-file -e {BASE}:<path>`). Sections: "
    "`ROWS:`, `FINDINGS:`.")
add("ConnW2Cross", "connector",
    "cross-claim interactions at B1: does C3's correction pass C2's guard over {BASE}..{B1} (run it)? does any C1 relabel depend on C3 "
    "landing (c59 quote-truth) and is that disclosed? would C1 stay met if C3 were reverted (scratch revert of the rows)? patterns from "
    "rounds 55-59 closures (corpus/lessons/round-5[5-9]-verifier-spotcheck.md) that B1 repeats. Sections: `INTERACTIONS:`, `REVERT TEST:`, "
    "`PATTERNS:`, `FINDINGS:`.")
add("CriticControls", "critic",
    "do-nothing and cheap controls for all three claims at B1 sizes: build (scratch) the cheapest control per claim — C1: register the 12 "
    "rows with junk cells / label everything live; C2: a tool that only passes the clean cases, a byte-prefix tool, a tool that ignores "
    "tags; C3: rows only, no entries — score each with the frozen counter and report whether any meets its target. Sections: `CONTROLS:` "
    "(claim, control, result), `FINDINGS:`.")
add("ReviewerContractTimeline", "reviewer",
    "the contract timeline: amendments A1-A9 and A3a in {W}/contract.md vs the commit history (`git -C {LANE} log --format='%H %ci %s' "
    "{BASE}..{B1}`) and the seat reports' timestamps: was every amendment declared before any after-state was scored? is each labelled "
    "tightening/loosening honestly (e.g. A1 admits h1; A2 drops [--base <rev>]; A3a exempts c52_mutation_ladder)? does contract.json still "
    "carry the same predicate sentences? Sections: `TIMELINE:`, `AMENDMENTS:` (id, label claimed, actual), `FINDINGS:`.")
add("ScoutCensusB1", "scout",
    "the SOURCES census at B1 on a scratch copy of B1's corpus (`{FLEET}/scripts/sources-census.sh validate --file <scratch>/corpus/SOURCES.md`) "
    "and the frozen CORPUS.md awk formulas: rows, malformed, duplicate ids, enum, used-by paths existing at B1; compare with "
    "{W}/controls/census-before.txt (164 rows, 14 W04). Sections: `CENSUS:`, `DIFF:`, `FINDINGS:`.")
add("SentinelMisroot", "sentinel",
    "round hygiene after wave 1: `git -C {FLEET} status --porcelain` — any untracked file whose content names kake round 60 (a misrooted "
    "seat file)? leftovers under {SCR} and /tmp from wave-1 seats (list dirs with sizes and ages; do not delete other seats' dirs, report "
    "them); any file written by a w1 seat outside {W}/w1/ (compare `git -C {LANE} status --porcelain`). Sections: `FLEET ROOT:`, "
    "`SCRATCH:`, `LANE:`, `FINDINGS:`.")
add("CriticAxisV2", "critic",
    "the round's claims as landed at B1 against the round prompt §9 and AXES.md: is C1 a calibration claim (self-assessment vs observed state) "
    "or registry bookkeeping; does C3 freshness rest on a re-opened live surface; is any claim's target reachable by a control that skips the "
    "work; is any claim narrowed after data? Compare with what the round-59 closure accepted ({LANE}/corpus/lessons/round-59-verifier-spotcheck.md). "
    "Sections: `C1:`, `C2:`, `C3:`, `FINDINGS:`.")

SPEC = {"reportDir": ".ufo/waves/round-60/w2", "maxLanes": 64, "context": CONTEXT, "items": items}
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w2-spec.json")
    json.dump(SPEC, open(out, "w"), indent=1, ensure_ascii=False)
    c = Counter(i["role"] for i in items)
    attack = sum(c[r] for r in ("reviewer", "critic", "mutation-tester"))
    print(len(items), dict(c), f"attack={attack} ({attack/len(items):.0%})")
