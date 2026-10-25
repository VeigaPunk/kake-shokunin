# ExecRowsAccess

ATTACKS: claim C1 — the three `corpus/README.md` §Coverage map rows at revision a7a548e102b71bd16b0a6ddafa469393a2c98b69 for `corpus/knowledge/accessibility-review-cards.json` (README.md:46), `corpus/knowledge/accessibility-review-packet.md` (README.md:47), `corpus/knowledge/freshness-sidecar.json` (README.md:55).

Method: every row was extracted with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show a7a548e…:corpus/README.md | awk -v n=<46|47|55> 'NR==n'`; every file body, `corpus/SOURCES.md`, `.ufo/waves/round-25/population.json` and `scripts/accessibility_packet.py` were read from the same revision; the gate was executed only inside a `mktemp -d` extraction (`git archive … | tar -x -C $D`). No lane path other than this report was written.

## PER-ROW

| file (README line) | atomic statement | class | evidence line | command output |
|---|---|---|---|---|
| cards.json (46) | "Preparation-only WCAG 2.2 success-criterion cards" | SUPPORTED | `cards.json:8` "Preparation only: kake inventories the scope and requests a separately operator-authorized evaluator" (12 words); `cards.json:6` every `source` is `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#…` | `publisherCheck` starts "Preparation only" in 55/55; `source` WCAG22 URL 55/55 |
| cards.json (46) | "a source quote, publisher check procedure, evidence needed, failure example and limitation per card" | SUPPORTED | `cards.json:7-11` carry `sourceQuote`, `publisherCheck`, `evidenceNeeded`, `failureExample`, `limitation` for card 1.1.1 | each of the 5 fields non-empty in 55/55 (`missing []` ×5) |
| cards.json (46) | "status is not-assessed" | SUPPORTED | `cards.json:12` `"status": "not-assessed"` | `Counter({'not-assessed': 55})` |
| cards.json (46) | "each names the shared handoff record" | SUPPORTED | `cards.json:9` "Use corpus/handoffs/accessibility-preparation.md; keep this reusable card not-assessed." (7 words) | handoff path present in `evidenceNeeded` 55/55; "Shared record for every card" 55/55 |
| packet.md (47) | "Fixed Level A/AA WCAG 2.2 criterion population" | SUPPORTED | `packet.md:15` "The fixed population is the Level A and AA success criteria in W3C's" (13 words); `packet.md:1` `source: S035 — …REC-WCAG22-20241212/` | `population.json` criteria 55 (`A` 31, `AA` 24); card ids == population ids, titles equal, levels equal (True/True/True) |
| packet.md (47) | "one `not-assessed` card per criterion" | SUPPORTED | `packet.md:25` "`accessibility-review-cards.json` contains one card per selected criterion:" (7 words); `packet.md:28` "limitation. Each card's status is `not-assessed`." | cards 55, unique ids 55, statuses not-assessed 55/55, `accepted 55 / expected 55` |
| packet.md (47) | "with located quote, publisher check, evidence needed, failure example, limitation" | SUPPORTED | `packet.md:25-31`; card fields as above | quote word counts min 7 / max 25 (packet rule 6–25); 5 fields non-empty 55/55 |
| packet.md (47) | "a local gate validates structure, metadata and quote binding" | SUPPORTED | `packet.md:138` "The gate validates **structure, metadata and quotation binding only**." (9 words); `scripts/accessibility_packet.py:13` FIELDS set, `:96,:111` `metadata_mismatch`, `:114-125` `quote_too_short`/`quote_too_long`/`quote_not_from_source` | `python3 -B scripts/accessibility_packet.py --root $D --json` → `EXIT=0`, `{"accepted":55,"expected":55,"findings":[],"verdict":"clean"}`; mutated quote probe → `EXIT=1`, `['quote_not_from_source']`, card 1.1.1 rejected |
| packet.md (47) | "never website conformance" | SUPPORTED | `packet.md:8` "It does **not** measure a website's accessibility." (7 words); script line 2 "Validate review-packet readiness, never a website's WCAG conformance." | both gate runs report `"websiteConformance": "not-assessed"` |
| sidecar.json (55) | "30 entries" | SUPPORTED | `sidecar.json:3` `"entries": [` | `entries 30`; duplicate `(file,line)` pairs `[]`; 11 distinct files, all readable at the revision |
| sidecar.json (55) | "each naming a cited file and line number, a `~/Projects/...` path token, the line SHA-256" | **STALE** | `sidecar.json:5-8` `"file"`, `"line"`, `"token"`, `"lineSha256"` for entry 1 | fields present 30/30; hash equals sha256 of the cited line at the authoring commit 3d07733 (2026-10-21): **30/30**; at a7a548e: **23/30**, the 7 mismatches are SKILL.md 364, 423, 431, 445, 448, 449, 450 and each recorded hash now matches the line **one number higher** (e.g. recorded `7070c25f…` is now SKILL.md:365, recorded `6e1baa1f…` is now :449). The line↔hash correspondence is true only at the recorded date, not at the measured revision |
| sidecar.json (55) | "kind `absent` or `restored`" | SUPPORTED | `sidecar.json:9` `"kind": "absent"` | `Counter({'restored': 26, 'absent': 4})` |
| sidecar.json (55) | "date 2026-10-21" | SUPPORTED | `sidecar.json:10` `"date": "2026-10-21"` | `Counter({'2026-10-21': 30})` |
| sidecar.json (55) | "a note carrying the `test -e` exit code" | SUPPORTED | `sidecar.json:11` "…absent (test -e exit 1); exact removal time and cause unknown…" | note contains `test -e exit` 30/30; exit digit agrees with kind 30/30 (absent→1, restored→0) |
| sidecar.json (55) | "marking the citation historical" | SUPPORTED | `sidecar.json:11` "Citation corpus/knowledge/drift-detection.md:77 is a historical record, not an executable instruction." | note contains `historical` 30/30 |

### S-id cross-check

- README.md:47 cell names `(S035)`; `packet.md:1` header names `S035`; `corpus/SOURCES.md:43` is `| S035 | W3C: Web Content Accessibility Guidelines (WCAG) 2.2 …`. Sets equal, id registered.
- README.md:46 cell names no `(S###)` id and `cards.json` is a bare JSON array with no `source:` header — both sets empty, no mismatch (each card instead carries a WCAG 2.2 URL).
- README.md:55 cell names no `(S###)` id and `freshness-sidecar.json` has only `"schema": "kake-paths-sidecar-v1"` (`sidecar.json:2`), no `source:` header — both sets empty.

## COUNTS RE-DERIVED

- cards.json: `len 55`; unique ids 55; levels `{'A': 31, 'AA': 24}`; statuses `{'not-assessed': 55}`; field-empties all `[]`; handoff path 55/55; `Shared record for every card` 55/55; quote words `min 7 max 25`.
- population.json: `population criteria 55`, levels `{'A': 31, 'AA': 24}`, `source https://www.w3.org/TR/2024/REC-WCAG22-20241212/`; card ids/titles/levels identical (`True/True/True`).
- packet gate (temp extraction of a7a548e): `EXIT=0`, `accepted 55`, `expected 55`, `findings []`, `verdict clean`, `websiteConformance not-assessed`; mutated-quote control `EXIT=1`, `quote_not_from_source`.
- freshness-sidecar.json: `entries 30`; kinds `restored 26 / absent 4`; dates `2026-10-21 ×30`; tokens starting `~/Projects/` 30/30; `lineSha256` 64-hex 30/30; note `test -e exit` 30/30; note `historical` 30/30; exit digit == kind 30/30; line-hash match at a7a548e 23/30, at 3d07733 30/30; 7 mismatched entries are SKILL.md and are all off by exactly one line.
- Note (not a row defect): 9 of 30 tokens do not appear literally on their cited line; the cited lines carry the same path in `/home/vgpnk/Projects/...` form, so the `~/Projects/...` token is a normalized rendering.

## PROPOSED REPLACEMENTS

Only README.md:55 needs one. Current cell:

``30 entries, each naming a cited file and line number, a `~/Projects/...` path token, the line SHA-256, kind `absent` or `restored`, date 2026-10-21, and a note carrying the `test -e` exit code and marking the citation historical.``

Proposed minimal cell (13+ tokens, no `|`, shares "entries", "line", "token", "kind", "date", "note" with the file's first 1500 bytes, true at a7a548e):

``30 entries dated 2026-10-21, each naming a cited file and line number, a `~/Projects/...` path token, the line SHA-256 as of that date, kind `absent` or `restored`, and a note carrying the `test -e` exit code and marking the citation historical.``

Optional stronger variant, if the map is to disclose the observed drift: append `Seven SKILL.md cited lines now sit one line lower than the recorded number; the hashes still identify the recorded line content.`

README.md:46 and README.md:47: none needed.

## UNRUN

- Network re-open of `https://www.w3.org/TR/WCAG22/` to test the dated-Recommendation claim (not asserted by README.md:47; the packet itself states the offline gate cannot observe a new release).
- Packet selftests and `frozen_replay.py` (README.md:47 claims only the gate's structure/metadata/quote-binding role, which was executed).
- No tool install or upgrade was needed or performed.

VERDICT: README.md:46 and :47 fully supported at a7a548e; README.md:55 is supported except the line↔SHA-256 correspondence, which is STALE for 7 of 30 SKILL.md entries (hashes now one line low), with a minimal date-qualified replacement cell supplied.
