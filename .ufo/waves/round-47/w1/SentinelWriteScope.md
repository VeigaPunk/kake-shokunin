# Sentinel — write scope (round-47, wave 1)

- seat: `SentinelWriteScope-2` · role: sentinel · axes: operability (scope/boundary evidence)
- lane: `/home/vgpnk/Projects/shokunin/kake-shokunin` · base `cd42e3c310ba442e89dde638ba6401adaefaf3e8` · measured tip `766f4610b64f35a0f402b37eb1d8be2d4d634c0f`
- measurement window: 2026-10-24 04:39–04:44 -0300 (07:39–07:44Z), i.e. live during dispatch (registry rewrite 07:40:04Z)
- method: read-only git plumbing (`status`, `log`, `show`, `ls-tree`, `cat-file`, `diff`, `for-each-ref`), `stat`/`find`, byte reads; one local sandbox clone under scratch for a mutation control. No jj command was executed (see F1). No sibling repo or fleet-root file was opened.

## Verdict rollup

| # | Surface | Result | Severity |
|---|---|---|---|
| F1 | Lane `.jj` state + git object store during dispatch | **changed** by a `jj log` snapshot at 07:40:23Z | medium |
| F2 | Counters' `--revision` → `git show` argv | option injection writes outside root (observed in sandbox) | low |
| F3 | `git cat-file -e HEAD:.ufo/waves/round-46/residual/<f>.md` | all 8 absent; cited as evidence in LOG | low |
| F4 | Sibling / fleet-root / `scripts/` / templates / MISSION / PROVINCE in the committed diff | **no path touched** | pass |
| F5 | Deletion count base..HEAD | **0** (append-only) | pass |
| F6 | Misroot receipt vs its own stdout | receipt records fleet `kake.report-baseline` and `watchdog.log` as ` M` | info |
| F7 | Declared artifact list vs actual committed diff | 2 committed paths outside the declared list (109 of 5,073 added lines) | info |
| F8 | Spot-check row 18 cites `.ufo/watchdog.log` (fleet root, mutable) | unverifiable from lane bytes by construction | info |

## F1 — medium — a read-intent `jj` command mutated lane `.jj` and added a git ref during dispatch

Evidence (all observed):

```
$ stat -c '%y %n' .jj/repo/op_heads/heads/c3662229… .jj/working_copy/tree_state .jj/working_copy/checkout
2026-10-24 04:40:23.326633158 -0300 .jj/repo/op_heads/heads/c3662229fc1bfdbe…5e357d01
2026-10-24 04:40:23.327121719 -0300 .jj/working_copy/tree_state
2026-10-24 04:40:23.328839480 -0300 .jj/working_copy/checkout

$ strings -n 6 .jj/repo/op_store/operations/c3662229…
snapshot working copy"
jj log -r @ --no-graph

$ git cat-file -p c77361c8e3bd646311eee34f3e0655c186655d36
tree af522d20ef1dab437af4e81fba9a6de4ac7e38de
parent 766f4610b64f35a0f402b37eb1d8be2d4d634c0f
committer kake-shokunin <kake@shokunin.local> 1792827623 -0300

$ git diff --name-status 766f461 c77361c8
M	.ufo/waves/round-47/w1/swarm-registry.json        (33 insertions, 33 deletions)

$ find .git/objects -type f -newermt "2026-10-24 04:38:00"   → 7 objects at 04:40
$ find .git/refs   -type f -newermt "2026-10-24 04:38:00"   → refs/jj/keep/c77361c8e3bd646311eee34f3e0655c186655d36
```

Exploit path: any seat or lane helper running `jj log` / `jj st` in the lane checkout with a dirty working copy causes jj to snapshot that copy, which writes a new operation, a new working-copy commit, new loose objects and a new `refs/jj/keep/<sha>` ref. Here the snapshot pinned the **dispatched** registry (32 non-null `agentId`s, `updatedAt` 07:40:04.494Z) that the L1 never committed — the committed blob `bce58d7f…` still has `agentId: null`. The worktree file is now `e5b5ee10c87463394f9dc2277a4470d7026ac68636036052c4fe03ec1b341855`.

Impact: literal violation of the wave bound "do not run mutating jj/git commands in the lane checkout" and "refs/bookmarks". No branch moved (`.git/refs/heads/master` mtime 04:37:54, `git for-each-ref refs/heads` → `master 766f461`; `.git/packed-refs` 2026-10-23 09:05), and `.git/index` has no staged entry (`git diff --cached --name-status` empty). The pinned object is reachable only through `refs/jj/keep`, so a later `jj git export` would surface uncommitted wave bookkeeping in lane history.

Attribution limit: the op file records the command but not the seat. Timing (07:40:23Z, 19 s after the registry write, inside the dispatch window) places it in this wave; a driver-side lane-state probe is equally consistent with the evidence and cannot be excluded from lane bytes.

Smallest remediation: read lane head with `git rev-parse HEAD`, or `jj log --ignore-working-copy`, from seats; keep `jj` state recording on the driver side. Do not delete the keep ref from inside the wave — that is another mutation.

Note on `.git/index` mtime 04:40:23.323 (3 ms before the jj op): consistent with a `git status` stat-cache refresh, and I cannot exclude my own read at that instant as the cause. [INFERENCE] No content change: `git diff --cached` is empty.

## F2 — low — `--revision` is interpolated into `git show` as an option position

Evidence:

- `.ufo/waves/round-47/c47_registry_count.py:75`, `.ufo/waves/round-47/c47_routed_count.py:82`, `.ufo/waves/round-47/c47_r4_mutation_check.py:25` all build `["git", "-C", root, "show", f"{revision}:{rel}"]` with no validation of `revision`.
- Docstrings at `c47_registry_count.py:21` and `c47_routed_count.py:23`: "Read-only: materializes committed bytes via `git show`/`git ls-tree` only."
- Sandbox control (clone of tip `766f461` under `/fast/scratch/hyaku/kake-r47/SentinelWriteScope/sandbox`, local, never pushed):

```
$ python3 -B .ufo/waves/round-47/c47_registry_count.py --root . \
    --revision='--output=/tmp/kake-r47-escaped'
could-not-evaluate: cannot ls-tree .ufo/waves/round-47/verification at --output=/tmp/kake-r47-escaped   (exit 2)
$ ls -la '/tmp/kake-r47-escaped:SKILL.md'
-rw-r--r-- 1 vgpnk vgpnk 13776 Oct 24 04:43 /tmp/kake-r47-escaped:SKILL.md
```

Exploit path: the composed token `--output=<path>:<rel>` is parsed by git as the `--output` option, so a revision string beginning with `-` redirects git's own output to a caller-chosen absolute path outside `--root`. The file was created outside the lane; I removed it immediately (`rm -f '/tmp/kake-r47-escaped:SKILL.md'`).

Not reachable today: all three scripts take the revision from argv only (`args.revision`, call sites above); no revision is read from a ledger row, receipt or other record, so no untrusted string reaches `git show` in the round-47 usage. Impact is therefore "read-only invariant false for malformed input", not an exploited path.

Smallest remediation: reject a revision that does not match `^[0-9a-f]{4,64}$|^HEAD$` before invoking git (or resolve it once with `git rev-parse --verify --end-of-options` and pass the resulting object id).

Related, not a defect: `--json` writes only when explicitly given, defaults to stdout (`const="-"`, `c47_registry_count.py:67`, `c47_routed_count.py:74`), and the R4 mutation script is entirely in-memory (`exec(compile(...))` + `re.subn`, no temp file, no write).

## F3 — low — evidence the round says it re-opened is not in the committed tree

```
$ git status --porcelain
?? .ufo/waves/round-46/residual/
$ du -sh .ufo/waves/round-46/residual      → 100K (8 reports, mtimes 03:26–03:37, all before the first r47 commit 04:05)
$ git cat-file -e HEAD:.ufo/waves/round-46/residual/CriticCitationOverreach.md   → absent (same for all 8 names)
```

`LOG.md:1893` names five of them by bare filename (`CriticCitationOverreach.md`, `ReviewWitnessOracle.md`, `CriticMatrixBlindness.md`, `MutationSemanticsGap.md`, `ReviewReceiptIdentity.md`) and states they "remain unmodified and orchestrator-owned". Commit `59146c9` ("scope inherited residual evidence") changed only 5 documentation files and did not commit the reports.

Impact: a reader at the committed tip cannot open the evidence the round asserts it re-opened; the bare filenames have no path, so the lane's path gate cannot resolve them either. Not a filed count (the sentence files no number, and the five named are the five it describes), so the QUALITY receipt-identity criterion is not violated — the spot-check already routes this as a durability item (`round-47-verifier-spotcheck.md`, "one routed durability item"), and that routing is accurate as of HEAD.

Smallest remediation: commit the eight reports (or the five cited) under the round that owns them with path + sha256 lines, or cite `.ufo/waves/round-46/residual/<name>.md` with an explicit "untracked, orchestrator-owned" marker.

## F4 — pass — committed diff touches no production, sibling or fleet path

```
$ git diff --name-only cd42e3c… HEAD | cut -d/ -f1-2 | sort | uniq -c
 1 corpus/knowledge   2 corpus/lessons   1 corpus/quality   1 corpus/QUALITY.md
 1 corpus/README.md   1 corpus/SOURCES.md   1 LOG.md   1 SCORECARD.md   1 SKILL.md   21 .ufo/waves
$ git diff --name-only cd42e3c… HEAD -- scripts/ templates/ MISSION.md PROVINCE.md   → (empty)
$ git diff --numstat cd42e3c… HEAD | awk '{a+=$1;d+=$2} END{print "added="a" deleted="d}'
added=5073 deleted=0
```

31 paths, all additive. The lane's production gates (`scripts/redirect_audit.py`, `scripts/citation_lint.py`, `freshness-sweep.mjs`, `ledger_latest_check.py`) are untouched. Pre-existing out-of-lane citations in `corpus/SOURCES.md:64,137-140` (`tameshi-shokunin`, `kama-shokunin`) and `corpus/QUALITY.md:649` (`…/.ufo/reports/round-33/kake.md`) are **not** additions of this diff — verified present in `git show cd42e3c:corpus/SOURCES.md` and `git show cd42e3c:corpus/QUALITY.md`.

## F5 — pass — append-only

`git diff --numstat` over the whole range: `deleted=0`. The five commits since base (`846138c`, `714e707`, `7855262`, `59146c9`, `766f461`) are export-only (`git log` reflog lines "export from jj"); no commit contains a deletion.

## F6 — info — the misroot receipt records fleet state as dirty

`verification/misroot-sweep.txt` (37 lines) is committed as the round's own boundary receipt:

```
1  command: git -C /home/vgpnk/Projects/shokunin status --porcelain
6   M .ufo/state/kake.report-baseline
15  M .ufo/watchdog.log
37 result: no kake/round-47 misroot files to copy/delete. All .ufo/state/* and watchdog entries were left untouched.
```

`LOG.md:1889` restates this as "Driver `.ufo/state/*`/watchdog churn and all other-root untracked files were left untouched". Read strictly, the receipt proves an *action* claim (nothing copied or deleted) and a marker scan over untracked paths only; it cannot support a *state* claim, because its own stdout shows `kake.report-baseline` and `watchdog.log` modified at sweep time and the receipt has no before/after hash pairing. I did not open the fleet root, so I cannot say whether those modifications predate this wave.

Also [INFERENCE], not observed: `git -C <fleet> status` may rewrite the fleet repo's index stat cache. Verifying that would require reading outside my bound, so it is left open rather than passed.

Smallest remediation: boundary receipts that assert non-modification of shared state should carry before/after sha256 of the named paths (or be limited to the narrow claim "this wave created/deleted nothing under X").

## F7 — info — two committed paths sit outside the declared artifact list

`corpus/quality/citation-adjudications.md` (+25) and `corpus/lessons/round-47-verifier-spotcheck.md` (+84, commit `766f461`) are in the committed diff but not in the round-47 artifact list I was given. Both are in-lane corpus documents; neither is production, and the ledger edit is the R3/R4 correction the round requires. Consequence for audit: a scope check driven from the declared list alone would leave 109 of the 5,073 added lines unreviewed.

Smallest remediation: add both paths to the declared target-artifact list.

## F8 — info — the closure spot-check cites a fleet-root mutable file

`corpus/lessons/round-47-verifier-spotcheck.md:18` cites `.ufo/watchdog.log` (self-described "mutable — the digest is the pointer") with two timestamped lines. In the lane: `ls .ufo/watchdog.log` → No such file; `git ls-tree -r HEAD -- .ufo/watchdog.log` → empty. The citation cannot be resolved or re-checked from committed bytes, and it is the one committed round-47 evidence row whose source lies outside the declared lane bound.

Smallest remediation: retain the two log lines verbatim in `verification/` (a small receipt), and cite that receipt.

## Worktree state at report time (04:43 -0300)

```
 M .ufo/waves/round-47/w1/swarm-registry.json
?? .ufo/waves/round-46/residual/
?? .ufo/waves/round-47/w1/*.md            (16 seat reports, 18–12,624 bytes)
```

All seat reports land in the registry's `reportDir` (`.ufo/waves/round-47/w1/`); `ConnectorBoundary.md` is 18 bytes at 04:42 — a stub, not a scope issue but worth the L1's eye. Worktree registry permissions are `0600` while the committed blob is `100644`; git does not track that difference, and no other lane file outside `.ufo/waves/round-47` has an mtime later than the HEAD commit.

## Checks not run, and why

- No inspection of sibling repos, the fleet root, `.ufo/state/` or `.ufo/watchdog.log` — outside my read bound. `.ufo/state/` and `.ufo/watchdog.log` do not exist in the lane tree (`git ls-files` count 0), so "untouched in lane" is evidenced by absence, not by hash comparison.
- No `jj` command executed in the lane — running one would itself reproduce F1.
- No lane file edited, no lane git/jj write, no push; the sandbox clone under `/fast/scratch/hyaku/kake-r47/SentinelWriteScope/` is local-only and the one `/tmp` artifact created by the F2 control was deleted.
