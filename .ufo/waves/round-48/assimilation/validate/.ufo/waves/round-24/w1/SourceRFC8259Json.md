# RFC 8259 JSON parsing evidence — Kake R24

## Verdict

For receipt replay, bare `json.loads` is too permissive: it silently resolves duplicate object names by retaining the last value and accepts `NaN`/`Infinity` as non-standard values. Reject duplicate names and these constants as receipt-validation failures; ensure failures become exit 1 or 2 without a traceback. Treat RFC `true`/`false` as booleans, not numeric schema values.

## Findings

### P1 — Duplicate names are silently overwritten (C2, operability)

- **RFC evidence:** RFC 8259 §4: “The names within an object SHOULD be unique.” (8 words.) It also says: “When the names within an object are not unique, the behavior of software that receives such an object is unpredictable.” (20 words.) RFC 8259 §9 adds: “A JSON parser MAY accept non-JSON forms or extensions.” (9 words.) Thus rejecting duplicates is a sound receipt-integrity policy; the §4 keyword is `SHOULD`, not an RFC `MUST`.
- **Exact command:** `python3 -c 'import json; cases = [("duplicate", "{\"x\":1,\"x\":2}"), ("NaN", "NaN"), ("Infinity", "Infinity")]; [print(f"{name}: accepted {json.loads(text)!r}") for name, text in cases]'`
- **Exact observed output (duplicate case):** `duplicate: accepted {'x': 2}`
- **Source locus:** `.ufo/waves/round-23/measure_c1.py:47-50` and `.ufo/waves/round-23/measure_c2.py:47-50` both call `json.loads` without an `object_pairs_hook`; each only catches `JSONDecodeError`. This is source inspection, not an end-to-end invocation of either frozen counter.
- **Smallest fix:** Add an `object_pairs_hook` that detects and rejects repeated decoded names at every object level; map that parser rejection to the replay's normal nonzero result without traceback. A probe also confirmed the hook must compare decoded keys: default parsing of `{"a":1,"\\u0061":2}` returns one key, while a duplicate-checking hook rejects it.

### P1 — `NaN` and `Infinity` parse as values (C2, operability)

- **RFC evidence:** RFC 8259 §6: “Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted.” (18 words.)
- **Exact command:** same command as the duplicate finding.
- **Exact observed output:**
  ```text
  NaN: accepted nan
  Infinity: accepted inf
  ```
  The broader probe also parsed `[Infinity,-Infinity]` as a list containing both non-finite values.
- **Source locus:** The same unconfigured `json.loads` calls at `measure_c1.py:48` and `measure_c2.py:48` accept these tokens; a normal schema check might catch some resulting values later but the parser itself does not reject them.
- **Smallest fix:** Supply `parse_constant` that rejects `NaN`, `Infinity`, and `-Infinity`; also prevent finite-grammar numbers such as `1e400` from silently becoming Python `inf` (e.g. validate parsed floats with `math.isfinite`). The probe observed default `json.loads("1e400")` as `inf`; §6 allows implementation range limits and identifies `1E400` as a possible interoperability problem.

### P2 — JSON booleans are not numbers; avoid Python's `bool`/`int` trap (C2, operability)

- **RFC evidence:** RFC 8259 §3 says: “A JSON value MUST be an object, array, number, or string, or one of the following three literal names:” (19 words), followed by the literal names `false`, `null`, `true` on lines 301–303. They are separate from the `number` alternative. §3 also says: “The literal names MUST be lowercase. No other literal names are allowed.” (12 words.)
- **Exact observed output from `python3 /tmp/kake-r24-SourceRFC8259Json-3jfs/probe_json.py` (Python 3.14.8):**
  ```text
  C1 true
    default json.loads : OK True
  isinstance(True, int) = True
  True == 1 -> True; False == 0 -> True; 1.0 == 1 -> True
  ```
- **Source locus:** `measure_c2.py:58-59` already uses `type(status) is not int` for its recorded HTTP status, correctly excluding booleans there. Preserve that exact-type discipline for integer receipt fields; do not infer a replay bug on this field from Python's `isinstance` behavior alone.
- **Smallest fix:** Validate each receipt field against its declared JSON type; use `type(value) is int` for integer-only fields, and exclude `bool` explicitly from generic numeric checks. `true` and `false` remain valid JSON literals where the schema expects booleans.

## Checked and held

- **RFC URL:** https://www.rfc-editor.org/rfc/rfc8259.txt
- **Access:** 2026-10-21T11:45:33Z (HTTP HEAD returned `HTTP/2 200` and `date: Wed, 21 Oct 2026 11:45:33 GMT`).
- **SHA-256 of the fetched RFC text:** `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` (28,360 bytes).
- **Retrieval/hash command:** `curl -fsSL -o /tmp/kake-r24-SourceRFC8259Json-3jfs/rfc8259.txt https://www.rfc-editor.org/rfc/rfc8259.txt && sha256sum /tmp/kake-r24-SourceRFC8259Json-3jfs/rfc8259.txt && wc -lc /tmp/kake-r24-SourceRFC8259Json-3jfs/rfc8259.txt`
- **Parser test environment:** `python3 --version` → `Python 3.14.8`; `sys.get_int_max_str_digits()` → `4300`.
- **Additional parser observations:** Default `json.loads` accepted `-Infinity` as well as `Infinity` and `NaN`; it rejects other tested malformed literals such as `True`. An RFC-number-grammar probe over 2,801 short candidates found no mismatch; a literal probe isolated the three extensions `NaN`, `Infinity`, and `-Infinity`. This does not establish equivalence for all possible JSON texts.
- **Current tree scan (not frozen-revision counter validation):** a read-only scratch scan examined 190 current round-23/round-24 JSON files and Markdown `json` fences. Of those, 184 parsed by default; six fenced blocks were not standalone JSON. The strict scratch parser accepted all 184 default-accepted units; no current strict-only rejection was observed.
- No tools were installed or updated.

## Limits

The RFC text and Python behavior were directly observed. The round-23 parser call sites were read, but the frozen round-23 counters were not run end-to-end against mutated receipt files; this report is source evidence, not C2 population or admission evidence. The scratch scan describes the current filesystem, not the frozen base revision or the round-24 malformed-case counter.