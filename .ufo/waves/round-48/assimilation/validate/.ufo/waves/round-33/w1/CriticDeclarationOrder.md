# KakeR33.CriticDeclarationOrder — was the round-33 declaration frozen before data?

Verdict (advisory): the receipt order holds and the counters are unchanged. One undisclosed
pre-declaration measurement exists for C2, and the commit has two different times.

## Timeline (all -03:00, 2026-10-22; births from `stat %w`, jj from `jj --ignore-working-copy op log`)
| time | event | evidence |
|---|---|---|
| 16:26:05 | base 5777d5a committed; jj opens the new empty change that later becomes bc6c4a8 | `git show -s` author=committer=16:26:05; op 6021563dc952 |
| 16:49:58 | upstream clone of ds4cc-marketplace at 7fc6aa2f | /fast/scratch/hyaku/kake-r33/ds4cc-upstream/.git/logs/HEAD epoch 1792698598 |
| 16:51:50 | c1_code_probe.py written (mtime = ctime, never touched since) | stat: mod 16:51:50.904, change 16:51:50.905 |
| **16:52:01** | **/fast/scratch/hyaku/kake-r33/probe/ created: the three frostbite pages plus m.json, a canonical_audit manifest for /magga/frostbite/ and /classic/** | `find probe`; birth 16:52:01.45 |
| 16:52:28 | c2_pin_count.py written (mtime = ctime) | stat: mod 16:52:28.658, change 16:52:28.659 |
| 16:52:44 | bc6c4a8 committed (committer time) and pushed | `%cI` 2026-10-22T16:52:44-03:00; ops d66a8b570f9e, b4f2ffaa4d6c |
| 16:52:51 | census-before.txt and c1-before-5777d5a.json created | birth 16:52:51.227 |
| 16:53:00 | c2-before-5777d5a.json, c2-at-bc6c4a8.json, c1-at-bc6c4a8.json created | births 16:53:00.790 / .826 / .860 |
| 16:58:41 | /fast/scratch/hyaku/kake-r33/m.json (remastered manifest) | birth |
| 16:59:40 | b1752a2 (implementation plus the before receipts) committed and pushed | op c5e9a5d8ed83 |
| 16:59:46–51 | c1-after-b1752a2.json, c2-after-b1752a2.json (untracked) | births |

## Order checks
- Receipts compared with the declaration: no violation. Every before or at receipt was created 7 to 20 s after the committer time, and the after receipts were created after b1752a2.
- Before values were stated before this round's measurement: yes. C1 "met 2 (reworded fails P6, recoded n/a)" and C2 "met 0" are in bc6c4a8:SCORECARD.md lines 1107–1110, so they predate the receipts. C1's "reworded fails" was already known from round-32 data (corpus/lessons/round-32-verifier-spotcheck.md:127–130, `w1/MutReasonCheckGate.md`), so it was a known prior result, not a blind prediction. SCORECARD.md is unchanged in b1752a2 and in the lane working tree.
- My sandbox reruns from a clone at bc6c4a8, with TMPDIR set to my sandbox:
  - `python3 -B .ufo/waves/round-33/c2_pin_count.py --rev 5777d5a…` exit 0: met 0, JSON equal to c2-before-5777d5a.json.
  - `… c2_pin_count.py --rev bc6c4a8…` exit 0: met 0, equal to c2-at-bc6c4a8.json.
  - `… c1_code_probe.py --rev 5777d5a…` exit 0: met 2, guard_ok true, equal to c1-before-5777d5a.json.

## Counterexample 1: undisclosed C2 pre-measurement (fixable wording or provenance defect)
SCORECARD.md:1104–1105 says the declaration lands "before either counter has run at any revision".
That is literally true, because c2_pin_count.py did not exist until 16:52:28. However, at 16:52:01, 43 s
before the commit, the L1 had staged exactly the inputs the C2 c4 condition measures: the three pages
(blobs equal upstream: index e0d9ee29, classic 12c58e2d, remastered 4e6d70ae) plus a manifest of
the same shape that c2_pin_count.py:159–160 writes (`url`, `file`, `expectedCanonical`). Running the
lane's own auditor on that pre-declaration probe gives the verdicts later stated in the section:
- `python3 -B scripts/canonical_audit.py --manifest <sandbox>/probe-copy/m.json` exit 0 →
  `{"findings":[],"pagesChecked":2,"verdict":"clean"}`
- the remastered manifest (/fast/scratch/hyaku/kake-r33/m.json, made after the commit) exit 0 → `clean`.

[INFERENCE] The auditor was run on the probe before the commit. Its output went to stdout, so nothing on disk proves the run. The declaration discloses the upstream clone but not this probe.
Impact is limited: C2's c4 is a self-consistency check (stated verdicts equal re-derived verdicts), so
knowing the verdicts beforehand cannot make "met 4" easier to reach. The "before met 0" is also trivially
true. Axes: freshness provenance (the "frozen before data" wording) and operability, low severity.

## Counterexample 2: two commit times (false-provenance risk)
bc6c4a8's author time is 16:26:05, identical to the base commit's, because jj set it when it opened the
empty change. Default `git log` shows the author date, so the declaration appears to predate the
upstream clone (16:49:58) and the probe (16:52:01) by about 26 minutes. The declaration's "that commit's time"
does not say which of git's two times it means. Only the committer time (16:52:44) is truthful.

## sha256 comparison (lane file compared with the committed blob at bc6c4a8 and at master b1752a2)
| file | lane sha256 | bc6c4a8 blob / sha256 | b1752a2 |
|---|---|---|---|
| c1_code_probe.py | 74bf1f80d79e830d2a5c30a711dad3172f79135af1212e998860afb653b9e047 | f4ee0e89… / same sha256 (mode 100755) | same blob |
| c2_pin_count.py | 97a481294e9f0cd76f6a7608536b5bbeab8dbfc6191ea9437afe7005d5629ea8 | 27547634… / same sha256 (mode 100755) | same blob |
`git hash-object` of the lane files matches both blobs, and `git diff --stat bc6c4a8 b1752a2 -- <counters>` is empty (exit 0).
Gap: the receipts record neither counter sha256 nor counter blob. Their tie to the frozen bytes rests
on mtime and ctime predating the commit, plus my byte-equal reruns.

## Smallest safe correction
Append a correction under the round-33 declaration, leaving the declaration text unchanged. It should say: (a) "the time of the declaration" means
the committer time 2026-10-22T16:52:44-03:00, and the author time 16:26:05 is jj's change-creation time; (b) at 16:52:01,
before the declaration, the L1 staged canonical_audit inputs for two of the three frostbite pages
(/fast/scratch/hyaku/kake-r33/probe/), so the C2 verdicts were open to the author before the freeze.
Optional: future counters could print their own sha256 into each receipt.

## Not verified
Whether canonical_audit actually ran at 16:52:01 (no on-disk output). Whether c1_code_probe.py ran
between 16:51:50 and 16:52:44: it uses a self-deleting TemporaryDirectory, so no trace remains. Nothing was found that shows such a run.
I did not rerun c1 or c2 at b1752a2, and I did not check the C1 or C2 implementations themselves.

Sandbox: /fast/scratch/hyaku/kake-r33/w1/CriticDeclarationOrder/ (clone at bc6c4a8, c1-base.json,
c2-base.json, c2-decl.json, probe-copy/). No tools installed. No network use.
