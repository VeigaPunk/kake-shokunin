# ExecC1Tool

Claim C1, primary implementation. Implemented `scripts/receipt_lineage.py` (new, 1038 lines, stdlib
only, read-only) exactly to contract § Claim C1. Access date 2026-10-27 (UTC). No tool installed or
upgraded this seat (nothing was needed; the host git is 2.56.0).

## Files changed

- `scripts/receipt_lineage.py` — the tool (new file; nothing else in the lane mutated).
- `.ufo/waves/round-61/w1/ExecC1Tool.md` — this report.
- `.ufo/waves/round-61/w1/ExecC1Tool.files/` — retained evidence: `base-run.txt`,
  `base-run-disclosed.txt`, `base-run.json`, `head-run.txt`, `selftest.txt`,
  `population-rule.txt`, `disclosures-used-in-evidence.json`.

No git/jj mutation, no commit, no index touch, no sibling-lane or fleet-repo write.

## DESIGN: rule to code map

CLI (`build_parser` L1004, `main` L1016): `--root --revision [--disclosures] [--json] [--selftest]`;
`--selftest` rejects any other argument (exit 64, `Parser.error` L997). Exit codes L92–97:
0 clean / 1 findings / 2 could-not-evaluate / 64 usage. Module is 1040 lines.

| Contract rule | Code |
|---|---|
| read-only; committed bytes only via git plumbing, never the worktree | every read is `git ls-tree -r -z --full-tree` (L179), `git log --raw` (L238), `git cat-file --batch` (L267); the worktree is never opened except the disclosures fallback |
| inherited `GIT_*` scrubbed | `git_env` L123 drops every `GIT_*` key for every git subprocess, adds `GIT_OPTIONAL_LOCKS=0`, `GIT_TERMINAL_PROMPT=0` |
| `--root` must be a repository toplevel | `toplevel` L138 + `evaluate` L437–443: not a directory / not a repo / toplevel != realpath(root) → exit 2 |
| revision resolved to a commit | `resolve_commit` L151: rejects a leading `-`, `rev-parse --verify --quiet --end-of-options REV^{commit}`, 40/64 hex required, else exit 2 |
| population path rule (`.ufo/waves/round-<N>/` + a `control`/`controls` segment, any depth, `.txt`/`.json`) | `is_population_path` L169 + `population` L179; non-blob paths (symlink/submodule) skipped with a named stderr note (L197–200) |
| receipt grammar `(?im)^\s*#\s*receipt\s*:` OR `EXIT=` OR `^VERDICT:` | `RECEIPT_GRAMMAR_RE` L103, used verbatim; applied to the FIRST committed version only (`evaluate` L458) |
| history walk: first-parent commits after the add, child blob != first parent's blob; merges diffed on the first parent; renames not followed | `walk_changes` L238: `git log --first-parent --reverse --format=C:%H --raw --no-abbrev --no-renames --diff-merges=first-parent`; `unquote_path` L205 decodes C-quoted raw paths |
| delete ends a history segment, re-add starts its own (rename ends the path's history) | `segments_of` L313 (A/C/R start, D ends, M continues) |
| result span = set of lines matching the frozen span regex | `RESULT_SPAN_RE` L104 verbatim, `result_span` L295 returns a `frozenset` of whole lines |
| `rewrite` = candidate whose child span set differs from the parent's | `path_events` L411: compare within the segment, parent = previous version of the same segment |
| `pending_filled` = first version carries a pending marker, a later version does not | `has_pending_marker` L299 + `path_events` L411; fires at the first later version without the marker, once |
| one kind per (path, commit); pending_filled wins | `path_events`: `pending_filled` branch precedes the span-diff branch |
| disclosure = entry with equal path and commit; phantom for a non-event entry; malformed JSON → exit 2 | `parse_disclosures` L344, `load_disclosures` L378, `commit_matches` L403, `evaluate` L463–493 |
| one finding per line `<kind> <path> <commit>` then `receipts=<n> events=<k> undisclosed=<m> met=<bool>` | `render` L504; `evaluate` builds exactly that summary (L485) |
| `met` = undisclosed == 0; exit 0 iff no finding | `evaluate` L483–485, `main` L1036 |

Deliberate readings, each noted in the module docstring (L64–78) and reported to the C1 disclosure
seat before it froze the registry. Readings 1–3 were confirmed by the L1 as the contract's intended
semantics (Amendment A1, 2026-10-27):

1. `EXIT=` is **unanchored**, exactly as frozen, so `.ufo/waves/round-52/control/c1-mutation-ladder.json`
   (JSON values `"EXIT=1"`) is a receipt. An anchored grammar drops 5 population files and 3 events.
2. Result span compared as a **set of whole lines** (unordered, de-duplicated): the r52 `revision:`
   relabels fire; a pure reordering of identical result lines is not an event.
3. The pending marker is tested over the **whole first-version text** (and, symmetrically, the whole
   later version), not only its result span, because the motivating r57 receipt at `31b61a4` opens
   with a bare `pending` line that no span alternative matches. The `# receipt: <name>` line is
   excluded from the marker test so a file named `pending.txt` cannot stay pending forever. This is a
   strict superset of the frozen span test; it changes only the `kind` of one event, never disclosure
   matching (`kind` is not consulted).
4. Disclosures path resolution is committed-first for a repo-relative path (`<rev>:<path>`), then the
   filesystem; an absent **default** path means "no disclosures", an absent **explicitly named** path
   is exit 2.
5. `met` carries the frozen `undisclosed == 0` predicate, so `phantom_disclosure` alone gives
   met=True with exit 1 (a finding, not an undisclosed event).
6. `--json` prints one document whose `summary` member is byte-equal to the plain summary line, so
   either reader finds the frozen shape.

## MEASURED AT BASE (evidence in `.files/`)

- Population rule reproduces the frozen list exactly: 144 derived, `diff` IDENTICAL to
  `controls/population-144.txt` (`population-rule.txt`).
- `--revision 9f07731a... --disclosures .files/disclosures-empty.json` →
  `receipts=95 events=12 undisclosed=12 met=False`, exit 1 (`base-run.txt`, `base-run.json`); 95
  because 49 of the 144 population files carry no receipt-grammar line in their first committed
  version (the round-37/40/48 JSON fixtures etc. are non-receipts by the frozen rule and are never
  findings). The empty registry is pinned in `.files/` so this run is reproducible even though the
  live default path now holds the disclosure registry.
- With the 12 disclosure entries (`.files/disclosures-used-in-evidence.json`, path+commit) the same
  run reads `receipts=95 events=12 undisclosed=0 met=True`, exit 0 (`base-run-disclosed.txt`);
  abbreviated (>=7 hex) commits also match; an entry naming no event yields `phantom_disclosure` and
  exit 1.
- At lane HEAD (registry present) → `receipts=95 events=12 undisclosed=0 met=True`, exit 0
  (`head-run.txt`).
- Runtime 0.09 s over the 371-commit first-parent chain; 1 merge commit is walked on the first parent.
- Identity of the 12 events at base: r52 `c1-ledger-real.txt` and `c2-quote-real.txt` at `a4a890cf`;
  r52 `c1-mutation-ladder.json` at `1ae8de5d`, `a4a890cf`, `fd91527a`; r54 `c1-selftest.txt` at
  `8e408e00`, `a631cc02`; r55 `after-c1-readme-index.txt` and `after-c2-quote-truth.txt` at
  `955e3d7b`; r56 `after-c1-selftally.txt` and `after-c2-quote-truth.txt` at `ad06cb8a`; r57
  `after-c1-receipt-pins.txt` at `20217f23` (kind `pending_filled`). This is the same 12 the
  disclosure seat extracted independently; kinds agree except r57, which its table called a fill.

## SELFTEST: 68 checks passed, 0 failed

`TMPDIR=<seat scratch> python3 -B scripts/receipt_lineage.py --selftest` →
`PASS 68/68`, `receipt_lineage selftest: 68 checks passed`, exit 0 (`selftest.txt`). Fixtures are
`git init` repos under TMPDIR, each asserted to be its own toplevel before the first commit; commits
use `-c user.name=selftest -c user.email=selftest@local`; the fixture tree is deleted at the end.

Cases (fixture id → what is proven): L1 clean receipt → 0; L2 undisclosed revision relabel → 1
`undisclosed_rewrite`, exit 1; L3 disclosed via explicit registry → 0; L3b disclosed via the default
path read as the committed blob → 0; L4 non-result body-line rewrite → 0; L5 non-receipt population
file rewritten → 0, `receipts=0`; L6 `met=False`→`met=True` flip → 1 rewrite; L7 bare-`pending`
first version filled → 1 `undisclosed_pending_filled`; L8 same fill disclosed → 0; L9 two rewrites,
one disclosed → exactly 1 finding; L10 pure reordering of result lines → 0 (set semantics); L11 four
malformed-registry shapes (truncated JSON, entries not a list, entry without commit, wrong schema) →
exit 2 each; L12 phantom entry → 1 `phantom_disclosure`, met=True, exit 1; L13 rewrite after the
measured revision → 0; L14 unresolved and dash-leading revisions → exit 2; L15 empty population →
`receipts=0`, exit 0; L16 nested `--root` and non-repository `--root` → exit 2; L17 five usage shapes
(no args, root only, revision only, unknown option, `--selftest` plus args) → exit 64; L18 poisoned
`GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_OBJECT_DIRECTORY`/`GIT_CEILING_DIRECTORIES` → same
finding as the clean run; L19 rename ends the path's history → 0; L20 delete+re-add starts a new
segment → 0; L21 merge commit whose first-parent diff changes the receipt → 1 finding at the merge
commit; L22 symlink population path skipped with a `non-blob` note → `receipts=0`, exit 0; L23
`--json` parses and its `summary`/`findings`/`met`/exit agree with the plain run; L24 the three
grammar alternatives (`EXIT=` alone, `VERDICT:` alone, spaced `# receipt :`) → `receipts=3`; L25 a
body-line pending marker still pending → rewrite, marker cleared → fill; L26 grammar appearing only
later than the first version → not a receipt.

These are device-level self-tests of the tool. The frozen counter (`c61_lineage_cases.py`, cases
L1–L16 + R1/R2) is another seat's deliverable and was **not** run here; no after-state is scored.

## LIMITS

- Truthfulness of a disclosure entry's `note`/`disclosed-by` prose is not checked (contract scopes it
  to the reviewer). `kind` in an entry is parsed but never consulted for matching.
- The result-span set comparison is order-insensitive: a commit that only reorders identical result
  lines is not an event. No lane round is known to have done this (`[INFERENCE]`: unmeasured across
  the full history).
- Depth: `git log --raw` over the 371 first-parent commits at base is fast; a very long history would
  grow linearly (single `git log` + single `git cat-file --batch`, no per-commit subprocess).
- The pending marker is whole-version, so a later version that keeps the word `pending` in prose
  (`no pending rewrites`) delays the fill kind; the change is still caught as `rewrite`.
- The registry is read committed-first but falls back to the worktree; an uncommitted registry can
  therefore disclose a commit at a revision where the committed registry does not exist yet.
- Exit 2 folds every could-not-evaluate cause into one stderr line (revision unresolved, root not a
  toplevel, malformed or missing explicit registry, git plumbing failure).

## Risks / blockers for the L1

- **Contract R2's literal `receipts=144` was unreachable** (`receipts` is the grammar-matched count:
  95 at base; 144 is the population size; 49 population files carry no receipt grammar). Raised to
  the L1 before the counter froze; **Amendment A1 now fixes R2's expected stdout as `receipts=95
  events=12 undisclosed=0 met=True` exit 0 at the measured revision, `undisclosed=12` exit 1 at base**
  — which is exactly what this tool prints, so the blocker is closed. Not silently matched to 144.
- R2's `undisclosed=0` depends on the disclosure registry existing at the measured revision (the 12
  entries listed above). Measured true with the seat's 12-entry registry, exit 0.
- `--json` shape is not frozen by the contract; it emits `version/root/revision/population/receipts/
  events/undisclosed/met/findings/finding_lines/summary/skipped` and repeats the frozen summary
  string in `summary` plus the plain finding lines in `finding_lines`. A counter that greps either
  form works.

VERDICT: `scripts/receipt_lineage.py` implemented to the frozen C1 rules; 68/68 selftest checks pass; `receipts=95 events=12 undisclosed=12 met=False` exit 1 at base and `receipts=95 events=12 undisclosed=0 met=True` exit 0 with the 12-entry registry — exactly Amendment A1's R2 expectation, so the claim's instrument is ready for the counter to score.
