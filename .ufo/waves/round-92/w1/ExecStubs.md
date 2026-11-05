# ExecStubs — round-92 seat report

VERDICT: C2 held-out differential — the frozen counter holds on 9/14 subjects (both contract-faithful conforming implementations read `met=true`; 7 clause-violating subjects refused) but **admits 5 clause-violating subjects with `met=true`** (clauses 2, 3, 4, 6, 8 uncovered), and the counter's own reference violates contract clause 4 (quoted delta-seconds accepted — oracle/contract drift). Findings F1–F6 below are defects of the frozen instrument, reported not patched.

Seat: ExecStubs (leaf executor, no labrat needed). Freeze measured: `a5640ca02c20f94a0fa03af41b977b46ae99808e`.

## Deliverables

- `subjects/` — 14 held-out subjects written from `.ufo/waves/round-92/c2-contract.md` alone: `conforming-table-driven.py` (validation table + first-match rule table), `conforming-branch-per-clause.py` (flat numbered branches), and 12 negatives each breaking exactly one clause (`neg-clause01-duplicate-case-kept`, `neg-clause02-cr-in-value-accepted`, `neg-clause03-types-coerced`, `neg-clause04-quoted-delta`, `neg-clause05-date-parsed-as-float`, `neg-clause06-expires-parsed-as-float`, `neg-clause08-validate-after-decision`, `neg-clause09-nostore-ignored`, `neg-clause10-smaxage-when-not-shared`, `neg-clause11-public-not-honored`, `neg-clause12-cap-absent`, `neg-clause13-lm-after-date`).
- `scores.txt` — first line of every counter run.
- `runs/` — 15 full receipts (stdout+stderr+exit per run, including the baseline).
- `Notes.md` — method, results table, findings.

## Method (exact commands)

Scratch root `/fast/scratch/hyaku/kake-r92/ExecStubs/` (created explicitly; one clone; deleted at the end after receipts were copied). Clone and freeze checkout:

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kake-shokunin $S/clone
git -C $S/clone checkout -q --detach a5640ca02c20f94a0fa03af41b977b46ae99808e
git -C $S/clone update-ref refs/heads/master $(git -C .../kake-shokunin rev-parse refs/heads/master)
# toplevel asserted == $S/clone before every commit; fixture identity set clone-locally:
git -C $S/clone config user.name "ExecStubs fixture"; git -C $S/clone config user.email execstubs@fixture.invalid
```

Per subject (14 runs, one at a time):

```
cp subjects/<name>.py $S/clone/scripts/heuristic_freshness.py
git -C $S/clone add scripts/heuristic_freshness.py && git -C $S/clone commit -q -m "ExecStubs held-out subject: <name>"
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-92/c92_heuristic.py \
  --root $S/clone --revision $(git -C $S/clone rev-parse HEAD) --work $S/w \
  --candidate scripts/heuristic_freshness.py   # receipt: runs/<name>.txt, exit on last line
```

Baseline control re-run in the same clone (candidate absent):
`runs/00-baseline-candidate-absent.txt` → `C2v92 revision=a5640ca02c20f94a0fa03af41b977b46ae99808e candidate=absent hand=0/28 generated=0/120 forgeries_refused=0/5 anti_table=n/a population=n/a seed=92 met=false`, exit 1 — matches `controls/base-c2.txt`.

## Results

Expected readings held: both conforming subjects `hand=28/28 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok met=true`, exit 0 (receipts `runs/conforming-branch-per-clause.txt` rev `5b4b25bb…`, `runs/conforming-table-driven.txt` rev `e5a7f8cd…`). Seven negatives refused as required (`met=false`, exit 1), each failing on exactly the frozen case its named clause predicts (e.g. neg-clause01 → `refuse/duplicate-header-name`, neg-clause09 → `store/no-store`, neg-clause13 → `gate/last-modified-after-date` with `lifetime −1`; full detail line 2 of each receipt).

**Five negatives a conforming counter must refuse read `met=true` (exit 0):**

| # | Subject / clause broken | Counter reading | Receipt |
|---|---|---|---|
| F1 | neg-clause02-cr-in-value-accepted (clause 2: CR/LF/NUL refusal) | `hand=28/28 generated=120/120 … met=true` | `runs/neg-clause02-cr-in-value-accepted.txt`, rev `db88997d…` |
| F2 | neg-clause03-types-coerced (clause 3: type refusals — the variant R91-2/K91-6 named) | `hand=28/28 … met=true` | `runs/neg-clause03-types-coerced.txt`, rev `ba0c78f1…` |
| F3 | neg-clause04-quoted-delta (clause 4: quoted delta-seconds refusal) | `hand=28/28 … met=true` | `runs/neg-clause04-quoted-delta.txt`, rev `dd5199c6…` |
| F4 | neg-clause06-expires-parsed-as-float (clause 6: Expires non-integer refusal) | `hand=28/28 … met=true` | `runs/neg-clause06-expires-parsed-as-float.txt`, rev `016fcd1f…` |
| F5 | neg-clause08-validate-after-decision (clause 8: validation before decision) | `hand=28/28 … met=true` | `runs/neg-clause08-validate-after-decision.txt`, rev `bed1c4f7…` |

**F3 carries a second, sharper defect — oracle/contract drift inside the frozen counter itself.** Contract clause 4: a delta-seconds argument in "a quoted or signed form is a refusal". The counter's reference strips quotes in `parse_cc` *before* the bare-decimal check, so on
`{"stored": {"status": 200, "headers": {"Date": "1000000", "Cache-Control": "max-age=\"600\""}}, "now": 1000000}`
it returns `{"decision": "explicit", "lifetime": 600, "heuristic": false}` (measured by importing the frozen counter and calling `reference()`; both contract-faithful conforming subjects refuse the same input, exit 1, `invalid_input: delta-seconds argument is quoted`). The counter's reference self-check runs only against its own hand cases, none of which feeds a quoted delta, so the drift cannot self-report: on this clause an oracle-follower is indistinguishable from a contract-follower.

**F6 — the generated population cannot witness any refusal-clause violation.** `generate()` in the frozen counter emits only well-formed fields (integer dates, no duplicate names or directives, no quoted/signed delta, no control characters; `Last-Modified > Date` with p = 5/2 000 005 per case). All refusal coverage sits in the 5 hand cases; measured consequences: neg-clause11 and neg-clause13 are caught hand-only (generated 120/120), and the clause-4 duplicate-directive variant (same name twice, different arguments) plus clause 7 (Last-Modified non-integer, same `delta()` path as clause 6) are uncovered by the case set — argued from the counter source, not separately counter-measured (12-slot budget).

Subject digests (sha256, for cross-checking the committed copies): conforming-branch-per-clause `5525cfe5…c70f0`, conforming-table-driven `7e77dc9f…daed7`, neg-clause01 `67653063…5959d`, neg-clause02 `2f9d6574…fa2e6`, neg-clause03 `324d5961…e12f0`, neg-clause04 `ce63c4e4…059a32`, neg-clause05 `34ac6ff8…bdd95`, neg-clause06 `0010a574…cc0de`, neg-clause08 `4489410d…f87ee5`, neg-clause09 `84bfd811…feafd`, neg-clause10 `0b4516f7…3e3710`, neg-clause11 `d5e0823b…f1887`, neg-clause12 `f952297d…95920`, neg-clause13 `975c0dac…2efe650`.

## What the counter does distinguish (for the routed list)

Clauses 1, 5, 9, 10, 11, 12, 13 are covered: neg-clause01 `hand 27/28`, neg-clause05 `hand 27/28`, neg-clause09 `hand 27/28`, neg-clause10 `hand 27/28 gen 108/120`, neg-clause11 `hand 27/28`, neg-clause12 `hand 27/28 gen 107/120`, neg-clause13 `hand 27/28` — each `hand_failures` entry names the predicted case, so the single-violation property of every negative is confirmed by the instrument itself, not just by construction.

## Limits and disclosures

- Single-author population: this seat wrote both conforming subjects and all 12 negatives from the same contract reading; no second independent author. The counter's reference/hand cases were not used to author subjects — only for the post-scoring F3 demonstration and failure-name attribution.
- Clause 7 and the clause-4 duplicate-directive gap are source-reading arguments, not measured runs.
- No frozen file was edited; nothing under `scripts/` was written in the lane; the only lane writes are this seat's own `w1/ExecStubs/` tree. No commits in LANE; clone commits only (fixture identity, toplevel asserted).
- No tools installed or upgraded (none needed); no network access; pacman untouched; no /tmp writes; scratch `/fast/scratch/hyaku/kake-r92/ExecStubs/` deleted after receipts were copied.

## Routed (counter/contract defects for the round's routed list)

1. Add hand cases for clauses 2, 3, 6, 7 (control characters; scalar/value types; Expires/Last-Modified non-integer) and a malformed-field-on-unstorable case for clause 8 — the 28-case set covers none of them.
2. Add a quoted-delta case AND repair the reference's `parse_cc` ordering (quote stripping before the bare-decimal check) in the next round's instrument revision; the current reference encodes the clause-4 violation the contract forbids.
3. Widen `generate()` to emit refusable shapes (or accept that generated conjuncts can never guard refusal clauses and say so in the counter header).
