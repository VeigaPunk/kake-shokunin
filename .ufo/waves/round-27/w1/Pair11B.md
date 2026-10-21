# Pair11B — critic: (S008, corpus/knowledge/crawl-scope-per-host.md)

Seat: KakeR27.Pair11B (critic, leaf, read-only). Axis judged: freshness. Milestone: r27-full-citing-set.
I did not read the A report (Pair11A).

## Verdict

**HOLD (kind: artifact).** The only S008 token in this file is r26 round-wide fetch provenance. That provenance is true at its own stated scope. The line does not attribute any crawl-scope claim to S008. No STALE correction is owed.

## The citing line, found and expanded

- File: `corpus/knowledge/crawl-scope-per-host.md`. Its blob is identical at the frozen base `83528f7` and at the declarations commit `be375d9`: git blob `a05625c9dad9282a3905dad8b957342c0c4a5c2d`, sha256 `aea5d1579b1cec8ccefb30de600cce710f885bfddfd33c60a8809b7a609af691`. The sha256 matches `frozen/expected.json:9`.
- The `count_c1.py` regexes give these literal ids for this file: S008, S011, S012, S013. There are **no ranges**. S008 appears on **line 57 only**.
- Line 57 is the `## Round-26 source recheck` tail, which is r26 end-of-file prose. The S008 clause sits inside the round-wide provenance parenthetical:
  > Rows S011, S012 and S013 were re-fetched by one public GET each (`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`) and judged HOLD at their anchors against the retained bytes
- The surrounding claim: the grammatical subject, the "one public GET each" count, and "judged HOLD" all cover S011, S012 and S013. S008 appears only as a provenance aside saying its fetch is recorded in the retry manifest.
- The entry's own source header (line 1) reads `source: S011, S012, S013 (corpus/SOURCES.md)`. S008 is not a source of this entry.

## Scope test: what the S008 clause claims

The clause makes one claim: in r26, S008's bytes were obtained through `manifest-retry.json` rather than `manifest.json`.

| Check | Evidence (repo path at `83528f7`; identical blob at `be375d9`) | Result |
|---|---|---|
| A retry manifest exists and records S008 | `.ufo/waves/round-26/fetched/manifest-retry.json`: one entry, `"row": "S008"`, `"attempt": 2`, `"status": 200`, `"reason": "first attempt TimeoutError at 60s; single retry with 240s timeout"`. Blob `637e278d…` is unchanged at `be375d9`. | true |
| The first attempt really failed, so the retry was needed | `manifest.json` S008 entry: `"status": null`, `"error": "TimeoutError: The read operation timed out"`, `bytes 0`, sha256 = the empty-input hash `e3b0c442…` | true |
| The retained retry bytes match the recorded hash | `gzip -dc S008-1-retry.raw.gz \| sha256sum` gives `93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084` and 512359 bytes. Both equal the manifest values. | true |
| S008 was judged on the retry bytes | `.ufo/waves/round-26/rechecks/S008.json`: `"verdict": "HOLD"`, reason begins "Commit-pinned texi re-fetched 2026-10-21 (attempt 2 after a 60s timeout)". Blob `22a7d881…` is unchanged. | true |
| The round record agrees | `corpus/lessons/round-26.md:23` contains "S008 first timed out at 60 s and was retried once". `corpus/SOURCES.md:79` contains "34 fetches; S008 one retry after a 60 s timeout". | true |

## Counterexamples tried (strongest first)

1. **False attribution: S008 presented as a source for crawl scope.** Rejected. The clause's subject and "judged HOLD at their anchors" cover only S011, S012 and S013. Line 1 names only those three. `corpus/SOURCES.md:16` lists S008's used-by as `corpus/knowledge/ghp-served-set.md` only. S008's scope is "GNU tar exclusion-pattern defaults", which is unrelated to robots or sitemaps. Nothing in the file relies on S008 for a claim.
2. **"One public GET each" contradicted by S008 needing two GETs.** Rejected. S008 is outside the "each" set. In `manifest.json` (34 entries), S011, S012 and S013 each have exactly 1 entry with status 200, so the count holds for its own subject.
3. **The provenance is not reproducible.** The retry ran as an inline heredoc, and no committed code produced `manifest-retry.json`. This is already disclosed at `corpus/lessons/round-26.md:76` ("the manifest remains the evidence, the file documents the procedure"). The citing line claims only where the manifest is, not how it was produced, so this does not falsify it.
4. **Stale premise against current source dates.** Rejected. `corpus/SOURCES.md:16` still records S008's last opening as 2026-10-19 with a 365d recheck, and `:79` records the 2026-10-21 r26 recheck. The clause is dated r26 history ("2026-10-21, append-only"). It makes no present-tense claim about S008's upstream bytes, which the URL pins to commit `cfdb891b…`. No r27 S008 fetch exists (`round-27/fetched/manifest.json` covers S001–S006 only), and none is needed to decide this historical clause.
5. **Locator ambiguity.** The bare name `manifest-retry.json` resolves against the directory given in the same parenthetical (`.ufo/waves/round-26/fetched/`). There is exactly one such file in the repo tree, so it is resolvable. This is precision only, not a staleness issue.
6. **r20 tails.** `round-20-verifier-spotcheck.md:12` and `round-20.md:310` mention the withdrawn S008 "1.35" label. That erratum is about `ghp-served-set`/`ghp-etag-anatomy` wording. It is not about this file and does not touch line 57.

## Distinction (stale premise / source date / irrelevant boilerplate)

- **Stale premise:** none.
- **Source date:** none at issue. Historical dates are preserved: 2026-10-19 for the opening, 2026-10-21 for the r26 retry at 15:11:01Z.
- **Irrelevant retry boilerplate:** yes. The same parenthetical is copied into 4 knowledge files besides `ghp-served-set.md`: crawl-scope-per-host:57, ghp-custom-domain:62, ghp-etag-anatomy:60 and static-canonical-preflight:184. r26 critic `.ufo/waves/round-26/w2/Rejection07S013.md` (item 2) already called it "true of the round but irrelevant to this entry … a provenance-precision nit, not staleness." I agree.

The consequence for C1: this pair exists only because the boilerplate exists. Three sibling oracle pairs share the same basis: S008 with ghp-custom-domain, ghp-etag-anatomy and static-canonical-preflight (all in `c2-oracle.json`). Their reviewers should reach a consistent artifact HOLD on the same retry-manifest evidence, unless their line context differs.

## Suggested C1 ledger record (`pairs.json` → `pairs[]`)

```json
{"row":"S008","file":"corpus/knowledge/crawl-scope-per-host.md","kind":"artifact","verdict":"HOLD","evidence":".ufo/waves/round-26/fetched/manifest-retry.json","contains":"\"file\": \"S008-1-retry.raw.gz\"","reason":"Only citation is line-57 r26 EOF provenance '(…manifest.json, S008 via `manifest-retry.json`)': round-wide fetch metadata, not attribution of any crawl-scope claim (entry sources S011–S013; SOURCES usedBy S008=ghp-served-set.md). Retry manifest records S008 attempt 2, status 200, sha256 93281a63…; retained bytes re-hash equal; r26 receipt S008.json HOLD. Carried r26 provenance, not an r27 fresh source observation."}
```

The `contains` check passes. In Python, `'"file": "S008-1-retry.raw.gz"' in git show <rev>:.ufo/waves/round-26/fetched/manifest-retry.json` returns True at both `83528f7` and `be375d9`. That is the same test `count_c1.py` applies to artifact rows.

## Correction wording

None is required, because the verdict is not STALE and `[r27-recheck S008 STALE]` must **not** be added. If L1 wants to remove the scope ambiguity, it may append this optional, non-STALE clarification (append-only, original lines unchanged):

> - Round-27 note (append-only): the "S008 via `manifest-retry.json`" aside above is round-26 fetch provenance (`.ufo/waves/round-26/fetched/manifest-retry.json`); S008 is not a source of this entry.

## Uncertainties

- The verdict depends on L1 accepting artifact-kind evidence for r26 EOF provenance. The contract allows this: an artifact needs an evidence repo path and a contains substring. I made no source-kind observation of S008 in r27.
- I did not run `count_c1.py` or the gate, as the seat bounds require.

## Commands and tooling

I used read-only commands only: `git show`, `git grep`, `git rev-parse`, `git log`, `gzip -dc | sha256sum | wc -c`, `rg`, and inline Python stdlib over git blobs. There was no network GET, no r24 material, and no edits other than this report. Installs or updates: none.
