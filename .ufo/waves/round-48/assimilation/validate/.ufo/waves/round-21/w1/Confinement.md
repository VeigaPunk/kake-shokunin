# Confinement — round 21 w1 (sentinel)

Scope: a static review of the corpus-contract gate draft against four confinement requirements: a read-only normal path, temp-only selftests, no unsafe subprocess shell, and no credential surfaces. **Nothing was executed.** I did not run the script, its `--selftest`, or any test, per the assignment and the KakeR21 wrap-up instruction.

Target reviewed: `scripts/corpus-contract.mjs`, 610 lines, sha256 `ca6f685e0b826a40894990b4f536d272ba3e948444e7ab74fb41602bbdf0ed29` (mtime 2026-10-20 06:06:57 -0300). The file is untracked on base `5009eca`. If the file changes after this hash, these findings do not apply to the new version.
Contract reference: `~/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:388-435` (§Gate standard: self-test over "temp trees, no network, no live-tree write"; Scope "read-only over surfaces it does not own").
Precedent compared: `scripts/freshness-sweep.mjs` (writeConfinement 1078-1134, selftest 1137-1525).

Axes: confinement (writes, subprocess, credentials) · gate integrity (fail-open paths).

## Verdict per requirement

| Requirement | Status | Evidence |
|---|---|---|
| Normal path is read-only | **Met** | `main` 599-608 → `evaluate` 187-245 calls only `fs.readdirSync` (181) and `fs.readFileSync` (131, 147). The normal path has no write API, no `process.env` read, no network, and no `os.homedir`. |
| Selftests write only to temp | **Met, with 2 low gaps** (F4, F5) | The only write regions are 405-479 (fixture build) and 587-589 (cleanup). The fixture root is `fs.mkdtempSync(path.join(os.tmpdir(), 'kake-corpus-contract-'))` (406): a unique directory with mode 0700. `rmSync` (588) targets only the path that mkdtemp returned. This is an improvement over freshness-sweep, which uses a fixed `/tmp/kake-r16/selftest` that `KAKE_SELFTEST_DIR` can override, and creates a fixture under `$HOME`. |
| No unsafe subprocess shell | **Met today; the proof does not check it** (F2) | The only child call is `execFileSync(process.execPath, [SELF, ...args], {encoding, stdio})` (381): argv array, no `shell` option, called only inside `selftest()`. All children get `--root <tmp>`, or exit at usage before `evaluate` (c6). No child passes `--selftest`, so selftest cannot recurse. |
| No credential surfaces | **Met** | Output contains only the root path, relative corpus paths, field names, detail tokens and `e.code`/`e.message`. File content is never echoed, so even a misdirected read cannot exfiltrate secrets through findings. Symlinked entries are not read at all (see F1). The script reads no env except `TMPDIR` (through `os.tmpdir()`, in selftest only), reads no auth or credential files, and makes no network calls. |

## Findings

### F1 — Medium: symlinked or non-regular `.md` entries fail open without being reported
- **Exploit path:** replace `corpus/lessons/round-5.md` (or any knowledge entry) with a symlink, for example `round-5.md -> round-5.orig.md`, or a dangling link.
  - `listMd` filters on `d.isFile()` (182). A `readdir` Dirent for a symlink reports `isSymbolicLink()`, not `isFile()`, so the entry is silently dropped.
  - It is not counted as checked, not listed in `skipped`, and not reported in `errors`.
  - The gate then exits 0 with `lessonsChecked` one lower. The same happens to a directory named `x.md`.
- **Impact:** a lesson can evade C2, or a knowledge entry can evade C1, while the gate is green. The draft pins no expected population: `EXPECTED_BARE` (369) deliberately makes an empty corpus clean. So the drop shows only as a changed count that nothing asserts.
- **Confinement upside, not a defect:** symlink targets are never read, so this cannot be used as a credential-read path. The `corpus/knowledge` and `corpus/lessons` directories themselves are still followed if they are symlinks, through `readdirSync`. That is read-only and content is never echoed.
- **Current tree:** `find corpus -type l` returns nothing (checked 2026-10-20), so this is latent, not live.
- **Smallest fix:** in `listMd`, return every `*.md` Dirent, and in `evaluate` push `{file, error: 'non-regular-entry'}` to `errors` (exit 2) for any entry where `!d.isFile()`. Add one selftest fixture (`fs.symlinkSync` inside the BEGIN/END region) that pins exit 2.

### F2 — Low/Medium: the read-only proof (e1) is weaker than the header claims
The header (30-35) claims that the only write calls "sit inside SELFTEST-WRITES-BEGIN/END marker pairs **in selftest()**", and that `--selftest` proves it. Three gaps separate that claim from what e1 checks:
- **a. A region is only bounded from below.** `inside` checks that each marker line is greater than the line where `selftest()` is declared (575-577). It never checks that the marker is before the end of `selftest()` (596). A future `// SELFTEST-WRITES-BEGIN` … `END` pair wrapped around a write in `main()` (599+) would pass e1. freshness-sweep has the same weakness (`regionsInSelftest`, 1501-1502).
  - **Fix:** compute the line where `selftest()` closes (the first column-0 `}` after `decl`) and require `decl < r < end` for every region.
- **b. Child-process calls are outside the scanner's scope.** The header documents this (321-322). The "no unsafe subprocess shell" property is therefore true by inspection, not by proof. A later `exec(`, `execSync(`, `spawn(…, {shell:true})` or `execFileSync('sh', ['-c', …])` anywhere would pass e1.
  - **Fix:** a second scan, so the property is proved rather than inspected:
    - assert that the child_process import is exactly `{ execFileSync }` (53);
    - assert that every `execFileSync(` call is inside `selftest()`, its first argument is `process.execPath`, and the file never contains `shell:`.
- **c. The API list is not pinned.** e1 has one positive control (`writeFileSync`, 567-568). Deleting a name from `syncNames`/`directNames` (279-287) would silently narrow the scan. freshness-sweep pins its list with `apiPin === '31:cf1b238d8d9f2486'` (1500) plus a mutation loop over each API name; this draft has neither.
  - **Fix:** loop the positive control over every entry in `apis`, and pin `apis.length === 31`.

### F3 — Low: filenames are untrusted input and are echoed raw in human mode
- `file` is built from `d.name` (199, 220) and printed unescaped in `FAIL`/`SKIP`/`ERROR` lines (266-269). A name ending in `.md` that contains `\n` can forge a `result: 0 findings … exit 0` line in text output.
- The exit code and `--json` (escaped by `JSON.stringify`) stay authoritative, so only a human reader skimming the text could be misled.
- **Fix:** report names that match `/[\x00-\x1f]/` as errors (exit 2), or print `JSON.stringify(file)`.

### F4 — Low: the selftest temp tree leaks if fixture build or a case throws
- Cleanup (587-589) is straight-line code, not in a `finally`. An exception thrown after line 406, for example ENOSPC during a `put` or EACCES, propagates to `main().catch` and exits 2. That leaves `kake-corpus-contract-XXXXXX` behind in `os.tmpdir()`.
- The leftover directory has mode 0700 and contains fixtures only, so there is no data exposure.
- **Fix:** wrap everything from fixture build through the e1 case in `try { … } finally { /* region */ fs.rmSync(tmp, …) }`, keeping the marker pair around the `rmSync`.

### F5 — Low: `TMPDIR` controls where selftest writes
- `os.tmpdir()` honours `$TMPDIR`. With `TMPDIR=/home/vgpnk/Projects/shokunin/kake-shokunin`, selftest would create and then delete a mkdtemp subdirectory inside the live lane tree. It never touches existing files, because mkdtemp guarantees a new name. Still, this is a transient live-tree write that the Gate standard forbids ("no live-tree write").
- **Fix:** after `mkdtempSync`, check `path.relative(laneRoot, fs.realpathSync(tmp))`. If the temp path is inside the lane, remove it and exit 2 with `selftest-tmp-inside-lane`.

### F6 — Info: child environment and timeout
- Children inherit the parent's full `process.env` (381, no `env:` option), including `NODE_OPTIONS`. That gives no more privilege than the parent already has, and no secret is passed explicitly, so this is not a new boundary.
- `execFileSync` has no `timeout`. Children only read fixtures in tmpfs, so a hang is unlikely. Adding `timeout: 15000` would bound a pathological `TMPDIR`, for example a stalled FUSE mount.

### F7 — Info, gate integrity outside strict confinement: substring exclusion
- `EXCLUDE_RE = /verifier|aggregator|operator/i` (73) is a substring test on knowledge basenames. A future lane-authored entry such as `operator-handoff.md`, or any name containing "cooperator", would be excluded from C1.
- It is visible as `SKIP excluded-name`, so it is not silent, unlike F1. None of the 21 current `corpus/knowledge/*.md` basenames match. Lesson exclusion is already handled by the anchored `LANE_LESSON_RE` (74).
- A word-boundary or prefix rule would be stricter. The exclusion policy belongs to GateContract/CountingRecipes; it is flagged here only.

## What is confirmed safe (do not re-litigate)
- **No shell anywhere.** There is no `exec`/`execSync`/`spawn` and no `shell:` option. The single `execFileSync` uses `process.execPath` and an argv array (381).
- **Normal path is a pure read.** It has no env-dependent path resolution and no `~/projects` fallback (unlike freshness-sweep 181-193). The default root is `dirname(SELF)/..` (604).
- **Marker strings in the e1 controls are inert.** Lines 571 and 573 are string literals: the trimmed line starts with `'`, so they are not counted as regions. The probe line is split by concatenation (567).
- **Fixture writes are confined to the BEGIN/END regions.** The `put` alias (416) is defined and called only inside region 405-479 (call sites 418-477). The `mkdirSync` loop (410-413) is also inside that region.
- **Selftest cannot recurse,** and no child runs against the live lane root. c6's `--bogus` / `--root` / `--root=` exit 64 at `parseArgs` before `evaluate`.

## Integration checklist for Main (static; Main runs this once)
1. `node scripts/corpus-contract.mjs --selftest` → expect 7/7 PASS and exit 0. Afterwards, `ls ${TMPDIR:-/tmp} | grep kake-corpus-contract-` should list nothing.
2. `node scripts/corpus-contract.mjs --json` on the lane → record `counts.knowledgeChecked` (should be 21) and `counts.lessonsChecked` (should be 15) in the registry or verdict evidence, so that F1-type population drops become visible.
3. Before landing, decide whether to fix F1 and F2a/b in this round. Otherwise, record them as known residual limits next to the gate's registry row (write scope: "selftest temp dir only; proof does not cover child_process or region end-bound").

## File changes
- Wrote `.ufo/waves/round-21/w1/Confinement.md` (this report). No other file was touched.

## Tooling
No installs or updates.

## Limitations
- This is a static read only: no runs and no selftest execution.
- The Dirent symlink behaviour in F1 comes from documented Node `readdir({withFileTypes})` semantics (lstat-style `d_type`); I did not observe it by running anything here.
- The review is pinned to sha256 `ca6f685e…ed29`.
