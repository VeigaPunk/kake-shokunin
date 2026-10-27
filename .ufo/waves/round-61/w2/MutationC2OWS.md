# MutationC2OWS — OWS-trim / value-comparison mutation probe on scripts/header_audit.py (C2 xcto_nosniff_value class)

Seat: MutationC2OWS (w2 falsify, leaf, no subagent dispatch). Lane repo untouched
(`git status --porcelain` empty at `f5a9b8a`); all work in scratch clone
`/fast/scratch/hyaku/kake-r61/MutationC2OWS` (deleted on exit). Detector: the frozen
counter `.ufo/waves/round-61/c61_header_cases.py` driven via its hidden `--tool` override
(same 18 H-fixture gate, seed 61), so no lane jj/index/git mutation was needed.
Mutation point: `scripts/header_audit.py:333` (the single behavior-bearing line of the
xcto class):

    if name.lower() == "x-content-type-options" and value.strip(" \t").casefold() != "nosniff":

Tool before: `01abd8d4ff628907713b4300adf26b5962924d85132d1f330a33b70110c1d1d4`
(scoped copy `pristine.py` byte-identical, verified by sha256).
Environment note: R3 reports "ambiguous manifests" in the scratch clone because the
materialize step walks every `.json` under `.ufo/waves/round-61/`, including w1 seat
`.files` fixtures; this is identical for pristine and every mutant and does not affect
the H1–H18 killed/survived signal. Baseline is a valid control: pristine scores 18/18
H-cases (R3/R4 gate lines are the only non-pass).

## Mutants and verdicts (detector = c61_header_cases.py --seed 61)

| # | mutant (line 333 edit) | detector result | verdict | killed by |
|---|---|---|---|---|
| M1 | `nostrip` — drop `.strip(" \t")` | H6+H17 fail (16/18) | KILLED | trailing SP / trailing+leading HTAB fixtures |
| M2 | `nocasefold` — compare after strip only | H6 fails (17/18) | KILLED | `NOsniff` case variant |
| M3 | `stripall` — `value.strip()` (strips \n\r\f\v too) | 18/18 pass | SURVIVED | — |
| M4 | `spaceonly` — `strip(" ")` | H6[1] (`nosniff\t`) fails | KILLED | HTAB fixture |
| M5 | `tabonly` — `strip("\t")` | H6[0] (`NOsniff `) fails | KILLED | SP fixture |
| M6 | `equpper` — compare to `"NOSNIFF"` | H1/H5/H6/H17 fail (14/18) | KILLED | exact-value case fold |
| M7 | `startswith` — `not ....startswith("nosniff")` | H7[1] (`nosniff; preload`) passes clean | KILLED | suffix fixture (exactness) |
| M8 | `lower` — `.lower()` instead of `.casefold()` | 18/18 pass | SURVIVED | — |
| M9 | `internalcollapse` — `" ".join(value.strip(" \t").casefold().split())` | 18/18 pass | SURVIVED | — |
| M10 | `emptypasses` — empty/OWS-only value skips the check | 18/18 pass | SURVIVED | — |
| M11 | `namecasesens` — `name == "X-Content-Type-Options"` (no `.lower()`) | 18/18 pass | SURVIVED | — |
| M12 | `rstriponly` — `value.rstrip(" \t")` | H17 fails (17/18) | KILLED | leading-OWS fixture |

Killed 7/12, survived 5/12, none inconclusive (baseline was green).

## Survivor truthfulness (micro-probe, direct CLI on both pristine and mutant)

| survivor | probe input | pristine | mutant | divergence |
|---|---|---|---|---|
| M3 stripall | value `nosniff\x0c` (form feed, not OWS) | finding exit 1 | clean exit 0 | mutant accepts non-OWS control chars — trim set widened beyond SP/HTAB |
| M8 lower | value `no\u017fniff` (U+017F long s) | clean (casefold→s) | finding exit 1 | non-ASCII case folding untested; mutant is stricter, pristine more lenient — contract "folding case" reading unobserved either way |
| M9 internalcollapse | value `nosniff\x0b` (VT) | finding exit 1 | clean exit 0 | internal-whitespace collapse makes a padded value pass — contract requires "not exactly nosniff" → finding |
| M10 emptypasses | value `""` (empty) | finding exit 1 (`value=<empty>`) | clean exit 0 | empty value must be a finding per "not exactly nosniff"; the tool's own --selftest covers OWS-only but the frozen counter never does |
| M11 namecasesens | name `x-content-type-options` (lowercase), value `sniff` | finding exit 1 | clean exit 0 | header-name case-insensitivity of the XCTO match is never exercised with a non-canonical field name; every counter fixture uses the exact mixed-case name |

All five survivors change observable behavior — they are coverage findings, not no-op mutants.

## Proposed hardening cases (for a v2 counter or seat-owned probe pack; contract change only)

1. XCTO value padded with a non-OWS control char (`nosniff\x0c`, `nosniff\x0b`, `nosniff\r\n`) → must find (pins the trim set to SP/HTAB; kills M3, M9).
2. XCTO value empty `""` and OWS-only `" \t "` → must find (kills M10; the tool selftest already encodes this reading, the counter does not).
3. XCTO recorded under a lowercase/other-case field name with a bad value → must find (kills M11; H9 exercises case-insensitivity only for singleton declarations, not for the XCTO name match).
4. Non-ASCII case-fold probe (`no\u017fniff`) → declare the intended reading (casefold vs lower) explicitly, then assert it (resolves M8's ambiguity).
5. Internal-whitespace value (`nos niff`, `nosniff extra`) → must find (kills M9; H7's `nosniff; preload` covers suffix but not embedded whitespace).

Coverage summary: H5–H7/H17 kill every mutation to trimming of SP/HTAB, case-folding of ASCII, and exact-equality comparison — that contract core is well pinned. The surviving five mutants cluster on (a) the trim-set boundary beyond SP/HTAB, (b) empty values, (c) field-name case, (d) internal whitespace, (e) non-ASCII case folding — none of which any H1–H18 fixture reaches. A v2 need only add the five cases above; no predicate change required.

## Restoration evidence

No lane file was ever modified: the mutation surface was a scoped byte-copy
(`pristine.py`, sha256 `01abd8d4…d1d4` before and after, matching the committed blob at
HEAD `f5a9b8a`), each `mut-*.py` lived only in scratch, and the detector's `--tool`
override was the only injection path. Lane worktree `git status --porcelain` empty at
end of run; scratch clone and fixtures deleted on exit. No tools installed this seat.

VERDICT: 12 single-point mutants at header_audit.py:333 — 7 KILLED by H5/H6/H7/H17 (trim SP+HTAB, ASCII case-fold, exact-equality core is detection-pinned), 5 SURVIVED on coverage gaps (non-OWS trim set, empty value, field-name case, internal whitespace, non-ASCII folding); all survivors verified as true behavioral mutants; proposed 5 hardening cases, no predicate change.
