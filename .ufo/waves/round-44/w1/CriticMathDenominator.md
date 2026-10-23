# CriticMathDenominator — independent C1 arithmetic review

Axes: **operability** (assigned: faithful control identities, witness attribution, and reproducible denominators). Freshness is the other lane axis, not assessed here. No round judgment is made.

## Findings

1. The manifest contains **27 distinct named control tools**, not 270 controls. Their hashes match the copied sources. There are **10 additional class runs per tool**, giving **21 generated-run keys** in v5 versus 11 in v4.
2. **Mapping defect: `buildport-m6`.** The TSV calls it `portdigit / G9`; its source and originating report describe an inverted **default-port branch**, so its source-derived attribution is **G2**, not a port-digits memo. G4 or another class can also catch the defect; a cross-class catch is not evidence that its mechanism became a G9 cache.
3. The requested before result is **not the result in the existing receipt**. `verification/freeze/control-v4blind.json` records **2/27 witnessed, 25/27 met, `ok: false`**. `buildscope-m5` differs on D; `repeat-depth-deep` differs on C. Both are stdout differences, not timing-only failures.
4. The driver as inspected does **not** audit the four r42 canaries or junk control. Its printed control denominator is the number of non-error manifest rows, normally 27, **not 32, 33, 270, or 567**. Its separate build denominator counts build scorings, not distinct builds.
5. `met: false` alone is weaker than a semantic witness: the driver currently counts timing failures and parsable cannot-evaluate receipts as witnessed too. A claimed semantic 27/27 needs actual unequal-run evidence; `ok=True` alone does not establish that or the expected class attribution.

## The 27 identities and required attribution

Prefixes: `c/` = `.ufo/waves/round-44/controls-r43/`; `r/` = `.ufo/waves/round-43/w1/`. Each source below was inspected directly, not inferred from its filename. All paths are relative to the lane root.

The final column is the requested **expected class → `caughtBy` key that must carry it**, source-derived **[INFERENCE]**, not a newly exercised v5 result. It means the named key must appear in that control's `caughtBy` array to demonstrate the intended class witness; additional unequal keys are allowed. Aggregate semantic witnessing may be demonstrated by a different genuine unequal run, but then that is cross-class attribution, not proof of the advertised mapping. `caughtBy` contains run keys such as `G2`, not family names or module filenames.

| # | Control | TSV family / class | Source mechanism and originating report | Expected class → required `caughtBy` key |
|---:|---|---|---|---|
| 1 | `portlen-v1` | portlen / G1 | `c/portlen-v1-skip-grammar-6plus.py:345`: admits failed grammar for ≥6-digit ports; `r/CtlPortLen.md:12,23,28` | G1 → `G1` |
| 2 | `portlen-v5` | portlen / G1 | `c/portlen-v5-abbrev-window-6plus.py:350-355`: judges first 64 cp on ≥6-digit ports; `r/CtlPortLen.md:14,25,29` | G1 → `G1` |
| 3 | `buildscheme-M5` | default_port / G2 | `c/buildscheme-M5-default-port-https80.py:303-304`: implicit HTTPS port becomes 80; `r/MutBuildScheme.md:17,21-24` | G2 → `G2` |
| 4 | `buildscope-m5` | empty_path / G3 | `c/buildscope-m5-empty-path.py:305`: removes empty-path `/` default; `r/MutBuildScope.md:18,25` | G3 → `G3` |
| 5 | `buildscope-m4` | port_scope / G4 | `c/buildscope-m4-port-dropped.py:510`: compares `parsed[:2]`, dropping port; `r/MutBuildScope.md:17,24` | G4 → `G4` |
| 6 | `headtail-V1` | prefix / G5 | `c/headtail-V1-prefix-cache64.py:293-301`: first-64-cp parse cache; `r/CtlHeadTail.md:8` | G5 → `G5` |
| 7 | `headtail-V2` | prefix / G5 | `c/headtail-V2-headtail-key48.py:294-305`: first48+last48 cache for values >96 cp; `r/CtlHeadTail.md:9` | G5 → `G5` |
| 8 | `headtail-V7` | prefix / G5 | `c/headtail-V7-prefix-cache45.py:294-302`: first-45-cp parse cache; `r/CtlHeadTail.md:13` | G5 → `G5` |
| 9 | `prefixcache-p48` | prefix / G5 | `c/prefixcache-p48-noreval.py:294-303`: first-48-cp parse cache, no tail revalidation; `r/CtlPrefixCache.md:26,35-38` | G5 → `G5` |
| 10 | `casememo-v3` | fold / G6 | `c/casememo-v3-validity-lower.py:221-230`: grammar-validity memo under `lower()`; `r/CtlCaseMemo.md:16,26-30` | G6 → `G6` |
| 11 | `casememo-v4` | fold / G6 | `c/casememo-v4-validity-lower-short.py:222-233`: same validity memo, gated to ≤64 cp; `r/CtlCaseMemo.md:17,26-30` | G6 → `G6` |
| 12 | `casememo-v7` | fold / G6 | `c/casememo-v7-value-lower-nonascii.py:320-332`: full-parse `lower()` memo consulted for non-ASCII; `r/CtlCaseMemo.md:20,31-34` | G6 → `G6` |
| 13 | `casememo-v8` | fold / G6 | `c/casememo-v8-value-casefold-nonascii.py:320-332`: non-ASCII full-parse `casefold()` memo; `r/CtlCaseMemo.md:21,31-34` | G6 → `G6` |
| 14 | `repeat-len-band` | band / G7 | `c/repeat-ctl_len_memo_band.py:223-234`: length memo, 6001–199999 cp; `r/CtlRepeat.md:28,48,105-106` | G7 → `G7` |
| 15 | `repeat-depth-band` | band / G7 | `c/repeat-ctl_depth_memo_band.py:223-234`: slash-count memo, ≥64 slashes and ≤1799 cp; `r/CtlRepeat.md:29,49,107-109` | G7 → `G7` |
| 16 | `repeat-defpos-band` | band / G7 | `c/repeat-ctl_defpos_memo_band.py:223-234`: `(length, first '%')` memo, first `%`≥1000 and length≤1799; `r/CtlRepeat.md:30,50,110-112` | G7 → `G7` |
| 17 | `repeat-depth-deep` | band / G7 | `c/repeat-ctl_depth_memo_deep.py:219-230`: slash-count memo, ≥64 slashes; `r/CtlRepeat.md:23,51,107-109` | G7 → `G7` |
| 18 | `repeat-defpos-late` | band / G7 | `c/repeat-ctl_defpos_memo_late.py:219-230`: `(length, first '%')` memo, first `%`≥1000; `r/CtlRepeat.md:24,52,110-112` | G7 → `G7` |
| 19 | `hosttable-A` | host / G8 | `c/hosttable-A-expanded46-fixed.py:366-373`: table hit returns fixed HTTPS/root tuple; `r/CtlHostTable.md:9,18` | G8 → `G8` |
| 20 | `hosttable-B` | host / G8 | `c/hosttable-B-expanded46-nogrammar.py:366-375`: table hit skips URI grammar; `r/CtlHostTable.md:10,19` | G8 → `G8` |
| 21 | `hosttable-F` | host / G8 | `c/hosttable-F-provable.py:351-358`: fixed tuple for provably off-generator host table; `r/CtlHostTable.md:11,20` | G8 → `G8` |
| 22 | `portvalue-digits` | portdigit / G9 | `c/portvalue-memo-digits.py:323-330`: parse memo keyed only on port digits; `r/CtlPortValue.md:12,18` | G9 → `G9` |
| 23 | `portvalue-digits-67` | portdigit / G9 | `c/portvalue-memo-digits-67.py:323-330`: same digits-only memo, 6–7 digits; `r/CtlPortValue.md:11,17` | G9 → `G9` |
| 24 | `portlen-v4` | portdigit / G9 | `c/portlen-v4-cache-portlen.py:345-363`: key preserves scheme/host/tail but only port digit count; `r/CtlPortLen.md:13,24,30` | G9 → `G9` |
| 25 | **`buildport-m6`** | **portdigit / G9** | `c/buildport-m6-default-branch.py:303-304`: inverted default-port branch, no memo; `r/MutBuildPort.md:20,24-29` | **G2 → `G2` — mapping defect** |
| 26 | `headtail-V4` | window / G10 | `c/headtail-V4-longport-head64.py:293-297`: long-port values truncated to head64; `r/CtlHeadTail.md:11` | G10 → `G10` |
| 27 | `headtail-V8` | window / G10 | `c/headtail-V8-longport-tail64.py:293-297`: long-port values truncated to tail64; `r/CtlHeadTail.md:14` | G10 → `G10` |

TSV family/class counts, in G1…G10 order: **2 + 1 + 1 + 1 + 4 + 4 + 5 + 3 + 4 + 2 = 27**. Source-corrected counts: **2 + 2 + 1 + 1 + 4 + 4 + 5 + 3 + 3 + 2 = 27**.

Independent report-origin cross-sum: CtlPortLen 3 + MutBuildScheme 1 + MutBuildScope 2 + CtlHeadTail 5 + CtlPrefixCache 1 + CtlCaseMemo 4 + CtlRepeat 5 + CtlHostTable 3 + CtlPortValue 2 + MutBuildPort 1 = **27**.

`headtail-V2` is **not** a second mapping defect: `classes/g5_prefix_cut_45plus.py:38-47` explicitly constructs pairs sharing both first48 and last48 while changing the middle. `classes/g2_default_port.py:13-22` constructs explicit-default-port sitemap URLs with implicit-port locs, the source-derived witness for `buildport-m6`. The source leaves implicit ports `None` and replaces explicit ports with 80/443; the reference normalizes the implicit default too. For example, the originating report's `http://example.com:80/a` under `http://example.com/sitemap.xml` changes from clean to out-of-scope.

This is the **named 27-tool cohort**, not an exhaustive census of every escape in every r43 report. No tools were added, removed, relabelled after scoring, or edited by this review.

## Four r42 canaries, junk, and held build

The r44 `control-v4blind.json` has only the 27 rows and no canary section. The required fallback is grounded in `SCORECARD.md:3225-3229` and the actual r43 frozen receipts below. These are historical **v4** results, not new v5 evidence.

| Tool under `.ufo/waves/round-43/controls-r42/` | Frozen receipt basename | Historical equality / unequal keys | Exit |
|---|---|---|---:|
| `M8-port-five-digits.py` | `r42ctl-M8-port-five-digits.json` | 9/11; `F`, `T3` | 1 |
| `v1_casefold.py` | `r42ctl-v1_casefold.json` | 9/11; `F`, `T2` | 1 |
| `v2_prefix32.py` | `r42ctl-v2_prefix32.json` | 7/11; `E`, `F`, `T2`, `T3` | 1 |
| `v4_hosttable.py` | `r42ctl-v4_hosttable.json` | 9/11; `F`, `T3` | 1 |

All four have `met: false`, `note: null`. Exit values are corroborated by `.ufo/waves/round-43/verification/freeze/exits.annotated.txt:1-8`.

Separate junk control: **`junk_constant.py`**, frozen receipt `r42ctl-junk_constant.json`: `met: false`, equality **0/11**, unequal keys `A,B,C,D,E,F,T1,T2,T3,T4,T5`, exit **1**.

Held build: **one** tool, `scripts/sitemap_audit.py` at `020bc4574729ed674299f6cab02faac1582d9464`, declared sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`; **three independent scorings**, not three builds. The identity is recorded by the task and the originating reports; I did not re-extract it or re-score it.

Arithmetic:

- Named r43 cohort: **27** tools, the audit numerator/denominator population.
- Red calibration tools outside that cohort: **4 + 1 = 5**. All negative tools together: **32**, not the audit's 27.
- Distinct tools including the held build: **33** (excluding reference/timing-baseline tools).
- Each v4 counter receipt: `A…F` + `T1…T5` = **11** run keys. Each v5 receipt: those 11 + `G1…G10` = **21**. Timing repetitions do not add run keys.
- Named-cohort v5 comparison records: **27 × 21 = 567**, including **27 × 10 = 270** new class-run records. Neither number is a control denominator.
- If the five separate calibrations each run once and the build runs three times under v5: **35 counter invocations** and **735 run records**, still 27 primary controls and 3 build scorings. This is arithmetic, not an exercised audit.

The audit's `total` is explicitly `len([r for r in results if not r.get("error")])` (`c44_audit.py:133`). A missing/hash-mismatched tool therefore shrinks the printed denominator, although `total == len(rows)` and the error check correctly prevent `ok=True` in that situation. The driver does not assert `len(rows)==27`; the input manifest supplies that population. `--build-runs 3` supplies the required build denominator; the code can otherwise accept a different positive build-run count.

## Two exact required summary lines

These are **expected strings derived from the inspected print format, not observed stdout**. Use the default label (omit `--label`), the inspected counter hash, the 27-row manifest, no build argument before, and the held revision with `--build-runs 3` after:

```text
AUDIT kake-r44 classes=v4 witnessed=0/27 build_met=0/0 ok=True counter=5cedaa3b9f91
AUDIT kake-r44 classes=v5 witnessed=27/27 build_met=3/3 ok=True counter=5cedaa3b9f91
```

Required exits: **0 before; 0 after**. “27/27 blind” is represented by **`witnessed=0/27`**, not by a printed `blind=27/27` field. A supplied label changes only the label token.

To substantiate the requested interpretation, before needs all 27 `met:true`, counter exit 0, `caughtBy:[]`, equality 11/11 and no errors. After needs 27 genuine semantic witnesses (counter exit 1, at least one unequal generated run per tool, with the intended attribution above), plus three held-build receipts with `met:true`, counter exit 0, equality **21/21**, all timing ratios within the predicate, and independent seeds. The four canaries and junk must remain red separately. The two summary lines alone do not certify those separate calibrations.

## Strongest local counterexample: the before receipt

`read` of `.ufo/waves/round-44/verification/freeze/control-v4blind.json` with query `{label,classesMode,expect,counterSha256,controls,witnessed,witnessedNames,witnessedByClass,metCount:(.metNames|length),errors,build,ok,verdict,rowCount:(.rows|length)}` returned, verbatim:

```json
{
  "label": "round44-control-v4blind",
  "classesMode": "v4",
  "expect": "blind",
  "counterSha256": "5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc",
  "controls": 27,
  "witnessed": 2,
  "witnessedNames": [
    "buildscope-m5",
    "repeat-depth-deep"
  ],
  "witnessedByClass": {
    "buildscope-m5": [
      "D"
    ],
    "repeat-depth-deep": [
      "C"
    ]
  },
  "metCount": 25,
  "errors": [],
  "build": [],
  "ok": false,
  "verdict": "witnessed 2/27",
  "rowCount": 27
}
```

Decisive per-tool receipt fields, verbatim from the reader's JSON projections:

```json
"seed": 181346457990762,
"met": false,
"equalRuns": "10/11",
"caughtBy": [
  "D"
],
"D": {
  "values": 2000,
  "ref41Exit": 2,
  "ref41OutSha256": "7bdf3ebd80c57e7e08a32dbeb7db07d4f0e3ba7cfc090e26fd061918c862f99a",
  "candExit": 2,
  "candOutSha256": "3406aa7462b7a76d02effa25f2ccc926fb87f010cfcf3675e70d2cefae2ee566",
  "equal": false
}
```

```json
"seed": 5994504518804,
"met": false,
"equalRuns": "10/11",
"caughtBy": [
  "C"
],
"C": {
  "values": 656,
  "ref41Exit": 2,
  "ref41OutSha256": "665f50f04fa3c6db17b8e7f3f3aadec2c00f4967006e88cf5cddac8b91eabcca",
  "candExit": 2,
  "candOutSha256": "8b0791818af0feba0381ca80567700a48b9c481714d16ee0e5deb5bd62ffdbd1",
  "equal": false
}
```

Both summary rows have counter exit **1**. Exit 2 inside a generated run is the *tested tool's* manifest result, not a counter cannot-evaluate exit; equal exit codes with unequal stdout hashes are semantic witnesses. These records cannot be dismissed as timing noise.

The existing label/receipt would reconstruct the following line **[INFERENCE; stdout not rerun]**, with driver exit 1:

```text
AUDIT round44-control-v4blind classes=v4 witnessed=2/27 build_met=0/0 ok=False counter=5cedaa3b9f91
```

Historical r43 met receipts and fresh r44 blindness are different propositions. No resampling or reinterpretation in this review turns this failed before receipt into the requested all-blind result.

## Fixable defects versus evidence limits; smallest safe correction

- **Fixable mapping:** before freeze, the owner can classify `buildport-m6` as `default_port / G2`, retaining the same source bytes, hash, name, and total 27. Keep cross-class catches visible rather than requiring all catches to equal the label. Do not describe a G2/G4 scope witness as acquired port-digit-cache coverage.
- **Fixable witness accounting:** distinguish semantic inequality from timing failure and cannot-evaluate. A witnessed row needs valid, error-free counter evidence and an actual `runs[key].equal == false`; `met:false` alone is insufficient. `c44_audit.py:96-107,113-118` currently uses the latter, while `c44_count_v5.py:1111-1118` shows timing failure or cannot-evaluate can leave `met:false`. This is a static control-flow finding, not a runtime reproduction.
- **Fixable denominator presentation:** retain the fixed 27 listed identities and report evaluated/error counts separately. Keep canaries/junk as a separate 5-tool calibration population so the before `blind` check does not accidentally include tools required to be red. Require three build scorings for this claim, not just a positive count.
- **Not repairable by arithmetic:** the two already-recorded v4 semantic witnesses contradict the requested fresh before line. Preserve them; distinguish 25 currently blind tools from two already witnessed, and let the owner/canonical judge resolve any pre-freeze claim/evidence alignment. Do not drop controls or cherry-pick a replacement baseline to conceal the counterexample. No acceptance judgment is made here.

## Commands, inspection evidence, writes, and limits

Shell commands actually run, in `/home/vgpnk/Projects/shokunin/kake-shokunin`:

```sh
mkdir -p /fast/scratch/hyaku/kake-r44/CriticMathDenominator
```

Output: none.

```sh
sha256sum .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/controls-27.tsv .ufo/waves/round-44/controls-r43/*.py
```

Output, trimmed to the counting pins and mapping-defect control (the other 26 source hashes also matched their displayed TSV entries):

```text
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
e88a0309825ef0e62e0dd64a41d1c66fdea27db29436c7b2fd200a1d6aa6e689  .ufo/waves/round-44/c44_audit.py
233afa37d6ce85b0cbbedba8fe941de25f96d13773d3d388d68cbd9ab182eb57  .ufo/waves/round-44/controls-27.tsv
68f3750025531d7815d6ec665432536abc3b0c78a036fdb49339e1f73bcbe87e  .ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py
```

Static tools used: `read` of `skill://godspeed`; manifest `:1-90`; audit driver `:1-260`; counter `:76-110` and `:975-1125`; the ten originating reports and the source blocks cited in the table; G2 `:1-180`, G5 `:1-200`; SCORECARD `:3192-3231` and `:3293-3347`; existing r44 summary and its two failing per-tool receipts; five r43 calibration receipts; `exits.annotated.txt:1-75`. Direct source evidence for the mapping defect returned:

```text
303:    if port is not None:
304:        port = 80 if scheme == "http" else 443
```

Exact JSON projection used for each of the five r43 calibration receipts:

```text
?q={label,toolFile,toolSha256,seed,met,equalRuns,caughtBy:[.runs|to_entries[]|select(.value.equal==false)|.key],note}
```

Exact JSON projections for the two failing r44 receipts:

```text
tools/buildscope-m5.json?q={classesMode,toolSha256,seed,met,equalRuns,caughtBy:[.runs|to_entries[]|select(.value.equal==false)|.key],D:.runs.D,note}
tools/repeat-depth-deep.json?q={classesMode,toolSha256,seed,met,equalRuns,caughtBy:[.runs|to_entries[]|select(.value.equal==false)|.key],C:.runs.C,note}
```

Source-search `grep` patterns, run through the specialized tool, not a shell:

```text
cache|memo|CACHE|MEMO|len\(.*port|port.*len\(|path = parts.path|parsed\[:|if port is|else 80|else 443|_parse_url|_uri_ok|return value
cache|memo|CACHE|MEMO|len\(value\)|\[:64\]|\[:48\]|\[:45\]|\[-64:|\[-48:|casefold|lower\(|def _parse_url|def _uri_ok|_NONASCII|ord\(
cache|memo|CACHE|MEMO|6001|199999|1799|1000|>= 64|>=64|def _parse_url|def _uri_ok|_HOST|hosts|wikipedia|if host|host in
```

These searched, respectively, `c/{portlen-*,portvalue-*,build*}.py`, `c/{headtail-*,casememo-*,prefixcache-*}.py`, and `c/{repeat-*,hosttable-*}.py` (individual semicolon-separated tool paths). Decisive results are the source expressions and line references in the 27-row table. A broad SCORECARD search was truncated; the relevant canary and r43 tally sections were then read by exact ranges.

During the concurrent build, direct reads of the registry-named `classes/g1_longport_grammar.py`, `classes/g9_port_digits.py`, and `classes/g10_headtail_windows.py` returned `Path '…' not found`. They were not needed to derive the source-based expectation table; this is a snapshot observation, not a claim about the eventual delivered class files.

Written: **only this report**, `.ufo/waves/round-44/w1/CriticMathDenominator.md`; created the assigned scratch directory, with no scratch files. No source, manifest, receipt, frozen artifact, history, route, or sibling-lane file was modified. No subagents dispatched; no git/jj commands; no installs/updates; no tests, probes, audit executions, full counters, or alternative runtime invoked. Expected output above is explicitly unrun.

Blocker to the requested before evidence: the existing receipt is 2/27 witnessed, not 0/27. No blocker to completing this static arithmetic review. Actual after witnessing, fresh canary results, and build 3/3 remain unexercised by this seat; this report does not assert them.
