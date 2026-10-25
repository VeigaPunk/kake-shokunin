# Round 51 — verifier spot-check (kake)

author: hyaku closure (non-author integrator, @m_flash)
role: closure role of the protocol lane; did not author this round and did not improve it
lane: kake-shokunin; round 51 (attempt 2)
base (before): `007d66e4e8360a5f88d29a93eeedd8066dad4434`
measured lane tip (after): `842c1b44a590104cff4c06ef84726cac19475d0a` (= `master`, pushed)
report under test: `.ufo/reports/round-51/kake.md` (fleet commit `11f058fb`, author `kake-shokunin <kake@shokunin.local>`)
seat support: eight read-only reviewer/critic seats, all findings re-derived here where a command exists.

## 1. Step-1 conformance

| Item | Result | Evidence |
|---|---|---|
| Report committed by the lane identity | pass | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-51/kake.md` → `kake-shokunin … 11f058fb75f7…`; the later `6b466644` is the closure dispatch only |
| Report is real, not a marker | pass | two claims with before→after, five landed commits, 54 seats, census pair, SHONEN section |
| `SHONEN` heading, one line per box | pass | report `## SHONEN` = 4 items in `SHONEN.md` order (SKILL.md tables, end-to-end task, executable-without-oral-context, no cross-domain bleed); committed `SHONEN.md` is the untouched canonical seed (`[ ]`×4), so the report's `[~]` marks assert nothing into the file |
| Every cited lane commit exists and is an ancestor of the branch | pass | `git cat-file -e` + `git merge-base --is-ancestor <h> master` for `19a99bd8 55915579 9d13768c 907790c7 842c1b44 007d66e4` → all `yes` |
| Lane pushed, no unpushed round work | pass | `scripts/hyaku/jj-lane.sh state …` → `branch=master local=842c1b44 remote=842c1b44 ahead=0 behind=0`; `git ls-remote origin refs/heads/master` → `842c1b44…` |
| No uncommitted round work | pass, with leftovers | `git status --porcelain -uall` → 17 entries, all `round-46/residual/*` and `round-48/assimilation/validate/…`; nothing under `.ufo/waves/round-51/` — routed defect 9 |
| Prompt carries the template contract | pass | a rendered `templates/round-prompt.md` is byte-identical to dispatched prompt lines 1–140 (all of (i)–(v) and the five child-lane items present verbatim); hyaku addendum §6 at line 141 |

## 2. Per-claim re-check at `842c1b44`

Both claims are backed by lane-owned counters. Per PROTOCOL §Gate standard I did **not execute the
lane's counters**; I re-derived every underlying figure myself from committed bytes and
evidence-verified the counter verdicts from their committed outputs. The committed counter runs name
`907790c` and the base, not the tip; `git diff --stat 907790c 842c1b4` touches 13 files, none of
them a counter input (the five `w1/*.md` edits change report text, and L1 only name-lists that
directory), and the two lesson `## Gate` quote lines are outside the `907790c..842c1b4` hunk — so
the verdict carries to the tip, and my measurements below are taken on tip bytes.

### C1 — operability, capability acquisition (`met: ledger_checks_passed == 3 of 3`)

Re-measured (mine, at `842c1b4`):

```
settlement.json: spawn 48 / settled 48 / report:true 48 / exit≠0 []   roles: reviewer 10, critic 10,
  executor 9, scout 6, mutation-tester 5, scribe 4, connector 1, sentinel 1, revenger 1, simplifier 1
`.ufo/waves/round-51/w1/` at tip: 49 files = 48 `.md` + swarm-registry.json; name set == settlement
  name set both ways (only-in-md {} , only-in-settlement {})
sum(seconds) = 23554 ; wave-timing 06:32:17Z→06:47:14Z = 897 s = wallClockSeconds = round-time-accounting.json
LOG.md:2088 — "wall clock **897 s**, aggregate seat seconds **23 554**"
models: 48/48 commandcode/deepseek/deepseek-v4.1-flash; route-probes/commandcode_…json httpStatus 200,
  ok true, bodyExcerpt present; route-probes/xai-oauth_grok-4.7-fast.json httpStatus 403, ok false,
  bodyExcerpt present, route-map.deviations[0] {route, receipt, httpStatus 403, boundToRoles []}
w51-taskcall.json counts {spawn 48, resume 0, total 48}; tasks[] length 48; w51-validator.err 0 bytes
wave-grant.txt: granted lane=kake wave=r51-w1 seats=48 live=66 pending=0 cap=256
```

L1, L2 and L3 all hold on those bytes: seat accounting agrees three ways, the single used route has
an integer-status receipt, the failing receipt carries an excerpt and is bound to no role and is
recorded as a deviation, and the three time figures re-derive from the committed settlement/timing
pair and are named in `LOG.md`. Evidence-verified counter output: `residual/ResidualC1Rerun.md:32`
`C1 ledger 3/3 met=True` exit 0 at `907790c`, base control `0/3` exit 1
(`controls/c1-before-base.txt`, `revision: 007d66e4…`).

### C2 — freshness, sourced learning claim (`met: conditions_passed == 8 of 8`)

Re-measured (mine, at `842c1b4`):

```
git show 007d66e:corpus/SOURCES.md -> 143 rows, sha256 cd9ee4cf…, S262/S263 absent
git show 842c1b4:corpus/SOURCES.md -> 145 rows, sha256 4ea81a5a…
git show 842c1b4:corpus/SOURCES.md | sed '152,153d' | sha256sum -> cd9ee4cf…  (byte-identical to base)
base id order is an ordered subsequence of the tip's: True ; tip-only ids {S262, S263}
S262 line 152, S263 line 153, 11 cells each: docs | A | … | mined | 2026-10-24 | 180d |
  used-by == the one citing entry (canonical-selection.md / crawler-identity.md)
entries: present at tip, absent at base (`git cat-file -e` both revs)
.ufo/waves/round-51/sources/S262.html 174926 B sha256 79222433… ; S263.html 175561 B sha256 6afbdc82…
  == receipts.json sha256 + bytes + URL == the registry row's URL
Gate quotes: "indicating a canonical preference is a hint, not a rule" (10 words) and
  "Googlebot is the generic name for two types of" (9 words) — raw substrings, 1 occurrence each
mirror .ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md at tip: 143 rows, sha256 cd9ee4cf…,
  zero S262/S263 ; add-commit (git log --diff-filter=A) = 19a99bd8, ancestor of tip
mirror blob AT 19a99bd: sha256 4ea81a5a…, 145 rows, carries both ids  (the contaminated original)
pre-append census receipt: argv names --file + the mirror path, no --root; exit 0; W04 only, no E03/E04
```

C1–C7 hold. C8 holds under two of three readings: the counter's (live registry at the mirror's
add-commit — `19a99bd:corpus/SOURCES.md`, 143 rows, no ids) and the tip-mirror reading (143 rows, no
ids). Under the reading "the bytes committed as the mirror at its add-commit" C8 is permanently
false (`4ea81a5a…` is immutable and carries both ids). The counter never reads the mirror bytes at
all — `c51_quote_truth.py` line ~271 does `show(root, mirror_commit, REGISTRY)` — so a still
contaminated mirror would print the same 8/8. **The round discloses exactly this** (report `C2:
MET at the counter's reading, contested under a third reading`; SCORECARD "Known gaps"; the lesson's
`## Mistakes` restates the r52 fix as `show(root, rev, MIRROR)`). Ruling: C2 is **met on its frozen
predicate**, with the mirror-integrity limitation named, disclosed and routed — not a clean met, and
not an over-assertion, because the report refuses the clean word itself. Evidence-verified counter
output: `residual/ResidualC2Rerun.md:24` `C2 quote-truth 8/8 met=True` exit 0 at `907790c`, base
`controls/c2-before-base.txt` `0/8` exit 1.

## 3. Per-axis verdicts

| Axis | Verdict | Evidence at `842c1b4` |
|---|---|---|
| operability | **improved** | new runnable instrument `c51_wave_ledger.py` (297 lines) whose three conditions are true of the committed wave evidence; capability row added; score row 10→10 HOLD (saturated), predicate 0/3→3/3 |
| freshness | **improved** | two new sourced entries on ground the lane did not hold (`canonical-selection.md`, `crawler-identity.md`), re-grounded this round with committed bodies + sha256 receipts; live refetch (mine and the seat's) still carries both quoted sentences; score 10→10 HOLD |
| depth | **improved** | entries carry real thresholds (HTTP/HTTPS, redirects, sitemap, rel=canonical weighing; UA subtype rule); 16 over-assertions remain and are routed, not hidden |
| coverage | **improved** | registry 143→145 (+2 tier A), `PROVINCE.md` § Round-51 block, JS rendering explicitly left to tabi |
| calibration | **improved** | the round's own headline defect (contaminated mirror) and 10 false quote-class labels were found by its seats and disclosed; counters' gaps named in SCORECARD rather than patched after scoring |
| adjacency | **improved** | two staged entries refused with reasons + flip conditions; no cross-domain absorption; PROVINCE boundary statement |

No axis harmed. One caveat, not harm: the lane's live `node scripts/freshness-sweep.mjs` exits 1
(`VERDICT: DRIFT — §armed: PQ-2 GATE-OPENED, sitemap LISTED-LIVE, plazir-gate-anomaly`), and the
control in `w1/CriticHarm.md` shows a base clone exits 1 with byte-identical verdict lines — the
drift is external and pre-existing, not caused by this round. The round's SCORECARD no-harm
sentence cites only the `--selftest` run; routed defect 7.

## 4. Discernment spot-check (`corpus/lessons/round-51.md` § Gate)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S262 canonicalization | admit | live `curl` https://developers.google.com/search/docs/crawling-indexing/canonicalization → HTTP 200, 174926 B; retained `sources/S262.html` sha256 `79222433…` | **agree** | the quoted sentence occurs once in the live page and once in the retained body; the entry states the mechanism the page states, and the row is placed on ground `static-canonical-preflight.md` disclaims |
| S263 Googlebot | admit | live `curl` …/googlebot → HTTP 200, 175561 B; retained `sources/S263.html` sha256 `6afbdc82…` | **agree** | quote raw in both; identity ground (subtypes, user-agent header, robots token) absent from the lane's held robots/crawl-budget entries |
| `engine-crawl-contracts.md` | reject | `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/engine-crawl-contracts.md` (staged package) | **agree** | its Google half cites `…/javascript/javascript-seo-basics`, the URL the lane already mines as S137 (`corpus/SOURCES.md:145`) — a second row is an E04-class duplicate; its Baidu sources are not in the registry (`grep -c ziyuan.baidu corpus/SOURCES.md` → 0) and were not opened this round |
| `crux-eligibility-route.md` | reject | same package, `…/crux-eligibility-route.md`; lane `corpus/knowledge/field-performance-cwv.md` | **agree** | the staged entry's ground is CrUX eligibility; the lane holds it — `field-performance-cwv.md:5` "…and CrUX eligibility", `:71` "### CrUX eligibility (S038)", cites S038/S039 |
| new row S262 (SOURCES.md) | — | row at `842c1b4:corpus/SOURCES.md:152` + retained body | **agree** | 11 cells, `docs \| A \| … \| mined \| 2026-10-24 \| 180d`, `used-by` exactly the citing entry; lesson quote 10 words (≤25) and a raw substring at offset 140620 |
| new row S263 | — | row line 153 + retained body | **agree** | same shape; quote 9 words, raw substring |

Census (frozen command, run by me): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
→ exit 0, 12 × W04 (pre-existing ids, none S262/S263), final line `kake ok`. `census … kake` at round
end: `rows 145`, `tier.A 122 / B 6 / C 17`, `mined 115 / queued 8 / rejected 22` — matches the report.

## 5. Trend verdicts

- **expansion — improved.** Two entries (`git cat-file -e` absent at base, present at tip), two
  tier-A rows (143→145, append-only proven byte-for-byte), one new `PROVINCE.md` block (`:352`).
  Note: the report's "frontier line 23 narrowed" is loose — line 23's bytes are identical at base
  and tip; the narrowing is the appended block's reading of it (routed defect 6).
- **quality — improved.** The round found and corrected 10 false quote-class labels in its own new
  entries and rebuilt a mirror that misrepresented its own state, adding a discriminating `census`
  receipt (`rows 143`) where `validate` alone cannot separate 143 from 145; 16 over-assertions and
  two non-heading anchors remain and are routed, not silently shipped.
- **discernment — improved.** Six residual seats were dispatched after `907790c` and all six reports
  are committed at the tip (`git log -1 --format=%H -- <each>` → `842c1b4`); they attacked the
  ledger with synthetic waves, C8 under three referents, the settlement with 47-of-48 and phantom
  seats, and corrected the round's own prescribed r52 fix as unsatisfiable.

## 6. Routed defects for round 52 (each with a pointer)

1. **The two counters are unregistered instruments.** No SKILL.md gate/probe registry row, no
   self-test mode (argparse surface is only `--root/--revision/--json`), no frozen baseline with
   input digests. PROTOCOL §Gate standard therefore grades them non-conformant as gates: register
   both rows at the registry home with name/kind/entry/verdict-map/self-test/pinned-values/write
   scope/owner, or register them as probes. (`w1/ExecLedgerMutants.md`, `w1/ExecQuoteCounterMutants.md`
   are good falsification evidence but their harnesses lived in `/tmp` and are not replayable.)
2. **C8 must read `show(root, rev, MIRROR)` and pin the mirror's sha256**; today it reads the live
   registry at the mirror's add-commit and never touches mirror bytes. With it: C6 URL equality +
   `httpStatus`/`bytes`/`fetchedAt`, and an entry-level quote-class condition (C5 guards only the
   lesson quote). (`residual/ResidualC2Rerun.md` F1/F3, `w1/ReviewC2Conditions.md`.)
3. **C1 vacuity floor.** `spawn`, the grant and the settlement are not bound to each other and no
   seat report's bytes are read; four seats scored 3/3 on an empty wave, a phantom seat, 48
   zero-byte reports and a used route whose receipt says `httpStatus 500, ok true`.
   (`w1/CriticZeroControl.md`, `residual/ResidualSettlement.md`.)
4. **Junk controls are not replayable.** `controls/c1-junk-wave.txt` and `controls/c2-junk-entries.txt`
   cite revisions the repo does not contain (`git cat-file -t` → could not get object info). Commit
   the junk tree or drop the files in favour of the mutation ladder that does run.
5. **The measured commit is descriptive, not hashed.** SCORECARD says "the lane commit that carries
   this section"; the committed counter outputs name `907790c`, not the cited tip. Run once at the
   cited tip and hash it in the table.
6. **"Frontier line 23 narrowed" overstates the bytes.** `PROVINCE.md` line 23 is byte-identical
   base↔tip (+15/−0 elsewhere); say "a new § Round-51 block narrows the reading of Frontier line 23".
7. **The no-harm sentence hides the live drift result.** SCORECARD cites only
   `freshness-sweep.mjs --selftest` (35/35, exit 0); the live sweep exits 1 with
   `PQ-2 GATE-OPENED, sitemap LISTED-LIVE, plazir-gate-anomaly`, and only `w1/CriticHarm.md` carries
   the base-clone control proving it pre-existing. Put the live verdict and the control in the report.
8. **Staged-id lists match no package revision.** Pin the `shokuknow` package revision (or commit the
   staged entry files) so both rejects resolve at closure time, not just from `LOG.md` prose.
9. **Seventeen untracked files sit in the lane worktree** from rounds 46/48
   (`.ufo/waves/round-46/residual/*`, `.ufo/waves/round-48/assimilation/validate/…`). They are not
   round-51 work, but they keep `status --porcelain` noisy and can ride a later sweep: commit or
   remove them.
10. **Host-wide pacman pause.** `/var/log/pacman.log` records installs at `2026-10-25T00:56:27` and
    `02:14:46 -0300` inside the round span; attempt 2's own window (`03:23:34`–`03:55:31 -0300`) is
    clean and the lane committed no install record, so the lane's "no tool installed" claim stands —
    but the host-wide clause cannot be confirmed from any lane record. Operator-visible only.

## 7. Closure ruling

Both claims verify against the predicates frozen in `.ufo/waves/round-51/contract.json` before any
score, on committed tip bytes; no axis is harmed; the round's own defects are disclosed and routed
rather than patched after scoring. **Admit.** `SHONEN.md` stays all `[ ]` — no box is fully
checkable by this closure alone: box 1 (tables, S-id cites) and box 4 (PROVINCE accuracy) are
mechanically checkable by a non-author, box 2 needs a fresh end-to-end task run, box 3 needs an
agent trial without oral context. Promotion stays operator-owned.
