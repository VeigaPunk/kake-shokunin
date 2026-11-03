# ScribeEntries — kake round 70, W1 (scribe)

Base revision for every read: `e5f6fd9e4c243d092160bc74e8bea24256087173`. Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Draft prose only: no repo file written except this report; no git/jj mutation; `shokuknow` read-only; no campaign tool run. Tools installed/updated: none. Scratch `/fast/scratch/hyaku/kake-r70/ScribeEntries/` created and removed (`rm -rf`, verified gone).

## Entry draft

Proposed file `corpus/knowledge/crux-bigquery-origin-membership.md` (provenance trio in lines 1–3, per contract C2(a)):

```
source: S438 — https://developer.chrome.com/docs/crux/bigquery — § CrUX on BigQuery → Materialized table schema → origin_summary (Last updated 2026-10-13 UTC) — retained body sha256 <sha256>
verified-at: 2026-11-03
recheck: 180d
ground: field performance (Core Web Vitals, CrUX eligibility) — the documented route that answers origin membership without a CrUX API key

# Where origin membership in the CrUX dataset is published

The lane's CrUX question — whether a named origin is in the Chrome UX Report dataset — is blocked by credentials, not by ignorance: the CrUX API needs a Google Cloud API key the lane does not hold (S039), and the campaign session's key-free probes were its own-work observations (staged S303/S304 rows and companions) that this lane neither holds as registry rows nor re-ran this round. The dataset's own documentation names a third route, and this entry records it.

The raw data behind CrUX is published on BigQuery, and the origin list is a first-class table:

> <quote-1>

The same paragraph continues: the table is updated monthly with the latest list of origins in the dataset and has a single column, `origin`. The release cadence is the second Tuesday of the following month, each release a new table under the `chrome-ux-report.all` dataset, alongside monthly summary tables that carry the metrics per origin, per device and per country. The cost is the part that matters for the lane: the dataset is free to explore within BigQuery's free tier, and the prerequisite is a Google Cloud account with SQL — not a CrUX API key.

> <quote-2>

That is the concrete difference between the blocked route and the open one. The CrUX API route needs an API key (the lane's S039 records the key requirement and the quota); the BigQuery route needs a Google Cloud project. Neither is a credential the lane holds, and secrets are `kagi`'s custody — but the BigQuery route is the one that can answer the question for a specific origin without the API's per-key identity, and it names the table to query.

Scope note: this entry records where the answer lives. No BigQuery query was run, no project was used, and no field data was read for any origin, the lane's own included.

Cross-reference: the held r28 entry `corpus/knowledge/field-performance-cwv.md` carries the thresholds, the eligibility rules and the API's key requirement; what this entry adds over it is the one place where membership in the dataset can be read without a key — the documented `origin_summary` table.
```

Exact quote strings for the placeholders (class derived, method stated — Finding 2):
- `<quote-1>` = "The origin_summary table contains a list of all origins in the CrUX dataset" — 13 units; class **collapsed-only**; § Materialized table schema → `origin_summary` (h3 id `schema-origin-summary`); retained body `.ufo/waves/round-70/w1/ScoutSources/sources/S438-crux-bigquery.html`, sha256 `<sha256>`, 110,697 bytes.
- `<quote-2>` = "Using BigQuery requires a Google Cloud account and basic knowledge of SQL" — 12 units; class **collapsed-only**; § Access the dataset (h2 id `access_the_dataset`); same retained body.

## Gate draft

Proposed `## Gate` block for `corpus/lessons/round-70.md` (bulleted admit/reject, house style of rounds 65–69):

```
- **Admit — the BigQuery origin-membership entry** (`corpus/knowledge/crux-bigquery-origin-membership.md`; registry id S438, renumbered from staged S352). PROVINCE scope: field performance / CrUX eligibility is this lane's Frontier ground (`PROVINCE.md`, Frontier, first entry `corpus/knowledge/field-performance-cwv.md`); this entry adds a publisher-side knowledge row and claims no gate, no measured property and no capability row, so the area stays in Frontier. QUALITY bar: the cited id resolves in this lane's own `corpus/SOURCES.md` at the measured revision (round-53 held-ground criterion); the locator names the section that carries the quote, § CrUX on BigQuery → Materialized table schema → origin_summary (round-53 locator criterion — the staged anchor "Data structures" does not occur in the retained body, so the anchor is corrected); every quoted span is at most 25 units (round-55 bar) and its match class is derived from the two retained blobs and stated with the method (round-50 quote-class criterion), not asserted. Normalized row: `status` mined, `opened` 2026-11-03, `recheck` cell `180d`, `used-by` corpus/knowledge/crux-bigquery-origin-membership.md, 13 awk fields, no literal or escaped pipe in any cell. Stripped recheck prose, recorded verbatim from the staged S352 row with the cadence prefix stripped: `curl -fsSL 'https://developer.chrome.com/docs/crux/bigquery' \| grep -F -c 'The origin_summary table contains a list of all origins in the CrUX dataset'` -> 1 (ran 2026-10-24) — the staged cell's `\|` is that cell's markdown escape of the pipe; the command as run uses a bare pipe. This round's re-derivation on the retained body: the same literal grep against the raw HTML prints 0 (exit 1) and prints 1 against the whitespace-collapsed flat text (recipe `.ufo/waves/round-63/quote-class/extract_text.py` at e5f6fd9e, flat sha256 8cc3fa21…9cff), so the mandated quote's class is collapsed-only and the recorded "1" is a collapsed-text count, not a raw-substring count.
- **Reject — `crux-keyless-check.md`** (staged S303 + S304). Reason: its probe rows are campaign-session own-work observations — the CrUX Vis page fetch and the unregistered-caller POST — that are not lane-held registry rows (neither S303 nor S304 is in this lane's `corpus/SOURCES.md` at the measured revision) and that would have to be re-run as fresh probes this round before anything in them could be admitted; and its Vis/eligibility surface overlaps the entry this lane already holds from r28, `corpus/knowledge/field-performance-cwv.md` (S036–S039). Flip: a round that re-runs both probes fresh and shows a publisher-side keyless surface that is not already held can adopt it.
```

## QUALITY draft

Proposed append to `corpus/QUALITY.md` (round-69 addendum shape: Grounding line, one bulleted criterion, closing line):

```
## Round-70 addendum — scorecard pointer calibration

Grounding: `corpus/lessons/round-70.md` §Mistakes M1; the round-70 C1 counter `.ufo/waves/round-70/c70_pointer_audit.py` and the `## Pointer calibration (round 70)` section of `SCORECARD.md`.

- **A SCORECARD evidence pointer either resolves at the measured revision or carries a dated calibration annotation.** Admit: every path-like pointer in `SCORECARD.md` resolves at the measured revision — a repo-relative pointer exists at that revision (`git cat-file -e <rev>:<path>`), a `~/…` or `/tmp/…` pointer exists as host state — or is the exact first cell of a row in `SCORECARD.md` §Pointer calibration (round 70) whose row names the dated absence event class and marks the record historical, not executable. Reject: a pointer that resolves only in the worktree but not at the measured revision; a dangling pointer with no annotation row, or one whose annotation row names a different token; an annotation row inside an HTML comment; a pointer count taken from a population other than the counter's own token set. Able-to-fail: `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --selftest --work <dir>` prints `selftest 5/5`, and the base run `--root <lane> --revision e5f6fd9e4c243d092160bc74e8bea24256087173` exits 1 (measured: `pointers=348 dangling=19 annotated=0 unannotated=19 met=false`).

Criteria are not rewritten: this addendum is the round-70 row, and earlier criteria stand unchanged.
```

## Findings (for the L1 / critic)

1. **Contract §10 collision premise is false at base.** The lane registry (175 rows in `git show e5f6fd9e:corpus/SOURCES.md`) carries no `S352`: my 0–3-leading-space extractor found it zero times, and the eight staged ids that do collide are `S312 S329 S367 S372 S373 S374 S390 S409`. The adopted id `S438` is still right (first unused id above the lane max `S437`, absent from lane registry and staged file), but the contract's stated reason for renumbering does not hold. ExecMirror measured the same.
2. **Quote class is collapsed-only, not raw-substring.** The mandated quote is present in the retained body only after whitespace collapse: raw `grep -F -c` → 0 (exit 1); the lane's own recipe `.ufo/waves/round-63/quote-class/extract_text.py` (at e5f6fd9e) renders the body to 10,137 bytes, sha256 `8cc3fa21…9cff`, where the quote appears once. The staged recheck's recorded `-> 1 (ran 2026-10-24)` reproduces only as a collapsed-text count. **Conflict for the L1 gate:** QUALITY round-55 keeps raw-substring discipline absolute for brand-new entries and round-63 confines collapsed-only to correction instruments, while contract C2(c) accepts "raw-substring or collapsed-only, stated with the method". A raw-substring alternative exists in the same body ("a list of all origins included in the dataset", raw `grep -F -c` → 1) but is a different sentence from the mandated quote.
3. **Anchor correction.** The staged anchor "§ CrUX on BigQuery → Data structures → origin_summary" names a heading absent from the retained body; the quote sits under h2 "Materialized table schema" (id `schema-materialized`) → h3 `origin_summary` (id `schema-origin-summary`). The body also prints "Last updated 2026-10-13 UTC" (2 raw occurrences), contradicting the staged entry's "no version printed" note, so the anchor can be pinned by the doc revision date.
4. **`/tmp` population differs from the contract's count.** The contract says 12 tokens across move-log rows 10–18; `git show e5f6fd9e:SCORECARD.md` carries 9 distinct `/tmp/kake-rNN` tokens (11 occurrences), of which 8 dangle — `/tmp/kake-r16` exists on this host.
5. **C1 counter state.** `.ufo/waves/round-70/c70_pointer_audit.py` does not exist at base; ExecC1Counter's patch creates it. Exercising that seat's delivered copy: `--selftest --work <dir>` printed `selftest 5/5` (exit 0); the base run printed `pointers=348 dangling=19 annotated=0 unannotated=19 met=false` (exit 1) — 8 `/tmp` tokens, 3 home tokens (`~/Projects/plazir-15-site`, `~/DIRMAP.md`, `~/projects`), 8 repo tokens. Base is red, so the do-nothing control holds.
6. **Not exercised by this seat:** the sources census (`scripts/sources-census.sh validate`) on the S438 mirror — ExecMirror measured exit 0 with the 16 pre-existing W04 warnings; I did not re-run it.

## Surfaces and artifacts

Touched: `.ufo/waves/round-70/w1/ScribeEntries.md` (this report) only. Read: contract, staged entry and staged rows (shokuknow, read-only), base lane bytes, ScoutSources' retained body, ExecMirror and ExecC1Counter artifacts. Out of scope for this seat — L1 integration: the entry file, the `corpus/SOURCES.md` row, `corpus/lessons/round-70.md`, `corpus/QUALITY.md`.
