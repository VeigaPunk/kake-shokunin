# ReviewAge — C2 semantic review

Axes: calibration (2 HOLD), freshness (10 HOLD). Neither score changed by this review. Lane-internal recommendation only; not outside admission.

## Findings, severity ordered

**Medium — frozen comparison does not enforce exact integer JSON outputs.** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/count.py:75-78` parses JSON and compares dictionaries using Python equality. `false == 0`, `true == 1`, and integer-valued floats also compare equal to integers. The contract requires all six exact integer outputs. Independent predicate demonstration replaced every output 0/1 by a boolean: all twelve valid expected-object comparisons still pass, with illegal booleans in ten outputs. Evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge/predicate_probe.py` and `predicate-results.json` in that same directory. This demonstrates the comparison weakness, not an end-to-end malicious candidate score; no frozen bytes changed. Recommendation: preserve this frozen result honestly and independently check exact output types; a future separately frozen counter should require `type(value) is int` for each required output. The reviewed candidate itself has no observed instance of this defect.

No candidate semantic defect found in the requested bounded domain. Candidate reviewed once: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge/cache_current_age.py`, SHA256 `d1b09ae17a54728a3b967cdc7436f19b62fc98e4304aab64324ee8969454331a`. Its new-file behavior is the six prescribed arithmetic expressions, required-key validation, bool/noninteger rejection, Age default0, nonnegative local times/Age, and ordered local times. The candidate was stable across the independent probe. No production edit or admission performed.

## Direct RFC comparison and hand checks

Reopened by explicit stdlib GET: https://www.rfc-editor.org/rfc/rfc9111.txt ; status200; body SHA256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`. Only §§4.2.3 and 1.2.2 body excerpts retained. Receipt: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge/rfc9111-get.json`. Located quotations in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge/rfc9111-quotes.txt`:

- Lines13–16: Age is its arithmetic field value “or 0, if not available.” Candidate correctly defaults only omitted age_value; explicit null, false, fractional or string values are invalid.
- Lines18–22: Date is the Date header value; missing-Date requirements refer to HTTP §6.6.1. This offline profile deliberately does not synthesize Date or implement those broader cache requirements. Missing and null Date reject; negative epoch Date is allowed. No claim that Date absence implies zero.
- Lines37–50: negative apparent age clamps to zero; corrected age includes response delay measured from request initiation. Both max branches and ties were checked.
- Lines52–57: “The corrected_age_value MAY be used as the corrected_initial_age”; conservative `max(apparent_age, corrected_age_value)` is allowed, not the sole RFC algorithm. Candidate description correctly makes this distinction.
- Lines63–64: resident time and current age match the contract. Integer seconds on a common epoch clock are an explicit profile restriction, not a claim that RFC clocks have only integer precision. Chronological local inputs reject rather than treating clock reversal as zero delay.
- Lines73–88: overflow replacement is conditional on representation/calculation overflow, not a universal cap at 2^31. Python arbitrary precision needs no such cap. The candidate disables Python decimal-string digit limits at CLI entry; an independent 5001-digit numeric input passed exact output assertions.

All twelve frozen numeric cases and five invalids independently hand-checked, including full six-value tuples, in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge/hand-check.md`. No frozen oracle error found.

Independent fresh-input probe: **60/60 passed**, seven valid and 53 invalid. These are not a replay of age-cases.json: valid omitted Age, future Date, both conservative branches, tie, negative Date at epoch, all-zero boundary, and 5001-digit arithmetic; invalid missing keys, all five fields with null/bool/float/string/list/object, negative local/Age values, both time inversions, malformed/nonobject JSON. Every valid output checked exact keys, values, integer types, exit0, and empty stderr; invalids checked exit1, empty stdout, nonempty stderr. Evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge/fresh_probe.py` and `fresh-results.json` in that directory.

## Residual risk and verification gaps

- The frozen finite counter alone does not test valid omitted Age, diagnostic presence, invalid stdout emptiness, or clean success stderr. Independent checks cover these; they are not claims that the frozen 17-case count enforces them.
- This is an arithmetic helper, not storage/reuse approval, Date parsing, freshness-lifetime evaluation, browser behavior, or general cache implementation. No network path is part of the candidate. No owned-property trial was performed by this seat; the RFC GET is source reopening, not a substitute for that trial.
- LSP unavailable: `read xd://lsp` returned “No such tool”. Therefore no semantic-server references/definition/diagnostics evidence exists. Direct candidate inspection and fresh CLI behavior are the evidence, not textual search presented as semantic proof.
- No canonical planner/runtime, rerouting, saturation scheduler, or resume paths changed by this candidate. Those broader invariants and resume_continuity_v1 are not exercised here; no invented assertions about their admission.
- Read-only reconnaissance showed the candidate absent at base/freeze and initial working production scripts. Initial shell reconnaissance used `ls` and `sed` despite tool-preference rules; this was read-only and is disclosed rather than represented as compliant specialized discovery. The initial RFC GET captured unsolicited response cookie metadata; retained receipt was immediately reduced to public Date/content-type/cache-control/ETag headers and rerun with an allowlist, no cookie reuse or credential/session access. No full RFC mirror retained.

## Commands and observed exits

All executed Python commands used the same installed interpreter, stdlib only. No tool installation, build, lint, broad test suite, services, provider probes, git/jj mutations, commits, production writes, or delegation.

- `mkdir -p /fast/scratch/hyaku/kake-r87/ReviewAge /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge` — exit0.
- `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge/reopen_rfc.py` — exit0 twice; second invocation produced the retained allowlisted HTTP200 receipt. The retained script reflects that final invocation.
- `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge/fresh_probe.py` — exit0, 60 fresh CLI checks passed; subprocess command recorded in fresh-results.json, each exit retained there.
- `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge/predicate_probe.py` — exit0; all12 comparisons accepted, ten with illegal booleans.
- `rmdir /fast/scratch/hyaku/kake-r87/ReviewAge` — exit0. Scratch removed after receipts retained; zero clones created.

Earlier shell reconnaissance (combined commands each overall exit0; no claims about individual command exit codes):

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin && git rev-parse --show-toplevel && git log --oneline -5 && git status --porcelain | sed -n '1,30p' && git rev-parse 86ca7803fd964db7ae2a628c7e9048741c78a45f 58fee726102aa89ad2c1fa9f697869de3a212510 2>&1
cd /home/vgpnk/Projects/shokunin/kake-shokunin && echo '--- freeze tree scripts/:' && git ls-tree 58fee726102aa89ad2c1fa9f697869de3a212510 --name-only scripts/ 2>&1; echo '--- worktree scripts/:' && ls scripts/ 2>&1; echo '--- wave w1 dir:' && ls -la .ufo/waves/round-87/w1/ 2>&1; echo '--- wc age-cases:' && wc -l .ufo/waves/round-87/age-cases.json
```

Retained scripts/receipts are evidence, not production scaffolds. No frozen predicate or expected file modified after checks.

Self-evaluation (not admission): accuracy4 (direct RFC and executable receipts; no LSP), completeness4 (bounded seat complete, owned-property trial belongs elsewhere), clarity4 (specific finding separate from candidate), actionability4 (exact predicate location and independent mitigation), conciseness4 (command disclosure adds length). Mean4.0. Improvement: future counter should enforce exact types without rewriting this frozen wave. User-agreement check: recommendations remain lane-internal and limitations explicit.
