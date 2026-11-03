# ScribeRows — round-74 w1: SKILL.md gate-registry section (draft)

Seat: scribe (read-only). No lane file was edited; this report is the only write.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Base revision measured:
`ced2878a1e77f57afb4ee3baebf1021e5130399b` (`SKILL.md` = 1404 lines).
Contract: `.ufo/waves/round-74/contract.md` §C1 (read first, untouched).
Evidence used: `.ufo/waves/round-74/w1/ExecC1Rows/rows-evidence.json` (present and read; it
appeared at 20:17 after my first probe at 20:15 found the directory empty — no derivation
fallback was needed for the seven population counters). The round-74 counter
`c74_registry_gap.py` has no evidence row and no file at base: its row is derived from
contract §C1 only and is marked as such below.
Scratch: `/fast/scratch/hyaku/kake-r74/ScribeRows` — created `mkdir -p`, nothing written into
it, removed before yield (`rm -rf`, see §Scratch).

## Draft

Land the bytes **inside** the fence, not the fence itself. The table must land as a real
markdown table outside any fenced block: registry readers exclude fenced lines from the
annotation/row locus (the round-70 `## Pointer calibration (round 70)` rule), and the
round-74 counter's own conjunct 1 speaks of a table row, not of a quoted one.

````markdown
### Round 74 gate registry additions

Round 74 registers the seven population counters that the frozen contracts of rounds 69–73 named
but no gate-registry table row carried at base, plus the round's own registry-gap counter. The
population is the eight counters contract §C1 fixes: `c69_recorded_counts.py`,
`c69_tmp_honour.py`, `c70_pointer_audit.py`, `c71_calibration.py`, `c71_tmp.py`,
`c72_tmp_v2.py`, `c73_tmp_v3.py` and `c73_wave_pointers.py` (`population=8`).
`c73_tmp_v3.py` was already registered by the round-73 section above and is not re-rowed here,
so this section adds eight rows: the seven it registers and the row for
`c74_registry_gap.py` itself. At base `ced2878a` the measured gap was `unregistered=7` with the
own-row conjunct absent (`.ufo/waves/round-74/controls/base-c1-registry.txt`). The section is
appended at EOF, after line 1404, which is below line 935 — the largest `.line` pinned for
`SKILL.md` in `corpus/knowledge/freshness-sidecar.json` — so no pinned line moves; a future row
keeps this append-at-EOF discipline or re-pins the sidecar in the same commit. Withdrawal rule:
a row goes when its counter leaves the tree; a superseded row is replaced by a new row that
names its successor and the class, and the old cell is never edited in place.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| c69_recorded_counts.py | gate (offline over committed bytes; calibration: every integer count the round-67 and round-68 records attribute to a named revision either re-derives at that revision or is relabelled by an exact correction row) | `python3 -B .ufo/waves/round-69/c69_recorded_counts.py --root <lane> --revision <rev> --pairs .ufo/waves/round-69/c1/pairs.json` | `0=met` (`unrelabelled=0`; summary `pairs=N mismatches=M relabelled=R unrelabelled=U met=true`); `1=not met`; `2=usage or IO fault` (malformed pairs file, unresolvable revision, `--root` not a directory, `--selftest` without `--work`, bad argv — a fault never prints a verdict) | `python3 -B .ufo/waves/round-69/c69_recorded_counts.py --selftest --work <dir>` → `selftest 6/6`, exit 0 (evidence file leg `selftest`) | predicate frozen `.ufo/waves/round-69/contract.md` section C1 plus Amendment 1; pair set `.ufo/waves/round-69/c1/pairs.json` is frozen input; do-nothing control `.ufo/waves/round-69/controls/c1-base.txt` at `4d188f94` (`pairs=20 mismatches=1 relabelled=0 unrelabelled=1 met=false`, exit 1); after `.ufo/waves/round-69/controls/c1-after-t1.txt` at `c182f579` (`pairs=20 mismatches=1 relabelled=1 unrelabelled=0 met=true`, exit 0); round-74 base `ced2878a` is green on the same pair set (`pairs=20 mismatches=1 relabelled=1 unrelabelled=0 met=true`, exit 0) | read-only; the frozen pair commands are host-absolute (`git -C /home/vgpnk/Projects/shokunin/kake-shokunin show <rev>:<path>`, frozen input) and read committed blobs, and `cwd=<--root>` does not redirect them; fixture trees under `--work` only; no network | kake round 69 (counter by wave-1 seat ExecC1Counter; row by the L1 in round 74) |
| c69_tmp_honour.py | gate (offline; operability: the freshness sweep carries no code-level scratch-root path literal, the sweep's `--selftest` fixture lands under TMPDIR and not under HOME, and the `--offline` exit code plus VERDICT line equal the frozen round-69 baseline) | `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root <lane> --revision <rev> --work <scratch dir> [--baseline <rev>]` | `0=met` (`tmp_literals=0 selftest_under_tmpdir=true offline_unchanged=true`); `1=not met or runtime fault` (a failed `git show`, a missing `node`, or an absent sweep file raises a message and exits 1 — no separate fault code, named limitation); `2=usage` (argparse) | none (no self-test mode; `--selftest` is an argparse error, exit 2 — the counter's own three terms are exercised by the base and after controls, and its nested sweep `--selftest` is not a counter fixture suite) | predicate frozen `.ufo/waves/round-69/contract.md` section C2 plus Amendment 1 (`offline_exit=0` replaced by `offline_unchanged=true` against the frozen baseline); do-nothing control `.ufo/waves/round-69/controls/c2-base.txt` at `4d188f94` (`tmp_literals=2 selftest_under_tmpdir=false offline_unchanged=true`, exit 1); after `.ufo/waves/round-69/controls/c2-after-t1.txt` at `c182f579` (`tmp_literals=0 selftest_under_tmpdir=true offline_unchanged=true`, exit 0); baseline default `4d188f94`; round-74 base `ced2878a` is green (same three `true` values, exit 0) | offline; materialises the revision tree with `git archive` under `--work`; runs `node scripts/freshness-sweep.mjs` in that tree; writes nothing outside `--work` | kake round 69 (counter by wave-1 seat ExecC2Fix; row by the L1 in round 74) |
| c70_pointer_audit.py | gate (offline over committed SCORECARD bytes plus host state; calibration: every path-like SCORECARD evidence pointer resolves at the measured revision or on the host, or is annotated by an exact-token row of `## Pointer calibration (round 70)`; `--base` adds the append-only conjunct) | `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <lane> --revision <rev> [--base <rev>]` | `0=met` (`unannotated=0` and, when `--base` is given, `append_only=true`); `1=not met`; `2=usage or IO fault` | `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --selftest --work <dir>` → `selftest 8/8` only where the scratch root is the system temp root (round-70 receipt). Measured at the round-74 base with `TMPDIR` under the mandated scratch tree: `selftest 4/8`, exit 1 — the tmp fixtures are minted under TMPDIR while the population regex matches only the system temp root. Not a green claim | predicate frozen `.ufo/waves/round-70/contract.md` section C1 plus `amendment-1-note.md` §C1 (extension cap 7→16, normpath resolution, `test -e` semantics, home-escape exclusion, fenced blocks excluded from the annotation locus); do-nothing control `.ufo/waves/round-70/controls/c1-base-v2.txt` (`pointers=348 dangling=17 annotated=0 unannotated=17 met=false`, exit 1); after `.ufo/waves/round-70/controls/c1-tip-final.txt` (`pointers=351 dangling=17 annotated=17 unannotated=0 append_only=true met=true`, exit 0); selftest receipt `.ufo/waves/round-70/controls/selftest-v2.txt` (`selftest 8/8`); round-74 base `ced2878a` with the historical `--base e5f6fd9e` is red (`pointers=362 dangling=17 annotated=17 unannotated=0 append_only=false met=false`, exit 1) — the frozen round-70 append-only baseline no longer holds, so this row is historical, not a continuing live gate | read-only over committed SCORECARD bytes and the host paths its pointers name; fixture repositories under `--work`; no network | kake round 70 (counter by wave-1 seat ExecC1Counter; row by the L1 in round 74) |
| c71_calibration.py | gate (offline over committed SCORECARD bytes; calibration: no active `## Planned` heading names a round below 72, the stated attack share equals the strict count over `.ufo/waves/round-70/w1-results.json`, and the append-only guard holds) | `python3 -B .ufo/waves/round-71/c71_calibration.py --lane <lane> --revision <rev>` | `0=met` (`mismatches=0` and `guard=ok`); `1=not met`; `2=unevaluable` (missing SCORECARD, results file or correction list, or a stated attack-share population other than exactly one); `64=usage` (also what `--help` and `--selftest` return: the module docstring is printed) | none (one-off round counter; no self-test mode — `--selftest` exits 64; predicate frozen in `.ufo/waves/round-71/contract.md` section C1) | base `.ufo/waves/round-71/controls/c1-base.txt` at `cc6b4e0b` (`stale_planned=2 attack_mismatch=1 mismatches=3 met=False`, exit 1); after `.ufo/waves/round-71/controls/c1-after.txt` at `8102bb0b` (`stale_planned=0 attack_mismatch=1 mismatches=1 met=False`, exit 1) — round-71 C1 was adjudicated `unprovable`, not green (`corpus/lessons/round-71-verifier-spotcheck.md`); round-74 base `ced2878a` is unevaluable, exit 2: `C1 unevaluable: stated attack-share population is 2, frozen population is 1`; no successor counter is registered for this class | read-only over committed bytes (`git show`); writes nothing; no network | kake round 71 (counter frozen at `04557e17`; row by the L1 in round 74) |
| c71_tmp.py | gate (offline over committed SKILL.md bytes; freshness: every scratch-root citation is annotated with `not an executable instruction` or replaced by a `mktemp` recipe under the round-71 replacement guard; superseded for this class by `c73_tmp_v3.py`) | `python3 -B .ufo/waves/round-71/c71_tmp.py --lane <lane> --revision <rev>` | `0=met` (`unannotated_tokens=0` and `guard=ok`); `1=not met`; `2=unevaluable` (`git show` failure); `64=usage` (also `--help` and `--selftest`) | none (one-off round counter; no self-test mode — `--selftest` exits 64; predicate frozen in `.ufo/waves/round-71/contract.md` section C2) | base `.ufo/waves/round-71/controls/c2-base.txt` at `cc6b4e0b` (`tokens_total=7 unannotated_tokens=7 met=False`, exit 1); after `.ufo/waves/round-71/controls/c2-after.txt` at `8102bb0b` (`tokens_total=8 unannotated_tokens=0 removed=7 added=7 guard=ok met=True`, exit 0); successor `c73_tmp_v3.py` — the equal-count guard re-reddens on later SKILL.md edits by design, measured at the round-74 base `ced2878a`: `tokens_total=8 unannotated_tokens=0 removed=8 added=16 guard=fail met=False`, exit 1 | read-only over committed SKILL.md bytes (`git show`); writes nothing; no network | kake round 71 (counter frozen at `04557e17`; row by the L1 in round 74) |
| c72_tmp_v2.py | gate (offline over committed SKILL.md bytes; operability: brace-default and command-position citations are findings, prose citations carrying the full phrase are clean, and the guard rejects a token-bearing addition without the phrase; superseded for this class by `c73_tmp_v3.py`, which keeps this file byte-identical as its do-nothing control) | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane <lane> --revision <rev>` | `0=met` (`brace_findings=0 command_findings=0 prose_findings=0`, `findings=[]`, `guard=ok`); `1=not met`; `2=unevaluable` (`git show` failure); `64=usage` | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --selftest` → `C2v2 selftest 11/11`, exit 0 (function-level fixtures; writes nothing) | predicate frozen `.ufo/waves/round-72/contract.md` section C2; selftest receipt `.ufo/waves/round-72/controls/c2-selftest.txt` (`C2v2 selftest 11/11`); J3 control `.ufo/waves/round-72/controls/j3-control.sh` → `c71_exit=0` and `c72_exit=1`; red-before `.ufo/waves/round-72/controls/c2-base-red.txt` at `cc6b4e0b` (exit 1); after `.ufo/waves/round-72/controls/c2-tip-final.txt` at `5013c0ee` (`findings=[] guard=ok met=True`, exit 0); round-74 base `ced2878a` is green (`findings=[] removed=8 added=16 guard=ok met=True`, exit 0) | read-only over committed SKILL.md bytes; `--selftest` writes nothing; no network | kake round 72 (row by the L1 in round 74) |
| c73_wave_pointers.py | gate (offline over committed LOG.md and SCORECARD.md bytes; calibration: every `controls/`, `sources/` and `w1/` token cited by the LOG.md round-72 section and by SCORECARD rows whose first cell is 72 resolves under `.ufo/waves/round-72/`, or is annotated by a tail line naming both the dead token and a resolving corrected path, with the append-only conjunct) | `python3 -B .ufo/waves/round-73/c73_wave_pointers.py --root <lane> --revision <rev>` | `0=met` (`unannotated=0`, `dead>=2`, `append_only=true`); `1=not met`; `2=unevaluable` (unresolvable revision or unreadable file); `64=usage` | `python3 -B .ufo/waves/round-73/c73_wave_pointers.py --selftest [--work <dir>]` → `selftest 6/6`, exit 0 (six fixture repositories; the default scratch root is a `tempfile.mkdtemp` under TMPDIR) | predicate frozen `.ufo/waves/round-73/contract.md` section C1; do-nothing control `.ufo/waves/round-73/controls/c1-base-lane.txt` at `c1f3d8d4` (`pointers=9 dead=2 annotated=0 unannotated=2 met=false`, exit 1); after `.ufo/waves/round-73/controls/c1-tip-lane.txt` at `c2482e5c` (`pointers=9 dead=2 annotated=2 unannotated=0 append_only=true met=true`, exit 0); round-74 base `ced2878a` is green (`pointers=9 dead=2 annotated=2 unannotated=0 append_only=true met=true`, exit 0) | read-only over committed LOG.md and SCORECARD.md bytes; fixture repositories under `--work`; no network | kake round 73 (counter by wave-1 seat ExecPointerCounter; row by the L1 in round 74) |
| c74_registry_gap.py | gate (offline over committed SKILL.md and counter-tree bytes; calibration: each of the eight counters the round-69 to round-73 contracts name has at least one gate-registry table row containing its exact filename, every such row's counter path resolves at the measured revision, and the round-74 section's own row names this counter) | `python3 -B .ufo/waves/round-74/c74_registry_gap.py --root <lane> --revision <rev> [--json]` | `0=met` (`unregistered=0` and `own_row=true` and every population line `file_exit=0`); `1=not met`; `2=unevaluable` (unresolvable revision, unreadable `SKILL.md`, or a missing or renamed population counter file — never silently met); `64=usage` | `python3 -B .ufo/waves/round-74/c74_registry_gap.py --selftest` → five frozen fixtures: f1 an unregistered population counter is red; f2 a row naming a counter in a non-first cell counts; f3 a prose-only mention does not count; f4 a row whose entry-command path does not resolve fails conjunct 2; f5 a missing or renamed counter file is `unevaluable`, never silently met. CLI flags are those frozen in contract §C1; no run exists at this draft | predicate frozen `.ufo/waves/round-74/contract.md` section C1; do-nothing control `.ufo/waves/round-74/controls/base-c1-registry.txt` at `ced2878a` (`population=8`, `c73_tmp_v3.py rows=1`, the seven other counters `rows=0`, `unregistered=7 met=false`, exit 1); the counter file does not exist at that base revision — wave 1 delivers it and the integrator commits it before the after-state measurement, so this row is inert until that commit and its entry-command path resolves only from it | read-only over committed bytes (`git show` and `git cat-file -e`); writes nothing; no network | kake round 74 (counter delivered by wave 1; row by the L1) |

**How to verify.** Run `python3 -B .ufo/waves/round-74/c74_registry_gap.py --root . --revision <rev>`; it must exit 0 with `unregistered=0`, the own-row conjunct satisfied (`own_row=true`), and every population line carrying `file_exit=0`.
Expected after line, not yet observed since no after-state exists at this draft: `unregistered=0 met=true`, exit 0.
Base control: the same command at `ced2878a` reproduces `.ufo/waves/round-74/controls/base-c1-registry.txt` — `c73_tmp_v3.py rows=1`, the other seven `rows=0`, `unregistered=7 met=false`, exit 1.
````

## Checks run

| # | Command (cwd = lane unless stated) | Result |
|---|---|---|
| 1 | `mkdir -p /fast/scratch/hyaku/kake-r74/ScribeRows` | exit 0 |
| 2 | `wc -l SKILL.md` | `1404 SKILL.md` (last line = the round-73 registry row) |
| 3 | `python3 -c` over `corpus/knowledge/freshness-sidecar.json`, `file == "SKILL.md"` entries | 25 entries, largest `.line` = 935 (so an EOF append moves no pinned line) |
| 4 | `python3 -B .ufo/waves/round-71/c71_calibration.py --lane . --revision ced2878a…` | exit 2, stderr `C1 unevaluable: stated attack-share population is 2, frozen population is 1` |
| 5 | `python3 -B .ufo/waves/round-71/c71_tmp.py --lane . --revision ced2878a…` | exit 1, `tokens_total=8 unannotated_tokens=0 unannotated_lines=[] removed=8 added=16 guard=fail met=False` |
| 6 | `grep`/`sed`/`tail` over `SKILL.md`, the five contracts, and the `controls/` receipts of rounds 69–73 | read-only; the values quoted in the draft are the receipts' own lines |
| 7 | Read `.ufo/waves/round-74/w1/ExecC1Rows/rows-evidence.json` (JSON walk) | 7 counter rows with per-leg runs; `revision=ced2878a…`; `cleanup.status=removed` |
| 8 | `find` for `rows-evidence.json` | first probe (20:15) empty; file present at 20:17 under `ExecC1Rows/`; the ticket path resolved |

No production edit, no commit, no jj call, no tool install (nothing to record under the
tooling authorization).

## Findings (verbatim where measurable)

1. **c71_calibration.py is unevaluable at the round-74 base**, exit 2, message
   `C1 unevaluable: stated attack-share population is 2, frozen population is 1` (my run and
   the evidence's `base` leg agree). Round-71 C1 landed `unprovable`
   (`mismatches 3 → 1`, `met=False`, `corpus/lessons/round-71-verifier-spotcheck.md` §Gate).
   The row records the red history and the current exit 2; it does not claim green.
2. **c71_tmp.py is red at the round-74 base** — `guard=fail` with `removed=8 added=16`
   (the equal-count guard cannot survive later SKILL.md additions). Successor named:
   `c73_tmp_v3.py`.
3. **c70_pointer_audit.py's selftest is host-bound**: `selftest 8/8` on the round-70 host
   (receipt), `selftest 4/8` at the round-74 base with `TMPDIR` under `/fast/scratch/...`,
   because `fresh_tmp_token` mints under TMPDIR while the tmp population regex matches only the
   system temp root. Also red at base with its historical `--base e5f6fd9e`
   (`append_only=false met=false` despite `unannotated=0`). The row marks it historical rather
   than live green.
4. **c69_tmp_honour.py has no self-test mode either** (the ticket named only the two c71
   counters): `--selftest` is an argparse error, exit 2. Its runtime faults also exit 1, not a
   separate code — recorded as a named limitation, not smoothed over.
5. **c71_calibration.py and c71_tmp.py have no self-test mode**: `--selftest` (and `--help`)
   print the module docstring and exit 64. Recorded as `none (one-off round counter; predicate
   frozen in …)`, as the ticket required.
6. **Green at the round-74 base**: `c69_recorded_counts.py` (exit 0, `met=true`),
   `c69_tmp_honour.py` (exit 0), `c72_tmp_v2.py` (exit 0, `met=True`, `findings=[]`),
   `c73_wave_pointers.py` (exit 0, `met=true`).
7. **c74_registry_gap.py does not exist at base** (checked: absent). Its row's entry-command
   path resolves only after the integrator commits the delivered counter; that is exactly the
   C1 conjunct-2 behaviour, and the row says so rather than pretending the file exists.
8. **The draft's table must land unfenced**; only this report fences it. A fenced landing would
   hide the rows from the annotation/row locus readers (the round-70 fenced-line rule).
9. The round-74 counter's summary field `own_row` is quoted from contract §C1; the base receipt
   does not print it (`unregistered=7 met=false` only). The "how to verify" block therefore names
   the conjunct, not an observed token string.
10. **c69_recorded_counts.py's pair commands are host-absolute**: each frozen row is
    `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show <rev>:<path> | grep …`, so `--root`
    does not redirect them and a lane moved off that path turns every pair into an error (exit 2,
    not a silent pass). Recorded in the row's write-scope cell.

## Landing notes for the L1

- Append after the current last line (1404) with one blank line before the heading; do not touch
  lines ≤ 935 (sidecar pins) and do not re-edit the round-73 row.
- Before the after-state run, confirm the delivered `c74_registry_gap.py` accepts exactly
  `--root`, `--revision`, `--json`, `--selftest`; if the delivered CLI adds a scratch flag, extend
  the row's Self-test cell only (the predicate itself is frozen).
- Re-run conjunct 2 yourself: every entry-command path in these eight rows must resolve at the
  measured revision (`git cat-file -e <rev>:<path>`); all seven historical counters already
  resolve at `ced2878a`. Successor and control mentions are bare filenames or existing
  `controls/…` paths, never a second entry command — if the delivered counter extracts more than
  the entry-command path per row, confirm it skips a bare filename such as `c73_tmp_v3.py` when
  that name appears in a successor sentence.
- No cell contains a literal `|`; the row cells were machine-checked (8 cells per row, 9 pipes).

## Scratch

`/fast/scratch/hyaku/kake-r74/ScribeRows` was created at 20:15, held nothing (no fixture, no
clone — every measurement was read-only against the lane), and was removed before yield:
`rm -rf -- /fast/scratch/hyaku/kake-r74/ScribeRows` exit 0, `test -e` exit 1 (absent). No tree
of this seat remains under `/fast/scratch/hyaku/kake-r74/`. If a later reader finds it on disk,
that is this seat's defect.
