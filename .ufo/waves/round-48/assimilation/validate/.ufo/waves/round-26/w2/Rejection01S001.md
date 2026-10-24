# Rejection01S001 — falsify L1's rejection of three S001 pointer-drift findings

Axis: freshness. Milestone: r26-recheck-falsify. Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.

Target: `.ufo/waves/round-26/statements.json` pair S001 × `corpus/knowledge/ghp-served-set.md`, `l1Disposition`:
"3 anchor-drift findings rejected: the r20 tail scopes README/SKILL/sitemap pointers explicitly "at base cb807bc"; current-tree movement is covered by the QUALITY round-21 coordinate rule."
The seat findings are rows 11–13 of `w1/PairS001GhpServedSet.md` (corrections C1–C3).

## Verdict: AGREE on the outcome. The second justification cites the wrong authority, a low-severity defect.

The statement is true at its own stated scope, so the rejection does not hide any staleness. However, the second ground in the disposition ("covered by the QUALITY round-21 coordinate rule") is false for two of the three pointers. Applying that rule would land a reader on the wrong lines.

## Evidence

### 1. The statement's scope is explicit

`git show 97404de:corpus/knowledge/ghp-served-set.md`, lines 14–16:
`**r20-correction at base `cb807bc`.** Refines `corpus/README.md:26,52-55`, `SKILL.md:227`, `corpus/knowledge/sitemap-orphan-audit.md:20-30`, and `corpus/lessons/round-7.md:20-25`: checkout membership alone was used as a proxy for publication.`

- `git blame` shows these lines were written in `02b6dd0` (round-20).
- `git log cb807bc..02b6dd0` returns only `02b6dd0`, so `cb807bc` is the base the author worked from.
- `cb807bc` resolves uniquely to `cb807bc8d8bc94be1268e4741191bb3d5e518565`, and `git merge-base --is-ancestor cb807bc 97404de` returns true.

### 2. Every pointer is correct at `cb807bc`, so the strongest counterexample fails

I read each pointer with `git show cb807bc:<path>`:

- **`corpus/README.md:26`**: `| Sitemap/orphan audit | … GHP orphan impossibility proof (deploy = full-tree artifact) …`. This uses checkout membership as a proxy, as the statement says.
- **`corpus/README.md:52-55`**: `- Live-only orphan paths: **closed 2026-09-28** — GHP Pages deploys are full-tree artifacts, so the served set ≡ `origin/main` tree; …`. Proxy, as stated.
- **`SKILL.md:227`**: `| URL lists (sitemap) | … GHP live-only orphans impossible by construction (deploy artifact = full tree snapshot) …`. Proxy, as stated.
- **`corpus/knowledge/sitemap-orphan-audit.md:20-30`**: line 20 `` `actions/upload-pages-artifact` + `actions/deploy-pages` deploy a `` … line 28 `does not exist on GHP — the live tree IS the last-pushed `origin/main``. The decisive sentence sits inside 20–30. The seat's "incomplete" flag only holds at current coordinates.
- **`corpus/lessons/round-7.md:20-25`**: line 22 `every deploy ships the entire checked-out tree as a fresh artifact.` Proxy, as stated (the seat also judged this one HOLD).

Every attribution is true at the stated revision. The only false pointer in this tail is `publish-channels.md:5-14`, which was false even at `cb807bc`. That pointer belongs to S003 and the candidate already records it as STALE (`ghp-served-set.md:85`). That is the case the round-26 rule's "false even at its base revision is STALE" clause is for, and it was applied there. No row in the S001 set falls under that clause.

The retained S001 bytes cannot test these three statements. They are intra-repo pointers and do not cite `action.yml` content. The seat's own rows 11–13 cite the S001 quote only as "premise".

### 3. The rule that actually governs the rejection

`corpus/QUALITY.md:217-221` (round-26 rule): "STALE means the statement is wrong or unsupported at its own stated scope. … a pointer explicitly scoped to a base revision … is not a stale claim; record it as a note. A statement whose attribution was false even at its base revision is STALE."

The ledger's `rule` field says the same: "base-scoped pointers are not stale." Rows 11–13 fall squarely under it, so the rejection is correct.

### 4. The round-21 rule does not cover README or SKILL, and applying it misreads them

`corpus/QUALITY.md:69-71`: "All pre-round-21 literal pointers into **knowledge entries** that receive the four-line metadata prefix retain their baseline coordinates. Add four…"

The per-file register at `corpus/lessons/round-21.md:110-141` sets "old line N at baseline `5009ecaa` is current line N+4". Its targets are only files under `corpus/knowledge/`, and lines 141–142 add "The other four knowledge entries and all original lesson lines retain their coordinates."

- README.md and SKILL.md are not in that register.
- Under the round-21 rule, a "pre-round-21 pointer" resolves at baseline `5009ecaa`, not at `cb807bc`. The two baselines disagree:
  - `git show 5009ecaa:corpus/README.md | sed -n 26p` gives `| Speedrun pipeline | …`, the wrong row.
  - `git show 5009ecaa:SKILL.md | sed -n 227p` gives `| Byte-twin copies | …`, the wrong row.
  - For comparison, `cb807bc:README.md:26` is `| Sitemap/orphan audit |`, the correct row.
- README.md changed in 6 commits and SKILL.md in 10 commits over `cb807bc..97404de` (`git log --format=%h -- <file>`). No register maps those changes.
- For `sitemap-orphan-audit.md`, the round-21 rule happens to give the right answer:
  - Lines 18–30 are identical at `cb807bc` and `5009ecaa`.
  - `cb807bc` lines 1–34 are byte-identical to base lines 5–38 (diff: IDENTICAL), so +4 gives 24–34.

So the "covered by the round-21 coordinate rule" ground holds for one pointer out of three. For README and SKILL it is false provenance. The candidate repeats the same citation in the shipped corpus, at `corpus/knowledge/ghp-served-set.md:83`: "Pointers labelled `at base cb807bc` stay base-scoped (QUALITY.md round-21 coordinate rule)". What actually keeps these pointers valid is the explicit `cb807bc` label, which can be resolved with `git show cb807bc:<path>`.

## Impacted axes

- **Freshness: none.** No stale claim is hidden; all four S001 pointers are true at `cb807bc`.
- **Provenance: low.** One inapplicable rule is cited as authority in the ledger `l1Disposition` and in the corpus note at `ghp-served-set.md:83`.
- **Duplicate authority: low.** The disposition cites two rules, and they resolve old pointers against different baselines (`cb807bc` and `5009ecaa`).

## Smallest safe correction

The disposition outcome and the counts (`stale: 0`, 3 rejected, 4 UNVERIFIABLE) stay as they are. Two citation edits are needed:

1. **Ledger `l1Disposition` for pair S001:** replace "current-tree movement is covered by the QUALITY round-21 coordinate rule" with "base-scoped pointers are notes, not STALE (QUALITY.md 'Recheck adjudication — round 26'); all four resolve correctly via `git show cb807bc:<path>`".
2. **`corpus/knowledge/ghp-served-set.md:83`:** append-only, matching the corpus convention. Add a follow-up note saying the `at base cb807bc` pointers resolve at `cb807bc` under the round-26 adjudication rule. It should also say the round-21 register, with baseline `5009ecaa` and only `corpus/knowledge/` entries, does not cover the README.md and SKILL.md pointers.

## Commands run

All read-only, with no writes except this report:

- `git log`, `git blame`, `git show <rev>:<path>`, `git diff 97404de e28312b -- corpus/knowledge/ghp-served-set.md`, `git rev-parse`, `git merge-base --is-ancestor`.
- `diff` on in-memory `git show` output.
- `python3` stdlib reading `statements.json`.

I installed or updated no tools, made no network GETs, and read no round-24 material.

```json
{"target":"S001 l1Disposition: 3 pointer-drift findings (README/SKILL/sitemap) rejected as base-scoped","verdict":"AGREE","severity":"low"}
```
