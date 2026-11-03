# Round 73 — lessons (kake, attempt 1)

Base `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc` (lane master at round open). Frozen contract
`.ufo/waves/round-73/contract.md` at freeze `4c7c53bc563a66ae0676b468966781f023ae0110` (predicates, base
controls and the attack corpus frozen before any seat ran; pre-freeze diagnosis disclosed in the contract).
Wave `w1`: 11 seats, one v1 wave, band 8–16 (scout 2, executor 3, reviewer 2, scribe 1, critic 1,
mutation-tester 1, connector 1; attack share 4/11; the L1 held the planner role). All 11 seats settled
(`.ufo/waves/round-73/w1-results.json`).

Claims: C1 calibration (lowest owned axis, score 2), C2 operability (score 10, HOLD), C3 freshness
(score 10, HOLD).

## Claims and verdicts

| Claim | Predicate (frozen) | Before (base `c1f3d8d4`) | After (measured at the landed tip) | Verdict |
|---|---|---|---|---|
| C1 calibration | c73_wave_pointers: `unannotated == 0`, `dead >= 2`, append-only conjunct | `C1v1 … pointers=9 dead=2 annotated=0 unannotated=2 append_only=true met=false`, exit 1 | `C1v1 … dead=2 annotated=2 unannotated=0 append_only=true met=true`, exit 0; the c70 do-nothing control stays exit 0 at the tip (`pointers=361 dangling=17 annotated=17 unannotated=0` at the scratch variant; measured exit 0 at the landing tip) | met on the frozen predicate (calibration HOLD 2) |
| C2 operability | c73_tmp_v3: selftest full; corpus `attack_accepted=0/A`, `legit_rejected=0/L`; base and tip `findings=[]`; one SKILL.md registry row naming the counter | do-nothing control: the frozen round-72 counter accepts `9/11` attack lines (`measure/c72-control.txt`, wave-1 MutC2 agrees) | `C2v3 … attack_accepted=0/11 legit_rejected=0/4 selftest=41/41 findings=[] met=True`, exit 0, on the corpus; base and tip runs `findings=[]` exit 0; registry row appended past the last sidecar pin (935) | met on the frozen predicate (operability HOLD 10); sourced on S440 |
| C3 freshness | sweep offline at tip exits 0 or 1, no `Error:` line; selftest passes; sidecar diff = one `lineSha256` | exit 2, `paths sidecar binding invalid: corpus/SOURCES.md:140` (`controls/c3-sweep-base.txt`) | exit 1, stderr clean, `VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet`; selftest `36/36`; `git diff` on the sidecar = 1 insertion / 1 deletion (the single `lineSha256`) | met on the frozen predicate — *evaluable with named drift*, not clean (HOLD 10); the named finding is the lowercase `~/projects` cites already tracked by the open L0 kake\|round-69 line |

All three verdicts are on the frozen predicates. Harm checks at the landing tip: c66 `members=28 evaluated=28
mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True` exit 0; c70 exit 0; c72 exit 0 (`findings=[]`).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| M1 dead wave-relative receipt pointers — the round-72 LOG entry and SCORECARD rows cite `controls/c1-tip.txt` and `controls/c2-tip.txt`; neither was ever committed, while the real receipts `controls/c1-tip-final.txt` / `controls/c2-tip-final.txt` exist. The standing pointer counter (round-70 c70) exits 0 at base because its grammar parses only repo-rooted pointers, so the two wave-relative dead tokens were invisible to the lane's own instrument | `.ufo/waves/round-73/controls/c1-pointer-base-c70.txt` (c70 exit 0, `unannotated=0` at base); `git log --all` empty on both paths; routed item 1 of `corpus/lessons/round-72-verifier-spotcheck.md` | none — c70's token grammar does not cover wave-relative `controls/…` pointers, and the round-72 landing ran no pointer check over its own new rows | C1: append-only corrections in LOG.md and SCORECARD.md (tag `[r73-correction 2026-11-03]`) naming the superseded tokens and the resolving `-final` receipts, plus `.ufo/waves/round-73/c73_wave_pointers.py` whose grammar covers the round-72 LOG section and SCORECARD round-72 rows; shown able to fail (red at base, `dead=2 unannotated=2`) |
| M2 misattributed gate failure — the round-71 SCORECARD recorded the offline sweep's exit 2 as "pre-existing host state", but the break was caused by round-71's own commit `84dcc841` appending a `used-by` cell to the S132 row on the sidecar-pinned line `corpus/SOURCES.md:140`, invalidating that entry's `lineSha256` (ReviewerC1C3 F1: the pre-edit line hashes to the pinned value; the post-edit line hashes to the new pin) | `.ufo/waves/round-73/controls/c3-sweep-base.txt`; `git blame -L140,140` at base → `84dcc841`; sidecar diff at base = exactly that one entry's sha | QUALITY.md round-64 criterion "a round that edits a sidecar-pinned file re-runs the standing §paths sweep on its draft before landing" — round 71 edited a sidecar-pinned line and did not re-run the sweep | C3: re-pin that one entry's `lineSha256` (nothing else changes); the sweep evaluates again at the tip. The criterion itself stands; its scope is sharpened in words: an allowed registry *cell* edit is still an edit to a sidecar-pinned file |
| M3 systemic host-relative absence annotations (found by the attack seat, not fixed) — on this host 144 of 148 `kind=absent` sidecar tokens resolve today, including the re-pinned `SOURCES.md:140` entry whose note claims a 2026-10-31 absence that cannot be reproduced here (the file's birth predates the note); the sweep is unaffected because an absent note on a resolving token is inert | ReviewerC1C3 F5/F6 (`.ufo/waves/round-73/w1/ReviewerC1C3.md`), with `test -e`/`stat` evidence | none — no instrument compares a `kind=absent` note against the live filesystem; the sweep consults the note only in the citation-scan absent branch | routed to the next round: a dated re-observation pass over the 144 resolving absent tokens (flip to `restored` with present-state notes where true, per QUALITY.md "each re-pin has a dated observation"), or an explicit host-scope statement in the sidecar schema |

## Gate

- **Admit — S440 registry row** (GNU Bash manual, Shell Parameter Expansion; docs, tier A; opened 2026-11-03,
  HTTP 200, 30,764 bytes, sha256 `6b0800fd…a13c8e3`, retained at `.ufo/waves/round-73/sources/bash-param.html`).
  Located quote `If parameter is unset or null, the expansion of` (9 words) — one whole raw line (line 117) of the
  tag-stripped retained text `.ufo/waves/round-73/sources/bash-param.txt`, from the `${parameter:-word}` entry
  (the quote's second occurrence, line 139, belongs to the `${parameter:=word}` entry and is not the one cited).
  Grounds C2's H1: `${TMPDIR:-/tmp}` substitutes `/tmp` when `TMPDIR` is unset or null, so a repoint keeping the
  `/tmp` word still falls back to `/tmp`. The quote is grounded in the tag-stripped derivative (the raw html wraps
  `parameter` in `<var>` tags); html and text are line-aligned (661 lines each), so line 117 is the anchor for html
  line 117.
- **Admit — C1 correction tails** (ScribeRow drafts, integrator-applied): the superseded tokens stay
  wave-relative; the corrected `-final` receipts resolve at base; the round-70 identically-named pointer is
  explicitly scoped out. ConnOverlap O1 verified the tail shape keeps c70 exit 0 and that a repo-rooted spelling
  of a dead token would have flipped it red (negative control measured).
- **Admit — the SKILL.md registry section at EOF** (after line 1396; 22 of 25 SKILL.md sidecar pins would break
  under a line-213 insertion — ConnOverlap O2 measured the failure mode `exit 2 SKILL.md:365`).
- **Reject — editing the frozen attack corpus to close MutC2's three survivor classes** (M1 brace-branch removal,
  M3 imperative removal, M5 phrase truncation are invisible to the frozen 15 data lines). The corpus is frozen;
  the H4 phrase pin lives in the counter selftest (two truncation cases), and c73 detects the no-slash brace
  default directly, so the claim does not depend on the corpus lines the mutation probe showed blind. MutC2's
  three held-out lines are recorded for a future corpus amendment.
- **Reject — registering the round-72 c72 counter's own gate-registry row this round.** The frozen C2 predicate
  says exactly one row naming `c73_tmp_v3.py`; adding a second row would have required re-running the whole harm
  battery for a non-claimed change. Routed to the next round (the c72 counter's tip status — exit 0 — is
  measured and recorded for that row's Kind cell).
- **Reject — claiming the freshness gate "restored/clean".** The predicate is *evaluable*; the honest reading
  (ReviewerC1C3 F4/F5) is: exit 2 → exit 1 with the named `~/projects` drift (an L0-tracked host case-sensitivity
  artefact), and the re-pinned entry's absence note is contradicted on this host (M3). Nothing is claimed clean.

Spot-check: the non-author closure is owed. The L1 sample for it: 3 admits (S440, C1 tails, registry section at
EOF) and 3 rejects (frozen-corpus edit, c72 row, the "clean" freshness reading).

## Sourced claims

- **C2 rests on S440** (opened this round; quote and receipts above).
- C1 and C3 rest on lane instruments and receipts, not web sources.
