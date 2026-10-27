# Kake round 61 — contract (predicates declared before any data)

Lane: kake-shokunin. Base revision (lane master tip at round open, the round-60 non-author spot-check):
`9f07731a873585e655a6518233ea39f5d9fb8204`. Round opened 2026-10-27 (attempt 1, L1 `KakeR61`). The round's
live source fetches and captures run 2026-10-27, so the **access date** of every new row, Gate line,
`verified-at:` and correction tag is `2026-10-27` (UTC). This file and `contract.json` are committed before
any wave seat is dispatched and before any counter scores anything. The predicate sentence of each claim below
is the sentence the counter's code carries (`PREDICATE`) and every receipt label repeats.

Round shape: two v1 waves — `w1` build (tools, counters, captures, entries, rows, recon, first falsifiers;
32–64 seats) and `w2` falsify (fresh reviewer/critic/mutation-tester/sentinel/scout seats on what w1 produced;
32–64), round total 64–128, plus at most one residual call of ≤8 reviewer/critic seats. The counters are written
by wave-1 seats to the conditions frozen here, integrated by the L1, frozen as version 1 with their base controls
**before any after-state is scored**; wave 2 attacks version 1; a version 2 may only tighten (every loosening is
named in § Counter versions). The L1 holds the canonical §3 planner seat (the validator rejects `planner`).
Seats are read-only except their own report and `<Seat>.files/` directory.

Receipt rule (round 58, kept): a receipt under `.ufo/waves/round-61/controls/` is committed once, after the run
it records, and never rewritten; a re-run lands under a new name. No placeholder receipt is committed. Every
receipt carries a first line `# receipt: <name>` (round-60 spot-check nit 3).

## Routed defects of the round-60 spot-check (`corpus/lessons/round-60-verifier-spotcheck.md` §6)

- **R60-D1** ("three relabels" count vs 2 relabels + 1 pin move) → process note only; this round's report keeps
  relabel counts and named rows consistent.
- **R60-D2** (EN counterpart quote printed as 19 units; the lane's own `units()` measures 22) → an erratum note
  lands in the round-61 lesson (append-only to the record, no claim); the 22-unit measurement stands.
- **R60-D3** (T1 receipts lacked the `# receipt:` header) → the receipt rule above; C1's lineage tool recognises
  the header as one receipt-grammar form.
- **R60-D4** (C1↔C3 causal coupling, operator routing) → carried; C1 this round covers only the round-61
  instruments and the disclosure registry, C2/C3 touch neither, so the three claims are isolation-separable at
  the build.
- **R60-D5** (quarantine slice 12 rows held; calibration-ownership L0 rows) → quarantine re-verified
  byte-identical, still held; `Assimilation: none` this round (no staged theme matches the claims; the slice
  stays operator-held).
- **R60-D6** (SHONEN boxes all `[~]`; promotion operator-owned) → carried; boxes stay `[~]` with pointers.

## Axis declaration

Prompt-declared lane axes: operability + freshness; the scorecard also carries the round-54 bounded sub-axis
**calibration** (score 2, lowest non-retired), so the lowest-axis obligation lands on C1 (ownership still open
for the operator, L0 row of round 59). Three claims on three distinct axes: C1 calibration, C2 operability
(capability acquisition), C3 freshness (sourced via the C2 rows and its own re-opened rows). No exploratory
claim. This round declares **no score change**: the C1 counter carries a `scores_held == 3` term (operability
10, freshness 10, calibration 2) shown able to fail by a score-only mutant, per R59-D2.

Causal separability: C1 reads only git history of `.ufo/waves/*/control*/` files, `scripts/receipt_lineage.py`,
`.ufo/receipt-disclosures.json`, `SKILL.md`/`SCORECARD.md`; C2 reads only `scripts/response_snapshot.py`,
`scripts/header_audit.py`, the round-61 capture under `.ufo/waves/round-61/capture/`, the manifest and the new
registry rows; C3 reads only `corpus/SOURCES.md` recheck cells of S001–S010, the retained re-open bodies under
`.ufo/waves/round-61/recheck/` and the lesson Gate. C2 appends registry rows; C3 changes recheck cells in place;
neither touches C1's surface.

## Claim C1 — calibration: receipt-lineage watch (undisclosed receipt rewrites become detectable in-lane)

Motivation (considerthese `2026-10-26.md` proposal 2): rounds 56 and 57 each rewrote a committed receipt after
the fact — r56 relabelled a receipt's `revision:` line in a later commit; r57 committed a `pending` receipt and
filled it in later — and only the external verifier caught either. The lane owns no committed check for the
class. A fix counts only once shown able to fail.

Surface: every receipt file committed at the measured revision under `.ufo/waves/round-<N>/control/` or
`.ufo/waves/round-<N>/controls/` (either spelling; files only in those directories, any depth of round number,
`.txt` or `.json` extension) — the population is frozen by path list in the counter at base (144 files at
`9f07731a`, enumerated in `.ufo/waves/round-61/controls/population-144.txt`, committed before any seat runs;
`members` counts frozen paths present unchanged at the measured revision; a population file changed or missing →
`member_changed`/`member_missing`; a new file matching the path rule outside the frozen list → `extra_member`).

Tool: `scripts/receipt_lineage.py` (new; read-only; stdlib Python; committed bytes only via `git cat-file` /
`git rev-list` / `git ls-tree`, never the worktree; inherited `GIT_*` scrubbed; `--root` must be a repository
toplevel). CLI: `python3 -B scripts/receipt_lineage.py --root <lane> --revision <rev> [--disclosures <path>]
[--json]`, plus `--selftest`. Default disclosures path: `.ufo/receipt-disclosures.json`. Exits: 0 clean, 1
findings, 2 could-not-evaluate (revision unresolved, root not a toplevel), 64 usage. One finding per line
`<kind> <path> <commit>`, then a summary line `receipts=<n> events=<k> undisclosed=<m> met=<bool>`.

Rules:
- **receipt detection**: a population file whose FIRST committed version (base..revision first-parent history)
  carries a receipt grammar line — a line matching `(?im)^\s*#\s*receipt\s*:` OR `EXIT=` OR `^VERDICT:` — is a
  receipt. Other population files are never findings even when rewritten.
- **history walk**: for each receipt, every first-parent commit C (after the commit that first added the file,
  through the revision under test) whose tree holds a different blob for the path than C's first parent is an
  event candidate. Renames are followed by exact path only (a rename ends the history; the new path is its own
  first-added commit).
- **result span**: the set of lines of a version matching `(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)`.
- **rewrite event**: an event candidate where the result span of the child's version differs from the parent's.
  Kind `rewrite`.
- **pending-fill event**: the first committed version's result span contains the literal word `pending`
  (case-insensitive) and a later version's result span does not → kind `pending_filled` at that later commit.
- **disclosure**: a rewrite/pending_filled event is disclosed when the disclosures JSON (schema
  `kake-receipt-disclosures-v1`, a `{"entries": [{path, commit, kind, note, disclosed-by}]}` object) holds an
  entry with equal `path` and `commit`. An undisclosed event is a finding (`undisclosed_rewrite` /
  `undisclosed_pending_filled`). Malformed disclosures JSON → exit 2. A disclosures entry for a non-event
  (path,commit) → finding `phantom_disclosure`.
- **met** (tool): `undisclosed == 0` over the walked range.

Counter: `python3 -B .ufo/waves/round-61/c61_lineage_cases.py --root <lane> --revision <rev> [--work <scratch>] [--seed N] [--json]`.
The counter runs the tool **as committed at the revision** over gate-built fixture repositories (each `git init`
in its own scratch dir, ids drawn from the seed so a fixture-keyed tool cannot recognise them) and over the real
lane. 16 fixture cases + 2 real-lane cases:

| id | fixture (population file history) | expected |
|---|---|---|
| L1 | receipt created clean; never touched | 0 |
| L2 | receipt created; later commit rewrites its `revision:` line, undisclosed | 1 `undisclosed_rewrite` |
| L3 | same rewrite, disclosed by entry (path,commit) | 0 |
| L4 | later commit rewrites a NON-result body line only | 0 |
| L5 | non-receipt population file rewritten freely | 0 |
| L6 | receipt's final summary line changed (`met=False`→`met=True`), undisclosed | 1 `undisclosed_rewrite` |
| L7 | first version contains `pending`, later commit fills the result, undisclosed | 1 `undisclosed_pending_filled` |
| L8 | same fill, disclosed | 0 |
| L9 | two sequential rewrites, one disclosed, one not | 1 `undisclosed_rewrite` |
| L10 | population file changed to a different blob at the measured revision vs the frozen base list (member mutation) | 1 `member_changed` (counter-level, not tool) |
| L11 | new population-path file appears at the measured revision outside the frozen list | 1 `extra_member` |
| L12 | disclosures JSON malformed | tool exit 2 |
| L13 | disclosures entry names a (path,commit) with no event | 1 `phantom_disclosure` |
| L14 | receipt rewritten only in a commit AFTER the revision under test (range bound) | 0 |
| L15 | `--revision` not an ancestor tip / unresolved | 2 |
| L16 | empty population directory | 0 `receipts=0` |
| R1 | real lane at base: tool absent → every case fails | 0/18 |
| R2 | real lane at the measured revision: `receipts=144 events=<k> undisclosed=0`, exit 0 | met |

- Predicate (frozen): **met: cases_passed == 18 of 18 AND scores_held == 3**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable (revision unresolved, clone failure, counter internal
  error); 64 usage.
- Do-nothing control: base (no tool) → 0/18. Counter selftest controls (before data): no tool, always-clean
  (prints `met=True` everywhere), always-exit-1, fixture-sniffing composite.
- What the counter does not test: whether a disclosed note's prose is truthful (reviewer-checked); whether the
  population regex misses a receipt shape no lane round ever used (scout-checked); symlinks/submodules in the
  population path (a non-blob population path is skipped with a named note).

## Claim C2 — operability (capability acquisition): offline response-header expectation audit

Surface: the response headers a publisher's served pages return. Two new tools:
- `scripts/response_snapshot.py` — GET-only capture of the 12 named public surfaces (the round-23 population,
  `.ufo/waves/round-23/live/` ids) writing per-surface `response.json` under
  `.ufo/waves/round-61/capture/<id>/`: final status, finalUrl, ordered header name/value pairs (duplicates
  preserved), body sha256, bytes, fetchedAt, userAgent tagged `round61`. Constraints identical in spirit to
  `scripts/live_snapshot.py`: no cookies, credentials or request body; at most 5 redirects, 20 s, 2 MiB; one
  GET per surface. Capture is input preparation and is claimed only as "ran with these receipts"; nothing in the
  claim depends on any surface being up.
- `scripts/header_audit.py` — reads a version-1 manifest of recorded responses plus declared expectations and
  reports, read-only and network-free, each check whose recorded headers violate an expectation class (clean /
  failed-policy / could-not-evaluate per check; exits 0/1/2/64; one finding per line
  `<check-id> <class> <detail>`, then `checks=<n> findings=<k>`; `--selftest`).

Manifest v1 (frozen shape): `{"version": 1, "checks": [{"id", "source" (capture receipt path), "url", "https": bool,
"expect": {"content_type_present": bool, "hsts_present": bool, "xcto_nosniff_value": bool, "csp_present": bool,
"singleton_fields": [names]}}]}`. Expectation classes (each grounded in a row opened this round; the entry
carries the located quotes):
- `content_type_present`: a recorded 2xx response whose headers carry no `Content-Type` field → finding (RFC 9110
  §8.3 semantics row).
- `hsts_present`: a check with `"https": true` and `"hsts_present": true` whose recorded headers carry no
  `Strict-Transport-Security` → finding (RFC 6797 row: the HSTS policy is conveyed in that field).
- `xcto_nosniff_value`: a recorded `X-Content-Type-Options` field whose value is not exactly `nosniff` → finding
  (WHATWG fetch / MDN row).
- `csp_present`: a check with `"csp_present": true` whose recorded headers carry no `Content-Security-Policy` →
  finding (W3C CSP Level 3 REC row).
- `singleton_fields`: a field name listed in the check's `singleton_fields` occurring more than once (case-
  insensitive) in the recorded headers → finding (RFC 9110 field-lines row; `Set-Cookie` is never a singleton).
- A check whose source receipt is missing/malformed, or whose recorded status is not parseable →
  `could_not_evaluate` for that check (manifest fault → exit 2 only when NO check is evaluable).
- Header names are matched case-insensitively; values are compared after trimming OWS; the audit never fetches.

Counter: `python3 -B .ufo/waves/round-61/c61_header_cases.py --root <lane> --revision <rev> [--work <scratch>] [--seed N] [--json]`.
The counter runs the audit tool as committed at the revision over gate-built fixture manifests (seeded ids) and
over the real manifest. 18 fixture cases:

| id | fixture manifest | expected |
|---|---|---|
| H1 | 200 with `Content-Type: text/html` and all expected headers present | 0 |
| H2 | 200 with no `Content-Type` | 1 `content_type_present` |
| H3 | https check, `hsts_present: true`, no `Strict-Transport-Security` header | 1 `hsts_present` |
| H4 | HSTS present with parameters (`max-age=31536000; includeSubDomains`) | 0 |
| H5 | `X-Content-Type-Options: nosniff` correct | 0 |
| H6 | `X-Content-Type-Options: NOsniff ` (case + OWS) | 0 |
| H7 | `X-Content-Type-Options: sniff` | 1 `xcto_nosniff_value` |
| H8 | `csp_present: true`, no CSP header | 1 `csp_present` |
| H9 | two `Content-Type` headers in one recorded response, singleton list includes content-type | 1 `singleton_fields` |
| H10 | two `Set-Cookie` headers, singleton list includes set-cookie | 0 (Set-Cookie never a singleton) |
| H11 | 404 recorded response, no Content-Type | 0 (content_type_present applies to 2xx only) |
| H12 | header-name syntax fault in a recorded response (`X Bad Name: v`) | 1 `field_name_syntax` |
| H13 | check whose source receipt file is missing | per-check `could_not_evaluate`, exit 1 with 0 policy findings |
| H14 | manifest version != 1 | 2 |
| H15 | manifest not parseable JSON | 2 |
| H16 | every expectation declared false/absent, clean headers | 0 |
| H17 | header value with leading/trailing whitespace only | 0 |
| H18 | empty checks array | 0 `checks=0 findings=0` |
| R3 | real manifest built from the round-61 capture: audit runs, `checks=12 findings=<k>` exit 0 iff k==0 else 1 — recorded, not asserted clean |
| R4 | do-nothing: audit absent at base | 0/18 |

- Predicate (frozen): **met: cases_passed == 18 of 18** (H-fixtures plus R3's run-recorded shape check: the real
  manifest has exactly 12 checks, each bound to an existing capture receipt; R3's verdict value itself is NOT
  asserted — a non-clean live census is reported, not a failure of the claim).
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: base → 0/18 (no tool). Counter selftest controls: no tool, always-clean, always-exit-1,
  manifest-sniffing composite.
- What the counter does not test: whether the expectation classes are the right publisher policy (critic-checked);
  whether the capture itself is honest (capture receipts are sha256-pinned and re-readable; sentinel-checked);
  live serving at any moment (the audit is offline by construction).

Sources (all opened 2026-10-27 with retained bodies + sha256 receipts under `.ufo/waves/round-61/sources/`):
- **S430** = RFC 6797 HTTP Strict Transport Security — `https://www.rfc-editor.org/rfc/rfc6790`… the canonical
  `https://www.rfc-editor.org/rfc/rfc6797.html` (tier A for the HSTS scope).
- **S431** = W3C Content Security Policy Level 3 — `https://www.w3.org/TR/CSP3/` (tier A for the CSP scope).
- **S432** = WHATWG Fetch — `https://fetch.spec.whatwg.org/` (tier A for the `X-Content-Type-Options`/nosniff
  scope).
- **S433** = RFC 9110 HTTP Semantics — `https://www.rfc-editor.org/rfc/rfc9110.html` (tier A for the Content-Type
  and field-line semantics scopes; adds one W04 duplicate-URL-across-scopes note with the existing S088 row —
  census stays exit 0).
Entry: `corpus/knowledge/response-header-expectations.md` citing S430–S433. Rows append-only; `used-by` names the
entry. Capability row enters `SCORECARD.md` only on the demonstrated run.

## Claim C3 — freshness (sourced): the ten oldest registry rows re-verified live and their recheck cadences pinned to concrete dates

Surface: `corpus/SOURCES.md` recheck cells. Due set (frozen at base by rule — non-rejected rows with the oldest
`opened` date, ties by lowest id): **S001, S002, S003, S004, S005, S006, S007, S008, S009, S010** (all opened
2026-10-19; 16 ties, lowest 10 taken).
- For each due row: one fresh GET of the row's URL (retained body + receipt: sha256, bytes, HTTP 200, fetchedAt on
  the access date, userAgent `round61`) under `.ufo/waves/round-61/recheck/`; the row's Gate/anchor quote re-located
  in the fresh body (source-recheck semantics; quote truth, not a new crawl).
- Pin rule: when the fetch is HTTP 200 and the anchor quote still occurs, the recheck cell moves from its cadence to
  the concrete ISO date `opened + cadence` for `Nd` cadences (S003–S007 → 2027-01-17; S008–S010 → 2027-10-19); for
  non-`Nd` cadences (`on-release`, `on-use`) the pin is `opened + 90d` (S001, S002 → 2027-01-17). Each change is
  logged old→new in the round-61 lesson `## Gate` (contract rule 2).
- Non-200, quote-missing or fetch-failed rows keep their cadence and carry a Gate note naming the observed state
  (honest carry; no date pin, no status invention).
Counter: `python3 -B .ufo/waves/round-61/c61_recheck_pins.py --root <lane> --revision <rev> [--json]` (offline;
committed bytes only). Conditions:
- C1: the due-set rule re-derived at the measured revision yields exactly the frozen ten ids (rows present,
  non-rejected, opened 2026-10-19, lowest 10 by id).
- C2: for each pinned row the recheck cell is a concrete ISO date, `opened < pinned ≤ opened + cadence` for `Nd`
  cadences at base, or `= opened + 90d` for the two non-`Nd` rows.
- C3: each pinned row has a lesson Gate line carrying its URL, the access date, and one double-quoted span
  (6..25 whitespace units, ≤160 chars, ASCII) that occurs in the row's retained fresh body (sha256-pinned).
- C4: each retained body has a receipt pinning sha256, bytes, HTTP 200, fetchedAt on the access date, userAgent
  `round61`, receipt URL = row URL; every sha256 matches the committed blob.
- C5: an unpinned due row has a Gate note naming the observed state; there is no pinned row without a Gate line.
- C6: rows not in the due set are byte-identical to base (append-only registry outside the recheck-cell changes).
- Predicate (frozen): **met: conditions_passed == 6 of 6**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: base → C2 fails (0 concrete dates). Constant control (all dates rewritten but no receipts) →
  C3/C4 fail.
- What the counter does not test: that the fresh body is semantically the same page beyond the located quote
  (reviewer-checked); that ten rows is the right sweep width (a maintenance sizing choice, recorded).

## Frontier step and assimilation (inside the claim cap)

Census at round start: exit 0, 167 rows, 15 W04 (`controls/census-before.txt` + `.exit`, committed before any
seat runs). Census at round end must be exit 0. New rows: S430–S433 (C2), each with lesson Gate lines (URL, access
date, ≤25-unit located quote). C3 changes ten recheck cells in place, old→new logged in the lesson. Mistake mined:
the undisclosed receipt-rewrite class (r56/r57; captured-by `none` — only the external verifier caught it; fix:
claim C1, shown able to fail by cases L2/L6/L7). Sourced claim: C2 rests on rows opened this round. Quarantine
slice: re-derived this round (12 rows, byte-identical to the round-58/59/60 record), still held — nothing appended.
Assimilation: none. Considerthese: proposal 2 (receipt-rewrite watch) is claim C1; proposals 1/3/4/5 recorded as
read with reasons not taken this round.

## SHONEN.md

All four boxes stay `[~]` (lane-asserted with resolvable pointers); promotion is operator-owned (R60-D6).

## Amendments before any data (counters not yet frozen; no seat has scored an after-state)

- **A1 (2026-10-27, during w1; raised by `w1/ExecC1Tool`, reconciled with `w1/ExecC1Disclose`):** the frozen receipt
  grammar matches 95 of the 144 population files' first committed versions — the other 49 (round-37/40/48 JSON
  fixtures and similar) carry no receipt-grammar line and are population files but not receipts. R2's expected value
  therefore reads `receipts=95 events=12 undisclosed=0 met=True`, exit 0, at the measured revision (at base, with no
  disclosures file, the same run prints `undisclosed=12`, exit 1); `population=144` is separately asserted through the
  frozen path list (`member_changed`/`extra_member`), and the tool's `--json` reports both numbers. Disambiguations
  confirmed as intended semantics (no predicate change): `EXIT=` in the receipt grammar is unanchored (anywhere in the
  first version, so `.ufo/waves/round-52/control/c1-mutation-ladder.json` is a receipt and its three re-pin events
  count); the result span is compared as a set of whole lines; the pending marker is tested over the whole first
  version (the round-57 `after-c1-receipt-pins.txt` fill at `20217f23` is kind `pending_filled`, not `rewrite`);
  disclosure matching uses (path, commit) only, never kind, so no entry becomes a phantom through kind choice.

No predicate sentence changed: C1 `met: cases_passed == 18 of 18 AND scores_held == 3`, C2 `met: cases_passed ==
18 of 18`, C3 `met: conditions_passed == 6 of 6`.
