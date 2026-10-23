# ScoutBandFamily — repetition-band witnesses

Axes: operability (a semantic stdout/exit divergence, not a timing artifact) and freshness (quoted lines and stdout are from this run).

No tools installed. PACMAN was not used.

## Reference

`REF41_REV` in `.ufo/waves/round-44/c44_count_v5.py` is `1ef7a0e95f6884dd113fe583a997c633fe330ddd`.

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 1ef7a0e95f6884dd113fe583a997c633fe330ddd:scripts/sitemap_audit.py
```

Bytes written to `/fast/scratch/hyaku/kake-r44/ScoutBandFamily/tools/ref41.py` (15061 bytes). sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`, equal to `REF41_SHA`.

The tool's real CLI is `python3 -B <tool> --manifest <path>` (`main` returns `EXIT_USAGE` unless `argv[1] == "--manifest"`). Every run below uses `--manifest`. A bare path was not run.

## What the diff actually is

`diff -u` of ref41 against each control is not a small patch on `_URI_RE`. All five controls replace the round-41 regex with the same round-42 byte scanner (`_uri_ok_slow` and the class tables) and call it through a memoising `_uri_ok`. Pairwise, the five files are byte-identical outside the memo banner: stripping lines 212 up to `def _uri_ok_slow` leaves equal text. The family-specific shortcut is that memo. A lone defective loc (no earlier value with the same key) agrees with ref41 on every shape below, so the pair divergence is the memo, not the scanner.

`_parse_url` calls `_uri_ok` before `urlsplit`. The dict is process-global. `MAX_LOC_CODEPOINTS = 2048` (`loc_too_long` is recorded before the parse and is not memoised).

## Shared fixture

One urlset per control, two `<url><loc>` in order (clean, then one grammar defect), manifest `version: 1` with one check, `sitemapUrl` `https://ex.test/sitemap.xml` (directory `/`, so an in-scope path is not `loc_out_of_scope`). Files under `/fast/scratch/hyaku/kake-r44/ScoutBandFamily/fix/`. Host prefix `https://ex.test/` is 16 code points and 3 slashes.

Grammar defect is `|` (not in `pchar`) or a bad triplet `%ZZ`. Stderr was empty on every run. Exit 0 = clean, exit 1 = failed-policy.

## repeat-ctl_len_memo_band.py

Injected lines 212–234 (the only lines that differ from the other four controls):

```
# CONTROL (round-43 CtlRepeat): value-length memo for values of 6001..199999 code points
# The memo answers the round-41 URI grammar check from an earlier value with the
# same key.  The key does not determine the verdict, so a later value with that
# key can be judged differently from the round-41 tool.
_LEN_MEMO = {}
def _uri_ok(value):
    if 6001 <= len(value) <= 199999:
        key = len(value)
        try:
            return _LEN_MEMO[key]
        except KeyError:
            pass
        result = _uri_ok_slow(value)
        _LEN_MEMO[key] = result
        return result
    return _uri_ok_slow(value)
```

Shortcut: for a value of 6001..199999 code points the grammar verdict is the first verdict stored for that length, not this value's.

Shape that exposes it: two locs of equal length in that window, clean first, then the same length with one non-`pchar` (`|`). Used length 6001 (`"a"*5985` vs `"a"*5984 + "|"`). Both have 3 slashes and no `%`, so the other memos do not fire. A lone defect agrees with ref41 (scanner is not the witness).

```
python3 -B /fast/scratch/hyaku/kake-r44/ScoutBandFamily/tools/ref41.py --manifest /fast/scratch/hyaku/kake-r44/ScoutBandFamily/fix/len-band.json
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/controls-r43/repeat-ctl_len_memo_band.py --manifest /fast/scratch/hyaku/kake-r44/ScoutBandFamily/fix/len-band.json
```

ref41 exit 1:

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "len-band", "status": "findings", "error": null, "findings": [{"code": "loc_too_long", "entry": 1}, {"code": "loc_not_absolute", "entry": 2}, {"code": "loc_too_long", "entry": 2}]}]}
```

control exit 1:

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "len-band", "status": "findings", "error": null, "findings": [{"code": "loc_too_long", "entry": 1}, {"code": "loc_too_long", "entry": 2}]}]}
```

First differing finding: entry 2 `loc_not_absolute` (present on ref41, absent on the control). Both still emit `loc_too_long` because 6001 >= 2048, so the exit codes match. The witness is stdout bytes.

G7 blueprint: witnesses it only as `("value", "loc", clean)` then `("value", "loc", defect)` with the same length in 6001..199999. The blueprint's "control says clean" is false here. A two-check manifest (one loc per file, the layout `layout_f` actually emits) was also run: ref41 puts `loc_not_absolute` on the second check, the control does not; both checks still have `loc_too_long`; both exit 1.

## repeat-ctl_depth_memo_band.py

Injected lines 212–234:

```
# CONTROL (round-43 CtlRepeat): dir-depth memo for values with >= 64 '/' separators and <= 1799 code points
_DEPTH_MEMO = {}
def _uri_ok(value):
    if value.count('/') >= 64 and len(value) <= 1799:
        key = value.count('/')
        ...
    return _uri_ok_slow(value)
```

Shortcut: a value with at least 64 slashes and length <= 1799 reuses the first grammar verdict stored for that slash count.

Shape: both locs length 138 (<= 1799), 64 slashes (`https://ex.test/` + `a/`*61 vs `a/`*60 + `|/` ). The `|` does not change the slash count. Key is the count only, not the length.

ref41 exit 1:

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "depth-band", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 2}]}]}
```

control exit 0:

```
{"version": 1, "verdict": "clean", "checks": [{"id": "depth-band", "status": "clean", "error": null, "findings": []}]}
```

First differing finding: entry 2 `loc_not_absolute` vs absent (control verdict `clean`). Lone `|/` loc: both tools exit 1 with `loc_not_absolute` on entry 1.

G7 blueprint: the planned depth pair (slash count >= 64, both lengths <= 1799, clean loc first) witnesses it. A length of 1800 with the same 64 slashes does **not**: the band control agreed with ref41 on `fix/depth-deep.json` (both exit 1, both report entry 2 `loc_not_absolute`).

## repeat-ctl_defpos_memo_band.py

Injected lines 212–234:

```
# CONTROL (round-43 CtlRepeat): defect-position memo for a first '%' at index >= 1000 and <= 1799 code points
_DEFPOS_MEMO = {}
def _uri_ok(value):
    if value.find('%') >= 1000 and len(value) <= 1799:
        key = (len(value), value.find('%'))
        ...
    return _uri_ok_slow(value)
```

Shortcut: a value whose first `%` is at index >= 1000 and whose length is <= 1799 reuses the first grammar verdict stored for the pair `(length, index of first '%')`.

Shape: both length 1003, first `%` at index 1000. Clean is a valid triplet `%41`; defect is `%ZZ` at the same index. A percent-free clean loc does not enter the memo, so it cannot seed a witness.

ref41 exit 1:

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "defpos-band", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 2}]}]}
```

control exit 0:

```
{"version": 1, "verdict": "clean", "checks": [{"id": "defpos-band", "status": "clean", "error": null, "findings": []}]}
```

First differing finding: entry 2 `loc_not_absolute` vs absent. Lone `%ZZ`: both tools agree (`loc_not_absolute`, exit 1).

G7 blueprint: witnesses it if both locs share length <= 1799 and the same first-`%` index >= 1000, and the first loc's `%` is a valid triplet. Length 1800 with `%` at index 1000 does **not** hit this control (agreed with ref41 on `fix/defpos-late.json`).

## repeat-ctl_depth_memo_deep.py

Injected lines 212–230 (no length cap, shorter comment, no "key does not determine the verdict" paragraph):

```
# CONTROL (round-43 CtlRepeat): dir-depth memo for values with 64+ '/' separators
_DEPTH_MEMO = {}
def _uri_ok(value):
    if value.count('/') >= 64:
        key = value.count('/')
        ...
    return _uri_ok_slow(value)
```

Shortcut: any value with 64 or more slashes, regardless of length, reuses the first grammar verdict for that slash count.

Shape that is inside deep and outside the band: length 1800, 64 slashes (the band pair plus `b`*1662). 1800 < 2048, so `loc_too_long` is not involved.

ref41 exit 1:

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "depth-deep", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 2}]}]}
```

control exit 0:

```
{"version": 1, "verdict": "clean", "checks": [{"id": "depth-deep", "status": "clean", "error": null, "findings": []}]}
```

First differing finding: entry 2 `loc_not_absolute` vs absent. The band control on this same file agreed with ref41.

G7 blueprint: the planned in-window depth pair also hits this predicate. Confirmed on the two-check depth-band manifest: this control exited 0 (`clean` on both checks) while ref41 exited 1. A separate len>1799 pair is not required. It must not be the only depth pair, or `repeat-ctl_depth_memo_band.py` stays unwitnessed.

## repeat-ctl_defpos_memo_late.py

Injected lines 212–230:

```
# CONTROL (round-43 CtlRepeat): defect-position memo for a first '%' at index 1000+
_DEFPOS_MEMO = {}
def _uri_ok(value):
    if value.find('%') >= 1000:
        key = (len(value), value.find('%'))
        ...
    return _uri_ok_slow(value)
```

Shortcut: any value whose first `%` is at index >= 1000, regardless of length, reuses the first grammar verdict for `(length, that index)`.

Shape inside late and outside the band: length 1800, first `%` at index 1000, `%41` then `%ZZ`, padded with `b`.

ref41 exit 1:

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "defpos-late", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 2}]}]}
```

control exit 0:

```
{"version": 1, "verdict": "clean", "checks": [{"id": "defpos-late", "status": "clean", "error": null, "findings": []}]}
```

First differing finding: entry 2 `loc_not_absolute` vs absent. The band control on this file agreed with ref41.

G7 blueprint: the planned in-window defpos pair also hits this predicate. Confirmed on the two-check defpos-band manifest: this control exited 0 while ref41 exited 1. Same caveat: do not drop the len<=1799 pair.

## Blueprint verdict

`g7_band_memos.py` (ExecG7Bands) can witness all five controls with the planned pairs of `("value", "loc", ...)` units, clean member first, in one `cases()` list (`layout_f` keeps that order and runs every check in one process). `derived_smu` is `scheme://host/sitemap.xml` and does not share these keys.

What the planned text does not say, and what has to hold:

- The field is `loc`. A `sitemapUrl` defect is `check_invalid` (or, once memoised true, an audit of the shared dummy file), not `loc_not_absolute`.
- Length-band divergence is stdout only. Both exit 1 because every in-band value is also `loc_too_long`.
- The defpos clean member must itself contain a valid `%HH` at the shared index.
- Depth members must both stay at `len <= 1799` (the key is the slash count, but the band predicate checks length too). The defect must not add or remove a `/`.
- Deep and late need no extra shape. They are witnessed by those in-window pairs. An out-of-window pair (len >= 1800) witnesses only the uncapped control.

## Files

Scratch only, plus this report. Fixtures and stdout copies: `/fast/scratch/hyaku/kake-r44/ScoutBandFamily/fix/`, `/fast/scratch/hyaku/kake-r44/ScoutBandFamily/out/`. No lane file other than this report was written.
