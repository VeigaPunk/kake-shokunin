# ScribeLOG — round-62 LOG.md evidence list

Seat: `ScribeLOG` (scribe, leaf; no subagent dispatch). Item: draft the round-62 `LOG.md` entry
and its evidence list for the calibration claim, the round-62 lesson and the opened S432 source;
keep measured after values blank pending the L1 run.

Advisory only. No lane file, Git/jj state, counter, criterion or score was written or altered.
No installs, no pacman. Scratch dir `/fast/scratch/hyaku/kake-r62/ScribeLOG/` was created and is
empty (removed before yield).

## 1. Verified base state (read-only; nothing rerun to decorate)

Lane root below is `/home/vgpnk/Projects/shokunin/kake-shokunin`.

| # | Check | Command | Observed |
|---|---|---|---|
| 1 | Lane base / worktree | `git -C <lane> rev-parse HEAD`; `git -C <lane> status --porcelain` | `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`; `?? .ufo/waves/round-62/` only |
| 2 | Frozen counter identity | `sha256sum .ufo/waves/round-62/c62_calibration.py` | `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d` (matches contract) |
| 3 | Unique verifier disagreement | `corpus/lessons/round-61-verifier-spotcheck.md:33` (48-line file) | one line with both `S432` and `Disagree`: `| S432 / Fetch | Admit | https://fetch.spec.whatwg.org/, §3.6; retained body … | Disagree | “Web developers and conformance checkers must use the following” is only a generic lead-in, not substantive evidence for a response-header expectation. Lesson itself identifies it as a generic lead-in. |` |
| 4 | Knowledge entry at base | `corpus/knowledge/response-header-expectations.md` (216 lines), §xcto at `:69-94` | `:75` already contains `S432 §3.6`; `:77` contains the fragment `can be used to require checking of a`; `:79` contains the verifier-rejected lead-in. Counter literal absent (`in` → `False`); token `Round-62 correction` absent |
| 5 | QUALITY at base | `corpus/QUALITY.md` (1408 lines) | `substantive located quote` count `0`; `round-61-verifier-spotcheck.md` count `0`; last criteria heading is `## Round-60 criteria` (`:1360`); no round-61 criteria section |
| 6 | Round-62 lesson | `ls corpus/lessons/round-62.md` | `No such file or directory` (counter's `lesson_gate` reads `""`) |
| 7 | S432 source row | `corpus/SOURCES.md:178`; row count | `| S432 | WHATWG Fetch — https://fetch.spec.whatwg.org/ | spec | A | X-Content-Type-Options nosniff value rule | … | mined | 2026-10-27 | 180d | corpus/knowledge/response-header-expectations.md |`; 171 rows matching `^\| S\d+ \|` |
| 8 | Retained S432 body | `sha256sum`; `stat -c %s`; `.ufo/waves/round-61/sources/receipts.json` | `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`, 1,854,393 bytes; receipt `S432` `status 200`, `fetchedAt 2026-10-27T09:14:55Z`, `userAgent round61`, same sha256 (a round-61 fetch, not a round-62 receipt) |
| 9 | Quote provenance | raw lines 6151–6154 of `.ufo/waves/round-61/sources/S432.html`; collapsed text | Nearest heading `6149: 3.6. \`X-Content-Type-Options\` header`. Collapsed §3.6 text: `` `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request. `` The counter literal (120 chars / 19 words, no backticks) occurs **0** times in the collapsed page text; the backticked form occurs **1** time; the sentence spans ≥8 inline nodes (`dfn`, `code`, `a`) |
| 10 | LOG.md target | `wc -l LOG.md`; `grep -c '^## Round 62' LOG.md` | 2249 lines; last heading `:2239 ## Round 61 — 2026-10-27 (attempt 1)`; no `## Round 62` heading yet — append at EOF |
| 11 | Wave shape | `.ufo/waves/round-62/w1-dispatch.json`; `w1/swarm-registry.json` | `counts.spawn=64`; 64 registry members: scout 16, executor 14, reviewer 14, scribe 8, critic 5, mutation-tester 4, connector 2, sentinel 1 |

**Base-control line (recorded before wave data, as carried in the wave context/`w1-spec.json`):**
`unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false`, exit 1.
The five component states above independently reproduce exactly that line from the base blobs
(1 disagreement; no quote/token; no criterion tokens; no lesson file; row present). The frozen
counter itself was not executed by this seat.

## 2. Draft LOG.md entry (append at EOF; after-state values left blank)

```markdown
## Round 62 — 2026-10-27 (attempt 1)

- **Claims frozen.** Base `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`; contract `.ufo/waves/round-62/contract.md`
  (one claim, C1 calibration — the lowest-scoring non-retired axis, score 2). Frozen C1 counter
  `.ufo/waves/round-62/c62_calibration.py`, sha256 `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`;
  no predicate change after any score.
- **C1 calibration.** Base control before wave data: `revision=c341a7a4… disagreements=1 unresolved=1
  quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false`, exit 1
  (`python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`).
  After, measured only at the integrated committed revision: ⟨pending L1 run — full counter line, exit
  code, measured revision⟩.
  - The counter re-derives four token states from committed blobs: `quote_correction` = the 120-char
    S432 §3.6 span (below, field names without the body's backtick markers) + `S432 §3.6` +
    `Round-62 correction` in `corpus/knowledge/response-header-expectations.md`; `criterion` =
    `substantive located quote` + `round-61-verifier-spotcheck.md` in `corpus/QUALITY.md`;
    `lesson_gate` = `## Gate` + `S432` + `Agree` + `Reject` in `corpus/lessons/round-62.md`;
    `source_row` = `| S432 |` in `corpus/SOURCES.md` (`.ufo/waves/round-62/c62_calibration.py:31-41`).
  - Stated limit: the counter does not mechanize "preserve the old knowledge prose, source row and
    verifier record"; preservation is shown by the append-only diff / `scripts/append_guard.py` and
    review, not by a counter state (see the seat finding in `.ufo/waves/round-62/w1/ScribeLOG.md`).
- **Sources & frontier.** S432 `https://fetch.spec.whatwg.org/` was re-opened this round
  (2026-10-27, HTTP 200, web reader) per contract § Source grounding; the retained committed body
  `.ufo/waves/round-61/sources/S432.html` (sha256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`,
  1,854,393 bytes) carries §3.6 `X-Content-Type-Options` header at source lines 6151–6154. Registry
  held at 171 rows: S432 (`corpus/SOURCES.md:178`, `mined`, used-by
  `corpus/knowledge/response-header-expectations.md`) is kept, not rejected and not edited; no new
  row, and no `status` / `recheck` / `used-by` change. Start census
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  → `kake\tok\t/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`, exit 0 (16 W04,
  including S433); end census: ⟨pending L1 run⟩. Assimilation: none.
- **Mistakes / lesson.** Class: a quote that is a generic lead-in was admitted as the grounding for a
  response-header policy; evidence `corpus/lessons/round-61-verifier-spotcheck.md:33`, the unique S432
  `Disagree` (discernment harmed, "an admitted row's quote does not ground its teaching"). Captured by
  the new QUALITY criterion; fix: a substantive located S432 §3.6 quote in an append-only
  `[r62-correction 2026-10-27]` run of `corpus/knowledge/response-header-expectations.md`, plus
  `corpus/QUALITY.md` ⟨pending L1: appended criterion text — must contain the literal
  `substantive located quote` and cite `corpus/lessons/round-61-verifier-spotcheck.md`⟩, plus
  `corpus/lessons/round-62.md` `## Mistakes` and `## Gate` (S432 URL, access date, ≤25-word located
  quote, Admit/Reject rationale, independent spot-check marked pending).
  Source quote for the correction (contract literal, 120 chars / 19 words, backtick markers dropped
  per the Gate note): "response header can be used to require checking of a response’s Content-Type
  header against the destination of a request."
- **Waves.** One v1 wave `w1`, 64 seats (scout 16, executor 14, reviewer 14, scribe 8, critic 5,
  mutation-tester 4, connector 2, sentinel 1; `.ufo/waves/round-62/w1-dispatch.json`
  `counts.spawn=64`); reports under `.ufo/waves/round-62/w1/`. ⟨pending L1: w1 report tally, dead
  seats, tools installed⟩.
```

Placeholders left blank on purpose (measured only by L1 after integration): after counter line,
after exit code, measured revision, end-census output/exit, appended criterion wording, wave tally,
score delta. Everything else above is grounded in §1.

## 3. Evidence checklist L1 must attach with the entry

1. **Base-control receipt, committed.** No `.ufo/waves/round-62/controls/` exists and the base-control
   line lives only in the contract/wave context; contract § Frozen controls says to record the
   committed base-control output before the wave. Persist it (e.g.
   `.ufo/waves/round-62/controls/base-c1-calibration.txt` with command + line + `exit 1`) and cite it
   in the C1 bullet. Until then the base number is a prompt assertion only.
2. **After measurement at a committed revision.** The counter reads `git show <rev>:<path>`
   (`.ufo/waves/round-62/c62_calibration.py:20`), so an uncommitted correction scores
   `quote_correction=0`. Commit the four surfaces, then run and paste the full line + exit code +
   revision into `.ufo/waves/round-62/controls/after-c1-calibration.txt`.
3. **Knowledge correction.** Append at EOF after `corpus/knowledge/response-header-expectations.md:216`
   (end-of-file runs need no tag, but the round-60 criterion requires the visible
   `[r62-correction 2026-10-27]` tag anyway), containing the exact counter literal and the literal
   words `Round-62 correction`; run
   `python3 -B scripts/append_guard.py --root . --base c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 --revision <after>`
   (default scope `corpus/knowledge/**/*.md`).
4. **QUALITY criterion.** Append under a new `## Round-62 criteria` heading after
   `corpus/QUALITY.md:1408`; must contain `substantive located quote` and
   `round-61-verifier-spotcheck.md` verbatim, with the round-61 verifier finding as grounding.
5. **Lesson.** Create `corpus/lessons/round-62.md` with `## Mistakes` (class · evidence pointer ·
   captured-by · fix) and a `## Gate` block that contains `S432`, `Agree`, `Reject` and the opened
   URL/date/quote; state the independent non-author spot-check as pending (dispatched seats are not
   non-author verification).
6. **Row preserved.** Evidence that `corpus/SOURCES.md:178` is byte-identical at base and after
   (the counter only tests presence of `| S432 |`), and that the verifier row
   `corpus/lessons/round-61-verifier-spotcheck.md:33` is untouched.
7. **Opened source.** Cite the contract line for the 2026-10-27 HTTP-200 re-open and the retained
   body sha256/lines; state plainly that the stored body and receipt (`receipts.json`, `round61`,
   `2026-10-27T09:14:55Z`) are the round-61 fetch, unless L1 records a round-62 fetch receipt under
   `.ufo/waves/round-62/sources/`.
8. **Census after.** Paste
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
   output + exit code (171 rows expected unchanged; W04 count unchanged at 16).
9. **Score delta pointer.** SCORECARD calibration row/score evidence at the measured commit; the
   contract forbids claiming calibration above its ceiling or that every corpus disagreement closed.

## 4. Findings (advisory; these change what the LOG may truthfully say)

- **F1 — the chosen quote is not a byte-literal page span.** The counter literal
  (`response header can be used to require checking of a response’s Content-Type header against the
  destination of a request`) occurs **0** times in the retained body's collapsed text; the body has
  literal backticks around `<code>Content-Type</code>` (raw lines 6151–6154), and the sentence spans
  `dfn`/`code`/`a` element boundaries. Copy the quote from `contract.md`/the counter constant, never
  from the HTML; the Gate must say the field names' backtick markers were dropped and must **not**
  claim the round-61 Gate's "one collapsed text node, page-unique" property. The 19-word / 120-char
  size does fit the round-61 6..25-unit / ≤160-char bound.
- **F2 — `Round-62 correction` is a second, distinct literal.** The correction tag
  `[r62-correction 2026-10-27]` does not satisfy it (`scripts/append_guard.py:45` tag regex vs
  `c62_calibration.py:33-34`). The appended run needs both.
- **F3 — preservation is unmechanized by c62.** `c62_calibration.py:31-41` counts the S432
  `Disagree` line, then forces `unresolved=0` whenever `resolved` is 1; it never compares base vs
  revision for the old knowledge prose, the source row's other cells, or the spot-check row. Do not
  write "the counter verified old-row preservation" in LOG/report; cite the append guard + diff.
- **F4 — `source_row` is presence-only.** Any `| S432 |` line passes, including a newly added one;
  the "kept, not rejected, no new row" claim needs its own byte-identity evidence.
- **F5 — no committed base-control receipt exists yet** (no `.ufo/waves/round-62/controls/`; the
  line is only in the contract/wave context). Item 1 above.
- **F6 — the round-62 S432 open has no round-62 receipt.** `receipts.json` records the round-61
  fetch; the only round-62 open evidence is contract § Source grounding. The LOG must attribute the
  open to the contract, not imply a new fetch receipt.
- **F7 — after-state must be committed before measuring** (`git show` reads blobs). Measuring the
  worktree is not possible with this counter.
- **F8 — the `lesson_gate` tokens are literal**: `## Gate`, `S432`, `Agree`, `Reject`; a Gate that
  only says "pending" and no Admit/Reject decisions keeps `lesson_gate=0`.
- **F9 — LOG placement**: append after `LOG.md:2249`; do not renumber or edit the round-61 entry.

## 5. Scope, tooling, cleanup

- Files read (read-only): `contract.md`, `c62_calibration.py`, `w1-dispatch.json`, `w1-spec.json`,
  `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
  `corpus/knowledge/response-header-expectations.md`, `corpus/lessons/round-61-verifier-spotcheck.md`,
  `corpus/lessons/round-61.md`, `.ufo/waves/round-61/sources/S432.html` + `receipts.json`,
  `scripts/append_guard.py`, `/home/vgpnk/Projects/shokunin/AXES.md` and
  `.ufo/prompts/kake-round-62.md`.
- Written: this report only. No lane Git/jj/index, fleet, sibling or source-tree writes; no
  counter, claim, criterion or score change; no counter execution.
- Tools installed: none; no pacman transactions; no PATH-directory writes.
- Scratch: `/fast/scratch/hyaku/kake-r62/ScribeLOG/` created empty and removed before yield.

Out of scope by design: after-value measurement, criterion/lesson/entry wording decisions, score
assignment, wave tally, and any lane commit — all L1's at integration.
