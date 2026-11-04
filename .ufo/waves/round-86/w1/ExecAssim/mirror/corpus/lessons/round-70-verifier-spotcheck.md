# round-70 verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-03
round: kake 70 · base `e5f6fd9e4c243d092160bc74e8bea24256087173` → tip `2c1a700d12c245b6cde82b251deaf1f8953bf241`
report: `.ufo/reports/round-70/kake.md` (fleet repo, committed `025141c7` by `kake-shokunin <kake@shokunin.local>`)

## Conformance (protocol step 1)

| Check | Result |
|---|---|
| Report committed by lane identity | PASS — `git log --format='%an <%ae> %H %ad' -- .ufo/reports/round-70/kake.md` → `kake-shokunin <kake@shokunin.local> 025141c72e563683727525b6284fc6ccf117a8f1 Tue Nov 3 17:29:20 2026 -03:00`; lands after the round's lane commits, before the driver `complete` line (17:31:00) |
| `SHONEN` heading, one line per box | PASS — `## SHONEN` + 4 lines (`[~]`, `[~]`, `[ ]`, `[~]`), matching the canonical 4 boxes; no self-written `[x]` |
| Cited commits exist and are ancestors | PASS — all 6 cited hashes + base `e5f6fd9e` are ancestors of `master` (`git merge-base --is-ancestor`, tested against the branch ref, not `@{u}`) |
| Lane clean and pushed | PASS — `jj-lane.sh state` → `local=remote=2c1a700d ahead=0 behind=0`; `git status --porcelain` empty |
| Dispatch evidence | PASS — watchdog lines match the digest below; prompt committed `61510243` |
| Prompt fidelity | PASS — `.ufo/prompts/kake-round-70.md` lines 1–140 render `templates/round-prompt.md` byte-faithfully (only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substituted); fleet template is identical to the canonical kimi-shokunin copy; hyaku addendum §6 follows; all five child-lane items and the round-level items present; axes bucket `operability + freshness` matches `MISSION.md:25` |
| Marker predicate | Real report — named claims, evidence pointers, landed commits with hashes, measurements; not a marker |

## Claim re-checks

### C1 — calibration (2 → 2, HOLD) — re-measured by the verifier

Independent re-implementation of the frozen predicate over committed bytes (token regexes and
dangling rules re-derived from the counter's committed docstring; not an execution of the lane's
counter):

```
python3 (own script): git show <rev>:SCORECARD.md, strip HTML comments, apply the three
token classes (repo/home/tmp), dedupe first-occurrence, repo-dangle iff both the literal
and os.path.normpath token fail `git cat-file -e <rev>:<tok>`; home/tmp-dangle iff
os.path.exists fails; annotation = calibration-section markdown table row (fences skipped);
append-only = base is a line-prefix of tip.
```

Observed:

- base `e5f6fd9e`: `pointers=348 dangling=17 annotated=0 unannotated=17` — red, matches
  `controls/c1-base-v2.txt` token-for-token (all 17 dangling tokens reproduced, including
  `~/Projects/plazir-15-site`, `~/DIRMAP.md`, `~/projects`, 12 × `/tmp/kake-rNN`, the two
  round-44 verification paths, `scripts/sources-census.sh`, `scripts/hyaku/ufo-wave-policy.json`,
  `.ufo/charter-scribe/ledger.jsonl`, `.ufo/l0-questions.md`).
- tip `2c1a700d`: `pointers=351 dangling=17 unannotated=0 append_only=True` — green, matches
  `controls/c1-tip-final.txt`. The verifier's `annotated=18` counts the table rows; the extra
  row is the declared host-independence row `/tmp/kake-r16` (not dangling, annotated anyway) —
  exactly the report's "17 exact-token rows + one host-independence row".
- Able-to-fail evidence verified from committed receipts (not re-executed):
  `controls/selftest-v2.txt` selftest 8/8; `controls/tip-attacks.txt` both mutants killed
  (row removed → exit 1; base line rewritten → `append_only=false` exit 1), run at `50ec1446`.
- `git diff e5f6fd9e 2c1a700d -- SCORECARD.md`: 62 insertions, 0 deletions; only two appended
  `##` sections (calibration + round-70 declared claims); no axis row touched.

Verdict: **improved** (predicate red→green, verified by independent re-measurement; score row
held at 2, which the report states).

### C2 — freshness (10 → 10, HOLD) — re-measured by the verifier

- base: `git show e5f6fd9e:corpus/knowledge/crux-bigquery-origin-membership.md` → path not in
  revision; `grep -cE '^\| *S438 *\|'` on base SOURCES.md → 0; registry rows 175.
- tip: entry present, opens with the provenance trio (`source: S438 — https://developer.chrome.com/docs/crux/bigquery — §…origin_summary`, `verified-at: 2026-11-03`, `recheck: 180d`); S438 row
  present exactly once (registry 175 → 176), 11 cells, status `mined`, opened 2026-11-03,
  recheck `180d`, used-by the entry, inside `## Registry`;
  `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0 (`kake ok`),
  same 16 pre-existing W04 duplicate-url warnings as the round's before/after receipts.
- Retained body re-derives: `sha256sum .ufo/waves/round-70/w1/ScoutSources/sources/S438-crux-bigquery.html`
  → `dd17ea8cb30ec89a…db420`, 110,697 B — matches the receipt.

Verdict: **improved** (entry absent at base, present at tip with live re-grounding; score held
at 10, which the report states).

### No axis harmed

SCORECARD base→tip is append-only (0 deletions); operability/depth/coverage/adjacency rows
byte-identical. All four grade **unchanged**.

## Trend verdicts (verifier-graded)

- **expansion: improved** — re-derived: base registry `grep -ci bigquery` → 0; tip adds the
  S438 row (176 total) cited by the new entry's `source:`; `corpus/README.md:82` coverage-map
  row and `:127` frontier ground-map row exist at tip.
- **quality: improved** — C1 predicate moved 17→0 unannotated with append-only proof
  (re-measured); counter able-to-fail (8/8 selftest, red base, two killed attacks — committed
  receipts); the round's one admitted entry re-grounded live 2026-11-03 and passed its re-check.
- **discernment: improved** — the outside spot-check below agrees with the gate on the sampled
  admits and rejects (`LEARNING.md` improved condition); the lane itself claimed only
  `unchanged`, deferring to this check.

## Spot-check table (LEARNING.md — ≥1 admit, ≥1 reject, ≥1 new SOURCES row re-opened)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| BigQuery origin-membership entry + S438 row | admit | `https://developer.chrome.com/docs/crux/bigquery` re-fetched 2026-11-03 (HTTP 200; canonical and og:url both equal the entry's source URL; live sha `797affa6…`, 110,693 B — live page churns vs the pinned GET; quotes checked against **both** bodies) | **agree** | Both raw ≤25-word blockquotes re-derive as raw substrings on the retained **and** live bodies ("a list of all origins included in the dataset" 8 w; "it is updated monthly with the latest list of origins in the dataset" 13 w); the C2(c) quote (13 w) re-derives exactly as the Gate disclosed — raw 0, collapsed 1 (tag-strip + whitespace collapse), method stated; anchor stamp "Last updated 2026-10-13 UTC" present in the retained body |
| `crux-keyless-check.md` (staged S303/S304 probes) | reject | lane registry at tip + held entry `corpus/knowledge/field-performance-cwv.md` | **agree** | S303 and S304 absent from the lane registry at tip (0/0) — admitting un-re-run session-own-work probes would break SOURCES rule 1 (a row is written only after opening the source in the writing round); the probe conflicts with the held policy line at `field-performance-cwv.md:142` ("no API call without an operator-provisioned one"); flip conditions recorded are concrete |
| Appending the 8 colliding staged rows (S312 S329 S367 S372 S373 S374 S390 S409) | reject | lane registry at tip | **agree** | All 8 ids already present exactly once; re-appending duplicates ids (census E03); the single-row adoption path (S438) is collision-free as claimed |
| S438 registry row (new SOURCES row) | row check | source re-opened (row 1 above) | **agree** | NF=13 (11 cells), no escaped pipe, tier A docs, status mined, opened 2026-11-03, recheck 180d, used-by the entry; census validate exit 0 |

## Routed defects / notes for next round (status-neutral)

1. **Attack-share counting** — the report counts 4/14 ≈ 28.6 % by including the revenger seat;
   the run-15 addendum's list is "(reviewer, critic, mutation-tester, labrat)", under which the
   strict count is 3/14 ≈ 21.4 %. The four adversarial roles present (reviewer, critic,
   mutation-tester, revenger) arguably satisfy the intent, and the wave-policy groups revenger
   with the thinking proposal roles, but the lane should either count strictly per the list or
   record the wider definition it uses, so closure does not re-litigate it. Cosmetic here (the
   band 8–16, ≤2 connectors, and role coverage all hold; no `model` passed).
2. Prompt axes gloss reads "(web properties and publishing)" against `MISSION.md`'s
   "(web properties)" — axis names match the bucket; cosmetic driver-substitution variance only.
3. Pre-existing, carried: the 16 W04 duplicate-url census warnings (unchanged before→after).
4. SHONEN box 3 stays `[ ]` with named residuals (`SKILL.md:95,356,359`, r69 citation debt) —
   correctly left unchecked; boxes are **not** all checkable, so no promotion signal from this
   verifier. Promotion remains operator-owned.
5. No red gate this round; no misplaced writes; scratch-discipline slip (a seat dir outliving
   its report, removed by the L1) is already recorded in the report.

Dispatch/complete digest copied from `.ufo/watchdog.log`:
`2026-11-03T16:21:45-03:00 launch kake round=70 pgid=3584047 driver=hyaku-inline attempt=1` /
`2026-11-03T17:31:00-03:00 complete kake round=70; hyaku-inline attempt=1`.
