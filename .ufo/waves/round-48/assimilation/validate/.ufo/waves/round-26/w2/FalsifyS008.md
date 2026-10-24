# FalsifyS008 — round-26 C1 freshness attack on row S008 (verdict HOLD)

Scope: row S008 of `corpus/SOURCES.md:16` / `population.json` (GNU tar manual, "Controlling
Pattern-Matching"), receipt `.ufo/waves/round-26/rechecks/S008.json` (verdict HOLD). I tried to
show the HOLD is wrong on the freshness axis: (a) the quote does not ground this row's `teaches`,
(b) the anchor observed is not what the raw bytes say, (c) the content/version changed under the
receipt, (d) the row's own anchor is wrong. All four attacks failed. One low-severity wording
defect is reported; it does not change the verdict.

## Verdict

**AGREE** with the row-level HOLD. The receipt's quote, anchor, byte digests and reason are
reproduced exactly from the retained bytes and from a live GET of the row URL.

## Evidence

### 1. Anchor observed is correct in the retained raw bytes

`fetched/S008-1-retry.raw.gz` → 512,359 bytes, sha256
`93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084` (matches
`fetched/manifest-retry.json` and the receipt's `reason`). 13,681 lines. Raw lines:

```
8478 @end menu
8480 @node controlling pattern-matching
8481 @unnumberedsubsec Controlling Pattern-Matching
8587 subsequence.  Default is @option{--no-anchored} for exclusion members
8588 and @option{--anchored} inclusion members.
8602 When wildcards match slash (the default for exclusion members), a
8603 wildcard like @samp{*} in the pattern can match a @samp{/} in the
8604 name.  Otherwise, @samp{/} is matched only by @samp{/}.
8617 @item Inclusion @tab @option{--no-wildcards --anchored --no-wildcards-match-slash}
8618 @item Exclusion @tab @option{--wildcards --no-anchored --wildcards-match-slash}
8619 @end multitable
```

Every location the receipt cites is exact: `@node` 8480, `@unnumberedsubsec` 8481, anchored-patterns
table 8579–8588, wildcard-slash item 8598–8604 with the quote at 8602–8604, summary table
8613–8619 with the Exclusion row at 8618. The receipt's quote is verbatim from 8602–8604
(terminating at "…in the name.").

### 2. The quote does ground this row's `teaches` (not page chrome, not a neighbouring clause)

Row `teaches`: "GNU tar exclusions are unanchored and wildcard matching can cross slash by
default, so patterns may apply to nested paths". Both conjuncts sit **inside the row's own cited
anchor range 8478–8617**:

* "unanchored" → raw 8587–8588: "Default is `--no-anchored` for exclusion members and
  `--anchored` inclusion members." (the receipt's `reason` cites 8587–8588 explicitly).
* "wildcard matching can cross slash by default" → the receipt's quote, raw 8602–8604.
* "so patterns may apply to nested paths" → 8586–8587 ("the pattern can match any subsequence")
  + 8602–8604 ("`*` … can match a `/`"), both in range.

The quote is not chrome: it is the body of the `--wildcards-match-slash` option item inside the
same `@table @option` that the section header names; it names "exclusion members" explicitly, so
it is scoped to this row's subject and not to inclusion members.

The quote is also row-specific under the amendment's rule: `grep -l "When wildcards match slash"
fetched/text/*.txt` → only `S008-1.txt`; the token/word budget holds (23 alphanumeric tokens,
23 whitespace words — limits are ≥6 and ≤25). Reproducing the counter's own check with the
committed `source_text.py` (module loaded from the worktree, raw decompressed in memory):

```
quote_in_text: True
committed text file identical to module output: False   ← only a trailing "\n" (503331 vs 503332)
```

so the committed retained view `fetched/text/S008-1.txt` is byte-equal to the helper output apart
from one trailing newline. Nothing is stale in the view.

### 3. No content/version change under the receipt

The row URL is commit-pinned, so drift would have to show up as a different blob. Plain GETs of
exactly the recorded URL (no other URL, nothing saved on disk, bytes hashed in memory) — two
requests to that same URL were made: one to read status/size, one to hash and re-locate the anchor
lines:

```
http_code=200 size=512359 url=https://cgit.git.savannah.gnu.org/cgit/tar.git/plain/doc/tar.texi?id=cfdb891bbd68c920ea75210977593f3cd08f0418
bytes 512359 sha256 93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084
```

Byte-identical to the retained bytes and to the sha recorded in the receipt, the retry manifest and
`population.json` (fetch index 1). The live GET also reproduces every anchor line above verbatim
(8480/8481/8587/8588/8602/8603/8604/8617/8618/8619). Corroborating internal evidence that the
pinned blob did not shift: the round-20 erratum in `corpus/knowledge/ghp-served-set.md:76-77`
cites "lines 8587–8588 and 8602" — exactly the lines the 2026-10-21 bytes carry.

Committed-at-candidate integrity (the counter reads these from the revision, not the worktree):
`git show e28312b:.../rechecks/S008.json` = the worktree receipt
(sha256 `9e39e7da3099c442b4789919b1690339d74d776050ab5bd4536b242c22efe6ab`);
`git show e28312b:.../fetched/S008-1-retry.raw.gz` decompresses to 512,359 bytes with sha256
`93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084`;
`manifest-retry.json` matches the worktree byte-for-byte. The failed attempt 1 is honestly
recorded as `TimeoutError`, 0 bytes, sha256 `e3b0c442…` (sha of empty) with a 20-byte gzip in
`fetched/S008-1.raw.gz`, and `population.json` pins the *retry* file as fetch index 1 — the
counter's `Checker.build_view` (`measure.py:303-305`) resolves the retry manifest over the base
entry and then re-verifies sha256 and file name against the population, so the S008 row is
decided against the real bytes, not against the empty first attempt.

### 4. Version semantics

`corpus/knowledge/ghp-served-set.md:34` still carries the label "GNU tar 1.35"; the round-20
erratum at `:73-79` withdraws it. The withdrawal is correct against today's bytes: the raw body
contains 0 occurrences of "1.35", 0 occurrences of "cfdb891" (commit identity rests on the fetch
URL), and 10 occurrences of `@value{VERSION}`. The row's own anchor cell says "GNU tar master
cfdb891bbd68c920ea75210977593f3cd08f0418" — a commit pin, not a release-version claim, so the
row itself carries no stale version statement.

## Findings

### F1 (low) — `anchorObserved` contains a literally false clause about its own range

`rechecks/S008.json` `anchorObserved` ends: "… summary defaults 8613-8619 — all inside the cited
8478-8617 range". 8618 and 8619 are **not** inside 8478–8617. The receipt's own `reason`
immediately discloses this ("only the anchor tail ends 2 lines before the subsection's closing
multitable"), and `w1/RowS008.md` and `w1/PairS008GhpServedSet.md` #12 already flag that
`SOURCES.md:16` / `population.json:197` anchor 8478–8617 omits raw 8618 (the one-line
"Exclusion → `--wildcards --no-anchored --wildcards-match-slash`" summary row).

Impact on the verdict: none. The teaches is grounded inside the cited range by 8587–8588 and
8602–8604; 8618 is corroboration, not the sole support. The clause is a wording defect in the
receipt prose, not a false anchor observation and not a content drift.

Minimal correction (optional, non-STALE, wording only — no corpus or row-cell change):

```
anchorObserved: "Controlling Pattern-Matching (@node line 8480, @unnumberedsubsec 8481, body to
8619); anchored-patterns table 8579-8588; wildcard-slash item 8598-8604 (quote at 8602-8604);
summary defaults 8613-8619 — the teaching lines 8587-8588 and 8602-8604 are inside the cited
8478-8617 range; the summary's Exclusion row (8618) and @end multitable (8619) lie just outside it"
```

Widening the SOURCES/population anchor to 8478–8619 is a separate editorial option; this wave's
contract restricts SOURCES row cells to status/recheck/used-by, so it is out of scope here and is
already recorded for L1 by `w1/PairS008GhpServedSet.md`.

No other finding. In particular, no content, version, attribution, quote-fidelity or scope defect
was found, and the row's `teaches`/`scope` need no correction.

## Residual risk and verification gaps

1. **"GNU tar master" label is unverifiable within lane bounds.** The row anchor labels commit
   `cfdb891…` as "master"; with only the pinned URL GET-able I cannot confirm it is still
   master's tip (a cgit log/tip URL is not a SOURCES.md documentation URL, so I did not fetch it).
   Impact is confined to the label's descriptive accuracy; the quoted bytes are commit-pinned and
   were verified byte-identical today, so the `teaches` cannot drift under this pin.
2. **No pre-2026-10-21 bytes are retained for S008**, so "no change" rests on (i) the pinned
   commit being immutable, (ii) the live GET matching the retained sha256, and (iii) the
   round-20 erratum's line numbers (8587–8588, 8602) still matching. No byte-level diff against
   the original 2026-10-19 fetch is possible.
3. **The retained view is a single physical line** (503,332 bytes, one LF), so the row's raw line
   anchors (8478–8617) are checkable only on the raw gzip, not on `fetched/text/S008-1.txt`. The
   receipt's `anchorObserved` line numbers are raw-based and are correct on the raw; the receipt's
   caveat says so.
4. **Release identity is not carried by the artifact.** `version.texi` is not retained, so "not
   release 1.35" is shown only by the absence of "1.35" in the body — adequate for the withdrawn
   label, but the tar release version of the pinned commit is not itself observable in the bytes.
5. **Statement-level repro not re-executed** (`ghp-served-set.md:43-51`, the local `mktemp` depth
   repro): out of bounds for this lane (writes under /tmp) and out of scope for the row verdict;
   the same gap is recorded in `w1/PairS008GhpServedSet.md` (statement #6). It does not bear on
   the row's `teaches`, which are document-grounded.
6. Attempt 1 of the fetch is a 20-byte gzip of empty content retained under
   `fetched/S008-1.raw.gz`; anyone re-deriving S008 bytes must take
   `fetched/S008-1-retry.raw.gz` (as `population.json` does) or they will hash an empty payload.

## Tooling

No tools installed, upgraded or removed. Python 3 standard library only (`gzip`, `hashlib`,
`json`, `re`, `importlib`), all in-memory; two `curl` GET requests, both of the single recorded row
URL (bytes piped to a hasher, never saved). No writes outside this report; no /tmp use; no builds,
tests or linters.

```json
{"target":"S008","verdict":"AGREE","severity":"low"}
```
