# ReviewCriticIdentity — round 47, wave 1 (reviewer, freshness)

Target: trace `dc8e1adf` through the round-35 lesson/spot-check evidence and inspect
the r47 R4 correction; confirm `CriticProbeLeniency` (`dc8e1adf`, 12/12) is
distinguished from `CriticC2Sufficiency` (`0b7779dc`, 11/12).

Lane tip read: `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` (HEAD); base
`cd42e3c310ba442e89dde638ba6401adaefaf3e8`. Read-only work: no lane production
file, `.jj`, ref/bookmark, fleet repo, sibling repo, `.ufo/state/` or
`.ufo/watchdog.log` was written or moved. No sandbox clone was created. No tools
installed or updated. No LSP device was mounted (`xd://lsp` → "No such tool …
Mounted devices: ast_edit, debug"), so caller/definition checks are literal
reads/greps; no grep output is presented as semantic LSP proof.

## Verdict

**Confirmed, with two low-severity provenance findings and one informational
phrasing risk.** The two controls are distinguished correctly and consistently
across every artifact in the trace; the R4 repair is append-only, its hash pins
match, and its able-to-fail control reproduces at the pinned revision. Nothing
here falsifies C2 as declared. C1 (operability) is outside this slice and is not
assessed.

## Trace of `dc8e1adf` (12/12) vs `0b7779dc` (11/12)

| Evidence | Location | Observed |
|---|---|---|
| Control authored and scored | `.ufo/waves/round-35/w2/CriticProbeLeniency.md:15-17` | sandbox commit `dc8e1adf` on `95abec21`; counter exit 0, `met: true`, `probesPassed: 12`, words 201, `copiedShare 0.0`, goodCites S078/S079/S080/S082 |
| Controls retained as bundles only | `.ufo/waves/round-35/retained/r35-w2-c2-inverted-facts.bundle`; `…/r35-w2-c2-sufficiency.bundle` | heads `refs/heads/ctl/c2-inverted-facts` = `dc8e1adf0f2bdb8ddbd4398fe4b18fd2bba40cb5`; `refs/heads/suff/B-topic-cite` = `0b7779dc4ff214d620929da5b0619022b0fd914a` |
| Criterion receipt | `.ufo/waves/round-35/verification/criterion-knowledge-controls-r35-c2.txt:2-4` | `control dc8e1adf: … "probesPassed": 12`; `control 0b7779dc: … "probesPassed": 11`; `FAIL: control meets the target: dc8e1adf, 0b7779dc`, `exit=1` |
| Sufficiency seat's own table | `.ufo/waves/round-35/w2/CriticC2Sufficiency.md:27` | `0b7779dc` = `met true`, probes `11`, words 639 |
| Lesson | `corpus/lessons/round-35.md:153-157` | 12/12 `(CriticProbeLeniency, commit dc8e1adf)`; 11/12 `(CriticC2Sufficiency, commit 0b7779dc)`; and `:223` cites "QUALITY round-35 (e)" for the same pair |
| Closure spot-check | `corpus/lessons/round-35-verifier-spotcheck.md:26-29, 74-75, 115-116, 185-189` | hashes resolve only from round-35 bundles (`dcef39b5`/`0cce15f0` are the round-34 ones); `dc8e1adf` 12/12 vs `0b7779dc` 11/12; both cheap controls meet the old counter |
| QUALITY criterion | `corpus/QUALITY.md:824-840` (criterion (e); values at `:832`) | `dc8e1adf`, met true, 12 of 12; `0b7779dc`, met true, 11 of 12 |
| SCORECARD | `SCORECARD.md:1550-1553` | `CriticProbeLeniency` + `dc8e1adf` 12 of 12; `CriticC2Sufficiency` + `0b7779dc` 11 of 12 |
| r47 correction | `corpus/quality/citation-adjudications.md:49-54` | `dc8e1adf` = `CriticProbeLeniency` all-false/inverted-facts control, met true, 12 of 12; `CriticC2Sufficiency` = the separate `0b7779dc` row, 11 of 12 |

The distinction is **not** conflated anywhere in the committed r47 target
artifacts: `LOG.md:1806`, `SCORECARD.md:1551`, the append-only ledger correction
(`:49-54`), `corpus/lessons/round-47.md:21` and
`corpus/lessons/round-47-verifier-spotcheck.md:39` each name the right critic or
the right commit; the sole pre-correction row (`:16`) carries the misattribution
that block corrects, and the remaining hits are round-35/36/46 evidence with the
same correct pairing.

## R4 repair under test

- Old cell: `corpus/quality/citation-adjudications.md:16` =
  `Round-34/35 seat-sandbox commit (`CriticC2Sufficiency` re-score, 12 of 12)`.
- Append-only diff: `git diff --stat cd42e3c3…HEAD -- corpus/quality/citation-adjudications.md`
  → `1 file changed, 25 insertions(+)`, 0 deletions. Original 20 data rows stay
  byte-identical (recount at HEAD: 20 total = 12 `LOG.md` + 8 `SCORECARD.md`).
- Lane-local absence of both controls (they are bundle-only, as the round-35
  spot-check says): `git cat-file -t dc8e1adf0f2bdb8ddbd4398fe4b18fd2bba40cb5`
  → `fatal: could not get object info` (exit 128); `git rev-parse -q --verify dc8e1adf`
  → exit 1; the same two commands on `0b7779dc…` give the same result.
- Counter reproduction (read-only; the counter uses `git show` only):
  - `python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision cd42e3c3…`
    → `outstanding=4/4 C2_NOT_MET`, exit 1.
  - same at `714e707…` → `outstanding=0/4 C2_MET`, exit 0.
- Able-to-fail proof reproduction:
  `python3 -B .ufo/waves/round-47/c47_r4_mutation_check.py --root . --revision 714e7074110469a9ed2a3594677197baa0890905`
  → `R4_REASON_FIDELITY base=pass mutants=5/5_rejected PASS`, exit 0.
  The `dc8e1adf` mutant swaps `CriticProbeLeniency` → `CriticC2Sufficiency`
  (`.ufo/waves/round-47/c47_r4_mutation_check.py:65-66`) and is rejected.
- Hash pins: at `714e707` and at HEAD the ledger is
  `e75bc3a746539d86651f4b31f578480702fc325cbe1e1555cd76aa38d5058669`, the counter
  `9be35ef2452aaff0757a0c2839c17cb58e08a7a59f6a217a3489598c19a8359e`, the probe
  `0c8aa7a4357e836e0011871900d0e26bbb4f4c426b91ea2634538405c482ada2` — equal to
  the receipt's `ledger_sha256_at_revision`, `counter_sha256_at_revision` and
  `mutation_probe_sha256`; `git merge-base --is-ancestor 714e707 HEAD` → 0.
  Receipt `verification/c2-r4-mutation.txt` sha256 =
  `1e7636ecb023b2d2fa61d5bb6904166ebe84337514beed175c8010675cd507c3`, as the
  lesson and spot-check state.
- Round-46 gate still clean at the tip: `python3 -B scripts/citation_lint.py --root .`
  → exit 0, 0 violations; `dc8e1adf` is adjudicated only at `SCORECARD.md:1551`.

## Findings

### 1. LOW — the correction's QUALITY pointer names the wrong criterion

`corpus/quality/citation-adjudications.md:51-52` cites
`QUALITY round-35 (a)` for the 12/12 grounding. The grounded criterion is
round-35 **(e)** at `corpus/QUALITY.md:824-840` (values at `:832`), and the lane's
own lesson already cites it as "(e)" (`corpus/lessons/round-35.md:223`).
`(a)` is wrong under every reading: round-35 criterion (a) is the
do-nothing-control target criterion; the round-35 wave-2 corrections item (a)
(`QUALITY.md:856`) is the C1 22-of-24 slack; round-36 (a) (`QUALITY.md:864`) is
the sourced-learning bar in a different section. The same parenthetical also
names `corpus/lessons/round-35.md`, which does carry the values, so the corrected
reason and the C2 predicate are unaffected. This is nonetheless the same class
of defect R4 was raised to repair (evidence pointer drifted from the artifact it
describes), so it should be fixed append-only in a later round.

### 2. LOW — `Round-34/35` era label is unsupported for `dc8e1adf`

Both the old cell (`citation-adjudications.md:16`) and the corrected reason
(`:53`) say `Round-34/35 seat-sandbox commit`. `dc8e1adf` exists only in the
round-35 bundle, and the round-35 closure itself separates the eras:
`corpus/lessons/round-35-verifier-spotcheck.md:26-29` lists `dc8e1adf` and
`0b7779dc` among hashes resolving only from round-35 bundles and says
`dcef39b5`/`0cce15f0` are the round-34 ones; `CriticProbeLeniency.md:15` records
the commit on the round-35 build `95abec21`. `Round-34/35` is defensible only as
a series label, not as the commit's round. The same label remains on the
`0b7779dc` row (`:23`), which the R4 correction did not touch. Note the label is
pinned in `R4_EXPECTED` (`.ufo/waves/round-47/c47_routed_count.py:45`), so a
precision fix requires updating the counter in the same change.

### 3. INFO — "wrong critic" overstates the original text

`LOG.md:1804-1808` and `corpus/lessons/round-47.md:20-22` describe the old
attribution as naming "the wrong critic". The round-35 spot-check records that
the `C2Sufficiency` seat re-scored the wave-2 controls from the bundles,
including `dc8e1adf` at 12/12 (`corpus/lessons/round-35-verifier-spotcheck.md:70-75`).
The old phrase "(`CriticC2Sufficiency` re-score, 12 of 12)" was therefore a true
statement about the re-scoring seat read as authorship. The corrected reason is
right about provenance; a future touch should say "names the re-scoring seat, not
the control's author" rather than "wrong critic".

## Residual risk

- **Gate suppression is positional.** The new `dc8e1adf` mention at `LOG.md:1806`
  is neither adjudicated nor flagged: `scripts/citation_lint.py:161` skips the
  line because `EXTERNAL_RE` (`:45`) matches "charter" on the same physical line,
  and there is no `(dc8e1adf, LOG.md)` ledger row. A reflow that drops "charter"
  from that line while adding a commit-context word would surface an
  unadjudicated dead token. Low likelihood, but the ledger row population is
  keyed by `(token, file)` and does not cover the LOG correction.
- **The R4 predicate cannot see either finding.** `r4_reasons_fixed`
  (`c47_routed_count.py:100-112`) checks only that each "Corrected reason:"
  phrase is contained in its token's bullet. A wrong explanatory pointer
  (finding 1) or an unsupported era label (finding 2) passes it by construction;
  the corrected reason and the 12/12-vs-11/12 distinction remain correct.

## Verification gaps

- I did not re-execute `.ufo/waves/round-35/criteria/knowledge_control_check.py`
  against the retained bundles: that needs a bundle-fetched sandbox clone, and
  this lane's bounds allow sandbox clones for mutation controls only. Evidence
  used is the committed criterion receipt (`:2-4`), the probe-leniency seat's
  recorded counter output (`:15-17`), the sufficiency seat's table (`:27`), the
  lesson (`:153-157`) and the closure spot-check (`:70-75`).
- No LSP device was mounted; no definition/reference semantics were claimed.
- I did not run the other r47 seats' checks (R1/R2 C1 registry and receipt
  coverage, R3/R5/R6 repairs); no claim is made about them.
