# CtlRepeat — round-43 wave-1 (counter v4 vs fresh repetition classes)

**MET** — five of twelve controls met the C1 predicate under counter v4
(`c43_count_v4.py`, sha256 `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab`, frozen at
`b49cba9`).  Counter v4 catches the three fresh repetition classes (value-length memo,
dir-depth cache, defect-position cache) when the skip is applied across the whole value
space, but is **blind to the same classes when the skip is confined to a band the counter's
corpus never generates** (equality 11/11, ratios ≤ 1.35, met=true, stable over 2–5
independent os.urandom seeds).  Per the round's frozen kill rule (1) ("any live-seat control
receipt meeting v4 means C1 is NOT MET"), the counter is too weak to certify the build against
these classes.

## Controls built and scored (all derived from the fast build `020bc457…`, sha256
`914ebdee…`; each adds one skip — a process-global memo over `_uri_ok`, keyed on a
repetition class outside the frozen list; each is a genuine behaviour skip with a witness)

| tool | key | guard | skip |
|---|---|---|---|
| `ctl_len_memo` | len(value) | always | value-length memo |
| `ctl_depth_memo` | value.count('/') | always | dir-depth cache |
| `ctl_defpos_memo` | (len, first '%') | always | defect-position cache |
| `ctl_len_memo_long` | len(value) | len ≥ 4096 | length memo, natural heuristic |
| `ctl_depth_memo_deep` | count('/') | depth ≥ 64 | depth memo, natural heuristic |
| `ctl_defpos_memo_late` | (len, first '%') | first '%' ≥ 1000 | defect-position memo, natural heuristic |
| `ctl_len_memo_mid` | len(value) | 1000 ≤ len ≤ 4095 | length memo, mid band |
| `ctl_depth_memo_mid` | count('/') | 8 ≤ depth ≤ 63 | depth memo, mid band |
| `ctl_defpos_memo_mid` | (len, first '%') | 0 ≤ first '%' ≤ 999 | defect-position memo, mid band |
| `ctl_len_memo_band` | len(value) | 6001 ≤ len ≤ 199999 | length memo, corpus-absent band |
| `ctl_depth_memo_band` | count('/') | depth ≥ 64 and len ≤ 1799 | depth memo, corpus-absent band |
| `ctl_defpos_memo_band` | (len, first '%') | first '%' ≥ 1000 and len ≤ 1799 | defect-position memo, corpus-absent band |

sha256 (tools): ctl_len_memo `1eed3014…`, ctl_depth_memo `6fe67fea…`, ctl_defpos_memo
`95f52f8a…`, ctl_len_memo_long `f6b3bbad…`, ctl_depth_memo_deep `7eb373f2…`,
ctl_defpos_memo_late `9d49f8c8…`, ctl_len_memo_mid `a2d1a384…`, ctl_depth_memo_mid
`7cdec1cc…`, ctl_defpos_memo_mid `1df393e1…`, ctl_len_memo_band `c3a8770e…`,
ctl_depth_memo_band `abf4984a…`, ctl_defpos_memo_band `b9c7eda6…`.

All receipts: `/fast/scratch/hyaku/kake-r43/CtlRepeat/receipts/*.json`; scoring command per
round (`timeout 900 prlimit --as=8000000000 -- python3 -B c43_count_v4.py --root <repo>
--tool-file <tool> --label CtlRepeat-<suffix> --out <receipt>`, no `--seed`).

## Receipts (seed; equalRuns; ratios T1/T2/T3/T4/T5; met; which run caught it)

Meeting (met=true, 11/11 equal, all ratios ≤ 1.35):

| tool | seeds | met |
|---|---|---|
| `ctl_len_memo_band` | 118348663684194, 180377758793319 | true, true |
| `ctl_depth_memo_band` | 8241544000919, 102742830749208 | true, true |
| `ctl_defpos_memo_band` | 26853201231934, 138732775952067 | true, true |
| `ctl_depth_memo_deep` | 265228268634935, 75535296645022, 166548730620687, 149485501928976, 106282657268816 | true ×5 |
| `ctl_defpos_memo_late` | 199088683903274, 27383583814723, 20742093587065, 197825956887710, 51836978993564 | true ×5 |

Caught (met=false):

| tool | equalRuns | caught by |
|---|---|---|
| `ctl_len_memo` | 1/11 | A,B,C,D,E,F,T1,T2,T3,T5 |
| `ctl_depth_memo` | 1/11 | A,B,C,D,E,F,T1,T2,T3,T5 |
| `ctl_defpos_memo` | 3/11 | A,B,C,D,E,F,T2,T5 |
| `ctl_len_memo_long` | 9/11 | C, T5 |
| `ctl_len_memo_mid` | 8/11 | C, T1, T2 |
| `ctl_depth_memo_mid` | 8/11 | C, T2, T3 |
| `ctl_defpos_memo_mid` | 1/11 | A,B,C,D,E,F,T1,T2,T3,T5 |

## Measurement of the blind spot (local replay, seed 4242, instrumented memo)

For every tool, the counter's generators were replayed and the memo instrumented to count:
`active` = values entering the memo, `keys` = distinct memo keys, `hits` = key collisions,
`wrong` = hits where the cached verdict differs from the true verdict.

| tool | active | keys | hits | wrong |
|---|---|---|---|---|
| ctl_len_memo | 122445 | 935 | 121510 | 21266 |
| ctl_depth_memo | 125899 | 113 | 125786 | 19149 |
| ctl_defpos_memo | 123152 | 14339 | 108813 | 19612 |
| ctl_len_memo_long | 83 | 24 | 59 | 10 |
| ctl_depth_memo_deep | 8 | 8 | 0 | 0 |
| ctl_defpos_memo_late | 0 | 0 | 0 | 0 |
| ctl_len_memo_mid | 21621 | 355 | 21266 | 1844 |
| ctl_depth_memo_mid | 6258 | 67 | 6191 | 182 |
| ctl_defpos_memo_mid | 58543 | 14182 | 44361 | 9789 |
| ctl_len_memo_band | 3 | 3 | 0 | 0 |
| ctl_depth_memo_band | 0 | 0 | 0 | 0 |
| ctl_defpos_memo_band | 0 | 0 | 0 | 0 |

Interpretation: the counter's corpus *does* exercise the three classes in the ranges it
generates (the unrestricted and mid-band memos are heavily exercised and caught).  The
meeting controls are blind only because the counter's corpus never generates a value in the
guard band at all (`ctl_depth_memo_band`, `ctl_defpos_memo_band`, `ctl_defpos_memo_late`:
active=0), or generates too few to produce a key collision with a different verdict
(`ctl_len_memo_band`: 3 values, distinct keys; `ctl_depth_memo_deep`: 8 values, distinct
keys).

## Witnesses (each meeting tool judges a value differently from the round-41 tool)

CLI witness manifests under `/fast/scratch/hyaku/kake-r43/CtlRepeat/witness/`, each with a
sitemap file whose first `<loc>` is valid and whose second `<loc>` carries the same memo key
but contains a space (so the round-41 tool emits `loc_not_absolute` while the control reuses
the first value's verdict and emits `loc_out_of_scope`).

`python3 -B <tool> --manifest <case>/manifest.json` vs the round-41 tool
(`ref41.py`, sha256 `50287ac6…`, i.e. the counter's pinned REF41):

- `ctl_len_memo_band`: first loc 6999 cp valid, second same length with space at 5000 →
  ref41 `loc_not_absolute` entry 2; control `loc_out_of_scope` entry 2.  stdout differs.
- `ctl_depth_memo_band` / `ctl_depth_memo_deep`: first loc 72 slashes valid, second same
  slash count with a space → ref41 `loc_not_absolute` entry 2; control `loc_out_of_scope`
  entry 2.  stdout differs.
- `ctl_defpos_memo_band` / `ctl_defpos_memo_late`: first loc 1722 cp, first '%' at 1219,
  valid; second identical length and first-'%' index with a space → ref41
  `loc_not_absolute` entry 2; control `loc_out_of_scope` entry 2.  stdout differs.

(`_parse_url` witnesses in `witness.json` — for each meeting tool the control returns a
parsed URL where ref41 returns None, or vice versa.)

## Findings (path:line)

- `.ufo/waves/round-43/c43_count_v4.py:239-249` (run F `cases_f`) and the timing shapes
  exercise the *frozen* repetition classes (case-fold pairs, prefix pairs, repeated-host
  blocks, common-host values, 6+-digit ports), but not value-length / dir-depth /
  defect-position collisions in the bands above.  The corpus's value distribution never
  pairs two same-key values with different verdicts in those bands, so the memos are
  invisible.  Holds as measured (wrong=0 for the five meeting tools).
- `.ufo/waves/round-43/c43_count_v4.py:606-627` (main loop) — equality runs A–F + T1–T5
  compare stdout bytes; a skip that never fires on the corpus is not observable.  This
  makes the five band/heuristic controls meet the predicate as worded.
- The unrestricted memos are caught (1/11, 1/11, 3/11) — so v4 does cover the three classes
  where the corpus exercises them.  The class gap is corpus-coverage, not judgment-class
  exclusion.

## Per-statement verdicts

- "any live-seat control receipt meeting v4 means C1 is NOT MET" — **holds**: five controls
  met v4; per the frozen kill rule (1), C1 is NOT MET.
- "the counter generates every repetition class of the new list" — **overstated**: the
  generated corpus exercises the classes only in the ranges it samples; band-limited skips
  escape.
- "the build keeps the round-41 tool's judgments on every generated run" — **holds** for
  the build itself (base == ref41 replay, 0 differences on all 11 runs at seed 4242); the
  finding is about the counter's blindness to the band-limited controls, not the build.

## Risks / boundary

- The meeting controls are not do-nothing/junk/constant: they do the real work on corpus
  values and only skip the grammar check in the guard band.  But they are genuine unsound
  skips (witnesses above), so the kill rule (1) applies.
- Seed stability checked: `ctl_depth_memo_deep` and `ctl_defpos_memo_late` met on 5
  independent seeds; the band controls on 2 each.  No meeting receipt flipped within the
  seeds scored.
- No tool was installed or upgraded; no repo files other than this report were written; no
  network use; no git/jj mutations; all processes killed.

## Reproduce

```
cd /fast/scratch/hyaku/kake-r43/CtlRepeat
python3 -B build_variants.py && python3 -B build_variants2.py && python3 -B build_variants3.py
bash score.sh ctl_len_memo_band len_memo_band   # … per tool, receipts in receipts/
python3 -B replay.py 4242 tools/<tool>.py /tmp/ctlr.json   # exposure measurement
python3 -B cli_witness.py                                  # CLI witnesses
```
