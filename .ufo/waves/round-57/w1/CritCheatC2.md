# CritCheatC2

Hypothesis: a junk resolver that recognises the gate's fixture and the red revision passes C2 5/5. **Confirmed**, then closed.

Scratch clones (all `mktemp -d`, `git rev-parse --show-toplevel` = the clone, commits only there with
`-c user.name=selftest -c user.email=selftest@local`):
- `$D=/tmp/c2cheat-TUK6z3` — clone of the lane at `b9a5d012f7fd`, junk commits `bcbbaeb` (13-line) and `4b8f8956` (10-line).
- `$G=/tmp/c2genuine-eVapXv` — clone at `b9a5d012f7fd` + a reference resolver I wrote for this probe, commit `7ed2ebe7`.
- `$H=/tmp/c2cand-zepN7a` — clone at `f7c98ff` + the lane's own candidate `ExecResolverBuild.files/id_resolver.py`
  (sha256 `2bee5a8fa08efb432d946465f361db169e6572a9cfe5697f6de3ffd6f3bdfba5`), commit `8f7ecc95`.
- `$A=/tmp/c2alt-*` — clone at `f7c98ff` + `ExecResolverAlt.files/alt_resolver.py`, commit `74c97dc2`.

Gate under test: the lane working-tree `c57_idresolver_gate.py` (= the `f7c98ff` version, the one carrying `--fleet`).

## JUNK TOOL:

`scripts/id_resolver.py` at `4b8f8956` in `$D` — 10 non-blank lines, 971 bytes, no parsing of anything:

```python
import sys, os
a = sys.argv[1:]
if "--selftest" in a: print("selftest: 16/16"); sys.exit(0)
r = a[a.index("--revision")+1] if "--revision" in a else ""
if r.startswith("3994101"):
    print("\n".join(f"DANGLING {i} cited-by=k.md owners=kotodama-shokunin url-match=-" for i in "S367 S372 S373 S390 S409".split())); print("ids_cited=120 ids_resolved=115 dangling=5 owned_elsewhere=5 unowned=0"); sys.exit(1)
root = a[a.index("--root")+1] if "--root" in a else "."
if root.endswith("demo-shokunin") and os.path.exists(root+"/corpus/knowledge/sub/bad.md"):
    print("\n".join(f"DANGLING {i} cited-by=corpus/knowledge/sub/bad.md owners={o} url-match={u}" for i,o,u in [("S101","alpha-shokunin","alpha-shokunin"),("S200","alpha-shokunin,beta-shokunin","-"),("S0300","alpha-shokunin","-"),("S777","-","-")])); print("ids_cited=6 ids_resolved=2 dangling=4 owned_elsewhere=3 unowned=1"); sys.exit(1)
print("ids_cited=999 ids_resolved=999 dangling=0 owned_elsewhere=0 unowned=0")
```

Four constants and one shape test: `--selftest` → `16/16`; revision prefix `3994101` → the five red lines; a root whose
basename is `demo-shokunin` with `corpus/knowledge/sub/bad.md` → the fixture lines; everything else → a green summary.
It never opens `corpus/SOURCES.md`, never reads a knowledge file, never looks at a sibling.

## GATE RESULT:

`python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root $D --revision 4b8f8956… --fleet /home/vgpnk/Projects/shokunin`

```
C2 id-resolver 5/5 met=True  (met: gate_conditions_passed == 5 of 5)      exit 0, 1.3 s
  G1_tool_present PASS   G2_selftest PASS  (selftest: 16/16 — a printed constant)
  G3_fixture      PASS   exit=1 dangling=[S0300,S101,S200,S777] summary=(6,2,4,3,1); clean exit=0 summary=(999,999,0,0,0)
  G4_red_before   PASS   exit=1 dangling=[S367,S372,S373,S390,S409] owners=all kotodama-shokunin
  G5_green        PASS   exit=0 summary=(999,999,0,0,0)
```

All five pass. The frozen predicate `met: gate_conditions_passed == 5 of 5` is satisfied by a 10-line constant printer.
Mechanisms: G2 hashes nothing, so the selftest line is free text; G3's fixture is built with fixed lane/sibling names and
fixed ids (`EXPECT_FIXTURE`, `EXPECT_SUMMARY` are module constants) and the clean half only asserts exit 0 + `dangling==0`;
G4 is keyed on a revision constant (`RED_REV`) whose expected rows are also constants; G5's green expectation is the constant
`dangling==0, ids_cited>=100`, and `ids_cited=999` satisfies it.

## MINIMUM JUNK:

**10 non-blank lines / 971 bytes / 11 statements** (the 13-line variant at `bcbbaeb` was the first cut; collapsing each
`for`+`print` pair into one `"\n".join(...)` print is the whole saving). Below that it stops working: the four branches
(`--selftest`, red revision, bad fixture, fall-through green) and the two discriminators (revision prefix, `demo-shokunin`
+ `bad.md`) are each load-bearing — dropping the `bad.md` test breaks G3's clean half (the clean fixture would print the
four dangling lines and exit 1); dropping the `demo-shokunin` test breaks G4/G5 on the real lane. No parsing is needed at
any length.

## PROPOSED GATE PATCH:

`.ufo/waves/round-57/w1/CritCheatC2.files/gate.patch` (10975 bytes, sha256
`c5322eb627a302ecba09e26b24584b9f78920e5b89a01be3b457aff6a20761d5`), unified diff against
`.ufo/waves/round-57/c57_idresolver_gate.py`, **not applied to the lane**. Base is the lane working-tree copy at `f7c98ff`
(the `b9a5d012` copy lacks the `--fleet` option, so a diff taken against it does not apply to the graded file).
Verified: `patch -p1 --dry-run` then `patch -p1` in `$D` → byte-identical to the prototype (`cmp`), 176 diff lines (+90/−29).

Two changes, folded into the existing conditions because the frozen predicate fixes the count at five (a sixth condition
would change `gate_conditions_passed == 5 of 5`):

1. **G3 — per-run fixture.** `build_fixture()` draws an 8-char token for the lane name and both sibling names and draws every
   id (`S`+3 digits, one 4-digit) from `random.SystemRandom()`; the expected rows and summary are computed from the drawn
   values instead of being module constants. The rules the fixture tests are untouched: 0- and 2-space registry rows, a
   resolved id, a 4-digit id, a one-sibling id with its URL quoted, a two-sibling id, an unowned id, the `S12`/`AS500`/
   `S500x`/`s101` decoys, `url-match`.
2. **G5 — planted dangling id.** After the green run passes, the gate clones the measured revision again, appends
   `Planted dangling citation <id>.` to the largest `corpus/knowledge/**/*.md` file, commits it in the throwaway clone with
   an explicit selftest identity and `-c commit.gpgsign=false`, then runs the tool at that new revision: it must exit 1 and
   report **exactly** that one id dangling. The id is drawn at 4 digits (5-digit fallback) and checked against the lane
   registry at the revision, so it is genuinely unregistered; the commit message carries no id.

Measured effect (artifact-applied gate, `$D/.ufo/waves/round-57/c57_idresolver_gate.py`):

| tool | frozen gate | patched gate |
|---|---|---|
| junk (10 lines) | 5/5, exit 0 | **3/5, exit 1** — G3 FAIL (`expected=[S4662,S479,S697,S783]`, tool printed `999` green), G5 FAIL (planted `S4940` not reported) |
| candidate `ExecResolverBuild` | 5/5, exit 0 | 5/5, exit 0 (G3 ids drawn fresh; planted `S8773` reported, `(105,104,1,0,1)`) |
| reference resolver (mine) | 5/5, exit 0 | 5/5, exit 0 (planted `S6040`, `(105,104,1,0,1)`) |
| `ExecResolverAlt` | 4/5, exit 1 (G2: no `--selftest`, exit 64) | 4/5, exit 1 — identical verdict, patch changes nothing |

The other two candidate defences, judged from the gate source:
- **randomised fixture alone is insufficient.** G4's `RED_IDS`/`RED_REV` and G5's `dangling==0, ids_cited>=100` stay
  constants, so a tool that genuinely parses only the *synthetic* fixture and hardcodes red/green would still reach 5/5
  without ever touching the real lane. G5's planted run is what forces the real-lane read.
- **hashing the selftest output** pins the tool's exact message text. The tool is authored in this round *after* the counter
  froze, so the digest cannot be frozen without a post-hoc edit to the counter (violates "frozen before any seat scored"),
  and it rejects a genuine tool that adds a check (`33/33` vs `16/16`) or rewords a line. Not taken.

Residual under the patch: the planted commit's *diff* names the planted id, so a tool that reads `git show` of the last
commit rather than resolving could pass the planted half. G3's randomisation still forces citation+registry+sibling+url
resolution on the synthetic side, so such a tool would need both mechanisms. Cheapest further hardening (not applied):
plant in a non-git copy — no diff oracle — but that exercises only the working-tree path G3 already covers and drops the
"reads a revision, not the tree" property.

## GENUINE-TOOL RISK:

Measured, not argued: the lane's own candidate (722 lines, `selftest: 33/33`) and an independently written reference both
pass the patched gate 5/5, and the alt resolver keeps its unchanged 4/5 verdict. Risks assessed:
- **No new parsing rule.** Randomisation varies names and ids only; every format feature the fixture already tested is
  still tested. A correct tool reads the files, so the drawn values are invisible to it. Only a tool that hardcodes the
  fixture names/ids fails — that is the defect being closed.
- **Planted id shape.** 4 digits (fallback 5) inside the contract's `S` + 3-or-more-digits rule, which G3 already exercises
  with a 4-digit id; it is verified against the lane registry at the revision, so it is genuinely dangling and no sibling
  collision can turn the check into a false failure (owners are not asserted).
- **Planted commit hygiene.** Throwaway clone, explicit selftest identity, `commit.gpgsign=false` (a global signing config
  cannot fail it), commit message without an id. Failure to plant raises `RuntimeError` → exit 2 (unevaluable), never a
  silent PASS or a spurious FAIL.
- **Behavioural demand.** The only new demand is "a revision whose knowledge cites an unregistered id → exit 1 and name it",
  which is the CLI contract already in the gate docstring. A tool that treats `dangling>0` as an error contradicts the
  contract and would already fail G4.
- **Cost.** One extra clone+commit+run: +~1.2 s (candidate 2.1 s → 3.3 s).
- **Frozen surfaces untouched.** G1/G2/G4 logic, condition names, the predicate string, exit codes 0/1/2/64.

Secondary observations (not part of the hypothesis, no action taken): G2 is satisfiable by a printed constant — it is a
presence check, not a behaviour check; and G4's owner test is `RED_OWNER in v[1].split(",")`, so extra owners pass — observed
as `kake-shokunin,kotodama-shokunin` in every scratch-clone run, because `--root` was a clone (not `*-shokunin`) and the real
lane therefore counted as a sibling. In the graded run `--root` is the lane, so the realpath exclusion applies.

No tool installs, no pacman, no lane writes beyond this report and `.ufo/waves/round-57/w1/CritCheatC2.files/gate.patch`.

VERDICT: C2's gate is hardcode-passable — a 10-line constant printer scores 5/5 — and a two-part patch (per-run fixture + one planted dangling id in a copy of the measured revision) drops it to 3/5 while the lane's real candidate, an independent reference and the alt resolver keep their verdicts.
