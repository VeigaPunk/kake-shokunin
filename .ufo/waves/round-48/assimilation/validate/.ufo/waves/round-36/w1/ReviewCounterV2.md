# ReviewCounterV2 — sealed counter v3 review (round 36, wave 1)

I never touched anything under `/fast/scratch/hyaku/kake-r36/` and never ran `sealed_count.py` as a program (no key). I imported the module in-process and unit-tested `project`/`judge`/`materialize` on synthetic cases. No tools installed. Lane untouched except this report. Sandbox `/fast/scratch/hyaku/kake-r36w1/ReviewCounterV2/` (empty after cleanup; temp fixtures in `/tmp` deleted).

## Commands and exit codes
- `grep -n -E "def project|..." .ufo/waves/round-36/sealed_count.py` → 0 (line numbers below from this).
- `eval` python unit run importing `sealed_count.py` via `importlib` (21 assertions) → 0; all declared behaviors PASS; 2 intended crash repros reproduced; duplicate-id case FAILed as predicted.
- `python3 -c "from pathlib import Path; Path('/nonexistent/r36-review-probe').read_bytes()"` → traceback, `exit=1` (uncaught-exception exit semantics for D3).
- `mkdir -p` report dir; `rm -rf /tmp/r36w1-review-*` → 0.

## Defects

**D1 (medium, robustness/DoS — cannot inflate a pass count, can destroy the run): a finding with an unhashable `check` crashes the whole counter.**
`project()` line 110 does `idmap.get(check, check)`; a JSON `check` of `[]` or `{}` raises `TypeError` (dict lookup with list key). `judge()` line 157 and `main()` have no guard, so the exception kills `main` → traceback, exit 1, no JSON receipt. Exit 1 is contractually "not met", so a run that crashes is indistinguishable from a scored 0-of-28 for anything keying on the exit code, and `perCase` is lost for all remaining cases.
Repro (imported module, observed): `sc.project([{"check": ["unhashable"], "reason": "hold"}], {})` → `TypeError: cannot use 'list' as a dict key`; `sc.judge(case, proc_with_findings=[{"check":[]},{"check":[]}], idmap)` → same uncaught `TypeError`.
Pass count impact: none for an honest tool (our tool emits string ids); a malicious/buggy control can convert "clean fail" into "crash".

**D2 (medium, latent — changes a pass count only if the sealed key contains duplicate check ids within one case): duplicate ids are split and the map keeps only the last.**
`materialize()` lines 130–133: for each dict check it draws a fresh id and overwrites `idmap[c["id"]]`. Two checks with id `"D"` get two different fresh ids while `idmap` has one entry; the inverse map (judge line 158) sends only the second fresh id back to `"D"`. An honest tool reporting both fresh ids deterministically fails the case.
Repro (imported module, observed): case with checks `[{"id":"D",...},{"id":"D",...}]` → fresh ids `['cbf8729d9bff6','c814fa38c14bb']`, `idmap` size 1; judge of a correct tool output vs expected findings `[{"check":"D"},{"check":"D"}]` → False.
Pass count impact: only if a key case reuses an id. The L1's reference scored 28/28 through this exact counter, so duplicates are probably absent; flagging the latent hazard and its shape, not a live count change.

**D3 (low, error-exit contract): `--tool-file` failures exit 1 (reads as "not met") instead of exit 2 "cannot evaluate".**
`main()` line 200 `tool = Path(args.tool_file).read_bytes()` has no try; a missing or unreadable path (or a directory) raises before any JSON is printed, and Python exits 1. The docstring (line 43–44) promises exit 2 only for the three listed causes; a harness keying on exit codes would record a cannot-evaluate run as a predicate failure. Same class: `load_key` line ~101 `json.loads(data)` and `key["cases"]` at line 214 would raise (unreachable in practice — key sha is pinned).
Evidence: code path line 200 + generic Python exit semantics (`python3 -c` FileNotFoundError probe → exit 1, shown above). I did not execute the counter to demonstrate; not run per bounds.

**D4 (low, isolation claim inaccurate; cannot inflate a pass count): each jailed run sees every previously materialized case.**
`main()` lines 211–228: per case a `work` dir is created under the shared `scratch` and never deleted until the `TemporaryDirectory` exits; `jail()` line 168 binds the whole `scratch`. So run N sees runs 1..N−1 (their renamed manifests and plaintext bodies) plus the tool file. The `jail` docstring (lines 163–166) claims the tool sees "only /usr and the scratch directory (its case, the tool file and the escaping body file)" — the parenthetical is false. Sealed expects are never materialized, so nothing here reveals verdicts/findings; the exposure is body text of earlier cases and a "which case index am I" signal. Fix is one line (`--bind work work` + move escaping bodies, or rmtree after each case).

**D5 (info, residual — unverifiable, sealed): `moved` targets are compared verbatim and never renamed.**
`project()` lines 107–108 compares `target` for `reason=="moved"` on both sides; `materialize()` renames only `check` ids and exact `body` refs (line 134), not substrings inside `target`. If any sealed moved target embedded a body path or a check id, an honest tool (which only ever saw fresh names) would deterministically fail. The reference's 28/28 through this counter implies no such embedding; I could not verify the key (sealed), so this stays a residual risk, not a finding of wrong output.

**D6 (info): `--tool-file` mode skips the key-visible refusal by construction.**
The refusal (lines 193–195) only guards the measured revision; in `--tool-file` mode `rev` is None and a file embedding key data would score. Receipts record `toolSha256` and provenance (reference/ablations only), which mitigates. No change recommended for this round.

## Declared behaviors verified correct (imported-module tests, all PASS)
- `project`: observed fresh ids mapped back via inverse map; multiset semantics via `sorted` (order-insensitive, duplicates preserved); `target` compared for `moved` only and discarded symmetrically on the expected side too; non-dict finding → 1-tuple sentinel, cannot false-match.
- `judge`: exit code checked first (line 148); `proc is None` → fail; bad JSON / non-dict report / wrong verdict / `findings` not a list or missing → fail; correct report → pass.
- `materialize`: string ids renamed (`c`+12 hex), `None`/int/`""`/non-dict checks passed through unchanged and still compare equal both sides; `../` bodies written at `work.parent/<fresh>` with manifest ref `"../"+fresh` and byte-identical content; a body path shared by two checks → one file, same fresh name in both checks; unknown body refs untouched; manifest extra fields preserved.
- `met` requires exactly 28 rows and ≥25 passes (line 231); key-visible-at-REV refusal reads the measured revision via `show` (lines 193–195); key sha pin rejects any other key bytes (lines 95–97).

## Not verified
- Anything about the sealed key's contents (ids, duplicate-id presence, moved-target shapes) — out of bounds; D2/D5 impact therefore conditional.
- `bwrap` jail runtime behavior under the real loop (would require running the counter); D4 is established from code paths 211–228 and 162–172 only.
- v1/v2 counter files (out of scope; version 3 is the measured artifact).

Report: .ufo/waves/round-36/w1/ReviewCounterV2.md
