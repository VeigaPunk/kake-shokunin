# ReviewQualityBar — round 51 wave 1

Seat: `L1Kake51.ReviewQualityBar-2` (leaf; no subagent dispatch). Judged on freshness.

**Measured revision:** `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (lane tip at wave dispatch).
All byte reads below are `git show <rev>:<path>` / `git cat-file -e <rev>:<path>`, i.e. committed
bytes, not the worktree. Scratch only under `/tmp` (`/tmp/r51qc`, `/tmp/r51qcf` clones).
No lane file, jj state, index, residual report or inherited validation copy was touched.
**Tools installed/upgraded: none** (nothing needed; no pacman/uv/npx/cargo invocation).

Artifacts judged, per the assignment:

| Artifact | Path |
|---|---|
| Entry 1 | `corpus/knowledge/canonical-selection.md` (77 lines, new) |
| Entry 2 | `corpus/knowledge/crawler-identity.md` (54 lines, new) |
| Lesson | `corpus/lessons/round-51.md` (116 lines, new) |
| Registry rows | `corpus/SOURCES.md:152-153` (S262, S263) |
| Retained sources | `.ufo/waves/round-51/sources/{S262.html,S263.html,receipts.json}` |
| Claim machinery | `.ufo/waves/round-51/{contract.json,c51_quote_truth.py,c51_wave_ledger.py,controls/*.txt}` |
| Append log | `LOG.md:2051-2086` |

---

## 0. Claim verdicts at the measured revision

| Claim | Predicate | Reproduced verdict | Exit |
|---|---|---|---|
| C2 (freshness) | `met: conditions_passed == 8 of 8` | **C2 quote-truth 8/8 met=True** | 0 |
| C1 (operability) | `met: ledger_checks_passed == 3 of 3` | **C1 ledger 0/3 met=False** | 1 |

C1's three failures at `9d13768`: `settlement receipt absent`, `route map absent`,
`timing/settlement absent`. `git cat-file -e 9d13768:.ufo/waves/round-51/{settlement.json,
route-map.json,wave-timing.json,round-time-accounting.json}` → absent for all four; `w1/` is
absent from the tree at that revision. The wave had not settled, so this is the declared
"expected 0 before the L1 writes the evidence" state — but the contract's C1 `after` text and
the lesson already speak as if it exists (finding **M4**).

**C2's 8/8 is a printed verdict, not a valid measurement.** Seven conditions are real and I
reproduced their discrimination; **C8 never reads the mirror it names** and the committed
"pre-append mirror" is byte-identical to the *post*-append registry. See **H0** below. C2's
declared `after` sentence — *"the mirror census-validated with `--file` before the append"* —
is false on the committed bytes, so C2 is **not met as claimed** at this revision even though
the counter exits 0.

**Frontier step.** The contract declares no separate frontier artifact; it names one theme and two
claims. `corpus/README.md`'s `## Frontier` and its per-round frontier sections contain no
round-51 entry (newest: `## Round-39 frontier step`, `README.md:377`), and the coverage index has
no round-51 row (L3). So the round's only declared movement is: C2's two entries (real, with the
label/locator defects in M1/M2/M7) and C1's ledger (an instrument with no data yet). Nothing else
is claimed, and nothing else is evidenced.

---

## 1. Commands actually run (argv, output, exit)

```
python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768c…  -> 8/8 met=True,  exit 0
python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 559155795…  -> 8/8 met=True,  exit 0
python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 19a99bd8c…  -> 2/8 met=False, exit 1
python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 007d66e4e…  -> 0/8 met=False, exit 1
python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision deadbeef…  -> 0/8 met=False, exit 1  (finding M6)
python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768c…  -> 0/3 met=False, exit 1
python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 007d66e4e…  -> 0/3 met=False, exit 1
python3 -B .ufo/waves/round-51/c51_wave_ledger.py                     (no args)  -> exit 2          (finding M6)
python3 -B .ufo/waves/round-34/criteria/gate_reject_check.py --repo . --rev 9d13768 \
        --lesson corpus/lessons/round-51.md  -> "NO MATCH: ## Gate has no source decision
        beginning with reject and a non-empty reason", exit 1                                (finding H4)
git cat-file -e <hash>^{commit}   for d969fa28…, cc57cb80…  -> absent (exit 128)               (finding H1)
git diff --numstat 007d66e 5591557 -- corpus/SOURCES.md corpus/knowledge/ LOG.md \
        corpus/lessons/ -> 2/0, 77/0, 54/0, 116/0, 33/0 (added/deleted; pure additions)
comm -12 <(sort staged-ids) <(sort reg-ids) -> S273 S274 S286   (matches lesson:60-67)
git show 19a99bd:<MIRROR>       | sha256sum -> 4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3
git show 5591557:corpus/SOURCES.md | sha256sum -> 4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3  (identical)
git show 19a99bd:corpus/SOURCES.md | sha256sum -> cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117
data rows: mirror@19a99bd = 145, live registry@5591557 = 145, live registry@19a99bd = 143
grep -n 'mirror_registry = show' c51_quote_truth.py -> 277: mirror_registry = show(root, mirror_commit, REGISTRY)
```

Independent re-derivation I performed (not the round's own instruments):

- **Digests**: `sha256(S262.html)=792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b`
  (174,926 bytes) and `sha256(S263.html)=6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de`
  (175,561 bytes) both equal `receipts.json`, and both byte counts equal the files.
- **Quote classes**, every quoted span in both entries classified by testing the raw body, then a
  tag-stripped body, then a whitespace-collapsed tag-stripped body (table in §6).
- **Discrimination mutants** in `/tmp/r51qcf` (depth-50 clone; baseline 8/8 exit 0):
  `m1` wrong-but-plausible Gate quote → 7/8, **C5 FAIL**, exit 1; `m2` + one-byte flip in
  `S262.html` → 6/8, **C5+C6 FAIL**, exit 1; `m3` + `used-by` swapped → 5/8, **C4+C5+C6 FAIL**,
  exit 1. The counter therefore rejects fabricated quotes, mutated bodies and wrong `used-by`.

---

## 2. Findings

### High

**H0 — C8 passes without reading the mirror, and the committed "pre-append mirror" is the
post-append registry.**
`c51_quote_truth.py:277` reads `mirror_registry = show(root, mirror_commit, REGISTRY)` — the
**live** `corpus/SOURCES.md` at the mirror's add-commit, not the `MIRROR` path. At `19a99bd`
the live registry has 143 data rows and no S262/S263, so for this round's data C8's "the mirror
already carries the row" branch cannot fire. The actual committed mirror is byte-identical to the post-append
registry: `sha256(git show 19a99bd:…/pre-append/corpus/SOURCES.md)` =
`sha256(git show 5591557:corpus/SOURCES.md)` = `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3`,
both 145 data rows, both carrying S262 and S263; the live registry at the mirror commit is
`cd9ee4cf…` with 143 rows. So the file committed as "before" is the *after* registry, the copy C7's
`--file` census names is (in the committed tree) the post-append registry, and C2's `after`
sentence *"the mirror census-validated with `--file` before the append"* is not supported by
any committed bytes. Criteria (`QUALITY.md:461`):
*"A counter compares every field its expectation names, and judges a usage case on the usage
object"* — C8 names "the mirror's registry" and compares a different file; and
(`QUALITY.md:11`) *"Replayable claim … frozen input expectations pin their bytes"* — the frozen
"before" bytes are the "after" bytes. A wave-1 sibling (`ExecRegistryDiff`) reached the same fact
from the registry diff; the repair in progress is
`.ufo/waves/round-51/assimilation/pre-append/census-correction.txt` (worktree, uncommitted at
`9d13768`). My own earlier worktree `grep` read 0 only because that repair had already rewritten
the file in the worktree; the committed blob is the contaminated one, which is what C2 measures.

**H1 — The two junk-control receipts cite revisions that resolve nowhere; the round's own
counter-discrimination evidence cannot be replayed.**
`.ufo/waves/round-51/controls/c1-junk-wave.txt:10` names
`revision: d969fa2819f1f2050c10637531cba2e12f92a557`; `.ufo/waves/round-51/controls/c2-junk-entries.txt:16`
names `revision: cc57cb80b2060f8c754a896235e323f67a5a91da`. `git cat-file -e <hash>^{commit}`
is absent for both, and neither receipt names a bundle. Criterion (`QUALITY.md:899`):
*"(d) Every cited commit hash resolves in lane history, or the citation names the bundle that
contains it. Do not present a bundle-only hash as a lane commit."* This is also `QUALITY.md:608`:
*"A cited artifact resolves from committed lane bytes, not a seat's sandbox."* The junk control is
the only evidence that C2 rejects a fabricated entry set; it is unreplayable. My three mutants
(§1) supply discrimination in place of it, but they are reviewer-side, not round evidence.

**H2 — Control receipts name a revision but not the counter they were scored with.**
All four `.ufo/waves/round-51/controls/*.txt` carry a `revision:` line and no digest of
`c51_quote_truth.py` / `c51_wave_ledger.py`. The C2 counter was changed **after** those receipts
were committed (`9d13768`, +2 lines at `c51_quote_truth.py:224-225`), so their bytes cannot show
which counter produced them. Criterion (`QUALITY.md:433`): *"A measurement receipt names the
revision it measured and the digest of the bytes it measured. … an absolute tool path is not a
digest."* Round-34 wave-2 correction (c) sharpens it: *"text receipts count only when the file
name carries the hash."* Neither applies here.

**H3 — The lesson cites two artifacts that do not exist at the citing revision.**
`corpus/lessons/round-51.md:106-109`: *"the round-51 settlement carries the wave's start and end
stamps, `.ufo/waves/round-51/round-time-accounting.json` carries the three figures"*. At
`9d13768` neither `settlement.json` nor `round-time-accounting.json` exists (and the latter does
not exist in the worktree either). Criterion (`QUALITY.md:608`): *"A cited artifact resolves from
committed lane bytes … a citing line whose retained path is absent at the citing revision."*
Round-34 (c) (`QUALITY.md:643`): *"Every run a report cites ships a committed receipt … 'run, not
committed' is not a result."*

**H4 — The round's `## Gate` records no screened reject.**
`corpus/lessons/round-51.md:6-16` holds two `admit`-shaped source lines and no reject. The two
screened rejections (engine-crawl-contracts, crux-eligibility-route) sit under a separate
`## Refused entries` heading at `:32-47`, with located reasons. The committed check
`.ufo/waves/round-34/criteria/gate_reject_check.py --repo . --rev 9d13768 --lesson
corpus/lessons/round-51.md` exits **1** with `NO MATCH: ## Gate has no source decision beginning
with reject and a non-empty reason`. Criterion (`QUALITY.md:627`): *"A round's `## Gate` records at
least one screened reject with its reason … Reject: … a screened rejection recorded only in a wave
report."* Scope note: the same check exits 1 on `round-49.md` and `round-50.md`, so this is an
inherited lane pattern, not a round-51 regression — but it is still not met by these bytes.

**H5 — A verdict-time result is stated in `LOG.md` prose with no committed receipt.**
`LOG.md:2081-2083`: *"Re-run at the append commit `55915579563a…`: C2 8 of 8 (exit 0). The junk
control still fails 3 of 8 and the base control still 0 of 8, both re-run with the corrected
counter."* No committed receipt names `5591557` or the post-fix re-run; `git show --stat 9d13768`
touches only `c51_quote_truth.py` and `LOG.md`, so the control files on disk are the pre-fix bytes.
Criteria: `QUALITY.md:1073` *"Verdicts carry committed receipts (round 47). A filed verdict-time
gate result (exit code or tally) has its output committed as a receipt at the round it is
claimed; prose restatement in a report or LOG is not the receipt."* And `QUALITY.md:450`:
*"A named measurement revision has a committed receipt that names it."*

### Medium

**M1 — A quote-class sentence in the entry contradicts its own annotations.**
`corpus/knowledge/canonical-selection.md:37`: *"The page lists the variant classes it recognises,
each quoted raw from the page:"* — but `:41` and `:43` annotate two of those same four bullets
`"(collapsed-only quote)"`. Mechanically none of the four is a raw substring of the retained HTML
(the body carries `<b>Device variants</b>: …`); two are raw only in tag-stripped visible text and
two require whitespace collapse. Criterion (`QUALITY.md:1100`): *"A quote's match class is derived
from its own two blobs, never asserted (round 50) … a collapsed-only span is never described as a
raw substring nor the reverse — the two classes are different facts and a swapped label fails the
check."* Nothing in the round derives the class of a non-Gate quote: `c51_quote_truth.py` C5
checks only the lesson Gate quote.

**M2 — The lesson's universal quote claim is false on its own artifacts.**
`corpus/lessons/round-51.md:13-16`: *"Every quote in the two admitted entries is an exact substring
of the retained body after whitespace collapse; the two quotes above are raw substrings, and each
entry marks the class of every other quote it carries."* Counterexamples in committed bytes:
`canonical-selection.md:62` quotes `"how to specify"` and `"fix issues"` (S021/S022 shorthand, not
in either body); `:68` quotes `"quality comparison"` (Baidu, not in either body); `:60` quotes
`"objectively the most complete and useful for search users"` with no class mark at all. The
first three are labels, not source quotes, so the entry is defensible — the lesson's unqualified
*"every quote"* and *"marks the class of every other quote"* are not.

**M3 — Condition C2's stated identity does not exist: "below its 8-line metadata header".**
`contract.json:41` and `c51_quote_truth.py:154` say *"8-line metadata header"* / *"8-line header"*;
the code skips `lines[:8]`. The corpus rule is a **four-line** prefix (`QUALITY.md:70`: *"knowledge
entries that receive the four-line metadata prefix"*), and both entries have exactly four metadata
lines (`source:`, `verified-at:`, `recheck:`, `ground:`) then a title. So the condition's wording
describes a shape the artifacts do not have, and the check silently skips the title and the first
three body lines. It still passes for the right reason (inline `[S262]`/`[S263]` citations below
line 8), but the declared identity and the measured one differ.

**M4 — C1's declared after-state is contradicted at the measured revision and no honest-stop
record exists.**
`contract.json` C1 `after`: *"3 of 3 at the measured commit (the settlement, the route receipts, the
time-accounting artifact and the LOG figure are all committed)"*, and `killRule`: *"a miss on any
of L1, L2 or L3 is an honest stop for C1 and is reported as such."* Measured: 0/3, exit 1, all four
artifacts absent. Neither the lesson nor `LOG.md` records the C1 result at `9d13768`; the lesson
does not mention C1 at all, and its `Mistakes` fixes describe the settlement/timing in the present
tense (H3). Criterion (`QUALITY.md:12`): *"Missing substrate stays visible: Source/history
unavailability is marked as named debt with an owner and concrete restore-or-retire action. Reject:
… weakening the gate solely to recover a green verdict."* The L1 states the evidence lands after
settle, which is a legitimate pending state — but pending must be written as pending.

**M5 — The wave grant and dispatch command are not committed at the measured revision.**
`.ufo/waves/round-51/wave-grant.txt` (`granted lane=kake wave=r51-w1 seats=48 live=66 pending=0
cap=256`) and `w51-taskcall.json` are untracked: `git ls-files .ufo/waves/round-51/` lists neither.
`corpus/lessons/round-51.md:3-4` cites the 48-seat wave. Criterion (`QUALITY.md:1090`): *"A wave
citation carries its own grant (round 50). A round that cites a dispatched wave commits the
wave-slot grant stdout and the exact dispatch command as committed bytes at a revision that is a
strict ancestor of the revision the citation is made in … A grant line that exists only in a
report, in a LOG entry or in a `/tmp` file is not evidence."* Unmet at this revision; it may land
with the wave evidence.

**M6 — The counting commands document exit codes they never return.**
Both docstrings declare *"Exit codes: 0 the predicate is met, 1 it is not, 2 the evidence cannot be
evaluated, 64 usage error"* (`c51_wave_ledger.py:26-27`, `c51_quote_truth.py:31-32`). `main()`
returns only 0 or 1 in both; a nonexistent revision is scored `0/8` and `0/3` at exit 1,
indistinguishable from a measured miss, and a usage error exits **2** (argparse), not 64.
Criterion (`QUALITY.md:112`): *"A documented output contract ('always one JSON object') covers
every exit path including usage errors"*; and `QUALITY.md:104`: *"An unmeasurable baseline
(instrument not validated) exits nonzero, never with the 'proven absent' code."*

**M7 — The `§` locator for S262 resolves to page chrome, not a section.**
`corpus/SOURCES.md:152` and `corpus/lessons/round-51.md:8` both write
`§ "What is URL canonicalization"`. In the retained body the only occurrence of that string is a
navigation link title: `<span class="devsite-nav-text" tooltip>What is URL canonicalization</span>`
inside `class="devsite-nav-title"`; the page's `<h1>` is **"What is canonicalization"**.
`canonical-selection.md:12-13` therefore says *"quoted from the section \"What is URL
canonicalization\""* for a section with another title. Criterion (`QUALITY.md:212`, round-26): *"A
recheck HOLD needs a row-specific located quote: page chrome or any text that also occurs in a
different source's bytes cannot ground a row."* For S263 the locator is the section's first body
sentence, not its heading (`<h1 id="googlebot">Googlebot</h1>` then `<p>Googlebot is the generic
name for two types of …`), so the `§` convention is looser than the heading it implies. The Gate
*quote* is body text and true in both cases; the locator label is what is wrong.

### Low

**L1 — An unsourced attribution about another engine.**
`corpus/knowledge/canonical-selection.md:68-69`: *"It does not establish the selection rule for any
other engine. Baidu publishes a different account (a quality comparison); that is outside this
row's scope."* No row, no quote, no `[INFERENCE]`. Criterion (`QUALITY.md:16`): *"A claim about what
a hosting, CI or crawler platform serves, ignores or validates cites a tier-A row in
`corpus/SOURCES.md` …"* — a scoping sentence is still an attributed fact.

**L2 — An inferential clause stated as source fact.**
`corpus/knowledge/canonical-selection.md:55-56`: *"A declared canonical can be ignored, and a page
with no declaration still gets one."* The first clause is quoted; the second is not quoted anywhere
and carries no `[INFERENCE]`. It is supported by inference from the page's definition
(*"Canonicalization is the process of selecting the representative – canonical – URL of a piece of
content"*, located at body offset before "What is canonicalization" in the retained bytes), but the
mark is missing. Criterion (`QUALITY.md:512`): *"A qualifier a source does not state is marked …
Reject: … a claim made over a list of keys is checked key by key"*; round-27's *"label the
inferential/local-policy step"*.

**L3 — The coverage index is not updated.**
`corpus/README.md` holds neither entry and has no round-51 coverage row or section; the
`## Coverage map` table's newest rows stop at round 38 and the per-round coverage sections stop at
round 37/39. The lesson's claim (*"the coverage map in `corpus/README.md` did not hold this
ground"*, `:44-47`) is true but is left true. Inherited since round 39, not introduced here; still
an index/freshness gap for the ground this round claims to move.

**L4 — `## Refused entries` reasons are better than the `## Gate` needs, and the Gate could cite
them.** Not a defect on its own; recorded because H4's fix is a one-line relocation, not new work.

---

## 3. Criteria the round's artifacts MEET (criterion's own wording)

| QUALITY.md | Criterion (own wording, quoted) | Evidence at `9d13768` |
|---|---|---|
| :10 | "Citation-local absence — A deleted publishing-source citation carries its own annotation under P1's documented local rule, or is fixed to a verified surviving source." | Vacuously met: `git diff --numstat 007d66e 5591557 -- corpus/SOURCES.md` = `2 0`; no occurrence is edited or deleted. |
| :13 | "Admission authority — Local implementation evidence is labelled local; specialist dispatch and non-author review are evidenced separately." | Both entries label themselves: `canonical-selection.md:77` "It is not a live measurement"; `crawler-identity.md:54-55` "the entry is a documentation reading, not a live observation." No admission or promotion is claimed. |
| :14 | "Shape-only probe environment — Record override variable names and lane-local isolation shape; use symbolic placeholders in captured output. Keep replay paths only as ordinary fixture metadata." | `receipts.json` carries URL, integer HTTP status, byte count, sha256, doc revision only; no env values, headers, cookies or session bodies. Grep of both bodies for `sessionid|csrf|api[_-]?key|authorization: bearer|set-cookie` → 0 hits. The census argv's absolute path is replay metadata, which the admit clause allows. |
| :16 | "Platform mechanism (r20 resume) — A claim about what a hosting, CI or crawler platform serves, ignores or validates cites a tier-A row in `corpus/SOURCES.md` at a pinned tag, commit or dated doc, with a recheck argv." | S262/S263 are tier `A`; the dated doc revisions are in the retained bodies ("Last updated 2026-08-20 UTC", "Last updated 2026-02-03 UTC", both verified by grep); the recheck argv is at `round-51.md:78-82`. The argv's own 2026-10-23 run has no receipt (see §4). |
| :19 | "Population unit named (r20 resume) — Every dead-path or count claim names its population … the scanner contract and the command." | `round-51.md:60-67` names the populations (staged ids, lane-registry ids) with the committed files; I re-derived the intersection (`comm -12`) → exactly S273/S274/S286. |
| :31-38 | Superseding append-only ruling: "preserve every prior lesson/knowledge line byte-identically; use pure new-line additions or end-of-file correction blocks." | `git diff --numstat 007d66e 5591557` = 0 deletions in `corpus/SOURCES.md`, `LOG.md`, and both new entries/lesson are pure additions. |
| :70 | "All pre-round-21 literal pointers into knowledge entries that receive the four-line metadata prefix retain their baseline coordinates." | No existing entry receives a prefix; both entries are new files; no pointer moved. |
| :104 | "An unmeasurable baseline (instrument not validated) exits nonzero, never with the 'proven absent' code." | Half met: an unmeasurable revision exits nonzero (1) in both counters; the missing distinction from a measured miss is M6. |
| :307 | "A counter must be able to reject a constant. … A gate that refuses everything, or returns a fixed answer, must score below the declared after-value." | C2: 0/8 at base, 2/8 at the pre-append commit, 8/8 after → not a fixed answer. Reviewer mutants: 7/8 (C5), 6/8 (C5+C6), 5/8 (C4+C5+C6), exit 1 each. |
| :375 | "A Gate quote is found in retained source text. A Gate quote counts only when it is an exact substring of retained visible source text whose digest the counter verifies against the round's committed receipt before comparing." | Both Gate quotes are raw substrings; both body digests match `receipts.json` (I re-hashed both files). `round-51.md:8-9` and `:10-11`. |
| :433 | "A measurement receipt names the revision it measured and the digest of the bytes it measured." | Half met: `receipts.json` pins both body digests; the control receipts' missing counter digest is H2. |
| :549 | "Stated times are read, not estimated." | `round-51.md:11-12` says "2026-10-24, 23:16 -03:00"; `receipts.json.fetchedAt` = `2026-10-24T23:16:49-03:00`; the declaring commit `5591557` has committer time `23:20:56-03:00`, after the fetch. |
| :741 | "No pre-build receipt publishes a value the build is later measured by." | The four control receipts publish the base/junk revisions and their own condition states; the entry states no number copied from them. The contract's `8 of 8` is a declared target, which this criterion permits. |
| :866 | "(b) A counter version bump preserves the declared predicate." | `9d13768` diff = +2 lines (receipt lookup under `sources`); predicate `8 of 8`, the eight condition sentences and the target are unchanged; `LOG.md:2077-2080` names the forcing failure (C6 "no receipt"). |
| :905 | "(g) A bare source id alone does not satisfy a knowledge-entry `cites` condition." | Ids appear beside claim text: `canonical-selection.md:12-17,30-31,36`, `crawler-identity.md:8-10,22-24,32`. |
| :1109 | "Operator-owned and inherited artifacts are not swept to zero a count (round 50)." | `git status --porcelain` still shows the eight `.ufo/waves/round-46/residual/` reports and nine `>1MiB` copies under `.ufo/waves/round-48/assimilation/validate/`, untracked; `round-51.md:110-119` reports the count as it stands. |
| :145 round-23 | "A freshness receipt counts only with at least one claim decided against a live surface." | The claim is decided against bytes fetched 2026-10-24 from the live vendor pages (HTTP 200 in `receipts.json`), not against repo shape. |
| :161 round-24 | "Parse every receipt field against its documented grammar and JSON type before method calls or comparisons." | `fetchedAt` is a valid ISO offset timestamp; `httpStatus` 200 is an integer; `bytes` are integers equal to the file sizes; `sha256` equals the body digest; `url` equals the registry row URL (C6 pass, re-verified by hand). |
| :170 round-25 | "A source adapter's abstract-only result is not a normative source read. Open the pinned official document and locate the criterion body; retain the source bytes and digest." | Full pages retained (174,926 / 175,561 bytes); both Gate quotes are in `<p>` body elements (S262: `<p>` around "…a hint, not a rule."; S263: `<p>` after `<h1 id="googlebot">Googlebot</h1>`), not in a meta description, nav span or doclink. |
| :212 round-26 | "STALE means the statement is wrong or unsupported at its own stated scope." | Both statements hold at their stated scope; the dated doc revisions are in the retained bytes. |
| :260 round-27 | "Freeze expected outcomes before implementation … Freeze … retained original counter bytes." | Contract + counters committed at `19a99bd` (committer 23:20:47) before the entries at `5591557` (23:20:56); the pre-fix counter bytes remain in history at `19a99bd:c51_quote_truth.py`. |

---

## 4. Criteria NOT met or NOT evidenced (criterion's own wording)

| QUALITY.md | Criterion (own wording, quoted) | Why it fails / is unevidenced |
|---|---|---|
| :11 | "Replayable claim — The report names the source revision or script digest, exact argv, full verdict and exit; frozen input expectations pin their bytes." | Bytes are pinned (sha256 + size), but **no exact fetch argv**: `receipts.json.fetcher` is a template with `<body>`/`<url>` placeholders, and the lesson states no C2 verdict/exit. H3/H5. |
| :12 | "Missing substrate stays visible — Source/history unavailability is marked as named debt with an owner and concrete restore-or-retire action." | The quarantine slice is visible (`round-51.md:69-75`, 12 ids with reasons), but the absent settlement/route/timing — the entire C1 substrate — is never named as debt with an owner/action. M4. |
| :16 (argv half) | "…with a recheck argv." | The argv exists (`round-51.md:78-82`) but its recorded run ("run 2026-10-23 by the package") has no receipt; see `:643`. |
| :19 (command half) | "…the scanner contract and the command." | The collision check's command is never recorded — `round-51.md:60-67` names the pattern and the guard fixture, not an argv. |
| :389 | "A new gate ships its fixtures in the same round." | The C2 counter ships two control *transcripts*, not a fixture set with per-case expected values, and their input commits do not resolve (H1). |
| :461 | "A counter compares every field its expectation names, and judges a usage case on the usage object." | No usage object exists; the documented `2`/`64` exits are never returned and a bad revision is scored as a miss (M6). |
| :461 (C8 field) | "A counter compares every field its expectation names." | C8 names "the mirror's registry" but compares `corpus/SOURCES.md` at the mirror commit (`c51_quote_truth.py:277`), so the mirror blob is never opened; the contaminated mirror passes (H0). |
| :506 | "Every seat's end state is recorded." | No `seat-status.json` at `9d13768`; wave 1 had not settled. Not yet due, but not evidenced. |
| :512 | "A qualifier a source does not state is marked." | L2's clause is unmarked; L1's Baidu sentence is unattributed. |
| :541 | "(F4) Qualifier search within the cited sentence." | Same as `:512`: `canonical-selection.md:55` adds "a page with no declaration still gets one" to a sourced sentence without a mark. |
| :608 | "A cited artifact resolves from committed lane bytes, not a seat's sandbox." | `round-time-accounting.json` and the settlement named at `round-51.md:106-109` are absent at the citing revision (H3). |
| :627 | "A round's `## Gate` records at least one screened reject with its reason." | Check exits 1; rejects live under `## Refused entries` (H4). |
| :643 | "Every run a report cites ships a committed receipt." | Three cited runs have none: the collision check, the 2026-10-23 recheck commands, and the post-fix C2 re-run (H5). |
| :703 | "A declared target is out of reach of the cheapest do-nothing controls, scored with the frozen counter and committed before the build. The declaring round names its counter by sha256 …" | Controls are committed before the build, but the declaration names the counter by **path only** (`contract.json` `countingCommand`); `grep -c sha256 contract.json` = 1, and that one is condition C6 about receipts. The junk control is unreplayable (H1). |
| :824 and :864 (a) | "A knowledge counter refuses an inverted-facts entry and an unsourced entry." | No inverted-facts control exists. The unsourced shape is claimed (`c2-junk-entries.txt`) but unreplayable (H1), and its failure is `C2`/`C5`/`C8`, not a distinct unsourced-entry case. |
| :899 | "(d) Every cited commit hash resolves in lane history, or the citation names the bundle that contains it." | `d969fa28…` and `cc57cb80…` resolve nowhere and no bundle is named (H1). |
| :951 | "(l) A post-measurement receipt pins the measured tool bytes (revision and sha256, re-derivable from the revision)." | Control receipts carry no tool sha256 (H2). |
| :955 | "(m) Control receipts are committed before the build wave is dispatched." | Controls are committed before the entries, but the dispatch stamp is uncommitted (`wave-start-utc.txt`, `w51-taskcall.json` untracked), so the comparison cannot be made from committed bytes. |
| :1071 | "Receipt identity for filed counts (round 46). Any filed count or verdict against a receipt cites that receipt's path + sha256; a receipt citation without sha256 violates this criterion." | `LOG.md:2081-2083` restates "8 of 8", "fails 3 of 8", "0 of 8" with no receipt path and no sha256 (H5). |
| :1073 | "Verdicts carry committed receipts (round 47). A filed verdict-time gate result (exit code or tally) has its output committed as a receipt at the round it is claimed; prose restatement in a report or LOG is not the receipt." | Same as above (H5). |
| :1090 | "A wave citation carries its own grant (round 50)." | Grant and dispatch command are untracked at `9d13768` (M5). |
| :1100 | "A quote's match class is derived from its own two blobs, never asserted (round 50)." | Classes are asserted; `canonical-selection.md:37` contradicts `:41/:43`; `:60` carries no class; no derivation artifact exists (M1/M2). |

---

## 5. Criteria that do not apply to this round's artifacts

No artifact of the named class exists in this round, so these were read and set aside rather than
scored: `:15` absence annotation content; `:17` validator is not identity (no ETag/validator
claim); `:18` self-source confinement (no write-region checker); `:20` index continuity (no index
prose edited); `:317` conformance exceptions; `:328` field data; `:346`/:362 reason-code fixtures;
`:411` seat live-surface invocation (the fetch is L1-side, not a wave seat); `:493`/:500/:523/:529/
`:535` containment/closure commands; `:555`/:571` defence-in-depth and structured refusal codes;
`:590`/:658` repair-counter and lookup-control (C2 is an acquisition counter; the hollow-control
half is covered by `:307` and H1); `:769` retained-control quotation (no retained bundles);
`:797` gate registry rows (both counters live under `.ufo/waves/round-51/`, not `scripts/*.py`);
`:939`/:948`/:960`/:969`/:982`/:986`/:993`/:1001`/:1007`/:1023`/:1029`/:1035`/:1043` control
consequence, dead-seat routing, tool-byte pinning, control classes, sealed keys, routing of code
work to critics, witness identity, live tallies, fresh review, generated-class support;
`:1051`/:1059`/:1065` cost and sampling counters; `:1085` receipt exit labels; `:1086` residual
findings (no admission); round-28 `:317` no-harm (met above); round-31 `:506` is scored; round-36
(c)/(d)/(f) contract-bullet ablations and sealed polarity; round-37 (a)/(b)/(c)/(e)/(f)/(h)/(i)/(j)
sandboxes, key repair, coverage wording, polarity, control trees, fixture oracles; round-38 (j)/(k)/(n);
round-39 (o)/(p); round-40 (q)/(r); round-41 (s)/(t)/(u)/(n); round-42 (v)/(w)/(x); round-46 citation
reason fidelity; round-47 (a)/(b); round-49.

---

## 6. Per-entry content audit (what the entries actually establish)

### `corpus/knowledge/canonical-selection.md` (S262)

| Line | Claim / quote | Class | Verdict |
|---|---|---|---|
| 15-16 | "indicating a canonical preference is a hint, not a rule." | raw body substring | **supported** |
| 19-21 | "There are a handful of factors … rel=\"canonical\" link annotations." | collapsed-only (line breaks + `<a>`) | **supported**, label correct |
| 23-27 | "Google then chooses the page … objectively the most complete and useful for search users …" | collapsed-only (`<em>signals</em>`) | **supported**, label correct |
| 30-31 | "You can indicate your preference … for various reasons." | collapsed-only (`<a>`) | **supported**, label correct |
| 39 / 41 / 43 / 45 | four variant-class bullets | 2 raw-in-visible-text, 2 collapsed-only | **supported**, but the `:37` framing calls all four "raw" (M1) |
| 60 | "objectively the most complete and useful for search users" | raw body substring | **supported**, class unmarked (M2) |
| 55-56 | "A declared canonical can be ignored, and a page with no declaration still gets one." | first half sourced, second half inference | **half supported, unmarked** (L2) |
| 62-64 | S021 "how to specify", S022 "fix issues" | row titles, not body quotes | **defensible in the entry; breaks the lesson's universal claim** (M2) |
| 68-69 | "Baidu publishes a different account (a quality comparison)" | nothing in either body | **unsourced** (L1) |
| 77-78 | doc revision "Last updated 2026-08-20 UTC" read from the retained body | verified | **supported** |

### `corpus/knowledge/crawler-identity.md` (S263)

| Line | Claim / quote | Class | Verdict |
|---|---|---|---|
| 8-10 | "Googlebot is the generic name for two types of" | raw body substring, inside `<p>` | **supported**, correctly labelled raw; truncated before its object (note, not a defect) |
| 16 / 18 | "Googlebot Smartphone : …" / "Googlebot Desktop : …" | collapsed-only (`<b>` + line break) | **supported**, labels correct |
| 22-24 | "You can identify the subtype … in the request" | collapsed-only (`<a>`) | **supported**, label correct |
| 28-30 | "both crawler types obey the same product token (user agent token) in robots.txt" | collapsed-only | **supported**, label correct |
| 34-42 | consequences (log ambiguity, robots token cannot target one subtype, S096 is a parser) | local analysis + rows S011/S095/S096 | **supported**: S096 is `google/robotstxt`; S011 is RFC 9309; S095 is Google's robots interpretation |
| 46-55 | "does not establish" scope + doc revision "2026-02-03 UTC" | verified | **supported**, honest |

**Net content verdict:** every direct quote is a true substring of the retained bytes under one
consistent convention (raw HTML → tag-stripped → whitespace-collapsed), and both entries are
honest about not being live measurements. The freshness defects are in the *labels and locators*
(M1, M2, M7, L1, L2), not in fabricated quote text. No fabricated sentence survived — which is
the round's own stated mistake lesson (`round-51.md:76-88`) and it holds.

### Lesson (`corpus/lessons/round-51.md`)

- Gate lines (`:8-9`, `:10-11`) carry URL, access date, section, doc revision, quote, word count,
  class, sha256, byte count and HTTP 200 — strongest part of the artifact, and independently
  verified.
- `## Admitted entries` (`:18-30`) is accurate about both files being new and about the ground
  they add.
- `## Refused entries` (`:32-47`) gives located reasons for both refusals (duplicate-URL E04 for
  the Google half; un-re-grounded Baidu sources; covered ground for CrUX) — good content, wrong
  section for the `:627` check (H4).
- `## Stripped staged prose` (`:49-58`) records the two recheck commands and the reason the cells
  were normalized to `180d` — correct W04/E04-safe behaviour.
- `## Id collision check` (`:60-67`) is arithmetically correct (verified by set intersection) and
  the guard fixture genuinely catches a column-zero-only parser (`guard-registry.md` has an
  indented row; `guard-col0` is empty, `guard-collisions` = `S262`).
- `## Quarantine` (`:69-75`) is honest: 12 slice ids with reasons, "no quarantined id was
  hand-checked this round".
- `## Mistakes` (`:76-116`): the four routed-defect rows are well-formed (class/evidence/
  captured-by/fix), but the third and fourth `fix` sentences describe artifacts that do not exist
  at the revision (H3) and the C1 result is never recorded (M4).

---

## 7. Residual risk and verification gaps

1. **The printed 8/8 is seven real conditions plus one vacuous one.** C8 does not open the
   mirror (H0), so at most 7 of 8 conditions carry evidence. The conditions are also structural:
   they do not prove the quotes are *representative* of the pages, only present. My class table
   (§6) closes the presence question; representativeness remains a non-author read.
2. **My discrimination mutants are reviewer-side.** They show `c51_quote_truth.py` rejects a wrong
   Gate quote (`C5`), a mutated body (`C6`) and a wrong `used-by` (`C4`). They do not replace the
   round's own hollow control, which cannot be re-scored because its commit is absent (H1). I did
   not build an inverted-facts knowledge control (:824/:864) — that gap is real and unscored.
3. **The C1 instrument is unexercised on real wave bytes.** `c51_wave_ledger.py` returns 0/3 at
   both the base and the tip because no settlement exists; I could not evaluate whether its L1/L2/
   L3 comparisons are correct against a real settlement. Its predicate/condition wording does
   match the contract's, and it reads `git show`/`ls-tree` only, so the "committed bytes only"
   claim in its docstring is honest.
4. **`git clone --depth 50` was required for the mutant runs.** A depth-1 clone made `C8` fail
   falsely (the shallow root looks like the commit that "added" the mirror); the 8/8 baseline and
   all mutant deltas reported here come from the depth-50 clone, not the lane.
5. **No GitHub/live re-fetch was run** (not authorized and not needed): the HTTP 200 in
   `receipts.json` is the receipt's own claim; I verified the bytes and digests, not the status
   line. The retained bodies are the full pages, so the `abstract-only` risk is absent.
6. **The wave had not settled at measurement.** Seat end states, route probes, timing and the
   settlement are all post-settle artifacts; every finding about them is "not evidenced at
   `9d13768`", not "wrong". The one finding that would survive settle is the contract/lesson
   speaking in the present tense about artifacts that do not exist yet (M4/H3).
7. **The S262 locator defect (M7) is one of two highest-value fixes**: it is what a later recheck
   reads first, and it currently points at a `devsite-nav-title` span rather than the `<h1>` the
   content sits under. The other is H0, because it makes C2's own `after` sentence false while the
   counter prints green.
8. **The worktree moved under me during the review.** `assimilation/pre-append/corpus/SOURCES.md`
   is now modified in the worktree (the two rows removed), and
   `census-correction.txt`, `census-count-*.txt`, `quarantine-slice.{argv.txt,raw}` and
   `superseded/` appeared under `.ufo/waves/round-51/assimilation/`; a wave-1 sibling
   (`ExecRegistryDiff`) reported the same mirror contamination from the registry diff. I did not
   write any of those files and did not review them. Every verdict in this report is pinned to
   the committed bytes of `9d13768`; a corrected mirror committed later would need a fresh
   measurement, and the corrected file is not the bytes C2 scored.
