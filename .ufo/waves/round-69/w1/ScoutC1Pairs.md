# ScoutC1Pairs — recorded integer count claims, rounds 67–68 (kake, round 69 W1)

Scope: leaf enumeration + re-run. Read base `4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4`
(`git cat-file -t` = commit). Lane tree unmodified (`git status --porcelain` shows only
round-69 wave untracked paths). No clone/fixture/scratch needed, so none created.
Artifacts: `ScoutC1Pairs/pairs-candidate.json` (schema exactly `{id, record_path,
record_locus, rev, path, command, recorded_value, observed_value, match}`; all `rev` full
40-hex; every command single-stage `git -C <lane> show <rev>:<path> | grep -c '<pat>'` or
`... | wc -l`) and `ScoutC1Pairs/pairs-run.txt` (per-pair receipt: exit 0/1, no fatal stderr).
cwd for every run: `/home/vgpnk/Projects/shokunin/kake-shokunin`. `grep` exits 1 iff count 0.
Read set at the base only: LOG.md lines 2301–2325, `corpus/lessons/round-67.md`,
`round-68.md`, `round-68-verifier-spotcheck.md` (read only), SCORECARD.md 4655–4699.

## 20 pairs — 19 re-derive, 1 does not

| id | rev | path | recorded | observed | verdict |
|---|---|---|---|---|---|
| C1-01 | `6ff73edd1` | gate-status-ledger.md | 5 | 5 | MATCH |
| C1-02 | `4b03efe1e` | gate-status-ledger.md | 1 | 2 | **MISMATCH** |
| C1-03 | `6ff73edd1` | SKILL.md | 0 | 0 | MATCH |
| C1-04 | `4b03efe1e` | SKILL.md | 1 | 1 | MATCH |
| C1-05 | `6ff73edd1` | SKILL.md (`wc -l`) | 1377 | 1377 | MATCH |
| C1-06 | `4b03efe1e` | SKILL.md (`wc -l`) | 1396 | 1396 | MATCH |
| C1-07 | `6ff73edd1` | publish-queue.md | 0 | 0 | MATCH |
| C1-08 | `4b03efe1e` | publish-queue.md | 1 | 1 | MATCH |
| C1-09 | `6ff73edd1` | corpus/SOURCES.md | 171 | 171 | MATCH |
| C1-10 | `4b03efe1e` | corpus/SOURCES.md | 172 | 172 | MATCH |
| C1-11 | `396128196` | gate-status-ledger.md | 2 | 2 | MATCH |
| C1-12 | `099923320` | gate-status-ledger.md | 2 | 2 | MATCH |
| C1-13 | `d69b720f5` | gate-status-ledger.md | 1 | 1 | MATCH |
| C1-14 | `ce2ba6547` | gate-status-ledger.md | 1 | 1 | MATCH |
| C1-15 | `17072048d` | gate-status-ledger.md | 1 | 1 | MATCH |
| C1-16 | `396128196` | publish-queue.md | 0 | 0 | MATCH |
| C1-17 | `ce2ba6547` | publish-queue.md | 1 | 1 | MATCH |
| C1-18 | `17072048d` | publish-queue.md | 1 | 1 | MATCH |
| C1-19 | `396128196` | corpus/SOURCES.md | 172 | 172 | MATCH |
| C1-20 | `17072048d` | corpus/SOURCES.md | 173 | 173 | MATCH |

`record_locus` per pair (in the JSON): C1-01/02 LOG.md:2304 + round-67.md:53-54 +
SCORECARD.md:4664; C1-03/04 LOG.md:2305 + round-67.md:59-60 + SCORECARD.md:4665;
C1-05/06 LOG.md:2305 + round-67.md:59 + SCORECARD.md:4665; C1-07/08 LOG.md:2306 +
round-67.md:72 + SCORECARD.md:4666; C1-09/10 LOG.md:2308 + SCORECARD.md:4671;
C1-11 LOG.md:2333 + round-68.md:31-32 + SCORECARD.md:4688 + spotcheck:46; C1-12 LOG.md:2333 +
round-68.md:31-32 + spotcheck:47; C1-13 LOG.md:2390 + round-68.md:36 + spotcheck:48;
C1-14 LOG.md:2390 + round-68.md:36 + SCORECARD.md:4688 + spotcheck:48; C1-15 spotcheck:49
(command at spotcheck:42); C1-16 LOG.md:2355 + round-68.md:54 + SCORECARD.md:4689 +
spotcheck:81; C1-17 LOG.md:2355 + round-68.md:54 + SCORECARD.md:4689 + spotcheck:81;
C1-18 spotcheck:81; C1-19/20 LOG.md:2369 +
SCORECARD.md:4698 + spotcheck:147-148. Pattern: `not adjudicated here\|candidate mechanism`
(BRE), `c66_gate_status_hostportable`, `r67 dated`, `r68 dated`,
`^|[[:space:]]*S[0-9][0-9][0-9]*[[:space:]]*|` (BRE registry form; the spotcheck's ERE
`^|[[:space:]]*S[0-9]{3,}[[:space:]]*|` gives the same 172/173, so C1-19/20 are
dialect-independent).

Mismatch detail (C1-02): at `4b03efe1` the ledger has two matching lines — line 44
`| c55_quote_truth | historical | …` and line 47 `| c56_selftally | live | …`, whose closing
sentence then read "The r65/r66 PYTHONUTF8 **candidate mechanism** is REFUTED." The BRE
pattern self-matches the round's own row — the mechanism S435 documents. At `ce2ba654`
(C1-14) the rewording leaves one match. For C1's frozen rule this means the r67 end-state
value `1` is unreachable at `4b03efe1`: C1-02 needs a correction row naming re-derived 2
for `unrelabelled=0` to be attainable.

## Rejected (not a single-stage count at a named revision)

| claim (record) | reason | value measured anyway |
|---|---|---|
| "5 → 2 at every r67 revision" (LOG.md:2319; round-68.md:10) | prose summary, no command | 2 at `3961281`/`099923320`/`4b03efe1`/`b569bb63`; 5 at `6ff73edd` |
| S133 "11" → 10 words; S434 "16" → 26 (round-67.md:105,109; round-68.md:117,120) | `wc -w` over quote text, not a committed path | 10; 26 full / 22 sub-quote |
| raw-substring `grep -c` = 1 / 0 (spotcheck:134-135) | bodies named, no revision, no `show` | 1 (`S434-naming.html`), 0 (`subprocess.html`) at `4b03efe1` |
| "diff = exactly 2 lines" (LOG.md:2339; round-68.md:36) | range diff, not `show <rev>:<path>` | numstat 2/2; `diff \| wc -l` = 22 |
| `members=28 … agreement=17/18 … structural=0` (LOG.md:2304,2311) | counter stdout, needs the c66 script | not run (out of scope) |
| `events=25 undisclosed=6`, `19→25` (LOG.md:2304) | JSON field counts, no recorded command | not run |
| `pathsFiles 177→179`, `files +0/-0` (LOG.md:2311) | pins-diff scan | not run |
| `16 W04` census warnings | tool output, not a path count | not run |
| canonical-tag counts (spotcheck:84-85) | record elides the body path (`…charter….body`) | 1 and 0 at `17072048`, consistent |
| `selftest 10/72`, `rc 128 vs 0`, `9009` (round-67.md §Mistakes) | host-bound runs, no pinned command | not run |

- 20 pairs found (>=3 minimum); no duplicate `(rev, path, command)` (asserted by the writer).
- `b569bb638` (LOG.md:2317) is not an object name (`git rev-parse` fails): the D-1 drift, not a pair.
- Tool installs: none; pacman not invoked; no network access.
