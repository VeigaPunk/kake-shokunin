# ReviewReceiptIdentity — round-46 residual attack (receipt identity for filed counts)

Wave `kake-r46-residual` · lane `/home/vgpnk/Projects/shokunin/kake-shokunin` (read-only) · tip `cd42e3c` · build `ee43e66` · base `7cdbaefd`.

**Criterion under test** (`corpus/QUALITY.md:1071`): *"Any filed count or verdict against a receipt cites that receipt's path + sha256; a receipt citation without sha256 violates this criterion."* Grounding (same line): round-45 Mistake 15 — the count must bind to **that receipt's identity (path + sha256)** and be re-derived from **the named receipt's committed bytes**, not another same-named receipt's values.

**Two admissible readings, both tested:**
- **A (filed side):** a count/verdict names the receipt path **and that receipt file's sha256**.
- **B (receipt side):** the receipt itself pins path + sha256 of the bytes it measures.

Round-46 passes **neither** in full: under A every one of the four verdict receipt citations fails; under B the C1 and S135 receipts pass, the C2 receipts fail outright. This is a **recommendation**, not an admission; the C2 verdict text stands as filed.

---

## HIGH-1 — No filed round-46 document cites any receipt's sha256; the verdict that declares the criterion cites receipts path-only

Evidence (all at HEAD `cd42e3c`, unchanged since `861113e`):

- `SCORECARD.md:3883-3884` (declaration): *"Receipts cite path + sha256 per the C2 criterion."*
- `SCORECARD.md:3906` (C1 verdict): *"receipts `verification/c1-before-7cdbaefd.json`, `verification/c1-after-ee43e66.json`; tool selftest 23/23"* — no digest.
- `SCORECARD.md:3907` (C2 verdict): *"receipts `verification/c2-before-7cdbaefd.json`, `verification/c2-after-ee43e66.json`"* — no digest.
- `LOG.md:1775-1776`: same two C1 receipt paths; `LOG.md:1780` cites the ledger path only.
- `corpus/lessons/round-46.md:31` still cites receipts as **placeholders** `verification/c1-after-<tip>.json`, `c2-after-<tip>.json`.
- Fleet round report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-46/kake.md:22-23,28-30` cites the same four receipts by path only (lines 22-23 name the two commits, not the receipt digests).
- `corpus/lessons/round-46-verifier-spotcheck.md` states *"receipt-identity criterion honored"* on the strength of the counter sha256 **inside** the receipt (`git show 861113e:…/c46_matrix.py | sha256sum = 7335b001…`). That is instrument pinning under pre-existing criterion (l), not receipt identity under the new criterion.

Exhaustive check (literal, not semantic — see gaps): a scan for `\b[0-9a-f]{64}\b` over `SCORECARD.md`, `LOG.md`, `corpus/lessons/round-46.md`, `corpus/lessons/round-46-verifier-spotcheck.md`, all `.ufo/waves/round-46/{w1,build,drafts,attack,verification}/*.md`, and the fleet report returns **zero round-46 receipt digests**. The only round-46 digests anywhere are inside the receipt JSONs themselves and in `w1/ReviewLessonQuality.md` (a round-45 counter digest). No `SHA256SUMS`/`.sha256` file exists for round 46 (`git ls-tree -r 861113e` has none under `.ufo/waves/round-46/`).

Additional identity hole at the filing commit: at `ee43e66` (where the verdict section was first committed — `git log -S 'Round 46 — measured verdicts'` → `ee43e66`), the two after-receipts **did not exist** and the rows cited `c1-after-<tip>.json` / `c2-after-<tip>.json` (`git show ee43e66:SCORECARD.md`, lines 3906-3907; `git ls-tree ee43e66:.ufo/waves/round-46/verification/` lists only c1-before, c2-before, c2-after-working). The real paths were substituted only at `861113e`, one commit later, and neither SCORECARD nor LOG names `861113e` (the fleet report does).

**Why it matters:** without a digest, the citation is satisfied by any file of that name; the criterion's stated failure mode — "another same-named receipt's values" — is exactly what the verdict's path-only citations permit (and the tree contains such a duplicate, see HIGH-2).

## HIGH-2 — The C2 receipts carry no sha256 at all and no tool identity; filed C2 counts are not re-derivable from the receipt bytes alone

- `verification/c2-before-7cdbaefd.json` and `verification/c2-after-ee43e66.json` have keys `{adjudicated, adjudications, population, revision, verdict, version, violations}` only. JSON-parsed: **no `sha256` substring anywhere, no `tool` object, no `measuredAt`.**
- `scripts/citation_lint.py` sha256 `3c78a0a82f70b166776f7f7626dc7afbf9f9916a4399ae879287e4bf9662987f` is never recorded. `corpus/quality/citation-adjudications.md` sha256 `432a36a2f9a6a20e6083ea223b63aa3c337e1fee4a9a938a08f8f61e57269394` is never recorded — yet the ledger **decides** clean vs violation (`citation_lint.py` suppresses only rows named in it). Population digests (`SCORECARD.md`, `LOG.md`) are also absent.
- This also violates pre-existing criterion (l) (`corpus/QUALITY.md:951-955`: post-measurement receipts pin `toolRevision`, `toolSha256`, `selftestSha256`), which `w1/ReviewLessonQuality.md:104-132` had already recorded red at base. Round 46 lands C2 receipts that repeat that red state.
- `verification/c2-after-working.json` is a **second, unbound after-receipt**: `revision: null`, verdict `clean`, 30 adjudicated, committed at the build commit `ee43e66` (sha256 `2a333f07…`). It is superseded by `c2-after-ee43e66.json` but remains in the tree, uncited and indistinguishable by content. Any later "c2-after" citation that drops the revision stem binds an unbound receipt — the precise hazard the criterion's grounding names.

## MEDIUM-3 — False counts filed against receipt paths without sha256

1. **"12 rows"** — `SCORECARD.md:3912` and `LOG.md:1780` and fleet report lines 13, 40: *"`corpus/quality/citation-adjudications.md` (12 rows…)"*. Committed bytes: `git show ee43e66:corpus/quality/citation-adjudications.md` (and HEAD) contain **20 data rows** — 8 `SCORECARD.md` + 12 `LOG.md`. The number 12 is the LOG subset, not the ledger. The receipt (`c2-after-ee43e66.json`) has **20 distinct `(token,file)` pairs / 30 occurrences**; ledger↔receipt pair sets match exactly (20 = 20), so 20 is independently the right count. No sha256 is filed for the ledger, so the count cannot be re-derived from the citation.
   Already routed by non-author closure as defect **R3**, but graded there as prose correction; it is still standing at HEAD and it is a count filed against a receipt with a path only.
2. **"23 base + 2 tip-only + duplicates at other lines"** — fleet report line 29. Re-derived from the receipts: **28** base-occurrence entries + **2** tip-only `e5455253` (SCORECARD:3867, LOG:1766) = 30; the duplicate at SCORECARD:1490 is already inside the base's 28. "23 base" is not derivable from either receipt. This decomposition is **not** covered by R1–R7.
3. True counts, for the record (re-derived from receipt bytes, not restated): before = 28 violations / 17 unique tokens / 15 SCORECARD + 13 LOG; after = 30 adjudicated occurrences over 29 distinct `(file,line,token)` (SCORECARD:1490 legitimately names `dcef39b5` twice) / 0 violations; C1 before = 0/11 caught (`tool_absent`); C1 after = 11/11 caught, 0 clean false positives, 0 controls accepted of 3, wall 1.154 s of a 120 s budget.

## MEDIUM-4 — Selftest tallies are filed with no receipt and no selftest digest

`SCORECARD.md:3906` and `LOG.md:1774,1777` and the fleet report file *"tool selftest 23/23"* and *"selftest 8/8; 4 mutant classes killed"*. Neither receipt carries a `selftestSha256` or any selftest block, no selftest receipt exists in `.ufo/waves/round-46/verification/`, and no digest is filed. Re-running the **committed** bytes reproduces both tallies exactly (my run: `redirect_audit --selftest` → `selftest: 23/23 passed` exit 0; `citation_lint --selftest` → `selftest: 8/8 passed` exit 0; 23 = 14 witnesses + 6 mutants + 3 CLI controls). The counts are true but unbound; this is routed defect **R2**.

## MEDIUM-5 — S135 source receipt is identity-valid, but its filing is asymmetric and the census count has no receipt

- `sources/receipts.json` (sha256 `29b2884641afc6ed305bbc47dff185897a7000d57bae42eee566881609c02434`) names `htmlSha256 0792591e…a819100c`, `textSha256 73b3b4a8…66ec18d`, `bytes 139250`, `httpStatus 200`, `finalUrl` = `url`. Verified against committed bytes: `S135.html` → `0792591e…` (size exactly 139,250), `S135.txt` → `73b3b4a8…`. **Valid under reading B.**
- But the SCORECARD capability row (`SCORECARD.md:3917`) cites `(S050, S135)` with no source-receipt path and no digest — a filed verdict on a source with no receipt identity. The lesson (`corpus/lessons/round-46.md:39-42`) and `corpus/SOURCES.md:143` are the round's best citations (text digest + retained path + receipt path) but still name the **artifact** digest, not the receipt file's own sha256.
- `LOG.md:1785-1787` files *"S135 … admitted … registry 134 → 135, census exit 0"* with no receipt, and **no round-46 census artifact exists** in the lane (`find .ufo/waves/round-46 -iname '*census*'` → none; rounds 37–45 all committed `census-before/after`). The census command appears only as prose in the fleet report.

## LOW-6 — Receipt paths are wave-relative shorthand and the commit-recording promise is half-kept

`SCORECARD.md:3899-3901` promises "build commit and verdict commit recorded in the round report and LOG". The fleet report records `ee43e66` and `861113e`; `LOG.md` names neither (closure defect **R5**). The verdict cites `verification/…` with no `.ufo/waves/round-46/` prefix and the section declares no base for it (root `verification/` does not exist), unlike round-44 precedent `SCORECARD.md:3761-3764` which cites the full wave path **with** the receipt's sha256.

## LOW-7 — `quality-broad-{base,tip}.txt` are bare 2-byte counts, cited path-only

`SCORECARD.md:3907` / `LOG.md:1784` cite the files; contents are exactly `32 0a` and `33 0a` (`2\n`, `3\n`). The values are true — `git show 7cdbaefd:corpus/QUALITY.md | grep -c '^- .*receipt.*\(path\|sha256\)'` = 2, HEAD = 3 — but the files carry no command, revision, or digest, so the falsification cannot be audited from the citation alone.

---

## Verified-identity positives (what does hold)

Byte-exact via `git show <rev>:<path> | sha256sum`; receipt structure via JSON parse:

| Object | Digest named in receipt | Committed bytes |
|---|---|---|
| `c46_matrix.py` (both C1 receipts) | `7335b001…b102164` | equal at `ee43e66` and HEAD |
| `scripts/redirect_audit.py` (c1-after) | `1e1dff18…4bb748a` | equal at `ee43e66` and HEAD; `present:false` at base is honest |
| controls (c1-after) | `d24af687…` constant, `4cc05b3c…` do-nothing, `48e3c3c2…` junk | all three equal the committed fixture blobs and `controls/placebo.py` |
| S135 retained bytes | `0792591e…` html, `73b3b4a8…` txt | equal; html size = 139,250 = receipt `bytes` |
| revisions | `7cdbaefd…` (before), `ee43e66…` (after) | both resolve; base holds no tool; `ee43e66` holds tool+counter+ledger |
| filed counts | 28/17, 30/0, 0/11, 11/11, 0 FP, 3/3 rejected, wall 1.154 < 120 | all re-derive true (except MEDIUM-3 items) |

Receipt file digests (not filed anywhere; supplied here so r47 can bind them):
`c1-before` `5f438e14ba72fa00e51cd6deb84cedf76a110b903a6b82ba2ea7f10df2d05b8c`, `c1-after` `8c8d9521b3ddc45f9719ddb13ffdb1468e6662c94c59b246d5dcf2b75a7c90c0`, `c2-before` `bdb88eca0a293eefd9c3343aeb9e5914b80eefb8b9840e9c53bee363bfe4b4f7`, `c2-after` `1d9a5a23f1ffa1ded728f3e6867e6964570251890b136a2906a5592873c085f9`, `sources/receipts.json` `29b28846…c02434`, ledger `432a36a2…e57269394`, `scripts/citation_lint.py` `3c78a0a8…bf9662987f`, `c2-after-working` `2a333f07…b58acef3e` (unbound).

One canonical runtime per stage holds (one receipt per stage/revision); the exception is the unbound `c2-after-working.json`, and the filed citations carry no digest to distinguish it.

## Residual risk

- The criterion's first enforcement is its own violation: r46 lands the rule and cites r46 receipts path-only. Unless r47 files an append-only erratum with the digests above (and corrects 12→20, 23→28), the lane's first entry under the new criterion is a non-compliant filing.
- Path-only citations plus a same-named duplicate receipt mean receipt substitution would be undetectable from the filed text; only commit history distinguishes them.
- C1 fixture manifests are bound only transitively through `revision` (no digest list in the receipt). Re-derivation at `ee43e66` is sound; a reader checking the current tree rather than the cited revision could be misled if fixtures ever change.
- External/sandbox adjudication classes were not re-verified here (separate seat).

## Verification gaps

- **No `lsp` device is mounted** (`read xd://lsp` → "No such tool: xd://lsp. Mounted devices: ast_edit, debug"), and no language server answers Markdown/JSON evidence files. No definition/reference/diagnostics claim is made; the 64-hex scan is an exhaustive **literal** scan over a declared file set, and is presented as completeness evidence for "no digest filed", not as semantic proof. Receipt structure was checked by JSON parsing; byte identity by git plumbing + sha256.
- I did not re-run the sealed matrix (owned by `CriticMatrixBlindness`); counts were re-derived from receipt bytes. I did run both committed selftests read-only — both use `tempfile` only; `HEAD` unchanged, and `git ls-files --others` shows no file of mine (siblings' residual reports and `.ufo/waves/round-47/verification/census-start.txt` only).
- Digest values for `c1-after`/`c2-after` are HEAD/`861113e` bytes; those files do not exist at `ee43e66`.

## Smallest remediation (append-only, round 47)

1. File an erratum in `LOG.md` (and the r47 report) carrying: the four receipt path+sha256, `sources/receipts.json` sha256, ledger sha256, `scripts/citation_lint.py` sha256, and the two corrections `12 rows → 20 rows` and `23 base → 28 base`.
2. Add `tool {path, sha256}`, `toolRevision`, `measuredAt`, and adjudications-ledger `path+sha256` to future `citation_lint.py` receipts (criterion (l) + this criterion, reading B).
3. Mark `verification/c2-after-working.json` superseded (or drop it in a later commit) so only revision-bound after-receipts remain.

Report: `.ufo/waves/round-46/residual/ReviewReceiptIdentity.md`
