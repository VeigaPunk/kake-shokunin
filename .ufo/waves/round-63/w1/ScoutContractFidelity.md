# Report: ScoutContractFidelity — round-63 contract-fidelity verification

Seat: ScoutContractFidelity (leaf scout, no subagent dispatch, no commits).
Scope: verify the frozen sha256 of `c63_calibration.py`, `c63_quote_tool.py`,
`quote-classes.json` and `scripts/quote_class.py` match the files at the
measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`; verify component
semantics in the contract match the counter code; verify the freeze note's
old/new tool sha story against git history (`git log --oneline -3`).

Fleet root: `/home/vgpnk/Projects/shokunin/kake-shokunin` (cwd-relative
commands below were run with cwd = fleet root). No files were mutated; all
verification is read-only against the fleet repo plus two counter runs whose
only writes are the counters' own `tempfile.TemporaryDirectory` scratch
(C2 counter copies the tool blob there by design).

## 1. Frozen sha256 — all four files match at the measured commit

Working tree (`sha256sum`, run 2026-10-27):

```
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
```

Measured commit (`git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:<path> | sha256sum`, same run) — identical digests:

```
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  -
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  -
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  -
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  -
```

Contract values matched (contract.md lines: counter sha `bcd16f68…` in the
C1 block; ledger sha `5f48e26b…` in the C1 component-semantics paragraph;
tool sha `431e75e8…` in the C2 block; counter sha `9fcbfad0…` in the C2
block). VERIFIED — working tree is byte-identical to the measured commit for
all four frozen files.

## 2. Component semantics — contract description matches counter code

### C1 — `.ufo/waves/round-63/c63_calibration.py` (read in full, 177 lines)

- `quote_correction` (file lines ~103–135): requires the literal markers
  `"[r63-correction"` and `FROZEN_QUOTE` (the Fetch §3.6 field-purpose span)
  and the ledger path string in `corpus/knowledge/response-header-expectations.md`;
  then loads ledger `.ufo/waves/round-63/quote-class/quote-classes.json`,
  requires row `S432` and `row["rawSha256"] == sha256(blob at rev of
  .ufo/waves/round-61/sources/S432.html)` and `row["textSha256"] == sha256(blob
  at rev of .ufo/waves/round-63/quote-class/S432.txt)` and `row["quote"] ==
  FROZEN_QUOTE`; then re-derives the class inline via `classify()` — `raw-substring`
  if the quote is a substring of the raw HTML, `collapsed-only` if a substring
  of the flat text only, else `absent` — and requires `derived == "collapsed-only"
  == row["matchClass"]`. Matches contract: "requires the knowledge
  [r63-correction] block to quote the frozen span AND the round-63 ledger
  … to record it, the ledger sha256s to re-derive from the retained blobs at
  the measured revision, and the class to re-derive inline from those blobs
  as `collapsed-only`".
- Separability: no reference to `scripts/quote_class.py` anywhere in
  `c63_calibration.py` — C1 never gates on the tool, exactly as the
  contract's Separability paragraph states. VERIFIED.
- `criterion` (lines ~137–140): requires `"substantive"` and
  `"round-61-verifier-spotcheck"` in `corpus/QUALITY.md` plus all three
  `PURPOSE_TERMS` (`X-Content-Type-Options`, `Content-Type`,
  `destination`). Matches contract ("names the located proposition").
- `lesson_gate` (lines ~142–148): requires `## Gate`,
  `round-61-verifier-spotcheck`, `Disagree`, `collapsed-only`, and
  `author-side` or `self-assessment` in `corpus/lessons/round-63.md`.
  Matches contract ("records the round-61 outside verdict and labels its
  own assessment author-side").
- `source_row` (line ~150): regex `^\|\s*S432\s*\|` against
  `corpus/SOURCES.md`. Matches contract ("requires the S432 registry row").
- Marker-only fixture cannot green: with no retained blobs/ledger,
  `blobs_match=0`, `derived=unevaluable`, `class_match=0` →
  `quote_correction=0` → `met=false` regardless of planted markers
  (confirmed live by the committed `control-junk-fixture.txt` receipt and by
  the code path; see §4).

### C2 — `.ufo/waves/round-63/c63_quote_tool.py` (read in full, 110 lines)

- Reads `scripts/quote_class.py` at the revision; absent → prints
  `present=0 selftest=unevaluable met=false`, exit 1 (matches contract's
  base behaviour; base `13d45198` genuinely lacks the tool — `git show
  13d4519818db28cd0aa912e49020659140d7b9fa:scripts/quote_class.py` returns
  "path … exists on disk, but not in '13d45198…'").
- Present → copies the blob into a tempdir, runs
  `python -B <tmp>/quote_class.py --selftest --json` with `cwd=root` (the
  lane root — the exact reason for the one-line tool change, see §3),
  requires `ok`, all four frozen case ids
  `{inline_raw_substring, markup_collapsed_only, absent_everywhere, s432_real}`
  present with `passed is True` and `derived == expected`, and
  `total == passed == len(FROZEN_CASE_IDS) == 4`; prints
  `present=1 selftest={passed}/{total} frozen_cases={'ok'|'missing'} met={bool}`,
  exit 0 iff met. Matches contract frozen predicate
  `present=1 selftest=4/4 frozen_cases=ok met=true` and the stub-rejection
  clause ("rejects a stub selftest missing the four frozen case ids").

VERIFIED — counter code implements exactly the component semantics the
contract freezes.

## 3. Freeze note old/new tool sha story — consistent with git history

`git log --oneline -3 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`:

```
05b0d7f4 round-63: bind quote-class tool fixtures to cwd; contract freeze-note (pre-wave)
6d8c52a6 round-63: freeze contract; semantics-binding calibration counter; quote-class tool; S432 collapsed-only correction
13d45198 round-62 verifier spot-check (integrator, hyaku): non-author admit/reject
```

- Old tool sha `40655dd87ab026fad29648bb784493d010b922b8a93dcf792f618186f2ef88a1`
  == `git show 6d8c52a6:scripts/quote_class.py | sha256sum` (measured, matches).
- New tool sha `431e75e8…` == tool at `05b0d7f4` (§1).
- `git diff 6d8c52a6 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f --stat`:
  `.ufo/waves/round-63/contract.md | 9 ++++++++` and
  `scripts/quote_class.py | 2 +-`. The tool diff is exactly one line:
  `LANE_ROOT = Path(__file__).resolve().parent.parent` → `LANE_ROOT = Path.cwd()`.
  This is precisely the freeze-note reason: "the tool originally resolved
  its selftest fixtures against its own file location, which the C2
  counter's scratch-copy run cannot see; the frozen tool binds fixture
  resolution to the invoking cwd (the lane root)". Selftest case set and
  expectations unchanged — no other code touched. VERIFIED.
- Working-tree HEAD `15eb965c` (round-63 w1 wave spec) sits two commits
  above the measured commit; the two later commits
  (`7f77d12b` green-after receipts, `15eb965c` wave spec) do not touch any
  of the four frozen files (their shas at HEAD equal the shas at the
  measured commit, §1).

## 4. Independent reproduction of receipts (read-only runs)

Command:
`python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` (+ base twin, + both C2 twins), all from fleet root, 2026-10-27.

Output (exit codes appended by `echo "exit=$?"`):

```
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1
```

These match the committed receipts
`.ufo/waves/round-63/controls/after-c1.txt` (`met=true`, exit 0),
`after-c2.txt` (`selftest=4/4 met=true`, exit 0), `base-c1.txt`
(`met=false`, exit 1), `base-c2.txt` (`present=0 met=false`, exit 1)
byte-for-byte on the counter output lines. Also matches
`control-marker-fixture.txt` (old c62 `met=true` defect reproduced in the
receipt; new c63 `met=false`, exit 1) and `control-junk-fixture.txt`
(`met=false`, exit 1).

Ledger re-derivation spot check at the measured commit:
`git show 05b0d7f4:…/S432.html | sha256sum` → `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b` and
`git show 05b0d7f4:…/S432.txt | sha256sum` → `8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69` —
both equal the `rawSha256`/`textSha256` recorded in
`.ufo/waves/round-63/quote-class/quote-classes.json` (S432 row), and the
row's `matchClass` is `collapsed-only` with the frozen quote string.

Round-62 defect receipt `.ufo/waves/round-62/controls/counter-false-green-l1.txt`
exists and documents the independent L1 reproduction of the marker-only
false green under the old counter, matching the C1 routed-defect narrative.

## 5. Verdict

All scoped checks PASS:

1. Frozen sha256 of `c63_calibration.py`, `c63_quote_tool.py`,
   `quote-classes.json`, `scripts/quote_class.py` — VERIFIED against the
   measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` (working tree
   identical too).
2. Component semantics — VERIFIED: counter code implements exactly the
   frozen `quote_correction` / `criterion` / `lesson_gate` / `source_row`
   (C1) and present/selftest/frozen-case-set/met (C2) semantics; C1 never
   gates on the C2 tool (separability holds).
3. Freeze-note sha story — VERIFIED: old sha = tool at parent `6d8c52a6`,
   new sha = tool at measured commit; the delta is exactly the one-line
   `LANE_ROOT` cwd binding plus the contract freeze-note, matching the
   stated reason and `git log --oneline -3`.

Confidence: high (all claims backed by executed commands and quoted output
above). Remaining unknowns: none within this seat's scope — wave-attack
robustness of the counters (e.g. adversarial blob/ledger crafting) is other
seats' lane; this seat only checked fidelity of the frozen artifacts to the
contract text and git history.

Tooling installs: none (only stock `git`, `sha256sum`, `python3` already on
the host).
