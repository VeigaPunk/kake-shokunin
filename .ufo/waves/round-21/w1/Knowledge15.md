# Knowledge15 — origin-repos.md provenance trio

Seat: scribe (leaf). Target: `corpus/knowledge/origin-repos.md` only. No commits, no rechecks run, no credential/auth files read, no tools installed.

## Field audit (pre-edit)

- Entry opened without the provenance trio (`source:` / `verified-at:` / `recheck:`). Line 1 was `# Origin repos — the 50-clone canonical-source map`; line 3 is a prose `Source:` line that is not the trio and was preserved byte-identically.
- Read the whole entry (69 lines) before editing: clone map, byte-verified writers, name traps, five sourceless artifacts, fleet.config drift. Existing r18 re-census absence annotations and [INFERENCE] flags were left untouched.

## Change

Pure prefix addition at file start (`PUT <1:`), body unchanged. Post-edit the old line 1 is line 5 and the old line 69 is line 73.

Prefix = 4 lines, **745 bytes** (measured with `wc -c` over the exact text, including the trailing newline of each line; the three metadata lines plus one blank line).

1. `source:` — derived from the entry's own evidence: `~/Projects/webzites/reports/keepers/repos-r1.md … repos-r8.md` (wz-repos lane, run `gqab44994c06d7e7a4`), noting the sources are absent since the 2026-10-12 prune. Names S019 as metadata-format authority only (`format authority only; entry evidence is the wz-repos reports`).
2. `verified-at:` — original evidence date/revision: terminal round 2026-09-21, round r8, run `gqab44994c06d7e7a4`. Marked `historical-not-live-reverified; no live domain recheck performed`. Not stamped with today's date.
3. `recheck:` — local-only reading command: `test -e ~/Projects/webzites/reports/keepers/repos-r1.md && test -d ~/Projects/webzites/repos && echo present || echo absent`, with operator requirement to restore the sources from the prune/migration archive or retire the entry as historical.
4. Blank line.

## Evidence basis

- Source paths and absence: the entry's own r18 re-census annotations (2026-10-14) at lines 3, 5, 7, 15, 66 of the original file record `~/Projects/webzites/reports/keepers/repos-r1.md`, `~/Projects/webzites/repos`, and `~/Projects/ds4cc-marketplace` as absent after the 2026-10-12 prune. The recheck command targets exactly those paths.
- Run id and round: original line 4 `(wz-repos lane, terminal round 2026-09-21, run gqab44994c06d7e7a4)`; original line 9 `50/50 clones re-fetched HEAD == @{u} at r8`.
- Reference model: sibling `corpus/knowledge/*.md` entries use `source:` / `verified-at:` / `recheck:` with the same em-dash separators; `crawl-scope-per-host.md`, `ghp-custom-domain.md`, `ghp-etag-anatomy.md`, `ghp-served-set.md` checked for format only.

## Limitations and findings

- **S019 is not registered in this checkout.** `corpus/SOURCES.md` registers S001–S018 only; `grep S019` under `corpus/` returns no match. The reference is to the contract as named by the wave spec. L1 is registering the canonical CORPUS.md this round; if S019 lands with a different scope, the prefix's contract reference should be re-checked against it.
- **Sources vanished.** The entry's primary evidence (repos-r1…r8, clone tree) is absent. The prefix does not revive it; it records the absence and assigns restore-or-retire to the operator. The body's `[INFERENCE]` and r18 absence flags remain authoritative for present-state claims.
- Body live-status claims (`live 200` for veigapunk.github.io subpaths, `sha` receipts) are historical r5–r8 evidence and were not reverified; `verified-at` says so.
- Count field coverage across the corpus is L1's job; not audited here.
- Recheck command was written, not run.

## Touched surfaces

- `corpus/knowledge/origin-repos.md` — prefix only (745 bytes added at offset 0; no existing byte altered).
- `.ufo/waves/round-21/w1/Knowledge15.md` — this report.

## Out of scope / not touched

SCORECARD, LOG, QUALITY, SOURCES, README, SKILL (L1). No other knowledge entries. No installs or upgrades (none were needed).

## Checks for main agent

- Confirm `head -c 745` of the file matches the three metadata lines plus blank line, and that line 5 is `# Origin repos — the 50-clone canonical-source map`.
- After L1 registers S019 in CORPUS.md, confirm the `metadata contract S019` reference resolves.
