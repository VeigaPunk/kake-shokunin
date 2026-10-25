# Round 50 verifier spot-check

author: hyaku closure (non-author integrator, @m_swe)
session: Kimi fresh closure agent — a fresh non-author closure judge dispatched by the hyaku
orchestrator (never by the lane), model MiniMax-M3.1-Flash on the kimi substrate. Not the lane,
not a seat the lane dispatched, not a subagent of the lane. This file verifies; it does not
improve the round.

Round tip checked: `1c7f0769a838852971426a672936413fa50ef84f` (also `origin/master`).
Measured claim commit: `ff3f6ecff5caf579fdc76216aa9cb82fa146a30e`.
Pre-append mirror commit: `33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1`.
Grant/dispatch commit: `89096c387622785af59312bd2ee3b169202f1d4e`.
Dispatch-fix commit: `dfb4a3f9705f26d50c38695ad73a9c8461baf122`.
Base: `9619af67c52939daac502ca7a24c9d714f3f51db`.
Fleet report: `47e235a51334cd9c641180d5466415dabc78fc22` (misroot-list correction) over
`f546bfc076046bd27d70c7efa5672611b8875bf5`.

## Conformance

- The report is committed in the fleet repo by the lane identity.
  `git log --format='%an <%ae> %H %s' -- .ufo/reports/round-50/kake.md` prints
  `kake-shokunin <kake@shokunin.local> 47e235a51334cd9c641180d5466415dabc78fc22 round-50: kake report (misroot list correction)`
  and `kake-shokunin <kake@shokunin.local> f546bfc076046bd27d70c7efa5672611b8875bf5 round-50: kake report`.
  `git merge-base --is-ancestor` holds for **both** hashes against fleet `HEAD`
  (`40e55ebd1384c51d43caff58447ff1d9a8beb0f1`). No swept or orphaned report.
- The report is a real report, not a marker: Work performed, Landed changes, Before → after
  measurements, Sources & frontier, Trend verdicts, and a `## SHONEN` heading with one line per
  box (four lines: `[~]`, `[ ]`, `[~]`, `[~]`). No `[x]` is written by the lane; `SHONEN.md` in the
  lane is byte-unchanged from the base (`git diff 9619af67… 1c7f0769… -- SHONEN.md` is empty) and
  still holds the canonical four-box seed.
- Every cited lane commit exists and is an ancestor of the lane branch `master`
  (`git merge-base --is-ancestor <hash> master` exits 0 for `33eec7f2`, `89096c38`, `dfb4a3f9`,
  `ff3f6ec`, `1c7f0769`). The chain is linear:
  `9619af67` → `33eec7f2` → `89096c38` → `dfb4a3f9` → `ff3f6ec` → `1c7f0769`.
- Push state: `scripts/hyaku/jj-lane.sh state` printed
  `state branch=master local=1c7f0769a838852971426a672936413fa50ef84f remote=1c7f0769a838852971426a672936413fa50ef84f ahead=0 behind=0 head=detached tracked=0 untracked=10`.
  `git -C …/kake-shokunin ls-remote origin refs/heads/master` prints `1c7f0769…`. Ancestry was
  tested against the branch ref `master`, never `@{u}` (HEAD is detached at the same commit).
- Prompt fidelity: `.ufo/prompts/kake-round-50.md` carries the round-level contract (mission/axes
  binding, 1–3 falsifiable claims with the lowest-axis rule and the stagnation nudge, the L2
  floor, commit-then-push, push scope, the L0 side channel) and the five child-lane items (report
  path `.ufo/reports/round-50/kake.md`, commit-before-report ordering, the `SHONEN` heading
  requirement, the commit-hash citation rule, the lane write scope). It quotes no L2 route map
  that could contradict `MISSION.md`.
- Append-only discipline holds in the lane: `git diff --numstat` base→tip gives `68 0 LOG.md` and
  `28 0 corpus/QUALITY.md` (appends only, no deletions). `corpus/SOURCES.md` changed by exactly
  one added line (the S286 row); no existing row cell changed.
- Dispatch/completion digest copied from `.ufo/watchdog.log` (the log itself is mutable; this
  digest is the pointer):
  `2026-10-24T21:49:51-03:00 launch kake round=50 pgid=3258694 driver=hyaku-inline attempt=1`;
  `2026-10-24T22:58:43-03:00 complete kake round=50; hyaku-inline attempt=1`.
  The report landed last: lane tip `1c7f0769` is dated 2026-10-24 22:54:33 -0300, the report
  commit `47e235a5` follows it.
- No other mission of this lane is open; nothing stale. No tool was installed this round, so no
  entry is owed under `/home/vgpnk/.omp/agent/RULES.md`; this closure installed nothing either.

### Uncommitted paths (classified, not swept)

`git status --porcelain` in the lane prints exactly **10** paths, no tracked path modified
(`tracked=0`). They are the eight `round-46/residual/` reports and the nine `>1MiB` round-48
validate copies, and they are named as deliberately untouched in committed lane evidence
(`corpus/lessons/round-49-verifier-spotcheck.md`, §routed defect 3, and the round-50 `LOG.md`
block "Uncommitted, left untouched"):

1. `.ufo/waves/round-46/residual/` — one porcelain path holding **eight** orchestrator-owned
   residual reports (`CriticCitationOverreach.md`, `CriticMatrixBlindness.md`,
   `MutationSemanticsGap.md`, `ReviewQualityCriterion.md`, `ReviewReceiptIdentity.md`,
   `ReviewWitnessOracle.md`, `ScoutSiblingOverlap.md`, `SentinelBounds.md`), mtimes 2026-10-24
   03:26–03:37 -0300, before this round's launch.
2–10. Nine untracked copies under `.ufo/waves/round-48/assimilation/validate/`, each larger than
   1 MiB (1048576 bytes): `round-21/anchors-fixed.json` 2,355,487 · `round-36/realrun/snap-bodies-run2.tar.xz`
   1,808,836 · `round-36/realrun/snap-bodies.tar.xz` 1,811,344 · `round-37/sealed/cases.json` 2,777,011 ·
   `round-39/sources/xmlschema11-2.html` 1,508,774 · `round-40/sources/xmlschema11-2.html` 1,508,774 ·
   `round-41/realrun/sitemaps/nodejs.xml` 1,652,267 · `round-41/realrun/sitemaps/postgresql.xml` 4,620,210 ·
   `round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py` 1,283,159.

Nothing was edited, staged, force-added or swept. These are the same 10 paths the driver verify
warned about, they are inherited orchestrator/large-file artifacts, not r50 round work, and the
lane's own `LOG.md` names them as deliberately untouched.

## Claims (re-measured by this reviewer)

Both claims are the lane's own counting commands over committed bytes. They were re-executed
here (read-only: `git show` / `git merge-base --is-ancestor`, no worktree writes), and every
predicate was **independently re-derived** with this reviewer's own script
(`/tmp/kake_r50_verify/independent_check.py`, own `classify()`, own ancestry and own registry
parse) so no verdict rests on the lane's instrument alone.

### C1 — freshness (capability acquisition) — re-measured, **improved**

Predicate `met: classed == 3 of 3 declared ids` over S273, S274, S286.
`python3 -B .ufo/waves/round-50/c50_quote_class.py --root . --revision <commit>`

| Revision | Observed | Exit |
|---|---|---|
| base `9619af67` | `C1 classed 0/3 met=False` (ledger absent, lesson absent; S286 also retained blob absent, no live registry row, entry absent) | 1 |
| pre-append `33eec7f2` | `C1 classed 0/3 met=False` (lesson absent; S286 also no live registry row, entry absent) | 1 |
| measured `ff3f6ec` | `C1 classed 3/3 met=True`, all three ids `all rules hold` | 0 |
| tip `1c7f0769` | `C1 classed 3/3 met=True`, all three ids `all rules hold` | 0 |

Do-nothing controls hold at the base and at the pre-append mirror: the predicate cannot be
reached without the round's work.

Independent re-derivation (my own `classify()` over the committed blobs):

- S273 — quote 21 tokens, in the collapsed text, **not** in the raw HTML → derived
  `collapsed-only`. Ledger `matchClass` = `collapsed-only`, both sha256 pins match the committed
  blobs, the lesson carries `S273 quote class is collapsed-only` and does **not** carry the
  opposite sentence.
- S274 — quote 10 tokens, in the collapsed text **and** in the raw HTML → derived
  `raw-substring`. Ledger `matchClass` = `raw-substring`, pins match, lesson carries
  `S274 quote class is raw-substring`, no opposite sentence.
- S286 — quote 15 tokens, in both blobs → derived `raw-substring`. Ledger `matchClass` =
  `raw-substring`, pins match, lesson carries `S286 quote class is raw-substring`, no opposite
  sentence. The lesson's Gate quote equals the frozen quote exactly and is 15 tokens (contract
  6–25).
- S286 live registry row (my own parse of the committed `corpus/SOURCES.md`): `status=mined`,
  `opened=2026-10-24`, `recheck=180d`, `used-by=corpus/knowledge/crawl-error-status-table.md`
  (exactly that one path). The entry cites S286 below its 8-line header.
- Swap-label failure: `.ufo/waves/round-50/verification/blur-control.txt` records derived
  `raw-substring`, swapped `collapsed-only`, `swapped_equals_derived=False`. The control can fail.
- The counter reads committed bytes only (`git show`); it opens no worktree artifact.

### C2 — operability — re-measured, **improved**

Predicate `met: durable == 1 of 1`.
`python3 -B .ufo/waves/round-50/c50_durable.py --root . --revision <commit>`

| Revision | Observed | Exit |
|---|---|---|
| base `9619af67` | `C2 durable 0/1 met=False` (order proof absent, wave-cite proof absent, LOG does not cite the wave, settlement absent) | 1 |
| pre-append `33eec7f2` | `C2 durable 0/1 met=False` | 1 |
| measured `ff3f6ec` | `C2 durable 1/1 met=True` | 0 |
| tip `1c7f0769` | `C2 durable 1/1 met=True` | 0 |

Independent re-derivation (my own ancestry checks and committed-blob reads):

- `order-proof.json` names `pre_rev = 33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1` and
  `adopted_ids = ["S286"]`. `wave-cite-proof.json` names
  `grant_rev = 89096c387622785af59312bd2ee3b169202f1d4e`.
- **Order proven from ancestry**: `33eec7f2` is a strict ancestor of `ff3f6ec`; `89096c38` is a
  strict ancestor of `ff3f6ec`; `89096c38` is distinct from `33eec7f2`; and `33eec7f2` is an
  ancestor of `89096c38`. The mirror therefore lands before the grant, and the grant before the
  append.
- The live registry at `33eec7f2` has **no** S286 row; the mirror at `33eec7f2` **has** it; the
  live registry at `ff3f6ec` **has** it. Registry row count 142 → 143, and the base→tip diff of
  `corpus/SOURCES.md` is exactly one added line.
- Census argv blob at `33eec7f2` is
  `…/sources-census.sh validate --file …/pre-append/corpus/SOURCES.md` — contains `--file` and
  the mirror path, does **not** contain `--root`. Exit blob is `0`; stdout has no `E03` and no
  `E04`. Validate-before-append holds.
- At `89096c38`: `wave-grant.txt` is exactly one non-blank line,
  `granted lane=kake wave=r50-w1 seats=36 live=54 pending=0 cap=256` (seats in 32..64);
  `dispatch-command.txt` contains `kimi` and `--prompt` and does not contain `--auto`; and
  `LOG.md` at that revision does **not** contain `r50-w1`. At `ff3f6ec` the LOG **does** cite
  `r50-w1` and cites the grant commit hash. The LOG therefore cites the wave only after the
  grant exists.
- `settlement.json` at `ff3f6ec`: `spawn = 36`, `replacements = []`.

## Wave reconciliation (from committed registries and grant/dispatch bytes, not prose)

`git show 1c7f0769:.ufo/waves/round-50/settlement.json`:

- one v1 wave, `spawn 36`, `timeout_seconds 300`, `replacements []`;
- `settled_count 24`, every settled seat `exit 0`; `dead_count 12`, every dead seat `exit 124`,
  `reason timeout-300s` (the twelve: ScribeGateQuotes, ScribeRowShape, ScribeLessonShape,
  ScribeConsider, ReviewClassLedger, ReviewOrderProof, ReviewEntryCite, ReviewReportContract,
  ReviewShonen, RevengerR49, RevengerR48, SimplifierCounters) — killed, **not** replaced;
- `reports_written 25`. Independently counted: `git ls-tree --name-only 1c7f0769 .ufo/waves/round-50/w1/ | grep -c '\.md$'` = **25**
  (24 settled seats with a report, plus `ScribeRowShape`, a killed seat that still wrote one).
  All five critic seats and all four mutation-tester seats returned.
- role mix from the same receipt: scout 5, executor 6, scribe 4, reviewer 5, critic 5,
  mutation-tester 4, sentinel 3, revenger 2, connector 1, simplifier 1 = 36. Strict attack
  (reviewer + critic + mutation-tester) = **14 of 36** (38.9 %).
- grant bytes: `granted lane=kake wave=r50-w1 seats=36 live=54 pending=0 cap=256` at
  `89096c38`; dispatch command is the `kimi --prompt` batch, one prompt per seat, no `--auto`.

**Minor, status-neutral defect.** The report's Waves paragraph states "25 at settlement, 26
present when this report was written (one seat's file landed after the settlement snapshot)". The
committed tree at the tip and the current working tree both hold exactly **25** seat reports
(`git ls-tree … .ufo/waves/round-50/w1/` = 25; `ls .ufo/waves/round-50/w1/*.md | wc -l` = 25;
`git status --porcelain` shows no untracked `w1/` file). The 26th file is not present in any
committed byte or in the worktree, so the "26" figure is not re-derivable. The settlement's own
`reports_written = 25` is right.

## Discernment spot-check (LEARNING.md — checked from outside)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S286 (round-50 admit) | admit | `https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors` — live GET, HTTP 200, 193,275 bytes (identical to the lane's recorded figures) | **agree** | The 15-word span "Googlebot will scale back its crawling if it detects that your servers are having trouble" is a **raw substring** of the freshly fetched body, so the row's `raw-substring` class and the entry's claim hold live, not only against the retained blob. The row's teach-quote is 13 words (≤ 25). Row normalisation verified: `mined`, opened `2026-10-24`, recheck `180d`, `used-by` exactly the one admitted entry; the staged prose recheck (`curl … \| grep -c 'scale back its crawling'`) is stripped and recorded in the lesson's Gate block; no literal or escaped pipe in any cell. |
| S259 Jekyll url/baseurl (staged reject) | reject | `https://jekyllrb.com/docs/configuration/options/` — live GET, HTTP 200, 40,569 bytes; and the held row S080 in the committed registry | **agree** | The source is live and openable, so this is not a dead-source reject: the ground is the duplicate-URL rule, and the row's URL is verbatim the URL already mined as S080 (`| S080 | Jekyll: Configuration Options — https://jekyllrb.com/docs/configuration/options/ |`). A second row would be an E04 duplicate URL in scope. The flip ("supersede S080 in place, no second row for that URL") is actionable. |
| S321 Ollama OpenAPI (staged reject) | reject | `https://raw.githubusercontent.com/ollama/ollama/main/docs/openapi.yaml` — live GET, HTTP 200, 87,348 bytes | **agree** | The document is the Ollama HTTP API spec (`openapi: 3.1.0`, `title: Ollama API`, `servers: url http://localhost:11434`) — local model serving, which kake `PROVINCE.md:41` assigns to kama ("`kama` owns local model-serving endpoints; kake owns remote web properties"). The staged ground line said the same. Scope reject, not a quality reject; the flip (operator amends kake's province, or kama releases the surface) is recorded. |
| 12 quarantine ids (S142, S143, S148, S154, S156, S161, S178, S184, S193, S194, S195, S206) | not adopted | committed `.ufo/waves/round-50/assimilation/quarantine-slice` | **agree** | The committed slice re-derives exactly those 12 ids (nine `payload-absent`, three "the cited source could not be fetched"), S286 is not in the slice, and none of the 12 was hand-checked this round, so the round-48 hand-check is not used as an adoption basis. The base→tip `corpus/SOURCES.md` diff is one added line (S286): no quarantine id was appended. |
| `considerthese/2026-10-24.md`, second unimplemented proposal (watch unmerged operator-save/WIP branches by tree diff, not ancestry) | mined, not edited | `remotes/origin/wip/operator-save-20261023` | **agree** | The pointer opens: `git rev-parse remotes/origin/wip/operator-save-20261023` = `e80f84ddb84f4120cf62128c32498edc30db38bc` (the recorded hash); `git merge-base --is-ancestor <that> master` exits 1 (not merged); the tree diff against `master` is non-empty and its stat shows **4 insertions**, matching the lesson's "4 lines are in that commit and not in `master`". The branch was neither merged nor deleted, and `git status --porcelain -- considerthese/` is empty: the proposal file was mined, not edited. |
| Row-shape guard (able-to-fail) | control | `.ufo/waves/round-50/assimilation/guard/guard-collisions`, `guard-col0` | **agree** | `guard-collisions` is non-empty (contains `S286`) on the indented-row fixture while the column-zero-only fixture `guard-col0` is empty — the guard is shown able to fail, and the staged ids overlapping the registry are S273 and S274 only. |

Census re-run by this reviewer:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
→ exit 0, `kake ok`, over 143 rows, with the same twelve `W04` cross-scope duplicate-URL warnings
(S033, S088, S092, S098, S099, S102, S110, S111, S115, S116, S117, S127) as before the round and
as the report states. No `E03`/`E04`.

Newly written row re-opened: S286 (row 151 of the committed `corpus/SOURCES.md`) — its teach-quote
is 13 words and the anchor cell names the sentence it grounds; both re-opened and verified above.

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| freshness | **improved** | C1 re-measured: `classed 0/3` exit 1 at base `9619af67` and at pre-append `33eec7f2` → `classed 3/3` exit 0 at measured `ff3f6ec` and at tip `1c7f0769`, with the class derived (not asserted) from two sha256-pinned blobs and a committed swap-label control that fails. Independently re-derived by this reviewer. |
| operability | **improved** | C2 re-measured: `durable 0/1` exit 1 at base and at pre-append → `durable 1/1` exit 0 at measured and tip. The commit order is proven from ancestry (`33eec7f2` → `89096c38` → `ff3f6ec`), the mirror was census-validated with `--file` only before the append, and the LOG cites the wave only at a revision whose ancestor carries the grant. |
| depth | unchanged | No depth row changed; the round adds an instrument, not a wider evidence chain. |
| coverage | unchanged | Registry grew by exactly one row (142 → 143); the base→tip diff is one added line, no existing row changed. |
| calibration | unchanged | No calibration surface changed; the round's SHONEN assessment stays author-attested. |
| adjacency | unchanged | The cross-domain candidate (Ollama) was refused and reported, not absorbed; `PROVINCE.md` is unchanged by this round. |

No owned axis was harmed. `git diff 9619af67… 1c7f0769… -- SCORECARD.md` shows axis ratings staying
10 → 10, one new capabilities row (the quote-class ledger — a capability acquisition whose
demonstration runs in the round report), and the appended Round-50 declared-claims and
measured-results sections. No existing capability row was weakened.

## Trend verdicts

- **expansion: improved** — one admitted knowledge entry on ground the coverage map did not hold
  (`corpus/knowledge/crawl-error-status-table.md`, on the crawl-error status layer), grounded on a
  row opened and mined this round (S286, tier A docs), with the registry 142 → 143. The row's
  `used-by` is exactly that one entry, and the entry's `source:` cites S286.
- **quality: improved** — both do-nothing controls fail (C1 0/3 exit 1, C2 0/1 exit 1) and both
  predicates pass only after the claimed work landed; the class ledger pins both blobs by sha256
  and derives the class from the blobs, and the committed swapped-label control
  (`blur-control.txt`: `swapped_equals_derived=False`) shows the check can fail; the order proof
  ties the append to a strict ancestor carrying the mirror and its `--file` census exit 0. No
  admitted entry failed its re-check: the S286 admit was re-opened live and holds.
- **discernment: improved** — two staged entries refused with a reason and an actionable flip,
  and this reviewer independently re-opened both and agrees with both refusals; the 12 quarantine
  ids were re-derived and none adopted without a fresh hand-check; the considerthese reflection
  was treated as a pointer and its target measured (branch hash, ancestry exit 1, 4-line tree
  diff) rather than believed; the guard that checks row shape was shown able to fail. No row was
  adopted on another round's hand-check.

## Routed defects (the lane must fix these next round)

1. **Report overstatement on the wave report count.** The report says 26 seat reports were present
   when it was written; committed bytes and the working tree both hold 25 (`reports_written 25`,
   `ls-tree` 25). Correct the figure in the next round's report — append-only, never a rewrite of
   the filed bytes (`PROTOCOL.md` §Evidence standard).
2. **Route-failure detail is prose-only.** The fallback is recorded in committed evidence
   (`.ufo/waves/round-50/route-map.json`: `connector`/`sentinel`/`executor`/`mutation-tester` →
   `devin/swe-2-max`, "own bucket unreachable on this substrate"), but the HTTP status codes that
   caused it — the `xai-oauth/grok-4.7-fast` **403** (out of credits) and the
   `commandcode/deepseek/…` **402**/unconfigured bucket — appear only in the lane report's prose,
   never in a committed artifact. Commit the probe receipts (status code + body excerpt) next time
   a route is substituted, so the deviation is re-derivable without the report.
3. **No aggregate round-overrun figure is named in committed evidence.** The `KeyError: 'role'`
   dispatcher defect *is* recorded in committed bytes (`LOG.md` round-50 block: "exited in 0.08 s
   with `KeyError: 'role'` and launched no seat"), with the fix at `dfb4a3f9` before the wave
   launched. The overrun is not. The supportable figures this reviewer measured are: driver
   launch→complete = 4,132 s = **68.87 min** (21:49:51 → 22:58:43); wave wall-clock =
   `wave-grant.txt` 22:41:53.898 → `settlement.json` 22:48:51.935 = 417.0 s = **6.95 min**;
   dead-seat time = 12 × 300 s = **3,600 seat-seconds**; aggregate seat time = **7,088 s = 118.13
   seat-minutes**. No "~185-minute" figure is derivable from committed bytes or from the driver
   digest, and the two numbers that do add up to ≈187 min (68.87 wall + 118.13 seat) double-count
   concurrent seat time. Name the overrun measure and its counting command in the next round's
   report and `LOG.md`, so the ledger carries a figure a reader can re-derive.
4. **Keep the ten inherited paths untouched.** The eight `round-46/residual/` reports and the nine
   `>1MiB` `round-48/assimilation/validate/` copies are orchestrator/large-file artifacts, named as
   deliberately untouched in `LOG.md` and in the r48/r49 spot-checks. Do not force-add them to
   silence a `git status` warning; a >1 MiB add is skipped by jj's snapshot limit anyway.

## Operator note (not a lane duty)

`SHONEN.md` is not fully checkable by a non-author: box 2 is `[ ]` and boxes 1, 3 and 4 are the
lane's own `[~]`. The round's evidence does not obviously close box 2 — the lane executed its
frozen counters end to end, but no non-author checked an end-to-end domain task this round, and
the promotion decision is operator-owned. No `[x]` was written by this reviewer, and none was
written by the lane.

## Verdict

Every declared claim verifies against the lane tip by this reviewer's own measurement, no owned
axis is harmed, and the trend verdicts are `improved` on all three. Status `ok`, admitted `true`.
