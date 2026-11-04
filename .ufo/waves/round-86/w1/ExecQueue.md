# ExecQueue — kake round 86, w1 (author-side; not independent closure)

Seat scope: draft the two C1 corpus texts, verify R3 preservation files, run the
assigned counter selftest. All production files read-only; L1 alone integrates
after WAVE-DONE. No VCS mutations, no delegation, no installs or upgrades
(pacman paused; none needed), no network. Base `376ac5dcdf86457ef1f8dd490dada735dad81f68`.

## Deliverables (under `.ufo/waves/round-86/w1/ExecQueue/`)

| File | What it is |
|---|---|
| `corpus-README-debt-block.md` | Candidate 11-line `## Open instrument debt (round 86)` block for `corpus/README.md`: names D84-2 and D84-3 retained-open with `flip:` re-open conditions, cites `corpus/lessons/round-85.md` and `corpus/lessons/round-85-verifier-spotcheck.md`; debt record, not repair claim. Satisfies every `c1_item_r4` literal (`D84-2`, `D84-3`, `flip:`, `corpus/lessons/round-85.md`). Placement: append after the round-85 coverage section. |
| `corpus-lessons-round-86.md` | Candidate `corpus/lessons/round-86.md` R1–R4 disposition table: what each item closes, exact evidence paths, `<placeholders>` for values measured at integration. Contains the required `round-85/w1/CriticClaims.md` reference (`c1_item_r3` conjunct) and the records-only-tree disclosure. |
| `receipts/receipt-existence.txt` | ls + wc receipts for both R3 preservation files (below). |
| `receipts/receipt-selftest.txt` | Assigned counter selftest receipt (below). |

## Executed checks (exactly the assigned ones)

1. R3 file existence at the current worktree — both resolve:
   - `.ufo/waves/round-85/w1/CriticClaims.md`: ls exit 0, 11806 bytes, 81 lines, mode 644, mtime Nov 4 11:53.
   - `.ufo/waves/round-85/controls/late-shortcut-c1.txt`: ls exit 0, 298 bytes, 7 lines, mode 644, mtime Nov 4 11:49.
   Receipt: `receipts/receipt-existence.txt`.
2. `TMPDIR=/fast/scratch/hyaku/kake-r86/ExecQueue python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/count.py --selftest`
   → stdout `selftest: 10/10 passed`, exit 0. Receipt: `receipts/receipt-selftest.txt`.
   This proves the C1/C2 fixtures read as declared (green, per-item mutants, junk,
   missing-tree); it is not an after measurement of any claim.

## Corroborating read (not an assigned check, read-only)

`.ufo/l0-questions.md` (fleet root) already carries the `kake | round-86 |` D84-4
routing line at candidate time — noted in the lesson draft's R2 row so L1's
carrier re-check (`c1_item_r2`) is expected to hold; no fleet file was written.

## Limits and handoff

- Author-side seat: the drafts are candidate bytes only; `open=4 → open=0` is
  claimed solely by the counter's committed after receipt at the carrier.
  Records-only textual conjuncts are disclosed as such in the lesson draft.
- Counter, controls and all production files untouched; no `--claim` measurement
  run (not assigned to this seat; L1 owns before/after).
- Byte sizes cited above are worktree observations, not git-object pins; the
  counter re-verifies both R3 files inside the carrier export.
- Scratch `/fast/scratch/hyaku/kake-r86/ExecQueue/` deleted before yielding;
  receipts copied to the deliverable dir first. No `/tmp` evidence used.
