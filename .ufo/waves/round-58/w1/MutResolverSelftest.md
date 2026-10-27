# MutResolverSelftest
Mutation test of `scripts/id_resolver.py --selftest` (49 checks). Detector: `python3 -B <copy> --selftest`, exit 0 iff `selftest: 49/49`. Pristine bytes copied to `/fast/scratch/hyaku/kake-r58/MutResolverSelftest/` before any run; lane repo never mutated.
- pristine sha256 `25982446d2e647830269cfff0b4bebf7bf263dde57c4321d87eeb42f06461bee` (scratch copy identical); baseline run: exit 0, `selftest: 49/49` (0.13 s, TMPDIR in scratch).
- 25 mutants, one behavioral change each, applied by exact-once string replacement to independent copies; per-mutant sha256 prefix given below. 18 killed, 7 survived. Kill = non-zero exit with named FAIL lines; survivor = exit 0 `selftest: 49/49`.

## MUTANTS:
| id | function | mutation (old → new) | sha16 | verdict | first detector evidence |
|---|---|---|---|---|---|
| M01 | parse_registry | `inside = True` → `False` after Registry heading | 2b7a63d4aad05268 | KILLED | FAIL 01 status=1 (every cited id dangles) |
| M02 | parse_registry | ROW_RE `^ {0,3}` → `^ {0,4}` | a7795ac2dc0d6dcf | KILLED | FAIL 04 4-space row no longer treated as code |
| M03 | parse_registry | drop `rstrip(".,;:")` on registry URLs | 7e005ad33cb49e1c | KILLED | FAIL 46 url-match missed with trailing punctuation |
| M04 | parse_registry | `URL_RE.findall(...)` → `[:1]` (first URL per cell only) | ae2c65867636bc27 | SURVIVED | selftest: 49/49; probe below |
| M05 | parse_registry | heading regex `\s*$` → `.*$` (trailing text ok) | 732618e52e4f5e83 | KILLED | FAIL 36 `## Registry (legacy)` now registers |
| M06 | parse_registry | source cell `.split("|", 1)[0]` → `[-1]` | fa756430f67bb7ac | KILLED | FAIL 25 gate-shaped totals |
| M07 | parse_cited | citing paths `sorted(paths)` → `reverse=True` | f010ffebf80afdeb | KILLED | FAIL 23 citing-path order |
| M08 | parse_cited | ID_RE `\d{3,}` → `\d{2,}` | c332275c2c8fd2b4 | KILLED | FAIL 08 decoy S12 accepted |
| M09 | parse_cited | lookbehind `A-Za-z0-9_` → `A-Za-z0-9` | f7a71afb5d07031b | KILLED | FAIL 34 `_S777` accepted |
| M10 | knowledge_bodies | revision filter startswith `KNOWLEDGE_REL + "/"` → `KNOWLEDGE_REL` | 6ddc749f0ba39b27 | SURVIVED | selftest: 49/49; probe below |
| M11 | knowledge_bodies | worktree walk `.md` → `.markdown` | 762308465f935e98 | KILLED | FAIL 01 status=2 no knowledge file |
| M12 | knowledge_bodies | revision branch: drop `if not bodies: return None` | 8d16f13270e43601 | SURVIVED | selftest: 49/49; probe below |
| M13 | knowledge_bodies | worktree branch: `return None, "...empty"` → `return {}, None` | 510a115ccb4433fb | SURVIVED | selftest: 49/49; probe below |
| M14 | sibling_registry | `.git` probe `exists` → `isdir` | 600b77e03b72fa2a | SURVIVED | selftest: 49/49; probe below |
| M15 | sibling_registry | `HEAD:{REGISTRY_REL}` → `HEAD:{REGISTRY_REL}.bak` | dfde96e054e00c29 | KILLED | FAIL 39 sibling HEAD ownership lost |
| M16 | sibling_registry | repo branch `if os.path.exists(...)` → `if False` (worktree file preferred) | e24153b15f0e6f49 | KILLED | FAIL 39 dirty worktree became evidence |
| M17 | evaluate | dangling diff `cited - registry` → `registry - cited` | b1070e87c1b74704 | KILLED | FAIL 04/07 summaries inverted |
| M18 | evaluate | `Result(1 if dangling else 0)` → `0 if ... else 1` | 96f50a8e10d7b808 | KILLED | FAIL 01/02 exit status flipped |
| M19 | evaluate | summary `(owned, unowned)` → `(unowned, owned)` | 8d94f47c675307e0 | KILLED | FAIL 04 summary swap |
| M20 | evaluate | url-match `any(url in bodies[path] ...)` → `all(...)` | 2f1f52a811284d82 | KILLED | FAIL 45 match must scan every citing file |
| M21 | evaluate | owners `sorted(genexp)` → unsorted list | 04e8cb20b1e9d081 | SURVIVED | selftest: 49/49 (masked, see below) |
| M22 | evaluate | default fleet `os.path.dirname(root)` → `root` | c019c1ac5427f10a | SURVIVED | selftest: 49/49; probe below |
| M23 | render | drop `or '-'` on empty owners | 7db085313c509342 | KILLED | FAIL 24 `owners=` without placeholder |
| M24 | render | summary labels `owned_elsewhere/unowned` swapped | f3ba3ae7a9df4e06 | KILLED | FAIL 24 summary line mismatch |
| M25 | render | ` url-match=...` field dropped | 5287fa41535fdfd3 | KILLED | FAIL 24 DANGLING line missing field |

Per-function coverage: parse_registry 6 (1 survived), parse_cited 3 (0), knowledge_bodies 4 (3), sibling_registry 3 (1), evaluate 6 (2), render 3 (0).

## SURVIVORS:
Each survivor was re-verified on a minimal CLI fixture (pristine vs mutant output differs), except M21.
- M04 `parse_registry` — only the FIRST url of a registry source cell is kept. Probe: sibling cell `| S777 | t — https://a.example/777 also https://b.example/777 |`, lane cites S777 quoting the second URL. Pristine: `owners=alpha-shokunin url-match=alpha-shokunin`; mutant: `url-match=-`. No selftest case puts two URLs in one cell.
- M10 `knowledge_bodies` (revision branch) — path filter loses the `/` boundary, so a committed `corpus/knowledge-x/evil.md` counts as knowledge. Probe at a committed rev: pristine `ids_cited=1 ids_resolved=1` exit 0; mutant `DANGLING S777 ... ids_cited=2` exit 1.
- M12 `knowledge_bodies` (revision branch) — a revision whose tree has NO `corpus/knowledge/**/*.md` no longer exits 2. Probe (repo committing only the registry): pristine exit 2 `no knowledge file at <rev>`; mutant exit 0 `ids_cited=0 ...`. Only the worktree empty case is covered (check 19); the revision branch is not.
- M13 `knowledge_bodies` (worktree walk) — the walk-ends-empty branch is unreachable in the suite: check 19's fixture never creates `corpus/knowledge/`, so it exits via the `absent` branch, not the `empty` branch. Probe (dir exists, holds only `notes.txt`): pristine exit 2 `no knowledge file: corpus/knowledge/**/*.md empty`; mutant exit 0 `ids_cited=0`.
- M14 `sibling_registry` — `exists(.git)` → `isdir(.git)`: a sibling whose `.git` is a FILE (gitdir pointer / linked worktree) falls back to its uncommitted on-disk file. Probe: sibling `.git` file → real repo, S777 only at HEAD, worktree file lacks it. Pristine `owners=alpha-shokunin` (HEAD); mutant `owners=-` (on-disk). The docstring's "a worktree file is not committed evidence" rule has no test.
- M21 `evaluate` — removing the explicit `sorted(...)` on owners survives because `sibling_dirs` already iterates `sorted(os.listdir(fleet))`, so fixture owner order is sorted by construction. Checks 31/25 pass for the wrong reason; the selftest cannot falsify the sort. [INFERENCE from source, not probed: unobservable without refactoring sibling_dirs or mocking listdir.]
- M22 `evaluate` — the default fleet root (`--fleet` omitted) is never exercised: every selftest fixture passes `fleet=base`. Probe via CLI without `--fleet` (parent of lane holds alpha-shokunin owning S777): pristine `owners=alpha-shokunin owned_elsewhere=1`; mutant `owners=- unowned=1`.

## CASES TO ADD:
Selftest cases the C2 fix should add (each kills exactly one survivor above; all are plain fixture cases like the existing ones).
1. `case_revision_without_knowledge`: repo lane, commit registry only, `evaluate(root, revision=rev)` → status 2, `"knowledge" in error` (kills M12).
2. `case_knowledge_dir_without_markdown`: create `corpus/knowledge/notes.txt` (dir exists, no `.md`) → status 2, `"empty" in error` (kills M13).
3. `case_revision_knowledge_prefix_boundary`: commit `corpus/knowledge-x/x.md` citing a dangling id at a revision → it is NOT cited (kills M10).
4. `case_sibling_git_file_reads_head`: sibling dir whose `.git` is a file pointing at a real gitdir; S777 committed at HEAD, on-disk registry without it → `owners=[sibling]` (kills M14).
5. `case_url_match_second_url_in_cell`: sibling cell with two URLs, citation quotes the second → `url-match=[sibling]` (kills M04).
6. `case_default_fleet_is_parent`: call `main(["--root", lane])` with no `--fleet` where the parent dir holds the owning sibling → `owned_elsewhere=1` (kills M22).
7. M21 cannot be killed by a fixture-level case (order is guaranteed by `sibling_dirs`); either drop the redundant `sorted()` in `evaluate` or leave it as belt-and-braces with a comment — do not count check 31 as covering it.

Housekeeping: all fixtures and mutants lived under `/fast/scratch/hyaku/kake-r58/MutResolverSelftest/` (TMPDIR included); per-mutant copies were deleted after each run; restoration evidence — after the sweep the scratch pristine file re-hashed `25982446d2e64783…` (unchanged) and re-ran `selftest: 49/49` exit 0; lane file hash identical before and after. Scratch dir removed after this report was written. No git state (lane or fixture) was mutated beyond throwaway fixture repos inside scratch.

VERDICT: 25 mutants on id_resolver.py --selftest: 18 killed, 7 survived — the selftest is blind to multi-URL registry cells, revision-branch path-prefix and empty-knowledge handling, .git-file siblings, the owners sort (masked), and the default fleet root; six concrete cases listed for the C2 fix.
