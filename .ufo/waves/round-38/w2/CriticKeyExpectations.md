# Key expectations (C2 sealed cases v3) — critic, wave 2

Attacked: every expectation in `.ufo/waves/round-38/sealed/cases_v3.json` (20 cases, 22 runs).
Hand derivation (all runs, findings + checksEvaluated) written before the first reference run:
`/fast/scratch/hyaku/kake-r38w2/CriticKeyExpectations/hand_derived.txt`.
## 1. Expectation set — no run disagrees with my reading: HOLDS
All 22 runs re-derived by hand (group split/fallback c3, ASCII-only folding c4a, longest
normalized value and allow-tie d1m/d2m/d3m, non-final `$` d4a/b/c, `%XX` normalisation d3n,
implicit allow r1–r4, status ranges, (h) Infinity/NaN runs j1/j2, 5000-digit status j3b,
1e400 j3e, unread-field numbers j4, 43 excluded URL chars u1–u4) agree with the key. Anchors:
"every other key … is ignored and does not end a group" (c3); "compared ASCII case-insensitively"
(c4a); "every other `%XX` escape is kept with its hex digits uppercased" (d3n); "`1e400` and other
non-integer numbers stay floats" (j3e); "a number of any length in a field the contract does not
read changes nothing" (j4); implicit allow not overridden (r2c).
```
$ python3 -B run_ref.py                        22/22 MATCH, MISMATCHES: 0              exit 0
$ internal consistency pass (checksEvaluated, ids, verdict/exit)                        issues: []
$ sealed_count_v3.py --revision af43a50f --key-revision 99357694                       exit 1, 8/20, met false
$ sealed_count_v3.py --revision 3ed8e15c --key-revision 99357694                       exit 0, 20/20, met true
$ sealed_count_v3.py --revision 99357694 --key-revision 99357694                       exit 2, "key visible at the measured revision"
$ sealed_count_v3.py --tool-file reference.py --key-revision 99357694                  exit 0, 20/20
$ sealed_count_v3.py --tool-file /nope/x.py  --key-revision 99357694                   exit 2, "tool file unreadable: ..."
```
Key sha256 `749ef6a6…3aa6` = pin; counter sha256 `28b120a5…f9e4` = every receipt's
`counterSha256`; build tool sha256 `f4d057c4…baace`. Verdict: the expectations are right; the
counter reproduces 8/20 base, 20/20 build, and refuses the reveal revision.
## 2. Three declared clarifications are untested: OVERSTATED
Four single-point mutants of `retained/private/reference.py`, each violating exactly one declared
clarification, all score 20/20, met true, exit 0, zero per-case failures (same counter 28b120a5…):
```
--tool-file mutants/m_emptyq.py    20/20  treats "/robots.txt?" as query-bearing
--tool-file mutants/m_barepct.py   20/20  rejects a bare "%" (clarification: allowed, kept by (e))
--tool-file mutants/m_explicit.py  20/20  explicit "Disallow: /robots.txt" overrides implicit allow
```
sha256 m_emptyq ed00b962…, m_barepct f20d1bf8…, m_explicit e11073ae… (receipts/tools in
/fast/scratch/hyaku/kake-r38w2/CriticKeyExpectations/mutants/). Mechanically confirmed: of the 120
sealed URLs none has a bare `%` or `/robots.txt?`; no sealed robots file has
`Disallow: /robots.txt`. The build is right on all three (checks below), so "20 of 20" certifies
the rules but not the clarifications the C2 text attaches to them.
## 3. The (h) 20 s bound is untested: OVERSTATED
`m_unguarded.py` = reference with `_parse_int` unguarded (sha256 e7907567…), scores 20/20. On a
67,108,864-byte manifest holding one integer literal (inside the 64 MiB cap):
```
$ prlimit --as=4000000000 timeout 20 python3 -B tools/build_robots_audit.py --manifest big.json  exit 1, 167 ms
$ prlimit --as=4000000000 timeout 20 python3 -B mutants/m_unguarded.py       --manifest big.json  exit 124, 20,022 ms
```
The build meets the bound; a predicate-meeting tool does not. The key's largest integer is 6000
digits, so "a manifest within the 64 MiB cap, however long its numbers, finishes within 20 s" is
not exercised (agrees with wave-1 `ProbeDigits`: 24.9 s for one 64 MiB literal).
## 4. Stale contract summary in the private reference: provenance defect (minor)
`retained/private/reference.py:47-49` still states the pre-(k) reading ("compared on the raw
path-to-match … `/robots%2Etxt` are not implicitly allowed"), contradicting code :550-551 and the
key (r1 a, r2 a). Following the docstring fails r1 a/r2 a. Fix the text, not the code.
## Build checks and correction
Reference agrees 22/22; build vs reference identical on `/robots.txt?` allow -> clean; `/a%b`
allow -> blocked; `Disallow: /robots.txt` allow -> clean, disallow -> exposed (t1–t3b in sandbox).
- operability: certification surface narrower than "rules (h), (i), (k)"; freshness untouched.
- Smallest safe correction, no re-key (predicate and key frozen, already measured): (1) amend the
  C2 measured sentence to scope 20/20 to the 22 sealed runs and mark the (h) 20 s bound, the empty
  query, the bare `%` and the explicit-`Disallow` clauses untested; (2) add those four cases to
  the round-39 key before any saturation claim; (3) fix reference docstring :47-49.
- No installs. Read-only git; all runs from sandbox clone at adab4c7e; no lane file modified.
