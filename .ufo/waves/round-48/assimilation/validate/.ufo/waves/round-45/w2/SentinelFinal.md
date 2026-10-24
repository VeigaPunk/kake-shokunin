# SentinelFinal — frozen-set integrity
**Axes:** operability and freshness.

## Attack and verdict

**Target:** Rebuild the SHA-256 inventory for the named round-44 frozen scripts/data, all files under `classes/`, `classes-placebo/`, and `controls-r43/`, all files under round-43 and round-44 `verification/`, plus `scripts/sitemap_audit.py` and `scripts/ledger_latest_check.py`; compare it to `.ufo/waves/round-45/verification/sha-guard/before.sha256`.

**Verdict: PASS, modulo the required cache exclusion.** The rebuilt scoped inventory matches the baseline exactly after excluding `__pycache__` paths. The filtered baseline check verified 447 entries with zero failures. No included frozen-byte drift was found.

**Severity: INFO (cache-only mismatch in the unfiltered guard).** The raw guard check had one mismatch: `.ufo/waves/round-44/classes/__pycache__/g3_empty_path.cpython-314.pyc`. `__pycache__` entries were excluded throughout, as instructed, because these are generated caches remediated this round and are not stable committed-source bytes. No other failure appeared in the raw check.

**Exploit path:** None demonstrated for the included byte set. An unfiltered check can report the generated-cache mismatch as a false integrity failure; applying the specified exclusion removes it.

**Impact:** No changed source, control, or verification bytes were detected in the scoped inventory. The cache-only mismatch can confuse or block a raw, unfiltered verification but does not falsify the scoped frozen-set guard.

**Smallest remediation:** No source remediation indicated. Keep `__pycache__` excluded consistently when rebuilding/checking this frozen-byte set; do not treat generated cache drift as committed-byte drift.

## Commands and decisive output

Working directory for all commands: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

Raw guard check:

```sh
sha256sum -c .ufo/waves/round-45/verification/sha-guard/before.sha256
```

Decisive output (verbatim):

```text
.ufo/waves/round-44/classes/__pycache__/g3_empty_path.cpython-314.pyc: FAILED
sha256sum: WARNING: 1 computed checksum(s) did NOT match
```

Filtered check, omitting every manifest entry whose path contains the `__pycache__` directory component:

```sh
set -o pipefail; sha256sum -c <(awk '$2 !~ /(^|\/)__pycache__(\/|$)/' .ufo/waves/round-45/verification/sha-guard/before.sha256) 2>&1 | awk '/: OK$/ {ok++} /: FAILED/ {bad++; print} /No such file|WARNING/ {print; bad++} END {printf "checked=%d failed=%d\n", ok+bad, bad; exit (bad > 0)}'
```

Output (verbatim):

```text
checked=447 failed=0
```

Freshly rebuilt the target inventory (the explicit files plus every regular file under the named directories, excluding `__pycache__`) and compared sorted SHA-256/path rows against the filtered baseline:

```sh
set -o pipefail; LC_ALL=C; if diff -u <({ printf '%s\0' 'scripts/ledger_latest_check.py' 'scripts/sitemap_audit.py' '.ufo/waves/round-44/c44_audit.py' '.ufo/waves/round-44/c44_count_v5.py' '.ufo/waves/round-44/c44_placebo.py' '.ufo/waves/round-44/controls-27.tsv' '.ufo/waves/round-44/controls-canary.tsv'; find '.ufo/waves/round-44/classes' '.ufo/waves/round-44/classes-placebo' '.ufo/waves/round-44/controls-r43' '.ufo/waves/round-43/verification' '.ufo/waves/round-44/verification' -type f ! -path '*/__pycache__/*' -print0; } | sort -z | xargs -0 sha256sum | sort -k2) <(awk '$2 !~ /(^|\/)__pycache__(\/|$)/' '.ufo/waves/round-45/verification/sha-guard/before.sha256' | sort -k2); then printf 'PASS: rebuilt scoped inventory matches before.sha256 after __pycache__ exclusion\n'; else printf 'FAIL: rebuilt scoped inventory differs from before.sha256\n'; fi
```

Output (verbatim):

```text
PASS: rebuilt scoped inventory matches before.sha256 after __pycache__ exclusion
```

## Files written

- `.ufo/waves/round-45/w2/SentinelFinal.md` (this report)

Created `/fast/scratch/hyaku/kake-r45/SentinelFinal/`; no files were written there. No tools were installed or updated.