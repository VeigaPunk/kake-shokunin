source: S457 — RFC 9111: HTTP Caching, httpwg HTML rendering — https://httpwg.org/specs/rfc9111.html — anchors located this round in `.ufo/waves/round-84/w1/ScoutSources/rfc9111-httpwg.html` (178,573 B, sha256 999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64, HTTP 200, fetched 2026-11-04 by the round-84 ScoutSources seat): §4.2 heading at HTML line 269 (col 12,463), §5.2 heading at line 279 (col 1,006), §5.2.2 heading at line 282 (col 6,574), §5.2.2.1 `max-age` heading at line 282 (col 6,944) and its defining sentence at line 282 (col 7,400). S456 — the same RFC's rfc-editor `.txt` rendering, opened in round 83 — https://www.rfc-editor.org/rfc/rfc9111.txt — supplies every quoted span, from `.ufo/waves/round-84/w1/ScoutSources/rfc9111.txt` (84,477 B, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e) at lines 587, 597, 621, 661, 677, 684, 1099, 1104, 1106, 1205, 1214, 1215, 1218 and 1775. S456 and S457 are two renderings of one document: the HTML rendering is the one opened this round, the `.txt` rendering carries the line anchors this entry quotes.
verified-at: 2026-11-04, base revision fe42ad11eb1084ad2ea68d12c5bbb2922a089868, freeze f358022f7e1b2f3846be8ceacbe3a7ef22edf4be — 14 quoted spans re-opened this round in the retained `.txt` and each checked as a raw substring of the single physical line named (14/14, `.ufo/waves/round-84/w1/ScribeKnowledge/quote-substrings.tsv`); the S457 anchors re-located by byte offset in the retained HTML — four headings plus the `max-age` sentence — and recorded in `.ufo/waves/round-84/w1/ScribeKnowledge/html-anchors.tsv`; `scripts/policy_value_class.py` read in full and run by this seat — real pair exit 0 verdict `policy-unchanged`, `control` pair exit 0 with 3 changed and verdict `policy-changed`, `equivalent` pair exit 0 with 1 changed and verdict `policy-rewritten-equivalent`, `--selftest` printed `selftest: 15/15 passed` exit 0 (stdout and exit codes under `.ufo/waves/round-84/w1/ScribeKnowledge/`). The round-84 `.txt` copy is byte-identical to the round-83 retained copy (same sha256), so S456's line anchors did not move.
recheck: 365d (an RFC changes only by a new publication). Re-open: `T=$(mktemp -d) && curl -sSL --max-time 90 -o "$T/rfc9111.txt" https://www.rfc-editor.org/rfc/rfc9111.txt && sha256sum "$T/rfc9111.txt"` (expect aeb52adb…) and `curl -sSL --max-time 90 -o "$T/rfc9111.html" https://httpwg.org/specs/rfc9111.html && sha256sum "$T/rfc9111.html"` (expect 999f4013…); then `python3 -B scripts/policy_value_class.py --a .ufo/waves/round-81/capture --b .ufo/waves/round-82/capture --declared .ufo/waves/round-81/capture-expectations.json` and compare with `.ufo/waves/round-84/controls/tool-real-pair.txt`; decide the claim with `python3 -B .ufo/waves/round-84/c84_policy_values.py --root . --revision <rev>`.
ground: freshness — C2's policy-value gate, `.ufo/waves/round-84/contract.md` §C2
scope: Whether a changed `policy`-class response header's value actually moved — a numeric parameter, a directive added, removed or changed, the field appearing or vanishing, an order-only rewrite, or a value that does not parse — decided from two retained captures by `scripts/policy_value_class.py` under a frozen comma-separated `name[=parameter]` grammar. Not a judgement that the new policy is good, correct or compliant; not a history (two captures give one transition); not the set of responses the policy governs; not the header-class table itself, which stays in `corpus/knowledge/header-change-classes.md` (S456), nor which header names are `policy` (lane policy, frozen in the contract); not any claim that a capture observed origin bytes.

# Policy-value classes — whether a policy statement moved

## 1. The gap this entry closes

Round 83 classified a changed response header by field name (S456, `corpus/knowledge/header-change-classes.md`). Its §7 names the limit this entry closes: a `policy` header whose new value changes freshness semantics still reads `policy`, because a name-level classifier sees `cache-control` on both sides and records one `policy` diff without reading either value.

The value-level classifier `scripts/policy_value_class.py` adds a second step for the `policy` class only: for every changed header whose class is `policy`, it parses the canonical value from both captures under a frozen grammar and names the shape of the move. The claim it serves, C2, is that a capture pair can distinguish an order-only rewrite from a real policy change instead of reporting both as one `policy` diff.

## 2. What the source fixes

Each span below is a literal substring of the single physical line named in `rfc9111.txt`; where the sentence continues on the next line, the line column gives the range.

| Fact the classifier rests on | `rfc9111.txt` line | Raw span (one physical line) |
|---|---|---|
| A freshness lifetime is a duration | 587 | `A response's "freshness lifetime" is the length of time between its` |
| Freshness is a comparison of two quantities | 621 | `response_is_fresh = (freshness_lifetime > current_age)` |
| A fresh response may be reused without the origin | 597 | `When a response is fresh, it can be used to satisfy subsequent` |
| `max-age` supplies the lifetime | 661 | `If the max-age response directive (Section 5.2.2.1) is present,` |
| Response directives are mandatory for a cache | 1205 | `This section defines cache response directives.  A cache MUST obey` |
| `max-age` is a number of seconds | 1214-1216 | `The max-age response directive indicates that the response is to be` / `considered stale after its age is greater than the specified number` |
| `max-age` is generated in token form | 1218-1220 | `This directive uses the token form of the argument syntax: e.g.,` |
| `Cache-Control` is a comma-separated list | 1104, 1775 | `Cache-Control   = #cache-directive` / `Cache-Control = [ cache-directive *( OWS "," OWS cache-directive ) ]` |
| The directive grammar is a name with an optional argument | 1106 | `cache-directive = token [ "=" ( token / quoted-string ) ]` |
| Both argument forms are accepted | 1099 | `insensitively, and have an optional argument that can use both token` |
| Duplicate values are not order-free | 677 | `When there is more than one value present for a given directive` |
| Invalid freshness information is treated as stale | 684 | `directive with non-integer content) to be stale.` |

Two consequences follow from the source and are what make the class table meaningful. First, `max-age` is a duration in seconds (1214-1216), so a changed number is a changed freshness window, not cosmetic text; that is why a numeric parameter gets its own class instead of falling into a generic "value differs". Second, the list grammar (1104, 1775) carries no stated meaning for the position of *distinct* directives, so an order-only rewrite of distinct names is plausibly inert — but the source does give an order rule for duplicates: first occurrence gets used or the response is considered stale (677-679), which is a limit on the `reordered` class, recorded in §6.

The grammar the tool freezes is deliberately narrower than the ABNF: comma-separated `name[=parameter]`, name lowercased, parameter trimmed and lowercased. It keeps the comma list and the optional `=` argument (1106), but it does not unquote a quoted-string parameter and it rejects a name that is not a token.

## 3. The value-level class table

One class is assigned per changed `policy` header. The definitions below are what the tool implements; each example was exercised through the tool's own `value_class` or through a frozen control pair, not invented.

| Class | Definition as implemented | Concrete example |
|---|---|---|
| `reordered` | The parsed `(name, parameter)` multiset is unchanged. | `public, max-age=600` → `max-age=600, public` |
| `numeric_parameter` | Directive names are unchanged and exactly one `(name, parameter)` is replaced, same name, both parameters all digits. | `max-age=600` → `max-age=60` (frozen `control` pair, `ds4cc-primary` `cache-control`) |
| `directive_added` | The before name set is a strict subset of the after name set. | `public` → `public, immutable` (tool selftest) |
| `directive_removed` | The after name set is a strict subset of the before name set. | `public, immutable` → `public` (tool selftest) |
| `directive_changed` | Names are unchanged but a non-numeric parameter, or its presence, differs; or names moved both ways. | `mode=one` → `mode=two` (tool selftest) |
| `header_added` | The field is present on the B side only. | `x-frame-options` absent → `SAMEORIGIN` (frozen `control` pair, `ds4cc-robots`) |
| `header_removed` | The field is present on the A side only. | `public` → absent (tool selftest) |
| `unclassified` | A changed value fails the frozen grammar on either side. | `public` → `bad directive` (a space is not a token; tool selftest) |

`opinion:` the eight class names and the assignment of a move to one of them are lane policy, frozen in `.ufo/waves/round-84/contract.md` §C2 — RFC 9111 states directive syntax and freshness arithmetic, never these names. The source constrains what the classes may treat as meaningful (a number in `max-age`, a name set, a field's presence); it does not choose the taxonomy. A reader should not cite §3 to the RFC as if the RFC named a "reordered" class.

## 4. Verdict order

The verdict is computed from the class counts:

1. `policy-unchanged` when `changed == 0` — no policy-class header moved.
2. `policy-unclassified` when any change is `unclassified` — checked before the equivalence test, so one unreadable field is never waved through.
3. `policy-rewritten-equivalent` when `changed == reordered` — every move was an order-only rewrite.
4. `policy-changed` otherwise.

The frozen order is never looser than its strongest member:
`policy-unchanged < policy-rewritten-equivalent < policy-changed < policy-unclassified`.

A surface's verdict is computed from that surface's counts; the summary verdict is computed from the summed counts, which yields the same verdict as taking the strongest surface verdict. `opinion:` treating `reordered` as not-a-change is a lane decision, supported by the comma-list grammar (1104, 1775) but not stated by the source as "order is insignificant"; §6 records where the source states the opposite.

## 5. Measured record

Real pair, `round-81` capture → `round-82` capture, three declared surfaces: 14 header diffs (4 / 5 / 5), every one in the `per-request` class, 0 changed policy headers → `summary surfaces=3 changed=0 … verdict=policy-unchanged`. Independent re-derivation with the sibling module agrees: the moved names are `date`, `x-fastly-request-id`, `x-served-by`, `x-timer`, plus `x-cache` on `ds4cc-robots` and `ds4cc-sitemap`, and the four policy-class fields present — `access-control-allow-origin: *`, `cache-control: max-age=600`, `expires` and `server: GitHub.com` — are identical strings on both sides of every surface.

Frozen control pairs: `control` prints three change lines — `cache-control numeric_parameter`, `x-frame-options header_added`, `referrer-policy reordered` — and `verdict=policy-changed`; `equivalent` prints one change line — `referrer-policy reordered` — and `verdict=policy-rewritten-equivalent`. Both match `.ufo/waves/round-84/policy-expectations.json` exactly. The tool's `--selftest` printed `selftest: 15/15 passed`.

Receipts: `.ufo/waves/round-84/w1/ScribeKnowledge/tool-real-pair.stdout` / `.exit`, `tool-control.stdout` / `.exit`, `tool-equivalent.stdout` / `.exit`, `tool-selftest.stdout` / `.exit`.

## 6. Limits

1. **Text, not quality.** The classifier says whether the policy statement's text moved and in what shape; it does not say whether the new policy is good, safe, effective, or correct for the property. `max-age=600` → `max-age=60` is a shorter freshness window — the instrument reports the window, not whether shortening it is an improvement. `opinion:` the reading that an order-only move signals no intent to change, and that a numeric move is deliberate tuning, is interpretation; neither is a source claim.
2. **Two captures, not a history.** One pair yields one transition. `policy-unchanged` means those two instants agree, not that the policy never moved between them; `policy-changed` says nothing about when the move happened, how long it persisted, or whether it reverted. A value that changes and changes back inside the interval is invisible.
3. **Duplicate directives break order-only equivalence.** `reordered` is decided by multiset equality, which is not semantic identity when one name appears twice with different parameters. `max-age=600, max-age=60` → `max-age=60, max-age=600` classifies `reordered` and yields `policy-rewritten-equivalent`, while RFC 9111 §4.2.1 says of duplicate values that the first occurrence should be used or the response considered stale (677-679) — so position can select 600 or 60 seconds. No duplicate directive occurs in the real pair or in either control pair.
4. **Case and whitespace are folded into `reordered`.** The grammar lowercases names and trims parameters, so `Max-Age=600` → `max-age=600` and `max-age = 600` → `max-age=600` both classify `reordered` although nothing was reordered. In this tool `reordered` means "canonicalized multiset unchanged".
5. **A numeric reshuffle can read as `numeric_parameter`.** The class is decided by a differing all-digit parameter string, so `max-age=0600` → `max-age=600` classifies `numeric_parameter` although the numeric value did not move.
6. **Quoted-string arguments read as `directive_changed`.** `max-age="600"` → `max-age=600` classifies `directive_changed` because the grammar does not unquote; the source says recipients ought to accept both forms (1099-1102), so this is a formatting move read as a semantic one. The real pair contains no quoted parameter.
7. **Only names the sibling table already calls `policy` are read at the value level.** A changed name the header table calls `unknown` is not value-classified here; that header-level verdict stays decisive for the drift gate.

The working evidence for limits 3-6 is `.ufo/waves/round-84/w1/ScribeKnowledge/value-class-edges.txt`, produced this round by calling the tool's own `value_class` on the listed pairs.

[r84-correction 2026-11-04] **Experimental instrument; semantic capability not
admitted.** The label `policy-rewritten-equivalent` is a frozen tool label, not
a field-independent equivalence guarantee. Referrer-Policy selects the last
recognized policy; the frozen control's reversed list can therefore change
semantics. See `.ufo/waves/round-84/w1/ReviewC2.md`. C2 reports unprovable rather
than changing its target after measurement. Do not use this tool to waive a
policy drift alert or authorize publishing.
