# ExecC3Counter

Claim C3 counter, written to contract § Claim C3. Deliverable: `.ufo/waves/round-61/c61_recheck_pins.py` (new,
1232 lines, `chmod +x`), plus the evidence in `.ufo/waves/round-61/w1/ExecC3Counter.files/`. The counter was NOT
run against the lane after-state (no counter score exists); every run below is a fixture, a base-revision control
or a master invariant check.

## FILES CHANGED

- `.ufo/waves/round-61/c61_recheck_pins.py` — new counter (only lane code file written); this report.
- `.ufo/waves/round-61/w1/ExecC3Counter.files/` — `selftest.txt`, `base-control.txt/.json`, `integration.txt`,
  `real-registry-mutants.txt`, `live-probe.txt`, `receipt-schema-calibration.txt`, `integ_driver.py`, `mutants.py`.
- No tool install or upgrade (nothing was needed); no `pacman`; nothing outside the lane report path and scratch.

## BEHAVIOR

`python3 -B .ufo/waves/round-61/c61_recheck_pins.py --root <lane> --revision <rev> [--json]` (+ `--base`, default
the frozen `9f07731a…`; `--selftest`). Exits 0 met / 1 not met / 2 unevaluable (registry unreadable at either
revision, root not a toplevel, revision unresolved) / 64 usage. `PREDICATE = "met: conditions_passed == 6 of 6"`;
text summary line `c61 recheck-pins: conditions_passed=<n> of 6 met=<bool>`, then one line per condition with its
findings. Offline: `git show`/`git ls-tree` only, `GIT_*` scrubbed, worktree never read, no network import.

## DESIGN

Surface read at the measured revision: `corpus/SOURCES.md` rows (0–3-space pipe, under `## Registry`),
`corpus/lessons/round-61.md`, and the retained recheck evidence — bodies under `.ufo/waves/round-61/recheck/`
with the row id as the filename stem (`Sxxx.html`; any extension), receipts in `recheck/receipts.json` as a
`receipts` list (also accepts a `sources` id→entry map and the `httpStatus`/`fetched_at`/`user_agent`/`digest`
spellings), fields `url, effectiveUrl, status, sha256, bytes, fetchedAt, userAgent`.

- **C1** — the due-set rule is re-derived at the measured revision, not read from the contract: rows with a
  parseable `opened`, status != `rejected`, oldest date taken, ties sorted by numeric id, first ten. Compared to
  the frozen S001–S010. Any row with != 11 cells or a non-ISO `opened` fails C1 (a row that cannot be scheduled).
- **C2** — base cadence per due row decides the pin: `Nd` → concrete date with `opened < pinned <= opened+N`;
  `on-release`/`on-use` → exactly `opened+90d`. A due cell that is neither an ISO date nor its base cadence fails
  (a rewritten cell is not a carry). Zero pins fails C2 (contract do-nothing row). `facts.pins[<id>]` records the
  bound, `exact` (`pinned == opened+cadence`) and the base cadence, so a compliant-but-early pin is visible.
- **C3** — the Gate line is a bullet whose leading token is the id or a table row whose first cell is the id,
  inside a `## Gate*` section (fenced blocks skipped). It must carry one of the row's URLs (S001/S002 each name
  two) and the access date `2026-10-27`; curly quotes fail. ASCII double-quoted spans: a claim-sized span
  (>= 6 units) must be ASCII, 6..25 units, <= 160 characters, a substring of one whitespace-collapsed text node of
  the retained body and page-unique; a sub-6-unit span is context and fails only when it is not body text at all;
  at least one span must pass. Text nodes: HTML → text between tags with comments, script/style/noscript/svg/
  template/head and page chrome (nav/aside/header/footer/form) blanked; untagged bodies (raw YAML/C/texi) →
  blank-line paragraph blocks; nodes whitespace-collapsed, entities not decoded. A span missing only because it
  crosses inline markup is named as such (`inline_flattened` diagnostic).
- **C4** — each pinned row needs a committed body blob and a receipt: `sha256` == blob digest, `bytes` == blob
  length, status 200, `fetchedAt` with an offset on 2026-10-27 UTC, `userAgent` carrying `round61`, `url` in the
  row's URL set. A body retained for a carried row needs sha/bytes consistency only (its status is recorded —
  the carry rule allows non-200). An extra `.html` body needs a receipt matching its sha256.
- **C5** — every unpinned due row keeps its base cadence and carries a Gate note naming the observed state
  (`anchor_moved`, `page_changed`, `fetch_failed`, `quote-missing`/`anchor not located`, `non-200`/`HTTP <code>`,
  `timed out`, `unreachable`, `redirected`); a note that says only `anchor_found` with no pin fails. Every pinned
  row must have a Gate line.
- **C6** — base rows outside the due set are byte-identical (raw committed line bytes); a due row may differ from
  base only in cell 9; every base id is still present; appended ids are recorded, not failed.

Selftest builds throwaway `git init` fixture repos under `TMPDIR` (toplevel asserted, commits only with
`-c user.name=selftest -c user.email=selftest@local`, every later git call `-C "$D"`), with one base commit and one
after-state commit, and compares each case's failing-condition set against the green baseline.

## SELFTEST

**`--selftest`: 56/56, exit 0** (`selftest.txt`): green 6/6 exit 0; base-tree control (measured at the fixture's
base commit) → C2 fails with `0 pins` + C5 fails; constant control (all ten dates rewritten, no lesson/bodies/
receipts) → C3 + C4 fail while C2 passes; 30 fixture cases; 23 unit checks (units floor/ceiling, CJK units, char
ceiling, the pin dates 2027-01-17/2027-10-19, node extraction incl. chrome exclusion and inline split, ISO-date
refusals, `--json` schema, text summary, exits 2/64).

Per-condition able-to-fail evidence (each case fails exactly the named condition unless two are noted):
C1 — a new mined row opened 2026-10-18 shifts the due set; a new *rejected* row opened 2026-10-18 does not (green).
C2 — a 90d row pinned 2027-01-18 (out of bounds), an `on-release` row pinned 2027-01-18 (not `opened+90d`), a cell
rewritten to a datetime, all ten carried with notes (`0 pins`). C3 — quote absent from the body; 26 units; 215
characters; URL missing; access date missing; curly quotes; a nav-only span. C4 — receipt dropped; sha mismatch;
status 404; userAgent without `round61`; `fetchedAt` on 2026-10-26; URL outside the row; wrong byte count; body
missing. C5 — unpinned with no note; unpinned note saying `anchor_found`; unpinned with a changed cadence; pinned
row with no Gate line. C6 — a due row's non-recheck cell changed; a non-due row changed; a base row removed; a
single-space change in a non-due row. Green controls: appended row allowed; sub-floor accurate context quote is an
observation, not a failure; rejected oldest row filtered.

**Real-lane base control** (`base-control.txt`, `.json`) — measured at `9f07731a…`, i.e. the do-nothing tree, not
an after-state: **4/6, exit 1**. C1 PASS (167 rows; 16 non-rejected rows opened 2026-10-19 → S001–S010, matching
the frozen ten), C2 FAIL `no due row carries a concrete ISO recheck date (0 pins)`, C3 PASS (no pinned rows), C4
PASS (no bodies/receipts claimed), C5 FAIL (ten rows without an observation note), C6 PASS. So the real registry
parses and the base cannot pass C2 — the declared do-nothing control is reachable in the lane itself.

**Real-registry integration** (`integration.txt`) — read-only `git clone -q --shared` of the lane into scratch, then
a *synthetic* ten-pin after-state on the actual 167-row registry (synthetic bodies; no network) → **6/6, exit 0**,
`pinned=10 carried=0`; mutating a non-due row (S050) → C6 only, exit 1. This exercises the real multi-URL source
cells of S001/S002 (receipt carries the first URL; C4 accepts either) and the real lesson grammar.

**Real-registry mutants** (`real-registry-mutants.txt`, same clone and driver): over-pinning S011 (not due) → C6
only; dropping the S003 receipt → C4 only; a Gate quote absent from the body (S006) → C3 only; a non-200 carry for
S005 with a Gate note → pass (`pinned=9 carried=1`); a due pin earlier than its base cadence (S008 365d →
2027-01-17) → pass (inside the frozen bound, `exact` false — see ambiguity 2).

**Live node probe** (`live-probe.txt`, my own single GET, 2026-10-27, UA `kake-shokunin-round61`) — the S003 row
URL: HTTP 200, 154136 bytes, sha256 head `261408c59b4476f6`, 129 nodes. A 13-unit sentence lands in one text node;
"About publishing sources" lands in one node with chrome blanked but two without (the navigation copy), which is why
page chrome is excluded; spans crossing inline links are named by the diagnostic; `&quot;` stays undecoded.

**Receipt schema calibration** (`receipt-schema-calibration.txt`) — the recheck evidence the fetch seat had written
by 06:15 (worktree copies, uncommitted; a parser check, not a score): 10/10 receipts parse, every `url` is one of
its row's URLs, `status` 200, `sha256` == blob digest, `bytes` == blob length, `fetchedAt` on 2026-10-27 UTC,
`userAgent` carries `round61`, and `body_nodes` yields nodes for all ten bodies. No C4 schema surprise at
integration; S002's 199999-byte body is complete (`</body></html>`), not truncated. Unrun, by assignment: the counter
against the lane after-state; no after-state score; no counter freeze (the L1 freezes).

## CONTRACT AMBIGUITIES

1. **C2 non-vacuity is implied, not written.** "For each pinned row …" is vacuous when nothing is pinned, yet the
   do-nothing row requires base to fail C2 "with 0 concrete dates". Implemented: zero pins fails C2. Otherwise a
   no-op build would score C2 green.
2. **C2's bound is looser than the pin rule's date.** C2 allows `opened < pinned <= opened + cadence`, the pin rule
   says the cell moves to `opened + cadence`; a 365d row pinned at 2027-01-17 passes C2 (measured on the real
   registry). Recorded as `exact: false` in `facts`, not failed — tightening to equality is a v2 move.
3. **C4's "HTTP 200" vs the carry rule.** Read literally it would fail an honestly carried non-200 row whose body
   was kept. Implemented: pinned rows require 200; carried rows' bodies require sha/bytes consistency and their
   recorded status becomes a fact, not a failure.
4. **"Receipt URL = row URL" when a row names two URLs.** S001 and S002 each name two URLs in their source cell, so
   no single receipt URL can equal "the row URL". Implemented: the receipt URL must be one of the row's URLs, and
   the C3 Gate line may carry either.
5. **C3 "one double-quoted span" vs the lane quote rule ("every quote 6..25 units").** A Gate line may legitimately
   quote a short anchor name as context. Implemented: claim-sized (>= 6 units) quotes are hard-checked; sub-6-unit
   quotes fail only when they are not body text; at least one span must fully pass.
6. **C6 "rows not in the due set are byte-identical to base" cannot hold for the rows C2 appends** (S430–S433):
   implemented as base rows outside the due set byte-identical, due rows differing only in cell 9, every base id
   present, appended ids recorded. Registry prose/heading edits are outside C6 (nothing checks them).
7. **C5's observed-state vocabulary is unspecified.** Implemented as the named token set above; an unpinned note
   that says only `anchor_found` fails as contradictory. Any other vocabulary (e.g. `no-anchor-in-body`) needs a v1
   amendment — the L1 should make the C3 seats use one of the named tokens.
8. **"page-unique" is not scoped.** Implemented within the row's own body only; the same phrase on two different
   pages is not a defect.
9. **Body filename.** The dispatch pins `recheck/Sxxx.html`; the counter accepts any extension when the stem is the
   row id (a `S001.yaml` raw body works) but a lowercase `s001.html` would not (ids as written in the registry).
10. **"Text node" for untagged bodies.** Raw YAML/C/texi (S001, S002, S009 if kept raw) have no tags; implemented
    as blank-line paragraph blocks. A one-paragraph raw file is a single node, so page-uniqueness is vacuous there.
11. **Entities.** Not decoded, per the round-60 rule. A literal `"` cannot be represented inside a Gate
    double-quoted span, and a body quotation mark must be quoted as `&quot;`; C3 fails a span where the author
    wrote the decoded character.

## RISKS

- Lesson Gate lines inside a fenced block are skipped (a subdirectory body is fine: the stem is the basename), so a
  mis-shaped lesson fails C3/C5 with a locatable note instead of passing silently.
- Real docs.github.com spans often cross inline markup (measured); the quote seats must pick a single text node.
- The counter recomputes the body digest from the committed blob, so a receipt cannot outrun its body; the recorded
  *fetch* remains the fetch seat's sha256-pinned testimony (reviewer-checked).

VERDICT: C3 counter built to the frozen six conditions (offline, committed bytes only, exits 0/1/2/64), selftest 56/56 including base-tree and constant controls, real-lane base control 4/6 with C2 failing at 0 pins, and a real-registry synthetic after-state passing 6/6 — no after-state score taken, awaiting L1 freeze.
