# Review — "Round-34 wave-1 additions" section of corpus/knowledge/link-preview-metadata.md @ 24a1647

Verdict: every checkable claim in the appended section holds against the named
evidence. No defect found. Sandbox: /fast/scratch/hyaku/kake-r34/w2/ReviewEntryWave1Additions/
(extracted html.tar.xz, recount script output below). No installs; no network; no lane writes besides this file.

## Per-claim verdicts

1. S073 quote "No code is executed, so tags added by a client-side script after load are never seen."
   VERIFIED — exact substring of .ufo/waves/round-34/sources/S073.txt (grep -o hit, line 1).
2. S073 quote "The key comes from name if present, otherwise from property" — VERIFIED, exact substring
   (retained text carries a trailing space before the period, outside the quoted span).
3. "a <meta name=\"og:image\"> counts on Discord" — VERIFIED: S073.txt Tag Reference table maps
   "og:image , og:image:url , og:image:secure_url , twitter:image , twitter:image:src" to the
   image field, and the key rule at (2) accepts name=. Lane tool's property-only policy confirmed
   at scripts/link_preview_audit.py:29-31,80 (24a1647).
4. "102 pages are hand-authored static HTML; the Pages workflow uploads the directory as-is and no
   script emits Open Graph tags" — VERIFIED: upstream pages.yml @7fc6aa2f runs validators/tests then
   `actions/upload-pages-artifact@v3` path ./ds4cc-marketplace, no HTML build step; provenance
   commit e38da85 "magga: canonical+og+description head metadata on 73 pages" confirmed.
   "Hand-authored" is the scout's inference from absent template machinery, plausible, marked as such.
5. "15 pages without title/type/url triple = 11 burnerchrome/ + bloat.html + burnerchrome.html +
   exa.html + benchmarks/benxshitter-frontier.html" — VERIFIED by independent recount over retained
   html.tar.xz (102 members extracted to sandbox): exactly these 15 have zero og:* tags; the other
   87 all carry the triple.
6. "burnerchrome.html (a zero-second refresh shim)" — VERIFIED: `<meta http-equiv="refresh"
   content="0; url=/burnerchrome/">`, canonical https://ds4cc.com/burnerchrome/.
7. "no site-wide default raster image" — VERIFIED: `git ls-tree --name-only 7fc6aa2f` shows
   assets/fonts only; root-level raster/ico grep empty (exit 1). 82 rasters exist in subdirs
   (e.g. omegag/assets/masterpiece.png) — claim is about a default, holds.
8. "all 87 og:url values equal their canonical link and their own sitemap loc" — VERIFIED by my
   own recount: og:url==canonical 87/87, og:url ∈ sitemap locs 87/87, zero mismatches
   (sitemap sha256 55cb947f… matches upstream 7fc6aa2f:sitemap.xml per w1 scout).
9. "bloat.html and exa.html declare canonicals https://ds4cc.com/bloat and /exa while the sitemap
   lists …/bloat.html and …/exa.html; neither has og:url" — VERIFIED: canonicals confirmed via
   git show; sitemap.xml contains `<loc>https://ds4cc.com/bloat.html</loc>` and `…/exa.html</loc>`;
   no og:url on either (grep + recount). "Not checked whether extensionless resolves" is honest.
10. Real-input bullet (exit 1; 101 missing og:image; 15 each missing title/type/url; no other
    finding) — VERIFIED verbatim against verification/real-input-at-5613071.json (toolExit 1,
    observed counts identical, agrees:true).
11. Owned-properties paragraph vs round-23 snapshots — VERIFIED per byte:
    - plazir15-ghp and charter-ghp page.html carry all four (og:image vessel.webp / hero-domes.jpg).
    - ds4cc-primary: og:title/type/url + canonical https://ds4cc.com/, no og:image.
    - ds4cc-kimi: og:url "./" relative, no canonical link.
    - burnerchrome-kimi, vault-index-kimi, lucario-ghp, ufo-fsd-kimi-pro: grep -c 'og:' = 0.
    - fetch.json fetchedAt 2026-10-21T06:33:03–20Z → "one-day-old captured bytes" accurate.
12. Preamble "The C2 counter does not read them" — VERIFIED: c2_source_census.py quotes come from
    the lesson "## Gate" section (section_lines/glines), not the entry; IDS covers S067–S070 only,
    so S073 and appended prose are outside its checks.

## Not verified / residual

- "Hand-authored" (claim 4) rests on absence-of-generator evidence from the w1 scout; I confirmed
  the workflow and the bulk-edit commit but did not re-grep every non-html path myself.
- No live checks (owned hosts out of bounds); all snapshot claims are stale-by-construction and the
  section says so.
