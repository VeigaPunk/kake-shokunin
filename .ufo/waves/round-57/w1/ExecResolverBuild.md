# ExecResolverBuild

SCRIPT PATH:
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-57/w1/ExecResolverBuild.files/id_resolver.py`
(python3, stdlib only; 1 file, 722 lines including the embedded 33-case selftest). It is **not** placed at
`scripts/id_resolver.py` in the lane — seat bound is this report plus `<report name>.files/`; the measured-revision
commit that the gate scored carries it at `scripts/id_resolver.py` inside the scratch clone.

SELFTEST: 33/33 — `python3 -B id_resolver.py --selftest` exits 0 in ~0.11 s, last line `selftest: 33/33`
(G2 in the gate re-ran it in a clean clone of the measured revision: `selftest: 33/33`). Coverage, mapped to the
assigned list: rows at 0/2/3 leading spaces; 4 spaces treated as code (id dangling, exit 1); CRLF registry;
id inside a markdown table; range `S011–S013` cites only S011 and S013 (ids_cited=2); decoys `S12`, `AS500`,
`S500x`, `s101` (each ids_cited=0); 4-digit `S0300`; id held by two siblings (owners `alpha-shokunin,beta-shokunin`);
id held by none (unowned=1); lane excluded from owners by realpath (symlinked sibling + `--revision` where only the
sibling's HEAD registry holds the id); sibling without `corpus/SOURCES.md`; unresolved revision → 2; missing registry
→ 2; no knowledge files → 2; `--revision` reads old blobs not the working tree (two commits, plus short-rev and
working-tree checks); usage errors → 64 (`--root` with no value, unknown option, no `--root`); duplicate citation
counted once; citing-path ordering stable; exact DANGLING and summary lines; gate-shaped fixture totals
(6,2,4,3,1); exit 0 clean / exit 1 dangling; url-match present, absent, and one-of-two-owners; owners sorted;
nested knowledge path; registry section ends at the next heading. All git fixtures are `mktemp -d` repos with
`git rev-parse --show-toplevel` verified equal to the fixture root and `-c user.name=selftest -c user.email=selftest@local
-c commit.gpgsign=false` on commit; every fixture dir is removed in a `finally`.

GATE RUN:
Scratch clone: `git clone -q --no-checkout <lane> $D`, `git -C $D checkout -q 28fa0b23e699303725aba2727094531f5e44494d`
(toplevel verified `$D`), tool copied to `$D/scripts/id_resolver.py`, committed as
`e7ff23e8c38572c75a3b8234255d92716cb2786b`; then
`python3 -B <lane>/.ufo/waves/round-57/c57_idresolver_gate.py --root $D --revision e7ff23e8c38572c75a3b8234255d92716cb2786b --fleet /home/vgpnk/Projects/shokunin`

```
C2 id-resolver 5/5 met=True  (met: gate_conditions_passed == 5 of 5)
  G1_tool_present PASS
  G2_selftest PASS
    - selftest: 33/33
  G3_fixture PASS
    - exit=1 dangling=['S0300', 'S101', 'S200', 'S777'] summary=(6, 2, 4, 3, 1); clean exit=0 summary=(2, 2, 0, 0, 0)
  G4_red_before PASS
    - exit=1 dangling=['S367', 'S372', 'S373', 'S390', 'S409'] owners={'S367': 'kake-shokunin,kotodama-shokunin', 'S372': 'kake-shokunin,kotodama-shokunin', 'S373': 'kake-shokunin,kotodama-shokunin', 'S390': 'kake-shokunin,kotodama-shokunin', 'S409': 'kake-shokunin,kotodama-shokunin'}
  G5_green PASS
    - exit=0 summary=(104, 104, 0, 0, 0)
  revision: e7ff23e8c38572c75a3b8234255d92716cb2786b
```
Gate exit 0, wall 3.06 s. Independent direct runs of the same tool against the real lane repo
(`--root <lane> --fleet /home/vgpnk/Projects/shokunin`): RED `3994101` → exit 1,
`ids_cited=99 ids_resolved=94 dangling=5 owned_elsewhere=5 unowned=0`, the five ids each
`owners=kotodama-shokunin url-match=-`; green `28fa0b2` → exit 0, `ids_cited=104 ids_resolved=104 dangling=0
owned_elsewhere=0 unowned=0`.

DESIGN NOTES (parser decisions):
- Cited ids: `(?<![A-Za-z0-9_])S\d{3,}(?![A-Za-z0-9_])` — an explicit ASCII word boundary rather than `\b`, so the
  result does not depend on Unicode word semantics. This is load-bearing on real data: an unguarded scan also matches
  `S404` inside `S404_SHA256` in `corpus/knowledge/free-read-verbs.md:195` and would report a false dangling id.
- Registry: `## Registry` opens the section, the next `^#{1,2}\s` heading closes it; rows match
  `^ {0,3}\|\s*([^|]*?)\s*\|(.*)$`, and the first cell must fullmatch `S\d{3,}` (header and separator rows fail
  naturally). 4+ leading spaces never match → indented code ignored. `splitlines()` + `rstrip("\r")` makes CRLF
  registries identical to LF ones.
- `--revision`: `git rev-parse --verify <rev>^{commit}` first; knowledge paths come from `git ls-tree -r --name-only`
  filtered to `corpus/knowledge/**/*.md`, each body from `git show <rev>:<path>`; the lane registry is also read from
  `git show <rev>:corpus/SOURCES.md`. This is required by G4/G5: at `3994101` the registry lacked the five ids, and a
  working-tree registry read would have resolved them and failed red-before.
- Siblings: every `<fleet>/*-shokunin/` directory (symlinks followed) whose realpath differs from the lane realpath;
  registry via `git show HEAD:corpus/SOURCES.md` when the sibling is a git repo (falling back to the working-tree file
  if HEAD has no such blob), else the file. A sibling with no registry owns nothing — that is not an error; only the
  lane's missing registry is exit 2. Sibling registries are read lazily, only when at least one id is dangling.
- `url-match`: URLs are taken from the row's source (second) cell and matched as substrings against the citing bodies.
  Cell-2-only is deliberate — 7 rows in the real lane registry carry URLs in other cells, which are not the row's
  source URL.
- Output determinism: ids, citing paths, owners and url-match all sorted; duplicate citations collapse to one path;
  fields comma-joined with no spaces (the gate's `DANGLE` regex uses `\S+`). Status mapping: dangling==0 → 0,
  dangling>0 → 1, unevaluable → 2 (message on stderr), argparse `SystemExit` → 64 (`--help` → 0). `--selftest` needs
  no `--root`, so the gate's bare `--selftest` call parses.

LIMITS:
- Gate G4 passes the real fleet while `--root` is the `/tmp` clone; under the contract's realpath rule the real
  `kake-shokunin` is then a sibling of the clone, so owners print `kake-shokunin,kotodama-shokunin` (the gate asserts
  only that kotodama is among the owners). With `--root` pointing at the real lane the lane is excluded and owners
  print `kotodama-shokunin` alone — both verified.
- `url-match` only sees URLs in the source cell; URLs quoted from anchor/used-by cells will not match. For the five RED
  ids it is `-` because the citing files quote none of kotodama's row URLs.
- Siblings are read at HEAD, not their working tree (contract); a sibling with uncommitted registry rows is invisible.
- Knowledge scan is `*.md` only, per contract; non-markdown knowledge (e.g. the `.json` sidecars in that directory) is
  not scanned.
- No network access, no writes outside `mktemp -d` fixtures, no lane/jj/git-index mutation, no tool installs
  (nothing needed; system python3 + git sufficed). Scratch clone `$D` left at `/tmp/tmp.sUkvfyxUxA` (ephemeral).

VERDICT: C2 candidate built and gate-scored 5/5 (G1–G5 PASS, selftest 33/33, red 5 ids owned by kotodama, green 104/104/0).
