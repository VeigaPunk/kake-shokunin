# ScribeProvinceStep — round 38, wave 1

## Axes and behavior
- Operability: drafted a concise Province step and corpus coverage entry distinguishing the round-37 non-admission from round-38 C2's declared re-claim, stating the h/i/k rules and v3 control separation, and preserving explicit scope limits.
- Freshness: no web property or source URL was fetched; the drafts retain synthetic/offline wording and make no live-freshness claim.
- The drafts are not evidence that C2 built, passed its predicate, or was admitted.

## Gates and commands
- `timeout 10s mkdir -p /fast/scratch/hyaku/kake-r38w1/ScribeProvinceStep/tmp` — exit 0; no output.
- `export TMPDIR=/fast/scratch/hyaku/kake-r38w1/ScribeProvinceStep/tmp && prlimit --as=4000000000 timeout 10s sha256sum /fast/scratch/hyaku/kake-r38w1/ScribeProvinceStep/province-r38.md` — exit 0; output: `9f45a8a7f3137b0eb19195a0cdc3433106f1122ff053d5428c98c9eb88f7e2da  /fast/scratch/hyaku/kake-r38w1/ScribeProvinceStep/province-r38.md`.
- No build, selftest, round-37/round-38 counter, test suite, git command, or network request was run. C2 execution and admission remain unverified here.
- No tool was installed or updated.

## Touched surfaces
- Sandbox deliverable: `/fast/scratch/hyaku/kake-r38w1/ScribeProvinceStep/province-r38.md` — SHA-256 `9f45a8a7f3137b0eb19195a0cdc3433106f1122ff053d5428c98c9eb88f7e2da`; contains both requested drafts, each under 20 lines.
- Report: `.ufo/waves/round-38/w1/ScribeProvinceStep.md` (this file).
- Read-only source surfaces: `PROVINCE.md:297-305`; `corpus/README.md:362-370`; `SCORECARD.md:2070-2122,2123-2162,2211-2248`; `corpus/SOURCES.md:19,37,42,97,103-104`; `corpus/lessons/round-37-verifier-spotcheck.md:149-151`.
- Product prose and code in the lane were not edited; only this report was written in the lane.

## Findings and limits
- The closure correction says round-37 C1 was not admitted and the tool/selftest/independent implementation remain non-claim work (`SCORECARD.md:2072-2083`).
- C2 is a declared repair of the existing tool surface: h rejects non-JSON constants and handles arbitrary-length integers by field use; i checks ASCII URL characters against the RFC 3986 set while retaining non-ASCII; k applies implicit `/robots.txt` allow after path normalization (`SCORECARD.md:2211-2221,2142-2162`).
- The declared v3 target is 20/20; the pre-build base measured 8/20 and the stdlib-plus-six-patches control 7/20, below target (`SCORECARD.md:2223-2242`).
- The drafts retain the offline/synthetic boundary and leave live fetch, redirects, caching, crawler-specific extensions, sitemap handling, the symlinked-manifest-directory contract point, and per-byte U+FFFD handling open (`PROVINCE.md:299-305`; `SCORECARD.md:2050-2057,2138-2140`; round-37 lesson `:149-151`). The sources cited for the draft scope include S011, S034, S029/S089, S095/S096, and S012/S013.
- Out of scope: product implementation, editing `PROVINCE.md` or `corpus/README.md`, running gates, and making a round verdict. No sealed-key tree was accessed.
