# SentinelScope — execution-boundary vectors (kake round 98, C1 + C2 counters)

Scope: `c98_stale.py` candidate execution (`run_one`, `main`) and the git reads of
`c98_stale.py` and `c98_captable.py` (`--revision`, `--fleet-revision`). Lane tip
`7838981e4e40280176085e8aa1f6827eb7133a69`; instruments `2db76835…`; freeze `c3eace8b…`.

Digest check (committed == worktree): `c98_captable.py` `efd598575c6e…`, `c98_stale.py`
`e0331e56378f…` (both at 2db76835 and at master tip; receipt-instrument-digests.txt).

Method and bounds: harmless PoC candidates run only via `--candidate-file` with
`--work` under my scratch `/fast/scratch/hyaku/kake-r98/SentinelScope/` (fixtures and
PoCs there; all markers under scratch). LANE was read-only: no git mutation, no writes;
writability was probed with `os.access(W_OK)` only. Counters run with `python3 -B`.
Tools: none installed. System `python3` 3.14.8, `/usr/bin/git` 2.56.0.

Facts from code (c98_stale.py): `run_one` runs `[python3, -I, -B, cand]` with
`cwd=mkdtemp(work)`, `env={PATH:/usr/bin:/bin, LC_ALL, HOME:cwd}`, `timeout=10`;
`cand` is `work/cand.py`, written once from git bytes and re-executed from disk every case.
Only the per-case dir is removed (`finally: rmtree(d)`); `work` is removed at end of
`main`. `subprocess.run` timeout kills only the direct child. `GENV` is
`dict(os.environ, …)`, unfiltered.

## Register

| ID | Vector | Observed (PoC, receipt) | Rating |
|---|---|---|---|
| SV-1 | Candidate imports the counter's oracle and HAND expectations from LANE (`spec_from_file_location(c98_stale.py)`, `expect()`) | p2: `hand=60/60 generated=240/240 refusals=34/34 met=true` rc 0 (`poc-p2-oracle-read.py.txt`) | carried under R97-5 (declared limit in docstring and freeze) |
| SV-2 | Candidate rewrites its own executed file `work/cand.py`; later cases run different bytes than the printed sha | p3: committed bytes sha `1097db39…`; first case rewrites self to the oracle reader; line 1 prints `sha256=1097db39…` and `met=true`; cases 2–300 executed rewritten code | carried under R97-5 (remedy must re-hash or run a read-only copy per case; otherwise the printed sha is not a statement about executed bytes) |
| SV-3 | Cross-case and cross-run state: candidate persists state via absolute paths; not reset between cases | p2 counter file: 300 cases of p2 + 300 of p3 = `600` (`receipt-p2-state-count.txt`) | carried under R97-5 |
| SV-4 | Writes outside per-case cwd; same-uid write access to frozen files and lane `.git` | p1 marker written from every case to an absolute scratch path (300 lines, `receipt-p1-marker-linecount.txt`). `os.access(W_OK)` true for `SCORECARD.md`, `.ufo/waves/round-98/freeze.md`, `.git/HEAD`, `.git/config` (probed, not written). A candidate can therefore change frozen bytes after the digests were recorded, which the freeze forbids | carried under R97-5. L1 control: re-verify `controls/instrument-sha256.txt` and the scored revision after every run |
| SV-5 | Spawned grandchild outlives case timeout and counter: `start_new_session=True` child is not killed | p4 spawned `sleep 300` once; alive after counter exit (ppid 1487, reparented). PoC killed it; no survivor remained at seat end | carried under R97-5 (process cleanup). Does not change verdicts; can leak one process per run |
| SV-6 | Network egress from candidate | p5: 300 TCP connects to a loopback listener (`receipt-p5-listener.txt`, `conns=300`). External egress not exercised | carried under R97-5 |
| SV-7 | Parent env readable: candidate's reduced env does not hide the counter's env via `/proc/<ppid>/environ` | 35 variables visible; secret-like names present (`PI_TOOL_BRIDGE_TOKEN`, `SSH_AUTH_SOCK`); names recorded only, values not read (`receipt-p6-probe.json.txt`) | carried under R97-5 |
| SV-8 | Scored-revision selection (seed grind). Seed `= int(sha256(commit id)[:8],16)`; the commit id is chosen by whoever lands the candidate, and a message-only change re-seeds the 240 generated cases | Seed formula verified on 3 revisions against the counter output (1795259000, 428231123, 1036764515). Flaw candidate p7: lenient `shared: null` (passes all 60 hand cases; default file-mode seed `generated=239/240 met=false`). Over 10 fixture commits differing only in message: `met=true` at **3/10** (the candidate commit itself among them). Control `pos-oracle` at 4 grind commits: `met=true` 4/4. Freeze does not declare this; the "unknown until the scored commit exists" premise fails when the author picks the commit. Generator rate of `shared:null` ≈ 0.15×(1/9)×(1/3) ≈ 0.56% of cases; no hand case covers it | **BLOCKING for C2.** Route: pin the seed in the frozen contract before any candidate exists (or enumerate the population, or require the verdict across K pinned seeds), and the L1 records the number of revisions scored |
| SV-9 | Option or ref injection via `--revision` / `--fleet-revision` | Every probed form rejected by `rev-parse --verify`: `-h`, `--all`, `--show-toplevel`, `--git-path=HEAD`, `--`, `HEAD --output=…`, `:/Capabilities`, `:`, empty, `--revision=-h/--all/--show-toplevel/:`, `--fleet-revision=--all/-h`, plus `--branches=`, `--glob=`, `--disambiguate=`, `--remotes=`, `--tags=`, `--exclude=`, `--show-superproject-working-tree`, `--git-path=SCORECARD.md` (all rc 128 "Needed a single revision"). Stale counter: "setup-error bad revision". `@` resolves to HEAD (benign) | none |
| SV-10 | Working-tree reads instead of committed bytes | Both counters read only `git show <rev>:<path>` and `cat-file -e <rev>:<path>`, `rev` being the rev-parse output (a commit id). Index form `:path` is unreachable under `--verify <x>^{commit}` | none |
| SV-11 | Committed attributes or textconv changing `git show` bytes | Committed `.gitattributes` `diff=zz` plus local `diff.zz.textconv = tr a-z A-Z`: `git show <rev>:path` returned untransformed bytes (sha equal to `cat-file blob`); counter sha `bfb48d81…` = committed | none |
| SV-12 | Replace refs | `git replace <bad blob> <good blob>` in fixture: counter scored the committed bad blob (`sha256=6d8e0809…`, `hand=14/60 met=false`). `GIT_NO_REPLACE_OBJECTS=1` effective | none |
| SV-13 | Inherited `GIT_*` environment redirects reads (`GENV` copies `os.environ`) | `GIT_DIR=<fixture>/.git` with `--root LANE --revision HEAD`: scored the fixture's candidate (`met=true`, sha `bfb48d81…`); env unset: `candidate=absent` (LANE HEAD has no candidate, `cat-file -e` rc 128) | none for the frozen claim when the scoring shell is clean (L1 receipt must show `env` has no `GIT_*`). Hygiene: allowlist `GENV` |
| SV-14 | `--candidate-file` overrides `--revision` silently | Line 1 prints `source=candidate-file`; frozen predicate scores `--revision` only | none (visible label) |
| SV-15 | Unbounded candidate stdout, memory, CPU; no rlimits | Not exercised (no resource PoC run) | carried under R97-5 (unmeasured) |

Counts: vectors = 15; blocking = 1 (SV-8). Carried under R97-5: SV-1..SV-7, SV-15 (8).
None: SV-9..SV-14 (6).

Not exercised: external egress, memory or CPU exhaustion, grafts/shallow/partial-clone lazy
fetch, and any mutating git against LANE. c98_captable.py per-row review conjunct is out of
scope here.

## Receipts (flat, in this seat dir)

- `poc-p0-control-pos.py.txt` … `poc-p7-flaw-shared-null.py.txt`: candidate sources (renamed `.txt`; not lane code)
- `receipt-p1-marker-head3.txt`, `receipt-p1-marker-linecount.txt`, `receipt-p2-state-count.txt`, `receipt-p5-net.txt`, `receipt-p5-listener.txt`, `receipt-p6-probe.json.txt`
- `receipt-instrument-digests.txt`
- `receipt-grind.txt`: the 10 grind results and control, verbatim from the run

Verdict line: SENTINEL vectors=15 blocking=1
