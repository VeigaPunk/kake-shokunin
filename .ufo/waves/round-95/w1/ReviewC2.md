# ReviewC2 — round-95 C2 independent contract read, fixture scoring and v2-diff review

Seat: ReviewC2 (reviewer, leaf member — no subagent dispatch). 2026-11-05.

Scope honoured: writes only under `.ufo/waves/round-95/w1/ReviewC2/` and scratch
`/fast/scratch/hyaku/kake-r95/ReviewC2/` (deleted before yield; receipts copied first).
Fixture repos in scratch, identity `reviewc2@example.invalid`, `rev-parse --show-toplevel`
asserted before the first commit. No mutating git/jj command touched any lane tree. No
tool installed (none needed; pacman untouched; no sysctl proposed).

## 0. Instrument digest verification

`sha256sum LANE/.ufo/waves/round-95/c95_conditional.py` →
`f09f84090fdda405992d7b51191be8838549e3df402b0898eb2ca00c4c3ff312` — matches the pin in
the seat prompt and `controls/instrument-sha256.txt`. Verified before any attack.

Side note for the L1 (Amendment A cross-check): the amendment is live at
`freeze.md` §144 and only retargets the C1 side (`c95_selfassess.py`
`04be4a7d…`, `frozen/c1-surfaces.json` `9eff04c5…`, both re-hashed by me and found
matching). The C2 digests are unchanged, as the amendment states.

## 1. Clause-wise reading of the frozen reference (`reference()` in c95_conditional.py)

Reference read in full (lines 128–233 of the frozen file) against the retained body
`{LANE}/.ufo/waves/round-94/w1/ScoutRFC/rfc9110.txt` (502 941 bytes, sha256
`21c1cdce…` per round-94 lesson) and against the contract text
`c2-contract-v2.md`. Decisions I verified byte-for-byte:

- **C1 (empty list members, S478).** `parse_list` splits on `","` (safe here: `etagc`
  members emerge from `parse_etag`, so an embedded comma can never reach this parse
  — see the deviation below), strips `" \t"` (exactly the OWS production of §5.6.3,
  line 1774 of the retained body), refuses a whitespace-only field value as
  "empty precondition field value" (contract: "not a list and stays refused" — agree),
  refuses `"*"` mixed with any member (agree), accepts `""`/`","`/`",   ,"` as the
  empty list (the RFC's own invalid-for-`1#element` examples at lines 1726–1730 are
  invalid *for the example production*; `#entity-tag` with `[ element ]` carries no
  mandatory member, and the contract explicitly decides "A list of only empty members
  decides as the empty list" — reference agrees with the contract). All-empty
  If-None-Match → 200, all-empty If-Match → 412 — both verified.
  Members like `"\x0c"` (form feed), `"\x0b"`, NBSP, CR, LF are refused: correct,
  OWS is SP/HTAB only. Tab-padded empty members (`"9", \t , "9"`) accepted: correct.
- **C2 (obs-text in etagc, S455).** `ETAGC = {0x21} ∪ 0x23–0x7E ∪ 0x80–0xFF` —
  matches `etagc = %x21 / %x23-7E / obs-text` at line 1787 of the retained body and
  `obs-text = %x80-FF` at line 1589. Probes: 0x80 and 0xFF accepted in opaque and in
  list members; DEL (0x7F), CR, LF, NUL, HTAB, US-control refused; `w/"a"` lowercase
  weak prefix refused (`weak = %s"W/"` is case-sensitive); `""` empty opaque matches
  (`opaque-tag = DQUOTE *etagc DQUOTE` allows zero chars, example `ETag: ""` at the
  body's line for the empty example). The trailing RFC note ("servers ought to avoid
  backslash") does not require refusal — backslash (0x5C) is inside etagc;
  reference accepts and compares bytewise (`"a\\b"` ≠ `"ab"`, verified). Agree.
- **C3 (role null means origin).** `role = inp.get("role", "origin")`; explicit
  `None` → `"origin"`; missing key → origin; `role` of any non-`origin`/`cache`
  value (0, dict, list, `False`, `" cache"`) refused; extra top-level key refused.
  Agree with the contract clause ("The key remains optional").
- **C4 (raw duplicate keys refused).** The reference itself has no raw-byte path —
  `_no_duplicate_keys` exists in the reference module and mirrors the contract
  clause (`invalid_input:` refusal "before any decision"), but the raw cases reach
  the *subject*, not the reference (`reference_selfcheck` skips `__raw__` cases; the
  two `refuse/duplicate-*` cases pin refusal by subject behaviour, rc != 0). This
  asymmetry is a design note, not a defect: the clause is enforced one-sidedly
  because the counter's reference never sees bytes. Verified equivalence of the
  enforcement: my re-implementation of the hook over the two frozen raw payloads
  refuses at parse; a last-wins parser survives neither case (top-level dup flips
  method GET→HEAD, so a deciding subject is killed by the refusal expectation).
- **C5 (method-filter edges).** Reference: If-None-Match match under OPTIONS →
  412 (verified, plus PATCH/DELETE/POST/TRACE/CONNECT → 412; GET/HEAD → 304);
  If-Modified-Since under OPTIONS ignored → 200 (verified, including a
  date-passing IMS). Both edges agree with the contract's pinned cases.

### Reference-vs-contract divergences found (none within the frozen population)

| # | Where the reference decides differently | Case input | Reference | Contract/RFC exact reading |
|---|---|---|---|---|
| R1 | Comma inside an opaque-tag in a list member. `parse_list` splits the field on `","` before `parse_etag`, so `'"a,b"'` dies as "malformed entity-tag" while `etagc = %x21 / %x23-7E / obs-text` includes 0x2C and the RFC list grammar recognises member boundaries before commas. | `{"method":"PUT", current exists etag '"a,b"' lm 500, request if_match '"a,b"'}` | refused (`malformed entity-tag`) | RFC-exact: accepted, If-Match matches, 200. The v2 candidate implements the sequential grammar and accepts (verified; `grid/opaque-comma-probe.txt`) — so the candidate is *more* RFC-exact than the reference here. **Unobservable by the frozen population**: no hand case and no generated input (tag pool `'"a"' 'W/"a"' '"b"' 'W/"b"' '"c"' '"a\x80"', join-only separators) contains a comma-bearing opaque tag — both re-derived counts are 0. ExecC2V2 disclosed the same divergence (`selftest-notes.md` §Known reading divergence). |
| R2 | If-Unmodified-Since under OPTIONS: reference evaluates it (412 on failure). RFC §13.2.1 (line 6203–6207) says a server MUST ignore all conditional fields for methods that "do not involve the selection or modification of a selected representation, such as CONNECT, OPTIONS, or TRACE". | `{"method":"OPTIONS", current exists lm 500, request ius 400}` | 412 `if_unmodified_since` | The RFC text → ignore → 200. The contract's C5 pins only the two INM/IMS edge cases and does not decide IU-S-under-OPTIONS; the reference therefore follows no stated clause here. Unpinned by the frozen population too: generated coverage has IM-under-OPTIONS (10 cases) and IU-S-under-OPTIONS (4 cases) — and those agree with the reference because generated expectations ARE the reference — but no *independent* contract text decides them. |

Both divergences are recorded for the L1; neither is exploitable inside the frozen
population, and neither changes the frozen `met` predicate. R2 is a candidate
contract-deviation risk for a future contract revision that may decide it.

## 2. Independent 30-case agreement grid

Built from my own reading of `c2-contract-v2.md` (clauses C1–C5 + the contract's
lane-convention language), NOT from the counter's hand cases. Every case's
expectation was written before running the reference. The full grid is
`ReviewC2/grid.json` (per-case records) and `ReviewC2/independent-30.txt`
(the decision transcript). Highlights of the clause faces covered: If-Match
strong comparison matrix (weak-member, weak-current), INM weak+star both
representation states, empty members middle/leading/trailing/all-empty for both
tag fields, whitespace-only refusal, `*`-mixed refusal, obs-text accept/strong/weak
and control-char refusal, role-null default, OPTIONS edges (INM 412, IMS ignored)
and two unpinned dates edges (IU-S digit boundaries), date-value type refusals.
All 30 cases were decided by the reference independently of the frozen 66-case set
(8 of the 30 are not present in the frozen set in the same shape, e.g. case 3
weak-current If-Match, case 16 IU-S-under-OPTIONS, case 20 role-null-412).

**Verdict: agreement 30/30.**

Receipt: `ReviewC2/grid.json` — `agreement_count: 30`, `case_count: 30`.

## 3. Frozen fixture scoring (`c95_conditional.py --selftest`, read-only import)

Command (observer, `TMPDIR` pointed at my scratch, no lane writes):

```
TMPDIR=/fast/scratch/hyaku/kake-r95/ReviewC2 python3 -B \
  .ufo/waves/round-95/c95_conditional.py --selftest
```

Observed rc=0, line: `selftest 8/8 fixtures scored as declared; drifted-reference
cases=5; M11 killed=True` (receipt `ReviewC2/selftest.out`; identical text in the lane's
committed `controls/ctl-c2-selftest.txt` line 1). firmware reading: the positive
`pos-good-v2.py` is admitted, each of the seven forgeries including
`neg-refuse-empty-member.py` (hand 61/66, first failure
`inm/empty-member-middle-ignored … rc=1 invalid_input: empty list member`) is refused.
The `drifted-reference cases=5` count independently re-derived by me: exactly the five
weak/strong-comparison-sensitive cases distinguish the comparison-swapped reference
(`ReviewC2/forge-c2-selftest.txt`).

Fixture-level probes (under the counter's own SANDBOX harness, in scratch):
- The seven neg subjects each refuse under the sandbox; `neg-oracle-import.py` and
  `neg-pin-reader.py` refuse by import/scope hook (PermissionError,
  `import denied: c93_conditional` / pin-reader path outside the tree) —
  refusal-by-behaviour, not by crash to be read as anything but hostile
  (`ReviewC2/forge-neg-fixtures.txt`, `forge-oracle-detail.txt`).
- Renamed, nonce-altered copies flip nothing: renamed positive scores 304 on the
  empty-member case; renamed negative refuses. The class of counter the lane runs
  hashes pins, not names (round-90 renamed-copies rule stands).
- The `--skip-battery`-style route is closed for C2: the frozen CLI has no such
  flag (`argparse` rc=2), and selftest-extras like `--generated 0 --seed 1` change
  nothing in selftest mode (fresh 8/8 run) — `ReviewC2/selftest-attacks.txt`.
- Do-nothing base re-run in a scratch fixture git (my own fixture repo, base
  revision `480ac589`): rc=1 with `candidate=present hand=21/66 generated=0/120
  forgeries_refused=7/7 positive=admitted mutants=40/40 … met=false` —
  matches the lane's committed `controls/base-c2.txt` reading shape (revision named
  at the commit, reading is a by-design do-nothing control, not a verdict about
  round work) — receipt `ReviewC2/base-control-replay.out`.

## 4. ExecC2V2's delivered diff review

Patch `w1/ExecC2V2/conditional_eval-v2.diff` (10 456 bytes):
- Applies cleanly to the v1 blob (`git apply --check` rc=0 against
  `git show fdd5fdbe:scripts/conditional_eval.py` in scratch; resulting blob
  sha256 `9cff0c34128477dbe98e1449e074206e80b0985d223de720e1453fcc6b608848`,
  matching the executor's claimed candidate sha — verified by me).
- The tool's selftest re-run by me on the patched blob in scratch:
  `python3 -B scripts/conditional_eval.py --selftest` → `selftest 99/99`, rc=0.
- Scope check: the diff touches exactly the five clause surfaces and nothing else —
  `_entity_tag` obs-text (C2), `_precondition_members` empty-member acceptance with
  `saw_empty` (C1), role-null fold-to-origin (C3), `_no_duplicate_keys` +
  `object_pairs_hook` (C4), and comment/selftest text for C5 (no code change —
  correctly, since v1 already gated GET/HEAD). Two v1 refusal cases flip to
  acceptance (r06, r29) with the flip recorded, plus r42's reason-string change
  (`has an empty list member` → `mixes '*' with other members`); those are the only
  refusals-message changes. No clause beyond C1–C5 is implemented.
  One residual deviation, already disclosed by the executor and independently
  confirmed by me: an opaque-tag containing a comma inside a list member is
  accepted by the candidate (sequential parser) but refused by the frozen
  reference (`parse_list` comma-split) — see divergence R1; no frozen case
  observes it (`grid/opaque-comma-probe.txt`).
- Selftest additions are real assertions (every new `v2c*` row is a
  decision-or-refusal pair checked with the same equality test as the rest of the
  matrix; `selftest 99/99` fails on any drift — the r42 sequence in the executor's
  own notes shows the assertions do fire when violated).
- C5 semantics of the delivered blob re-checked directly through `_process`:
  ws-only refused, `*, ` refusal (star+empty), INM-star under OPTIONS → 412,
  role-null under IMS-cache → 304 (same as reference), duplicate nested key
  refused, many-empties accepted (receipts `forge-cand-*`, `c4-order-check.txt`,
  `c5-ims-options.txt`, and the consolidated edge matrix
  `candidate-vs-reference.txt`).

## 5. Deliverables and receipts

`w1/ReviewC2/` (flat): `grid.json` (the 30-case grid record),
`independent-30.txt`, `selftest.out`, `base-control-replay.out`,
`frozen-hand-cases.json` (hex-safe dump of the counter's 66 frozen cases for the
L1), and 44 probe receipts named `forge-*`/`c3-*`/`c4-*`/`c5-*`/`candidate-vs-reference*`
/`gen-population-coverage.txt`/`m11-equivalence-replay.txt`/`m11-semantics.txt`
/`opaque-comma-probe.txt`.

Independent M11 re-check (supplementing the frozen `mutant-scan-v2` reading):
M11's find-string occurs exactly once in the round-93 pos-good bytes; the mutant's
`stamp or 0` change is behaviourally inert for every admissible input (`stamp is
None` only when `last_modified` is None, where base already skips the check, and
`(0 > ius)` is False for every legal `ius >= 0`); my 108-input differential in the
counter's sandbox gives 0 differences (`m11-equivalence-replay.txt`), so the
free-of-receipt empty `c2-equiv-receipts.json` with kill target 40/40 remains sound.

## Verdict

C2-REVIEW agreement=30/30 reference-defects=R1(comma-in-opaque-tag:reference
over-refuses, RFC-exact candidate, unobservable in frozen population),
R2(IU-S-under-OPTIONS evaluates 412 vs RFC-§13.2.1 ignore reading — unpinned by
contract C5, unobservable in frozen population)
