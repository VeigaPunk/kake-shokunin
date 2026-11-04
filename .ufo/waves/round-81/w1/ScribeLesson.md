# ScribeLesson — round 81 (kake, attempt 1)

**Verdict: the round-81 lesson is written at `corpus/lessons/round-81.md` and its three C1 rows
parse green; S454 is admitted with corrected anchors (§15.5.5 + §15.5.11), §15.5.4 is refused as an
absent-resource anchor, and S433 is re-opened on a byte-identical body. No C1/C2 after-value is
claimed: the wave had not settled when this seat finished.**

## What was produced

| Path | What it is |
|---|---|
| `corpus/lessons/round-81.md` | the lesson, 20,815 B, sha256 `68cc115521673d2f74fc34595d850186707e67787ebc318a52084c3ffb528372`; the only production file this seat wrote |
| `corpus/lessons/round-81-gate/rfc9110.txt` | retained GET body, 502,941 B, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` |
| `corpus/lessons/round-81-gate/rfc9110.html` | retained GET body, 1,187,554 B, sha256 `d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5` |
| `.ufo/waves/round-81/w1/ScribeLesson/receipts/` | `accounting-probe.txt`, `counter-formula-probe.txt` (both cited by `amendments/amendment-1.md`), `quote-spans.txt`, `census-proposed.out`, `census-file-mode-artefact.out`, `SOURCES-inserted.md` |

## Gates run (commands verbatim, exit codes observed)

1. `grep -n '^| S453 ' /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` →
   `200:| S453 | RFC 9110: HTTP Semantics, §5.6.7 …`, **exit 0**. Row `R80-1` names
   `corpus/SOURCES.md:200`.
2. Constants arithmetic re-parsed from `.ufo/waves/round-80/controls/ctl-c80-constants.txt`
   (`CONST_RE`/`SUMMARY_RE` as the counter defines them): per-constant `12/12, 12/12, 11/12,
   12/12` → `47/48`; summary `constants_failed=4/4`; `const_echo.py 11/12`. **exit 0.**
3. Registry URL-token count over `source` cells: `rfc9110.txt` → `3` (S028, S033, S453);
   `rfc9110.html` → `3` (S010, S088, S433). **exit 0.**
4. The counter's own three predicates over my file, by importing the module and calling
   `p_r80_1`/`p_r80_2`/`p_r80_3` at the working tree:
   `(True, 'R80-1 correction names corpus/SOURCES.md:200; S453 is on that line')`,
   `(True, 'R80-2 correction re-derives constants_failed=4/4, 47/48, 11/12 over 4 constants')`,
   `(True, 'R80-3 correction re-derives rfc9110.txt rows=3 and rfc9110.html rows=3 (…)')`.
   **exit 0.** I did not run the counter end to end: `w1-results.json` and `w1-accounting.json`
   did not exist, so R80-4/5/6 had no after-state to read.
5. Two GETs, one per URL, `curl -sS --max-time 120 -L --compressed -A 'kake-round81-gate/1'`:
   `.txt` → `200 139493 https://www.rfc-editor.org/rfc/rfc9110.txt` at 2026-11-04T11:46:55Z,
   **rc=0**; `.html` → `200 212574 https://www.rfc-editor.org/rfc/rfc9110.html` at
   2026-11-04T11:46:56Z, **rc=0**. Final URLs identical to the requests (`%{url_effective}`).
6. `sha256sum .ufo/waves/round-61/sources/S433.html corpus/lessons/round-81-gate/rfc9110.html`
   → identical digest `d4317606…368fe1e5`, **exit 0**: S433's retained body has not drifted.
7. Quote truth, spans on the retained bytes (`receipts/quote-spans.txt`): 404 sentence 21 words
   `:7589-7590`; 410 sentence 20 words `:7669-7670`; 403 sentence 17 words `:7571-7572`; S433
   singleton sentence 17 words `:4039-4040`. All four are **collapsed-only** (not raw
   substrings — each wraps), and the class is stated in the lesson rather than asserted as raw.
   **exit 0.**
8. Census shape test on a scratch copy with the proposed row inserted after line 200:
   `scripts/sources-census.sh validate --root …/kake-shokunin --file <scratch>/SOURCES-inserted.md`
   → `file W04 S454 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes`, **exit 1**
   (warning line present, no `E12`, i.e. the row is inside the Registry section at that
   position). Lane control `.ufo/waves/round-81/controls/census-before.txt` reads `kake ok …`
   with 20 `W04` lines, **exit 0**.

## Findings

1. **S454's section pointer is wrong in two frozen files** — `contract.md` §Sources and
   `capture-expectations.json` `grounding.status` both say "§15.5.4/§15.5.5".
   `corpus/lessons/round-81-gate/rfc9110.txt:7569` is `15.5.4.  403 Forbidden`; 404 is `:7587`
   and 410 is `:7667`. Closed by `amendments/amendment-1.md` (A2), by the lesson's Gate (the
   anchor is refused with the 403 sentence and line numbers), and by anchoring S454 at
   §15.5.5 + §15.5.11. No mechanical effect on C2: `scripts/header_audit.py` never reads status
   semantics. Severity low, decision recorded.
2. **S454 overlaps S088.** `corpus/SOURCES.md:96` (S088) already names "404 Not Found and 410
   Gone" in its scope, anchored at §15.5.5/§15.5.11 of the `.html` form. The admitted row is
   narrowed to the absence/permanence reading that S088's `teaches` (all 3xx/Location) does not
   use, cross-references S088, and emits a duplicate-URL `W04` — measured, not assumed. The
   lesson states that if section overlap is later ruled fatal, S454 is the row to withdraw.
3. **`scripts/sources-census.sh --file` resolves `used-by` against the wrong root** — on an
   **unmodified** copy of the registry it prints 252 `E11` lines naming files that exist
   (`file E11 S001 missing used-by corpus/knowledge/ghp-served-set.md`), exit 1, while the same
   registry through the lane path exits 0 with no `E11`
   (`receipts/census-file-mode-artefact.out` vs `controls/census-before.txt`). Consequence: only
   the mode's `E12`/`W04` verdicts are usable. Routed, not fixed — the script is fleet-level and
   outside this seat's write scope.
4. **R80-4's counter counted a different population than the contract** (found by this seat
   from bytes before any after-state; probe: builder `settled 2/5 share=0.400` vs counter formula
   `3/6 share=0.500`, `agreement: False`). Reported to the L1 by id; closed by
   `amendments/amendment-1.md` A1, with `p_r80_4` now filtering non-empty output
   (`c81_defect_queue.py:198-201`) and the selftest at `15/15`
   (`controls/c81-selftest-c1.txt`), including `r80-4-empty-seat-excluded` and
   `r80-4-empty-seat-counted-opens`. The base and junk control receipts re-ran byte-identical
   (`2346b4d6…`, `b03b3097…`); only the selftest receipt was re-cut, and it is disclosed in
   `.ufo/waves/round-58/receipt-rewrites.json` (`kind=content`).
5. **Round-80's filed prose keeps three wrong numbers** — `:201` for S453 (it is `:200`),
   "12/12 each" for the constants (const_echo is `11/12`), and "held five times … a second scope"
   for the URL census (3 `.txt` scopes, 3 `.html` scopes). Corrected by append only; no filed
   byte rewritten.
6. **A citing-file locator drift, found by ScoutSources and verified here.**
   `corpus/knowledge/response-header-expectations.md:115-116` labels the "generate multiple field
   lines with the same name" sentence `[S433 §5.2]`, but that sentence is §5.3 Field Order
   (`rfc9110.txt:1529-1536`; §5.2 ends at `:1514`). `corpus/QUALITY.md:1116` requires a locator to
   point at the section containing its quote. Not fixed by this seat (the entry belongs to the
   knowledge seat); S433's own `anchor` cell still supports the combination rule and the
   Content-Type singleton rule, so the row is not withdrawn.

## Reconciliation with ScoutSources

`w1/ScoutSources.md` existed when this seat finished, so its receipts were read and reconciled
rather than duplicated:

- **Agreement on bodies.** Its GETs at 2026-11-04T11:46:19Z returned the same 502,941 B /
  `21c1cdce…` and 1,187,554 B / `d4317606…` as this seat's at 11:46:55Z/11:46:56Z — two
  independent fetches, one body pair.
- **Agreement on the anchor defect.** Its F1 and this seat's finding 1 are the same defect,
  reached independently; its S454 proposal cites §15.5.5 + §15.5.11.
- **One change adopted.** Its Q3 — "the 410 (Gone) status code is preferred over 404", 9 words,
  `:7593` — is a **raw substring**, so the lesson's admission quote is now Q3; this seat's Q1/Q4
  remain as located collapsed-only spans. Verified here: `raw: True`, `:7593`.
- **One change deferred to its proposal.** The S433 `recheck` old → new is recorded as
  `180d → 2027-05-03` (its absolute-date cell shape), replacing this seat's earlier
  `180d → 180d` phrasing; the cadence is unchanged either way.
- **No duplicate registry row.** The lesson tells the registry seat to insert ONE S454 row and
  notes the two proposals differ only in anchor line-range width (its `7587-7599`/`7667-7688` are
  supersets of the ranges verified here).

## Touched surfaces

- Wrote: `corpus/lessons/round-81.md`, `corpus/lessons/round-81-gate/rfc9110.txt`,
  `corpus/lessons/round-81-gate/rfc9110.html`, `.ufo/waves/round-81/w1/ScribeLesson/**`,
  this report.
- Read: the frozen contract and counters, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
  `corpus/knowledge/response-header-expectations.md`, round-80 controls and lesson,
  `.ufo/waves/round-80/verifier-spotcheck` §6, round-61 `S433.html`, `.ufo/waves/round-81/w1-spec.json`,
  `amendments/amendment-1.md`, `scripts/header_audit.py`, `scripts/sources-census.sh`.
- Not touched: `SOURCES.md`, any counter, any control receipt, any commit.

## Out of scope / not decided

- C1's R80-4/5/6 after-values and C2's whole after-value: the wave had not settled (no
  `w1-results.json`, `w1-accounting.json`, `seat-failures.json`, `capture/manifest.json`).
  The lesson says so in its Settlement section rather than guessing.
- The registry edit itself (S454 row, S433 `used-by` append): recorded for the registry seat,
  not written here — this seat's only production target is the lesson.
- Property-level conformance, per-bot behaviour, and any freshness claim about `ds4cc.com`.

## Tooling

No installs or upgrades. `curl` 8.23.0 pre-existing; Python 3 stdlib only. Network use: two GETs,
one per URL, no cookies, no credentials, no body.

## Scratch

`/fast/scratch/hyaku/kake-r81/ScribeLesson` (census copies, header dumps, probe trees) is deleted
before yield; the receipts that matter were copied to
`.ufo/waves/round-81/w1/ScribeLesson/receipts/` first.
