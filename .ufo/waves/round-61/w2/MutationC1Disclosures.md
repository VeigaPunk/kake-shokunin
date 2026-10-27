# MutationC1Disclosures

Detector: the committed `scripts/receipt_lineage.py` (`--json`) on an isolated scratch Git fixture with one frozen-path receipt, one rewrite event, and disclosures stored at the default path. The fixture is under `/fast/scratch/hyaku/kake-r61/MutationC1Disclosures/fix`; no lane source was changed. I also ran the tool at lane revision `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f`.

Baseline: exit 0, `receipts=1 events=1 undisclosed=0 met=True`. Real lane: exit 0, `receipts=95 events=12 undisclosed=0 met=True` (tool JSON reports `population=146`). The contract-specified `.ufo/waves/round-61/c61_lineage_cases.py` was not present in the lane at that revision, so no C1 counter result is claimed.

| Mutation | Actual result | Verdict |
|---|---|---|
| Omit `path` | exit 2; `disclosures entry 0 has no path` | Rejected |
| Wrong commit (receipt's first-add commit) | exit 1; `undisclosed_rewrite` plus `phantom_disclosure` | Rejected |
| Duplicate identical `(path, commit)` pair | exit 0; no findings | Accepted; both entries were marked matched |
| Wrong `kind` (`pending_filled` instead of `rewrite`) | exit 0; no findings | Accepted, consistent with A1 (matching ignores kind) |
| Blank `note` and `disclosed-by` | exit 0; no findings | Accepted; tool does not validate these fields |
| `entries: []` | exit 1; one `undisclosed_rewrite` | Rejected |
| Missing `entries` key | exit 2; `disclosures entries is not a list` | Rejected |
| Entry path set to committed directory/tree `.ufo/waves/round-10/control` | exit 1; event undisclosed and `phantom_disclosure` for the directory path | Rejected (path does not equal receipt path) |
| Entry path set to non-population `README.md` | exit 1; `phantom_disclosure README.md <commit>` | Tool emits phantom for non-population path; see A3 finding below |
| Worktree edits a disclosures file that exists at the revision | exit 0; committed JSON wins over worktree `entries: []` | Correct committed-blob precedence |
| Disclosures path absent both at revision and in worktree | exit 1; zero entries, one `undisclosed_rewrite` | Correct missing-file behavior |
| Worktree-only disclosures file at path absent from measured revision | exit 0 when run at the pre-disclosure revision; the worktree entry disclosed its rewrite | Tool falls back to uncommitted bytes, contrary to A3's committed-bytes-only rule |
| Absolute `--disclosures` path | exit 0 with the file's disk contents | Absolute-path behavior; disk input is used |

A3 discrepancy: it limits `phantom_disclosure` to entries naming a frozen population path with no event at that commit, but the tool reports an entry for `README.md` as phantom. A3 also says disclosures are read only from `<revision>:<path>` and a missing file means zero entries; the worktree-only default-path probe instead disclosed the event from an uncommitted file. These are observed contract mismatches, not proposed contract changes.

Restoration: pristine disclosure JSON SHA-256 before mutation and restored JSON SHA-256 were both `65e76f3344bfceb2bfc9bf4b8895e1aea09de6eedb1a67ff5892ed78eec2378e`. Restored run: exit 0, `receipts=1 events=1 undisclosed=0 met=True`. Fixture tool invoked from the lane's committed script; its checked-out bytes matched the committed file (blob `d2470d4c8ac063b2e26e92245deb98a9d614d1f2`). No tools installed.

MUTANTS: 13 disclosure mutations/probes (including separate empty-list, missing-key, worktree-precedence, absent-file, and uncommitted-file cases). KILLED: malformed/missing path, wrong commit, empty entries, missing entries key, mismatched directory path, and missing disclosure file produced nonzero exits. SURVIVORS: duplicate pair, wrong kind, blank note, and worktree edits to an already committed disclosures path were accepted. CONTRACT MISMATCHES: non-population phantom and worktree-only default-path fallback behaved contrary to A3.

VERDICT: A3 disclosure probes found two tool/contract mismatches (phantom scope and worktree-only fallback); the specified C1 counter was absent, so its outcome is unverified.
