# ExecC1History

Claim C1 data walk. Method: `git clone -q --shared` of the lane under `/fast/scratch/hyaku/kake-r61/ExecC1History/clone`
(scratch removed at exit; cited artifacts copied to `ExecC1History.files/`); read-only git plumbing only, no lane writes.
Walk: first-parent chain of base `9f07731a873585e655a6518233ea39f5d9fb8204` = **371 commits** (root
`11261443ec6a1748fdeab9c3fc85e7f6c06ed530` → base), one merge (`5009ecaa`, 2026-10-19); every one of the 144 frozen
population paths resolved with `git ls-tree` per commit and blobs read with `git cat-file` (never the worktree).
Rules applied literally as the contract writes them (receipt grammar `(?im)^\s*#\s*receipt\s*:|EXIT=|^VERDICT:`;
result span = set of lines matching `(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)`).
Raw table: `ExecC1History.files/events.tsv` (header + 12 rows, 5 columns, tab-clean); per-event span deltas, commit
subjects and reverse-chronological order in `ExecC1History.files/disclosure-candidates.json`; population split in
`ExecC1History.files/population-split.txt`; script in `ExecC1History.files/walk_lineage.py`.

## EVENTS:

**12 events, 9 distinct files, all `kind=rewrite`, `pending_filled=0`.** Distribution: round-52 = 5, round-54 = 2,
round-55 = 2, round-56 = 2, round-57 = 1. Commits: `20217f23`(1), `ad06cb8a`(2), `955e3d7b`(2), `a631cc02`(1),
`8e408e00`(1), `fd91527a`(1), `a4a890cf`(3), `1ae8de5d`(1). Candidates behind this: 163 raw `(path,commit)` blob
pairs on the first-parent chain = 144 first-adds (excluded by the rule, "after the commit that first added the file")
+ 19 post-add blob changes; of those 19, 12 change the result span (events) and 7 do not (see NOTES 3).
Validation: an independent derivation (`git log --first-parent --raw --no-renames`, no simplification) reproduces the
same 144 A / 19 M split; every event's `parent_commit` equals its chain predecessor; 0 events at the merge commit
(0 population paths differ merge-vs-first-parent); 0 deleted-then-re-added population paths; 0 missing at base.

Reverse-chronological, verbatim (full line text in events.tsv; the three `c1-mutation-ladder.json` rows abbreviate
their 18 removed / 18 added span lines as `…`):

1. `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` `20217f23eca15862febe14545523832e21584106` rewrite, parent `31b61a4ddfcade92c108ff3786b8e9770bc8da31`
   `+C1 receipt-pins undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=3 scorecard_pin=1 met=True  (met: undisclosed_relabels == 0 AND phantom_errata == 0 AND deleted_receipts == 0 AND new_relabelled == 0 AND new_unpinned == 0 AND new_receipts == 3 AND scorecard_pin == 1)`
2. `.ufo/waves/round-56/controls/after-c2-quote-truth.txt` `ad06cb8a17bda28f0691b95aecda13cd4708ea6c` rewrite, parent `4cb225fb032b04166fb0232bc98a7bcce72675ec`
   `-revision: f8438a282d5946b386812d784cc617edcbc9201d` → `+revision: 4cb225fb032b04166fb0232bc98a7bcce72675ec`
3. `.ufo/waves/round-56/controls/after-c1-selftally.txt` `ad06cb8a17bda28f0691b95aecda13cd4708ea6c` rewrite, same parent
   `-revision: f8438a282d5946b386812d784cc617edcbc9201d` → `+revision: 4cb225fb032b04166fb0232bc98a7bcce72675ec`
4. `.ufo/waves/round-55/controls/after-c2-quote-truth.txt` `955e3d7bd6d1eff5060e4cebbed51891bb53027a` rewrite, parent `64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6`
   `-revision: faf9abe81d1ef5925733f756a918527483073fe8` → `+revision: 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6`
5. `.ufo/waves/round-55/controls/after-c1-readme-index.txt` `955e3d7bd6d1eff5060e4cebbed51891bb53027a` rewrite, same parent
   `-revision: faf9abe81d1ef5925733f756a918527483073fe8` → `+revision: 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6`
6. `.ufo/waves/round-54/controls/c1-selftest.txt` `a631cc0246b97f2a949d61186c7466468faf94d6` rewrite, parent `a0a4fd482700110600b0327c2fce1a270b272136`
   `+ok correction_removed_render: exit 1 (met=False) expected 1` / `+ok unrelated_marker: exit 1 (met=False) expected 1` (append only)
7. `.ufo/waves/round-54/controls/c1-selftest.txt` `8e408e00fbe1c5908df62ba79e78c944bda479e2` rewrite, parent `acae1dccab8a19d9494566b3e9fa564a898694fe`
   `+ok correction_before_render: exit 1 (met=False) expected 1` / `+ok correction_wrong_polarity: exit 1 (met=False) expected 1` (append only)
8. `.ufo/waves/round-52/control/c1-mutation-ladder.json` `fd91527a286086c1f4e6d4f44f715a907f041b5d` rewrite, parent `3994101dba28896830604fd0b08c7f00faca8ed6`
   `-"old_tail": "  revision: 09868888104db4fc3e528d2ec5ca59d917dcaf54"` … (18 removed / 18 added `"old_tail"` `revision:` strings; first removals `098688…`, `0e3c9e…`, first additions `0141f0…`, `2ae089…`)
9. `.ufo/waves/round-52/control/c2-quote-real.txt` `a4a890cf1381a194891689dcbba0bf524350926b` rewrite, parent `1ae8de5d4dee8300624b0db2a94497ff905942c5`
   `-revision: 3a50ae4321e64856229c7cd0d39d3557b204d489` → `+revision: 1ae8de5d4dee8300624b0db2a94497ff905942c5`
10. `.ufo/waves/round-52/control/c1-mutation-ladder.json` `a4a890cf1381a194891689dcbba0bf524350926b` rewrite, parent `1ae8de5d4dee8300624b0db2a94497ff905942c5`
    `-"old_tail": "  revision: 05643750f12344f43bba001ca2252b0e62ba3a53"` … (18 removed / 18 added; first additions `098688…`, `0e3c9e…`)
11. `.ufo/waves/round-52/control/c1-ledger-real.txt` `a4a890cf1381a194891689dcbba0bf524350926b` rewrite, same parent
    `-revision: 3a50ae4321e64856229c7cd0d39d3557b204d489` → `+revision: 1ae8de5d4dee8300624b0db2a94497ff905942c5`
12. `.ufo/waves/round-52/control/c1-mutation-ladder.json` `1ae8de5d4dee8300624b0db2a94497ff905942c5` rewrite, parent `3a50ae4321e64856229c7cd0d39d3557b204d489`
    `-"old_tail": "  revision: 220eddc445b40a3ef56401c67cdc60ca98868d3d"` … (18 removed / 18 added; first additions `056437…`, `1e4439…`)

Span churn total: 60 lines removed, 65 added; the three mutation-ladder rows are 54/54 of that.

## NON-RECEIPTS:

**49 of 144** population files never match the receipt grammar under the contract-literal reading (regexes carry
`(?im)`, i.e. case-insensitive): 18 `.json` fixtures/manifests (round-37 `retained/controls/c2/*` ×8, their round-48
`assimilation/validate/` copies ×8, round-40 `CtlKeyFinder/selftest_table.json` and its round-48 copy) + 31 `.txt`
census/rows/before-after/selftest logs (round-51 c1/c2 before-base and junk ×4, round-52 census/registry-rows ×3,
round-55/56/57/58/59/60 census and selftest files ×24).
Case sensitivity is the dividing line: **11 files flip to non-receipt** if the grammar is read case-sensitively
(they match only on lowercase `exit=` / `verdict:`): round-52 `census-before.txt`, round-55 `census-after.txt`,
`census-before.txt`, round-57 `census-after.txt`, round-58 `c1-selftest-v1.txt`, `c1-selftest-v2.txt`,
`c2-selftest-v2.txt`, `c3-selftest-v2.txt`, round-59 `a2-selftests-rerun.txt`, `c2-selftest-v2.txt`, round-60
`validate-append.txt`. Case-sensitive reading ⇒ 84 receipts / 60 non-receipts. Of the 95 literal hits, only 16 carry
the `# receipt:` header form; 77 match on `EXIT=`/`exit=`, 2 on `VERDICT:`.

## RENAMES:

**0** population paths have a history ending in a rename. Whole-chain first-parent rename scan
(`git log --first-parent -M --diff-filter=R`) finds exactly 2 pairs, both round-23 commit `4e7dd1d4`:
`.ufo/waves/round-22/residual/misroot/err.txt` and `.../out.txt` (R100) — neither source nor destination is a population
path, so no walk is truncated by a rename boundary. (Renames elsewhere in the repo are therefore irrelevant to C1 at
base; if a future round renames a receipt the old path's walk stops at the rename and the new path starts fresh.)

## NOTES:

1. **The literal `pending` rule misses the only real pending receipt.** Result span is a set of *lines* matching the
   anchored forms; the r57 placeholder's first version
   (`31b61a4ddfcade92c108ff3786b8e9770bc8da31:.ufo/waves/round-57/controls/after-c1-receipt-pins.txt`) is three lines —
   `pending`, `  revision: 32754df7…`, `EXIT=0`. The word `pending` sits on a bare body line, so span-pending receipts
   across the whole population = **0**, and no `pending_filled` event exists at base; `20217f23` is classified
   `rewrite`. If "the first version's result span contains pending" were instead tested over the whole first version,
   exactly one event reclassifies (`20217f23` → `pending_filled`) and no other event changes: the four other
   body-only `pending` files (round-52 `drift-before.txt`, `sweep-after.txt`, round-58 `c1-selftest-v1.txt`,
   `c1-selftest-v2.txt`) have no post-add span change. The tool must state which reading it implements; L7's fixture
   (pending inside `met=`/`EXIT=` text) is satisfiable either way, so the fixture cannot distinguish them.
   [INFERENCE] the C1 owner will want the tool docstring to pin this, since the real lane's flagship case hinges on it.
2. **`receipts=` in the summary line is ambiguous and the counter's R2 asserts 144.** Literal grammar matching yields 95
   receipts walked; the counter's R2 shape check expects `receipts=144`. [INFERENCE] that only holds if `receipts=`
   counts frozen population members, not grammar-matched receipts — a builder implementing it as matched receipts will
   print 95 and fail the R2 shape assert. Recommendation: print population members and a separate matched count (or
   state the definition in the tool docstring before the counter freezes).
3. **The span filter misses 6 of 7 real post-add modifications.** The 7 blob changes with an identical result span:
   round-52 `c2-quote-selftest.txt` (`fixture revision 3a50ae4321e6` → `1ae8de5d4dee`, invisible because
   `revision\s*[:=]` needs a colon/equals), round-54 `base-c2-ops-debt.txt` (`uncovered=4` → `uncovered=7`, plus a
   `cited=`/`uncovered_names=` list growth), round-54 `sources-census.txt` (provenance sentence gains "measured
   against lane tip a631cc02…"), round-54 `base-c1-s374.txt` (PASS/FAIL reason prose only), round-55
   `c1-selftest-v2.txt` (`32/32` → `44/44`), round-55 `c2-selftest.txt` (`fixture revision faf9abe…` → `64c0ce1…`),
   round-56 `c2-selftest.txt` (`67/67` → `86/86`). So a receipt whose recorded count or revision pin is rewritten in
   prose form is undetectable by the frozen span regex — the class exists in the real history, six times. Not a build
   defect (the rule is frozen); it is the honest limit of the claim and the obvious w2 attack surface.
4. **3 of the 12 events are grammar false positives from fixture data.** `c1-mutation-ladder.json` is a JSON control
   manifest whose `"old_tail": "  revision: <sha>"` strings match `revision\s*[:=]`; every regeneration moves 18 span
   lines, so the single file contributes 3 events (and 54 of the 60/65 span-line churn). At base the tool therefore
   reports 12 events of which 3 are fixture-data churn, not receipt relabels. Treating the file as a receipt is
   contract-correct (it matches `EXIT=` inside a JSON string value), so the only remedies are a disclosure entry or a
   version-2 narrowing (a loosening, allowed only by naming it in § Counter versions).
5. **Disclosures: all 12 events are currently undisclosed.** `.ufo/receipt-disclosures.json` does not exist at base nor
   in the lane worktree (checked 2026-10-27), so a tool run at base prints `undisclosed=12 met=False`. For the measured
   revision's R2 (`undisclosed=0`) the registry must carry exactly these 12 `(path, commit)` pairs; the matching key is
   `(path, commit)` only (kind is not compared), but writing the kind the tool computes (`rewrite`, including the r57
   pair) keeps prose and tool consistent. `phantom_disclosure` stays 0 as long as no entry names a non-event pair.
   Candidates with the observed change, ready to be given disclosure prose by the C1 owner: `disclosure-candidates.json`.
6. The round's cited defects are reproducible from data: r56 relabel = `ad06cb8a` on two receipts
   (`after-c1-selftally.txt`, `after-c2-quote-truth.txt`); r57 pending-then-filled = `20217f23` on
   `after-c1-receipt-pins.txt`. r55 shows the same relabel pattern at `955e3d7b` (two receipts), which the round-60
   record does not name — worth a lesson line, not a claim change.
7. Round-61 headroom: the new round-61 receipts are files outside the frozen list, so they surface as `extra_member`,
   not as events; only a rewrite of one of the 144 frozen paths after base adds events (none so far — the walk ends at
   base by assignment).
8. Tooling: nothing installed, no `pacman` invocation, no host service touched; `uv`/`npx`/binary channels unused.
   Execution: 371 `ls-tree` calls + blob reads; total wall clock under a second per pass.
9. Unverified-by-construction: the tool `scripts/receipt_lineage.py` does not exist yet, so nothing here was produced
   by running it; every statement above comes from my own first-parent walk of committed objects. Cross-check against
   the tool when it lands is the w2 job.

VERDICT: Base-revision receipt population walks clean structurally (144 members, 0 renames, 0 missing) but carries 12 post-add result-span rewrites across 9 files (3 of them fixture-JSON churn), 0 pending_filled under the literal span rule, and 6 semantically meaningful rewrites the frozen span regex cannot see; all 12 events need disclosure entries for a met run, and the `receipts=`/case-sensitivity/pending definitions must be pinned before the counters freeze.
