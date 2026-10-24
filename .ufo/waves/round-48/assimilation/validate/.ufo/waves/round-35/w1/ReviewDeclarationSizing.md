# ReviewDeclarationSizing — round-35 declaration vs claim-sizing rules (item 9)

Axes: operability + freshness. Leaf seat; no subagents; no tools installed (none needed).
Never touched /fast/scratch/hyaku/kake-r35/sealed/ (counter read statically; no counter run).
Sandbox clone: /fast/scratch/hyaku/kake-r35/w1/ReviewDeclarationSizing/clone at 318561efa67206699fdaf259ffb86e39f2d916a8 (lane working tree not read as evidence).

## Rule verdicts (prompt section 6 item 9 + assignment deltas)

1. PASS — one concrete after-state per claim, re-derivable by one command over committed bytes.
   C1: `passed` >= 22 of 24 (SCORECARD.md:1375); C2: `met` true with five enumerated conditions (SCORECARD.md:1376).
   Counter reads only committed bytes: tool/entry/SOURCES/sources via `git show <rev>:<path>` (sealed_count.py:142,218,227,230,239); key via `--key-revision` (also committed) or `--key-file`. One pasteable command per claim; receipts show the same JSON fields (`passed`, `met`, `probesPassed`).
2. PASS (one residual) — no universal clause the counter does not enumerate.
   C2 conditions are constants in code: 24 cases/22 target (sealed_count.py:54), 1500 words, 0.25 copied, 3 cites, 9 of 12 probes; nine pinned texts (sealed_count.py:62-72).
   Residual: SCORECARD.md:1393 "Every other round-34 rule, reason name, verdict and exit code is unchanged" is a universal the counter enforces only through the 12 sealed round-34 cases; coverage of all round-34 rules is not publicly enumerable (cases sealed). It scopes interpretation, it is not the declared after-state (>= 22 of 24 is), so not a sizing violation. Mitigation: round-34 selftests remain runnable at any revision; closure still owes independent verification.
3. N/A — no calibration claim declared (both claims are capability-repair and sourced-learning; nothing to check).
4. PASS — exactly 2 claims (prefer 2). Causally separable, verified in code: run_c1 reads only TOOL (sealed_count.py:142); run_c2 reads only ENTRY, SOURCES.md, sources dir (sealed_count.py:218-241). Neither reads the other's artifacts; declaration states the same (SCORECARD.md:1413-1414).
5. PASS — no target narrowed after landing. `git diff 81d9fd7 318561e -- SCORECARD.md` only appends the controls section (27 added lines, 0 removed); declaration table bytes unchanged; branch tip is 318561e (no later commit).
6. PASS — target not reachable by a do-nothing control; controls scored and committed before any build.
   10 receipts at .ufo/waves/round-35/verification/control-*.json, each with matching .exit=1 and met=false: c1 base 14/24, c1 at declaration 14/24, lookup dcef39b5 7/24, constant-clean 7/24; c2 base 0/12, at declaration 0/12, hollow 0cce15f0 0/12, junk 0/12 (copied 0.0), keyword 3/12, RFC transcript 8/12 (copiedShare 0.9951). No control reaches >= 22 or met=true.
   No build bytes at the controls commit: `git cat-file -e 318561e:corpus/knowledge/security-txt-publishing.md` exit 128; `git diff --stat 16a6b8b 318561e -- scripts/link_preview_audit.py` empty, exit 0.
   Commit order verified: 81d9fd7 2026-10-22 19:08:40 -03 (declaration) is ancestor of 318561e 19:09:56 -03 (controls), `merge-base --is-ancestor` exit 0; base 16a6b8b 18:54:04 -03.
7. PASS — counter frozen, unchanged after data. `git diff 81d9fd7 318561e -- .ufo/waves/round-35/sealed_count.py` empty; sha256 of committed bytes c4d58daea09d27a15f7792aae320cd56ac44dc1a6911307d6320f0a2c04349ef equals `counterSha256` in all 10 receipts; no commit after 318561e.
8. PASS — no target value published before the build. Sealed keys absent from the lane at both commits (`git ls-tree <rev> .ufo/waves/round-35/sealed/` empty for 81d9fd7 and 318561e); counter refuses to measure a revision holding a key file (exit 2, sealed_count.py:271-274) and refuses key sha mismatch (sealed_count.py:268). Declared values are thresholds, not measured results; pre-build measured values are before-values at base (14/24, met false) plus the disclosed private reference patch (24/24, outside the lane, not the landed tool) — a reachability disclosure, not a declared after-state.
9. PASS — the sourced claim rests on rows opened this round. sources/receipts.json: accessedUtc 2026-10-22T22:00:48Z-22:02:19Z (S006, S078-S085), before the declaration commit 22:08:40Z; all nine texts sha256-pinned in the counter (sealed_count.py:62-72) and `copied` fails if any is altered at the measured revision (sealed_count.py:227); a good cite requires a Registry row with status mined, opened exactly `2026-10-22`, and the entry path in used-by (sealed_count.py:241).

## Commands run (exit codes)

- `git clone -q <lane> <sandbox>/clone && git checkout -q 318561e` — exit 0; `log --oneline -8` shows 318561e -> 81d9fd7 -> 16a6b8b; `merge-base --is-ancestor 81d9fd7 318561e` exit 0.
- `git diff --stat 81d9fd7 318561e` — 25 files, 955 insertions, 0 deletions (receipts, bundles, SCORECARD append only).
- `git diff 81d9fd7 318561e -- .ufo/waves/round-35/sealed_count.py` — empty (frozen).
- `git cat-file -e 318561e:corpus/knowledge/security-txt-publishing.md` — exit 128 (no build).
- `git diff --stat 16a6b8b 318561e -- scripts/link_preview_audit.py` — empty, exit 0 (no build).
- `sha256sum <clone>/.ufo/waves/round-35/sealed_count.py` — c4d58dae… (matches all 10 receipts).
- `git ls-tree <rev> .ufo/waves/round-35/sealed/` for 81d9fd7 and 318561e — empty both.
- Receipts loop (python json over control-*.json + .exit) — 10 rows, all exit=1, met=False, counter c4d58dae, values as in the SCORECARD controls table.

## Findings by severity

- Blocker/major: none.
- Minor (residual, disclosed): the cite condition is satisfiable by well-formed junk rows opened 2026-10-22 (the junk control passed cites with probes 0/12); the counter's own note ("cites is necessary only", SCORECARD controls section) and the Gate + non-author row-truth read carry this. Cite range S078-S099 is wider than the opened set S078-S085; a fabricated S086+ row dated today would satisfy cites but not row truth.
- Minor (counter-code note, fails safe): declaration says probes are "case-insensitive regexes", but the counter lowercases the entry text and applies the sealed regexes unchanged (sealed_count.py:242-243); an uppercase letter inside a sealed probe regex could never match. Direction is undercounting, so it cannot inflate the result; not checkable without the sealed probes.

## Residual risk and verification gaps

- I did not execute either counter (the run must read sealed key inputs; leaf seats may not touch them). "Command re-derives the value" is verified by static code reading plus the ten committed receipts, not by my own run.
- Key sha256 pins vs actual sealed keys: not verified directly; inferred because all controls exited 1 with full JSON (load_key succeeded, so both keys matched their pins at control time).
- Coverage of the 12 sealed round-34 cases over all round-34 rules: unverifiable from public bytes (see rule 2 residual).
- Target reachability for C1 rests on the L1's disclosed 24/24 reference patch in a sandbox outside the lane; I could not and did not inspect it.

Verdict (advisory): the round-35 declaration conforms to every claim-sizing rule in item 9 that applies; no rule fails.
