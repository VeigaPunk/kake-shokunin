# NoGoogleSelection — critic attack on claim C1

Seat: critic (leaf, read-only). Axis judged: **operability**. Milestone: offline-canonical-capability.
Scope: the *selection-vs-policy* boundary of C1 — the one limit the contract states in words
("policy comparison, not search-engine selection") that no parser/traversal/exit-code reviewer
covers. Only file written: this report. No installs; no lane edits outside this file.

## Claim under attack

C1 "Offline static canonical publishing preflight" (`contract.json`): a read-only local validator
`scripts/canonical_audit.py` classifies all 32 frozen matrix cases with expected exit + finding id,
"rejects missing/conflicting/mismatching canonical signals, and proves clean positive controls",
counted by `python3 .ufo/waves/round-22/measure.py --root . --revision <master-tip>`.

Verified before-state: at base `7c61c8c`, `scripts/` holds only `corpus-contract.mjs`,
`freshness-sweep.mjs`, `probe-delta.mjs`; no `canonical_audit.py`, no `round-22/measure.py`.
"0 accepted cases" is literally true.

## The attack surface, sourced

The dangerous failure mode is not a wrong exit code — it is a validator that *silently becomes a
Google-selection emulator* while claiming policy comparison. Landed scout evidence makes the
boundary concrete:

- `w1/GoogleTroubleshoot.md`: "Even if you explicitly designate a canonical page, Google might
  choose a different canonical for various reasons"; companion page: "indicating a canonical
  preference is a hint, not a rule". The Google-selected canonical is observable only via live URL
  Inspection — unreproducible offline. Any output phrased as selection is unprovable by construction.
- `w1/GoogleCanonical.md`: canonicalization signals "can stack" across `link` element, HTTP `Link`
  header, sitemap, redirects, hreflang. A static HTML file exposes **one** of those channels. The
  page states no duplicate-link precedence and no rel-token rules.
- `w1/RFC6596.md`: cross-host/cross-scheme targets are *permitted* by the RFC — `wrong_host` fails
  only against the manifest oracle, never against RFC conformance. The single RFC MUST
  (duplicative/superset content) is statically unverifiable.
- `w1/HTMLLink.md`: `rel` tokens are ASCII case-insensitive by the HTML Standard; "exactly one
  canonical" and head-only-for-canonical are local policy / derived, not stated spec rules;
  `href=""` URL-parses to the document URL — a browser-engine fact that must NOT make `href_empty`
  clean.

## Falsifiable acceptance constraints

Reject C1 if any of these fails on the measured revision:

1. **NS-AC1 — zero selection vocabulary.** `grep -inE 'google|search.?engine|index(able|ing)|serp|select(s|ed|ion)?.canonical|crawl|rank' scripts/canonical_audit.py .ufo/waves/round-22/measure.py` yields no hits outside an explicit limitation comment/docstring. Verdict strings, finding ids, and the report must never phrase exit 0 as "Google/engine will select this URL".
2. **NS-AC2 — signal scope is single-channel.** Every finding derives only from explicit-head
   `<link>` elements, the first head `<base href>`, and manifest `url`/`expectedCanonical`. No code
   path, fixture, or claim text may merge HTTP-`Link`-header, sitemap, redirect, or hreflang signals —
   including the statically representable decoy `<meta http-equiv="Link" content="…rel=canonical…">`,
   which is NOT a `link` element and must be ignored, not counted as a conflicting canonical.
3. **NS-AC3 — no engine heuristics in comparison.** The URL comparator must not apply Google-style
   clustering: http↔https equivalence, www/non-www merge, trailing-slash merge, "prefer shorter
   URL", or cross-page cluster analysis. `expectedCanonical` mismatch on scheme alone must remain
   `canonical_mismatch`.
4. **NS-AC4 — policy finding text, not conformance text.** `canonical_multiple`/`canonical_outside_head`/
   `canonical_mismatch` messages must cite contract policy ("exactly one in explicit head",
   "differs from expectedCanonical"), not "Google requires", "RFC violation", or "invalid canonical".
   RFC 6596 permits cross-host and "ought to" uniqueness; overstating authority is false provenance.
5. **NS-AC5 — no-fetch proof.** Static audit: no `urllib`/`http`/`socket`/`ssl`/`requests`/
   `subprocess` import or call in either script; manifest `url` is a string oracle. Any derived
   document URL (fetch, base-as-URL fallback beyond contract wording) → exit-2-or-reject.
6. **NS-AC6 — "conflicting" is in-head only.** The claim's "conflicting canonical signals" reads as
   duplicate/conflicting head declarations (`duplicate_different` → `canonical_multiple`). Any
   broader interpretation (cross-page, cross-file, meta-equiv, comment text) is out-of-contract
   selection logic — reject.
7. **NS-AC7 — bounded normalization claim.** Output/docs must say "WHATWG-like" with the explicit
   subset (scheme/host lowercase, default-port drop, dot-segment removal, query preserved, fragment
   and credentials rejected). Claiming WHATWG URL conformance from `urllib.parse`/`HTMLParser`
   stdlib is an overclaim of the comparison primitive.
8. **NS-AC8 — expectations are frozen, not generated.** The 32-case expected exit+finding table must
   exist as committed, independently-authored data at `--revision`. If `measure.py` derives
   "expected" from validator stdout, the count is circular — reject.

## Overclaims to reject outright

- **O1**: any "after" wording implying the validator verifies *the* canonical a search engine will
  use, indexability, dedup outcome, or publishing readiness. Clean verdict = declaration conforms to
  local policy, full stop.
- **O2**: "checks canonical signals" unqualified — statically visible surface is one channel of
  several; the claim must stay "explicit-head link canonical only".
- **O3**: `duplicate_same`/`duplicate_different` justified as "what Google does" — Google docs are
  silent on duplicate precedence; basis is contract "exactly one" + RFC "ought to". Wrong provenance
  = reject, even with the right exit code.
- **O4**: `relative_*` cases failed or warned "because Google recommends absolute" — the source calls
  absolute a recommendation and relative "supported"; resolving then comparing is the contract rule.
- **O5**: `href_empty` accepted because empty-href URL-parses to the document URL (browser behavior,
  noted in `w1/HTMLLink.md`) — contract expects `canonical_href_missing`; engine parse-behavior is
  not policy.
- **O6**: clean positive controls "proven" by working-tree run or validator-derived expectations —
  r21 verifier standard is re-measurement over committed blobs at the named revision (`corpus/
  lessons/round-21-verifier-spotcheck.md`: independent counter over `git ls-tree`/`git show`).

## Distinct wave2 attack (owned by this seat; disjoint from HeadBoundary/ParserScope/URLNormalization/PathTraversal/SymlinkSafety reviewers)

Falsification probes aimed only at selection-drift, additive to — never edits of — the frozen 32:

1. **Scheme-merge trap.** Fixture: declared `http://example.test/a.html`, `expectedCanonical`
   `https://example.test/a.html`. Expected: `canonical_mismatch`, exit 1. A validator merging schemes
   (Google's known HTTPS preference) yields false clean → overclaim caught.
2. **Meta-equiv injection.** Fixture head contains `<meta http-equiv="Link" content='<https://evil.test/x>; rel="canonical"'>` plus one good `link`. Expected: still clean/`canonical_missing`-free
   with exactly the one link counted. `canonical_multiple` here proves signal-merging beyond `link`
   elements → reject.
3. **Cluster-analysis probe.** Manifest: page A canonical→B, page B self-canonical. Per-page verdicts
   must each compare declaration to its own `expectedCanonical`; a verdict on A that reasons about
   B's canonical (loop/chain detection) is selection logic → reject. (RFC 6596 chained-canonical
   "heuristics" are engine latitude, not this contract.)
4. **Provenance grep + static audit** per NS-AC1/NS-AC5/NS-AC8, run on the committed revision only.
5. **Decoy-finding precision.** Comment/sitemap-shaped text (`<!-- canonical: X -->`,
   `<link>` inside `<script>`/`<template>`) must produce the frozen ids (`canonical_missing` etc.),
   never a generic "conflicting signal" finding — the finding-id set is closed.

## Smallest safe correction for L1

Require `canonical_audit.py` to emit its scope limit verbatim in JSON output or docstring
("explicit-head link element policy check only; no engine selection, no other canonicalization
signals"), keep finding text contract-cited, and have `measure.py` read a committed expectation
table — not validator output — for the 32/32 count.

## Checks for main agent (L1)

- NS-AC1 grep over landed `canonical_audit.py` + `measure.py`; NS-AC5 import audit.
- Wave2 fixtures 1–3 above executed against the measured revision.
- Confirm expectation table is committed data, keyed to all 32 frozen case names verbatim.
- Confirm no finding/claim text cites the Google scout quotes as authority for mechanics
  (`w1/GoogleCanonical.md` explicitly disclaims duplicate-precedence and token rules).

Author-side finding; no admission implied. Operability is the only axis attacked; freshness and
non-owned axes untouched by design.
