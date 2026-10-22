# ScoutQualityCriteriaCanFail — round 33, wave 1 (F1–F3 at bc6c4a8)

Seat scout, axes operability/freshness. Lane rev `bc6c4a8d435473f3c30903210be30d9d6e3ef750`
(clone). Sandbox `/fast/scratch/hyaku/kake-r33/w1/ScoutQualityCriteriaCanFail/` (TMPDIR inside).
Target: `.ufo/waves/round-31/a2-w2/CriticQualityCriteria.md` F1–F3 vs `corpus/QUALITY.md`.
No lane mutation, no network, no installs.

## Status at bc6c4a8

- `git diff 92235a0 bc6c4a8 -- corpus/QUALITY.md` → 52 insertions, 0 deletions: criteria
  at `:493-515` byte-unchanged since the critic read them.
- F1 **unchanged** (`:493-499`); the wave-2 bullet at `:523-528` answers `CriticSymlinkCases`
  (P5 name shapes), not F1. F2 **superseded** (`:529-534`), F3 **superseded** (`:535-540`).

## F1 — criterion 1 check passes with one of six shapes (`:493-499`)

- `python3 -B clone/scripts/citing_set_hostile_selftest.py --root clone --tmpdir h1 --runner runner-f80bd8f.py`
  → exit 1, six of six specs `passed:false` (`out-prerepair.json`; runner from
  `git show f80bd8f:scripts/citing_set_selftest.py`, sha256 `9f2d1ecb…`).
- Same argv without `--runner` → exit 0, six of six pass (`out-repaired.json`).
- Export with only the P1 spec (`onlyP1/`, full `scripts/`): `--root onlyP1 --runner runner-f80bd8f.py`
  → **exit 1**, one case. The stated check cannot tell one probe from six; it never runs the
  claimed runner; P6's gap is `m3`, not a routed shape.

Fix (append-only, text in `proposed-QUALITY-append.md`): declare the claimed shape list; require
spec `gap` set equals it, pre-repair exit 1 with every spec failing, claimed runner exit 0 with
every spec passing. Check:
`python3 -B scripts/containment_check.py --root <tree> --shapes N1,N2,N3,N5,N6,m3 --prerepair-runner <runner> --claimed-runner scripts/citing_set_selftest.py`.
Demonstrated: `--root clone` → 0, `problems: []`; `--root onlyP1` → 1
(`declared shapes with no spec: ['N2','N3','N5','N6','m3']`) where the criterion's own check exits 1.

## F2 — replacement sub-check (a) cannot fail (`:529-534`)

- `git ls-tree 4580c78 -- .ufo/waves/round-30/sources/` prints 9 blobs, exit 0: ls-tree
  recurses on a trailing slash. Without the slash: `040000 tree d159ba5…`.
  `git cat-file -t 4580c78:.ufo/waves/round-30/sources/` → `tree`. Line 534's claim that the
  round-30 command fails (a) is false as worded.
- (b) discriminates: on stage commit `bc3ae57` (adds `sources/S062.txt`, `screened/zz-unrelated.txt`
  beside round-31's named paths) the named-file form exits **0**, the directory form **1**.
  Round-30 command over probe commit `652fe61` → exit 1.

Fix: (a) becomes `git cat-file -t <rev>:<path>` prints `blob` after stripping one trailing `/`;
name a command. Check:
`python3 -B scripts/closure_check.py --rev <decl> --rev2 <commit> --probe <add-beside> --change <named-change> -- <paths>`.
Demonstrated: round-30 paths, `--rev 4580c78 --probe 652fe61 --change d66b746` → 1 (`is a tree, not a blob`,
`trailing slash`, `command fails on an unrelated addition`); round-31 named paths,
`--rev a16602a --probe bc3ae57 --change cfd300a` → 0.

## F3 — replacement is prose only; vacuous wave passes (`:535-540`)

- Original count rule (`:506-511`) on round-31 w1: 13 `returned` vs 14 reports, no
  `partial-reports.json` → fails the round's own wave.
- Corrected set rule passes it: 14 returned (incl. safety-filter) vs 14 non-partial reports
  (`seat_check.py --wave clone/.ufo/waves/round-31/w1` → exit 0).
- A wave with `members: []` also passes set comparison (`mut/vacuous` → exit 0 before patch).
  Round-30 w2 has `partial-reports.json` and no status file; the criterion allows a listed
  partial and no command reads it.

Fix: name the command, reject empty `members`, require `seats == len(members)`, accept `--partials <json>`.
Check: `python3 -B scripts/seat_status_check.py --wave <wave dir> [--partials <list>]`.
Demonstrated after patch: round-31 w1 → 0; `mut/vacuous` → 1 (`status file names no seats`);
returned-report swap onto a dead seat → 1; `PARTIAL:` first line on a returned report → 1;
listed-partial on a returned report → 1; stranger report → 1.

## Adjacent risk for C1 (not my item)

`SPEC_KEYS` (`scripts/citing_set_hostile_selftest.py:85`) rejects unknown spec keys: adding
`"reason_code"` to `P6-commit-before-init/hostile.json` makes the selftest exit **2**
(`spec must be an object with keys ['cases','description','gap','tmpdir_in_victim']`;
`keyprobe/`, `out-key.json`). C1's spec key needs a matching `SPEC_KEYS` change or a per-case key.

## Not verified

- No round-33 closure command exists to test (C1/C2 name counters); F1/F2 were exercised on the
  round-30/31 command shapes only, with `--rev2` set to the declaration commit.
- F4/F5 and entry sentences not judged; no fetches, no browser. No tools installed.

Artifacts: `/fast/scratch/hyaku/kake-r33/w1/ScoutQualityCriteriaCanFail/{containment_check.py,closure_check.py,seat_check.py,proposed-QUALITY-append.md,out-f1-full.txt,out-f1-onlyP1.txt,out-prerepair.json,out-repaired.json,out-key.json}`.
