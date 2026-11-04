# ExecShonenLedger — C1: every SHONEN box classified from committed bytes

Round 77, wave w1, attempt 1. Lane `kake-shokunin`, base
`a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`. Frozen contract
`.ufo/waves/round-77/contract.md` §C1 as amended mid-wave by
`.ufo/waves/round-77/amendment-1.md` and `.ufo/waves/round-77/amendment-2.md`.
Only the three named files and this report were written; no commit, no ref, no
worktree mutation, no network, no tool installed or upgraded.

## 1. Result — both observed lines

Frozen predicate, the same sentence in the ledger, the counter and this report:

```
met  <=>  boxes == 4  and  unexamined == 0  and  mismatches == 0
```

Base state, exact frozen form (the line is amendment 2 **A1**'s, not the
contract's earlier `mismatches=4`):

```sh
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . \
  --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=0 met=false
EXIT=1
```

stderr: `diagnostic: corpus/knowledge/shonen-ledger.json is absent at the revision: every box is unexamined`.
A `[ ]` marker with no row is **not** a mismatch (A1/A4); the red is
`unexamined=4`.

After state — the current worktree's three files on top of the round's
instrument commit `893b0f33`, at a no-commit tree snapshot (§4). This is the
shape the closure commit will have:

```sh
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . \
  --git-dir <scratch>/snap/repo.git --revision f0effe0b808c2e7cdc7ef313adc28dd02c7c3d78 \
  --work <scratch>
C1 revision=f0effe0b808c2e7cdc7ef313adc28dd02c7c3d78 boxes=4 evidenced=3 gap=1 unexamined=0 mismatches=0 met=true
EXIT=0
```

The same three files on top of the contract base `a2cc5f51` gave the identical
line (`evidenced=3 gap=1 unexamined=0 mismatches=0 met=true`, tree
`b1e74a86d79e1cb10537944375f99e156036a353`), which is how the `corpus/SOURCES.md`
edit that landed in `893b0f33` was shown not to disturb box 1's 77/77 id
resolution.

`evidenced=3 gap=1` fills the contract's after-shape
(`boxes=4 evidenced=<e> gap=<4-e> unexamined=0 mismatches=0 met=true`). The
single gap is box 2 and it is the gap amendment 1 **A12** predicted.

## 2. Amendments consumed (and what they changed in this build)

| Amendment | Term | How this build implements it |
|---|---|---|
| 2 A1 | base arithmetic | a marker with no row is a mismatch only for `[~]`/`[x]`; base is `unexamined=4 mismatches=0`, exit 1 |
| 2 A2 | checks are declarations | `checks[]` carry `{id, kind, path, params, observed}`; kinds are exactly `exists`, `count_at_least`, `regex_count`, `all_ids_resolve`, `no_match`; an unknown kind or measure is a mismatch; **no command path exists in the counter** |
| 2 A3 | exact comparison | one normalisation: ints as ints, bools as bools (never `True == 1`), strings exact, containers element-wise; `holds` is accepted but never read |
| 2 A4 | box range / revisions | a row outside box 1–4 is a mismatch (never ignored); `--revision` required, no `HEAD` default; one row per box; `[x]` needs a verifier; `[~]`/`[x]` with no row, `" "` over an evidenced row → mismatch |
| 2 A5 | attack fixtures | the selftest contains 02–07 by name (§5) and each stays red |
| 1 A11 | frozen box scopes | the ledger's ten checks are exactly the four box-1, three box-2, two box-3 and one box-4 scopes; no extra check asserts anything else |
| 1 A12 | a gap is a result | box 2 is `status=gap` with the failing observation, `reason` and `flip`; a `status=evidenced` row over a failing frozen check is a mismatch |

Two consequences worth naming. First, the original contract's
`mismatches=4` base target and the frozen (a) enumeration are superseded by
A1, so no `[ ]`-with-no-row mismatch exists. Second, because A2 forbids
executable checks, the box-3 evidence that a command *runs* is gone; box 3
claims A11's path-existence scope only, and the playbook's non-executable spans
are routed in §8 rather than folded into the row.

## 3. Files changed (lane-relative)

| File | Change | Lines |
|---|---|---|
| `.ufo/waves/round-77/c77_shonen_ledger.py` | new counter + 26-case selftest (declaration-only vocabulary) | 1112 |
| `corpus/knowledge/shonen-ledger.json` | new ledger, `shonen-ledger/v1`, 4 rows, 10 checks | 138 |
| `SHONEN.md` | markers `[~] [ ] [~] [~]` + one pointer line per box; box text unchanged | 12 |
| `.ufo/waves/round-77/w1/ExecShonenLedger.md` | this report | — |

```
6a166f19bc9a14904fbd3bda05f4166b52ac63650923a84b9b29c3ba70b93ee4  SHONEN.md
7962018bf8166064fef4a28312e856906e80f1dc59c72e3aaf6bc3f475382a8b  corpus/knowledge/shonen-ledger.json
2d66e5af30b90f50875ac820879430b55f0c344e3c4965b6bcc203a3567a4396  .ufo/waves/round-77/c77_shonen_ledger.py
```

**Writer collision, recorded:** between this seat's first base run and the
final build, `.ufo/waves/round-77/c77_shonen_ledger.py` was edited by another
writer while the amendments were landing (the edit rejected `kind="command"`
with an A2 comment). The delivered file is this seat's full rewrite, which
implements A2 natively and deletes the command path; no other writer's
semantics survive because there is nothing left to preserve. The amendment
files themselves appeared mid-wave, not as this seat's writes.

**Repository state at measure time, recorded:** HEAD moved during the wave from
`bc2e5fb9` to `893b0f33` ("round-77: instruments …", an `export from jj`),
which committed **earlier intermediate versions** of all three owned files
(counter `7f35ad45…`, ledger `ba11efe5…`, SHONEN.md `5c3859e1…`) and a
`corpus/SOURCES.md` edit. The worktree carries the final bytes quoted above;
the after-state in §1 is measured at a snapshot of `893b0f33` + those final
bytes, and the closure commit must carry them (the digests in this section are
the ones to check). Separately, the git index is stale relative to `HEAD`
(`git status` reports 21,358 staged deletions; `git ls-files` holds no entry
for these paths) — a `jj`-export artifact, not this seat's doing: this seat ran
no `git add`, `rm`, `read-tree` or `write-tree` against the lane repository,
only against scratch object stores. A plain `git commit` in that state would
revert the round's instrument landing, so closure should go through the lane's
history tool as usual.

## 4. Which bytes the green line read (snapshot disclosure)

No commit is allowed, so the after revision is a **tree object** in a scratch
bare repository, built with plumbing only — no commit, no ref, no index inside
the lane, no lane object written (the scratch object store reads the lane's
objects through `objects/info/alternates`):

```sh
git init --bare -q <scratch>/snap/repo.git
printf '%s\n' "$LANE/.git/objects" > <scratch>/snap/repo.git/objects/info/alternates
export GIT_DIR=<scratch>/snap/repo.git GIT_INDEX_FILE=<scratch>/snap/index
git read-tree 893b0f334bac216cec2768c4402e3ccb1a494423   # the round-77 instrument commit
for p in SHONEN.md corpus/knowledge/shonen-ledger.json .ufo/waves/round-77/c77_shonen_ledger.py; do
  blob=$(git hash-object -w --stdin < "$LANE/$p")
  git update-index --add --cacheinfo 100644,$blob,$p
done
git write-tree        # -> f0effe0b808c2e7cdc7ef313adc28dd02c7c3d78
```

**21,358 entries**: `893b0f33`'s tree with exactly three blobs replaced
(`git diff a2cc5f51 893b0f33` is the round's own instrument landing; the
snapshot differs from `893b0f33` by `3 files changed, 153 insertions(+), 230
deletions(-)`, which is the earlier ledger being replaced by this one). The replacement blobs are
`ba1fbe97e213b3f24da9bdcd50e64fdc689c1287` (SHONEN.md),
`6b831c71779051a8c3200ed3faff9a8e179bb19c` (ledger) and
`a64633f11473829e26fa82bbc2a1e6e40aa91f33` (counter), each the content hash of
the worktree file in §3. Every check reads `git show <rev>:<path>`; nothing in
the derivation touches the worktree, which is why an untracked ledger cannot
influence a base run (A5 fixture 07).

## 5. Selftest

```sh
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --selftest --work <scratch>
selftest: 26/26 passed
EXIT=0
```

Each case builds a fixture tree (`git init --bare` + `hash-object -w` +
`update-index --cacheinfo` + `write-tree`; no commit) and asserts the printed
line and the exit code.

| # | Case | Asserts |
|---|---|---|
| 1 | `clean-four-boxes` | 1 evidenced + 3 gap, `met=true`, exit 0 |
| 2 | **A5-02** `evidenced-without-measurement` | four `evidenced` rows carrying `holds=true` and no measurement ⇒ invalid rows ⇒ red |
| 3 | **A5-03** `x-over-gap-fabricated-verifier` | `[x]` over gap rows with a fabricated verifier ⇒ red |
| 4 | **A5-04** `command-check` | `kind="command"` ⇒ outside the vocabulary ⇒ red |
| 5 | **A5-05** `row-for-box-7` | box outside 1–4 reported ⇒ red |
| 6 | **A5-06** `observed-contradicts-derivation` | recorded ≠ re-derived ⇒ red |
| 7 | **A5-07** `untracked-worktree-ledger` | ledger only in the worktree ⇒ unexamined=4, `met=false`, exit 1 |
| 8 | `missing-ledger` | `evidenced=0 gap=0 unexamined=4 mismatches=0 met=false`, exit 1 (A1 base shape) |
| 9 | `empty-checks` | empty `checks` ⇒ unexamined for that box, red |
| 10 | `fake-path` | `exists` over an absent path ⇒ red |
| 11 | `x-with-verifier-and-clean-checks` | `[x]` + verifier + all checks true ⇒ `evidenced=4 met=true` |
| 12 | `x-without-verifier` | `[x]` without a verifier ⇒ red |
| 13 | `tilde-with-no-row` | `[~]` over no row ⇒ red |
| 14 | `space-over-evidenced` | `" "` over an evidenced row ⇒ red |
| 15 | `duplicate-row` | two rows for one box ⇒ red |
| 16 | `threshold-below-min` | `count_at_least` below `params.min` ⇒ red |
| 17 | `evidenced-with-failing-check` | `status=evidenced` over a failing frozen check ⇒ red (A12) |
| 18 | `gap-without-flip` | gap row without `flip` ⇒ invalid row ⇒ red |
| 19 | `five-boxes` | `boxes=5 met=false` |
| 20 | `missing-checklist` | no SHONEN.md ⇒ `boxes=0 met=false`, exit 1 |
| 21 | `bad-schema` | foreign schema ⇒ exit 2 |
| 22 | `malformed-json` | unparseable ledger ⇒ exit 2 |
| 23 | `marker-drift` | checklist marker ≠ row `marker` ⇒ red |
| 24 | `unknown-measure` | measure outside the vocabulary ⇒ red |
| 25 | `observed-type-mismatch` | `"0"` vs `0` ⇒ red (A3 exact typing) |
| 26 | `row-without-box` | row missing `box` ⇒ invalid row ⇒ red |

## 6. Per-box derivation (frozen scopes → checks → observed → verdict → status)

All ten observations below were re-derived from committed bytes at the
snapshot revision and matched the ledger exactly; every verdict is the
counter's own, not the ledger's.

| Box | Check | Kind / measure | Observed | Verdict | Box status |
|---|---|---|---|---|---|
| 1 | `b1-ids` | `all_ids_resolve`, SKILL.md → corpus/SOURCES.md | `{"ids": 77, "resolved": 77, "unresolved": 0}` | true | — |
| 1 | `b1-tables` | `count_at_least` `markdown_tables_with_min_rows` (min_rows 3, min 3) | `18` | true | — |
| 1 | `b1-registry` | `count_at_least` `registry_rows_with_code_cell` (min 20) | `105` | true | — |
| 1 | `b1-checklist` | `count_at_least` `checklist_headings` (min 1) | `1` | true | **evidenced** |
| 2 | `b2-rounds` | `count_at_least` `round_sections` (min 3) | `56` | true | — |
| 2 | `b2-receipts` | `count_at_least` `wave_receipt_paths` (min 20) | `98` | true | — |
| 2 | `b2-missing` | `no_match` `wave_receipt_paths_missing` | `1` | **false** | **gap** |
| 3 | `b3-scripts` | `no_match` `skill_script_paths_missing` | `0` | true | — |
| 3 | `b3-invocations` | `no_match` `skill_python_invocations_missing` | `0` | true | **evidenced** |
| 4 | `b4-lanes` | `no_match` `cross_lane_citations` (glob `corpus/knowledge/*.md`, exclude `freshness-*.json`) | `0` | true | **evidenced** |

The box-2 failing pointer is exactly A12's: `.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt`. The row carries the flip: the pointer resolves (file committed, or LOG.md's citation corrected append-only), `wave_receipt_paths_missing` re-derives to 0, and the row can move to evidenced with the same three checks.

Scope statements are written into the ledger rows, not implied: box 3's `note` records that A11's scope excludes the `node ~/Projects/...` and `.mjs` spans; box 4's `note` records the `freshness-*.json` exclusion and the measure's `.shokunin` naming limit; box 4 also records that PROVINCE.md's own province lines are **not** claimed by the frozen scope.

## 7. Real-artifact kill tests (same counter, same snapshot base)

Each variant is the snapshot tree with one blob replaced; same command as §1
with the variant tree (base `f0effe0b`).

| Variant | Replacement | Observed |
|---|---|---|
| A — fabricated observation | `b2-missing` recorded `observed` changed `1` → `0` | `evidenced=3 gap=0 mismatches=1 met=false`, EXIT=1; finding `observation-differs box 2 b2-missing — recorded 0 but re-derived 1` (tree `0eaf66ba39472ca2bc4b2c8355dd48591c41ac18`) |
| B — gap relabelled evidenced | box 2 `status` changed to `evidenced` while its own `no_match` check still derives 1 | `evidenced=3 gap=0 mismatches=2 met=false`, EXIT=1; findings `marker-understated box 2` and `status-unsupported box 2 — … amendment 1 A12 makes a failing check a gap` (tree `2605fe018635a2400512299b76595ab4b90dfba7`) |
| C — false tick | box 1 marker changed `[~]` → `[x]` | `evidenced=2 gap=1 mismatches=2 met=false`, EXIT=1; findings `marker-disagrees-with-row box 1` and `verifier-missing box 1` (tree `d0c8f65de0f697720893c7e2d357f9e7590f3370`) |

Variant A is the sharpest: the box-2 gap is the claim's only red result, and
the counter refuses a ledger that paints it green.

## 8. Routed observations (recorded, not claimed)

1. **Box 3's frozen scope is narrower than the box's words.** A11 box 3 covers
   `scripts/*.py|sh`, counter paths and `python3 -B <path>` targets; it does not
   cover the three `node ~/Projects/webzites/...` spans (SKILL.md:59, :111,
   :224; the checkout is absent and the page annotates :59/:111 "not executable
   until restored and re-checked") nor `node scripts/kimi-surface.mjs sync-check
   <id>` at SKILL.md:222, whose target does not exist in this repo. The box-3
   row's `note` says this; the defect stays open and is routed.
2. **Box 2's gap pointer** — `.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt`
   — is the only non-glob receipt path among 98 that LOG.md names and the
   revision lacks. Repair is a citation correction (append-only) or committing
   the receipt; either flips box 2.
3. **The lane's citation gate is red at the base revision**, adjacent to this
   claim and not part of it:
   `python3 -B scripts/citation_lint.py --root . --revision a2cc5f51…` exits 1
   on `SCORECARD.md:4926: 153fa2a9eda8d95618697186feb18574cc7daae1` and
   `LOG.md:2317: b569bb638 (dead_citation)`. Both are quoted prose tokens (a
   mutant receipt line inside an `[r76-correction]` row; the one-char-drift
   token whose own sentence says "not an object name"), not task citations.
   They are not adjudicated in `corpus/quality/citation-adjudications.md` and
   are routed for adjudication or repair.
4. **The counter file itself was edited by another writer mid-wave** (§3); the
   amendments also landed mid-wave and superseded the contract's original base
   target. Both are recorded here rather than silently absorbed.

## 9. What a non-author must do to promote a `[~]` to `[x]`

`[x]` is refused without a verifier, over a non-x row, and over a
non-evidenced row; the counter re-derives every number the signer would
otherwise be trusting (variant C shows two of those refusals).

1. **Re-run at the revision to sign.** A seat that is not the author runs
   `python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . --revision <full-hash>`
   and commits a receipt with the printed line and exit code.
2. **Re-derive at least one observation per kind from the bytes:** resolve an
   `S###` row by hand, count a table's data rows, test one named wave-receipt
   path with `git cat-file -e <rev>:<path>`, list one `corpus/knowledge` entry
   for a sibling-lane citation. A signature over a line the signer did not
   re-derive is the `holds`-as-given failure A3 exists to prevent.
3. **Name themselves in the row:** add
   `"verifier": "<seat id> — <date> — <receipt path under .ufo/waves/round-77/>"`
   to the row, set that row's `marker` to `"x"`, and set the box marker in
   `SHONEN.md` to `[x]` so the two agree.
4. **Re-run** and require `mismatches=0`; a marker mismatch or an observation
   drift reddens the run.
5. **Box 2 first satisfies its flip** (the missing pointer resolves), then
   moves to `status=evidenced`; signing a `gap` row is a mismatch, and a
   `status=evidenced` row over a failing frozen check is a mismatch (A12).

No `[x]` exists this round: no named non-author has signed a box.

## 10. Reproduce / limits

```sh
# base (red, amendment 2 A1 shape)
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . \
  --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68
# selftest
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --selftest --work <scratch>
# after (green at the snapshot tree; rebuild it with §4's plumbing)
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . \
  --git-dir <scratch>/snap/repo.git \
  --revision f0effe0b808c2e7cdc7ef313adc28dd02c7c3d78 --work <scratch>
```

- Without `--json`, stdout is exactly one line (`| wc -l` = 1); findings and
  diagnostics go to stderr. `--json` appends the per-box derivation.
- Exit map: 0 met, 1 not met, 2 could-not-evaluate (unresolvable revision,
  malformed or foreign-schema ledger, a check's auxiliary resolution file
  absent, a pattern without a capture group), 64 usage. The frozen form only
  yields 0/1.
- A missing ledger is the red state, not a fault (A1); a malformed or
  foreign-schema ledger is exit 2.
- **The counter cannot judge whether a scope is sufficient for its box's prose** —
  it re-derives each declared observation and its own threshold verdict. The
  scopes are amendment 1 A11's; sufficiency is a reviewer judgement and §6 is
  printed for it.
- **Append sensitivity:** the ledger pins numbers over `SKILL.md` and `LOG.md`
  at the measured revision. A later round that edits either file (e.g. appends
  a round-77 gate-registry row, or logs round 77) will change those numbers and
  re-derive a mismatch until the ledger is refreshed at the new revision. That
  is intended — the check is a receipt, not a tolerance — and the counter's
  finding lines print the replacement values verbatim.
- `derived-at` in the ledger records `a2cc5f51` as the first measurement
  revision and is not a gate; observations are always re-derived at
  `--revision`.
- Concurrent seats were editing `scripts/sitemap_audit*.py` and
  `corpus/QUALITY.md`; none of their files is a check input here, and the
  derivation reads only committed bytes at the named revision, so their
  in-flight work cannot move a number in this report.
- Environment: `python3` 3.14.8 (host), git plumbing only; no network; no
  package installed or upgraded (host pacman paused as ruled; nothing needed).
  Scratch `/fast/scratch/hyaku/kake-r77/ExecShonenLedger` was removed after this
  report; every command, tree id, blob id and digest above is recorded here.
- No blocker. No publish, deploy or operator-owned property contact: none
  occurred.
