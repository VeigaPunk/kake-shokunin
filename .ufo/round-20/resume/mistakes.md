# Round-20 resume — mistakes mined (kake)

Base: `cb807bc8d8bc`. Every lane pointer is a **base-commit** line, not the concurrently
edited worktree (`corpus/README.md` is modified this session); the two old-commit T1
pointers are verified with `git -C "$L" show <commit>:corpus/README.md`. Verification command:
`git -C "$L" show cb807bc:<path> | grep -nF -- '<cited fragment>'` (ranges checked with
`awk -v ls=...`); ART lines were checked with `grep -n` in the ART file. `L` = the lane worktree; `ART` = read-only
`/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/kake-art.md`.
C1–C3 are this round's pre-registered claims; the Fix column records planned work, not
executed or verified results. All non-post-base pointers below were re-verified
2026-10-19 at `cb807bc` with the listed command. `corpus/lessons/round-20.md`
§Round-20 resume is this round's post-base append (not present at `cb807bc`),
so it is cited by heading for this round's new evidence.

## Mistakes

| # | Class | Evidence pointer (base lines) | Captured-by | Fix |
|---|---|---|---|---|
| M1 | False green in the citation gate: target-wide OR let an absence note on one occurrence hide an unannotated instruction elsewhere | `corpus/lessons/round-20.md:12-18,28-34`; `corpus/QUALITY.md:9` | `Citation-local absence` (`corpus/QUALITY.md:9`) | C1: annotate/repair all 26 measured locations in place; `pathsMissSet` stays 55, `newMissing` stays 0 |
| M2 | Shape-only evidence violation: controlled fixture environment values serialized, then echoed through captured output | `corpus/lessons/round-20.md:124-143`; `LOG.md:544-559`; `corpus/QUALITY.md:13` | `Shape-only probe environment` (`corpus/QUALITY.md:13`) | Closed by correction `9825b2a` plus append-only erratum; C1–C3 keep symbolic output only |
| M3 | Authority inflation: 32 rendered scopes treated as a dispatched wave; launch counter 16 treated as completed rounds | `corpus/lessons/round-20.md:5,53-60`; `LOG.md:470-489`; `corpus/QUALITY.md:12` | `Admission authority` (`corpus/QUALITY.md:12`) | No dispatch in-lane; named debt, owner host owner/integrator (`routing-blocker.json`) |
| M4 | Self-source confinement: write-region scanner opened on prose/literal BEGIN tokens, so a write planted in a later function survived the selftest | `corpus/lessons/round-19-recensus.md:44`; `SKILL.md:212` (gate-registry row only) | `none` | C2: standalone marker lines plus a permanent mutation case for an out-of-region write |
| M5 | Dead-path population units conflated: 77 live citations vs 8 fleet-level hits vs 26 unannotated locations are different contracts | `corpus/lessons/round-19-recensus.md:52-53`; `corpus/lessons/round-20.md:110-111` | `none` | C1 closes only the 26-location contract; 77/8 reconciliation is named debt, owner kake |
| M6 | Stale live counts/prose beyond the named sites; "every `origin-work` cite is marked" was false | `corpus/lessons/round-19-recensus.md:48`; `SCORECARD.md:32,64` | `SKILL.md:199-203` (counts are dated measurements) | Historical-qualified (`SCORECARD.md:32`); citation half handled by C1; count repair is named debt, owner kake |
| M7 | Clock mix: journal `Starting` line written as the history `at` | `LOG.md:31-33` | `none` | Closed by append-only r14 erratum (`LOG.md:31-33`); no code change |
| M8 | "Byte-frozen" misclaim: raw sha varies per fetch via Cloudflare cfemail re-encoding | `LOG.md:42-44` | `none` | Closed by erratum naming the cfemail-normalized sha (`LOG.md:44`); no rewrite |
| M9 | Journal start-time misread: `03:32:06` recorded, `04:14:50` correct | `SCORECARD.md:74` | `none` | Closed by append-only correction; move-log row 10 records it |
| M10 | Proposed cmdProbe F1 merge guard refuted on `probe <id> --all`; corrected rather than shipped | `SCORECARD.md:72`; `corpus/handoffs/cmdProbe-merge-fix.md:5-10` | `none` | Closed by handoff/refutation record; guard was not shipped |
| M11 | No independent non-author spot-check of one admit and one reject | `corpus/lessons/round-20.md:58-60`; `SCORECARD.md:112` | `Admission authority` (`corpus/QUALITY.md:12`) | Named debt, owner host owner/operator; cannot close in-lane |
| A1 | Validator treated as identity: an ETag flip read as content change, then "refuted" by a fetch that hit another replica | `corpus/knowledge/publish-queue.md:255-261`; `LOG.md:245-247`; `corpus/lessons/round-16.md:35-38` | `none` | C3: S009/S010 rows plus `ghp-etag-anatomy`; ETag = mtime/length, never a freeze metric |
| A2 | Platform mechanism inferred from workflow shape: "served set ≡ `origin/main` tree" / full-tree artifact | `corpus/README.md:26,52-53`; `SKILL.md:227`; `corpus/lessons/round-7.md:21-25`; `corpus/knowledge/sitemap-orphan-audit.md:20-24` | `none` | C3: S001/S002/S003/S004/S006/S008 rows plus `ghp-served-set`; annotate `round-7.md` append-only |
| A3 | Repo file read as platform configuration: "`CNAME` file pins `ds4cc.com`" | `corpus/knowledge/publish-channels.md:9`; `SKILL.md:16` | `none` | C3: S003/S005/S007 rows plus `ghp-custom-domain`; correct both sites |
| A4 | Tier-B version number admitted: Firefox 114 vs Firefox 144.0 `interactionId` | `ART:322` (R3), `ART:334` (M4) | `none` | C3 registry admits tier A only; S018 rejection retained; no lane claim depends on the number |
| T1 | Index continuation silently dropped by an edit; sentence ended at "intentionally" | `corpus/README.md:60`; `dd4eabf:corpus/README.md:45`; `cd5b381:corpus/README.md:27-28` | `none` | Restored this round from `cd5b381` (worktree `corpus/README.md:61-63`, uncommitted at write time) |

## Proposed QUALITY.md criteria

Covers every class whose `Captured-by` is `none` (M4, M5, M7–M10, A1–A4, T1); historical
classes M7–M10 share one append-only criterion.

| Criterion | Admit | Reject | Grounding |
|---|---|---|---|
| Platform mechanism (served-set, CNAME) | Serving, ignoring and validating behavior cites a tier-A source at a pinned tag or SHA, or the platform's own doc with fetch date, plus a recheck argv. | Inferring behavior from repo files or workflow shape alone; taking versions, dates or mechanisms from tier B/C without a tier-A recheck. | `corpus/lessons/round-7.md:21-25` (the shape inference); `corpus/README.md:52-53`; `corpus/knowledge/publish-channels.md:9`; `SKILL.md:16,227`; `ART:322,332-334`; `corpus/lessons/round-20.md` §Round-20 resume. |
| Validator is not identity (ETag) | A validator claim names the generating mechanism, decodes the literal, and states what the validator cannot prove; content identity uses a normalized digest. | A validator flip as a content change; a matching validator as byte identity; a cross-replica fetch as refutation. | `corpus/lessons/round-16.md:35-38`; `corpus/knowledge/publish-queue.md:255-261`; `LOG.md:245-247`; `corpus/lessons/round-20.md` §Round-20 resume. |
| Self-source confinement | Write-region markers are exact standalone comment lines; mutation proof covers every out-of-region top-level statement position; a command names the covered span. | Token membership anywhere in a line as a marker; header prose or checker literals opening the region; a tally with no planted out-of-region write. | `corpus/lessons/round-19-recensus.md:44`; `SKILL.md:212`; `corpus/lessons/round-20.md` §Round-20 resume. |
| Population unit named | Every dead-path/count claim names its population (live citations, unannotated locations, pinned miss-set), scanner contract and command. | Reporting 77, 8 and 26 as one number; comparing counts from different units; treating a dated count as a constant. | `corpus/lessons/round-19-recensus.md:52-53`; `corpus/lessons/round-20.md:110-111`; `SKILL.md:199-203`; `corpus/lessons/round-20.md` §Round-20 resume. |
| Digest normalization before comparison | Raw-byte identity claims name every normalization (cfemail, seed tag, entities) and show the normalized digest. | "Byte-frozen" from a raw sha across fetches; sha comparison of rewritten hosts. | `LOG.md:42-44`; `SKILL.md:240-246`; `corpus/lessons/round-20.md` §Round-20 resume. |
| Append-only correction/refutation | Corrections and refutations are appended with date, commit and line pointer; original text is preserved; a refuted guard is recorded and not shipped. | Rewriting or amending lesson/log history; silent removal; shipping an untested guard. | `LOG.md:31-33,42-44`; `SCORECARD.md:72,74`; `corpus/handoffs/cmdProbe-merge-fix.md:5-10`; `corpus/lessons/round-20.md` §Round-20 resume. |
| Index continuity | Edits to index/list prose preserve or explicitly supersede every continuation; the diff is read before commit. | Leaving a sentence that ends in a dangling modifier with no continuation or pointer. | `corpus/README.md:60`; `dd4eabf:corpus/README.md:45`; `cd5b381:corpus/README.md:27-28`; `corpus/lessons/round-20.md` §Round-20 resume. |

## Sweep

Pattern: `git -C "$L" show cb807bc:<file> | grep -icE '<pattern>'` (`SKILL.md` is repo-root).

- M1: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'unannotated'` → 1 → captured.
- M2: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'shape-only'` → 1 → captured.
- M3: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'launch counter'` → 1 → captured.
- M4: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'confinement'` → 0; `git -C "$L" show cb807bc:SKILL.md | grep -icE 'confinement'` → 1 at `:212` (gate registry, not a rule) → none.
- M5: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'dead path'` → 0; `git -C "$L" show cb807bc:SKILL.md | grep -icE 'dead path'` → 0 → none.
- M6: `git -C "$L" show cb807bc:SKILL.md | grep -icE 'pinned literal'` → 1 → captured.
- M7: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'clock|timestamp|mtime'` → 0 → none.
- M8: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'normaliz'` → 0 → none; the SKILL rule at `:240-246` is kimi-host-specific.
- M9: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'clock|timestamp|mtime'` → 0 → none.
- M10: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'refut'` → 0; `git -C "$L" show cb807bc:SKILL.md | grep -icE 'refut'` → 0 → none.
- M11: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'non-author'` → 1 → captured.
- A1: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'validator|etag'` → 0; `git -C "$L" show cb807bc:SKILL.md | grep -icE 'validator|etag'` → 0 → none.
- A2: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'served set|platform'` → 0; `git -C "$L" show cb807bc:SKILL.md | grep -icE 'served set|platform'` → 0 → none.
- A3: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'CNAME'` → 0 → none.
- A4: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'tier'` → 0 → none.
- T1: `git -C "$L" show cb807bc:corpus/QUALITY.md | grep -icE 'truncat'` → 0 → none.

## Conflicts (verbatim, for the canonical judge)

- `corpus/lessons/round-19-recensus.md:52-54`: "A lane-specific sweep (`.ufo/waves/shokunin12h-20261014-p1-audit/members/KakeDeadPathSweep.md`) measures **77 live citations** of deleted paths at this revision — not the 8 the fleet-level sweep reported, whose method was coarser."
- `corpus/lessons/round-19-recensus.md:48`: "`SCORECARD.md:22`'s "every `origin-work` cite is marked absent-historical" is false — `keeper-timer-inert.md:91` and `publish-queue.md:167` are unmarked and present-tense." The inner `keeper-timer-inert.md:91` /
  `publish-queue.md:167` tokens are quoted lesson text; the resolving pointer is
  `corpus/lessons/round-19-recensus.md:48`.
- `ART:333` reports lane `corpus/knowledge/publish-channels.md:9` "`CNAME` file pins `ds4cc.com`" contradicted by S005's "any existing `CNAME` file is ignored" under Actions publishing. Reported, not re-opened or repaired here.
