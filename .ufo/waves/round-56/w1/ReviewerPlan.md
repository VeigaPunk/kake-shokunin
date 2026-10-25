# ReviewerPlan

Review of the W1 assimilation plan (43 seats in `w1-spec.json`) against §10 of the round prompt
(`kake-round-56.md` L440–545), `contract.md`, and the staged evidence under
`.ufo/waves/round-56/assimilation/`. All recomputations below were run read-only this round.

CHECKLIST:

1. id lists + collision count recorded — **met.** My recomputation with the required pattern
   (`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort`) is byte-identical
   to `assimilation/reg-ids` (156) and `assimilation/staged-ids` (129); `comm -12` gives exactly the
   8 recorded collisions: S312 S329 S367 S372 S373 S374 S390 S409. ExecIdGuard is dispatched to
   re-replicate this byte-for-byte (redundant coverage, no harm).
2. Collision = same document — **met.** URL cells of all 8 colliding ids are identical lane-vs-staged
   (S312/S329/S390/S409 baidu ziyuan; S367 002852; S372 002849; S373 002850; S374 002851). Renumbering
   is therefore needed only for *adopted* staged ids.
3. Renumber map by document — **met.** Staged S375 → lane S419 (both = `archives/002856.php`);
   staged S376 → lane S420 (both = `archives/002857.php`); staged S367 → held lane S367 (same doc,
   002852). Lane next free id is S419 (max S418). Dispatch names the three `archives/` URLs; id follows
   the document, no arithmetic.
4. Guard proof — **met.** `assimilation/guard-proof/` is absent under round-56 because the contract
   says wave 1 re-proves it; ExecIdGuard's prompt carries the exact indented-row fixture
   (`  | S287 | x |`) and requires the 0–3-space pattern to catch S287 while a column-zero-only
   pattern reports nothing, saved under `.files/`. Semantics preserved.
5. No row appended that no admitted entry cites — **met.** ExecRowDryRun appends exactly S419 + S420
   and only *extends* S367's `used-by`; no staged bulk append anywhere in the spec (also consistent
   with CorpUS rule 4).
6. Normalized recheck cell — **met.** Staged S375/S376 rows carry campaign cells
   `180d — \`curl … \| grep …\`` (13 fields when split on `|`). Dry-run plan normalizes to `180d`
   (the S418 convention: `| mined | 2026-10-25 | 180d |`); the stripped command lands in the entry's
   `recheck:` line (`curl -fsSL '<url>' | grep -F -c '<quote>'`, run against the retained body).
   Residual: L1 must record the stripped prose in the lesson's Gate block — see GAPS g2.
7. No pipe in cells — **met.** Staged rows contain literal escaped pipes (`grep -c '\\|'` = 104 in
   SOURCES.append.md, incl. S375/S376 recheck commands). The dry-run prompt states "no pipe inside any
   cell"; EntryDeletedUrl requires the row to parse as 11 cells vs the S418 shape.
8. `opened`/`status` normalization — **met.** Staged `opened` = 2026-10-24 (campaign fetch date);
   plan writes `2026-10-25` (the lane's own re-open date). `status=mined` kept.
9. used-by lists exactly the admitted entries — **met, with a rename caveat.** Staged S376 used-by =
   `corpus/knowledge/yahoo-japan-soft-404-recrawl.md`, but the entry lands as
   `yahoo-japan-nonexistent-url-recrawl.md` (the page never says "soft 404"; EntryNonexistentUrl is
   instructed accordingly). L1 must point S420's used-by at the *landed* path, not the staged one —
   GAPS g1.
10. Scratch census validation before append — **met.** `assimilation/pre-append/corpus/SOURCES.md`
    sha256 (cc402e4b…) equals `git show e48354b7:corpus/SOURCES.md`; `mirror-pin.json` records
    sourceRevision, 156 rows, adoptedAbsent [S419,S420]. `validate_append.sh` mirrors the whole
    working `corpus/` + used-by targets and gates on
    `sources-census.sh validate --file $V/corpus/SOURCES.md` (exit recorded in `census-exit.txt`).
    ExecRowDryRun exercises the same gate in scratch plus 3 deliberate breaks (dup id, 10-cell row,
    dangling used-by).
11. Quarantine slice derived, not adopted — **met.** `assimilation/quarantine-slice` byte-matches my
    re-derivation of the kake slice from `absent-defect-register.md`: 12 rows (9 `payload-absent`,
    3 "could not be fetched" = unverifiable class). Contract: "not adopted, not hand-checked this
    round"; no seat appends a quarantined row.
12. ≥1 admit + ≥1 reject for non-author spot-check — **met.** Admits: the three entry scribes produce
    GATE LINEs. Rejects: ScoutRejectCanonical (S388/003036), ScoutRejectRedirect (S389/002865),
    ScoutRejectDynamic (S387/002867) — retained reject-evidence bodies exist in `sources/` with
    receipts — each instructed to decide ADMIT/REJECT on merit and name the flip condition, which is
    exactly the S364-class refusal shape round 55 recorded. (The three are out-of-theme by the
    one-theme rule regardless of merit.)
13. Gate quote rules (URL + access date + ≤25-unit located quote per new row) — **met.** The
    GATE LINE template is literal in each scribe prompt:
    `- S4NN — <url> — accessed 2026-10-25 — § <heading> (更新日 <date>) — quote: "<6–25 units,
    page-unique>" (<n> units; raw substring of the retained body, sha256 <receipts.json>, <bytes>,
    HTTP 200)` — matches the round-55 Gate block format. `span_tools.py` enforces page-unique,
    ≤25-unit, raw-substring quotes.
14. `doctrine/` not used as corpus — **met.** No W1 prompt references `doctrine/` at all.
15. MERGE-REPORT.md consulted — **met (planner-side).** The contract ledger and every dispatch name
    the staged candidates by their MERGE-REPORT titles (`yahoo-japan-deleted-url-recrawl` round11,
    `yahoo-japan-soft-404-recrawl` round11, `yahoo-japan-link-target-crawl-restriction` round10;
    rejects round13). No *seat* is assigned to re-read MERGE-REPORT.md itself — acceptable since the
    consultation happened at planning; not required in any seat prompt.
16. One theme / 1–3 entries — **met.** Single theme (Yahoo! JAPAN crawl handling); 3 entries adopted
    (≤3). Reject seats must state merit separately from the theme limit.
17. PROVINCE scope — **met.** ScoutScopeOverlap checks each candidate against PROVINCE.md
    (publisher-side/per-engine crawl hygiene = Frontier; refuse sibling-domain material) and produces
    per-candidate admit/refuse + flip conditions.
18. Frozen claims untouched — **met.** Contract §10's "never rewrites a frozen claim": no W1 seat
    edits the predicates/counters; ExecBaseControls only *replicates* the frozen base controls in a
    clone.
19. Considerthese — **met.** Exactly one proposal taken (ExecLandedCheck, proposal 1, landed-vs-
    claimed); contract says proposals 2–3 not taken — matches "at most one per round".

GAPS:

g1. **S420 used-by rename is the one place the plan can silently go stale.** Staged S376's used-by
    names `yahoo-japan-soft-404-recrawl.md`; the landed file is `yahoo-japan-nonexistent-url-recrawl.md`.
    The dry-run prompt already names the landed path — the L1 must not copy the staged used-by cell
    verbatim, and must verify `ls corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` resolves
    before append (ExecRowDryRun creates only scratch placeholders, so this check is real, not cosmetic).
g2. **Gate-block assembly has no seat.** GATE LINEs arrive per-scribe and reject DECISIONs per-scout,
    but `lessons/round-56.md` ## Gate is L1-written. L1 must (a) compose the 3 admit lines + ≥1 reject
    with reason+flip, and (b) record the stripped staged recheck prose there (§10 requires it; the
    normalized row holds only `180d`). Round-55's lesson (lines 10–45) is the template to copy.
g3. **`assimilation/guard-proof/` will not exist until ExecIdGuard lands** — expected, but the L1
    should save ExecIdGuard's `.files/` fixture+outputs into `assimilation/` (or cite the report) so
    the guard proof survives as wave evidence, not just a report claim.
g4. EntryLinkTarget must not cite staged-claimed ids S192/S199/S200/S201 (instructed: cite only ids in
    `corpus/SOURCES.md` — S374 + S367). This is prompt-covered; flagged because staged cross-references
    were a round-55 defect class.

ORDER OF OPERATIONS (the sequence the L1 must follow):

1. **Guard re-proof (wave evidence, before first append).** Collect ExecIdGuard's COMMANDS/COMPARISON/
   GUARD PROOF/SAME-DOCUMENT TABLE/NEXT ID; independently re-run, in scratch:
   `S=/home/vgpnk/Projects/shokuknow; A=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-56/assimilation`
   `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"`
   `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/kake/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"`
   `comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"` — must equal the recorded files (156/129/8).
   Then the scratch fixture `  | S287 | x |` must produce nonempty collisions under the 0-3-space
   pattern and empty under column-zero-only; if not, guard is broken → adopt nothing this round.
2. **Scratch append dry-run, before any real edit** (ExecRowDryRun): mirror
   `assimilation/pre-append/corpus/SOURCES.md` + the files `validate_append.sh` copies into `$S`,
   append normalized S419/S420 rows + extend S367 used-by, create placeholder used-by files, run
   `sources-census.sh validate --file $S/corpus/SOURCES.md` → exit 0, plus the 3 intentional breaks.
3. **Collect build inputs:** the three ENTRY + REGISTRY ROW + GATE LINE + COVERAGE ROW outputs;
   the three ScoutReject DECISIONs (merit + flip); ScoutScopeOverlap admit/refuse per candidate;
   ReviewerStaged reuse-vs-redraft verdicts.
4. **Normalize the two new rows (do not copy staged cells verbatim):** 11 cells; S419 (S375 doc,
   002856) and S420 (S376 doc, 002857); `opened`=2026-10-25; `recheck`=180d (move the `curl | grep`
   command into the entry's `recheck:` line and the stripped prose into the lesson's Gate block);
   `status`=mined; `used-by` = the *landed* entry paths — S420's is
   `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md`, NOT the staged `…soft-404…` name;
   no literal `\|` or `|` inside any cell. S367: only append the link-target entry path to its
   `used-by` cell; touch no other cell.
5. **Land the three entry files** at `corpus/knowledge/` verbatim from the scribe ENTRY blocks, then
   `ls` each used-by path (files must exist before the census mirror — the census checks used-by
   existence).
6. **Pre-append mirror validation — hard gate:**
   `bash .ufo/waves/round-56/validate_append.sh` → `census-exit.txt` must read `exit=0` BEFORE the real
   registry edit. Any E03/E04 (duplicate id / within-scope duplicate URL) → refuse or supersede that
   row per CORPUS.md rule 2; never append past it.
7. **Real edits:** append S419/S420 to `corpus/SOURCES.md`; extend S367 `used-by`; write the README
   coverage-map rows (after entry files exist — ScribeGroundMap's ORDERING note: the r55 readme index
   counter treats pointers as dangling otherwise) and the Frontier ground map; write
   `corpus/lessons/round-56.md` with the ## Gate block (admits + rejects + stripped recheck prose +
   mined mistake + census before/after).
8. **Round-end census (contract requirement):**
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0.
9. **Then** run the C1/C2 counters and `landed_check.py` on the round report; do not append any
   quarantined row (S142/S143/S148/S154/S156/S161/S178/S184/S193/S194/S195/S206) this round.

VERDICT: plan satisfies every §10 checklist item — id lists/collisions/quarantine/mirror-pin verified
byte-exact against recomputation; the only real gaps are the S420 used-by rename and the un-seated
Gate-block assembly, both owned by the L1 in the order above.
