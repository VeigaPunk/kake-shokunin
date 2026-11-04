# ConnectorScope — round-87 w1 cross-claim & sibling overlap scan (read-only)

Author: ConnectorScope (connector seat, leaf — no subagent dispatch, no production writes).
Report path (relative to `/home/vgpnk/Projects/shokunin/kake-shokunin`): `.ufo/waves/round-87/w1/ConnectorScope.md`; receipts: `.ufo/waves/round-87/w1/ConnectorScope/evidence.md`. Scratch `/fast/scratch/hyaku/kake-r87/ConnectorScope/` created explicitly, empty use, deleted before yield. No installs (none needed; stdlib reads only).

## Axes

- **C1 calibration** (lowest axis, 2 HOLD): finite gate-agreement self-assessment ledger, 8 gate decisions r84/r85/r86, mismatches 8 → 0.
- **C2 freshness** (10 HOLD): bounded offline RFC 9111 §4.2.3 current-age calculator, 17 case exits + 12 valid JSON outputs vs fixed oracle.
- Unaffected axes held: operability, expansion, quality, discernment — no claim moves them this scan.

## 1. considerthese proposal 4 → C1 connection (latest = 2026-10-26.md)

`considerthese/2026-10-26.md` §Part 2 proposal 4: *"Gate-agreement ledger. Track the verifier's agree/disagree count on admits and rejects per round (r56 6/6 with one reason disagreement on S388; r57 7/7) so I can say when the lane's own gate can be trusted more and when it's drifting, instead of reading each spot-check separately."*

C1 is that proposal operationalized as a frozen finite predicate, with three deliberate narrowings an integrator must preserve in wording:

1. **Window bounded to r84–r86** (the three outside spotchecks with committed snapshot copies) instead of proposal 4's open-ended per-round series. Population = exactly 8 decisions; my independent table read confirms 8/8 `agree` (evidence.md §3).
2. **Digest-bound, not trust-bound**: each row pins `source` + `sha256`; count.py re-verifies the snapshot bytes at the scored revision. I re-computed all three digests and they match `expected-ledger.json` exactly (evidence.md §1). This answers proposal 4's drift-detection intent with a bytes-level instrument.
3. **Self-assessment, not trust certification**: contract explicitly disclaims "does not close D84-2/3/4, certify sources or establish universal calibration", and "a copied lie could pass this finite counter". Proposal 4's "can be trusted more" phrasing must NOT appear in the lesson as an earned trust claim.

Non-obvious constraint (integration-blocking): `count.py:ledger_errors` requires the top-level value to be a **JSON list** and each row **data-equal** to the expected row (`matches[0] != want`; extras/renamed keys fail; additional rows counted). Therefore `corpus/knowledge/gate-agreement-ledger.json` must be a **bare 8-element array** — no provenance trio, no `_classification` field, no wrapper object. The "self-assessment metadata, not domain knowledge" classification can live **only in adjacent prose** (README/lesson/QUALITY), never inside the file, without breaking the frozen counter.

**Ledger classification (explicit):** despite its `corpus/knowledge/` path, the ledger is lane self-assessment metadata. It must get: no SOURCES.md row (S-numbers are external-source registry cells), no coverage-map row, no PROVINCE row, no frontier-ground claim. The `.md`-only corpus census (r86 spotcheck counts `grep -c '\.md$'` over `corpus/knowledge`) is unaffected by the JSON, so the 73-count does not move; the lesson should name the placement exception so a future census does not flag it as drift or mistake it for an admitted entry.

## 2. r86 outside defects and their round-87 handling (read)

From `.ufo/waves/round-87/snapshots/round-86-verifier-spotcheck.md` (defects section + routed defects 1–3):

| r86 outside defect | Current state (my check) | r87 surface |
|---|---|---|
| (a) untracked 1.2 M `rfc9110.html` mirror byproduct in lane repo | **Disposed at filesystem level**: absent at HEAD and never in git history (evidence.md §7). A sibling `rfc9110.txt` (502,941 B) at the same path has been **tracked since r86 carrier `3f2de0fd`**, predating the spotcheck that named only the html | ScribeLesson carries the "r86 inherited scratch mirror disposal" item; the txt's receipt status (kept-as-evidence vs remove) should be stated, not silently inherited |
| (b) register data-row quarantine sweep ran **after** the SOURCES append | Not yet re-formed | Integration order this round: quarantine sweep **before** any SOURCES append (S462) |
| (c) W04 census warnings 22→23 (intentional S461 duplicate URL) | Disclosed, intentional | No action; do not "fix" by deduplicating a disclosed intentional row |
| C1-r86 self-certifying predicate (after-receipt green + cross-claim dependency → unprovable) | Structural cause | r87 C1 is designed against it: no receipt or claim output is an input; snapshots committed, base/freeze do-nothing is red on both claims (evidence.md §2) |
| D84-4 planner routing | **Open**: fleet `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:294` (`kake | round-86`) unanswered; lane-side l0 file does not exist | Contract: "existing D84-4 operator question remains open, not silently resolved"; lane must not edit the fleet L0 file or claim mitigation = settlement |

## 3. C2 boundary proof: age arithmetic only

Contract C2 exclusion list: no clock, no network in the tool, no Date parser, no storage/reuse approval, no Cache-Control interpretation, no browser behavior; missing Date unsupported; "no synthetic request timing may be relabeled as observed timing". The formulas are exactly the six §4.2.3 terms (apparent_age clamp, response_delay, corrected_age_value, conservative max, resident_time, current_age). The conservative max is "a chosen allowed profile, not the RFC's sole permitted algorithm" — the knowledge entry must keep that boundary (ScribeKnowledge spec already does).

**Frontier delta shown against current bytes**: `corpus/README.md:665-668` (r86 close) says "General policy equivalence, the independent changed-row oracle, full HTTP extraction, **Age/Vary/Pragma**, browser/runtime cache behavior and live property repair remain frontier." C2 moves exactly and only the offline-arithmetic slice of "Age".

**The one real integration risk (my bounded proposal):** when ScribeRegistry/L1 update README/PROVINCE, the frontier wording must **split Age into two layers**:
- *held by C2*: current-age **arithmetic on supplied integer epochs** under the conservative §4.2.3 profile (`scripts/cache_current_age.py`);
- *still frontier*: **Age/Date header extraction, parsing and validation** (C2 has no Date parser — an invalid/missing Date in the trial is "could-not-evaluate", never fabricated), Vary, Pragma, browser/runtime cache behavior, storage/reuse authorization, general policy equivalence (D84-3), live property repair.
If the integration prose shortens "Age/Vary/Pragma remain frontier" to "Vary/Pragma remain frontier" without the arithmetic/extraction split, a future round can read C2 as licensing Age-header interpretation — over-broadening into S461's neighbor and D84-3's retained-open general-semantics debt. This single wording constraint is the cheapest way to keep freshness moving without harming calibration/evidence-fidelity.

**No sibling province absorption**: per w1-spec (evidence.md §9), every sibling stays inside kake's publisher-side domain; the excluded surfaces (browser → tabi, storage/reuse approval → operator, publishing → operator, method/secrets/model-serving → chousa/kagi/kama) are named as out of scope in the sibling items themselves. PROVINCE "Refuses" clause respected; the ExecTrial GET is one owned public property (https://ds4cc.com/), GET-only, sanitized — in-domain.

**Duplicate-capability scan (bounded grep, evidence.md §6)**: no script in `scripts/` matches `current_age|apparent_age|corrected_age|age_value|resident_time|response_delay`; no `cache_current_age*.py` anywhere in the worktree; S462 unused in SOURCES.md. Nearest neighbor `scripts/cache_control_effective.py` is directive-level freshness-lifetime reading (r86 coverage row) — complementary, not duplicate; its row explicitly says "not cache storage/reuse authorization". New name is clean.

## 4. D84-3 and D84-4 verified still open

- **D84-3** (general-classifier semantic/input-dependence debt): `corpus/README.md:680-682` retained-open with flip: conditions ("field-specific order/duplicate rules and an independent changed-row oracle verify together; this field reader alone does not close it"); contract C2 mined source is scoped to "§4.2.3 conservative age arithmetic (not S461's duplicate/lifetime scope)" and claims no equivalence result. Nothing in either claim asserts generic policy semantics. **Stays open.**
- **D84-4** (literal dispatched L2 planner vs validator prohibition): fleet L0 line 294 unanswered (plus kotodama line 295, same conflict); contract: "existing D84-4 operator question remains open, not silently resolved"; "validator forbids planner role; L1 planner; bounded planning data-walk on scout" is the recorded mitigation only. **Stays open.** No sibling item answers or closes it; the fleet L0 file is outside all lane write scopes this round.

## 5. Concrete integration checklist (for L1; no edits made by this seat)

1. Commit `corpus/knowledge/gate-agreement-ledger.json` as a **bare JSON array of exactly the 8 expected rows** (ExecLedger candidate), each row data-equal to `expected-ledger.json` (keys `round,item,decision,outside,source,sha256`); no wrapper, no metadata fields (count.py list + exact-equality + no-additional-rows logic).
2. Classify in prose only: README/lesson sentence "self-assessment artifact, not an admitted domain knowledge entry" (contract wording); no SOURCES row, no coverage-map row, no PROVINCE row for the ledger.
3. Commit the three snapshot files `.ufo/waves/round-87/snapshots/round-{84,85,86}-verifier-spotcheck.md` **byte-identical** (digests in evidence.md §1); the counter re-verifies them at the scored revision; never re-fetch or edit them.
4. Integrate exactly one production `scripts/cache_current_age.py` (ExecAge candidate): sequential arithmetic, stdlib, stdin/stdout JSON, integer-not-bool, negative date allowed, ordered nonnegative local times, `age_value` default 0, exit 1 + `invalid_input` diagnostic, `--selftest` via real subprocess, **frozen cases never imported into the production tool**.
5. Knowledge entry `corpus/knowledge/cache-current-age.md` (ScribeKnowledge) with S462 provenance trio; keep "conservative max is an allowed profile, not the RFC's sole permitted algorithm" visible; never broaden S461.
6. SOURCES append S462 (ScribeRegistry, 11 cells, `used-by` exactly `corpus/knowledge/cache-current-age.md`) — **run the register data-row quarantine sweep before this append** (r86 defect (b) route). S462 verified unused today.
7. SKILL.md probe registry row: `cache_current_age`, code0 `clean calculated` / code1 `failed invalid_input`, pinned oracle `.ufo/waves/round-87/age-cases.json`, stdin/out only, owner kake.
8. README coverage row + PROVINCE scoped frontier update with the **Age arithmetic-vs-extraction split** (§3 above); retire only the arithmetic slice from the frontier list; keep Vary/Pragma/extraction/browser/storage-reuse and D84-3 general-equivalence language intact.
9. ScribeLesson records: r86 inherited mirror disposal state (html gone — never committed; tracked `rfc9110.txt` since carrier `3f2de0fd` — state its receipt status explicitly), quarantine-before-append rule, assimilation none, ledger-is-metadata statement, and "outside spotcheck remains closure-owned".
10. ExecTrial: one GET, sanitized record (Date/Age/Cache-Control/status/final URL/times/bodysha/bytes only), runner offline with `now` fixed to recorded trial_now; missing/invalid Date → honest could-not-evaluate, no fabricated inputs; no cookies/auth retained.
11. Do-not-touch set: `.ufo/waves/round-87/{contract.md,count.py,age-cases.json,expected-ledger.json,controls/*,snapshots/*}` after scoring; fleet `.ufo/l0-questions.md` (D84-4 stays operator-owned); no D84 queue-closure claim anywhere.
12. Scoring order for L1: `python3 -B .ufo/waves/round-87/count.py --selftest`; c1 at base and at integration/freeze revision; c2 with `--work` under L1 scratch; controls already committed show base red (`controls/base-c1.txt`, `base-c2.txt`, `no-work-*.json`).

## 6. Risks

- **Ledger false-accept ceiling**: a copied lie passes; designed counterweight is ExecLedger's independent per-source-table comparison plus reviewer predicate attacks; admission stays outside-owned. Say "recorded agreement", never "calibration established".
- **Frontier over-narrowing** on the Age wording (§3) — the single highest-leverage defect class this round.
- **knowledge/-path placement** of a JSON metadata file can be misread by future censuses/humans as a domain entry; prose-only classification is mandatory and fragile — keep it adjacent and explicit.
- **Scratch hygiene**: the r86 html debt shows wave-tree byproducts leak into the lane repo; ExecAge/ExecTrial/MutAge temp files must stay inside their own dirs/scratch.

## 7. Verification done by this seat (and limits)

Verified by direct tool observation: snapshot digests, expected-ledger bindings, base/freeze object existence and target absence, 8-row table agreement across all three snapshots, fleet L0 line 294 presence/unanswered, README debt block and frontier lines, scripts/ duplicate-capability grep, S462 id availability, mirror disposal state, age-cases shape, sibling scope text. **Limits**: I did not run count.py itself (ReviewCounter/ExecLedger own the authorized counter runs), did not re-open RFC 9111 (ScoutAge/ReviewAge own the GET), did not compare ExecLedger's candidate rows cell-by-cell against source tables (ExecLedger's assignment), and made no edits. No installs. Scratch deleted; receipts retained in `.ufo/waves/round-87/w1/ConnectorScope/evidence.md`.
