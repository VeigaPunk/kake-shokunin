# ReviewerC1Separability — round-63 w1 separability review (2026-10-27)

Item: verify claim separability from the code — (a) `c63_calibration.py` never reads
`scripts/quote_class.py` and re-derives the class inline; (b) `c63_quote_tool.py` never
reads the ledger/correction; conclude whether each claim is verifiable without the other
landed, per `AXES.md`. All paths below absolute; `/k` = `/home/vgpnk/Projects/shokunin/kake-shokunin`.

**Verdict: SEPARABLE — both claims verified independent; no defects found.** One
informational note on a shared evidence blob (not a claim artifact).

## 0. Frozen-byte fidelity (precondition)

Working tree and measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` are
byte-identical for all four frozen files (`git show 05b0d7f4:<f> | sha256sum`):

| File | sha256 | contract match |
|---|---|---|
| `/k/.ufo/waves/round-63/c63_calibration.py` | `bcd16f68…a3fc91` | yes |
| `/k/.ufo/waves/round-63/c63_quote_tool.py` | `9fcbfad0…7f01e` | yes |
| `/k/scripts/quote_class.py` | `431e75e8…41f14` | yes |
| `/k/.ufo/waves/round-63/quote-class/quote-classes.json` | `5f48e26b…0c42d` | yes |

`git status --porcelain` on these paths: clean (only untracked `w1*/` lane outputs).

## 1. C1 never reads the C2 tool; class re-derived inline

Full read of `/k/.ufo/waves/round-63/c63_calibration.py` (177 lines) + greps:

- Imports (lines 31–38): `argparse, hashlib, json, re, subprocess, sys` only. No
  `importlib/__import__/eval/exec/getattr/os.system/popen` anywhere (grep: 0 hits).
- Every content read goes through `git_show()` (lines 70–76), whose only `subprocess`
  call is `git -C <root> show <rev>:<rel>`; the only other subprocess is the
  `git rev-parse --verify` probe (lines 87–88). Call sites enumerate the complete read
  surface: `PATHS` (lines 44–50: five corpus files), `QUOTE_REL` = round-61 S432.html
  (line 41), `TEXT_REL` = round-63 S432.txt (line 42), `LEDGER_REL` = the ledger
  (line 43) — fetched at lines 107–109. `scripts/quote_class.py` is **not** among them;
  there is no `open()`/`Path`/`read_text` read in the file at all.
- The only occurrences of the string `scripts/quote_class.py` are prose: docstring
  lines 15–16 and the `classify` docstring lines 60–62 ("C1 never gates on the tool").
- Inline re-derivation: `classify()` lines 59–67 — `raw-substring` if quote ∈ raw,
  else `collapsed-only` if quote ∈ text, else `absent` — semantics line-identical to
  `/k/scripts/quote_class.py:32-37`. The gate chain uses only inline results:
  `blobs_match` (133–136, ledger sha256s vs `git show` blobs), `derived = classify(...)`
  (139–141), `class_match` (142–143), `quote_correction = correction and blobs_match and
  class_match` (145), `resolved` (164). The tool's output is never an input.

## 2. C2 never reads the ledger or the correction

Full read of `/k/.ufo/waves/round-63/c63_quote_tool.py` (91 lines): its entire input
surface is `TOOL_REL` (line 24) via `git show` (line 56) plus executing that blob's
`--selftest --json` with `cwd=root` (lines 62–67). Grep for
`ledger|correction|knowledge|QUALITY|SOURCES|lesson|S432|quote-class|r63` hits only
docstring lines 2/4–5; no code reference to `.ufo/waves/round-63/quote-class/quote-classes.json`
or `corpus/knowledge/response-header-expectations.md`.

Transitive check (C2's met flows through the tool, so the tool was audited too): full
read of `/k/scripts/quote_class.py` (147 lines). Its only file reads are
`raw_path/text_path.read_bytes()` (lines 84–85 selftest, 129–130 classify mode) over
`FIXTURE_CASES`: four committed fixtures under `scripts/fixtures/quote-class/`
(`FIXTURES`, line 25; files exist at the measured commit) and the two retained blobs for
`s432_real` (lines 63–72: round-61 `S432.html`, round-63 `S432.txt`). It never opens the
ledger, the correction block, `QUALITY.md`, lessons, `SOURCES.md`, or `c63_calibration.py`.

## 3. Empirical separation tests (throwaway `--shared` clone, identity `r63-sep-review` inside scratch only; scratch deleted after)

Baseline at fleet root, read-only — reproduces the committed controls exactly:
- `python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4…` →
  `… quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1
  lesson_gate=1 source_row=1 unresolved=0 met=true`, exit 0 (= `controls/after-c1.txt`);
  at base `13d4519…` → `met=false`, exit 1.
- `python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4…` →
  `present=1 selftest=4/4 frozen_cases=ok met=true`, exit 0 (= `controls/after-c2.txt`);
  at base → `present=0 … met=false`, exit 1.

- **Demo A — C1 with C2's tool deleted** (scratch commit `72c2cbb9`, `git rm scripts/quote_class.py`):
  C1 → `quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 … met=true`, exit 0.
  C1 verifies on a tree where the C2 tool never landed.
- **Demo B1 — C2 with every C1 landed artifact deleted** (scratch commit `f38e6312`:
  `git rm .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-63/quote-class/quote-classes.json
  corpus/knowledge/response-header-expectations.md`):
  C2 → `present=1 selftest=4/4 frozen_cases=ok met=true`, exit 0. C2 verifies without
  C1's correction, ledger or counters.
- **Demo B2 — boundary quantification** (scratch commit `bf2b1d60`: additionally
  `git rm .ufo/waves/round-63/quote-class/S432.txt`): C2 → `present=1 selftest=failed
  met=false`, exit 1. The sole residual coupling is the shared retained text blob.

## 4. Conclusion per AXES.md

AXES.md (fleet root `/home/vgpnk/Projects/shokunin/AXES.md`, "Working the axes"):
claims must be **causally separable** — each verifiable without the others having landed —
and name **distinct axes**. Verified:

- **C1 without C2**: proven statically (no read path to the tool) and empirically (Demo A,
  `met=true` with tool absent). Holds.
- **C2 without C1**: proven statically (counter and tool never read correction/ledger/counter)
  and empirically (Demo B1, `met=true` with all three removed). Holds.
- **Distinct axes**: C1 = calibration (the lane's lowest owned axis, 2/10, satisfying the
  lowest-axis obligation), C2 = operability. Holds.

The contract's Separability paragraph is accurate as frozen. The claims land in one round
but score independently.

## Findings by severity

- **Defects: none.**
- **Informational (shared evidence substrate):** both claims' `met` transitively require
  the two retained blobs; `.ufo/waves/round-63/quote-class/S432.txt` is a round-63 file
  (absent at base `13d4519…`, confirmed via `git cat-file -e`), co-located with — but
  distinct from — C1's ledger. A hypothetical tree landing only the tool+fixtures would
  fail C2's frozen case `s432_real` (Demo B2). This is shared evidence inputted by both
  predicates, not a landed artifact of either claim, and the frozen contract enumerates
  the dependency boundary correctly (tool ↔ correction/ledger/counters). No action needed;
  recorded for the aggregator's honesty ledger.

## Residual risk & verification gaps

- Did not re-audit the c62 legacy counter or the scribes' scorecard rows (out of scope).
- Ledger content correctness (sha256 re-derivation honesty) is C1's own gate, exercised
  by the counter runs above, not independently re-derived by this seat beyond the
  `blobs_match=1` observation.
- Tooling installs: none. Lane compliance: fleet root touched read-only only (counter
  runs write only throwaway tempdirs); scratch clone verified via
  `git rev-parse --show-toplevel` before use and deleted; no writes outside this Report.
