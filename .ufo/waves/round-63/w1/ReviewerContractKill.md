# Round-63 w1 — ReviewerContractKill — kill-rule coverage review

Seat: ReviewerContractKill (leaf; no subagents, no commits, no mutations).
Scope: the kill rules in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/contract.md` (C1 kill rule L42-45, C2 kill rule L70-71, preamble L3-6, Separability L75-81, No-harm L84-87), against the four attack classes (a)-(d) in my lane task. Claims, counters, receipts untouched; the only file I wrote is this report.
Method: static reading of the contract and both frozen counters; read-only git inspection at the measured commit. No tool installs. I did not re-execute counters or rebuild fixtures (sibling seats hold rerun/reproduction lanes); runtime claims below are cited from committed receipts.

## 0. Ground state verified (read-only)

Measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` resolves (`git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse --verify 05b0d7f4...^{commit}` → full id). All contract-frozen sha256s match the committed bytes at that revision:

| Artifact | Contract sha | Measured-commit sha | Match |
|---|---|---|---|
| `.ufo/waves/round-63/c63_calibration.py` | `bcd16f68…a3fc91` | `bcd16f68…a3fc91` | yes |
| `.ufo/waves/round-63/c63_quote_tool.py` | `9fcbfad0…f01e` | `9fcbfad0…f01e` | yes |
| `.ufo/waves/round-63/quote-class/quote-classes.json` | `5f48e26b…c42d` | `5f48e26b…c42d` | yes |
| `scripts/quote_class.py` | `431e75e8…1f14` | `431e75e8…1f14` | yes |

Ledger↔blob anchors at the measured commit: ledger `textSha256=8b90d096…2a69` == sha256 of `.ufo/waves/round-63/quote-class/S432.txt`; `rawSha256=63b0a018…911b` == sha256 of `.ufo/waves/round-61/sources/S432.html`; span present in collapsed text (1 hit), absent from raw HTML (0 hits) → `collapsed-only` consistent. Round-62 routed-defect receipt exists: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/controls/counter-false-green-l1.txt` (marker tokens green, `source_file_present=no`).

## 1. Answers to (a)-(d)

(a) **Green after-receipt from a tree that games one component — PARTIAL.**
C1's `resolved` is a four-way conjunction (`quote_correction and criterion and lesson_gate and source_row`, `c63_calibration.py:157-159`), so a tree cannot green with one component merely missing. But three of the four components are pure substring checks (`criterion`: `"substantive"`, `"round-61-verifier-spotcheck"` + `PURPOSE_TERMS`, `c63_calibration.py:147-150`; `lesson_gate`: `"## Gate"`, `"Disagree"`, `"collapsed-only"`, `"author-side"`, L151-156; `source_row`: regex `^\|\s*S432\s*\|`, L152 area) — a tree that plants one component's strings while the others are genuinely met greens. The one expensive component, `quote_correction`, is itself gameable without any marker-only green: the counter re-derives blob shas **from the attacker-controlled ledger itself** (`c63_calibration.py:133-136`) and never pins the ledger file to the contract-frozen `5f48e26b…c42d` (the string `5f48e26b` appears nowhere in the counter). Appending the span to `S432.txt` is even no-harm-compatible (append-only), and a matching ledger row update greens `quote_correction` alone [INFERENCE from `classify()` substring semantics at L57-64 and the blob/ledger code path — not executed]. Neither C1 kill trigger fires: the after receipt prints `met=true`, controls are untouched, and the green is **not** a "marker-only green" — blobs exist.
C2 has a single component (tool+selftest). Gaming it = swapping `scripts/quote_class.py`; the counter never checks the tool sha (no `hashlib` import in `c63_quote_tool.py`), so any implementation whose `--selftest --json` reports `total=4, passed=4, ok=true` with the four frozen ids and self-consistent `derived==expected` fields greens (L77-85 — both fields are tool-reported, never independently re-derived). The only kill trigger is the subjective "a stub tool passes" (contract L70-71).

(b) **Control regression — C1 PARTIAL, C2 NO.**
C1: "or either control prints `met=true`" (L43) — but C1 commits **three** control receipts (`base-c1.txt`, `control-marker-fixture.txt`, `control-junk-fixture.txt`, L37-40). "Either" literally covers two; whichever two are intended, the third control's regression does not trip the kill rule by the letter. C2: the kill rule (L70-71) contains **no control clause at all** — a `base-c2.txt` regression (`present=0 met=false` → `met=true`, i.e. a counter swap or weakening) would not make C2 unprovable by the letter. Asymmetric with C1.

(c) **Wave attack reproducing a marker-only green — C1 YES (species-bound), C2 NO.**
C1 names it explicitly: "or any wave attack reproduces a marker-only green" (L43-44). This covers the round-62 routed-defect species broadly (any marker-only tree, not only the committed fixture). But it is species-bound: a wave attack demonstrating a **different** false-green species (fabricated-blob green per (a), junk-fixture-with-blobs, planted component strings on a blob-bearing tree) is not named. C2 has no wave-attack clause whatsoever; a wave attack demo (e.g. a tool whose selftest prints the frozen JSON verbatim) trips the rule only if seats independently classify it a "stub".

(d) **Seat-discovered counter bug — PARTIAL both.**
A seat-discovered C1 bug is covered by the letter only if its demonstration manifests as a marker-only green; a bug producing any other false green is unnamed. A seat-discovered C2 bug is covered only via "a stub tool passes" — a judgment term with no mechanical definition; a faithful-looking reimplementation of the four frozen cases is not obviously a "stub". Crucially, **no kill trigger in either rule binds any frozen sha256 to claim validity** — not the two counter shas, not the tool sha, not the ledger sha. A counter swapped for a revision-conditional one (green only at `05b0d7f4…`, red at base/fixture revisions) greens the after receipt while every control stays red: no trigger fires. The preamble (L4-5, "a counter, control or predicate changed after a seat has scored is not this round's rule") makes this worse, not better: rules cannot be tightened retroactively, so an unnamed trigger class stays unnamed for the round.

## 2. Findings by severity

**HIGH-1 — No kill trigger binds measured-artifact identity (frozen sha256s) to claim validity; a swap greens through the letter of both rules.**
Evidence: `c63_quote_tool.py` contains no sha check of the tool (no `hashlib` import; tool blob is hashed nowhere — L60-71 just executes it); `c63_calibration.py` uses `hashlib` only to re-derive per-row blob shas from the ledger itself (L134-135) and never compares the ledger file to `5f48e26b…c42d`; C1 kill rule L42-45 and C2 kill rule L70-71 reference only output strings. Attack: (i) revision-conditional counter swap → after receipt green, base/marker/junk controls red → C1 verifies falsely; (ii) tool reimplementation passing the four frozen case ids → after receipt green → C2 verifies falsely unless seats vote "stub". Contract-frozen shas exist for all four artifacts (L17-18, L24, L52) but are wired into nothing mechanical.

**HIGH-2 — C2 kill rule lacks control-regression and wave-attack triggers (asymmetric with C1).**
Evidence: C2 kill rule L70-71 has exactly two triggers (after receipt not met; stub tool passes). C1 has three (L42-44) including controls and wave attacks. Consequence: a `base-c2` regression to `met=true` (counter swap/weakening) or a demonstrated C2 false-green wave attack is not, by the letter, an `unprovable` event.

**MED-1 — C1 wave-attack clause is species-bound; the one-component `quote_correction` game (blob+ledger fabrication) is an unnamed false-green species.**
Evidence: L43-44 ("a marker-only green"); `classify()` L57-64 makes the class a substring property of whatever text blob the tree commits; the counter trusts the in-tree ledger for both blob anchoring and the recorded class (L122-141); no raw→text derivation check (e.g. re-running `extract_text.py` semantics) and no frozen-ledger-sha check. The fabricated-blob green reproduces the *effect* of the routed defect (green without genuine retained evidence) but not its *species*, so L43-44 does not catch it by the letter.

**MED-2 — "either control" (L43) vs three committed C1 controls; one control is literally uncovered.**
Evidence: L37-40 lists `base-c1.txt`, `control-marker-fixture.txt`, `control-junk-fixture.txt`. Whichever pair "either" denotes, the third receipt's regression to `met=true` is outside the trigger set.

**LOW-1 — False-kill trap: `control-marker-fixture.txt` legitimately contains a literal `met=true` line (the old-c62 defect demo, line 5 of the receipt).**
A literal application of "either control prints `met=true`" to receipt text kills C1 on the committed control as written. The rule needs the qualifier "on the repaired-counter (c63) line". This direction false-kills rather than false-verifies, but it is the same sentence's defect.

**LOW-2 — No-harm violations have no stated kill consequence.**
L84-87 constrains edits (append-only, S432 cells untouched, ledger implicitly immutable via its frozen sha) but the preamble (L5-6) defines consequences only for "kill-rule breach". A no-harm breach that greens a claim (e.g. the append-only span insertion in MED-1) breaches no kill trigger by the letter.

## 3. Recommendations (recommendations only — I edited nothing)

1. Wire the frozen shas into the kill rules: "or any frozen sha256 at the measured commit differs (C1/C2 counters `bcd16f68…`/`9fcbfad0…`, C1 ledger `5f48e26b…`, C2 tool `431e75e8…`) ⇒ claim `unprovable`." This closes the swap classes in HIGH-1 mechanically and gives "stub tool" a definition (tool sha ≠ frozen ⇒ stub).
2. C2 kill rule: add "or `base-c2.txt` re-run prints `met=true`" and a wave-attack clause (parity with C1).
3. C1 kill rule: replace "either control" with the enumerated three receipts, qualify the `met=true` check with "on the c63 line", and generalize the wave-attack clause from "a marker-only green" to "any false green demonstrated on any fixture (green without genuine retained-source evidence)".
4. State that a no-harm breach at the measured commit lands the affected claim `unprovable` (or explicitly that it does not, so seats know the boundary).

## 4. Residual risk and verification gaps

- The fabricated-blob/ledger-swap green (MED-1) and the revision-conditional counter swap (HIGH-1) are code-level inferences from the frozen counter sources and contract text, marked [INFERENCE]; I did not execute them (leaf seat, read-only bounds; reproduction lanes belong to sibling seats). Their feasibility rests on `classify()` substring semantics (L57-64), attacker-controlled ledger re-derivation (L122-141), and absent sha pinning — all cited above.
- I did not re-run either counter; `after-c1.txt`/`after-c2.txt` outputs are taken as committed receipts (sibling rerun lanes cover execution).
- The frozen tool's internal selftest semantics were reviewed only via the counter's use of its JSON contract (`c63_quote_tool.py:73-85`), not by reading `scripts/quote_class.py` in full; if the tool's `s432_real` case re-derives from cwd-resolved blobs (freeze note, contract L52-56), the planted-fixture variant of HIGH-1(ii) would additionally require blob plants in the invoking tree — same kill-rule gap either way, since no trigger checks tool identity.
- Ground-state shas (§0) were verified by me this session; everything downstream of them (receipts' exit codes) is cited, not re-executed.
