# CriticClaims — round 85, w1

Scope: author-side adversarial review, not independent closure, judgment, integration or publication approval. Base `bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7`; frozen contract supplied at `2f042c370b5f11b84d4f8c9e5d066517aef646b8`. Read host RULES, godspeed, contract and complete count.py before running the assigned checks. No production edits, VCS mutations, sibling/fleet writes, delegation, network requests or installs.

## Axes

- **Calibration (2, HOLD):** discoverable, truthful registry rows; do not promote row-shape completion into full gate conformance.
- **Freshness (10, HOLD):** bounded field-specific effective-token decoding; do not promote a ten-case numerator into arbitrary response-field equivalence or universal decoder conformance.
- **Operability / no harm:** preserve existing callers, historical evidence, experimental warnings and publishing boundaries. Neither score increase nor saturation is established here.
- Cross-cutting evidence fidelity: frozen before/after populations, source provenance, independent semantic expectations and clear author-side status.

## Executed controls and receipts

All receipts below are under `.ufo/waves/round-85/w1/CriticClaims/`; each JSON records exact argv, actual exit, stdout and stderr. Counter commands used absolute paths, cwd `/fast/scratch/hyaku/kake-r85/CriticClaims`, `TMPDIR` set to that directory, and `--work /fast/scratch/hyaku/kake-r85/CriticClaims/count`. Independent jobs ran concurrently. No clone was needed.

| Receipt | Actual result |
|---|---|
| `baseline-c1.json` | Frozen counter at base: exit 1, complete=0/3, missing=3, met=false |
| `baseline-c2.json` | Frozen counter at base: exit 1, cases=0/10, met=false |
| `c1-prose.json` | Prose-only assertion of complete registry: exit 1, complete=0/3 |
| `c1-shortcut.json` | Three structurally sufficient but bogus rows: exit 0, complete=3/3 |
| `c2-constant.json` | Constant `strict-origin`: exit 1, cases=3/10 |
| `c2-shortcut.json` | Canned input discriminator: exit 0, cases=10/10 |
| `c2-shortcut-counterexample.json` | Same canned decoder on `["no-referrer"]`: exit 0 but outputs `strict-origin`, not `no-referrer` |

Exact baseline argv shape (both claims were run):

`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7 --claim c1|c2 --work /fast/scratch/hyaku/kake-r85/CriticClaims/count`

For shortcut/prose/constant runs, omit `--revision` and replace `--root` with the corresponding absolute scratch fixture directory. Retained fixture bytes are in matching named subdirectories next to the JSON receipts; they are deliberately false synthetic controls, never production candidates. Counterexample argv and stdin are recorded verbatim in its receipt. Directory preparation (`mkdir -p`) exited 0.

## Counterexamples and smallest safe corrections

### C1: discovery is not truth or full conformance

**Counterexample.** Each synthetic row has the instrument filename in cells 1 and 3, arbitrary nonempty Kind/write-scope cells, `0=x 1=y`, literal `--selftest`, `.ufo/waves/nonexistent`, and owner `kake`. There are no actual instrument files or proof receipts in this fixture. It nevertheless scores 3/3.

**Evidence.** `count.py:26–38` parses all pipe-prefixed rows anywhere in SKILL.md. It does not restrict matching to a registry section, resolve commands/proof paths, check verdict truth, execute a selftest, inspect receipt bytes, validate write scope, or enforce experimental status. Complete-looking rows could also live in a fenced example. The executed shortcut uses ordinary rows, not that additional unexecuted variant.

**Impacted axes.** Calibration/evidence fidelity; operability if readers treat fictional receipts or selftest success as authorization. This is a measurement limit under the explicitly bounded contract, but false row content would be a fixable deliverable defect—not acceptable merely because the count is green.

**Smallest safe correction.** Keep frozen count.py unchanged. L1 must manually bind each new row to the actual entry command, truthful exit meanings, actual selftest invocation and retained expected-value/receipt paths, write scope and owner. Keep `policy_value_class.py` explicitly experimental and forbid publication approval. Report exactly registry discoverability 3/3, not D84 queue closure or full semantic/gate conformance. Append rows at EOF, following the existing registry's pinned-line-preservation convention; do not rewrite earlier authority.

### C2: ten frozen examples are memorisable

**Counterexample.** A seven-branch input recognizer defaults to `strict-origin` and special-cases only the frozen distinctions. It passes all ten cases, including reversed order, without a token decoder, valid-input validation, usage handling or selftest. The one-token input `["no-referrer"]` decisively fails immediately afterward.

**Evidence.** `count.py:11–21,39–54` runs only ten successful-input examples and checks parsed JSON equality plus exit 0. It does not exercise three valid tokens at all (`no-referrer-when-downgrade`, `origin-when-cross-origin`, `strict-origin-when-cross-origin`), unsupported input, usage=64, selftest isolation/exit assertions, or the retained control-pair trial. JSON parsing also does not enforce a unique serialized key or exact textual framing. There is no per-process timeout. These latter observations are static, not additional executed attacks.

**Impacted axes.** Freshness, calibration and operability if a green count is represented as complete implementation evidence. Opposite-order cases defeat constant output, but not canned input discrimination. The frozen numerator is valid as a bounded measurement, not proof of universality.

**Smallest safe correction.** Preserve the frozen ten-case oracle and numerator; do not retrofit it after scoring. Inspect the candidate for a genuine sequential loop over every field and comma token, with case-sensitive membership in all eight tokens, whitespace stripping, unknown/empty skipping and last-recognized selection. Require separate honest evidence for invalid data=1, usage=64, selftest isolation/exit assertions and retained-pair effective values. A real loop is both simpler and more maintainable than the synthetic canned control. Do not edit or silently upgrade the experimental general classifier. No claim that equal decoded tokens establish arbitrary policy equivalence or publishing permission.

## Separability, no-harm and source grounding

C1's predicate reads SKILL.md only; C2's predicate executes only `scripts/referrer_policy_effective.py`. Baseline extraction materializes those two surfaces. C1 shortcut succeeds without a decoder, and C2 shortcut succeeds without a registry: observed causal separability, not merely prose. Both unchanged controls are red, so neither target is already satisfied by doing nothing. Prose and constant controls are also red, but the stronger passing shortcuts bound what those controls establish.

No candidate after-state was inspected or executed by this seat. Therefore no-harm is **not proven** by these baseline/shortcut controls. Preserve the historical classifier, warnings at `corpus/knowledge/policy-value-classes.md:89–95`, frozen r84 receipts and existing registry rows/callers. No source census or general regression check was assigned to this seat or run here. These are limits, not invented green checks.

Local source grounding inspected: `.ufo/waves/round-85/sources/referrer-policy-prefreeze.html:1596–1614`, §8.1 of https://w3c.github.io/webappsec-referrer-policy/#parse-referrer-policy-from-header . Located quote (23 whitespace-delimited words): “For each token in policy-tokens, if token is a referrer policy and token is not the empty string, then set policy to token.” The retained source receipt records GET, access date 2026-11-04, 246577 bytes and SHA-256 `339bdd20be241c9eca2f47a18d35368af460edfc708288d90c51e094393743a6`; it explicitly says status and exact fetchedAt were not captured. This seat did not refetch or independently hash that source, and does not claim it registered S458. Source-seat reopening/registration remains separate evidence. The algorithm supports sequential token selection, not general response-header reordering; RFC 9111 request Vary normalization must not substitute for that field-specific authority.

## Routed r84 defects: what remains open

Authoritative routing read at `corpus/lessons/round-84-verifier-spotcheck.md:93–106`, with detailed weaknesses at `.ufo/waves/round-84/w1/ReviewC1.md:7–30,75–80`.

| Defect | Round-85 scope and remaining debt |
|---|---|
| D84-1 | C1 targets the three missing registry rows. Baseline confirms 0/3, but row truth and persisted path bindings still need after-state inspection. Discoverability alone does not establish full gate conformance. No closure asserted here. |
| D84-2 | Remains open. No new row repairs v1's absent D3/D4 prose conjuncts, split-line D1 binding, non-string connector acceptance, permissive census exit/path tokens or rejection of empty-equal census sets. Preserve v1 and diagnostic v2 evidence without relabeling them universally sound. |
| D84-3 | Remains open as a general-equivalence debt. New decoder can address only Referrer-Policy last-token behavior. Keep the opposite-order witness and warnings. Canned-output weakness is concretely reproduced for the new counter; imported-table enforcement, prior repeated-run exit/newline weaknesses, other fields' order/duplicates and independent changed-row oracle remain outside this repair. |
| D84-4 | Remains open except possible procedural mitigations. The frozen r85 contract still holds planner at L1, maps planning data-walk to scout and acknowledges the outside literal dispatched-L2-planner disagreement. Sole L1 production integration avoids overlapping writers but does not by itself satisfy a separate-worktree requirement or adjudicate that disagreement. Binding-read evidence does not retroactively cure r84 load order. |

The r84 spotcheck already independently verified the actual older D1–D4 repairs while rejecting C2's semantic premise. Do not conflate those older repair states with closing the four new D84 routes. No full D84-queue closure, promotion, universal semantics or independent admission is claimed.

## Limits and handoff

No final candidate was available to this assigned review; findings target the frozen claims/counter and retained local evidence. Passing shortcuts are counterexamples to stronger interpretations, not a judgment on unseen candidate bytes. Canonical judgment remains outside this seat. L1's smallest safe next action is truthful row/path binding and actual decoder/source/retained-trial evidence, while retaining the frozen numerator and disclosed limitations. Assimilation: none. Tool installs/updates: none. No prohibited external actions occurred. Receipts and substantive fixtures were copied before removal of the exact scratch root; cleanup receipt is retained beside these findings.

Self-evaluation: accuracy 4 (executed receipts separated from static findings; no candidate verification), completeness 4 (assigned baselines, shortcuts, controls and all four routes covered; unseen after-state explicitly excluded), clarity 4 (findings distinguish numerator from conformance), actionability 4 (specific minimal corrections without changing frozen counters), conciseness 4 (detail retained for replay). Overall 4.0/5. Highest-impact improvement applied: one concrete one-token counterexample accompanies the passing canned shortcut. The user should find the evidence and limits explicit.

Report: .ufo/waves/round-85/w1/CriticClaims.md
