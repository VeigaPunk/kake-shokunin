# ExecSweepSections — round 64 §paths sweep

## Evidence

Ran the requested offline command against a pristine archive of measured T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`, extracted under the assigned scratch directory:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive 4c8295fa5e3b628f1fdf3840299ae415c01849fb | tar -x -C /fast/scratch/hyaku/kake-r64/ExecSweepSections
cd /fast/scratch/hyaku/kake-r64/ExecSweepSections
node scripts/freshness-sweep.mjs --offline
```

Observed output (2026-10-30T11:08:47Z; Node v24.21.0):

```text
§paths  172 files · 679 occurrences · 106 unique tokens
  resolve 31 · declaredAbsent 65 · drift 0 · unresolved 10
  citation base: 106 targets · missSet 65 · files 172
§history  SUSPENDED — probe-history source absent by declaration (pins.probeHistoryAbsent): /home/vgpnk/Projects/webzites/state/probe-history.jsonl — section suspended until a history source is re-anchored
§armed
  all remote checks skipped(offline) — NOT counted as pass (complete=false)
skipped(offline): §armed (all remote checks) · §history (probe-history source absent — pin-declared) — complete=false, never counted as pass
VERDICT: OK (exit 0, partial: offline)
```

The unresolved list was exactly these ten, all labeled placeholder/glob and explicitly `not existsSync-checkable`:

```text
~/ [placeholder]
~/.config/systemd/user/webzites-*.timer [glob]
~/.grok/agents/grokbot- [placeholder]
~/Projects/**/ufofsdbeta-kimi-review [glob]
~/Projects/webzites/reports/dead-slot- [placeholder]
~/Projects/webzites/reports/keepers/grokbot-*.log.md [glob]
~/Projects/webzites/state/rebuild-*.json [glob]
~/Projects/webzites/state/recreate-*.json [glob]
~/Projects/webzites/state/recreate-plazir15-*.json [glob]
~/Projects/webzites/state/update-*.json [glob]
```

## Verdict and discrepancy

The measured sweep returned `VERDICT: OK` / exit 0; the requested resolve, declaredAbsent, drift, unresolved, missSet, history pin-declaration, and offline-armed properties are present. However, the required file count was **171**; the actual output is **172** in both the `§paths` summary and citation-base line. Thus the entire specified numerical check does not match exactly.

The pre-repair receipt at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/sweep-before.txt:1-10` records only `paths sidecar binding invalid: SKILL.md:364` and exit 2; it contains no declaredAbsent token-set expectation. It cannot substantiate a token-by-token comparison or prove that this was the only differing condition. The after receipt `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/sweep-after.txt:1-6` records offline armed skipping, `complete=false`, and OK exit 0, but does not include the path counts/token set. Contract `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md:96-120` describes the sole seven-entry sidecar re-pin and the prior SKILL.md:364 error; it does not give a baseline declaredAbsent token set.

No source, claim, counter, receipt, or contract was changed. Scratch archive was removed. No tools were installed; no tests/builds/linters were run.
