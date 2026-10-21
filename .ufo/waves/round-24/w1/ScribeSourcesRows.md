# ScribeSourcesRows — round 24, w1 (kake lane)

Author-side draft only. `corpus/SOURCES.md` was NOT edited; no row is admitted by this report. Lane HEAD observed: f7de3ab4e9f030a15a857a5a08631bd8e690f436. Scratch: /tmp/kake-r24-ScribeSourcesRows-xXMt.

## Verdict

DRAFT READY, NOT LANDABLE YET. Three rows S032–S034 (RFC 3339, RFC 9110 media type, RFC 8259) are drafted in the exact 11-column registry format and pass every CORPUS.md census check except one: `status: mined` requires its `used-by` path to exist and cite the row, and `scripts/receipt_replay.py` does not exist in the lane yet and `corpus/knowledge/static-canonical-preflight.md` does not cite S032–S034. The rows must land together with the C2 receipt_replay.py and the knowledge citation, or be held as `queued`. Quote/locator cells are left as `<FROM-SOURCE-SEAT>` as instructed.

## Findings

### F1 (P2) — `mined` rows reference a used-by path that does not exist yet

Command (run from the lane root, against a scratch copy of SOURCES.md with the draft appended):
```
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' /tmp/kake-r24-ScribeSourcesRows-xXMt/combined.md | sort -u | while read -r p; do [ -e "$p" ] || echo "  missing: $p"; done
```
Observed output:
```
  missing: scripts/receipt_replay.py
```
Also observed: `grep -n "S032\|S033\|S034" corpus/knowledge/static-canonical-preflight.md` returned nothing, so the knowledge path does not cite the rows yet. The CORPUS.md rule "mined = cited by ≥1 path in used-by" is not satisfied until both exist.
Impacted: CORPUS.md SOURCES rule 1 and census line 147 (mined used-by existence).
Smallest fix: land S032–S034 with status `mined` only in the same integration that adds `scripts/receipt_replay.py` (C2 deliverable) and a `source:` citation of S032/S033/S034 in `corpus/knowledge/static-canonical-preflight.md`; otherwise land them as `queued` (rule: queued = opened, worth mining) and promote later.

### F2 (P3) — Round gate evidence not yet recorded for the three new rows

CORPUS.md SOURCES rule 1 requires the round lesson's `## Gate` to record, for every new row, the URL, the access date, and a ≤25-word quote with its location. No round-24 lesson gate entry for S032–S034 exists in the lane (I did not create one; that is the L1's file). The quotes below are the observed text the source seat should cite; they are not yet a Gate entry.

Observed locators in the fetched plain text (fetched 2026-10-21 by read-only GET, `curl -sSL`, HTTP 200, `text/plain;charset=utf-8`):

| row | file (sha256 of fetched text) | locator observed | observed text (for seat verification) |
|---|---|---|---|
| S032 | rfc3339.txt (9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a, 35064 bytes) | §5.6 "Internet Date/Time Format", lines 399–440 | `date-time = full-date "T" full-time`; `time-offset = "Z" / time-numoffset`; NOTE: "the "T" and "Z" characters in this syntax may alternatively be lower case" |
| S033 | rfc9110.txt (21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a, 502941 bytes) | §8.3 Content-Type line 2928; §8.3.1 Media Type lines 2972–2990 | "The type and subtype tokens are case-insensitive." ; "The type/subtype MAY be followed by semicolon-delimited parameters" |
| S034 | rfc8259.txt (61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7, 28360 bytes) | §2 JSON Grammar lines 246–256; §4 Objects lines 316–334; §8.1 Character Encoding lines 483–487 | "A JSON text is a serialized value."; "The names within an object SHOULD be unique."; "When the names within an object are not unique, the behavior of software that receives such an object is unpredictable."; "JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8 [RFC3629]." |

Cross-check: the S028 row records the rfc9110.txt plain-text sha256 as `21c1cdce…7232a`; the fetched file's full sha256 is `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, which matches. The S028 pin is therefore the same revision this draft reads.

### F3 (P3) — Scope boundaries the draft encodes (for C2 and for the seat)

- S032 is a lexical grammar. RFC 3339 §5.6 allows lower-case `t`/`z` and fractional seconds, and its `time-second` range admits `60` for leap seconds. A grammar match therefore does not establish an ordering or freshness claim; the C2 fix (lexical prefix replacement) should use the grammar, and the observedAt future check remains a separate date comparison. This is the scope the row's `scope` cell states.
- S033 scopes media-type syntax only. S010 (§8.8 ETag) and S028 (§4.2 URI schemes) are named as distinct, so no reader can cite S033 for validator or URI claims.
- S034 scopes JSON grammar, name uniqueness and UTF-8 of exchanged text. Its `scope` excludes receipt-schema validity, so `served()`-style type checks on `contentType` are not covered by S034 (that check is a schema concern).

## Draft rows (report only — NOT written to corpus/SOURCES.md)

Columns: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by. Anchor and quote-grounded cells are `<FROM-SOURCE-SEAT>`; `teaches` is drafted from the observed text in F2 and must be re-grounded by the seat's Gate quote before landing.

```
| S032 | RFC 3339: Date and Time on the Internet: Timestamps — https://www.rfc-editor.org/rfc/rfc3339.txt | spec | A | RFC 3339 `date-time` grammar for timestamp strings in receipt fields (observedAt, fetchedAt); lexical well-formedness only, not ordering, freshness or future-date judgment | <FROM-SOURCE-SEAT> | `date-time` requires full-date, upper-case T by default, and a mandatory Z or numeric offset; fractional seconds are optional; lower-case t and z are permitted by the NOTE in the same section | mined | 2026-10-21 | 365d | scripts/receipt_replay.py, corpus/knowledge/static-canonical-preflight.md |
| S033 | RFC 9110: HTTP Semantics, Media Type — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | Media-type syntax for Content-Type on HTTP responses (type/subtype tokens, parameters); distinct from S010 (ETag validators, section 8.8) and S028 (http/https URI schemes, section 4.2) | <FROM-SOURCE-SEAT> | The type and subtype tokens are case-insensitive, and parameters follow as name/value pairs whose significance depends on the media-type registry, so a served type must be compared under those rules | mined | 2026-10-21 | 365d | scripts/receipt_replay.py, corpus/knowledge/static-canonical-preflight.md |
| S034 | RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format — https://www.rfc-editor.org/rfc/rfc8259.txt | spec | A | JSON text grammar, object member-name uniqueness and UTF-8 encoding of exchanged JSON receipt files; not a receipt schema or a semantic-validity claim | <FROM-SOURCE-SEAT> | A JSON text is any serialized value, not only an object; object names SHOULD be unique and duplicate names give unpredictable results; JSON text exchanged outside a closed ecosystem MUST be UTF-8 | mined | 2026-10-21 | 365d | scripts/receipt_replay.py, corpus/knowledge/static-canonical-preflight.md |
```

Registry state checked: highest existing id is S031, so S032–S034 are the next unused ids (ids are never reused). Existing rows S010 (RFC 9110 §8.8) and S028 (RFC 9110 §4.2) are untouched.

## Checked and held

Commands run and exact outputs (census from CORPUS.md lines 133–148, applied to the scratch copy `/tmp/kake-r24-ScribeSourcesRows-xXMt/combined.md` = lane SOURCES.md + draft rows):

- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' combined.md` → `34` (31 existing + 3 drafts).
- malformed (NF!=13) → `0`.
- tier histogram → `A=32 C=2` (existing A=29 + 3 drafts; C=2 are the rejected S017/S018 rows, unchanged).
- status histogram → `mined=30 queued=2 rejected=2`.
- duplicate ids → empty.
- enum/tier-inflation check → empty.
- draft pipe width (NF) → `0` malformed draft rows; each draft row has NF=13.
- mined used-by existence → `missing: scripts/receipt_replay.py` (F1).

Read-only fetches: `curl -sSL --max-time 60` GET of the three RFC Editor plain-text URLs, HTTP 200 each; sha256 and grep-located sections as recorded in F2. No POST, no fetch of any non-RFC page.

Lane discipline: the only file written is this report. No lane production file, `corpus/SOURCES.md`, `corpus/knowledge/*`, `scripts/*` or git/jj state was changed. No subagent was spawned.

Tooling: no installs or upgrades were performed. Used host `curl`, `sha256sum`, `awk`, `grep`, `wc`, `sort`.

## Limits

- The `teaches` and `scope` text is drafted from the fetched primary text, but the locator (anchor) and the Gate quote are left as `<FROM-SOURCE-SEAT>` per assignment. The line ranges in F2 are for the seat to confirm, not a substitute for its Gate entry.
- I did not run the RFC 9110 §8.3.1 and RFC 8259 text through a reader beyond grep/sed-range printing; the locator lines were confirmed by printing the exact ranges above.
- The `used-by` paths are the ones assigned. static-canonical-preflight.md and scripts/receipt_replay.py do not yet cite these rows; I did not edit either.
- Independent admission is not claimed: I am author-side. A non-author verification pass should re-open each of the three sources and the seat's quote before the rows change status from `queued`.
- No round-24 lesson `## Gate` section was written (not in my write scope).
