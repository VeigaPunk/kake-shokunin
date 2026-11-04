# kake round 84 — non-author closure spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed round work at `c5d89c086ad1f427e40090688fa85ac2aba5dfcf`, base `fe42ad11eb1084ad2ea68d12c5bbb2922a089868`, freeze `f358022f7e1b2f3846be8ceacbe3a7ef22edf4be`, measured carrier `b05c390135302c44415b021fd0c0723b3f58d45e`. Report: fleet `.ufo/reports/round-84/kake.md`; lesson: `corpus/lessons/round-84.md`. No lane gate or selftest was executed by this closure.

## Conformance

- `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H' -- .ufo/reports/round-84/kake.md` returned `kake-shokunin <kake@shokunin.local> dfe648a1ed86cfef866297bb2ccb65fdc46d4305`. This is a substantive report, not a marker; it contains four checklist lines under `## SHONEN` and a LOG-linked committed-work table.
- `git cat-file -e <hash>^{commit}` and `git merge-base --is-ancestor <hash> master` succeeded for all four report commits (`f358022f`, `87cbfd99`, `b05c3901`, `c5d89c08`) and the base. Ancestry was tested against `master`, not detached HEAD/upstream.
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kake-shokunin` returned `branch=master local=c5d89c086ad1f427e40090688fa85ac2aba5dfcf remote=c5d89c086ad1f427e40090688fa85ac2aba5dfcf ahead=0 behind=0 head=detached tracked=0 untracked=0`. `git status --porcelain` was empty; `git ls-remote origin refs/heads/master` returned the same hash.
- Independently rendered `templates/round-prompt.md` substitutions for lane, round, root, axes and repo, then tested `prompt.startswith(rendered_template)`: `True`. The committed dispatched prompt includes the canonical contract and hyaku addendum §6, with routing amendments. Full round-level and child report contract retained.
- The 13-seat wave has 13 nonempty outputs, one connector and 4 attack seats. No L2 planner appears in the committed role list; holding planner at L1 does not meet the literal dispatched-planner split. The report also discloses late load order and shared-checkout rather than separate-worktree execution. These are status-neutral conformance defects.
- New round-84 verdict instruments have no registry-home entry: independent regex `c84_|policy[_-]value` over committed `SKILL.md` returns 0 matches. Selftest green is not full gate conformance.

Dispatch/completion digest (copied from closure assignment, durable here):

```text
2026-11-04T10:57:19-03:00 launch kake round=84 pgid=2799657 driver=hyaku-inline attempt=1
2026-11-04T11:19:56-03:00 complete kake round=84; hyaku-inline attempt=1
```

## Claim rechecks: measurements versus evidence

All `git show` measurements below read committed bytes at the named revisions. Python Eval used `subprocess.check_output(['git','-C',lane,'show',revision+':'+path], text=True)`; no lane-owned code was imported or executed.

### C1 calibration — improved, instrument qualified

Committed evidence read with `git show <after>:.ufo/waves/round-84/controls/<file>`:

| File | Observed committed output |
|---|---|
| `base-c84-defect-queue.txt` | `C1v1 revision=worktree items=4 open=3 closed=1 met=false`; `base_exit=1`; D4 already fixed at freeze |
| `after-c1.txt` | `C1v1 revision=b05c390135302c44415b021fd0c0723b3f58d45e items=4 open=0 closed=4 met=true`; `counter_exit=0` |
| `c84-selftest-c1.txt` | eight named fixtures, `selftest: 8/8 passed`; `selftest_c1_exit=0` |
| `c84-selftest-c1-v2.txt` | `selftest: 10/10 passed`; `selftest_c1_v2_exit=0`; diagnostic only, not substitution for frozen v1 |

Independently re-measured delivered repair state:

1. D1: each of `5.2.  Cache-Control`, `5.2.1.  Request Directives`, `5.2.2.  Response Directives`, `5.2.3.  Extension Directives` is a literal substring of committed `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt`; output `[True, True, True, True]`. Lesson line 43 contains the single named round-83 Gate correction and all four headings.
2. D2: `len('\n'.join(raw.splitlines()[837:844]).split())` returns `66`; lesson line 45 reads `D2 count=66 span=838-844 measure=words-full-span`.
3. D3: JSON-reading `w1-spec.json` items with `role == 'connector'` finds `ConnectorSibling`; `w1-results.json` has the same named `agent == 'connector'` with string output length `8341` UTF-8 bytes. Lesson line 40 names it. No connector proof depends on the counter's permissive non-string handling.
4. D4: `controls/census-before.txt` is committed, contains `census_exit=0` and 22 W04 lines; lesson lines 41/47 name the receipt. Independent required census below returns exit 0 with the same 22 W04 warnings. Thus the actual state and prose are both present, despite v1 omitting two prose checks.

The base commit lacks the new lesson/receipt/results; true base-revision state is four open items, not the worktree receipt's three. Report/lesson disclose this distinction. Frozen worktree baseline is evidence-verified, not represented as a re-executed committed-base gate result. The actual D1–D4 repairs verify independently; v1 soundness is not admitted by implication.

### C2 freshness — unprovable, honest stop

Evidence-verified `base-c84-policy-values.txt`: `revision=worktree ... real_changed=-1 ... met=false`, `base_c2_exit=1`. `after-c2.txt` pins carrier `b05c390135302c44415b021fd0c0723b3f58d45e`, `declared=3 receipts_ok=1 real_changed=0 ctl_changed=3 ctl_mismatch=0 eq_changed=1 eq_mismatch=0 record_equal=1 determinism=1 tool_offline=1 selftest_ok=1 counter_selftest_ok=1 met=true`, `counter_exit=0`. Frozen counter selftest receipt is `4/4 passed`, exit 0; `w1/ScribeKnowledge/tool-selftest.stdout` reads `selftest: 15/15 passed`.

Independent synthetic-pair measurement: load committed `capture-control/{control,equivalent}/{a,b}/<surface>/response.json`; form `{h['name'].lower(): h['value'] for h in doc['headers']}` and compare the union of names. Observed control: primary `cache-control: max-age=600 -> max-age=60`; robots `x-frame-options: absent -> SAMEORIGIN`; sitemap `referrer-policy: no-referrer, strict-origin -> strict-origin, no-referrer`; total 3. Equivalent pair has only that sitemap reorder; total 1. The before tree has no `scripts/policy_value_class.py`; the after tree does.

These reproduce syntax deltas, not semantic equivalence. `w1/ReviewC2.md:14-19` identifies the decisive frozen counterexample: Referrer-Policy selects the last recognized policy, so reversing two recognized policies changes the effective policy. Lesson lines 182-187 and knowledge-entry appended correction lines 89-95 explicitly retain `unprovable`, experimental status and prohibition on using the tool to waive drift/publishing. A green frozen tally cannot verify the declared semantic capability. No capability is added; the claim is not retrospectively narrowed to syntax.

## Per-axis and admission verdicts

`git diff fe42ad11eb1084ad2ea68d12c5bbb2922a089868 c5d89c086ad1f427e40090688fa85ac2aba5dfcf -- SCORECARD.md` shows only an appended round record: calibration 2→2, freshness 10→10, operability 10 unchanged; no capability credit. Spot reads of lesson, knowledge warning and QUALITY criterion preserve rather than conceal limitations.

| Owned axis | Verdict | Reason |
|---|---|---|
| calibration | improved | Four actual routed repairs independently verified; counter flaws disclosed rather than laundered as proof |
| freshness | unprovable | Declared value-semantics capability fails its frozen equivalence premise; syntax tally is insufficient |
| operability | unchanged | Experimental instrument added, but no new working semantic capability credited; existing workflows not shown harmed |

Status `ok`, admission `false`, verdict `rejected-honest-stop`. C2 does not verify; no owned axis is graded harmed. Neither claim is exploratory, so no taste-based replacement admission is appropriate.

## Outside discernment spot-check

Reopened live HTTPWG HTML with the reader and independently fetched it GET-only with Python `urllib.request.urlopen` for exact substring checks; also reopened live RFC Editor text. New row S457 is in committed `corpus/SOURCES.md`; S456/S457 are two renderings, not independent corroboration.

| Item | Gate decision | Re-opened source | Agreement | Reason |
|---|---|---|---|---|
| S457 response max-age semantics | admit/mined | https://httpwg.org/specs/rfc9111.html §5.2.2.1; https://www.rfc-editor.org/rfc/rfc9111.txt §5.2.2.1 | agree | Live source says exactly: “The max-age response directive indicates that the response is to be considered stale after its age is greater than the specified number of seconds.” Independent `len(quote.split())=24`; `quote in live_html=True`. Scope excludes lane class names/equivalence. |
| §4.1 normalization as response-directive reorder proof | reject | Same reopened documents, §4.1 Calculating Cache Keys with the Vary Header Field | agree | Exact phrase “reordering field values when order is not significant” is present; context expressly says “The header fields from two requests are defined to match”. Request-key normalization does not prove arbitrary response policy equivalence. |
| §5.2.2.2 as max-age anchor | reject | Same documents, §5.2.2.1 and §5.2.2.2 | agree | Actual headings are max-age at .1 and must-revalidate at .2, not the wave spec's mistaken pairing. |

Required census executed independently:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
```

Observed exit 0; 22 W04 duplicate-URL warnings (S033, S088, S092, S098, S099, S102, S110, S111, S115, S116, S117, S127, S416, S417, S427, S433, S445, S450, S451, S453, S454, S455), followed by `kake ok /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` (tab-delimited). Independent committed regex row count `len(re.findall(r'^ {0,3}\|\s*S\d{3,}\s*\|', text, re.M))` returns base 194, after 195. Prior registry rows are byte-identical; S457 is the added tier-A/mined row.

## Learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | One bounded source entry, but experimental semantic frontier explicitly not promoted to core or working capability |
| quality | improved | Named D1/D2 corrections and marked semantic limitation; no false semantic claim left unmarked; QUALITY lines 1703-1710 require field-specific equivalence grounded in this counterexample |
| discernment | improved | This non-author check agrees with both admit and rejects; semantic overreach becomes an explicitly grounded QUALITY criterion rather than hidden success |

## Routed defects — owner kake, next authorized round

- D84-1: Register the new verdict instruments at SKILL.md registry home with command, verdict map, selftest invocation, persisted expected-value paths, write scope and owner. Existing selftest/frozen receipts alone do not establish registry conformance.
- D84-2: Preserve frozen v1 evidence, but make any new instrument assert D3/D4 prose, a same-line D1 correction, nonempty string connector output and exact census exit tokens. Diagnostic v2 fixes only two omissions; `ReviewC1.md` documents the remaining gaps.
- D84-3: Before re-declaring semantic equivalence, freeze field-specific order/duplicate rules and an independent changed-row/input-dependence oracle. Retain the Referrer-Policy failing witness, canned-output limitation and imported-table enforcement debt (`ReviewC2.md`, `CriticClaims.md`, `MutC.md`). Do not use the experimental classifier for publishing approval.
- D84-4: Supply the required dispatched planner seat and read operative bindings before dispatch; resolve disclosed shared-checkout isolation deviation. Status-neutral procedural debt, not reason to call real work a marker.

SHONEN boxes are not all checkable: box 2 still explicitly records a gap/missing historical receipt. No checklist marks, promotion, mint, lane-authored file or other lane was changed by this closure. No tool installs or upgrades.

## Closure self-evaluation

Accuracy 4: committed measurements and live quote checks are separated from evidence-only gate tallies; no gate rerun or authenticity proof is implied. Completeness 4: both claims, three owned axes, three trends and admit/reject/source checks are covered; the spot-check is a sample, not exhaustive corpus review. Clarity 4: base versus freeze versus carrier are explicit, though the record is long. Actionability 4: four owner-routed defects name concrete failing conditions; future authorization remains operator-owned. Conciseness 3: durable commands and evidence make this artifact longer than the terminal digest; keep the final handoff short. Overall 3.8/5. Highest-impact improvement applied: retain only a brief verdict/digest in the final response. The user should agree that honest rejection is not marker failure.

Additional read-only seat `CloseKakeR84-8.Kake84Claims` independently confirmed all four repair states, identical 22-warning census set and carrier-to-head artifact stability; no lane gate was executed. It confirmed that v1 D4 also falsely rejects empty-equal census sets, the C2 import-table conjunct is unenforced, and repeated-run exit/one-newline handling remain weak: include these in D84-2/D84-3. Its snapshot review found no missing digests among ReviewC1's five present snapshot inputs and confirmed honest absent-file markers. It considered L1 planner sufficient under the local frozen contract; this integrator retains D84-4 because the dispatched higher-level prompt literally requires a planner L2 seat. This procedural disagreement does not alter status or claim admission.
