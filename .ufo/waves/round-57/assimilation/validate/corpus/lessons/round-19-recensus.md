# round-19 re-census — §history suspend semantics repaired; selftest made hermetic

2026-10-14. Steered round 19. Advisory inventories:
`../.ufo/waves/shokunin12h-20261014-p1-repair/members/Kake*.md`.

## Landed change (one file)

`scripts/freshness-sweep.mjs`:

1. `pins.probeHistoryAbsent` now SUSPENDS **only the canonical** probe-history
   default when it is missing. An explicit `KAKE_PROBE_HISTORY` override that
   does not resolve stays fail-closed `exit 2`. The selftest rebind is gated on
   `KAKE_IN_SELFTEST=1` (set by the proof runner only), so an ambient
   `KAKE_SELFTEST_CANONICAL_HISTORY` cannot silence a real run.
2. `probeHistoryAbsent` joins the consumed-pin list, so it no longer renders
   under the "pins not evaluated" footer while simultaneously driving §history.
3. The selftest's hermetic resolve fixture no longer cites a live host project
   tree, and no longer writes persistent HOME state.

## Verdict lines (measured)

- `node scripts/freshness-sweep.mjs --selftest` → exit 0, **13/13 passed**
  (`e` region marks `B19,B1083,E1139,B1298,E1300,B1318,E1320`, 0 write sites
  outside the region).
- `node scripts/freshness-sweep.mjs --offline` → exit 0,
  `VERDICT: OK (exit 0, partial: offline)`; §history `SUSPENDED`
  (pin-declared), §armed `skipped(offline)`.
- `KAKE_PROBE_HISTORY=<missing>` → exit 2 (explicit bad override fails closed).
- No `$HOME/.kake-freshness-selftest-*` residue after the run (verified).

## Named debt (unchanged, correct)

Bare online `exit 1` stands: PQ-2 + PQ-14 ANOMALY (source repos gone) and
§history SUSPENDED. Do not re-pin to silence them. `~/Projects/ufo-fsd-alpha`
present; `origin-work` absent.

Stale live prose recorded, not rewritten in place: `SKILL.md:59`/`:111` still
name deleted webzites binaries; `freshness-sweep.md:43-53` copies pre-r18 pin
literals; `SCORECARD.md:20` says 14 `~/Projects` children where the receipt
measures 30 (P2b is informational by design).

## Independent audit erratum (appended 2026-10-14)

Independent audit: gates re-ran green (13/13, offline partial exit 0, explicit-bad exit 2, no HOME residue); identity/pathspec/record confirmed. Audit coverage finding: the selftest write-region opens on the line-19 header comment containing the BEGIN token, so a write planted as the first statement of a later function survives the confinement check (scratch mutant, not patched). Carried debt: PQ-2/PQ-14 + suspended history; stale webzites binaries; pre-r18 pin literals; SCORECARD 14-vs-30 children.

### Audit detail (appended 2026-10-14)

Historical-marking audit: describe-don't-pin does not hold for kake. Beyond the three sites the lesson named — `freshness-sweep.md:43-53` still quotes pre-r18 pin literals as the current baseline (`pathsMissSet` 10 vs 55; children 36 vs pin 14 vs live 30; live sha `fb365e38…` vs loaded `7c243a1d…`), `SCORECARD.md:20` says 14 `~/Projects` children where the live listing is 30, and `:85-87` + `SCORECARD.md:9` + the standing PQ-12/PQ-14 rows add further current-voice counts and hashes. No unmarked sentence asserts a sha256 of a missing local file as that file's current identity; `origin-repos.md:15` is already marked historical. Commit hashes of the missing checkouts (`a8f1e2b`, `c814526`, `bd02d10`, `e6bd071`) do not resolve locally and were not re-fetched. No pid pin. Inode `27238` and alpha HEAD `964f443e` still match. Owner kake; unblock: mark those lines historical and re-measure the pin literals.

### Dead-path sweep, lane-granular (appended 2026-10-14)

A lane-specific sweep (`.ufo/waves/shokunin12h-20261014-p1-audit/members/KakeDeadPathSweep.md`)
measures **77 live citations** of deleted paths at this revision — not the 8 the
fleet-level sweep reported, whose method was coarser. It also falsifies two claims
in this record: `SKILL.md:59`/`:111` are not the only stale live prose, and
`SCORECARD.md:22`'s "every `origin-work` cite is marked absent-historical" is false
— `keeper-timer-inert.md:91` and `publish-queue.md:167` are unmarked and
present-tense. The other 322 hits are marked-historical (65) or labelled (257);
unresolved: 0. Owner kake; unblock: mark those lines and correct the scorecard
sentence.

## Gate

Retrospective round-21 reconstruction, not original admission. The 2026-10-14 round recorded no gate section. This section is a label-only reconstruction from this lesson's own sections and later on-disk references. No live state was re-verified and no check was re-run.

Original sections cited: `Landed change` (lines 6-18), `Verdict lines (measured)` (20-29), `Named debt (unchanged, correct)` (31-35), stale-prose paragraph (37-40), `Independent audit erratum` (42-44), `Audit detail` (46-48), `Dead-path sweep, lane-granular` (50-60).

Later references: `corpus/lessons/round-20.md` Gate (41-60), Named debt (62-82), Round-20 resume C1-C3 (156-180), Gate — round-20 resume (182-196), Mistakes M4-M6 (252-254). Round-21 contract: `.ufo/waves/round-21/wave1-spec.json` (reportDir `.ufo/waves/round-21/w1`). No `corpus/lessons/round-21*.md` file was on disk at read time.

S019 metadata/gate contract (as stated in the round-21 wave spec, not as a located corpus entry): S019 is the metadata authority, not platform authority. `verified-at` names original evidence date and revision and says historical-not-live-reverified. A recheck gives a safe concrete local reading command and an operator restore-or-retire requirement where source vanished. Each entry retains entry-specific evidence. S019 was not found under `corpus/` at read time, and `CORPUS.md` was not on disk; the wave spec assigns its registration to L1. This section carries no `verified-at` field because it is a gate, not a knowledge entry.

### Candidates and historically supported outcomes

| # | Candidate (original section) | Outcome | Basis |
|---|---|---|---|
| C1 | `pins.probeHistoryAbsent` suspends only the canonical probe-history default; explicit bad `KAKE_PROBE_HISTORY` fails closed (Landed change 1) | admitted with qualification | Explicit-bad exit 2 measured (line 28). Round-20 carries §history forward as named debt, not reversed (`round-20.md:73-76`). Qualification: §history remains SUSPENDED; no explicit admit row for this change exists in round-19 or round-20. |
| C2 | Selftest rebind gated on `KAKE_IN_SELFTEST=1`; `probeHistoryAbsent` joins consumed pins; hermetic fixture with no live tree and no HOME writes (Landed change 2-3) | admitted with qualification | 13/13 and no HOME residue measured (lines 22, 29). Qualified by the confinement finding in C4 (`round-20.md:77-79`). |
| C3 | Verdict lines (lines 22-29) | unverified | Measured 2026-10-14 at that revision; not re-measured here; no outside check. |
| C4 | Selftest write-region opens on the header BEGIN token; planted writes in later functions survive (erratum, line 44) | admitted as finding; repaired in part downstream | Round-20 Mistake M4 and C2 (`round-20.md:165-174`, `:252`): standalone markers, 15 more write APIs, 25/25 planted mutants killed. Residual bypasses named: aliasing, bracket access, child-process writes. |
| C5 | Named debt: PQ-2/PQ-14 ANOMALY and §history SUSPENDED (lines 33-35) | carried, not closed | `round-20.md:73-76` names the same operator debt. |
| C6 | Stale live prose: `SKILL.md:59`/`:111`, `freshness-sweep.md:43-53`, `SCORECARD.md:20` (lines 37-40, 44-48) | carried, not closed | Count repair named debt, owner kake (`round-20.md:254`, M6); `SCORECARD.md:32` historical-qualified. |
| C7 | Dead-path population: 77 live citations vs 8 fleet-level hits (lines 50-60) | population-unit criterion admitted; 77/8 reconciliation carried | `corpus/QUALITY.md:18` cites `round-19-recensus.md:52-53` for the "population unit named" criterion; `round-20.md:253` (M5) names the 77/8 reconciliation as debt. |
| C8 | `SCORECARD.md:22` claim "every `origin-work` cite is marked" recorded as false (lines 57-60) | recorded as a mistake, not re-verified | `round-20.md:254` (M6). Unmarked `keeper-timer-inert.md:91` and `publish-queue.md:167` not re-read here. |

### Recorded refusal and actions not performed

- R1: re-pin PQ-2/PQ-14 or the §history pin to silence the bare online `exit 1`. Rejected: "Do not re-pin to silence them" (lines 33-34). Reason: named debt stands as correct.
- Not performed: the confinement flaw was not patched in round 19 (“scratch mutant, not patched”, line 44). No rejection decision or reason is recorded.
- Not performed: missing-checkout commit hashes were not re-fetched (line 48). This is not a candidate rejection.

Any other rejected candidate: not recorded.

### Outside spot-check

Not recorded for round 19. The in-file “Independent audit erratum” and “Audit detail” are advisory same-L1 reruns, not a non-author admit/reject spot-check. The original section names no author; round-21 GateTruth.md records the same-L1 provenance limit. The round-20 verifier file covers round 20 only.

### Gate completeness

Gaps: no admit or reject row was recorded at round 19 for C1-C2; no outside spot-check exists; C3 is unverified. The lesson's own audit recorded C6 and C8 as unmarked or stale; no repair for them is recorded in round 19. Nothing in this section changes the original sections.
