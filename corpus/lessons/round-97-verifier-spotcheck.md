# Round 97 verifier spot-check — kake (hyaku closure, non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Lane round: kake round 97 (hyaku run 15, attempt 1). Base `36d148f5c60100021304903c30e5663207c72f4f`,
lane tip `1dacba598775d37f18705e130354465e3c19802b`. Report `.ufo/reports/round-97/kake.md`; dispatched
prompt `.ufo/prompts/kake-round-97.md`. This closure did not author the round and changes none of
its files. Every check below was run by this closure on 2026-11-05 (~21:20–21:40Z). It never ran
the lane's counters (gates). Where a claim rests on those counters, this closure checked the
committed evidence and then took a separate measurement of its own.

Driver digest (copied from the mutable `.ufo/watchdog.log`, lines 2919 and 2926):

    2026-11-05T17:42:17-03:00 launch kake round=97 pgid=1636561 driver=hyaku-inline attempt=1
    2026-11-05T18:34:38-03:00 complete kake round=97; hyaku-inline attempt=1

`grep -c 'lane-dead-no-report kake round=97' .ufo/watchdog.log` → 0.

## 1. Step-1 conformance — PASS; the named defects do not change the status

- **Report attribution.** `git log --format='%an %ae %H %cI' -- .ufo/reports/round-97/kake.md` →
  `kake-shokunin kake@shokunin.local 8b852b3858fc77dfa3e1b78cd0638cdca3937f4d 2026-11-05T18:34:21-03:00`.
  The lane identity committed it, 17 s before the driver's `complete` line.
- **SHONEN heading.** `## SHONEN` is present, with one line per box (4 lines: `[~]`, `[ ]`, `[~]`, `[~]`).
- **Cited commits.** `cat-file -t` plus `merge-base --is-ancestor <h> master` was run on each of the 7
  hashes: base, `74bda9b7`, `a2208ac7`, `5d5f608f`, `9e27ce0b`, `d687cd6a` and `1dacba59`. All 7
  exist and all 7 are ancestors of `refs/heads/master`. Base is the protocol-identity r96 spot-check
  commit, and the 6 round commits are authored `kake-shokunin`.
- **Lane state.** `scripts/hyaku/jj-lane.sh state …` →
  `branch=master local=remote=1dacba59… ahead=0 behind=0 head=detached tracked=0 untracked=0`.
  `git status --porcelain` printed 0 lines, and `ls-remote origin refs/heads/master` = `1dacba59…`.
- **Prompt fidelity.** The template has 140 lines (`templates/round-prompt.md`). I diffed it against
  lines 1–140 of the dispatched prompt. The only differences are placeholder substitutions
  (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`), so §§1–5 are verbatim. §6 (the hyaku
  addendum) and §7 are appended after them. The prompt was committed at `124d0a58` (17:42:13-03:00),
  before the launch line.
- **Claim–axis fit.** C1 is scored on calibration. Calibration is an owned row of the lane's
  `SCORECARD.md`, held at 2, and is the lowest owned axis. C2 is scored on freshness (HOLD 10) as a
  capability acquisition.

Conformance defects (status-neutral; routed in §6):
- **D-a.** An admitted knowledge entry carries a leaked drafting line.
  `corpus/knowledge/revalidation-exchange.md:130` reads
  ``## Errata sweep (round 97)`; body is 103 words (word-count receipt in quotes-verified.txt, rc 0, count 103). Drafted by ScoutErrata; the L1 integrates it (this seat makes no knowledge-entry edit).``.
  The real `## Errata sweep (round 97)` heading follows at line 132. Line 130 is a malformed duplicate
  heading carrying seat-handoff meta-text inside a corpus entry. The report and lesson do not
  disclose it.
- **D-b.** Seat ReviewReval died with no verdict and was not replaced. The report discloses this.
  As a result, C2 has no dedicated review seat this round. ExecScoreC2 and CriticClaims covered the
  ground, and r96's ReviewReval (24/24) remains on record for the same candidate bytes.
- **D-c.** The §3 planner seat was again held by the L1, because the validator rejects `planner`.
  R97-D2 is carried, and the report discloses it.
- **D-d.** Seat ConnectorScope ran `rm -rf` on the shared round scratch parent mid-wave. The report
  discloses this, and it is mined as Mistake 6 and routed R97-4. No committed byte was affected:
  frozen digests re-hash equal (§2).

## 2. Claim re-checks

### C1 — calibration (HOLD 2 → 3): the `corpus/README.md` coverage index matches the committed knowledge entries — **verifies (re-measured)**

**Independent re-measure.** I wrote my own counter in the closure kernel (it is not the lane's
`c97_index.py`) and ran it over committed bytes through `/usr/bin/git` with `GIT_NO_REPLACE_OBJECTS=1`:
- Population: `ls-tree` of `corpus/knowledge/*.md`.
- Ids: each entry's `source:` line from its first 15 lines, with `S###` ranges expanded.
- Rows: GFM rows of tables that have an `Entry` header, outside fences.
- An entry counts as indexed if some row carries the backticked `knowledge/<file>`, every source id,
  and at least 8 words.

| revision | entries | unindexed | dangling |
|---|---|---|---|
| `36d148f5` (base) | 84 | 38 | 0 |
| `9e27ce0b` (repair) | 84 | 0 | 0 |
| `1dacba59` (tip) | 84 | 0 | 0 |

This reproduces the reported `entries=84 … mismatches=38` → `mismatches=0`. The first five unindexed
entries at base (`cache-control-effective`, `cache-current-age`, `cache-key-conformance-gate`,
`cache-key-construction`, `claim-count-derivation`) match the lane's `base-c1.txt` detail.

**Committed evidence.**
- `controls/after-c1.txt` @`d687cd6a`: `mismatches=0 met=true exit=0`.
- `controls/base-c1.txt`: `mismatches=38 met=false exit=1`.
- `ctl-c1-selftest.txt`: `selftest 14/14`.
- `c97_index.py` sha256 is `8535150e…aa008` at both the freeze `5d5f608f` and the tip, matching
  `controls/instrument-sha256.txt`. The instrument was not touched after the freeze.
- Review conjunct: `cut -f2 w1/ReviewIndex{A,B}/verdicts.tsv | sort | uniq -c` → `19 agree` + `19 agree`
  = 38/38.

**Closure prose spot-read (3/3 agree).** I compared each new row in the `9e27ce0b` README diff
(40 `+|` lines = 38 rows plus a header and a separator) with the entry it indexes:

| row | entry evidence | result |
|---|---|---|
| `cache-current-age` | `source:` S462 (S461 retained) | the row's §4.2.3 integer-second age arithmetic matches the entry's title and scope |
| `cache-key-construction` | `source:` S463 | the row's "no server, CDN or browser" scope matches the entry's `scope:` line |
| `claim-count-derivation` | `source:` S130 | the row matches the entry body |

**Discrimination caveat.** CriticClaims F-C1-1/F-C1-2 showed that the counter also passes a one-row
mega-index and per-entry scope copies. The repair is neither: it has 38 separate rows, each naming one
entry, and that is checked above. The weakness belongs to the instrument, not to this repair, and is
routed as R97-1.

Before → after: 38 → 0 mismatches, re-measured.

### C2 — freshness (HOLD 10), capability acquisition: revalidation exchange, contract v1, first passing counter run — **verifies (evidence-verified counter + independent capability probes)**

**Committed evidence.**
- `controls/after-c2.txt` @`d687cd6a`: `candidate=present hand=37/37 generated=104/104 heldout=57/57
  forgeries_refused=7/7 positive=admitted mutants=14/14 survivors=none anti_table=ok population=ok
  seed=97 met=true`, `exit=0`.
- `ctl-c2-selftest.txt`: `selftest 8/8 … mutants killed 14/14`.
- `ctl-c2-slot-table.txt` (the lookup-table forgery in the candidate slot): `heldout=22/57 met=false`.
- `c97_reval.py` sha256 is `f3895a32…39266` at both the freeze and the tip, matching the pin.

**Predecessor (before).** `c2-predecessor-at-base.txt` ends `NameError: name 'mutants' is not
defined … exit=1`. Reading the committed bytes `36d148f5:.ufo/waves/round-96/c96_reval.py` confirms
that `mutants` is referenced as a free name at the `mutant_cases(...)` call. Before: no verdict.

**Candidate identity.** `scripts/reval_exchange.py` sha256 is `192b3bf7596abad8…` at `36d148f5`,
`5d5f608f`, `d687cd6a` and `1dacba59`. The candidate is byte-identical to the round-96 landing, so the
credited move is the first passing run of a working counter on it. That is the r96 closure's flip
condition (r96 spot-check §3 capability-row reject: "no frozen-counter pass exists"). The SCORECARD
repertoire row (line 5829) says so and names the K1–K4 caveat (CriticClaims F-C2-8), so the row does
not pre-claim.

**Independent capability probe.** I ran the committed candidate bytes with `python3 -I` on 10 inputs
that I chose against RFC 9111 §4.3.1/§4.3.3 and contract v1, including the four classes CriticClaims
showed the counter cannot see:

| probe | candidate | expected | result |
|---|---|---|---|
| etag+LM, no reply | `construct` INM=`"x"` IMS=5 | send both validators (§4.3.1) | ok |
| W/ etag, 304 | `update-stored` | §4.3.3 | ok |
| LM, 502 (K1) | `may-reuse-stored` | 5xx | ok |
| LM, 504 (K1) | `may-reuse-stored` | 5xx | ok |
| etag, 200 | `replace-stored` | full response | ok |
| etag, 101 (K4) | refuse, rc 1 | 1xx refused | ok |
| etag `"a"b"` (K2) | refuse, rc 1 | etagc excludes DQUOTE | ok |
| LM `true` (K3) | refuse, rc 1 | non-negative int | ok |
| no validators | `cannot-revalidate` | — | ok |
| `exists:false` + etag | refuse, rc 1 | contradictory | ok |

Result: 10/10.

**Instrument weaknesses.** These are real and routed; they belong to the instrument and do not
falsify the capability:
- F-C2-1…5: population blindness.
- F-C2-6: `generated=104/104` counts only valid inputs, while contract prose says 120.
- F-C2-7: the mutant clause is a harness self-check.
- MutReval: 3/8 killed.
- SentinelScope: 6 sandbox vectors escaped.

The routes are R97-2 and R97-5. Before → after: no counter verdict (crash) → `met=true` on the frozen
predicate, and the capability is shown correct by independent probes.

### Harm check
`git diff 36d148f5 1dacba59 -- SCORECARD.md` changes only the calibration cell (2 → 3) and appends the
`### Round 97` section. The operability and freshness cells are unchanged.

Non-`.ufo` diff stat:

| file | change |
|---|---|
| `LOG.md` | +8 |
| `SCORECARD.md` | +43 −1 |
| `SKILL.md` | +2 (registry rows 221–222, `c97_index.py` and `c97_reval.py`, both `gate`) |
| `corpus/README.md` | +45 |
| `corpus/SOURCES.md` | +1 |
| `corpus/knowledge/revalidation-exchange.md` | +6 |
| `corpus/lessons/round-97.md` | +103 |

No knowledge or SKILL line was deleted (0 `-` lines). No owned axis is harmed. D-a degrades one
entry's form, but no claim in it is false: the errata paragraph re-verifies (§3).

## 3. Discernment spot-check (non-author; LEARNING.md)

Sample from `corpus/lessons/round-97.md` `## Gate`: 1 admit and 1 reject. I re-opened each source
myself.

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| Row S481 (RFC Editor errata search, RFC 9111) plus the `## Errata sweep (round 97)` paragraph | admit | `curl -sSL https://www.rfc-editor.org/errata_search.php?rfc=9111` → 200 at `https://errata.rfc-editor.org/search/?rfc_number=9111`, 40374 bytes | **agree** | see note 1 |
| merge/kake package adoption (`/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md`) | reject | the package file itself (126796 bytes), with the id extractor `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` run against tip `corpus/SOURCES.md` | **agree** | see note 2 |

Note 1 (S481 admit). The sha256 is `b906ce97…7395`, byte-identical to the committed body
`w1/ScoutErrata/errata-9111.html`. `Section 4.3.4 says:` occurs once. After I stripped the HTML, the
four records read:

| EID | status | section |
|---|---|---|
| 9004 | Reported | §3.5 |
| 9185 | Reported | §4.3.4 |
| 9166 | Held for Document Update | — |
| 7695 | Rejected | §4.3.2 |

There is no erratum on §4.3.1 or §4.3.3, exactly as the row and paragraph state. A `dataset` kind, a
tier-A scope limited to "errata status of §4.3 … as of the fetch", and a 90d recheck are proportionate.

Note 2 (package reject). The package has 129 staged ids. Against the tip registry I get 8 collisions
(S312 S329 S367 S372 S373 S374 S390 S409), equal to the committed `ExecCensus/assimilation/collisions`.
S312 exists on both sides with differently worded scope cells, so a blind append would duplicate ids
with divergent content. Rejecting until a renumber map exists and the entries are re-grounded follows
CORPUS rule 1.

**SOURCES row re-open (S481, tip `corpus/SOURCES.md:227`).** The quote cell is `Section 4.3.4 says:`
(4 words, ≤25). It is located at body line 260 of the retained page and is present in my live
re-fetch. The rest of the row is likewise verified against the bytes I fetched: URL, 302 hop, byte
count, sha256 and the EID-to-section mapping.

**Registry counts.** Base: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` gives 217, and
the tip gives 218, a delta of +1 (S481). This matches the report.

**Census.** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → rc 0, final
line `kake ok …/corpus/SOURCES.md`. Every other line is the pre-existing W04 duplicate-URL class, with
no E-class finding.

Spot-check result: agrees with the gate on the sampled admit and the sampled reject.

## 4. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| calibration | **improved** | C1 re-measured independently 38 → 0 at base/tip; 38/38 review; 3/3 closure prose reads; score 2 → 3 |
| freshness | **improved** | C2 capability row enters on its first frozen-counter pass (evidence-verified, pins intact) on a candidate that the closure probed independently, 10/10 including K1–K4; score HOLD 10 |
| operability | **unchanged** | no operability claim; cell unchanged |

## 5. Trend verdicts (closure)

| trend | verdict | evidence |
|---|---|---|
| expansion | **improved** | One tier-A `mined` row (S481, re-opened byte-identical) plus an errata section on ground the map did not hold (errata status of RFC 9111 §4.3). One capability row admitted to SCORECARD on a demonstrated pass. Census rc 0. |
| quality | **improved** | 38 coverage-index rows now match their entries (independently re-measured; review 38/38). The routed R96-1 crash class is closed with a pinned successor. No admitted entry failed its re-check. D-a is a form defect, not a false or stale claim, and is routed. |
| discernment | **improved** | This outside spot-check agrees with the gate on both the sampled admit (S481) and the sampled reject (package adoption). The lane's own attack seats falsified the lane's instruments, and the lane recorded and routed those findings instead of hiding them. |

## 6. Routed defects (kake must fix in round 98)

- **R98-D1 (closure-routed; D-a).** Delete the leaked drafting line
  `corpus/knowledge/revalidation-exchange.md:130`, the malformed duplicate `## Errata sweep (round 97)`
  heading with the ScoutErrata handoff text. Add a check that fails when a wave integration copies
  seat meta-text ("Drafted by", "this seat", "word-count receipt") into `corpus/knowledge/`.
  Record the fix in LOG.md as a correction.
- **R98-D2 (closure-routed; D-b).** Make a dead review seat on a claim either replaced within the
  wave, or have the report name which surviving seat carries that claim's review.
- **R97-1…R97-5, R96-3, R95-6, R95-2 (L0)** stay as the lane routes them in
  `corpus/lessons/round-97.md` `## Routed to round 98`. The closure adds none and removes none. This
  includes the C2 population/denominator fix (F-C2-6: score refusals against the contract's 120)
  and the sandbox vectors.
- **R97-D2 (driver/validator-side)** is unchanged: the §3 `planner` role is still rejected by the
  validator.

## 7. SHONEN observation for the operator (promotion is operator-owned)

A non-author cannot check every box. Box 2 ("end-to-end domain task executed and logged") is `[ ]`,
which the lane reports and its shonen ledger shows. Boxes 1, 3 and 4 are `[~]`, with pointers. No
promotion recommendation.
