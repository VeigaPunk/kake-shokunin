# CritFailOpen — r26 measure.py fail-open reproduction (round 27, W1)

Seat: KakeR27.CritFailOpen (critic, leaf). Axis judged: operability. Milestone: r27-full-citing-set.
Scope: reproduce historical `python3 -B .ufo/waves/round-26/measure.py --root . --revision 83528f7c…` in an owned
scratch clone; independently count the missed citing pairs from Git blobs. No live-source writes, no other tests,
no r24 code read or executed. Tool installs: none.

## Verdict

- **REPRODUCED: r26 fails open.** It exits 0 with `findings: []` even though 16 knowledge citing pairs have no ledger adjudication.
- **INDEPENDENT COUNT = 16 missed / 57 citing / 41 ledger.** This equals `c2-oracle.json` expectedPairs and `c1-before.json` missing exactly, with set equality and nothing extra on either side.
- **ONE CANDIDATE PAIR NAMED: (S013, corpus/knowledge/ghp-served-set.md).** The frozen grammar misses it. It needs an explicit L1 decision (details below). It does not change the 16-pair C2 oracle.

## Environment

- Scratch clone: `/fast/scratch/hyaku/kake-r27/CritFailOpen/repo`, cloned `--no-checkout` from the lane repo, detached at
  `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`. `git status --porcelain` was empty before and after the run. TMPDIR=`…/CritFailOpen/tmp`.
- Python 3.14.8; git 2.56.0.
- Code reviewed before execution: `measure.py` imports only stdlib modules. Its only `exec` target is `.ufo/waves/round-26/source_text.py`
  (sha256 `55ae7abc…57b7d6`; imports only gzip, html.parser and re). It contains no round-24 path or reference.

## Inputs at base (sha256 of the bytes, then git blob id)

| path | sha256 | blob |
|---|---|---|
| .ufo/waves/round-26/measure.py | 13f5e1f7defddd168f28b38517c12bc04e4ad07c79081f008a50e15873e43836 | 1a823b4d |
| .ufo/waves/round-26/population.json | 16330e1effd5ee52665f8f31738e9423c6ec387e5d4a1404c5bcc35f69d01b03 (= pinned POPULATION_SHA256) | 18269471 |
| .ufo/waves/round-26/statements.json | c2026376832ad4e4114d1bc19abeec4fcbdbd0fea3dbb102ab8a5c2eb18c95ce | 52042d44 |

`git diff --stat 83528f7 be375d9 -- corpus/knowledge .ufo/waves/round-26` is empty. The declarations commit therefore did not touch any measured input.

## Reproduction result

- Exit: **0**. stderr is empty (sha256 `e3b0c442…b855`).
- stdout sha256 `24c44b9e10778283005406d3245526e09d4e5385555a8f0d0214e0a2514eae76`.
- Summary: `decided 32, expected 32, hold 32, stale 0, unverifiable 0, findings [], statements 313, statementsStale 7, statementCorrections 7, populationSource revision`.
- After JSON parsing, stdout is identical to `.ufo/waves/round-27/r26-fail-open-before.json` stdout (`identical_to_captured True`).
- Raw artifacts: `/fast/scratch/hyaku/kake-r27/CritFailOpen/measure.{stdout,stderr,exit}`.

### Why it fails open

`Checker.statement_ledger` (measure.py:437-483) iterates only `statements.json` `pairs` entries (line 456, `for entry in entries:`).
It never enumerates the corpus citing set. A (row, file) pair that is cited in `corpus/knowledge` but absent from the ledger therefore produces no finding.
Tag accounting (lines 474-483) is also keyed per ledger entry. [INFERENCE, not probed because mutation tests are out of scope]: deleting a
ledger entry whose file holds `[r26-recheck … STALE]` tags would also stay silent.

## Independent missed-pair count

Counter: `/fast/scratch/hyaku/kake-r27/CritFailOpen/indep_count.py` (sha256 `8e2000d5…8c68`). Output: `indep.json` (sha256 `311705d8…bf1`).
The counter was written fresh. It does not import or copy `count_c1.py`, `c2_count.py` or any repo code.

- It reads blobs through a single `git cat-file --batch` at the revision and lists files with `ls-tree -r -z`. All 26 knowledge files are regular (modes 100644/100755), with no symlinks or submodules.
- It walks tokens rather than using a single range regex. Every `S\d{3,}` token must have no alphanumeric or underscore character on either side. Two adjacent tokens joined only by the connectors `-`, en dash, em dash, `..`, `to` or `through` (with optional spaces) form a range, which is expanded when lo ≤ hi ≤ lo+200.
- The result is intersected with the 32-row r26 population and then compared against the 41 `statements.json` pairs.

Result: `citingPairs 57, ledgerPairs 41, missed 16, ledgerNotCited []`.

Ranges found (5): publish-channels.md `S001-S007`; sitemap-orphan-audit.md `S001-S006`; static-canonical-preflight.md
`S020-S027`, `S028-S029`, `S001–S006` (en dash).

| # | row | file | cited via |
|---|---|---|---|
| 1 | S001 | static-canonical-preflight.md | literal |
| 2 | S002 | static-canonical-preflight.md | range only |
| 3 | S003 | sitemap-orphan-audit.md | range only |
| 4 | S003 | static-canonical-preflight.md | range only |
| 5 | S004 | publish-channels.md | range only |
| 6 | S004 | static-canonical-preflight.md | range only |
| 7 | S005 | sitemap-orphan-audit.md | range only |
| 8 | S005 | static-canonical-preflight.md | range only |
| 9 | S006 | publish-channels.md | range only |
| 10 | S006 | static-canonical-preflight.md | literal |
| 11 | S008 | crawl-scope-per-host.md | literal |
| 12 | S008 | ghp-custom-domain.md | literal |
| 13 | S008 | ghp-etag-anatomy.md | literal |
| 14 | S008 | static-canonical-preflight.md | literal |
| 15 | S022 | static-canonical-preflight.md | range only |
| 16 | S023 | static-canonical-preflight.md | range only |

All files are under `corpus/knowledge/`. Eleven pairs are reachable only through range expansion. The other five are bare literals that r26 also missed: S001 and S006 in preflight, and S008 ×4. **So the r26 hole is not range-only: a pure literal scan against the ledger also catches 5 of the 16.**

Blob identities at base (git blob id / sha256):
static-canonical-preflight.md d86ddec6 / 833b28f2…31bc; sitemap-orphan-audit.md 45648e9d / 553ad100…60ec;
publish-channels.md fc35cc91 / 18042de4…73be; crawl-scope-per-host.md a05625c9 / aea5d157…f691;
ghp-custom-domain.md dda34134 / 65dd561a…19b6; ghp-etag-anatomy.md 65038704 / fa71ecd6…1d95; ghp-served-set.md efa42d20 / 405b8587…a1e7.

Frozen C2 snapshot: all 28 entries in `round-27/frozen/expected.json` `sha256` (26 knowledge files, population and ledger) match both the
local frozen bytes and the base blobs. The mismatch list is empty, so `snapshot_tampered` is not triggered on an honest run.

## Probe for citing forms outside the grammar

These forms were probed: a range with a bare end (`S001-006`), a lowercase `s001`, 1–2 digit `S1`, an attached suffix, an attached prefix, bare lists (`S001, 002`) and other
connectors (U+2212, hyphen variants, `~`, `:`, `→`, `->`, `thru`, `until`). Results:

- Bare-end ranges, lowercase, short digits, bare lists, other connectors: **0 hits**.
- Attached suffix: 1 hit, `S404_SHA256` (free-read-verbs.md:195). It is an identifier outside the population and has no impact.
- Attached prefix: 23 hits, all evidence filenames such as `w1/PairS010GhpEtagAnatomy.md` or `w2/Correction7S030.md`. Twenty-two of them name a row
  whose (row, file) pair is already in the ledger, so they have no impact.
- **Exception: (S013, corpus/knowledge/ghp-served-set.md).** Line 95 of ghp-served-set.md ends:
  > "name the round's retry, not a source of this entry (w2/Rejection01S001.md, w2/Rejection07S013.md)."

  S013 appears nowhere else in that file. The pair is neither in the ledger nor in the 57.
  `.ufo/waves/round-26/w2/Rejection07S013.md` targets "row S013, `crawl-scope-per-host.md`". The token is therefore an artifact pointer, not an
  attribution to source S013.

## Counterexamples and impacted axes

1. **Operability (C2 before-state): confirmed.** r26 detects 0/16. The "before" claim in contract.json C2 holds on local evidence.
2. **Freshness (C1 denominator): candidate 58th pair, S013 × ghp-served-set.md.** The token is literal `S013` text inside a knowledge file's historical-metadata prose,
   which the contract INCLUDEs. It is excluded only because `\b` does not fire between `7` and `S`. The contract says "none silently excluded".
   Whether a filename-embedded token is a "citing form" is UNVERIFIABLE from the contract text alone. I do not round it into decided either way.
3. **Duplicate-authority risk between the C1 and C2 grammars.** `count_c1.py` uses `\bS(\d{3,})\b`. If the gate writer (`scripts/citing_set.py`) instead uses
   a looser token rule, such as a lookbehind-free `S\d{3}` like my attached-prefix probe, the gate reports (S013, ghp-served-set.md) on the frozen snapshot.
   That yields 17 findings, so `c2_count.py` returns `passed:false` (falsePositive 1). Conversely, if C1 adds the pair through discovered-pairs.json, the gate stays
   at 16. This is correct, because C2 is pinned to the frozen r26 set. The two authorities must stay consistent on purpose, not by accident.

## Smallest safe correction (for L1; this seat makes no edits)

- C1: append `{"row":"S013","file":"corpus/knowledge/ghp-served-set.md"}` to `.ufo/waves/round-27/discovered-pairs.json`. This keeps the denominator monotone (57→58).
  Adjudicate it as `kind: artifact`, with evidence `.ufo/waves/round-26/w2/Rejection07S013.md` and contains `row S013, \`crawl-scope-per-host.md\``.
  The verdict is HOLD at its stated scope: the file says S013's evidence file is "not a source of this entry", and the artifact confirms that.
  Alternatively, record an explicit, labelled exclusion rationale. Do not drop it silently.
- C2: the gate's token rule must keep word boundaries equivalent to `\bS\d{3,}\b`. The fixture set should include an "embedded filename token is not
  a citation" case so the 16/16 and no-false-positive result is not an accident of regex choice.

## Uncertainties

- The S013 candidate's status as a "citing form" is a judgment call that belongs to L1 and the parent judge. Its evidence is listed above.
- The ledger-deletion fail-open in the "Why it fails open" section is static reasoning only; no mutation run was performed, by assignment.
- I ran no gate, selftest, fixtures or `count_c1.py`. My counter equals c1-before.json by set comparison only.
