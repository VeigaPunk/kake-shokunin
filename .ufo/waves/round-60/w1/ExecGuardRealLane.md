# ExecGuardRealLane

C2 grounding on the real lane. Classifier: `.ufo/waves/round-60/w1/ExecGuardRealLane.files/classify_lane_changes.py`
(stdlib only; `git diff-tree -r --find-renames -z` per commit and per endpoint; byte-level `split(b"\n")`; existence-of-
alignment DP matching contract rule; visible tag = `\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]` outside `<!-- -->`
comments and backtick spans). Window "since round 50" = `9619af67..97cdc12` (round-50 opens after the round-49
verifier-spot-check `9619af67`, convention base = previous round's spot-check; measured tip = contract base `97cdc12`).
38 corpus commits touch `corpus/knowledge/`; all in-scope entries are `A` or `M` — no `D`, no `R`, no mode/type changes
(audit of every raw status in the window: 18 `A` + 24 `M` on `corpus/knowledge/*.md`; the one `M nonmd` is
`freshness-pins.json`, out of scope). No file in scope was renamed or deleted in the window.

## CHANGES:

Per-commit classification of `corpus/knowledge/**/*.md` (commit range = `c^..c`):

| commit | round | status/path | classification |
|---|---|---|---|
| ff3f6ecff5 | r50 | A crawl-error-status-table.md | new file (unchecked) |
| 5591557956 | r51 | A canonical-selection.md | new file |
| 5591557956 | r51 | A crawler-identity.md | new file |
| 907790c780 | r51 | M canonical-selection.md | **changed** (rewrite, base line 37) |
| 907790c780 | r51 | M crawler-identity.md | **changed** (rewrite, base line 12) |
| 5422ff3901 | r52 | A baidu-friendly-crawl-guidance.md | new file |
| 5422ff3901 | r52 | A baidu-mobile-matching-error-causes.md | new file |
| 5422ff3901 | r52 | A yahoo-japan-rel-nofollow-semantics.md | new file |
| 755914926e | r53 | M baidu-friendly-crawl-guidance.md | pure EOF append (+4 lines) |
| 755914926e | r53 | M baidu-mobile-matching-error-causes.md | pure EOF append (+4 lines) |
| 8e408e00fb | r54 | M yahoo-japan-rel-nofollow-semantics.md | **untagged_insertion :52** |
| 2bda8e4227 | r55 | A yahoo-japan-robots-pattern-syntax.md | new file |
| 2bda8e4227 | r55 | A yahoo-japan-robots-txt-basics.md | new file |
| 2bda8e4227 | r55 | A yahoo-japan-robots-txt-refusal-rules.md | new file |
| faf9abe81d | r55 | M crawl-scope-per-host.md | pure EOF append (+7 lines) |
| faf9abe81d | r55 | M robots-txt-rules.md | pure EOF append (+7 lines) |
| faf9abe81d | r55 | M yahoo-japan-rel-nofollow-semantics.md | pure EOF append (+7 lines) |
| faf9abe81d | r55 | M yahoo-japan-robots-pattern-syntax.md | **changed** (rewrite, base line 24) |
| faf9abe81d | r55 | M yahoo-japan-robots-txt-basics.md | **changed** (rewrite, base line 3) |
| faf9abe81d | r55 | M yahoo-japan-robots-txt-refusal-rules.md | **changed** (rewrite, base line 69) |
| 64c0ce12ff | r55 | M yahoo-japan-robots-txt-refusal-rules.md | **changed** (rewrite, base line 21) |
| d5afc48acd | r56 | A yahoo-japan-deleted-url-recrawl.md | new file |
| d5afc48acd | r56 | A yahoo-japan-link-target-crawl-restriction.md | new file |
| d5afc48acd | r56 | A yahoo-japan-nonexistent-url-recrawl.md | new file |
| f8438a282d | r56 | M yahoo-japan-deleted-url-recrawl.md | **changed** (rewrite, base line 6) |
| f8438a282d | r56 | M yahoo-japan-link-target-crawl-restriction.md | **changed** (rewrite, base line 1) |
| f8438a282d | r56 | M yahoo-japan-nonexistent-url-recrawl.md | **changed** (rewrite, base line 6) |
| cddef5b4fd | r57 | A baidu-dead-link-types.md | new file |
| cddef5b4fd | r57 | A baidu-spider3-dead-link-model.md | new file |
| 4b8c730504 | r57 | M baidu-dead-link-types.md | **changed** (rewrite, base line 91) |
| 32754df757 | r57 | M baidu-dead-link-types.md | **changed** (rewrite, base line 1) |
| 32754df757 | r57 | M baidu-spider3-dead-link-model.md | **changed** (rewrite, base line 4) |
| c1e39ef356 | r58 | A baidu-spider-identification.md | new file |
| c1e39ef356 | r58 | A baidu-spider-unblocking.md | new file |
| 8d340c1520 | r58 | M baidu-spider-identification.md | **changed** (rewrite, base line 39) |
| 8d340c1520 | r58 | M baidu-spider-unblocking.md | **changed** (rewrite, base line 8) |
| ab6e100e44 | r59 | A crawler-identity-signals.md | new file |
| ab6e100e44 | r59 | M crawler-identity.md | tagged mid-file insertion, tag `[r59-correction 2026-10-27]` at run start, rev line 35 |
| ab6e100e44 | r59 | A googlebot-verification.md | new file |
| b322ccabe1 | r59 | M crawler-identity-signals.md | **changed** (rewrite, base line 58) |
| b322ccabe1 | r59 | M crawler-identity.md | **changed** (rewrite, base line 36) |
| b322ccabe1 | r59 | M googlebot-verification.md | **changed** (rewrite, base line 8) |

## TAG SPELLINGS:

Run-start / in-window correction tags in corpus/knowledge (spellings matched against the contract regex):

- `**[r59-correction 2026-10-27]**` — 1 tagged insertion (matches regex; `**` bold is outside the brackets so the
  bracketed tag itself is visible). `crawler-identity.md:35` (rev `97cdc12`), inserted by `ab6e100e44`.
- `**[r54-correction 2026-10-25]**` — 1 occurrence; regex-correct spelling but sits on the run's third line
  (`yahoo-japan-rel-nofollow-semantics.md:54`; run starts line 52: `##` heading, blank, then the tag) → does not
  satisfy the rule.
- Near-miss historical spellings present at base but outside the window's insertions (pre-round-50; not flagged since
  not new insertions): `[r20-correction 2026-10-19: ...` (unclosed `[INFERENCE]` inside the bracket; fails regex —
  `sitemap-orphan-audit.md:125`), `[r23-correction]` (no date; fails — `static-canonical-preflight.md:140`),
  `[r2N-recheck S0NN STALE]` (different kind — e.g. `ghp-etag-anatomy.md:62`). No K9/K10-style tags inside
## EXPECTED R1:

Tool rule applied to endpoint diffs (`--base` → `97cdc12`, `corpus/knowledge/**/*.md`, committed blobs):

- `fd6303ce..97cdc122379711c2b02a8970752c8782da3ac81d` (contract R1): **exit 0** — 3 in-scope paths:
  `crawler-identity-signals.md` and `googlebot-verification.md` are new files (unchecked); `crawler-identity.md` is a
  tagged mid-file insertion (`[r59-correction 2026-10-27]` at run start, rev line 35). findings=0. The `b322ccabe1`
  rewrites are invisible to the endpoint rule because every `fd6303ce` base line survives in order.
- `64c0ce12..97cdc122379711c2b02a8970752c8782da3ac81d`: **exit 0** — 10 paths: 9 new files + the same tagged insertion
  in `crawler-identity.md`. The `faf9abe81d`/`64c0ce12ff` rewrites of r55-created files, the `f8438a282d`, `4b8c730504`,
  `32754df757`, `8d340c1520` rewrites all concern files created after `64c0ce12` → new-file at endpoints, unchecked.
- Last 10 rounds (r50–r59 as 10 per-round endpoint runs, base = previous spot-check → own spot-check): r50 0, r51 0,
  r52 0, r53 0, **r54 exit 1 (`untagged_insertion corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md:52`)**,
  r55 0, r56 0, r57 0, r58 0, r59 0. As one cumulative run `9619af67..97cdc12`: **exit 0** — 20 paths, findings=0:
  the two pre-r50 files `crawl-scope-per-host.md` and `robots-txt-rules.md` show pure EOF appends (+7 each,
  blank-first run); the other 18 paths are new files (unchecked) — including
  `yahoo-japan-rel-nofollow-semantics.md`, which did not exist at `9619af67`, so its r54 flagged edit is invisible
  at this endpoint.

## FLAGGED HISTORY:

Per-commit edits the contract rule would report if the tool ran per commit (facts, not failures — the tool is
endpoint-based and never ran historically; 18 flagged file-edits across 9 commits):

- `untagged_insertion` (1): `8e408e00fb` r54 `yahoo-japan-rel-nofollow-semantics.md:52` — 17-line correction block
  appended to a `\n`-terminated file; the run's first line is `## Round-54 correction — S374 crawl qualifier
  (2026-10-25)` and the tag `**[r54-correction 2026-10-25]**` sits on the run's third line (file line 54) → K8-style
  fail. (Also: under literal `split(b"\n")` semantics a non-blank-first append to a newline-terminated file is a
  mid-file run before the trailing `""` element — the same trap; the r55 appends escaped it only because the first
  appended line was blank, extending the `""` run.)
- `changed` (17): `907790c780` ×2 (canonical-selection.md, crawler-identity.md — r51 "mirror repair" rewrites);
  `faf9abe81d` ×3 (yahoo-japan-robots-{pattern-syntax,txt-basics,refusal-rules}.md); `64c0ce12ff` ×1
  (yahoo-japan-robots-txt-refusal-rules.md); `f8438a282d` ×3 (r56 Yahoo entries — heading/source-line rewrites);
  `4b8c730504` ×1 and `32754df757` ×2 (baidu-dead-link-types.md, baidu-spider3-dead-link-model.md); `8d340c1520` ×2
  (baidu-spider-identification.md, baidu-spider-unblocking.md); `b322ccabe1` ×3 (crawler-identity-signals.md,
  crawler-identity.md, googlebot-verification.md — r59 attempt-2 fidelity rewrites of r59-added lines).
- `deleted` / `rename` (0): none in the window.

Endpoint consequence (why the named ranges stay green): every `changed` commit above modifies a file created inside
its own round (or, for `crawler-identity.md`, preserves the round-open blob as a subsequence of the tip). The only
round whose own-endpoint run would have flagged history is r54. `[INFERENCE]` on K1 fixture construction: whether
`lines appended at EOF` passes depends on the fixture's trailing-newline shape per the split-on-`\n` trap noted
above — the real tool, once committed this wave, decides.

Tooling: none installed or updated (existing `git` + `python3` sufficed); pacman untouched per host guard.
VERDICT: Contract rule reports exit 0 for `fd6303ce..97cdc12` (R1) and `64c0ce12..97cdc12` — the only surviving
mid-file insertion is the tagged `[r59-correction 2026-10-27]` run at crawler-identity.md:35; per-commit, 18 historical
edits would flag (17 `changed` rewrites + 1 K8-style `untagged_insertion` at `8e408e00fb`).
