# Lesson14 — round-8 lesson retrospective Gate (round 21)

## Scope and behavior

- Target: `corpus/lessons/round-8.md` (sole owned file). No other file edited; no commits.
- Pre-state: no `## Gate` heading present (exact or otherwise). Action: appended a retrospective `## Gate — round-21 retrospective reconstruction` section at EOF. Labeled as reconstruction, not original admission.
- Prior bytes: preserved. `head -c 3264` of the new file hashes to `13fb8c895f93e6133b97506ef82df90ded88f04436376a5b009fe6f5f0a27407`, the pre-edit whole-file sha256.

## Line counts and bytes

- Old: 58 lines, 3264 bytes (ends `\n`).
- New: 86 lines, 7193 bytes. Appended lines 59-86 (line 59 blank, line 60 heading).

## Evidence basis for the appended Gate

- Original sections: lines 1-8 (cites), 10-15 (gap closed), 17-40 (what the audit found), 42-58 (learned).
- `LOG.md:12` (round-8 entry) and `LOG.md:13` (round-9 correction to 75 locs).
- `corpus/knowledge/kimi-subpath-audit.md` (entry table, errata at 39-43, procedure at 71-86).
- `corpus/knowledge/free-read-verbs.md:211` (cites 75/93).
- `.ufo/waves/round-21/wave1-spec.json` Lesson14 prompt (S019 metadata-contract reference, `verified-at`/`recheck` shape).
- Convention: `corpus/lessons/round-20.md:41-60` (`## Gate` layout, `Outside spot-check` wording).
- Round-21 lesson `corpus/lessons/round-21.md`: not present at read time; not depended on.
- Outside spot-check: not recorded. Only later review is in-lane errata (`kimi-subpath-audit.md:39-43`), not an outside verifier.

## Findings

1. **74 vs 75 supersession.** Original lines 19-25 say 74 missing; the sitemap commit `f3d2ecd` yields 75 `<url>` entries and the record (`kimi-subpath-audit.md:39-43`, `LOG.md:13`, `free-read-verbs.md:211`) uses 75. The Gate records this as a supersession. The original line was not edited.
2. **44 same-origin links not reconciled.** Original line 32 ("44 same-origin links GET'd, 0 real non-200"). The `kimi-subpath-audit.md` table (lines 53-65) sums to 33 across its nine listed rows; the ds4cc row's link count is absent from the table. Gate marks the count unverified; zero-real-non-200 admitted with qualification.
3. **S019 contract text absent from corpus.** Grep of `corpus/` for `S019` returns no match; the only in-repo reference is the round-21 wave spec, which says L1 will register canonical `CORPUS.md`. `CORPUS.md` is absent at repo root at read time. The Gate cites S019 as metadata-contract authority only, and asserts no S019 row as verified.
4. **Transient evidence.** `/tmp/kimi_audit.py` and `/tmp/kimi-subpath-audit.json` are cited as evidence but are transient artifacts (`kimi-subpath-audit.md:3`). Gate recheck instruction names this as an operator restore-or-retire item. Not checked for existence (no live-state reads).
5. **Unverified in round 21:** `kimi-surface.mjs` :459-466 vs :903-908 payload claim; orphaned 09-26 `update` fire (code 7); kimi-map updateTimes whitelist claim. Not re-read.

## Tools

- Installed or updated: none.

## Verification

- Ran no build, lint, or test. Read-only checks only: `sha256sum`, `wc -lc`, `head -c 3264`, `od`, `sed -n`, `git status --short -- corpus/lessons/round-8.md` (shows ` M`, expected).

## Checks for the main agent

- `head -c 3264 corpus/lessons/round-8.md | sha256sum` equals `13fb8c89…7407`.
- `grep -n '^## Gate' corpus/lessons/round-8.md` shows exactly one match (line 60, `## Gate — round-21 retrospective reconstruction`).

## Out of scope / not touched

- `SCORECARD`, `LOG`, `QUALITY`, `SOURCES`, `README`, `SKILL`, `CORPUS.md`, `corpus/lessons/round-21.md`, and all other lessons: untouched.
- Operator-owned: restore or retire `/tmp` kimi audit artifacts; register S019 in canonical `CORPUS.md` (L1).
