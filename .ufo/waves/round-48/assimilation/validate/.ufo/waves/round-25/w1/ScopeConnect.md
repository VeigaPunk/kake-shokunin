# ScopeConnect — round-25 C1 scope and wording constraints

Seat: `KakeR25.ScopeConnect` (read-only scout; this file is its only write). Axes judged: operability, freshness. No r24 probe, assignment or counter was read or run. No website, browser, network, account or publication action. No tools installed or updated.

## Evidence (all relative to the lane root)

| # | Fact | Where |
|---|---|---|
| E1 | WCAG 2.2 sits in **Frontier**, not Core: "accessibility conformance (WCAG 2.2) … Ground moves to Core only with source-backed entries and a gate." | `PROVINCE.md:22-26` |
| E2 | Province sections are append-only, dated; earlier lines are kept unchanged ("the four lines above are unchanged"; r22/r23/r24 are appended sections). | `PROVINCE.md:7`, `:50-72` |
| E3 | Adjacent owners: `tabi` drives browsers; `chousa` owns research method and source hierarchy; `kagi` owns secrets and credentials ("kake records no secret values"); publication and accounts stay with the operator. | `PROVINCE.md:28-37`, `:17-18` |
| E4 | The corpus Frontier still lists "WCAG 2.2" as open ground; the coverage map has no accessibility row. | `corpus/README.md:102-104`, `:15-43` |
| E5 | `SOURCES.md` registry ends at **S034**. The contract cites "S035 WCAG22 pinned REC 2024-12-12", but no S035 row exists. Three WCAG items are still *unopened leads*: the ISO press release, the WCAG overview ISO/EAA section, and Understanding 2.5.8. | `corpus/SOURCES.md:42`, `:85-87`; `.ufo/waves/round-25/contract.json:13` |
| E6 | The census validator rejects a row with E11 when a `used-by` path is missing, E04 for a duplicate URL+scope, and E08 for an `opened` date in the future. The baseline already carries one warning, W04 (S033). | `../scripts/sources-census.sh:24-33`; `.ufo/waves/round-25/census-before.json` |
| E7 | Population: 55 criteria (31 A, 24 AA), 4.1.1 absent, `source` = dated TR URL, `sourceSha256` 6e3c5fe3…7057. This matches `source-wcag22.html` byte for byte (sha256 checked). | `.ufo/waves/round-25/population.json`; `sha256sum .ufo/waves/round-25/source-wcag22.html` |
| E8 | **Contradiction:** `normativeText` for **2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7 and 3.3.8** begins with `New `. In the pinned HTML this word is the editorial `<p class="change">New</p>` marker that follows `(Level AA)`, not criterion body. The draft knowledge entry says `normativeText` "excludes headings … conformance labels". | `source-wcag22.html` (`id="target-size-minimum"` block); `corpus/knowledge/accessibility-review-packet.md:21-23` |
| E9 | The extraction put spaces at tag boundaries: 29/55 `normativeText` values contain ` .` or ` ,` (45 punctuation-only whitespace tokens in total, e.g. `CSS pixels , except`). The rendered spec reads `CSS pixels, except`. | population scan (python, read-only) |
| E10 | All 55 sibling cards in `w1/SC*.md` scan clean against the shared interface: exactly one json fence, exact 10 fields, id/title/level/source match, quote contained (whitespace-collapsed) and ≤25 whitespace words, status `not-assessed`, no quote starting with `New`, no owned-property hostname (ds4cc/kimi/veigapunk/github.io). | read-only python scan of `.ufo/waves/round-25/w1/SC*.md` |
| E11 | 49 cards use verdict words (pass/fail/conformance/inapplicable) only inside disclaimers. Example, 1.4.13 limitation: "does not declare the criterion passed, failed, inapplicable or conformant." | same scan |
| E12 | Browser and assistive-technology (AT) execution appears as an imperative publisher step in one card. 4.1.3 publisherCheck: "Then confirm with at least one screen reader and browser pairing…". Other browser/zoom/screen-reader mentions (21 cards) sit in evidenceNeeded or failureExample. | `w1/SC413.md` |
| E13 | Authentication content: 3.3.8 discusses password-field paste/autofill design, and 1.1.1 covers CAPTCHA alternatives. Neither records a credential value, a test account or a bypass. | `w1/SC338.md`, `w1/SC111.md` |
| E14 | `corpus-contract.mjs` checks only `corpus/knowledge/*.md` for the `source:`/`verified-at:`/`recheck:` trio in the first 8 lines, so the cards JSON is exempt. `freshness-sweep.mjs` §paths only resolves `~/` and `/home/vgpnk/` cites in `.md` files, so the relative cites in the draft entry cannot raise §paths drift. | `scripts/corpus-contract.mjs:117,181-206`; `scripts/freshness-sweep.mjs:125,233-240` |
| E15 | Lane gate convention: an 8-column registry row (`Name \| Kind \| Entry command \| Verdict map \| Self-test \| Pinned values / frozen proof \| Write scope \| Owner`) plus a Situation→Decision table that routes browser work to tabi and publishing/accounts to the operator. 64 maps to `could-not-evaluate`, and stdout is still one JSON object. | `SKILL.md:385-411` |

## Exact scope and wording constraints for the new C1

1. **Name:** call it a "publisher-side WCAG 2.2 Level A/AA manual-review packet" or "packet inventory". NEVER call it an accessibility audit, conformance check, compliance, or "WCAG gate". JSON MUST carry `websiteConformance: "not-assessed"` on every exit path, including 2 and 64.
2. **Province move:** add a dated `## Round-25 publisher-side addition` section to `PROVINCE.md` and a `## Round-25 …` section to `corpus/README.md`, plus one coverage-map row. Do not edit the r20 Frontier line (E1, E2). The wording MUST say that *review preparation* gained a source-backed entry and a gate, while WCAG **conformance evaluation** of any property stays Frontier/open.
3. **Adjacency routing** (copy into the SKILL decision table, E15):
   - Rendering, reflow/zoom, keyboard, focus, pointer, and screen-reader/AT observation go to a *separate authorized evaluation*. Browser execution goes to `tabi`.
   - Credentials, test accounts and session material go to `kagi`/operator. Cards and evidence MUST NOT hold secret values, sign-in steps, CAPTCHA solving or bypass, or authentication-defeat techniques. Review 3.3.7/3.3.8/1.1.1 against form and process design and source only.
   - Source hierarchy stays with `chousa`. Ground cards only in S035 normative text. Do not cite the Understanding, How-to-Meet or ISO/EAA pages (still unopened leads, E5) as S035.
   - Deployment and publication go to the operator.
4. **Card prose:** publisherCheck MUST be phrased as preparation, or as a request to an authorized evaluator. It MUST NOT be an instruction for kake to run a browser or AT. Fix `4.1.3` (E12): for example "Request an authorized evaluation that records whether each message is announced…". failureExample MUST be hypothetical and MUST NOT name an owned property (E10 currently holds). Verdict words are allowed only as negated disclaimers (E11). So **do not** add a vocabulary lint to the tool or counter: it would false-fail 49 valid cards. Enforce verdicts only through `status`.
5. **Quote mechanics** (tool, counter and selftest MUST share one definition):
   - Eligible text is `' '.join(normativeText.split())`.
   - A word is a whitespace token, so ` .` counts as one (E9). Authors MUST copy quotes from `population.json`, not the rendered W3C page, or containment fails.
   - Expected interface ids for PacketTests: `quote-too-long`, `quote-not-in-source`, and per E8 `quote-includes-change-marker`. Naming is advisory; whatever the tool chooses, the counter and selftest must assert the identical ids.
6. **Sources registry (freshness):** add exactly one row, **S035**, before commit:
   - kind `spec`, tier `A`, status `mined`, opened `2026-10-21`, recheck `on-release` (or `365d`).
   - Use only the dated URL `https://www.w3.org/TR/2024/REC-WCAG22-20241212/` (one URL+scope, so no new W04/E04).
   - Anchor: "Success criteria 1.1.1–4.1.3 A/AA and §5.2; html sha256 6e3c5fe3…7057".
   - `used-by` must list only paths that exist at validation time: `corpus/knowledge/accessibility-review-packet.md`, `corpus/knowledge/accessibility-review-cards.json`, `corpus/lessons/round-25.md`. Otherwise the row fails with E11.
   - Add a round-25 search-log line (identified, screened, included S035, excluded 0) and leave lines 85-87 as unopened leads.
7. **SKILL registry:** add an `accessibility-packet` row:
   - Verdict map: `0=clean` packet structure; `1=failed`; `2=could-not-evaluate` input; `64=could-not-evaluate` usage, with one JSON object on stdout.
   - Self-test: `--selftest` (tempfile only).
   - Frozen proof: `population.json` and `source-wcag22.html` sha256.
   - Write scope: none on the ordinary path. Owner: kake.
8. **Legacy separation:** packet and lesson wording may only say that r24 C1/C2 remain unadmitted separate debt (draft entry lines 102-105 already do). They must not describe, count or retry those probes.

## Proposed move (one)

**Strip the editorial `New ` change marker from the six `normativeText` values before the first commit, and add one selftest case that rejects a quote carrying it.**

- Why it works:
  - The population is still untracked, and its own hash is pinned nowhere (grep for `8f31cf5e…` found nothing).
  - `sourceSha256` binds the HTML, not the JSON, so the source pin is unchanged.
  - No current card quote starts with `New` (E10), so all 55 cards stay accepted.
  - The knowledge entry's claim (E8) becomes true.
  - No HTML change marker can become "normative grounding".
- Axes: operability improves (one false-accept path closed, and the tool, counter and selftest need no special case). Freshness improves (the population and the knowledge entry stop contradicting each other, and the S035 row closes the dangling contract cite in E5). Neither axis is harmed: the expected count stays 55 and the cards are unchanged.
- Fallback if the population is treated as frozen: the tool and the counter both drop a leading `New ` token from eligible text for exactly ids whose source block has `<p class="change">New</p>`. Then edit lines 21-23 of the knowledge entry to name the exclusion.

## Risks

- If the population is regenerated by a script, the fix must go into that extractor, not a hand edit, or a re-extraction reintroduces it.
- Changing tag-boundary spacing (E9) now would break all 29 affected card quotes. Keep the spacing and document "copy from population".
- If `corpus/lessons/round-25.md` is not written before census validation, S035's `used-by` raises E11.

## Verification (main, after all seats land)

- Test (a): run `python3 -c` over `population.json`. No `normativeText` starts with `New `, and there are still 55 ids (31 A / 24 AA).
- Test (b): run `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`. Exit 0, no E-codes, and W04 only for S033.
- Test (c): run `python3 -B scripts/accessibility_packet.py --root . --json`. Verdict `clean`, accepted 55, `websiteConformance` `not-assessed`.
- Test (d): run `.ufo/waves/round-25/packet_selftest.py --root .`, including a change-marker quote case that returns exit 1 with the shared finding id.
- Test (e): run `node scripts/corpus-contract.mjs --json`. No new `missing_metadata` for `accessibility-review-packet.md`.
- Test (f): run `rg -n 'screen reader and browser pairing' corpus/knowledge/accessibility-review-cards.json`. No match, i.e. 4.1.3 has been reworded.
