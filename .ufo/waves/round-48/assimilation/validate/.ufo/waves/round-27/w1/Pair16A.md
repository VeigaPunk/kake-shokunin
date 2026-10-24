# Pair16A — (S023, corpus/knowledge/static-canonical-preflight.md) — proposed HOLD

Seat: `KakeR27.Pair16A` (reviewer, leaf — no dispatch). Axis: **freshness**. Milestone: `r27-full-citing-set`.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Checked 2026-10-21. Frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (the two revisions are byte-identical for every file cited below).
Read-only: no corpus, ledger, script, lane-state or Git mutation by this seat. **No tool installed or upgraded** (no `pacman`/`uv`/`cargo`/`npm`); only `python3` stdlib, `curl`, `grep`, `read`. No r24 work read, retried, rephrased or rerouted.

## 1. Where the citation actually is (ranges expanded)

`corpus/knowledge/static-canonical-preflight.md` contains **zero literal `S023`** tokens. The pair exists only because the C1 counter expands the range on **line 2**:

```
corpus/knowledge/static-canonical-preflight.md:2
verified-at: 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029), documentation opened this round; local behavior has separate committed round22 receipts, not live website verification
```

`S020-S027` uses ASCII hyphen `0x2d`; `count_c1.py`'s `RANGE` regex (`[-–—]|\.\.|to|through`) therefore matches it and expands the block to S020…S027, admitting S023 (and S022) as citing pairs of this file. Reproduced over the whole `corpus/knowledge` tree at the base revision:

- literal `S023` hits in this file: **none** (`LITERAL` finditer → 0);
- range hits spanning 23: **exactly one**, line 2, `S020-S027`;
- all row ids the file contains: `S001-S006, S008, S020-S034` (no S007/S009–S019/S014/S015… outside that set) — the set is unchanged by this seat's reading.

**Denominator effect of this seat: none.** This seat adds **no** citing pair; the pair it adjudicates is already in the frozen 57 (`c1-before.json` `missing` list, and the `c2-oracle.json` expected set). The single entry in `.ufo/waves/round-27/discovered-pairs.json` (`(S013, corpus/knowledge/ghp-served-set.md)`, raising 57→58) is a **sibling seat's** discovery, not mine; I did not and could not shrink it. A separate sibling sweep (`w1/SourceCensus.md`) independently confirms S023 has no uncaptured citing form beyond the line-2 range, consistent with my own scan.

So the whole S023 ↔ this-file relationship is **one front-matter date stamp**, not a statement attributed to S023. The r26 EOF prose (lines 184–203) never names S023 either; the only S-ids it names are S020, S021, S026–S034, S024, S025.

## 2. Scope test of the citing line (its own terms)

Line 2 asserts two things: (a) the S020–S027 documentation was opened/verified **2026-10-20**, (b) the S028–S029 documentation on **2026-10-21**. Both hold for S023:

- `corpus/SOURCES.md:31` — the S023 row records `opened 2026-10-20` and anchor `Section 4.6.8 Link types and 4.6.8.4 canonical; Living Standard accessed 2026-10-20`.
- Every row of the S020–S027 block carries `opened 2026-10-20` (SOURCES.md:28–35); S028 and S029 carry `opened 2026-10-21` (SOURCES.md:36–37) — i.e. the two date groups on line 2 partition the registry exactly, with no row mis-dated.
- `corpus/SOURCES.md:69` — `Searched the fixed eight official sources listed in S020–S027 on 2026-10-20 … Identified 8, screened 8, included 8`. The range is the round-22 eight-source set (S020…S027 = 8 rows), so the parenthetical is the round-22 read group, not a claim that this file derives anything from S023.
- **The contemporaneous round-22 record splits the two roles explicitly** — `corpus/lessons/round-22.md`:
  - `:36` — `### Sources opened for C1 (2026-10-20)` — the section heading under which the S023 row sits (`:46` — `| S023 | https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | Section 4.6.8.4: …`). S023 was therefore opened on 2026-10-20, exactly the date line 2 attaches to the S020–S027 block.
  - `:55–56` — `C1's knowledge entry cites S020/S021/S026/S027; the remaining rows ground its implementation/rejection boundaries in this Gate.` The corpus's own round-22 account states that S023 (one of the "remaining rows") grounds the **Gate/lesson**, not the knowledge entry — the same division SOURCES.md's `used-by` records. This is the strongest available corroboration that the range on line 2 is a date bracket over the round-22 read group, not a claim that the knowledge entry rests on S023.
  All three strings (`### Sources opened for C1 (2026-10-20)`, `C1's knowledge entry cites S020/S021/S026/S027`, and the S023 lesson row) occur **exactly once** in `corpus/lessons/round-22.md` at both `83528f7c…` and `be375d9…`.

## 3. Historical dates preserved; no r20 tail; retry boilerplate irrelevant

- **r20 tails**: `corpus/lessons/round-20.md` contains **0** `S023` tokens and **0** `S02x` literals at all; `corpus/lessons/round-21.md` likewise 0. No r20/r21 tail claims anything about S023, so no stale premise can originate there. `corpus/lessons/round-22.md:46` (the row's real `used-by`) states `Section 4.6.8.4: "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document."` — verbatim still true (see §4).
- **r26 manifest-retry is S008 boilerplate**: `.ufo/waves/round-26/fetched/manifest-retry.json` contains exactly one entry, `row: S008` (GNU tar texi, `reason: "first attempt TimeoutError at 60s; single retry with 240s timeout"`). It has no bearing on S023. S023 was fetched in the ordinary single attempt — `.ufo/waves/round-26/fetched/manifest.json` row S023, `index 1`, `status 200`, `fetchedAt 2026-10-21T15:10:45.104275+00:00`, `bytes 381019`, `sha256 82a81f23…f6b7`, `last-modified: Tue, 20 Oct 2026 12:58:32 GMT`, `etag "6ad76578-5d05b"`.
- **Historical dates are not stale by design**: the entry's own r26 paragraph (line 184) states `Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten.` The 2026-10-20 stamp is therefore a preserved historical reading date, not a live-freshness assertion, and rewriting it would be the error.
- **The corpus's own citation policy for this row type is explicit** — `corpus/lessons/round-22.md` (once at both revisions): `Living Standard citations are date-anchored, not immutable revision pins.` S023 is a Living Standard row, so its `opened 2026-10-20` / `accessed 2026-10-20` is a **date anchor by policy**, not a claim of an immutable revision. The correct freshness test is therefore "did the document change under that anchor", answered in §4 (it did not) — not "is the date still current" (a Living Standard is never still current).

## 4. Source still supports the row (freshness, not just metadata)

- Live GET today, 2026-10-21, `https://html.spec.whatwg.org/multipage/links.html#link-type-canonical`: `sha256 = 82a81f233583716daf76ce20938a399016dfd877a9368ea2cdb1a60bcd3df6b7`, `content-length: 381019`, `last-modified: Tue, 20 Oct 2026 12:58:32 GMT`, `etag: "6ad76578-5d05b"` — **byte-identical** to the retained r26 raw (`git show 83528f7c…:.ufo/waves/round-26/fetched/S023-1.raw.gz | gunzip | sha256sum` → same digest) and to the round-22 pin `corpus/SOURCES.md`-era `82a81f23…f6b7` recorded at `.ufo/waves/round-22/w1/Case06.md:387`.
- Retained text view `.ufo/waves/round-26/fetched/text/S023-1.txt` (108,074 chars, one line): the r26 receipt quote `Keywords are always ASCII case-insensitive, and must be compared as such.` occurs **exactly once**, at char **41679** — matching the corrected locator in `.ufo/waves/round-26/receipt-locator-errata.json` (`"S023": 41679`).
- r26 receipt `.ufo/waves/round-26/rechecks/S023.json`: `"verdict": "HOLD"`, `fetchIndex 1`, quote as above (11 words ≤ 25), `correction: null`. The r26 falsify seat agreed (`w2/FalsifyS023.md`, `{"verdict":"AGREE","severity":"low"}`); its one residual nit (receipt `anchorObserved` says §4.6.8.4 "body follows at the same heading level" — §4.6.8 is `<h4>`, §4.6.8.4 is `<h5>`) is already carried as an erratum row in `receipt-locator-errata.json` (`"row": "S023"`), so it is not an open r27 item.

## 5. Verdict: HOLD (decided, at the citing line's own scope)

The only assertion this file makes about S023 is the line-2 verified-at date stamp, and it is supported at that scope: S023's registry row records `opened 2026-10-20` / `Living Standard accessed 2026-10-20`, the S020–S027 date group matches the registry exactly, the source bytes are unchanged (identical digest live today), and the file's r26 paragraph declares older verified-at dates historical and preserved. There is **no** S023-derived statement in this file to be wrong or over-scoped, and no evidence of drift ⇒ not STALE, and nothing undecided ⇒ not UNVERIFIABLE.

Registry cross-check (read-only, no edit proposed): SOURCES.md's `used-by` for S023 is `corpus/lessons/round-22.md` only — it does not list this knowledge file, and S023 is absent from the file's `source:` front-matter (line 1). Exactly the two rows newly admitted into the C1 set by the line-2 range expansion (S022, S023) are the two whose `used-by` omits this file, so the registry and the file agree that the mention is metadata-level, not a substantive use. That agreement is the reason this is HOLD rather than a mis-attribution.

### Suggested C1 ledger record (contract C1 `pairs.json` shape)

```json
{
  "row": "S023",
  "file": "corpus/knowledge/static-canonical-preflight.md",
  "kind": "artifact",
  "verdict": "HOLD",
  "evidence": "corpus/SOURCES.md",
  "contains": "| S023 | WHATWG HTML: Link type canonical — https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | spec | A | HTML link-type keyword semantics | Section 4.6.8 Link types and 4.6.8.4 canonical; Living Standard accessed 2026-10-20 |",
  "reason": "S023 appears in this file only through the range S020-S027 on line 2 (verified-at: 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029)); no literal S023 and no statement attributed to it. The date stamp is supported at its own scope: corpus/SOURCES.md:31 records S023 opened 2026-10-20 with anchor 'Section 4.6.8 Link types and 4.6.8.4 canonical; Living Standard accessed 2026-10-20', every S020-S027 row is opened 2026-10-20 (SOURCES.md:28-35) and S028-S029 2026-10-21 (SOURCES.md:36-37), matching SOURCES.md:69 'Searched the fixed eight official sources listed in S020-S027 on 2026-10-20' and the contemporaneous round-22 record (corpus/lessons/round-22.md:36 'Sources opened for C1 (2026-10-20)', whose S023 row sits at :46, and :55 'C1's knowledge entry cites S020/S021/S026/S027; the remaining rows ground its implementation/rejection boundaries in this Gate'). Freshness unchanged: live GET 2026-10-21 returns sha256 82a81f233583716daf76ce20938a399016dfd877a9368ea2cdb1a60bcd3df6b7, identical to the retained r26 raw and the round-22 pin (round-22/w1/Case06.md:387), last-modified Tue, 20 Oct 2026 12:58:32 GMT; r26 receipt rechecks/S023.json is HOLD with quote 'Keywords are always ASCII case-insensitive, and must be compared as such.' (11 words) at char 41679 of fetched/text/S023-1.txt. Historical date preserved: the corpus policy is 'Living Standard citations are date-anchored, not immutable revision pins' (round-22.md) and the entry's r26 paragraph states older verified-at dates remain the historical record and are not rewritten."
}
```

Alternative evidence, also verified exactly once at `83528f7c…` and `be375d9…`: `corpus/lessons/round-22.md` with `contains: "### Sources opened for C1 (2026-10-20)"`, or `.ufo/waves/round-26/fetched/manifest.json` with `contains: "\"sha256\": \"82a81f233583716daf76ce20938a399016dfd877a9368ea2cdb1a60bcd3df6b7\""`.

`contains` verified present **exactly once** in `corpus/SOURCES.md` at both `83528f7c…` and `be375d9…`; `corpus/SOURCES.md` is tracked at both revisions (`git cat-file -e` → ok), so the counter's `artifact_support` check passes.

**Alternative if L1 prefers a fresh r27 source observation**: `kind: "source"`, `fetchIndex: 1`, `quote: "Keywords are always ASCII case-insensitive, and must be compared as such."`, `anchor: "Section 4.6.8 Link types preamble (text view line 1; quote at char 41679 of the committed view)"`. This requires S023 to be present in `.ufo/waves/round-27/fetched/manifest.json` with a matching `.ufo/waves/round-27/fetched/S023-1.raw.gz` + `text/S023-1.txt` at the measured revision; the r27 fetch set produced so far covers S001–S006 only (`fetch_group.py` restricts to `range(1,7)`), so this variant is **not** satisfiable today without a new fetch. The artifact variant above is what the counter can validate as committed.

## 6. Appended correction wording (optional, non-STALE — no `[r27-recheck S023 STALE]` marker)

Verdict is HOLD, so **no** STALE marker is owed and none should be added. One factual gap in the same file is worth an append-only precision note, mirroring the entry's own precedent at line 200 for S024/S025: the r26 recheck paragraph at line 184 lists the rows re-fetched in r26 and omits **S022 and S023**, although both were re-fetched (`r26/fetched/manifest.json` rows S022, S023) and judged HOLD (`r26/rechecks/S022.json`, `r26/rechecks/S023.json`); line 200 discloses that omission only for S024/S025. Suggested append-only wording (place at the end of the "Round-26 falsify-wave adjudication" block):

> - S022 and S023 were re-fetched this round as well (receipts HOLD, `.ufo/waves/round-26/rechecks/S022.json` and `S023.json`) and were missing from the recheck paragraph's row list above; the file's front-matter date stamp `verified-at: 2026-10-20 (S020-S027)` (line 2) names both rows, and neither is used for any statement in this entry.

Constraint for L1: this wording must not introduce any row id outside the file's existing id set (`S001-S006, S008, S020-S034`), or it would enlarge the C1 denominator with new pairs. `S022`/`S023` are already inside it, so this append adds **no** new citing pair. The registry-side gap (SOURCES.md `used-by` for S022/S023 omits this knowledge file, while the C1 range expansion admits the pair) is a `corpus/SOURCES.md` question for a writer seat, not a finding I am editing.

## 7. Residual risk / verification gaps

- **Low**: the pair is a range-expansion artifact. If L1 later narrows the C1 denominator to exclude pure date-stamp ranges, this pair leaves the denominator and the count would shrink — forbidden ("denominator grows monotonically"); keep it adjudicated as HOLD.
- **Low**: the range on line 2 (`S020-S027`) over-covers the file's actually-used rows; that over-coverage is what creates the S022/S023 pairs. It is historically faithful (round-22 eight-source set) and should not be "corrected" by rewriting the range, which would erase two pairs.
- **Gap (not verifiable here)**: the counter's `source` branch for S023 is untested in r27 because S023 was never fetched into `.ufo/waves/round-27/fetched/`; only the `artifact` branch is exercised by the record proposed in §5.
- **Gap**: `corpus/SOURCES.md:31`'s `recheck 90d` for S023 falls due ~2027-01-18; the 2026-10-20 access date is inside its window, so no recheck obligation is triggered by this round.
- **Scope note**: this is a scoped citation adjudication, not admission; the parent independently judges.

## 8. Bottom line

HOLD. The S023 ↔ `corpus/knowledge/static-canonical-preflight.md` citation is the front-matter verified-at range `S020-S027` on line 2 — a historical date stamp, not a claim; it is correct at its stated scope against `corpus/SOURCES.md:31` and `:28-35`/`:36-37`, the source bytes are unchanged (live sha256 identical to the r26 retained raw and the round-22 pin), and no S023-derived statement exists in the file to falsify. No `[r27-recheck S023 STALE]` marker is owed; an optional append-only note (line 200 precedent) may record that S022/S023 were likewise re-fetched in r26, without introducing any new row id.

Report: .ufo/waves/round-27/w1/Pair16A.md
