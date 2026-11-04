# Round 52 — kake (operability: counter registration and hardening; freshness: per-engine crawl hygiene)

lane: kake-shokunin · round 52 · base `93d7fdbd45b0e5698927e7f9cb3dafca24ace416`
axes owned: operability, freshness (both on the 10/10 saturation line; one claim each)

Contract: `.ufo/waves/round-52/contract.json`, frozen before any data. Claims C1
(operability: register and harden the two round-51 counters) and C2 (freshness: three
per-engine crawl-hygiene entries on rows opened this round, plus drift reconciliation).

## Gate

- S374 — https://info-search.yahoo.co.jp/archives/002851.php — accessed 2026-10-25 — § rel属性の利用 (更新日 2010年11月24日) — quote: "このリンク先のウェブページの巡回を推奨していない" (24 units; raw substring of the retained body, sha256 3ad358bdbe7a74798df151c282e4b57af7475686dc405b3f8bad08f68881aecb, 8153 bytes, HTTP 200)
- S329 — https://ziyuan.baidu.com/college/courseinfo?id=1399 — accessed 2026-10-25 — § 友好抓取 → robots写法 (no revision printed on the page) — quote: "如果封禁的agent是Baiduspider，会对PC和移动同时生效" (15 units; raw substring of the retained body, sha256 452aabc38f47828ac92d8de6c9b149fe8f78a52c588834dde414d5281a722c40, 61418 bytes, HTTP 200)
- S312 — https://ziyuan.baidu.com/college/courseinfo?id=267&page=15 — accessed 2026-10-25 — § 移动适配 → 对应关系错误的常见原因 (章节时间戳 2020-08-14) — quote: "手机页使用了ajax等异步加载的方法加载内容主体" (20 units; raw substring of the retained body, sha256 126c3da4e960916b3e5a9f49f273dd7c2ec87d4ee62bff034c93fba63e077935, 46056 bytes, HTTP 200)

Unit rule (declared with the counter, `.ufo/waves/round-52/c52_quote_truth.py` C5): one
unit per CJK character, one per non-CJK whitespace token, bound 6–40 units. The round-51
counter's "6 to 25 whitespace words" rule would make every Japanese or Chinese Gate quote
unquotable (CJK text has no word spaces), so the counter states its own unit rule rather
than silently accepting a one-word quote.

Each URL was fetched once this round; the body is retained under
`.ufo/waves/round-52/sources/` and its sha256, byte count, HTTP status and fetch timestamp
are pinned in `.ufo/waves/round-52/sources/receipts.json`.

## Admitted entries

- `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` (S374) — the link attribute is an
  endorsement and ordering statement, not a crawl refusal; the tagged URL is still used to
  find new pages. New ground: the lane's robots rows (S372, S373) and the meta/header
  link-target restriction (S367) say nothing about `rel=nofollow`.
- `corpus/knowledge/baidu-friendly-crawl-guidance.md` (S329) — one `User-agent: Baiduspider`
  block binds the PC and mobile crawlers together; the crawler honours `*` and `$`; the
  spider trap is the site's own low-cost generation of near-identical parameter URLs. New
  ground: the lane holds Baidu's tools manual and its fetch model, not its crawler guidance.
- `corpus/knowledge/baidu-mobile-matching-error-causes.md` (S312) — five causes of a failed
  PC↔mobile correspondence, two of which a page-side or crawl-side check can see: an ajax
  main body, and a robots block on Baiduspider. New ground: the lane holds no mobile-matching
  row from this operator.

## Refused entries (reason and flip)

- `crux-keyless-check.md` (staged, S303/S304) — **refused: ground already held and sources
  not opened this round.** The lane's `field-performance-cwv.md` already carries the
  eligibility question (§ "CrUX eligibility (S038)") and the API route (§ "The CrUX API
  (S039)"); neither S303 nor S304 was in this round's registry or fetched this round. Flip:
  open S303/S304 with a retained body and show the staged entry states a rule the held entry
  does not.
- `jekyll-url-baseurl-options.md` (staged, S041/S042) — **refused: E04-class duplicate.**
  `corpus/knowledge/pages-base-path.md` holds the `baseurl`/`relative_url` ground and cites
  S041/S042; a second entry on the same rows would split one claim across two files. Flip:
  the held entry loses the rule, or the staged entry states a different rule (for example a
  Jekyll `baseurl` interaction with a custom domain) grounded on a row the lane does not hold.

## Id collision check

Staged ids for this lane (`S374`, `S329`, `S312`) against the adopted registry ids: no
overlap (`comm -12` over sorted id lists, empty; `.ufo/waves/round-52/assimilation/reg-ids`
vs `staged-ids`). The guard proof that the check is not vacuous — an indented staged row whose
id collides is detected — is `.ufo/waves/round-52/assimilation/guard-proof/` (fixture with a
deliberate collision; the checked command names it).

## Quarantine

`.ufo/waves/round-52/assimilation/quarantine-slice` carries this lane's slice of
`.ufo/waves/corpus-expansion-1/absent-defect-register.md` (rows whose staged evidence cannot
be produced by a plain GET). Nothing in this round's three admissions comes from that slice.

## Mistakes

1. **The wave-1 dispatch never ran.** The 46-seat payload
   (`.ufo/waves/round-52/w1-dispatch.json`, validator stderr empty) was refused at the
   background-job cap and `spawned nothing`; no seat was replaced or invented, so the round's
   evidence carries **0 seats** and the L1 built and measured every instrument directly. A
   dispatch refusal is not a wave: nothing here claims seat-output evidence.
2. **The first hardened ledger rewrite dropped a guard I meant to keep.** The rewrite removed
   the seat-name-in-body check and initially made absent evidence exit 0 (`0/3 met=True` at
   the base revision). The base control caught it: absent evidence must be a miss (exit 1),
   and the counter now does that.
3. **The mutation ladder's first family set proved too weak.** Five of twelve mutants were
   already killed by the old counter, so the ladder scored 7/18. Six new families were added
   against gaps the old counter has by construction (`seats` mirror, accounting roster,
   `wallClockSeconds`, seat role, unclassified dead reason, ok-with-500, conflicting duplicate
   probe receipts), taking the ladder to 13/18 with the control still green.
4. **The pre-append mirror needs a base snapshot to satisfy E11.** A bare copy of
   `corpus/SOURCES.md` makes the census report `E11 missing used-by` for rows whose `used-by`
   names an entry, a lesson or a script: the `--file` mode resolves used-by paths against the
   file's grandparent. The mirror tree therefore carries the base revision's `corpus/`,
   `SCORECARD.md`, `SKILL.md` and the three named scripts, and the census exits 0 on it.
5. **The ledger's coverage floor was wrong on its first formulation.** It required
   `settled == spawn`, which would reject every wave that loses a seat to a classified death.
   It now requires `settled + dead == spawn`, `reports_written == settled` and each dead seat
   to carry a classified reason.

## Wave accounting

| item | value |
|---|---|
| declared batch | 46 seats (`w1-dispatch.json`, maxLanes 47) |
| spawned | 0 (dispatch refused: background-job cap; payload resent once, unchanged) |
| settled / dead | 0 / 0 |
| seat reports committed | 0 |
| instruments built this round | `c52_wave_ledger.py`, `c52_mutation_ladder.py`, `c52_quote_truth.py`, `c52_gate_registry.py` |
| measured revisions | base `93d7fdb…`; round evidence commit; measured tip (see SCORECARD) |

No seat time is claimed, so the C1 predicate is not a statement about a wave: it is a
statement about the instruments (registry rows, selftest receipts, mutation ladder, real-data
reruns), each of which has a committed receipt under `.ufo/waves/round-52/control/`.

## Drift reconciliation (observed, not re-pinned over a live divergence)

The sweep entered this round at `VERDICT: DRIFT` with three legs (`control/drift-before.txt`).

- **PQ-2 push gate** — the remote had advanced `e6bd071…` → `24991e44c74d1061db55652be4a27db56efc8791`
  and the local clone was 0 commits ahead (pin said 20). Re-pinned to the observed remote and 0
  unpushed, with the transition recorded in `freshness-pins.json` (`pq2Reconciled`); the sweep now
  reports `GATE-CLOSED`. This is a pin advancing to an observed state, not a red state hidden.
- **ds4cc sitemap** — the listing answered 200/7810 B where the pin held 404 (pre-push). Because a
  published listing is a legitimate steady state, the instrument gained a pure
  `sitemapVerdict(status, bytes, pinStatus, pinBytes)` with a `LISTED-STEADY` branch (bytes are the
  predicate once the pinned status is 200) and a six-case selftest, taking the sweep selftest to
  36/36. The pin now records 200/7810 B and the sweep reports `LISTED-STEADY`.
- **plazir-gate-anomaly** — left red and disclosed: the source directory exists but its sitemap
  source is absent (`source skipped(no-source-file)`) and the live sitemap carries 7 locs against a
  pin of 8. Re-pinning it would hide an operator-owned absence.

Result: the live sweep exits 1 with one leg (`control/sweep-after.txt`). The C2 predicate's
`after == 1` counts that leg, not a clean sweep.

## Round-53 correction — refused-entry grounds (append-only)

The refusal decisions above stand; their reasons are corrected here, not rewritten.

- `crux-keyless-check.md`: the round-52 receipt set contains only S374, S329 and S312, so the staged CrUX Vis and API sources were not opened in-round (CORPUS SOURCES rule 1); neither source was registered. The held `field-performance-cwv.md` covers CrUX eligibility and the key-requiring API, not the keyless CrUX Vis route. S304 also maps to the quarantined `queryRecord` source. The refusal is not justified by claiming the entire topic was already held.
- `jekyll-url-baseurl-options.md`: the staged source was not opened in-round, which is sufficient under rule 1. The staged row's distinct scope would produce a W04 cross-scope duplicate warning, not E04; the earlier E04/duplicate-in-scope rationale is withdrawn. The refusal is not a claim that S080 is a same-scope duplicate.

Evidence: `.ufo/waves/round-52/sources/receipts.json` lists the three opened sources; `.ufo/waves/round-52/assimilation/quarantine-slice` lists the CrUX queryRecord source. Round-53 falsifier `.ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py` covers the staged ids and true procedural grounds, but the uncommitted shokuknow package snapshot was never pinned in round 52.
