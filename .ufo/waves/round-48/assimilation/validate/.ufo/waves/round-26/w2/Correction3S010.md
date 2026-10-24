# Correction3S010: falsify `[r26-recheck S010 STALE]` line-1 locator correction

Target: `corpus/knowledge/ghp-etag-anatomy.md:62` at candidate `e28312b14b076584fedd696fae2a684e460bd11e` (base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`). Axis: freshness.

**Verdict: DISAGREE (low).** The correction is accurate and every base byte is preserved. The problem is the STALE label. The same header structure appears in three other knowledge files, and eight sibling seat-judgments of it were HOLD. The S010 seat itself says the defect is "not source drift". So this one STALE is not decided "against the 2026-10-21 bytes" as the statement rule requires, and the counted 8 STALE statements are one too many. Alternatively, if this STALE stands, the same rule leaves at least three locator STALEs unflagged elsewhere.

## 1. Byte preservation (prefix check): passes

Command (Python, read-only):

```
base = git show 97404de…:corpus/knowledge/ghp-etag-anatomy.md
cand = git show e28312b…:corpus/knowledge/ghp-etag-anatomy.md
-> base len 3304 endsNL False cand len 4905 prefix True worktree==cand True; first diff at 3304
```

The base has no trailing newline. That is why `git diff` shows the last line (`- **Validator is not identity:** …`) as removed and re-added. The bytes are identical, and the candidate only appends after byte 3304.

## 2. Accuracy of the correction text: passes

Line 62: "the URL there is S009's nginx source only. S010 is RFC 9110 §8.8 — https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8 (§8.8.1 Weak versus Strong; §8.8.3 ETag), re-fetched 2026-10-21."

- The URL at base line 1 (`https://raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c §ngx_http_set_etag`) equals the S009 row URL at `corpus/SOURCES.md:17`.
- The S010 URL equals `corpus/SOURCES.md:18`, the `population.json` fetch URL, and `manifest.json` `finalUrl`. The fetch returned HTTP 200, `fetchedAt` `2026-10-21T15:10:38.602255+00:00`, sha256 `d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5`.
- The headings are verbatim. In `fetched/text/S010-1.txt`, `8.8.1. Weak versus Strong` and `8.8.3. ETag` each occur 2 times.
- The S010 bytes contain neither `nginx` nor `ngx_http_set_etag` (0 occurrences each). So the line-1 locator does not resolve inside S010.

## 3. Is base line 1 wrong at its own stated scope? Counterexample: not under the rule as applied everywhere else

Base line 1: `source: S009, S010 (corpus/SOURCES.md) — <S009 URL> §ngx_http_set_etag`. The parenthetical `(corpus/SOURCES.md)` sends source-ID resolution to SOURCES.md, where the S010 locator is correct. `corpus/QUALITY.md` (lines 44-48) prescribes no per-source URL in the header. Four base knowledge files use the same pattern: several source IDs and one primary URL.

| File, line 1 (base) | Printed URL belongs to | Non-matching IDs judged in round-26 wave 1 |
|---|---|---|
| `crawl-scope-per-host.md` (S011, S012, S013, RFC 9309 URL) | S011 | S012: HOLD, "Provenance note only: the header prints the RFC 9309 URL, and S012's URL lives in SOURCES.md:20. Non-blocking." (`w1/PairS012CrawlScopePerHost.md:17`). S013: HOLD (`w1/PairS013CrawlScopePerHost.md:22`) |
| `ghp-custom-domain.md` (S003, S005, S007, S005 URL) | S005 | S003: HOLD, "F4 PROVENANCE … S003's URL and anchor live in SOURCES.md:11. Nothing changed, so no correction." (`w1/PairS003GhpCustomDomain.md:18,44`). S007: HOLD, "L1's URL and anchor … belong to S005. S007's own URL is not on that line" (`w1/PairS007GhpCustomDomain.md:19`) |
| `ghp-served-set.md` (S001…S008, S001 action.yml URL) | S001 | S004: HOLD (`w1/PairS004GhpServedSet.md:18`). S006: HOLD (`w1/PairS006GhpServedSet.md:15`). S008: HOLD, "The pinned URL on :1 is S001's `action.yml`, which is outside this pair." (`w1/PairS008GhpServedSet.md:20`) |
| `ghp-etag-anatomy.md` (S009, S010, S009 URL) | S009 | **S010: STALE** (`w1/PairS010GhpEtagAnatomy.md:13`) |

Eight HOLD judgments against one STALE, for the identical fact. The STALE also fails the ledger's own rule. `statements.json` `rule` says: "STALE = the statement is wrong or unsupported at its own stated scope against the 2026-10-21 bytes". The S010 seat says: "Both STALE rows are pre-existing defects in the entry (a wrong locator and an incomplete paraphrase), not source drift" (`w1/PairS010GhpEtagAnatomy.md:7`). Its row-1 quote, the RFC abstract, has no bearing on the locator. The locator defect is the same against any fetch, 2026-10-19 or 2026-10-21, so it is not a freshness decision. Labelling it `[r26-recheck S010 STALE]` gives a write-time locator gap freshness provenance it does not have.

The S010 C2 correction (line 64, the §8.8.1 "and retrieved between those modifications" condition) is not challenged. The quote is verbatim, appears once in the text view, and fits the rule's "quote fidelity" clause.

## 4. Impact on the counter

Read-only run (disclosed: the item did not name this command, but it writes nothing): `python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b…` exited 0 with `statements 276, statementsStale 8, statementCorrections 8, hold 32, stale 0, findings []`. The ledger total is 8 = S003 2 + S010 2 + S021 1 + S026 1 + S030 2. With the locator note reclassified, the totals become 7 and 7. The exit code is unchanged: the ledger requires tags ≥ stale, so the 32/32 HOLD row result and C1 still pass. Only the stated "8/8 STALE corrections" figure is overstated.

Minor, same block (low): the line-60 preamble says "S008 via `manifest-retry.json`". S008 is not cited by this file, so this looks like boilerplate carried over from `ghp-served-set.md`. The same preamble says S010 was "judged HOLD", which is true at row level (`rechecks/S010.json` verdict HOLD, `correction: null`). Two `S010 STALE` tags follow it, and the block does not say these are statement-level verdicts.

## 5. Smallest safe correction (choose one rule and apply it everywhere)

1. **Preferred (matches 8 precedents).** Keep the line-62 text but retag it as an uncounted provenance note, for example `- Round-26 locator note (S010; not STALE): …`. Line 62 is new in this round, so editing it is append-only safe. Set `statements.json` S010 `stale` from 2 to 1, change `w1/PairS010GhpEtagAnatomy.md` row 1 to HOLD with a provenance flag, and the counter reads 7/7.
2. **Alternative.** If L1 rules that a header URL belonging to another source is STALE, apply that consistently: add `[r26-recheck S0NN STALE]` locator corrections to `crawl-scope-per-host.md`, `ghp-custom-domain.md` and `ghp-served-set.md`, and raise the ledger counts. Leaving one STALE among eight HOLDs is the defect.

Optionally drop "S008 via `manifest-retry.json`" from the line-60 preamble.

## Tooling

No tools installed or upgraded. I used git, Python 3 stdlib (read-only), grep and sed. I made no network GET. The only file written is this report.

```json
{"target":"corpus/knowledge/ghp-etag-anatomy.md:62 [r26-recheck S010 STALE] line-1 locator","verdict":"DISAGREE","severity":"low"}
```
