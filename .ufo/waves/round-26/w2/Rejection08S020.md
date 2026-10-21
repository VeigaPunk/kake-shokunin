# Rejection08 S020: falsify L1's rejection of the R2 date-stamp STALE

Target: the L1 rejection of seat finding R2 (`corpus/knowledge/static-canonical-preflight.md` line 2, the S020 `verified-at` stamp). Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`. Axis: freshness. Milestone: r26-recheck-falsify.

**Verdict: AGREE.** Line 2 was correct at its stated scope when it was written, and it is still correct as a historical record. The rejection does not hide any staleness: the RFC bytes have not drifted, the date is backed by evidence, and "this round" refers to round 22, the round in which the line was written.

## What was rejected

- Ledger `.ufo/waves/round-26/statements.json:137-146`: row S020, `"statements": 13, "seatStale": 1, "stale": 0`, `"l1Disposition": "R2 is a verification-date stamp only; content HOLD."`
- Seat `w1/PairS020StaticCanonicalPrefl.md:18` (R2): `STALE (date only; content HOLD)`. The reason given is that the S020 date "is superseded by fetchedAt 2026-10-21T15:10:43Z". Flags F1 and F2 (lines 32-33) give the same reasoning.
- Statement at base, line 2: `verified-at: 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029), documentation opened this round; local behavior has separate committed round22 receipts, not live website verification`

## Attempts to show the statement is wrong at its stated scope

1. **Was the date false when it was written?** No.
   - `git blame -L1,3 97404de… -- corpus/knowledge/static-canonical-preflight.md` shows line 2 comes from `b539cc1` (round-22 recovery, 2026-10-21 03:16:39 -0300). That commit only split the date to add S028-S029. The original `c0fd6d5` (round-22, author date 2026-10-20T18:30:55-03:00, committer date 2026-10-20T18:53:36-03:00) already read `verified-at: 2026-10-20, documentation opened this round`.
   - Primary evidence at base, `.ufo/waves/round-22/w1/RFC6596.md:4`: `**Accessed.** 2026-10-20 (UTC, ~21:33Z).` That access time falls between the author time (21:30:55Z) and the committer time (21:53:36Z) of `c0fd6d5`, and the date is 2026-10-20 in both UTC and -0300. There is no timezone-boundary counterexample.
   - Corroborated at base by `corpus/SOURCES.md:28` (`opened 2026-10-20`, verified 2026-10-20, 365d window) and `corpus/SOURCES.md:69` ("Searched the fixed eight official sources listed in S020–S027 on 2026-10-20").
2. **Is "this round" a false indexical?** No. Both commits that wrote line 2 belong to round 22. At base, round 23's reopen list (`SOURCES.md:73`: "Re-opened this round without row changes: S021, S023, S024, S025, S026") does not include S020, so no later reading was misattributed to this line. Round-24 material was not read, per the bounds.
3. **Has the source drifted, so that an old date masks stale content?** No.
   - The retained bytes match the manifest (`fetched/manifest.json:358-374`): `gzip -dc fetched/S020-1.raw.gz | sha256sum` gives `87a13951ce93195e9a52915e6d170eebd4c48260576b637407bb96ea8c47f5e4`, 18428 bytes.
   - I made one plain public GET of the URL already in SOURCES (not saved): `curl -sS -w 'HTTP %{http_code} bytes %{size_download}\n' -o >(sha256sum) https://www.rfc-editor.org/rfc/rfc6596.html` returned `HTTP 200 bytes 18428`, sha256 `87a13951…f5e4`. The live page is byte-identical to the retained bytes.
   - Literal counts in `fetched/text/S020-1.txt` are `Category: Informational` 1, `Obsoletes` 0, `Updates` 0. The raw HTML has no "obsoleted by" or "updated by" marker.
4. **Is the freshness window expired?** No. SOURCES gives S020 a 365-day window, verified 2026-10-20, so it was 1 day old at recheck.
5. **Does the rejection rely on a rule the candidate wrote for itself?** Partly, but the result does not depend on it. The rule in `corpus/QUALITY.md:217-221` ("A historical verified-at date … is not a stale claim; record it as a note") is new in `e28312b` (base count of "Recheck adjudication" = 0). However, the rule already in force at base, `QUALITY.md:46-48`, says: "A provenance header records the original evidence date/revision … installing a header is never live re-verification." Under that rule, a header date is a record of when the evidence was taken, not a freshness claim, and the base rule alone supports the rejection.
6. **Did the candidate still add a STALE correction, or count one, for S020?** No. `git diff 97404de… e28312b… -- corpus/knowledge/static-canonical-preflight.md` adds no `[r26-recheck S020 STALE]` tag. The note required by the rejection is present at candidate line 184: "Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten." `measure.py:441-454` counts corrections from the ledger's `stale` field, not `seatStale`, so S020 `stale: 0` requires no tag. This is consistent with 8/8.

## Side findings (not about the rejection)

- **Low, provenance.** The seat records `fetched/text/S020-1.txt` sha256 `bd0283930f510c3a…` at `w1/PairS020StaticCanonicalPrefl.md:7`. The committed file (`git show e28312b:.ufo/waves/round-26/fetched/text/S020-1.txt | sha256sum`) is `febc2d99f8f02f301ddf651edbd5595c04d53489ec2f71b7be1867d04dff490e`, 11893 characters. `RowS020.md` says 11,883. The likely cause is re-extraction after `source_text.py` and `text_selftest.py` landed (single-unescape rule, `QUALITY.md:222-224`) [INFERENCE]. All ten seat quotes still occur exactly once in the committed text, so no verdict changes. The fix is a one-line note that the hash belongs to a pre-re-extraction text view.
- **No action needed (seat F3, R4).** "preferred" appears at offsets 381-2414 (Abstract and §1) and 6734-9307 (§4 and §5), but not inside §3 (offsets 2926-6608). Line 13's "section 3 defines a preferred IRI" is therefore imprecise about the section. The teaching holds at the source level, and HOLD with a note is correct.

## Impacted axes and correction

- Freshness: nothing hidden. The date is a correct historical stamp, the source is byte-identical live, and the window is not expired.
- Correction needed for the rejection: none. Optionally, add the text-hash note above to the seat report.

Tooling: nothing installed or upgraded. Used `git`, `gzip`, `sha256sum`, `grep`, `wc`, `python3` (read-only string counts) and one `curl` GET whose output was piped straight to `sha256sum`.

```json
{"target":"S020 L1 rejection of R2 verified-at date stamp (static-canonical-preflight.md:2)","verdict":"AGREE","severity":"none"}
```
