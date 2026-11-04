# ScoutSources — round 84 wave w1

Seat: source scout for C2 (freshness, capability acquisition). One GET-only opening of the source that
grounds the value semantics C2 classifies, plus the registry row the Gate needs. No production corpus
file was written; the row text below is appended by ScribeRegistry. All paths are absolute; scratch was
`/fast/scratch/hyaku/kake-r84/ScoutSources/` and is deleted at yield.

## What was opened and retained

| rendering | GET | status | bytes | sha256 | fetched (UTC) |
|---|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 1 | 200 | 84477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-04T14:04:48Z |
| `https://httpwg.org/specs/rfc9111.html` | 1 | 200 | 178573 | `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64` | 2026-11-04T14:06:43Z |

Both bodies retained at `.ufo/waves/round-84/w1/ScoutSources/rfc9111.txt` and `.../rfc9111-httpwg.html`;
receipts `fetch-receipt.json`, `fetch-receipt-httpwg.json` (final URL, integer status, byte count, sha256,
RFC 3339 fetch time, `truncated: false`, `curl_exit: 0`, curl's own `size_download` equal to the retained
byte count). GET only, no credentials, no cookies, no redirects followed. `curl` exit 0 both times.
Cross-round integrity: my `.txt` fetch is byte-identical to `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt`
(same sha256), so the bytes D1/D2 re-derive from are exactly the bytes I quote.

## Quote method and proof

26 quotes, every one a single-line raw substring of *both* retained renderings, each ≤25 words.
`quotes.tsv` holds qid, section, word count, 1-based line, byte offset and occurrence count per rendering;
`raw-checks.txt` holds the `grep -c -F` invocation, count and exit code per quote (52 checks, all count ≥1,
exit 0); `line-assertions.txt` prints the asserted line itself; `rendering-agreement.txt` proves the same
words appear in both renderings after tag-stripping and the .txt's end-of-line hyphen joining.
`python3 -B build_quotes.py` → `quotes=26 failures=0`, exit 0 (a copy of the builder is kept at
`ScoutSources/build_quotes.py`).

HTML coordinates are 1-based lines of the retained HTML (303 lines, several sections per long line), so
byte offsets are given as well: §4.2 heading/p.1-p.3 line 269 (bytes 69398/69558/69862/70283); §5.2
heading and p.1 line 279 (107517/107665, unidirectional at 107770); §5.2.2 heading line 282 (115955),
obligation 116122; §5.2.2.1 max-age heading line 282 (116325), staleness sentence 116849 (its section-local p.1 `Argument
syntax:` and p.2 `delta-seconds (see Section 1.2.2)` are also on line 282, p.2 at byte 116551 — distinct from
§1.2.2's own definition at line 266/byte 41638, which is what Q12 quotes for a tag-free substring); §5.2.2.2
must-revalidate heading line 282 (117223), body 117410; §5.2.3 heading line 282 (131037), ignore rule
131205; §4.2.1 duplicate/conflict line 270 (76141, 76228); §4.1 normalization line 269 (67165); §1.2.2
delta-seconds line 266 (41638, 41903). `.txt` cross-check lines: 581, 583, 587, 594, 601, 621, 1081, 1083,
1085, 1098, 1108, 1203, 1205, 1208, 1215, 1222, 1224, 1408, 1411, 677, 681, 683, 548, 217, 7, 8, 11.

## Why a max-age value change alters freshness

Grounded, quote by quote, on the retained bytes: a response's freshness lifetime is "the length of time
between its generation by the origin server and its expiration time" (§4.2, html 269 / txt 587); the test
is `response_is_fresh = (freshness_lifetime > current_age)` (§4.2, txt 621); the max-age response directive
makes the response "considered stale after its age is greater than the specified number of seconds"
(§5.2.2.1, html 282 / txt 1215); its argument type is `delta-seconds (see Section 1.2.2)` (txt 1120) and
"delta-seconds  = 1*DIGIT" (txt 217), i.e. a non-negative integer. So `max-age=600 → max-age=60` moves the
age at which the same representation stops being fresh from 600 s to 60 s; the directive-name set and every
other directive are untouched, but the freshness outcome at any age in (60, 600] flips. That is the class
the frozen table calls `numeric_parameter`, and the frozen control's `cache-control` leg is admitted on
exactly these quotes (see `gate-pair.txt`, ADMIT 1).

## Why a directive reorder does not (and what is inference)

The retained bytes ground the pieces but never the sentence. Grounded: the field "is used to list
directives" (§5.2, html 279); a directive is "identified by a token ... and have an optional argument"
(§5.2, html 279); "no argument is defined (nor allowed) unless stated otherwise" (§5.2, html 282);
semantics are stated per directive and a cache "MUST obey" those definitions (§5.2.2, html 282); duplicate
values of one directive are resolved by "the first occurrence ... or the response should be considered
stale" (§4.2.1, html 270); conflicting directives resolve to "the most restrictive" (§4.2.1, html 270).
Nowhere does RFC 9111 attach meaning to the position of a *distinct* directive. `absence-checks.txt`
quantifies it: the word "order" occurs twice in the whole `.txt` (line 515 "in order to satisfy them",
line 548 in §4.1) and **zero** times inside the Cache-Control range lines 1081-1453. The one normative
reorder sentence is §4.1's normalization rule, and it is conditional: reordering is a no-op only "when
order is not significant" *according to the header field's own specification* (html 269). [INFERENCE]:
therefore, for `cache-control`, an order-only rewrite of the value changes nothing RFC 9111 defines, so
the `reordered` class is sound for that field. This is an inference from per-directive semantics plus a
proved absence, not a quoted sentence; no retained sentence says "directive order is insignificant".

## What I could NOT ground

- `referrer-policy` and `x-frame-options`: **0 occurrences** in both retained renderings
  (`absence-checks.txt`). RFC 9111 cannot ground the frozen `equivalent` pair's `reordered` expectation
  for `referrer-policy`, nor the `header_added` expectation for `x-frame-options` (the latter is only a
  field-presence fact of the synthetic captures). Those legs need their own primary texts.
- An explicit rule that Cache-Control directive order is insignificant (see above): absent.
- Whether `referrer-policy` is in fact order-sensitive. I hold no bytes for that field and do not judge
  it; `gate-pair.txt` REJECT 1 records it as a flip condition with the hypothesis left unasserted.
- Any statement that a changed `max-age` is a *policy* change in the lane's sense: that mapping is lane
  policy, not RFC 9111.

## A defect in the frozen pointer (reported, not patched)

The contract §C2 and this seat's item both say "§5.2.2.2 `max-age`". Both renderings say otherwise:
`5.2.2.1.  max-age` at `.txt` 1208 / HTML line 282, anchor `rfc.section.5.2.2.1`, section
`cache-response-directive.max-age`; `5.2.2.2.  must-revalidate` at `.txt` 1222 / HTML line 282 byte 117223,
section `cache-response-directive.must-revalidate`. `heading-mismatch.txt` carries the coordinates. The row
cites 5.2.2.1 and names 5.2.2.2 as must-revalidate; the frozen files are read-only for this seat.

## Row delivery

`ScoutSources/s457-row.txt` is the proposed row in contract-v1 shape: 11 cells, no `|` inside a cell,
ISO `opened` 2026-11-04, `recheck` 180d, `used-by` corpus/knowledge/policy-value-classes.md, `kind` spec,
`tier` A, `status` queued (ScribeRegistry marks it mined). It was machine-checked: `split('|')` yields 13
tokens, 11 non-empty cells. **S456 and S457 are two renderings of one RFC**: S456 is the rfc-editor `.txt`
scoped to cache storage/validators and explicitly excludes "cache-directive argument syntax"; S457 is the
HTTPWG HTML scoped to that excluded value-level semantics. The reviewer should judge the duplication
explicitly; the two URLs normalize differently, so the census stays clean.

While I worked, ScribeRegistry landed an S457 row at `corpus/SOURCES.md` line 204 (uncommitted, +1 line)
with the corrected `https://httpwg.org/specs/rfc9111.html` source. I verified every anchor claim it makes
against the retained bytes: `row-anchor-check.txt` maps each claim to its line/byte and all are VERIFIED,
including its parenthetical that 5.2.2.2 is must-revalidate and its §5.2.3 ignore-rule citation. It differs
from my draft only in the source-cell wording (it adds the section list), `status` (`mined` vs my `queued`),
and the absence of byte offsets; I recommend adding the byte offsets and the `.txt` cross-check lines.

## Census / D4 interaction

`census-probe.txt` imports `census_w04` read-only from the frozen counter. Current tree with the landed
S457: derived W04 = 22, equal to the frozen control's 22 (D4's conjunct intact; `controls/census-after.txt`
agrees, `census_exit=0`). Counterfactual: rewriting S457's source to `https://www.rfc-editor.org/rfc/rfc9111.txt`
derives 23 and adds exactly `S457 duplicate url www.rfc-editor.org/rfc/rfc9111.txt across scopes`, which
would reopen D4 — so the L1's URL correction was necessary, not cosmetic. (Precedent, not exemption: the
frozen control already carries S453/S454/S455 on the same rfc9110.txt URL with distinct scopes.)
Honest note on method: my first probe appended the row after the `## Registry` heading, where the census
never reads it, and reported 22 for both variants; that probe was wrong and was redone with the row inserted
inside the registry table, which is what the numbers above report.

## Commands and exit codes

- `curl -sS --max-time 60 -o rfc9111.txt -w … https://www.rfc-editor.org/rfc/rfc9111.txt` → exit 0, http_code=200, size_download=84477.
- `curl -sS --max-time 90 -o rfc9111-httpwg.html -w … https://httpwg.org/specs/rfc9111.html` → exit 0, http_code=200, size_download=178573 (matches the L1's probe).
- `sha256sum rfc9111.txt` → `aeb52adb…`; `sha256sum /home/vgpnk/…/round-83/w1/ScoutSources/rfc9111.txt` → same digest.
- `python3 -B /fast/scratch/…/build_quotes.py` → `quotes=26 failures=0`, exit 0 (one earlier run exited 1 on a wrong asserted line for `STD: 98`; the line is 7, not 5, and the fix is in the kept copy).
- `grep -c -F` × 52 → all ≥1, exit 0 (raw-checks.txt).
- `grep -c -i -F 'order is not significant' rfc9111.txt` → 0 (wrapped at line 548); `…rfc9111-httpwg.html` → 1.
- `awk 'NR>=1081 && NR<=1453' rfc9111.txt | grep -c -i -w order` → 0.
- `python3 -B` import of `.ufo/waves/round-84/c84_defect_queue.py` + `census_w04` → 22 == 22 current, 23 with the `.txt` URL, exit 0.
- No VCS mutation; read-only `git status`/`git diff`/`git rev-parse` only. No tool installs (curl and python3 preinstalled; pacman deliberately unused).

## Verdict

Grounding delivered and admissible: RFC 9111's §4.2, §5.2, §5.2.2 and §5.2.2.1 `max-age` define the
numeric parameter whose change moves freshness, and §4.2.1 resolves duplicates/conflicts without reference
to the position of distinct directives; the `reordered` class is sound for `cache-control` as an inference
from that plus a proved absence. Two limits must travel with C2: the frozen `equivalent` pair's
`referrer-policy` leg is **not** grounded by this source (0 occurrences; flip condition recorded), and the
frozen pointer "§5.2.2.2 max-age" is wrong in both renderings. The S457 row is row-shaped and cell-complete,
the landed version at `corpus/SOURCES.md:204` is verified claim by claim, and the HTMLWG source cell leaves
D4's census intact where the `.txt` URL would have reopened it.

## Addendum (refer token census)

The absence of a referrer field is total, but the surrounding word census has an arithmetical trap
worth recording because finding 7 cites it. Case-insensitive whole-token search for `refer` over both
renderings returns **52 tokens, 8 distinct types** (`.txt` 19 / `.html` 33), not 27:
`references` 25, `referring` 8, `prefers` 6, `preferred` 4, `reference` 3, `preference` 2,
`preferences` 2, `preferable` 2. Every one is either a citation (`references`/`referring`/`reference`)
or a `prefer*` word — and `prefer` contains `refer` only as `p` + `refer`, which is why a flat
`grep -i refer` over-reports. Zero substring and zero whole-word hits for
`referrer`/`Referrer`/`referer`/`Referer` in either file. Receipt: `ScoutSources/referrer-token-census.txt`.
Precise sentence: RFC 9111 names no referrer field in either spelling; it does contain 52 non-referrer
tokens that a case-insensitive `refer` search also matches.
