# ReviewerC1Semantics — C1 counter review

## Finding — High: `met=true` is reproducible with fabricated source bytes and marker prose

The counter does not authenticate or derive the retained text from the retained source. At `c63_calibration.py:107-109`, it reads the two blobs and ledger from the candidate revision; `:121-124` checks only global substrings in knowledge; `:133-142` checks that ledger SHA values match those candidate blobs, that the ledger quote equals the frozen quote, and that the quote is present in text but absent in raw. `:145` combines these checks. No frozen identity/provenance check, extraction of `S432.txt` from `S432.html`, `locatedRawLines` validation, or committed `extract_text.py` execution occurs. The ledger itself is candidate-controlled; its schema and paths are not validated.

I built a scratch fixture under `/fast/scratch/hyaku/kake-r63/ReviewerC1Semantics/fabric`, verified its Git top-level before committing, and removed it after the attack. It contained a 45-byte fabricated raw body (`fabricated body, not the Fetch standard.`), a text file consisting only of the frozen quote, an internally SHA-consistent ledger with `schema: fabricated`, and junk marker prose. The counter returned:

```text
revision=f2fe8a52d363c2eddf8d9c2c4f0bbe1ae0f12363 disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

Exact command (from `/home/vgpnk/Projects/shokunin/kake-shokunin`):

```sh
python3 -B .ufo/waves/round-63/c63_calibration.py --root /fast/scratch/hyaku/kake-r63/ReviewerC1Semantics/fabric --revision f2fe8a52d363c2eddf8d9c2c4f0bbe1ae0f12363
```

The fixture's knowledge file had `[r63-correction` and the ledger path in one unrelated paragraph, with the frozen quote elsewhere; its quality, lesson, and SOURCES files were single-line marker stubs. Thus **every component of `resolved` was 1 with no genuine source or prose evidence**. This is an actionable semanticless-tree green and triggers the contract's C1 kill rule if treated as a wave attack.

## Finding — High: prose components are individually marker-only

A second scratch fixture used the authentic raw/text blobs and ledger copied from measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`, but replaced each corpus evidence file with junk marker strings. It also printed `met=true`:

```text
revision=HEAD disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

The checks are global substrings (`:121-124`, `:148-150`, `:153-160`) and a prefix regex (`:162`), not block/row or meaning validation. For example, `criterion` accepts the terms scattered in one marker line; `lesson_gate` accepts `## Gate`, the spot-check name, `Disagree`, `collapsed-only`, and `author-side` with no relationship between them; `source_row` accepts the incomplete row `| S432 |`. The correction check similarly does not establish that the block quotes/records the span in the claimed context. This attack shows the defect remains even when the underlying source-byte relationship is genuine: semantic contents of the required corpus evidence can be absent.

## What is sound / residual notes

At the measured commit, the ledger SHA values do match the actual retained blobs, and direct byte checks confirmed the frozen quote is absent from raw HTML and present in the 286,933-byte text rendering. The recorded honest green is therefore consistent with the implemented substring-class rule. The old marker-only fixture and junk-marker control receipts correctly show red under this counter, but do not cover fabricated self-consistent blobs or semantically empty evidence files.

`disagreements` is not part of `resolved`; a candidate with no S432/Disagree line can still green if the other markers and blobs pass. `unresolved` is forcibly zero whenever resolved, even with `disagreements=1` (`:164-165`). This is potentially misleading diagnostics, not an independent green route beyond the findings above.

## Verification evidence

- Counter file SHA256 matched the frozen value: `bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91`.
- Measured raw/text SHA256 values matched ledger: `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b` and `8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69`.
- The report's empirical counter runs were performed only on the two disposable scratch repos; both were removed. No install performed.
- No build, test suite, or linter run.

Report file: `.ufo/waves/round-63/w1/ReviewerC1Semantics.md`
