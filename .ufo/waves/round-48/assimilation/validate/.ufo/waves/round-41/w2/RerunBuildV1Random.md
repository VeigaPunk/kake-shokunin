# RerunBuildV1Random — counter v1 at the build, three fresh random seeds

Seat: `KakeR41.RerunBuildV1Random` (falsify, wave 2). Axis: operability.
Statement checked: "the build meets counter v1 on any seed."
Revision under test: `eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6` (= HEAD; working tree clean
for `scripts/sitemap_audit.py` and the counter).
Counter v1 bytes: `.ufo/waves/round-41/c1_count.py` sha256
`2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4` — matches the frozen value.
Oracle wheel sha256 `cdcac127…0917` — matches. `bwrap` at `/usr/bin/bwrap`. No installs.

## Commands (cwd = repo root; `prlimit --as=4000000000 timeout 900`, no `--seed`)

```
python3 -B .ufo/waves/round-41/c1_count.py --root . \
  --revision eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6 \
  --label RerunBuildV1Random-<N> --out /fast/scratch/hyaku/kake-r41w2/RerunBuildV1Random/receipt-<N>.json
```

## Results

| run | seed (os.urandom) | exit | passed | byField | byComponent | met |
|---|---|---|---|---|---|---|
| 1 | 212450270016260 | 0 | 1434/1434 | loc 630/630, sitemapUrl 804/804 | all six 239/239 | true |
| 2 | 51887750559447 | 0 | 1434/1434 | loc 630/630, sitemapUrl 804/804 | all six 239/239 | true |
| 3 | 211039439028470 | 0 | 1434/1434 | loc 630/630, sitemapUrl 804/804 | all six 239/239 | true |

Receipts: `/fast/scratch/hyaku/kake-r41w2/RerunBuildV1Random/receipt-{1,2,3}.json`.
Common fields: `toolSha256 0b485431…13edbf` (the claimed build sha; verified independently
via `git show eae5ae2c:scripts/sitemap_audit.py | sha256sum`), `counterSha256 2acc443a…67b4`,
`oracleInvalid` 634 / 628 / 626, `misses []`, `note null`, `toolExit 2`.

Note on `toolExit`: the counter runs the tool with only `--manifest` inside bwrap; the tool
exits 2 (usage error) on stderr, but its stdout JSON is complete and every one of the 1434
judged fields was read from it — the counter's judge only reads `checks[]` items, so
`passed == 1434` is unaffected by the exit code. Same shape as the retained wave receipts.

## Verdict on the statement

**Holds** on all three fresh random seeds observed: met=true, exit 0, 1434/1434 each run,
byField and byComponent saturated, zero misses. Consistent with the pre-landed receipts
(`verification/build/c1-v1-at-eae5ae2c-{41001,random}.json`, seeds 41001 and
257874988366475, both 1434/1434 met). Three samples do not prove "any seed" universally,
but nothing in this check contradicts the statement and every sample supports it.

Scope: this seat ran only counter v1 at the build. No claim about counter v2, the control
receipts, selftest, or the byte-equal real run (other seats own those).

## Tooling

No installs or upgrades; only python3 3.14.8, bwrap, git, jq already on the host.
