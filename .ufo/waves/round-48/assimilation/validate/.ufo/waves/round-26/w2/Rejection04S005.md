# Rejection04S005: falsify attempt on L1's rejection of S005 C2 (`publish-channels.md:9`)

- Target: `.ufo/waves/round-26/statements.json` row S005 / `corpus/knowledge/ghp-custom-domain.md`, `l1Disposition`: "C2 publish-channels.md:9 is base-scoped and correct at cb807bc." Seat finding under attack: `w1/PairS005GhpCustomDomain.md` P06 / C2 (STALE: "`publish-channels.md:9`, now `:13`").
- Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`. Judged on: freshness. Milestone: r26-recheck-falsify.
- Verdict: **AGREE**. At its own stated scope the statement is correct, so the rejection does not hide any staleness. The seat's own C2 text concedes "The attribution claim itself still holds"; it graded a coordinate move as STALE, which QUALITY round-26 bullet 2 forbids.

## Axes

1. Scope: does the statement name its own revision?
2. Truth at scope: is the pointer target the attributed line at that revision?
3. Mechanism: does the "depends on publishing mode" half still hold against the 2026-10-21 S005 bytes?
4. Coverage: does any pointer in this S005 pair lack a scope label and also fall outside the round-21 register?
5. Provenance of the L1 note appended to the corpus.

## Evidence

**Axis 1, scope.** The line under attack labels its own revision. This is base `97404de` line 13, `git blame` → `02b6dd0` (round 20, 2026-10-19):

```text
13 **r20-correction at base `cb807bc`.** Refines `corpus/knowledge/publish-channels.md:9`
14 and `SKILL.md:16`: those lines attribute the domain to a repository file,
15 whereas the documented mechanism depends on Pages publishing mode.
```

QUALITY.md:217-221 (round 26): "A historical verified-at date, a pointer explicitly scoped to a base revision, … is not a stale claim; record it as a note. A statement whose attribution was false even at its base revision is STALE." Only the last sentence could make this STALE, so axis 2 decides.

**Axis 2, truth at scope.**
- `git rev-parse cb807bc` → `cb807bc8d8bc94be1268e4741191bb3d5e518565`. `git merge-base --is-ancestor cb807bc 97404de…` → ancestor.
- `git show cb807bc:corpus/knowledge/publish-channels.md` line 9: `` `CNAME` file pins `ds4cc.com`. `` This attributes the domain to a repository file, as line 14 says.
- `git show cb807bc:SKILL.md` line 16: "GH Actions on push to `main` (`CNAME` = ds4cc.com)". This is the same attribution.
- Line 9 stayed stable across every revision where the pointer could have been read:
  - `02b6dd0`, `9639ec7` and `df6196b^`: line 9 is still the CNAME line. At `02b6dd0` an inline r20 bracket was appended to the same line, which did not renumber anything.
  - Round-21 baseline `5009ecaa` (an ancestor of base): `:9` is the CNAME line.
  - `git diff cb807bc 5009ecaa -- publish-channels.md` has its first hunk at `@@ -28`, so lines 1–27 are identical.
- The only renumbering is `df6196b` (round 21), `@@ -1,3 +1,7 @@`: three metadata lines plus a blank line, so +4. `git diff df6196b 97404de…` has its first hunk at `@@ -59`. So the base-tree line 13 is the CNAME line, and the seat's ":13" is just the +4 coordinate.

**Axis 3, mechanism, against the retained bytes.** `zcat fetched/S005-1.raw.gz | sha256sum` → `dc89eecd…e0cee9`, which matches the manifest. In `fetched/text/S005-1.txt`:
- `grep -oF` "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored" → 2.
- `grep -oF` "If you are publishing your site from a branch, this will create a commit that adds a CNAME file directly to the root of your source branch" → 2.

Mode dependence is still documented. `rechecks/S005.json` is HOLD on the Actions sentence at both step-4 anchors.

**Axis 4, strongest counterexample tried.** Line 35 (Named debt), `` (`SKILL.md:16`; `corpus/knowledge/publish-channels.md:5-9`) ``, has **no** "at base" label. At base, `publish-channels.md:5-9` is the title, a blank line, the H2 and the bullet head, not the ds4cc bullet. Even so, it is not stale:
- `git blame` puts it in `02b6dd0`, so it is a pre-round-21 pointer.
- `corpus/lessons/round-21.md:110-139` ("Inbound-pointer correction register") lists `| publish-channels.md | N → N+4 |` with "Ranges shift both endpoints by four". That maps `5-9` to `9-13`, which is exactly the ds4cc `pages.yml` bullet at base.
- QUALITY.md:69-73 adopts that register.

This line was also outside the C2 finding: the seat routed it "out of pair". The counterexample fails.

**Axis 5, provenance (low, non-blocking).** The candidate appends to `ghp-custom-domain.md` (diff `@@ -56,3 +56,7 @@`): "Pointers labelled `at base cb807bc` stay base-scoped (QUALITY.md round-21 coordinate rule)". The round-21 rule (QUALITY.md:69-71; round-21.md:116) defines its baseline as `5009ecaa`, not `cb807bc`. Base-scoping of a `cb807bc` label comes from the label itself plus QUALITY round-26 bullet 2. The two baselines happen to agree here, because lines 1–27 of `publish-channels.md` are byte-identical between them, so no reader reaches a wrong line. The citation is imprecise, not false in effect.

## Impacted axes

- Freshness: none. No stale statement is hidden by the rejection.
- Provenance: low. The base-scoping is credited to the wrong rule (axis 5).

## Smallest safe correction

The rejection itself needs no correction. Optionally, in a later append-only note, cite QUALITY round-26 bullet 2 ("a pointer explicitly scoped to a base revision") for `at base cb807bc` labels. Keep the round-21 coordinate rule only for unlabelled pre-round-21 pointers such as line 35's `publish-channels.md:5-9` → current `9-13`.

## Commands run (read-only)

`rg` over `statements.json`, `population.json` and the manifests; `git show` of `{cb807bc,02b6dd0,9639ec7,df6196b^,5009ecaa,97404de}:corpus/knowledge/publish-channels.md` and `ghp-custom-domain.md`; `git show {cb807bc,97404de}:SKILL.md | sed -n 16p`; `git blame -L 13,15 -L 34,35 97404de -- corpus/knowledge/ghp-custom-domain.md`; `git rev-parse cb807bc`; `git merge-base --is-ancestor` for `cb807bc` and `5009ecaa`; `git diff` hunk headers for `cb807bc..5009ecaa`, `df6196b..97404de` and `97404de..e28312b` (ghp-custom-domain); `git log` for both entries; `zcat S005-1.raw.gz | sha256sum`; `grep -oF … | wc -l` on `S005-1.txt`. Nothing fetched from the network and nothing written except this report.

## Tooling

No installs or upgrades. Used the existing git, ripgrep, grep, zcat and sha256sum. pacman not touched (host-wide pause).

```json
{"target":"S005 l1Disposition C2 publish-channels.md:9 base-scoped rejection","verdict":"AGREE","severity":"none"}
```
