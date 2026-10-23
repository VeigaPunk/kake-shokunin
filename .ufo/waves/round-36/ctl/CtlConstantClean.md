# CtlConstantClean — constant-clean negative control

## Axes and skipped work

- **Freshness:** source-drift detection and the counter's sensitivity to omitted work.
- **Operability:** deterministic JSON and the documented CLI exit codes.

Control: `/fast/scratch/hyaku/kake-r36/controls/CtlConstantClean/source_recheck.py`.
Public-contract evidence: read-only `timeout 20s git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 3555f63f:SCORECARD.md`, section `## Round 36 — declared claims`.

For `--manifest PATH`, the control never opens or parses the manifest and never reads, searches, or stats any body. It skips all seven substantive contract bullets: status, redirects, HTML text extraction, quote normalization/matching, media types, decoding, and input validation. It always prints exactly:

```json
{"version":1,"verdict":"clean","checksEvaluated":0,"findings":[]}
```

It exits 0. Missing/extra CLI arguments or a flag other than `--manifest` produce usage on stderr and exit 64 instead.

## How it tries to score; choice of constant

The frozen comparison ignores `checksEvaluated`, so zero there costs nothing. An empty findings list is independent of the freshly randomized check ids and body names. A fixed nonempty per-check finding cannot anticipate those ids; a fixed `input_invalid` finding with null check could only hit manifest-level faults. Clean/exit 0 is therefore my best **[INFERENCE]** for the broadest useful fixed report, not a demonstrated optimum. Public historical evidence supports trying this shape: the preceding round's constant-clean control scored 7 of 24, although that is a different contract and does not establish any round-36 score.

This control only wins cases whose expected findings are empty and verdict is clean. Its expected weakness is every case requiring an identified finding, a moved target, or an input-error verdict. No sealed score is known; the frozen counter was not read or run.

## Self-test actually run

Ran four hand-made manifest inputs, piped as JSON to stdin, with the child command:

```text
timeout 5s python3 -B /fast/scratch/hyaku/kake-r36/controls/CtlConstantClean/source_recheck.py --manifest /dev/stdin
```

A `timeout 30s python3 -B -c ...` harness used `subprocess.run(..., input=json.dumps(manifest), capture_output=True, text=True, timeout=8)` and asserted identical JSON, exit 0, and empty stderr for all four. No manifest or body files were created. These were the inputs:

```json
{"version":1,"checks":[]}
{"version":1,"checks":[{"id":"gone-handmade","url":"https://example.invalid/docs/source","quote":"evidence","hops":[{"status":404,"location":""}]}]}
{"version":1,"checks":[{"id":"move-handmade","url":"https://example.invalid/docs/source","quote":"evidence","hops":[{"status":301,"location":"../moved"},{"status":410,"location":""}]}]}
{"version":1,"checks":"not-a-list"}
```

Observed versus manually derived public-contract expectations:

| Input | Observed | Contract expectation |
|---|---|---|
| Empty checks | clean, exit 0, no findings | Same |
| Final 404 | clean, exit 0, no findings | failed-policy, exit 1; `gone` for `gone-handmade` |
| 301 then 410 | clean, exit 0, no findings | failed-policy, exit 1; `moved` for `move-handmade`, target `https://example.invalid/moved`, plus `gone` |
| Non-list checks | clean, exit 0, no findings | could-not-evaluate, exit 2; `input_invalid`, check null |

Each observed report was the exact fixed JSON above. An additional no-argument invocation returned exit 64, empty stdout, and stderr `usage: source_recheck.py --manifest PATH\n`.

Harness final output:

```text
self-test: four identical clean reports; four manual contract expectations: one agreement, three deliberate mismatches; usage exit 64; all child processes reaped
```

These are negative-control smoke observations, not a sealed-case measurement or a judgment of the lane tool.

## Counterexample and smallest safe correction

The final-404 manifest is the cheapest concrete counterexample: this tool claims clean even though bullet (a) requires `gone` and exit 1. The permanent-redirect example additionally shows suppressed URL provenance (`moved` target); the invalid manifest shows suppressed inability to evaluate. Those three observed false greens impact freshness correctness; the stable CLI alone does not establish audit operability.

If this constant nonetheless meets `passed >= 25 of 28`, the counter has a fixable discrimination defect, not evidence that skipped auditing is an acceptable tradeoff. The smallest safe correction is to repair expected findings/comparison, or replace mistakenly clean fixtures, so at least four of the 28 cases genuinely require nonempty findings. Re-freeze before any build; keep the declared threshold. This report makes no admission or rejection judgment and invokes no judging runtime.

## Key-blindness tree listing

Executed only the authorized own-directory listing:

```text
$ timeout 10s ls -la /fast/scratch/hyaku/kake-r36/controls/CtlConstantClean/
total 4
drwxr-xr-x 2 vgpnk vgpnk  31 Oct 22 22:23 .
drwxr-xr-x 4 vgpnk vgpnk  49 Oct 22 22:23 ..
-rwxr-xr-x 1 vgpnk vgpnk 461 Oct 22 22:23 source_recheck.py
```

## Compliance

Complied with key blindness: no listing, reading, searching, or statting anywhere under `/fast/scratch/hyaku/kake-r36/` except this own `controls/CtlConstantClean/` directory; no access to lane `.ufo/waves/round-36/verification/`; no search for sealed cases; no counter execution. The `..` entry above is from the required own-directory `ls -la`, not a parent-directory listing.

Exactly two persistent files were written: this report and the control. No git/jj writes, sandbox git operations, network, integration, or shipping occurred. Every explicitly started process had an external `timeout` cap of at most 30 seconds (tool-call deadlines at most 35 seconds); all completed, and the self-test reaped all children. No process tree remains from this assignment.

Read `/home/vgpnk/.omp/agent/RULES.md` first. No tools were installed or updated; existing Python stdlib and host utilities sufficed. No pacman transaction was attempted.
