# ScoutErrata — seat report, kake round 97, w1 (hyaku run 15, attempt 1)

seat: ScoutErrata
lane tip verified at start: `git rev-parse master` = `9e27ce0b2a8d168e032ab79ea11471b36eaceedf` (expected C1 repair tip)
frozen digests verified: `sha256sum` over
  `.ufo/waves/round-97/c97_index.py`            = `8535150e91bd610bd42186b3ad8be23477b0386a1f8d14b95aba8375788aa008` (match)
  `.ufo/waves/round-97/c97_reval.py`            = `f3895a32464ffe88d08cfeae5cd4ace1d4b1df6a472871c19c96131164e39266` (match)
  `.ufo/waves/round-97/frozen/neg-lookup-table.py` = `898df9a2ce5ea7713d3d5c33ada13250a667c490eccbaf642556295ca9c460cc` (match)
All three match `controls/instrument-sha256.txt`; re-verified after the mid-run scratch-deletion incident (below) with no drift.

# Deliverables (all inside `.ufo/waves/round-97/w1/ScoutErrata/`)

| file | sha256 (first 16) | what it is |
|---|---|---|
| errata-9111.html | b906ce97f132718b | retained raw body of the errata search page (713 lines, 40374 bytes) |
| fetch.txt | ddfc674ab477e10d | single-GET fetch receipt (hop-by-hop URL + 302 hop status, final URL, byte count, sha256, UTC access time) |
| records.tsv | 9e7c26f43556c19e | 4 records, columns: eid / status / type / section / line:id_heading / line:section_line / line:record_span |
| s481-row.md | 463b891ed780cd1c | drafted SOURCES S481 row (S479 shape) + cell checks |
| entry-paragraph.md | 6e0c51460434ee21 | `## Errata sweep (round 97)` paragraph draft for revalidation-exchange.md |
| entry-paragraph-receipt.txt | 1af5b6c42ec98265 | structural verification of entry-paragraph.md |
| quotes-verified.txt | 6e5b01329bec9ead | quote-in-body checks (exact substring, single hit each) |

# Fetch receipt (the one GET)

  requested_url: https://www.rfc-editor.org/errata_search.php?rfc=9111
  hop 1: HTTP 302 -> Location https://errata.rfc-editor.org/search/?rfc_number=9111
  final_url: https://errata.rfc-editor.org/search/?rfc_number=9111
  http_status: 200 (final); 302 (hop 1)
  bytes: 40374, sha256 b906ce97f132718b55c846639bb1ffdfcd0da387c7988fc7c055066bea3b7395
  content_type: text/html; charset=utf-8
  server_date: 2026-11-05 (both hops)
  accessed_utc: 2026-11-05T21:07:55Z (shell date -u immediately before curl, t0; t1 same second)
  command: single `curl -sS -L --max-redirs 10 -o errata-9111.html -D headers-raw.txt -w '...' "...9111"` (rc 0, final_code=200)
  exactly one fetch; no per-EID sub-fetch.

# Records found (errata page lines 105-673)

  9004  Reported                 Technical   sec 3.5    id_heading line 129  sec_line 173  record lines 127-209
  9185  Reported                 Technical   sec 4.3.4  id_heading line 212  sec_line 260  record lines 210-359
  9166  Held for Document Update Technical   sec 5.2.3  id_heading line 385  sec_line 443  record lines 383-465
  7695  Rejected                 Technical   sec 4.3.2  id_heading line 491  sec_line 547  record lines 489-670
No Verified erratum exists for RFC 9111 on this page.

# §4.3-family targeting finding

EID 9185 (Reported, Technical) is the only record in the Verified/Reported/Held set that targets any of §4.3, §4.3.1, §4.3.2, §4.3.3, §4.3.4 — its record heading is `Section 4.3.4 says:` (raw body line 260) and its notes name §4.3.1 at body lines 305 and 322. It proposes replacing the §4.3.4 stored-response-update initial set and appending a strong-ETag association rule. EID 9004 targets §3.5 (not 4.3.x), EID 9166 targets §5.2.3 (not 4.3.x), EID 7695 targets §4.3.2 but is Rejected (excluded from the Verified/Reported/Held scope).

So the targeting_4.3 count over the Verified/Reported/Held set is 1, and none of those records touches the §4.3.1/§4.3.3 spans the C2 instrument decides — the §4.3.1/§4.3.3 ground S480 holds is untouched; the nearest live threat (EID 9185) operates on §4.3.4, which contract v1 explicitly excludes.

# Located quote

  4 words. Exact substring of the raw fetched body, raw line 260, inside the EID 9185 record (lines 210-359):

  > Section 4.3.4 says:

Verified in quotes-verified.txt: substring_ok=True, count_lines=1, line=[260].

# S481 row draft and entry paragraph draft

- `s481-row.md` carries the drafted 11-column row in the S479 shape (same column order, kind `dataset`, tier `A` scoped to "errata status of RFC 9111 section 4.3 and its subsections", status `mined`, opened `2026-11-05`, recheck `90d`, used-by `freeze.md, corpus/knowledge/revalidation-exchange.md, corpus/lessons/round-97.md`) plus cell-pipe and backslash-free checks (11 cells, no `\|`, no `|` inside a cell, verified rc 0).
- `entry-paragraph.md` carries the `## Errata sweep (round 97)` paragraph in S479's prose register: names the fetch receipt, the S481 id, the finding (9185 is the 4.3-family hit, §4.3.1/§4.3.3 remain untouched), and the excluded-ground note; 107 words.

# Mid-run incident receipt (ConnectorScope-23, ~18:14Z)

Peer agent `ConnectorScope-23` broadcast that it ran `rm -rf /fast/scratch/hyaku/kake-r97` — the round PARENT directory — deleting all sibling seats' scratch trees, including mine. Verified by this seat immediately after the broadcast:

- `ls -d /fast/scratch/hyaku/kake-r97` still exists
- `ls /fast/scratch/hyaku/kake-r97/ScoutErrata` -> No such file or directory (my tree destroyed)
- all seven deliverables in the lane seat directory are intact, sha256-verified post-incident, byte counts unchanged (errata-9111.html still 40374 bytes, 713 lines)
- no re-derivation was needed; the pulled errata body had already been copied into the lane dir before the deletion, and the scratch carried only the curl headers/tools that fetch.txt already summarizes.

This seat makes no scratch cleanup: the scratch tree is already non-existent post-incident, which is the required end-of-run clean state. Reporting the incident here as received (not re-derived from ConnectorScope's own logs — outside this seat's discovery scope); ConnectorScope reports the same event as its own defect route.

# Defects / routes from this seat

1. (structural, status-neutral) `entry-paragraph.md` paragraph word width is 107 words — well under the 120-word bound, no usable defect; noted only because the S479 precedent paragraph was 103 words and a tighter register would read cleaner.
2. (ambient, routed by ConnectorScope-23, recorded here for visibility) cross-seat scratch deletion at ~18:14Z destroyed this seat's tree; no frozen artifact, lane tree, MANIFEST, or host state was touched; this seat's lane-dir deliverables were unaffected.
3. (nothing else) fetch was a single clean GET with no retry, no rate-limit, no per-record sub-fetch; the records.tsv spans and §-targeting findings were re-checked against the committed body copy line-for-line.
