# MutCounters — mutation-test of the round-100 frozen counters (w1, kake round 100)

Seat: MutCounters-5 (leaf, no subagents). Target: `c100_registry.py` and `c100_fresh304.py` at the
instruments commit. All work inside `w1/MutCounters/` and scratch
`/fast/scratch/hyaku/kake-r100/MutCounters-5/` (deleted before yield; deliverables and evidence
copied out first). Lane untouched: read-only git only; digest re-verified after all runs.

## Method

1. Verify, then attack: `sha256sum -c controls/instrument-sha256.txt --quiet` → all 22 entries OK
   before any mutant ran (rc 0). Lane tip `master` = `e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f`
   (the C1 repair commit, as staged).
2. Baseline (pristine counter bytes copied to scratch): the full committed battery was re-run and
   compared byte-for-byte against the committed receipts. **19/19 reproduced identically**
   (stdout + rc): `ctl-c1-selftest.txt`, `base-c1.txt`, `ctl-c2-selftest.txt`, `base-c2.txt`, and
   all 15 `ctl-c2-*.txt` candidate controls. The three C1 fixtures were rebuilt per `controls.sh`
   (clone --shared into scratch → detach `3989618d` → `c1_repair_fixture.py <mode>` → commit with
   fixture identity via -c flags only); fixture SKILL.md sha256 matched the committed receipts:
   pos `397b6dec…` MATCH, keepold and deleteall MATCH (reproduced, never re-stamped; fixture
   commit shas necessarily differ, counter output lines compared).
3. 32 single-point mutants (15 registry + 17 fresh304), one predicate-bearing line each, anchored
   by exact-string match asserted unique in the file (`count==1`), each `py_compile`d:
   registry — interpreter set, flag-skip loop, assignment-strip, escaped-pipe split, duplicated
   threshold (>2, >=1), CODE lookbehind, CODE lookahead, probe argument, sandbox unshare scope,
   met sum, names_path boundaries, fence length, population depth filter;
   fresh304 — qualified-name tuple, case folding, quoted-escape path, OWS after comma, leading
   OWS, inter-element garbage tolerance, output trim (dropped / OWS-set), stored PROXY drop,
   PROXY membership, HOP exclusion, decide_bytes error set, judge trailing-NL, judge whitespace
   strictness, sandbox_ok pid assertions, etag trim, stored last-modified trim.
4. Detector = (rc, stdout) of each command vs pristine on the same fixture/dir. Battery per
   registry mutant: `python3 -B <mutant> --selftest --work <scratch>/...`, `--root LANE
   --revision 3989618d… `, and `--root <fixture> --revision HEAD` for pos/keepold/deleteall
   (5 commands). Per fresh304 mutant: `--selftest`, `--root LANE --revision 3989618d…`, and
   `--candidate-file frozen/<15 candidates>.py` (17 commands). Every mutant ran its complete
   battery: 32/32 × (5 or 17) = 352 counter runs + 19 pristine runs; no MISSING cells in
   `mutants.tsv` (judge marks INCOMPLETE loudly if any run is absent — none was).
5. Each survivor was challenged with a constructed separating input executed against pristine and
   mutant (`evidence/sepout-*.txt`).

## Results

**registry 8/15 killed, fresh304 13/17 killed, 11 survivors, 1 equivalent** — full table in
`w1/MutCounters/mutants.tsv`, per-survivor analyses in `w1/MutCounters/survivors.md`, raw evidence
in `w1/MutCounters/evidence/`.

Killed highlights (first observed divergence, pristine → mutant):
- reg-m03 (flag-skip loop removed): base flips to `duplicated=0 probe_mismatch=0 mismatches=0
  met=true` rc 0 — a one-loop mutant **fakes the C1 target at base**; caught by selftest
  (`no-verdict` case) and keepold. The probe/duplicate machinery is load-bearing for the round
  verdict, not just decoration.
- reg-m07 (duplicated ≥1): base `duplicated=55`, pos fixture met flips true→false (rc 0→1).
- reg-m09 (CODE lookahead `(?=\s*[=:])` only): base `probe_mismatch=44`; killed on all 4 registry
  commands (backtick-terminated bare digits must keep counting).
- fr-m01/fr-m02 (qualified-name tuple / case folding): `fresh-self` rc 0→2 — the counter's own
  reference-drift guard kills reference mutants before any candidate runs.
- fr-m13 (judge trailing-newline): killed on `fresh-base` and all positive-oracle-bearing
  candidates (newline allowance is load-bearing).
- fr-m16/fr-m17 (etag / last-modified trim): killed on hand cases (`v2-strong-trim`,
  `e3-lm-tab-trim`) via reference drift.

Survivor coverage findings to route (instruments frozen — admissions, not repairs):
1. **fr-m14 is the serious one**: dropping the judge's whitespace strictness lets a semantically
   correct candidate that prints `"   {json}   \n"` score `hand=91/91 generated=300/300 met=true`
   rc 0. No committed forgery exercises the success-whitespace clause (`neg-e4-wsstdout` fails via
   refusal-stdout only). The frozen C2 predicate is reachable by a padded candidate under a judge
   mutation; the 13-forgery battery has a blind spot there.
2. The registry probe/sandbox guarantees are only network-tested, and degenerately so on this
   host: outbound 1.1.1.1:53 is unreachable, so `v2-probe-sandbox-no-network` passes even under
   `--unshare-net`-only (reg-m11). PID-namespace isolation — the property the fresh304 counter's
   own `sandbox_ok` asserts — is untested by any registry control (separated by a /proc-introspecting
   tool).
3. Fence parsing (reg-m14): the committed `[:3]` truncation mis-parses >3-char fences (mutant is
   CommonMark-correct; rows 0 vs 1 on a constructed SKILL.md).
4. `INTERP` membership (`python`, `node`) and `names_path` boundaries are structurally dead on the
   committed registry (no committed row exercises them); both separate immediately on constructed
   rows and flip `met`.
5. reg-m05 shows the escaped-pipe split is only behavior-bearing when the escaped pipe is adjacent
   to the invoked path — the committed piped-invocation case cannot detect the mutant.
6. fr-m12: the `UnicodeDecodeError` arm of the error set is redundant (`ValueError` subclass); the
   `RecursionError` arm is real (separates at depth 60000: pristine Refuse vs mutant CRASH) but
   unreachable from the committed hand/generated populations.
7. fr-m15 (`sandbox_ok` pid assertions dropped): equivalent-in-context — the probe re-asserts what
   the `SANDBOX` argv guarantees on this host; no constructable separating input without sabotaging
   bwrap (host change forbidden by bounds). Pure defense-in-depth.

## Honesty / evidence

- Every verdict line in `mutants.tsv` is backed by stored run artifacts (rc/stdout/cmd per command
  under scratch `results/`, summarized in `evidence/evidence-summary.txt`); every rc quoted above
  was observed, none inferred. Pristine-vs-receipt comparison: 19/19 byte-identical.
- Restoration: the frozen counters were never written; post-run re-check
  `sha256sum c100_registry.py c100_fresh304.py` in the lane matches `controls/instrument-sha256.txt`
  (c25d981e… and e7dff63b…, re-verified at cleanup, rc 0). Mutants and fixtures lived only in the
  scratch seat dir, deleted at cleanup. No tool was installed or upgraded (none needed).
- No mutating git/jj command touched LANE or the fleet repo; fixture clones were created, used,
  and destroyed one mode at a time inside the scratch seat dir.

`disk-guard.sh status` before start: rc 0, `/fast/scratch/hyaku` 51% used, 399.5G free.

MUT registry=8/15 fresh304=13/17 survivors=11 equivalent=1
