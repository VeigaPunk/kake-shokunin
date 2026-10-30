# ScribeCensusNarrative — round 64 Sources census narrative vs receipts

Seat: `ScribeCensusNarrative` (leaf; no subagents). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Lane HEAD observed: `cc8add1fa740b920ea5179a71152680ab220c70c`. Base `1a48131577ba82c967650561be34e8dba909432a`. T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`.
Scope: `corpus/lessons/round-64.md` §"Sources census" (lines 103–110) against `.ufo/waves/round-64/controls/census-before.txt` and `census-after.txt`, and the `corpus/SOURCES.md` no-change claim.

## Verdict

**Admit with one narrative correction.** The census numbers and the "no row added or changed" claim are true. The lesson's arrow `→ 171 rows, 16 W04 …, exit 0` attributes the row count to a receipt that does not contain it. The receipts contain the W04 warnings and the exit code, but not "171" or any row count. Correct the lesson sentence or add a pointer to the command that produces 171. Do not edit the lesson in this seat.

## Claim-by-claim

| # | Lesson claim (`corpus/lessons/round-64.md`) | Evidence | Result |
|---|---|---|---|
| 1 | Command: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (line 106) | Ran it live (below). Stdout is identical to both receipts, excluding the exit line. | matches |
| 2 | Exit 0 (line 107) | live exit 0; `census-before-exit=0` (receipt line 18); `census-after-exit=0` (receipt line 18) | matches |
| 3 | 16 W04 cross-scope duplicate-URL warnings (line 107) | `grep -c $'\tW04\t'` on live output = 16; `grep -c` on census-before.txt = 16; on census-after.txt = 16 | matches |
| 4 | **171 rows** (line 107), attributed to the validate command's output | `validate` mode prints no row count (its output is only `E*`/`W*`/`ok` lines; the `rows` metric exists only in `census` mode, `sources-census.sh:691,768`). `grep -n '171\|rows' controls/census-before.txt` and `census-after.txt`: **no match** (grep exit 1 on both). | **drift: narrative attributes a number to a receipt that does not record it** |
| 5 | 171 rows is true | live `census` mode: `kake rows 171` (exit 0); `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` = 171; same count at 1a481315, 4c8295fa, cc8add1f | matches |
| 6 | "No `corpus/SOURCES.md` row was added or changed this round" (lines 108–109) | `git diff 1a481315 4c8295fa -- corpus/SOURCES.md` → 0 bytes (exit 0). `git diff 4c8295fa cc8add1f -- …` → 0 bytes. `git diff --stat 1a481315 4c8295fa -- …` → empty. Blob `3993185e5eb13ed51cd32ffd21b20c3a2815a261` at all of 1a481315, 4c8295fa, cc8add1f. Worktree `git status --porcelain -- corpus/SOURCES.md` → empty. | matches |
| 7 | "recorded 2026-10-30 before any registry edit" (line 107–108) | The receipt has no timestamp, command or revision header (it begins at the `kake` row). It was first committed in `4c8295fa` (2026-10-30T08:00:22-03:00), the same commit as the registry-neutral build. "Before" is not self-attested by the receipt. It is supported indirectly: the registry bytes are identical from base through HEAD, so no edit could have occurred in the round. | matches in substance; receipt does not self-verify the timing label |
| 8 | "the round-end census output is pasted in the round report" (lines 109–110) | No round-64 report file exists in the committed tree at `cc8add1f` (`git ls-tree -r --name-only cc8add1f | grep round-64` lists only the contract, controls, fixtures, sources and `corpus/lessons/round-64.md`). The untracked `.ufo/waves/round-64/w1/` seat reports are the only other round-64 narrative. | pointer target not present in committed tree; see finding F2 |

## Live reproduction (exact commands and output)

Scratch: `/fast/scratch/hyaku/kake-r64/ScribeCensusNarrative/` (removed before yield; see cleanup).

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake > live-validate.out 2> live-validate.err; echo exit=$?
exit=0
$ cat live-validate.out
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
kake	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
kake	W04	S427 duplicate url developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers across scopes
kake	W04	S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
$ cat live-validate.err   → (empty)

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake; echo exit=$?
kake	rows	171
kake	tier.A	148
kake	tier.B	6
kake	tier.C	17
kake	status.mined	141
kake	status.queued	8
kake	status.rejected	22
FLEET	rows	171
FLEET	tier.A	148
FLEET	tier.B	6
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	141
FLEET	status.rejected	22
FLEET	status.invalid	0
FLEET	missing	0
exit=0
```

Receipt comparison:

```
$ diff <(grep -v '^census-before-exit' controls/census-before.txt) live-validate.out            → IDENTICAL
$ diff <(grep -v '^census-after-exit'  controls/census-after.txt)  live-validate.out            → IDENTICAL
$ grep -c $'^kake\tW04\t' controls/census-before.txt controls/census-after.txt
controls/census-before.txt:16
controls/census-after.txt:16
$ grep -n '171\|rows' controls/census-before.txt controls/census-after.txt; echo grep-exit=$?
grep-exit=1
```

Registry byte identity (paths relative to the lane):

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a481315 4c8295fa -- corpus/SOURCES.md | wc -c      → 0
$ git -C … diff 4c8295fa cc8add1f -- corpus/SOURCES.md | wc -c                                             → 0
$ git -C … diff 1a481315 cc8add1f -- corpus/SOURCES.md | wc -c                                             → 0
$ git -C … rev-parse 1a481315:corpus/SOURCES.md 4c8295fa:corpus/SOURCES.md cc8add1f:corpus/SOURCES.md
3993185e5eb13ed51cd32ffd21b20c3a2815a261  (×3)
$ git -C … status --porcelain -- corpus/SOURCES.md                                                         → (empty)
$ grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md   → 171 ; sha256 63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2
```

Receipt-pair diff: `census-before.txt` and `census-after.txt` differ only at line 18 (`census-before-exit=0` vs `census-after-exit=0`), confirmed by `git diff` output at `cc8add1f`.

## Findings

**F1 — drift (narrative vs receipt), line 107 of `corpus/lessons/round-64.md`.** The sentence `Round-start census: <validate command> → 171 rows, 16 W04 cross-scope duplicate-URL warnings, exit 0` presents "171 rows" as the output of the cited command and implies the receipts record it. They do not: `validate` never prints a row count, and neither `controls/census-before.txt` nor `census-after.txt` contains `171` or `rows`. The 171 comes from `census` mode (`kake rows 171`) or the frozen manual `grep -cE` count (171); both reproduce it, so the number is correct but its provenance in the lesson is wrong. Suggested narrow fix (for the integrator; not applied here): either cite `sources-census.sh census --root … kake` (or the `grep -cE '^\| S[0-9]{3,}'` manual count) for the 171, or state that the receipts carry the 16 W04 lines and exit code only. Impact: none on the registry claim; it is a provenance precision issue in the census narrative.

**F2 — pointer to an uncommitted artifact, lines 109–110.** "the round-end census output is pasted in the round report" points to a round report that is not in the committed tree at `cc8add1f`. The only round-64 receipts are the two census files, which carry no separate round-report copy. The pointer is unverifiable from the committed tree; the receipts themselves are the verifiable evidence. Suggested fix: name the receipt paths instead of "the round report", or commit the report.

**F3 — unverifiable timing label, lines 107–108.** "recorded 2026-10-30 before any registry edit" is not self-attested: `census-before.txt` has no timestamp, command or revision header. Its ordering claim is supported only indirectly by the byte-identical registry from base through HEAD. This does not contradict the lesson; note it as a receipt-format gap. (Contrast the round-21 census receipt, which carries `command:` and `revision:` headers.)

**F4 — no drift found.** Row count (171, verified three ways), W04 count (16 in both receipts and in a fresh run), exit codes (0 in both receipts and live), "no row added or changed" (registry blob identical across base, T0 and HEAD; empty diff) all match. Also cross-checked against `.ufo/waves/round-64/w1/ExecCensusCommands.md:40-42`, `ScoutCensusState.md:22-27`, `ReviewerContract.md:75-96`, `ReviewerCensusDiscipline.md:15-36` — each reports the same numbers and byte-identity; none contradicts the lesson.

## Out of scope (observed, not adjudicated)

- The seven-command frozen manual census (`CORPUS.md` §"SOURCES.md — where a shokunin learns") is not recorded in the committed receipts; its results (A=148/B=6/C=17, mined=141/queued=8/rejected=22, 0 malformed) appear only in seat reports. This is consistent with F1.
- `ExecSweepSections.md` reports `§paths 172` versus a required 171 — a sweep-count matter for another seat, not the census.

## Tools installed or updated

None. No `pacman`, `uv tool`, `npm -g`, or binary install performed. `/home/vgpnk/.omp/agent/RULES.md` does not exist at the path I attempted (`/home/vgpn/.omp/agent/RULES.md` was a typo on my first attempt; the correct path `/home/vgpnk/.omp/agent/RULES.md` returned the tooling directive, which I followed by installing nothing).

## Mutation and write discipline

- Only write: this report, at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/w1/ScribeCensusNarrative.md`.
- No mutating git/jj command run. Only `git diff`, `git rev-parse`, `git show`, `git log`, `git ls-tree`, `git status --porcelain` (read-only).
- Lane working tree untouched. Lesson, receipts, counters, contract and SOURCES.md not edited.
- Scratch: `/fast/scratch/hyaku/kake-r64/ScribeCensusNarrative/` held three captured outputs (`live-validate.out`, `live-validate.err`, `live-census.out`); the content is reproduced in full above, and the directory is removed before yield.
