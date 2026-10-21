# S032 freshness recheck — RFC 3339

```json
{"id":"S032","verdict":"HOLD","fetchIndex":1,"quote":"full-time = partial-time time-offset date-time = full-date \"T\" full-time","anchorObserved":"RFC 3339 §5.6 Internet Date/Time Format, ABNF block (pp. 7–8); §5.7 Restrictions (pp. 8–9); July 2002 masthead","reason":"Re-fetched 2026-10-21 bytes still define date-time as full-date \"T\" full-time, with full-time requiring a time-offset (\"Z\" or numeric), and §5.7 still bounds date-mday by month/year and permits second 60 only for leap seconds, so lexical grammar alone cannot enforce real calendar rules; scope and anchor unchanged.","correction":null}
```

- Fetch #1, https://www.rfc-editor.org/rfc/rfc3339.txt, status 200, 35064 bytes, sha256 9ab2b886…700a, ETag W/"497904d3f8d7902fe014956f95fe59f6"; manifest row S032/index 1.
- Anchor present verbatim: "5.7. Restrictions", "July 2002", "Standards Track"; §5.6 grammar block intact including time-offset and date-time productions.
- Second teaches clause ("real calendar restrictions are not validated by lexical prefix comparisons") is a synthesis: §5.6 gives `date-mday = 2DIGIT` with a month/year note and §5.7 supplies the month/leap table; RFC text itself does not use "lexical prefix", so HOLD rests on those two sections, not a verbatim sentence.
- RFC 3339 is frozen (2002 Standards Track); no content drift observed, no version/date pin mismatch. No tools installed.
