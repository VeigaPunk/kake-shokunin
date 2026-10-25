# Gate criterion — is each `## Mistakes` fix testable?

Seat: `L1Kake51.CriticGateCriterion-2` (critic, leaf — no subagent dispatch).
Lane: `kake-shokunin`. Lane tip at dispatch and at every command below:
`9d13768c4fdd0e9a2688d2ecf1616b539cf57658`. Base: `007d66e4e8360a5f88d29a93eeedd8066dad4434`.
Question asked: for each row of `## Mistakes` in `corpus/lessons/round-51.md`, **can a command show
the fix able to fail?** I read the two counters, ran them, ran byte-level probes over the retained
bodies, and read the tracked/untracked state of the inherited paths. I did not run any peer's
fixture and I do not adopt any peer's verdict.

Nothing was installed this round (no package, no tool upgrade), so nothing is owed to
`/home/vgpnk/.omp/agent/RULES.md`. Lane write scope respected: this file only.

## Axes

1. **Falsifiability** — a fix is *testable* only if a command exists that (a) passes on the round's
   own bytes and (b) fails on a named, single-property perturbation of those bytes. A recorded
   transcript is not a command.
2. **Freshness** — every ruling below is grounded in bytes I read at the tip, not in the row's own
   prose. Where the row's prose and the bytes disagree, the bytes win and the disagreement is named.
3. **Non-regression on the frozen claims** — a proposed command must not reject ground C1/C2 rely
   on. Each proposal is checked against the 14 quotes the two admitted entries actually carry.

## Measured state

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768c…
C1 ledger 0/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL - settlement receipt absent at the measured revision
  L2 FAIL - route map absent at the measured revision
  L3 FAIL - settlement receipt absent at the measured revision
exit=1

$ python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768c…
C2 quote-truth 8/8 met=True   exit=0
```

`git status --porcelain` shows `settlement.json`, `wave-timing.json`, `round-time-accounting.json`,
`route-map.json`, `w51-taskcall.json`, `route-probes/`, `wave-grant.txt` and the `w1/*.md` reports
still **untracked**. C1's `0/3` is therefore an *absence* failure, not a defect the ledger caught:
no C1 check has ever run against a committed wave. That is the state the wave tips on, and it is
the reason rows 2–4 need a demonstrability argument rather than an observed failure.

## Rulings

| # | Row | Fix as written | Testable today? | Ruling |
|---|---|---|---|---|
| R1 | staged quote mis-transcribed as a source quote | "every admitted entry is re-grounded … C5 requires each Gate quote to be a raw substring of the retained body" | **NO** | instrument absent for the artifact, and the stated class accepts the quote the row calls false |
| R2 | seat-report count stated in prose | `c51_wave_ledger.py` L1 | **only by a /tmp fixture** | code reachable; the committed control is not reproducible |
| R3 | route substitution in prose only | `c51_wave_ledger.py` L2 | **only by a /tmp fixture**, and two holes | duplicate-alias shadowing; deviation read from prose only |
| R4 | no aggregate overrun derivable | `c51_wave_ledger.py` L3 | **only by a /tmp fixture**, and two holes | digit-substring LOG test; open-vocabulary dead-seat reason |
| R5 | inherited artifacts swept | "stay uncommitted and untouched this round" | **as written, false at directory granularity** | 7732 tracked paths under one of the two named paths |

---

### R1 — staged quote mis-transcription — **NOT TESTABLE**

**What the fix claims.** Every quote in the admitted entries is re-grounded, and C5 enforces a raw
substring of the retained body.

**What the bytes show.**

1. C5 is not an instrument over the admitted entries. `gate_quote()` (`c51_quote_truth.py:103`) is
   called once, at `:206`, and reads **only** `.ufo/waves/round-51/w1`-sibling `corpus/lessons/round-51.md`.
   No check parses a quoted span out of `corpus/knowledge/canonical-selection.md` or
   `corpus/knowledge/crawler-identity.md`. The artifact where the mistake happened is unscanned; only
   its Gate line is scanned.
2. The row's own evidence sentence is false at the byte level. The row says the staged
   `canonical-selection.md` quote "Google chooses the most complete and useful page as the canonical
   URL" "is not in the source", and that "Both were confirmed absent from the bodies this round
   fetched". Measured over the committed body:

   ```
   S262 body: occurrence count of that string = 1
   offset: char 145222;  <template class="devsite-content-data-template"> begins at char 144628
   Gate quote "indicating a canonical preference is a hint, not a rule" at char 140534 (before it)
   string in prose-only region (template blocks removed): False
   ```

   The string is Google's own devsite content-data summary sentence, verbatim, inside the retained
   body. The staged quote was **not** invented and **not** absent: it is a quote of the page's
   machine-readable summary rather than of the prose section. That is a region defect, not a
   transcription defect, and the row names the wrong defect class.
3. Therefore the proposed class fails in the direction that matters: "raw substring of the retained
   body" **accepts** the very string the row calls false. Measured:

   ```
   "Google chooses the most complete and useful page as the canonical URL" in raw body  -> True
   same string in tag-stripped FULL body                                                -> True
   same string in tag-stripped PROSE-ONLY body (template removed)                        -> False
   ```

   Only a region-restricted class rejects it. Tag stripping alone does not.
4. The lesson's other half of the same claim is false too. Gate section: "Every quote in the two
   admitted entries is an exact substring of the retained body after whitespace collapse". Measured
   over the 14 block quotes the two entries carry (raw ⊂ collapsed ⊂ tag-stripped):

   ```
   raw                        2   (canonical-selection.md:15, crawler-identity.md:10)
   collapsed-only             3   (:20, :49, crawler-identity.md:26)
   tag-stripped-and-collapsed 9   (:26, :32, :39, :40, :41, :43, crawler-identity.md:15, :17, :21)
   ```

   Nine of fourteen are **not** collapsed-only; they need tag stripping first (the page wraps
   `Device variants`, `Googlebot Smartphone`, the `signals` code span in `<b>`/`<a>`/`<code>`).
   Both quotes the entries explicitly annotate `(collapsed-only quote)` — `canonical-selection.md:41`
   and `:43` — are in fact tag-stripped-only. The annotation is wrong in the exact direction that
   would make a checker reject them.

**Smallest safe correction.** Define three ordered classes in the counter — `raw`,
`collapsed-only`, `tag-stripped-and-collapsed` — over the *prose region* (drop
`<template class="devsite-content-data-template">` blocks), require every quoted span in an admitted
entry to be found in one of them, and require the entry to carry the class it used for every span
that is not `raw`.

**Proposed command** (fails today; see the third bullet for why it is not vacuous):

```
python3 -B .ufo/waves/round-51/c51_entry_quote_class.py --root . --revision <commit>
# must print, for each adopted id: spans_total, spans_by_class, unmarked_nonraw, and met=...
```

It must be demonstrably able to fail, and the round already supplies its two mutants:

- fed the staged S262 string, the prose-only class returns **absent** (raw class returns present) —
  reject; a command whose raw class accepts it is not a test of this row;
- fed the staged S263 string `Googlebot Smartphone: a mobile crawler…`, every class returns absent
  (measured), so it is rejected by all three;
- non-regression, measured now: the strict class `prose-tag-stripped` rejects **0 of 14** admitted
  quotes, so adding it does not walk back C2's existing 8/8.

---

### R2 — seat-report count — **TESTABLE, but not reproducible as committed**

The L1 body (`c51_wave_ledger.py:99-149`) has real arms: `reports_written != len(committed)`,
`reported != committed` with missing/extra name lists, `spawn != payload seats`,
`settled_count + dead_count != len(seats)`. It reads committed bytes through `git ls-tree`/`git show`.
So the *code* can fail. Two problems with showing it:

1. **The committed control cannot be re-run.** `controls/c1-junk-wave.txt` cites revision
   `d969fa2819f1f2050c10637531cba2e12f92a557` with the exact miscount note
   (`reports_written 40 != committed report files 25`). Measured:
   `git cat-file -e d969fa28^{commit}` → **ABSENT**. The same holds for C2's control revision
   `cc57cb80b2060f8c754a896235e323f67a5a91da` → **ABSENT**. Both transcripts are unreproducible
   assertions: the fixture commit is gone, and a transcript cannot be re-run.
2. **The demonstrability lives in `/tmp`.** The mutation seats built fixtures under
   `/tmp/r51-mut-l1`, `/tmp/mutroute-51`, `/tmp/kake51-mutdrop-2`, `/tmp/r51mut`; those are
   ephemeral and none is committed under `.ufo/waves/round-51/controls/` (that directory tracks
   four `.txt` transcripts only). I did not run them and do not adopt their verdicts.

**Smallest safe correction.** Commit the fixture builder, not the verdict: a script that writes a
synthetic wave tree into `/tmp`, `git init`/`commit`s it, asserts `3/3` on the pristine fixture
(so `pass` is reachable and the mutation baselines are scorable), then applies **one** mutation per
run, re-commits, and asserts `exit 1` **and** the named note. Combine with R3/R4 into one harness.

**Proposed command:**

```
python3 -B .ufo/waves/round-51/c51_ledger_selftest.py --root . --revision <commit> --scratch /tmp/r51-gate
# each mutant line: pristine=3/3 exit0 ; mutated exit1 note=<exact substring>
# L1 mutants: reports_written+1 ; one report deleted ; spawn-1 ; settled_count-1
# R3 mutants: duplicate alias ; duplicate alias failing ; failing receipt used by a role
# R4 mutants: wall_clock+1 ; LOG figure removed ; LOG names 1360 while wall is 360
```

An instrument that only fails for *absence* (today's `0/3`) is indistinguishable from a tautology
once the files land; the harness is what separates them.

**Coverage note (not a gate failure).** L1 is satisfied by a wave that writes **zero** reports:
`reports_written: 0` with every seat `report: false` compares equal to `0` committed files. The
contract's L1 wording permits this, so I do not call it a miss — but a reader should not read
`3/3` as "every settled seat reported".

---

### R3 — route substitution in prose only — **TESTABLE, two holes**

L2 (`:152-196`) checks the right things for the happy path. Measured at the tip's own (untracked)
route map: every role's `kimiModel` is the single alias `commandcode/deepseek/deepseek-v4.1-flash`,
and the committed receipt set has that alias with `httpStatus: 200` (int) and `ok: true`; the 403
route `xai-oauth/grok-4.7-fast` carries `ok: false` and a body excerpt and is bound to no role. So
L2 is satisfiable by the real evidence, which is the non-regression property.

Two holes make the fix weaker than its sentence:

1. **Duplicate aliases are silently shadowed.** `receipts.setdefault(alias, receipt)` (`:170`)
   keeps the first `.json` seen in `git ls-tree` order and discards the rest. A second receipt for
   the same alias with `ok: false` is invisible, so "a failing receipt … is not used by a role" can
   be satisfied while a failing receipt exists unrecorded. Fix: count parsed receipts and note
   `duplicate probe receipts for alias X` when the counts disagree.
2. **Deviation is read from prose, not the route map's own field.** `:186-191` builds
   `recorded` from `roles[*]["probe"]` only. The route map carries a top-level `deviations` array
   (`[{route, receipt, httpStatus, boundToRoles, resolution}]`) that L2 never reads. Consequences in
   both directions: a deviation recorded *only* in `deviations` is a false **FAIL**; and a failing
   alias whose string happens to occur in unrelated probe prose (all ten roles share a paragraph
   naming the same aliases) is a false **PASS**. Fix: read `deviations[*]["route"]` first, fall back
   to prose, and match on equality of the alias token, not `in`.

**Proposed command** — the R2 harness mutant list above (`duplicate alias`, `failing receipt used by
a role`, `deviation only in deviations[]`). Each must produce exit 1 with the alias named.

---

### R4 — no aggregate overrun derivable — **TESTABLE, two holes**

L3 (`:219-270`) re-derives aggregate seat seconds, dead-seat seconds and the wall clock from
`settlement` + `wave-timing`, compares them to `round-time-accounting.json`, requires `wave-grant.txt`
and a LOG mention. That is a genuine re-derivation, not a restatement. Holes:

1. `str(wall) not in log_text` (`:249`) is a **digit-substring** test. `wall = 360` is satisfied by
   `1360`, by `2026-10-25T07:32:17`, or by a hash. A LOG that names the *wrong* figure passes
   whenever the digits appear anywhere. Fix: require a labelled co-occurrence, e.g.
   `re.search(r"wall[- ]?clock\b[^\n]{0,60}\b%d\b" % wall, log_text)`.
2. Dead-seat durations are checked only for `reason.startswith("timeout-")` and
   `str.startswith("exit-")` (`:233-240`). A reason of `timeout` (no dash), `killed`, or
   `overrun` skips **every** dead-seat check, so the contract's "every dead seat's duration matches
   its recorded reason" is unenforced for any reason outside the two prefixes. Fix: a closed reason
   vocabulary in the settlement and a note for any reason not in it.

**Proposed command** — R2 harness mutants `LOG names 1360 while wall is 360` (must fail),
`reason: "timeout"` with `seconds != timeout_seconds` (must fail), `round-time-accounting` wall ±1
(must fail).

---

### R5 — inherited artifacts swept — **TESTABLE, but the predicate as written is false**

The row's fix — "they stay uncommitted and untouched this round" — is not a command, and its
"uncommitted" half is false at the granularity the row names. Measured:

```
git ls-files .ufo/waves/round-46/residual                          -> 0
git ls-files .ufo/waves/round-48/assimilation/validate             -> 7732
git log --oneline -1 -- .ufo/waves/round-48/assimilation/validate  -> af7b217 round-48: declare claims, …
git status --porcelain .ufo/waves/round-48/assimilation/validate   -> 9 paths, all "??"
```

So `.ufo/waves/round-48/assimilation/validate/` is a committed tree of 7732 paths; what stays
uncommitted is the **nine loose files** inside it (sizes 2,355,487 · 1,808,836 · 1,811,344 ·
2,777,011 · 1,508,774 · 1,508,774 · 1,652,267 · 4,620,210 · 1,283,159 bytes) plus the eight
`round-46/residual/` reports (`CriticCitationOverreach.md`, `CriticMatrixBlindness.md`,
`MutationSemanticsGap.md`, `ReviewQualityCriterion.md`, `ReviewReceiptIdentity.md`,
`ReviewWitnessOracle.md`, `ScoutSiblingOverlap.md`, `SentinelBounds.md`). `git status --porcelain`
collapses `residual/` to one path, which is why the round-50 note says "10 paths" and not 17.
A directory-level check would report these as *committed* and a directory-level sweep would "fix"
the count by deleting tracked history.

**Smallest safe correction.** Name the ten exact paths and pin their bytes before anything else
touches them (`corpus/lessons/round-51.md` already prints the residual hashes, which I re-measured
and confirm: `f084b660…`, `f4984bbc…`, `9b011fb4…`, `ccc8dde0…`, `5865e8c2…`, `129b5f49…`,
`a775ec29…`, `ec88465c…`).

**Proposed command** (can fail: one `git add`, one deletion, one byte edit breaks it):

```
git status --porcelain -- <the ten exact paths>   # must print exactly ten lines, every one "??"
sha256sum <the ten exact paths>                     # must equal the pinned baseline
```

This is the one row whose fix is already cheaply falsifiable today; it needs the baseline committed
(`.ufo/waves/round-51/w1/inherited-baseline.json`) and the predicate restated as
"these ten paths, not these two directories".

## Adjacent finding — the "pre-append mirror" is post-append, and C8 cannot see it

Found while measuring R1's provenance chain. It is a claim-level defect, not a mistakes-row defect,
and it is byte-measured at the tip.

**The artifact.** `.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` was added by
`19a99bd` ("commit the pre-append mirror"). At that same commit:

```
git show 19a99bd:corpus/SOURCES.md                                    ->  0 rows for S262/S263
git show 19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md -> 2 rows (S262, S263)
diff <lane at 19a99bd> <mirror at 19a99bd>                            -> exactly the two adopted rows, added
```

The mirror registry is the lane registry **plus** the two rows that C2 says were appended later, in
`5591557`. So the file named "pre-append" contains the append. The rows' own cell reads
`used-by corpus/knowledge/canonical-selection.md` and `opened 2026-10-24`: they are this round's rows.

**Why the counter does not catch it.** C8 reads `REGISTRY`, not `MIRROR`
(`c51_quote_truth.py`, C8 block: `show(root, mirror_commit, REGISTRY)`, variable named
`mirror_registry`). Measured replication of C8 against both paths at the tip:

```
C8 as coded  (lane  corpus/SOURCES.md at 19a99bd) -> S262 False, S263 False  -> pass
C8 as worded (mirror file at 19a99bd)             -> S262 True,  S263 True   -> would FAIL
```

The contract's C8 sentence is "the mirror's **registry** carries none of the adopted ids". Under that
wording, C8 is **false** at `9d13768c…`, and C2's reported `8/8` is really `7/8`. The counter's C7
passes for the same reason at one remove: the census receipt
(`--file …/pre-append/corpus/SOURCES.md`, exit 0, `file ok`) validated the rows-present bytes, so the
"pre-append" validation is of post-append content.

I state the reading explicitly because a charitable one exists and I will not hide it: if "the
mirror's registry" means "the registry as it stood in the lane at the mirror commit" — the commit is
the mirror, not the file — then C8 is sound as coded and C2 keeps `8/8`. That reading is not
available to the artifact's own name, though: a directory called `pre-append` whose
`corpus/SOURCES.md` already carries the append, plus a census receipt that validates it as
pre-append, is false provenance either way. The defect is that the counter leaves the two readings
indistinguishable; the correction below forces the literal one.

**Smallest safe correction.** In C8 read the mirror path itself
(`show(root, mirror_commit, MIRROR)`), and add one line: the mirror path must have exactly one
commit in `git log --format=%H <rev> -- <MIRROR>` (the add commit), so no later commit can rewrite a
file that is presented as frozen evidence.

**Live drift, measured during this seat's run (not mine).** The worktree copy of that same mirror
changed at `2026-10-25 03:36:34 -0300`: the two rows were removed and `census-exit.txt` went
`0` -> `exit=0`. Committed state at the tip: 2 rows; worktree: 0 rows. If that drift is committed,
the census receipt no longer describes the file it names; if it is discarded, the committed mirror
stays post-append. Either resolution must be recorded, and the correction above makes the counter
say which one happened.

## Cross-cutting finding

Rows 2–4's fixes are instruments, and every attempt to show them failing is either a transcript whose
fixture revision is absent from the repo (`d969fa28`, `cc57cb80`) or a `/tmp` tree that dies with the
session. A gate criterion that cannot be re-run is a claim, not a criterion. The single correction
that closes all three is the committed mutant harness in R2 — pristine-pass asserted first, one
property mutated per run, exit code **and** note text asserted.

## Non-regression check

- C2 at `9d13768c…`: `8/8 met=True`, exit 0 (re-measured here, not quoted from another seat).
- The strict quote class proposed in R1 rejects 0 of the 14 quotes the admitted entries carry, so it
  cannot walk C2 back.
- The strict route reading proposed in R3 accepts the tip's own route map and both probe receipts.
- C1 remains `0/3` at the tip for absence; nothing in this report moves it, and it must not be scored
  as `3/3` until the wave evidence is committed and the harness has been run at that commit.

## Files I could not read

None. Peer fixture trees under `/tmp` were deliberately not read as evidence.
