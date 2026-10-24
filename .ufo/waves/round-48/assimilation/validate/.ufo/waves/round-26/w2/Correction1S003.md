# Correction1S003 — falsify `[r26-recheck S003 STALE]` (Actions-vs-branch attribution), ghp-served-set.md EOF

- Seat: critic (leaf). Axis: freshness. Milestone: r26-recheck-falsify. Checked 2026-10-21.
- Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
- Target: candidate `corpus/knowledge/ghp-served-set.md:85` (first `[r26-recheck S003 STALE]` bullet).

## Verdict: AGREE

I tried four ways to show the correction is wrong. None held up.

### 1. Is the original wrong at its own stated scope? Yes.
Original, base `ghp-served-set.md:14,17-18`: “**r20-correction at base `cb807bc`.** … `corpus/knowledge/publish-channels.md:5-14` distinguishes Actions from branch publishing.”

The stated scope is the file at `cb807bc`. `git merge-base --is-ancestor cb807bc 97404de…` succeeds, and `git rev-parse cb807bc` resolves to `cb807bc8d8bc94be1268e4741191bb3d5e518565`. In `git show cb807bc:corpus/knowledge/publish-channels.md`:
- Lines 5-9 describe the ds4cc `pages.yml`: “on push to main → validate … `upload-pages-artifact` repo root → `deploy-pages`.”
- Lines 10-11 describe the plazir `pages.yml`: “same shape, uploads `.` whole”.
- Lines 12-14 describe `deploy-github-pages.sh`: “a one-time *setup* script … pushes once … Not the deploy path.”
- `git show cb807bc:corpus/knowledge/publish-channels.md | grep -n -i branch` returns no lines. The word “branch” does not appear anywhere in that file at `cb807bc`.

**Strongest counterexample tried.** Lines 12-14 contrast a push script with the Actions deploy path (“Not the deploy path”). Could that count as distinguishing Actions from branch publishing? No. It contrasts a setup push with the Actions deploy. It does not name branch-source publishing, which is the Pages mode S003 describes. The heading at line 3 (“push to `main` is the publish verb”) describes the trigger for an Actions workflow, so it fails the same way.

At base `97404de`, the only “branch” in publish-channels.md is the r20 tail at line 59, added after `cb807bc`. It sits outside the 5-14 pointer. So the original pointer is false at base too, and the correction's phrase “false already at base cb807bc” is accurate.

### 2. Is the correction accurate and verbatim where it quotes? Yes.
- **Quote of the original.** “`corpus/knowledge/publish-channels.md:5-14` distinguishes Actions from branch publishing” matches base lines 17-18 byte for byte, apart from the line break. The location “line 17-18” is correct.
- **Description of the cited lines.** “two Actions workflows and a setup script” matches `cb807bc` lines 5-14, as shown above.
- **Quote of S003.** “You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.”
  - `grep -nF` finds it in `.ufo/waves/round-26/fetched/text/S003-1.txt` (line 1, a single-line file).
  - It is also in the raw HTML: `zcat fetched/S003-1.raw.gz | grep -o 'You can publish your site when changes are pushed to a specific branch[^<]*'` prints the exact sentence.
  - The anchor “About publishing sources” is present, and receipt `rechecks/S003.json` records the same quote and anchor.
- **Integrity of the retained bytes.** `zcat S003-1.raw.gz | sha256sum` gives `aa758b4a543f792f3afa1ea37edf4042581719510a479a3f45ce3ace58fdf1ac`. That equals `manifest.json` and `population.json` (154,136 bytes, status 200, fetchedAt 2026-10-21T15:09:34Z).
- **Live comparison.** I ran one plain public GET of the SOURCES.md:11 URL and did not save it. After stripping tags and normalizing whitespace, the quote is present (`True`). The sibling quote “the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch.” is also present (`True`). The retained bytes are not stale against the live page.

### 3. Were all original bytes preserved? Yes.
I compared the two blobs from `git show <rev>:corpus/knowledge/ghp-served-set.md` in memory: base is 4843 bytes, candidate is 6865 bytes, and `cand.startswith(base)` is `True`. The appended bytes begin with `\n## Round-26 source recheck\n\n- Round-26 `. `git diff --stat` shows `ghp-served-set.md | 10 +` with no deletions. That fits the append-only rule; the round-20 section is unchanged.

### 4. Does the receipt contradict the correction? No.
`rechecks/S003.json` gives verdict HOLD with `"correction": null`. That is a row-level verdict: the source still teaches branch-or-Actions. `statements.json` separately records `{"row":"S003","file":"corpus/knowledge/ghp-served-set.md","statements":7,"stale":2}`. The STALE verdict is statement-level and concerns a local pointer, not the source, so the two records describe different things.

## Observation (no verdict impact)
The applied text is a condensed version of the draft C1 in `w1/PairS003GhpServedSet.md`. It drops the draft's scope caveat, which S003 itself states (verified in the text view): “Your GitHub Pages site will always be deployed with a GitHub Actions workflow run”. Without it, a reader could take “branch publishing” to mean no Actions run happens. The correction remains true as written, because the attribution and quote are both correct, so this is a fidelity tradeoff rather than a defect. Smallest optional refinement: a later append-only line that restores the caveat with that quote. No change to the existing correction is required.

## Commands run
`git show` (base, candidate, `cb807bc`), `git merge-base --is-ancestor`, `git rev-parse`, `git diff --stat`, `git diff cb807bc 97404de -- publish-channels.md`, `sha256sum`/`zcat`, `grep -F` on the retained text and raw bytes, an in-memory Python prefix check, and one public `curl` GET of the SOURCES.md:11 URL (not saved).

## Tooling
None installed, upgraded or removed.

```json
{"target":"[r26-recheck S003 STALE] Actions-vs-branch attribution, corpus/knowledge/ghp-served-set.md:85 @ e28312b","verdict":"AGREE","severity":"none"}
```
