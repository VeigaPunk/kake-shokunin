## Verdict

C2 SHA/page audit complete: four receipt mutations were committed and replayed from the frozen round-23 base. The old runner correctly rejects a digest copied from another page, a `page.html` on a not-served surface, and an integer `sha256`, with no traceback. It also rejects uppercase hexadecimal for the exact digest; I classify that as an unintended false reject because the documented receipt contract requires the SHA-256 of the stored bytes but does not require lowercase spelling. No lane implementation file was changed; this report is the only lane write. This is author-side evidence, not independent admission.

## Findings

- **P2 — Uppercase SHA spelling is a valid digest control but is rejected.**
  - **Command:** `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-KakeR24.GapC2ShaPage-clone --revision HEAD` at committed probe `2b48b71d69e7759222d22d9a2dff4c80490bfca5`.
  - **Observed output (faithfully abbreviated):** `"accepted": 11`, `"total": 12`; `ds4cc-primary` has `"pass": false`, `"problems": ["page.html missing or digest differs from fetch.sha256"]`, `"verdict": null`; process exit 1, no traceback, stdout tail `}`.
  - **Expected:** accept. Uppercase A–F represents the same hexadecimal SHA-256 value; the runner's documented contract does not state a lowercase-only encoding. RFC 8259 §3 permits a string value but does not define digest casing. RFC 3339 §5.6 concerns timestamp syntax, and RFC 9110 §8.3.1 concerns media types, so neither requires lowercase digest text.
  - **Impacted claim/axis:** C2, operability; valid hash representation is rejected by receipt replay.
  - **Smallest fix:** validate a 64-character hexadecimal string and compare its decoded digest (or normalized hex) with the page digest; alternatively, if lowercase-only is intended, state that explicitly in the maintained receipt contract and keep this case a reject. The current round-23 docs do not make that restriction.

- **P3 — The three malformed page-binding controls are rejected as required.**
  - **Commands:** the same runner command above, with `--revision HEAD` at commits `2bc322c1b281a233656acc26ad59c0634e08d11b`, `93b6948877edac187134620c480c3ebd072afbda`, and `1c9631714980aec429434df987eaa2d2b51bd2e9` respectively.
  - **Observed output:** for the different-page digest and integer SHA cases, stdout reports `"accepted": 11`, `"total": 12` and `ds4cc-primary` false with `"page.html missing or digest differs from fetch.sha256"`; for the not-served page case, stdout reports `"accepted": 11`, `"total": 12` and `charter-kimi` false with `"page.html stored for a non-served response"`, verdict `"not-served"`. Each process exited 1 without a traceback; each stdout tail was `}`.
  - **Expected:** reject all three. The round-23 `measure_c2.py` contract requires a digest of stored page bytes and requires no `page.html` for a not-served response. RFC 8259 §3 distinguishes JSON strings from numbers, so integer `sha256` is not the digest string; RFC 9110 §8.3.1 defines the media type but does not make a 404 response a 2xx served surface.
  - **Impacted claim/axis:** C2, operability; these negative controls behaved as specified.
  - **Smallest fix:** none indicated by these probes.

## Checked and held

- Read the frozen contract `.ufo/waves/round-24/contract.json`, round-23 `measure_c2.py`, C2 population, and representative receipts. The runner's module contract says a served page needs a `sha256` of its stored body, while a not-served surface has no stored `page.html`; `served()` requires 2xx plus `text/html`.
- Clone command: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-KakeR24.GapC2ShaPage-clone`. Observed initial clone HEAD: `f7de3ab4e9f030a15a857a5a08631bd8e690f436` (the assigned base). The final clone HEAD is the integer-SHA probe `1c9631714980aec429434df987eaa2d2b51bd2e9`; named probe branches retain all four commits. Each probe commit used `GIT_AUTHOR_DATE=2026-10-21T12:00:00Z` and `GIT_COMMITTER_DATE=2026-10-21T12:00:00Z`.
- Baseline control command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-KakeR24.GapC2ShaPage-clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436`. Exact summary: `"accepted": 12`, `"total": 12`, revision `f7de3ab4e9f030a15a857a5a08631bd8e690f436`; exit 0.
- The foreign digest used in the second mutation was computed from the committed `ds4cc-kimi` page: `git -C /tmp/kake-r24-KakeR24.GapC2ShaPage-clone show f7de3ab4e9f030a15a857a5a08631bd8e690f436:.ufo/waves/round-23/live/ds4cc-kimi/page.html | sha256sum` → `108f5aca89b9cac35df0ea24930618045be142ed24fc696580f9fc6dff1574c5  -`.
- Retained committed mutation files and SHA-256 (absolute paths; lane-relative paths are in the JSON cases below):
  - `/tmp/kake-r24-KakeR24.GapC2ShaPage-clone/.ufo/waves/round-23/live/ds4cc-primary/fetch.json` at `2b48b71d69e7759222d22d9a2dff4c80490bfca5`: `cb984798beba76ecb5eb8ef7a26e81f9954afd1a072171cfd80e13c02d9b4859`.
  - `/tmp/kake-r24-KakeR24.GapC2ShaPage-clone/.ufo/waves/round-23/live/ds4cc-primary/fetch.json` at `2bc322c1b281a233656acc26ad59c0634e08d11b`: `3a80a94163610fd194db497726eb6b87ded14eb8502cf52bfc49f86c722a3cc8`.
  - `/tmp/kake-r24-KakeR24.GapC2ShaPage-clone/.ufo/waves/round-23/live/charter-kimi/page.html` at `93b6948877edac187134620c480c3ebd072afbda`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (zero-byte file; the probe is about file presence on a not-served surface).
  - `/tmp/kake-r24-KakeR24.GapC2ShaPage-clone/.ufo/waves/round-23/live/ds4cc-primary/fetch.json` at `1c9631714980aec429434df987eaa2d2b51bd2e9`: `29ce6c411606491a74f7f7489485cbc79c1b77504ff0634f88017f81d1e975e8`.
- Public RFC references read from RFC Editor on 2026-10-21: RFC 3339 §5.6 (`https://www.rfc-editor.org/rfc/rfc3339`), RFC 9110 §8.3.1 (`https://www.rfc-editor.org/rfc/rfc9110`), and RFC 8259 §3 (`https://www.rfc-editor.org/rfc/rfc8259`). No installs or upgrades.
- C2 malformed-case records for exactly the four executed mutations:

```json
[
  {
    "id": "uppercase-sha256",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": ["sha256"],
    "value": "CCB3F46EDA1CE3270DF1E3373D49C4034025C4F475A6999142279E03B00B2BB8",
    "expect": "accept",
    "why": "Uppercase hexadecimal encodes the same SHA-256 value and the documented receipt contract does not require lowercase (RFC 8259 §3 permits a string but does not define digest casing).",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "sha256-from-different-page",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": ["sha256"],
    "value": "108f5aca89b9cac35df0ea24930618045be142ed24fc696580f9fc6dff1574c5",
    "expect": "reject",
    "why": "The round-23 contract requires the digest of the stored page bytes; this value was hashed from the different committed ds4cc-kimi page.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "page-present-not-served",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/page.html",
    "op": "set",
    "jsonPath": [],
    "value": "",
    "expect": "reject",
    "why": "The round-23 contract requires no page.html for a not-served response; a 404 is not served merely because a response has a media type (RFC 9110 §8.3.1).",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "sha256-as-integer",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": ["sha256"],
    "value": 123,
    "expect": "reject",
    "why": "A JSON number is not the receipt's hexadecimal digest string; RFC 8259 §3 defines number and string as distinct JSON value types.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  }
]
```

## Limits

- These are mutation probes against the historical round-23 runner only; no edits were made to `measure_c1.py`, `measure_c2.py`, or lane production code. The replay validates stored artifacts and does not authenticate the original network observation.
- The uppercase-hash expectation follows semantic digest equality because the frozen round-23 doc does not explicitly require lowercase. If the lane wants canonical lowercase receipts, that is a contract clarification decision; the old runner currently rejects the uppercase variant.
- No builds, linters, formatters, or tests were run; only the requested targeted receipt-replay CLI probes and read-only RFC/reference inspection were performed.
