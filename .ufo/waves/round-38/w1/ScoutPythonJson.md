# ScoutPythonJson — r38 w1: Python `json` docs and the 4300-digit limit (operability/freshness)

Question: do the Python docs (a) say `json` accepts NaN/Infinity outside the spec, (b) say how `parse_constant`/`parse_int` work, (c) state the 4300-digit limit and its ValueError — and does this host behave that way? It explains round-37 D2/D3 (`ReviewRobotsTool.md` lines 22-23).

Both pages fetched fresh; every quote below was also reproduced in a one-line `python3` run on this host: **Python 3.14.8 (main, Oct 2 2026) [GCC 16.2.1]**, `/usr/lib/python3.14/json/__init__.py`.

## Access receipt (GET only, no login, no challenge)

| # | URL requested | UTC | Status | Effective URL / redirect | Bytes | sha256 |
|---|---|---|---|---|---|---|
| 1 | `https://docs.python.org/3/library/json.html` | 2026-10-23T04:30:22Z | **200** | same, 0 redirects | 115104 | `234b80bf7385ea72e198521156d012cbe8997bab428740468f46f881a07f792e` |
| 2 | `https://docs.python.org/3/library/stdtypes.html` | 2026-10-23T04:30:22Z | **200** after **301** | `location: https://docs.python.org/3/builtins/stdtypes.html`, `age: 604680` | 814482 | `04b741a2a8d841f81f74b36c18a35a9ec5b8e87059de7ae46297a24a5a66f06a` |
| 3 | `https://docs.python.org/3.14/library/json.html` (pinned) | 2026-10-23T04:30:50Z | **200** | same | 112740 | `57c32a2790e411b128cdf1faa0d47f842b4759f3d9374dfcb3a98cc98f44b892` |
| 4 | `https://docs.python.org/3.14/library/stdtypes.html` (pinned) | 2026-10-23T04:30:50Z | **200** after **301** | `https://docs.python.org/3.14/builtins/stdtypes.html` | 773977 | `4054caf232e8c27934f22e8ed7c630b0d15564a708d944f67875d13cd8a1a78b` |

Saved bytes + receipt files: `/fast/scratch/hyaku/kake-r38w1/ScoutPythonJson/{json.html,stdtypes.html,v314-json.html,v314-stdtypes.html,receipt-*.txt}` (receipts hold the exact `curl -w` line and `sha256sum` output). `x-cache: HIT, HIT`; server `last-modified: Fri, 23 Oct 2026 01:40:01 GMT`.

## Quotes (each ≤25 words; `file:line` is the saved HTML source line; `[text]` = my elision)

- **Q1 NaN/Infinity accepted (18 w)** — json `json.load`, `json.html:600`: "It also understands NaN, Infinity, and -Infinity as their corresponding float values, which is outside the JSON spec."
- **Q2 non-compliance (23 w)** — "Standard Compliance", `json.html:844`: "This module does not comply with the RFC in a strict fashion, implementing some extensions that are valid JavaScript but not valid JSON."
- **Q3 serializer half (16 w)** — "Infinity and NaN" section, `json.html:880`: "accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON number literal values."
- **Q4 `parse_constant` (17 w)** — `json.html:501`: "If set, a function that is called with one of the following strings: '-Infinity', 'Infinity', or 'NaN'."
- **Q5 the escape hatch (14 w)** — `json.html:501`: "This can be used to raise an exception if invalid JSON numbers are encountered." (also `JSONDecoder`, `json.html:628`: same wording, list `'-Infinity', 'Infinity', 'NaN'`)
- **Q6 `parse_int` (17 w)** — `json.html:497`: "If set, a function that is called with the string of every JSON int to be decoded."
- **Q7 `parse_int` default (9 w)** — `json.html:498`: "If None (the default), it is equivalent to int(num_str)."
- **Q8 the 3.11 link to the limit (14 w)** — `json.html:532`: "The default parse_int of int() now limits the maximum length of the integer string".
- **Q9 the 4300 default (10 w)** — `stdtypes.html:6981` ("Integer string conversion length limitation", anchor `id="int-max-str-digits"` at `stdtypes.html:6946`): "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits."
- **Q10 the ValueError (14 w)** — `stdtypes.html:6967`: "ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5432 digits"
- **Q11 the docs' own "parser limit" framing (16 w)** — `json.html:923,927`: "Some JSON deserializer implementations may set limits on: [the size of accepted JSON texts; the maximum level of nesting;] the range and precision of JSON numbers".

Verbatim identical in the pinned 3.14 page at `v314-json.html:591,825,880→(rendered),491,492,526` and `v314-stdtypes.html:6657` — diff of the extracted sentences is empty.

## One-line confirmations on this host (exit code = observed)

```
$ python3 -c 'import json;print(json.loads("NaN"),json.loads("Infinity"),json.loads("-Infinity"))'
nan inf -inf                                        exit=0     # Q1; also strict=True accepts NaN
$ python3 -c 'import json;print(json.loads("{\"x\":NaN}",parse_constant=lambda c:("C",c)))'
{'x': ('C', 'NaN')}                                 exit=0     # Q4
$ python3 -c 'import json;print(json.loads("[12]",parse_int=lambda s:("I",s)))'
[('I', '12')]                                       exit=0     # Q6
$ python3 -c 'import sys;print(sys.version.split()[0],sys.int_info.default_max_str_digits,sys.get_int_max_str_digits())'
3.14.8 4300 4300                                    exit=0     # Q9
$ python3 -c 'import json;json.loads("["+"9"*5000+"]")'
ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits; ...   exit=1   # Q8/Q10, raised in json/decoder.py:361
$ python3 -c 'import json;print(json.loads("["+"9"*5000+"]",parse_int=lambda s:"ok"))'
['ok']                                              exit=0     # Q6: a custom parse_int never calls int()
$ python3 -c 'import json;print(json.loads("{\"x\":1e400}"))'
{'x': inf}                                          exit=0     # see hazard below
```

Boundary: `int('9'*4300)` succeeds, `int('9'*4301)` raises the same ValueError. Non-JSON variants rejected as expected (`+Infinity`, `nan`, `inf`, `INFINITY`, `01`, `+1`, `1_000`, `1.`, `.5`, `0x10`, `[1,]`, `True`, `NULL` → JSONDecodeError), so the three tokens are the whole extension set; `-0` → `0` (int).

## What this settles for round-37 D2/D3

- **D2 (observed, now documented):** `json.loads` accepting `NaN`/`Infinity`/`-Infinity` is documented unspec behaviour, not a tool bug of its own. The repair lever is documented too: `parse_constant` is called with exactly `'-Infinity'`, `'Infinity'`, `'NaN'` (Q4), and the docs name raising from it as the intended use (Q5). Tool must classify that raise as `input_invalid` — note `json.JSONDecodeError` subclasses `ValueError`, so a bare `except ValueError` around `loads` cannot distinguish this from a syntax error by type alone.
- **D3 (observed, now documented):** the 4300-digit failure is the interpreter's *integer-string conversion* limit reached through the default `parse_int` (Q8), and the docs classify range limits on numbers as an *implementation* limit of deserializers (Q11) — i.e. a parser fault, not a syntax violation, which agrees with C2 (h)'s `check_invalid` for out-of-range status. Passing `parse_int` avoids `int()` entirely (last confirmation), so "integers of any length … unused long numbers change nothing" is reachable without raising the interpreter limit; a repair that leaves the default in place cannot implement (h) as written.

## Freshness observations (inference where marked)

- **Observed:** `docs.python.org/3/library/stdtypes.html` now 301s to `/3/builtins/stdtypes.html` (and `/3.14/library/stdtypes.html` → `/3.14/builtins/stdtypes.html`); anchor `#int-max-str-digits` survives at both targets. A citation that spells the old path resolves only through the redirect — pin the new path *and* the sha256 above.
- **Observed:** `/3/` currently serves **Python 3.15.1** docs, `/3.14/` serves **3.14.9**; this host runs **3.14.8**. Quoted sentences are word-identical across the two pages, so behaviour claims verified on 3.14.8 are backed by both.
- **Observed (bears on S034):** the json page cites "RFC 7159 (which obsoletes RFC 4627)" (`json.html:234`) — **not** RFC 8259. Any lane text citing docs.python.org as corroboration for RFC 8259 inherits an off-by-one RFC; RFC 8259 supersedes 7159. The normative JSON grammar source must stay S034, not this page.
- **Hazard for (h) wording (inference, untested against the sealed key):** `1e400` is a *valid* RFC 8259 number (syntax) that Python decodes to `inf`. Rule (h) keys on "non-JSON number literals", so a repaired tool that maps decoded `inf`/`nan` to `input_invalid` would also reject `1e400`; one that only hooks `parse_constant` leaves `1e400` → `check_invalid` via range. The C2 sentence does not decide this; flagging rather than guessing.

## Not done / limits

- Did not read, list or stat `/fast/scratch/hyaku/kake-r38/` or `.../kake-r38ctl/`; did not run any round-38 counter; did not open any owned site. No tools installed or upgraded (nothing needed).
- Opened only the four `docs.python.org` URLs above (GET). Nothing else fetched.
- Not verified: that the sealed cases exercise `parse_int`/`parse_constant` repairs at all; whether the L1's chosen repair keeps `1e400` semantics. Those are L1/build decisions, not doc facts.
- Sandbox artifacts: `/fast/scratch/hyaku/kake-r38w1/ScoutPythonJson/` (`json.html`, `stdtypes.html`, `v314-json.html`, `v314-stdtypes.html`, `receipt-json.html.txt`, `receipt-stdtypes.html.txt`, `receipt-v314-json.html.txt`, `receipt-v314-stdtypes.html.txt`); all processes exited.
