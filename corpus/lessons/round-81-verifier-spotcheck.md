# Round-81 verifier spot-check — kake (non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04T12:39Z
lane: kake (web properties & publishing) · lane_round 81 · base `2e11925500dd5a739376c9108c94616243af0cd4`
report: `.ufo/reports/round-81/kake.md` (filed `cb02b70551f14ac3dea7eadebac22cb2cdc45c10`, amended
`7678247a3c13b1dc03ed1cb8f80d2dba603ee0ca`) · lane branch tip at verification
`ddd38022f888e4199e198195be173797ff416381` (the report-cited carrier
`2b46f5c4db418c9a79e1990940da1a5029ff7e5b` is its parent)

## 0. Method and scope

Read-only. No lane or fleet write except this file. Registered gates were **not executed**: the
round-80 defect queue (`c80_defect_queue.py`), the standing receipt ledger (`c79_receipt_ledger.py`)
and the receipt-replay family are gate rows in `SKILL.md`; their verdicts below are
*evidence-verified* from committed receipts. I did execute non-gate instruments: the builder
`junk_tree_build.py` (determinism only), the registered **tool** `scripts/header_audit.py`
(offline), and the fleet `scripts/sources-census.sh`. Scratch was
`/fast/scratch/hyaku/kake-r81/closure-r81`, deleted afterwards.

All lane bytes were read through `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show
<rev>:<path>` at `ddd38022`; every file the two claims read is blob-identical across `498a0969`,
`2b46f5c4` and `ddd38022` (`git rev-parse <rev>:<path>` compared for SOURCES, the round-81 lesson,
the round-80 constants receipt, `junk_tree_build.py`, `junk-tree.json`, `w1-spec.json`,
`w1-results.json`, `w1-accounting.json`, `seat-failures.json`, the capture tree, and
`after-c81`-named receipts).

## 1. Step-1 conformance

| Check | Result |
|---|---|
| Report path/name | `.ufo/reports/round-81/kake.md` — correct |
| Report attribution | `kake-shokunin <kake@shokunin.local>` on both commits: `cb02b705` (filed 09:27:24) and `7678247a` (amendment, author 09:28:26, committer 09:34:52). Both are ancestors of fleet `origin/master` (HEAD `7678247a`) |
| `SHONEN` heading | `grep -c '^## SHONEN'` = **1**; exactly **4** box lines (`[~]`, `[ ]`, `[~]`, `[~]`), no `[x]` — matches `SHONEN.md`'s 4 boxes |
| Cited lane hashes | 14 distinct hashes cited (`a77b8a19`, `0a27045e`, `bec3ecf7`, `eccd0f9c`, `e93d26b7`, `a704ffa6`, `5ae1f32b`, `395f123c`, `dc8e5b08`, `e84c354e`, `31f502cb`, `498a0969`, `2b46f5c4`, `ddd38022`) plus base `2e119255`: every one exists (`git cat-file -e`) and `git merge-base --is-ancestor <hash> master` exits 0 |
| Uncommitted round work / push | `jj-lane.sh state` → `branch=master local=ddd38022 remote=ddd38022 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master` = `ddd38022` (remote `https://github.com/VeigaPunk/kake-shokunin.git`) |
| Prompt contract | Sections 1–5 are byte-identical to `templates/round-prompt.md` rendered with LANE=kake, ROUND=81, FLEET_ROOT=/home/vgpnk/Projects/shokunin, AXES=`operability + freshness (web properties and publishing)`, except one renderer substitution: line 1 prints `kake-shokunin` where the template literal is `<{{LANE}}-repo>`. Round-level contract present; all five child-lane items present (report path §4, commit-before-report §5, `SHONEN` heading §4, commit-hash citation §4, write scope addendum §3); addendum §6 present |
| Misroot | `git -C /home/vgpnk/Projects/shokunin status --porcelain` holds no kake/round-81 file |

Conformance defects are named in §6 and are status-neutral.

## 2. Claim C1 — calibration: the round-80 routed-defect queue closes

Frozen contract: `.ufo/waves/round-81/contract.md` §C1, predicate `met <=> open == 0` over the six
items `corpus/lessons/round-80-verifier-spotcheck.md` §6 files (verified: six numbered items,
matching the conditions below). I re-derived each item from committed bytes at `ddd38022`; the
counter was not run.

```text
$ git show ddd38022:corpus/SOURCES.md | grep -n '^| S453 ' | cut -d: -f1
200
$ git show ddd38022:corpus/SOURCES.md | grep -n '^| S454 ' | cut -d: -f1
201
$ git show ddd38022:corpus/lessons/round-81.md | grep -c 'corpus/SOURCES.md:200'
1        # R80-1 row also contains "S453"
```

| Item | Condition (frozen) | My measurement | Verdict |
|---|---|---|---|
| R80-1 | S453's line **L** re-derived, and an `R80-1` row names `corpus/SOURCES.md:L` for S453 | S453 at line **200** at base and tip; `corpus/lessons/round-81.md` carries `R80-1 … corpus/SOURCES.md:200 … S453` | closed |
| R80-2 | R80-2 row carries the numbers re-derived from `ctl-c80-constants.txt` | independent parse: `const_all.py 12/12`, `const_clean.py 12/12`, `const_echo.py 11/12`, `const_regex.py 12/12`; sum **47/48**; summary `constants_failed=4/4 cases=12`; row carries `constants_failed=4/4`, `47/48`, `11/12` | closed |
| R80-3 | R80-3 row carries registry counts for the two RFC 9110 URL forms | my count over registry `source` cells: `rfc9110.txt` = **4** (S028, S033, S453, S454), `rfc9110.html` = **3** (S010, S088, S433); row carries both | closed |
| R80-4 | settled attack share ≥ 0.25 over {reviewer, critic, mutation-tester, labrat}, and `w1-accounting.json` re-derives from spec+results | spec 15 items, attack requested **6/15**; results 15 rows, **14** non-empty (`ReviewRegression` empty); settled attack **5/14 = 0.3571**; `w1-accounting.json` matches `attack_roles`, requested/settled totals and share; `spec_sha256` = sha256 of the committed spec (`62dc6eec…1ff6e`) | closed |
| R80-5 | builder rebuilds round-80's junk tree deterministically (two runs identical) and round-80's own counter reads `open=5 closed=1 met=false`, exit 1 | my two builder runs are identical: one file `corpus/lessons/round-80.md`, sha256 `f32ae6a609f1…` in both (matches `w1/ExecJunkTree/determinism.txt`); the gate verdict is **evidence-verified** from `controls/after-r80-5-junk-rerun.txt` (registered gate not executed) | closed |
| R80-6 | recorder re-derivation equals `seat-failures.json` canonically; every seat has role/status/exit/error; record names the schema limit | my independent derivation (agent, role from spec, status = reported/empty by `output.strip()`, exit `unknown`, error `not recorded in w1-results.json`, output bytes/sha256, plus `empty_output`/`not_settled`/`schema_limit`) parsed-equals the committed record; 15 seats, 1 empty (`ReviewRegression`), all fields present, `schema_limit` names the schema's silence about status | closed |

**C1 verdict: verifies (6/6 closed).** Re-measured: R80-1, R80-2, R80-3, R80-4, R80-6 and the
R80-5 determinism. Evidence-verified: the R80-5 gate verdict and both selftest tallies
(`c81-selftest-c1.txt` = `selftest: 15/15 passed`, exit 0; `c81-selftest-c2.txt` =
`selftest: 22/22 passed`, exit 0).

**Post-report disclosure, verified.** Lane commit `ddd38022` and report amendment `7678247a`
disclose a second dead seat: `MutC` (mutation-tester) returned a 3,801-byte progress transcript, not
a deliverable (`seat-failures.json` `output_bytes=3801`; `w1/MutC.md` absent). Under the frozen
non-empty rule it is one of the five settled attack seats (5/14 = 35.7 %); on deliverables only the
share is 4/13 = 30.8 %. Both clear 0.25, so R80-4 stays closed on either reading; the disclosure is
honest and the frozen record is left as computed.

**Citation defect (status-neutral).** The report's before→after table says the after was measured at
`2b46f5c4…` and cites `controls/after-c1-final.txt` / `controls/after-c2-final.txt`; both receipts
record `revision=498a0969499f70830b7c992eb36ea364672f1a1b`. Commit `2b46f5c4` only adds the two
receipt files (`git diff --stat 498a0969 2b46f5c4` = 2 files, 17 insertions). Every claim-relevant
blob is identical across `498a0969`, `2b46f5c4` and `ddd38022`, so the predicate holds at the cited
revision; the receipt's measured revision does not.

## 3. Claim C2 — operability: capture → offline audit re-derives from committed bytes

```text
$ sha256sum capture/ds4cc-{primary,robots,sitemap}/body.bin
f2c5d2b3…  primary (78,897 B)   70f9ea28…  robots (62 B)   55cb947f…  sitemap (7,810 B)
```
Every body digest and byte count equals its `response.json`; each status is the integer 200;
`fetchedAt` `2026-11-04T12:05:06Z` ≥ `2026-11-04T00:00:00Z`; method `GET`; `truncated: false`;
`url` equals the declared url; `finalUrl` host is allowlisted (`ds4cc.com`). The manifest's three
checks equal `capture-expectations.json` on ids, urls, expect objects and allowlist.

```text
$ python3 -B scripts/header_audit.py --manifest .ufo/waves/round-81/capture/manifest.json --root .
ds4cc-primary hsts_present missing
ds4cc-primary csp_present missing
ds4cc-robots hsts_present missing
ds4cc-sitemap hsts_present missing
checks=3 findings=4
exit 1   # findings, not a manifest fault; stdout equals controls/after-c2-audit.txt byte-for-byte
```

Base control `declared=0 surfaces=0 failures=1 met=false`, exit 1
(`controls/base-c81-capture-audit.txt`); tampered control `body sha256 d1220935b5bd != receipt
f2c5d2b3ab34`, `met=false`, exit 1 (`controls/ctl-c81-tampered-capture.txt`). Selftest receipt
`selftest: 22/22 passed`, exit 0 (evidence-verified; not re-run).

**C2 verdict: verifies.** Same measured-revision citation defect as C1 (`after-c2-final.txt` records
`498a0969`). Stated limit, confirmed by the round's own reviewers: the chain binds body→receipt→audit
output but nothing binds a receipt to a socket, so a well-formed fabricated capture reads `met=true`;
provenance is the capture transcript (`w1/ExecCapture/capture-run.txt`), not the predicate.

## 4. Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | **improved** | C1: six routed defects re-derived closed from bytes at `ddd38022`; counter selftest 15/15, base control `open=6 met=false`, junk control `open=6 met=false` |
| operability | **improved** | C2: the capture-once/audit-offline chain runs and re-derives from committed bytes (receipts, declared-surface equality, audit stdout equality); capability row enters SCORECARD |
| freshness | **unchanged** | held at 10; `node scripts/freshness-sweep.mjs --offline` receipt `VERDICT: OK (exit 0, partial: offline)` with remote/armed/history skipped; no whole-corpus re-measure is claimed |
| coverage | **unchanged** | no new admitted knowledge entry; the new instrument is wave evidence outside the gate-registry population |
| depth | **unchanged** | appends deepen two existing entries (absent-resource section, locator correction), no new depth claim |
| adjacency | **unchanged** | box-4 sweep re-derived: 0 of 67 knowledge files cite a sibling lane repo path (`grep -lE '(kagi\|tabi\|…)-shokunin/' corpus/knowledge/*.md \| wc -l` → 0) |

No axis is `harmed` by the claims. §6 D1 is a report/SCORECARD accuracy defect on the round's own
account of its work; it is routed, and it does not overturn C1 or C2.

## 5. Discernment spot-check (non-author)

| Item | Gate decision | Source re-opened | Agree? | Reason |
|---|---|---|---|---|
| S454 admit (RFC 9110 §15.5.5 404 Not Found, §15.5.11 410 Gone) | admit, `mined`, tier A | `https://www.rfc-editor.org/rfc/rfc9110.txt` re-fetched 2026-11-04T12:3xZ: HTTP 200, sha256 `21c1cdce…47232a` = retained body = S028/S453 digest; retained `:7593` carries the 9-word quote "the 410 (Gone) status code is preferred over 404" as a raw substring; `:7589-7590` and `:7669-7670` carry the two collapsed-only definition spans | **agree** | The row is opened, tiered correctly, the quote is located and the section anchors name the section that contains it |
| Reject §15.5.4 as an absent-resource anchor | reject | `rfc9110.txt:7569` = `15.5.4.  403 Forbidden`; `:7571-7572` is an authorization refusal, nothing about an absent target | **agree** | The anchor named the wrong section; refusing it was correct |
| Re-open S433 (RFC 9110 singleton/field-line semantics) | re-open, bytes unchanged | retained `.html` sha256 `d4317606…fe1e5` = round-61 `sources/S433.html` sha256; quote at `.html:4039-4040` "Fields that only anticipate a single member as the field value are referred to as \"singleton fields\"" is present | **agree** (source) / **disagree** (landing) | The re-open is real; but the report's "Rows touched old→new — S433: `recheck 180d → 2027-05-03` … `used-by … round-81.md`" did not land: the committed S433 row is byte-identical to base (`git diff base..tip -- corpus/SOURCES.md` = one inserted S454 line; cell-by-cell diff of S433 empty) |
| Reject the `merge/kake` staged package | reject | `.ufo/waves/round-80/w1/ConnectorC/collision.out`: `id_collisions 8`, `staged_urls_held 27`, `staged_rows 129`; round-81 `w1/ConnectorC/collisions.txt` lists the same 8 ids | **agree** | Adoption would collide on 8 ids and duplicate 27 held URLs |
| S454 registry row | new row, `status=mined`, `opened 2026-11-04`, `recheck 365d`, `used-by` cites the entry and the lesson | `corpus/SOURCES.md:201`, 11 columns, census-valid | **agree** | Row parses under the frozen census, anchor lines resolve in the retained body, `used-by` paths exist |

## 6. Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **unchanged** | `corpus/knowledge/*.md` = 67 at base and at `ddd38022` (`git ls-tree -r --name-only <rev> -- corpus/knowledge \| grep -c '\.md$'`); the round appended a section to an existing entry, one mined row (`SOURCES.md` 191 → 192) and one capability — no net new admitted entry on uncovered ground, which is the LEARNING.md observable |
| quality | **improved** | S433 re-opened with retained bytes identical to the round-61 copy (sha256 `d4317606…`); an append-only locator correction in `corpus/knowledge/response-header-expectations.md` §5.2 → §5.3 (`rfc9110.txt:1529-1536`); the stale "still 404" lines in `publish-queue.md` superseded by an appended `[r81-observation]` with digests; both claim instruments superseded by dated amendments with the predicate unchanged; five receipt rewrites disclosed in `.ufo/waves/round-58/receipt-rewrites.json` (base prefix byte-preserved). Defects D1/D6/D7 below are routed |
| discernment | **improved** | this spot-check agrees with the Gate on the S454 admit, the §15.5.4 reject and the package reject; the six routed round-80 defects are now decidable from bytes; the round's own attack seats found four instrument/term defects before the after-states (settled population, manifest self-assertion, lexical time compare, wrong RFC anchor) and each fix is a dated amendment; the lane disclosed the dead mutation-tester and the substantive share after the report rather than leaving the frozen 5/14 to stand alone |

## 7. Routed defects (lane to fix next round; status-neutral)

1. **D1 — S433 row update claimed, not landed.** `corpus/SOURCES.md`'s S433 row is byte-identical
   to base (cell `recheck` = `180d`, `used-by` = `corpus/knowledge/response-header-expectations.md`
   at both revisions). The report line 126 and the SCORECARD round-81 block state `recheck 180d →
   2027-05-03` and the `used-by` addition as done. Apply the permitted in-place cells (SOURCES rule
   2 allows `status`/`recheck`/`used-by`, logged old→new) and append a correction naming the
   superseded sentence, or withdraw the claim by append.
2. **D2 — measured revision mislabelled.** Both before→after rows name `2b46f5c4…` as the final
   measured commit and cite `after-c1-final.txt` / `after-c2-final.txt`, which record
   `revision=498a0969…`; `2b46f5c4` only adds the receipts. Cite `498a0969` (blob-stable to the tip)
   or re-run both counters at the tip and commit the receipts.
3. **D3 — filed report bytes rewritten.** `7678247a` edits the filed report in place (lane-tip line,
   wave bullet, landed-changes row, claim row) instead of appending an erratum that names the
   superseded text. PROTOCOL ("A filed report is a record") forbids rewriting filed bytes. Record
   the superseded lines in the next report's erratum.
4. **D4 — disclosure arithmetic.** The report and lesson say `MutC` left a "3,771-byte" progress
   log; `seat-failures.json` records `output_bytes: 3801` and the committed output encodes to 3,801
   bytes. Re-derive the number from the record and correct by append.
5. **D5 — dead receipt paths.** `corpus/lessons/round-81.md` §Settlement names
   `controls/after-c81-defect-queue.txt` and `controls/after-c81-capture-audit.txt`, which do not
   exist; the committed receipts are `after-c1.txt`/`after-c1-final.txt` and
   `after-c2-carrier.txt`/`after-c2-final.txt`. Append the correction.
6. **D6 — stale selftest tally in a new criterion.** `corpus/QUALITY.md`'s round-81 criterion cites
   `controls/c81-selftest-c2.txt` as `18/18`; the committed receipt reads `selftest: 22/22 passed`.
   The lesson §Claims also carries `18/18` (partly self-corrected in §Post-attack settlement). Append
   a superseding criterion row naming the corrected tally.
7. **D7 — ledger-gate claim without a committed receipt.** The report states the standing round-79
   receipt ledger is "green at the tip: `C1v2 revision=5ae1f32b… events=40 … met=true`, exit 0"; no
   such receipt exists in the lane at that revision or at the tip (round 80 committed
   `controls/after-c1-ledger-gate.txt`). Commit the gate receipt at the measured revision.
8. **D8 — R80-1's routed ask is only partly discharged.** The round-80 closure asked for the pointer
   in `.ufo/reports/round-80/kake.md:158` and `corpus/lessons/round-80.md:51` to be corrected by
   erratum/append; both still read `corpus/SOURCES.md:201`. The frozen R80-1 condition closes on the
   in-lane row, but the filed fleet report has no erratum. Append one, or state why not.

## 8. Promotion status (operator-owned)

`SHONEN.md` box 2 remains `[ ]`: the ledger row's gap (one LOG-named receipt absent) is unchanged,
and the round says so. Boxes 1 and 3 are `[~]` ledger-backed; box 4's sweep I re-derived as 0/67
sibling citations. No box carries a named non-author `[x]`; promotion is not available on this
round's evidence and stays operator-owned.

## 9. Verdict and limits

- **Verdict: admitted.** Both declared claims verify (C1: 6/6 conditions; C2: the whole chain),
  and no owned axis is harmed; scores are held, and the SCORECARD diff is additive except for one
  in-place line inside the new round-81 block. The eight routed defects are accuracy/evidence
  defects of the round's reporting, not claim failures.
- Limits: I read the gate receipts, not the gates; I did not re-fetch every URL, only the S454
  `.txt` (live) and the committed retained bodies for S433; a capture's provenance remains a
  transcript claim (the lane's own stated limit).
