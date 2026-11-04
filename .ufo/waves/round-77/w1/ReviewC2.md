# ReviewC2 — adversarial review of C2 (kake round 77, wave w1)

Seat: ReviewC2 (reviewer, leaf). Date: 2026-11-03. Base `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`.
Scratch: `/fast/scratch/hyaku/kake-r77/ReviewC2` (removed after this report; receipts embedded below).
Everything I ran was read-only against the lane; the only file I wrote is this one.

**Tree-state caveat.** The wave was amended *while I reviewed*. Observed mtimes (all `-0300`):
`amendment-1.md` 22:44:28, `amendment-2.md` 22:44:52, `c77_sitemap_matrix.py` 22:46:54 (29,293 B),
`cases/g03/expect.json` 22:41:01 (sha256 `544db951…`). A `--verbose` run at ~22:55 was **refused**
(see F6); my successful counter runs measured the 22:46:54 counter version against then-current case
bytes. Every receipt below names the exact bytes it measured. Nothing here redefines a frozen claim;
findings are recommendations.

## Findings

### F1 — HIGH (instrument gap): the matrix does not decide G2 (magic, not name)

All four gzip-content payloads are named `*.gz`:

```
$ ls cases/g01 cases/g02 cases/g03 cases/g04 cases/t06   (payload lines)
g01: sitemap.xml.gz   g02: sitemap.xml.gz   g03: sitemap.xml.gz
g04: sitemap.xml.gz   t06: sitemap.txt.gz
```

A tool that dispatches the gzip container by **file name** (not magic) is indistinguishable from a
magic-dispatching tool on this population. Receipt — a name-gated wrapper (delegates to the real tool
except when name and magic disagree) through the delivered counter (22:46:54 version):

```
$ python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . --tool <wrapper> \
    --revision NAMEGATED-PROBE --cases .ufo/waves/round-77/cases --consts .ufo/waves/round-77/consts \
    --work $S/tmp/counter_wrap
C2 revision=NAMEGATED-PROBE cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true
```

The wrapper provably violates G2 — on a synthetic gzip-magic payload named `bundle.bin` (my own file,
built to S012's rule "once uncompressed must be no larger than 50MB", 2 valid entries):

```
candidate:  {"verdict":"clean",...}                                  exit 0   (correct per G2)
wrapper:    {"verdict":"failed-policy","findings":[{"code":"encoding_invalid"}]}  exit 1
```

Mitigation that exists: the delivered selftest's `r77_gzip_magic_reads_body` uses a gzip payload named
`a.txt`, so a name-gated tool fails the selftest (candidate `PASS 266/266`). But the C2 *measurement
instrument* stays green for a G2-violating tool. Fix inside contract bounds ("bytes built in-wave";
ids/expectations/population unchanged): rename one gzip-content payload to a non-`.gz` name (g01 is the
natural choice — its manifest `sitemapUrl` may keep any form), leaving g04 as the only `.gz`-named
plain case, which sharpens the g01/g04 pair into the G2 decision.

### F2 — MEDIUM (false source citation): "(S012)" claimed for RFC 822 pubDate

`scripts/sitemap_audit.py` (candidate, working tree) `_valid_feed_date` docstring:

```
RSS 2.0's `<pubDate>` is an RFC 822 date (S012), which `email.utils` reads.
```

S012 (fresh GET, 2026-11-03: 45,292 B, sha256 `5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654`
— identical to the frozen round-open receipt) states **no feed date syntax**. Its entire date sentence
for feeds is: "modified date field (the `<pubDate>` field for RSS feeds and the `<updated>` date for
Atom feeds) - indicates when each URL was last modified. Use of the modified date field is optional."
The RFC 822 requirement comes from the RSS 2.0 spec, which is not among the round's sources
(S012/S447/S448). Amendment-1 A4 itself says "S012 states no validity rule for `<pubDate>`/`<updated>`"
— the docstring contradicts the wave's own amendment. Fix: drop "(S012)" or open the RSS 2.0 spec as a
source row and cite that.

### F3 — MEDIUM (grammar pinned asymmetrically): no case exercises an RFC 822 pubDate

`cases/r01/feed.xml` (landed bytes) uses ISO shapes: `<pubDate>2026-11-02T10:00:00Z</pubDate>` and
`2026-11-02T11:00:00Z`. `r03` uses prose (`not-a-date`), invalid under any grammar. So the matrix
decides "ISO pubDate accepted" and cannot decide "RFC 822 pubDate accepted" — an implementation that
accepts **only** ISO (rejecting every real-world RSS 2.0 feed's dates) passes r01/r03/a01–a03. The
tool documents and implements the RFC 822 branch (`email.utils`), but the instrument cannot verify it.
Per A4 (feed-date validity is lane policy) this is admissible only if the knowledge entry states the
accepted grammar in so many words; recommend the entry say exactly: both ISO-8601 and RFC 822 accepted;
and consider one RFC-822-shaped clean case if the population is ever amended.

### F4 — MEDIUM-LOW (S448 deviation, unpinned): date-only `<updated>` accepted

RFC 4287 (S448) §4.2.6 requires `atom:updated` content to be an RFC 3339 **date-time**; the candidate
reuses the sitemap `lastmod` rule, which accepts date-only. Receipt (my file):

```
$ cat f4.json  ->  {"id":"f4demo","file":"dateonly.xml",...};  dateonly.xml =
  <feed xmlns="http://www.w3.org/2005/Atom"><entry><link href="https://example.com/a"/>
  <updated>2026-11-02</updated></entry></feed>
$ python3 -B scripts/sitemap_audit.py --manifest f4.json
{"version": 1, "verdict": "clean", ...}          exit 0
```

No landed case pins date-only (`a03`'s malformed value is `2026-13-45T99:99:99Z`, invalid under both
readings). The frontier step opens S448 as a source row, so an unrecorded deviation from it is a
grounding inconsistency: record the deviation in `corpus/knowledge/sitemap-formats.md` (or add a case).

### F5 — LOW (receipt provenance): the after-state I measured is uncommitted bytes

My candidate receipt below was produced against the **working tree**, not a commit:

```
$ python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . --tool scripts/sitemap_audit.py \
    --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --cases … --consts … --work $S/tmp/rc
C2 revision=a2cc5f51… cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true   (exit 0)
```

`git status` shows `scripts/sitemap_audit.py` and `scripts/sitemap_audit_selftest.py` modified; the
`--revision` flag records the label, it does not check out the tool. Per the contract (D1 repair:
"C2 re-run at a full-hash committed revision") the quoted round receipt must be re-produced at the
committed hash by `ExecRevisionReceipts`. Also `controls/` currently holds only hreflang-named files
(`r77-hreflang-matrix.txt`, `r77-hreflang-realrun.txt`) — no C2 matrix receipt has landed yet.

### F6 — MEDIUM (transition flux): amendment A5/A6 not yet reflected in bytes; counter refuses mid-flight

Amendment-1 A5 renames g02's expected id to `too_large` ("`sitemap_too_large` is dropped") and A6 sets
the gzip fault id to `gzip_invalid`; the landed bytes still carry the pre-amendment values
(`g02/expect.json` → `sitemap_too_large`; tool emits `sitemap_too_large` / `gzip_corrupt`), and the
counter has been edited at least twice during this review (a `--verbose` run at ~22:55):

```
c77_sitemap_matrix: cannot evaluate: …/cases/g03: an exit-2 case must name its input-fault error code
                     (exit 2; g03/expect.json still has "findings": [])
```

An import of the counter at ~22:47 caught a torn file (SyntaxError: unterminated triple-quoted string,
line 451→679). No receipt should be quoted by the round until bytes, amendment text, and counter agree
at one frozen instant, and the base receipt is re-measured post-amendment (amendment-1's own promise).

## Verifications that held (per assigned surface)

1. **Does each case decide the rule it names?** Mostly yes; two gaps (F1, F3). Positive discriminators
   verified in the landed bytes: t02 `# comment` → `text_line_not_url`; t03 `/page` →
   `text_url_not_absolute`; t04 empty → `text_empty`; t07 UTF-8 BOM (`ef bb bf`, xxd receipt) → clean;
   r03 `not-a-date` and a03 `2026-13-45T99:99:99Z` → `lastmod_invalid` under any grammar; d01 is
   doctype-free `<html>` → `format_unsupported` (A9's ordering hazard avoided — my probe of a
   doctype'd html doc at base fired `doctype_present` first, so the doctype-free build is the right
   byte choice); s01 index with `.txt/.rss/.atom` locs → clean, grounded in S012:884 ("This location
   can be a Sitemap, an Atom file, RSS file or a simple text file").
2. **Are expectations grounded in S012?** Fresh GET matches the frozen receipt byte-for-byte (sha256
   above). G1 verified ("…the sitemap file once uncompressed must be no larger than 50MB"; note A1 is
   right that the contract's 52,428,800 splice is not contiguous — the byte figure lives in the
   XML-limit sentence); T1 verified (one URL per line, fully specified incl. http, UTF-8, ≤50,000,
   ≤52,428,800; the no-header/footer clauses are SHOULDs — A2 correctly re-grounds `text_line_not_url`
   in the must-sentence); F1/F2 roles verified (link/pubDate/updated, optional); F3 verified (884);
   G2's magic is S447's, not S012's (contract says so); X1 is lane convention (A9 says so). Two
   grounding defects found: F2, F4.
3. **Does the base really fail the new cases?** Yes — on committed bytes, not a malformed-file
   artifact. Base copy extracted with `git show a2cc5f51:scripts/sitemap_audit.py` (657 lines, no
   `import gzip`):

   ```
   C2 revision=a2cc5f51… cases=20 decided=20 correct=2 wrong=18 constants_failed=4/4 met=false  (exit 1)
   ```

   The 2 green are g04 and s01 (correct — base reads plain bytes and index XML already). Container-only
   red proofs: g01 decompressed (205 B) audited by base → exit 0 clean; g02 decompressed → base exit 1
   `too_large`. My hand-built 20-case map agreed case-by-case. **Kill-rule load-bearing receipt:** 10 of
   the 18 reds differ only by finding id (g02 `encoding_invalid`≠`sitemap_too_large`; t02–t05
   `xml_malformed`≠text ids; r02/r04/a02/a03, r03/a03 `root_invalid`≠feed ids) — under exit-only
   comparison base would look 12/20 green.
4. **Can a shape-only stub pass?** Echo-level, no: the tool receives only `cases/<id>/manifest.json`
   (id/file/sitemapUrl — verified by `cat`); expectations live in `expect.json`, which `observe()` never
   hands over. My echo stub, run against expectation-free manifests, degenerates to always-clean and
   fails every finding-case under the id-set judge. The judge compares exit + sorted finding-id set +
   error-present for exit-2 cases, and requires named fault codes when the expectation names one
   (12/12 counter selftest incl. wrong-expected, crash→undecided, exit-two-needs-error-status,
   empty-expect, mixed-fault fixtures — exit 0). Constants each fail ≥1 case (`constants_failed=4/4` in
   base and candidate runs). **Residual:** a hardcoded 20-row stub would still pass the counter; the
   only catcher is the delivered tool selftest (base 235/235 → candidate 266/266, exit 0), which is in
   the wave's edit surface — the committed selftest diff must be reviewed to keep the round-39 coverage
   (base's 235 cases) plus the r77 additions I verified present (gzip magic-reads-body, .gz-name plain
   body, 1-byte-over bomb, exact-limit clean, truncated stream, text/feed cases).
5. **Is the decompressed-size rule enforced on decompressed bytes?** Yes, verified at code level and by
   a real receipt. Candidate `_load_payload`: magic `b"\x1f\x8b"` check, then
   `stream.read(MAX_BYTES + 1)` (bounded — a bomb is never buffered whole) plus a 1-byte EOF read to
   verify CRC/length; `_audit_file` applies the limit to the decompressed `data`. Landed g02 is a real
   >50MB case: compressed 51,139 B → decompressed **52,428,801 B** (exactly one byte over) → candidate
   emits the over-size finding, exit 1. Base applied the limit to raw file bytes only
   (base `_audit_file`: `handle.read(MAX_BYTES + 1)` → `too_large`; gzip bytes died earlier at
   `encoding_invalid`).

## Residual risk and verification gaps

- Measured candidate bytes are uncommitted (F5) and the counter/cases were still converging at review
  time (F6): the `met=true` line above is evidence the *design* reaches the target, not the round's
  receipt. The canonical re-run at the committed hash is still owed.
- Name-gated dispatch passes the frozen instrument (F1) until one payload is renamed.
- Hardcoded-table stub: undetectable by execution; selftest diff review is the control.
- Unpinned edges, accepted by the frozen population: multi-member gzip and trailing garbage after a
  member; feed entry counts (recorded gap per A8); date-only `<updated>` (F4); RFC 822 pubDate branch
  (F3).
- I did not run any tool installs; no tooling changes to record.

## Addendum — post-review responses verified (2026-11-03, ~23:0x -0300)

ExecSitemapFormats answered all findings; every byte claim re-verified against the current tree:

- **F2 RESOLVED.** `scripts/sitemap_audit.py` sha256 is now `742c2ab18c7ef0f7cbcc654a06a9f27b639b9d3d2ed5b18d96934dac90446cab`; the `_valid_feed_date` docstring no longer cites "(S012)" — it now reads "S012 states no feed-date validity rule, so accepting either form is lane policy (amendment 1, A4)" (verified by grep, lines 386–392).
- **F6 bytes converged.** `cases/g02/expect.json` → `["too_large"]`, `cases/g03/expect.json` → `["gzip_invalid"]` (cat receipts); the executor's tool/selftest bytes carry the A5/A6 ids; executor reports a worktree counter preview of 20/20, constants 4/4. The refusing `--verbose` state I observed is expected to be gone; the canonical run at the committed hash is still owed (F5).
- **F3 mitigation verified in tool+selftest.** The RFC 822 branch is implemented and selftested (`r77_rss_rfc822_pubdate`, RFC-822-shaped date, clean); selftest is now `PASS 267/267` (sha256 `82a587e3de77a1d95c2bec7ff33ec962c809b2229662ada61d08a9f62c4a0d62`), re-run by me. A matrix case remains ExecMatrix's surface (my recommendation stands: one RFC-822-shaped clean case would pin the branch in the instrument).
- **F4 reclassified as intentional lane policy.** Contract F2's own sentence checks `<updated>` with "the existing date validation" (`_valid_lastmod`), and A4 makes that lane policy; recording the S448 deviation in `corpus/knowledge/sitemap-formats.md` is ScribeSources' item. Downgraded from defect to documentation dependency.
- **F1 UNCHANGED (open, with ExecMatrix).** The executor confirms the tool dispatches by magic (`r77_gzip_magic_reads_body` fails without the branch) and relayed the population gap: cases/ is ExecMatrix's edit surface. The instrument gap stands until one gzip payload loses the `.gz` name.
- **F5 UNCHANGED.** Executor's run is worktree-only; the frozen receipt requires the committed full hash.

Selftest re-verification receipt (mine, final bytes): `PASS 267/267`, exit 0.

**Supersession (2026-11-03, later):** the executor landed a final byte change after my verification —
tool sha256 is now `f767af770652437d7af18c693dff7cafd64d7f79c38cec36a20e6c4e0bbe9176` (901 lines),
selftest `f22e0a67d777ce80ce2d1099520f50f98016c28901e77b7cb5e4b73c386b9c89`. Re-verified by me: hashes
match, 901 lines, the three new SentinelC file-plumbing guards are present (realpath containment,
non-blocking open, bounded manifest read — 5 grep hits), and the selftest passes `271/271` on the new
bytes. Finding statuses are unchanged (no semantics or finding ids moved; g02/g03 ids stayed
`too_large`/`gzip_invalid` per the executor; matrix preview 20/20, constants 4/4 per executor).

## Commands-of-record (all under $S=/fast/scratch/hyaku/kake-r77/ReviewC2)

Counter runs quoted above used the frozen form from the contract with `--work $S/tmp/…`. Base copy:
`git -C <lane> show a2cc5f51002433e11cc3d2f70e650a6c60ad5e68:scripts/sitemap_audit.py > $S/base_sitemap_audit.py`.
Selftests: `python3 -B scripts/sitemap_audit_selftest.py --tool <tool>` (base `PASS 235/235`, candidate
`PASS 266/266`); `python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --selftest --root .` →
`selftest 12/12 passed`. S012: `curl -sSL --max-time 30 https://www.sitemaps.org/protocol.html` →
45,292 B, sha256 `5e757059…` (public GET, per authorization).
