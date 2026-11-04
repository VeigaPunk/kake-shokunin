# Round 66 — lessons (kake)

Round opened 2026-10-31 on the Windows host at base
`6a2ecb18f58dfa47492d38d736ee7c34b6eaa3c6` (round-65 verifier spot-check tip,
pushed). Work commit `a26fd6a57a3549a927b2e9fb589cf72813af2c24` (contract,
instruments, §paths re-pin, carry-in corrections, probes); settlement and
receipts follow it. Frozen contract:
`.ufo/waves/round-66/contract.md` (predicates frozen before the C1 instrument
existed and before the C2 repair was applied; amendment 1 recorded pre-data at
instrument-verification time).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| generated-code splice without a post-generation smoke gate (this round) | the c66 build script's ASSERT replacement omitted the `ASSERT = '''` delimiters and the docstring splice duplicated the shebang, leaving `sys.exit(0 if ok else 7)` at MODULE top level — the instrument exited 7 with empty stdout and empty stderr (receipt trail: no-arg invocation `E2=7` vs v1's usage-64; bisect over cumulative top-level statements pinned "FIRST FAILURE at top-level stmt 79") | the standing order "run `--selftest` (or no-arg usage) before trusting a rebuilt instrument"; a silent nonzero with NO traceback is structural, not a verdict | build scripts must append a compile+exec smoke assertion; and the round's reusable diagnostic is recorded: exec-cumulative-prefix bisect localizes a silent module-level death in one pass |
| Windows CreateProcess PATH asymmetry (this round, caught by the instrument's own selfcheck) | the D4 env selfcheck spawned bare `python3` with the alias dir first in the CHILD env and still got the Store stub (rc 9009, empty output): on Windows CreateProcess resolves a bare executable through the CALLING process's PATH, not the child env block; POSIX os.get_exec_path(env) resolves via the new env — v1's observation design silently relied on the POSIX behavior | the selfcheck failing closed (exit 2) on the first real run, exactly as designed | probes swap `os.environ["PATH"]` to the observation PATH and restore it; member inner spawns are unaffected (their caller IS the member process with the observation PATH) — documented in the instrument docstring |
| cross-platform key normalization missing in the sidecar mechanism (inherited-latent since round 24, inert since the 2026-10-30 migration) | `corpus/knowledge/freshness-sidecar.json` entries are validated forward-slash-only but looked up with `path.relative`'s host separators — all 30 standing entries invisible on Windows; surfaced as 3 drift tokens whose only annotations were sidecar entries + the two red selftest cases (`.ufo/waves/round-66/controls/selftest-before.txt`, 34/36) | the r65 sweep receipt's drift list naming exactly those sidecar-bound cites | lookup + cite display normalized to canonical forward slashes (POSIX-identical); selftest 36/36 (`.ufo/waves/round-66/controls/selftest-sweep-after.txt`) |
| c56_selftally's fixed-key child env blocks the UTF-8 pin (inherited, NOT repaired — frozen bytes) | c56_selftally builds its inner child env from a fixed key set, so the v2 observation's PYTHONUTF8=1 cannot reach its ten inner gate runs; observed this round as its e_T=2 (unparsable row) with the limit named in the contract before any data | contract §C1 "known frozen limit" clause, disclosed pre-data | carried; a repair would touch a frozen counter and belongs to the operator's calibration ruling (the row is carried in `corpus/knowledge/gate-status-ledger.md`, not normalized away) |
| report-prose counts without their counting command (r65 carry-in D1, corrected this round) | the round-65 report said "LOG +9 lines … lesson new +105"; numstat over `b783d18437db..a421769` gives LOG +10/0 and lesson +106/0 — re-measured this round: `git diff-tree --numstat b783d18437db..a4217696859deb49cde9ddca7a39d718b73503b1 -- LOG.md corpus/lessons/round-65.md` | the r65 non-author closure (defect D1) | corrected append-only here and in the round-66 report; every count in this round's artifacts carries its command |
| receipt-label contradicts its own recorded lines (r65 carry-in D2, corrected this round) | `.ufo/waves/round-65/controls/base-c1.txt` labeled the A4 block "c65-red/c64-green DIFFERENTIAL OK" while its own A4 lines record c64 met=false exit 1 (A4 is non-differential per the frozen r65 contract) | the r65 non-author closure (defect D2) | relabel appended to the file (append-only; the recorded lines untouched) with the counting command in the appended block |

## Gate

Candidates: (a) C1 host-evaluability of the 28-member gate registry;
(b) C2 §paths gate exit-0 restoration + sidecar host-path repair;
(c) re-adjudicating the 11 observed registry mismatches; (d) registering c66
in SKILL.md; (e) forcing or explaining away the mismatch rows.

- **Admit (a): calibration 2→2 HOLD (lowest owned non-retired axis).**
  Before: v1 at base prints `members=28 mismatches=28`, every member outside
  the family verdict alphabet (receipt
  `.ufo/waves/round-66/controls/c60-v1-base-r66.txt`, exit 1) — zero members
  adjudicable. After: v2 at `a26fd6a5` prints
  `members=28 evaluated=28 structural=0 agreement=17 scores_held=3/3 met=True`
  exit 0 (receipt `.ufo/waves/round-66/controls/after-c66.txt`; env line
  `python3=3.13.15 git=2.55.0.windows.3`); selftest 86/86
  (`.ufo/waves/round-66/controls/selftest-c66.txt`); v1→v2 diff confined to
  the five frozen deltas + amendment 1 + their direct selftest fixtures
  (`.ufo/waves/round-66/controls/c66-v1-v2-diff.txt`); do-nothing base has no
  instrument (`.ufo/waves/round-66/controls/donothing-c66-base.txt`, exit
  128). Counting command: `python -B .ufo/waves/round-66/
  c66_gate_status_hostportable.py --root . --revision <commit> --jobs 6`.
  The claim is EVALUABILITY: 0/28 comparable exits → 28/28 comparable exits.
  The 17/28 label agreement and the 11 observation-class mismatches are
  measured and reported as-is — this claim does not assert the registry's
  recorded statuses are correct, and no mismatch was forced or explained
  away. Sourced: S133 re-opened live this round (one GET, 2026-11-01T04:39Z,
  HTTP 200, 208,624B, sha256 `f98756fe…699c`; located quote, 11 words: "an
  exit status of 0 indicates that it ran successfully"; receipt
  `.ufo/waves/round-66/sources/receipt.json`); no registry row added or
  edited (171 rows).
- **Admit (b): freshness 10→10 HOLD.** Before: the standing §paths gate
  could-not-evaluate on this host (r65 receipt exit 1: 23 drift tokens with
  unannotated cites + 29 migration paths unpinned; this round's re-run at
  the same state: `.ufo/waves/round-66/controls/sweep-base-r66.txt`). After:
  `node scripts/freshness-sweep.mjs --offline` exits 0 — VERDICT: OK
  (partial: offline, as designed) — at the settlement worktree
  (`.ufo/waves/round-66/controls/sweep-after-r66.txt`) and again at the
  settlement tip (`.ufo/waves/round-66/controls/sweep-final-thishost.txt`),
  with drift 0 and newMissing 0. Mechanism, each receipted: the sidecar
  lookup host-path repair (selftest 34/36 → 36/36, no case removed); 144
  line-bound sidecar annotations generated from the sweep's own drift JSON
  by the committed `sidecar_from_drift.mjs` (mid receipt: drift 0, 29
  unpinned — `.ufo/waves/round-66/controls/sweep-mid-annotations.txt`);
  pins re-measured from the sweep JSON (missSet 65→93, citedSet 106 new,
  files 175, `round: 66`, `updated: 2026-10-31`; diff
  `controls/pins-diff.txt`; K2 boundary verified: added == exactly the 29
  documented migration paths, recovered == exactly `~/projects`). Zero
  corpus-prose bytes changed: SKILL.md is byte-identical to base
  (sidecar route per the QUALITY r20 ruling). Counting command:
  `node scripts/freshness-sweep.mjs --offline; echo $?`.
- **Reject (c):** re-adjudicating the 11 observed mismatches this round.
  Each needs its own revision-pinned re-derivation (several are deltas at
  the round-66 revision vs receipts taken at older revisions; the five
  historical not-green-at-pin rows share a plausible old-checkout mechanism
  the round did not test). Routed via the ledger rows; guessing would repeat
  the r64 causation error.
- **Reject (d):** adding c66 to the SKILL.md registry this round — the
  frozen C2 no-harm list forbids SKILL.md byte changes this round; routed
  as the next round's first registry item (the counter is otherwise
  registry-shaped: documented command
  `python -B .ufo/waves/round-66/c66_gate_status_hostportable.py --root .
  --revision <commit>`).
- **Reject (e):** forcing agreement or explaining away mismatches — the r64
  standing c56_selftally red must be re-pinned or carried with a named
  mechanism, never silently normalized; the ledger records it with its
  candidate mechanism and the frozen inner-env limit.
- **Protocol work (not claims):** carry-in D1/D2 corrections (mistakes
  table); five un-probed .kimi.page mirrors probed GET-only 2026-11-01T04:48Z
  (receipt `.ufo/waves/round-66/probes/receipt.json`; charter sentinel
  byte-identical to its PQ-5 pin — the armed watch has still never fired;
  plazir15 + lucario join the same fleet 404 sentinel; ufo-fsd/veigapunk
  serve 200) with dated corrections appended to
  `corpus/knowledge/publish-queue.md`; assimilation:
  `considerthese/2026-10-26.md` proposal 5 adopted as
  `corpus/knowledge/gate-status-ledger.md`, rows derived line-for-line from
  `controls/after-c66.txt`. No L2 wave was dispatched (no dispatch surface
  on this host; the r65 L0 question stands, routed around, not treated as
  answered); the non-author closure remains the outside check. Assimilation
  source register: shokuknow unreachable (absent on this host).

## Sources census

Round start (2026-10-31, before any edit):
`bash .../shokunin-clone/shokunin/scripts/sources-census.sh validate --root .../shokunin-clone/shokunin kake`
→ 16 W04 duplicate-URL warnings + `kake ok`, exit 0
(`.ufo/waves/round-66/controls/census-before.txt`). Round end: same command,
same 16 W04 + `kake ok`, exit 0 (`.ufo/waves/round-66/controls/
census-after.txt`). Registry 171 → 171 (no row added or edited; S133
re-opened only). The sidecar annotations bind lines by sha256, so the sweep
itself fails closed if any annotated line moved.
