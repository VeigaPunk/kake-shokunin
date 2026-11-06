# CriticClaims — kake round 99 w1 report (C1/C2 falsification, predicate holes)

Seat CriticClaims, leaf member. Full per-attack log with fixture commits, commands, observed
lines and rcs: `.ufo/waves/round-99/w1/CriticClaims/attacks.md` (receipts in `receipts/`,
candidates in `candidates/`). Instruments verified against `controls/instrument-sha256.txt` and
the instruments commit `2345e309…` before attacking: all match; nothing was patched, no lane
writes outside my seat dir. No tools installed. Scratch `/fast/scratch/hyaku/kake-r99/CriticClaims/`
deleted after receipt copy-out.

## C1 — 8 escapes demonstrated

All fixtures: branch `c1-<name>` in scratch clone of LANE on top of the C1 repair commit
`9d341d1b…`, scored with the frozen `c99_registry.py`. Baseline reproduced `met=true` exit 0
first. Each escape prints `met=true` exit 0 while the registry is demonstrably wrong in a way the
declared junk-prose limit (verdict map / write scope falsity) does not cover:

1. **a1 vacuous self-test** (1ccf4a35): tool's `--selftest` prints ok unconditionally while its
   real path always fails; R5 credits the executed-but-empty check. `tools=55 … met=true`.
2. **a2 comment self-test** (3ab1b6af): span `echo selftest-ok # python3 -B scripts/z9_broken.py
   --selftest` — shlex strips the comment; a SyntaxError tool is "self-tested" by `echo`.
3. **a3b duplicate Owner column** (cc76173b): `ix` is last-wins, the first Owner cell (`kaidoku`)
   is never validated.
4. **a4 ls-tree quoting** (f549c5ba): `git ls-tree -r --name-only` without `-z` C-quotes
   `scripts/z9_café.py` / `scripts/z9_qu"te.py`; they vanish from the population — committed
   tools with no registry row, `tools=54 … met=true` (also breaks tokenization symmetrically).
5. **a5 non-.py/.mjs tool** (2fffdd90): committed `scripts/z9_tool.sh` needs no row (population
   scope is declared in the docstring but the freeze surface says "tools directly under
   scripts/"); counted, flagged partially declared.
6. **a6 dangling boundary** (cc93b248): `scripts/gone.py` wrapped in `(…)` in the entry cell
   escapes SCRIPT_TOKEN lookahead → `dangling=0`.
7. **a7 non-entry column** (23e74367): dead tool named in write scope; dangling scans entry
   spans only.
8. **a8 blank-line orphan** (3dc2756b): a visible corrupted row referencing `scripts/gone.py`
   after a blank line is never scanned; `dangling=0 met=true`.

Observations (not escapes): a9 unclosed fence forces `met=false` on the TRUE registry (false
negative); a10 cross-reference in a later column never lists the tool; a11 companion-selftest
listing of a dead tool is **declared** by R5's docstring. Persistent: `exec_fail=1
scripts/robots_audit.py rc=2` at the scored repair commit and at both tips — reported, not scored.

## C2 — 7 escapes demonstrated; the landed candidate itself is clean

Counter-escape candidates (oracle + one patched behavior, `--candidate-file` only, two seeds:
99099 and 2136677243) each score `hand=50/50 generated=240/240 met=true` exit 0 while violating:

- e1 stored hop-by-hop/proxy/connection fields deleted from the updated map (contract excepts
  only 304 fields); untested — stored maps never carry them.
- e2 stored-ETag validation skipped when the 304 carries Last-Modified only ("malformed ETag in
  any stored response" refusal lost).
- e3 Last-Modified compared with spaces-only trim (contract: spaces and tabs).
- e4 refusal leaves `\n` on stdout ("nothing on stdout"; judge strips).
- e5 invalid JSON crashes with a traceback instead of `invalid_input:` (no scored input is
  invalid JSON).
- e6 304 `age` excluded from the copy (LC5: no other field excluded).
- e7 weak-rule top-tie picks the first response instead of refusing LC3 when the 304 also
  carries Last-Modified (the hand tie case is ETag-only). Passes at 230/300 random seeds
  (76.7%), and with zero generated failures at the seeds of `cde408e5`, `9d341d1b`, `7f5b1b7b`
  — and the default seed is `int(rev[:8],16)`, chosen by the landing commit (kill rule bans
  `--seed`, not landing iteration).

Direction-B: no honest-conforming candidate that fails the counter was found; blind spots are
one-sided (an over-strict probe candidate also passes).

**Landed work audit** (`998b6d5f`, sha256 `db3a0f12…`): frozen counter at its own commit
`met=true` exit 0 (seed 2576051551), and 9/9 escape-class probes agree with the frozen reference
(stored hop kept, tab trim, LC3 LM-tie refusal, age copied, malformed stored ETag refused,
case-dup refused, CR refused, tie-below-top control, invalid-JSON refusal). The C2 holes are
counter holes — the frozen predicate cannot certify contract conformance — not defects in
ExecFresh's candidate.

## Predicate holes — 11

1. `met=true` at the scored repair commit coexists with a failing declared self-test
   (`exec_fail=1`, not in mismatches).
2. Review-conjunct provenance unverifiable: plain `verdicts.tsv` files; junk `agree` lines
   satisfy it; "live" has no retained evidence.
3. One live all-agree reviewer suffices; the second seat can be dead.
4. Tip re-read "reported, not re-scored" — tip drift unbound (observed at `7f5b1b7b` and
   `998b6d5f`, both `met=true` with `exec_fail=1`).
5. C2 predicate = counter line, so all C2 blind spots are predicate blind spots.
6. The sha256 conjunct is true by construction; it cannot fail.
7. Census **after**-receipt absent from `controls/` though the freeze names before/after.
8. "One mined mistake" in `corpus/lessons/round-99.md` has no verifier.
9. C2-commit registry-row ordering rule bound by nothing (C1 not scored there; tip re-read only).
10. Default seed committer-steerable via landing choice; a hand-blind LC3 violation passes 76.7%
    of seeds and all three real revision seeds.
11. `instrument-sha256.txt` pins neither `sources/rfc9111.txt` (inline in freeze.md only) nor
    `sources/eid9185.html` (pinned nowhere).

## Smallest safe corrections (for the L1, routed not applied)

- C1: `-z` + dequote for ls-tree population; scan ALL cell spans for dangling tokens; validate
  every header cell whose name repeats; require the self-test span's argv to contain the named
  tool path outside comment position (compare `shlex.split` tokens against the span text);
  count `exec_fail` into mismatches or fail met on it.
- C2: add the e1–e7 divergence classes as hand cases (stored hop retention, LM tab trim, LC3
  LM-tie with LM present, age copy, malformed stored ETag under LM-only 304, whitespace-stdout
  refusal, invalid-JSON refusal); derive the seed from something the committer cannot choose
  post-hoc or pin it pre-freeze.
- Predicate: hash-stamp verdict files with seat identity + a liveness marker; require the
  after-census receipt; pin S484/S485 evidence digests in `instrument-sha256.txt`.

CRITIC c1_escapes=8 c2_escapes=7 predicate_holes=11
