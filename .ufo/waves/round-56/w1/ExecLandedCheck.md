# ExecLandedCheck

Landed-vs-claimed check — considerthese 2026-10-25 proposal 1, implemented as a candidate tool for round 56.
Lane repo `/home/vgpnk/Projects/shokunin/kake-shokunin`, branch `master` (local head `6b3df99`, `origin/master`
tracking ref at the same object). Read-only git throughout; no lane jj/index/ref mutation, no commit.

## SCRIPT PATH:

`.ufo/waves/round-56/w1/ExecLandedCheck.files/landed_check.py` (python3, stdlib only, 474 lines).
Receipts beside it: `selftest.txt` (fixture run), `real-run.txt` (primary + supplemental + negative + usage runs).

Invocation: `python3 -B landed_check.py --report <report.md> --repo <git dir> --branch <name>`.

Behaviour as built:
- extracts every 7–40 hex-digit token (backticked or bare); a 64-hex sha256 digest is skipped by construction
  (the regex never matches inside a longer hex run), and an unresolvable hex token on a line naming a digest
  algorithm (`sha256`/`sha1`/`md5`) is suppressed as a digest fragment;
- resolves each token in `--repo`; a token resolving to a non-commit object (blob/tree) is skipped, a token
  resolving to nothing is `UNKNOWN`;
- ancestry via `git merge-base --is-ancestor <oid> <branch>`; duplicates deduped by resolved full oid;
- prints `ANCESTOR|NOT-ANCESTOR|UNKNOWN <hash> <subject>` per cited commit, then
  `cited=N landed=N missing=N unknown=N`; suppressed digest tokens are reported on stderr only, so stdout keeps
  the four-counter contract;
- exits 0 (all cited resolvable hashes are ancestors, at least one resolvable), 1 (any `NOT-ANCESTOR`),
  2 (unevaluable: bad repo/branch/report, no resolvable hash, or an ancestry query failed), 64 (usage).

## SELFTEST: 14/14

`python3 -B landed_check.py --selftest` → `selftest 14/14`, exit 0 (`selftest.txt`). Fixtures, each in its own
`mktemp -d` repo initialised with `git -C "$D" init -q -b master`, every later call `git -C "$D" …`, toplevel
asserted equal to `$D`, commits made with `-c user.name=selftest -c user.email=selftest@local`:

| fixture | proves | observed |
|---|---|---|
| honest-report | full + short citations of two ancestors | exit 0, cited=2 landed=2 |
| side-branch-hash | hash on a side branch is not landed | exit 1, missing=1 |
| unknown-hash | unresolvable 40-hex token | exit 0, unknown=1, landed=1 |
| sha256-token-ignored | 64-hex digest never extracted | cited=1 |
| short-hash-ambiguity | 7-hex prefix shared by two written blobs (`rev-parse --disambiguate` asserted ≥2) | `UNKNOWN`, unknown=1, exit 0 |
| empty-report | nothing cited | exit 2, cited=0 |
| prose-only-report | no hex tokens at all | exit 2, cited=0 |
| branch-missing | branch does not resolve | exit 2 |
| hash-inside-code-fence | fence does not hide a citation | exit 0, cited=1 |
| duplicate-hash-counted-once | full + 12-char + 7-char of one commit | cited=1 |
| non-commit-object-skipped | blob oid cited beside a commit | cited=1 (blob not counted) |
| digest-label-ignored | `sha256 2b146a72` fragment on a digest line | cited=1 |
| report-missing | absent report path | exit 2 |
| usage-error | no arguments | exit 64 |

## REAL RUN:

`python3 -B landed_check.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-55/kake.md --repo /home/vgpnk/Projects/shokunin/kake-shokunin --branch master`

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
landed_check: suppressed 3 digest-labelled non-commit token(s)
EXIT=0
```

- **10 unique commit hashes, not 9** (assignment said 9). The report cites 12 hash tokens: 3 in the header
  (`fcaf4b85…` base, `64c0ce12ffe3ca…` measured content, `5515f8bbcd69ef…` tip) and 9 in the *Landed changes*
  table, of which two are short repeats of header entries (`64c0ce12ffe3`, `5515f8bbcd69`) → 10 distinct commits.
  All ten are ancestors of `master`; the r55 "pushed before landed" failure mode does not recur here.
- Suppressed tokens: `ee8c9def`, `3173d961`, `2b146a72` — the report's "sha256 ee8c9def…, 3173d961…, 2b146a72…"
  line. Checked: `git cat-file -t` says `Not a valid object name` for each, so none is a git object in the lane;
  they are page-body digests, not landing claims.
- Independent cross-check (different mechanism, full walk): `git rev-list master | grep -qx <full oid>` returned
  IN-MASTER-WALK for all ten.
- Supplemental run against `origin/master` → identical output, exit 0. `origin/master` is the local
  remote-tracking ref, and it equals `master` (`6b3df99`); no fetch was performed.
- Negative control on the real repo (`real-run.txt`): a scratch report citing `955e3d7bd6d1` plus
  `d1ac21ee860b` (a `refs/jj/keep` commit not reachable from `master`) → `NOT-ANCESTOR d1ac21ee860b -`,
  `cited=2 landed=1 missing=1 unknown=0`, exit 1. Usage with no arguments → exit 64.

## LIMITS:

- **Local ancestry only.** `--branch master` answers "is this commit on the lane's local branch", not "was it
  pushed". A claim like r52's "six commits pushed" is only covered when `--branch origin/master` is used and
  that tracking ref is fresh; this run used the stale-by-default tracking ref (no `git fetch`), so push state is
  still unverified. Live verification would need a network fetch or `git ls-remote`, which this tool does not do.
- **Text heuristics.** Hash extraction is lexical: any 7–40 hex run in prose, tables, code fences, URLs or
  filenames is a candidate. A genuine short commit hash that happens to be all decimal digits still resolves
  (resolution precedes the digest rule); an unresolvable hex token on a digest-labelled line is silently
  suppressed, which could hide a fabricated hash written on such a line (it can only be an `UNKNOWN`, never a
  landed/missing result, since it does not resolve).
- **`UNKNOWN` is not proof of dishonesty.** It means "this token is not a commit object in this repo" — could be
  a digest prefix, a foreign-repo hash, or a fabrication. The tool cannot tell them apart.
- **Branch must exist locally.** `--branch` resolves to a commit; an unfetched remote branch yields exit 2.
- **Ancestry only, not content.** The tool does not check that the cited commit actually contains the change the
  report attributes to it, nor that the report's "before/after" numbers were measured at those revisions.
- **Merge-base cost.** One `merge-base --is-ancestor` plus one `log -1` per cited commit; fine for report-sized
  inputs, not intended for whole corpora.
- **Proposal 1's cadence not implemented.** This is the check, not the daily run: nothing here schedules it per
  round, and the report-side call site (the closure that writes round reports) is unchanged.
- Tooling: nothing installed or upgraded; no pacman transaction attempted.

VERDICT: landed_check.py built and green (selftest 14/14); real run on r55 kake report shows 10/10 cited commits are ancestors of master, 0 missing, exit 0.
