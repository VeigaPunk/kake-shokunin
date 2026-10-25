# ExecMisroot

Misroot and scope sweep, read-only. No file outside this report was written; no git/jj mutation; no pacman, no tool installs (none needed). All commands below were run against `/home/vgpnk/Projects/shokunin` (fleet) and `/home/vgpnk/Projects/shokunin/kake-shokunin` (lane).

## FLEET STATUS:

`git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec; re-read with `-uall` to expand the untracked dir) — 17 modified + 2 untracked, nothing else:

- `M .scratch/goal-20261025-hyaku-run7.md`
- `M .ufo/watchdog.log`
- `M .ufo/state/{chousa,kaidoku,kake,kama,kasegi,kengaku,kotoba,kotodama,kumitate,mado,mori,revenger,souji,tabi,tameshi,tsukuroi}.report-baseline` (16 files)
- `?? .ufo/reports/round-42/kama.md`
- `?? .ufo/waves/round-30/wave1/ScribeLesson.md` (the collapsed `?? .ufo/waves/round-30/` entry)

Dirty fleet-root paths whose **name or content** mentions kake or round 56 (nothing under `kake-shokunin/` qualifies):

1. `.ufo/state/kake.report-baseline` — name mentions kake; content is one line `56 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Diff: `54 e3b0…b855` → `56 e3b0…b855`. mtime `2026-10-25 18:56:30 -0300`, i.e. 2 s *before* the watchdog launch line for kake round 56 → harness baseline capture, not a seat write.
2. `.ufo/watchdog.log` — content mentions kake; line 1421 `2026-10-25T18:56:32-03:00 launch kake round=56 pgid=85773 driver=hyaku-inline attempt=1`, plus 62 further added lines (older kake rounds 1–22, 28, 39, 53). mtime `2026-10-25 19:46:38 -0300`.
3. `.scratch/goal-20261025-hyaku-run7.md` — content mentions kake but only round 55 (`kake (55)` line 43; `kake r55 admitted [706]` line 107); **no** round-56 reference. mtime `2026-10-25 19:30:36 -0300`.

Checked and *not* matching (`grep -i 'kake|round[-_ ]?56'`): `.ufo/reports/round-42/kama.md` (mtime 19:54:33), `.ufo/waves/round-30/wave1/ScribeLesson.md` (mtime 15:58:07).

Fleet has **no** `.ufo/waves/round-56/` (`ls` → No such file or directory), so no round-56 wave artifact is misrooted at the fleet root. `find . -maxdepth 3 -name '*kake*' -not -path './kake-shokunin/*'` returns only tracked-and-clean `.ufo/prompts/kake-*.md` (incl. `kake-round-56.md`, tracked at fleet HEAD, 43,930 B) and `.ufo/state/kake.{mission,round,out}` (clean).

## LANE DIFF SCOPE:

`git -C …/kake-shokunin diff --name-status e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6 a450e43e696d032e3ac308383f6b3394e0c92860` → 262 files: 257 `A`, 5 `M`, 0 `D`, 0 `R`.

- Paths **outside** the allowed set (`corpus/`, `scripts/`, `.ufo/waves/round-56/`, `PROVINCE.md`, `SKILL.md`, `LOG.md`, `SCORECARD.md`): **0** (awk filter over the full name-status output returns no row).
- The 5 `M`: `PROVINCE.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`.
- Changed paths outside `.ufo/waves/round-56/` (10): `PROVINCE.md`, `SKILL.md`, `corpus/{QUALITY,README,SOURCES}.md`, `corpus/knowledge/yahoo-japan-{deleted-url-recrawl,link-target-crawl-restriction,nonexistent-url-recrawl}.md`, `corpus/lessons/round-56.md`, `scripts/landed_check.py` — all in-scope.
- 252 changed paths under `.ufo/waves/round-56/`; 164 of them (2,803,744 B) are the nested mirror `.ufo/waves/round-56/assimilation/validate/`, which duplicates `corpus/`, `SCORECARD.md`, `SKILL.md` and carries `.ufo/waves/round-41/{c1_count.py,oracle_crosscheck.py}` at `…/validate/.ufo/waves/round-41/`.
- Lane **worktree** (outside base..tip): 5 untracked paths, all under the allowed prefix — `.ufo/waves/round-56/{w2.ready, w2.ready.dispatched, w2/ExecReopenS367.md, w2/ExecReopenS419.md, w2/ExecReopenS420.md}`; none matched by `git check-ignore -v` (not ignored, merely uncommitted). No modified tracked lane file.
- Lane HEAD has advanced past the revision under attack: `HEAD = 7ad7db51dfcff2eccea9f7f73726f2437b2ed8de` "round-56: W2 spec and dispatch (41 seats)" (2026-10-25 19:52:22 -0300); `a450e43e…` is its ancestor. Range `a450e43..HEAD` adds 5 paths, all inside `.ufo/waves/round-56/` (`make_spec_w2.py`, `w2-dispatch.json`, `w2-spec.json`, `w2-validator.err`, `w2/swarm-registry.json`). `e48354b..HEAD` = 267 files, still **0** outside the allowed set.

## DELETIONS AND SIZE:

- Deletions: **0**. Renames: **0**. Mode/symlink changes: **0** (`git diff --raw` shows only `:100644 100644`).
- Changed files over 1 MiB: **0**. Largest changed: `363,347 B .ufo/waves/round-56/assimilation/validate/SCORECARD.md`; `163,613 B …/validate/corpus/knowledge/accessibility-review-cards.json`; `153,466 B .ufo/waves/round-56/w1-results.json`; `147,221 B corpus/SOURCES.md` (and its identical 147,221 B mirror). Sum over the 262 changed files: 4,342,610 B.
- Untracked lane files are all small (max 5,264 B `w2/swarm-registry.json`); none over 1 MiB.
- Pre-existing >1 MiB blobs in the tree, untouched by this diff (`git ls-tree -r -l a450e43`): `round-41/realrun/sitemaps/postgresql.xml` 4,620,210 B; `round-37/sealed/cases.json` 2,777,011 B; `round-21/anchors-fixed.json` 2,355,487 B; `round-36/realrun/snap-bodies{,-run2}.tar.xz` 1,811,344 / 1,808,836 B; `round-41/realrun/sitemaps/nodejs.xml` 1,652,267 B; `round-39` and `round-40` `sources/xmlschema11-2.html` 1,508,774 B each; `round-42/controls/w1/CtlCache/ctl_accept_table_seed4242.py` 1,283,159 B; each also present under the `round-48/assimilation/validate/` mirror.

## MISROOT FINDINGS:

- **M1 — scope rule holds (attacks the round-56 lane-scope rule).** Zero of the 262 changed paths (and zero of the 267 `base..HEAD` paths) fall outside the allowed prefixes; no lane file was written outside `corpus/`, `scripts/`, `.ufo/waves/round-56/`, `PROVINCE.md`, `SKILL.md`. Evidence: awk filter + `grep -v -E '^(corpus/|scripts/|\.ufo/waves/round-56/|PROVINCE\.md$|SKILL\.md$|LOG\.md$|SCORECARD\.md$)'` → empty.
- **M2 — no round-56 artifact misrooted at the fleet root.** Fleet `.ufo/waves/round-56/` does not exist; the only kake-round-56 dirty fleet state is harness-owned `.ufo/state/kake.report-baseline` (content `56 e3b0…`) plus the `watchdog.log` launch line 1421. Both are fleet-level state written by the runner (baseline mtime 18:56:30, watchdog launch 18:56:32), not by a lane seat.
- **M3 — uncommitted kake baseline (attacks `.ufo/state/kake.report-baseline`).** It is dirty at fleet root carrying the round-56 value while lane commits land separately; if any consumer treats the committed fleet HEAD value as the round-56 baseline it will read `54`, not `56`. Report-only: ownership is the harness, not this lane; no action taken.
- **M4 — 2.8 MB nested mirror inside the wave dir (attacks `.ufo/waves/round-56/assimilation/validate/`).** 164 files duplicating `corpus/` plus copies of `.ufo/waves/round-41/*.py` and `SCORECARD.md`/`SKILL.md`. Permitted by the stated prefix rule, but it inflates the lane diff (164 of 262 paths, 2,803,744 of 4,342,610 B) and will trip any future audit that forbids corpus copies under `.ufo/`.
- **M5 — tip drift vs revision under attack (attacks the "revision under attack" fact).** Lane HEAD is `7ad7db5`, not `a450e43`; the delta is W2 dispatch metadata only, all in-prefix. Any seat that recomputes "changed since base" from HEAD will count 267 paths instead of 262; the claim scripts pinned to `a450e43` remain consistent because that revision is still an ancestor.
- **M6 — stale fleet counter (attacks `.ufo/state/kake.round`; not a dirty path).** Tracked-and-clean file contains `16`, while `.ufo/watchdog.log` records `launch kake round=56`. Outside the required dirty-path list; flagged for L1 awareness only, no edit made.

VERDICT: No misrooted or out-of-scope writes found — 0/262 lane paths outside the allowed prefixes, 0 deletions, 0 changed files over 1 MiB; the only fleet-root kake round-56 dirt is harness-owned state (`kake.report-baseline`, `watchdog.log` line 1421).
