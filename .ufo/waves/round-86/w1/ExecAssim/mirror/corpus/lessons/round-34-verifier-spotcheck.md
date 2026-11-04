author: hyaku closure (non-author integrator, @m_opus)

# Round 34 — verifier spot-check (kake)

Round: kake 34, L1 `KakeR34`, hyaku in-session, attempt 1. Base
`1e54c89515b0b1f7c9d7d10e6232d15e43320713`; lane tip
`ce72dd1b31673f62c54e4663ffa9723a53caf79d`. Report `.ufo/reports/round-34/kake.md`
(fleet commit `6d7e9971636d00e0decb63bab2f2e59aefc4b19a`).

Driver digest (copied from `.ufo/watchdog.log`, lines 761 and 769):
- `2026-10-22T17:52:50-03:00 launch kake round=34 pgid=3998466 driver=hyaku-inline attempt=1`
- `2026-10-22T18:35:18-03:00 complete kake round=34; hyaku-inline attempt=1`

Closure seats (read-only, dispatched by the closure, not by the lane): `ReopenGateSources`,
`ReadLinkPreviewTool`, `ReadEntryVsHollow`. Held items `KakeR31.CriticC1Counter` and
`KakeR31.CriticSandboxThreatModel` were not recreated.

What the closure executed, and where: the orchestrator asked for a ruling on what the landed tool
and entry do, measured by the closure. So the closure ran both declared counters, the landed tool
and the two retained control commits. All of these ran in a sandbox clone
`/tmp/kake-r34-close/lane`, detached at `ce72dd1b`, with the control bundles fetched into it.
Nothing ran in the lane checkout. The lane selftest and criteria checks were not run; their
committed receipts were verified instead.

## Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-34/kake.md` | `kake-shokunin kake@shokunin.local 6d7e9971636d00e0decb63bab2f2e59aefc4b19a` | pass |
| prompt committed | `git log --format='%an %H' -- .ufo/prompts/kake-round-34.md` | `kake-shokunin 7b1c1e8493ddd2daddebb53d277f51c5c443c1e9` | pass |
| SHONEN heading, one line per box | report §SHONEN; `grep -c -E '^- \[[ x~]\]' SHONEN.md` | 4 lines, all `[~]` with pointers; SHONEN.md has 4 boxes | pass |
| cited lane commits on branch | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for `d08d8de a2fe31b 5613071 9ef758c 24a1647 76fac3b 2ac06c5 ce72dd1b 1e54c895` | all `commit`, all ancestors (exit 0); `git log 1e54c895..ce72dd1b` gives exactly the 8 commits in the Landed table, all by `kake-shokunin <kake@shokunin.local>` | pass |
| control hashes the report cites | `git cat-file -t dcef39b5`, `0cce15f0` in the lane | not in the lane object store (as disclosed). They resolve from the retained bundles `.ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle` (head `dcef39b5f4e8…`, `refs/heads/lookup-c1`) and `r34-c2-hollow-0cce15f0.bundle` (head `0cce15f0719a…`, `refs/heads/hollow-c2`). Both bundles verify, and each has parent `a2fe31b` | pass (retained) |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state kake-shokunin` | `branch=master local=ce72dd1b… remote=ce72dd1b… ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| no leftovers | `git -C kake-shokunin status --porcelain` | empty | pass |
| remote ref | `git -C kake-shokunin ls-remote origin refs/heads/master` | `ce72dd1b31673f62c54e4663ffa9723a53caf79d` | pass |
| prompt carries template contract | each non-empty line of `templates/round-prompt.md` (placeholder lines checked by their fixed fragments) searched in `.ufo/prompts/kake-round-34.md` | 116/116 present; §1–§5 plus §6 hyaku addendum | pass |
| SOURCES.md seat write and revert | `git rev-parse <rev>:corpus/SOURCES.md` at each round commit | blob `bac1bf2e…` is identical at `1e54c895`, `d08d8de`, `a2fe31b` and `5613071`, so the seat's write never reached a commit. It is `d0ba7316…` at `9ef758c`, where 11 rows are added (S067–S077, 66 → 77), and `59e470b2…` from `76fac3b` on, where the only change is S077 tier B → A (logged at lesson `:148`) | pass |

Conformance defects (status-neutral): none affecting the record. Small accuracy items are routed
below.

## Claims (step 2)

Harm check: `git diff --stat 1e54c895 ce72dd1b` gives 270 files and 11912 insertions. Only the 15
binary files report non-zero numstat columns (`-`/`-`): 3 bundles, 11 `.html.gz` and 1 `.tar.xz`.
No text line is deleted anywhere. `git diff … -- SCORECARD.md` holds additions only: a capability
row and the round-34 sections. The axis ratings are unchanged at 10 → 10 (saturation line).
No owned axis is harmed.

### C1 — operability (capability): offline link-preview audit `scripts/link_preview_audit.py`

The declared counter was re-run in the sandbox clone:
`python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision <rev>`. Its counter sha256
is `fc72d855…c51e`, unchanged since `d08d8de`, and the matrix sha256 is `246a6a3b…14f7` (pinned).

| revision | exit | passed | constants (clean / failed-empty / refuse / all-missing) | allRejected |
|---|---|---|---|---|
| `1e54c895` (base) | 1 | 0/28 (tool absent) | 6 / 0 / 6 / 1 of 28 | true |
| `ce72dd1b` (tip, tool sha256 `cccc3a17…a4db`) | 0 | 28/28 | 6 / 0 / 6 / 1 | true |
| `dcef39b5` (retained lookup control, tool sha256 `a2e274c0…30ec`) | 0 | **28/28** | 6 / 0 / 6 / 1 | true |

The re-run matches the reported values: 0/28 before and 28/28 after, constants rejected. It also
confirms the lane's disclosure. The control's 18-line tool (`git show
dcef39b5:scripts/link_preview_audit.py`) parses no HTML. Line 2 is a 28-entry table mapping a
sha256 to (exit, verdict, findings). Lines 5–15 hash `argv` plus every relative path and file
content under the cwd, then print the stored row; an unknown key prints `[0,"clean",[]]`.

**Ruling as declared: does not verify.** The declared after-state is "28 of 28 with all four
constant gates rejected". A tool that does none of the declared work reaches it: no HTML parsing
and no rule, only a transcription of the matrix committed beside the declaration. So the target
cannot fail on the quality the claim names ("reads … local HTML pages and reports …"). That
breaks the dispatch condition the orchestrator states: a trivial baseline must not reach the
target. It also falls short of the committed prompt's §2 "Admission: every claim verifies —
measured". The lane says so itself (SCORECARD "Limits found by wave 1": "Both counters are
necessary, not sufficient"). C1 was not declared exploratory, and a measure the closure builds
after landing cannot replace the lane's declared target (prompt §6.9: "Never narrow a target
after landing").

**What the landed tool does, measured by the closure (not counted toward C1):**
- Perturbed matrix: the same 28 cases, materialized under a random uuid directory, with
  `<!-- closure perturbation -->` appended to every `.html` file. This keeps the meaning, so the
  expected outputs do not change. Landed tool **28/28**; lookup control **7/28**: it passes
  K1–K6 and I3 and falls back to exit 0 on every defect, input and usage case.
- Twelve held-out cases written by the closure from the declared contract, none of them in the
  matrix. H1 is clean with og:description. H2 lacks image and url. H3 has a relative og:url. H4
  has an og:url on another host than the canonical. H5 has three og:type. H6 has a blank title.
  H7 is the middle page of three lacking og:type. H8 uses `OG:TITLE`. H9 has an ftp page URL. H10
  has `pages` that is not a list. H11 has a `../z/` canonical equal to og:url. H12 has a `../z/`
  canonical that differs from og:url. Landed tool **12/12**; lookup control **2/12** (H1 and H11
  only).
- Real input: the 102 pages of the retained `sources/ds4cc-7fc6aa2f/html.tar.xz`, with a manifest
  built by the closure (`url = https://ds4cc.com/<path>`). Landed tool: exit 1, `failed-policy`,
  `pagesChecked` 102, `og_required_missing`: og:title 15, og:type 15, og:image 101, og:url 15, and
  no `og_url_not_canonical`. Lookup control: exit 0, `clean`, `pagesChecked` 0. The landed
  counts agree with the closure's own stdlib `html.parser` census in the C2 table below
  (102 − 87 = 15; 102 − 1 = 101).
- Code read (`ReadLinkPreviewTool`), `scripts/link_preview_audit.py` at tip:
  - It parses each page with stdlib `html.parser` (`MetadataParser` :80–113, fed at :222–224).
  - It holds no case id, matrix literal or hash table.
  - It implements the four rules: required-missing at :226–234, multiple og:type at :236–243,
    non-absolute og:url at :245–254, and og:url against the first canonical at :255–269.
  - Its only I/O is the manifest and page reads and `print`; nothing touches the network or
    writes.
  - Divergences: `og:image:url` aliases `og:image` (:59, a wave-2 change citing S067; no matrix
    case uses it), and only the first non-empty og:url is compared (disclosed).
- Committed evidence verified, not run: `verification/selftest-link-preview-at-76fac3b.txt` gives
  `passed 35`, `failed 0`, `exit=0`, at tool sha256 `cccc3a17…`, which equals the tip tool.
  `verification/selftest-w2-survivor-mutants.txt` shows 34/35 for each of 3 mutants.

Axis verdict, **operability: `unprovable-but-better`**. The declared measure cannot prove the
capability. The closure, as named non-author reviewer, judges the landed tool to be a real
working audit: 40/40 on perturbed and held-out inputs against 9/40 for the lookup control,
real-input counts consistent with an independent recount, and a code read.

### C2 — freshness (sourced): `corpus/knowledge/link-preview-metadata.md` + ds4cc census line

The declared counter was re-run in the sandbox clone:
`python3 -B .ufo/waves/round-34/c2_source_census.py --root . --revision <rev>`. Its counter sha256
is `ee7461b9…f892`, unchanged since `d08d8de`.

| revision | exit | met | controlBroken |
|---|---|---|---|
| `1e54c895` (base) | 1 | 0/5 | false |
| `ce72dd1b` (tip) | 0 | 5/5 | false |
| `0cce15f0` (retained hollow control) | 0 | **5/5** | false |

The control (`git show 0cce15f0 --stat`) is 20 added lines:
- four `SOURCES.md` rows of the form `| S067 | junk https://ogp.me/ | x | x | x | x | x | mined | 2026-10-22 | x | x |`;
- an entry made of `# junk`, seven `filler` lines, `S067 S068 S069 S070` and the census line;
- Gate quotes that are page-title fragments ("The Open Graph protocol The Open", "Slack Robots | Slack Go to").

The census numbers were already published before the entry existed: `census.derived` in the
declaration-commit receipt `verification/c2-at-d08d8de.json` carries them.

**Ruling as declared: does not verify.** The declared after-state is `met 5 of 5`. A 10-line junk
entry that carries no knowledge reaches it, so the target cannot fail on the quality the claim
names ("link-preview metadata enters held knowledge … grounded in S067–S070"). The same dispatch
condition and the same §2 admission rule apply as for C1. This shape was routed at round 33
(routed defect 1: junk row and other hollow shapes) and was reused in this round's declaration.

**What the landed entry holds, measured by the closure (not counted toward C2):**
- Census: the closure's own stdlib `html.parser` recount of the 102 retained pages gives
  `pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1 og-url-equals-canonical=87`.
  That equals the entry line at `corpus/knowledge/link-preview-metadata.md:128`.
- Quotes (`ReadEntryVsHollow`): all 48 of the entry's 48 quoted spans are exact
  (whitespace-normalised) substrings of the cited retained text: S067 16, S068 12, S069 6,
  S070 11, S073 2, plus the source title.
- Six substantive claims were checked against the retained text, and each is supported:
  - the four required properties (`:20–21`);
  - the image cache keyed by URL (`:62–63`);
  - the crawler's heuristic fallback (`:66–68`);
  - Slack's range-limited fetch (`:83–84`);
  - robots.txt not honoured (`:95`);
  - the card generated from OpenGraph tags (`:101–102`).
- Per-page ds4cc findings reproduce from the archive: the sole all-four page is
  `omegag/index.html`, the 15 unmarked pages are 11 under `burnerchrome/` plus bloat, burnerchrome,
  exa and frontier, and the bloat and exa canonicals were checked.
- The closure found no false or unsupported statement.

Axis verdict, **freshness: `unprovable-but-better`**. The declared measure cannot prove the
entry. The closure judges the entry to be real, current and grounded knowledge, unlike the
transcription control.

### Other axes

depth, coverage, calibration and adjacency: `unchanged`. No claim touched them, their ratings did
not move, and no line was deleted.

**Admission: not admitted** (`rejected-honest-stop`). Neither declared claim verifies as declared,
and no axis is harmed. The lane disclosed both controls itself, retained them, and wrote that
"Admission rests on a non-author read". This closure's read finds the work real, but a measured
claim whose own measure a do-nothing control meets is not a verified claim, and neither claim was
declared exploratory.

## Discernment spot-check (step 3)

The Gate (`corpus/lessons/round-34.md:34–44`) records 11 decisions. Closure seat
`ReopenGateSources` re-opened the sources live during this closure on 2026-10-22 (UTC).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S067 | admit (A, mined) | https://ogp.me/: HTTP 200. Quote "The four required properties for every page are" is present live and retained, 8 words | agree | The spec's own statement of required page metadata. The SOURCES row's quote and location cells match the retained text; the receipt's sha256 `0174794e…675581` matches the row |
| S070 | admit (A, mined) | https://docs.joinmastodon.org/entities/PreviewCard/: HTTP 200. Quote "Represents a rich preview card that is generated using OpenGraph tags from a URL." is present live and retained, 14 words | agree | The entity's opening definition, in tier-A primary docs |
| S069 | admit (A, mined) | Retained `S069.txt`: "Specifically, we are looking for oEmbed and Twitter Card / Open Graph tags." is an exact substring, 13 words | agree | Slack's own robot documentation names the tag families it reads |
| S071 | reject (C) | The requested cards-markup URL redirects to `https://docs.x.com/overview` (HTTP 200). Quote "Fetch the complete documentation index at: /llms.txt …" is present live and retained, 15 words | agree | The URL still serves the generic docs index with no cards-markup documentation |
| S074 | reject (A, out of scope) | https://core.telegram.org/bots/api: HTTP 200. The 21-word quote is present live and retained | agree | LinkPreviewOptions holds only a bot's switches and no publisher-side tag rule. Accuracy nit: "no og: occurrence" is true of the extracted text only; the page `<head>`, live and in `S074.html.gz`, carries 3 `og:` metas describing the page itself (routed, verdict unchanged) |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exits 0 and
prints `kake W04 S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes` (that
warning predates the round) and `kake ok …/corpus/SOURCES.md`. Rows go from 66 to 77
(`git show <rev>:corpus/SOURCES.md | grep -c '^| S0'`).

Spot-check result: the closure agrees with the Gate on 3 of 3 admits and 2 of 2 rejects.

## Trend verdicts

- **expansion: `unprovable-but-better`.** Link-preview metadata is ground the lane never held,
  and the round adds a working offline audit (measured above), a grounded entry and 11 opened
  rows. LEARNING's `improved` needs net new *admitted* entries, and neither claim was admitted.
- **quality: `unchanged`.** No earlier admitted entry was re-verified, deepened or superseded, and
  none was found false or stale. The round-33 sandbox-only evidence is now retained in the lane
  (`retained/r33-*`). That makes an earlier pointer resolve, but it is not an entry-quality move.
- **discernment: `improved`.**
  - The spot-check agrees on admits and on rejects.
  - The round's own counter insufficiency became lesson mistake row 4 and QUALITY round-34
    criterion (d).
  - `criteria/lookup_control_check.py` is shown able to fail:
    `verification/criterion-lookup-control-c1-dcef39b.txt` records exit 1, "FAIL: control reaches
    the full score".
  - The Gate now records 4 rejects with located reasons, which closes round-33 routed defect 3.

## Routed defects (lane must address next round)

1. **Declare a target a do-nothing control cannot reach.**
   - Both round-34 targets were met by retained controls (`dcef39b5` C1 28/28; `0cce15f0` C2 5/5).
   - Next declaration: ship a measure on held-out or meaning-preserving perturbed inputs (for a
     knowledge claim, a condition a transcription fails).
   - Commit the retained controls' scores on that measure *before* the build, showing each below
     target.
   - Re-run `criteria/lookup_control_check.py` against the new counter with both retained controls.
2. **The lookup control is misdescribed.**
   - The control keys on content, not the directory name:
     - mistake row 4 (`corpus/lessons/round-34.md:68`), `criteria/lookup_control_check.py:6` and
       SCORECARD "Limits found by wave 1" say `dcef39b5` "keys on the case directory name";
     - its bytes (`dcef39b5:scripts/link_preview_audit.py` lines 5–15) hash `argv` plus each
       relative path and file content under the cwd.
   - So the carried item "C1 counter leaks the case id through the case directory name" is not
     what lets it pass. Renaming directories does not defeat it, but a one-comment HTML
     perturbation does (7/28, above).
   - Correct this by append.
3. **No gate registry row for the link-preview audit.** It has exits 0/1/2/64 and a selftest, yet
   `SKILL.md` has no `link-preview-audit | gate|probe | …` row. Precedent rows: `SKILL.md:411`
   canonical-audit and `:725` base-path-audit. Under PROTOCOL §Gate standard (Registry,
   Delivery), it is not conformant until the row exists.
4. **The C2 census numbers were published by the counter's own declaration receipt.**
   `verification/c2-at-d08d8de.json` `census.derived` carries them before any entry existed, so a
   copy reaches the census condition. A future census condition must not publish its target in a
   pre-build receipt.
5. **S074 reason overclaims.** Gate `:41` and the SOURCES row say "no og: occurrence". That is true
   of the retained text, but the page head carries 3 `og:` metas about the page itself. Correct by
   append; the reject stands.
6. Carried, unchanged: the C2 counter defects D1–D4; the tool's first-og:url-only comparison,
   canonical inside `<template>`/`<svg>`, and the non-UTF-8 page stopping the manifest; the
   Git-pin mutants; option tables; the NUL-byte runner crash; the freshness-pins re-pin; round-31
   F1–F3.

For the operator:
- The trivial-baseline clause the orchestrator cites is not in the committed bytes:
  `grep -n -i -E 'trivial|quality it claims|able to fail on'` over `.ufo/prompts/kake-round-34.md`,
  `templates/round-prompt.md` and `scripts/hyaku/lane-addendum.md` returns nothing. This closure
  rests its ruling on prompt §2 "each falsifiable" and "Admission: every claim verifies — measured",
  together with the lane's own "necessary, not sufficient" disclosure. Adding that clause to
  template §2 is operator-owned.
- SHONEN: all 4 boxes are `[~]`. Box 2 rests on an offline-only task with no live surface. None is
  promoted by this closure.
