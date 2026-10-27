# Round 61 — lessons (kake)

Round opened 2026-10-27 (attempt 1, L1 `KakeR61`); the round's live fetches and captures run 2026-10-27, so the access date of
every new row, Gate line, `verified-at:` and correction tag is `2026-10-27` (UTC). Base `9f07731a873585e655a6518233ea39f5d9fb8204`
(lane master at round open; the contract commit `eaa9177e` follows it). Contract `.ufo/waves/round-61/contract.md` + `contract.json`,
committed before any seat ran; counters frozen as version 1 by the L1 after wave `w1`, before any after-state is scored. Wave `w1`:
build (`.ufo/waves/round-61/w1/`); wave `w2` falsifies what w1 produced.

Claims, one line each:

- **C1 calibration** — receipt-lineage watch: read-only `scripts/receipt_lineage.py` over committed bytes and the disclosure registry
  `.ufo/receipt-disclosures.json` make an undisclosed receipt rewrite or pending-fill detectable in-lane across the frozen 144-file
  population (`.ufo/waves/round-61/controls/population-144.txt`); counter `.ufo/waves/round-61/c61_lineage_cases.py`, 18 cases
  (L1–L16, R1, R2); predicate `cases_passed == 18 of 18 AND scores_held == 3`.
- **C2 operability** — capability acquisition: GET-only `scripts/response_snapshot.py` captures the 12 round-23 public surfaces'
  response headers, offline `scripts/header_audit.py` audits them against a version-1 manifest of five declared expectation classes;
  counter `c61_header_cases.py`, 18 cases (H1–H18, R3, R4); predicate `cases_passed == 18 of 18`; rows S430–S433 opened this round.
- **C3 freshness** — the ten oldest registry rows S001–S010 re-verified live (fresh GET, retained body with a sha256 receipt, the
  row's anchor quote re-located) and their recheck cells pinned to concrete ISO dates (S001–S007 → 2027-01-17, S008–S010 →
  2027-10-19); counter `c61_recheck_pins.py`, 6 conditions; predicate `conditions_passed == 6 of 6`.

This round declares **no score change**: C1 carries the `scores_held == 3` term (operability 10, freshness 10, calibration 2).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| process/undisclosed-receipt-rewrite | Two rounds rewrote a committed receipt after the fact, and the lane's own gates read the result as if it were the run. r56: `.ufo/waves/round-56/controls/after-c1-selftally.txt` and `after-c2-quote-truth.txt` were added at `4cb225f` carrying `revision: f8438a282d59…`; `ad06cb8` edited that line to `revision: 4cb225fb…` with no re-run, and `controls/c2-selftest.txt` read `67/67` at the revision the report labelled as its measured one, corrected to `86/86` only in `ad06cb8` (both versions read this round from the lane's committed bytes; `round-56-verifier-spotcheck.md` §6 defect 1). r57: `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` was committed at `31b61a4` as `pending` + `revision: 32754df7…` + `EXIT=0` and filled in at `20217f2` (counter line and `tip: 31b61a4d…`), while the round's report said no receipt was rewritten — the exact pattern its own C1 counter forbade (`round-57-verifier-spotcheck.md` §5 D1). considerthese `2026-10-26.md` Part 1 §2 ("the same class kept recurring one level up") and Part 2 proposal 2 name the read. | none: no in-lane rule, counter or relabel duty read a receipt's own history; the class was caught only by the external verifier (r56 defect 1, r57 D1) and by the operator's read. | Claim C1: `scripts/receipt_lineage.py` (first-parent walk over `git cat-file` blobs only, result-span diff, `pending` fill, disclosure schema `kake-receipt-disclosures-v1`, `phantom_disclosure`) + `.ufo/receipt-disclosures.json` + counter `c61_lineage_cases.py`. Ability-to-fail evidence frozen in the contract as cases **L2** (undisclosed rewrite of a `revision:` line → 1 `undisclosed_rewrite`), **L6** (final summary line `met=False`→`met=True`, undisclosed → 1), **L7** (`pending` first version filled later, undisclosed → 1 `undisclosed_pending_filled`), discriminated by L4 (non-result body line only → 0) and L5 (non-receipt population file → 0); do-nothing control R1 = 0/18 at base. State at this writing: tool, disclosures file and counter are absent at lane HEAD `eaa9177e`, so no exit, case count or event number is claimed here. |
| number-drift (R60-D2, EN-unit erratum) | `.ufo/waves/round-60/w1/ScoutRejectCommonJa.md` printed the EN counterpart as 19 whitespace tokens; the lane's own `units()` rule (one unit per CJK character, one per non-CJK whitespace token — `.ufo/waves/round-60/c60_quote_truth.py:120` `CJK_RE`, `:189` `units`) measures that sentence at **22** units, 112 characters, 22 whitespace tokens. Measured this round on the retained EN body `.ufo/waves/round-60/w1/ScoutRejectCommonJa.files/en.html` (sha256 `8f7f1e9b239309edd6f001ac4bc374e52a11a6bc3f2feca7610e066d54e6d664`, 88,970 bytes, committed): one occurrence in the whitespace-collapsed text; the round-60 closure measured 22 independently. | none in-lane; the round-60 closure's non-author spot-check (§4, §6 item 2) measured 22 against the seat's 19. | Correction note only, no claim (contract R60-D2): append-only erratum, the 22-unit measurement stands. The flip stands too — 22 ≤ 25 units and 112 ≤ 160 characters, so re-grounding the rejected Japanese staged entry on the EN edition still passes the quote rule. |
| process/receipt-grammar (R60-D3) | Round-60's T1 receipts carry no `# receipt:` first line while the round's base receipts do (`controls/after-c1-gate-status-t1.txt`; `round-60-verifier-spotcheck.md` §6 item 3). | none mechanically: the header was a convention with no reader, so only a by-eye read could notice it missing. | The contract's receipt rule: a receipt under `.ufo/waves/round-61/controls/` is committed once, after the run it records, never rewritten, a re-run lands under a new name, no placeholder receipt is committed, and every receipt's first line is `# receipt: <name>`; C1's lineage tool recognises `^\s*#\s*receipt\s*:` as one of its three receipt-grammar forms (with `EXIT=` and `^VERDICT:`), so the convention now sits inside a scored surface. |
| process/tool-bytes-not-retained (L1 ruling d; row from SentinelC2Net w1) | C2's 12 capture receipts (`response.json` mtimes 06:15:55–06:16:03 -0300, 2026-10-27) were written by `scripts/response_snapshot.py` at sha256 `eac57099a6e097a28638bc2b7e29ddd3dfd301b34c0caa255d8d708bcb039643`; the file in the worktree is `ba107024c770db194f0b07c806641f1674e109134f62c0eac671e5b06bde1bb7` (mtime 06:17:14). The tool is worktree-only — `git ls-tree HEAD scripts/` has no `response_snapshot.py` and `git log -- scripts/response_snapshot.py` is empty at `eaa9177e…` — so no blob identifies the producing bytes and the pre-edit bytes survive in no artifact. | `none` (no lane rule reads the history of a tool that wrote a receipt); manual capture: SentinelC2Net w1, which proved the delta is confined to the docstring/usage text and the `--overwrite` pre-flight (`Redirects`, `utc_now`, `fetch` through the body cap, `write_file`, `write_json`, `load_population` occur verbatim in the committed file), and that both versions behave identically. | Before a load-bearing run: `sha256sum scripts/<tool>.py` and copy the exact bytes into `<Seat>.files/`, then quote the digest on the capture line of the seat report (round-61 C2 line does this). Where the tool's identity carries a claim, commit it first and cite `git rev-parse HEAD:<path>` instead of a bare sha256. |

Row 4 is a process defect, not a data defect: the 12 receipts are self-consistent and re-verifiable (`len(body.bin)==bytes` and
`sha256(body.bin)==sha256` on 12/12), and the audit's inputs are unaffected; what no artifact proves is that the committed code wrote
them. It is row 1's class applied to a tool rather than a receipt, with the difference that this one was disclosed in prose. Two
halves of the claim are independently re-checkable, and both were re-run for this draft: the pre-edit digest also appears in
`w1/ExecC2Capture.files/run.txt` (an executor-authored source, 1 occurrence), and each stored pre-edit text excerpt (`pre_excerpt.txt`,
2,864 bytes; `pre_excerpt2.txt`, 678 bytes) occurs verbatim in the current tool. Only the producing bytes are unrecoverable.

## Gate

Skeleton: the C2 rows (S430–S433), the C3 ten rows (S001–S010) and the assimilation record are filled from the seat reports named in
`.ufo/waves/round-61/w1/`; `<…>` placeholders are not yet observed by this draft.

Fill rules (contract §Claim C2, §Claim C3, §Frontier step):

- Unit rule: one unit per CJK character, one per non-CJK whitespace token. Every quote 6..25 units and at most 160 characters, a
  substring of one whitespace-collapsed text node of the retained body, page-unique, in ASCII double quotes.
- Anchor rule (round-60 L1 ruling): the line names the nearest heading above the row's quote, and every quote on that line sits in
  that heading's section.
- Provenance on every line: retained body path under `.ufo/waves/round-61/{sources,recheck}/`, its sha256, byte count and HTTP status,
  access date 2026-10-27, fetch userAgent `round61`.
- C3 pin logging (contract rule 2): every recheck-cell change is logged old → new on its line; a non-200, quote-missing or
  fetch-failed row keeps its cadence and carries a Gate note naming the observed state (no pin, no status invention).

C2 rows opened this round (entry `corpus/knowledge/response-header-expectations.md` cites all four):

- S430 — https://www.rfc-editor.org/rfc/rfc6797.html — accessed 2026-10-27 — § `<anchor heading>` — quote: `<6..25-unit span>` (`<n>` units; substring of one collapsed text node, sha256 `<sha256>`, `<bytes>` bytes, HTTP `<status>`) — scope: the HSTS policy field
- S431 — https://www.w3.org/TR/CSP3/ — accessed 2026-10-27 — § `<anchor heading>` — quote: `<6..25-unit span>` (`<n>` units; same retained body, sha256 `<sha256>`, `<bytes>` bytes, HTTP `<status>`) — scope: the CSP field and policy delivery
- S432 — https://fetch.spec.whatwg.org/ — accessed 2026-10-27 — § `<anchor heading>` — quote: `<6..25-unit span>` (`<n>` units; same retained body, sha256 `<sha256>`, `<bytes>` bytes, HTTP `<status>`) — scope: `X-Content-Type-Options` / nosniff
- S433 — https://www.rfc-editor.org/rfc/rfc9110.html — accessed 2026-10-27 — § `<anchor heading>` — quote: `<6..25-unit span>` (`<n>` units; same retained body, sha256 `<sha256>`, `<bytes>` bytes, HTTP `<status>`) — scope: `Content-Type` (§8.3) and field-line semantics; one W04 duplicate-URL note with S088, census exit 0

C3 due rows, ten, pins frozen by the contract (opened 2026-10-19 for all ten; cadence cells read at base):

- S001 — `<URL fetched>` (registry cell carries two raw.githubusercontent URLs) — recheck `on-release` → 2027-01-17 (opened + 90d)
- S002 — `<URL fetched>` (registry cell carries the v4.0.0 and v5.0.0 release URLs) — recheck `on-release` → 2027-01-17 (opened + 90d)
- S003 — `<URL fetched>` — recheck `90d` → 2027-01-17
- S004 — `<URL fetched>` — recheck `90d` → 2027-01-17
- S005 — `<URL fetched>` — recheck `90d` → 2027-01-17
- S006 — `<URL fetched>` — recheck `90d` → 2027-01-17
- S007 — `<URL fetched>` — recheck `90d` → 2027-01-17
- S008 — `<URL fetched>` — recheck `365d` → 2027-10-19
- S009 — `<URL fetched>` — recheck `365d` → 2027-10-19
- S010 — `<URL fetched>` — recheck `365d` → 2027-10-19

Per-row line template (one line per row, filled by the C3 seat reports):

- `- S00N — <URL fetched> — accessed 2026-10-27 — § <anchor heading> — quote: "<span>" (<n> units; substring of one collapsed text node, sha256 <sha256>, <bytes> bytes, HTTP <status>) — recheck <old cell> → <pinned date>`
- unpinned form: `- S00N — <URL fetched> — accessed 2026-10-27 — observed: <status|quote absent|fetch failed> — recheck kept <old cell> (no pin; honest carry)`

Assimilation record (contract §Frontier step, R60-D5):

- Assimilation: none — no staged theme in `merge/kake/` matches the three claims; the quarantine slice was re-derived this round and
  byte-compared to the round-58/59/60 record (12 rows, sha256 `<slice sha256>`, held, nothing appended); the per-row verdicts stay as
  previously recorded and no slice URL was re-opened.
- ADMIT: `<none | staged entry>` — `<grounds>`
- REJECT: `<none | staged entry>` — `<grounds and flip>`

## Carried

- **R60-D4** (C1↔C3 causal coupling, operator routing): carried. C1 this round covers only the round-61 instruments and the disclosure
  registry; C2 and C3 touch neither, so the three claims are isolation-separable at the build. Whether the coupling is admitted stays
  an operator ruling.
- **R60-D5** (quarantine slice of 12 rows held; calibration-ownership L0 rows): carried. The slice is re-verified byte-identical and
  still held, `Assimilation: none` this round, and the L0 calibration-ownership row stays unanswered.
- **R60-D6** (SHONEN boxes all `[~]`; promotion operator-owned): carried. All four boxes stay `[~]` with resolvable pointers;
  promotion is not a lane action.
