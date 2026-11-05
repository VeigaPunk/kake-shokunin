# ScoutErrata — round 95 (kake, w1) seat report

Seat: ScoutErrata (scout, leaf member — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE). Round base `fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3`; instruments commit `43cdd9fc899a2613d8ba7b55edf820825e57b4d1`; freeze commit `8f638b591e739e1863f5fa22334d5e15178189ed` (HEAD of the lane at read time; `git -C <lane> rev-parse HEAD` → `8f638b591e739e1863f5fa22334d5e15178189ed`).

## 0. Instrument digests (verified before any attack)

Command: `sha256sum .ufo/waves/round-95/c95_selfassess.py .ufo/waves/round-95/c95_conditional.py` (cwd = LANE, rc 0).

| file | observed sha256 | pinned (`controls/instrument-sha256.txt`) | match |
|---|---|---|---|
| `.ufo/waves/round-95/c95_selfassess.py` | `8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193` | same | yes |
| `.ufo/waves/round-95/c95_conditional.py` | `f09f84090fdda405992d7b51191be8838549e3df402b0898eb2ca00c4c3ff312` | same | yes |

No mismatch. Nothing under `controls/` or `frozen/` was touched; no instrument was patched.

## 1. The errata page (one fetch)

Command (exactly one invocation, rc 0, printed `200`):

```
curl -sS -L -o errata-9110.html -D headers.txt -w '%{http_code}' \
  -A 'Mozilla/5.0 (kake-r95 ScoutErrata)' \
  'https://www.rfc-editor.org/errata_search.php?rfc=9110'
```

- Requested URL: `https://www.rfc-editor.org/errata_search.php?rfc=9110` (bare form). It answered **HTTP 302** with `location: https://errata.rfc-editor.org/search/?rfc_number=9110`, and the redirect was followed inside the same invocation → **HTTP 200**, `content-type: text/html; charset=utf-8`, `Date: Thu, 05 Nov 2026 16:32:52 GMT`.
- `&rec_updated=1` was **not** appended: the bare page returned the full errata list (14 records), so it was not empty.
- Accessed (UTC): **2026-11-05T16:32:51Z**. Bytes: **97741**. sha256: **e6ddebb240b522f36acf0ccc9b6a52030a35ff77d17203dbd1fcf6d1339c0911**.
- Retained byte-exact copy: `.ufo/waves/round-95/w1/ScoutErrata/errata-9110.html` (`cmp` against the scratch body → identical; sha256 and size re-measured on the lane copy: `e6ddebb…c0911`, 97741 bytes). Receipt: `.ufo/waves/round-95/w1/ScoutErrata/fetch.txt`.
- Page fetches: **one**. No crawl, no per-EID page opened, no second query. The 302 hop is the origin's relocation of the errata search to `errata.rfc-editor.org`, not a second page request.
- Tooling: no install or upgrade was needed; `curl 8.23.0` (system) was the only client. Nothing under `~/.local/bin` or any PATH directory was created or modified.

### 1a. Every record on the page (raw HTML line numbers in the retained body)

Status headings present: `Verified (6)` (line 108), `Reported (2)` (line 689), `Rejected (6)` (line 904). **No** "Held for Document Update" heading.

| erratum id | status | type | section the record cites | one-line note |
|---|---|---|---|---|
| 7138 | Verified | Technical | 12.5.1 | media-range example in the Accept field (row 100 of the text extract) — unrelated to the round's sections |
| 7306 | Verified | Technical | 14.1.1 | charset example — unrelated |
| 7419 | Verified | Technical | 8.3.2 | Content-Encoding example — unrelated |
| 7105 | Verified | Editorial | B.1 | "Changes from RFC 2818": CN-ID deprecation wording — unrelated |
| 7109 | Verified | Editorial | 15.4.9 | 308 Permanent Redirect text should match 15.4.8 (307) wording — unrelated |
| 8268 | Verified | Editorial | B.2 | the absolute-form-priority sentence belongs in RFC 9112 Appendix C.3 — unrelated |
| 9162 | Reported | Technical | 5.2 | "combined field value" is a comma SP separated list, but the example shows comma SP — adjacent to §5.6 list grammar, does **not** target 5.6.1.2 or 5.6.3 |
| 9164 | Reported | Technical | Appendix A | Appendix A's list-rule expansion is not the only transformation it applies; reporter calls the collected grammar and the body semantically equivalent, and cites `list rules are expanded per Section 5.6.1` (raw lines 855/859) and `weak §8.8.3 %s"W/" — Appendix A %x57.2F` (raw line 876) |
| 7107 | Rejected | Technical | 6.5.1 | HTTP/1.1 §7.1.2 cross-reference — unrelated |
| 7599 | Rejected | Technical | 6.4.1 | 205 No Content vs "1xx, 204 and 304 have no content" — unrelated |
| 7870 | Rejected | Technical | 8.6 | "Content-Encoding" / redirect handling note — unrelated |
| 8138 | Rejected | Technical | 15.4 | status-code range note — unrelated |
| 8459 | Rejected | Technical | 15 | status-code three-digit range — unrelated |
| 7530 | Rejected | Editorial | 15.5.2 | 401 Unauthorized wording — unrelated |

### 1b. Errata touching the round's four target sections

**Verified or reported errata touching §5.6.1.2, §5.6.3, §8.8.3 or §13.1.x: none.**

- §5.6.1.2 — no record.
- §5.6.3 — no record.
- §8.8.3 — no record *targets* §8.8.3. EID 9164 (Reported) *names* the `weak §8.8.3 %s"W/"` rule while describing Appendix A's rendering (raw line 876), but the section it cites is "Appendix A" and its own conclusion is that the collected grammar and the body define the same language.
- §13.1.x — no record (no record cites 13.1 at all).

Adjacent-but-not-targeting: EID 9162 (Reported) cites §5.2, the section that introduces "combined field value"; its subject is the comma SP separator in that section's own example, not the §5.6.1/§5.6.3 list grammar. Rejected records (6) and Verified records other than the Appendix A one cite no §5.6/§8.8/§13.1 text.

**Interpretation for the C2 claim (the row's clause):** the RFC text the v2 contract rests on (S478 §5.6.1.2/§5.6.3, S455 §8.8.3 `etagc`, S473/S474 §13.1.x) has **no pending verified or reported erratum** that changes it. One reported erratum (9164) names §5.6.1 and §8.8.3 rules and states they are semantically equivalent to the body, so it does not alter any contract clause. [INFERENCE from the page listing: the page is the publisher's complete errata list for RFC 9110 at fetch time; it does not cover errata filed against RFC 9110 in other venues, e.g. the httpwg issue tracker.]

## 2. Anchor re-verification against the retained RFC 9110 body (read-only)

Retained body: `.ufo/waves/round-94/w1/ScoutRFC/rfc9110.txt`.

- `sha256sum` → **21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a** — matches the digest named in the seat spec and in rows S471–S475. The same digest is held by `.ufo/waves/round-81/w1/ScoutSources/rfc9110.txt` and `.ufo/waves/round-93/L1/src/rfc9110.txt` (both re-hashed by this seat: identical).
- Line numbers below are 1-based over the file's `\n`-split lines; the file was read only.
- Full verbatim excerpts: `.ufo/waves/round-95/w1/ScoutErrata/anchors-verbatim.md`.

### S478 — §5.6.1.2 (heading line 1693, lines 1695-1702) — HOLDS

```
1693: 5.6.1.2. Recipient Requirements
1695: Empty elements do not contribute to the count of elements present. A
1696: recipient MUST parse and ignore a reasonable number of empty list
1697: elements: enough to handle common mistakes by senders that merge
1698: values, but not so much that they could be used as a denial-of-
1699: service mechanism. In other words, a recipient MUST accept lists
1700: that satisfy the following syntax:
1701:
1702: #element => [ element ] *( OWS "," OWS [ element ] )
```

First sentence of the located range (line 1695): *"Empty elements do not contribute to the count of elements present."* — the row's claim that empty elements are accepted and contribute no members is carried by lines 1695-1702 (the `#element` production at 1702 admits `[ element ]` empty brackets and `*( OWS "," OWS [ element ] )` empty trailing members). The S478 teaches clause ("A recipient MUST accept lists with empty elements, empty elements do not count toward the number present, and OWS (SP or HTAB) surrounds each comma") is supported by lines 1695-1702 plus §5.6.3 below; the sentence "In other words, a recipient MUST accept lists that satisfy the following syntax:" begins at 1699 and the production is at 1702, inside the cited range 1695-1702.

### S478 — §5.6.3 (heading line 1745, lines 1762-1764, production line 1774) — HOLDS

```
1745: 5.6.3. Whitespace
1762: OWS and RWS have the same semantics as a single SP. Any content
1763: known to be defined as OWS or RWS MAY be replaced with a single SP
1764: before interpreting it or forwarding the message downstream.
1774: OWS = *( SP / HTAB )
1775: ; optional whitespace
```

First sentence of the located range (1762): *"OWS and RWS have the same semantics as a single SP."* The production at 1774 is exactly `OWS = *( SP / HTAB )`; line 1775 is the trailing comment (the row cites 1774 for the production — correct; note the production occupies 1774-1775 with its comment). The §5.6.1 pointer to §5.6.3 sits at lines 1670-1672 (outside the S478 anchor cells, as it was in round 94).

### S455 — §8.8.3 `etagc` (line 3587, obs-text) — text present at the cited line; the row's cited anchor does NOT name line 3587

```
3570: 8.8.3. ETag
3584: entity-tag = [ weak ] opaque-tag
3585: weak = %s"W/"
3586: opaque-tag = DQUOTE *etagc DQUOTE
3587: etagc = %x21 / %x23-7E / obs-text
3588: ; VCHAR except double quotes, plus obs-text
```

Line 3587 reads exactly `etagc = %x21 / %x23-7E / obs-text` — obs-text **is** admitted inside an opaque-tag, as contract v2 clause C2 asserts. First sentence of the located range (3584): *"entity-tag = [ weak ] opaque-tag"*. `obs-text` itself is defined at line 1589 (§5.5 Field Values; the line reads `obs-text       = %x80-FF`, the padding is the RFC's own column alignment).

But S455's anchor cell names only "§8.8.3 lines 3570-3617 (opaque validator 3574-3576; W/ rule 3607-3612)" — line 3587 sits **inside** the cited span 3570-3617, so the span covers it, yet no cell-level pointer names it. S455's **scope** cell additionally states, verbatim: *"…not conditional requests…"*, while the round-95 contract grounds clause C2 (obs-text inside an opaque-tag, a conditional-request evaluation) on S455. See Finding F1 below.

### S473 — §13.1.2 (lines 5872-5932) — HOLDS

```
5872: 13.1.2.  If-None-Match
5880:   A recipient MUST use the weak comparison function when comparing
5881:   entity tags for If-None-Match (Section 8.8.3.2), since weak entity
5882:   tags can be used for cache validation even if there have been changes
5883:   to the representation data.
5885:     If-None-Match = "*" / #entity-tag
5917:   To evaluate a received If-None-Match header field:
5919:   1.  If the field value is "*", the condition is false if the origin
5920:       server has a current representation for the target resource.
5922:   2.  If the field value is a list of entity tags, the condition is
5923:       false if one of the listed tags matches the entity tag of the
5924:       selected representation.
5926:   3.  Otherwise, the condition is true.
5928:   An origin server that evaluates an If-None-Match condition MUST NOT
5929:   perform the requested method if the condition evaluates to false;
5930:   instead, the origin server MUST respond with either a) the 304 (Not
5931:   Modified) status code if the request method is GET or HEAD or b) the
5932:   412 (Precondition Failed) status code for all other request methods.
```

First sentence of the located range (line 5874): *"The "If-None-Match" header field makes the request method conditional on a recipient cache or origin server either not having any current representation of the target resource, when the field value is "*", or having a selected representation with an entity tag that does not match any of those listed in the field value."* Every sub-pointer in S473's anchor cell lands where the row says: heading 5872 ✓, weak-comparison requirement 5880-5883 ✓, field syntax 5885 ✓, evaluation steps 5917-5926 ✓, status split 5928-5932 ✓ (the GET-or-HEAD / 412 split is at 5930-5932, inside the cited range).

### S474 — §13.1.3 (lines 5942+) — HOLDS with one off-by-two in a sub-pointer

```
5942: 13.1.3.  If-Modified-Since
5956:   A recipient MUST ignore If-Modified-Since if the request contains an
5957:   If-None-Match header field; …
5963:   A recipient MUST ignore the If-Modified-Since header field if the
5964:   received field value is not a valid HTTP-date, the field value has
5965:   more than one member, or if the request method is neither GET nor
5966:   HEAD.
5968:   A recipient MUST ignore the If-Modified-Since header field if the
5969:   resource does not have a modification date available.
6006:   To evaluate a received If-Modified-Since header field:
6008:   1.  If the selected representation's last modification date is
6009:       earlier or equal to the date provided in the field value, the
6010:       condition is false.
6012:   2.  Otherwise, the condition is true.
6023: 13.1.4.  If-Unmodified-Since
6037:   A recipient MUST ignore If-Unmodified-Since if the request contains
6038:   an If-Match header field; …
6043:   A recipient MUST ignore the If-Unmodified-Since header field if the
6044:   received field value is not a valid HTTP-date (including when the
6045:   field value appears to be a list of dates).
6047:   A recipient MUST ignore the If-Unmodified-Since header field if the
6048:   resource does not have a modification date available.
6071:   1.  If the selected representation's last modification date is
6072:       earlier or equal to the date provided in the field value, the
6073:       condition is true.
```

First sentence of the located range (5944): *"The "If-Modified-Since" header field makes a GET or HEAD request method conditional on the selected representation's modification date being more recent than the date provided in the field value."* Sub-pointers: heading 5942 ✓; ignore on If-None-Match 5956-5958 ✓; ignore on invalid value / non-GET-or-HEAD 5963-5966 ✓; ignore on absent modification date 5968-5969 ✓; §13.1.4 heading 6023 ✓; ignore on If-Match 6037-6039 ✓; ignore on invalid value 6043-6045 ✓; ignore on absent modification date 6047-6048 ✓; true-condition boundary 6072-6073 ✓. **One drift**: S474's anchor cell says "§13.1.3 … evaluation steps lines 6004-6011"; the steps actually occupy **6006-6012** (the lead-in line "To evaluate a received If-Modified-Since header field:" is 6006 and step 2 ends at 6012). Lines 6004-6011 still contain step 1 (6008-6010) but cut the lead-in at the top and step 2's last line at the bottom. Minor, non-blocking; see Finding F2.

### Anchor check summary

| anchor | located? | text matches the row's claim? | note |
|---|---|---|---|
| S478 §5.6.1.2 (1693, 1695-1702) | yes | yes | empty elements accepted, contribute nothing; production at 1702 |
| S478 §5.6.3 (1745, 1762-1764, 1774) | yes | yes | `OWS = *( SP / HTAB )` at 1774 (comment at 1775) |
| S455 §8.8.3 `etagc` (3587) | yes, exact text | yes (obs-text admitted) | line 3587 is inside S455's cited span 3570-3617 but no cell-level pointer names it; S455's scope excludes "conditional requests" (F1) |
| S473 §13.1.2 (5872-5932) | yes | yes | every sub-pointer lands as claimed |
| S474 §13.1.3/§13.1.4 (5942+) | yes | yes | "evaluation steps 6004-6011" are actually 6006-6012 (F2) |

## 3. Findings (read-only; nothing was patched)

**F1 — S455's scope excludes the use the round-95 contract makes of it (defect against the registry's own rule).**
`corpus/SOURCES.md` S455 scope cell: *"…not conditional requests…"*. The round-95 freeze's Sourced-claim requirement grounds contract v2 clause C2 (obs-text inside an opaque-tag) on S455, and clause C2 governs the conditional-request evaluation instrument. `corpus/QUALITY.md` (Round 85 section) says: *"Also reject widening an existing source row's immutable scope by adding a citation: append a newly grounded row for previously excluded order/argument support (S461 supplements S457)."* Under that rule the C2 grounding cannot ride on S455 by citation. Suggested remedy for the L1 (a new row, not an edit to S455): a row for RFC 9110 §8.8.3 `etagc` (line 3587) plus §5.5 `obs-text` (line 1589), scope "obs-text admissibility inside an opaque entity tag", anchored to the retained body's lines 3584-3588 and 1589, with a located quote (e.g. `etagc = %x21 / %x23-7E / obs-text`). This seat did not draft that row: the seat spec names only S479 as its deliverable. **[INFERENCE]** — the rule's wording ("append a newly grounded row") is applied by analogy to the scope-versus-citation situation; a reviewer may read the round-95 reading as admissible if the C2 grounding is declared as a new claim on S455 rather than as a widening.

**F2 — S474's "evaluation steps lines 6004-6011" is off by two.** Actual lines 6006-6012. Everything the row claims (lead-in + two steps) is still inside the cited span, so this is a citation-precision defect, not a wrong claim.

**F3 — a whitespace-only field value is not an RFC-exact clause.** Contract v2 clause C1 says "A whitespace-only field value is not a list and stays refused." The RFC body does not support that sentence as an RFC-exact rule: §5.6.3's OWS rule defines optional whitespace, and §5.5 states (line 1591) *"A field value does not include leading or trailing whitespace."* — so a whitespace-only field value, once trimmed, is an empty field value, and an empty list is admitted by the C1 clause itself. **[INFERENCE]** — the refusal of a whitespace-only value is a lane convention (a distinct token from an empty list), not RFC-exact ground, and the contract should say so. It is not an erratum matter and no erratum touches it.

**F4 — the errata page gives no ground for any C2 clause; it only certifies that the ground is undisturbed.** Recorded so the S479 row is not mistaken for a source that decides a contract clause: its scope is errata status only.

**F5 — the errata search has moved hosts.** `https://www.rfc-editor.org/errata_search.php?rfc=9110` now 302s to `https://errata.rfc-editor.org/search/?rfc_number=9110`. Any freshness re-check that fetches the old URL will see a 302 and must follow it (or record the redirect) to observe the page. This is why the row's anchor cell records both the requested URL and the final URL.

## 4. S479 (drafted row)

File: `.ufo/waves/round-95/w1/ScoutErrata/S479-row.md` (the row itself is in a fenced context there; it is one Markdown table row with 11 cells).
Receipts: `.ufo/waves/round-95/w1/ScoutErrata/quotes.json` (located quote), `.ufo/waves/round-95/w1/ScoutErrata/census-validate-control.txt`, `.ufo/waves/round-95/w1/ScoutErrata/census-validate-with-s479.txt`, `.ufo/waves/round-95/w1/ScoutErrata/census-withrow.txt`. The two validate outputs are byte-identical apart from the mirror path they name: the added row produces no finding, and the W04 "duplicate url across scopes" warnings in them are pre-existing lane warnings (the same 40 appear in the control run, none for S479 — its URL is new).

- 11 cells; `python3` `len(row.split('|')[1:-1]) == 11` → True; `'\\|' in row` → False (no literal or escaped pipe in any cell).
- kind `dataset`, tier `A` (scoped to errata status), status `mined`, opened `2026-11-05`, recheck `90d`, used-by `.ufo/waves/round-95/freeze.md` (exists at the freeze commit; the L1 should append the lesson and knowledge-entry paths when they land).
- teaches = one grounded clause + a 21-word located quote copied verbatim from the fetched body (raw line 863): *"Each is semantically equivalent ABNF, so no interoperability question arises: the collected grammar and the body define the same language throughout."* `q in raw_body` → True (count 1); `q in row` → True.
- Census on a scratch mirror of the freeze commit (`git archive 8f638b59`): control rc 0 `mirror ok`; with S479 rc 0 `mirror ok`, no S479 finding; rows 215 → 216, tier.A 191, status.mined 186.
- The row's anchor cites the retained body path `.ufo/waves/round-95/w1/ScoutErrata/errata-9110.html`; it must be committed together with the row.

VERDICT: **S479-DRAFT admit-ready** (scope-limited: errata status of RFC 9110; it supplies no RFC-text grounding for any contract clause).

ANCHOR-CHECK S478-5.6.1.2 ok (1693, 1695-1702, first sentence "Empty elements do not contribute to the count of elements present."); ANCHOR-CHECK S478-5.6.3 ok (1745, 1762-1764 first sentence "OWS and RWS have the same semantics as a single SP.", production 1774 `OWS = *( SP / HTAB )`); ANCHOR-CHECK S455-8.8.3 text ok (3587 `etagc = %x21 / %x23-7E / obs-text`) but the row's cited span does not name 3587 and its scope excludes conditional requests (F1); ANCHOR-CHECK S473-13.1.2 ok (5872-5932, first sentence "The "If-None-Match" header field makes the request method conditional…", status split 5930-5932); ANCHOR-CHECK S474-13.1.x ok (5942+, first sentence "The "If-Modified-Since" header field makes a GET or HEAD request method conditional…") with the evaluation-steps pointer off by two (6004-6011 → 6006-6012, F2).

## 5. Scope and hygiene

- Written, all inside the seat's own directory: `.ufo/waves/round-95/w1/ScoutErrata/` — `errata-9110.html` (byte-exact fetched body), `errata-9110.txt` (text extract used for the section/status table), `fetch.txt`, `anchors-verbatim.md`, `S479-row.md`, `S479-row.txt` (the row alone, for a one-line append), `quotes.json`, `census-validate-control.txt`, `census-validate-with-s479.txt`, `census-withrow.txt`; and this report at `.ufo/waves/round-95/w1/ScoutErrata.md`.
- Nothing else in the lane tree was written; no other round dir, no sibling lane, no fleet repo, no `.ufo/state`, no `MANIFEST.json`. `git -C <lane> status --porcelain` after the seat's writes lists this seat's two paths (`.ufo/waves/round-95/w1/ScoutErrata.md` and `.ufo/waves/round-95/w1/ScoutErrata/`) alongside other seats' untracked entries, which are not this seat's. In the fleet root, `git status --porcelain` shows `.scratch/run15-state.json` modified and `.ufo/closure-kaidoku-r92.json` untracked — both pre-date this seat's writes and are outside the lane; this seat never wrote to the fleet root.
- No mutating git or jj command was run anywhere. The only git use was read-only (`rev-parse`, `archive` of the freeze commit into scratch, `status --porcelain`).
- Scratch: `/fast/scratch/hyaku/kake-r95/ScoutErrata/` (fetch, parse, anchors, first census run) and `/fast/scratch/hyaku/kake-r95/ScoutErrata2/` (regenerated census receipts) — both deleted before this report was written; receipts were copied into the seat directory first. The scratch trees contained the mirror, the raw body, the header dump (with Cloudflare cookies — deliberately not copied into the lane) and the census outputs.
- No host sysctl was touched; no tool was installed or upgraded (none needed).
