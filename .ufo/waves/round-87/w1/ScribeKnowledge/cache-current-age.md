source: S462 — RFC 9111 HTTP Caching, §4.2.3 “Calculating Age” — https://httpwg.org/specs/rfc9111.html#age.calculations. Independently opened by ScribeKnowledge with the URL reader this round; source access was not delegated. This new source identity covers conservative current-age arithmetic only; S461 retains its existing duplicate/directive/lifetime scope unchanged.
verified-at: 2026-11-04 — own URL-reader access returned RFC 9111 text, then the complete §4.2.3 was read in the returned artifact, lines 291–345. Own access is source evidence, not calculator execution evidence. No HTTP status, raw-byte fingerprint, or wall-clock access time was exposed in that reader response; none is claimed.
recheck: 180d, due 2027-05-03, or earlier if source text or the adapter contract changes. Concrete GET-only stdlib command below reopens the same source and prints the located age-calculation passage; check the six equations and MAY alternative before retaining this interpretation.
ground: freshness — round-87 C2 bounded age arithmetic; calibration remains 2 HOLD and freshness remains 10 HOLD pending canonical gates.
scope: Integer-second offline adapter for already-observed Date, optional Age, and local request/response/current timestamps. Draft for L1 integration; not production or acceptance evidence.

# Conservative HTTP current age

## Located source and recheck

Own located quote (8 words), §4.2.3, paragraph immediately after the first three-equation block:

> The corrected_age_value MAY be used as the corrected_initial_age.

The following paragraph and equation permit a more conservative maximum when old caches might not insert Age correctly. The maximum is this adapter's selected allowed profile, **not the RFC's sole permitted algorithm**. No evidence that such old caches actually occur on a particular response path is asserted.

Run this public specification GET only when rechecking is authorized. It writes no files:

```sh
python3 -B - <<'PY'
from html.parser import HTMLParser
from urllib.request import urlopen
class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data)
with urlopen('https://httpwg.org/specs/rfc9111.html', timeout=30) as response:
    raw = response.read()
p = Text()
p.feed(raw.decode('utf-8'))
text = ' '.join(' '.join(p.parts).split())
start = text.index('Age calculation uses the following data:')
end = text.index('4.2.4.', start)
print(text[start:end])
PY
```

This is a recheck recipe, not a command executed by this seat. The specification fetch is not an owned-property trial.

## Six equations and what they mean

All terms are seconds. The adapter evaluates these sequentially:

| Output key | Equation | Interpretation |
| --- | --- | --- |
| `apparent_age` | `max(0, response_time - date_value)` | Age inferred from Date and receipt time; a future Date cannot produce a negative apparent age. Its estimate depends on reasonably synchronized origin/local clocks. |
| `response_delay` | `response_time - request_time` | Local interval for the request that produced this response. |
| `corrected_age_value` | `age_value + response_delay` | Received Age, or zero when unavailable, corrected relative to request initiation, not merely response receipt. |
| `corrected_initial_age` | `max(apparent_age, corrected_age_value)` | Select the conservative estimate at receipt; do not add the two independent estimates. |
| `resident_time` | `now - response_time` | Time since this implementation received the stored response. |
| `current_age` | `corrected_initial_age + resident_time` | Conservative age at the supplied current timestamp. |

The RFC also permits `corrected_initial_age = corrected_age_value`; its independent corrected-Age estimate assumes caches along the path implement HTTP/1.1 or greater. The offline tool deliberately always retains the maximum. It does not detect protocol versions or switch profiles.

## Input and output adapter

The planned entry point is `scripts/cache_current_age.py` at absolute path `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py`. Supply one JSON object on stdin:

- Required: `date_value`, `request_time`, `response_time`, `now`.
- Optional: `age_value`, default `0` when omitted.
- Each supplied value must be an integer, **not a boolean**, float, string, or null. All timestamps use the same epoch and integer-second unit. `date_value` may be negative; all other values must be nonnegative.
- Require `request_time <= response_time <= now`.
- Valid input exits 0 and emits only one JSON object with all six output keys and exact integer values. Missing required keys, wrong types, negative Age/local timestamps, or inverted local time exit 1 with a stderr diagnostic. Unknown keys may be rejected; callers should omit them.

Converting observed HTTP Date text into epoch seconds is upstream adapter work, **not an implemented Date parser in this tool**. Age is a duration, not an epoch timestamp. Keep original observation provenance; do not substitute Date for an unobserved request time, or invent zero-duration timing and call it observed. The tool does not read a clock or perform network requests.

Python arbitrary-precision integer arithmetic is the local convention: no fixed-width saturation is needed for arithmetic that does not overflow. For example, `2147483648 + 2147483648` remains `4294967296`. This is not a claim that every HTTP cache must use arbitrary precision or that RFC overflow handling has been removed; it does not change S461's separate capped adapter profile. Runtime input/resource limits are not an assurance of unbounded-size acceptance.

Missing Date is unsupported by this adapter. Do not synthesize a date or downgrade missing Date into Age-only success. Missing request/response/current times also prevent evaluation. This limitation is not a general RFC prohibition against processing responses without Date.

## Decision table

| Input situation | Adapter action / expected result | Boundary |
| --- | --- | --- |
| Date 80; request 90; response 100; now 130; Age 5 | apparent 20; delay 10; corrected Age 15; initial 20; resident 30; current 50 | Date estimate dominates; not Age-only. |
| Date 100; request 95; response 100; now 140; Age 5 | apparent 0; delay 5; corrected Age 10; initial 10; resident 40; current 50 | Both transit and residence count. |
| Date 110; request/response/now 100; Age omitted | All six terms zero | Clamp negative apparent age only; this is not permission to clamp inverted local times. |
| Date -20; request/response 0; now 10; Age omitted | apparent/initial 20; resident 10; current 30 | Negative Date epoch is valid. |
| Date/request/response 0; now 2147483648; Age 2147483648 | current 4294967296 | No unconditional 2^31 cap in this profile. |
| Date missing, or any required local time missing | Exit 1, stderr diagnostic | Could not evaluate; no fabricated timing. |
| Boolean, fractional, string, or null numeric input | Exit 1, stderr diagnostic | Python bool is not an accepted integer here. |
| Negative Age/local timestamp or inverted local-time order | Exit 1, stderr diagnostic | Do not turn invalid timing into a valid age by clamping. |

These are contract-derived expectations, not results executed by this seat.

## Error patterns to reject

- Returning Age alone: omits response delay, apparent-age dominance, and residence.
- Returning only `now - Date`: ignores received Age and request-delay correction.
- Adding apparent age to corrected Age: double-counts independent estimates instead of taking their maximum.
- Calling the conservative max a universal RFC MUST, or calling the RFC MAY alternative nonconforming.
- Accepting `true`/`false` because Python treats bool as an int subclass.
- Defaulting missing Date or observation times to zero/current time and labeling them observed.
- Saturating all results at 2147483648, or using float arithmetic that loses integer precision.
- Concluding that age 0 proves cacheability, freshness, or reuse permission.

## Runnable checklist for integration

L1 owns integration and execution. The following offline commands are proposed checks, **not an execution receipt**; run only after the candidate tool is integrated at the path shown.

1. Check all six terms on a Date-dominant fixture:

```sh
printf '%s\n' '{"date_value":80,"request_time":90,"response_time":100,"now":130,"age_value":5}' | python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py
```

Expected exit 0; JSON whitespace/order immaterial:

```json
{"apparent_age":20,"response_delay":10,"corrected_age_value":15,"corrected_initial_age":20,"resident_time":30,"current_age":50}
```

2. Check Age omission and delay/residence using valid input:

```sh
printf '%s\n' '{"date_value":60,"request_time":45,"response_time":60,"now":75}' | python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py
```

Expected exit 0; apparent 0, delay 15, corrected Age 15, initial 15, resident 15, current 30.

3. Check unsupported missing Date (not Age-only success):

```sh
printf '%s\n' '{"request_time":0,"response_time":1,"now":2}' | python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py
```

Expected exit 1 and stderr diagnostic.

4. Check bool rejection and inverted-clock rejection separately:

```sh
printf '%s\n' '{"date_value":false,"request_time":0,"response_time":1,"now":2}' | python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py
printf '%s\n' '{"date_value":0,"request_time":2,"response_time":1,"now":3}' | python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py
```

Each invocation must exit 1 with a diagnostic; inspect exits separately rather than relying on the last shell status alone.

The frozen counter separately expects 17/17 case exits and complete JSON equality for all twelve valid cases. This document neither runs that counter nor proves the finite target. Separate independent sequential implementation, production selftests, and the actual owned-property GET trial remain their respective seats' evidence, not this source-access receipt.

## No caching-reuse verdict

The output is age arithmetic only. It does not calculate freshness lifetime, compare lifetime against age, interpret Cache-Control, approve storage/reuse, implement Vary/validation, model browsers, or prove full RFC compliance. Missing Date on an actual property trial means could-not-evaluate here, not a fabricated success. Neither this entry nor a successful calculator run resolves retained operator questions, outside admission, or S461's distinct scope.
