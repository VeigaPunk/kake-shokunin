## Verdict

C1's frozen **before** is failure-capable and the 17-unit population is honestly frozen, but the **after** predicate is not freshness-safe. A forged, entirely local receipt set with no live check passes 17/17; all-`UNVERIFIABLE` receipts also pass 17/17. This is a false-positive acceptance defect on the freshness axis, not a population defect.

## Findings

### P1 — A full C1 pass requires only plausible nonempty strings, not live re-verification

**Exact command** (run against a temporary clone checked out at candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`; attack revision `8590369e3c99a7c6ec7c2cfaf056b5c6d8ae18c9`):

```sh
python3 .ufo/waves/round-23/measure_c1.py --root /tmp/kake-r23-CritCounterC1-8-pCDu/clone --revision 8590369e3c99a7c6ec7c2cfaf056b5c6d8ae18c9
```

**Exact observed output excerpt:**

```json
{
 "accepted": 17,
 "claimVerdicts": {
  "HOLD": 17,
  "STALE": 0,
  "UNVERIFIABLE": 0
 },
 "revision": "8590369e3c99a7c6ec7c2cfaf056b5c6d8ae18c9",
 "total": 17,
 "units": [
  {
   "claims": {
    "HOLD": 1,
    "STALE": 0,
    "UNVERIFIABLE": 0
   },
   "pass": true,
   "problems": [],
   "unit": "drift-detection"
```

The output continued with `pass: true` and `problems: []` for every unit. In that temporary clone, each unit had just one claim: a one-character anchor taken from its base file, `claim: "placeholder"`, `surface: "not-a-live-surface"`, `method: "none"`, `observation: "not checked"`, `observedAt: "2026-10-21"`, and `verdict: "HOLD"`. Each unit file received only the required heading and `[<unit>:x]` citation. No live or local verification was performed. The test shows the counter does not enforce the stated receipt schema's 3–8 claims, 20–160-character anchors, allowed method values, or meaningful/claim-linked observations. It only requires nonempty strings, an anchor substring somewhere in the base file, and a citation. A literal empty/missing `observation` is rejected, but filler such as `"not checked"` passes.

**Impacted claim/axis:** C1 / freshness. The measured result can assert 17/17 fresh re-verifications while containing no re-verification evidence.

**Smallest safe correction:** Keep the frozen 17-unit list and its digest unchanged. Make the checker enforce the declared row contract (3–8 claims, 20–160-character exact base anchors, uniqueness where possible, allowed method, valid timestamp, etc.) and require evidence tied to each row's actual `surface` + `method` + `claim`, rather than arbitrary text. For evidence intended to prove a live observation, require independently reviewable/replayable output (for example, captured GET/HEAD status/final URL and response identity or exact local command/output); do not treat a free-text `observation` as proof. Structural validation alone cannot establish that a live check occurred.

### P1 — `UNVERIFIABLE` is a free-text escape hatch that counts as completed freshness

**Exact command** (temporary clone; attack revision `9581bd2eb16dd32e2be45a4f9122ac0a7106b499`):

```sh
python3 .ufo/waves/round-23/measure_c1.py --root /tmp/kake-r23-CritCounterC1-8-pCDu/clone --revision 9581bd2eb16dd32e2be45a4f9122ac0a7106b499
```

**Exact observed output excerpt:**

```json
{
 "accepted": 17,
 "claimVerdicts": {
  "HOLD": 0,
  "STALE": 0,
  "UNVERIFIABLE": 17
 },
 "revision": "9581bd2eb16dd32e2be45a4f9122ac0a7106b499",
 "total": 17,
```

All 17 units had `pass: true` and `problems: []`. The records still said `surface: "not-a-live-surface"`, `method: "none"`, and `observation: "not checked"`; adding only `verdict: "UNVERIFIABLE"` and `reason: "surface gone"` was sufficient. This is permitted by both the code (only a nonempty reason is checked) and contract C1's “counts as re-verified only with a reason” language. A reason does not establish that a surface existed, was probed, or is gone.

**Impacted claim/axis:** C1 / freshness. An all-unknown result saturates the metric at 17/17.

**Smallest safe correction:** Retain `UNVERIFIABLE` as an honest status, but count it as unresolved—not as a completed re-verification. If C1 intentionally grants an exception for a disappeared surface, require independently checkable failed-probe evidence and report that exception separately; a reason string alone must not increment `accepted`.

## Checked and held

- **Failure-capable before: yes.** The frozen and candidate checkers, and the working-tree checker used for this run, have identical SHA-256 `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe`.

  **Exact command:**
  ```sh
  python3 .ufo/waves/round-23/measure_c1.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 6847479d404d1dd93ecb59f99ff735bd7f010a4a
  ```

  **Exact observed output excerpt:**
  ```json
  {
   "accepted": 0,
   "claimVerdicts": {
    "HOLD": 0,
    "STALE": 0,
    "UNVERIFIABLE": 0
   },
   "revision": "6847479d404d1dd93ecb59f99ff735bd7f010a4a",
   "total": 17,
  ```
  The command exited with code `1`; every unit row reported `"problems": ["receipt missing"]`. Thus the frozen counter rejects the actual 0/17 state rather than passing vacuously. The lane's current `measure-c1-before.json` is not present in commit `6847479` (the direct `git show <freeze>:.ufo/waves/round-23/measure-c1-before.json` lookup failed), so that working-tree snapshot is not itself frozen evidence; the direct rerun above reproduces the baseline.

- **Population: accurate and frozen.** The population SHA-256 in the checker is `ffc9b3a44ee84ed827f3badc697f0ae5c8be007a50de3cafc2ccd23617697daf`, matching the frozen `c1-population.json` bytes. At base `b5d599e19bead54b96f589444e9ec64cdf67c28a`, searching `corpus/knowledge` for `historical-not-live-reverified` returned exactly the 16 entries in the frozen population: `drift-detection`, `fire-journal-codes`, `fleet-registry`, `free-read-verbs`, `ghp-subpath-spotcheck`, `keeper-timer-inert`, `kimi-subpath-audit`, `mirror-pitfalls`, `ops-automation`, `origin-repos`, `probe-delta-alerting`, `publish-channels`, `publish-queue`, `sitemap-orphan-audit`, `speedrun-pipeline`, and `vault-properties`. The same base has `SKILL.md:12: ## Property map (re-probed 2026-09-28; config `updatedAt` can lag live state)`, matching the 17th population unit and the contract's before statement. I found no denominator mismatch.

- The attack revisions and generated receipts were confined to `/tmp/kake-r23-CritCounterC1-8-pCDu/clone`; no lane production file or Git state was changed by these probes.

## Limits

No public HTTP GET/HEAD was made. These are local counter probes, so they establish that the validator accepts evidence-free receipts; they do not independently determine whether any underlying historical knowledge claim is currently true. No builds, lint, or formatters were run; no tools were installed.