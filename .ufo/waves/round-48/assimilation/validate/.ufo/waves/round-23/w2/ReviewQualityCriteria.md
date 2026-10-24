## Verdict

Counterexample found. The round-23 parser-relaxation probe passes after its canonical-link guard is deliberately removed, despite that mutation producing a clean result for a foreign-content canonical link. The C1 counter also accepts a receipt whose absent surface is mislabeled HOLD, so the freshness rule is not failure-capable for an expressly prohibited classification.

## Findings

### P1 — C1 can count a gone surface mislabeled HOLD as fresh re-verification

**Source / affected criterion:** `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md:145-147` requires a gone surface to be UNVERIFIABLE (with a reason), never HOLD, and says a gone presence claim is STALE. The criterion does not name a failure command. The contract's `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py` is the counting command.

**Evidence:** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py:69-94` validates that verdicts are among HOLD/STALE/UNVERIFIABLE, that UNVERIFIABLE has a nonempty reason, and that each unit has at least one HOLD or STALE. It does not compare verdicts to surface state, method, or observation. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/counter_selftest.py:82-98` also treats a synthetic `fixture://c1` surface and synthetic observation as a valid HOLD fixture.

In a `git clone --no-hardlinks` scratch clone of 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd, I changed only `fire-journal-codes:c2` from `UNVERIFIABLE` to `HOLD`; its existing observation still says `script=absent`, and its reason still says the implementation and state directory are absent. The isolated clone mutation was committed as `e4452fe8ed6ba0f6953ba7484d9a7cc36395ac56`.

**Exact command:**

```sh
python3 /tmp/kake-r23w2-ReviewQualityCriteria-T90T/lane/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r23w2-ReviewQualityCriteria-T90T/lane --revision e4452fe8ed6ba0f6953ba7484d9a7cc36395ac56
```

**Exact observed result excerpt:** `accepted: 17`, `total: 17`, exit 0; claim verdicts changed to `HOLD: 80, STALE: 49, UNVERIFIABLE: 39`. The counter therefore accepts a receipt violating the criterion's explicit “gone ... never ... HOLD” rule. The clone came from the lane; to reconstruct the baseline receipt use `git show 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd:.ufo/waves/round-23/receipts/fire-journal-codes.json`, then change the `c2` verdict as described above. No lane files were modified.

**Impacted claim/axis:** C1 / freshness. A 17/17 count can include an explicitly misclassified missing surface.

**Smallest fix:** Define a structured per-claim surface state and claim kind, validate the required HOLD/STALE/UNVERIFIABLE mapping against those fields, and add a selftest that changes an absent-surface claim to HOLD and requires `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py` to exit 1. A reason string or an enum membership check is not evidence that a claim was decided correctly.

### P2 — The named relaxation probe does not cover the canonical-link failure mode it claims to cover

**Source / affected criterion:** `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md:139-144` names canonical links as one way the newly evaluated region can feed the decision and requires a probe for each. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/relaxation_probe.py:22-31` tests base variants, including foreign-content/base and parser-recovery cases, but no canonical-looking link in SVG/MathML/foreignObject.

**Mutation:** In the same scratch clone, I changed only `/tmp/kake-r23w2-ReviewQualityCriteria-T90T/lane/scripts/canonical_audit.py`'s `_foreign_token` condition at line 209 from the base/head/canonical-link guard to the base/head guard alone. This disables the foreign-content canonical-link guard. The named probe still passed all 11 cases:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/relaxation_probe.py --validator /tmp/kake-r23w2-ReviewQualityCriteria-T90T/lane/scripts/canonical_audit.py
```

Observed: `passed: true`, `met: 11`, `total: 11`, exit 0.

A scratch manifest/page with a self-closed wrong canonical link inside `<svg><foreignObject>…</foreignObject></svg>` demonstrates the missed decision path. The current validator returned `html_unsupported` / `could-not-evaluate`, exit 2; the mutated validator returned no findings / `clean`, exit 0. The page was:

```html
<head><link rel=canonical href=a.html></head><body><svg><foreignObject><link rel=canonical href='https://wrong.test/evil.html'/></foreignObject></svg></body>
```

The earlier `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/w1/FalsifyForeignContent.md` records a one-off 14-case run that included a foreignObject canonical link, but the named, committed `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/relaxation_probe.py` does not retain that case, and its stated fail condition does not detect this regression.

**Impacted claim/axis:** Parser-relaxation criterion / C2 operability. A false-clean regression in a named signal path leaves the quality-bar command green.

**Smallest fix:** Add a foreign-content canonical-link attack (including the self-closing form above) to `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/relaxation_probe.py`; require it to fail closed, and verify the probe exits nonzero when that guard is removed.

## Checked and held

- Current C1 counter (run with working directory `/home/vgpnk/Projects/shokunin/kake-shokunin`):
  `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` → exit 0, `accepted: 17/17`; verdict totals `HOLD 79, STALE 49, UNVERIFIABLE 40`.
- Current C2 counter (run with working directory `/home/vgpnk/Projects/shokunin/kake-shokunin`):
  `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` → exit 0, `accepted: 12/12`; per-surface outcomes were 3 clean, 5 failed-policy, and 4 not-served. This is receipt coverage, not 12 clean policy outcomes.
- `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/counter_selftest.py` → `selftest: passed`. Its all-UNVERIFIABLE mutation was rejected (`accepted: 16/17`, exit 1), so that narrow failure condition is live; it does not test an invalid HOLD classification.
- C2 404 falsifier: in a scratch clone, I changed the `plazir27-kimi` 404 audit receipt from `not-served` to `clean`, then ran `/tmp/kake-r23w2-ReviewQualityCriteria-T90T/lane/.ufo/waves/round-23/measure_c2.py` at clone revision `11908396ce573418f811d817ed5c5d51b9405f60`. It exited 1 with `accepted: 11/12` and `non-served surface lacks a matching not-served receipt`. The 404-is-not-canonical rule is failure-capable.
- Exact relaxation-probe runs using validators extracted with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show <revision>:scripts/canonical_audit.py`: b539cc1 → exit 1, 7/11; 4d95d2e → exit 1, 2/11; current 5e5afb9 → exit 0, 11/11. This confirms the stated overall predicate direction, but not the omitted canonical-link branch above.
- Correction-register predicate checks: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/postfix/counter-probe.py` against the c0fd6d5 runner exited 1 (the probe reported `passed: false`); against the current round-22 runner it exited 0 (`passed: true`). The current probe output says CE1/CE3 were rejected at the frozen-instrument-digest check, rather than exercising the mutated matrix's aggregate calculation. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/postfix/defect-probe.py` against c0fd6d5 exited 1 (2/8); against the current validator it exited 0 (8/8). The corrected exit directions are therefore observed.
- Trying C1 against base `b5d599e19bead54b96f589444e9ec64cdf67c28a` returned exit 2, `revision or frozen population unreadable`; that revision predates the frozen round-23 population and is not a meaningful 0/17 counterexample.

## Limits

- No independent public HTTP requests were made. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py` reproduces the committed body/audit against the revision's validator; it does not independently attest that the GET occurred or authenticate `fetchedAt` and the claimed URL against a remote response. Thus C2's 12/12 is reproducible receipt coverage, not independent network provenance. No builds, linters, or formatters were run; no tools were installed.

I attempted to read `xd://lsp`; the tool returned `No such tool` and listed no LSP device. LSP status/references/definition/diagnostics were unavailable. Findings are based on direct source reads and the targeted CLI probes above; no text grep is presented as semantic proof.
