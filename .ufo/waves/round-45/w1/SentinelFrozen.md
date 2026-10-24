# SentinelFrozen — round 45 wave 1

## Axes
Operability; freshness.

## Named attack: frozen-path drift between baseline and end guard
**FAIL — kill-rule-1 failure.** The initial SHA-256 manifest covered 483 entries. The end-of-seat regeneration covered 484 entries and `diff -u` found two changed directory entries under the explicitly frozen `.ufo/waves/round-44/classes/` tree. The only observed differences were Python bytecode cache files; no source file or the two guarded scripts differed. I cannot attribute the cache changes to a particular process or seat.

### Finding 1 — High (per the assignment's kill rule): frozen byte drift
- **Exploit path:** an interpreter invocation that imports/compiles modules in `round-44/classes` without suppressing bytecode writes can create/update `__pycache__` files. This is a plausible mechanism for the observed changes, not an attribution of the process that caused them.
- **Evidence:** baseline had `g3_empty_path.cpython-314.pyc` at `25ba8580…f998051` and no `g9_port_digits.cpython-314.pyc`. The end manifest had `g3_empty_path.cpython-314.pyc` at `ff0cbbc8…3cce197` and added `g9_port_digits.cpython-314.pyc` at `bb3b9b59…7ebe703`. The full decisive diff is below.
- **Impact:** the requested byte-level freeze check fails even though the observed drift is confined to generated cache entries; do not report the frozen tree as unchanged.
- **Smallest remediation:** preserve the original `before.sha256` and stop executions from writing bytecode into frozen paths (e.g. use `python -B` / `PYTHONDONTWRITEBYTECODE=1`). Do not replace the baseline to bless this drift; obtain the L1's disposition before any new baseline.

### Additional local finding — Low: unbounded sitemap manifest read
- **Exploit path:** a reviewer runs the offline sitemap auditor against an untrusted manifest path containing a very large JSON document.
- **Evidence:** `scripts/sitemap_audit.py:523-532` calls `handle.read()` without a byte limit before decoding and `json.loads`; by contrast the named sitemap file itself is bounded to `MAX_BYTES + 1` at lines 405-413.
- **Impact:** excessive memory/CPU use may prevent the local audit from producing its result. This is a static finding; I did not construct or run a payload.
- **Smallest remediation:** cap manifest bytes at read time and reject an oversized manifest as `input_invalid`.

## Coverage and commands
The baseline included 476 files under the five recursive directories plus seven explicitly named files (the five round-44 top-level files and both scripts). No symlinks were found. The two script hashes in the baseline were:

```text
50384505b981352b691f24fbdd66c521c18b80408aeed4bbb54c70f8903f63dd  scripts/ledger_latest_check.py
914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021  scripts/sitemap_audit.py
```

Baseline generation command:

```sh
set -euo pipefail
cd /home/vgpnk/Projects/shokunin/kake-shokunin
for p in .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_placebo.py .ufo/waves/round-44/controls-27.tsv .ufo/waves/round-44/controls-canary.tsv scripts/ledger_latest_check.py scripts/sitemap_audit.py .ufo/waves/round-44/classes .ufo/waves/round-44/classes-placebo .ufo/waves/round-44/controls-r43 .ufo/waves/round-43/verification .ufo/waves/round-44/verification; do test -e "$p" || { printf 'MISSING: %s\n' "$p" >&2; exit 2; }; done
mkdir -p .ufo/waves/round-45/verification/sha-guard
{ printf '%s\0' .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_placebo.py .ufo/waves/round-44/controls-27.tsv .ufo/waves/round-44/controls-canary.tsv scripts/ledger_latest_check.py scripts/sitemap_audit.py; find .ufo/waves/round-44/classes .ufo/waves/round-44/classes-placebo .ufo/waves/round-44/controls-r43 .ufo/waves/round-43/verification .ufo/waves/round-44/verification \( -type f -o -type l \) -print0; } | sort -zu | xargs -0 sha256sum > .ufo/waves/round-45/verification/sha-guard/before.sha256
printf 'guarded files: '; wc -l < .ufo/waves/round-45/verification/sha-guard/before.sha256
for d in .ufo/waves/round-44/classes .ufo/waves/round-44/classes-placebo .ufo/waves/round-44/controls-r43 .ufo/waves/round-43/verification .ufo/waves/round-44/verification; do printf '%s: ' "$d"; find "$d" \( -type f -o -type l \) -print0 | tr -cd '\0' | wc -c; done
printf 'symlinks: '; find .ufo/waves/round-44/classes .ufo/waves/round-44/classes-placebo .ufo/waves/round-44/controls-r43 .ufo/waves/round-43/verification .ufo/waves/round-44/verification \( -type l \) -print | wc -l
sha256sum .ufo/waves/round-45/verification/sha-guard/before.sha256
```

Verbatim baseline output:

```text
guarded files: 483
.ufo/waves/round-44/classes: 19
.ufo/waves/round-44/classes-placebo: 10
.ufo/waves/round-44/controls-r43: 54
.ufo/waves/round-43/verification: 68
.ufo/waves/round-44/verification: 325
symlinks: 0
30d33f643530aaee1400a86f61b07d4b3456fc8a137d3e7e28375ece7b8f457d  .ufo/waves/round-45/verification/sha-guard/before.sha256
```

End guard command:

```sh
set -euo pipefail
cd /home/vgpnk/Projects/shokunin/kake-shokunin
{ printf '%s\0' .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_placebo.py .ufo/waves/round-44/controls-27.tsv .ufo/waves/round-44/controls-canary.tsv scripts/ledger_latest_check.py scripts/sitemap_audit.py; find .ufo/waves/round-44/classes .ufo/waves/round-44/classes-placebo .ufo/waves/round-44/controls-r43 .ufo/waves/round-43/verification .ufo/waves/round-44/verification \( -type f -o -type l \) -print0; } | sort -zu | xargs -0 sha256sum > /fast/scratch/hyaku/kake-r45/SentinelFrozen/after.sha256
printf 'after guarded files: '; wc -l < /fast/scratch/hyaku/kake-r45/SentinelFrozen/after.sha256
if diff -u .ufo/waves/round-45/verification/sha-guard/before.sha256 /fast/scratch/hyaku/kake-r45/SentinelFrozen/after.sha256; then printf 'guard diff: identical (exit 0)\n'; else rc=$?; printf 'guard diff: changed (exit %s)\n' "$rc"; exit "$rc"; fi
sha256sum /fast/scratch/hyaku/kake-r45/SentinelFrozen/after.sha256
```

Verbatim decisive end output (the command exited 1):

```text
after guarded files: 484
-25ba85808f19b6abb95ec8cc0f3631126b22a28b2f049a1844e8de87af998051  .ufo/waves/round-44/classes/__pycache__/g3_empty_path.cpython-314.pyc
+ff0cbbc8d23d7272c30ce3bd74985a1f433c7962f1b65e2a8772ad17d3cce197  .ufo/waves/round-44/classes/__pycache__/g3_empty_path.cpython-314.pyc
+bb3b9b590308a482077cc6b547054b0fd0e2ea07d8ba62a7b412e8fa87ebe703  .ufo/waves/round-44/classes/__pycache__/g9_port_digits.cpython-314.pyc
guard diff: changed (exit 1)
```

## Other evidence / boundaries
Read-only inspection found `ledger_latest_check.py:71-88` passes Git arguments as an argv list (no shell) and rejects absolute/parent-traversal committed paths; `sitemap_audit.py:555-584` rejects absolute and `..` manifest paths and joins relative names against the manifest directory. Both script files were included in the baseline; no command/selftest was run. No edits were made to the frozen tree or either script.

## Files written and checks
- `.ufo/waves/round-45/verification/sha-guard/before.sha256`
- `.ufo/waves/round-45/w1/SentinelFrozen.md`
- `/fast/scratch/hyaku/kake-r45/SentinelFrozen/after.sha256`

Unrun: script execution/selftests. No tool installs; no blocker.
