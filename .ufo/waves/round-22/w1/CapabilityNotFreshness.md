# CapabilityNotFreshness — critic report (C1, operability)

Seat: critic, wave 1, read-only. Scope: attack claim C1 on the
capability-vs-instrument axis — whether the deliverable earns a `capabilities:`
row under `AXES.md` §Capabilities, and whether "capability" wording launders a
freshness claim or an unverifiable pre-claim. Contract:
`.ufo/waves/round-22/contract.json`; base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Sibling critics own exit-map relabels, population denominators, Google-selection
overreach, and causal separation; none of that is restated here except where it
changes capability admission.

## Governing rule and observed state

`AXES.md` (fleet): "Rows enter only through a round that demonstrates the
capability running; a capability without a passing demonstration in the round
report is pre-claiming and does not enter the table." SCORECARD precedent: the
lone existing row (Curated source registry) entered on a demonstration that
produced *new domain artifacts* (18 mined rows, 4 citing knowledge entries,
census exit 0) — not on a selftest. The r21 verifier
(`corpus/lessons/round-21-verifier-spotcheck.md`) likewise graded the
`corpus-contract` gate an *operability improved* verdict, not a capability,
because its demonstration was author fixtures plus replay.

Observed at lane HEAD `7c61c8cc` (this session, read-only):

| Surface | Observed |
|---|---|
| `scripts/canonical_audit.py` | absent from tree and index (`find` + `git ls-files`) |
| `.ufo/waves/round-22/{matrix.py,cases.json,measure.py,fixtures/**}` | absent from lane tree (writer-clone only by design) |
| `SKILL.md` (uncommitted diff) | already contains a `canonical-audit` **gate registry row** naming `python3 scripts/canonical_audit.py --manifest …` as Entry command with selftest/pinned-proof columns |
| `corpus/knowledge/static-canonical-preflight.md` | untracked; its `recheck:` already names `python3 scripts/canonical_audit.py --selftest` and `matrix.py --root .` |
| `~/Projects/ufo-fsd-alpha` | present; `docs/charter-ufo-fsd/index.html:8` carries `<link rel="canonical" href="https://veigapunk.github.io/charter-ufo-fsd/">` — a real committed HTML artifact with a canonical signal, fully offline |

Consequence: the working tree currently registers consumers of the capability
(gate row, knowledge recheck line) while the capability artifact does not yet
exist in this tree. If that registration is committed in any state where the
script/matrix are absent — or cited at a revision where the artifacts are
clone-only — the capability is pre-claimed: the evidence pointer does not run.

## Falsifiable acceptance constraints for C1-as-capability

1. **Runnable-at-revision pointer.** The capability row's evidence pointer must
   resolve and execute at the cited master tip committed by L1
   (`python3 scripts/canonical_audit.py --selftest` exit 0; `measure.py
   --revision <tip>` materializes validator+matrix+cases+fixtures from git
   blobs, not from a sibling clone's working tree). A pointer that requires
   `/tmp/kake-r22-<seat>` or uncommitted bytes is a pre-claim; the row must be
   withheld or the revision re-cited.
2. **Demonstration ≠ selftest.** Matrix acceptance (32/32 against author-built
   frozen cases) is the instrument-grade proof; the capability row needs a
   distinct *domain run*: a manifest over HTML the lane did not author for this
   round. Offline-safe candidate exists today —
   `~/Projects/ufo-fsd-alpha:docs/charter-ufo-fsd/index.html` (committed
   `72ab84a8`, canonical at line 8). Acceptable minimum: manifest with
   `expectedCanonical` derived from the *declared publishing policy*
   (`veigapunk.github.io/<repo-path>` host convention), run against the file
   as-committed, verdict recorded. If no such run is archived, admit C1 only as
   an operability instrument move (r21 corpus-contract precedent), not a
   capability row.
3. **Non-tautological policy input.** `expectedCanonical` must come from the
   named policy source, never from the page's own `rel=canonical` href or from
   running the validator to harvest expected values. A demonstration whose
   expected values are copied out of the audited tag is self-agreement: it can
   detect `canonical_missing`/`canonical_multiple` but can *never* fire
   `canonical_mismatch`, so the head verdict is vacuous. Matrix-side: the 32
   expected exits/ids must be derivable from contract policy text without the
   validator's output (shared line with NoCarriedRedRelabel — mine adds the
   *policy-source* requirement on real inputs).
4. **No freshness bleed.** The claim is `type: capability`, axis operability.
   Reject any SCORECARD/LOG/report wording that counts a canonical-audit run as
   freshness evidence: validator input is manifest+file bytes, so a clean run
   proves nothing about what any host currently serves. The knowledge entry's
   own wording ("local behavior has separate committed round22 receipts, not
   live website verification") is the bound; deviations in the round report or
   SCORECARD row are defects. Also reject the r20-C3 failure mode in reverse:
   no "freshness supported" credit from a static audit.
5. **Registered upkeep, honest gate class.** Capability registration (SKILL.md
   gate row / SCORECARD row) must classify `canonical-audit` as an
   author-invokable gate on named local inputs, with `measure.py`/matrix/`replay.py`
   explicitly *evidence tools, not domain gates* (the uncommitted SKILL.md diff
   already does this — it must survive integration verbatim or better). A
   capability with no standing re-run path is undetectable rot: first drift of
   `cases.json`/fixture digests must break `replay.py` exit 0, which is the
   lane's own drift-detection discipline applied to the new capability.
6. **Input provenance stays author-side and frozen.** `measure.py` must pin
   SHA-256 of every measured blob (validator, matrix, cases, fixtures) at both
   baseline and candidate revisions, and the baseline run must record
   `accepted 0 / unavailable` — capability absent, not 32 failures (SKILL.md
   draft already states this; hold it).
7. **Claim-type honesty.** The round report must record `type: capability` and
   the axis verdicts must say operability HOLD-10 capability-entered-or-not —
   never a numeric score move, never a second freshness credit. If the
   capability row is withheld per constraint 2, C1 still lands as operability
   improved-bounded; calling it a capability anyway is the exact pre-claiming
   defect AXES names.

## Overclaim to reject

- **"Proves clean positive controls" → "the capability works."** A green
  self-authored matrix is instrument acceptance, not demonstration. The r21
  verifier required committed-blob re-measurement plus domain artifacts for the
  registry capability; hold C1 to the same.
- **Any capability-row wording implying live coverage**: "audits the fleet's
  canonicals", "pages canonical-checked", "site canonicals verified". The tool
  audits serialized local files against a declared manifest; the lane's
  publishing targets are remote and operator-gated — zero live pages were or
  can be audited this round.
- **Gate-row-before-artifact**: the uncommitted `SKILL.md` diff registers
  `canonical-audit` while `scripts/canonical_audit.py` is absent from the lane
  tree. Landed in that order it is pre-claiming; L1 must integrate script +
  registry atomically at one cited revision.
- **"Offline" as a completeness word**: offline bounds reads, it does not make
  the audit total. The 32 cases are a sample of policy space; `html_unsupported`
  and `input_invalid` outcomes are could-not-evaluate, never silently clean.
- **Capability without durable evidence**: a row whose pointer is a `.ufo/waves`
  artifact that decays (fixture drift, unpinned blob) is a freshness debt the
  lane created itself — reject rows lacking digest-pinned replay
  (`replay.py`-style) or a committed selftest.

## Distinct wave-2 attack — the tautological demonstration and the phantom row

My wave-2 attack, distinct from the per-case falsifiers and the exit-map
relabel:

1. **Policy-source probe.** Read the integrated `cases.json` + any archived
   demonstration manifest. For every non-fixture manifest cited in the report,
   check how `expectedCanonical` was obtained: declared policy (host/path
   convention, sitemap, prior corpus pin) vs. harvested from the audited tag.
   Harvested ⇒ the `canonical_mismatch` finding id is unreachable on that run;
   the demonstration is structurally vacuous → capability not demonstrated,
   only the instrument.
2. **Real-artifact run.** Construct a manifest over
   `~/Projects/ufo-fsd-alpha/docs/charter-ufo-fsd/index.html` with
   `expectedCanonical: https://veigapunk.github.io/charter-ufo-fsd/` (policy =
   gh-pages host convention `owner.github.io/<repo>/path`, already the lane's
   documented convention in `ghp-*` knowledge). Expect exit 0. Then two
   negative mutations in scratch: (a) href → `#` (expect
   `canonical_fragment`/exit 1), (b) manifest expected →
   `https://example.test/x` (expect `canonical_mismatch`/exit 1). If the real
   page trips `html_unsupported`/`input_invalid`, the capability's practical
   surface is narrower than claimed → bound the row wording.
3. **Registration-vs-artifact check.** At the measured revision, `git ls-tree
   <tip> scripts/canonical_audit.py` must exist AND `SKILL.md`'s gate row and
   the SCORECARD capability row must cite that same revision. Row present +
   script absent at cited revision = pre-claiming defect, judge-must-reject.
4. **Freshness-bleed grep.** `git diff` SCORECARD/LOG at the measured revision
   for any row that (a) changes the freshness score/verdict, (b) cites
   canonical-audit output under freshness evidence, or (c) re-labels the
   carried paths-gate red as covered by the new capability.
5. **Decay tripwire.** Flip one byte in one committed fixture in a scratch
   clone; `replay.py`/matrix must turn non-zero. A capability whose proof can't
   detect its own inputs rotting fails the lane's own freshness doctrine.

## Smallest safe correction

- Integrate `scripts/canonical_audit.py`, `cases.json`+fixtures, `matrix.py`,
  `measure.py`, `replay.py`, the SKILL.md gate row, and the SCORECARD row in
  ONE commit; cite that commit's hash as the measured revision.
- Add one archived real-artifact demonstration (ufo-fsd-alpha manifest, policy-
  derived expected value, JSON receipt) before writing the capability row;
  otherwise land C1 as operability improved-bounded and hold the row for a
  round that demonstrates it.
- In every report/row, bind wording to "local publisher-policy comparison over
  named serialized files" — never site/live/current.

Verdict shape: fixable defect (ordering + one demonstration + wording bounds)
if caught before L1 integrates; if the capability row lands with a
clone-only/non-resolving pointer or a self-agreeing demonstration, it is
pre-claiming — the class AXES.md explicitly bars — and the canonical Rust judge
must reject the capability, leaving at most an operability improved-bounded
verdict.
