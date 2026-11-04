# ScoutRecon — round 84 wave w1

Read-only recon of the C1 queue at the freeze plus the bounded planning data-walk. No production
file was written; nothing outside `.ufo/waves/round-84/w1/ScoutRecon.md` and
`.ufo/waves/round-84/w1/ScoutRecon/` was touched. All commands ran with
`cd /home/vgpnk/Projects/shokunin/kake-shokunin`; the scratch dir
`/fast/scratch/hyaku/kake-r84/ScoutRecon/` was deleted before this report was yielded.

Revisions observed: base `fe42ad11eb1084ad2ea68d12c5bbb2922a089868` (ancestor of the freeze, exit 0
from `git merge-base --is-ancestor`), freeze `f358022f7e1b2f3846be8ceacbe3a7ef22edf4be`, worktree
HEAD `87cbfd99b677a330c14a68a33f10548f15e6e10c` (`round-84: w1 spec, validated dispatch and ready
file`, descendant of the freeze, exit 0). `scripts/policy_value_class.py` **exists untracked in the
worktree** at my read and is **absent at the freeze** (`git cat-file -e f358022…:scripts/policy_value_class.py`
→ rc 128); any worktree-based C2 reading during the wave is therefore racy and should be taken at a
revision.

## 1. The four routed defects, restated from `corpus/lessons/round-83-verifier-spotcheck.md` §6

- **D1 (discernment).** Measured: the round-83 Gate rejects RFC 9111's “Invalidating Stored
  Responses” and “Common Cache-Control Directives” sections, and the second title does not exist in
  the retained RFC (headings are §5.2 *Cache-Control*, §5.2.1 *Request Directives*, §5.2.2 *Response
  Directives*, §5.2.3 *Extension Directives*). Asked: append a named correction in the next lesson
  citing the real headings; the reject itself stands.
- **D2 (quality).** Measured: the same Gate says the `:838-839`/`:840-844` quotes are “22 + 44 words”
  while its own check line records “14 / 23 / 21 / 48”, and the verifier's count of the `:838-844`
  span is 66 words (48 only if the final parenthetical is dropped). Asked: state one measurement and
  the span boundary next time.
- **D3 (L2 floor).** Measured: prompt §3's minimum role split asks for 1× connector and wave `w1`
  carried none. Asked: carry one connector seat or file the waiver with the wave's claimed-shape
  rationale in the report.
- **D4 (frontier step).** Measured: the report gives the round-start census as prose (“exit 0, 22
  `W04`”) while only `controls/census-after.txt` is committed; the round-82 precedent committed a
  before receipt. Asked: commit the start-run output next round (the verifier's base replication
  gives 193 rows / 22 `W04`).

## 2. C1 — the file each item needs and the exact shape the counter greps

Counter read in full: `.ufo/waves/round-84/c84_defect_queue.py` (335 lines). It reads a worktree or
`git -C <root> show <rev>:<path>`, and prints one `item=<D#> closed=<0|1> state=<0|1> row=<0|1> …`
line then `C1v1 revision=<token> items=4 open=<n> closed=<n> met=<true|false>`, exit 0 iff `met`.

| item | file a seat must produce | exact string shape the counter tests |
|---|---|---|
| D1 | `corpus/lessons/round-84.md` | a line with `line.lstrip().startswith("[r84-correction")` that contains **all four** literals `5.2.  Cache-Control`, `5.2.1.  Request Directives`, `5.2.2.  Response Directives`, `5.2.3.  Extension Directives` (two spaces after the number; one after the final dot), **and** each of the four is also a raw substring of `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt`; plus a `[r84-correction` line containing both `round-83.md` and `Gate` while `state` is true |
| D2 | `corpus/lessons/round-84.md` | one line matching `D2 count=(\d+) span=838-844 measure=words-full-span`; `<n>` must equal `len(re.findall(r"\S+", "\n".join(rfc_lines[837:844])))` = **66** (boundary lines 838–844 inclusive; newline join makes no difference — I measured both 66) |
| D3 | `.ufo/waves/round-84/w1-spec.json` **and** `.ufo/waves/round-84/w1-results.json` | spec has ≥1 item with `role == "connector"` (already true: 1 of 13 at HEAD); results has ≥1 row with `agent == "connector"` and `output.strip()` non-empty (file absent at freeze → open) |
| D4 | `.ufo/waves/round-84/controls/census-before.txt` | contains `census_exit=0`; one line containing `\tok\t` and `SOURCES.md`; every `\tW04\t` line must be shaped `<id> duplicate url <normalized-url> across scopes` (tab-split, `parts[0]`=id, `parts[1]` minus `" across scopes"`=url), and the sorted set must equal the counter's own `census_w04()` over the measured tree's `corpus/SOURCES.md` |

Measured inputs, independently: the four heading literals each occur **2×** in the retained RFC
(`grep -Fc`, exit 0); the `:838-844` span is **66** words (`derived=66`, `no-join=66`); the freeze
`census-before.txt` carries **22** `W04` lines plus one `ok` line naming an absolute
`…/kake-shokunin/corpus/SOURCES.md`. My own census parse over `f358022…:corpus/SOURCES.md` gives
**195** registry rows, **194** `S` rows, **22** `W04` collisions, max id **S456** — so the next free
id is S457, matching `ScribeRegistry`'s item.

Selftest: `python3 -B …/c84_defect_queue.py --selftest` → 8 `ok` lines, `selftest: 8/8 passed`, exit
**0**: `green-all-closed` (0), `junk-prose-only` (2), `mutant-d1-wrong-heading` (1),
`mutant-d2-wrong-count` (1), `mutant-d3-no-connector` (1), `mutant-d4-wrong-w04` (1),
`mutant-rfc-absent` (2), `missing-tree-reopens-all` (4). The committed control
`controls/c84-selftest-c1.txt` is the same eight lines with `selftest_c1_exit=0`; my run reproduces
it.

Freeze reading, read-only:
`python3 -B .ufo/waves/round-84/c84_defect_queue.py --root . --revision f358022f7e1b2f3846be8ceacbe3a7ef22edf4be`
→ `D1 open`, `D2 open`, `D3 open`, `D4 closed=1 state=1 row=1 receipt_w04=22 derived_w04=22`,
`C1v1 revision=f358022… items=4 open=3 closed=1 met=false`, exit **1**. So D4 is **already closed at
the freeze**, and C1's base state is open=3, not open=4.

## 3. Data-walk — `corpus/knowledge` at the freeze

`git ls-tree -r --name-only f358022f7e1b2f3846be8ceacbe3a7ef22edf4be -- corpus/knowledge | wc -l`
→ **74** (69 `.md`, 5 `.json`). `corpus/knowledge/policy-value-classes.md` does not exist at the
freeze (`git cat-file -e` → 128), so the entry is net-new. A loose regex
`cache-control|freshness|stale|max-age|etag|policy` (`git grep -il`) matches **48** entries; the
eleven below are the ones whose scope/opening lines put them on this ground (the other 37 were not
read and are not claimed either way).

| entry | what it holds | verdict for a new `policy-value-classes.md` |
|---|---|---|
| `header-change-classes.md` | RFC 9111 class table (18 located quotes); §4 at line 98 defines `policy` as a name-level class that “is recorded in its own counter but does not flip the verdict by itself” (line 101) and says the name table is lane policy | **EXTEND** — this is the seam: value-level classes for exactly the names the frozen table calls `policy`. Duplicate only if the new file restates §2's quote table or the name→class mapping; cite `scripts/header_change_class.py` (`POLICY` at lines 54–63) instead |
| `capture-drift-validators.md` | RFC 9110 validator reading + `capture_delta.py`; §7 (line 216) reads `expires = cache-fill epoch + max-age (600 s)` and `Age: 0` | **EXTEND by citation only** — its scope line excludes cache policy, and the new entry must not re-derive validator semantics or the cache-fill arithmetic; cite the one real-pair observation |
| `response-header-expectations.md` | six publisher-side presence/audit classes (S430–S433); line 66 “it does not parse `max-age`”; lines 110–111 “does not parse the policy, does not compare two policies”; limits: “Presence is not policy strength” | **no duplication** — nearest prior art, and the entry that names the gap (presence vs. value/strength). State the boundary; do not re-teach the six classes |
| `x-robots-tag-header.md` | declarations in recorded response header fields (S452/S449); `x-robots-tag` is in the frozen `POLICY` set | **adjacent** — directive semantics of one policy-class field, not a value-class taxonomy |
| `http-date-grammar.md` | date shapes in a recorded `X-Robots-Tag: unavailable_after` value | **adjacent value grammar**, different field family |
| `ghp-etag-anatomy.md` | decodes the recorded ETag (validator), never identity | **no overlap** on policy values |
| `render-static-sites.md` | line 53 quotes Render's example response `cache-control: public, max-age=86400 …` | **no duplication** — publisher platform doc, not a classifier |
| `freshness-sweep.md` + `freshness-pins.json` | standing-claim drift instrument and its pinned baselines (`kake-freshness-pins-v1`) | **name collision only** — “freshness” here is claim staleness, not HTTP cache lifetime |
| `drift-detection.md` | historical live-vs-source probe; source tree absent since the 2026-10-12 prune | **no overlap** |
| `sidecar-reobservation.md` + `freshness-sidecar.json` | local-path absence notes (`kake-paths-sidecar-v1`) | **no overlap** |
| `meta-robots-directives.md` | HTML meta declarations, not HTTP header fields | **no overlap** |

Also excluded after reading their opening lines: `instrument-receipts.md` and `receipt-integrity.md`
(receipt ground the C2 `record_equal` conjunct reuses by citation), `static-canonical-preflight.md`
(its “policy” hits are local publishing policy, not HTTP policy headers), `probe-delta-alerting.md`
(probe-history diffing), and the platform/crawler entries whose `policy`/`freshness` hits are name
collisions. Conclusion: **no existing entry duplicates a value-level policy-class table**; the only
duplication risks are restating `header-change-classes.md` §2/§4 and
`capture-drift-validators.md` §7.

## 4. Ordering of the round's work

Production file → the receipt it unlocks (each arrow is a hard input dependency the counters read):

1. `ScoutSources` retained RFC + located anchors (round-84 path) → cited by the entry and by the
   lesson correction; D1's state half also needs the **round-83** retained `rfc9111.txt` (present).
2. `corpus/SOURCES.md` **S457** row (`ScribeRegistry`) → must resolve before the entry cites `S457`
   (QUALITY.md: every cited `S###` resolves in this registry at the citing revision) and before the
   after-census. Census at HEAD: 194 `S` rows, max `S456`.
3. `corpus/knowledge/policy-value-classes.md` (`ScribeKnowledge`) → cites S457 + the retained bytes;
   coverage-index rows in `corpus/README.md` land with it.
4. `scripts/policy_value_class.py` (`ExecPolicyTool`) → then
   `.ufo/waves/round-84/controls/tool-real-pair.txt` (the counter's `RECORD`) can be taken; a fresh
   run's stdout must equal that committed record after stripping one trailing newline, and the tool
   must be **final** (the record is compared to a fresh run with `TMPDIR=<work>`).
5. `corpus/lessons/round-84.md` (`ScribeLesson`) → unlocks D1 and D2. With the census receipt already
   frozen, the maximum pre-WAVE-DONE state is D1+D2+D4 closed and D3 open, so **C1 cannot reach
   `met` before WAVE-DONE**.
6. L1-only, after WAVE-DONE: `w1-results.json` (no script writes it; `make_wave_spec.py` writes only
   the spec/dispatch, and no round-84 file references `w1-results.json` except the counter) → then
   `controls/after-c1.txt`; the wave-landing commit → `controls/after-c1-tip.txt` and
   `controls/after-c2-tip.txt`; the pushed-lane `jj-lane.sh state` / `landed <hash>` citation; the
   at-tip `controls/census-after.txt`. Only the L1 can take these because only the L1 may write
   `w1-results.json` and commit/push.
7. Not L1-only: `controls/after-c2.txt` at a wave commit is still a committer-side receipt, but the
   C2 `record` and the tool's own `--selftest` can be taken by any seat once step 4 lands.

## Findings (routed, not patched — frozen files untouched)

- **F1.** The contract's C1 counting line advertises `--fleet <dir>`; the counter's parser accepts
  only `--root/--revision/--selftest/--work` and exits **2** on `--fleet`
  (`error: unrecognized arguments`, measured). A seat copying the contract's command verbatim fails.
- **F2.** The contract claims a prose **row conjunct** for D3 (“the round lesson or `SCORECARD.md`
  names the connector seat”) and D4 (“the round lesson names `controls/census-before.txt`”), but the
  counter never reads the lesson for D3/D4. Measured probe: a fixture tree whose lesson contains
  **zero** occurrences of `connector` and **zero** of `census` still prints
  `C1v1 … open=0 closed=4 met=true`, exit **0** (`ScoutRecon/prose-row-probe2.txt`).
- **F3.** D4 is closed at the freeze revision (the start census is committed at the freeze), so C1
  reads `open=3 closed=1` at `f358022…`; a seat expecting the contract's “four open” picture will
  misreport. The committed base control also carries token `revision=worktree`, not the freeze hash.
- **F4.** The selftest cannot catch F2: its `junk-prose-only` fixture keeps the good `w1-spec.json`,
  `w1-results.json` and census receipt (so D3/D4 stay closed and the expected open count is 2), and
  no fixture exercises a prose-free D3/D4 row.
- Non-finding: C2's `evaluate()` sets `tool_absent` but does not use it in `met`; absence is fatal
  through `tool_offline` and `selftest_ok` anyway.

## Limits

I did not re-derive C2's control-pair header edits (ExecControlAudit owns that), did not run the C2
tool (absent at the freeze and untracked/partial in the worktree at my read), and my data-walk
duplicate judgements are scope/opening-line and cited-window readings, not a full read of all 69
Markdown entries.

## Verdict

Recon complete and consistent with the frozen contract's mechanism: D1, D2 and D4 are deterministically
producible, D3 is gated on the L1's post-WAVE-DONE `w1-results.json`, and C2's `met` is gated on the
tool plus the committed `tool-real-pair.txt` record. Two frozen contract row conjuncts are not
enforced by the counter (F2, with a measured green probe) and the contract's `--fleet` flag does not
exist in the code (F1); both are reported, not patched. No production file written; no network used;
scratch deleted.
