# MutKey — mutation test of the round-89 C2 candidate (wave 1)

Seat: mutation tester, leaf. Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE).
Base revision `76225160d0dff8d2042fbcd037bd08b0971d5e07`; declared freeze commit
`08ab46a130a6355a7b19e2bfa83ffb7e116db803` (2026-11-04T18:12:25-03:00).
Everything below is lane-internal evidence, not outside admission.

## 1. What was mutated

The final C2 candidate from `w1/ExecKey/`, not the counter's embedded reference:

| object | path | sha256 | note |
|---|---|---|---|
| candidate **v2** (mutated here) | `w1/ExecKey/cache_key.py` | `3a658326714108ebec8f26c6dfcff9007ad781915b909616e9313d664e7da996` | 3662 B, mtime 18:15:56; the bytes scored |
| candidate v1 | (superseded copy kept in my scratch only) | `ea8006e64a818e54d4c986b358d871716a16834bc6fa1b1666c9d787bbecc338` | first copy I took; differs only in `TCHARS = frozenset(` → `TCHARS = (` |
| counter used for scoring | `c89_key.py` (committed `46a43e94`, "freeze v2") | `d4588d4bdb4507be912410343edf7e27644eca3146a97e94d67bd406749f7e03` | = working tree at HEAD `08ce630d` |
| counter at declared freeze `08ab46a1` | `c89_key.py` | `a72d5efcab06d50c266f587f0db74ad6571e111165f61e5bc52e04615fe29bee` | strict guard; cannot score any `frozenset` candidate (§6 D1) |
| contract | `c2-contract.md` | `93a563b66799ba561128e0cdb02b03b502360b405cdef736a2035fac1297db0c` | |
| frozen cases | `frozen/c2-cases.json` | `3644da37e2531fbb4f31e8954b8837aebd43843c817789eab7c749ca34d0f2d5` | never read by the counter (§6 D8) |
| base receipt | `controls/base-c2.txt` | `1fca950945df765521f39f9dc9f02e72f51049379a607ea2ee96ff0911d70ed0` | not reproducible from `08ab46a1` bytes (§6 D3) |

Full hash sheet: `w1/MutKey/receipts/byte-identities.txt`.

## 2. Method

37 single-point mutants, each one textual replacement of one clause in the candidate
(generator: `w1/MutKey/drivers/gen_mutants.py`, sources: `w1/MutKey/mutants/`, anchors verified
unique — `mutants=37 skipped=0`). Each mutant is scored by the counter's own CLI path:

```
python3 -B <COUNTER>/c89_key.py --root <scratch-repo> --revision <sha> \
  --candidate scripts/cache_key.py --work <absolute work dir>
```

where `<scratch-repo>` is a throwaway git repo (`git init`, one commit, `git rev-parse
--show-toplevel` asserted equal to that repo) whose only content is `scripts/cache_key.py` = the
mutant bytes, so the counter's `git show <rev>:scripts/cache_key.py` fetches exactly that mutant.
`<COUNTER>` is a scratch mirror of the committed counter (`d4588d4b`) beside copies of
`frozen/c2-cases.json` and `controls/ctl-*.py`, because the counter resolves both from its own
directory. Driver: `w1/MutKey/drivers/score_all.py`; per-mutant receipts `w1/MutKey/receipts/<id>.txt`
(they contain the exact command, candidate sha256, exit code and full counter output).

Verdict rule, exactly the counter's: `met=true` (exit 0) → **SURVIVED**; `met=false` (exit 1) →
**KILLED**. The control gate is invariant here (every mutant scores `controls=5/5`, so the verdict is
driven by `frozen`, `props`, `refuse`). Reference run of the same driver: `REF ... frozen=16/16
props=200/200 refuse=9/9 controls=5/5 met=true`, exit 0 — the harness scores the candidate it was
built from as passing.

The strict-vs-relaxed guard difference cannot affect any verdict: both counters' `guard()` return
`None` for all 38 sources (reference + 37 mutants). I checked that mechanically rather than assuming it.

To separate real defects from equivalent mutants, every mutant was also run through a differential
corpus of **544 inputs** (`drivers/differential.py`, results `receipts/diff.json`, witnesses
`receipts/witness/<id>.json`): all 16 frozen cases, all 9 refusals, the 7 contract worked examples,
and adversarial inputs over the clauses — each of `%`, U+001C, U+001D, U+001E, U+001F inside a value
and inside the URI, absent vs present-empty vs value-U+001C, internal double spaces, LF/VT/FF/CR/NBSP/
EM-space at value and member edges, `*` alone / inside / adjacent to members, duplicate members,
duplicate header names, empty-ish `Vary`, token boundaries, CR/LF, URI shapes, malformed stdin, plus
400 seeded random cases. Each input is executed through the candidate's `main()` with stdio patched,
which reproduces the CLI contract (return code, stdout, refusal) without a process per input; the
reference produced no malformed stdout on the corpus (`bad_stdout=0`).

## 3. Result

**27 / 37 mutants killed = 73.0 %.** Excluding the three equivalent mutants (§5.2): **27 / 34 = 79.4 %**
of non-equivalent mutants killed.

Ten survivors: seven are real semantic divergences the counter cannot see (§5.1), three are
equivalent mutants (§5.2). Every kill is clause-specific — the first failing check in each receipt
names the clause the mutant broke, so no verdict rests on a mass failure. (M35, which emits the bare
key instead of `{"key": …}`, is killed by the stdout shape on every key case, as intended.)

Verdicts are stable: identical across two independent scoring runs and across the candidate's v1→v2
revision (the two revisions differ only in the `TCHARS` declaration).

## 4. Matrix

<!--MATRIX-->

Column notes: `frozen`/`props`/`refuse` are the counter's counts at the verdict; `first_fail` is the
counter's first `fail:` line; `differences` is the number of inputs (of 544) where the mutant's
observable behaviour differs from the candidate's; `witness` is the first such input's label.

## 5. Survivors

### 5.1 Real divergences the counter cannot kill (7)

| id | clause mutated | differences / 544 | witness (candidate → mutant) | should have been caught by | class |
|---|---|---|---|---|---|
| M06 | member OWS trim widened from `SP/HTAB` to `str.strip()` | 6 | `vary="\na\n"`: candidate refuses `vary member is not a token`; mutant keys `u␟a␞v` | a frozen case with a member wrapped in LF/VT/FF/CR or a Unicode space; the `member_ows` property only pads with `' \t'` | **case-set gap** + population gap |
| M08 | value OWS trim widened to `str.strip()` | 9 | `a="\x1c"`: candidate `…␟a␞%1C`; mutant `…␟a␞` (i.e. *present* collapses to *present-empty*) | a frozen case whose value is U+001C..U+001F alone; `value_edge_ows` pads with `' \t'` only | **case-set gap** + population gap |
| M12 | escaping of U+001C dropped | 52 | `a="x\x1cy"`: `…x%1Cy` → `…x␜y`; and `a="\x1c"` keys identically to an **absent** field (`u␟a␞␜` both) | a frozen case with U+001C in a value; `separator_collision` uses only U+001F/U+001E, `VALS` has no U+001C | **case-set gap** + population gap |
| M13 | escaping of U+001D dropped | 45 | `a="x\x1dy"`: `…x%1Dy` → `…x␝y` | any case with U+001D anywhere — none exists; the contract never assigns U+001D a layout role (§6 D9) | **case-set gap** + contract gap |
| M20 | wildcard refusal widened to `"*" in member` | 4 | `vary="a*"`: candidate keys member `a*` (a legal token); mutant refuses `vary wildcard nominates no field` | a case with `*` inside a token (`a*`, `*a`, `x*y`); the refusal list only covers a member that *is* `*` | **case-set gap** |
| M21 | duplicate-member refusal removed | 5 | `vary="a,A"`: candidate refuses `duplicate vary member`; mutant keys `u␟a␞v␟a␞v` | the contract's own refusal #9 — it has **no** frozen case, **no** entry in `REFUSALS`, **no** property | **case-set gap** (declared refusal, zero coverage) |
| M31 | URI not escaped | 209 | `uri="https://e.test/a%b"`: `a%25b` → `a%b`; and `uri="u\x1fa\x1eb"` keys identically to `{uri:"u", vary:"a", a:"b"}` (`u␟a␞b` both) | a URI containing `%` or any separator; every URI in the cases and in `_rand_case` is `https://e.test/<sep-free>` and `uri_change` only appends `/x` | **counter gap** (population alphabet) + case-set gap |

Each of these is a behaviour the contract fixes and the candidate gets right, which a single-clause
defect turns into a wrong key or a wrong refusal. M12 and M31 are not cosmetic: they make two
distinct logical inputs share one key, which is the one thing the escaping clause exists to prevent
(measured pairs quoted above). M20 is the mirror image — a legal request refused.

### 5.2 Equivalent mutants (3, 0 differences / 544)

| id | mutation | why it is equivalent |
|---|---|---|
| M33 | `name.lower()` → `name.casefold()` for header names | header names must be RFC 9110 tokens, so they are ASCII; `casefold()` and `lower()` agree on ASCII |
| M36 | `sorted(names)` → `sorted(set(names))` | unreachable: the duplicate-member refusal immediately above raises first, and for duplicate-free input `set()` is a no-op |
| M37 | absent branch emits `name` instead of `esc(name)` | names are tokens: they cannot contain `%` or U+001C..U+001F, so `esc(name) == name` |

These are reported as equivalents, not as coverage gaps — they are the vacuous corners of the
contract (name escaping, dedupe-after-refusal, ASCII-only case mapping).

## 6. Defects found in the round's own counters, contract and case set

**D1 — the declared freeze bytes cannot score the candidate at all (false positive on `frozenset`).**
`08ab46a1`'s guard forbids the substring `frozen`, and the candidate's `TCHARS = frozenset(...)`
contains it. Running the freeze-commit counter on the candidate:
`C2v1 … frozen=0/16 props=0/200 refuse=0/9 controls=5/5 met=false`, exit 1
(`receipts/frozen-candidate.txt`), with the guard note sliced into characters (`fail: s`, `fail: h`, …).
At the declared freeze, the C2 predicate was unmeetable by the candidate that was actually written,
for a reason unrelated to the contract.

**D2 — the C2 counter and its base receipt were re-frozen after dispatch (R88-E class, on this round).**
`46a43e94` ("freeze v2", 18:16:18) rewrites `c89_key.py` (→ `d4588d4b`) *and* `controls/base-c2.txt`.
`w1.ready` was committed in `2e700b9a` at 18:13:04 and the dispatch marker written at 18:13:46, i.e.
**before** the counter was changed (and before this seat started). The wave's premise is "frozen before any after-state data". The commit message
attributes the false positive to "a docstring that names the contract path"; what the candidate
actually tripped on is `frozenset` (v1→v2 diff), so the recorded reason is not the reason either.
Diff: `receipts/counter-guard.diff`; history: `git log -- .ufo/waves/round-89/c89_key.py`.

**D3 — the base receipt committed at the freeze was produced by different counter bytes.**
`controls/base-c2.txt` (committed at `08ab46a1`) ends `ctl=ctl-table met=false (shortcut guard: source
names 'c2-cases')`. The `08ab46a1` counter prints `names '.ufo/waves'` for that stub (its `FORBIDDEN`
order differs), while the relaxed counter reproduces the committed file **byte-for-byte**
(`diff` exit 0, `receipts/base-c2-diff.txt`, `receipts/live-base.txt`, `receipts/frozen-base-quiet.txt`).
So the freeze commit ships a receipt its own bytes do not produce.

**D4 — C1's R88-E repair cannot see a re-freeze.** `item_e` compares the *first-add* commit of
`c89_key.py` with the *first-add* commit of `w1.ready` and their committer times. `46a43e94` amends a
file that was already added, so it is invisible: C1's "freeze-before-dispatch" passes while the
counter was in fact amended after dispatch. The defect class the round claims to close is measured
narrower than the class.

**D5 — guard note is a string where the caller expects a list.** On a guard hit `score_candidate`
returns the note as `fails`; `main` does `for f in fails[:12]` and prints one character per line
(`receipts/timing.txt`, `receipts/frozen-candidate.txt`). The guard's actual reason never reaches the
receipt in readable form.

**D6 — a relative `--work` silently turns every candidate run into exit 2, and the control gate still passes.**
`run_candidate` passes `str(path)` (derived from `--work`) while setting `cwd=work`; with a relative
`--work` the child resolves the script against its own new cwd and fails. Measured on the oracle
probe: relative `--work` → `frozen=0/16 props=0/200 refuse=0/9 controls=5/5 met=false` with
`fail: frozen … exit 2` for every case (`receipts/probe-P2-oracle-import-split.txt`); the same bytes
and the same command with an absolute `--work` → `frozen=16/16 props=200/200 refuse=9/9 met=true`
(`receipts/probe-P2.txt`). Because `score_controls` counts `if not met: passed += 1`, a harness that
cannot run at all is indistinguishable from five rejected stubs.

**D7 — the textual guard is evadable, and the property population is what actually holds.**
Probe P2 (`drivers/P2-oracle-import-split.py`) loads the counter's own reference through
`importlib` with the path assembled from fragments: both counters' guards return `None`, and it scores
`frozen=16/16 props=200/200 refuse=9/9 met=true`, exit 0 — a candidate that implements nothing is
admitted. This is the disclosed limit, now measured. Probe P1 (`drivers/P1-case-table-split-path.py`)
reads `frozen/c2-cases.json` through a split path: it evades the relaxed guard, scores `frozen=16/16`
and is stopped only by the property population (`props=0/200`, `receipts/probe-P1.txt`). So the
freeze's claim that a case table cannot reach the population holds; the guard contributes nothing
there, and it is not load-bearing for the oracle case either.

**D8 — `frozen/c2-cases.json` is never read.** `CASES` is defined (`c89_key.py:33`) and never used;
the counter scores its embedded `FROZEN` list. The two currently agree (16/16 identical inputs and
expectations), but nothing checks that, so the artifact the freeze lists as measured can drift
silently — and the one stub that does read it (`ctl-table`) is rejected by the guard before it can
disagree.

**D9 — contract §4 and §5 disagree about the separators.** §4 declares four escapes (`%1C`, `%1D`,
`%1E`, `%1F`); §5 names three (`US` = U+001F, `RS` = U+001E, `GS` = U+001C). U+001D is escaped but
has no role in the layout, and the name `GS` is given to U+001C, which is FS in ASCII (GS is U+001D).
Consequence: the `%1D` escape can only ever be observed as a literal encoding (M13), never as a
collision guard.

**D10 — declared refusals and value classes with zero coverage.** The contract refuses "two `Vary`
members equal case-insensitively", but no frozen case, no `REFUSALS` entry and no property exercises
it (M21, M36). The population's alphabet (`NAMES`, `VALS`, `_rand_case` URI choices) cannot reach:
U+001C/U+001D in values, `%` or a separator in a URI, `*` inside a member, non-OWS whitespace at
value/member edges, internal whitespace in a value. Those are exactly the seven real survivors.

**D11 — unexplained concurrency sensitivity (flagged, not concluded).** With the same counter bytes,
seed and revision, one run under six concurrent scoring workers reported
`ctl-constant-key props=0/200`, `ctl-naive-join props=0/200`, `ctl-repr-key props=0/200`
(`receipts/frozen-base.txt`), where an unloaded run of the same command reports `100/200`, `140/200`,
`140/200` (`receipts/frozen-base-quiet.txt`). I could not reproduce it under a controlled 32-process
CPU load (`drivers/loadprobe.py`: `props=100/200`, 425 runs, no timeouts), so the mechanism is not
established; what is established is that the counter prints no control-level diagnostic, and that a
control which fails to execute is counted as rejected.

## 7. Honest limits

- Kill rate is measured against **this** counter (`d4588d4b`) and **this** candidate
  (`3a658326`). The candidate was revised once mid-run (v1 → v2, `frozenset` removed); verdicts were
  identical on both. If ExecKey revises it again, these verdicts apply to the hash above only.
- 37 mutants cover the 14 clauses named in the tasking, with two or three mutants where a clause has
  two directions. Not covered by a dedicated mutant: header-value type check (`a: 1`), `uri`
  missing/not-a-string, `request_headers` not an object, input not JSON. Those paths are covered by
  the counter's own `REFUSALS` and by the differential corpus, but I did not mutate them.
- The differential corpus is mine, not the round's. It establishes that each survivor is a real
  semantic divergence; it does not establish that any particular new case *should* be added, only
  that the current case set and property alphabet cannot reach the clause.
- The differential harness calls the candidate's `main()` in-process with stdio patched rather than
  spawning a process per input; it reproduces the CLI contract but is not the CLI. Every verdict in
  §3 comes from the CLI path, not from the harness.
- I did not modify the candidate, the counter, the contract or the case set. I did not judge whether
  C2 should pass; a surviving mutant is a coverage finding, not permission to change the contract.
- `mutants/`, `receipts/` and `drivers/` in my wave directory are the only things I wrote, plus this
  file. Scratch `/fast/scratch/hyaku/kake-r89/MutKey/` was deleted after the receipts were copied;
  no `/tmp` path is cited.

## 8. Reproduction

```
# counter mirror (committed bytes) + case/control copies, then per mutant:
git init <repo> && cp mutants/<id>.py <repo>/scripts/cache_key.py && git -C <repo> add -A \
  && git -C <repo> commit -m <id>
python3 -B counter-live/c89_key.py --root <repo> --revision HEAD \
  --candidate scripts/cache_key.py --work /abs/work/<id>
# driver that does this for all 37 plus the reference, 6 in parallel:
python3 -B drivers/score_all.py counter-live live      # → receipts/live/score.json, 27/37 killed
python3 -B drivers/differential.py                     # → receipts/diff/diff.json, 544 inputs
python3 -B drivers/matrix.py                           # → receipts/matrix.tsv
```

Tooling: none installed or upgraded — `python3` 3.14.8 and `git` were sufficient; no `pacman`, no
`uv`, no `npx`, no network GET.
