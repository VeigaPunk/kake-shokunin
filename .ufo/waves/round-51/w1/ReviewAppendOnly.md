# ReviewAppendOnly — does the round keep its own append-only discipline over committed bytes?

Seat: `L1Kake51.ReviewAppendOnly-2` (leaf, no dispatch). Assigned question only: compare
`corpus/SOURCES.md`, `SCORECARD.md` and `LOG.md` between
`007d66e4e8360a5f88d29a93eeedd8066dad4434` and `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`, and report
per file the count of **removed or rewritten lines that are not part of a new section**. Judged axis:
freshness. Read-only; the only file this seat wrote is this report.

## Answer to the assigned question

| file | removed lines | rewritten lines | removed/rewritten lines not part of a new section |
|---|---|---|---|
| `corpus/SOURCES.md` | **0** | **0** | **0** |
| `SCORECARD.md` | **0** | **0** | **0** |
| `LOG.md` | **0** | **0** | **0** |

**No historical line was removed or rewritten in any of the three files.** The defect-naming clause of the
assignment is therefore vacuously satisfied: there is no rewritten historical line to name. The append-only
discipline holds at the line level, and it holds by three different kinds of proof — byte identity
(`SCORECARD.md`), byte-prefix (`LOG.md`), and delete-then-compare reconstruction (`corpus/SOURCES.md`) — not
by a single `--numstat` 0 that could be an artifact of diff alignment.

One caveat, stated up front and kept strictly separate from the verdict: the lane **worktree** was being
edited concurrently while I read it, and in that uncommitted state two of these three files diverged from the
commits I compared. That correction has since landed as `907790c` ("round-51: land the wave evidence, the
ledger verdict and the mirror repair"), and I re-ran the same three proofs against it: the answer is
**0/0/0 at both tips** — `git diff --numstat 007d66e 907790c` is `2 0` for `corpus/SOURCES.md`, `61 0` for
`SCORECARD.md` and `59 0` for `LOG.md`, with both large files still exact byte-prefix appends (+5471 B and
+5230 B) and `sed '152,153d'` on the new tip still reproducing base byte-for-byte. Details in *In-flight
worktree correction* below.

## Revisions under comparison

| object | blob | sha256 | bytes |
|---|---|---|---|
| `007d66e…:corpus/SOURCES.md` (base) | `cd448eaf06bbccefbd2e672be03355c79dd6d851` | `cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117` | 133 780 |
| `9d13768…:corpus/SOURCES.md` (tip) | `9e2a22175ef95a23252b349d8743cf0e5b5480fc` | `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3` | 135 068 |
| `007d66e…:SCORECARD.md` (base) | `a8c7c16d1484ef01eac9dd1ab293e3d9967a0e81` | `87db00410ff1bf782c5d90ff26bb0feed169635a22f80c9e6c25281daadadffd` | 347 513 |
| `9d13768…:SCORECARD.md` (tip) | `a8c7c16d1484ef01eac9dd1ab293e3d9967a0e81` | `87db00410ff1bf782c5d90ff26bb0feed169635a22f80c9e6c25281daadadffd` | 347 513 |
| `007d66e…:LOG.md` (base) | `b9f49ca567455863f3fa28a24a13afdf9d77dbdd` | `f41fa6ef175cfab84fb8f1657af7b3d79af92cd67529144fd69f4f0a03577013` | 167 063 |
| `9d13768…:LOG.md` (tip) | `39ea8eb422009d38594db1c77874398aa8416e1d` | `cc9d6244b8a92dddcfb100e4113719a1d2ede259adff434f95092e9f7a179d03` | 170 601 |

The base is the declared do-nothing revision; the tip is the lane tip frozen at wave dispatch. The three
commits in the range are `19a99bd` (parent `007d66e`) → `5591557` (parent `19a99bd`) → `9d13768` (parent
`5591557`), so the range is a plain 3-commit chain with no merge and no rewrite.

`git diff --numstat 007d66e 9d13768 -- corpus/SOURCES.md SCORECARD.md LOG.md`:

```
40	0	LOG.md
2	0	corpus/SOURCES.md
```

`SCORECARD.md` is absent from that output because it never appears in the diff at all. I did not stop at
`--numstat`: a 0-deletion count is also what a rename or a move produces, so each file was closed by a
second, independent method below.

## Per-file evidence

### `corpus/SOURCES.md` — pure insertion at the end of the row region

Four checks, all agreeing:

1. **`--numstat`**: `2  0  corpus/SOURCES.md` — 2 insertions, 0 deletions.
2. **Line multiset (comm on sorted files)**: lines in base but absent from tip = **0**; lines in tip but
   absent from base = **2**. A rewritten line survives a naive `diff` as delete+insert but cannot survive
   this check while also being reported as 0 removals; both agree there is nothing removed.
3. **Byte reconstruction.** `sed '152,153d'` applied to the tip reproduces the base **byte-for-byte**
   (`cmp` clean, 133 780 bytes both sides). So the 2 new lines are the entire delta and every other byte of
   the file — all 256 base lines — is untouched. This is the strongest available statement of append-only
   for this file.
4. **Structure.** Base rows are lines 9–151 (143 rows, first row line 9, last row line 151). Tip rows are
   lines 9–153 (145 rows) with **zero non-row lines inside 9–153**, i.e. the row region stays contiguous.
   The two new rows occupy tip lines 152 and 153 — immediately after the last pre-existing row `S286` and
   before the blank line at 154 and the `## Paths` heading at 155. The insertion is a tail append to the
   row region, not an edit to the notes block and not a mid-table splice:

```
tip 150  | S274 | Google for Developers — Reduce the Google crawl rate …
tip 151  | S286 | Google for Developers — Troubleshoot Google Search c…
tip 152  | S262 | Google Search Central — What is URL canonicalization
tip 153  | S263 | Google Search Central — Googlebot — https://develo
tip 154  (blank)
tip 155  ## Paths
```

5. **No id collisions.** `S262` and `S263` each occur exactly once at tip; the whole-table duplicate sweep
   (`grep -oE '^\| S[0-9]+ ' | sort | uniq -d`) returns nothing. Each new row is 11 cells with
   `status=mined`, `opened=2026-10-24`, `recheck=180d`, and `used-by` naming exactly one path —
   `corpus/knowledge/canonical-selection.md` for S262 and `corpus/knowledge/crawler-identity.md` for S263.

Both files end in `0a` at base and tip, so the insertion introduces no missing-final-newline churn.

### `SCORECARD.md` — byte-identical, not merely "unchanged"

- Base and tip resolve to the **same blob** `a8c7c16d1484ef01eac9dd1ab293e3d9967a0e81` and the same sha256
  `87db0041…dadffd`, 347 513 bytes, 4146 lines both sides. Same object id means the tree entry cannot have
  been touched at all between the two revisions.
- `git log 007d66e..9d13768 -- SCORECARD.md` returns **no commit**. None of the three round-51 commits
  touched this file, so there is no intermediate rewrite that was later reverted — the endpoint equality is
  not hiding a transient edit.
- Line multiset: 0 lines in base absent from tip, 0 lines in tip absent from base.

This is the strongest possible form of the property: not "append-only", but "untouched".

### `LOG.md` — exact byte-prefix append of 4 new round-51 bullets

- **Prefix proof.** `cmp` between the base file and the first 167 063 bytes of the tip file is clean —
  the base is an **exact byte prefix** of the tip. 2043 → 2083 lines; 40 lines appended at the tail only;
  `--numstat` 40/0; line multiset removed = 0, added = 40.
- The 40 appended lines form **exactly 4 new `- **Round 51 — …**` bullets** (counted
  `grep -cE '^- \*\*Round 51'` over lines 2044–2083 = 4), and `grep -vE '^- \*\*Round 51' | grep -vE '^  '`
  over that block returns **zero** lines — every appended line is either a bullet head or a 2-space
  continuation of one. Nothing was threaded into an earlier round's entry.
- The last line of the file (`… re-run with the corrected`) is part of the fourth bullet, so the append is
  contiguous to EOF with no trailing scratch.

The fourth bullet is the one that matters most for discipline: the C2 counter bug was fixed by **appending
an entry that states the defect** ("The C2 counter read the source receipts at the top level of
`receipts.json` while the committed receipt file carries them under its `sources` key") rather than by
editing the earlier claim about that counter. Commit `9d13768` confirms it: `git diff --name-status 9d13768^
9d13768` = `M .ufo/waves/round-51/c51_quote_truth.py` and `M LOG.md`, 7 insertions 0 deletions in `LOG.md`.
A prior claim was corrected forward, not rewritten in place.

## Attack findings on the append-only evidence chain

The three files are clean. The *evidence that the append happened in the claimed order* is weaker than the
append itself, and that is where the reportable defects are.

### F1 — the "pre-append mirror" already contains the two rows; the order proof rests on live blobs, not on the mirror (LOW — **confirmed and under repair**; see the next section)

The mirror at `.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` (committed at `19a99bd`) is
blob `9e2a22175ef95a23252b349d8743cf0e5b5480fc` — **byte-identical to the post-append live registry at the
tip**, 258 lines / 145 rows, and it contains both `| S262 |` and `| S263 |`.

This is a real hazard for a freshness reader but it is **not a false claim**, because the LOG discloses it
in the same sentence: "The mirror is the lane's `corpus/` **plus the two new rows** and the two admitted
knowledge files". The lane's own round-50 precedent uses the identical design, and says so explicitly in
`.ufo/waves/round-50/assimilation/order-proof.json`:

> `"note": "The mirror carrying the S286 row and the --file census receipts are committed at pre_rev; the
> live registry carries no S286 row at that revision."`

I verified round 50 behaves the same way: its mirror carries `S286` once, and the live registry at its
`pre_rev` `33eec7f` carries `S286` zero times. So the mirror is a *staged-content* artifact by convention,
not a snapshot of the registry.

**The ordering claim itself survives**, and it survives on live bytes alone, which are the right evidence:

| revision | live `corpus/SOURCES.md` blob | live rows | carries S262/S263 |
|---|---|---|---|
| `19a99bd` (mirror commit) | `cd448eaf…` | 143 | **no** |
| `5591557` (append commit) | `9e2a2217…` | 145 | **yes** |

Since `19a99bd` is the parent of `5591557`, the registry append provably landed strictly after the mirror
commit. Residual risk is terminological: a reader who reads the directory name `pre-append/` as "the registry
before appending" will find 145 rows there and conclude the append is unproven. The path name does not
describe its content.

I derived the above from the committed blobs before reading any correction record. The round has since
independently reached the same conclusion and is repairing it; the round's own correction text states the
defect in the same terms I measured ("Its blob was byte-identical to the post-append registry: 258 lines,
145 data rows, already carrying S262 and S263 … a copy taken after the append").

### F2 — round 51 has no machine-readable order proof, while round 50 did (LOW)

`git ls-tree -r --name-only 9d13768 -- .ufo/waves/round-51/ | grep -c order-proof` = **0**. Round 50
committed both `.ufo/waves/round-50/assimilation/order-proof.json` (schema `kake-r50-order-proof-v1`, with
`pre_rev`, `adopted_ids`, `mirror`, `census_argv/stdout/exit`, and the note quoted in F1) and
`.ufo/waves/round-50/wave-cite-proof.json`. Round 51's ordering evidence exists only as prose in the second
`LOG.md` bullet.

This is a regression against the immediately preceding round's own standard, and it is the reason F1 has to
be resolved by hand-scanning LOG prose rather than by reading a predicate. It does not break either frozen
claim — C1 and C2 are the contract predicates and neither asserts append ordering — so it stays LOW.

### F3 — the LOG's enumeration of the mirror's contents is incomplete by one file (LOW)

The second bullet says the mirror is "the lane's `corpus/` plus the two new rows and the two admitted
knowledge files". The actual mirror corpus delta against base is **four** files, all additions:

```
 SOURCES.md                       |   2 +
 knowledge/canonical-selection.md |  77 ++++++++++++++++++++++++++
 knowledge/crawler-identity.md    |  54 +++++++++++++++++++++
 lessons/round-51.md              | 116 +++++++++++++++++++++++++++++++++++++++
 4 files changed, 249 insertions(+)
```

`corpus/lessons/round-51.md` (+116 lines) is present in the mirror and is not named in the enumeration. The
omission is in the direction of understating, and it does not weaken any claim, but the sentence is not an
exact description of the committed bytes. Note the useful part of the same check: the mirror delta is
**249 insertions and 0 deletions**, so even the staged artifact is additive-only.

### F4 — `LOG.md` itself is never mirrored (INFO)

`pre-append/` contains `SCORECARD.md`, `corpus/`, `scripts/` and `.ufo/`, but no `LOG.md`. So the round's own
log append has no pre-append snapshot, and its ordering rests solely on the byte-prefix property proven
above. That property is sufficient here (it is a harder guarantee than a snapshot comparison), so this is
recorded rather than raised.

### F5 — the census receipt validates the 145-row mirror, not the 143-row registry (INFO)

`pre-append/census-argv.txt` is
`sources-census.sh validate --file …/pre-append/corpus/SOURCES.md`; exit `0`; stderr is 0 bytes; stdout is
13 lines = 12 `W04` duplicate-url warnings + 1 `ok` line. The census stdout prints **no row count**, so the
LOG's "143 rows" figure is evidenced by the git blob (which I confirmed: 143 at base and at `19a99bd`), not
by this receipt. Two consequences worth stating:

- The receipt is a check on post-append content, so it cannot serve as a pre-append registry check. The LOG
  sentence "The census ran on the mirror" is accurate; the path prefix `pre-append/` invites the wrong
  reading (same root cause as F1).
- **Positive result:** none of the 12 `W04` ids is `S262` or `S263` (they are S033, S088, S092, S098, S099,
  S102, S110, S111, S115, S116, S117, S127). The two assimilated rows introduce no new duplicate-url
  warning, and the census exits 0 with the rows present.

## LOG claims about these three files, tested against bytes

| claim in the appended LOG block | verdict | evidence |
|---|---|---|
| "the live registry at this commit still holds 143 rows and carries neither S262 nor S263" | **TRUE** | `19a99bd:corpus/SOURCES.md` = `cd448eaf`, 143 rows, 0 matches for either id |
| "Rows S262 and S263 are appended to `corpus/SOURCES.md` (143 rows to 145 rows)" | **TRUE** | base/`19a99bd` live 143 → tip 145 |
| "no existing row's cell changed" | **TRUE** | `sed '152,153d'` tip == base byte-for-byte |
| "after the pre-append mirror committed at `19a99bd8c30d…`" | **TRUE** | `19a99bd` is `5591557`'s parent; live registry lacks both rows at `19a99bd` |
| "`opened` 2026-10-24, `recheck` `180d`, `status` `mined`" | **TRUE** | both rows, cells 9/10/11 |
| "`used-by` exactly the one admitted entry that cites each row" | **TRUE** | S262 → `corpus/knowledge/canonical-selection.md`; S263 → `corpus/knowledge/crawler-identity.md` |
| mirror "is the lane's `corpus/` plus the two new rows and the two admitted knowledge files" | **INCOMPLETE** | F3: also adds `corpus/lessons/round-51.md` (+116) |
| "only the receipt lookup was corrected" (4th bullet) | **TRUE for these files** | `9d13768` touches `c51_quote_truth.py` + 7 appended `LOG.md` lines, 0 deletions |

## In-flight worktree correction (observed 2026-10-25 03:34–03:43; **landed** as `907790c`)

Everything above is *committed* bytes, which is what the assignment asks for. This section is separate: the
lane worktree was being edited concurrently while I read it (mtimes 03:34–03:36 fall inside my read window),
and the changes bear directly on append-only discipline for two of my three assigned files. **I created none
of these changes**; I observed them read-only. The worktree moved twice while I watched, so what follows is a
timestamped trajectory, not a single snapshot — I say which state each claim belongs to.

Modified tracked files at first observation (`git status --porcelain`, 03:36):

| path | delta |
|---|---|
| `PROVINCE.md` | +15, **0 deletions** |
| `SCORECARD.md` | +33, **0 deletions** |
| `.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` | **2 deletions** |
| `.ufo/waves/round-51/assimilation/pre-append/census-exit.txt` | 1 line replaced (later reverted) |
| `corpus/knowledge/canonical-selection.md` | +21 / **−1** (appeared after 03:41) |
| `corpus/knowledge/crawler-identity.md` | +23 / **−2** (appeared after 03:41) |
| `LOG.md` | **unchanged** at every observation |

Every row above landed in `907790c`, but the deltas are the **observation-time** worktree-vs-`9d13768`
values, not the final ones — the worktree kept growing after I read it, so the landing is larger:
`SCORECARD.md` finished at **+61** lines (not +33) and `LOG.md` at **+19** (not 0). The committed
base→tip numbers are in *Answer to the assigned question*. The landing commit reports **14 301 insertions,
5 deletions** across 88 files; the 5 deletions are exactly the 3 entry-label lines and the 2 mirror lines
named in this section, and the live `corpus/SOURCES.md` is untouched by it
(`git diff --numstat 9d13768 907790c -- corpus/SOURCES.md` is empty).

### The mirror repair deletes two committed lines — and it is done correctly

The two lines removed from the mirror are exactly the two rows F1 named: `| S262 | Google Search Central —
What is URL canonicalization — …` and `| S263 | Google Search Central — Googlebot — …`. The mirror is now
sha256 `cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117`, **byte-identical to
`007d66e:corpus/SOURCES.md`** (verified by `cmp`, 133 780 bytes, 143 rows). The artifact named `pre-append`
now actually is the pre-append registry. Note the repair rewrites an *evidence* artifact to match the live
registry at the mirror commit, and the live registry at `19a99bd` is blob `cd448eaf` — the same bytes as
base — so the reconstruction is faithful rather than merely convenient.

### The receipt handling changed mid-correction — the current state rewrites nothing

At the first observation (03:36) the committed line `0` in `census-exit.txt` had been replaced by `exit=0`,
with the attempt-1 originals copied under `pre-append/superseded/`. That supersession was itself
byte-faithful — `cmp` against `git show 19a99bd:…` returned IDENTICAL for all four receipts — so even then no
history was destroyed. But a committed receipt line *was* being rewritten, which is the exact move this
round's discipline forbids.

By the last observation (03:43) that rewrite had been reverted. All four committed receipts are again
**byte-identical to their commits**:

```
census-argv.txt:   == committed
census-exit.txt:   == committed
census-stderr.txt: == committed
census-stdout.txt: == committed
```

and the corrected run is carried by a **separate, additive** receipt set instead:

```
census-count-argv.txt    sources-census.sh census --file …/pre-append/corpus/SOURCES.md
census-count-stdout.txt  file rows 143 / file tier.A 120 / … / FLEET rows 143 / FLEET missing 0
census-count-stderr.txt  0 bytes
```

So the current state **rewrites no committed receipt line at all** — strictly better than the intermediate
state, and the correct resolution under this round's append-only rule. It also closes F5's evidential gap:
the LOG's "143 rows" figure is now evidenced by a `census` receipt that literally prints `rows 143` against
the corrected mirror, which the `validate` receipt never printed. The corrected `validate` run reproduces
stdout identical to attempt 1 (same 12 `W04` + `ok`), independently confirming that the two-row difference
changed no warning.

Two defects remain in this receipt set, both minor:

- **`census-count-exit.txt` is absent.** The count receipt carries argv, stdout and stderr but no exit code,
  so a reader cannot bind "the count run succeeded" to a committed byte the way the `validate` receipt's
  exit file allows. The `validate` convention in this same directory records exit; the count run should too.
- **`census-correction.txt` step 2 no longer describes the tree.** It says "the attempt-1 census receipt
  files were moved to `superseded/` unchanged, and the census was re-run" and that "`census-argv.txt`,
  `census-stdout.txt`, `census-stderr.txt` and `census-exit.txt` are this corrected run's receipt". In the
  current tree those four files are the attempt-1 bytes and the corrected run lives in `census-count-*`.
  The note is stale about its own repair — and it is the one document a later reader would consult to learn
  what happened here, so the staleness has outsized cost for its size.

### Append-only also holds for the other two files in the worktree

- `SCORECARD.md`: the committed 4146-line version is an **exact byte prefix** of the worktree file
  (`cmp` clean on the first 347 513 bytes). The +33 lines are a new section appended at EOF —
  `## Round 51 — declared claims (frozen at base 00766e, before any claim receipt)` — with 0 deletions.
  So this file is append-only in the worktree as well as untouched between the two committed revisions.
- `PROVINCE.md`: +15 insertions, 0 deletions.

### Outside my three assigned files: the two admitted entries are being rewritten in place (flagged for the C2 seats)

These are not `corpus/SOURCES.md`, `SCORECARD.md` or `LOG.md`, so they do not change my verdict — but they
are the same append-only question and they touch C2's subject, so I report what the bytes show rather than
let the observation die with my read.

Both entries committed new at `5591557` are now modified in the worktree: **41 insertions, 3 deletions**
across the pair. The three deleted lines are rewritten historical lines, named here verbatim:

```
canonical-selection.md:  -The page lists the variant classes it recognises, each quoted raw from the page:
crawler-identity.md:     -and names the two types beneath it [S263] (collapsed-only quotes; the source puts a space
crawler-identity.md:     -before the colon and breaks the lines):
```

Each is replaced by text that calls the committed wording false and says why. `canonical-selection.md`'s
"each quoted raw from the page" becomes "each quoted below as rendered text — the inline markup is removed,
so the space before each colon is this entry's rendering, not the source's bytes"; `crawler-identity.md`'s
"collapsed-only quotes; the source puts a space before the colon" becomes "rendered-text quotes … the page
closes the link element immediately before the colon", with the new section stating outright that "Two
claims this entry previously made are corrected here".

Three things are worth separating:

- **The correction is honest and self-documenting.** Each entry gains a `## Quote classes (round-51
  correction)` section that names the false label, gives the mechanism, and cites the measuring seat
  (`ExecQuoteRawScan`: 15 body quotations, 3 raw substrings, 2 collapse-only, 10 needing markup removal,
  none fabricated). That is the same "correct forward and say so" pattern the round used for the counter.
- **It is still a rewrite of committed text, not an append.** The committed labels are edited in place
  rather than superseded by a new record, so the pre-correction wording survives only in git history — not
  in a `superseded/`-style artifact, which is how the census receipts in this same round were handled.
- **Consequence a C2 seat should test.** `c51_quote_truth.py` reported 8 of 8 at both `5591557` and
  `9d13768` — i.e. against these pre-correction labels. If two labels in the very entries it scores were
  false, the 8/8 predicate does not cover quotation labelling: it could not have caught what this correction
  fixes. I did not run the counter (out of scope, sibling-owned) and I do not assert the predicate is
  wrong; I assert only that its 8/8 and this correction are mutually consistent only if labelling falls
  outside the eight conditions. The round's own landing text converges with that reading: its third new
  `LOG.md` bullet records that "C2's C8 reads the live registry at the mirror commit rather than the mirror,
  and C6 accepts URL containment and never reads `httpStatus`/`bytes`/`fetchedAt`", and routes the fixes to
  round 52 — i.e. the counter's conditions leave this labelling unmeasured, which is why it is being fixed by
  hand in the entries.

### Residual — CLOSED by the landing commit `907790c` (was LOW; resolved)

At observation (03:43) `LOG.md` was **unchanged** and the repair had no chronicle entry. That gap is now
closed. The lane advanced to `907790c`, and `LOG.md` gained **19 appended lines, 0 deletions** across three
new bullets — one of which is exactly the disclosure that was missing:

> - **Round 51 — the pre-append mirror is rebuilt, and the repair is disclosed.** Attempt 1's mirror
>   snapshot was byte-identical to the post-append registry; it was discarded and rebuilt from
>   `git show 19a99bd:corpus/SOURCES.md` (143 rows, sha256 `cd9ee4cf…`), the census re-run on it
>   (exit 0, W04 only), a `census` receipt added (`rows 143`) and attempt 1's receipt files kept in
>   `superseded/`. `assimilation/pre-append/census-correction.txt` records it. The predicate and the
>   eight condition sentences are unchanged.

That satisfies (a) contamination, (b) mirror-copy-only removal, (c) the `4ea81a5a… → cd9ee4cf…` change and
(d) the final receipt layout, including the `census` receipt reporting `rows 143`. The mirror in the landing
commit is byte-identical to the base registry (`cmp` clean), so the repair is complete and correct, and the
repair commit is itself append-only where it touches my files: `LOG.md` +19/0, `SCORECARD.md` +61/0,
`corpus/lessons/round-51.md` +85/0 all pure-tail, with the only 5 deletions in the whole 88-file commit being
the 3 entry-label lines and the 2 mirror lines named above.

Two smaller items from this section were **not** picked up by the landing and remain open:

- `census-count-exit.txt` is still absent — the count run carries argv, stdout and stderr but no exit code.
- `census-correction.txt` step 2 still describes the superseded layout ("the attempt-1 census receipt files
  were moved to `superseded/` unchanged, and the census was re-run … `census-exit.txt` are this corrected
  run's receipt") rather than the additive `census-count-*` layout the tree actually has.

Neither affects any predicate; both are one-line fixes if a later seat wants the evidence self-describing.

## What I did not verify, and why

- **C1 (`c51_wave_ledger.py`) and C2 (`c51_quote_truth.py`) predicate outcomes.** Out of this seat's
  assignment and owned by sibling seats; running them here would duplicate another seat's evidence, and I
  will not present their conclusions as mine. I read the counters' *effect* on these three files only
  (commit `9d13768` changes `c51_quote_truth.py` and appends 7 LOG lines, nothing else).
- I did not attempt to reconstruct authoring order beyond commit topology. Git ordered the commits; I
  verified the parent chain and the live blob at each step, which is as far as committed bytes can take the
  claim.
- The 12 `W04` duplicate-url warnings are pre-existing (none names S262/S263); I did not adjudicate them.

No file I attempted to read failed. Every command above exited 0; the only nonzero-ish signal reported is
that `SCORECARD.md` does not appear in the round's diff, which is the finding, not an error.

## Tooling

No tools installed or upgraded. Only `git` (`rev-parse`, `show`, `cat-file`, `diff`, `log`, `ls-tree`,
`merge-base`), `sed`, `awk`, `sort`, `uniq`, `comm`, `cmp`, `sha256sum`, `grep`, `wc`, `cut`, `nl`. All
read-only against the lane; scratch under `/tmp` (`/tmp/c51_tip_sources.md`, `/tmp/c51_base_sources.md`,
`/tmp/c51_tip_minus.md`, `/tmp/s_base.md`, `/tmp/s_tip.md`, `/tmp/c51_census.txt`). No `git add/commit/stash/
checkout/switch/reset/pull/push`, no `jj`, no writes outside this report file.
