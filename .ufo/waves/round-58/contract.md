# Kake round 58 — frozen contract (predicates declared before any data)

Lane: kake-shokunin. Base revision (lane master tip at round open, = `BASE_REV`/`BASE` in the counters):
`044048597d62f3199494b63b36e90dd57825e350`. This file, `contract.json`, the three counters (version 1), their base-control receipts,
the retained source bodies with receipts and the pre-append registry mirror are committed together before any build edit and before
any seat scores. The predicate sentence of each claim is the same sentence here, in the counter's code (`PREDICATE`) and in every receipt
label. Round date 2026-10-26. Round shape: ONE v2 wave (`w1`, build + attack items together, >= 25 % attack roles, 64–128 seats) plus at
most one residual handoff of <= 8 reviewer/critic seats; round total <= 128. The L1 holds the canonical planner seat (the validator rejects
`planner`). Seats are read-only except their own report file and a `<Seat>.files/` directory beside it.

Receipt rule (routed defect D1 of the round-57 spot-check): a receipt under `.ufo/waves/round-58/controls/` is committed once, after the
run it records, and never rewritten; a re-run lands under a new file name. No placeholder receipt is committed. C1 enforces this for the
round's own receipts (`new_rewritten == 0`).

## Axis declaration

The prompt-declared lane axes are operability + freshness; the lane scorecard also carries the round-54 bounded sub-axis **calibration**
(score 1, the lowest-scoring non-retired axis, so the lowest-axis obligation lands on C1). The ownership question (calibration vs
operability) stays open for the operator, as in rounds 55–57. Three claims on three distinct axes: C1 calibration, C2 operability, C3
freshness (sourced). No exploratory claim. Causal separability: C1 reads only receipt history and the ledger; C2 reads only
`scripts/id_resolver.py` and gate-built fixtures (P7 reads the lane's own knowledge/registry, which C3 extends — P7's floor `ids_cited >= 106`
holds with or without C3's entries); C3 reads only the two entries, their rows, the lesson Gate and the round-58 evidence files.

## Claim C1 — calibration: every post-commit change to a measurement receipt is disclosed with its true values

Surface: every path ever committed under `.ufo/waves/round-<N>/control/` or `controls/` (all rounds) in the tip's ancestry, and the lane's
own statement about them, the ledger `.ufo/waves/round-58/receipt-rewrites.json`. Observed state: git history of each receipt. The round-57
spot-check (D1) found `controls/after-c1-receipt-pins.txt` committed as `pending` and filled in later while the report said no receipt was
rewritten; considerthese 2026-10-26 proposal 2 (receipt-rewrite watch) names the same class. The round-57 counter watched `revision:` lines only.
- Before (base): `events=19 undisclosed=19 … new_receipts=0 met=False`, exit 1 (`controls/base-c1-receipt-rewrites.txt`): 19 post-commit
  modifications across rounds 52–57 (6 of them the revision relabels the round-57 errata disclosed; 13 never disclosed, including the round-57 fill).
- After: the ledger lists every event with path, commit, status, the from/to blob ids git shows, the counter-classified kind and a note that
  names a resolvable evidence pointer; this round's receipts are never rewritten; the two round-58 C2/C3 after-receipts exist at the tip.
- Counter: `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root <lane> --revision <tip>` (tip = the lane revision that holds the
  C2 and C3 after-receipts; the C1 receipt is written after this run and committed once, covered by `new_rewritten` at every later tip).
- Predicate (frozen): **met: undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0 AND unpointed == 0 AND new_rewritten == 0 AND new_receipts == 2**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: base, exit 1, 19 undisclosed. Junk controls (selftest v1, 18 checks, `controls/c1-selftest-v1.txt`): a wrong blob, an
  invented commit, a duplicate entry, a false kind, an empty or pointer-free note, a note naming an absent path, an unknown kind, a round-58
  receipt rewrite (even disclosed), a rename/deletion, a re-add, a missing C3 receipt and a non-JSON ledger each fail.
- What the counter does not test: whether a note's prose explanation is true (reviewer-checked); receipts outside `control(s)/` dirs; a
  ledger generated from git by the counter's own classifier would meet the counter — it would be a true disclosure, and the claim is the
  disclosure's truth, so this is a stated limit, not a junk pass.

## Claim C2 — operability: `scripts/id_resolver.py` closes its two disclosed false-green defects, nothing else moves

Surface: the lane tool `scripts/id_resolver.py` (round-57 capability). Defects disclosed after the round-57 freeze: D1 fence-blind registry
(`w2/CriticResolverCheat.md` C08–C10), F1 git-quoted knowledge paths dropped with `--revision` (`w2/ReviewerResolverCode.md` F1). Routed
defect D5 of the round-57 spot-check carries both.
- Before (base): `7/12 met=False`, exit 1 (`controls/base-c2-resolver-cases.txt`): K1–K5 fail (exit 0, `dangling=0` where an id is dangling), P1–P7 pass.
- After: 12/12 — K1–K5 report the dangling id with exit 1; P1–P7 unchanged (3-space row resolves; a row after a closed fence resolves;
  4-space line is code; a committed sibling owns; absent `--fleet` exit 2; tool selftest N/N with N >= 49; real lane at the revision green with ids_cited >= 106).
- Counter: `python3 -B .ufo/waves/round-58/c58_resolver_cases.py --root <lane> --revision <rev> [--work <scratch>]`.
- Predicate (frozen): **met: cases_passed == 12 of 12**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: base 7/12, exit 1. Junk controls: a tool that prints a constant green line fails K1–K5 and P3/P4/P5; a tool that always
  exits 1 fails P1/P2/P6/P7; a tool that drops every fenced line including the rows after a closed fence fails P2.
- What the counter does not test: the census stays fence-blind (it counts a fenced row; the tool after the fix does not — the divergence is the
  contract's stated choice, markdown semantics); sibling ownership beyond P4; network sandboxing (fixtures are local files).

## Claim C3 — freshness (sourced): two Baidu crawler-identification entries on rows opened this round

Surface: two knowledge entries on the `Crawler identity` frontier ground (`corpus/README.md` frontier map, r51 Googlebot row): Baidu's own
identification procedure (UA strings + two-step reverse/forward DNS, `*.baidu.com`/`*.baidu.jp`) and its unblocking procedure (robots / UA / IP
blocks, the curl UA check). Assimilation theme: Baidu crawler identification from `merge/kake/` (staged entry `baidu-crawler-identification.md`, row S395).
- Rows: S423 = staged S395, renumbered by document (`https://ziyuan.baidu.com/college/articleinfo?id=3457`, retained `sources/S423.html`);
  S424 lane-found, linked from S423 (`https://ziyuan.baidu.com/college/articleinfo?id=3028`, retained `sources/S424.html`). Both opened 2026-10-26.
- Entries: `corpus/knowledge/baidu-spider-identification.md` (cites S423), `corpus/knowledge/baidu-spider-unblocking.md` (cites S424).
- Before (base): `0/8 met=False`, exit 1 (`controls/base-c3-quote-truth.txt`); registry 160 rows.
- After: 8/8; registry 162 rows.
- Counter: `python3 -B .ufo/waves/round-58/c58_quote_truth.py --root <lane> --revision <rev>` (derived from the round-57 counter version 2.1 by
  `derive_c58_quote_truth.py`; conditions C1..C8 in its docstring; the selftest is a stub in version 1 and is ported by wave 1 before data).
- Predicate (frozen): **met: conditions_passed == 8 of 8**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: base 0/8, exit 1. Junk controls (round-57 v2.1 selftest classes, to be ported): off-topic spans (topic 百度蜘蛛 required),
  sidebar/nav quotes outside the article block, spans over 25 units or 40 characters, curly quotes, a body whose sha256 differs from the frozen
  digest, a row whose used-by names another file, a validate receipt from `--root`, a mirror that differs from the base registry.
- What the counter does not test: whether the English rendering is faithful (reviewer/critic-checked); quote truth, not support.

## Frontier step and assimilation (inside the claim cap)

SOURCES census at round start: exit 0, 160 rows (`controls/census-before.txt`). Collision check (0–3-space pattern): reg 160, staged 129,
collisions 8 (S312 S329 S367 S372 S373 S374 S390 S409; the same documents as round 57) — neither S395 nor S378 collides; renumber map
S395 → S423 by document. Quarantine slice: 12 rows (`assimilation/quarantine-slice`), neither S395 nor S378 among them; nothing from the slice is adopted.
Reject candidate: staged `yahoo-japan-crawler-address-change-notice.md` (S378) — the page is the LINE Yahoo ads API notice for the Display
Ads product-list crawler (FTP periodic fetch), not a search crawler; to be gated against PROVINCE.md in wave 1.
Mined mistake: the round-57 placeholder receipt (D1) — captured-by `c57_receipt_pins.py` did not catch it (revision lines only); fix = C1,
shown able to fail (base exit 1, 19 undisclosed).

## Counter versions — version 2 (after wave 1, before any claim was measured)

Wave 1 (68 seats, `w1/`) attacked every version-1 counter before data; no seat scored the after-state. Version 1 stays committed at
`fff3eea6` as history; version 2 is what the claims are judged on. Base controls were re-run under version 2 under new file names
(`controls/base-c{1,2,3}-*-v2.txt`); the version-1 receipts are never rewritten.

- **C1** (`c58_receipt_rewrites.py` v2). Predicate (frozen, version 2): **met: undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0 AND unpointed == 0 AND symlinks == 0 AND new_rewritten == 0 AND new_receipts == 2**.
  Population at any depth under `control(s)/` (w1/CriticC1Cheat CH2); a rename target is an event (CH1); symlinked receipts fail (CH7);
  a note must name an existing path (CH4); byte-level kinds `pin-only` / `content` / `pending-fill` with a pin-residue rule (w1/RevengerReceiptIntent:
  13 of 19 events misnamed by the version-1 semantic names; w1/ReviewerLedgerKinds events 10, 17); binary, null-blob, `./`-pointer and merge-flag
  fixes (w1/ExecC1SelftestHarden). Selftest 18 → 45 (`controls/c1-selftest-v2.txt`). Base under v2: 19 events, 19 undisclosed, exit 1.
  **Correction of the version-1 before-statement** (w1/CriticC1Before): "13 never disclosed" was overstated — of the 13 events outside the
  round-57 errata, two were disclosed in prose at the time (the round-53/54 report/LOG and the round-57 report's landing table name them), so
  11 were disclosed nowhere. The counter's before-value (19 undisclosed in a machine ledger) is unchanged; the prose count is corrected here.
  Stated limits: note prose truth; receipts outside `control(s)/` (79 artifact rewrites, w1/ExecEventsIndependent); side-branch states;
  history rewritten before push.
- **C2** (`c58_resolver_cases.py` v2). Predicate (frozen, version 2): **met: cases_passed == 14 of 14**. Fixture ids drawn per run (`--seed`,
  printed) and random case dirs (w1/CriticC2Cheat H1/H2/H4: masks and canned output met 12/12); K6 (low fenced id vs registered high id) and K7
  (newline file name, H3) added; every K case forbids the registered id dangling and K4/K5/K6/K7 assert the summary (w1/ExecC2GateSelftest);
  P4 asserts url-match; P6 floor 49 → 55. Selftest: 7 scored control tools (`controls/c2-selftest-v2.txt`). Base under v2: 6/14 (P6 now fails
  for the 49-case base tool), exit 1. Stated limit: P6 reads a printed tally, not that the cases ran.
- **C3** (`c58_quote_truth.py` v2, regenerated by `derive_c58_quote_truth.py`). Predicate unchanged: **met: conditions_passed == 8 of 8**.
  S423 article block ends before the series promo trailer `——什么是【搜索问答剧场】` (w1/ExecC3BaseControls H1: trailer spans met 8/8 with zero
  identification content); an out-of-block span no longer counts toward the page-unique floor (H3); the round-57 120-check selftest ported to the
  round-58 bodies (w1/ExecC3SelftestPort; `controls/c3-selftest-v2.txt` 120/120). Base under v2: 0/8, exit 1. Stated limits: quote truth, not
  support; topic rule is lexical.
