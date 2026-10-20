# PointerRisk — round-21 w1 (read-only)

Scope: round-20 verifier spot-check, the post-review anchor/movement criterion, whether
provenance prefix metadata (round-21 C1) can keep historical lines append-only while moving
anchors, and exact acceptance checks for the inbound movement register. Read-only. The only file
written is this report. No commit, no edit, no sweep or build run by this seat.

Measurement basis: committed bytes only, at `cb807bc` (round-20 base), `02b6dd0`, `9639ec7`
(post-review fixes), `5009eca` (HEAD, = round-21 shared base). The worktree was also observed
because sibling Knowledge seats are editing it now (see F2). Worktree numbers are time-stamped
and will change.

## Verdict

1. **Yes, both at once.** A prefix keeps every base line's content and order and moves every
   line anchor in that file by the same integer N. Measured: the 17 knowledge files in the worktree
   gained a 4-line prefix with 0 deleted lines, and all 395 register rows that target them resolve
   at exactly `newTarget + 4`. Acceptance must therefore check content (no deletions, exact suffix)
   and offset (one integer per file). "No movement" is not achievable with an in-file prefix.
2. **The round-20 integrity proof is correct but mislabelled.** Its declared `targetCommit`
   (`02b6dd0`) is the pre-fix commit: 276 of 589 rows fail there. The same rows pass with 0
   mismatches at `9639ec7` and at HEAD `5009eca`. The register heading and JSON need a labelling
   correction before round 21 relies on them.
3. **The round-20 register is already stale in the worktree.** Its "correct current target"
   values are `9639ec7` coordinates; the round-21 prefix shifts them by +4 for every knowledge
   target. It cannot be reused as is.
4. **Scope gap.** Five more files receive the same +4 prefix (`ops-automation`,
   `keeper-timer-inert`, `origin-repos`, `kimi-subpath-audit`, `vault-properties`). None appears in
   the register. This includes the append-only `LOG.md:232` pointer `keeper-timer-inert.md:65`.
5. **Recommendation:** keep the trio in-file (it satisfies "first 8 lines"), register one integer
   offset per prefixed file, widen the register to all 44 pointer-bearing knowledge/lesson
   basenames, regenerate it after the last historical-file edit, and run checks A1–A9 below.

## Findings (ordered by severity)

**F1 (High) — declared proof commit is the pre-fix commit.**
- `.ufo/round-20/resume/post-review-anchors.json` sets `targetCommit: 02b6dd05…`. Its
  `targetTextMatchBasis` says the comparison is against a "pre-tail text … reconstructed", not
  committed bytes.
- At `02b6dd0`, committed bytes differ from base at 276 of 589 rows: 110 rows have a
  `*[r20 citation-local …]*` note appended inside the same line (e.g. `drift-detection.md:73`,
  `fleet-registry.md:53`); 84 rows have the base text elsewhere in the file; 82 are not found at
  the recorded line. 42 base lines are deleted across all 17 files. The subsequence test (every base
  line present in order) fails in all 17 files at `02b6dd0`.
- At `9639ec7`: 589/589 rows match committed bytes; subsequence holds in all 17 files; deletions
  are 2 lines (EOF-newline re-termination in `freshness-sweep.md` and `round-6-aggregator-audit.md`;
  base last line has no `\n`). `restoration.txt` says "91 current lines" for `drift-detection.md`,
  which matches `9639ec7` (`wc -l` = 91), not `02b6dd0`.
- At HEAD `5009eca`: same results as `9639ec7` (0 mismatches; 17 changed lines in
  `corpus/knowledge|lessons` between `9639ec7` and HEAD, none on a register row).
- Also mislabelled: `corpus/lessons/round-20.md` §"Inbound-pointer correction register" says
  "at commit `02b6dd0`". The lesson's own spot-check line says "after post-review fixes `9639ec7`".
- Consequence: anyone who replays the proof against its declared commit gets 276 failures.

**F2 (High) — the prefix is in the worktree now and the register is stale by +4.**
- Worktree vs HEAD: 17 knowledge files each show `@@ -0,0 +1,4 @@` (trio + blank line) with
  0 deletions: `drift-detection, fire-journal-codes, fleet-registry, free-read-verbs,
  freshness-sweep, ghp-subpath-spotcheck, probe-delta-alerting, publish-channels, publish-queue,
  sitemap-orphan-audit, speedrun-pipeline, keeper-timer-inert, kimi-subpath-audit,
  mirror-pitfalls, ops-automation, origin-repos, vault-properties`. The remaining four knowledge
  entries (`crawl-scope-per-host`, `ghp-served-set`, `ghp-custom-domain`, `ghp-etag-anatomy`)
  already had the trio at HEAD. That is the "4/21" in the goal.
- Register rows vs worktree (recorded `newTarget` line, base text at `oldTarget`):
  194 rows match at the recorded line (lessons and non-prefixed files); 395 rows match at
  `newTarget + 4` (all 11 register knowledge targets, per file: drift 32, fire 16, fleet 44,
  free-read 55, freshness 48, publish-channels 40, publish-queue 82, speedrun 29, ghp-subpath 13,
  probe-delta 18, sitemap 18); 0 rows match neither.
- Worktree lesson changes (round-1…9, 16, 17, 18, 19, 3, 4, 5, 6, 7, 8, 10, 12) are EOF-only
  (hunk start = base line count). They move no anchors. The round-16 hunk is the same
  EOF-newline class as F4.

**F3 (High) — inbound pointers outside the register are shifted by the same prefix.**
Non-evidence pointer lines at HEAD for the five unregistered files:
- `ops-automation.md`: 6 knowledge + 9 lesson lines (+28 `.ufo` snapshot lines).
- `keeper-timer-inert.md`: 7 knowledge + 1 `LOG.md:232` + 1 lesson line (+63 `.ufo` snapshot).
- `origin-repos.md`: 3 lesson lines (+44 `.ufo` snapshot).
- `kimi-subpath-audit.md`: 3 lesson lines.
- `vault-properties.md`: 3 lesson lines.
The round-20 register has 0 rows naming these five files (checked). `mirror-pitfalls.md` has no
inbound pointers. The proof regex covered only 17 basenames; the repo has 44 knowledge/lesson
basenames. Pointers from `.ufo` evidence are frozen snapshots (1,926 lines in the census) and must
be classified, not silently ignored.

**F4 (Medium) — "pure addition" and "subsequence" checks are weaker than the criterion says.**
- Subsequence (every base line present in order) passes for insertions anywhere. It does not bind
  an offset, so it cannot prove a register entry is right. The stronger check for the
  append-only claim is `git diff --numstat <base>` deletions == 0 (see A1).
- Missing final newline: `freshness-sweep.md` (base ends `occurrences.` with no `\n`),
  `round-6-aggregator-audit.md` (ends ```` ``` ```` with no `\n`), `round-16.md` (ends
  `landing.` with no `\n`). Any byte-exact suffix check must normalise this one case and record it.
- The QUALITY criterion "Append-only tails" (`corpus/QUALITY.md:20`) says "every base line survives
  byte-for-byte once the tails are stripped". It does not mention a prefix block. L1 owns that text.

**F5 (Medium) — some live pointers need in-place repoint, not register-only.**
- `corpus/QUALITY.md:15` (`round-7.md:21-25`, `publish-channels.md:9`) and `:20`
  (`round-4-aggregator-audit.md:31`): current-state rubric text, owned by L1. Rewrite in place.
- `scripts/freshness-sweep.mjs:309` comment (`publish-queue.md:219-224`): live code comment; owner
  kake. Rewrite in place.
- Knowledge→knowledge cross-links (e.g. `keeper-timer-inert.md:49,79,97,107,125,140,170`,
  `ghp-served-set.md:15-17`, `ghp-etag-anatomy.md:15,17,47`) sit inside entries that are
  append-only by the round-20 ruling; they belong in the register.

**F6 (Medium) — line-keyed ledgers go stale.**
- `.ufo/round-20/resume/citation-disposition.json` records `currentLine` for 26 annotated locations
  (restoration.txt). Knowledge-file entries are now off by +4. The §paths sweep is relative to the
  citing line, so it still passes; the ledger does not.
- `freshness-pins.json` has no line-number pins (checked: pins are tokens and counts). Sweep line
  numbers are display labels only, so pins are unaffected.

**F7 (Low) — prefix adds `~/` cites on new lines.**
- `drift-detection.md:3` (recheck line) cites `~/Projects/webzites` and
  `~/Projects/plazir-15-site`. The sweep's `ABSENT_RE` (`absent|gone|vanished|emptied|no longer|
  dangling|no such file|never published|missing`) matches on the same line ("If the trees stay
  absent"), so this cite is annotated. The rule to test is: every new cite-bearing line, or a line
  within ±2, contains an `ABSENT_RE` word. Tokens already in the corpus do not change
  `pathsMissSet`; only occurrences rise.

**F8 (Low) — ambiguous base lines in the proof.**
- `freshness-sweep.md:43` is a blank line repeated 26 times in base; 2 register rows point at blank
  or non-unique lines. A text-only replay can mis-map them. Require a 3-line window match.

**F9 (Info) — base-coordinate notes must stay exempt.**
- The r20-correction tails name base coordinates in prose, e.g. `Base corpus/knowledge/publish-channels.md:8`
  (`publish-channels.md:54-57`), `Base corpus/knowledge/sitemap-orphan-audit.md:14…112`
  (`:116-123`), `Base corpus/knowledge/speedrun-pipeline.md:36` (`:66`). These refer to `cb807bc`
  and must not be moved by a prefix. The register must mark them as base-coordinate, exempt.

**F10 (Info) — placement decides movement.** EOF additions move no anchors; prefix additions move
every anchor in the file. The C2 historical gates are EOF-only (F2), so they are anchor-safe.
The C1 provenance trio is a prefix by design, so it is the only anchor-moving change in round 21.

## Can prefix metadata preserve append-only lines yet move anchors?

Yes. The two properties are independent. A prefix of N lines keeps the base suffix intact
(`tail -n +N+1 F` equals base, modulo EOF newline) and shifts every line number in F by N. The
round-20 post-review movements were interior and varied (offsets 0–4 by region). A prefix is a
single integer per file, which is simpler to register and to check.

Options:

| Option | Anchor movement | Meets "first 8 lines" | Notes |
|---|---|---|---|
| A. In-file trio prefix + one integer offset per file | Every anchor in the file, +N | Yes | Recommended. Requires the register to be regenerated after the last edit. |
| B. Sidecar metadata file per entry | None | No (provenance off-file) | Only if user accepts moving provenance off the entry. Decision for user/L1. |
| C. Heading or quote anchors for new pointers | None for new text | Yes | Does not fix already-frozen historical pointers. Use in addition to A. |
| D. Trio at EOF | None | No | Fails the stated goal. Not recommended. |
| Edit line 1 in place to carry the trio | Zero shift | Yes | Violates byte-identical preservation. Rejected. |

## Proposed acceptance checks for the inbound movement register

Run once after the last historical-file edit lands, by the main agent. Not run by this seat.
Notation: `BASE_R21 = 5009eca`; `BASE_R20 = cb807bc`; `F` = a historical file; `N_F` = prefix length
recorded in a per-file ledger (expected 4 for the 17 knowledge files now in the worktree).

- **A1 — pure addition.** `git diff --numstat 5009eca -- <historical files>` deletions column is 0,
  except the EOF-newline class listed in an explicit ledger (currently 3 files, F4). Pass: no
  other deletions.
- **A2 — exact suffix, per prefixed file.** The first hunk is `@@ -0,0 +1,N_F @@`, and
  `diff <(git show 5009eca:F | sed '$a\') <(tail -n +$((N_F+1)) F | sed '$a\')` is empty.
  Pass: all prefixed files. Also: lines 1–3 match `^source: `, `^verified-at: `, `^recheck: `, and
  line 4 is blank (A9).
- **A3 — offset replay (the register check).** For every register row
  `(source, F, L[-L2], L')`: the base line at `git show cb807bc:F_old | sed -n Lp` is byte-equal to
  the final `F | sed -n L'p` (both endpoints for ranges). For blank or non-unique base lines
  (F8), require a 3-line window match. Pass: 0 mismatches.
- **A4 — completeness.** Regenerate the inbound census over the final tree with a pattern built
  from every basename under `corpus/knowledge` and `corpus/lessons` (44 at HEAD), covering `:N`,
  `:N-M`, `:N,M` and `Base <file>:N` forms. Each hit must be exactly one of: register row; base-
  coordinate exempt (F9); frozen `.ufo` snapshot (listed by file, with capture commit); or live
  (must be repointed in place, F5). Pass: the four classes sum to the total hit count. Currently
  failing: `ops-automation`, `keeper-timer-inert` (incl. `LOG.md:232`), `origin-repos`,
  `kimi-subpath-audit`, `vault-properties` are absent from the register.
- **A5 — sweep invariance.** Run `TZ=UTC node scripts/freshness-sweep.mjs --section=paths` (plus
  `--offline` for the full set) on a `git archive 5009eca` extract and on the final tree, using the
  repo-root override the confinement recipe uses (`KAKE_REPO_ROOT`; confirm before use). Pass:
  exit code unchanged; `pathsMissSet` and `newMissing` unchanged (0 new); `uniqueTokens` unchanged
  or each new token listed and annotated; `occurrences` delta equals the count of `~/` or
  `/home/vgpnk` cites on added prefix lines (F7).
- **A6 — ledger re-key.** `.ufo/round-20/resume/citation-disposition.json` `currentLine` values
  point at the final coordinates. Pass: each `sed -n currentLine F` contains the annotation text
  (`r20 citation-local`). Currently 17 knowledge-target entries would fail (F6).
- **A7 — base-coordinate exemption.** Each `Base <file>:N` note resolves in `git show cb807bc:<file>`
  to the quoted text, and no tail line changed (A1 covers the second part). Pass: all.
- **A8 — proof self-consistency.** The anchor JSON's `targetCommit` is the commit whose bytes were
  compared. `targetTextMatchBasis` is replaced by "committed bytes at <commit>". Replay per A3
  against that commit gives 0 mismatches. Correct the register heading in `round-20.md` by an
  appended erratum (the lesson is append-only; do not rewrite the heading in place). Expected:
  `targetCommit` 9639ec7 (or the integrated commit).
- **A9 — provenance trio shape.** For each knowledge entry: lines 1–3 are the trio, line 4 is
  blank, line 5 is the `#` title, and the trio sits inside the first 8 lines. Pass: all 21.
- **A10 — criterion text (L1-owned).** Amend the "Append-only tails" criterion to say: the declared
  prefix block and tails are removed, and the remainder equals base line-for-line with 0 deletions
  except the declared EOF-newline class. Not applied by this seat.

Register composition rule: final coordinate = replay result, not hand arithmetic. For knowledge
targets with only a prefix, final = round-20 coordinate + N_F (+4 now). For interior edits, use the
A3 replay. Regenerate once; do not patch rows by hand.

## Residual risk and verification gaps

- The worktree is in flight (sibling seats). All worktree figures (F2, F6, F7) are at measurement
  time. Re-measure after integration; only committed-byte figures are durable.
- No `freshness-sweep.mjs` run, no tests, no build, and no semantic-pointer analysis. A5 is a
  proposed check, not an observed result.
- Pointers in prose that name a file without line numbers (e.g. "round-7.md §Gate") are not
  covered by the register. They survive a prefix but remain untested.
- `.ufo` evidence snapshots are classified as frozen, not checked against their capture commit.
  That classification is a policy decision for the integrator.
- Option B (sidecar provenance, zero movement) is a decision for the user and L1.

## Evidence locations

- `.ufo/round-20/resume/post-review-anchors.json` (589 rows; `targetCommit`, `targetTextMatchBasis`,
  `protectedMovedPointers` 120 rows / 148 occurrences)
- `.ufo/round-20/resume/post-review-restoration.txt` (claims; "91 current lines")
- `corpus/lessons/round-20.md` §"Inbound-pointer correction register" (line 328) and §"Post-review
  fixes" (line 284); `corpus/lessons/round-20-verifier-spotcheck.md` line 17
- `corpus/QUALITY.md:15,20`; `scripts/freshness-sweep.mjs:309`; `LOG.md:232,237,648,649`
- Commits: `cb807bc` (base), `02b6dd0`, `9639ec7`, `5009eca` (HEAD)
- Stale ledger: `.ufo/round-20/resume/citation-disposition.json` (`currentLine`)

## Tooling

No tools installed or updated. Used `git` (read-only: `show`, `diff --numstat`, `grep`, `ls-tree`)
and the system Node.js (v24.21.0) for read-only analysis; scratch scripts were in `/tmp`, outside
the repo, and were removed.
