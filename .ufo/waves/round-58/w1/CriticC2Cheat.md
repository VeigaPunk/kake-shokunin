# CriticC2Cheat

Round-58 w1 attack on C2's gate (`c58_resolver_cases.py`). Method: shared clone of the lane at base
0440485 under `/fast/scratch/hyaku/kake-r58/CriticC2Cheat/lane-c2`; each stub committed as `scripts/id_resolver.py`
with selftest identity; gate run with `--root <clone> --revision <stub commit> --work <scratch>/gatework`.
No tools installed (none needed). All tallies below are actual gate runs (receipt files kept in scratch, deleted at cleanup).

## CHEATS:

| stub (commit) | idea | tally | cases that would catch it |
| --- | --- | --- | --- |
| vA_orig (c60e5ed) | base tool + rule `int(sid[1:]) >= 900` forces dangling; F1 fixed with `git ls-tree -r -z --name-only` (NUL-raw); real 49-case selftest | 12/12 met=True | none |
| vB_orig (1f7a625) | base tool + literal mask `{"S900","S901","S950","S951","S952"}`; same `-z` F1 fix; real selftest | 12/12 met=True | none |
| vH2 (d3acbc3) | threshold rule + F1 "fix" that re-splits the `-z` stream by replacing NUL with `\n` (mishandles a literal newline inside a filename); canned `selftest: 49/49` | 12/12 met=True | none (see HOLES H1/H3) |
| vD (b99fd09) | argv-fingerprint oracle: emits canned per-fixture output keyed on `/k1/…/p5/` fragments of `--root`; `--selftest` prints 49/49 | 12/12 met=True | none (H4) |

Engine of the break: every K fixture uses an id >= S900 (S950, S951, S952, S900, S901) while every P fixture uses
ids < S900 (S001–S004), and the real lane at base cites nothing >= S900 (preflight grep: zero `S9xx`/`S1xxx` in
corpus/knowledge; P7 green with ids_cited=106). The two disclosed false-green defects (fence-blind registry D1, quoted
paths F1) are therefore reproducible by id-magnitude/id-literal masks plus a path-listing fix — no fence awareness is
implemented at all in vA/vB/vH2 (the base tool stays fence-blind; S950/S951/S952 remain parsed as rows, then force-masked).

Attempted variants that do NOT score 12/12 (kept as negative controls):

| stub (commit) | idea | tally | failing cases |
| --- | --- | --- | --- |
| vC (b7504f4) | F1 via `-c core.quotePath=false` + line parse, no mask | 8/12 | K1–K3 (no rule), K5 (`a"b.md` still C-quoted by git even with quotePath=false — verified: `ls-tree` emits `"corpus/knowledge/a\"b.md"`, fails the `.md` filter) |
| vE (cfd1cb7) | "DANGLING for any id appearing after a ``` line": stop parsing registry rows at the first fence line | 8/12 | K1 (S001's row is also after the first fence → both dangling), K4/K5 (F1 unfixed), P2 (S002 after a closed fence dropped) |
| vF (b094cf3) | strip everything from the first fence to EOF before parsing | 8/12 | same set as vE |
| vG (f1c8258) | `-z` but NUL→`\n` re-split only (no mask) | 9/12 | K1–K3 (no rule) |

## HOLES:

- H1 (vA/vH2): a genuine non-fenced registry row with id >= S900 would be reported dangling. The gate never registers
  an id >= S900, so the mask is invisible. Also: the lane's own real selftest does not catch it — `case_lane_excluded_by_realpath`
  uses S900 only at a revision where it is *genuinely* dangling, and no selftest case asserts a registered >=S900 row resolves
  (vA_orig/vB_orig pass 49/49 with the real suite).
- H2 (vB): the mask is a hard-coded 5-tuple copied from the gate's own fixture ids; any id choice in a future/rotated
  gate (e.g. K1 switched to S953) evades it.
- H3 (vH2/vG): a citation file whose name contains a literal newline is split mid-name by the NUL→`\n` re-split and
  dropped → false green. A correct NUL split (vA) or `core.quotePath=false` line parse (vC) has the same blind spot for
  newline names; only a true NUL-raw parse plus exact record handling is safe.
- H4 (vD): the gate names fixture lanes deterministically `k1..p5` under `tempfile.mkdtemp` parents; a stub can read its
  own `--root` and emit canned output per fixture, bypassing all semantics including P7 (canned 106/106). P6 likewise only
  checks the last `selftest: N/N` line and exit code: a hollow suite printing 49/49 passes identically to the real suite
  (vA2/vB2/vH2), and the real suite itself lacks ≥900-registered/rotated-id cases.
- Structural: K/P id-band separation above is the enabler of H1/H2; P7's "real lane green" cannot see the mask because the
  lane's ids are all < S900.

## PROPOSED CASES:

- KH1 (registered S900+ resolves): `SOURCES.md` = `# Sources\n\n## Registry\n\n` + `HDR` + `row("S900")` (non-fenced,
  0-space row, as `reg_ok` style); `corpus/knowledge/ok.md` = `Cites S900.\n`; run `--root <lane> --fleet <fleet>`.
  Expect exit 0 and `^ids_cited=1 ids_resolved=1 dangling=0 `. vA_orig/vH2 exit 1 with `DANGLING S900` → caught.
- KH2 (id rotation): copy K1's exact body but with S953: `registry("```\n## Registry\n\n" + HDR + row("S953") + "```\n\n" + reg_ok)`,
  knowledge `ok.md` = `Cites S001 and S953.\n`; run without revision. Expect exit 1, `^DANGLING S953 `, and NOT
  `^DANGLING S001 `. vB_orig exits 0 → caught.
- KH3 (newline filename at revision): git lane (`git_lane=True`) with `corpus/knowledge/ok.md` = `Cites S001.\n` and
  `corpus/knowledge/a\nb.md` = `Cites S902.\n`, registry `reg_ok`; run with `--revision <head>`. Expect exit 1 and
  `^DANGLING S902 cited-by=corpus/knowledge/a\nb\.md `. vH2/vG exit 0 → caught.
- KH4 (randomized fixture dir): run K1's exact content/args but with the lane folder named `probe-x7q2` instead of `k1`
  (same content, same expectations as K1). Expect exit 1 + `^DANGLING S950 `. vD's fingerprint misses → falls through to
  its P7 branch, exit 0 → caught. Generalizes: the gate should randomize fixture subdir names.
- Hardening note (not a fixture): P6 should verify the selftest is non-vacuous (e.g. require N == number of check
  functions actually executed, or run a probe lane through the tool's own suite and diff behavior), since the tally line
  alone is spoofable.

VERDICT: The gate passes 12/12 to stubs that never fix either disclosed defect — id-magnitude/literal masks plus a
NUL-raw ls-tree listing (vA_orig, vB_orig, vH2) and even to a canned argv-fingerprint oracle (vD); K/P id-band
separation, hollow P6, and deterministic fixture names are the exploitable weaknesses (cases KH1–KH4).
