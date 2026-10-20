# FalsifyPolicy — wave-2 critic attack on C1 (policy-vs-platform conformance; selection/freshness overclaim)

Seat: critic (leaf, read-only). Axis attacked: **operability** — specifically whether
C1's evidence supports "policy comparison" without silently becoming a platform
emulator or claiming selection/freshness. Integrated revision under test:
`c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (lane HEAD, verified `git rev-parse HEAD`).
All probes run in `/tmp/r22-policy-probes/` against the committed
`scripts/canonical_audit.py` (sha256 `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7`,
matching `frozen/expected.json` and all integrated receipts). No installs, no lane
edits, no builds/formatters. Production bytes untouched.

## Checks executed

Static:
- `grep -inE 'google|search.?engine|index(able|ing)|serp|select(s|ed|ion)?.canonical|crawl|rank'`
  over `scripts/canonical_audit.py`, `measure.py`, `matrix.py`, `replay.py`: two hits
  only, both explicit scope disclaimers (`canonical_audit.py:4` docstring, `:92`
  `usage()` "compares publisher policy only, not Google or other search-engine
  canonical selection"). **NS-AC1 pass.**
- Import/syscall audit of the four shipped programs: `urllib.parse` (pure parsing,
  no `urlopen`), no `socket`/`ssl`/`requests`/`http.client`. `subprocess` appears
  only for selftest re-invocation (`canonical_audit.py:742`), `git` read-only
  plumbing in `measure.py:90`, and matrix child runs. No fetch surface. **NS-AC5 pass.**
- Expectations are committed data: `cases.json` carries `expectedExit`/`expectedFindings`
  per case; `matrix.py:278-281` compares against it, `measure.py` materializes
  everything from `git ls-tree`/`git show` blobs and pins SHA-256 per blob
  (`measure.py:391-462`). Validator output never feeds the expectation side.
  **NS-AC8 pass.** `measure-before.json` records `accepted 0, available:false`
  ("capability absent"), pins labeled `source:"working-tree"` for the supplied
  instrument — honest provenance, not circularity.
- Output vocabulary: verdicts are `clean` / `failed-policy` / `could-not-evaluate`;
  finding ids are exactly the closed contract set; no verdict or finding text cites
  Google/RFC authority for the mechanics. **NS-AC4 pass.**
- Integrated wording audit (`git show c0fd6d5`): SKILL.md gate row calls it
  "`0=clean` named static publisher policy" and "Canonical declarations are
  signals, not guarantees of Google's selection"; LOG.md "Freshness stays
  unchanged … No numeric score increase"; PROVINCE.md "not a claim that a live
  website was repaired or a Google-selected canonical observed";
  `corpus/README.md` keeps JS-rendered canonicals/live delivery open; QUALITY.md
  "never proves Google's selected canonical"; no SCORECARD row added — the
  capability stayed out of the capability table, so there is no phantom-row or
  freshness-credit defect. `knowledge/static-canonical-preflight.md` states the
  tool "enforces a stricter local policy … not a claim that the URL violates
  RFC 6596." **No selection or freshness overclaim found in any integrated text.**

Runtime probes (exact outputs, all against committed script):

| Probe | Fixture | Expected under honest policy-check | Observed |
|---|---|---|---|
| scheme-merge trap | canonical `http://example.test/a.html`, expected `https://…` | `canonical_mismatch` exit 1 — Google's HTTPS preference must NOT merge | `{"id":"canonical_mismatch","page":"http://example.test/a.html"}` exit 1 ✓ |
| meta-equiv injection | `<meta http-equiv="Link" content='<https://evil.test/x>; rel="canonical"'>` + one good link | ignored; still clean | `{"findings":[],"verdict":"clean"}` exit 0 ✓ |
| cluster analysis | page A canonical→B, B self-canonical | per-page: A `canonical_mismatch`, B clean; no chain reasoning | finding on A only, `pagesChecked:2`, exit 1 ✓ |
| www merge | canonical `www.example.test`, expected apex | `canonical_mismatch` | `canonical_mismatch` exit 1 ✓ |
| trailing-slash merge | canonical `…/a.html/`, expected `…/a.html` | `canonical_mismatch` | `canonical_mismatch` exit 1 ✓ |
| body+head dup | one head canonical (match) + one body canonical (other host) | not clean | `canonical_outside_head` exit 1 ✓ |

**NS-AC2/NS-AC3/NS-AC6 pass: no engine heuristics, single-channel signal scope,
no cross-page clustering.** Decoy finding precision (`comment_decoy`,
`script_decoy`, `template_decoy` → `canonical_missing`) confirmed by
`matrix-integrated.json` (32/32 PASS, committed receipt) and selftest receipts.

## Divergences found — bounded, none judge-must-reject

**D1 — `noscript` fails closed instead of counting the serialized signal.**
w1 `PublisherVsBrowser.md` argued the contract's ignore list omits `noscript`, so
the default-parser tree should count a `noscript`-descended canonical
(expectation: `canonical_multiple`, exit 1). Observed: both probes
(head canonical + noscript canonical, and noscript-sole canonical) return
`html_unsupported`, exit 2 — `canonical_audit.py:177-182` marks canonical/base
inside noscript unsupported. This *contradicts* the w1 seat's publisher-tree
reading, but it does not violate the frozen contract (ignore list is permissive,
not exhaustive; `html_unsupported` is a licensed could-not-evaluate), it is
explicitly disclosed in `usage()` line 90 ("canonical/base inside noscript, is
unsupported"), and it errs on the non-clean side — it cannot produce a false
clean or a selection claim. **Bounded acceptance; not a defect under C1.** The
disclosure covers it.

**D2 — attribute-scoped canonicals counted where Google ignores them.**
The lane's own knowledge entry (`static-canonical-preflight.md`, sourced S021)
states Google ignores canonical annotations carrying `hreflang`/`lang`/`media`/
`type`. Observed: `<link rel="canonical" hreflang="en" href=…>` and
`media="print"` variants both return `verdict:"clean"` exit 0 when the href
matches. Under the frozen contract this is *correct local policy* — "exactly one
canonical link in explicit head" is met, and the verdict is contract-cited, not
platform conformance. The residual risk is a reader inferring platform-visible
signal; mitigated by the lesson's explicit line "explicit local publisher policy,
not a second platform conformance standard" and SKILL.md's "not complete
publication readiness." **Bounded acceptance** — a declared simplification of the
contract policy, honestly bounded, not a hidden overclaim.

## Verdict shape

**Bounded acceptance of C1 on this axis.** No counterexample found that
produces (a) a clean verdict the frozen policy forbids, (b) any selection or
freshness vocabulary outside disclaimers, (c) cross-channel signal merging, or
(d) engine-style equivalence merging — all scheme/host/www/slash distinctions
stay strict and the oracle stays `expectedCanonical`. Every observed divergence
from platform behavior is either stricter (fail-closed: noscript, foreign
content, template self-close) or a documented policy simplification (D2). The
"policy-vs-platform" split survives: the tool never claims WHATWG URL
conformance (`usage()` says "conservative RFC-style subset"), never claims
Google selection, never touches freshness.

## Smallest safe correction (optional, non-blocking)

None required for C1. If L1 wants zero residual ambiguity, one sentence in
`usage()` or the knowledge entry noting that attribute-scoped canonical
annotations (`hreflang`/`media`/`type`) are counted under local policy though
Google documents ignoring them would close D2's reader-inference gap entirely.
D1 needs nothing — already disclosed.

## Install log

None. No package transactions, no tool installs; probes used system Python 3.14.8.
