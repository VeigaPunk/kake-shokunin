# ReviewCharterBake — ledger row `b74190e` vs the LOG charter-ghp citing line

Axis: freshness. Scope: the R4 correction for `b74190e` in
`corpus/quality/citation-adjudications.md` against the exact citing clause in
`LOG.md`. Read-only; HEAD `766f4610b64f35a0f402b37eb1d8be2d4d634c0f`; base
`cd42e3c310ba442e89dde638ba6401adaefaf3e8`. No lane files edited except this report.

## Verdict

**PASS — no falsifier.** The corrected reason names the **charter** repo and
drops the ds4cc-marketplace attribution; the class stays `external-repo commit`;
the repair is purely additive (25 insertions, 0 deletions vs base). Three
precision residuals below (the third is a repo-label note), none an artifact
defect.

## Evidence

### 1. Row under review is byte-identical at base and tip
- `corpus/quality/citation-adjudications.md:17`:
  `| b74190e | LOG.md | external-repo commit | ds4cc-marketplace repo commit from the 2026-09-28 push series (external, absent); historical live-audit record. |`
- `git show cd42e3c…:corpus/quality/citation-adjudications.md | sed -n '17p' | sha256sum`
  -> `0fa912e25bca1a7dca2d155ef72f9267d0504a80dbee4867ef1f9fbc424fd4be`
- `git show HEAD:corpus/quality/citation-adjudications.md | sed -n '17p' | sha256sum`
  -> the same `0fa912e2…4fd4be`; class cell (`cut -d'|' -f4`) = ` external-repo commit `.
- `git diff --numstat cd42e3c…HEAD -- corpus/quality/citation-adjudications.md`
  -> `25  0` (additions/deletions). The table prefix was not touched.

### 2. Correction block names charter, not ds4cc-marketplace
- `corpus/quality/citation-adjudications.md:38-42` (verbatim):

```text
- Row `b74190e` | LOG.md — reason says "ds4cc-marketplace repo commit from the
  2026-09-28 push series"; the citing line (LOG.md, round-13 entry, charter-ghp
  clause) names the **charter** repo's 2026-09-28 HUMAN push series. Corrected
  reason: charter repo commit from the 2026-09-28 push series (external, absent);
  historical live-audit record.
```
- The corrected phrase itself contains no ds4cc-marketplace token; that string
  survives only as the explicitly quoted old reason and in the untouched table
  cell (append-only requirement).

### 3. The citing line is exactly the charter-ghp clause
- `LOG.md:21` is the round-13 entry header; `LOG.md:69` is the next entry
  (round 14). The clause is `LOG.md:47-52`:
  - `47`: `surfaces. (4) charter-ghp: pin-lag persists BUT live is deploy-current —`
  - `48`: ``the HUMAN pushed 5 commits 18:32:06–20:43:21Z (`b74190e` bake →``
  - `49`: `` `d69dd22` og-block → `0c767c2` window sync → `b9db4b1` CORRECTION → ``
  - `50`: `` `a8f1e2b` fixup), Pages served each within ~30s (live sha `0decd827…` ``
- So the correction's "round-13 entry, charter-ghp clause" locator is accurate,
  and "HUMAN push series" matches line 48 verbatim.
- Independent in-lane corroboration that `b74190e` is a charter-repo commit:
  `LOG.md:8` (round-6 entry) `charter 2 behind: … = b74190e static-index bake not
  pulled`; `LOG.md:108` `Charter post-push subpath audit (b74190e…a8f1e2b series)`;
  `corpus/knowledge/publish-queue.md:27` (PQ-3, charter row) `was behind 5
  b74190e…a8f1e2b`. No lane record asserts the ds4cc-marketplace attribution
  as fact; the only occurrences of that attribution are the pre-correction table
  row itself and the r47 texts that quote it to supersede it (`ledger:38-39`,
  `LOG.md:1804`; the C2 predicate at `SCORECARD.md:3943` describes the defect).

### 4. Class is preserved and still correct
- Table class remains `external-repo commit`.
- `git rev-parse -q --verify 'b74190e^{commit}'` -> exit 1 (no object in the lane
  repo), consistent with an external repo; sibling charter row `9c28d29`
  (`webzites/charter … external repo, absent`) uses the same class.
- The committed gate still parses exactly this adjudication:
  `python3 -B scripts/citation_lint.py --root . --revision HEAD` -> exit 0,
  `verdict clean`, `violations 0`, and the `b74190e` record is
  `{"class":"external-repo commit","file":"LOG.md","line":48,"token":"b74190e"}`.
  The appended block creates no extra ledger rows: the real loader
  (`load_adjudications`, 20 rows) returns 20, split 12 LOG.md / 8 SCORECARD.md.

### 5. Fix predicate and receipts reproduce
- `python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision cd42e3c…`
  -> `outstanding=4/4 C2_NOT_MET`, exit 1 (able-to-fail control).
- Same command at `714e707…` -> `outstanding=0/4 C2_MET`, exit 0.
- `python3 -B .ufo/waves/round-47/c47_r4_mutation_check.py --root . --revision HEAD`
  -> `R4_REASON_FIDELITY base=pass mutants=5/5_rejected PASS`, exit 0 (the
  `b74190e` mutant rewrites the expected phrase to `ds4cc-marketplace repo
  commit` and is rejected).
- Receipt identity: `c2-r4-mutation.txt` sha256
  `1e7636ecb023b2d2fa61d5bb6904166ebe84337514beed175c8010675cd507c3` equals the
  lesson's cited hash; ledger sha256 at `714e707` and at HEAD/worktree is
  `e75bc3a746539d86651f4b31f578480702fc325cbe1e1555cd76aa38d5058669`, matching
  the receipt's `ledger_sha256_at_revision`. No commit after `714e707` touches
  the ledger (`git log 714e707..HEAD -- <ledger>` empty).
- Append-only authority: `corpus/QUALITY.md:31-37` (post-review ruling: pure
  new-line additions / EOF correction blocks citing the old line, never in-place
  cell edits) and `corpus/QUALITY.md:1072` (round-47 "Citation reason fidelity"
  criterion, which names this exact repair). The block conforms.

## Residual risk (not falsifiers)

1. **Fix is block-scoped, not cell-scoped.** Table line 17 still reads
   `ds4cc-marketplace …` by design; the corrected reason exists only at
   `citation-adjudications.md:41-42`. Any check that greps the table for
   `charter` (or the file for the absence of `ds4cc-marketplace`) will read the
   wrong surface. The committed predicate anchors on the full corrected phrase
   and is not vacuous, but it would not catch a silent in-place edit of the
   table and does not assert the class at all; class preservation rests on the
   `25 0` diff above, not on the counter.
2. **Citing-line locator omits line numbers.** The block locates the line as
   "LOG.md, round-13 entry, charter-ghp clause"; the canonical numbers are
   `LOG.md:47-52` with the token at `48` (siblings at `49`). The r46 routed
   defect gave `48-49`. A cross-reader using `46-51` (as in
   `.ufo/waves/round-47/w1/CriticReasonFidelity.md`) is shifted one line low;
   the attribution is unaffected.
3. **Repo label is family-level.** "charter repo" matches the routed-defect
   wording and the ledger's neighboring `webzites/charter` row, but the surface
   the lane actually tracked is `charter-ufo-fsd`
   (`corpus/knowledge/publish-queue.md:192`, whose r18 re-census annotation
   records that checkout absent since the 2026-10-12 prune). The block names no
   canonical remote; the class is external either way. "(external, absent)" is
   inherited unchanged from the old reason and is corroborated only by lane
   records, not re-tested on disk.

## Verification gaps

- No LSP server/device was available to this seat (`lsp` is not in the tool
  inventory and no `xd://lsp` device exists), so caller/definition checks used
  the committed gate's own loader plus `git show`/`diff`/`rev-parse`; no
  semantic-index claim is made.
- Host filesystem and sibling repos were not inspected per lane bounds, so
  charter-repo absence is taken from committed lane records
  (`publish-queue.md:192,250`), not re-verified.
- Tool installs/updates: none.
