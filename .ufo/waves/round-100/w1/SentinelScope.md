# SentinelScope — round 100 W1 report (sandbox attack on the two round-100 counters)

Seat: SentinelScope (leaf, no subagents). Target: the sandboxes both counters added this round:
`c100_fresh304.py` (`SANDBOX`, `run_candidate`, `sandbox_ok`) and `c100_registry.py` (`sandbox_argv`,
`run_span`, `probe`). Ledger with every attempt, command and observed value: `w1/SentinelScope/vectors.md`.
PoCs: `w1/SentinelScope/poc-registry-probe-gaming.py`, `poc-registry-scored-tree-write.py`,
`poc-registry-failopen-bwrap.py`, `poc-fresh304-sandbox-probe.py` (outputs in `poc-*.out.txt`).
Receipts: `w1/SentinelScope/receipt-*.txt`.

Frozen-instrument hygiene: digests verified first (`sha256sum -c controls/instrument-sha256.txt` → 21/21 OK).
Counters imported read-only with `python3 -B`; nothing in the lane was written; no instrument patched.
Findings below are routed to L1, not repaired.

## Verdict summary

| Boundary | Result |
|---|---|
| Host escape from either sandbox (fs, network, processes, counter memory) | none observed (F1–F10, F14, F16, R6–R8, R11) |
| Outlive the case (daemon survives teardown) | none observed, both counters (F9, R8) |
| Cross-case persistence via tmpfs/ipc | none for C2 (F14); **yes for C1** via the shared scored tree (R3, R4) |
| Counter bypass (scored `met=true` while committed tool misbehaves) | **yes** (R1 probe-aware, R2 sandbox-detect, R12 bwrap fail-open) |
| Resource exhaustion | RAM via tmpfs (F12), disk without quota (R9), time 120–240 s per hostile probe/span (R10), unlimited fork within the uid's NPROC (F11) |

Acceptance line: `SENTINEL vectors=28 escapes=0 cross_case_leaks=2`.

## Findings (severity, exploit path, evidence, impact, smallest remediation)

### R1 — C1 D2 probe is gamed by a tool that recognises the probe argv (High for C1 integrity)
- Exploit path: a committed `scripts/x.py` exits 0 only for `sys.argv[1:] == ['--zz-bogus-r100']` and returns
  the real unmapped code 64 for every other unknown flag. The verdict map names `0` and `1`.
- Evidence: `poc-registry-probe-gaming.out.txt`: `probe-aware met=True … probe_mismatch=0 … real rc for --zz-other=64`;
  the honest control `met=False probe_mismatch=1 rc=64`. The probe token is also disclosed to scored tools (R5).
- Impact: D2 certifies the probe's answer, not the tool's behaviour. `met=true` does not imply the committed tool
  returns the mapped codes on any other unknown flag. This is not the freeze's declared limit (which covers maps
  naming extra codes); it is a bypass of the probe itself.
- Smallest remediation: the counter chooses a fresh random unknown token per run (`secrets.token_hex(8)`), never
  stored in tracked files, and checks that the exit code matches the map for that token; optionally repeat with a
  second random token and require agreement. A tool can still recognise "unknown flag" in general, so pair this with
  the review conjunct for behavioural cases.

### R2 — sandbox detection by pid (Medium, same class as R1)
- Exploit path: `os.getpid()==2` (the counter's bwrap makes the tool pid 2 in a fresh pid namespace) selects a
  different answer inside the probe. Evidence: `poc-registry-probe-gaming.out.txt` `sandbox-detect met=True`,
  real rc 64; F15 shows the detection itself works. Remediation: run the random-token probe also outside the
  sandbox and require identical codes (a tool keyed on pid/argv disagrees), or accept as a documented limit.

### R3 + R4 — the scored tree is one read-write extraction shared by every span and probe (High, C1)
- Exploit path (R3): a self-test span (`python3 -B scripts/a.py --selftest`) rewrites its own file under
  `tree/` (`__file__` relative, cwd = tree, bind is rw). The probe that runs later executes the rewritten file.
  Evidence: `poc-registry-scored-tree-write.out.txt` `self-rewrite met=True`, tree sha `14c75fb904c5` vs committed
  `5261ab80cb0f`; committed file still exits 64.
- Exploit path (R4): row a's self-test writes `scripts/b.py`; row b ("no self-test", no sandbox run of its own) is
  then probed on the rewritten file. Evidence: `… cross-row met=True tools=2 probe_mismatch=0`, committed b sha
  `7626264709c3` exits 64 on unknown flags.
- Impact: a committed tool can change what another row's probe measures, so `met=true` can be produced by a tree
  the lane never committed. Two cross-case leaks.
- Smallest remediation: bind the extracted tree read-only (`--ro-bind`), and give each span/probe its own
  throwaway copy of the tree (or re-extract per row). Keep only the per-run scratch writable.

### R12 — C1 fails open when bwrap itself fails (High for counter integrity)
- Exploit path / failure: `c100_registry.py` `probe()` takes bwrap's exit code as the tool's exit code; it has no
  `sandbox_ok()` gate (unlike `c100_fresh304.py`). With a bwrap that exits 1 before running anything, the probe
  rc is 1, which a map naming `1` accepts.
- Evidence: `poc-registry-failopen-bwrap.out.txt`: `broken-bwrap-shim … direct probe rc=1 … met=True`;
  `control-real-bwrap … direct probe rc=64 … met=False`. The fresh304 counter under the same broken bind:
  `sandbox_ok: False` → exit 2 (F16).
- Impact: a C1 `met=true` can be produced with no tool executed when the namespace setup fails (the "exit 2
  could-not-evaluate" promised in the docstring does not happen).
- Smallest remediation: port `sandbox_ok()` (a probe with a known-good program that must print its own pid 2 and
  an isolated `/proc`) into `c100_registry.py` and exit 2 on failure; treat a bwrap-originated failure (stderr
  prefixed `bwrap:`) as `could-not-evaluate`, not as a tool exit code.

### R5 — instrument sources are inside the scored tree (Medium)
- Evidence: `git ls-tree -r --name-only e84a187…` lists `.ufo/waves/round-100/{c100_registry.py,c100_fresh304.py,freeze.md}`;
  the registry's `git archive` extraction therefore contains them. `receipt-registry-out-oracle.txt`: a scored tool
  reads `c100_registry.py` (`has_probe_arg=True`) and `c100_fresh304.py` (`has_fresh304_reference=True`).
- Impact: the D2 token (R1) and the whole C2 reference implementation are readable by every tool that runs under
  the registry. C2's own predicate is not reachable this way (its candidate runs with no tree bound), but the
  oracle is no longer unseen by anything the registry executes.
- Smallest remediation: exclude `.ufo/waves/` from the registry's archive (`git archive … -- ':(exclude).ufo'`) and
  take the probe token from a per-run random value (R1).

### R9 + R10 — no disk quota, no time aggregate, long per-probe waits (Medium)
- R9: a self-test wrote 256 MiB into the tree on host `/fast` (`receipt-registry-out-…`: `bigfile.bin size 268435456`);
  no `RLIMIT_FSIZE` (unlimited, F13). Bounded only by the 240 s span timeout; the rate beyond 256 MiB was not measured.
- R10: a hostile probe costs 120.0 s (`rc=124`), a hostile span 240 s; no total budget across rows.
- Remediation: `RLIMIT_FSIZE` and `RLIMIT_CPU` in a `preexec_fn`, a total wall-clock budget per score run.

### F12 — C2 candidate can drive host RAM through the /tmp tmpfs (Medium)
- Evidence: `receipt-fresh304-drive-out-2.txt`: tmpfs total 16,241,557,504 B (half of 30 GiB RAM); a 2 GiB write
  completed in 0.25 s; host `free` fell by ~1.9 GB during the write. [INFERENCE] a single 10 s case can fill ~15 GiB.
- Impact: host memory pressure from a scored candidate. Not an escape, but it can starve other seats.
- Smallest remediation: a memory cgroup (`systemd-run --scope -p MemoryMax=…`) around the case, or a size-limited
  tmpfs if the bwrap build offers it (not verified here).

### F11 — fork without a pids limit (Low–Medium)
- Evidence: 200 forks in 2.02 s; `RLIMIT_NPROC=122865`, which is the real uid's limit, shared with the operator's
  session; no pids cgroup in the sandbox. A full bomb within 10 s is [INFERENCE], not run.
- Remediation: pids cgroup (`TasksMax=`) for the case.

### F13 — no seccomp filter and no resource rlimits (Low hardening)
- Evidence: `Seccomp: 0`, `Seccomp_filters: 0`, `NoNewPrivs: 1`, `CapEff: 0`; `RLIMIT_AS/FSIZE/CPU` unlimited.
- Not exploited. Remediation: `--seccomp` filter fd for bwrap; rlimits in the child.

### F16 gap — `sandbox_ok()` checks only pid visibility (Low; C2 gate is otherwise sound)
- `sandbox_ok()` passes if the pid list is `['1','2']`; it does not check network isolation, the read-only binds,
  or the absence of host paths. A partially broken sandbox that keeps the network would still pass the gate
  [INFERENCE from the code; the network was isolated in this run (F8)].
- Remediation: add a loopback-listener and `/home`-absence check to `sandbox_ok()`.

### F4 — mount table discloses the counter's work-dir name (Low)
- `/proc/self/mountinfo` shows the bind source host path (`…/c100f-*/freshen_304.py`). Nothing readable is behind it.
  Remediation: pass the candidate through a pipe/memfd or a copied file in tmpfs.

## C2 predicate impact
None of the observed escapes affects `candidate=present hand=… generated=… met=…` for C2: every C2 sandbox attempt was
blocked (F1–F3, F5, F7–F10, F14) or detection-only (F15). The C2 counter's fail-closed path works (F16). Nothing here
suggests the C2 result is contaminated by sandbox leakage.

## C1 predicate impact
R3, R4 and R12 mean a C1 `met=true` at the repair commit can be produced by a tree that was not committed, or with
no tool executed. R1 and R2 mean a committed tool can satisfy D2 by recognising the probe. The review conjunct and
the repair-commit checks do not cover these cases. L1 should treat C1 `met=true` as not established by the counter
alone until R3/R4/R12 are closed, or record the limit explicitly in the round.

## Tooling record
No tools installed or updated. Used: `/usr/bin/bwrap` 0.13.1, `/usr/bin/python3` 3.14.8, system `git` (read-only).
A PATH shim named `bwrap` (a real bwrap with a missing bind source) was created only inside my scratch to simulate a
failing sandbox; it was not placed in any PATH directory. Sysctls and host config were not touched.

## Scratch and cleanup
Seat scratch `/fast/scratch/hyaku/kake-r100/SentinelScope/` (fixtures, work dirs, 256 MiB and 2 GiB test files) is
deleted before yield; receipts were copied into `w1/SentinelScope/` first.

SENTINEL vectors=28 escapes=0 cross_case_leaks=2
