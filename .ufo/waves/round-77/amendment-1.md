# Round 77 — Amendment 1 (terms-only; recorded before any after-state)

Written after the wave's read-only recon seats (`ScoutSurface`, `ScoutSources`) reported, and before any
after-state measurement exists. It settles ten ambiguities the frozen contract left open and freezes two
check scopes. No target, predicate, kill rule or claim sentence changes; the C2 case **expectations** that
change are re-measured at the base after this amendment, so the base receipt quoted by the round is the
post-amendment base.

## C2 — container/format readings

- **A1. G1's quote is two S012 sentences, never one spliced one.** `sitemaps.org/protocol.html` states the
  XML limit and the gzip allowance at lines 177–180 of the retained stripped text; the contract's rendered
  "the file once uncompressed must be no larger than 52,428,800 bytes" is not contiguous in the source.
  Quote 177 and 179–180 separately. Applying the decompressed-size limit to **every** container (text and
  feed bodies included) is this lane's reading, stated as such in the tool docstring and the knowledge
  entry, not attributed to S012.
- **A2. `text_line_not_url` rests on S012:263** ("The text file must have one URL per line"), not on the
  no-header/footer sentence, which is a SHOULD (S012:271–272) and motivates rather than requires the id.
- **A3. A UTF-8 BOM is stripped in the text path as a lane convention** (the XML path already strips one),
  so `t07` is clean. The entry states the convention in those words.
- **A4. `lastmod_invalid` for a malformed feed date is lane policy.** S012 states no validity rule for
  `<pubDate>`/`<updated>`; the XML `<lastmod>` W3C-Datetime sentence is a SHOULD. The entry says so.
- **A5. One condition, one id.** A file whose bytes exceed 52,428,800 **after** container expansion emits the
  existing `too_large` (round-39 behaviour, pinned by the delivered selftest's `lim_too_large`). Case `g02`'s
  expected finding id is therefore `too_large`; `sitemap_too_large` is dropped.
- **A6. A truncated or invalid gzip stream is a check *error* `gzip_invalid`** (exit 2,
  `could-not-evaluate`), never a finding.
- **A7. Root dispatch is namespace-qualified.** `rss` is the unqualified RSS 2.0 root; `feed` is
  `{http://www.w3.org/2005/Atom}feed`. A sitemaps-namespaced `<feed>` stays `root_invalid`, which keeps the
  delivered selftest's `root_wrong_local` and `root_invalid_suppresses_entries` fixtures green.
- **A8. No entry-count rule is claimed for syndication feeds.** S012 states 50,000 for XML sitemaps and text
  files only; a feed over that count is a recorded gap, not a rule, and no case covers it.
- **A9. `format_unsupported` is a lane convention** (no S012 line names an unsupported format or an exit
  alphabet). It is a check error at exit 2. Case `d01` is built **without** a doctype: the doctype gate runs
  before the root gate, so an HTML document with a doctype would decide `doctype_present` instead.
- **A10. Entry keys.** Text findings carry the 1-based line number and feed findings the 1-based item index
  as `entry`, matching `_evaluate_check`'s sort key.

## C1 — frozen check scopes

- **A11. Box checks are frozen at these scopes** (chosen before the ledger existed, from the recon seat's
  counts at base):
  - box 1 — (i) every `S###` cited in `SKILL.md` is a row of `corpus/SOURCES.md`; (ii) `SKILL.md` carries at
    least 3 markdown tables with ≥3 data rows; (iii) at least 20 rows of the SKILL.md registry carry an
    exit-code or finding-id cell (the row form of "error patterns", since no heading names them); (iv) at
    least one heading names a checklist.
  - box 2 — (i) `LOG.md` carries at least 3 round sections; (ii) at least 20 distinct `.ufo/waves/round-N/…`
    receipt paths are named there; (iii) **every** path so named that is not a glob exists at the measured
    revision.
  - box 3 — every `scripts/*.py|sh` and every counter path named in `SKILL.md` exists at the revision, and
    every `python3 -B <path>` invocation names an existing repo-relative path.
  - box 4 — no `corpus/knowledge/*.md` file cites another lane's repository path. `corpus/knowledge/freshness-*.json`
    are named probe registries, not entry prose: they are excluded by name, and the exclusion is written in
    the ledger row rather than applied after a red result.
- **A12. A gap is a result.** If a frozen check fails at the measured revision, the box is `gap` with the
  failing observation, a `reason` and a `flip`; it is never ticked and the counter's `met` is unaffected.
  Box 2 is expected to be a gap at base: `LOG.md` names
  `.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt`, which does not exist at `a2cc5f51`.
