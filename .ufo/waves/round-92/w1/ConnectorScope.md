VERDICT: C2 frontier on RFC 9111 §4.2.2 has 0 sibling overlap; new SOURCES.md row is non-duplicate under CORPUS rule 2; sandbox allowlist mandates standalone stdlib implementation.

# ConnectorScope — Sibling Overlap, Registry Duplication & Adjacency Scan (Round 92)

**Author:** ConnectorScope (kake round 92, wave 1)  
**Lane Root:** `/home/vgpnk/Projects/shokunin/kake-shokunin`  
**Base / Freeze Revision:** `a5640ca02c20f94a0fa03af41b977b46ae99808e`  
**Date:** 2026-11-04  

---

## 1. Findings & Evidence

### 1.1 Sibling-Overlap Scan (Read-Only)
Across all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin/`, searches across `corpus/SOURCES.md` and `corpus/knowledge/` yielded:

1. **`heuristic freshness`**: 0 hits (exit 1). Receipt: `.ufo/waves/round-92/w1/ConnectorScope/receipts/query-heuristic-freshness.txt`.
   - Extended check: `heuristic-freshness` produced 1 hit in `tabi-shokunin/corpus/knowledge/async-step-evidence.md:264`, where tabi observed stylesheet revalidation counts during browser automation and noted: *"the mtime/heuristic-freshness candidate is correlational only"*.
2. **`RFC 9111 §4.2.2`**: 0 hits (exit 1). Receipt: `.ufo/waves/round-92/w1/ConnectorScope/receipts/query-rfc9111-sec422.txt`.
   - General RFC 9111 search produced 16 hits across 4 siblings (`chousa`, `kumitate`, `mori`, `tabi`). None implement or cite §4.2.2.
   - `chousa-shokunin` S025 (`corpus/SOURCES.md:35`) evaluated §4.2 (Freshness) and **REJECTED** it as authority for research-record metadata or validity.
   - `kumitate-shokunin` S237 (`corpus/SOURCES.md:191`) uses §5.1 / §4.2.3 for shape-receipt age on the compare path.
   - `mori-shokunin` S594 (`corpus/SOURCES.md:375`) uses §4.1 for Vary-selected representation variations across User-Agents.
   - `tabi-shokunin` S123 (`corpus/SOURCES.md:137`) cites RFC 9111 only in the reference list of RFC 9309 (Robots Exclusion Protocol).
3. **`Last-Modified`**: 48 hits across 9 lanes (exit 0). Receipt: `.ufo/waves/round-92/w1/ConnectorScope/receipts/query-last-modified.txt`.
   - 45 hits record passive HTTP header metadata for documentation, datasets, and image snapshots (`kaidoku`, `kasegi`, `kotoba`, `kotodama`, `kumitate`, `mori`, `tabi`, `tameshi`, `tsukuroi`).
   - 3 hits examine protocol mechanisms: `tabi` (`network-evidence-rung.md:556` for IMS 304 in browser test passes) and `tsukuroi` (`SOURCES.md:105` and `pause-lift-gate-r24.md:47` for pacman `libalpm` setting database mtime from server's `Last-Modified`).
   - 0 sibling hits compute heuristic freshness lifetime from `Last-Modified`.
4. **`heuristic`**: 142 hits across 14 lanes (exit 0). Receipt: `.ufo/waves/round-92/w1/ConnectorScope/receipts/query-heuristic.txt`.
   - All hits reflect domain-specific heuristics (codec mapping in `audio`, text locators in `chousa`, disassembly in `kaidoku`/`revenger`, service listeners in `kama`, triage in `kasegi`, OOM killer in `tsukuroi`). None touch HTTP response caching lifetime.
5. **`stale-while-revalidate`**: 0 hits (exit 1). Receipt: `.ufo/waves/round-92/w1/ConnectorScope/receipts/query-stale-while-revalidate.txt`.
6. **`Expires`**: 11 hits across 2 lanes (exit 0). Receipt: `.ufo/waves/round-92/w1/ConnectorScope/receipts/query-expires.txt`.
   - 9 hits in `kasegi-shokunin` refer to the RFC 9116 `security.txt` mandatory `Expires` field (vulnerability disclosure clock).
   - 2 hits in `tabi-shokunin` refer to the IETF draft expiration date (`Expires 18 May 2024` for `draft-ietf-httpbis-rfc6265bis-13`).
   - 0 hits refer to the HTTP response caching header `Expires` (RFC 9111 §5.3 / §4.2.1).

### 1.2 Registry Scan in LANE (`corpus/SOURCES.md`)
`grep -rn "rfc9111" corpus/SOURCES.md` identifies 7 rows:
- **S456** (tier A, `rfc9111.txt`): Reading two dated captures of one URI; validators compared; Age as clock estimate. Anchors §3.1, §3.2, §4, §4.2 (lines 581-599), §4.2.3, §4.3.1, §4.3.4.
- **S457** (tier A, `rfc9111.html`): Cache-Control response directives value semantics. Anchors §4.2, §5.2, §5.2.2, §5.2.2.1, §5.2.3. (Superseded in part by S461).
- **S461** (tier A, `rfc9111.html`): First-match lifetime, duplicate directive handling, quoted arguments. Anchors §§1.2.2, 4.2.1, 5.2, 5.2.2.5, 5.2.2.10.
- **S462** (tier A, `rfc9111.html#age.calculations`): Calculating Age arithmetic on supplied timestamps. Anchors §4.2.3.
- **S463** (tier A, `rfc9111.html#caching.negotiated.responses`): Vary match profile. Anchors §4.1. (Superseded by S467).
- **S467** (tier A, `rfc9111.txt`): Cache key construction ingredients. Anchors §2, §4.1.
- **S469** (tier A, `rfc9111.txt`): Request directives constraining reuse, explicit freshness lifetime, serving stale. Anchors §5.2.1, §4.2.1, §4.2.4, §1.2.2.

**Duplicate Verdict under CORPUS.md Rule 2:**  
A new row for RFC 9111 §4.2.2 (lines 686–720) is **NOT a within-scope duplicate**.
- In round 91, a proposed second row for §4.2.3 was rejected because S462 already owned §4.2.3 on the exact same RFC.
- In round 92, **no existing row anchors or scopes §4.2.2**. S456 stops at line 599 (§4.2 overview: fresh/stale definitions), S461 and S469 anchor §4.2.1 (explicit lifetime), S462 anchors §4.2.3 (Age), and S467 anchors §4.1 (Vary).
- Citing S456 or S469 for §4.2.2 would be false attribution. Opening §4.2.2 as a new row (e.g. S470) satisfies `CORPUS.md` rules 1 and 2 by grounding previously unmined specification ground.

### 1.3 Adjacency & Prohibited Absorptions
- **`kake-shokunin`** owns publisher-side placement, cache-control policy, and freshness calculations/decisions over supplied integer timestamps and headers (RFC 9111 §4.2.2).
- **`chousa-shokunin`** owns research method. Kake must **NOT** absorb chousa's rejection of RFC 9111 §4.2 (S025), which was based on research-record validity.
- **`tabi-shokunin`** owns live browser automation and empirical client behavior. Kake must **NOT** absorb tabi's live browser journey findings (`async-step-evidence.md:264`) or treat browser implementation variance as normative specification rules. Kake's C2 instrument operates over pure integer models without browser or network side-effects.
- **`kumitate-shokunin`** owns artifact receipt age. Kake must **NOT** absorb kumitate's receipt-age metadata model (S237).
- **`mori-shokunin`** owns crawler representation selection. Kake must **NOT** absorb mori's crawler/UA-variance findings (S594).
- **`kasegi-shokunin`** owns security disclosure channels. Kake must **NOT** absorb kasegi's RFC 9116 `Expires` field (S063).

---

## 2. Non-Obvious Move (UFO-FSD Connector Synthesis)

### 2.1 Evidence of Contradiction
In round 91, routed defect **K91-9** (and R91-4 in `corpus/lessons/round-91.md`) stated:
> *"scripts/stored_reuse.py re-implements the Cache-Control directive grammar that scripts/cache_control_effective.py (r86) already reads — compose it."*

Furthermore, `swarm-registry.json` for `ExecHeuristic` suggests:
> *"Do not re-implement the Cache-Control directive grammar if scripts/cache_control_effective.py already provides it..."*

**However**, inspecting the frozen C2 counter `.ufo/waves/round-92/c92_heuristic.py` (lines 320–355) reveals an explicit execution-time audit-hook sandbox:
```python
def hook(event, args):
    if event == "import":
        name = args[0]
        if name.split(".")[0] not in allowed:
            raise PermissionError("sandbox: import denied: %s" % name)
```
Where `allowed` is a frozen set containing **only Python standard library modules** (`json`, `sys`, `re`, `collections`, etc.). `scripts` and `cache_control_effective` are **NOT** in `allowed`!

### 2.2 Second-Order Effect
If `ExecHeuristic` follows K91-9 and the suggestion in `swarm-registry.json` by attempting to import `cache_control_effective` (or any non-stdlib module in `scripts/`), `c92_heuristic.py`'s audit hook will immediately intercept the import and abort execution with:
`PermissionError: sandbox: import denied: cache_control_effective`
This would cause all 28 hand cases and all 120 generated cases to fail, falsifying C2 at the carrier.

### 2.3 Proposed Move
1. **Self-Contained Stdlib Implementation:** `scripts/heuristic_freshness.py` MUST be implemented as a standalone, standard-library-only script (`json`, `sys`, `re`), parsing Cache-Control directives directly per `c2-contract.md` clauses 1–4, without importing any external script or sibling tool.
2. **Defect Disposition in Report:** Name K91-9 as a **falsified refactoring recommendation**: under a strict audit-hook sandbox that isolates candidate subjects from repo imports, intra-repo module reuse cannot be achieved via un-whitelisted imports.
3. **Registry Grounding:** ScribeRegistry and ScribeEntry must register RFC 9111 §4.2.2 under a new, distinct row (`S470`), avoiding both duplicate row rejections and false-attribution links to S456 or S469.

### 2.4 Affected Axes
- **freshness (C2, score 10 HOLD):** Protected from immediate falsification by preventing import-sandbox rejections during counter execution.
- **operability (score 10 HOLD):** Maintains reproducible, self-contained CLI behavior with zero external dependencies and a clean `--selftest`.
- **calibration (C1, score 2):** Prevents cross-contamination between instrument suites.

### 2.5 Verification
Run `python3 -B .ufo/waves/round-92/c92_heuristic.py --root . --revision <REV> --work <scratch>` against the candidate. Under the audit hook, `candidate=present`, `anti_table=ok`, `hand=28/28`, and `generated=120/120` hold only when the subject avoids non-stdlib imports.
