# ReviewC2 — independent conformance review of the C2 instrument

VERDICT: C2 instrument conforms — 93/97 cases agree, 0 tool defects found; all 4 disagreements trace to three pre-flagged contract ambiguities (A2, A3, A4 below), not to candidate behaviour on any unambiguous clause.

- Reviewer: `ReviewC2` (leaf seat, no subagents). Method: computed from
  `.ufo/waves/round-92/c2-contract.md` (sha256 `5fc49c7af47ce4331563bf991e4199817eef8748621b02e05682a4f01f14c944`) alone.
  `c92_heuristic.py` and its hand cases were **not read**; the counter was not executed.
- Measured bytes: `scripts/heuristic_freshness.py` sha256
  `7bfe82da8e1a1d541930ef1b4ee64cfe9b3fa5b8169680795bcc8626d2f37f5c` (22985 B, mtime 2026-11-04 21:40:40 -03:00;
  landed 21:40:47, re-hashed unchanged at 21:41:22). Lane HEAD at review open: `f0b2dc63`; freeze `a5640ca0` is its parent.
- Case set: `cases.json` — **97 cases** (40 refusal, 57 decision), every clause 1–13 plus the Input block,
  every vocabulary member. Run: one `python3 -B scripts/heuristic_freshness.py` process per case (stdin/stdout),
  harness `run_cases.py`, raw per-case evidence `runs.jsonl`, summary `agreement.txt` — all beside this file.
- **Case count: 97. Disagreement count: 4** (R31, D44, D48, D49). Agreement 93/97.

## Protocol conformance (all 97 cases)

- Every success row: exit 0, empty stderr, stdout = one JSON object with exactly the three keys
  `decision`/`lifetime`/`heuristic`. 0 protocol violations.
- Every refusal row: exit 1, empty stdout, stderr starting `invalid_input:`. 18 distinct reason strings,
  all stable and clause-shaped (e.g. `empty Cache-Control directive`, `duplicate header name`,
  `s-maxage argument is not a bare non-negative decimal integer`). The contract leaves reason text free-form;
  the comparator asserts the prefix only. Reason strings are not pinned by anything frozen — a successor that
  rewords them stays conformant; a counter that pins exact strings would not be. Recorded as protocol debt, not a defect.

## Disagreements (each named: ambiguity clause or tool line)

All four fall inside ambiguity families I flagged **before** running (they are marked `note`/flagged in `cases.json`).
No case computed from an unambiguous clause disagreed, so no tool defect was found and no candidate line needs naming.

| Case | Input delta | Candidate | My contract-only expectation | Class |
|---|---|---|---|---|
| R31 (cl. 4) | `Cache-Control: s-maxage= 60`, shared | `explicit 60` | refusal — argument `" 60"` is not a **bare** decimal integer | ambiguity **A3** |
| D44 (cl. 4) | `Cache-Control: max-age = 60` + `Last-Modified` | `explicit 60` | `heuristic 10` — name split at `=` is `"max-age "` (never re-trimmed by clause 4), an unknown, ignored directive | ambiguity **A2** |
| D48 (cl. 6) | `Expires: -10`, `Date: 1000` | refusal `Expires is not a decimal integer` | `explicit -1010` — clauses 5–7 say "a decimal integer" with **no** "non-negative" (contrast clause 4's explicit "bare non-negative"), and clause 6 says Expires "may precede Date" | ambiguity **A4** |
| D49 (cl. 5/7) | `Date: -100`, `Last-Modified: -200` | refusal `Date is not a decimal integer` | `heuristic 10` — same A4 reading (interval 100) | ambiguity **A4** |

Candidate's resolved grammar (observed, consistent across both disagreements per family):
directive name and argument are trimmed after the `=` split (A2), the argument must match `^[0-9]+$` after trimming (A3),
and Date/Expires/Last-Modified are unsigned digit strings with leading zeros accepted (D57 agrees) and a sign refused (A4).
Each side of each family is a defensible reading; none is a malfunction. They must be pinned in the contract (v2) or by
the frozen counter's hand cases — see residual risk.

## Contract debt — every sentence a second implementer could read two ways

Re-read of the frozen contract after the run; these are the ambiguities, independent of who is right:

1. **A1 (cl. 10/11, s-maxage when not shared).** "`s-maxage` (only when `shared`)" — when not shared, is `s-maxage`
   (a) ignored entirely, so clause 11's "no explicit expiration is present" treats it as absent (my reading; candidate
   agrees: D03, D04, D47), or (b) present-but-inapplicable, which would leave a non-cacheable status with `s-maxage` in
   a decision gap clause 11 does not cover?
2. **A2 (cl. 4, name/argument split).** "each directive is trimmed of SP and HTAB; its name is lowercased" — is the name
   the raw pre-`=` substring (so `max-age ` ≠ `max-age`, D44 → ignored → heuristic path) or re-trimmed (D44 → `max-age`)? Disagreed.
3. **A3 (cl. 4, "bare").** "must be a bare non-negative decimal integer" — does `bare` reject interior/leading whitespace in
   the argument (`s-maxage= 60`, R31), or is the argument trimmed first? Disagreed.
4. **A4 (cl. 5/6/7, integer grammar).** "a decimal integer in epoch seconds" — no sign or leading-zero rule is given, and the
   deliberate contrast with clause 4's "non-negative" cuts both ways. Negative `Date`/`Expires`/`Last-Modified` (D48/D49),
   leading zeros (D57), a leading `+`: admitted or refused? Disagreed on the sign.
5. **A5 (Input, requiredness inside `stored`).** "exactly these keys" is stated for the top level only; the `stored` block's
   shape is shown but never given requiredness rules. Missing `status` (R13), missing `headers` (R14), an extra key inside
   `stored` (R40): refuse or tolerate? Candidate refuses all three (agrees with my reading); the text alone does not compel it.
6. **A6 (Input/cl. 3, JSON float vs int).** "`status` must be an int (not a bool)" — is `100.0` (a JSON number with integral
   value) an int (R15)? Candidate refuses; a lenient reader could accept.
7. **A7 (cl. 9, Vary member parsing).** "`Vary` present and one of its members is `*`" — member splitting, trimming and
   comparison are never defined (`Accept-Encoding, *`, D21). I read comma-split + SP/HTAB-trim + exact `*`; candidate agrees.
8. **A8 (cl. 9/11, presence with an argument).** "`no-store` in the stored Cache-Control; `private` in the stored
   Cache-Control" / "carries no `public` directive" — does `private="Set-Cookie"` (D41) count as `private` present?
   I read name-presence (argument ignored); the RFC's own field-list semantics differ, and the text is silent.
9. **A9 (cl. 4, duplicate-argument comparison).** "The same directive name twice with different arguments" — what is
   "the argument" for equality: byte-exact after trim (`max-age=10, max-age=10` OK, D14; `no-store, no-store` OK, D56)?
   Is `max-age=010` different from `max-age=10` (bytes) or equal (values)? Is a missing argument equal to an empty one?
10. **A10 (cl. 4, empty directive list).** `Cache-Control: ""` (R23) or whitespace-only (R22): literal split-on-comma yields an
    empty directive → refusal; an implementer may instead read an empty value as "no directives" → accepted. Candidate refuses.
11. **A11 (cl. 4, roleless-but-known directives).** "Unknown directive names are ignored" — `no-cache`, `must-revalidate`,
    `proxy-revalidate` are known in HTTP but have no role in clauses 9–13, and the contract never enumerates its operative
    vocabulary. Are they ignored like unknown ones (my reading, D13/D54) or handled otherwise?
12. **A12 (cl. 2, trim-before-parse).** "A value is trimmed ... and is otherwise byte-exact" — trimming must happen before the
    clause 5–7 integer parse for `" 1700000000 "` to be valid (D15); the sentence implies it but never says the parse consumes
    the trimmed value. An implementer who parses the raw value would refuse D15.
13. **A13 (cl. 4, quoted-string grammar).** "an optional `=` introduces a token or a quoted-string argument" — escapes inside
    quotes, unclosed quotes, and empty quoted strings are unspecified for non-delta-seconds arguments (`X-Goo="unclosed`).

Protocol debt (not an ambiguity): refusal `<reason>` text is free-form, so refusal agreement is only meaningful at
exit/stdout/prefix granularity.

## Coverage map (seat requirements → case ids)

- Cap boundary: D35 (exactly 86400), D36 (864010 → 86400), D37 (863990 → 86399), D51 (huge interval capped).
- Floor boundary: D32 (LM == Date → 0), D33 (interval 9 → 0), D46 (10 → 1), D38 (all-zero epoch).
- Last-Modified equal to Date: D32. Last-Modified after Date: D39.
- s-maxage shared vs not: D02/D43/D53/D10 (shared) vs D03/D04/D47 (not shared).
- Expires before Date: D07 (−100), D08 (zero), D06 (positive). private shared vs not: D18/D41 vs D19.
- Vary star vs members: D20/D21/D23/D45 vs D22/D55.
- Duplicate header name differing only in case: R32 (Date/date), R34 (with no-store).
- Signed delta-seconds: R26 (`max-age=+60`), R27 (`max-age=-1`), R30 (`s-maxage=-5`).
- Empty directive: R20 (trailing comma), R21 (comma-only), R22 (spaces), R23 (empty value).
- Malformed field refused while not storable: R33 (bad Expires + no-store), R34 (dup names + no-store), R35 (empty directive + private/shared).
- Vocabulary: explicit ×20, heuristic ×17, not-heuristically-cacheable ×5, heuristic-undecided ×7, not-storable ×8.
- Clauses: 1→R32/D42; 2→R16–R19/D15/D52; 3→R01–R09/R15; 4→R20–R31/D11–D14/D16/D44/D56; 5→R36/R37/D49/D57;
  6→R17/R39/D06–D08/D48; 7→R18/R38; 8→R33–R35; 9→D17–D23/D41/D45; 10→D01–D10/D42/D43; 11→D03/D24/D25/D30/D31/D54;
  12→D26/D32–D40/D46/D51; 13→D27–D29/D39/D47/D50/D55; Input→R10–R14/R40.

## Residual risk and verification gaps

- I did not read `c92_heuristic.py` or its hand cases (the seat's independence constraint), and did not run the counter.
  Whether the frozen 28 hand cases pin my side or the candidate's side of A2/A3/A4 is unknown to me; if they pin my side,
  the counter will disagree with the candidate on these four inputs and the wave must resolve the contract, not the candidate.
  If they are silent, the four disagreements remain pure contract debt for a v2.
- The candidate landed at 21:40:47 and its author seat may still be iterating; my measurement is bound to digest
  `7bfe82da…37f5c` (re-hashed unchanged at 21:41:22). The scorer should re-pin before counting.
- Refusal reasons are unpinned (above), so a byte-exact refusal-text comparison by any other instrument is out of contract scope.
- The 120-case generated population, the forgery subjects and the audit-hook sandbox are the frozen counter's conjuncts and
  were deliberately not exercised by this seat; my result says nothing about them.
- `now` is required but decision-irrelevant; only D38/D40 pin its irrelevance (any value ≥ 0 must not change the decision).
- No tool installs (none needed), no network GETs (none authorized for this seat), no git mutations in LANE
  (read-only `rev-parse`/`log`/`status`/`cat-file`/`sha256sum` only). Scratch root created and deleted empty.
