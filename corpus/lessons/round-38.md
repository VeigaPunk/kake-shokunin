# Round 38 — robots audit repair under a redesigned counter

## Claims

Base `af43a50fa399881eead9381d835b78a015e277a6`. Round 37 was not admitted
(`corpus/lessons/round-37-verifier-spotcheck.md`). Its stdlib-plus-six-patches control met C1's
predicate before the build, and the lane kept the claim. This round re-claims the same tool under
a redesigned counter (routed defect 2) and appends the closure correction (routed defect 1).

- **C1** (declared `b0ab7f60`, counter v2, `met: passed >= 19 of 20 sealed cases`): **withdrawn
  before any build** at `2dab7f31`. Its declaration listed a cheapest-wrapper shortcut and a
  mutation pass on the reference among its controls. The mutation pass met the predicate (29 of
  42 mutants), and so did wrappers that implement all three rules. The declared consequence was
  "redesign before any build or withdraw", with no reclassification. A wrapper that does every
  rule cannot be put below any target, so C1 was withdrawn.
- **C2** (declared `2dab7f31`, counter v3, `met: passed >= 20 of 20 sealed cases`): the same three
  rules, (h) non-JSON number literals and integers of any length, (i) URL characters, (k) the
  implicit `/robots.txt` allow on the normalized path. It uses a stricter key (one check per
  excluded ASCII character; extra (c)/(d)/(k) checks; every run states `checksEvaluated`), a
  20-of-20 target and control classes named in advance. Before 8 of 20 (`af43a50f`); after
  20 of 20 at `3ed8e15c` (reveal `99357694`).

## Gate

### Source openings (2026-10-23, wave 1)

- S034 RFC 8259 — https://www.rfc-editor.org/rfc/rfc8259.txt — accessed 2026-10-23T04:30:20Z, HTTP 200,
  sha256 `61a5378f…2cd2d7` (identical to the 2026-10-21 opening) — re-open, keep, tier A, spec,
  mined. Quote “Numeric values that cannot be represented in the grammar below (such as Infinity
  and NaN) are not permitted.” (§6). `used-by` widened (below).
- S098 RFC 3986 §§2.1–2.3 — https://www.rfc-editor.org/rfc/rfc3986.txt — accessed 2026-10-23T04:30:17Z,
  HTTP 200, sha256 `3102dae4…b2d683` (same bytes as S029) — admit, tier A, spec, mined. This scope
  is one S029 (§3) and S089 (§5.2) do not hold. Quote “Characters that are allowed in a URI but do
  not have a reserved purpose are called unreserved.” (§2.3). Per-character check of rule (i)
  against §§2.2/2.3: 85 allowed, 43 excluded, 0 mismatches (`w1/ScoutReopenRFC3986s2.md`).
- S011 RFC 9309 — https://www.rfc-editor.org/rfc/rfc9309.html — accessed 2026-10-23T04:30:20Z, HTTP 200,
  sha256 `bbaa2806…dc1a87` (the same bytes as the round-37 retained copy) — re-open, keep, mined.
  Quote “The /robots.txt URI is implicitly allowed.” (§2.2.2).
- S099 RFC 9309 §§1–5 — https://www.rfc-editor.org/rfc/rfc9309.html — accessed 2026-10-23T04:30:34Z,
  HTTP 200 — admit, tier A, spec, mined. It supersedes S011's host-root scope (the round-37 owed
  superseding row). Quote “use case-insensitive matching to find the group that matches the
  product token” (§2.2.1).
- S100 Python json docs — https://docs.python.org/3/library/json.html — accessed 2026-10-23T04:30:22Z,
  HTTP 200, sha256 `234b80bf…a07f792e` — admit, tier A, docs, mined. Quote “It also understands NaN,
  Infinity, and -Infinity as their corresponding float values, which is outside the JSON spec.”
  (`json.loads`; `w1/ScoutPythonJson.md`).
- S101 WHATWG URL Standard — https://url.spec.whatwg.org/ — accessed 2026-10-23T04:30:17Z, HTTP 200,
  sha256 `08cb42a9…` — **reject**, tier A, spec: the contract is RFC 3986, and the tool does not use
  a WHATWG parser; WHATWG strips and removes the characters (i) rejects. Flip: the lane adopts
  WHATWG parsing or requires browser-equivalent normalization. Quote “The URL parser takes an
  arbitrary scalar value string and returns either failure or a URL.” (§4.4).
- Not a row: Google's parser (S096, `robots.cc` at `22b355ff`) has no implicit allow and does not
  decode the path (`w1/ScoutGoogleImplicit.md`). The knowledge entry records this as a difference.

Registry changes, old → new: S034 `used-by` `corpus/knowledge/static-canonical-preflight.md,
corpus/lessons/round-24.md` → `…, corpus/knowledge/robots-txt-rules.md`; S098, S099, S100 `—` →
`mined` (recheck 365d, 365d, on-release; used-by `corpus/knowledge/robots-txt-rules.md,
corpus/lessons/round-38.md`); S101 `—` → `rejected` (recheck 90d). S011 status, recheck and
used-by unchanged.

### Claim gate

- **Reject: C1** (`b0ab7f60`). Controls of its own declared kinds met its predicate: 29 of 42
  `MutRefPass` mutants, plus `CtlLabelShortcut` delegate ceiling, `CtlBaseWrapper` care and
  `CriticPredicate` rulepatch(_pct) at 20 of 20. Withdrawn before any build seat was dispatched
  (receipts `.ufo/waves/round-38/verification/control-*.json`, `mutref/`).
- **Admit for measurement: C2** (`2dab7f31`). Every control of the named classes scored at most
  16 of 20 under v3, and all 42 mutants and 8 ablations scored at most 19 (`verification/v3/`).
  Control receipts landed at 04:28:54Z, 58 s before wave 1 was dispatched (`w1-dispatched-at.txt`;
  `criteria/receipts/timeline-r38.txt`).
- Not admitted as a fix: counter v3 still judges only exit, verdict, `checksEvaluated` and
  findings, and its control classes were written while the four 20-of-20 tools were already
  scored under v2. Wave-1 `CriticControlReceipts` reads this as possible reclassification; the
  closure rules on it.

## Controls

See `SCORECARD.md` "Round 38 — control call results" and "Round 38 — C2 declared". Seven control
seats returned; there were no dead seats. Two of them disclose touching the sealed directory's
path: `CtlStdlibV2` ran one `test ! -e`, and in wave 1 `ProbeDigits` ran one `test -d`. Neither
opened anything inside it. A third, `CriticControlReceipts`, listed the child names of
`/fast/scratch/hyaku/kake-r38ctl` once.

## Non-claim routed repairs

- Routed 1: SCORECARD "Round 37 — closure correction"; both robots capability rows end in
  "not admitted". Each row is an in-place append, so `git diff` shows the 2 lines changed.
- Routed 3: QUALITY (j) check `control_consequence_check.py`. Exit 1 on round 37, 0 on rounds 36
  and 38; selftest 10/10.
- Routed 4: QUALITY (k) is a rule only (there was no dead seat to test it on).
- Routed 5: `pinned_selftest.py`. Round-37 postfix pinned at `944d2f51…d3e5`, 137/137. Every
  round-38 harm receipt names `toolSha256` and `toolRevision`.
- Carried round-37 items closed: robots `NaN`/long integers/malformed URLs (C2); `source_recheck.py`
  body reads capped at 16 MiB and `MemoryError` on a near-cap manifest mapped to `input_invalid`
  (fixtures g33–g35 red on base, green on fix; 106/106; round-36 counter 28 of 28).
- Robots selftest 137 → 194 fixtures. They were written blind; the base fails exactly the 45
  (h)/(i)/(k) fixtures, and the round-37 shortcut fails 44.

## Mistakes

| Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|
| Control consequence overridden by reclassifying the control (round 37) | `round-37-verifier-spotcheck.md:59-71` | QUALITY (j), which had no check | `control_consequence_check.py`: round 37 exit 1, round 36 exit 0 (`criteria/receipts/ccc-*.txt`) |
| Control receipts landed after the build seat was dispatched (round 37) | spot-check lines 36–38; `round-37/w2/ReviewTimeline.md` | none | `timeline_check.py`: round 37 exit 1 (435 s late), round 38 exit 0 (`criteria/receipts/timeline-*.txt`) |
| Post-measurement receipt named the tool by path only (round 37) | spot-check lines 41–43 | none | `pinned_selftest.py` (QUALITY (l)); pinned re-run receipt |
| Control list that includes tools doing the claimed work (round 38 C1) | SCORECARD "Round 38 — control call results" | the declared consequence itself fired, which withdrew C1 | QUALITY (n). No check yet; read the list against the claimed rules before freezing |
| Count misreported: "28 of 42" mutants met C1, receipts say 29 | `verification/mutref/` | wave-1 `CriticControlReceipts`, `CriticClaimSizing` | correction appended to SCORECARD "Round 38 — measured results" |

## Holds and dead seats

No dead seats and no refusals in the control call or wave 1 (wave 2 in the report).

## Carried open

- Symlinked manifest directory; U+FFFD per byte versus per maximal subpart (round-37 contract points).
- Duplicate JSON member names (undecided, untested).
- Dot segments in the implicit-allow path (decided by the rules; RFC silent).
- `source_recheck.py` body-path race (narrowed, not closed); criteria false passes/fails (round-37
  `ReviewCriteriaV2`).
- The control-consequence check classifies receipts by file name.
