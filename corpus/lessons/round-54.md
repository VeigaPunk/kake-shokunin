# Round 54 — kake

Lane: `kake-shokunin`; round-open base `68228b2d74e7930ae4f07e90e382a0d03ab80c7b`.

## Gate

No new SOURCES rows were added. S374 was re-opened locally from the retained
round-52 source body; no network request was made this round. URL:
https://info-search.yahoo.co.jp/archives/002851.php; access date: 2026-10-25;
located quote: 「このリンク先のウェブページの巡回を推奨していない」 (24 units
under the lane's CJK counter); location: rel=nofollow paragraph under
`rel属性の利用` in the page titled
`リンク先のウェブページの巡回制限　― rel属性の利用`. Retained body:
`.ufo/waves/round-52/sources/S374.html`; SHA-256
`3ad358bdbe7a74798df151c282e4b57af7475686dc405b3f8bad08f68881aecb`;
retained receipt records HTTP 200. This verifies the quote/locator against the
retained bytes, not current source availability.

Assimilation: none. `considerthese/2026-10-25.md` remains the latest reflection;
its cross-registry proposal is not expanded by this round's settlement.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| Material crawl qualifier dropped by an endorsement-only translation | `corpus/lessons/round-53-verifier-spotcheck.md` §Discernment (S374, quality harmed); exact source phrase and page title in retained `.ufo/waves/round-52/sources/S374.html`; the round-52 knowledge gloss at `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` renders “does not recommend” / “cannot vouch” without saying that the crawling of the link target is not recommended. | No existing criterion checked that the English rendering preserves material qualifiers from its located source. | Append the S374 correction without rewriting the earlier gloss; add a QUALITY criterion and a calibration counter over committed entry/body bytes. The counter must reject the round-open no-op (one mismatch) and accept only a quote-backed correction that explicitly retains the crawl qualifier. |
| A launched wave was presented without a durable seat-report settlement | The round-53 closure records 40 spawned, 0 committed reports, seven unresolved report names and no `w1/` directory (`corpus/lessons/round-53-verifier-spotcheck.md` §Dead-seat reconciliation). | Round-53 report described seat-level dispatch results but no settled manifest check required committed reports or an honest lost disposition. | Preserve the dispatch spec; add `.ufo/waves/round-53/settlement.md` with each cited report resolved or lost and state explicitly that the individual dead-seat count is unverified. Add a SKILL registry row for `c53_gate_truth.py`; test both obligations from committed bytes. |
| CJK quote “word” counts were conflated with unit counts | The round-53 verifier recorded S367/S372/S373 at 31/27/27 units under the inherited counter, whose `units()` gives one per CJK character and one per non-CJK whitespace token. These values exceed 25 units; they do not establish how many lexical words the CORPUS rule means for Japanese. | `corpus/QUALITY.md` had no explicit CJK accounting criterion; the inherited counter's unit convention was not called out alongside the separate ≤25-word corpus language. | Add a criterion stating the CJK unit convention and report its counts as units, not words. Do not claim these values satisfy the 25-word rule; the exact meaning of “word” for CJK remains ambiguous until the corpus contract specifies segmentation. |

## Round-53 settlement

The 40-seat dispatch spec records roles scout 14, connector 1, executor 3,
scribe 6, reviewer 8, critic 8. The closure found 0 committed seat reports.
Seven named report files remain lost pointers; settlement does not infer which
seat timed out or claim an individual death count. Manifest:
`.ufo/waves/round-53/settlement.md`.

## Round-54 claims

Frozen contract: `.ufo/waves/round-54/contract.md`, committed before claim data
was scored. C1 is calibration; C2 is operability. Their counters derive from
committed Git blobs. The round-open base control for C1 is expected to report
one mismatch and fail; C2's base control is expected to show the absent
registry/manifest and fail. CJK quote accounting is maintenance, not a third
claim.
