# Round-64 contract (frozen before after-state measurement, 2026-10-30)

Base revision: `1a48131577ba82c967650561be34e8dba909432a` (round-63 tip).
All receipts listed below commit with the round; a counter, control or
predicate changed after a seat has scored is not this round's rule; a
kill-rule breach lands the affected claim `unprovable`.

Frozen instruments (sha256 at freeze):

- `.ufo/waves/round-64/c64_calibration.py` —
  `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf`
- `.ufo/waves/round-64/c64_quote_tool.py` —
  `96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b`
- `.ufo/waves/round-64/fixtures/build_fixtures.py` —
  `7fbd8cbc67c17264096e44474a698b3f0d7702c3e1cc23f0b5bdaa26ee0271d3`
- `.ufo/waves/round-64/fixtures/stub_tool.py` —
  `7c78a05df78703044f8fe8fa02793a63b580f6353f58e8ebcee836038762edde`

Fixture revisions (built by `build_fixtures.py` in
`/fast/scratch/hyaku/kake-r64/l1/fixtures/`, receipts
`.ufo/waves/round-64/controls/fixture-builds.txt`): stub-repo
`14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3`; marker-repo
`4c666e7632cb2093fbed18117e460bf37d1d14ce`; fabrication-repo
`f924538ede0d290d74af3126a40103887f4c8d46`; junk-repo
`82dcba0d2f83bdd427c9566b33739af71fe84efc`; ledger-mut-repo
`5b981bd0c43dd30c1546a1966d971f4227f60973`.

## C1 — calibration (lowest owned axis, 2/10): the repaired semantics-binding counter verifies the S432 resolution

Routed defect (round-63 settlement + closure item 1): the round-63 frozen
counter could be greened by marker prose and by a digest-self-consistent
fabrication (circular text blob, unmasked `unresolved`, unbound located
lines, unquoted spot verdict).

Frozen predicate (identical sentence in this contract, the counter docstring
and the receipt labels): **at the measured revision,
`c64_calibration.py --root . --revision <measured>` prints `met=true`
(exit 0), and on each committed control fixture (marker-only
`4c666e76`, digest-consistent fabrication `f924538e`, junk `82dcba0d`,
ledger-mutation `5b981bd0`) it prints `met=false` (exit 1), and at the base
`1a481315` it prints `met=false` (exit 1).**

- Counter pins (constants in the counter): raw blob
  `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`, flat
  text `8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69`,
  ledger `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`,
  recipe `6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405`,
  located lines `6150-6154`, frozen span, and the spot-check verdict span
  `is only a generic lead-in, not substantive evidence for a response-header
  expectation` bound block-level into `corpus/lessons/round-64.md` `## Gate`.
- Controls (committed receipts, all `met=false` exit 1 unless named):
  `controls/base-c1.txt`, `controls/control-marker.txt`,
  `controls/control-fabrication.txt`, `controls/control-junk.txt`,
  `controls/control-ledger-mut.txt`; selftest `controls/selftest-c1.txt`
  (26/26).
- Kill rule: if the after receipt does not print `met=true` at the measured
  commit, or any pinned sha differs at the measured revision, or any control
  prints `met=true`, or the counter crashes on adversarial input, or any
  wave attack reproduces a marker-only / stub / do-nothing /
  digest-consistent-fabrication green, C1 is `unprovable` (honest stop), no
  calibration credit.
- Counting command:
  `python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision <commit>`

## C2 — operability (HOLD 10): the quote-class tool gate is stub-proof

Routed defect (round-63 closure item 2): the round-63 counter validated
self-report shape; a canned-JSON stub passed it and adversarial JSON crashed
it.

Frozen predicate (identical sentence in this contract, the counter docstring
and the receipt labels): **at the measured revision,
`c64_quote_tool.py --root . --revision <measured>` prints `met=true`
(exit 0) over the lane tree; on the committed stub fixture
(`14fe2eab`) it prints `tool_sha=mismatch met=false` (exit 1); and the
round-63 counter `c63_quote_tool.py` run on that same stub fixture prints
`met=true` (exit 0) — the routed round-63 defect, reproduced.** (At the
base the real tool already exists, so the base tree also prints `met=true`;
the stub differential is the claim's falsifiable before/after.)

- Stub definition: "tool sha ≠ frozen sha" with the round-63 tool sha frozen
  `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14` (the
  tool is unchanged this round; a tool whose sha differs at the measured
  revision is `unprovable` by the kill rule).
- Controls: `controls/stub-c64.txt` (`tool_sha=mismatch met=false` exit 1),
  `controls/stub-c63-defect.txt` (`met=true` exit 0 — the defect),
  `controls/selftest-c2.txt` (11/11).
- Kill rule: if the after receipt does not print `met=true` at the measured
  commit, or the stub control prints anything but
  `tool_sha=mismatch met=false`, or `c63_quote_tool.py` fails to reproduce
  the defect green on the stub, or any wave attack passes a stub/lying
  tool through the new counter, C2 is `unprovable`, no capability row.
- Counting command:
  `python3 -B .ufo/waves/round-64/c64_quote_tool.py --root . --revision <commit>`

## C3 — freshness (HOLD 10): the standing §paths gate evaluates again

Routed defect (this round's build): the §paths freshness gate stood
could-not-evaluate (`paths sidecar binding invalid: SKILL.md:364`, exit 2)
from roughly round 56 to 63 — receipt `controls/sweep-before.txt` (exit 2 at
the round-60 tip `9f671056`, the round-61 base `d2da25de` and the base
`1a481315`).

Frozen predicate (identical sentence in this contract, the lesson §Mistakes
and the receipt labels): **on the measured tree,
`node scripts/freshness-sweep.mjs --offline` prints `VERDICT: OK` and exits
0, where at the base archive it exits 2 with `paths sidecar binding invalid:
SKILL.md:364`; the repair is exactly the seven-entry sidecar re-pin recorded
old→new in `controls/sidecar-repin-map.txt` and
`corpus/lessons/round-64.md` §Mistakes.**

- The re-pin changes only `line` and `lineSha256` of seven SKILL.md entries
  of `corpus/knowledge/freshness-sidecar.json` (23 further entries verified
  byte-identical at their pinned lines and untouched); no note, kind, date
  or token cell changes; `corpus/SOURCES.md` is untouched.
- Kill rule: if the after receipt exits anything but 0, or the §paths drift
  count is non-zero, or any sidecar cell other than the seven `line`/
  `lineSha256` pairs changed, C3 is `unprovable`.
- Counting command: `node scripts/freshness-sweep.mjs --offline`
  (run at the measured tree root).

## Separability

C1 never gates on `scripts/quote_class.py` (it re-derives the class inline
and re-executes the recipe itself), so C1 verifies on a tree where the tool
or its counter never landed; C2's counter only reads the tool, its fixtures
and the retained blobs at the revision, so C2 verifies without C1's lesson
gate or counters; C3 touches only `corpus/knowledge/freshness-sidecar.json`
and reads no claim instrument. Each claim is re-derivable alone.

## No-harm

Append-only edits to `corpus/QUALITY.md`, `LOG.md`, `SCORECARD.md`;
`SKILL.md` gains two gate-registry rows (the new counters) — a line-pinned
sidecar file, so the sidecar re-pin in C3 is sequenced in the same build;
`corpus/SOURCES.md` untouched (171 rows before and after); the round-62/63
held corrections preserved verbatim; the round-63 counters and receipts
remain committed and are re-run at the measured revision in the no-harm
sweep. After-receipts: `controls/after-c1.txt`, `controls/after-c2.txt`,
`controls/sweep-after.txt`, `controls/census-before.txt` /
`controls/census-after.txt`.
