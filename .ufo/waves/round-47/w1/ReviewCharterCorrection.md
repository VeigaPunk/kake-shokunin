# ReviewCharterCorrection — ledger row `b9db4b1` vs LOG.md charter-ghp clause (r47 w1)

seat: `ReviewCharterCorrection` · lane: kake-shokunin · base: `cd42e3c310ba442e89dde638ba6401adaefaf3e8` · tip read: `766f4610b64f35a0f402b37eb1d8be2d4d634c0f`
mode: read-only over committed bytes (`git show`/`git diff`/`git rev-parse`, linter + counter runs that only read). Scratch: `/fast/scratch/hyaku/kake-r47/ReviewCharterCorrection/`. No sibling repo, `.ufo/state`, git index/refs or jj mutation; no tool installs.

**Verdict.** The charter attribution is correct (the row's `ds4cc-marketplace` reason was the error) and the append-only pointer is sound at byte level: the base ledger is preserved exactly as a 29-line prefix and the correction is a pure EOF append. One LOW evidence-labeling defect: the R4 mutation receipt's `b9db4b1` mutant never mutates `b9db4b1`. No falsifier for C2 (R4) from this seat.

## 1. Row, class, and what the gate consumes

| Check | Command | Observed |
|---|---|---|
| Row location | `grep -n b9db4b1 corpus/quality/citation-adjudications.md` | `26:` table row; `47:` correction bullet |
| Table reason (unchanged) | `nl -ba …:26` | `\| `b9db4b1` \| LOG.md \| external-repo commit \| ds4cc-marketplace repo commit in the same 2026-09-28 push series (external, absent). \|` |
| Corrected reason | `nl -ba …:47-48` | `- Row `b9db4b1` \| LOG.md — same misattribution; corrected reason: charter repo commit in the same 2026-09-28 push series (external, absent).` |
| Gate key live | `python3 -B scripts/citation_lint.py --root .` | exit 0, `violations: 0`, `adjudicated: 30`; entry `{file: LOG.md, line: 49, token: b9db4b1, class: external-repo commit}` |
| Row is load-bearing | same with `--adjudications <empty file>` | exit 1, 30 `dead_citation`, including `{LOG.md, line 49, b9db4b1}` |
| Row key is unique | `load_adjudications()` over HEAD ledger (`scripts/citation_lint.py:102-123`) | 20 rows → 20 distinct `(token, file)` keys |
| Block is gate-neutral | lint at `ee43e66` (r46 build, no block) vs HEAD | both 30 adjudicated, 0 violations, identical `(file, token, class)` set |
| Class holds | `git rev-parse -q --verify b9db4b1`; `git rev-parse --disambiguate=b9db4b1` | exit 1; 0 objects — token absent from lane store. Same result for `b74190e`, `d69dd22`, `0c767c2`, `dc8e1adf` |

Reading `scripts/citation_lint.py:48,118-123` confirms the gate keeps `token + file + class` and discards the reason cell; the block's own sentence (`citation-adjudications.md:33-36`) is accurate, and the empty-ledger / `ee43e66` pair proves the append changed gate behaviour in neither direction.

## 2. Repo attribution: charter, not ds4cc-marketplace

- Citing clause: `LOG.md:47-52`, inside the round-13 entry (`LOG.md:21`; next entry round 14 at `LOG.md:69`): `(4) charter-ghp: … the HUMAN pushed 5 commits 18:32:06–20:43:21Z (`b74190e` bake → `d69dd22` og-block → `0c767c2` window sync → `b9db4b1` CORRECTION → `a8f1e2b` fixup), Pages served each within ~30s`. `b9db4b1` is at `LOG.md:49`; the r46 spot-check's `LOG.md:48-49` locator is still valid because the r47 LOG diff is one hunk at `@@ -1790,3 +1790,104 @@` (`git diff --numstat cd42e3c…..HEAD -- LOG.md` → `101 0`).
- Repo identity corroborated independently in-lane: `corpus/knowledge/keeper-timer-inert.md:162-165` names `origin/main` of `~/Projects/origin-work/charter-ufo-fsd` and the same five-token chain; `:96-97` puts beat `61d0ce6` in the charter repo; `corpus/knowledge/fleet-registry.md:60` maps `charter-ghp` → `~/Projects/origin-work/charter-ufo-fsd` (annotated absent since the 2026-10-12 prune, `keeper-timer-inert.md:163`); `corpus/knowledge/publish-queue.md:174-182` files the same series under a "**charter** post-push subpath audit" with `origin-work` paths. No lane record ties any of the four tokens to `ds4cc-marketplace`.
- So the *reason* was the defect and `external-repo commit` was and stays right (non-resolving in the lane, attributed to an external repo) — exactly what `corpus/QUALITY.md:1072` requires.

## 3. Append-only pointer

| Check | Command | Observed |
|---|---|---|
| Base bytes preserved verbatim | `git show base:… \| sha256sum` vs `git show HEAD:… \| sed -n '1,29p' \| sha256sum` | both `432a36a2f9a6a20e6083ea223b63aa3c337e1fee4a9a938a08f8f61e57269394`; base is 29 lines, HEAD lines 1-29 are the whole base file |
| Pure addition | `git diff --numstat base..HEAD -- corpus/quality/citation-adjudications.md` | `25 0` (one hunk `@@ -27,3 +27,28 @@`, additions only) |
| Block placement | `nl -ba …:31-54` | `## Round-47 corrections (r46 closure routed defect R4, append-only)` at `:31`, five `- Row …` bullets `:38-54`, EOF; no table split |
| Old-line citation | bullets `:38,43,45,47,49` | each cites the old row by `token + population file`; unique per §1, so the pointer is unambiguous without a line number |
| Back-pointer | `LOG.md:1804-1808` | names the five tokens and quotes `"## Round-47 corrections"` (heading at ledger `:31`) |
| No moved inbound anchors | `grep -rn "citation-adjudications.md:[0-9]"` (repo) | no hits — the +25 lines move no referenced pointer |
| Predicate agrees | `c47_routed_count.py --root . --revision <rev>` | base `outstanding=4/4 C2_NOT_MET` exit 1; `714e707` and HEAD `outstanding=0/4 C2_MET` exit 0 |
| Receipt integrity | `sha256sum verification/c2-r4-mutation.txt`; ledger/counter/probe hashes at `714e707` | `1e7636ec…d507c3` (matches SCORECARD.md:3976 and round-47-verifier-spotcheck.md:39); `e75bc3a7…`, `9be35ef2…`, `0c8aa7a4…` all equal the committed receipts |

## 4. Finding (LOW) — the `b9db4b1` mutant is collateral, not row-specific

`c47_r4_mutation_check.py:62-73` normalizes the whole ledger (`" ".join(ledger.split())`) and applies `re.subn(phrase, mutant, count=1)`. `R4_EXPECTED` gives `0c767c2` and `b9db4b1` **the identical phrase** (`c47_routed_count.py:43-44`), and the ledger bullets are byte-identical (`citation-adjudications.md:45-48`). `count=1` therefore always hits `0c767c2` first:

```
b74190e: subn_count=1 killed=True entries_changed=['b74190e'] own_entry_changed=True
d69dd22: subn_count=1 killed=True entries_changed=['d69dd22'] own_entry_changed=True
0c767c2: subn_count=1 killed=True entries_changed=['0c767c2'] own_entry_changed=True
b9db4b1: subn_count=1 killed=True entries_changed=['0c767c2'] own_entry_changed=False
dc8e1adf: subn_count=1 killed=True entries_changed=['dc8e1adf'] own_entry_changed=True
```
(scratch `/fast/scratch/hyaku/kake-r47/ReviewCharterCorrection/mutant_scope.py`, reading `714e707`; the kill for the `b9db4b1` label comes from damaging `0c767c2`'s entry.)

Impact: SCORECARD.md:3976 ("5/5 wrong-reason mutants rejected") and round-47-verifier-spotcheck.md:39 count five runs, but only four distinct rows are exercised; the receipt does not demonstrate that restoring the *old* `b9db4b1` reason alone is rejected. The correction itself is still pinned: the counter keys entries by token (`c47_routed_count.py:105-111`), and an isolated mutation of only the `b9db4b1` segment is rejected — `b9-only mutation killed: True | base passes: True` (`isolate_b9b.py`, same scratch). So this is a receipt-coverage overstatement, not a false green in the committed state. Remedy for a future round: slice per `- Row \`<token>\`` entry before mutating, or assert `token in changed_entries`.

## 5. Observation outside the routed set (not a C2 falsifier)

Row `9c28d29` (`citation-adjudications.md:18`) still reads `webzites/charter scribe remote HEAD`; that repo spelling occurs nowhere else in the lane corpus, while the charter repo is named `~/Projects/origin-work/charter-ufo-fsd` (`fleet-registry.md:60`, `keeper-timer-inert.md:96-97`) and `publish-queue.md:27` places `9c28d29` in the "local charter checkout". `[INFERENCE]` the intended repo is the charter repo, so the ledger now uses two names for it. It was not one of the routed R4 five, its class is right, and no round-47 claim asserts all 20 reasons are correct — logged for the next closure, not as a defect of this repair.

## 6. Residual risk and verification gaps

- External presence **not** verified: the presence/message of `b9db4b1` in `origin-work/charter-ufo-fsd` cannot be checked without inspecting an absent sibling repo (out of lane bounds). Attribution rests on lane records (`LOG.md:48-50`, `keeper-timer-inert.md:162-165`, `fleet-registry.md:60`); `git rev-parse` absence only proves non-resolution in the lane.
- Wording precision: the block says the citing line "names the **charter** repo" (`citation-adjudications.md:39-40`); the line names `charter-ghp` + "the HUMAN pushed 5 commits". Repo identity is one documented hop away (`fleet-registry.md:60`). The corrected reason text itself is consistent with corpus vocabulary.
- Reason fidelity has no standing gate: `scripts/citation_lint.py:48,118-123` discards the reason cell, and the only enforcement is the wave-local `c47_routed_count.py:100-112` under `.ufo/waves/round-47/`. A later reason edit outside a repair round can regress silently (expected under "no capability entered", but it makes §4's receipt the only able-to-fail evidence).
- Not run by this seat: gate selftests (8/8, 23/23), `node scripts/freshness-sweep.mjs`, jj state, LOG R5/R6 semantics — other seats/claims own them.
