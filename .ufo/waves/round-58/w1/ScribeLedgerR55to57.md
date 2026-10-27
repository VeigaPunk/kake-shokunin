# ScribeLedgerR55to57

Round-58 W1, claim C1 (calibration) ledger notes for the 8 receipt events of rounds 55–57. Lane repo
`/home/vgpnk/Projects/shokunin/kake-shokunin`; lane HEAD at read time `cc8da16` (round-58 w1 spec), measured revision
`044048597d62f3199494b63b36e90dd57825e350` verified an ancestor of HEAD (`git merge-base --is-ancestor`).

## Command run

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/c58_receipt_rewrites.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 044048597d62f3199494b63b36e90dd57825e350
C1 receipt-rewrites events=19 undisclosed=19 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=0 met=False
ledger: .ufo/waves/round-58/receipt-rewrites.json absent (0 entries)      (EXIT=1)
```
The 19 events split 11 (rounds 52/54, another seat's set) + 8 (mine, rounds 55–57). Each of my 8 is status `M`
(modified), re-checked with `git diff --name-status <commit>^ <commit> -- <path>`. Kind was re-derived by importing
`classify` from the counter over the two blobs (`git cat-file blob <fromBlob|toBlob>`), not guessed from the docstring.

Read-only git only (`show`, `log`, `diff`, `cat-file`, `ls-tree`); no lane mutation, no index/jj touch; the only lane
write is this report. Nothing but the C1 counter was executed: the 44/44 and 86/86 selftest totals were **not** re-run;
what I did count is the committed selftest case lists (`grep -c 'case("'` on the extracted blobs).

## EVENTS

| path | commit | kind (counter) | what happened | disclosed at the time |
|---|---|---|---|---|
| `.ufo/waves/round-55/controls/c1-selftest-v2.txt` | `64c0ce12ffe3` (77c713e→39f9bb8) | `rerun` | `c55 readme-index selftest: 32/32` → `44/44`. Counter grew: 10 case names at `b467ac3` (v1), 35 at `2bda8e4` (v2, the commit that first committed this 32/32 receipt), 44 at `faf9abe` (v2.1) — and 44 is exactly what the new receipt reports, so the body tracks a re-run of the grown selftest. The 32/32 it replaced matches no committed counter version. | new value stated (`SCORECARD.md:4311` `c1-selftest-v2.txt` (44/44), same commit; LOG "counters to v2.1"); **the replacement of 32/32 is stated nowhere** |
| `.ufo/waves/round-55/controls/after-c1-readme-index.txt` | `955e3d7bd6d1` (05ce598→5b1c9c6) | `relabel` | Body byte-identical in substance (`index_mismatches=0 knowledge_files=49 met=True`, exit 0); only the `revision:` pin moved `faf9abe81d1e` → `64c0ce12ffe3`. Pin landed on the commit that *introduced the receipt*, i.e. the run cannot have been over it. | LOG.md:2166 rewritten in the same commit to "after `0`, exit 0 at `64c0ce1`" — a claim, not a disclosure of the re-pin; disclosed only in round 57 (`receipt-errata.json`, LOG.md:2203 "rewritten to a revision no run backs, undisclosed") |
| `.ufo/waves/round-55/controls/after-c2-quote-truth.txt` | `955e3d7bd6d1` (4fd472c→85cdf7b) | `relabel` | Same shape: eight PASS lines, `8/8 met=True`, exit 0 unchanged; only `revision:` `faf9abe81d1e` → `64c0ce12ffe3`. | same as above: only the LOG/SCORECARD measurement point was restated; round-57 `receipt-errata.json` entry 4 is the first disclosure |
| `.ufo/waves/round-55/controls/c2-selftest.txt` | `955e3d7bd6d1` (6a028cc→85430aa) | `relabel` | `54/54` kept; only the printed token `(fixture revision faf9abe81d1e)` → `(fixture revision 64c0ce12ffe3)`. `c55_quote_truth.py` is identical at both blobs (last touched `faf9abe`) and prints that token from the run's clone HEAD or `KAKE_R55_SELFTEST_REV` (line 852) — so a hand-edit and an identical-count re-run are byte-indistinguishable. 12-hex token ⇒ outside the round-57 errata population. | **not disclosed** anywhere (absent from `.ufo/waves/round-57/receipt-errata.json`; no round-55/56/57 text mentions it) |
| `.ufo/waves/round-56/controls/after-c1-selftally.txt` | `ad06cb8a17bd` (23043b2→913e602) | `relabel` | `tally_mismatches=0 rows_checked=10 met=True`, ten OK cells, exit 0 unchanged; only `revision:` `f8438a282d59` → `4cb225fb032b` (the commit that introduced the receipt). Same commit also filled the `@R@` placeholder in LOG.md:2186 with `4cb225f`. | commit subject says "revision pins"; no statement that a run does not back the new pin; first disclosure round 57 (`receipt-errata.json` entry 5, LOG.md:2203) |
| `.ufo/waves/round-56/controls/after-c2-quote-truth.txt` | `ad06cb8a17bd` (236f623→ce5a879) | `relabel` | Eight PASS lines, `8/8 met=True`, exit 0 unchanged; only `revision:` `f8438a282d59` → `4cb225fb032b`. | same as above; first disclosure round 57 (`receipt-errata.json` entry 6) |
| `.ufo/waves/round-56/controls/c2-selftest.txt` | `ad06cb8a17bd` (f96bb11→1cfd566) | `relabel` (**counter is wrong — see §KIND DISAGREEMENTS**) | `67/67` → `86/86` with the fixture pin unchanged at `f8438a282d59`. The +19 is exactly the counter's growth: `c56_quote_truth.py` has 63 → 82 `case("` calls between `f8438a28` and `4cb225f`. The receipt was first committed (still `67/67`) in `4cb225f`, the very commit that added the 19 cases. | value change disclosed *before* the receipt caught up: `.ufo/waves/round-56/settlement.md:23` "C2 selftest 67 -> 86 (19 dual-edit fixtures from `MutC2Selftest`)", `SCORECARD.md:4339` `c2-selftest.txt` (86/86); the rewrite itself is filed under a "revision pins" commit subject |
| `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` | `20217f23eca1` (417ca0c→b514c80) | `fill` | Placeholder `pending` + `revision: 32754df75774…` + `EXIT=0` (committed at `31b61a4`) filled with the counter line `… new_receipts=3 scorecard_pin=1 met=True` and `tip: 31b61a4ddfca`; `EXIT=0` kept. A receipt with a revision pin and an exit code existed before the run, then grew a body — the pattern round-57 C1 was built against. | presented as ordinary landing: r57 report table rows "placeholder C1 receipt" / "C1 receipt written after its run at T0"; **contradicted by the lane's own LOG.md:2207** ("this round's receipts are pinned to the measured revision and never rewritten") and later named by the lane's spot-check (`corpus/lessons/round-57-verifier-spotcheck.md:104` §5 D1) |

Disclosure cross-check that the lane itself supplies for four of the eight: `.ufo/waves/round-57/receipt-errata.json`
entries 3–6 name events 2, 3, 5, 6 with the same from/to revisions and commits I found, and LOG.md:2203 counts "six
measurement receipts of rounds 52–56". Events 1, 4, 7 are outside the round-57 population (a bare count line, a 12-hex
fixture token, and a `67 → 86` count line), so the round-57 errata could not cover them and nothing else does.

## NOTES JSON

```json
[
 {"path": ".ufo/waves/round-55/controls/c1-selftest-v2.txt", "commit": "64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6", "kind": "rerun",
  "note": "The C1 selftest receipt first committed as `c55 readme-index selftest: 32/32` at 2bda8e4 was rewritten to `44/44` here, the new total equalling the 44 case names in `.ufo/waves/round-55/c55_readme_index.py` at faf9abe (v2.1) after the counter held 35 case names at 2bda8e4, so this is a re-run of the grown selftest and not a revision-pin edit; the new value is stated as the round's selftest receipt in `SCORECARD.md` (line 4311) while the replacement of 32/32 is stated nowhere."},
 {"path": ".ufo/waves/round-55/controls/after-c1-readme-index.txt", "commit": "955e3d7bd6d1eff5060e4cebbed51891bb53027a", "kind": "relabel",
  "note": "Body unchanged (`index_mismatches=0 knowledge_files=49 met=True`, exit 0) and only the `revision:` pin moved faf9abe81d1e -> 64c0ce12ffe3, the commit that introduced this receipt, in the same commit that rewrote `LOG.md` line 2166 to `after 0, exit 0 at 64c0ce1` without saying the receipt had been re-pinned; the lane disclosed the relabel only in round 57 (`.ufo/waves/round-57/receipt-errata.json`, `LOG.md` line 2203)."},
 {"path": ".ufo/waves/round-55/controls/after-c2-quote-truth.txt", "commit": "955e3d7bd6d1eff5060e4cebbed51891bb53027a", "kind": "relabel",
  "note": "Same pattern as its C1 sibling: the eight PASS lines, `8/8 met=True` and exit 0 are unchanged and only the `revision:` pin moved faf9abe81d1e -> 64c0ce12ffe3 in the commit that also restated the round's measurement point in `LOG.md` line 2166, with the relabel first disclosed in round 57 (`.ufo/waves/round-57/receipt-errata.json`, `LOG.md` line 2203)."},
 {"path": ".ufo/waves/round-55/controls/c2-selftest.txt", "commit": "955e3d7bd6d1eff5060e4cebbed51891bb53027a", "kind": "relabel",
  "note": "The body keeps `54/54` and only the printed fixture-revision token moves faf9abe81d1e -> 64c0ce12ffe3, a token `.ufo/waves/round-55/c55_quote_truth.py` line 852 prints from the run's clone HEAD or `KAKE_R55_SELFTEST_REV`, so the bytes fit both a hand-edited label and a second identical-count run and no committed text says which; the round-57 errata population requires a 40-hex pin and this line carries 12 hex, so `.ufo/waves/round-57/receipt-errata.json` omits it and it is disclosed nowhere."},
 {"path": ".ufo/waves/round-56/controls/after-c1-selftally.txt", "commit": "ad06cb8a17bda28f0691b95aecda13cd4708ea6c", "kind": "relabel",
  "note": "Body unchanged (`tally_mismatches=0 rows_checked=10 met=True`, ten OK cells, exit 0) and only the `revision:` pin moved f8438a282d59 -> 4cb225fb032b, the commit that introduced this receipt, while the same commit replaced the `@R@` placeholder in `LOG.md` line 2186 with that id and said nothing about a re-pin; disclosed only in round 57 (`.ufo/waves/round-57/receipt-errata.json`, `LOG.md` line 2203)."},
 {"path": ".ufo/waves/round-56/controls/after-c2-quote-truth.txt", "commit": "ad06cb8a17bda28f0691b95aecda13cd4708ea6c", "kind": "relabel",
  "note": "Same pattern as its C1 sibling: the eight PASS lines, `8/8 met=True` and exit 0 are unchanged and only the `revision:` pin moved f8438a282d59 -> 4cb225fb032b in the commit whose subject claims `revision pins`, with the relabel first disclosed in round 57 (`.ufo/waves/round-57/receipt-errata.json`, `LOG.md` line 2203)."},
 {"path": ".ufo/waves/round-56/controls/c2-selftest.txt", "commit": "ad06cb8a17bda28f0691b95aecda13cd4708ea6c", "kind": "relabel",
  "note": "The count went `67/67` -> `86/86` against an unchanged fixture pin f8438a282d59, the +19 exactly matching the `c56_quote_truth.py` selftest growth from 63 to 82 `case(` calls between f8438a28 and 4cb225f, so this is a re-run of a counter that gained 19 dual-edit fixtures (stated at `.ufo/waves/round-56/settlement.md` line 23 and `SCORECARD.md` line 4339) rather than a revision relabel, even though the unchanged `(fixture revision ...)` token makes the counter's `relabel` rule fire."},
 {"path": ".ufo/waves/round-57/controls/after-c1-receipt-pins.txt", "commit": "20217f23eca15862febe14545523832e21584106", "kind": "fill",
  "note": "The placeholder `pending` plus `revision: 32754df7...` plus `EXIT=0` committed at 31b61a4 was filled here with the counter's `met=True` line and `tip: 31b61a4ddfca`, which the round's own landing table presents as an ordinary write (`placeholder C1 receipt`, `C1 receipt written after its run at T0`) while `LOG.md` line 2207 asserts this round's receipts are `never rewritten` and the lane's later spot-check calls it the exact pattern the round-57 C1 counter forbade (`corpus/lessons/round-57-verifier-spotcheck.md` line 104)."}
]
```
All eight notes pass the counter's own `pointed()` check (imported and run against revision `0440485`; 8/8 `True`):
each names a repo-relative path that exists at the lane tip. `kind` above is the counter's classification, so these
entries would yield `wrong_kind=0` if copied with `status`/`fromBlob`/`toBlob` from the counter's event list — except
that for event 7 the declared kind then misdescribes the event (below).

## KIND DISAGREEMENTS

1. **Established — `.ufo/waves/round-56/controls/c2-selftest.txt` @ `ad06cb8a17bd`: counter says `relabel`, the event is
   a `rerun`.** `classify` only sees one changed line, and that line contains the word `revision` inside
   `(fixture revision f8438a282d59)`, so the `REVLINE_RE` branch fires; the real change is `67/67` → `86/86`, backed by
   the counter itself growing 63 → 82 `case("` calls (`f8438a28` → `4cb225f`) and by the lane's own
   `.ufo/waves/round-56/settlement.md:23`. Consequence for the predicate: declaring `relabel` (what the frozen
   classification demands) writes a false kind into the ledger; declaring `rerun` fails `wrong_kind == 0`. A note can
   state the truth while the `kind` field stays `relabel` (my note above does exactly that) — the L1 must decide
   whether that is acceptable or whether the counter's `relabel` rule should stop matching `(fixture revision …)`
   tokens. I did not edit the counter.
2. **Not established — `.ufo/waves/round-55/controls/c2-selftest.txt` @ `955e3d7bd6d1`: `relabel` may be wrong.** Same
   counter, same `54/54`; the only change is the printed fixture token, emitted at run time (`c55_quote_truth.py:852`)
   from the clone HEAD or `KAKE_R55_SELFTEST_REV`. A re-run at `64c0ce1` would produce this exact blob, so I can neither
   confirm nor refute `relabel`; flagged because the round-57 errata never examined this file (12-hex token, outside its
   population) and round-57's "six receipts" count therefore undercounts the rewrites c58 can see.
3. Population mismatch worth stating plainly: c58's receipt population (every path under
   `.ufo/waves/round-<N>/control(s)/`) is wider than round-57's (paths carrying a 40-hex pin), so events 1, 4 and 7
   were never disclosable under the round-57 regime. Of my eight, only events 2, 3, 5, 6 have a committed disclosure,
   and all four are round-57 retro-disclosures, not contemporaneous ones.

## Unrun / limits

- Not run: any selftest of `c55_readme_index.py`, `c55_quote_truth.py`, `c56_quote_truth.py`; the 44/44, 54/54 and
  86/86 receipts are corroborated only by counting committed `case("` calls, not by execution.
- Not read: the round-55/56/57 prompt-side fleet reports beyond the lines quoted (`.ufo/reports/round-5[5-7]/kake.md`
  were grepped, not audited); the `w1/`/`w2/` seat reports for the commits in question.
- [INFERENCE] The 32/32 body in event 1 came from an uncommitted intermediate counter state during the build commit
   `2bda8e4` — the only explanation I can see for 32 when the committed counter had 35 cases; not proved.
- Scratch `/fast/scratch/hyaku/kake-r58/ScribeLedgerR55to57/` deleted; no tool installed or upgraded.

VERDICT: 8/8 round-55–57 events classified from blobs; four relabels are round-57 retro-disclosures, three rewrites (one count re-run, one bare count, one 12-hex fixture token) are disclosed nowhere, and the counter's `relabel` kind is provably wrong for `.ufo/waves/round-56/controls/c2-selftest.txt` @ `ad06cb8a17bd`.
