# Pair02A — r27 C1 adjudication, row S002

Seat: KakeR27.Pair02A (reviewer, read-only findings). Axis: freshness. Scope: pair **(S002, corpus/knowledge/static-canonical-preflight.md)**. Repo: /home/vgpnk/Projects/shokunin/kake-shokunin. Measured revision `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (working tree clean for `corpus/knowledge/`). No ledger, source, manifest or Git mutation; no subagent dispatched.

## 1. Verdict

**HOLD** for (S002, corpus/knowledge/static-canonical-preflight.md), with the grouped-synthesis inferential step labelled explicitly (contract C1 `sourceVerdict`).

The citation is a grouped range (`S001–S006`) inside a local synthesis recommendation, not a per-row quotation. S002 individually does **not** entail the whole recommendation; S002's specific contribution — artifact membership ≠ checkout membership — is real, non-vacuous and supported verbatim by the round-27 retained bytes, so the row is HOLD at its own stated scope. No `[r27-recheck S002 STALE]` tag is required.

## 2. Exact citing line(s)

Only one citing site for S002 exists in this file. The expanded range `S001–S006` (en-dash U+2013) yields S001…S006; the pair (S002, file) arises solely from that expansion.

`corpus/knowledge/static-canonical-preflight.md:52-54` — identical in the blob at `be375d9:corpus/knowledge/static-canonical-preflight.md` (`git show | grep -n S001` → line 54 only):

```
52: same opened directory, so a symlink earlier in your own path is followed
53: manifest over actual built/deployable HTML when that artifact exists, not over
54: an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production
```

Located support (20 words, lines 52-54): "Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set (S001–S006, `ghp-served-set.md`)."

Context: the "Input and handoff" run-section (manifest prep, exit-code table). Line 54 is a normative publisher instruction; lines 55-56 add "No production artifact was available or claimed as tested in round22; its fixtures are local, authorized publisher examples." No other S002 token (literal or ranged) occurs in this file, so **no new citing pair is added by this seat**; the S002 denominator is unchanged by my findings.

## 3. Source evidence (round-27 retained bytes, manifest-verified)

Manifest `.ufo/waves/round-27/fetched/manifest.json`; blobs `fetched/S002-{1,2}.raw.gz`; text `fetched/text/S002-{1,2}.txt`. Both sha256 values below were independently recomputed from the decompressed raw blobs and match the manifest.

| fetchIndex | URL | status | fetchedAt | bytes | sha256 |
|---|---|---|---|---|---|
| 1 | https://github.com/actions/upload-pages-artifact/releases/tag/v4.0.0 | 200 | 2026-10-21T19:59:53Z | 200835 | `43d5e22d3d02d07e4cb8abfb1bd35b01cc29ccba819fa1d9d3883c3f278ef070` |
| 2 | https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0 | 200 | 2026-10-21T19:59:55Z | 205035 | `bc5d74856acfadf73123ddc235c84019ed12e43af91b1b6c030b22c3786693a0` |

**Primary support (fetchIndex 1), 14 words:** "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact"
- Anchor: v4.0.0 release page, "What's Changed" block; release tag line renders `v4.0.0 7b1f4a7`,
  matching SOURCES.md `S002` recorded tag `7b1f4a764d45c48632c6b24a0339c27f5614fb0b`.
- Verified as a whitespace-normalised substring of `fetched/text/S002-1.txt` (passes the count_c1 quote test).

**Secondary support (fetchIndex 2), 4 words:** "feat: add include-hidden-files input"
- Anchor: v5.0.0 release page, "Changelog" block; release tag line renders `v5.0.0 fc324d3`,
  matching SOURCES.md `S002` recorded tag `fc324d3547104276b827a68afc52ff2a11cc49c9`.

## 4. Freshness determination (stale premise vs. source-date vs. retry boilerplate)

**Stale premise: none found.** The premise behind line 54 is that the Pages artifact is not the checkout's path set. S002 evidences exactly that divergence in the dotfile dimension: v4.0.0 excludes hidden files from the artifact by default and v5.0.0 converts that into an opt-in input, so artifact membership is version- and config-dependent and the checkout cannot stand in for the served set. The recommendation stays sound at the scope S002 is cited for.

**Source-date difference, not staleness.** The round-26 receipt for this row recorded sha `455adcec328f88362641c1d533e1c7a65c46d5120f8ebe2d55b7dc5eaca6334f` (index 1) and `28d5566afe0653febefea1777c191bd7afb1ecae02e502587c202b74f46fd998` (index 2); round-27 shas differ. That difference is GitHub release-page dynamism (reaction counts, "Footer © 2026", loading placeholders), not a change of release content: the load-bearing sentences are identical in substance across the r26 receipt, the r27 text extract and the live release feed. **A sha difference between rounds is therefore not evidence of a stale claim** and is not reported as one.

**Live re-open (bounded, public release feed).** `https://github.com/actions/upload-pages-artifact/releases` (atom alternate) on 2026-10-21 lists **v5.0.0 (2026-04-10) as the newest release** — no v6 — and repeats "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact" for v4.0.0 and "feat: add include-hidden-files input" for v5.0.0. No newer release alters the artifact-membership behaviour S002 is cited for. I deliberately did **not** mint a sha from this live read: the C1 counter authenticates quotes against the retained `fetched/text/S002-*.txt` blobs and their manifest sha, so a live-read sha would be unusable in a ledger row and would break manifest↔blob identity.

**Irrelevant retry boilerplate: absent for this row.** This file's round-26 recheck paragraph (line 184) lists rows S020, S021, S026, S027, S028, S029, S030, S031, S032, S033, S034 only. The grouped `S001–S006` citation at line 54 was never re-stated in an r26 statement here. The r26 ledger (`.ufo/waves/round-26/statements.json`, 41 pairs) decided S002 in four *other* files — `ghp-served-set.md`, `publish-channels.md`, `sitemap-orphan-audit.md`, `speedrun-pipeline.md` — but not in `static-canonical-preflight.md`. That is a **coverage gap, not boilerplate**, and it is exactly why this pair sits in the 16 r27-unadjudicated set (all six grouped S001–S006 preflight pairs). No "retry" wording in this entry touches S002.

## 5. S002's specific contribution (not just row HOLD)

- The line-54 instruction is a **local synthesis** over six rows; the substance is delegated to
  `ghp-served-set.md` (which carries the per-row quotes for S001-S004, S006, S008).
- **S002's contribution** is the release-level artifact-membership fact: v4.0.0 excludes hidden
  dotfiles from the uploaded artifact; v5.0.0 adds the `include-hidden-files` input — so what the artifact contains is a function of version and configuration, not of the checkout alone.
- **Inferential step (labelled, not hidden):** S002 establishes *artifact ⊄ checkout* in the dotfile
  dimension; *Pages serves the deployed artifact* comes from S001/S004 and the publishing mode from S003. S002 alone therefore supports the "not an assumed checkout served set" instruction only jointly with the other cited rows; it is not presented as entailing it individually.
- S002 does **not** carry the v3.0.1 half of the artifact-contrast story: `ghp-served-set.md:93`
  already re-attributed that half to S002 (r26 rejection `w2/Rejection02S001.md`), consistent with the "Full Changelog: v3.0.1...v4.0.0" line present in the retained bytes.
- **Row scope check:** SOURCES.md `S002` teaches "v4.0.0 excludes hidden dotfiles by default; v5.0.0
  adds the include-hidden-files input". The r27 bytes support both halves verbatim at the recorded anchors; row scope, anchor and teaches are unchanged → row-level HOLD.

## 6. Uncertainties and residual risk (for the parent)

1. **Header metadata gap (freshness, not staleness).** The entry's `source:` header (line 1) declares
   only S020, S021, S026, S027, S028, S029, and `verified-at:` (line 2) covers "2026-10-20 (S020-S027) and 2026-10-21 (S028-S029)". The grouped S001-S006 citation at line 54 appears **only in the body**; no in-file date covers S002 (SOURCES.md records it opened 2026-10-19). Metadata-completeness gap, not staleness; it does not block the HOLD. Sibling pairs S001/S003-S006 in this file share it, so the L1 may want one append covering all six.
2. **v5 opt-in nuance.** Under v5.0.0 with `include-hidden-files: true` the dotfile divergence
   disappears; S002's own `teaches` says so, and line 54 is conservative ("when that artifact exists", "not over an assumed checkout served set"). No correction indicated.
3. **Grouped-synthesis risk.** This HOLD does not license HOLD for the other five grouped rows on
   S002's strength; each needs its own contribution (S001 = pinned action.yml exclusions, S003 = publishing modes, S004 = artifact shape/deploy, S005 = custom domain, S006 = Jekyll defaults). None of the six individually entails the instruction alone.
4. **Not verified by me:** `scripts/canonical_audit.py` behaviour (out of lane; no build/test run per
   bounds) and whether any newer Pages-side change alters served-set semantics.

## 7. Suggested C1 ledger record (per contract `C1.ledger`)

One row for `.ufo/waves/round-27/pairs.json` (`pairs` array). **Not written by this seat.**

```json
{
  "row": "S002",
  "file": "corpus/knowledge/static-canonical-preflight.md",
  "kind": "source",
  "verdict": "HOLD",
  "fetchIndex": 1,
  "quote": "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact",
  "anchor": "upload-pages-artifact v4.0.0 release page, \"What's Changed\" block, release tag line \"v4.0.0 7b1f4a7\" (= 7b1f4a764d45c48632c6b24a0339c27f5614fb0b); second half at v5.0.0 \"Changelog\" block, tag \"v5.0.0 fc324d3\" (= fc324d3547104276b827a68afc52ff2a11cc49c9), \"feat: add include-hidden-files input\"",
  "reason": "Citing site is the grouped range at line 54 only: \"an assumed checkout served set (S001-S006, `ghp-served-set.md`)\" inside the recommendation to prepare the manifest over actual built/deployable HTML. Grouped local synthesis: S002 contributes the artifact-membership half - v4.0.0 \"What's Changed\" (fetchIndex 1, sha256 43d5e22d3d02d07e4cb8abfb1bd35b01cc29ccba819fa1d9d3883c3f278ef070) states hidden dotfiles are excluded from the artifact, and v5.0.0 \"Changelog\" (fetchIndex 2, sha256 bc5d74856acfadf73123ddc235c84019ed12e43af91b1b6c030b22c3786693a0) adds the include-hidden-files input - so artifact membership is version/config dependent and the checkout cannot stand in for the served set. Inferential step labelled: S002 alone establishes artifact-not-checkout in the dotfile dimension; the served-set and publishing-mode halves come from S001/S003/S004, so the line-54 instruction is not entailed by S002 alone. Row scope and anchors match corpus/SOURCES.md S002 unchanged. Freshness: v5.0.0 is still the newest release as of 2026-10-21 (live release feed), and the round-27 sha differs from the round-26 sha (455adcec... / 28d5566a...) only in GitHub release-page dynamic content - the load-bearing sentences are identical, so this is a source-date difference, not a stale premise. No STALE correction required."
}
```

Field check against the frozen counter (`count_c1.py`): `verdict` ∈ {HOLD,STALE,UNVERIFIABLE} ✓; `reason` non-empty ✓; `kind`=source → `fetchIndex` resolves to manifest entry row S002 / index 1 ✓; `quote` = 14 words (≤25) and is a whitespace-normalised substring of `fetched/text/S002-1.txt` ✓ (both re-verified locally against the retained bytes); `anchor` non-empty ✓; no `[r27-recheck S002 STALE]` marker required for a HOLD ✓.

## 8. Appended-correction wording (proposed, optional, NOT written by this seat)

No STALE correction is warranted, so no mandatory append exists for this pair. If the L1 wants a provenance append for the grouped citation (one block can cover S001-S006, since the six pairs share one citing line), proposed wording in the entry's existing append-only house style — it asserts no staleness and rewrites no original line:

```
### Round-27 grouped citation grounding — S001-S006 (2026-10-21, append-only; original lines unchanged)

- The grouped range at line 54 ("an assumed checkout served set (S001-S006, `ghp-served-set.md`)")
  is a local synthesis: no single cited row entails the line-53 instruction on its own. Per-row
  contributions were re-grounded this round against bytes opened 2026-10-21
  (`.ufo/waves/round-27/fetched/manifest.json`, retained text under `fetched/text/`). S002's
  contribution is the artifact-membership half: the v4.0.0 release "What's Changed" block reads
  "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the
  artifact", and the v5.0.0 "Changelog" block reads "feat: add include-hidden-files input"; what
  the artifact contains is therefore version- and configuration-dependent, and the checkout cannot
  stand in for the served set. S002 is judged HOLD at its recorded anchors
  (`.ufo/waves/round-27/w1/Pair02A.md`); the entry's `source:`/`verified-at:` header lines (1-2)
  continue to name only S020-S029 and are not rewritten.
```

If the L1 prefers no append for a HOLD, omitting this block does not affect the C1 count: the counter requires an appended `[r27-recheck S0NN STALE]` marker only for STALE verdicts.

## 9. Evidence index

- `corpus/knowledge/static-canonical-preflight.md:52-56` (citing line 54); `:1-2` (header); `:184` (r26 recheck paragraph, rows S020-S034 only).
- `.ufo/waves/round-27/fetched/manifest.json` — S002 index 1-2: url, status 200, fetchedAt, bytes, sha256, file, text.
- `fetched/S002-1.raw.gz` → sha256 `43d5e22d3d02d07e4cb8abfb1bd35b01cc29ccba819fa1d9d3883c3f278ef070`, 200835 bytes; `fetched/S002-2.raw.gz` → sha256 `bc5d74856acfadf73123ddc235c84019ed12e43af91b1b6c030b22c3786693a0`, 205035 bytes.
- `fetched/text/S002-1.txt` (3497 chars), `fetched/text/S002-2.txt` (3559 chars).
- `.ufo/waves/round-26/statements.json` (41 pairs; S002 in 4 files, absent for this file); `.ufo/waves/round-26/rechecks/S002.json` (row HOLD, fetchIndex 1, prior sha256 values).
- `corpus/SOURCES.md:10` (S002 row: scope, anchor, teaches), `:9-14` (S001-S006 rows).
- `corpus/knowledge/ghp-served-set.md:25-27` (S002 quotes), `:93` (v3.0.1 half re-attributed to S002).
- Live 2026-10-21: `https://github.com/actions/upload-pages-artifact/releases` (atom feed) — newest release v5.0.0, 2026-04-10.

## 10. Tooling / transaction record

No tool install, upgrade or service mutation was needed or performed; no pacman transaction (all pacman transactions are PAUSED host-wide and untouched). Reads used `read`, `grep`, `bash` (git/awk/sha256 computation) and `write` for this report only. Network access was limited to the two named public GitHub release pages and the public release feed; no account, credential, cookie, property or publication operation was performed.
