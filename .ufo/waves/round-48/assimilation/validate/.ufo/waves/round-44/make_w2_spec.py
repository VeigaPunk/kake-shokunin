#!/usr/bin/env python3
"""Build the round-44 wave-2 spec (build-finish + falsify, 32 seats, policy v1 band 32-64).

The wave's one build item is the G6 class fix (23/27 -> 27/27 witnessed); the other 31
seats falsify what wave 1 and the L1 freeze produced: they re-run every counting command,
re-open every new source row, attack each claim's predicate/kill rules/harm guard, review
each new entry or tool, and mutation-test each new gate. Seat paths are absolute under the
lane repo; reportDir stays lane-relative for the validator. Every prompt leads with the
Godspeed directive bytes verbatim.
"""
import json
import os
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = ".ufo/waves/round-44/w2"
SCRATCH = "/fast/scratch/hyaku/kake-r44"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CTX = """# Goal
Kake round 44 wave 2 (build-finish + falsify, 32 seats). Lane: kake-shokunin (axes: operability, freshness; offline sitemap/manifest auditing, local CLI tools only). You are one leaf seat with one item; the L1 (kake-r44) is sole writer of lane history.

Lane repo: LANE_PH. Scratch: SCRATCH_PH/<YourSeatName>/ (create it; temp files there only).

# Round claims (context; do not re-declare)
- C1 (operability, capability): frozen counter v5 .ufo/waves/round-44/c44_count_v5.py + audit driver c44_audit.py must WITNESS all 27 controls in .ufo/waves/round-44/controls-27.tsv under --classes v5, while placebo c44_placebo.py witnesses only k/27 (k measured), held build rev 020bc457 meets v5 3/3, canaries 5/5 not met. Current state: 23/27 witnessed; G6 fails the four casememo controls (casememo-v3/v4/v7/v8) — the one open build item.
- C2 (freshness): scripts/ledger_latest_check.py --root . must exit 0 — last statement of each of 3 figures in LOG.md/SCORECARD.md equals receipt-derived values (receipts at master, uneditable).

# Frozen — never edit
.ufo/waves/round-44/c44_count_v5.py, c44_audit.py, controls-27.tsv, controls-r43/*, c44_placebo.py, .ufo/waves/round-43/* receipts, the 020bc457 build bytes. Class modules classes/gN_*.py are editable ONLY by the seat item that names one.

# Report
Write LANE_PH/WAVE_PH/<YourSeatName>.md: what you did, exact commands, verbatim decisive output, files written, blockers. Unrun check = reported unrun. Every `Report:` trailer path is relative to LANE_PH — write it at LANE_PH/<that path>.

# Bounds
You may write only: the lane paths your item names, your scratch dir, your report. Read-only: fleet repo /home/vgpnk/Projects/shokunin (except reading sibling lanes' cited files), sibling lane repos except paths your item names, .ufo/state/, watchdog logs. Never git commit/jj/push; never edit MANIFEST.json, templates/, fleet scripts/, route tables, mcp.json. Never `agent://all`. Tool installs authorized (official channels; record tool/version/channel/reason). PACMAN IS PAUSED host-wide: no pacman transactions; use uv tool/npx/~/.local/bin binaries. Report dead ends as dead ends; never fabricate.
""".replace("LANE_PH", LANE).replace("SCRATCH_PH", SCRATCH).replace("WAVE_PH", WAVE)


def item(name, role, axes, body):
    return {"name": name, "role": role, "axes": axes,
            "prompt": GODSPEED + "\n# Target\n" + body +
            "\n# Acceptance\nPaste the decisive command output into your report; state pass/fail "
            "against the item's named attack; name every file you wrote.\n"}


L = LANE
S = SCRATCH

items = [
    # ---- build-finish (1) ----
    item("ExecG6FoldFix", "executor", ["operability"],
         "Fix ONE file: " + L + "/.ufo/waves/round-44/classes/g6_fold_pairs.py (rewrite in place).\n"
         "# Change\n"
         "Current G6 witnesses 0/4 casememo controls (receipt .ufo/waves/round-44/verification/claim/after-v5.json "
         "rows casememo-v3/v4/v7/v8 have empty caughtBy; the audit txt lists them met=True caught=-). Read the four "
         "controls' memo blocks (grep 'CONTROL V' in .ufo/waves/round-44/controls-r43/casememo-*.py) and the layout "
         "contract in c44_count_v5.py (layout_f, segment_smu, foldpair handling). v3: validity memo under "
         "value.lower() for all values; v4: same but only values of at most 64 code points; v7: _parse_url memo "
         "under lower(), consulted only for non-ASCII values; v8: same under casefold(). A foldpair (a,b) is "
         "written [a,b] into one file with sitemapUrl=segment_smu(a) (a's first-segment directory, case-sensitive); "
         "ref41 flags b loc_out_of_scope when b's first segment differs by case from the sitemapUrl. Design shapes "
         "where each control's memo fires and differs from the round-41 reference: e.g. a pure case swap (KELVIN "
         "U+212A or long-s U+017F for ASCII k/s) in the FIRST path segment — ref41 flags b out_of_scope while a memo "
         "returning a's parse/validity answers in-scope; keep v4 pairs at most 64 cps; for v3 find where b's "
         "as-written verdict differs from the folded one (study _uri_ok_scan and the loc_out_of_scope checks near "
         "lines 313/534/539 of casememo-v3). Constraints: deterministic from rng only, stdlib only, no I/O, no env "
         "reads, no imports of control files (kill rule 4 circularity = C1 NOT MET); use helpers h.tok, h.fill, "
         "h.rcase, h.short_url, h.TLDS per the class-module contract in make_w1_spec.py header.\n"
         "# Self-test (never run the full counter)\n"
         "cd " + L + " && for c in casememo-v3-validity-lower casememo-v4-validity-lower-short "
         "casememo-v7-value-lower-nonascii casememo-v8-value-casefold-nonascii; do for s in 7 99; do "
         "python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file "
         ".ufo/waves/round-44/controls-r43/$c.py --seed $s; echo \"$c seed=$s exit=$?\"; done; done\n"
         "Required: exit 1 (witness) for all four controls on both seeds; then also seeds 1234 5555 777777 "
         "and paste results."),
    # ---- counting-command re-runs (4) ----
    item("ExecAfterBaseline", "executor", ["operability"],
         "Establish the wave-2 baseline of the claim's own receipt: cd " + L + " && python3 -B "
         ".ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv --counter "
         ".ufo/waves/round-44/c44_count_v5.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 "
         "--workers 4 --out .ufo/waves/round-44/verification/claim/after-v5-wave2-baseline.json > "
         ".ufo/waves/round-44/verification/claim/after-v5-wave2-baseline.txt 2>&1; echo exit=$?\n"
         "Attack: the L1's after-v5.json claims 23/27 + build 3/3. Your fresh unseeded run must reproduce 23/27 "
         "(the four casememo rows unwitnessed) or the original receipt is seed-luck: report your witnessed count, "
         "which rows differ, and all build# lines. ~5 minutes wall time."),
    item("ExecBeforePlacebo", "executor", ["operability"],
         "Re-produce C1's BEFORE receipt with frozen bytes: cd " + L + " && python3 -B "
         ".ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv --counter "
         ".ufo/waves/round-44/c44_placebo.py --classes v5 --expect witnessed --workers 4 --out "
         ".ufo/waves/round-44/verification/claim/placebo-before.json > "
         ".ufo/waves/round-44/verification/claim/placebo-before.txt 2>&1; echo exit=$?\n"
         "Attack: placebo must witness only k<27 (k measured, not targeted); if it witnesses 27/27 the classes are "
         "not doing the work. Report k, exit code, whether it equals the inherited receipt's 1/27, and which row."),
    item("ExecV4Support", "executor", ["operability"],
         "Re-produce the v4 supporting control: cd " + L + " && python3 -B .ufo/waves/round-44/c44_audit.py --root . "
         "--controls .ufo/waves/round-44/controls-27.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes v4 "
         "--expect blind --workers 4 --out .ufo/waves/round-44/verification/claim/v4-support.json > "
         ".ufo/waves/round-44/verification/claim/v4-support.txt 2>&1; echo exit=$?\n"
         "Attack: report the v4 met count j/27, which rows diverge on which v4 runs, and whether the two attempt-1 "
         "divergences (buildscope-m5 on run D, repeat-depth-deep on run C) reproduce with fresh seeds."),
    item("ExecCanary", "executor", ["operability"],
         "Re-produce the canary control: cd " + L + " && python3 -B .ufo/waves/round-44/c44_audit.py --root . "
         "--controls .ufo/waves/round-44/controls-canary.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes "
         "v5 --expect not-met --workers 2 --out .ufo/waves/round-44/verification/claim/canary.json > "
         ".ufo/waves/round-44/verification/claim/canary.txt 2>&1; echo exit=$?\n"
         "Attack: the five-row canary (4 r42 controls + junk) must be notMet 5/5. Report each row's met/witnessed "
         "state and the exact paths of the canary controls you inspected."),
    # ---- mutation tests (4) ----
    item("MutClassGate", "mutation-tester", ["operability"],
         "Mutation-test the witness gate in your scratch dir (copy .ufo/waves/round-44/c44_audit.py; never edit the "
         "lane file). (a) Original --selftest exits 0. (b) Four mutants on the copy: m1 revert semantic_witness to "
         "require EVERY caughtBy key be a class key; m2 accept timing-only witnesses; m3 treat a v4-run divergence "
         "as a class witness; m4 witness when any run errors. Each mutant's --selftest must exit nonzero. Attack: "
         "the frozen witness classifier must be able to fail. Paste each mutant's selftest exit code."),
    item("MutLedgerChecker", "mutation-tester", ["freshness"],
         "Mutation-test scripts/ledger_latest_check.py in your scratch dir (copy; never edit the lane file). (a) "
         "original --selftest exits 0. (b) mutants: m1 containment instead of exact equality; m2 first-match instead "
         "of last; m3 drop one figure from contract_spec; m4 accept a quoted value rounded differently from the "
         "receipt. Each must make the copy's --selftest exit nonzero. (c) In scratch, craft a fake LOG.md whose "
         "last build-range statement says T5 1.13-1.18 (the stale value, with EN-DASH) and show the original "
         "checker exits nonzero against a --root pointing at your scratch tree (read the checker's root handling "
         "first)."),
    item("MutG6Placebo", "mutation-tester", ["operability"],
         "Hypothesis: a placebo G6 delegating to cases_f would still witness casememo controls on some seeds by "
         "luck — proving G6 is not what does the witnessing. In scratch: copy c44_placebo.py and the classes dir; "
         "overwrite g6_fold_pairs.py cases() to delegate to the counter's cases_f generator (same unit kinds). Run "
         "c44_probe.py --class G6 --tool-file each casememo control --seed 1..20. Report per-seed exit codes; if "
         "any seed exits 1, name it so the G6 seat's witnesses can be checked for luck over the same seeds."),
    # ---- critics (4) ----
    item("CriticC1Predicate", "critic", ["operability"],
         "Attack C1's frozen predicate reading (SCORECARD round-44 'pre-freeze amendment A' + 'correction 2' "
         "predicate reading): 'a v4-corpus divergence is never a class witness, not a universal v4-blindness "
         "requirement'. Find a concrete reading under which a control diverging on BOTH a v4 run and a class run "
         "still satisfies the predicate yet defeats the capability's intent (counter v5 would catch it on v4 too). "
         "If found, state exactly which predicate sentence must change; else demonstrate by case analysis over the "
         "row fields (classCaught/legacyCaught) in .ufo/waves/round-44/verification/claim/after-v5.json."),
    item("CriticC2Repair", "critic", ["freshness"],
         "Attack C2's repairs before landing. Read .ufo/waves/round-44/verification/ledger-before.txt, "
         "scripts/ledger_latest_check.py, and derive from the master receipts yourself: (a) distinct toolSha256 "
         "count over .ufo/waves/round-43/verification/l1-rescores/*.json at master (git ls-tree + git show) — is it "
         "14? (b) T1/T5 ratios in freeze/ref41-base.json rounded to 2 decimals — 4.21/7.05? (c) extrema over "
         "freeze/build-1,2,3.json — exactly 1.00-1.01 / 1.11-1.22? (d) scan LOG.md and SCORECARD.md for any line "
         "that would match the repair phrases AFTER append and could supersede them. Report each derivation "
         "verbatim."),
    item("CriticKillRules", "critic", ["operability"],
         "Attack C1 kill rules 1-4 against committed bytes. (1) Each controls-27.tsv row's family/class vs its "
         "control source (grep the CONTROL block in controls-r43/*.py) — any misattribution left after the "
         "buildport-m6 fix? (2) Kill rule 2: any witness in verification/claim/after-v5.json that is timing-only — "
         "inspect per-row receipts under verification/tools/ for timing-channel vs equality divergence. (3) Kill "
         "rule 3: did any build run use fixed seeds or caches — inspect receipt fields. (4) grep all "
         "classes/gN_*.py for open(/import/read of controls-r43 paths — any circular class = C1 NOT MET."),
    item("CriticHarmGuard", "critic", ["operability"],
         "Attack the harm guard: C1 claims v4-mode semantics unchanged. Diff .ufo/waves/round-44/c44_count_v5.py "
         "against master:.ufo/waves/round-43/c43_count_v4.py (git show into a scratch file, then git diff --no-index "
         "or diff -u). Enumerate every hunk; confirm each touches only class-run dispatch (cases_gN wiring) and "
         "nothing in cases_f/layout_f/runs A-F/T1-T5. Any hunk inside v4 code paths = harm: name it."),
    # ---- reviewers (5) ----
    item("ReviewCounterContract", "reviewer", ["operability"],
         "Review .ufo/waves/round-44/c44_audit.py end-to-end as a contract instrument: does --expect "
         "blind/witnessed/not-met implement the SCORECARD predicates exactly? Trace: seed handling (unseeded = "
         "os.urandom?), per-row receipts, exit codes (0 ok / 1 predicate fail / 2 input error), the witness "
         "classifier (at-least-one class key), build-run semantics (three unseeded runs; met = equal 21/21 AND "
         "timing bound 2.0). File defects with line numbers; say 'no defects' only after tracing each predicate "
         "clause to code."),
    item("ReviewManifest", "reviewer", ["operability"],
         "Review .ufo/waves/round-44/controls-27.tsv against the round-43 settle prose (SCORECARD round-43 final "
         "correction): 27 controls by family (CtlHeadTail x5, CtlPortLen x3, CtlCaseMemo x4, CtlRepeat x5, "
         "CtlHostTable x3, CtlPortValue x2, CtlPrefixCache x1, 4 build mutants). Verify exactly those rows, each "
         "path exists under controls-r43/, each sha256 matches the on-disk file. Report extra/missing/mismatch."),
    item("ReviewWave1Reports", "reviewer", ["quality"],
         "Sample-review 6 wave-1 reports (.ufo/waves/round-44/w1/ExecG6Fold.md, ExecG1LongPort.md, CriticClaimC1.md, "
         "CriticMathDenominator.md, ScribeSources.md, RevengerControls.md): pick each report's load-bearing claim "
         "and re-run one command it pastes (probe, grep, or sha256). Any pasted output that does not reproduce = "
         "fabrication defect: name it with both outputs side by side."),
    item("ReviewScorecardR44", "reviewer", ["freshness"],
         "Review the uncommitted SCORECARD.md round-44 section (git diff SCORECARD.md) for internal contradiction "
         "across: original C1/C2 declarations, amendment A (placebo before-state), amendment B (C2 scope), "
         "correction 2 (three instrument fixes), the frozen predicate reading. Check: the quoted C2 counting "
         "command (must be --root . with no --spec), placebo sha256 pins, and the claim 'no receipt decided "
         "anything under the old classifier'. List contradictions with line numbers or state none found after "
         "tracing."),
    item("ReviewG6Semantics", "reviewer", ["operability"],
         "Independently derive the G6 witness shape BEFORE reading the fixed file's final bytes: from the four "
         "casememo control sources and the layout contract, write into your report the exact unit shapes (which "
         "segment carries the case swap, first vs later; ASCII vs KELVIN/long-s; pair length cap for v4; why each "
         "control's memo fires) that must witness each control. Then read classes/g6_fold_pairs.py as it stands at "
         "your runtime and state whether its shapes match your derivation (it may still be the pre-fix file — say "
         "so). This gives the L1 a wrong-reason-witness guard for the landed G6."),
    # ---- scouts (5) ----
    item("ScoutSiblingOverlap", "scout", ["adjacency"],
         "Sibling-overlap scan: grep the last 3 rounds of kumitate, tameshi, and kama lane repos "
         "(/home/vgpnk/Projects/shokunin/<lane>-shokunin/.ufo/waves/round-4*/ and SCORECARD tails) for work on "
         "differential-counter witness classes, ledger receipt re-derivation checkers, or witness-class gates. "
         "Report overlap with kake r44 C1/C2 and whether a shared SOURCES.md teaches row should cite it. Read-only; "
         "name every path you opened."),
    item("ScoutPatternPollution", "scout", ["freshness"],
         "Attack C2's regex approach: list every line in LOG.md and SCORECARD.md matching the three checker "
         "patterns ('re-scored N of the 27'; 'not met (T1 x, T5 y)'; 'T1 a\u2013b, T5 c\u2013d' with EN-DASH), with "
         "line numbers in file order. The L1's repair lines must become the LAST match of each pattern — identify "
         "any existing line (including this round's reports under .ufo/) that could accidentally match. Report the "
         "current last-match line per pattern."),
    item("ScoutSourcesVerify", "scout", ["freshness"],
         "Re-open the sources behind lesson rows S131/S132 (corpus/lessons/round-44.md gives exact paths): tameshi "
         ".ufo/waves/round-33/w1/CtlDoNothing.md and ReviewFreeze.md; kama "
         "corpus/knowledge/self-assessment-at-writing.md. Verify each quoted passage appears verbatim at the named "
         "section, first section-prose paragraph, and is at most 25 words. Report found/missing with the actual "
         "first paragraph you found."),
    item("ScoutRescoreCensus", "scout", ["freshness"],
         "Independently re-derive the rescore-tally figure: git ls-tree --name-only master "
         ".ufo/waves/round-43/verification/l1-rescores/ ; for each top-level *.json run git show master:<path>, "
         "extract toolSha256, count DISTINCT values; also count total top-level json files. Report both numbers — "
         "the checker's derive must equal your distinct count."),
    # ---- scribes (3) ----
    item("ScribeSourcesRows", "scribe", ["freshness"],
         "Append rows S131 and S132 to corpus/SOURCES.md exactly as specified in corpus/lessons/round-44.md "
         "section 'Superseding source rows' (copy the anchor and teaches cell text byte-exact from the two tables "
         "there), with status/used-by/recheck cells following the file's existing column shape and opened date "
         "2026-10-23. Then run /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "
         "/home/vgpnk/Projects/shokunin kake and paste exit code plus output tail. Do not edit any other row."),
    item("ScribeC2Repairs", "scribe", ["freshness"],
         "Draft (do NOT append to the ledgers) the three C2 repair paragraphs into one scratch file " + S +
         "/c2-repairs.md: (1) SCORECARD repair naming verification/l1-rescores receipts and the distinct "
         "toolSha256 count, containing the exact phrase 're-scored N of the 27'; (2) LOG repair containing 'not "
         "met (T1 4.21, T5 7.05)' naming ref41-base.json; (3) LOG repair containing 'T1 1.00\u20131.01, T5 "
         "1.11\u20131.22' (EN-DASH, matching the checker's regex) naming the build receipts. Each names the receipt "
         "file(s), the derived value, and the spot-check section repaired. Derive the values yourself from the "
         "master receipts (git show master:...) — never copy values from prose."),
    item("ScribeLessonMistake", "scribe", ["quality"],
         "corpus/lessons/round-44.md has an empty '## Mistakes' section. Read "
         ".ufo/waves/round-44/w1/CriticClaimC1.md and CriticMathDenominator.md first, then mine ONE mistake "
         "visible in this round's inherited evidence (e.g. the original v4 counter blind to 27 live-seat controls "
         "scored as a class instrument, or the buildport-m6 manifest misattribution). Write it as "
         "'N. class - evidence pointer - captured-by - fix' following the format of corpus/lessons/round-43.md "
         "entries; the fix must name the committed artifact that now prevents recurrence. Append under '## "
         "Mistakes'."),
    # ---- guards / others (5+4=9) ----
    item("SentinelScope", "sentinel", ["operability"],
         "Scope audit: git -C " + L + " status --porcelain — every modified/untracked path must be lane-authored "
         "round-44 work. Flag anything else. Verify frozen artifact sha256s: c44_count_v5.py = "
         "5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc, c44_placebo.py = "
         "9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27, c44_audit.py = "
         "8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75. Report each check. Note: the ExecG6FoldFix "
         "seat may legitimately modify classes/g6_fold_pairs.py during this wave; report the file's sha256 as you "
         "observe it."),
    item("RevengerLineage", "revenger", ["operability"],
         "Reverse-engineer the freeze lineage: run python3 -B .ufo/waves/round-44/build_v5.py --check and "
         "independently verify what --check compares (read build_v5.py). Separately diff the ten classes/gN_*.py "
         "against classes-placebo/gN_*.py: the ONLY differences must be inside cases() (placebo delegates to "
         "cases_f). Any other difference = undeclared capability smuggled into the freeze: name it. Also confirm "
         "placebo sha256 equals 9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27."),
    item("ScoutSeedStability", "scout", ["operability"],
         "One falsifiable hypothesis, read-only probes only: the G6 witness is seed-luck — a correct G6 witnesses "
         "each casememo control on fewer than 90 percent of seeds. First record sha256sum of "
         "classes/g6_fold_pairs.py. If the file still matches the pre-fix description in your wave context "
         "(witnesses 0/4), report BLOCKED with the sha256 and instead probe the CURRENT g6 over seeds 1..30, "
         "reporting the per-control witness rate as before-data. If the fix has landed, probe the fixed g6 over "
         "seeds 1..30 and report the witness rate per control with exact probe commands."),
    item("DistillerWave1", "reviewer", ["quality"],
         "Distill the 24 wave-1 reports in .ufo/waves/round-44/w1/*.md into a numbered attack ledger in your "
         "report only: one line per distinct finding (what it attacks, report pointer). Mark each finding already "
         "dispositioned by the SCORECARD pre-freeze amendments (manifest row fix, classifier fix, C2 command fix, "
         "C2 scope) vs still-open. This ledger is the L1's wave-2 evidence."),
    item("SimplifierAudit", "simplifier", ["operability"],
         "YAGNI review of .ufo/waves/round-44/c44_audit.py and scripts/ledger_latest_check.py: find dead code, "
         "unused flags, or receipt fields nothing consumes (trace consumers). Does --expect blind differ "
         "observably from --expect not-met? Is every --selftest fixture referenced by a kill rule? Propose "
         "deletions with line numbers — or state none, with the trace that justified keeping each branch."),
    item("SonicPins", "scribe", ["freshness"],
         "Mechanical pin check of the SCORECARD round-44 section (git diff SCORECARD.md): compute sha256 of every "
         "pinned file (counter v5 5cedaa3b..., placebo 9ce3acd4..., audit driver 8ee2c8bf..., build tool "
         "914ebdee..., any control pins) and report match/mismatch in a table."),
    item("ExecBuildMeet", "executor", ["operability"],
         "Attack the held build's 3/3 claim without editing the lane: create a 1-row controls TSV in your scratch "
         "dir (copy the buildscheme-M5 row from controls-27.tsv), then run c44_audit.py with --classes v5 --expect "
         "blind --build-rev 020bc457 --build-runs 3 --workers 1 --out <scratch>/buildmeet.json. Run it three times; "
         "twice under load (spawn 3 background CPU hogs: yes > /dev/null &). Report all build# lines verbatim and "
         "whether any timing ratio approaches the 2.0 bound."),
    item("CriticExploratoryCap", "critic", ["quality"],
         "Verify the round's claim cap: read the SCORECARD round-44 section and confirm the round declares exactly "
         "two measured claims and zero exploratory claims (so the at-most-one-exploratory rule is not strained). "
         "Then attack the 'sourced claim' rule: C1 cites S129 and C2 cites S130 as re-opened this round — check "
         "that corpus/lessons/round-44.md's Gate section records their re-opening with URL/path, access date "
         "2026-10-23, and quotes of at most 25 words, and that the SCORECARD 'Sourced.' lines name rows that exist "
         "in corpus/SOURCES.md. Report any missing link in the citation chain."),
]

assert len(items) == 32, len(items)
spec = {"wave": "kake-r44-w2", "milestone": "round-44 wave 2 (build-finish + falsify)",
        "maxLanes": 64, "axes": ["operability", "freshness"], "reportDir": WAVE,
        "context": CTX, "items": items}
os.makedirs(".ufo/waves/round-44", exist_ok=True)
with open(".ufo/waves/round-44/w2-spec.json", "w") as fh:
    json.dump(spec, fh, indent=1)
print("items:", len(items))
print(Counter(i["role"] for i in items))
