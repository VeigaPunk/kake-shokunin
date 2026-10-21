# Pair05A — (S004, corpus/knowledge/publish-channels.md) — freshness adjudication (r27 C1)

Seat: `KakeR27.Pair05A` (read-only reviewer, leaf, no dispatch). Axis judged: **freshness**.
Measured revision: `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (declarations commit; frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`).
Verdict: **HOLD** (no STALE marker required; no correction needed).

## 1. Where the citation is, and how the pair arises

`corpus/knowledge/publish-channels.md` contains **no literal `S004`**. The pair exists only because
the C1 range rule expands the token `S001-S007` on the `verified-at:` prefix line.

- Citing line (only line producing the pair), `corpus/knowledge/publish-channels.md:2`:

  `verified-at: 2026-09-26 (kimi-webbridge "not supported on Linux" check) and 2026-09-28 (round-1 commit cd5b381 that introduced this entry; wz1-ds4cc emptied 2026-09-28T21:42-03:00); round-20 corrections 2026-10-19 (S001-S007 opened that day) — historical-not-live-reverified; no live domain recheck performed`

- Expanded range `S001-S007` → S001…S007; members S004 and S006 are *range-only* (no literal `S004`
  anywhere in the file: the only `S00x` lines are 1, 2, 58, 59, 60, 61, 84; lines 58-61 and 84 carry
  only S001, S002, S003, S005, S007 literals).
- Canonical pre-declared "before" state confirms this pair is one of the 16 unadjudicated:
  `.ufo/waves/round-27/c1-before.json` → `missing` contains `{"row":"S004","file":"corpus/knowledge/publish-channels.md"}`
  (measured at base `83528f7c…`: 57 citing pairs, 41 decided, 16 missing). My independent replication of
  `count_c1.py`'s regexes over `corpus/knowledge` at `be375d9…` reproduces that exact 16-pair list.
- r26 already adjudicated `S001,S002,S003,S005,S007 × publish-channels.md`
  (`.ufo/waves/round-26/statements.json`), but **no `S004 × publish-channels.md` row** — hence this seat's row.

## 2. What the citing line actually asserts for S004 (scope test)

The parenthetical `(S001-S007 opened that day)` is **historical source-date metadata**, not a substantive
platform claim. Its stated scope for S004: *S004 was among the sources opened on 2026-10-19*.

What it does **not** assert: that S004 supports any claim in this entry. The entry itself restricts the
support set on line 1:

- `corpus/knowledge/publish-channels.md:1` — `source: S001, S002, S003, S005 and S007 in corpus/SOURCES.md support the EOF round-20 corrections;` (S004 and S006 deliberately absent)
- `corpus/knowledge/publish-channels.md:84` (r26 EOF provenance) — `The round-20 correction lines in this entry cite S001, S002, S003, S005 and S007 (lines 58-61).`

So S004 enters this file as a **member of the opened-batch range**, not as an attribution of content.

## 3. Evidence for the asserted scope (source-date claim)

Located support (exact substrings, verified present in the blobs at `be375d9…`):

1. `corpus/SOURCES.md:12` (registry row S004, opened date cell):
   `Configuring the upload-pages-artifact action; fetched 2026-10-19`
   Full row also carries `| S004 | GitHub Docs: Using custom workflows with GitHub Pages` and
   `used-by … corpus/knowledge/ghp-served-set.md` (i.e. S004's *content* is used only there — consistent
   with this file mentioning S004 for provenance only).
2. `corpus/lessons/round-20.md:206` (r20 tail row S004): `“Configuring the `upload-pages-artifact` action”; first and second paragraphs; fetched 2026-10-19.`
3. `.ufo/round-20/resume/sources-gate.md:26-30` (round-20 gate): `- Accessed: 2026-10-19` under `## S004 — Using custom workflows with GitHub Pages`.
4. `corpus/SOURCES.md:101`: `No source ids are void: all S001-S018 were opened.` — the batch reading of the range is corroborated in-repo.

All three records agree on 2026-10-19; the historical date is preserved verbatim (no re-dating).

## 4. Liveness / freshness cross-check of the cited source itself

- r27 wave fetch (this round): `.ufo/waves/round-27/fetched/manifest.json` → row `S004`, index 1,
  `status 200`, `error null`, `fetchedAt 2026-10-21T19:59:55.714609+00:00`, `bytes 141818`,
  `sha256 9ee0766a2fb78e5af104bbc97dfe32ba09ebd8f2d68df1ed2d49efc081a5f53a`.
- The r26 receipt for the same row: `.ufo/waves/round-26/rechecks/S004.json` → verdict `HOLD`,
  quote `The tar file must be under 10GB in size and should not contain any symbolic or hard links`,
  anchor `Configuring the upload-pages-artifact action`, sha256 `5c15ef2d…`.
- The r26→r27 digest change (`5c15ef2d…` → `9ee0766a…`) is **page-build churn only**: the diff ops are
  Next.js `buildId` (`ndrfAHwVnt-w5Yffjl7If` → `gOeUVmJQ7z9zrUAITPynv`) and `/_next/static/chunks/*.js`
  filename hashes; after stripping `<script>` blocks and `/_next/static/...` tokens the article prose is
  **identical** (20693 == 20693 chars). The r26 quote and anchor are verbatim present in the r27 text
  (checked against `.ufo/waves/round-27/fetched/text/S004-1.txt`).
- **Irrelevant retry boilerplate — excluded:** `.ufo/waves/round-26/fetched/manifest-retry.json` contains
  exactly one entry, `S008` (`reason: first attempt TimeoutError at 60s; single retry with 240s timeout`).
  S004 has **no** retry record in r26 (single `S004-1.raw.gz`, status 200) and **no** retry in r27
  (`error: null`). Nothing in the retry artifact bears on this pair.

## 5. Verdict and reasoning

**HOLD** — support at the stated scope.

- The only claim the S004 member of the range makes (S004 opened 2026-10-19) is supported by three
  independent in-repo records of that date (SOURCES.md:12, round-20 lesson:206, sources-gate.md:26-30),
  and by the in-repo statement that S001-S018 were all opened (SOURCES.md:101).
- The cited source is live and materially unchanged as of 2026-10-21T19:59Z (r27 fetch status 200; r26
  quote/anchor verbatim present; only build-hash churn in the bytes).
- No claim in `publish-channels.md` depends on S004's content: the entry's r20 corrections (lines 58-61)
  and the r26 EOF (line 84) both list exactly S001, S002, S003, S005, S007. S004's teaches ("artifact
  shape and deployment requirements") do not contradict anything the entry asserts (c1–c7 live checks).
- Not **STALE**: no wrong date, no contradicted attribution, no unsupported content claim at the token's
  own scope. The only defect is *precision*: the range over-includes S004/S006 relative to the ids this
  entry actually cites — a scoping imprecision, not a false statement, and already disclosed by the file
  itself at line 84.
- Not **UNVERIFIABLE**: the metadata claim is decidable from in-repo evidence; the r27 re-fetch removes any
  doubt that the source still resolves (note: the *historical* open date rests on corpus self-attestation;
  the re-fetch corroborates liveness/content, not the 2026-10-19 timestamp).

**Inferential step, labelled:** the range token `S001-S007` is read as *the round-20 source batch opened
2026-10-19*, not as a per-claim support set. This reading is required because line 1 independently fixes the
support set to S001, S002, S003, S005, S007 and line 84 restates it. Under the alternative reading
(range = per-claim support set), the token would be an unsupported attribution for S004/S006; that
reading is contradicted by lines 1 and 84 of the same file, so it is not the file's own scope.

## 6. Suggested C1 ledger record (contract C1 schema)

`kind: artifact` is recommended for this row because the claim adjudicated is registry/metadata
provenance; the source's own text does not state its open date. `kind: source` is valid **only if** the
r27 `fetched/` tree is committed at the measured revision (count_c1 reads fetched blobs at `--revision`;
`fetched/` is currently untracked — see §7).

```json
{
  "row": "S004",
  "file": "corpus/knowledge/publish-channels.md",
  "kind": "artifact",
  "verdict": "HOLD",
  "evidence": "corpus/SOURCES.md",
  "contains": "| S004 | GitHub Docs: Using custom workflows with GitHub Pages — https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages | docs | A | Artifact shape and deployment requirements for custom workflows | Configuring the upload-pages-artifact action; fetched 2026-10-19 |",
  "reason": "Citation is historical source-date metadata: publish-channels.md:2 reads 'round-20 corrections 2026-10-19 (S001-S007 opened that day)', so the S004 member of the expanded range asserts only that S004 was opened 2026-10-19. Supported at that scope by corpus/SOURCES.md:12 ('Configuring the upload-pages-artifact action; fetched 2026-10-19'), corpus/lessons/round-20.md:206 (S004 row, 'fetched 2026-10-19') and .ufo/round-20/resume/sources-gate.md:26-30 ('Accessed: 2026-10-19'); SOURCES.md:101 records that all S001-S018 were opened. The source itself is live and materially unchanged: r27 fetched/manifest.json row S004 index 1 status 200 sha256 9ee0766a2fb78e5af104bbc97dfe32ba09ebd8f2d68df1ed2d49efc081a5f53a contains the r26 quote 'The tar file must be under 10GB in size and should not contain any symbolic or hard links' verbatim under anchor 'Configuring the upload-pages-artifact action'; the r26->r27 digest delta is Next.js buildId/chunk-hash churn only, article prose identical. No claim here depends on S004 content: lines 58-61 and the r26 EOF at line 84 both restrict this entry's citations to S001, S002, S003, S005 and S007. Inferential step: the token 'S001-S007' denotes the round-20 opened batch (SOURCES.md rows S001-S007 all 'fetched 2026-10-19'), not a per-claim support set; line 1 fixes the support set to S001,S002,S003,S005,S007. Precision defect only (range over-includes S004/S006), not a stale premise, so no '[r27-recheck S004 STALE]' marker is warranted."
}
```

Variant if L1 prefers source-grounding (requires `fetched/` committed at the measured revision):

```json
{
  "row": "S004", "file": "corpus/knowledge/publish-channels.md", "kind": "source",
  "verdict": "HOLD", "fetchIndex": 1,
  "quote": "The tar file must be under 10GB in size and should not contain any symbolic or hard links",
  "anchor": "Configuring the upload-pages-artifact action",
  "reason": "<as above>; the quote/anchor are re-verified in the round-27 fetch of S004 (sha256 9ee0766a…), so the cited source remains live and unchanged while the open-date half of the claim is carried by corpus/SOURCES.md:12 and corpus/lessons/round-20.md:206."
}
```

Note for the integrator: `count_c1.py` checks `kind=source` rows against `git show <revision>:.ufo/waves/round-27/fetched/...`;
`fetched/` is currently untracked, so source-kind rows fail at any revision until that tree is committed.
`kind=artifact` rows pointing at committed paths (`corpus/SOURCES.md`) validate unconditionally.

## 7. Suggested appended wording

**No STALE correction is required** for this pair, and adding the token `[r27-recheck S004 STALE]` would be
false (it would assert staleness that the evidence does not support). Optional precision note, append-only,
for the next round (not required by the contract; it does not change any verdict):

```
- Base `corpus/knowledge/publish-channels.md:2`: **[r27-recheck 2026-10-21: the parenthetical `(S001-S007 opened that day)` names the round-20 source batch opened 2026-10-19; this entry's round-20 corrections cite only S001, S002, S003, S005 and S007 (lines 58-61), so S004 and S006 occur in the range as batch members only, not as support for any claim in this entry — S004, S006]**
```

Pairing side-effect check: every id in that wording is **already** a citing pair for this file
(S001, S002, S003, S005, S007 from r26; S004, S006 from this round), so the note does **not** grow the C1
denominator. Any wording that introduced an id not already paired with this file would enlarge the
denominator monotonically (allowed, but it would create a new obligation for the ledger).

## 8. Uncertainties / residual risk

- The historical open date (2026-10-19) is **self-attested by corpus metadata** (registry + round-20 gate
  + r20 tail). No independent timestamped third-party record is retained in-repo, and the r27 re-fetch
  (2026-10-21) cannot confirm a past open date. Flagged as an honesty limit, not a blocker.
- The r27 `fetched/` tree is untracked at `be375d9…`; any `kind=source` row (mine or another seat's) will
  fail `count_c1.py` until it is committed at the measured revision.
- Registry `used-by` drift (pre-existing class, r21 `TrendQuality.md` F8): SOURCES.md's S004 row lists
  `used-by … ghp-served-set.md` only, while S004 also appears in this file's range token. Because that
  appearance is provenance-only (no use of S004's content), no `used-by` change is required — flagged
  informationally for L1, not adjudicated here.
- Scope limit of this seat: I judged only the (S004, corpus/knowledge/publish-channels.md) pair. The
  structurally identical sibling pair (S006, corpus/knowledge/publish-channels.md) — same line 2, same
  range token — is a separate obligation; my reasoning above applies to it by symmetry, but it is not
  decided here and must be adjudicated on its own row (and it would need its own
  `[r27-recheck S006 STALE]` marker if judged STALE — which the same evidence does not support).
- I did not fetch, retry, or re-open any r24-stopped work; no r24 artifact was read.

## 9. Tooling

No tool installs or updates performed this seat (no tool needed; no pacman transaction attempted —
host-wide pacman is PAUSED).

Report: `.ufo/waves/round-27/w1/Pair05A.md`
