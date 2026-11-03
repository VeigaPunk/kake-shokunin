# CriticAdoption — round 70, W1 — adversarial pre-data critique of C2

Read-only critic, leaf member, no tools installed or updated (git 2.51, python3, coreutils only).
Base for every byte below: e5f6fd9e4c243d092160bc74e8bea24256087173. Scratch
/fast/scratch/hyaku/kake-r70/CriticAdoption deleted on exit.

## 1. Overlap attack — held entry vs staged BigQuery entry

Held entry `corpus/knowledge/field-performance-cwv.md` (S036–S039), exact sentences about CrUX and
eligibility: "The public field source, the Chrome UX Report (CrUX), only holds a page or origin
that is publicly discoverable and sufficiently popular among eligible Chrome users"; S038 block:
"A page must be publicly discoverable", "A page or origin must also be sufficiently popular; the
minimum visitor count is not disclosed"; S039 block: "Use requires a Google Cloud API key; the
quota is 150 queries per minute per project, free, and cannot be raised by payment"; and "CrUX API
calls need a Google Cloud API key (S039). kake holds no key; by lane policy it makes no API call
without an operator-provisioned one."

Checks: `grep -c 'bigquery'` on base `corpus/SOURCES.md` → 0 hits; `grep -iE 'crux/vis|cruxvis'`
→ 0 hits; the held entry never names BigQuery, `origin_summary`, a monthly origin table, or
BigQuery free-tier cost. Staged entry (shokuknow `lanes/kake/round7/KNOWLEDGE-PROPOSED.md`,
S352→S438, fetched 2026-10-24): "the dataset is queryable on BigQuery, the monthly origin list is
published as a table that is refreshed every month, and the dataset is free to explore within
BigQuery's free tier — so eligibility can be answered with a project rather than an API key".

**Verdict: new ground.** The held entry documents *why* origins drop out (eligibility criteria)
and the *keyed* API route; the staged entry adds the *key-free* membership route (BigQuery
`origin_summary`). Nothing held is deepened — there is no prior BigQuery statement. Complementary
to S038/S039, not a duplicate; duplicate-adoption attack fails.

## 2. Quote attack — retained S438 bytes (receipt still pending; only the .html exists in
ScoutSources/sources/, no receipt file yet — quote attack ran on the 110697-byte file present,
sha256 dd17ea8cb30ec89af9eb6cbb16fcb0de3d04eb33143a3aa8ac19c9da6d5db420)

Method: python3 — remove script/style, strip tags→space, html.unescape, collapse whitespace;
search raw, tag-stripped, and raw-collapsed. Canonical link and og:url both =
https://developer.chrome.com/docs/crux/bigquery (the required URL); title "CrUX on BigQuery |
Chrome UX Report | Chrome for Developers".

- Q1 "The origin_summary table contains a list of all origins in the CrUX dataset": raw=absent
  (inline tags split it), collapsed-only present exactly once → **class collapsed-only**. Predicate
  (c) admits collapsed-only only *with the method stated*; a receipt claiming raw-substring is
  false.
- Monthly refresh: the page's actual wording is "it is updated monthly with the latest list of
  origins in the dataset" — present as a **raw substring**. The staged entry paraphrases "refreshed
  monthly"; a quote of "refreshed monthly" attributed to the page would misquote. Page wording only.
- Free tier: "The CrUX dataset on BigQuery is free to access and explore up to the limits of the
  free tier, which is renewed monthly and provided by BigQuery." — collapsed-only (a link tag
  splits it; stripped text shows "free tier , which", so match whitespace-insensitively).
- Chrome-vs-body: free-tier sentence at raw offset 78621 vs article 74148 / h1 76380 → article
  body ("Access the dataset" section). origin_summary sentence sits in the "Data structures"
  schema table → body. Neither is nav/cookie/footer chrome. Extra claims the adoption carries
  ("second Tuesday" release cadence, `chrome-ux-report.all`, single `origin` column) are all
  present in the retained bytes. Quote truth holds.

## 3. Reject-reason attack — crux-keyless-check.md

The reject is **sound, with one overclaimed half**. Load-bearing half: its probe rows (S303 CrUX
Vis page + S304 own-work 403 PERMISSION_DENIED, 2026-10-23) are campaign own-work; CORPUS.md rule 1
forces this lane to re-run them, and a keyless POST to queryRecord violates the held entry's own
policy sentence quoted in §1. Not a dodge: no credit is taken, and the flip condition (re-run both
probes fresh) is named — though note it carries a latent conflict: a flip needs an
operator-provisioned key (which moots the keyless premise) or an explicit policy amendment for
unauthenticated probes. Overclaimed half: "Vis/eligibility surface overlaps the r28 held entry
(S036–S039)" — kake's registry holds no Vis source (0 hits); the overlap is thematic only. The
honest line between admit and reject is evidence re-groundability: the BigQuery entry is 100%
publisher-side (one docs GET re-grounds it fully); the keyless-check entry's core includes an
own-work probe this lane cannot re-ground within policy. That distinction is taste, not laziness.

## 4. Predicate attack — cheapest fake satisfying (a)–(d) without a real re-grounding

**The fake:** `cp` the staged campaign's copy
(shokuknow `lanes/kake/round7/.evidence/crux_bigquery_r7.html`, 110643 bytes, sha256
2c43abe9b88fc951ec8a500d0e07a186c8bb1f98c5330be184c28bff810c28d1) into ScoutSources/sources/,
hand-write the (a) header and the (b) row. Verified: all three quotes are present in that staged
copy (Q1 collapsed-only, Q2 raw, Q3 collapsed-only), so (c) passes; (d) is format validation only.
**No clause of (a)–(d) catches it** — (c) binds quote-presence in the retained file only; nothing
requires the receipt's sha256 to equal the retained file's sha256, the receipt's access date to be
2026-11-03, or the retained bytes' canonical URL to equal the entry's source URL. A cheaper fake
still passes: any HTML blob containing the sentences, no URL binding at all. (a)'s `verified-at:`
is a self-asserted string; nothing re-verifies entry content truth — that duty currently falls on
critic/reviewer seats (this report exercises it).

**Smallest safe correction** (contract frozen; recorded for the reviewer to check, not an edit):
extend (c)'s check with three one-liners — receipt sha256 == sha256(retained file); receipt access
date == 2026-11-03; retained bytes carry canonical/og:url == the entry's source URL.

**Bonus identity finding:** the contract's collision premise is false at base. `grep -c 'S352'` on
base `corpus/SOURCES.md` → **0** (also 0 for all of S350–S359); 175 distinct `| S### |` rows, max
id S437, S438 unused (0 hits) — registry 175 → 176 holds. Per the contract's own rule (decide by
committed reg-ids/staged-ids/collisions outputs, never arithmetic) the adoption must paste the
extractor outputs; an empty collision set means the "renumber map" is empty — pasting any
non-empty renumber map would be fabricated provenance.

## Exercised verification log

- `git show e5f6fd9e:corpus/knowledge/field-performance-cwv.md` — full text read.
- `git show e5f6fd9e:corpus/SOURCES.md` + grep — S036–S039 rows quoted; S352 count 0; S438 count
  0; 175 rows; max S437; 'bigquery' 0; 'crux/vis|cruxvis' 0.
- python3 quote analysis on the retained S438 file and on the staged campaign copy (exact outputs
  in §2 and §4 above); canonical/og:url extracted from both.
- Stat/sha256: retained 110697 B dd17ea8c…; staged copy 110643 B 2c43abe9… — different bytes, so
  the *current* retained file is not the staged copy (fresh-GET evidence), though no predicate
  would have caught reuse.
