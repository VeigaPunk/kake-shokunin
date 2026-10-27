# ScribeC2SkillRows

Drafting only: no SKILL.md, SCORECARD.md, counter or tool edit; no lane git/jj mutation. The one commit I made is in a
scratch clone under `/fast/scratch/hyaku/kake-r59/ScribeC2SkillRows/lane` (created from the lane with `git clone -q --shared`,
`git rev-parse --show-toplevel` asserted, `-c user.name=selftest -c user.email=selftest@local`). Scratch deleted at exit; the six
probe logs are copied to `.ufo/waves/round-59/w1/ScribeC2SkillRows.files/`. Base facts used: base `fd6303ce5c14b3f892dec586297a942ab6e4193b`,
contract commit `45a92b64ac8a0f82dba369100e30682f14de81fb`, lane tip `cb685273cc9e331b51f45485793d5d1c91184b3a` (registry 162 rows at both).

ROWS:

Insert under a new `### Round 59 gate registry additions` table with the same eight cells as rounds 56-58
(`| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |`). Tallies are
`<N>/<N>` for the L1's final run: all three c59 selftests are version-1 stubs today (measured exit 2 each,
`.files/probe-c59-selftest-stubs.txt`). Row names are unused in the current registry (checked: 159 `| ` rows).

| axis-evidence-counter | gate (offline; calibration: the SCORECARD axis-table evidence cells against committed blobs at the measured revision; base pinned at `fd6303ce`) | `python3 -B .ufo/waves/round-59/c59_axis_evidence.py --root . --revision <rev> [--base <rev>] [--json]` | `0=met` (`mismatches == 0 AND rows == 3` — the rows named operability, freshness, calibration in that order — `AND scores_held == 2 AND superseded_kept == 3`); `1=not met`; `2=could-not-evaluate` (`SCORECARD.md` unreadable at the measured or base revision, `--root` not a repository toplevel, revision or base unresolved, exception); `64=usage` | `python3 -B .ufo/waves/round-59/c59_axis_evidence.py --selftest` (`<N>/<N>` checks; v1 stub until wave 1 writes the fixture kill matrix) | base control `.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` (`mismatches=16`, exit 1); contract `.ufo/waves/round-59/contract.json` `counterSha256v1 95d23511…`; atom rules frozen in the counter docstring | none | kake |
| disclosed-route-resolver-cases-counter | gate (the tool at the revision against gate-built fixture lanes with per-run fixture ids; every fixture repo is `git init` in its own dir; `--root` must be a repository toplevel) | `TMPDIR=<scratch> python3 -B .ufo/waves/round-59/c59_resolver_cases.py --root . --revision <rev> [--work <scratch>] [--seed N]` | `0=met` (`cases_passed == 21 of 21`: K1-K7, P1-P5, P7 as round 58; K8 a multi-line HTML-comment row registers nothing; K9 a setext heading ends `## Registry`; K10 an in-lane symlinked knowledge dir is read; K11 at a revision a committed symlink resolves inside the tree, never parsed as its target string; K12 a registry symlinked out of the lane is unevaluable; K13 a non-UTF-8 knowledge file name at a revision is read, not fatal; K14 a `--root` below the repository toplevel is unevaluable; P6 tool selftest >= 66); `1=not met`; `2=could-not-evaluate` (`--root` not a toplevel, revision unresolved, tool absent at the revision); `64=usage` | `TMPDIR=<scratch> python3 -B .ufo/waves/round-59/c59_resolver_cases.py --selftest` (`<N>/<N>` control tools over the 21 cases; v1 stub until the port) | base control `.ufo/waves/round-59/controls/base-c2-resolver-cases.txt` (`13/21` at seed 59, exit 1: K8-K14 and P6 fail); contract `counterSha256v1 ca2e85c6…`; case list frozen in the counter docstring | none | kake |
| crawler-identity-quote-truth-counter | gate (offline, committed bytes only; no network; quote truth plus the append-only stale-claim correction) | `python3 -B .ufo/waves/round-59/c59_quote_truth.py --root . --revision <commit> [--base <rev>] [--json]` | `0=met` (`conditions_passed == 9 of 9`: C1-C8 as round 58 on S425/S426, C9 the append-only `[r59-correction 2026-10-27]` tail on `corpus/knowledge/crawler-identity.md`); `1=not met`; `2=could-not-evaluate` (`--root` not a toplevel, revision or base unresolved, unreadable retained body or receipt); `64=usage` | `KAKE_R59_SELFTEST_REV=45a92b64ac8a0f82dba369100e30682f14de81fb python3 -B .ufo/waves/round-59/c59_quote_truth.py --selftest` (`<N>/<N>` checks; v1 stub — env name to be fixed by the port, finding 3) | bodies pinned by sha256 (S425 `ff2b9fd7…` 74477 B, S426 `8df9d4ad…` 69789 B, `.ufo/waves/round-59/sources/receipts.json`); mirror pin `.ufo/waves/round-59/assimilation/mirror-pin.json` = 162 rows at `fd6303ce`; base control `controls/base-c3-quote-truth.txt` (`0/9`, exit 1); contract `counterSha256v1 b3aef90c…` | none | kake |

Replacement for the existing `source-id-resolver` row (round-57/58 table; the tool's written paths stay unchanged, the sentence
below is the round-59 behaviour set):

| source-id-resolver | tool (read-only; stdlib python; round 58 fence-aware `## Registry` parse and NUL-split `git ls-tree -z` paths at a revision; round 59: a multi-line HTML comment hides no row, a setext heading ends the Registry section, in-lane symlinked knowledge dirs are read, committed symlinks resolve inside the tree at `--revision`, a registry symlinked outside the lane and a `--root` that is not a repository toplevel are unevaluable, a non-UTF-8 knowledge file name is not fatal; selftest `<N>` checks, P6 floor 66) | `python3 -B scripts/id_resolver.py --root . [--revision REV] [--fleet FLEET]` (lists every `S###` id cited in `corpus/knowledge/**/*.md` that the lane registry lacks and names the sibling registries that hold it) | `0=no dangling id`; `1=dangling ids found` (one `DANGLING` line each, then `ids_cited=N ids_resolved=N dangling=N owned_elsewhere=N unowned=N`); `2=could-not-evaluate` (revision unresolved, registry absent or symlinked out of the lane, `--root` not a repository toplevel, no knowledge file); `64=usage` | `python3 -B scripts/id_resolver.py --selftest` (`<N>/<N>` checks) | red-before: at lane revision `3994101` it reports exactly S367 S372 S373 S390 S409, each held by kotodama-shokunin (`.ufo/waves/round-57/w1/ExecResolverGroundTruth.md`, gate condition G4) | none | kake |

HISTORICAL:

1. `baidu-crawler-identification-quote-truth-counter` (round-58 table) becomes `historical`. Replace its Kind cell with:
   `gate (historical from round 59: green at its round-58 measured revision `8d340c15200959190ba3e894399cdc931976331f`; red on later
   trees by design because C7 pins the round-58 validate scratch and C8 pins the 160-row mirror against the 162-row registry round 58
   landed, and round 59 grows the registry to 164; offline, committed bytes only)`
   Measured: exit 0, `8/8` at `cb68527` (registry still 162, `.files/probe-c58-quote-162rows-cb68527.txt`); exit 1 on a scratch clone
   with two added rows (164), C7 `validated scratch registry is not byte-equal to the landed registry` and C8 `registry rows 164 !=
   mirror rows 160 + 2` (`append-only … != mirror bytes`) — `.files/probe-c58-quote-164rows.txt`. Two independent frozen pins break,
   not C8 alone. Premise correction: **c58's mirror pin is 160 rows** (base `0440485`); the **162-row** pin is round 59's own mirror
   (`.ufo/waves/round-59/assimilation/mirror-pin.json`, base `fd6303ce`). The round-59 run measures against a 164-row registry.
2. `resolver-cases-counter` (c58) stays green, not historical. Measured `14/14 met=True` at `cb68527` and on the 164-row clone, with
   P6 `59/59` and P7 `ids_cited=108 ids_resolved=108 dangling=0` (`.files/probe-c58-resolver-162rows-cb68527.txt`,
   `probe-c58-resolver-164rows.txt`). P6 floor 55 is still satisfied: the round-59 build raises the tool selftest to at least 66
   (round-59 P6 floor 66), and the 14 round-58 cases are a subset of the 21 the C2 claim scores. [INFERENCE] at the round-59 tip,
   which does not exist yet.
3. `receipt-rewrite-counter` (c58) stays green, not historical. Measured `met=True` at `cb68527`: `events=19 undisclosed=0 phantom=0
   malformed=0 wrong_kind=0 unpointed=0 symlinks=0 new_rewritten=0 new_receipts=2` (`.files/probe-c58-receipt-rewrites-cb68527.txt`).
   Later-round receipts enter as first additions, which `events()` skips, so round-59 additions do not trip it; a round-59 receipt
   rewrite would (it would be `undisclosed`). It keeps guarding.
4. No round-57 row changes state this round: `c57_receipt_pins.py` and `c57_quote_truth.py` are already `historical`; `c57_idresolver_gate.py`
   gates a fixed measured revision (`32754df…`) and the round-59 tool change is not at that revision.

CAPABILITY ROW:

Add to the round-59 section, in place of a new-row claim: `No new capability-table row: C2 deepens the round-57 source-id resolver.`
If the table is updated rather than only annotated, the replacement row is:

| Source-id resolver | Lists every `S###` cited in `corpus/knowledge/**/*.md` that the lane registry lacks and names the sibling registries that hold it, at a revision or the working tree — round 59: reads in-lane symlinked knowledge dirs, resolves committed symlinks inside the tree at a revision, refuses a registry symlinked outside the lane and a `--root` that is not a repository toplevel as unevaluable (exit 2), and registers no row hidden by an HTML comment or a section closed by a setext heading; exit 0/1/2/64 | `scripts/id_resolver.py`, `.ufo/waves/round-59/controls/after-c2-resolver-cases.txt`, `.ufo/waves/round-59/c59_resolver_cases.py` | 57 |

`after-c2-resolver-cases.txt` is the planned receipt name (the file does not exist yet; base receipt is `base-c2-resolver-cases.txt`).

GATES (mine, read-only):

| Command | Outcome |
|---|---|
| `c58_quote_truth.py --root lane --revision cb68527` | exit 0, 8/8, registry 162 |
| `c58_quote_truth.py --root lane --revision 5c63e1d` (clone + 2 rows = 164) | exit 1, 6/8, C7+C8 fail |
| `c58_resolver_cases.py --root lane --revision cb68527 --seed 59` | exit 0, 14/14, P6 59/59, P7 108/108 |
| `c58_resolver_cases.py --root lane --revision 5c63e1d --seed 59` | exit 0, 14/14 |
| `c58_receipt_rewrites.py --root lane --revision cb68527` | exit 0, met=True, events=19, new_receipts=2 |
| `c59_axis_evidence.py --selftest` / `c59_resolver_cases.py --selftest` / `c59_quote_truth.py --selftest` | exit 2, version-1 stubs |

TOUCHED SURFACES: this report; `.ufo/waves/round-59/w1/ScribeC2SkillRows.files/` (6 probe logs). Nothing else in the lane; no
fleet-repo write; no lane git/jj state touched (read-only `show`/`log`/`rev-parse` only), no sibling lane read.

FINDINGS:

1. `c59_axis_evidence.py` `PREDICATE` (and `contract.json`) omits `names_ok`, which `measure()` requires: the three rows must be named
   operability, freshness, calibration in that order (`tuple(row_names) == AXES`). The verdict map above states the requirement; the L1
   should either keep my wording or align the frozen predicate string before the final run.
2. C1 cell drafting constraint for the axis table: any `A/B` written in an evidence cell must occur verbatim in one of that cell's
   resolved blob pointers (otherwise `tallies_unfound`); every cited `.ufo/waves/round-<N>/` receipt needs a table row naming that axis
   in SCORECARD's `## Round N` section (otherwise `receipts_off_axis`); and the three base evidence cells must survive verbatim outside
   the axis table (`superseded_kept == 3`), which the base control shows at 0 today.
3. The round-59 quote-truth selftest's revision env name is unpinned in v1 (the c58 port used `KAKE_R58_SELFTEST_REV`); my row assumes
   `KAKE_R59_SELFTEST_REV`. The L1 should correct the cell after `ExecC3SelftestPort` lands.
4. Base-control `/tmp/kake-r59/L1/w/...` paths appear in `controls/base-c2-resolver-cases.txt`; that is a receipt of a run, not a
   pointer in an axis cell, so the C1 tally rule does not read it — but do not cite the base receipt as axis evidence.
5. `c59_resolver_cases.py` returns 2 when the tool is absent at the revision (`measure` early return), so the row's exit-2 cell is
   complete only with that wording; my row has it.

VERDICT: Three c59 gate rows and the resolver row update are drafted; one round-58 row (c58 quote truth) goes historical through two frozen pins, the resolver-cases and receipt-rewrite rows stay green; c59 tallies await the ported selftests.
