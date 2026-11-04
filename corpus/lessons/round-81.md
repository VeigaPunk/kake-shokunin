# Round 81 — lessons (kake, attempt 1)

Base `2e11925500dd5a739376c9108c94616243af0cd4` (lane `master` tip at round open, 2026-11-04);
frozen contract `.ufo/waves/round-81/contract.md` at the freeze commit
`a77b8a19c2b65a07dfbe40aaf7ec86aaeee2f9cb`, which carries the contract, both counters
(`c81_defect_queue.py`, `c81_capture_audit.py`), the junk-tree builder and its spec, the C2
expectations file, the base and junk control receipts, and `scripts/wave_seat_record.py`. One v1
wave of fifteen requested seats (`w1-spec.json`: executor 4, reviewer 4, scout 2, scribe 2,
critic 1, mutation-tester 1, connector 1) against the band 8–16 and the ≥25 % attack floor over
{reviewer, critic, mutation-tester, labrat}. Two claims: **C1 calibration 2** — the lowest
non-retired axis — closes the round-80 routed-defect queue, and **C2 operability 10** lands a
capture-once / audit-offline chain whose verdict re-derives from committed bytes. Two amendments,
both written before any round-81 after-state — `amendments/amendment-1.md` (C1's settled-seat
population; the S454 section anchor) and `amendments/amendment-2.md` (C2's instrument measures the
frozen declared expectations, adds `--revision`, and compares the audit bytes) — correct three
instruments' readings and one prose anchor without moving a predicate. Scores are held; a claim
moves evidence, not a scalar.

## Claims

**C1 — calibration: the round-80 routed-defect queue closes.** Population: the six items the
non-author round-80 closure filed at `corpus/lessons/round-80-verifier-spotcheck.md` §6 —
`R80-1` … `R80-6`; none added or dropped after data. Frozen predicate:

    met <=> open == 0

decided from bytes by `python3 -B .ufo/waves/round-81/c81_defect_queue.py --root <tree>
[--revision <rev>]`, which never reads a word that merely says "closed". The item conditions:
R80-1 re-derives the `S453` line of `corpus/SOURCES.md` and looks for an `R80-1` row naming it
in this file; R80-2 re-parses `.ufo/waves/round-80/controls/ctl-c80-constants.txt` and recomputes
its arithmetic; R80-3 counts registry rows per URL token; R80-4 re-derives the wave's settled
attack share from `w1-spec.json` + `w1-results.json` and compares `w1-accounting.json` to it;
R80-5 rebuilds round-80's junk tree twice from `junk-tree.json` and re-runs round-80's own
counter over it; R80-6 re-runs `scripts/wave_seat_record.py` and compares the result to
`seat-failures.json` canonically. Controls, all committed before the after-state:
`controls/base-c81-defect-queue.txt` reads `open=6 met=false`, exit 1;
`controls/ctl-c81-junk-queue.txt` over a tree that fabricates closure in words reads
`open=6 closed=0 met=false`, exit 1; `controls/c81-selftest-c1.txt` ends
`selftest: 15/15 passed`, exit 0 — a green and at least one mutant per item (13 fixtures at the
freeze; R80-4 already carried two mutants, the floor and a drifted record) plus amendment 1's
`r80-4-empty-seat-excluded` (green) and `r80-4-empty-seat-counted-opens` (mutant). Kill rule: a base or junk control that reads `met=true` means the counter is
wrong and the claim is not scored.

**C2 — operability: a fresh domain capture feeds the offline audit chain and the verdict
re-derives from committed bytes.** Frozen predicate:

    met <=> the manifest's checks are exactly the surfaces declared in
              `.ufo/waves/round-81/capture-expectations.json` (same ids, same urls,
              same expect objects, same allowlist)
          and every receipt verifies (sha256 of the retained body, byte count, integer status
              in 100..599, RFC 3339 fetch time on or after 2026-11-04T00:00:00Z, GET, not
              truncated, url identical to the declared url, finalUrl https on an allowlisted host)
          and header_audit over the committed manifest exits 0 or 1 with `checks=<surfaces>`
          and the audit's stdout equals the committed audit receipt byte-for-byte
              (after removing one trailing newline from each side)

Counter `python3 -B .ufo/waves/round-81/c81_capture_audit.py --root <tree> [--revision <rev>]
[--work <dir>]`, offline by construction and able to evaluate an exported revision;
`controls/c81-selftest-c2.txt` ends `selftest: 18/18 passed`, exit 0 (one green fixture and nine
mutants: body digest, byte count, stale fetch time, drifted audit receipt, manifest url drift,
manifest expect drift, a dropped declared surface, an empty declaration, and their audit runs).
Base control `controls/base-c81-capture-audit.txt` reads
`C2v1 revision=2e119255… declared=0 surfaces=0 failures=1 met=false`, exit 1; the tampered control
`controls/ctl-c81-tampered-capture.txt` is the real capture with byte 0 of
`capture/ds4cc-primary/body.bin` flipped (`0x3c` → `0x3d`) and reads
`body sha256 d1220935… != receipt f2c5d2b3… … met=false`, exit 1.
The declared expectations are frozen at `.ufo/waves/round-81/capture-expectations.json`
(allowlist `ds4cc.com`, `www.ds4cc.com`; three surfaces `/`, `/robots.txt`, `/sitemap.xml`;
classes grounded in S430–S433 and the new S454 row) and are the lane's *policy*, never a claim
that the property satisfies them — a finding is the audit's output. Kill rule: a base or
tampered control that reads `met=true` means the counter is wrong.

Amendment 2 (below) tightened four terms to the sentence above before the capture existed: the
manifest must equal the frozen declaration rather than assert its own expectations, `--revision`
exists so "committed bytes" is measurable at a revision, the audit comparison is byte-exact, and
a receipt's `url` must equal the declared url with `finalUrl` https on an allowlisted host.

## Corrections

The three rows below are the correction of round-80's filed bytes, by append: round-80's report
and lesson are not rewritten.

```
$ grep -n '^| S453 ' /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
200:| S453 | RFC 9110: HTTP Semantics, §5.6.7 Date/Time Formats — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | …
exit=0
```

R80-1 — citation: the S453 row sits at corpus/SOURCES.md:200 for S453, not at `:201` as the round-80 report and lesson wrote (line 201 is blank; `## Paths` starts at 202), so the round-80 pointers are corrected here by append and the counter re-derives the line itself, opening this item again if the row ever moves.

R80-2 — numeric accuracy: `.ufo/waves/round-80/controls/ctl-c80-constants.txt` parses to `const_all.py 12/12`, `const_clean.py 12/12`, `const_echo.py 11/12`, `const_regex.py 12/12`, i.e. `12+12+11+12 = 47` case-level failures over `12+12+12+12 = 48` slots, with the summary line `ctl constants_failed=4/4 cases=12` and `const_echo 11/12`; the round-80 sentence "fail 12/12 each" is therefore wrong only for `const_echo`, and the corrected tokens are constants_failed=4/4, 47/48, 11/12 — the frozen criterion ("each must fail at least one case") held at 4/4, so no C2 predicate moves.

R80-3 — corpus count/scope prose: counting every registry row whose `source` cell holds the URL token gives rfc9110.txt rows=4 (S028, S033, S453 and this round's S454, inserted directly after S453 so no earlier row moves; the count was 3 at the base) and rfc9110.html rows=3 (S010, S088, S433), so round-80's "a URL the registry already holds five times … a second scope" was wrong twice over — S453 was the third `.txt` scope before this round's S454 made it the fourth, and the five-row count mixed the two URL forms; the counter recomputes both counts at the measured revision, so this row follows the registry rather than the other way round.

**R80-4 — wave accounting.** Closes when round 81's own settled attack share, over the four
directive roles and counting only seats whose output is non-empty, reaches ≥ 0.25, and when
`w1-accounting.json` re-derives from `w1-spec.json` (sha256 included) + `w1-results.json` on
`attack_roles`, requested/settled totals and the share. The readings come from those three
committed files, not from any sentence in a report; `make_accounting.py` writes the record and
`c81_defect_queue.py`'s `p_r80_4` decides it. Amendment 1 (below) made the counter's population
equal the contract's before any after-state existed.

**R80-5 — evidence reproducibility.** Closes when `junk_tree_build.py` materialises round-80's
junk control tree twice from `junk-tree.json` with identical file sets and digests and round-80's
own counter over the rebuilt tree prints `open=5 closed=1 met=false`, exit 1. The reading is the
rebuilt tree's own bytes plus that counter's stdout; the builder's two runs are compared by a
path-and-content digest, so a builder that is deterministic only in file names fails.

**R80-6 — residual R79-8.** Closes when `scripts/wave_seat_record.py` re-derives
`seat-failures.json` from `w1-results.json` + `w1-spec.json`, the committed file equals that
re-derivation canonically, every seat carries `role`, `status`, `exit` and `error`, and the
record names the results-schema limit (that a results file which never carried an error text
cannot yield one). The reading is the re-run plus a byte comparison; a hand-edited record
differs.

## Gate

**Admit S454** — RFC 9110, *HTTP Semantics*, §15.5.5 *404 Not Found* and §15.5.11 *410 Gone*,
`https://www.rfc-editor.org/rfc/rfc9110.txt`. Access 2026-11-04T11:46:55Z, HTTP 200, final URL
identical to the request URL, 502,941 bytes, sha256
`21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, retained at
`corpus/lessons/round-81-gate/rfc9110.txt`. Command and exit code:

```
$ curl -sS --max-time 120 -L --compressed -A 'kake-round81-gate/1' -o …/rfc9110.txt -D …
  -w '%{http_code} %{size_download} %{url_effective}' https://www.rfc-editor.org/rfc/rfc9110.txt
200 139493 https://www.rfc-editor.org/rfc/rfc9110.txt
exit=0
```

The digest equals the one the lane already holds for this document (S028's `21c1cdce…7232a`,
S453's round-80 retained text), and the sources seat's independent GET at 11:46:19Z returned the
same 502,941 bytes and the same digest (`w1/ScoutSources.md` §1), so body identity rests on two
fetches, not one. Admission quote, retained text `:7593`, 9 words, match class **raw-substring**
(the span is in the bytes; verified `raw: True`, `:7593`):

> the 410 (Gone) status code is preferred over 404

The definitional spans are located but **collapsed-only** (each wraps at 72 columns, so the raw
span is not a substring while the whitespace-collapsed span is; both digests and both classes
were re-derived, `w1/ScribeLesson/receipts/quote-spans.txt`): `:7589-7590`, 21 words, "The 404
(Not Found) status code indicates that the origin server did not find a current representation for
the target resource", and `:7669-7670`, 20 words, "The 410 (Gone) status code indicates that
access to the target resource is no longer available at the origin server".

Tier A: Standards Track document, definitional status-code semantics. Scope: the
absence/permanence reading of a captured 404 or 410 — that a 404 does not settle whether the
lack of representation is temporary or permanent and that 410 is preferred when the origin server
knows it is; *not* a header-expectation class, *not* robots.txt semantics, *not* crawler
behaviour, *not* evidence that any surface is currently absent. Proposed registry row (this seat
writes no registry byte; the row is inserted **after line 200**, so R80-1's `:200` pointer does
not move):

```
| S454 | RFC 9110: HTTP Semantics, §15.5.5 404 Not Found and §15.5.11 410 Gone — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | <scope above> | §15.5.5 lines 7587-7596 (definition 7589-7590; permanence 7592-7595) and §15.5.11 lines 7667-7675 (definition 7669-7670); June 2022; HTTP 200 at 2026-11-04T11:46:55Z, retained text sha256 21c1cdce…47232a | <teaches: the absence/permanence reading> | mined | 2026-11-04 | 365d | corpus/knowledge/response-header-expectations.md, corpus/lessons/round-81.md |
```

Shape-tested on a scratch copy at the measured line position:
`scripts/sources-census.sh validate --root …/kake-shokunin --file <scratch>/SOURCES-inserted.md`
prints `file W04 S454 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes`, exit 1 —
the duplicate-URL *warning* the lane already carries 20 times, not an error. The sources seat's
own row text is congruent (`w1/ScoutSources.md` §5a: same id, same two anchors, its line ranges
`7587-7599` / `7667-7688` are supersets of the ranges verified here); the registry seat should
insert ONE row, and the differences are range width, not address. The same run also
prints 252 `E11` lines naming `used-by` paths that exist (`corpus/knowledge/ghp-served-set.md`
among them) on an **unmodified** copy of the registry, while the lane's own control
`controls/census-before.txt` exits 0 with no `E11`: `--file` mode resolves `used-by` against the
wrong root, so only its `E12`/`W04` verdicts are usable and this row's placement is what it
measures. **Overlap, stated not hidden:** S088's scope cell already names 404 and 410
(`corpus/SOURCES.md:96`), so S454 is a duplicate-section admit narrowed to the reading S088 does
not use (S088's `teaches` is entirely 3xx and `Location`); S088 stays untouched, and if a later
census treats section overlap as fatal, S454 is the row to withdraw.

**Reject — §15.5.4 as an absent-resource anchor.** The contract and
`capture-expectations.json` both cite "§15.5.4/§15.5.5"; `rfc9110.txt:7569` is
`15.5.4.  403 Forbidden`, and its sentence at `:7571-7572` (17 words, collapsed-only) is
"The 403 (Forbidden) status code indicates that the server understood the request but refuses to
fulfill it" — a client-error authorisation statement, with nothing about an absent target. The
anchor is refused; the admitted row takes §15.5.5 + §15.5.11. The frozen expectations file's
prose is not edited this round; `amendments/amendment-1.md` and this section carry the
correction.

**Reject — the `merge/kake` staged package**, restated and unchanged: 8 id collisions
(S312, S329, S367, S372, S373, S374, S390, S409) and 27 staged URLs the registry already holds
(`.ufo/waves/round-80/w1/ConnectorC/collision.out`: `id_collisions 8`, `staged_urls_held 27`,
`consistent true`). Adoption stays closed; nothing in this round's work makes it safer.

**Re-open S433** — `https://www.rfc-editor.org/rfc/rfc9110.html`, access
2026-11-04T11:46:56Z, HTTP 200, final URL identical, 1,187,554 bytes, sha256
`d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5`, which is byte-identical to
the lane's round-61 retained `S433.html` (`sha256sum .ufo/waves/round-61/sources/S433.html`
prints the same digest, exit 0) — so the body S433's `teaches` rests on has not drifted in eight
days. Located quote, retained text `:4039-4040`, 17 words, collapsed-only:

> Fields that only anticipate a single member as the field value are referred to as "singleton fields"

Tier A, scope unchanged (Content-Type as a singleton field and the field-line combination rule).
Row changes for the registry seat, old → new: `recheck 180d → 2027-05-03` (the same 180-day
cadence re-anchored to this access date, in the registry's absolute-date style), and `used-by
corpus/knowledge/response-header-expectations.md → corpus/knowledge/response-header-expectations.md,
corpus/lessons/round-81.md`. These are the sources seat's cell-level proposal
(`w1/ScoutSources.md` §5b); `opened`, `anchor`, `teaches`, `status` and `tier` do not move. The
second body fetched this round (`corpus/lessons/round-81-gate/rfc9110.html`) is retained with its
digest so the recomputation needs no network.

One citing-file defect is **not** fixed here: `corpus/knowledge/response-header-expectations.md:115-116`
labels the "generate multiple field lines with the same name" sentence `[S433 §5.2]`, but that
sentence is §5.3 Field Order (`rfc9110.txt:1529-1536`); §5.2 ends at `:1514`. Per
`corpus/QUALITY.md:1116` a locator must point at the section containing its quote, so the label is
drift — in the entry, not in S433's row — and it belongs to the knowledge seat, which this seat
does not edit.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| **a selftest that cannot run is indistinguishable from a property that cannot pass** | the first `c81_defect_queue.py --selftest` at the freeze: `SUMMARY_RE` lacked `re.MULTILINE` so the summary line never matched, one fixture's `cwd` was passed to `subprocess` before it existed, and one green line cited registry `:5` for an `S453` row at `:6` — three fixtures that read as red conjuncts | nothing in the lane: `corpus/lessons/round-80.md` names the mirror class (an unsatisfiable conjunct) but no rule required a fixture to be shown able to run green before its red counted | every fixture is scored green-first in the same receipt, and the receipt lists the green cases: `controls/c81-selftest-c1.txt` carries one `ok` line per fixture and `selftest: 13/13 passed` before amendment 1, `15/15` after. Can fail: it did — three fixtures were repaired before the first 13/13 |
| **a locator that names the section above its quote** | my first span probe printed `txt/s454-404 span=(7584, 7590)` for a sentence that begins at `rfc9110.txt:7589`; `:7584` is the tail of the §15.5.4 403 body (`forbidden target resource MAY instead respond with a status code of`) | `corpus/QUALITY.md:1116` — "a source locator points to the section containing its quote" — a rule the probe did not encode: it accepted any ≤7-line window and returned the first starting line | tightest-span search, so the 404 sentence resolves to `7589-7590` and the 410 sentence to `7669-7670`. Can fail: force the window to start at the heading (`7587`) and it returns `7587-7590`, which the assertion `span[0] == 7589` rejects; the rejected answer is the one the first probe produced |
| **the instrument's population is not the predicate's population** | contract §C1 ("a seat whose output is empty does not count as settled") and `.ufo/waves/round-81/make_accounting.py:35-37` against `c81_defect_queue.py:198-200` before amendment 1, where `settled` took every results row; probe on one synthetic empty seat: the builder printed `requested 3/6 settled 2/5 share=0.400 met=true` (exit 0) while the counter's formula gave `3/6 share=0.500`, `agreement: False` | the rule amendment 1 states after the fact: the population sentence must appear in the contract, the builder and the counter as the same words — it appeared in two of three | `p_r80_4` now selects settled seats by non-empty output (`c81_defect_queue.py:198-201`), selftest `15/15` with `r80-4-empty-seat-excluded` green and `r80-4-empty-seat-counted-opens` red; the base and junk receipts re-ran byte-identical (`2346b4d6…`, `b03b3097…`), only `controls/c81-selftest-c1.txt` changed and is disclosed in `.ufo/waves/round-58/receipt-rewrites.json` (`kind=content`). Can fail: the mutant counts the empty seat as settled and the item opens |

## Limits

- **C2 decides the chain, not the property.** Three surfaces of one property at one instant, one
  GET each, no cookies, no body: the claim is that receipt digests, byte counts, fetch time, the
  allowlist and the audit output re-derive from committed bytes — not that `ds4cc.com` conforms to
  any expectation class, not that a later change would be detected, and not any per-bot
  behaviour. A finding line is the audit's output, not a verdict about the site.
- **S454's scope is narrowed against S088, deliberately.** S088's scope sentence names 404 and
  410 (`corpus/SOURCES.md:96`); S454 holds only the absence/permanence reading. The census
  reports a duplicate-URL warning for the row, which the lane tolerates elsewhere. If section
  overlap is later ruled fatal, S454 is the row to withdraw — not S088.
- **The frozen expectations prose keeps a wrong anchor.** `capture-expectations.json`'s
  `grounding.status` still reads "§15.5.4/§15.5.5"; it is frozen and is not edited. The
  correction lives in `amendments/amendment-1.md`, the Gate above and the round report, so a
  reader must take the anchor from the registry row, not from that file.
- **No registry byte is written here.** The S454 row and the S433 `used-by` append are recorded
  for the registry seat; the `W04` line above is what a scratch copy emits, not a lane census
  result, and `--file` mode's `E11` lines are an artefact of its used-by root, demonstrated on an
  unmodified copy.
- **Round-80's filed bytes stand as filed.** These corrections are append-only; the report and
  lesson keep their sentences and the counter, not this file, decides the items.
- **R80-5 does not make the junk tree right.** The builder's determinism and round-80's
  `open=5 closed=1` show the tree is reproducible, not that its one closed item is closed for a
  good reason: round-80's R79-5 conjunct is textual and a fabricated withdrawal satisfies it.
  That is round-80's stated limit, restated here, not repaired.
- **R80-6 records what the schema carries.** A results file that never held an error text cannot
  yield one; the record names that limit (`schema_limit`) instead of reconstructing a cause, so a
  dead seat's message is whatever the dispatcher wrote, and nothing more.
- **Held, not measured.** Freshness 10 is untouched; no scalar score is asserted; no property
  beyond the three C2 surfaces was fetched by this seat (two RFC GETs only).

## Settlement (appended 2026-11-04)

Authored before the carrier: at the time of writing, `w1-results.json`, `w1-accounting.json`,
`seat-failures.json` and `capture/manifest.json` did not exist, so the sections above cite only
bytes that existed when they were written — the freeze commit, the round-80 receipts, the two RFC
bodies retained under `corpus/lessons/round-81-gate/`, the scratch census copy and amendment 1.
No C1 or C2 after-value is claimed here. The receipts that decide them at the carrier are
`controls/after-c81-defect-queue.txt` (six per-item lines plus `C1v1 … open=? closed=? met=?`)
and `controls/after-c81-capture-audit.txt` (`C2v1 … surfaces=? failures=? audit_rc=? met=?`
plus the audit's own `checks=<n> findings=<k>` line), and the three correction rows in
`## Corrections` are already decided from committed bytes (the counter's three predicates return
`(True, …)` over this file at the current working tree, exit 0).
