# Correction2S003 — falsify `[r26-recheck S003 STALE]` (lines 28-29 quote) in `corpus/knowledge/ghp-served-set.md`

- Seat: KakeR26-2.Correction2S003 (critic, leaf). Axis: freshness. Milestone: r26-recheck-falsify. Checked 2026-10-21.
- Candidate `e28312b14b076584fedd696fae2a684e460bd11e` against base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
- Verdict: **AGREE**. The only finding is a low-severity wording note that does not block the correction.

## Q1 — Is the original actually wrong at its own stated scope?

Yes. Base file, lines 28-29:

> `- S003, About publishing sources: “the source folder can either be the`
> `  root of the repository (`/`) or a `/docs` folder.” S004 steps 4-5 upload`

The bullet uses typographic quotation marks, so it presents the text as a verbatim quote. The ledger rule is at `statements.json:4`: "STALE = the statement is wrong or unsupported at its own stated scope against the 2026-10-21 bytes (content, attribution, quote fidelity, version semantics)." Quote fidelity is therefore in scope.

- Checked the retained bytes. `zcat fetched/S003-1.raw.gz | sha256sum` gives `aa758b4a543f792f3afa1ea37edf4042581719510a479a3f45ce3ace58fdf1ac`, which equals the S003 value in `manifest.json` and `population.json`. The raw HTML reads: `the source folder can either be the root of the repository (<code>/</code>) on the source branch or a <code>/docs</code> folder on the source branch.`
- Searched the text view: `rg -n -o '.{0,200}source folder can either.{0,200}' fetched/text/S003-1.txt` returns "…and the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch. Whenever changes are pushed…". The base wording is not a substring with or without backticks, because "on the source branch" is missing twice and no ellipsis marks the omission.
- Checked the anchor. In the raw HTML, the sentence is at byte offset 52277. That falls between `id="about-publishing-sources"` (51642) and `id="publishing-from-a-branch"` (53834). The original's section label "About publishing sources" is correct, so the defect is limited to quote fidelity.

## Q2 — Is the correction accurate, and verbatim where it quotes?

Yes. The candidate's line 87 quotes: “the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch.”

- It matches the text view exactly. In the raw HTML, the `(/)` and `/docs` positions are `<code>` markup only, so dropping the backticks is normalization, not alteration.
- At 24 whitespace words, it is within the 25-word limit in `contract-amendment.json:12`. `rg -l -F 'source folder can either be the root' fetched/text/` matches only `S003-1.txt`, so the quote is specific to S003.
- The line pointer "lines 28-29" matches the base line numbers.
- The claims "root-or-/docs substance is unchanged" and "dropped 'on the source branch' twice" both match a text diff of the base wording against the bytes.
- The correction matches the seat proposal `w1/PairS003GhpServedSet.md` C2 and statement K6. The ledger records S003 × ghp-served-set as `seatStale: 2, stale: 2` (`statements.json:35-41`), and the file carries two `[r26-recheck S003 STALE]` tags (lines 85 and 87).

## Q3 — Were all original bytes preserved?

Yes. Command output:

```
git show e28312b…:corpus/knowledge/ghp-served-set.md | cmp - corpus/knowledge/ghp-served-set.md  → SAME_AS_CANDIDATE
base_bytes=4843
head -c 4843 corpus/knowledge/ghp-served-set.md | cmp - <(git show 97404de…:corpus/knowledge/ghp-served-set.md)  → PREFIX_OK
wc -c → 6865
```

The base's 4843 bytes are an exact prefix of the candidate, and the addition is the EOF section `## Round-26 source recheck` (lines 81-89). `git log 97404de..e28312b -- <file>` shows one commit, `e28312b`.

## Counterexamples tried (none overturn the correction)

1. **Docs wording may have drifted since 2026-10-19.** No S003 bytes from before 2026-10-21 are retained. `corpus/lessons/round-20.md:205` records a different S003 sentence, and `.ufo/waves/round-21/frozen/before/…:28-29` holds only the corpus wording. If the docs did drift, the original would be STALE instead of mis-transcribed. Under the ledger rule, STALE is judged against the 2026-10-21 bytes either way, so the verdict stands.
   - Wording note (low severity): "the earlier wording dropped" could be read as a past transcription error. The seat's `[INFERENCE]` caveat (K6), that drift cannot be excluded, did not carry over into the admitted text. [INFERENCE] I believe the GitHub Docs wording "on the source branch" is long-standing, but no retained bytes show it.
2. **"Substance unchanged" may understate the omission.** The dropped qualifier limits the folder choice to branch publishing, while the entry is about the Actions-workflow artifact. The base bullet makes no claim that Actions uploads are limited to `/` or `/docs`, and the companion correction (line 85) covers the branch-versus-Actions distinction. Not a defect.
3. **Wrong anchor or wrong line pointer.** Both checked above, and both hold.

## Smallest optional refinement (non-blocking)

This would need a new append-only block, since the admitted bytes must stay unchanged. Replace "the earlier wording dropped" with "the 2026-10-19 wording omits, relative to these bytes," to restate the seat's drift caveat. The verdict, quote and tag would not change.

## Tooling

None installed, upgraded or removed. Only read-only commands were run: `git show`, `git log`, `cmp`, `head`, `wc`, `zcat`, `rg`, `sha256sum`, `sed`, `python3 -c`. No network GET. The only file written is this report.

```json
{"target":"[r26-recheck S003 STALE] ghp-served-set.md lines 28-29 S003 source-folder quote","verdict":"AGREE","severity":"low"}
```
