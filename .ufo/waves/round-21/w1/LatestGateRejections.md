# LatestGateRejections — round-21 w1 (kake)

Scope: `corpus/lessons/round-16.md`, `round-17.md`, `round-18.md`, `round-19-recensus.md`, `round-20-verifier-spotcheck.md`. Question: which historical findings were admitted or measured in their round, which are unverified assertions, and what gate text should say. Read-only. No lesson, SCORECARD, LOG, QUALITY, SOURCES, README or SKILL was edited. No test, selftest, build, freshness sweep, fetch or live probe was run. Read commands only: `read`, `grep`, `ls`, `wc`, `git show|diff|log|cat-file` against base `cb807bc`. No tool was installed or upgraded.

Working-tree caveat: other round-21 seats were appending `## Gate` sections while this was written. Observed state (2026-10-20 working tree, HEAD `5009eca`): `## Gate` present in round-16 (line 78), round-17 (58), round-18 (appended, reviewed in §3.4), round-19-recensus (62). `round-20-verifier-spotcheck.md` has no `## Gate`. Line numbers below refer to that state.

## 1. Evidence presence (checked at read time)

| Claimed evidence | Location | Present? |
|---|---|---|
| r16 raw claim census (`scout-claims.md`, `claims.tsv`) | `/tmp/kake-r16/` | Directory exists, created 2026-10-20 05:55, contains only `selftest/`. `claims.tsv` and `scout-claims.md` absent. Not round-16 evidence. |
| r17 sentinel hashes, mutant runs | `/tmp/kake-r17/` | Absent. |
| r18 `before.json`, `before.out`, `after*.out`, `p.json` | `/tmp/kake-r18/` | Absent. |
| r20 anchor-integrity census (728 / 148 / 942 / 0) | `kake-shokunin/.ufo/round-20/resume/post-review-anchors.json` | Present. `citationOccurrences: 728` confirmed; 148/942/0 not re-derived. |
| r20 post-review restoration log | `.ufo/round-20/resume/post-review-restoration.txt` | Present (not opened here). |
| r19 advisory re-run (13/13, mutant survives) | `../.ufo/waves/shokunin12h-20261014-p1-audit/members/KakeGateRerun.md` (fleet repo `/home/vgpnk/Projects/shokunin`) | Present. Lines 11, 27, 61–62 match the r19 erratum. |
| r19 dead-path sweep (77 live, 65 marked, 257 labelled, 0 unresolved) | `…/p1-audit/members/KakeDeadPathSweep.md` lines 66–68, 91 | Present; counts match. |
| r18 history claims | `…/p1-repair/members/KakeHistoryClaims.md` | Present. |
| r20 non-author verifier report | `…/.ufo/waves/kaika-w3/kake-review.md` (fleet repo) and `kake-critic.md` | Present. Reviewer: `W3ReviewKake`. |
| Round-20 commits | `9639ec7`, `7e17c66` | Both resolve (`git cat-file -t` → commit). |
| r18 "2026-10-12 prune" date | `LOG.md` | Not present. `LOG.md:400` dates the W7 prune only to the 2026-10-14 round-18 entry. |

Consequence: any gate line saying `/tmp/kake-r16/` is "absent" is now wrong (the directory exists, but holds no round-16 artifacts). Any gate line citing `/tmp/kake-r17/` or `/tmp/kake-r18/` as present is wrong. Round-17 and round-18 admissions therefore rest on the lesson text and LOG only.

## 2. Cross-cutting defects

### 2.1 Wording: "admitted" for reconstructed outcomes
Retrospective gates for rounds 16 and 17 label candidates "Admitted with qualification" (r16 A, B, C, D, G; r17 C1–C5, C8). The r16 gate header and r17 gate header both state that no admission was recorded at the time. The candidate-table verb still implies an original gate decision. `LOG.md` contains no admit or reject record for rounds 16–19 (`grep -n admit LOG.md` hits only round 20, lines 528–538). Under the C2 rule ("no fabricated admissions/rejects"), that verb is the defect to fix.

Advice: use `supported (reconstructed)` / `measured-in-round` / `carried` / `unverified` / `superseded by rN`. Keep `admitted` only where the original round recorded an admit (none of the five does, apart from the round-20 verifier decision in §2.4 that the integrator recorded, not the lane).

### 2.2 Mid-sentence annotations (append-only)
`git diff cb807bc -- corpus/lessons/round-17.md round-18.md` shows pure insertions (0 deletions):
- round-17: new lines 14, 16, 23, 25 (`> *[r20 citation-local …]*`), each inserted inside a sentence or list item.
- round-18: new line 33, inserted between `` `~/Projects/ `` and `` webzites/fleet` `` (splits a code span).

A `>` line in the middle of a paragraph renders as a block quote that interrupts the sentence. The base lines survive byte-for-byte, and `post-review-anchors.json` covers round-17.md:13/14 in its inbound-pointer census. The rule in `corpus/QUALITY.md:37-39` requires that census for adjacent standalone notes, and it is present for these. The defect is readability, not byte preservation. Gate text should record the insertion positions; it must not edit the body.

### 2.3 Unsourced 2026-10-12 prune date
The phrase "W7, the 2026-10-12 `~/Projects` prune/migration" appears in many r18 re-census annotations (`round-18.md:16`, `round-17.md:14`, `round-18.md:33`, `knowledge/keeper-timer-inert.md`, `ops-automation.md`, `origin-repos.md`, `handoffs/cmdProbe-merge-fix.md`). The round-18 body itself says only "sometime between r17 (2026-09-29) and today" (`round-18.md:9`). The date has no measurement in the corpus. `LOG.md` has no `10-12`. The only file that supplies it, `.ufo/round-20/resume/citation-disposition.json:10,18,26`, cites `corpus/lessons/round-18.md:14,16` as evidence, and those lines are annotations: the chain is circular.

Status: unverified assertion, repeated across ~25 files. Gate text must say "prune date unmeasured; bounded 2026-09-29 < t ≤ 2026-10-14 by the round-18 record."

### 2.4 Count drift: r18 "63 cite lines across 22 files"
Current working tree: `grep -r 'r18 re-census' corpus` → 64 lines in 25 files (includes lesson and knowledge self-references). Round-18's figure is a dated measurement at its commit, not a standing claim. Gate text should label it historical.

## 3. Per-lesson classification

### 3.1 round-16 (`corpus/lessons/round-16.md`, body 1–76; gate 78–179)
**Recorded in-round, admitted with measurement (LOG-backed):**
- 160-claim census: 117 HOLD / 15 STALE / 7 UNVERIFIABLE / 21 HISTORICAL-OK (`LOG.md:227-228`); all 15 stale fixed or re-pinned in-round (`LOG.md:228`).
- Journal key union `site, mode, startedAt, steps[], fire, error` and `recreate plazir15` fire count ×3 (`knowledge/fire-journal-codes.md`).
- ETag rule (`6ab49127` vs `6ab49126`): r16 7/7 and r17 8/8 fetches recorded in LOG (gate candidate E).
- PQ-14 ledgered, stale-not-rot (`publish-queue.md` PQ-14).

**Unverified in the body:**
- "Ten of the 15 stale rows" (`round-16.md:19-20`): the body lists four classes, not ten rows. The gate (`:106-107`) correctly says this was not recounted.
- Sample values in `free-read-verbs.md` (`{ok:4, attention:[…5…]}`, "6 ids / 5 DIFF + 1 ERR"): the lesson's own rule 2 (`:47-52`) requires a run timestamp. The body carries none; the timestamp lives only in the knowledge file's r16 amendment. Treat as dated, not standing.
- "~1050 lines" and "revisit before a fourth section" (`:68-73`): not measured in the round; gate candidate H already says so.
- "sentinel/reviewer/critic each caught a real defect" (`:74-76`): L2 drafts, in-lane. Not outside review.

**Gate-text fixes (r16 gate, 78–179):**
1. Line 164–166 says `/tmp/kake-r16/` "was absent when this gate was written". Replace with: the directory exists since 2026-10-20 05:55 and contains only `selftest/`; no round-16 raw file is present.
2. Line 170–171 says S019 "was not found in the repository". S019 is now present at `corpus/SOURCES.md:27`. Date the statement.
3. Candidate verbs per §2.1.

### 3.2 round-17 (`corpus/lessons/round-17.md`, body 1–56; gate 58–88)
**Measured in-round (in-lesson record, LOG round-17 cited):** W6 drift at 03:20:19Z, exit 1; `pathsMissSet` 9→10 with `~/projects`; `projectsChildrenSet` 36 with `set MATCH` (`§Verification` line 48); `pathsFiles` array fix with `set-delta files +0/-0`; `loadPins` exit 2 on malformed pins; `--selftest` 10/10 (line 47); "rule learned" (type-mismatch pins silently inert).

**Unverified in the body:**
- C6 — header classification of six plazir pins (`§What happened` 3, third bullet): no output shown; the gate already says so.
- C7 — state-guard `~/Projects/webzites/state/` 33-file sha set (`§Verification` line 49): the evidence (`/tmp/kake-r17/sentinel-*.sha`) is absent; the path itself is annotated absent by r18.
- W6 window 03:13:18–03:14:07Z and "2026-09-29": measured by the lesson's own mtime reading; not re-observable now.
- W7 "2026-10-12" inside the r20 annotation at line 14: §2.3.

**Gate-text fixes (r17 gate, 58–88):**
1. C1–C5, C8 verbs per §2.1.
2. Line 86 treats `S019` as "tier A". The SOURCES row (`corpus/SOURCES.md:27`) is `own-work`, self-authored, tier A. Say "tier A own-work (self-sourced); not an external check" so the gate does not read as independent authority.
3. Line 80 names `/tmp/kake-r17/` as the location of L2 artifacts; state that the directory is absent at read time.

### 3.3 round-18 (`corpus/lessons/round-18.md`, body 1–63; gate appended by another seat, reviewed here)
**Measured in-round (LOG round-18 item 1–3, lesson's own numbers):** exit 2 at round open (12:40Z); 33/36 children removed, 11 added; §paths 36 unannotated + 45 beyond pins; §history fail-closed exit 2; PQ-12 armed watch fired (marker `2026-09-26`→`2026-09-30 scribe beat`); selftest 10→8→10. The "alpha HEAD `964f443e`, no `ledger.jsonl`" claim is independently matched by the r19 audit (`round-19-recensus.md:48`, citing the audit member) — partly confirmed.

**Unverified:**
- "2026-10-12" date (§2.3).
- The PQ-12 interpretation "edit landed while the registry file was unverifiable": lesson's own reading, no outside check. Must be labelled as interpretation.
- "63 cite lines / 22 files" (§2.4).
- Pin values `pathsMissSet` 10→55, `projectsChildrenSet` 36→14: re-measured in-round, but r19 shows `freshness-sweep.md:43-53` still quoting pre-r18 literals and live children = 30 (`round-19-recensus.md:39-40, 48`). Historical only.

**Gate-text review (appended section, 100 lines):** structure and rejection notes are sound. Three corrections:
1. The round-18 gate's statement that `corpus/lessons/round-21.md` "is not on disk at read time" is now stale: the file exists in the working tree. Date the statement.
2. Candidate verb "admitted with qualification" (C1–C3, C5–C7) per §2.1.
3. C8 (verdicts, "unverified here; historical observation") is correctly labelled. Keep.

### 3.4 round-19-recensus (`corpus/lessons/round-19-recensus.md`, body 1–60; gate 62–99)
**Measured:** selftest 13/13 (lesson line 22); offline exit 0 with §history SUSPENDED; explicit missing `KAKE_PROBE_HISTORY` exit 2 (line 28); no `$HOME/.kake-freshness-selftest-*` residue (line 29). Independent advisory re-run `KakeGateRerun.md` reproduces 13/13 and shows the mutant `verdictOf` write surviving at case `e` (lines 11, 27, 61–62, 68). Confirms the erratum at lines 42–44.

**Dead-path population:** 77 live citations (`KakeDeadPathSweep.md:91`), 65 marked-historical and 257 labelled, 0 unresolved (lines 66–68). Lesson lines 50–60 match. The 8-vs-77 conflict is a named population issue (QUALITY row "Population unit named").

**Unverified/overstated in the body:**
- "Independent audit" (line 42, 46): the lesson names no author. The supporting files are advisory members of the fleet wave `shokunin12h-20261014-p1-audit`, labelled "Observer" (`KakeGateRerun.md:3`). Non-author status is not evidenced. Call it "advisory re-run by a lane-named observer seat in a fleet audit wave".
- "Stale live prose … `SKILL.md:59`/`:111`" (lines 37–38): `KakeDeadPathSweep.md:76` disagrees with the framing ("not rewritten in place"). Carried, not closed.
- `keeper-timer-inert.md:91` and `publish-queue.md:167` unmarked, present-tense (lines 55–58): confirmed by the sweep; still unrepaired.

**Gate-text review (62–99):** correct on labels and rejected candidates. Fix:
1. C3 "Verdict lines … unverified; not re-measured here; no outside check" — now re-run by `KakeGateRerun.md` (advisory, 13/13). Reword: "advisory re-run in fleet audit wave: 13/13; not a non-author admit/reject".
2. Line 95 "author not named in the file" is correct; add the member path so the reader can check it.
3. Line 70 "S019 was not found under corpus/" is stale: `corpus/SOURCES.md:27` now carries S019.

### 3.5 round-20-verifier-spotcheck (`corpus/lessons/round-20-verifier-spotcheck.md`, 17 lines)
Integrator-written (header line 3: "Written by the integrator, not the lane"). It is **not** a lane lesson and must not be counted as one for C2.

**Checked against the verifier report (`kaika-w3/kake-review.md`):**
- "reviewer re-opened 18 of 18 rows" — `kake-review.md:84`: "rows re-opened 18/18". Verified.
- Admit `crawl-scope-per-host` — `kake-review.md:118`: "agree". Verified.
- Reject S017, S018 — `kake-review.md:116-117`: "agree". Verified.
- "3/3 sampled gate decisions agree" — **wrong count**. `kake-review.md` §5 samples four decisions (rows 1–4: `ghp-custom-domain` admit, S017 reject, S018 reject, `crawl-scope-per-host` admit), all agree. The spot-check row omits `ghp-custom-domain`. Correct to "4/4".
- "S007 wording and S008 '1.35' label corrected by appended errata" — verified: `round-20.md:310-311` ("S008's '1.35' label is withdrawn"); `knowledge/ghp-served-set.md:73-75`.
- "728 citations, 148 moved, 942 comparisons, 0 mismatches" — 728 verified (`post-review-anchors.json`); 148/942/0 not re-derived.
- "freshness 26→4, drift 7→3, missSet 55→55" — matches `round-20.md:291-293`. Verified by lane text, not re-measured.
- "operability selftest 14→15; planted writes 0/25 → 25/25" — matches `round-20.md:169-170`.
- "sources-registry (18 rows)" — true at `9639ec7`. Working tree now has 19 rows (S019 added); say "at 9639ec7".
- "expansion improved (narrow …)" — matches the corrected basis in `round-20.md:298-302`, not the report's original claim (`kake-review.md:157`).
- "quality improved (27 corrections)" — matches `round-20.md:177-179`.

**Unverified / missing in the verifier file:**
1. Post-fix re-verification: the verifier reviewed `02b6dd0`; `kake-review.md` says ADMIT WITH CONDITIONS. The file says "ADMITTED after post-review fixes `9639ec7`" but records no re-review of `9639ec7`. The fix is verified only by the lane's own anchor census. Mark as "integrator-adjudicated; no non-author re-review of 9639ec7".
2. Condition 1 (append-only violation at `02b6dd0`, `kake-review.md:37`) required "waive on the record or re-land". The file does not record which. It records the repair (`9639ec7`). Add the decision explicitly.
3. "discernment improved": no discernment verdict beyond the §5 table is quoted. Mark as "§5 table: 4/4 agree; no separate discernment score in the verifier file".
4. Cross-file staleness (lane-owned, not this seat's to edit): `round-20.md:58-60` ("outside spot-check unavailable") and `round-20.md:194-196` ("still owed") are superseded by this file, but `round-20.md` has no pointer to it. `round-20.md:162-163` ("exit 1 → 0, drift 7 → 0") is superseded by `round-20.md:291-293` (4 unannotated, 3 drift targets remain) without a marker. Recommend an appended pointer in `round-20.md` for the round-20 seat or L1.

**Gate-text advice for this file:** do not add `## Gate` to the integrator file as if it were a lane lesson. The SCORECARD metric (`SCORECARD.md:30`: `ls corpus/lessons/round-*.md | grep -v aggregator | xargs grep -l '^## Gate' | wc -l`) includes this file (16 of 17 files currently carry `## Gate`; this one is the zero). Either add an explicit exclusion for `*-verifier-spotcheck.md` to the metric, or append a clearly labelled integrator record. Do not present it as a lane gate.

## 4. Verified vs unverified — summary

| Item | Status | Evidence |
|---|---|---|
| r16 160-claim census 117/15/7/21 | Recorded (LOG) | `LOG.md:227-228` |
| r16 "ten of 15 stale in unseen classes" | Unverified (not enumerated) | `round-16.md:19-20` |
| r16 sample values (free-read-verbs) | Dated; needs timestamp in body | `round-16.md:47-52` |
| r17 W6 drift and window | Recorded in lesson; evidence absent | `round-17.md:8-20`; `/tmp/kake-r17` absent |
| r17 C6 header classification | Unverified | `round-17.md:39-41` |
| r17 C7 state guard | Unverified; evidence absent | `round-17.md:49-50` |
| r18 W7 33/36 removed, 11 added | Recorded in lesson/LOG; evidence absent | `round-18.md:9-19`; `LOG.md:400` |
| r18 "2026-10-12" prune date | Unsourced; circular | §2.3 |
| r18 PQ-12 "edit landed" reading | Interpretation | `round-18.md:26-31` |
| r18 63 lines / 22 files | Dated; now 64 / 25 | §2.4 |
| r19 13/13, offline 0, explicit-bad 2 | Recorded; advisory re-run matches | `KakeGateRerun.md:11,27,61-62` |
| r19 "independent audit" | Advisory re-run; non-author not evidenced | `round-19-recensus.md:42-48` |
| r19 77 vs 8 populations; 65/257/0 | Recorded; artifact matches | `KakeDeadPathSweep.md:66-68,91` |
| r20 verifier 18/18 rows, admit + rejects agree | Verified | `kake-review.md:84,116-118` |
| r20 "3/3" sampled decisions | Wrong; 4/4 | `kake-review.md` §5 |
| r20 728 citations | Verified; 148/942 not re-derived | `post-review-anchors.json` |
| r20 post-fix 9639ec7 admission | Integrator-adjudicated; no re-review | §3.5 |
| r20 S007/S008 errata | Verified | `round-20.md:310-311` |

## 5. Gate-text template (for each historical gate; pure EOF append)

```
## Gate

Label: <retrospective reconstruction | recorded in round N>. Written <date> by <seat>.
Original sections cited: <line ranges>.
Recorded in round: <what the original round itself wrote, or "no gate section">.

### Candidates
| # | Candidate (section, lines) | Outcome | Basis (artifact, line) |
Outcome vocabulary: recorded-measured · supported (reconstructed) · carried · unverified · superseded by rN · rejected (recorded).
Do not use "admitted" unless the original round recorded an admit.

### Rejected candidates
Only those the original record names; otherwise "Not recorded."

### Outside spot-check
"Not recorded" unless a non-author artifact exists; name its path and whether non-author status is evidenced.

### Evidence presence (date-stamped)
List each /tmp or external path with present/absent at write time. A present directory is not the round's evidence unless its files match.

### Gaps and debt
Named, with owner and unblock. No re-pin or green-by-annotation language.
```

Per-file application:
- round-16 gate (78–179): replace "Admitted" verbs; fix `/tmp/kake-r16` presence sentence; date the S019 statement.
- round-17 gate (58–88): replace verbs; relabel `S019` as own-work tier A; state `/tmp/kake-r17` absent.
- round-18 gate (appended): replace verbs; date the round-21.md statement.
- round-19 gate (62–99): update C3 to the advisory re-run; add member path to the audit line; date the S019 statement.
- round-20-verifier-spotcheck: no lane gate. Correct "3/3" → "4/4"; add post-fix re-review status and the condition-1 decision; exclude from the lane count.

## 6. Limits
- Only read-only inspection. The 13/13, 10/10, 14/14 and 728/148/942 figures were not re-run; they are cited as recorded.
- `/tmp/kake-r16` was inspected only at directory level.
- Fleet-repo artifacts (`/home/vgpnk/Projects/shokunin/.ufo/waves/…`) were checked for presence and for the cited lines/counts, not for full content.
- Round-17 cite target `~/Projects/shokunin/.ufo/reports/round-1/web-properties-publishing.md` was not checked.
- The working tree was changing during this read (other seats appending gates); line numbers reflect the read-time state.
