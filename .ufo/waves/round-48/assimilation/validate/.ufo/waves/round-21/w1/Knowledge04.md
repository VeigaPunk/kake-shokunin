# Knowledge04 — fleet-registry.md provenance trio (round 21, w1)

## Behavior
- Target: `corpus/knowledge/fleet-registry.md`. Its first line was `# Fleet registry & tripwires`; no `source:` / `verified-at:` / `recheck:` trio existed, so the prefix was added.
- Change: prepended exactly 4 lines (3 metadata lines + one blank line), 1002 bytes. Nothing else in the file was edited.
- Body preservation: `tail -n +5` sha256 = `5b79d39d8ac43fa9100b77324615c8a217712f789184e929cafe50347402775e`, identical to the pre-edit file hash taken before the edit. The full file is now 6684 bytes. The heading moved to line 5.
- Target file is the only file changed by this seat. No commits, no other corpus files, no SCORECARD/LOG/QUALITY/SOURCES/README/SKILL edits.

## Metadata content and evidence basis
- `source:` — derived from the entry's own evidence, not an S-id: `~/Projects/webzites/fleet/fleet.config.json` (schema `webzites-fleet-v1`, updatedAt 2026-09-26), `fleet/fleet.dedupe-report.md` (r2 mutation table), `src/probe.mjs` (prober, case-sensitive `html.includes`), and the live probe of 2026-09-28, all as cited in the entry body lines 3–17 and 76–77. Names S019 only as metadata-format authority, not platform evidence.
- `verified-at:` — `2026-09-28`, the original evidence date for `len(sites)` = 21 and the live probe. Labelled `historical-not-live-reverified`; states the source is absent since the 2026-10-12 prune per the body's r18 re-census (2026-10-14). No domain recheck is claimed for 2026-10-19.
- `recheck:` — local-only reading command: `test -f` plus `node -p` over the fleet config, with an `echo` fallback stating that the operator must restore the fleet source or retire the entry. Expected output when present: `webzites-fleet-v1 2026-09-26 21`. No network probe is included.

## Checks performed
- Read the target completely (85 lines), the wave1 spec, `corpus/SOURCES.md`, and sibling trios in `corpus/knowledge/`.
- Verified that `~/Projects/webzites` is absent (`ls` → No such file or directory).
- Measured prefix (`head -n 4 | wc -c` = 1002) and body hash as above.

## Findings and limits
- **Accidental local read:** I ran `node -e 'require(...fleet.config.json)'` once to confirm absence. It failed with `ENOENT` (module not found). This was not the recheck command and read no content. The recheck was not run as a validation step.
- **S019 not registered:** `grep S019` across `corpus/` and the repo finds no registration in `corpus/SOURCES.md`. The entry therefore names S019 as a metadata-contract reference only. L1 must register or confirm S019 in CORPUS.md, otherwise the reference dangles.
- **Entry-local sources have no S-ids:** the webzites fleet sources are not registered in `SOURCES.md`. This is acceptable for the trio but should be noted for L1 coverage work.
- **Field truth (audit only, no body change):** the body's counts (21 rows; 12 live / 3 pruned / 3 broken / 3 queued; updatePath 14/4/2/1) are historical as of 2026-09-28. The source is absent, so they cannot be re-derived this round. Count-field coverage is the L1 job and is not evaluated here.
- No tool was installed or updated. No pacman or network reads.

## Checks for main agent
- `head -n 4 corpus/knowledge/fleet-registry.md | wc -c` → expect 1002.
- `tail -n +5 corpus/knowledge/fleet-registry.md | sha256sum` → expect `5b79d39d…2775e`.
- Confirm S019 is registered in CORPUS.md by L1, and that `recheck:` wording matches the CORPUS.md metadata contract.
