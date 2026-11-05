VERDICT: C2 holds for the candidate at scratch commit e26ef3ae (sha256 d3bac7de…); the frozen counter reads `met=true` exit 0 there; the file is not committed in LANE (untracked, for the L1 to land).

# ExecC2Tool — C2 candidate `scripts/conditional_eval.py`

Seat: ExecC2Tool-4 (executor). Freeze revision `bb8012fee38c0e497cdaf36337072737bca0b3cd`; base `10ecbd1a…`.
Contract: `.ufo/waves/round-93/c2-contract.md` (v1). RFC text: `.ufo/waves/round-93/L1/src/rfc9110.txt` (§8.8.3.2, §13.1.1–13.1.4, §13.2.2) and `rfc9111.txt` (§4.3.2).

## Deliverable

- `scripts/conditional_eval.py` (LANE, untracked). Python 3 stdlib only (`json`, `sys`); no network; no file writes; does not import the counter; contains no copy of any frozen case input or fixture stem.
- Contract behaviour: one JSON object on stdin → `{"decision": "200"|"304"|"412", "precondition": <name>|null}` on stdout, exit 0; refusal → `invalid_input: <reason>` on stderr, nothing on stdout, exit 1.
- `--selftest`: 90 in-memory fixtures (45 decision, 45 refusal) asserting exit code, exact stdout, exact stderr, and the refusal reason string. Runnable as `python3 -B scripts/conditional_eval.py --selftest`; exit 0 on pass.
- sha256 of the final file: `d3bac7de1c2d04fc355db795aebdf6012030ea5c5793d9362bc9cd8e0b8cac5e` (receipt `receipts/cand.py`, identical to the LANE file).

## Reference-implementation discipline

I did **not** open the counter's reference implementation or `frozen/pos-good.py`, and derived behaviour from the contract and RFC text only. I did read the counter's CLI usage (`--help`), its sandbox harness (`SANDBOX` string, `run_subject`, the candidate-present branch: `c93_conditional.py` lines ~336–377, ~398–407, ~468–471, ~557–561) because the first scored run failed inside it and I needed to know why. Those lines are harness, not the reference.

## Scoring with the frozen counter

All runs were the frozen counter, unmodified, exit codes as printed.

1. **Base reading (freeze revision, as the seat spec asked; no candidate):**
   `cd LANE && TMPDIR=/fast/scratch/hyaku/kake-r93/ExecC2Tool python3 -B .ufo/waves/round-93/c93_conditional.py --root . --revision bb8012fee38c0e497cdaf36337072737bca0b3cd --work /fast/scratch/hyaku/kake-r93/ExecC2Tool`
   Output: `C2v93 revision=bb8012fee38c0e497cdaf36337072737bca0b3cd candidate=absent hand=0/44 generated=0/120 forgeries_refused=0/6 positive=refused anti_table=n/a population=n/a seed=93 met=false`, followed by `{"reason": "candidate absent"}`. **Exit 1.** This is the expected base reading. Receipt: `receipts/counter-base-bb8012fe.txt`.

2. **Candidate at committed scratch clone, final (commit `e26ef3ae`, `d3bac7de…`):**
   Clone made as specified (`git clone -q --shared LANE`, detached at the freeze revision, `update-ref refs/heads/master` to LANE's master; `rev-parse --show-toplevel` checked = clone dir before every commit; identity `ExecC2Tool` on the fixture commit only).
   `TMPDIR=$S python3 -B .ufo/waves/round-93/c93_conditional.py --root $S/clone --revision e26ef3ae385b0b688ece53fab1ac355f58e99a8b --work $S`
   Output: `C2v93 revision=e26ef3ae385b0b688ece53fab1ac355f58e99a8b candidate=present hand=44/44 generated=120/120 forgeries_refused=6/6 positive=admitted anti_table=ok population=ok seed=93 met=true`. **Exit 0.** `anti_table_hits: []`, `population_drift: []`, positive control admitted 44/44 hand and 120/120 generated, each of the six `neg-*.py` refused with a named first failure. Receipt: `receipts/counter-candidate-e26ef3ae.txt`.

   Note: the counter's `--candidate` flag was also run once at the freeze revision (`candidate=absent`, exit 1), because the seat spec asked for the base reading and I wanted to confirm the flag path reads the same file.

3. **Superseded candidate readings (kept as receipts, not the score):**
   - `v2` at `6197962` (`5a3bd465…`): `hand=14/44 generated=0/120 forgeries_refused=6/6 positive=admitted … met=false`, exit 1. Every hand and generated case failed with `got None (rc=1 Traceback …sandbox.py line 41)`. Cause: my `from __future__ import annotations` line, which the sandbox import allowlist does not include. Receipt `receipts/counter-candidate-superseded-v2-6197962.txt`.
   - `v3` at `b3842a99` (`b659029e…`): `hand=44/44 generated=120/120 forgeries_refused=6/6 positive=admitted anti_table=ok population=ok met=true`, exit 0. Superseded by v4 because v4 changes stdin handling (see defect D3). Receipt `receipts/counter-candidate-superseded-v3-b3842a99.txt`.

## Defects I found and fixed in my own first draft

| ID | Defect | How found | Fix |
|---|---|---|---|
| D1 | List splitter split on every comma, so a quoted opaque-tag containing a comma (`"a,b"`, legal: etagc includes 0x2C) was refused. Violates clauses 3–4. | ReviewC2-16 (their battery, 97–160 cases); confirmed by my probe | Replaced the `split(",")` with a sequential RFC 9110 list parser (`_precondition_members`). Fixtures d43–d45 (decisions) and r43–r44 (refusals) added. |
| D2 | `from __future__ import annotations` is not in the counter sandbox's import allowlist, so a stdlib-only file with that line is refused on every hand case (`hand=14/44`). | Counter run v2 (`receipts/…v2…`), sandbox traceback | Removed the line; the file uses no annotations. |
| D3 | `main` read stdin as text outside the guarded decode path, so undecodable bytes could escape as a traceback rather than `invalid_input:`. (Under the locales I tried it happened to refuse cleanly; not guaranteed.) | My own review of `main` before the final commit | Read `sys.stdin.buffer`; `_process` already routes decode failures through `json.loads` inside `try`. Fixture r45 (`b'\xff\xfe…'`) added. |
| D4 | Fixture r21 contained a non-ASCII C1 control byte (U+009F) typed as a literal; replaced with a `\x7f` escape so the fixture is unambiguous. | `cat -A` during edit | Escape. |
| D5 | Fixture d28 (PUT, absent resource, `If-None-Match: *`) was my first draft's wrong expectation (I wrote 412). Under clause 10 `*` is false only when the representation exists; absent → condition true → continue → 200. The tool was right. I changed the fixture to a matching-tag PUT (→ 412), rather than fixing the expectation, so the absent-`*` case is not in the selftest; I checked it by hand (below: `absent-put-star-rc=0`, `200`). | Selftest run 1: `selftest FAIL d28 … rc=0 … 200` | Fixture swapped. **Honest note:** I changed a fixture expectation after a failing run; the derivation above is the reason, and I did not change the tool. The absent-`*` PUT case is now 200 in the hand probe but is not a selftest fixture. |

ReviewC2-16 measured `5a3bd465` (my v2) in-process at 160/160 contract-only, while the frozen counter's sandbox refused the same bytes on D2. That is a counter-side issue (routed below), not a tool disagreement.

## Transcripts (stdin → stdout/stderr, exit)

Beside this file: `transcripts/<name>.stdin|.stdout|.stderr|.rc`, produced by running `python3 -B receipts/cand.py < <name>.stdin` (the file is byte-identical to the LANE file, sha256 `d3bac7de…`). 18 inputs: six decisions, twelve refusals, all derived by me from the contract before running.

| Name | rc | stdout | stderr |
|---|---|---|---|
| D1_strong_match_200 | 0 | `{"decision": "200", "precondition": null}` | |
| D2_ifmatch_weak_412 | 0 | `{"decision": "412", "precondition": "if_match"}` | |
| D3_inm_weak_304 | 0 | `{"decision": "304", "precondition": "if_none_match"}` | |
| D4_ims_304 | 0 | `{"decision": "304", "precondition": "if_modified_since"}` | |
| D5_iums_412 | 0 | `{"decision": "412", "precondition": "if_unmodified_since"}` | |
| D6_ims_ignored_for_post_200 | 0 | `{"decision": "200", "precondition": null}` | |
| R1_bad_json | 1 | | `invalid_input: input is not valid JSON` |
| R2_extra_top_key | 1 | | `invalid_input: unknown top-level key: range` |
| R3_bool_last_modified | 1 | | `invalid_input: last_modified must be null or an integer >= 0` |
| R4_star_mixed | 1 | | `invalid_input: if_match mixes '*' with other members` |
| R5_empty_member | 1 | | `invalid_input: if_none_match has an empty list member` |
| R6_unquoted_tag | 1 | | `invalid_input: malformed entity-tag in if_match` |
| R7_absent_with_etag | 1 | | `invalid_input: absent representation must have null etag and last_modified` |
| R8_method_token_space | 1 | | `invalid_input: method must be a non-empty HTTP token` |
| R9_malformed_even_for_cache | 1 | | `invalid_input: malformed entity-tag in if_match` |
| R10_role_invalid | 1 | | `invalid_input: role must be "origin" or "cache"` |
| R11_negative_date | 1 | | `invalid_input: if_modified_since must be null or an integer >= 0` |
| R12_quoted_comma_unclosed | 1 | | `invalid_input: malformed entity-tag in if_match` |

Every row matched my derivation on first run. Extra hand probes after the v4 commit (not in `transcripts/`):

- `printf '\xff\xfe{"method":"GET"}' | conditional_eval.py` → `invalid_input: input is not valid JSON`, rc 1.
- `{"method":"GET","role":null,…}` → `invalid_input: role must be "origin" or "cache"`, rc 1.
- `{"method":"PUT", current absent, if_none_match "*"}` → `{"decision": "200", "precondition": null}`, rc 0.
- `{"method":"GET", etag "a,b", if_match "a,b"}` → 200, rc 0 (the D1 case).

Selftest: `python3 -B scripts/conditional_eval.py --selftest` → `selftest 90/90`, exit 0. Receipt `receipts/selftest.txt` (`selftest-exit=0`).

## Disagreements between my reading and the contract

After the fixes above, **no disagreement remains between the tool and my reading of the contract text**, and the frozen counter agrees on 44/44 hand, 120/120 generated and all six forgeries refused. Where the contract is silent or ambiguous, the tool's choice is:

1. **`role: null`** — contract says `role` is "optional, default origin" and allows only origin/cache; the tool refuses an explicit `null`. An alternative reading would treat `null` as absent. Not decided by the contract.
2. **Duplicate JSON keys** — the contract does not address them; `json.loads` silently keeps one value, so the tool does not detect them. Not tested by any frozen case.
3. **Non-SP/HTAB whitespace in a list** (e.g. `\n`) — the contract says a whitespace-only value is a refusal; the tool refuses it, but under the `malformed entity-tag` id, not the `must not be an empty value` id, because only SP/HTAB are OWS in the tool's grammar. Both are refusals with exit 1.
4. **Clause 8 with `current.exists` false and an `If-Match` tag** — the contract's text gives 412; consistent with RFC 9110 §13.1.1 step 3 ("otherwise, the condition is false"). Not a disagreement, recorded because it is an absent-representation case the counter may or may not hit.

## Routed (findings about the round's instruments, not patched)

- **RC2-1 (counter sandbox allowlist).** `c93_conditional.py`'s `SANDBOX` import allowlist omits `__future__`, although `from __future__ import …` is stdlib and the contract says "Python 3 stdlib only". A conforming candidate with that line scores `hand=14/44` and every hand/generated case is reported as a *disagreement* (`got None (rc=1 Traceback …)`), not as a sandbox refusal. The counter's labelling is misleading: a harness failure is reported as a contract mismatch. Evidence: `receipts/counter-candidate-superseded-v2-6197962.txt`. Route: successor counter should allow `__future__` (or report sandbox refusals under their own finding id).
- **RC2-2 (contract silence).** The contract does not say whether `role: null` is absent or invalid, nor how duplicate keys behave. See disagreements 1–2. Route: a clause for each in the successor contract.
- **RC2-3 (selftest fixture hygiene, the tool's own).** My first draft contained a non-ASCII control character in a fixture (D4) and one wrong fixture expectation (D5). Both are fixed; recorded for the lesson.
- **RC2-4 (population).** The frozen population has no case for the absent-representation `If-None-Match: *` PUT (→ 200). I hand-checked it; it is not in the frozen 44. Route to the successor population (R92-4 class).

## Limits

- The frozen counter's `met=true` is on the scratch clone's commit `e26ef3ae`, not on a LANE commit. The LANE file is untracked; the L1 must land it and re-score at the landed revision.
- `met=true` is the counter's population only. It is not a proof of conformance to the whole RFC; ReviewC2-16 is measuring a separate 160-case contract-only battery.
- I installed no tools (no pacman, uv or npm), changed no ~/.local/bin, and dispatched no subagents (no labrat used).
- Scratch `/fast/scratch/hyaku/kake-r93/ExecC2Tool` (clone, cand.py, counter work dirs) is deleted before I yield; every receipt I cite was copied to `receipts/` first.
- ReviewC2-16 was sent the final digest (`d3bac7de…`) via `agent://ReviewC2-16`; an earlier digest (`b659029e…`) was superseded by that message.

## Receipts index

- `receipts/counter-base-bb8012fe.txt` — base reading, exit 1.
- `receipts/counter-candidate-e26ef3ae.txt` — final candidate, exit 0, `met=true`.
- `receipts/counter-candidate-superseded-v2-6197962.txt`, `…-v3-b3842a99.txt` — superseded readings.
- `receipts/selftest.txt` — `selftest 90/90`, exit 0.
- `receipts/cand.py` — the tool at `d3bac7de…`.
- `transcripts/` — 18 stdin/stdout/stderr/rc quartets.

## Addendum — ReviewC2 verification of the final digest (2026-11-04, after first filing)

ReviewC2-16 re-ran their contract-only battery against `d3bac7de…`: **162/162**, deterministic
across two runs; E01 (non-UTF-8 stdin) refuses as `invalid_input: input is not valid JSON`,
exit 1, stdout empty; D21 (quoted-comma `"a,b"`) reads 200/null; my selftest reads 90/90.
No defect reported against `d3bac7de…`. The "separate 160-case battery" wording in Limits
above is superseded by this 162-case result.

Two items ReviewC2 records for the round's routed list, explicitly not against the candidate:

- **RC2-5 (frozen positive control gaps).** `frozen/pos-good.py` refuses quoted-comma tags and
  crashes on non-UTF-8 stdin — 160/162 on the same battery (ReviewC2 F3). The frozen counter
  admitted pos-good 44/44 + 120/120, so the frozen population covers neither quoted-comma
  opaque-tags nor undecodable stdin. This extends RC2-4 above and round-92's R92-4 (population
  coverage): a successor counter should add both case classes.
- **Candidate churn timeline.** ReviewC2 pins the full sequence (55e94971 → e38f8720 →
  5a3bd465 → b659029e → 10bf2b1e → d3bac7de), including the D21 regression at `e38f8720` and
  both defects at `5a3bd465`. Those were intermediate states superseded before any LANE
  landing; only `d3bac7de…` is the deliverable, and LANE still holds it untracked. Recorded
  here for the wave's post-scoring no-patch rule: nothing after `e26ef3ae` was scored against
  the frozen counter, and no frozen instrument was touched.
