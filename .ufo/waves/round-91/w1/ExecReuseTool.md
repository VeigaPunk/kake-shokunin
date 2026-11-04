# Seat report — ExecReuseTool (round 91, wave 1, C2 capability)

VERDICT: C2 candidate met — the frozen counter prints `met=true`
(`hand=45/45 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok seed=91091`), exit 0, first run.

## What landed

- `scripts/stored_reuse.py` in LANE (working tree; L1 lands the commit):
  sha256 `5004657dbf2ae43399631f79e5d5955a8aa698b53f6127e22e2cc654ba9ad299`,
  stdlib only (`json`, `re`, `sys`), mode 755.
- Developed in the scratch clone `/fast/scratch/hyaku/kake-r91/ExecReuseTool/clone`
  (shared clone of LANE, detached at lane master `f4fff130a52ae6de49af5de7d568d2ee320ebfb0`),
  committed there as `945aaca5c96ff25ad900966638a747737c248079` with a fixture identity
  (`-c user.name=… -c user.email=…@r91.fixture.invalid`, never global), after asserting
  `git rev-parse --show-toplevel` == the clone dir. The commit adds exactly
  `scripts/stored_reuse.py`; the tree was clean afterwards.
- The LANE working-tree copy is byte-identical to the measured blob: its sha256 equals
  the counter's `candidate_sha256` (see `counter-final.txt`).

The module docstring names what it decides (the seven-member vocabulary) and what it
refuses to decide (no Date parsing, no clock, no network, no revalidation exchange, no
store, no heuristic freshness, no key identity / Vary matching / stale-serving
permission); clause numbers 1–21 are cited in comments at each branch.

## Measured command and outputs (the frozen instrument, unmodified)

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-91/c91_reuse.py \
  --root /fast/scratch/hyaku/kake-r91/ExecReuseTool/clone --revision HEAD \
  --work /fast/scratch/hyaku/kake-r91/ExecReuseTool/work --seed 91091
```

- line 1: `C2v91 revision=945aaca5c96ff25ad900966638a747737c248079 candidate=present hand=45/45 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok seed=91091 met=true`
- line 2: `{"anti_table_hits": [], "candidate_sha256": "5004657d…", "errors": [], "forgeries": {"…neg-allowlist.py": {"admitted": false, "hand": 14}, "…neg-blanket-admit.py": {"admitted": false, "hand": 0}, "…neg-blanket-refuse.py": {"admitted": false, "hand": 9}, "…neg-hash-table.py": {"admitted": false, "hand": 0}, "…neg-pin-reader.py": {"admitted": false, "hand": 0}}, "hand_failures": [], "pins_digest": "033b6103…", "population_drift": []}`
- exit 0. Full verbatim copy: `counter-final.txt` (same directory as this report).

## --selftest output (required by the item)

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/stored_reuse.py --selftest
selftest 45/45
exit=0
```

Fixtures are the contract's 45 worked cases in memory (one entry per contract table
row, in table order); nothing is written. Receipt: `selftest.txt`, which also records
two smoke runs on the landed file (one `reuse` success, one `invalid_input` refusal
with empty stdout and exit 1).

## Evidence beyond the counter

- Differential harness vs the frozen counter's own `reference()`: 45 hand + 120
  generated (seed 91091) + 20 000 fuzzed (valid and malformed) + Age/max-age boundary
  sweeps = 20 605 comparisons, **0 mismatches**, exit 0, run against the landed LANE
  file. Harness retained: `diff-harness.py`; output: `diff-harness.txt`. (An earlier
  scratch variant with a redundant boundary loop reported 21 045/0; the retained
  harness is the cleaned one.)
- The counter itself re-verified reference/case agreement and population pins before
  scoring (its `pins_digest` equals the frozen `PINS_SHA`).

## Contract readings the wording leaves to care (implemented as forced; no ambiguity unresolved)

1. Clause 20 converts `heuristic-undecided` (clause 11) to `only-if-cached-miss` when
   the request carries `only-if-cached`: its text excludes only `reuse` and
   `not-storable` from conversion. No hand case pins this; the seeded generated
   population does (only-if-cached × no-lifetime inputs). The counter's reference
   decides the same.
2. Clause 4 details: an empty delta argument refuses (`max-age=`, `max-stale=`) while
   bare `max-stale` is the unbounded sentinel; quotedness is tested before the
   delta-integer check, so `max-age="60"` refuses (worked case 36) while `foo="bar"`
   and `foo=bar` are the *same* argument and not a duplicate-with-different-argument
   refusal; unknown directives keep their parsed values, so `foo="a,b"` fails at the
   comma split.
3. Clause 10's method test is exact and case-sensitive: `"get"` is not `GET` →
   `not-storable`.
4. Clauses 5–7: `Date` and `Expires` accept negative integers; `Expires` may precede
   `Date`, giving a negative lifetime (worked case 12); only `Age` must be ≥ 0.
5. Validation order: a case-variant duplicate header name refuses before value
   validation (reason-text choice only; the counter checks only the
   `invalid_input:` prefix and exit code).

## Findings on the round's own instruments (reported, not edited)

- `c91_reuse.py` cosmetic: the two `for i, … in enumerate(...)` loops inside
  `score_subject` bind `i` and never use it (they use their own `idx`/`enumerate`
  counters). No predicate impact.
- The `anti_table` stem check is substring-based (`stem in src`), so a legitimate
  candidate that merely quoted a frozen forgery's file name in prose would be
  refused. Designed false-positive risk, not a defect; the shipped tool contains
  none of the five stems and no hand-case input digests.
- The contract names no input encoding. The tool decodes stdin via `json.loads`
  (strict UTF-8) and refuses anything else as `invalid_input: input is not valid
  JSON: …`, matching the round-90 routed disposition (R90-1) taken by the r90 gate.
- Refusal contract honoured exactly: `invalid_input: <reason>` on stderr, empty
  stdout, exit exactly 1 (all 10 refusal hand cases and the fuzz population pass).

## Limits and hygiene

- The counter measured the clone commit; the LANE copy is proven identical by sha256,
  not by a counter run against a LANE revision, because the file is not yet a LANE
  commit — landing it at the carrier is L1's step, and L1's rerun at that revision
  should reproduce this receipt byte-for-byte.
- No subagents (no labrat needed), no tool installs (python3 stdlib sufficed; pacman
  untouched per the host-wide pause), no network, no LANE git state changed, no
  sibling files touched, frozen bytes untouched (candidate digest re-checked against
  the counter's pins by the counter itself).
- Scratch `/fast/scratch/hyaku/kake-r91/ExecReuseTool` deleted after copying the
  receipts above; nothing citable lives under /tmp or /fast/scratch.

## Files in this directory

- `ExecReuseTool.md` — this report
- `counter-final.txt` — frozen-counter receipt (command, both lines, exit)
- `selftest.txt` — `--selftest` and smoke receipts
- `diff-harness.py`, `diff-harness.txt` — retained differential harness and its output
