# ScoutMisrootSweep — fleet-root misroot check (kake round 31, attempt 2, wave 2)

Read-only seat. Nothing moved, deleted, added or committed in the fleet repo or the lane; no
live request to any owned property. The only lane file written is this report. Scratch copies:
`/fast/scratch/hyaku/kake-r31/a2-w2/ScoutMisrootSweep/`.

## Answer (acceptance)

Fleet HEAD `fc94f5651f8cd7793a4b3ed1f5e0b83a0086c22b`; final status read at `2026-10-22T18:06:31Z`.
Five `??` entries. Exactly one names kake round 31 or a KakeR31 seat:

| untracked path | naming line |
|---|---|
| `.ufo/reports/round-31/kake.md` (9416 B, mtime `2026-10-22T14:09:39.371275605-03:00`, sha256 `1b61c8344e64da51016a2897349e48416e4c48c7c87804e0b32a064d66d6b8b4`) | line 1: `# kake round 31 report (hyaku, in-session L1 KakeR31, attempt 1)`; line 68 also names `KakeR31.CriticC1Counter` and `KakeR31.CriticSandboxThreatModel` |

No untracked file names `KakeR31a2`. The other four `??` entries have zero matches for
`kake|KakeR31|round.?31` (case-insensitive; `.pyc` checked with `strings -a`):
`live_s228.html` (Anubis challenge page), `nama.html` ("Page not found"), `tf_bavelas.html`
(Cloudflare "Just a moment..."), `scripts/hyaku/__pycache__/wave-live.cpython-314.pyc`.
Ignored entries filtered the same way yield only `!! kake-shokunin/` (the lane checkout,
a directory, expected).

## What the hit is

Observed:
- The path is the one the round-31 prompt assigns the L1 for its own report
  (`.ufo/prompts/kake-round-31.md:252`); line 257 is the *seat-note* misroot sweep
  (copy seat files written at the fleet root into the lane, `cmp`, delete the fleet copy).
  So this file is not a wave seat's stray note; it is the L1 report at its canonical path.
- The watchdog builds the same path (`scripts/shokunin-watchdog.sh:121,145`) and records the
  digest at every launch (`:203`). `.ufo/state/kake.report-baseline` contains
  `31 1b61c8344e64da51016a2897349e48416e4c48c7c87804e0b32a064d66d6b8b4` (mtime
  `2026-10-22T14:30:11.536541490-03:00`), byte-identical to the untracked report's digest;
  the log shows `lane-dead-no-report kake round=31` at 14:30:11 and the attempt-2 launch at
  14:30:13. The attempt-2 launch therefore baselined the dead attempt-1 report's bytes.
- `report_of` rejects exactly these bytes: when the baseline round equals the lane round, the
  digest must differ (`scripts/shokunin-watchdog.sh:159`). Content checks otherwise pass:
  `## SHONEN` heading at report line 52, 9416 B >= `MIN_REPORT_BYTES` 400 (`:54,163`).
- Never committed: `git ls-files --error-unmatch .ufo/reports/round-31/kake.md` exit 1;
  `git log --all -- .ufo/reports/round-31/kake.md` prints nothing; HEAD tracks only
  `.ufo/reports/round-31/kotodama.md` in that directory.

Staleness and placeholders in those bytes:
- line 3: ``Lane tip (pushed): `LANE_TIP` (branch `master`)`` — literal placeholder, no hash.
- line 66: `- Misroot sweep: MISROOT` — literal placeholder, not a sweep result.
- Identity is the dead attempt-1 L1 (`KakeR31`), never `KakeR31a2`; the report predates the
  attempt-2 measured-results commit `92235a0` (`SCORECARD.md:920` in the lane).
- No lane copy exists: the lane tracks only `.ufo/reports/round-20/kake.md`; the phrase
  "in-session L1 KakeR31, attempt 1" occurs in no lane Markdown file
  (`grep -rln --include='*.md'`, no output, exit 1).

Inference:
- [INFERENCE] Untracked presence at this path is expected until the attempt-2 L1 finalizes its
  report. The defect visible today is content (attempt-1 identity, two unresolved placeholders)
  plus the baseline tie, not a misplaced path. No action taken.

## Commands (all read-only; exit codes)

- `git --no-optional-locks status --porcelain=v1 --untracked-files=all` in
  `/home/vgpnk/Projects/shokunin` — exit 0, run three times (18:0xZ). ` M .ufo/waves/hyaku/PHASE3.md`
  appeared between run 1 and run 2 (another process; not kake-related).
- `git rev-parse HEAD` — exit 0, `fc94f565…`.
- `grep -n -E 'KakeR31a2|KakeR31\b|kake round 31' .ufo/reports/round-31/kake.md` — exit 0,
  lines 1 and 68 only.
- `sha256sum .ufo/reports/round-31/kake.md` and `cat .ufo/state/kake.report-baseline` — exit 0,
  digests equal.
- `git check-ignore -v .ufo/reports/round-31/kake.md .ufo/reports/round-31/kotodama.md` — exit 1
  (neither ignored).
- `git ls-files --error-unmatch .ufo/reports/round-31/kake.md` — exit 1.
- `grep -ciE 'kake|KakeR31|round.?31'` on the three HTML files — exit 1, count 0 each;
  `strings -a <pyc> | grep -ciE 'kake|r31|round.?31'` — count 0 each.
- `grep -nE '<SHONEN heading pattern>' .ufo/reports/round-31/kake.md` — exit 0, line 52.
- `git --no-optional-locks status --porcelain --ignored=matching -uall | grep -iE 'kake|r31|round-31'`
  — exit 0, only `!! kake-shokunin/`.
- `grep -rln 'in-session L1 KakeR31, attempt 1' --include='*.md' .` in the lane — exit 1, no output.
- `git -C kake-shokunin ls-tree -r --name-only fde133a .ufo/reports/` — exit 0, only
  `.ufo/reports/round-20/kake.md`.

Staged-but-uncommitted entries (`A`) were also read, though out of the untracked scope: `write`
= `agent://U100N079H334f935b`; three `*.report-baseline` = `<round> <empty-stream sha256>`;
`.scratch/goal-20261022-hyaku-12h.md` names kake r28 only — none names kake round 31 or a
KakeR31/a2 seat.

## Not verified

- Did not execute the watchdog or `report_of` (either can spawn lanes); their predicates were
  replicated by hand on the same bytes.
- Did not identify which process wrote the three stray HTML files; they name no kake content
  and were left untouched.
- No tool installs or upgrades were made.
