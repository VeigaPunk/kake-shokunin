# ExecLandedCheckRun

Target: `scripts/landed_check.py` at `a450e43e696d032e3ac308383f6b3394e0c92860` (blob `7bf05031011b4682f010990195047bc72ff0e3ce`,
487 lines). Every run below happened in my own clone `D=/tmp/tmp.D8cOXwVkEv`
(`git clone -q --no-checkout /home/vgpnk/Projects/shokunin/kake-shokunin "$D" && git -C "$D" checkout -q a450e43…`,
`git -C "$D" rev-parse --show-toplevel` = `/tmp/tmp.D8cOXwVkEv`, HEAD detached at `a450e43`). A second independent clone
(`/tmp/tmp.anNw8cgPNt`) reproduced every number quoted here. The lane checkout was never executed in and never written to.

## SELFTEST:

`cd $D && timeout 600 python3 -B scripts/landed_check.py --selftest` → 14 `PASS` lines, final line `selftest 14/14`,
**exit 0**, wall time 1.4 s. Fixtures exercised: `honest-report`, `side-branch-hash`, `unknown-hash`,
`sha256-token-ignored`, `short-hash-ambiguity`, `empty-report`, `prose-only-report`, `branch-missing`,
`hash-inside-code-fence`, `duplicate-hash-counted-once`, `non-commit-object-skipped`, `digest-label-ignored`,
`report-missing`, `usage-error`.

Fixture hygiene (`scripts/landed_check.py:233`, `:426`): each fixture repo is `tempfile.mkdtemp(prefix="landed-check-")`,
its toplevel is asserted equal to the temp dir (`:235-239`), commits are made with
`-c user.name=selftest -c user.email=selftest@local` (`:250-252`), and the tree is removed in `finally` via
`shutil.rmtree`. After the run, `ls -d /tmp/landed-check-*` = 0 leftover directories.

## REAL RUN:

```
cd $D && timeout 600 python3 -B scripts/landed_check.py \
  --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-55/kake.md \
  --repo /tmp/tmp.D8cOXwVkEv --branch master
```

Branch used: **`master`** (clone-local ref, `7ad7db51dfcff2eccea9f7f73726f2437b2ed8de`, identical to `origin/master`;
`origin/master` also exists — `master` is the branch this clone checks out-able and the one the lane calls master).

stdout (10 lines, then summary):

```
ANCESTOR fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d round-54 verifier spot-check (integrator, hyaku): non-author admit/reject
ANCESTOR 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 round-55: content revision — reviewer repairs, lesson caveat, validation receipts
ANCESTOR 5515f8bbcd69ef5ddd51ed0f7bccebd76a8485fc round-55: W2 settlement, remaining seat reports
ANCESTOR b467ac3a89c8 round-55: frozen contract, counters, base controls, retained sources
ANCESTOR 143e59293896 round-55: W1 spec and dispatch, pre-append registry mirror pin
ANCESTOR 2bda8e4227a7 round-55: build — three Yahoo robots entries, S418 row, coverage-map rows, counters v2, W1 reports
ANCESTOR a7a548e102b7 round-55: QUALITY criteria, gate registry rows, PROVINCE step, counter selftests
ANCESTOR 78963ae28e1c round-55: W1 settlement results, ScoutScopeOverlap report, W2 spec
ANCESTOR faf9abe81d1e round-55: wave-2 repairs — entries, README rows, lesson, counters v2.1, validation receipts
ANCESTOR 955e3d7bd6d1 round-55: measurement receipts, settlement, SCORECARD and LOG
cited=10 landed=10 missing=0 unknown=0
```

stderr: `landed_check: suppressed 3 digest-labelled non-commit token(s)` (streams confirmed separately: summary on stdout,
suppression note on stderr, `scripts/landed_check.py:478-480`). **Exit 0**, elapsed < 1 s.

Independent cross-check of the same report (own `git rev-parse --verify <t>^{commit}` / `git cat-file -t` loop): 17 distinct
7–39-hex tokens; 14 resolve to commit objects (10 distinct after 12- and 7-char prefixes collapse), 3 resolve to no object:
`ee8c9def`, `3173d961`, `2b146a72`. All three sit on report line 19, which names `sha256`, and they are the first 8 hex of the
sha256 of `.ufo/waves/round-55/sources/S372.html`, `S373.html`, `S418.html` (`sha256sum` = `ee8c9def…`, `3173d961…`,
`2b146a72…`; same values in `sources/receipts.json`). So in this run the suppression hid digest fragments, not a commit claim,
and the 10/10 result is complete for the report's commit citations.

## FIXTURE RUN:

Scratch repo `F=/tmp/tmp.G6ppG2VOwS`: `git -C "$F" init -q -b master`, `git -C "$F" rev-parse --show-toplevel` = `$F`,
commits made with `-c user.name=selftest -c user.email=selftest@local`. Contents:

- real ancestor on `master`: `42119f85ee2971aa27e8f06b40427a902e4be338` (root commit)
- hash on side branch `side` created inside `$F`: `672b6d3d1f5e3ec76b70767ac8424c29dc0ca9e2`
  (`git -C "$F" merge-base --is-ancestor 672b6d3d… master` → exit 1, so not an ancestor)
- random 40-hex string: `7e4afbcabb1f594427f246b7f1caddbcf77c18d3` (`python3 -c 'secrets.token_hex(20)'`)

Report `$F/report.md` cites those three. Output:

```
ANCESTOR 42119f85ee2971aa27e8f06b40427a902e4be338 fixture root commit
NOT-ANCESTOR 672b6d3d1f5e3ec76b70767ac8424c29dc0ca9e2 side-branch-only commit
UNKNOWN 7e4afbcabb1f594427f246b7f1caddbcf77c18d3 -
cited=3 landed=1 missing=1 unknown=1
```

**Exit 1** — matches the documented rule "at least one cited commit is NOT an ancestor of BRANCH"
(`scripts/landed_check.py:20-21`); all three classes are classified as the assignment requires.

Write-safety, both repos inspected: `(path,size,mtime)` snapshots taken immediately before and after each run, over the whole
worktree **and** every entry under `.git/` (e.g. `.git/index`, `.git/logs/*`, `.git/refs/*`). In `$F` and in `$D` the two
snapshots are byte-identical (`diff` empty, "no-writes-in-fixture-repo" / "(none)") and `git -C "$D" status --porcelain` is
0 lines. Attribution note: an earlier attempt in a third clone showed `.git` and `.git/index` mtime movement, which came from my
own `git status` interleaved between the snapshots; with the tool as the only command between snapshots, nothing changes.
Read-only git subcommands only: `rev-parse --git-dir`, `rev-parse --verify …^{commit}`, `cat-file -t`, `log -1`,
`merge-base --is-ancestor` (`:69-115`); no `fetch`, `update-ref`, `gc`, no index write.

**Limit found by probe** (attacks `scripts/landed_check.py:189-193`, line-scoped `DIGEST_LABEL.search(line_text)`): in `$F`,
`sha256 0226a9359f431a31f7b487baf555d232a9a018c2 digest fragment; landed 42119f85…` → `cited=1 landed=1 missing=0 unknown=0`,
exit 0, one suppressed token — a fabricated 40-hex hash is silently absorbed because the *line* mentions `sha256`. The same
hash without the label → `UNKNOWN 0226a935…`, `cited=2 landed=1 unknown=1`. So one word on a line can blind the tool to a
fabricated citation; this is disclosed in the module docstring (`:11-13`) but in neither `SKILL.md` nor the lesson.

## TRUTHFULNESS:

Worktree blobs of all three doc/tool files are byte-equal to their committed blobs at `a450e43`
(`git hash-object <file>` = `git rev-parse a450e43:<file>`): `SKILL.md` `0bb37a25…`, `corpus/lessons/round-56.md`
`30356ea9…`, `scripts/landed_check.py` `7bf05031…`.

1. `SKILL.md:1248` — "`scripts/landed_check.py` is a tool, not a gate: it compares the commit hashes a report cites with
   branch ancestry (considerthese proposal 1)." **True on both clauses.** It appears only in prose, not in either gate-registry
   table (the two round-56 rows are `selftest-tally-counter` and `yahoo-crawl-handling-quote-truth-counter`), so calling it a
   tool is consistent with the registry; its only behaviour is ancestry comparison against the `--branch` argument. The
   parenthetical matches `considerthese/2026-10-25.md` proposal 1 ("compare every commit hash a round report cites against
   `origin/master` ancestry before I describe it as landed"). One narrowing the sentence does not carry: "every commit hash"
   is implemented as every 7–40-hex token that resolves to a commit — 64-hex tokens (`:122`), tokens resolving to non-commit
   objects (`:185-187`) and unresolvable hex on digest-labelled lines (`:189-193`) are dropped by design.
2. `corpus/lessons/round-56.md:65` — "implemented as `scripts/landed_check.py` with a selftest and run on the round-55 report
   (10 cited hashes, 10 ancestors of `master`)". **Reproduced exactly**: selftest exists and is green (14/14, exit 0); the
   round-55 run yields `cited=10 landed=10 missing=0 unknown=0`, exit 0, and every one of the ten is `ANCESTOR` of `master`.
   "10 cited hashes" is the tool's distinct-commit count; the report holds 17 distinct hex tokens (14 resolving to commits,
   3 genuine body sha256 prefixes), so the phrase is exact for the counter and merely not a token census.
3. Stdlib-only — `grep -n '^import\|^from'` on the committed file: `:39 from __future__`, `:41 argparse`, `:42 hashlib`,
   `:43 os`, `:44 re`, `:45 shutil`, `:46 subprocess`, `:47 sys`, `:48 tempfile`. No other import form (`importlib`,
   `__import__`, dynamic import) anywhere in the file; no network module; the only spawned binaries are `git` and
   `sys.executable` (the usage-error fixture, `:409-411`). **Claim holds.**
4. Out of my named scope, recorded as data only: `/.ufo/waves/round-56/w1/ExecLandedCheck.md:9` says the candidate is
   "474 lines", while the candidate copy `.ufo/waves/round-56/w1/ExecLandedCheck.files/landed_check.py` is 487 lines and is
   blob-identical (`7bf05031…`) to the landed `scripts/landed_check.py`. The line count is stale; the file identity is exact.

Unrun: no run against a bare repo, a shallow clone, or a `--branch` given as a raw commit; no test of the tool on a report
whose cited hash exists only in a remote-tracking ref that is absent from the clone.

VERDICT: landed_check.py is green and honest at a450e43 — selftest 14/14 exit 0; real run on the r55 kake report `cited=10 landed=10 missing=0 unknown=0` exit 0 against `master` (`7ad7db51`); fixture (ancestor / side-branch / random 40-hex) `cited=3 landed=1 missing=1 unknown=1` exit 1; stdlib-only, zero writes in either inspected repo, SKILL.md and lesson claims reproduced — one residual risk: a fabricated hash on a line naming a digest algorithm is silently suppressed.
