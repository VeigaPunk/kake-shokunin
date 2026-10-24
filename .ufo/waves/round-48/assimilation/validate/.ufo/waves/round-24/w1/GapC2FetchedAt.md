## Verdict

C2 `fetchedAt` audit complete. The frozen round-23 replay accepts all eight malformed/future/impossible/offset-less strings on both a served and a not-served surface (exit 0, 12/12 accepted). It rejects the four JSON non-string values cleanly (exit 1, 11/12 accepted, no traceback). This is author-side evidence only, not an independent admission. No lane production files were changed.

## Findings

### P2 — Round-23 C2 replay accepts invalid `fetchedAt` strings

**Impacted claim/axis:** C2 / operability. `measure_c2.py` line 56 checks only that `fetchedAt` is a string and that its first ten characters are not lexically before `2026-10-21`. That accepts trailing garbage, a 2099 instant, an impossible November date, and a local timestamp without an offset. The same bypass applies before the not-served branch, so neither response class is protected.

**Exact command:** each listed run used:

`python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2FetchedAt-clone --revision <revision>`

The revision column supplies the literal value substituted for `<revision>`. The reported target-surface row is the exact parsed JSON value from the runner's `surfaces` array; `stdoutTail` is the exact last stdout line. All runs had empty stderr.

| Case | Revision | Mutated `fetchedAt` | Exact target-surface row | Exit; accepted/total; traceback; stdout tail |
|---|---|---|---|---|
| served-malformed | `41139e4d3cbd5fed0831c402e128f0867cea865b` | `"2026-10-21T06:33:03Z trailing"` | `{"id":"ds4cc-primary","pass":true,"problems":[],"verdict":"clean"}` | `0; 12/12; false; "}"` |
| served-future | `9b38b8ba24f8286b5524ad1e88605df01bcfa473` | `"2099-12-31T23:59:59Z"` | `{"id":"ds4cc-primary","pass":true,"problems":[],"verdict":"clean"}` | `0; 12/12; false; "}"` |
| served-impossible | `84a880bd0213a0cc795a523d4745140aeabfba23` | `"2026-11-31T06:33:03Z"` | `{"id":"ds4cc-primary","pass":true,"problems":[],"verdict":"clean"}` | `0; 12/12; false; "}"` |
| served-offsetless | `72c45531a5c1d4dfae925f4a7554311bdfa40ef5` | `"2026-10-21T06:33:03"` | `{"id":"ds4cc-primary","pass":true,"problems":[],"verdict":"clean"}` | `0; 12/12; false; "}"` |
| not-served-malformed | `bc895438224bf8e94cc6b972c50a836735d51b6c` | `"2026-10-21T06:33:17Z trailing"` | `{"id":"lucario-kimi","pass":true,"problems":[],"verdict":"not-served"}` | `0; 12/12; false; "}"` |
| not-served-future | `1fc916e6d9c60989b5063d7b6c77fdbf76406a97` | `"2099-12-31T23:59:59Z"` | `{"id":"lucario-kimi","pass":true,"problems":[],"verdict":"not-served"}` | `0; 12/12; false; "}"` |
| not-served-impossible | `b13c6c852e5109632a963bdbdb7b60501cb64f88` | `"2026-11-31T06:33:17Z"` | `{"id":"lucario-kimi","pass":true,"problems":[],"verdict":"not-served"}` | `0; 12/12; false; "}"` |
| not-served-offsetless | `b3879cf0beb72e6ea154b745dcab27d79fa42c44` | `"2026-10-21T06:33:17"` | `{"id":"lucario-kimi","pass":true,"problems":[],"verdict":"not-served"}` | `0; 12/12; false; "}"` |
| served-null | `5b7a34e255e8744da98099dc0c6c64846974bfa5` | `null` | `{"id":"ds4cc-primary","pass":false,"problems":["fetchedAt missing or before 2026-10-21"],"verdict":"clean"}` | `1; 11/12; false; "}"` |
| served-number | `a6e746cc9623d08a9ccd4319cf7093dc8c4a7de7` | `7` | `{"id":"ds4cc-primary","pass":false,"problems":["fetchedAt missing or before 2026-10-21"],"verdict":"clean"}` | `1; 11/12; false; "}"` |
| not-served-array | `7b5e9c1947291286bcb9f990ac1324783cd7da53` | `[]` | `{"id":"lucario-kimi","pass":false,"problems":["fetchedAt missing or before 2026-10-21"],"verdict":"not-served"}` | `1; 11/12; false; "}"` |
| not-served-object | `622984d9c0cf128a1e0a47a2ec151ba76622c7bc` | `{}` | `{"id":"lucario-kimi","pass":false,"problems":["fetchedAt missing or before 2026-10-21"],"verdict":"not-served"}` | `1; 11/12; false; "}"` |

**Smallest fix:** replace the prefix comparison with strict type and complete RFC 3339 date-time validation (including calendar/time/offset ranges), then reject event timestamps later than the replay observation time. Keep the existing non-string guard. RFC 3339 §5.6 requires a full date, `T`, full time and a time offset; §5.7 bounds day-of-month. RFC 8259 §3 permits `null`, numbers, arrays and objects as JSON values, but none is a timestamp string. The two fixture classes were checked against the runner's `served()` rule; both carry `Content-Type: text/html; charset=utf-8`, whose media type is `text/html` before its parameter under RFC 9110 §8.3.1.

**C2 malformed-case array (all 12 cases were applied, committed and run):**

```json
[
  {"id":"served-malformed","target":"c2","file":".ufo/waves/round-23/live/ds4cc-primary/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":"2026-10-21T06:33:03Z trailing","expect":"reject","why":"RFC 3339 §5.6 defines the date-time grammar; trailing text is not a fetchedAt timestamp.","r23Observed":{"exit":0,"traceback":false,"stdoutTail":"}"}},
  {"id":"served-future","target":"c2","file":".ufo/waves/round-23/live/ds4cc-primary/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":"2099-12-31T23:59:59Z","expect":"reject","why":"This valid RFC 3339 instant is after the completed 2026-10-21 GET, so it cannot truthfully attest that fetch event (§5.6 represents a date-time as an instant).","r23Observed":{"exit":0,"traceback":false,"stdoutTail":"}"}},
  {"id":"served-impossible","target":"c2","file":".ufo/waves/round-23/live/ds4cc-primary/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":"2026-11-31T06:33:03Z","expect":"reject","why":"RFC 3339 §5.7 caps November at day 30, so this impossible calendar date is not a timestamp.","r23Observed":{"exit":0,"traceback":false,"stdoutTail":"}"}},
  {"id":"served-offsetless","target":"c2","file":".ufo/waves/round-23/live/ds4cc-primary/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":"2026-10-21T06:33:03","expect":"reject","why":"RFC 3339 §5.6 requires full-time to include a time-offset, so this offset-less value is not a complete timestamp.","r23Observed":{"exit":0,"traceback":false,"stdoutTail":"}"}},
  {"id":"not-served-malformed","target":"c2","file":".ufo/waves/round-23/live/lucario-kimi/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":"2026-10-21T06:33:17Z trailing","expect":"reject","why":"RFC 3339 §5.6 defines the date-time grammar; trailing text is not a fetchedAt timestamp.","r23Observed":{"exit":0,"traceback":false,"stdoutTail":"}"}},
  {"id":"not-served-future","target":"c2","file":".ufo/waves/round-23/live/lucario-kimi/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":"2099-12-31T23:59:59Z","expect":"reject","why":"This valid RFC 3339 instant is after the completed 2026-10-21 GET, so it cannot truthfully attest that fetch event (§5.6 represents a date-time as an instant).","r23Observed":{"exit":0,"traceback":false,"stdoutTail":"}"}},
  {"id":"not-served-impossible","target":"c2","file":".ufo/waves/round-23/live/lucario-kimi/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":"2026-11-31T06:33:17Z","expect":"reject","why":"RFC 3339 §5.7 caps November at day 30, so this impossible calendar date is not a timestamp.","r23Observed":{"exit":0,"traceback":false,"stdoutTail":"}"}},
  {"id":"not-served-offsetless","target":"c2","file":".ufo/waves/round-23/live/lucario-kimi/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":"2026-10-21T06:33:17","expect":"reject","why":"RFC 3339 §5.6 requires full-time to include a time-offset, so this offset-less value is not a complete timestamp.","r23Observed":{"exit":0,"traceback":false,"stdoutTail":"}"}},
  {"id":"served-null","target":"c2","file":".ufo/waves/round-23/live/ds4cc-primary/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":null,"expect":"reject","why":"The receipt contract requires fetchedAt to be a timestamp string; RFC 8259 §3 permits null as a JSON value, but it is not that string.","r23Observed":{"exit":1,"traceback":false,"stdoutTail":"}"}},
  {"id":"served-number","target":"c2","file":".ufo/waves/round-23/live/ds4cc-primary/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":7,"expect":"reject","why":"The receipt contract requires fetchedAt to be a timestamp string; RFC 8259 §3 permits numbers as JSON values, but a number is not that string.","r23Observed":{"exit":1,"traceback":false,"stdoutTail":"}"}},
  {"id":"not-served-array","target":"c2","file":".ufo/waves/round-23/live/lucario-kimi/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":[],"expect":"reject","why":"The receipt contract requires fetchedAt to be a timestamp string; RFC 8259 §3 permits arrays as JSON values, but an array is not that string.","r23Observed":{"exit":1,"traceback":false,"stdoutTail":"}"}},
  {"id":"not-served-object","target":"c2","file":".ufo/waves/round-23/live/lucario-kimi/fetch.json","op":"set","jsonPath":["fetchedAt"],"value":{},"expect":"reject","why":"The receipt contract requires fetchedAt to be a timestamp string; RFC 8259 §3 permits objects as JSON values, but an object is not that string.","r23Observed":{"exit":1,"traceback":false,"stdoutTail":"}"}}
]
```

## Checked and held

- Read the frozen contract at `.ufo/waves/round-24/contract.json`; base: `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. At clone creation, `git rev-parse HEAD` returned exactly that base.
- Clone: `/tmp/kake-r24-GapC2FetchedAt-clone` (`git clone --no-hardlinks`). Each mutation was committed separately with `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` set to `2026-10-21T12:00:00Z`; the table records all 12 resulting revisions. Every run used the literal command above and the round-23 runner in the lane; its bytes matched the base clone copy (SHA-256 `91134d27af6c48f8e8bd6e604e533396f6d9c3542d1285ec1e3901f6358e5653`).
- Baseline served surface: `ds4cc-primary`, status `200`, `text/html; charset=utf-8`, original fetchedAt `2026-10-21T06:33:03Z`. Baseline not-served surface: `lucario-kimi`, status `404`, `text/html; charset=utf-8`, original fetchedAt `2026-10-21T06:33:17Z`, matching `not-served` audit and no stored `page.html`.
- Read RFC Editor texts: RFC 3339 §§5.6–5.7, RFC 9110 §8.3.1 and RFC 8259 §3. No external requests to the sites were made. No tool was installed or updated.
- Non-string results are already safe in round 23: all four produced the ordinary `fetchedAt missing or before 2026-10-21` problem, without traceback. The timestamp strings are the failing behavior: each resulted in a clean/not-served pass and exit 0.

## Limits

- Round-23 `measure_c2.py` documents only `fetchedAt >= 2026-10-21`; it does not state an upper bound. The future cases are marked `reject` under the round-24 C2 contract's explicit future-timestamp gap and the event-time meaning of `fetchedAt`, not because RFC 3339 syntax itself disallows future instants. The maintained replay contract should make its reference observation time/upper-bound rule explicit.
- The live round-24 worktree did not contain `.ufo/waves/round-24/c2-population.json` when checked, so this report carries the complete 12-case array and observations for L1 to integrate; it does not claim that array was admitted or that round-24 replay passes.
- These are committed synthetic receipt mutations against the frozen round-23 evidence. They do not authenticate live network behavior or establish any publishing/deployment state.
