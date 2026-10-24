# CrawlScope → offline static canonical preflight

Seat: connector, read-only. Axis judged: **operability**. Milestone: `offline-canonical-capability`. Base observed: `7c61c8cc791bde36dd5e3688bdfea2678d90146c`. No tool installed. Pacman transactions not attempted.

This seat does not admit, integrate, or claim `scripts/canonical_audit.py` passes. That file is absent in the lane (no match under `scripts/`).

## Axes

| Axis | Relation to this move |
|---|---|
| operability | The only axis this move is allowed to improve: C1 stays a runnable local classifier whose clean exit means the frozen explicit-head policy, not host crawl hygiene. |
| freshness | Must stay put. Armed check A4 (`sitemapStatus` 404 and the plazir live/source sitemap pins) is a different instrument. |
| frontier coverage of crawl hygiene | Must stay open. Host-root `robots.txt` contents are still named debt. JS-rendered canonicals stay open. |
| quality (population unit, missing substrate) | Held only if the two denominators below stay named and are not added into one accepted count. |

## Evidence

**C1 contract** (`.ufo/waves/round-22/contract.json`). Before: no lane-owned canonical-policy validator; 0 accepted cases in a frozen 32-case matrix. After: a read-only local validator classifies every matrix case. Limits: explicit-head serialized static HTML only; policy comparison, not search-engine selection, JS rendering, HTTP headers, redirects, network freshness, or publishing readiness. File resolution: paths relative to the manifest directory, regular files only, reject symlinks and traversal, no network or writes in normal mode. Finding ids are the ten listed ids. Exit map is 0/1/2/64.

**Province container vs file contents.** `PROVINCE.md:22-23` puts robots.txt, sitemap scope, and canonical signals in one frontier bullet and names `corpus/knowledge/crawl-scope-per-host.md` as the first entry, then says canonical/JS rendering is open. A search of that knowledge file for `canonical` returns no matches. Its claim (`crawl-scope-per-host.md:6-18`) is only: robots rules are discovered at the service root `/robots.txt`; the project sites under `veigapunk.github.io/<repo>/` share that one host policy; sitemaps are limited by file location and, for Google unless Search Console is used, by parent directory. Sources on the entry are S011, S012, S013.

**Two populations already measured, with different units.**

1. Crawl-scope host population. The entry's recheck (`crawl-scope-per-host.md:37-41`) counts unique `veigapunk.github.io/<repo>/` tokens in `SKILL.md` and `corpus/knowledge/fleet-registry.md`. The property rows that match that pattern are `plazir-15-site`, `charter-ufo-fsd`, and `lucario` (`SKILL.md:17`, `:18`, `:26`). The admitted outside review states the consequence: the three project sites cannot carry their own `robots.txt` (`corpus/lessons/round-20-verifier-spotcheck.md:12`).
2. C1 static-file population. `contract.json` `matrixCases` length 32. `corpus/QUALITY.md:85-88` already says a canonical preflight proves the declared signal against explicit publisher policy over that named static-file population, and never proves Google's selected canonical, content duplication, live delivery, or JavaScript state.

**Named debt left visible.** `crawl-scope-per-host.md:44-46`: current status of `https://veigapunk.github.io/robots.txt`, and whether it lists project sitemaps, remains unknown. No lane property was probed. `corpus/README.md:40` describes the entry as robots-at-host-root plus sitemap scope. `corpus/README.md:101-102` still lists canonical signals and JS-rendered canonicals as open ground.

**Source path does not authorize `rel=canonical`.** `corpus/SOURCES.md:33` sequences crawl hygiene as S010 → S009 → S011 → S012 → S013 (HTTP validators, nginx ETag format, RFC 9309, sitemaps.org, Google sitemap location). The registry rows present in this tree stop at S019. RFC 6596 is not on that path and is not a registry row. Stretching S011–S013 into the HTML canonical policy would cite the wrong mechanism.

**Exit-map pattern already in the lane, with the offline caveat.** `SKILL.md:212` and `corpus/knowledge/freshness-sweep.md:26-31`: `0` clean, `1` failed/drift, `2` could-not-evaluate input, `64` usage. Offline, skipped, and suspended sections are never proof of a complete publishing check. C1's `exitMap` matches those four codes. Freshness A4 (`freshness-sweep.md:62-63`) is the live sitemap/robots watch and is not an HTML-head check.

**Word collision, not one mechanism.** Elsewhere in the lane, "canonical" also means the writer repo (`corpus/README.md` origin-repos row), the sitemap of the canonical host (kimi subpath row), a filesystem path inside `freshness-sweep.mjs`, and the charter property note that kimi variants point `rel=canonical` at the charter GHP front (`SKILL.md:18`). None of those is the C1 manifest comparison.

## Contradiction (do not collapse)

The province bullet reads as one surface. The cited file filled only the host-root robots and sitemap-location half, and it never states an HTML `rel=canonical` rule. C1 is the other half: one explicit-head link resolved against `expectedCanonical` on a manifest-listed regular file. A clean 32/32 does not observe `https://veigapunk.github.io/robots.txt`. A future live robots read would not classify the 32 HTML cases. Adding those counts produces a number that matches neither contract.

The r20 admit (project sites cannot carry their own robots file) and C1's per-file resolution are compatible only while the validator does not look for a project-local robots or sitemap. Reading `robots.txt` beside `lucario/a.html` revives the per-project policy model that admit rejected. Fetching the host-root robots file leaves the offline contract.

## Pattern to reuse

Reuse the crawl-scope entry's claim anatomy, not its robots or sitemap rules:

1. Name the population unit in the claim sentence (here: manifest pages in the frozen 32, not the 3 project sites).
2. Keep a local recheck that does not fetch (case-name list length versus `matrixCases`).
3. Leave the live substrate as named debt (host-root robots contents; Google selection; JS-rendered canonicals).
4. Keep the shape-only clearance already written at `crawl-scope-per-host.md:48-54`: replayable argv, missing substrate visible, no live response collected.

Reuse the existing 0/1/2/64 gate shape from freshness-sweep / corpus-contract, including the sentence that an offline clean is not a complete publishing check (`SKILL.md:212`).

## Boundary not to absorb

Do not absorb into `canonical_audit.py` or into C1's accepted/32:

- RFC 9309 host-root discovery, the sitemaps.org location rule, or Google's parent-directory sitemap rule (S011–S013).
- Freshness A4's live sitemap/robots status, or any narration that a static clean exit clears that pin.
- Sitemap `<loc>` membership as a substitute for an explicit-head canonical link.
- A project-directory `robots.txt` as a veto or an allow on a matching `expectedCanonical`.
- JS-rendered canonicals, HTTP `Link` headers, redirects, and publishing readiness (contract limits; `QUALITY.md:85-88`).
- `tabi`'s client-side crawler discipline (`PROVINCE.md:30-31`). This stays a publisher-side declaration check.
- Edits to `crawl-scope-per-host.md` or other historical knowledge bytes. The contract debt line forbids that.

## Proposed move

Denominator firewall, one change of integration policy and no new matrix case.

Measure C1 only as accepted cases over the frozen `matrixCases` list (32). Do not add robots, sitemap, or host-population cases to that list. Do not mark the `PROVINCE.md:22-23` bullet closed when the matrix goes green. Do not retarget A4. Do not edit `crawl-scope-per-host.md` in this round. Keep the out-of-matrix falsifier below as a later check, outside `measure.py`'s `total`.

Operability improves because a clean exit stays interpretable: the declared head link matched explicit local policy on the named static files. Freshness, the robots debt, and the JS-canonical gap are not moved.

## Future falsifier

Name: `crawl_files_do_not_satisfy_or_veto_canonical`.

Run only after a candidate `scripts/canonical_audit.py` exists. Do not add this name to `matrixCases`. Do not commit the temp trees. Do not fetch any URL. Use mode `0644` siblings so a directory listing that does not parse them can still pass; this recipe is about verdict identity, not about unreadable-file handling.

Shared clean page `a.html`:

```html
<!DOCTYPE html><html><head><link rel="canonical" href="https://veigapunk.github.io/lucario/a.html"></head><body></body></html>
```

Page with an explicit head and no canonical link, `missing.html`:

```html
<!DOCTYPE html><html><head><title>x</title></head><body></body></html>
```

Manifest for dirs A and B (`version` 1, one page): `url` and `expectedCanonical` are both `https://veigapunk.github.io/lucario/a.html`, `file` is `a.html`.

- Dir A: that manifest and `a.html` only.
- Dir B: dir A plus `robots.txt` containing `User-agent: *` and `Disallow: /lucario/`, plus a sitemap whose only `<loc>` is `https://veigapunk.github.io/other/b.html`.
- Dir C: manifest page `file` `missing.html` with the same `url` and `expectedCanonical`, plus a sitemap whose only `<loc>` is `https://veigapunk.github.io/lucario/a.html`, plus `robots.txt` `Allow: /`.

Command, once per directory: `python3 scripts/canonical_audit.py --manifest <absolute-manifest> --json`.

Pass predicate:

- A and B both exit 0, `pagesChecked` is 1, `findings` is empty, and the two JSON objects are equal.
- C exits 1, `pagesChecked` is 1, and the findings contain id `canonical_missing` and no id outside the contract's ten.

Fail, absorption: A and B differ, either exits non-zero, or any finding mentions robots or sitemap. Fail, false green: C exits 0 or returns an empty findings array. The lucario URL is fixture text inside the crawl-scope host population. It is not a live observation and must not be written back into the knowledge entry.

Today the script is absent, so this predicate is not executable. Absence stays the contract's before-state (accepted 0 because unavailable). Do not score a missing tool as a policy failure of this falsifier.

## Risks

- Folding the falsifier into the 32 changes the frozen denominator and breaks the measure counter's `total` of 32.
- A walker that opens every sibling and treats a non-HTML file as `html_unsupported` fails dir B with exit 2. That is scope creep into could-not-evaluate, distinct from a policy finding, and still fails the equality predicate.
- Coupling this exit 0 to freshness A4 would hide the pinned live sitemap/robots watch behind a static HTML result.
- RFC 6596 permits a target on another host. Dir B's `Disallow` must not become a local reason to reject a matching `expectedCanonical`. This recipe locks that; the matrix case `wrong_host` remains a separate `expectedCanonical` mismatch and is not this check.
- Parser-scope decoys (comment, script, template) belong to other seats. This recipe uses one explicit head link so it does not silently redefine those cases.

## Verification for L1

Not run here (read-only seat; no mid-flight test of the missing validator).

1. At base `7c61c8cc`, confirm `scripts/canonical_audit.py` is absent and `measure` reports accepted 0 / total 32 unavailable, without running this falsifier as if it were a matrix case.
2. After the candidate script exists, run dirs A, B, and C as specified. Require the pass predicate.
3. Confirm `matrixCases` is still exactly the 32 contract names and this falsifier is not among them.
4. Confirm `corpus/knowledge/crawl-scope-per-host.md` is byte-unchanged and still names the unknown `https://veigapunk.github.io/robots.txt` debt. Do not request that URL.
5. Confirm the province frontier bullet is not marked closed by the matrix result.

## Report

`.ufo/waves/round-22/w1/CrawlScope.md`
