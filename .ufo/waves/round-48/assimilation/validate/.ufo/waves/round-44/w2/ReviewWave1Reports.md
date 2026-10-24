# ReviewWave1Reports — wave-2 sample review of six wave-1 reports

Axes: **operability** (do the load-bearing claims of wave-1 reports hold?) and **freshness** (do pasted outputs match current repo bytes?).

Method: for each of the six `.ufo/waves/round-44/w1/` reports I picked its load-bearing claim and re-ran one decisive pasted command (probe / sha256 / extraction script / wc), from `/home/vgpnk/Projects/shokunin/kake-shokunin`. Tool installs: none.

## Verdicts (0 fabrication defects found)

| Report | Load-bearing claim | Repro result |
|---|---|---|
| ExecG6Fold.md | G6 fold pairs do NOT witness casememo controls (all probes equal) | **PASS** — byte-identical JSON |
| ExecG1LongPort.md | G1 witnesses portlen-v1 (probe exit 1, unequal hashes) | **PASS** — byte-identical JSON, exit 1 |
| CriticClaimC1.md | Existing v4-blind receipt records witnessed 2/27, ok=false, two differing-hash divergences | **PASS** — receipt lines reproduce verbatim; one paste drifted (see drift section) |
| CriticMathDenominator.md | Counter/TSV/control sha pins; buildport-m6 is a default-port branch control | **PASS on counter + buildport-m6 pins**; audit/TSV pins drifted post-write (see drift section) |
| ScribeSources.md | Three Gate quotes carry wc -w 6/8/10 and exist in the cited sources | **PASS** — counts and all three source hits confirmed |
| RevengerControls.md | G5 witnesses headtail-V2 (seed 101, exit 1); three control hashes equal TSV pins | **PASS** — probe and all three pins reproduce |

## 1. ExecG6Fold — re-ran probe

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ReviewWave1Reports python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v3-validity-lower.py --seed 44; echo "EXIT=$?"
```

Observed (decisive fields, verbatim): `"units": 100, "values": 200, "ref41Exit": 0, "candExit": 0, "ref41OutSha256": "2f578c004a67e6dd1a21703a08ec43b682b5909093e5e9ff315176f77b2ede39", "candOutSha256": "2f578c00…(same)", "equal": true`, `EXIT=0`. Identical to the paste (`2f578c00…` both sides, equal true). Fold one-liner `python3 -c "print('\u212a'.lower(), '\u212a'.casefold(), '\u017f'.casefold())"` → `k k s` (matches paste). Named attack ("no fold witness exists for casememo-v3") **confirmed against current bytes** — also true of the post-20:09 edited `classes/g6_fold_pairs.py` (sha `f4f13a76…`), which still returns equal=true on this seed.

## 2. ExecG1LongPort — re-ran probe

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ReviewWave1Reports python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G1 --tool-file .ufo/waves/round-44/controls-r43/portlen-v1-skip-grammar-6plus.py --seed 44001; echo "EXIT=$?"
```

Observed verbatim: `"units": 299, "values": 300, "ref41Exit": 2, "candExit": 1, "ref41OutSha256": "0002484a4b4deb14185086d3106119bba5b109621e6d82ac324d20559b36a787", "candOutSha256": "b33422606cdadef5d1ed904e7d10e27fa42ab0fd03de3b4334cc155e105d4cde", "equal": false`, `EXIT=1` (witness). Byte-identical to the pasted first JSON block. Named attack (G1 witnesses portlen controls) **confirmed**.

## 3. CriticClaimC1 — re-ran its pasted extraction script

```sh
python3 -B /fast/scratch/hyaku/kake-r44/CriticClaimC1/review_evidence.py
```

Load-bearing lines reproduced **verbatim** (side-by-side identical): `MANIFEST rows=27 unique_names=27 unique_sha256=27 sha_mismatches=[]`; `CLOSURE_TALLY missing=[] extra=[]`; `EXISTING_SKIP_WORK {…"controls": 27, "counterSha256": "5cedaa3b…7672bc", "ok": false, "witnessed": 2}`; both `EXISTING_SKIP_ROW` (seeds `181346457990762` / `5994504518804`, caughtBy `["D"]` / `["C"]`) and both `EXISTING_DIVERGENCE` blocks (`3406aa74…` vs `7bdf3ebd…`, `8b079181…` vs `665f50f0…`). Its 2/27-witnessed falsifier **stands**.

Two non-load-bearing deltas vs the paste, both caused by post-write edits of the named artifacts, not by the critic:
- `CLASSES` line: pasted `"G2": 1, … "G9": 4`; now `"G2": 2, … "G9": 3` — the 20:40:59 TSV relabel of `buildport-m6` portdigit/G9 → default_port/G2 (exactly the mapping defect this critic reported).
- Trailing audit-exec step now fails differently: pasted `SyntaxError: CUT 61.=171` during a concurrent edit; now `KeyError: 'class'` at `c44_audit.py:217` — again because `c44_audit.py` changed at 20:40:04. The receipt-derived lines above printed before the crash.

## 4. CriticMathDenominator — re-ran its pasted sha256sum (4 of the pinned files)

```sh
sha256sum .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/controls-27.tsv .ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py
```

Side by side:

| File | Pasted | Now |
|---|---|---|
| `c44_count_v5.py` | `5cedaa3b9f91…7672bc` | `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc` — MATCH |
| `c44_audit.py` | `e88a0309825e…6e689` | `8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75` — DRIFT |
| `controls-27.tsv` | `233afa37d6ce…2eb57` | `a1f0e364dad5ff937666966a16622e6895591a2eb3db714d6ecf3f3948c31bf8` — DRIFT |
| `buildport-m6-default-branch.py` | `68f375002553…be87e` | `68f3750025531d7815d6ec665432536abc3b0c78a036fdb49339e1f73bcbe87e` — MATCH |

**Not fabrication**: all six w1 reports have mtimes 20:11:06–20:12:54; `c44_audit.py` mtime 20:40:04, `controls-27.tsv` mtime 20:40:59 — both edited ~28 min after the reports. The TSV diff is exactly the demanded `buildport-m6` relabel (`default_port G2` in the current TSV, sha `68f37500…` unchanged). The critic's paste was true at write time. But note: both files are on the round's frozen list, so the freeze boundary moved under pasted evidence — any tally/receipt citing `counter=…` plus audit/TSV identity must be re-pinned to final bytes.

## 5. ScribeSources — re-ran pasted wc and grepped the cited sources

```sh
printf '%s\n' 'The do-nothing shortcut never reaches predicate_pass=true' | wc -w; printf '%s\n' 'every pinned sha256 verifies over the committed blob' | wc -w; printf '%s\n' 'records a calibration error present when the statement was written' | wc -w
```

Observed: `6` / `8` / `10` — matches the paste exactly.

Quote existence in the cited sources (grep, all three hit): quote 1 in `corpus/SOURCES.md:137` (S129 row) and originally `tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md`; quote 2 in `tameshi-shokunin/.ufo/waves/round-33/w1/ReviewFreeze.md:5` ("**CONFORMANT.** … every pinned sha256 verifies over the committed blob, …"); quote 3 in `kama-shokunin/corpus/knowledge/self-assessment-at-writing.md:7` ("A mismatch therefore records a calibration error present when the statement was written"). Named attack (fabricated/miscounted quotes) **not sustained**.

## 6. RevengerControls — re-ran probe and pasted sha256sum of the three controls

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ReviewWave1Reports python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/headtail-V2-headtail-key48.py --seed 101; echo "EXIT=$?"
```

Observed verbatim: `"units": 100, "values": 200, "ref41Exit": 1, "candExit": 1, "ref41OutSha256": "b17870cbf918faf48414cfa53fc3cf6df2414d790052ff281f8a019507f6d130", "candOutSha256": "cd747e64872aa8b0571bdc6dfd2a7ad26492f9c92f9d1469dd00b6a8c08021ce", "equal": false`, `EXIT=1`. Matches the pasted prefixes (`b17870cb…` vs `cd747e64…`, exit 1). Control pins all match TSV and report: `headtail-V2…c10bf` = `012527ff78763caf8e20bc244cf5c7d899436e026c06fb4e9e43809f700c10bf`; `portvalue-memo-digits` `d09ad5fe…b00d` = `d09ad5fec5c9493f3c206ab1b1a33acf5e6ece344fe0e988a99bfa8749dab00d`; `repeat-ctl_defpos_memo_band` `b9c7eda6…55c0e` = `b9c7eda690cf0566c8a6f37e1b1472a16324bbfe86213a9556c68b5264c55c0e`. Named attack (G5 witness on headtail-V2) **confirmed**.

## Residual risk / unrun checks

- One decisive paste per report was re-run; the remainder were not re-executed: ExecG6Fold's other 7 probes (seed 440, v4/v7/v8), ExecG1LongPort's five other probe outputs and its benchmark control, RevengerControls' scratch fixtures (`caseA`/`caseB`, `diffcheck.py`), CriticClaimC1's `classifier_evidence.py`/`population_evidence.py` outputs, CriticMathDenominator's 26 remaining control hashes. No contradiction surfaced in any sampled paste.
- `c44_audit.py` and `controls-27.tsv` changed at 20:40 after being pasted into w1 evidence (three audit identities observed today: `aed7d771…` → `e88a0309…` → `8ee2c8bf…`). Current `c44_audit.py` also crashes `review_evidence.py`'s AST step (`KeyError: 'class'`, line 217). The L1 should re-pin final audit/TSV hashes in any receipt-bound summary before scoring.
- Current G6 module (post-20:09 edit) still does not witness casememo-v3 on seed 44 — consistent with the open build item.

## Files written

- `.ufo/waves/round-44/w2/ReviewWave1Reports.md` (this report)
- Scratch dir `/fast/scratch/hyaku/kake-r44/ReviewWave1Reports/` created (probe TMPDIR only; no persistent files)

No other lane file read or written; no installs; no git/jj commands.
