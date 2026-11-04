# ScribeLesson — round87 w1 report

## Behavior and deliverables

Drafted the round87 lesson and a separate append-ready QUALITY criterion, inside this seat's allowed directory only. Axes: calibration (lowest, 2 HOLD), freshness (10 HOLD). Both drafts distinguish proposed Gate decisions from admission and unobserved execution evidence. No production edit, delegation, VCS mutation, install, service, browser, provider probe, commit or push.

- Lesson candidate: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeLesson/round-87.md`
- QUALITY candidate: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeLesson/QUALITY-criterion.md`
- Own reopened RFC source: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeLesson/receipts/rfc9111.txt`

## Findings and gates

1. Read the frozen contract and count.py, expected ledger, r84/r85/r86 snapshots, latest considerthese proposal4, existing QUALITY tail and L1 disposal record. Independently compared all eight expected ledger decisions with the three outside tables; all show agreement. Snapshot hashes match expected-ledger.json. This is source-table transcription evidence, not a counter run or historical judgment re-execution.
2. Own RFC9111 GET succeeded: 84477 bytes, SHA256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`. Source URL https://www.rfc-editor.org/rfc/rfc9111.txt. Exact HTTP status/headers and request/response timestamps were not captured; no HTTP 200 receipt or owned-property trial is claimed.
3. Located two Gate quotes myself: §4.2.3 L775, “corrected_initial_age = max(apparent_age, corrected_age_value);” (3 whitespace words); §4.2 L621, “response_is_fresh = (freshness_lifetime > current_age)” (5). §4 L468–490 supplies the additional reuse conditions. ADMIT candidate S462 conservative arithmetic; REJECT age-alone reuse proposition. Neither quote proves cache reuse permission.
4. Read-only JSON census observed 17 age cases, twelve exit0 and five exit1; union of valid output keys is the six specified terms. It did not execute the tool or establish every output's exact key-set validity.
5. r86 mistakes retained: self-certifying/cross-claim predicate and live-fleet drift. r87 snapshot/no-receipt dependency is the design change; mutant results remain explicitly unobserved. No successful after receipts invented.
6. Candidate scratch-disposal disposition distinguishes L1's recorded rm from this seat's observation. Directory listing showed retained rfc9110.txt (502941 bytes), no HTML mirror. L1's bindings-disposal.md reports removal of the untracked HTML with exit0; this seat did not run that deletion. Quarantine-before-append is carried as a rule; assimilation is none.
7. Gate agreement is calibration metadata, not domain knowledge or proof of reliability outside the eight decisions. Independent spotcheck/admission stays closure-owned; D84-2/3/4 stay open. Exact conflict retained from r85 snapshot: “resolve D84-4 literal L2-planner versus validator prohibition. L1 planning/scout data-walk is mitigation, not an actual dispatched planner seat.”

## Exact shell commands and outcomes

Command 1 (overall tool success; curl_exit=0, hashes/size printed):

```sh
mkdir -p /fast/scratch/hyaku/kake-r87/ScribeLesson /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeLesson/receipts && cd /fast/scratch/hyaku/kake-r87/ScribeLesson && curl -fsS --max-time 60 -o rfc9111.txt https://www.rfc-editor.org/rfc/rfc9111.txt; echo "curl_exit=$?"; sha256sum rfc9111.txt; wc -c rfc9111.txt; sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/snapshots/round-84-verifier-spotcheck.md /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/snapshots/round-85-verifier-spotcheck.md /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/snapshots/round-86-verifier-spotcheck.md
```

Observed snapshot SHA256s, r84/r85/r86 respectively:

```text
80f48887b1e5f2e9d7d54adcce19d8b935f77fc0b236620abac3335b730dfda9
948c316831d0c71927e6a29501f05037b3faa940a251984ed28ca8f0eee2ce71
47499686bc976564c43174fdeeae2219e0db2351c571678ba35caff0a34de42b
```

Command 2 (overall tool success; printed total17 / exit0 12 / exit1 5 / six-key union; ls_exit=0):

```sh
python3 -c "
import json
cases = json.load(open('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/age-cases.json'))
print('total', len(cases))
print('exit0', sum(1 for c in cases if c['exit']==0), 'exit1', sum(1 for c in cases if c['exit']==1))
keys = {k for c in cases if c['exit']==0 for k in c['output']}
print('output_keys', sorted(keys))
"; ls -la /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ExecAssim/mirror/corpus/lessons/round-81-gate/ 2>&1; echo "ls_exit=$?"
```

Command 3 (success, no output; retained own source before deleting own scratch):

```sh
cp -- /fast/scratch/hyaku/kake-r87/ScribeLesson/rfc9111.txt /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeLesson/receipts/rfc9111.txt && rm -r -- /fast/scratch/hyaku/kake-r87/ScribeLesson
```

The fetch used a relative output only after changing into the explicitly created owned scratch. No clone created. Scratch removed before handoff. Read/grep/glob/write tools supplied remaining observations and artifacts; no counter/selftest/build/lint/product smoke run was executed.

## Limits and process defects

- Initial local:// globs failed to resolve; absolute-path discovery recovered. A broad read-only grep unnecessarily traversed .jj binary metadata; narrowed reads used frozen snapshots thereafter. No VCS command was executed.
- The Godspeed skill was read late, after initial context reads; source/draft claims are not execution-credit substitutions. The initial response was unnecessarily verbose; terminal handoff is compact.
- Counter, mutation, sequential-implementation, selftest and owned-property trial evidence remain assigned-owner work, not scribe successes. The draft explicitly names these unresolved findings rather than filling results.
- No install/update occurred. No build, lint, tests, service or runtime delegation was performed. Source bytes were retained, not a full-lane mirror.

## Self-evaluation

Accuracy 4: quotes and digests observed; HTTP status and trial absent and disclosed. Completeness 4: all seat topics covered, integration execution remains separately owned. Clarity 4: proposed decisions separated from receipts. Actionability 4: separate lesson and append-ready criterion; closure-owned debt explicit. Conciseness 3: initial narration was excessive; report retains exact commands for audit. Overall 3.8/5. Improvement applied: deliver separate compact criterion and no speculative successful receipts. Would the user agree: likely, subject to L1 and independent closure review, not this scorecard.

## Report trailer — lane-relative artifact paths

- `.ufo/waves/round-87/w1/ScribeLesson/round-87.md`
- `.ufo/waves/round-87/w1/ScribeLesson/QUALITY-criterion.md`
- `.ufo/waves/round-87/w1/ScribeLesson/receipts/rfc9111.txt`
- `.ufo/waves/round-87/w1/ScribeLesson.md`

Touched production surfaces: none. Out of scope: integration, judging, admission, source registry append, other seats' evidence and outside spotcheck. Scratch `/fast/scratch/hyaku/kake-r87/ScribeLesson/` created, source retained, scratch deleted.
