# Round 93 C1 counter attack — ReviewC1 (w1)

VERDICT: C1 counter falsified — `met=true` is reachable without doing the predicate's
work by six fixture routes (F1–F6 below); two of them have live instances at the base
(`10ecbd1a`): SKILL.md rows naming directories pass E5 today, and 9 Round-numbered
QUALITY.md sections sit outside the counted E2 population. The counter holds on file
deletions (pins catch them), on canonical planted defects of all five classes, and on
unevaluable input (fail-closed exits).

Everything below was measured in throwaway git fixtures under
`/fast/scratch/hyaku/kake-r93/ReviewC1/` (deleted after receipts were copied); the lane
working tree was never written and no lane commit was made. The counter under test is
the frozen blob `bb8012fee38c0e497cdaf36337072737bca0b3cd:.ufo/waves/round-93/c93_selfassess.py`,
sha256 `4e25b72e88299300c55525cc21bcc30e1c5b05f1f74ebbcd2ad4e6d50bb7390f`
(byte-identical to the working tree at review time). Fixture driver: `receipts/drive.py`;
live cross-checks: `receipts/live.py`. All fixtures were created per the round's git-fixture
rule (`git -C "$D"` on every call, `rev-parse --show-toplevel` asserted to equal the fixture
dir before the first commit, throwaway identity used only inside fixtures).

## Controls (the counter is not trivially broken)

| Control | Receipt | Result |
|---|---|---|
| Base reading re-run in the lane | `receipts/base-rerun.txt` | `mismatches=20 E1=1 E2=8 E3=1 E4=4 E5=6 pins=ok met=false`, exit 1 — matches `freeze.md` and `controls/base-c1.txt` exactly |
| Full-size clean fixture (87 lessons, 80 entries, 257 rows, 39 criteria) | `receipts/00-sanity-clean.txt` | `mismatches=0 … pins=ok met=true`, exit 0 |
| One planted defect per class (E1–E5) | `receipts/01-planted-five.txt` | exactly `E1=1 E2=1 E3=1 E4=1 E5=1`, met=false, exit 1 |
| Fail-closed inputs | `receipts/19-fail-closed.txt` | unknown revision → exit 2; SKILL.md absent at rev → exit 2; empty repo → exit 2 (`unevaluable=missing-surface`) |

Fixture population note: the CLI path pins against the hardcoded `BASE_PINS`
(87/80/255/39, floor-only), so every fixture was built at or above those floors. Pins
are `pins[k] < base` checks — they prevent shrink, never substitution or growth.

## Direction A — `met=true` without doing the work

| # | Attack | Receipt | Counter line 1 | Exit | Verdict |
|---|---|---|---|---|---|
| A1a | Canned wrapper at the documented path | `receipts/17-A1a-canned-wrapper.txt` | `…mismatches=0 … pins=ok met=true` (revision `bd02dcd5…` is real; nothing was audited) | 0 | **counter fooled** (protocol hole; defense is procedural only) |
| A1b | `subprocess.py` shadow beside the untouched frozen bytes | `receipts/18-A1b-shadow-module.txt` | `revision=80522f68… lessons=87 entries=80 rows=257 criteria=39 mismatches=0 … met=true` while `git show 80522f68:corpus/lessons/round-05.md` on the same revision shows no `## Gate` and `SKILL.md` still names `scripts/gone.py` | 0 | **counter fooled** — frozen bytes spoofed through `sys.path[0]` |
| A2a | Defective lesson deleted (E1) | `receipts/02-A2a-delete-lesson.txt` | `lessons=86 … pins=short met=false` | 1 | counter holds |
| A2b | Defective `## Mistakes` section deleted, lesson + `## Gate` kept | `receipts/03-A2b-delete-mistakes-section.txt` | `mismatches=0 … pins=ok met=true` | 0 | **counter fooled** — no pin counts Mistakes tables or sections |
| A2d | Defective counted criteria section deleted | `receipts/04-A2d-delete-criteria-section.txt` | `criteria=38 … pins=short met=false` | 1 | counter holds |
| A2e | Defective knowledge entry deleted | `receipts/05-A2e-delete-entry.txt` | `entries=79 … pins=short met=false` | 1 | counter holds |
| A3a | `## Gate` heading with no content under it | `receipts/06-A3a-bare-gate.txt` | `met=true` | 0 | holds per predicate letter; the predicate itself admits content-free Gates (routed to the predicate owner, not the counter) |
| A4 | QUALITY section cites a nonexistent lesson | `receipts/07-A4-missing-vs-empty-pointer.txt` | part 1 `E2=1 met=false`; part 2 (pointer moved to an existing lesson whose only content is a bare `## Gate`) `met=true` | 1 / 0 | counter catches missing pointers; admits empty ones (letter-faithful) |
| A5 | SKILL rows naming a committed **directory** (`scripts/pkg`) and a 0-byte blob (`scripts/empty.py`) | `receipts/08-A5-dir-and-empty-path.txt` | `mismatches=0 met=true` | 0 | **admits both** — `git show <rev>:<dir>` exits 0 and prints the tree listing, so `read()` is non-None; a directory row satisfies E5 |

A1a/A1b are the serious ones. The documented counting command
(`python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision <REV>`) puts the
script's own directory first on `sys.path`; any file the lane can place there
(`subprocess.py`) is imported instead of the stdlib. `-B` does not prevent this;
`-P`/`-I`/`PYTHONSAFEPATH` (Python 3.14.8 here supports all) or running a hash-verified
blob copy from a directory containing only that file would. Neither the counter nor the
freeze pins the counter's own digest (round-92's C2 got a `PINS_SHA`; this C1 counter has
no self-pin), so nothing mechanical binds a receipt to the frozen bytes either.

## Direction B — planted defects the counter misses

| # | Planted defect | Receipt | Result | Verdict |
|---|---|---|---|---|
| B-E1 | `## Gate ` with one trailing space | `receipts/09-B-E1-trailing-space.txt` | admitted (`^## Gate\s*$` allows trailing whitespace) | miss vs the predicate letter "a line **exactly** `## Gate`" |
| B-E2 | Defective counted criteria section escapes the population: heading loses "criteri", the word moves past char 400; a junk section citing an existing lesson refills `criteria=39` | `receipts/10-B-E2-identity-swap.txt` | `mismatches=0 … criteria=39 pins=ok met=true`; the unrepaired `corpus/lessons/round-missing.md` pointer is still in QUALITY.md at the measured revision (grep in receipt) | **counter fooled** — pins are cardinality-only, so any one-out-one-in swap passes |
| B-E3a | `source:` line with no S-id at all | `receipts/11-B-E3a-no-id-source.txt` | admitted | holds per letter ("every S<digits> id … resolves" is vacuous with zero ids); predicate-level vacuity |
| B-E3b | Entry cites `S999`; SOURCES.md contains `S999` only in a prose footer sentence, no row | `receipts/12-B-E3b-token-not-row.txt` | admitted | **counter weaker than the predicate** — predicate says "resolves to a row id"; the counter scans the whole file text (`ids = set(ID_RE.findall(sources))`) |
| B-E3c | Entry cites `S47` (two digits, no such row) | `receipts/13-B-E3c-short-id.txt` | admitted — `ID_RE = S\d{3,}` never sees it | miss vs the letter "`S<digits>`" |
| B-E4 | Blank-line-split table inside a **second** `## Mistakes` section | `receipts/14-B-E4-second-section.txt` | `E4=0 met=true` — only the first `## Mistakes` match is checked | **counter fooled** |
| B-E4b | Two blank-line gaps in one table | `receipts/15-B-E4-undercount.txt` | `E4=1` (break after the first gap) | undercount; exit still 1, so detection survives |
| B-E5 | SKILL row names `scripts/gone9.py` without backticks | `receipts/16-B-E5-unbackticked.txt` | admitted — `PATH_RE` reads only backticked tokens | miss vs the letter "named inside a SKILL.md table row" |

## Live cross-checks at the base (`receipts/live-crosscheck.txt`)

- **E5, live instance of A5:** 12 backticked row paths resolve to trees, not blobs —
  `scripts/fixtures`, `scripts/fixtures/base-path/`, `.ufo/waves/round-51/`,
  `.ufo/waves/round-56/sources/`, `.ufo/waves/round-61/capture/`, `.ufo/waves/round-72/`,
  `.ufo/waves/round-80/cases`, `.ufo/waves/round-85/controls/`,
  `.ufo/waves/round-85/w1/ExecRegistry/`, `.ufo/waves/round-29/real-input/out/` and
  siblings. All pass silently today (the 6 counted E5 mismatches are genuinely missing
  paths). Letter-faithful, intent-miss: a registry row that names a directory is not a
  usable entry point, and the counter cannot say so.
- **E2, live population blind spot:** QUALITY.md at the base has **48** headings matching
  `^Round[- ]\d+`; the counter counts **39** and silently skips **9**
  (`Round-63 addendum…`, `Round-69 addendum…`, `Round-70 addendum…`, `Round 84 —
  field-specific equivalence`, `Round 85 — …`, `Round 86 — …`, `Round 87 — …`,
  `Round 90 — a counter earns a met only after it has been shown able to say no`).
  None of the 9 cites a missing lesson today, so no live E2 defect hides there now —
  but the B-E2 swap has a ready-made uncounted home.
- E1: 5 lessons carry non-exact Gate headings (`## Gate — round-20 resume`, etc.); all
  also carry the exact `## Gate` line, so no live miss. E3: all 207 S-tokens in
  SOURCES.md are row-leading ids (0 prose-only), and no entry cites a 1–2-digit id —
  no live instance of B-E3b/B-E3c. E4: no lesson has two `## Mistakes` headings and no
  lesson has two gaps — no live instance of B-E4/B-E4b. E5 unbackticked: 140 distinct
  path-shaped mentions outside backticks, 2 missing — `scripts/kimi-surface.mjs` (already
  counted via its backticked twin) and `.ufo/waves/round-` (a false positive of my own
  scan regex against template text, not a lane defect). No additional live E5 miss.

## Findings for the routed list

- **F1 (high, environment):** the frozen counting command is shadow-module vulnerable;
  frozen bytes do not freeze `sys.path`. Successor: copy the digest-verified blob into a
  directory holding nothing else and run that, or add `-P`/`-I`; print the counter blob's
  sha256 in line 1 of the receipt so a receipt names the bytes that produced it.
  Evidence: `receipts/18-A1b-shadow-module.txt`.
- **F2 (high, protocol):** line 1 of the receipt is fully forgeable (A1a). Any consumer
  that treats line 1/exit as the verdict without the line-2 enumeration and a
  byte-identity check against the freeze blob can be handed a canned pass. The counter
  has no self-digest (contrast: round-92's C2 `PINS_SHA`).
- **F3 (high, pins are cardinal-only):** `pins=ok` prevents shrink, not substitution.
  One-out-one-in swaps (B-E2; the same move works for SKILL rows) keep every pin green
  while the defective surface survives. Identity pins (per-file digests or a section
  census) would close it. Evidence: `receipts/10-B-E2-identity-swap.txt`.
- **F4 (high, deletion holes):** the Mistakes surface is not pinned. The 4 live E4
  defects at the base can each be silenced by deleting the `## Mistakes` section
  (keeping the lesson and its `## Gate`) and the counter reads `met=true`.
  Evidence: `receipts/03-A2b-delete-mistakes-section.txt`.
- **F5 (medium):** E3 resolves ids against any `S\d{3,}` token anywhere in SOURCES.md,
  not against row ids (B-E3b); ids of 1–2 digits are invisible outright (B-E3c).
- **F6 (medium):** E5 admits trees and empty blobs; 12 live rows name directories.
  Evidence: `receipts/08-A5-dir-and-empty-path.txt`, `receipts/live-crosscheck.txt`.
- **F7 (medium):** E4 checks only the first `## Mistakes` section (B-E4) and reports at
  most one gap per lesson (B-E4b undercount).
- **F8 (low):** E1 admits trailing whitespace after `## Gate` (letter says "exactly");
  E5 ignores unbackticked path mentions. No live misses today.
- **F9 (predicate-level, not counter defects):** bare `## Gate` headings (A3a),
  pointers to existing-but-empty lessons (A4 part 2), and irrelevant-but-existing
  pointers satisfy the frozen predicate's letter. If the round wants "grounds
  something", the predicate sentence must say so before the wave — not after.
- **Fail-closed confirmed:** unevaluable input exits 2, never 0
  (`receipts/19-fail-closed.txt`).

## Honest limits

- Fixtures are synthetic (generated by `receipts/drive.py`); the base reading was
  re-run live (`receipts/base-rerun.txt`) but the carrier does not exist yet, so no
  carrier-side measurement was possible.
- I tested the CLI audit path only; `--selftest` internals were not re-derived beyond
  reading them, and `expand_braces` edge recursion was not fuzzed.
- My first A1a attempt used a `#!/bin/sh` wrapper, which `python3 -B` refuses to parse
  (SyntaxError, exit 1) — that attempt is superseded by the Python wrapper in
  `receipts/drive.py::sc_17`; the final receipt is the Python one. Driver defect, not a
  counter property.
- No live instances exist today for B-E3b, B-E3c, B-E4, B-E4b, F8 — those are latent
  holes demonstrated in fixtures only.
- Tooling: nothing was installed or upgraded (python 3.14.8, git, coreutils
  sufficed); no network GETs were made. Scratch
  `/fast/scratch/hyaku/kake-r93/ReviewC1/` is deleted after this report; the receipts
  and the two driver scripts beside them are the only evidence retained, and
  `drive.py` regenerates every fixture from scratch.
