# ReviewerC1 — round 75 / w1

Recommendation: **do not rely on the freeze counter as a complete C1 certificate**. Base reproduction agrees with the frozen diagnosis; four independent false-green mechanisms were found. This is a review recommendation, not admission of an after-state.

Axes: execution/claim fidelity; frozen-population retention; attack coverage; committed-byte reproducibility; lane/scratch isolation. No production edits or subagent dispatch.

## Findings, by severity

All source references below are to `.ufo/waves/round-75/c75_row_truth.py` **at freeze commit `88f2e05f36f008faf01fcf77afedd33ae3c53e40`**, not a later implementation. Retained counter sha256: `43538343c1f26e15a795f5486a6daca977c88ef5fa4458adacd2c68a00a596ce`.

### P1 — E4 ignores secondary path tokens

Lines 167–172 check only the selected instrument `f`; paths elsewhere in its row are not checked. F13 commits a valid `scripts/ok.py` gate with working `3/3` self-test, but its Pinned cell names nonexistent `scripts/does_not_exist.py`. Counter: **exit 0, met=true**. Frozen E4 requires every path token to resolve.

This also survives the full frozen population: A04 corrects the two known base claims, adds the missing proof-path token to the effective c74 row, and returns `files=16 mismatches=0 append_only=true met=true`, exit 0, at `75688e99541aef59143875efe43be9959013dbac`. Thus this is not merely a miniature-population artifact. Evidence: `ReviewerC1-heldout/F13-E4-secondary-missing.{SKILL.md,log,bundle}`, `A04-E4-whole-population.{SKILL.md,log,patch}`; exact commands in `additional-results.json`.

### P1 — self-test command is not bound to the instrument

Lines 173–188 accept whichever command the Self-test cell supplies. F14 names `scripts/broken.py` as its instrument but records `python3 scripts/other.py --selftest`; the other script prints `3/3` and exits 0. Counter: **exit 0, met=true**. Direct execution of the instrument's own `--selftest` exits **2**. Evidence: `F14-wrong-command.{SKILL.md,log,bundle}`, `F14-direct-selftest.txt`.

The requested prefix case F03 independently exposes the same hole: its second row first mentions `c75_row_truth.py` in Entry prose, then runs `c750_row_truth.py`. The frozen first-token rule correctly groups that row under c75, but its passing c750 command supersedes the failing c75 self-test: two rows, one derived file, met=true. This is not a regex prefix match; it is incorrect command-to-instrument binding after order-sensitive derivation.

F17 adds the failing instrument's path only in a shell comment: `python3 scripts/other.py --selftest # scripts/ok.py`. Counter again returns met=true although `scripts/ok.py` exits 2. A token-presence-only repair would not establish actual invocation. Evidence: `F17-command-comment.{SKILL.md,log,bundle}`, `edge-results.json`.

### P1 — derived-population shrink is not a finding

Lines 239–252 compare row Names for append_only, but never compare derived paths with the frozen floor. F11 keeps the prose Name `broken counter`, keeps its instrument blob committed, and rewrites that row so it carries no path token. The derivation drops `scripts/bad11.py`; append_only remains true. This is the Amendment-1 floor gap, **not deletion of the instrument blob and not a failed E4 lookup**.

Committed base `ccda8a1b0d989b978d34b0ace56d0b311c55c73d` row:

```text
| broken counter | gate (offline) | `python3 -B scripts/bad11.py --root .` | 0=met | the gate has no selftest of its own | dash | reports only | ReviewerC1 |
```

Committed tip `543ab1fd6ca9a94a053e5613bdc78cbb6ac4a206` row:

```text
| broken counter | instrument (retired in place) | subsumed by the ok counter | dash | retired | dash | reports only | ReviewerC1 |
```

Full counter stdout, exit **0**:

```text
C1v1 revision=543ab1fd6ca9a94a053e5613bdc78cbb6ac4a206 rows=3 live=3 files=2 mismatches=0 classes=- append_only=true met=true
```

Evidence: `F11-shrink.SKILL.md`, `F11-shrink.base.SKILL.md`, `F11-shrink.bundle`, `fixture-results.txt:36-37`. A delivered implementation must enforce the supplied population floor; this miniature fixture's floor is its three base-derived files, not the real lane's unrelated sixteen paths.

### P2 — `nondifferential` silently grants the differential exception

Line 183 uses substring membership rather than matching the frozen **word** `differential`. F16 Kind `gate (nondifferential; offline)` and Self-test `the gate has no selftest of its own` produce **exit 0, met=true**, despite no differential declaration. Evidence: `F16-nondifferential.{SKILL.md,log,bundle}`. The legitimate differential-word F06b remains a required green control.

## Independent base reproduction

Measured revision: `c9c5e484c533aa65f4374b841a3edcf572ed19a9`. Counter bytes come from the freeze commit: attempting `git show c9c5e484c533aa65f4374b841a3edcf572ed19a9:.ufo/waves/round-75/c75_row_truth.py` exited **128**, because the counter did not yet exist at base. This is not an unevaluable base measurement: the freeze counter was run with `--revision` naming base.

Commands (S was `/fast/scratch/hyaku/kake-r75/ReviewerC1`):

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show c9c5e484c533aa65f4374b841a3edcf572ed19a9:SKILL.md
python3 -B "$S/derive_population.py" "$S/SKILL.base.md"
python3 -B "$S/counter-at-freeze.py" --root "$S/lane-shared" --revision c9c5e484c533aa65f4374b841a3edcf572ed19a9 --base c9c5e484c533aa65f4374b841a3edcf572ed19a9 --work "$S/base-work" --json
```

Exit codes respectively **0, 0, 1**. Independent extraction: **28 rows, 16 live rows, 16 distinct files**. All sixteen match both the contract list and counter JSON results (`population-comparison.json`); complete path/line list is retained in `population.txt`.

Base verdict: `mismatches=2 classes=E1 E3 append_only=true met=false`:

- E1 `.ufo/waves/round-69/c69_tmp_honour.py`: base `SKILL.md:1426`, gate without self-test or differential declaration.
- E3 `.ufo/waves/round-74/c74_registry_gap.py`: base `SKILL.md:1432`, five distinct fixture ids claimed, observed total eight.

`base.log` retains the full counter result and per-instrument command exits. The independent extractor was written separately from the counter but uses the frozen rule; its agreement is a reproducibility cross-check, not an independent semantic oracle.

## Held-out fixture outcomes

Each named state has a retained text `*.SKILL.md`; miniature git bundles preserve committed revisions and, where relevant, their base commits. Exact identities are in `fixture-identity.txt`; exits/stdout in `fixture-results.txt`, `additional-results.json`, and `edge-results.json`. **Accepted attack** means met=true for a state that should be red, not merely a successful green control.

| State | Expected | Observed exit / verdict | Classification |
|---|---|---|---|
| F01 path only in Pinned-values; gate without working Self-test cell | red | 1 / E1 | rejected attack |
| F02 path only in Owner prose; missing instrument | red | 1 / E4 | rejected attack |
| F03 c75/c750 first-token collision and cross-command supersession | red | 0 / met=true | **accepted attack** |
| F03M additional cross-command rewrite | red | 0 / met=true | **accepted**, same root defect |
| F04-base honest three-fixture row | green | 0 / met=true | green control |
| F04-false-supersede claims four fixtures and 4/4, observes 3/3 | red | 1 / E2 E3 | rejected attack |
| F05 a/b pair in prose, no command; gate | red | 1 / E1 | rejected attack; E2 itself is correctly inapplicable without command |
| F06a no own selftest, no differential word | red | 1 / E1 | rejected attack |
| F06b no own selftest, differential word in Kind | green | 0 / met=true | green control under frozen rule |
| F07 ids f1 f2 f3, observed total three | green | 0 / met=true | required green control |
| F08 three ids, observed total four | red | 1 / E3 | rejected attack |
| F09 exit-0 command prints prose but no tally; claims 3/3 | red | 1 / E2 | rejected attack |
| F10 row deleted between committed base/tip | red | 1 / append_only=false | rejected attack |
| F11 row Name retained, instrument no longer derived | red under supplied population floor | 0 / files=2 met=true | **accepted floor attack** against v0 |
| F12 appended new live gate, selftest exits 1 | red | 1 / E1 | rejected attack; new-row coverage works |
| F13 secondary path absent | red | 0 / met=true | **accepted E4 attack** |
| F14 unrelated script's command supplied | red | 0 / met=true | **accepted binding attack** |
| F15 contradictory 0/3 then 3/3 in same cell | ambiguous multiple claims | 0 / met=true | last-pair-only residual; not counted as proven defect |
| F16 nondifferential substring | red | 0 / met=true | **accepted E1 attack** |
| F17 instrument path only in shell comment | red | 0 / met=true | **accepted binding attack**, same root defect |

Twenty committed measured states across at least seventeen distinct fixture scenarios; no semantic-security or saturation claim follows from this bounded set.

## Three requested cheap-append attempts against the actual base

All mutate only scratch clones, append `### Round 75 gate registry additions`, commit there, and measure that exact revision with `--base c9c5e484…`. Exact argv, revisions, stdout, exits: `additional-results.json`; committed SKILL snapshots and patches are retained.

| Attempt | Revision | Files / mismatches | Exit / result |
|---|---|---|---|
| A01 junk repeats both wrong claims | e6b964737ce6cd7bd01368184d1b823fbbf29e0b | 16 / 2 | 1 / rejected |
| A02 relabel c69 only | e5555b315640abd1ff5438f807257cb6e644e390 | 16 / 1 (E3) | 1 / rejected |
| A03 add honest new live instrument | 3d0adb217740a933f5377adc20b08dfa5d1788bb | 17 / 2 | 1 / rejected |

**Successful cheap-append attempts: 0/3.** Population growth itself is permitted by Amendment 1; adding a file does not erase existing findings. A04 is an additional E4 adversarial state, not one of these three: it deliberately corrects the original claims before introducing a separate false claim.

## Residual risk / verification gaps

- Only the freeze implementation was exercised. The L1 has acknowledged E4, binding, and floor gaps and described planned repairs; **no claim is made that any later implementation passes these held-outs**. Re-run its amended population option with the miniature fixture's own base-derived floor.
- E2 takes only the last pair in a cell and the last pair in concatenated stdout/stderr (`claim_pair:133-138`, `observed_pair:141-146`). F15 proves that an earlier contradictory tally is ignored. Historical-vs-current multiple tallies already exist at base, so rejecting every multi-pair cell without a frozen interpretation would be a predicate change. Keep this as explicit ambiguity, not an invented new kill rule.
- append_only checks Name presence, not row-byte preservation (`241-248`), exactly as its frozen definition says. It does not independently certify append-only editing of old cells.
- Reusing an existing `--work/tree` skips checkout (`228-239`); all reported measurements use fresh work directories. No stale-work exploit is claimed as executed.
- LSP device unavailable: `read xd://lsp` returned `No such tool`. Caller/definition/diagnostic semantic checks could not run; source inspection and executed fixtures are the evidence, not semantic grep proof.
- Review is C1 pre-after-state only; no C2, resume-continuity, final integration, or canonical-runtime saturation claim was assigned or verified.

## Reproduction / hygiene

`build_fixtures.sh` (exit 0), `additional_attacks.py` (exit 0), and `edge-results.json` retain exact construction/measurement evidence. `all-commands.json` records fixture argv and exit codes. Bundles are small self-contained miniature repos; full-lane variants retain patches against the named base, not a full repository mirror. For replay, clone a fixture bundle into a new scratch mktemp directory, pass its recorded revision/base, and use a fresh external `--work` directory with the retained counter.

Final fixture construction used `mktemp -d` / `mkdtemp(dir=S)`, explicit scratch/work placement, `git -C`, and toplevel assertions before fixture commits. Earlier discarded pilot fixtures used fixed names under the same owned scratch tree; their measured receipts were replaced by the final mktemp fixtures. One initial counter extraction was briefly placed at `/fast/scratch/.r75c1-counter-freeze.py` rather than under S; it was moved into S immediately and the stray pathname no longer exists. No lane production files, sibling lanes, fleet tracked files, PATH directories, or host services were modified. No tool installs/updates.

Artifacts were copied into the assigned heldout directory before deleting S; cleanup completion is recorded by `cleanup.json`.

Self-evaluation: accuracy 4/5 (freeze-only, not repaired-tip evidence); completeness 5/5 (all requested fixture classes, base derivation and three append attempts); clarity 4/5 (many fixture identifiers, indexed receipts); actionability 5/5 (bundles/patches/commands retained); conciseness 4/5 (full F11 bytes retained as requested). Priority: replay the retained cases against the delivered counter, not infer repair success from plans.

Report: .ufo/waves/round-75/w1/ReviewerC1.md
