# CriticAbsence — round 51, wave 1

Seat: `L1Kake51.CriticAbsence-2`. Lane: `kake-shokunin`. Mode: read-only critic, no subagents.
Base: `007d66e4e8360a5f88d29a93eeedd8066dad4434`. Lane tip at dispatch: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`.
Tool installs/upgrades: **none** (no pacman, no `uv tool`, no npm — nothing was needed).

Scope: attack every **proof-by-absence** in the round's artifacts — each claim that is true only
because something is *not* at a commit — and name what a later reader must re-check.

---

## 0. Verdict

**C2 scores 8/8, and four of its eight conditions still do not mean what their sentences say.**

| | Counts | Actually proves |
|---|---|---|
| C1 (operability) | 0/3 at base **and** 0/3 at the lane tip | Nothing yet. No C1 input exists in any commit. The instrument also returns 3/3 for an empty wave. |
| C2 (freshness) | 8/8 at tip | Corpus facts hold (entries, rows, bodies, sha256, Gate quotes). C7/C8 do not: the artifact named `pre-append` is byte-identical to the post-append registry, and the counter never reads it. |

Three findings are hard, reproducible, and independent of any other seat:

- **P0-a — the "pre-append mirror" is a post-append snapshot.** It carries both adopted rows at
  lines 152–153 and the round's own lesson file `corpus/lessons/round-51.md`, which only exists in
  the data commit. C8 passes anyway because it reads `corpus/SOURCES.md` *at the mirror commit*,
  not the mirror file.
- **P0-b — the C1 counter certifies an empty wave.** Zero seats, zero receipts, zero-duration clock,
  empty `LOG.md` → `ledger_checks_passed: 3, met: true`, exit 0 (demonstrated).
- **P0-c — the lesson's Mistakes ledger asserts a present string is absent.** "Google chooses the
  most complete and useful page as the canonical URL" is claimed "not in the source"; it is a raw
  substring of the retained `S262.html` at line 4073.

Additionally: both junk controls cite commits that do not exist in the object database, and the
8/8 was produced by a counter revision committed **after** the data commit; the counter frozen
before the data scores **7/8**.

---

## 1. Ledger of absence claims

`R` = "a later reader must re-check". All commands run from
`/home/vgpnk/Projects/shokunin/kake-shokunin`.

| # | Claim (short) | Commit it rests on | Result now |
|---|---|---|---|
| A1 | C2/C8: "the mirror's registry carries none of the adopted ids" | `19a99bd` (contract + mirror file) | **FALSE against the named file.** True only of a different file. |
| A2 | C1/after: "the settlement, the route receipts, the time-accounting artifact and the LOG figure are all committed" | `19a99bd` declared; tip `9d13768` | **FALSE.** None of the six inputs nor `route-probes/` nor `w1/` exist in the commit graph. |
| A3 | C1/before: "no ledger instrument, no route receipts, no time accounting" | base `007d66e` | True prose, **5 of 7 absences unmeasured** — the counter early-returns after two. |
| A4 | Lesson Mistakes: the staged canonical quote "is not in the source" / "Both were confirmed absent from the bodies this round fetched" | `5591557` | **FALSE.** Present raw at `S262.html:4073`. |
| A5 | Lesson Mistakes: "the page renders 'Googlebot Smartphone :' with a space before the colon" | `5591557` | **FALSE.** The body renders `…<b>Googlebot Smartphone</b></a>:` then a newline — no space, and the gap is markup, not whitespace. |
| A6 | Lesson: "the coverage map in `corpus/README.md` did not hold this ground" | `5591557` | **Contradicted by the same file**: `README.md:44` says the r22 entry covers "canonical signals versus selection"; `README.md:137` says selection "remain[s] open". |
| A7 | Controls: junk runs score 0/3 and 5/8 | `19a99bd` receipts | **Unreproducible.** `d969fa2…` and `cc57cb8…` are not in the object DB. |
| A8 | C1 instrument: absence of evidence counts as evidence of absence | `19a99bd` counter | **CONFIRMED.** Empty wave ⇒ 3/3 met. |

---

## 2. Detail

### A1 — the "pre-append" mirror contains the append (P0)

`c51_quote_truth.py` C8 does:

```python
mirror_commits  = git log --diff-filter=A --format=%H <rev> -- MIRROR
mirror_commit   = mirror_commits[-1]                     # git log is newest-first ⇒ oldest add
mirror_registry = show(root, mirror_commit, REGISTRY)    # corpus/SOURCES.md — NOT MIRROR
```

so the sentence "the mirror's registry carries none of the adopted ids" is evaluated against
`corpus/SOURCES.md` at `19a99bd`, never against the mirror.

The mirror file itself:

```
$ git show 19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | grep -nE '^\| S26[23] '
152:| S262 | Google Search Central — What is URL canonicalization — https://developers.google.com/…
153:| S263 | Google Search Central — Googlebot — https://developers.google.com/…
```

and the rows sit **inside** the registry section (`## Registry` at line 5, `## Paths` at 155).

Worse, the mirror is a full post-data snapshot:

```
$ diff <(git show 007d66e:corpus/SOURCES.md) \
       <(git show 19a99bd:…/pre-append/corpus/SOURCES.md)
151a152,153   > | S262 … | S263 …                     # base + exactly the two adopted rows

$ diff <(git show 5591557:corpus/SOURCES.md) \
       <(git show 19a99bd:…/pre-append/corpus/SOURCES.md)   # → empty
$ git cat-file -e 19a99bd:…/pre-append/corpus/lessons/round-51.md && echo YES
YES                                                   # the lesson is only born in the data commit
```

`pre-append/corpus/knowledge/canonical-selection.md` and `crawler-identity.md` are byte-identical
to their `5591557` versions. So the only artifact that could evidence "the rows were absent before
the append" is a copy of the state *after* the append. The C7 census validates that same file
(`census-argv.txt` names it) and prints `file ok`, so C7's receipt also cannot distinguish pre
from post: its 12 findings are all `W04` duplicate-URL warnings on *other* ids, and it never
mentions `canonicalization` or `googlebot`. The receipt is append-invariant except for its own
path line.

**Impacts:** C2 **C7, C8**; the C2 `before` sentence's "no pre-append mirror"; the lesson's
"census-validated with `--file` before the append". Not the corpus facts (A4 aside).

**Smallest safe correction.** Two lines, both honest:

1. In C8, read the mirror: `mirror_registry = show(root, mirror_commit, MIRROR)`, and add
   `if mirror_registry != show(root, BASE, REGISTRY): fail("mirror is not the pre-append registry")`
   with `BASE` a new argument. Then C8 fails here, as it should.
2. Re-take the mirror from `007d66e` (or from `git show 007d66e:corpus/SOURCES.md`), re-run the
   census on it, re-run C2. Expect 7/8 until that is done.

If the tree is meant to be the *knowledge-package* snapshot, rename the directory (it is not
pre-append) and delete the absence clause — do not keep a name that asserts a state it does not hold.

### A2 — C1's "after" names files that do not exist (P0)

```
settlement.json             base=no tip=no
wave-timing.json            base=no tip=no
round-time-accounting.json  base=no tip=no
route-map.json              base=no tip=no
w51-taskcall.json           base=no tip=no
wave-grant.txt              base=no tip=no
route-probes/ (committed paths)  0
w1/ (committed paths)            0        (19 reports were sitting untracked during this seat)
```

`python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768…` →
`C1 ledger 0/3 met=False`, exit 1. The counter has no worktree read path (`git show` only), so
untracked evidence can never move the number.

**R:** run the same command at the settlement commit the round eventually names — the contract
does not name one, so a later reader cannot tell whether "the measured commit" means `9d13768` or
some later commit. **Correction:** the contract must name the commit in `after` (e.g. "3 of 3 at
`<settlement-commit>`"), and must not say "committed" while the bytes are untracked.

### A3 — C1's "before" overstates what the counter measured

At base the counter prints exactly two notes: `settlement receipt absent` and `route map absent`;
L3 also fails on the settlement before it ever looks at timing/accounting. So the contract's seven
named absences reduce to two measured ones. I checked the other five directly — all genuinely
absent at `007d66e` (`route-probes/` → 0 paths; `wave-timing.json`, `round-time-accounting.json`,
`w51-taskcall.json`, `wave-grant.txt` → `cat-file -e` fails). The prose is true; the *do-nothing
control* is a two-fact proof dressed as three checks.

**R:** `git ls-tree -r --name-only 007d66e -- .ufo/waves/round-51/route-probes` and
`git cat-file -e 007d66e:<each path>`.

### A4 — the Mistakes ledger calls a present quote absent (P0)

`corpus/lessons/round-51.md` (commit `5591557`):

> the staged `canonical-selection.md` quotes "Google chooses the most complete and useful page as
> the canonical URL", which is not in the source … **Both were confirmed absent from the bodies
> this round fetched.**

The retained body, at the measured commit:

```
$ git show 9d13768:.ufo/waves/round-51/sources/S262.html > /tmp/s262.html
S262 offset: 145222  line: 4073
…[[],["Canonicalization is the process of selecting a representative URL for duplicate content.
 Google chooses the most complete and useful page as the canonical URL, indexing it more
 regularly. …
```

By the round's own test — C5's "exact raw substring of the retained body" — this string is
**present**. The staged source note (`shokuknow/lanes/kake/round2/SOURCES-PROPOSED.md:41`) and the
staged entry (`KNOWLEDGE-PROPOSED.md:36-37`) both quote it correctly.

So the round attributes a fabrication to the package where the package was faithful. The real
story is only that the sentence lives in the page's embedded summary block, not its prose.

**Impacts:** freshness's learning claim (the "mistake" is false provenance); the lesson's
credibility as an honesty artifact. Not C5, which never reads the Mistakes section.

**Correction:** replace that mistake with what the bytes show — "the quote is a raw substring of
the retained body but only inside the page's embedded summary; the entry must say which block" —
or drop the entry. Do not leave a false accusation of fabricated quotation.

### A5 — the Googlebot "space before the colon" story is wrong

```
$ python3 …  # S263.html
'Googlebot Smartphone: a mobile crawler that simulates a user on a mobile device'  → present=False
'Googlebot Smartphone : a mobile crawler'                                        → present=False
```

The body (line 3883) is:

```html
<a href="…#googlebot-smartphone"><b>Googlebot Smartphone</b></a>:
    a mobile crawler that simulates a user on a mobile device.
```

Rendered text is exactly the staged quote. The lesson's stated cause ("a space before the colon")
does not exist; the split is an anchor close plus a newline. The staged quote is **collapsed-only**,
not fabricated — the same mislabel as A4.

**R:** `git show 9d13768:.ufo/waves/round-51/sources/S263.html | grep -n -A1 'googlebot-smartphone'`.

**Correction:** state the class correctly ("collapsed-only: anchor close and newline between the
name and the colon"), consistent with the entry's own "collapsed-only quotes" labels.

### A6 — the coverage-map absence is self-contradictory

`corpus/README.md` at `9d13768`:

```
 44: | Static canonical preflight (r22) | knowledge/static-canonical-preflight.md | … canonical signals versus selection, parser/URL limits; …
137: JS-rendered canonicals, Google-selected canonical, live delivery, … remain open.
```

The held entry itself disclaims selection (`static-canonical-preflight.md:8-9`), so the lesson's
claim is defensible against the entry but **not** against the coverage map row it cites. And the
data commit does not touch `README.md` (`git show --stat 5591557` → 5 files, README absent;
`grep -c -i 'round[- ]\?51'` on README = 0), so the two new entries appear in no coverage-map row.

**R:** `git show 9d13768:corpus/README.md | sed -n '44p;137p'` and `git show --stat 5591557`.

**Correction:** add a round-51 row naming both entries, and reconcile line 44's "versus selection"
with the entry's own disclaimer.

### A7 — both junk controls cite commits that do not exist

```
$ git cat-file -t cc57cb80b2060f8c754a896235e323f67a5a91da   # c2-junk-entries.txt
fatal: git cat-file: could not get object info
$ git cat-file -t d969fa2819f1f2050c10637531cba2e12f92a557   # c1-junk-wave.txt
fatal: git cat-file: could not get object info
```

Both receipts (`controls/`, commit `19a99bd`) are therefore unfalsifiable: no reader can re-derive
`0/3` or `5/8` against the cited trees. This matters more than usual this round, because the tips
of both counters lean on "the junk control still fails".

**Correction:** commit the junk trees (or a regenerating script) under the wave dir and re-run both
counters; store the new revision ids in the receipts.

### A8 — the C1 instrument's strongest counterexample: an empty wave passes (P0)

Built in `/tmp/r51probe` (no lane bytes touched): one commit containing a settlement with
`spawn: 0`, `reports_written: 0`, `settled: []`, `dead: []`; a payload with `tasks: []`; a route
map with `{"kimiModel": null}`; no `route-probes/`; `startedAt == settledAt`; accounting all
zeros; a grant line; an empty `LOG.md`.

The `/tmp` tree is ephemeral. This recipe rebuilds it byte-for-byte, from a clean shell:

```sh
R=/tmp/r51probe; rm -rf $R; mkdir -p $R/.ufo/waves/round-51; cd $R
git init -q .; git config user.email p@x; git config user.name p
printf '%s' '{"spawn":0,"reports_written":0,"settled":[],"dead":[],"settled_count":0,
"dead_count":0,"timeout_seconds":600}' > .ufo/waves/round-51/settlement.json
printf '%s' '{"counts":{"spawn":0},"taskCall":{"tasks":[]}}' > .ufo/waves/round-51/w51-taskcall.json
printf '%s' '{"roles":{"scout":{"kimiModel":null,"probe":""}}}' > .ufo/waves/round-51/route-map.json
printf '%s' '{"startedAt":"2026-10-25T00:00:00Z","settledAt":"2026-10-25T00:00:00Z"}' > .ufo/waves/round-51/wave-timing.json
printf '%s' '{"wall_clock_seconds":0,"aggregate_seat_seconds":0,"dead_seat_seconds":0}' > .ufo/waves/round-51/round-time-accounting.json
printf 'granted lane=kake\n' > .ufo/waves/round-51/wave-grant.txt
: > LOG.md
git add -A && git commit -qm probe
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/c51_wave_ledger.py \
        --root $R --revision HEAD --json
```

Run from any directory; the counter path is the lane's committed script, and `--root` points at
the throwaway repo. Expected: `"ledger_checks_passed": 3, "met": true`, exit 0.

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root /tmp/r51probe --revision HEAD --json
  "L1": {"passed": true, "facts": {"payload_spawn": 0, "settlement_spawn": 0, "payload_seats": 0,
          "settlement_seats": 0, "settlement_reports_written": 0, "committed_report_files": 0}}
  "L2": {"passed": true, "facts": {"roles": 1, "receipts": 0}}
  "L3": {"passed": true, "facts": {"aggregate_seat_seconds": 0, "dead_seat_seconds": 0,
          "wall_clock_seconds": 0}}
  "ledger_checks_passed": 3, "met": true        exit 0
```

Mechanisms:

- **L1** compares counts only; `0 == 0` satisfies "the settlement's spawn equals the payload's seat
  count" and "reports_written equals committed reports".
- **L2** builds `used` from `kimiModel` only; a role with no `kimiModel` contributes nothing to the
  set, and an empty set requires no receipt. `if not roles` guards only a *fully* empty map.
- **L3** guards the `LOG.md` requirement with `if wall > 0`; `wall == 0` skips it entirely, and the
  check is a substring test (`str(wall) in log_text`), so `12` would be satisfied by `120`.
- Non-`kimiModel` route keys are never inspected; a failing model bound under any other key would
  be invisible.

**Impacts:** the operability frontier step and the r50-1/r50-3 routed defects — this is exactly the
"prose replaced by a re-derivable ledger" claim, and the ledger currently accepts a wave that never
ran. **Correction (four lines):** require `payload_spawn >= 1`; require every role to carry a
non-empty `kimiModel`; require `wall > 0`; require `len(receipts) >= len({r["kimiModel"] for r in roles.values()})`.

---

## 3. What actually holds (independently verified, not taken from the counter)

These are C2's real assets and I could not break them:

- Both entries exist at `corpus/knowledge/canonical-selection.md` (77 lines) and
  `crawler-identity.md` (54) at `9d13768`; both are new files at `5591557`.
- Both registry rows at `corpus/SOURCES.md:152-153`, **11 cells each**, status `mined`, opened
  `2026-10-24`, recheck `180d`, `used-by` = exactly the one entry.
- Retained bodies committed; sha256 re-derived by me and equal to `receipts.json`:
  `S262 7922243…50d23b`, `S263 6afbdc8…e155de`.
- Gate quotes are raw substrings: `indicating a canonical preference is a hint, not a rule` → 1 hit
  in `S262.html`; `Googlebot is the generic name for two types of` → 1 hit in `S263.html`.
  10 and 9 words respectively, inside 6–25.
- Base registry really has no `S262`/`S263` (`grep -c` → 0 each), and the collision set
  (`S273`, `S274`, `S286`) is real: the lane holds those rows.
- `crawler-identity` is genuine new ground: the base lane mentions `Googlebot` in three knowledge
  files but never states the two-subtype identity.

So the freshness *content* lands. The freshness *evidence chain* (C7, C8, the Mistakes ledger)
does not.

## 4. Instrument identity: the 8/8 was produced by a counter committed after the data

```
$ git show 19a99bd:.ufo/waves/round-51/c51_quote_truth.py > /tmp/q51_frozen.py
$ python3 -B /tmp/q51_frozen.py --root . --revision 5591557        → C2 7/8, exit 1
$ python3 -B /tmp/q51_frozen.py --root . --revision 9d13768…       → C2 7/8, exit 1
$ python3 -B .ufo/waves/round-51/c51_quote_truth.py … --revision 9d13768… → C2 8/8, exit 0
```

The only difference (`9d13768`) is a two-line unwrap of the `sources` key in `receipts.json`. The
contract says the claims "were declared and frozen BEFORE any score"; the *declaration* was, the
*instrument that produced the score* was not. `LOG.md` (added at `9d13768`) then asserts
"Re-run at the append commit `5591557`: C2 8 of 8 (exit 0)" — **false under the frozen counter**
(7/8).

**Correction:** name `9d13768` as the counter revision in the contract and in the LOG, and say
plainly that the fix moved 7→8 by repairing a lookup, not by changing a condition. A reader
scoring with the frozen bytes must get the same number the round reports.

## 5. Residual instrument holes (not currently exploited, still worth closing)

- `C6`: `if receipt.get("url") not in row[1]` is a substring test; `url: ""` passes vacuously. Use
  equality on the URL extracted from the row.
- `C8`: `mirror_commits[-1]` is the **oldest** add (git log is newest-first). After a delete/re-add
  it scores the stale add.
- `C7`: "no `E03`/`E04`" is treated as clean; the census did emit 12 `W04` warnings. Say
  "no error-class finding", not "clean".
- Lesson "no quarantined id was hand-checked this round" is an absence about an *action*; bytes can
  show the register was listed (`assimilation/quarantine-slice`, 11 ids) but never that no check
  happened. Reword as a scope statement, not a fact.

## 6. Commands that produced this report

```
git rev-parse HEAD; git log --oneline -8; git status --porcelain
python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 007d66e…   # 0/3
python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768…  # 0/3
python3 -B .ufo/waves/round-51/c51_quote_truth.py  --root . --revision 007d66e…  # 0/8
python3 -B .ufo/waves/round-51/c51_quote_truth.py  --root . --revision 9d13768…  # 8/8
git show 9d13768 -- .ufo/waves/round-51/c51_quote_truth.py LOG.md
git show 19a99bd:.ufo/waves/round-51/c51_quote_truth.py > /tmp/q51_frozen.py
python3 -B /tmp/q51_frozen.py --root . --revision 5591557                        # 7/8
git show 19a99bd:<mirror> | grep -nE '^\| S26[23] '                              # 152,153
diff <(git show 007d66e:corpus/SOURCES.md) <(git show 19a99bd:<mirror>)           # +2 rows
diff <(git show 5591557:corpus/SOURCES.md) <(git show 19a99bd:<mirror>)           # empty
git cat-file -e 19a99bd:<mirror dir>/corpus/lessons/round-51.md                   # YES
for p in settlement wave-timing round-time-accounting route-map w51-taskcall; do git cat-file -e …; done
git ls-tree -r --name-only 9d13768 -- .ufo/waves/round-51/{w1,route-probes}       # 0, 0
git cat-file -t cc57cb8… ; git cat-file -t d969fa2…                              # fatal ×2
python3 (find "Google chooses the most complete…" in S262.html)                   # line 4073, present
python3 (find Googlebot staged quotes in S263.html)                               # absent; body renders "<b>…</b></a>:"
python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root /tmp/r51probe …           # 3/3 met, empty wave
```

## 7. Bounds observed

Read-only. Wrote only this file. Scratch confined to `/tmp` (`/tmp/r51probe`, `/tmp/s262.html`,
`/tmp/s263.html`, `/tmp/q51_frozen.py`). No `git add/commit/stash/checkout/reset` and no mutating
`jj`. Did not touch `considerthese/`, `.ufo/waves/round-46/residual/`, the >1 MiB round-48 copies,
or `shokuknow` (read-only greps there only).

**Scratch is ephemeral; the report body is the durable evidence locus.** This report cites no
lane-resident scratch and no `.ufo/waves/round-35/` path at all — the round-35 `scratch/` →
`scratch-evidence/` relocation discussed by `L1Mado35.RevEntryR15` and `L1Mado35.RevQuoteS210`
belongs to another lane and dangles nothing here. Three `/tmp` artifacts could still vanish:

- `/tmp/r51probe` (A8) — the rebuild recipe is inlined in §2 A8; no external file is needed.
- `/tmp/q51_frozen.py` (§4) — regenerated in one line from `git show 19a99bd:<counter> > /tmp/…`;
  the two-line diff is also quoted in §4.
- `/tmp/s262.html`, `/tmp/s263.html` — both are `git show 9d13768:<body>` and need no copy.

So every claim survives deletion of `/tmp`; none needs a re-created scratch tree.

## 8. Frontier-step judgement

- **C2 (freshness):** the step is real in the corpus — two source-backed entries, two rows, retained
  bytes with matching digests, Gate quotes raw. It is *not* evidenced end-to-end: C7/C8 certify a
  mirror that already contains the append, and the Mistakes ledger carries two false absence
  claims. Net: the knowledge is new; the proof that it was new is not.
- **C1 (operability):** no frontier step exists in committed bytes. The instrument that would
  certify one returns 0/3 at every commit named, and 3/3 for a wave with zero seats. The r50-1 and
  r50-3 defects are not yet addressed — they have been re-expressed as a counter that a null wave
  satisfies.

## 9. Worktree drift observed during this seat (not caused by this seat)

All findings above rest on **committed** bytes (`--revision 9d13768…`), which are unchanged. But the
worktree moved under me between 03:34 and 03:40 UTC-3, so a reader who re-runs a `diff` against the
working tree instead of the commit will see different bytes. Observed at 03:40:

```
$ git status --porcelain | grep -v '^??'
 M .ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md   # 2 rows deleted (S262,S263) at 03:36:34
 M PROVINCE.md                                                      # +15 lines, 03:38:13
 M SCORECARD.md                                                     # +33 lines, 03:34:47
 M corpus/knowledge/canonical-selection.md                          # +21 lines, 03:39:51
 M corpus/knowledge/crawler-identity.md                             # +23 lines, 03:39:51
```

The entry edits add a `## Quote classes` section and withdraw the phrase "the source puts a space
before the colon", which corroborates A5 independently of my derivation. The mirror edit deletes the
two adopted rows from the working copy — i.e. someone is repairing A1's artifact — but **`19a99bd`
still contains them**, so A1 is unaffected as evidence and C8 will still pass on the old commit.

This seat wrote none of these; its only write was this file.
