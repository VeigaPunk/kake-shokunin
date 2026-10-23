# CriticPredicateIdentity — §6 item 9 review
Axes: freshness (declared measurement/provenance); operability (counter prerequisites). Advisory findings only; no round judgment or admission.
Attacked: predicate identity and freeze chronology at 3555f63f, 9d81c75c and cd321279. No sealed tree touched, counter executed, network request, subagent, or tool installation.

## Per-bullet conformance
1. **Conforms as a declaration, not an exercised closure replay.** One concrete after-state, `met` true, and one counting command are specified (SCORECARD.md:1579-1581). The reveal/key is a prerequisite; I did not re-derive a build score.
2. **Conforms for the bounded scored value.** Pasted code: `CASES = 28`; `for case in key["cases"]:`; `met = len(rows) == CASES and passed >= TARGET` (sealed_count.py:63,216,231). This is not proof of correctness beyond those cases; “shows the contract ... is implemented” (SCORECARD.md:1594) should be qualified accordingly.
3. **Conforms / not applicable.** This is not a calibration claim: `**C1 — freshness (capability): offline source re-check audit` (SCORECARD.md:1573).
4. **Conforms to the claim cap.** Pasted declaration: `One claim.` (SCORECARD.md:1564). Two is a preference, not a minimum; no third claim needs an independence justification.
5. **Conforms: no target narrowing found.** All three source versions have `CASES = 28`, `TARGET = 25`, and `met = len(rows) == CASES and passed >= TARGET`; all 52 receipts have cases 28 / target 25 and consistent `met`. The key changed, but the numerical target was not narrowed.
6. **Does not conform to the before-freezing chronology; observed control discrimination does conform.** 3555f63f calls the predicate frozen but contains zero verification receipts. Receipts first enter at 9d81c75c; the five control-seat tools are based on that later commit (SCORECARD.md:1682-1687). Current base/constant/all-false/no-reader/naive/shortcut scores are 0/0/0/8/12/9, all below 25. Calling the later wave “pre-freeze” does not precede the already committed freeze.
7. **Does not conform to the after-any-seat-scored freeze; literal label identity also differs.** The numeric condition is unchanged, but the pinned oracle changes after the shortcut seat scored. “Before any build” is weaker than the binding “after any seat has scored” prohibition (prompt:357-360). Evidence and the harmless label mismatch are separated below.
8. **Conforms to surface-based naming, scoped to the declaration.** Pasted text: `freshness — a new tool (operation) for drift detection of SOURCES.md rows` and the absent-tool `git ls-tree` counterfactual (SCORECARD.md:1568-1571). No live registry freshness or axis-rating improvement was verified here.

## Strongest counterexample: same tool, changed oracle after scoring
The same revision `f06b0e15ca08eea6e2e6cc6dc5fbe4b3bff79561`, same tool SHA-256 `f6cb0aa43c6d720caee97104fa121fdc940f64425133a05bc30ca2b871c7bcc9`, scores 17 then 9:
- verification/v2/control-CtlShortcut.json:4-11: counter `1bf16734…162c`, passed 17, target 25, met false.
- verification/control-CtlShortcut.json:4-11: counter `88ec5914…ff8e`, passed 9, target 25, met false.
- Both matching .exit files contain `1`. These are inspected historical outputs, not my executions.
Pasted v2→v3 diff (full copy: sandbox/v2-v3.diff:19-27):
```diff
-KEY_SHA256 = "a690d39e912cf641baa14f101f461e31304ac336c59a41c9689aacf91e02f9ca"
+KEY_SHA256 = "44c94838f31af6740a3f1bb4123abe6cbb8df0bbdd3414de7acbb3838863ef1d"
```
SCORECARD.md:1689-1696 explicitly attributes the redesign to the scored shortcut and describes added negative quote checks/content-type rotations. Thus identical case count, case ids and predicate text do not mean identical measurement. I did not inspect either key's contents.
Git chronology (`%cI`, all -03:00): 3555f63f 2026-10-22T22:20:56 declaration; 9d81c75c 22:24:43 jailed v2 + receipts; cd321279 22:33:53 key v2/counter v3 + rescores.

## Identity and v1→v2 checks
Pasted plan/code/receipt labels:
```text
SCORECARD.md:1577: met: passed >= 25 of 28 sealed cases
sealed_count.py:65: PREDICATE = "passed >= 25 of 28 sealed cases"
verification/* (52 JSON receipts): "predicate": "passed >= 25 of 28 sealed cases"
```
The plan sentence is unchanged between the two requested commits; original declaration content differs only by an appended separator blank line, not an in-place rule edit (sandbox/declaration-boundary.json). Logically the labels match after stripping `met: `, but the claimed literal sameness is false.
No v1 receipt presented as v2 was found: 52 current receipts = 45 exact v3 counter hashes + 7 exact v2 hashes; the 37 JSON receipts committed at 9d81c75c all name the v2 hash. None names v1. Counter originals byte-match preserved v1/v2 files. This establishes recorded provenance, not that undocumented v1 runs never happened.
v1 SHA-256: `28169d958bf38818127e247e62c0e0fe2d95223edeea44908e5c39b1d2979728`.
v2 SHA-256: `1bf16734a3c1f8149f6fb2fbb811cccc5b74b5cd99fda7409d2d4443cd2f162c`.
v3 SHA-256: `88ec59140258ce759107b7472fdd07a005b7c1bb8b3ba5218347e4518342ff8e`.
v1→v2 leaves cases pin, constants, projection and judge unchanged. Changes are confinement-related, not merely a wrapper: bubblewrap, fixed `/usr/bin/python3` and PATH/environment, plus an early missing-bwrap/interpreter exit-2 guard. Full diff: sandbox/v1-v2.diff:1-68. Pasted dependency hunk:
```diff
+    if shutil.which("bwrap") is None or not Path("/usr/bin/python3").is_file():
+        out["error"] = "bwrap or /usr/bin/python3 missing: the tool cannot be jailed"
+        print(json.dumps(out, indent=1))
+        return 2
```
[INFERENCE] That guard can change an absent-tool baseline from a scored miss to cannot-evaluate on a host without bwrap. No such host probe was run. No scoring/threshold change beyond confinement and its prerequisites was found in v2.

## Smallest safe correction
Treat v3/key-v2 results as explicitly post-data supplementary evidence, not the unchanged frozen rule. Preserve original pins and receipts and route the freeze defect to the non-author closure; disclosure/re-scoring cannot retroactively satisfy §9. Do not restore an unsafe runtime merely to hide that defect. The `met:` mismatch is a fixable presentation defect: append the mapping, without rewriting historical receipt labels. Future declarations should share an exact predicate string and finish control scoring before asserting a freeze. The chronology defect is substantive, not cured by that wording fix.

## Reproduction and retained evidence
`sandbox` = `/fast/scratch/hyaku/kake-r36w1/CriticPredicateIdentity/`.
Exact executed command, exit 0:
`timeout 120s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r36w1/CriticPredicateIdentity/tmp python3 -B /fast/scratch/hyaku/kake-r36w1/CriticPredicateIdentity/identity_audit.py`
Observed: receipts 52; predicate labels 1; versions v3=45/v2=7; threshold/boolean mismatches []; historical v2 receipts 37, all v2. Exact read-only Git argv and exit-0 records are in sandbox/identity-audit.json:961-1467; each subprocess had a 20-second timeout.
Also executed, exit 1 (differences, not failure): `timeout 30s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --no-index -- .ufo/waves/round-36/sealed_count_v1.py .ufo/waves/round-36/sealed_count_v2.py`.
Same command with operands `sealed_count_v2.py` and `sealed_count.py`, exit 1. The full pasted diffs are retained in the sandbox.
Evidence SHA-256: identity-audit.json `4fe5309f7d37608d5bf5d80b4f42935ad017622b6b6de74f02e79037e1d49f3c`; v1-v2.diff `be211d39ffaee821e86a6160b4ad63524a18c62448bb4118557727a28e052567`; v2-v3.diff `675f89165cc6cb46ca510c6ce72aac2dc974591317d56212505c144d95a7491c`.
Not verified: sealed-case content, tool behavior, later build receipts, key reveal/replay, or any axis gain. No processes remain from this review. Lane writes were confined to this report.
