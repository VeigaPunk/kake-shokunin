# Round 29 wave 1 — CriticC2CounterGameable (C2 counter gaming attack)

Seat: leaf critic, axis operability. Advisory input for the L1 and the non-author closure; no verdict.

## Result

Yes: the C2 counter can be satisfied by a wrong tool. Four of the five fake tools score 30/30, exit 0,
with all three constant gates rejected. The counter is correct about where it reads the tool from, the
digest pin and reason-tuple comparison. The gaps are in case isolation and in what a frozen public
30-case matrix can prove.

Counter under attack: `.ufo/waves/round-29/c2_matrix_count.py`, sha256 62732c86…fac2d273 (same bytes
in the working tree, at d18bbf3 and at HEAD e58b66c). Matrix sha256 75c08f64…dbac2e84a (equals the pin at line 28).

## Gaming attempts (lane counter, unmodified, `--root <sandbox clone> --revision <tag>`)

| Fake | Keyed on | Counter output | Gamed? |
|---|---|---|---|
| F1 `f1_dirname` b03519bf | case id: the working directory is `scratch/<stem>/<case id>` (line 53) | 30/30, exit 0, gates 7/0/7 rejected | yes |
| F2 `f2_content` cf7c1e74 | sha256 of the materialized file contents (independent of directory names) | 30/30, exit 0, gates rejected | yes |
| F3 `f3_order` 6201a1de | invocation order, ordinal kept in `$HOME`, which is the shared scratch directory (line 108) | 30/30, exit 0, gates rejected | yes |
| F4 `f4_wrong_generic` 6bd8a3b9 | no lookup: a regex scan over raw text, any element, host-only origin check, no entity decoding, single and unquoted attributes missed, findings carry `id/page/resolved` "WRONG", `pagesChecked` -7 | 30/30, exit 0, gates rejected | yes |
| F6 `f6_poison_constants` b68c2074 | F1, plus it plants `usercustomize.py` in `$HOME/.local/lib/python3.14/site-packages`. The constant gates later run with the same HOME. | 30/30, but gates 30/30/30, `constantGatesAllRejected` false, exit 1 | no false pass: it forces a false failure (the tool can sabotage the gates) |

F4 on 8 held-out probes whose expectations I took from the matrix `interface` text (lines 6-12)
[INFERENCE: my reading of that text, no reference tool exists]: 1/8 pass. It flags `<div href="/x">`,
`<a src="/x">`, `http://o.github.io/other/` (other scheme) and `https://o.github.io:8443/x` (other port).
It misses `&#47;x` (entity decoded), `'/x'` (single quotes) and `/x` (unquoted). The only probe it
passes is "first base element with href". The frozen matrix has no case covering any of the seven it fails.

## Properties checked

- The tool is read only from `git show <commit>:scripts/base_path_audit.py` (lines 39-42). A working-tree
  copy of F1 at tag `absent` (tool deleted in the commit) scored 0/30 with `toolPresent` false, exit 1.
  Base e58b66c also scored 0/30, exit 1. With `GIT_DIR` pointed at my clone and `--root` set to the lane,
  the result was `revision not found`, exit 2, so `GIT_*` stripping holds.
- The digest pin holds: a one-byte matrix edit in the clone gave `matrix digest mismatch`, exit 2. The pin
  sits inside the counter itself, and the counter and matrix both run from the working tree, not from
  `git show` at the declaration commit. Closure should confirm the counter sha 62732c86… before it trusts a run.
- Reason tuples are compared: constant-refuse passes 7/8 input cases and fails I5 (wrong reason code);
  constant-failed-empty passes 0/30 (empty findings are rejected). Only `reason/element/attribute/value`
  are compared (lines 62-72 and matrix line 14). `id`, `page`, `resolved`, `pagesChecked` and
  `referencesChecked` are never checked; F4 emits garbage in all of them and passes. D11 has two pages,
  but which page a finding is attributed to is never checked.
- The constant gates are close to vacuous. The condition is "each constant fails at least one case"
  (line 155). Any constant tool fails at least one case of a matrix that mixes exits 0, 1, 2 and 64, so
  this condition can only catch a broken counter. It cannot reject any adaptive tool.
- The tool runs unsandboxed as the operator user (no namespace and no read-only filesystem). Not tried,
  because it would mutate the lane: a tool could also rewrite files outside scratch. [INFERENCE]

## Hardened counter (sandbox only, not a proposal to edit the frozen counter)

`c2_matrix_count_hardened.py` (sha256 46303762…08cd4b) changes three things: each case runs in a random
`<token>/site` directory, each case gets a fresh HOME with `PYTHONNOUSERSITE=1`, and case order is
shuffled with SystemRandom. Diff in `runs/hardened.diff`. Results:

- F1: 0/30
- F3: 7/30
- F6: 0/30, gates 7/0/7 rejected
- F2: 30/30, exit 0 (still gamed)
- F4: 30/30, exit 0 (still gamed)
- absent: 0/30

## Impacted axes and smallest safe corrections

- Operability (C2 capability): 30/30 on this counter does not show that the tool implements the
  interface. The directory-name, order and gate-poisoning holes are fixable defects. Content lookup (F2)
  and a wrong generic tool (F4) are an inherent tradeoff of a frozen public matrix; no isolation fix stops them.
- Fixes in order of cost, without breaking the declared freeze:
  1. Closure reads the landed tool source and rejects embedded case tables, digests of case contents or
     case ids.
  2. Closure runs a held-out probe set it did not publish beforehand, such as my 8 probes in
     `probes.py`, together with check 1, and reports the result separately from the count.
  3. A future counter randomizes case directories, isolates HOME per case with `PYTHONNOUSERSITE=1`,
     shuffles case order, and compares `page`, `pagesChecked` and `referencesChecked`.

## Commands run (all with TMPDIR inside the sandbox; exit codes as observed)

- `git clone -q <lane> <sandbox>/clone` → 0. Then `python3 -B make_fakes.py` → 0, with no case-key
  collisions. Each fake was committed and tagged in the clone only.
- `python3 -B <lane>/.ufo/waves/round-29/c2_matrix_count.py --root <sandbox>/clone --revision <tag>`:
  F1, F2, F3 and F4 → 0; F6, absent and e58b66c → 1.
- `python3 -B probes.py <counter> <sandbox>/fakes/f4_wrong_generic.py` → 0 (1/8). A first run used a
  relative tool path, failed every probe with exit 2, and was discarded as a harness error.
- `python3 -B c2_matrix_count_hardened.py --root . --revision <tag>`: F2 and F4 → 0, the others → 1.
- `GIT_DIR=<clone>/.git … --root <lane>` → 2. Matrix tamper in the clone → 2; the matrix was restored
  with `git checkout` in the clone, sha back to 75c08f64….

Not verified: the real `scripts/base_path_audit.py`, which does not exist at HEAD; the lane-file-rewrite
attack (deliberately not run); and the probe expectations against any reference implementation.
No installs or updates.

Evidence (sandbox `/fast/scratch/hyaku/kake-r29/w1/CriticC2CounterGameable/`): `make_fakes.py`,
`fakes/*.py` (F1 923a839c, F2 f31baa1e, F3 0ec252bf, F4 72817c72, F6 a35d89d9), `probes.py`,
`c2_matrix_count_hardened.py`, `runs/*.json` (counter outputs), `runs/probes-f4.jsonl`, `runs/hardened.diff`,
and `clone/` (tags f1_dirname … absent).
