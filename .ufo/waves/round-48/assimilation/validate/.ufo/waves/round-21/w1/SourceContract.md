# SourceContract — S019 row for the canonical metadata/Gate contract

Seat: KakeR21.SourceContract (scout). Round 21, W1. Report only; no file edited.
Read at 2026-10-20. All lane paths are relative to
`/home/vgpnk/Projects/shokunin/kake-shokunin`.

## 1. What exists at read time

Sources opened:

- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`,
  sha256 `b6ed4476b0d1a5a3176ce728e4eb44997bddfa6dfb9fdb2f1a15e81d3f0821bf`,
  commit `e737d2ea97f6b0198503e077676c3f2ea07974a9` (2026-10-19 21:21:25 -0300,
  clean worktree for both protocol files).
- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md`,
  sha256 `3ff7ab4da9f3ce448477872af62c8d74ad0671e0d5bfc29a4ca8945bd8865964`,
  same commit.

`corpus/SOURCES.md:27` already carries an S019 row, added this wave and still
uncommitted (`git status --porcelain` → `M corpus/SOURCES.md`; the diff is a
single added line, no pre-existing line changed):

| S019 | own-work: publishing corpus contract audit — scripts/corpus-contract.mjs; canonical input /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md | own-work | A | Provenance metadata and recorded lesson gates for kake's publishing corpus, not verification of historical platform claims | Canonical input Layout and Additional corpus rules, opened 2026-10-20; local gate first-working round 21 | Knowledge entries open with source, verified-at and recheck; round lessons record candidates, admissions, rejections and spot-check state | mined | 2026-10-20 | on-release | corpus/lessons/round-21.md |

Assessment: scope, honesty clause, `own-work`, tier A, `opened: 2026-10-20`,
`on-release`, `mined`, and `used-by: corpus/lessons/round-21.md` are correct
(`round-21.md` exists and cites S019). Two contract defects remain.

1. The anchor has no revision. Contract v1 requires "exact section / heading /
   page / line plus revision (version, commit, or publication date)". "opened
   2026-10-20" is an access date and duplicates the `opened` column.
2. The source cell names `scripts/corpus-contract.mjs`, which did not exist at
   this read (`test -f scripts/corpus-contract.mjs` → absent; the implementer
   seat is still in flight per `.ufo/waves/round-21/wave1-spec.json:189`).
   A row is a claim; a `source` path that cannot be opened at row-writing time
   fails rule 1. Keep the clause only if the file exists at commit.

Census at read (contract commands, from the lane root): rows 19; malformed 0;
duplicate ids none; tier `A=17 C=2`; status `mined=15 queued=2 rejected=2`;
S019 `NF=13`.

## 2. Recommended exact row

Paste-ready, with the script clause omitted (see condition below):

```
| S019 | Shokunin protocol corpus contract: canonical metadata and Gate rules — kimi-shokunin/skills/shokunin/protocol/CORPUS.md; kimi-shokunin/skills/shokunin/protocol/LEARNING.md | own-work | A | Required provenance-trio prefix in knowledge entries and the round-lesson Gate record fields; format only, never platform or historical verification | CORPUS.md §Layout lines 18-19 and §Additional corpus rules lines 162-165; LEARNING.md §Files the path writes lines 69-73; canonical commit e737d2ea97f6b0198503e077676c3f2ea07974a9 (2026-10-19) | A knowledge entry opens with source:, verified-at: and recheck: because freshness sweeps read those fields, and a round lesson carries a Gate naming candidates, admits, rejects and the spot-check result | mined | 2026-10-20 | on-release | corpus/lessons/round-21.md |
```

Condition: if `test -f scripts/corpus-contract.mjs` passes before commit, use
`own-work: publishing corpus contract audit — scripts/corpus-contract.mjs (lane
gate); canonical input kimi-shokunin/skills/shokunin/protocol/CORPUS.md and
LEARNING.md` in the source cell instead. The two anchors above are unchanged
either way; only the source cell differs.

Validation of the recommended text: `awk -F'|' … NF!=13` → 0 malformed;
kind `own-work`, tier `A`, status `mined` accepted by the enum check.

Tier rationale: A is scoped to the format contract because the canonical
protocol text is the authority for that scope. The scope cell explicitly
withholds platform and historical-verification authority, so A here says
nothing about any GitHub Pages claim.

Copy hazard (worth stating in the row's Gate record): the lane's parent repo
carries a vendored copy at `/home/vgpnk/Projects/shokunin/CORPUS.md`
(sha256 `88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8`,
commit `6a1dd8ce1a3165a25f9f2b774b21449e0d125c94`, 2026-10-19 21:22:45,
"vendor canonical e737d2e"). It differs in wording and line numbers (trio at
163, not 162) and the canonical text says fleet copies do not override it.
The row and every quote must name the file actually read; never quote the
fleet copy's line 163 under the kimi path.

## 3. Gate record required by rule 1

Rule 1 requires the round lesson's `## Gate` to record, for every new row, the
URL, the access date, and a ≤25-word quote with its location grounding
`teaches`. `corpus/lessons/round-21.md:24` (`## Gate`) and `:37` currently have the URI and
"opened 2026-10-20" plus two quotes labelled "(Layout)" but without line
numbers or a revision. Recommended replacement for that paragraph:

> Sourced claim: C1 and C2 follow S019. Source:
> `file:///home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`
> and `…/LEARNING.md`, accessed 2026-10-20, canonical commit
> `e737d2ea97f6b0198503e077676c3f2ea07974a9` (2026-10-19). Located quote:
> “Each `knowledge/` entry opens with `source:`, `verified-at:` and `recheck:`”
> (CORPUS.md:18, 9 words); “each `lessons/round-<N>.md` carries a `## Gate`
> section” (CORPUS.md:19, 7 words); corroborating “carries a `## Gate` section:
> candidates considered, admitted, rejected (with reasons), and the spot-check
> result” (LEARNING.md:71-73, 15 words). These are contract quotes, not
> evidence of any platform mechanism. No public URLs were fetched. S019 is
> scoped own-work evidence for this audit, not a new domain source.

Both quotes are exact substrings of the canonical file (`grep -c` → 1 each);
each is under 25 words. The existing round-21 wording otherwise already makes
the correct separation ("not a new domain source"; "No public URLs were
fetched").

## 4. Historical reconstruction vs new admission

Observed facts:

- S019's `opened` value is 2026-10-20. It did not exist in rounds 1-20. It is
  therefore never contemporaneous evidence for a historical round decision.
- The reconstructed Gate sections inspected (`corpus/lessons/round-3.md:33`,
  `corpus/lessons/round-19-recensus.md:64`) open with "Retrospective round-21
  reconstruction, not original admission" and cite the lesson's own historical
  sections, LOG and later on-disk references. That framing satisfies the
  distinction.
- The 21 knowledge entries now open with the trio (`grep -L '^source:'
  corpus/knowledge/*.md | wc -l` → 0). Sample diffs keep historical
  `verified-at` dates and add "historical-not-live-reverified"; the entries
  cite S001-S007 etc. for external claims and mark S019 "metadata contract
  only … not a platform authority". The format repair was not turned into a
  re-verification, and S019 was not inserted as the source of a domain claim.

Defects to fix before commit (each belongs to another seat's file; reported,
not edited):

1. `corpus/lessons/round-19-recensus.md:70`: "S019 was not found under
   `corpus/` at read time, and `CORPUS.md` was not on disk". S019 is now at
   `corpus/SOURCES.md:27`, and CORPUS.md existed at
   `kimi-shokunin/skills/shokunin/protocol/` and at the fleet root. True
   statement: "not registered under `corpus/` at the 2026-10-20 read; the
   canonical copy is outside the lane". A reconstruction must not embed a
   transient working-tree negative as a stable claim.
2. Same paragraph, same line: the contract is sourced "as stated in the
   round-21 wave spec, not as a located corpus entry". The wave spec is
   dispatch metadata, not authority; the authority is the canonical
   CORPUS.md/LEARNING.md pair at the pinned commit. Cite that.
3. `corpus/lessons/round-3.md:33`: "The round-21 lesson file
   `corpus/lessons/round-21.md` does not exist yet" — true at that read,
   false now. Phrase as a dated observation ("absent at the 2026-10-20 read").
4. Repaired during the wave, recorded as the positive convention:
   `corpus/knowledge/drift-detection.md:1` now reads "Metadata authority only:
   S019 in corpus/SOURCES.md, not platform verification" (the earlier
   "registration pending in L1 `CORPUS.md`" wording is gone). Registration
   lives in `corpus/SOURCES.md`, not CORPUS.md.

Rule to carry into the corpus gate: a reconstructed Gate may cite S019 only as
the present metadata authority and must say so; it must never cite S019 as the
rule in force during the reconstructed round or as support for a historical
decision. Missing historical rejects and spot-checks stay "not recorded".

New admission: C1 and C2 admit no new domain claim. S019's only `used-by` is
`corpus/lessons/round-21.md`; no knowledge entry cites S019 as a source. If
the contract statement itself is later admitted as a knowledge entry, that is
a new admission citing S019 — not part of this round.

## 5. Registry hygiene (L1-owned; recommendations only)

- Search log: no S019 entry exists. Rule 5 wants one. Suggested appended
  paragraph: "The query was which canonical document fixes the provenance-trio
  order and the round-lesson Gate record shape for kake's corpus. Where: the
  fleet canonical protocol at kimi-shokunin/skills/shokunin/protocol/CORPUS.md
  and LEARNING.md, read at commit
  e737d2ea97f6b0198503e077676c3f2ea07974a9. Date: 2026-10-20. Identified 1,
  screened 1, included 1, excluded 0. Stop rationale: one authoritative
  document pair covers the assigned contract question; no external search was
  performed."
- The closing line "No source ids are void: all S001-S018 were opened" is now
  incomplete but not false. Keep it byte-identical and append: "S019 was
  opened 2026-10-20 in round 21; the sentence above describes the 2026-10-19
  pass."
- Paths: S019 is a format authority, not a study sequence; no path entry
  needed.

## 6. Limitations and unknowns

- The worktree moved during this read: rows went 18 → 19, trio coverage
  4/21 → 21/21, and Gate-bearing lessons 1 → 10 while I was inspecting
  (sibling seats). Counts above are one snapshot with their commands; re-run
  the contract census at integration.
- `scripts/corpus-contract.mjs` was absent at 2026-10-20 read; its existence
  at commit is unverified. The source-cell condition in §2 depends on it.
- Whether `corpus/lessons/round-21.md` is committed is unverified. If it is
  not, S019's `mined`/`used-by` must revert to `queued`/`—`, logged old→new in
  that lesson (rule 2), or the census's mined-path check fails.
- No public URLs were fetched; both canonical files were read locally. No tool
  installation or update was made. No credential or agent-state file was
  read. `corpus/SOURCES.md`, `QUALITY.md`, `LOG.md`, `SCORECARD.md`, `SKILL.md`
  and the lessons were not edited.
