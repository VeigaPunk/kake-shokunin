# ReviewHarmUnchanged — "v4 changes only generated inputs, not the tool" + H4 qualification

CONFORMANT — the tool is byte-unchanged since the round-42 build commit, the round-42 harm
receipts pin those same bytes, the SCORECARD round-43 section carries the H4 in-class-only
qualification, and v4's diff against v3 touches only input generation.

## Commands (all read-only git; cwd = lane repo)
1. `git diff --stat 020bc457… b49cba9… -- scripts/sitemap_audit.py` → empty, exit 0.
2. `git show 020bc457…:scripts/sitemap_audit.py | sha256sum` → `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`; same for `b49cba9…:…` and for the working-tree copy; `git status --porcelain scripts/sitemap_audit.py` clean.
3. `git log --oneline -- scripts/sitemap_audit.py` → last commit on the path is `020bc45 round-42: build — URL check rewritten as a byte-table scanner …; selftest 235`.
4. `git merge-base --is-ancestor b49cba9… HEAD` → exit 0 (HEAD `7c07079` = freeze + wave-1 bookkeeping); `git diff --stat b49cba9… HEAD` touches only `.ufo/waves/round-43/` wave files (no tool, no SCORECARD); tool at HEAD still `914ebdee…`.
5. `sha256sum .ufo/waves/round-43/c43_count_v4.py` → `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab` (= frozen value; committed blob `ecff943c` at `b49cba9`).
6. `git diff --no-index .ufo/waves/round-42/c42_count_v3.py .ufo/waves/round-43/c43_count_v4.py` → 319 insertions / 14 deletions; every deleted line is a docstring line or a `shape_t1/t2/t3/t5` generation body (hunk contexts all `def shape_t*`); `RUNNER`, `Sandbox`, tool-hash and scoring code untouched (copy: `/fast/scratch/hyaku/kake-r43/ReviewHarmUnchanged_v3v4.diff`).
7. `grep` over `c43_count_v4.py` for writes: only case dirs, the temp runner, and `--out`; the tool is read once (`open(a.tool_file, "rb").read()`, :987) to record `toolSha256`; no write/chmod/rename/shutil touches `scripts/sitemap_audit.py`.

## Per checked statement
- **Tool byte-unchanged since the r42 build commit — holds.** Zero diff over the tool path between `020bc457` (r42 build) and `b49cba9` (r43 freeze); identical sha256 at both commits, at HEAD, and in the worktree.
- **r42 harm receipts describe the same tool bytes — holds.** `verification/harm/h4-020bc457-{924141,42001}.json` both record `toolSha256: 914ebdee…` with inClass 19,750/19,720, validReject 0, newAccept 0, oracleDisagree 0 (matches SCORECARD r42 §). `harm/selftest-{build,tip41-235}-py314.txt` and `selftest-{build,tip41}-py310.txt` each `PASS 235/235`; `w2/ReviewHarmSelftest.md` ties those receipts to sha `914ebdee…` with fresh reruns on both interpreters. `w2/ReviewHarmRealRun.md`: build `914ebdee…` exit 1, `jq -S . | sha256sum` = `fd985a41867e…`, equal to rounds 39–41 hashes.
- **SCORECARD r43 carries the H4 qualification — holds.** SCORECARD.md:3242-3246: "Harm rule: unchanged from round 42 (H1 selftest 235 … H5 Python 3.10 selftest — v4 changes only generated inputs, not the tool). **H4 stays qualified, in-class only** (routed repair 3) … kept qualified until measured out-of-class."
- **Freeze receipts agree with the same tool bytes — holds.** `verification/freeze/build-{1,2,3}.json`: `revision 020bc457…`, `toolSha256 914ebdee…`, met true, equalRuns 11/11; every scoring receipt's `predicate` field equals v4's `PREDICATE` constant byte-for-byte (AST-extracted comparison: 8/8 true); r42ctl-{M8,v1,v2,v4} and ref41-base all met false (able to fail; junk 0/11).
- **No seat score predating the freeze observed** — all receipts examined are under the `b49cba9` tree.

## Findings
- None actionable. (My first predicate comparison printed False — extraction bug in my one-line regex, not a repo defect; the AST-extracted comparison supersedes it.)

## Residual risk and verification gaps
- I verified v4 by source diff/write-surface audit plus the receipts' recorded `toolSha256`; I did not execute v4 (scoring is other seats' item), so no runtime canary of tool immutability.
- Receipt-level selftest/H2 files do not embed the tool sha inline; the sha tie is via `ReviewHarmSelftest.md`/`ReviewHarmRealRun.md` and the h4/freeze receipts — adequate but indirect for those two.

Tooling: nothing installed or updated. No processes left running.
