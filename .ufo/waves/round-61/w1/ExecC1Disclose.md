# ExecC1Disclose

Claim C1 (calibration), disclosure-registry half. Work product: lane file
`.ufo/receipt-disclosures.json` (schema `kake-receipt-disclosures-v1`, 12 entries), merged from the
round-57 errata (6 historical relabels, rounds 52/55/56) and an independent first-parent extraction over
the frozen 144-path population at base `9f07731a873585e655a6518233ea39f5d9fb8204`.

Method: read-only history walk in a `--shared` clone at
`/fast/scratch/hyaku/kake-r61/ExecC1Disclose/lane` (evidence scripts kept in this seat's `.files/`).
Receipt grammar per contract (`# receipt:` / `EXIT=` / `VERDICT:`); first-parent blob comparison per commit;
result span compared as the set of whole matching lines; window from each path's first-add commit through base.

## ENTRIES

12 entries, 12 unique `(path, commit)` pairs, all with `{path, commit, kind, note, disclosed-by}`.
Timeline order as committed:

1. `rewrite` `.ufo/waves/round-52/control/c1-mutation-ladder.json` `1ae8de5d4dee8300624b0db2a94497ff905942c5`
2. `rewrite` `.ufo/waves/round-52/control/c1-ledger-real.txt` `a4a890cf1381a194891689dcbba0bf524350926b` (errata)
3. `rewrite` `.ufo/waves/round-52/control/c2-quote-real.txt` `a4a890cf1381a194891689dcbba0bf524350926b` (errata)
4. `rewrite` `.ufo/waves/round-52/control/c1-mutation-ladder.json` `a4a890cf1381a194891689dcbba0bf524350926b`
5. `rewrite` `.ufo/waves/round-52/control/c1-mutation-ladder.json` `fd91527a286086c1f4e6d4f44f715a907f041b5d`
6. `rewrite` `.ufo/waves/round-54/controls/c1-selftest.txt` `8e408e00fbe1c5908df62ba79e78c944bda479e2`
7. `rewrite` `.ufo/waves/round-54/controls/c1-selftest.txt` `a631cc0246b97f2a949d61186c7466468faf94d6`
8. `rewrite` `.ufo/waves/round-55/controls/after-c1-readme-index.txt` `955e3d7bd6d1eff5060e4cebbed51891bb53027a` (errata)
9. `rewrite` `.ufo/waves/round-55/controls/after-c2-quote-truth.txt` `955e3d7bd6d1eff5060e4cebbed51891bb53027a` (errata)
10. `rewrite` `.ufo/waves/round-56/controls/after-c1-selftally.txt` `ad06cb8a17bda28f0691b95aecda13cd4708ea6c` (errata)
11. `rewrite` `.ufo/waves/round-56/controls/after-c2-quote-truth.txt` `ad06cb8a17bda28f0691b95aecda13cd4708ea6c` (errata)
12. `pending_filled` `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` `20217f23eca15862febe14545523832e21584106`

The six errata entries carry that errata's own `note` text verbatim (from→to revision, the rewriting commit's
subject, and the observation that `to` is the commit that introduced the receipt itself); `disclosed-by`
credits `receipt-errata round-57 (kake-r57-receipt-errata-v1)`. The six extras carry notes derived from the
commits' own diffs and credit `ExecC1Disclose (round-61 w1)`.

## EXTRA EVENTS

Six events beyond the errata six (errata covers rounds 52/55/56 only; scan covers the whole 144 population):

1-3. `.ufo/waves/round-52/control/c1-mutation-ladder.json` at `1ae8de5` (round 52 frozen baselines),
   `a4a890cf` (round 52 measured receipts), `fd91527a` (round-53 re-ground crawl citations) — each re-pinned
   18 row-level `old_tail` values (18 insertions / 18 deletions), every value being a receipt `revision:` line.
   The file is a receipt only because its `new_tail` JSON values literally contain `EXIT=1` (unanchored
   `EXIT=` alternative, confirmed with the tool seat as implemented).
4-5. `.ufo/waves/round-54/controls/c1-selftest.txt` at `8e408e00` / `a631cc02` — each commit appended two
   further passing rows (`correction_wrong_polarity`, `correction_before_render`; then `unrelated_marker`,
   `correction_removed_render`) above an unchanged `EXIT=0`; span-matched only because each row's text carries
   `met=False`. Content appends, not label rewrites.
6. `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` at `20217f23` — the r57 pending receipt:
   `31b61a4` committed the bare line `pending`, `20217f23` ("round-57: C1 receipt written after its run at T0")
   filled in the receipt-pins line, a `tip: 31b61a4...` line, `revision: 32754df...` and `EXIT=0`.

Pending scan (no further events): five receipt first-versions contain the word "pending", but only r57's is a
placeholder. `.ufo/waves/round-52/control/drift-before.txt` and `.../sweep-after.txt` carry a body status line
`PQ-5 kimi dead slot  PENDING` and were never modified after their first add; round-58
`controls/c1-selftest-v1.txt` / `c1-selftest-v2.txt` mention "pending fill" inside a documented selftest row
and likewise have a single commit each. None of these four has a later version, so no `pending_filled` fires.

## VERIFICATION

Base revision `9f07731a873585e655a6518233ea39f5d9fb8204` (lane master tip at round open, 2026-10-27).

Each of the six errata `path`+`commit` pairs, checked with git plumbing only (`cat-file`, `merge-base`,
`show`) against that base: all six `commit` ids resolve as commits, all six are ancestors of the base, the
path exists in both the commit and its first parent, the blob differs, the errata `from` value occurs in the
parent's blob, the `to` value occurs in the child's blob and the `from` value is absent there. 6/6 rows pass
every predicate (`ALL_OK: true` in `ExecC1Disclose.files/verify.json`). No errata entry is a phantom.

Fresh extraction reproduces the errata six exactly — same paths, same commits, same from→to strings — so the
errata is complete for its own six and carries no phantom rows. Whole-population result at base: 95 receipt
files (of 144 population paths) and 12 events; the registry's `(path, commit)` set equals that event set
exactly (0 missing, 0 extra). `ExecC1History` independently inventoried the same 12 events; `ExecC1Tool`
reported the same 12 and confirmed the grammar semantics (unanchored `EXIT=`, whole-line span set, pending
tested over the whole first version, disclosure matched on path+commit, wrong `schema` string -> exit 2).

Count point, resolved by the L1: contract R2 as written expected `receipts=144`, but `receipts` in the tool's
summary is the grammar-matched receipt count, which is 95 at base under the frozen `(?im)` pattern
(case-sensitive counting would give fewer; the contract's pattern is case-insensitive) while 144 is the frozen
population size. L1 ruling (amendment A1): R2's expected value is `receipts=95 events=12 undisclosed=0
met=True` exit 0 at the measured revision, with `population=144` asserted separately via the frozen list. This
registry is unaffected by A1 — it holds 12 entries whose (path, commit) set equals the tool's 12 events.

Second contract-text point for the L1 (raised by `ExecC1History`, confirmed by the tool seat's answer): the
frozen sentence tests `pending` inside the *result span*, while the implemented tool tests the *whole first
version*. Outcome is identical on all 144 population files at base (only r57's `20217f23` flips, and it is
disclosed either way, under a kind label matching ignores), so the deviation is benign here but not
rule-equivalent. Fixture L7 (`pending` inside a `met=`/`EXIT=` line) passes under both readings, so a w2 fixture
needs a bare body-line `pending` to tell them apart. L1 ruling (2026-10-27): the amended contract block records
both readings — the whole-first-version pending test and the unanchored `EXIT=` alternative — so w2 binds on
them directly; this report's notes are carried into the w2 attack list.

Not run here (out of seat scope, L1 owns the gate): the lineage tool and counter. `ExecC1Tool` ran the tool at
base before this registry existed and got `events=12 undisclosed=12 met=False`; after the L1 commits this
registry the same run should read `undisclosed=0 met=True` — [INFERENCE], not observed by me. The registry is
currently untracked in the lane; it only binds the tool once committed at the measured revision.
Tooling: nothing installed or upgraded. Scratch deleted before yield; cited evidence copied to
`.ufo/waves/round-61/w1/ExecC1Disclose.files/` (`extract.py`, `events.json`, `verify.py`, `verify.json`,
`receipt-disclosures.snapshot.json`).

VERDICT: 12-event disclosures registry written (errata six + six extras, all path+commit verified at 9f07731a); tool-side confirmation of grammar obtained; only pending step is the L1 committing the file and the counter scoring it.
