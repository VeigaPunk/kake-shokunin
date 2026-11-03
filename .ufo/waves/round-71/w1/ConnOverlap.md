# ConnOverlap — kake round 71, W1 connector (read-only sibling-overlap scan)

Seat `ConnOverlap` · base `cc6b4e0b8c35e72dfb02c6184b847f68c1262153` · contract `04557e17` + `amendment-1.md`.
Lane tree untouched (`git status --porcelain` on the lane: only the pre-existing untracked
`.ufo/waves/round-71/` wave files). Scratch `/fast/scratch/hyaku/kake-r71/ConnOverlap/` removed on exit.

## (1) Which sibling lanes carry the same `/tmp` paths or the same SOURCES rows?

**`/tmp` paths — ZERO sibling overlap.** Kake's C2 population is 7 tokens on 7 lines
(`SKILL.md:27,95,227,356,359,463,464`), spanning 4 distinct path strings.

```
grep -l -E '/tmp/kake-r12/live/|/tmp/probe-latest\.backup\.json|/tmp/kake-r11/|/tmp/kake-r23-SurfacePlazir15Kimi-bnbU' \
  /home/vgpnk/Projects/shokunin/*-shokunin/SCORECARD.md
→ kake-shokunin/SCORECARD.md          count=1
grep -l -E '<same pattern>' /home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md
→ kake-shokunin/SKILL.md              count=1
```
Committed-byte form over all 21 lane repos, `git -C <repo> grep -l -E <pattern> HEAD -- SCORECARD.md SKILL.md`
→ 2 hits, both kake (`HEAD:SCORECARD.md`, `HEAD:SKILL.md`). Broadened to `/tmp/kake` → same 2 hits.
`audio-shokunin` and `game-dev-2d-shokunin` have **no** `SKILL.md` at all (18 of 21 lanes have one).
Fleet-wide for the 4 path strings (any file, any extension) every hit is inside `kake-shokunin/`.
**Conclusion: no sibling lane cites kake's `/tmp` paths → the C2 repair cannot collide with a sibling's text.**

**SOURCES rows S129–S132 — row-ID collision is a naming artefact, not shared content.**
`grep -l -E '\bS1(29|30|31|32)\b'` over sibling `SCORECARD.md`/`SKILL.md` returns 12 sibling lanes
(chousa, kaidoku, kama, kengaku, kotoba, kotodama, kumitate, mori, souji, tabi, tsukuroi + kake) — but
`corpus/SOURCES.md` shows every lane numbers its own registry independently: 15 of 21 lanes have rows
numbered S129–S132, and **all 15 name different sources** (chousa = CN clinical-evaluation guidelines;
kaidoku = binwalk/unblob/OpenWrt; kama = llama.cpp; kengaku = Terminal-Bench; kotodama = sign-language
papers; kumitate = Bailian docs; mado = kitty; mori = systemd; revenger = dewolf/Ghidra; souji = git;
tabi = Chromium; tsukuroi = btrfs). Kake's S129/S130/S131/S132 are the *only* registry rows in the fleet
naming tameshi r33 control docs and the kama r29 calibration method. Precedent for this reading:
`kaidoku-shokunin/.ufo/waves/round-49/w1/ConnSibling.md:51-52` — "Source ids … name different sources in
each lane. Ids are per-lane homonyms." `grep -l 'kake-shokunin/corpus/SOURCES\.md'` over sibling
SCORECARD/SKILL → **0 hits**: no sibling's live self-assessment cites kake's registry at all.

**S132's source document — one sibling imports the same file.** `grep -l 'self-assessment-at-writing'`
over sibling `SCORECARD.md`/`SKILL.md` → kake's `SCORECARD.md` + **kama's `SCORECARD.md`** (kama names
its own file at `:1534`). Per-lane committed-file counts: kake 145, kama 147, kotoba 55, souji 4,
kaidoku 2, kasegi/kumitate/mori/revenger 1 each. Only **kotoba** imports it as a registry row
(`kotoba-shokunin/corpus/SOURCES.md:128`, row **S117**, "Sibling lane kama, Checking self-assessment
statements at writing", tier B, `opened 2026-10-23`, same blob `0601bd03…`, same sha256
`cd6e3730…f959`) — the *same* source kake calls **S132**. Kake's S132 is a second, independent import of
one file; kotoba's is a practice-level borrowing with **no counter** (`kotoba-shokunin/corpus/knowledge/
writing-revision-calibration-round61.md:1-3`; `kotoba-shokunin/.ufo/waves/round-49/w1/ConnSibling.md`
B11: "Practice-level borrowing from kama only. No counter.").

## (2) S132 source path — exists; kama's tree changed, the cited file did not

```
ls -l /home/vgpnk/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md
→ -rw-r--r-- 1 vgpnk vgpnk 5831 Oct 23 16:07 corpus/knowledge/self-assessment-at-writing.md   (exists)
sha256sum …/self-assessment-at-writing.md
→ cd6e3730085ed08ca583604390e84c352ea122e4a6386e383d261a0a0b4cf959   (identical to kotoba S117's pin)
git -C /home/vgpnk/Projects/shokunin/kama-shokunin log -1 --format=%cI -- corpus/knowledge/self-assessment-at-writing.md
→ 2026-10-23T16:09:39-03:00        (the file's last change — 11 days ago, unchanged since S132 was opened)
git -C …/kama-shokunin rev-parse HEAD:corpus/knowledge/self-assessment-at-writing.md  → 0601bd0301d65cb4a688901b0db6c8488a739f03
git -C …/kama-shokunin rev-parse 6de225c289b7682bf280cffb4a07de3fb7d1275c:corpus/knowledge/self-assessment-at-writing.md → 0601bd0301d65cb4a688901b0db6c8488a739f03
```
**Yes, kama's own tree has changed since 2026-10-23** — `git log --since=2026-10-23 --oneline` → **327
commits**, HEAD `6035e952c2521999e192d6f236331f265ac98392` `2026-11-01T13:46:24Z`. But the **cited file
is byte-identical**: same blob at HEAD and at the 2026-10-23 commit `6de225c2`, same sha256, same mtime
`Oct 23 16:07`. The S132 quote still verifies verbatim:
`grep -c 'A mismatch therefore records a calibration error present when the statement was written'` → **1**,
at line **7** of a 33-line file — the **first section-prose paragraph**, exactly as S132's locator states
(the `## Checking self-assessment statements at writing` heading is line 5). A located quote for the
Gate, verbatim and 18 words: *"The check then evaluates the statement against the committed tree/history
at `W`, not just against the current tip."* (line 7). So kama's 327 later commits are **not** a source-
stability risk for C1: the whole surrounding tree moved while the cited artifact did not.

## (3) Who owns the calibration method, and who owns the `/tmp` rule?

**Calibration method → `kama`, exclusively.** Origin lane, own counter:
`kama-shokunin/.ufo/waves/round-29/count-c1.py` (frozen sha256 `fe11d599…7383`) +
`kama-shokunin/corpus/knowledge/self-assessment-at-writing.md`, whose `source:` header names that counter.
Kake imports it as S130/S132; kotoba imports it as S117 (tier B, no counter). Two further lanes run
**same-job, different-instrument** calibration counters (kaidoku r49 census B1 revenger `corpus/
self_assessment_check.py`, B5 tabi `scripts/check-selfassessment.mjs`, B2 kagi `corpus/self-counts.py`,
B4 souji `census/round-39/c1-counter.py`, B7 mori `tools/mori-freeze-order.py`, B10 tameshi
`corpus/knowledge/executable-self-assessment.md`) — the method family is shared fleet-wide, the
instrument is not; kaidoku's own census says "the method family is shared; the instrument is not."

**The `/tmp` rule → nobody else owns it; kake owns it.** The rule's two owning artefacts are kake-local:
`corpus/QUALITY.md` carries the *only* "Absence annotation content" criterion in the fleet (21 lanes
checked → kake=1, all others=0), and `scripts/freshness-sweep.mjs` exists in **kake only** (21 lanes
checked → 1 owner). The annotation phrase `not an executable instruction` is committed in **kake 273
files**, kotodama 4, tabi 1 — and kotodama's is a *different* surface (SKILL.md:716, an embedded historical
counting-command string, no `/tmp` token on that line) while tabi's is a copied kake context file
(`.ufo/waves/round-35/w2/CritScreenKake/kake-context.txt`). **No sibling lane owns the `/tmp` absence-
annotation rule, and no sibling lane's SKILL.md contains a `/tmp` path that the C2 repair could touch.**
Only kotodama SKILL.md:458 carries a `/var/tmp` prose mention (0 `/tmp` tokens).

## The non-obvious finding: C1's own repair breaks the round-70 standing counter's append-only conjunct

The contract's C1 repair rewrites two **base** SCORECARD.md lines (21 and 3990). The round-70 C1 counter
`.ufo/waves/round-70/c70_pointer_audit.py` measures the *same* file with an append-only conjunct
(`--base e5f6fd9e…`): `tip_lines[:len(base_lines)] == base_lines`. Rewriting base lines 21/3990 in place
therefore makes that conjunct false. Isolated in scratch (`/fast/scratch/hyaku/kake-r71/ConnOverlap/clone`,
`git clone --shared` at `cc6b4e0b`, `user.name=kake-seat`), three variants, both counters:

| variant | `c71_calibration.py` | `c70_pointer_audit.py --base e5f6fd9e…` |
|---|---|---|
| base `cc6b4e0b` | `stale_planned=2 … mismatches=3 met=False` exit 1 | `unannotated=0 append_only=true met=true` exit 0 |
| **appends only** (Correction + `## Planned — next round`) | `stale_planned=2 … mismatches=2 met=False` exit 1 | `unannotated=0 append_only=true met=true` exit 0 |
| **rewrites only** (lines 21 + 3990) | `stale_planned=0 … mismatches=1 met=False` exit 1 | `unannotated=0 append_only=false met=false` **exit 1** |
| **full contract repair** (all four items) | `mismatches=0 guard=ok met=True` exit 0 | `unannotated=0 append_only=false met=false` **exit 1** |

C2 side is clean: applying the contract's C2 repair rule in scratch gives
`C2 … tokens_total=6 unannotated_tokens=0 removed=7 added=7 guard=ok met=True` exit 0, and
`node scripts/freshness-sweep.mjs --offline` is **byte-identical** at base and at the C2 draft
(`§paths 187 files · 704 occurrences · 107 unique tokens · resolve 32 · declaredAbsent 64 · drift 1`,
same `VERDICT: DRIFT — §paths: 1 unannotated miss` pre-existing `~/projects` red) — because the sweep's
`PATH_RE` matches only `~` and `/home/vgpnk` paths, never `/tmp`, and it never reads `SCORECARD.md`.

**Contradiction to state plainly (not a scalar):** round-71's frozen C1 repair rule *requires* rewriting
base lines 21/3990; round-70's committed QUALITY criterion (round-70 addendum) *rejects* "a calibration
landing that rewrites any base line of the file (the append-only conjunct)", and the round-70 counter's
own `--base` form goes red at the round-71 tip. Both cannot be satisfied by one SCORECARD.md edit. The
contract's kill rule covers a *round-71* guard failure, not this cross-round one, so C1 can still land
green while a previously-green round-70 receipt becomes unreproducible at the new tip — that is a
fact the L1 must record, not a reason to narrow C1.

## Risks / verification

- **Risk**: an L1 that re-runs `c70_pointer_audit.py --base e5f6fd9e…` at the round-71 tip sees exit 1
  and may treat it as a regression of the landed C1. It is the *inevitable* consequence of the contract's
  own repair rule (proved by the rewrites-only variant above), not an executor error.
- **Risk**: C2's repair must not use `/tmp` in the replacement text — `c71_tmp.py` counts any `/tmp/`
  token in the line, so `$(mktemp -d)` must be written literally as the contract says, else
  `unannotated_tokens>0`.
- **Verification for the L1** (all in scratch, never the lane):
  `python3 -B .ufo/waves/round-71/c71_calibration.py --lane <clone> --revision <tip>` → `met=True` exit 0;
  `python3 -B .ufo/waves/round-71/c71_tmp.py --lane <clone> --revision <tip>` → `met=True` exit 0;
  `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <clone> --revision <tip> --base e5f6fd9e…`
  → **expected exit 1, `append_only=false`** — record it as a named cross-round consequence, alongside a
  `node scripts/freshness-sweep.mjs --offline` run showing no new red against
  `controls/sweep-offline-base.txt`.

## Tooling

None installed or upgraded; pacman untouched. Read-only `git grep`/`git show`/`git log`/`grep`/`sha256sum`/
`node`/`python3` only. No lane tracked file modified; no sibling repo written; `shokuknow` read-only,
untouched. Scratch tree `/fast/scratch/hyaku/kake-r71/ConnOverlap/` deleted on exit.
