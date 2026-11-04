# ScoutSources — round 83 wave w1

**Verdict:** RFC 9111 opened once from the network and retained; all three C2 grounding passages located byte-exactly; the chosen admission quote is 21 words and passes a raw multi-line substring check; the `S456` cells are drafted pipe-free and were machine-validated inside `## Registry` (exit 0) against an EOF-append control (E12, exit 1). No production file written. No blocker.

Scope: `corpus/knowledge/header-change-classes.md` is this round's new entry and `corpus/SOURCES.md` receives `S456`; both are the scribe's files, so everything below is a draft plus receipts. Retained artifact dir: `.ufo/waves/round-83/w1/ScoutSources/`.

## 1. Fetch — one GET, no retry

```
curl -sSL --max-time 90 \
  -A 'kake-shokunin-r83-w1-ScoutSources/1.0 (lane kake-shokunin; round 83 wave w1; one GET)' \
  -o rfc9111.txt -D rfc9111.headers -w 'HTTP=%{http_code} URL=%{url_effective} SIZE=%{size_download}\n' \
  https://www.rfc-editor.org/rfc/rfc9111.txt
```

| Field | Value |
|---|---|
| curl exit | 0 |
| HTTP status | 200 (HTTP/2) |
| requested = final URL | `https://www.rfc-editor.org/rfc/rfc9111.txt` (no redirect) |
| fetched-at UTC | `2026-11-04T13:29:41Z` (start and end) |
| wall time | 0.220934 s |
| bytes | 84,477 (`size_download` = retained bytes) |
| sha256 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` |
| lines | 1,956 (LF only; `grep -c $'\r'` = 0) |
| encoding | UTF-8 with BOM `ef bb bf`; `content-type: text/plain;charset=utf-8` |
| document | RFC 9111 "HTTP Caching", June 2022, STD 98, obsoletes RFC 7234 |

Response headers worth recording (`rfc9111.headers`, sha256 `77d1b975…2af1b496`): `cache-control: public, max-age=86400`, `etag: W/"f8907618635703edd228aee4aa834eee"` (weak), `date: Wed, 04 Nov 2026 13:29:41 GMT`, `cf-r2-served: 1`, `alt-svc: h3=":443"`. The weak `ETag` on this very response is S455's ground (a weak validator cannot exclude a byte change), not a claim made here.

### Comparison with retained copies in the lane

`grep -rl 'RFC 9111' corpus .ufo/waves | wc -l` → **70** files (exit 0), but every one is a *citation*: `corpus/SOURCES.md`, `corpus/knowledge/capture-drift-validators.md` §7, `corpus/lessons/round-82.md`, the retained RFC 9110 copies (`corpus/lessons/round-81-gate/rfc9110.{txt,html}`, `S010-1.txt`, `S088.txt`), wave receipts and the round-48 assimilation duplicates. No file is an RFC 9111 body:

- `find /home/vgpnk/Projects/shokunin/kake-shokunin -type f -size 84477c` → only `…/round-83/w1/ScoutSources/rfc9111.txt` (this fetch); exit 0.
- `grep -rl 'This document obsoletes RFC 7234'` (the RFC's own abstract sentence) → only this fetch and its derived `rfc9111.collapse.txt`; exit 0.
- `grep -c 'rfc9111.txt' corpus/SOURCES.md` → **0**; `grep -c '^| S456' corpus/SOURCES.md` → **0**. `corpus/SOURCES.md:265` is under `## Leads (unopened)` and names the `.html` URL, not `.txt`, so it is not a registry row and not a URL collision.

**Byte-identity answer: there is no prior side to compare.** The lane retained no RFC 9111 body before this fetch; the digest above is new to the lane, and no retained file is byte-identical to it. The `.html` lead at `corpus/SOURCES.md:265` is a different serialization (not fetched here) and is left untouched.

## 2. The three grounding passages (retained `rfc9111.txt`, 1-based lines)

Byte ranges below are the **quoted text** (leading indent excluded); `quotes.tsv` holds the same table machine-generated. Every quote occurs exactly once as a raw byte span and exactly once after whitespace collapse.

### (a) A cache reusing a stored response — the §4 reuse gate (lines 466-525)

| Lines | Bytes | Words | Quote |
|---|---|---|---|
| 468-469 | 20513..20595 | 14 | When presented with a request, a cache MUST NOT reuse a stored response unless: |
| 480-482 | 20950..21090 | 18 | the stored response does not contain the no-cache directive (Section 5.2.2.4), unless it is successfully validated (Section 4.3) |
| 484-490 | 21103..21298 | 30 | the stored response is one of the following: - fresh (see Section 4.2), or - allowed to be served stale (see Section 4.2.4), or - successfully validated (see Section 4.3). |
| 495-498 | 21402..21633 | 37 | When a stored response is used to satisfy a request without validation, a cache MUST generate an Age header field (Section 5.1), replacing any present in the response with a value equal to the stored response's current_age |

Reading taken: the item's "(a)" is the reuse gate — the only place the RFC states the conditions under which stored bytes may answer a request. The origin-server-facing conditions are the `no-cache` clause (480-482) and the three alternatives (484-490); reuse without validation carries the `Age` obligation (495-498). The other reading — a cache's own exchange with the origin server — is §4.3 (/revalidating/), covered under (c).

### (b) Fresh versus must-be-validated (§4.2 Freshness, lines 581-651)

| Lines | Bytes | Words | Quote |
|---|---|---|---|
| 583-585 | 25724..25863 | 23 | A "fresh" response is one whose age has not yet exceeded its freshness lifetime. Conversely, a "stale" response is one where it has. |
| 587-592 | 25868..26277 | 65 | A response's "freshness lifetime" is the length of time between its generation by the origin server and its expiration time. An "explicit expiration time" is the time at which the origin server intends that a stored response can no longer be used by a cache without further validation, whereas a "heuristic expiration time" is assigned by a cache when no explicit expiration time is available. |
| 597-599 | 26414..26559 | 21 | When a response is fresh, it can be used to satisfy subsequent requests without contacting the origin server, thereby improving efficiency. |

The distinction is stated twice: by definition (583-585) and by consequence — a fresh response may be reused with no origin contact (597-599), while one past its explicit expiration time "can no longer be used by a cache without further validation" (590-591). `§4.2.4` (784-799) adds the stale-serving prohibitions, and `§4.3.4` (951-988) the freshening-on-304 rules; both are cited for completeness, not quoted as admission text.

### (c) `ETag` as a validator for conditional requests (§4.3.1, lines 812-865)

| Lines | Bytes | Words | Quote |
|---|---|---|---|
| 838-839 | 37723..37811 | 15 | Another validator is the entity tag given in an ETag field (Section 8.8.3 of [HTTP]). |
| 840-844 | 37813..38160 | 51 | One or more entity tags, indicating one or more stored responses, can be used in an If-None-Match header field for response validation, or in an If-Match or If-Range header field for representation selection (i.e., the client is referring specifically to one or more previously obtained representations with the listed entity tags). |
| 848-850 | 38235..38402 | 23 | MUST send the relevant entity tags (using If-Match, If-None-Match, or If-Range) if the entity tags were provided in the stored response(s) being validated. |

This is also the RFC's own grouping of validators: `§4.3.1` says "One such validator is the timestamp given in a Last-Modified header field" (831-836) and "Another validator is the entity tag given in an ETag field" (838-839). That sentence pair is the nearest primary text for the classifier's two-member `validator` class (`etag`, `last-modified`); the other three class names are not RFC vocabulary (see §5).

## 3. Raw substring check for the admission quote

Chosen quote: **lines 597-599, bytes 26414..26559, 21 words** —

> When a response is fresh, it can be used to satisfy subsequent requests without contacting the origin server, thereby improving efficiency.

Commands and results (`raw-checks.txt`):

1. `awk 'NR>=597 && NR<=599' rfc9111.txt` → the three raw lines, exit 0.
2. `grep -F 'When a response is fresh, it can be used to satisfy subsequent' rfc9111.txt` → line 597 matched, **exit 0** (a contiguous raw single-line prefix).
3. `grep -F '<the whole sentence on one line>' rfc9111.txt` → **exit 1**: expected, because the sentence is hard-wrapped at 3-space continuation indents; a single-line literal cannot occur in this file.
4. `grep -Pzo 'When a response is fresh, it can be used to satisfy subsequent\n   requests without contacting the origin server, thereby improving\n   efficiency\.' rfc9111.txt` → **exit 0** (the exact multi-line raw span).
5. `awk 'NR>=597 && NR<=599' … | wc -w` → **21** words ≤ 25.
6. Byte-level count of the exact raw span → 1 occurrence; same quote after whitespace collapse → 1 occurrence.

**Over-25 case found and reduced.** The natural second sentence of the freshness-lifetime paragraph (lines 588-592, from "An \"explicit expiration time\"" through "…is available.") is **45 words**, well over 25. Its first clause alone is 28 words. Shorter raw span, bytes 26085..26165 (inside lines 590-591, **14 words**) verified by `grep -Pzo` exit 0 and one raw occurrence:

> a stored response can no longer be used by a cache without further validation

If the scribe prefers a different admission quote, the safe ≤25-word candidates are 468-469 (14 w), 480-482 (18 w), 583-585 (23 w), 597-599 (21 w), 838-839 (15 w) and 848-850 (23 w); 484-490 (30 w), 840-844 (51 w) and 838-844 (66 w) exceed 25 as spans and must be trimmed.

## 4. `S456` row — cells in contract order

Insertion point: **after line 202** of the current `corpus/SOURCES.md` (the `| S455 | …` row; the table ends there, `## Paths` is line 204). Eleven cells, no `|` in any cell, tab-free, one physical line (`rows-draft.txt`):

```
| S456 | RFC 9111 — HTTP Caching — https://www.rfc-editor.org/rfc/rfc9111.txt | spec | A | The HTTP cache-reuse gate, the fresh-versus-stale distinction and the entity tag as a conditional-request validator, which is the caching behaviour a two-instant capture comparison is read against; not the classifier's per-request, validator, representation, policy and unknown class names, which are lane policy; not which fields a particular edge or origin varies per exchange; not ETag generation, opacity or comparison strength (RFC 9110 §8.8, S010 and S455); not cache-directive argument syntax as a subject; not conditional-request semantics beyond the ETag validator; not any claim that a capture observed origin bytes | §4 Constructing Responses from Caches lines 466-525 (MUST NOT reuse gate 468-490; no-cache validation clause 480-482; fresh, stale or validated alternatives 484-490); §4.2 Freshness lines 581-651 (fresh and stale definitions 583-585; freshness lifetime versus explicit expiration 587-592; fresh reuse without contacting the origin 597-599); §4.3.1 Sending a Validation Request lines 812-865 (entity tag as validator 838-839; If-None-Match and If-Match 840-844; MUST send stored entity tags 848-850); June 2022, STD 98, obsoletes RFC 7234; fetched 2026-11-04T13:29:41Z, HTTP 200, 84,477 bytes, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e, retained at .ufo/waves/round-83/w1/ScoutSources/rfc9111.txt | A cache must not reuse a stored response unless it is fresh, allowed to be served stale or successfully validated; a fresh response can be used without contacting the origin server, while one past its explicit expiration time can no longer be used without further validation; the entity tag in ETag is a validator that a cache sends in If-None-Match to validate a stored response | mined | 2026-11-04 | 365d | corpus/knowledge/header-change-classes.md |
```

Cell lengths in registry order: id 4 · source 68 · kind 4 · tier 1 · scope 625 · anchor 725 · teaches 379 · status 5 · opened 10 · recheck 4 · used-by 41.

Mechanical checks (`check-row.txt`):

- Splitting the line on `|` yields 13 fields, first and last empty; the 11 middle cells are non-empty; no cell contains `|` (checked in Python over the split, not assumed).
- The anchor's sha256 and `84,477` are the retained file's actual values (`sha_in_anchor=True`, `bytes_in_anchor=True`).
- **Positive control:** `git archive HEAD | tar -x` of the lane into scratch, a placeholder `corpus/knowledge/header-change-classes.md`, row inserted after `| S455 |`, then `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <copy>/corpus/SOURCES.md` → **exit 0**, `file ok …`, `S456` findings 0. No W04 for the new URL (it is unique in the registry).
- **Negative control:** same tree with the row appended at EOF → **exit 1**, `file E12 S456 row outside Registry section`. So appending at end of file is a defect; insert after line 202.
- **Ordering requirement (E11):** `used-by corpus/knowledge/header-change-classes.md` must exist on disk *before* the row is validated. The scribe's step order (entry first, row second, census third) satisfies this; if the entry lands after the row, validation will read `E11 S456 missing used-by …`.
- A first sandbox that held only `corpus/` + a knowledge placeholder was discarded: every existing row read `E11` because the rest of the lane was absent there, so it could not serve as evidence. Only the `git archive` tree is cited above.

## 5. Findings the entry should not overclaim (marked, not sourced)

- **RFC 9111 uses the word "validator" (18 occurrences) and names exactly two:** Last-Modified and the entity tag. It never uses "per-request", "representation metadata" (0 occurrences of the phrase in the retained bytes), "policy" or "unknown" as header classes. So the frozen class table's `validator` members have direct textual support; the other four class names and the rule "an unknown changed header is treated as representation-bearing" are **lane policy**, to be marked as such in the entry.
- **Nearest RFC adjacency for the `unknown` class:** §3.1 "Storing Header and Trailer Fields" lines 338-343 — "Caches MUST include all received response header fields -- including unrecognized ones -- when storing a response". This grounds *storage* of unrecognised fields, not the stronger claim that a changed unrecognised field means the representation changed. Quote it only for the storage premise.
- **`Vary` and cache keys are separate ground:** §4.1 (526-580, `cache key` at 251-264) defines key selection from `Vary`; the classifier's `representation` membership of `vary` is a classification choice, not a §4.1 inference.
- **The fetch's own `ETag` is weak** (`W/"f8907…"`). Nothing in this report reads it as a byte identity; the digest above is computed from retained bytes, mirroring S455's `:3428-3429` ground.

## Tooling, scope, hygiene

- No tool installed or upgraded; used only pre-existing `curl`, `grep`, `awk`, `python3`, `git` (read-only `git archive`).
- Production files written: **none**. Files written are the report, `rows-draft.txt` and the receipts under `.ufo/waves/round-83/w1/ScoutSources/` (`rfc9111.txt`, `rfc9111.headers`, `rfc9111.collapse.txt` sha256 `1e13f59d…8ace19`, `quotes.tsv`, `fetch.txt`, `raw-checks.txt`, `retained-copy-scan.txt`, `check-row.txt`).
- Scratch `/fast/scratch/hyaku/kake-r83/ScoutSources/` removed before yield (verified absent; `ls` exit 2). The two `/tmp` temporaries used by the archived-tree driver were deleted.
- No socket opened beyond the single GET in §1.

## Verdict

**PASS (scout scope).** RFC 9111 fetched once (HTTP 200, 84,477 bytes, sha256 `aeb52adb…02cf3e`, `2026-11-04T13:29:41Z`), no prior lane copy exists so no byte-identical comparison is available; the three C2 passages are located and quoted with exact line and byte spans; the admission quote is 21 words with a passing raw multi-line check (an over-25 natural sentence was found and reduced to a 14-word raw span); the `S456` cells are complete, pipe-free and validated inside `## Registry` at exit 0 with an EOF-append E12 control at exit 1. Remaining unknown: none blocking the scribe; the only preconditions are the insertion point (after line 202) and creating `corpus/knowledge/header-change-classes.md` before the census run.
