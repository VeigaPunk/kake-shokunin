# Citation adjudication ledger (round 46, C2)

Committed ledger read by `scripts/citation_lint.py`: a flagged citation named
here (token + population file) is reported as adjudicated, not as a violation.
Classes name what the line itself asserts; every target below was re-verified
non-resolving in the lane repository at round 46 (`git rev-parse -q --verify`).

| Token | File | Class | Reason |
|---|---|---|---|
| `e5455253` | SCORECARD.md | quoted-dead-token | Quoted defect token from the round-45 closure (routed defect 1), not a provenance citation; the true registry commit is `e54552553eaff4d7…`, named in `corpus/lessons/round-45-verifier-spotcheck.md`. |
| `e5455253` | LOG.md | quoted-dead-token | Same quoted defect token as the SCORECARD row; retained as defect evidence, not as a citation of record. |
| `7fc6aa2f` | SCORECARD.md | external-repo pin | ds4cc-marketplace upstream pin (rounds 33–34); the marketplace repository is external to the lane and absent from the host, so the pin cannot resolve here. |
| `dcef39b5` | SCORECARD.md | sandbox-control commit | Round-34/35 control commit built in a seat sandbox (junk-directory / lookup-tool control); never a lane commit; cited as a control label of record. |
| `0cce15f0` | SCORECARD.md | sandbox-control commit | Round-34 hollow-control commit (seat sandbox); never a lane commit; control label of record. |
| `5f767534` | SCORECARD.md | sandbox-control commit | Round-34 constant-clean control commit (seat sandbox); control label of record. |
| `dc8e1adf` | SCORECARD.md | sandbox-control commit | Round-34/35 seat-sandbox commit (`CriticC2Sufficiency` re-score, 12 of 12); control label of record. |
| `b74190e` | LOG.md | external-repo commit | ds4cc-marketplace repo commit from the 2026-09-28 push series (external, absent); historical live-audit record. |
| `9c28d29` | LOG.md | external-repo commit | webzites/charter scribe remote HEAD (external repo, absent); historical beat record. |
| `e6bd071` | LOG.md | external-repo commit | ds4cc-marketplace remote HEAD at round 16 (external, absent). |
| `f3d2ecd` | LOG.md | external-repo commit | ds4cc-marketplace working-tree HEAD at rounds 13–16 (external, absent); its sitemap commit role is named on the citing line. |
| `dcef39b5` | LOG.md | sandbox-control commit | Same round-34 control commit as the SCORECARD row; control label of record. |
| `b6580c79` | SCORECARD.md | sandbox-control commit | Round-33 `CriticC2Sizing` hollow commit (seat sandbox) cited as a control of record. |
| `0b7779dc` | SCORECARD.md | sandbox-control commit | Round-34/35 seat-sandbox commit (`CriticC2Sufficiency`, 11 of 12); control label of record. |
| `d69dd22` | LOG.md | external-repo commit | ds4cc-marketplace repo commit in the 2026-09-28 push series (external, absent). |
| `0c767c2` | LOG.md | external-repo commit | ds4cc-marketplace repo commit in the same 2026-09-28 push series (external, absent). |
| `b9db4b1` | LOG.md | external-repo commit | ds4cc-marketplace repo commit in the same 2026-09-28 push series (external, absent). |
| `c814526` | LOG.md | external-repo commit | plazir-15-site repo HEAD, 2026-09-26 (external, absent). |
| `bd02d10` | LOG.md | external-repo commit | plazir-15-site repo remote HEAD, 2026-09-26 (external, absent). |
| `481d28cb` | LOG.md | external-repo commit | Fleet-repo commit where the round-20 S009 anchor moved (external to the lane, absent from its object store). |

## Round-47 corrections (r46 closure routed defect R4, append-only)

The five table rows above stay byte-identical; their classes are correct and
`scripts/citation_lint.py` reads only token + file + class. This block corrects
their reason prose, per the round-20 post-review ruling (pure new-line
additions citing the old line, never an in-place cell edit).

- Row `b74190e` | LOG.md — reason says "ds4cc-marketplace repo commit from the
  2026-09-28 push series"; the citing line (LOG.md, round-13 entry, charter-ghp
  clause) names the **charter** repo's 2026-09-28 HUMAN push series. Corrected
  reason: charter repo commit from the 2026-09-28 push series (external, absent);
  historical live-audit record.
- Row `d69dd22` | LOG.md — same misattribution; corrected reason: charter repo
  commit in the 2026-09-28 push series (external, absent).
- Row `0c767c2` | LOG.md — same misattribution; corrected reason: charter repo
  commit in the same 2026-09-28 push series (external, absent).
- Row `b9db4b1` | LOG.md — same misattribution; corrected reason: charter repo
  commit in the same 2026-09-28 push series (external, absent).
- Row `dc8e1adf` | SCORECARD.md — reason says "(`CriticC2Sufficiency` re-score,
  12 of 12)"; the commit is the `CriticProbeLeniency` all-false/inverted-facts
  control (met true, 12 of 12 — `corpus/lessons/round-35.md`; QUALITY round-35
  (a)). `CriticC2Sufficiency` is the separate `0b7779dc` row (11 of 12).
  Corrected reason: Round-34/35 seat-sandbox commit (`CriticProbeLeniency`
  all-false entry, met true, 12 of 12); control label of record.
