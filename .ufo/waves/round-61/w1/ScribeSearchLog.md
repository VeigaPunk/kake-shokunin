# ScribeSearchLog

Seat: leaf scribe, round-61 kake wave w1. Lane `kake-shokunin`, base revision
`9f07731a873585e655a6518233ea39f5d9fb8204`; reads were made from the lane worktree, whose
`git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD` printed
`eaa9177e2965a50fa038d57254934a53909052b6` (read-only; no checkout, no reset, no add/commit, no jj call).
Access date 2026-10-27 (UTC). Deliverable: the CORPUS.md rule-5 search log for the round-61 build,
written to `.ufo/waves/round-61/w1/ScribeSearchLog.files/searchlog.md` (rule 5: question/query, where
searched, date, identified/screened/included/excluded counts, exclusion reasons, stop rationale).

## Behavior

Three bounded searches were run and written up; no live fetch, no clone, no fixture repository, no tool
install was needed, so none was made.

- **(a) receipt-rewrite detection.** Swept `scripts/` (28 code files: 25 `.py`, 3 `.mjs`; `fixtures/`
  and `__pycache__/` excluded) for `lineage`, `rewrit`, `receipt-history`, `receipt_history`,
  `pending_filled`, `undisclosed`, and `corpus/knowledge/` (57 `.md`) for the same terms plus
  `receipt`/`pending`. Result: **no lane script detects a receipt rewrite** (`lineage` 0/28,
  `undisclosed|pending_filled|receipt_history` 0/28; the 6 `rewrit` files concern fixture/scope writes,
  selftest docstrings, host rewrite rules or a grammar rewrite, all read and excluded); knowledge 21/57
  matched, 0 included. Details and the one adjacent committed counter are under `SEARCH LOG: A`.
- **(b) response-header audit.** Same 28 script files for `strict-transport`,
  `content-security-policy`, `x-content-type-options`, `header_audit`, `response_snapshot`, `headers`:
  **0 matches** for the three policy fields and for either tool name; `corpus/knowledge/` and
  `corpus/lessons/` also 0. No lane gate compares recorded headers with declared expectations.
- **(c) considerthese 2026-10-26 proposals 1, 3, 4, 5** read with one-line reasons each (practice change
  with no lane surface; operator-ordering artifact that no counter can fail; bookkeeping over past
  spot-check verdicts that restates R60-D1; a second red-by-design list that duplicates
  `SKILL.md:1273`). Proposal 2 is claim C1 by the contract; not re-argued. Counts: identified 5,
  screened 5, included 1 (already C1), excluded 4.

## SEARCH LOG:

- **A — receipt rewrites.** Question: does a committed lane check already turn an undisclosed rewrite of
  a receipt into a finding? Where: `scripts/`, all of `corpus/knowledge/`, then `SKILL.md`,
  `SCORECARD.md` and `.ufo/waves/round-5*/` (extended once, because the lessons point there). Found: no
  script; but a committed **wave-local** counter, `.ufo/waves/round-57/c57_receipt_pins.py` (870 lines),
  which walks whole ancestry, follows renames, compares each commit with its first parent and counts
  `undisclosed_relabels` against `.ufo/waves/round-57/receipt-errata.json` (6 entries, r52/r55/r56). Its
  population is frozen at `POP_RE = ^\.ufo/waves/round-5[2-7]/(control|controls)/[^/]+\.(txt|json)$`, its
  receipt test is a 40-hex `revision:`/`revision=` line (`REV_RE`), its predicate includes
  `new_receipts == 3 AND scorecard_pin == 1`, and `pending` occurs only in its own fixture bodies
  (lines 526, 532). So it has no `pending_filled` kind, does not cover the round-61 144-file population
  (`.ufo/waves/round-61/controls/population-144.txt`, 144 lines, first entry
  `.ufo/waves/round-37/retained/controls/c2/c2-all-failing.json`), and cannot pass after round 57. It is
  registered as `receipt-pin-counter` at `SKILL.md:1273` with a historical note; `SCORECARD.md:4362`
  and `:4378` carry the round-57 rows. Not found: any receipt-grammar detector (`# receipt:` / `EXIT=`),
  any result-span comparison, any disclosures-with-phantom-check, any handler for
  `member_changed`/`extra_member`. Stop: both scopes swept exhaustively, then one extension to the only
  directory the lessons name; a further sweep cannot change the answer.
- **B — response headers.** Question: does any committed gate audit response headers? Where: `scripts/`,
  `corpus/knowledge/`, `corpus/lessons/`. Found: only single-field `Content-Type` capture in
  `live_snapshot.py` / `source_snapshot.py` and its parse in `receipt_replay.py`. Not found: any use of
  HSTS/CSP/`X-Content-Type-Options`, any expectation-vs-recorded comparison, any field-duplication or
  field-name-syntax check, any `response_snapshot.py`/`header_audit.py`. Stop: the question reduces to a
  name search over the only executable directory plus the knowledge base; zero hits, and the two capture
  tools were read at the lines that touch headers to confirm they only record.
- **C — proposals not taken.** Where: `considerthese/2026-10-26.md` Part 2, against the contract's
  considerthese line. Found: five proposals, one (2) already claim C1. Excluded 1, 3, 4, 5 with the
  reasons above; no proposal was silently dropped. Stop: the list is closed and fully screened.

## COMMANDS:

Searches were issued with the harness `grep` tool (no shell grep for search); inspection and counting
used these shell pipelines, verbatim (all read-only; `cd` prefixes were part of the command):

```
find /home/vgpnk/Projects/shokunin -maxdepth 3 -name 'CORPUS.md' 2>/dev/null; grep -n "^## \|^### \|rule 5\|^5\." /home/vgpnk/Projects/shokunin/CORPUS.md | head -60
cat /home/vgpnk/Projects/shokunin/kake-shokunin/considerthese/2026-10-26.md
cd /home/vgpnk/Projects/shokunin/kake-shokunin && ls .ufo/waves/round-57/ | head -40; echo ---; find .ufo -name '*receipt*' -maxdepth 4 | head -40; echo ---; head -40 scripts/receipt_replay.py
cd /home/vgpnk/Projects/shokunin/kake-shokunin && sed -n '1,80p' .ufo/waves/round-57/c57_receipt_pins.py; echo ===; wc -l .ufo/waves/round-57/c57_receipt_pins.py
cd /home/vgpnk/Projects/shokunin/kake-shokunin && head -c 1200 .ufo/waves/round-57/receipt-errata.json; echo; echo ===; grep -rln "receipt" scripts/*.py | head; echo ===; grep -rn "revision:" scripts/receipt_replay.py | head
cd /home/vgpnk/Projects/shokunin/kake-shokunin && echo "=== scripts rewrit files"; grep -ril 'rewrit' scripts/*.py scripts/*.mjs | sort; echo "--- scripts lineage files"; grep -ril 'lineage' scripts/*.py scripts/*.mjs | wc -l; echo "--- scripts undisclosed files"; grep -ril 'undisclosed\|pending_filled\|receipt_history' scripts/*.py scripts/*.mjs | wc -l; echo "--- knowledge files total"; ls corpus/knowledge/*.md | wc -l; echo "--- knowledge query hits"; grep -ril 'lineage\|rewrit\|receipt-history\|receipt_history\|undisclosed\|pending' corpus/knowledge/*.md | wc -l; echo "--- knowledge receipt+rewrite co-occur"; grep -ril 'receipt' corpus/knowledge/*.md | sort
cd /home/vgpnk/Projects/shokunin/kake-shokunin && grep -n "contentType\|\"headers\"\|header" scripts/live_snapshot.py | head -20; echo "=== inventory"; ls scripts/ | wc -l; ls scripts/ | grep -c '\.py$'; ls scripts/ | grep -c '\.mjs$'; echo "=== knowledge header terms"; grep -ril "strict-transport\|content-security-policy\|x-content-type-options" corpus/knowledge/ corpus/lessons/ | sort | head
cd /home/vgpnk/Projects/shokunin/kake-shokunin && wc -l .ufo/waves/round-61/controls/population-144.txt; head -3 .ufo/waves/round-61/controls/population-144.txt; echo "=== rev"; git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD
cd /home/vgpnk/Projects/shokunin/kake-shokunin && grep -rl "relabel" corpus/lessons/ | sort; echo "=== counts per lesson"; grep -rc "relabel" corpus/lessons/round-56-verifier-spotcheck.md corpus/lessons/round-57-verifier-spotcheck.md 2>/dev/null; echo "=== c57 pop scope"; grep -n "POP_RE =\|REV_RE =\|pending" .ufo/waves/round-57/c57_receipt_pins.py | head -5
cd /home/vgpnk/Projects/shokunin/kake-shokunin && grep -n "rewrit\|relabel\|history\|git cat-file\|undisclosed" corpus/knowledge/receipt-integrity.md | head -20; echo "=== head"; head -8 corpus/knowledge/receipt-integrity.md
mkdir -p /fast/scratch/hyaku/kake-r61/ScribeSearchLog && echo ok
```

Harness `grep` tool calls, verbatim parameters (case-insensitive unless noted):
`pattern=lineage|rewrit|receipt-history|receipt_history|pending_filled|undisclosed`, `path=kake-shokunin/scripts`;
`pattern=lineage|rewrit|receipt-history|receipt_history|undisclosed|pending`, `path=kake-shokunin/corpus/knowledge`;
`pattern=receipt[-_]?(pin|errata)|errata|revision\s*:`, `path=kake-shokunin/scripts`;
`pattern=strict-transport|content-security-policy|x-content-type-options|header_audit|response_snapshot|headers`,
`path=kake-shokunin/scripts`.

## Gates

No gate was run: the counters `c61_lineage_cases.py`, `c61_header_cases.py` and `c61_recheck_pins.py` are
not built yet (this is the build wave), and this seat's item names no measurement. The census, the
build and the quote checks belong to the L1 after integration. Nothing in this report is a score or a
met/unmet verdict.

## Touched surfaces

- Wrote (only): `.ufo/waves/round-61/w1/ScribeSearchLog.md` (this file) and
  `.ufo/waves/round-61/w1/ScribeSearchLog.files/searchlog.md`.
- Scratch `/fast/scratch/hyaku/kake-r61/ScribeSearchLog/` created and removed empty.
- Read-only: lane worktree files listed in COMMANDS; `git rev-parse` only. No lane index, jj state,
  fleet repo, sibling lane or `~/Projects/shokuknow` write; no `git add/commit/stash/checkout/reset/pull/push`;
  no pacman, no install (none needed), no host service touched.

## Findings

1. **Contract-vs-lane conflict, reported verbatim for the canonical judge.** The round-61 contract's C1
   motivation states: "the lane owns no committed check for the class". At the revision I read, the lane
   owns `.ufo/waves/round-57/c57_receipt_pins.py`, a committed whole-ancestry counter for *revision-line
   relabels* over `.ufo/waves/round-5[2-7]/{control,controls}/`, with errata `.ufo/waves/round-57/receipt-errata.json`,
   registered as the `receipt-pin-counter` gate in `SKILL.md:1273` and carried in `SCORECARD.md:4362`/`:4378`.
   What C1 adds over it (population breadth, 144 frozen paths, receipt-grammar detection incl. `EXIT=` and
   `# receipt:`, result-span comparison, `pending_filled`, disclosures with `phantom_disclosure`,
   `member_changed`/`extra_member`) is real; the sentence "the lane owns no committed check for the class"
   is true of `scripts/` and of the 144-file population, and false of the round-57 wave directory.
   [INFERENCE] A w2 reviewer will find this the cheapest attack on the claim's novelty; the contract's own
   wording, not the tool, is what is exposed. I did not edit the contract (out of a leaf's scope).
2. **C2 surface is unoccupied.** No script and no knowledge entry mentions HSTS, CSP or
   `X-Content-Type-Options` (0/28 scripts, 0/57 knowledge files, 0 lessons). The two snapshot tools store
   one header field for other purposes; `redirect_audit.py` is about redirect/rewrite decisions.
   [INFERENCE] `scripts/header_audit.py` therefore cannot collide with an existing gate, and its
   `could_not_evaluate`/`singleton_fields` classes have no in-lane precedent to copy.
3. **C1's population is broader than any pre-existing list.** `population-144.txt` has 144 lines and
   starts at `.ufo/waves/round-37/retained/controls/c2/…`; the round-57 counter's regex covers only rounds
   52–57. [INFERENCE] That breadth is where `member_changed`/`extra_member` earn their keep — no existing
   instrument froze a path list at that scope — and c57's predicate (`new_receipts == 3 AND
   scorecard_pin == 1`) is round-57 state that cannot be reused; `SKILL.md:1273` already marks it red by
   design on later trees.
4. No credential, token, `op://` ref or private URL was read or written; the search note carries none.

## Out of scope (not done, by item)

- No counter, tool, capture, registry row, lesson, knowledge entry, SHONEN box, SCORECARD cell or
  contract file was written or changed; no `scripts/` change; no gate or selftest run.
- No subagent was dispatched (leaf seat); no live fetch; no fixture repo; no pacman, no install.
- Proposals 1, 3, 4, 5 were recorded as read and not taken, not implemented.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/w1/ScribeSearchLog.md` (this report)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/w1/ScribeSearchLog.files/searchlog.md`
  (rule-5 draft: searches A, B, C with counts, exclusion reasons and stop rationales)
- Read-only evidence: `.ufo/waves/round-57/c57_receipt_pins.py`, `.ufo/waves/round-57/receipt-errata.json`,
  `SKILL.md:1273`, `SCORECARD.md:4362,4378`, `scripts/live_snapshot.py:81,85,97`,
  `scripts/source_snapshot.py:199`, `scripts/base_path_audit.py:28`, `scripts/canonical_audit.py:5`,
  `corpus/knowledge/receipt-integrity.md`, `.ufo/waves/round-61/controls/population-144.txt`,
  `considerthese/2026-10-26.md`, `/home/vgpnk/Projects/shokunin/CORPUS.md:126` (all lane-relative unless
  absolute).

VERDICT: Search log drafted (three bounded notes, counts and stop rationales); no lane script detects receipt rewrites and no gate audits response headers; one contract-vs-lane conflict (round-57 relabel counter) reported for the judge; no gate run, no mutation.
