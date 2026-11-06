# ExecTwinFresh — round 99 seat report (differential falsifier of the C2 oracle)

Path note: the item asked for `.ufo/waves/round-99/w1/ExecTwinFresh.md`, which is outside the
seat's hard write bound (`w1/<SeatName>/` only). This report is placed inside the seat directory
instead. The L1 should read it from here.

## Scope

- Twin written from the contract text only: `fresh304-contract.md` (sha256 2be46b4d…) plus the
  retained RFC 9111 body for background. `c99_fresh304.py`, `frozen/*.py` (other than as a black-box
  peer process), and the counter's generator were not read.
- Oracle used as a black box: `frozen/pos-oracle.py` (sha256 ae789bfb…, verified against
  `controls/instrument-sha256.txt`: OK).
- Lane tip read-only: `master` = 7f5b1b7b8dbfdae74dfe6d487bbf5406c478b916. Round base
  cde408e5817bf1376c701d8decc5469fa82b2985 is unchanged in the frozen digests.

## Result

- Inputs: 2400 (own generator, seed 99226, 8 scenario families, 18 refusal kinds).
- Agree: 2370 (1845 identical OK JSON, 525 identical refusal shape).
- Disagree: 30. All one class, all twin-accepts / oracle-refuses, all a case-variant qualified
  Cache-Control directive (`Private="g"`, `NO-CACHE="x"`) in the 304 (LC6).
- Classification: **contract ambiguity**. Oracle defect 0. The twin's case-sensitive reading is
  the literal LC6 text; the cited RFC 9111 line 1098 says directive names are compared
  case-insensitively, which the oracle follows. The contract needs a sentence, the oracle does not
  need a repair. The disagreement is recorded, not fixed; the contract and counter are frozen.

Verdict line (run.txt and disagreements.md): `TWIN inputs=2400 disagreements=30 oracle-defects=0 ambiguities=30`

## Harness correction (disclosed)

The first run reported 555 disagreements because the seat's own predicate scored both-refuse rows
as disagreements. The predicate was corrected; the reported counts above come from the corrected
run. No oracle or twin behaviour changed between runs. Both runs are the same 2400-input corpus.

## Checks executed (command → observed rc)

- `sha256sum -c controls/instrument-sha256.txt` → rc 0, all 11 files OK.
- `printf '{"stored":[],"response":{"status":304,"headers":{}}}' | python3 -B frozen/pos-oracle.py` → rc 0, stdout `{"decision": "no-update", "rule": "no-validator", "updated": []}`.
- `printf 'not json' | python3 -B frozen/pos-oracle.py` → rc 1, stderr `invalid_input: Expecting value…`.
- `python3 -B gen_run.py` (seat scratch, corrected predicate) → rc 0, `inputs=2400 disagreements=30 groups=2`.
- Targeted oracle/twin probes on Cache-Control case variants (run.txt) → recorded per variant.
- `grep` of RFC 9111 retained body for directive case and §3.1 qualified forms → lines 1098, 1273–1284.
- `grep` of `controls/ctl-c2-*.txt` for `cache-control` → no matches (rc 1): no frozen control
  exercises Cache-Control.

Not run: the twin was not checked for conformance beyond the differential. Two independent
implementations can share a blind spot; the differential establishes disagreement only.

## Tooling

No tools installed or upgraded. Python 3.14.8 (`/usr/bin/python3`, stdlib only). No pacman, no
`~/.local/bin` writes.

## Files (all in `w1/ExecTwinFresh/`)

- `twin.py` (sha256 dabc0a88…) — the twin.
- `gen_run.py` (sha256 ee3f0cce…) — generator + differential runner (corrected predicate).
- `results.jsonl` — 2400 rows (input, both sides, agree flag).
- `groups.txt`, `run.stdout`, `run.stderr` — runner output (run.stderr empty).
- `run.txt` — command, n, disagreement count, tallies, probes.
- `disagreements.md` — the 30-input class, the quoted deciding sentences, classification, and
  the recommended routing for the L1.

## Routing for the L1 (not acted on by this seat)

1. Contract: decide whether LC6 directive names are case-sensitive. The RFC text favours
   case-insensitive; the oracle implements that. A one-sentence clarification in the contract
   settles it either way.
2. Counter: no change requested. The oracle's current behaviour is consistent with the cited RFC.
3. The frozen controls contain no Cache-Control cases. A future round should add one.

## Verdict

TWIN inputs=2400 disagreements=30 oracle-defects=0 ambiguities=30

## Cleanup

Seat scratch `/fast/scratch/hyaku/kake-r99/ExecTwinFresh/` removed after the receipts above were
copied into `w1/ExecTwinFresh/`. No other path was removed.
