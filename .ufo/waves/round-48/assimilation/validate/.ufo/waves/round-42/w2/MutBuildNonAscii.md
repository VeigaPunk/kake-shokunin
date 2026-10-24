VERDICT: the attack failed — counter v3 (`ce2d5a0c…`) killed 6/6 one-member non-ASCII mutants of the landed build; no survivor, no coverage gap found on the assigned surface.

# Seat KakeR42.MutBuildNonAscii (wave 2, falsify) — attack on counter v3's power over non-ASCII handling

Base: lane tip `721310b1`, build `020bc457`, tool `scripts/sitemap_audit.py` sha256
`914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` (copied to
`/fast/scratch/hyaku/kake-r42w2/MutBuildNonAscii/build.py`, `cmp` byte-identical to the lane file, which still
hashes `914ebdee…` after the seat). References: tip41 `50287ac6…`, base40 `4de35f8c…`, counter v3 `ce2d5a0c…`.

## Detector baseline (pristine bytes, same counter, fresh seed)

`timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-42/c42_count_v3.py --root <lane> --tool-file build.py
--label KakeR42.MutBuildNonAscii-pristine --out pristine.json` → exit **0**, seed 43802594672256, equal **10/10**,
ratios T1 0.9835 / T2 1.3738 / T3 1.2918 / T4 1.1490 / T5 1.2234, met true. Baseline passes, so kills below are
attributable to the mutation and not to the counter.

Local name differential (`probe.py`: importlib-loads tip41, build, m1–m6; `_parse_url` on 13 targeted values):
pristine build differs from tip41 on **0/13** — the detector's oracle is sound at the baseline.

## Mutants (each one line changed; all scored with the command above, no `--seed`, exit 1 = not met)

| # | sha256 | one-line change | seed | equalRuns | ratios T1/T2/T3/T4/T5 | met | caught by | witness vs tip41 (`_parse_url`) |
|---|--------|-----------------|------|-----------|------------------------|-----|-----------|----------------------------------|
| m1 | `66e06187…` | L130 `_TABLE_IP_LITERAL = _class_table(_IP_LITERAL_ASCII)` — bytes ≥0x80 accepted inside `[ ]` | 275742781642591 | 8/10 | 1.086/1.242/1.260/1.381/1.177 | false | **B, E** | `https://[fe80::1%25en1é]/a` → build/tip41 `None`; m1 `('https','fe80::1%25en1é',443,'/a')` |
| m2 | `f1981f7a…` | L113 `range(0x80, 0x100)` → `range(0xA0, 0x100)` — non-ASCII floor at U+00A0 | 269339079978634 | 7/10 | 0.978/1.286/1.457/1.243/1.354 | false | **C, D, E** | `https://a/\u0080` → tip41 tuple; m2 `None` (also `\u009f`, `\U0010ffff`) |
| m3 | `0b35aa08…` | L127 `_TABLE_REGNAME = _class_table(_REGNAME_ASCII, non_ascii=False)` — non-ASCII host rejected | 147169950672397 | 8/10 | 1.044/1.338/1.454/1.175/1.027 | false | **D, E** | `https://é.example/` → tip41 `('https','é.example',443,'/')`; m3 `None` |
| m4 | `8cfd2c2c…` | L126 `_TABLE_USERINFO = _class_table(_USERINFO_ASCII, non_ascii=False)` — non-ASCII userinfo rejected | 146275780877943 | 8/10 | 1.001/1.382/1.332/1.205/1.060 | false | **D, E** | `https://usér@example.test/` → tip41 tuple; m4 `None` |
| m5 | `5ab13bd4…` | L128 `_TABLE_PCHAR = _class_table(_PCHAR_ASCII, non_ascii=False)` — non-ASCII path rejected | 121872614217817 | 7/10 | 1.040/1.344/1.322/1.226/1.519 | false | **C, D, E** | `https://a/\u0080` (and `\u00a0`, `/paéth`, `\ud800`, `\U0010ffff`) → tip41 tuple; m5 `None` |
| m6 | `f357322e…` | L215 `encode("utf-8", "surrogatepass")` → `encode("utf-8", "strict")` — lone surrogate raises | 153620960046194 | 9/10 | 1.045/1.345/1.518/1.190/1.135 | false | **E** | `https://a/\ud800` → tip41 `('https','a',443,'/\ud800')`; m6 `EXC UnicodeEncodeError` (tool crashes, exit/output differ) |

Receipts: `/fast/scratch/hyaku/kake-r42w2/MutBuildNonAscii/m{1..6}.json`, `pristine.json`.
Per-run flags (from each receipt's `runs`): m1 A ok B UNEQ C ok D ok E UNEQ; m2 C/D/E UNEQ; m3 D/E UNEQ;
m4 D/E UNEQ; m5 C/D/E UNEQ; m6 E UNEQ. Every timing shape T1–T5 stayed equal for all six, so no mutant was
killed by a cost or timing artefact — each kill is an equality-run judgment.

## Checked statements

- SCORECARD "run E … boundary code points (U+0080/U+009F/U+00A0, surrogate edges…)" — **holds**: m2 (floor
  0xA0) and m6 (surrogate reject) are killed by run E alone; run E is the only run that kills m6 (9/10).
- SCORECARD "bytes ≥0x80 … rejected inside an IP-literal" — **holds**: m1 (accepting them) is killed.
- SCORECARD "keeps every judgment of the round-41 tool on the generated runs" — **holds on this surface**: the
  six single-member changes each break it, and the pristine build is 10/10 with 0/13 name-differential.
- "The counter is too weak on non-ASCII" (the hypothesis under test) — **wrong**: 6/6 killed; the wave-1 v1
  survivors of this class (non-ASCII range via U+00A0, surrogates excluded) are both caught by v3 (m2, m6).
- No meeting tool was produced, so the equivalence-differential clause (witness value) was not exercised and no
  kill-rule event is claimed.

## Restoration / footprint

No lane file was written: `scripts/sitemap_audit.py` still sha256 `914ebdee…`; all writes are under
`/fast/scratch/hyaku/kake-r42w2/MutBuildNonAscii/` (7 receipts, `build.py`, `m1–m6.py`, `probe.py`, ~0.3 MB).
The lane build itself was only read; the mutants are copies, so restoration evidence is the unchanged build hash
plus the byte-identical `build.py` copy. No installs or upgrades were made. No process of this seat is running
(`pgrep -af MutBuildNonAscii` → none); every scoring command exited (exit codes 1,1,1,1,1,1 and 0 for pristine).
