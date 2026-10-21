# GapC2UrlMethod — C2 audit, url/method axis (round 24, author-side)

Base f7de3ab4e9f030a15a857a5a08631bd8e690f436 · runner `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root <clone> --revision <head>` · sandbox clone `/tmp/kake-r24-GapC2UrlMethod-k9HT/clone` (HEAD at probe `255ca93159db21c8582644a62cebaf16c829095a`), per-case results `/tmp/kake-r24-GapC2UrlMethod-k9HT/results.json`.

## Verdict

On the url/method axis the round-23 runner at the frozen revision is already conformant: all 9 malformed variants I applied to a committed receipt (`.ufo/waves/round-23/live/ds4cc-primary/fetch.json`) are rejected with exit 1 and **no traceback**, each citing the exact documented check, and the unknown-member control stays accepted (exit 0). The C2 "before" gaps (lexical dates, `contentType` crash) live on other axes; none appeared here. These 10 cases are fit to freeze into the round-24 C2 population as regression cases that the maintained `scripts/receipt_replay.py` must reproduce exactly (reject 9, accept 1). Every case ran: applied to the committed receipt, committed (`GIT_COMMITTER_DATE=GIT_AUTHOR_DATE=2026-10-21T12:00:00Z`, verified via `git log --format='%h %ad %cd' --date=iso`), runner executed at that probe HEAD. Round-23 runners untouched (byte-intact historical evidence).

## Findings

No P0–P2 defects found on this axis. One P3 observability item.

- **P3 — runner stdout tail is non-discriminating.** Command: `python3 .ufo/waves/round-23/measure_c2.py --root <clone> --revision <head>`; observed: stdout is one `indent=1, sort_keys=True` JSON document whose literal last line is `}` for every outcome (accept and all 9 rejects), so `r23Observed.stdoutTail` cannot distinguish cases; the discriminating strings sit mid-document (quoted per case below). Impacted claim/axis: C2 operability — verdicts remain correct, but replay evidence is harder to quote. Smallest fix (for the maintained `scripts/receipt_replay.py`, not the historical runners): print a final one-line summary naming failed surface ids, e.g. `summary: rejected=[ds4cc-primary] accepted=11/12`, so the last line alone evidences the verdict.

Per-case runner output (the mutated `ds4cc-primary` surface's exact `problems` from the runner's JSON):

| case | exit | traceback | problems |
|---|---|---|---|
| method-get-lowercase | 1 | false | `fetch url/method does not match population GET` |
| method-head | 1 | false | `fetch url/method does not match population GET` |
| url-trailing-slash-diff | 1 | false | `fetch url/method does not match population GET`, `fetch finalUrl differs from redirect chain` |
| url-as-list | 1 | false | `fetch url/method does not match population GET`, `fetch finalUrl differs from redirect chain` |
| finalurl-missing | 1 | false | `fetch finalUrl differs from redirect chain`, `audit.json {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}} != reproduced {'exit': 2, 'result': {'findings': [{'id': 'input_invalid', 'page': None}], 'pagesChecked': 0, 'verdict': 'could-not-evaluate'}}` |
| finalurl-int | 1 | false | same as finalurl-missing (reproduced `input_invalid`/`could-not-evaluate`) |
| redirects-as-dict | 1 | false | `fetch redirect chain missing or too long` |
| redirects-as-hop-dict | 1 | false | `fetch redirect chain missing or too long` |
| finalurl-trailing-slash-diff | 1 | false | `fetch finalUrl differs from redirect chain` |
| extra-member-note (control) | 0 | false | none — 12/12 accepted |

Note for the maintained script's authors: `scripts/canonical_audit.py` already treats a missing or non-string manifest `url` as a clean `input_invalid` finding (exit 2, no crash), so `finalUrl` type errors are caught by the audit-reproduction mismatch — `receipt_replay.py` should still check the type directly so rejection does not depend on the reproduction path.

```json
[
 {"id": "method-get-lowercase", "target": "c2", "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json", "op": "set", "jsonPath": ["method"], "value": "get", "expect": "reject", "why": "The contract documents fetch.json must record a GET and RFC 9110 §9.1 makes method tokens case-sensitive, so \"get\" is a different token that documents no GET observation.", "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}},
 {"id": "method-head", "target": "c2", "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json", "op": "set", "jsonPath": ["method"], "value": "HEAD", "expect": "reject", "why": "The contract requires a GET receipt and RFC 9110 §9.3.2 defines HEAD as carrying no response body content, which could not support the stored page.html sha256.", "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}},
 {"id": "url-trailing-slash-diff", "target": "c2", "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json", "op": "set", "jsonPath": ["url"], "value": "https://ds4cc.com", "expect": "reject", "why": "The contract requires the receipt to name the population url and RFC 3986 §6.2.3 slash normalization is not part of the contract, so the receipt must record the requested target byte-exactly.", "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}},
 {"id": "url-as-list", "target": "c2", "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json", "op": "set", "jsonPath": ["url"], "value": ["https://ds4cc.com/"], "expect": "reject", "why": "Per RFC 8259 the url is a JSON string member of the receipt and an array is a different JSON value type that names no resource.", "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}},
 {"id": "finalurl-missing", "target": "c2", "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json", "op": "delete", "jsonPath": ["finalUrl"], "value": null, "expect": "reject", "why": "The contract derives the validator manifest url from fetch.finalUrl and requires it to equal the redirect-chain end, so an absent finalUrl makes every replay input_invalid.", "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}},
 {"id": "finalurl-int", "target": "c2", "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json", "op": "set", "jsonPath": ["finalUrl"], "value": 42, "expect": "reject", "why": "RFC 8259 makes 42 a number where the contract requires a string naming the final resource, and the reproduced audit can never match input_invalid.", "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}},
 {"id": "redirects-as-dict", "target": "c2", "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json", "op": "set", "jsonPath": ["redirects"], "value": {}, "expect": "reject", "why": "The contract requires the redirect chain as a JSON array and RFC 8259 §5 keeps objects and arrays distinct types.", "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}},
 {"id": "redirects-as-hop-dict", "target": "c2", "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json", "op": "set", "jsonPath": ["redirects"], "value": {"from": "https://ds4cc.com", "status": 301, "to": "https://ds4cc.com/"}, "expect": "reject", "why": "A correctly shaped hop is still malformed as an object where the contract's array is required (RFC 8259 §5), pinning the check as type-based rather than content-based.", "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}},
 {"id": "finalurl-trailing-slash-diff", "target": "c2", "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json", "op": "set", "jsonPath": ["finalUrl"], "value": "https://ds4cc.com", "expect": "reject", "why": "With an empty chain the chain end is the requested url byte-exactly, so a slash-differing finalUrl contradicts the receipt's own redirect record.", "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}},
 {"id": "extra-member-note", "target": "c2", "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json", "op": "set", "jsonPath": ["note"], "value": "r24 probe", "expect": "accept", "why": "RFC 8259 objects are unordered name/value sets and the contract forbids no extra members, so an unknown member must not flip the verdict — control against an over-strict maintained script.", "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}}
]
```

## Checked and held

- Baseline unmodified clone at f7de3ab: `measure_c2.py --root <clone> --revision f7de3ab…` → exit 0, `12 / 12` accepted; stderr empty.
- All 10 cases applied to committed receipts (mutation + `git add` + commit at fixed dates), runner run at each probe HEAD: `6a9ef95`, `487fd9b`, `c4dc99c`, `2c069e9`, `16cadc1`, `2e86f95`, `41b35e4`, `2e8bb37`, `af30563`, `255ca93` — exits 1,1,1,1,1,1,1,1,1,0 respectively; `Traceback` absent from stderr in all 10; runner itself never crashed on this axis.
- Probe bytes verified: `git show 487fd9b:.ufo/waves/round-23/live/ds4cc-primary/fetch.json` yields `"method": "HEAD"`.
- Coverage of the assigned focus: method `get`/`HEAD`; trailing-slash difference on both `url` and `finalUrl`; `url` as list; `finalUrl` missing/int; `redirects` as dict (empty and hop-shaped).
- RFC grounding: RFC 9110 §9.1 (case-sensitive method tokens), §9.3.2 (HEAD body semantics); RFC 3986 §6.2.3 (slash normalization not contractual); RFC 8259 §4/§5 (string/number/array/object distinctions). RFC 3339 §5.6 not engaged by this axis (date fields are a sibling's scope).
- No tool installs or upgrades were needed or made (python3 3.14.8, git 2.56.0 already present; pacman untouched).

## Limits

- Structural replay only, per the contract's own limit: no network re-observation; a self-consistent fabricated redirect chain with a matching stored audit would still pass (residual risk owned by the contract, not a defect).
- `url`/`finalUrl` grammar is enforced only by equality; a string-typed non-URL value equal to a fabricated hop `to` passes chain checks and is caught only when the audit reproduction diverges — recommend the maintained script add a cheap RFC 3986 absolute-URI check.
- Single-surface mutation per case (`ds4cc-primary`, served/200): the runner fails globally on any malformed surface and the url/method checks run before `served()`, so not-served surfaces exercise identical code paths for these fields.
- `r23Observed.stdoutTail` is the literal last stdout line (`}`); discriminating strings are in the findings table and `/tmp/kake-r24-GapC2UrlMethod-k9HT/results.json`.
- Leaf member: no subagents spawned; lane untouched except this report file.
