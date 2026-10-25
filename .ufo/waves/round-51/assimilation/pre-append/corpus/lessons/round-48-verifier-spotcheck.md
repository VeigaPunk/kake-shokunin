# Round 48 verifier spot-check

author: hyaku closure (non-author integrator, Kimi fresh closure agent)

Reviewer is a fresh Kimi closure agent, not an `@m_swe` session and not a seat this lane dispatched. This file verifies; it does not improve the round. Round tip checked: `fd917a42567ff3642c0f7930659681141200b419`. Base: `766f4610b64f35a0f402b37eb1d8be2d4d634c0f`. Report: fleet `124cf646ab96589ff30068b02f28bfc60f834e38`.

## Conformance

- Report commit `124cf646ab96589ff30068b02f28bfc60f834e38` is `kake-shokunin <kake@shokunin.local>`, subject `round-48: kake report`, dated 2026-10-24 21:12:21 -0300, and is an ancestor of fleet `HEAD` (`96791bf84940349eb4ae1b72a171263c7a790fd6`). It is a real report: Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, and a `SHONEN` heading with four box lines. No `[x]`.
- Lane commits `af7b217c9b0837428e50c944adfab9f5c692a50f` and `fd917a42567ff3642c0f7930659681141200b419` exist, are `kake-shokunin <kake@shokunin.local>`, and `git merge-base --is-ancestor` holds against `master` (the lane has no `main` ref; HEAD is detached at `master`). `jj-lane.sh state` printed `ahead=0 behind=0`. `ls-remote origin refs/heads/master` equals the tip.
- Report landed after the lane tip (21:11:32 -0300, then report 21:12:21 -0300). Dispatch digest copied from `.ufo/watchdog.log`: `2026-10-24T19:58:12-03:00 launch kake round=48 pgid=1647007 driver=hyaku-inline attempt=1`; `2026-10-24T21:13:06-03:00 complete kake round=48; hyaku-inline attempt=1`.
- Prompt `.ufo/prompts/kake-round-48.md` carries the template contract: mission/axes binding, 1–3 claims, frontier step, L2 floor, report path, SHONEN heading, commit-hash citation, commit-then-push, push scope, L0 channel, and lane write scope. It does not quote an L2 route map that could contradict `MISSION.md`; routing is deferred to the host table.
- SHONEN is not fully checkable for promotion: box 2 is `[ ]`, and the other three are author `[~]`. Promotion stays operator-owned.
- Wave spec `w48-spec.json` has 64 roles (scout 6, executor 22, scribe 8, reviewer 7, critic 8, mutation-tester 6, sentinel 2, revenger 4, connector 1) and 27 attack roles. `.ufo/waves/round-48/w1/` contains only `swarm-registry.json`. Zero seat reports landed. The wave is not claim evidence.

### Uncommitted paths (classified, not swept)

`git status --porcelain` shows 10 paths. `status -uall` expands the first.

1. `.ufo/waves/round-46/residual/` holds eight orchestrator-owned residual reports (`CriticCitationOverreach.md`, `CriticMatrixBlindness.md`, `MutationSemanticsGap.md`, `ReviewQualityCriterion.md`, `ReviewReceiptIdentity.md`, `ReviewWitnessOracle.md`, `ScoutSiblingOverlap.md`, `SentinelBounds.md`). Mtimes are 2026-10-24 03:26–03:37, before the r48 launch. Not r48 lane work. Left uncommitted on purpose. Continuing r47 durability item, not lane debt.
2–10. Nine files under `.ufo/waves/round-48/assimilation/validate/` are untracked and each is larger than jj `snapshot.max-new-file-size` (`1MiB`): `anchors-fixed.json`, `snap-bodies.tar.xz`, `snap-bodies-run2.tar.xz`, `cases.json`, two `xmlschema11-2.html`, `nodejs.xml`, `postgresql.xml`, `ctl_accept_table_seed4242.py`. Each is byte-identical (`cmp -s`) to the already-tracked source path. Directory track skips new files over 1 MiB, so a repeat directory commit returns nothing to commit. Not swept.

No tracked path is modified.

## Claims (re-measured)

Commands were run from the lane root against committed revisions. The counters at the tip read revision bytes for rows, quotes, and the lint tool. C1 R4 still opens the retained text from the worktree; at this check the four retained files matched the tip blobs.

### C1 freshness — re-measured, improved

```
python3 -B .ufo/waves/round-48/c48_quote_truth.py --root <lane> --revision <commit>
```

- Base `766f4610…`: `C1 passed 0/4 met=False`, exit 1. Each id failed with no receipt, no row, no entry, no gate quote. Do-nothing control holds.
- Tip `fd917a42…`: `C1 passed 4/4 met=True`, exit 0, for S137, S138, S139, S249.
- Pre-fix counter extracted from `af7b217c…` and run at that revision: `C1 passed 0/4`, exit 1, reason `retained text absent` on all four. `PREDICATE = "met: passed >= 4 of 4 declared ids"` is byte-identical in `af7b217c…` and `fd917a42…`. The only code change is the path join (`os.path.dirname(RECEIPTS)` plus the receipt filename) and a comment. No seat report existed when that commit landed. The fix did not change the predicate after a score.

Independent substring check against `git show fd917a42:.ufo/waves/round-48/sources/<id>.txt`:

- S137 gate quote, 23 words, substring, sha256 `7f12d2f257b02fb498277925c0cc150bee6ff7ff076e1e8cccb3469b75a5cfdb`.
- S137 second gate quote, 21 words, substring of the same blob.
- S138, 5 whitespace tokens / 52 characters, substring, sha256 `e15db715242b22ec5e1ccd5cb14f0cb8d9e94bfc4d3961dfc5186eadcecbfce3`.
- S139, 7 tokens / 77 characters, substring, sha256 `9290f969eafc865db2607d1198d813c274c9a8a6bcb670bc2ae1a4778cb87745`.
- S249, 18 words, substring, sha256 `f5a9fd1f8f1d3c291f3ad45d9aeb243eb38c7fe94adaaca6babdd8d09f87c09f`.
- Cross-wire: none of the four quotes is a substring of another id's retained bytes.

### C2 operability — re-measured, improved

```
python3 -B .ufo/waves/round-48/c48_lint_count.py --root <lane> --revision <commit>
python3 -B <blob of scripts/citation_lint.py> --selftest
```

- Base tool sha256 `3c78a0a82f70b166776f7f7626dc7afbf9f9916a4399ae879287e4bf9662987f`: counter `dead_full_40=0 dead_short=1 live_full_40=0 live_short=0 exclusions_clean=1 met=false`, exit 1. Selftest `8/8 passed`, exit 0. Do-nothing control holds.
- Tip tool sha256 `0beba6478ce4e840b9220d9414c3d9ca888747267599e8a345b4eb67bf211235`: counter `dead_full_40=1 dead_short=1 live_full_40=0 live_short=0 exclusions_clean=1 met=true`, exit 0. Flagged tokens are the planted dead full-40 and the planted dead short. Selftest `9/9 passed`, exit 0, including `planted dead full-40-hex token flagged (1/1)`.
- Live control: `python3 -B scripts/citation_lint.py --root <lane> --json` at the clean tip worktree printed `"verdict":"clean"` and `"violations":[]`, exit 0. The previously accepted dead full-40 `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` is in `adjudicated`, not `violations`.

`git diff 766f4610… fd917a42… -- SCORECARD.md` is insertions only (81 lines). No owned-axis score line was reduced. No capabilities row was added.

## Registry and frontier checks

- `corpus/SOURCES.md` at the tip: 136 → 140 rows. Added only S137, S138, S139, S249. No existing row's cells changed. Each new row has 11 cells, status `mined`, opened `2026-10-24`, recheck exactly `180d`, no pipe and no backslash in any cell. `used-by` is `corpus/knowledge/js-rendering-queue.md` for S137–S139 and `corpus/knowledge/dynamic-rendering-workaround-limits.md` for S249. Both entries exist and open with `source:` / `verified-at:` / `recheck:`.
- Committed collision scratch: `reg-ids` 136 lines (S001–S136), `staged-ids` 115 lines (S137–S251), `collisions` empty. `guard-collisions` contains `S137`, so the guard is shown able to fail.
- Quarantine receipt `quarantine-handcheck.json`: 12 rows, 9 `absent` (S142, S143, S148, S156, S161, S193, S194, S195, S206), 3 `unreachable` (S154 HTTP 404, S178 HTTP 429, S184 HTTP 404). Evidence-verified from the committed receipt; not re-fetched. Neither rejected slug is in the tip tree.
- Census re-run: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exit 0, twelve pre-existing W04 warnings, then `kake ok`.
- Validate-before-append does not re-derive. The committed mirror `assimilation/validate/corpus/SOURCES.md` is byte-identical to the post-append registry (140 rows, includes S137–S249). No pre-append census stdout is filed beside the scratch. The landed rows validate now; the order claim is not proven by the committed mirror.

## Spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S137 | admit | live `https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics` (HTTP 200, saved body 221711 bytes at 2026-10-24 21:17:07 -0300, sha256 `17f924c3ac900d6e1a6448e5ee09a863716780767e2f6c1acf59d8a742c13af6`, not equal to the receipt raw sha256 `2a672e81…`) and committed `S137.txt` | agree | The 23-word rendering-queue quote is in the live extracted text. The live body has drifted from the in-round raw bytes; the quote is still a substring of the committed retained text. Row is mined, recheck `180d`, used-by names the admitted entry. |
| `client-rendered-source-citation-rule.md` | reject | staged file under `shokuknow/merge/kake/knowledge/...` and cited `shokuknow/lanes/kake/round9/.evidence/archive_route_r9.txt` | agree | `source:` cites a campaign-internal evidence path, not a public row. The opened file is an archive-route measurement note. Contract v1 rule 1 is not met for a publisher-domain row. Flip is a restatement against a re-openable public source. Not present in the lane tree. |
| `ollama-openapi-contract.md` | reject | staged file; kake `PROVINCE.md` Adjacent; kama `PROVINCE.md` domain line | agree | The staged ground line and kake Adjacent both assign local model-serving endpoints to kama. kama's domain is local model serving and endpoint health. Out of province. Flip (operator amends kake's province, or kama releases it) matches the boundary. Not present in the lane tree. |

S137's Gate quote is 23 words, within the ≤25-word rule. S138's 5-token quote is 52 characters, inside the counter's 12–120 character alternate. S249's quote is 18 words.

## Axis verdicts

- freshness: improved. 0/4 → 4/4 on the declared ids. Score stays 10 (HOLD).
- operability: improved. `dead_full_40` 0 → 1; selftest 8/8 → 9/9; live lint clean. Score stays 10 (HOLD).
- depth: unchanged. No depth claim; SCORECARD diff is additive.
- coverage: unchanged. No coverage-score claim. Frontier ground was entered as expansion, not as a coverage-axis claim.
- calibration: unchanged. The round disclosed the counter path fix and the empty wave. The post-append mirror overstates validate-before-append; that is a routed defect, not a harmed score.
- adjacency: unchanged. The Ollama candidate was rejected rather than absorbed.

## Trend verdicts

- expansion: improved. Two admitted knowledge entries on frontier ground `PROVINCE.md` still listed as open ("canonical signals and JS rendering"), each citing a mined row opened this round, plus four new registry rows.
- quality: improved. The citation gate now fails a dead full-40 token (do-nothing control rejected; live controls clean), and the new quotes are substrings of their own retained bytes. Rows were normalized to bare `180d` with no pipes.
- discernment: improved. This outside sample agrees on the re-opened admit and on both rejects. The lane's own `unchanged` grade was correct before this check existed; the check now agrees. Quarantine was not re-fetched.

## Routed defects

1. Next round must file a pre-append census stdout and a pre-append `SOURCES.md` digest before any append. The committed `validate/` mirror is the post-append registry, so validate-before-append is not re-derivable.
2. C1 R4 should read retained bytes with `git show <revision>:` rather than opening the worktree. The disclosed path fix did not change the predicate, and the four files matched the tip at this check, but a dirty tree could still move the score.
3. Do not call the committed census mirror full-repo while directory-track has skipped the nine >1 MiB copies. Name those files with `--allow-large` only if a later claim needs them inside the mirror. Do not sweep them in a closure.
4. Operator, not the lane: the eight `round-46/residual/` reports stay uncommitted orchestrator evidence. The 64-seat wave produced 0 reports and is not claim validation.
