# CriticClaims — round 89, falsification of the two frozen claims

Seat: leaf member, no dispatch. Lane `kake-shokunin`. Base `76225160`, freeze
`08ab46a1`, dispatch `2e700b9a`. Every number below is from a receipt in
`w1/CriticClaims/receipts/`; the lane moved under me twice (`f62e7954`,
`9784ad54`) and I name the revision each measurement used.

## 0. Verdict

**C1 (calibration, 2 HOLD) does not survive as declared.** Its six items are not
six observations: one is behavioural (A), one is a git-process check (E), one
recounts a self-chosen revision (D), and three are text-decided (B, C, F) — and
the counter's own do-nothing instrument reaches `open=0 closed=6 met=true` with
`.ufo/` and `scripts/` byte-identical to base. Two further hard falsifications:
item E is not revision-pinned, so the frozen base line `open=6` no longer
reproduces (`open=5` today); and item E reports **closed** on this round although
the round's own freeze was amended after dispatch (`46a43e94` at 18:16:18, three
minutes after `2e700b9a` at 18:13:04), rewriting the frozen base receipt in place
and weakening the shortcut guard. The item that exists to prevent
freeze-after-dispatch cannot see it.

**C2 (freshness, 10 HOLD) reaches its predicate at `9784ad54` and still does at
`a225647f` (`frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true`, exit
0), but the target certifies the instrument's sample, not the declared
capability.** A candidate that never escapes the URI and a candidate that strips
all whitespace instead of SP/HTAB both score `16/16 + 200/200 + 9/9` — and they
score it at **all four seeds tried** (`89089`, `1`, `7`, `424242`), so the
"seed-generated population" defence does not apply. The URI mutant produces a
*key collision between two distinct logical requests*, the exact property the
claim says it certifies. A 421-entry table over the committed seed and committed
generator also reaches `met=true`, i.e. round 88's R88-1 was reproduced, not
fixed.

**Live confirmation of the C1 pattern.** At `a225647f` the lane's own C1 is
`open=1` — the only open item is A, the one behavioural item — because
`corpus/lessons/round-89.md` now carries exactly the four markers my prose-only
control wrote: `gate-sample: admits=2 rejects=2`,
`r88-gate-summary-correction: admits=2 rejects=2`, `r88-c-rerun: retracted`,
`controls-count: 1604@21770586…` (`receipts/live-c1-closure.txt`). B, C, D, F
and E are green; no behaviour changed for B, C, D or F.

Axes: calibration is harmed in method (not in number); freshness is unharmed in
number but mislabelled; operability is unharmed.

## 1. Axes named

- **calibration** — the lane's own instruments agree with observed repo state.
  C1 claims to move it.
- **freshness** — HTTP freshness (lifetime, Age, revalidation). C2 is labelled
  here.
- **operability** — a capability the lane can run. C2 is actually this.

## 2. C1 — calibration

### 2.1 Is C1 causally separable from C2? No.

Item E resolves the commit that *adds* `.ufo/waves/round-89/c89_key.py` — a C2
artifact — and requires it to precede the commit that adds `w1.ready`. The base
receipt records the dependency from the other side: at base the counter's only
E failure is `no commit adds .ufo/waves/round-89/c89_key.py`
(`receipts/base-c1-as-filed.txt` = the frozen `controls/base-c1.txt`). So with
C2 unlanded, E cannot close and C1 cannot reach `met=true`.

The coupling is one-way and narrow: C1 needs C2's *commit existence and
committer time*, never C2's *score*. A C2 that fails its own target but lands
the freeze file before dispatch still lets C1 pass. But the two claims therefore
share a single failure mode, and the freeze's "two claims on distinct axes" is
true of the axes and false of the measurements.

Smallest correction: move E into its own third claim, or state the coupling in
`freeze.md` and in the C1 predicate line.

### 2.2 Which of the six items are decided by prose?

| Item | Decided by | Independent observation? |
|---|---|---|
| A-selftest-number | runs `vary_match.py --selftest` at the revision **and** a SCORECARD marker | **yes** (behavioural) |
| B-gate-sample | round-88 `## Gate` table vs two markers in round-89 lesson | **no** — prose against prose |
| C-receipt-pointers | existence of named paths, plus `r88-c-rerun: retracted` | **no** for the re-run claim; the retraction is a magic word |
| D-revision-pinned-count | marker `N@rev` vs a recount at that rev | **yes**, but the rev is self-chosen and the recount is mode-dependent (2.6) |
| E-freeze-before-dispatch | two commit objects | **yes** (git), but not revision-pinned (2.5) |
| F-lesson-shape | `## Mistakes` with five column names and ≥1 row, plus any tagged line in the round-88 lesson | **no** — shape only |

So four of six are decided by prose the counter itself does not cross-check
against an independent observation, and B is prose against the *same* prose
family (the round-88 lesson's table is the only source for both sides).

**Does that make C1 a calibration claim or a bookkeeping claim?** Bookkeeping.
Calibration means the lane's statements match observed repo state; C1's pass
condition is that the lane's *new* statements match the counter's parse of the
lane's *old* statements, plus one behavioural item (A) and one git item (E). The
freeze's own guarantee — "No item is scored from prose alone where a behaviour
is available" — is false for C: a behaviour was available (commit the re-run
receipt, or remove the claim) and the counter accepts `retracted` instead.

### 2.3 The do-nothing control — measured

Built against a scratch mirror of the base tree (`git archive 76225160`), with
`--mirror` (the only non-committing mode the counter offers).

- **D0, literal do-nothing** — base bytes plus a `corpus/lessons/round-89.md`
  that names only the six ids: `items=6 open=5 closed=1 met=false`, exit 1
  (`receipts/c1-d0-ids-only.txt`). E is already `[]` — see 2.4.
- **D1, prose-only closure** — base bytes, three `[r89-correction]` tags, one
  `integrated-selftest: 35/35` line, a `## Mistakes` table, and four marker
  lines (`gate-sample`, `r88-gate-summary-correction`, `r88-c-rerun:
  retracted`, `controls-count`). **Zero** change under `scripts/` and `.ufo/` —
  `diff -rq` reports both trees identical (`receipts/c1-d1-integrity.txt`) —
  and no receipt added. Result: `items=6 open=0 closed=6 met=true`, exit 0
  (`receipts/c1-d1-prose-only-mirror-count.txt`).

So the answer to the seat's question is two-part and both parts matter:

1. The *literal* control (ids only) does **not** reach `met=true` — the freeze's
   sentence is true for that exact text.
2. The *cheapest next step* — writing the numbers the counter parses, with no
   behavioural change at all — does reach `met=true`. C1 therefore certifies
   that a round can write the right sentences, not that six defects closed.
   A bookkeeping claim with a behavioural item attached is still a bookkeeping
   claim when five of six items can be satisfied by text.

**The live lane confirms the pattern rather than refuting it.** At `a225647f`
the real C1 prints `open=1` with A as the only open item
(`receipts/c1-final-head.txt`), and `corpus/lessons/round-89.md` carries exactly
the four markers my fixture wrote — including `r88-c-rerun: retracted` and a
restated `controls-count: 1604@21770586…`
(`receipts/live-c1-closure.txt`). Five of the six items closed without a single
behavioural change: B restated a count that the round-88 lesson had already
corrected in an append, C wrote `retracted` for a claim that exists in committed
bytes only as a quotation in the spot-check, D pinned a self-chosen revision, F
supplied a five-column table, and E passed because `--diff-filter=A` cannot see
`46a43e94`.

### 2.4 The round's own freeze-after-dispatch, invisible to E

Measured (`receipts/freeze-v2-after-dispatch.txt`):

```
08ab46a1  1793826745  2026-11-04T18:12:25  round-89: freeze — ...
2e700b9a  1793826784  2026-11-04T18:13:04  round-89: wave-1 dispatch evidence ...
46a43e94  1793826978  2026-11-04T18:16:18  round-89: freeze v2 — shortcut guard ...
merge-base --is-ancestor 2e700b9a 46a43e94  ->  rc=0
```

`46a43e94` changed the frozen counter and the frozen base receipt after the wave
was dispatched:

- `FORBIDDEN` went from six tokens including `'.ufo/waves'`, `'round-89'`,
  `'frozen'`, `'oracle'` to three tokens, plus a line-level check that only
  fires when one line contains both `open(` and `.ufo`. A source can now read
  the frozen case file through a path variable on another line.
- `controls/base-c2.txt` was **rewritten in place** (last line `'.ufo/waves'` →
  `'c2-cases'`), which is precisely what the round-88 spot-check forbade under
  R88-A: "correct the number in a new entry, never by rewriting filed bytes".

Item E still prints `"E-freeze-before-dispatch": []` at `9784ad54`, because
`--diff-filter=A` only ever looks at the *adding* commit. E is blind to
amendments, which is the freeze-after-dispatch event it exists to catch. The
round committed the defect it claims to close, and its instrument reported
green.

Smallest correction: E must bound the *last* commit touching the round's frozen
artifacts, not only the first that adds one:

```
git log -1 --format=%ct -- <freeze paths>   must be < committer time of w1.ready
```

and the same check must include every path the freeze declares
(`c89_key.py`, `c89_defect_queue.py`, `c2-contract.md`, `frozen/`,
`controls/`).

### 2.5 The base predicate no longer reproduces

Frozen predicate: "the same counter at the base prints `open=6 closed=0
met=false`, exit 1". Re-run today at `76225160` (`receipts/c1-base-rerun.txt`):

```
C1v1 revision=76225160... items=6 open=5 closed=1 met=false
"E-freeze-before-dispatch": []
```

`item_e` ignores `--revision` entirely: it runs `git log` over the whole
repository and therefore sees the freeze and dispatch commits that did not exist
when the receipt was filed. The filed receipt is honest *as captured*; the
predicate is not reproducible. That is the same class as R88-D ("a count that
names no revision"), reproduced inside the counter that claims to close R88-D.

Smallest correction: resolve both commits relative to the measured revision
(`git rev-list <rev> -- <path>`) so the base line stays `open=6`.

### 2.6 Mode inconsistency: the recount depends on how you ask

One tree, two answers (`receipts/count-mode-mismatch.txt`):

```
git ls-tree -r --name-only <rev> | grep -c '/controls/'    -> 1590
Path('.ufo/waves').glob('*/controls/**/*')                 -> 1002
find .ufo/waves -path '*/controls/*' -type f               -> 1590
```

The mirror glob only matches `.ufo/waves/<wave>/controls/`, so nested controls
trees (`.../w1/<seat>/controls/...`) are invisible to it; git mode counts any
path containing `/controls/`. The split is exact
(`receipts/count-mode-explanation.txt`): **1002** depth-2 control files + **588**
nested ones = **1590**. Consequence: a `controls-count` marker that is
true in git mode (1590@base) is rejected in mirror mode, and a marker that the
mirror mode accepts (1002) is false at the named revision in git mode
(`receipts/c1-d1-prose-only-git-count.txt` shows D as the *only* open item when
the marker is git-true). The counter's selftest never sees this because it only
builds depth-2 control trees.

### 2.7 Fidelity of the six items to the six routed defects

Routed text is `corpus/lessons/round-88-verifier-spotcheck.md` (added by the
base commit itself), `## Routed defects`.

- **R88-A** → A: faithful and behavioural. The receipt is the authority: the
  cited `controls/integrated-selftests.txt` prints `selftest: 35/35 passed` and
  the tool prints `35/35`; the prose says `22/22` at `SCORECARD.md:5469`,
  `:5488` and `corpus/lessons/round-88.md:265`
  (`receipts/r88-a-authority.txt`). This is the one item that observes.
- **R88-B** → B: **unfaithful**. The routed defect is the *report's* `Sources &
  frontier` summary ("one admit and three rejects"). Item B never reads any
  report; it parses the round-88 `## Gate` table (2 admits, 2 rejects) and
  requires the round-89 lesson to restate `admits=2 rejects=2`. It therefore
  certifies a new sentence, not a corrected one — and the round-88 lesson
  already carries an append-only note at line 335 correcting the same thing, so
  B re-states a correction that already exists.
- **R88-C** → C: **partially unfaithful**. The routed fix is "commit the re-run
  receipt with its revision or drop the claim". `r88-c-rerun: retracted` is
  accepted with no check that the claim was dropped; and the claim's text is not
  in committed bytes at all (it appears only as a quotation in the spot-check),
  so the retraction is unlinked from anything.
- **R88-D** → D: **partially faithful**. The routed object is the unpinned
  `1,577 tracked files` count, which lives at **`LOG.md:3021`** — a path item D
  never reads (`receipts/r88-b-and-d-objects.txt`). D checks a self-chosen
  `N@rev` marker. The routing did say "pin the revision in the next filing", so
  D is faithful to the letter, but it cannot tell whether the offending
  statement was pinned.
- **R88-E** → E: faithful in intent, broken in execution (2.4, 2.5).
- **R88-F** → F: shape only. Five column names, one row, and any line in the
  round-88 lesson containing both `[r89-correction` and `L1 mistakes`. A pointer
  sentence that names nothing passes.

## 3. C2 — capability vs instrument

Measured with the counter's own `score_candidate` (the same function
`main()` uses), seed 89089, `receipts/c2-probe.txt`:

| candidate | frozen | props | refuse | met |
|---|---|---|---|---|
| reference | 16/16 | 200/200 | 9/9 | true |
| **URI never escaped** | 16/16 | 200/200 | 9/9 | **true** |
| **values stripped of all whitespace** | 16/16 | 200/200 | 9/9 | **true** |
| table over the generated population (421 entries) | 16/16 | 200/200 | 9/9 | **true** |

Both mutants violate `c2-contract.md` §4 ("In the URI, each name and each value,
`%` becomes `%25`…") and §3 ("trimmed of leading and trailing SP and HTAB")
respectively. The URI mutant is the decisive one, because it breaks the property
the claim itself names:

```
{'uri': 'https://e.test/a\x1faccept\x1egzip', 'request_headers': {}}  ->  key K
{'uri': 'https://e.test/a', 'headers': {'accept': 'gzip'}, 'vary': 'accept'} ->  key K
collision: True
```

Two distinct logical requests map to one key. The claim says "separators escaped
so distinct logical inputs cannot collide". The target says `met=true`.

**Does the target measure the capability or the instrument?** The instrument's
sample. The sample is fixed: the seed `89089` and the generator `_props` are
committed in the same commit as the counter, and the oracle is embedded in that
same file. "Generated at scoring time from a committed seed" is a committed
table with extra steps.

Population shape (`receipts/c2-probe.txt`): 200 properties, **100 `same` and 100
`different`**. The 100 `same` relations are satisfied by any constant key — the
committed `ctl-constant-key` stub scores `props=100/200` from a constant. So the
discriminating half of the target is 100 comparisons, and 16 exact-form cases.

Seed stability (`receipts/c2-seed-stability.txt`): both mutants score
`16/16 + 200/200 + 9/9 met=true` at seeds `89089`, `1`, `7` and `424242`. The
missing coverage is a property of the *generator's URI and value alphabets*, not
of the seed: `_rand_case` draws URIs only from `a`, `b`, `c/d`, `p?q=1`, `r#f`
(no `%`, no control characters) and `VALS` only from `gzip`, `br`, `GZIP`,
`deflate`, `en`, `50%`, `a<US>b`, `' v '`, `x<RS>y`, `''` (no `\x0b`/`\x0c`).
Changing the seed cannot reach a clause the alphabet excludes.

### 3.1 Strongest argument that the counter certifies nothing

The counter contains its own oracle, the population is derived from a seed
committed beside it, and the guard is textual and disclosed as such. Therefore
the maximum information the receipt carries is "this candidate agrees with the
reference on 225 public inputs", which is satisfiable without implementing the
contract (measured: 421-entry table, `met=true`). Round 88 already routed this
exact defect as **R88-1** with the fix direction "hold the population outside
the candidate's reach and score a batch frozen after the candidate is (a keyed
digest revealed at scoring, or an independent seat's batch)". Round 89 did
neither: the seed is still committed, the population is still generated by the
scored code, and the oracle is still in the counter. So C2 re-certifies R88-1's
false green while the freeze claims the opposite ("a table over the committed 16
cases cannot reach it" — true of 16 cases, false of the 200 generated ones).

### 3.2 Strongest counter-argument

The 225 inputs are not arbitrary: they cover ten declared semantic classes
(name case, member order, member OWS, value OWS, value case, URI change,
unrelated header, absent vs empty, separator collision, percent) and the
reference's five mutants (no-escape, no-trim, case-fold, no-sort,
absent=empty) are each killed, so every clause the population *names* is
discriminated. The 16 frozen cases pin exact byte form and the 9 refusals pin
the refusal surface, and the contract's seven worked examples are re-derived
from the reference before scoring, so oracle/contract drift fails the selftest
rather than passing. Behavioural equivalence on a clause-covering population is
the only meaningful reading of "can construct the key" — capability claims are
always sample-bounded, and the freeze discloses the bound. On that reading the
gap is **coverage**, not instrument: the population simply lacks a URI-escaping
class and a non-SP/HTAB whitespace class, which is a case-set defect fixable
with two frozen cases and two property classes.

I hold the first reading for the *claim as written*, because the claim asserts a
collision property the accepted mutant violates; but the counter-argument is
correct about the fix: this is a missing-case defect, not a proof that nothing
is measured.

### 3.3 Is C2 really freshness?

No. `c2-contract.md` `## Scope` says: "It does not decide storability,
freshness, revalidation, reuse, or what any server or browser does." Freshness
in RFC 9111 §4.2 is lifetime, Age and revalidation — none of which the artifact
computes. The freeze itself calls C2 "bounded capability acquisition", which is
an operability/coverage phrase. Round 88 used the same bucket ("Axis-fit is a
bounded capability move, as in r86/r87"), so this is a lane convention, not a
new error — but it is false provenance: if the scorecard ever moves freshness on
this artifact, it records a freshness change that did not happen. Today it does
not move (10→10 HOLD), so the harm is a label, not a number.

## 4. Does the round harm an owned axis?

- **calibration — harmed in method.** The round banks closure on an instrument
  that (a) is not revision-pinned on E, so its base predicate is unreproducible;
  (b) reaches `met=true` on prose alone; (c) was itself amended after dispatch,
  with a frozen receipt rewritten in place, while its E item printed closed. A
  lane that accepts this learns that bookkeeping satisfies calibration — a
  regression in the practice the axis is supposed to measure.
- **freshness — not harmed in number.** No score delta; the artifact does not
  touch freshness. Mislabelled (3.3).
- **operability — not harmed.** `scripts/cache_key.py` landed at `9784ad54` as a
  standalone stdlib script with no caller; it adds surface but no runtime
  obligation. The only new obligation is the dispatch-ordering rule, which the
  round itself then violated (2.4).

No whole-corpus no-harm claim is made here; this is lane-internal.

## 5. Defect list (severity, in the round's own counters/contract/cases)

| id | sev | defect | receipt |
|---|---|---|---|
| D89-C1-1 | high | item E is not revision-pinned; base predicate `open=6` unreproducible (`open=5` today) | `c1-base-rerun.txt` |
| D89-C1-2 | high | item E blind to post-dispatch freeze amendment; the round did it (`46a43e94` after `2e700b9a`) and E prints `[]` | `freeze-v2-after-dispatch.txt` |
| D89-C1-3 | high | prose-only closure reaches `open=0 closed=6 met=true` with `scripts/` and `.ufo/` byte-identical to base | `c1-d1-prose-only-mirror-count.txt`, `c1-d1-integrity.txt` |
| D89-C1-4 | med | item B is prose-to-prose and never reads the report it routes | `defect-object-locations.txt` |
| D89-C1-5 | med | item C closes on `retracted` without checking the claim was dropped; the claim is absent from committed bytes | `defect-object-locations.txt` |
| D89-C1-6 | med | item D's recount is mode-inconsistent (1590 git vs 1002 mirror) and never reads the routed object at `LOG.md:3021` | `count-mode-mismatch.txt`, `r88-b-and-d-objects.txt` |
| D89-C1-7 | med | item E auto-closes in `--mirror`, so the sanctioned do-nothing instrument cannot reproduce `open=6` (D0 gives `open=5`) | `c1-d0-ids-only.txt` |
| D89-C1-8 | low | item F is shape-only (column names, one row, any tagged line) | `c1-prose-only` fixture |
| D89-C1-9 | low | the freeze's "no item is scored from prose alone where a behaviour is available" is false for C | `freeze.md:31-33` vs `c89_defect_queue.py:item_c` |
| D89-C1-10 | low | C1 is not separable from C2: E needs `c89_key.py`'s add commit | frozen `controls/base-c1.txt` |
| D89-C2-1 | high | target accepts contract-violating candidates (URI escaping, SP/HTAB trim); the accepted URI mutant collides two distinct requests | `c2-probe.txt` |
| D89-C2-2 | high | committed seed + committed generator + embedded oracle; a 421-entry table reaches `met=true` (R88-1 unfixed) | `c2-probe.txt` |
| D89-C2-3 | med | 100 of 200 properties are `same` relations satisfied by a constant key | `c2-probe.txt`, `base-c2.txt` |
| D89-C2-4 | med | guard weakened after dispatch (`FORBIDDEN` 6→3 tokens, line-level `open(`/`.ufo` bypassable); alias import undetected (disclosed) | `freeze-v2-after-dispatch.txt` |
| D89-C2-5 | low | `c89_key.py:14` says base prints `controls=0/5`; `freeze.md:47` and the receipt say `5/5` | `freeze.md`, `c89_key.py` |
| D89-C2-6 | med | axis misattribution: contract disclaims freshness; this is operability/coverage | `c2-contract.md` `## Scope` |

## 6. Smallest safe corrections

1. **E, revision-pinned:** resolve commits with `git rev-list <rev> -- <path>`;
   require the *last* commit touching any declared freeze path to precede the
   dispatch marker's committer time. Two lines.
2. **E, mirror mode:** do not return `[]`; return a failure ("E unmeasurable in
   mirror mode") so a mirror control cannot report E closed.
3. **D, one count:** make mirror mode use the same predicate as git mode
   (`'/controls/' in str(p.relative_to(root))`), so 1590 == 1590.
4. **C:** require the routed claim's text to be absent at the revision, or
   require `retracted` to name the file and line that no longer carries it.
5. **B:** read the routed object (the report), or delete B and keep A/D/E as the
   behavioural set — four prose items cannot carry a calibration claim.
6. **Base receipt:** record it as "as captured at 18:08, not reproducible after
   dispatch" until (1) lands.
7. **C2, two clauses:** add frozen cases and property classes for `%`/US/RS/GS
   in the **URI** and for `\x0b`/`\x0c` at a **value edge**; both mutants then
   fail. This is the cheap fix.
8. **C2, population:** apply R88-1's fix direction — score a batch frozen after
   the candidate exists, or reveal a population digest at scoring — or stop
   claiming the table shortcut is blocked.
9. **C2, reporting:** print `props_same` and `props_diff` separately so the
   non-discriminating half is visible in every receipt.
10. **Freeze v2:** restore `base-c2.txt` to blob `71a199a8` and append a
    correction entry; never rewrite a filed base receipt. Disclose v2 in
    `freeze.md` with its commit id and the guard delta.

## 7. Commands, limits, tooling

All commands are in the receipt headers. Two modes only: `--root/--revision`
against LANE (read-only git) and `--mirror` against `git archive 76225160`
extracted into scratch. `TMPDIR` was set explicitly to my scratch on every run.

Limits, stated honestly:

- I could not demonstrate D1 end-to-end in **git** mode: that needs a commit,
  and the seat forbids commits. D1 is therefore proven in mirror mode
  (`met=true`), with the mode-independent items (A, B, C, F) identical in both
  modes, D's git recount proven separately by `git ls-tree` (1590), and E proven
  closed at HEAD by the real counter. The git-mode conclusion follows from those
  four facts and is labelled `[INFERENCE]`.
- E's mirror auto-close is a code fact, not a measurement I could vary.
- No network was used; no URL is cited, so no fetch receipt exists.
- Tooling: nothing installed, nothing upgraded. No pacman, no `uv tool`, no
  binary placed in a PATH directory.
- LANE moved during the seat (`2e700b9a` → `f62e7954` → `9784ad54` →
  `21770586` → `a225647f` → `658f72f8`). Each receipt names its revision. The
  C2 `met=true` line is reproduced at `9784ad54` and `a225647f`; the C1
  `open=1` line is at `a225647f`; the live lesson markers are at `658f72f8`.
- Scratch `/fast/scratch/hyaku/kake-r89/CriticClaims/` deleted before yield; no
  `/tmp` or `/fast` path is cited as evidence.

## 8. Receipt index (`w1/CriticClaims/receipts/`)

| file | what it shows |
|---|---|
| `base-c1-as-filed.txt` | the frozen base C1 receipt from `08ab46a1` (`open=6`, E fails: `no commit adds …/c89_key.py`) |
| `base-c2-as-filed.txt` | the frozen base C2 receipt from `08ab46a1` (`controls=5/5`, candidate absent) |
| `c1-base-rerun.txt` | the declared base command re-run today: `open=5`, E `[]` — predicate not reproducible |
| `c1-head.txt` / `c1-final-head.txt` | C1 at `9784ad54` (`open=5`) and `a225647f` (`open=1`, A only) |
| `c1-d0-ids-only.txt` | D0 literal do-nothing control: `open=5` (E auto-closed in mirror mode) |
| `c1-d1-prose-only-mirror-count.txt` | D1 prose-only closure: `open=0 closed=6 met=true`, exit 0 |
| `c1-d1-prose-only-git-count.txt` | same fixture with the git-true marker: D is the only open item (mode mismatch) |
| `c1-d1-integrity.txt` | `scripts/` and `.ufo/` byte-identical to the base mirror; only 3 text files differ |
| `c1-selftest-rerun.txt` / `c2-selftest-rerun.txt` | `12/12` and `43/43`, exit 0 |
| `c2-base-rerun.txt` / `c2-head.txt` / `c2-final-head.txt` | C2 at base (`met=false`), `9784ad54` and `a225647f` (`met=true`) |
| `c2-probe.txt` | the two contract-violating mutants and the 421-entry table, all `met=true`; collision witness; 100/100 split |
| `c2-seed-stability.txt` | both mutants pass at seeds `89089`, `1`, `7`, `424242` |
| `count-mode-mismatch.txt` | git `1590` vs mirror `1002` on one tree |
| `count-mode-explanation.txt` | 1002 depth-2 + 588 nested = 1590 |
| `freeze-v2-after-dispatch.txt` | `46a43e94` after `2e700b9a`; guard 6→3 tokens; frozen base receipt rewritten |
| `defect-object-locations.txt` | where the R88-B/C/D objects actually live; the counter reads none of them |
| `r88-a-authority.txt` | the cited receipt and the tool both print `35/35`; three prose sites say `22/22` |
| `r88-b-and-d-objects.txt` | the round-88 lesson's existing append-only R88-B correction; `LOG.md:3021` unpinned `1,577` |
| `live-c1-closure.txt` | `corpus/lessons/round-89.md` at `658f72f8` carries the four markers my D1 fixture wrote |
