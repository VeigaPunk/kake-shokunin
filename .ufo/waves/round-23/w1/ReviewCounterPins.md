## Verdict

**HOLD — one P2 operability finding.** At candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`, the counter rejects changed matrix/oracle bytes and enforces the `executed >= derived` floor. However, it does not pin the fixture bytes actually consumed by the matrix. A fixture-only change can therefore retain a 32/32 result while weakening the test represented by that row. This is an author-side recommendation, not independent admission.

## Findings

### P2 — Fixture content is outside the frozen instrument digest check

**Evidence:** `.ufo/waves/round-22/measure.py:62-68` pins only `MATRIX` and `CASES`; `:129-130` classifies the entire `fixtures/` tree as instrument inputs; `:471-480` checks only entries in `PINNED_INSTRUMENT_SHA256`. The runner collects/materializes fixture blobs but does not reject changed fixture hashes.

**Exact probe command:**

```text
git -C /tmp/kake-r23-ReviewCounterPins-xpdd/fixture-clone add .ufo/waves/round-22/fixtures/wrong_query/page.html && git -C /tmp/kake-r23-ReviewCounterPins-xpdd/fixture-clone -c user.name='ReviewCounterPins probe' -c user.email='review-counterpins@example.invalid' commit --quiet -m 'probe unpinned fixture change' && printf 'PROBE_HEAD=' && git -C /tmp/kake-r23-ReviewCounterPins-xpdd/fixture-clone rev-parse HEAD && python3 /tmp/kake-r23-ReviewCounterPins-xpdd/fixture-clone/.ufo/waves/round-22/measure.py --root /tmp/kake-r23-ReviewCounterPins-xpdd/fixture-clone --revision HEAD | jq '{available,accepted,total,acceptedDerivedFromRows,instrumentValidated,error,wrongQuery:.results[]|select(.caseId=="wrong_query")|{caseId,status,expectedExit,actualExit,expectedFindings,actualFindings},fixtureSha:.blobs[".ufo/waves/round-22/fixtures/wrong_query/page.html"].sha256,expectedFixtureSha:"unknown-to-counter"}'
```

**Exact observed output:**

```text
PROBE_HEAD=f20714ae8009af861dd91b0b475e6e9e37b0d008
{
  "available": true,
  "accepted": 32,
  "total": 32,
  "acceptedDerivedFromRows": true,
  "instrumentValidated": null,
  "error": null,
  "wrongQuery": {
    "caseId": "wrong_query",
    "status": "PASS",
    "expectedExit": 1,
    "actualExit": 1,
    "expectedFindings": [
      "canonical_mismatch"
    ],
    "actualFindings": [
      "canonical_mismatch"
    ]
  },
  "fixtureSha": "dc023f4ad0829bc755c8374e59fff224a5f869619f4566fcfed2e0756a68d251",
  "expectedFixtureSha": "unknown-to-counter"
}
```

The fixture was changed from `href="?x=wrong"` to `href="https://other.test/project/a.html?x=wrong"`. Its manifest still targets `https://example.test/project/a.html?x=expected`. The candidate's matrix and oracle remain the pinned versions; the changed fixture SHA is reported but not checked:

```text
original wrong_query/page.html: 3c5ff622447c13bd468ef98bdbcbe2c5d1406316efdec0cda32126a8c3f6281b  -
tampered wrong_query/page.html: dc023f4ad0829bc755c8374e59fff224a5f869619f4566fcfed2e0756a68d251  /tmp/kake-r23-ReviewCounterPins-xpdd/fixture-clone/.ufo/waves/round-22/fixtures/wrong_query/page.html
pinned matrix/oracle at candidate: d7de622cf149c4a7a0d3152b3d6c0560fadcc4c0c784c764502d0a2110bf4aab  -
28a49013d3aaf72b0e1c3801fd5359592602e079408d9a71c99f2df03d1cbeb6  -
```

**Impact / axis:** Operability evidence from the 32-case counter is not bound to the full input fixture set. **[INFERENCE]** This modified `wrong_query` row no longer isolates query comparison: a query-blind implementation can still report `canonical_mismatch` because the changed canonical host is `other.test` while the expected host is `example.test`. Thus an output of 32/32 does not establish that the frozen query fixture was exercised.

**Smallest fix:** Add a pinned digest for every fixture blob (including `escape.html`), or validate one deterministic digest over the complete sorted fixture path/digest set, before invoking the matrix. Apply the same check to the `--cases-root` instrument path.

## Checked and held

- Candidate baseline (`4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`) ran in a no-hardlinks `/tmp` clone whose observed initial HEAD was the candidate. Exact command:

  ```text
  python3 /tmp/kake-r23-ReviewCounterPins-xpdd/clone/.ufo/waves/round-22/measure.py --root /tmp/kake-r23-ReviewCounterPins-xpdd/clone --revision 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc | jq '{revision,available,accepted,total,acceptedDerivedFromRows,runnerSha256,instrumentRevision,matrixExitCode,caseCount:(.results|length),pinMatrix:.blobs[".ufo/waves/round-22/matrix.py"].sha256,pinCases:.blobs[".ufo/waves/round-22/cases.json"].sha256}'
  ```

  Exact output:
  ```json
  {
    "revision": "4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc",
    "available": true,
    "accepted": 32,
    "total": 32,
    "acceptedDerivedFromRows": true,
    "runnerSha256": "fa916ada90ac776deaa783403ddca883b75f68eb952b75029df762d566f44218",
    "instrumentRevision": "4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc",
    "matrixExitCode": 0,
    "caseCount": 32,
    "pinMatrix": "d7de622cf149c4a7a0d3152b3d6c0560fadcc4c0c784c764502d0a2110bf4aab",
    "pinCases": "28a49013d3aaf72b0e1c3801fd5359592602e079408d9a71c99f2df03d1cbeb6"
  }
  ```

- A committed fake matrix reporting all 32 oracle-shaped rows, together with a changed oracle, was rejected before execution. Exact observed output from the counter:

  ```json
  {"available":false,"unavailable":true,"accepted":0,"total":32,"instrumentValidated":false,"error":"frozen instrument digest mismatch: .ufo/waves/round-22/matrix.py, .ufo/waves/round-22/cases.json","pinnedMatrix":"b1574eb36f1605b23cdfd32fcd90bec25f6e082d610f4949a00435acabac163a","pinnedCases":"086d1f34f992d630fd3ae0f175c17ad90b197b962d6387e1e08909a8e46ac316"}
  ```

  The same altered instrument supplied via `--cases-root` while measuring baseline `7c61c8cc791bde36dd5e3688bdfea2678d90146c` returned `available=false`, `accepted=0`, `instrumentValidated=false`, and `error="frozen instrument digest mismatch: .ufo/waves/round-22/matrix.py, .ufo/waves/round-22/cases.json"`.

  Exact command and output:

  ```text
  python3 /tmp/kake-r23-ReviewCounterPins-xpdd/executed_floor_probe.py
  {"derived": 32, "executed": 0, "problems": ["executed=0 is not a count between derived 32 and the result rows"]}
  {"derived": 32, "executed": 31, "problems": ["executed=31 is not a count between derived 32 and the result rows"]}
  {"derived": 32, "executed": 32, "problems": []}
  ```
- Tried `read xd://lsp` for the required LSP status check; exact result: `No such tool: xd://lsp.` No semantic grep was used.

## Limits

Only this counter and its pinned fixture integrity were in scope. The fake-matrix and executed-floor probes were run in `/tmp` clones; no lane source or Git state was changed. No builds, linters, or general test suites were run. Runtime-routing and saturation claims are not assertions of this counter review.
