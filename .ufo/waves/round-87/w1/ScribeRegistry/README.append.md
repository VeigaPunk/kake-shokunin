
## Coverage — round 87: current-age arithmetic

| Area | Entry | Bounded held ground |
|---|---|---|
| Conservative current-age arithmetic | `knowledge/cache-current-age.md` (S462); `scripts/cache_current_age.py` | Offline RFC 9111 §4.2.3 six-term arithmetic over caller-supplied integer epoch seconds: apparent age, response delay, corrected Age value, conservative corrected initial age, resident time and current age; absent Age defaults to zero. Invalid inputs fail rather than inventing a Date or request timing. |

This supersedes only the round-86 frontier sentence's Age-arithmetic slice.
The conservative maximum is an allowed profile, not the RFC's only algorithm;
integer epoch inputs and arbitrary precision are local adapter conventions.
General policy equivalence, the independent changed-row oracle, full HTTP
extraction, Vary/Pragma, storage/reuse authorization, browser/runtime cache
behavior and live property repair remain frontier. A calculated age is not a
freshness or reuse verdict. `.ufo/waves/round-87/age-cases.json` is a fixed
seventeen-case oracle, not proof of universal coverage or a run receipt.
