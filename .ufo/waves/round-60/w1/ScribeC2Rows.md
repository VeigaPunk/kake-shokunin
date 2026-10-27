# ScribeC2Rows

Drafting only. No `SKILL.md`, `SCORECARD.md`, counter or tool edit; no lane git/jj mutation; no receipt written. Lane tip read:
`b3b9e29ceb388ab1795c0c399703df5172b298ce` (round-60 contract commit); base `97cdc122379711c2b02a8970752c8782da3ac81d`. Only these two
paths were written: `.ufo/waves/round-60/w1/ScribeC2Rows.files/rows.md` (55 lines, 12,627 B) and this report. Scratch dir
`/fast/scratch/hyaku/kake-r60/ScribeC2Rows` created, used as cwd only, deleted (no clone, no fixture, no commit anywhere).

Inputs read (read-only): `.ufo/waves/round-60/contract.md`, `contract.json`, `sources/receipts.json`,
`assimilation/mirror-pin.json`, `controls/census-before.txt`, `assimilation/guard-proof.txt`, `w1-spec.json`; lane `SKILL.md`
lines 1276, 1293, 1307, 1309 (tool-row and gate-row cell style), `SCORECARD.md` lines 191-204, `corpus/knowledge/googlebot-verification.md`
lines 30-40; `.ufo/waves/round-59/w1/ScribeC2SkillRows.md` as the drafting precedent. Row names checked unused in `SKILL.md`:
`append-guard`, `gate-status-counter`, `guard-cases-counter`, `user-triggered-quote-truth-counter` → 0 occurrences each.

ROWS:

Four complete 8-cell rows (`Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope |
Owner`) plus the table header and a suggested `### Round 60 gate registry additions` paragraph, in
`.ufo/waves/round-60/w1/ScribeC2Rows.files/rows.md` `# Rows`. Structural check run on the file: 4 rows × 8 cells, 0 empty cells,
`0=`, `1=`, `2=`, `64=` present in every Verdict-map cell, no `|` inside any cell, `Kind` cells contain neither `historical` nor
`never met` (so the C1 counter labels all four `live`).

1. `append-guard` — `tool (read-only; stdlib python; committed bytes only …)`; entry
   `python3 -B scripts/append_guard.py --root . --base <rev> --revision <rev> [--scope <glob> ...] [--json]`; `0=clean` /
   `1=findings` (`deleted`, `changed`, `untagged_insertion` + `files=<n> findings=<k>`) / `2` (revision unresolved, base not an
   ancestor, root not a toplevel) / `64`; self-test `--selftest` with `<N>` checks and no receipt (a tool row: the gate is row 3);
   proof cell carries the red-before (no tool at base, contract's `0/24` control) and R1 base `fd6303ce…`.
2. `gate-status-counter` — `gate (offline; calibration …)`; entry
   `python3 -B .ufo/waves/round-60/c60_gate_status.py --root . --revision <rev> [--work <scratch>] [--jobs N] [--json]`;
   `0=met` (`members == 28 AND mismatches == 0 AND scores_held == 3`, scores 10/10/2) / `1` (ten named mismatch classes) / `2` / `64`;
   self-test `<N>` checks, planned receipt `controls/c1-selftest.txt`; proof cell carries the frozen population regex, the 28-member
   per-round split (c48 ×2 … c59 ×3, c53 ×1 under `exec-quality-gate/`), the contract's before-state triples and a planned
   `controls/base-c1-gate-status.txt` (≥13 mismatches, exit 1).
3. `guard-cases-counter` — `gate (the tool as committed at the measured revision against gate-built fixture repositories … one
   git init per case, ids/names/line contents from --seed, `git show <rev>:scripts/append_guard.py`, missing tool fails every case)`;
   entry `python3 -B .ufo/waves/round-60/c60_guard_cases.py --root . --revision <rev> [--work <scratch>] [--seed N]`;
   `0=met` (`cases_passed == 24 of 24`, K1–K22 + R1/R2 summarised by class) / `1` / `2` / `64`; self-test `<N>` scored controls,
   planned `controls/c2-selftest.txt`; proof cell carries the five declared controls (no tool `0/24`, always-0, always-1, c55
   byte-prefix port must fail K2/K15/R1, reference `24/24`) and planned `controls/base-c2-guard-cases.txt` (`0/24`, exit 1).
4. `user-triggered-quote-truth-counter` — `gate (offline, committed bytes only; no network; quote truth on S427–S429 and the two
   entries plus the append-only [r60-correction 2026-10-27] correction …)`; entry
   `python3 -B .ufo/waves/round-60/c60_quote_truth.py --root . --revision <rev> [--json]`; `0=met` (`conditions_passed == 9 of 9`,
   C1–C9 named) / `1` / `2` / `64`; self-test `KAKE_R60_SELFTEST_ROOT=<lane> TMPDIR=<scratch> … --selftest`, `<N>` checks, planned
   `controls/c3-selftest.txt`; proof cell pins S427 `d70ce6f5…` 74477 B, S428 `0f296b86…` 76197 B, S429 `423d99c5…` 178797 B, the
   mirror pin `bc054d10…` = 164 rows / 152817 B at `97cdc122`, and planned `controls/base-c3-quote-truth.txt` (`0/9`, exit 1).

Digest cross-check (script, one pass): the three sha256 prefixes and byte counts in the draft equal `sources/receipts.json`;
`bc054d10…`, `164`, `152817` equal `assimilation/mirror-pin.json`. No digest was typed by hand.

CAPABILITY ROW:

One 4-cell row for `SCORECARD.md` `## Capabilities`, in the style of lines 191-204 (capability · what it can now do with its exits and
its stated non-claims · evidence pointer · first-working round `60`). It describes the guard as accepting an end-of-file append and a
visible `[rNN-correction YYYY-MM-DD]` mid-file run, catching changed/reordered/deleted lines and symlinked-away paths, and claiming
nothing about whether a tagged run is faithful. Evidence cell names `scripts/append_guard.py`, the planned
`controls/after-c2-guard-cases.txt` at `<P>/24` against `controls/base-c2-guard-cases.txt` `0/24`, and the tool selftest `<N>/<N>`.
The draft states the entry condition explicitly: `AXES.md` §Capabilities admits a row only from a round that demonstrates the capability
running, and wave 1 scores no after-state, so the row enters only if the L1's frozen run yields that receipt.

OPEN NUMBERS:

- Five placeholders, all for the L1: append-guard selftest `<N>`, `c60_gate_status.py` selftest `<N>`, `c60_guard_cases.py` control
  count `<N>`, `c60_quote_truth.py` check count `<N>`, capability row `<P>/24`. No counter, tool or receipt existed when this draft was
  written (`controls/` held only `census-before.txt`/`.exit`), so nothing was measured and no tally is estimated.
- All seven receipt names are planned, not observed: `c1-selftest.txt`, `c2-selftest.txt`, `c3-selftest.txt`, `base-c1-gate-status.txt`,
  `base-c2-guard-cases.txt`, `base-c3-quote-truth.txt`, `after-c2-guard-cases.txt`. Naming follows the round-59 convention (version-1
  receipt unsuffixed, `-v2` only from version 2). `controls/validate-append.txt` is fixed by contract C3 condition C7 and is cited as such.
- The C1 before-state triples (12 unregistered with its per-round split, `c53_gate_truth.py` live/exit 1, `c57_idresolver_gate.py`
  live/exit 2 without `--fleet`) are quoted as the contract's declaration; the base receipt must re-derive them before that cell is read
  as measured. Same for the C2 `0/24` base control and the five selftest controls.
- Exit-2 sets are partly [INFERENCE]: contract C1 names revision unresolved / `SKILL.md` or `SCORECARD.md` unreadable / clone failure;
  contract C2 names no unevaluable set for the counter at all (only for the tool); both counters' wave-1 seat specs require `--root` to
  be a repository toplevel, so the rows list it, and `guard-cases-counter` also lists an unusable work directory. Each exit-2 cell must be
  reconciled with the built counter, and a condition the tool does not implement must be removed from the cell.
- `Kind` cells avoid `historical` and `never met` deliberately (C1 derives the label from that cell alone); all four rows therefore
  oblige the L1 to a live exit 0 at the measured revision — an obligation the draft creates, not a result this seat observed.
- S427's `Last updated` date is deliberately absent: this seat did not read `sources/S427.html`. Only `receipts.json` values are cited.
- Single-row alternative recorded: if the L1 wants one row per claim surface, drop `append-guard` and keep `guard-cases-counter`, which
  already names the tool in its Kind and Self-test cells.
- Out of scope, untouched: the four counters and the tool themselves, all receipts, `SKILL.md`/`SCORECARD.md` bytes, `corpus/**`, the
  lane index and jj state, sibling lanes, the fleet repo.

VERDICT: Four complete 8-cell registry rows and one capability row drafted from the contract's own commands, exit maps and case lists, all tallies and receipt names left as `<N>`/planned markers for the L1; no measurement, no repository edit.
