# Independent source access — ScribeRegistry

Access date: 2026-11-04.
Exact requested and reader-reported URL:
https://httpwg.org/specs/rfc9111.html#age.calculations

Operation: functions.read(path=the URL). Outcome: returned RFC 9111 reader text,
Content-Type text/html, Method native. Follow-on bounded read:
functions.read(path="artifact://108390:295-375"). This displayed §4.2.3's
age_value definition, both corrected-initial-age alternatives, and all equations.
No shell exit status applies to either reader operation. No HTTP status, raw
response byte length, response digest or timestamp finer than the access date
was exposed by these reader results; none is claimed here.

Located quote, §4.2.3 paragraph immediately after the first equation block:
> The corrected_age_value MAY be used as the corrected_initial_age.

Quote length: 8 whitespace-separated words.

Observed equation blocks (excerpt, not a raw-body retention):

```text
apparent_age = max(0, response_time - date_value);
response_delay = response_time - request_time;
corrected_age_value = age_value + response_delay;
corrected_initial_age = max(apparent_age, corrected_age_value);
resident_time = now - response_time;
current_age = corrected_initial_age + resident_time;
```

The max equation follows the source's more-conservative alternative discussion;
it is not the sole RFC-permitted path. The age_value definition says zero if
not available. Integer epoch JSON inputs, rejection rules and Python arbitrary
precision are local contract choices, not requirements newly established by
this source.

Identifier check before drafting the row: functions.grep with pattern
`\| S462 \|`, absolute path
/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md,
gitignore=false, returned “No matches found”. This establishes the source id
was unused in the canonical registry at observation time, not a reservation
against concurrent future integration. A separate repo-wide search found
cache_current_age/cache-current-age in round-87 contract and dispatch material;
the capability name is therefore not globally unused. No existing production
registry row for it appeared in the inspected registry.
