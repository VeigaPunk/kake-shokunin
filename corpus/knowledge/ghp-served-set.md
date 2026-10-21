source: S001, S002, S003, S004, S006, S008 (corpus/SOURCES.md) — https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml §Archive artifact
verified-at: 2026-10-19 (v4.0.0 commit 7b1f4a7; current action commit 5f327015)
recheck: on action release or workflow change — for v in v3.0.1 v4.0.0 main; do printf '%s ' "$v"; curl -fsSL "https://raw.githubusercontent.com/actions/upload-pages-artifact/$v/action.yml" | grep -cF -- '.[^/]*'; done

# GitHub Pages workflow artifact membership

**Claim (falsifiable).** For an Actions workflow uploading `path: .`,
`upload-pages-artifact` excludes `.git` and `.github`; v4.0.0 excludes
dot paths by default. The pinned current action also defaults
`include-hidden-files` to `false` while excluding `.git` and `.github`
regardless. Thus the archive can omit checkout paths; it does not alone
establish a live site's membership.

**r20-correction at base `cb807bc`.** Refines `corpus/README.md:26,52-55`,
`SKILL.md:227`, `corpus/knowledge/sitemap-orphan-audit.md:20-30`, and
`corpus/lessons/round-7.md:20-25`: checkout membership alone was used as
a proxy for publication. `corpus/knowledge/publish-channels.md:5-14`
distinguishes Actions from branch publishing.

**Source checks (quotes reopened 2026-10-19).**
- S001, pinned `action.yml` Archive steps: v4.0.0 excludes `.[^/]*` in all
  three OS steps; v3.0.1 does not. Current commit conditionally excludes it
  unless `include-hidden-files: true`; input quote: “Include hidden files
  and directories (those starting with a dot) in the artifact.”
- S002, v4.0.0 release, What's Changed: “Potentially breaking change:
  hidden files (specifically dotfiles) will not be included in the artifact”
  — v5.0.0 release notes announce the input.
- S003, About publishing sources: “the source folder can either be the
  root of the repository (`/`) or a `/docs` folder.” S004 steps 4-5 upload
  static files and deploy the artifact. S006's Jekyll defaults skip
  `node_modules`, `vendor`, names starting `_`, `.`, or `#`, and names
  ending `~` (quote: “Start with `_`, `.`, or `#`”); not every workflow
  uses that build path.
- S008, GNU tar 1.35, Controlling Pattern-Matching: “Default is
  `--no-anchored` for exclusion members and `--anchored` inclusion members.”
  Exclusion defaults also let wildcard `*` match `/` in a member name.

**Rechecks (2026-10-19).** Header dotfile loop returned `v3.0.1 0`,
`v4.0.0 3`, `main 3`. The `.github` loop
`for v in v3.0.1 v4.0.0 main; do printf '%s ' "$v"; curl -fsSL "https://raw.githubusercontent.com/actions/upload-pages-artifact/$v/action.yml" | grep -cF -- '--exclude=.github'; done`
returned `v3.0.1 3`, `v4.0.0 3`, `main 3`.

Local tar depth repro, with the temporary fixture removed after listing:
```
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT; mkdir -p "$d/.well-known" "$d/a"; touch "$d/.nojekyll" "$d/.well-known/x" "$d/a/.keep" "$d/a/b" "$d/CNAME"; tar --directory "$d" -cf - --exclude=.git --exclude=.github '--exclude=.[^/]*' . | tar -tf - | sort
./
./a/
./a/b
./CNAME
```
The fixture's `.nojekyll`, `.well-known/x`, and `a/.keep` were absent.
**[INFERENCE]** The depth result follows from GNU tar's unanchored exclusion
and slash-matching defaults plus this repro; GitHub's action source alone
does not specify that matching detail.

**Named debt.** Workflow action tag, upload path, and hidden-file option in
ds4cc/plazir remain unavailable after the 2026-10-12 prune. Owner:
operator/webzites; re-open those workflows before asserting a deployed payload.

**Prediction, not a claim.** Since `CNAME` is not excluded, a root upload may
package it; public service at `/CNAME` remains unverified and needs an
operator-authorized free read. Not probed.

## How it clears corpus/QUALITY.md
- **Replayable claim:** records pinned action revisions, exact argv, and outputs.
- **Missing substrate stays visible:** workflow inputs remain named debt with an owner.
- **Admission authority:** action, platform docs, and GNU tar manual are cited at their scoped sources.
- **Citation-local absence:** superseded coverage lines are named; no deleted checkout path is used as evidence.
- **Shape-only probe environment:** no API credentials or live-target output is recorded.

## Post-review correction — round 20 (2026-10-19)

S008 version erratum: the “GNU tar 1.35” label at original line 34 is
withdrawn. The cited source is the GNU tar manual text at commit
`cfdb891bbd68c920ea75210977593f3cd08f0418`, not evidence of release 1.35; it
uses `@value{VERSION}`. The exclusion-default quotes (lines 8587–8588 and
8602 in the reviewer-opened source) remain supported. The SOURCES anchor
range 8478–8617 and the gate range 8478–8603 both contain those lines; use
the exact quote lines, not an inferred release label.

## Round-26 source recheck

- Round-26 source recheck (2026-10-21, append-only; original lines unchanged). Rows S001, S002, S003, S004, S006 and S008 were re-fetched by one public GET each (`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`) and judged HOLD at their anchors against the retained bytes; receipts `.ufo/waves/round-26/rechecks/S0NN.json`, statement-level reviews `.ufo/waves/round-26/w1/Pair*.md`. Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten. Pointers labelled `at base cb807bc` stay base-scoped (QUALITY.md round-21 coordinate rule), so current-tree line movement is not a stale claim. Counting command: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`.

- [r26-recheck S003 STALE] The r20-correction sentence at line 17-18, “`corpus/knowledge/publish-channels.md:5-14` distinguishes Actions from branch publishing”, was false already at base cb807bc: those lines describe two Actions workflows and a setup script. The Actions-versus-branch distinction is S003's own text (“About publishing sources”, re-fetched 2026-10-21): “You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.” Evidence: w1/PairS003GhpServedSet.md (C1).

- [r26-recheck S003 STALE] The S003 bullet at lines 28-29 is not a verbatim quote. The 2026-10-21 bytes read: “the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch.” The root-or-/docs substance is unchanged; the earlier wording dropped “on the source branch” twice. Evidence: w1/PairS003GhpServedSet.md (C2).

- UNVERIFIABLE this round (not STALE): the four upload-pages-artifact v3.0.1 statements. S001 pins only v4.0.0 and main, and no v3.0.1 bytes are retained under round 26 (w1/PairS001GhpServedSet.md). They remain historical claims until a pinned v3.0.1 source is opened.
