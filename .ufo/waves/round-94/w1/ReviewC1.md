# ReviewC1 — C1 counter attack round 94, w1

VERDICT: C1 counter admits route R03 (dual `source:` lines), and R02b (indented
Mistakes table) + R10b (absence span with mismatched closing bracket) are
`met=true` false-greens on any lane that carries those shapes; plus one
effective-scope cost finding that makes the strict surface effectively a
synthetic-only bar (R08 identity-displacement via LAE-LA-1 route; R18
`--surfaces-file` route escape). The frozen predecessor-admission logic runs
frac-admitted against a per-`met`-cell synthetic mismatch-population and is
therefore unscored in this round's `met` receipt (`predecessor_admits=frac/8`);
the genuine floor of 2 is maintained against the frozen totals in the
predecessor's own ROUTE-population (13/13), not in the run of the frozen
round-94 counter.

## Controlled reproductions (all scratch dirs under /fast/scratch/hyaku/kake-r94/ReviewC1/)

Fixed input ground truth — counter:
`c94_selfassess.py` digest = `58028584f1a…36a` (sha256sum, matches
`controls/instrument-sha256.txt`, ON LANE at revision `ba667b24` and not in the
earlier `0f7d9bbc…` round-base tree).

### Base control (replicates `controls/base-c1.txt`, exit 1, host-live)

```
cd /fast/scratch/hyaku/kake-r94/ReviewC1
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-94/c94_selfassess.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 0f7d9bbcdd6a9ed36f5bc62b2116ddd040e871a8 --work $PWD/basewrk > baseline.out
```
rc=1; line 1 `... mismatches=15 E1=0 E2=0 E3=0 E4=0 E5=15 pins=ok battery=8/8
predecessor_admits=7/7 floor=2 self_pin=ok met=false` — matches the frozen
control. Receipt: `/…/w1/ReviewC1/baseline.out`.

### --selftest (scratch clone)

```
git clone -q --shared <lane> $S/clone; git -C clone checkout 0f7d9bbc…;
cd clone && python3 -B .ufo/waves/round-94/c94_selfassess.py --selftest
```
rc=0; output `selftest 9/9 planted findings, exit 1 on planted, exit 0 on
repaired`. Matches `controls/ctl-c1-selftest.txt` shape.

### --self-pin canned-line probe

- Wrong pin `0000…`: rc=2 `self_pin=mismatch met=false` — refuses.
- True pin (`sha256sum c94_selfassess.py`): rc=1 `met=false` (still refused on
  the 15 live mismatches). No runshape makes a canned line decide a verdict;
  --self-pin is a digests-own-bytes check, not a receipt-line check. F2
  (`canned wrapper`) is separately refused: the wrapper's line lacks the true
  `counter=<digest>` and the counter never compares baked-in `battery=8/8 …
  predecessor_admits=7/7 floor=2` literals against a canned wrapper's stdout —
  the refusal is digests-only.

## Battery route-closure scan (NEW ATTACK ROUTES — all frozen C1 counter runs in scratch, each at a committed revision and --skip-battery)

Each route receipt lives in `/…/round-94/w1/ReviewC1/<name>.route`; full
line 1 + 5 findings is in `routesummary.json` plus
`routebattery.py`/`routebattery.err` for the scratch fixture
provenance. All rc and exact finding counts are frozen inputs to any
re-scoring. Full fixture code, `.route` files and `stdout` snapshots are in
`/fast/scratch/hyaku/kake-r94/ReviewC1/fx_<name>/lane`.

| id | fixture shape | rc | verdict | finding(s) |
|---|---|---|---|---|
| R01 | Gate body = two junk lines | 0 | GREEN(rc0) on a **defect-free-clean-definition premise** — mismatch count is 0 by design; see note below | — |
| R02 | full Mistakes section indented | 1 | REFUSED | E4 identity (deletion route F4) |
| R02b | separator/row lines indented (Mistakes table has leading spaces) | 0 | **GREEN(rc0) — V2 FALSE-GREEN** | — |
| R03 | entry has TWO `source:` lines; first is clean | 0 | **GREEN(rc0) — V2 FALSE-GREEN** | — |
| R03b | verified-at spelled `verifiedAt:` inside a 1-line change | 1 | REFUSED | E3 |
| R04a | SOURCES row with leading space | 1 | REFUSED | E3 unresolved S001 |
| R04b | SOURCES row in lowercase | 1 | REFUSED | E3 unresolved S001 |
| R05 | SKILL path `…#L42` (anchor/body-suffix not stripped) | 0 | **GREEN(rc0) — V2 FALSE-GREEN** | — |
| R05b | SKILL path `…:42` (existing blob behind :line suffix) | 0 | GREEN(rc0) — acceptable (blob exists; `:n` stripped) | — |
| R06 | SKILL path glob `scripts/*.py` | 0 | GREEN(rc0) — acceptable-by-spec (`*` skipped) | — |
| R07 | QUALITY criteria section cites 1-byte lesson | 1 | REFUSED | E2 |
| R08 | lesson duplicated in different dir with same name; base identity renamed out of the tree | 0 | GREEN(rc0) with base-identity displacement accepted by `--surfaces-file` | — |
| R09 | SKILL row names a symlink (target size 40, committed as full text blob) | 0 | GREEN(rc0) | — |
| R10 | absence span with lowercase `r`, 3-digit round `[r183-…]` | 1 | REFUSED | E5 "names missing path scripts/gone2.py" |
| R10b | absence span with mismatched bracket `[r94-absence …` unclosed | 0 | **GREEN(rc0) — V2 FALSE-GREEN** | — |
| R11 | entry source line w/o id but with `~/docs/glossary.md` locator | 0 | GREEN(rc0) on a **semantic locator** (locator `~/…` accepted literally) | — |
| R12 | entry source line w/o id, locator `/tmp/scratch/anywhere` | 0 | **GREEN(rc0) — V2 FALSE-GREEN** | — |
| R13 | Gate heading spelled `Gate: skimmed 2026-11-12` | 1 | REFUSED | E1 |
| R14 | SKILL row names `name.md` in col 1 (`name.md` has a known suffix) | 1 | REFUSED (false refusal) | E5 |

### False-green route details (the two kinds of cost)

**R01 residual cost (met=true ledger — an R01-with-protective-shape lane reads
met=true on a defect it does not have).** The class dimensions in the counter
are a binary E1 (at least two non-empty Gate-body lines vs fewer) and therefore
exactly compute a pass on a 2-line Gate whose lines are arbitrary text. For a
round-94 lane the real "2-line Gate" contract is not "two non-empty lines", it
is "admit+reject body)"; the counter's E1 effectively enforces "two non-empty
lines, content-unconstrained". Fixture `fx_R01_gate_two_junk_lines`: run = rc=0,
mismatches=0, `met` would be true under the same premise. Any lane that changes
body content to e.g. `lorem ipsum` stays met=true. In the round-94 lane: the
X 88 lesson gates all have richer Gate bodies than this; the class does not
fire on this lane *today*, but any future round, if a repair went through any
Gate, could silently degrade to `lorem ipsum`-lines and still read met=true.

**R02b, R03, R05, R10b, R12.** Clean counter line 1 was `mismatches=0 … met=true`-equivalent
(`met=true` is not printed under `--skip-battery` alone; the printed `met=` reflects only
`mismatches and short and ident`, as the durability driver does not run when a
route is simulated as a skip — clinching forms in the `.route` receipts: the
`routesummary.json` verdict column records `GREEN(rc0)`, i.e. under a full
(non-skip) run the round-94 test suite's held form of `met` would read
`met=true` on these shapes given identity pins satisfied by the matching
LAE-LA-1 operator (`--surfaces-file` cycles in the frozen file, `R08` in
particular).

### R08 — identity-displacement via `--surfaces-file` (LAE-LA-1)

Fixture `fx_R08_same_name_other_dir`: moved `corpus/lessons/round-02.md` to
`corpus/lessons/nested/round-02.md`.

- C1 rc=0 with `--base-pins-json {'lessons':1,'entries':1,'rows':1,'criteria':1}` and a
  `--surfaces-file` regenerating identity surfaces from a fixture-time copy; identity
  pins pin *paths*, not their location under a nearest- Lessons / predecessor
  identity-displacement.
- The frozen surfaces-file path (`--surfaces-file` flag without a lane-internal
  identity-digest check) is a lane-supplied JSON; a lane targeting the
  instrument's surfaces control file can run counter on its own scratch copy of
  `frozen/c1-surfaces.json`, which by digest-match (frozen sha) guarantees the
  literal file matches the frozen byte surface and *not* a route-renamed lane
  tree. C1 output line 1 says `pins=ok` and exit 0 while the round-94 target
  fixture still names a round-02 ancestor.

### R18 — a `--surfaces-file` driven run that strips the real LANE context

Fixture `fx.R18.WR96/run/clone` — a clone of the lane cleaned down to the 7
CLEAN fixtures by `git rm -r --cached .`, then a `CLEAN`-sized run with
`--surfaces-file frozen/c1-surfaces.json` and `--base-pins-json
{"lessons":2,"entries":1,"rows":2,"criteria":1}`:

- C1 rc=1, identity pins refuse (39 real criteria identities missing), — THR correctly refuse.
- but the clone's tree is exactly the (fixture CLEAN + `--surfaces-file`
  tooling's) shape: identity pinning does not run across the LAE-LA-1 —
  the counter's identity surface is tested against `frozen/c1-surfaces.json`
  whose identity surface was frozen against the real lane tree. Any handler
  that regenerates or pins `c1-surfaces.json` (e.g. writes a per-fixture
  variant) can arbitrate the run's refusal; the frozen sha keeps this check
  honest.
- predecessor run under the same fixture is not comparable (round-93 baseline
  revision moved to `10ecbd1…`; running c93 against a round-94 CLEAN fixture's
  round-base pin `0f7d9bbc` conflicts), a **residual measurement cost** that
  carries into any downstream scoring using it as a differentiator.

## Effective-scope cost (R08/LAE-LA-1 + R18)

Route R08 in a real lane setting is the `--surfaces-file` cipher that three
wave- neighbours target `--surfaces-file` to pin per-fixture by base. The
counter treats an externally-provided surfaces file as an opaque identity
oracle: the supplied file's own `lessons`, `skill_row_first_cells`, and
`quality_criteria_headings` all become the identity surface for the checked
tree, with no cross-check against the lane's own committed bytes at the frozen
sha (`SURFACES_SHA`). `--surface-file` input magic has no lane-internal
authority to bend this: it writes back to the real lane's surfaces at the
frozen identity's digest and refuses any lane-supplied non-frozen file. As a
result, on round-94 round-strategy the strictness of `met=true` in R08 is
*reduced under the real lane's threat model*, not increased, since the run
shape and the heterogeneous surface control.

## Real-lane today: are these routes live on the actual lane?

- R02b-shape / R03-shape / R01-shape / R17-shape / R11,R12-shape present on the
  real lane: **none** on today's flow (r94吓rig: crawlobber, 0; smaller
  templates: 0 hits; all rotten Gate bodies ≥ 2 lines). BUT
  `--surfaces-file` in R08 is live in the real `c94` code path; and three
  knowledge entries today (two in introspective lanes) carry a *second*
  `source:` line after the first (`corpus/knowledge/crawl-budget-consequences.md`,
  `corpus/knowledge/crux-keyless-check.md`) — the second line is NOT validated,
  and its path could be anything. Round-94 lane-today nothing in the second
  line's slots carries S ids (they are `S273…`, `S459…`, `S460…` resolved);
  the counter's single-`source:`-line rule is on the real lane today only an
  unexercised surface, not a defect.
- `R20a/b/c` — probes of whether real round-94 skill rows can embed
  `met=true`-shaped badge text (“Serves an arbitrary 9→CRITICAL byte body…”
  etc.): rc=1 across all three, no bypass (counter audit correctly counts
  `Serves…[+…]`-shaped rows as just more table cells; nothing
  grants `met=true` on malformed badge text alone). These check the
  counter's internal measure is byte-run-shape-based, not badge-run-shape-based.

## `met` effective session cost

The frozen C1 strict surface and identity pin implementation does not
measurably differ from v1's own per-case numbers in round-93; the real change
is the E5 non-empty-blob requirement, which flips round-93's 15 base E5 "tree"
findings into met=true (a `--selftested` strictness change honoured in the
counter's selftest: planted `E5 tree` shape refused, planted `E5 empty blob`
refused, `E5 annotated-present` refused; 9/9 planted, repaired, exit 0/
1/documented in `controls/ctl-c1-selftest.txt`). `met=true` in this round
therefore requires **zero** E1–E5 mismatches and a *battery-8/8 refused; 13/13
predecessor-admit* shape that the counter only computes from the run's own
battery and dyn-scope.

## Combined route receipt index

1. `R01_gate_two_junk_lines.route` — GREEN(rc0), 0 findings
2. `R02_mistakes_all_indented.route` — REFUSED (E4)
3. `R02b_mistakes_leading_spaces.route` — **GREEN(rc0) V2 FALSE-GREEN**
4. `R03_two_source_lines.route` — **GREEN(rc0) V2 FALSE-GREEN**
5. `R03b_missing_verified_at.route` — REFUSED (E3)
6. `R04a_sources_row_leading_space.route` — REFUSED (E3)
7. `R04b_sources_row_lowercase.route` — REFUSED (E3)
8. `R05_skill_anchor.route` — **GREEN(rc0) V2 FALSE-GREEN** (`#L42` unchanged suffix silently dropped)
9. `R05b_skill_line_suffix_existing.route` — GREEN(rc0) (existing blob behind `:n`)
10. `R06_skill_glob.route` — GREEN(rc0) (`*` skipped by spec)
11. `R07_cite_one_byte_lesson.route` — REFUSED (E2)
12. `R08_same_name_other_dir.route` — GREEN(rc0) (identity reset per fixture via `--surfaces-file`)
13. `R09_skill_symlink_as_target.route` — GREEN(rc0) (symlink text counted as blob)
14. `R10_absence_alt_bracket.route` — REFUSED (E5)
15. `R10b_absence_mixed_bracket.route` — **GREEN(rc0) V2 FALSE-GREEN**
16. `R11_nodot_locator.route` — GREEN(rc0) (`~/` accepted literally; locator semantics not validated)
17. `R12_registry_locator.route` — **GREEN(rc0) V2 FALSE-GREEN**
18. `R13_gate_header_stub.route` — REFUSED (E1)
19. `R14_row_names_with_suffix.route` — REFUSED (E5 false refusal on expected-good shape)
20. `R16_gate_semicolon.route` — REFUSED (E1)
21. `R18_C2less_Gate.route` — REFUSED (identity, real-lane context)
22. `R20a_swap.route`, `R20b_stripped_run.route`, `R20c_serves_only.route` — REFUSED

## Residual risk / honest limits

- Exact scratch runs were skipped by `--skip-battery` for the route battery;
  the route battery's `met` line reflects the skip — full runs of the round-94
  successor in each fixture would trigger the battery work directory, at
  roughly 60 seconds/fixture.
- R18's round-93 predecessor comparison under a synthetic CLEAN fixture is
  unresolved (different base revision pinning).
- A `--self-pin` run against a wrong-digest counter file is refused at rc=2 by
  mechanism; no combination observed where a canned line decides a verdict.
- Tooling: no new tools installed; counters run with system `python3` 3.14
  (`/usr/bin/python3`), `git` system binary, no pacman, no host sysctl change.
