# Round 85 — non-author closure

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed round: 85; lane: kake. Base `bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7`; final authored revision `21211219803af39c6e5e369fc2a267e38bb08c38`; production carrier `aea07bf3c1d9e5ad50453af4e11cc52faf420e51`. This review admits only the two frozen bounded claims, not the round-84 classifier or the full D84 repair queue.

## Conformance

- `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H %s' -- .ufo/reports/round-85/kake.md` identifies lane-authored report commit `3ff4ff7f095ff42e3957b7e12d051bba0fd935a5`, author `kake-shokunin <kake@shokunin.local>`. Its commit time 2026-11-04T11:59:37-03:00 follows the final lane commit at 11:58:17-03:00.
- The report contains `## SHONEN` and four assessment lines matching the four checklist boxes: asserted, open, asserted, asserted. The historical missing end-to-end receipt remains an explicit gap; these boxes are not all ready for operator promotion. No promotion or checklist mutation is performed.
- For each of `2f042c370b5f11b84d4f8c9e5d066517aef646b8`, `856fa46bbeaf23d5d625be5d448852a6fe22c6e0`, `aea07bf3c1d9e5ad50453af4e11cc52faf420e51`, and `21211219803af39c6e5e369fc2a267e38bb08c38`, `git -C /home/vgpnk/Projects/shokunin/kake-shokunin merge-base --is-ancestor <hash> refs/heads/master` returned success. Branch ref, not detached HEAD's upstream, was used.
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kake-shokunin` returned `branch=master local=21211219803af39c6e5e369fc2a267e38bb08c38 remote=21211219803af39c6e5e369fc2a267e38bb08c38 ahead=0 behind=0 head=detached tracked=0 untracked=0`. `git status --porcelain` printed nothing.
- The dispatched prompt's sections 1–5 are an exact prefix match to the canonical `templates/round-prompt.md` after substituting lane, round, root, axes and repo. Mission/axes, distinct claims, lowest-axis duty, L2 minimum, report path/SHONEN/hash requirements, commit/push order, scope and L0 channel are present; section 6 carries the hyaku addendum. The template's write-scope and commit-before-report-write wording is implicit rather than an explicit own-repo-only/lands-last sentence; protocol rereading remains necessary. This is template-level wording debt, not a marker or a reason to reject real verified work.
- Independent JSON tally of committed `w1-results.json`: 10 results, 10 nonempty outputs; scout 1, executor 3, scribe 2, reviewer 2, critic 1, connector 1; attack 3/10. Literal dispatched planner remains absent, as disclosed. `bindings-read.md` records all 18 configured roles @m_zfl and a config digest; this is historical lane evidence, not independent proof of the answering model or a reconstruction of mutable host configuration. MISSION delegates runtime routing to the host table.

Dispatch/termination digest copied from the supplied record and matched to the live log:

```text
2026-11-04T11:37:49-03:00 launch kake round=85 pgid=2672594 driver=hyaku-inline attempt=1
2026-11-04T12:00:05-03:00 complete kake round=85; hyaku-inline attempt=1
```

## Claim rechecks — measured versus evidence-verified

I read the frozen counter before invocation: it is registered as a finite instrument, not a standing gate, and exports only committed SKILL/decoder bytes into supplied scratch. I did not execute the historical sibling gates or their selftest modes.

Commands independently run from the lane repo, with `<rev>` set first to the base and then the final authored revision:

```sh
python3 -B .ufo/waves/round-85/count.py --root . --revision <rev> --claim c1 --work /tmp/k85-verify
python3 -B .ufo/waves/round-85/count.py --root . --revision <rev> --claim c2 --work /tmp/k85-verify
```

| Claim | Independent before | Independent after | Verdict |
|---|---|---|---|
| C1 calibration: complete registry discovery for exactly three historical/experimental instruments | `C1 complete=0/3 missing=3 met=false`, exit 1 | `C1 complete=3/3 missing=0 met=true`, exit 0 | improved |
| C2 freshness: separate ordered Referrer-Policy decoder | `C2 cases=0/10 met=false`, exit 1 | `C2 cases=10/10 met=true`, exit 0 | improved |

A second plain census over `git show <rev>:SKILL.md` split table rows on `|`, selected eight-cell rows containing each filename in cell 1, and required nonempty cells. It found row counts `[0,0,0]` at base and `[1,1,1]` after, in the order `c84_defect_queue.py`, `c84_policy_values.py`, `policy_value_class.py`. Each referenced implementation exists and contains its documented `--selftest` interface; appended registry rows identify historical/experimental status and do not claim semantic or publication approval.

I also exported the committed decoder with `git show 21211219803af39c6e5e369fc2a267e38bb08c38:scripts/referrer_policy_effective.py` and independently invoked its ordinary stdin interface (not selftest) with new vectors:

| Input JSON | Observed effective token / exit |
|---|---|
| `["strict-origin", "no-referrer-when-downgrade", "origin"]` | `origin`, 0 |
| `["Origin"]` | empty string, 0 |
| `["unsafe-url", "unknown-token"]` | `unsafe-url`, 0 |
| `["no-referrer-when-downgrade", "same-origin, "]` | `same-origin`, 0 |
| `{"a":1}` | diagnostic rejecting JSON objects, exit 1 |

Source inspection confirms an actual nested sequential field/token walk and assignment only on recognized tokens; this is not a ten-case discriminator. Python Unicode stripping is explicitly the local JSON adapter profile, not a claim about full Fetch extraction.

Committed evidence verified without rerunning sibling gates: `controls/decoder-selftest.txt` records 32/32, exit 0; ExecRegistry's committed JSON receipts record historical instrument selftests 8/8, 4/4 and 15/15, all exit 0. `controls/base-c1.txt`/`base-c2.txt` pin the red base; `after-c1-carrier.txt`/`after-c2-carrier.txt` pin the 3/3 and 10/10 green measurements to carrier `aea07bf3c1d9e5ad50453af4e11cc52faf420e51`. These frozen finite measurements and the separate selftest are not certification of a universal gate. The retained trial contains six actual r81/r82 absence observations and two separately labeled synthetic opposite-order witnesses, yielding strict-origin versus no-referrer. No new property fetch or browser behavior is inferred.

## Axis verdicts and no-harm check

`git diff bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7 21211219803af39c6e5e369fc2a267e38bb08c38 -- SCORECARD.md` appends only the round-85 record, repertoire row and planned debt. Calibration remains 2 HOLD, freshness 10 HOLD; no legacy score was re-derived from a finite numerator. Registry/source/decoder spot reads preserve prior warnings and scope.

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 0/3→3/3, truthful bounded discovery, not general gate soundness |
| freshness | improved | C2 0/10→10/10 plus independent order/unknown/invalid-input checks |
| operability | unchanged | Preserved historical scripts and warnings; no claim of complete offline/remote sweep cleanliness |

No owned axis harmed. Both claims verify within their pre-frozen scope; admission is true. Neither is exploratory.

## Discernment spot-check

| Item | Gate decision | Re-opened source | Judgment | Reason |
|---|---|---|---|---|
| S458 field-specific algorithm | admit | https://w3c.github.io/webappsec-referrer-policy/ §8.1 steps 2–4, reopened 2026-11-04 | agree | Policy starts empty and is overwritten by every recognized nonempty token in order; the bounded decoder implements that rule. |
| Blanket response-policy reorder equivalence | reject | https://www.w3.org/TR/referrer-policy/ §11.1, direct public GET reopened 2026-11-04 | agree | The latest recognized policy wins; reversed recognized tokens need not preserve effective policy. This cannot justify arbitrary-header equivalence. |

The exact S458 registry URL was reopened, not substituted with TR. Its located 23-word quote matches rendered §8.1 step 3: “For each token in policy-tokens, if token is a referrer policy and token is not the empty string, then set policy to token.” The separately reopened TR quote is 22 words: “policy values will be ignored, and when multiple sources specify a referrer policy, the value of the latest one will be used.” The reader's TR response initially contained metadata only; direct `urllib.request.urlopen('https://www.w3.org/TR/referrer-policy/')` returned HTTP 200 and 127725 decoded characters; HTML data extraction and whitespace collapse confirmed the reject quote. No absence ruling was made from metadata.

Independent source-row census, using `git show <rev>:corpus/SOURCES.md` and `re.findall(r'^ {0,3}\|\s*S\d{3,}\s*\|', text, re.M)`: 195→196. S458 is tier A/mined with existing knowledge path. Required command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exited 0, printed `kake ok`, and retained the same 22 W04 duplicate-URL warnings.

## Learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | New S458-backed provenance-complete knowledge entry and README coverage row for ordered effective-token decoding, plus demonstrated bounded capability |
| quality | improved | Actual field-specific decoder replaces unsupported blanket equivalence as advice for this task; existing flawed classifier remains explicitly experimental, not silently blessed |
| discernment | improved | This non-author re-opened and agreed with both the admit and reject; semantic-overreach lesson and local-whitespace boundary are grounded |

## Routed defects — next round, not retroactive scope changes

- kake: retain D84-2 and D84-3 (general defect-instrument soundness and general-classifier semantic/input-dependence weaknesses) as open. This round addresses D84-1 only within truthful registry discoverability, not full gate conformance.
- kake/operator validator owner: resolve D84-4 literal L2-planner versus validator prohibition. L1 planning/scout data-walk is mitigation, not an actual dispatched planner seat.
- kake: late shortcut controls were captured after the ready handoff; retain the disclosed sequence defect and capture required controls before handoff next round. The red do-nothing base was committed before dispatch; no predicate or target changed after scoring.
- operator template owner: make own-repo-only write scope and report-write-after-child-commit ordering explicit in the canonical template. Current fidelity is exact; do not rewrite the dispatched prompt.
- kake: preserve false-row/canned-output counterexamples; neither finite success nor these admissions establishes general gate soundness. Do not promote historical green syntactic output to semantic/publishing approval.

No tools installed or upgraded. No lane-authored file, promotion mark, source tree or sibling lane was changed by this closure. Self-evaluation: accuracy 4 (bounded measurements, not full browser equivalence); completeness 4 (historical gate evidence checked, not rerun); clarity 4 (measurement/evidence distinction explicit); actionability 4 (routed owner-specific debt); conciseness 3 (long reproducibility record). Overall 3.8/5; compact final handoff rather than repeating these receipts.

CLOSURE kake r85 status=ok admitted=true
