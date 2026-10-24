# NoTrade — round-21 w1 critic: no-harm attack on C1 prefixes / C2 EOF Gates

Seat: `KakeR21.NoTrade` (critic, leaf). Base `5009ecaa1cce10b895617a585ddd3f7c7c923a84`.
Axes attacked: **freshness** (citation gate `§paths`, reference integrity) and **operability** (byte-preservation and gate checks that main runs once).
Only file written in the repo: this report. Scratch is outside the repo, in `/tmp/kake-r21-notrade/`
(`base/`, `wt2/` = `git archive HEAD` and a tar snapshot of the mid-flight worktree, taken
2026-10-20 ~06:0xZ with 35 dirty paths; `base.json`, `wt2.json` = `freshness-sweep.mjs --offline --section=paths --json`).
No tools were installed or updated.

The verdict on the planned trade: **the trade is not no-harm in its current state.** The byte rule holds and no
preexisting annotation was masked. However, the known red gate got **wider** (C2-W1 and C1-W2 below), and the round
introduced **unbound line references** (C1-W3 and C2-W4 below). Each fix is small and stays within the byte rule.

## What holds (tested, no counterexample found)

| Check | Result | Evidence |
|---|---|---|
| C1 prefixes are pure prefix | 17/17 modified knowledge files: worktree bytes = 4-line prefix + exact HEAD bytes (`w.endswith(git show HEAD:f)`) | eval over `git diff --name-only HEAD`, wt2 snapshot |
| C1 coverage | 21/21 knowledge entries have `source:`/`verified-at:`/`recheck:` in their first 8 lines (4 entries were already there at base, 17 are new) | `head -n 8 \| grep -cE '^(source\|verified-at\|recheck):'` = 3 on every file |
| C2 appends are pure EOF | 14 modified lessons all start with exact HEAD bytes. `round-20.md` already had a Gate and is unchanged. The aggregator and verifier lessons are unchanged | same eval |
| Scanner-window masking of preexisting cites | **0 flips.** No base line that carries a `PATH_RE` hit changed its ±2 annotation status after the +4 shift or the EOF append. The window of shifted line 5 (old line 1) reaches metadata line 3, but every old line 1 is a heading with no `~/` cite | re-implementation of `annotate()` (non-strict) over base and wt2 with line mapping |
| `declaredAbsentIndirect` set | Same 3 targets at base and wt2 (`origin-work/open-bug-bounties`, `ufofsdbeta`, `webzites/scripts`). Only the line moved: `publish-queue.md:233→237` | `wt2.json` |
| Round-20 frozen proof | `.ufo/round-20/frozen/citation-locality/expected.json` pins only the hermetic `corpus/knowledge/note.md` fixture, so the prefixes do not affect it | grep |
| Script | `scripts/` has no diff vs HEAD, so the selftest behaviour cannot have moved | `git status` |

## Counterexamples

### C2-W1 — The red gate widened: 3 new unannotated misses, all in newly authored Gate text

Base `§paths` result: exit 1, **drift 3**, newMissing 0. The drift targets are:
- `~/Projects/plazir-15-site` at `drift-detection.md:73` and `fleet-registry.md:53`
- `~/Projects/webzites/bin/webzites.mjs` at `free-read-verbs.md:317`
- `~/Projects/webzites/scripts/kimi-surface.mjs` at `round-6-aggregator-audit.md:48`

wt2 result: exit 1, **drift 6**. The 3 base targets are still there; the knowledge cites moved +4 (`:77`, `:57`, `:321`). These are new:
- `~/Projects/webzites` at `corpus/lessons/round-4.md:46`. The line says "historical records (see the r20 annotations on lines 5-6)" and has no absence word within ±2.
- `~/projects` at `corpus/lessons/round-17.md:64,65` (Gate candidate bullets C1/C2). Base had this target in declaredAbsent; it is now drift.
- `~/Projects/webzites/reports/r9-publish-queue.md` at `corpus/lessons/round-9.md:179`. This is the first line of a multi-line `ls -l` recheck; the word "missing" on `:182` is 3 lines away.

Impacted axes: freshness (harm), operability (the operator sees a different red).
Smallest correction: the Gate text is new in round 21, so its authors can edit it. Put a citation-local absence note on each line, or within ±2. The note must name the target and its dated event, to meet the QUALITY "Absence annotation content" bar. Example: "`~/Projects/webzites` absent — gone in the 2026-10-12 `~/Projects` prune". Alternatively, describe the path without the `~/` spelling.

### C1-W2 — 5 new not-pinned misses (`newMissing` 0 → 5), from metadata recheck lines and the round-9 Gate

| New miss | Cite | Pinned absent ancestor |
|---|---|---|
| `~/Projects/ds4cc-marketplace/render.yaml` | `publish-channels.md:3` | `~/Projects/ds4cc-marketplace` |
| `~/Projects/plazir-15-site/.github/workflows/pages.yml` | `publish-channels.md:3` | `~/Projects/plazir-15-site` |
| `~/Projects/webzites/fleet` | `mirror-pitfalls.md:3`, `round-18.md:84` | `~/Projects/webzites` |
| `~/Projects/webzites/state/probe-latest.json` | `drift-detection.md:3` | `~/Projects/webzites/state` |
| `~/Projects/webzites/reports/sentinel-sourceless-extract-r9.md` | `round-9.md:182` | `~/Projects/webzites/reports` |

All five are declared absent (`newDrift` 0), but `verdictOf` fails on `newMissing > 0`. The VERDICT line therefore changes from `3 unannotated miss · 0 NOT in pins.pathsMissSet` to `6 · 5`.

Smallest correction: the pins comment describes the protocol: "Re-pin = edit this file in the SAME commit that lands the corrected corpus prose". Following it, absorb exactly these 5 into `pins.pathsMissSet` (55 → 60) in the integration commit and report the growth. Absorbing them is honest because every one sits under an ancestor that is already pinned absent. The other option is to drop the `~/` spellings from the recheck lines.

### C2-W3 — False annotation in new Gate text (the selftest-F class)

`round-9.md:182` reads "Any missing file keeps its claim unverified until restored or retired". That is a conditional, not a declaration. `:177` says the status of `dead-slot-recreate-readiness-r9.md` and `sentinel-sourceless-extract-r9.md` is "unknown here". The sweep nevertheless records `sentinel-sourceless-extract-r9.md` as declaredAbsent, with evidence `{word:"missing", line:182, direct:true}`. This is the false green that `corpus/QUALITY.md:14` rejects ("an absence word that merely falls inside the ±2-line window").

Smallest correction: rephrase the conditional without the absence vocabulary (for example "Any file not found keeps…"). Or state the actual absence, which the absent ancestor `~/Projects/webzites` entails.

### C1-W3 — Reference integrity: the new metadata contradicts its own file

`publish-channels.md:1` (new `source:` line) says the S001–S007 corrections are "cited by the round-20 corrections (lines 54-57)". After the +4 prefix those bullets are at **lines 58-61**, and lines 54-57 are now ordinary body text.
Smallest correction: change the number in the new line to `58-61`, or anchor it by text ("the four `Base …` r20-correction bullets at EOF"). This touches no preexisting byte.

### C2-W4 — Reference integrity: newly authored Gate text cites knowledge line numbers in two numbering bases, without revision binding

The 42 new `knowledge/<file>.md:N` refs in appended Gate regions all point into the 17 files that shifted +4 this round. Spot checks:

| New ref | Numbering base | Notes |
|---|---|---|
| `round-8.md:74` → `kimi-subpath-audit.md:39-43` | **base** | "75 … `f3d2ecd`" is at base 39-43; wt 39-43 is different text |
| `round-8.md:73` → `kimi-subpath-audit.md:1-5` | **base** | wt lines 1-5 are the new metadata plus the heading |
| `round-8.md:74` → `free-read-verbs.md:211` | **base** | |
| `round-12.md:82` → `publish-queue.md:32` | **base** | Base 32 = PQ-12; wt 32 = PQ-8 |
| `round-12.md:81` → `keeper-timer-inert.md:3-16` | **base** | |
| `round-3.md:33,47` → `drift-detection.md:4` | **base** | wt line 4 is the blank separator |
| `round-3.md:40` → `publish-queue.md:36` | **worktree** | Base 36 is `## Ordering DAG`; wt 36 = PQ-12. This mixes both bases inside one Gate |

Full list (recomputed from wt2):
- `round-10.md`: lines 72-79
- `round-12.md`: lines 80-95
- `round-17.md`: line 69
- `round-18.md`: lines 85, 86, 100
- `round-19-recensus.md`: lines 81, 83
- `round-3.md`: lines 33-47
- `round-8.md`: lines 73-84
- `round-9.md`: lines 122, 123, 174

`round-12.md:66` binds its own line numbers to "base `5009eca`" but not its knowledge refs. Impacted axis: freshness (a reader following the ref lands on the wrong claim).
Smallest correction: give each Gate one binding sentence: "knowledge line numbers are at base `5009eca`, before the round-21 4-line metadata prefix (add 4 for the current file)". Then change `round-3.md:40` to `publish-queue.md:32`. Alternatively, convert all of them to post-prefix numbers in one pass.

### C1-W5 — Preexisting current-voice refs into prefixed files are now off by 4 (byte rule forbids repair in place)

About 208 preexisting `…md:N` refs into the prefixed files carry no base qualifier (counted by a regex heuristic; most are in historical lessons). Some are present-tense claims:
- `keeper-timer-inert.md:101` ("`publish-queue.md:32` **now** reads 'operator config edit'"; it is now `:36`)
- `corpus/QUALITY.md:15` (`publish-channels.md:9`)
- `ghp-custom-domain.md:35` (`publish-channels.md:5-9`)
- `scripts/freshness-sweep.mjs:309` comment (`publish-queue.md:219-224`)
- `LOG.md:232-237,637-649`

`publish-queue.md:229-231` itself warns "the line-number pin WILL shift on the next edit — re-grep".
Smallest correction (L1-owned): add one appended erratum in the round-21 lesson or SKILL. It states that every pre-round-21 in-corpus line ref into the 17 prefixed entries uses pre-prefix numbering (+4 now). This keeps all bytes and gives readers the offset.

### Lower severity

- **C2-W6 — heading exactness.** `round-4.md:44` and `round-8.md:60` read `## Gate — round-21 retrospective reconstruction`. The exact match `^## Gate$` gives 13/15, while `^## Gate\b` gives 15/15. The planned `scripts/corpus-contract.mjs` must use the same predicate the seats assumed. Smallest fix: use an exact `## Gate` heading with the label in the first body line, or document `^## Gate(\s|$)`.
- **C2-W7 — line-based append check false alarm.** `round-16.md` at HEAD has no final newline (last byte `.`). The append starts `\n\n`, so the bytes are preserved, but the QUALITY "Append-only tails" stripped-diff (line-based) will show line 75 as changed (`\ No newline at end of file`). Use a byte-prefix check (below), not `diff <(git show) <(head -n N)`.
- **Stale present-tense claims written mid-flight.** `round-3.md:33` says "`corpus/lessons/round-21.md` does not exist yet"; `round-10.md:68`, `round-17.md:85` and `round-4.md:48` say the same at read time. `round-21.md` now exists as an untracked file. "At read time" phrasing is honest; "does not exist yet" becomes false after integration.
- **S019 cites a script that does not exist.** `corpus/SOURCES.md:27` (S019) names `scripts/corpus-contract.mjs`, but only `freshness-sweep.mjs` and `probe-delta.mjs` exist in the wt2 snapshot. `PATH_RE` cannot see this relative cite (relativeCites 634 → 740). Main must land the script or amend the row before commit.
- `SOURCES.md` is an insert-only change (one row at line 27). The new Gates' `corpus/SOURCES.md:27` refs use post-insert numbering, so they are consistent.

## Checks for main to run once, after integration

Run from `/home/vgpnk/Projects/shokunin/kake-shokunin`.

1. **Prefix byte check** (expect 17 OK and an exact 4-line prefix):
   `for f in $(git diff --name-only HEAD -- corpus/knowledge/); do s=$(git cat-file -s HEAD:$f); n=$(stat -c%s $f); tail -c $s $f | cmp -s - <(git show HEAD:$f) && echo "OK $f +$(head -c $((n-s)) $f | wc -l)" || echo "FAIL $f"; done`
2. **EOF byte check for lessons** (expect OK on 14; covers `round-16.md` without a false alarm):
   `for f in $(git diff --name-only HEAD -- corpus/lessons/); do s=$(git cat-file -s HEAD:$f); cmp -s -n $s <(git show HEAD:$f) $f && echo OK $f || echo FAIL $f; done`
   Also: `git diff --quiet HEAD -- corpus/lessons/round-20.md corpus/lessons/*aggregator* corpus/lessons/round-20-verifier-spotcheck.md`
3. **Coverage.** The trio check returns 3 on each of the 21 entries: `head -n 8 F | grep -cE '^(source|verified-at|recheck):'`. Also run `grep -c '^## Gate'` on the 15 lane lessons and reconcile it with the corpus-contract predicate (C2-W6).
4. **Known red gate, preserved exactly:**
   `node scripts/freshness-sweep.mjs --offline --section=paths --json`
   Expected after the fixes: exit 1, and drift is exactly the 3 base targets:
   - `~/Projects/plazir-15-site` (`drift-detection.md:77`, `fleet-registry.md:57`)
   - `~/Projects/webzites/bin/webzites.mjs` (`free-read-verbs.md:321`)
   - `~/Projects/webzites/scripts/kimi-surface.mjs` (`round-6-aggregator-audit.md:48`)

   Also expect `newMissing` 0 (with the 5 re-pinned and pathsMissSet at 60, or with the `~/` spellings removed), the `declaredAbsentIndirect` set unchanged, and resolve gaining only `~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`.
   Compare with `/tmp/kake-r21-notrade/base.json` (base: exit 1, drift 3, newMissing 0, declaredAbsent 52, resolve 5, unresolved 8).
5. **Script unchanged:** `git diff --quiet HEAD -- scripts/freshness-sweep.mjs`. Optionally run `node scripts/freshness-sweep.mjs --selftest` once; it is hermetic.
6. **Line-ref spot check.** Re-open C1-W3 (`publish-channels.md:1`) and C2-W4 (`round-3.md:40` vs `:33/:47`, and `round-8.md:73-74`) after the authors fix them.

## Limitations

- wt2 is a mid-flight snapshot. Seats were still writing, and C2-W1 grew from 2 to 3 new drift targets between my two snapshots. Main's single post-integration run is authoritative.
- The masking re-implementation covers non-strict mode only. The `pathsAbsenceStrictSameLine` pin is not set.
- The ~208 unqualified-ref count is a regex heuristic: it treats "Base", "at base", "historical" and "as of rN" as qualifiers. Only the refs named above were verified by content.
- Not assessed: whether the field content is true (owned by the scribes, SourceScope and MetadataSafety) or the gate requirements (owned by GateContract).
