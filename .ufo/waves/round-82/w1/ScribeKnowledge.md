# ScribeKnowledge — round 82 wave w1

C2 knowledge entry (`corpus/knowledge/capture-drift-validators.md`, new) and S455 registry row.
No network, no VCS mutation, no tool install or upgrade, no subagent dispatch.

## Axes

1. **Source fidelity** — every RFC claim carries a retained `file:line` and a quoted span that replays
   against those bytes; the retained copy's digest matches the one S453/S454 already pin.
2. **Scope confinement** — validator/change-detection ground only; no cache policy, no conditional
   requests, no property-correctness claim.
3. **Replayability** — each executed claim names argv, exit and, where applicable, a digest.
4. **Declared absence** — capture B and its record are absent; the entry says pending and asserts no
   finding.

Moves kept (each improves an axis, harms none): the entry; the one-row insert; the receipt set. The
entry was revised twice — the S010 cross-reference its row's scope cell promises, and a note for the
one quoted compound the source itself folds across lines.

## Commands run

cwd is `/home/vgpnk/Projects/shokunin/kake-shokunin` unless stated.

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `sha256sum .ufo/waves/round-81/w1/ScoutSources/rfc9110.txt .ufo/waves/round-80/sources/rfc9110.txt corpus/lessons/round-81-gate/rfc9110.txt` | 0 | all three `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`; retained copy 502,941 B |
| 2 | `python3 -B scripts/capture_delta.py --selftest` | 0 | `selftest: 14/14 passed` (contract asks >= 12) |
| 3 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` | 0 | 22 `W04` lines, 1 `ok` line (full stdout below) |
| 4 | `awk 'NR==202' corpus/SOURCES.md \| awk -F'\|' '{print NF; print NF-2}'` | 0 | `NF=13`, 11 cells |
| 5 | `git diff --numstat -- corpus/SOURCES.md` | 0 | `1 0 corpus/SOURCES.md` — one added line, none removed |
| 6 | `grep -c '^| S455 ' corpus/SOURCES.md` | 0 | `1`; `S455` appears nowhere else in the file |
| 7 | `sha256sum corpus/knowledge/capture-drift-validators.md corpus/SOURCES.md scripts/capture_delta.py` | 0 | entry `8f0fe969…c601e3f6` (174 lines); SOURCES `67cf235e…bf2b39b`; tool `4b0dc252…558d9680` |
| 8 | `ls -la corpus/lessons/round-82.md .ufo/waves/round-82/capture/manifest.json .ufo/waves/round-82/controls/after-c2-delta.txt` | 2 | all three absent on the first two checks; the lesson appeared on the third (row 10); the capture and the record are still absent at report time |
| 9 | replay of the entry's 12 quoted spans against the retained RFC text | 0 | `verbatim_after_whitespace_collapse=11/12`; the miss is the source's own fold of `opaque-tags` at 3651-3652, and `with_source_fold_joined=12/12`; receipt `quote-check.out` |
| 10 | `ls -la corpus/lessons/round-82.md && wc -l corpus/lessons/round-82.md && sha256sum corpus/lessons/round-82.md` | 0 | 14,779 B, 215 lines, `11bc1293…5473d6`; stable across a 2 s re-read; S455's `used-by` then amended to name it |
| 11 | re-run of command 3 after the amendment | 0 | stdout byte-identical to command 3 (`diff` empty); row still `NF=13`, 11 cells; `git diff --numstat` still `1 0` |

No socket was opened by this seat; the RFC bytes quoted here are the retained copy that S453 and S454
pin, and command 1 re-derived that copy's digest. Scratch: none needed, none created, nothing to
delete.

## Deliverables

- `corpus/knowledge/capture-drift-validators.md` — 174 lines. Provenance trio on lines 1-3
  (`source:`, `verified-at:`, `recheck:`); `source:` cites S455, the URL
  `https://www.rfc-editor.org/rfc/rfc9110.txt` and the §8.8.1 / §8.8.3 / §8.8.3.2 line spans.
  Sections: what the source fixes (10 quoted facts with word counts), what the delta compares (exact
  printed line formats), the two captures, procedure and exit codes, limits, marked lane readings.
- `corpus/SOURCES.md` — S455 inserted at line 202, immediately after S454 (line 201). Rows S449-S454
  keep their previous lines 196-201; the diff is one insertion and zero deletions. `used-by` names
  `corpus/knowledge/capture-drift-validators.md` and `corpus/lessons/round-82.md`; the lesson was
  absent when the row was first written, so the cell was completed once the file appeared (row 10)
  and the validator re-run green (row 11).
- Receipts under `.ufo/waves/round-82/w1/ScribeKnowledge/`: `sources-validate.out`,
  `sources-validate.final.out` (byte-identical), `sources-validate.exit`, `capture-delta-selftest.out`,
  `row-check.out`, `quote-check.out`, `digests.out`.

## Validator stdout (verbatim, exit 0)

```text
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
kake	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
kake	W04	S427 duplicate url developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers across scopes
kake	W04	S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S445 duplicate url html.spec.whatwg.org/multipage/links.html across scopes
kake	W04	S450 duplicate url html.spec.whatwg.org/multipage/semantics.html across scopes
kake	W04	S451 duplicate url www.rfc-editor.org/rfc/rfc3339.txt across scopes
kake	W04	S453 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S454 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S455 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```

`W04` is the documented same-URL-across-scopes warning; S455 joins 21 rows that already warned (22
`W04` lines including it), and warnings do not change the exit status.

## Verdict

Authored and green on the mandated check: entry written, S455 inserted after S454 with 11 cells and
no earlier row moved, `used-by` naming the entry and the round lesson, validator exit 0 on the final
bytes. **C2's delta finding is pending, not stated** — capture B and
`.ufo/waves/round-82/controls/after-c2-delta.txt` did not exist at authoring or at report time, so the
entry names capture A's three instants and digests (`2026-11-04T12:05:06Z` for all three) and records
B as pending. No handoff is open on the row itself.

## Findings

- **F1 — delta record absent.** `.ufo/waves/round-82/capture/` and
  `.ufo/waves/round-82/controls/after-c2-delta.txt` do not exist (checked at authoring and at report
  time). The entry therefore carries no delta verdict, no `identical`/`changed` count and no capture
  B instant. Named remedy, already in the entry: run
  `python3 -B scripts/capture_delta.py --a .ufo/waves/round-81/capture --b .ufo/waves/round-82/capture`
  once B exists and let its stdout be the record. A later editor should replace the pending sentence
  with the record's actual summary line rather than leaving it stale.
- **F2 — the round lesson landed mid-seat, and `used-by` now names it.** `corpus/lessons/round-82.md`
  is owned by ScribeLesson82 (`w1-spec.json` item). It was absent when the row was first written, and
  `sources-census.sh`'s `E11` treats any `used-by` path missing from disk as an error, so naming it
  then would have turned the mandated validate from exit 0 into exit 1. The row was inserted with the
  knowledge entry only, the lesson appeared afterwards (14,779 B, 215 lines, `11bc1293…5473d6`), and
  the cell was amended to `corpus/knowledge/capture-drift-validators.md,
  corpus/lessons/round-82.md`. The validator re-run on the amended bytes is byte-identical to the
  first run and exits 0 (rows 10-11). No handoff remains; a later renumbering would be a defect.
- **F3 — S455 overlaps S010 on the same document.** S010 already cites
  `https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8` for "HTTP validator semantics for entity
  tags" (8.8.1 Weak versus Strong, 8.8.3 ETag) and teaches ETag opacity plus a strong validator
  changing on a metadata change. This is not an `E04` duplicate (different serialization path, new
  scope text) and not the seat's stop condition (the URL is not the same string and the scope is the
  delta ground, not ETag anatomy), so the row was inserted as specified and the entry cross-references
  S010 in its lane readings instead of claiming that ground as new. Reported, not repaired: the item
  freezes S455 and its section anchors.
- **F4 — `W04` on S455 is expected.** `www.rfc-editor.org/rfc/rfc9110.txt` is now the row-level URL of
  S028, S033, S453, S454 and S455, each with a distinct section scope; the warning is informational
  and the lane remains exit 0. It is pre-existing behaviour (21 such rows before this one).
- **F5 — the record's verdict is not a body verdict.** `identical` conjoins status, body sha256, body
  length and the full header mapping, so a header-only difference prints `verdict=changed` with
  `body=same` (e.g. a per-response `Date` or an `ETag` move). The entry states this so a reader does
  not read a header move as content drift; it is also the concrete reason the lane's gate never
  consumes a server `ETag` as a byte identity.
- **F6 — ordering and floor are not the tool's.** `capture_delta.py` parses `fetchedAt` as RFC 3339
  but compares no instants; `order_ok` and `floor_ok` belong to `c82_capture_delta.py`. The entry says
  so, so a green delta record is not misread as proof that B postdates A.

## Not done / limits of this seat

- Did not capture B and did not touch the network: the second capture and the record are the capture
  executor's, not this seat's item.
- Did not write `corpus/lessons/round-82.md`, `corpus/README.md` or `PROVINCE.md`.
- Did not commit, stage, or run any mutating git/jj command; read-only `git diff`/`status` only.
- Did not renumber anything and did not touch a row above S455; the insert diff is `1 0`.
- Unobserved and therefore not claimed: any live property's state, any crawler behaviour, and any
  cache or conditional-request semantics (outside the entry's scope by instruction).
