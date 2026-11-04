# Round 86 frozen contract — kake

Base: `376ac5dcdf86457ef1f8dd490dada735dad81f68`. Freeze occurs before ready-file
dispatch. Two causally separable claims; neither claims the whole D84 queue closed.
This contract, both counters and every pre-dispatch control are committed in one
freeze commit BEFORE the wave ready file is written — the round-85 routed
late-controls sequence defect (R1 below) is fixed by exactly this ordering.

## C1 — calibration (lowest owned score 2, HOLD): the round-85 routed-disposition queue

The round-85 non-author closure routed five defects. This round resolves four of
them to recorded dispositions over committed bytes; the fifth (operator template
wording) is operator-owned and only named. `open=4 → open=0` measured by
`.ufo/waves/round-86/count.py --claim c1`:

- **R1 late-controls sequence**: at the freeze revision, `controls/base-c1.txt` and
  `controls/base-c2.txt` exist and read `met=false`, and no
  `controls/after-c{1,2}-carrier.txt` exists; at the measured carrier revision the
  after receipts exist and read `met=true`. Ordering provable from bytes, not
  timestamps.
- **R2 D84-4 operator routing**: the fleet file `.ufo/l0-questions.md` carries a
  `kake | round-86 |` line routing the literal-L2-planner vs validator-prohibition
  conflict to the operator. Route-around, never a silent settlement.
- **R3 counterexample preservation**: `.ufo/waves/round-85/w1/CriticClaims.md`
  (bogus complete rows / canned discriminator disclosure) and
  `.ufo/waves/round-85/controls/late-shortcut-c1.txt` still resolve at the carrier
  revision, and the round-86 lesson references the preserved path.
- **R4 D84-2/D84-3 retained-open debt**: `corpus/README.md` carries a debt row
  naming D84-2 and D84-3 with a `flip:` re-open condition, citing
  `corpus/lessons/round-85.md`. Retention is the routed instruction, not closure of
  the debts.

Textual conjuncts are disclosed as such: a records-only tree with the right
sentences opens nothing; transcription is the non-author closure's catch. The
counter's selftest proves one green fixture, one mutant per item, a junk fixture
and a missing-tree fixture all read as declared.

## C2 — freshness (10, HOLD): bounded value-level Cache-Control reader (capability)

Acquire offline `scripts/cache_control_effective.py`: stdin JSON
`{"cache_control": [<field values in field-line order>], "expires": <http-date|null>,
"date": <http-date|null>, "shared": <bool>}` → one JSON object
`{storable, freshness_lifetime_seconds, basis, no_cache, no_cache_qualified,
must_revalidate, must_understand, duplicate_directives, conflict, invalid_directives}`.
Token-form arguments (recipients accept quoted, §5.2); directive names
case-insensitive; first occurrence wins on duplicate values (§4.2.1 SHOULD — NOT
RFC 7234's most-restrictive rule); shared s-maxage overrides (§5.2.2.10); Expires −
Date fallback (§4.2.1); no-store → storable=false (§5.2.2.5); delta-seconds capped
at 2147483648 (§1.2.2). Exit 0 decode, 1 invalid data, 64 usage; `--selftest` with
TMPDIR-honoring scratch. No socket/urllib usage (offline by construction).

Source: S457 (RFC 9111 via httpwg, tier A, already held) re-opened by the lane THIS
round with a fresh GET receipt; S456 supports. Frontier moved: the round-85
coverage map (`corpus/README.md` "Frontier line") declared value-level
`cache-control` reading open frontier; this instrument holds a bounded slice of it.
It is a separate field-specific reader; it does not upgrade or rewrite the r84
experimental general classifier, claims no arbitrary-header equivalence, no
publishing authorization, no live property request, no browser cache model (Vary,
Age, Pragma, must-understand store-permission stay out of scope, disclosed).

Target: all fifteen frozen count.py CASES match at the carrier (`cases=15/15`),
`selftest_ok=1`, `tool_offline=1`, from `cases=0/15` absent at base. The order
witness pair (cases 5/15: first occurrence ≠ minimum) discriminates against a
min() shortcut; the shared pair (2/3) discriminates against a shared-always
shortcut; no-store heterogeneity discriminates against constant output. Case 15
(`max-age=200, max-age=100` → 200) is the RFC-9111-vs-RFC-7234 order witness: a
most-restrictive implementation is expected to fail by design.

## Measurements, controls, kill rules

```
python3 -B .ufo/waves/round-86/count.py --root . --claim c1 \
  --freeze <freeze-rev> --revision <rev> --work /fast/scratch/hyaku/kake-r86/L1-count
python3 -B .ufo/waves/round-86/count.py --root . --claim c2 \
  --revision <rev> --work /fast/scratch/hyaku/kake-r86/L1-count
```

Committed before dispatch (this freeze commit): `controls/base-c1.txt` (R1–R4 all
unrecorded at base, met=false), `controls/base-c2.txt` (tool absent at base,
cases=0/14, met=false), `controls/ctl-c2-constant.txt`,
`controls/ctl-c2-minmost.txt`, `controls/ctl-c2-sharedalways.txt` (shortcut
decoders fail the frozen cases), `controls/c86-selftest-c1.txt` (counter
selftest green), `controls/census-before.txt`. Kill rule: if any unchanged/shortcut
control meets its target, that claim is unprovable and the counter or target is
wrong — fix before data, never after. Never narrow the 15-case population or
retrofit expectations after a seat scores. A nonzero after measurement is
unprovable. New discovered defects are disclosed, never hidden by green counts.

## Wave / ownership

One v1 wave of 14 seats inside the run-15 band 8–16: scout 2, executor 4, scribe 3,
reviewer 2, critic 1, mutation-tester 1, connector 1; attack share 4/14 = 28.6%
over {reviewer, critic, mutation-tester} — the validator refuses `labrat` as a
swarm role (frozen-topology taxonomy), so the capture probe rides an executor
seat named LabratCapture.
L1 holds the canonical planner (validator forbids planner); ScoutCache
carries the bounded planning data-walk; this is the recorded r85 mitigation, not a
settlement of D84-4 — routed to the operator under R2. Routing is
`task.agentModelOverrides` (read before dispatch; no model passed). Seats write
deliverables only under their unique `.ufo/waves/round-86/w1/<Seat>/` directory and
their own scratch `/fast/scratch/hyaku/kake-r86/<Seat>/`, removed on exit; L1 alone
integrates after WAVE-DONE; seats never commit, push, or mutate any VCS state.

## Frontier, assimilation, mistakes

Census before/after required (`196 → N` rows). The sourced-claim duty: C2 rests on
S457 re-opened this round (fresh receipt, used-by old→new logged in the lesson).
Assimilation (§10, one theme): adopt `crux-keyless-check.md` (staged round-2
new-file) re-grounded on re-opened sources — staged S303 renormalized (escaped-`\|`
recheck cell rewritten) into a new lane id, plus a lane own-work probe row from a
re-run keyless probe; ≥1 reject from the assimilation set recorded in the lesson
Gate (candidate: `crux-eligibility-route.md`, duplicate ground). The §10 id-guard
proof (indented-collision fixture → nonempty collisions) and the scratch-mirror
census gate must both pass before any append. No bumping of staged package bytes;
adoption lands only inside the lane repo. Mine this round's real mistakes into the
round lesson `## Mistakes`; if none, commit the sweep that found none.
