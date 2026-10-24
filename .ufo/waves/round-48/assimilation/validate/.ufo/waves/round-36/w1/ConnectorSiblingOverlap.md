# ConnectorSiblingOverlap — fleet sibling-lane overlap scan for C1 (round 36, w1)

Seat: leaf connector. Read-only on all sibling lanes; no network; sealed tree untouched; no installs.
Sibling state read at working tree 2026-10-22, kake lane at `cd3212796cab7a2afa03b638dbfafe7194df9629`.

## What "recheck" means fleet-wide (CORPUS.md)

- `CORPUS.md:105-106`: "`opened` — ISO date the row's author opened the source. `recheck` — ISO date or
  cadence (`90d`, `180d`, `on-release`)."
- `CORPUS.md:112-115`: "A row is a claim. Write it only after opening the source in the round that writes
  … date, and a ≤25-word quote with its location grounding `teaches`. Non-author verification re-opens a sample."
- So fleet-wide `recheck` is a **due date**, and quote re-checking is a **manual, sampled, author-adjacent
  act**. Nothing in the contract defines an offline replay of a recorded fetch: C1 adds, it does not restate.

## Sibling hits (path:line → overlap judgement)

| hit | judgement |
|---|---|
| `scripts/sources-census.sh:34-37` (fleet) | `overdue` mode reads only the recheck cell: "ISO recheck dates or NNd cadence … symbolic cadences … are reported, never judged overdue." C1 cannot drive it (no row/date fields); no conflict. |
| `kumitate-shokunin/scripts/sources-check.mjs:21,31,114,306-335`; `tabi-shokunin/scripts/check-sources.mjs:39,58,315-322` (+E04 `:34`) | `RECHECK_INVALID`/`RECHECK_OVERDUE` only, offline, never opens a body (tabi adds duplicate-URL). Same axis, different object; C1 is the missing content arm, and cannot drive either without a generator. |
| `kagi-shokunin/corpus/rendered-text-v1.py:1-60` (sha256 `7d6bfe8154…`) | **Closest algorithmic overlap with C1 (c)+(d):** the fleet's "one committed declaration" of the quote/page normalizer, with `locate FILE QUOTE`. Differs in every rule except `html.unescape`: strict UTF-8 (setup error) vs BOM/charset table, no comment rule vs comment-first, `<[^>]+>`→space vs `<`+letter…`>`→removed, no template rule, whitespace collapse vs `isspace()` deletion, no NFKC, no media-type branch. |
| `kagi-shokunin/corpus/source-fetches.tsv:6-32`; `kagi-shokunin/corpus/SOURCES.md:7` | Rows carry `Quote: …` and `Fetch sha256: …` (16-column capture table: status, final URL, method, representation, body sha256, bytes, normalized sha256) but **no body path**. kagi can verify a quote only by live re-fetch; a recorded fetch cannot be re-judged offline. C1 could serve kagi; kagi cannot serve C1. |
| `chousa-shokunin/tools/research-gate.sh:44-52,78` | `verify-claims` checks a verbatim span against a local source; "URLs refused — never fetched". Complementary and disjoint: chousa refuses exactly the object C1 judges. Match rule differs (token-boundary, raw text) from C1 (NFKC + whitespace deletion). |
| `chousa-shokunin/corpus/QUALITY.md:171` (working tree only) | Rule 25 says run `python3 tools/quote-reopen.py verify --items <tsv>`. **The tool does not exist**: `git -C chousa-shokunin ls-tree HEAD tools/` → `tools/research-gate.sh` only; `git log --all -- tools/quote-reopen.py` → 0 lines; the only artefact is `.ufo/waves/round-29/build/ExecToolB/quote-reopen-b.py` (sha256 `158ff00ef1…`), a differential oracle. Documented-but-unlanded capability, live-fetch based, counter page-sampled (130 items, network-dependent). |
| `kumitate-shokunin/scripts/anchor-truth.mjs:12,23-32,721-727`; `tabi-shokunin/scripts/check-adjacency.mjs:70-76,729-731`; `kama-shokunin/tools/citation-provenance.py:1-30` | Token-on-cited-line truth against a pinned clone; verbatim quote on a cited line of a sibling lane at a pinned revision; `cite(rev,path,sha256)` via `git cat-file`. All git-scoped, no HTTP: same purpose (machine-checkable citation), disjoint object. |
| `kotodama-shokunin/tools/check-source-access.py:1-25` | A bypass marker in a row makes it unopened. C1 has no access-control knowledge: a manifest built from a bypassed fetch reads clean. Named limit, not conflict. |
| `kotodama-shokunin/tools/check-gate-quotes.py:1-25`; `tsukuroi-shokunin/tools/check-recheck-commands.py:1-20`; `tabi-shokunin/scripts/check-freshness.mjs:1-30`, `freshness-witness.mjs:1-30` | Quote word cap; recheck-procedure binary safety; local file hash pins with a git witness. All disjoint from content-vs-recorded-fetch. |
| `kotoba-shokunin/corpus/lessons/round-53.md:14` (M42 `loose-match`) | A counter that "matched … a quote by substring" let a **fragment of the recorded quote** survive; substring matching is recorded as a defect class in the fleet. Direct tension with C1 (d); see below. |

## Demonstrated divergence (real recorded bytes, no network)

`/fast/scratch/hyaku/kake-r36w1/ConnectorSiblingOverlap/differential.py` (sha256 `456fb89315…`), run
`timeout 120 python3 differential.py` → **exit 0**, receipt `differential.out` (sha256 `065828f231…`):

```
S092 kagi_exit=0  count=1  C1_ref_holds=True  quote='references The ampersand must be followed'
S092 kagi_exit=1  count=0  C1_ref_holds=True  quote='referencesThe ampersand must be followed'
S088 kagi_exit=0  count=1  C1_ref_holds=True  quote='345 Park Ave San Jose'
S088 kagi_exit=1  count=0  C1_ref_holds=True  quote='345 Park AveSan Jose'
```

Bodies: S092 `sha256=0128a08f5d…` 89,196 B (`<dd>`), S088 `sha256=d431760660…` 1,187,554 B (`<br>`). The
C1 side is my re-implementation of (c)+(d), not the tool. C1's whitespace deletion makes a quote that no
reader sees as contiguous — joined across a block boundary or split by an inline tag — read as a hold; kagi's
declared normalizer rejects both.
C1 also cannot detect a **truncated** registry quote (substring containment is one-directional).

## Contradiction (stated, not smoothed)

kotoba M42 treats substring quote matching as `loose-match`; C1 (d) mandates substring matching. Both are
correct in their direction — M42's counter accepted a *mutation of the quote*, C1 asks whether the *quote is
contained* — but a C1 `clean` verdict therefore certifies "the recorded quote occurs in the recorded text",
never "the quote is the whole located sentence" or "the quote is reader-visible". chousa's ≤25-word located
quote rule carries completeness; C1 must not be reported as carrying it.

## Proposed move (one, bounded, docs+receipt only)

**Pin C1's normalizer lineage against kagi's `rendered-text-v1.py` instead of leaving it unstated.**
(1) One line in `scripts/source_recheck.py`'s docstring and in the round-36 C1 "Limits": C1 (c)(d) is *not*
`corpus/rendered-text-v1.py` (pin sha256 `7d6bfe8154…`), and the three demonstrated divergences are
deliberate. (2) Commit `verification/normalizer-differential.json` holding the four rows above with exit
codes and body hashes, produced against the **built** tool, not my reference. (3) Word the claim as
"recorded quote present in recorded text", never "quote verified".

- Axes: **freshness** — adds the only N-version oracle available (the 34 ablations are the L1's own
  reference, so they cannot catch a shared text-rule mistake); **operability** — gives kagi's row format and
  chousa's unlanded rule 25 a documented consumer path for an offline arm.
- Harm: none to the sealed predicate (no behaviour change, no new runtime dependency, no contract bullet
  touched); it *removes* a possible false-freshness claim, which is the r34/r35 rejection class.
- Risks: kagi's file may change (pin the sha, mismatch = could-not-evaluate); the differential must be run
  against the built tool or it proves nothing about C1; do **not** substitute C1 for chousa's
  `quote-reopen` (its counter is live-sampled and its rule token-boundary — a drop-in would be a contract
  mismatch); do **not** "unify" the two normalizers (C1's comment-first and `<`+letter rules decide sealed
  cases).

## Not verified

C1 tool and sealed counter were not run (tool absent; no key). `rendered-text-v1.py --selftest` not run.
chousa's working-tree changes are another lane's live state; I read them, changed nothing.
