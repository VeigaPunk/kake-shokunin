# ConnW1 — evidence appendix (round 69 W1, kake lane)

Full transcripts behind `.ufo/waves/round-69/w1/ConnW1.md`. Base `4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4`.
Scratch `/fast/scratch/hyaku/kake-r69/ConnW1/` (removed on exit). No tool installed.

## E1 — Amendment 1 relabel rule vs the Scribe-drafted correction row

Amendment 1 (lane `git diff .ufo/waves/round-69/contract.md`, section "Amendment 1"):

> Relabel rule, exact: a mismatching pair is relabelled only if a line of `correction_locus` read at `--revision` matches
> `^\|\s*<correction_id>\s*\|\s*<observed integer>\s*\|` (exact id token and the re-derived integer).

Delivered counter, `.ufo/waves/round-69/w1/ExecC1Counter/c69_recorded_counts.py`:

```
221: def relabel_row(text, correction_id, observed):
224:      A mismatching pair is relabelled only when a line of the correction locus matches
226:         ^\|\s*<correction_id>\s*\|\s*<observed integer>\s*\|
233:      pattern = re.compile(r"^\|\s*" + re.escape(correction_id)
235:      return any(pattern.match(line) for line in text.splitlines())
```

Drafted table shape, `.ufo/waves/round-69/w1/ScribeC1Text.md:49-51`:

```
| Pair id | Recorded value | Revision | Re-derived value | Re-derived by | Note |
|---|---|---|---|---|---|
| `<pair id>` | `<recorded value>` | `<revision>` | `<re-derived value>` | `<command>` | `<one line: …>` |
```

Frozen pair (`.ufo/waves/round-69/c1/pairs.json`, id C1-02): `recorded_value 1`, `observed_value 2`, `match false`,
`correction_locus "corpus/lessons/round-69.md"`, `correction_id "C1-02"`. sha256 of the file:
`4e787bcb7b588416dbe4db5d76a2e263cf147c26f3faeecdf826f4c198a9e9be` (20 pairs) — matches the L1's
`.ufo/waves/round-69/amendment-1-note.md`.

Regex probe over the two candidate row shapes:

```
rx = re.compile(r"^\|\s*" + re.escape("C1-02") + r"\s*\|\s*" + "2" + r"\s*\|")
Scribe draft shape  "| C1-02 | 1 | 4b03efe1… | 2 | `git …` | … |"   -> NO MATCH
Amendment-1 shape  "| C1-02 | 2 | 4b03efe1… | … |"                  -> MATCH
```

End-to-end with the delivered counter and committed `c1/pairs.json` (scratch clone, two commits: base + correction row):

```
$ python3 -B .ufo/waves/round-69/c69_recorded_counts.py --root <clone> --revision <tip> \
      --pairs .ufo/waves/round-69/c1/pairs.json
# Scribe-drafted row
pairs=20 mismatches=1 relabelled=0 unrelabelled=1 met=false
pair C1-01 recorded=5 observed=5 status=ok
pair C1-02 recorded=1 observed=2 status=unrelabelled
EXIT=1

# Amendment-1 row shape
pairs=20 mismatches=1 relabelled=1 unrelabelled=0 met=true
pair C1-01 recorded=5 observed=5 status=ok
pair C1-02 recorded=1 observed=2 status=relabelled
EXIT=0
```

Also at the base revision with the surrogate pairs file (before `c1/pairs.json` existed):
`pairs=8 mismatches=1 relabelled=0 unrelabelled=1 met=false`, EXIT=1.

## E2 — kake census placement rules for C1's S436/S437 rows

Census source, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:611-621`:

```
if (!in_registry) {
  if (mode=="validate" && $0 ~ /^\|[ \t]*S[0-9]{3,}[ \t]*\|/) {
    id=trim($2)
    printf "%s\tE12\t%s row outside Registry section\n",lane,id
  }
  next
}
```

`in_registry` is set true only between a `## Registry` heading and the next `##`/`#` heading.

Fixture: scratch fleet root with `scripts` symlinked from the real fleet, `shokunin.conf` copied, and
`kake-shokunin` a `git clone --shared` of the lane checked out at `4d188f94`.

```
$ bash scripts/sources-census.sh validate --root <fleet> kake
kake  ok  <fleet>/kake-shokunin/corpus/SOURCES.md
CENSUS_EXIT=0     (16 W04 duplicate-url warnings, unchanged)
```

Placement trials on `corpus/SOURCES.md`:

```
(a) rows appended at EOF (after "## Leads (unopened)")
    kake  E12  S436 row outside Registry section
    kake  E12  S437 row outside Registry section
    EXIT=1

(b) rows inserted inside "## Registry" (immediately before "## Paths", line 184),
    used-by = corpus/lessons/round-69.md   (that file does not yet exist)
    kake  E11  S436 missing used-by corpus/lessons/round-69.md
    kake  E11  S437 missing used-by corpus/lessons/round-69.md
    EXIT=1

(c) rows inserted inside "## Registry", used-by = corpus/knowledge/freshness-sweep.md (exists)
    kake  ok  <fleet>/kake-shokunin/corpus/SOURCES.md
    EXIT=0     (W04 count still 16)
```

Section map of kake's `corpus/SOURCES.md` at base (`git show 4d188f94:corpus/SOURCES.md | grep -n '^#'`):
line 1 `# SOURCES — where kake learns`, 5 `## Registry`, 184 `## Paths`, 199 `## Search log`,
238 `## Leads (unopened)`. So the file's tail is outside the Registry, and "append two rows at the end" trips E12.

Precedent in the lane: `git log` commit `ce2ba654` (round-68) — "S435 row moved inside the Registry section
(census-after caught E12 'row outside Registry section', exit 1; the row had landed at the file tail)".

## E3 — cross-claim coupling: C1's corpus prose can turn C2's `offline_unchanged` false

`scripts/freshness-sweep.mjs` §paths (`scanCitations`, base lines 394-400) collects `SKILL.md` plus every
`corpus/**/*.md`, then resolves each `~`- or `/home/vgpnk`-prefixed cite and compares the miss set against
`pins.pathsMissSet`. The verdict line carries the counts:

```
$ node scripts/freshness-sweep.mjs --offline            # base clone, HOME=/home/vgpnk
VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)
EXIT=1

$ node scripts/freshness-sweep.mjs --offline --json
counts.drift=1  newMissing=['~/projects']
drift[0].unannotatedCites = ["corpus/lessons/round-66.md:69",
                             "corpus/lessons/round-66-verifier-spotcheck.md:101",
                             "corpus/lessons/round-66-verifier-spotcheck.md:102"]

$ node scripts/freshness-sweep.mjs --offline            # HOME = fake home with projects -> ~/Projects
ok=True code=0 drift=0 newMissing=0
EXIT=0
```

After adding `corpus/lessons/round-69.md` to the same clone:

```
C1 prose cites one unresolvable ~/ path:
  VERDICT: DRIFT — §paths: 2 unannotated miss · 2 NOT in pins.pathsMissSet (exit 1, partial: offline)
  -> offline_unchanged = false   (C2 red)

C1 prose cites no ~/ or /home/vgpnk path:
  VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)
  set-delta files: +4 / -0 — added: corpus/lessons/round-67-verifier-spotcheck.md ·
                           corpus/lessons/round-68-verifier-spotcheck.md · corpus/lessons/round-68.md ·
                           corpus/lessons/round-69.md
  -> offline_unchanged = true    (filesAdded is informational, not gating)

C1 prose quotes the pair's own command (git -C /home/vgpnk/Projects/shokunin/kake-shokunin show …):
  VERDICT unchanged -> offline_unchanged = true
```

Why the base is red here but the lane's receipts say exit 0 — `~/projects` (lowercase) is cited in
`SKILL.md:309,311` and five corpus files; it is in `pins.pathsCitedSet` but not in `pins.pathsMissSet`.
`corpus/lessons/round-66.md:69` records it as *recovered*, and the r68 receipt header shows the pinning host
was `C:\Users\jpvei\.zcode\workspace\…\kake-shokunin` — Windows, where `~/projects` resolves case-insensitively
to `~/Projects`. On this Linux host it does not exist, so it is a live unannotated miss. Amendment 1 already
replaced `offline_exit=0` with `offline_unchanged=true` for this reason.

## E4 — tmp literal counting

`git show 4d188f94:scripts/freshness-sweep.mjs | grep -n '/tmp'` → 20, 103 (both `//` comments), 108, 182,
899, 1204. Comment-classifier over the 1679-line base file: code lines containing `/tmp` = **4** (108, 182, 899,
1204); **3** if the bare-word `/tmp` at 899 is excluded. Under Amendment 1's pinned regex `['"\`]/tmp` the count
is **2** (108, 1204) — matching the contract prose "two sites".

Selftest red side, at base:

```
$ env -u KAKE_SELFTEST_DIR TMPDIR=$S/tmpd.XXXX HOME=$S/home.XXXX node scripts/freshness-sweep.mjs --selftest
selftest: 36/36 passed
EXIT=0
# TMPDIR dir: empty        <-- selftest_under_tmpdir = false
# fixture landed in: /tmp/kake-r16/selftest
```

`node -e "os.tmpdir()"` → `/tmp`; with `TMPDIR=` set → the set value, so `os.tmpdir()` is the S436/S437 route.

## E5 — C1 counter independence from C2

`grep -ci 'sweep\|freshness' .ufo/waves/round-69/w1/ExecC1Counter/c69_recorded_counts.py` → **0**.
The counter reads the pairs file, runs each pair's `command` via `subprocess.run(shell=True)`, and resolves
`correction_locus` with `git -C <root> show <rev>:<locus>`. Frozen pair paths: `corpus/knowledge/gate-status-ledger.md`
(7), `SKILL.md` (4), `corpus/knowledge/publish-queue.md` (5), `corpus/SOURCES.md` (4); one pair carries
`correction_locus: corpus/lessons/round-69.md`. No pair command touches `scripts/freshness-sweep.mjs`.
All 20 pair commands hardcode `git -C /home/vgpnk/Projects/shokunin/kake-shokunin` (absolute lane path).

## E6 — shokuknow merge package: quarantine and id-collision detail

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, kake data rows
(payload-absent table): S142, S143, S148, S156, S161, S193, S194, S195, S206 (9 — matches the "By lane" count
`kake | 9`); never-checked table: S154, S178, S184 (3). `MERGE-REPORT.json`: `accepted 129`, `refused []`,
`entries 104`, `existing_rows 145`, `renumbered []`, `first_id S287`.

None of the nine is held in the lane: `git show 4d188f94:corpus/SOURCES.md | grep -E '^\| (S142|S143|S148|S156|S161|S193|S194|S195|S206) '`
→ no match. The lane holds 173 rows, max id S435. Five of the nine sources are staged under new ids:
kimi FAQ → S292, CrUX methodology → S293, arxiv 2308.06409 → S298, `kimi.page/` → S302/S305/S306,
reduce-crawl-rate → S311.

Id collisions (`comm -12` over lane ids and `SOURCES.append.md` ids): S312 S329 S367 S372 S373 S374 S390 S409.
Lane S372 vs staged S372: same source URL, different text, 1157 B vs 1252 B, `cmp` → DIFFERENT.

Staged targets already existing in the lane: 12 of 104 — 6 flagged as amendments (js-rendering-queue,
canonical-selection, crawler-identity, crawl-budget-consequences, crawl-error-status-table,
dynamic-rendering-workaround-limits) and 6 unflagged, all `new-file` in the report but present with more content:
`yahoo-japan-link-target-crawl-restriction.md` 2417 B staged vs 10893 B lane;
`yahoo-japan-robots-txt-refusal-rules.md` 2350 vs 9866; `yahoo-japan-robots-pattern-syntax.md` 1876 vs 8300;
`yahoo-japan-rel-nofollow-semantics.md` 1748 vs 4545; `yahoo-japan-robots-txt-basics.md` 2491 vs 5661;
`yahoo-japan-deleted-url-recrawl.md` 2491 vs 9109, reported `collides_with_existing: false` — a false negative in
the package's own collision check.

## E7 — considerthese scan

Files read newest-first: `considerthese/2026-10-26.md`, `-25`, `-24`, `-23`, `-22`, `-21`, `-20`, `-19`.
Proposals in `2026-10-26.md` §Part 2 (lines 29-33). `git grep -ni 'gate-agreement' 4d188f94 -- LOG.md SCORECARD.md corpus/`
→ 5 hits, all dispositions of non-implementation (quoted in the report). `git ls-tree -r --name-only 4d188f94 |
grep -iE 'agreement|ledger'` → only `complete-ledger.json`, `frozen/ledger.json`, `CarryLedger.md` and unrelated
mutant-ledger fixtures. `considerthese/2026-10-25.md` proposal 3 (non-Latin locator sample) also not implemented
(`corpus/lessons/round-55.md:62`); proposal 4 of the 2026-10-26 file is the one with a recorded flip condition
already met (`corpus/lessons/round-64-verifier-spotcheck.md:62`).

## E8 — cross-lane note (tsukuroi r64 CRLF/E12 alarm)

Seat `SC2Census` reported `corpus/SOURCES.md` back to CRLF (381 CR, sha256 2349bfda141ab055, byte-identical to the
committed blob 2f3061ef) with census rc=1 E12=278, and asked for `sed -i 's/\r$//'`. That lane is
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (its `round-64/after/gates-recon.md` exists there and nowhere else;
blob 2f3061ef is not an object in the kake repo). Read-only check from this seat: tsukuroi's committed blob
`2f3061ef:corpus/SOURCES.md` → CR=381 sha256 2349bfda141ab055 (matches); tsukuroi's worktree file → CR=0,
sha256 e1558e4b3eeef885, `git status` → ` M corpus/SOURCES.md` — i.e. the L1 had already applied the CR strip.
SC2Census confirmed the timeline and attributed the repair to the lane L1. **Kake is not exposed**: kake's
`corpus/SOURCES.md`, `corpus/QUALITY.md`, `LOG.md`, `SCORECARD.md`, `SKILL.md` are CR=0 in both the worktree and
their HEAD blobs; the only CR bytes in kake's tracked files are inside binary
`.ufo/waves/round-26/fetched/*.raw.gz` payloads. No action taken in tsukuroi (out of this seat's write scope);
a reply with the measurements was sent to `SC2Census`.
