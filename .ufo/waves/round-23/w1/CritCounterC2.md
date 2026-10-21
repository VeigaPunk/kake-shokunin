## Verdict

C2 is **not established at candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`**: the named counter returns `accepted: 0` because that revision contains no per-surface `fetch.json`/`audit.json` receipts. More fundamentally, a passing `measure_c2.py` receipt would prove that committed metadata and bytes are internally consistent and that the committed validator reproduces the committed audit—not that an HTTP GET actually occurred, that the body came from the named URL, or that canonical policy passed.

The strongest admissible positive reading is narrower: **a read-only snapshot-and-audit workflow was attempted for each frozen URL; for each served body, its committed bytes can be re-audited reproducibly under the pinned local policy; unavailable outcomes are reported separately.** That supports operability only if the snapshot producer is trusted as the source of the GET claim and `accepted` is described as receipt coverage, not a clean or independently proven end-to-end preflight. A successful validator verdict is not part of the counter's acceptance condition.

## Findings

### P1 — Candidate revision does not contain the receipts C2 requires

- **Command:** `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`
- **Exact observed output (selected fields; the identical missing-receipt problem was emitted for all 12 IDs):**
  ```json
  {
   "accepted": 0,
   "revision": "4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc",
   "surfaces": [
    {
     "id": "ds4cc-primary",
     "pass": false,
     "problems": ["fetch.json or audit.json missing"],
     "verdict": null
    }
   ],
   "total": 12,
   "validatorSha256": "d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac"
  }
  ```
- **Impacted claim/axis:** C2 / operability, specifically its “every surface has a committed read-only snapshot ... and an audit receipt” after-state. The existing working-tree `live/` files do not satisfy a counter run over the named commit; `measure_c2.py` uses `git show <revision>:...`.
- **Smallest safe correction:** Commit the generated snapshots and receipts in the measured revision, then run the counter against that resulting commit. Until then, C2 is unmeasured/not met at this candidate; do not substitute working-tree presence for committed evidence.

### P1 — Replay proves audit reproducibility, not network provenance or a successful preflight

- **Command:** none; static inspection of `measure_c2.py:31-39,42-84,92-108` and `scripts/live_snapshot.py:50-91`.
- **Exact observed code behavior:** `measure_c2.py` obtains `page.html`, `fetch.json`, and `audit.json` from the selected commit; checks the page SHA-256 against the `sha256` field in that same committed `fetch.json`; reconstructs a manifest using the committed `fetch.finalUrl` plus the frozen `expectedCanonical`; re-runs the revision's `scripts/canonical_audit.py`; and compares the resulting JSON/exit to the committed `audit.json`. It does not issue or independently observe a request, and it does not authenticate the claimed `url`, `finalUrl`, `status`, `fetchedAt`, or digest against a network response. `live_snapshot.py` does perform a GET and create these files, but the counter does not verify that this producer ran or attest its output.
- **Exact acceptance behavior:** the served branch returns `actual["result"]["verdict"]`; `main` sets `"pass": not problems` and counts those rows. Thus an exact replay of `failed-policy` or `could-not-evaluate` is accepted as a valid receipt, not as a clean policy result. This is defensible for a *capability/receipt-coverage* measure, not for a claim that every surface passed canonical policy.
- **Impacted claim/axis:** C2 / operability, and the words “live-served HTML” and “end-to-end” if taken as independently proven network provenance or policy success.
- **Smallest safe correction:** State the scope as reproducible re-audit of a committed snapshot plus producer-reported GET metadata; keep per-surface audit verdicts visible and report clean, failed-policy, could-not-evaluate, and not-served counts separately. If C2 intends to prove the GET rather than trust its producer, require an independently verifiable run attestation; a self-authored JSON/hash pair cannot prove that event.

### P2 — `not-served` is receipt-accepted, and the branch can accept a no-response error as well as an HTTP status

- **Command:** none; static inspection of `measure_c2.py:36-39,57-62,102-108`. The current worktree also contains `.ufo/waves/round-23/live/plazir27-kimi/fetch.json` and `audit.json` (not present in the measured candidate revision).
- **Exact observed local evidence:** `fetch.json` records `"status": 404`, `"contentType": "text/html; charset=utf-8"`, `"error": null`; its `audit.json` is `{"error":null,"exit":null,"status":404,"verdict":"not-served"}`. The current `live-summary.json` records four `404`/`not-served` surfaces. This is an attempted-URL/status observation, not a canonical audit of served HTML.
- **Exact code path:** every `not served` case is returned with verdict `not-served` after checking only that no page exists and the receipt status equals `fetch.status`. It does not require an integer HTTP response status. Because `served(fetch)` is also false when `fetch.error` is non-null, a record with no HTTP status and a matching `not-served` receipt can reach the no-problems/`pass: true` path. That example is inferred from the shown branch; I did not execute a synthetic mutation.
- **Impacted claim/axis:** C2 / operability. Treating actual 404s as *completed probe coverage* is honest if stated as such; calling them passing canonical preflights is not. Treating DNS/TLS/timeout errors or truncated/non-HTML responses as `not-served` with status `null`/`200` further blurs a completed HTTP classification with an uncompleted/unusable audit.
- **Smallest safe correction:** Keep 404 as a valid recorded outcome but never label it a canonical-policy pass. Emit separate attempted/response-recorded, served-and-evaluated, and policy-clean counts. Require an actual integer HTTP status for `not-served`; classify transport errors, truncation, and non-HTML responses distinctly, and do not count them as successful surface preflights.

### P2 — Frozen `expectedCanonical` values are usable local policy, but not all are property-map facts or live-verified

- **Command:** none; static inspection of `c2-population.json:4-5,7-78`, `SKILL.md:16-28,394-407`, and the current `live-summary.json`.
- **Exact observed policy/evidence:** population declares `"policy": "local publisher policy: one head canonical equal to expectedCanonical; mirrors declare their primary"`. The map explicitly calls the charter GHP page the “canonical doc” and says its Kimi variants canonicalize there (`SKILL.md:18`), calls `plazir27.kimi.page` the canonical Kimi charter mirror (`:22`), and calls Lucario GHP canonical (`:26`). The map identifies ds4cc.com as primary (`:16`). By contrast, `expectedCanonical = self` for burnerchrome, the vault, and `ufo-fsd.kimi.pro` is explicitly a “no primary on record: self-canonical” policy choice in the population, not a fact implied by “no primary.” The population also assigns expected values to the plazir15, charter, and lucario Kimi slots, which the map describes as 404/never-published; the current summary additionally reports plazir27 Kimi as 404. None of these current responses provides served HTML on which to test the expected value. The C2 policy is explicitly local; round-22 guidance says matching it means “Local policy clean, not complete publication readiness” and canonical declarations are not Google-selection guarantees (`SKILL.md:399,404`).
- **Observed current summary:** among 12 rows, 4 are `not-served`, 4 served rows are `could-not-evaluate`, 3 are `failed-policy`, and 1 is `clean`. Therefore receipt acceptance cannot be read as a clean canonical result for this population.
- **Impacted claim/axis:** C2 / operability. The choices are defensible as fixed local test expectations where the map names a primary/canonical target, and as explicit owner-policy defaults where it does not. They are not evidence that an unserved page declares that value, nor an independent SEO/search-engine determination.
- **Smallest safe correction:** Preserve the frozen expectations (do not silently tune them to current content), but describe the no-primary self-canonical entries as owner-ratified local defaults and dead/unpublished rows as conditional policy expectations. Keep “policy mismatch” and “unable/not served” outcomes visible rather than treating them as successful canonical checks.

## Checked and held

- Ran the named C2 counter once against candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`; it exited 1 with `accepted: 0`, `total: 12`.
- Read the snapshot producer and counter; the producer's code issues GETs, while the counter only replays files read from the measured revision.
- Read the frozen population, the property-map rows, the prior local canonical-policy limits, and the current local summary / one 404 snapshot pair.
- No lane production files were modified, no external URL was fetched, and no tools were installed.

## Limits

No independent network GET or synthetic mutation was performed. The working-tree `live/` snapshot and `live-summary.json` are treated only as local observations; the counter's candidate-revision output establishes that per-surface receipts were absent from that commit. This review makes no claim about Google-selected canonicals, headers, duplicate-content selection, or later revisions.