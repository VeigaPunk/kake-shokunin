#!/usr/bin/env python3
"""Round-51 wave-1 spec generator.

Emits `.ufo/waves/round-51/w51-spec.json` — one v1 wave of 48 seats under
`scripts/hyaku/ufo-wave-policy.json` (band 32-64). The L1 holds the planner seat;
attack roles (reviewer, critic, mutation-tester) are 25 of 48 seats.
Every item names one concrete verification or attack on the two frozen claims
(`.ufo/waves/round-51/contract.json`) or on the round's frontier step.

Usage: python3 -B make_spec_w1.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
BASE = "007d66e4e8360a5f88d29a93eeedd8066dad4434"
TIP = "9d13768c4fdd0e9a2688d2ecf1616b539cf57658"
REPORT_DIR = f"{LANE}/.ufo/waves/round-51/w1"

DIRECTIVE = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can be run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""


def context() -> str:
    return f"""# Goal
Kake round 51, wave 1: a 48-seat batch. The L1 holds the planner seat (a frozen-topology role is never a swarm seat).
The two claims were declared and frozen BEFORE any score in `{LANE}/.ufo/waves/round-51/contract.json`:

  C1 (operability, capability acquisition) — a wave-evidence ledger that re-derives the round's own
     seat accounting, route deviations and time accounting from committed bytes.
     Predicate: `met: ledger_checks_passed == 3 of 3`.
     Counting command: `python3 -B {LANE}/.ufo/waves/round-51/c51_wave_ledger.py --root {LANE} --revision <commit>`
  C2 (freshness, sourced learning claim) — Google's canonical selection and crawler identity enter
     held ground as two entries on rows S262 and S263, re-grounded this round.
     Predicate: `met: conditions_passed == 8 of 8`.
     Counting command: `python3 -B {LANE}/.ufo/waves/round-51/c51_quote_truth.py --root {LANE} --revision <commit>`

Base (do-nothing) revision: {BASE}
Lane tip at wave dispatch: {TIP}
Lane root: {LANE}
Fleet root: {FLEET}

# Measured state at dispatch
`c51_quote_truth.py --revision {TIP}` prints `C2 quote-truth 8/8 met=True`, exit 0.
`c51_wave_ledger.py --revision {TIP}` prints `C1 ledger 0/3 met=False`, exit 1 — the wave evidence
(settlement, route map, probe receipts, timing, accounting) does not exist yet; the L1 writes it
after this wave settles. Your job is to verify or attack what the committed bytes prove, not to
author the wave evidence.

# Report (mandatory)
Every `Report:` trailer path the dispatcher renders is relative to {LANE} — write it at
{LANE}/<that path>. Concretely, each item names its own absolute report path; write exactly that
file and nothing else in the lane.

# Bounds
Read-only except your own report file. Never mutate the fleet repo, a sibling lane, the lane jj
state or the lane Git index. Do not run `git add`, `git commit`, `git stash`, `git checkout`,
`git switch`, `git reset`, `git pull`, `git push`, or any mutating `jj` command. Read-only git
(log, show, diff, status, ls-files, rev-parse, merge-base, cat-file) is fine. Scratch goes under
`/tmp` only. Never edit `{LANE}/considerthese/` (operator-authored input). Never edit
`{LANE}/.ufo/waves/round-46/residual/` or the >1MiB copies under
`{LANE}/.ufo/waves/round-48/assimilation/validate/`.
External read-only: `{FLEET}/../shokuknow/merge/kake/` and
`{FLEET}/../shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`. Never write there,
never run a campaign tool there.

# Tooling authorization (operator, 2026-10-19)
You may install or upgrade tools that help the task — read `/home/vgpnk/.omp/agent/RULES.md` first
(official channels, update-safety gate, record tool/version/channel/reason in your report).
Pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide.
Install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or file an L0 question. Never
`-Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host service.

# Honesty
An unrun check has not passed. Report what the commands actually printed, including failures.
Name any file you could not read. Do not repeat another seat's conclusion as your own evidence.
"""


ITEMS: list[dict] = [
    # ---- scout (per-surface reconnaissance) ----
    dict(name="ScoutCensusBefore", role="scout", axes=["freshness"],
         item=("Run the frozen census command read-only: "
               "`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`. "
               "Record the exact argv, stdout, stderr and exit code, and the registry row count it reports. "
               "Do not modify the registry.")),
    dict(name="ScoutCounterC1Base", role="scout", axes=["operability"],
         item=(f"Run `python3 -B {LANE}/.ufo/waves/round-51/c51_wave_ledger.py --root {LANE} --revision {BASE}` and record the "
               "full stdout and exit code. State which of L1/L2/L3 fail and the exact note each prints. This is the "
               "do-nothing control for C1.")),
    dict(name="ScoutCounterC2Base", role="scout", axes=["freshness"],
         item=(f"Run `python3 -B {LANE}/.ufo/waves/round-51/c51_quote_truth.py --root {LANE} --revision {BASE}` and record the "
               "full stdout and exit code. State which conditions fail. This is the do-nothing control for C2.")),
    dict(name="ScoutCounterC2Tip", role="scout", axes=["freshness"],
         item=(f"Run `python3 -B {LANE}/.ufo/waves/round-51/c51_quote_truth.py --root {LANE} --revision {TIP}` and record the "
               "full stdout and exit code. Independently re-check one of the eight conditions by hand (name which) so the "
               "8/8 is not taken on the counter's word alone.")),
    dict(name="ScoutQuarantineSlice", role="scout", axes=["freshness"],
         item=("Read-only: re-derive the lane's slice of `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` "
               f"with the awk filter in the round prompt and compare it with the committed `{LANE}/.ufo/waves/round-51/assimilation/quarantine-slice`. "
               "Report the row count, whether every line carries an S-id, and list every S-id. Adopt nothing.")),
    dict(name="ScoutMisroot", role="scout", axes=["operability"],
         item=("Run `git -C /home/vgpnk/Projects/shokunin status --porcelain` with no pathspec. For every untracked path, say whether "
               "its content names kake or round-51 (read the file; do not guess from the name). Report the classification table. "
               "Touch nothing.")),
    # ---- connector (sibling-overlap scan) ----
    dict(name="ConnectorSiblingOverlap", role="connector", axes=["operability", "freshness"],
         item=("Scan the sibling lanes' committed round-50/round-51 material under "
               "`/home/vgpnk/Projects/shokunin/{kumitate,kotoba,kotodama,tabi,revenger,chousa,souji,mado,kasegi}-shokunin` "
               "(git log/show only) for a wave-evidence ledger, a route-probe receipt shape or a canonical/crawler-identity "
               "knowledge entry that kake round 51 duplicates or contradicts. Name each overlap with path and line; say "
               "`none found` with the command you ran if there is none. Do not write in any sibling repo.")),
    # ---- executor (writes or runs code) ----
    dict(name="ExecLedgerMutants", role="executor", axes=["operability"],
         item=(f"Copy `{LANE}/.ufo/waves/round-51/c51_wave_ledger.py` into `/tmp/r51-mut-l1/`. If the committed wave evidence (settlement, route map, "
               "timing, accounting) is not on disk yet, construct the minimal passing fixture the counter's own code requires under "
               "`/tmp` and say you did; then run at "
               "least five mutants against the C1 counter and record the exit code and note for each: (a) a settlement whose "
               "`reports_written` is inflated by one, (b) a settlement with one seat marked `report: true` but no file, "
               "(c) a route receipt whose `httpStatus` is a string, (d) a used route with `ok: false`, (e) an accounting "
               "artifact whose `wall_clock_seconds` differs by one from the timing pair. Every mutant must be rejected "
               "(exit 1) with a named note. Write only under `/tmp` and your report path.")),
    dict(name="ExecQuoteCounterMutants", role="executor", axes=["freshness"],
         item=(f"Copy `{LANE}/.ufo/waves/round-51/c51_quote_truth.py` and the committed corpus bytes into `/tmp/r51-mut-l2/`, then run at least "
               "five mutants and record exit code plus failing condition for each: (a) swap the two Gate quotes between S262 "
               "and S263, (b) corrupt one retained body's sha256 in the receipt, (c) drop one id from a row's `used-by`, "
               "(d) make one registry row 12 cells, (e) point the receipt URL at the other row's URL. Every mutant must be "
               "rejected (exit 1). Write only under `/tmp` and your report path.")),
    dict(name="ExecCensusMirrorValidate", role="executor", axes=["freshness"],
         item=(f"Rebuild the pre-append census check from committed bytes: copy `{LANE}/corpus/` to `/tmp/r51-mirror/`, remove the two adopted rows, "
               f"run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/r51-mirror/SOURCES.md` and record argv/stdout/exit. "
               "Then confirm the committed mirror output at `.ufo/waves/round-51/assimilation/pre-append/` names `--file` and not `--root`. "
               "Report whether the two agree.")),
    dict(name="ExecRowShape", role="executor", axes=["freshness"],
         item=(f"Parse `{LANE}/corpus/SOURCES.md` with the census parser's own 0-to-3-leading-space pattern and report, for S262 and S263: "
               "cell count, whether any cell holds a literal or escaped pipe, status, opened, recheck, and the `used-by` value. "
               "Then state whether the two rows would parse as eleven cells.")),
    dict(name="ExecSourceDigest", role="executor", axes=["freshness"],
         item=(f"Recompute sha256 over `{LANE}/.ufo/waves/round-51/sources/S262.html` and `S263.html`, compare with `sources/receipts.json`, and report "
               "each body's byte size, digest match, and the receipt's URL. Flag any mismatch as a defect.")),
    dict(name="ExecQuoteRawScan", role="executor", axes=["freshness"],
         item=(f"For every quote in `{LANE}/corpus/knowledge/canonical-selection.md` and `crawler-identity.md`, classify it against the retained body of the "
               "row the entry cites: raw substring, whitespace-collapsed-only, or absent. Write a small script under `/tmp` and "
               "report a table (entry, quote head, class). An `absent` quote is a defect; name it.")),
    dict(name="ExecRegistryDiff", role="executor", axes=["freshness"],
         item=(f"Prove the registry append is append-only: diff `git -C {LANE} show {BASE}:corpus/SOURCES.md` against the tip file at the row level and report "
               "the added row ids, the removed row ids and the count of changed pre-existing rows. Any changed pre-existing "
               "row is a defect; name it with the id.")),
    dict(name="ExecAccountingPrototype", role="executor", axes=["operability"],
         item=(f"Build a `/tmp` fixture settlement/timing pair whose wall clock is a known integer and whose aggregate and dead-seat seconds are known, then "
               f"run `{LANE}/.ufo/waves/round-51/c51_wave_ledger.py` L3 logic against it (import the module or copy the function) and report "
               "whether it accepts and whether it rejects the same fixture with the wall clock off by one. Report the exact "
               "numbers used.")),
    dict(name="ExecSpecLint", role="executor", axes=["operability"],
         item=(f"Validate the round's own dispatch payload once it exists: read `{LANE}/.ufo/waves/round-51/w51-taskcall.json` and report seat count, "
               "unique-name check, role histogram, whether every item text names an absolute report path under "
               f"`{REPORT_DIR}`, and whether the band 32-64 holds. If the file does not exist yet, lint `{LANE}/.ufo/waves/round-51/w51-spec.json` "
               "instead and say which file you linted.")),
    # ---- scribe (prose) ----
    dict(name="ScribeEntryAudit", role="scribe", axes=["freshness"],
         item=(f"Read `{LANE}/corpus/knowledge/canonical-selection.md` and `crawler-identity.md` as prose. For each entry list every sentence that asserts "
               "more than its cited row supports, and every quote whose class label does not match a raw scan you ran yourself. "
               "Propose append-ready wording in your report; do not edit the entries.")),
    dict(name="ScribeLessonShape", role="scribe", axes=["freshness"],
         item=(f"Read `{LANE}/corpus/lessons/round-51.md` and the lesson contract in `/home/vgpnk/Projects/shokunin/LEARNING.md`. List every required section "
               "that is absent, every section present but empty, and whether `## Gate` carries at least one admit and one "
               "reject with reason and flip. Name line numbers.")),
    dict(name="ScribeSourcesCells", role="scribe", axes=["freshness"],
         item=(f"Read the SOURCES.md registry schema in `/home/vgpnk/Projects/shokunin/CORPUS.md` and the two new rows for S262/S263. For each cell, quote the "
               "schema rule and the row's value side by side, and name any cell whose value would violate a rule a reader can "
               "check by eye (dates, cadence, tier, status vocabulary). No edits.")),
    dict(name="ScribeReportSources", role="scribe", axes=["freshness"],
         item=(f"Using only committed bytes, draft the `Sources & frontier` paragraph the round report needs: census before and after "
               "(argv + exit), rows added by tier, rows touched old-to-new, frontier rows advanced, and the at-least-one-sourced-claim "
               f"statement naming S262/S263. Write the draft under `/tmp` and reproduce it in your report; the L1 owns the real report.")),
    # ---- reviewer ----
    dict(name="ReviewC1Predicate", role="reviewer", axes=["operability"],
         item=(f"Read `{LANE}/.ufo/waves/round-51/contract.json` C1 and the `PREDICATE` constant plus docstring in `c51_wave_ledger.py`. Report whether the "
               "same sentence appears in both, whether the threshold is 3 of 3 in both, and whether the counter's three checks "
               "match the three condition sentences L1/L2/L3 word for word. Name any divergence with line numbers.")),
    dict(name="ReviewL1Accounting", role="reviewer", axes=["operability"],
         item=("Adversarially read `check_l1` in "
               f"`{LANE}/.ufo/waves/round-51/c51_wave_ledger.py`. Construct, on paper, a settlement and report set that passes L1 while "
               "attesting a wave that never ran. If one exists, name the missing guard precisely; if none exists after your "
               "attempt, name the guard that blocks each attempt you tried.")),
    dict(name="ReviewL2Routes", role="reviewer", axes=["operability"],
         item=("Adversarially read `check_l2`. Report: can a failing probe receipt be used by a role without failing? can a "
               "receipt omit its excerpt and still pass? can a role's alias be absent from every receipt? Name each guard and "
               "the line that implements it, or the hole.")),
    dict(name="ReviewL3Time", role="reviewer", axes=["operability"],
         item=("Adversarially read `check_l3`. Report whether the wall clock is re-derived from the timing pair or copied from the "
               "accounting artifact, whether every figure the accounting carries is cross-checked, and whether a dead seat can "
               "record an impossible duration. Name lines.")),
    dict(name="ReviewC2Conditions", role="reviewer", axes=["freshness"],
         item=(f"Read the eight conditions in `{LANE}/.ufo/waves/round-51/c51_quote_truth.py` and the eight sentences in `contract.json`. Match them one to one; "
               "name any condition the code does not implement, or any code check the contract does not declare.")),
    dict(name="ReviewEntryScope", role="reviewer", axes=["freshness"],
         item=(f"Apply `{LANE}/PROVINCE.md` to each of the two admitted entries: does the ground belong to kake's core or frontier, or to a sibling "
               "lane (tabi for crawler discipline, chousa for method, kagi for secrets)? Give a per-entry verdict with the "
               "PROVINCE line that decides it.")),
    dict(name="ReviewQualityBar", role="reviewer", axes=["freshness"],
         item=(f"Apply `{LANE}/corpus/QUALITY.md` to each entry and to the lesson. List every criterion the round's artifacts meet, and every criterion that "
               "is not met or not evidenced, with the criterion's own wording.")),
    dict(name="ReviewAppendOnly", role="reviewer", axes=["freshness"],
         item=(f"Verify the round's own append-only discipline over committed bytes: compare `{LANE}/corpus/SOURCES.md`, `SCORECARD.md` and `LOG.md` between "
               f"`{BASE}` and `{TIP}` and report, per file, the count of removed or rewritten lines that are not part of a new "
               "section. A rewritten historical line is a defect; name it with its text.")),
    dict(name="ReviewReportContract", role="reviewer", axes=["operability"],
         item=("Read `/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-51.md` section 4 and produce a checklist of the six required "
               "report sections with the exact heading text and what evidence each needs. Say which sections the round's "
               "committed artifacts can already support and which need a measurement that does not exist yet.")),
    dict(name="ReviewShonen", role="reviewer", axes=["operability"],
         item=(f"Read `{LANE}/SHONEN.md` and report one line per box: the box text, what evidence would mark it `[x]`, and the evidence that exists now "
               f"at `{TIP}`. Mark `[x]` only where a named non-author verifier exists, `[~]` where a pointer exists, `[ ]` otherwise.")),
    # ---- critic ----
    dict(name="CriticZeroControl", role="critic", axes=["operability", "freshness"],
         item=("Falsify the do-nothing controls. Run both counters at the base and at the tip, then argue whether a round that "
               "committed nothing but the wave evidence could still reach C1 3/3, and whether a round that copied the retained "
               "bodies without opening the URLs could reach C2 8/8. Name the guard that blocks each, or the hole.")),
    dict(name="CriticTautology", role="critic", axes=["operability"],
         item=("Attack C1 as self-attestation: the L1 authors the settlement the counter then certifies. Decide whether any check "
               "in the ledger is independent of a number the L1 typed, and say which. If every figure is self-authored, say so "
               "plainly and name the cheapest independent cross-check the lane could add next round.")),
    dict(name="CriticStaleRows", role="critic", axes=["freshness"],
         item=(f"The rows carry `opened 2026-10-24` while this run is 2026-10-25. Decide whether that is a defect under CORPUS.md rule 1 as written, "
               "and whether the Gate's access dates match the commit dates of the commits that carry them. Give the ruling and "
               "the rule text you relied on.")),
    dict(name="CriticQuarantine", role="critic", axes=["freshness"],
         item=("Attack the quarantine handling: the slice was re-derived and adopted nothing. Is an unadopted slice acceptable "
               "under the round prompt's quarantine clause, or does the clause require a verdict per row this round? Quote the "
               "clause and give your ruling.")),
    dict(name="CriticHarm", role="critic", axes=["operability", "freshness"],
         item=(f"Attempt to show an owned axis is harmed by this round's committed changes. Run the standing gates a reader can run "
               f"(`node {LANE}/scripts/freshness-sweep.mjs --selftest`, `python3 -B {LANE}/scripts/citation_lint.py --root {LANE}`, "
               f"`python3 -B {LANE}/scripts/ledger_latest_check.py`) and report each exit code. Name any harm, or say none observed "
               "with the exits you got.")),
    dict(name="CriticCapability", role="critic", axes=["operability"],
         item=("Argue both sides of whether C1 is a capability acquisition or instrumentation theater: what can the lane now do "
               "that it could not do at the base, and what does the ledger not prove about a wave. Give a verdict with the "
               "strongest counter-argument stated fairly.")),
    dict(name="CriticAbsence", role="critic", axes=["freshness"],
         item=(f"Attack every proof-by-absence in the round's artifacts: name each claim that rests on a file being absent at the base, and say what a "
               "later reader would need to re-check it. Report at least three such claims with their commit.")),
    dict(name="CriticIds", role="critic", axes=["freshness"],
         item=(f"Attack the id-collision evidence: the staged package's S273, S274 and S286 overlap the lane registry and were not adopted. Is the overlap "
               "resolved or merely noted? What breaks if a later round adopts the staged rows under those ids? Name the "
               "scratch evidence you relied on.")),
    dict(name="CriticGateCriterion", role="critic", axes=["freshness"],
         item=(f"Read the `## Mistakes` block in `{LANE}/corpus/lessons/round-51.md`. Decide whether its fix is testable — can a command show the fix able "
               "to fail? If not, propose the command. Give a ruling on each mistake row.")),
    dict(name="CriticShape", role="critic", axes=["operability"],
         item=("Read the round prompt's section 2 wave-shape options and the lesson's declared shape. Decide whether one v1 wave of "
               "48 seats plus a residual call satisfies the named default shape, and whether a second 32-seat wave is required "
               "when wave 1 yields fewer than 32 distinct attack items. Give the ruling and the clause.")),
    # ---- mutation-tester ----
    dict(name="MutationDropReport", role="mutation-tester", axes=["operability"],
         item=(f"In `/tmp`, copy the C1 counter and build (or copy, if it now exists) the minimal passing wave-evidence fixture, then delete one seat report "
               "file and re-run the L1 check. Report the exact note and exit code. The mutant must be rejected; if it is accepted, the L1 guard "
               "is broken and you must say so.")),
    dict(name="MutationSwapIds", role="mutation-tester", axes=["freshness"],
         item=("In `/tmp`, swap the S262 and S263 rows' `used-by` cells and re-run C2. Report which condition fails and its note. "
               "The mutant must be rejected.")),
    dict(name="MutationWallClock", role="mutation-tester", axes=["operability"],
         item=("In `/tmp`, build (or copy) the minimal passing fixture, change the timing pair's `settledAt` by 60 seconds without touching "
               "the accounting artifact, and re-run C1's L3. Report the note and exit. The mutant must be rejected.")),
    dict(name="MutationRoute", role="mutation-tester", axes=["operability"],
         item=("In `/tmp`, build (or copy) the minimal passing fixture, flip a used route's receipt to `ok: false` keeping the excerpt, and "
               "re-run C1's L2. Report the note and exit. The mutant must be rejected; if it is accepted, name the hole.")),
    dict(name="MutationSourceSha", role="mutation-tester", axes=["freshness"],
         item=("In `/tmp`, alter one byte of a retained body (keeping the receipt) and re-run C2. Report the failing condition "
               "and exit. The mutant must be rejected.")),
    # ---- sentinel / revenger / simplifier ----
    dict(name="SentinelWriteScope", role="sentinel", axes=["operability"],
         item=("Security-review the wave's write scope: list every path a seat was permitted to write, then check the lane and "
               "fleet worktrees for any file outside that set with a round-51 mtime. Report the out-of-scope writes and the "
               "commands you used. Do not delete anything.")),
    dict(name="RevengerR50", role="revenger", axes=["operability"],
         item=("Re-derive the round-50 routed defects r50-1..r50-4 from the committed round-50 material "
               f"(`{LANE}/.ufo/waves/round-50/`, `{LANE}/corpus/lessons/round-50*.md`, the fleet report "
               "`/home/vgpnk/Projects/shokunin/.ufo/reports/round-50/kake.md`) and state, per defect, whether round 51's "
               "committed artifacts address it, partly address it, or leave it open. Quote the defect text you relied on.")),
    dict(name="SimplifierCounters", role="simplifier", axes=["operability"],
         item=(f"Attempt to delete code from `{LANE}/.ufo/waves/round-51/c51_wave_ledger.py` and `c51_quote_truth.py` that no condition needs, and name "
               "each deletion candidate with the lines it covers and whether the frozen predicate still evaluates the same. "
               "Do not edit the committed files; work on a `/tmp` copy. Report dead code or `none found`.")),
]


def main() -> None:
    items = []
    for entry in ITEMS:
        report = f"{REPORT_DIR}/{entry['name']}.md"
        text = entry["item"] + f" Write ONLY {report}"
        items.append({
            "name": entry["name"],
            "role": entry["role"],
            "axes": entry["axes"],
            "item": text,
        })
    names = [i["name"] for i in items]
    assert len(set(names)) == len(names), "duplicate seat name"
    spec = {
        "wave": "kake-r51-w1",
        "milestone": ("Round 51 wave 1: verify and attack the two frozen claims (the wave-evidence ledger "
                      "and the two assimilated entries) plus the frontier step"),
        "maxLanes": len(items),
        "axes": ["operability", "freshness"],
        "reportDir": ".ufo/waves/round-51/w1",
        "context": context(),
        "template": DIRECTIVE + "\n\n{{item}}",
        "items": items,
    }
    out = os.path.join(HERE, "w51-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    roles: dict[str, int] = {}
    for i in items:
        roles[i["role"]] = roles.get(i["role"], 0) + 1
    print(f"wrote {out}: seats={len(items)} roles={roles}")


if __name__ == "__main__":
    main()
