# CriticReasonFidelity — adversarial review of the append-only R4 block

Axis: freshness. Scope: `corpus/quality/citation-adjudications.md` "## Round-47
corrections" block (lines 31–54 at tip `766f461`) vs frozen base
`cd42e3c310ba442e89dde638ba6401adaefaf3e8`. Read-only evidence only.

## Headline

VERIFIED with two unresolved imprecisions and one predicate-scope gap. The R4
block is genuinely append-only, every corrected reason is grounded in the
citing line, and no class changed. Nothing in the artifact falsifies C2's R4
repair; the weakest point is that the committed predicate does not itself
verify the append-only/no-silent-edit property it claims.

## Evidence

### Append-only / no silent row change
- `git diff cd42e3c… HEAD -- corpus/quality/citation-adjudications.md` → a
  single `+`-only hunk (`@@ -27,3 +27,28 @@`): all 20 table rows byte-identical
  at base and tip; only the `## Round-47 corrections` block was added. The
  block's own claim "The five table rows above stay byte-identical" is true.
- `scripts/citation_lint.py:121` `token, file_part, class_part, _reason =
  match.groups()` and `:122 rows[(token, file_part)] = class_part` — the reason
  cell is literally discarded; the ledger's claim "reads only token + file +
  class" (lines 34–35) is accurate.

### Per-row checks (five named rows)

| Row | Citing line/repo/critic precise? | Original untouched? | Class preserved? |
|---|---|---|---|
| `b74190e` | Mostly — names "LOG.md, round-13 entry, charter-ghp clause"; verified LOG.md:46–51 "(4) charter-ghp: … HUMAN pushed 5 commits 18:32:06–20:43:21Z (`b74190e` bake → …)". Round-13 entry starts LOG.md:21. | yes (diff) | yes — corrected reason keeps "(external, absent); historical live-audit record", consistent with `external-repo commit` |
| `d69dd22` | "same misattribution" — verified literal: its only LOG.md citation is line 49 in the same charter-ghp clause (`d69dd22` og-block); old reason was identical phrasing modulo from/in | yes | yes — "(external, absent)" kept |
| `0c767c2` | same — sole citation LOG.md:49 (`0c767c2` window sync) | yes | yes |
| `b9db4b1` | same — sole citation LOG.md:50 (`b9db4b1` CORRECTION) | yes | yes |
| `dc8e1adf` | Critic corrected `CriticC2Sufficiency`→`CriticProbeLeniency`, verified at the citing line SCORECARD.md:1550–1552 ("`CriticProbeLeniency`, `dc8e1adf`, 12 of 12 … `CriticC2Sufficiency`, `0b7779dc`, 11 of 12") and corpus/lessons/round-35.md:154,156,223 + QUALITY.md:832–837 | yes | yes — "Round-34/35 seat-sandbox commit … control label of record" still matches `sandbox-control commit` |

- Each LOG-row correction is a minimal repo-name substitution: original
  `ds4cc-marketplace` → `charter`, all other wording (from/in phrasing, "(external,
  absent)", "historical live-audit record") preserved verbatim.
- Token non-resolution re-verified: `git rev-parse -q --verify` →
  b74190e/d69dd22/0c767c2/b9db4b1/dc8e1adf all non-resolving in the lane
  (consistent with `external, absent` / sandbox classes).
- Predicate re-run: `python3 -B .ufo/waves/round-47/c47_r4_mutation_check.py
  --root . --revision HEAD` → `R4_REASON_FIDELITY base=pass
  mutants=5/5_rejected PASS`, exit 0.

## Unresolved ambiguity / residual findings

1. **Predicate does not enforce append-only (scope gap, not an artifact
   defect).** `r4_reasons_fixed` (c47_routed_count.py:100–112) checks only that
   the corrections block contains the five expected phrases. A revision that
   edited the original rows in place AND added a compliant block would still
   pass. Append-only currently holds only because the committed bytes hold it —
   I verified the diff manually; the gate would not catch a future silent-edit
   regression. Smallest safe correction: none required for this round's claim
   (the claim is about committed bytes), but a durable gate should diff the
   20-row table prefix against base.
2. **`b74190e` "the citing line" is singular; there are two.** LOG.md:8
   (round-6 entry, "`b74190e` static-index bake") and LOG.md:48–51/108
   (round-13) both cite `b74190e` — both name charter-ghp, so the corrected
   reason is right either way, but the correction's wording implies a single
   citing line. Imprecision, not error.
3. **Asymmetric citing-line precision.** `b74190e` names (file, entry, clause);
   `d69dd22`/`0c767c2`/`b9db4b1` rely on "same misattribution" (true — one
   shared clause, verified) and `dc8e1adf` names only the file (unique
   occurrence, SCORECARD.md:1551, so unambiguous). Acceptable; a fully precise
   block would name each citing line.
4. **Adjacent coverage observation (out of R4's declared scope, flagged).**
   `a8f1e2b` — the fifth commit in the same charter series — is cited at
   LOG.md:50–51 in the same clause, is non-resolving, and has no ledger row.
   R4 fixed the four misattributed rows it was routed for; it did not audit the
   whole clause. The line is lint-excluded via EXTERNAL_RE ("charter"), so no
   violation results; noting it as a completeness residual only.

## Checks deliberately not re-run
- Did not re-run `citation_lint.py` itself or the full C2 counter
  (c47_routed_count.py) end-to-end; seat scope was the R4 block's fidelity.
  Receipt `.ufo/waves/round-47/verification/c2-r4-mutation.txt` records the
  mutation check output matching my own re-run.

## Verdict
No falsifier found: the R4 block satisfies "precise citing line/repo/critic,
no silent row change, class preserved" for all five rows, modulo the two
imprecisions above. The predicate-scope gap (finding 1) is the only item a
canonical judge might weigh as a gate-design weakness rather than a claim
falsifier.
