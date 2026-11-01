# Round 66 contract — kake (frozen before any after-state data)

Base revision: `6a2ecb18f58dfa47492d38d736ee7c34b6eaa3c6` (round-65 verifier
spot-check tip, pushed, `origin/master` identical at freeze). Host: Windows,
Python 3.13.15 (`python.exe`; `python3` resolves only to the inert Microsoft
Store alias stub), node v24, git for Windows. Frozen 2026-10-31 before the
C1 instrument existed and before the C2 repair was applied. Pre-change
evidence already committed or captured at freeze: r65 receipts
(`.ufo/waves/round-65/controls/`, incl. `c60-paired-thishost.txt` v1 28/28
host-bound and `sweep-final-thishost.txt` exit 1 / 23 drift / 29 newMissing)
and the sweep selftest red captured before any change
(`.ufo/waves/round-66/controls/selftest-before.txt`, `selftest: 34/36`,
the two failures being exactly the sidecar-lookup cases).

## C1 — calibration (lowest owned non-retired axis, 2): the 28-member gate
## registry becomes host-evaluable on this Windows host

Claim (evaluability, NOT agreement): the frozen round 48–59 gate-status
family (population, labels and command grammar exactly as in
`.ufo/waves/round-60/c60_gate_status.py` v1) cannot be adjudicated on this
host — v1's every member observation dies of the environment (28/28 outside
the family verdict alphabet, receipt `c60-paired-thishost.txt`). A
versioned successor `.ufo/waves/round-66/c66_gate_status_hostportable.py`
(v2) re-derives the same registry so that every member produces a
family-verdict exit on this host.

Frozen predicate:

    met: members == 28 AND evaluated == 28 AND scores_held == 3

Amendment 1 (pre-data, recorded at instrument-verification time, before any
after-state receipt existed): the v2 selftest's `E.extra_member` case (v1's
own population-guard fixture) showed a population violation must stay
verdict-relevant. The predicate gains `AND structural == 0` where structural
counts the twelve v1 structural/population classes (member_missing,
member_changed, extra_member, unregistered, duplicate_row, row_incomplete,
label_invalid, unpinned, pin_not_ancestor, member_absent_at_pin,
command_unparsable — population and registry-row integrity gate exactly as
in v1); the observation classes (a recorded label vs what the gate printed
on this host) remain reported, never gating. timed_out keeps v1's
unevaluable exit-2 behavior.

- `members`: the 28 frozen member paths present at `--revision` with the
  same blob ids as v1's FROZEN table (byte-identical definition).
- `evaluated`: a member counts when EVERY of its observations (e_T; e_P for
  label historical/never-met members whose pin run ran) exits with a code in
  the family verdict alphabet {0, 1, 2, 64} — the documented exits of every
  counter in the family ("Exits: 0 met, 1 not met, 2 unevaluable, 64
  usage") — and did not time out. An exit outside the alphabet (this host's
  command-not-found 9009 from the Store `python3` stub, or any other
  environment death) means the member was NOT evaluated. Grounding for
  reading exits this way: SOURCES row S133 (Python subprocess returncode
  semantics), re-opened live this round.
- `scores_held`: v1's A7 measure verbatim (exactly one axis table;
  operability 10, freshness 10, calibration 2).
- Informational, never gating: per-member v1 mismatch classes; `agreement=`
  (members with zero v1-class label mismatches); the `env:` selfcheck line.
  A recorded label that does not reproduce on this host is REPORTED, not
  forced: this claim does not assert the registry's statuses are correct.

v2's only deltas from v1 (each documented in its docstring; diff receipt
committed at `controls/c66-v1-v2-diff.txt`):

1. `FLEET_ROOT` is this host's fleet root (v1 hardcoded the dead old-host
   path `/home/vgpnk/Projects/shokunin`).
2. Member observation env: PATH is built for the running host (scratch
   alias dir first, then the real interpreter dir, the git dir, and the
   Windows system dirs) instead of POSIX `/usr/bin:/bin`; `PYTHONUTF8=1`
   pins text encoding to UTF-8 (matching the old host's C.UTF-8 locale;
   without it Windows decodes corpus text as cp1252); on Windows the
   minimal system vars (SystemRoot/SystemDrive/ComSpec/PATHEXT) are passed
   because git.exe requires them. Everything else v1 pinned stays: fresh
   shared clone detached at the revision under test, cwd=clone,
   HOME=TMPDIR=scratch, LANG=C.UTF-8, no GIT_*/PYTHON*/KAKE_* inheritance.
3. Scratch alias dir: one `python3.exe` per run (byte-copy of the running
   interpreter) so the members' frozen documented argvs (`python3 -B …`,
  e.g. c56_selftally's inner spawns of the ten registered gates) resolve to
   a real CPython instead of the Store stub. The alias is an environment
   provision, exactly what `/usr/bin/python3` was on the old host; no
   frozen byte (registry rows, member counters) is rewritten.
4. Pre-measure env selfcheck: `python3 -c` prints a CPython version and
   `git --version` succeeds under the constructed env, else exit 2
   unevaluable (the instrument refuses to adjudicate from a broken env).
5. The predicate counts `evaluated` (above); v1's `mismatches == 0` term is
   deliberately NOT carried — registry agreement is measured and reported,
   not promised (the r64 note already recorded one standing c56_selftally
   mismatch whose causation was unproven; it is not mine to promise away).

Known limit, frozen and disclosed: c56_selftally's inner spawns build their
child env from a FIXED key set (`PATH/HOME/LANG/PYTHONDONTWRITEBYTECODE`),
so `PYTHONUTF8=1` does not reach the ten inner gate runs; if an inner run's
Windows text decoding corrupts its result, v2 reports that member's real
exit as measured and the limit is named in the receipt — it is carried
debt, not silently patched.

Kill rules (any fire → C1 not admitted):

- K1: env selfcheck fails at the settlement tip (no real python3/git under
  the observation env) → exit 2, no credit.
- K2: `evaluated < 28` at the settlement tip → met=False, honest stop.
- K3: `scores_held != 3` → fail (axis table altered mid-round).
- K4: v2's selftest not all-pass, or the committed v1→v2 diff touching
  anything outside deltas 1–5 → fail.

Do-nothing control: v2 does not exist at base (`git cat-file -e
6a2ecb1…:.ufo/waves/round-66/c66_gate_status_hostportable.py` fails) and a
fresh v1 run at base prints every member outside the alphabet — no control
reaches `evaluated == 28` without building the portable observation env.

Receipts: `controls/c60-v1-base-r66.txt` (v1 fresh at base),
`controls/selftest-c66.txt`, `controls/after-c66.txt` (v2 full run at the
settlement tip, revision named in the receipt),
`controls/donothing-c66-base.txt`, `controls/c66-v1-v2-diff.txt`.

## C2 — freshness (10): the §paths gate returns to exit 0 on this host
## (migration re-pin), with the sidecar annotation mechanism repaired

Claim: the host migration left the standing §paths gate could-not-evaluate
(exit 1: 23 drift tokens with unannotated cites + 29 migration paths not in
`pins.pathsMissSet`, receipt `sweep-final-thishost.txt`); the round restores
`node scripts/freshness-sweep.mjs --offline` to exit 0 at the settlement
worktree by (a) repairing the sidecar lookup's host-portability bug, (b)
annotating every unannotated drift cite through the line-bound sidecar
(QUALITY r20 ruling: preserves original corpus bytes — zero SKILL.md byte
changes), and (c) re-measuring the pins sets (r18 pattern), each step
receipted.

Frozen predicates:

- Part 1 (instrument repair): in `scripts/freshness-sweep.mjs`, the only
  change is normalizing the sidecar key to forward slashes at the lookup
  (JSON entries are validated forward-slash-only; `path.relative` emits
  host separators). Red-before: the committed pre-change selftest
  (`controls/selftest-before.txt`, taken before any edit) prints
  `selftest: 34/36` with exactly the two sidecar-lookup cases failing on
  this host. Green-after: the same command prints all cases passing at the
  settlement tip, with NO selftest case removed.
- Part 2 (annotations): every unannotated cite of every drift token in the
  post-fix sweep gets a `corpus/knowledge/freshness-sidecar.json` entry
  (schema kake-paths-sidecar-v1: file/line/token/lineSha256 bound, kind
  absent, dated 2026-10-31, note carrying the migration context and the
  exact phrase "historical record, not an executable instruction"),
  generated by the committed tool `.ufo/waves/round-66/sidecar_from_drift.mjs`
  from the sweep's `--json` drift output; the existing 30 entries are
  appended to, never edited.
- Part 3 (re-pin): `corpus/knowledge/freshness-pins.json` gains the current
  `pins.pathsMissSet`, `pins.pathsCitedSet`, `pins.pathsFiles` as measured
  at the settlement worktree, with `round: 66`, `updated: 2026-10-31` — a
  dated re-measure (round-18 pattern), values taken from the sweep JSON
  itself, not hand-written.
- Gate (the claim): at the settlement worktree, `node
  scripts/freshness-sweep.mjs --offline` exits 0 (VERDICT: OK, partial:
  offline — §history stays pin-suspended, §armed stays skipped offline, as
  designed), with `drift []` and `newMissing []`.

Kill rules (any fire → C2 not admitted):

- K1: the sidecar loader throws (binding invalid / duplicate) at the
  settlement tip → the sweep exits 2, fail.
- K2: the new miss set contains any path beyond the 29 documented migration
  paths minus the recovered `~/projects` (i.e. the round itself broke a
  citation) → fail.
- K3: any selftest case removed, or any corpus file edited to carry an
  inline annotation (the sidecar route is byte-preserving BY construction;
  an inline edit would break the QUALITY r20 ruling) → fail.
- K4: SKILL.md or `corpus/SOURCES.md` bytes differ from base → fail
  (no-harm list; SOURCES re-open only).

Do-nothing control: at base the sweep exits 1 with 23 drift / 29
newMissing (`controls/sweep-base-r66.txt`, fresh this round) — no control
reaches exit 0 without the repair + annotations + re-pin.

Receipts: `controls/sweep-base-r66.txt`, `controls/selftest-before.txt`
(pre-change), `controls/selftest-after-c2.txt`,
`controls/sweep-mid-annotations.txt` (drift 0, newMissing 29 — annotations
landed, pins not yet re-pinned), `controls/sweep-after-r66.txt` (exit 0 at
the settlement tip), `controls/pins-diff.txt`.

## Sourced claim (§2b)

C1 rests on SOURCES row S133 (Python: subprocess — child-process exit-status
semantics used by receipt gates), re-opened LIVE this round: one GET, bytes
recorded in `sources/s133-receipt.json` with access date and digest, and the
≤25-word located quote recorded in the round lesson `## Gate`. The
`evaluated` term is exactly S133's semantics: only an exit the docs define
(counting the family's documented verdict codes) can carry the evaluability
witness; an environment death (9009) can never pass as one. No registry row
is added or edited (registry stays 171 rows).

## Non-claim work in scope (protocol; no score credit)

- Carry-in D1 (r65 verifier): the round-65 report's "LOG +9 / lesson +105"
  prose counts drift vs numstat +10/+106 — corrected append-only (LOG entry
  + lesson mistake row + report section; every count in this round's
  artifacts carries its counting command per the CORPUS rule).
- Carry-in D2 (r65 verifier): `.ufo/waves/round-65/controls/base-c1.txt`
  labels the A4 block "c65-red/c64-green DIFFERENTIAL OK" while its own A4
  lines record c64 met=false (A4 is non-differential per the frozen r65
  contract) — relabel appended to the file (append-only; recorded lines
  untouched).
- Un-probed mirror re-probe (GET-only, receipts
  `probes/<name>.txt` + dated corrections appended to
  `corpus/knowledge/publish-queue.md`): the five properties the r65
  verifier listed un-probed (ufo-fsd / veigapunk / plazir15 / charter-ufo-fsd
  / lucario mirrors on their .kimi.page / .kimi.pro surfaces). Findings are
  dated protocol corrections, NOT claims (no standing claim is frozen on
  them before the data exists).
- Assimilation candidate: considerthese/2026-10-26.md proposal 5
  (historical-gate list) — adopted only if C1's measurement exists and the
  ledger's rows are derived from the committed v2 receipt line-for-line;
  else Assimilation: none — shokuknow unreachable.
- §9 fresh-start duty: r62/r63/r64 rejected closures re-read and
  spot-checked; ruled out (a) any semantic-resolution calibration claim
  from syntax-class counters (r63/r64 kill rules fired on marker-prose
  greens twice), (b) counters without committed differential fixtures
  (r62's marker-only false-green), (c) promising the registry agreement
  green (r64's standing c56_selftally mismatch has unproven causation).
  C1/C2 are instrument-evaluability moves neither a do-nothing control nor
  any prior round reached on this host.

## Erratum (append-only, r67) — receipt-name map for this contract

The r66 non-author closure (defect 1, `corpus/lessons/round-66-verifier-spotcheck.md` §7)
recorded that three receipt paths this contract names do not resolve verbatim to the
landed files, while every artifact exists and verifies. Name map, so future re-openers
hit live pointers (contract lines above are untouched; recorded 2026-11-01):

- `controls/selftest-after-c2.txt` (contract line ~174) → landed as
  `.ufo/waves/round-66/controls/selftest-sweep-after.txt` (the §paths sweep selftest after
  the host-path repair, 36/36).
- `sources/s133-receipt.json` (contract line ~183) → landed as
  `.ufo/waves/round-66/sources/receipt.json` (the S133 live re-open receipt; the live body
  sits beside it as `sources/subprocess.html`).
- `probes/<name>.txt` (contract line ~202) → landed as
  `.ufo/waves/round-66/probes/<name>.kimi.page.body` (one file per probed host) plus the
  single index receipt `.ufo/waves/round-66/probes/receipt.json`.

The round-67 contract names its receipt paths in the landed form directly
(`probes/<host>.body` + `probes/receipt.json`), which is the fix in kind.
