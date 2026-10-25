# ExecQuoteCounterMutants — round 51, wave 1 (C2 counter mutation lab)

Seat: `L1Kake51.ExecQuoteCounterMutants-2`. Scope: attack `c51_quote_truth.py` and the
committed corpus bytes it reads; write only this file.

**Headline.** All five required mutants and five further rejection mutants are killed (exit 1,
failing condition named). Six probes survive, bounding what the 8/8 actually proves. Separately,
the committed *pre-append snapshot* at revision `9d13768` is a copy of the **post**-append tree,
and the in-flight worktree repair left a `census-exit.txt` that **C7 rejects byte-for-byte**
(`exit=0` instead of `0`) — committing it as-is flips C2 to 7/8.

## 1. Method (reproducible, /tmp only)

Lab: `/tmp/r51-mut-l2/`. Harness: `/tmp/r51-mut-l2/mutants.py`. Raw results:
`/tmp/r51-mut-l2/mutant-results.json`, `run.log`, `run2.log`.

1. Extracted the committed bytes with `git show <rev>:<path>` into `/tmp/r51-mut-l2/base/` for the
   11 paths the counter reads:
   `corpus/SOURCES.md`, `corpus/lessons/round-51.md`, the two `corpus/knowledge/*.md` entries, the
   two `.ufo/waves/round-51/sources/S26{2,3}.html` bodies, `sources/receipts.json`, the
   `assimilation/pre-append/` mirror registry and its three census receipt files.
2. Built a two-commit replica repo at `/tmp/r51-mut-l2/repo` so the counter's `git log
   --diff-filter=A` / `merge-base --is-ancestor` path is exercised:
   - commit A `6a4935d7990afef8fe7667af486108472866cb60` — registry at `19a99bd` (pre-append,
     143 rows) at `corpus/SOURCES.md`; the mirror blob and census receipt as committed at
     `19a99bd`; no entries, no lesson, no receipts.
   - commit B `0c8c879acdb86e3b22aabd164c2c924f9de1bfbe` — the measured-revision tree.
3. Baseline on the replica: `C2 quote-truth 8/8 met=True`, exit 0, reproduced twice. The replica
   is therefore byte-faithful for this measurement.
4. Each mutant = `git reset --hard B` + one asserted text mutation (`assert` on occurrence count,
   so a no-op mutation fails loudly) + one commit + one counter run.

Nothing under the lane was written except this report. No `git` mutation, no `jj`, no installs.

## 2. Required mutants — all rejected (exit 1)

| # | mutant | mutation | exit | failing condition | counter note |
|---|--------|----------|------|-------------------|--------------|
| a | `a_swap_gate_quotes` | S262 ↔ S263 Gate quote strings in `corpus/lessons/round-51.md` | **1** | `C5_gate_quote_truth` | S262 and S263: "Gate quote is not a raw substring of the retained body" |
| b | `b_corrupt_sha256` | S263 receipt `sha256` first hex digit `6`→`0` | **1** | `C6_receipt_pins` | "receipt sha256 0afbdc82… != body 6afbdc82…" |
| c | `c_drop_used_by` | S263 row `used-by` cell emptied (its only id dropped) | **1** | `C4_used_by` | "used-by is [], expected exactly ['corpus/knowledge/crawler-identity.md']" |
| d | `d_row_12_cells` | S262 row gains a 12th cell | **1** | `C3_row_shape` | "registry row has 12 cells, expected 11" |
| e | `e_receipt_url_other_row` | S262 receipt `url` → S263's googlebot URL | **1** | `C6_receipt_pins` | "receipt URL is not the registry row's URL" |

Mutant commits: a `863b43fb…`, b `3b5c8fa2…`, c `77b1b2cc…`, d `ac69ec6c…`, e `3f7bb54c…`.

## 3. Further rejection mutants — all killed

| mutant | mutation | exit | failing condition |
|--------|----------|------|-------------------|
| `f_swap_row_ids` | registry row ids S262 ↔ S263 swapped | **1** | `C4_used_by`, `C6_receipt_pins` (both rows) |
| `g_entry_wrong_id` | S263 entry's below-header citations rewritten to S262 | **1** | `C2_entry_cites_id` |
| `j_registry_row_url_other` | S262 row's URL cell → S263's URL | **1** | `C6_receipt_pins` |
| `k_census_no_file` | `--file` deleted from `census-argv.txt` | **1** | `C7_validate_before_append` |
| `u_corrected_exit_format` | `census-exit.txt` = `exit=0\n` (the in-flight repair's bytes) | **1** | `C7_validate_before_append`, note "census exit is 'exit=0', expected '0'" |

Ten mutants, ten rejections, each attributed to the condition it should trip. No mutant produced a
different failing condition than designed, and none produced exit 2 or a crash.

## 4. Survivors — what the 8/8 does *not* cover

| probe | mutation | exit | reading |
|-------|----------|------|---------|
| `m_prefix_url_probe` | S262 receipt URL truncated to `…/canonicalizatio` | **0** | C6 uses `receipt["url"] not in row[1]` (substring). A *different, non-resolving* URL that is a prefix of the row URL passes. Divergence between receipt and registry row is exactly what C6 claims to catch; the test is containment, not equality. |
| `p_duplicate_row_probe` | S262 row duplicated verbatim in the registry table | **0** | `parse_registry` is a dict keyed by id; the last row wins, duplicates are invisible. The census owns E03, but C2's own parser cannot see a duplicated row. |
| `r_receipt_fetched_at_probe` | receipts `fetchedAt` → `2020-01-01T00:00:00-03:00` | **0** | No condition reads `fetchedAt`. C2 cannot falsify the *date* of re-grounding. |
| `s_http_status_probe` | S263 receipt `httpStatus` → `404` | **0** | No condition reads `httpStatus`. A receipt claiming a failed fetch still pins its sha256 and passes. |
| `t_lesson_provenance_probe` | lesson S262 Gate line relabelled with S263's URL, sha256 and byte count | **0** | `gate_quote()` extracts only the quoted span; the lesson's own provenance fields are unchecked free text. |
| `v_corrected_mirror_neutral` | mirror replaced by the true pre-append registry (143 rows) | **0** | The score is invariant to the mirror's bytes: 8/8 before and after the repair. C7 reads the receipt's shape, C8 reads the live registry at the mirror commit — neither opens the mirror file at the measured revision. |

Severity: `m` is the only one that defeats a sentence C6 actually asserts (URL agreement) — it is a
containment-vs-equality bug worth fixing in a future counter. `p` is a registry-integrity hole
mitigated by census E03. `r`, `s`, `t` are outside the frozen eight conditions; they bound the
claim, they are not counter bugs. `v` is the structural gap that let the defect in §5 pass.

## 5. Lane finding — the committed "pre-append" snapshot is post-append

Found while building the replica: my first replica put the mirror file only in the append commit,
and C8 failed with "S262: the mirror already carries the row". I then measured the committed blobs
directly (read-only commands, all run in the lane root):

```
$ git show 9d13768:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | sha256sum
4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3
$ git show 9d13768:corpus/SOURCES.md | sha256sum
4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3
$ git show 19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | sha256sum
4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3
$ git show 19a99bd:corpus/SOURCES.md | sha256sum
cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117
```

Row/line counts: mirror blob at `19a99bd` = **145 rows / 258 lines** (blob `9e2a2217…`, 135068 B);
live registry at `19a99bd` = **143 rows / 256 lines** (blob `cd448eaf…`, 133780 B); tip registry =
145/258. `git diff` between the two `19a99bd` versions is exactly the two added rows.

The snapshot is a whole-tree copy, not just a registry copy, and the entries were in it before the
append:

```
$ git ls-tree -r 19a99bd -- .ufo/.../pre-append/corpus/knowledge/ | grep -E 'canonical-selection|crawler-identity'
100644 blob 6fee23e433ca034a1ba37708ff203a402bc2bd93  .../canonical-selection.md
100644 blob cac1358807125562d927cf09a962d188cbb00c03  .../crawler-identity.md
$ git ls-tree 9d13768 -- corpus/knowledge/canonical-selection.md corpus/knowledge/crawler-identity.md
100644 blob 6fee23e4…  corpus/knowledge/canonical-selection.md
100644 blob cac13588…  corpus/knowledge/crawler-identity.md
```

Same blobs: the "pre-append" snapshot at the mirror commit already contained both admitted entries
and both registry rows, and `census-argv.txt` names that snapshot's `corpus/SOURCES.md`. Because
`resolve_targets()` in `scripts/sources-census.sh:501` derives the validation base as
`dirname(file)/..`, the censused `used-by` paths resolved *inside the snapshot* — which is why the
receipt carries W04 lines only and no E11. So the committed C7 receipt proves "these post-append
bytes are census-clean", not "the pre-append registry was clean before the append".

What this does and does not mean:

- No quote, row shape, receipt pin, or condition sentence is false. `c51_quote_truth.py` at
  `9d13768` is 8/8, reproduced independently (twice) at exit 0.
- The census found no E03/E04 for S262/S263 on those bytes (`grep -cE 'E0[34]' census-stdout.txt`
  → 0), so the append itself is census-clean; my own `--file` census of the tip registry copy
  produced the identical 12 W04 lines and zero E03/E04 (it also emitted E11 for every used-by,
  because with an out-of-tree `--file` the base becomes `dirname(file)/..` = `/tmp` — the same
  base-resolution rule that let the mirror receipt pass).
- C8 is worded over *the registry at the mirror commit*, so it cannot see that the mirror bytes
  contradict their name. That is the structural reason the defect passed the frozen predicate.

A concurrent seat reached the same fact in this wave; the commands above are mine and were run
independently, not taken from that report.

## 6. In-flight repair — one byte away from breaking C7

During this seat's run the worktree changed (not by me):

```
 M .ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md   (mtime 2026-10-25 03:36:34 -0300)
 M .ufo/waves/round-51/assimilation/pre-append/census-exit.txt
?? .ufo/waves/round-51/assimilation/pre-append/census-correction.txt
```

The mirror was correctly rewritten to the true pre-append registry (`sha256 cd9ee4cf…`, 143 rows).
The replacement receipt, however, writes the exit as:

```
$ od -c .ufo/waves/round-51/assimilation/pre-append/census-exit.txt
0000000   e   x   i   t   =   0  \n
```

while the committed file was `0\n` and C7 requires `exit_text.strip() == "0"`. Probe
`u_corrected_exit_format` reproduces exactly this byte content on top of the good replica:
**exit 1, `C7_validate_before_append`, "pre-append census exit is 'exit=0', expected '0'"** — C2
would score 7/8 and the claim would be judged unmet. The receipt must contain `0\n` (or C7 must be
changed, which is a rule change and would forfeit the frozen predicate).

The mirror repair alone is score-neutral (`v_corrected_mirror_neutral`: exit 0, 8/8), which is
consistent with §5: the counter never opens that file at the measured revision.

## 7. What 8/8 proves, precisely

It proves: the two entries exist and cite their ids; both registry rows are 11 cells with
`mined`/`2026-10-24`/`180d`; `used-by` matches exactly; each Gate quote is 6–25 words and a raw
substring of a retained body whose sha256 and URL are pinned in the receipt; the pre-append census
receipt has the required shape and no E03/E04; and the mirror commit is a strict ancestor while the
live registry there lacks the ids.

It does **not** prove that the bodies were fetched this round (`fetchedAt`/`httpStatus` unread), that
the lesson's provenance fields are true, that the mirror file is a pre-append snapshot, or that a
receipt URL equals the row URL rather than being contained in it. On the freshness axis the claim
rests on the sha256 pin plus the round's own receipts — not on any date the counter verifies.

## 8. Files, tooling, limits

- Written by this seat: this report only. Lab under `/tmp/r51-mut-l2/` (harness, replica repo,
  extracted bytes, results JSON, logs) is a convenience copy: Appendix A carries the extraction
  recipe and every mutation delta, so no finding depends on `/tmp` surviving.
- No tools installed or upgraded; no pacman/uv/npm transactions; no network.
- Lane worktree was dirty before and after (26 porcelain entries, including wave-1 artifacts); I
  did not touch it and did not read or copy any credential/token material.
- Could not verify: whether the sibling repair will be committed with `exit=0` or corrected — it is
  uncommitted at this writing, and `census-correction.txt` states the counter is unchanged, which is
  precisely why the `exit=0` byte content is a live hazard.

## Appendix A — reproduction without the /tmp lab

The `/tmp/r51-mut-l2/` lab is a convenience copy; the lane's live evidence is committed git bytes,
and every mutant delta is below, so this report reproduces alone. `REV=9d13768…` below means the
measured revision.

Recipe:

```
# 1. extract the eleven committed inputs the counter reads
git -C <lane> show $REV:<path> > <tree>/<path>
#    paths: corpus/SOURCES.md, corpus/lessons/round-51.md,
#    corpus/knowledge/{canonical-selection,crawler-identity}.md,
#    .ufo/waves/round-51/sources/{S262.html,S263.html,receipts.json},
#    .ufo/waves/round-51/assimilation/pre-append/{corpus/SOURCES.md,census-argv.txt,
#    census-stdout.txt,census-exit.txt}
# 2. commit A: registry bytes of 19a99bd at corpus/SOURCES.md + the committed mirror blob and
#    census receipts; commit B: the full extracted tree.
# 3. baseline: python3 -B c51_quote_truth.py --root <tree> --revision <B>   -> 8/8, exit 0
# 4. per mutant: reset --hard <B>, apply one delta below, commit, run with --revision HEAD
```

Deltas (`old -> new`, one occurrence unless stated):

| mutant | file | delta |
|---|---|---|
| a | lesson | swap `"indicating a canonical preference is a hint, not a rule"` and `"Googlebot is the generic name for two types of"` |
| b | receipts | S263 `"sha256": "6afbdc82…"` -> `"0afbdc82…"` (first hex digit) |
| c | registry | S263 row cell 11 (used-by) -> empty string |
| d | registry | S262 row: append cell `stray-twelfth-cell` (11 -> 12 cells) |
| e | receipts | S262 `"url"`: `…/crawling-indexing/canonicalization` -> `…/crawling-indexing/googlebot` |
| f | registry | swap `cells[1]` on both rows: `S262`<->`S263` |
| g | `crawler-identity.md` | every `S263` after the first 8 lines -> `S262` |
| j | registry | S262 row URL cell: canonicalization -> googlebot |
| k | `census-argv.txt` | delete the substring ` --file` |
| m | receipts | S262 `"url"` -> `…/crawling-indexing/canonicalizatio` (dropped final `n`) |
| p | registry | insert the verbatim `S262` row immediately after the `S286` row |
| r | receipts | `"fetchedAt": "2026-10-24T23:16:49-03:00"` -> `"2020-01-01T00:00:00-03:00"` |
| s | receipts | first `"httpStatus": 200` inside the `"S263"` block -> `404` |
| t | lesson | on the `- S262 —` line: canonicalization URL -> googlebot URL, `79222433…` -> `6afbdc82…`, `174926 bytes` -> `175561 bytes` |
| u | `census-exit.txt` | `0\n` -> `exit=0\n` |
| v | mirror | `corpus/SOURCES.md` content of `19a99bd` (`sha256 cd9ee4cf…`, 143 rows) |

Expected outcomes are invariant: a,b,c,d,e,f,g,j,k,u exit 1 with the conditions in §2–§3;
m,p,r,s,t,v exit 0.
