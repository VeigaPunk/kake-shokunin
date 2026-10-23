# ReviewManifest — r44 w2 review of `controls-27.tsv` against round-43 settle prose

**Verdict: PASS.** The manifest carries exactly the 27 controls the round-43 settle
prose enumerates, with the right family counts; every declared path exists under
`.ufo/waves/round-44/controls-r43/` and every declared sha256 matches the on-disk
bytes. No extra, missing, or mismatched rows.

## Named attack

Extra/missing/mismatch between `controls-27.tsv` and (a) the round-43 "final
kill-rule tally correction" prose (SCORECARD.md §"Round 43 — final kill-rule tally
correction", SCORECARD.md:3385–3396), and (b) the on-disk `controls-r43/` fileset.

## Prose enumeration (SCORECARD.md:3387–3393, verbatim anchor)

> **27 witnessed live-seat controls meet the frozen counter v4 while judging URL
> values differently from the round-41 tool** — CtlHeadTail ×5 (head/tail
> windows), CtlPortLen ×3 (port-length gates), CtlCaseMemo ×4 (case-fold memos),
> CtlRepeat ×5 (band memos), CtlHostTable ×3 (host tables over hosts outside the
> generator's population), CtlPortValue ×2 (port-digit caches), CtlPrefixCache ×1
> (48-cp prefix cache, p48_noreval), and the four build mutants (MutBuildScope
> m4/m5, MutBuildScheme M5, MutBuildPort m6).

Expected: 5+3+4+5+3+2+1+4 = 27 rows.

## What I ran (all under `/home/vgpnk/Projects/shokunin/kake-shokunin`)

### 1. Row count, family census, duplicate scan

```
tail -n +2 .ufo/waves/round-44/controls-27.tsv | wc -l
tail -n +2 .ufo/waves/round-44/controls-27.tsv | cut -f6 | sort | uniq -c   # seat-report col
tail -n +2 .ufo/waves/round-44/controls-27.tsv | cut -f2 | sort | uniq -c   # family col
tail -n +2 .ufo/waves/round-44/controls-27.tsv | cut -f3 | sort | uniq -c   # class col
cut -f1 | sort | uniq -d | wc -l   # dup names; same for f4 paths, f5 shas
```

Output (verbatim):

```
=== rows ===
27
=== by seat report (prose family) ===
      4 w1/CtlCaseMemo.md
      5 w1/CtlHeadTail.md
      3 w1/CtlHostTable.md
      3 w1/CtlPortLen.md
      2 w1/CtlPortValue.md
      1 w1/CtlPrefixCache.md
      5 w1/CtlRepeat.md
      1 w1/MutBuildPort.md
      1 w1/MutBuildScheme.md
      2 w1/MutBuildScope.md
=== by TSV family col ===
      5 band
      2 default_port
      1 empty_path
      4 fold
      3 host
      3 portdigit
      2 portlen
      1 port_scope
      4 prefix
      2 window
=== by class ===
      2 G1
      2 G10
      2 G2
      1 G3
      1 G4
      4 G5
      4 G6
      5 G7
      3 G8
      3 G9
=== dup names ===
0
=== dup paths ===
0
=== dup sha ===
0
```

Seat-report column census matches the prose exactly: CtlHeadTail 5, CtlPortLen 3,
CtlCaseMemo 4, CtlRepeat 5, CtlHostTable 3, CtlPortValue 2, CtlPrefixCache 1, and
build mutants 4 (MutBuildScope 2 = m4/m5, MutBuildScheme 1 = M5, MutBuildPort 1 =
m6). Every row's `control file` column points under
`.ufo/waves/round-44/controls-r43/`. No duplicate name/path/sha.

### 2. sha256 verification (decisive)

```
tail -n +2 .ufo/waves/round-44/controls-27.tsv | awk -F'\t' '{print $5"  "$4}' \
  > /fast/scratch/hyaku/kake-r44/ReviewManifest/manifest.sha256
sha256sum -c /fast/scratch/hyaku/kake-r44/ReviewManifest/manifest.sha256
```

Output (verbatim, truncated to per-file verdicts — all 27 lines):

```
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
EXIT:0
```

27/27 OK, exit 0. (A missing file makes `sha256sum -c` emit FAILED-open plus exit 1;
none occurred — every file exists and hashes match.)

### 3. Extra-file check (directory vs manifest)

```
diff <(tail -n +2 .ufo/waves/round-44/controls-27.tsv | cut -f4 | sed 's|.*/||' | sort) \
     <(ls .ufo/waves/round-44/controls-r43/ | grep -v __pycache__ | sort)
```

Output: empty diff, `DIFF-EXIT:0`. Directory holds exactly the 27 declared files
plus `__pycache__/` (interpreter bytecode cache, not a control — informational
only, not a manifest row candidate).

### 4. Seat-report existence (beyond-scope sanity)

All 10 cited `w1/*.md` reports exist at
`.ufo/waves/round-43/w1/{CtlHeadTail,CtlPortLen,CtlCaseMemo,CtlRepeat,CtlHostTable,CtlPortValue,CtlPrefixCache,MutBuildPort,MutBuildScheme,MutBuildScope}.md`
— confirmed with per-file `[ -f ]` (all `PRESENT`).

## Findings

- **No defect found.** Rows: exactly 27, family counts per prose exactly,
  paths all under `controls-r43/`, all files present, all sha256 match, no
  extras on disk, no duplicates.
- **Observation (not a defect):** the TSV `family` column is the v5 class-family
  grouping, which differs from the prose/seat-report grouping in one cell:
  `portlen-v4` (file `portlen-v4-cache-portlen.py`) sits in `portdigit`/G9 while
  its seat report is `w1/CtlPortLen.md`. The prose groups by seat, not class; the
  row is still one of the 27 and its seat report is CtlPortLen, so the prose
  census holds. Noted so the L1 does not re-derive the family column as a prose
  census — use the seat-report column for that.

## Files written

- `.ufo/waves/round-44/w2/ReviewManifest.md` (this report)
- `/fast/scratch/hyaku/kake-r44/ReviewManifest/manifest.sha256` (scratch manifest fed to `sha256sum -c`)

## Tool installs

None. `sha256sum`, `awk`, `diff`, `sort`, `uniq` from coreutils only; no pacman
transactions (paused host-wide), nothing installed.

## Blockers

None.
