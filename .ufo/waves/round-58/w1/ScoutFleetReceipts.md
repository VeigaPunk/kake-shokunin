# ScoutFleetReceipts

Method (observed, 2026-10-26): per lane, `git ls-files .ufo/waves` filtered by `^\.ufo/waves/round-*/(any depth)/controls?/`, then `git -C <lane> log --format=%h -- <path> | wc -l` per path; ledger search by file name over tracked `.ufo`. Read-only; nothing absorbed. Lane working-tree HEAD only (no other revisions). Script was in scratch (deleted).

LANES:
| lane | rounds w/ controls | control paths (receipts) | rewritten (>1 commit) | dedicated control-rewrite ledger? |
|---|---|---|---|---|
| kotoba | 17 | 390 | 11 (all round-57 CtlC1*.md/.txt, 2 commits each) | no. Only generic `*Errata*`/ledger files (122 name hits, mostly census/mutation ledgers) |
| kaidoku | 11 | 445 | 4 (r38 ctl-c1-0 x3 commits, r38 ctl-c1-1/-2 x2, r30 receipts.tsv x2) | no (43 ledger/errata/rewrite name hits, none about controls) |
| tsukuroi | 9 | 141 | 2 (r32 controls/README.md x3, r41 run_controls.py x2) | no (465 ledger-ish hits, all other subjects) |
| kumitate | 12 | 1798 (8 more ever existed, deleted from HEAD) | 84 (mostly nested r63 controls/inline fixture files, 2-3 commits) | YES, prose: `round-63/controls/CHANGES-AFTER-FREEZE.md` (+ round-64 copy); also `round-45/a2-control/ScoutErrataCheck.md` |
| souji | 1 (r22 evidence/control/) | 5 | 0 | no |
| kake (self, for contrast) | 14 | 1099 | 16 (r52 c1-mutation-ladder.json x4, r54 c1-selftest.txt x3, r52/r54 others x2) | no machine ledger yet; r58 adds `receipt-rewrites.json` + counter. Closest prior: `round-26/receipt-locator-errata.json` (locators, not rewrites) |

Rewrite reasons seen in commit subjects (observed):
- kotoba r57: "C1 counter v2 (stricter)... control receipts" then "v2 re-control receipts" — rewrite is a re-score under a changed counter, disclosed in subject only.
- kaidoku r38: "c1 controls re-scored under freeze v2" then "re-scored under freeze v3" — same pattern, subject-only.
- kake r52: "frozen baselines and the seven measurement receipts", then "measured receipts, drift reconciliation", then "re-ground crawl source citations" (r53) — three different reasons across one path.
- kumitate r63: controls changed after the freeze commit; disclosed in a markdown file listing each change, reason, and counts (14 -> 75 cases), and which changes are not pure strengthening.

NOTE:
- Only kumitate has a purpose-built disclosure file for post-freeze control changes; it is prose, with no machine-checkable path-to-reason mapping and no counter. The other four lanes disclose, if at all, in the commit subject only. So kake's r58 ledger + counter (C1) has no direct sibling analogue to copy; kumitate's CHANGES-AFTER-FREEZE.md is the nearest shape (numbered change, cause with seat names, monotone/not-pure-strengthening split).
- Multi-commit count overstates "rewrite": it includes legitimate append (add in one commit, extend in a later one), renames-by-copy are not followed (no `--follow`), and pure-additive growth of a directory counts per file. Rewrite rate is thus an upper bound per lane: kotoba 11/390 (2.8%), kaidoku 4/445 (0.9%), tsukuroi 2/141 (1.4%), kumitate 84/1798 (4.7%, inflated by one r63 fixture tree), souji 0/5, kake 16/1099 (1.5%). [INFERENCE] The kake base figure of 19 undisclosed events in the contract uses a different event definition than this path count; the two are not comparable.
- Layout varies: kake uses `control/` (r52) and `controls/` (r54+) and `retained/controls/`; tsukuroi `measure/controls/`; souji `evidence/control/`; kumitate `controls/` and `a2-control/` (the latter is not matched by the filter). Any lane-agnostic counter must glob `control(s)?` at any depth under a round dir.
- Unrun: no `--follow` rename tracking; no cross-branch/`--all` rewrite (history-rewrite via amend/force-push) detection beyond a path-set check (kumitate 8 deleted control paths; others 0).
VERDICT: 5 sibling lanes surveyed; only kumitate has a (prose) control-change disclosure file, none has a machine ledger; multi-commit control paths 11/4/2/84/0 (kotoba/kaidoku/tsukuroi/kumitate/souji).
