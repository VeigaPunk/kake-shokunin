# ReviewerC3Repin — C3 re-pin review

Recommendation: source repair is narrowly compliant; receipt coverage is insufficient to confirm the requested §paths drift count or declaredAbsent-set preservation. This is a review recommendation, not admission or settlement.

Axes attacked: exact change boundary; unchanged gate strength; receipt fidelity and path-set continuity.

## Findings by severity

### Medium — committed after receipt omits the entire §paths result

Absolute evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/sweep-after.txt:1-6`, read also directly from receipt commit `cc8add1fa740b920ea5179a71152680ab220c70c` with:

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/sweep-after.txt
```

Exact output:

```
$ node scripts/freshness-sweep.mjs --offline (measured tree T0, contract §C3)
§armed
  all remote checks skipped(offline) — NOT counted as pass (complete=false)
skipped(offline): §armed (all remote checks) · §history (probe-history source absent — pin-declared) — complete=false, never counted as pass
VERDICT: OK (exit 0, partial: offline)
exit=0
```

There is no §paths section, no drift count and no declaredAbsent list. The before receipt (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/sweep-before.txt:1-10`, also checked at the same receipt commit) is solely an exception trace ending `sweep-before-exit=2`, beginning `freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:364`. It supplies no before declaredAbsent set either. Thus the requested same-set comparison cannot be made from these receipts.

Canonical unchanged code provides an additional fidelity check: `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs:1094-1096` executes selected sections; `:1119-1125` prints the header and each executed section; `:946-956` prints §paths counts and declaredAbsent rows. The receipt is not a complete default-command transcript. Moreover `:1060-1061` gates paths only when present, so the final OK line by itself does not establish paths execution. This is an evidence gap, not proof that the measured run skipped paths or that C3 is false. Preserve complete stdout/JSON and the actual invocation/environment to resolve it; do not equate this abridged receipt with drift-zero evidence.

## Confirmed source boundaries

Exact command exercised (exit 0):

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- corpus/knowledge/freshness-sidecar.json scripts/freshness-sweep.mjs corpus/knowledge/freshness-pins.json
```

Only seven one-line substitutions appear, all in the sidecar's `line` fields:

| Entry index (zero-based) | Old → new SKILL.md line | Sidecar line at T0/current |
|---|---|---|
| 6 | 364 → 365 | 60 |
| 7 | 445 → 446 | 69 |
| 8 | 448 → 449 | 78 |
| 9 | 449 → 450 | 87 |
| 10 | 450 → 451 | 96 |
| 21 | 423 → 424 | 195 |
| 22 | 431 → 432 | 204 |

Absolute sidecar path: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/freshness-sidecar.json`. All seven `lineSha256` values are unchanged, not replaced. These are seven re-pinned line/hash entry pairs, not fourteen changed cells. All other cells, including notes, kind, date and token, are unchanged. The old→new map at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/sidecar-repin-map.txt:3-9` agrees.

Revision-data analysis used Python Eval with `subprocess.check_output(['git','-C',repo,'show',revision+':'+path])`, JSON-decoded both sidecars, compared every key of every paired entry plus outer keys, and SHA256-hashed `git show T0:<entry.file>` split on newline at `entry.line - 1`. Observed output:

```
entries 30 30
entry 6 {'line': (364, 365)} sha unchanged True
entry 7 {'line': (445, 446)} sha unchanged True
entry 8 {'line': (448, 449)} sha unchanged True
entry 9 {'line': (449, 450)} sha unchanged True
entry 10 {'line': (450, 451)} sha unchanged True
entry 21 {'line': (423, 424)} sha unchanged True
entry 22 {'line': (431, 432)} sha unchanged True
changed entries 7 unchanged entries 23
outer cells equal True
T0 invalid line digests []
```

Therefore all 30 line digests bind to measured T0 bytes, including the 23 untouched entries. This is a digest check, not a substitute for the sweep's token, annotation or live-filesystem checks (`scripts/freshness-sweep.mjs:357-390`).

Weakening attack: exact command exercised, no output, exit 0:

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --exit-code 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- scripts/freshness-sweep.mjs corpus/knowledge/freshness-pins.json corpus/SOURCES.md
```

Independent byte comparisons of revision blobs were all True; T0 SHA256s:

```
scripts/freshness-sweep.mjs 972eb9d6f6487299ea18264a94f95f355f218b49d7d7bccd42eabea5f464377c
corpus/knowledge/freshness-pins.json abf5248ae6356c81a955745bf56241e27ddc14f0658cf5447ffee2d65918cf14
corpus/SOURCES.md 63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2
```

No weakening of the sweep script, pins file or SOURCES occurred in the requested base→T0 diff.

## Residual risk and verification gaps

- Runtime path drift and declaredAbsent-set continuity remain unverified; offline OK is explicitly partial, not remote-check success. No sweep or alternate runtime was invoked in this review.
- LSP prerequisite attempted: `read xd://lsp` returned `No such tool: xd://lsp`. Semantic references/definition/diagnostics were unavailable; text search and direct source inspection were literal fallbacks, not semantic proof.
- No installations, lane edits other than this report, mutating git commands, fixture repositories or commits. Seat scratch `/fast/scratch/hyaku/kake-r64/ReviewerC3Repin` was created and removed via `mkdir -p … && rmdir …` (exit 0); no retained scratch.
- Self-evaluation: accuracy 4 (runtime result intentionally not inferred), completeness 4 (requested receipt comparison is impossible from supplied evidence), clarity 4 (source and receipt conclusions separated), actionability 4 (full section output needed), conciseness 4 (explicit evidence adds length); overall 4.0. Improvement: retain full before/after section evidence. User-agreement check: conclusions stay within observed data and distinguish verified repair from missing runtime evidence.
