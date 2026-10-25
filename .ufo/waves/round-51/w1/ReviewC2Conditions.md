# Review — C2 (freshness) conditions vs. counter, round 51 wave 1

Scope: the eight contract sentences in `.ufo/waves/round-51/contract.json` (claim `C2`) against the
eight checks in `.ufo/waves/round-51/c51_quote_truth.py`. Measured revision
`9d13768c4fdd0e9a2688d2ecf1616b539cf57658`; do-nothing base `007d66e4e8360a5f88d29a93eeedd8066dad4434`.
Read-only; scratch under `/tmp/c2atk`. No tool installs were needed.

## What the counter actually prints

```
$ python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)
  C1_entries_exist pass
  C2_entry_cites_id pass
  C3_row_shape pass
  C4_used_by pass
  C5_gate_quote_truth pass
  C6_receipt_pins pass
  C7_validate_before_append pass
  C8_append_after_mirror pass
  revision: 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
EXIT=0
```

At the base revision the same command prints (tail):
`C8_append_after_mirror FAIL` / `- no commit adds the pre-append mirror`, with `C2 quote-truth 0/8
met=False` and exit 1.

The predicate reads 8/8 at the tip and 0/8 at the base: the do-nothing control holds. The
findings below are therefore about *what the 8/8 is allowed to mean*, not about a failed run.

## One-to-one match

| Contract sentence | Code check | Verdict |
|---|---|---|
| C1 both admitted entries exist at their repo-relative paths | `C1_entries_exist` (:143-150) | faithful; also accepts a 0-byte entry (only `git show` failure counts as absent) |
| C2 each entry cites its own row id below its 8-line metadata header | `C2_entry_cites_id` (:152-158) | faithful |
| C3 each row has 11 cells, no literal or escaped pipe, status `mined`, the round's opened date, a normalized recheck | `C3_row_shape` (:164-178) | cells / escaped pipe / status faithful; literal pipe only caught collaterally by the cell count; opened date unanchored (F6); recheck grammar narrower than the census (F5) |
| C4 each row's used-by lists exactly the admitted entry that cites it | `C4_used_by` (:180-189) | faithful |
| C5 each Gate quote is 6-25 words and an exact raw substring of the retained body | `C5_gate_quote_truth` (:191-220) | word count and substring faithful in effect; the *identity* of "the Gate quote" and an undeclared UTF-8 gate are code-only rules (F7) |
| C6 each body's sha256 equals its receipt's and its receipt URL is the row's URL | `C6_receipt_pins` (:222-244) | sha half faithful; URL half is substring containment and is silently skippable (F3) — falsified live |
| C7 the pre-append census receipt names `--file` and the mirror path and not `--root`, exit 0, no E03/E04 in stdout | `C7_validate_before_append` (:246-263) | implemented exactly as worded, but the receipt carries no content binding, so "pre-append" is not evidenced (F2, F8) |
| C8 the mirror commit is a **strict** ancestor of the measured revision, **the mirror's registry carries none of the adopted ids**, the measured registry carries all of them | `C8_append_after_mirror` (:265-288) | the second clause is implemented against `corpus/SOURCES.md` at the mirror commit, not the mirror's own registry table; on the committed bytes the mirror's registry **does** carry both ids (F1) — falsified live; "strict" is implemented non-strict (F4) |

Code checks the contract does not declare:

- `:214` the retained body must decode as UTF-8 before the substring test (an undeclared precondition
  that can fail C5 on a body whose quote bytes are present).
- `:116` the Gate quote is specifically the **last** double-quoted run on the first `- SID ` line under
  `## Gate`.
- `:172-174` the recheck whitelist `(\d{4}-\d{2}-\d{2}|\d+d|on-release)` — narrower than the census's
  accepted `symbolic` cadence (see F5).
- `:273` `mirror_commits[-1]` — the **oldest** commit that adds the mirror path is the one judged.
- `:241` `if row and len(row) >= 2` — the C6 URL clause silently disappears for a short/absent row.
- `:254,258` `--file` and the mirror path are matched as raw substrings of `argv`, not as argv tokens.

## Findings

### F1 — Blocker: C8's "the mirror's registry carries none of the adopted ids" is false on the committed bytes

Contract: *"the mirror's registry carries none of the adopted ids"*. Code (`:277-285`) reads
`show(root, mirror_commit, REGISTRY)` — `corpus/SOURCES.md` **at** the mirror-add commit — and never
opens the mirror file itself.

The mirror file `.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md`:

- at `19a99bd` (the commit that adds it) parses to **145** rows including `S262` and `S263` as complete
  11-cell rows, and is **byte-identical at HEAD** (sha256 `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3`);
- while `corpus/SOURCES.md` at `19a99bd` parses to **143** rows and carries neither id.

Applying the counter's own `parse_registry` to the mirror file gives
`{'S262': True, 'S263': True}` and the two notes `S262: the mirror already carries the row`,
`S263: the mirror already carries the row` — i.e. **7/8, met=False**, under the natural reading of
"the mirror's registry". C8 passes only because it substitutes a different object (the registry at the
mirror commit) for the object the contract names.

### F2 — Blocker: the "pre-append mirror" is a snapshot of the post-append worktree; C7's census therefore validates post-append bytes

`git log --diff-filter=A -- corpus/knowledge/canonical-selection.md corpus/knowledge/crawler-identity.md`
→ the entries are first committed at `5591557` ("append S262 and S263 **after** the pre-append mirror
and land the two entries"). Yet the mirror at `19a99bd` already contains
`.ufo/waves/round-51/assimilation/pre-append/corpus/knowledge/canonical-selection.md` with sha256
`280b7f95989201a37d9fc98679dcab8dc5ea450607e5d2011232416e91c3c729`, identical to HEAD's entry, while
`19a99bd:corpus/knowledge/canonical-selection.md` does not exist. The mirror is a 139-file copy of the
uncommitted post-append tree, committed one commit early under a message that asserts the opposite order.

Consequence: `census-argv.txt` targets that mirror path and `census-stdout.txt` (1054 bytes: twelve `W04`
lines plus one `ok` line) records a clean validation of a registry that already contained both rows.
`census-stderr.txt` is 0 bytes. The receipt carries **no content hash**, so C7 cannot bind the
validation to any particular bytes — it is equally consistent with a census of the pre-append working
tree and with a census of the post-append file that was committed. Either way it does not evidence
"validated before the append", which is the assurance the claim's *after* text asserts
("the mirror census-validated with `--file` before the append"). All five of C7's sub-clauses are
implemented exactly as the contract words them; the defect is in the evidence chain, and no condition
in the set can detect it.

### F3 — Medium: C6's URL clause is substring containment; falsified live in 8/8

`:242` reads `if receipt.get("url") not in row[1]`. In a `/tmp` repo using the lane as a git alternate
(no write touches the lane), I replaced the `S262` receipt URL with the bare prefix
`https://developers.google.com/search/docs` — not the row's URL — and committed it as `b307bbe`:

```
$ python3 -B .ufo/waves/round-51/c51_quote_truth.py --root /tmp/c2atk --revision b307bbe36d27b56742204e64ca74d5e441200d10
C2 quote-truth 8/8 met=True   EXIT=0
```

Any prefix of the cell, and in principle any short common substring, satisfies the contract sentence
"its receipt URL is the registry row's URL". `:241` additionally drops the clause entirely when the row
has fewer than two cells, so the condition's second half can be vacuously true.

The falsification does not depend on the scratch repository surviving: set `sources.S262.url` in
`.ufo/waves/round-51/sources/receipts.json` to any prefix of the row's URL, write that file as a blob
over the measured tree, and rerun the counter at the resulting commit — it prints 8/8. The mutation
fixture lives in `/tmp/c2atk`, a throwaway repo whose object store alternates onto the lane; commit
`b307bbe…` exists only there. The recipe above is the whole fixture, so losing `/tmp` costs nothing.

### F4 — Low: "strict ancestor" is implemented non-strict

`:274` uses `git merge-base --is-ancestor`, which exits 0 when `mirror_commit == rev`. The contract says
"strict ancestor". No live violation: `19a99bd ≠ rev`. The sibling clause incidentally blocks the
trivial same-commit construction, because a commit that adds the mirror and the rows would present a
registry-at-commit that already carries the ids. Formal mismatch, not a live falsification.

### F5 — Medium: C3's recheck grammar is narrower than the census the round cites

`:172-174` accepts only an ISO date, `\d+d`, or the literal `on-release`. The fleet census accepts any
`symbolic` cadence `/^[A-Za-z][A-Za-z0-9 _-]*$/` (`scripts/sources-census.sh:582,665`; its own selftest
uses `annual` at :149). A registry row the census validates clean would fail C3. The contract says only
"a normalized recheck"; the whitelist is a code-only narrowing. The live rows use `180d`, so this does
not affect the current 8/8.

### F6 — Medium: "the round's opened date" is a code constant, not derived

`ROUND_DATE = "2026-10-24"` (`:46`) is compared against `row[8]` (`:170`). The row text, the entry front
matter (`verified-at: 2026-10-24`), the lesson prose and `receipts.json`'s `fetchedAt`
(`2026-10-24T23:16:49-03:00`) were all authored in this round by the same hand, so their agreement is
not independent corroboration: the check cannot distinguish a correct opened date from an incorrect one
whenever the constant and the row are wrong together. Nothing in the committed bytes anchors the round's
open date except LOG.md prose written this round.

### F7 — Low: C5's quote identity and UTF-8 gate

`:116` takes `quotes[-1]`, so the "Gate quote" is defined as the last `"…"` run on the first `- SID `
line under `## Gate`; a second quoted phrase later on that line would silently become the subject. `:214`
rejects a body that does not decode as UTF-8 before the substring test, an undeclared precondition.
`:218` compares decoded strings, which for well-formed UTF-8 is equivalent to byte containment, so
"raw" is preserved in practice. No live defect: both quotes are byte substrings with exactly one
occurrence each, and are also substrings after whitespace collapse.

### F8 — Low: C7's five tests bind to strings, not tokens

`:254` `"--file" not in argv` is satisfied by `--files`; `:258` `MIRROR not in argv` is satisfied by any
path ending in the repo-relative mirror path (measured: `MIRROR in "/tmp/elsewhere/"+MIRROR` is `True`),
and the live receipt records an absolute host path,
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/.../pre-append/corpus/SOURCES.md`; `:256` `"--root" in argv`
is a substring test that would also trip on a path containing `--root`. `:260` `exit_text.strip() != "0"`
and the E03/E04 stdout scan are faithful.

### F9 — Low: C1 accepts a zero-byte entry

`show` returns `""` (not `None`) for an empty file, so a 0-byte entry passes C1. C2 then fails on the
missing id, so the loss is contained.

## What does hold, measured

- Base control: `007d66e` → `0/8 met=False`, exit 1. The counter reads committed bytes only
  (`git show` / `git log`), opens no worktree file, makes no network call, and touches none of C1's
  inputs: separability as declared.
- Retained bodies are genuine and self-consistent: `S262.html` 174926 B sha256 `79222433…d50d23b`,
  `S263.html` 175561 B sha256 `6afbdc82…a4e155de` — both equal `receipts.json`'s `sha256` and `bytes`;
  both are UTF-8 and both carry their declared doc revision literally (`Last updated 2026-08-20 UTC`,
  `Last updated 2026-02-03 UTC`). That last fact is a corroboration the counter does not use.
- Gate quotes: 10 and 9 words, byte-exact single occurrences in their bodies.
- Registry rows: 11 cells, `mined`, opened `2026-10-24`, recheck `180d`, `used-by` exactly the citing
  entry, URL a substring of the source cell.

## Residual risk and verification gaps (freshness)

1. The "re-grounded this round" half of the claim has **no independent time anchor**. `fetchedAt`,
   the lesson's "accessed 2026-10-24", the entry's `fetched 2026-10-24` and LOG.md's prose are all
   self-reported in the same round; the retained bodies carry no HTTP `Date`, `ETag` or
   `Last-Modified`, and no third-party timestamp. A byte-identical retained body is equally consistent
   with a re-fetch yesterday and with a copy taken months ago. The only freshness fact the bytes do
   prove is the documents' own revision dates (2026-08-20, 2026-02-03), which is *weaker* than
   "re-grounded this round" but is the fact worth claiming.
2. `receipts.json` declares `bytes`/`declaredBytes`; the counter never compares them to `len(body)`.
   They agree today (174926/175561), so this is a missing redundancy, not a live defect.
3. C8's `--diff-filter=A` + `[-1]` picks the oldest add; had the mirror been deleted and re-added, the
   counter would judge the original commit.

## In-flight repair observed in the worktree (not authored by this seat, uncommitted)

While reviewing I found the lane worktree already carrying an attempt-2 repair by another wave-1 seat
(`.ufo/waves/round-51/assimilation/pre-append/census-correction.txt`, which credits `ExecRegistryDiff`
with the same F1/F2 finding). None of it is committed; the measured revision `9d13768` is unchanged,
so everything above describes the bytes the counter actually scored. Four observations matter:

1. The repaired mirror is correct: `corpus/SOURCES.md` in `pre-append/` is now sha256
   `cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117`, 143 rows, neither adopted id —
   the correction document's claim checks out.
2. **The repair as first observed would break C7.** `census-exit.txt` then read the literal string
   `exit=0`, and `c51_quote_truth.py:260` requires `exit_text.strip() != "0"` to be false. Measured at
   the time: `stripped='exit=0' -> C7 note fires: True`. Committing that shape would flip C7 to FAIL
   unless the counter were also changed — a rule change, contradicting the correction document's own
   statement that "the C7 check's rules … are unchanged". Currently both exit receipts are bare `0\n`
   (2 bytes each, `od -c` on `census-exit.txt` and `census-count-exit.txt`), so the C7 shape hazard is
   cleared in the worktree — including for a C7 extension that read the count receipt. The hazard was
   real when observed, but it is not live.
3. The re-run receipt is **byte-identical to the superseded receipt** (`census-stdout.txt` 1054 B and
   `census-argv.txt` both `cmp`-equal to `superseded/`). That is consistent with a genuine re-run — the
   two extra rows carried unique URLs, so they added no `W04`/`E` line and the `ok` line is the path —
   but it also demonstrates that the census output has **zero discriminating power** over the append:
   pre-append and post-append registries produce the same receipt. Rewriting the mirror's content does
   not fix F2/C7; only binding the receipt to a hash of the validated bytes does. A newer uncommitted
   `census-count-*` receipt is a genuine discriminator where the validate stdout is not: it reports
   `rows 143`, `tier.A 120`, `tier.B 6`, `tier.C 17` (a contaminated mirror would read 145). It is the
   better pin — but still a content assertion at an unknown time, not an ordering proof.
4. Because the current C8 never reads the mirror file, **no repair to the mirror's content can change
   its verdict**. The correction document's "C8 … scored exactly as declared before and after the
   repair" is true precisely because C8 ignores its subject. Even a corrected C8 that read `MIRROR` at
   the measured revision would not make this repair honest — see addendum item 3.

## Cross-check with ExecRegistryDiff (addendum)

ExecRegistryDiff (read-only registry-diff seat) reviewed F1-F3 over IRC and confirmed both C7 points and
the byte-identical receipts. Attribution corrected there and here: the attempt-2 repair was made by an
**unidentified** wave-1 seat; ExecRegistryDiff wrote only `w1/ExecRegistryDiff.md`, which scores C8 as
**FAIL**, not "as declared". F1 above was derived independently by applying `parse_registry` to the
mirror blob here; the agreement is convergence, not borrowed evidence.

Six measured refinements:

1. Blob identity. The contaminated mirror is git blob
   `9e2a22175ef95a23252b349d8743cf0e5b5480fc` at **both** `19a99bd` and `9d13768` (sha256 `4ea81a5a…`);
   `git rev-parse` returns the same object at both revisions, so the mirror file never changed before
   the repair.
2. A content pin alone does not establish order. Pinning `cd9ee4cf…` is truthful *now* because that is
   exactly `sha256(git show 19a99bd:corpus/SOURCES.md)` — verified byte-identical (143 rows) — but a
   post-hoc rewrite satisfies any content pin. A pin binds *which bytes were validated*, never that
   they predate the append.
3. **My earlier "repairable formulation" was weaker and is withdrawn.** I had proposed requiring
   `MIRROR` at the measured revision to equal `REGISTRY` at the mirror-add commit. ExecRegistryDiff
   showed this is satisfied by a post-hoc copy, and the repair in this worktree *is* that copy:
   measured, `cmp` PASSES on the repaired worktree while `MIRROR@19a99bd` is still the contaminated
   blob. That check therefore measures "the mirror now equals the pre-append bytes", not "it did
   before the append" — it would launder the defect rather than fix it. The form that binds both
   operands to one immutable commit:

       MIRROR@mirror_add == REGISTRY@mirror_add            (blob ids, same commit)
       and mirror_add is a STRICT ancestor of the commit that first adds the adopted rows

   Measured: `MIRROR@19a99bd` = `9e2a22175ef95a23252b349d8743cf0e5b5480fc` versus
   `REGISTRY@19a99bd` = `cd448eaf06bbccefbd2e672be03355c79dd6d851` → **FAIL**. The ancestry half holds
   (`19a99bd` is a strict ancestor of `5591557`, the row-adding commit). No post-hoc copy can satisfy
   it, because commits are immutable. Equality and ancestry are conjuncts (b) and (a) below; the third
   conjunct is what makes `[0]` safe.
4. Selection is latent, not active. `git log` is newest-first, so `mirror_commits[-1]` is the **oldest**
   add. The MIRROR path has exactly one add event today (`git log --diff-filter=DA` → `19a99bd` only;
   the in-flight repair is a worktree modification, not an add), so `[-1] == [0]` and the bug does not
   bite at `9d13768`. It starts misjudging after any delete+re-add re-landing, so the selection must
   become `[0]`.
5. Equality alone is **not** sufficient — the fix is a three-part conjunction. A delete+re-add at HEAD
   would give `MIRROR@add == REGISTRY@add` at 145 rows, both carrying the ids: equality passes and
   proves nothing. The binding form:

       (a) the selected add commit is a strict ancestor of the commit that ADDS the adopted rows;
       (b) MIRROR@add == REGISTRY@add            (snapshot identity, blob ids);
       (c) MIRROR@add carries none of the adopted ids.

   (a)+(b) defeats the post-hoc copy; (c) defeats a post-append delete+re-add even when the append
   commit is re-identified by a later landing. Measured on today's history: **(a) holds** (`19a99bd`
   strictly precedes `5591557`), **(b) fails** (`9e2a221…` vs `cd448eaf…`), **(c) fails** (both rows
   present, 145 rows). So the committed 8/8 rests on an assertion false under (b) and (c), and true
   only under (a).
6. Reachability, by construction (not measured): no history rewrite is needed — the mirror must be
   re-added while the registry is still at 143 rows, followed by a separate append. That is a
   re-landing of the wave, not a patch on top of `5591557`, whose registry already carries 145 rows.
   Any copy taken after the append, including the repair now in the worktree, cannot reach it.

## Verdict

C2's predicate prints 8/8 at `9d13768`, but that number does not survive the contract's own wording.
**C8's mirror clause is false** on the committed bytes — the mirror's registry carries both adopted ids
(blob `9e2a2217…` at `19a99bd`, where the registry is `cd448eaf…`) — so the honest score is **7/8,
met=False**. **C7's "pre-append" premise is unevidenced** rather than false: all five of its sub-clauses
pass as worded, but the census receipt cannot bind to content and the bytes it names already contained
the appended rows, so it certifies nothing about the pre-append state. C6's URL clause is additionally
falsifiable at 8/8. Recommendation: C2 is **not** honestly met as declared. Minimum fix
before any re-score: (1) C8 must become the three-part conjunction — (a) the selected add commit is a
strict ancestor of the commit that adds S262/S263, (b) `MIRROR@add == REGISTRY@add` as blob ids at that
one commit, (c) `MIRROR@add` carries neither adopted id — with the newest add selected rather than the
oldest; measured at `9d13768`: (a) holds, (b) fails (`9e2a22175ef9…` vs `cd448eaf06bb…`), (c) fails
(both rows present). Equality alone is not enough: a delete+re-add after the append satisfies it, and
reading the mirror at the measured revision instead is satisfied by exactly the post-hoc copy in the
worktree. `[-1]` is latent today (one add event) but must still become `[0]`;
(2) the mirror must be a genuine pre-append copy (the worktree repair already produces
`cd9ee4cf…`, 143 rows, but as a copy taken after the append it cannot satisfy (1));
(3) the census receipt must pin a sha256 — or better, the `rows 143` count — of the bytes it validated,
since its validate stdout is byte-identical across the pre- and post-append registries, and the pin must
be read together with (1), because a post-hoc rewrite satisfies any content pin; (4) `census-exit.txt`
must carry the bare `0`, not `exit=0`, or C7 fails at the repaired revision; (5) C6's URL test must be
equality against the row's URL field rather than substring containment.

The honest consequence: on the committed bytes C2 scores **7/8, met=False**, and no artifact written at
the measured revision can change that — only a fresh landing that commits the mirror while the registry
still lacks the rows, followed by a separate append, makes C8 true.

Nothing here disputes the two entries themselves: the retained bodies, their sha256 pins, their doc
revisions and both Gate quotes verify byte-exactly. The defect is in the *pre-append mirror* evidence
chain, which is the only part of C2's eight conditions that cannot be re-derived from the entries.
