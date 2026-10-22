# RunEdgeProbes — C1 edge probes beyond the counter's 15 checks

Seat: KakeR28a3.RunEdgeProbes (leaf). Gate under test: repaired `scripts/citing_set.py`
at commit `b5d423fc02057f67a6f3a255808313ce40d29069`, extracted read-only via
`git -C … show b5d423f:scripts/citing_set.py` into scratch. All work under
`/fast/scratch/hyaku/kake-r28a3/w1/RunEdgeProbes/`; nothing outside the report was written
in the lane repo.

## Method
Harness `run_probes.py` builds one fixture tree per probe under `cases/`, then runs
`python3 -B citing_set.py --root <root> --population population.json --ledger ledger.json
--json [--revision …]` with stdin=/dev/null, 20 s timeout, `TMPDIR` set to scratch.
Stdout checked for exactly one JSON object via `json.JSONDecoder().raw_decode` (that
stripped text parses to a dict and nothing follows). Exit codes: 0 clean, 1 failed, 2
could-not-evaluate, 64 usage.

## Results (all 8 probes; harness exit 0)
| probe | exit | verdict | finding id / reason | JSON-ok |
|---|---|---|---|---|
| P1 population = symlink to FIFO (inside root) | 2 | could-not-evaluate | input_invalid / document_not_regular_file | yes |
| P2 ledger = symlink to /dev/null | 2 | could-not-evaluate | input_invalid / path_escapes_root | yes |
| P3 population = symlink to /dev/zero (char device) | 2 | could-not-evaluate | input_invalid / path_escapes_root | yes |
| P4a population JSON nested 1,000,000 deep | 2 | could-not-evaluate | input_invalid / document_not_json | yes |
| P4b ledger JSON nested 1,000,000 deep | 2 | could-not-evaluate | input_invalid / document_not_json | yes |
| P5 corpus/knowledge contains only an empty subdirectory | 2 | could-not-evaluate | input_invalid / corpus_empty | yes |
| P6 root is a Git repo with no commits, --revision HEAD | 2 | could-not-evaluate | input_invalid / revision_not_found | yes |
| P7 --revision of three spaces "   " | 2 | could-not-evaluate | input_invalid / revision_not_found | yes |

No hang (no probe hit the 20 s timeout), no traceback (stderr empty for every probe), no
clean verdict. The first P5 fixture accidentally left `entry.md` beside the empty
subdirectory; the gate then correctly measured `failed` (unadjudicated_citing_pair), which
is also non-clean — rebuilt fixture with no corpus files yielded `corpus_empty`.

## Commands and evidence
- Extract: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b5d423fc02057f67a6f3a255808313ce40d29069:scripts/citing_set.py > …/citing_set.py` — exit 0; sha256 `28ba996524b444b2e1c23e3751f3fa662a9a44adbfcb6337a0d23fcebaf8f415` (715 lines).
- Run: `TMPDIR=… python3 -B …/run_probes.py` — exit 0; full per-probe table in `…/probe-results.json` (sha256 `ade164ee6eb373076fa9283c9d5cdab2e9b0dbd3d3401fdb6a3150247ff27810`).
- Gate internals reviewed at `citing_set.py:213-238` (O_NONBLOCK open + fstat non-regular refusal), `:192-197` (realpath escape check), `:394-405` (RecursionError/ValueError caught), `:263-284` (walk + corpus_empty), `:312-326` (revision resolve/strip).

## Tooling record
No installs or updates performed (none needed). Environment: Python 3.14.8, git 2.56.0.
Gate executed with `python3 -B`.

## Not verified
Counter `c1_interface_count.py` runs (15 checks) and the full gate selftest were not run by
this seat; parent owns post-integration gates. No network, API, or live property access used.

## Risks / observations
- P2/P3 escape via `is_inside` realpath comparison; refusal reason is `path_escapes_root`
  rather than a device-specific id — consistent with the contract, but note the reason does
  not distinguish device from escape. Single finding per probe, exit 2 in all cases.
- 1,000,000-deep JSON is refused as `document_not_json` via RecursionError, no memory blowup
  in the gate (files ~2 MB).
- All probes held at the repair commit; no blocker.
