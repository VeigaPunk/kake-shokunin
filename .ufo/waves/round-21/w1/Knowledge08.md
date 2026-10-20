# Knowledge08 — ghp-etag-anatomy.md provenance audit (round-21, w1)

## Decision

Target `corpus/knowledge/ghp-etag-anatomy.md` already opens with the provenance trio (lines 1-3). Per assignment, the target is **left unchanged**. No prefix was added.

- Prefix added: **0 lines / 0 bytes**.
- Existing trio: lines 1-3 = **348 bytes**; through the blank line 4 = **349 bytes**.
- Integrity: sha256 `0952ed19a5f4cc38b9c9b1c39e4dd8a8c4d40e21ac323ef89cdcd2eb7cdc6b28` (55 lines, 3304 bytes), identical to `.ufo/waves/round-21/frozen/before/corpus/knowledge/ghp-etag-anatomy.md`.

## Field truth audit

| Field | Value (verbatim, line) | Result |
|---|---|---|
| `source:` L1 | `S009, S010 (corpus/SOURCES.md) — https://raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c §ngx_http_set_etag` | **Valid.** S009 and S010 exist in `corpus/SOURCES.md` rows 17-18. S009 URL and anchors match row 17 (`ngx_http_set_etag` line 1682; sprintf 1708-1710; release-1.28.0). Body lines 22-23 agree. S010 `§8.8.1/§8.8.3` matches row 18. |
| `verified-at:` L2 | `2026-10-19 (nginx release-1.28.0; RFC 9110 published June 2022)` | **Date correct, wording non-compliant.** 2026-10-19 matches the S009/S010 "opened" column, not today (2026-10-20), so it is not presented as a domain recheck. The required token `historical-not-live-reverified` is absent. Body header says "reopened 2026-10-19" while SOURCES says "opened"; minor wording mismatch. |
| `recheck:` L3 | `on recorded ETag or source revision change — printf '%d\n' 0x1365d; date -u -d @$((0x6ab49127)) +%FT%TZ` | **Partial.** The command is concrete, local, and contains no credential or auth references. It is pure arithmetic and does not re-read the source. **Missing:** the operator restore-or-retire requirement for when the nginx source vanishes. |

### Arithmetic (hand-verified, not executed)
- `0x1365d` = 65536 + 13917 = **79453** ✓
- `0x6ab49127` = **1790218535** → 1790218535 − 1767225600 (2026-01-01T00:00:00Z) = 22992935 s = day 266 + 10535 s → **2026-09-24T02:55:35Z** ✓
- `0x6ab49126` = 1790218534 → **2026-09-24T02:55:34Z** ✓
- The "one second earlier" claim holds.

## Body evidence audit

- `LOG.md:161-163` — literals `79,453B` and `6ab49127-1365d` at lines 161-162. ✓ (also true at base `cb807bc`)
- `corpus/knowledge/publish-queue.md:255-261` — literals at 256-258, edge-flip rule 259-261. ✓ (true at base `cb807bc`, where literals sit at 256-258)
- `corpus/lessons/round-16.md:35-38` — literals at 35-37. ✓ (true at base)
- **Base `cb807bc`** exists as a commit (`git cat-file -t`). Current HEAD is `5009eca`.
- **Re-grep completeness (finding):** the entry says its pattern `6ab49127|6ab49126|1365d|79,453` "found" three locations. The current worktree also matches `LOG.md:244-245` (S11 refutation, "7/7 L1 fetches"), `LOG.md:333-334` (r17 edge-flip record), and `corpus/knowledge/publish-queue.md:22` (PQ-2 erratum). The enumeration is incomplete; the three listed are a subset. This does not change any claim, but the sentence overstates completeness.
- **Unverifiable locally:** the nginx `grep -cF '%xT-%xO'` returned `1` and the S010 §8.8.1 quote ("...might be a weak validator"). No local copy of either exists; a local grep for the quote finds only the target and its frozen copy. Recorded as historical 2026-10-19 evidence, not reverified (no network reads permitted).
- Absence flags and corrections are preserved: `[INFERENCE]` on backend identity, the "tag is not a body hash" correction, and the round-16 sample discrepancy.

## S019 metadata authority — unresolved

- `S019` appears nowhere in `corpus/` (`SOURCES.md` registers only S001-S018).
- No `CORPUS.md` exists in the tree (glob empty).
- `QUALITY.md` and `README.md` define no `verified-at` / `historical-not-live-reverified` convention (grep empty).
- The entry's trio does not reference S019. Other entries' trios (`ghp-custom-domain.md`, `crawl-scope-per-host.md`, `ghp-served-set.md`) also omit it and use the same non-compliant `verified-at` form, so this is a corpus-wide convention gap, not specific to this entry.
- **L1 must** register S019 / canonical `CORPUS.md` before any trio can cite it.

## Recommended follow-up (not performed; target unchanged by mandate)

1. `verified-at:` → append "historical-not-live-reverified" (e.g. `2026-10-19 (nginx release-1.28.0 opened 2026-10-19; RFC 9110 published June 2022; historical-not-live-reverified)`), keeping the date as the original evidence date.
2. `recheck:` → add a restore-or-retire clause, e.g. "if the nginx release-1.28.0 source is unavailable, operator must restore it or retire this entry's §Source checks".
3. Optionally reconcile "reopened" vs "opened" in the body header.
4. Field-count coverage is L1's job; not audited here.

## Commands run (all read-only; no rechecks, no network)

- `read` on target, SOURCES.md, LOG.md:155-170, publish-queue.md:250-265, round-16.md:30-40
- `grep` for trio pattern across `corpus/`; for ETag literals across the tree; for S019 / CORPUS / convention terms
- `glob` for `CORPUS.md` and the corpus tree
- `git cat-file -t cb807bc`, `git rev-parse --short HEAD`, `git show cb807bc:<file> | grep` for four cited files
- `grep -rlF 'one-second resolution'` for the RFC quote
- `sha256sum`, `wc`, `head -n | wc -c` on the target and its frozen copy
- No tools installed or updated. No files written other than this report.
