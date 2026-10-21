# ScribeKnowledgeReplay — kake r24 w1 (C2 operability, knowledge draft)

Scope: draft only. The appended section below is NOT written into
`corpus/knowledge/static-canonical-preflight.md`; the L1 integrator decides
placement. Author-side; no independent admission is claimed.

## Verdict

Draft section ready for L1 integration, with three findings the integrator must
resolve before it can be true: (F1) the round-23 c1 `observedAt` field is a
full-date, so a date-time-only rule would break the 17/17 controls; (F2) the
contract's C2 count path and the wave spec's CLI path disagree and the script
does not yet exist at base; (F3) exit 1 is shared by a verdict and an uncaught
Python exception, so the exit code alone cannot prove "no traceback".

## Findings

### F1 — P1 — c1 `observedAt` is full-date; date-time-only rule breaks the controls

Exact commands/outputs (read-only, against the lane HEAD):

```
$ for f in .ufo/waves/round-23/receipts/*.json; do ... print observedAt ...; done | sort | uniq -c
     14 drift-detection.json '2026-10-21'
      3 sitemap-orphan-audit.json '2026-10-21'
      1 rejected.json <class 'list'>
$ python3 -B .ufo/waves/round-23/measure_c1.py --root . --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436
{'accepted': 17, 'total': 17, 'claimVerdicts': {'HOLD': 79, 'STALE': 55, 'UNVERIFIABLE': 42}}
exit=0
```

Impacted: C2 "after" (`c1 17/17` control must stay accepted); axis operability.
Smallest fix: the replay validates per field. c1 `observedAt` accepts RFC 3339
`full-date` OR `date-time`; c2 `fetchedAt` accepts `date-time` only. Add an
`expect: accept` control for the full-date `"2026-10-21"` form.

### F2 — P2 — contract count path, wave-spec CLI path and file existence disagree

```
$ ls scripts/receipt_replay.py
ls: cannot access 'scripts/receipt_replay.py': No such file or directory
```

`contract.json` C2 `count` = `python3 .ufo/waves/round-24/measure_c2.py --root . --revision <commit>`
(that file is not present in `.ufo/waves/round-24/`). `w1-spec.json` item
ScribeKnowledgeReplay and the gap text say the maintained instrument is
`scripts/receipt_replay.py c1|c2`. Impacted: C2 count command; the CLI documented
below is the contracted interface, not an observed one.
Smallest fix: L1 reconciles `contract.json` `count` to
`python3 scripts/receipt_replay.py c2 --root . --revision <commit>` (and c1 for the
c1 population) once the script lands, and re-checks this draft's exit table
against the landed file.

### F3 — P2 — exit 1 is shared by a verdict and an uncaught exception

Function-level probe (copy of round-23 `served()`, measure_c2.py:36-39):

```
served 'text/html; charset=utf-8' -> True
served 'TEXT/HTML' -> True
served ['text/html'] -> RAISES AttributeError 'list' object has no attribute 'split'
served 5 -> RAISES AttributeError 'int' object has no attribute 'split'
$ python3 -B -c 'def served(f): return f["contentType"].split(";")[0]
served({"contentType": 5})'; echo "uncaught-exit=$?"
AttributeError: 'int' object has no attribute 'split'
uncaught-exit=1
```

Impacted: C2 "no traceback" criterion; an exit-code-only gate cannot tell a crash
from a rejection.
Smallest fix: explicit type checks for every field (no reliance on exceptions);
a top-level guard converts any unforeseen exception into exit 2 with a JSON error
object (instrument failure), keeping exit 1 reserved for a row-level verdict.
Runners treat stderr traceback or non-JSON stdout as instrument failure.

Not run: a committed sandbox mutation through `measure_c2.py` (the `r23Observed`
column of the C2 case list). That is executor work; this seat authored no cases.
The traceback claim above rests on the function-level probe only and is labelled so.

### F4 — P3 — round-24 artifacts are untracked; `--revision` cannot see them

```
$ git status --short
?? .ufo/waves/round-24/
$ git ls-files .ufo/waves/round-24 | wc -l
0
```

The round-23 replays read committed round-23 files, so they are unaffected. Any
round-24 counter that uses `--revision <commit>` (C1 population, C2 count if it
points at round-24) sees nothing until the round-24 files are committed by the L1.

### F5 — P3 — lexical-prefix predicates accept the malformed strings the contract names

```
lexical accept=True  value='2026-10-21garbage'
lexical accept=True  value='2026-13-45T99:99:99Zjunk'
lexical accept=True  value='2099-01-01T00:00:00Z'
lexical accept=True  value='zzzz-not-a-date'
lexical accept=True  value='2026-10-21 nonsense'
lexical accept=False value='2026-10-20T23:59:59Z'
```

Confirms the contract's gap statement. Fixed by the typed grammar in the draft.

## Draft section (for `corpus/knowledge/static-canonical-preflight.md`, appended, not written)

````markdown
## Receipt replay hardening — round 24

Sources: S### RFC 3339 section 5.6 (date-time and full-date grammar; the NOTE
permitting lowercase `t`/`z` and a space separator) and section 5.7 (leap-second
restriction); S### RFC 9110 sections 5.6.2 (tokens), 5.6.3 (whitespace), 5.6.6
(parameters), 8.3 and 8.3.1 (Content-Type; type and subtype tokens are
case-insensitive), 15.3 (2xx). Verified-at: 2026-10-21, documentation opened this
round (rfc-editor text, read-only GET).

Round-23 replay gates compared a lexical prefix and read `contentType` unchecked.
`scripts/receipt_replay.py` replaces both with typed checks.

### Lexical timestamp prefixes are unsafe

`x[:10] < "2026-10-21"` compares the first ten characters of an arbitrary string.
It accepts `"zzzz-not-a-date"`, `"2026-10-21 nonsense"`, `"2026-10-21garbage"`,
`"2026-13-45T99:99:99Zjunk"` (impossible calendar and clock values) and
`"2099-01-01T00:00:00Z"` (no upper bound, so a future date passes). Only strings
whose first ten characters sort before the bound are rejected.

RFC 3339 defines the timestamp grammar: a date-time is `full-date "T" full-time`
with a required offset (`Z` or `±hh:mm`), and the `date-mday` and `time-second`
ranges are restricted (sections 5.6 and 5.7). The replay parses the field against
that grammar first and compares instants afterwards.

Two fields, two grammars. Round-23 C1 receipts store `observedAt` as an RFC 3339
`full-date` (`"2026-10-21"`), which is kept for the historical c1 units. Live
`fetchedAt` values are always `date-time` with `Z` and follow the date-time rule.

Local policy, stricter than the RFC where stated:

- The RFC NOTE permits lowercase `t`/`z` and a space separator. The replay rejects
  them so receipts stay canonical. This is local policy, not an RFC violation.
- Second value `60` is rejected. Section 5.7 allows it only at leap-second
  instants, which the replay cannot verify.
- A timestamp later than the replay's UTC clock at run time is rejected.
- A timestamp before `2026-10-21T00:00:00Z` (full-date: before `2026-10-21`) is
  rejected.

### Untyped contentType is unsafe

`served()` evaluated `fetch.get("contentType") or ""` and then called `.split`.
A JSON list or number raised `AttributeError`, so the instrument crashed. The
`or ""` also turned `0`, `false` and `[]` into an empty string without a
diagnostic. Python exits 1 on an uncaught exception, the same code as a
rejection, so the exit code alone cannot separate a crash from a verdict.

RFC 9110 section 8.3 defines Content-Type as a media-type. Section 8.3.1 gives
`media-type = type "/" subtype parameters`, with type and subtype as tokens
(section 5.6.2) compared case-insensitively. Parameters are
`*( OWS ";" OWS [ parameter ] )` (section 5.6.6), where OWS is SP or HTAB
(section 5.6.3).

A `contentType` that is not a JSON string is a malformed receipt: a reject row,
not a "not-served" verdict. A string is first matched against the media-type
grammar. Only then is its essence compared, case-insensitively, with `text/html`.
Whitespace before `;` is OWS, so `text/html ;charset=utf-8` is served. `text/html junk`
is not a media type and is rejected rather than reported as not-served.

A surface is served iff its status is 2xx (section 15.3), `error` is null, the
body is not truncated, and the contentType essence is `text/html`.

### Entry point and exit contract

```sh
python3 scripts/receipt_replay.py c1|c2 --root . --revision <commit>
```

- `c1` replays the 17 round-23 drift-detection receipts under
  `.ufo/waves/round-23/receipts/` as they exist at `<commit>`, with the population
  digest gate of `measure_c1.py`.
- `c2` replays the 12 round-23 live surfaces under `.ufo/waves/round-23/live/<id>/`
  and reproduces each `audit.json` through `scripts/canonical_audit.py` at `<commit>`.

| Exit | Meaning | Output |
|---|---|---|
| 0 | Every row accepted | JSON report; stderr empty |
| 1 | At least one row rejected (malformed or mismatched receipt) | Complete JSON report, one row per unit or surface with `problems` |
| 2 | Instrument input unreadable: revision does not resolve, frozen population digest differs, validator missing; also argparse usage errors | JSON error object with no rows, or argparse usage text |

No input produces a Python traceback. A traceback, or stdout that is not one JSON
object, is a failure of the instrument: it is neither exit 0 nor exit 1. A runner
checks the exit code and that stdout parses with `accepted == total` for exit 0.

The round-23 runners `measure_c1.py` and `measure_c2.py` remain byte-intact as
historical evidence. They are not replaced in place.

### Limits of the replay

- Structure, not authentication. A passing receipt shows that its fields are
  well-formed and that the stored bytes reproduce the recorded audit at the
  revision. It does not show that the network GET happened, that the server sent
  those bytes, or that the producer was the recorded client. A receipt built
  consistently by hand passes. Provenance stays in the producer invocation and
  independent seat observations.
- Clock dependence. A pass is valid only for runs made at or after the latest
  recorded timestamp. An earlier replay rejects the same receipt as future.
- `charset` and other parameter values are checked for grammar only, not meaning.
- A leap-second `60` is rejected even where RFC 3339 permits it.
- Only the round-23 c1 and c2 populations are replayed. Round-24 freshness
  receipts are outside this script.
- A pass is a structural and policy result about the bytes stored at `fetchedAt`.
  It is not delivery, rendering, or search-engine selection (round-23 limits
  unchanged).
````

## Checked and held

- `corpus/SOURCES.md`: last row S031 at this base; this draft uses S### placeholders
  for the sources seat's S032+ rows and does not assign numbers.
- `corpus/knowledge/static-canonical-preflight.md`: existing text and line 1 source
  list untouched; the section is appended in the round-23 style (`Sources:` line,
  no edit to the line-1 list), not written.
- RFC 3339 section 5.6 grammar, NOTE on lowercase `t`/`z` and space separator, and
  section 5.7 leap-second restriction: read from the fetched rfc-editor text.
- RFC 9110 sections 8.3.1 (media-type, case-insensitive type/subtype), 5.6.2 (tchar),
  5.6.3 (OWS), 5.6.6 (parameters), 15.3 (2xx): read from the fetched rfc-editor text.
- Round-23 baseline: `measure_c1.py` 17/17 exit 0; `measure_c2.py` 12/12 exit 0 at
  `f7de3ab4e9f030a15a857a5a08631bd8e690f436` (both read-only, `git show` only).
- Timestamp shapes in round-23 receipts and live `fetch.json` files (all `2026-10-21`
  or `2026-10-21T06:33:xxZ`; `contentType` values `text/html` and `text/html; charset=utf-8`).

## Limits

- The CLI in the draft is the contracted interface. `scripts/receipt_replay.py` does not
  exist at the observed HEAD, so its flags, exit codes and "no traceback" behaviour are
  unobserved; re-check the draft against the landed file (F2).
- The F3 traceback claim rests on a function-level probe of a copied predicate, not on a
  committed sandbox run through `measure_c2.py`. The `r23Observed` cases are executor work.
- Clock-dependent future bound: the draft's rule is the scribe's reading of the contract's
  "future strings" gap; the executor and L1 must match it or amend the draft.
- Not run: no builds, no lint, no counters at round-24 paths (none exist), no network
  beyond two read-only GETs of rfc-editor RFC 3339 and RFC 9110 text.
- Tools: none installed or upgraded. `curl` (pre-existing) used for the two GETs. Scratch
  directory: `/tmp/kake-r24-ScribeKnowledgeReplay-ie3h` (probe.py, RFC text copies).
  No lane file other than this report was written. `.ufo/waves/round-24/` shows as
  untracked in the lane (F4); not touched by this seat.
