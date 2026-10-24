# Knowledge16 — probe-delta-alerting.md provenance prefix (round 21, w1)

## Scope and change

Target: `corpus/knowledge/probe-delta-alerting.md` (only file changed).

- Pre-edit state: line 1 was the title. No provenance trio was present, so the prefix was added.
- Edit: pure prefix addition of 4 lines (`source:`, `verified-at:`, `recheck:`, blank line) before the title. No pre-existing byte changed.
- Prefix length: **1085 bytes, 4 lines** (file 7097 → 8182 bytes).
- Byte preservation: `tail -c 7097` of the new file has sha256 `562f1b888cd411d635d13a5763167255f531cf738f555623b1d86eb5b6e4b8f3`, equal to the pre-edit sha and to `frozen/before/expected.json`. Every original line is intact, including the in-body absence flags at original lines 18, 78 and 80, the r10 ground-truth correction, and the merged-row and absence-is-not-ok limits.
- Line shift: every original line now sits at +4. Line-pinned citations elsewhere will be stale until L1 re-pins them (see Downstream below).

## Evidence basis for the prefix

- `source:` is own-work. It names `scripts/probe-delta.mjs` (present in this repo, `ls scripts/` in this session), the history input `~/Projects/webzites/state/probe-history.jsonl` (its absence is recorded in the entry's own r18 annotation, and the `~/Projects/webzites/state` directory was not found when I measured), and the ground-truth records (`ops-automation.md`, the 2026-09-28 raw-row self-verification). It cites S019 only as the metadata contract, not as platform authority. SOURCES.md has no row for this entry (S001–S018 cover other topics; S014 is the freshness-path gate).
- `verified-at:` gives the original evidence date, 2026-09-28 (round-10 final run: 76 rows, 6 events, 0 phantom), and the in-entry re-pins and absence annotations with their dates. It is labelled `historical-not-live-reverified`. It does not claim a domain recheck.
- `recheck:` gives a read-only local command: a syntax-only `node --check` on the script, then a readability test and line count on the history file, falling back to `ABSENT`. It names the operator requirement for the absent case: restore the history file and re-derive, or retire the run-derived event claims as a historical record. No credential or auth files are referenced.

## Verification performed

- Read the whole entry (109 lines) before editing.
- Measured file size and sha256 before the edit.
- Measured the new size and checked the prefix line count and tail sha after the edit. These are the byte measurements the report needs.
- Did not run `node scripts/probe-delta.mjs`, the `recheck:` command, or any webzites command. No domain rechecks were run.

## Field audit / limits

- `S019` is not registered yet. `corpus/` has only QUALITY.md, README.md, SOURCES.md, and no CORPUS.md. The prefix refers to `corpus/CORPUS.md` as pending L1 registration. L1 must register S019 for this reference to resolve.
- The `recheck:` line uses `~/Projects/...` paths. Those are the same paths that round 20 and round 18 flagged as absent after the 2026-10-12 prune. The command is still valid as a reading command and is expected to print `ABSENT` until the operator acts.
- Count fields (e.g. 78 rows / 67 full sweeps) stay in the body. Count coverage is L1's job and was not touched here.

## Downstream (not changed by this seat)

- `corpus/knowledge/probe-delta-alerting.md` sha256 changed. `.ufo/waves/round-21/frozen/before/expected.json` still lists the old hash `562f1b…`. L1 owns the frozen-hash update.
- Line-pinned citations into this file will need +4 re-pins. Examples: `:18`→`:22`, `:77`→`:81`, `:78`→`:82`, `:79`→`:83`, `:80`→`:84`. These appear in `.ufo/round-20/citation-debt.json`, `.ufo/round-20/resume/citation-disposition.json`, `.ufo/round-20/resume/post-review-anchors.json`, `.ufo/round-20/resume/paths-before.json`, `.ufo/round-20/same-surface-baseline.json`, and `corpus/lessons/round-20.md` (the table at about line 348 and lines 367–368). Round-20 files are historical records; L1 decides whether to re-pin or note the shift.
- `free-read-verbs.md` and `ops-automation.md` cite this file by name, not by line. Those citations are unaffected.

## Tools

None installed or updated.

## Files changed

- `corpus/knowledge/probe-delta-alerting.md` (prefix only, +1085 bytes, +4 lines)
- `.ufo/waves/round-21/w1/Knowledge16.md` (this report)
