# ScribeRegistry — round-92 capability row draft (for the L1 to apply)

I do not edit `SCORECARD.md`; the L1 owns it. This is the row text, ready to paste.

## Where it goes

`SCORECARD.md` → a new `### Demonstrated repertoire — round 92` section, in the
house form of `### Demonstrated repertoire — round 91` (four columns:
`Capability | What it can now do | Evidence | First-working round`).

## The row

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| Heuristic freshness decision | From a stored status and header map, an integer `Date` and an optional shared-cache flag, decide whether a heuristic expiration time may be assigned to the stored response and what lifetime it carries — one decision out of five (`explicit` / `heuristic` / `not-heuristically-cacheable` / `heuristic-undecided` / `not-storable`), the heuristic lifetime being `min((Date - Last-Modified) // 10, 86400)` under the lane's own 10 % and 86400-second conventions; refuses malformed input (duplicate case-variant header name, signed or quoted delta-seconds, empty Cache-Control directive, missing or non-integer `Date`); decides nothing about storage, keys, revalidation, serving or any live property | `scripts/heuristic_freshness.py`; `.ufo/waves/round-92/c2-contract.md` (clauses 1–13, sha256 `5fc49c7af47ce4331563bf991e4199817eef8748621b02e05682a4f01f14c944`); `.ufo/waves/round-92/c92_heuristic.py` (28 hand cases, 120-case seeded population, five frozen forgery subjects, audit-hook sandbox); `corpus/knowledge/heuristic-freshness.md`; S470; `w1/ExecHeuristic.md`, `w1/ExecStubs.md`, `w1/ReviewC2.md` | 92 (demonstrated; round unadmitted, instrument defects routed) |

## Move-log row the L1 may also want (same shape as round 91's)

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 92 | freshness (HOLD, capability acquisition) | candidate absent at `e143faff` | tool meets the frozen counter `hand=28/28 generated=120/120 forgeries_refused=5/5` at the carrier | `.ufo/waves/round-92/controls/{base-c2.txt,after-c2-carrier.txt}` |
| 92 | calibration (HOLD 2) | `open=3 closed=0` at `e143faff` | `open=0 closed=3` at the carrier | `.ufo/waves/round-92/controls/{base-c1.txt,after-c1-carrier.txt}` |

## Claim-table row (shape of round 91's two-row claim table)

| Claim | Axis / score delta | Before → after | Counting command | Evidence / author verdict |
|---|---|---|---|---|
| C1 the routed round-91 instrument defects K91-1, K91-2, K91-4, K91-5 close | calibration 2→2 HOLD, lowest owned | `open=3 closed=0 met=false`, exit 1 at base → `open=0 closed=3 met=true`, exit 0 at the carrier | `python3 -B .ufo/waves/round-92/c92_defects.py --root . --revision <REV> --work <scratch>` | `controls/base-c1.txt` → `controls/after-c1-carrier.txt`; the counter is frozen and is not repaired after scoring |
| C2 a heuristic freshness decision instrument | freshness, capability acquisition | `candidate=absent … met=false`, exit 1 at base → `hand=28/28 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok met=true`, exit 0 at the carrier | `python3 -B .ufo/waves/round-92/c92_heuristic.py --root . --revision <REV> --work <scratch>` | `controls/base-c2.txt` → `controls/after-c2-carrier.txt`; tool `scripts/heuristic_freshness.py`; measured met on the frozen predicate; not admitted by this round |

## Honest limits the L1 should keep in the row text

- The C2 gate scores **contract v1**, not the RFC. Its 28 hand cases and its
  120-case generated population were written by the same round as the contract.
  `met=true` is conformance to the contract and never evidence about a deployed
  cache.
- The 10 % fraction and the 86400-second cap are the **lane's** conventions. The
  RFC calls 10 % "a typical setting" and names no cap.
- The tool is a **decision over supplied integer seconds**: no clock, no
  HTTP-date parsing, no network, no storage, no revalidation exchange, no
  serving permission, no browser observation.
- The gate's `anti_table` conjunct is a substring screen over the five forgery
  stems and the 28 hand-case input digests, so a legitimate candidate that
  merely quoted a stem in prose would be refused — a designed false positive.
