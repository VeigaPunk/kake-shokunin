# ExecReuseTrial — kake round-91 w1 — the reuse-decision instrument on real recorded data

VERDICT: the shipped instrument decides all 18 convertible recorded surfaces offline — 4 not-storable (`no-store`), 4 heuristic-undecided (cacheable 404s with no lifetime header), 10 `reuse` at capture time flipping to `revalidate` at +30 d — the tool agrees with the frozen counter's own `reference()` on 36/36 decision points, and the frozen counter scores the shipped tool `met=true` at seeds 1, 2 and 3. This is an offline decision over recorded bytes only; it says nothing about any live surface's current behaviour.

All paths below are relative to the lane root. LANE was never mutated: no commit, no staging, no working-tree change outside my own wave directory.

## 0. What was measured (digests and revisions)

| Subject | Value |
|---|---|
| Tool under test | `scripts/stored_reuse.py`, sha256 `5004657dbf2ae43399631f79e5d5955a8aa698b53f6127e22e2cc654ba9ad299` (433 lines, working tree; authored by a sibling seat, not yet committed when measured) |
| Lane HEAD at measurement | `f4fff130a52ae6de49af5de7d568d2ee320ebfb0` — `git cat-file -e HEAD:scripts/stored_reuse.py` → absent at HEAD |
| Fixture revision for counter runs | `96465827bba40d3cf5e26a525884f39700f93f86` — scratch clone of LANE at HEAD, detached, plus the tool snapshot committed with identity `kake-r91 ExecReuseTrial fixture <fixture@invalid>`; `git rev-parse --show-toplevel` asserted equal to the clone dir before committing; exists only in the deleted scratch clone |
| Frozen instruments re-verified | `c91_reuse.py` `0cd610426896fc76b4913c907d83b95d22c7a66c4ecf2da8fc4fc9ecf21ab660`, `c2-contract.md` `faa91e096f4f9ae062d14402bbad5615c9ace8cfb2e820c519cb5cd01d768fe4`, `c91_defects.py` `5239c7f808095e5e146bc57f72bdaa00ce2cab20fdd7cc1b0b2d201ddec5629b`, `frozen/c2-population.sha256` `033b6103303d33690c4a6d02b04df36ba86b3b4f1d1e18aa5e267cb9b95084c8` — all four equal the values named in `.ufo/waves/round-91/freeze.md`; the pins digest also equals the counter's own `PINS_SHA` constant |
| Counter selftest | `python3 -B .ufo/waves/round-91/c91_reuse.py --selftest` → `selftest 45/45 hand cases, 120 generated, 7 decisions`, exit 0 |
| Racing-edit check | tool sha256 taken before and after all runs: identical (`5004657d…`), and equal to the fixture copy — no sibling edit raced the measurement |

Timing note (honest): `scripts/stored_reuse.py` did not exist when this seat started. I polled at a 45 s interval inside a 20-minute budget; the tool appeared during that window (file mtime 2026-11-04 20:27 local). No installs or upgrades were needed; nothing was installed (tooling-authorization record: none).

## 1. Recorded captures that exist (item 1)

| Tree | Contents | Convertible? |
|---|---|---|
| `.ufo/waves/round-23/live/` (named by my item: "GET snapshots with receipts") | 12 surfaces, each with `fetch.json` (status, contentType, sha256, byte count, `fetchedAt`, finalUrl, redirects) plus `audit.json`; five surfaces also carry `manifest.json` and `page.html`. Surfaces: burnerchrome-kimi, charter-ghp, charter-kimi, ds4cc-kimi, ds4cc-primary, lucario-ghp, lucario-kimi, plazir15-ghp, plazir15-kimi, plazir27-kimi, ufo-fsd-kimi-pro, vault-index-kimi | **No** — no record in this tree carries a header list (`fetch.json` has status/bytes/digest/timestamp only). Converting them would mean inventing headers; excluded |
| `.ufo/waves/round-61/capture/` (the tree `corpus/knowledge/response-header-expectations.md` names, via the `response_snapshot.py` flow) | 12 surfaces, each `response.json` (status, fetchedAt, wire-order name/value header pairs with duplicates preserved, body sha256) + `body.bin`; `capture/manifest.json` binds 12 checks | **Yes** — 12 records converted |
| `.ufo/waves/round-81/capture/`, `.ufo/waves/round-82/capture/` | 3 surfaces each (ds4cc-primary, ds4cc-robots, ds4cc-sitemap), same `response.json` shape; these are the r83 header-change ground's inputs named in `PROVINCE.md`, not in the knowledge entry; included as supplementary dated captures | **Yes** — 6 records converted |

Convertible total: **18 records** (requirement: ≥ 8). Two dated snapshots of the same three ds4cc.com URLs exist (r81 `fetchedAt` 2026-11-04T12:05:06Z, r82 2026-11-04T13:00:27–28Z); both are kept as distinct recorded bytes.

## 2. Adapter convention (declared, as implemented in `convert_recorded.py`)

- **Field mapping** (matched ASCII-case-insensitively on recorded names): recorded `date` → contract `Date`; recorded `expires` → `Expires`; recorded `age` → `Age`; recorded `cache-control` → `Cache-Control`; recorded `vary` → `Vary`. All five values pass through verbatim **except** the two HTTP-date fields.
- **HTTP-date → integer epoch**: `email.utils.parsedate_to_datetime`, naive results assumed UTC, truncated to seconds. This is the only timestamp conversion; per the contract the lane records epoch integers, not parsed HTTP-dates.
- **Every other recorded field line is dropped** (the contract has no clause for it): `last-modified`, `etag`, `server`, security and CDN fields never reach the decision.
- **Header map fidelity**: names kept exactly as recorded. A name repeated with the *same* spelling folds first-wins (a JSON object cannot hold two equal keys) and the dropped value is recorded verbatim in `inputs/index.json`. Seven r61 kimi.page records carry `vary` twice (`Accept-Encoding` kept, `Origin` dropped) — decision-neutral here because neither value contains `*`. A scan of all 18 records found **no case-variant duplicate spellings** of any header, so the contract's clause-1 refusal is never silently dodged by the fold.
- **Request side**: `{"method": "GET", "headers": {}}` — the recorded method, and the captures recorded no request headers.
- **`shared`: `false`** (the contract default) — a recorded capture does not disclose the cache mode it was observed from.
- **`now`**: two declared offline passes per record. Primary `now` = epoch of the record's own `fetchedAt` (the moment the snapshot was taken). Aged pass = primary + 2 592 000 s (30 days), to exercise the stale branches on real data without inventing headers.
- **No header is ever invented.** A record with no Cache-Control legitimately reaches the lifetime-null path; a record with no Date would legitimately be refused by the tool (none occurred — every convertible record carries `Date`).

Converted inputs: `w1/ExecReuseTrial/inputs/round-{61,81,82}/<surface>.json` (18 files) + `inputs/index.json` (per-input sha256, recorded vs converted fields, dropped-duplicate notes, both `now` values).

## 3. Per-surface decisions (item 3)

Tool invoked as `python3 -B scripts/stored_reuse.py < inputs/<row>.json` (stdin JSON, exactly the contract's input shape). "Rests on" = the converted headers that can change the decision (Date = epoch(fetchedAt) equals capture-time `now`, so it is implied in every row).

| Input (under `w1/ExecReuseTrial/inputs/`) | URL | st | Resting headers (converted) | Capture-time decision (lifetime / age) | Aged +30 d decision (lifetime / age) |
|---|---|---|---|---|---|
| round-61/burnerchrome-kimi.json | https://burnerchrome.kimi.page/ | 200 | Cache-Control `no-store`; Vary `Accept-Encoding` | **not-storable** (null / null) | not-storable (null / null) |
| round-61/charter-ghp.json | https://veigapunk.github.io/charter-ufo-fsd/ | 200 | Cache-Control `max-age=600`; Age `70`; Expires `Tue, 27 Oct 2026 09:24:45 GMT`; Vary `Accept-Encoding` | **reuse** (600 / 70) | revalidate (600 / 2592070) |
| round-61/charter-kimi.json | https://charter-ufo-fsd.kimi.page/ | 404 | Vary `Accept-Encoding`; no Cache-Control | **heuristic-undecided** (null / 0) | heuristic-undecided (null / 2591998) |
| round-61/ds4cc-kimi.json | https://ds4cc.kimi.page/ | 200 | Cache-Control `no-store`; Vary `Accept-Encoding` | **not-storable** (null / null) | not-storable (null / null) |
| round-61/ds4cc-primary.json | https://ds4cc.com/ | 200 | Cache-Control `max-age=600`; Age `73`; Expires as above; Vary `Accept-Encoding` | **reuse** (600 / 73) | revalidate (600 / 2592072) |
| round-61/lucario-ghp.json | https://veigapunk.github.io/lucario/ | 200 | Cache-Control `max-age=600`; Age `73`; Expires as above; Vary `Accept-Encoding` | **reuse** (600 / 73) | revalidate (600 / 2592072) |
| round-61/lucario-kimi.json | https://lucario.kimi.page/ | 404 | Vary `Accept-Encoding`; no Cache-Control | **heuristic-undecided** (null / 0) | heuristic-undecided (null / 2592000) |
| round-61/plazir15-ghp.json | https://veigapunk.github.io/plazir-15-site/ | 200 | Cache-Control `max-age=600`; Age `74`; Expires as above; Vary `Accept-Encoding` | **reuse** (600 / 74) | revalidate (600 / 2592074) |
| round-61/plazir15-kimi.json | https://plazir15.kimi.page/ | 404 | Vary `Accept-Encoding`; no Cache-Control | **heuristic-undecided** (null / 0) | heuristic-undecided (null / 2591998) |
| round-61/plazir27-kimi.json | https://plazir27.kimi.page/ | 404 | Vary `Accept-Encoding`; no Cache-Control | **heuristic-undecided** (null / 0) | heuristic-undecided (null / 2592000) |
| round-61/ufo-fsd-kimi-pro.json | https://ufo-fsd.kimi.pro/ | 200 | Cache-Control `no-store` (no Vary) | **not-storable** (null / null) | not-storable (null / null) |
| round-61/vault-index-kimi.json | https://veigapunk.kimi.page/ | 200 | Cache-Control `no-store`; Vary `Accept-Encoding` | **not-storable** (null / null) | not-storable (null / null) |
| round-81/ds4cc-primary.json | https://ds4cc.com/ | 200 | Cache-Control `max-age=600`; Age `0`; Expires `Wed, 04 Nov 2026 11:47:14 GMT`; Vary `Accept-Encoding` | **reuse** (600 / 0) | revalidate (600 / 2592000) |
| round-81/ds4cc-robots.json | https://ds4cc.com/robots.txt | 200 | Cache-Control `max-age=600`; Age `0`; Expires `Wed, 04 Nov 2026 12:15:06 GMT`; Vary `Accept-Encoding` | **reuse** (600 / 0) | revalidate (600 / 2592000) |
| round-81/ds4cc-sitemap.json | https://ds4cc.com/sitemap.xml | 200 | Cache-Control `max-age=600`; Age `0`; Expires as above; Vary `Accept-Encoding` | **reuse** (600 / 0) | revalidate (600 / 2592000) |
| round-82/ds4cc-primary.json | https://ds4cc.com/ | 200 | same as r81 primary | **reuse** (600 / 0) | revalidate (600 / 2591999) |
| round-82/ds4cc-robots.json | https://ds4cc.com/robots.txt | 200 | same as r81 robots | **reuse** (600 / 0) | revalidate (600 / 2592000) |
| round-82/ds4cc-sitemap.json | https://ds4cc.com/sitemap.xml | 200 | same as r81 sitemap | **reuse** (600 / 0) | revalidate (600 / 2592000) |

**Scope sentence, stated plainly:** every decision above is an offline computation over recorded bytes frozen at their `fetchedAt` moments (2026-10-27 and 2026-11-04). It is not a measurement of, and says nothing about, what any of these URLs serves today, how any live cache would actually behave, or whether any surface is currently fresh.

Machine-readable copies: `w1/ExecReuseTrial/results.json` (rc/stdout per row and pass) and `w1/ExecReuseTrial/inputs/index.json`.

## 4. Frozen counter, three seeds (item 4)

Command (per seed): `python3 -B .ufo/waves/round-91/c91_reuse.py --root <scratch-clone> --revision 96465827bba40d3cf5e26a525884f39700f93f86 --work <scratch>/work --seed <n>`, run from the scratch root; receipts at `w1/ExecReuseTrial/seed-{1,2,3}.out` (`.err` all 0 bytes):

```
C2v91 revision=96465827bba40d3cf5e26a525884f39700f93f86 candidate=present hand=45/45 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok seed=1 met=true   (exit 0)
C2v91 revision=96465827bba40d3cf5e26a525884f39700f93f86 candidate=present hand=45/45 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok seed=2 met=true   (exit 0)
C2v91 revision=96465827bba40d3cf5e26a525884f39700f93f86 candidate=present hand=45/45 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok seed=3 met=true   (exit 0)
```

Three distinct seeds re-decide the whole 120-case generated population with the counter's own reference each run; all three runs agree, all five frozen forgeries refused each time (`seed-1.out` line 2 detail: every forgery `admitted: false`, `anti_table_hits: []`, `errors: []`, `hand_failures: []`, `candidate_sha256` equal to the measured tool digest). The seeded population is stable and the shipped tool is not seed-lucky on this evidence.

## 5. Independent cross-check on the real data

`compare_rows.py` loads the frozen counter's `reference()` (module import of the unmodified frozen bytes) and re-decides all 18 inputs at both `now` values: **agree = 36, disagree = 0, reference-side refusals = 0** (`w1/ExecReuseTrial/compare.json`). The shipped tool and the counter's reference never split on this recorded corpus.

## 6. Findings, limits and defects

1. **No defect in the tool or in the frozen counter was exercised by this data.** All 36 tool decisions match the frozen reference; the counter is deterministic across seeds; no input needed a case the contract refuses.
2. **The recorded corpus exercises a thin slice of the decision vocabulary.** Across 18 recorded surfaces the only stored directives seen are `no-store` and `max-age=600`; the only statuses are 200 and 404. No recorded surface exercises `serve-stale`, `must-revalidate-fail`, `only-if-cached-miss`, `no-cache` (either side), request `max-age`/`min-fresh`/`max-stale`/`only-if-cached`, `s-maxage`, `shared`, or a non-`Accept-Encoding` Vary. Those branches are attested by the counter's synthetic population only — recorded data cannot witness them, and no claim here says otherwise.
3. **Expires is always dominated on this corpus**: every recorded `Expires` sits ≈ capture-time + 9 min while `max-age=600` is present, so contract clause 9's Expires branch is exercised only as dominated-out; no recorded surface derives a lifetime from Expires alone.
4. **Duplicate-`vary` fold is an adapter choice the contract does not cover** (two recorded field-lines with the same name cannot both live in one JSON header map). Both values are disclosed per row in `inputs/index.json`; the fold is decision-neutral on this corpus (no `*` among dropped values).
5. **`.ufo/waves/round-23/live/` cannot feed this contract** — its records carry no header lists at all. My item calls it "GET snapshots with receipts"; what exists is 12 status/digest/timestamp records plus audit verdicts. Listed, not converted, not embellished.
6. **r81/r82 are the same three URLs captured twice.** They are distinct recorded bytes (both kept), but they add URL diversity of zero.
7. The tool was sibling-authored and uncommitted at measurement time; my sha-pinned runs and the fixture-commit recipe above are what I measured. If the tool changes after mtime 2026-11-04 20:27, these receipts measure the `5004657d…` bytes only.

## Receipts (all under `w1/ExecReuseTrial/`)

`inputs/` (18 converted inputs + `index.json` with per-input sha256) · `results.json` · `compare.json` · `seed-1.out` `seed-2.out` `seed-3.out` (+ empty `.err` × 3) · `convert_recorded.py` `run_rows.py` `compare_rows.py` (the exact adapters/runners, readable above) · this report.

Scratch root `/fast/scratch/hyaku/kake-r91/ExecReuseTrial/` was deleted after the receipts were copied; nothing citable lives there. No tool was installed (none needed). No git/jj command mutated the lane; the single fixture commit lives only in the deleted scratch clone.
