# Round 44 — source locator correction

## Gate

Re-opened the S129 and S130 sources on 2026-10-23. Section locations below use section-prose paragraph counting; each quoted passage is in the first paragraph of its named section.

| Row | Re-opened source path | Verbatim quote and true location | Decision |
|---|---|---|---|
| S129 | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md`; `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/ReviewFreeze.md` (both re-opened 2026-10-23) | “The do-nothing shortcut never reaches predicate_pass=true” — 6 words; CtlDoNothing.md §Verdict, first section-prose paragraph. “every pinned sha256 verifies over the committed blob” — 8 words; ReviewFreeze.md §Verdict, first section-prose paragraph. | Admit; retain the pre-data control and freeze-conformance method, correcting the locators to the first section-prose paragraphs. |
| S130 | `/home/vgpnk/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` (re-opened 2026-10-23) | “records a calibration error present when the statement was written” — 10 words; §Checking self-assessment statements at writing, first section-prose paragraph. | Admit; retain the writing-revision calibration method, correcting the locator to the first section-prose paragraph. |

### Superseding source rows

S131 and S132 are the append-only superseding rows for S129 and S130 under SOURCES.md contract rule 2: a correction is a new row whose `teaches` cell opens `supersedes S0NN — `. These exact anchor and `teaches` cells are the new row text; S129 and S130 remain unchanged.

| New row | Exact new anchor cell | Exact new `teaches` cell |
|---|---|---|
| S131 (supersedes S129) | `CtlDoNothing.md "## Verdict", first paragraph (seat tameshi-r33-w1-CtlDoNothing, lane rev f6d8a891); ReviewFreeze.md "## Verdict", first paragraph and §1 (seat tameshi-r33-w1-ReviewFreeze); opened 2026-10-23` | `supersedes S129 — the frozen counter must catch a do-nothing shortcut before data, and the freeze commit's pinned bytes must verify before seats score; the corrected locators are CtlDoNothing.md §Verdict, first paragraph, and ReviewFreeze.md §Verdict, first paragraph and §1.` |
| S132 (supersedes S130) | `§"Checking self-assessment statements at writing", first paragraph; opened 2026-10-23` | `supersedes S130 — a self-assessment is checked against the committed tree/history at its writing revision, not only at the current tip; the quoted calibration-error statement is in the first section-prose paragraph.` |

## Mistakes

12. **Class: a manifest class label treated as causal proof — one control attributed to a
    mechanism its source does not contain (round 44, found by the wave-1 critics).** Evidence:
    `.ufo/waves/round-44/controls-27.tsv` row 26 read `buildport-m6  portdigit  G9` in every
    inherited receipt — `verification/freeze/control-v4blind.json`,
    `verification/placebo/before.json`, `verification/smoke-v4.json` — while the control source
    flips the **default-port branch** (`controls-r43/buildport-m6-default-branch.py:303-304`:
    `if port is not None: port = 80 if scheme == "http" else 443`), a one-hunk mutation of
    `if port is None:` whose originating witness is an explicit-default-port loc against an
    implicit-port sitemapUrl (`.ufo/waves/round-43/w1/MutBuildPort.md:20,24-29`); the control
    holds no memo or cache construct (0 hits for `memo`/`cache`). The wrong label propagated into
    the wave-1 instrument spec (`make_w1_spec.py:103` gave the G9 seat "port-keyed parse caches
    and the inverted default-port branch"), so the frozen G9 generator also carries default-port
    witness batches (`classes/g9_port_digits.py:1,10,50`). Captured-by: the wave-1 critics —
    `CriticClaimC1` attack (a3) and `CriticMathDenominator` finding 2 and table row 25 — before
    any claim receipt existed; the L1 recorded the correction at `SCORECARD.md:3551` ("Round 44
    — pre-freeze correction 2", item 2). Fix: the frozen manifest now carries the source-derived
    label — row 26 reads `buildport-m6  default_port  G2` (manifest sha256 `a1f0e364…`, changed
    from the `233afa37…` the critics pinned) — and the frozen audit driver `c44_audit.py`
    (sha256 `8ee2c8bf…`) writes the label together with the caught keys into every receipt
    (`class` / `classCaught` / `legacyCaught`, `c44_audit.py:199-200`), so a label that does not
    match the mechanism stays visible per row: the claim receipt
    `verification/claim/after-v5.json` records `buildport-m6` as `default_port / G2` with
    `classCaught ["G2","G4","G9"]` — the source-derived key present, the cross-class catches
    visible instead of being described as port-digit-cache coverage. Able to fail: the inherited
    receipts still carry the old `portdigit / G9` label and the pre-correction manifest hash, so
    the misattribution is preserved as evidence rather than erased; the label is not itself a
    witness gate (`semantic_witness` accepts any class key, `c44_audit.py:63-66`), so the
    recurrence guard is the manifest row plus the receipt-level label-vs-caught exposure, not the
    predicate.

13. Instrument defect — audit-driver receipt cohorts collide across runs — evidence:
    `c44_audit.py:130-132,174-175` derives `tools/` and `build-{1,2,3}.json` from
    `dirname(--out)`, so every audit leg whose `--out` shares a parent overwrites the previous
    leg's per-control receipts (observed 2026-10-23: three concurrent wave-2 legs in
    `verification/claim/` clobbered each other's cohorts; `w2/ExecAfterBaseline.md`,
    `w2/ExecBeforePlacebo.md`, `w2/ExecV4Support.md`, `w2/CriticKillRules.md` preserve the
    8-v4/19-v5 mix and 17 row mismatches) — captured-by: receipt-link integrity
    (a cited receipt must re-derive from the summary's recorded seeds; kill rule 2's
    evidence chain) — fix: every audit leg uses its own `--out <dir>/<name>.json` cohort
    directory, never a shared parent (applied this round:
    `verification/claim/{after-final,placebo-final,v4-final,canary-final}/`); a future
    driver revision should name a per-run cohort directory itself. Able to fail: the
    contamination is preserved verbatim in the wave-2 reports above and re-derived by
    re-running any two legs into one parent.
