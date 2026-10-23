# ExecBuildRegex — fast, behaviour-equal `_URI_RE` (round 42, wave 1)

## What I built

* Tool: `/fast/scratch/hyaku/kake-r42w1/ExecBuildRegex/sitemap_audit.py`, sha256 `8a30432dc69a671b9aa53e05c6356dc4ca8c0afb3906aa971e78318232ecbc13` — a copy of tip41 (`50287ac6…`, byte-identical to `scripts/sitemap_audit.py` at the lane tip `d1c3f37`) with **only** the URL block changed (`build.diff`: 45+/16− in `scripts/sitemap_audit.py`, 47+ in `scripts/sitemap_audit_selftest.py`, 133 lines, sha256 `60f298076f23c03501d1877ef01afc21637299880c439c8ec74b56bf7e92268e`). `_parse_url` below the regex, every other rule and the CLI are unchanged.
* Technique (`sitemap_audit.py:73-121`): every class is split into an ASCII core plus the rare items it may contain — a percent triplet `%XX` and one non-ASCII code point — and each run is spelled possessively (`[core]*+(?:(?:%XX|[^\x00-\x7f])[core]*+)*+`, Python ≥3.11 `*+`; host `ScoutPythonRe`). The round-41 pattern spelled each class as one alternation, so the engine unwound every repetition when a defect appeared late.
* Selftest: `/fast/scratch/hyaku/kake-r42w1/ExecBuildRegex/sitemap_audit_selftest.py`, sha256 `57c382b5e0c8baf11ae3bcd7de734a91743747ca043fc4d94ad731da57070f7d` — the lane selftest plus 10 `r42_*` guards (`sitemap_audit_selftest.py:999-1036`): `loc`/`sitemapUrl` × zone id `%eth0`, `%25eth0` (accepted), `%é`, `%en|0` (rejected), plus a 2 047-code-point single-segment `loc` ending in `%` (rejected) and the same value ending in `b` (accepted).
* Comment fix routed by the round-41 closure: `sitemap_audit.py:67-72` now states the bracket rule exactly (only `[A-Za-z0-9._~:!$&'()*+,;=%-]` before `urlsplit`; a zone id with a non-ASCII character or `|` is rejected; the port range is judged by `urlsplit`), and `:80-84` explains the possessive rewrite.

## Commands run (exit codes)

| command | exit |
|---|---|
| `python3 -B work/patch.py` (writes both files) | 0 |
| `python3 -B work/difftest.py 200000 20261023` | 0 (200 000 values, 0 disagreements) |
| `python3 -B work/difftest.py 250000 777` | 0 (250 000, 0) |
| `python3 -B work/difftest.py 120000 555` | 0 (120 000, 0) |
| `python3 -B work/difftest2.py 200000 7` (per-component non-ASCII/percent/defect) | 0 (200 000, 0) |
| `python3 -B work/difftest2.py 100000 31337` | 0 (100 000, 0) |
| `python3 -B sitemap_audit_selftest.py --tool …/tip41.py` | 0, `PASS 235/235` |
| `python3 -B sitemap_audit_selftest.py --tool …/sitemap_audit.py` | 0, `PASS 235/235` |
| round-41 real run, both tools, `--manifest manifest.json` | 1 / 1, stdout byte-identical, sha256 `2ffbea3a8fafa3ca8d7c759acc2c6c7df9646a74c388757800f6598e9180b22e` |

Differential total: **870 000 generated values, 0 disagreements** in `_parse_url`'s full return tuple (long, short, IP-literal, non-ASCII, percent, defects at any position, both seeds per generator). Evidence, not proof.

## Timing (my own measurement; the counter was **not** run)

Per call, `_parse_url`, µs (best of 5): short valid 1.54→**1.01**; valid 2 000 cp 36.3→**3.5**; defect at the end, 2 000 cp 102.3→**1.6**; 200 000 cp with a late defect 9 728→**150**.
CLI, child CPU s, against the round-40 tool: T1-like 20 000 long `loc` with a late defect: r40 0.52, r41 3.03, build **0.54** (r41/r40 5.83, **build/r40 1.04**); T2-like 20 000 valid long `loc`: 0.52 / 1.31 / **0.61** (2.52 / **1.17**); T3-like 50 000 valid short `loc`: 0.46 / 0.60 / **0.45** (1.30 / **0.98**); T5-like 48 `sitemapUrl` of 200 000 cp: 0.04 / 0.64 / **0.05** (16.0 / **1.25**).

## Counter results

**None — the counter was not run by this seat** (`c42_count.py` forbidden). `equalRuns`, `ratios`, `met` for this tool are **not measured**; the L1 must score `--tool-file /fast/scratch/hyaku/kake-r42w1/ExecBuildRegex/sitemap_audit.py`.

## Findings

1. `sitemap_audit.py:73-121` — the round-41 cost driver is the class range `\u0080-\U0010ffff` in every class (sre BIGCHARSET, per-character range scan) plus the late-defect unwind; it is not catastrophic backtracking, but the rewrite removes both (10–50× per call).
2. `sitemap_audit.py:67-72,80` — the round-41 comment ("an IP literal's contents and the port range are still judged only by `urlsplit`") was **overstated**; the tool rejects a zone id with a non-ASCII character or `|` before `urlsplit`. Corrected here, as `CriticZoneId` routed.
3. `sitemap_audit.py:78-84` — the rewrite needs **Python ≥ 3.11** (possessive quantifiers); the lane interpreter is 3.14.8, so the tool's "Python 3 standard library only" note now has an unstated floor. Nothing else in the lane pins a floor.

## Per checked statement

* "keeps EVERY judgment of the round-41 tool" → **holds** on 870 000 generated values, 235/235 fixtures on both tools, and the byte-identical round-39/41 real run — evidence, not proof.
* "costs at most 2.0 times the round-40 tool's CPU time on five input shapes" → **holds locally** on four self-built shapes (0.98–1.25); **unmeasured** on the counter's own shapes.
* "slow on long adversarial values (backtracking)" → **overstated**: linear per-character scanning of a big character class plus a late-defect unwind, not exponential backtracking.
* "the rewrite keeps every judgment" → **holds**; the regex's language is unchanged (same alternation per position: `%` only via `%XX`, non-ASCII only as a single code point).

Tooling: nothing installed or updated (no pacman/uv/npx/cargo); Python 3.14.8 stdlib only. No network. Writes limited to this sandbox, the clone, and this report.
