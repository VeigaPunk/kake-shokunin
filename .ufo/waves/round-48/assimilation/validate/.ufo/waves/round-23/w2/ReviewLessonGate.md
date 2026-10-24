## Verdict

**Counterexample found.** The headline C1 `17/17` counter result is reproducible, but a targeted temporary-clone probe also makes the current counter accept 17 fabricated, unrun `HOLD` receipts as `17/17`. The lesson also has a three-row candidate-count discrepancy, swapped S030/S031 digest prefixes, and a `LOG round 23` pointer with no Round-23 entry in `LOG.md`. C2 and the parser-relaxation measurements reproduce as reported, with policy outcomes distinct from receipt coverage.

## Findings

### P1 — C1 counter credits fabricated, unrun live-reverification receipts (freshness)

- **Evidence:** `.ufo/waves/round-23/measure_c1.py` checks required fields are non-empty, a one-character anchor occurs in the base text, the claim ID is cited under the round-23 heading, and at least one verdict is `HOLD` or `STALE`. It does not validate whether the named surface/method was used or whether the observation is evidence of a live check. The `HOLD` attack reported in `w1/CritCounterC1.md` still satisfies the only post-freeze tightening (reject all-UNVERIFIABLE units).
- **Probe:** In a no-hardlinks clone of the integrated tree, replaced every unit receipt with one claim (`surface: "not-a-live-surface"`, `method: "none"`, `observation: "not checked"`, `verdict: "HOLD"`, one-character base anchor) and added only the required heading/citation. Probe commit: `958fec198b393b1d1ec8a75f4671f11f8b2125f4` (`counter probe: fabricated HOLD receipts`).
- **Exact counter command:**
  ```text
  python3 /tmp/kake-r23w2-ReviewLessonGate-probe-qhazmzi_/clone/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r23w2-ReviewLessonGate-probe-qhazmzi_/clone --revision HEAD
  ```
- **Exact observed probe summary:**
  ```json
  {
    "temp_clone": "/tmp/kake-r23w2-ReviewLessonGate-probe-qhazmzi_/clone",
    "exit": 0,
    "accepted": 17,
    "total": 17,
    "claimVerdicts": {"HOLD": 17, "STALE": 0, "UNVERIFIABLE": 0},
    "firstUnit": {
      "claims": {"HOLD": 1, "STALE": 0, "UNVERIFIABLE": 0},
      "pass": true,
      "problems": [],
      "unit": "drift-detection"
    }
  }
  ```
- **Impact / axis:** C1 freshness. A structurally valid but wholly unrun receipt set can satisfy the same unit-level `17/17` claim. `counter_selftest.py` covers all-UNVERIFIABLE rejection, but not fabricated HOLD receipts.
- **Smallest fix:** Do not treat free-text `surface`/`method`/`observation` as proof of live work. Require independently reviewable evidence bound to each claim (or label the metric strictly as receipt-structure coverage and leave live-verification status unproven); add a regression case for fabricated HOLD receipts.

### P2 — Gate candidate count is short by the three rejected rows

- **Evidence:** `corpus/lessons/round-23.md:28` says “Candidates: 168 C1 claim rows”; the Gate then admits 168 and rejects 3. `integrate-c1-summary.json` reports 168 admitted claims and `rejectedClaims: 3`; the three rejected records in `receipts/rejected.json` are from the same 29 Reverify*/Surface* seats.
- **Exact command:**
  ```text
  python3 -c "import json; d=json.load(open('.ufo/waves/round-23/integrate-c1-summary.json')); n=sum(u['claims'] for u in d['units'].values()); print('admitted claims total:',n); print('rejectedClaims:',d['rejectedClaims']); print('candidates implied:',n+d['rejectedClaims'])"
  ```
- **Exact observed output:**
  ```text
  admitted claims total: 168
  rejectedClaims: 3
  candidates implied: 171
  ```
- **Impact / axis:** Gate accounting for C1 freshness; the stated candidate and admitted/rejected counts cannot all be true as written.
- **Smallest fix:** Change the candidate total to 171, or say “168 admitted rows; 3 rejected from 171 submissions.”

### P2 — S030 and S031 SHA-256 prefixes are cross-assigned

- **Evidence:** `corpus/lessons/round-23.md:60-61` associates `a11dcf17…` with the S030 `syntax.html` URL, and `04b65bf0…` with the S031 `parsing.html` URL. Fresh public GETs on 2026-10-21 returned the opposite page digests.
- **Exact fetch/hash commands:**
  ```text
  curl -sS https://html.spec.whatwg.org/multipage/syntax.html -o /tmp/kake-r23w2-ReviewLessonGate-X7q2/syntax.html
  curl -sS https://html.spec.whatwg.org/multipage/parsing.html -o /tmp/kake-r23w2-ReviewLessonGate-X7q2/parsing.html
  sha256sum syntax.html parsing.html  (reported prefixes)
  ```
- **Exact observed prefixes:**
  ```text
  syntax.html:  04b65bf0b4b5f3bb3815…
  parsing.html: a11dcf1768a76e24cdf7…
  ```
- **Impact / axis:** Source-provenance pointers for both admitted WHATWG rows; the digests identify the opposite page bytes.
- **Smallest fix:** Swap the two digest prefixes in the source table (or replace them with the correct full digests).

### P2 — The cited `LOG round 23` evidence does not exist

- **Evidence:** `corpus/lessons/round-23.md:76` says the C2 end-to-end domain task is logged in `LOG.md` and cites “LOG round 23.” `LOG.md` currently ends with `## Round 22 — recovery attempt 2: falsification integrated and measured`; no Round-23 entry is present.
- **Exact search:** `functions.grep(pattern="Round 23|round 23|round-23|r23", path="/home/vgpnk/Projects/shokunin/kake-shokunin/LOG.md", case=false)`
- **Exact observed output:** `No matches found` (and `read LOG.md:-60` ends at the Round-22 recovery entry, line 781).
- **Impact / axis:** Operability evidence pointer and author-side SHONEN/C2 logging claim cannot be checked against the named record.
- **Smallest fix:** Add the actual Round-23 author-side LOG entry before citing it, or remove/qualify the claim until that record exists.

### P3 — S031's fragment does not locate the quoted SVG sentence

- **Evidence:** The lesson row at `corpus/lessons/round-23.md:61` links to `parsing.html#parsing-main-inforeign` but quotes “Insert a foreign element for the token, with SVG namespace.” `w1/SourceHTMLForeignContent.md` locates that SVG-namespace wording in the **in-body** SVG start-tag rule; its foreign-content quote is “Insert a foreign element for the token, with the adjusted current node's namespace.” The broader S031 registry row correctly covers both sections, but the lesson's fragment/quote pairing is imprecise.
- **Impact / axis:** Freshness/source-location precision for the admitted S031 row.
- **Smallest fix:** Point the SVG quote to `#parsing-main-inbody`, or quote the foreign-content rule actually located at `#parsing-main-inforeign`.

### P3 — The credited `ReviewHelpSynopsis` fix is incomplete on the error path

- **Evidence:** `corpus/lessons/round-23.md:74` credits “P3 fixed: `--help` in synopsis.” The `argparse` usage at `scripts/canonical_audit.py:122` now includes `-h | --help`, but the separate `usage()` synopsis at line 80 still omits both aliases.
- **Exact command:** `python3 scripts/canonical_audit.py --not-a-flag`
- **Exact observed output (selected complete usage lines):**
  ```text
  exit=64
  stdout={"findings":[],"pagesChecked":0,"verdict":"could-not-evaluate"}
  stderr=canonical_audit.py: one of the arguments --manifest --selftest is required
  usage: canonical_audit.py --manifest PATH [--json] | --selftest
  --help prints standard CLI help, exits 0, and emits no publishing verdict.
  ```
- **Impact / axis:** Operability; the reviewer finding covered inconsistent explicit and error-path synopses, but only the argparse synopsis was updated.
- **Smallest fix:** Use one synopsis for argparse and `usage()`, or describe the fix as partial and retain the residual inconsistency.

## Checked and held

- Integrated candidate `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` is HEAD; base `b5d599e19bead54b96f589444e9ec64cdf67c28a`, freeze `6847479d404d1dd93ecb59f99ff735bd7f010a4a`, and cited `4d95d2e` / `4e7dd1d` all resolve as commits. Freeze contains the contract, populations, and both counters before implementation. Contract, populations and C2 counter are unchanged from freeze; C1's later change is only the disclosed all-UNVERIFIABLE guard.
- `measure_c1.py --root . --revision 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` exited 0: 17/17, 168 claims = 79 HOLD + 49 STALE + 40 UNVERIFIABLE. Receipt census: 17 files, 168 rows, 29 seats (17 Reverify*, 12 Surface*); three rejected rows are separately recorded. The three rejected anchors are absent from the base unit text; C1's counter checks all admitted anchors and appended citations against base/revision bytes.
- `measure_c2.py --root . --revision 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` exited 0: 12/12 reproducible receipts. Outcomes are 3 clean, 5 failed-policy, 4 not-served; this is not 12 clean canonical results. `measure-c2-before-v2.json` records 0/12 at freeze.
- `counter_selftest.py` exited 0 with all 7 cases passing, including “C1 all-UNVERIFIABLE receipt rejected” and “C2 non-GET fetch rejected.” The fabricated-HOLD counterexample above remains outside that selftest.
- `relaxation_probe.py --validator scripts/canonical_audit.py` passed 11/11 (exit 0); the same probe on `4d95d2e` reported 2/11 and the nine attacks clean, and on `b539cc1` reported 7/11, with `body_base` and `body_base_selfclose` clean. Current parser source has a `foreign_stack`, fails closed on base/head/canonical-link signals in foreign content, and avoids HTML raw-text mode while inside foreign content.
- Round-22 replay `frozen/expected.json` contains exactly 64 fixture pins and 69 pins total; committed replay reports `frozen_replay_match`, 69 inputs, 32 cases. This supports the lessons' “64 fixture digests” claim. `4e7dd1d` records both misroot files as byte-identical 100% renames and adds `postfix/REPRODUCE.md`; `ExecReproduceBefore.md` reports `all_matched: true`, defect probe 2/8, and all three counter examples `rejected:false`.
- Round-22's 21 dead seats enumerate as Attack23 + 8 Boundary + 4 Connect + 8 Reopen. Round 23 has reports for the 18 re-runs (Attack23, all 8 Boundary, 4 dead Connect, 5 Reopen); the 3 omitted Reopen rows map to S020/S022/S027, which the round-22 verifier re-opened. The five round-23 source reopens S021/S023–S026 exist. `SOURCES.md` only adds S030/S031; no old source row was changed.
- `final-suite.txt` resolves to `.ufo/waves/round-22/final-suite.txt` (paths gate exit 1, carried 3 targets / missSet 55 / no new miss); the lesson should qualify this basename as round-22 evidence.
- The “Mistakes” arithmetic is otherwise consistent: 168 = 79+49+40; 11 = 9 attacks + 2 controls; the round-22 replay comparison is correctly pinned to `b539cc1`; and the QUALITY correction register/new parser-relaxation criterion exist. All named C1/C2 counters, the relaxation probe, and the counter selftest were run for this review.

## Limits

- `measure_c2.py` proves consistency/reproducibility of committed snapshot bytes and audit receipts; it does not independently authenticate the network GET event or fetchedAt metadata. The lesson does distinguish receipt coverage from clean/failed-policy/not-served outcomes; keep that boundary explicit.
- The live owned-property URLs were not fetched in this review; I reviewed the committed snapshots, counters and source receipts. Public WHATWG GETs were used only to compare S030/S031 page digests.
- LSP is not mounted (`read xd://lsp` returned `No such tool`), so no LSP status/references/definition/diagnostics were available. No build, lint, formatter, or broad test suite was run; no tools were installed. No lane production file or Git/JJ state was changed; only this requested report is to be written. Existing untracked wave-2 artifacts were present before this review.