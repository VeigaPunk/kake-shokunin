# ScoutCache — kake round 86 w1 (S457/S456 re-open, quotes, lane boundary)

Seat: ScoutCache (leaf scout; no subagent dispatch). Date: 2026-11-04. Lane:
`/home/vgpnk/Projects/shokunin/kake-shokunin` at base `376ac5dcdf86457ef1f8dd490dada735dad81f68`;
frozen contract read first (`.ufo/waves/round-86/contract.md`, efc2ad654f1ee56a86ecb57b3b709c18cd1323b5)
plus `.ufo/waves/round-86/count.py` (437 lines; CASES at 154–199). All paths
below relative to the lane root. No production writes; no VCS mutations; no
installs (none needed — pacman unused; only curl/python3/grep/coreutils used).

## 1. Re-opened sources — receipts

Both held RFC 9111 rows re-opened by GET this round (GET-only; no POST probe
was authorized for this seat, and none was sent):

- **S457** https://httpwg.org/specs/rfc9111.html — HTTP 200, 178,573 bytes,
  sha256 `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64`,
  fetched 2026-11-04T15:37:19Z; `last-modified: Mon, 19 Oct 2026 01:13:54 GMT`,
  `etag: "6ad56ed2-2b98d"`. Body: `s457.body.html`; headers/meta:
  `s457.headers`, `s457.fetch.meta` (under `.ufo/waves/round-86/w1/ScoutCache/`).
- **S456** https://www.rfc-editor.org/rfc/rfc9111.txt — HTTP 200, 84,477 bytes,
  sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`,
  fetched 2026-11-04T15:37:20Z; `etag: W/"f8907618635703edd228aee4aa834eee"`.
  Body: `s456.body.txt`; `s456.headers`, `s456.fetch.meta`.

Both hashes match the abbreviated expectations displayed in
`corpus/knowledge/policy-value-classes.md` (`999f4013…`, `aeb52adb…`).
This is prefix agreement; no full historical-body comparison was run.
Full fresh-GET receipt + quote table:
`ScoutCache/s457-reopen-receipt-draft.md` (same directory).

## 2. Quoted spans (≤25 words, section anchors; verified substrings of retained bodies)

| Fact | Quote (S456 `rfc9111.txt` lines; S457 anchor) | Check |
|---|---|---|
| §4.2.1 first-match freshness | "evaluating the following rules and using the first match" — L654–656, `rfc.section.4.2.1` | PASS, 9 w |
| §4.2.1 duplicate first-occurrence-or-stale | "either the first occurrence should be used or the response should be considered stale" — L677–681, `rfc.section.4.2.1` | PASS, 14 w |
| §5.2 case-insensitive tokens + quoted-string acceptance | "identified by a token, to be compared case-insensitively, and have an optional argument that can use both token and quoted-string syntax" — L1099–1104, `rfc.section.5.2` | PASS, 21 w |
| §5.2.2.1 token-form generation | "This directive uses the token form of the argument syntax: e.g., 'max-age=5' not 'max-age=\"5\"'.  A sender MUST NOT generate the quoted-string form." — L1218–1220, `rfc.section.5.2.2.1` | PASS, 22 w |
| §5.2.2.5 no-store | "MUST NOT store any part of either the immediate request or the response and MUST NOT use the response to satisfy any other request" — L1297–1299, `rfc.section.5.2.2.5` | PASS, 24 w |
| §5.2.2.10 s-maxage override | "the maximum age specified by this directive overrides the maximum age specified by either the max-age directive or the Expires header field" — L1390–1393, `rfc.section.5.2.2.10` | PASS, 22 w |
| §1.2.2 delta-seconds cap | "the cache MUST consider the value to be 2147483648 (2^31) or the greatest positive integer it can conveniently represent" — L222–225, `rfc.section.1.2.2` | PASS, 19 w |

All six S457 anchors present exactly once in the retained HTML; "first match"
and "overrides the maximum age" confirmed in the HTML text too. Verification
transcript: `ScoutCache/verify-quotes.txt` (7/7 substring PASS, 7/7 ≤25 words).
Quoted spans map 1:1 onto the frozen counter semantics (count.py CASES:
`duplicate-first-occurrence` lifetime 100 vs `first-occurrence-not-minimum` lifetime 200 = the
order witness; `shared-s-maxage-overrides` vs `private-ignores-s-maxage`;
`no-store-not-storable`; `delta-seconds-cap`; `directive-case-insensitive`;
`no-cache-qualified`; `expires-minus-date`).

## 3. Bounded planning data-walk — boundary paragraph

The new tool (`scripts/cache_control_effective.py`, to be authored by an
executor seat) and its knowledge entry must stay byte- and authority-disjoint
from three existing lane files. First, `scripts/header_audit.py` (48,986 B) is
the round-61 offline expectation audit: it reads a frozen manifest v1 and
declares exactly six expectation classes (content_type_present, hsts_present,
xcto_nosniff_value, csp_present, singleton_fields, field_name_syntax); it
contains zero occurrences of "cache-control" (grep -c -i → 0), so the new
reader must not modify it, import it, or claim any of its six classes — a
cache-control finding has no home in that manifest's grammar. Second,
`corpus/knowledge/response-header-expectations.md` (17,296 B) is the S430–S433
ground for precisely those six classes, with a scope line that self-limits to
them; the new reader must not extend that entry or read its rules as freshness
authority. Third, `corpus/knowledge/policy-value-classes.md` (14,905 B) is the
S457-grounded r84 entry behind `scripts/policy_value_class.py` (policy-class
value moves under a frozen `name[=parameter]` grammar); the new
`corpus/knowledge/cache-control-effective.md` (absent at base, confirmed) is a
sibling S457 consumer, not a rewrite: per the frozen contract it "does not
upgrade or rewrite the r84 experimental general classifier," so the boundary is
— value-level freshness reading of Cache-Control/Expires/Date only (storable,
first-match lifetime, first-occurrence duplicates, s-maxage shared override,
no-store, delta-seconds cap), with Vary, Age, Pragma, must-understand store
permission and heuristic factors disclosed out of scope, and neither S457
entry absorbing the other's grammar, verdict order, or class table.

## 4. Receipts, exits, limits

Successful fetch/digest/quote commands exited 0: `curl -sS -L` GET ×2 (bodies + headers saved, fetch
meta written); `sha256sum` ×2; `date -u` ×2; `grep` anchor/span checks;
`python3` substring/word-count verification (7/7 PASS); `test -e
corpus/knowledge/cache-control-effective.md` → absent; SOURCES.md S457 row
cell-read → used-by cell is exactly `corpus/knowledge/policy-value-classes.md`
(SOURCES.md:204, column 10), which the receipt draft's old→new updates with
`; corpus/knowledge/cache-control-effective.md`. Limits: quotes are
normalized-whitespace substrings (RFC line-wrapping dehyphenated) of the
retained `.txt`; S457 ids are the anchors; no live property request, no
browser, no credentials, no deploy. Scratch
`/fast/scratch/hyaku/kake-r86/ScoutCache/` used transiently and deleted before
yield; all receipts copied out first.

## Evidence qualification

Axes: source freshness, quote precision, boundary preservation. Observed source
facts have high confidence from retained bodies; the boundary paragraph is a
planning recommendation, not semantic call-graph proof. No LSP device/server
is available in this seat's tool inventory; literal reads/searches are the
fallback, not semantic proof of absence. No definitions/callers were changed.

Important modals: §5.2 additionally says “recipients ought to accept both forms,
even if a specific form is required for generation” (S456 lines 1101–1102,
§5.2 anchor above). §1.2.2 mandates the quoted overflow treatment on overflow
or unrepresentable input; it does not universally require clamping every
representable number above 2147483648. The frozen contract's fixed cap is a
bounded implementation choice permitted by, not verbatim required by, that
text. Likewise first-occurrence is one allowed duplicate disposition; stale
is the alternative. These distinctions must survive the new knowledge entry.

Execution defects/limits: the first mkdir and both initial fetch attempts
failed before execution because their specified cwd did not yet exist; all
three were retried successfully after creating scratch from the fleet cwd.
The existence predicate returned 1 (absent), wrapped with an echo returning 0;
the no-cache-control grep count also returned 1 with count 0. No frozen
counter, tool selftest, build, or integration verification was run. The
truncated pre-existing recheck line supplies abbreviated expected digests,
so this report observes prefix agreement, not an independently verified
full-digest comparison to round-84 retained bodies. Production integration,
guard proof, mirror census gate, and closure remain L1/assigned-seat work.
