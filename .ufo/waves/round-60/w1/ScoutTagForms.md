# ScoutTagForms

C2 tag grounding at base `97cdc122379711c2b02a8970752c8782da3ac81d`. Enumeration via
`git -C <lane> grep` on corpus/ + SKILL.md at the base blob (never the worktree). Question answered:
is `\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]` the lane's in-file-correction convention, and
which other spellings exist and are they in-file insertions?

## SPELLINGS:

Bracket `[rNN-…]` forms (all observed at base, path scope `corpus` + `SKILL.md`):

| spelling | total | in-file corrections | file:line (in-file instances) |
|---|---|---|---|
| `[rNN-correction YYYY-MM-DD]` bare tag ending `]` | 9 | 3 | `corpus/knowledge/crawler-identity.md:35` (r59), `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md:54` (r54), `corpus/QUALITY.md:121` (r23); other 6 are rule/report mentions — `SKILL.md:1309`, `corpus/QUALITY.md:1330`, `corpus/lessons/round-59.md:173,233`, `corpus/lessons/round-59-verifier-spotcheck.md:73`, `corpus/lessons/round-54-verifier-spotcheck.md:29` |
| `[rNN-correction YYYY-MM-DD: <prose>]` inline bracket | 27 | 27 | all r20: `SKILL.md:16,230`; `corpus/README.md:28,178`; `corpus/knowledge/ghp-subpath-spotcheck.md:95`, `publish-channels.md:58-61` (×4), `sitemap-orphan-audit.md:120-127` (×8), `speedrun-pipeline.md:70`; `corpus/lessons/round-7.md:57-65` (×9) |
| `[rNN-correction]` undated | 6 | 6 | `corpus/knowledge/static-canonical-preflight.md:140,143,186,200,203`; `SKILL.md:485` (all r23) |
| `[rNN-correction <defect-id>]` (R3/R5/R5 identity/R6/R6 withdrawal/R6 supersession) | 0 in scope | — | 6 mentions in `corpus/lessons/round-47-verifier-spotcheck.md:38,40,41,80`; the actual corrections sit in fleet-root `LOG.md`/`SCORECARD.md` outside grep scope |
| `[rNN citation-local YYYY-MM-DD: <prose>]` (space, not hyphen) | 26 | 26 | all r20: `SKILL.md:24,51,59,111,309,311,312`; `corpus/README.md:204`; `corpus/knowledge/drift-detection.md:95`, `fire-journal-codes.md:8`, `fleet-registry.md:85`, `free-read-verbs.md:325,483`, `freshness-sweep.md:98`, `probe-delta-alerting.md:82,84`, `publish-channels.md:35`, `publish-queue.md:267`; `corpus/lessons/round-4.md:5`, `round-4-aggregator-audit.md:32`, `round-6-aggregator-audit.md:145`, `round-17.md:14,16,23,25`, `round-18.md:33` |
| `[rNN-recheck SNNN STALE]` | 14 in-file | 14 | r26/r27: `corpus/knowledge/ghp-etag-anatomy.md:62,64`, `ghp-served-set.md:85,87,93,99`, `sitemap-orphan-audit.md:163`, `static-canonical-preflight.md:186,188,190,192,198,199,235`; plus mentions `SKILL.md:582`, `corpus/README.md:292`, `corpus/lessons/round-26.md:54`, `round-26-verifier-spotcheck.md:40,69` |
| `[rNN-recovery registry clarification]` | 1 | 1 | `SKILL.md:499` (r23) |
| `[rNN resume YYYY-MM-DD: <prose>]` (space) | 1 | 1 | `SKILL.md:212` (r20, mid-table-cell) |

Non-bracket forms:

| spelling | total | file:line / notes |
|---|---|---|
| `<!-- r18 re-census YYYY-MM-DD: <prose> -->` (HTML comment) | 73 | 10 in `SKILL.md` (16,18,19,30,157,283,334,343,365,370), 63 across `corpus/` incl. `corpus/knowledge/keeper-timer-inert.md` ×8, `fleet-registry.md` ×6, `origin-repos.md` ×5, `speedrun-pipeline.md` ×4, `publish-queue.md` ×3; per-file list truncated (top counts only). Excluded class by contract K9. |
| `*(rNN correction: <prose>)*` parenthesized | 2 in-file + 1 mention | `corpus/knowledge/ops-automation.md:48` (r10), `corpus/README.md:186` (r20); mention `corpus/lessons/round-6-aggregator-audit.md:30` |
| `rNN correction` bare prose | ~8 | `corpus/knowledge/free-read-verbs.md:386` (r16), `keeper-timer-inert.md:70` (r16), `fire-journal-codes.md:2`, `speedrun-pipeline.md:2`, `corpus/README.md:32` (r43), `corpus/lessons/round-26.md:60` (r23); partial enumeration |
| `erratum:` / `errata` (no bracket) | 8 in `corpus/knowledge` | `ghp-custom-domain.md:52` ("S007 quote-format erratum"), `ghp-served-set.md:73,125`, `ops-automation.md:64,104`, `publish-queue.md:230`, `robots-txt-rules.md:3`; plus section-heading `## Independent audit erratum` `corpus/lessons/round-19-recensus.md:42`, `## Shape-only evidence erratum` `corpus/lessons/round-20.md:124` |
| `## Round-NN correction[s] — …` / `## Quote classes (round-NN correction)` heading-only (no bracket tag) | ~19 headings | `corpus/QUALITY.md` (r31:517, r34:677, r35:845, r47:1075), `corpus/quality/citation-adjudications.md:31,57`, `corpus/lessons/round-51.md:18,138`, `round-53.md:9,130`, `round-7.md:55`, `yahoo-japan-rel-nofollow-semantics.md:52` ("## Round-54 correction — S374 crawl qualifier (2026-10-25)", bracket tag on the body line below), etc. |

All correction classes above are in-file insertions (appended lines/blocks or, for r20 inline forms,
mid-line insertions inside table cells and prose). Every rule cited below forbids rewrites; none
prescribes one canonical tag spelling.

## RULES:

- `/home/vgpnk/Projects/shokunin/CORPUS.md:53` — "**Corrections are new entries, never rewrites.** Lanes own `lessons/round-<N>.md`; the aggregator writes only `lessons/round-<N>-aggregator-*.md` and does not edit lane-authored corpus files in place (same append-only discipline `PROTOCOL.md` gives `LOG.md`)."
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md:123-125` — "Corrections land as new commits, never by amending a cited one (amending or rewriting orphans the record); append-only files (`LOG.md`) take an appended correction entry pointing at the superseded text, never an in-place rewrite."
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md:135-137` — "a correction to it lands in the correcting round's own report, or as an erratum appended after the filed bytes in a new commit and naming the text it supersedes — never a rewrite of the filed bytes, labelled or silent."
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md:366` — "**A falsified claim in an append-only file gets a named correction entry in the lane's next round** — appended, never rewritten; it stays on the routed-defect queue until it lands."
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md:363` — "**Corrections sweep every mention.** Before a round's commit, grep every file the lane touches (`corpus/README.md`, `SKILL.md`, `knowledge/`) for the superseded claim."
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md:463` — "`LOG.md` is append-only: entries are never rewritten or deleted; corrections land as new entries." ; `:501-502` — "Corpus corrections are new entries, never in-place rewrites: no lane edits another lane's corpus files."
- `corpus/QUALITY.md:31-40` (base blob) — "## Post-review append-only ruling — round 20 … The orchestrator rejects the earlier 'Append-only tails' criterion: a suffix changes the original line's bytes and hash even if its old text survives. Superseding rule: preserve every prior lesson/knowledge line byte-identically; use pure new-line additions or end-of-file correction blocks citing the old line. Never split a table to satisfy the citation-local gate."
- `corpus/QUALITY.md:1116` — "corrections to admitted prose are appended rather than rewritten."
- `corpus/QUALITY.md:1325-1331` (round-59 criterion) — "… `9/9 met=True` with `C9_stale_claim_corrected` PASS, and C9 fails on three independent sub-reasons (no `[r59-correction 2026-10-27]` line within 8 base lines, no S425 citation, no retained body)." — the only rule text naming the bare-bracket dated tag form.
- `SKILL.md:581-583` — "append `[r26-recheck S0NN STALE]` corrections to the citing entry only when a statement is wrong at its own stated scope"; `corpus/lessons/round-26.md:52` — "Each is an EOF block tagged `[r26-recheck S0NN STALE]`; no original line changed."
- `SKILL.md:1233` (gate row, round-55 `readme-index-counter` labelled `historical` from round 59) — "its `head_changed` term requires every round-55-base knowledge file to survive as a byte prefix, and the round-59 append-only correction inserts lines inside `corpus/knowledge/crawler-identity.md`" — grounds the R59-D1 gate collision C2 resolves.
- `AGENTS.md` (base blob) — no correction/tag rule beyond ":4  - Every change appends a LOG.md entry with the evidence that motivated it."

## REGEX FIT:

`\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]` matches exactly one observed class: the **bare
dated bracket tag** (`[rNN-correction DATE]` ending in `]`), 9 occurrences at base of which 3 are
in-file corrections (`corpus/knowledge/crawler-identity.md:35` r59, `yahoo-japan-rel-nofollow-semantics.md:54` r54, `corpus/QUALITY.md:121` r23 register).

Fit verdict: **yes for the current convention, no for the historical population.**

- For: the two most recent in-file corrections in `corpus/knowledge` (r54, r59 — both bold-`**` opening lines of a standalone appended block under a `##` heading) carry exactly this form, and it is the only form named by the newest counter predicate (QUALITY.md:1330, C9 `[r59-correction 2026-10-27]`). It is the de-facto tag for new appended correction blocks.
- Against-as-sole-form: the historically dominant in-file correction spelling is `[rNN-correction DATE: <prose>]` (27, all r20) which does **not** match — the char after DATE is `:` not `]`; `[rNN-correction]` undated (6), `[rNN citation-local DATE:…]` (26), `[rNN-recheck SNNN STALE]` (14), `[rNN-recovery …]` (1), `[rNN resume DATE:…]` (1), `<!-- r18 re-census … -->` (73), `*(rNN correction:…)*` (2), bare `rNN correction` (~8), `erratum:` (~8 in knowledge) and heading-only correction blocks (~19) all fail the regex too.
- Consequence for `scripts/append_guard.py`: every existing in-file correction except the r54/r59/r23 bare tags would be reported `untagged_insertion` if it were re-inserted above its own base. That is safe for the frozen rule because the guard only judges **new** insertions between `--base` and `--revision`; the old tags sit in base lines, never in inserted runs. The regex thereby encodes "new corrections must use the bare dated bracket tag" — stricter than the recorded conventions, consistent with the post-round-20 byte-preservation ruling (QUALITY.md:31-40: pure new-line additions / EOF blocks, which the r20 mid-line `: <prose>` inserts violate).
- Visibility clauses match corpus reality: at base, no `[rNN-correction` tag occurs inside `<!-- … -->` (the comment population uses `r18 re-census` instead) or inside a backtick span (SKILL.md:1309 and QUALITY.md:1330 carry mentions where the backticks sit outside the `[`). So the "outside HTML comment / outside code span" exclusions of C2 have no counterexample among existing `-correction` tags, and K9/K10 cover the plausible evasions.
- Gap note (observation, not a defect): `[rNN-recheck SNNN STALE]` EOF blocks are lane-blessed corrections (round-26 rule) that the tag regex does not cover; if a future mid-file run ever opens with one, the guard would flag it. `erratum:`/heading-only/`rNN correction` prose forms likewise stay invisible to it.

Installs: none (no tools installed or upgraded; pacman untouched).

VERDICT: The contract regex matches only the newest bare-dated `[rNN-correction YYYY-MM-DD]` convention (3 in-file instances, r23/r54/r59); it misses the older, more numerous `[rNN-correction DATE: prose]`, `[rNN citation-local]`, `[rNN-recheck STALE]`, `r18 re-census`, `*(rNN correction:…)*`, `erratum:` and heading-only forms — all in-file insertions — which is acceptable only because the guard judges new inserts, not history.
