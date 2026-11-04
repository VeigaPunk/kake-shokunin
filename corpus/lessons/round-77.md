# Round 77 — lessons (kake, attempt 1)

Base `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68` (lane `master` tip at round open, 2026-11-03). Frozen
contract `.ufo/waves/round-77/contract.md` (`bc2e5fb9`), frozen before any seat ran. Amendments 1 and 2
(terms-only, recorded before any after-state) land at `893b0f33`. Carrier measured: `3db64e09`. Wave `w1`:
one v1 wave, 14 seats — scout 2, executor 4, scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1,
sentinel 1; attack share 4/14 = 28.6 %; the L1 held the planner seat.

## Claims

**C1 — calibration (score 2, the lane's lowest non-retired axis; HOLD).** Each of the four `SHONEN.md` boxes
is classified by the lane's own counter from committed bytes at one named revision: every recorded
observation is re-derived, a box with no row is unexamined, and a box whose evidence is partial is a `gap`
with a reason and a flip rather than a tick. Frozen predicate
`met <=> boxes == 4 and unexamined == 0 and mismatches == 0`; counter
`.ufo/waves/round-77/c77_shonen_ledger.py` (selftest 26/26).

```sh
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . --revision <rev> [--work <scratch>]
```

Base `a2cc5f51`: `C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=0 met=false`,
exit 1 (`.ufo/waves/round-77/controls/base-c1-ledger.txt`). Carrier `3db64e09`:
`C1 revision=3db64e09550c9f8309f6c1077f9f7df6243cb446 boxes=4 evidenced=3 gap=1 unexamined=0 mismatches=0 met=true`,
exit 0 (`.ufo/waves/round-77/controls/after-c1-ledger.txt`). The gap is box 2 and is honest: `LOG.md` names
98 wave-receipt paths and one of them, `.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt`,
does not exist at the revision.

**C2 — operability (score 10, HOLD; capability acquisition).** `scripts/sitemap_audit.py` decides every case
of the frozen 20-case container/format matrix — gzip container, plain-text sitemap, RSS 2.0 and Atom 1.0
feeds, container-agnostic index `<loc>`s, unsupported roots — with every one of four degenerate constants
failing at least one case. Frozen predicate
`met <=> cases == decided and wrong == 0 and constants_failed == 4`; instrument
`.ufo/waves/round-77/c77_sitemap_matrix.py` (selftest 14/14).

```sh
python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . --tool-revision <rev> \
  --cases .ufo/waves/round-77/cases --consts .ufo/waves/round-77/consts --work <scratch>
```

Base `a2cc5f51`: `C2 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 cases=20 decided=20 correct=2 wrong=18 constants_failed=4/4 met=false`,
exit 1 (`.ufo/waves/round-77/controls/base-c2-matrix-v2.txt`). Carrier `3db64e09`:
`C2 revision=3db64e09550c9f8309f6c1077f9f7df6243cb446 cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true`,
exit 0 (`.ufo/waves/round-77/controls/after-c2-matrix.txt`). The base's XML-only constant is byte-identical
to the base tool (`sha256 914ebdee…`), so the before-state's red is the tool's, not a fixture artefact.

## Gate

- **Admit — S012, sitemaps.org protocol (re-opened).** <https://www.sitemaps.org/protocol.html>, opened
  2026-11-03, HTTP 200, 45,292 B (sha256 `5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654`),
  retained at `.ufo/waves/round-77/w1/ScoutSources/protocol.raw`. Located quote (11 words, §"Using Sitemap
  index files", rendered `protocol.txt:355-357`): "the sitemap file once uncompressed must be no larger than
  50MB". Teaches the decompressed-size limit the container layer enforces. Status `mined`; `used-by` changed
  in place (see Corrections).
- **Admit — S447, RFC 1952 (GZIP file format specification version 4.3).**
  <https://www.rfc-editor.org/rfc/rfc1952.txt>, opened 2026-11-03, HTTP 200, 25,037 B (sha256
  `164ef0897b4cbec63abf1b57f069f3599bd0fb7c72c2a4dee21bd7e03ec9af67`). Located quote (22 words, §2.3.1,
  `rfc1952.txt:240-241`): "These have the fixed values ID1 = 31 (0x1f, \037), ID2 = 139 (0x8b, \213), to
  identify the file as being in gzip format." Teaches the magic bytes that decide the container. `mined`.
- **Admit — S448, RFC 4287 (The Atom Syndication Format).**
  <https://www.rfc-editor.org/rfc/rfc4287.txt>, opened 2026-11-03, HTTP 200, 81,922 B (sha256
  `3bd71d76289560c9e860151f39cebbdc402cfd8b788a62048d8dc42824f2d89c`). Located quote (14 words, §4.2.7.1,
  `rfc4287.txt:943-944`): "atom:link elements MUST have an href attribute, whose value MUST be a IRI
  reference". Teaches the required `href` an Atom entry's URL is read from. `mined`.
- **Reject — "the decompressed-size limit applies to text and feed bodies" as a sourced fact.** S012 states
  the "once uncompressed" clause for the XML sitemap and index only; the text-file limit at 265–266 carries
  no such clause and the text-gzip sentence at 273–274 follows it. Applying the limit to every container is
  this lane's reading and is written in the tool docstring and the entry as such. **Flip:** an opened source
  states the rule for text or feed containers.
- **Reject — feed-date validity as a sourced rule.** S012 names the feed date fields and calls them
  optional; it states no syntax. Accepting ISO-8601 or RFC 822 is lane policy (amendment 1, A4), recorded in
  `corpus/knowledge/sitemap-formats.md` together with two edges: the RFC 822 branch is pinned only by the
  selftest's `r77_rss_rfc822_pubdate`, and a date-only `<updated>` is accepted although S448 §4.2.6 asks
  for a date-time. **Flip:** an opened source fixes the grammar, or a matrix case pins the date-only edge.
- **Reject — "no comment line" as S012's words.** S012 says "should contain no information other than the
  list of URLs" (SHOULD) and never uses the word "comment"; `text_line_not_url` rests on the MUST sentence
  "The text file must have one URL per line" (`protocol.txt:523`). **Flip:** a source states the comment
  prohibition with a MUST.
- **Reject — `format_unsupported` as a protocol rule.** No S012 line names an unsupported format or an exit
  alphabet; the class is a lane convention (amendment 1, A9), and it is a check *error* (exit 2), never a
  policy finding.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| **reference-drift — a receipt named a revision that does not contain the bytes it measured** (round-76 D1, the third round in a row of this class: r75 R3/R7, r76 D1). `after-c2-matrix.txt:4` reads `revision=master revision_ok=yes head=d00ea7fb1471f66bf6067cd6fcb5d82c743159c8` while the tool lands at `2cccd59a`; `git cat-file -e d00ea7fb:scripts/hreflang_audit.py` → `rc=128` | `.ufo/waves/round-76/controls/after-c2-matrix.txt:4`; `.ufo/waves/round-77/controls/r77-hreflang-matrix.txt` (`revision=a2cc5f51… revision_ok=yes`, 69/69 correct) | the round-76 QUALITY criterion required "one revision per artifact" but no instrument checked that the revision *contains* the artifact | `ExecRevisionReceipts` re-ran the matrix at a full hash on the landed digest (three checks: concrete hash, artifact present at that hash, named tool digest equals the blob there) and this round's own receipts name one full hash per artifact |
| **landing — the L1 committed an instrument while its author seat was still writing it.** Commit `893b0f33` captured `c77_shonen_ledger.py` mid-write with a syntax error (`LOG.md=FIXTURE_LOG…`), and the repaired carrier had to land again at `3db64e09` | `git show 893b0f33:.ufo/waves/round-77/c77_shonen_ledger.py` fails `python3 -c 'import ast; ast.parse(...)'`; `3db64e09` is the measured carrier | none — the integration step has no gate | before a carrier commit, parse every committed Python file and re-run its selftest from the committed bytes; the round report cites the carrier hash, never the intermediate |
| **stale-premise — the frozen contract asserted that all five `considerthese/2026-10-26.md` proposals are implemented.** Measured: proposal 1 is unimplemented and proposal 4 exists only as an aggregate number | `.ufo/waves/round-77/w1/ConnectorC.md` §3 (with `corpus/lessons/round-62.md:13`, `corpus/lessons/round-67.md:127-131`) | none; the contract's frontier sentence was written from memory of earlier rounds | the report and this lesson state the measured statuses; `Assimilation`/`considerthese` status is derived each round by the connector, not asserted in the contract |

## Routed dispositions (round-76 closure §6)

| # | Routed item | Status | Pointer | Flip |
|---|---|---|---|---|
| 1 | C2 measured revision and real-input build scope | fixed (evidence, not an edit) | `.ufo/waves/round-77/controls/r77-hreflang-matrix.txt` — 71 cases, 69 decided, 69 correct, 4/4 constants, `revision=a2cc5f51…`, tool digest `0762452f…` equal to the blob at that revision; real-input rerun `controls/r77-hreflang-realrun.txt` | a later receipt names a revision lacking its artifact |
| 2 | Census warning count 16 vs 17 | stated | report §Sources: 17 at `a2cc5f51` = 16 inherited + `S445 duplicate url html.spec.whatwg.org/multipage/links.html across scopes`; the fleet report's text stays operator-owned | the census prints a different count and no round added a row |
| 3 | Report quote rendering (`pages=8 findings=[] exit=0`) | criterion | `corpus/QUALITY.md` §"Round-77 criteria — the report's own evidence" criterion 2; this round's report quotes whole receipt lines only | a report span that is not a committed line |
| 4 | Correction-row count/location (7 vs 5+1+1) | corrected append-only | §Corrections below | — |
| 5 | "frontier to core" wording | corrected append-only | §Corrections below (`git grep -in hreflang a0491fcd -- PROVINCE.md corpus/README.md` → 0) | — |
| 6 | Deletion-control parenthetical | corrected append-only | §Corrections below (`A1 SCORECARD.md:0 …`, `ctl-deletion.txt:8`, no `append_only=` token) | — |

Open, not claimed closed: box 2's missing round-47 receipt; the three `node ~/Projects/webzites/...` spans
and `scripts/kimi-surface.mjs` in `SKILL.md` (outside amendment 1 A11's box-3 scope, still non-executable);
SentinelC F2 (manifest containment is lexical — a symlink escapes it), F3 (a FIFO named by a manifest
blocks the audit), F4 (manifest read without a size bound), F5 (the frozen summary line can be forged
through `--revision`), F6 (`--tool-revision` reaches git's option parser, fails closed); ReviewC2 F3/F4
(feed-date grammar pinned asymmetrically; date-only `<updated>` accepted); A8 (no feed entry-count rule);
the freshness sweep's single `~/projects` drift (open L0 `kake | round-69`).

## Corrections (append-only)

- **D4 — correction-row count.** The round-76 claim row reads "closed by seven whole-line correction rows in
  the section above, one `QUALITY` criterion and one lesson correction"; the section holds **five**
  numbered rows (`SCORECARD.md:4925-4929`), and the other two findings are closed by the `QUALITY` criterion
  and the `round-75.md` bullet: **5 + 1 + 1 = 7**. `[r77-correction 2026-11-03]`
- **D5 — "frontier to core".** `git grep -in hreflang a0491fcd -- PROVINCE.md corpus/README.md` → `0`
  (11 at `a2cc5f51`), so hreflang declarations entered from unlisted ground; the PROVINCE text "are now
  core" is accurate, "entered from frontier to core" is not. `[r77-correction 2026-11-03]`
- **D6 — deletion control.** The round-76 report wrote "deletion (`A1`, `append_only=false`)"; the control's
  line 8 is `  A1 SCORECARD.md:0 claim row present at --base is gone at the measured revision` — `A1` only,
  no `append_only=` token. `[r77-correction 2026-11-03]`
- **D2 — census count.** The round-76 report's "same 16 pre-existing `W04` duplicate-URL warnings" reads 17
  at its own tip: 16 inherited plus the S445 row that round added. `[r77-correction 2026-11-03]`
- **Registry updates (old → new).** S012 `used-by`:
  `corpus/knowledge/crawl-scope-per-host.md` → `corpus/knowledge/crawl-scope-per-host.md, corpus/knowledge/sitemap-formats.md, corpus/lessons/round-77.md`;
  status `mined`, `recheck 365d`, `opened 2026-10-19` unchanged. Rows S447 and S448 added; registry
  184 → 186; `W04` count 17 → 17 (16 inherited + S445, no new duplicate URL).
  `[r77-correction 2026-11-03]`

## Sources

- **S012**, sitemaps.org protocol — re-opened 2026-11-03 (HTTP 200, 45,292 B, sha256 `5e757059…`), the
  formats, gzip and text-limit sentences the C2 readings rest on. Row updated in place (`used-by`).
- **S447**, RFC 1952 — opened 2026-11-03 (HTTP 200, 25,037 B, sha256 `164ef089…`), the gzip member header,
  magic bytes, CRC32/ISIZE trailer and the header checks a decompressor must make.
- **S448**, RFC 4287 — opened 2026-11-03 (HTTP 200, 81,922 B, sha256 `3bd71d76…`), `atom:link`'s required
  `href` and the `atom:updated` Date construct.
- C1 rests on lane instruments and committed receipts, not on a web source: the predicate is contract §C1 as
  amended, the counter `.ufo/waves/round-77/c77_shonen_ledger.py`, the ledger
  `corpus/knowledge/shonen-ledger.json`, and the controls under `.ufo/waves/round-77/controls/`.
- Assimilation: none. The `merge/kake` package's 129 staged rows carry 8 ids already occupied by different
  content (`.ufo/waves/round-77/assimilation/collisions`), 121 staged ids are free and no renumber map is
  produced; adoption stays closed this round (`w1/ConnectorC.md` §2).
