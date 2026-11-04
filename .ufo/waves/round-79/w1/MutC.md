# MutC — mutation test of the round-79 instruments (w1)

**Verdict: the frozen C2 matrix is a strong killer — all 10 semantic tool mutants killed, each by the exact predicted frozen case. The C1 counter holds for its two reachable-by-fixture mutants (k1, k2 killed), but three predicate conjuncts (`wrong_kind`, `malformed`, `symlinks`) are unguarded by the frozen fixture battery and the c79 selftest: mutants dropping them survive both and were killed only by scratch probe scenarios I built (receipts 05). Three coverage findings routed to the L1 below. Lane bytes were never touched; scratch deleted.**

## 1. What was mutated, and the detector

Pristine bytes copied to scratch and hashed before any mutation; all mutants are scratch-only.

| Instrument | sha256 (mutated digest source) |
|---|---|
| `scripts/x_robots_tag_audit.py` (tool, L1-authored, worktree) | `f06c47b5cdd38bccf3dd1c0f381fbd560f6622bdf9d25443a02a2e2c23a24de8` (18053 B) |
| `.ufo/waves/round-79/c79_receipt_ledger.py` (counter) | `98b7c13729578c79b6ac2085576e2e61d425f818a0aec5c1449c27a59eb0a195` |
| `.ufo/waves/round-79/c79_xrt_matrix.py` (detector) | `84777a97e26cbfd990953d231337edca1bf37d68b4035a97b244bfdea54c8626` |
| `.ufo/waves/round-58/c58_receipt_rewrites.py` (frozen c58 import, copied unmodified) | `3f52040a8a6d7833975e9f8c98a6752692fd6f0cffd001a96b028283ae926c2d` |

Detector (verbatim, run from the lane root; identical for baseline and every mutant):

```
python3 -B .ufo/waves/round-79/c79_xrt_matrix.py --root <lane> \
  --tool <mutant> \
  --cases <lane>/.ufo/waves/round-79/cases \
  --expect <lane>/.ufo/waves/round-79/expect/expect.json \
  --consts <lane>/.ufo/waves/round-79/consts \
  --work <scratch>/work-<mutant>
```

Baseline (pristine scratch copy): `cases=31 decided=31 correct=31 wrong=0 undecided=0 constants_failed=4/4 selftest_ok=true cases_sha256=fd0a3bcc…9788af met=true`, exit 0 (receipt `receipts/01-tool-baseline.txt`). The `cases_sha256` is byte-identical in all 11 runs (`receipts/06-integrity.txt`), so every verdict below is attributable to the mutant alone.

## 2. Tool mutants — 10/10 killed by the frozen matrix

| # | Mutant (semantic change) | sha256 | Verdict | Killing evidence |
|---|---|---|---|---|
| m1 | bot scope does not persist across segments (`scope = None` after each rule) | `27adbede…bca8091` | **killed** | `WRONG c28 directives:c28:['nofollow']!=[]` — c28 `googlebot: noindex, nofollow` leaks the second rule into the global scope; met=false exit 1 |
| m2 | `none` removed from KNOWN/VALUELESS (treated as unknown) | `98134064…3aef2b1` | **killed** | `WRONG c03 exit:1!=0` — c03 `none` no longer expands to `noindex,nofollow`; met=false |
| m3 | `nosnippet` no longer suppresses `max-snippet:*`/`max-video-preview:*` in `effective` | `e7873170…0ad0b346` | **killed** | `WRONG c08 effective:c08:['max-snippet:50', 'nosnippet']!=['nosnippet']`; met=false |
| m4 | any non-empty `max-image-preview` value accepted | `5c35f6e5…9fa44d1c9` | **killed** | `WRONG c14 exit:0!=1` — c14 `max-image-preview:huge` accepted instead of `xrt_invalid_value`; met=false |
| m5 | header name compared case-sensitively | `ca4427d2…61cff0d7aa` | **killed** | 25 wrong cases (c01, c02, c03, c05, c06, c07, c08, c09, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c26, c27, c28, c29, c30); correct=6/31; met=false |
| m6 | empty segment no longer yields `xrt_empty_rule` | `9bab42e2…82147788` | **killed** | `WRONG c12 exit:0!=1` — c12 `noindex,,nofollow`; met=false |
| m7 | duplicate value-bearing directives no longer flagged | `b3296dce…727943ac4e97d` | **killed** | `WRONG c21 exit:0!=1` — c21 loses `xrt_duplicate_directive`; met=false |
| m8 | report exit always 0 (findings ignored) | `702a0ad6…2a7792c666` | **killed** | 10 wrong (c09, c10, c11, c12, c13, c14, c17, c18, c20, c21), all `exit:0!=1`; met=false |
| m9 | directive names matched case-sensitively (no `.lower()`) | `c975f49a…8d8a789` | **killed** | `WRONG c19 exit:1!=0` — c19 `NoIndex` becomes `xrt_unknown_directive`; met=false |
| m10 | duplicate caps collapse to **max** instead of min | `67af67ef…932cec410a89` | **killed** | `WRONG c21 effective:c21:['max-snippet:100']!=['max-snippet:50']`; met=false |

Every kill came from the case comparison, not from an accidental crash: all 11 runs decided 31/31 (no `undecided`), constants stayed 4/4, and the counter selftest stayed green (`selftest_ok=true`) — as expected, because the counter selftest tests the counter, not the tool under test. Receipts: `receipts/02-tool-mutants.txt`.

No survivor. No coverage gap on the tool side: for each of the nine grammar behaviours listed in contract §C2 grammar items 1–7 and exit item 9 there is at least one frozen case that kills the matching mutant (c03, c08, c12, c14, c19, c21, c28, c30, c09…c21 respectively).

## 3. Counter mutants — 2 killed by frozen fixtures, 3 survivors with routed coverage findings

Harness: per mutant, a scratch tree `cm/<mutant>/round-79/c79_receipt_ledger.py` next to an unmodified copy of `ctl_receipt_fixture.py`, with the frozen c58 counter copied to `cm/<mutant>/round-58/` (byte-identical, sha above). Baseline: the pristine harness reproduces the frozen `ctl-c1-fixtures.txt` receipt line-for-line (revision-masked), and the pristine counter reproduces `base-c1-receipt-ledger.txt` at `0898085` (`events=32 undisclosed=5 … met=false`, exit 1) and `c1-selftest.txt` (`15/15 passed`, exit 0) — receipts `receipts/03-counter-baseline.txt`. Note the fixture builder itself always exits 0; the verdicts are read from the printed `C1v2` lines against the frozen receipt.

| # | Mutant (semantic change) | sha256 | vs selftest | vs frozen fixture battery | Verdict |
|---|---|---|---|---|---|
| k1 | `undisclosed` conjunct dropped from `met` | `530a3307…87031d74` | 15/15 (blind, see F4) | **drop-one scenario flips** to `met=true exit=0` (must fail) | **killed** by frozen `drop-one` |
| k2 | round equality dropped from `round_rewritten()` (any round counts) | `0096d2e9…fbea84cf` | 15/15 (blind, see F4) | **correct scenario flips** to `round_rewritten=1 met=false exit=1` (able-to-pass) | **killed** by frozen `correct` scenario |
| k3 | `wrong_kind` zeroed in the measure accounting | `a01d8890…b04d5cf` | 15/15 | all 5 scenarios unchanged | **survived frozen battery + selftest** |
| k4 | `malformed` zeroed (accepts empty note) | `a659a6a3…d8c3915` | 15/15 | all 5 scenarios unchanged (cheap-note stays red only via `undisclosed=1`) | **survived frozen battery + selftest** |
| k5 | `symlinks` zeroed in the measure accounting | `d6160f70…cb476937` | 15/15 | all 5 scenarios unchanged | **survived frozen battery + selftest** |

### Kill evidence for the three survivors (scratch probe, not a frozen control)

`probe.py` (receipt `receipts/05-probe.txt`) builds one throwaway fixture repo with four states; S0 proves the probe can pass, S1–S3 isolate one conjunct each. Pristine vs mutant, same revision, `--round 79`:

- **S1 wrong-kind** (disclosed event, true blobs, `kind="append"` for a `content` change): pristine `wrong_kind=1 met=false exit=1`; **k3 `met=true exit=0`** → k3 killed here.
- **S2 isolated-malformed** (correct entry + duplicate entry with blank note): pristine `malformed=1 undisclosed=0 phantom=0 met=false exit=1`; **k4 `met=true exit=0`** → k4 killed here.
- **S3 symlink** (receipt replaced by a symlink at tip, rewrite disclosed with the true link blobs): pristine `symlinks=1 undisclosed=0 met=false exit=1`; **k5 `met=true exit=0`** → k5 killed here.

So the conjuncts are live code and the counter does fail when they fire — the gap is purely in the frozen detection surface.

## 4. Coverage findings for the L1 (route; no frozen byte was changed)

- **F1 — no frozen fixture pins `wrong_kind>0`.** The `fabricated` scenario cannot reach it (its blob mismatch phantom-fires first, `wrong_kind` stays 0). A mutant zeroing `wrong_kind` passes the whole frozen battery. Suggested scenario (probe S1): disclosed event with true blobs and a false byte-level `kind`.
- **F2 — `cheap-note` shadows `malformed`.** An empty-note entry is counted as both `undisclosed` and `malformed` (frozen receipt shows `undisclosed=1 malformed=1`), so dropping the `malformed` conjunct flips nothing. Suggested scenario (probe S2): a fully-disclosed state plus one extra structurally-faulted ledger entry (blank note) → sole red `malformed=1, undisclosed=0`.
- **F3 — no symlink scenario exists.** `symlinks` is in the frozen predicate but no fixture ever sets it. Suggested scenario (probe S3): receipt stored as a symlink at the measured tip (even fully disclosed) → `symlinks=1`.
- **F4 — c79 `--selftest` cannot catch `measure`/`round_rewritten` regressions (minor).** The selftest re-implements the predicate arithmetic and the `ROUND_PATH_RE`+round comparison inline instead of calling `round_rewritten()`/`measure()`, so all five mutants (including k2's real regression) passed `15/15`. The kills came from the fixture battery. If the battery gains F1–F3 scenarios, the selftest gap is tolerable; otherwise consider wiring the selftest through `round_rewritten()`.

## 5. Restoration and integrity evidence

- The committed/worktree tool and counters were never edited: post-session sha256 of all four lane artifacts equal the pre-session values (`receipts/06-integrity.txt`; tool still `f06c47b5…4de8`, counter `98b7c137…`, matrix `84777a97…`, c58 `3f52040a…`).
- `git status --porcelain -- .ufo/waves/round-79 .ufo/waves/round-58 scripts` shows **no tracked modification** — only untracked w1 report files (incl. this seat's `w1/MutC/`). No case, oracle, const, counter or contract byte changed; the mutation base was the scratch copy throughout.
- Scratch discipline: everything lived under `/fast/scratch/hyaku/kake-r79/MutC/` (including the fixture battery's `HYAKU_SCRATCH` redirect); receipts copied to `w1/MutC/receipts/` first, then the tree deleted (verified below).
- Tooling installs: none (pacman guard unaffected; no new tools needed).

## 6. Receipts

All under `.ufo/waves/round-79/w1/MutC/receipts/`: `01-tool-baseline.txt`, `02-tool-mutants.txt`, `03-counter-baseline.txt`, `04-counter-mutants.txt`, `05-probe.txt`, `06-integrity.txt`.
