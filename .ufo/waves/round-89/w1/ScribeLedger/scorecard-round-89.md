# DRAFT — SCORECARD.md `## Round 89` section (ScribeLedger, wave 1)

Measured at lane HEAD `acc69ba59af9ddff84a704331087b9147cc0aa1b`. L1 must re-measure at its
own final carrier and replace every `acc69ba5` below if the carrier moves. This draft
supersedes the landed section (commit `28532540`, edited by `658f72f8`): its C1 numbers were
measured before the round-89 lesson markers landed, and its C2 row understated the
instrument's admitted set.

## Round 89 — routed-defect closure, a cache-key constructor, and two unadmitted claims

Base `76225160d0dff8d2042fbcd037bd08b0971d5e07`; freeze `08ab46a1`; dispatch `2e700b9a`;
freeze v2 `46a43e94`, committed after dispatch and disclosed in `corpus/lessons/round-89.md`.
Candidate `scripts/cache_key.py` (blob `13ea9374`, sha256 `3a658326…`). Counters
`.ufo/waves/round-89/c89_defect_queue.py` (sha256 `0ebea07f…`) and
`.ufo/waves/round-89/c89_key.py` (v2 sha256 `d4588d4b…`; frozen v1 `a72d5efc…`).

integrated-selftest: 35/35

| Claim | Axis / score delta | Before → after | Counting command | Evidence / author verdict |
|---|---|---|---|---|
| C1 six routed round-88 defects close | calibration 2→2 HOLD, lowest owned | freeze-time base `open=6 closed=0 met=false`, exit 1 → `open=1 closed=5 met=false`, exit 1 at `acc69ba5`; the one open item is A (untagged `22/22` at `SCORECARD.md:5469`, `:5488` and `corpus/lessons/round-88.md:265`) | `python3 -B .ufo/waves/round-89/c89_defect_queue.py --root . --revision <REV> --work <explicit-scratch>` | **Not met.** B, C, D, E and F read closed, but the wave review (RC-1, RC-2, RC-8, RC-9, RC-10) shows the counter's B, C, E and F cannot tell repair from prose, so those closures are not evidence of repair. The base control does not reproduce with HEAD past dispatch: the same counter at `76225160` prints `open=5 closed=1` (`controls/c1-base-revision-control-at-acc69ba5.txt`, RC-1). No score change. |
| C2 conservative Vary-nominated cache-key construction | freshness 10→10 HOLD; declared axis disputed (the contract disclaims freshness; the critic places it under operability or coverage, D89-C2-6) | candidate absent `frozen=0/16 props=0/200 refuse=0/9 controls=5/5 met=false`, exit 1 → `frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true`, exit 0, under both the v2 counter and the frozen v1 counter | `python3 -B .ufo/waves/round-89/c89_key.py --root . --revision <REV> --candidate scripts/cache_key.py --work <explicit-scratch>` | **Met by the instrument; not admitted.** The counter also accepts non-conforming candidates: seven of ten adversarial probes (`w1/ExecControls.md`); values stripped of all whitespace (the contract trims SP and HTAB only) and a URI without escaping, both at four seeds, and a 421-entry table over the committed seed (`w1/CriticClaims.md`); runtime, alias, `file://` and environment imports, a hybrid literal table, and a textual guard bypass (`w1/ReviewCounterC2.md`). Mutation: 27/37 killed, seven real survivors (`w1/MutKey.md`). Met is a sample result, not conformance. No score change. |

Receipts are under `.ufo/waves/round-89/`: `controls/base-c1.txt` (freeze-time C1 base);
`controls/c1-selftest.txt` (12/12); `controls/base-c2.txt` (v2 re-run of the C2 base) and
`controls/base-c2-freeze-v1.txt` (freeze-time bytes, restored); `controls/c2-carrier-frozen-v1.txt`
and `controls/c2-carrier-v2.txt`; `controls/c2-selftest.txt` (43/43). Re-measured by the
scribe at `acc69ba5` under `w1/ScribeLedger/receipts/`: `c1-at-acc69ba5.txt`,
`c1-base-revision-control-at-acc69ba5.txt`, `c2-v2-at-acc69ba5.txt`,
`c2-frozen-v1-at-acc69ba5.txt`, `c1-selftest-run.txt` (12/12), `c2-selftest-run.txt` (43/43),
`candidate-identity.txt`, `candidate-selftest-mode.txt`, `trial-committed-run.txt` and
`trial-committed-results.json`. The superseded `1b0f1008` C1 measurement is kept as
`c1-at-1b0f1008-superseded.txt`.

Integrity, stated plainly: freeze v2 changed the C2 counter's shortcut guard after dispatch,
and the item-E check cannot see that change (RC-2; `w1/CriticClaims.md` §2.4), so E's closure
is closure on the frozen predicate only. The freeze-time base receipt for C2 was overwritten
in place and is restored beside the v2 re-run. The C2 predicate's "frozen before any data"
sentence is therefore true for the frozen claim text and false for the counter file.

Move log (round 89):

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 89 | calibration (HOLD 2) | `open=6 closed=0 met=false`, exit 1, at freeze `08ab46a1` (`controls/base-c1.txt`) | `open=1 closed=5 met=false`, exit 1, at `acc69ba5`: item A open; B, C, D, E, F closed by a counter the wave review found defective | `.ufo/waves/round-89/controls/base-c1.txt`; `w1/ScribeLedger/receipts/c1-at-acc69ba5.txt`; `corpus/lessons/round-89.md` |
| 89 | freshness (HOLD 10) | candidate absent, `met=false`, exit 1, at `76225160` (`controls/base-c2.txt`) | candidate `3a658326` meets the v2 and frozen-v1 counters, exit 0; the instrument admits non-conforming candidates, so the score does not move | `.ufo/waves/round-89/controls/{c2-carrier-frozen-v1.txt,c2-carrier-v2.txt}`; `w1/ScribeLedger/receipts/c2-*-at-acc69ba5.txt` |

### Demonstrated repertoire — round 89

| Capability | What it can do | Evidence | First-working round |
|---|---|---|---|
| Canonical Vary-nominated cache-key construction (key only) | From a URI, a request header map and a `Vary` value, produce the stored-response key under the declared form (sorted lowercased members, byte-exact trimmed values, escaped separators, absent distinct from present-empty), or refuse malformed input with `invalid_input:` and exit 1. Demonstrated on the frozen counter, twelve committed-candidate trial cases (seven recorded surfaces, five synthetic refusals) and the lane's knowledge entry. Not conformance: the instrument admits non-conforming candidates. Not storability, reuse, revalidation, freshness or serving. | `scripts/cache_key.py` (blob `13ea9374`, sha256 `3a658326`); `corpus/knowledge/cache-key-construction.md` (S464, S465); `w1/ExecTrial.md`; `w1/ScribeLedger/receipts/trial-committed-results.json` | 89 (demonstrated; instrument not admitted, R89-2) |

### Planned — after round 89

Outside closure owns admission and the admit/reject spot-check; neither claim is admitted by
this round's own measurements. Round 90 routes the wave-review defects. For C1: RC-1 (item E
reads HEAD, not `--revision`), RC-4 (mirror mode skips E), RC-9 (item C sees only the full
`round-88/controls/` prefix; 16 of 21 named receipts are unchecked), RC-7 and RC-5/RC-6 (item A
trusts the tool's self-report and accepts any `[r89-correction` line in any scope), RC-8 (item B
classifies by substring) and RC-10 (item F matches header substrings). RC-2 and RC-3 change the
frozen E claim and need an explicit claim decision. For C2, "one frozen item per clause" is not
enough: the guard is textual and is defeated by runtime-built import paths and `file://` reads,
and the property classes assert relations (same or different) and never the key string. The
instrument needs key-string assertions against a declared oracle, a behavioural guard or none,
and the uncovered clauses (duplicate members, URI and name escaping, CR-only, missing headers,
malformed JSON, case-sensitive member order, and the every-header CR/LF and case-duplicate
refusals). The contract needs decisions on three points: the combination of duplicate `Vary`
header lines (the ExecTrial driver joins them with `, `; the contract is silent), the fourth
separator U+001D (the reference escapes it, the contract names three separators, and its GS is
U+001C where ASCII has FS), and the behaviour for duplicate JSON keys and CTL bytes in
non-nominated values. The C2 axis label is a claim decision. Frontier stays open: cache-key
storage, revalidation, freshness and serving; browser Vary and Pragma behaviour; the D84-2/3
debt and the operator-owned literal L2-planner item D84-4. No round 90 is started here.
