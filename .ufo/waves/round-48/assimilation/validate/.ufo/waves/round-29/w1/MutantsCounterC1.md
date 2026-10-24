# Round 29 wave 1 — MutantsCounterC1: mutation probe of the C1 quote-truth counter

Seat: MutantsCounterC1 (leaf, mutation tester). Axis judged: freshness. Milestone: r29-build.
Target under test: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-29/c1_quote_truth.py`
(sha256 `1b8225b570cb458e2ab765d49902651365105899b64327c8a562d0b98abc20d9`; read only, never edited).
## What I attacked

I did not edit the counter. I attacked the invariant it claims to enforce by feeding it one
single-fault corpus state at a time in a sandbox clone. Faults are changes to the corpus state the
counter reads (registry row, entry body, Gate line, retained text, receipts). Each fault is applied
alone, then the bytes are restored. Detector: the counter's exit code plus its per-id report line for
the target id S040. A fault is **killed** when the counter exits non-zero and reports S040
`passed: false`; **survived** when the counter still exits 0 with S040 `passed: true`.
## Sandbox and commands (exit codes)

- Clone `/fast/scratch/hyaku/kake-r29/w1/MutantsCounterC1/clone` (from the lane at `e58b66c`);
  driver `probe.py`; baseline fixture `fixture/`; machine output `results.json`, all under
  `/fast/scratch/hyaku/kake-r29/w1/MutantsCounterC1/`.
- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r29/w1/MutantsCounterC1/clone` — exit 0.
- `TMPDIR=/fast/scratch/hyaku/kake-r29/w1/MutantsCounterC1/tmp python3 -B probe.py` — exit 0. Inside,
  per state: `python3 -B <clone>/.ufo/waves/round-29/c1_quote_truth.py --root <clone> --revision <commit>`.
- Pristine lane readings (read only) in `/home/vgpnk/Projects/shokunin/kake-shokunin`:
  `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision <rev>` — `fe1805c` exit 1
  (`C1 0/4`), `e58b66c` exit 1 (`C1 0/4`), `9e541a1` exit 1 (`C1 0/4`): the lane still has no entry,
  no lesson and no S040–S043 rows, so the declared before-state is reproduced at 0/4 on real lane bytes.
- No lane file was written except this report. `git status --porcelain` shows only the pre-existing
  untracked `.ufo/waves/round-29/*` wave files; no tracked lane file, index or jj state was touched and
  no git/jj write command was run against the lane.
## Baseline (pristine, passing)

Fixture commit `c9db4e37cd06f89e3810d653af0e7c83a6ba28b7`: rows S040–S043 in `corpus/SOURCES.md`
(status `mined`, opened `2026-10-22`, receipt url in the source cell), `corpus/knowledge/pages-base-path.md`
citing each id after its first 8 lines, `corpus/lessons/round-29.md` with a `## Gate` section holding one
`- <id> — ` line and one curly quote each, and the retained `S04x.txt` plus `receipts.json` taken
unchanged from `e58b66c`. Counter: exit 0, `C1 4/4 at c9db4e37`, `controlBroken: false`, all four ids
`passed: true`. Baseline sha256: `corpus/SOURCES.md` `2f5e6ac187122c866dec6b3a35af74728201d09a86e0fe0ef429239d93f0ebc7`,
`corpus/knowledge/pages-base-path.md` `4671fd8ebca26354b937308a2036ed67673e8c2ec9995e17f695c5b7dc5ffa92`,
`corpus/lessons/round-29.md` `5682a70fdaeac7128578ed263edf3b9409e958ae63e5e73e38d34878436771fd`,
`receipts.json` `970aae1f5baee9859904f5472e55ce617572d1bf1fbf2a8007f8643ea44d1327`,
`S040.txt` `625f2b0783a129d2492669d1761329b6b3a5262455aa314dc6900b9143d56eab`.

## Mutant table (assigned faults, target S040)

| fault | counter exit | `C1 n/4` | failing check | verdict |
|---|---|---|---|---|
| registry status `queued` | 1 | 3/4 | `a_row` | killed |
| opened date `2026-10-21` | 1 | 3/4 | `a_row` | killed |
| id cited only in the entry header | 1 | 3/4 | `b_entry_body_cites` | killed |
| Gate quote of 26 words | 1 | 3/4 | `c_gate_quote` | killed |
| Gate quote altered by one letter | 1 | 3/4 | `d_quote_in_retained_text` | killed |
| receipts `textSha256` does not match the retained text | 1 | 3/4 | `d_quote_in_retained_text` | killed |
| two curly quotes on the Gate line | 1 | 3/4 | `c_gate_quote` | killed |
| Gate line moved outside `## Gate` | 1 | 3/4 | `c_gate_quote` | killed |

All eight assigned faults are detected, and `controlBroken` stayed false in every run, so each was
caught by the substantive check rather than by the letter-flip control. The 26-word quote was an exact
substring of the retained text, so that fault was caught by the word rule alone.
## Extended probes (beyond the assignment) — two survivors, both coverage findings

Advisory for the L1. These are not contract changes; I did not modify the counter.

1. **The registry url check is a substring test** (counter line 101, `url in cells[1]`). Changing the
   S040 source cell to cite `.../about-github-pages-2026` instead of `.../about-github-pages` leaves
   the receipt url as a prefix substring, so the counter still exits 0 (`C1 4/4`, S040 `passed: true`).
   Mutant commit `3312e3cd6032db128cb92c678bacfc501b695729`; `corpus/SOURCES.md` sha256
   `9a38f9a863de6788fc3a4d0f30ee1c0e1dfbecb1e3e488d14a2354398b7fbc31`. The counter cannot tell
   "the receipt page was cited" from "a URL that starts with the receipt page was cited".
2. **Retained text and receipts are self-attesting** (counter lines 109–111). Doctoring one word of the
   retained `S040.txt` (`and` → `plus`, word 301 of 528), pointing the Gate quote at the doctored
   sentence and updating `receipts.json` `textSha256` to the new digest leaves the counter at exit 0
   (`C1 4/4`, S040 `passed: true`). Mutant commit `64348fad9b74a0b598c4f52c0b35bf31ca5fd820`;
   `S040.txt` sha256 `f9564992cd05cb2d118914f275dec3adc0461afadec4fd6334d403c79292f5e0`,
   `receipts.json` sha256 `a84d139947a992e10d8506a3e3189274905dbf21b21562cacfd1c588f710e7e3`,
   `corpus/lessons/round-29.md` sha256 `e1465144d105d81052cdfd8e6bf3c99781bc4d8de1afa9de7f3ff1c94574b9fd`.
   Nothing in the committed bytes binds the retained visible text to the page that was fetched, so a
   coordinated edit of text plus receipt is invisible to the counter.

Both survivors describe gaps in the freshness evidence chain, not in the assigned fault list; the review seat KakeR29.CriticC1CounterGameable reproduced both independently (states F10 and F4) and owns neither fix.
## Restoration evidence

After the last mutant the clone was reset to the baseline commit; the working-tree sha256 of
`corpus/SOURCES.md`, `corpus/knowledge/pages-base-path.md`, `corpus/lessons/round-29.md`,
`receipts.json` and `S040.txt` matched the baseline digests exactly (`hashes_match_baseline: true`)
and the counter again printed `C1 4/4 at c9db4e37` with exit 0. The lane itself was never modified.
## What I did not verify

- I did not check the quotes against the live pages; the probe tests the counter against its own
  committed bytes only.
- I did not probe behaviour when the entry, lesson, receipts or retained text are absent at the
  revision, beyond the 0/4 lane readings above, and I did not apply faults to S041–S043 (the counter
  code path is per-id and identical).
- No package was installed or upgraded, so there is no tooling record for this seat.
## Evidence pointers

- Counter source: `.ufo/waves/round-29/c1_quote_truth.py:91` (entry body slice), `:100-101` (registry
  row), `:102` (entry cite), `:103-106` (Gate quote), `:109-111` (receipts sha, quote in text),
  `:113-114` (letter-flip control).
- Machine-readable results `/fast/scratch/hyaku/kake-r29/w1/MutantsCounterC1/results.json`; probe
  driver `probe.py`; baseline fixture commit `c9db4e37cd06f89e3810d653af0e7c83a6ba28b7` in the clone.
