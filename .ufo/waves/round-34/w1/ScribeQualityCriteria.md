# ScribeQualityCriteria — draft of QUALITY.md "Round-34 criteria"

From round-33 spot-check routed items 2, 3, 4 (`corpus/lessons/round-33-verifier-spotcheck.md:192-201`), shape from "Round-33 criteria" (`corpus/QUALITY.md:569-604`). Read at `a2fe31b2`, declaration `d08d8de`. This seat edits no QUALITY.md line; the block below is paste-ready and verbatim.

## Round-34 criteria

- **A cited artifact resolves from committed lane bytes, not a seat's sandbox.** A cited
  counterexample commit, patch, retained source or receipt is committed under the lane; the
  citing line names a lane-relative path that `git cat-file -e <revision>:<path>` resolves at
  the revision it is added or corrected in. A `/fast/scratch/...` or `/tmp/...` path stands
  beside that path as provenance, never as the only pointer; a preserved earlier line stays
  byte-identical and the lane path arrives as an appended correction. Reject: a pointer that
  resolves only in a seat's sandbox; a retained file no committed line cites; a citing line
  whose retained path is absent at the citing revision. Grounding: routed item 2
  (`corpus/lessons/round-33-verifier-spotcheck.md:192-196`), where `489714be` and the
  option-table patch were cited from `/fast/scratch/hyaku/kake-r33/w1/...` only; round 34 now
  retains them at `.ufo/waves/round-34/retained/` as
  `r33-c1-counterexample-489714be.bundle` (`a2fe31b2`, sha256 `6ff6c403…77c00`, head
  `489714be413c…` on tag `r33-c1-counterexample`), `r33-option-table-dedup-patch.diff`
  (`28fd9adf…47d6e`) and `r33-option-table-alt-patch.diff` (`daeaa738…0ce6e`), beside the
  pinned ds4cc bytes under `.ufo/waves/round-34/sources/`. Check: per cited sandbox path,
  `git cat-file -e <revision>:<retained path>` for each retained file the section names;
  able to fail at `d08d8de` (exit 128) and pass at `a2fe31b2` (exit 0). Limit: retention
  makes bytes reachable, not proved; whether the bundled commit or patch says what the
  citing line claims stays with the round's probes and the non-author read.
- **A round's `## Gate` records at least one screened reject with its reason.** Every
  candidate the Gate screens carries a decision, and each reject states the located fact
  that failed it (the quote or byte that did not match), not a status word or the verdict
  again. Reject: a Gate whose decisions are all admits; a reject with no reason; a screened
  rejection recorded only in a wave report. Grounding: routed item 3
  (`corpus/lessons/round-33-verifier-spotcheck.md:197-198`); the round-33 Gate
  (`corpus/lessons/round-33.md:25-37`) holds two `admit` rows and no `reject` word
  (`grep -c reject` there: 0), so the LEARNING admit+reject sample used a code patch; round
  34 screened S071 and S072 as rejection candidates (`SCORECARD.md:1202-1203`). Check:
  `python3 -B .ufo/waves/round-34/criteria/gate_reject_check.py --repo . --rev <commit> --lesson <path>`
  (its docstring states the exit contract; this criterion requires it to fail a Gate with no
  reject and a reject with no located reason). Receipts: `<pending>` — the checker is
  another seat's wave-1 deliverable and no run is claimed. Limit: structural over the
  lesson text at `--rev`; a present reason is not a true reason.
- **Every run a report cites ships a committed receipt.** A report line stating that a
  command ran at a revision names the receipt committed in that round whose `revision` field
  equals the stated revision; a run without one is written as not run, and "run, not
  committed" is not a result. Reject: a tally with no receipt; a glob (`c1-after-*.json`)
  offered for a named revision; a receipt naming a different commit than the citing line.
  Grounding: routed item 4 (`corpus/lessons/round-33-verifier-spotcheck.md:199-201`) and its
  quoted line `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kake.md:62`
  ("`93359ff`: 4/4 (run, not committed)"), harmless only because `git diff 3abfc44 93359ff
  --stat -- scripts/` is empty. It extends the round-30 bullet at `corpus/QUALITY.md:450-460`
  to every run a report cites; that witness reads the working tree and stays for claim
  revisions. Check:
  `python3 -B .ufo/waves/round-34/criteria/receipt_presence_check.py --report <md> --repo . --rev <commit> --round <N>`
  (report read from disk, possibly the fleet path; receipts resolved in `--repo` at `--rev`).
  Receipts: `<pending>` — the checker is another seat's wave-1 deliverable and no run is
  claimed. Limit: presence and revision agreement, not replay or tally truth.

## Commands (read-only; lane rev `a2fe31b2`; lane tree untouched)

| command | exit | observed |
|---|---|---|
| `grep -n "Two evidence artifacts\|records no reject\|cites a run" corpus/lessons/round-33-verifier-spotcheck.md` | 0 | items at 192, 197, 199 |
| `git ls-tree -r --name-only a2fe31b2 -- .ufo/waves/round-34/retained` | 0 | 3 files; at `d08d8de` 0 lines |
| `git cat-file -e {d08d8de,a2fe31b2}:…/r33-c1-counterexample-489714be.bundle` | 128, 0 | absent at `d08d8de`, present at `a2fe31b2` |
| `git show a2fe31b2:….bundle \| sha256sum`; `git bundle list-heads ….bundle` | 0 | `6ff6c403c4df5b2afa532556fcf13f9d4f6db55905442a77daa0955ab7877c00`, equals on-disk; head `489714be413c936a6d98188a80fce016c0b52ef7` |
| `git show a2fe31b2:…dedup-patch.diff \| sha256sum`; alt patch | 0 | `28fd9adf…47d6e`, `daeaa738…0ce6e`, both equal on-disk |
| `awk 'NR>=25 && NR<=37' corpus/lessons/round-33.md \| grep -c reject` | 0 | `0` |
| `git grep -n "fast/scratch" a2fe31b2 -- SCORECARD.md` | 0 | `:1103` sandbox pointer, no lane sibling |
| `git status --porcelain -- .ufo/waves/round-34/retained .ufo/waves/round-34/w1` | 0 | `?? .ufo/waves/round-34/w1/`; retained tracked |

## Findings and limits

1. `ls .ufo/waves/round-34/criteria/*.py` exits 2: both checkers were absent at write time, so
   criteria (b) and (c) carry `<pending>` receipts and are unexercised. Not run: the checkers, the
   C1/C2 counters, the round-33 script diff quoted in (c), any judgment of the round.
2. `SCORECARD.md:1103` keeps a `/fast/scratch/hyaku/kake-r33/` pointer while the archive sits at `.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz`; criterion (a) is met there by an appended correction, not by editing the preserved declaration.
3. Criterion (c) extends, not replaces, the round-30 receipt bullet, so the scopes do not collide;
   criterion (b) fails if round 34 admits both S071 and S072.
4. Only criterion (a) has a runnable able-to-fail witness today. Untouched: `corpus/QUALITY.md`,
   the checkers, claims, counters, lane index and refs. No tool installs; sandbox
   `/fast/scratch/hyaku/kake-r34/w1/ScribeQualityCriteria/` holds only empty `tmp/`.
