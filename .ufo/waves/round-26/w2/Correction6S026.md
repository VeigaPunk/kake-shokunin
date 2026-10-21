# Correction6S026: falsify the [r26-recheck S026 STALE] correction for line 69

Target: `corpus/knowledge/static-canonical-preflight.md:188` (candidate `e28312b14b076584fedd696fae2a684e460bd11e`). It corrects line 69, which is unchanged from base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
Axis judged: freshness. Milestone: r26-recheck-falsify. Leaf; no delegation.

## Verdict: DISAGREE (low)

The correction is mechanically sound. Its quote is verbatim, the retained bytes check out, and the base bytes are preserved. Its diagnosis is not established, though. Line 69 says the parser does not "report **all** implicit closures". S026's sentence entails that weaker claim, so line 69 is not wrong at its own stated scope. At most the paraphrase is ambiguous, and "overstates" holds only under a "reports none" reading that the words do not force. The source has also not changed since round 23, so nothing here went stale.

## Evidence

1. **Original line (base).** `git show 97404de…:corpus/knowledge/static-canonical-preflight.md`, lines 68–69:
   "Its docs explicitly say it does not check / matching start/end tags or report all implicit closures (S026)."
2. **Retained bytes.**
   - `fetched/text/S026-1.txt` line 1: "This parser does not check that end tags match start tags or call the end-tag handler for elements which are closed implicitly by closing an outer element."
   - `zcat fetched/S026-1.raw.gz | sha256sum` gives `d92217e08486dc9bfedf255f071fdad1ea1a506a1e8a8570c4711a47aad5faa3`, 55260 bytes. This matches the manifest and `rechecks/S026.json`.
3. **Live page.** One public GET of the S026 URL from `SOURCES.md` (not saved):
   - The same sentence appears word for word: `[' This parser does not check that end tags match start tags or call the end-tag handler for elements which are closed implicitly by closing an outer element.']`
   - Version label: `['Python 3.15.1 documentation']`.
4. **History.** `.ufo/waves/round-23/w1/ReopenPythonParser.md:8` quotes the identical sentence from the 3.15.0 build (2026-10-21 06:59 GMT). Round 23 filed it as "P3 … precision", not as staleness. `round-22/w1/PythonParser.md:34` describes the same disclaimer as "implicit end-tag dispatch".
5. **Logic of the original.** S026 says the end-tag handler is not called for one class of implicitly closed elements. It follows that not all implicit closures are reported. "Does not … report all implicit closures" is therefore a correct, weaker entailment under its literal not-all quantifier. Calling it "overstates" requires reading it as "reports no implicit closures". That reading is possible but not the plain one. Even under it, the claim is true of HTMLParser's behaviour, since it is a tokenizer that synthesizes no implied end tags [INFERENCE: from the documented callback model, not tested]. The claim is just not explicit in S026.
6. **Correction text checks.** Line 188 of the candidate:
   - Its quote “or report all implicit closures (S026)” matches line 69 verbatim.
   - Its quote “closed implicitly by closing an outer element” is verbatim in `S026-1.txt` and on the live page.
   - "Python 3.15.1 documentation" appears in both `S026-1.txt` and `S027-1.txt`.
   - "relied-on sentences are unchanged" holds against round 23's exact quote. The lowercasing sentences are still present in `S026-1.txt`: "converted to lower case" ×2, "translated to lower case" ×1, "entity references have been replaced" ×1.
   - All of these are accurate.
7. **Prefix check.** The base file (14076 bytes, 180 lines) is a byte-exact prefix of the candidate file (16987 bytes, 194 lines). The prefix `cmp` printed `PREFIX_OK`, and `git diff --stat 97404de e28312b -- <file>` shows "14 insertions(+)" with no deletions. The worktree equals the candidate.
8. **Ledger coupling.**
   - `statements.json:158-165` records S026 as `stale: 1` (C2 accepted). The row receipt `rechecks/S026.json` is HOLD with `correction: null`.
   - That pairing is consistent with the two-level design. The anchor holds, and statement-level STALE tags are counted separately by `measure.py:450-454`.
   - Because of this coupling, the reported 8/8 statement corrections include this disputed one.

## Impacted axes

- **Freshness / provenance.** Labelling a precision issue present since round 22 as STALE reads as source drift, but the source is unchanged across round 23, round 26 and the live page.
- **Correctness of the tag's claim.** "Overstates" is not demonstrated.

## Smallest safe correction

Change the diagnosis wording only; no original bytes change. Replace "overstates S026" with: "is broader than S026's explicit wording: S026 states only that the end-tag handler is not called for elements “closed implicitly by closing an outer element” (unchanged since round 23); it is silent on other implied end tags."

There is a tradeoff the judge has to settle. Reclassifying this as a precision note instead of STALE would take the S026 ledger count from `stale: 1` to `0` and the counter from 8/8 to 7/7. The contract defines STALE as a statement not matching the re-fetched bytes. Under that definition, keeping the tag is defensible only on the "reports none" reading.

Tooling: no installs or updates. Commands run: `git show`, `cmp`, `git diff --stat`, `zcat | sha256sum`, `grep`, one read-only `curl` GET of the `SOURCES.md` URL (output not saved), and the read/grep tools.

```json
{"target":"corpus/knowledge/static-canonical-preflight.md:188 [r26-recheck S026 STALE] (line 69 'all implicit closures')","verdict":"DISAGREE","severity":"low"}
```
