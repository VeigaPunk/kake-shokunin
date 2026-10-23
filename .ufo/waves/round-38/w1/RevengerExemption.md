# R38 w1 — RevengerExemption: origin of the raw-path implicit allow + NaN/urlsplit; amendment flip audit

Axes: operability (tool-repair correctness, judged axis) and freshness (nothing stale in the
narrative — all pointers re-verified at today's tree). No installs were needed or made.
Bounds: read-only on the lane except this report; sandbox `/fast/scratch/hyaku/kake-r38w1/RevengerExemption/`
(clone at 2dab7f31, TMPDIR under it); no round-38 counter run; nothing under kake-r38{,ctl} touched.

## 1. Who chose the raw-path implicit /robots.txt allow, and on what evidence

- Author: round-37 wave-1 seat **ExecRobotsTool**; landed unedited at 9dbc88b ("C1 build —
  scripts/robots_audit.py (wave-1 ExecRobotsTool, landed unedited)"). Base bytes at af43a50f
  (sha256 944d2f51…d3e5, verified in my clone) are those bytes.
- The choice is disclosed twice by the author: docstring lane-reading bullet,
  scripts/robots_audit.py:46-50 at af43a50f ("compared on the raw path-to-match, before
  normalization (the contract sentence precedes the normalization sentence)"), and
  `.ufo/waves/round-37/w1/ExecRobotsTool.md` open-point choice 6 ("Implicit /robots.txt allow
  compares the raw path-to-match before normalization, so /robots.txt?x=1 and /robots%2Etxt are
  rule-decided"), flagged in its own Risks (line 74-76): "the silent readings the sealed cases
  could pin against me — the raw /robots.txt comparison (6)".
- Evidence the executor had: contract sentence order only (S011/S095 named, no quote deciding the
  point); its own 29/29 case suite (none of which pinned raw-vs-normalized either); **no sealed
  counter access** ("Not verified: the sealed counter and reference behavior (no key)").
- Wave-2 evidence: `.ufo/waves/round-37/w2/ScoutContractAmbiguityR37.md` split 2 (lines 26-35):
  differential run t2, `/robots%2Etxt` vs `Disallow: /robots.txt` — tool+independent raw reading
  (`clean`), ref post-normalization (`exposed`); split 2:1, called undecided. D5 of
  `.ufo/waves/round-37/w2/ReviewRobotsTool.md` (line 28): "unverifiable (contract under-specified)";
  contract (e)'s "both sides are normalized before comparison" can be read to cover this comparison;
  sealed key has 0 occurrences of `robots%2E`/`robots.txt?` (I re-verified by scanning the public
  key at 424aa248: also 0 NaN/Infinity, 0 integers ≥8 digits, 0 ASCII-outside-RFC-3986 url chars).
- So the reading survived round 37 because the executor chose it, an independent implementation
  agreed 2:1 (scout), and no sealed case could pin either side (review + my key scan).

## 2. NaN/urlsplit behavior: what round 37 knew

- D2 (ReviewRobotsTool.md:25): `json.loads` (base line 397) accepts `NaN`/`Infinity`/`-Infinity`
  (not JSON, RFC 8259 §6); wrong against (g). D3 (:26): 5000-digit int → ValueError caught at 398 →
  `input_invalid` where contract wants `check_invalid`; unused-field long int → `input_invalid`
  where contract wants `clean`. D4 (:27): `urlsplit` (line 444) strips tabs/newlines/leading
  controls, so non-RFC-3986 URLs pass as valid. All three common-mode with the independent
  implementation, hence invisible to 28/28 and 137/137. All three were routed as round-38 repairs
  (h) and (i); D5 became (k). Round-37 C1 itself was NOT admitted (round-37 closure, routed defect 1).

## 3. Flip table — round-37 counter (key 424aa248) and 137 selftest per single amendment

Patched variants of the base file, one rule each (sandbox; sha256):
`/fast/scratch/hyaku/kake-r38w1/RevengerExemption/var/k.py` 19671b7b74cdf3d763584fd346e01f2a070d78ae007509a615e9f4bf23405f3b,
`…/var/i.py` 14ca2b932af35e871c3d81ba332508cc2bc463a502266d3574848b2d51047349,
`…/var/h.py` 6f0d6dff1fb761b5a9bbeceac07abf0df4e73189aba4faf649709508932c4297.
Commands (all in the clone; exit codes as shown):
- `python3 -B scripts/robots_audit_selftest.py --tool <variant>` → verdict clean, 137/137 failed 0
  (base, k, i, h; exit 0 by the runner's `failed==0` rule).
- `python3 -B .ufo/waves/round-37/sealed_count.py --root . --tool-file <variant> --key-revision 424aa2480bcbac1832b2aa9da49c51b78ec5092f`
  → exit 0, `met true` every run: base 28/28 (toolSha 944d2f51…), k 28/28 (19671b7b…),
  i 28/28 (14ca2b93…), h 28/28 (6f0d6dff…); `fails []` in all four receipts.

| amendment | counter 28 | selftest 137 | sealed cases flipped | fixtures flipped |
|---|---|---|---|---|
| base (control) | 28/28 met | 137/137 | — | — |
| (k) normalized implicit allow | 28/28 met | 137/137 | none | none |
| (i) RFC 3986 url charset | 28/28 met | 137/137 | none | none |
| (h) JSON numbers | 28/28 met | 137/137 | none | none |

**Answer: the round-38 amendments contradict no round-37 sealed case and no selftest fixture.**
The only round-37 artifact (k) reverses is the tool's own disclosed open-point reading
(docstring 46-50 / ExecRobotsTool.md choice 6) — an undecided point, never sealed, never pinned.

Patches are non-vacuous (differential probes, exit codes + reports observed):
- (k): manifest naming `robots.txt` = `disallow: /robots.txt`; urls `…/robots%2Etxt`, `…/%72obots.txt`,
  `…/robots.txt?x=1`, `…/robots.txt` (all expect disallow). Base: exit 1, only `k4` exposed.
  k.py: exit 1, `k1,k2,k4` exposed — %2E/%72 flip to allowed, `?x=1` stays rule-decided (matches
  the C2 clarifications: `/robots.txt?` would be allowed via empty query; `/ROBOTS.TXT` not exempt).
- (i): urls with space / tab (404 checks): base exit 0 clean → i.py exit 2, `check_invalid` on the
  two faulty checks; non-ASCII `ä` host check kept (evaluated). h.py/base unchanged on this probe.
- (h): (m1) 5000-digit int in unused top-level field: base exit 2 `input_invalid` → h.py exit 0
  clean. (m2) `robotsStatus: NaN`: base `check_invalid` (check h2) → h.py `input_invalid` (check
  null). (m3) 40-digit valid status + 5000-digit unused check field: base exit 2 → h.py exit 0.
- (h) declared bound: 64,000,037-byte manifest of unquoted digits: base exit 2 input_invalid in
  0.09 s (early 4300-digit ValueError); h.py exit 0 clean in 0.08 s ≪ 20 s.

## 4. Findings for the L1 (advisory)

1. ScoutContractAmbiguityR37.md:34 overstates: "Selftest fixture e11-robots-txt-exemption-is-exact
   pins the tool's pre-normalization reading". Empirically e11 (selftest :505-508, url
   `/Robots.txt` + `Disallow: /Robots.txt`) passes unchanged under the (k) post-normalization
   comparison — it pins only exactness/case, not raw-vs-normalized. Nothing in the selftest pins
   the raw reading; (k) is freer than wave 2 believed.
2. Symmetrically, nothing in the 28 sealed cases or 137 fixtures pins NaN, long integers, url
   character faults, or the normalized implicit allow: the harm instruments cannot detect a
   build that drops (h)/(i)/(k), exactly as the SCORECARD's ablation table (raw-path implicit
   allow 16, etc.) already says for the v3 key. The 28/28+137/137 pair is necessary, not sufficient.
3. Divergence candidate at base worth keeping on the radar: an unreadable-after-validation robots
   file is `check_invalid` (D8) and the 64 MiB digit flood is `input_invalid` at base — (h) moves
   the latter to clean; no round-37 instrument covers either.

Confidence: high for all runs (direct execution, receipts summarized above, base control
reproduces the declared 28/28 and 137/137). Not verified: the round-38 sealed keys/counters (not
mine to run); the private reference's exact bytes; behavior of (i) on U+007F/DEL and controls
beyond the probed space/tab (patch rejects all ord<128 outside the allowed set by construction).
No round-38 counter, no sealed directory, no lane mutation was touched.
