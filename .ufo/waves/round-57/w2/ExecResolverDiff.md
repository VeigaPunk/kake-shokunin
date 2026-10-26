# ExecResolverDiff

Differential test of two independent implementations of the round-57 C2 rule. Tool A (shipped) is
`scripts/id_resolver.py`; tool B (wave-1 oracle) is `.ufo/waves/round-57/w1/ExecResolverAlt.files/alt_resolver.py`
(sha256 `137509b3599c…`, committed in `cddef5b`). A's blob at the build under attack
`4b8c73050470ada9e6583f3b12d659d1bed6a17f` is sha256 `2bee5a8fa08efb432d946465f361db169e6572a9cfe5697f6de3ffd6f3bdfba5`, byte-identical to
the working-tree file, so the code I read *is* the revision 4b8c7305 build. Rulings quote the CLI docstring
`.ufo/waves/round-57/c57_idresolver_gate.py:19-30` and are corroborated by running the gate's own reference
implementation (`c57_idresolver_gate.py:128-203`) on the same fixture; the gate/counter itself was **not** run
(that is the L1's measurement, not this seat's).

## GENERATOR:

`.ufo/waves/round-57/w2/ExecResolverDiff.files/gen_and_diff.py` (evidence: `results.json`, `run.log` beside it).

    python3 -B .ufo/waves/round-57/w2/ExecResolverDiff.files/gen_and_diff.py \
        --workdir $(mktemp -d) --count 44 --results <workdir>/results.json [--only NAME[,NAME]] [--gate-ref NAME|ALL]

Each fixture is a JSON spec (`build_spec`) materialised under `<workdir>/fixtures/<name>/fleet/`: a lane
`<lane>-shokunin` with `corpus/SOURCES.md` + `corpus/knowledge/**/*.md`, and 1-3 sibling `*-shokunin` dirs.
Randomised knobs: registry row indentation 0/2/3/4 (4 = code), CRLF lane and/or sibling registries, 4-digit ids
mixed with 3-digit ids, `S011–S013` en-dash ranges, ids adjacent to CJK (`来源是S501的`), an id inside a URL
(`https://example.test/S501/page`), an id inside a code fence, a duplicate citation across files, decoys
(`S12 AS500 S500x s101 S_777 1S888`), a sibling that is a git repo vs a plain dir vs a dir with no registry, a
`## Registry` heading with trailing text, `# H1` inside the registry section, a pipe-less registry row, a second
table after `## Paths`, a backtick-wrapped or period-terminated URL in a sibling row, a symlink alias of the
lane, a repo sibling whose HEAD lacks the registry, a fleet root that is itself a git repo, a missing `--fleet`,
the default fleet, and `--revision` over two-commit git fixtures. Git fixtures run `git init <dir>` inside the
mktemp tree, assert `rev-parse --show-toplevel` == that dir, and commit only with
`-c user.name=selftest -c user.email=selftest@local`. Both tools run with identical argv, cwd, `PYTHONHASHSEED=0`,
`LC_ALL=C.UTF-8`; stdout is CRLF-normalised and compared verbatim with the exit code (stderr recorded, not compared).

## RESULT:

72 fixtures (44 randomised `R00`–`R43` + 28 targeted `T01`–`T28`), 25 agree, **47 disagree**, 8 distinct causes.
No fixture produced a crash or an stderr-only difference. All 47 are reproducible from `results.json`.

| cause | fixtures | A vs B |
|---|---|---|
| 1 dangling-line order (numeric vs lexicographic) | T07, R00-R16, R18-R20, R22-R29, R31, R33, R35, R37-R39, R41-R43 (38) | order only; lines and summary equal |
| 2 repo sibling whose HEAD lacks the registry | T17 | owners differ |
| 3 registry row without a closing pipe | T18 | resolved/dangling differ, exit 1 vs 0 |
| 4 `# H1` inside `## Registry` | T19, R21, R36 | resolved/dangling differ, exit 1 vs 0 |
| 5 backtick-wrapped URL in a sibling row | T20 | url-match differs |
| 6 symlink alias of the lane inside the fleet | T21 | owners differ |
| 7 `--fleet` names a missing directory | T23 | exit 1 vs 2 |
| 8 fleet root is a git repo, plain sibling | T28 | owners differ |

Axes that **agreed** on every fixture built for them (A == B, exit and stdout): indentation 0/2/3/4 (T01-T04),
CRLF lane registry (T05), CRLF sibling registry (T06), ranges (T08), CJK-adjacent ids (T09), id inside a URL
(T10), id inside a code fence (T11), sibling as git repo (T12) and as plain dir (T13), `## Registry` with trailing
text (T14), second table after `## Paths` (T15), `--revision` over a git fixture (T16), default fleet (T22),
all-resolved exit 0 (T24), sibling without a registry (T25), stale sibling worktree vs HEAD (T26), trailing-period
URL (T27).

Real-lane runs (read-only, `--root . --fleet /home/vgpnk/Projects/shokunin`), **confirmed by running**: at
`4b8c7305…` both print identical stdout, exit 0, `ids_cited=106 ids_resolved=106 dangling=0`; at `3994101…` both
print identical stdout, exit 1, `ids_cited=99 ids_resolved=94 dangling=5 owned_elsewhere=5 unowned=0` with
`S367 S372 S373 S390 S409`, each `owners=kotodama-shokunin`; the working tree run is also identical
(`dangling=0`). So the eight divergences are latent on today's fleet, not active on the claim's revisions.

## DISAGREEMENTS:

**1. Dangling-line order.** T07 (`Cites S501 and S1000.`, alpha holds both). A: `DANGLING S1000 …` then
`DANGLING S501 …`; B: `DANGLING S501 …` then `DANGLING S1000 …`; both `ids_cited=2 ids_resolved=0 dangling=2
owned_elsewhere=2 unowned=0`. **Ruling: A right, on the gate's own comparator.** `id_resolver.py:223`
`sorted(set(cited) - set(registry))` is lexicographic; B sorts by `(int(s[1:]), s)` (`alt_resolver.py:205`),
numeric. The contract says "one line per dangling id, sorted by id" (`c57_idresolver_gate.py:26`) and its reference
emits `sorted(i)` (`:194`), so B deviates from the reference; the prose alone is ambiguous, because a human reads
`S501` as the smaller id. Operationally inert: the gate parses DANGLING lines into a dict and compares id sets
(`:205-217`), so C2 measures no order at all — see gap G3.

**2. Repo sibling whose HEAD lacks the registry but whose worktree has it.** T17: sibling `alpha-shokunin` is a
git repo (commit = `README.md` only); `corpus/SOURCES.md` with `S501` exists uncommitted on disk. A: `DANGLING S501
… owners=alpha-shokunin`, `owned_elsewhere=1`. B: `owners=- … owned_elsewhere=0`. Gate reference: `owners=-`.
**Ruling: B right.** Contract (`:24-25`): a sibling is "read through `git show HEAD:corpus/SOURCES.md` when the
directory has a `.git`, else the file; a sibling without a registry owns nothing" — A's fallback at
`id_resolver.py:198-199` re-reads the worktree after `git show` fails, so an uncommitted registry buys an owner.
Same rule as the tool's own `--revision` promise ("never the working tree", `:19-21`).

**3. Registry row without a closing pipe.** T18: lane registry rows `  | S101 | …` and `  | S501` (single cell);
knowledge cites both. A: `DANGLING S501 … unowned=1`, exit 1. B: `ids_cited=2 ids_resolved=2 dangling=0`, exit 0.
Gate reference: same as B. **Ruling: B right.** Contract (`:21-22`): "first cell of each table row … 0 to 3
leading spaces before the pipe" — a one-cell row still has a first cell; A's `ROW_RE` (`id_resolver.py:39`) demands
a second pipe, so the row is silently dropped and its id is reported dangling.

**4. `# H1` inside the `## Registry` section.** T19: rows `S101`, then `# Appendix`, then row `S501`; both cited.
A: `DANGLING S501`, exit 1. B: `dangling=0`, exit 0. Gate reference: **same as A** (it ends the section on
`# ` too, `:132-133`). **Ruling: unresolved by the contract text** — the prose says "up to the next `## ` heading"
(`:22`), which makes B right, while the gate's reference sides with A (`SECTION_END_RE = ^#{1,2}\s`,
`id_resolver.py:43`); recorded as gap G2. No real-fleet effect: the lane's only H1 is the file title before
`## Registry` (verified on `corpus/SOURCES.md`). Same cause: R21, R36.

**5. Backtick-wrapped URL in a sibling registry cell.** T20: sibling row source `` `https://a.example/501` ``,
citing file says "see https://a.example/501 here". A: `owners=alpha-shokunin url-match=alpha-shokunin`. B:
`url-match=-`. Gate reference: `url-match=alpha-shokunin` (its `URL_RE` excludes the backtick, `:75`).
**Ruling: A right.** B's `URL_RE` (`alt_resolver.py:35`) admits a backtick, so its token is
`https://a.example/501\`` and never occurs verbatim. Live exposure: kotodama 20, kaidoku 14, chousa 12, kotoba 10,
kama 10 backticked URLs in sibling registries (counted), so B would under-report `url-match` on real data.

**6. Symlink alias of the lane inside the fleet.** T21: lane is a git repo; `HEAD` registry holds `S900`, the
`--revision` registry does not; `fleet/other-shokunin -> lane`. A: `owners=-`, `unowned=1`. B:
`owners=other-shokunin`, `owned_elsewhere=1`. Gate reference: `owners=-`. **Ruling: A right.** Contract (`:24`)
says "whose realpath differs from the lane's"; A compares realpath (`id_resolver.py:180,187`), B compares abspath
(`alt_resolver.py:192`) and thus credits the lane's own HEAD registry to a phantom lane name.

**7. `--fleet` names a missing directory.** T23 (`--fleet …/no-such-fleet`). A: normal report, `DANGLING S501 …
owners=- unowned=1`, exit 1. B: empty stdout, exit 2. **Ruling: B safer, A defensible — contract gap G5.** The
docstring enumerates exit 2 as "(revision unresolved, registry absent, no knowledge file)" (`:30`), which does not
cover an unreadable fleet, so A's `if not os.path.isdir(fleet): return out` (`id_resolver.py:178`) is not
contradicted; but it silently prints `unowned` for every id when ownership is unknowable. The gate always passes a
real fleet, so C2 cannot catch it.

**8. Fleet root is itself a git repo; sibling is a plain dir with no registry.** T28: `fleet/corpus/SOURCES.md` at
the fleet root's HEAD holds `S501`; `fleet/alpha-shokunin` has no `.git` and no registry. A: `owners=alpha-shokunin`
(it reads the *fleet root's* HEAD registry as the sibling's). B and gate reference: `owners=-`. **Ruling: B right.**
`id_resolver.py:194` treats "git resolves a toplevel" (which climbs out of the sibling) as "the directory has a
`.git`", then `git show HEAD:corpus/SOURCES.md` resolves against the fleet root. B's
`os.path.exists(sib/.git)` (`alt_resolver.py:137`) is the documented test. C2's `read_siblings` uses the same
`.git`-existence test (`:175`), so the gate would flag A here.

## CONTRACT GAPS:

- **G1 `## Registry` with trailing text.** Contract (`:21-22`), A (`REGISTRY_HEADING_RE`, `id_resolver.py:42`) and B
  (`alt_resolver.py:32`) require the exact heading `## Registry`; the gate's reference accepts any heading starting
  `## registry` (`c57_idresolver_gate.py:133`), so `## Registry (162 rows)` registers rows for the reference and not
  for either tool. T14 shows A == B == "rows ignored"; a gate fixture with such a heading would fail G3 against a
  correct tool.
- **G2 Section end: `## ` vs `# `.** Prose says "up to the next `## ` heading" (`:22`); A ends on `#{1,2}`
  (`id_resolver.py:43`), B on `^##\s` (`alt_resolver.py:33`), the reference on `# `/`## ` (`:132-133`). Cause 4 above.
- **G3 "sorted by id" is unmeasured.** The gate parses DANGLING lines into a dict (`:205-217`), so the order
  divergence (cause 1, 38 fixtures) cannot fail C2 even though the docstring's own reference fixes lexicographic order.
- **G4 URL tokenisation.** The reference does no `rstrip` of `.,;:` (`:75`, `:194-199`); A and B both strip. T27
  (`https://a.example/501.` in a sibling row, bare URL in the citing file) gives A = B = `url-match=alpha-shokunin`,
  reference `url-match=-`. C2's `build_fixture` always writes `t — {url} |`, so the reference's over-inclusive token is
  currently unreachable; any future fixture with punctuation after a URL would fail a correct tool.
- **G5 Unreadable fleet is not an enumerated unevaluable case** (`:30`); see cause 7.
- **G6 "the directory has a `.git`"** is implemented as "git resolves a toplevel" in A (`id_resolver.py:194`) and as
  ".git exists here" in B (`alt_resolver.py:137`); the whole real fleet is 20 real repos with a HEAD registry, so this
  is invisible there, but it is the root of cause 8.
- **G7 stderr is unspecified.** A prefixes `id_resolver: unevaluable: …`; B prints `unevaluable: …`. Only exits are
  contractual, so this is harmless, but no document names the stderr contract.

VERDICT: 72 fixtures / 47 disagreements in 8 causes — shipped A right on 3 (order, backtick URL, symlink realpath), oracle B right on 3 (uncommitted sibling registry, pipe-less row, fleet-root repo read), 2 undecided by the contract (H1 section end, missing fleet); both tools are byte-identical on the real lane at `4b8c7305` (exit 0) and `3994101` (exit 1, the five kotodama ids), so every divergence is latent today but causes 2 and 8 are genuine sibling-ownership misreads.
