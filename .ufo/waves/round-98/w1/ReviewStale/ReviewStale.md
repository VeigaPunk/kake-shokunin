# ReviewStale — C2 semantic ground: contract + 60 hand expectations vs RFC 5861/9111

Round 98, seat ReviewStale (leaf, no subagents). Scope per seat spec: (1) judge hand cases
H01–H60 in `.ufo/waves/round-98/c98_stale.py` against the retained RFC bodies or against
contract sentences explicitly marked as lane conventions; (2) list conventions-stated-as-RFC
and RFC rules in scope that the contract omits; (3) review the ExecStale candidate against the
contract if it exists at review completion.

## Verification trail (commands and observed results)

- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse master` → `7838981e…` (rc 0);
  freeze commit `c3eace8b` present with subject "round-98: freeze C1/C2 predicates…".
- `sha256sum` over all 11 entries of `.ufo/waves/round-98/controls/instrument-sha256.txt`
  (c98_captable.py, c98_stale.py, stale-contract.md, gen_cap_rows.py, six frozen/neg-*.py,
  frozen/pos-oracle.py): every computed digest equals the stored digest — no frozen-byte drift.
- `sha256sum .ufo/waves/round-98/sources/rfc5861.txt` → `1193f1c8710af162…dd2529e`, matching the
  freeze's S482 digest.
- RFC 9111 body read at `.ufo/waves/round-96/w1/ScoutRFC/rfc9111.txt` (§1.2.2, §4, §4.2,
  §4.2.1, §4.2.4, §4.3.3, §5.2, §5.2.1.2–§5.2.1.4, §5.2.2.2, §5.2.2.4, §5.2.2.8, §5.2.2.10,
  §5.2.3).
- `awk` integrity check on my `hand-verdicts.tsv` → `lines=60 agree=60`, three columns each.
- ExecStale candidate existence checked after (1)+(2) were written: present (mtime 19:04),
  read in full (599 lines).

No mutating git/jj command was run in LANE or the fleet repo. No scratch directory was created
(nothing under /fast/scratch/hyaku/kake-r98/ReviewStale — nothing to clean). No tools were
installed. Report-path note: the item's `Report:` line names `w1/ReviewStale.md`; per the
round bound ("write ONLY inside w1/<YourSeatName>/") and the round-97 seat convention, this
report lives at `w1/ReviewStale/ReviewStale.md`.

## (1) Hand verdicts — `hand-verdicts.tsv`

60/60 `agree`. Distribution of grounds: ~40 directly RFC-derived (5861 §3/§3.1/§4/§4.1;
9111 §1.2.2, §4, §4.2, §4.2.1, §4.2.4, §4.3.3, §5.2, §5.2.1.4, §5.2.2.2, §5.2.2.4,
§5.2.2.8, §5.2.2.10, §5.2.3; 9110 list/quoted-string grammar via the contract's S478 ground);
~7 rest on the contract's three explicitly marked lane conventions (H18/H19 request-sie
precedence, H30–H32 quoted/non-digit absent, H53 qualified no-cache); ~11 on the contract's
own I/O interface, where the RFCs are silent by nature (H39–H43, H47–H51, H59).

Notable judgments:

- H05/H38 (age==lifetime is stale) follow from 9111 §4.2's formula
  `response_is_fresh = (freshness_lifetime > current_age)` — equality is stale.
- H07/H08 take the §4.1 example literally: usable "until the age is greater than 1800", so
  1800 inclusive, 1801 error-through. The contract's inclusive-boundary rule is correctly
  derived, not asserted.
- H37 (fresh-on-error → `fresh`) is grounded in 9111 §4's reuse list (fresh → reusable) plus
  §4.3.3: on a 5xx during validation the cache may "act as if the server failed to respond"
  and send a stored response subject to §4.2.4.
- H16 (SWR window does not cover an error) — agreed on the synthesis reading (5861 §1 "two
  independent" extensions; §4 governs error serving; 9111 §4.2.4 forbids stale generation
  absent permission), but see finding F1: the RFC text alone does not compel it.
- H21/H22 (must-revalidate beats both extensions) — 9111 §5.2.2.2: "in all circumstances, a
  cache MUST NOT ignore the must-revalidate directive", overriding 5861's MAY.

## (2) Contract review — `contract-review.md`

Four findings (full citations in contract-review.md):

- **F1 (medium)** — the SWR/SIE event split is an unmarked interpretation: 5861 §3's
  circumstance-free "MAY serve … up to the indicated number of seconds" admits an error-time
  reading; the contract (and the H16 tag "5861§3") present the separation as settled RFC text.
- **F2 (minor)** — request `no-cache` is implemented as a flat prohibition, though 9111 §5.2.1
  marks request directives advisory ("MAY implement") and §4's reuse list does not include it;
  unmarked, and asymmetric with the marked qualified-no-cache convention.
- **F3 (medium-minor)** — the omitted coupling: §4.2.1 makes s-maxage the first freshness
  match for a shared cache and §5.2.2.10 prohibits reuse of a *stale* response with s-maxage;
  the contract treats s-maxage as a presence-prohibition while taking `freshness_lifetime` as
  an opaque input, so `shared=true` with L < A < s-maxage blocks a response RFC considers
  fresh. No hand case hits it; the 240-case generator (independent s-maxage and L draws) does.
- **F4 (cosmetic)** — the clamp is stated as the plain §1.2.2 MUST, whose text conditions it on
  representability; unconditional clamp-to-2^31 is the conventional reading. No hand case
  distinguishes the readings.

Also recorded: rule 4's marked "lane convention" (quoted/non-digit → absent) is actually
RFC-derivable (5861 ABNF + 9111 §5.2.3 "MUST ignore unrecognized") — marked conservative, not
wrong; and RFC 9110 §5.6.2/§5.6.4 (S478) is cited by the contract but no 9110 body is retained
in-lane, so the six grammar-dependent hand verdicts rest on the contract's stated grammar
(flagged for the L1's source ledger, not a contract defect).

## (3) Candidate `w1/ExecStale/stale_extensions.py` vs contract

Present at review completion; read in full. **No contract contradiction found.** Traced:
interface (exit 0 + exactly `decision`/`staleness` + newline; exit 1 + empty stdout + stderr
beginning `invalid_input:`); input table (unknown keys, missing keys, bool/float/string type
violations on ages, negative ages, `error` conditionality incl. absent-or-null on request
events, `shared` boolean-or-absent, `request_cc` default `""`); parsing (comma split outside
quoted-strings, SP/HTAB strip, empty-element skip, 1*tchar names, token/quoted-string values
with exact qdtext `%x21/%x23-5B/%x5D-7E/%x80-FF` and quoted-pair `HTAB/SP/VCHAR/obs-text`
ranges, refusal on no-OWS violations / empty value / unterminated quote / text after closing
quote / >U+00FF / control chars, first occurrence wins, case-insensitive names); rule 4
convention (quoted/non-digit/bare-name SWR/SIE → absent, clamp at 2147483648 inclusive); rule
5 (request directives refused in `request_cc` — matching the counter oracle's field-limited
check; storage directives and unknown extensions ignored); decision order (not-an-error →
fresh → swr → request-first-sie fallback) with `staleness = max(0, A−L)` always reported. The
candidate's own selftest receipt (`selftest.txt`) says cases=113 passed=113; the scored counter
run remains the L1's. The candidate's docstring honestly labels the lane conventions,
including the F1/F2/F4 points as contract-stated — it implements the contract, not my findings
about the contract.

One ambiguity note (resolved correctly, no defect): contract rule 5 does not say request
directives are refused only in `request_cc`; the candidate (like the frozen oracle) refuses
them only there and ignores them in `response_cc`. Flagging so the L1 knows the contract
sentence is looser than the operative behavior.

## Verdict

REVIEW-STALE hand_agree=60/60 contract_findings=4
