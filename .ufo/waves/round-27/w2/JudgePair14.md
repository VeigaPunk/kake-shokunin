# JudgePair14 — (S008, corpus/knowledge/static-canonical-preflight.md) — axis: freshness

Seat `KakeR27.JudgePair14`, reviewer (leaf, no dispatch). Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; every Git read used that full hash. Read-only source; only this report written. Scratch `/fast/scratch/hyaku/kake-r27/JudgePair14/` (TMPDIR set there). No installs, no pacman transaction, no commits/index/jj/remote change (`git status --porcelain --untracked-files=no` and `git diff --cached --stat` both empty at end).

## Verdict

**CONFIRM `HOLD`, `kind:"artifact"`** for this pair at its own stated scope. The verdict is right; one **low-severity factual defect in the durable ledger `reason`** is real (F1) and verdict-neutral.

## Attacked item and its scope

`pairs.json` row (sha256 of pairs.json at candidate = worktree = `f1fa20cab67053fea3945330d14efa59f095ede22b6dacbb058d688d0b376a6a`):
`{"row":"S008","file":"corpus/knowledge/static-canonical-preflight.md","kind":"artifact","verdict":"HOLD","evidence":".ufo/waves/round-26/fetched/manifest-retry.json","contains":"\"file\": \"S008-1-retry.raw.gz\""}`.

Citing text, `corpus/knowledge/static-canonical-preflight.md` (candidate blob `7bcf31ddab3689e269ca5d085d5543dad6a2daac`, sha256 `40ebd1da…`; base/declaration blob `d86ddec6…`, sha256 `833b28f2…`):

- **L184** (r26, unchanged at base, declarations and candidate): "Rows S020, S021, S026, S027, S028, S029, S030, S031, S032, S033 and S034 were re-fetched by one public GET each (`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`) and judged HOLD at their anchors against the retained bytes…"
- **L244** (added in the candidate commit, in the new `## Round-27 grouped-citation adjudication` block starting L205): "The line184 S008 retry aside is historical artifact provenance only, not GNU-tar support for this entry. All three pairs are explicitly adjudicated."

Stated scope of the S008 mention = round-26 **retrieval provenance** (which manifest holds S008's row). It is **not** a content citation: the entry's `source:` header (L1) lists S020,S021,S026,S027,S028,S029 — S008 absent; `corpus/SOURCES.md:16` gives S008 `used-by = corpus/knowledge/ghp-served-set.md` only; grep for `anchored|wildcard|GNU tar|tar\.texi|exclusion member` over the whole file returns **0 hits** — no tar-semantics claim exists here to support.

## F1 (low, verdict-neutral): the ledger `reason` asserts a citing-set fact the candidate itself invalidated

`reason` says "**The only row mention** is r26 EOF retrieval provenance…". True at `be375d9` (S008 mentions = 1). **False at the frozen candidate**: S008 mentions = **2** (L184 r26 provenance, plus L244 — the candidate's own appended r27 clarification). The reason text was carried over unchanged when the appended block was written in the same commit that froze the candidate. Impact: the verdict is unaffected (L244 says the same thing, so the pair is still provenance-only), and `count_c1.py` does not inspect reason semantics — but the durable record misstates the citing set of the file it adjudicates, and the identical reason string is shared verbatim by the other three S008 rows (crawl-scope-per-host / ghp-custom-domain / ghp-etag-anatomy), where the "only mention" claim *is* still true (1 mention each at candidate). Smallest fix: state both occurrences, e.g. "L184 r26 EOF provenance and the L244 r27 clarification both name the round-26 retry location; no claim of this entry is attributed to S008." No STALE marker is warranted; the appended L244 text is itself accurate.

## Verification (expected declared before each run)

| probe | expected | actual |
|---|---|---|
| `git cat-file` candidate vs base blob of the citing file | candidate = base + append-only r27 block (44 added lines at 204) | diff = `@@ -203,0 +204,44 @@` only; base/declaration sha256 `833b28f2…` both; candidate `40ebd1da…` |
| S008 mention count in that file at base / declarations / candidate | 1 / 1 / 2 | 1 / 1 / **2** (L184, L244) → F1 |
| `manifest.json` S008 slot | failed first attempt, so "via manifest-retry.json" is precise | `status:null`, `error:"TimeoutError: The read operation timed out"`, `bytes:0`, `sha256 e3b0c442…b855` (= SHA-256 of empty), `file S008-1.raw.gz`; **S008 is the only non-200 row in 34** |
| `manifest-retry.json` content | single S008 row, attempt 2, status 200 | exactly one record: `row S008, index 1, attempt 2, status 200, bytes 512359, sha256 93281a63…6084, file "S008-1-retry.raw.gz"`, `reason "first attempt TimeoutError at 60s; single retry with 240s timeout"`; the ledger `contains` needle occurs **exactly once** |
| retained bytes vs manifest digest | equal | gunzip `S008-1-retry.raw.gz` → 512359 B, sha256 `93281a63…6084` = manifest value; `S008-1.raw.gz` → 0 B, sha256 `e3b0c442…b855` = manifest value |
| artifact blobs base / declarations / candidate | byte-identical (r26 not rewritten) | sha256 `84e83fb0cf5bf431eb029a9ab8cab69b661054e6e992b862e87b514786a65d1b` at all three; `git diff base..candidate -- .ufo/waves/round-26/` empty |
| r26 receipt `rechecks/S008.json` at candidate | HOLD, fetchIndex 1, anchor claims true of the bytes | verdict HOLD, fetchIndex 1, sha256 `9e39e7da…`; in the bytes: `@node controlling pattern-matching` L8480, `@unnumberedsubsec Controlling Pattern-Matching` L8481, `--no-anchored for exclusion members` L8587-8588, "the default for exclusion members" L8602-8604, `Exclusion --wildcards --no-anchored --wildcards-match-slash` L8618 — every claimed line number checks out |
| live re-fetch of the S008 official URL (SOURCES.md:16, pinned commit `cfdb891…`) | HTTP 200, identical content digest + ETag, if the source is still the same | `curl -sS` GET → `http=200 size=512359`, sha256 `93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084` (identical to r26 retained bytes), `etag "9b668bb3c441a095e7c39a7baa7f88a93599ab4c"` = r26 recorded ETag. Caveat: `curl -I` (HEAD) returns **502** while GET returns 200 → do not use HEAD as authenticity evidence. Live bytes kept in scratch only; nothing committed |
| r26 receipts for the L184 named rows | all HOLD | S020,S021,S026,S027,S028,S029,S030,S031,S032,S033,S034 → HOLD, fetchIndex 1 |
| citing-set sweep (independent re-implementation of the frozen literal+range grammar over all `corpus/knowledge`) | 57 at base → 58 at candidate, only the known S013 discovery added, no pair removed | 57 → 58; added = {S013×ghp-served-set}; removed = ∅; this file: 22 pairs at both revisions |
| counter `count_c1.py --root . --revision ac46a74` | S008×preflight decided, valid, no marker needed | exit 1; citing 58 / reviewed 58 / decided 55 / known-unverifiable 7 units in 3 pairs; outcome for this pair `verdict HOLD, valid True`; `missing` = S001×ghp-served-set, S007×ghp-custom-domain, S033×static-canonical-preflight (all carried-UNVERIFIABLE, none of them this pair). C1 stays UNPROVABLE — 58 review records are not 58 strictly decided |

## Dissent considered and resolved (S005 preflight, S005/S003 sitemap, S004 ghp steps)

- **S005 preflight** (this same file, `[r27-recheck S005 STALE]` at L235, ledger verdict STALE): the correction narrows the L54 range to S001,S002,S003,S004,S006. **S008 was never in that range**, and S008 is not a source of this entry (no header row, no tar-semantics content, `used-by` elsewhere), so narrowing S005 leaves the S008 provenance aside untouched. The candidate's own L244 note is consistent with that narrowing.
- **S005/S003 sitemap** (`sitemap-orphan-audit.md`, S003 HOLD / S005 STALE on the same `S001-S006` token): different file; no bearing on this pair.
- **S004 ghp steps** (`ghp-served-set.md`, `[r27-recheck S004 STALE]` at L99): S004's numbered-flow attribution is reassigned to S003; the S008 row of that file is untouched. Note the real contrast: in `ghp-served-set.md` S008 **is** a genuine source (header L1, tar anchor at L34), so its L83 sentence mixes a real S008 citation with the retry parenthetical and needed the extra `:95` / `:108` clarifications; here S008 is provenance-only and the candidate's L244 supplies the equivalent disambiguation. The two files must not be given one shared reading.
- **Residual interpretive risk (accepted):** a reader could attach L184's "one public GET each" to S008 via the parenthetical. Here S008 is not among the named rows, so the wording does not cover it; in `ghp-served-set.md` it does, which is why that file carries the attempt-count clarification. Verdict unchanged.

## Uncertainties / gaps

- Live re-verification of the S008 source was done by this seat (one public GET, benign public documentation, pinned commit URL from SOURCES.md:16); the ledger record itself is r26-artifact-scoped and correctly does not claim a fresh r27 opening (the r27 fetch manifest holds S001–S006 only).
- The manifest's `last-modified` header is **response-time, not content-version** (r26 recorded `15:11:02 GMT`, live `22:11:25 GMT` for byte-identical content with identical ETag). No freshness or provenance date may be derived from that header; content digest/ETag are the reliable identity. Recorded as informational, not a defect in this pair.
- `reason` semantics are not machine-checked by `count_c1.py`; F1 therefore does not move any count and cannot regress the gate.
- No r24 material was read, retried, rephrased or rerouted; no live source, doc or registry file was edited.

## Tooling

No tool installed or upgraded; no pacman transaction; no service mutation. Read-only git (`cat-file`, `ls-tree`, `diff`, `log`), `grep`, `sha256sum`, `python3 -B` (stdlib only), `curl` (one GET + one HEAD to the named public source, bytes to scratch only).

Report: .ufo/waves/round-27/w2/JudgePair14.md
