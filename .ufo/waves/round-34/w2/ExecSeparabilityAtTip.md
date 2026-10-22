# Round 34 wave 2 — claim separability at tip

Axes: operability (C1) and freshness (C2).

## Result

Neither score depends on the other claim's files in these tested removals. A removes only `scripts/link_preview_audit.py`: C1 scores 0/28 (expected absent-tool result), while C2 stays 5/5. B starts again from tip and removes `corpus/knowledge/link-preview-metadata.md` plus the S067–S070 registry rows: C1 stays 28/28, while C2 scores 0/5. C1's constants were all rejected in both runs; C2's control was not broken in either run.

Variants in sandbox clone `/fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/clone`:
- Tip: `24a16474ee73e20453f3e1be9d2f33573c5196d9`.
- A: `70275c0733b728271ee44e227b7c1b5bbe5e7eed`; commit removed only `scripts/link_preview_audit.py` (1 file, 259 deletions).
- B: `b3340f20b38254acad330686854d862c37608ac8`; commit from tip removed the metadata entry and four registry rows (2 files, 226 deletions).

## Commands and outputs

All four commands used the isolated `TMPDIR=/fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/tmp`, unset `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`, and redirected stdout/stderr to the receipts below. Exact command invocations (as executed inside `set +e; ...; rc=$?; printf 'exit=%s\\n' "$rc"; cat <stderr>`):

- A/C1: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/tmp python3 -B .ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/clone --revision 70275c0` → exit 1; `C1 0/28 at 70275c0733b728271ee44e227b7c1b5bbe5e7eed`.
- A/C2: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/tmp python3 -B .ufo/waves/round-34/c2_source_census.py --root /fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/clone --revision 70275c0` → exit 0; `C2 5/5 at 70275c0733b728271ee44e227b7c1b5bbe5e7eed`.
- B/C1: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/tmp python3 -B .ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/clone --revision b3340f2` → exit 0; `C1 28/28 at b3340f20b38254acad330686854d862c37608ac8`.
- B/C2: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/tmp python3 -B .ufo/waves/round-34/c2_source_census.py --root /fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/clone --revision b3340f2` → exit 1; `C2 0/5 at b3340f20b38254acad330686854d862c37608ac8`.

## Retained evidence

The complete JSON stdout and exact stderr are retained in the sandbox; `sha256` follows each JSON receipt. `path:line` points to score and resolved revision:
- A/C1 `/fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/A-c1.json:4-10`, sha256 `7cd7d1a777a06116302e19ea936d58c62d57a8a5b578ca8de2d38b1a43a33772`; stderr `A-c1.stderr:1`, sha256 `532cbaf1a29bd9b8e2218c165b9caf25d07640e08831539785cb27a69502ac96`.
- A/C2 `/fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/A-c2.json:4-6`, sha256 `50f5540d70700c9d6d7f14069717ce984466a6a1a7d4fda49da9f5e02256f730`; stderr `A-c2.stderr:1`, sha256 `d3b5049afe15496cfb4cfd7b6f5f02e618094ea1c8ad15cd21e6876b19f7934a`.
- B/C1 `/fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/B-c1.json:4-10`, sha256 `89531932150dbb00ba6a7f8c5cf34e6a196aced38168ef0dd6fbaaa74fcd3c02`; stderr `B-c1.stderr:1`, sha256 `fba65da3d4b069cd6ccb3e91bff62380b232039933fb6f069d59ed2024b90de1`.
- B/C2 `/fast/scratch/hyaku/kake-r34/w2/ExecSeparabilityAtTip/B-c2.json:4-6,11-13,22-25,33-36,44-47,55-67`, sha256 `fb72a1ea6a4c9b424c47425d417af0d69db081adc709b39516c28bb79b99f125`; stderr `B-c2.stderr:1`, sha256 `5ce2eb8932ede40fdb3910e0632847430420e8d7ac21f7638962175647fb8a24`.

## Scope, risks, blockers

C2's B mutation removes the entry and all four registry rows together, so this run does not measure their separate individual contribution; it does show C1 is unchanged by that combined removal. No additional build, lint, test, or format check was run. No tools were installed. No blocker.