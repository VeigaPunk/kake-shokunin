<!-- Draft for LOG.md — append after the round-80 entry. Bullet style matches rounds 79-80. -->

> **Draft status (ScribeRecord, round 81).** Base-state lines are quoted from committed receipts with
> `file:line`; `⟨FILL …⟩` marks an after-state byte not yet on disk. Replace markers with the
> receipt's own words at integration.

## Round 81 — 2026-11-04 (hyaku run 15; attempt 1; Linux host; claims frozen before any seat ran)

- **Frozen contract.** `.ufo/waves/round-81/contract.md` at
  `a77b8a19c2b65a07dfbe40aaf7ec86aaeee2f9cb`, frozen before any seat ran: the C1 item conditions
  R80-1 … R80-6 and the `met <=> open == 0` predicate, the C2 receipt/allowlist/audit-equality
  predicate, both kill rules and the base/junk/tampered control receipts. Amendment 1
  (`.ufo/waves/round-81/amendments/amendment-1.md`) at `0a27045e`, written before any after-state:
  A1 aligns `p_r80_4` with the contract's settled definition and adds two selftest fixtures; A2
  corrects the S454 anchor to §15.5.5/§15.5.11 and leaves the frozen expectations bytes alone. Base
  `2e11925500dd5a739376c9108c94616243af0cd4`. Measured carrier ⟨FILL⟩.
- **Motivating evidence.** The non-author round-80 closure
  (`corpus/lessons/round-80-verifier-spotcheck.md` §6) routed six defects at the round-80 report,
  lesson and evidence chain: a one-line pointer error (R80-1: `corpus/SOURCES.md:201` is blank, the
  S453 row is at line 200), a misstated constant tally (R80-2: "12/12 each" against
  `4/4` constants and `47/48` case-level failures, `const_echo` `11/12`), a count/scope mislabel
  (R80-3: the exact `rfc9110.txt` URL was held twice, so S453 is the *third* scope, not the second),
  a wave-accounting error (R80-4: sentinel counted as an attack role; settled share `2/15 = 13.3 %`
  below the ≥25 % floor), a scratch-only control (R80-5), and a results schema with no error field
  (R80-6). The same spot-check re-ran both round-80 counters and agreed with them, so these are
  accuracy/accounting/reproducibility defects, not claim failures; the round's calibration move is to
  make each decidable from bytes by a committed counter instead of by a sentence.
- **Wave `w1`.** One v1 wave, 15 seats, band 8–16: scout 2, executor 4, scribe 2, reviewer 4,
  critic 1, mutation-tester 1, connector 1 (`.ufo/waves/round-81/w1-spec.json`); requested attack
  share 6/15 = 40.0 % over {reviewer, critic, mutation-tester, labrat}; settled
  ⟨FILL `w1-accounting.json` / `make_accounting.py` stdout — the settled definition is a results row
  with non-empty output⟩. Spec `w1-spec.json`, dispatch `w1-dispatch.json`, ready `w1.ready`,
  results `w1-results.json`; no planner seat appears in the spec (the L1 holds planning).
- **C1 landed and measured.** `.ufo/waves/round-81/c81_defect_queue.py` decides each of the six items
  from lane bytes: R80-1 computes the S453 line itself and requires an `R80-1` correction row naming
  it; R80-2 re-derives `constants_failed`, the summed case-level failures and `const_echo` from
  round-80's constants receipt; R80-3 counts the registry's `source` cells for `rfc9110.txt` and
  `rfc9110.html`; R80-4 re-derives the settled attack share only from a matching accounting record;
  R80-5 rebuilds round-80's junk tree from a committed spec and re-runs round-80's own counter; R80-6
  re-derives the seat record from `w1-spec.json` + `w1-results.json` and compares it canonically.
  Base `2e119255`: `C1v1 revision=2e11925500dd5a739376c9108c94616243af0cd4 items=6 open=6 closed=0
  met=false`, exit 1 (`controls/base-c81-defect-queue.txt:8-9`). Carrier ⟨FILL
  `controls/after-c1.txt:8` — `items=6 open=0 closed=6 met=true`, exit 0⟩. Counter selftest
  `selftest: 15/15 passed`, exit 0 (`controls/c81-selftest-c1.txt:17-18`, re-cut by amendment 1 A1): a
  green fixture closes all
  six and one mutant per item opens it, including an over-built junk tree that must read
  `open=4 closed=2 met=false`. Junk control `C1v1 revision=worktree items=6 open=6 closed=0
  met=false`, exit 1 (`controls/ctl-c81-junk-queue.txt:8-9`) — a tree that fabricates closure in
  words closes nothing.
- **C2 landed and measured (capability).** Three declared `ds4cc.com` surfaces (`/`,
  `/robots.txt`, `/sitemap.xml`) were captured once, GET-only, and retained under
  `.ufo/waves/round-81/capture/<id>/response.json`; `.ufo/waves/round-81/capture-expectations.json`
  froze the allowlist (`ds4cc.com`, `www.ds4cc.com`), the six expectation classes (S430–S433) and the
  S454 status rule before the audit ran; `capture/manifest.json` is the mechanical join of the two.
  `scripts/header_audit.py` (unchanged this round) audits the committed manifest offline, its stdout
  committed byte-for-byte as `controls/after-c2-audit.txt`, and `.ufo/waves/round-81/c81_capture_audit.py`
  re-derives the chain: receipt sha256 and byte count against the retained body, an integer status in
  100..599, an RFC 3339 fetch time on or after `2026-11-04T00:00:00Z`, GET/not-truncated, the URL host
  inside the allowlist, and audit stdout equal to the committed receipt (the counter compares
  receipt-normalised lines; the contract's sentence says byte-for-byte — `w1/ScribeRecord.md` F3). Base `2e119255`:
  `capture: no manifest at the measured revision`, `C2v1 root=kake-shokunin surfaces=0 failures=1
  audit_rc=- met=false`, exit 1 (`controls/base-c81-capture-audit.txt:12-14`). Carrier ⟨FILL
  `controls/after-c2.txt`⟩. Counter selftest `selftest: 12/12 passed`, exit 0
  (`controls/c81-selftest-c2.txt:14-15`); five mutants (body digest, byte count, stale fetch time,
  drifted audit receipt, empty manifest) each open the item. Per-surface audit outcome ⟨FILL the
  findings count and exit from `controls/after-c2-audit.txt`⟩.
- **Frontier and sources.** `corpus/SOURCES.md` 191 → ⟨FILL the census-after row count⟩ rows.
  **S454 admitted** (`corpus/lessons/round-81.md:101`): RFC 9110 §15.5.5 *404 Not Found* and
  §15.5.11 *410 Gone*, `https://www.rfc-editor.org/rfc/rfc9110.txt`, access 2026-11-04T11:46:55Z,
  HTTP 200, final URL identical to the request URL, 502,941 bytes, sha256
  `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, retained at
  `corpus/lessons/round-81-gate/rfc9110.txt`; the located quote is `:7589-7590`, 21 words,
  collapsed-only, with the paired permanence sentence at `:7669-7670`, 20 words. §15.5.4 is
  **rejected** as the anchor (`rfc9110.txt:7569` is `15.5.4. 403 Forbidden`, `:150`), and the frozen
  `capture-expectations.json` prose keeps the wrong anchor by design (`:200`; amendment 1 A2).
  The row is inserted after line 200 and writes no registry byte from the Gate seat (`:204`), so
  R80-1's `:200` pointer does not move. **S433 re-opened** (`:164`): access 2026-11-04T11:46:56Z,
  HTTP 200, 1,187,554 bytes, sha256 `d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5`,
  byte-identical to the round-61 retained body; quote `:4039-4040`, 17 words, collapsed-only;
  `recheck 180d → 180d` with next due `2027-04-25 → 2027-05-03` and `used-by
  corpus/knowledge/response-header-expectations.md → …, corpus/lessons/round-81.md`. Overlap stated
  not hidden: S088's scope cell already names 404 and 410 (`corpus/SOURCES.md:96`), so S454 holds only
  the absence reading (`:145-149`). Census before: 191 rows, 20 `W04` lines, exit 0
  (`controls/census-before.txt`); census after ⟨FILL rows and the `W04` count from
  `controls/census-after.txt`; the Gate's scratch-copy check emits `W04 S454 duplicate url
  www.rfc-editor.org/rfc/rfc9110.txt` and its 252 `E11` lines are a `--file`-mode artefact, not a lane
  census result (`:141-144`)⟩. Assimilation: none — the `merge/kake` staged package still collides on
  8 ids and 27 URLs the registry already holds (`:159-162`). Grounding for the S454 row: a 404 or 410
  answer is the target resource's absence, not a header failure — the audit records it with its status
  and draws no `content_type_present` conclusion from it.
- **Mined mistakes.** Three classes, each with its own receipt (`corpus/lessons/round-81.md:185-187`):
  (i) *a selftest that cannot run is indistinguishable from a property that cannot pass* — the first
  `c81_defect_queue.py --selftest` at the freeze had an unmatchable summary regex, a `cwd` passed to
  `subprocess` before it existed and a green line citing registry `:5` for a row at `:6`, so three
  fixtures read as red conjuncts; the fix is that every fixture is scored green-first in the same
  receipt. (ii) *a locator that names the section above its quote* — the first span probe returned
  `rfc9110.txt:7584-7590` for a sentence beginning at `:7589` (`:7584` is the tail of the §15.5.4 403
  body); a tightest-span search resolves 404 to `7589-7590` and 410 to `7669-7670`, and forcing the
  window to start at the heading shows the assertion can fail. (iii) *the instrument's population is
  not the predicate's population* — contract §C1 and `make_accounting.py:35-37` count only non-empty
  settled seats; the frozen counter counted every results row (`c81_defect_queue.py:198-200` before
  amendment 1), so on one synthetic empty seat the builder printed `requested 3/6 settled 2/5
  share=0.400 met=true` while the counter's formula gave `3/6 share=0.500`; amendment 1 A1 aligned the
  counter before any after-state. The round-80 drift class this round closes — a pointer, a tally and
  a scope count written in prose — is the motivating evidence above, not a new mistake.
- **Routed (not claimed).** R80-4's floor is bounded by the results schema: a dead seat is
  *not settled*, so the wave meets ≥25 % only by replacing it, and the accounting record now states
  that definition in bytes rather than in prose; the junk control reads `open=6`, stricter than the
  contract's `open>0` kill rule, so the kill rule is a floor and not the measured value; C2's
  audit-output equality proves the committed bytes and the tool's stdout agree, never who wrote the
  file (a hand-written identical file is indistinguishable at this layer); the capture is a receipt of
  the bytes served at `fetchedAt` and cannot support a claim about any other instant; the six
  expectation classes remain the lane's declared policy (S430–S433), not a source statement that any
  surface should serve them; the C2 counter lives under `.ufo/waves/`, outside the round-75
  instrument-receipt population, and no `scripts/` instrument changed this round; S454 overlaps S088's
  scope cell (`corpus/SOURCES.md:96`) and is the row to withdraw if section overlap is later ruled
  fatal (`corpus/lessons/round-81.md:197-200`); the frozen `capture-expectations.json` keeps the
  §15.5.4 anchor and a reader must take the anchor from the registry row or the Gate (`:201-204`);
  R80-5 proves the junk tree reproducible, not that its one closed item closes for a good reason —
  round-80's R79-5 conjunct is textual (`:211-214`); R80-6 records only what the results schema
  carries, so a dead seat's message remains whatever the dispatcher wrote (`:215-217`); the round-81
  lesson's settlement paragraph names the after receipts `controls/after-c81-defect-queue.txt` /
  `controls/after-c81-capture-audit.txt` while the contract and this block name `controls/after-c1.txt`
  / `controls/after-c2.txt` — one pair must be chosen before the claim is read
  (`corpus/lessons/round-81.md:220-226`); the C2 counter's fetch-time floor is a string comparison
  (`c81_capture_audit.py:87`), so a non-`Z` offset is ordered by digit not instant, and
  `capture-expectations.json` is never read by the counter — `surfaces` and the allowlist come from the
  manifest the capture seat writes (`w1/ScribeRecord.md` F2, F4); ⟨FILL any further wave finding the L1
  routes, including the freshness sweep's standing `~/projects` drift (open L0 `kake | round-69`) if it
  still exits 1⟩.
- **Not done this round.** No publish or deploy. The only operator-owned fetches were the three
  declared GET-only requests to `https://ds4cc.com/`, `/robots.txt` and `/sitemap.xml` (no cookies,
  no credentials, no request body, one per URL), plus any public source GETs the opening seats made
  for S454/S433; no MANIFEST edit; `corpus/`, `PROVINCE.md` and `SCORECARD.md` edits are append-only;
  no tool installed or upgraded; pacman untouched.
