# ScribeGroundMap

Claim C3 support (leaf seat, read-only). Drafted the two corpus index edits a round-59 C3 build needs
(one coverage-map row per new entry, one frontier-ground-map row for the Google verification step), the
PROVINCE question, and the landing order that keeps the round-55 index counter green.

## Behavior

- Read only: `corpus/README.md`, `PROVINCE.md`, `corpus/knowledge/crawler-identity.md`,
  `corpus/SOURCES.md` (rows S423/S424), `.ufo/waves/round-59/{contract.md,contract.json}`,
  `.ufo/waves/round-59/c59_quote_truth.py`, `.ufo/waves/round-59/w1-spec.json`,
  `.ufo/waves/round-55/c55_readme_index.py`. No lane file created or modified except my report and
  `.files/`. No git/jj mutation, no counter of this round scored, no entry/registry/lesson text authored.
- Instrument runs (evidence, not scoring): `python3 -B .ufo/waves/round-55/c55_readme_index.py --root .
  --revision HEAD` -> `index_mismatches=0 knowledge_files=56 met=True … coverage_rows=58 EXIT=0`
  (the committed lane HEAD, i.e. the wave's base state, not an after-state). Plus a scratch git fixture
  (52 knowledge files, one stale `crawler-identity.md`, every knowledge file indexed); transcript in
  `ScribeGroundMap.files/c55-ordering-receipt.txt`. `c59_*` counters were not run against the lane.
- Counters are version 1 and the wave attacks them first; nothing here measures C1/C2/C3.

## CURRENT:

`corpus/README.md` (line numbers as committed at base `fd6303ce`):

```
53|| Crawler identity (Googlebot subtypes) | `knowledge/crawler-identity.md` (S263) | Googlebot names two crawlers, Smartphone and Desktop; the HTTP user-agent header identifies the subtype, and both types obey the same robots.txt product token; it also lists what the entry does not establish. |
76|| Baiduspider unblocking (r58) | `knowledge/baidu-spider-unblocking.md` (S424) | Baiduspider unblocking: the three block classes the page names (robots.txt, the Baidu user agent, an IP-level firewall block), the curl head request under a Baiduspider user agent whose 200 answer it calls normal, and the remedies it names (strategy change, user-agent whitelist); no unblock observed |
77|(blank — last coverage-map row is 76; `### Frontier ground map` heading follows)
78|### Frontier ground map (round 55; round-58 update)
86|at the round-58 final revision (162 rows, S423 and S424 added), not at base `0440485…`. Ranges
108|| Crawler identity (Baidu: UA + two-step DNS; unblocking) | r58 (lands this round) | `knowledge/baidu-spider-identification.md` `knowledge/baidu-spider-unblocking.md` | S423 S424 |
109|| Field performance (CWV, CrUX) | r28 | `knowledge/field-performance-cwv.md` | S036–S039 |
126|round-58 row's two entry paths are absent at its base `0440485…`, and S423 and S424 are not in
127|that registry.
147|`PROVINCE.md:344`, canonical selection and crawler identity `PROVINCE.md:361`,
148|the eleven per-engine entries (the round-52 trio `PROVINCE.md:382`, the round-55 Yahoo! robots trio
```

The counter parses only the first contiguous table after `## Coverage map` (`corpus/README.md:8`), but
its dangling scan reads every backticked token of the whole `## Coverage map` section (coverage table
plus frontier ground map plus prose). `corpus/knowledge/` holds 56 files; the two round-59 entries do
not exist yet.

## PROPOSED EDITS:

E1 — insert two rows after line 76 (three cells, no `|` inside a cell; one file token per row, so
`multi` stays 0; distinct from the line-53 cell so `duplicate` stays 0):

```
| Crawler identification signals (r59) | `knowledge/crawler-identity-signals.md` (S425) | Google's three identification signals as the page states them: the user-agent request header, the source IP address and the reverse DNS hostname; several IP addresses per crawler; US egress and the fallback when US requests are blocked; the pointer to the verification page |
| Googlebot verification (r59) | `knowledge/googlebot-verification.md` (S426) | Googlebot verification as the page states it: the two methods (manual command line and automatic IP-list match), the reverse DNS then forward DNS two-step check against the three domain masks, the printed worked examples and the crawler-category range files |
```

E2 — insert one row after line 108 (frontier ground map shape, 4 cells):

```
| Crawler identity (Google: identification signals and verification procedure) | r59 (lands this round) | `knowledge/crawler-identity-signals.md` `knowledge/googlebot-verification.md` | S425 S426 |
```

E3 — line 78: `### Frontier ground map (round 55; round-58 update)` -> `### Frontier ground map (round 55; round-59 update)`.

E4 — replace line 86 by two lines:

```
at the round-58 final revision (162 rows, S423 and S424 added), not at base `0440485…`; the round-59 row
at the round-59 final revision (164 rows, S425 and S426 added), not at base `fd6303ce…`. Ranges
```

E5 — replace lines 126-127 by four lines (insert-only):

```
round-58 row's two entry paths are absent at its base `0440485…`, and S423 and S424 are not in
that registry; the
round-59 row's two entry paths are absent at its base `fd6303ce…`, and S425 and S426 are not in
that registry.
```

E6 — optional, not required: after `the round-57 Baidu pair` / `PROVINCE.md:441` in line 149, add
`, and the round-59 Google identity pair (new row above)`. The `eleven per-engine entries` count stays
11 (round 59 is identity ground, already named generically at line 147), so a count rewrite is wrong.

Why E1's cells pass the counter: `thin` needs >= 5 words plus one shared word that is not common
(common = present in >= 40 % of knowledge files, i.e. 23 of 56). Measured frequencies at HEAD: `signals`
4, `hostname` 2, `verification` 10, `address` 0, `reverse` 0, `crawler` 10, `google` 11 — none common.
The shared word must occur in the entry's H1 + first 1500 chars, which the entry seats control; if an
entry's head wording diverges, re-derive the cell's tail from the committed H1 rather than adding filler.
Check after landing: `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision <R2> --json`
must show `unindexed=[] dangling=[] thin=[] duplicate=[] multi=[] head_changed=[] deleted=[]`,
`knowledge_files=58`, `coverage_rows=60`, exit 0.

S425's `used-by` is the entry plus `corpus/knowledge/crawler-identity.md` (contract C4). Keep the r51
row (line 97) at S263 and do not add `crawler-identity.md` to E2's Entries cell: it is not a round-59
entry, and the map's row set is the used-by cells of the entries the row names.

## ORDERING:

The counter resolves README pointers against the `--revision` tree and requires every knowledge file to
be indexed at that same revision, so the entries and the rows must coexist at the measured revision,
and the C9 insertion must come after it.

1. R1: land the two entries (`corpus/knowledge/crawler-identity-signals.md`, `…/googlebot-verification.md`),
   the S425/S426 registry rows and the round-59 lesson `## Gate`. At R1 the index counter reports
   `unindexed=[both new files]` — expected; do not record R1 as the index measurement.
2. R2 (R1 itself if one commit): land E1–E5. Every new token now resolves and every knowledge file has a
   row: fixture B2 (`ScribeGroundMap.files/c55-ordering-receipt.txt`) reproduces exactly this state and
   exits 0, `met True`, all seven lists empty.
3. Run and record the index counter at R2 by id (it takes any `--revision`; record the sha, because later
   commits will move the tip).
4. LAST: land the C9 insertion in `corpus/knowledge/crawler-identity.md` (inserted lines after the stale
   bullet, no base line changed). It is mid-file, so `new.startswith(old)` is false and the counter
   reports `head_changed=["crawler-identity.md"]` at every later revision — fixture B3 shows exit 1 with
   exactly that term and nothing else. If the insertion must precede R2, then no revision can be green:
   report `head_changed` as the append-only test's known false positive for an insert-only mid-file
   correction, do not move the insertion to EOF (C9 needs it within 8 base lines of the stale sentence),
   and do not claim the index counter met.
5. Evidence for the reverse order: a revision carrying E1/E2 but not yet the entry files yields
   `dangling=['knowledge/crawler-identity-signals.md','knowledge/googlebot-verification.md']`
   (fixture B1) — the frontier row's tokens are scanned too, so E2 cannot land early either.

The counter has no `--base` flag (it hard-codes `BASE_REV = fcaf4b85…`), so it cannot be re-baselined in a
fixture; the fixture used the module's `measure(root, rev, base_rev=…)` directly.

## PROVINCE:

Lines 22-23, verbatim (the `Crawl hygiene per host` bullet the frontier map anchors to `PROVINCE.md:22-30`):

```
- Crawl hygiene per host (robots.txt, sitemap scope, canonical signals) — first
  entry `corpus/knowledge/crawl-scope-per-host.md`; canonical/JS rendering open.
```

No line change. Rounds 51 and 58 put the crawler-identity ground under this bullet and left these bytes
identical (`PROVINCE.md:451`: "the `Crawler identity` ground (round-51 Googlebot subtypes row;
`PROVINCE.md:22-23` unchanged)"); round 59 continues that ground, so rewriting the bullet would
retroactively change two rounds' reading and shift every line the README cites (`PROVINCE.md:361`,
`:382`, `:397`, `:423`, `:441`). The round-59 record therefore belongs in a new `## Round-59 …` section
appended after the current last block (`PROVINCE.md:449-460`), which keeps 22-23 and all cited line
numbers stable. Appending that section is the L1's edit, not this seat's; if the L1 prefers to name the
ground in the Frontier bullet instead, the oldest anchor in the frontier map (`PROVINCE.md:22-30`) and
the README's "Untouched ground" citations must be re-derived in the same commit.

## Out of scope / findings

- Not mine, not done: the two entry files, S425/S426 registry rows, lesson `## Gate`, the C9 insertion
  text, the PROVINCE round-59 section, the README write itself, any commit/measurement of C1–C3.
- F1 the round-55 append-only test and the round-59 C9 mid-file correction are mutually exclusive at one
  revision; ordering (not a text change) is the only fix — see ORDERING 3-4 and receipt B3.
- F2 `c55_readme_index.py` exposes no `--base`; evaluable only inside the lane (base `fcaf4b85` present).
- F3 the dangling scan covers the frontier ground map and the prose, not just the coverage rows (B1).
- F4 `c59_quote_truth.py` still has the version-1 selftest stub (`exit 2`, "not yet ported") at the base
  revision; the wave's attack seats own that, reported here only as observed.
- Touched surfaces: `.ufo/waves/round-59/w1/ScribeGroundMap.md` and
  `.ufo/waves/round-59/w1/ScribeGroundMap.files/c55-ordering-receipt.txt`. Scratch
  `/fast/scratch/hyaku/kake-r59/ScribeGroundMap/` deleted (receipt copied out first). Tooling: none
  installed or upgraded.

VERDICT: Two coverage rows (S425, S426), one frontier ground-map row, heading/intro/paragraph inserts and no PROVINCE line change are ready to paste; land entries first, README rows second (measure the index counter there), the C9 mid-file insertion last.
