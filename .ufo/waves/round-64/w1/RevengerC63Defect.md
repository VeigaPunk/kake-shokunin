# RevengerC63Defect — reverse-engineering the c63 falsification class against round-64

Seat: w1 leaf, round-64 kake. Item: reverse-engineer the c63 falsification class completely and
check c64 against every variant, not just the committed fixtures. Report path (this file).
Everything below was produced in scratch `/fast/scratch/hyaku/kake-r64/RevengerC63Defect/`
(deleted before yield; all decisive evidence lines are copied into this report).

## 0. Environment, revisions, integrity checks

- Tools: git 2.56.0, Python 3.14.8 (system). **No tools installed or upgraded** (none needed;
  pacman channel never touched per host pause).
- Lane repo `/home/vgpnk/Projects/shokunin/kake-shokunin` used strictly read-only
  (`git show/rev-parse/log/diff/status` only). Base `1a48131577ba82c967650561be34e8dba909432a`
  (round-63 tip), measured T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`, receipts
  `cc8add1fa740b920ea5179a71152680ab220c70c` (T0 verified ancestor of cc8add1f via
  `git merge-base --is-ancestor`; cc8add1f adds only the four after-receipt files, +30 lines).
- Frozen-instrument shas re-verified at T0 **as blobs** (`git show <T0>:<path> | sha256sum`), all
  matching contract `.ufo/waves/round-64/contract.md` lines 8–17:
  `c64_calibration.py 5489eb2f3ac498e0…`, `c64_quote_tool.py 96fd64e9a915468a…`,
  `fixtures/build_fixtures.py 7fbd8cbc67c17264…`, `fixtures/stub_tool.py 7c78a05df7870304…`,
  `scripts/quote_class.py 431e75e8fee2c913…` (the frozen C2 tool).
- Pinned claim blobs re-verified at T0: raw `63b0a018753c330a…`, text `8b90d096d2653ce5…`,
  ledger `5f48e26be27975ee…`, recipe `6b0a88cddfa3b712…` (counter constants at
  `.ufo/waves/round-64/c64_calibration.py:66-69`).
- Method: every attack variant is its own git fixture repo built in scratch
  (`git init` + `--allow-empty` commit; `git rev-parse --show-toplevel` asserted equal to the
  fixture dir before commit, per host guard). The **frozen counters were never edited on disk in
  the lane**; counter-edit variants run scratch copies under
  `/fast/scratch/hyaku/kake-r64/RevengerC63Defect/variants/`. Driver:
  `python3 harness.py` (scratch, now deleted; full 46-line transcript embedded in §4).

## 1. What the frozen counters actually bind (reconstructed contract)

`c64_calibration.py` (frozen sha `5489eb2f…`), `evaluate()` lines:

- `:198` — the round-61 spot-check contributes **one integer**: `disagreements = sum("S432" in ln
  and "Disagree" in ln for ln in spot.splitlines())`. The spot file is **never sha-pinned**
  (`PIN_SHAS` `:90-95` covers raw/text/ledger/recipe only) and its text is never searched for the
  verdict span.
- `:206-208` — pins: the four blobs' sha256 must equal the constants; any drift → `pins=0` and
  everything downstream is skipped.
- `:222-243` — recipe re-execution (`load_recipe` imports the **revision blob** `:122-130`),
  output must equal the pinned text blob byte-for-byte; class re-derived inline (`:113-119`);
  located range re-derived over raw lines 6100–6200 (`:163-182`) and must equal the pinned
  `6150-6154` **and** the ledger's `locatedRawLines`.
- `:247-251` — prose gate 1/2: `[r63-correction]` block must contain `FROZEN_QUOTE` and the
  ledger path; QUALITY `## Round-62 criteria` must contain the criterion sentence + 3 terms —
  **pure substring predicates**.
- `:252-259` — prose gate 3 (`lesson_gate`): lesson `## Gate` section must contain `"S432 / Fetch"`,
  `SPOT_VERDICT_SPAN` (`"is only a generic lead-in, not substantive evidence for a
  response-header expectation"`), `"collapsed-only"`, `"c64_calibration.py"`, and
  `"author-side"`/`"self-assessment"` — again **substring-only**, and the spot file is never
  consulted to confirm the span is that spot-check's actual verdict reason.
- `:267-270` — `unresolved = max(disagreements - (1 if lesson_gate else 0), 0)`; `met` requires
  `pins ∧ recipe_rederive ∧ class_match ∧ quote_correction ∧ criterion ∧ lesson_gate ∧
  source_row ∧ disagreements ≥ 1 ∧ unresolved == 0`. So **one lesson-green substring cancels one
  disagreement**, whatever the spot file actually says.

`c64_quote_tool.py` (frozen sha `96fd64e9…`): `:147-157` reads the tool **blob** at the revision
and refuses any blob whose sha ≠ frozen `431e75e8…` (`tool_sha=mismatch met=false`) before
execution; `:168-184` materializes tool + 6 fixture blobs into a scratch tree and runs the tool
there with a scrubbed env; `:200-204` requires every frozen case id present/passed/derived-equal;
`:208-221` re-derives each case itself from the revision's fixture bytes; `:222-223` `met`.

`scripts/quote_class.py` at the frozen sha (T0 blob): `:79-86` the selftest genuinely
`read_bytes()` each fixture and runs `classify` — the frozen tool is not a canned printer, so
"prints correct JSON but reads nothing" cannot carry its sha (proven behaviorally by B5 below).

## 2. Sanity: the committed claims reproduce (before attacking)

- `python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision 4c8295fa…` →
  `… pins=1 … lesson_gate=1 … unresolved=0 met=true`, exit 0 — reproduces
  `controls/after-c1.txt`; same at `cc8add1f` → `met=true` exit 0.
- `python3 -B .ufo/waves/round-64/c64_quote_tool.py --root . --revision 4c8295fa…` →
  `present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true`, exit 0 —
  reproduces `controls/after-c2.txt`.
- Base `1a481315` → `lesson_gate=0 … unresolved=1 met=false`, exit 1 — reproduces
  `controls/base-c1.txt`.
- Selftests in my scratch: `c64_calibration.py --selftest --selftest-work
  /fast/scratch/hyaku/kake-r64/RevengerC63Defect/tmp/st1` → `selftest 26/26`;
  `c64_quote_tool.py --selftest --selftest-work …/tmp/st2` → `selftest 11/11` — reproduce
  `controls/selftest-c1.txt` / `selftest-c2.txt`.
- Stub differential rebuilt from frozen bytes in my own scratch (commit `d50f88a2c393445d…`;
  differs from the committed fixture `14fe2eab` only because commit timestamps differ — verdicts
  identical): `c63_quote_tool.py` → `present=1 selftest=4/4 frozen_cases=ok met=true` exit 0
  (**the routed round-63 defect reproduced**), `c64_quote_tool.py` on the same repo →
  `tool_sha=mismatch … met=false` exit 1.
- Rebuilt the frozen `build_fixtures.py` controls in scratch: marker/fabrication/junk → all
  `met=false` exit 1 with the exact component pattern of the committed receipts
  (`controls/control-marker.txt`, `control-fabrication.txt`, `control-junk.txt`).

## 3. Variant-by-variant attack results

25 fixture variants + 3 rebuilt controls ran green-to-red exactly as predicted; the decisive
counter output lines are quoted. "KILLED" = frozen counter prints `met=false` (or exit 2) on the
attack fixture; "SURVIVES" = prints `met=true` exit 0 on a fixture that does **not** honestly
carry the claim.

| # | c63-class variant | Verdict | Fixture + counter output (abridged) |
|---|---|---|---|
| 1 | Planted markers in all prose files, real blobs (fabrication-repo class) | **KILLED as committed — SURVIVES with copied spans** | A2 (markers without committed spans, rev `3274528601e8a757…`): `quote_correction=0 criterion=0 lesson_gate=0 … met=false`. A3 (same markers **plus the public committed-byte spans** pasted into the same files, rev `8b4c7e1959fbd527…`): `pins=1 recipe_rederive=1 class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 unresolved=0 met=true` exit 0 |
| 2 | Fake ledger with internally recomputed shas | **KILLED** | A12 (matchClass→raw-substring, located→6100-6105, self-consistent JSON, rev `13426df135b411f8…`): `pins=0 pin_drift=drift:ledger … met=false`. The row-level recomputation is irrelevant; the whole-ledger sha pin binds bytes |
| 3 | Real blobs, ledger matchClass swapped | **KILLED** | A11 (rev `d631b63b0009793d…`): `pin_drift=drift:ledger … met=false`; double-checked independently at `:238-239` when pins hold |
| 4 | Spot file without the disagreement (vacuous green) | **KILLED literally — SURVIVES when masked in prose** | A6 (row flipped to Agree, rev `a061be9e401992aa…`): `disagreements=0 … met=false`; A6b (no S432-Disagree line, rev `cf53e433f0defb2a…`): `disagreements=0 … met=false`; A10 (spot deleted): exit 2 `could-not-evaluate: round-61 verifier spot-check absent`. BUT A8 (spot **table says Agree**; one prose sentence "S432 was re-read; Disagree is not recorded…" added, rev `2b79bd888cfadd00…`): `disagreements=1 … met=true` |
| 5 | Lesson faking the outside verdict (span present, fabricated context) | **SURVIVES — worst finding** | A4 (same paragraph, `Disagree`→`` `Agree` ``, span kept, rev `2c5f16ddfe1dc3bb…`): `lesson_gate=1 unresolved=0 met=true` exit 0. A5 (whole Outside-verdict paragraph replaced with a fabricated "spot-check recorded Agree" narrative still quoting the span, rev `6d3a194469be2b1c…`): `met=true` exit 0. The spot file was untouched and still says `Disagree` (line 33) — the counter never compares them |
| 6 | Recipe swapped for an equivalent-output implementation | **KILLED** | A14 (comment-only append, byte-different, output-identical, rev `378576f0403e82c5…`): `pin_drift=drift:recipe … met=false`. Output equivalence is irrelevant; the sha pin binds recipe bytes |
| 7 | Canned-JSON stub tool | **KILLED** | B1 (frozen `stub_tool.py` bytes, rev `d50f88a2c393445d…`): `present=1 tool_sha=mismatch selftest=skipped … met=false`; B2 (stub + trailing comment, rev `d058f368c65285e3…`): same |
| 8 | Tool printing correct JSON but reading nothing | **KILLED** | B4 (`print(json.dumps(...))` hard-coding the frozen answers, rev `d1df04791a723142…`): `tool_sha=mismatch … met=false` — a non-reading tool necessarily has different bytes, and the sha pin fires before execution. B5 additionally proves the frozen tool itself reads bytes: with `S432.txt` mutated (unique phrase `require checking of a response` → `…of the response`, rev `20c12304c4eb8a4d…`) the **frozen** tool flips to `selftest=failed met=false` — its verdicts track fixture bytes |

Additional probes (all behaved as the code predicts, no crashes anywhere):

- A9 (two S432-Disagree rows, lesson green, rev `cfd99de1e496a105…`): `disagreements=2
  unresolved=1 met=false` — the unresolved arithmetic does gate surplus disagreements.
- A15 (adversarial bytes `\xff\xfe\x00…`, invalid `\xc3\x28` in lesson/knowledge/QUALITY, rev
  `5b9022e5378bf88a…`): `met=false`, **no traceback**.
- A16 (verdict span removed from lesson, rev `6c2f2e38130757bf…`): `lesson_gate=0 … met=false`.
- B7 (counter copy re-pinned to a garbage tool; rev `cfc9a72a56b56202…`): `selftest=unparseable:
  JSONDecodeError … met=false`, no traceback — the JSON guards hold.
- `git show <rev>:<path>` textconv probe: with `diff.shout.textconv` configured, `git show` still
  returned raw blob bytes (`hello world`, not `HELLO WORLD`) — the counters' `git show` reads are
  not spoofable by fixture `.gitattributes`.

**Counter-edit channel (both counters):** neither instrument protects its own constants. Scratch
copies of the frozen counters with one pin constant re-pointed:

- A13 — `LEDGER_SHA` re-pinned to a ledger whose **unchecked fields** (`note`) were fabricated
  (rev `87dc7356bc3a5d45…`): `met=true` exit 0. The ledger row's `note`, `quote`, `textPath`,
  `rawPath`, `schema`, `predicate` are never verified by the counter when pins hold; only
  `matchClass` and `locatedRawLines` are read (`:238-241`).
- A14b — `RECIPE_SHA` re-pinned to the equivalent-output recipe (rev `378576f0…`): `met=true`.
- B6 — `FROZEN_TOOL_SHA` re-pinned to the canned stub's sha (rev `d50f88a2…`): `present=1
  tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true` — the stub sails through.

This channel is **outside the frozen instrument** and is exactly what the contract's freeze
covers: contract lines 8–17 pin all four instruments, line 5 makes post-score changes void, and
I verified the on-disk/T0 shas match. So it is not a kill-rule breach of the committed round —
but it means every pin in C1/C2 is only as strong as the frozen-sha discipline, not self-enforcing.

## 4. Full harness transcript (verbatim)

```
== C1 calibration counter (frozen c64_calibration.py) ==
[AS-EXPECTED] c1/A0-real-tree exit=0 (expect 0) traceback=False :: revision=5d6bdb304c491886ccad91f87e990465d9ee1875 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
[AS-EXPECTED] c1/A1-base-lane exit=1 :: revision=1a48131577ba82c967650561be34e8dba909432a disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
[AS-EXPECTED] c1/A2-marker-prose-real-blobs exit=1 (expect 1) traceback=False :: revision=3274528601e8a7579f909533261818525fa4de5d disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
[AS-EXPECTED] c1/A3-marker-prose-plus-spans exit=0 (expect 0) traceback=False :: revision=8b4c7e1959fbd5277ec56870d99b8a88c69728f9 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
[AS-EXPECTED] c1/A4-lesson-flips-outside-verdict exit=0 (expect 0) traceback=False :: revision=2c5f16ddfe1dc3bbe01b3578f4e498dc8783882c disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
[AS-EXPECTED] c1/A5-lesson-fabricated-outside-verdict exit=0 (expect 0) traceback=False :: revision=6d3a194469be2b1c3c275afdbafafb01b11e77cd disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
[AS-EXPECTED] c1/A6-spot-agree-no-disagreement exit=1 (expect 1) traceback=False :: revision=a061be9e401992aa42e20e33b9e723128e96cc46 disagreements=0 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
[AS-EXPECTED] c1/A6b-spot-no-S432-disagree-line exit=1 (expect 1) traceback=False :: revision=cf53e433f0defb2a22c0a3bdfd4b0f46c1a19c96 disagreements=0 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
[AS-EXPECTED] c1/A7-spot-disagree-reason-unbound exit=0 (expect 0) traceback=False :: revision=deb8e46b916c4b01e205d58d75c65a8f3a156335 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
[AS-EXPECTED] c1/A8-disagree-only-in-prose exit=0 (expect 0) traceback=False :: revision=2b79bd888cfadd001741f33e38d75577d5402088 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
[AS-EXPECTED] c1/A9-two-disagreements exit=1 (expect 1) traceback=False :: revision=cfd99de1e496a105b9214b59c65ba7f7f1c545b5 disagreements=2 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
[AS-EXPECTED] c1/A10-spot-absent exit=2 (expect 2) traceback=False ::  :: stderr=could-not-evaluate: round-61 verifier spot-check absent
[AS-EXPECTED] c1/A11-ledger-matchclass-swapped exit=1 (expect 1) traceback=False :: revision=d631b63b0009793d66b49accb3c66df07c6856d4 disagreements=1 pins=0 pin_drift=drift:ledger recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
[AS-EXPECTED] c1/A12-fake-ledger-recomputed-sha exit=1 (expect 1) traceback=False :: revision=13426df135b411f89dc3422d47f6e6a767171297 disagreements=1 pins=0 pin_drift=drift:ledger recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
[AS-EXPECTED] c1/A13-counter-edit-repinned-ledger-note exit=0 (expect 0) traceback=False :: revision=87dc7356bc3a5d45d3ab524dc6ae203856652359 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
[AS-EXPECTED] c1/A14-recipe-equivalent-output exit=1 (expect 1) traceback=False :: revision=378576f0403e82c5e6697eb42251e97363282aa8 disagreements=1 pins=0 pin_drift=drift:recipe recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
[AS-EXPECTED] c1/A14b-counter-edit-repinned-recipe exit=0 (expect 0) traceback=False :: revision=378576f0403e82c5e6697eb42251e97363282aa8 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
[AS-EXPECTED] c1/A15-adversarial-bytes-prose exit=1 (expect 1) traceback=False :: revision=5b9022e5378bf88a0af66d744d7adc6d6cc9a951 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
[AS-EXPECTED] c1/A16-lesson-span-removed exit=1 (expect 1) traceback=False :: revision=6c2f2e38130757bf456fc225a86a42766c9f3676 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
== C1 control fixtures built by the frozen fixture builder ==
build_fixtures exit=0 stderr=
[AS-EXPECTED] control/marker-repo rev=962dc29917 exit=1 :: revision=962dc29917a9a5e1a7c081fd33acdf2d5dd2bb56 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
[AS-EXPECTED] control/fabrication-repo rev=91cc72e5dc exit=1 :: revision=91cc72e5dc9248f1617abcda6c4988e3463b9f5f disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
[AS-EXPECTED] control/junk-repo rev=28a769dfa3 exit=1 :: revision=28a769dfa3af1f00e8cad2586af62334909705b0 disagreements=1 pins=0 pin_drift=drift:raw,text,ledger,recipe recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
== C2 operability counter (frozen c64_quote_tool.py) ==
[AS-EXPECTED] c2/B0-frozen-tool-real-fixtures exit=0 (expect 0) traceback=False :: revision=445f31573779d0861d52fcdc6b2e666c1860a12a present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true
[AS-EXPECTED] c2/B1-canned-stub exit=1 (expect 1) traceback=False :: revision=d50f88a2c393445dec5fae67ad7942bd05b8b8ef present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
[AS-EXPECTED] c2/B2-stub-plus-comment exit=1 (expect 1) traceback=False :: revision=d058f368c65285e36b615e4e5ceab78d816c8e4a present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
[AS-EXPECTED] c2/B3-lying-reads-but-wrong exit=1 (expect 1) traceback=False :: revision=1ad09024e371038be9bafaef658c4411fc61df1b present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
[AS-EXPECTED] c2/B4-reads-nothing-correct-json exit=1 (expect 1) traceback=False :: revision=d1df04791a7231422cfbcc96e3b3e434e7aabbb4 present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
[AS-EXPECTED] c2/B5-frozen-tool-mutated-fixture exit=1 (expect 1) traceback=False :: revision=20c12304c4eb8a4d696ae601030c03bad7bd3e41 present=1 tool_sha=ok selftest=failed frozen_cases=missing rederive=unevaluable met=false
[AS-EXPECTED] c2/B6-counter-edit-repinned-to-stub exit=0 (expect 0) traceback=False :: revision=d50f88a2c393445dec5fae67ad7942bd05b8b8ef present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true
[AS-EXPECTED] c2/B7-counter-edit-garbage-tool exit=1 (expect 1) traceback=False :: revision=cfc9a72a56b5620e284229e71a88f8d6f10d4afe present=1 tool_sha=ok selftest=unparseable:JSONDecodeError frozen_cases=missing rederive=unevaluable met=false
== C2 stub differential: round-63 counter on the same stub ==
[AS-EXPECTED] c63/stub exit=0 :: revision=d50f88a2c393445dec5fae67ad7942bd05b8b8ef present=1 selftest=4/4 frozen_cases=ok met=true traceback=False
c64/stub(same repo) exit=1 :: revision=d50f88a2c393445dec5fae67ad7942bd05b8b8ef present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
== summary ==
variants=26 unexpected=0
```

Provenance: the block above is the verbatim `results.txt` of the final harness run, copied out
before the scratch tree was deleted. `variants=26` counts the 26 `case()` fixtures (A0, A2–A16,
B0–B7); A1, the three rebuilt controls and the stub-differential pair are printed outside that
counter. Fixture commit ids differ between harness runs (git commit timestamps), which is why
earlier partial runs cited different ids; verdict tokens and exit codes were identical across
every run of each variant.

## 5. Root causes behind the survivors

1. **The outside-verdict binding is one-directional substring presence.** `lesson_gate`
   (`c64_calibration.py:252-259`) requires `SPOT_VERDICT_SPAN` to appear inside the lesson's
   `## Gate` block, but never checks that the spot file contains that span, never compares the
   lesson's claimed verdict against the spot row, and never pins `SPOT_REL`
   (`:90-95`). Any lesson that pastes the public span while asserting any verdict greens
   (A4/A5); any spot file whose verdict row was edited — even to the opposite decision — stays
   green as long as some line carries `S432`+`Disagree` (A7/A8). This is the round-63
   fabrication class surviving at the prose layer with **all shas pinned and all re-derivations
   passing** (`pins=1 recipe_rederive=1 class_match=1 located=6150-6154`).
2. **`unresolved` is arithmetic, not evidence** (`:267`): `lesson_gate`'s substring green cancels
   one disagreement regardless of whether the disagreement was genuinely resolved.
3. **All three prose gates are substring predicates over public committed bytes** (`:247-259`).
   The fabrication control (variant 1) is red only because its planted markers lack those spans;
   a fabricator who copies the committed span text (public in `corpus/lessons/round-64.md`,
   `corpus/QUALITY.md`, `corpus/knowledge/response-header-expectations.md` at T0) greens (A3).
4. **C2's guarantee is exactly one bit: the tool blob's sha.** Everything else (frozen cases,
   rederivation, guards) only matters for the frozen bytes. That bit is honest (B1–B5), but the
   counter itself can be re-pinned to any bytes (B6), and C2 never pins its six fixture blobs —
   a tree whose `S432.txt` drifts consistently greens B0-shaped (tool and counter agree on the
   drifted bytes); only C1's text pin catches that drift, which is fine under the contract's
   separability but means C2 alone is drift-blind.

## 6. Verdict

- **Killed by c64 (verified with fixtures, not just the committed ones):** variant 2 (fake
  ledger, recomputed shas — A12), variant 3 (swapped matchClass — A11), variant 6
  (equivalent-output recipe — A14), variant 7 (canned-JSON stub — B1/B2 + rebuilt committed
  fixture), variant 8 (correct-JSON reads-nothing tool — B4; frozen tool proven byte-reading —
  B5), variant 4 in its literal form (no disagreement anywhere — A6/A6b/A10), variant 1 in its
  committed marker form (A2 + rebuilt marker/fabrication/junk controls). Surplus-disagreement
  gating (A9), adversarial-byte robustness (A15, B7, t3/t6) and the round-63 stub defect
  differential (c63 green vs c64 `tool_sha=mismatch` on the same stub bytes) all hold.
- **Survivors (each demonstrated on a fixture that prints `met=true` exit 0):**
  - **Variant 5 — lesson faking the outside verdict — fully survives** (A4, A5). Sharpest
    companion: **A7**, the spot file's actual verdict *reason* can be replaced while the lesson
    still quotes the real span, and the counter cannot tell.
  - **Variant 1 survives in its span-copying form** (A3): real blobs + prose containing the
    public committed-byte spans greens.
  - **Variant 4 survives in its prose-masking form** (A8): the spot table may say `Agree` while
    one prose line containing `S432`+`Disagree` supplies the tally.
  - Outside-the-instrument channel for all of the above: counter-edit re-pins (A13, A14b, B6) —
    defended only by the contract's frozen-sha list and the post-score voiding rule, both of
    which check out at T0/`cc8add1f`.
- **Confidence:** high for every killed variant (direct fixture execution of the frozen
  counters, outputs above). High that the survivors green the counter; labeled **inference**
  when judging intent: the prose-gate substring design is what makes the "block-level binding"
  claim weaker than its wording — the counter binds *presence* of committed spans in the lesson,
  not *provenance* of the outside verdict.
- Smallest fixes that would close the survivors (for the round's consideration, not landed):
  pin `SPOT_REL` by sha and require `SPOT_VERDICT_SPAN` to be present in the spot blob with the
  claimed verdict token on the same row; or hash-pin the three prose blocks; or make
  `unresolved` derive from the spot file's own disagree rows minus rows the spot file itself
  marks resolved. Counter-edit exposure is structural — only the freeze discipline covers it.

## 7. Boundaries honored

- No mutating git/jj command anywhere; no commit or push; lane read-only
  (`git show/rev-parse/log/diff/status/merge-base` only). Fixture toplevels asserted before
  first commit. The only lane write is this report file.
- Lane worktree observation (not mine, recorded for the orchestrator): between 08:12 and 08:24
  the worktree gained append-only modifications `M SKILL.md (+13)`, `M corpus/QUALITY.md (+25)`,
  `M corpus/lessons/round-64.md (+58)`, mtimes 08:21, zero deletions. My runs are unaffected:
  every counter invocation reads revision-pinned blobs via `git show <rev>:<path>`, and I
  re-verified the two lane-level green runs (`4c8295fa`, `cc8add1f`) — both receipt-identical.
- Scratch `/fast/scratch/hyaku/kake-r64/RevengerC63Defect/` (fixtures, harness, variants,
  results) deleted after copying all decisive evidence into this report. `/tmp` used only for
  counter-internal `mkdtemp` noise (<50 MB).
