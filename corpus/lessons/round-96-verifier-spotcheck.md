# Round 96 verifier spot-check — kake (hyaku closure, non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-05
lane repo: /home/vgpnk/Projects/shokunin/kake-shokunin
round base `bde9869144f69c5a459c0d2c93f5135922fe3a8d` → tip `9177e65823ee29fd52c4d4c0b3105c18bc63ee9a`
report: `.ufo/reports/round-96/kake.md` (fleet commit `502c3d492922c5572ebce3c051b27a4d570b4eeb`, lane identity)
dispatch digest (copied verbatim from `.ufo/watchdog.log`; lines 2892 and 2905):
2026-11-05T14:27:28-03:00 launch kake round=96 pgid=290456 driver=hyaku-inline attempt=1
2026-11-05T16:02:05-03:00 complete kake round=96; hyaku-inline attempt=1

This file is the non-author closure verification of kake round 96. Every command below was
run by the closure session at or against the cited commits; nothing was copied from the
report without re-derivation.

## 1. Step-1 conformance — PASS with named, status-neutral defects

- Report committed in the fleet repo by the lane identity:
  `git -C /home/vgpnk/Projects/shokunin log --format='%an %ae %H' -- .ufo/reports/round-96/kake.md`
  → `kake-shokunin kake@shokunin.local 502c3d492922c5572ebce3c051b27a4d570b4eeb`;
  `git merge-base --is-ancestor 502c3d4… HEAD` holds in the fleet repo.
- `SHONEN` heading present with one line per box, marks `[~]`/`[ ]`/`[~]`/`[~]` with
  resolvable pointers; box 2 left `[ ]` (unchanged gap, correctly not asserted).
- Every cited lane commit exists and is an ancestor of the branch ref (jj-colocated repo,
  ancestry tested against `refs/heads/master`, never `@{u}`):
  `7ae3e9b0`, `049e8eca`, `7dc9bf43`, `05c19fd1`, `1098dccd`, `9177e658` → all `ancestor-ok`;
  base `bde98691` and tip `9177e658` likewise.
- Pushed and clean:
  `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kake-shokunin` →
  `branch=master local=9177e658… remote=9177e658… ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` empty; `git ls-remote origin refs/heads/master` prints `9177e658…`.
- Dispatch digest lines match `.ufo/watchdog.log` verbatim (line 2892 launch, line 2905
  complete); `grep -c 'lane-dead-no-report kake round=96'` → 0; attempt 1 is the first attempt.
- Dispatch evidence durable: `.ufo/prompts/kake-round-96.md` committed in the fleet repo
  (`284c37cd` "round-96: kake dispatch evidence"). Prompt carries the canonical
  `templates/round-prompt.md` contract verbatim — mission/axes binding, 1–3 falsifiable claims
  with the lowest-non-retired-axis rule, frontier step 2b, L2 floor (≥8 seats, ONE batched call,
  role split), report contract with the five child-lane items (report path, commit-before-report,
  SHONEN heading, commit-hash citation, write scope), commit-then-push ordering, push scope, L0
  side channel — plus hyaku addendum §6. No missing embed item.
- L0 line landed: `.ufo/l0-questions.md` line 371 at fleet HEAD carries
  `kake | round-96 | R95-2 fleet kill-predicate arbitration owed: …` (verbatim check passed).
- Report sections present in the required order (Work performed, Landed changes, Before →
  after measurements, Sources & frontier, Trend verdicts, SHONEN).
- Frontier step: SOURCES census exit 0 at the tip (re-run by closure, see §2); mistake mining
  present (`## Mistakes`, 3 rows, class/evidence/captured-by/fix); sourced claim duty met (C2
  rests on S480, opened this round).
- LOG.md tie: `## Round 96` entry present at LOG.md line 3266 naming both claims.

Conformance defects (status-neutral; routed, never admission-blocking):
1. **§3 minimum role split: no planner seat dispatched.** `w1-results.json` lists 12 seats —
   ScoutRFC, ExecReval, ExecC1Guard, ExecRegistry, ExecReceipts, ScribeEntry, ReviewC1,
   ReviewReval, CriticClaims, MutReval, SentinelScope, ConnectorScope — every seat with a
   nonempty output payload. The report discloses the planner seat was held by the L1 because
   the validator rejects `planner` as a swarm role. Disclosed, but the prompt's minimum role
   split is not literally met: recorded as a defect for the driver/validator owner.
2. **Coverage-map index not updated.** `git diff bde9869… 9177e658… -- corpus/README.md` is
   empty: the new knowledge entry `corpus/knowledge/revalidation-exchange.md` (and the ground
   it holds) has no README index/coverage row; the five pre-existing `revalidation` mentions
   are the open-frontier list. CORPUS round-1 rule: "An index row is a claim. Write the row
   when the file exists, not before." Routed as R97-D1.
3. **Assimilation count nit.** The lesson's Gate quotes "217 registry ids" citing
   `w1/ExecReceipts/assimilation/{reg-ids,staged-ids,collisions}`; `grep -c .` over the
   committed `reg-ids` gives 216 nonempty ids (wave-time, before the round's own S480 row
   landed). The delta is exactly the round's own row and the collisions count (8, re-verified:
   S312 S329 S367 S372 S373 S374 S390 S409, with S312 present in both sides) is unaffected,
   but the lesson should state the delta at the citation. Routed as a count-accuracy note.
4. **Driver-side prompt drift (not a lane defect).** Prompt §1 says "Your lane axes:
   operability + freshness" while the lane SCORECARD owns calibration (2, lowest non-retired),
   freshness (10) and operability (10); the round worked calibration + freshness, satisfying
   the lowest-axis rule per SCORECARD/AXES. Surfaced for the driver template owner.

## 2. Claim re-checks

Re-measured by closure = plain commands run by this session over committed bytes.
Evidence-verified = the claim rests on a lane-owned gate; per PROTOCOL §Gate standard
(closure consequence) its committed evidence (self-test tally, frozen-run verdict, revision
measured) was verified and the sibling's counter was NOT executed.

### C1 — calibration (HOLD 2, lowest owned axis): routed R95-1/R95-5/R95-7-C1 instrument defects close — **verifies (met on the frozen predicate)**

Evidence-verified (gate-owned receipts, none executed):
- `controls/after-c1-successor.txt`: `C1v96 revision=1098dccd… counter=a282da65… lessons=91
  entries=84 rows=262 criteria=40 mismatches=0 E1=0 E2=0 E3=0 E4=0 E5=0 pins=ok battery=23/23
  admit=5/5 shadow=absent predecessor_admits=6/22 floor=4 ng_pred_admits=3/3 self_pin=ok
  met=true`, `exit=0` — revision named, matches the report exactly.
- `controls/after-c1-predecessor.txt`: same revision, `pins=identity battery=20/20 met=false`,
  `exit=1` — the differential the claim needs, at the same tree.
- Do-nothing controls at base: `controls/c1-successor-at-base.txt` (`met=true`, exit 0) and
  `controls/base-c1-predecessor.txt` (`pins=identity met=false`, exit 1) — pre-freeze,
  committed; Mistake 3's reading (the successor-at-base control is the claimed work scoring
  itself) is recorded in the lesson, not defended.
- Self-test: `controls/ctl-c1-selftest.txt` `selftest 13/13 … battery 23/23 admit 5/5 …
  --surfaces-file refused`, exit 0.
Re-measured by closure (plain, this session):
- Freeze pins vs tip bytes: `git show 9177e658:.ufo/waves/round-96/c96_selfassess.py | sha256sum`
  → `a282da654d5ee6af923abb2cae4bd0a4fd6e4309db81de5a67999ed7b25ad134`; same method for
  `c96_reval.py` → `ec40aec19d0b4563ad21d79b398c7aaa65a99806984dbca55086c099571eebb9` — both
  equal `controls/instrument-sha256.txt`. No frozen byte changed after the freeze commit
  `049e8eca`.
- SOURCES rows 216 → 217: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base → 216,
  at tip → 217.
- Census re-run by closure at the pushed tip:
  `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin kake` → final verdict `kake ok …/corpus/SOURCES.md`, exit 0;
  40 `W04` duplicate-URL warnings, the pre-existing class the report names; no E-class findings.

### C2 — freshness (HOLD 10, capability acquisition): revalidation exchange, contract v1 — **does not verify (unmet; honest stop)**

Evidence-verified:
- Before: `controls/base-c2.txt` `candidate=absent hand=0/37 generated=0/120
  forgeries_refused=0/6 positive=refused mutants=0/14 survivors=none anti_table=ok
  population=ok seed=96 met=false`, exit 1, at base.
- The honest-stop crash is independently receipted by two attack seats: SentinelScope
  `r08-c2-crash-nameerror.txt` (five candidate variants incl. the frozen positive control,
  each rc=1 `NameError: name 'mutants' is not defined` at `c96_reval.py:624`) and CriticClaims
  `C2-01` (committed candidate in a scratch clone, same crash).
- No after receipt was forged: `git ls-tree … .ufo/waves/round-96/controls/` contains only
  `base-c2.txt` and `ctl-c2-selftest.txt` — no `after-c2*`.
- No Capabilities row entered: the SCORECARD diff base→tip is 50 appended lines only; its
  round-96 section says "No new capability row (no frozen-counter pass)". Score stays 10.
- The candidate landed and is independently verified: `scripts/reval_exchange.py` at
  `7dc9bf43`; ReviewReval grid `agree=24/24 tooldefects=0 contractdefects=0 referencedefects=0`
  on a fresh non-overlapping 24-case grid (`w1/ReviewReval/grid.md`,
  `receipt-nonoverlap.txt`); MutReval frozen population 14/14.
Re-measured by closure (plain, this session):
- Crash site read from committed bytes: `c96_reval.py` line 624 is
  `killed, survivors, notes, mdrift = mutant_cases(work, sandbox, cases, gen_expected, base_src, mutants, tree)`
  inside the main scoring path, where no `mutants` binding exists (only `selftest()` binds the
  population list) — consistent with both crash receipts and Mistake 1 / QUALITY R96-A.
- `ctl-c2-selftest.txt` (`7/7 fixtures … mutants killed 14/14 … anti_table=ok`, exit 0) is the
  green selftest whose path diverges from the crashing main path — exactly the defect R96-A
  now names.
- C2's SOURCES ground: row S480 landed `mined` (11 cells, census-clean), knowledge entry
  `corpus/knowledge/revalidation-exchange.md` present at tip with the provenance trio first
  (`source: S480 … §4.3, lines 812-949`; `verified-at: 2026-11-05`; `recheck: 180d`).

**No owned axis harmed:** SCORECARD diff base→tip is append-only (50 inserted lines, zero
deletions/edits); operability (10), freshness (10), calibration (2) scores untouched; verdicts
are recorded, not silently absorbed.

## 3. Discernment spot-check (non-author; LEARNING.md)

Sample: 1 admit + 2 rejects from `corpus/lessons/round-96.md` `## Gate`, each source re-opened
by this session.

| item | decision | re-opened source (closure's own access) | agree/disagree | reason |
|---|---|---|---|---|
| SOURCES row S480 (RFC 9111 §4.3.1/§4.3.3 validation exchange) | admit | fresh `curl` GET of https://www.rfc-editor.org/rfc/rfc9111.txt this session: 84 477 bytes, sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` — byte-identical to the scout receipt and the retained round-93 body | **agree** | the six clause lines named by the Gate all carry the claimed text at exactly lines 848 ("MUST send the relevant entity tags…"), 852 ("SHOULD send the Last-Modified value…"), 861 ("In most cases, both validators are generated…"), 935 ("A 304 (Not Modified) response status code…"), 938 ("A full response (i.e., one containing content)…"), 944 ("However, if a cache receives a 5xx (Server Error) response while…"); the ≤25-word quote "In most cases, both validators are generated" (7 words) sits at line 861 as receipted; tier A scoped to §4.3.1/§4.3.3 with explicit exclusions is correct curation |
| knowledge entry `revalidation-exchange.md` | admit | ScribeEntry `quotes-verified.txt` (13/13 quotes ok, `words_ok=True`, body-vs-fetched IDENTICAL at the retained sha) + closure's own fetch above; entry's provenance trio first; exclusions paragraph bounds scope | **agree** | quote-bound entry on distinct ground (validation-exchange decision; nearest held ground is r83 header-classification via S456 and r92 heuristic-freshness via S470 — different scopes, verified against base README) |
| Capability-row entry for the revalidation exchange | reject | AXES.md Capabilities ("Rows enter only through a round that demonstrates the capability running; a capability without a passing demonstration in the round report is pre-claiming") + the crash receipts and closure's own line-624 read | **agree** | no frozen-counter pass exists (the counter crashes before scoring); admitting the row would be pre-claiming; the flip condition (round-97 successor counter `met=true` on candidate `192b3bf7…`) is on record |
| merge/kake package adoption | reject | committed receipts `w1/ExecReceipts/assimilation/{reg-ids,staged-ids,collisions}` (216 wave-time registry ids, 129 staged, 8 collisions; S312 cross-checked present in both sides) + CORPUS rule 1 (a row is written only after opening/re-grounding) | **agree** | no scratch renumber map was produced and no entry was re-grounded; adoption would have ridden ungrounded collisions; flip condition recorded |

No disagreement was found; nothing to learn from this spot-check beyond what the round already
routed (R96-1…R96-4). Chousa prior-art citation verified: chousa `corpus/QUALITY.md` line 1054
criterion 146 at the sibling's current HEAD `378fda82` matches the text R96-A cites — cited,
not ported (R95-3 closed as specified).

## 4. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| calibration | **improved** | C1 verifies on the frozen predicate with the differential at one revision (successor `met=true` exit 0 vs predecessor `pins=identity met=false` exit 1, both receipts at `1098dccd`); the routed R95-1/R95-5/R95-7-C1 defect classes are closed and receipted; the instrument's newly-found false-greens are routed (R96-3/R96-4), not hidden. Score stays 2 (lane-declared; closure does not re-score). |
| freshness | **unchanged** | C2 lands unmet (honest stop): the frozen counter cannot score the candidate, no capability row enters, score stays 10; the candidate lands uncredited with independent verification; nothing on the freshness axis regressed (existing freshness instruments untouched) and nothing countably improved. |
| operability | **unchanged** | untouched this round; SCORECARD diff append-only; no operability claim declared. |

## 5. Trend verdicts (closure)

| trend | verdict | evidence |
|---|---|---|
| expansion | **improved** | one admitted knowledge entry (`corpus/knowledge/revalidation-exchange.md`, quote-verified 13/13) on ground the coverage map did not hold (§4.3.1/§4.3.3 validation-exchange decision; nearest held ground is r83 S456 header-classification and r92 S470 heuristic-freshness, different scopes — verified against the base README), whose `source:` cites the mined row S480 — the CORPUS contract v1 rule 4 counting unit ("admitted knowledge/ entries whose source: cites a mined row on uncovered coverage-map ground"); registry 216 → 217 with census exit 0, re-run by closure. The lane self-graded `unchanged` on a capabilities-repertoire argument; closure grades by the LEARNING/CORPUS counting rule and records both positions. The missing README index row is routed (R97-D1) — an index defect, not a trend blocker. |
| quality | **improved** | the round-95 corpus repairs are now certifiable (successor counter `met=true` at the tip with `mismatches=0` and identity pins), two gate-registry rows landed and resolve (ExecRegistry receipt, 8/8 digests), the S480/entry pair is quote-verified, and no admitted entry failed a re-check; the C2 counter defect is receipted and routed rather than papered over. |
| discernment | **improved** | LEARNING.md's improved condition — "the spot-check agrees with the gate on admits and rejects" — is met by §3 above (1 admit + 2 rejects, all agreed, sources re-opened by the non-author); the R96-A criterion is grounded in Mistake 1 with committed crash receipts (no criterion-without-lesson defect); no disagreement was left unlearned. The lane self-graded `unchanged` because the spot-check was owed at its write time; this closure's agreeing spot-check discharges it. |

## 6. Routed defects (kake must fix in round 97)

- **R96-1…R96-4, R95-2, R95-6/R95-7-C2** — as the round lesson routes them (verified present in
  `corpus/lessons/round-96.md` §Routed; the closure adds nothing and removes nothing).
- **R97-D1 (closure-routed): write the corpus/README.md index/coverage row for
  `corpus/knowledge/revalidation-exchange.md`** (and mark the §4.3.1/§4.3.3 ground held),
  per "An index row is a claim. Write the row when the file exists, not before."
- **R97-D2 (driver/validator-side, recorded here for routing): the §3 planner seat cannot be
  dispatched because the validator rejects the role** — the lane disclosed the L1 held the
  duty; the minimum role split is still unmet on its face. Owner: driver template/validator.
- **Count-accuracy note:** cite the assimilation receipt's wave-time number (216 registry ids)
  with the delta named, or re-derive at the tip (217) with a fresh command line.

## 7. SHONEN observation for the operator (promotion is operator-owned)

Boxes 1, 3 and 4 carry author-assertions `[~]` with resolvable pointers; from committed
evidence they look fully checkable by a non-author: SKILL.md decision tables/error
patterns/checklists with the two new gate-registry rows resolving (ExecRegistry 8/8), the
frozen counters' self-contained CLI contracts (docstrings + freeze + registry rows), and
PROVINCE untouched with read-only sibling-overlap receipts (`w1/ConnectorScope/overlaps96.md`).
Box 2 (end-to-end task logged) remains `[ ]`. This closure wrote nothing into SHONEN.md; a
named non-author may write `[x]` only through the operator's promotion review.
