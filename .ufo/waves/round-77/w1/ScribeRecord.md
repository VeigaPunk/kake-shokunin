# ScribeRecord — round 77 / wave w1 / scribe (the report's own evidence)

Seat `ScribeRecord`, leaf. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`, frozen contract
`.ufo/waves/round-77/contract.md` at `bc2e5fb91e23c8acdac2470ac0f042c76f75417e` (lane `master` tip at
round open was `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`). No subagent was dispatched, no git mutation was
run, no tool was installed, and the only file I edited is `corpus/QUALITY.md`.

Convention in the delivered text below: `<rev>`, `<e>`, `<4-e>`, `<d>`, `<c>`, `<w>`, `<k>` and
`<scratch>` are the frozen contract's own field names and argv slots for the L1's measurements (contract
§C1/§C2 "Printed fields" and "Counting command"). Every other token is literal. Receipt files are pointed
at by directory (`.ufo/waves/round-77/controls/`, the contract's declared receipt home) except
`controls/base-c2-matrix.txt`, which the dispatched C2-matrix seat's item names literally; no receipt
filename is invented.

## 1. Behavior

1. Appended 49 lines to `corpus/QUALITY.md` under a new heading `## Round-77 criteria — the report's own
   evidence`: two named criteria (census-warning counts quoted whole; a report's evidence quotes obey the
   ledger's whole-line rule) with rule, admit/reject set and an able-to-fail command, plus the one
   revision-per-artifact line (round-76 D1 class). No earlier line of the file changed; no file under
   `corpus/` other than `QUALITY.md` was written.
2. Delivered ready-to-apply text in §4 (SCORECARD §Round 77: two claim rows in the round-76 table shape,
   plus the two capability rows the round enters if C2 lands), §5 (LOG §Round 77 in the round-76 entry's
   shape) and §6 (three append-only correction lines closing round-76 routed defects D4, D5 and D6, for
   `SCORECARD.md` and `corpus/lessons/round-76.md`).

## 2. Gates and observations

Read-only probes only; no lane gate was executed (that is the L1's step). Scratch
`/fast/scratch/hyaku/kake-r77/ScribeRecord` was created with `mkdir -p`, used with `TMPDIR=$S/tmp`, and
removed after the observations below were copied into this file.

| Command | Observed | Grounds |
|---|---|---|
| `git diff --numstat corpus/QUALITY.md` | `49	0	corpus/QUALITY.md` | the append is 49 added lines, zero removed: append-only conjunct holds |
| `git rev-parse HEAD` and `git rev-parse a2cc5f51…` | `bc2e5fb91e23c8acdac2470ac0f042c76f75417e`; `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68` | contract commit and base of the rows below |
| `git show a0491fcd:corpus/SOURCES.md > $S/SOURCES-base.md` then `TMPDIR=$S/tmp scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin --file $S/SOURCES-base.md > $S/census-base.txt` | exit 1; `grep -c 'W04' $S/census-base.txt` → `16` | base warning count |
| same with `git show a1b3f33b:corpus/SOURCES.md` (round-76 tip) | exit 1; `grep -c 'W04'` → `17` | round-76 tip warning count (the D2 class) |
| same with `git show a2cc5f51:corpus/SOURCES.md` (round-77 base) | exit 1; `grep -c 'W04'` → `17` | round-77 inherited count |
| `diff` of the two `W04` line sets (base vs round-76 tip) | one added line, verbatim: `file	W04	S445 duplicate url html.spec.whatwg.org/multipage/links.html across scopes` (fields tab-separated) | the one warning round 76 added |
| `grep -cF 'pages=8 findings=[] exit=0' .ufo/waves/round-76/controls/after-c2-realrun.txt` | `0` (exit 1) | the round-76 report's real-input span is no receipt substring (D3 class); the receipt is one JSON object line plus `rc=0` |
| `cat .ufo/waves/round-76/controls/after-c2-matrix.txt \| head -8` | line 4 is `revision=master revision_ok=yes head=d00ea7fb1471f66bf6067cd6fcb5d82c743159c8` | D1 class: the receipt labels a revision |
| `git cat-file -e d00ea7fb:scripts/hreflang_audit.py` | `fatal: path 'scripts/hreflang_audit.py' exists on disk, but not in 'd00ea7fb'`, exit 128 | that revision does not contain the artifact |
| `git cat-file -e 2cccd59a:scripts/hreflang_audit.py` | no output, exit 0 | the artifact exists at `2cccd59a` |
| `git grep -in hreflang a0491fcd -- PROVINCE.md corpus/README.md \| wc -l` | `0` | D5: no declared frontier row existed at base |
| `grep -n '^| [0-9] |' SCORECARD.md \| tail -5` | rows at `4925`–`4929`, five numbered rows | D4: the round-75 correction section holds five rows, not seven |
| `grep -n 'append_only' .ufo/waves/round-76/controls/ctl-deletion.txt` | lines `2,3,6,7` only (all four are `T1` lines); the `A1` line at `:8` has no `append_only=` token | D6: the round-76 deletion control prints `A1` only |
| `sed -n '8p' .ufo/waves/round-76/controls/ctl-deletion.txt` | `  A1 SCORECARD.md:0 claim row present at --base is gone at the measured revision` | D6 corrected statement |
| `git show a2cc5f51:corpus/SOURCES.md \| grep -c '^| S[0-9]'` | `184` (at `a0491fcd`: `181`) | row counts used in the LOG entry |
| `git show a2cc5f51:corpus/SOURCES.md \| grep -in 'rfc1952\|rfc4287'` | no matches | the round adds no duplicate URL, so no new `W04` |
| `grep -n '^#' corpus/lessons/round-76.md` | `1:# Round 76 …`, `20:## Claims`, `49:## Gate`, `88:## Mistakes`, `116:## Routed dispositions`, `137:## Sources` | finding F1: no `## Corrections` heading exists yet |

The `--file` census mode exits 1 on every blob I tried with `E11` missing-used-by rows that are unrelated to
the warning count; the `W04` line count, not the exit, is what the new criterion uses.

## 3. Touched surfaces

| Path | Change |
|---|---|
| `corpus/QUALITY.md` | appended 49 lines, new section `## Round-77 criteria — the report's own evidence` (lines 1535–1582); base lines 1–1533 byte-identical |
| `.ufo/waves/round-77/w1/ScribeRecord.md` | this report (new) |

Nothing else in the lane, the fleet root, another wave dir or a sibling repo was written.

## 4. Deliverable A — `SCORECARD.md` §"Round 77 — declared and measured claims"

Apply after §"Round 76 — corrections (appended round 77)" (§6 below), which must stay the round-76
section. The two claim rows are in the round-76 table's five-column shape; the capability section is
entered only if C2's frozen predicate measures `met`.

```markdown
## Round 77 — declared and measured claims (attempt 1; author-side, admission belongs to the closure)

Frozen contract `.ufo/waves/round-77/contract.md` (`bc2e5fb9`), frozen before any seat ran. Base
`a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`. Wave `w1`: one v1 wave, 14 seats (scout 2, executor 4,
scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1; attack share 4/14 = 28.6 %).
Scores unchanged: operability 10, freshness 10, calibration 2 (all HOLD; no scalar move).

| Claim | Axis | Before → after | Counting command | Verdict |
|---|---|---|---|---|
| C1 every `SHONEN.md` box classified from committed bytes | calibration 2→2 HOLD | base `a2cc5f51`: `C1 revision=<rev> boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=4 met=false`, exit 1 (contract §C1 base target; base receipt under `.ufo/waves/round-77/controls/`) → after `<rev>`: `C1 revision=<rev> boxes=4 evidenced=<e> gap=<4-e> unexamined=0 mismatches=0 met=true`, exit 0 (after receipt under `.ufo/waves/round-77/controls/`) | `python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . --revision <rev> [--work <scratch>]` | L1 fills `<rev>`, `<e>`, `<4-e>` and both receipt names; predicate frozen `met <=> boxes == 4 and unexamined == 0 and mismatches == 0`; every `evidenced` row re-derives its `observed` from committed bytes, and every `gap` row carries `reason` + `flip` rather than a tick |
| C2 sitemap container and format coverage (capability) | operability 10→10 HOLD (capability) | base `a2cc5f51`: `C2 revision=<rev> cases=20 decided=<d> correct=<c> wrong=<w> constants_failed=<k>/4 met=false`, exit 1 (`.ufo/waves/round-77/controls/base-c2-matrix.txt`) → after `<rev>`: `C2 revision=<rev> cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true`, exit 0 (after receipt under `.ufo/waves/round-77/controls/`) | `python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . --tool scripts/sitemap_audit.py --revision <rev> --cases .ufo/waves/round-77/cases --consts .ufo/waves/round-77/consts --work <scratch>` | L1 fills `<rev>`, `<d>`, `<c>`, `<w>`, `<k>` and both receipt names; predicate frozen `met <=> cases == decided and wrong == 0 and constants_failed == 4`; the four frozen constants each fail at least one case, and finding-id sets are compared, not exits alone |

Capabilities acquired in round 77 (entered when C2's frozen predicate measures `met`):

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Sitemap container and format coverage | Decides, offline and without fetching, whether a sitemap file is gzip-compressed (magic `1f 8b` whatever the name, the 52,428,800-byte limit applied to the decompressed bytes, a truncated stream as an input fault), a plain-text sitemap (one absolute URL per line, UTF-8, at most 50,000 URLs, no other line), an RSS 2.0 item (`<link>`, optional `<pubDate>`) or an Atom 1.0 entry (`<link href>`, optional `<updated>`), and keeps a sitemap index container-agnostic over `<loc>` targets of any of those formats; a document rooted at none of `urlset`, `sitemapindex`, `rss`, `feed` is `format_unsupported` (exit 2), never silently clean; the round-39 XML checks and the 0/1/2/64 exit alphabet are unchanged | `scripts/sitemap_audit.py` and `scripts/sitemap_audit_selftest.py`; matrix receipts `.ufo/waves/round-77/controls/base-c2-matrix.txt` and the after-state receipt under the same directory | 77 |
| Frozen container/format case matrix | Runs any same-CLI sitemap tool over the 20 frozen cases (gzip g01–g04, text t01–t07, RSS r01–r04, Atom a01–a03, index s01, unsupported d01) plus four degenerate constants (always-clean, report-every-id, empty-findings-with-real-exits, the round-39 XML-only tool) and requires every constant to fail at least one case, comparing finding-id sets and exits rather than exits alone | `.ufo/waves/round-77/c77_sitemap_matrix.py`, `.ufo/waves/round-77/cases/`, `.ufo/waves/round-77/consts/`, receipts under `.ufo/waves/round-77/controls/` | 77 |
```

## 5. Deliverable B — `LOG.md` §"Round 77 — 2026-11-03 (hyaku run 15; attempt 1; Linux host; claims frozen before any seat ran)"

```markdown
## Round 77 — 2026-11-03 (hyaku run 15; attempt 1; Linux host; claims frozen before any seat ran)

- **Frozen contract.** `.ufo/waves/round-77/contract.md` at `bc2e5fb91e23c8acdac2470ac0f042c76f75417e`,
  frozen before any seat ran: the C1 field line and `met` predicate, the C2 field line, predicate, 20-case
  matrix and four constants, and both kill rules. Base `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`.
- **Motivating evidence.** Calibration is the lane's lowest non-retired axis (score 2), and its four
  `SHONEN.md` boxes were classified by prose only: the round's counter must derive each box from committed
  bytes at one named revision, re-deriving every recorded observation rather than trusting it. Operability
  is the capability axis: the round-39 sitemap tool refuses the gzip container, the plain-text sitemap and
  the syndication feeds S012 names as sitemap formats, so three families of real sitemap bytes cannot be
  audited at all. The round-76 non-author closure routed six documentation/evidence-scope defects
  (`corpus/lessons/round-76-verifier-spotcheck.md` §6): D1 is repaired by the C2 re-run at an explicit full
  hash, D2 and D3 become the two `corpus/QUALITY.md` criteria of this round, and D4–D6 become the
  correction lines below.
- **Wave `w1`.** One v1 wave, 14 seats, band 8–16: scout 2, executor 4, scribe 2, reviewer 2, critic 1,
  mutation-tester 1, connector 1, sentinel 1; attack share 4/14 = 28.6 %; the L1 held the planner seat.
  Spec `w1-spec.json`, dispatch `w1-dispatch.json`, ready `w1.ready`, registry `w1/swarm-registry.json`.
- **C1 landed and measured.** `.ufo/waves/round-77/c77_shonen_ledger.py` classifies each of the four
  `SHONEN.md` boxes from committed bytes at the measured revision — a `path` check must exist at the
  revision, a `command` check is re-run or its committed receipt re-read — and prints one line; a counter
  that takes the ledger's `holds` flags as given is invalid (contract §C1 kill rule). Base `a2cc5f51`:
  `C1 revision=<rev> boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=4 met=false`, exit 1. After `<rev>`:
  `C1 revision=<rev> boxes=4 evidenced=<e> gap=<4-e> unexamined=0 mismatches=0 met=true`, exit 0 (receipts
  under `.ufo/waves/round-77/controls/`). `corpus/knowledge/shonen-ledger.json` carries one row per box; a
  `gap` row names its `reason` and the `flip` that would evidence it, and an `[x]` marker carries a named
  non-author `verifier`.
- **C2 landed and measured (capability).** `scripts/sitemap_audit.py` now decides the three families the
  round-39 tool refused — gzip (magic `1f 8b` regardless of name, the 52,428,800-byte limit on the
  **decompressed** bytes, a bounded read, a truncated stream as an input fault), plain text (one absolute
  URL per line, UTF-8, at most 50,000 URLs, no header/footer/comment line), RSS 2.0 (`<item><link>`,
  optional `<pubDate>`) and Atom 1.0 (`<link href>`, optional `<updated>`) — and keeps a sitemap index
  container-agnostic; a root that is none of `urlset`, `sitemapindex`, `rss`, `feed` is
  `format_unsupported` (exit 2). Matrix at base `a2cc5f51`: `C2 revision=<rev> cases=20 decided=<d>
  correct=<c> wrong=<w> constants_failed=<k>/4 met=false`, exit 1
  (`.ufo/waves/round-77/controls/base-c2-matrix.txt`); after `<rev>`: `C2 revision=<rev> cases=20 decided=20
  correct=20 wrong=0 constants_failed=4/4 met=true`, exit 0. The four frozen constants (always-clean,
  report-every-id, empty-findings-with-real-exits, the round-39 XML-only tool) each fail at least one case,
  and the matrix compares finding-id sets, not exits alone; `scripts/sitemap_audit_selftest.py` carries the
  round-39 cases plus the new format cases.
- **Frontier and sources.** `corpus/SOURCES.md` gains two rows over the 184 measured at `a2cc5f51`: S447
  (RFC 1952, the gzip container) and S448 (RFC 4287, Atom 1.0), both opened 2026-11-03, each with a
  ≤25-word located quote in `corpus/lessons/round-77.md` §Gate; S012 (`sitemaps.org/protocol.html`)
  re-opened 2026-11-03 (HTTP 200, 45,292 B, sha256 `5e757059…`), its `used-by` gaining the round-77 entry
  with old→new logged in the lesson. New entry `corpus/knowledge/sitemap-formats.md` cites
  S012/S447/S448, and `corpus/README.md` gains its coverage row. Census: the `a2cc5f51` blob prints 17
  `W04` duplicate-URL warnings and the `a0491fcd` blob 16 (`scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin --file <blob>` over `git show <rev>:corpus/SOURCES.md`, counted with
  `grep -c 'W04'`); the round adds no duplicate URL — neither `rfc1952` nor `rfc4287` occurs in
  `corpus/SOURCES.md` at `a2cc5f51` — so the round-end line carries the same 17, and the round-end census
  line is quoted whole in the round receipt per the new QUALITY criterion. Assimilation: none — the
  `merge/kake` package's staged ids S287–S415 sit below the registry tip and are occupied by different
  rows, re-checked read-only this round (`w1/ConnectorC.md`), and no `considerthese/2026-10-26.md`
  proposal is mined because all five are already implemented (r58, r66, r72 and report practice).
- **Mistake mined.** (i) A round's report restated a pre-round warning count as the round-end count: the
  round-76 report said the tip census carried "same 16 pre-existing `W04` duplicate-URL warnings,
  unchanged" (`.ufo/reports/round-76/kake.md:130`) while the tip prints 17, the round's own S445 row adding
  one — `.ufo/waves/round-76/controls/` receipts and `corpus/lessons/round-76-verifier-spotcheck.md` §6.2;
  captured by the non-author closure; fixed as the QUALITY criterion "Census-warning counts are quoted
  whole". (ii) A report's evidence span was a rendering, not a quote: `pages=8 findings=[] exit=0`
  (`.ufo/reports/round-76/kake.md:34`) is a space-joined selection of the fields in the one JSON line of
  `controls/after-c2-realrun.txt` plus `rc=0` (§6.3); fixed as the QUALITY criterion "A report's evidence
  quotes obey the same whole-line rule as the ledger's". (iii) A receipt named a revision that does not
  contain the artifact it measures: the round-76 matrix receipt's `revision=master revision_ok=yes
  head=d00ea7fb…` line, where `git cat-file -e d00ea7fb:scripts/hreflang_audit.py` fails (§6.1); fixed by
  this round's re-run at an explicit full hash and by the QUALITY line that a receipt names one revision
  per artifact and that revision must contain the artifact's bytes.
- **Corrections (round-76 closure D4/D5/D6).** Three append-only correction lines land in `SCORECARD.md`
  §"Round 76 — corrections (appended round 77)" and `corpus/lessons/round-76.md` §"Corrections (appended
  round 77)": D4 the seven closed findings are five `SCORECARD.md` rows + one `corpus/QUALITY.md`
  criterion + one `corpus/lessons/round-75.md` bullet (5 + 1 + 1), not seven rows in `SCORECARD.md`; D5
  hreflang declarations entered from unlisted ground, not from a declared frontier row
  (`git grep -in hreflang a0491fcd -- PROVINCE.md corpus/README.md` → 0); D6 the round-76 deletion control
  prints `A1` and carries no `append_only=` field.
- **Routed (not claimed).** The open L0 `kake | round-69` lowercase `~/projects` case still governs the
  freshness sweep and no round-77 seat touches it; SHONEN markers and any promotion stay author-side
  (promotion is operator-owned); the sitemap-format entry's quotes rest on this round's fetches, retained
  under the wave dir, and no re-fetch is claimed; no behaviour outside the 20 frozen C2 cases is claimed
  (compression other than gzip, feed versions other than RSS 2.0/Atom 1.0, and fetching a `<loc>` target
  are outside the matrix).
- **Not done this round.** No publish or deploy; network reads were confined to the public documentation
  URLs the contract's frontier step and C2 seats name (S012, RFC 1952, RFC 4287); no operator-owned
  property fetched; no MANIFEST edit; no tool installed or upgraded; pacman untouched; no scalar score
  moved.
```

## 6. Deliverable C — three append-only correction lines (round-76 D4/D5/D6)

### C.1 For `SCORECARD.md` (new section after the round-76 section)

```markdown
## Round 76 — corrections (appended round 77)

`[r77-correction 2026-11-03]` Three append-only correction lines close the round-76 non-author closure's
routed defects D4–D6 (`corpus/lessons/round-76-verifier-spotcheck.md` §6). No earlier line of this file is
rewritten; the same three lines land in `corpus/lessons/round-76.md` §"Corrections (appended round 77)".
Line breaks inside the quoted prose are collapsed to single spaces; no word is added or dropped.

1. **D4 — the seven closed findings are 5 + 1 + 1, not seven rows in `SCORECARD.md`.** The defective
   wording is “closed by seven whole-line correction rows in `SCORECARD.md` §"Round 75 — quote corrections
   (appended round 76)", one `corpus/QUALITY.md` criterion and one `corpus/lessons/round-75.md`
   §Corrections bullet” (`.ufo/reports/round-76/kake.md:27-29`), “closed by seven whole-line correction
   rows in the section above, one QUALITY criterion and one lesson correction” (this file, the round-76 C1
   claim row) and “The repair lands seven whole-line correction rows in `SCORECARD.md`, one
   `corpus/QUALITY.md` criterion and one `corpus/lessons/round-75.md` correction” (`LOG.md:2563-2564`).
   Corrected: §"Round 75 — quote corrections (appended round 76)" holds **five** numbered correction rows
   (`SCORECARD.md:4925-4929`), and the remaining two of the seven base findings are closed by **one**
   `corpus/QUALITY.md` criterion and **one** `corpus/lessons/round-75.md` §Corrections bullet — 5 + 1 + 1.
2. **D5 — the area entered from unlisted ground, not from a declared frontier row.** The defective wording
   is “hreflang declarations entered from frontier to core” (`.ufo/reports/round-76/kake.md:135`).
   Corrected: base `PROVINCE.md` and `corpus/README.md` hold no hreflang row — `git grep -in hreflang
   a0491fcd -- PROVINCE.md corpus/README.md` prints nothing (0 lines) — so there was no frontier row to
   advance from; the area entered from unlisted ground, and `PROVINCE.md` §"Round-76 hreflang frontier
   step" moving it to Core, with its boundary, is accurate and stands.
3. **D6 — the round-76 deletion control prints `A1` only.** The defective wording is “deletion (`A1`,
   `append_only=false`)” (`.ufo/reports/round-76/kake.md:38`). Corrected: the committed round-76 control
   line is `.ufo/waves/round-76/controls/ctl-deletion.txt:8` —
   `A1 SCORECARD.md:0 claim row present at --base is gone at the measured revision` — and the file carries
   no `append_only=` token on that line (the field appears only on its four `T1` lines, `:2`, `:3`, `:6`,
   `:7`); `append_only=false` belongs to the round-75 control `ctl-deletion-landed.txt`, not to this one.
```

### C.2 For `corpus/lessons/round-76.md` (appended end-of-file section)

```markdown
## Corrections (appended round 77)

`[r77-correction 2026-11-03]` Three append-only correction lines close the round-76 non-author closure's
routed defects D4–D6 (`corpus/lessons/round-76-verifier-spotcheck.md` §6); no earlier line of this lesson is
rewritten, and the same three lines land in `SCORECARD.md` §"Round 76 — corrections (appended round 77)".

- **D4.** “closed by seven whole-line correction rows in `SCORECARD.md` …, one `corpus/QUALITY.md`
  criterion and one `corpus/lessons/round-75.md` §Corrections bullet”
  (`.ufo/reports/round-76/kake.md:27-29`) is corrected to 5 + 1 + 1: `SCORECARD.md:4925-4929` holds five
  numbered rows, and one `corpus/QUALITY.md` criterion plus one `corpus/lessons/round-75.md` bullet close
  the other two of the seven base findings. The same correction applies to this file's §Mistakes row on
  the whole-line rule and to `LOG.md:2563-2564`.
- **D5.** “hreflang declarations entered from frontier to core” (`.ufo/reports/round-76/kake.md:135`) is
  corrected to “entered from unlisted ground”: base `PROVINCE.md`/`corpus/README.md` hold no hreflang row
  (`git grep -in hreflang a0491fcd -- PROVINCE.md corpus/README.md` → 0), so no declared frontier row
  existed; the PROVINCE move to Core is accurate as written.
- **D6.** “deletion (`A1`, `append_only=false`)” (`.ufo/reports/round-76/kake.md:38`) is corrected to
  `A1` only: `.ufo/waves/round-76/controls/ctl-deletion.txt:8` reads `A1 SCORECARD.md:0 claim row present
  at --base is gone at the measured revision`, with no `append_only=` token on that line.
```

## 7. Findings and limits

- **F1 (pointer, not repaired by text).** `corpus/lessons/round-76.md` has no `## Corrections` heading
  (headings: `Claims`, `Gate`, `Mistakes`, `Routed dispositions`, `Sources`), yet routed-disposition rows 3
  and 7 and one Mistakes row point at “this lesson §Corrections”; the Mistakes cell at line 94 also ends
  mid-token — it ends with the words “one lesson”, then a backtick, then “## Corrections”, with no closing
  backtick and no full stop (byte read of the line's last 320 characters). C.2 supplies that heading at
  end-of-file, which makes those pointers resolve; the heading alone does not re-derive the stale-digest or
  C2-scope corrections they claim, so nothing here should be read as their repair.
- **F2 (measurement mode).** `scripts/sources-census.sh validate --file <blob>` exits 1 on every
  committed `SOURCES.md` blob I ran (base, round-76 tip, round-77 base) with `E11` missing-used-by rows.
  The blob mode is a deterministic `W04` count oracle, not a clean-run oracle, and criterion 1 says so
  in its able-to-fail note.
- **F3 (D4 occurrence set).** The count defect appears in three files, not the two the routed text names:
  the fleet report (`:27-29`), the round-76 C1 claim row in `SCORECARD.md` (`:4942`) and `LOG.md:2563-2564`
  (verified by fixed-string search for `seven whole-line`). The lesson's Mistakes cell says “whole-line
  correction rows in `SCORECARD.md` … one QUALITY criterion, one lesson `## Corrections`, which is
  consistent with 5 + 1 + 1 and is not a count defect; its defect is the missing heading and the
  unterminated cell (F1).
- **F4 (scope of the row shapes).** The C1/C2 before→after cells carry only what the contract froze; the
  after-state field values, the printed revision and the receipt filenames are the L1's to fill. I did not
  invent a receipt filename: the C2 base receipt `controls/base-c2-matrix.txt` is the one the dispatched
  matrix seat's item names, and every other receipt is pointed at by the contract's receipt directory.
- **F5 (conditional section).** The capability table is entered only if C2's frozen predicate measures
  `met`; if C2 does not land, apply the C1 claim row alone (the C2 claim row records its own before-state
  and `met=false`).
- No score is moved by this seat: calibration stays 2, operability 10, freshness 10, all HOLD. Nothing here
  admits either claim; admission belongs to the closure.

## 8. Out of scope (not done)

No edit to `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/**`,
`scripts/**`, `.ufo/state/`, `MANIFEST.json`, any other wave dir, the fleet repo or a sibling lane; no
commit, push, or other mutating git/jj verb; no subagent dispatch; no `agent://all` message; no network
request; no tool install or upgrade; no `/tmp` evidence path.
