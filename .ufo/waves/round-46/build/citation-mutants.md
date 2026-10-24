# Citation-lint mutation findings

## Result
**FAIL / dependency-blocked:** none of the five named mutants was executed, so no mutant can be classified as killed or survived. The required implementation `scripts/citation_lint.py` was absent when inspected and the requested entrypoint could not be opened. Per assignment, no replacement implementation or guessed mutant behavior was created.

## Decisive evidence
Command, from `/home/vgpnk/Projects/shokunin/kake-shokunin`:

```text
python3 -B scripts/citation_lint.py --selftest
```

Verbatim output:

```text
python3: can't open file '/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citation_lint.py': [Errno 2] No such file or directory
```

Exit code: `2`.

The static file read also returned verbatim: `Path '/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citation_lint.py' not found.` A recursive filename lookup returned: `No files found matching pattern` for `**/citation_lint.py`.

## Mutant outcomes
| Mutant | Outcome | Evidence |
|---|---|---|
| Drop git-resolution check | NOT RUN — dependency absent | The selftest entrypoint could not be opened; no mutant output exists. |
| Drop citation-context filter | NOT RUN — dependency absent | The selftest entrypoint could not be opened; no mutant output exists. |
| Drop sha256 exclusion | NOT RUN — dependency absent | The selftest entrypoint could not be opened; no mutant output exists. |
| Always exit 0 | NOT RUN — dependency absent | The selftest entrypoint could not be opened; no mutant output exists. |
| Flag every token | NOT RUN — dependency absent | The selftest entrypoint could not be opened; no mutant output exists. |

No source copy or mutants were made; scratch directory `/fast/scratch/hyaku/kake-r46/ExecCitationSelftest/` is empty. No tools were installed.
