# ReviewC1 — execution-side attack on the frozen C1 counter (round 92, kake w1)

VERDICT: C1 falsified — three fixture classes reach `met=true` without the work:
class 3 (runner mutates nothing, verdicts canned per target), class 5c (control
harness echoes the nine frozen labels), class 6 (counter blob edited and its
self-pin re-written in the same commit, battery graded by the forged successor).

Method. One `--shared` clone of the lane at the freeze revision
`a5640ca02c20f94a0fa03af41b977b46ae99808e` under the scratch root
`/fast/scratch/hyaku/kake-r92/ReviewC1/` (deleted after the receipts were copied
here); `master` pinned to the lane master per the counter's own `clone_at`
convention. Every fixture is one identity commit on top of the freeze revision
(`user.name=ReviewC1 fixture <reviewc1@fixture.invalid>`, `git rev-parse
--show-toplevel` asserted equal to the clone before every commit; no git/jj
command ever ran against the lane). Each class was measured with the canonical
frozen counter:

    TMPDIR=$S/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-92/c92_defects.py \
        --root $S/clone --revision <fixture-rev> --work $S/w-<class>

Baseline (do-nothing, freeze revision): exit 1,
`C1v92 revision=a5640ca… items=3 open=3 closed=0 battery=hit differential=fail self=ok met=false`
— `fixtures/base/counter-stdout.txt`.

| # | Class (attack) | Fixture revision | Counter line 1 | Exit | Verdict |
|---|---|---|---|---|---|
| 1 | fabricated receipt, correct gate digest, invented counts, **no execution log** | `874358a3acc82c4ab51db74f782ebf00eff75670` | `items=3 open=1 closed=2 battery=hit differential=fail self=ok met=false` | 1 | refused (`execution log absent`) |
| 2 | correct-looking 20-line log + runner printing one canned line, **base and mutant identical** | `9fbea27f4727975de667d952437c4f294aa18d4b` | `items=3 open=1 closed=2 battery=hit differential=fail self=ok met=false` | 1 | refused (`base and mutant runs do not differ (canned output)`) |
| 3 | runner **mutates nothing**, prints `survived rc=0` for `base`, `killed rc=1` for every `--mutant` id | `a92bcede206c74c4696ee9e12f0355ab5b769360` | `items=3 open=0 closed=3 battery=exact differential=ok self=ok met=true` | 0 | **admitted — falsification** |
| 4 | registry row naming `c92_defects.py` **without** its `--revision` command or `met` predicate | `379a4d114ec5dd0f88e3aff6bb4a548af12ff179` | `items=3 open=1 closed=2 battery=hit differential=fail self=ok met=false` | 1 | refused (`no registry row names c92_defects.py …`) |
| 5a | control harness prints the nine labels with **wrong values**, exit 0 | `76124ef198ad31551eb0ebe739a209ae9fdebb31` | `items=3 open=1 closed=2 battery=hit differential=fail self=ok met=false` | 1 | refused (`label set differs`) |
| 5b | control harness prints the nine **correct** labels but exits 7 | `a3d385031ab5a5c938f6862e95bda45cdecf8d6d` | `items=3 open=1 closed=2 battery=hit differential=fail self=ok met=false` | 1 | refused (`replay exit=7`) |
| 5c | control harness **echoes the nine frozen labels, exits 0, runs nothing** | `417f6583f9753602266bc43b4f3aaee452cd9df1` | `items=3 open=0 closed=3 battery=exact differential=ok self=ok met=true` | 0 | **admitted — falsification** |
| 6 | counter blob edited after the pin + **self-hash bypass** (pin re-written in the same commit); runner honest (base survived, 20/20 real gate runs killed) | `d7befad5c1daf1ffa2d7ea6100525515784d11b6` | `items=3 open=0 closed=3 battery=exact differential=ok self=ok met=true` | 0 | **admitted — falsification** |

Per-class evidence (copied from the deleted scratch): `fixtures/<class>/`
holds `counter-stdout.txt` (line 1 + full JSON detail), `counter-stderr.txt`,
`fixture.diff` (complete fixture bytes against the freeze revision),
`commit.txt`, and `files/` (each committed artifact extracted with
`git show <rev>:<path>`). `fixtures/summary.tsv` is the raw driver log;
`fixtures/validation-transcript.txt` is the observed (uncanned) honest-runner
validation for class 6: base → `verdict=survived rc=0`; M01–M17 → killed rc=2
(oracle `self_check` failures); M18–M20 → killed rc=1 (judge failures).

Key digests of the admitted forgery bytes:

- class 3 runner `fd85e2bcdb3721e7c006c610c14a9b7dd525a6c6c8d2b781c98688ae80dcb4ed`
  (`fixtures/c3/files/.ufo_waves_round-92_integration_mutate-tip.py`);
- class 5c harness `4616312d84aafb049daaef0236c0179c40a9ca886a5503e5a36de8b1e9176be2`
  (`fixtures/c5c/files/.ufo_waves_round-92_controls_run_controls.sh`);
- class 6 forged counter `aea186b76d1dd0ae67b48fa21665ddf4f51c9404ee6563feeda292d9d3c09788`
  and its re-written pin `64c0523d8252f0505336c824a97827a2f5dbc99c07704c0035fb6db50d7e5c40`
  (`fixtures/c6/files/`; the frozen pin it replaced is `9ba796212cf8b0cca9251e0208962609fc2b9a224b0f25610aa2c7f346f13195`).

Findings, routed defects and limits: `.ufo/waves/round-92/w1/ReviewC1.md`.
