# CriticControlsSizing

Leaf critic seat. Frozen counters (v1; sha256 dace35ce…/60c814aa…/0dde4d64… per contract.json) run unmodified against a `git clone -q --shared` of the lane (base `cc8da1674d6e590ae2d05e1f48944ac7939e9ecd`; `BASE_REV 044048597d62f3199494b63b36e90dd57825e350`) under `/fast/scratch/hyaku/kake-r58/CriticControlsSizing/lane`. All fixture commits use `-c user.name=selftest -c user.email=selftest@local`; every git call names `-C <fixture>`; toplevel asserted. No tools installed (system git/python3 only). Staged entry read from the read-only domain tree (`/home/vgpnk/Projects/shokuknow/merge/kake/…`); no lane/domain/sibling writes.

## CONTROLS

### C1 — calibration (receipt rewrites disclosed)
- Base reproduction (cc8da16): `events=19 undisclosed=19 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=0 met=False` EXIT=1 — identical to `controls/base-c1-receipt-rewrites.txt`.
- Control 1 — empty ledger with one dummy note (tip `0c4c0d…`): ledger present with exactly one entry whose path/commit/status/blob keys match the oldest real event (kind=relabel, true blobs) but whose note is `x` (no evidence pointer); no round-58 after-receipts.
  - Tally: `events=19 undisclosed=18 phantom=0 malformed=0 wrong_kind=0 unpointed=1 new_rewritten=0 new_receipts=0 met=False` EXIT=1.
  - Met? No. A non-disclosing ledger cannot reach the target: 18 events stay hidden and the single stub note fails the resolvable-pointer rule.
- Control 2 — mechanical ledger (tip `86e0277…`): ledger generated from git with the counter's own `events()`/`classify()` (true path/commit/status/fromBlob/toBlob, true kinds), each note set to the receipt's own path, plus `controls/after-c2-ctrl.txt` and `after-c3-ctrl.txt`.
  - Tally: `events=19 undisclosed=0 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=2 met=True` EXIT=0.
  - Met? Yes — empirically confirms the contract's stated limit: a mechanically-true disclosure passes the frozen counter.
- Do I agree it is a stated limit, not a junk pass? Yes, with one caveat. The mechanical ledger discloses every event with correct machine values, so it is a *true* disclosure (the predicate's letter, "disclosed with its true values", is satisfied) rather than a false green; the counter never claims to verify prose truth (contract: reviewer-checked). Caveat: `note = the receipt's own path` is a circular pointer (it points at the receipt that changed, not at separate evidence), and `pointed()` accepts any resolvable repo path, so the self-reference counts as pointed. Smallest safe correction: exclude the event's own path from the note's pointer set (or require ≥1 external pointer), preserving the stated-limit property while closing the self-reference loophole.

### C2 — operability (id_resolver.py closes D1+F1, nothing else moves)
- Base reproduction (cc8da16; tool sha256 `25982446…` identical at 0440485): 7/12 met=False EXIT=1 — K1–K5 green-fail (exit 0, `dangling=0`), P1–P7 pass (P6 selftest 49/49; P7 106 cited).
- Control — base tool with only the `-z` fix (tip `2f42ac…`): `knowledge_bodies()` changed from `git ls-tree -r --name-only` + `splitlines()` to `git ls-tree -r -z --name-only` + NUL-split; all other bytes identical.
  - Tally: 9/12 met=False EXIT=1. K4 (`中文.md`) and K5 (`a"b.md`) PASS (exit 1, `DANGLING S900`/`S901` with the correct cited-by path); K1–K3 still FAIL green (fenced `## Registry` / fenced rows counted as registry); P1–P7 unchanged PASS.
  - Met? No. The minimal `-z` fix reaches only the F1 half (quoted paths); D1's fence-awareness is disjoint and required — the 12/12 target is not reachable by this near-nothing control.

### C3 — freshness (sourced): two Baidu crawler-identification entries on rows S423/S424
- Base reproduction (cc8da16): 0/8 met=False EXIT=1 — matches `controls/base-c3-quote-truth.txt`.
- Control — staged entry copied unchanged with renumbered ids (tip `2c39d70…`): staged `baidu-crawler-identification.md` copied byte-for-byte except `S395→S423` into `corpus/knowledge/baidu-spider-identification.md`; nothing staged exists for S424, so the unblocking entry is left absent (a near-nothing control cannot fabricate it). Minimal landing scaffolding built mechanically: two 11-cell rows (anchors `§ 第一步：DNS反查IP (发布日期 2022-08-19)` / `§ 解除百度UA封禁 (发布日期 2020-07-23)`, both unique in-body text-node spans per `span_tools.py`); `## Gate` lines carrying the sha256/bytes from `sources/receipts.json` and topic spans `百度蜘蛛遵守互联网robots协议` (11u/17c) and `正确识别和获取百度蜘蛛` (11u/11c), both raw substrings of one text node and cross-body unique; a hand-written validate/ receipt (argv `sources-census.sh validate --file …validate/corpus/SOURCES.md`, `exit=0`, stdout tail `file<TAB>ok<TAB>…`, scratch registry byte-equal; C7 is a receipt-shape check, not proof the census ran).
  - Tally: 4/8 met=False EXIT=1.
    - C1 FAIL — S424 entry absent (no staged source exists).
    - C2 FAIL — S423 copied header lacks the round date (`verified-at: 2026-10-24` is the staging fetch) and cites no id below the 8-line header; S424 absent.
    - C3 PASS — rows well formed, new, URLs/dates/status/enums correct.
    - C4 PASS — used-by cells exactly the adopted entry paths.
    - C5 FAIL — S423 entry carries 0 page-unique quoted spans: the staged copy contains zero ASCII double quotes and zero `百度蜘蛛` mentions (checked: `"` count 0, topic count 0); the Gate lines themselves pass. Independent probe: the staged text's only real span `非*.baidu.com或*.baidu.jp即为冒充。` (6u/28c, unique) plus `Baiduspider/2.0`/`Baiduspider-render/2.0` (1u each, appear 3×, below the 6-unit uniqueness bar) would still leave the copy with zero qualifying unique quotes even on S423.
    - C6 PASS — receipts pin the bodies (sha256/bytes/200/UTC round date/round58 UA) and receipt URLs equal row URLs.
    - C7 FAIL — S424 validated scratch entry missing.
    - C8 PASS — mirror bytes equal the base-revision registry, pinned sha256/rows hold, mirror add-commit (fff3eea) is a strict ancestor, measured registry minus new rows reproduces the mirror bytes.
  - Met? No. Only the mechanical scaffolding passes; every condition that demands genuinely new sourced content (second entry, round-date header, below-header citation, quoted topic-carrying spans) fails.

## VERDICT PER CLAIM
- C1 — target sound for the do-nothing control (empty+dummy ledger: 18 undisclosed, unpointed=1, met=False); the mechanical-ledger pass is exactly the contract's declared stated limit and is a true disclosure, so I agree with the contract — with the smallest correction that note pointers should not be the receipt's own path.
- C2 — target sound: the `-z`-only near-nothing control fixes K4/K5 but leaves K1–K3 red (9/12 ≠ 12/12); D1's fence fix is irreducible claimed work.
- C3 — target sound: the staged-copy + renumber near-nothing control reaches 4/8; S424 has no staged precursor and the staged copy has no quotes/topic/round header, so 8/8 is unreachable without the claimed sourced entry work.

Note: during this run one `edit` call initially matched the lane's own `scripts/id_resolver.py` by basename; the file was immediately restored byte-exactly from `git show HEAD:` and the lane checkout is clean again (only pre-existing untracked `w1` files remain). No other lane/domain/sibling writes occurred.

VERDICT: All three targets withstand the assigned do-nothing/near-nothing controls (C1 1-fail + 1-stated-limit-pass, C2 9/12, C3 4/8) — the claims as scoped are sound, with C1's note-pointer self-reference loophole as the only flag.
