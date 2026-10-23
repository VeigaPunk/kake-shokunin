# SonicPins — round-44 wave 2, seat item "mechanical pin check of the SCORECARD round-44 section"

Seat: `kake-r44.SonicPins` (scribe, axis: freshness). Lane: `kake-shokunin`
(`/home/vgpnk/Projects/shokunin/kake-shokunin`).

**Scope of this seat's item (verbatim from `.ufo/waves/round-44/make_w2_spec.py:279-282`):**
"Mechanical pin check of the SCORECARD round-44 section (git diff SCORECARD.md): compute sha256 of
every pinned file (counter v5 5cedaa3b..., placebo 9ce3acd4..., audit driver 8ee2c8bf..., build tool
914ebdee..., any control pins) and report match/mismatch in a table."

Read-only seat: no lane file other than this report was written; no git commit/jj/push; no product
code, judge, or ledger edited.

---

## 1. What I did

1. Read the round-44 section of `SCORECARD.md` as it exists in the worktree (`git diff SCORECARD.md`
   — 184 added lines, 0 removed lines; the whole round-44 section is uncommitted).
2. Extracted every hash-shaped token from that diff (`git diff SCORECARD.md | grep -oE
   '[0-9a-f]{8,64}' | sort -u`) to enumerate the pins the section actually makes.
3. Recomputed sha256 of every artifact the section pins, and of every artifact reachable from the
   pins it makes (the counter's own internal reference pins, the manifest rows' per-control pins,
   the canary manifest rows' pins, and the `counterSha256` field carried by each round-44 receipt).
4. Cross-checked the *derived* values the section asserts (the correction-2 row attribution, the
   line citation `controls-r43/buildport-m6-default-branch.py:303-304`, the C2 ledger figures) so a
   pin that matches bytes but describes the wrong thing is not reported as a clean pass.
5. Verified the round-44 claim receipts' counter pin against the live counter bytes.

## 2. The pins the SCORECARD round-44 section makes (exhaustive)

```
$ git diff SCORECARD.md | grep -oE '[0-9a-f]{8,64}' | sort -u
020bc457
181346457990762
18cb2c28f47c3ec3732ffa06c456e61b3444b1a2
5994504518804
5cedaa3b
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75
914ebdee
9ce3acd4
```

Interpretation: `020bc457` = held-build revision; `18cb2c28…` = round base revision; `181346457990762`
and `5994504518804` = the two seeds the freeze receipt names; `5cedaa3b…` = counter v5; `9ce3acd4…` =
placebo counter; `8ee2c8bf…` = audit driver (full hash given); `914ebdee…` = held build tool.

So the section pins **four files by hash** (counter v5, placebo, audit driver, build tool) and
**no other file by hash**. The per-control pins live one level down, in
`.ufo/waves/round-44/controls-27.tsv` (27 rows) and `.ufo/waves/round-44/controls-canary.tsv`
(5 rows), which the section names by path.

## 3. Pin table — match / mismatch

| # | pinned artifact | declared sha256 | observed sha256 | verdict |
|---|---|---|---|---|
| 1 | counter v5 — `.ufo/waves/round-44/c44_count_v5.py` (diff pin `5cedaa3b…`) | `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc` | `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc` | **MATCH** |
| 2 | placebo counter — `.ufo/waves/round-44/c44_placebo.py` (diff pin `9ce3acd4…`) | `9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27` | `9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27` | **MATCH** |
| 3 | audit driver — `.ufo/waves/round-44/c44_audit.py` (diff pin `8ee2c8bf…`) | `8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75` | `8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75` | **MATCH** |
| 4 | held build tool — `scripts/sitemap_audit.py` (diff pin `914ebdee…`) | `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` | `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` | **MATCH** |
| 5 | held build bytes at revision `020bc457` (`git show 020bc457…:scripts/sitemap_audit.py`) | `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` | `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` | **MATCH** |
| 6 | counter's own REF41 pin (`c44_count_v5.py:89`, `50287ac6…`) | `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` | `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` (at `1ef7a0e9…`) | **MATCH** |
| 7 | counter's own BASE40 pin (`c44_count_v5.py:91`, `4de35f8c…`) | `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e` | `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e` (at `8eb121c8…`) | **MATCH** |
| 8 | freeze receipt `verification/freeze/control-v4blind.json` → `counterSha256` | `5cedaa3b9f918979…` | `5cedaa3b9f918979…` | **MATCH** |
| 9 | claim receipt `verification/claim/after-v5.json` → `counterSha256` | `5cedaa3b9f918979…` | `5cedaa3b9f918979…` | **MATCH** |
| 10 | placebo receipt `verification/placebo/before.json` → `counterSha256` | `9ce3acd4c4c72de0…` | `9ce3acd4c4c72de0…` | **MATCH** |
| 11 | canary receipt `verification/claim/canary.json` → `counterSha256` | `5cedaa3b9f918979…` | `5cedaa3b9f918979…` | **MATCH** |
| 12 | 27 control pins in `controls-27.tsv` (one sha256 per control file) | 27 declared | 27 recomputed | **27/27 MATCH, 0 mismatch** |
| 13 | 5 canary pins in `controls-canary.tsv` | 5 declared | 5 recomputed | **5/5 MATCH, 0 mismatch** |

**Aggregate: 0 mismatches over 11 file/receipt pins + 32 per-control pins (43 pin comparisons).**

## 4. Decisive command output (verbatim)

### 4.1 The four named pins + the build bytes at the held revision

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ sha256sum .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_placebo.py \
      .ufo/waves/round-44/c44_audit.py scripts/sitemap_audit.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27  .ufo/waves/round-44/c44_placebo.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021  scripts/sitemap_audit.py

$ git show 020bc4574729ed674299f6cab02faac1582d9464:scripts/sitemap_audit.py | sha256sum
914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021  -

$ git diff --stat 020bc4574729ed674299f6cab02faac1582d9464 -- scripts/sitemap_audit.py
(no output — the build bytes at the held revision and in the worktree are the same blob)
```

### 4.2 The 27 control pins (sha256sum -c over the manifest's own pin column)

```
$ awk -F'\t' 'NR>1{print $5"  "$4}' .ufo/waves/round-44/controls-27.tsv | sha256sum -c -
.ufo/waves/round-44/controls-r43/portlen-v1-skip-grammar-6plus.py: OK
.ufo/waves/round-44/controls-r43/portlen-v5-abbrev-window-6plus.py: OK
.ufo/waves/round-44/controls-r43/buildscheme-M5-default-port-https80.py: OK
.ufo/waves/round-44/controls-r43/buildscope-m5-empty-path.py: OK
.ufo/waves/round-44/controls-r43/buildscope-m4-port-dropped.py: OK
.ufo/waves/round-44/controls-r43/headtail-V1-prefix-cache64.py: OK
.ufo/waves/round-44/controls-r43/headtail-V2-headtail-key48.py: OK
.ufo/waves/round-44/controls-r43/headtail-V7-prefix-cache45.py: OK
.ufo/waves/round-44/controls-r43/prefixcache-p48-noreval.py: OK
.ufo/waves/round-44/controls-r43/casememo-v3-validity-lower.py: OK
.ufo/waves/round-44/controls-r43/casememo-v4-validity-lower-short.py: OK
.ufo/waves/round-44/controls-r43/casememo-v7-value-lower-nonascii.py: OK
.ufo/waves/round-44/controls-r43/casememo-v8-value-casefold-nonascii.py: OK
.ufo/waves/round-44/controls-r43/repeat-ctl_len_memo_band.py: OK
.ufo/waves/round-44/controls-r43/repeat-ctl_depth_memo_band.py: OK
.ufo/waves/round-44/controls-r43/repeat-ctl_defpos_memo_band.py: OK
.ufo/waves/round-44/controls-r43/repeat-ctl_depth_memo_deep.py: OK
.ufo/waves/round-44/controls-r43/repeat-ctl_defpos_memo_late.py: OK
.ufo/waves/round-44/controls-r43/hosttable-A-expanded46-fixed.py: OK
.ufo/waves/round-44/controls-r43/hosttable-B-expanded46-nogrammar.py: OK
.ufo/waves/round-44/controls-r43/hosttable-F-provable.py: OK
.ufo/waves/round-44/controls-r43/portvalue-memo-digits.py: OK
.ufo/waves/round-44/controls-r43/portvalue-memo-digits-67.py: OK
.ufo/waves/round-44/controls-r43/portlen-v4-cache-portlen.py: OK
.ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py: OK
.ufo/waves/round-44/controls-r43/headtail-V4-longport-head64.py: OK
.ufo/waves/round-44/controls-r43/headtail-V8-longport-tail64.py: OK
exit=0
```

### 4.3 The 5 canary pins

```
$ awk -F'\t' 'NR>1{print $5"  "$4}' .ufo/waves/round-44/controls-canary.tsv | sha256sum -c -
.ufo/waves/round-43/controls-r42/M8-port-five-digits.py: OK
.ufo/waves/round-43/controls-r42/v1_casefold.py: OK
.ufo/waves/round-43/controls-r42/v2_prefix32.py: OK
.ufo/waves/round-43/controls-r42/v4_hosttable.py: OK
.ufo/waves/round-43/controls-r42/junk_constant.py: OK
exit=0
```

### 4.4 Counter v5 re-derives from its builder (byte-for-byte), and the counter's own reference pins resolve

```
$ python3 -B .ufo/waves/round-44/build_v5.py --check; echo "exit=$?"
current sha256: 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
built   sha256: 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
exit=0

$ git show 1ef7a0e95f6884dd113fe583a997c633fe330ddd:scripts/sitemap_audit.py | sha256sum
50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d  -
$ git show 8eb121c81ffebada064eefcabcd94dd2303d646f:scripts/sitemap_audit.py | sha256sum
4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e  -
```

### 4.5 Every round-44 receipt's `counterSha256` field equals the live counter bytes

```
$ python3 -c "...compare each receipt's counterSha256 with sha256(c44_count_v5.py)..."
freeze/control-v4blind.json  counterSha256=5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  MATCH
claim/after-v5.json           counterSha256=5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  MATCH
placebo/before.json           counterSha256=9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27  MATCH
claim/canary.json             counterSha256=5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  MATCH
```

### 4.6 The claim receipt's own 27 control pins re-derive (receipt ↔ manifest ↔ file)

```
$ python3 -c "...for each of after-v5.json's 27 rows: manifest sha == receipt sha == sha256(file)..."
receipt rows: 27 pin mismatches: 0
```

### 4.7 The correction-2 claims the section makes about content (not just bytes)

The section's correction 2.2 says the `buildport-m6` row "now reads `default_port / G2`" and cites
`controls-r43/buildport-m6-default-branch.py:303-304`. Both check out:

```
$ grep -n "buildport-m6" .ufo/waves/round-44/controls-27.tsv
26:buildport-m6	default_port	G2	.ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py	68f3750025531d7815d6ec665432536abc3b0c78a036fdb49339e1f73bcbe87e	w1/MutBuildPort.md

$ awk 'NR==303||NR==304{printf "%d: %s\n", NR, $0}' .ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py
303:     if port is not None:
304:         port = 80 if scheme == "http" else 443
```

The claim receipt agrees with the manifest: `buildport-m6` → `class=G2`,
`classCaught=['G2','G4','G9']`.

Correction 2.1 says the audit driver's witness classifier was changed to *at least one* class key.
The live bytes do that (`c44_audit.py:63-66`):

```
def semantic_witness(row, class_keys):
    caught = row.get("caughtBy") or []
    return (row.get("met") is False and bool(caught) and
            any(isinstance(key, str) and key in class_keys for key in caught))
```

and the driver's own selftest passes on those bytes:

```
$ python3 -B .ufo/waves/round-44/c44_audit.py --selftest; echo "exit=$?"
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
exit=0
```

### 4.8 The C2 figures the section asserts, re-derived from `master` receipts

The section claims "14 of the 27 live-seat controls" re-scored, and the C2 repair line quotes
T1 4.21 / T5 7.05 and T1 1.00–1.01 / T5 1.11–1.22. Re-derived independently of the checker:

```
$ python3 -c "...count distinct toolSha256 over master:.ufo/waves/round-43/verification/l1-rescores/*.json..."
json receipts: 14 distinct toolSha256: 14

$ git show master:.ufo/waves/round-43/verification/freeze/ref41-base.json
ratios: {'T1': 4.207, 'T2': 1.917, 'T3': 1.152, 'T4': 1.228, 'T5': 7.047}   → quoted 4.21 / 7.05  MATCH

$ git show master:.ufo/waves/round-43/verification/freeze/build-{1,2,3}.json
build-1: T1=1.005 T5=1.105
build-2: T1=1.009 T5=1.144
build-3: T1=1.004 T5=1.215
                                                     → quoted T1 1.00–1.01, T5 1.11–1.22  MATCH
```

The checker's own output agrees and the declared before/after states are as the section states:

```
$ python3 -B scripts/ledger_latest_check.py --root . ; echo "exit=$?"
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3575
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1703
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1706
ledger-quotes: 3 figures, 0 mismatches
exit=0

$ cat .ufo/waves/round-44/verification/ledger-before.txt
rescore-tally MISMATCH quoted=18 derived=14 SCORECARD.md:3393
donothing-ratios MISMATCH quoted=T1 4.27, T5 8.68 derived=T1 4.21, T5 7.05 LOG.md:1661
build-ratio-range MISMATCH quoted=T1 1.00–1.02, T5 1.13–1.18 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1660
ledger-quotes: 3 figures, 3 mismatches
exit 1

$ python3 -B scripts/ledger_latest_check.py --selftest; echo "exit=$?"
  PASS matching fixture MATCH quoted=14 derived=14
  RED MISMATCH mismatching fixture quoted=18 derived=14
selftest: 2/2 passed
exit=0
```

The spec file the section names is the fixed contract, not a narrowable JSON: the checker ignores
any edit to it and refuses a spec that differs from its in-code contract.

```
$ python3 -B -c "import ledger_latest_check as L; ... disk==contract_spec() ..."
disk == contract_spec: True
figures ids: ['rescore-tally', 'donothing-ratios', 'build-ratio-range']
```

### 4.9 Placebo is the declared byte-copy

The section calls `c44_placebo.py` "a byte-copy of v5 whose ten class modules all delegate to
`cases_f`". Its ten class modules are one identical file that delegates to `h.cases_f`:

```
$ sha256sum .ufo/waves/round-44/classes-placebo/*.py | awk '{print $1}' | sort -u | wc -l
1
$ grep -L "cases_f" .ufo/waves/round-44/classes-placebo/*.py | wc -l
0
$ cat .ufo/waves/round-44/classes-placebo/g6_fold_pairs.py
"""Placebo class for the round-44 skip-work control: delegates to the v4 run-F
generator, so the run is real but carries none of the targeted class shapes."""

def cases(rng, h):
    return h.cases_f(rng)
```

and the placebo differs from v5 only in its class directory (line 98 vs line 102):

```
$ diff <(grep -n "CLASS_DIR = " .ufo/waves/round-44/c44_count_v5.py) \
       <(grep -n "CLASS_DIR = " .ufo/waves/round-44/c44_placebo.py)
1c1
< 98:CLASS_DIR = ".ufo/waves/round-44/classes"
---
> 102:CLASS_DIR = ".ufo/waves/round-44/classes-placebo"
```

The placebo's own receipt therefore carries the placebo hash, and it witnessed 1/27 (not 27/27) —
i.e. the classes, not the harness, do the work:

```
$ python3 -c "read .ufo/waves/round-44/verification/placebo/before.json"
counter= .ufo/waves/round-44/c44_placebo.py
counterSha256= 9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27
witnessed= 1 notMet= 3 ok= False
```

## 5. Verdict against the item's named attack

**Attack:** mechanical pin check of the SCORECARD round-44 section — recompute sha256 of every
pinned file and report match/mismatch.

**Verdict: PASS.** Every hash the round-44 section pins resolves to the bytes it claims:
4/4 directly-named file pins MATCH (counter v5, placebo, audit driver, held build tool), the held
build's bytes at revision `020bc457` are byte-identical to the worktree build and hash to the
declared `914ebdee…`, 27/27 control pins MATCH, 5/5 canary pins MATCH, and 4/4 round-44 receipts
name the live counter's actual hash. 43/43 pin comparisons match; **0 mismatches**. Two
content-level claims that ride on those pins (correction 2.1's classifier change and correction
2.2's row re-attribution) were also checked against the bytes and both hold, as do the three C2
ledger figures (re-derived independently from `master` receipts).

## 6. Findings (observations for the L1; nothing here was edited)

1. **The class corpus is unpinned in the ledgers.** `LOG.md:1694` names
   `.ufo/waves/round-44/classes/gN_*.py` as the corpus that witnesses the controls, but neither
   `SCORECARD.md` nor `LOG.md` carries a sha256 for any class module or for the manifest
   `controls-27.tsv` itself (`grep -c "g6_fold_pairs\|classes/g1\|a1f0e364\|233afa37" SCORECARD.md
   LOG.md` → 0 in both). Since the wave explicitly authorises `classes/g6_fold_pairs.py` to be edited
   this wave, the corpus bytes that decide the 27/27 claim can change without any ledger pin moving.
   Observed at check time: `g6_fold_pairs.py` sha256
   `f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d` (unchanged from what
   `.ufo/waves/round-44/w2/SentinelScope.md` and `w2/ScoutSeedStability.md` recorded), and
   `controls-27.tsv` sha256 `a1f0e364dad5ff937666966a16622e6895591a2eb3db714d6ecf3f3948c31bf8`.
   The manifest's own bytes already moved once this round (`233afa37…` → `a1f0e364…`, per
   `w2/ScribeLessonMistake.md`) — recorded here because the ledger never carried the old value.
2. **No receipt records the audit driver's own hash.** `c44_audit.py` is the counting driver and
   is pinned in the section, but `verification/claim/after-v5.json`,
   `verification/claim/canary.json`, `verification/placebo/before.json` and
   `verification/freeze/control-v4blind.json` record only `counterSha256` (the counter), not the
   driver's sha256. A receipt therefore cannot prove which driver bytes produced its tally. The
   pin I recomputed matches the section, so today's receipts are consistent with the pinned driver,
   but the receipts themselves would not detect a driver swap.
3. **The section's C1 "After" line is still the frozen declaration, not the measured state.** The
   declaration text says the frozen counter v5 "witnesses **27/27**", while the claim receipt
   `verification/claim/after-v5.json` records `witnessed = 23`, `ok = False`,
   `verdict = witnessed 23/27 notMet=23 build met 3/3`, with the four `casememo-*` controls in
   `metNames` (not witnessed). The section's own text says it is "not edited" after the freeze, so
   the closure measurement (and the G6 fix that would move 23→27) is what has to reconcile this —
   not this seat. Flagged because the section reads as a claim of 27/27 while the only claim receipt
   under `verification/claim/` says 23/27.

## 7. Files written by this seat

- `.ufo/waves/round-44/w2/SonicPins.md` — this report (the only file written in the lane repo).
- `/fast/scratch/hyaku/kake-r44/SonicPins/pin-check.txt` — raw transcript of the consolidated
  pin-check command (scratch only).
- `/fast/scratch/hyaku/kake-r44/SonicPins/pin-table.txt` — raw transcript of the generated pin table
  (scratch only).

No lane file other than this report was written; no file was modified, deleted, committed, staged,
or pushed; no tool was installed or upgraded (no pacman/uv/npm transaction was performed).

## 8. Commands run (exact)

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
git status --short
git diff --stat SCORECARD.md ; git diff --numstat SCORECARD.md
git diff SCORECARD.md
git diff SCORECARD.md | grep -oE '[0-9a-f]{8,64}' | sort -u
git diff SCORECARD.md | grep -oE '`[^`]*`' | grep -E '\.(py|tsv|json|txt|md)' | sort -u
sha256sum .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_placebo.py \
          .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/controls-27.tsv \
          .ufo/waves/round-44/controls-canary.tsv .ufo/waves/round-44/ledger-quotes.json \
          .ufo/waves/round-44/build_v5.py .ufo/waves/round-44/c44_probe.py scripts/sitemap_audit.py
git show 020bc4574729ed674299f6cab02faac1582d9464:scripts/sitemap_audit.py | sha256sum
git diff --stat 020bc4574729ed674299f6cab02faac1582d9464 -- scripts/sitemap_audit.py
git show 1ef7a0e95f6884dd113fe583a997c633fe330ddd:scripts/sitemap_audit.py | sha256sum
git show 8eb121c81ffebada064eefcabcd94dd2303d646f:scripts/sitemap_audit.py | sha256sum
awk -F'\t' 'NR>1{print $5"  "$4}' .ufo/waves/round-44/controls-27.tsv | sha256sum -c -
awk -F'\t' 'NR>1{print $5"  "$4}' .ufo/waves/round-44/controls-canary.tsv | sha256sum -c -
python3 -B .ufo/waves/round-44/build_v5.py --check
python3 -B .ufo/waves/round-44/c44_audit.py --selftest
python3 -B scripts/ledger_latest_check.py --root .
python3 -B scripts/ledger_latest_check.py --selftest
sha256sum .ufo/waves/round-44/classes/g*.py .ufo/waves/round-44/classes-placebo/*.py
grep -n "def semantic_witness" -A 14 .ufo/waves/round-44/c44_audit.py
grep -n "buildport-m6" .ufo/waves/round-44/controls-27.tsv
awk 'NR==303||NR==304{printf "%d: %s\n", NR, $0}' .ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py
python3 -c "<receipt counterSha256 vs live counter; after-v5 rows vs manifest pins; master receipt derivations>"
git ls-tree -r master --name-only | grep l1-rescores
git show master:.ufo/waves/round-43/verification/freeze/ref41-base.json
git show master:.ufo/waves/round-43/verification/freeze/build-1.json   (and -2, -3)
```

## 9. Unrun checks / limits of this seat

- I did **not** re-run the C1 counting command (the full `--classes v5` audit over 27 controls, or
  the placebo/v4-support/canary audits). Those are the wave-2 executor seats' items
  (`ExecAfterBaseline`, `ExecV4Support`, `ExecCanary`) and each takes many minutes; this seat's
  item is the pin check. My receipt reading is of the *existing* receipts, not a fresh run.
- I did **not** verify the four `casememo-*` G6 witnesses under any seed; the G6 class module is
  wave-2 `ExecG6FoldFix`'s territory and its bytes may change after this report is filed.
- Receipts `verification/claim/placebo-before.json` and `verification/claim/v4-support.json` were
  **absent** when I read the directory at check time (only `placebo-before.txt` and `v4-support.txt`
  stubs existed, both 0 bytes). The placebo receipt I cited instead is the inherited
  `verification/placebo/before.json`. Reported as observed, not inferred.
- Everything in this report is scoped to the **uncommitted** round-44 section of `SCORECARD.md`
  (`git diff` against `HEAD` = `18cb2c2`); no round-44 file is tracked in git yet
  (`git ls-files .ufo/waves/round-44 | wc -l` → 0), so "the pinned bytes" are worktree bytes.

Report: .ufo/waves/round-44/w2/SonicPins.md
