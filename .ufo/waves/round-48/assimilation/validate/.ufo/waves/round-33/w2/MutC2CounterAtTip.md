# Round 33 C2 counter mutation probe

Axis: freshness. Probe base: `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` in isolated clone `/fast/scratch/hyaku/kake-r33/w2/MutC2CounterAtTip/clone`.

Detector: `python3 -B "$C/.ufo/waves/round-33/c2_pin_count.py" --rev "$R" --repo "$C"` (`C` is the clone path; `R` is the listed commit). Each run exited 0. Baseline output: `c1_retained=true, c2_row=true, c3_section=true, c4_truth=true; met=4/4`; sitemap count 100; all three canonical observations and statements `clean`.

| Mutation (one independent commit from base) | Commit | Conditions c1/c2/c3/c4 | met | Verdict |
|---|---|---|---:|---|
| Retained sitemap: one byte `ds4cc` → `dt4cc` | `c5881489ac527fdc27f2580bf86c0025ce1e7f14` | F/T/T/F | 2/4 | killed |
| Retained hub page mode `100644` → `100755` | `ec912df47e6df9de033e0256b66e307944c65ce3` | F/T/T/F | 2/4 | killed |
| S065 status `mined` → `queued` | `0fc6eeac9944e832adb0e2f3c4669bcba863ace9` | T/F/T/T | 3/4 | killed |
| S065 opened date `2026-10-22` → `2026-10-21` | `37d6538d9af0e8a905d72e8e1b4904fab6c4a1dd` | T/F/T/T | 3/4 | killed |
| Heading suffix `7fc6aa2f` → `7fc6aa2e` | `5f0eb8b2c6b8a0803a88b1a2950f70fecb009d2a` | T/T/F/F | 2/4 | killed |
| `sitemap-locs: 100` → `99` | `82d9e8535e73e8397b66c3a22b81f2ace4fd9844` | T/T/T/F | 3/4 | killed |
| First canonical verdict `clean` → `dirty` | `f1d5984b6370d446681cd4006f2f01c50f946e07` | T/T/T/F | 3/4 | killed |

No mutation survived or was inconclusive. The retained-file probes also fail c4 because c4 requires c1; the heading probe fails c4 because its section is absent.

Hash evidence (base blob → mutant blob): sitemap.xml `67d8c7a50dc3a3734ce4be97ffa4810e1e257e12` → `de3432b11aa7a8d76a0a97fda6deed7146bb2bad`; hub page blob remains `e0d9ee29d9f1bf21faa0238e3253d4e9199304de` with mode `100644` → `100755`; `corpus/SOURCES.md` `bac1bf2ebb1494f84e914afbafec5bd19e1a0f97` → `a698e19eb8a4dff84d74754af00edf1cb9721b44` (status) and `73eec74d7022296d787a376f7423fba9636f047b` (date); audit entry `e19405372b50c21476f5fdc9151f6b58d273e0be` → `e4997b9c99066164c11302b2ffade0f47305bd9d` (heading), `5c2fced2044dcbb075bf80ca98e608bd6577eda1` (loc count), `a9f8d137fe009efe5b7984bbb131e8887f13bb45` (canonical).

Restoration: switched clone back to base; `HEAD=0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`, `git status --porcelain=v1` empty. Restored blobs: SOURCES `bac1bf2ebb1494f84e914afbafec5bd19e1a0f97`, audit entry `e19405372b50c21476f5fdc9151f6b58d273e0be`, sitemap `67d8c7a50dc3a3734ce4be97ffa4810e1e257e12`; hub page mode `100644`. Reran the same counter command on the restored base: exit 0, `T/T/T/T`, `met=4/4`.

Commands: from the clone, each independent mutant used `git switch --detach 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`, `git switch -c <branch> 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`, one listed change, then the following `git add <target> && git commit -m <subject>` (each commit succeeded):
- `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/sitemap.xml` — `mutant: change one retained sitemap byte`
- `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/magga/frostbite/index.html` — `mutant: mark retained page executable`
- `corpus/SOURCES.md` — `mutant: change S065 status cell`; separately `mutant: change S065 opened date`
- `corpus/knowledge/sitemap-orphan-audit.md` — `mutant: alter source-pin heading`; separately `mutant: alter stated sitemap count`; separately `mutant: alter one canonical verdict`

Exact detector invocation for each table commit, with `C=/fast/scratch/hyaku/kake-r33/w2/MutC2CounterAtTip/clone` and `R` set to that commit, was `python3 -B "$C/.ufo/waves/round-33/c2_pin_count.py" --rev "$R" --repo "$C"` (exit 0 for all seven); the same invocation ran with `R=0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` before mutation and after restoration (both exit 0).

Disclosure: one preliminary baseline invocation omitted `--repo` (`python3 -B .ufo/waves/round-33/c2_pin_count.py --rev HEAD` from the clone directory), invoking the script's default repo path. I discarded that run as evidence; every reported baseline, mutant and restored result uses `--repo /fast/scratch/hyaku/kake-r33/w2/MutC2CounterAtTip/clone`.