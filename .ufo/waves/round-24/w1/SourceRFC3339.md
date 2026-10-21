# SourceRFC3339 — RFC 3339 date-time grammar for the C2 receipt validator

Seat: KakeR24.SourceRFC3339 (kake r24, wave 1, milestone r24-build, judged on operability). Leaf, no subagents. Base f7de3ab4e9f030a15a857a5a08631bd8e690f436. Only lane write: this file.

## Verdict

Source opened and pinned this round. RFC 3339 defines `date-time = full-date "T" full-time` with a **required** `time-offset`; a date-only string (`2026-10-21`) is a `full-date`, **not** an RFC 3339 `date-time`. A receipt validator must therefore reject date-only, offset-less, space-separated, out-of-range, and non-string `observedAt`/`fetchedAt` values, and must compare parsed instants — the round-23 lexical `x[:10] < "2026-10-21"` gate accepts month-13, future-2027, date-only, hour-24, space-separator, and missing-offset strings (all demonstrated below) and must be replaced in `scripts/receipt_replay.py`. The `>= 2026-10-21` and "not in the future" bounds are lane policy; RFC 3339 itself imposes no future-date restriction.

## Source

- URL: https://www.rfc-editor.org/rfc/rfc3339.txt (canonical rel link `https://www.rfc-editor.org/info/rfc3339/` in response headers)
- Access date: 2026-10-21T11:44:10Z
- HTTP: 200, `content-type: text/plain;charset=utf-8`, 35064 bytes
- sha256 of fetched plain-text bytes: `9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a`
- Exact command: `curl -fsS --retry 2 -D "$D/headers.txt" -o "$D/rfc3339.txt" -w "http_code=%{http_code} size=%{size_download}\n" https://www.rfc-editor.org/rfc/rfc3339.txt`
- Observed: `http_code=200 size=35064` / sha256 above / `2026-10-21T11:44:10Z`
- Local copy held for the round at `/tmp/kake-r24-SourceRFC3339-gV9r/rfc3339.txt` (line numbers below are into this file)

## Quotes (verbatim from fetched bytes, ≤25 words each)

**§5.6 ABNF — time-offset, full-date, full-time, date-time** (lines 415, 419–422; exact ABNF lines):

```
time-offset     = "Z" / time-numoffset
full-date       = date-fullyear "-" date-month "-" date-mday
full-time       = partial-time time-offset
date-time       = full-date "T" full-time
```

**§5.7 — date-mday by month/year** (lines 457–459):

> The grammar element date-mday represents the day number within the current month. The maximum value varies based on the month and year

(followed by the §5.7 table: January 31 … February normal 28 / leap year 29 … December 31; "Appendix C contains sample C code to determine if a year is a leap year.")

**§5.7 — leap second** (lines 480–484):

> The grammar element time-second may have the value "60" at the end of months in which a leap second occurs

> It is also possible for a leap second to be subtracted, at which times the maximum value of time-second is "58". At all other times the maximum value of time-second is "59".

**§5.6 NOTE — lowercase t/z** (lines 424–425):

> the "T" and "Z" characters in this syntax may alternatively be lower case "t" or "z" respectively.

**§5.7 — hour 24 forbidden** (lines 496–498):

> Although ISO 8601 permits the hour to be "24", this profile of ISO 8601 only allows values between "00" and "23" for the hour

**Appendix A — the "T" is mandatory in this grammar** (lines 639–640):

> ISO 8601 states that the "T" may be omitted under some circumstances. This grammar requires the "T" to avoid ambiguity.

(Appendix A is informational, but this sentence states this RFC's grammar requires the "T".)

**§5.6 NOTE — space separator is an ISO 8601 readability remark, not this grammar** (lines 436–438):

> Applications using this syntax may choose, for the sake of readability, to specify a full-date and full-time separated by (say) a space character.

**§4.3 — `-00:00` means "local offset unknown"** (lines 256–259):

> If the time in UTC is known, but the offset to local time is unknown, this can be represented with an offset of "-00:00".

## Is a date-only string an RFC 3339 `date-time`?

**No — confidence high.** `date-time` admits only `full-date "T" full-time` (§5.6, line 422), and `full-time` requires `time-offset` (line 420). `2026-10-21` matches only the intermediate `full-date` production; the document defines no interchange format consisting of a bare full-date. A grep of every `full-date` occurrence (lines 419, 437, 679) found no date-only allowance.

## What a receipt validator must accept / reject (feeds `scripts/receipt_replay.py`, claim C2)

MUST accept (per §5.6/§5.7 grammar):

- Strings of the form `date-fullyear "-" date-month "-" date-mday "T" partial-time time-offset`: 4-digit year; month 01–12; mday per §5.7 month/leap-year table; hour 00–23; minute 00–59; second 00–59, plus "60" only under the §5.7 leap-second rules (generation of ":60" SHOULD NOT happen per lines 491–494; a validator may accept it syntactically); optional `.` frac with ≥1 digit; offset `"Z"`/`"z"` or `±HH:MM` (offset minutes 00–59). Lowercase `t`/`z` are valid per the §5.6 NOTE — the maintained replay must not reject them.

MUST reject:

- Non-string values (`observedAt`/`fetchedAt` not `isinstance(str)`).
- Date-only `full-date` (e.g. `2026-10-21`) — not a `date-time`.
- Missing time-offset (`2026-10-21T12:00:00`) — `time-offset` is required.
- Space separator instead of `T` (`2026-10-21 12:00:00Z`) — the §5.6 space NOTE describes ISO 8601 usage; the ABNF requires `"T"` (Appendix A: "This grammar requires the 'T' to avoid ambiguity.").
- Hour `24`; month `00`/`13`; Feb 30; second `61`+; 1-digit fields (violating `2DIGIT`); offset `+24:00` or `+00:99`.
- `-00:00` is syntactically valid but semantically "local offset unknown" (§4.3); since the lane contract pins UTC receipt instants, the replay should reject or explicitly flag it (policy decision for the L1; recommendation: reject for receipts).
- Lane-policy bounds layered on top (NOT RFC 3339): `observedAt`/`fetchedAt` ≥ 2026-10-21 and not after the measurement instant. RFC 3339 imposes no future-date restriction. Enforce by parsing to a comparable instant (aware datetime/epoch, with a documented ":60" policy), never by string prefix.

## Findings

**F1 (P2 — known frozen gap, now source-grounded) — lexical prefix gate accepts malformed and future timestamps.**
- Exact command: `python3 -c 'cases = ["2026-13-45T23:59:60Z", "2027-01-01T00:00:00Z", "2026-10-21", "2026-10-21T12:00:00", ...] ; for c in cases: print(repr(c), "prefix<2026-10-21 ->", c[:10] < "2026-10-21", ...)'` (mirrors `.ufo/waves/round-23/measure_c1.py:55` `receipt["observedAt"][:10] < "2026-10-21"` and `measure_c2.py:56` `fetch["fetchedAt"][:10] < "2026-10-21"`)
- Exact observed output (r23 verdict = REJECT iff prefix test true):
  - `'2026-13-45T23:59:60Z' prefix<2026-10-21 -> False => r23 verdict: ACCEPT`
  - `'2027-01-01T00:00:00Z' ... -> False => ACCEPT` (future)
  - `'2026-10-21' ... -> False => ACCEPT` (date-only — not a date-time)
  - `'2026-10-21T12:00:00' ... -> False => ACCEPT` (missing time-offset)
  - `'2026-10-21T24:00:00Z' ... -> False => ACCEPT` (hour 24, §5.7-forbidden)
  - `'2026-10-21 12:00:00Z' ... -> False => ACCEPT` (space separator)
  - `'2026-10-21t12:00:00z' ... -> False => ACCEPT` (correct control — lowercase t/z is valid and must stay accepted)
  - `'2026-02-30T12:00:00Z' ... -> True => REJECT` — rejected only by accident of the cutoff (`"2026-02-30" < "2026-10-21"` lexically); the same malformation after the cutoff, `'2026-11-30T12:00:00Z'`, is ACCEPTed.
- Impacted claim/axis: C2, operability.
- Smallest fix: in the maintained `scripts/receipt_replay.py`, replace both prefix tests with strict RFC 3339 `date-time` grammar validation plus instant comparison (parse → bounds check); never compare raw prefixes.

**F2 (P3, cross-reference only — sibling seat's scope):** `.ufo/waves/round-23/measure_c2.py:37-39` `served()` does `fetch.get("contentType") or ""` then `.split(";")`; a non-string truthy `contentType` (e.g. `5`) reaches `.split` and raises AttributeError. RFC 9110 media-type grammar is another seat's sourcing task; noted here only because it was observed in the same read.

## Checked and held

- Single HTTP 200 GET of the RFC text; sha256 computed over exactly the 35064 fetched bytes; copy retained at `/tmp/kake-r24-SourceRFC3339-gV9r/rfc3339.txt`.
- Every quote verified verbatim against the fetched bytes at the cited line numbers.
- All ACCEPT/REJECT cases above actually executed with python3 (no simulated outputs). Controls `2026-10-21T12:00:00Z` and lowercase `t/z` remain accepted by the lexical test — the replacement validator must keep them accepted.
- No subagents spawned; no tool installs (curl/python3 already present, none needed); no lane files touched except this report; no git/jj commands run.

## Limits

- One fetch, one mirror (rfc-editor.org); RFC 3339 errata not consulted (out of assigned scope).
- The §5.6 space-separator NOTE is worded loosely; my ruling (reject space separator) follows the normative ABNF plus Appendix A's explicit "requires the T". A stricter reading that accepts it is arguable from the NOTE alone, but the lane contract pins "UTC RFC 3339 date-time", so rejection is the conservative correct choice.
- Leap-second acceptance (`:60`) beyond IERS-announced dates is a validator policy choice; RFC only says applications "should not generate" them (lines 491–494).
- RFC 9110 media-type grammar (contentType) deliberately not covered here; assigned to the sibling source seat.
- Unknowns: none within the assigned question.
