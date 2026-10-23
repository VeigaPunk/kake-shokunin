# CriticKeyV2Change — advisory falsification, not an admission ruling
Axes: freshness (source-drift detection) and operability (the audit and its measurement).
Attacked: key v1→v2 / counter v2→v3 as post-score rule replacement and possible loosening.
Sandbox: `/fast/scratch/hyaku/kake-r36w2/CriticKeyV2Change`; clone pinned to `f3a38bf8e68f6cee386125d34b5e95ac9b2df66e`.

## Finding: two cases became easier; a defective tool crosses the target
I AST-derived a diagnostic from the public reference, adding only HTML-branch casefolding of text and quote; plain-text matching remains case-sensitive. This violates contract (d), not a permitted implementation tradeoff.
`evidence/html_casefold_only.py:176-179` below the sandbox is the mutation; SHA256 `ba39e5d3a1c3a73f91d4d4c3584a8cc5dde1f82fce099ef31edd8eb6bb824173`.
Old key/counter: **24/28, met false, exit 1**, failing k13–k16. New key/counter: **26/28, met true, exit 0**, failing only k13/k15.
**k14 and k16 became easier:** x4 changed `text/html; charset=utf-8`→`text/plain; charset=utf-8`; their case-sensitive negative expectations stayed identical. The same HTML-only defect no longer affects those checks.
Evidence: lane `sealed/cases.json:1425,1589` under `.ufo/waves/round-36/`; old file has the same line numbers. Sandbox `evidence/commands.json:58-120` records exact commands/exits and the adjacent named JSON files contain complete per-case receipts.
This disproves a monotonic-tightening interpretation, not the actual build: **4d5b3d55 scores 28/28 under BOTH versions** (exit 0/0). The diagnostic was written after reveal and is not a blind pre-freeze control.

## Case-by-case diff
Full structured diff: `/fast/scratch/hyaku/kake-r36w2/CriticKeyV2Change/evidence/case-diff.json` (SHA256 `6e93247e5ab7035a858369628874de121728bae2b947d96ba06bf1774ce9f73d`). No existing check or body removed; no existing body bytes changed. Twelve checks added; 35 existing contentTypes replaced.
For c/d, all replacements below start at H=`text/html; charset=utf-8`. N=`text/html`; U=`text/html;charset=UTF-8`; Q=`TEXT/HTML; Charset="utf-8"`; X=`application/xhtml+xml`; P=`text/plain; charset=utf-8`.
- k01, k02, k03, k04: unchanged (a).
- k05, k06, k07, k08: unchanged (b).
- k09: 7→7 checks; x2=N, x3=U, x4=Q, x6=U, x7=N.
- k10: 7→7; x1=N, x2=U, x3=Q, x5=X, x6=Q, x7=U.
- k11: 7→7; x1=U, x2=Q, x4=N, x5=U, x7=Q.
- k12: 7→7; x1=Q, x3=N, x4=U, x5=X, x6=N.
- k13: 4→4; x1=Q, x2=U, x3=N.
- k14: 4→4; x2=Q, x3=U, **x4=P**.
- k15: 4→4; x1=N, x3=Q, x4=U.
- k16: 4→4; x1=U, x2=N, **x4=P**.
- k17: 4→6; add x5 `text/plain` reference-negative and x6 `application/xhtml+xml` script-negative.
- k18: 4→6; add x5 `Text/Plain; charset=utf-8`, x6 `Application/XHTML+XML; charset=utf-8`, same negative classes.
- k19: 4→6; additions as k17.
- k20: 4→6; additions as k18.
- k21: 4→5; add x5 `text/html; charset="Windows-1252"`, UTF-8 body expected quote_missing.
- k22: 4→5; existing x4 `text/html`→`text/plain`; add x5 `text/plain; charset=ISO-8859-1`, same negative class.
- k23: 4→5; add x5 `text/html; charset=us-ascii`, same negative class.
- k24: 4→5; existing x4 `text/html`→`text/plain`; add x5 `text/plain; charset="latin1"`, same negative class.
- k25, k26, k27, k28: unchanged (g).
Existing expectations remain; k17–k20 add x5/x6 quote_missing, k21–k24 add x5 quote_missing. Case exits/verdicts unchanged. Top-level key version 1→2; target remains 25.
Counter executable ASTs are identical after removing the module docstring and normalizing KEY_SHA256; the pin selects materially different tests, so numeric-predicate identity alone is not rule identity. Sandbox `evidence/identity.json:3-13` carries full hashes (old key `a690d39e…`, new `44c94838…`; counters `1bf16734…`→`88ec5914…`).

## Chronology and arguments both ways
All following commit times are 2026-10-22, UTC−03, from `%cI` (not author dates).
- `3555f63f` **22:20:56**: declaration/key-v1 pin; author date is 20:54:59, not landing time.
- `9d81c75c` **22:24:43**: counter v2, base/reference/34-ablation receipts before a build.
- `cd321279` **22:33:53**: key-v2 pin/counter v3 plus retained v2 control scores and v3 rescoring.
- Builder wave dispatch: **22:34:22** (`w1-dispatched-at.txt:1` = 2026-10-23T01:34:22Z); builder report `w1/ExecToolBuild.md:3` identifies cd321279 as its contract base.
- `4d5b3d55` **22:54:39**: first committed source_recheck.py build; `fd1fb723` **22:55:08**: reveal and first committed build-score receipt; `f3a38bf8` **23:00:34**: measured-results writeup.
**Strict argument against:** prompt §6.9 (`/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-36.md:351-360`) forbids narrowing after landing and changing a rule after ANY seat scored. Five controls had scored v2; SCORECARD:1687-1698 admits that sequence. CtlShortcut was only 17/28, not the 25 target triggering the express fix-before-data clause. The key pin changed anyway, and the k14/k16 result proves an actual relaxation rather than merely more negatives.
**Strong argument for:** round-35 closure `corpus/lessons/round-35-verifier-spotcheck.md:80-91` explicitly treated control-only scoring as pre-data and accepted a redeclaration before the first build. Here v3 precedes even builder dispatch, and no committed build/after receipt precedes it. SCORECARD:1681-1704 openly declares the amendment. Constant/all-false/no-reader/naive remain 0/0/8/12; shortcut falls 17→9. The actual build still gets 28 on the original key, just as the round-35 measured build agreed across versions.
Further support for repairing the old key: the reference's `s_ctkey` ablation (assume hold whenever contentType differs from H) scores **28/28 old, 13/28 new** (exit 0/1). This is a retrospective diagnostic, NOT evidence that this particular control had been scored before v3; exact commands/receipts are in sandbox `evidence/commands.json:122-193`.
**Boundary for the canonical judge:** decide whether the round-35 control-only exception applies despite §6.9's literal wording and the reported control never reaching target. I do not resolve admission. The prior closure also routed “Do not loosen a counter in a version bump” at :190-193; current build agreement does not erase the newly demonstrated relaxation.

## Commands, evidence and smallest safe correction
Executed from the sandbox, exit **0**: `timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r36w2/CriticKeyV2Change/tmp python3 -B /fast/scratch/hyaku/kake-r36w2/CriticKeyV2Change/review_key_change.py`.
That script (SHA256 `fc37880692c7bbf06bff17c019a5601ff1525489183727b0c20499ae3dd72d61`) saves all SIX exact counter argv arrays, exits and summaries in `/fast/scratch/hyaku/kake-r36w2/CriticKeyV2Change/evidence/commands.json` (SHA256 `13f6e6c91cd7fa2ec389ec4720740fd6ac7d7186bd0e93740b16bdc55e00f138`). Each counter command has its own 150-second timeout; observed whole diagnostic duration 5.45 seconds.
Executed, exit **0**: `timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --format='%H %cI %s' -- .ufo/waves/round-36/ scripts/source_recheck.py`.
Executed with cwd=sandbox clone, exit **1** (differences): `timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff --no-index -- .ufo/waves/round-36/sealed/cases-v1.json .ufo/waves/round-36/sealed/cases.json`.
Executed with that cwd, exit **1** (docstring+pin difference): `timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff --no-index -- .ufo/waves/round-36/sealed_count_v2.py .ufo/waves/round-36/sealed_count.py`.
Smallest safe current correction is evidentiary: disclose k14/k16's lost HTML-negative coverage, preserve both measurements, and stop describing the pin bump as harmless solely because the predicate sentence is unchanged. Do NOT edit this round's key after these scores to cure the counterexample.
For a future pre-data declaration, preserve original HTML checks and add plaintext variants instead of replacing them; freeze an HTML-only casefold mutant below target. That is an instrument defect to fix, not a freshness-for-operability trade to accept.
Not verified: absence of unrecorded/private scoring, absolute wall-clock provenance, or private-tree state (never accessed). No network, installs, production edits, other-runtime/judge calls or background jobs; all started commands finished. Only the requested report is written in the lane.
