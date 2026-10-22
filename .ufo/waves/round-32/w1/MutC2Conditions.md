# MutC2Conditions — can each C2 condition go false?

Seat: KakeR32.MutC2Conditions (mutation tester). Axis: freshness. Base: `285abcad632e3c1c57bb402232e7d218054db383`.
Sandbox: `/fast/scratch/hyaku/kake-r32/w1/MutC2Conditions/` (clone `clone/`, tmp `tmp/`). Counter:
`.ufo/waves/round-32/c2_retained_count.py`, sha256 `48126fc5b42db1e210bcc2c24c7cb699207ee79b0683bf47cb0c8f94c3f3e22c` (copied to the
sandbox unmodified; lane copy read only). Every run: `python3 -B c2_retained_count.py --repo ./clone --rev HEAD` with
`TMPDIR=…/MutC2Conditions/tmp`. Exit 0 always — the counter never exits non-zero on a false condition, it only prints `met`.

## Baseline (pristine bytes)
`c1 true, c2 true, c3 true, met 3`; `c2RowIds ["S062"]`; `c3Cites {"S062": 2}`;
`c1BlobPaths` = `.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/{render.yaml,apps-sdk/Dockerfile}`.
Same at the later lane tip `7e05aa8c04cffa1e963887a9c7c90b4c3d82c4cc` (met 3).

## The three assigned mutants (one commit each, own branch off the base)
| # | mutant | commit | condition | met | drop |
|---|--------|--------|-----------|-----|------|
| M1 | flip one byte of retained `render.yaml` (`services:` → `Services:`) | `b91c5a8` | c1 | 2 | 1 |
| M2 | S062 opened cell `2026-10-22` → `2026-10-21` | `44773f6` | c2 | 1 | **2** |
| M3 | remove both `S062` tokens from the entry append | `d80b9e8` | c3 | 2 | 1 |

M1: blob `d17ab7e5…` → `aeb2455…`; output `c1 false`, `render.yaml` path list empty. M3: `corpus/knowledge/render-web-services.md`,
2 insertions / 2 deletions; output `c3Cites {"S062": 0}`, `c3 false`, `c1 true`, `c2 true`.

## Finding 1 (counter design): M2 drops met by 2, not 1 — c2 and c3 are coupled
M2 breaks only the S062 `opened` cell. Output: `c2RowIds []`, `c2 false`, **`c3Cites {}`, `c3 false`**, `met 1`.
Cause is the counter source, not the mutant: `c2_retained_count.py:54-57` collects `row_ids` only from registry rows
matching `cells[8] == "2026-10-22"`; `c2_retained_count.py:60-61` builds `cites` from `row_ids` only, and `c3 = any(n > 0 …)`.
With no matching row the citation set is empty, so c3 is false by vacuity even though the entry still cites S062 twice.
Consequence: `met` cannot distinguish "S062 row lost its opened date" from "S062 row deleted and its citation removed"
— both give met 1. A lane could carry a wrong `opened` date and a correct entry citation and the counter reports two
failures instead of one. The declared counter command reports only `met` (0..3), so a "met == 3" reader is unaffected, but
the JSON's per-condition attribution is wrong for c3 whenever the opened-date filter rejects the row. Suggested fix for
the counter owner: build the citation set from every `S\d{3}` registry row id, independent of the `opened`-date filter.
This does not falsify the C2 claim: at the base the lane really does retain both blobs byte-identical, really does have
the S062 row with `opened 2026-10-22`, and really does cite S062 in the appended entry section. The counter only cannot
attribute a failure to c2 alone.

## Finding 2 (coverage): four more plausible defects the counter does not catch
All four left `met 3` on a dirty tree (survived):
| # | mutant | commit | counter still says |
|---|--------|--------|--------------------|
| M4 | move the retained copies to `other/dir/ds4cc-1fbdb8ed/` (same bytes) | `98746aa` | `met 3`; `c1BlobPaths` follow the move |
| M5 | add duplicate row `S063` with S062's cells, cite S063 instead | `d6f440a` | `met 3`; `c2RowIds ["S062","S063"]`, `c3Cites {"S062":0,"S063":2}` |
| M6 | delete the S062 tokens from the "Retained copies (round 32, append-only)" section, keep one elsewhere in the file | `b44aea9` | `met 3`; `c3Cites {"S062":1}` |
| M8 | make the S062 row quote a wrong `render.yaml` blob id (`…7252` → `…7253`), copy stays correct | `4e2f8f6` | `met 3` |

M4: the counter matches blobs by id across the whole tree and never checks the declared path
`.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/`. M6: c3 is a bare `\bS062\b` count over the whole entry file, so the citation may sit in any
section; the claim says "in an appended entry section", which is not what is tested. M8: the blob id quoted inside the
S062 row is never cross-checked against the tree's blob id. M5: row identity is not pinned — any registry row matching the
pattern satisfies c2, and c3 accepts a citation of any matching row id. Also run: M7, one byte flipped in the retained
`apps-sdk/Dockerfile` (`81c74fa`) → `c1 false`, `met 2`, drop 1: c1 requires both blobs, not only render.yaml.

## Restoration evidence
`git -C clone checkout -q master` → `git rev-parse HEAD` = `285abcad632e3c1c57bb402232e7d218054db383`;
`git -C clone diff 285abcad HEAD --stat` = empty; `git -C clone status --short` = empty. Blob ids after restore: render.yaml
`d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252`, Dockerfile `ee0b63819a9ce71e51469796541b9075e9676ae9`, `corpus/SOURCES.md`
`a6d2c8140614313c7d86a61dd6f6c965c86bf220`, `corpus/knowledge/render-web-services.md` `0a3c7c700880452ddca4379e8183e9289246a4f6`
— all identical to the base (checked with `git hash-object` on the restored tree and `git ls-tree -r`). Mutant commits stay
reachable in the sandbox clone on branches `m1`…`m8` only; nothing pushed, no lane ref moved.

## Lane hygiene
No lane file was modified by this seat except this report; `git status --short` in the lane shows only untracked wave-1
files from other seats. No `git add`/`commit`/`stash`/`checkout`/`reset`/`push` and no mutating `jj` command ran in the
lane repo; the clone came from `git clone` of the lane path and was mutated only in the sandbox. No live request to any
operator-owned property; the ds4cc-marketplace checkout was not touched.

## Not verified
- The counter at the before-commit `a0b0dff` (declared "before 0") — that is the `RerunC2Before` seat.
- The C1 counter and the hostile selftest — out of scope here.
- That the retained blobs match the external ds4cc-marketplace checkout at commit 1fbdb8ed; I checked only that the lane
  holds those two blob ids. The offline `git cat-file` equivalence is asserted by the lane, not re-verified here.
- No tool was installed or updated (no pacman, uv tool, npm): git and python3 were already present.

## Verdict for the L1 (advisory)
The C2 counter does fail — met falls 3 → 2 for a broken retained blob (M1) and 3 → 2 for a removed entry citation (M3)
— so "counter able to fail" holds in the coarse sense the declared claim uses. Two caveats for the closure: (a) c2 and c3
are coupled in the counter, so the M2 mutant drops met by two and the JSON's per-condition attribution is wrong for c3
when the opened-date filter rejects the row; (b) the counter pins neither the retained path, nor the appended section, nor
the row id, nor the blob id quoted in the row, so four further plausible corruptions survive at met 3. The landed C2 claim
itself is not contradicted: the base tree genuinely satisfies all three conditions.
