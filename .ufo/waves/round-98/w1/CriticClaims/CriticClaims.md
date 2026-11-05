# CriticClaims — round 98 scoped findings

Full attacks, commands, output lines and rc values: `attacks.md` (this directory). Receipts are flat files here.

Note on location: the report trailer names `.ufo/waves/round-98/w1/CriticClaims.md`, which is outside this seat's directory. The seat bounds require writing only inside `w1/CriticClaims/`, so this report is written here. The L1 should copy it up if that path is wanted.

## C1 — calibration: falsified by the counter (5 escapes)

- F-C1-1: key word-prefix extension. `Coverage-index calibration counter with automatic CDN cache purge` backs the admitted `Coverage-index calibration counter` entry. `met=true` rc 0.
- F-C1-2: the same collision spelled with an escaped pipe. `met=true` rc 0.
- F-C1-3: an existing unrelated path (`SCORECARD.md`) satisfies the evidence check. `met=true` rc 0.
- F-C1-5: a phantom table in a second `Capability` table inside the same `## Capabilities` section is never read. `met=true` rc 0. The repair itself moved 5 rows into such a region.
- F-C1-6: an in-place evidence edit to a matched row is outside the review conjunct. `met=true` rc 0.
- Partial, not counted: F-C1-4, the round-cell tail `52 (not 25; …)` is not parsed.
- Coupling: F-C1-7, the frozen C2 row (round 98) makes C1 `mismatches=1 met=false` rc 1.
- Do-nothing and cheap controls reproduce: base `mismatches=46 met=false` rc 1; drop-the-unbacked-rows `mismatches=40 met=false` rc 1.
- Live: ReviewCapB has two `disagree` rows (56, 57); row 57's premise checks out at `4446ce21` (`grep -ci ambiguous` → 0). Under the kill rule this lands C1 unmet independent of the counter. ReviewCapA has no verdicts file yet.

## C2 — freshness: candidates pass the counter and violate the contract (7 escapes)

Each of these passes `hand=60/60 generated=240/240 met=true` on every seed tested (default, 1, 2, and for K6/K7/K8 seeds 1–10), and each deviates on a named contract input:
- K1 error 100/599 refused (contract: valid, `not-an-error`)
- K2 error `"500"` accepted (contract: refuse)
- K3 non-tchar byte `é` in a token accepted (contract: refuse)
- K4 `U+0100` inside a quoted-string accepted (contract: refuse)
- K5 clamp at 2^31 wrong (`revalidate` where contract says `serve-stale-revalidate`)
- K6 request duplicate uses the last occurrence (contract: first)
- K7 inclusive boundary broken only for error 504 + shared + staleness == E

The generated population agrees with these candidates on 480,000 of 480,000 cases across 2000 seeds for K1–K5 (blind), and fails K6 on 157/2000 seeds and K7 on 17/2000.

## Freeze predicate — 6 holes

- PH-1 Causal separability: the C2 row required by C2 flips C1 unmet at any revision that carries it. The ordering rule picks the repair revision, but the predicate sentence says "landed content revision".
- PH-2 Review conjunct covers only "adds, renames or moves", so in-place edits are unreviewed (F-C1-6).
- PH-3 Review conjunct is satisfied by one reviewer's agree and a silent second reviewer. Live: ReviewCapA has no verdicts file.
- PH-4 The C2 seed is sha256 of the scored commit id, so re-committing re-rolls the population (K6 fails about 7.9% of seeds).
- PH-5 Delegation: candidate K8 imports the counter's oracle from the lane path and meets the predicate with no capability (`met=true` on 11/11 seeds).
- PH-6 Population blindness: the grammar never draws error 100/599, string errors, non-ASCII bytes, clamp values above 2^31; request duplicates only by chance.

## Verdict

CRITIC c1_escapes=5 c2_escapes=7 predicate_holes=6
