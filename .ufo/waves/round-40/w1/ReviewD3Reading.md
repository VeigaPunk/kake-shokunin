# ReviewD3Reading — is "Not changed: D3" a contract reading or a dodged repair?

Round 40 wave 1, leaf KakeR40.ReviewD3Reading. Tip f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8.
Axes: operability, freshness. Verdict up front: **leaving D3 unchanged is a contract reading, not
a dodged repair.** One scope overstatement found in the resid text (finding F1, LOW).

## Statements attacked and verdicts

**S1 "doctype plus malformed gives `doctype_present`" (resid/ReviewBuildContract.md D3) — holds in
substance, overstated in scope.** The D3 combo resolves to `doctype_present` whenever a parse
*reaches* the document-type-decl event before the error, not for any malformed doc that merely
contains `<!DOCTYPE`. Counterexample to the unqualified phrasing:
`junk<!DOCTYPE urlset><urlset …>` → `xml_malformed`; `<urlset …><!DOCTYPE urlset` (unclosed) →
`xml_malformed`. Both verdicts are failed-policy exit 1 either way, so only the code differs — LOW.

**S2 round-40 lesson "Not changed: D3 … sentence 9 is the lane's safety reading and the round-39
build declared this precedence; the contract does not order (b)'s two sentences, and changing it
would be a contract change, not a repair" (corpus/lessons/round-40.md:30-32) — holds, every clause
verified.** (i) s9 is explicitly marked "Lane reading (safety, not from a source)"
(.ufo/waves/round-39/c1-contract.md:39) so no source can order it against s8; (ii) s8 and s9 are
both unconditional — "otherwise `xml_malformed` … and no other finding" (:38-39) vs "a document
type declaration gives `doctype_present` … and no other finding" (:39-40) — for a malformed doc
with a DTD both fire and neither yields; the contract's own header routes undetermined behaviour
"outside the contract"; (iii) the build seat declared the precedence key-blind, before any counter
existed (w2a3/BuildSitemapAudit.md:57 "doctype pre-scan before parsing", :59 Risks "DOCTYPE-vs-
malformed precedence is a lane reading (both sentences say 'no other finding')"); (iv) a repair
must move behaviour toward the contract; since the contract underdetermines the combo, flipping to
`xml_malformed`-wins would be a second arbitrary pick, not a repair.

**S3 "not a dodge" — holds.** A dodge skips declared work; round-40 C1 declares exactly E/U/R
(SCORECARD.md:2554-2561) and the frozen counter contains zero doctype witnesses:
`grep -c doctype .ufo/waves/round-40/c1_count.py` → 0. `git log f171c58b..f043c72 --
scripts/sitemap_audit.py` → 0 commits: the script is literally untouched this round. The reference
repair (`03a8fba4…`, shared/ref_fix.py) behaves identically to base on all 10 D3 probes below and
its diff's three hunks (@@ -67, @@ -184, @@ -330) never touch `_has_doctype` (:155-169) or the
gate (:190-191).

## Evidence — commands (exit 0 unless noted)

`prlimit --as=4000000000 timeout 120 python3 -B probe_d3.py <tool>` run twice (base tool, then
ref_fix); driver + fixtures at /fast/scratch/hyaku/kake-r40w1/ReviewD3Reading/probe_d3.py.
Base = lane scripts/sitemap_audit.py, sha256 6d86c8ce…a240ec (unchanged since the round-39 build).
All rows: verdict failed-policy, exit 1, unless marked.

| probe | bytes (sketch) | base | ref_fix |
|---|---|---|---|
| d1 | `<!DOCTYPE urlset><urlset …><url><loc>x` (truncated) | doctype_present | doctype_present |
| d2 | `<!DOCTYPE urlset>` alone | doctype_present | doctype_present |
| d3 | `<!DOCTYPE urlset [<!ENTITY e "x">]><urlset …>&e;<url>` | doctype_present | doctype_present |
| d4 | `junk<!DOCTYPE urlset><urlset …>` (error before DTD event) | xml_malformed | xml_malformed |
| d5 | `<urlset …><!DOCTYPE urlset` (unclosed, matches resid s9 note) | xml_malformed | xml_malformed |
| d6 | `<!DOCTYPE feed><feed xmlns=…>` (root_invalid suppressed) | doctype_present | doctype_present |
| d7 | well-formed + DTD (s9 baseline) | doctype_present | doctype_present |
| d8 | `<!--<!DOCTYPE x>-->` comment only, host-matching loc | clean, exit 0 | clean, exit 0 |
| d9 | `…<!ENTITY e "aaaa">…<loc>http://h/&e;</loc>` (entity gated) | doctype_present | doctype_present |
| d10 | latin-1 declaration + DTD (sourced s7 gate first) | encoding_invalid | encoding_invalid |

The gate chain is coherent: sourced gates s6/s7/s19 first, then lane reading s9, then s8's parse
(sitemap_audit.py:172-195). d4/d5 refine the reading to event-based — the parser must reach the
DTD for s9 to fire; under the safety rationale that is exactly right (an error before the DTD
means the DTD is never processed), and d5's behaviour was already recorded in the resid s9 line.

No tools installed (none needed). No lane file other than this report touched; scratch ≤ 3 MB.

## Residual risk and gaps

- F1 (LOW): resid D3's "a document that is ALSO malformed" lacks the reaches-the-DTD-event
  qualifier; d4/d5 show docs with a DTD in the bytes that give `xml_malformed`. Not fixed here —
  round-39 resid is outside my write scope; recommend the L1 carry one sentence into round-40
  closure. Text-only: no behaviour change implied.
- The selftest pins `doctype_present` only on well-formed doctype docs
  (scripts/sitemap_audit_selftest.py:302-321), so the round-40 regression half does NOT pin the
  combo itself — the "not changed" call rests on the contract ambiguity + prior declaration, not
  on counter force. Verified; stated so nobody over-claims the predicate pins D3.
- Not probed: DTD detection under expat with `text` given as str vs the gate's byte-decoded text
  (same path for both probes; no divergence observed).
