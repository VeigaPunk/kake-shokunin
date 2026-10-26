# CriticC2Gate

Seat: critic (W1, pre-data). Target: `C2` gate `c57_idresolver_gate.py` (v1, 218 lines) against the frozen predicate
`met: gate_conditions_passed == 5 of 5`. Method: read the gate and contract, then build candidate tools in a throwaway clone and
run the real gate against them. No lane file was touched except this report; the lane was read with `git show`/`git grep` only.

Probe rig (reproducible): `D=$(mktemp -d); git clone -q <lane> $D` (toplevel verified `== $D`); each candidate committed inside
`$D` with `-c user.name=selftest -c user.email=selftest@local`; gate run as `python3 -B <lane>/.ufo/waves/round-57/c57_idresolver_gate.py
--root $D --revision <candidate> --fleet /home/vgpnk/Projects/shokunin`. Reference implementation of the docstring CLI ("genuine
tool", 18 selftests): **5/5 PASS**, `G5 summary=(104,104,0,0,0)` — the gate does accept a correct tool, so every finding below is a
differential against that baseline.

## ATTACKS:

A1 — **constant printer reaches 5/5 with no capability (empirical, confirmed).** Minimal input: 45-line `scripts/id_resolver.py`
that (a) prints `selftest: 24/24` for `--selftest`, (b) prints the four `EXPECT_FIXTURE` lines + `ids_cited=6 ids_resolved=2
dangling=4 owned_elsewhere=3 unowned=1` when `--root` ends in `demo-shokunin` **and** `corpus/knowledge/sub/bad.md` exists,
(c) prints five `DANGLING` lines with `owners=kotodama-shokunin` when `--revision` starts `3994101`, (d) otherwise prints
`ids_cited=104 ids_resolved=104 dangling=0 owned_elsewhere=0 unowned=0`. Predicted 5/5; **observed 5/5 met=True** (clone rev
`082a7401`, exit 0). Nothing in the fixture is randomised: lane name `demo-shokunin`, ids `S101/S200/S0300/S777`, sibling names
`alpha-/beta-shokunin`, and the expected dict is a literal in a file that ships in the same revision. Two stronger variants of the
same hole: (A2) the gate is its own oracle — `EXPECT_FIXTURE`/`EXPECT_SUMMARY`/`RED_REV` are committed at the measured revision and
the tool runs with `cwd=<clone>`, so it can `exec` the gate file and print the key instead of hardcoding it; (A3) the fixture is
detectable by path — `tempfile.mkdtemp(prefix="c57-fixture-")` plus a fixed basename `demo-shokunin` (A1 used the basename form).
Both predicted and implied 5/5.

A4 — **G3's clean half tests nothing.** Gate line:
`ok = rc2 == 0 and not d2 and s2 is not None and s2[2] == 0`. A1's clean run printed `(104, 104, 0, 0, 0)` for a fixture that cites
two ids and got **PASS**. Minimal input: any tool that prints `dangling=0` and exits 0. Predicted PASS; observed PASS in the A1 run
note (`clean exit=0 summary=(104, 104, 0, 0, 0)`).

A5 — **`ids_cited >= 100` is decorative.** The gate never computes its own cited count, so `print("ids_cited=100 ...")` satisfies
the floor. Real numbers: 104 distinct word-bounded ids at HEAD, 99 at `3994101`, 1126 token occurrences. The floor is 4 below the
truth and 1 above a defensible narrower count (prose-only = 101, header-only ids = 3: `S019 S081 S087`). Predicted PASS with a
constant; observed PASS (A1 printed 104, would pass with 100).

A6 — **G5 is green by construction.** At HEAD the lane registry holds `S367 S372 S373 S390 S409` (5 rows, verified) and
`cited − registry = ∅`. G5 therefore only re-tests arithmetic a constant tool already prints. Observed: A1's G5 PASS.

A7 — **revision special-case.** `RED_REV` is a public constant; `if rev.startswith("3994101")` is one line (A1 branch (c)).
Predicted 5/5; observed 5/5.

A8 — **G4 checks membership, not the owner set, and never checks `cited-by`.** Gate line:
`ok = (rc == 1 and sorted(dang) == RED_IDS and all(RED_OWNER in v[1].split(",") for v in dang.values()) and summ is not None and summ[2] == 5)`.
A tool may print `owners=kotodama-shokunin,anything` and `cited-by=x` for the five ids and pass. Minimal input: five lines with a
bogus `cited-by`; predicted PASS.

## WRONG-REJECT:

W1 — **the contract's literal id rule fails the gate (empirical).** Contract C2 surface says "lists every `S###` id cited"; the gate
docstring pins `S` + 3-or-more digits **word-bounded**. A genuine tool using `re.compile(r"S\d{3,}")` scores **1/5**
(G2/G3/G4/G5 FAIL). Why it matters beyond formatting: at HEAD the loose rule finds exactly one extra id, `S404`, from the variable
name `S404_SHA256` in `corpus/knowledge/free-read-verbs.md:195`; `S404` is **not** in the lane registry and **is** held by
kotodama, so the tip is not actually dangling-free under the contract's wording — G5's green rests on a definitional choice that
the contract sentence does not state. At `3994101` the loose rule yields **six** dangling ids (`S367 S372 S373 S390 S404 S409`), so
`sorted(dang) == RED_IDS` fails too. Smallest correction: state the word-boundary rule in the contract/SCORECARD sentence and in
the lesson, or make the gate own both counts explicitly.

W2 — **owner order is unpinned.** `EXPECT_FIXTURE` requires `alpha-shokunin,beta-shokunin`. A genuine tool joining a `set` or
`os.listdir` order scores 4/5 (G3 FAIL, empirical). The docstring says only "comma lane names".

W3 — **`cited-by` path form is unpinned.** `EXPECT_FIXTURE` requires exactly `corpus/knowledge/sub/bad.md`. Prefixing `./`
(a normal `os.walk`/`Path` result) → 4/5 (G3 FAIL, empirical). Absolute paths likewise fail.

W4 — **empty-owner token is unpinned.** `url-match=none` instead of `-` → 4/5 (G3 FAIL, empirical); same for `owners=none`.

W5 — **`S\d{3}` (the contract's `S###`) → 3/5** (G3 FAIL: `S0300` dropped, summary `(5,2,3,2,1)`; G2 also FAILs on a 4-digit check).

W6 — **selftest line exactness.** `print("selftest: 18/18 passed")` → G2 FAIL (4/5) because of `re.fullmatch`. The docstring does
say "a last line `selftest: N/N`", so this is defensible but brittle.

W7 — **registry indent tolerance is exactly the census rule.** A tool accepting 0–1 leading spaces → 3/5 (G3 FAIL: fixture's only
2-space row `S002` goes dangling, summary `(6,1,5,3,2)`; G2 also fails on that check). The fixture tests 0, 2 and 3 spaces; a
tool at 0–3 passes, 0–2 would pass by luck (beta's 3-space row is what would break it — untested combination).

W8 — **comma-space is silently fatal.** `DANGLE = re.compile(r"^DANGLE ... owners=(\S+) url-match=(\S+)$")`: a tool printing
`owners=alpha-shokunin, beta-shokunin` produces a line that does not match at all, so the id vanishes from `dang` and G3 fails with
a misleading note.

W9 — **fixture lanes are not git repos.** `build_fixture()` makes plain directories. A genuine tool that resolves `--root` with
`git rev-parse --show-toplevel` (natural, since `--revision` exists) exits 2 on G3 → 4/5. Predicted from the code; not run.

W10 — **default `--fleet` silently fails for clone roots (empirical).** Contract CLI is
`--root <lane> --revision <rev>`; the natural measurement root is a clone. Run with `--root $D` and no `--fleet`: fleet = `/tmp`,
G4 prints `owners={'S367': '-', ...}` → **4/5**. The pre-dispatch `--fleet` option mitigates only if the caller remembers it.

W11 — **"the lane" has no defined identity.** Docstring: "every `<fleet>/*-shokunin/` other than the lane". My path-identity tool,
run with `--root $D` (clone outside the fleet), reported `owners=kake-shokunin,kotodama-shokunin` at G4 — it counted the real lane
directory as a sibling because at HEAD that directory holds the five ids. A basename-identity tool reports only
`kotodama-shokunin`. Both pass G4 today; an equality check (recommended below) would need the identity pinned first.

W12 — **the contract's stated reason for G4 is inverted.** Contract: "a tool that reads the working tree instead of the revision
fails G4 (the red-before ids are absent at the tip)". At the tip the five ids are *present* in the lane registry (verified `reg=1`
for each at `HEAD` and at base `28fa0b2`), i.e. they *resolve*. A working-tree registry reader therefore reports `dangling=[]`
and fails G4 — outcome right, reason wrong (empirical: worktree-registry variant **4/5**, `G4 exit=0 dangling=[]`). The claim text
should be corrected in the lesson/SCORECARD; the frozen contract cannot be edited.

## FLAKINESS:

F1 — **`PYTHONHASHSEED` is unset and order is compared literally.** `run_tool` passes `env={"PATH","HOME","LC_ALL"}` only (no
`PYTHONHASHSEED`, `TMPDIR`, `PYTHONPATH`, `VIRTUAL_ENV`), so a tool that joins a `set` or `os.listdir` order is randomised per run
and a tool that needs a stripped variable dies with a bare `KeyError`. The unsorted-owner variant, same revision `62a504e7`, four
consecutive runs: **PASS, PASS, FAIL, PASS** on G3. A correct tool is therefore non-deterministically rejected; a junk tool is never
affected.

F2 — **G4 reads live sibling HEADs and records nothing.** `kotodama-shokunin@f7104cb` holds the five ids now (804 registry rows).
If kotodama rewrites/renumbers a row (a legitimate curation act) G4 fails as "not met" with no attribution; if a new `*-shokunin`
lane appears holding those ids, owners changes silently (still passes). A sibling whose registry is mid-write or unreadable makes
the tool skip or crash → G4 FAIL. The gate prints no sibling revision, so a later reader cannot tell environment from tool.

F3 — **G4/G5 are not sandboxed.** `sandbox_clone` is used only for the tool binary: the gate's clone is the tool's `cwd`, never a
tree the tool resolves against. The working tree a tool can read is the fixture dir (G3) or the caller's lane (G4/G5), so the
measured run depends on the caller's working tree, shallow-ness (missing `3994101`) and any concurrent seat edit; only G3's fixture
is hermetic. (F4, minor: 300 s × 4 tool runs on a loaded host can surface as exit 2 "unevaluable" rather than a tool defect; record
per-run wall time in the note.)

## RECOMMENDED GATE CHANGES:

R1 (kills A1/A2/A3/A7 — highest value). Randomise the fixture per run and add a second, hidden one. Replace
`    lane = os.path.join(fleet, "demo-shokunin")` with
`    nonce = secrets.token_hex(3)` / `    lane = os.path.join(fleet, f"demo-{nonce}-shokunin")`, and build the ids from the nonce
(`f"S{int(nonce[:3],16):03d}"`-style, keeping one 4-digit id, one two-sibling id, one unowned id, one 2-space and one 3-space
row); rename `alpha-`/`beta-` to `f"{nonce}-a-shokunin"`/`f"{nonce}-b-shokunin"`; compute `EXPECT_FIXTURE`/`EXPECT_SUMMARY` from
the generated ids instead of the literal dict, and run the whole G3 twice with two independent nonces. A constant printer and a
path-detector then fail both times.

R2 (A4). `        ok = rc2 == 0 and not d2 and s2 is not None and s2[2] == 0` → `        ok = rc2 == 0 and not d2 and s2 == (2, 2, 0, 0, 0)`.

R3 (A5). Before the G5 run, count the gate's own cited ids (`git -C root ls-tree -r --name-only rev corpus/knowledge` + `git show`,
`re.compile(r"\bS\d{3,}\b")`) into `own_cited`; then
`        ok = rc == 0 and not dang and summ is not None and summ[2] == 0 and summ[0] >= MIN_CITED` →
`        ok = rc == 0 and not dang and summ is not None and summ[2] == 0 and summ[0] == own_cited` (keep `>= MIN_CITED` as an
additional guard, and print `own_cited` in the note). This is what makes the floor meaningful and forces the word-boundary
decision into the open.

R4 (A8). `        ok = (rc == 1 and sorted(dang) == RED_IDS and all(RED_OWNER in v[1].split(",") for v in dang.values())` →
`        ok = (rc == 1 and sorted(dang) == RED_IDS and all(v[1] == RED_OWNER for v in dang.values())` — after R8 pins lane identity —
`              and all(v[0] for v in dang.values())` and `summ == (own_cited_red, own_cited_red - 5, 5, 5, 0)`.

R5 (F2, W12). At the top of `evaluate`, resolve each sibling's `HEAD` once, print
`    print(f"  siblings: {', '.join(f'{n}@{sha[:12]}' for n, sha in sibling_heads)}")`, and if any of `RED_IDS` is absent from
`kotodama-shokunin`'s registry at that sha, `return 2, results` with `C2 id-resolver-gate unevaluable: kotodama registry no longer
holds <id> at <sha>` — environment failures must not read as "not met". (Alternative that removes the dependency entirely: build G4's
fleet from a pinned copy of kotodama's registry blob captured at round open; the frozen condition says "with the real fleet", so the
attribution route is the contract-safe one.)

R6 (F1, W2, W8). Add `"PYTHONHASHSEED": "0"` to the `env` dict; in `parse`, store `frozenset(x.split(","))` for `owners`/`url-match`
and `frozenset` of paths for `cited-by`, comparing against frozensets; change the regex to
`^DANGLING (S\d{3,}) cited-by=(.+?) owners=(.+?) url-match=(\S+)$` so `, ` is tolerated.

R7 (W6, W9). Docstring: state "`selftest:` must be the **last** stdout line, exactly `selftest: <passed>/<total>`" and "fixture
lanes are plain directories (no `.git`); `--root` must work without git when `--revision` is absent". If a git-repo fixture is
preferred instead, add `git -C <fixture lane> init -q` + one commit inside `build_fixture`.

R8 (W11). Docstring line "siblings: every `<fleet>/*-shokunin/` other than the lane" → "other than the directory whose basename
equals `os.path.basename(os.path.abspath(root))`", and have the gate assert that the lane's own name never appears in `owners`.

R9 (W3, W4, W5). Docstring: pin `cited-by` = repo-relative paths, `/`-separated, no `./`; pin the empty-set token as `-` for both
`owners` and `url-match`; pin the id rule as word-bounded `S` + **3 or more** digits and note that `S0300` is an id while `S12`,
`AS500`, `S500x` are not. Pin the registry rule as 0–3 leading spaces (fixture already exercises 0, 2, 3).

R10 (A6, cheap). Add the arithmetic identity to `parse`/`evaluate`: `summ[0] == summ[1] + summ[2]`, `summ[2] == len(dang)`,
`summ[3] + summ[4] == summ[2]` for both G3 and G4 runs.

R11 (F3, W10). For G4/G5 pass a gate-made clone as root: `probe = sandbox_clone(root, rev)` and use `--root probe` (a full clone has
`3994101`), so the caller's working tree leaves the measurement; make `--fleet` default to "the nearest ancestor of `--root` that
contains `*-shokunin` siblings", print the resolved fleet, and return 2 (`unevaluable: no sibling lane under <fleet>`) instead of
scoring G4 FAIL when none is found. Also correct the contract's G4 sentence in the lesson/SCORECARD (W12: at the tip the five ids
are present and resolve; the worktree reader fails because it resolves them, not because they are absent).

Nothing above changes the frozen predicate or the five condition names; R1–R11 tighten what each condition actually observes.

VERDICT: gate v1 is satisfiable by a 45-line constant printer (5/5 observed) and non-deterministically rejects correct tools (G3 flake 3 PASS / 1 FAIL on one revision); randomise the fixture per run, pin order/format, cross-check `ids_cited`, and make sibling loss unevaluable before any score is taken.
