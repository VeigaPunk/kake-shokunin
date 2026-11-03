# Curated sources to consider — kake — batch 2 — 2026-11-03

**Status: unassimilated future reading after hyaku.** Source-candidate review only, not a training round, admission, readiness claim or change to the current plan. Public primary material checked on 2026-11-03 UTC. No candidate code or artifact was executed, no live target tested, no private artifact uploaded and no candidate implementation deployed.

## lychee: local publication-link semantics

[Primary repository](https://github.com/lycheeverse/lychee)

### Original summary

An offline link-checker implementation adds a concrete publishing question beyond batch-one markup validation and accessibility methodology: does a saved generated site's link resolve to the intended local file and fragment? The README distinguishes filesystem roots, base URLs, directory index files and fragment modes. Its offline fixture includes root-relative paths, spaces, encoded spaces and an anchor. These are useful implementation examples beside the lane's existing base-path/canonical rules, not evidence that deployed routing matches disk layout.

### Exact source and license

- Version: lychee-v0.24.2, published 2026-05-01T15:41:38Z; annotated tag object `e85aaf5524b2f808e63bae55e594c843220f10f2` peeled through the official GitHub API to commit `2bba271688c1abb1503097a064e6c3bc1d1b6a9b`. [Release](https://github.com/lycheeverse/lychee/releases/tag/lychee-v0.24.2)
- License: Apache-2.0 OR MIT, verified in the pinned repository's license text and Cargo manifest/README, rather than relying on GitHub’s single-license badge.
- Reading links: [README.md](https://github.com/lycheeverse/lychee/blob/2bba271688c1abb1503097a064e6c3bc1d1b6a9b/README.md) · [fixtures/offline/index.html](https://github.com/lycheeverse/lychee/blob/2bba271688c1abb1503097a064e6c3bc1d1b6a9b/fixtures/offline/index.html) · [LICENSE-APACHE](https://github.com/lycheeverse/lychee/blob/2bba271688c1abb1503097a064e6c3bc1d1b6a9b/LICENSE-APACHE) · [LICENSE-MIT](https://github.com/lycheeverse/lychee/blob/2bba271688c1abb1503097a064e6c3bc1d1b6a9b/LICENSE-MIT) · [lychee-bin/Cargo.toml](https://github.com/lycheeverse/lychee/blob/2bba271688c1abb1503097a064e6c3bc1d1b6a9b/lychee-bin/Cargo.toml)

### Proposed future review

After hyaku, prepare a paper-only expectation matrix for one already authorized saved build: root-relative URL, project-subpath URL, directory index, encoded-space path and missing anchor. Read README “Commandline usage”: `--offline`, `--root-dir`, `--base-url`, `--index-files`, `--include-fragments`; then `fixtures/offline/index.html`. Ask: which failures are missing content versus an incorrectly declared publication root? Record expected results without running the checker.

### Caveats

Offline results cannot establish remote status, redirects, JavaScript links or search indexing. Configuration and preprocess hooks require separate review before any future run; no execution is proposed here.

### Novelty check

No lychee/lycheeverse match in the supplied lane inventory or full context, including batch one. Existing base-path audits overlap in purpose; the new surface is explicit local resolution and fragment-checker behavior, not another HTML validator.

## Boundary

Any later adoption requires normal independent review after hyaku. Recheck pins and applicable notices first. This note changes no corpus registry, skill, scorecard, training input, authorization or deployment state.
