# kake round 70 — frozen contract (attempt 1)

Base: `e5f6fd9e4c243d092160bc74e8bea24256087173` (lane `master` tip at round open; `jj-lane.sh state`
local=remote, ahead=0 behind=0; `git status --porcelain` empty). This commit freezes both predicates
before any after-state measurement and before any seat runs.

Scores at open: calibration 2 (lowest owned non-retired axis), operability 10, freshness 10 (both
HOLD at the legacy ceiling). The stagnation nudge does not apply (calibration sits below the
saturation line), so the lowest-axis obligation binds and C1 works calibration.

Round-start census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
→ exit 0, 16 W04 duplicate-url warnings (S033, S088, S092, S098, S099, S102, S110, S111, S115,
S116, S117, S127, S416, S417, S427, S433), `kake ok` — unchanged from round 69. Full output pasted
in the report.

Two claims, one axis each, causally separable (C1 touches only SCORECARD.md and
`.ufo/waves/round-70/c70_pointer_audit.py`; C2 touches only `corpus/knowledge/`,
`corpus/SOURCES.md`, and the round-70 wave evidence; the shared files — LOG.md, SCORECARD.md round
section, the lesson — are L1-integrated bookkeeping, and each claim's counter runs without the
other's files). No exploratory claim. No capability row is claimed.

## C1 — calibration (2 → 2, HOLD). SCORECARD evidence pointers resolve at the measured revision or carry a dated calibration annotation.

Claim: every path-like evidence pointer in `SCORECARD.md` either resolves at the measured revision
(repo-relative pointers) or exists as host state at measurement time (`~/...`, `/tmp/...` pointers),
or is annotated as historical by the appended `## Pointer calibration (round 70)` section of
`SCORECARD.md`.

Predicate (identical sentence in this plan, the counter's code, and the receipt label): **C1 is met
iff `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <lane> --revision <rev>` prints
`unannotated=0` and exits 0.**

- Population (enumerated by the counter itself from the revision's `SCORECARD.md` bytes; no external
  input file): tokens of three classes —
  (a) repo-relative: `(?:^|[`(>|\s])((?:\.ufo|corpus|scripts|handoffs|considerthese)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]{1,7})`
  — dangling iff `git cat-file -e <rev>:<path>` fails;
  (b) home: `(?:^|[`(>|\s])(~/[A-Za-z0-9_./+-]+)` — dangling iff the expanded path does not exist on
  the measurement host (`test -e`);
  (c) tmp: `(?:^|[`(>|\s])(/tmp/[A-Za-z0-9_.+-]+)` — dangling iff the path does not exist.
  URLs (http/https), bare names without a path separator, and in-line `git`/`grep` command strings
  are not pointers. A token is counted once.
- Annotation locus: the section `## Pointer calibration (round 70)` of `SCORECARD.md` at
  `--revision`. A dangling pointer is annotated iff a table row in that section has the exact token
  as its first cell (same exact-token discipline as the round-69 correction rows; a token that is
  only a substring of another id or pointer annotates nothing).
- Annotation content duty (checked by review, not the counter): each row names the dated absence
  event class on record — the 2026-10-12 `~/Projects` W7 prune, the 2026-11-01 host migration, or
  scratch-discipline cleanup — and marks the record historical, not executable.
- Do-nothing control: the base revision `e5f6fd9e` run. Known motivating pointers on record at base
  (read from the committed SCORECARD this round): `/tmp/kake-r10` through `/tmp/kake-r18` (12
  tokens across the move-log rows 10–18), `~/DIRMAP.md`, and `~/Projects/...` and lowercase
  `~/projects` host-tree tokens. Kill rule: if the base already prints `unannotated=0` exit 0, the
  counter or the population is wrong and C1 lands `unprovable` with no credit.
- Junk control: a fixture SCORECARD whose pointers all resolve must print `met=true` exit 0.
- Attack controls baked into `--selftest` (fixture git repo under `--work`): (a) resolving repo
  pointer → counted, not dangling; (b) dangling repo pointer, no annotation → exit 1;
  (c) dangling tmp pointer annotated with the exact token → exit 0; (d) an annotation row whose
  first cell is a strict prefix of the dangling token must NOT annotate it → exit 1; (e) a file
  with no pointers → `pointers=0 met=true` exit 0. Selftest prints `selftest 5/5`.
- Boundary: C1 does not touch `corpus/lessons/round-66*.md`, `pins.pathsMissSet`, or any file the
  `--offline` sweep scans; the round-69 L0 question (line 260 of `.ufo/l0-questions.md`) stays open
  and unrouted-around-work is not claimed here. SKILL.md `/tmp` cites (spot-check routed item 2)
  are outside C1's population; the round reports why they are not fixed this round.

## C2 — freshness (10 → 10, HOLD). One staged `merge/kake` entry adopted, re-grounded against a live source this round.

Claim: the staged entry `crux-bigquery-origin-membership.md` (theme: key-free CrUX eligibility
routes) is adopted into `corpus/knowledge/` with every cited external source re-opened by this lane
in-round, and its registry row appended under the lane's next unused id.

Predicate (same sentence in plan, receipt, and report): **C2 is met iff all of**
(a) `corpus/knowledge/crux-bigquery-origin-membership.md` exists at the tip and opens with
`source:`, `verified-at:` (2026-11-03) and `recheck:` in its first five lines, with `source:`
naming the new `S###` id and the live URL `https://developer.chrome.com/docs/crux/bigquery`;
(b) exactly one new registry row for that id exists inside `## Registry` of `corpus/SOURCES.md`,
`status` `mined`, `opened` 2026-11-03, `used-by` naming the entry path, and the row parses as 13
awk fields with no literal or escaped pipe in any cell;
(c) the retained body of the re-opened source (`.ufo/waves/round-70/w1/ScoutSources/sources/`,
retained this round with a receipt: status, bytes, sha256, access date) contains the located quote
“The origin_summary table contains a list of all origins in the CrUX dataset” (class raw-substring
or collapsed-only, stated with the method; `absent` fails the claim);
(d) `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exits 0 at the tip.

- Do-nothing control: at base the entry file is absent and the id appears in `## Registry` zero
  times; both are the before measurement. A control that skips the adoption cannot create either.
- Re-grounding rule (CORPUS.md rule 1): the staged campaign `opened` date (2026-10-24) and quote
  prove nothing about this lane; the row's `opened` is this lane's access date, the quote is
  located in the body this lane retains, and the entry's Gate block carries the located quote with
  its position.
- Id collision rule (§10): staged id S352 collides with the lane registry's S352 (verify in
  scratch with the 0–3-leading-space extractor); the adopted id is the lane's next unused id
  (expected S438, decided by the committed `reg-ids`/`staged-ids`/`collisions` outputs, never by
  arithmetic). Renumber map pasted in the report.
- Row normalization rule (§10): no staged row is appended as-is — the staged `recheck` cell
  (“180d — `curl … \| grep …` -> 1 (ran 2026-10-24)”) is normalized to `180d`, and the stripped
  recheck prose is recorded in the round lesson's Gate block; no cell carries a literal or escaped
  pipe.
- Proof obligations, both before any append: (1) the id-collision guard is proven able to fail on a
  scratch fixture whose registry row carries two leading spaces (the indented-collision class from
  the operator's §10 contract); (2) the scratch mirror (lane `corpus/` copy + normalized append
  block + adopted entry at its repo-relative path) passes
  `sources-census.sh validate --file <mirror>/corpus/SOURCES.md` with exit 0 (warnings allowed) —
  an E03/E04 finding refuses the row.
- Gate duty (LEARNING.md): the round lesson's `## Gate` records ≥1 admit (the BigQuery entry, if it
  clears the gates) and ≥1 reject from the assimilation set with reasons and flip conditions. Named
  reject candidate: `crux-keyless-check.md` — its probe rows are campaign-session own-work
  observations (staged S303 companion S304) that would have to be re-run as new probes this round,
  and its Vis/eligibility surface overlaps the r28 held entry `field-performance-cwv.md` (S036–S039);
  flip: a round that re-runs both probes fresh and shows a publisher-side keyless surface not
  already held can adopt it. The critic/reviewer seats test both the overlap claim and the quote
  truth; the L1 gates on their evidence.
- Boundary: the register slice in
  `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` is not
  appended to (the kake r58 L0 question on adopting quarantine rows stays open); no campaign tool
  runs; shokuknow is read-only.

## Frontier step (child-lane duty, not a claim)

- SOURCES: expected registry 175 → 176 (one adopted row; collision-renumbered). Census before
  (recorded above) and after both exit 0.
- Mistake mining: M1 — self-assessment drift: SCORECARD evidence pointers name scratch paths (12
  `/tmp/kake-rNN` tokens, rounds 10–18) and host-tree paths that no round ever annotated;
  captured-by: none (the corpus append-only rules never covered SCORECARD, and the freshness sweep
  scans corpus files, not SCORECARD); fix: the C1 counter + the Pointer calibration section + a
  QUALITY criterion. Any further mistake the round produces is mined the same way.
- QUALITY addendum: one criterion per uncaught mistake, appended end-of-file, each with an
  able-to-fail command.

## Round shape

- W1: one v1 wave of 13 seats under `scripts/hyaku/ufo-wave-policy.json` (band 8–16): 3 scout,
  2 executor, 2 scribe, 1 reviewer, 1 critic, 1 mutation-tester, 1 labrat, 1 connector, 1 revenger.
  Attack share 4/13 ≈ 31 %. Connector seats 1. No planner seat (the L1 holds the planner role;
  the validator rejects it). No residual wave planned; round total 13.
- Routing: run-15 map via `task.agentModelOverrides` (never pass `model`).

## Write scope and discipline

- Writer seats (ExecC1Counter, ExecMirror) work in scratch clones under
  `/fast/scratch/hyaku/kake-r70/<SeatName>/` and deliver patch or new-file outputs into
  `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-70/<SeatName>/`. The integration
  owner (the L1) applies patches to the lane tree and commits through `jj-lane.sh` only.
- Non-writer seats write only new files under their own `.ufo/waves/round-70/<SeatName>/` directory
  and never edit tracked files.
- No seat commits, pushes, or runs a mutating git or jj command in the lane. No seat writes into the
  fleet root, `/home/vgpnk/Projects/shokunin/.scratch/`, `.ufo/state/`, other lanes, or any sibling
  repo. `/home/vgpnk/Projects/shokuknow` is read-only; no campaign tool runs there.
- Every scratch tree is removed on exit; `/tmp` only for files under 50 MB.
- Every scratch clone is created with `git clone --shared` and checked out at the base revision
  `e5f6fd9e4c243d092160bc74e8bea24256087173`; commits inside a scratch clone use
  `-c user.name=kake-seat -c user.email=seat@fixture` and never elsewhere.
