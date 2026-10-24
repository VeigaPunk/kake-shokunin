# ReviewQualityCriteria — QUALITY.md captured-by audit and Fails-if predicate sweep

Axes: **operability** (do the criteria make counter defects rejectable before admission), **freshness** (criteria checked against current file bytes at f7de3ab4e9f030a15a857a5a08631bd8e690f436 worktree, 2026-10-21). Author-side review; no admission claimed. Read-only on the lane; only this file written. No subagents (leaf bound).

## Verdict

**captured-by: none.** No criterion in `corpus/QUALITY.md` — neither the 13 round-20 table rows nor any round-21/22/23 appended section — should have caught the round-23 lexical `observedAt`/`fetchedAt` prefix test or the `served()` non-string `contentType` crash before round-23 admission. The three nearest criteria all fail to fire on their written scope (details in F1). The Fails-if sweep found exactly three predicates: the known inverted one at `QUALITY.md:106` (corrected by the r23 register at `:121-127`; confirmed accurate against probe source), and two correct ones at `:111` and `:142-144` (verified against probe source). No unfalsifiable predicate found.

## Findings

### F1 — P2: Both known round-23 counter gaps are captured by no criterion (captured-by: none)

- **Exact commands (read/grep on the admitted revision's worktree):**
  - `grep -n "observedAt" .ufo/waves/round-23/measure_c1.py`
  - `grep -nE "def served|contentType|fetchedAt|Exit 0 iff" .ufo/waves/round-23/measure_c2.py`
  - `grep -n "TODAY|observedAt|contentType" .ufo/waves/round-23/counter_selftest.py`
- **Exact observed output (abbreviated faithfully):**
  - `measure_c1.py:55`: `if not isinstance(receipt.get("observedAt"), str) or receipt["observedAt"][:10] < "2026-10-21":` — any string whose first 10 chars sort ≥ `"2026-10-21"` passes: `"2099-01-01T00:00:00Z"` (future), `"zzzz-not-a-date"`, and `"2026-10-21GARBAGE"` (malformed shape, `[:10]` still matches). No RFC 3339 parse despite docstring `measure_c1.py:9` "observedAt >= 2026-10-21".
  - `measure_c2.py:56`: identical lexical test on `fetchedAt`; `measure_c2.py:37-39` (`served()`): `ctype = fetch.get("contentType") or ""` then `ctype.split(";")` — a truthy non-string `contentType` (number, `true`, array, object) raises an uncaught `AttributeError`: traceback, exit 1. Note `measure_c2.py:15` documents "Exit 0 iff all surfaces pass; 1 otherwise; 2 when inputs cannot be read" — an uncaught exception's exit 1 is indistinguishable from a controlled rejection under that documented contract, so no documented contract is breached either.
  - `counter_selftest.py:20,87,146,166,396,427`: every fixture value is well-formed (`"observedAt": TODAY`, `"contentType": "text/html; charset=utf-8"`; negative cases use only `"2026-10-20"`, wrong-path, empty claims, bad digest, `status: None`). No malformed-token, future-token, or wrong-type case exists anywhere in the selftest.
- **Why no criterion fires (the audit):**
  - `QUALITY.md:107-111` ("Every URL-resolution branch of a gate has a one-character adversarial neighbour…") is explicitly scoped to **URL-resolution branches** and to a **one-character** neighbour of a frozen case. `observedAt`/`fetchedAt`/`contentType` are receipt-field parses, not URL-resolution branches; and a one-character neighbour of `"2026-10-21"` is by construction well-formed (`"2026-10-20"`), which is exactly the class r23's mutants tested — it cannot generate `"zzzz…"`, `"2099-…"`, or a non-string type.
  - `QUALITY.md:112-115` (output contract "always one JSON object" covering every exit path) is conditioned on such a contract being **documented**; the measure runners document exit codes only (`measure_c1.py:126` docstring tail, `measure_c2.py:15`), so the traceback path breaches nothing written.
  - `QUALITY.md:102-106` (counter-probe) attacks numerator-vs-rows consistency and baseline validation only; its CE1–CE3 never feed malformed receipt fields.
  - `QUALITY.md:138-144` (relaxation probe) is scoped to `scripts/canonical_audit.py` parser-relaxation feed paths, not the counters.
  - `QUALITY.md:145-148` and the falsifier clarification at `:154` ("A counting command validates receipt structure and replay consistency, not the truth of a claimed GET/HOLD") state what counting commands do but carry no fails-if predicate and no malformed-input mandate.
  - Table rows `QUALITY.md:9-20` (e.g. "Replayable claim" `:10` — frozen input expectations pin their bytes) pin bytes of *used* inputs; none demands an adversarial input class.
- **Corroboration that r23's own adversarial battery missed it for the same reason:** `w1/MutateCounterC1.md:57,70,92-95` — the `mutant-drop-observed-at` mutant (the exact line `measure_c1.py:55` replaced by `if False:`) was **KILLED** solely by the well-formed `observedAt-2026-10-20` case; mutant-kill equivalence is not malformed-class coverage. `w1/MutateCounterC2.md:159,168` — `stale-fetchedAt` likewise well-formed. `w1/CritCounterC2.md:44` — the r23 critic inspected `served()` and flagged only the status-shape hole ("does not require an integer HTTP response status"), not the `contentType` receiver crash.
- **Impacted claim/axis:** C2 operability (round-24 contract: replay must reject malformed receipts with exit 1 or 2, never a traceback) and C1 freshness (a freshness count can be earned with a future or malformed `observedAt`, so "17/17 fresh" is not earned by the date gate).
- **Smallest fix:** append (never rewrite; `QUALITY.md:28-29` and the post-review ruling `:31-40` require pure new-line additions / superseding rows) one criterion row, e.g. "Receipt-field parsing (r24)": every externally-supplied field a counter or gate consumes (a) is parsed with a real date/time parser or fully format-checked — a prefix slice compare is never the validator, generalizing `:110-111` beyond URL resolution; (b) is type-checked before any method call on it; (c) has one probe per adversarial class (malformed token, future token, wrong type), with controls staying accepted. Fails if that probe against the counter exits nonzero. This makes the round-24 C2 runner fix (`scripts/receipt_replay.py`, reject-with-exit-not-traceback) a criterion obligation rather than a one-off repair.

### F2 — P3 (known, already corrected): `QUALITY.md:106` Fails-if predicate is inverted

- **Exact commands:**
  - `grep -n "Fails if" corpus/QUALITY.md`
  - `grep -nE "_ok = |passed|return 0 if" .ufo/waves/round-22/postfix/counter-probe.py`
- **Exact observed output:**
  - `QUALITY.md:106`: `Fails if \`postfix/counter-probe.py\` against the counter exits 0.`
  - `counter-probe.py:71-73,76,78`: `ce1_ok = not (ce1["exit"] == 0 or ce1["accepted"] == 32)` / `ce2_ok = ce2["exit"] != 0` / `ce3_ok = …`; `"passed": ce1_ok and ce2_ok and ce3_ok`; `return 0 if result["passed"] else 1` — the probe exits **0 exactly when every counter-example is rejected**, i.e. when the counter is healthy. As written, `:106` declares the criterion failed by a healthy counter and survived by one that accepts counter-examples (probe exit 1). Inverted in both directions.
- **Disposition:** this is the round-22 verifier's find, already corrected by `QUALITY.md:121-127` ("[r23-correction 2026-10-21] … Read it as: the criterion fails if `counter-probe.py` against the counter exits nonzero (any counter-example accepted). The defect-probe sentence ("exits 1") is correct as written. The original line stays for history."). I verified the correction's semantics against probe source: accurate. Original retained per the append-only rules (`:28-29`, `:31-40`) — correct behavior, no rewrite proposed.
- **Impacted claim/axis:** round-22 "Derived counts" criterion (operability of the quality bar itself).
- **Smallest fix:** none beyond what exists; the F1 row may restate the corrected reading so the r22 section is never read alone.
- **Verified from source, not re-executed** — see Limits.

### F3 — held, correct: `QUALITY.md:111` (defect-probe)

- **Exact command:** `grep -n "exit 0 only|return 0 if" .ufo/waves/round-22/postfix/defect-probe.py`
- **Exact observed output:** docstring `defect-probe.py:6-7` "exit 0 only if every probe meets it"; `defect-probe.py:114` `return 0 if ok else 1`. Exits 1 exactly when some wave-2 defect expectation is unmet, so "Fails if `postfix/defect-probe.py` against the gate exits 1" (`QUALITY.md:111`) has the correct direction. Matches the register's `:126-127`. Not inverted, falsifiable (runnable command; runner recreated per `.ufo/waves/round-22/postfix/REPRODUCE.md` per the `:128-130` rule).

### F4 — held, correct: `QUALITY.md:142-144` (relaxation probe)

- **Exact command:** `grep -n "Exit 0 iff|return 0 if" .ufo/waves/round-23/relaxation_probe.py`
- **Exact observed output:** docstring `relaxation_probe.py:9` "Exit 0 iff every expectation holds"; `relaxation_probe.py:69` `return 0 if ok else 1`, where `ok = all(row["ok"] …)` over attacks (expect not clean) and controls (expect clean). Nonzero iff an attack reaches `clean` or a control breaks — exactly the criterion's failure condition. "Fails if … exits nonzero" is correct and falsifiable (exact argv at `:143`).

## Checked and held

- **Completeness of the Fails-if sweep:** `grep -n "Fails if" corpus/QUALITY.md` returns exactly three predicate sites: `:106`, `:111`, `:142-144`. A wider sweep for predicate wording (`[Ff]ails|[Mm]ust (not |never )?(see|exits?|reject|accept)|never with`) surfaced only: `:17` ("must see each one caught" — mutation-case mandate, direction correct), `:105` ("An unmeasurable baseline … exits nonzero" — consistent with `counter-probe.py:72` `ce2_ok = ce2["exit"] != 0`), `:112-115` ("last value wins never decides a verdict" — fine), `:125` (the correction itself), `:154` (descriptive clarification, no predicate). No fourth Fails-if, no additional inversion, no unfalsifiable predicate (all three name runnable commands with resolvable paths).
- **Round-20 table rows** (`QUALITY.md:9-20`) reviewed for applicability to the two gaps: none reaches receipt-field parsing (see F1). "Replayable claim" (`:10`) is the closest in spirit but pins bytes of used inputs; it does not demand adversarial classes.
- **Known-gap statements taken as ground truth** (lane rules: user-reported failures are not re-run to confirm); both code paths independently confirmed by reading `measure_c1.py:55-56`, `measure_c2.py:36-39,56-57`. The `r23Observed` case runs belong to the executor seats (e.g. GapC2ContentType), not this review.
- **Read-only honored:** no lane production file touched; no git/jj mutations in the lane; no sibling-lane or fleet writes. No tools installed or updated (in-lane probes sufficed; nothing to record under the tooling directive).

## Limits

- **No LSP device** is mounted in this seat's tool inventory and no language server answers `.md`/`.ufo` scripts; per role fallback, verification is direct source reads and line-pinned greps of the actual runner/probe code (semantic reading of the real code paths, not just text matches).
- **Probe exit semantics verified from source, not execution:** the inversion (F2) and the two correct directions (F3, F4) follow unambiguously from the cited `return` statements and docstrings; I did not re-execute the historical probes against a clone. An actual counter-probe replay (clone + 3 measure runs) was skipped as duplicative of the documented r23 correction and the executor lanes' round-24 work.
- **No admission authority:** findings here are author-side recommendations; the L1 (KakeR24) holds the planner seat and sole integration write. The F1 criterion row is a proposal for the round's append, not an edit.
- Scope was the two ticketed questions; the correctness of the round-24 `receipt_replay.py` fix itself is owned by its executor/reviewer seats.

Report: .ufo/waves/round-24/w1/ReviewQualityCriteria.md
