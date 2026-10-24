# GitNameRegression — Git path-name regression test for the citing-set gate

Seat: `KakeR27.BuildGate` (operability). Scope granted by L1 `KakeR27`: one new file, same worktree/branch, no model restart, no new wave.

## Source (exact path + hash)

- Path: `/fast/scratch/hyaku/kake-r27/writer-gate/.ufo/waves/round-27/git_name_selftest.py`
- sha256: `244de25530158c97940a9976a1a2dd7e6999355baafdd7f9870cfead1463c768`
- 377 lines, mode 755, new file, untracked in worktree `kake-r27-gate` (base `be375d90afc6fc7aca369ab3cf5247bf460aeed2`).
- Nothing else was written in this scope. The gate `scripts/citing_set.py` was **not** touched (worktree copy sha256 `5b7b1f03de7263aa0094017753061a2c785f50c24de2e2de1b8714ff66f7bf1b`); the L1's fixed live gate is `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py`, sha256 `790d732799510c69cd870ae89a331a2178ce84d6d98cbda13cb50a0aa5f05b92` (`ls-tree -rz`, NUL framing, `os.fsdecode`).

## What the test covers (behavioural, not value capture)

`--revision` mode enumerates `corpus/knowledge` from `git ls-tree`. The historical text framing (newline records, TAB split) cannot represent a path containing a TAB or a NEWLINE and mangles non-ASCII paths under `core.quotePath`. The test drives the **real gate binary** through a subprocess and asserts stable finding ids, exit codes and `(row, file)` identities for knowledge files named:

1. `alpha.md` (plain)
2. `with space.md` (space)
3. `with<TAB>tab.md` (tab)
4. `with<LF>newline.md` (newline)
5. `naïve-Ω.md` (non-ASCII)

## Fixture construction (isolated)

- Temporary tree under `/fast/scratch/hyaku/kake-r27/` (`tempfile.mkdtemp(prefix="git-name-selftest-")`), repository at `<tmp>/repo`; removed afterwards unless a case failed or `--keep`.
- Isolated Git: `HOME=<tmp>`, `XDG_CONFIG_HOME=<tmp>/xdg`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=<tmp>/absent-gitconfig`, `GIT_ATTR_NOSYSTEM=1`, `core.hooksPath=<tmp>/hooks` (empty), `commit.gpgsign=false`, `core.quotePath=true` (kept **on** so the historical quoting bug would actually bite), fixed author/committer identity and dates, `GIT_TERMINAL_PROMPT=0`. `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_OBJECT_DIRECTORY` are removed from the environment. No remote is configured and no network command is issued; the live repository is never written.
- Population is fixed: `{"rows": [{"id": "S001"}]}`. Every knowledge file cites `S001` only.
- Phase 1: `ledger.json` = `{"pairs": []}` (committed). Phase 2: `ledger.json` = the exact five pairs `{"row": "S001", "file": "corpus/knowledge/<name>"}` (committed as a second commit).

## Expected outcomes (derived from the fixture, never captured from gate output)

| Mode | Ledger | Exit | Verdict | Findings |
|---|---|---|---|---|
| working tree (`--root`, no `--revision`) | empty | 1 | `failed` | exactly 5 × `unadjudicated_citing_pair`, `(S001, corpus/knowledge/<name>)` for the five names; `citingPairs` 5, `ledgerPairs` 0 |
| `--revision <commit>` | empty | 1 | `failed` | identical five identities; `citingPairs` 5, `ledgerPairs` 0 |
| working tree | exact | 0 | `clean` | `findings` empty; `citingPairs` 5, `ledgerPairs` 5 |
| `--revision <commit>` | exact | 0 | `clean` | `findings` empty; `citingPairs` 5, `ledgerPairs` 5 |

Assertions per run: JSON parses and carries `verdict`/`citingPairs`/`ledgerPairs`/`findings`; exit code is exactly 1 (red) / 0 (green); the finding-id set is exactly `{unadjudicated_citing_pair}`; the finding count is exactly 5; the identity set equals the five expected `(row, file)` pairs; the two modes agree on the identity set (`modes-agree-empty-ledger`).

## Command (NOT RUN — L1 barrier)

```
python3 -B /fast/scratch/hyaku/kake-r27/writer-gate/.ufo/waves/round-27/git_name_selftest.py \
  --gate /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py \
  --tmpdir /fast/scratch/hyaku/kake-r27
```

Exit codes of the test: 0 all cases passed, 1 a case failed, 2 could-not-evaluate (gate absent, tmpdir unusable, repository setup failed), 64 usage. stdout is one JSON summary (`schema: kake-citing-set-git-name-selftest-v1`, keys `verdict`/`passed`/`cases`/`failed`/`gate`/`gateSha256`/`expectedIdentities`/`results`), ASCII-safe; a failing run keeps the temporary repository and prints its path on stderr.

## Status / limits

- **Not executed.** Per the L1 instruction no test, smoke run or formatter was run; this file has never been executed, so its own correctness is unmeasured. Expected values come from the constructed fixture, not from gate output.
- Default `--gate` is `scripts/citing_set.py` resolved from this file's own location (`<repo>/scripts/citing_set.py`); pass `--gate` explicitly to test the L1's fixed gate (the worktree copy still holds the pre-fix `ls-tree` text framing, which this test is expected to fail against — that is the regression signal).
- No r24 material, no raw HTML, no auth/credential state, no browser or publication surface is involved.
