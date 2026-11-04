# Round 52 — verifier spot-check (kake)

author: hyaku closure (non-author integrator, @m_flash)
lane: kake-shokunin · round 52 (lane round 52) · campaign hyaku
base: `93d7fdbd45b0e5698927e7f9cb3dafca24ace416` · lane tip at re-check: `a1d83ecf2012f92fd470c5aaacebf2225207b8e9`
report checked: `.ufo/reports/round-52/kake.md` (fleet commit `24ea368`, author `kake-shokunin <kake@shokunin.local>`)
dispatch digest: `2026-10-25T07:02:07-03:00 launch kake round=52 pgid=3248979 driver=hyaku-inline attempt=1`;
`2026-10-25T07:31:15-03:00 complete kake round=52; hyaku-inline attempt=1`

This is a non-author check: I did not author the round and did not improve it. Nothing below re-runs a
lane gate; each claim is either re-measured with a plain command or evidence-verified against the
committed receipt, and which one is stated per claim. The 46-seat wave ran **zero** seats (dispatch
refused at the host job cap, orchestrator-side), so no falsification wave attacked these claims; the
re-derivation is mine.

## 1. Step-1 conformance

| Check | Result | Evidence |
|---|---|---|
| report committed by the lane identity | **pass** | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-52/kake.md` → `kake-shokunin <kake@shokunin.local> 24ea3681f9c47fa7846b63c850ddc281e8bb6ad9` |
| `SHONEN` heading, one line per box | **pass** | report lines 78–85: 4 marks (`[~]`, `[ ]`, `[~]`, `[~]`); no `[x]` claimed |
| cited lane commits exist | **pass** | `73c22a3 5422ff3 3a50ae4 1ae8de5 a4a890c a1d83ec` all resolve (`git rev-list --max-count=7 a1d83ecf`) |
| cited commits are ancestors of the branch ref | **FAIL** | `git merge-base --is-ancestor a1d83ecf master` → exit 1; `git rev-list --left-right --count master...HEAD` → `0	6` (branch `master` = `93d7fdbd`, the round base) |
| repo pushed (`ahead=0`) | **pass only vacuously** | `jj-lane.sh state` → `local=93d7fdbd remote=93d7fdbd ahead=0 behind=0`; the six round commits are **not on the branch**, so `ahead=0` measures nothing about them |
| report's `pushed:` line truthful | **FAIL** | report header: `pushed: git ls-remote origin refs/heads/master = a1d83ecf (ahead 0)`; observed `git ls-remote origin refs/heads/master` → `93d7fdbd45b0e5698927e7f9cb3dafca24ace416`, and `git reflog show origin/master` → last push `2026-10-25 04:03:09` at `93d7fdbd` (before the round) |
| no uncommitted round work | **FAIL** | `git status --porcelain` → `M .ufo/waves/round-52/control/c1-mutation-ladder.json` (mtime 07:30:18; differs from the committed blob only in 18 `old_tail` strings) |
| dispatched prompt carries the template contract | **pass** | prompt lines 3–140 diff byte-identical to `templates/round-prompt.md` modulo the lane substitution; round-level items i–v and child-lane items a–e all present (lines 3–7, 11, 15–16, 82, 101–102, 106–108, 118–119, 133–140) |
| L2 floor (≥8 lanes, one batched swarm) | **not met, disclosed** | `0` seats spawned of a declared 46 (`.ufo/waves/round-52/w1-dispatch.json`, `w1-validator.err` empty); refused at the host job cap — orchestrator-side, status-neutral, recorded in the report and lesson |
| `LOG.md` entry for the round | **FAIL** | `git diff --stat 93d7fdbd a1d83ecf -- LOG.md` → empty; the appendix chain ends at round 51. No landed change is tied to a `LOG.md` entry |
| report sections | **defect** | `## Sources & frontier` absent and `## Trend verdicts` absent (both contract-required conformance items); `Work performed`, `Landed changes`, `Before → after measurements` have no heading (the substance sits under `## Claims` / `## Measured`) |
| evidence-pointer consistency | **defect** | report names measured revision `a4a890c`; every per-instrument receipt names `1ae8de5`; `SCORECARD.md` names `1ae8de5`; `final-verify.txt` names `a4a890c` and contains neither `a1d83ec` nor `1ae8de5` although the report calls it verification "at the measured tip". `final-verify.txt`'s census block echoes one `W04` line where `census-after.txt` (and every other census receipt) carries 12 |

Status stays `ok`: the report is contentful, names six real committed round-work hashes, and is not a
completion marker. The push/ancestry failure, the `LOG.md` gap and the missing sections above are
conformance defects; the closure landing that carries this file pushes the six round commits, so the
ancestry defect is repaired by the record that reports it (verified with
`git ls-remote origin refs/heads/master` after the landing).

## 2. Claims re-derived

Counting commands and observed output are the ones I ran against committed bytes at `a1d83ecf`
(`git show <rev>:<path>` / `git grep` / `jq`), never the lane's counters.

### C1 — operability, capability deepening · **improved**

| predicate leg | reported | my measurement | method |
|---|---|---|---|
| `registry_rows == 2` | 2 | `git show a1d83ecf:SKILL.md \| grep -nE 'wave-evidence-ledger\|quote-truth-counter'` → 2 rows, `SKILL.md:1214` and `:1215`, 9 cells each | re-measured |
| `selftest_receipts == 2` | 2 | `control/c1-ledger-selftest.txt` `19/19 EXIT=0`, `control/c2-quote-selftest.txt` `18/18 EXIT=0` (plus `c1-registry-selftest.txt` `10/10`); both digest-pinned in `baselines.json` | evidence-verified + independent fixture count (18+1 / 17+1) |
| `vacuity_mutant_families_killed >= 10` | 13 of 18 | `jq '[.rows[]\|select(.old_accepted==true and .new_rejected==true)]\|length'` → `13`; `[.rows[]\|select(.kind=="mutant")]\|length` → `18`; pass fixture `old=0 new=0`, `pass_fixture_agrees=true`; polarity of all 19 rows consistent with their exits | re-measured (arithmetic) |
| `real_data_reruns_pass == 2 of 2` | 3/3, 8/8 | L1–L3 re-derived PASS (spawn 48 = payload 48 = grant 48, 48 settled, 0 dead, 48 distinct report digests; 10 roles, 2 probe receipts, used alias 200/ok, the 403 alias absent from the used set; wall 897 s = timing = accounting = LOG) and C1–C8 re-derived 8/8 at `1ae8de5`, `a4a890c`, `93d7fdbd`, `a1d83ecf` | re-derived from the committed inputs, not by executing the gate |
| controls discriminate | `0/3 @ 007d66e4`; `0/8 @ 93d7fdbd` | `c1-ledger-control-absent.txt` 3 FAIL with the three absent files confirmed absent at `007d66e4`; `c2-quote-base.txt` genuinely 0/8 (8 conditions, 21 detail lines). Caveat: `c1-ledger-at-contract-base.txt` is a non-discriminating control (the base already passes 3/3) and the report says so | evidence-verified |

`C1`'s last sentence ("C1's vacuity floor, C2's C8 mirror read and C6's receipt fields are implemented
and each has a fixture") is evidence-verified only at the tally level: the selftest receipts print a
tally, not fixture names, so which fixture covers C8/C6 is not independently nameable from the
committed bytes.

### C2 — freshness, sourced learning + drift reconciliation · **improved**

| predicate leg | reported | my measurement | method |
|---|---|---|---|
| `admitted_entries_citing_mined_rows == 3` | 3 | each entry exists (`git cat-file -e`), line 1 carries `source: S374` / `S329` / `S312`; each row's `used-by` names exactly that entry; the three ids are absent at the base and present once at the tip | re-measured |
| `registry_rows_delta == +3` | 145 → 148 | `grep -cE '^\| *S[0-9]+'` on `93d7fdbd:corpus/SOURCES.md` → `145`, on `a1d83ecf:` → `148`; `git diff --numstat` for the file → `3	0` (no existing row rewritten) | re-measured |
| `census_validate_exit == 0` | exit 0 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, `kake ok …/corpus/SOURCES.md`, 12 `W04` warnings, no `E` codes | re-executed (my run, not the lane's) |
| `sweep_drift_legs_before == 3` | 3 | `drift-before.txt:93` → `DRIFT verdicts: PQ-2 GATE-OPENED · sitemap LISTED-LIVE · plazir-gate-anomaly`; `:100` `VERDICT: DRIFT … (exit 1)` | evidence-verified |
| `sweep_drift_legs_after == 1` | 1 | `sweep-after.txt:91` → `DRIFT verdicts: plazir-gate-anomaly`; `:98` `VERDICT: DRIFT … (exit 1)`; the plazir block is byte-identical before/after; `PQ-12 EDIT-LANDED` and `PQ-5 PENDING` are not legs | evidence-verified |
| retained bodies and receipts | sha256 / bytes / 200 | `S374.html` 8153 B `3ad358bd…`, `S329.html` 61418 B `452aabc3…`, `S312.html` 46056 B `126c3da4…` — all equal to `sources/receipts.json` | re-measured |

No-harm: both owned axes stay at 10/10 (`SCORECARD.md` rows `operability`, `freshness`); the round's
lane diff to owned content is additive only (`corpus/SOURCES.md` +3/−0, three new `knowledge/` files,
`SKILL.md` +18/−0, `PROVINCE.md` +18/−0, `SCORECARD.md` +57/−0); the sweep moves 3 legs → 1 and the
plazir absence is disclosed rather than re-pinned. Residual risk on `sweep_drift_legs_after`: the two
closed legs were closed by editing `corpus/knowledge/freshness-pins.json` to match the observed state,
and the observed external state in `drift-before.txt` is the same as in `sweep-after.txt` — the 3→1
delta is a pin reconciliation, not a between-run change in the world. The round says so; it must not be
read as external freshness improvement.

## 3. Discernment spot-check (`corpus/lessons/round-52.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S374 (Yahoo! JAPAN `rel` attributes) | admit | `.ufo/waves/round-52/sources/S374.html` (8153 B) | **agree** | quote is a raw substring, sha256 and byte count match, URL and 更新日 2010-11-24 match, section `rel属性の利用` exists |
| S329 (Baidu friendly-crawl course) | admit | `.ufo/waves/round-52/sources/S329.html` (61418 B) | **disagree (locator)** | quote, hash and URL reproduce, but the quote sits under `如何正确识别Baiduspider移动ua` (~char 10875), ~4.4 k characters before the cited `robots写法` heading; the wrong anchor is propagated into the `S329` registry row. The note "no revision printed on the page" is also false — the page carries `最新更新章节：2019-09-18` |
| S312 (Baidu mobile-matching error causes) | admit | `.ufo/waves/round-52/sources/S312.html` (46056 B) | **disagree (locator)** | quote, hash and URL reproduce, but `常见原因` occurs 0 times in the body; the quote sits under `如何提升移动适配效果`. The claimed `章节时间戳 2020-08-14` is the page-level `最新更新章节` marker, not a timestamp on the quoted section. Propagated into the `S312` row |
| `crux-keyless-check.md` | refuse | staged package file; `corpus/knowledge/field-performance-cwv.md` | **disagree as stated, decision stands** | the held entry carries only `CrUX eligibility (S038)` and `The CrUX API (S039)`; the keyless CrUX Vis rule is **not** held, so the stated ground is wrong. What is true and sufficient: S303/S304 are in neither the base nor the tip registry and in no receipt (`grep -c 'S303\|S304'` → 0), so the row could not be written under CORPUS rule 1 |
| `jekyll-url-baseurl-options.md` | refuse | same package file; `corpus/knowledge/pages-base-path.md` | **disagree as stated, decision stands** | the staged file's rows are `S296`/`S146` (same config-options URL), not `S041`/`S042`, and `pages-base-path.md` does not carry the composition/trailing-slash rule. The genuine duplicate is the duplicate **URL** already held as `S080` — which is what rounds 49/50 recorded, and round 52 replaced with a false reason |

Verdict: every gate **decision** survives re-opening (three genuine admits with exact quotes; two
correct refusals), but four of five **stated reasons/locators** do not. `corpus/SOURCES.md` rows placed
on this round's quotes therefore carry two wrong section cells.

Newly written `corpus/SOURCES.md` rows: `S374`, `S329`, `S312`, each 11 cells, `status mined`, `opened
2026-10-25`, `recheck 180d`, `used-by` one entry. The `S374` row's quote is a raw substring of its
retained body and its section is accurate; the `S329`/`S312` rows inherit the wrong sections above. The
≤25-unit rule the lesson declares (one unit per CJK character, one per non-CJK whitespace token;
6–40) holds for all three quotes as counted.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0 over
148 rows, 12 `W04` duplicate-URL warnings and **no** dangling-id finding — the census does not resolve
`S###` citations made in `knowledge/` prose against the registry, which is why the defect below
survives a green gate.

## 4. Trends

| trend | verdict | evidence |
|---|---|---|
| expansion | **improved** | `corpus/SOURCES.md` 145 → 148 rows (`grep -cE '^\| *S[0-9]+'` at both revisions; `git diff --numstat` `3	0`); three admitted entries on uncovered per-engine crawl-hygiene ground, each `source:` citing a `mined` row opened this round (`CORPUS.md` rule 4); capability rows appended to `SCORECARD.md` (57 added, 0 removed) |
| quality | **unchanged** | no existing entry re-verified, deepened or superseded this round, and no `QUALITY.md` criterion added (`git diff --stat 93d7fdbd a1d83ecf -- corpus/QUALITY.md` empty); the round's instrument work is an operability capability, counted under expansion. The three new entries were admitted with two wrong section locators and five unresolvable supporting ids, and none is marked — a defect routed below, not a quality gain |
| discernment | **unchanged** | the outside spot-check agrees on 1 of 3 admits' locators and on 0 of 2 rejects' stated reasons (table above), so it does not meet the `improved` condition; the disagreement is recorded here (a `corpus/lessons/` artifact) but has not yet become a `QUALITY.md` criterion, so it meets neither the `improved` nor the `harmed` ("left unlearned") condition at closure — the criterion is owed by the next round |

## 5. Routed defects (lane must fix next round)

1. **Push/ancestry (highest).** The six round commits (`73c22a3…a1d83ec`) were not on `master` and not
   on the remote when the report claimed them pushed; the lane must commit through
   `scripts/hyaku/jj-lane.sh commit` (which moves the bookmark and verifies `landed <hash>`) and cite
   only the `landed` line. The closure landing that carries this file also lands those six commits.
2. **`LOG.md` round entry.** Round 52 changed `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `SOURCES.md`
   and `corpus/` with no `LOG.md` appendix entry; add the appended entry (never rewrite prior text) and
   tie each landed change to it.
3. **Report sections.** Add `Sources & frontier` (rows before→after with the counting command, rows by
   tier, old→new) and `Trend verdicts` (expansion / quality / discernment); name the three measurement
   headings the contract requires. File the next report with one measured revision, not three.
4. **Dangling cross-registry citations.** `yahoo-japan-rel-nofollow-semantics.md` (lines 26–27),
   `baidu-friendly-crawl-guidance.md` (lines 38–39, 47) and `baidu-mobile-matching-error-causes.md`
   (line 35) cite `S367`, `S372`, `S373`, `S390`, `S409` as held ground; those ids resolve only in
   `kotodama-shokunin/corpus/SOURCES.md` (`grep -c` for each in kake → 0). Either open and register the
   rows in kake's registry or restate the comparisons against rows kake holds (`S098`, `S099`, `S011`,
   `S095`, `S263` all resolve). Corpus corrections are new entries, never rewrites.
5. **Gate locators.** Correct the `S329` and `S312` section cells and the lesson `## Gate` locators to
   the headings that actually contain the quotes (`如何正确识别Baiduspider移动ua`; `如何提升移动适配效果`),
   and drop the "no revision printed" claim for `S329` (the page prints 2019-09-18).
6. **Refusal reasons.** Restate both round-52 refusals on their true grounds (S303/S304 unopened and
   unregistered; duplicate URL with the held `S080` row), not the held-ground claims the spot-check
   falsified.
7. **Gate registry rows (Gate standard).** `64=usage` is unreachable — `argparse.error()` exits 2, which
   the same cell already maps to `could-not-evaluate`; malformed `settlement.json`/`route-map.json`/
   probe receipts exit 1, not 2 as the row claims; the self-tests assert exit codes but no expected
   finding id; `quote-truth-counter` pins one receipt digest, not "both", and leaves the mirror input
   unpinned by name; `wave-evidence-ledger` pins 8 round-51 blobs plus `LOG.md`, not "nine round-51"
   blobs.
8. **Receipt reproducibility.** `c1-mutation-ladder.json` embeds per-fixture git commit hashes from
   throwaway repos with unpinned timestamps, so it is not byte-reproducible (the uncommitted worktree
   copy differs in exactly those 18 strings); `c2-quote-selftest.txt` is pinned at `1ae8de5` but the
   selftest stamps `HEAD`, so a re-run at the measured revision cannot match its pin. Pin only stable
   fields (tally, verdict, input digests) and state the fixture rule.
9. **`final-verify.txt` fidelity.** The census block echoes 1 `W04` line where every committed census
   receipt carries 12, and the file is labelled "at the measured tip" while its header names
   `a4a890c`; regenerate it verbatim from the seven instruments at one named revision.
10. **`SCORECARD`/`freshness-pins` prose.** `plazir-15-site` **does not exist** on this host
    (`[ -e … ]` false; the sweep prints `fatal: cannot change to …`), so the lesson's "the source
    directory exists but its sitemap source is absent" is false (the SCORECARD wording "source
    absence" is right). The `sitemapReconciled` premise ("source tree pruned 2026-10-12, cannot be
    source-verified") is also false: `~/Projects/ds4cc-marketplace` is present with `sitemap.xml`
    tracked, and `sitemap.xml` at remote tip `24991e44` is byte-identical to the live listing
    (200, 7810 B, 100 locs) — the source check that was declared impossible was available and passes.
    Replace the pin justification with the source-parity check.
11. **Uncommitted round work.** Commit `control/c1-mutation-ladder.json` (or revert it) so the lane
    closes clean; a regenerated receipt left in the tree can ride the next push.

Promotion note for the operator: `SHONEN.md` is untouched (`[ ]` ×4) and no box is claimed checked.
Box 2 (end-to-end task) is honestly marked `[ ]` because no wave seat ran. The citation-resolvability
defect in item 4 is the kind of cross-domain bleed box 4 asks about, so it should be read before any
promotion review treats the round's corpus as clean.
