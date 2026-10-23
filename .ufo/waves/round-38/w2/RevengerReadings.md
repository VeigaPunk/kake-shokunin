# Kake R38 W2 — RevengerReadings (build docstring vs C2 clarifications vs independent readings)

Sandbox `/fast/scratch/hyaku/kake-r38w2/RevengerReadings/` (clone at tip `adab4c7`; `git diff
--stat 3ed8e15c adab4c7 -- scripts/robots_audit.py` empty). Tools: build `scripts/robots_audit.py`
sha256 `f4d057c4…baace` (bytes equal at 3ed8e15c, `git show | sha256sum` equal); independent
`independent_robots_audit.py` sha256 `ee78ba46…95b1` (matches w1/ExecIndependent.md). No tools
installed (host python 3.14 sufficed); no lane file touched except this report.

## Counter runs (evidence both readings sit inside the sealed surface)

- `python3 -B .ufo/waves/round-38/sealed_count_v3.py --root . --revision 3ed8e15c2707…f2b0 --key-revision 99357694` → exit 0, **20 of 20, met** (counterSha256 `28b120a5…f9e4` = file hash).
- Same with `--tool-file <sandbox>/independent_robots_audit.py` → exit 0, **20 of 20, met**. First
  v3 score of the blind tool; lane `verification/w2/` did not exist when I ran (glob: path not found).

## Readings diff — where the three sources choose

Sources: build docstring (`clone/scripts/robots_audit.py:36-100`), independent docstring readings
1–14 (`independent_robots_audit.py:6-32`), C2 clarifications (SCORECARD at `adab4c7`,
lines 2254-2257) and round-37 (e) (SCORECARD:1839-1846). Agreements, each shown by an input
(harness `probe.py` sha256 `487211ba…46ff`, run exit 0, 1.2 s):

- (k) matrix — input `r.txt` = `User-agent: *\nDisallow: /\n` plus 8 checks. Both tools, parsed
  JSON identical: `https://x/robots.txt` allowed despite the explicit Disallow; `/robots.txt?`
  allowed (empty query); `/ROBOTS.TXT`, `/robots%2Ftxt`, `/robots.txt?x=1` blocked; `/robots%2Etxt`,
  `/%72obots.txt`, `/robots.txt#frag` allowed. = C2 clarifications verbatim. Build docstring (k)
  bullet and independent reading 1 agree. Holds.
- Bare `%` — url `https://x/a%zzb`, rule `Disallow: /a%zzb`: both `failed-policy`/`blocked`, i.e.
  `%zz` allowed by (i), kept by (e). = C2 clarification line 2254-2255; independent reading 13.
  Holds.
- 15 vs 4000 digit sentinel — probes `robotsStatus` of 100 / 3999 / 5000 digits → `check_invalid`
  both; 16-digit `version` → `input_invalid` both; 200-digit inert field → `clean` both. The
  thresholds (build `_INT_TOKEN_DIGITS=15`, line 161; independent `INT_DIGIT_LIMIT=4000`, line 47)
  are behaviorally indistinguishable, exactly as C2's "however many digits it has" requires.
  Holds; ProbeDigits.md already said the threshold is "a cost knob, not a correctness knob".
- Timing bound — 2,000,000-digit `robotsStatus`: both finish ~0.017 s (20 s bar). (h) bound holds.
- Dot segments — no source states a dot-segment reading; rule (e) (SCORECARD:1842-1846) enumerates
  normalization exhaustively without dot-segment removal, so all three silently agree. Input
  `https://x/a/../robots.txt` and `/./robots.txt` with `Disallow: /`, expect allow: both
  `blocked`. Consistent with the contract; RFC 3986 §5.2.4 fans may call it surprising, but that
  is the contract's choice, not a tool defect.

## Divergences found

- D1 (real, input shown): lone surrogate in a URL (JSON `"\ud800"` escape). Build docstring
  (line 97-99): percent-encoded via `surrogatepass`, "always reports". Input
  `{"version":1,"checks":[{"id":"s1","url":"https://x/a\ud800b","robotsStatus":200,"userAgent":"b",
  "expect":"allow","robots":"r.txt"}]}` with `r.txt` = `Allow: /a%ED%A0%80b`: build → exit 0,
  `clean`; independent → exit 2, `check_invalid` (its `percent_encode_non_ascii` raises
  UnicodeEncodeError, caught as ValueError). Neither counter (both 20/20) nor the 194-fixture
  selftest (grep `surrogate|ud800`: no match) pins this reading. The independent's "readings
  where the text admits more than one" list (1–14) omits surrogates entirely — its claimed
  completeness is overstated; the build docstring's reading is the load-bearing one and holds.
- D2 (docstring rationale overstated, both sides): build docstring line 96 and independent reading
  10 justify the sentinel with "int() … is quadratic". Wave-1 ProbeDigits.md (committed) measured
  exponent 1.47–1.54 on CPython 3.14 (`_pylong.int_from_string`), i.e. not quadratic — though one
  64 MiB literal still takes 25 s > 20 s, so the sentinel itself remains necessary. Rationale
  wrong, decision right; no behavior change (probe P5).
- D3 (code reading, INFERENCE, no fixed input): build docstring bullet (lines 40-42) rejects a
  manifest whose read exceeds a short stat ("input fault"); independent `read_manifest` does
  `handle.read()` unbounded after stat, so a file grown between stat and read is parsed, not
  rejected. Needs a racing file to demonstrate; flagged, not scored.

## Verdicts

- "Build docstring readings (k)/(i)/(h) match the C2 clarifications" — holds (probes P2, P3, P4, P5).
- "15 vs 4000 sentinel is an observable divergence" — wrong: convergent behavior on every probed
  input; divergence is only in docstring choice and rationale.
- "The independent implementation is behaviorally equivalent to the build" — overstated: D1 shows
  clean vs check_invalid on a surrogate URL, unpinned by counter or selftest.
- "Dot segments are a point where the readings differ" — wrong: all three sources are silent and
  rule (e) pins the behavior; both tools agree (P6).
- Counter v3 on the build at 3ed8e15c and on the independent tool: both met, 20/20 (exits 0).

Artifacts (absolute paths): `/fast/scratch/hyaku/kake-r38w2/RevengerReadings/probe.py`
(`487211ba3d7b089c0982e103ff795f41fb17b2e7f3c015e60475e73d633346ff`), fixtures under its
`tmp/probes/` (p1 manifest `71deba5d…2557`), tool copies as hashed above.
