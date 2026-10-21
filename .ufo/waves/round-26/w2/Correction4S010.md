# Correction4S010 — falsify `[r26-recheck S010 STALE]` §8.8.1 condition (ghp-etag-anatomy.md)

Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`. Target bullet: `corpus/knowledge/ghp-etag-anatomy.md:64` (candidate; worktree byte-equal to candidate per `cmp`).

**Verdict: AGREE (low).** The original paraphrase is wrong at its own scope. The correction's central claim is accurate, and its quoted fragment is verbatim. Every base byte is preserved. One low-severity imprecision remains in the correction, described in item 4.

## Axes
Freshness / correctness at stated scope (ledger rule); quote fidelity; append-only byte preservation; provenance and tag accounting.

## Evidence

1. **The original is wrong at its own scope.** Base L25–28 reads: `S010 §8.8.1 notes: “a representation's modification time, if defined with only one-second resolution, might be a weak validator” when changed twice within that second.`
   - The retained bytes at `.ufo/waves/round-26/fetched/text/S010-1.txt` (manifest S010 fetchIndex 1, sha256 `d4317606…e1e5`, fetchedAt 2026-10-21T15:10:38Z) read: `…might be a weak validator if it is possible for the representation to be modified twice during a single second and retrieved between those modifications`.
   - `grep -o` for that full clause returns 1 match.
   - The gloss drops the retrieval conjunct, so it presents a necessary-but-insufficient condition as the condition. `statements.json` `rule` says: "STALE = the statement is wrong or unsupported at its own stated scope against the 2026-10-21 bytes (content, attribution, quote fidelity…)". The gloss meets that rule.
   - Strongest counterexample tried: "RFC 9110 is immutable, so nothing is *stale*." This fails. The ledger rule does not require source drift, and `w1/PairS010GhpEtagAnatomy.md` row 5 records this as a pre-existing paraphrase defect, not drift.
   - Second counterexample tried: "row receipt `rechecks/S010.json` is HOLD with `correction: null`, which conflicts with the STALE tag." This also fails. The receipt judges the row's *teaches* claim. Statement-level STALEs are the ledger's job, and `statements.json` carries `{"row":"S010","file":"corpus/knowledge/ghp-etag-anatomy.md","statements":9,"stale":2}`. The file carries exactly 2 `[r26-recheck S010 STALE]` tags (`grep -c` → 2), which matches.

2. **The correction quotes verbatim.**
   - `“when changed twice within that second”` equals base L27–28 (`when changed twice` / `  within that second.`) joined across the line wrap.
   - `“and retrieved between those modifications”` occurs once in `S010-1.txt` (`grep -o … | wc -l` → 1).
   - "Lines 25-28" is the correct span: the §8.8.1 sentence starts on L25 and the gloss ends on L28.

3. **The base bytes are preserved.**
   - Base blob is 3304 bytes. `cmp -n 3304 <(git show $B:$P) <(git show $C:$P)` → `PREFIX_OK`.
   - The candidate continues at byte 3305 with `\n\n## Round-26 source recheck\n\n- …`.
   - `git diff` shows `-- **Validator is not identity:** …` plus `\ No newline at end of file`. That is only the added EOF newline. It is not a content change, and `cmp` confirms the prefix.
   - No original line was rewritten. L25–28 are untouched.

4. **Residual imprecision (low, fixable).**
   - The correction says the bytes "condition it on modification twice during a single second ‘and retrieved between those modifications’". The source conditions on *possibility*: "if it is possible for the representation to be modified twice during a single second and retrieved between those modifications".
   - So the correction drops the "if it is possible for" modality. It restates a design property as an occurrence, which is the same kind of qualifier loss the original had.
   - The w1 proposal C2 quoted the full clause verbatim. The admitted bullet compressed it.
   - The central correction, that the retrieval conjunct is missing and two changes alone are not the condition, stays true. That is why this is low severity and does not change the verdict.

5. **Scope note (no defect).** The bullet ends with an S009 sentence: "Current nginx lines (1.30/1.31) move the same format expression; the release-1.28.0 pin and its line anchors remain correct as pinned". It is correctly attributed to `w1/PairS009GhpEtagAnatomy.md`. R4 and R7 there record the identical expression at 1.30.6:1722 and 1.31.8:1773, and the pinned 1.28.0 anchors at 1682/1708. Its placement under an S010 tag is cosmetic and does not change any tag count.

## Smallest safe correction (optional, append-only)
Append a further EOF bullet. It must not carry an extra `[r26-recheck S010 STALE]` tag, because that would break the 2-of-2 ledger match:
`- Note on the S010 §8.8.1 correction above: the RFC condition is modal — "if it is possible for the representation to be modified twice during a single second and retrieved between those modifications".`

## Commands run
`git show $B:…ghp-etag-anatomy.md | cat -n`; `grep -o` on `S010-1.txt` (context, full clause → 1, fragment → 1); `cmp -n 3304` prefix → PREFIX_OK; `cmp` candidate vs worktree → equal; `tail -c +3305 | od -c`; `git diff --stat` / `grep '^-'`; `grep -c 'r26-recheck S010 STALE'` → 2; manifest, statements.json and w1 Pair reads.

## Tooling
No tools installed or updated. Only this report was written.

```json
{"target":"[r26-recheck S010 STALE] §8.8.1 condition paraphrase, corpus/knowledge/ghp-etag-anatomy.md L25-28","verdict":"AGREE","severity":"low"}
```
