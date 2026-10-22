# ReviewDeclarationText — Round 30 wave 1

Seat: declaration text vs counters. Scope: SCORECARD.md:676-727 ("Round 30 — declared
claims") against `.ufo/waves/round-30/c1_reason_count.py` (548 ln) and `c2_quote_truth.py`
(124 ln), their docstrings, both before-receipts, `fetch_sources.py`, `sources/receipts.json`.
Leaf seat; no lsp server in this toolset — direct reads plus hashing; grep is not semantic proof.

## Result in one line

Every hard claim (counts, digests, exit codes, pass conditions) is implemented by the
counters; six statements are weaker than the code — omissions of conditions the code
additionally enforces. No contradiction found.

## Verified matches (evidence)

- Table counting commands (SCORECARD:689,690) match both usage lines (c1:53-54,
  c2:26-27, both `--root . --revision <commit>`).
- "0/14 (R01-R08 0/8, F01-F06 0/6)" (SCORECARD:689): receipt c1-before-0356681.json
  passed 0 / total 14 / rPassed 0 / fPassed 0.
- "14 checks" and R-code list+order (SCORECARD:692-695) == `R_CODES` (c1:77-86);
  R01-R08 + F01-F06 built in `grade()` (c1:454-464), 14 total.
- Three-part pass condition, behaviour/fixture/compared (SCORECARD:695-700): `coded()`
  (c1:445-452); fixture scan of exported `scripts/fixtures/citing-set/*/expected.json`
  (c1:391-404); compared = runner exit 0 at baseline, non-zero with `"<code>"`→
  `"<code>_mutated"` in the gate (c1:417-431, 448-449). "At base the behaviour holds
  and the other two parts fail" (SCORECARD:700-701): receipt R01-R08 behaviour true,
  fixture false, compared false (receipt lines 68-306).
- "with the 3 controls holding" (SCORECARD:689): K1-K3 all passed in receipt (lines
  30-63); broken control exits 2 before the pass verdict (c1:542-544).
- "both constant gates below 14" (SCORECARD:689) == `s["passed"] < len(checks)`
  (c1:525); receipt: constantClean 0, refuseEverything 0 → "0/14, 0/14" (SCORECARD:713).
- R/F exit shapes: refused = exit 2 / could-not-evaluate / (input_invalid, code)
  (c1:199-200); F01 two dup cases (c1:266-274); F02 NaN/Infinity/-Infinity (c1:277-286);
  F03 S01+S02 and S1 (c1:289-301).
- Base digests (SCORECARD:713-714) recomputed: counter be2a1287…c53e == sha256 of the
  live counter file (receipt ties it to these exact counter bytes); gate d7e79ba1…9d48
  == sha256(`git show 0356681:scripts/citing_set.py`); runner 3c167895…2a1c ==
  sha256(base `scripts/citing_set_selftest.py`). All three match the receipt.
- C2 per-id conditions (SCORECARD:717-721): mined + opened 2026-10-22 (c2:103-104);
  cites below 8-line header == `splitlines()[8:]` (c2:94); quote 1-25 words (c2:106-109);
  quote substring of retained text whose sha256 equals receipts.json textSha256
  (c2:110-114). "Names its own sha256" (SCORECARD:716) == counterSha256 (c2:120-121).
  Round-29 origin exists (`.ufo/waves/round-29/c1_quote_truth.py`).
- "Opened 2026-10-22T11:49Z, one GET each" (SCORECARD:721-722): receipts show
  accessedUtc 11:49:44Z-11:49:45Z, status 200 x4; "each receipt names the fetcher
  sha256" (SCORECARD:723): fetcherSha256 in all four (fetch_sources.py:56).
- C2 base evidence 0/4 (SCORECARD:724): receipt passed 0 / total 4, all sub-checks false.

## Findings (all minor; text weaker than code, with line numbers)

1. [minor] F04: text says only "refused with exit 64" (SCORECARD:707-708); the counter
   additionally requires stdout to be one JSON object (c1:318-319; docstring c1:36
   "exit 64 with one JSON object on stdout"). A gate exiting 64 silently would pass the
   text's wording and fail the code.
2. [minor] F05: text "(exit 1, one `unadjudicated_citing_pair`)" (SCORECARD:708-709)
   omits verdict `failed`, which the judge requires (c1:332-333; docstring c1:38). The
   "without a traceback" half is real (judge flags stderr Traceback, c1:206-207).
3. [minor] F06: text omits the expected finding (input_invalid,
   document_not_regular_file) that the pty case requires (c1:371-372); it states only
   "refused without becoming the controlling terminal" (SCORECARD:709-711); tty_nr==0
   is enforced at c1:367-368.
4. [minor] C2 registry condition: text "registry row is `mined` and opened
   2026-10-22" (SCORECARD:717-718) omits that the counter also requires the receipt's
   URL to appear in the row's source cell, plus >=11 cells (c2:103-104).
5. [minor] C2 Gate quote: text "one quote of at most 25 words" (SCORECARD:718-719)
   omits the required line shape `- <id> — ` (exactly one such line) and exactly one
   curly-quoted span on it (c2:106-108).
6. [minor] C2 self-break control is unstated: for every passing id a one-letter mutated
   quote must NOT match the retained text, else controlBroken and exit 1 (c2:116-117,
   123; flip_letter c2:64-69). The text (SCORECARD:716-721) never mentions this check.

No finding contradicts the code; each is a condition the code enforces that the
declaration text does not state. Severity rationale: none weakens the declared 14/14
or 4/4 barriers; they only under-describe what "pass" means.

## Residual risk (contract vs counter, outside SCORECARD text)

- Duplicate-key refusal is exercised at two depths only (population top level, ledger
  pair object; c1:266-274) while the interface contract says "at any depth"; the
  counter cannot catch a gate that refuses only those two depths.
- F04 repeats are space-separated only; the contract's `--name=value` repeat form is
  not exercised by any counter case.
- SCORECARD:678 "pushed lane tip at round start" not independently checked (no vc
  history inspection in this seat); 0356681 resolves and is the receipt revision.

## Commands run (all exit 0)

- `git clone -q <lane> /fast/scratch/hyaku/kake-r30/w1/ReviewDeclarationText/clone`
- `sha256sum .ufo/waves/round-30/{c1_reason_count,c2_quote_truth}.py`
- `git -C clone show 0356681…:scripts/citing_set{,_selftest}.py | sha256sum`;
  `git -C clone rev-parse 0356681…^{commit}`
- reads/greps: SCORECARD.md:675-745, both counters, both before-receipts,
  fetch_sources.py, sources/receipts.json.

Not verified: neither counter executed (receipt numbers accepted via the byte-level
digest tie above; running them belongs to ReviewC1Before/ReviewC2Before). No installs;
pacman untouched.

Report: .ufo/waves/round-30/w1/ReviewDeclarationText.md
