# ReviewerContract

Scope: `.ufo/waves/round-59/contract.md` + `contract.json` as a whole, against the round-59 prompt §2/§6 item 9/§10.
Read-only: lane HEAD `cb68527`, contract commit `45a92b64ac8a0f82dba369100e30682f14de81fb`, base `fd6303ce5c14b3f892dec586297a942ab6e4193b`
(= contract commit's parent, = round-58 spot-check). Scratch `/fast/scratch/hyaku/kake-r59/ReviewerContract` removed; no lane
mutation (reads, `git show/log/ls-tree/status`, counter runs only). Working tree was live during review (wave-1 seats were editing
the counters: shas moved from the pinned v1 values between two `sha256sum` calls), so §"live drift" statements are timestamped
facts about the tree at review time, not claims about the committed contract.

FINDINGS:

**F1 HIGH — the frozen predicate sentence is already broken in the tree, and contract.json has no amendment slot.**
At the contract commit all three ties hold byte-for-byte (verified): contract.md == contract.json == counter `PREDICATE` ==
base-receipt label — C1 `met: mismatches == 0 AND rows == 3 AND scores_held == 2 AND superseded_kept == 3`, C2
`met: cases_passed == 21 of 21`, C3 `met: conditions_passed == 9 of 9`; and `counterSha256v1` in contract.json equals the sha256 of
the three committed blobs (`95d23511…`, `ca2e85c6…`, `b3aef90c…`). But the working tree has already moved:
`c59_axis_evidence.py` is now `1d04f19d…` (then `b6c1b21b…`) with `PREDICATE = "met: mismatches == 0 AND tables == 1 AND rows == 3
AND scores_held == 2 AND superseded_kept == 3"`, `c59_quote_truth.py` `52cd698c…` (pinned `b3aef90c…`), `c59_resolver_cases.py`
`90c431bf…` (pinned `ca2e85c6…`). Contract.md's own first paragraph requires the sentence to be the same "here, in the counter's
code and in every receipt label", so any landing of these files as-is violates the frozen contract; and because the C1 amendment
adds a predicate atom (`tables == 1`) and changes a condition's semantics, the *rule* changes, not just the implementation.
Fix: before any seat scores, land one amendment commit in the round-58 shape — `predicateV2`, `counterSha256v2`, `baseReceiptV2`
per claim in contract.json plus a contract.md "version 2" section carrying the new sentence verbatim; keep v1 pins untouched.

**F2 HIGH — the stated C1 before-value no longer describes the counter that is being amended.**
contract.md C1 says `Before (base): mismatches=16 unresolved=11 rows_no_receipt=3 receipts_off_axis=0 tallies_unfound=0
rows_no_tally=2 rows=3 scores_held=2 superseded_kept=0 met=False`, exit 1, and the committed receipt plus a re-run of the *committed*
v1 counter reproduce exactly that (byte-identical). The amended working-tree counter at the same base revision produces
`mismatches=21 … tables=1 tallies_unfound=4 rows_no_tally=3`, exit 1 — because v2 counts a tally only when it occurs in a cited
*receipt* instead of any cited blob, and tightens receipt qualification. Receipt rule: a re-run lands under a new file name.
Fix: commit `base-c1-axis-evidence-v2.txt` (and C2/C3 equivalents where their semantics moved — C3's C9 placement and C2's
selftest), and restate the "Before (base)" line against the counter version that will be scored.
Sharpest consequence of the in-tree C1 v2 draft (measured by reading the tree file while wave 1 edited it): its receipt scope is
`base_sections` filtered to `n < MEASURED_ROUND`, so a receipt under `.ufo/waves/round-59/` is off-axis by construction — the round's
own after-receipts can no longer be cited as C1 evidence; the axis cells must cite a *round 58 or earlier* receipt whose base-revision
section names the axis (round 58's section does: `| Claim | Axis | …` with cells `calibration`, `operability`,
`freshness (sourced: S423, S424)`). contract.md's C1 "After" does not say this. Any v2 landing must state it, or fix the filter.

**F3 MEDIUM — C1's declared predicate omits an enforced conjunct (`names_ok`), in v1 and in the v2 draft.**
`measure()` computes `met = mismatches == 0 and rows == 3 and names_ok and scores_held == 2 and superseded_kept == 3`
(c59_axis_evidence.py:254 v1, :314 in the tree), where `names_ok` requires the three rows named exactly
operability/freshness/calibration in that order. The frozen sentence says only `rows == 3`, and the receipt label prints only the
sentence, so a closure re-deriving "met" from the label can disagree with the exit code (e.g. three rows in another order).
Prompt §6 item 9 requires the sentence, the code condition and the receipt label to be one thing.
Fix: either drop `names_ok` from `met` or state it in the sentence (both contracts, both keys, all receipts).

**F4 MEDIUM — C3's contract wording ("tail") contradicts the counter's placement rule; the trap is live.**
contract.md C3: "an append-only `[r59-correction 2026-10-27]` tail in `crawler-identity.md` citing S425". The counter's C9 requires
the inserted line adjacent to the stale bullet: v1 `s < i1 <= s + 1 + STALE_WINDOW` (within 8 base lines after line 31), v2
`i1 == end` (exactly where the bullet ends — the base bullet spans lines 31–34, so an EOF insert is ~40 lines away). Measured in a
scratch clone of the lane: inserting the tagged correction at end of file → `C9_stale_claim_corrected FAIL — no inserted line
within 8 base lines after the stale sentence carries [r59-correction 2026-10-27]` (plus the two dependent notes). A builder
following the word "tail" lands a red.
Fix: state the placement in contract.md ("inserted immediately after the stale bullet's last line, before the next bullet; ≤8 base
lines after the sentence") and name which counter version governs it.

**F5 MEDIUM — C1's after-state forces the six `/tmp/kake-r17/…` and `cli.mjs:935` pointers back into SCORECARD.md verbatim.**
`superseded_kept == 3` counts base evidence cells that still occur verbatim *outside* the axis table; the base operability cell
carries `cli.mjs:935` + three line continuations, the freshness cell carries six `/tmp/kake-r17/…` files and `corpus/claims`.
The contract discloses the retention, but not its consequence: the committed SCORECARD will again contain paths that prompt §7.5 and
the lane's own QUALITY.md:611 call non-citable, which a QUALITY reviewer can read as a §7.5 defect even though the counter's pointer
scan only reads axis-table cells. Fix: say in the contract that the retained cells are historical, non-citable text kept outside the
axis table, and say where they live and that no gate treats them as evidence.

**F6 MEDIUM — C2's separability claim covers only the `ids_cited` floor; P7 is also a whole-lane corpus check.**
Contract: "C2 reads only scripts/id_resolver.py and gate-built fixtures (P7 reads the lane's registry/knowledge, floor
ids_cited >= 106, which holds with or without C3's rows)." P7's actual condition is `rc == 0 and ids_cited >= 106 and dangling == 0`
at the measured revision (c59_resolver_cases.py P7 block; base receipt `ids_cited=108 … dangling=0`). `dangling == 0` is a property
of the whole lane corpus, which C3 mutates (two entries citing S425/S426, two registry rows, a S425 citation in
crawler-identity.md). A partially landed or inconsistent C3 turns P7 red and fails C2's 21/21 for a reason outside C2's surface.
Fix: state the coupling and the measurement order (measure C2 at a revision where the registry/knowledge pair is self-consistent,
or before C3's entries land), as round 58 declared its C1 admission coupling.

**F7 MEDIUM — C1 can be met with the calibration score unchanged (or lower); the lowest-axis move is unmeasured.**
`HELD = ("operability","freshness")`; nothing in the predicate reads the calibration score, and contract.md's C1 "After" says only
"operability/freshness scores unchanged". The claim is the round's lowest-axis obligation (calibration 2, base SCORECARD line 19),
yet a green C1 is compatible with calibration staying at 2 — or being lowered — because `mismatches` counts cell matter only.
Fix: state the expected calibration delta (e.g. 2 -> 3) and add the atom, or declare explicitly that C1 is a bounded integrity
improvement with a 0 score delta (round-58 wording) and that no score drop is permitted.

**F8 MEDIUM — the C3 append cannot be validated the way the round's recipe says; C7 requires a materially larger mirror.**
C7 demands, at the measured revision, `assimilation/validate/{census-argv,census-stdout,census-exit}.txt`, a validate registry
byte-equal to the *landed* registry and per-entry copies, with `census-exit.txt == exit=0`, no E03/E04, and the *last* stdout line
exactly `file<TAB>ok<TAB><path>` — i.e. zero E-level findings, not merely zero E03/E04. The census resolves every row's `used-by`
against the mirror root (E11). Measured here with the current registry: corpus/ only → 16 E11; corpus/ + SCORECARD.md + SKILL.md +
corpus/lessons/ → still 7 E11 (rows naming `scripts/source_recheck.py` and `.ufo/waves/round-41/{c1_count,oracle_crosscheck}.py`) and
no `file ok` tail → exit 1 → C7 red. r58's committed `validate/` tree shows the same shape (it carries `.ufo/waves/round-41/*`,
SCORECARD.md, SKILL.md). contract.md's C3 never says this.
Fix: one contract line naming the required mirror content ("every path any row's used-by names, plus corpus/ and the root docs"),
so the builder does not stop at corpus/.

**F9 LOW — the round's own base control receipts qualify as C1 "on-axis receipts".**
v1 receipt qualification is `^\.ufo/waves/round-(\d+)/` + the round section naming the axis. Everything under
`.ufo/waves/round-59/controls/` (including `base-c1-axis-evidence.txt`, which records the red before-state and contains `117/117`
inside its tallies list) matches, so an axis cell can cite a before-state receipt and quote a tally that merely occurs in it.
partially disclosed ("whether a cited receipt supports the score (reviewer-checked)") but not in this shape.
Fix: exclude `controls/base-*` from receipt eligibility (v2 already narrowed tallies to receipts; add the name filter).

**F10 LOW — access date 2026-10-27 (UTC) is coherent but creates a future-dated row against the local round date.**
Fetch receipt `2026-10-27T01:21:22+00:00`; local (-03:00) is `2026-10-26T22:21`. Contract declares the UTC date for every row,
Gate line, `verified-at:` and the correction tag, and C3 enforces it (C3 row `opened`, C2 `verified-at:`, C5 Gate line, C6
`stamp.date() == ROUND_DATE` with `+00:00`) — internally consistent, and the UTC convention is what prior rounds' receipts carried
(r57/r58 fetches were 22:02Z/23:35Z and their `opened` equals the UTC date, which there also equals the local date). Residual: the
census's E08 ("opened not a past/present ISO date") compares against `TODAY=${TODAY:-$(date -u +%F)}` (scripts/sources-census.sh:91)
and fires on `opened_epoch > today_s` (:661-662), so a default run passes once UTC passes midnight, while any validator pinned at
`--today 2026-10-26` (the round's local date) reads both new rows as E08 future-dated → exit 1 [code-read, not executed with that
`--today`].
Fix: contract states the convention and that validators must use the UTC day (or `--today 2026-10-27`) for this round.

**F11 LOW — "162 rows" is attributed to a receipt that holds no row count.**
contract.md Frontier: "SOURCES census at round start: exit 0, 162 rows, 14 W04 (`controls/census-before.txt`)". That file holds 14
W04 lines + `kake<TAB>ok<TAB><path>` and `census-before.exit` holds `exit=0`; the count 162 is evidenced elsewhere
(`assimilation/reg-ids` = 162, `mirror-pin.json` rows 162, base registry 162 S-rows). Fix: point at `mirror-pin.json`/`reg-ids`.

**F12 LOW — D3/quarantine hold is honest but the §10 verdict duty is left implicit.**
Verified: the 12-row slice file is committed with exactly 12 rows (S142 S143 S148 S154 S156 S161 S178 S184 S193 S194 S195 S206);
the round-58 L0 line exists (`.ufo/l0-questions.md:180`) and carries no answer (the only `L0 ANSWER` marks in the file belong to
kama r11 / tsukuroi r12), so "no answer → nothing appended → routed around, not treated as answered" matches prompt §5 and the
run-8 "never treat an L0 as answered" rule; kake is not in the prompt's wave-4 quarantine-first list, and §10's quarantine clause
gates appendability, so appending nothing is conformant. Gap: the contract does not say whether the 12 rows were re-hand-checked
this round and where the verdicts land (r58 recorded per-row verdicts in its lesson; §10 says verdicts land in lesson and report).
Fix: one line — "slice unchanged, not re-checked this round, r58 verdicts stand, L0 open, nothing appended".

**F13 LOW — stale comment inside the frozen C2 counter.** The P6 block is commented "version 2: floor 55"; the constant is
`P6_FLOOR = 66` and contract.md quotes 66. A reader trusting the comment misjudges the P6 requirement by 7 cases. Same file's
`# P6 … a printed tally is still not proof the cases ran` is the disclosed hollow-tally limit and is correctly disclosed in the
contract's "What the counter does not test". Fix: correct the comment in the v2 amendment.

VERDICT: The frozen triple is honest at commit 45a92b6 — predicate sentence identical in contract.md, contract.json, each counter's
PREDICATE and each base receipt label; `counterSha256v1` pins the committed counters; all three base receipts reproduce
(C1 byte-identical 16 mismatches/exit 1, C2 13/21 with exactly K8–K14+P6 red at seed 59, C3 0/9), and the derive scripts regenerate
the counters byte-identically; mirror bytes == base registry (sha256 ecb5ced…) with the collision/renumber evidence consistent
(reg 162, staged 129, the 8 named collisions, S398→S425 by matching URL) — but the contract needs an amendment commit before any
score: F1/F2 (the tree counters have already changed the C1 predicate sentence, the sha pins and the C1 before-value, with no
`predicateV2/counterSha256v2/baseReceiptV2` slot), plus the wording/atom fixes F3–F8.
