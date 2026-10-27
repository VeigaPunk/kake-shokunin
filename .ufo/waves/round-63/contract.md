# Round-63 contract (frozen before after-state measurement, 2026-10-27)

Base revision: `13d4519818db28cd0aa912e49020659140d7b9fa` (round-62 tip).
All receipts below commit before any after-state measurement. A counter,
control or predicate changed after a seat has scored is not this round's
rule; a kill-rule breach lands the affected claim `unprovable`.

## C1 — calibration (lowest owned axis, 2/10): repair the falsified counter family and resolve the S432 disagreement

Routed defect (round-62 closure): `c62_calibration.py` computed `resolved`
from literal marker strings; the committed marker-only fixture
(`.ufo/waves/round-62/controls/false-green-fixture/corpus/`, fixture rev
`7833be888760bc7878857aa39362792b02e3ab07` as re-committed in scratch)
prints `met=true` under the old counter while the S432 disagreement stands
and no source body exists.

Frozen predicate (identical sentence in contract, counter code and receipt):
**at the measured revision, `c63_calibration.py` prints `met=true` (exit 0),
and on the marker-only fixture it prints `met=false` (exit 1), and at base it
prints `met=false` (exit 1).**

- Counter: `.ufo/waves/round-63/c63_calibration.py`, frozen sha256
  `bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91`.
- Component semantics: `quote_correction` requires the knowledge
  `[r63-correction]` block to quote the frozen span AND the round-63 ledger
  `.ufo/waves/round-63/quote-class/quote-classes.json` (sha256
  `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`) to
  record it, the ledger sha256s to re-derive from the retained blobs at the
  measured revision, and the class to re-derive inline from those blobs as
  `collapsed-only` (never gating on `scripts/quote_class.py`; see
  Separability). `criterion` requires
  `corpus/QUALITY.md` to name the located proposition
  (`X-Content-Type-Options` / `Content-Type` / `destination`). `lesson_gate`
  requires `corpus/lessons/round-63.md` to record the round-61 outside
  verdict and label its own assessment author-side. `source_row` requires the
  S432 registry row.
- Controls (committed receipts in `.ufo/waves/round-63/controls/`):
  `base-c1.txt` (base → `met=false`, exit 1);
  `control-marker-fixture.txt` (old c62 → `met=true` defect; new c63 →
  `met=false`); `control-junk-fixture.txt` (adversarial markers, no blobs →
  `met=false`).
- Kill rule: if the after receipt does not print `met=true` at the measured
  commit, or either control prints `met=true`, or any wave attack reproduces
  a marker-only green, C1 is `unprovable` (honest stop), no calibration
  credit.
- Counting command:
  `python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision <commit>`

## C2 — operability (HOLD 10): the quote-class tool runs at the measured revision

Frozen predicate: **`c63_quote_tool.py` prints `present=1 selftest=4/4
frozen_cases=ok met=true` (exit 0) at the measured revision, and `present=0
met=false` (exit 1) at base.**

- Tool: `scripts/quote_class.py`, frozen sha256
  `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14`.
  Freeze note (pre-wave, no seat scored): the tool originally resolved its
  selftest fixtures against its own file location, which the C2 counter's
  scratch-copy run cannot see; the frozen tool binds fixture resolution to
  the invoking cwd (the lane root). The contract's tool sha changed
  `40655dd87ab026fad29648bb784493d010b922b8a93dcf792f618186f2ef88a1` →
  `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14` for this
  reason only; the selftest case set and expectations are unchanged.
- Counter: `.ufo/waves/round-63/c63_quote_tool.py`, frozen sha256
  `9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e`.
- Controls: `base-c2.txt` (base → `present=0 met=false`); the counter's
  frozen-case-set check rejects a stub selftest missing the four frozen case
  ids (`inline_raw_substring`, `markup_collapsed_only`, `absent_everywhere`,
  `s432_real`).
- Kill rule: if the after receipt does not print `met=true`, or a stub tool
  passes, C2 is `unprovable`.
- Counting command:
  `python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision <commit>`

## Separability

C1 re-derives the match class inline from the retained blobs (round-50
semantics) and never gates on `scripts/quote_class.py`, so C1 is verifiable
on a tree where C2's tool never landed; C2's counter only reads the tool and
its selftest, so C2 is verifiable without C1's correction, ledger or
counters. The claims land in one round but score independently: C1's met is
calibration evidence only, C2's met is operability evidence only.

## No-harm

Append-only edits to existing files; no registry row added or changed; the
S432 row's `status`/`recheck`/`used-by` cells untouched; the round-62 held
correction preserved verbatim above the round-63 block; the old c62 counter
and its receipts remain committed as defect history.
