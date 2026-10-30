# ScoutSidecarDiff — round-64 sidecar re-pin verification (C3)

Verdict: **PASS for the scoped claim.** The re-pin is exactly seven
`line` cell pairs on SKILL.md entries; no other sidecar cell changed; the
23 other entries are byte-identical; every pinned SKILL.md line re-binds at
the measured revision `4c8295fa5e3b628f1fdf3840299ae415c01849fb`; the
`controls/sidecar-repin-map.txt` table matches the sidecar 7/7; and
`node scripts/freshness-sweep.mjs --offline` exits 0 at the measured tree
(I did not re-run the sweep at the later tip `cc8add1f`; its sidecar blob is identical to measured, and the committed receipt `controls/sweep-after.txt` records exit 0 at measured.) The base
`1a481315` exits 2 with the expected fault.

Leaf seat, no subagents, no git mutation. Every clone lived under
`/fast/scratch/hyaku/kake-r64/ScoutSidecarDiff/` (deleted before yield).
Lane repo working tree untouched.

## 1. Raw diff: exactly 7 line cells changed

Command:
```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- corpus/knowledge/freshness-sidecar.json
```
Output summary: one hunk set, 7 `-` lines and 7 `+` lines, all of the form
`"line": N`. Blob ids: base `53ae3eeb…`, measured `0fa3d87a…`, tip `0fa3d87a…`
(sidecar unchanged between measured and tip).

Removed/added `"line"` cells (file `corpus/knowledge/freshness-sidecar.json`):

| array idx | token | kind | old line | new line |
|---|---|---|---|---|
| 6  | `~/Projects/ds4cc-marketplace` | restored | 364 | 365 |
| 7  | `~/Projects/ds4cc-marketplace` | restored | 445 | 446 |
| 8  | `~/Projects/ds4cc-marketplace` | restored | 448 | 449 |
| 9  | `~/Projects/ds4cc-marketplace` | restored | 449 | 450 |
| 10 | `~/Projects/ds4cc-marketplace` | restored | 450 | 451 |
| 21 | `~/Projects/ds4cc-marketplace/burnerchrome` | restored | 423 | 424 |
| 22 | `~/Projects/ds4cc-marketplace/burnerchrome` | restored | 431 | 432 |

Parsed comparison (python, `json.loads` of both blobs, positional zip, 30
entries each): changed entries = 7 (indices above); `fields changed` across
all 7 = `['line']` only; violations outside `line`/`lineSha256` = none; no
`lineSha256` changed (the new lineSha256 values equal the base values; see
§3); `file` set unchanged (all 7 are `SKILL.md`); `note`, `kind`, `date`,
`token` unchanged on all 30 entries. Entry field set is uniform:
`{date, file, kind, line, lineSha256, note, token}`.

Unchanged: 23 entries, identical as parsed objects. By file: fleet-registry.md
6, speedrun-pipeline.md 4, SKILL.md 3 (idx 4,5,20: lines 16,19,20),
origin-repos.md 3, drift-detection.md 1, free-read-verbs.md 1,
round-6-aggregator-audit.md 1, publish-channels.md 1, round-18.md 1,
round-1-aggregator-audit.md 1, mirror-pitfalls.md 1. Textual confirmation:
the raw unified diff has exactly 14 changed lines (7 `-`, 7 `+`), all
`"line"` cells, so the file is otherwise byte-identical to base. Blob ids of
every non-SKILL.md target file the sidecar points into are identical at base
and measured (drift-detection, fleet-registry, free-read-verbs,
mirror-pitfalls, origin-repos, publish-channels, speedrun-pipeline,
round-1-aggregator-audit, round-18, round-6-aggregator-audit: all
`unchanged=True`).

Pin commit check: `git show 3d07733b:corpus/knowledge/freshness-sidecar.json`
equals base for all 30 entries (pin→base changed entries = 0), so the
re-pin is the only sidecar change since round-24.

## 2. Recomputed sha256 of each pinned SKILL.md line

Method: `hashlib.sha256(line.encode())` over `git show <rev>:SKILL.md`
split on `\n`, indexed `line-1`, compared to the sidecar `lineSha256`. Also
the sweep's own binding predicate (canonHome-normalized PATH_RE tokens of the
line contain `token`), reimplemented in python from
`scripts/freshness-sweep.mjs:135,376-386`.

At measured `4c8295fa`: **30/30 entries bind, 0 failures** (all 30 sha256
match, all tokens present under the sweep's tokenization).

Per SKILL.md changed entry (measured line, sha256 matches `lineSha256`):
- SKILL.md:365 `7070c25fb9ab…` ✓ (line: "- `~/Projects/ds4cc-marketplace/` — ds4cc.com source: …")
- SKILL.md:446 `f08a35d9d8cb…` ✓
- SKILL.md:449 `6e1baa1fa1e9…` ✓
- SKILL.md:450 `cfb08909875e…` ✓
- SKILL.md:451 `c16c7a6a684c…` ✓
- SKILL.md:424 `97576af9b60a…` ✓
- SKILL.md:432 `f2d75f797445…` ✓

(Full lineSha256 values: `7070c25fb9ab6fd1220c9aa504c965290a47fb710093ae55d39124ec8baf4216`
for 365, identical at base line 365 — verified directly.)

Unchanged SKILL.md entries (lines 16, 19, 20) also bind at measured (sha ✓).

At base `1a481315`: 7 of 30 entries fail binding — exactly the 7 re-pinned
entries (idx 6,7,8,9,10,21,22). Each of those 7 `lineSha256` value matches the
base line at `pinned+1` (e.g. base SKILL.md:365 sha = `7070c25f…` = entry 6's
pinned sha), confirming the cause is a +1 line shift, not content change.
Base line 364 is `  failing), not a keeper automation block.` (sha `5f3a92f4…`),
so the pre-shift pin no longer binds — matching the sweep's
`paths sidecar binding invalid: SKILL.md:364` (first failing entry in file
order).

## 3. Cross-check: `controls/sidecar-repin-map.txt`

Parsed the 7 map rows (`SKILL.md OLD -> NEW SHA KIND TOKEN`) and matched each
against the measured sidecar on (file, new line, sha, token, kind): **7/7
match**, 7 rows total. The map's sha column (12-char prefix) equals the
sidecar's full `lineSha256`. Map row kinds and tokens agree with the sidecar.
The lesson table in `corpus/lessons/round-64.md` §Mistakes lists the same 7
old→new pairs and the same first-12 sha prefixes (verified by reading the
table: 364→365 `7070c25fb9ab`, 423→424 `97576af9b60a`, 431→432 `f2d75f797445`,
445→446 `f08a35d9d8cb`, 448→449 `6e1baa1fa1e9`, 449→450 `cfb08909875e`,
450→451 `c16c7a6a684c`).

The lesson's "23 further entries re-verified byte-identical at their pinned
lines" is consistent with §1 and §2.

## 4. Sweep evaluation

Commands (each in a per-revision clone under scratch, `git rev-parse
--show-toplevel` confirmed before use):
```
cd <clone@4c8295fa> && node scripts/freshness-sweep.mjs --offline   # exit 0
cd <clone@1a481315> && node scripts/freshness-sweep.mjs --offline   # exit 2
```

Measured `4c8295fa` (exit 0), relevant lines verbatim:
```
§paths  172 files · 679 occurrences · 106 unique tokens
  resolve 31 · declaredAbsent 65 · drift 0 · unresolved 10
  set-delta miss: no new miss
VERDICT: OK (exit 0, partial: offline)
```
`drift 0` satisfies the contract kill rule (§paths drift count must be zero).

Base `1a481315` (exit 2), verbatim:
```
freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:364
```

Tip `cc8add1f`: not swept by me. Its `corpus/knowledge/freshness-sidecar.json` blob (`0fa3d87a…`) equals the measured blob, so the sidecar-side outcome is identical; the committed receipt is the only evidence for the tip sweep.

## 5. Evidence gap (non-blocking, recorded)

`controls/sweep-after.txt` (committed after-receipt, 359 bytes) shows
`VERDICT: OK (exit 0, partial: offline)` and the `§armed`/`§history` skip
lines, but **does not contain the `§paths` section line** (`drift 0`). The
contract kill rule names the §paths drift count, so the committed receipt
alone cannot show it; it is only visible on a fresh run (§4 above). Suggest
the after-receipt be replaced with, or supplemented by, the full sweep
stdout. Not a defect in the re-pin; a receipt-completeness observation.

Similarly `controls/sweep-before.txt` (10 lines) omits the `§paths` line
(expected — it failed before §paths evaluated).

## 6. Things checked and found clean

- No note/kind/date/token/file cell changed (§1).
- No `lineSha256` value changed; the re-pin is line-number-only, and the
  sha values are the content hashes of the lines now at the new positions.
- No sidecar entry added or removed (30 → 30; positional zip aligned by
  construction, and entry key set `(file,token)` equal base↔measured).
- No SKILL.md line content change that would invalidate a pin: the only
  SKILL.md diff base→measured is two appended lines at 1360-1365 (table rows
  for calibration-counter and quote-tool-counter) plus the sidecar; the
  rows are below all pinned lines (max pinned line 451), so they cannot
  shift any pin. Verified: `git diff --stat` SKILL.md = `2 ++`.

## 7. Attacks attempted

- Field-widening: checked whether any non-`line` field moved (none).
- Sha-laundering: checked whether any new `lineSha256` equals its base
  value for a different line (no; the 7 new shas equal the base sha at the
  post-shift line, i.e. the pin tracks the same content).
- Token drift: checked whether tokens still appear on re-pinned lines under
  the sweep's canonHome/PATH_RE tokenization (yes for all 7; a naive
  substring check on `~/` tokens fails for lines spelled `/home/vgpnk/…`,
  which is a false alarm of my check, not a sweep defect).
- Pin-commit shortcut: confirmed base==pin for the sidecar, so the 7-line
  change is the only sidecar delta since round-24.
- Tip vs measured: sidecar blob identical (`0fa3d87a…`); sweep run only at measured (exit 0) and base (exit 2).

## Tools

No tools installed or updated. Used: git, node v24.21.0 (already present),
python3 with stdlib json/hashlib/subprocess/re.

## Scratch

`/fast/scratch/hyaku/kake-r64/ScoutSidecarDiff/` (three git clones at
1a481315, 4c8295fa, cc8add1f; sweep outputs) — removed before yield.
