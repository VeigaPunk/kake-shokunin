# W2 ScratchAudit — did any W1 seat write outside the lane?

Item: audit the routed round-25 `/tmp` defect for round 26. Read-only; no tools installed or
upgraded; no writes outside this report.

## Verdict

**DISAGREE** with a clean bill. No W1 seat declared a `/tmp` write, and no kake-round-26
scratch is detectable in `/tmp`. But one W1 report — RowS012 — was **written at the fleet
root**, outside the lane, and the wave's own record says so. The repair was byte-exact and
no freshness verdict is affected. Severity low; the defect is that the round-26 lesson's
fix/witness names only `/tmp` and would not catch the variant that actually occurred.

## 1. Declared writes and tool use (64 `w1/*.md`, 65 files incl. `swarm-registry.json`)

No report declares a `/tmp` write. `/tmp` appears in six reports, every time as a
prohibition, refusal, or disclosure:

- `w1/PairS001GhpServedSet.md:86` — "Nothing written except this report; no /tmp; no builds, tests or linters".
- `w1/PairS008GhpServedSet.md:53` — a prior repro was **not re-executed** because "Its scratch directory uses `mktemp`, which writes under /tmp, and lane bounds bar that"; `:61` "no /tmp use".
- `w1/PairS031StaticCanonicalPrefl.md:66` — "No scratch files were written and nothing was written to `/tmp`."
- `w1/RecheckCounter.md:58` — "Nothing is written to /tmp, per the round-25 disclosure at `LessonScribe.md:84`."
- `w1/RecheckFixtures.md:63` — "nothing written to `/tmp`."
- `w1/LessonScribe.md:78,84` — the round-26 rule itself ("nothing under `/tmp`"; receipts must state where scratch lived).

Two reports make no write/scratch statement at all: `w1/PairS002GhpServedSet.md` and
`w1/RowS029.md` (no tooling paragraph; `grep -cE 'report|Report'` = 0 in both). Under
`LessonScribe.md:84` ("A receipt that does not state this is not counted as clean") these
two cannot be counted clean on their face. This is a disclosure gap, not a write.

Every report that does describe writes names lane-internal paths only (`w1/…`, `sandbox-counter/`,
`sandbox-tests/`, report file). No report declares a fleet-root or `/tmp` write.

## 2. One W1 report did exist at the fleet root — RowS012

- `.ufo/waves/round-26/misroot-RowS012.txt` (in candidate `e28312b1`, mtime 13:02):

  ```
  bab0163ae0ce64325f1604c839b29eb9916163e389f7b7323fc1743204e55456  /home/vgpnk/Projects/shokunin/.ufo/waves/round-26/w1/RowS012.md
  bab0163ae0ce64325f1604c839b29eb9916163e389f7b7323fc1743204e55456  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/w1/RowS012.md
  moved; fleet copy removed
  ```

  The lane copy still hashes to `bab0163a…` (`sha256sum w1/RowS012.md`), and its mtime is
  `12:28:49`, i.e. the authoring time, consistent with a move rather than a later copy.
- `LOG.md:999-1000`: "One report was misrooted at the fleet root and moved byte-exact
  (`misroot-RowS012.txt`)."
- Cause is visible in the dispatch: `w1-dispatch.json` `/taskCall/tasks[11]` gives the
  report path **relative** — `Report: write your scoped findings to .ufo/waves/round-26/w1/RowS012.md` —
  while `w1-spec.json` `/context` says the path is "relative to /home/vgpnk/Projects/shokunin/kake-shokunin"
  and "Never write to /tmp or outside the lane". The seat resolved the relative path against
  its fleet-root cwd.
- Current state: `find /home/vgpnk/Projects/shokunin -maxdepth 6 -name RowS012.md -not -path '*/kake-shokunin/*'`
  returns nothing; the fleet `.ufo/waves/round-26` directory no longer exists
  (`ls .ufo/waves/round-26` → "No such file or directory"); `git -C /home/vgpnk/Projects/shokunin
  status --porcelain | grep -c round-26` → `0`.

Attribution: a W1 report objectively existed at the fleet root and the wave records it as a
seat misroot. That the *seat* rather than a later integration step placed it there follows
from the preserved 12:28:49 mtime and the dispatch's relative path. [INFERENCE on the
seat-vs-harness causality; the fleet-root existence itself is observed.]

No other W1 seat is implicated: only one `misroot-*` receipt exists for the round, and the
fleet sweep found no other owned file.

## 3. The prescribed fleet check is structurally blind to the lane

`git -C /home/vgpnk/Projects/shokunin status --porcelain` cannot show kake round-26 files:

```
.gitignore:1:*-shokunin/    kake-shokunin
.gitignore:1:*-shokunin/    kake-shokunin/corpus/SOURCES.md
```

The lane is entirely ignored in the fleet repo (`!! kake-shokunin/`), and fleet
`.gitignore` line 5 also hides `.ufo/waves/*/*-scratch/` scratch. Lane-internal truth comes
from the lane's own repo: `git -C kake-shokunin status --porcelain -uall` shows only
round-26 artifacts under `.ufo/waves/round-26/` (`__pycache__/source_text…pyc`, `verification/*`,
`w2-*`, `w2/*`), no modified tracked file, no stray lane-root file; `HEAD` is the candidate
`e28312b1` ("round-26: re-verify 32 cited sources and append adjudicated corrections",
13:08:15). At the time of the misroot the fleet-root copy *would* have appeared as
`?? .ufo/waves/round-26/…`, so the check is capable of catching that one class — but it can
never clear the lane itself.

## 4. `/tmp` negative evidence

No file under `/tmp` created 12:20–13:12 (≤3 MB) contains `r26-recheck`, `sandbox-counter`,
`sandbox-tests`, `RowS0NN`/`PairS0NN`, `ghp-served-set`, `static-canonical-preflight`,
`crawl-scope-per-host`, `ghp-etag-anatomy`, `ghp-custom-domain`, `S031-1`, or `S020-1`
(`find … -print0 | xargs -0 grep -l -F …` → no matches). Three `/tmp` files match
`kake-shokunin`: `/tmp/claim-ledger.sh` (11:00, pre-window) and `/tmp/r24-mon-1.json` +
`/tmp/r24-mon-1.keep` (13:01:40/49). The `r24` pair names and timestamps align with the
concurrently live round-24 peer `TameshiR24-2.RunMonitor`; I did not read them (round-24
material barred), so kake attribution is unsupported. [INFERENCE]

Absence of tokens is not proof of absence of writes, but there is no positive `/tmp`
evidence for any kake round-26 seat.

## 5. Gate gap in the lesson's proposed witness

`w1/LessonScribe.md:78` fixes the round-26 defect as "seats write only their named sandbox
or report file; nothing under `/tmp`", with the witness "a bounded path check of seat
receipts for `/tmp` references". Two mismatches:

1. All 32 `rechecks/S0NN.json` share one 7-key schema —
   `id, verdict, fetchIndex, quote, anchorObserved, reason, correction` — with **no scratch
   or tooling field**, so the stated "receipts must state where their scratch lived"
   (`LessonScribe.md:84`) cannot be evaluated against the committed receipts.
2. The witness is scoped to `/tmp`, but round 26's actual out-of-lane write was to the
   **fleet root**. A `/tmp`-reference check returns clean and misses it; the misroot receipt
   and `LOG.md:1000` are what caught it.

## Minimal correction

- Amend the `seat-scratch` row of `LessonScribe.md` (append-only) to record: round 26 had
  one fleet-root report misroot (`RowS012`, byte-exact move, fleet copy removed) and zero
  `/tmp` writes.
- Extend the witness to assert each seat report's **absolute** path equals
  `<lane>/.ufo/waves/round-26/w1/<name>.md`, and keep the fleet-level `git status` sweep
  only as a cross-check (it cannot see the lane: `.gitignore:1 *-shokunin/`).
- Do not change any freshness verdict or the 32/32 HOLD count; the misrooted file was
  byte-identical and inside the candidate.

```json
{"target":".ufo/waves/round-26/w2/ScratchAudit.md","verdict":"DISAGREE","severity":"low"}
```
