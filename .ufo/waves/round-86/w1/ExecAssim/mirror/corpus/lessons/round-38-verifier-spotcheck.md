author: hyaku closure (non-author integrator, @m_opus)

# Round 38 — verifier spot-check (kake)

Non-author closure of kake round 38. Report `.ufo/reports/round-38/kake.md` (fleet `694cb77a`),
prompt `.ufo/prompts/kake-round-38.md` (fleet `aa10be14`). Lane base
`af43a50fa399881eead9381d835b78a015e277a6`, tip `729878e3e74e18b55cd9a58d071a4f7b2419a8b7`.
Driver digest (copied from `.ufo/watchdog.log`, mutable):
`2026-10-23T01:05:34-03:00 launch kake round=38 pgid=2352315 driver=hyaku-inline attempt=1` ·
`2026-10-23T02:03:58-03:00 complete kake round=38; hyaku-inline attempt=1`.
No closure seat ran: one batch of three read-only seats was refused at the host's 100-job limit,
so the integrator ran every check below. No lane gate, counter or selftest was executed (PROTOCOL
§Gate standard, Closure consequence). C2 is **evidence-verified** against committed receipts plus
plain re-derivations (git, sha256, jq, census, curl). Nothing ran inside the lane except read-only git.

## Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H %ad' -- .ufo/reports/round-38/kake.md` | `kake-shokunin 694cb77a1b06…` author date 01:46:57-03:00, committer date 02:03:43-03:00 (after tip 02:02:39, before driver complete 02:03:58). Earlier jj snapshots `8a8094a`, `1bbc823` exist only under `refs/jj/keep/*` | ok |
| `## SHONEN`, one line per box | report lines 108–113 vs `git show 729878e3:SHONEN.md \| grep -c '^- \['` → 4 | 4 boxes, 4 lines, all `[~]`, no `[x]` | ok |
| Cited commits exist and are ancestors of `master` | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for af43a50f, b0ab7f60, 2dab7f31, 3ed8e15c, 99357694, 145a6468, adab4c7e, b7d821e3, 729878e3 | all exist and are ancestors | ok |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=remote=729878e3… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `729878e3…` | ok |
| Fleet-root leftovers | `git -C /home/vgpnk/Projects/shokunin status --porcelain` filtered on kake | only ` M .ufo/state/kake.report-baseline` (driver runtime, not lane work) | ok |
| Prompt carries template contract | `diff templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/kake-round-38.md)` | 22 differing lines, each a `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitution; hyaku §6 from line 141; prompt committed 01:05:32, 2 s before launch | ok |
| Commit order | `git log --format='%h %ad %cd' af43a50f..729878e3` | b0ab7f6 01:14:15 → 2dab7f3 01:28:54 → 3ed8e15 01:38:59 → 9935769 01:39:18 → 145a646 01:40:21 → adab4c7 01:43:03 → b7d821e 01:45:02 → 729878e 02:02:39 (all -03:00) | ok |

Status: real report with checkable commits → `ok`.

Defects (status-neutral, routed below):
- The QUALITY (j) check (`criteria/control_consequence_check.py`) landed at `145a6468` (01:40:21),
  after the build `3ed8e15c` (01:38:59). Its round-38 green depends on C2's own class text: lines
  near 279 print "not a control for this" for the four 20-of-20 receipts. `w2/CriticReclassification.md` item 6
  shows that renaming one receipt to `control-…` flips it to exit 1.
- Wave-2 mutant tools and receipts (`CriticKeyExpectations`, `MutBuildTool`) exist only under
  `/fast/scratch/hyaku/kake-r38w2/` (xfs, not tmpfs, but outside any repo). The committed reports carry their
  sha256. The integrator re-hashed the four reference mutants and read their receipts there; they match (below).

## Claims (step 2)

### C1 — operability (tool repair), counter v2, `met: passed >= 19 of 20 sealed cases`

Withdrawn before any build at `2dab7f31` (control call dispatched 04:15:37Z, wave 1 04:29:52Z,
`ctl-dispatched-at.txt`, `w1-dispatched-at.txt`). This is a gate reject, not a claim. Re-derived:
`jq -s '[.[].passed]|{n:length,at20:(map(select(.==20))|length),ge19:(map(select(.>=19))|length)}' verification/mutref/M*.json`
→ `{"n":42,"at20":13,"ge19":29}` (29 met, as corrected; the first table said 28). Control receipts
`control-{CtlBaseWrapper-care,CtlLabelShortcut-delegate_ceiling,CriticPredicate-rulepatch,CriticPredicate-rulepatch_pct}.json`
each read `passed 20, met true`. The withdrawal applied C1's declared consequence. **Agree.**

### C2 — operability (tool repair), counter v3, `met: passed >= 20 of 20 sealed cases`

Evidence-verified (lane-owned counter `sealed_count_v3.py`; not executed).

| Re-derivation | Command | Observed |
|---|---|---|
| Base tool bytes | `git show af43a50f:scripts/robots_audit.py \| sha256sum` | `944d2f51f396…bf1d3e5` |
| Build bytes (= tip) | same at `3ed8e15c` and `729878e3` | `f4d057c4afac…f36baace` both; `git show --stat 3ed8e15c` → only `scripts/robots_audit.py` |
| Counter v3 frozen | `git show {2dab7f31,729878e3}:.ufo/waves/round-38/sealed_count_v3.py \| sha256sum` | `28b120a5…0f38f9e4` at both; `PREDICATE = "met: passed >= 20 of 20 sealed cases"` (line 66), `met = len(rows) == CASES and passed >= TARGET` (line 271), `KEY_SHA256 = "749ef6a6…"` (line 62) |
| Key sealed until reveal | `git cat-file -e 2dab7f31:…/sealed/cases_v3.json`; `git show 99357694:…/cases_v3.json \| sha256sum` | absent at the declaration; `749ef6a6…77b63aa6` at reveal = pin |
| Before receipts | `jq -c '{passed,cases,met,predicate,toolSha256,counterSha256}' verification/c2-{at,keyrev-at}-{af43a50f,b0ab7f60,2dab7f31}.json`; `.exit` | each `passed 8 of 20, met false`, tool `944d2f51`, counter `28b120a5`, exit 1 |
| After receipts | same on `c2-at-3ed8e15c.json`, `c2-keyrev-at-3ed8e15c.json` | `passed 20 of 20, met true`, tool `f4d057c4`, counter `28b120a5`, exit 0 |
| Reveal refused | `c2-keyrev-at-99357694.json/.exit` | `passed null`, exit 2 |
| v3 controls | `jq .passed verification/v3/{Ctl*,CriticPredicate*,base*}.json` | base 8, all_false 0, constant_clean 0, junk 0, no_reader 1, label 16, stdlib 13, min wrapper 14; **CtlBaseWrapper-care 20, CtlLabelShortcut-delegate_ceiling 20, CriticPredicate-rulepatch 20, rulepatch_pct 20** (all `met true`) |
| v3 mutants and ablations | `jq -s '[.[].passed]\|{n:length,max:max,min:min}' verification/v3/mutref-M*.json`; `v3/A*.json` | 42 mutants 16–19, none at 20; ablations 18,18,16,16,16,16,18,18 |
| Where the four 20s were read | `git show --name-only --format= 2dab7f31 \| grep 'v3/'` | the four v3 receipts (20/20) and their v2 receipts (20/20) both land **in the declaration commit `2dab7f31`** |
| C1 control list and kill rule | `git show b0ab7f60:SCORECARD.md \| grep -n 'cheapest-wrapper\|no reclassification'` | line 2168 "a cheapest-wrapper shortcut around the base tool"; line 2171 "…or withdrawn; no reclassification of the control is an option." |
| C2 class text | `git show 2dab7f31:SCORECARD.md` lines 2237, 2243, 2250 | 2237 "Measured with `--tool-file` before this declaration"; 2243 "Control classes, named before any v3 control score is read as a control"; 2250 "…rules is a build, whatever its packaging (patch, wrapper, rewrite); the four such tools above are recorded as builds that reach the target, not as controls." `CriticReclassification` item 2: `git grep -c 'implements all three' b0ab7f6` → no match anywhere in the tree |
| Untested declared sentences | `sha256sum /fast/scratch/hyaku/kake-r38w2/CriticKeyExpectations/mutants/m_*.py`; `jq -c '{passed,met,counterSha256,toolSha256}' m_*.json` | m_emptyq `ed00b962`, m_barepct `f20d1bf8`, m_explicit `e11073ae`, m_unguarded `e7907567` (= the committed report); each `passed 20, met true`, counter `28b120a5`. Each breaks one clarification declared in C2's text at `2dab7f31` (`/robots.txt?` empty query; bare `%`; explicit `Disallow: /robots.txt`; the 20 s bound) |
| Build mutants | `w2/MutBuildTool.md` table | 6 of 36 build mutants survive both the 194 selftest and key v3 (H03 sign, H04 truncation of short integers, `_` rejected, U+00A0 rejected, implicit allow https-only, implicit allow below a directory) |

The re-derivation agrees with the report: **8 → 20 of 20, counter and key frozen before the build,
measured met.**

**Ruling under §6 item 9 (prompt lines 357–360): C2 is not admitted.**

1. **The class was not frozen before data.** The sentence that keeps the four tools out of the
   control set ("a tool implementing all three rules is a build … not as controls",
   `2dab7f31:SCORECARD.md:2250`) first appears in the commit that also lands their scores. They had
   scored 20/20 under v2 and 20/20 under v3, and the declaration itself says the v3 scores were
   "measured … before this declaration" (:2237). "Named before any v3 control score is read *as a
   control*" names the class after the score was read. It does not name it before data.
2. **This changes the rule after seats scored.** The prompt says: "A rule changed after any seat
   has scored is not the claim's rule." `CtlBaseWrapper`, `CtlLabelShortcut` and `CriticPredicate`
   are seats, and their tools scored first. C1's declaration made the wrapper family a control
   (:2168) and forbade reclassification (:2171). It allowed two answers to a control that met the
   predicate: redesign the counter or target, or withdraw. C2 repeats C1's surface and amendments.
   Its v3 redesign leaves all four tools at 20, so what answers them is the relabel alone. The
   lane's own QUALITY (j) (`corpus/QUALITY.md:926-929`) allows a reclassification only "unless the
   declaration named that class beforehand", and no declaration did before those seats scored.
3. **Precedent.** The round-37 closure (`round-37-verifier-spotcheck.md:65-75`) refused the same
   argument, "this control does not skip the claimed work", as a rule change after a seat had
   scored. Closures have to rule the same way on the same argument.
4. **The substance does not rescue the claim's rule.** `w2/AblateBuilds.md` (12/12 ablations → 16)
   persuades me that the four tools are correct implementations, and v3 closes the 13 v2 false
   passes (v2 mutants at 20: 13 → v3: 0, re-counted above). So a full-rule wrapper was never a
   work-skipping control, and C1's list was mis-specified (the lane's own QUALITY (n)). The honest
   remedy for a mis-specified list is to withdraw (done for C1) and re-declare with the classes
   frozen before any tool is scored, in a later round. Relabelling the already-scored tools in
   the same commit is not that remedy.
5. **The build/control line cannot be measured.** The class turns on "implements all three rules".
   Four reference mutants, each breaking one clarification that C2 itself declared, and six build
   mutants (sign or truncation of short integers, `_`, U+00A0, https-only and below-directory
   implicit allow) all reach 20 of 20. So the counter cannot tell a tool that implements the rules
   as declared from one that breaks a declared sentence. Under C2's own class (6) ("implements at
   most two of (h), (i), (k)", read with the clarifications as part of each rule), such a tool
   meeting the predicate withdraws C2. I give this as supporting weight only: wave 2 found these
   tools after the build, and the 42-mutant coverage bar C2 declared holds.

This is a rejection, not a finding of harm. The build tool, the 194 selftest (base fails exactly
the 45 new fixtures, `w2/ReviewSelftest194.md`), the real-run 7/7 against 1/7, and the independent
implementation at 20/20 stand as non-claim work.

### Harm check

`git diff --numstat af43a50f 729878e3 -- SCORECARD.md SKILL.md PROVINCE.md LOG.md SHONEN.md corpus/QUALITY.md corpus/SOURCES.md corpus/README.md corpus/knowledge`
→ LOG 17/0, PROVINCE 19/0, SKILL 11/0, QUALITY 35/0, README 1/0, SCORECARD 264/2 (the two
capability rows gain "not admitted", routed defect 1), SOURCES 5/1 (S034 `used-by`, logged
old→new), knowledge 41/1 (source line, logged in "Wave-2 corrections"). No axis row was edited.
Harm receipts (`jq` on `verification/harm/*.json`): round-37 counter on build 28/28 (tool
`f4d057c4`); robots selftest 137/137 at `3ed8e15c`, 194/194 at `145a6468`; source_recheck selftest
106/106, hardening 9/9, round-36 counter 28/28 (tool `6629d800`). No axis harmed.

### Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| operability | unprovable-but-better | The tool gains (h), (i), (k): v3 8 → 20, selftest 137 → 194 with the base failing exactly the new 45, real run 7/7 against 1/7, independent implementation 20/20. The claim's rule is not proven, because its admitting class was written after seats scored (above) |
| freshness | unprovable-but-better | `source_recheck.py` 16 MiB body cap and `MemoryError` mapping. Hardening 9/9 and selftest 106/106 come from the lane's committed receipts. Non-claim, with no frozen measurement |
| depth | unchanged | no claim |
| coverage | unchanged | no claim |
| calibration | unchanged | no claim |
| adjacency | unchanged | no claim |

## Discernment spot-check (step 3)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S098 RFC 3986 §§2.1–2.3 | admit, A, spec, mined | `curl -sL https://www.rfc-editor.org/rfc/rfc3986.txt` (2026-10-23T05:07:16Z, HTTP 200, sha256 `3102dae4…2b2d683` = lesson and row) | agree | Quote at lines 720–721 verbatim (17 words, ≤25). `gen-delims`/`sub-delims` (681–684) and `unreserved` (724) plus §2.1 `%` give exactly rule (i)'s allowed ASCII set. The scope differs from S029 §3 and S089 §5.2 as the row says |
| S099 RFC 9309 §§1–5 | admit, A, spec, mined | `curl -sL https://www.rfc-editor.org/rfc/rfc9309.txt` (05:07:18Z) | agree | Line 202 "Crawlers MUST use case-insensitive matching to find the group that…" carries the quoted fragment. Line 259 "The /robots.txt URI is implicitly allowed." grounds (k). The broader scope justifies a superseding row |
| S101 WHATWG URL Standard | reject, A, spec | `curl -sL https://url.spec.whatwg.org/` (05:07:17Z, HTTP 200, sha256 `08cb42a9…9656be4` = row) | agree | Quote "The URL parser takes an arbitrary scalar value string and returns either failure or a URL." is present (16 words). The parser also says "Remove any leading and trailing C0 control or space from input" and "Remove all ASCII tab or newline from input", so it normalizes where (i) rejects. The contract is RFC 3986 and the tool uses `urllib.parse`. The reject and its flip hold |
| C1 withdrawal (`2dab7f31`) | withdrawn before any build | `verification/control-*.json`, `mutref/M*.json` | agree | Controls of both declared kinds met the predicate, and C1 was withdrawn 58 s before wave 1 as declared |
| C2 control classes (`2dab7f31`) | admit for measurement; full-rule tools "builds" | `git show 2dab7f31:SCORECARD.md` :2237–2251; `b0ab7f60` :2168–2171 | disagree | Class written after those tools scored 20 (v2 and v3); see C2 ruling |

New SOURCES row re-opened: S098 (row line 106, `git show 729878e3:corpus/SOURCES.md`). Its scope
and anchor match the fetched text, and the retained-text sha256 equals today's fetch. The quote
lives in the lesson Gate (17 words). Rows 97 → 101 (`grep -c '^| S[0-9]'` at base and tip).
Census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kake` → exit 0. It gives five `W04` duplicate-URL warnings (S033,
S088, S092 carried; S098 and S099 new, as the report says) and `kake ok`.

## Trend verdicts

- **expansion: unchanged.** I agree with the lane. The round repaired an existing tool and grew
  the existing `robots-txt-rules.md` (41 lines). The three new mined rows (S098–S100) deepen held
  ground; they open no new area (PROVINCE "Round-38 robots audit repair step").
- **quality: improved.** Routed defects 1, 3 and 5 landed with receipts (SCORECARD round-37
  correction; (j) check; `pinned_selftest.py` with `toolSha256` in the harm receipts). Counter v3
  closes 13 v2 false passes (re-counted: v2 mutants at 20 = 13, v3 = 0). The robots selftest grew
  137 → 194, and the S098 and S101 retained digests match a fresh fetch.
- **discernment: unchanged.** For: C1 was withdrawn under its own consequence, and the source
  admits and the S101 reject all agree on re-open. Against: C2 answered C1's wrapper controls by
  relabelling them as builds after they scored, which repeats the round-37 mistake in a new form.
  The new (j) check encodes that relabel by file name, so its green is circular. The lane
  disclosed the issue as contested and did not self-admit, which keeps the trend from `harmed`.

## Routed defects (kake owes, next round)

1. Append a SCORECARD correction: C2 (round 38) is not admitted at closure. The control-class text
   at `2dab7f31` was written after the four full-rule tools scored. Keep counter v3 and key v3 as
   C2's rule of record; append, never rewrite.
2. Any re-claim of (h), (i), (k) must freeze its control classes, including any build/control
   boundary, before any tool is scored under the counter it will be judged on. Or declare it
   exploratory.
3. Put the untested declared sentences into the selftest or the key before a new claim on this
   tool: `/robots.txt?`, bare `%`, explicit `Disallow: /robots.txt`, the 20 s bound on a 64 MiB
   literal, and the six `MutBuildTool` survivors (H03, H04, `_`, U+00A0, https-only, below-directory).
4. Make `control_consequence_check.py` classify by declaration, not by file name or by the class
   text under test. `MutCcCheck` shows 11 of 15 mutants survive.
5. Commit the wave-2 mutant tools and receipts (or a bundle) that the reports cite from
   `/fast/scratch/hyaku/kake-r38w2/`.
6. The report's carried items stay open: source_recheck `moved` + `check_invalid` on oversized
   bodies, lone-surrogate URLs, bracket hosts, S011 cited outside its scope, symlinked manifest
   directory, U+FFFD per byte, duplicate JSON member names, two counter harm receipts without
   `toolRevision`, forgeable `pinned_selftest.py` runner field, `timeline_check` receipts without
   their invocation.

SHONEN: all four boxes are `[~]` with pointers a non-author can follow (the SKILL round-38
amendment, LOG round 38 with `realrun/build-3ed8e15c/summary.json`, wave-2 re-runs from written
commands, the PROVINCE round-38 step). They look checkable by a non-author; promotion is
operator-owned.
