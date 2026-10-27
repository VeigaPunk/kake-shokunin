# ExecC1Data52

Claim C1 data — round-52 members: `c52_gate_registry.py`, `c52_mutation_ladder.py`, `c52_quote_truth.py`, `c52_wave_ledger.py`.
Method: `git clone -q --shared /home/vgpnk/Projects/shokunin/kake-shokunin` detached at `97cdc122379711c2b02a8970752c8782da3ac81d`;
the three argparse counters ran `python3 -B <path> --root . --revision <rev>` (counter code read from the checkout — all four files
are byte-unchanged since round 52, `git log --follow` last touch `73c22a3`/`3a50ae4`); the ladder takes no args and resolves the lane
from `__file__`, so it ran in checkouts of each revision. `TMPDIR`=scratch, `GIT_DIR`/`GIT_WORK_TREE` unset, `timeout 1800`. Raw runs:
`.files/{gate_registry,gate_registry_base_full,wave_ledger,quote_truth,summaries,ladder}.txt`, receipt copy `.files/c1-mutation-ladder-run-at-base.json`.

## MEMBERS

Round-52 measured revisions (disagreement inherited, both named): `SCORECARD.md` `### Round 52 — measured claims and receipts`:
"Measured revision `1ae8de5d4dee8300624b0db2a94497ff905942c5`"; `.ufo/reports/round-52/kake.md:5`: "measured revision:
`a4a890cf1381a194891689dcbba0bf524350926b`; tip `a1d83ecf2012f92fd470c5aaacebf2225207b8e9`". The spot-check
(`corpus/lessons/round-52-verifier-spotcheck.md` §1) calls this defect "evidence-pointer consistency"; every per-instrument receipt
names `1ae8de5`. All ancestors of `97cdc122` verified (`merge-base --is-ancestor`).

| Member | Exit@97cdc122 (last summary line) | Exit@measured | Ever green | Honest label |
|---|---|---|---|---|
| `.ufo/waves/round-52/c52_gate_registry.py` | 1 — `C1 registry rows=2 receipts=2 met=False`; fail leg `frozen_baselines: wave-evidence-ledger pinned input LOG.md does not hash to its pin` | 0@1ae8de5, 0@a4a890c | green 1ae8de5, a4a890c, tip a1d83ec; 2 (baselines absent) @73c22a3/5422ff3/3a50ae4/007d66e4 | unregistered row → historical, pin `1ae8de5d4dee8300624b0db2a94497ff905942c5` |
| `.ufo/waves/round-52/c52_mutation_ladder.py` | 0 — `C1 ladder families=18 caught=13/18 pass_agrees=True met=True` | 0@1ae8de5, 0@a4a890c | green at 97cdc122, 1ae8de5, a4a890c, a1d83ec | unregistered row → live |
| `.ufo/waves/round-52/c52_quote_truth.py` | 1 — `C2 quote-truth 6/8 met=False`; fail leg `append-only: measured registry minus the adopted rows != mirror bytes` | 0@1ae8de5 (8/8), 0@a4a890c | green 5422ff3..a1d83ec; 1@007d66e4 | row carries `historical`, pin `1ae8de5…` — confirmed correct |
| `.ufo/waves/round-52/c52_wave_ledger.py` | 0 — `C1 ledger 3/3 met=True` | 0@1ae8de5 (3/3), 0@a4a890c | green at every tried revision from `73c22a3` onward incl. base; 1 only at pre-wave `007d66e4` (settlement receipt absent) | row carries `live` — confirmed correct |


Current SKILL.md state (worktree = base content for these lines): two registered rows (`wave-evidence-ledger`, `quote-truth-counter`,
SKILL.md:1215–1216); `c52_gate_registry.py` named only in prose (line 1218) as "the completeness counter"; `c52_mutation_ladder.py`
named only inside the ledger row's pinned-values cell. So at base the population counter would score `c52_gate_registry` and
`c52_mutation_ladder` `unregistered` — matching the contract's before-line of 12 unregistered members.

## ROWS

`.ufo/waves/round-60/w1/ExecC1Data52.files/rows.md` — 8-cell rows for all four members in the line-1213 table format: the two
existing rows carried verbatim (labels verified by re-run), plus new rows `ledger-mutation-ladder` (live) and
`gate-registry-completeness-counter` (historical, pin `1ae8de5…`). Verdict maps written from the code: gate-registry
`0/1/2` (argparse errors exit 2 — round-52 spot-check routed defect 7 is right that no 64 path exists; corrected phrasing used);
ladder `0/1/2` (1 is also `SystemExit` on missing r51 evidence; extra argv ignored); self-test cells name `KAKE_R52_SELFTEST_REV`
(registry selftest honors it too) / `none (no selftest mode)` for the ladder.

## NOTES

- `c52_gate_registry` is red at base for a real by-design reason: `baselines.json` pins `LOG.md`'s round-52 blob, and later rounds
  append to `LOG.md` → `frozen_baselines` fails. `historical` is the honest label, not `never-met`.
- `c52_mutation_ladder` is green at base but mutates its checkout: it rewrites `control/c1-mutation-ladder.json` (a tracked file) —
  a `git checkout` right after a run fails on the dirty receipt (hit and worked around; the observation rule's per-run fresh clone
  also sidesteps it). Its entry command in the drafted row takes no `<commit>`; as written the gate would run it in the
  measured-revision clone — green.
- Exit-code nuance worth a reviewer's eye: ladder exit 1 conflates "not met" with `SystemExit` aborts (missing evidence files);
  `argparse` usage errors exit 2 in all three argparse counters, not 64.
- `c52_quote_truth` at base fails only the C8 mirror leg (registry is 164 rows vs pinned 148) — consistent with its existing
  `historical` label text; C8 mirror bytes also require 5422ff3+ (green at `5422ff3`, `3a50ae4`).
- No counter file changed after `3a50ae4`; running base-checkout code against earlier `--revision`s is faithful.
- Scratch `/fast/scratch/hyaku/kake-r60/ExecC1Data52` holds the `--shared` clone and raw logs; retained copies under `.files/`.
  No installs (system `git`, `python3` sufficed); `/home/vgpnk/.omp/agent/RULES.md` not needed beyond the standing pacman pause.

VERDICT: 4 of 4 round-52 members measured — registry rows drafted in `.files/rows.md`: wave-ledger live (0@base), mutation-ladder live (0@base), quote-truth historical@1ae8de5 (1@base), gate-registry historical@1ae8de5 (1@base, LOG.md pin); two existing labels confirmed.
