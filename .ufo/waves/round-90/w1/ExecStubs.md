VERDICT: C2 as frozen (57/57 on the pinned population) is not contradicted, but the gate is falsified as a conformance gate: 14 of 23 new single-clause non-conforming stubs are FALSE ADMITS (met=true, exit 0, on all 3 seeds).

Seat ExecStubs, round 90 wave 1. Lane HEAD `79e1aac24654e01dc0559eb3beb8abbe61ec73a8`. Gate `scripts/cache_key_conformance.py` sha256 `2840f32e53317327fbaa6df3f8e02da06363e0fcda829270651a356192517591` (also in the `gate-runs.txt` header, along with the `scripts/cache_key.py` sha256 `3a658326…`, which matches the population pin, and python 3.14.8).

## Receipts (all in /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/w1/ExecStubs/)
- `stubs/S01…S23-*.py`: 23 stubs. Each is a copy of `scripts/cache_key.py` with one localized edit, and its docstring names the clause it breaks and a minimal input.
- `stubs.sha256`: pins for all 23 stubs. None of these hashes appears in `frozen/c2-population.sha256` (checked by substring match against the file).
- `gate-runs.txt`: the full `--verbose` stdout and exit code for 72 runs: 24 subjects × seeds 1, 90 and 20261104.
  Command: `python3 -B scripts/cache_key_conformance.py --candidate <subject> --work <scratch> --seed <s> --verbose`, run with cwd and TMPDIR set to the scratch directory.
- `exposures.txt`: for each stub, the minimal input, the gate's own `reference()` output, the stub's direct run output (rc/stdout/stderr), and the gate's own `judge()` verdict for the stub and for the shipped positive. It also holds three contract/gate probes on the shipped `cache_key.py` (below).

## Table: stub → clause violated → gate verdict (seeds 1 / 90 / 20261104)

| stub | clause violated (one) | gate | minimal exposing input → reference vs stub |
|---|---|---|---|
| S01-member-split-semicolon | members: split on `,` only; `;` not tchar | **FALSE ADMIT** met=true ×3 | `{"uri":"u","request_headers":{},"vary":"a;b"}` → REFUSE vs key `u␟a␞␜␟b␞␜` |
| S02-member-trim-one-leading | members: trim all leading SP/HTAB | **FALSE ADMIT** ×3 | `"vary":"  a"` → `u␟a␞␜` vs refusal |
| S03-member-sort-hyphen-high | members: sort lowercased names in code-point order | **FALSE ADMIT** ×3 | `"vary":"a-b, aa"` → a-b before aa vs aa before a-b |
| S04-member-token-after-lower | members: token check (lowercase is ASCII-only) | **FALSE ADMIT** ×3 | `"vary":"\u212a"` (KELVIN SIGN) → REFUSE vs key with member `k` |
| S05-name-token-isalnum | names/refusals: header name must be a token | **FALSE ADMIT** ×3 | `"request_headers":{"\u00e9":"1"}` → REFUSE vs key `u` |
| S06-name-token-skipped-unnominated | names/refusals: every header name must be a token | **FALSE ADMIT** ×3 | `{"a b":"1"}`, `"vary":"x"` → REFUSE vs key |
| S07-value-nonascii-lowered | values: no case folding | **FALSE ADMIT** ×3 | `{"a":"\u00c9"}`, vary a → `É` vs `é` |
| S08-value-nfc | values: byte-exact | **FALSE ADMIT** ×3 | `{"a":"e\u0301"}` → `e◌́` vs NFC `é` |
| S09-value-nul-refused | refusals: value refused only for CR/LF | **FALSE ADMIT** ×3 (advisory 2/3, unscored) | `{"a":"x\u0000y"}` → key `…x\x00y` vs refusal |
| S10-uri-lowercased | layout: key = ESC(uri), URI verbatim | **FALSE ADMIT** ×3 | `"uri":"https://E.test/A"` → `https://E.test/A` vs `https://e.test/a` |
| S11-uri-space-escaped | escaping: only `%` + 4 separators | **FALSE ADMIT** ×3 | `"uri":"u v"` → `u v` vs `u%20v` |
| S12-uri-stripped (`str.strip()`) | layout: URI not trimmed | refused ×3 (hand 68/70, gen 93–103/120) | caught only because `str.strip()` also strips U+001C–U+001F |
| S23-uri-strip-ows (`strip(" \t")`) | layout: URI not trimmed | **FALSE ADMIT** ×3 | `"uri":" u "` → `" u "` vs `"u"` |
| S13-output-duplicate-key-member | output: `{"key": <string>}` | **FALSE ADMIT** ×3; the gate's `judge()` also passes it on the minimal input | stdout `{"key": "u", "key": "u␟a␞1"}`. A first-wins consumer reads the bare URI. |
| S14-output-raw-utf8-surrogate-crash | output: a valid string uri yields a key, exit 0 | **FALSE ADMIT** ×3 | `"uri":"\ud800"` → key `\ud800` vs traceback `UnicodeEncodeError`, rc 1, no `invalid_input:` |
| S15-empty-as-absent-multi | layout: present-empty contributes "" | refused ×3 (generated only: 117/114/119 of 120; hand 70/70) | `{"a":"","b":"1"}`, vary a,b |
| S16-member-sort-length-first | members: sort order | refused ×3 (generated only: 85/90/102) | `"vary":"accept, q"` |
| S17-refusal-exit-2 | output: refusal exits 1 | refused ×3 | |
| S18-refusal-to-stdout | output: refusal on stderr | refused ×3 | |
| S19-dup-header-equal-values-ok | names: case-variant duplicate refused | refused ×3 (hand `dup-header-unnominated`) | |
| S20-member-trim-sp-only | members: trim HTAB too | refused ×3 | |
| S21-output-trailing-space-in-key | layout: exact key | refused ×3 | |
| S22-escape-1D-lowercase-hex | escaping: `%1D` uppercase | refused ×3 | |
| POSITIVE scripts/cache_key.py | — | admitted met=true ×3 (clauses 6/6, hand 70/70, gen 120/120, sandbox ok) | |

All 14 false admits score `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok met=true` with exit 0 on every seed (`gate-runs.txt`). For every one of them, `exposures.txt` shows the gate's own `judge(stub, reference(input))` returns False on the minimal input, except S13, where `judge` itself returns True. The shipped positive is judged correct on all 23 minimal inputs.

## Defects found (gate, contract, shipped positive)

1. **Hand-case coverage gap (G1).** Coverage stops at the population's mutation sites. The generated cases cannot reach the gaps either: `NAME_POOL` holds only ASCII tokens, `VAL_ALPHA` has no uppercase non-ASCII and no combining marks, URIs come from `{p,%,US,GS,2,/}` with a fixed lowercase prefix, member separators are always `,`, and the OWS prefix is at most one character. Specific gaps:
   - header names: only `"a b"` and `""` are tested;
   - URIs: always lowercase, never space or SP/HTAB at the edges;
   - values: never uppercase non-ASCII, never decomposed Unicode;
   - Vary: no `;`, no double leading OWS, no non-ASCII that lowercases to ASCII, no `-` against a letter at the same position.

   This is why S01–S08, S10, S11 and S23 pass.
2. **`judge()` output check (G2).** `judge()` accepts duplicate JSON members (`json.loads`, last wins). S13 emits two `key` members and passes. A fix is `object_pairs_hook` rejecting repeats.
3. **NUL refusal unscored (G3).** The `nul-in-value` case sits only in the unscored advisory population. The contract's refusal list does not contain NUL, and its value clause says "byte-exact", so under the contract as written a NUL value must be keyed. The gate therefore admits a stub that adds an off-contract refusal (S09). The gate's docstring frames this as "the contract does not decide"; in my reading the contract does decide it (key) and RFC 9110 §5.5 disagrees. That is a contract gap the gate should route, not leave unscored.
4. **Contract worked example 5 is unsatisfiable by the shipped positive as written.**
   - The contract says the example-5 JSON "carries them raw". `scripts/cache_key.py` refuses the raw-byte form with `invalid_input: input is not valid JSON`, rc 1 (receipt in `exposures.txt`), because Python's strict `json` rejects raw controls.
   - The gate avoids this by sending example 5 JSON-escaped (`WORKED` comment) and by treating raw-control refusal as the *advisory-correct* outcome.
   - So the contract text and the RFC 8259 advisory contradict each other, and the gate silently picks RFC 8259.
5. **utf8-required advisory fails on the positive.** The shipped positive fails it under the gate's env (`LC_ALL=C.UTF-8`): stdin decodes with surrogateescape, so `{"uri":"\xff",…}` → rc 0, key `"\udcff"`. The `UnicodeDecodeError` branch in `cache_key.py main()` is dead code under this env. Advisory only; it is not scored.
6. **Exact-duplicate JSON header keys are never tested.** The contract refuses "two header names equal case-insensitively", but `{"a":"1","a":"2"}` is keyed last-wins by both the shipped positive (`u␟a␞2`) and the gate reference. `json.loads` collapses the keys, so the refusal clause is invisible to the reference. No case covers it.
7. **Scope.** None of this breaks C2's frozen predicate: it counts only the 57 pinned subjects plus the 4 positives. What it shows is that "refuses the non-conforming population" generalizes poorly: 14/23 ≈ 61% of fresh single-clause violators pass. The C2 claim should not be read as "admit ⇒ conforming".

## Limits
- I did not run `c90_gate.py`, C1 or the population counter; that is out of seat scope.
- The stubs were executed directly for the exposures and inside the gate's sandbox for the verdicts.
- The S04 and S06 mutations are deliberately contrived; S01–S03, S05, S07–S11, S13, S14 and S23 are plausible implementation errors.
- Three seeds only. Generated-case counts for S15 and S16 show the refusals depend on chance within 120 cases.

## Tooling
No installs. No network. Scratch `/fast/scratch/hyaku/kake-r90/ExecStubs/` was created, used as `--work`/TMPDIR, and deleted before yield. No clone, no git mutation, no labrat.
