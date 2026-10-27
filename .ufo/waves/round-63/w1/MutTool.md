# Seat: MutTool — mutation-test of scripts/quote_class.py (round-63 C2 tool)

## Scope

Tasked item: `>=6` mutants of `classify` and the selftest harness of
`scripts/quote_class.py` (frozen sha256
`431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14`), each run
through its own `--selftest` detector: "the selftest must fail or the mutation
is a survivor."

Lane root (detector cwd — the tool binds fixtures via `LANE_ROOT = Path.cwd()`,
source line 27, so mutants must run from here, exactly as
`.ufo/waves/round-63/c63_quote_tool.py` line 57 invokes it):
`/home/vgpnk/Projects/shokunin/kake-shokunin`

Isolated scratch copy: `/fast/scratch/hyaku/kake-r63/MutTool/pristine.py`
(cp of the fleet file; the fleet file was never touched). All mutants are
separate files derived from that pristine copy by one localised substitution
each — pristine bytes were never modified in place, so the scratch copy is
byte-exact throughout (restoration = hash equality, below).

## Baseline (pristine)

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 -B /fast/scratch/hyaku/kake-r63/MutTool/pristine.py --selftest
case inline_raw_substring: derived=raw-substring expected=raw-substring pass
case markup_collapsed_only: derived=collapsed-only expected=collapsed-only pass
case absent_everywhere: derived=absent expected=absent pass
case s432_real: derived=collapsed-only expected=collapsed-only pass
selftest 4/4
EXIT=0
```

`--selftest --json` also exits 0 with `"ok": true, "passed": 4, "total": 4`.
Baseline green → detector is live; kills below are real kills, not baseline
artifacts. Python 3.14.8.

## Mutants (single-site diffs against pristine)

| # | file | mutation |
|---|------|----------|
| M1 | m1_no_collapsed.py | `classify`: deleted `if quote in text: return "collapsed-only"` (collapsed-only branch removed) |
| M2 | m2_swap_qr_callsite.py | callsite `classify(case["quote"], raw, text)` → `classify(raw, case["quote"], text)` (quote/raw args swapped) |
| M2b | m2b_swap_blobs.py | ambiguity coverage: `classify(case["quote"], text, raw)` (--raw/--text blob args swapped) |
| M3 | m3_text_before_raw.py | `classify`: `quote in text`/`collapsed-only` branch moved ahead of `quote in raw`/`raw-substring` (text checked before raw) |
| M4 | m4_absent_as_rawsub.py | `classify`: `return "absent"` → `return "raw-substring"` (absent returned as raw-substring) |
| M5 | m5_bad_fixture_path.py | `FIXTURES = Path("scripts/fixtures/quote-class")` → `.../quote-clas` (fixture path wrong) |
| M6 | m6_json_lies_passed.py | `--selftest --json` path in `main`: sets every `c["passed"]=True`, `passed=total`, `ok=True` before serialising (JSON marks failed cases passed) |
| M7 | m7_containment_flip.py | bonus: `classify` first check `quote in raw` → `raw in quote` (containment direction flipped) |
| M8 | m8_harness_all_pass.py | bonus: selftest harness `passed = error is None and derived == case["expected"]` → `passed = True` (harness marks every case passed) |

Mutant file sha256s (for reproduction):
m1 `5505750808e2b14209d4e7771dfb48916dd05ecf75b007b6a5ad1f956e39606b`,
m2 `ec63e7fcdfc030dc50531103409e45f4d6957782b4b0e6399607296376cc2f3b`,
m2b `738b923ae188668a58a2bde3f769a2777950a64d8ab6f5ccc5ecbf1bd22b0056`,
m3 `ad054df0a3dbd3712b7722fd707d7e441080e122f58f5d7c63b63b2ee80bc00b`,
m4 `290b429d34a254099ecda79171bae848f07284526ba51c9350bb0bfb1a0d8887`,
m5 `59c729a15d7322d72f5198d5c3cfffa0520a562db90391da75110bc20e38c38a`,
m6 `2f39d2a3a0315ff0fbbaf3afeb9692d6f24da81c64afa04a82a185d557745e9a`,
m7 `6ca03d1b5c9cb3dd182ef688e029c7444c11d4031783c274b71e7719b6ee130e`,
m8 `a8ef6209910940447babcbc51697751d825280ed85647dd37c72f480b37d7566`.

## Kill matrix — detector `python3 -B <mutant> --selftest` (plain mode, cwd=lane root)

| mutant | `--selftest` output (score) | exit | verdict |
|--------|-----------------------------|------|---------|
| M1 | markup→absent FAIL, s432_real→absent FAIL; `selftest 2/4` | 1 | KILLED |
| M2 | inline→absent FAIL, markup→absent FAIL, s432→absent FAIL; `selftest 1/4` | 1 | KILLED |
| M2b | markup→raw-substring FAIL, s432→raw-substring FAIL; `selftest 2/4` | 1 | KILLED |
| M3 | inline→collapsed-only FAIL (text hit shadows raw hit); `selftest 3/4` | 1 | KILLED |
| M4 | absent_everywhere→raw-substring FAIL; `selftest 3/4` | 1 | KILLED |
| M5 | 3 cases derived=unevaluable (FileNotFoundError …/quote-clas/…), s432 passes (its path is independent); `selftest 1/4` | 1 | KILLED |
| M6 | `selftest 4/4`, all cases pass — lie lives only on the `--json` path | 0 | **SURVIVOR** |
| M7 | inline→collapsed-only FAIL (raw blob cannot be a substring of the 15-char quote); `selftest 3/4` | 1 | KILLED |
| M8 | `selftest 4/4` — harness reports pass regardless | 0 | **SURVIVOR** |

Score: 7/9 mutants killed by the tasked detector. Both survivors are
*self-reporting* mutants — they corrupt the verdict, not the derivation, so a
detector that only reads the verdict cannot see them while all cases pass.

## Survivor analysis — dormant lies, and what actually sees them

Both survivors are equivalent mutants **while the corpus is green**:
`diff` of `--selftest --json` output, pristine vs m6 and pristine vs m8, is
byte-identical (`ok:true, passed:4, total:4`, all `passed:true`) — the lie has
no failed case to mask, so no selftest of any mode can distinguish them.

To expose the lies, I fired live-fire probes = a real classify defect (M1's
missing collapsed-only branch) armed with each lie:

- **m1_m6_livefire.py** (sha256 `7b163d3ebdeb84ea6ec98aae841e575683a48b4fc92de3613761ffabdc165b61`):
  plain `--selftest` still exits **1** (`selftest 2/4`, two FAILs) — the
  JSON-path lie cannot rescue a real defect under the plain detector.
  `--selftest --json` exits **0** and emits `ok:true, passed:4/4`, all
  `passed:true` — the lie fires — but `derived` stays truthful
  (`absent` vs `collapsed-only`).
- **m1_m8_livefire.py** (sha256 `f3b83e6a2802ee0f1c6b5574f4deb049c1507a805ec9c81180448f6fc588c5e5`):
  plain `--selftest` prints `pass` on genuinely-failed cases, `selftest 4/4`,
  exit **0** — a live false green, the same defect class as the round-62
  falsified counter (`counter-false-green-l1.txt`).

Would the lies fool the actual claim instrument? Simulated
`c63_quote_tool.py`'s exact predicate (frozen case ids, `passed is True`,
`derived == expected`, `ok`, `total == passed == 4`) over each mutant's
`--selftest --json` output:

| blob | selftest exit | frozen_ok | counter met |
|------|---------------|-----------|-------------|
| pristine | 0 | True | **true** |
| m6_json_lies_passed | 0 | True | true (dormant; indistinguishable) |
| m8_harness_all_pass | 0 | True | true (dormant; indistinguishable) |
| m1_m6_livefire | 0 (lie fires) | **False** | **false** |
| m1_m8_livefire | 0 (lie fires) | **False** | **false** |

The c63 counter kills both armed lies: `passed:true` cannot rescue a case
whose `derived` the counter re-checks against `expected`. Its per-case
`derived==expected` cross-check (counter lines 70–74) is exactly the
defense the tool's own exit code lacks.

## Findings

1. The 6 tasked defect classes in `classify` and the selftest fixture wiring
   are all killed by `--selftest` — both orderings, both swap directions,
   absent-aliasing, and missing fixtures. The derivation half of the harness
   has real teeth.
2. **Coverage finding (survivor M8):** a harness-side lie (`passed = True`)
   is invisible to `--selftest` in both modes and stays invisible under
   `--selftest --json` even when armed with a real defect — the plain
   detector is a false-green channel of the same shape the c62 counter had.
   Only an external checker that re-derives or re-compares `derived` vs
   `expected` per case (as c63_quote_tool.py does) catches it. Bare
   `quote_class.py --selftest` as a standalone gate would be attackable;
   as counted by the c63 counter it is not.
3. **Coverage finding (survivor M6):** the `--json` output path can lie
   about `passed`/`ok` without the plain `--selftest` detector ever
   exercising it — a blind spot of the plain-mode detector by construction.
   Armed, the lie still fails the c63 counter because `derived` is printed
   truthfully and re-compared.
4. Both survivors are equivalent mutants while all cases pass — killing them
   requires a case that can fail (a negative/red fixture), which the frozen
   corpus deliberately lacks.

## Restoration / non-mutation evidence

- Fleet file before and after the wave:
  `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14
   /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py`
  (sha256sum, before = after = frozen claim value; never opened for write).
- Pristine scratch copy after all runs:
  `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14
   /fast/scratch/hyaku/kake-r63/MutTool/pristine.py` — byte-exact; mutants
  were separate files, nothing to restore.
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain
  scripts/quote_class.py` → empty (`git-status-clean`). No commits, no
  git/jj mutation anywhere; no fixture repos created (none needed — the
  selftest binds committed lane fixtures via cwd).
- Scratch inventory: pristine.py + 11 mutant .py files under
  `/fast/scratch/hyaku/kake-r63/MutTool/` only.
- Tools installed: none (Python 3.14.8 already present). No pacman.

Report: .ufo/waves/round-63/w1/MutTool.md
