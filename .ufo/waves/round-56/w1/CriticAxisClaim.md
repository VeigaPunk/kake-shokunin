# CriticAxisClaim

Axis-naming review of round-56 C1 and C2 against the round prompt's §9 rule (`/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-56.md:435-439`):
"Name the axis by the surface the round changes, not by the number it produces (kaidoku r29). ... A coverage claim names the surface it moves
(frontier → core, a new tool, operation or edge class) and the command that would show it unmoved."

Method: read-only. Read: the frozen contract and `contract.json`, both counters' code at the working tree (`c56_quote_truth.py` is modified vs base —
its docstring says version 1.1 only ports the `--selftest` stub), `AXES.md`, `LEARNING.md`, `SCORECARD.md` head and `## Round 55`, `PROVINCE.md`,
`corpus/README.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, the r52/r53/r55 lessons and the r55 verifier lesson, `sources/receipts.json`. **Not run
by this seat** (axis review, not measurement): both counters, the census, `span_tools.py` checks. Claims below rest on code and committed bytes I
read.

Baseline numbers re-derived here (read-only): registry rows at base = 156, knowledge files at base = 49.

## C1 AXIS:

**Verdict: not calibration by the rule's own words; closest honest label is operability (10 → 10 HOLD, closing round-55 routed defect 1). Calibration
stays 1/10 this round.**

For calibration:

1.  Shape match. A number the lane writes about itself against the number its own command prints is the same class as `AXES.md:15`'s signal; at base 7
of 10 registry rows overstate their gate's fixture count.
2.  Precedent. Round-55's C1 was already a third surface (`corpus/README.md` coverage map) and the r55 verifier ruled it "calibration (C1) | improved"
(`corpus/lessons/round-55-verifier-spotcheck.md:48`), so the lane's calibration axis has already been widened past SCORECARD/SHONEN once.
3.  Obligation fit. Calibration is the only axis below 10 (score 1), so the lowest-axis obligation lands there; r55 routed defect 2 leaves that
ownership with the operator, i.e. the widening is an open question rather than a settled no.

Against calibration (decisive):

1.  `AXES.md:15` names the signal: "SHONEN.md/SCORECARD entries match observed repo state". The ten rows are `SKILL.md:726, 1067, 1093, 1128, 1198,
1199, 1215, 1216, 1233, 1234` — neither file.
2.  The same §9 that carries the naming rule fixes the calibration claim's form (`kake-round-56.md:422-423`): "A calibration claim must count
mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state." C1 counts `SKILL.md` cells; it fails that required form.
3.  The r54 sub-axis's own stated surface is published-source meaning: "the lane's self-assessment of the S374 source phrase in
`corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` ... bring the lane's rendered claim into alignment with the retained source"
(`.ufo/waves/round-54/contract.md:8-14`). r55's README map still described corpus files. r56 is the first C1 that leaves that ground for tooling assurance.
4.  What the counter actually does: clone the revision, run the documented command with its `VAR=value` pin, require exit 0 and the printed A/B to
equal the stated integer (`c56_selftally.py:107-126, 154-168, 211-213`). That is `AXES.md:13` verbatim: "A checklist item can be run and produces the
stated outcome".
5.  The r55 verifier routed the stale tallies as an operability-side defect — "their registry rows exist ... though the fixture counts in the rows are
stale (defect 2)" (`round-55-verifier-spotcheck.md:50`) — and routed the fix as defect 1: "Correct `SKILL.md` registry rows 1233–1234 (selftest
fixture counts 35 → 44; 47 → 51 cases + 3 unit checks)" (`:78`).
6.  The contract's own after-state is an operability sentence: "the command runs as documented (including any `VAR=value` pin the row names), and
exits 0 with A == B" (`contract.md`, C1 After). Nothing in it touches SCORECARD or SHONEN.

Consequence the report must carry: the axis declaration (`contract.md:13-15`) names C1 as the deviation from the prompt's operability + freshness
list. Honest labels invert that — C1 *is* the prompt's operability axis (no deviation), and C2 (below) is the deviating claim. Also: if C1 is honestly
operability, no claim works calibration this round, so the lowest-axis obligation is unmet unless the operator rules that the sub-axis now covers
tooling rows. The honest lowest-axis target is already visible: `SCORECARD.md:8-9` says "The numeric ratings below are legacy round-17/18 assessments,
not a fresh proof that the current corpus is clean" — a self-assessment vs repo-state mismatch inside the file `AXES.md` names, unmeasured.

## C2 AXIS:

**Verdict: coverage / expansion, not freshness. The freshness component is one held row (S367) and does not carry the claim.**

1.  The counter has no drift condition. The eight are: C1 entry existence; C2 header shape; C3 registry row shape (incl. "S367 differs from its
base-revision row in `used-by` only"); C4 `used-by` links; C5 quote truth; C6 receipts; C7 census-validated append; C8 mirror append-onlyness
(`c56_quote_truth.py:15-36`). 8 of 8 measures admission fidelity; none can fail because a previously held claim went stale. Three brand-new pages and
three re-verified held claims score identically.
2.  The surface changed is countable and is coverage: knowledge files 49 → 52, registry rows 156 → 158, and the coverage map's own count of per-engine
entries 6 → 9 (`corpus/README.md:130`, rows at `:66-69`). `LEARNING.md`'s expansion observable is "net new admitted entries on uncovered ground, each
`source:` citing a `mined` `corpus/SOURCES.md` row" — the contract's C2 is that sentence.
3.  Not quality either, so §9's "re-scoring a rule the lane already holds on new inputs" does not bite. The three rules are held nowhere: no knowledge
file states a deleted-URL or non-existent-URL recrawl rule, `corpus/knowledge/crawl-error-status-table.md:14` explicitly declines one ("A soft-404
remedy is not claimed from this sentence"), and S367's decision triple (`index,nofollow` / `noindex,nofollow` / `X-Robots-Tag: NOFOLLOW`,
`corpus/SOURCES.md:157`) is stated by no held entry.
4.  The freshness content is one row, real but small: S367 re-fetched 2026-10-25 (HTTP 200, 8051 bytes, sha256
`0188de9dae01e9088231098a9c6af3c8f5dc62a5982419a5f82fd98e86772a19` equal to the round-53 body recorded at
`.ufo/waves/round-53/sources/gate-draft.md:15`) — no drift found.
5.  Label decay, factual: r52 declared "C2 (freshness: three per-engine crawl-hygiene entries on rows opened this round, **plus drift
reconciliation**)" (`corpus/lessons/round-52.md:7`; its SCORECARD row carries the drift number `dangling ids 5 → 0`). r55 declared "C2 freshness
(three Yahoo! JAPAN robots.txt entries ...)" with the drift-reconciliation clause gone (`corpus/lessons/round-55.md:4`), and 2 of its 3 rows were
held. r56 keeps the same three-entry shape with 1 of 3 rows held and no drift number at all.
6.  What the r55 verifier's ruling implies: that ruling is internally split. The same document books the same substance twice — axis table "freshness
(C2) | improved | three new/re-verified entries on rows opened or re-opened this round" (`round-55-verifier-spotcheck.md:49`) and trend table
"expansion: **improved** — three admitted entries on per-engine crawl-hygiene ground that held only the rel=nofollow entry" (`:72`). Copying the axis
half books one move twice and books freshness on a counter that cannot fail for staleness. Its freshness reason also leans on "digests equal live
today", which for a page the lane never held is provenance, not drift. Read carefully, the precedent licenses a split verdict (axis:
coverage/expansion; freshness component: held rows only) — not a freshness axis label for new rows.

## HARM RISKS:

1.  **Operability — new tool rows are outside C1's population.** `POP` is a hard-coded ten-tuple list (`c56_selftally.py:51-63`), `EXPECTED_ROWS = 10`
(`:64`) and the loop reads `rows.get(name)` (`:183`), so an eleventh registry row added this round is invisible. The r55 pattern predicts exactly
that: rows `SKILL.md:1233-1234` are r55's own two counters. If r56 adds rows for `c56_selftally.py`, `c56_quote_truth.py` or `scripts/landed_check.py`
(Maintenance section, considerthese proposal 1), the round closes the stale-tally class on ten rows and can add up to three unchecked rows in the same
commit. Smallest correction: the after-state names every row added this round with the command that prints its tally, and C1's sentence stays "ten
rows in population", not "the registry is accurate".
2.  **Operability — the `tool_changed` guard.** A row whose pinned selftest blob differs from base is a mismatch (`c56_selftally.py:197-199`); a "fix"
that edits a selftest instead of the row exits 1. Correction: rows-only edits, stated in the report so no executor repairs `scripts/*_selftest.py`.
3.  **Freshness — S367's re-opened row records no re-verification.** `corpus/SOURCES.md:157` keeps `status: mined`, `opened: 2026-10-25`, `recheck:
180d`; only `used-by` may move. The no-drift evidence exists only in `sources/receipts.json`, so from the registry alone a later audit cannot tell
"re-verified today, no drift" from "untouched since round 53". Also, r55 routed defect 4's 31-unit span lives in
`.ufo/waves/round-53/sources/gate-draft.md:15`, not in a row cell — re-cutting quotes in the new entry does not remove it. Correction: the axis note
says "fixed in the new entry only; the r53 gate-draft span and the row's cells are unchanged", and names the receipt as the drift record.
4.  **Freshness — premature saturation by relabelling.** Freshness sits at 10/10. Booking "improved" on a counter with no drift condition turns the
axis's observable into "we fetched today", while the freshness content falls 2/3 (r55) → 1/3 (r56). Correction: report `freshness: unchanged (no drift
found on the one held row S367)`; do not book an improvement.
5.  **Calibration — the lane answering its own ownership question.** Scoring calibration 1 → 2 on tooling rows answers r55 routed defect 2 ("Axis
ownership for C1 stays with the operator", `round-55-verifier-spotcheck.md:79`) from inside the lane, and leaves the axis's named surface
(`SCORECARD.md:8-9` legacy ratings) unmeasured. Correction: keep 1/10 until the operator rules, and write the widening criterion into
`corpus/QUALITY.md` before any score move.
6.  **Cross-round gate regression (operability/calibration).** r55's C1 gate requires every knowledge file to be named and described in
`corpus/README.md` §Coverage map (`corpus/QUALITY.md:1146-1153`). Three new knowledge files without three new map rows make `c55_readme_index.py`
print `index_mismatches=3`, i.e. the previous round's gate regresses in the round that adds them. Correction: re-run it after the append and report
the number.

## RECOMMENDED WORDING:

Exact sentences for the report's axis note (replace the contract's "C1 is declared on calibration ... C2 is freshness. No exploratory claim."):

1.  "C1 is declared on calibration, but the surface it changes is the `SKILL.md` gate registry: its counter clones the measured revision, runs each
row's documented command with the pin the row names, and requires exit 0 and a printed tally equal to the stated one — operability's own signal, 'a
checklist item can be run and produces the stated outcome'. C1 is therefore booked on **operability** (10 → 10 HOLD, closing round-55 routed defect
1); the prompt-declared axis list is met by C1, not deviated from."

2.  "Calibration stays at 1/10 this round. The round-54 sub-axis's recorded surface is the lane's rendered claim about a retained source, and the r55
README widening still described corpus files; `SKILL.md` registry tallies are tooling assurance and are not calibration by `AXES.md`'s signal or by
§9's required form (mismatches between SCORECARD/SHONEN and observed repo state). The lowest-axis obligation is therefore **unmet** unless the
operator rules the widening; the lane asks rather than scores."

3.  "C2 is declared on freshness, but its counter has no drift condition — the eight conditions measure entry existence, header shape, registry shape,
`used-by` links, quote truth, receipts, census-validated append and mirror append-onlyness, so 8 of 8 cannot fail because a held claim went stale. The
surface C2 changes is three newly admitted entries (knowledge files 49 → 52, registry rows 156 → 158, per-engine entries in the coverage map 6 → 9):
C2 is booked on **coverage** (expansion: improved), an axis outside this lane's scored ownership, and the operator rules on that ownership."

4.  "C2's freshness component is one held row and is reported as `freshness: unchanged (no drift)`: S367 was re-fetched 2026-10-25 (HTTP 200, 8051
bytes, sha256 `0188de9d…` equal to the round-53 body), and the round-55 defect-4 span is re-cut in the new entry only — the round-53 gate-draft span
and the row's cells are unchanged. Freshness is not booked as improved."

5.  "The round-55 verifier booked the same three-entry shape as freshness in its axis table and as expansion in its trend table; this round books it
once, as expansion, so one move is not counted twice."

VERDICT: C1 is operability (not calibration — the surface is the gate registry's runnable-command claims), C2 is coverage/expansion (not freshness —
no condition in its counter can detect drift; one held row is the whole freshness component); book neither as the frozen contract names them, and
report the lowest-axis obligation as unmet pending the operator's ownership ruling.

