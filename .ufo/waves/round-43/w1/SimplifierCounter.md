DEFECT: 2 v4 blocks named by no weakening experiment (F pairfile unit c43_count_v4.py:478; T2 long-port variants :620), and the repeated-host class has no discriminating control — coverage gaps, not counter unsoundness.

# Method
MutCounter*.md absent at run time (w1/ held only swarm-registry.json) -> fallback, 2 named weakenings run myself, reusing frozen controls from .ufo/waves/round-43/controls-r42/ (sha256s match its SHA256SUMS; counter sha 1c3b96610873301b... = frozen). Frozen baseline (verification/freeze/): M8 not met killed via F+T3; v4_hosttable not met via F+T3; v1_casefold via F+T2; v2_prefix32 via E+F+T2+T3; junk 0/11.

# Commands (receipts in /fast/scratch/hyaku/kake-r43/SimplifierCounter/, no --seed)
1. `timeout 900 prlimit --as=8000000000 -- python3 -B w-port.py --root <lane> --tool-file M8-port-five-digits.py --label SimpCounter-wport-M8 --out wport-m8.json` -> counter exit 0, met=True, 11/11, ratios all <=1.24, seed 63124960035509. (w-port.py sha256 171ca0d6e11b5ac4...; union weakening: removed F port values :465-467, T1 2% branch :761, T3 branch :793, T5 k in {45,46,47} :811.)
2. `... python3 -B w-host.py --root <lane> --tool-file v4_hosttable.py --label SimpCounter-whost-hosttable --out whost-hosttable.json` -> counter exit 1, met=False, 10/11, unequal run T3 (candRepsEqual 0/5), seed 171166807417973. (w-host.py sha256 3d41d01e2c35c5b2...; removed F repeated-host blocks :479-483 + F common-host values :484-489 + T3 block machinery :784-789, KEPT T3 common-host branch :790.)

# Per-block: covering experiment / load-bearing
- A :cases_a (r41 case shapes) | none in MutCounter* (r43 experiments scope r43 classes by design) | provenance, adjudicated r41/r42.
- B :cases_b IP literals | same | provenance.
- C :cases_c long values | same | provenance.
- D :cases_d whole-value edits | same | provenance.
- E :cases_e units x 11 slots | none named, but frozen receipt: v2_prefix32 killed via E | load-bearing YES (live discriminator).
- F ports :465-467 | MutCounterPort; my weakening-1 | YES (M8 fails v4, meets removal).
- F fold pairs :470 | MutCounterFold (report absent) | YES by baseline (v1_casefold killed via F; attribution vs pairfile ambiguous).
- F prefix pairs :473 | MutCounterPrefix (absent) | YES by baseline (v2_prefix32 killed via F; same ambiguity).
- F pairfiles :478, layout_f :557 | NO experiment names this unit | UNPROVEN — FLAG 1.
- F repeated-host blocks :479-483 | MutCounterHost ("remove F/T3 repeated-host blocks") | NO discriminating control found: removal did not lift hosttable's fail (it fails via T3 anyway) -> dead-weight candidate, FLAG 2.
- F common-host values :484-489 | MutCounterHost | not necessary for hosttable (see run 2); no other control attributed | UNPROVEN.
- T1 :756 whole shape | r42 provenance | provenance.
- T1 port variants :761 | MutCounterPort | redundant for M8 at frozen seed (T1 was equal there) | UNPROVEN for other tools.
- T2 restructure :603-627 (fold pair, segment_smu :493, write_scoped :629) | MutCounterFold + MutCounterT2 | YES by baseline (v1_casefold killed via T2).
- T2 long-port variants :620 | named in NO experiment (MutCounterPort lists "T1/T3/T5" only) | UNPROVEN — FLAG 3.
- T3 common-host branch :790 | MutCounterHost (implicit; spec names F only) | YES — my weakening-2 proves it ALONE discriminates hosttable.
- T3 repeated-host blocks :784-789 | MutCounterHost | same as F blocks — no demonstrated discriminator | FLAG 2.
- T3 long-port branch :793 | MutCounterPort | YES (M8 fails v4 via T3, meets removal).
- T3 prefix branch :795-798 | MutCounterPrefix | YES by baseline (v2_prefix32 killed via T3).
- T4 :826 real run | none (r39 adjudication, not a r43 class) | provenance.
- T5 long-port checks :811 | MutCounterPort | redundant for M8 at frozen seed (T5 equal there) | UNPROVEN.

# Missing-class check
All 15 named weakening members (make_w1_spec.py:91-100) map to existing v4 blocks; no weakening kills discrimination without a corresponding block. No missing class found.

# Statement check (SCORECARD round-43 / freeze receipts)
- "Counter v4 sha 1c3b9661..., build-1..3 met 11/11" — holds (sha re-verified byte-identical).
- "r42ctl-M8/v1/v2/v4 not met" — holds (receipts re-read: 9/11, 9/11, 9/11, 7/11; unequal-run attribution as cited).
- "junk 0/11" — not re-run; receipts only (exit=1 in exits.txt); holds as recorded.
- "Five MutCounter experiments cover the r43 classes" — OVERSTATED: pairfile unit and T2 port variants are not named by any of them.
- Tooling: no installs/updates performed (existing python3/bwrap/prlimit sufficient).

Tradeoff: only 2 of the 15 named members were runnable within the fallback cap; port was weakened as a union (per-run attribution for T1/T5 port variants open), host removal kept T3's common-host branch, which turned out to be the sole discriminator — a luckier cut than planned, it hardened rather than weakened the conclusion. Fold/Prefix/T2 verdicts rest on frozen baseline kills until MutCounterFold/Prefix/T2 land.
