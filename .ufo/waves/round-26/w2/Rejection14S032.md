# Rejection14 S032 — FALSIFY of "RFC 3339 updated by RFC 9557 = version note, not STALE"

Candidate e28312b14b076584fedd696fae2a684e460bd11e, base 97404de4ff73d6c8a4f87385cf5fdf36dca7f006. Judged on: freshness. Verdict: **AGREE** — no S032-attributed statement is wrong at its stated scope; the note classification hides no staleness.

## Axes
1. Does any statement attributed to S032 rely on RFC 3339 text that RFC 9557 revises (§4.3 / meaning of `Z` / `-00:00`)?
2. Is any statement wrong at its own scope even at base (QUALITY round-26: "A statement whose attribution was false even at its base revision is STALE")?
3. Do the retained bytes still match the live source, and do they back the anchors?
4. Is the "note" a real application of the rule, or a downgrade that lets a STALE finding slip through?

## Framing correction
No seat ever reported S032 as STALE, so L1 had nothing to downgrade. `statements.json:214-221` gives the S032 row as `"statements": 7, "seatStale": 0, "stale": 0, "seatUnverifiable": 0` with no `l1Disposition`. In the seat report `w1/PairS032StaticCanonicalPrefl.md`, the Verdict section says "HOLD 7, STALE 0" and "Flag, not STALE: the RFC 3339 version named at :159 and :173 … is partly superseded at §4.3, which no row cites." L1 kept the seat's own classification and appended it as a note at `corpus/knowledge/static-canonical-preflight.md:194`. I still attacked the merits.

## Counterexample search and evidence

**Retained bytes match the live source.** `sha256sum fetched/text/S032-1.txt` gives `ba73293a…0959b4a0`, which matches the seat. I did one plain public GET of the SOURCES.md:40 URL (`curl -sS -D - -o >(sha256sum) https://www.rfc-editor.org/rfc/rfc3339.txt`, not saved). It returned `HTTP/2 200`, `etag: W/"497904d3f8d7902fe014956f95fe59f6"`, and sha256 `9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a`. These are byte-identical to `fetched/manifest.json` row S032/index 1 (same sha256 and ETag).

**What the revised text says, and who relies on it.** In S032-1.txt (character offsets):
- 9069/9078, §4.3: "this can be represented with an offset of "-00:00". This differs semantically from an offset of "Z" or "+00:00", which imply that UTC is the preferred reference point for the specified time." This is the only text RFC 9557 is said to revise.
- 14926: `time-offset = "Z" / time-numoffset`
- 15088: `full-time = partial-time time-offset`
- 15125: `date-time = full-date "T" full-time`
- 15191: "the "T" and "Z" characters in this syntax may alternatively be lower case"
- No hits for `Updated by`, `Obsoleted by` or `9557`. The in-scope source bytes carry no update header, so the update is evidenced only by the RFC Editor info page cited in the seat report.

**Search for anything relying on §4.3.** I grepped the corpus, scripts and skills for `-00:00|\+00:00|local offset|preferred reference|RFC ?3339|rfc3339`. The only hits are SOURCES.md:40/75/79, static-canonical-preflight.md:159/173/194, the lessons, and `scripts/receipt_replay.py`. None of the corpus statements claims anything about the unknown-local-offset convention or the reference-point meaning of `Z`/`+00:00`/`-00:00`.
- :159 cites "S032 (RFC3339 §5.6–5.7)". §5.6 and §5.7 are present at chars 14397 and 16005, and §4.3 is not cited.
- :173 says "c2 fetchedAt requires date-time with offset". This holds by the offsets-15088/15125 grammar. Under either reading, `Z` remains a `time-offset` alternative.
- SOURCES.md:40 teaching: "A date-time combines a full date with a full time whose offset is required; real calendar restrictions are not validated by lexical prefix comparisons". This rests on §5.6/§5.7 only.

**Strongest code counterexample tried.** `scripts/receipt_replay.py:144-184` maps `Z`/`z`, `+00:00` and `-00:00` to the same instant (offset 0). The selftest at :660 accepts `"2026-10-21T06:00:18-00:00"`. RFC 3339 §4.3 and the RFC 9557 change are both about local-offset meaning, not the instant. The parser computes instants and UTC days only (:184, :187-188), so neither interpretation changes its outcome. `-00:00` stays syntactically valid under the unchanged `time-numoffset` production (`[INFERENCE]` for RFC 9557's own wording: its bytes are not in SOURCES.md, so I did not fetch them).

**Base-revision check (axis 2).** `git show 97404de…:corpus/knowledge/static-canonical-preflight.md | sed -n '157,174p' | md5sum` gives `8c3922b8aff29c8e76c9096eedbe8b0a`, identical to the candidate. The diff for this file only adds lines after :178. At base, the attribution of these statements to §5.6/§5.7 was already true, so the "false even at base revision" STALE route does not apply.

**Rule fit (axis 4).** QUALITY.md:216-221 says "STALE means the statement is wrong or unsupported at its own stated scope." An "updated by" status is not one of the rule's three named note categories (verified-at date, base-scoped pointer, patch-version label). The note therefore rests on the general criterion, and it meets it: every relied-on anchor stands verbatim in identical live bytes. The S026/S027 Python 3.15.0→3.15.1 disposition (`statements.json:165,175`) is a different exemption and was not needed here.

## Residual (non-blocking, not a defect of the rejection)
- The note at :194 asserts RFC 9557 content ("revises the unknown-local-offset convention of §4.3 and keeps the §5.6 grammar"). That rests on unretained RFC Editor pages read by the seat, with no source row behind it. The note itself fences this ("A new source row is needed before any claim depends on RFC 9557"), and SOURCES.md:79 records it as "Lead noted, not a row", so it is not counted provenance.
- The seat's provenance label is imprecise. It attributes RFC 9557 §4.1/§2.2 section text to "[RFC9557 page] = https://www.rfc-editor.org/info/rfc9557/". An info page normally carries the abstract, not section bodies (`[INFERENCE]`, not fetched because the URL is outside SOURCES.md). This affects wave evidence only, not the corpus.
- `w1/RowS032.md:10` says "RFC 3339 is frozen … no version/date pin mismatch". The bytes are indeed frozen (identical sha256), but the RFC's status is updated. This is a wave artifact, not a corpus statement, and the PairS032 flag and the :194 note supersede it.

## Minimal correction
None required.

Tooling: none installed or updated. Commands run: `git log`/`git diff`/`git show` (read-only), `sha256sum`, in-memory Python substring/manifest reads, one public GET of `https://www.rfc-editor.org/rfc/rfc3339.txt` (piped to sha256sum, not saved).

```json
{"target":"S032 RFC3339→RFC9557 version-note classification","verdict":"AGREE","severity":"none"}
```
