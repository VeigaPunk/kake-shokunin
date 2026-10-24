# Knowledge13 — mirror-pitfalls provenance trio (round 21, C1 scope)

## Scope

- Target: `corpus/knowledge/mirror-pitfalls.md` only.
- Entry state on open: no provenance trio; line 1 was the H1 `# Mirror pitfalls — observed, not hypothetical`. Trio was therefore prepended, not audited-in-place.
- No other file was edited. No rechecks were run. No credential/auth files were read. No commands, builds, or tests were run.

## Exact file change

- Pre-edit size: 2761 bytes (`stat`), 50 body lines plus the leading `Sources:` paragraph (file now 54 lines).
- Prepended prefix: **1021 bytes**, four lines (`source:`, `verified-at:`, `recheck:`, blank).
- Post-edit size: 3782 bytes. `3782 − 1021 = 2761`, which equals the pre-edit size, so no pre-existing byte changed length. The H1 now sits at line 5. Every old line is intact per the edit tool's before/after echo (old line 1 → new line 5, old line 2–50 unchanged).
- Prefix was built in two passes: first draft 907 bytes; a second edit to line 3 widened the recheck to add `~/Projects/ufofsdbeta-kimi-review/` (the body's own absence claim, line 30 of the old file, was not covered by the first recheck). Final prefix 1021 bytes.

## Field content and evidence basis

- `source:` — S019 is cited only as the metadata contract (registration still pending; S019 is absent from `corpus/SOURCES.md`, which registers S001–S018 only). Entry-specific evidence is the entry's own header: `fleet/kimi-surface-ops.md` failure-mode tables (r1–r4), `fleet.dedupe-report.md`, `ufofsdbeta/.ufo/` wave evidence (citation-only). Paths are written under `~/Projects/webzites/fleet/` because `corpus/knowledge/publish-channels.md:50` and `publish-queue.md:3` and `LOG.md` round 1 place them there.
- `verified-at:` — original evidence date from `LOG.md` round 1 and round 4 entries (both 2026-09-28) and the dated absence event `2026-09-28T23:51:31Z` (r15 sweep, recorded in the entry body). Marked `historical-not-live-reverified`. No "today" domain recheck is claimed.
- `recheck:` — three `test -e` presence checks (kimi-surface-ops, ufofsdbeta, ufofsdbeta-kimi-review; no content reads, no credential paths), with operator restore-or-retire requirement. Notes the r18 re-census (2026-10-14) recording webzites absent after the 2026-10-12 prune. Not executed.

## Audit findings (not fixed here; for L1 / owners)

1. **S019 unregistered.** The trio references S019 as metadata authority, but `corpus/SOURCES.md` has no S019 row this round. L1 must register it (CORPUS.md, per the round-21 spec) or the reference dangles.
2. **Browser/CDP bullets have no named source.** The entry's "Browser/CDP lane" section (lease, `t<N>` renumbering, composer selectors, `SingletonLock`, metered fires) is not covered by the header's "Sources:" paragraph. The only corroboration I found is `SKILL.md` §traps lines ~296–302 (and `lessons/round-8-aggregator-box3-coldrun.md`), which the entry itself does not cite. I did not add those as sources because the entry's own evidence does not name them; the trio states this gap explicitly. Owner decision needed: either cite SKILL.md (L1 owns SKILL) or treat the section as unsourced debt.
3. **Round-level dates are coarse.** `verified-at` uses 2026-09-28 for rounds 1–4 because LOG.md gives one date per round, not per failure-mode table row. Acceptable; not inflated.
4. **`ufofsdbeta/.ufo/` wave evidence is undated** in the entry. It is marked citation-only in the header and was not given a date.
5. **Name-trap and dead-slot claims** (`plazir27runson` vs `plazir27runs-on`, `ufo-fsd.kimi.page` etc.) are not individually re-verified; their evidence is the same undated `kimi-surface-ops.md` table set now absent from FS. Under the trio these are historical claims only.

## Tooling

- No tools installed or updated. (Used only `read`, `glob`, `grep`, `edit`, `write`, and `bash` `stat`/`head`/`wc`/`mkdir`.)
- `mkdir -p` created `.ufo/waves/round-21/w1/` only if missing; the directory already existed with other reports.

## Out of scope / not done

- Field-coverage counts across the corpus (L1 job).
- Any change to `SCORECARD`, `LOG`, `QUALITY`, `SOURCES`, `README`, `SKILL`.
- Any domain re-read of `~/Projects/webzites` or `~/Projects/ufofsdbeta*` (absent per the cited history; not re-probed).
