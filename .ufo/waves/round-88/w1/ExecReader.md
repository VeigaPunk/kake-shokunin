# ExecReader — round 88 · C2 candidate (v1 wave)

Seat ExecReader (executor), lane `kake-shokunin`. Findings are lane-internal, not
outside admission. No production byte was edited; the only writes are
`.ufo/waves/round-88/w1/ExecReader/` and this file.

Base `f4479c14813037ad993a49a3dee4028763470f7a`. Freeze was **amended from v2 to v3 while this
seat was scoring**; D1 below records it with artifacts. The candidate and its
receipt are against the current freeze (v3), which also carries the precedence rule I had
independently measured as a v2 defect.

## Deliverable

| item | value |
|---|---|
| candidate | `.ufo/waves/round-88/w1/ExecReader/vary_match.py` |
| sha256 | `fdceef474e618d6664c15333cba6a1fa136fbc44f2791bbbdbf92d234fb287d6` |
| size | 294 lines / 12 937 bytes, stdlib only, reads only stdin |
| `--selftest` | `selftest: 35/35 passed`, exit 0, stderr empty; red path (one expectation forced wrong) `34/35`, exit 1 (`neg-selftest.txt`) |
| C2 score (v3) | `frozen 20/20  random 200/200  met=true`, exit 0, stderr empty |

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ExecReader/vary_match.py --selftest
35 × "PASS ..."; selftest: 35/35 passed            exit 0   (receipt selftest-v3.txt)

$ TMPDIR=/fast/scratch/hyaku/kake-r88/ExecReader python3 -B \
    /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py \
    --tool /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ExecReader/vary_match.py \
    --work /fast/scratch/hyaku/kake-r88/ExecReader/work-v3
exit 0   (receipt c2-score-v3.json / c2-score-v3.exit; stderr 0 bytes)
```

The seat command wrote `LANE/...` for `--tool`; my process cwd is the fleet root, so I passed the
absolute path. Same bytes, same tool sha. Full JSON line, verbatim:

```json
{"cases_sha256": "c461cbd87bc9b4818381c42cd847ee94c642bedfb2cf6c829a1828c311b0802d", "claim": "C2", "details": [], "frozen": 20, "frozen_total": 20, "met": true, "random": 200, "random_sha256": "52714a5f4ae9b66ee444f39284b6e5ce575c6ae5760965fb8736e6983444b981", "random_total": 200, "revision": "file:/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ExecReader/vary_match.py", "tool_sha256": "fdceef474e618d6664c15333cba6a1fa136fbc44f2791bbbdbf92d234fb287d6"}
```

Frozen bytes read (worktree == `52e41d2d` for all three):
`c88_vary.py` `e4cf5ad943a2f54742562ad169f437197c01bb67eb423aa93d457ba912c95124`,
`vary-cases.json` `c461cbd87bc9b4818381c42cd847ee94c642bedfb2cf6c829a1828c311b0802d`,
`contract.md` `639035d3e1f6ea962ca86c4629763e22b00956584db73f77ae91b1ccfb2b1d8a`.
Neither the case file nor the counter was edited by this seat.

## Per-case evidence

Every one of the 220 cases was also run individually outside the counter (`percase.py`, exact
exit / exact stdout bytes / exact stderr), not just tallied:

```
rows 220  frozen 20  random 200
frozen_fails 0  random_fails 0        exit 0   (receipts percase.tsv, percase-summary.txt)
```

Frozen set, 20/20: `1 match · 2 match · 3 mismatch · 4 match · 5 mismatch · 6 mismatch ·
7 mismatch · 8 mismatch · 9 match · 10 mismatch · 11 match · 12 mismatch · 13 match ·
14 invalid · 15 invalid · 16 match · 17 mismatch · 18 mismatch · 19 invalid · 20 invalid`.
Random set, 200/200, same distribution the counter's own selftest prints
(`match=67 mismatch=109 invalid=24`, receipt `counter-selftest-v3.txt`, 17/17, exit 0).
**No failing case exists on the v3 freeze.** The only failures I ever measured were under v2 and
are explained in D1 below.

## Candidate ↔ declared profile

| declared rule (contract.md C2) | code | proof |
|---|---|---|
| field names ASCII case-insensitive | `ascii_lower` translate on A–Z only; token alphabet is ASCII | selftest 2, 14 |
| nominated names deduplicated | `seen` set in `parse_vary` | selftest 14 |
| array field lines combine in order with `, ` | `', '.join(value)` | selftest 17–19 |
| values byte-compare after SP/HTAB trim only | `left.strip(' \t') != right.strip(' \t')`, nothing else | selftest 9, 10, 20, 32 |
| absent both → match; absent one → mismatch | `get` pair check | selftest 4–6 |
| `*` member always fails | `star` ⇒ `mismatch` after validation | selftest 7, 8 |
| non-string Vary/values, non-token/empty members, empty Vary refused | `refuse()` with `invalid_input:` and empty stdout | selftest 15, 21–24, 27 |
| validation precedes the wildcard rule (v3) | maps normalised before `if star` | selftest 29–31 |
| `--selftest` ≥12 isolated assertions | 35 assertions, each a fresh `python3 -B <this file>` subprocess | selftest receipt |

Decisions the contract leaves open, taken conservatively and declared in the docstring: a request
map that is not an object is refused; a field name that is not a token (e.g. trailing SP) is
refused; two keys differing only in ASCII case are refused as ambiguous (the counter's reference
does the same); a payload that is not one JSON object, missing `vary`/`stored`/`presented`,
malformed, BOM-prefixed or with trailing bytes is refused. `stdout` is the verdict with **no
trailing newline** (`b'match'`), and refusals write nothing to stdout — both stricter than the
counter's `.strip()` checks.

Differential against the counter's reference on 5 000 fresh generated inputs (seeds 1, 7, 88, 527,
88088; 1 000 each): **0 disagreements** (`differential.txt`). 500 extra inputs whose alphabet
admits a trailing LF produced 8 disagreements, all of them the counter defect D2 below.

## Defects found in the round's own counters and case set

D1 (record integrity, affects C2 receipts) — **freeze v3 landed after a seat had already scored.**
`52e41d2d` says “v3 (still before any candidate was scored and before any production byte
changed)”. My v2-scored receipt predates it:

| time (-0300) | artifact |
|---|---|
| 15:44:46 | `vary-cases.json` mtime (unchanged through the amendment) |
| 15:49:39 | v2 commit `80637397` |
| **15:55:53** | **my v2 score receipt**: `frozen 20/20 random 200/200 met=true`, `random_sha256 004a8eb7…`, `tool_sha256 51f5d778…` (`c2-score.json`) |
| 15:56:39 | `w1/L1/vary_match.py` mtime — a candidate file, shipped by the v3 commit |
| 15:57:12 | `c88_vary.py` mtime (the v3 reference) |
| 15:57:35 | `controls/c2-selftest.txt` mtime |
| 15:58:05 | v3 commit `52e41d2d` |
| 15:59:31 | my v3 score receipt |

Consequences, stated without judging intent: (a) the v2 receipt can no longer be re-derived from
current bytes — the same command now prints `random_sha256 52714a5f…`; (b) C2's kill rule says
“the case set, the seed, the generator and the reference are not edited after scoring”, and v3
edits the reference after a seat scored; (c) the amendment is substantively right (it is exactly
the precedence defect I measured on v2) but the commit's “before any candidate was scored” is
contradicted by the artifacts above. The v2 measurement that pins it: the same reader with the two checks in the
opposite order (validation before the wildcard) scored `20/20` frozen and `197/200` random under v2,
failing exactly **r53, r150, r193** — the three inputs that mix a `Vary` `*` member with a
non-string/empty-array field value (`alt-validity-first.json`, exit 1, `details` naming all
three). Those are precisely the three cases v3 re-labels `invalid`. Recommendation: keep both
receipts in the round evidence, report C2 against v3, and state in SCORECARD/LOG that the freeze
was amended after ExecReader's v2 score. I did not retain the v2 candidate bytes (overwritten in
place at 15:57+); only `tool_sha256 51f5d778…` in `c2-score.json` identifies them — my omission,
recorded here.

D2 (counter reference, latent) — `is_token` accepts a **single trailing LF**: `TOKEN` ends in `$`,
which in Python matches before a final newline. `is_token('accept-encoding\n') is True`, so
`reference` treats `Vary: accept-encoding\n` (and a field name ending in LF) as a valid token
instead of refusing it, contradicting the declared “non-token members … refused”. Neither
population contains an LF, so it cannot move a score today; it is a live hole for any future case
and a candidate exploit surface (`is_token('a\n\n')` is False, so only exactly one LF). Evidence:
8/500 newline fuzz disagreements (`differential.txt`), e.g. `vary='accept-encoding\n, x-kake-token'`
with matching maps → reference `match`, candidate `invalid`. Fix: `re.fullmatch` / `\Z`.

D3 (counter measurement, medium) — verdict and refusal checks are `.strip()`-based, so the
instrument cannot enforce the contract's “exactly `match`/`mismatch` on stdout, empty stderr” or
“no stdout” on refusal. A stub printing `"  match \n\n\t"` scores the constant-match tally
(`7/20 + 67/200`), and a stub printing `" \n\t"` to stdout with `invalid_input:` on stderr scores
the always-invalid tally (`4/20 + 24/200`) — both `met=false` only because they are constant
policies, not because of the padding (`stub-tallies-v3.txt`). Failure `details` also store
`p.stdout.strip()[:40]`, so padding is invisible in receipts. The C2 claim text should not say the
counter enforces byte-exact output.

D4 (counter robustness, low) — a candidate that writes non-UTF-8 stdout **crashes the counter**:
`subprocess.run(..., text=True)` at `c88_vary.py:175` raises `UnicodeDecodeError`, the process
exits 1 with a traceback and prints **no JSON receipt** (`stub-v3-bad_utf8.err`). It fails closed
(never `met=true`), but the measurement is lost and a candidate can abort a run.

D5 (receipt completeness, low) — `details=(frozen_details + random_details)[:12]` truncates the
failure list at 12 entries, so a badly failing candidate's receipt hides the rest.

D6 (reproducibility, measured benign) — the “frozen” random population is an artifact of
CPython's `random.sample/shuffle/choice`, whose sequences are not part of the module's documented
cross-version guarantee (only `random()` is). Measured identical `random_sha256` and identical
`match/mismatch/invalid = 67/109/24` on CPython 3.12.15, 3.13.16, 3.14.8 and 3.15.0
(`cross-version-sha.txt`), so the risk is residual, not present on this host. The generated
*inputs* are what v3 preserved: comparing the v2 and v3 modules over the same 200 inputs shows
**3 expectation flips only**, r53/r150/r193 `mismatch→invalid`, same inputs and order
(`compare-v2-v3.txt`).

D7 (spec gap, low) — refusal of two keys differing only in ASCII case is implemented by the
counter's reference and by my candidate, but is stated nowhere in `contract.md` and pinned by no
case. Either declare it or drop it; scoring is unaffected (no case exercises it).

D8 (claim wording, inference) — “empty Vary is refused” is an **adapter** choice, not something
RFC 9111 §4.1 requires [INFERENCE: I did not fetch the RFC this seat; ScoutSpec owns quotes]. The
list extension tolerates empty list elements (recipients parse and ignore), so a stricter reader
could call `Vary: ` a zero-member list and answer `match`. The contract declares refusal, so the
reader is correct to the contract — but the knowledge entry must attribute this to the adapter,
not to §4.1.

D9 (case-coverage, honest limit) — the frozen 20 pin only part of the declared profile: HTAB-only
values, empty arrays, star-vs-invalid precedence, LF tokens, non-token request keys, OWS around
`Vary` members, duplicate case-variant keys and one-element arrays appear in **no** frozen case
(empty arrays and precedence are pinned only by the random population: r53/r150/r193). My
`--selftest` covers all of them; the frozen set alone would not.

## What the candidate adds over both populations

Probed and recorded in `edge-probes.txt`: empty stdin, `null`, a JSON array, a lone-surrogate
`Vary`, a UTF-8 BOM, trailing bytes after the JSON and a 30-digit integer all exit 1 with empty
stdout and an `invalid_input:` stderr line; a textually duplicated JSON key resolves by JSON's
last-wins rule (`{"vary":"a","vary":"b",…}` → `match`, `b` absent on both sides). No crash path
was found: every refusal goes through `refuse()`, so exit 1 always carries the prefix.

## Limits

- This reader answers only the §4.1 field-match question; it builds no cache key and claims no
  storage, revalidation, freshness, serving or browser behaviour. A `mismatch` may be more
  conservative than a field-specific rule; a `match` uses only §4.1-permitted transformations.
- I derived the reader from `contract.md` and the counter's declared reference, not from a
  primary RFC fetch (my item names no URL); the verdict labels are therefore not an independent
  spec re-derivation. ExecCases/ReviewReader/ScoutSpec own that.
- I did not read any sibling candidate, including `w1/L1/vary_match.py`; independence kept.
- The v2 candidate bytes were not retained (see D1).
- No network request was made; no live surface is asserted clean.

## Hygiene

- Scratch `/fast/scratch/hyaku/kake-r88/ExecReader/` created explicitly, `TMPDIR` pointed there
  (the counter's `--selftest` uses `tempfile`), one work dir per run, no `/tmp` path used, and the
  directory is deleted before yield after copying receipts.
- No install or upgrade was needed (python3.14.8 already present); no `pacman`, no `uv`, no
  `~/.local/bin` write.
- No mutating git/jj command: only `git rev-parse`, `git log`, `git show`, `git diff`,
  `git status` reads. No commit, push, deploy or account action.
- Measured `git rev-parse --show-toplevel` = `/home/vgpnk/Projects/shokunin/kake-shokunin`
  before any read-only git use in the comparison harness.

## Files written (all inside the seat's two allowed paths)

`vary_match.py`, `selftest-v3.txt`, `neg-selftest.txt`, `neg_selftest.py`,
`neg-selftest-check.txt`, `c2-score-v3.json`, `c2-score-v3.exit`, `c2-score.json`,
`c2-score.exit`, `alt-validity-first.json`, `alt-validity-first.exit`, `percase.py`,
`percase.tsv`, `percase-summary.txt`, `differential.py`, `differential.txt`, `compare_v2_v3.py`,
`compare-v2-v3.txt`, `counter-selftest-v3.txt`, `cross-version-sha.txt`, `edge-probes.txt`,
`stub_spacey_match.py`, `stub_ws_invalid.py`, `stub_bad_utf8.py`, `stub-tallies-v3.txt`,
`stub-v3-bad_utf8.err`, `receipts-sha256.txt` (manifest of all of the above), and this
`ExecReader.md`.
