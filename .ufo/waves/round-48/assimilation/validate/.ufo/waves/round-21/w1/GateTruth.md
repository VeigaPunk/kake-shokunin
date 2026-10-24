# GateTruth — critic report on C2 (round 21, wave 1)

Seat: `KakeR21.GateTruth` (critic, leaf). Scope: does a retrospective `## Gate`
manufacture historical admits, rejects or independent review? I read the
representative lessons round-1, round-7 and round-19-recensus, then checked
the landed EOF gates against the repo. This report is the only file I wrote. No
lessons were edited, no commits were made, nothing was installed, no network
reads were made.

Snapshot: worktree on base `5009eca`, read on 2026-10-20 while sibling scribes
and L1 were still editing. Line numbers and counts below come from that read
and may move.

## Verdict

C2 can be admitted on operability: the heading structure exists and the
original bytes are preserved. It must not be read as discernment evidence.
Four defects need fixing before integration. Defects 1 and 2 break the
"no manufactured admission/reject" promise. Defect 3 breaks the structural
claim itself. Defect 4 is a same-round freshness regression.

## Counterexamples (strongest first)

### 1. "Admitted" applied to a claim the corpus now rejects (round-7)

- **What it says:** `corpus/lessons/round-7.md` new Gate marks "Live-only GHP
  orphans impossible by construction" (orig. lines 20-22) and the
  "two coverage directions … provably empty" claim (42-46) as **admitted with
  qualification**.
- **What the corpus says elsewhere:**
  - `corpus/lessons/round-20.md:261` lists this exact inference as mistake
    **A2** ("Platform mechanism inferred from workflow shape").
  - `corpus/QUALITY.md:15`, the Platform mechanism criterion, cites
    `round-7.md:21-25` as its *failing* example.
  - Nine r20-correction tails (`round-7.md:57-65`) supersede the claim.
- **Why it fails:** under the current bar this candidate is a reject. Calling
  it "admitted" invents an admission round 7 never made.
- **Root cause, wider than round 7:** kake had no QUALITY.md before `f405166`
  (2026-10-15, round 20). Before that date there was no bar, so nothing in
  rounds 1-19 could have been "admitted" in the LEARNING.md:13-15 sense
  ("admit only what clears the shokunin's own bar in `corpus/QUALITY.md`").
  The scribe prompt's required vocabulary ("admitted with qualification or
  unverified") forces this error onto every pre-r20 lesson.

### 2. Non-actions filed as rejections, and later rejections filed under an earlier round

- **round-19-recensus.md Gate, "Rejected candidates":**
  - R1 ("Do not re-pin to silence them", orig. 33-34) is a recorded rejection. Keep it.
  - R2 ("not patched", line 44) is an omission, not a rejected candidate.
  - R3 ("not re-fetched", line 48) is an omission, not a rejected candidate.
  - Both R2 and R3 carry "Reason: not recorded", which proves no decision was logged.
- **round-10.md Gate, "Rejected candidates":** lists "60/60 paths resolve …
  Rejected later, in round 15". This is a round-15 supersession sitting under a
  round-10 heading.
- **Risk:** the hyaku closure step samples "≥1 admit and ≥1 reject" from a
  lesson's `## Gate` (`../scripts/hyaku/closure-prompt.md:36-37`). These rows
  could be sampled as round-19 or round-10 rejects.
- **Contrast:** round-7's Gate handles this correctly ("Recorded, not edited" is
  a deferral, not a rejection).

### 3. Heading not exact, so the structural claim is not met and the planned count cannot see it

- **CORPUS contract:** a lesson carries a `## Gate` section (`../CORPUS.md:19`).
  Fleet contract-friction note: count with `^## Gate$`
  (`../.ufo/reports/round-22/kasegi.md:130`).
- **Observed headings:**
  - `round-4.md:44` and `round-8.md:60`: `## Gate — round-21 retrospective reconstruction`.
  - `round-10.md:64` had the same heading; it has since been corrected mid-flight.
- **Exact count over the fixed 15-lesson population:** **13/15**. Inexact:
  round-4, round-8.
- **Planned count recipe** (`SCORECARD.md:30`, `grep -l '^## Gate'`):
  - Unanchored, so it counts these headings as passes. It also matches
    `## Gate — round-20 resume`, and would match `## Gated …`.
  - Run over the current tree it returns **16**, because round-21.md is
    included. The baseline it claims is "1/15".
  - Its `grep -v aggregator` does not exclude `round-20-verifier-spotcheck.md`.
    The tree-wide denominator is therefore 17 files, not 15.

### 4. Statements true when written but false once integrated (freshness regression)

Several gates record time-of-read absences that the same round removes on
landing:

| Gate | Statement | Why false after landing |
|---|---|---|
| `round-1.md:66` | round-21 lesson "not present" | `corpus/lessons/round-21.md` now exists |
| `round-17.md:85` | same | same |
| `round-18.md:72` | same | same |
| `round-5.md:150` | same | same |
| `round-8.md:69` | same | same |
| `round-19-recensus.md:70` | S019 "not found under `corpus/`" | S019 is now `corpus/SOURCES.md:27` |
| `round-4.md:50` | "registry ends at S018" | same |
| `round-8.md:68` | same kind of claim | same |
| `round-7.md` "Basis read" | "not registered … cited by name only" | same |
| `round-19-recensus.md:70` | "`CORPUS.md` was not on disk" | `../CORPUS.md` and `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` both exist (10541 B, mtime Oct 19 21:21) |
| `round-1.md:68` | canonical CORPUS.md "not readable at its registered path" | same file exists at that path |

After commit these read as current-voice falsehoods. This is the
describe-don't-pin defect class that round 19 itself recorded.

Related: S019's anchor `scripts/corpus-contract.mjs` does not exist at read
time (`scripts/` holds only `freshness-sweep.mjs` and `probe-delta.mjs`). Every
retro gate that cites S019 as its contract authority will dangle unless L1
lands that script.

## Independent-review truth per representative lesson

| Lesson | Existing review evidence | Is the reviewer non-author? | Was there an admit+reject sample? | Required gate wording |
|---|---|---|---|---|
| round-1 | `round-1-aggregator-audit.md`: aggregator L1 (m_qwen) plus an L2 reviewer the aggregator dispatched, 2026-09-28; verdict **NOT conformant**; 3 defects, including "~40 clones" vs 50 against `round-1.md:20` | Yes, relative to kake | No | "Non-author corpus audit present; verdict NOT conformant; admit/reject spot-check: not recorded." The landed gate already says this. Keep it. |
| round-7 | `round-6-aggregator-audit.md:88-92,132`: open finding that the label `~20:20Z` is future-dated (run time bounded at 19:35Z; ship time `83d08e4` 19:39:21Z) | Yes | No | "Outside spot-check: not recorded; one non-author **disagreement** (timestamp) open." The landed gate mentions it. It must not be omitted or softened. |
| round-19-recensus | "Independent audit erratum" (lines 42-48) from wave `Shokunin12hP1Audit20261014`; `KakeGateRerun.md` agrees on 4 verdict lines and disagrees that case `e` proves confinement | **Contestable.** Repair wave and audit wave both ran "under the sole Sol 6.1 L1" (`../.ufo/waves/shokunin12h-20261014-p1-{repair,audit}/spec.json` context line 2), and LOG.md:435 records "parent integration" as the author. LEARNING.md:45-46: "A subagent the lane dispatched is still the lane." | No. It is a gate re-run, not a decision sample | "Same-L1-dispatched acceptance audit (re-run, not admit/reject spot-check); outside spot-check: not recorded." The landed gate says "author not named in the file". Add the same-L1 fact; never use the lesson's own "Independent" heading as the independence attestation. |

## Necessary qualifications (minimal set C2 must carry)

1. **Vocabulary.** For lessons before QUALITY.md (rounds 1-19), outcomes may
   only be:
   - "landed (no gate, no QUALITY bar at the time)"
   - "corroborated by non-author audit <file:line> on <date>"
   - "contradicted/superseded by <cite>"
   - "unverified"

   Never "admitted". If the word must stay, define it once in the label as
   "landed-without-gate", and every superseded claim (round-7 A2) must read
   "superseded; fails QUALITY.md:15".
2. **Rejected.** Only decisions recorded in the original text, with the
   original reason quoted. Omissions and deferrals go under a separate
   "Not performed / deferred" line. Later-round supersessions go under
   "Superseded later (round N, cite)", outside the Rejected list.
3. **Outside spot-check.** Always the literal "admit/reject spot-check: not
   recorded" unless a non-author record samples one admit **and** one reject
   of *that* round. Any other non-author evidence is cited separately, with its
   verdict, including disagreements. Reviewers dispatched by the lane or by
   the same L1 are author-side.
4. **Attribution.** Every retro gate names round 21, the writing seat and the
   date in its first body line, so sampling tools cannot attribute its rows
   to round N.
5. **Credit.** The count is an operability structure metric. It must not move
   discernment, the verified-round count or any historical round's admission
   status. This matches the new `corpus/QUALITY.md:43-57` ("A heading count
   alone cannot prove those decisions occurred").

## Falsifiers Main can run (post-integration)

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin
# exact heading over the fixed population — must print 15
for f in 1 3 4 5 6 7 8 9 10 12 16 17 18 19-recensus 20; do grep -q '^## Gate$' corpus/lessons/round-$f.md && echo ok; done | wc -l
# byte-prefix preservation — must print nothing
for f in corpus/lessons/round-*.md; do b=$(git show 5009eca:$f 2>/dev/null|wc -c); [ $b -gt 0 ] && ! git show 5009eca:$f | cmp -s - <(head -c $b $f) && echo BROKEN $f; done
# stale read-time absences — must print nothing after fixes
grep -nE 'not present (in|when)|not on disk|not registered|not found under|registry ends at S018|not readable at its registered' corpus/lessons/round-{1,3,4,5,6,7,8,9,10,12,16,17,18,19-recensus}.md
# manufactured independence — every hit must be qualified (non-author named, or "not")
git diff 5009eca -- corpus/lessons | grep '^+' | grep -niE '\bagree\b|independent' 
# "admitted" on A2-class claims — round-7 hits must say superseded/fails QUALITY.md:15
grep -n -i 'admitted' corpus/lessons/round-7.md
# S019 anchor resolves
test -e scripts/corpus-contract.mjs && echo s019-anchor-ok
```

A gate is falsified by any of the following:

- a sampled "Rejected" row whose reason is "not recorded";
- an "admitted" row whose claim appears in round-20 Mistakes A1-A4 or as a
  failing example in QUALITY.md;
- any `agree` attributed to a reviewer dispatched by the lane or by the same
  L1.

Byte-prefix result at read time: all 23 lessons were prefix-OK.
`round-16.md` shows "1 deletion" in `git diff --numstat` only because its base
file lacked a trailing newline (last byte `0x2e`). The bytes are preserved. A
check that counts line deletions will flag it, so verify with `cmp` instead.

## Impacted axes

- **operability:** defect 3 (2 of 15 inexact headings; the recipe's anchor and
  denominator).
- **freshness:** defect 4 (more than 10 read-time absence statements made
  false by integration; the S019 anchor dangles).
- **discernment / quality (not owned, harm guard):** defects 1-2 would plant
  sampleable fake admits and rejects. If integrated unqualified, report this
  as harm, not a trade.

## Smallest safe corrections

All are edits to lines added in round 21 only. Prior bytes stay untouched.

1. **Headings.** Change `round-4.md:44` and `round-8.md:60` to `## Gate`, with
   the label moved to the first body line.
2. **Count recipe.** L1 changes `SCORECARD.md:30` to anchor `^## Gate$` over the
   explicit 15-file list. round-21.md is reported separately as the 16th,
   contemporary gate.
3. **round-7 Gate.** Re-label the two served-set candidates "landed without
   gate; superseded by r20 corrections (lines 57-65); fails QUALITY.md:15
   (A2)".
4. **round-19-recensus Gate.** Move R2/R3 to "Not performed (no decision
   recorded)". Add one sentence: the audit wave was dispatched by the same
   sole Sol 6.1 L1 that integrated the round, so it is author-side under
   LEARNING.md:45-46.
5. **round-10 Gate.** Move the "60/60 … round 15" row to "Superseded later".
6. **Read-time absence sentences.** Replace each with the resolved cite
   (`corpus/lessons/round-21.md`; `corpus/SOURCES.md:27` S019; canonical
   `CORPUS.md` Layout lines 18-20), or delete it.
7. **S019.** L1 lands `scripts/corpus-contract.mjs` or corrects S019's anchor.
8. **Vocabulary rule.** Add qualification 1 as one sentence to the round-21
   lesson so the "admitted" vocabulary has a defined, non-admission meaning
   for rounds 1-19.

## Limitations

- I did not open the dead-path lane file cited at `round-19-recensus.md:52`.
- I opened `KakeGateRerun.md` and the p1 audit/repair specs only for
  authorship and verdict.
- The other 11 retro gates were scanned for risky terms, not read in full.
  The scout and reviewer seats cover them.
- The worktree was changing during my read (round-10's heading was fixed
  mid-flight). Counts are point-in-time.
- No tool installs or updates.
