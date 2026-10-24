## Verdict

`datetime.fromisoformat()` alone is **not a sufficient RFC 3339 date-time validator**. Python 3.11+ intentionally accepts ISO 8601 forms outside RFC 3339's date-time grammar (including date-only, basic-format, and week-date forms, and a naive date-time without its required offset). It also rejects some RFC 3339 forms, including its documented leap-second example and lowercase `z`. For the round-24 C2 operability claim, use a strict RFC 3339 syntax/profile check and calendar/clock/offset checks; `fromisoformat()` can be a value parser after the syntax gate, not the gate itself.

## Findings

### P1 — `fromisoformat` acceptance is broader than RFC 3339

**Sources and located quotes** (accessed 2026-10-21):

- Python docs: <https://docs.python.org/3/library/datetime.html> — the unversioned page title showed **Python 3.15.0 documentation**; HTTP `Date` observed `Wed, 21 Oct 2026 11:44:29 GMT`. The pinned <https://docs.python.org/3.11/library/datetime.html> title showed **Python 3.11.17 documentation**.
- `date.fromisoformat` examples, 3.11 docs: `date.fromisoformat('20191204')` (basic date) and `date.fromisoformat('2021-W01-1')` (week date). Both are shown as examples returning dates.
- `datetime.fromisoformat` examples, 3.11 docs: `datetime.fromisoformat('20111104T000523')` (basic date-time), `datetime.fromisoformat('2011-W01-2T00:05:23.283')` (week date), and `datetime.fromisoformat('2011-11-04 00:05:23.283')` (space separator).
- Quote (datetime.fromisoformat): “The `T` separator may be replaced by any single unicode character.” (11 words.) Thus the date/time separator is not simply optional; Python accepts a different single character.
- Quote (datetime.fromisoformat): “Changed in version 3.11: Previously, this method only supported formats that could be emitted by `date.isoformat()` or `datetime.isoformat()`.” (19 words.)
- Quote (date.fromisoformat): “Reduced precision dates are not currently supported (`YYYY-MM`, `YYYY`).” (9 words.) The docs also list extended dates and ordinal dates as exceptions.

**Required local check:** exact command run:

```sh
python3 --version; python3 -c 'import datetime as dt
def r(f, s):
    try:
        return repr(f(s))
    except Exception as e:
        return type(e).__name__ + ": " + str(e)
for s in ["20261021", "2026-W43-3", "2026-10-21T12:00", "2026-10-21 12:00:00+00:00"]:
    print(repr(s))
    print("  datetime.fromisoformat ->", r(dt.datetime.fromisoformat, s))
    print("  date.fromisoformat     ->", r(dt.date.fromisoformat, s))
'
```

Exact output:

```text
Python 3.14.8
'20261021'
  datetime.fromisoformat -> datetime.datetime(2026, 10, 21, 0, 0)
  date.fromisoformat     -> datetime.date(2026, 10, 21)
'2026-W43-3'
  datetime.fromisoformat -> datetime.datetime(2026, 10, 21, 0, 0)
  date.fromisoformat     -> datetime.date(2026, 10, 21)
'2026-10-21T12:00'
  datetime.fromisoformat -> datetime.datetime(2026, 10, 21, 12, 0)
  date.fromisoformat     -> ValueError: Invalid isoformat string: '2026-10-21T12:00'
'2026-10-21 12:00:00+00:00'
  datetime.fromisoformat -> datetime.datetime(2026, 10, 21, 12, 0, tzinfo=datetime.timezone.utc)
  date.fromisoformat     -> ValueError: Invalid isoformat string: '2026-10-21 12:00:00+00:00'
```

The first three `datetime` results are not RFC 3339 `date-time` values: §5.6 defines `date-time = full-date "T" full-time`, and `full-time = partial-time time-offset`. The third input is also naive (no offset). The fourth is parsed as aware; RFC 3339 §5.6's note allows an application to choose a space separator for readability, so it is not the decisive counterexample. (It is not the literal ABNF `T` form.)

Additional exact probes with `python3` 3.14.8: `datetime.fromisoformat('2026-10-21x12:34:56Z')` succeeds; `'2026-10-21T12:34:56,5Z'`, `'2026-10-21T12:34:56+0530'`, and `'2026-10-21T12:34:56+05:30:15'` also succeed. Those forms do not match RFC 3339 §5.6's literal date-time structure, decimal point, or `±HH:MM` offset grammar. The parser also accepts a date-only string as midnight.

**Impact:** C2 / operability. A replay validator that uses `fromisoformat()` as its sole format check can accept malformed/non-profile receipt timestamps, so parser success alone cannot satisfy “rejects every frozen malformed case.”

**Smallest fix:** require a full-string RFC 3339 profile match before parsing; validate real calendar values, clock and offset ranges, the required offset on date-times, and the round's cutoff/future bound. Catch both `TypeError` and `ValueError` at the replay boundary. The RFC Editor source is <https://www.rfc-editor.org/rfc/rfc3339>; §5.6 requires an offset in `full-time`, while its note says applications may choose a space separator. Do not reject the fourth probe solely for its space without resolving that application choice.

### P2 — Python also does not preserve or accept every RFC 3339 case

RFC 3339 §5.8 itself gives `1990-12-31T23:59:60Z` and says “This represents the leap second inserted at the end of 1990.” Python 3.14.8 `datetime.fromisoformat()` raises `ValueError: second must be in 0..59, not 60` for it. RFC 3339 §5.6 also says `T`/`Z` may be lowercase: Python accepts `2026-10-21t12:34:56Z`, but raises `ValueError: Invalid isoformat string: '2026-10-21T12:34:56z'` for lowercase `z`. Conversely, Python maps `-00:00` to `datetime.timezone.utc`, losing RFC 3339 §4.3's distinction between unknown local offset (`-00:00`) and `Z`/`+00:00`; a nine-digit fractional second is accepted but stored only to six-digit microsecond precision (`123456`).

**Impact:** C2 / operability if receipts need general RFC 3339 interoperability or exact input semantics; less material for timestamps produced exclusively by `date -u` at whole-second precision.

**Smallest fix:** decide and document the receipt profile for leap seconds, lowercase markers, `-00:00`, and fractional precision. Preserve the original string/precision or reject unsupported semantic cases explicitly rather than treating parse success as full RFC 3339 equivalence.

## Checked and held

- Direct checks: `python3 --version` → `Python 3.14.8`; the four requested values above were run with `python3 -c` and exact outputs are recorded above.
- Ran the documented date/datetime examples with Python 3.11.17, 3.14.8, and 3.15.0; every example matched the documentation's expected value. Ran a broader scratch probe against Python 3.11.17, 3.12.15, 3.13.16, 3.14.8, and 3.15.0; the results relevant above were consistent across 3.11+.
- Installed CPython 3.10.22 and 3.15.0 with `uv python install 3.10 3.15` (uv 0.13.0; uv-managed interpreter channel), solely to compare the pre-3.11 boundary and current docs version. Python 3.10.22 rejects the basic/week-date and trailing-`Z` examples that succeed on 3.11+; no lane files were changed except this report.
- RFC 3339 §5.6 quotes referenced above: `full-time = partial-time time-offset`; `date-time = full-date "T" full-time`. Its note says “Applications using this syntax may choose, for the sake of readability, to specify a full-date and full-time separated by (say) a space character.” (23 words.) RFC §5.6 also permits lowercase `t`/`z`; §4.3 gives `-00:00` its unknown-local-offset meaning.
- No Python packages or lane production files were installed/edited. Scratch probes were kept under `/tmp/kake-r24-SourcePythonDatetime-YUhR`.

## Limits

The RFC 3339 examples and grammar establish the distinction needed here; this was not an exhaustive RFC conformance suite. The Python docs' unversioned URL is rolling and displayed 3.15.0 at access time; Python 3.11.17's version-pinned page was also read. No receipt replay runner or lane acceptance counter was executed or changed by this source-scoping assignment.