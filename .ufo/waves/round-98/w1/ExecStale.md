# ExecStale — seat report, kake round 98 (C2 candidate builder)

Scope held: wrote only `.ufo/waves/round-98/w1/ExecStale/` (deliverables below)
and this report. No other lane file, no fleet-repo file, no `.ufo/state`, no
MANIFEST. Read-only git only (`rev-parse`, digests). No counter, contract or
frozen byte touched — the candidate was fixed, never the counter.

## Delivered (all in `.ufo/waves/round-98/w1/ExecStale/`)

| file | content |
|---|---|
| `stale_extensions.py` | independent stdlib-only Python 3 candidate, sha256 `895be37af511cfd98fa0bc04e0992df1c7923e0e73d06ab38c6622d46015bc54`; docstring names the contract, RFC 5861 §3/§3.1/§4/§4.1, RFC 9111 §4.2.4 + directive sections + §1.2.2, RFC 9110 §5.6.2/§5.6.4, every lane convention, and what it does not decide; `--selftest` with 113 own cases |
| `selftest.txt` | `selftest cases=113 passed=113 failed=0` (rc 0) |
| `score-seed1.txt` … `score-seed3.txt` | counter output incl. `exit=0` for seeds 1, 2, 3 |
| `score-noseed.txt` | counter output incl. `exit=0`, derived seed 1000093071 |
| `notes.md` | interpretation decisions ([INFERENCE] flags), defect log, evidence table, risks |

## Behavior

Reads ONE JSON object on stdin; decided → exit 0 with exactly
`{"decision": …, "staleness": …}` + newline; refused → exit 1, stdout empty,
stderr starting `invalid_input:`. Implements contract v1 fully: quoted-string
comma splitting, tchar/quoted-string grammar with >U+00FF and control
refusals, first-occurrence values, quoted/non-digit swr/sie absent,
qualified no-cache conservative prohibition, must-revalidate, shared-gated
proxy-revalidate/s-maxage, request no-cache, request-directive refusal in
requests, request stale-if-error precedence, inclusive boundaries, 2^31
clamp, eligible errors 500/502/503/504/network.

## Evidence

- `python3 -B .ufo/waves/round-98/c98_stale.py --candidate-file
  w1/ExecStale/stale_extensions.py --work <scratch> --seed 1|2|3` and once
  without `--seed`: all four runs `candidate=present
  sha256=895be37a… hand=60/60 generated=240/240 met=true`, exit 0 (refusals
  36/36, 42/42, 33/33 and 34/34 respectively per file). First scored pass; the
  candidate was never edited after the first scored run.
- Frozen instruments verified before attacking:
  `controls/instrument-sha256.txt` re-hashed — `c98_stale.py` `e0331e56…`,
  `stale-contract.md` `ec077b4f…`, `freeze.md` `9076420b…`, `c98_captable.py`
  `efd59857…` — all match.
- `sources/rfc5861.txt` re-hashed `1193f1c8…` — matches the freeze pin.
- Lane tip at round open read: `git rev-parse master` → `7838981e4e40280176085e8aa1f6827eb7133a69`.

## Findings routed (defects, not repairs)

None in the instruments. Two pre-scoring defects were found **in my own
candidate** by my selftest (quote-state opening in the element splitter; two
wrong expectations) and are logged in `notes.md` with the fix history.

## Risks

- Predicate identity conjunct: the claim's scored run must land these exact
  candidate bytes (`895be37a…`) at `scripts/stale_extensions.py` and be
  scored from `--revision` by the L1; my runs prove the content, not the
  landing.
- Interpretation decisions 1–2 in `notes.md` are contract readings that agree
  with the counter on 4×(60 hand + 240 generated) cases; both flagged
  [INFERENCE].
- Tooling: nothing installed or upgraded (stdlib python3 only). Scratch seat
  directory `/fast/scratch/hyaku/kake-r98/ExecStale` removed at yield after
  receipts were copied here; no ancestor or sibling touched (R97-4).

Report: .ufo/waves/round-98/w1/ExecStale.md
