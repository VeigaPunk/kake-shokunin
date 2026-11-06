# CriticClaims — kake round 99 w1 attack log (C1, C2, predicate holes)

Seat CriticClaims (hyaku run 15, kake round 99, wave 1). Scope: falsify C1 and C2 as frozen at
`ab35eace`/instruments `2345e309`; attack instruments and work, never patch them. Leaf member, no
subagents. Every command below was executed; every observed line is verbatim from the receipts
copied to `receipts/`. No repairs were made to any lane file; all writes stayed inside
`.ufo/waves/round-99/w1/CriticClaims/` and scratch `/fast/scratch/hyaku/kake-r99/CriticClaims/`.

## 0. Environment, authorization, digest verification

- Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`; `git rev-parse master` observed
  `7f5b1b7b8dbfdae74dfe6d487bbf5406c478b916` at attack start; the C2 content commit `998b6d5f`
  landed mid-attack and is audited in §3. No lane mutation performed (read-only git only).
- Fixture clone: `git clone --shared <LANE> fx`, then `git checkout --detach 9d341d1b…`;
  `git -C fx rev-parse --show-toplevel` observed `/fast/scratch/hyaku/kake-r99/CriticClaims/fx`
  (asserted before every fixture commit). Fixture identity used `-c user.name=CriticClaims
  -c user.email=criticclaims@example.invalid` only. One live clone.
- Frozen digests: `sha256sum` of worktree bytes equals `controls/instrument-sha256.txt` equals
  `git show 2345e309…:<path> | sha256sum` for c99_registry.py (`0f39bbbc…`), c99_fresh304.py
  (`d13bba5d…`), fresh304-contract.md (`2be46b4d…`); `sources/rfc9111.txt` observed
  `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, matching freeze.md.
  No mismatch → no repair license. **Observation:** `controls/instrument-sha256.txt` contains 11
  entries and pins neither `sources/rfc9111.txt` nor `sources/eid9185.html`; the EID 9185 page
  (S485 evidence) is pinned nowhere (hole H11).
- Tooling: nothing installed (python3/git/node preexisting sufficed) — operator rule satisfied
  vacuously; pacman untouched.

## 1. C1 — attacks on `.ufo/waves/round-99/c99_registry.py`

Counter command template (all runs):
`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-99/c99_registry.py --root <fx> --revision <FIXTURE_SHA> --work /fast/scratch/hyaku/kake-r99/CriticClaims/work`

Baseline (reproduction, not re-stamp): revision `9d341d1b…` in fx →
`tools=54 rows=152 listed=54 unlisted=0 dangling=0 exec_fail=1 mismatches=0 met=true`, exit 0
(`receipts/c1-baseline.txt`) — matches `controls/after-c1.txt`. Note `exec_fail=1`
(`exec_fail 1104 scripts/robots_audit.py rc=2`) is reported but NOT counted in mismatches: the
scored, predicate-satisfying state carries a row whose declared self-test fails to execute (H1).

Fixtures are branch `c1-<name>` in fx on top of `9d341d1b…`; delta described per line.

| id | fixture (commit) | delta | observed first line | rc | escape |
|----|------------------|-------|---------------------|----|--------|
| a1 | `receipts/c1-a1-vacuous-selftest.txt` (1ccf4a35) | add `scripts/z9_demo.py` whose `--selftest` prints ok unconditionally while its real path (`real_check()` false → exit 1) always fails; add a conformant row whose self-test is `python3 -B scripts/z9_demo.py --selftest` | `tools=55 rows=153 listed=55 unlisted=0 dangling=0 exec_fail=1 mismatches=0 met=true` | 0 | **YES** |
| a2 | `receipts/c1-a2-comment-selftest.txt` (3ab1b6af) | add `scripts/z9_broken.py` (SyntaxError); row self-test span `echo selftest-ok # python3 -B scripts/z9_broken.py --selftest` | `tools=55 rows=153 listed=55 … met=true` | 0 | **YES** |
| a3 | `receipts/c1-a3-dup-owner-column.txt` (89be5cce) | first attempt: dup-Owner table inserted mid-table — swallowed as rows of the parent table (driver placement bug, my defect, superseded) | `tools=55 rows=153 listed=54 unlisted=1 … met=false` | 1 | no (fixture malformed) |
| a3b | `receipts/c1-a3b-dup-owner-eof.txt` (cc76173b) | dup-Owner table appended after the completion table: header `… Write scope \| Owner \| Owner`, row cells `… \| kaidoku \| kake \|` | `tools=55 rows=153 listed=55 unlisted=0 dangling=0 … met=true` | 0 | **YES** |
| a4 | `receipts/c1-a4-lstree-quoting.txt` (f549c5ba) | commit `scripts/z9_café.py` and `scripts/z9_qu"te.py`, no rows | `tools=54 rows=152 listed=54 unlisted=0 dangling=0 … met=true` | 0 | **YES** |
| a5 | `receipts/c1-a5-sh-extension.txt` (2fffdd90) | commit `scripts/z9_tool.sh`, no rows | `tools=54 rows=152 … met=true` | 0 | **YES** (partially declared, see below) |
| a6 | `receipts/c1-a6-dangling-paren-entry.txt` (cc93b248) | completion row entry span becomes `python3 -B scripts/base_path_selftest.py (dead fallback scripts/gone.py)` | `tools=54 rows=152 listed=54 unlisted=0 dangling=0 … met=true` | 0 | **YES** |
| a7 | `receipts/c1-a7-dangling-write-scope.txt` (23e74367) | base_path row write-scope cell gains `(replaces scripts/gone.py)` | `tools=54 rows=152 … dangling=0 … met=true` | 0 | **YES** |
| a8 | `receipts/c1-a8-blankline-orphan.txt` (3dc2756b) | visible corrupted row `… cache_key.py && python3 -B scripts/gone.py …` placed after a blank line at EOF | `tools=54 rows=152 … dangling=0 … met=true` | 0 | **YES** |
| a9 | `receipts/c1-a9-unterminated-fence.txt` (bd5158b8) | unclosed ` ``` ` inserted before the completion heading (OBSERVATION) | `tools=54 rows=126 listed=28 unlisted=26 … mismatches=26 met=false` | 1 | no — instrument false negative on the TRUE registry |
| a10 | `receipts/c1-a10-later-column-only.txt` (3efbc468) | row mentions committed `scripts/z9_late.py` only in write scope; entry names uncommitted z9_ok.py (OBSERVATION) | `tools=55 rows=153 listed=54 unlisted=1 dangling=1 … met=false` | 1 | no — false negative: later-column coverage never lists |
| a11 | `receipts/c1-a11-companion-selftest.txt` (b127bd58) | dead `z9_real.py` listed via always-pass companion `z9_real_selftest.py` (OBSERVATION) | `tools=56 rows=154 listed=56 … met=true` | 0 | no — **declared** by R5 ("or another population file whose name contains 'selftest'") |

Escape analysis (why these exceed the declared limit):
- a1/a2: the declared limit covers "a row whose verdict map or write scope is false but
  well-formed". The self-test cell is a third cell; R5's only enforcement is "that span EXECUTES
  with exit 0". a1 executes the tool in a mode that tests nothing; a2 executes `echo` (shlex
  strips the `#` comment) so the named tool is never run at all. `met=true` with a registry that
  asserts a working, self-tested gate for a tool that cannot run.
- a3b: `ix = {h: k for k, h in enumerate(hdr)}` makes a duplicate `Owner` header last-wins; the
  first Owner cell (`kaidoku`) is never read. R4 checks one cell only.
- a4: population is built from `git ls-tree -r --name-only` (no `-z`); with default
  `core.quotePath`, non-ASCII/quote names arrive C-quoted (`"scripts/z9_caf\303\251.py"`) and fail
  `startswith("scripts/")` → committed tools invisible → registry missing entire tools, `met=true`.
  Symmetric false-positive: referencing such a tool in a row also cannot be tokenized.
- a5: docstring declares the population as `scripts/*.py|*.mjs`; freeze.md's C1 surface says
  "the committed tools directly under `scripts/`" with no extension limit. A committed shell tool
  needs no row. Counted as an escape of the claim-vs-instrument gap, flagged partially declared.
- a6/a7/a8: dangling detection scans ENTRY-command spans only, with token boundaries
  `(^|[\s'"=])…(?=$|[\s'\"])`; a `(…)`-wrapped path, a non-entry column, or any row after a blank
  line is never scanned. The registry visibly references dead `scripts/gone.py`; counter reports
  `dangling=0 met=true`.
- a9/a10 are the mirror image: the counter can be forced to `met=false` on a true registry
  (unclosed fence) and cannot see cross-references — relevant to any junk landing that edits
  fences or splits tables.

**C1 result: 8 escapes demonstrated (a1, a2, a3b, a4, a5, a6, a7, a8).**

## 2. C2 — attacks on `.ufo/waves/round-99/c99_fresh304.py`

Candidate scoring (controls mode only, `--candidate-file`; never a lane write). Two seeds per
candidate: default `--candidate-file` (seed 99099) and `--revision 7f5b1b7b…` (seed 2136677243).
Template:
`python3 -B .ufo/waves/round-99/c99_fresh304.py --root <LANE> --candidate-file <cand> [--revision <rev>] --work /fast/scratch/hyaku/kake-r99/CriticClaims/work2`
Candidates: `candidates/<name>.py` (copies also in seat dir), all derived from the frozen oracle
`frozen/pos-oracle.py` with one patched behavior each.

| id | candidate | contract clause violated | observed (seed 99099) | rc | observed (seed 2136677243) | rc | escape |
|----|-----------|--------------------------|----------------------|----|---------------------------|----|--------|
| e1 | `candidates/e1-storedhopstrip.py` | updated map must start from the stored headers; only **304** fields are excepted — candidate deletes stored `connection`/hop/proxy fields from the updated map | `… hand=50/50 generated=240/240 refusals=50/50 seed=99099 met=true` | 0 | `… refusals=51/51 seed=2136677243 met=true` | 0 | **YES** |
| e2 | `candidates/e2-lazyetag.py` | refusal: "malformed ETag in the 304 **or in any stored response**" — stored ETags parsed only when selection reads them; slips through when the 304 carries Last-Modified only | `… met=true` | 0 | `… met=true` | 0 | **YES** |
| e3 | `candidates/e3-lmspacetrim.py` | LC1/LM compare "after trimming spaces **/tabs**" — candidate trims spaces only | `… met=true` | 0 | `… met=true` | 0 | **YES** |
| e4 | `candidates/e4-wsstdout.py` | refusal: "nothing on stdout" — candidate writes `\n` to stdout on refusal; judge's `out.strip()==""` accepts it | `… met=true` | 0 | `… met=true` | 0 | **YES** |
| e5 | `candidates/e5-badjsoncrash.py` | unparseable input must refuse `invalid_input:` — candidate lets `json.loads` raise a traceback; no scored input is invalid JSON | `… met=true` | 0 | `… met=true` | 0 | **YES** |
| e6 | `candidates/e6-ageexcl.py` | LC5: "no other field is excluded" — candidate also excludes the 304's `age` from the copy | `… met=true` | 0 | `… met=true` | 0 | **YES** |
| e7 | `candidates/e7-lmtiepickfirst.py` | LC3: tie on largest `received` must refuse — candidate picks the first corresponding response when the 304 also carries Last-Modified (hand `weak-tie-refused` is ETag-only, so hand stays 50/50) | `… refusals=50/50 seed=99099 met=true` | 0 | `… refusals=51/51 seed=2136677243 met=true` | 0 | **YES** |
| — | `candidates/honest-strict.py` | direction-B probe: additionally refuses JSON objects with case-insensitive duplicate keys (contract silent, reference last-wins) | `… met=true` | 0 | `… met=true` | 0 | n/a — over-strictness also undetected |

Receipts: `receipts/c2-e*.txt`, `receipts/c2-honest-strict.txt`.

Seed steering (H10), in-process simulation using the counter's own `gen_case`/reference
(`c2_grindsim.py`, receipts in `receipts/`): the e7-flawed candidate passes hand 50/50 and, over
300 random 32-bit seeds, scores full `met=true` on **230/300 (76.7%)**; per-seed generated
failures mean 0.2/240 (histogram `{0:230, 1:65, 2:5}`). It passes with 0 generated failures at
the seeds of real revisions `cde408e5` (3454273765), `9d341d1b` (2637438235), `7f5b1b7b`
(2136677243). The default seed is `int(rev[:8],16)` — chosen by whoever lands the commit; the
kill rule forbids `--seed` but not landing iteration. Grinding is unnecessary for these classes
and trivially available for rarer ones.

Direction-B (fail while honouring): no honest-conforming candidate that FAILS the counter was
found; the frozen reference and the contract agree on every scored path I could derive (50 hand +
all grammar-reachable generated shapes). The blind spots are strictly one-sided: any candidate
conforming on tested paths and violating elsewhere passes.

**C2 result: 7 escapes demonstrated (e1–e7).**

## 3. Landed candidate audit (998b6d5f) — the work itself

`git show 998b6d5f…:scripts/freshen_304.py` (sha256 `db3a0f12b91a5a54409ebafcf800204011385a523ff4da9b897b71dd7c0c1d4f`):

- Frozen counter at its own commit:
  `revision=998b6d5f… candidate=present sha256=db3a0f12… hand=50/50 generated=240/240 refusals=47/47 seed=2576051551 met=true`, exit 0 (`receipts/c2-landed-998b.txt`).
- 9 escape-class probes (`probe_landed.py`, copied to seat dir): stored hop-by-hop fields kept,
  LM tab-trim, LC3 LM-tie refusal, `age` copied, malformed stored ETag refused under LM-only 304,
  case-duplicate response names refused, CR in stored value refused, tie-below-top control,
  invalid-JSON refusal — **0 divergences from the frozen reference**.
- Verdict: the landed candidate honours the contract on every class the counter cannot test. The
  C2 findings above are **counter holes** (the frozen predicate cannot certify contract
  conformance), not defects in ExecFresh's candidate.

## 4. Predicate holes in freeze.md (do-nothing / junk satisfiable)

- **H1** The frozen C1 predicate is satisfied by `met=true exit 0` at `9d341d1b…` while the
  counter itself reports `exec_fail=1 scripts/robots_audit.py rc=2`: a registered row's declared
  self-test fails at the scored commit and `exec_fail` is not part of `mismatches`. A registry
  with a failing declared self-test is "met". (controls/after-c1.txt; reproduced c1-baseline.)
- **H2** Review-conjunct provenance is unverifiable: `w1/<seat>/verdicts.tsv` are plain files;
  nothing binds a line to a live seat's execution. Junk `agree` lines satisfy "no live verdict is
  disagree". (Corollary: "live" has no retained liveness evidence.)
- **H3** One live all-agree reviewer suffices: the predicate needs ≥1 live verdict per row and
  zero `disagree`; one dead seat + one complicit/junk seat passes. Kill rule only fires on
  `disagree` or both seats verdict-less.
- **H4** "C1 … re-read at the tip (reported, not re-scored)": tip drift is unbound. Observed:
  C1 at tip `7f5b1b7b` still `met=true` with `exec_fail=1` (`receipts/c1-attip.txt`); after the
  C2 content commit landed, re-read at `998b6d5f` observed `tools=55 rows=153 listed=55
  unlisted=0 dangling=0 exec_fail=1 mismatches=0 met=true`, exit 0
  (`receipts/c1-at-master-998b.txt`) — the C2 commit did carry its row, and the failing
  `robots_audit` self-test persists at the tip. A landing that regresses SKILL.md after the
  repair commit is only "reported".
- **H5** The C2 predicate is exactly the counter line, so every counter blind spot above (e1–e7)
  is a predicate blind spot: "met on the frozen predicate" certifies counter-pass, not contract
  conformance.
- **H6** The target conjunct "the scored sha256 equals `git show <REV>:scripts/freshen_304.py |
  sha256sum`" is true by construction for any committed candidate — it cannot fail and verifies
  nothing beyond self-consistency.
- **H7** Freeze requires "Census before/after"; `controls/` contains only `census-before.txt`.
  No after-receipt, no target: a junk landing can skip the after-census.
- **H8** "one mined mistake in `corpus/lessons/round-99.md`" has no counter, digest, or checker;
  any edit claiming the role satisfies the sentence.
- **H9** Ordering rule "the C2 commit must carry its own conformant registry row" is bound by
  nothing: C1 is not scored at the C2 commit, and the tip re-read is reported only (H4). Had
  `998b6d5f` landed without its registry row, no frozen artifact would fail.
- **H10** Default seed committer-steerable (§2): seed = `int(rev[:8],16)`; "no re-seeding"
  forbids the flag, not choosing the revision. With mean 0.2 generated failures per seed for a
  hand-blind LC3 violation, a flawed candidate passes most seeds outright (76.7%), all three real
  revision seeds included.
- **H11** `controls/instrument-sha256.txt` pins the two counters, the contract, and the frozen
  control subjects — not `sources/rfc9111.txt` (pinned only inline in freeze.md) and not
  `sources/eid9185.html` (pinned nowhere). S485's evidence bytes are unpinned.

**Predicate holes: 11.**

## 5. Verdict lines (each names its command and observed rc)

- Digests: `sha256sum` over the five frozen paths vs `controls/instrument-sha256.txt` vs
  `git show 2345e309…` — all equal (c99_registry `0f39bbbc…`, c99_fresh304 `d13bba5d…`,
  contract `2be46b4d…`, rfc9111 `aeb52adb…`); eid9185 unpinned. rc 0.
- C1 baseline reproduction: counter `--root fx --revision 9d341d1b…` → `met=true`, exit 0.
- C1 escapes: 8 fixtures (§1) each `met=true` exit 0 while the registry is demonstrably wrong
  beyond the declared junk-prose limit; observations a9/a10 `met=false` exit 1 (false negatives).
- C2 escapes: 7 candidates × 2 seeds (§2) each `met=true` exit 0 (both rc 0) while violating the
  cited clause; honest-strict also passes (no false negative found).
- Seed steering: `c2_grindsim.py` in-process over 300 seeds → 230 met (rc 0), plus 0 failures at
  the three real revision seeds.
- Landed candidate: counter at `998b6d5f…` → `met=true` exit 0; 9/9 probes agree with the frozen
  reference (rc 0 probes, divergences=0).

## Final line

CRITIC c1_escapes=8 c2_escapes=7 predicate_holes=11
