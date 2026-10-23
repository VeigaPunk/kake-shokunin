# CtlNoReader — round-41 C1 no-reader (manifest only) control

Leaf seat; no lane file touched. Tools, receipts and helpers live only in
`/fast/scratch/hyaku/kake-r41w1/CtlNoReader/`. Counter `c1_count.py` unchanged, sha256 `2acc443a…67b4`;
base `4de35f8c…1460e` and reference `6d7c2dd4…010a` (both read-only).

| tool | sha256 | work it skips |
|---|---|---|
| `no_reader_all_valid.py` | `70ebfda5acf67e1402f103a9849cbe6c914a4873f4ecb9c1e1df14214f243ace` | never opens a sitemap file; every `loc` guessed valid |
| `no_reader_all_invalid.py` | `7dabf72e5423c7f27c12350f63cda6285e3a6b7572c4ba780e23cf56c8965247` | never opens a sitemap file; every entry 1..60 guessed invalid |

Both are `ref_fix.py` with `_evaluate_check` returning before `_audit_file` (XML audit code unreachable)
and keep the reference's RFC 3986 rule for the manifest's `sitemapUrl`. After `_load_manifest`,
`_guard_no_reads` installs a PEP 578 `open` hook on the manifest's directory; a recorded open makes the
tool emit `input_invalid` (score 0), so a scored run proves zero case-dir reads. `tripwire_check.py`
exit 0 (`tripwire fires: True`) proves the hook sees an `open` on a case-dir file.

## Results — receipts in `receipts/`, runner `run_controls.sh`
`timeout 900 python3 -B .ufo/waves/round-41/c1_count.py --root <lane> --tool-file <tool> --label CtlNoReader-<suffix> --seed <seed> --out <receipt>`, under `prlimit --as=4000000000`.

| tool | seed | passed | byField (loc, sitemapUrl) | met | counter exit |
|---|---|---|---|---|---|
| all-valid | 41001 | 1202 | 398/630, 804/804 | false | 1 |
| all-valid | 145622082234355 | 1202 | 398/630, 804/804 | false | 1 |
| all-invalid | 41001 | 1036 | 232/630, 804/804 | false | 1 |
| all-invalid | 175238237951072 | 1032 | 228/630, 804/804 | false | 1 |
| base | 41001 | 1049 | 509/630, 540/804 | false | 1 |
| ref_fix | 41001 | 1434 | 630/630, 804/804 | true | 0 |

byComponent seed 41001, all-valid / all-invalid / base / ref, each /239: fragment 211/162/157/239,
host 210/163/165/239, path 213/160/166/239, port 148/225/239/239, query 206/167/153/239,
userinfo 214/159/169/239. `all-valid` is caught by the 232 oracle-invalid `loc` cases (userinfo 25,
host 29, port 91, path 26, query 33, fragment 28): it answers `clean` to every file it never read.
`all-invalid` is caught by the 398 oracle-valid `loc` cases (port, 14 of 15 port `loc` labels, is its only
strong group). Two independent seeds per tool, so neither result rests on one draw.
## Findings
- **The counter scores this skip below 1434**: best manifest-only score 1202/1434, 232 below; no variant
  reached `met`. This is not a "control meets the predicate" notice.
- `sitemapUrl` is manifest data, so the no-reader gets 804/804 once its URL rule is the reference's: the
  manifest half is fully obtainable without the skipped work (base 540/804 → 804/804 is the whole
  264-case sitemapUrl gap). Separation rests on `loc`, with a 225–242-case margin over seeds.
  [INFERENCE] a `sitemapUrl`-only predicate would be met by this control class.
- [INFERENCE, from the counter's `generate`/`layout` plus `label_stats.json`] A no-reader's per-entry
  answer can only be constant: labels stay in the counter process, and the tool sees only randomized ids,
  file names and group membership. Ceiling `804 + #oracle-valid loc` = 1192–1209 over seeds 41001–41005
  and one random (`locValid` 398/399/405/403/396/388). Measured 1202 matches; a no-reader receipt above
  ~1210 read something.
- `loc` labels are ~63% valid (398/630), so the all-valid constant beats all-invalid by 166 cases.
## Statement checks
- "generates 1434 cases per run" — holds (630 `loc` + 804 `sitemapUrl`).
- "the base tool scores 1049" — holds (seed 41001: loc 509, sitemapUrl 540).
- "the reference repair scores 1434" — holds (`met` true, seed 41001).
- "base 1049 is below the reference" — holds, but this control class scores **above** base (1202);
  "control below base" is not the separation test on this counter.
## Limits
Not built: a `stat`-size-per-file predictor (same per-entry blindness; upside an [INFERENCE] ~+80 on
port-heavy files). No `urlsplit`-only `sitemapUrl` ablation (base's 540/804 already measures that path).
All tool runs exited 2 because every draw holds invalid `sitemapUrl` checks; the counter reads only JSON.
