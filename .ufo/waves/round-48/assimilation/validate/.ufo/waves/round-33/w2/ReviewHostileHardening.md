# ReviewHostileHardening — r33 wave-2 falsify (operability)

Target: `git diff e4903817 1cf452ea -- scripts/citing_set_hostile_selftest.py`
(stray/symlinked spec entries refused; whitespace-only `reason_contains`/`reason_code` refused).
Claims tested: SKILL.md "Citing-set runner — round 33" (clone at 1cf452ea, SKILL.md:948-972)
and the selftest's own docstring (exit 2 on bad input; one JSON object always).

## Method

Sandbox `/fast/scratch/hyaku/kake-r33/w2/ReviewHostileHardening/`; lane cloned with
`git clone -q <lane> clone`, `git -C clone checkout -q 1cf452ea` (HEAD verified).
Per case: a fresh root = `cp -a` of `scripts/` plus one mutation inside
`scripts/fixtures/citing-set-hostile/`, then
`python3 -B <root>/scripts/citing_set_hostile_selftest.py --root <root> --tmpdir <sandbox>/tmp/<case>`.
All 16 runs concurrent; full results in `<sandbox>/results.json`; mutated trees kept under `<sandbox>/cases/`.

## Observed (exit / JSON error)

| Case | Exit | Result |
|---|---|---|
| baseline (pristine clone tree) | 0 | passed=true, 6 cases |
| stray file `stray.txt` | 2 | "holds non-directory or symlinked entries: stray.txt" |
| stray dot-file `.DS_Store` | 2 | same, names `.DS_Store` |
| entry symlink -> sibling spec dir | 2 | names `PZ-link` |
| dangling symlink | 2 | names `PZ-dangle` |
| FIFO entry | 2 | names `PZ-pipe` |
| Unix-socket entry | 2 | names `PZ-sock` |
| dot-named dir `.hidden/` (empty) | 2 | Errno 2 `.hidden/hostile.json` |
| empty spec dir `PZ-empty/` | 2 | Errno 2 `PZ-empty/hostile.json` |
| spec dir itself a symlink | 0 | passed=true, 6 cases (followed, NOT refused) |
| spec dir missing | 2 | "runner, benign fixture or hostile specs missing" |
| spec dir chmod 000 | **1** | **no JSON; PermissionError traceback on stderr** |
| `reason_code: "   "` | 2 | "reason_code must be a string with a non-space character" |
| `reason_contains: "\t \n"` | 2 | same for reason_contains |
| `reason_code: 7` (non-string) | 2 | same message (old non-empty rule kept) |
| top-level spec key `" "` | 2 | key allowlist refusal |

## Findings

F1 (minor): `spec_dir.iterdir()` at `citing_set_hostile_selftest.py:248` runs outside
the `try` at :259-264, so an unreadable spec directory crashes with a Python
traceback, exit 1 and zero bytes of stdout — violating the documented contract
"Exit ... 2 on bad input" and "one JSON object", and the round-24 criterion "a
nonzero exit accompanied by a traceback is a crash, not a successful rejection".
Repro: `chmod 000` the fixture dir (command above; `tmp/u.err` head captured).
SKILL.md:961 says such OS errors are "reported, not raised" for `read_expected`;
the same expectation is broken one level up for the spec directory itself.
Fix is one line (wrap `iterdir` in the same OSError handling).

F2 (noted, already disclosed): a symlinked spec directory is silently followed
and its specs run (exit 0). SKILL.md:966-967 discloses this as still-open, so no
overclaim; it remains a live entry point (a hostile.json symlinked in from
elsewhere is loaded by `lstat`-regular check — actually refused if the inner
file is a symlink; only the directory hop is unguarded).

## No-defect confirmations

- Stray refusal covers files, dot-files, FIFOs, sockets, valid and dangling
  symlinks; all exit 2 naming the offenders, before any spec load.
- Whitespace-only values refused for both `reason_contains` and `reason_code`;
  non-strings still refused; message contract changed as declared.
- Empty and dot-named dirs are treated as spec dirs -> exit 2 on missing
  `hostile.json` (consistent with case names `.h*` being legal).
- Pristine tree passes all 6 specs (exit 0); no regression from the refactor.

Not verified: concurrent selftest runs (covered by ExecScratchDefaultConcurrency);
behaviour under `--runner` override; Python <3.9 (Path.is_dir OSError-swallow
changed in 3.8+ is irrelevant on this host, Python 3.13).

Report: .ufo/waves/round-33/w2/ReviewHostileHardening.md
