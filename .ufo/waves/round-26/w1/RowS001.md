# RowS001 — actions/upload-pages-artifact action.yml (freshness re-check, round 26)

```json
{"id":"S001","verdict":"HOLD","fetchIndex":2,"quote":"(those starting with a dot) in the artifact. Excludes.git and.github regardless.","anchorObserved":"Main-commit copy (S001-2): inputs.include-hidden-files lines 17-20; Linux Archive artifact exclusion block lines 37-39 (same unconditional .git/.github pair repeats at 55-56 macOS and 73-74 Windows)","reason":"Main-commit copy exposes include-hidden-files (default \"false\") that gates only the dotfile exclude, while --exclude=.git and --exclude=.github remain unconditional in all three OS archive steps; the v4.0.0 copy (S001-1) has no such input and hard-codes --exclude=\".[^/]*\" three times, exactly the split the row attributes to S002. Scope and teaches still hold.","correction":null}
```

Caveats (≤10 lines):
1. Line anchors 17-20 and 37-39 resolve only in the main-commit copy; at v4.0.0, lines 17-20 are `outputs:`/`artifact_id`, so the row's "v4.0.0 tag" is a second pin, not an anchor for the input.
2. Both URLs are commit-pinned and returned 200 today (sha256 `4524ed61c2fb…` = v4.0.0, `e8ce828a4f2a…` = main); this recheck therefore tests availability + anchor, not content drift.
3. v4.0.0 body pins `actions/upload-artifact@ea165f8d…` (#v4.6.2); main body pins `…@043fb46d…` (#v7.0.1) — an upload-artifact pin change outside S001's scope, relevant to the on-release cadence.
4. Tag identity 7b1f4a7 = v4.0.0 corroborated by the round's S002-1 fetch ("v4.0.0 7b1f4a7"), so the SHAs are not mislabeled.
5. Tooling: none installed or upgraded (zcat/python3 already present).
