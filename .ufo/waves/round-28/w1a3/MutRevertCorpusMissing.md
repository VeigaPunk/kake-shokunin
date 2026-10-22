# MUT-TESTER REPORT: MutRevertCorpusMissing (C1 counter sensitivity)

Round 28 attempt 3, wave 1. Leaf seat; no subagents used. Fleet repo untouched; all git/source work in own sandbox clone.

## Task
Mutate the repaired C1 gate so `WorkingTreeSource.corpus_files` returns `[]` again when `corpus/knowledge` is absent (one mutation only), commit in the clone, run `c1_interface_count.py` at the mutated HEAD and at the unmutated reference `b5d423fc02057f67a6f3a255808313ce40d29069`. Expect: counter drops below 15/15, failing check includes A1, controls K1-K4 still pass.

## Mutation
File: `scripts/citing_set.py`, `WorkingTreeSource.corpus_files`, `except FileNotFoundError:` branch (lines 244-245 in the clone).

```
-            raise InputInvalid("corpus_directory_missing", CORPUS_DIR, "corpus")
+            return []
```

One behavior-bearing point: the absent-corpus surface now looks empty instead of being refused. Diff (single hunk, `-2/+1`): recorded below. Commit in clone: `965b4c03596c9e4f3a2365eb71e005427955b2e8` (author mut/mut@invalid).

Hashes (sha256 of `scripts/citing_set.py`):
- Pristine (b5d423f, lane repair commit): `28ba996524b444b2e1c23e3751f3fa662a9a44adbfcb6337a0d23fcebaf8f415`
- Mutated (clone HEAD): `223d104c143ce2b08979c2acbaab2fb475473e24c99a692e13afd72c3f41c412`

## Commands and exit codes
All ran from the sandbox. `C=…/MutRevertCorpusMissing/clone`, `S=…/MutRevertCorpusMissing`.

1. Clone: `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin $C` — exit 0; HEAD was `b5d423fc…`, `status --short` empty (0 lines).
2. Mutation edit via `edit` tool (no shell sed/perl). Verified by `git diff b5d423f HEAD` (hunk above).
3. Commit: `git -C $C -c user.name=mut -c user.email=mut@invalid commit -qam mut` — exit 0.
4. Counter, mutated: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-28/c1_interface_count.py --root $C --revision HEAD --scratch $S/count` — **exit 1**.
5. Counter, reference: same with `--revision b5d423fc02057f67a6f3a255808313ce40d29069 --scratch $S/count-ref` — **exit 0**.

## Observed outputs
Mutated HEAD `965b4c0` — passed 14 / 15; defect 10/11; control 4/4.
Failing check: **A1-corpus-absent-working-tree** (defect): reasons `exit 0, want 2`, `verdict 'clean', want 'could-not-evaluate'`, `no input_invalid finding`; observed exit 0, verdict `clean`, no `input_invalid` finding.

Reference `b5d423f` — passed 15 / 15; defect 11/11; control 4/4; no failures.

Both runs: stderr empty; no timeouts; `K4-fixture-selftest` included in the 4/4 controls.

## Verdict
**KILLED.** The counter catches the reverted gate: the only regression the mutation causes (A1) is detected, all other 10 defect checks and all 4 controls (K1-K4) still pass. Counter is sensitive to the C1 repair at exactly the routed-defect point. No surviving mutant; no counter gap found.

## Evidence
- Counter JSON (full case listing): `$S/count-head.json` (14/15, A1 failure details), `$S/count-ref.json` (15/15). Stderr files empty.
- Mutation diff: `git -C $C diff b5d423fc02057f67a6f3a255808313ce40d29069 HEAD -- scripts/citing_set.py` (single hunk, shown above).
- Commit: clone HEAD `965b4c03596c9e4f3a2365eb71e005427955b2e8`.

## Not verified
- No installs performed (none needed; no tool changes to record). No pacman/uv activity.
- Did not inspect the L1's drafted `corpus/knowledge/field-performance-cwv.md` (C2 scribe scope); irrelevant to this probe.
- Fleet lane, sibling lanes, and lane git/jj state untouched; no commands run in `/home/vgpnk/Projects/shokunin` other than read-only `read`/`edit`-free access and the counter invocation listed above.
