# ExecMutationTip — R90-B closure: mutation score of the tip conformance gate

VERDICT: R90-B closed — the tip gate `scripts/cache_key_conformance.py` @ `f4fff130` scored
34 single-point mutants against the frozen round-90 counter: 20 killed, 14 survived, control
`met=true`; receipt `.ufo/waves/round-91/integration/mutation-tip.txt` passes the frozen
`c91_defects.py` item-B predicate (N=34 ≥ 20, K=20 ≥ 18, S=14 = N−K).

## 1. What was measured

- Tip: `git -C LANE rev-parse master` → `f4fff130a52ae6de49af5de7d568d2ee320ebfb0`.
- Gate blob: `git show f4fff13:scripts/cache_key_conformance.py | sha256sum` →
  `d7bca38ec146727087a2d2e37a64c5154214e2dd069553fb5594372d2064b65e` (working tree equal).
- Counter digest check: `sha256sum .ufo/waves/round-90/c90_gate.py` →
  `703b00580391d8546ce238099d8fdba46358797af307cad02169c3828d70ccfa` — byte-equal to the
  round-90 spot-check pin, i.e. the scoring instrument was frozen bytes.
- Control (no mutant): `python3 -B LANE/.ufo/waves/round-90/c90_gate.py --root $S/fx
  --revision HEAD --work $S/work --seed 90` on a shared scratch clone of LANE detached at the
  tip → `C2v90 revision=f4fff13… positives=4/4 negatives_refused=57/57 false_admits=0
  errors=0 anti_table=ok population=ok seed=90 met=true` (rc 0). Receipt:
  `w1/ExecMutationTip/control.txt`. This is the `met=true` in the receipt's first line.
- Fixture discipline: `git clone -q --shared LANE $S/fxN`, `--detach` at the tip,
  `rev-parse --show-toplevel` asserted equal to the clone before every commit; each mutant is
  exactly one commit on top of `f4fff13` (fixture heads and mutated-blob sha256 recorded per
  mutant in `w1/ExecMutationTip/results.jsonl`). Scored with the seat's canonical argv
  (`--seed 90`, counter default `--jobs 6`), 3 clones in parallel; no LANE git command was run.

## 2. Battery and result

34 mutants (`M01`–`M34`), every one a single-point edit of the pristine tip bytes, anchor
uniqueness asserted and `compile()` checked before commit (driver:
`w1/ExecMutationTip/driver.py`; full per-mutant counter line 1 + catching subject:
`w1/ExecMutationTip/results.jsonl`).

Killed = counter line 1 `met=false`; survived = `met=true`. Zero counter errors, zero
timeouts; 842 s total mutant wall time.

| Mutant | Change | Verdict | Caught by / mechanism |
|---|---|---|---|
| M01 | delete hand case `layout/absent` | survived | generated population subsumes absent-name coverage (90/120 seed-90 cases) |
| M02 | delete clause group `members` (25 cases) | killed | false admits `adv-wildcard-ok`, `M19-wildcard-not-refused`, `M20-wildcard-anywhere-refused`, `M06-member-trim-wider-than-ows` (seed-90 gen draws 0 wildcard members) |
| M03 | delete clause group `refusals` (14 cases) | killed | false admits `adv-missing-headers` (its own docstring predicts this), `adv-bad-json` |
| M04 | delete `refusals/headers-missing` | survived | sibling envelope cases (`headers-missing-vary/-list/-null`) catch the same stub |
| M05 | judge accepts key by substring containment | killed | 4/4 positives not admitted (json.dumps escapes lone surrogates, so raw-byte containment fails `uri-lone-surrogate`) |
| M06 | judge drops stdout-emptiness on refusals | survived | no pinned negative prints to stdout while refusing |
| M07 | judge drops `invalid_input:` stderr prefix | survived | no pinned negative refuses with non-conforming stderr |
| M08 | judge accepts exit 0 on refusals | killed | false admit `M34-refusal-exits-zero` |
| M09 | deny_events drop `os.system` | survived | no pinned subject spawns a process |
| M10 | deny_events drop `gc.get_objects` | survived | no pinned subject reads hook state via gc |
| M11 | deny_mods drop `_posixsubprocess` | survived | the a4814f58 fork_exec fix has no frozen subject |
| M12 | sandbox import branch dropped | survived | masked: `neg-oracle-path-import` dies at the *open* of the borrowed `c89_key.py` (probe receipt `probe-m12-m24.txt`) |
| M13 | reference: `sorted(members)` → `members` | killed | self-check abort (exit 2 → all 61 subjects error) |
| M14 | reference: separators escaped before `%` (replace-chain) | killed | self-check abort (`value-each-sep` double-escapes) |
| M15 | reference: `_trim` → `str.strip()` | killed | self-check abort (`vt-kept`, `lf-not-ows`) |
| M16 | reference: duplicate-vary-member refusal dropped | killed | self-check abort (`dup-member-case/-exact`) |
| M17 | reference: wildcard refusal dropped | killed | self-check abort (`wildcard`, `wildcard-ows/-listed`) |
| M18 | `--generated` default 120 → 0 | survived | ctl-table is refused by the sandbox open-deny (its absolute read), not by generated; all other negatives fall to hand cases |
| M19 | `met` ignores generated tally | survived | no pinned subject is caught only by generated cases at seed 90 |
| M20 | `met` ignores violation flag | survived | equivalent mutant: judge already fails every violating case; the flag only labels `sandbox=ok\|violation` |
| M21 | backdoor admitting a candidate whose source carries a pinned subject digest | killed | counter anti-table: `sha:.ufo/waves/round-89/w1/ExecControls/adv-bad-json.py` |
| M22 | judge accepts an extra output key (`len(doc) < 1`) | survived | no pinned negative emits extra JSON members |
| M23 | sandbox strict-UTF-8 stdin reconfigure dropped | survived | advisory `utf8-required` is never scored, so the a4814f58 stdin fix is invisible |
| M24 | sandbox open branch dropped | survived | masked: `neg-exec-source` dies at `import subprocess` inside the exec'd round-89 counter source (stderr captured in `probe-m12-m24.txt`) |
| M25 | judge rejects trailing-newline stdout | killed | 4/4 positives not admitted (all four positives end stdout with `\n`) |
| M26 | sandbox stdlib roots emptied | killed | 4/4 positives not admitted (candidates die opening stdlib files) |
| M27 | reference: name lowering dropped | killed | self-check abort (`lookup-ci`) |
| M28 | reference: member OWS trim dropped | killed | self-check abort (worked example 3) |
| M29 | reference: absent marker emits empty | killed | self-check abort (worked example 7) |
| M30 | reference: dup-header refusal dropped | killed | self-check abort (`dup-header-ci`) |
| M31 | reference: CR/LF value refusal dropped | killed | self-check abort (`cr-only`) |
| M32 | reference: uri type check dropped | killed | self-check abort (`uri-number` crashes `_esc`) |
| M33 | reference: vary type check dropped | killed | self-check abort (`vary-number` crashes `split`) |
| M34 | reference: request_headers type check dropped | killed | self-check abort (`headers-list` crashes `items`) |

N=34, K=20, S=14. Kill-mechanism breakdown: 13 self-check aborts, 3 behavioral false-admits
(M02, M03, M08), 3 positives-not-admitted (M05, M25, M26), 1 anti-table (M21).

## 3. Survivors — missing case classes for round 92

1. M01/M04 — the counter cannot see hand-case *count* regressions; its generated population
   subsumes most single-clause hand coverage. Not a gate defect; a measurement gap.
2. M06 — no pinned candidate refuses while writing to stdout. Case class: a refusal-with-stdout
   stub.
3. M07 — no pinned candidate refuses with non-`invalid_input:` stderr. Case class: an
   arbitrary-stderr refuser (the refusal output protocol is unguarded).
4. M09 — no pinned subject exercises process spawn (`os.system` needs only `os`, which is
   import-allowed). Case class: an `os.system`/`fork_exec` escape probe.
5. M10 — no pinned subject touches gc-based hook-state rebinding (round-90 ExecSandbox
   c13-class). Case class: a gc probe.
6. M11 + M23 — the a4814f58 hardening (fork_exec deny, strict-UTF-8 stdin) has **no frozen
   subject**: R90-B's premise confirmed by measurement — the frozen counter cannot score that
   hardening. Case classes: a `_posixsubprocess.fork_exec` delegator; a scored non-UTF-8 input
   case (needs R90-1's contract ruling first, else it stays advisory).
7. M12/M24 — the import and open sandbox branches mask each other (evidence in
   `probe-m12-m24.txt`); each single-point drop is unscorable, and the compound mutant that
   flips both subjects is two-point, outside this battery's single-point discipline.
8. M18/M19 — the frozen counter never passes `--generated` and owns no subject that the
   generated population alone catches at seed 90 (`ctl-table` is pre-refused by the sandbox
   open-deny; seed-90 gen draws 0 wildcard members). A shipped gate with its generated
   population silently off reads `met=true` 61/61 times. Counter-side fix candidates: pass
   `--generated 120` explicitly, or pin a wildcard-only negative (gen coverage is seed-luck).
9. M20 — equivalent by construction (judge already fails violating cases); recorded, not a
   defect.
10. M22 — no pinned negative emits extra output members. Case class: an `{"key":…,"extra":…}`
    stub.

## 4. Defects found in the round's own instruments (findings, not edits)

- **F1 (seat-menu defect):** the seat's mutant menu names "drop the anti-table check", but the
  gate carries no anti-table check — `grep -nE 'anti|sha256|digest|hexdigest'
  scripts/cache_key_conformance.py` is empty; the anti-table lives in the frozen counter
  (`c90_gate.py`), which I must not mutate. The menu item is inapplicable as written; M21
  instead implements the attack the check exists for (pinned-digest backdoor) and is killed by
  the counter's anti-table.
- **F2 (counter blind spot):** with `--generated` left at the gate's default, the counter's
  mutation score overstates generated-population protection — M18/M19 show the score is
  identical with the generated population effectively off (see §3.8).
- **F3 (kill skew):** 13/20 kills are self-check aborts (reference tamper → exit 2 → all 61
  subjects error), 3 come from positives failing. A successor counter could report
  crash-kills separately from verdict-flip kills so a K of 20 is not read as 20 behavioral
  catches (the behavioral margin is 7).
- **F4 (seed dependence):** verdicts are seed-90 facts. The M02 kill exists only because
  seed-90 generated cases draw zero wildcard members while four hand cases carry the whole
  wildcard clause; a seed that draws wildcards would make M02 a survivor.

## 5. Limits and environment

- One seed (90 — the seat's frozen scoring argv), counter defaults otherwise; each verdict is
  a full 61-subject counter reading, not a spot check.
- Python 3.14.8, 32-way host, 3 fixture clones in parallel; mutants scored in 842 s.
- No tools installed or upgraded (nothing needed); pacman untouched.
- Scratch `/fast/scratch/hyaku/kake-r91/ExecMutationTip/` deleted after copying receipts; no
  `/tmp` writes; no fleet-root or sibling writes; no commits outside scratch fixtures.

## 6. Evidence inventory (all under this wave directory)

- `integration/mutation-tip.txt` — the item-B receipt (validated against the frozen
  `parse_receipt` + `MUTANT_RE`: digest match, 34 ≥ 34 distinct `M<nn>` lines).
- `w1/ExecMutationTip/driver.py` — battery definitions (anchors, assertions, fixture guard).
- `w1/ExecMutationTip/results.jsonl` — per-mutant: rc, met, fixture head, mutated-blob sha256,
  false_admits, errors, positives_not_admitted, anti_table_hits, full counter line 1.
- `w1/ExecMutationTip/control.txt` — the control reading (met=true, 4/4 + 57/57).
- `w1/ExecMutationTip/run.log`, `w1/ExecMutationTip/probe-m12-m24.txt` — run stream and the
  M12/M24 masking evidence.
