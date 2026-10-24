# ReopenS061Resolution — routed defect 4: S061 row and the S053/S054 resolution

Seat: KakeR31a2.ReopenS061Resolution (reviewer leaf, freshness axis). Lane tip reviewed: `fde133a` content (tip `92235a0` adds only SCORECARD/receipts). No installs; only file written in lane: this report. Sandbox: `/fast/scratch/hyaku/kake-r31/a2-w2/ReopenS061Resolution/` (`S061-reopen.txt`, `S061-reopen.html.gz`, `S061-reopen-receipt.json`).

## Re-open (same method)

One public GET of https://render.com/docs/configure-other-dns via the `fetch_sources.py` method (urllib, UA `kake-shokunin-round-31-source-opening (one GET per page)`, same visible-text rule). Result `S061-reopen-receipt.json`: HTTP 200, `finalUrl` unchanged, bodyBytes 292139 (same as receipt), `bodySha256 aa60bb3d…09a2` differs (per-request trace/build drift), **`textSha256 aa904927cf…0c3d` byte-identical to `receipts.json`** and `cmp` of my text vs `sources/S061.txt` equal (`retained==reopen text: True`), 899 words. Third open (L1 15:41:29Z, w1 15:55:4xZ, mine 18:06:32Z).

## S061 row and Gate quote

- Gate quote (lesson line 46) is an exact substring of the retained text: 21 words, `substring: True`. All three S061 quotes in `render-static-sites.md:158-160` are exact substrings (25/21/10 words).
- Teaches/scope verified against text: ANAME/ALIAS section, A-record fallback `216.24.57.1`, AAAA warning, per-provider guide links (Cloudflare, Namecheap) match the "other providers" scope.
- Cosmetic only: anchor cell groups the AAAA warning under "Configuring root domains"; in the text the warning precedes that heading. No falsity.
- Cosmetic only: `render-static-sites.md` frontmatter `source:` names S049–S052/"the four retained pages" while the corrections section quotes S061; per contract rule 2 headers are not rewritten, `used-by` gives back-trace.

## Verdicts on S053 / S054 (rows at SOURCES.md:61-62; note at :144; lesson "Registry changes" lines 60-61)

- **S053 — `rejected` → `rejected`: HOLD.** The row's flip is self-neutralizing ("…and they match the tutorial, *which then still adds nothing beyond S050 and S052*"). Premise verified offline: retained screened body `round-30/sources/screened/C1.txt` shows "Grab your CNAME and ALIAS"; S061 names ANAME/ALIAS, so the match leg of the flip is met and the self-neutralizing tail decides. Consistent with the contract.
- **S054 — `rejected` → `rejected`: HOLD with a wording caveat (low).** Flip predicates are met: retained screened `C2.txt` states apex "Type: A … Value: 216.24.57.1" and FAQ "216.24.57.1, Render's load balancer IP"; S061 states the same address. Unlike S053 the flip clause carries no self-neutralizing tail, so its literal wording promised a verdict change that did not occur. The `rejected` outcome is still the only contract-legal one: `mined` is impossible while `used-by` is `—` (nothing cites it), `queued` would retain a lead superseded by primary S061, and registry convention keeps accurate-but-superseded community rows rejected (S046 "already carried"; S017). An independent surviving rejection ground stands: the post names only Let's Encrypt where S049's retained text names "Let's Encrypt and Google Trust Services". Rule 2 allows an unchanged status when logged old→new; the lesson and the :144 note log it, exactly what routed defect 4 (closure :277-279) asked.
- Stale teaches clauses (S053 "was not opened this round", S054 "no opened Render primary states") are immutable point-in-time text corrected by the tail note — the established S030 precision-note pattern; no defect.

## Contract check (CORPUS.md §SOURCES)

Rule 1: S061 quote 21 words ≤25, URL + access date + Grounding present in the Gate — pass. Rule 2: only logged status/recheck/used-by changes; the :144 note preserves immutables — pass. Rule 5: the resolution note sits at file tail after "## Leads", same placement as the S030 note (:142) — convention-consistent. Rule `community is never A`: both rows tier C — pass.

## Commands run

- `python3` fetch+extract (above) — exit 0.
- `python3` substring/word-count checks — exit 0 (all True).
- `grep -o` on `screened/C1.txt`, `screened/C2.txt`, `round-30/sources/S049.txt` — exit 0 (hits quoted above).
- `git log -S` provenance — S053/S054 rows authored in round-30 `451e98f` (same-round cell fix by `CriticRejects`, so rule 2 not implicated); resolution note in `fde133a`.
- `grep S061 SKILL.md` — no hits, consistent with S061 `used-by` naming only `render-static-sites.md` (that file exists and cites it). Census mined-row used-by check passes for S061.

## Residual risk / gaps

- I did not refetch dev.to or namesilo.com (assignment scoped the re-open to the Render page); their flip premises were verified on retained round-30 texts only.
- `render-static-sites.md` `falsifier:` says "the four Render Docs pages" though S061 is now a fifth source for that entry — cosmetic staleness, flagged for a future correction section.
