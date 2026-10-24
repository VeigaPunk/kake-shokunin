# Review: counter v3 new code (run E, T-shape defect placement, T4 renaming, RUNNER dumpable, append mode)

VERDICT: no defect found — every docstring statement about the five attacked areas holds against code and runtime probe; one minor wording overstatement (T2/T3 "at any position").

Attacked: `.ufo/waves/round-42/c42_count_v3.py` sha256 ce2d5a0ca2c3768ce2b1d7b9a57592817d7f16616ee7fb25989e580a70160acc (repo tip 721310b19af88d3c43c01647d3ce29d51e6e3b96, identical to 3490614's blob da5f2ba).
Diff v2→v3: `git diff c23c145c 3490614 -- .ufo/waves/round-42/c42_count_v3.py` (exit 0; v3 is a 769-line new file; v2 extracted via `git show c23c145c:.ufo/waves/round-42/c42_count_v2.py`, 672 lines, compared with `diff -u`, exit 1 as expected).

## Checks run (exit codes)
- Imported the module (sandbox copy) and exercised: e_units/cases_e/slot_value/layout_cases/shape_t1/t2/t3/t5/shape_t4/Sandbox.run. All exited 0 after fixes to my own instrumentation (two iterations; see gaps).
- bwrap probe (counter's exact argv, bwrap 0.13.1 non-setuid, unprivileged userns, uid 1000→1000, tool CapEff=0):
  with prctl(4,0): FD-LIST-DENIED errno 13 (exit 0); counterfactual without it: FD-LIST-OK + OPEN-RW-OK on the timing fd (exit 0).
- Live Sandbox runs (stub tool inside bwrap): plain cpu 0.0109 s; orphan-burning variant cpu 0.5473 s; repeat run clean; no leftover .out/.t (exit 0).
- T4 functional check against `.ufo/waves/round-41/realrun/` read-only: content set byte-equal (6/6 non-manifest blobs, exit 0).

## Run E — cases_e / slot_value (docstring lines 16-24)
- holds: 242 units = 128 ASCII + 13 percent forms (E_PCT, 6 with non-ASCII digits or case-fold partners: :315-317) + 40 BOUNDARY (:306-308, surrogates D800/DBFF/DC00/DFFF present) + 21 LOOKALIKE (:312-314) + 40 seeded random cps from U+0080-U+10FFFF (surrogates included, :321-324).
- holds: `sitemapUrl` takes every unit (2662 = 242×11), `loc` only XML-legal ones (2277 = 207 units×11) — cases_e:368-375, xml_legal:214.
- holds: insertion at random position, ends included — insert:138-141 (`randint(0, len)`); measured front 398 / back 368 / middle 1434 over 2200 slot_value builds.
- holds: unit lands in the correct slot in all 11 slots (zone after `%25` vs after `%`: :345-348; IPvFuture body: :341; IPv6: :342). Lone surrogates (44 values, all sitemapUrl) survive layout via json default ensure_ascii — no counter crash.
- note (benign): identity duplicate "%" — chr(0x25) among the ASCII units equals the E_PCT "%"; duplicate case value only, no docstring mismatch.

## T-shape defect placement (docstring lines 42-51)
- holds: T1 all 20,000 carry one defect; window last-64 fraction 0.501 (half/half) — shape_t1:489-492, long_value:278-303.
- holds: T2 fraction 0.020, T3 fraction 0.0156, both inside the per-file 1-3% (p=rng.uniform(0.01,0.03):496,502); T5 40/40 first, 0/8 rest, win64 20/40 — shape_t5:507-521.
- holds: 600 direct long_value trials, 0 violations of `b == len-len(unit)`, `a == head_len` or `max(head_len, b-64)`, `r in [a,b]` — "at or after the path start" and "last 64 positions" exact.
- overstated (wording only): T2/T3 docstring say "one defect at any position" (:44,:46) but placement is code-shared with T1, i.e. at-or-after the path start; scheme/host/authority never defected. T1's own sentence is exact. No material effect: both tools judge identical bytes; predicate unaffected.
- holds: "no timing file can be judged right without judging each value" — defects present in T2/T3 (>0 measured) and every timing repetition compared with ref41 output (:728-741).

## T4 renaming (docstring line 47-48; shape_t4:525-557)
- holds: SHA256SUMS verified before copy (CannotEvaluate on mismatch); copies under random names in a random subdirectory; original names not reused; manifest.json not copied; check ids random and unique; content set byte-identical (6/6). Unchanged v2→v3, confirmed working at tip.

## RUNNER dumpable (docstring lines 38-40; RUNNER:562-580, prctl line 566)
- holds: prctl(PR_SET_DUMPABLE=4, 0) before Popen; probe proves it both ways: hardened → tool (same ns, uid 1000, CapEff 0) denied /proc/<runner>/fd (errno 13); unhardened → FD-LIST-OK and the timing fd opens O_RDWR. Real hardening, not redundant (`--proc /proc` is mounted, Sandbox.run argv :606).

## Append mode (docstring line 40; :602)
- holds: timing file opened "ab"; fresh random path per run so semantics match; last-line parse correct across repeated runs; runner writes after the reap loop, so even a leaked fd could not displace the final line (append is a second layer behind the dumpable fix). Orphan CPU captured (0.5473 vs 0.0109) — "CPU time … every descendant" holds (:562-580).

Incidentally verified: run E wired into driver (:700, :707); five equality runs; seed from os.urandom recorded when --seed absent (:652); met requires all five exact ratios (:757-762 region).

## Residual risk / verification gaps
- I did not run a full scoring pass of the counter (other seats own scores); all attacked code was exercised at unit level plus a live sandbox replication of its bwrap argv on this host. A different kernel/bwrap could alter the dumpable probe outcome; here it is the canonical runtime.
- Dumpable probe used a replica runner/tool, not the counter's own files; prctl ordering was verified by reading (:565-566 precede Popen :567).
- Two instrumentation iterations of mine produced false alarms (positional-arg capture; basename mapping on renamed T4 files; `@`-in-path split) — all resolved as my errors, none are code defects.
- No tools installed (none needed).
