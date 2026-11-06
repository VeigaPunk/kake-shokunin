# ExecTwinFresh — round 100 seat report (C2 contract v2 held-out differential)

Path note: the item asked for `.ufo/waves/round-100/w1/ExecTwinFresh.md`,
which is outside the seat's hard write bound (`w1/<SeatName>/` only). This
report is placed inside the seat directory instead. The L1 should read it
from here.

## Scope

- Twin written from the texts only: `fresh304-contract-v2.md` (sha256
  343b3a55…, verified) superseding `fresh304-contract.md`, plus the
  retained RFC 9111 / RFC 9110 bodies. `c100_fresh304.py`, the counter's
  generator, and `frozen/*.py` sources were not read for behaviour;
  `frozen/pos-oracle.py` is used only as a black-box peer process
  (`python3 -I -B`, stdin bytes).
- Lane tip: `git -C LANE rev-parse master` → e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f
  (the C1 repair commit). All 21 frozen digests verified OK.
- One live deliverable seat, no submodule dispatch.

## Files (all in `w1/ExecTwinFresh/`)

- `twin.py` (sha256 ec81a5ce…) — independent v2 implementation: full
  `#cache-directive` parser (RFC 9111 §5.2, both argument forms, OWS only
  around commas/ends, empty elements ignored, quoted-string/qdtext/
  quoted-pair incl. obs-text, malformed → `malformed cache-control`,
  V2-1b qualified case-insensitive, V2-1c substring ignore), trimmed
  outputs (V2-2), stored proxy-field drop (V2-3), e1–e7 clarifications.
- `gen_run.py` (sha256 bfc54573…) — own generator + differential runner,
  seed 100226, N=3600 (>3000), 8 threads.
- `results.jsonl` (sha256 82ebc305…) — 3600 rows (input, both sides, agree).
- `groups.txt` / `run.txt` — counts, command log.
- `disagreements.md` — zero disagreements, counts per class.

## Result

- 3600 inputs; **3600 agree, 0 disagreements**: 2106 identical rc=0 JSON,
  1494 identical rc=1 (empty stdout + `invalid_input:` prefix; reason text
  not compared). Decisions: update=1014, no-update=591,
  must-not-update=501. Rules: strong=1094, weak=523, no-validator=489.
  CC-tagged inputs: 1452.
- No oracle defect, twin defect, or contract ambiguity observed on this
  corpus. (Two independent implementations can share a blind spot; the
  differential establishes disagreement only.)
- The round-99 ambiguity (LC6 case) is settled in v2 over the oracle's
  side (V2-1b case-insensitive) — the twin now implements it identically.

Verdict line (run.txt and disagreements.md): `TWIN inputs=3600 disagreements=0 oracle_defects=0 twin_defects=0 ambiguities=0`

## Checks executed (command → observed rc)

- `cd .../round-100 && sha256sum -c controls/instrument-sha256.txt` → rc 0, all 21 OK.
- `git -C LANE rev-parse master` → e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f.
- `python3 -I -B gen_run.py` (scratch, seed 100226) → rc 0, inputs=3600 disagreements=0.
- Staged probes vs oracle (CC parsing, connection-token handling, name/value
  controls, raw non-UTF-8 stdin): all matched; micro-fuzz of quoted-string
  variants also 0 diffs.

## Tooling

No tools installed or upgraded. Python 3.14.8 (`/usr/bin/python3`, stdlib
only). No pacman, no `~/.local/bin` writes.

## Cleanup

No gel scratch repos were created in the lane (no fixture git ops needed
beyond read-only `rev-parse`). Seat scratch
`/fast/scratch/hyaku/kake-r100/ExecTwinFresh/` is removed only if this
seat is the sole owner of that subtree; see the cleanup note handed to
the L1 (the seat's disposable scratch is that directory alone).

## Verdict

TWIN inputs=3600 disagreements=0 oracle_defects=0 twin_defects=0 ambiguities=0
