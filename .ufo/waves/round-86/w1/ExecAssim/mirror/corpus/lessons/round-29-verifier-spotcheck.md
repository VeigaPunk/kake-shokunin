author: hyaku closure (non-author integrator, @m_opus)

# Round 29 non-author verification: both declared claims verify; admitted

Runtime model as exposed to this closure session: `anthropic/claude-opus-5-5`
(task route `@m_opus`; no model parameter passed). Fresh closure subagent
`HyakuCloseKake29`, dispatched by the hyaku orchestrator, not by the lane.
Base `fe1805cf32a7aadf4574637a3a8912354cee2c7b`, head
`234524cdc06167ad14477e0956a8786cc3fc752d`, branch `master`. Judged on
committed bytes only. No optional review seats were dispatched; every check
below was run by this closure.

Driver digest (copied from `.ufo/watchdog.log`, which is mutable):

```
2026-10-22T07:22:41-03:00 launch kake round=29 pgid=3879740 driver=hyaku-inline attempt=1
2026-10-22T08:38:46-03:00 complete kake round=29; hyaku-inline attempt=1
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane | `git log --format='%an <%ae> %H %s' -- .ufo/reports/round-29/kake.md` (fleet) | `kake-shokunin <kake@shokunin.local> 1458dabc06dbb2cb28082f7812e8311fb49b8b06 round-29: kake report`, committed 08:38:20-03:00 | pass |
| `SHONEN` heading, one line per box | read report lines 149-154 | 4 lines, all `[~]`, one per `SHONEN.md` box | pass |
| Cited hashes exist and are ancestors | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for the 8 cited commits and the base | `ok` ×9 | pass |
| Report filed after its commits | committer dates | lane tip 08:37:17, report 08:38:20, completion 08:38:46 | pass |
| Lane pushed, nothing left over | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `ahead=0 behind=0 … tracked=0 untracked=0`; porcelain empty | pass |
| Prompt carries the template contract | every non-placeholder line of `templates/round-prompt.md` searched in `.ufo/prompts/kake-round-29.md` | 116/116 present; hyaku addendum §6 at prompt line 141 | pass |

Observation (no defect): `d18bbf3` has author date 07:05:08-03:00, before
the 07:22:41 launch, and committer date 07:28:41-03:00, after it. The
committer date is the one that orders the declaration before the
implementation commits `f8675e5` (07:46:29) and `98dbab2` (07:53:52). The
early author date is consistent with jj stamping a change when it is
created [INFERENCE].

## Claims

Re-measured: C1 (lane counter re-run at base and head, plus an independent
quote sweep over the entry). Evidence-verified: C2 (it rests on the lane's
gate `scripts/base_path_audit.py`; per PROTOCOL §Gate standard, Closure
consequence, this closure did not execute the gate, its selftest or the C2
counter, which runs the gate).

### C1 — freshness: base-path entry on S040–S043, 0/4 → 4/4

- Declaration frozen before the work: `d18bbf3:SCORECARD.md` carries the C1
  row (before 0/4, after 4/4). The counter blob is
  `139ede1efbbfeed612201239a4244b43aeda855d` at `d18bbf3`, `d8cd2e4` and
  `234524c` (`git rev-parse <rev>:.ufo/waves/round-29/c1_quote_truth.py`).
- `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision fe1805cf…`
  → `{"passed":0,"total":4,"controlBroken":false}`, exit 1.
- Same at `234524cdc06167ad14477e0956a8786cc3fc752d` → `{"passed":4,"total":4,"controlBroken":false}`,
  exit 0; all four ids pass, and the one-letter control is not found.
- Independent re-derivation: all 23 curly-quoted spans in
  `corpus/knowledge/pages-base-path.md` at `234524c` are exact substrings
  (whitespace collapsed) of the retained text of the source they cite. Each
  retained text's sha256 matched its `receipts.json` `textSha256` (23
  quotes; 0 not found under the cited id).
- Live re-open (one ordinary GET each, 2026-10-22 ~11:35Z): the body sha256
  of S040, S041, S042 and S043 is identical to the receipt `bodySha256`
  (`fac40d86…`, `1e3149a8…`, `610d127b…`, `be274bde…`).
- Sentence support (the counter does not test it): the entry's
  uncited statements about URL resolution, the base element and rebuild
  needs carry `[INFERENCE]`. The quoted Jekyll and Vite remedies read as the
  pages say (S042 Relative/Absolute URL rows; S043 GitHub Pages step 1 and
  step 2, re-read live).
- **Verdict: verifies at the declared value (4/4).** Axis freshness:
  `improved`.

### C2 — operability capability: `scripts/base_path_audit.py`, 0/30 → 30/30

- Declaration frozen in `d18bbf3` (before 0/30, after 30/30 with all three
  constant gates rejected). The counter blob `58dde0628c3e…` and the matrix
  blob `0687433ecd7c…` are the same at `d18bbf3`, `d8cd2e4` and `234524c`.
- Before: `git cat-file -e fe1805cf:scripts/base_path_audit.py` → path not
  in `fe1805cf`; tool absent, so 0/30 holds trivially. Committed receipt
  `c2-before-fe1805c.json`: `passed 0, total 30, toolPresent false`.
- Matrix: `jq '.cases|length' c2-matrix.json` → 30; `sha256sum` →
  `75c08f64…2e84a`, equal to `MATRIX_SHA256` pinned at
  `c2_matrix_count.py:28`.
- After (committed evidence): `c2-after-d8cd2e4.json` → `revision d8cd2e45…`,
  `passed 30, total 30`, byKind control 7/7, defect 14/14, input 8/8, usage
  1/1, constant gates 7/30, 0/30, 7/30, `constantGatesAllRejected true`,
  `toolSha256 c5a13a32…1dc0`. `git show 234524c:scripts/base_path_audit.py | sha256sum`
  → `c5a13a32…1dc0`, and `git diff --stat d8cd2e4 234524c` touches only
  receipts, `LOG.md` and `SCORECARD.md`, so the d8cd2e4 measurement grades
  the tip's tool bytes.
- Selftest (capability, not measurement): `selftest-lane-final.json` →
  `45/45, failed 0, verdict clean`, 45 case names; `git ls-tree -d
  234524c scripts/fixtures/base-path/ | wc -l` → 45. The receipt names no
  revision or tool digest; X01–X15 exist only from `d8cd2e4`, and X15 tests
  the same-scheme fix made in `d8cd2e4`, so the receipt was taken over
  the repaired tool [INFERENCE].
- Registry home: `SKILL.md` "Base-path audit gate registry — round 29" (line
  721+) has the row: gate, entry command, verdict map 0/1/2/64, selftest
  command, fixture path.
- Capability row and demonstration: SCORECARD `## Capabilities` row
  "Offline project-site base-path audit", first-working round 29, cites the
  C2 receipt, the selftest and the real-input run
  (`real-input/out/summary.json`: 3 sites, 3 pages, 114 references, 4
  findings, exits 1/0/1). That run was committed in `98dbab2` with the
  earlier tool (`e5167fa`). The only behavioural change after it
  (`git diff 98dbab2 d8cd2e4 -- scripts/base_path_audit.py`) is resolution
  of a same-scheme reference with no `//`. A grep for such references in the
  three snapshot pages finds 0 per page, so the demonstration's numbers
  cannot be changed by that change [INFERENCE from the diff and the grep; the
  tool was not run].
- **Verdict: verifies at the declared value (30/30, constant gates
  rejected), evidence-verified.** Axis operability: `improved` (capability
  added).

### No-harm

- `git diff fe1805cf 234524c -- SCORECARD.md`: additive only (+62/−0); axis
  ratings stay 10/10; one capability row and two round-29 sections added.
- `git diff --numstat`: the only removed lines in the round are 3 in
  `PROVINCE.md`, where the Frontier sentence moves "Jekyll/base-path build
  tooling" from open to held ground, with an appended round-29 section.
  That is accurate to what landed.
- `corpus/SOURCES.md`: 0 removed rows; S001–S039 unchanged; rows 39 → 48.
- `corpus/knowledge/`: one file added, none modified.
- `SHONEN.md` untouched (no `[x]`).
- Census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  → `kake W04 S033 duplicate url …rfc9110.txt across scopes` /
  `kake ok …/corpus/SOURCES.md`, exit 0. This is identical to the lane's
  committed before and after receipts; the W04 predates the round.

Per-axis verdicts: operability `improved`; freshness `improved`; depth,
coverage, calibration, adjacency `unchanged` (not owned, not claimed).

## Discernment spot-check

The `## Gate` in `corpus/lessons/round-29.md` records 10 identified sources,
9 opened, 9 screened: 4 mined, 3 rejected, 2 queued, and 1 not opened
(Stack Overflow 403 challenge). The `SOURCES.md` round-29 search log matches.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S042 Jekyll Liquid filters | admit (`mined`, tier A) | https://jekyllrb.com/docs/liquid/filters/; body sha256 `610d127b…` identical to receipt | agree | Jekyll's own docs (v4.4.1, modified 2026-10-13). The Relative URL row reads "Prepend `baseurl` config value to the input to convert a URL path into a relative URL. This is recommended for a site that is hosted on a subpath of a domain." It is primary for the filter semantics the entry uses, and the scope cell is narrow and correct |
| S043 Vite static deploy | admit (`mined`, tier A) | https://vite.dev/guide/static-deploy.html; body sha256 `be274bde…` identical to receipt | agree | Vite's own docs. The GitHub Pages step 1 states `base` `'/<REPO>/'` for a project site and `'/'` for a user site or custom domain. The scope cell rightly limits it to a bundler rule, not to Pages serving |
| S044 Made Mistakes, site.url and baseurl | reject (tier C) | https://mademistakes.com/mastering-jekyll/site-url-baseurl/; one GET, HTTP 200, body sha256 `54da0212…` identical to the screened receipt | agree | The served page dates from Jul 19, 2021. It calls Jekyll 4.2 "✨latest" and states "It is currently locked at 3.9.0" (raw HTML), while lane row S016 lists 3.10.0. Its example `_config.yml` uses `website:` / `basewebsite:`, not `url`/`baseurl`, as the row says. Its useful content is carried by the primary S041/S042. The flip condition is checkable |

New `SOURCES.md` row re-opened with its quote: **S043**. Gate quote “If you
are deploying to https://<USERNAME>.github.io/<REPO>/ (eg. your repository is
at https://github.com/<USERNAME>/<REPO> ), then set base to '/<REPO>/' .” is
25 words and is an exact substring of the retained text. The live page reads
the same sentence with `<code>` spans: the only differences are the spaces
that tag removal leaves, which the lesson discloses. The row's anchor (GitHub
Pages section, Update Vite Config step) and teaches cell match the page.
Agree.

The spot-check agrees with the gate on both admits and the reject.

## Routed round-28 defects

- (1) citing-set fixtures and (2) round-27 families: **carried as named
  debt, not dropped.** `corpus/lessons/round-29.md` "Not repaired this round
  (routed defects 1 and 2)" names both and restates their terms. The report
  lists them under Open items. Two `QUALITY.md` criteria (lines 346, 362)
  state the open failure. My re-measure matches the lesson's numbers:
  `git ls-tree -d 234524c scripts/fixtures/citing-set/ | wc -l` → 29;
  `git grep -l reason 234524c -- scripts/fixtures/citing-set | wc -l` → 0;
  the citing-set fixtures and `scripts/citing_set.py` are untouched. The
  stated reason (session drift sentinel, `.scratch/goal-20261022-hyaku-12h.md:173`:
  rounds 27 and 28 both worked the citing-set surface) is accurate. Both
  items stay open on the routed-defect queue.
- (3) Addressed in this round's own counters (quote truth with sha256 check;
  reason tuples), not on the citing-set surface.
- (4) Addressed: 3 rejects from the gate itself.
- (5) Addressed: `.gitignore` adds `__pycache__/` and `*.pyc`;
  `.ufo/waves/round-26/__pycache__` no longer exists.

## Seat incidents and installs (rulings)

- `NoHarmExistingGates` ran `freshness-sweep.mjs` with no section flag at
  base and at tip. That sends GET requests to the lane's pinned owned sites
  and `git ls-remote` to pinned repositories. **Ruling: a boundary breach by
  a lane seat, disclosed by the seat (`w2/NoHarmExistingGates.md` finding 1)
  and by the lesson and report.** Its live results are declared unverified,
  and no claim evidence rests on them. It is status-neutral and routed below.
- `HtmlParsingEdges` ran the pre-installed Chromium headless with
  `--dump-dom` on 16 local `file://` pages, with proxy 127.0.0.1:9 and DNS
  mapped to NOTFOUND (`w2/HtmlParsingEdges.md:72`). **Ruling: within
  bounds.** It was a read-only local parsing oracle: no remote surface, no
  challenge or access control, and no browser-domain work absorbed from tabi.
- Installs: parse5 8.0.1 via `npm install --prefix` into the seat sandbox
  (not global). GNU time 1.9 built from the official GNU tarball
  https://ftp.gnu.org/gnu/time/time-1.9.tar.gz into `~/.local/bin/time`;
  `~/.local/bin/time --version` → `time (GNU Time) 1.9`. The only build
  change was the compile flag `-std=gnu11`. Both use official sources, no
  piped script and no pacman, which is consistent with the operator tooling
  directive (`~/.omp/agent/RULES.md`). This closure installed nothing.

## Trend verdicts

- **expansion: improved.** The admitted entry `corpus/knowledge/pages-base-path.md`
  is on ground the coverage map listed as open Frontier. The new
  `corpus/README.md` coverage row is "Project-site base paths (r29)". Every
  `source:` id (S040–S043) is a `mined` row opened this round. A capability
  row was added (C2).
- **quality: unchanged.** The LEARNING observable is existing entries
  re-verified, deepened or superseded. No pre-existing knowledge entry was
  modified or re-verified (`git diff --name-only fe1805cf 234524c --
  corpus/knowledge` → the one added file), and the report says so. The
  stronger counters (quote truth, reason tuples) improve measurement, not
  held entries. No entry was found false and left unmarked, so the trend is
  not harmed. This differs from the lane's self-verdict `improved`.
- **discernment: improved.** This outside spot-check agrees with the gate
  on two admits (S042, S043) and one reject (S044). The reject sample comes
  from the source gate itself (round-28 defect 4 closed). The new
  `QUALITY.md` criteria are grounded in the round-28 spot-check's routed
  defects 1 and 3.

## Admission

Both declared claims verify at their declared values. Their targets were
frozen in `d18bbf3` before measurement. No owned axis is harmed.
**Admitted.** Capability added: "Offline project-site base-path audit"
(`scripts/base_path_audit.py`). No promotion, mint, SHONEN `[x]` or state
advance is made here.

For the operator: all four SHONEN boxes look checkable by a non-author
from committed bytes. Box 1: SKILL "Project-site base-path triage — round
29" rows cite S040–S043 and S024. Box 2: the `LOG.md` round-29 entry plus
the real-input run. Box 3: tool `--help` and the registry row. Box 4: the
PROVINCE frontier update. Promotion is operator-owned.

## Routed defects (kake, next round)

1. Round-28 routed defects 1 and 2 (citing-set fixtures asserting reason
   codes; round-27 families) remain open. The next citing-set round must
   land them or carry them again by name.
2. Wave context must bar `freshness-sweep.mjs` without a section flag (or
   any live mode) for falsify seats, since it reaches owned sites. Name the
   allowed offline flags in the seat item.
3. Evidence receipts should name what they measured. `selftest-lane-final.json`
   and `real-input/out/summary.json` carry no revision or tool digest. Re-run
   the real-input demonstration at the current tool bytes and record the
   tool sha256 in the summary.
4. The report and SCORECARD say C1/C2 were "re-measured at `7697990`" (and
   the report adds `234524c`), but no receipt for those revisions is
   committed. Commit receipts for every revision named, or name only the
   receipted ones.
5. Open C2 counter limits stay listed: `id`, `page`, `resolved` and counts
   are not compared, and the usage case passes on exit code alone. Tool
   gaps are named in its docstring.
