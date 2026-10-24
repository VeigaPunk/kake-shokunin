CONFORMANT

Axes: freshness — C2 claim sizing and honesty; operability not assessed. No round verdict.
Scope: frozen b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee; base 61046fcffa23898cd93b7a5a0af4906dac9926c9.

- Before committed receipt — holds. Freeze tree contains `verification/freeze/sweep-before.txt` (blob 601d65ff527bfd79e59629202a379572bbdb22b3) and `sweep-before.exit` (de8cbc88ee26756c3140cb3e4411a279decb19b2), both under `.ufo/waves/round-43/`. The latter records `sweep-before exit=1` at line 1.
- Exact before verdict — holds. `.ufo/waves/round-43/verification/freeze/sweep-before.txt:79`: `VERDICT: DRIFT — §paths: 2 unannotated miss · 2 NOT in pins.pathsMissSet (exit 1)`. Lines 8–9 identify the two original citations, round-29.md:102 and round-33.md:43.
- After committed receipt — holds. Same freeze tree contains `.ufo/waves/round-43/verification/freeze/sweep-after.txt` (6403da08cfe10154b8367f6377e594e5cdde8192); line 78 is exactly `VERDICT: OK (exit 0)`. Lines 6 and 75 record drift 0 and no new miss. Both receipts first appear in the freeze commit, dated 2026-10-23T16:44:33-03:00.
- One counting command — holds. `SCORECARD.md:3260` declares exactly `node scripts/freshness-sweep.mjs --section=paths`, counting exit code plus verdict line; not a multi-command recipe.
- Do-nothing exclusion — holds by source/receipt comparison, not an independently executed counterfactual. With the frozen missing targets unchanged, omitting both annotation rows and both pin additions leaves drift=2 and newMissing=2. Exact gate: `scripts/freshness-sweep.mjs:565`, `ok: drift.length === 0 && newMissing.length === 0,`. Line 1051 assigns exit 1 and the same §paths reason; lines 1119–1120 print the verdict and assign the process exit code. Thus the exact before verdict above stays red.
- Strongest cheap counterexample considered: pin-only would leave the two unannotated citations red (lines 494–497); annotation-only would leave the two unpinned misses red (lines 506,515–521). These are static deductions, not executed mutant scores. The gate source is byte-unchanged from base to freeze. The actual diff adds annotation rows at `corpus/lessons/round-29.md:104` / `round-33.md:45` (within +2 of each original citation) and pin entries at `corpus/knowledge/freshness-pins.json:77–78`.
- Claim scope — holds, not overstated. `SCORECARD.md:3248–3262` explicitly says “§paths gate” and `--section=paths`; `corpus/lessons/round-43.md:37–51` preserves that context. Section selection at `scripts/freshness-sweep.mjs:1084` and dispatch at 1022–1035 do not execute history or armed checks for this command. No whole-sweep-green claim is supported or asserted here.
- Gate limits: `sweep-after.txt:72,74` still reports 10 unresolved patterns and 1,720 relative-form citations outside resolution checks. The gate recognizes absence vocabulary plus miss-set membership; its exit alone does not establish removal-event truth or lane-copy byte identity. Those descriptive claims were not independently audited in this seat.
Smallest safe correction: none for this scoped claim; retain the section qualifier and do not promote it to whole-sweep or provenance verification.

Commands exercised (cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`; every command below exited 0):
```sh
timeout 30 prlimit --as=8000000000 -- git ls-tree b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee -- .ufo/waves/round-43/verification/freeze/sweep-before.txt .ufo/waves/round-43/verification/freeze/sweep-before.exit .ufo/waves/round-43/verification/freeze/sweep-after.txt .ufo/waves/round-43/verification/freeze/exits.txt scripts/freshness-sweep.mjs SCORECARD.md corpus/lessons/round-43.md corpus/knowledge/freshness-pins.json
timeout 30 prlimit --as=8000000000 -- git log --format='%H %cI %s' b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee -- .ufo/waves/round-43/verification/freeze/sweep-before.txt .ufo/waves/round-43/verification/freeze/sweep-before.exit .ufo/waves/round-43/verification/freeze/sweep-after.txt
timeout 30 prlimit --as=8000000000 -- git diff 61046fcffa23898cd93b7a5a0af4906dac9926c9 b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee -- scripts/freshness-sweep.mjs corpus/lessons/round-29.md corpus/lessons/round-33.md corpus/knowledge/freshness-pins.json
timeout 30 prlimit --as=8000000000 -- git diff --exit-code b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee -- scripts/freshness-sweep.mjs SCORECARD.md corpus/lessons/round-29.md corpus/lessons/round-33.md corpus/lessons/round-43.md corpus/knowledge/freshness-pins.json .ufo/waves/round-43/verification/freeze/sweep-before.txt .ufo/waves/round-43/verification/freeze/sweep-before.exit .ufo/waves/round-43/verification/freeze/sweep-after.txt
timeout 30 prlimit --as=8000000000 -- git diff --exit-code 61046fcffa23898cd93b7a5a0af4906dac9926c9 b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee -- scripts/freshness-sweep.mjs
timeout 30 prlimit --as=8000000000 -- sha256sum scripts/freshness-sweep.mjs .ufo/waves/round-43/verification/freeze/sweep-before.txt .ufo/waves/round-43/verification/freeze/sweep-before.exit .ufo/waves/round-43/verification/freeze/sweep-after.txt SCORECARD.md corpus/lessons/round-43.md corpus/knowledge/freshness-pins.json
```
Tool/evidence SHA-256 (inspected files match the freeze tree):
- `scripts/freshness-sweep.mjs`: a1aa79d114093cc5b663e811e86a20a57bf37357dd8a3598c9e02084770d8d8b
- `.ufo/waves/round-43/verification/freeze/sweep-before.txt`: 03dc57173bb9dfb76b3b690a5cf9051a5df27bd00e4c46793116fca8ffab9541
- `.ufo/waves/round-43/verification/freeze/sweep-before.exit`: 6da74813be820309007dd6e6e66e57550006216ec7c236e821024d3c62d9d38d
- `.ufo/waves/round-43/verification/freeze/sweep-after.txt`: 1c642de60432972eeef326d7863aea7122d508f0717e77fcd2f645480d21e1d2
Verification limits: receipt/source review only; no sweep replay, full sweep, or runtime counterfactual executed. No unrun runtime check is reported passed. No tools installed or upgraded, no network requests, no background processes started.
