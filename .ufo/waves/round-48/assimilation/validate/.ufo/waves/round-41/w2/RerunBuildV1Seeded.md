# RerunBuildV1Seeded — counter v1 at the build, seed 41001 vs committed receipt

Seat: `KakeR41.RerunBuildV1Seeded` (falsify, wave 2). Axis: operability.
Statement checked: "the build scores 1434/1434 under counter v1
(`verification/build/c1-v1-at-eae5ae2c-41001.json`)."
Revision under test: `eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6` (= `git rev-parse HEAD` at run time).
Counter v1 `.ufo/waves/round-41/c1_count.py` sha256 `2acc443a…67b4` — matches `counterSha256`
in the committed receipt. Oracle wheel `abnf-2.9.1-py3-none-any.whl` sha256 `cdcac127…0917`
— matches `oracleSha256`. `bwrap` at `/usr/bin/bwrap`. No installs.

## Command (exit code 0; wall time 1.78 s)

```
prlimit --as=4000000000 timeout 900 python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6 \
  --seed 41001 \
  --out /fast/scratch/hyaku/kake-r41w2/RerunBuildV1Seeded/v1-41001.json
```

Stdout: `{"label":"", "revision":"eae5ae2c…07b7d6", "passed":1434, "cases":1434,
"byField":{"loc":"630/630","sitemapUrl":"804/804"}, "met":true, "note":null}`.

## Receipt comparison (mine vs committed `.ufo/waves/round-41/verification/build/c1-v1-at-eae5ae2c-41001.json`)

Field-by-field JSON diff — every key identical except `label`:

| field | value (both receipts) |
|---|---|
| passed | 1434 / cases 1434 |
| met | true |
| seed | 41001 |
| revision | eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6 |
| toolSha256 | 0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf |
| counterSha256 | 2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4 |
| oracleSha256 | cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917 |
| byField | loc 630/630, sitemapUrl 804/804 |
| byComponent | all six 239/239 (userinfo, host, port, path, query, fragment) |
| oracleInvalid | 636; misses []; note null; toolExit 2; toolFile null |

Only difference: `label` `''` (mine; assigned command passes no `--label`) vs `'build-v1'`
(committed). Cosmetic; the label carries no case identity or score. Whole-file sha256 therefore
differs (`9bc673ec…` vs `fa2731f8…`), expected.

`toolExit 2` note: the counter invokes the tool with `--manifest` only; exit 2 is its usage-error
path but the stdout JSON the counter reads is complete — same shape as the committed receipt.

## Verdict on the statement

**Holds.** Independent re-run reproduces the committed receipt exactly on every substantive
field: exit 0, met=true, 1434/1434, byField and byComponent saturated, seed 41001, and the
claimed build `toolSha256 0b485431…13edbf`. The statement is neither overstated nor wrong.

Scope: this seat only re-ran counter v1 seed 41001 at the build. No claim about other seeds
(`RerunBuildV1Random`), counter v2 (`RerunBuildV2`), selftest, or the real-run byte equality.

## Tooling

No installs or upgrades; python3 3.14.8, bwrap, git already on the host.
