<!-- Draft for SCORECARD.md — append after the round-80 sections. No earlier line is rewritten. -->

> **Draft status (ScribeRecord, round 81).** Every base-state line below is quoted verbatim from a
> committed receipt and its `file:line` is given. After-state bytes were not on disk when this
> draft was written: each `⟨FILL …⟩` names the receipt file and line to quote at integration and
> the predicate that line must satisfy. Replace a marker with the receipt's own bytes — never
> transcribe a number from this draft.

## Round 81 — measured claims (author-side; closure owns admission)

Frozen contract `.ufo/waves/round-81/contract.md` at `a77b8a19c2b65a07dfbe40aaf7ec86aaeee2f9cb`,
frozen before any seat ran. Base `2e11925500dd5a739376c9108c94616243af0cd4`; round freeze commit
`a77b8a19` (contract, both counters, the junk-tree builder and spec, the C2 expectations file, the
base and junk control receipts, `scripts/wave_seat_record.py`). Amendment 1
(`.ufo/waves/round-81/amendments/amendment-1.md`) at `0a27045e4b1b18ae521c9be508429262fdf993ca`,
landed before any after-state: A1 corrects `p_r80_4` to count only non-empty settled seats (the
contract's own sentence) and adds two selftest fixtures; A2 corrects the S454 anchor from
§15.5.4/§15.5.5 to **§15.5.5 (404 Not Found) and §15.5.11 (410 Gone)**, leaving the frozen
`capture-expectations.json` bytes unchanged. Predicates, item conditions, targets and kill rules are
unchanged. The one re-cut receipt (the C1 selftest, `13/13` → `15/15`) is disclosed in
`.ufo/waves/round-58/receipt-rewrites.json` at `bec3ecf7`. Measured carrier: ⟨FILL the carrier
revision⟩. Wave `w1`: one v1 wave, 15 seats inside the 8–16 band — scout 2, executor 4, scribe 2,
reviewer 4, critic 1, mutation-tester 1, connector 1 (`.ufo/waves/round-81/w1-spec.json`); requested
attack share 6/15 = 40.0 % over the run-15 directive's roles {reviewer, critic, mutation-tester,
labrat}, sentinel excluded; settled share ⟨FILL `python3 -B .ufo/waves/round-81/make_accounting.py`
— quote its `requested 6/15 settled <a>/<b> share=<x> met=<bool>` line and the matching
`w1-accounting.json` fields⟩. Scores held: operability 10 HOLD, freshness 10 HOLD, calibration 2
HOLD.

| Claim | Axis | Before → after | Counting command | Evidence/verdict |
|---|---|---|---|---|
| C1 the round-80 routed-defect queue closes | calibration 2→2 HOLD | base `2e119255`: `C1v1 revision=2e11925500dd5a739376c9108c94616243af0cd4 items=6 open=6 closed=0 met=false`, exit 1 (`.ufo/waves/round-81/controls/base-c81-defect-queue.txt:8`, `:9`) → carrier: `open=6 → open=0` over the same six items ⟨FILL `controls/after-c1.txt:8` verbatim; the frozen predicate requires `items=6 open=0 closed=6 met=true` with `exit=0` on the following line⟩ | `python3 -B .ufo/waves/round-81/c81_defect_queue.py --root . --revision <rev>` | measured met ⟨FILL⟩; counter selftest `selftest: 15/15 passed`, exit 0 (`controls/c81-selftest-c1.txt:17-18`), one green fixture per item plus mutants for the wrong line, wrong arithmetic, wrong count, the 0.25 floor, a drifted accounting record, an empty attack seat excluded (`:11`) and counted (`:12`), an over-built junk tree and a tampered seat record; junk control `C1v1 revision=worktree items=6 open=6 closed=0 met=false`, exit 1 (`controls/ctl-c81-junk-queue.txt:8-9`) |
| C2 a fresh capture feeds the offline audit and the verdict re-derives from committed bytes (capability) | operability 10→10 HOLD | base `2e119255`: `capture: no manifest at the measured revision` and `C2v1 root=kake-shokunin surfaces=0 failures=1 audit_rc=- met=false`, exit 1 (`.ufo/waves/round-81/controls/base-c81-capture-audit.txt:12-14`) → carrier: `met=false → met=true` over the three declared surfaces ⟨FILL `controls/after-c2.txt` — requires `surfaces=3 failures=0 audit_rc∈{0,1} met=true` and `exit=0`⟩ | `python3 -B .ufo/waves/round-81/c81_capture_audit.py --root .` | measured met ⟨FILL⟩; counter selftest `selftest: 12/12 passed`, exit 0 (`controls/c81-selftest-c2.txt:14-15`), with the five mutants (body digest, byte count, stale fetch time, drifted audit receipt, empty manifest) each opening the item |

Move log (round 81):

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 81 | calibration (HOLD 2) | `open=6 closed=0 met=false` at `2e119255`; all six R80 items read open, three of them unsatisfiable from prose alone (pointer, arithmetic, scope count) | `open=0 closed=6 met=true` at the carrier ⟨FILL⟩; each item decided by a conjunct over lane bytes — the registry line computed by the counter, the round-80 constants receipt re-summed, the registry `source` cells re-counted, the settled attack share re-derived, round-80's own counter re-run over a rebuilt junk tree, the seat record re-derived canonically | `.ufo/waves/round-81/c81_defect_queue.py`, `controls/base-c81-defect-queue.txt` → `controls/after-c1.txt`, `controls/c81-selftest-c1.txt`, `controls/ctl-c81-junk-queue.txt`, `.ufo/waves/round-81/junk_tree_build.py`, `scripts/wave_seat_record.py` |
| 81 | operability (HOLD 10) | `surfaces=0 met=false` — no capture tree, no manifest, the audit chain unmeasured | three `ds4cc.com` surfaces captured once, GET-only; receipts committed under `.ufo/waves/round-81/capture/`; `header_audit.py` run offline over the mechanical manifest; the counter re-derives digests, byte counts, status, fetch time, allowlist and audit-output equality ⟨FILL the after line⟩ | `.ufo/waves/round-81/c81_capture_audit.py`, `.ufo/waves/round-81/capture-expectations.json`, `.ufo/waves/round-81/capture/manifest.json`, `controls/base-c81-capture-audit.txt` → `controls/after-c2.txt`, `controls/after-c2-audit.txt` |

### Capabilities acquired in round 81

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Capture-once / audit-offline re-derivation chain | Takes one GET-only capture of a declared surface set, retains each receipt as committed bytes (final URL, integer status, fetch time, byte count, body sha256, retained body, header list), joins the frozen expectations file and the receipts into a version-1 manifest, runs the offline header audit over that manifest, and re-derives the whole chain from the measured revision: every receipt verifies, the manifest's surface count is the audited population, every URL host is inside the manifest's declared allowlist, and the audit's stdout equals the committed audit receipt line-for-line. The manifest-versus-expectations join is the capture task's obligation, not something the counter proves (`w1/ScribeRecord.md` F4). It concludes only what the recorded bytes carry — not that the property is clean, not that the declared policy is universal, and not that an absent resource (404/410, S454) is an audit failure | `.ufo/waves/round-81/c81_capture_audit.py`; `.ufo/waves/round-81/capture-expectations.json`; `.ufo/waves/round-81/capture/manifest.json`; `controls/base-c81-capture-audit.txt` → `controls/after-c2.txt`; `controls/after-c2-audit.txt` | 81 ⟨FILL the round's own `met=true` receipt line⟩ |

Stated limits, not claimed closed: the capture is one GET per URL at one instant — it is a receipt of
the bytes served at `fetchedAt`, not a claim about the property's headers at any other time, and the
published `ds4cc.com/robots.txt` and `/sitemap.xml` were recorded live-404 in the round-14 log
(`LOG.md`, round 14), so an absent answer is recorded under S454 with its status and contributes no
`content_type_present` result (that class reads 2xx responses only); the audit-output equality proves
the committed receipt's bytes and `header_audit.py`'s stdout agree, it cannot prove who wrote the file
— a hand-written file with identical bytes is indistinguishable at this layer and is what the tampered
control and the line-for-line comparison bound, not eliminate; the six expectation classes are the
lane's declared policy read off S430–S433, not a source statement that any surface should serve them;
the C1 counter's R80-4 conjunct measures *settled* seats by non-empty output — amendment 1 A1
corrected the frozen counter, which had counted every results row and so reproduced the round-80
defect it was written to close; the wave's own probe found this before any after-state — so a wave can
meet the floor only by replacing dead attack seats, never by re-labelling them; S454's anchor is
§15.5.5 (404 Not Found) and §15.5.11 (410 Gone) per amendment 1 A2, while the frozen
`capture-expectations.json` string still reads §15.5.4/§15.5.5 and is deliberately left unrewritten; R80-5's rebuilt junk tree is
decided because the builder is committed and deterministic, and its `open=6` reading is stricter than
the contract's `open>0` kill rule — the kill rule is a floor, not the measured value; R80-6's record
re-derives from the results schema, and the schema's `error` field still records only what the
dispatch wrote, so a provider 429 remains asserted outside committed bytes unless the results file
carries it; the C2 counter is a wave instrument under `.ufo/waves/`, so it is outside the round-75
instrument-receipt population (gate-registry rows in `SKILL.md`), and no `scripts/` instrument changed
this round; the freshness axis is held, not re-measured live — ⟨FILL the round's
`node scripts/freshness-sweep.mjs --offline` receipt if the L1 ran one; otherwise say it was not run⟩.
The knowledge population and registry counts at the carrier ⟨FILL: registry rows and the census `W04`
count from `controls/census-after.txt`, derived the same way as the 191-row / 20-`W04` before-state
(`controls/census-before.txt`)⟩.
