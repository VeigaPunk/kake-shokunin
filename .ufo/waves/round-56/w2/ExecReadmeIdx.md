# ExecReadmeIdx

Seat: README coverage-map audit, round-56 W2 falsify wave. Revision under attack:
`a450e43e696d032e3ac308383f6b3394e0c92860`; base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`.
All runs in a throwaway clone `git clone -q --no-checkout … && git checkout -q a450e43…`
(`git rev-parse --show-toplevel` = the mktemp dir); the lane repo, its index and jj state were not
touched, no lane file edited. Own checker: `/tmp/readmeidx_audit.py` (git `ls-tree`/`show` at the
revision, no worktree reads). Mutant revisions named below exist only in that throwaway clone
(`-c user.name=selftest -c user.email=selftest@local`), reset after each probe.

## COUNTER:

Command (as assigned), at the tip, in the clone:

    python3 -B .ufo/waves/round-55/c55_readme_index.py --root $PWD --revision a450e43e696d032e3ac308383f6b3394e0c92860
    C1 readme-index index_mismatches=0 knowledge_files=52 met=True  (met: index_mismatches == 0 AND knowledge_files >= 46)
      unindexed=0 multi=0 thin=0 duplicate=0 head_changed=0 deleted=0 dangling=0 coverage_rows=54
      revision: a450e43e696d032e3ac308383f6b3394e0c92860
    EXIT=0

Selftest in the same clone: `--selftest` → `c55 readme-index selftest: 44/44`, exit 0 (matches the
44-fixture claim in `SKILL.md:1233`).

Committed-bytes authority probe (attacks `c55_readme_index.py:7` "no worktree reads"): removing the
`knowledge/keeper-timer-inert.md` index row in the **worktree only**, uncommitted → counter still
`index_mismatches=0 … met=True`, exit 0; worktree then restored. Claim holds.

Falsification mutants, each one commit in the clone, counter re-run at the mutant revision:

| # | mutation | mutant rev | counter | caught? |
|---|---|---|---|---|
| M1 | delete the keeper-timer index row | `4697e2e7f854` | `unindexed=1` (`keeper-timer-inert.md`) exit 1 | yes |
| M2 | add `knowledge/does-not-exist.md` row to the Frontier ground map | `300b3ef532e9` | `dangling=1` exit 1 | yes |
| M3 | Entry cell `mirror-pitfalls.md` → `.mdx` | `581716c40454` | `unindexed=1`, `dangling=0`, exit 1 | yes (via unindexed, not dangling) |
| M4 | three knowledge refs in one Entry cell | `4fe78fd1e13b` | `multi=1` exit 1 | yes |
| M6 | prepend a comment line to `knowledge/keeper-timer-inert.md` | `f0fd54b72069` | `head_changed=1` exit 1 | yes |
| M7 | copy the Publish-channels Coverage cell into the Drift-detection row | `b143616918a4` | `thin=1 duplicate=1` exit 1 | yes |
| M10 | replace the Mirror-pitfalls Coverage cell with `tbd` | `37552e539a41` | `thin=1` exit 1 | yes |
| M5 | add `knowledge/does-not-exist.mdx` row to the ground map | `352c22ddf453` | `dangling=0 … met=True` exit 0 | **no — survives** |
| M8 | add `knowledge/gone` (no extension) row to the ground map | `093e39979296` | `dangling=0 … met=True` exit 0 | **no — survives** |
| M9 | delete `knowledge/yahoo-japan-deleted-url-recrawl.md` **and** its index row **and** its name in the ground-map Entries cell | `846e28401d6b` | `knowledge_files=51 … met=True` exit 0 | **no — survives** |

Named limits of the counter (each attacks a stated guarantee, not a live defect at this revision):

1. **`c55_readme_index.py:205-207` (gate), `:64-65` (`EXTS`)** — the `dangling` surface skips any token whose final segment has
   no extension or an extension outside `EXTS` (`md py mjs json sh txt csv yml yaml toml html xml png
   svg jpg jpeg gif pdf log jsonl ndjson tsv`). M5 (`.mdx`) and M8 (no extension) are dead pointers in
   the Frontier ground map that the counter scores as met. The own audit flags M8
   (`DANGLING knowledge/gone`, 81 pointers/53 distinct/1 dangling). No such pointer exists at the tip.
2. **`FLOOR = 46` (line 59) vs the round-56 base population 49** (`git ls-tree -r e48354b7… --
   corpus/knowledge/` = 49 files; tip 52). The `deleted` term pins the 49 base files but nothing pins
   the three post-base round-56 entries: M9 removes one entry wholesale and the predicate still reads
   `met=True` at 51 files. The assignment's "expect 52" is therefore not enforced by the counter.
3. The floor is inherited from the round-55 base, which held exactly 46 files (`git ls-tree -r
   fcaf4b85… -- corpus/knowledge/` = 46); against the round-56 base (49) it is slack by 3, and the
   binding guard is the base-relative `deleted` term, not the floor. `knowledge_files=52` is a
   measurement, not a guarded invariant.

## INDEPENDENT AUDIT:

Own python (no counter import), committed bytes at `a450e43…`:

- `corpus/knowledge/` at the tip: **52** files (49 at base `e48354b7…`, +3 = the round-56 Yahoo trio).
- `corpus/README.md` `## Coverage map` = lines 15–142 (ends before `## Known gaps`, line 143); first
  contiguous table header `Area | Entry | Coverage` (lines 17–18), 54 data rows.
- Every one of the 52 files is named in an Entry cell of exactly one first-table row as
  `` `knowledge/<file>` ``: `unindexed=0`, rows naming a file more than once `multi_named=0`,
  distinct named files 52/52.
- Backticked `knowledge/…` pointers in the **whole** section, Frontier ground map included:
  80 occurrences, 52 distinct, all of the plain form `knowledge/<name>.md|.json` (no brace sets, no
  `:line` suffixes, no `corpus/knowledge/` forms); resolution against `corpus/<pointer>` at the
  revision: **0 dangling**.
- The three r56 entries are each named twice in the section as a whole (their index row plus the
  ground-map Entries cell); only the first table is an index row, so the one-row-per-file count above
  is taken there — same reading as the counter (`coverage_rows=54`).
- README's own base-absence statement ("the round-56 row's three entry paths are absent at its base
  `e48354b7…`") verified: all three absent from the base tree.

## ROW CELL CHECK:

Target: the round-56 Frontier ground-map row at `corpus/README.md:100`, under the subheading
`### Frontier ground map (round 55; round-56 update)` (line 74):

    | Yahoo! JAPAN crawl handling (link-target restriction, deleted URL, non-existent URL) | r56 (lands this round) | `knowledge/yahoo-japan-link-target-crawl-restriction.md` `knowledge/yahoo-japan-deleted-url-recrawl.md` `knowledge/yahoo-japan-nonexistent-url-recrawl.md` | S367 S419 S420 |

Rows cell = `S367 S419 S420`.

`corpus/SOURCES.md` `used-by` evidence at the same revision (registry 158 rows; 156 at base):

- S367 → `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md, corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md`
- S419 → `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md`
- S420 → `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md`

- Rows naming **any** of the three entries = {S367, S419, S420} → **equals the Rows cell exactly**
  (no missing id, no extra id).
- Per entry, the naming row is its own (S419 → S419, S420 → S420, link-target → S367); S367 is the one
  row that also backs a second entry (`…rel-nofollow-semantics.md`), which is consistent with the
  round-52 ground-map row listing S367 for that entry, not a duplicate of the r56 row set.
- S367's used-by is append-only: base = `…rel-nofollow-semantics.md` alone; tip adds
  `…link-target-crawl-restriction.md`, removes nothing. S419/S420 absent from the base registry.
- Every `corpus/knowledge/*.md|json` pointer in every tip `used-by` cell resolves at the tip
  (0 dangling), so the row-set evidence names real files.

## Findings (what each attacks)

1. `corpus/README.md:15-142` vs `corpus/knowledge/` at `a450e43…` — coverage map is complete and
   one-to-one (52/52, 0 unindexed/multi), 0 dangling pointers: no defect found.
2. `corpus/README.md:100` Rows cell vs `corpus/SOURCES.md` used-by — set-equal {S367 S419 S420}:
   no defect found.
3. `c55_readme_index.py:205-207` — dangling surface is extension-gated; dead `.mdx`/extensionless
   `knowledge/…` pointers are invisible (M5, M8 survive). Latent; nothing dead at the tip.
4. `c55_readme_index.py:59` (`FLOOR = 46`) — population floor sits 3 below the round-56 base (49), so a
   post-base entry deleted together with its index row and ground-map mention keeps the predicate met
   at 51 files (M9). The 52-file population is not pinned by the counter.
5. `SKILL.md:1233` row for readme-index-counter — claimed 44 fixtures, selftest printed 44/44: consistent
   (C1 calibration row, cross-checked only).

Not run / not checked by this seat: C1 selftally and C2 quote-truth counters (other seats),
`sources-census.sh validate` (C2's surface), and the `multi` term's row-vs-ref counting beyond M4.

VERDICT: Counter met at the tip (index_mismatches=0, knowledge_files=52, exit 0); own audit confirms 52/52 files indexed once each and 0 dangling pointers, and the r56 ground-map Rows cell equals the SOURCES used-by set {S367 S419 S420}; two latent counter gaps survive as mutants (extension-gated dangling, unpinned 52-file population), neither realized at this revision.
