# ReviewCounter — frozen-counter attack

Axes: reproducibility, conjunct soundness, RFC fidelity, claim/coverage honesty. Read-only author-side review; recommendation only, not independent closure. No production edits, VCS mutations, installs, dispatch, or background jobs.

## Findings, by severity

### High — R1 cannot bootstrap its own honest green receipt

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/count.py:72–84,115–130` requires both after receipts containing `met=true` inside the measured carrier before C1 can report true. With the C1 after receipt absent, the first measurement is necessarily red. Recording that honest red leaves the next carrier red. The counter does not establish that a receipt describes the measured revision, parse its exit, or prove measurement provenance. The assigned cheap hunt directly accepted non-measurement strings `not a measurement: met=false` / `not a measurement: met=true` as R1=true. Do not manufacture a green seed. Keep C1 unproven unless the canonical owner resolves this dependency; frozen bytes were not changed here.

### High — pinned-base C1 replay drifts with live fleet state

The base replay returned exit 1 but `closed=1 open=3`, not frozen `closed=0 open=4`. Only R2 changed: `l0_absent` became `ok=true l0_line`. C1 reads the current fleet in `count.py:87–91,120,426`, outside either pinned export. The current actual routing exists at `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:294`; it substantively names D84-4 and the policy conflict, but its existence also retroactively changes the base result. C2 replay is byte-identical, exit 1, `cases=0/15`.

The frozen receipt files record output and exit, not original argv or fleet snapshot. Replay used their exact revision labels, explicit lane root, C1 freeze=base, default live fleet, and seat-owned `--work`. Thus original undisclosed flags cannot be certified identical; this is an additional reproducibility gap, not a reason to hide observed drift. Full commands, stdout, exits and hashes are in the receipt directory.

### Medium — R2 and R4 accept unrelated wording

`count.py:41,87–91`: `kake | round-86 | lunch menu, no policy routing` passes R2. The conjunct does not require D84-4, the policy conflict, operator ownership, or a question. This is a real shortcut even though the live actual row is relevant.

`count.py:104–112`: a row naming both debts and the lesson but no `flip:` anywhere correctly fails. However, `D84-2 D84-3 CLOSED; corpus/lessons/round-85.md` plus a separate `Unrelated example flip: pancakes` passes. Tokens need not occur in one row, debts need not remain open, and the flip need not be a re-open condition. This can directly contradict retained-open D84-2/3 while scoring closed R4.

### Medium — 15 green cases cannot establish a general reader or offline execution

`count.py:268–279,315–318` explicitly supplies a canned exact-input lookup as the green C2 fixture; `selftest()` passing includes that fixture (`391–398`). Thus a lookup of the 15 frozen input/output pairs plus an exit-0 `--selftest` passes this bounded target without parsing other Cache-Control values. This limit is stronger than merely noting constant/min/shared shortcuts fail.

`count.py:203,243–244` calls the absence of a narrow beginning-of-line import regex `tool_offline=1`. Dynamic imports, `import os, socket`, subprocess networking, imported helpers, or alias/import indirection evade it. No network sandbox is applied by `206–245`. This is a static spelling screen, not an offline-by-construction proof. These are source-established bypasses, not network probes performed here.

### Low — frozen-contract inconsistency and CLI caveat

The contract at `efc2ad654f1ee56a86ecb57b3b709c18cd1323b5` says 15 cases at lines 61–67, but 0/14 at line 80 and “14-case population” at line 85. Actual CASES count is 15 and the base receipt says 0/15. Its wave text says 13 seats; the current worktree contract says 14 and also changes the population wording at line 85. Frozen contract bytes therefore differ from the current file; frozen counter and both base receipts exactly match current files. This review uses the pinned contract, preserved with receipts, not silently substituted worktree wording.

`count.py:25,412,426`: default REPO resolves to `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo`, not the lane root. Explicit `--root` avoids this in the controls replay; bare non-selftest CLI does not have the documented root default implied by the comment.

## Required C1 cheapest-bypass outcomes

- R1: canned receipt strings pass; receipt provenance/revision linkage and honest bootstrap are not enforced.
- R2: unrelated prefix-matching row passes; does not resist.
- R3: lesson reference with both preserved files absent fails (`critic=no late=no lesson_ref=yes`). Keeping only CriticClaims fails; keeping only late-shortcut fails. The conjunct independently demands both actual files, even though both exist at base. It resists this particular deletion shortcut. It does not require their original content/hash, a substantive preservation discussion, or valid nonempty file contents (`94–101`).
- R4: no flip anywhere fails; unrelated flip elsewhere passes, including explicitly CLOSED debts. It resists only literal token absence, not the required retained-open semantics.

## RFC 9111 verification and the 15-case population

Fetched https://httpwg.org/specs/rfc9111.html myself using GET, first through the reader and then curl for durable HTML/headers; curl exit 0. SHA-256 `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64`. Source bytes and headers are preserved.

[Section 4.2.1](https://httpwg.org/specs/rfc9111.html#calculating.freshness.lifetime) says: “either the first occurrence should be used or the response should be considered stale.” Therefore case 15, 200 then 100 → 200, is the first-occurrence choice, NOT minimum. Case 5, 100 then 200 → 100, alone would not discriminate minimum. The pair does. Important qualification: the RFC also allows considering duplicate freshness stale, and uses lowercase “should”; the contract’s uppercase “SHOULD” is not the complete normative wording. The chosen 200 expectation is valid policy, not the only RFC-compatible duplicate response.

| Case | Expected behavior | Source / assessment |
|---|---|---|
| 1 | max-age 3600 | §§4.2.1,5.2.2.1 |
| 2 | shared s-maxage 60 overrides 3600 | §§4.2.1,5.2.2.10 |
| 3 | private ignores s-maxage, 3600 | same sections |
| 4 | no-store → not storable | §5.2.2.5; null life/basis are local output policy |
| 5 | duplicate 100 then 200 → 100 | §4.2.1 first-occurrence choice |
| 6 | life 100 plus no_cache=true, conflict=true | §4.2.1 and §5.2.2.4; revalidation restriction dominates reuse; numeric life is not authorization |
| 7 | uppercase directive → 90 | §5.2 case-insensitive tokens |
| 8 | unknown teapot ignored → 60 | §5.2.3 |
| 9 | Expires minus Date → 1680 | §4.2.1; 28 minutes |
| 10 | large delta capped to 2147483648 | §1.2.2 permits overflow sentinel or greatest convenient positive integer; exact cap is selected local policy |
| 11 | must_revalidate=true, life 5 | §5.2.2.2 |
| 12 | qualified no-cache Set-Cookie, life 300 | §5.2.2.4; separate qualified list is reasonable, no_cache=false denotes no unqualified prohibition |
| 13 | max-age then no-store → not storable | §5.2.2.5 |
| 14 | no-store then max-age → not storable | same; order independent |
| 15 | duplicate 200 then 100 → 200 | §4.2.1 first occurrence, not min |

All 15 CASES were counted directly; full payloads/expected objects are preserved in `bypass-results.json` under the receipt directory. Cases match the contract’s bounded examples. JSON key names, basis strings, conflict/duplicate lists, and no-store null lifetime are local representation, not RFC-mandated JSON. `storable=true` cannot be a full RFC §3 eligibility conclusion without request method/status/authorization and other storage context; the contract explicitly excludes a full cache model. No case enables must-understand (all expect false), tests quoted numeric arguments, invalid input exit 1, usage exit 64, missing-Date fallback, invalid_directives nonempty, or general syntax/escape handling. Those capabilities are not established by 15/15.

## Executed checks and limits

- Assigned `env TMPDIR=/fast/scratch/hyaku/kake-r86/ReviewCounter python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/count.py --selftest`: exit 0, `selftest: 10/10 passed`.
- Pinned base C1/C2 replay and byte comparison: C1 mismatch; C2 exact. No after-carrier measurement or implementation tests assigned/performed.
- Direct frozen-conjunct fixture attacks only, in seat scratch; receipts include individual R3 missing-file results.
- Read-only `git show` pin comparisons: count/controls match freeze; contract does not. No VCS state changed.
- `xd://lsp` is not mounted (“No such tool”), so definitions/call paths above are source-text evidence, not semantic-LSP proof. No server was available to warm up or query references/diagnostics.
- C2 comparison uses Python equality, allowing e.g. numeric 1 to equal true; it is not a strict output-schema/type check (`233`). Exit-0 alone constitutes selftest_ok (`242`); no selftest content is checked. Case subprocess stderr is not part of acceptance. Selftest timeout is uncaught. Export directories are reused without clearing (`58–67`), so reusing a work directory for revisions with colliding 12-character prefixes can retain stale files. No such collision occurred in this review.
- No resume, rerouting runtime, or saturation behavior is implemented by these counters; no claims about those unrelated mechanisms are inferred. No D84-queue closure or independent admission is made.

Self-evaluation: accuracy 4 (original argv unavailable), completeness 4 (bounded source review, no production-reader review assigned), clarity 4 (many necessary limits), actionability 4 (frozen counter cannot be repaired in this seat), conciseness 4 (RFC table retained for audit); mean 4.0. Highest-impact recommendation: preserve honest C1 red and resolve receipt circularity/live-fleet reproducibility before any closure claim. Would the user agree: likely, because all failed controls remain visible.

Report: .ufo/waves/round-86/w1/ReviewCounter.md
Receipts: .ufo/waves/round-86/w1/ReviewCounter/
