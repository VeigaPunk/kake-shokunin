# ExecGuardTool2

Claim C2 second independent implementation: `append_guard.py` at
`.ufo/waves/round-60/w1/ExecGuardTool2.files/append_guard.py` (stdlib only,
python3 >= 3.10, ~750 lines incl. selftest). Built blind — no coordination
with other seats.

## DESIGN:

- Reads: `git ls-tree -rz -t <commit>` per side (mode/oid/type per path, NUL
  framing) and `git cat-file blob` for committed bytes only; the worktree and
  index are never consulted. `--root` must satisfy `rev-parse --show-prefix`
  returning empty (bare repos pass; subdirs fail). `rev-parse --verify -q
  <rev>^{commit}` resolves both revisions; `merge-base --is-ancestor` gates
  exit 2. Every git call runs `git -C <root>` with the
  `git rev-parse --local-env-vars` set scrubbed (same list citing_set.py
  uses); `GIT_CONFIG_*`, `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` etc.
  cannot redirect the repository.
- Per-path rule (in-scope regular blobs at base only): missing or non-regular
  at revision (mode 120000/160000/tree) -> `deleted`; else byte-split on `\n`
  (the trailing empty element after a final newline is dropped — a separator
  artefact, the only reading under which K1 is an EOF append); B not an
  ordered subsequence of R -> `changed`; else the existential tag check.
- `untagged_insertion` is implemented existentially, per contract: a file is
  flagged iff NO embedding of B into R has every non-EOF run starting with a
  visibly-tagged line. Bitset DP over base lines consumed x open-run mode:
  mode 0 = no open run, 1 = open run whose first line was tagged, 2 = open
  run whose first line was untagged. Per revision line: continue an open run
  (keep mode), open a run from mode 0 (enter mode 1 iff the line carries a
  visible tag, else 2), or match a base line (modes 0 and 1 only — a mode-2
  run may never close before another match). Accept iff bit nB set in any
  mode at end — an open run of either tag state reaching EOF is the allowed
  trailing append; an empty base file trivially accepts. This is a single
  forward pass with O(nR * nB/word) big-int ops; reported line = first line
  of the earliest non-EOF run lacking a tag in the leftmost (earliest-match)
  embedding, which is guaranteed to exist when the DP rejects.
- Tag visibility on the *revision* bytes, three masking passes: (1) fenced
  code blocks — lines starting with <= 3 spaces then >= 3 backticks mask the
  whole fence region; (2) backtick code spans — runs of equal length pair
  CommonMark-style over unmasked bytes (unmatched runs are literal, spans may
  cross lines); (3) HTML comments `<!--` .. `-->` over unmasked bytes,
  file-wide state (a comment may open in base text and be closed by the
  run's own first line, exposing a later tag). A tag is visible iff its whole
  regex match sits outside all masks; regex is the literal
  `\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]` (month 13 counts —
  documented).
- Scope: `--scope` repeats; default `corpus/knowledge/**/*.md`. Custom glob
  translator — `**` crosses zero or more directories so
  `corpus/knowledge/sub/x.md` matches. Output: `<kind> <path>[:<line>]` lines
  sorted by path then `files=<n> findings=<k>`; `files` = in-scope files
  examined at base (contract leaves the field's referent open), `findings` =
  finding lines (one per flagged file). `--json` prints
  `{files, findings, items:[{kind,path,line}]}`. Exits 0/1/2/64; usage errors
  (missing args, unknown flags) exit 64 via an ArgumentParser subclass.

## SELFTEST:

`python3 -B append_guard.py --selftest` builds throwaway `git init` fixtures
under $TMPDIR (selftest identity via `-c user.name=selftest`, HOME+TMPDIR
redirected, `GIT_CONFIG_NOSYSTEM=1`, toplevel asserted before every commit,
tempdir removed in `finally`). 36 cases, asserts exit code AND finding
kind+path: all 22 contract K-cases plus E1 fenced-code tag -> untagged, E2
tag after leading text -> clean, E3 base-opened comment closed on the run's
first line -> clean, E4 empty base file -> clean (all-EOF-append), E5/E6
mixed tagged+untagged runs / tag-on-second-line -> untagged, E7 `--scope`
redirection, E8 identical revisions, E9 malformed-date tag accepted (literal
regex), E10 tagged first line + untagged body lines -> clean, E11 `--json`
shape, E12 `--root` subdirectory -> 2, E13 unresolvable revision -> 2, E14
unknown flag -> 64.

Result: `selftest: 36 passed, 0 failed, 36 cases` — full PASS lines for
K1-K22, E1-E14 (observed).

## REAL LANE:

Run on `/home/vgpnk/Projects/shokunin/kake-shokunin` (verbatim):

```
$ python3 -B append_guard.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --base fd6303ce5c14b3f892dec586297a942ab6e4193b --revision 97cdc122379711c2b02a8970752c8782da3ac81d
files=53 findings=0
(exit 0)
$ python3 -B append_guard.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --base 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 --revision 97cdc122379711c2b02a8970752c8782da3ac81d
files=46 findings=0
(exit 0)
```

The round-59 tagged in-file correction in
`corpus/knowledge/crawler-identity.md` (16-line run, first line
`  **[r59-correction 2026-10-27]** ...`) is accepted — K2's `**tag**`
bold-marker shape on the real corpus. R2-shape probe on a scratch
`--shared` clone detached at the measured revision with one byte of a base
line of `crawler-identity.md` flipped and committed:
`changed corpus/knowledge/crawler-identity.md` / `files=53 findings=1`,
exit 1 (expected R2 finding).

## LIMITS:

- `files=<n>` counts examined files (contract only fixes the field names).
- Reported `:<line>` is the first bad run under the leftmost embedding;
  contract pins kind+path only.
- Fenced backtick blocks mask tags (treated as code-span family); tilde
  fences do NOT mask (contract says backtick). Code spans pair equal-length
  runs CommonMark-style and may span lines; an unmatched backtick run is
  literal. These are documented lane readings a sibling implementation may
  differ on — E1/E3/E9 carry them.
- Regex-literal tag: no date validation, `r` lowercase only.
- One finding line per flagged file; multiple bad runs in one file collapse
  to the earliest.
- Bitset DP memory O(nB) bits per mode; pathological files are bounded by
  corpus scale [INFERENCE — not stress-tested beyond 36-case fixtures and
  the real lane].
- K15 read as comma-joined line list (`a` / `""` / `b`), matching the
  contract's existential-annotation reading; single-CSV-line reading cannot
  satisfy the case.

Tools: none installed (system python3 3.14.8, git 2.56.0 sufficed).
Scratch `/fast/scratch/hyaku/kake-r60/ExecGuardTool2/` removed on finish.

VERDICT: append_guard.py implemented to contract C2 — selftest 36/36 (all 22 K-cases + 14 extras), both real-lane runs exit 0, R2 mutation flags `changed corpus/knowledge/crawler-identity.md`.
