# Sibling-overlap scan — C1 and C2
Axes: operability (primary), freshness. Advisory evidence and one bounded proposal; no code edits, integration, runtime invocation, admission or round verdict.
Paths below are relative to `/home/vgpnk/Projects/shokunin/` unless absolute.

## Scope and evidence
Read-only corpus searches covered twenty siblings; executable searches covered twelve sibling script/tool/verifier roots. Exact query patterns, expanded-scope description, commands, exits and stdout: `/fast/scratch/hyaku/kake-r32/w1/ConnectorSiblingOverlap/scan-evidence.json`.
The completed corpus sweep found no `render.yaml`, `render-web-services`, `render.com/docs`, `ds4cc-marketplace`, or either C2 blob-id match. This is not a fleet-wide absence claim: recursive filename scans and the broader sibling `.ufo` content search timed out. Domain-name mentions in Kotoba/Tabi are not independent Render sources.

| Overlap | Evidence and observed blob/hash | Reuse or cite? |
|---|---|---|
| C1 mutation mechanics | `tameshi-shokunin/tools/mutate-and-run.sh:40-68,115-128`; blob `c9e255e823e5827e037876ecfd797a268a2f449a` | Cite its unique-edit, pristine-control and pinned-replay method. Do not replace Kake's specialized counter with it unchanged. |
| C1 existing sibling citation | `kake-shokunin/corpus/SOURCES.md:64` already records S056, MTE interop at `f4e8f7d835a8e33c64a87ff93e79da32264f031c`; re-read hash `b173e3e549d0227e0d37df92956b652084290955bdcb6a0a7cbf2a9ad29c0fac` matches the row | Reuse that exact citation for per-mutant records versus aggregate sanity checks; do not create another row for the same opened source or treat it as Kake behavior evidence. |
| Both claims: command/receipt binding | `tameshi-shokunin/tools/command-binding.py:7-16`; blob `1b4bbb7741722a69945d8a6e15e37da0333d1997`; explanation `corpus/knowledge/required-command-binding.md:13-34,49-57` in that lane | Reuse the documentation pattern: exact argv, cwd, revision and expected exit are distinct from merely possessing source bytes. No new sibling executable dependency proposed. |
| Both claims: identity versus result reuse | `tameshi-shokunin/tools/pin-disposition.py:8-12,58-65`; blob `89a6ca38184138425fdb16ce7d0f955a51702b89` | Cite the explicit `result_reuse=not_established` boundary; matching bytes alone do not transfer a mutation result or demonstrate live freshness. |
| C1 fixture isolation | `mori-shokunin/tools/mori-round17-jj-regressions.py:31-51`; blob `317959bb815745b581bb3974eaa13ab3f48cd7e5` | Cite the existing real-Git, per-case sandbox pattern. Do not import Mori's unrelated census/jj suite. This is overlap identification, not a sandbox-threat-model audit. |
| C2 retained external source and negative controls | `tabi-shokunin/corpus/evidence/round-20/lifecycle/decisions.json:3-9`; blob `61b0ce7f15e5fca72d417a8dfeb5f06641e8d58f`; `selftests/expected.json:84-95` under the same round, blob `a266f681be5ebd4547e8f0946eff86099552c815` | Reuse the record shape: retained path, upstream URL/revision, digest, explicit source-only scope. Its missing-source and appended-byte controls are precedents, not additional C2 test results. Do not copy Chromium content into the Render corpus. |
| C2 citation/registry validation | `kumitate-shokunin/scripts/anchor-truth.mjs:26-32,74-87`, blob `489e28529daf89dd90b5180c5409a5bd5b26e17e`; `scripts/sources-check.mjs:3-8,10-44,61-101`, blob `6b57424fc5a213a01015beaceb97de47a67967f0` | Cite bounded anchor and registry checks as methods only. Token occurrence is not semantic truth; lane-specific pin/legacy policies prevent treating these as drop-in Kake gates. |

## One proposed move
Add one small, offline replay card to the existing round-32 lesson, with separate columns for **input identity** and **observed behavior** for C1 and C2. Borrow Tameshi's identity/result distinction and Tabi's source-only labeling, not their runtimes.
For C1, point to the frozen counter invocation, measured lane revision, runner digest and separate pristine/mutant/benign receipt fields. For C2, point to the original ds4cc revision, the two retained paths/blob IDs, S062 and the retention receipt; label these source retention, not a new service observation.
[INFERENCE] Operability improves because one bounded card tells a later reader what can be replayed offline and what each receipt actually establishes. Freshness is not claimed to improve: original source dates and live-state limitations remain visible. Neither declared counter, claim denominator nor claim independence changes.

## Contradictions and risks
- No drop-in runner equivalence: Tameshi's suite contract classifies nonzero exits other than 124/126/127 as red (`mutate-and-run.sh:60-61`), while Kake's hostile selftest reserves exit 2 for bad input (`citing_set_hostile_selftest.py:62-65`). A direct substitution could count setup refusal as a kill.
- Input retention is not behavior reproduction: `pin-disposition.py:8-12` explicitly refuses that inference. Likewise C2's offline copies cannot establish live Render state; Kake already says so at `corpus/knowledge/render-web-services.md:4,79-90`.
- S056 covers one pinned MTE entry only, not every Tameshi file above. Any durable citation to another source requires its own correctly scoped opening/curation; do not silently widen S056 or mark it mined without an actual citation and used-by update.
- Active sibling HEADs, tree reads and worktree hashes were separate observations, not an atomic snapshot. The evidence JSON preserves blob IDs and worktree digests separately; do not introduce live sibling-path dependencies into Kake's replay.
- No analysis of whether the runner's reported failure names or reason text are trustworthy was performed; the held lines were not reopened.

## Commands executed
All commands below completed with exit 0; full stdout is retained in `scan-evidence.json`. The pipeline status is the pipeline's status, not a separately captured status for each process.
`mkdir -p /fast/scratch/hyaku/kake-r32/w1/ConnectorSiblingOverlap/tmp`
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree HEAD -- tools/mutate-and-run.sh tools/pin-disposition.py tools/command-binding.py corpus/knowledge/required-command-binding.md`
`git -C /home/vgpnk/Projects/shokunin/tabi-shokunin ls-tree HEAD -- corpus/evidence/round-20/selftests/expected.json corpus/evidence/round-20/lifecycle/decisions.json corpus/evidence/round-20/sources/html_form_element.cc corpus/knowledge/webmcp-completion-lifecycle-round-20.md`
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree HEAD -- tools/mori-round17-jj-regressions.py`
`sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/command-binding.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/required-command-binding.md /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-jj-regressions.py /home/vgpnk/Projects/shokunin/tabi-shokunin/corpus/evidence/round-20/selftests/expected.json /home/vgpnk/Projects/shokunin/tabi-shokunin/corpus/knowledge/webmcp-completion-lifecycle-round-20.md`
`git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin ls-tree HEAD -- scripts/anchor-truth.mjs scripts/sources-check.mjs`
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse --verify HEAD` → `b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a`
`git -C /home/vgpnk/Projects/shokunin/tabi-shokunin rev-parse --verify HEAD` → `e3cf4e0d30bb835532ff44b118c5ad52e09eb76d`
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse --verify HEAD` → `ac696ad3037c3071584df60d84b5bf0af9818dd6`
`git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin rev-parse --verify HEAD` → `fb7046ca862e0d92f76c2a718a24807433c603ff`
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f4e8f7d835a8e33c64a87ff93e79da32264f031c:corpus/knowledge/mte-report-interop.md | sha256sum` → S056 digest above.
`export TMPDIR=/fast/scratch/hyaku/kake-r32/w1/ConnectorSiblingOverlap/tmp`

## Verification and limits
Exercised: local searches, source reads, read-only Git provenance queries, file hashing, and S056 pinned-digest comparison. No tools installed or updated.
Read, not rerun: `kake-shokunin/.ufo/waves/round-32/verification/c1-after-2f2f12d.json:64-70` records benign 45/0, guard_ok true, killed 1; `c2-after-2f2f12d.json:12-21` in the same directory records met 3.
Proposed verification for L1, not executed here: independently replay the unchanged declared C1/C2 counters in the authorized sandbox and check the card against those receipts; confirm it preserves C2's source-only limits and C1's separate controls. No sibling selftests or mutation ledgers were run. Broad sibling-cache absence remains unverified, not passed.
Only this requested report was written in the lane; the supporting evidence JSON and empty scratch temporary directory remain in the named sandbox.
