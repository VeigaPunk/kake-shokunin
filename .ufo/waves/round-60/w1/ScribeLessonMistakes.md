# ScribeLessonMistakes

Scope: draft `## Mistakes` rows for `corpus/lessons/round-60.md`, one red-before command per fix as the L1 will run
it, and the carried-limits block. Every pointer resolves at base `97cdc122379711c2b02a8970752c8782da3ac81d`
(`git show 97cdc12:<path> | sed -n '<line>p'`, read-only). This seat executed no counter and scored no after-state;
the c55 and c59 receipts cited below are committed files, quoted from their bytes, not re-runs. Line numbers marked
`(at ab6e100e)` / `(at b322cca)` are read from that commit, not from base.

## MISTAKES:

Table to paste under `## Mistakes` in `corpus/lessons/round-60.md`. Class column uses the `CORPUS.md` vocabulary
(`vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`,
`provider`); the round-59 informal name is kept in parentheses so the two rounds cross-read.

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| stale-premise (round 59 called it "gate-collision") | `corpus/knowledge/crawler-identity.md:35` carries `**[r59-correction 2026-10-27]**` — a mid-entry run, `git diff --numstat fd6303ce 97cdc12 -- corpus/knowledge/crawler-identity.md` → `16 0` (pure insertion) — while the round-55 gate's `head_changed` term requires the whole base blob to survive as a byte prefix (`.ufo/waves/round-55/c55_readme_index.py:30-31` doc; `:199` `if not new.startswith(old)`). At build `ab6e100e` the gate printed `C1 readme-index index_mismatches=1 knowledge_files=58 met=False`, `head_changed: crawler-identity.md`, `EXIT=1` (`.ufo/waves/round-59/a2r1/ReviewerNoHarm.files/out-c55.txt`, revision `ab6e100e442046006fa039315f5bd33bb516940b`). The gate's own selftest only ever appends at EOF (`pass_entry_appended_correction`, `c55_readme_index.py:330`), so no case of its own could see an inside-entry run. Predicted before data (`w1/ExecHistoricalGates.md:80`, H1) and not recorded in the round-59 contract. | none at the time; the non-author no-harm reviewer found it after build (`a2r1/ReviewerNoHarm.md`). Criterion now at `corpus/QUALITY.md:1350` (landed `b322ccab`: "a frozen claim never silently turns a standing gate red"). | C2: a lane tool whose append-only rule accepts one visible tagged in-file correction and still catches rewrites/deletions — `scripts/append_guard.py`, scored by `c60_guard_cases.py` (24 cases). The round-55 rule ported as a control must fail K2 (tagged mid-file run), K15 (`a,"",b` → `a,TAG,"","",b`) and R1 (the real round-59 correction), and pass R2 (one changed base byte). |
| scope (round 59 called it "counter-scope gap") | `.ufo/waves/round-59/c59_axis_evidence.py:67` `HELD = ("operability", "freshness")`; `:315-318` iterates `HELD` only; `:334` requires `res["scores_held"] == 2`; `PREDICATE` at `:62` and the rendered row `SKILL.md:1307` both read `scores_held == 2`. A scratch mutant commit `d64dd96e74a51945d2638be1184b0b12dcb1327a` moving only the calibration score 2 → 10 still printed `mismatches=0 … scores_held=2 superseded_kept=3 met=True`, exit 0 (`.ufo/waves/round-59/a2r1/CriticCountersV2.md:5`, remedy at `:15`). The claim is that the axis-table evidence cells match committed state; the one score the claim's own axis owns sat outside the counter's scope. | none: the selftest case `score_change_on_held_axis` covers held axes only (`a2r1/CriticCountersV2.md:5`); the predicate was frozen and could not be amended after data. | C1 term `scores_held == 3` (operability 10, freshness 10, calibration 2 — `SCORECARD.md:17-19`), with a selftest mutant that moves only calibration 2 → 10 and must fail. |
| reference-drift (round 59 called it "row precision") | `corpus/SOURCES.md:171` (row S425) `scope` cell (5th cell, byte offset 415 of the row) claims "the three crawler categories and their robots.txt posture"; the cited page gives a robots.txt posture for common crawlers and the AdsBot special case only, and none for user-triggered fetchers (`round-59-verifier-spotcheck.md` §2, "agree, with a row defect"). No superseding row existed at base: `git show 97cdc12:corpus/SOURCES.md \| grep -cE '\| S42[789] \|'` → 0, registry 164 rows. | none for the cell: no rule tests a registry `scope` cell against the categories the cited page actually states; the outside year-end spot-check caught it. | S427 (re-open of the S425 URL, `teaches` opening `supersedes S425 —`, scope without the phrase and with `common crawlers` / `special-case crawlers`) plus S428; condition `C3_row_shape` in `c60_quote_truth.py`. |
| survivor (the class behind the three above: a gate's status label not re-derived after the round's own change) | At build `ab6e100e` the registry row (`SKILL.md:1233` at that tree) reads Kind `gate (offline, committed bytes only; no network)` — live — while the gate exits 1 on that same tree (receipt above, revision `ab6e100e…`). The `historical` label and its pin `64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` land only at `b322ccab` (`git log -S'gate (historical from round 59' -- SKILL.md` names `b322cca`, the round's measured revision), i.e. after the reviewer, not after the change. The same shape is live at base on another row: `SKILL.md:213` (`c53_gate_truth.py`, Kind cell `gate` = live) while the contract's base probe reads exit 1 (contract §C1 "Before"), and `SKILL.md:1274` (`id-resolver-gate`, live) whose entry command carries the optional `[--fleet <fleet root>]` that must be kept — dropped, it becomes a false `live_not_green` at exit 2. | none: the gate registry had no re-derivation step; the criterion at `corpus/QUALITY.md:1350` binds a contract to run non-historical gates on a draft, it does not bind the label to the observed exit each round. | C1's per-member label re-derivation (`live_not_green`, `historical_but_green`, `historical_not_green_at_pin`, `never_met_but_green`), run over the 28-member population every round; c55's `historical` label is now covered by the pin run (`e_P == 0` at `64c0ce1`, an ancestor of base). |

Class-mapping note, worth one line under the table: `CORPUS.md` carries no `gate-collision` or `counter-scope gap`
class; the three round-59 labels map to `stale-premise` (a rule whose premise a later practice invalidates), `scope`
(a claim wider than its check), `reference-drift` (a cell that does not say what its source says), and the shared
label-drift class to `survivor` (the label outlived the round that invalidated it and had to be re-derived by hand).

## RED-BEFORE:

Each block is the fix's red state as the L1 will run it. `<lane>` = `/home/vgpnk/Projects/shokunin/kake-shokunin`,
`<scratch>` = `/fast/scratch/hyaku/kake-r60/<L1>`, `R=97cdc122379711c2b02a8970752c8782da3ac81d`. Exact label spelling
for the two counters written this wave is `[INFERENCE]`; their case ids, exit codes and predicates are frozen by the
round-60 contract and are quoted from it.

**RB-1 — C2 guard (row 1).**
(a) Base red, already committed, not re-run by me:
`git -C <lane> show $R:.ufo/waves/round-59/a2r1/ReviewerNoHarm.files/out-c55.txt`
→ `C1 readme-index index_mismatches=1 … met=False` / `head_changed: crawler-identity.md` / `EXIT=1` at `ab6e100e`.
(b) Do-nothing control, L1 runs after the wave-1 build:
`cd <lane> && python3 -B .ufo/waves/round-60/c60_guard_cases.py --root . --revision $R --work <scratch>`
→ expected `cases_passed=0 of 24`, exit 1 — at base there is no tool to run (`git cat-file -e $R:scripts/append_guard.py` fails).
(c) The c55-rule control (the "shown able to fail" evidence), same counter, port substituted for the tool: expected
`cases_passed=21 of 24`, exit 1, `failures=K2,K15,R1` — the tagged mid-file run, the alignment case and the real
round-59 correction all read as findings, while R2 (a one-byte change to a base line of
`corpus/knowledge/crawler-identity.md` committed in the scratch clone) passes under the port. Guard direction:
R1 exit 0, R2 `changed corpus/knowledge/crawler-identity.md`, exit 1.

**RB-2 — C1 `scores_held == 3` (row 2).** Mutant in a scratch clone (never in the lane):
```
D=$(mktemp -d -p <scratch>) && git clone -q --shared <lane> "$D/lane" \
  && git -C "$D/lane" checkout -q $R \
  && sed -i '19s/| calibration | 2 |/| calibration | 10 |/' "$D/lane/SCORECARD.md" \
  && git -C "$D/lane" -c user.name=selftest -c user.email=selftest@local commit -qam mutant \
  && python3 -B "$D/lane/.ufo/waves/round-60/c60_gate_status.py" --root "$D/lane" --revision HEAD
```
Line 19 is the calibration row (`SCORECARD.md:15-19`). Expected: `scores_held=2` of 3, one mismatch naming the
calibration cell, `met=False`, `EXIT=1`. Contrast, observed: the round-59 predicate on the same mutant printed
`scores_held=2 … met=True`, exit 0 (`a2r1/CriticCountersV2.md:5`). Base do-nothing: the same counter with
`--revision $R` on `<lane>` → `mismatches>=13` (contract §C1 before), `met=False`, exit 1.

**RB-3 — S427/S428 + C3 `C3_row_shape` (row 3).**
`cd <lane> && python3 -B .ufo/waves/round-60/c60_quote_truth.py --root . --revision $R`
→ expected `C3 quote-truth 0/9 met=False` with `C1_entries_exist FAIL` (both entries absent at base:
`git cat-file -e $R:corpus/knowledge/google-user-triggered-fetchers.md`,
`…:corpus/knowledge/robots-txt-limits.md`, `…:corpus/knowledge/google-robots-txt-limits.md` all fail) and
`C3_row_shape FAIL` (S427–S429 absent; the S425 scope cell still holds the phrase), `EXIT=1`. Print shape is the
round-59 one (`c59_quote_truth.py:1755-1761`: summary line, one `  <check> FAIL` per condition, `EXIT=<code>`);
condition labels `[INFERENCE]`.

**RB-4 — C1 live-label re-derivation (row 4).**
`cd <lane> && python3 -B .ufo/waves/round-60/c60_gate_status.py --root . --revision $R`
→ expected `met=False`, exit 1, with a `c53_gate_truth.py` mismatch classified `live_not_green` (Kind `gate` at
`SKILL.md:213`, contract base probe exit 1) among the 12 unregistered members (contract §C1 before: c48 ×2, c49 ×2,
c50 ×2, c51 ×2, c52_gate_registry, c52_mutation_ladder, c54 ×2). The run must stay green for `id-resolver-gate`
(`SKILL.md:1274`): its `[--fleet <fleet root>]` segment is kept with the placeholder substituted, so the label is
not falsely red on exit 2.

## CARRIED:

R59-D3 stands as carried in the round-60 contract (§Routed defects, third bullet) and is not claimed by any round-60
claim. Recorded here so the next round inherits it with its pointers:

- **C2 P6 — printed-tally trust.** `c59_resolver_cases.py:280-286` accepts a minimum printed tally, not the case
  inventory; the critic shrank the real selftest 72 → 71 and P6 still passed
  (`.ufo/waves/round-59/a2r1/CriticCountersV2.md`, NEW DEFECTS "C2 P6 verifies a minimum printed tally").
- **C2 fixture-sniff composite.** A resolver that returns canned green when the root's parent is not named `fleet`
  still scored 21/21, exit 0, in scratch commit `b58b83ab232691d710a187d916f20943297ee8fa`
  (`a2r1/CriticCountersV2.md`, C2 bullet).
- **Q1–Q8.** The eight proposed resolver cases and their measured holes are tabulated at
  `.ufo/waves/round-59/w1/MutC2Gate.md:156-163` (Q1 non-Markdown knowledge file, Q2 fence info string, Q3 default
  fleet root, Q4 prefix-sharing symlink, Q5 prefix-sharing registry symlink, Q6 self-verified tally, Q7 URL ending in a
  backtick, Q8 symlink-to-symlink); the extended counter measured 27/29 where the frozen one measured 21/21
  (`MutC2Gate.md:165-167`).

Reason for carrying rather than fixing: the contract allows one operability claim per round and this round's is R59-D1
(C2 is the append guard); round-60 C2 reads only `scripts/append_guard.py`, its 24 gate-built fixtures and the lane
history `fd6303ce..rev`, so the resolver's P6 tally surface, its fixture sniff and Q1–Q8 are unreachable by any
round-60 claim — widening the guard to cover them would be a second operability claim, which the contract forbids.
R59-D3's third item, C3's footer `Last updated` read, is **not** carried: the round-60 C3 condition C5 requires the
date inside `<devsite-content-footer`, which is the fix.

VERDICT: four rows drafted (stale-premise, scope, reference-drift, survivor), each with a base-resolving pointer and a red-before command the L1 runs; R59-D3 P6/fixture-sniff/Q1–Q8 carried with reason, C3 footer fixed forward.
