# ExecStale notes — kake round 98, C2 candidate (2026-11-05)

Built `stale_extensions.py` (candidate sha256
`895be37af511cfd98fa0bc04e0992df1c7923e0e73d06ab38c6622d46015bc54`) from
`stale-contract.md` (frozen digest `ec077b4f…`, verified against
`controls/instrument-sha256.txt` before starting) and the retained RFC 5861
body (`sources/rfc5861.txt`, sha256 `1193f1c8…` — re-hashed, match). RFC 9111
ground read from `.ufo/waves/round-96/w1/ScoutRFC/rfc9111.txt`. The counter
`c98_stale.py` was read ONLY at docstring lines 1–35 (allowed): CLI shape and
scoring semantics, no oracle code. `frozen/*.py` was never read. The
implementation is therefore independent; the scored sha256 differs from the
positive oracle's (`bfb48d81…`), as expected.

## Interpretation decisions (contract sentence → implementation)

1. **Values vs presence.** "The FIRST occurrence of a name is used" is applied
   to directive *values* (stale-while-revalidate / stale-if-error); a first
   occurrence with a quoted/non-digit value makes the directive absent with no
   fallback to later occurrences. Prohibition/other *presence* checks
   ("carries no-cache", "carries must-revalidate") look at the whole field.
   [INFERENCE: contract distinguishes "used" for values from "carries" for
   presence; the counter agrees on every generated and hand case run.]
2. **Request directives refuse in the request field only.** "Request
   directives max-age, max-stale, min-fresh, only-if-cached → refuse" is
   enforced when they appear in `request_cc` (case-insensitively, any
   occurrence, qualified or not). In `response_cc` they are ignored:
   RFC 5861 §3.1's example response carries `max-age=600`, and the contract
   itself cites §3.1, so a response refusal would contradict the contract's
   own ground. `max-stale`/`min-fresh`/`only-if-cached` in a response fall
   under "unknown extensions are ignored".
3. **`=` is not a tchar** (RFC 9110 §5.6.2), so a second `=` in a bare token
   value (`a=b=c`) refuses; only the FIRST `=` splits name from value.
4. **Empty value vs empty quoted-string.** `max-age=` (nothing after `=`)
   refuses; `x=""` is a legal quoted-string with empty content.
5. **Quoted-pair escapes** `\` + HTAB/SP/VCHAR/obs-text validated; qdtext set
   enforced exactly (HTAB, SP, %x21, %x23-5B, %x5D-7E, %x80-FF); anything
   above U+00FF or any control character refuses anywhere it cannot occur.
6. **`error` shape.** Required and int-not-bool 100–599 or the exact string
   `"network"` when `event` is `"error"`; absent or `null` otherwise.
   `shared`/`response_cc`/`request_cc` type-checked; unknown keys, invalid
   JSON, trailing data after the object, and non-UTF-8 stdin refuse.
7. **Eligible errors are exactly 500/502/503/504/"network"** (RFC 5861 §4);
   rule order not-an-error → fresh → serve-stale/revalidate-or-error-through
   as frozen; boundaries inclusive (`staleness ≤ limit`); delta-seconds
   clamped at 2147483648 (RFC 9111 §1.2.2).

## Defects found and fixed in my own candidate (before scoring)

- `_split_elements` never opened quote state on a leading DQUOTE, so a comma
  inside a quoted-string value split (`no-cache="a,b"` mis-parsed). Found by
  selftest case "no-cache with comma inside quoted value".
- Two wrong selftest expectations (not implementation defects): `a=b=c` must
  refuse (see 3 above); request `stale-if-error=100` with staleness 50 serves
  (50 ≤ 100), not error-through.

## Evidence (all run by this seat; every verdict line names its command)

| receipt | command | result |
|---|---|---|
| `selftest.txt` | `TMPDIR=$W python3 -B w1/ExecStale/stale_extensions.py --selftest` | `cases=113 passed=113 failed=0`, rc 0 |
| `score-seed1.txt` | `python3 -B .ufo/waves/round-98/c98_stale.py --candidate-file <candidate> --work $W/work-seed1 --seed 1` | `hand=60/60 generated=240/240 refusals=36/36 met=true`, exit 0 |
| `score-seed2.txt` | same, `--seed 2` | `hand=60/60 generated=240/240 refusals=42/42 met=true`, exit 0 |
| `score-seed3.txt` | same, `--seed 3` | `hand=60/60 generated=240/240 refusals=33/33 met=true`, exit 0 |
| `score-noseed.txt` | same, no `--seed` (derived seed 1000093071) | `hand=60/60 generated=240/240 refusals=34/34 met=true`, exit 0 |

All five runs print `candidate=present sha256=895be37a… met=true` — the
candidate bytes were never changed after the first scored run. `$W` =
`/fast/scratch/hyaku/kake-r98/ExecStale` (explicit TMPDIR; the seat scratch
directory is removed at yield after receipts were copied into this w1 dir).

## Tooling

No tool installed or upgraded: stdlib python3 only (channel n/a). No pacman
use. No git mutation in LANE; no fixture repo needed for this seat.

## Risks / routes for the L1

- The claim's predicate scores from `--revision` on the landed
  `scripts/stale_extensions.py`; my runs used `--candidate-file`. The scored
  blob must be this sha256 (`895be37a…`) for the predicate's identity conjunct.
- Interpretation decisions 1 and 2 above passed every counter case but remain
  the two places a stricter/looser oracle reading could diverge on unseen
  inputs; both are flagged [INFERENCE] with their contract sentences.
- Known-limit carry (declared pre-data, not mine to repair): the candidate is
  not sandboxed beyond `-I` and a scratch cwd (R97-5); generated population
  alone does not separate exclusive-boundary and request-sie forgeries — my
  selftest covers both boundaries and request-sie precedence explicitly.
