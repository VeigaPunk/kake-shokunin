# ScribeReportFacts
ATTACKS: the round-55 build measured at `a7a548e102b71bd16b0a6ddafa469393a2c98b69` against base
`fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d` — `corpus/SOURCES.md` (registry census; rows S372, S373,
S418), `corpus/knowledge/` (file count, entries-by-ground), `corpus/README.md` §Coverage map
(`coverage_rows`), `PROVINCE.md` §Frontier and §Round-55. Read-only. Nothing below re-adjudicates a
source; row sets are copied from the registry, not re-graded.

## COMMANDS AND OUTPUTS

Measured bytes, not the worktree. Both revisions materialised with committed bytes only:
```
$ D=$(mktemp -d) && git -C <lane> archive fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d | tar -x -C "$D"
  -> SCRATCH_BASE=/tmp/tmp.2ktzIW3dtk      (no .git in tree: test -e $D/.git -> no)
$ D=$(mktemp -d) && git -C <lane> archive a7a548e102b71bd16b0a6ddafa469393a2c98b69 | tar -x -C "$D"
  -> SCRATCH_AFTER=/tmp/tmp.rZkpV7r8LL     (no .git in tree)
sha256 corpus/SOURCES.md  git-show                       scratch
  fcaf4b85… f4e6cc8830c1d963218a31e5745c0c892a30a83d0d758fcd412a5c201bdc517d  f4e6cc88… (equal)
  a7a548e1… cc402e4b559528170fe71ba09b6ad3be663a8f9d5ce9f36caeaed5ea45e6c50e  cc402e4b… (equal)
```

### C1 counter (calibration) — `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision <rev>`
Base `fcaf4b85…` — **EXIT=1**
```
C1 readme-index index_mismatches=21 knowledge_files=46 met=False  (met: index_mismatches == 0 AND knowledge_files >= 46)
  unindexed=21 multi=0 thin=0 duplicate=0 head_changed=0 deleted=0 dangling=0 coverage_rows=27
  revision: fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d
```
(the 21 `unindexed:` names follow that line in the output; comma-joined here for width, names verbatim:
accessibility-review-cards.json, accessibility-review-packet.md, baidu-friendly-crawl-guidance.md,
baidu-mobile-matching-error-causes.md, canonical-selection.md, crawl-budget-consequences.md,
crawl-error-status-table.md, crawler-identity.md, dynamic-rendering-workaround-limits.md,
freshness-sidecar.json, js-rendering-queue.md, link-preview-metadata.md, pages-base-path.md,
receipt-integrity.md, redirect-rewrite-rules.md, render-static-sites.md, render-web-services.md,
robots-txt-rules.md, security-txt-publishing.md, vault-properties.md, yahoo-japan-rel-nofollow-semantics.md)

Build `a7a548e1…` — **EXIT=0**
```
C1 readme-index index_mismatches=0 knowledge_files=49 met=True  (met: index_mismatches == 0 AND knowledge_files >= 46)
  unindexed=0 multi=0 thin=0 duplicate=0 head_changed=0 deleted=0 dangling=0 coverage_rows=51
  revision: a7a548e102b71bd16b0a6ddafa469393a2c98b69
```

### C2 counter (freshness) — `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root . --revision <rev>`
Base `fcaf4b85…` — **EXIT=1**
```
C2 quote-truth 0/8 met=False  (met: conditions_passed == 8 of 8)
  C1_entries_exist FAIL
  C2_entry_provenance FAIL
  C3_row_shape FAIL
  C4_used_by FAIL
  C5_quote_truth FAIL
  C6_receipt_pins FAIL
  C7_validate_before_append FAIL
  C8_mirror_bytes FAIL
  revision: fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d
```
(22 `- ` detail bullets under those eight lines are elided for width; their content is quoted in the
SOURCES TABLE section as the C4 used-by expectation, and the full body is byte-identical to
`.ufo/waves/round-55/controls/base-c2-quote-truth-v2.txt` — see reproduction below.)

Build `a7a548e1…` — **EXIT=0**
```
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)
  C1_entries_exist PASS
  C2_entry_provenance PASS
  C3_row_shape PASS
  C4_used_by PASS
  C5_quote_truth PASS
  C6_receipt_pins PASS
  C7_validate_before_append PASS
  C8_mirror_bytes PASS
  revision: a7a548e102b71bd16b0a6ddafa469393a2c98b69
```

Reproduction against the committed receipts (byte comparison, not eyeballing):
```
$ python3 -B …/c55_readme_index.py --root . --revision fcaf4b85… > /tmp/srf_c1b.txt ; diff /tmp/srf_c1b.txt controls/base-c1-readme-index-v2.txt
  -> 0 diff lines (exit=1 from the counter)
$ python3 -B …/c55_quote_truth.py  --root . --revision fcaf4b85… > /tmp/srf_c2b.txt ; diff /tmp/srf_c2b.txt controls/base-c2-quote-truth-v2.txt
  -> 0 diff lines (exit=1 from the counter)
```

### Census validate — `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
**EXIT=0**; 14 `W04` duplicate-URL warnings then `ok`. Output byte-identical to
`.ufo/waves/round-55/controls/census-before.txt` (14 W04 lines: S033 S088 S092 S098 S099 S102 S110
S111 S115 S116 S117 S127 S416 S417, each `duplicate url … across scopes`):
```
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```
Warnings are non-fatal: the row is `ok` and the exit code is 0. The lane worktree was at `78963ae`
when this ran; `git diff a7a548e1… HEAD -- corpus/SOURCES.md` is empty and `sha256sum corpus/SOURCES.md`
= `cc402e4b…c50e`, the same digest as `git show a7a548e1…:corpus/SOURCES.md` — so this run reads the
build's bytes.

### CORPUS.md §Census at both revisions (run from the extracted scratch roots)
```
$ cd /tmp/tmp.2ktzIW3dtk   (base)                    $ cd /tmp/tmp.rZkpV7r8LL  (a7a548e)
-- rows --                155                        -- rows --                156
-- malformed --           0                          -- malformed --           0
-- tier --                A=132 B=6 C=17             -- tier --                A=133 B=6 C=17
-- status --              mined=125 queued=8 rejected=22   -- status --        mined=126 queued=8 rejected=22
-- duplicate ids --       (nothing)                  -- duplicate ids --       (nothing)
-- enum violations --     (nothing)                  -- enum violations --     (nothing)
-- missing used-by --     (nothing)                  -- missing used-by --     (nothing)
```
Commands were the seven blocks copied verbatim from `CORPUS.md` §Census (lines 131–152), unchanged;
`-- missing used-by --` resolves each `mined` row's used-by cells with `[ -e "$p" ]` inside the
extracted tree, so it is a real existence test, not an empty-loop pass.

### Knowledge-file count and coverage rows
```
$ find $B/corpus/knowledge -type f | wc -l          46      $ find $A/corpus/knowledge -type f | wc -l          49
$ find $B/corpus/knowledge -name '*.md' | wc -l     43      $ find $A/corpus/knowledge -name '*.md' | wc -l     46
$ find $B/corpus/knowledge -name '*.json' | wc -l    3      $ find $A/corpus/knowledge -name '*.json' | wc -l    3
```
46 → 49 files (+3 `.md`; the three `*.json` are unchanged) — matches the counters' `knowledge_files`.
`coverage_rows` 27 → 51 (+24 = the 21 files the map named nowhere at base + the 3 new entries).
Registry diff shape: `diff -u` of the two `SOURCES.md` = **1 hunk, 5 changed `|` lines**
(`-S372 -S373 +S372 +S373 +S418`); `README.md` = 1 hunk, 77 added / 0 removed lines; `PROVINCE.md` =
1 hunk, 19 added / 0 removed lines. No row was deleted (`removed: []`).

## SOURCES TABLE

Registry: **155 → 156 rows**; malformed 0 → 0; duplicate ids 0 → 0; enum violations 0 → 0; missing
used-by paths 0 → 0; **added by tier: A +1 (A 132 → 133), B 6 → 6, C 17 → 17**; status
**mined 125 → 126**, queued 8 → 8, rejected 22 → 22. The single added row is S418 (`docs`, tier `A`,
`mined`, `opened 2026-10-25`), `used-by` = `corpus/knowledge/yahoo-japan-robots-txt-basics.md`.

Touched rows — cell diff of all 11 columns, base vs `a7a548e1…`:

| Row | Changed cell | old → new |
|---|---|---|
| S372 | `used-by` only | `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` → `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md, corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md` |
| S373 | `used-by` only | `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md, corpus/knowledge/baidu-friendly-crawl-guidance.md` → same two, `+ corpus/knowledge/yahoo-japan-robots-pattern-syntax.md` |
| S418 | new row | absent at base → `docs / A / mined / 2026-10-25 / 180d / corpus/knowledge/yahoo-japan-robots-txt-basics.md` |

S372 and S373 are identical in the other ten columns (`source`, `kind`, `tier`, `scope`, `anchor`,
`teaches`, `status`, `opened`, `recheck`, `id`) — so the contract sentence "differ from base in
`used-by` only" is what the bytes show. The C2 counter's C4 line states the same old→new pair
independently (`used-by is [...] , expected [...]`).

## FRONTIER

Per `PROVINCE.md` §Round-55 (line 385) the round adds three entries on one operator's robots.txt rules
and **advances rows S372, S373, S418** on the per-engine crawl-hygiene ground that round 52 opened with
link attributes (S374). `corpus/README.md` §Frontier ground map row for that ground reads
`r55 (lands this round) | 3 entries | S372 S373 S418`.

Entries-by-ground, before → after. The ground map does not exist at base (`grep -c "Frontier ground
map" corpus/README.md` = 0 at base, 1 after), so the "before" column is the after-map's entry paths
tested for existence in the base tree (21 grounds; totals **20 → 23 entries**):

| Frontier ground (README map row) | Entered | before → after |
|---|---|---|
| Crawl hygiene per host | r20 | 1 → 1 |
| robots.txt rule semantics, offline expectation audit | r37; repaired r38 | 1 → 1 |
| Sitemap and orphan parity | r7; r33 source pin | 1 → 1 |
| Static canonical declaration | r22 | 1 → 1 |
| Canonical selection | r51 | 1 → 1 |
| Crawler identity (Googlebot subtypes) | r51 | 1 → 1 |
| JS rendering queue | r48 | 1 → 1 |
| Dynamic rendering limits | r48 | 1 → 1 |
| Crawl budget | r49 | 1 → 1 |
| Crawl-error status | r50 | 1 → 1 |
| Yahoo! JAPAN link attribute (`rel`) | r52; S374 re-read r54 | 1 → 1 |
| Baidu crawl guidance | r52; locators superseded r53 | 1 → 1 |
| Baidu mobile matching | r52; locators superseded r53 | 1 → 1 |
| **Yahoo! JAPAN robots refusal file, pattern syntax, basics** | **r55 (lands this round)** | **0 → 3** |
| Field performance (CWV, CrUX) | r28 | 1 → 1 |
| Jekyll/base-path build tooling | r29 | 1 → 1 |
| Render static sites | r30 | 1 → 1 |
| Render web services and Blueprint | r31 | 1 → 1 |
| Link-preview metadata | r34 | 1 → 1 |
| security.txt publishing | r35 | 1 → 1 |
| Accessibility review preparation | r25 | 1 → 1 |

Rows advanced, per PROVINCE: **S372** (used-by +1 entry, status unchanged `mined`), **S373** (used-by
+1, `mined`), **S418** (new row, `A`, `mined`) — all three on the r55 ground; no other ground moves.
Two dated row sets still hold no entry of their own (map note, not re-checked here): S102–S109
(round-39 lesson) and S416/S417 (round-53 lesson). The map's five `Untouched ground` bullets and its
five "held, but ungated or unmeasured" items are PROVINCE frontier items with no measured change this
round — `unrun` by me (they are PROVINCE prose, not counters).

Out of scope for this seat: counter selftests, the quote-span unit counts, receipts/`sha256` pins, and
the mirror-byte check — C2's C5/C6/C8 PASS lines above report them, but I did not re-open a source body.
Every number here is one of the pasted commands' output; the one arithmetic join
(27 + 24 = 51 coverage rows; 21 unindexed + 3 new = 24 added) is `[INFERENCE]` over observed counts.

VERDICT: at `a7a548e1…` C1 reads `index_mismatches=0 knowledge_files=49 met=True` exit 0 and C2 reads `8/8 met=True` exit 0 against base `21 / 46 / met=False` exit 1 and `0/8 met=False` exit 1; registry 155 → 156 rows with A +1, mined +1, S372/S373 changed in `used-by` only and S418 added; census 0 malformed, 0 duplicate ids, 0 enum violations, 0 missing used-by paths; validate exit 0; one frontier ground moves 0 → 3 entries, totals 20 → 23.
