# ReviewerC1Predicate — frozen C1 sentence vs counter PREDICATE vs receipt label

Scope: compare the frozen C1 predicate sentence in
`.ufo/waves/round-54/contract.md` (lines 27–28) with the `PREDICATE` constant in
`.ufo/waves/round-54/c54_s374_calib.py` (line 40) and the receipt output label.
Read-only; no edits. Counter revision reviewed: committed `8e408e0` worktree copy
(9776 bytes; the file advanced from an earlier worktree snapshot mid-review —
final numbers below are from current committed bytes).

## Byte-level drift — YES (one byte: trailing `.`)

Canonical (contract.md L27–28, `**` span, wrap whitespace joined):

    S374 qualifier: mismatches = rendered cells missing the crawl qualifier and
    not superseded by an r54 correction block; met when 0.
    sha256 = a9be3a031d876e3f1c2de49c8702b91365f9ed1666156e48b8d582c6922ffb26  (130 chars)

`PREDICATE` (c54_s374_calib.py:40):

    S374 qualifier: mismatches = rendered cells missing the crawl qualifier and not superseded by an r54 correction block; met when 0
    sha256 = 59c4ba0afedeb0f192560349210e8418b1ed94e364a714af7b048b824364a831  (129 chars)

- Common prefix = all 129 chars; the contract bold span ends `…met when 0.` —
  one extra byte `0x2E` (`.`). `contract.rstrip(".") == PREDICATE` → True.
- Receipt label: `print(PREDICATE)` at line 213 emits the 129-char string, so
  every runtime label (and `--predicate` at line 204) carries no final period.
  Verified live: base run prints the 129-char line, `sha256` of
  `--predicate` output = `232783c78e…` (129 bytes + newline).
- Committed receipt `controls/base-c1-s374.txt:7` and peer captures
  (`w1/ExecC1Base.md:20`, `w1/ReviewerC1Noop.md:22`, `w1/CriticC1Control.md:34`)
  all carry the 129-char form.
- Same file, third form: the docstring copy (L6–7) ends `…met when 0.` —
  WITH the period, matching the contract. So the file carries both forms.
- Contract L5–6 promises "the same sentence in the plan, in the counter's
  code, and in every receipt label." Verdict: the contract and docstring agree
  byte-for-byte; `PREDICATE` and all receipt labels drift by exactly one byte
  (missing terminal period). Semantic content identical.

## Predicate-implementation drift (semantic, not byte-level)

1. `met` is stricter than the frozen sentence (internal contradiction).
   Frozen: "met when 0". Code line 111:
   `met = quote_ok and corr_ok and mismatch == 0`. `corr_ok` (a valid
   correction block exists) and `quote_ok` (source-body pin, C1.1) are
   extra conjunctions. Docstring L28 itself restates this: "met iff
   mismatch == 0 AND at least one valid correction block exists" — the
   counter's own docstring and the frozen sentence disagree. A suspect-free
   file with zero correction blocks yields mismatch=0 → sentence reads met,
   counter returns exit 1. (Benign direction — stricter, repair-required —
   but it is drift from the literal frozen text.)

2. "Rendered cells missing the crawl qualifier" is narrowed. Code (L62–66):
   a cell is suspect only if it ALSO matches endorsement/refusal vocabulary
   `recommend|vouch|endorse|refusal|refuse` (L45) AND lacks `crawl|巡回`
   (L46). A rendered cell missing the crawl qualifier but phrased neutrally
   (no endorsement vocabulary) is never counted — the frozen sentence counts
   it. Matches the "Before" gloss in the contract (which does name the
   endorsement vocabulary), but the sentence alone is broader.

3. Correction-block validity is narrower than "an r54 correction block."
   `qualifier_findings` (L67–72): literal mark `[r54-correction 2026-10-25]`
   anywhere (not line-anchored despite docstring "line starting with"),
   then a fixed 1200-char window must contain the exact QUOTE AND
   `NEGATIVE_CRAWL_RE` = `\bnot\s+recommend(?:\s+the)?\s+(?:crawl|crawling)\b`
   (L47). A block asserting the qualifier in any other phrasing — "does not
   recommend crawling", "does not endorse the crawl", "site does not
   recommend the crawl" — is NOT supersession-eligible → false not-met.
   (selftest fixtures happen to use the matching phrasing; not exercised.)

4. "Superseded" = purely positional. mismatch counts suspects strictly
   after the first valid block (`corr_at < pos`, L107). Nothing binds the
   block to the specific cell beyond file order; consistent with the
   appended-repair reading, weaker than referential supersession.

5. Docstring C1.4 (L25–26) states mismatches are suspect cells "BEFORE any
   valid correction block" — inverted relative to the committed code
   (`corr_at < pos`) and the append-supersession rule. The corrected code is
   right per contract "appended, never rewritten"; the docstring is stale.
   Also note the frozen sentence is silent on which direction counts.

## Receipt-format drift (secondary, not the predicate line)

`controls/base-c1-s374.txt` check lines use a flat format
(`PASS C1.1_body: occurrences=1`, `FAIL C1.4_mismatch: mismatches=1`), but the
landed counter prints `  PASS C1.1_body: [] {'occurrences': 1}` /
`  FAIL C1.4_mismatch: ['mismatches=1'] {'mismatches': 1}` (verified live at
base `68228b2d…`, rc=1). The receipt's predicate label, `mismatches=1 met=False`,
and `EXIT=1` all match; only the per-check line rendering differs → receipt was
committed from an earlier counter revision (or normalized). Predicate-label
claim unaffected; per-line format is not byte-faithful to the landed tool.

## Findings summary

- F1 (low, confirmed): one-byte drift — terminal `.` present in contract +
  docstring, absent in `PREDICATE` + all emitted receipt labels.
- F2 (low–medium): `met` conjoined with `corr_ok`/`quote_ok`; counter's own
  docstring restates a different predicate than the frozen sentence.
- F3 (low): suspect-cell and correction-validity definitions both narrower
  than the frozen sentence's literal span (neutral cells uncounted;
  non-"not recommend" crawl assertions rejected; 1200-char window;
  mark not line-anchored).
- F4 (low): docstring C1.4 before/after wording inverted vs committed logic.
- F5 (informational): committed base receipt's check-line format is stale vs
  the landed printer; label/summary lines agree.

No tool installs performed (none needed). No writes beyond this report.
