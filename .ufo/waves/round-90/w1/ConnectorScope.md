VERDICT: C2's frozen predicate holds (4/4, 57/57 reproduce), but the gate's sandbox claim does not. A candidate that implements nothing and hands stdin/stdout to an unhooked child interpreter through `_posixsubprocess.fork_exec` is admitted `met=true sandbox=ok` at the carrier. chousa found this class of bypass in rounds 54 and 56. The uncommitted working-tree gate fix (`11eb630a…`) now refuses the shipped positive. C1's D2 receipt re-runs byte-identically. No sibling PROVINCE is contested. No staged theme fits this round. 8 staged ids collide.

Seat ConnectorScope (round 90, w1). All paths are absolute. The receipts are in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/w1/ConnectorScope/`, with checksums in `SHA256SUMS`. Lane HEAD `79e1aac2`. Python 3.14.8. No tools installed. No network GETs.

## 1. Cross-lane scan (read-only, `/home/vgpnk/Projects/shokunin/*-shokunin`, kake excluded)

**Method.** I ran `grep -rIlE` per lane for `cache[-_ ]key`, `\bVary\b`, `addaudithook|audit[- ]hook`, `RFC ?9110`, `RFC ?9111`, `RFC ?8259` and `conformance[- ]gate`, excluding `.git`. The raw counts are large: kotoba has 496 `cache key` files and game-dev-3d has 282. Those are build and content caches, not HTTP. I narrowed to files outside `.ufo/` that contain `Vary` together with RFC 9110/9111 or `cache key`. Only mori matched. I did not classify every raw hit.

**Overlaps (file:line)**
- **mori S594**, `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:375`: RFC 9111 §4.1. Its scope reads "the Vary-selected representation and the cache-key rule". It pins sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` (84477 bytes). kake's retained `rfc9111.txt` in the round-90 lesson Gate (`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-90.md:14`) has the same hash, so the two lanes independently agree on the bytes.
  - Mori uses the clause for reuse and matching: a per-User-Agent byte difference is not drift. The sources are `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/ua-serving-normative-r79.md:1-5`, `:40` (which disclaims vendor negotiation) and `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/README.md:861`.
  - kake's ground is key *construction* only (`/home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md:703-720`, and the contract Scope at `.ufo/waves/round-89/c2-contract.md:82-89`).
  - **Not contested.** Mori's PROVINCE.md has no cache/Vary claim; `grep -nIiE 'cache|vary'` on it finds only unrelated HTTP lines.
  - The only friction is wording: mori's scope cell says "cache-key rule" for what kake treats as the matching half. If kake ever widens into reuse or matching, mori r79 is prior ground, and the two should cross-cite rather than duplicate.
- **Other RFC rows in sibling registries**, all on different sections, so no overlap with S466–S468:
  - RFC 9110: mori S042 §10.2.3 (`mori…/SOURCES.md:48`), mori S221 §15.4 (`:227`), tabi S107 redirects (`tabi…/SOURCES.md:121`), chousa S061 404/410 (`chousa…/SOURCES.md:71`).
  - RFC 9111: chousa S025 §4.2 tier C (`:35`), kumitate S237 §5.1 Age (`kumitate…/SOURCES.md:191`).
  - RFC 8259: chousa S062 §4 (`:72`), mori S545/S546 (`mori…/SOURCES.md:325-326`).
  - No sibling lane holds RFC 9110 §5.5: the CR/LF/NUL grep over sibling SOURCES and knowledge returned no rows. kake's S466 is unique.
- **Audit-hook sandbox: a real cross-lane precedent the round did not use.**
  - chousa round 54, `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-54/w1/R54ReviewC1Counter.md:5-15`: "audit hook does not enforce the claimed no-spawn boundary". A forge via ctypes libc `system` passed the frozen counter.
  - chousa round 56, `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-56/w1/R56ConnPattern.md:26`: "Incomplete audit hook & descriptor bypass… patched only two strings in `BAD`".
  - kake's gate repeats the pattern; see §1a. kama also runs an audit-hook guard (`/home/vgpnk/Projects/shokunin/kama-shokunin/tests/ollama-corpus-guard/check.py`, `tools/round58-battery-exec-check.py`). I did not test it.

### 1a. Falsifier: the carrier gate's sandbox admits process spawn and oracle delegation

The gate is at its carrier bytes: `scripts/cache_key_conformance.py` sha256 `2840f32e53317327fbaa6df3f8e02da06363e0fcda829270651a356192517591`, equal to `git show 7f6c68f1:` and `HEAD:` at test time.

The claim under test is at `:9-10`: "spawn no process … A violation ends the candidate's process at once with exit 97". The carrier `_DENY` at `:294-298` lists `subprocess.Popen` and `os.fork` but not `_posixsubprocess`. `_posixsubprocess` is in `sys.stdlib_module_names`, so the import passes the allowlist, and `fork_exec` raises no audit event.

- **Spawn probe.** `probe_spawn.py` is `prefix.py`, which forks `/bin/sh` to append to a marker file, followed by `scripts/cache_key.py` verbatim.
  - Command: `TMPDIR=<scratch> python3 -B scripts/cache_key_conformance.py --candidate probe_spawn.py --seed 90 --work <scratch>/w`
  - Result: `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok seed=90 met=true`, exit 0. The marker had 193 lines, one spawned shell per case.
  - Receipt: `ConnectorScope/gate_probe_spawn.txt`.
- **Delegation probe.** `probe_delegate.py` implements no key logic. It `fork_exec`s a fresh `python3 -B …/scripts/cache_key.py` that inherits fds 0/1/2.
  - Result: `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok seed=90 met=true`, exit 0.
  - Receipt: `ConnectorScope/gate_probe_delegate.txt`.
  - This is the delegation the gate's knowledge entry says it stops: `corpus/knowledge/cache-key-conformance-gate.md:35` ("an oracle import or an exec of a counter file is not an implementation") and `:46`.
- **Control.** The shipped candidate on the same gate gave `met=true`, exit 0 (`ConnectorScope/gate_shipped.txt`).
- **Effect on C2.** C2's predicate is untouched because the frozen 57-subject population has no child-process negative. The defect is in the gate's capability claim and the knowledge entry's Sandbox row, not in the counter's arithmetic.
- **Independence.** ScoutGround found this independently in the same wave (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/w1/ScoutGround.md:1,8`, with `ScoutGround/neg-forkexec-delegate.py`; ExecSandbox has `c11_posixsubprocess_cat.py`). This seat corroborates it and adds the chousa precedent above.

### 1b. Harm: the uncommitted working-tree gate fix refuses the shipped positive

L1's working tree carries an uncommitted `scripts/cache_key_conformance.py` (sha256 `11eb630adcb104b4b64c9e4834ac8344fe9a44ba62973f78807d3c565ff18664`; `git status` ` M scripts/cache_key_conformance.py`). It widens the deny lists. The new import denylist includes `_posixsubprocess`, `ctypes` and `resource`, and the event prefix list includes `"marshal.load"`.

`"marshal.load"` is a prefix of `marshal.loads`, and CPython's importlib raises `marshal.loads` when it loads any cached stdlib `.pyc` (for example `json`). So every candidate dies on its first import.

- Run on a byte copy (`ConnectorScope/wip_gate_runs.txt`):
  - `candidate=cache_key.py exit=1 :: clauses=0/6 hand=0/85 generated=0/120 sandbox=violation met=false`
  - The `--verbose` reason is `SANDBOX_VIOLATION marshal.loads`.
- If committed as is, this gate fails C2's positives 4/4 → 0/4: a blanket refuser that the pre-freeze `ctl-c2` blanket-refuse control already shows is not met.
- The cure is to match the exact event `marshal.load`/`marshal.loads` only when the call is not from importlib, or to drop it. Re-run c90_gate before committing.
- Limit: this is a snapshot of in-flight L1 work and may already be superseded. The sha above identifies the bytes tested.

### 1c. Note: `sandbox=violation` is not diagnostic

At the carrier, 8 of the 61 subjects read `sandbox=violation` (count from `controls/after-c2-carrier.txt` line 2). With the fixture gate below, an uncaught exception in the candidate also ends as `SANDBOX_VIOLATION open …/sandbox.py`: traceback rendering opens the prelude file, which is outside the stdlib roots. A refusal labelled "sandbox" can therefore be an ordinary crash. Verdict polarity is unaffected, but per-subject refusal reasons in receipts should not be read as sandbox hits.

## 2. shokuknow merge package (read-only, nothing run there)

Sources: `/home/vgpnk/Projects/shokuknow/merge/kake/MERGE-REPORT.md` and `SOURCES.append.md`.

- **No theme fits this round's ground.** The staged package is rounds 1–16 publishing work: crawl, robots, CrUX, Baidu, Yahoo Japan, Chinese static hosting, Kimi, Jekyll. Grepping it for cache/Vary/RFC 9110/9111/8259/JSON gives only S306 (`SOURCES.append.md:26`, a kimi.page header spot check that records `cache-control: private, no-cache, no-store`). That is Cache-Control storability, which the contract scope excludes (`c2-contract.md:84-86`), so it is not key-construction ground.
- **The report's header is stale.** It says "lane registry currently holds **145** rows; first staged id is **S287**" (`MERGE-REPORT.md:9`). The lane now holds 205 rows, up to S468.
- **Id collisions.** I extracted ids with the 0–3-leading-space pattern `^ {0,3}\| *\KS[0-9]+(?= *\|)` on both files: 129 staged ids, 205 lane ids, no duplicates inside the lane. **8 collide:** S312, S329, S367, S372, S373, S374, S390, S409 (`ConnectorScope/collide.txt`).
  - Each pair is the same source URL, already adopted into the lane at `corpus/SOURCES.md:154-161`.
  - None is byte-identical. Lane/staged lengths: S312 906/903, S329 929/1130, S367 1083/1185, S372 1156/1251, S373 1011/1108, S374 863/994, S390 876/1147, S409 808/920.
  - Appending `SOURCES.append.md` as instructed (Adopt checklist step 3) would create 8 duplicate ids with diverging text. Those 8 rows must be skipped or reconciled, not appended.
  - The other 121 staged ids fall in lane gaps (S287–S311, S313–S328, S330–S366, …). They would not collide, but they would interleave pre-round-90 publishing rows into an id range the lane left open.

## 3. considerthese (latest: `/home/vgpnk/Projects/shokunin/kake-shokunin/considerthese/2026-10-26.md`)

**Proposal bearing on this round:** Part 2 item 2, "Receipt-rewrite watch" (`considerthese/2026-10-26.md:30`). As written it says to flag files under `.ufo/waves/round-*/controls/` that have more than one commit, using `git log --follow`. I found no evidence it has been implemented. It bears directly on C1 item D2 ("a correction counts only if its receipt re-runs").

- **Its method is broken as written.** `git log --oneline --follow` reports 35, 34 and 3 commits for `round-90/controls/census-before.txt`, `census-after.txt` and `r89-c1-at-f62e7954.txt`. Without `--follow`, each has exactly 1 commit. `--follow` attaches copy-detected ancestors from older rounds, for example `C099 round-89/controls/census-final-after-s464-drop.txt`. The watch would flag every census file every round. It needs `--no-follow` or `--diff-filter=AM` on the exact path.
- **That copy detection is worth checking, though.** `r89-c1-at-f62e7954.txt` is detected as a `C090` copy of `round-89/w1/ScribeLesson/receipts/c1-at-carrier-21770586.txt`, and only the revision line differs (`diff`).
  - I re-ran it independently. The frozen counter from `git show 209027f4:.ufo/waves/round-89/c89_defect_queue.py` has sha256 `0ebea07f…`, equal to the working copy. Command: `python3 -B c89.py --root LANE --revision f62e7954 --work <scratch>`.
  - Result: `C1v1 revision=f62e7954… items=6 open=5 closed=1 met=false`, exit 1. The body is byte-identical to the committed receipt (`ConnectorScope/r89-c1-at-f62e7954.rerun.txt`). The lesson's Mistake 2 receipt is genuine.

## Proposed move (one, bounded)

Close the sandbox's process boundary with a kernel limit instead of growing the denylist:

```python
import resource
resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))
```

placed in the `SANDBOX` prelude right before `sys.addaudithook`. Chousa r56 shows denylist patches miss paths. `RLIMIT_NPROC=0` makes every fork/clone path fail with EAGAIN: `_posixsubprocess`, `os.fork`, and ctypes-loaded libc `fork`/`system`.

- **Unit probe.** `fork_exec` → `BlockingIOError 11` and `os.fork` → refused (`ConnectorScope/rlimit_probe.txt`).
- **Fixture.** One `--shared` clone; I checked toplevel before committing. Fixture commit `3424939e`, two-line patch `ConnectorScope/rlimit.patch`.
  - `probe_delegate.py` → `met=false`, exit 1, marker 0 (`fx_probe_delegate.py.txt`).
  - `probe_spawn.py` → `met=false`, marker 0 (`fx_probe_spawn.py.txt`).
  - The shipped candidate → `6/6 70/70 120/120 met=true`, exit 0 (`fx_shipped.txt`).
  - The frozen counter `c90_gate.py --root <fixture> --revision HEAD` → `positives=4/4 negatives_refused=57/57 false_admits=0 errors=0 anti_table=ok population=ok met=true`, exit 0 (`c90_on_fixture.txt`).
- **Axes.** Operability (C2 gate soundness) improves. The C2 predicate and the positives are unharmed, as the fixture shows. C1 is unaffected.
- **Risks.**
  - RLIMIT_NPROC is per real uid and ignored for root or CAP_SYS_RESOURCE. Under root the gate must refuse to run, or add the import deny.
  - Threads count toward NPROC on Linux, so a threaded candidate would fail. No positive uses threads (`grep thread scripts/cache_key.py` is empty).
  - It does not cover sockets or file writes; the audit hook still owns those.
  - It must not be combined with the WIP `resource` import deny (§1b), which would block the prelude's own import if the prelude ran after the hook.
- **Verification for L1.**
  1. Add `probe_delegate`-style and ctypes-`system` negatives as new frozen subjects in a later round. This round's population is frozen.
  2. Re-run c90_gate on the carrier that contains the change.

## Limits
- The sibling scan is grep-based and only the narrowed subset was read. Raw counts include `.ufo/` dispatch text.
- `fork_exec` arity is specific to Python 3.14. On other versions the probe may need adjusting; that does not change the class of bypass.
- The WIP gate finding is a snapshot of uncommitted bytes.
- Scratch `/fast/scratch/hyaku/kake-r90/ConnectorScope/` was deleted after the receipts were copied. No writes outside this seat's two paths and scratch.
