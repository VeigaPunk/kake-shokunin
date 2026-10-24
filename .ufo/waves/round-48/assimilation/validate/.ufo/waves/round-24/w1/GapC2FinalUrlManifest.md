## Verdict

The validator re-run did not crash on any requested finalUrl shape: every runner invocation had empty stderr and no traceback. However, the chain-consistent malformed control-character receipt was accepted as a pass (counter exit 0, `could-not-evaluate` verdict), which is an actionable C2 operability defect.

## Findings

### P2 — A served receipt with an invalid finalUrl and reproducible input-error audit is counted as passing

- **Impacted claim/axis:** round-24 C2 / operability; the measured claim requires malformed receipts to be rejected.
- **Exact command:** `python3 /tmp/kake-r24-GapC2FinalUrlManifest-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2FinalUrlManifest-clone --revision a33be5524fdd1389474ba889704406475b4f976c`
- **Observed output:** counter exit `0`, `accepted=12`, `total=12`, `stderr` empty, no traceback, stdout tail exactly `}`; `ds4cc-primary` was `{"pass":true,"problems":[],"verdict":"could-not-evaluate"}`. The validator itself reproduced `exit=2` with `{"findings":[{"id":"input_invalid","page":"https://ds4cc.com/\n"}],"pagesChecked":0,"verdict":"could-not-evaluate"}`.
- **Reproduction:** committed receipt `a33be5524fdd1389474ba889704406475b4f976c` from base `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. Set `finalUrl` to `https://ds4cc.com/\n`, added a structurally matching 302 hop from the population URL to that finalUrl, and set `audit.json` to the validator's exact exit-2 JSON result. The stored page and fetch body digest were unchanged. Thus chain consistency and exact audit reproduction both pass despite the invalid HTTP(S) URL and zero evaluated pages.
- **Smallest fix:** in maintained `scripts/receipt_replay.py`, do not credit a served receipt when canonical audit returns exit 2 / `could-not-evaluate` (or an `input_invalid` finding); retain reproducible exit-0 `clean` and exit-1 `failed-policy` results. The base replay already accepts legitimate `failed-policy` results, so requiring `clean` would be too strict.

## Checked and held

- Clone: `/tmp/kake-r24-GapC2FinalUrlManifest-clone`, observed initial HEAD `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. Each case commit was made on a child branch from that frozen base, with author and committer dates fixed at `2026-10-21T12:00:00Z`; hashes are shown below.
- Base command: `python3 /tmp/kake-r24-GapC2FinalUrlManifest-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2FinalUrlManifest-clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436`. Exact summary: `accepted=12`, `total=12`, validator SHA-256 `23638a87dba90f151bc65ed220983ab948989a5dfadf64f62469ceeabe45d0a4`; exit `0`.
- Per-case command: `python3 /tmp/kake-r24-GapC2FinalUrlManifest-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2FinalUrlManifest-clone --revision <case-commit>`. `stderr` was empty in all six runs; the final stdout line was exactly `}` in every run.
- Exact target-surface output excerpts parsed from each runner stdout:

| Case | Committed revision | Runner exit | Accepted / total | Traceback | stdout tail | `ds4cc-primary` result |
|---|---|---:|---:|---|---|---|
| `finalurl-c0-lf-single` | `15f375b56b36f048710a3a7fd1c976c5c9d3e633` | `1` | `11/12` | `false` | `}` | `{"id":"ds4cc-primary","pass":false,"problems":["fetch finalUrl differs from redirect chain","audit.json {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}} != reproduced {'exit': 2, 'result': {'findings': [{'id': 'input_invalid', 'page': 'https://ds4cc.com/\\n'}], 'pagesChecked': 0, 'verdict': 'could-not-evaluate'}}"],"verdict":"could-not-evaluate"}` |
| `finalurl-c0-lf-chain-consistent` | `a33be5524fdd1389474ba889704406475b4f976c` | `0` | `12/12` | `false` | `}` | `{"id":"ds4cc-primary","pass":true,"problems":[],"verdict":"could-not-evaluate"}` |
| `finalurl-javascript` | `86c14cc3c2b4dc24107df1d16f0568ab0d175419` | `1` | `11/12` | `false` | `}` | `{"id":"ds4cc-primary","pass":false,"problems":["fetch finalUrl differs from redirect chain","audit.json {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}} != reproduced {'exit': 2, 'result': {'findings': [{'id': 'input_invalid', 'page': 'javascript:alert(1)'}], 'pagesChecked': 0, 'verdict': 'could-not-evaluate'}}"],"verdict":"could-not-evaluate"}` |
| `finalurl-long-8210` | `8f7e18eb6c92c33858acf5f4128ca0a893632a2b` | `1` | `11/12` | `false` | `}` | `{"id":"ds4cc-primary","pass":false,"problems":["fetch finalUrl differs from redirect chain"],"verdict":"clean"}` |
| `finalurl-nonascii-host` | `c8fd66d275f449f5e58efa6d8d3500f32dcf1e65` | `1` | `11/12` | `false` | `}` | `{"id":"ds4cc-primary","pass":false,"problems":["fetch finalUrl differs from redirect chain","audit.json {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}} != reproduced {'exit': 2, 'result': {'findings': [{'id': 'input_invalid', 'page': 'https://b\u00fccher.example/'}], 'pagesChecked': 0, 'verdict': 'could-not-evaluate'}}"],"verdict":"could-not-evaluate"}` |
| `finalurl-unchanged-control` | `04ad1b1851ceb4663fd03379f9d27986960f64d6` | `0` | `12/12` | `false` | `}` | `{"id":"ds4cc-primary","pass":true,"problems":[],"verdict":"clean"}` |

Single-field finalUrl mutations changed only `fetch.json`; `audit.json` and `page.html` remained at base bytes. The validator re-run produced structured output for the LF, javascript scheme, non-ASCII host, and 8,210-octet URL; none crashed. The first three returned validator exit 2 / `input_invalid` and the long URL returned validator exit 0 / `clean`, but the altered finalUrl broke the empty redirect-chain endpoint in each single-field receipt, so those receipts were rejected. The sixth case coordinated the redirect chain and `audit.json`; it demonstrates that a reproducible input-error result is accepted unless the maintained replay rejects it explicitly.

- RFC 3339 §5.6 defines the Internet date/time profile; the tested `fetchedAt` remained `2026-10-21T06:33:03Z`. RFC 9110 §8.3.1 defines HTTP media-type grammar; `contentType` remained `text/html; charset=utf-8`, so the served-page path was exercised. Neither section defines finalUrl validity. RFC 8259 §7 requires JSON string controls U+0000–U+001F to be escaped; the LF case is valid JSON with an escaped LF, which decodes to an unsupported URI control. RFC 3986 §3.2.2 requires non-ASCII registered-name data to be UTF-8 percent-encoded and DNS IDNs to be IDNA-transformed before lookup; raw Unicode host input is outside the validator's ASCII DNS profile. RFC 9112 §3 states that HTTP has no predefined request-line limit and RECOMMENDS support for at least 8,000 octets; RFC 8259 §9 permits implementation-specific limits. The 8,210-octet test was not rejected solely for length: the validator completed cleanly and only the deliberately inconsistent single-field receipt failed.

The C2 case array follows. For `finalurl-c0-lf-chain-consistent`, the primary mutation is the finalUrl set shown in the case; the same committed test also added the matching 302 hop and replaced `audit.json` with the exact validator exit-2 result as explained above. Long URL value is exactly `https://ds4cc.com/` followed by 8,192 ASCII `a` characters (8,210 octets total):

```json
[
 {
  "id": "finalurl-c0-lf-single",
  "target": "c2",
  "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
  "op": "set",
  "jsonPath": [
   "finalUrl"
  ],
  "value": "https://ds4cc.com/\n",
  "expect": "reject",
  "why": "Reject: with redirects empty, finalUrl no longer equals the chain endpoint; RFC 8259 \u00a77 requires the LF to be escaped in JSON, but escaping does not make the decoded URI control valid.",
  "r23Observed": {
   "exit": 1,
   "traceback": false,
   "stdoutTail": "}"
  }
 },
 {
  "id": "finalurl-c0-lf-chain-consistent",
  "target": "c2",
  "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
  "op": "set",
  "jsonPath": [
   "finalUrl"
  ],
  "value": "https://ds4cc.com/\n",
  "expect": "reject",
  "why": "Reject even with a structurally matching 302 hop and audit.json replaced by the validator's exact exit-2 result: the finalUrl still contains a URI control and the validator cannot evaluate the served page.",
  "r23Observed": {
   "exit": 0,
   "traceback": false,
   "stdoutTail": "}"
  }
 },
 {
  "id": "finalurl-javascript",
  "target": "c2",
  "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
  "op": "set",
  "jsonPath": [
   "finalUrl"
  ],
  "value": "javascript:alert(1)",
  "expect": "reject",
  "why": "Reject: with redirects empty, finalUrl no longer equals the chain endpoint; the replayed canonical-audit contract only accepts HTTP(S) URLs, while RFC 9110 \u00a78.3.1 specifies media types rather than URL schemes.",
  "r23Observed": {
   "exit": 1,
   "traceback": false,
   "stdoutTail": "}"
  }
 },
 {
  "id": "finalurl-long-8210",
  "target": "c2",
  "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
  "op": "set",
  "jsonPath": [
   "finalUrl"
  ],
  "value": "https://ds4cc.com/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "expect": "reject",
  "why": "Reject: with redirects empty, finalUrl no longer equals the chain endpoint; the 8,210-octet value is not invalid solely by length because RFC 9112 \u00a73 sets no predefined request-line limit and RFC 8259 \u00a79 permits implementation-specific limits.",
  "r23Observed": {
   "exit": 1,
   "traceback": false,
   "stdoutTail": "}"
  }
 },
 {
  "id": "finalurl-nonascii-host",
  "target": "c2",
  "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
  "op": "set",
  "jsonPath": [
   "finalUrl"
  ],
  "value": "https://b\u00fccher.example/",
  "expect": "reject",
  "why": "Reject: with redirects empty, finalUrl no longer equals the chain endpoint; RFC 3986 \u00a73.2.2 requires non-ASCII registered-name data to be UTF-8 percent-encoded and IDN names to be transformed to IDNA before lookup.",
  "r23Observed": {
   "exit": 1,
   "traceback": false,
   "stdoutTail": "}"
  }
 },
 {
  "id": "finalurl-unchanged-control",
  "target": "c2",
  "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
  "op": "set",
  "jsonPath": [
   "finalUrl"
  ],
  "value": "https://ds4cc.com/",
  "expect": "accept",
  "why": "Accept: the set preserves the original finalUrl, empty redirects, and matching replay receipt.",
  "r23Observed": {
   "exit": 0,
   "traceback": false,
   "stdoutTail": "}"
  }
 }
]
```

## Limits

- The chain-consistent reproduction uses a structurally valid but synthetic redirect receipt; as the C2 contract notes, replay does not authenticate the original network observation. Its purpose is to test whether the counter rejects malformed finalUrl inputs even when its recorded components reproduce exactly.
- The frozen-contract path `.ufo/waves/round-24/c2-population.json` was not present at this checkout (`read` returned “Path not found”); these manually executed cases are not asserted to match a later generated population.
- No installs or updates were made. Only the sandbox clone and this assigned report path were written; no lane production file was modified.
