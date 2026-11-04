author: hyaku closure (non-author integrator, @m_zfl)

# Round 77 — non-author verifier spot-check (kake)

Lane `kake`, round 77 (hyaku run 15, attempt 1). I did not author this round and did not improve it.
Base `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`; lane tip `bb2f8edac2e1d0bc102545a0ffa56871410e21b0`.
Report `.ufo/reports/round-77/kake.md` (fleet commit `0d758465`, author `kake-shokunin
<kake@shokunin.local>`). Every command below ran read-only over committed bytes (`git show <rev>:<path>`,
`git ls-tree`, `git merge-base --is-ancestor`); no lane gate or selftest was executed (PROTOCOL §Gate
standard, *Closure consequence*), so each claim is labelled **re-measured** (my own plain count over
committed bytes) or **evidence-verified** (the instrument's committed receipt, its self-test tally and
the revision it measured).

Driver digest (`.ufo/watchdog.log`, mutable — copied, not the live-line pointer):

```
2026-11-03T22:31:48-03:00 launch kake round=77 pgid=939068 driver=hyaku-inline attempt=1
2026-11-03T23:08:54-03:00 complete kake round=77; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Ruling |
|---|---|---|---|
| Report identity | `git log --format='%an %H %s' -- .ufo/reports/round-77/kake.md` | one commit: `kake-shokunin <kake@shokunin.local> 0d758465 round-77: kake report` | conform |
| Filing order | `git log -1 --format=%cI` on report and lane tip | report `0d758465` 23:08:02, after tip `bb2f8eda` 23:07:01; report cites `bb2f8eda`; fleet `origin/master` contains `0d758465` | conform — lands last |
| `SHONEN` heading | `grep -c '^## SHONEN'` and the box lines | `1` heading; four box lines `[~]`, `[ ]`, `[~]`, `[~]`, one per `SHONEN.md` box | conform |
| Cited lane commits | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> refs/heads/master` for `a2cc5f51 bc2e5fb9 893b0f33 3db64e09 b5a0053c 444ee748 b946acf9 3d9239ed c7f1fba3 bcbe4694 bb2f8eda` | 11/11 exist; 11/11 ancestors of `master` | conform — no dead or orphaned hash |
| Worktree / push | `scripts/hyaku/jj-lane.sh state …/kake-shokunin`; `git -C … status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=bb2f8eda remote=bb2f8eda ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote` prints `bb2f8eda…` | conform — no uncommitted round work |
| Prompt contract | `difflib` of `templates/round-prompt.md` (140 lines), rendered for kake/77/fleet, vs `.ufo/prompts/kake-round-77.md` lines 1–140 | one hunk, `{{AXES}}` → `operability + freshness (web properties and publishing)`; §6 hyaku addendum and §7 follow; report path, commit-before-report, `SHONEN` heading, hash-citation and write-scope items present | conform — template contract carried |
| Prompt durability | `git log -1 --format='%an %cI' -- .ufo/prompts/kake-round-77.md` | `kake-shokunin 2026-11-03T22:31:47-03:00`, one second before the launch line | conform |
| Axes / route map | `grep '^kake' shokunin.conf`; prompt §6; `~/.omp/agent/config.yml` `agentModelOverrides` | axes line matches the prompt; §6's net map (reviewer `@m_zfl`, every other role `@m_flash`) equals the live overrides; MISSION.md's role-class table is explicitly advisory | conform — no bucket contradiction |
| Wave | `.ufo/waves/round-77/w1-results.json`, `w1-dispatch.json`, `w1/*.md` | `seats=14`, 14 results, 0 empty outputs; scout 2 / executor 4 / scribe 2 / reviewer 2 / critic 1 / mutation-tester 1 / connector 1 / sentinel 1; one task call (`resumeSends=[]`); attack 4/14 = 28.6 %; 14 seat reports on disk; the L1 holds the planner seat | conform — L2 floor 8 met, no dead seat |
| Marker test | real report: two checkable claims, 11 cited lane hashes, evidence pointers | — | not a marker → status `ok` |

## 2. Claim re-checks

### C1 — calibration: every SHONEN box classified from committed bytes (score 2 HOLD)

- **Re-measured.** I implemented the five documented measures from their descriptions over
  `git show 3db64e09:` blobs — not with the lane's counter — and reproduced every `observed` value in
  `corpus/knowledge/shonen-ledger.json`: `b1-ids` 77 ids / 77 resolved / 0 unresolved; `b1-tables` 18
  (of 38 table blocks, 18 have ≥3 data rows); `b1-registry` 105; `b1-checklist` 1; `b2-rounds` 56
  (`^## ` lines matching `(?i)round ?0*\d+`); `b2-receipts` 98 distinct `.ufo/waves/round-N/…` file
  tokens; `b2-missing` 1; `b3-scripts` 0 missing of 112 script/counter tokens; `b3-invocations` 0
  missing of 90 `python3 -B` targets; `b4-lanes` 0 cross-lane citations across the 64
  `corpus/knowledge/*.md` files at the carrier (69 files in the directory).
- **Base.** `git cat-file -e a2cc5f51:corpus/knowledge/shonen-ledger.json` fails (no ledger), so the
  four boxes are unexamined; the base receipt prints the Amendment 2 A1 line
  `C1 revision=a2cc5f51… boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=0 met=false`, exit 1.
- **After.** Carrier `3db64e09`: `boxes=4 evidenced=3 gap=1 unexamined=0 mismatches=0 met=true`, exit 0.
  The gap is box 2: `.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt` is absent at
  `a2cc5f51`, `3db64e09` and `bb2f8eda` (`git cat-file -e` ×3) and `LOG.md:1811` names it.
- **Controls / byte binding (evidence-verified, not executed).** `ctl-c1-fake-ledger.txt` prints
  `boxes=4 … mismatches=4 met=false`, exit 1 — a fabricated `observed` (999) is caught (the receipt
  prints three of its four `observation-differs` lines; the mismatch count is the claim and it is red).
  Counter digest `2d66e5af…`, ledger `7962018b…` and checklist `6a166f19…` are the blobs at `3db64e09`
  and still at `bb2f8eda`; the seat receipt `w1/ExecShonenLedger.md:145` prints `selftest: 26/26
  passed`; the carrier parses (`ast.parse`) while `893b0f33` raises `SyntaxError` at line 988, exactly
  the carrier-supersession receipt's claim; the carrier has 26 `cases.append(Case(` entries.
- **Verdict: improved.** Base red is `unexamined=4`; after is a full classification with every
  observation re-derived, one named gap, zero mismatches. Score stays HOLD 2 (no scalar claimed).

### C2 — operability: sitemap container and format coverage (score 10 HOLD; capability)

- **Re-measured inventory.** `ls -d .ufo/waves/round-77/cases/*/ | wc -l` → 20 (each with
  `expect.json`); 4 constants; the cases cover gzip `g01–g04`, text `t01–t07`, RSS `r01–r04`, Atom
  `a01–a03`, index `s01`, unsupported `d01`. The expectation families read `gzip_invalid`,
  `text_line_not_url`/`text_url_not_absolute`/`text_empty`/`text_too_many_entries`,
  `feed_item_missing_link` and `format_unsupported`; each new id occurs 0 times in the base tool and
  ≥1 time in the carrier tool (`grep -c`).
- **Byte binding.** `git show 3db64e09:scripts/sitemap_audit.py | sha256sum` = `f767af77…`, the
  receipt's `tool sha256 at carrier`; `a2cc5f51:scripts/sitemap_audit.py` = `914ebdee…`, the receipt's
  base digest, and `consts/round39_xml_only.py` is byte-identical to it, so the XML-only constant is
  the base tool itself. Matrix instrument `5c6eacba…` and case generator `d4a67274…` are the committed
  blobs named in the receipt.
- **Before.** `base-c2-matrix-v2.txt` prints `cases=20 decided=20 correct=2 wrong=18
  constants_failed=4/4 met=false`, exit 1; the committed `base-c2-matrix.json` marks exactly `g04` and
  `s01` correct; the after receipt's `round39_xml_only` constant fails 18 ids (all but those two),
  which reproduces the base's 2/20 from the other side.
- **After.** `after-c2-matrix.txt` prints `cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4
  met=true`, exit 0; the four constants fail 12, 10, 20 and 18 cases (each ≥1).
- **Delivered selftest (evidence-verified, not executed).** `w1/ExecSitemapFormats.md:85` gives the
  exact command and `PASS 271/271`, exit 0; `w1/MutC.md:51` records the same on the delivered tool;
  `w1/CriticC.md:379` records `PASS 235/235` at the base. The case declarations confirm the delta:
  `grep -c 'add("r77_'` 0 → 36 and `grep -cE 'add\("'` 173 → 209, i.e. +36 = 271 − 235.
- **Verdict: improved** (capability acquisition; operability 10 HOLD, no scalar claimed).

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | **improved** | base `unexamined=4 met=false` → carrier `unexamined=0 mismatches=0 evidenced=3 gap=1 met=true`; my independent re-derivation matches all 12 recorded observations; the cheap-fake control is red at `mismatches=4` |
| operability | **improved** | matrix 2/20 → 20/20 decided correct with 4/4 constants failing; carried tool digest `f767af77`; delivered selftest 235 → 271 with 36 new declarations |
| coverage | unchanged | the tool and entry extend the governed ground, but `PROVINCE.md` and `corpus/README.md` were not edited (`git diff --name-only a2cc5f51 bb2f8eda -- PROVINCE.md corpus/README.md` → empty); `PROVINCE.md:342` still lists gzip and text/RSS sitemaps as "Still open" and the README's untouched-ground list (line 161) still holds them — routed defect 2 |
| depth | unchanged | no depth claim; the round adds an entry and two registry rows, and no owned depth score moved |
| freshness | unchanged | S012 re-opened 2026-11-03 and S447/S448 opened (live bytes re-fetched byte-identical, §4); the single `~/projects` drift stays open (L0 `kake \| round-69`); no knowledge entry left unmarked |
| adjacency | unchanged | the connector re-measured sibling overlap (audio `count_checklist.py`, kasegi `shonen-form.py`) and adopted nothing from `merge/kake`; no sibling scope absorbed |

No axis is harmed: `git diff --numstat a2cc5f51 bb2f8eda -- LOG.md SCORECARD.md corpus/QUALITY.md
corpus/SOURCES.md SHONEN.md` → `66/0 38/0 49/0 3/1 7/3` — the only removals are the SHONEN marker
rewrite and the S012 `used-by` in-place update the contract allows; no axis score decreased.

## 4. Discernment spot-check (LEARNING.md — non-author)

All three admits and all four rejects were re-opened; none needed sampling. Live re-fetches during
this closure (2026-11-04 UTC) returned exactly the retained bytes: `rfc1952.txt` 25,037 B sha256
`164ef089…`, `rfc4287.txt` 81,922 B sha256 `3bd71d76…`, `protocol.html` 45,292 B sha256 `5e757059…` —
the digests the Gate, the registry rows and the retained `.raw` files carry.

| Item | Decision | Source re-opened | Agree? | Reason |
|---|---|---|---|---|
| S012 (re-opened) gzip / decompressed limit | admit | live `https://www.sitemaps.org/protocol.html` (HTTP 200, 45,292 B, sha256 `5e757059…` = retained `protocol.raw`); quote at `protocol.raw:693-695` | **agree** | the 11-word quote "the sitemap file once uncompressed must be no larger than 50MB" is contiguous at raw 693–695; the row's tier-A scope (sitemap location and limits) matches, and the entry attributes only the uncompressed-limit reading to it |
| S447 RFC 1952 | admit | live `https://www.rfc-editor.org/rfc/rfc1952.txt` (25,037 B, sha256 `164ef089…`); quote at `rfc1952.raw:291-292` | **agree** | the 22-word quote ("These have the fixed values ID1 = … ID2 = … gzip format.") is contiguous at raw 291–292; tier A is right for the container framing |
| S448 RFC 4287 | admit | live `https://www.rfc-editor.org/rfc/rfc4287.txt` (81,922 B, sha256 `3bd71d76…`); quote at `rfc4287.raw:1159-1161` | **agree** | the 14-word href sentence is at raw 1159–1161; the row scopes Atom 1.0 `link`/`updated` only |
| "the decompressed-size limit applies to text and feed bodies" as a sourced fact | reject | `protocol.raw`: the "once uncompressed" clause is at 693–695 (sitemap section); the text-file bullet (rendered `protocol.txt:526-543`) says "must be no larger than 50MB … can be compressed" with no uncompressed clause; the feed section states no size limit at all | **agree** | S012 does not state the rule for text/feed bodies; the entry and the tool docstring present it as the lane's reading, with the flip condition |
| feed-date validity as a sourced rule | reject | `protocol.txt:511-515` | **agree** | S012 names `<pubDate>`/`<updated>` as "optional" and fixes no grammar; the entry calls ISO-8601/RFC 822 a lane policy and records both edges (RFC 822 pinned only by the selftest; date-only `<updated>` accepted against S448 §4.2.6) |
| "no comment line" as S012's words | reject | `grep -in comment protocol.txt` → no hits; `protocol.txt:518-523` | **agree** | the word "comment" occurs zero times; the MUST is "The text file must have one URL per line"; the entry grounds `text_line_not_url` there |
| `format_unsupported` as a protocol rule | reject | `grep -inE 'unsupported\|exit code' protocol.raw` → 0 | **agree** | no S012 line names an unsupported format or an exit alphabet; the entry labels it a lane convention and a check error |

New `corpus/SOURCES.md` rows: S447's Gate quote is 22 words at `rfc1952.raw:291-292`; S448's is 14
words at `rfc4287.raw:1159-1161`; both ≤25 and re-found in the digest-bound retained bytes. S012's
`used-by` change is logged old→new in the lesson's §Corrections.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → `kake ok`,
exit 0, 186 rows, 17 `W04` duplicate-URL warnings (16 inherited + S445). The base blob carries 184 rows
and all 17 flagged ids, and neither new URL appears in any other row, so the base count is 17 as well
and the two new rows add no duplicate.

Result: 7 of 7 sampled decisions agree (3 admits, 4 rejects); no disagreement to learn, and no
decision rests on a source I could not re-open.

## 5. Trend verdicts

- **expansion — improved (qualified).** One admitted `knowledge/` entry on ground the coverage map did
  not hold: `corpus/knowledge/sitemap-formats.md`, knowledge `.md` files 63 → 64, citing S012 (mined,
  re-opened) and S447/S448 (new tier A, opened this round); registry 184 → 186. The ground was declared
  open at base (`corpus/README.md:161`, `PROVINCE.md:342`). Qualified: the README coverage map and the
  PROVINCE frontier line were not updated (routed defect 2), so the report's "frontier rows advanced"
  sentence overstates the file state.
- **quality — improved.** The new entry's quotes re-found in live and retained bytes; the round-76
  receipt-drift class repaired by a full-hash rerun (`r77-hreflang-matrix.txt`,
  `tool_sha256=0762452f…` = the blob at `a2cc5f51`); C1's every observation now re-derived; C2's
  selftest 235 → 271 and matrix 2/20 → 20/20; 20 mutants with 19 killed and the one survivor named with
  its reachable path. No admitted entry was found false or stale without a mark.
- **discernment — improved.** The Gate records three admits and four rejects with flip conditions and
  no quote over 25 words; this outside spot-check agrees on all 7; the round's own recon froze ten
  ambiguities and two counter holes as terms-only amendments before any after-state. Qualified: the
  security-review paragraph and the lesson's open list repeat a pre-final SentinelC snapshot (routed
  defect 1), a report-accuracy defect rather than a gate disagreement.

## 6. Routed defects (status-neutral; the lane fixes them next round)

1. **SentinelC status list is stale in the report and the lesson.** The committed
   `.ufo/waves/round-77/w1/SentinelC.md` marks F2/F3/F4 **closed at `f767af77…`** (the carried tool) at
   lines 68/93/109, and F5/F6/F7/F8 open; the report's "Security review" bullet lists "five open
   read/denial/integrity classes (lexical manifest containment, FIFO denial, unbounded manifest read,
   `--revision` label forgery, `--tool-revision` option injection)" and the lesson's "Open, not claimed
   closed" paragraph names F2–F6. Correct append-only in the next lesson (and a report erratum): F2–F4
   are closed at the carrier's `_resolves_inside` / `O_NONBLOCK` / `MAX_MANIFEST_BYTES`; F5–F8 are open.
2. **`PROVINCE.md` and `corpus/README.md` were not updated.** `git diff --name-only a2cc5f51 bb2f8eda
   -- PROVINCE.md corpus/README.md` is empty, yet the report says "`PROVINCE.md`'s sitemap line … loses
   gzip and text/RSS sitemaps to held ground". The file still reads "Still open: gzip, live fetch,
   text/RSS sitemaps, …" (`PROVINCE.md:342`) and the README's untouched-ground list still holds the
   same ground, with no coverage row for `sitemap-formats.md`. Update both and correct the report's
   frontier sentence.
3. **Box 4's population count.** `SHONEN.md` box 4 and the report's SHONEN line say "0 of 63
   `corpus/knowledge/*.md` entries"; the measured carrier has **64** `.md` entries
   (`git ls-tree -r --name-only 3db64e09 corpus/knowledge | grep -c '\.md$'` → 64). The observation
   (zero cross-lane citations) is right; the count is the base population. State 64 (or "63 at base,
   64 at the carrier").
4. **SentinelC's F1 closing bytes are not in the repo.** The review's closing hash `00cb4fb2…` (and
   the intermediates `a9eef8bd…`, `9612baac…`) never committed; the only committed ledger counters are
   `2d66e5af…` (carrier and tip) and the broken `7f35ad45…` at `893b0f33`. The sentinel itself says
   nothing transfers to another hash. The closure is substantively present in the carrier (no
   `_run_command`, `command` kind rejected at `c77_shonen_ledger.py:449`, selftest fixture `a5-04`), but
   the receipt must name the committed blob: re-cut it on `2d66e5af…` or record the build split.
5. **Round-level `doc_quote_truth` run has no committed receipt.** The report and `LOG.md:2669` quote
   `C1v2 revision=b946acf9 rows=38 receipt_files=8269 spans=58 exempted=0 corrections=2 findings=0
   met=true`, but no `controls/` file carries that run (unlike the C1/C2 controls). Commit its stdout
   under `.ufo/waves/round-77/controls/` or mark the span as author-quoted, so the round's own QUALITY
   criterion 2 (report evidence = a committed receipt line) does not fail on its own report.
6. **Minor — amendment line citation.** Amendment 1 A1 cites "lines 177–180 of the retained stripped
   text"; the retained `protocol.txt` has the sentence at 353–357 and the entry cites
   `protocol.raw:693-695` (the correct raw range). Name one rendering in the amendment's correction.

## 7. Status

`CLOSURE kake r77 status=ok admitted=true`. Both claims verify (C1 re-measured independently against
every recorded observation; C2 evidence-verified on digest-bound receipts with the before state
re-derived from the committed base JSON and the XML-only constant), no owned axis is harmed, and the
three trends are `improved`. Routed defects 1–6 are report and corpus-documentation hygiene; none
touches either claim's measurement.

Operator note: the four `SHONEN.md` boxes are checkable by a non-author from the repo — box 1: the
`S###` resolution and the table/registry/checklist counts in `SKILL.md`; box 2: a real gap (one
LOG-named receipt absent), with the flip on the row; box 3: 0 missing script/counter targets inside the
frozen scope; box 4: 0 cross-lane citations. Box 2 fails as marked; the others resolve. Promotion is
operator-owned and was not touched.
