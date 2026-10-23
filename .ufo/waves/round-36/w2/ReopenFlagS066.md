# Reopen S066 — `unsupported_type` (wave-2 falsify)

**Verdict: real as a media-type report (contract bullet (e) output), not a freshness defect.**
The live body is unchanged and the quote is faithful; the finding is a tool coverage limit
(`application/json` is outside the three supported types) plus an elided extracted quote
(`…` copied from the lesson table, not the SOURCES row). The row needs another check only if
JSON sources are in scope.

Sandbox: `/fast/scratch/hyaku/kake-r36w2/ReopenFlagS066/` (live body `body_noredirect.json`, `body_urllib.json`, `manifest/S066.body`, `demo/`, clone at f3a38bf8).

## What I ran

1. GET, no redirect following (curl default), exit 0, `timeout 60 curl -sS --max-time 50 -D hdrs_noredirect.txt -o body_noredirect.json \
   "https://api.github.com/repos/VeigaPunk/ds4cc-marketplace/actions/runs?head_sha=7fc6aa2fc12451dd451fed5a9ee7125f3a90e884"`
   - `HTTP/2 200`, `content-type: application/json; charset=utf-8`, no `Location` header,
     47323 bytes, sha256 `a8b628fe4c8508fde9667999e4f84f725529b5de9b2eed7b0d9984be1a72b42f`;
     body is pretty-printed (`{\n  "total_count": 3,`). No redirect hop to follow.
2. Same GET with the recorder's own UA/Accept (`source_snapshot.py:48,98`), exit 0: status 200,
   `application/json; charset=utf-8`, **40587 bytes, sha256 `df6fb5a4…4d9c9`** — byte-identical
   to the realrun snapshot member `S066.body` (`manifest/S066.body`, receipt
   `tar/receipts.json` id S066: `bodyBytes 40587`, same sha256, `fetchedUtc 2026-10-23T01:57:20Z`).
   GitHub serves this API compact to that UA and pretty to curl; parsed JSON and NFKC+whitespace-
   deleted text are identical (`norm(live)==norm(recorded): True`, both 40278 chars).
3. Tool on the extracted body, clone at `f3a38bf8e68f6cee386125d34b5e95ac9b2df66e`
   (`scripts/source_recheck.py` sha256 `577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48`,
   matching the SCORECARD build hash), `python3 -B clone/scripts/source_recheck.py --manifest demo/<f>.json`:
   - contentType `application/json; charset=utf-8`, quote as recorded →
     `{"verdict": "failed-policy", "checksEvaluated": 1, "findings": [{"check": "as_recorded_json", "reason": "unsupported_type", "target": null}]}`, exit 1 — reproduces the realrun finding.
   - contentType `text/plain; charset=utf-8`, quote as recorded (with `…`) →
     `{"reason": "quote_missing"}`, exit 1.
   - contentType `text/plain; charset=utf-8`, row's contiguous quote `"name":"Deploy marketplace to GitHub Pages"` →
     `{"verdict": "clean", "checksEvaluated": 1, "findings": []}`, exit 0.
   - contentType `text/html; charset=utf-8`, quote as recorded → `quote_missing`, exit 1.
4. id-paired diff of round-33 retained `gh-actions-runs-7fc6aa2f.json` (sha256 `92bd3b31…ce1c`,
   captured 2026-10-22T20:05:11Z) against the live JSON: **0 differing fields on all three runs**;
   only the array order moved (`[775,773,805]` → `[773,775,805]`).

## Live text

    "total_count": 3,
    "id": 39644779773,
    "name": "Deploy marketplace to GitHub Pages",
    ...
    "status": "completed",
    "conclusion": "success",
    "head_sha": "7fc6aa2fc12451dd451fed5a9ee7125f3a90e884",

The other two runs are unchanged too (`Validate Plugin Manifests` success, `Test Apps SDK wrapper`
failure). Both elision-separated parts of the input quote are present in the live body after the
tool's NFKC + whitespace deletion: `"name":"DeploymarketplacetoGitHubPages"` and
`"status":"completed","conclusion":"success"` (verified with the tool's own `normalize`). The
whole quote with `…` is present in neither live nor recorded body — `…` is the lesson's elision.

## Reading

- **Media type is real and correctly reported.** `application/json; charset=utf-8` is not
  `text/html`, `application/xhtml+xml` or `text/plain`, so bullet (e) mandates one
  `unsupported_type` and no quote check; the sealed key (cases.json, bullet e, `o.bin`) pins that
  behaviour, and the tool did not misparse anything.
- **Source is fresh.** Same runs, ids, conclusions and quote text as the round-33 capture seven
  hours earlier; no page change, no JS-rendered dependency (raw API body), no paraphrase.
- **The quote is an extraction artifact.** SOURCES.md:74 carries the contiguous support quote
  `"Deploy marketplace to GitHub Pages"`; the `…` form comes from the round-33 lesson admit row
  (`corpus/lessons/round-33.md:32`), which the Gate-quote extraction used. S066 is the only one of
  the 90 input quotes containing `…`, and `…` can never match under bullet (d).
- **Row needs a different check only if JSON is in scope.** Treating `application/json` as
  `text/plain` and quoting the contiguous span is clean (run 3c, exit 0); if the contract stays as
  declared, dataset/API rows should be declared out of the quote check, not surfaced as failures.
- **Contract calibration (advisory, sealed so not a bug):** `unsupported_type` yields
  `failed-policy` while the sibling capability limit `charset_unsupported` yields
  `could-not-evaluate`, so any manifest holding a JSON/XML endpoint can never be clean (S016 and
  S066: 2 of the realrun's 14 findings) and the exit code reads as source drift. The real-input
  lesson (`corpus/lessons/round-36.md:69-72`) already labels these "JSON endpoints", so the
  landing text is not overstated.

## Not verified

Did not re-run the 28-case counter or the full 90-body audit (only S066), and did not fetch
S066's second registered URL (`apps-sdk.yml/runs?branch=main`, prose-only in the row).
