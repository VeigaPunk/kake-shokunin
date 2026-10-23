# CtlSkipU — partial repair that skips class U

Result: NOT MET. 20/30 witnesses, exit 1, 10 witnesses short. No kill: nothing here meets the predicate.

## Tool

`/fast/scratch/hyaku/kake-r40w1/CtlSkipU/skipu.py`
sha256 `ed579d17015c74237ab6dfe34f4b599fe8f78eddacb659bf3bc5fd902d146caa`
Construction: reference `/fast/scratch/hyaku/kake-r40/shared/ref_fix.py` with the
`_parse_url` guard block removed (ref_fix.diff hunk 1 only). `diff -u` against the base
(`git show f043c72:scripts/sitemap_audit.py`, sha256 `6d86c8cef78e36d372f7277096ec163cc8f1e919fa66702ad24e5e32f9a240ec`)
shows exactly two hunks: the UTF-16/NUL -> `xml_malformed` rule and the R duplicate-id rule,
both byte-identical to the reference. `_parse_url` is byte-identical to base; URL judgment is untouched.

## Counter runs

Command shape (all, exit codes measured):
`timeout 1200 prlimit --as=4000000000 python3 -B kake-shokunin/.ufo/waves/round-40/c1_count.py --root kake-shokunin --tool-file <tool> --label <L> --out <receipt>`

| tool | sha256 (12) | passed | byClass | selftest | met | exit |
|---|---|---|---|---|---|---|
| skipu.py (skip U) | ed579d17015c | 20 | E 9/9, R 8/8, U 3/13 | PASS 150/150 | false | 1 |
| skipu_urlhalf.py (skip loc half) | 8025bf69db0f | 24 | E 9/9, R 8/8, U 7/13 | PASS 150/150 | false | 1 |
| skipu_lochalf.py (skip sitemapUrl half) | 2095d8f88a78 | 26 | E 9/9, R 8/8, U 9/13 | PASS 150/150 | false | 1 |
| skipu_percent.py (heuristic over-block) | 141678b1797f | 19 | E 9/9, R 8/8, U 2/13 | PASS 149/150 | false | 1 |
| base f043c72 (unrepaired) | 6d86c8cef78e | 10 | E 4/9, R 3/8, U 3/13 | PASS 150/150 | false | 1 |

Receipts `receipt{,-urlhalf,-lochalf,-percent,-base}.json` in the sandbox, counter sha256
`6d73b8f498a29a5a86c9a7f1ce5d87cd135c40f1b634d869d14659cc10bee8d8`; seeds 64472905555718,
255642396474101, 187734660829295, 104393477913456, 4960753668980 (skipu, urlhalf, lochalf, percent, base).

## What caught the skip

- skipu: U1..U10 fail — `exit 0 != 1` for U1-U6 (tab/LF/CR in `loc`, incl. `&#13;`, host-split tab,
  `http:\n//`), `exit 0 != 2` for U7-U10 (tab/CR/leading space/leading U+0001 in `sitemapUrl`).
  Witnesses at `.ufo/waves/round-40/c1_count.py:96-105`.
- urlhalf 24/30: U1-U6 only (`c1_count.py:96-101`) — loc half is independently required.
- lochalf 26/30: U7-U10 only (`c1_count.py:102-105`) — sitemapUrl half is independently required.
- percent 19/30: U12 `exit 1 != 0` (`c1_count.py:107`) plus selftest 149/150 — negative witnesses
  reject over-blocking, so a crude pattern heuristic does not buy the predicate either.
- `judge` compares exit, verdict and the full normalized check list exactly (`c1_count.py:162-186`);
  no partial-credit route past the U witnesses.

## Statements attacked

1. "The C1 counter's 30 witnesses reject a tool that skips class U" — HOLDS. 20/30, U 3/13, exit 1;
   margin 10 witnesses, and no single-half skip exceeds 26/30.
2. "Class U repair is load-bearing for the predicate" — HOLDS. Each half is separately covered
   (loc U1-U6, sitemapUrl U7-U10); removing only the `_parse_url` guard drops the tool from 30 to 20.
3. "The round-39 selftest at 150/150 evidences C1 repair" — OVERSTATED, effectively wrong for this class.
   The unrepaired base tool passes 150/150 (`receipt-base.json`), and the skip-U control also passes
   150/150. `SELFTEST_PASS` / `st_ok` (`c1_count.py:37,286`) adds no discriminating power over classes
   E, R or U; all rejection in this wave came from the 30 witnesses. The predicate would be met by a
   skip-U tool if the witnesses were dropped.
4. "Kill rule" — NOT TRIGGERED; best U-skipping control 26/30, met=false.
5. "Frozen counter rejects the skip" — HOLDS, with the caveat in 3: only the witness clause carries it.

Notes: no installs, no network, no lane mutation (read-only `git show`/`rev-parse`, tip
`f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8`); sandbox <1 MB; no refusal or model switch.
