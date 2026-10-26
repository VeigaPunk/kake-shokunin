# CriticResolverCheat

Correctness attack on the shipped tool, not the gate: `scripts/id_resolver.py` at lane revision
`4b8c73050470ada9e6583f3b12d659d1bed6a17f`, blob sha256 `2bee5a8f…f3bdfba5` (the working tree
file hashes identically). "Expected" = frozen contract §C2 + the counter docstring's CLI rule
(`.ufo/waves/round-57/c57_idresolver_gate.py:38-72`) + the canonical registry census
(`kimi-shokunin/skills/shokunin/protocol/CORPUS.md` §Census:
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`). Fixtures: `mktemp -d` fleets only; no
lane/fleet/index writes, no git mutation outside throwaway repos, no pacman, no installs.
Baseline: `--selftest` 33/33 exit 0; over the measured revision with the real fleet
`ids_cited=106 ids_resolved=106 dangling=0 …` exit 0. Every case below is `confirmed by running`.

## CASES:

| # | minimal input | expected per rule | tool output | at fault |
|---|---|---|---|---|
| C01 | entry `Quoted as **S001** in bold.`, plain `S001` row | counted (rule: every token) | `ids_cited=1 ids_resolved=1`, exit 0 | none |
| C02 | registry first cell `**S001**` (bold) | not a row (census needs `S###` then spaces+`|`) | `DANGLING S001 … owners=-`, exit 1 | none; spec is silent on decorated cells |
| C03 | registry first cell `[S001](https://…)` (link) | not a row | `DANGLING S001`, exit 1 | none; a link-written row is inert (spec gap) |
| C04 | entry `Escaped: \S123 and \\S124.` | both counted | `ids_cited=2 dangling=2`, exit 1 | none |
| C05 | entry `<!-- S900 -->`, fenced `S901`, inline `` `S902` `` | all counted (contract: every token) | `ids_cited=3 dangling=3`, exit 1 | none; declared noise |
| C06 | entry `See S123. Then S124: done. Also (S125).` | S123,S124,S125 | S125 only dangling, exit 1 | none |
| C07 | entry `Spans S123-S125.` (and `S123–S125`) | endpoints only | `ids_cited=2`, exit 0; interior-only registry → 2 dangling, exit 1 | none |
| C08 | `corpus/SOURCES.md` = fenced block containing `## Registry` + `| S950 | … |`, then the real `## Registry`; entry cites `S950` | S950 is inside a fence, not a row → `DANGLING S950`, exit 1 | `ids_cited=1 ids_resolved=1 dangling=0`, **exit 0** | contract gap (D1) |
| C09 | fenced id row *inside* the real `## Registry` section | dangling, exit 1 | **exit 0**, resolved | contract gap (D1) |
| C10 | fenced `## Registry` after `## Paths` (section re-opens) | dangling, exit 1 | **exit 0**, resolved | contract gap (D1) |
| C11 | id cell `\|   S001   \|` | row (census tolerates padding) | resolved, exit 0 | none |
| C12 | id cell `\| S001 (preprint) \|` | not a row (census requires `S###`+spaces+`|`) | dangling, exit 1 | none |
| C13 | id cell `\| S001. \|` and `\| S002^1 \|` | not rows | 2 dangling, exit 1 | none |
| C14 | single-cell row `\| S002` (no closing pipe) | not a row by census and tool | `DANGLING S002`, exit 1 | tool right; the **gate reference** (`registry_rows`) accepts it → gate-side divergence |
| C15 | lane registry heading `## registry` (lowercase) | not the `## Registry` heading → all dangling | 1 `DANGLING`, exit 1 (not 2) | tool (D4: silent total misparse; reference would resolve) |
| C16 | lane heading `## Registry notes` | ambiguous: exact heading vs prefix | `DANGLING`, exit 1 | contract ambiguity (A2: reference resolves, tool does not) |
| C17 | lane heading `##  Registry` (two spaces) | `## Registry` with whitespace | resolved, exit 0 | tool right; reference rejects the section |
| C18 | sibling holds the id only in its `## Paths` table | owners `-` | `owners=-`, exit 1 | none |
| C19 | sibling has two rows for one id, two URLs; entry quotes the 2nd | owner + url-match | `owners=alpha-shokunin url-match=alpha-shokunin` | none |
| C20 | sibling repo (own `.git`), `corpus/SOURCES.md` only in the worktree, absent at HEAD | owners `-` (rule: `git show HEAD` when it is a repo) | **`owners=alpha-shokunin`** | tool (D2) |
| C21 | plain sibling (no `.git`, no registry file) inside a fleet-root git repo that has `corpus/SOURCES.md` | `-` ("a sibling without a registry owns nothing") | **`owners=sib-shokunin`** | tool (D3) |
| C22 | lane named `kake-shokunin` under the fleet; `--fleet` given / omitted / root with trailing `/` | lane never an owner | `owners=other-shokunin` in all three | none |
| C23 | sibling is a symlink to the lane | excluded by realpath | `owners=-`, exit 1 | none |
| C24 | clone of the lane at `kake-copy-shokunin`, lane read at an older rev | no rule covers it | `owners=kake-copy-shokunin` | contract ambiguity (A4) |
| C25 | `--fleet /nonexistent` | unevaluable (exit 2) or at least an error | exit 1, `owners=-`, empty stderr | tool (D5) |
| C26 | `--revision` with a symlinked `corpus/knowledge/linked.md` → outside file citing `S777` | the id is cited in `corpus/knowledge/**/*.md` | revision mode: `ids_cited=1 dangling=0` **exit 0**; worktree mode: `DANGLING S777` exit 1 | tool (D6) |
| C27 | CRLF registry | resolved | resolved, exit 0 | none |

C08 and C21 reproduce verbatim below (each `D`/`S` is `mktemp -d`, git toplevel verified,
`-c user.name=selftest -c user.email=selftest@local` inside the scratch). C20 shape: sibling
`S` = `mktemp -d` + `git init` + a committed `README` (no registry at HEAD) + an uncommitted
`corpus/SOURCES.md` holding the cited id, symlinked into a fleet as `alpha-shokunin`.

```sh
# C08 — exit 0 on a fenced phantom
D=$(mktemp -d); git -C "$D" init -q
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4b8c730:scripts/id_resolver.py > "$D/tool.py"
mkdir -p "$D/fleet/lane/corpus/knowledge"
printf '# SOURCES\n```\n## Registry\n| id | source |\n|---|---|\n| S950 | https://e.example/950 |\n```\n## Registry\n| id | source |\n|---|---|\n| S001 | https://e.example/1 |\n## Paths\n' > "$D/fleet/lane/corpus/SOURCES.md"
printf 'Cites S950.\n' > "$D/fleet/lane/corpus/knowledge/a.md"
python3 -B "$D/tool.py" --root "$D/fleet/lane" --fleet "$D/fleet"; echo EXIT=$?   # -> exit 0
# C21 — the fleet root is itself a repo; a plain sibling inherits its registry
D=$(mktemp -d); git -C "$D" init -q
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4b8c730:scripts/id_resolver.py > "$D/tool.py"
mkdir -p "$D/corpus"
printf '# SOURCES\n## Registry\n| id | source |\n|---|---|\n| S777 | https://fleet.example/777 |\n## Paths\n' > "$D/corpus/SOURCES.md"
git -C "$D" add -A && git -C "$D" -c user.name=selftest -c user.email=selftest@local -c commit.gpgsign=false commit -q -m seed
mkdir -p "$D/lane-shokunin/corpus/knowledge" "$D/sib-shokunin"
printf '# SOURCES\n## Registry\n| id | source |\n|---|---|\n| S001 | x |\n## Paths\n' > "$D/lane-shokunin/corpus/SOURCES.md"
printf 'Cites S777.\n' > "$D/lane-shokunin/corpus/knowledge/a.md"
python3 -B "$D/tool.py" --root "$D/lane-shokunin" --fleet "$D"   # -> owners=sib-shokunin
```

## TOOL DEFECTS:
- **D1 fenced registry rows resolve ids** (`parse_registry`, `scripts/id_resolver.py:77-104`;
  no fence tracking, `REGISTRY_HEADING_RE` matches a `## Registry` line inside a fence).
  `confirmed by running` (C08-C10): exit 0 where the markdown tree has a dangling id. The
  canonical census and the round-57 guard grep are fence-blind too, so the *contract* must
  say which wins (A1); the tool is still the artifact that hands out `exit 0`.
- **D2 sibling `.git` fallback** (`sibling_registry`, lines 193-206): after `git show
  HEAD:corpus/SOURCES.md` fails it falls back to the worktree file, against the rule "read
  through `git show HEAD:…` when it is a git repo, else the file". `confirmed by running`
  (C20): `owners=alpha-shokunin` for a row that exists only in an uncommitted file.
- **D3 repo test is `rev-parse --show-toplevel`, not "has a `.git`"** (line 196).
  `confirmed by running` (C21): a sibling nested in an enclosing repository whose toplevel
  holds `corpus/SOURCES.md` inherits that registry. Latent but armed: `/home/vgpnk/Projects/
  shokunin` is itself a git repo, carries no `corpus/SOURCES.md` today, and one added file
  would make every plain-dir `*-shokunin` a phantom owner.
- **D4 a format change is silent, not unevaluable** (`parse_registry` + `evaluate`, 208-232):
  a registry whose heading is `## registry` or `## Registry notes` parses to zero rows and
  every cited id becomes `DANGLING`/`unowned` with exit 1 and no stderr. `confirmed by
  running` (C15, C16). "Registry absent" is exit 2; "registry present, zero rows parsed" is
  not distinguished.
- **D5 a missing fleet is silently empty** (`evaluate` line 216 default, `sibling_dirs`
  176-190 returns `[]` when the path is not a dir): `--fleet /nonexistent` gives
  `owners=- unowned=1` exit 1, no error. `confirmed by running` (C25). A lane copy run from
  outside its fleet (the C22 shape, wrong cwd) loses every owner without saying so.
- **D6 revision mode reads a symlinked entry as the link blob** (`knowledge_bodies` 138-160,
  `git show rev:rel` on mode 120000 returns the target path, not the target's text):
  `confirmed by running` (C26). Same tree, two answers — exit 0 under `--revision` (the mode
  G4/G5 use), exit 1 in worktree mode. Live precondition absent: `git ls-tree -r 4b8c730
  corpus/knowledge` shows no mode-120000 entries.

None of D1-D6 changes the measured run: over `4b8c730` the tool is 106/106, exit 0, and no
live registry in the 21 lanes exercises D1-D5 (`## Registry` exactly once at column 0 in all
21; zero odd id cells; zero fences inside a Registry section; no symlinks in `corpus/knowledge`).

## CONTRACT AMBIGUITIES:
- **A1 fences.** The frozen rule says "first cell of each table row … under `## Registry`"; a
  `## Registry` inside a fence is not a heading, but the canonical census (`CORPUS.md`
  §Census) and the round-57 guard grep both count col-0 fenced rows — so a lane can turn any
  dangling id green by pasting `| S9xx | https://… |` into a fenced sample under the heading,
  and nothing in C2's G3/G5 notices. The entry side has the mirror rule: "every token" counts
  ids in HTML comments and fenced samples (C05; none exist in the live corpus).
- **A2 heading form.** Three parsers, three answers: tool `^##\s+Registry\s*$` (C15 no, C17
  yes, C16 no), gate reference `line.lower().startswith("## registry")` (C15 yes, C17 no,
  C16 yes), canonical census has no section at all. C16 and C17 are opposite verdicts
  between tool and reference; the gate's fixtures only ever write the exact heading.
- **A3 "the census parser's rule"** (tool docstring line 15): the canonical census is
  column-0-only and needs `S###`+spaces+`|`, i.e. it matches the tool's cell rule but *not*
  its 0-3 indentation and *not* its `## Registry` section gate; the 0-3 form comes from the
  round-57 guard (`assimilation/guard-proof/commands.txt`). The docstring conflates two rules.
- **A4 sibling identity.** "other than the lane (by realpath)" does not exclude a clone or a
  second worktree of the lane named `*-shokunin` under the fleet (C24: `owners=kake-copy-shokunin`
  at `--revision <older>`). The rule needs an identity (remote URL or tree), or the wording
  must disclose that a same-project copy is reported as a sibling registry.
- **A5 exit taxonomy.** "Registry absent" is 2; zero parsed rows (D4) and an unusable
  `--fleet` (D5) are silent 1s. The contract lists only revision-unresolved / registry-absent
  / no-knowledge-file.
- **A6 gate-side, reported for cross-reference** (gate seat owns it): the reference accepts a
  single-cell row `| S002` (no closing pipe) that the canonical census and the tool both
  reject (C14). A tool that emitted the reference's answer there would be *wrong* by census
  yet pass G3; and a correct tool can be failed by a fixture of that shape.

## RECOMMENDED CHANGES:
1. Track ``` / ~~~ fences in `parse_registry` (ignore fenced lines *and* fenced headings),
   state the rule in the contract and in the gate's `registry_rows` in the same words, and
   add the C08-C10 shapes to the gate's G3 fixture classes.
2. Make `sibling_registry` require a `.git` at `os.path.join(path, ".git")` and drop the
   worktree fallback when it is a repo (mirror the reference exactly). Optionally require
   `rev-parse --show-toplevel` to equal the sibling dir.
3. In `knowledge_bodies`, detect mode-120000 blobs (`git ls-tree` already gives the mode) and
   either follow the target inside the same revision or exit 2 naming the path — never
   silently drop it.
4. Fail loud: exit 2 when `--fleet` is given and is not a directory; when the lane registry
   yields zero rows while the file has non-blank lines; when `## Registry` is absent. Add
   stderr text naming the file for each.
5. Pin one heading rule (recommend `^##\s+Registry\b` in tool, reference and contract) and
   add `## registry`, `##  Registry`, `## Registry notes` as G3 fixtures so the divergence
   cannot come back.
6. Add selftest cases for D1-D6 to the tool's own `_cases()` (fenced heading, fenced row,
   sibling with uncommitted registry, sibling inside an enclosing repo, symlinked entry in
   revision mode, missing `--fleet`). The suite is 33/33 today and tests none of them.
7. Freeze the exit taxonomy sentence (A5) and the sibling-identity sentence (A4) in the
   contract; both are currently filled in by the implementation.

VERDICT: no defect changes the measured C2 result (tool 106/106, exit 0, and no live lane hits
these shapes), but `scripts/id_resolver.py` at 4b8c730 prints exit 0 on fenced phantom registry
rows and claims sibling owners from an uncommitted registry, an enclosing repo's registry, or a
clone of the lane — six confirmed tool defects (D1-D6), all latent on today's fleet.
