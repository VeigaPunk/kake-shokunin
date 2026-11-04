# CriticC — round 77, wave w1 (kake)

Seat: `CriticC` (leaf; no subagents). Base `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`. Lane HEAD at open
`bc2e5fb9` (the contract commit). Read before measuring: `contract.md`, `amendment-1.md` (22:44), `amendment-2.md`
(22:44), `AXES.md`, `SCORECARD.md`, `SHONEN.md`, the base blobs of `scripts/sitemap_audit.py` and its selftest,
and the in-wave artifacts below. No model named. Scratch `/fast/scratch/hyaku/kake-r77/CriticC` (`TMPDIR` and
every `--work` inside it) was removed at seat close; this file is the only lane write.

**Snapshot warning (honesty).** The wave is live: the two counters, the cases, the consts and the tool are
untracked and were still being written while I read them. Every in-wave measurement is pinned to the hash and
mtime stated beside it; the artifacts' hashes were:

| artifact | sha256 (final snapshot 22:50) | note |
|---|---|---|
| `.ufo/waves/round-77/c77_shonen_ledger.py` | `a9eef8bd278bfe436b1862d23882adb605b013251d53e898002f89733ebf047c` | 22:48, unchanged since |
| `.ufo/waves/round-77/c77_sitemap_matrix.py` | `5c6eacba266068845144ba59c8e7099cc22fee10ca95c0ab78019ba33d21afce` | cf6f8354 (22:45) → 7d2557b2 (22:48) → 5c6eacba (22:49) |
| `cases/g02, g03/expect.json` | — | corrected 22:49:45 to A5/A6 ids |
| `scripts/sitemap_audit.py` (worktree, uncommitted) | `16ea784f…`; `git diff --stat` = 251 added lines | mtime 22:47:32 |

Both counters and two case expectations changed under me between 22:45 and 22:50, and the changes matter for
C2 (§2.2). Findings are stated against the final hash; where an earlier hash behaved differently it is named.

Nothing below judges the landed after-state. It judges the premises, as the seat asks, plus the after-state as
far as it already exists.

---

## 0. Verdicts at a glance

| # | Question | Verdict |
|---|---|---|
| 1 | C1: calibration move or documentation reorganisation? | Calibration **in kind** (it is AXES' own signal); a *move* only if some box is `evidenced`. `met` does not require one, so the frozen target is a shape. |
| 2 | C2: after-state reachable in one round? | **Not yet, but close**: 18/20 at 22:50. The two red cases are the tool's stale ids after the cases were corrected at 22:49 to the amendment's codes. Two renames close it. An intermediate 20/20 at 22:48 was greened by a counter relaxation, since closed. |
| 3 | C2: 20 cases enough to separate the three families from r39? | Enough for the **coarse families** (r39/base fails 18/20). Not enough for family correctness: five named holes, no hold-out, no parsed-value comparison. |
| 4 | Axis naming | Both claims are on their declared axes. The risk is axis *laundering* (instrument verdict reported as a calibration move; capability reported as coverage), not mis-assignment. |
| 5 | Do-nothing control | C1: an all-gap ledger greens and the kill rule does not exclude it. C2: the 22:48 counter-edit green was real and was closed by the 22:49 case correction; post-correction the cheapest green is a two-line tool rename (a legitimate fix). Fixture-fitting remains unexcluded. |

---

## 1. C1 — calibration, or documentation reorganisation?

### 1.1 The axis sentence and the two strongest cases

AXES.md:15: calibration = *"Self-assessment quality: gaps named honestly, confidence graded, overreach caught"*;
signal *"SHONEN.md/SCORECARD entries match observed repo state."* C1 makes exactly that signal machine-checked,
so the axis assignment is correct. `git log --oneline -- SHONEN.md` is one commit (`11261443 seed: kake shonen`),
and all four boxes are `[ ]` at base (`SHONEN.md:5-8`).

- **Strongest case that the lane learns nothing it did not know.** If the ledger lands all four boxes as
  `gap`, every truth value in `SHONEN.md` is unchanged: the four `[ ]` markers stay `[ ]`, and the round's only
  new object is a JSON file of reasons. The lane already knew none were ticked. That is a documentation
  reorganisation with a derivation attached, not a correction of a false self-assessment.
- **Strongest case that it does learn.** Two ways. (i) **Underclaim correction**: if any frozen check passes at
  base, the `[ ]` was an underclaim and the counter now forces the marker up (`marker-understated`,
  `c77_shonen_ledger.py:680-683`); an underclaim is as much a calibration error as an overclaim. (ii) **A real
  broken pointer**: amendment 1 A12 freezes box 2's check on `LOG.md`'s named receipts and names
  `.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt` as absent at base. I verified it:
  `LOG.md:1811` names that path and `git cat-file -e a2cc5f51:.ufo/…/offline-sweep-r46-verdict-time.txt` exits
  128; `LOG.md:787` shows the end-to-end task evidence the box is about. That dead pointer is a fact about the
  lane's own record that was not known — calibration, not bookkeeping. If box 2 is the only gap, the round's
  learning is exactly that one fact.

So the honest verdict is conditional: **`evidenced >= 1` → calibration finding; `evidenced = 0` → grounded
gap documentation.** The report must say which one it got, and the contract's target line (`contract.md:58-60`)
deliberately allows the second ("gaps named with their flip conditions rather than ticked").

### 1.2 `met` is a shape — counterexample from the counter's own clean fixture

Contract predicate (`contract.md:32`): `met <=> boxes == 4 and unexamined == 0 and mismatches == 0`. There is no
`evidenced` term. I replayed the frozen definitions (`contract.md:39-51`) on a scratch tree:

```
C1 revision=REPLAY boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=0 met=false   # base, frozen text
C1 revision=REPLAY boxes=4 evidenced=0 gap=4 unexamined=0 mismatches=0 met=true    # four gap rows
C1 revision=REPLAY boxes=4 evidenced=0 gap=4 unexamined=0 mismatches=0 met=true    # four gap rows, each
                                                                                  # check PASSES (path exists)
```

The third line is the decisive one, and the delivered counter encodes the same reading: its own `_clean_rows()`
fixture has boxes 3 and 4 as `status="gap"` with `holds=True` checks (`c77_shonen_ledger.py:868-881`), and its
`clean-four-boxes` case expects `met=True` (`:922-925`). In code, only `status=evidenced` with a false check is
contradictory (`:716-719`); `status=gap` with all-true checks is accepted and counted as `gap`. The ledger's
`status` is therefore declarative and unchecked in the underclaim direction: a box whose cited check passes can
still be called a gap, and `met` stays true. The claim sentence *"no box marker asserts more than the
derivation supports"* is one-directional; it does not stop the reverse.

**Impacted axes:** calibration (the verdict), operability (the instrument's control now passes 22/22, but its base number contradicts A1 — see 1.3).
**Fixable defect or tradeoff:** a tradeoff the contract consciously made, but the *report* must not present
`evidenced=0` as a calibration improvement. If it does, the canonical judge must reject the claim.

**What would make it bite** (smallest first):
1. `met` gains `and evidenced >= 1` (or a named box must be evidenced). One clause, but it changes the frozen
   predicate, so it needs an amendment.
2. Derive `status` from the checks instead of declaring it: `evidenced` iff every check re-derives true, `gap`
   iff at least one re-derives false. Then "gap with a passing check" is impossible and the underclaim escape
   closes. This is a schema change, but amendment 2 A2/A3 already moved the schema toward derivation.
3. Require each `flip` to name a counter rule that currently re-derives false, so a flip is a measurement, not
   prose. This turns every gap into a claim the next round can re-run.

### 1.3 What the amendments already closed (credit), and what they left

Amendment 2 A1 **corrects** the contract's base arithmetic: under the frozen mismatch list, `[ ]` with no row is
not a mismatch, so the base is `mismatches=0`, not `4`. I independently derived that before reading A1. A2
removes executable ledger commands in favour of a counter-owned rule vocabulary; A3 compares `observed`
exactly; A4 closes `[x]`-over-gap and `~`-with-no-row (verified in code, `:680-693`). These are real repairs.

What is left:

- **The delivered counter contradicts A1.** It prints
  `C1 revision=a2cc5f51… boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=4 met=false` (measured, exit 1),
  with four `marker-unsupported` findings. A1 says the base line is `mismatches=0` and the report quotes it.
  The counter's docstring (`:37-53`) and its `missing-ledger` selftest expectation (`:927-929`) lock in the
  superseded `4`. Two standing terms, opposite numbers; the round cannot quote both. Resolve by amendment
  (accept the counter's added "marker with no row is unsupported for every marker" rule) or by changing the
  counter and its selftest to `0`.
- **`[~]` has no standing definition.** The counter's docstring defines it as "examined, evidenced" (`:37-53`),
  but neither the contract nor amendment 2 does; A4 only gates `[x]` on a verifier. A reviewer reading the
  terms cannot derive whether `~` over an evidenced row is legal. One sentence in the terms fixes it.
- **The counter's own selftest moved 18/22 → 22/22** between the two snapshots. At `b97e5037` it failed
  `clean-four-boxes` (`evidenced=1 != 2; gap=1 != 2; mismatches=3 != 0`), `command-run`, `command-drift`,
  `receipt-mode`; at `a9eef8bd` all 22 pass (`selftest: 22/22 passed`). Quote the 22/22 and the hash; the
  A1 contradiction above survives the fix.

---

## 2. C2 — reachability and the 20-case population

### 2.1 Reachability: three snapshots, one real red

The worktree tool (uncommitted, 22:47) supports gzip (bounded decompression), text, RSS, Atom and the
namespace-qualified root dispatch, and the delivered selftest is green (`PASS 266/266`; base `PASS 235/235`).
The matrix moved three times while this seat ran:

| time | counter | cases | line | reading |
|---|---|---|---|---|
| 22:45 | `cf6f8354` | g03 `[]` | `correct=19 wrong=1 met=false` | g03 unsatisfiable (§2.2) |
| 22:48 | `7d2557b2` | g03 `[]` | `correct=20 wrong=0 met=true` | g03 greened by accepting any error code |
| 22:50 | `5c6eacba` | g03 `["gzip_invalid"]`, g02 `["too_large"]` | `correct=18 wrong=2 met=false` | the cases now bite; the tool lags |

The third line is the healthy red. The expectations now name the amendment's ids (A5 `too_large`, A6
`gzip_invalid`) and the two failures are the tool's stale ids: `observed_findings=sitemap_too_large` (g02),
`observed_error=gzip_corrupt` (g03). The after-state is two renames away (`sitemap_too_large` → `too_large` in
the decompressed branch; `gzip_corrupt` → `gzip_invalid`), both inside the edit surface. So the seats can reach
it in one round: the remaining work is a tool edit, not a spec decision.

### 2.2 g03: a real unsatisfiability, a transient relaxation, and the final red

At `cf6f8354` g03 was genuinely unsatisfiable, and the proof is worth keeping because it shows what the case
was meant to test. `judge` required `observed.ids == expected_ids` **and** `error_present == (exit == 2)`;
`observe` added every per-check `error` code to `ids`. With `expect.json = {"exit": 2, "findings": []}` the
three exhaustive output shapes all failed:

| shape | ids | error_present | verdict at cf6f8354 |
|---|---|---|---|
| doc-level error, `checks=[]` | `[]` | false | wrong |
| per-check error `input_invalid` | `["input_invalid"]` | true | wrong |
| exit 2 with a clean check | `[]` | false | wrong |

I ran all three through the counter's own `observe`/`judge`: every verdict `False`; the live run at 22:45
agreed (`observed_findings=gzip_corrupt verdict=wrong`). The counter's selftest never exercised exit 2 with
empty expected ids — `SELFTEST_TABLE["s03"] = (2, ["beta"])` — which is how the hole survived its 10/10.

At `7d2557b2` the counter separated `finding_ids` from `error_ids`. For exit 2 with an empty expectation,
`judge` accepted any error code, and the 22:48 run turned g03 green without changing the tool
(`observed_error=gzip_corrupt verdict=correct`) — a do-nothing green (§4). The vocabulary fix was defensible
(an input fault is not a finding), but it removed the one distinction the case exists to make: a truncated
gzip (`gzip_invalid`) versus an unsupported format (`format_unsupported`).

At `5c6eacba` (22:49) that was closed: the cases were corrected to A5/A6's ids (`g03 ["gzip_invalid"]`,
`g02 ["too_large"]`), `judge` now requires `error_ids == expected_ids` for a pinned exit-2 code (`:209-216`),
and the counter's selftest adds `pinned-input-fault-code-accepted` (14/14). The same tool is now red on
exactly those two ids (`observed_error=gzip_corrupt`, `observed_findings=sitemap_too_large`) — which is the
correct outcome. The remaining action is the tool rename, not another counter edit.

**Impacted axes:** operability (the case under-tests the claimed capability until the code is pinned),
calibration (the 22:48 green was weaker than it read). **Fixable defect; the case fix has landed, the tool fix
has not.**

### 2.3 The 20-case population: what it separates, what it does not

It **does** separate the coarse families: the round-39-blob constant fails 18/20 (measured), and the four
delivered constants fail 12 (`always_clean`), 11 (`empty_findings_real_exits`), 20 (`report_every_id`) and 18
(`round39_xml_only`) cases. The constants are not decorative.

It **does not** establish the claim's family sentence, for five reasons, all local:

1. **RSS date grammar is untested and the clean case encodes the wrong form.** `cases/r01/feed.xml` carries
   `<pubDate>2026-11-02T10:00:00Z</pubDate>` — RFC 3339. RSS 2.0 defines pubDate as RFC 822 (public spec
   fetched 2026-11-03: HTTP 200, 38,676 B, *"All date-times in RSS conform to the Date and Time Specification of
   RFC 822"*). The lane has **no RSS source row at all**: `grep -ni 'rfc 822|rssboard|rss 2.0 specification'
   corpus/SOURCES.md` → empty. The tool happens to accept both forms (`_valid_feed_date`, worktree `:385-399`),
   but nothing in the matrix requires the RFC 822 branch, so the case can green while the family's grammar is
   unmeasured.
2. **No Atom relative-href negative.** `r04` covers an RSS relative link; Atom has only `a02` (missing href) and
   `a03` (malformed updated). A tool that never validates Atom hrefs passes all three Atom cases.
3. **No Atom missing-`<updated>` case.** Contract F2 (`contract.md:101`) calls `<updated>` optional; the wave's
   own retained RFC 4287 (`rfc4287.raw:761`) says *"atom:entry elements MUST contain exactly one atom:updated
   element."* The conflict between S012's "optional" and RFC 4287's MUST is frozen into the contract and never
   tested.
4. **G2 is tested in one direction only.** `g04` is `.gz` name with plain XML. There is no gzip stream under a
   plain name (`sitemap.xml`), which is the direction that falsifies name-based dispatch. A tool that dispatches
   on `.gz` passes g04 and `g01`/`g02`/`g03`/`t06`.
5. **Only the error surface is compared.** The expected value is exit + finding-id set; nine clean cases assert
   only "no finding". A tool that returns clean without parsing (or a 20-way fixture dispatcher) passes them.
   No case compares the URL or date the tool extracted, and there is no hold-out.

**Impacted axes:** operability (what the instrument can prove), coverage (the side-effect it cannot score).
**Fixable defect for 1–4; a tradeoff for 5 unless a hold-out or parsed-value comparison is added.**

### 2.4 The two cases most likely to be mis-specified

1. **`g03`** — the case now expects `gzip_invalid` (corrected 22:49:45) and the tool still emits
   `gzip_corrupt`, so the case is correctly specified and red for the right reason. The contract should have
   said from the start what A6 now says: *"a truncated gzip is exit 2 with check error `gzip_invalid`; expected
   findings `[\"gzip_invalid\"]`"*. The remaining defect is the tool's code, not the case.
2. **`r01`** — the clean RSS 2.0 case carries an RFC 3339 pubDate. The contract should have said: *"RSS 2.0
   `<pubDate>` is an RFC 822 date; r01 carries two RFC 822 dates and expects clean; an ISO-8601 pubDate is
   `lastmod_invalid`"*, and added the RSS 2.0 source row. As built, the case certifies the lane's W3C regex, not
   its RSS reader.

Next two: **`d01`** — the contract's X1 is namespace-blind, and the delivered selftest's `root_wrong_local` is a
`<feed>` root in the *sitemaps* namespace expecting `root_invalid` exit 1 (`selftest:339-354`, base tool
`:441`). Amendment 1 A7 fixes the taxonomy, but the contract table alone would turn `<urlset>`-without-namespace
into `format_unsupported` exit 2 and break four delivered cases. **`g02`** — the case now expects `too_large`
(A5, corrected 22:49:45) and the tool still emits `sitemap_too_large` on the decompressed path while keeping
`too_large` for the plain path (worktree tool `:501-506`): two ids for one condition, and no plain oversize
case compares the two paths. A5 is half-applied: the case yes, the tool no.

### 2.5 Two provenance defects

- **Constant 4 is mislabelled.** `consts/round39_xml_only.py` sha256 `914ebdee…` is **byte-identical to
  `a2cc5f51:scripts/sitemap_audit.py`**, not to the round-39 blob `565ef4c9:scripts/sitemap_audit.py`
  (sha256 `6d86c8ce…`). The contract (`:136-137`) and the matrix call it "the round-39 XML-only tool itself". The
  verdicts on these 20 cases are identical for both blobs (I ran both: `correct=2 wrong=18`), so the count is
  unaffected; the identity statement is false, and a capability claim must not rest on it.
- **`--revision` does not bind the tool bytes.** The frozen command passes `--tool scripts/sitemap_audit.py`
  and `--revision <hash>`; with `--tool`, the counter measures the worktree path and only prints the revision
  (`c77_sitemap_matrix.py:586-598`). I ran it with the round-39 blob in scratch under
  `--revision a2cc5f51…` and it printed `C2 revision=a2cc5f5100…` while measuring sha256 `6d86c8…`. This is
  the exact false provenance round-76 defect D1 asks the round to close. Fix: when `--revision` is given with
  `--tool`, require `git hash-object <tool>` == `git rev-parse <rev>:scripts/sitemap_audit.py`, else exit 2 —
  or use `--tool-revision` in the frozen command.

**Impacted axes:** calibration (receipt truth), operability. **Defects the canonical judge must reject.**

---

## 3. Axis naming

- **C2** is operability by AXES.md:13: *"Runnable artifacts: checklists that are executable, commands that
  exist, scripts that run | A checklist item can be run and produces the stated outcome."* The matrix runs the
  script and compares the stated outcome; that is the signal sentence. The coverage side-effect (AXES.md:12) is
  outside this lane's scored ownership (SCORECARD.md:3-6), so it must not be scored, and the capability table
  (AXES.md:40) is the right receptacle. **Not a different axis; a capability acquisition that lands an
  operability verdict.**
- **C1** is calibration by AXES.md:15's own signal (*"SHONEN.md/SCORECARD entries match observed repo state"*).
  **Not a different axis.** The trap is not mis-assignment but *laundering*: an instrument-completeness verdict
  reported as a calibration improvement (see §1.2), or a capability reported as coverage growth (see §3, C2).
- The lowest-axis rule is satisfied: C1 is on calibration (2), the lane's lowest non-retired axis; C2 is a
  capability on operability (10). The two claims are on distinct axes (AXES.md:32-33).

---

## 4. Do-nothing control

### C1 — an all-gap ledger greens; the kill rule does not exclude it

Cheapest do-nothing: write four `status="gap"` rows whose frozen checks genuinely fail (A12 hands box 2's
absent round-47 receipt), leave `SHONEN.md`/`SKILL.md`/`LOG.md`/`PROVINCE.md` untouched. Predicate:
`boxes=4, unexamined=0, mismatches=0` → `met=true`, exit 0. The delivered counter accepts `gap` with a passing
check and counts it as `gap` (§1.2), so even a box whose evidence holds can be filed as a gap.

Does the kill rule exclude it? **No.** It forbids (i) taking `holds` as given — the counter re-derives; (ii)
`met=true` on the base tree or on empty `checks` — the rows are non-empty. The all-gap ledger is inside the
rule and green. The cheapest variant that changes no lane artifact at all is therefore a valid round under the
frozen predicate; the verdict is "classification complete", not "calibration improved".

### C2 — the counter-edit green, and what closed it

**Demonstrated at 22:48, closed at 22:49.** The counter edit alone moved the matrix from
`correct=19 wrong=1 met=false` to `correct=20 wrong=0 met=true` with no change to the tool's gzip
classification: it emitted `gzip_corrupt` before and after, and g03 flipped because `judge` stopped requiring
the error code in the expected id set. That was the cheapest path to the frozen target, and the kill rule did
not exclude it: the comparison was still richer than exit-only, and the constants still failed 4/4. The round
then did the right thing — at 22:49 the cases were corrected to A5/A6's ids and `judge` was tightened to
compare a pinned error code (`error_ids == expected_ids`); the same tool is now red on exactly the two stale
ids. Post-correction the cheapest green is a two-line tool rename, which is a legitimate fix, not a
do-nothing.

The remaining do-nothing: a 20-way fixture dispatcher still greens — the four constants fail, but no hold-out
case exists, and clean cases assert only silence. The constants do exclude the *alignment-to-the-old-tool*
trick (constant 4 would then pass and `constants_failed < 4`), which is worth crediting; they do not exclude
fixture-fitting.

---

## 5. Smallest safe corrections (ranked)

**C1**
1. Resolve the base number: either amend A1 to accept the counter's added "marker with no valid row is
   unsupported for every marker" rule (base `mismatches=4`), or change the counter and its `missing-ledger`
   fixture to `0`. The report may quote only the surviving one.
2. Keep the counter's selftest green at the landed blob and quote `selftest: 22/22 passed` with the blob hash
   (`a9eef8bd…` at this snapshot).
3. State `[~]` in the terms (one sentence: "examined and evidenced, unsigned; `[x]` additionally requires a
   named verifier").
4. Decide the shape: either add `evidenced >= 1` to `met`, or write in the report that `evidenced=0` lands a
   classification verdict and no calibration move. Do not let the report imply the second is the first.

**C2**
1. Rename the tool's two ids: `sitemap_too_large` → `too_large` on the decompressed branch, and
   `gzip_corrupt` → `gzip_invalid`. The cases already expect both (22:49); re-run the matrix.
2. r01: replace the two RFC 3339 pubDates with RFC 822 dates; add an ISO-8601-pubDate case expecting
   `lastmod_invalid`; add the RSS 2.0 source row.
3. Add a plain-XML oversize case (52,428,801 bytes, uncompressed) so `too_large` on the plain path is
   compared with g02's decompressed path; the matrix currently has only the gzip path.
4. Constant 4: extract `565ef4c9:scripts/sitemap_audit.py` at counter time, or relabel it "base round-42 tool"
   and say so in the claim.
5. Bind `--revision` to the tool blob (hash-equality gate) or use `--tool-revision` in the frozen command.
6. Add the four family holes (Atom relative href, Atom missing updated, gzip under a plain name, RSS RFC 822)
   and at least one hold-out variant per family — or compare the parsed URL/date set so the clean cases test
   parsing rather than silence.

---

## Appendix A — commands and observed output

All from the lane root unless stated; scratch under `/fast/scratch/hyaku/kake-r77/CriticC`; `python3 -B`.

```
$ python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=4 met=false
  finding: marker-unsupported box 1 marker [ ] — no valid ledger row: the marker asserts a verdict nothing derives
  ... (boxes 2-4 identical)
exit=1

$ python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --selftest --work <scratch>
# b97e5037 (22:45): selftest: 18/22 passed, exit 1; FAIL clean-four-boxes (evidenced=1 != 2; gap=1 != 2;
#   mismatches=3 != 0), command-run, command-drift, receipt-mode
# a9eef8bd (22:48): selftest: 22/22 passed, exit 0

$ python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . --tool scripts/sitemap_audit.py \
    --revision worktree-snapshot-2245 --cases .ufo/waves/round-77/cases \
    --consts .ufo/waves/round-77/consts --work <scratch> --verbose        # counter cf6f8354, 22:45
C2 revision=worktree-snapshot-2245 cases=20 decided=20 correct=19 wrong=1 constants_failed=4/4 met=false
case g03 expect_exit=2 expect_findings=- observed_exit=2 observed_findings=gzip_corrupt verdict=wrong
const always_clean.py failed=12 ids=a02,a03,d01,g02,g03,r02,r03,r04,t02,t03,t04,t05
const empty_findings_real_exits.py failed=11 ids=a02,a03,g02,g03,r02,r03,r04,t02,t03,t04,t05
const report_every_id.py failed=20
const round39_xml_only.py failed=18
exit=1

$ same command --revision resnapshot-2248                                   # counter 7d2557b2, 22:48
C2 revision=resnapshot-2248 cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true
case g03 expect_exit=2 expect_findings=- observed_exit=2 observed_findings=- observed_error=gzip_corrupt verdict=correct
exit=0

$ same command --revision final-2250                                   # counter 5c6eacba, cases 22:49, 22:50
C2 revision=final-2250 cases=20 decided=20 correct=18 wrong=2 constants_failed=4/4 met=false
case g02 expect_exit=1 expect_findings=too_large observed_exit=1 observed_findings=sitemap_too_large verdict=wrong
case g03 expect_exit=2 expect_findings=gzip_invalid observed_exit=2 observed_findings=- observed_error=gzip_corrupt verdict=wrong
exit=1

$ python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --selftest --work <scratch>
selftest 14/14 passed            # 5c6eacba; was 10/10 at cf6f8354, 12/12 at 7d2557b2
exit=0

$ python3 - <<'PY'   # g03 at cf6f8354, using the counter's own observe/judge
... for each of: doc-level error; per-check error input_invalid; exit 2 + clean check
observed: ([] , error_present=False) / (["input_invalid"], True) / ([] , False)
verdict:  False / False / False
PY
# at 7d2557b2 the same three shapes: doc-level and clean-exit-2 still fail; input_invalid passes because
# judge accepts any error code for an empty expectation (selftest: empty-expect-input-fault-accepted)
# at 5c6eacba (22:49) the cases pin the codes: g03 expects ["gzip_invalid"], g02 ["too_large"]; the tool
# emits gzip_corrupt / sitemap_too_large and is red on both (selftest: pinned-input-fault-code-accepted)

$ python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py
PASS 235/235                 # base a2cc5f51
PASS 266/266                 # worktree snapshot 22:47

# base tool (a2cc5f51 blob) on scratch fixtures
g01  exit=1 encoding_invalid
g04  exit=0 clean
t01  exit=1 xml_malformed
d01  exit=1 root_invalid          # contract d01 expects exit 2 format_unsupported
r01  exit=1 root_invalid
a01  exit=1 root_invalid
root_nons/root_feed_sm exit=1 root_invalid

$ sha256sum .ufo/waves/round-77/consts/round39_xml_only.py
914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021
$ git show a2cc5f51:scripts/sitemap_audit.py | sha256sum
914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021
$ git show 565ef4c9:scripts/sitemap_audit.py | sha256sum
6d86c8cef78e36d372f7277096ec163cc8f1e919fa66702ad24e5e32f9a240ec

$ python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . --tool <scratch>/tool_r39.py \
    --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 ... --work <scratch>
C2 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 cases=20 decided=20 correct=2 wrong=18 constants_failed=4/4 met=false
# measured tool sha256 6d86c8ce… (round-39 blob), revision label a2cc5f51… — label not bound to bytes

$ python3 -c 'gzip-decompress cases/g02/sitemap.xml.gz'
g02 decompressed bytes = 52428801 > 52428800: True   (compressed 51,139)

$ curl -sSL --max-time 30 https://www.rssboard.org/rss-specification
200 38676   # "All date-times in RSS conform to the Date and Time Specification of RFC 822"
```

Against the frozen definitions (`contract.md:39-51`), the base tree with no ledger has `unexamined=4` and
`mismatches=0`; the contract's original `mismatches=4` needs the unwritten "a `[ ]` with no row is a mismatch"
rule, which amendment 2 A1 rejects and the delivered counter nevertheless implements. This is the one place
where the two standing terms give different base receipts.

## Appendix B — bytes read

- `contract.md:32,39-51,54-56,58-60,70,92,100-104,107,115-134,139-141`
- `amendment-1.md` A5/A6/A7/A9; `amendment-2.md` A1/A2/A3/A4/A5
- `AXES.md:12-13,15,32-33,40`; `SCORECARD.md:3-6`; `SHONEN.md:5-8`; `LOG.md:787`
- base tool `a2cc5f51:scripts/sitemap_audit.py:413` (`too_large`), `:441` (`root_invalid`);
  base selftest `:339-354` (four `root_invalid` cases), `:491` (`too_large`)
- `c77_shonen_ledger.py:37-53,680-726,846-882,922-929,1086-1092`
- `c77_sitemap_matrix.py:131-196,333-340,586-598`
- `cases/g02/expect.json`, `cases/g03/expect.json`, `cases/r01/feed.xml`, `cases/t07/sitemap.txt`,
  `cases/d01/page.xml`
- worktree `scripts/sitemap_audit.py:385-399,472,501-506,528-560` (uncommitted)
- `rfc4287.raw:653,761`; `protocol.raw:885,949,957,977-980,985-1025`
