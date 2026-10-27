# ExecReceiptPopulationNames

Claim C1 pre-data check, honest-reporting class: which committed files does the lane's **own prose** call
"receipts", and does the C1 counter's population (`.ufo/waves/round-N/control(s)/<file>`) cover them.

**Sources grepped** (`grep -in receipt`, HEAD of lane at check `cc8da1674d6e590ae2d05e1f48944ac7939e9ecd`;
base `0440485`, contract `fff3eea`): `SCORECARD.md` 203 matching lines, `LOG.md` 74, and
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-5[0-7]/kake.md`: r50 0, r51 9, r52 6, r53 4, r54 4,
r55 0, r56 0, r57 12. Path tokens adjacent to a `receipt`/`receipts` occurrence were resolved against the
lane tree at HEAD (round-relative tokens resolved under the `## Round N` section the line sits in).
**Commits per path:** `git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --format=%h -- <path> | wc -l`
(>1 = rewritten, per assignment).
**Population (from `c58_receipt_rewrites.py`):** `POP_RE = ^\.ufo/waves/round-[0-9]+/(control|controls)/[^/]+$`
— direct children only, any round.

Not run (not this seat's scope, reported as unrun): the C1/C2/C3 counters, the counter selftests, any build,
lint or test. No tool was installed. All statements below are `git log`/`git ls-tree`/`grep` output.

## NAMED RECEIPTS: (path/pattern, source round, in/out of population, files, files rewritten)

| Named receipt location | Round | In/Out | Files | Rewritten |
|---|---|---|---|---|
| `.ufo/round-20/receipt-binding.json` | R20 | OUT | 1 | 0 |
| `.ufo/waves/round-23/{live/,measure-c2-after-v2.json,evaluability.json}` | R23 | OUT | 42 | 0 |
| `.ufo/waves/round-24/measure-c{1,2}-c1-only.json` | R24 | OUT | 2 | 0 |
| `.ufo/waves/round-{28,29,30,31,34,35,36,37,48,51,53}/sources/receipts.json` | R28-R53 | OUT | 11 | 2 |
| `.ufo/waves/round-{29,30}/sources/screened/receipts.json` | R29,R30 | OUT | 2 | 0 |
| `.ufo/waves/round-34/verification/{criterion-lookup-control-c1-dcef39b.txt,c2-at-critic-hollow-0cce15f.json,real-input-at-5613071.json}` | R34 | OUT | 3 | 0 |
| `.ufo/waves/round-35/verification/c{1,2}-*.json` | R35 | OUT | 11 | 0 |
| `.ufo/waves/round-36/verification/control-*.json` | R36 | OUT | 8 | 2 |
| `.ufo/waves/round-36/verification/ablations/*.json` ("ablation receipts") | R36 | OUT | 37 | 35 |
| `.ufo/waves/round-36/verification/v2/*` | R36 | OUT | 14 | 0 |
| `.ufo/waves/round-37/realrun/robots/receipts.json` | R37 | OUT | 1 | 0 |
| `.ufo/waves/round-37/verification/` (`control-*`, `c1-*`, `.exit`, `postfix/*-receipt.txt`) | R37 | OUT | 130 | 0 |
| `.ufo/waves/round-38/realrun/robots/receipts.json` | R38 | OUT | 1 | 0 |
| `.ufo/waves/round-38/verification/` | R38 | OUT | 307 | 0 |
| `.ufo/waves/round-39/verification/{a3,a3-jcheck}/` | R39 | OUT | 163 | 0 |
| `.ufo/waves/round-40/verification/w1/` ("141 receipts") | R40 | OUT | 79 | 0 |
| `.ufo/waves/round-40/controls/w1/<Seat>/` (nested tool copies, named beside receipts) | R40 | OUT | 77 | 0 |
| `.ufo/waves/round-41/verification/{l1,w1,pre,r40standing}/` | R41 | OUT | 185 | 0 |
| `.ufo/waves/round-42/verification/{pre,pre-v2,v3probe,v3probe-a58e,w1v3,w2v3}/` | R42 | OUT | 112 | 0 |
| `.ufo/waves/round-43/verification/{freeze,l1-rescores}/` | R43 | OUT | 68 | 1 |
| `.ufo/waves/round-44/verification/{claim,placebo,freeze}/` | R44 | OUT | 295 | 1 |
| `.ufo/waves/round-45/verification/freshness/freshness.json` | R45 | OUT | 1 | 1 |
| `.ufo/waves/round-46/verification/` | R46 | OUT | 8 | 0 |
| `.ufo/waves/round-47/verification/` | R47 | OUT | 13 | 0 |
| `.ufo/waves/round-48/verification/` | R48 | OUT | 2 | 0 |
| `.ufo/waves/round-51/{sources/receipts.json,superseded/,assimilation/pre-append/census-correction.txt}` | R51 | OUT | 2 | 1 |
| `.ufo/waves/round-52/control/*` (the report's receipt table) | R52 | IN | 19 | 4 |
| `.ufo/waves/round-52/baselines.json` (receipt digests) | R52 | OUT | 1 | 1 |
| `.ufo/waves/round-53/sources/` (receipts + Gate quotes) | R53 | OUT | 9 | 0 |
| `.ufo/waves/round-54/controls/*` | R54 | IN | 6 | 4 |
| `.ufo/waves/round-54/source-reopen.txt` ("Receipt/hash in") | R54 | OUT | 1 | 0 |
| `.ufo/waves/round-55/controls/*` | R55 | IN | 11 | 4 |
| `.ufo/waves/round-56/controls/*` | R56 | IN | 9 | 3 |
| `.ufo/waves/round-57/controls/*` | R57 | IN | 20 | 1 |
| `.ufo/waves/round-57/{receipt-errata.json,measured.json}` | R57 | OUT | 2 | 0 |

Totals: **IN 65 files / 16 rewritten** (rounds 52-57 `control(s)/` only); **OUT 1,588 files / 44 rewritten**,
of which one row is 77 nested tool copies (not receipts in role) and one rewrite is `freeze/sweep-before.exit`
while the named `sweep-before.txt` is single-commit — i.e. **1,511 prose-named receipt files outside, 43 rewritten**.

IN-population rewritten (commits in parentheses): `round-52/control/{c1-ledger-real.txt (2),
c1-mutation-ladder.json (4), c2-quote-real.txt (2), c2-quote-selftest.txt (2)}`;
`round-54/controls/{base-c1-s374.txt (2), base-c2-ops-debt.txt (2), c1-selftest.txt (3), sources-census.txt (2)}`;
`round-55/controls/{after-c1-readme-index.txt (2), after-c2-quote-truth.txt (2), c1-selftest-v2.txt (2),
c2-selftest.txt (2)}`; `round-56/controls/{after-c1-selftally.txt (2), after-c2-quote-truth.txt (2),
c2-selftest.txt (2)}`; `round-57/controls/after-c1-receipt-pins.txt (2)`.
Cross-check: commits−1 over these 16 files sums to **19**, exactly the counter's base
`events=19 undisclosed=19` — the "rewritten" measure and the counter's event walk agree on the watched set.

## OUTSIDE AND REWRITTEN: (43 named receipt files, commits > 1)

- `.ufo/waves/round-36/verification/ablations/` — **35 of 37** `ablation-*.json`, 2 commits each (the two
  single-commit files are `ablation-s_ctkey.json`, `ablation-s_unsure.json`). Prose: "The 34 rule ablations …
  ablation receipts are committed before any build" (SCORECARD r36).
- `.ufo/waves/round-36/verification/control-base.json` (2), `control-declaration.json` (2) — prose calls
  `verification/control-*.json` "Controls (receipts …)".
- `.ufo/waves/round-34/sources/receipts.json` (2), `.ufo/waves/round-35/sources/receipts.json` (2).
- `.ufo/waves/round-44/verification/claim/ledger-after.txt` (2) — named "`.ufo/waves/round-44/verification/claim/ledger-after.txt`".
- `.ufo/waves/round-45/verification/freshness/freshness.json` (2).
- `.ufo/waves/round-51/assimilation/pre-append/census-correction.txt` (2) — a "census receipt".
- `.ufo/waves/round-52/baselines.json` (2) — receipt digests named in the r52 routed-defect table.

Outside but NOT rewritten (spot-checked, 0 rewrites): round-23 live (42), round-37 verification (130),
round-38 verification (307), round-39 a3+a3-jcheck (163), round-40 w1 (79), round-41 (185), round-42 (112),
round-43 freeze+l1-rescores (67 of 68), round-44 claim/placebo/freeze (294 of 295), round-46/47/48,
round-53 sources, round-57 errata/measured. Round-5x reports call their own `controls/` receipts exclusively
inside the population; the outside calls are the older `verification/` receipts and the `sources/receipts.json`
registry receipts.

## VERDICT:

No. The population covers only 65 of the 1,576 receipt paths the lane's prose calls receipts (4.1 %): every
`control(s)/` direct child of rounds 52-57 (16 rewritten, 19 events — matching the counter's base count), while
1,511 prose-named receipt files sit in `verification/`, `sources/`, `receipt-errata.json`, `measured.json`,
`baselines.json`, `source-reopen.txt`, `receipt-binding.json` and `superseded/`, of which 43 were rewritten
(35 round-36 ablation receipts and 2 round-36 control receipts the largest block); C1's own stated limit
"receipts outside `control(s)/` dirs" is therefore a coverage hole against the lane's vocabulary, not a corner.
VERDICT: population under-covers what the lane calls receipts (65 in / 1,511 out; 43 outside rewrites invisible to C1).
