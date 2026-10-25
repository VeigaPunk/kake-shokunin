# Residual C2 rerun — round 51, wave 2

- Seat: `L1Kake51.ResidualC2Rerun` (reviewer)
- Measured revision: `907790c78008819fc95c988431188f90b81f0d5f`
- Base revision: `007d66e4e8360a5f88d29a93eeedd8066dad4434`
- Root: `/home/vgpnk/Projects/shokunin/kake-shokunin`
- Instrument: `.ufo/waves/round-51/c51_quote_truth.py`, sha256
  `29a899a0345d36b457e8381e0f611b00cda920f741d3e52cbf3ba88df156f99f` — byte-identical to
  the copy committed at the measured revision, so both runs used the committed instrument.

## 1. Counter reruns — exit codes and condition states, verbatim

```
python3 -B .ufo/waves/round-51/c51_quote_truth.py --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 007d66e4e8360a5f88d29a93eeedd8066dad4434
→ C2 quote-truth 0/8 met=False  (met: conditions_passed == 8 of 8)      exit=1
  C1_entries_exist FAIL   C2_entry_cites_id FAIL   C3_row_shape FAIL   C4_used_by FAIL
  C5_gate_quote_truth FAIL   C6_receipt_pins FAIL
  C7_validate_before_append FAIL   ("pre-append census receipt is incomplete")
  C8_append_after_mirror FAIL      ("no commit adds the pre-append mirror")

python3 -B .ufo/waves/round-51/c51_quote_truth.py --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 907790c78008819fc95c988431188f90b81f0d5f
→ C2 quote-truth 8/8 met=True   (met: conditions_passed == 8 of 8)      exit=0
  C1_entries_exist pass   C2_entry_cites_id pass   C3_row_shape pass   C4_used_by pass
  C5_gate_quote_truth pass   C6_receipt_pins pass
  C7_validate_before_append pass   C8_append_after_mirror pass
```

Both frozen numbers reproduce. The 8/8 is not produced by the test C8 claims to perform —
see F1 — but the underlying condition does hold when read at the measured revision; see the
verdict in §4.

## 2. Hand verification against committed bytes — condition C6 (receipt pins)

Chosen because it is the only condition binding retained body bytes, receipt JSON and the
registry row together, and it is independent of the counter's `parse_registry`.

```
for S in S262 S263; do git show 907790c:.../sources/$S.html | sha256sum; done
  S262  792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b
  S263  6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de

git show 907790c:.../sources/receipts.json   (keys under "sources")
  S262 sha256=79222433…d23b  bytes=174926  declaredBytes=174926  httpStatus=200
  S263 sha256=6afbdc82…55de  bytes=175561  declaredBytes=175561  httpStatus=200

git cat-file -s 907790c:.../sources/S262.html → 174926    (== receipt bytes/declaredBytes)
git cat-file -s 907790c:.../sources/S263.html → 175561    (== receipt bytes/declaredBytes)

git show 907790c:corpus/SOURCES.md | grep -E '^ {0,3}\| ?S26[23] '
  both rows 11 cells; used-by = corpus/knowledge/canonical-selection.md /
  corpus/knowledge/crawler-identity.md; receipt URL is the URL in cell 1
  (url_is_suffix_of_cell1=True for both).
```

**C6: PASS, hand-verified.** Body sha256, blob size and declared size agree for both sources;
the receipt URL is the registry row's URL. Slack only in F5.

Supplementary (cheap, adjacent): both Gate quotes are exact raw substrings — S262
`"indicating a canonical preference is a hint, not a rule"` (10 words), S263
`"Googlebot is the generic name for two types of"` (9 words), each whitespace-exact inside its
retained body.

## 3. Mirror provenance — the fact that decides F1/F2

```
for R in 007d66e 19a99bd 5591557 9d13768 907790c; do
  git show $R:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | sha256sum; done
  007d66e  (absent)
  19a99bd  4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3   145 rows, both adopted ids
  5591557  4ea81a5a…                                                        (unchanged)
  9d13768  4ea81a5a…                                                        (unchanged)
  907790c  cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117   143 rows, no adopted ids
git show 007d66e:corpus/SOURCES.md | sha256sum  → cd9ee4cf951f9708…92189117  (identical)
git log --diff-filter=A --format=%H 907790c -- <MIRROR>  → 19a99bd  (only add; 907790c modifies)
```

So the artefact named "pre-append" was **contaminated when committed** and was **repaired in
the measured commit itself** (`907790c`, "…and the mirror repair"), after the append landed in
`5591557`. The shipped bytes at the measured revision are correct: `cd9ee4cf` equals the base
registry byte for byte, 143 rows, neither adopted id. The round's own
`assimilation/pre-append/census-correction.txt` and the lesson's "Mistakes (attempt 2)" entry
record this contamination, its discovery by seat `ExecRegistryDiff`, and the rebuild steps —
my readings agree with those documents.

## 4. Findings by severity

### F1 — HIGH: C8 reads `REGISTRY`, not `MIRROR`; no condition reads mirror bytes at all

```python
mirror_registry = show(root, mirror_commit, REGISTRY)   # REGISTRY == "corpus/SOURCES.md"
```

`MIRROR` is defined and used elsewhere in the same file, so the wrong constant is unambiguous.
At the measured revision the line evaluates `corpus/SOURCES.md` at `mirror_commit` = `19a99bd`,
a registry that trivially lacks the rows: the append had not landed. Measured directly with the
counter's own parser, `parse_registry(git show 19a99bd:<MIRROR>)` returns 145 rows with
`S262 in mirror=True, S263 in mirror=True`.

The result is that `C8_append_after_mirror pass` says nothing about the mirror. Grepping the
instrument, `MIRROR` occurs in C7 only as a substring test on `census-argv.txt`; **no condition
in the counter ever hashes or parses the mirror's bytes.** A round that shipped the
contaminated `4ea81a5a` blob would print exactly the same `8/8`. The pass coincides with the
truth instead of establishing it.

### F2 — HIGH, new: the round's recorded repair is unsatisfiable as written

The lesson routes the counter-side fix as "C8 must read `MIRROR` at the mirror commit"
(`corpus/lessons/round-51.md`, Mistakes (attempt 2), last line). Applied literally, that fix
**fails**, because git history is immutable and `19a99bd:<MIRROR>` still holds the contaminated
blob. Two probes on `/tmp` copies (one line changed each, repo untouched):

```
probe A  mirror_registry = show(root, mirror_commit, MIRROR)
→ C2 quote-truth 7/8 met=False   C8_append_after_mirror FAIL
    - S262: the mirror already carries the row
    - S263: the mirror already carries the row            exit=1

probe B  mirror_registry = show(root, rev, MIRROR)
→ C2 quote-truth 8/8 met=True    all eight pass           exit=0
```

Only probe B works, and only because the repair rewrote the file at `907790c`; under probe B
the mirror path is read at the measured revision, where the file no longer is what the "mirror
commit" produced. The recorded repair instruction must be restated as "read `MIRROR` at the
measured revision, and pin the mirror's sha256 in the census receipt" — otherwise round 52
implements a fix that turns this claim red for a reason unrelated to the data.

### F3 — MEDIUM: the condition's truth depends on which revision "the mirror's registry" means

C8 says "the mirror's registry carries none of the adopted ids". Read at the measured revision
→ true (`cd9ee4cf`, 143 rows, zero adopted ids). Read at the adding commit → false (`4ea81a5a`,
both ids). The repair is what made those two readings disagree, and the condition text does not
name a revision. Today the claim's truth is only defensible under the measured-revision reading.

### F4 — MEDIUM: the "validated before the append" ordering never happened this round

The append landed at `5591557`; the mirror that now ships as "pre-append" was reconstructed at
`907790c`, one commit later, by `git show 19a99bd:corpus/SOURCES.md > <MIRROR>`. Attempt 1's
validate receipt was produced against post-append bytes; attempt 2's validate was re-run after
the append. So no committed receipt evidences a census of bytes lacking the rows taken before
the append — the only receipts whose subject is the 143-row file were produced at `907790c`. C2's
`after` prose — "the mirror census-validated with `--file` before the append" — is therefore
false as provenance, while C7's condition text (argv names `--file` and the mirror path and not
`--root`; exit 0; no `E03`/`E04`) does not test ordering and passes. This is a prose-vs-condition
gap that the correction document acknowledges in substance ("evidence repair, not a rule
change") but that the claim text still overstates. The strongest honest wording is "the mirror
is byte-identical to the pre-append registry and was census-validated after the append".

### F5 — MEDIUM: C7's validate receipt is byte-identical to the superseded receipt

```
census-argv.txt IDENTICAL   census-exit.txt IDENTICAL
census-stdout.txt IDENTICAL census-stderr.txt IDENTICAL
```

`superseded/` holds attempt 1's receipts against the 145-row contaminated blob and every field
matches the "corrected" run, so the validate receipt cannot discriminate 143 rows from 145.
`census-count-stdout.txt` (`file rows 143`) is the only receipt whose output binds the repaired
bytes, and C7 does not read it. The correction document says as much ("`validate` alone cannot
tell a 143-row registry from a 145-row one"). Consequence: C7's four clauses are satisfied by
bytes that equally describe the wrong file.

### F6 — LOW: C6's URL comparison is containment, not equality

`if receipt.get("url") not in row[1]` accepts any prefix/shortened URL. Actual values are
suffix-equal but not cell-equal (`url_exact_equal=False`, `url_is_suffix=True`), because cell 1
is `"<title> — <url>"`; strict equality would never pass under this row format. No false pass
today, but a truncated receipt URL would pass.

### F7 — LOW: C8 selects the oldest commit that added the mirror

`mirror_commits[-1]` over newest-first `git log --diff-filter=A` picks the first-ever add. Any
later re-add is ignored and the stale snapshot is read. Inert today (one add, `19a99bd`).

### Verdict on C2

The printed predicate `conditions_passed == 8 of 8` reproduces at both revisions (exit 0 /
exit 1) and C2's substantive conditions hold at the measured revision — C1–C7 pass on their own
terms (C6 additionally hand-verified in §2), and C8 true under the measured-revision reading of
"the mirror's registry"
(`cd9ee4cf` = base registry; strict-ancestor mirror commit; both rows present at the measured
revision). C2 is **not** a false met on the data. It is a met whose certifying clause is not
evaluated by the instrument, plus an `after` sentence whose "before the append" ordering is
not evidenced. No kill-rule miss is available; the defect is in the evidence, not the answer.

## 5. Residual risk and verification gaps

- The contract is unchanged between declaration (`19a99bd`) and the measured revision
  (`git diff … -- .ufo/waves/round-51/contract.json` empty). The instrument changed once, at
  `9d13768`, confined to the receipts `{"sources": …}` unwrapping in C6 — not C8/C7.
- Both `contract.json` and `c51_quote_truth.py` are absent at the base revision (`git show`
  returns nothing); the base rerun remains valid because the counter reads only `git show`
  revision bytes, but the base cannot pin the instrument.
- Not run: mutation probes against a synthetic repo for C7/C8; re-derivation of the 145-row
  and 143-row counts with `scripts/sources-census.sh` (campaign tooling is out of bounds, and
  `census-count-stdout.txt` was read as committed evidence); any check of C1's inputs
  (settlement, route map, timing — sibling seat `L1Kake51.ResidualC1Rerun`).
- The lane working tree already carried sibling modifications
  (`.ufo/waves/round-51/w1/*.md`, 5 files) before this seat ran. My writes are limited to this
  report and `/tmp/c51_c2_pathprobe.py` / `/tmp/c51_c2_probe_rev.py`. No `git add/commit/
  checkout/reset/push`, no `jj` command, no repo file mutated.
- No tools were installed or updated for this seat.

## 6. Recommendation

1. Restate the round-52 repair as `show(root, rev, MIRROR)` **and** a mirror-sha256 pin in the
   census receipt; the currently recorded "read `MIRROR` at the mirror commit" yields 7/8
   against this round's immutable history.
2. Add one condition (or extend C7) that hashes the mirror and compares it to the registry at
   the revision the claim means; without it, an identical `8/8` is reachable with a
   contaminated mirror.
3. Soften C2's `after` prose on ordering: the mirror is a post-append reconstruction that is
   byte-identical to the pre-append registry, not a snapshot validated before the append.
