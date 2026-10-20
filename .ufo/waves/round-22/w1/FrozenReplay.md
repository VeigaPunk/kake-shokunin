# FrozenReplay — round 22 w1 (scout)

Report: `.ufo/waves/round-22/w1/FrozenReplay.md` (relative to `/home/vgpnk/Projects/shokunin/kake-shokunin`).
Lane: `kake-shokunin`. Base: `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Status: read-only design. The only lane write is this report; scratch probes lived and died under `/tmp`. No new-gate execution (the gate does not exist at base), no tests, no live properties, no installs, no lane git/jj writes.

At read time `.ufo/waves/round-22/w1/` contained only `swarm-registry.json`; no Implement/Matrix/Measure artifact was present. This design is therefore against the frozen contract and the r20/r21 evidence patterns, **not** against landed code. Nothing below asserts that the r22 gate passes anything.

## Axes (godspeed)

- **A1 frozen identity** — does the transcript bind the exact bytes that produced the number?
- **A2 replay determinism** — same bytes in, same bytes out, twice, with no hidden state.
- **A3 falsifiability** — can the proof fail? An oracle that cannot fail is not a proof.
- **A4 claim honesty** — selftest mechanics are not domain proof; matrix classification is not external truth.
- **A5 surface economy** — one immutable store, one counter, no duplicated manifests or materializers.

Moves kept: revision + blob-OID + SHA-256 pinning; two-run byte identity; independent digest recomputation; explicit baseline-absence semantics; separate selftest and matrix artifacts; mutation controls that prove the oracle can go red.

Moves rejected: copying fixtures into a second `frozen/` tree (duplicate store, second drift surface); normalizing stdout before comparison (hides nondeterminism); re-implementing `measure.py` inside a replay wrapper (two implementations to trust); storing tool stdout as the expected result (golden-output laundering).

## Evidence classes

- **O — observed here or in committed artifacts.** Contract text; r20/r21 replay and measure files; SKILL registry rows; scratch probes of git/Python (commands and results named where used); environment `Python 3.14.8`, `git 2.56.0`, lane clone ≈11 MB.
- **I — inference.** Exit/id assignments for borderline cases; expected before/after totals; independence analysis. Marked inline.
- **U — unresolved.** Section 8.

## 1. What can be frozen here

`measure.py --revision <hash>` already makes the git object database the immutable store. A materialized `frozen/` copy is therefore redundant: it would need its own pins and could itself drift. The r22 design should freeze by **revision + path + blob identity** and record SHA-256 as an independent, human-readable attestation.

| Input class | Authoritative identity | Materialization | Pinned as |
|---|---|---|---|
| Validator under test `scripts/canonical_audit.py` | `git ls-tree -r R` mode+OID | `git cat-file blob <oid>` → temp tree | mode, OID, SHA-256, bytes |
| Matrix instrument `.ufo/waves/round-22/matrix.py` | same | same | same |
| Expectations `.ufo/waves/round-22/cases.json` | same | same | same |
| Fixtures `.ufo/waves/round-22/fixtures/**` | same | same | same |
| Counter `.ufo/waves/round-22/measure.py` (runner) | same | run from the clone | same, separately labelled `runner` |
| Contract `.ufo/waves/round-22/contract.json` | same | not executed | same, labelled `pins.contract` |
| Interpreter | `sys.implementation` + `sys.version` | not a blob | recorded string; determinism scoped to it |

No network, no external anchor: the revision is the anchor. A digest recorded by the run is **not** external attestation; its authority comes from the reviewed commit plus an independent recomputation (F10).

Only `100644` and `100755` are admissible modes. `120000` (symlink) and `160000` (gitlink) are hard-fail `snapshot_unsupported` in the replay — see F1 for the observed reason.

The input set is an **explicit allowlist**, never a directory sweep: `scripts/canonical_audit.py`, `.ufo/waves/round-22/{measure.py,matrix.py,cases.json,contract.json}`, and `.ufo/waves/round-22/fixtures/**` (the set declared by `cases.json`). Wave bookkeeping — `w1-dispatch.json`, `w1-spec.json`, `w1-deaths.json`, `census-before.txt`, `w1/**` seat reports — is evidence, not gate input. Including it would make `inputs_digest` change whenever a seat writes a report and would make the two runs disagree for reasons unrelated to the gate.

Reachability: the freeze holds while `$R` remains reachable in the clone. Cite the full 40-hex hash, never a branch name alone; a shallow/partial clone that cannot resolve `$R` is a `could-not-evaluate` (exit 2 of the replay), not an empty or zero-accepted result.

## 2. Digest manifest

Per input, one record:

```json
{"path": "scripts/canonical_audit.py", "mode": "100644", "oid": "<40-hex>", "sha256": "<64-hex>", "bytes": 12345}
```

Worked example, recomputed here from the r21 measured commit `df6196b022a7fe9ac9a88af1293dc377a8197652` (and matching the committed `gate-digest.json`):

```json
{"path": "scripts/corpus-contract.mjs", "mode": "100755", "oid": "31b2f11a8b84d553af05fffd7b613541d851e2b0", "sha256": "ca6f685e0b826a40894990b4f536d272ba3e948444e7ab74fb41602bbdf0ed29", "bytes": 29355}
```

Paths are repo-relative, `/`-separated, no `..`, no leading `/`, no NUL. Records are sorted by `path`. The aggregate is a convenience root over exactly the listed set, never a claim about the whole tree:

```python
def inputs_digest(records):
    blob = json.dumps(records, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(blob).hexdigest()
```

`records` is the sorted list of the five-field objects above. The document says which set it covers; a Git tree OID is **not** substituted, because the input set is a subset of the tree.

Placement: `replay.json` at `.ufo/waves/round-22/replay.json` carries the records, the revision, the interpreter, the runs, the baseline, the controls and the no-write result. This matches the registry's stated frozen-input location (`.ufo/waves/round-22`) without adding a `frozen/` subtree.

## 3. Replay procedure

Precondition: L1 has committed target, instrument and expectations; `git status --porcelain` is empty at `$R`. Measurement at an uncommitted worktree is invalid (F2).

**P0 — resolve and assert the revision.**
```text
R=$(git -C "$CLONE" rev-parse --verify "$TIP^{commit}")
test -z "$(git -C "$CLONE" status --porcelain)"
sha256sum "$CLONE/.ufo/waves/round-22/measure.py"
git -C "$CLONE" cat-file blob "$R:.ufo/waves/round-22/measure.py" | sha256sum   # must match
```
The runner's bytes must equal the revision's bytes; otherwise label the run as `runner_override` and do not call it revision-bound.

**P1 — enumerate the input set and gate modes.**
```text
git -C "$CLONE" ls-tree -r -l "$R" -- \
  scripts/canonical_audit.py \
  .ufo/waves/round-22/measure.py \
  .ufo/waves/round-22/matrix.py \
  .ufo/waves/round-22/cases.json \
  .ufo/waves/round-22/contract.json \
  '.ufo/waves/round-22/fixtures'
```
Expect exactly these paths — not every file under `.ufo/waves/round-22/` (`w1/**` and the wave bookkeeping are evidence, not inputs). Modes outside `{100644,100755}` → `snapshot_unsupported` (exit 2), before execution.

**P2 — independent digest recomputation.**
For every record: `git -C "$CLONE" cat-file blob "$oid" | sha256sum` must equal `sha256`, and `ls-tree -l` size must equal `bytes`. This recomputation is independent of `measure.py`'s own pin list, so the counter cannot certify itself.

**P3 — after run, twice, byte-identical.**
```text
python3 -B .ufo/waves/round-22/measure.py --root "$CLONE" --revision "$R" > run1.json 2> run1.err
python3 -B .ufo/waves/round-22/measure.py --root "$CLONE" --revision "$R" > run2.json 2> run2.err
```
Assert equal exit, byte-identical stdout, byte-identical stderr. No normalization in the checker. If output embeds a `mkdtemp` path or a timestamp, that is a `measure.py` defect to fix, not to mask (F3).

**P4 — per-case assertions.**
- exit 0; `available == true`; `total == 32`; `accepted == 32`.
- `results` names are exactly `contract.matrixCases` as sets, no duplicates, no extras.
- For every case: observed exit equals the case's declared exit; observed finding ids equal the declared ids as sets; clean cases have `ids == []` and zero findings.
- Every contract `findingIds` member appears at least once among expected ids; otherwise record the uncovered ids as declared limits (this is the cheap check that the 32-name population still spans the policy).
- JSON has the contract's required keys (`verdict`, `pagesChecked`, `findings[].id`, `findings[].page`) per page.

**P5 — before run, instrument held fixed.**
```text
python3 -B .ufo/waves/round-22/measure.py --root "$CLONE" --revision 7c61c8cc791bde36dd5e3688bdfea2678d90146c --cases-root "$CLONE"
```
Assert exit 0, `available == false`, `accepted == 0`, `total == 32`. This is the controlled comparison: target absent, instrument present. Record the instrument records from `$CLONE` and label them `cases_root: candidate`. This is not "the baseline instrument measured 0" — no baseline instrument exists (U4). `cases_root` must not appear in the after run.

**P6 — selftest, separate artifact.**
```text
python3 -B scripts/canonical_audit.py --selftest
```
Assert exit 0 and a complete case table. Write `selftest.json`. The `n/n` here is a mechanics count, never the 32-case denominator (section 5).

**P7 — no-write and no-mutation.**
- Static: the tool imports no `socket`, `urllib.request`, `http.client`, `requests`, or `subprocess`; `urllib.parse` is allowed. This is a source-level claim, not a sandbox.
- Empirical: materialize the instrument into a scratch tree, `chmod -R a-w`, run a clean case with `--manifest` inside that tree and `cwd` an empty read-only directory. Exit must match the case's declared exit. Compare the tree's path list and `inputs_digest` before and after; both identical. Precondition: not root.
- Assert the lane worktree is unchanged (content hash of the input paths) and `$R` still resolves.

**P8 — falsification controls (scratch copies only, never counted).**
1. **Expectation mutation:** copy a materialization, change one case's declared exit or id; matrix must exit 1 and name that case. Proves the oracle compares against `cases.json`, not against tool output.
2. **Fixture mutation:** change the canonical host in the `absolute_match` fixture; matrix must exit 1 with `canonical_mismatch`. Proves the fixture is parsed and causally connected.
3. **Missing tool:** remove `scripts/canonical_audit.py`; matrix must exit 2 (tool missing); measure at baseline must report `available:false`, `accepted:0`, `total:32`.
4. **Missing fixture:** delete one fixture; matrix must exit 2, never a fabricated pass.

A replay without controls proves only that a program printed 32; controls 1–2 are what make it an oracle.

**P9 — transcript and postconditions.**
Write `replay.json` (section 4) plus `measure-before.json`, `measure-after.json`, `selftest.json` verbatim. Remove scratch trees. Re-check `git status --porcelain` and `$R`.

## 4. Transcript shape (proposed; field names may change, but revision/OIDs/SHA-256, run exits and byte hashes, before/after totals, and controls are required information)

```json
{
  "schema": "kake-r22-canonical-preflight-replay-v1",
  "revision": "<40-hex>",
  "revision_input": "<master-tip or ref>",
  "runner": {"path": ".ufo/waves/round-22/measure.py", "mode": "100644", "oid": "...", "sha256": "...", "bytes": 0},
  "pins": {"contract": {"path": ".ufo/waves/round-22/contract.json", "mode": "100644", "oid": "...", "sha256": "...", "bytes": 0}},
  "interpreter": {"impl": "CPython", "version": "3.14.8", "platform": "linux"},
  "inputs": [{"path": "scripts/canonical_audit.py", "mode": "100644", "oid": "...", "sha256": "...", "bytes": 0}],
  "inputs_digest": "<64-hex>",
  "runs": [
    {"argv": ["python3", "-B", ".ufo/waves/round-22/measure.py", "--root", "<clone>", "--revision", "<R>"], "exit": 0, "stdout_sha256": "...", "stderr_sha256": "..."},
    {"argv": ["...same..."], "exit": 0, "stdout_sha256": "...", "stderr_sha256": "..."}
  ],
  "stable": true,
  "after":  {"available": true,  "accepted": 32, "total": 32, "exit": 0},
  "before": {"revision": "7c61c8cc791bde36dd5e3688bdfea2678d90146c", "cases_root": "<clone>", "available": false, "accepted": 0, "total": 32, "exit": 0},
  "selftest": {"path": ".ufo/waves/round-22/selftest.json", "sha256": "...", "exit": 0},
  "controls": [
    {"name": "expectation_mutation", "observed_exit": 1, "observed_case": "absolute_match"},
    {"name": "fixture_mutation", "observed_exit": 1, "observed_ids": ["canonical_mismatch"]},
    {"name": "missing_tool", "observed": {"available": false, "accepted": 0, "total": 32, "exit": 0}},
    {"name": "missing_fixture", "observed_exit": 2}
  ],
  "no_write": {"case": "absolute_match", "tree_digest_before": "...", "tree_digest_after": "...", "read_only_tree_exit": 0},
  "tree_unchanged": true
}
```

`measure-before.json`, `measure-after.json`, `selftest.json` are the verbatim stdout artifacts; `replay.json` pins them by SHA-256 instead of duplicating their rows. This mirrors the r21 set (`measure-before/after`, `corpus-selftest`, `replay`) and avoids a second `gate-digest.json` that would only repeat `runner`.

## 5. Selftest is not domain proof

These are three different instruments answering three different questions.

| | `canonical_audit.py --selftest` | Frozen matrix (`measure.py` at `$R`) | External/domain truth |
|---|---|---|---|
| Inputs | synthetic strings/temp trees built by the tool itself | committed fixtures + manifest at `$R` | live pages, headers, redirects, JS, index state |
| Expectations authored by | the implementer, in the same file | the Matrix seat from the contract + docs, independent of the implementation | nobody in this round |
| Proves | CLI map 0/1/2/64; parser/URL mechanics; head/template/decoy handling; no network/write code paths; regressions | the tool classifies all 32 declared shapes with the pinned exit and id; clean positives stay clean | nothing |
| Cannot prove | policy coverage; that the matrix exists; external semantics | standards correctness; Google selection; real-site behavior; freshness | — |
| Failure means | implementation bug or selftest expectation bug | policy/implementation disagreement | — |
| Artifact | `selftest.json` | `measure-before/after.json` + `replay.json` | not produced |
| Count | `n/n` mechanics cases | `accepted/32` matrix cases | — |

**Non-substitution rules for the L1 report.**

1. A green selftest is necessary but not sufficient for C1's "classifies every frozen matrix case". The 32/32 claim cites the matrix, never the selftest.
2. A green matrix is not evidence that the selftest mechanics work; both artifacts are reported separately.
3. Exit 64 is reachable only through CLI misuse; no matrix case can prove it. It lives in the selftest.
4. Exit 2 appears in both, but for different reasons: the selftest can prove unreadable input and usage; the matrix proves only the cases whose pinned exit is 2.
5. Neither artifact proves Google selection, JS rendering, HTTP headers, redirects, network freshness or publishing readiness; the contract's limits stay attached to every citation.
6. Never store tool stdout as `cases.json`. Expectations are literals authored from the contract; a post-red edit is a new instrument version and requires a re-measurement (F9).

**Claim ledger for C1.**

| C1 clause | Artifact that can support it |
|---|---|
| "read-only local validator" | P7 (read-only tree, unchanged digests, static import scan) |
| "classifies every frozen matrix case with expected exit and finding id" | P3–P4 (`measure-after.json`, per-case rows), `replay.json` digests |
| "rejects missing/conflicting/mismatching canonical signals" | negative case ids in the matrix, controls 1–2 |
| "proves clean positive controls" (plural) | ≥2 structurally distinct exit-0 shapes, each with zero findings |
| "0 accepted before" | P5 (`measure-before.json`, `available:false`, `0/32`) |
| "deterministic replay" | P3 byte identity + P2 independent digest recomputation |
| "no Google selection / JS / freshness" | docs + absent imports; a **negative** claim, not an executed proof |

## 6. Freeze hazards specific to this gate

**F1 — Symlink mode laundering (medium; observed).** A committed symlink is mode `120000`; `git cat-file blob` returns the *link target text*, not the target file's bytes (probe: `link.html -> target.html` produced the 12-byte blob `target.html`; the absolute link produced 14 bytes). A materializer that writes blob bytes to a regular file silently turns the fixture into text. Smallest check: P1 mode gate; any `120000`/`160000` → `snapshot_unsupported`. The `symlink_html` fixture is built at matrix runtime (per the Matrix seat's assignment), so it must not be committed; its generator is covered by `matrix.py`'s digest.

**F2 — Revision/worktree drift (medium).** Running `measure.py` from a dirty clone at an older `$R` measures a different tool than the one being reviewed, and `--revision` will not complain. Smallest check: P0 `status --porcelain` empty plus runner digest equality. If the clone is dirty, stop; do not "just measure the tip".

**F3 — Nondeterministic stdout (medium).** A temp path, timestamp, set iteration or hash-order difference makes two runs differ; normalizing it away hides real instability. Smallest check: byte-identical stdout/stderr across two runs (P3), with a `measure.py` requirement to emit only stable relative identifiers. This is a design constraint on the Measure seat.

**F4 — Instrument drift through `--cases-root` (medium).** The baseline run deliberately holds the instrument fixed at the candidate root. If `cases_root` leaks into the after run, or its digest is not recorded, the before/after comparison is unauditable. Smallest check: `cases_root` appears only in the `before` block; its `inputs_digest` is recorded; the after run materializes everything from `$R`.

**F5 — Count-only oracle (high).** `accepted == 32` alone is compatible with swapped ids, duplicate names, or a matrix that silently lost a case and gained another. Smallest check: exact 32-name set equality against `contract.matrixCases`, per-case exit+id equality, clean-case emptiness, and `findingIds` coverage (P4). Reject aggregate-only reporting.

**F6 — Contradictory or duplicate expectations (medium).** Two cases with the same `(url, fixture bytes, expectedCanonical)` but different expected exit/id are contradictory. Two cases with identical input *and* identical expectation are redundant tests, not contradictions; report them as redundancy. Smallest check: compute a case-input digest and group; contradictions are a freeze failure, duplicates are a warning.

**F7 — Non-discriminating decoys (high for the three decoy cases).** If `comment_decoy`, `script_decoy` or `template_decoy` contain *only* the decoy link and expect `canonical_missing`, they are indistinguishable from `missing_link`: a tool that ignores the whole head passes. To discriminate over-absorption, the fixture needs a real canonical beside the decoy (clean expectation, or `canonical_mismatch` when the decoy points elsewhere). The Matrix author must choose the shape; the replay should record it, and the report may not claim "decoy handling" from a decoy-only fixture. Related observed parser facts: `HTMLParser` lowercases tag and attribute names, unescapes `&amp;` in attribute values, parses `<link>` inside `<template>` as an ordinary start tag, and does **not** parse script bodies into tags — so template/script handling is the tool's state machine, not the parser's.

**F8 — Vacuous path negatives (medium).** `manifest_traversal` and `symlink_html` must resolve to an existing target that the tool is expected to refuse; if the target is absent, the rejection is attributable to ENOENT, not to traversal/symlink policy, and a tool that never checks still exits 2. Smallest check: the fixture set contains the outside target and the link target exists; the expected id is `input_invalid`, and the control proves the same input shape is accepted when regular and inside the root.

**F9 — Expectation laundering (high).** Two forms: (a) generating `cases.json` from a first tool run, (b) editing an expectation after a red matrix so the rerun goes green. Both make the matrix a mirror. Smallest checks: expectations are literals with no reference to tool output; `git log -p` after integration shows either no expectation edits or an edit accompanied by a new `inputs_digest` and a fresh measurement. The wave dispatch file is the independence evidence (Implement and Matrix ran in parallel); git authorship cannot prove it, because all lane commits use the lane identity.

**F10 — Digest-authority overclaim (medium).** A `replay.json` digest is self-recorded. It becomes reviewable only when committed at `$R` and recomputed independently from `git cat-file`. Do not call it cryptographic attestation, and do not imply it covers the whole tree: it covers exactly the listed records. Smallest check: P2 recomputation, plus citing the full `$R` and per-path OIDs in the report.

**F11 — Interpreter and normalization unpinned (medium).** `urlsplit`/`urljoin` are RFC 3986, not WHATWG; the observed probes show: `urljoin(base, "")` self-resolves; host case and `:443` survive `urljoin`; `urlsplit("https:///a")` accepts an empty netloc with `hostname is None`; `.port` raises `ValueError` on `:abc` and `:99999`; `.netloc` retains case while `.hostname` lowercases. `HTMLParser` never implies `</head>`. The contract says "WHATWG-like", so the subset actually implemented must be documented and pinned in the selftest, and `replay.json` must record the Python version. Smallest check: a normalization table in the tool's header and at least one selftest case per normalization rule; record `sys.version`. Two consequences matter to the freeze: `urljoin(base, "")` returns the document URL, so an empty `href` must be classified before resolution (the `href_empty` case pins this; without that pin the outcome drifts to clean or `canonical_mismatch`), and `urlsplit` keeps userinfo in `netloc` while `hostname` drops it, so a hostname-only comparison silently accepts `https://user:pw@host/...` — credential rejection must inspect `.username`/`.password`.

**F12 — No-write proof weaker than the claim (medium).** Content hashing before/after misses transient files, metadata-only writes and writes outside the input tree. Smallest check: read-only tree + read-only cwd run (P7) in addition to hashing, plus the static import scan. State the residual: the proof covers this user and this tree; it is not a sandbox against arbitrary code.

**F13 — Population gap that replay cannot detect (limit, not a defect).** The 32-name matrix has no case for a document with `<head>` but no `</head>` followed by a body link (the `HTMLParser` probe shows the parser will not close head implicitly), no non-UTF-8/BOM fixture, no base-after-link ordering case, and no multi-page manifest/exit-precedence case. If these shapes are not in `cases.json`, the report must state them as unexercised limits rather than imply the parser is fully covered. A future falsifier can add one shape at a time, with a new instrument digest.

**F14 — Exit-map guess frozen as fact (medium).** The contract gives the exit map but not a case-by-case mapping. Borderline shapes — `missing_head` (no head at all), `base_url_invalid`, `invalid_url`, and the decoys — can plausibly be policy failures (exit 1) or could-not-evaluate (exit 2). `[INFERENCE]` the likely pins are: `missing_head → html_unsupported/2`; `base_url_invalid → base_url_invalid/1`; `invalid_url → canonical_url_invalid/1`; `manifest_traversal`/`symlink_html → input_invalid/2`. The Matrix author owns the final pin; the replay can reproduce it but cannot adjudicate it. The report must not present a guess as a contract fact.

**F15 — A policy clause with no matrix case: credentials (medium).** The contract's policy says "reject fragments and credentials", and `fragment_url` covers the fragment half, but no one of the 32 case names is a credential-bearing canonical. A URL such as `https://user:pw@example.test/a.html` with the correct host, path and query would be classified clean by a `.hostname`-only comparison, so the matrix can be 32/32 with this clause unexercised. Do **not** add a 33rd case silently (that changes the frozen denominator). Put one credentials case in the tool selftest, and state in the knowledge entry and the L1 report that the 32-name matrix does not cover credential rejection. Same treatment for the "no automatic fetching" clause: it is a code-absence claim, not a matrix case.

## 7. Minimal evidence set and L1 recipe

Evidence files (all under `.ufo/waves/round-22/`): `measure-before.json`, `measure-after.json`, `selftest.json`, `replay.json`. Frozen inputs are the revision-addressed files listed in section 1; no `frozen/` copy.

Checks L1 should run once after integration (I did not run any of these; the tool does not exist at base):

```text
git status --porcelain                                   # empty at $R
python3 .ufo/waves/round-22/measure.py --root . --revision "$R"   # twice; compare bytes
python3 .ufo/waves/round-22/measure.py --root . --revision 7c61c8cc791bde36dd5e3688bdfea2678d90146c --cases-root .
python3 scripts/canonical_audit.py --selftest
git -C . cat-file blob "$R:scripts/canonical_audit.py" | sha256sum   # vs transcript
grep -nE '^[[:space:]]*(import|from)[[:space:]]+(socket|urllib\.request|http\.client|requests|subprocess)' scripts/canonical_audit.py
```

Acceptance: after run `available:true, accepted:32, total:32, exit:0`; before run `available:false, accepted:0, total:32, exit:0`; selftest exit 0; two-run stdout byte-identical; every transcript record reproduces from `git cat-file`; all four controls observed; read-only tree run unchanged.

## 8. Limits and unresolved

- **U1** `cases.json` and `measure.py` output schemas are not in the contract. Section 4 proposes fields; only per-case name/exit/id and digest coverage are hard requirements.
- **U2** Exit/id pins for `missing_head`, `base_url_invalid`, `invalid_url` and the decoy shape are unresolved (F14); Matrix owns them.
- **U3** The decoy fixtures' discriminating shape (real canonical beside the decoy, or decoy-only) is unresolved (F7). A decoy-only fixture can still be shipped, but the claim must be reduced to "decoy not promoted", not "decoy handling proven".
- **U4** The baseline has no instrument. The before run necessarily uses the candidate instrument via `--cases-root`; the transcript must say so. There is no baseline-instrument measurement to compare against, only baseline-target absence.
- **U5** Independence of expectations is author-side and evidenced by the dispatch/seat reports, not by git authorship (all lane commits share the lane identity).
- **U6** The tool's file-decoding choice (UTF-8 strict vs replacement) and its behavior on non-UTF-8 bytes are not specified; no fixture exercises it.
- **U7** `symlink_html`'s runtime target (inside the fixture tree vs outside) is not specified; either is admissible only if the target exists and the expectation is `input_invalid` (F8).
- **U8** Multi-page manifests and exit precedence (2 outranks 1) are not in the 32-case matrix; do not claim them.
- **U9** Credential rejection is a contract policy clause with no matrix case (F15); until a selftest case covers it, it is an unexercised clause, not a proven behavior.

## Mechanism demonstration (not a C1 result)

To show the digest/manifest design is executable today without touching the new gate:

- Recomputed all 36 input digests in `.ufo/waves/round-21/frozen/before/expected.json` from the committed snapshot: **0 mismatches**; manifest SHA-256 `85a166fa3c59a137c1eebe20d0b24f1e073d2b24c2b347f7c2b0d935a19bdb89`. This validates the record/digest mechanics on a real frozen input set.
- Scratch git probe (`/tmp`, removed): a committed `link.html -> target.html` yields mode `120000` and a 12-byte blob `target.html`; the absolute-link fixture yields 14 bytes. This is the empirical basis for F1.
- Scratch `HTMLParser`/`urllib.parse` probes yielded the observed facts cited in F7/F11.

None of these exercised `scripts/canonical_audit.py`, `matrix.py`, `cases.json`, or `measure.py`; they are mechanism evidence only.

## Tooling

No installs or updates; no package transactions, services, credentials or live properties. Scratch work stayed under `/tmp`.

---
Base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`. Report `.ufo/waves/round-22/w1/FrozenReplay.md`. Read-only scout; no other lane writes.
