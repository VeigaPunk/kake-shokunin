# Round 23 — ScribeLessonDraft (author-side, not admission)

Scope: draft prose for `corpus/lessons/round-23.md` sections `## Claims` and `## Gate`,
following the round-22 lesson's structure. Measured numbers are `<TBD>`. No lesson file,
receipt, live/ snapshot, or product file was written; this report is the only file
produced. Author-side; independent admission belongs to the non-author closure.

Observed lane HEAD during this draft: `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`
(history: `6847479` freeze → `4d95d2e` candidate code → `4e7dd1d` routed round-22 fixes).
My probes used a scratch clone (`/tmp/kake-r23-ScribeLessonDraft-lqwE/clone`) and scratch
copies of the stored snapshot bytes; nothing was written to the lane.

## Verdict

Draft delivered below. It is **not ready to be landed as written**, for three reasons the
Gate section must disclose rather than hide:

1. The candidate validator change (`4d95d2e`) breaks the round-22 frozen replay at HEAD
   (exit 2, `snapshot_tampered`) because round-22 pins the validator digest to `5de32200…`.
2. The C2 snapshot/audit receipts do not exist at any committed revision (`live/` is
   untracked), and the existing `live/*/audit.json` files were produced by the base
   validator; four served surfaces flip verdict under the candidate validator.
3. No C1 receipt exists; both counters are at 0 and exit 1 at HEAD.

Freshness observations (candidate, not yet receipts): `plazir27.kimi.page` is now 404
against a SKILL.md row that says it serves; `lucario` GHP and `ds4cc.kimi.page` serve pages
with no `rel=canonical` against property-map claims that they are canonical or declare a
primary. Each needs a unit receipt before any STALE is recorded.

## Findings

### F1 — P1 — Round-22 frozen replay regresses at the candidate and HEAD

Impacted claim: operability (C2 depends on the revision's validator being the pinned,
reproducible one); round-22 Gate evidence named in SKILL.md:411 (`frozen/expected.json`).

Validator digests:
```text
git show b5d599e:scripts/canonical_audit.py | sha256sum  → 5de32200ea409349659180ab93d02d273c113008596d93834da94ef1c04a1c15
git show 4d95d2e:scripts/canonical_audit.py | sha256sum  → d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac
git show HEAD:scripts/canonical_audit.py | sha256sum      → d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac
git show HEAD:.ufo/waves/round-22/frozen/expected.json   → line 74: "scripts/canonical_audit.py": "5de32200ea409349659180ab93d02d273c113008596d93834da94ef1c04a1c15"
```

Replay, scratch clone:
```text
git checkout b539cc17c25e5f42fe8803e2aa42b4574c4b44c6 && python3 .ufo/waves/round-22/replay.py --root .
  → exit 0; "verdict": "clean", "id": "frozen_replay_match", "inputsVerified": 69, "casesCompared": 32

git checkout 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc && python3 .ufo/waves/round-22/replay.py --root .
  → exit 2; {"verdict": "could-not-evaluate", "id": "snapshot_tampered", "error": "snapshot member digest mismatch"}

git checkout 4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b && python3 .ufo/waves/round-22/replay.py --root .
  → exit 2; {"verdict": "could-not-evaluate", "id": "snapshot_tampered", "error": "snapshot member digest mismatch"}
```

Not regressed (held): round-22 `measure.py` at HEAD → exit 0, `"accepted": 32` (its
PINNED_INSTRUMENT list covers matrix.py/cases.json only); `canonical_audit.py --selftest`
at HEAD → exit 0, `"passed": true`, zero `"ok": false` rows.

Smallest fix (L1 decision, not made here): either append a named round-23 correction that
re-pins `frozen/expected.json` validator digest to `d8acf750…` while keeping `5de32200…`
recorded as the round-22 historical pin, or retire the replay pin with the same disclosure.
Do not silently overwrite the round-22 pin. Gate row at SKILL.md:411 must name whichever
pin is current.

### F2 — P1 — C2 receipts are not reproducible at any committed revision

Impacted claim: C2 operability ("every surface has a committed read-only snapshot and an
audit receipt that the counter reproduces by re-running the revision's validator").

```text
git ls-tree -r --name-only HEAD .ufo/waves/round-23/live   → (empty)
git ls-tree -r --name-only 4d95d2e .ufo/waves/round-23     → c1-population.json census-before.txt contract.json measure_c1.py measure_c2.py c2-population.json (no live/)
python3 .ufo/waves/round-23/measure_c2.py --root . --revision 4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b
  → exit 1; "accepted": 0; every surface "problems": ["fetch.json or audit.json missing"]
```

Worse: the existing working-tree `live/<id>/audit.json` files reflect the base validator.
Re-running each stored `page.html` with its `manifest.json` in a scratch directory:

```text
surface              base 5de32200 (b5d599e)                     candidate d8acf750 (4d95d2e/HEAD)
ds4cc-primary        could-not-evaluate / html_unsupported  exit 2   clean  exit 0
plazir15-ghp         could-not-evaluate / html_unsupported  exit 2   clean  exit 0
ds4cc-kimi           could-not-evaluate / html_unsupported  exit 2   failed-policy / canonical_missing  exit 1
burnerchrome-kimi    could-not-evaluate / html_unsupported  exit 2   failed-policy / canonical_missing  exit 1
charter-ghp          clean  exit 0                                   clean  exit 0
lucario-ghp          failed-policy / canonical_missing  exit 1       same
vault-index-kimi     failed-policy / canonical_missing  exit 1       same
ufo-fsd-kimi-pro     failed-policy / canonical_missing  exit 1       same
```

Served-but-not-evaluated pages: `ds4cc-primary/page.html` contains
`<link rel="canonical" href="https://ds4cc.com/" />` (self-closed void tag). The candidate
commit message names exactly this change ("void self-closing tags", body-only SVG/MathML);
the causal link is [INFERENCE] from that message plus the base/candidate probe split, not
separately bisected.

Not served (fetch.json status 404): `plazir27-kimi` (2026-10-21T06:33:10Z), `lucario-kimi`,
`plazir15-kimi`, `charter-kimi`. These record `not-served` with no page.html, as the contract
allows.

Smallest fix: regenerate every `live/<id>/audit.json` with the lesson revision's validator
(`canonical_audit.py --manifest live/<id>/manifest.json --json`, run at that revision), commit
`live/<id>/{fetch.json,page.html,manifest.json,audit.json}` for all 12 surfaces, and only then
run `measure_c2.py --revision <commit>`. Do not describe the four base-validator
could-not-evaluate results as the candidate's outcome.

### F3 — P2 — C1 has no receipts; the counter is 0/17 at HEAD

Impacted claim: C1 freshness.

```text
python3 .ufo/waves/round-23/measure_c1.py --root . --revision 4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b
  → exit 1; "accepted": 0; "total": 17; each unit "problems": ["receipt missing"]
ls .ufo/waves/round-23/ → no receipts/ directory; no "## Live re-verification — round 23" heading in any unit (grep of corpus/knowledge: none)
```

This is pre-work, not a defect, but it means the draft's C1 numbers stay `<TBD>` and no unit
may be described as re-verified in the lesson.

### F4 — P2 — Candidate freshness observations the property map and unit receipts must address

Observed from stored snapshot bytes (fetch 2026-10-21, candidate validator). These are
candidates for STALE/HOLD in receipts; none is a recorded verdict yet.

- `plazir27.kimi.page` — `fetch.json` `"status": 404`, `fetchedAt 2026-10-21T06:33:10Z`.
  SKILL.md:22 says "canonical kimi charter mirror (stale: serves 09-18 beat, canonical 09-28)".
  Candidate: the stated serving claim is not live now.
- `lucario` GHP `https://veigapunk.github.io/lucario/` — `status 200`, 3435 bytes,
  `grep -c -i 'rel=.\{0,2\}"\?canonical' page.html` → 0; validator `canonical_missing`/exit 1.
  SKILL.md:26 says "live 200, verified 09-28" and c2-population says "lucario GHP is
  canonical". The liveness part holds; the canonical-declaration part is contradicted by bytes.
- `ds4cc.kimi.page` — `status 200`, 74641 bytes, no canonical link; validator
  `canonical_missing`/exit 1 against expected `https://ds4cc.com/`. SKILL.md:19 already
  marks this row STALE (~Aug-29 vintage).
- `ufo-fsd.kimi.pro` — `status 200`, `bytes 612`, no canonical; SKILL.md:23 "612B SPA shell"
  HOLDs on size. No canonical claim exists in the map, so the policy finding is informational.
- `burnerchrome.kimi.page` and `veigapunk.kimi.page` — 200, no canonical; validator
  `canonical_missing`. Policy basis is self-canonical; no map claim asserts a canonical.

### F5 — P3 — Round-22 routed items: status at HEAD

Verified by read at HEAD:
- Predicate correction appended: `corpus/QUALITY.md` lines 123–125 name the inverted
  `postfix/counter-probe.py` predicate (round-22 note 1) — landed in `4e7dd1d`.
- Misroot relocated: `.ufo/waves/round-22/residual/misroot/err.txt` (2119 bytes) and
  `out.txt` (64 bytes) present; no `err.txt`/`out.txt` at the lane root (`ls` →
  no such file). Byte-equality to `d5a0369` not checked.
- Carried, unchanged: paths gate red (3 targets, missSet 55) — operator-owned; SHONEN not
  promoted; `postfix/REPRODUCE.md` (17 lines) added — content not reviewed.

### F6 — P3 — Limits of this draft's own checks

No live network request was made by this draft; all candidate verdicts come from scratch
copies of stored `page.html` bytes at fetch time. `scripts/live_snapshot.py` was not reviewed
for read-only behavior (out of scope; a reviewer seat should). The four "could-not-evaluate
→ clean/failed-policy" flips are a probe result, not a counter result, until the audit
receipts are regenerated and `measure_c2.py` reproduces them.

## Draft prose — `corpus/lessons/round-23.md`

Measured numbers are `<TBD>`. Round-22 structure: date/baseline line, `## Claims`, `## Gate`.

```markdown
Date: 2026-10-21. Baseline master: `b5d599e19bead54b96f589444e9ec64cdf67c28a`.
Candidate code commit: `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`. Round lane HEAD at
authoring: `<TBD: final commit>`.

## Claims

C1, freshness: live re-verification of the 16 historical knowledge entries that
self-declare historical-not-live-reverified at base, plus the SKILL.md property map
(re-probed 2026-09-28 before this round). Before: 0/17 units carry a round-23 receipt
(`measure-c1-before.json` at `6847479`: accepted 0, total 17). After: every unit carries a
receipt whose claim rows each name a live surface, an observation, an `observedAt` date and
a verdict of HOLD, STALE or UNVERIFIABLE. Each STALE correction appears verbatim under
`## Live re-verification — round 23` in the unit; each anchor is a substring of the unit at
base. Measured: `<TBD>`/17 units pass; verdicts HOLD `<TBD>`, STALE `<TBD>`,
UNVERIFIABLE `<TBD>` (each UNVERIFIABLE carries a reason). A HOLD is an observation at
2026-10-21, not a guarantee of current state. Freshness is the axis this round moves.

C2, operability: first end-to-end canonical-policy preflight over the 12 owned public
surfaces in `c2-population.json` (`app.ds4cc.com/mcp` excluded as an API endpoint). The
policy is local publisher policy: one head canonical equal to the surface's expected
canonical; mirrors declare their primary. Before: 0/12 surfaces have a reproducible receipt
(`measure-c2-before.json` at `6847479`: accepted 0, total 12). After: every surface has a
committed read-only snapshot (`fetch.json` metadata and a `page.html` digest) and an audit
receipt that `measure_c2.py` reproduces by re-running the revision's `canonical_audit.py`;
non-served surfaces record their status with no stored page. Measured: `<TBD>`/12 reproduce;
served `<TBD>`, not-served `<TBD>`; verdicts clean `<TBD>`, failed-policy `<TBD>`,
could-not-evaluate `<TBD>`, not-served `<TBD>`.

"Clean" in C2 means the served head canonical matches the local policy. It does not mean
Google selected that canonical, that the page is indexed, that the publication is ready,
or that the snapshot describes the deployment after 2026-10-21. No browser, JavaScript,
headers, redirects, or write action is part of either claim.

## Gate

Candidates: the frozen round-23 contract and populations (`c1-population.json` sha256
`ffc9b3a4…`, `c2-population.json` sha256 `ac58c80f…`, both matching the pins in the
counters), `measure_c1.py`, `measure_c2.py`, `scripts/live_snapshot.py` and
`scripts/canonical_audit.py` at `4d95d2e`, the 12 live snapshots, and the SKILL.md property
map. Author-side implementation and rejection decisions are recorded here; independent
admission belongs to the orchestrator's non-author closure, never this lane's author seats.

Validator change disclosed: `4d95d2e` changes `scripts/canonical_audit.py` from sha256
`5de32200…` to `d8acf750…` (body-only SVG/MathML evaluation; void self-closing tags after a
closed head). Consequence 1: the round-22 frozen replay pinned to `5de32200…` does not verify
at this revision: `python3 .ufo/waves/round-22/replay.py --root .` exits 2 with
`snapshot_tampered`; it exited 0 at `b539cc1` (`frozen_replay_match`, 69 inputs, 32 cases).
Round-22 `measure.py` stays at 32/32 and the selftest passes. Resolution: `<TBD: named
re-pin or retirement, with the commit that carries it>`. Consequence 2: the four served
surfaces that the base validator could not evaluate now return clean or failed-policy;
their audit receipts must be regenerated with the revision's validator, not reused. Result:
`<TBD>`.

Rejected scope: changing the round-22 pin without a named correction; treating
could-not-evaluate as clean; calling an HTML-policy match search-engine selection or live
freshness; treating a snapshot's bytes as the deployment at any later date; crediting an
unreceipted unit as re-verified; any POST, publish, auth, DNS, or domain-tree edit; altering
the population or the 12 surfaces to fit the result.

Sources: C1 and C2 cite live surfaces and local files, not new S-rows. `<TBD: any new
SOURCES.md rows added for unit receipts, each re-opened with digest or quote>`.

Measurement: `python3 .ufo/waves/round-23/measure_c1.py --root . --revision <TBD commit>`
→ `<TBD>`. `python3 .ufo/waves/round-23/measure_c2.py --root . --revision <TBD commit>`
→ `<TBD>`. Baseline at `6847479`: C1 accepted 0/17 and C2 accepted 0/12. At `4e7dd1d` (the
probed HEAD): both exit 1, C1 `receipt missing` on all 17 units, C2
`fetch.json or audit.json missing` on all 12 because `live/` is not committed.

Carried debts, unchanged from round 22: paths gate red (3 targets, missSet 55), restore or
retire operator-owned; SHONEN not promoted by the author. Round-22 routed items: the
inverted QUALITY predicate and the misrooted `err.txt`/`out.txt` were corrected at
`4e7dd1d` (checked by read; byte-equality to `d5a0369` not checked).

Tool installs or updates in this round: `<TBD: none unless recorded>`.
```

## Checked and held

- Population digests equal the counter pins: `sha256sum c1-population.json` →
  `ffc9b3a44ee84ed827f3badc697f0ae5c8be007a50de3cafc2ccd23617697daf` (= `measure_c1.py`
  line 29); `sha256sum c2-population.json` → `ac58c80fda73cae194fcc75bf56f62b19ea5443048ddf822fcee8d08e7c75d98`
  (= `measure_c2.py` line 28).
- Contract "before" figures match the baseline receipts: `measure-c1-before.json` total 17,
  accepted 0; `measure-c2-before.json` total 12, accepted 0, `validatorSha256 5de32200…`.
- Base validator blob equals the round-22 pin `5de32200…`; base validator reproduces the
  stored `could-not-evaluate` results for the four surfaces in `live/*/audit.json`.
- Round-22 counter `measure.py --root . --revision <HEAD>` → exit 0, `"accepted": 32`.
- Round-22 replay at `b539cc1` → exit 0, `frozen_replay_match`, 69 inputs, 32 cases.
- `canonical_audit.py --selftest` at HEAD → exit 0, `"passed": true`, no `"ok": false`.
- Served surfaces with no canonical link (grep count 0): `lucario-ghp`, `ds4cc-kimi`,
  `burnerchrome-kimi`, `ufo-fsd-kimi-pro`, `vault-index-kimi`.
- No live network request, write, or publish was made by this draft; the only git commands
  were read-only (`rev-parse`, `log`, `show`, `ls-tree`, `cat-file`) plus `clone` into scratch.

## Limits

- Numbers in the lesson draft are `<TBD>` by instruction; the per-surface candidate verdicts
  above are probe results on stored bytes, not counter output.
- The causal link between `4d95d2e`'s void-tag change and the four flips is inferred from the
  commit message and the base/candidate split; it was not bisected.
- Did not verify whether `live/*/audit.json` were produced by base `b5d599e` specifically; the
  verdicts match base, which is the only evidence.
- Did not review `scripts/live_snapshot.py`, the round-22 `postfix/REPRODUCE.md`, or
  `census-before.txt`.
- Did not check whether `live/` is intentionally untracked or is pending a commit by the L1.
- Scratch artifacts: `/tmp/kake-r23-ScribeLessonDraft-lqwE/` (base and candidate validators,
  per-surface probe copies, scratch clone with replay/measure outputs). Not evidence unless
  re-derived at a committed revision.
- Tool installs or updates by this agent: none.
