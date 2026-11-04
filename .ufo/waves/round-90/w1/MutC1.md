VERDICT: C1 counter is honest but under-controlled — 7/22 mutants killed by the frozen controls (6 by forgeries, 1 by the positive); 15 survive. All 15 die on MutC1's supplemental forgeries. Two forgeries also close D1 on the FROZEN counter: a root file hidden by `.git/info/exclude` or by a `/baseclean.out` line in `.gitignore`. A trivial 3-word RFC fragment closes D3 on the frozen counter too. None of this falsifies the C1 carrier reading. The lane's live tree hides no root entry: only `.jj/` is ignored.

Seat MutC1, round 90, wave 1. The counter under test is `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/c90_defects.py`, sha256 `462224f630d4369138af1bf38783b16695b712b85bb46b7b9d2d3c35f05d519b`. That matches freeze.md before and after every run.

## Method

- **Mutants.** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/w1/MutC1/make_mutants.py` builds 22 single-conjunct mutants from the frozen bytes. Each one is a single exact textual replacement, and the script asserts the anchor matches exactly once. The frozen source is never edited in place, so no restore is needed, and its sha256 was re-hashed afterwards (above). The mutants and their sha256 are in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/w1/MutC1/mutants/` (`manifest.tsv`, sha256 `e39ebe2b…`).
- **Driver.** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/w1/MutC1/drive.sh` (sha256 `e8006a00…`) copies the C1 section of `controls/run_controls.sh`. OUT is changed to `w1/MutC1` and SCR to `/fast/scratch/hyaku/kake-r90/MutC1` (also TMPDIR). It makes one `--shared` clone, checks the toplevel, and uses the fixture identity on every commit.
  - It rebuilds all 9 control fixtures (do-nothing, D1a, D1b, D2a, D2b, D2c, D3a, D3b, positive) and adds 19 supplemental forgeries (X-*).
  - On each fixture state it runs the frozen counter (M00) and all 22 mutants in parallel, each with its own `--work`.
  - One deviation: do-nothing runs on the fixture at the freeze-bytes commit with the inherited `baseclean.out` placed untracked at root. The lane at base is not used because the lane's live tree no longer holds that file.
- **Baseline parity.** The M00 reason JSON on the 9 control fixtures is byte-identical to `controls/ctl-c1.txt` (`diff` exit 0). The baseline is not inconclusive: the frozen counter leaves each forged item open and closes the positive (`open=0 closed=3 met=true exit=0`).
- **Kill rule** (`tabulate.py`): an item the frozen counter leaves open on a forgery fixture is closed by the mutant. `P` means the mutant leaves the positive open.
- **Commands:**
  - `bash …/w1/MutC1/drive.sh` → rc=0, 271 s.
  - `python3 -B …/w1/MutC1/tabulate.py > kill-table.txt` → rc=0.
  - No run printed a Traceback; `grep -l Traceback runs/*/*.txt` is empty.
- **Receipts:** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/w1/MutC1/drive-log.txt` (sha256 `d9cbef29…`) and `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/w1/MutC1/kill-table.txt` (sha256 `1ae6d3ed…`). There are 672 per-run outputs in `…/w1/MutC1/runs/<fixture>/<Mxx>.txt`, plus `_status.txt`, the fixture's live porcelain.

## Kill table (from kill-table.txt)

| mutant | conjunct dropped / weakened | vs frozen controls | MutC1 supplemental forgery that kills it |
|---|---|---|---|
| M01 | D2 base-prefix (append-only) | **killed** c1-F-D2c | — |
| M02 | D2 frozen c89 re-run | **killed** c1-F-D2b | — |
| M03 | D2 receipt first-line agreement | survived | X-D2e: fabricated receipt `open=0 closed=6` cited by a correction stating `open=1 closed=5`, which the re-run agrees with |
| M04 | D3 S463 byte-identity | **killed** c1-F-D3b | — |
| M05 | D3 quote-in-retained-body | **killed** c1-F-D3a | — |
| M06 | D3 accept any wording containing S463 instead of `supersedes S463 —` | survived | X-D3c: teaches `S463 remains authoritative — …` |
| M07 | D1 live untracked lane-root check | **killed** c1-F-D1a (also X-D1d) | — |
| M08 | D1 relocated-copy sha | **killed** c1-F-D1b | — |
| M09 | D2 SCORECARD OR LOG instead of both | **killed** c1-F-D2c (only SCORECARD is rewritten there, LOG stays valid; also X-D2d) | — |
| M10 | D1 `baseclean.out` not tracked at root | survived | X-D1c: root file committed beside the relocated copy |
| M11 | D3 source cell names rfc9111 | survived | X-D3d: source is an rfc9110 URL |
| M12 | D3 status == mined | survived | X-D3e: status `queued` |
| M13 | D3 new-row scope lacks `not cache-key construction` | survived | X-D3f: new row repeats the defective scope |
| M14 | D3 retained RFC body sha | survived | X-D3g: `rfc9111.txt` replaced with the fabricated quote |
| M15 | D3 quote length 3..25 words | survived | X-D3h: 2-word quote `cache key` |
| M16 | D3 quote must sit in `## Gate` | survived | X-D3i: quote only in `## Notes` |
| M17 | D3 quote line must name the row id | survived | X-D3j: S467 named on a different Gate line |
| M18 | D2 correction line must cite `f62e7954` | survived | X-D2f: otherwise-valid correction with no `f62e7954` |
| M19 | D2 receipt must be tracked | survived | X-D2g: receipt path never committed, numbers match the re-run |
| M20 | D2 reading = first `open/closed` on the whole line (v0 parse) | **detected by positive** (P) | X-D2h: earlier number right, stated reading `open=0 closed=6` wrong |
| M21 | D3 superseding row must be NEW | survived | X-D3k: existing S465 rewritten in place into a supersede row |
| M22 | D1 live check also counts root directories | survived | X-D1d: untracked `scratchdir/` at root |

The positive fixture stays closed under every mutant except M20, so no mutant is trivially vacuous.

**What the survivors leave uncovered.** Each survivor names a forgery class that `run_controls.sh` does not cover:

- **D1:** a root file that is committed (tracked); an untracked root *directory*.
- **D2:** a fabricated or disagreeing receipt that the re-run happens to back. M03 is masked by the c89 re-run, which is defence in depth, not a gap in the closure, but the conjunct is untested. Also: an untracked receipt; a correction that does not cite `f62e7954`.
- **D3:** non-`supersedes` wording; non-rfc9111 source; non-mined status; a scope that repeats the defect; a tampered retained body; out-of-bounds quote length; a quote outside `## Gate`; a quote line that names no row; an existing row rewritten in place.

Every one of these conjuncts is live in the frozen counter: M00 leaves the item open on each X fixture.

## Defects in the frozen counter (forgeries that close an item on M00)

1. **D1 can be closed with the root file still present, via `.git/info/exclude`.** Fixture X-D1e: relocated copy committed, `baseclean.out` left at root, `.git/info/exclude` set to `baseclean.out`. M00 reads `D1: []` (`runs/X-D1e-root-file-info-exclude/M00.txt`, `_status.txt` empty). The live conjunct reads `git status --porcelain --untracked-files=normal`, which omits ignored files. The exclusion lives in `.git/`, so no committed byte shows it.
2. **The same works through a committed `.gitignore` line `/baseclean.out`.** Fixture X-D1f gives M00 `D1: []` (`runs/X-D1f-root-file-gitignored/M00.txt`). This one leaves a trace at the revision, but the counter does not read it.
   - Fix for both: add `--ignored` (or `--ignored=matching`) and treat a `!!` root entry as open, perhaps with an allow-list such as `.jj/`.
   - A first X-D1f attempt with the unanchored pattern `baseclean.out` also ignored the relocated copy. That left D1 open for the wrong reason, so it was re-run with `/baseclean.out`.
3. **D3 accepts any 3-word fragment of RFC 9111 as the "located quote".** Fixture X-D3l: Gate line `S467 admit: "the request method"`. M00 reads `D3: []` (`runs/X-D3l-trivial-3-word-quote/M00.txt`). The phrase occurs 4 times in the body. The frozen spec ("3..25 words that occurs") allows this, so it is a weakness of the frozen predicate rather than an implementation bug: the quote does not have to support the supersede claim.

## Carrier check (read-only, the lane)

`git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain --ignored --untracked-files=normal` shows exactly one ignored root entry, `!! .jj/` (jj metadata). `.git/info/exclude` holds only the default comments. `core.excludesFile` is unset and `~/.config/git/ignore` does not exist. So defect 1 does not apply to the measured carrier: `baseclean.out` is really gone from the lane root (`ls` → No such file). `.ufo/waves/round-90/inherited/baseclean.out` at `e50c9566` hashes to `4046c204…`, which equals INHERITED_SHA.

## Honest limits

- Mutants are hand-chosen single conjuncts, not an exhaustive operator set. The regex constants (CORR_RE, REC_RE, OC_RE, ROW_RE) and the 11-cell row-shape check were not mutated.
- The do-nothing fixture is a fixture equivalent rather than the lane at base (see Method).
- The lane working tree showed ` M corpus/lessons/round-90.md` and ` M scripts/cache_key_conformance.py` (plus earlier ` M PROVINCE.md/SKILL.md/corpus/*`) during my run. Those edits are not mine; I wrote only under `w1/MutC1/` and `w1/MutC1.md`.
- No tool installs, no network, no lane git mutation. Scratch `/fast/scratch/hyaku/kake-r90/MutC1` was deleted before yield (`ls … | grep -c MutC1` → 0).
