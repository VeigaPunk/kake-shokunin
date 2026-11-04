author: hyaku closure (non-author integrator, @m_opus)

# Round 36 — verifier spot-check (kake)

Non-author closure of kake round 36. Report `.ufo/reports/round-36/kake.md` (fleet `12fe0694`),
prompt `.ufo/prompts/kake-round-36.md` (fleet `c655100`). Lane base
`b720d799ae99c19a7c97f2b1391d4fe928be0e11`, tip `1a16b8e3faebcd24718c2cde6bf0c04b4c09cc59`.
Driver digest (copied from `.ufo/watchdog.log`, mutable):
`2026-10-22T22:02:55-03:00 launch kake round=36 pgid=3654558 driver=hyaku-inline attempt=1` ·
`2026-10-22T23:35:58-03:00 complete kake round=36; hyaku-inline attempt=1`.
Read-only closure seats: `C1Receipts`, `PredicateIntegrity`, `PromptConformance`, `GateAdmits`,
`GateRejects`, `HarmAndContainment` (reviewer/critic). No lane gate, counter or selftest was
executed (PROTOCOL §Gate standard, Closure consequence): C1 is **evidence-verified** against
committed receipts plus plain re-derivations (sha256, jq, git, census); nothing ran in the lane.

## Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-36/kake.md` | `kake-shokunin 12fe0694c18edca60b1d1a590d07e54d93d2d464` (23:35:36-03:00, after tip 23:34:07) | ok |
| `## SHONEN`, one line per box | report lines 109–114 vs `git show 1a16b8e3:SHONEN.md` | 4 boxes, 4 lines (`[~] [~] [~] [ ]`), no `[x]` | ok |
| Cited commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for b720d799, 3555f63f, 9d81c75c, cd321279, 4d5b3d55, fd1fb723, e5a293b6, f3a38bf8, 25f84872, 1a16b8e3 | all `anc-master` | ok |
| Cited `bf9b2089` | `git cat-file -t bf9b2089` | `Not a valid object name`; `git bundle list-heads retained/r36-l1-postfix-remeasure.bundle` → `bf9b2089… refs/heads/postfix` | defect (orphaned hash, lives only in a committed bundle; post-measurement repair, counts toward no claim) |
| Lane pushed, clean | `jj-lane.sh state …` ; `git status --porcelain` | `local=remote=1a16b8e3… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | ok |
| Prompt carries template contract | canonical `templates/round-prompt.md` render vs prompt (seat `PromptConformance`) | §§1–5 incl. §2b and hyaku §6 verbatim; round-level items and five child-lane items present; no L2 route map quoted; prompt committed 2 s before launch | ok |
| Seat count | first-timestamp census of `KakeR36/*.jsonl` in the host session dir | 7 control + 36 wave-1 + 34 wave-2 = 77 | matches report |

Status: real report with checkable commits → `ok`.

Defects (status-neutral, routed below): orphaned `bf9b2089` citation; declaration base hash typo
at `3555f63f` (`b720d79976a1…`, names no object; disclosed and corrected by append, mistake row 1);
containment — two wave-1 executors (`ExecCriterionAblation` → `criteria/ablation_floor_check.py`,
`ExecCriterionControlTree` → `criteria/control_tree_check.py`) wrote into the lane although
`w1-spec.json` restricted lane writes to reports (sha256 matched sandbox copies; committed at
`e5a293b6` and reviewed in wave 2 — recovered, but a scope breach); the report's "no fleet-root
file carries this lane" needs qualifying (` M .ufo/state/kake.report-baseline` is driver runtime,
not lane work).

## Claims (step 2)

One claim. **C1 — freshness (capability): `scripts/source_recheck.py`; frozen predicate
`met: passed >= 25 of 28 sealed cases`.** Evidence-verified (lane-owned counter; not executed).

### Freeze timeline (the counter changed twice, the case set once)

| Event | Commit time (committer) | Remote landing (L1 transcript `landed` line) |
|---|---|---|
| declaration + counter v1 + key v1 `3555f63f` | 22:20:56-03:00 (author date 20:54:59, a jj change-creation artifact) | by 01:20:59Z |
| counter v2 (bubblewrap jail) `9d81c75c` | 22:24:43-03:00 | by 01:24:45Z |
| control wave dispatched (7 seats) | — | 01:22:45Z |
| key v2 + counter v3 `cd321279` | 22:33:53-03:00 | by 01:33:56Z |
| **first wave-1 seat dispatched (`ExecToolBuild` 01:34:22.447Z)** | — | host `KakeR36/*.jsonl` first timestamps; lane `w1-dispatched-at.txt` agrees |
| build `4d5b3d55` | 22:54:39-03:00 | by 01:54:41Z |

Both counter changes and the key change landed before any build seat existed (26 s margin).
Counter diffs (seat `PredicateIntegrity`, `diff <(git show A:p) <(git show B:p)`): v2 adds jail,
dependency checks, fixed interpreter; v3 changes only `KEY_SHA256` (`a690d39e…` → `44c94838…`)
plus comments; neither touches the predicate text, threshold 25, total 28, or the comparison.
`git diff cd321279 1a16b8e3 -- .ufo/waves/round-36/sealed_count.py` → empty.

Key v2 changed the case set after the control seats had scored under key v1 (CtlShortcut 17 of
28). Prompt §6 item 9 says "a rule changed after any seat has scored is not the claim's rule".
The claim does not rest on it: the same build meets under the original rule too (below). Key v2
also loosened one defect class (`w2/CriticKeyV2Change.md`: an HTML-only casefold defect 24 → 26);
recorded as a routed note, not a harm.

### Re-derivation

| Measurement | Command (mine or seat's, read-only) | Observed |
|---|---|---|
| Before at b720d799 / 3555f63f / 9d81c75c / cd321279 | `git show 1a16b8e3:.ufo/waves/round-36/verification/{c1-keyrev-at-b720d799,control-declaration,control-counter-v2-commit,c1-keyrev-at-cd321279}.json \| jq '{revision,passed,met}'` + `.exit` | 0/28, met false, exit 1 at each named revision; `git ls-tree b720d799 -- scripts/source_recheck.py` → empty |
| After at 4d5b3d55 (counter v3, key v2) | `jq '[.perCase[]\|select(.passed==true)]\|length'` on `c1-keyrev-at-4d5b3d55.json` | 28 (0 false, 28 unique ids); met true; exit 0 |
| Original rule (counter v1, key v1) | `c1-counter-v1-keyv1-at-4d5b3d55.json` | 28/28, met true, exit 0; counter digest `28169d95…` = `git show 3555f63f:.ufo/waves/round-36/sealed_count.py \| sha256sum` |
| Counter v2, key v1 | `c1-counter-v2-keyv1-at-4d5b3d55.json` | 28/28, met true, exit 0; digest `1bf16734…` = `9d81c75c` bytes |
| Case pins | `git show fd1fb723:.ufo/waves/round-36/sealed/cases{-v1,}.json \| sha256sum` | `a690d39e…` (v1/v2 pin), `44c94838…` (v3 pin): match |
| Tool identity | `git show 4d5b3d55:scripts/source_recheck.py \| sha256sum` | `577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48` = receipt and report |
| Reveal refused | `c1-keyrev-at-fd1fb723.exit` | 2 ("key visible at the measured revision") |
| Tip tool vs measured | `git diff 4d5b3d55 1a16b8e3 -- scripts/source_recheck.py` | +6 lines (realpath symlink containment); tip sha `3e5457a9…` = `c1-postfix-at-bf9b2089.json` 28/28 — post-measurement, counts toward nothing |
| Controls, final counter | `jq -s` over `verification/control-Ctl*.json` | constant clean 0, all-false 0, no-reader 8, naive reader **12**, shortcut 9; all met false; ablations 13–24 |
| Selftest tally | commit subject `4d5b3d55` + `w2/ReviewSelftest.md` | 101/101 exit 0 (fixture f08 corrected by L1, disclosed) |
| Independent blind reference | `independent-selftest-reference.json` | 28/28 (seat reference sha `a5176fee…` = `retained/independent/selftest-seat-reference.py`) |

**Does the frozen predicate depend on the overstated design statement?** No. The predicate is
`cases == 28 and passed >= 25` (`sealed_count.py` `PREDICATE`); the sentence "each of the 34 rule
ablations … fails at least the four cases of its bullet" (`3555f63f:SCORECARD.md`) was the
*rationale* for choosing 25, not a term of the predicate. It held for the L1's listed reference
ablations (13–24 of 28, committed before any build) but was overstated as a property of any
implementation: `w2/MutTool.md` — 9 of 32 single-point tool mutants still meet 25 (M07, M08, M13,
M20, M24, M26, M28, M31, M32; seven of them at 28), `w2/RerunAblations.md` 5 of 6 new reference
mutants meet. The correction was appended (`git diff 3555f63f 1a16b8e3 -- SCORECARD.md`: 87
additions, 0 deletions) with no change to threshold, total, case set or counter. Consequence: the
claim is met as declared, but "28 of 28" does not certify every contract rule — BOM-mark retention
(M24) survives both the sealed set and the selftest. That limits the capability row's wording,
not the measured move.

**Junk control without receipt.** Material to evidence completeness, not to the floor: the
prompt's duty is "the cheapest control that skips the claimed work" — constant clean (0) and
all-false (0) are that, with receipts; `sealed_count.py` rejects non-JSON output, so a junk
emitter cannot pass a case [INFERENCE from code read]. The lesson should say junk was *untested*.

C1: **verified** (before 0 → after 28 of 28, met under counters v1, v2 and v3; frozen before the
first build seat; no control above 12).

### Axis harm

`git diff b720d799 1a16b8e3 -- SCORECARD.md`: 192 additions, 0 deletions; operability 10 → 10,
freshness 10 → 10, no axis row changed; one capability row added ("Offline source re-check
audit", evidence receipt landed at `e5a293b6` before the row at `f3a38bf8`). `git diff --numstat
b720d799 1a16b8e3`: 251 paths, no deletions (LOG, lessons, SOURCES, QUALITY append-only).

| Axis | Verdict | Reason |
|---|---|---|
| freshness | improved | C1 verified: a re-check instrument where none existed (0 → 28 of 28) plus a first live re-check of 90 Gate quotes |
| operability | unchanged | score 10 → 10; not claimed |
| depth | unchanged | not claimed; no score change |
| coverage | unchanged | not claimed |
| calibration | unchanged | overstatements (design sentence, "2 real moves") caught and corrected by append in-round; not claimed |
| adjacency | unchanged | not claimed |

## Discernment spot-check (step 3)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S088 RFC 9110 | admit, A, mined | https://www.rfc-editor.org/rfc/rfc9110.html#section-15.4.2 (live, seat `GateAdmits`); retained `sources/S088.html.gz` `gunzip \| grep -cF 'has been assigned a new permanent URI'` → 2 | agree | normative 301 semantics; quote 10 words, found at §15.4.2 as stated |
| S090 WHATWG Encoding | admit, A, mined | https://encoding.spec.whatwg.org/ (live, by me: `grep -o 'A byte order mark has priority over a label'` → match; `Last Updated 2026-10-19` as anchored) | agree | 9-word quote at §8.1.1; grounds BOM precedence |
| S091 UAX #15 | admit, A, mined | https://www.unicode.org/reports/tr15/ (live, `GateAdmits`) | agree with admit; location defect | 10-word quote found live, but at §7 Design Goals item 2, not the stated §1.2; revision 18.0.0 matches |
| S093 Wikipedia HTTP 301 | reject, C | `https://en.wikipedia.org/w/index.php?title=HTTP_301&action=raw` (live, by me: `grep -c 308` → 0; line 6 cites RFC 2616 §10.3.2; line 4 carries the quote) | agree | tertiary restatement of superseded RFC; 8-word quote verbatim; row lacks the `flip:` form |
| S094 MDN Redirections | reject, B | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Redirections#principle; RFC 9110 §15.4.1, §15.4.5 (live, `GateRejects`) | agree (qualified) | Principle's blanket "redirects carry Location" is overbroad vs 300 SHOULD / 304; 7-word quote verbatim. "Contradicts" overstates: §15.4.5 omits Location, it does not forbid it. L1 rejected against the scribe's admit draft (`w1/ScribeSourcesRows.md:6–7`) |

New `corpus/SOURCES.md` row re-opened: S088 (above), ≤25-word quote verified (10 words).
Rows 87 → 94 (`git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
at b720d799 / 1a16b8e3); malformed rows 0.
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → three `W04`
same-URL-across-scopes warnings (S033, S088, S092), `kake ok`, exit 0.

## Trend verdicts

- **expansion: improved** — capability "Offline source re-check audit" admitted to
  `SCORECARD.md ## Capabilities` on a verified demonstration (28 of 28, real-input run); five
  mined A-tier rows on ground the registry did not hold (redirects, URI resolution, encoding,
  normalization, HTML syntax). No knowledge entry admitted.
- **quality: improved** — first quote-level re-verification of the registry: 90 Gate quotes
  recorded and audited (`realrun/audit.json` 14 findings → `audit-run2.json` 8, each
  dispositioned in `SOURCES.md` notes); round-35 corrections (S084, Preferred-Languages) appended.
  No admitted entry left false or stale unmarked. Wording nit: S040/S068 were already-documented
  redirects, re-verified, not newly found moves.
- **discernment: improved** — the spot-check agrees with the gate on 3 admits and 2 rejects; the
  pre-freeze control wave caught key-v1 body-blindness before any build; QUALITY round-36 (a)–(f)
  each cite a lesson, (a)–(e) with red-before receipts.

## Routed defects (the lane must address them next round)

1. Orphaned citation: `bf9b2089` is not an object in the lane history (only in
   `retained/r36-l1-postfix-remeasure.bundle`); cite it with its bundle path or land it.
2. Containment: two wave-1 executors wrote into the lane outside their report path; next round's
   wave context must make the sandbox the only deliverable path, the L1 copies after review and
   checks `git status` before integrating.
3. Capability-row and claim wording: "meets the public contract (a)–(g)" overstates what 28 of 28
   certifies — seven single-point mutants also score 28 (`w2/MutTool.md`), M24 (BOM mark kept)
   survives selftest too; add sealed or selftest cases for the surviving rules, append a limit line.
4. Key v2 was changed after control seats scored; it also loosened the casefold class (24 → 26,
   `w2/CriticKeyV2Change.md`). Future key repairs must keep the original-key measurement as the
   claim's rule of record (this round's build met it, so no verdict change).
5. Junk control: record it as *untested* (lesson "Holds", SCORECARD wave-2 corrections say it as
   if it ran: "No … junk … control met 25"); re-run a junk control on a non-filtered seat next round.
6. Gate lines: S091 quote location is §7 Design Goals, not §1.2; S093 `teaches` lacks `flip:`;
   S094 reason should say "overbroad" not "contradicts" for 304; `used-by` of S088–S092 names
   `scripts/source_recheck.py`, while CORPUS contract v1 asks for knowledge-entry or lesson paths.
7. QUALITY (f) has no polarity-specific red-before receipt (the shortcut 17 → 9 rescore is not a
   criterion check); (d) `control_tree_check.py` passes a root listing over a tree holding a sealed
   key (`w2/ReviewCriteriaChecks.md:40–53`); (a) lacks the bare-id-only negative receipt.
8. Carried tool defects (lesson "Carried open"): attribute-embedded `<script` truncation, FIFO and
   huge manifests, `body_path` check-then-open race, counter D1/D2 crashes, jail case-directory
   visibility, 18 undecided contract points.

SHONEN note for the operator: boxes 1–3 point to committed, non-author-checkable artifacts (SKILL
registry rows, LOG round 36 + `realrun/`, wave-2 re-runs from the written commands); box 4
(PROVINCE) is unassessed. Promotion is operator-owned.
