# ExecDefects — round 88 / w1 — D2 diagnostic repair (copy only)

Seat: `ExecDefects` (leaf, no subagents). Lane root:
`/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE). Base
`f4479c14813037ad993a49a3dee4028763470f7a`, freeze v2
`8063739791e21a8d7966fd968913e552e1433881`. No production edit, no commit, no
network, no tool install, no clone (0 of the allowed 1).

**Result:** repaired candidate written to
`LANE/.ufo/waves/round-88/w1/ExecDefects/cache_current_age.py` (mode 755,
sha256 `6513037537eee95653d9cff50d20923d2980f82387357c94826878824b7b559e`,
6710 bytes). Base 6571 bytes, 146 physical lines; candidate 6710 bytes, 146
physical lines. Exactly one line differs (line 34) and it is the invalid-input
message statement. The round's own D2 predicate (`item_d2`) is **GREEN** on the
candidate and returns exactly one fail on the frozen base. Candidate
`--selftest` prints `selftest: 61 isolated CLI fixtures passed`, exit 0, same as
base. Arithmetic stdout is byte-identical to base on all seven differential
fixtures.

Receipts (copied out of scratch before deletion): `receipts/out/` (94 files;
receipts, streams and summary files) plus the three drivers at
`receipts/drivers/{run_receipts.sh,line_proof.py,predicate_probe.py}` — 97 files
in `receipts/`.

---

## 1. Provenance of the base copy

```
$ sha256sum LANE/.ufo/waves/round-88/frozen/base-cache_current_age.py
d1b09ae17a54728a3b967cdc7436f19b62fc98e4304aab64324ee8969454331a  .../frozen/base-cache_current_age.py
$ git -C LANE rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/kake-shokunin
$ git -C LANE show f4479c14813037ad993a49a3dee4028763470f7a:scripts/cache_current_age.py | sha256sum
d1b09ae17a54728a3b967cdc7436f19b62fc98e4304aab64324ee8969454331a  -
$ sha256sum LANE/scripts/cache_current_age.py
d1b09ae17a54728a3b967cdc7436f19b62fc98e4304aab64324ee8969454331a  LANE/scripts/cache_current_age.py
```

The frozen base copy is byte-equal to the base-commit blob and to the current
production script (still pre-integration). `git show` is read-only; no git/jj
mutation was issued. The scratch working copy
(`/fast/scratch/hyaku/kake-r88/ExecDefects/base-cache_current_age.py`) has the
same sha256, so the red-before runs exercised the frozen base bytes. Production
sha256 re-checked after all runs: unchanged `d1b09ae1…`.

Tooling: `/usr/bin/python3` = `Python 3.14.8 (main, Oct  2 2026, 10:23:31)
[GCC 16.2.1 20260810]`. Arithmetic is `int`-only; nothing version-specific was
added.

---

## 2. The change (base line 34 only)

`diff -u` (driver: `receipts/drivers/run_receipts.sh`, file
`receipts/out/diff-u.txt`), exit **1** (files differ, expected):

```diff
--- /fast/scratch/hyaku/kake-r88/ExecDefects/base-cache_current_age.py	2026-11-04 15:44:33.448637679 -0300
+++ /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ExecDefects/cache_current_age.py	2026-11-04 15:55:37.731572038 -0300
@@ -31,7 +31,7 @@
     for key in (*REQUIRED, "age_value"):
         value = payload.get(key, 0)
         if not isinstance(value, int) or isinstance(value, bool):
-            raise ValueError(f"{key} must be an integer, not boolean")
+            raise ValueError("%s must be an integer, not %s" % (key, {bool: "boolean", type(None): "null", str: "string", float: "float", list: "array", dict: "object"}.get(type(value), type(value).__name__)))
         if key != "date_value" and value < 0:
             raise ValueError(f"{key} must be nonnegative")
     date_value = payload["date_value"]
```

Line-level proof (`receipts/out/line-proof.txt`, exit 0):

```
base_sha256: d1b09ae17a54728a3b967cdc7436f19b62fc98e4304aab64324ee8969454331a
cand_sha256: 6513037537eee95653d9cff50d20923d2980f82387357c94826878824b7b559e
base_bytes: 6571 cand_bytes: 6710 delta_bytes: 139
base_lines_split: 147 cand_lines_split: 147
equal_line_count: True
trailing_newline_preserved: True
differing_line_numbers_1based: [34]
differing_line_count: 1
all_other_lines_byte_identical: True
base_line_34: '            raise ValueError(f"{key} must be an integer, not boolean")'
cand_line_34: '            raise ValueError("%s must be an integer, not %s" % (key, {bool: "boolean", type(None): "null", str: "string", float: "float", list: "array", dict: "object"}.get(type(value), type(value).__name__)))'
base_line_34_len: 70
cand_line_34_len: 209
base_message_lines: [34]
cand_message_lines: [34]
base_message_occurrences: 1
cand_message_occurrences: 1
syntax_ast_parse: ok
```

So: identical line count, zero changed bytes outside line 34, one
`must be an integer` message occurrence in each file, arithmetic and the
six-key return dict untouched. The change maps the offending JSON value's type
to its JSON type name — `boolean`, `null`, `string`, `float`, `array`,
`object` — and keeps `type(value).__name__` only as an unreachable fallback
(`json.loads` yields exactly those six types). The message still begins with the
offending key, and the exit code / `invalid_input:` prefix contract is
untouched.

---

## 3. Red-before receipts (frozen base copy, sha256 `d1b09ae1…`)

Environment for every run: `TMPDIR=/fast/scratch/hyaku/kake-r88/ExecDefects/tmp`,
`PYTHONDONTWRITEBYTECODE=1`, `python3 -B`, cwd
`/fast/scratch/hyaku/kake-r88/ExecDefects`. Receipts:
`receipts/out/red-base-float.receipt`, `red-base-bool.receipt`,
`base-selftest.receipt`.

```
$ printf '%s' '{"date_value": 7.0, "request_time": 1, "response_time": 2, "now": 3}' | /usr/bin/python3 -B /fast/scratch/hyaku/kake-r88/ExecDefects/base-cache_current_age.py
exit: 1
stdout_bytes: 0
stderr (58 bytes): invalid_input: date_value must be an integer, not boolean
```

```
$ printf '%s' '{"date_value": true, "request_time": 1, "response_time": 2, "now": 3}' | /usr/bin/python3 -B /fast/scratch/hyaku/kake-r88/ExecDefects/base-cache_current_age.py
exit: 1
stdout_bytes: 0
stderr (58 bytes): invalid_input: date_value must be an integer, not boolean
```

```
$ /usr/bin/python3 -B /fast/scratch/hyaku/kake-r88/ExecDefects/base-cache_current_age.py --selftest </dev/null
exit: 0
stdout (42 bytes): selftest: 61 isolated CLI fixtures passed
stderr: (empty)
```

The float input is red exactly as routed: exit 1 with `invalid_input:`, correct
key, but the wrong type word (`boolean` where JSON says `float`). The bool input
is accidentally correct and is the only type word the base ever emits.

---

## 4. Candidate receipts (sha256 `65130375…`)

```
$ printf '%s' '{"date_value": 7.0, "request_time": 1, "response_time": 2, "now": 3}' | /usr/bin/python3 -B LANE/.ufo/waves/round-88/w1/ExecDefects/cache_current_age.py
exit: 1
stdout_bytes: 0
stderr (56 bytes): invalid_input: date_value must be an integer, not float
```

```
$ printf '%s' '{"date_value": true, "request_time": 1, "response_time": 2, "now": 3}' | /usr/bin/python3 -B LANE/.ufo/waves/round-88/w1/ExecDefects/cache_current_age.py
exit: 1
stdout_bytes: 0
stderr (58 bytes): invalid_input: date_value must be an integer, not boolean
```

```
$ printf '%s' '{"date_value":80,"request_time":90,"response_time":100,"now":130,"age_value":5}' | /usr/bin/python3 -B LANE/.ufo/waves/round-88/w1/ExecDefects/cache_current_age.py
exit: 0
stdout (128 bytes): {"apparent_age":20,"response_delay":10,"corrected_age_value":15,"corrected_initial_age":20,"resident_time":30,"current_age":50}
stderr: (empty)
```

```
$ /usr/bin/python3 -B LANE/.ufo/waves/round-88/w1/ExecDefects/cache_current_age.py --selftest </dev/null
exit: 0
stdout (42 bytes): selftest: 61 isolated CLI fixtures passed
stderr: (empty)
```

The float message names `date_value` + `float` and no longer contains
`boolean`; the bool message names `boolean` and contains no `float`; the valid
input emits all six integer terms; the 61-fixture selftest is green.

### Probes requested plus extra type coverage

All candidate, same invocation form; receipts `receipts/out/cand-*.receipt`.

| stdin | exit | stderr |
|---|---|---|
| `{"date_value": "80", ...}` | 1 | `invalid_input: date_value must be an integer, not string` |
| `{"date_value": null, ...}` | 1 | `invalid_input: date_value must be an integer, not null` |
| `{"date_value": [], ...}` | 1 | `invalid_input: date_value must be an integer, not array` |
| `{"date_value": {}, ...}` | 1 | `invalid_input: date_value must be an integer, not object` |
| `{..., "age_value": 5.0}` | 1 | `invalid_input: age_value must be an integer, not float` |
| `{"date_value": 80, "request_time": "90", ...}` | 1 | `invalid_input: request_time must be an integer, not string` |
| missing `date_value` | 1 | `invalid_input: missing date_value` |
| valid + `"extra": 1` | 1 | `invalid_input: unknown input key` |
| `[]` | 1 | `invalid_input: input must be a JSON object` |
| request 100 > response 90 | 1 | `invalid_input: require request_time <= response_time <= now` |
| `age_value: -1` | 1 | `invalid_input: age_value must be nonnegative` |

For the four non-int types the base said `not boolean` in every case
(`receipts/out/predicate.txt`, section `type-name wording`), so the repair
covers the whole type-word defect, not only the routed float case.

---

## 5. Arithmetic / exit-code identity

Seven base-vs-candidate differential runs (`receipts/out/arith-*.receipt`).
Each entry is `exit base/cand`, stdout comparison by `cmp`:

| fixture | exits | stdout | receipt |
|---|---|---|---|
| valid six-key | 0/0 | IDENTICAL | `arith-valid` |
| both max branches | 0/0 | IDENTICAL | `arith-both-max` |
| age-value max branch | 0/0 | IDENTICAL | `arith-age-max` |
| future Date, negative `date_value` | 0/0 | IDENTICAL | `arith-future-date` |
| all times equal | 0/0 | IDENTICAL | `arith-equal-times` |
| omitted `age_value` | 0/0 | IDENTICAL | `arith-omitted-age` |
| 60-digit magnitude `date_value`/`age_value` | 0/0 | IDENTICAL | `arith-huge` |

No stderr on any of these (`stderr` files are 0 bytes). Exit codes on every
invalid probe above are 1 for both base (measured for the four type probes and
the two routed inputs) and candidate; the single-line diff proves no other
control flow changed.

---

## 6. Round-counter evidence (read-only import of the committed counter)

Driver: `receipts/drivers/predicate_probe.py`, run as
`cd /fast/scratch/hyaku/kake-r88/ExecDefects && /usr/bin/python3 -B
/fast/scratch/hyaku/kake-r88/ExecDefects/predicate_probe.py`, exit 0, output
`receipts/out/predicate.txt`. It loads
`LANE/.ufo/waves/round-88/c88_defect_queue.py` via `importlib` and calls the
committed `item_d2` / `_run_tool`; all writes land under
`/fast/scratch/hyaku/kake-r88/ExecDefects/predwork`.

```
item_d2(base bytes)                            -> ['float input diagnostic does not name float (or still says boolean)']
item_d2(candidate bytes)                       -> GREEN (no fails)
item_d2(counter repaired_tool_bytes)           -> GREEN (no fails)
item_d2(gap mutant: float for str/null/list)   -> GREEN (no fails)
item_d2(mutant: always boolean otherwise)      -> GREEN (no fails)
```

Counter selftest (`/usr/bin/python3 -B LANE/.ufo/waves/round-88/c88_defect_queue.py
--selftest`, TMPDIR set, output `receipts/out/counter-selftest.txt`), exit 0:
`selftest: 11/11 passed` (all labelled PASS, including "mutant: base diagnostic
reopens D2 only" and "green tree closes all three").

The rejected input `7.0` scores as a miss on base for exactly one reason and
passes on the candidate, which is the D2 predicate's whole surface.

---

## 7. Defects / limits found in the round's own counters and case set

1. **D2's type-naming check is float-only (coverage gap).** `item_d2` inspects
   the type word only for the float case (`'float' in stderr` and `'boolean' not
   in stderr`) and the bool case (`'boolean' in stderr`, `'float' not`). It
   never sends a string, null, array or object value, so a tool that names the
   wrong type for those inputs is still green. Demonstrated: mutant
   `float for str/null/list` and mutant `float if float else boolean` both return
   `GREEN (no fails)`, yet their messages are
   `invalid_input: date_value must be an integer, not float` for a string and
   `invalid_input: date_value must be an integer, not boolean` for null
   (`receipts/out/predicate.txt`). The contract's phrase "must name the
   offending JSON type" is therefore only enforced for `float`/`boolean`. This
   does **not** create a false green for the committed production byte in this
   wave (the routed defect is the float case), but it means D2 cannot
   distinguish a fully type-accurate repair from a float/bool-only one.
2. **The counter's green fixture names Python types, not JSON types.**
   `c88_defect_queue.repaired_tool_bytes()` substitutes
   `... % (key, "boolean" if isinstance(value, bool) else type(value).__name__)`,
   so its messages are `not str` for a string, `not NoneType` for null,
   `not list` for an array and `not dict` for an object
   (`receipts/out/predicate.txt`, `counter-fix` rows). It passes `item_d2`
   (see gap 1) and it keeps the 11/11 selftest green, but it is not a valid
   template for the ticket's example `... not string`: if L1 promotes
   `repaired_tool_bytes()` verbatim into `scripts/cache_current_age.py`, the
   production diagnostic leaks Python type names for non-float inputs. The
   candidate in this seat avoids that by mapping to JSON type names. Counter
   selftest remains 11/11 either way.
3. **Base's defect is wider than the routed float repro.** For
   `string`, `null`, `array` and `object` the base also says `not boolean`
   (four measured rows in `receipts/out/predicate.txt`). The routed repro only
   names float; a fix that special-cases float (`"float" if isinstance(value,
   float) else "boolean"`) is green on D2 but still mislabels the other four
   types — this is exactly the second green mutant above.
4. **Sibling bytecode in the wave directory (not mine, not production).**
   `LANE/.ufo/waves/round-88/__pycache__/{c88_defect_queue,c88_vary}.cpython-314.pyc`
   exist with mtimes 15:54:29 and 15:57:13. My import ran at 15:56:38 under
   `-B` + `PYTHONDONTWRITEBYTECODE=1` and did not rewrite either file (the
   `c88_defect_queue` pyc mtime predates it and is unchanged), so these come
   from other concurrent seats. They are untracked bytecode under `.ufo/`, not
   `scripts/`/`corpus/` production bytes, but they sit inside the wave directory
   and are worth sweeping before the round closes.
5. **Base bool message is accidentally correct** — the bool row was already
   green before the fix; only the float row reds the predicate. Recorded so the
   red-before receipt is not misread as two independent reds.

This seat read `vary-cases.json` only for round context and has nothing to
report about it, but did not exercise C2: no claim is made about `c88_vary.py`,
the seeded random population or freshness.

---

## 8. Risks and limits of the candidate

- **Line length.** The replaced line is 209 chars vs 70 for the base line (the
  file's other lines are ≤ 101). This was deliberate: the contract names "the
  D2 diagnostic line" as the production byte, the counter's own
  `repaired_tool_bytes()` uses the same 1:1 line replacement shape, and 1:1
  keeps the diff proof exact (one removed line, one added line, zero other byte
  changes). A helper function or module constant would be prettier but would add
  hunks/lines outside the diagnostic line. If L1 prefers, the expression can be
  split across continuation lines without changing behaviour — but then the diff
  is no longer literally one message line.
- The inline dict literal is built only on the error path; no hot-path cost, no
  state, no import change.
- `type(value).__name__` is a defensive fallback only; `json.loads` can produce
  exactly `dict/list/str/int/float/bool/None`, all mapped. `int` never reaches
  the message (it passes the guard unless it is a bool).
- Message wording is behavioural surface: `float` and `boolean` are the two
  words the committed predicate inspects; both are preserved with the correct
  spelling. `string`/`null`/`array`/`object` are the JSON type names requested
  by the ticket.
- The candidate was exercised only through its CLI (the contract's surface) and
  through the counter's own `_run_tool`. `decode()` is not imported elsewhere in
  the lane by my reading, but I did not run a lane-wide reference search; if some
  consumer parses the stderr text expecting `boolean`, that consumer would need
  the same review. (No such consumer is named in the contract.)
- Not measured: the full C1 carrier against production (production still equals
  base, so D2 would still be open there). D1 and D3 are other seats' items and
  were not touched.

## 9. Files written (only allowed paths)

```
LANE/.ufo/waves/round-88/w1/ExecDefects/cache_current_age.py            (755, 6710 B, sha256 65130375…)
LANE/.ufo/waves/round-88/w1/ExecDefects/receipts/drivers/run_receipts.sh
LANE/.ufo/waves/round-88/w1/ExecDefects/receipts/drivers/line_proof.py
LANE/.ufo/waves/round-88/w1/ExecDefects/receipts/drivers/predicate_probe.py
LANE/.ufo/waves/round-88/w1/ExecDefects/receipts/out/*                 (94 receipt files)
LANE/.ufo/waves/round-88/w1/ExecDefects.md                             (this report)
```

Scratch `/fast/scratch/hyaku/kake-r88/ExecDefects/` was created explicitly,
used for the base copy, `TMPDIR`, predicate work dir and receipts, and is
deleted before yield. No `/tmp` path is cited as evidence. No tool was
installed or upgraded (pacman never invoked). No network request was made.
