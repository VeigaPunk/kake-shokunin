# ScoutUncommitted — untracked paths at the lane root

Seat: ScoutUncommitted (scout). Axes: operability, freshness. Read-only classification. This seat did not `git add`, delete, or edit any classified path, and did not run `jj`.

HEAD: `1c846ed2d67b1692ea966be064f0fc04542763c6` (detached). Census: `git status --porcelain=v1 --untracked-files=all` at `2026-10-25T00:38:05Z` from `/home/vgpnk/Projects/shokunin/kake-shokunin`. `git ls-files --others --exclude-standard` count: 26. `git diff --name-only` count: 0. Immediate children of the repo root: none untracked. Ignored others (`git ls-files --others -i --exclude-standard`): 5987, not classified.

Short porcelain collapses `.ufo/waves/round-46/residual/` and `.ufo/waves/round-49/w1/` into directories. The split below is the `-uall` view.

## Verdict

Two durable leftover classes stay separate, and both are still untracked.

- **A. Orchestrator-owned residual reports:** 8 files, all under `.ufo/waves/round-46/residual/`, all far under 1 MiB. Not validate copies.
- **B. >1 MiB validate copies:** 9 files, all under `.ufo/waves/round-48/assimilation/validate/`, each larger than 1048576 bytes, each byte-identical to an already-tracked source. Not residual reports.
- **C. This round's wave artifacts:** the other 9 paths in the snapshot (2 verification receipts, `w49-spec.json`, `w1/swarm-registry.json`, 5 sibling seat reports). Neither A nor B. `w1/` was still being written; later reports in that directory are the same class unless a path appears outside it.

Do not sweep A into a lane commit. Do not treat B as missing mirror content or as something a directory-track commit will pick up.

## A — orchestrator-owned residual reports

Directory listing is exactly these eight names. `git ls-files -- .ufo/waves/round-46/residual` is empty. `residual-spec.json` is tracked and is not one of the reports.

| path | bytes | mtime (-0300) |
|---|---:|---|
| `.ufo/waves/round-46/residual/SentinelBounds.md` | 1335 | 2026-10-24 03:26:21 |
| `.ufo/waves/round-46/residual/CriticMatrixBlindness.md` | 5090 | 2026-10-24 03:28:11 |
| `.ufo/waves/round-46/residual/ScoutSiblingOverlap.md` | 6633 | 2026-10-24 03:28:32 |
| `.ufo/waves/round-46/residual/MutationSemanticsGap.md` | 14369 | 2026-10-24 03:29:23 |
| `.ufo/waves/round-46/residual/ReviewReceiptIdentity.md` | 14304 | 2026-10-24 03:31:23 |
| `.ufo/waves/round-46/residual/ReviewWitnessOracle.md` | 18737 | 2026-10-24 03:33:52 |
| `.ufo/waves/round-46/residual/CriticCitationOverreach.md` | 10722 | 2026-10-24 03:34:34 |
| `.ufo/waves/round-46/residual/ReviewQualityCriterion.md` | 16258 | 2026-10-24 03:37:28 |

Largest is 18737 bytes. None is a validate copy.

Ownership, not inferred from the directory name:

- Tracked `.ufo/waves/round-46/residual-spec.json` names the wave `kake-r46-residual` and says the wave was prepared by the L1 and dispatched by the orchestrator. The eight filenames match that spec's eight task names and no others.
- `corpus/lessons/round-48.md` mistake 1: the eight reports "are orchestrator-owned (they were dispatched by the orchestrator, not by this lane) and stay uncommitted and untouched".
- `corpus/lessons/round-49.md` considerthese: "The eight residual reports stay uncommitted and untouched," and names `CriticCitationOverreach.md` as still uncommitted and orchestrator-owned.
- `corpus/lessons/round-48-verifier-spotcheck.md` routed defect 4: operator, not the lane; the eight reports stay uncommitted orchestrator evidence.

Freshness: mtimes are 03:26–03:37 -0300 on 2026-10-24, before the round-48 launch recorded in fleet `MANIFEST.json` notes (`2026-10-24T19:58:12-03:00 launch kake round=48`). They are not round-49 work.

## B — >1 MiB round-48 validate copies

1 MiB here is 1048576 bytes. All nine are above it (`min` 1283159, `max` 4620210, `at_or_below` 0). `git ls-files --others --exclude-standard -- .ufo/waves/round-48/assimilation/validate` count is 9. Tracked files under that tree: 7732. Each copy is absent from the index. Each source is tracked. `cmp -s` against the source (validate prefix stripped) was identical in every pair.

| untracked copy | bytes | tracked source |
|---|---:|---|
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-21/anchors-fixed.json` | 2355487 | `.ufo/waves/round-21/anchors-fixed.json` |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-36/realrun/snap-bodies-run2.tar.xz` | 1808836 | `.ufo/waves/round-36/realrun/snap-bodies-run2.tar.xz` |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-36/realrun/snap-bodies.tar.xz` | 1811344 | `.ufo/waves/round-36/realrun/snap-bodies.tar.xz` |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-37/sealed/cases.json` | 2777011 | `.ufo/waves/round-37/sealed/cases.json` |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-39/sources/xmlschema11-2.html` | 1508774 | `.ufo/waves/round-39/sources/xmlschema11-2.html` |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-40/sources/xmlschema11-2.html` | 1508774 | `.ufo/waves/round-40/sources/xmlschema11-2.html` |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-41/realrun/sitemaps/nodejs.xml` | 1652267 | `.ufo/waves/round-41/realrun/sitemaps/nodejs.xml` |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-41/realrun/sitemaps/postgresql.xml` | 4620210 | `.ufo/waves/round-41/realrun/sitemaps/postgresql.xml` |
| `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py` | 1283159 | `.ufo/waves/round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py` |

Why they stay untracked: `scripts/hyaku/jj-lane.sh` records that `--include-ignored` (which also admits files over `snapshot.max-new-file-size`) applies only to named files; a named directory is tracked like `git add <dir>`. This seat did not run `jj` and did not read a repo-local override (`~/.config/jj/config.toml` has no `max-new-file-size`). The closure note in fleet `MANIFEST.json` and `corpus/lessons/round-48-verifier-spotcheck.md` both state the cap is `1MiB` and that these nine were skipped. The size measurement above is this seat's; the cap value is cited, not re-queried from `jj`.

Freshness: the copies add no bytes the tracked sources do not already have. They are not a newer registry.

## C — round-49 wave artifacts (not A, not B)

Present in the same porcelain, all under 20 KiB:

- `.ufo/waves/round-49/verification/c1-after-1c846ed2.json` — 332 bytes, mtime 2026-10-24 21:34:49 -0300. Schema `kake-r49-c1-counter-v1`, revision `1c846ed2…`.
- `.ufo/waves/round-49/verification/c2-after-1c846ed2.json` — 664 bytes, same mtime. Schema `kake-r49-c2-counter-v1`.
- `.ufo/waves/round-49/w49-spec.json` — 15448 bytes, mtime 2026-10-24 21:35:50 -0300.
- `.ufo/waves/round-49/w1/swarm-registry.json` — 17264 bytes, mtime 2026-10-24 21:36:01 -0300. `createdAt` `2026-10-25T00:36:01.761Z`.
- `.ufo/waves/round-49/w1/ExecCensusLane.md` — 2889
- `.ufo/waves/round-49/w1/ExecQuoteBlob.md` — 2477
- `.ufo/waves/round-49/w1/ExecRerunC2.md` — 1947
- `.ufo/waves/round-49/w1/ScribeGateQuotes.md` — 1856
- `.ufo/waves/round-49/w1/ScribeRowShape.md` — 2922

These are this wave's own untracked outputs. They are not the round-46 residual queue and not the nine large copies. Sibling seats were still writing under `w1/` at the snapshot (five reports had landed; the registry lists more seats). A later `??` path under `.ufo/waves/round-49/w1/` is class C. This file is class C once written.

## Separation

A and B must not be counted as one leftover. A is small, older than the round-48 launch, orchestrator-dispatched, and absent from the index — a pathspec add could absorb it. B is nine copies over 1 MiB of sources that are already tracked — a directory track of `assimilation/validate/` does not admit them, and `cmp -s` says they are not new content. C is in-round and still growing; it is not the durable queue named in the round-48 and round-49 lessons.

Not done: no delete, no add, no `jj`, no edit of residual reports or validate copies.

Report: `.ufo/waves/round-49/w1/ScoutUncommitted.md`
