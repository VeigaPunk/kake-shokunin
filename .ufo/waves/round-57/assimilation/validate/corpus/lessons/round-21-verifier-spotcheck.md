author: hyaku closure (non-author integrator, @m_opus)

# Round 21 — verifier spot-check (non-author closure, hyaku)

Date: 2026-10-20. Closure prompt: fleet `.ufo/prompts/closure/kake-round-21.md`.
Lane HEAD before `5009ecaa1cce10b895617a585ddd3f7c7c923a84`, after
`c2d8da86d05f14e9d4c449a51911091bda7fc33b`. This reviewer authored no round-21
work and dispatched no seat for it; the lane's 64 seats are author-side.

Driver digest (copied from mutable `.ufo/watchdog.log`):

```text
2026-10-20T05:51:51-03:00 launch kake round=21 pgid=3053950 driver=hyaku-inline attempt=1
2026-10-20T06:16:11-03:00 complete kake round=21; hyaku-inline attempt=1
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane | `git log --format='%an %H' -- .ufo/reports/round-21/kake.md` (fleet) | `kake-shokunin 3304dd9aadd32d5260da107ad2a8ae2aa68275ea` | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]` with pointers | pass |
| Cited commits exist, ancestors of HEAD | `git merge-base --is-ancestor <h> HEAD` for df6196b0…, c2d8da86… | exit 0 both; both authored `kake-shokunin <kake@shokunin.local>` | pass |
| No uncommitted round work | `git status --porcelain` | empty | pass |
| Pushed | `git rev-list --count @{u}..HEAD` | `0` | pass |
| Prompt carries template contract | read fleet `.ufo/prompts/kake-round-21.md` (271 lines, committed by kake-shokunin) | §1 MISSION/AXES binding, §2 claims, §2b frontier step, §3 L2 floor, §4 report contract (path, SHONEN, hash, LOG tie), §5 commit/push scope/L0, §6 hyaku addendum incl. write scope and commit-before-report | pass |
| Marker? | — | real report naming checkable pushed commits | not a marker → `ok` |

No step-1 conformance defect found.

## Per-claim re-check (re-measured, not lane scripts)

Independent Python counter over committed blobs (`git ls-tree`/`git show`), not
`measure.mjs`. C1: each of `^source:`, `^verified-at:`, `^recheck:` with a
non-empty value within the first 8 lines of every `corpus/knowledge/*.md`.
C2: exact `^## Gate$` line in lessons matching `^round-\d+(-recensus)?\.md$`.

| Revision | knowledge | complete trios | lane lessons | exact Gate |
|---|---|---|---|---|
| `5009ecaa` | 21 | 4 (17 missing, list matches the round-21 correction register) | 15 | 1 |
| `df6196b0` | 21 | 21 | 16 | 16 |
| `c2d8da86` | 21 | 21 | 16 | 16 |

- **C1 freshness 4/21 → 21/21:** reproduced exactly. Re-measured.
- **C2 operability 1/15 → 15/15 (16/16 with round-21):** reproduced exactly;
  the 14 Gate-less baseline lessons were round-1/3/4/5/6/7/8/9/10/12/16/17/18/19-recensus. Re-measured.
- **Byte preservation (my own audit):** for every baseline file under
  `corpus/knowledge/` and `corpus/lessons/`, after-blob vs before-blob:
  17 = before-bytes preceded by exactly 4 new lines, 14 = before-bytes as prefix
  (EOF append), 14 = identical (includes `round-20-verifier-spotcheck.md` and all
  aggregator lessons). Zero modified. The one `-1` line in `round-16.md` is the
  missing-final-LF boundary the lesson declares.
- **Gate evidence (evidence-verified, not executed):** `scripts/corpus-contract.mjs`
  registry row present in `SKILL.md` §"Publishing-corpus contract gate — round 21"
  (name, kind, entry, verdict map 0/1/2/64, `--selftest`, frozen proof, write scope,
  owner). `corpus-selftest.json` stdout `selftest: 7/7 passed`, exit 0, revision
  df6196b0. `replay.json`: `REPLAY_PROOF: PASS (files=36, runs=2, failures=0)`,
  digests verified, stable red baseline exit 1. `corpus-after.json` exit 0,
  knowledgeChecked 21, lessonsChecked 16, findings []. `gate-digest.json` sha256
  `ca6f685e…ed29` equals `sha256sum` of the committed gate at c2d8da86;
  `git diff df6196b c2d8da86 -- scripts corpus` touches only `round-21.md`, so the
  measured revision equals the closed tree for the gate and claim populations.
- **No owned-axis harm:** `git diff 5009ecaa c2d8da86 -- SCORECARD.md` is a pure
  append (round-21 section, HOLD 10 for both claims); no score row changed.
  `corpus/knowledge/freshness-pins.json` and `scripts/freshness-sweep.mjs` unchanged
  (no pin weakening). New prefixes are labelled historical-not-live-reverified.

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| freshness | improved | C1 re-measured 4/21→21/21; bounded to provenance discoverability, explicitly not live re-verification; score HOLD 10 |
| operability | improved | C2 re-measured 1/15→15/15; registered gate with committed selftest 7/7 and frozen red-baseline replay |
| depth | unchanged | no knowledge body changed (prefix-only) |
| coverage | unchanged | same 21 entries |
| adjacency | unchanged | no province change |
| calibration | unchanged | no calibration claim |

## Discernment spot-check (round-21 `## Gate`)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| `vault-properties.md` provenance prefix crediting ed0b632, not dd4eabf | admit | `git show ed0b632 --stat` (adds the 83-line entry; `157` occurs twice in its blob) and `git show dd4eabf -- corpus/knowledge/vault-properties.md` (one line-ref change `:891-894`→`:903`) | agree | header attribution matches history; header labels state as historical, operator restore-or-retire |
| Draft header claiming `corpus/CORPUS.md` registered by L1 (`w1/Knowledge18.md`, `w1/MetadataSafety.md`) | reject | `ls corpus/CORPUS.md` → no such file; `git log --all -- corpus/CORPUS.md` → 0 commits; current `publish-queue.md` line 1 cites S019 instead | agree | the claimed path never existed; landed header was corrected |
| Weakening the paths gate or its miss-set to obtain green | reject | `git diff 5009ecaa c2d8da86 --stat -- corpus/knowledge/freshness-pins.json scripts/freshness-sweep.mjs` → empty | agree | pins untouched; red paths verdict honestly retained |

New `SOURCES.md` row re-opened: **S019** (tier A own-work, mined, used-by
`corpus/lessons/round-21.md`). Per CORPUS §Rules 1 the URI, access date and
quote live in the round Gate: `file://…/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`,
2026-10-20, quote “Each `knowledge/` entry opens with `source:`, `verified-at:` and
`recheck:`” (9 words ≤25). Re-opened `git show e737d2ea:skills/shokunin/protocol/CORPUS.md`:
line 18 reads exactly that; line 19 carries the `## Gate` clause; sha256
`b6ed4476…21bf` matches the lesson. Agree.

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
→ `kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`, exit 0.

## Trend verdicts

- **expansion: unchanged** — 21 knowledge entries before and after; no
  capability row; S019 is maintenance evidence, not new ground.
- **quality: improved** — bounded: 17 entries gained honest historical
  provenance and 14 lessons explicit decision records with zero original bytes
  modified (audit above); no admitted entry failed re-check.
- **discernment: improved** — this outside spot-check agrees with the gate on one
  admit and two rejects (LEARNING.md `improved` row). The lane's own report said
  `unchanged` pending this act; that was correct at write time.

## Admission

All declared claims re-measured and verified; no axis harmed → **admitted**.

## Routed defects / notes for the lane (next round)

1. Existing paths gate `freshness-sweep.mjs --section=paths` remains red (exit 1,
   three drift targets / four legacy locations, missSet 55) — pre-existing,
   honestly carried; still owed (restore or retire per operator).
2. `anchor-census.mjs` exit 1 retained (78 baseline-inapplicable diagnostics in
   author wave reports); an evidence helper, not a registered gate — keep it out
   of any gate claim or reduce its scope to historical bytes.
3. Reconstructed old Gates in `round-4.md:50`, `round-9.md:185`, `round-16.md:171`
   keep read-time statements that S019 / the round-21 lesson were absent; they are
   superseded only by the round-21 register. Readers of those files alone may
   misread them; future reconstructions should be written after their sources land.
4. SHONEN: all four boxes `[~]` author assertion; box 2 points to a local corpus
   repair, not a domain end-to-end task. Not fully checkable by a non-author yet;
   promotion stays operator-owned.
