# ScoutReopenS034 — r38 w1: live re-open of RFC 8259 §6/§9 and verdict on rule (h)

Item: GET S034 (https://www.rfc-editor.org/rfc/rfc8259.txt), quote §6's Infinity/NaN exclusion and the implementation-limits sentence on number range and precision, judge whether amendment (h) reads S034 correctly, including "a number of any length is JSON". Leaf; no subagents, no sealed tree touched, no round-38 counter run.

## Access receipt (GET/HEAD only, no login, no challenge, ordinary means)

| URL | UTC | HTTP | final URL | bytes | sha256 |
|---|---|---|---|---|---|
| https://www.rfc-editor.org/rfc/rfc8259.txt | 2026-10-23T04:30:20Z | 200 | same, 0 redirects | 28360 | `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` |
| same URL, independent second GET | 2026-10-23T04:30:51Z | 200 | same | 28360 | same digest |
| https://www.rfc-editor.org/rfc/rfc8259.json | 2026-10-23T04:30:5xZ | 200 | same | 1074 | `5de136e66c519d883f0fc66947ba25e88a6b11c54770429bf287b0ac5782c724` |
| https://www.rfc-editor.org/errata/rfc8259 | 2026-10-23T04:31Z | 200 | errata.rfc-editor.org/search/?rfc_number=8259&presentation=records | 93426 | `5819db2e0233addf17ed540db88cf92cbefda5a60c38877e0d4cbf6b876b7cf4` |

`curl` exit 0 on every fetch. HEAD at 04:30:51Z: `etag: W/"effcde61d580b8bb9e8eb8fdca283c5f"`, `cache-control: public, max-age=86400`, `link: <https://www.rfc-editor.org/info/rfc8259/>; rel="canonical"`.

Freshness: the body is byte-identical to the day the row opened (2026-10-21, `corpus/lessons/round-24.md:33` records the same sha256) and to the round-26 recheck (`.ufo/waves/round-26/rechecks/S034.json`, HOLD, same digest). Metadata: `INTERNET STANDARD`, `obsoletes ["RFC7159"]`, `obsoleted_by []`, `updates []`, `updated_by []`, `pub_date "December 2017"`. Errata: 7383 **Verified** §3, 9095 Reported §11, 7650 Held for Document Update §7, 5218 Rejected §12 — **none touches §6 or §9**. S034's row (`corpus/SOURCES.md:42`, teaches "NaN and Infinity are not JSON numbers", 365 d recheck) still matches: no drift, no row change due.

Sandbox artifacts (sha256 above): `/fast/scratch/hyaku/kake-r38w1/ScoutReopenS034/{rfc8259.txt,rfc8259b.txt,rfc8259.json,errata8259.html}`.

## Quotes (exact, whitespace-normalized, matched against the saved body)

- **§6 Numbers**, `rfc8259.txt:377-378`, 18 words: "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted."
- **§6 Numbers**, `rfc8259.txt:407-408`, 15 words: "This specification allows implementations to set limits on the range and precision of numbers accepted."
- **§9 Parsers**, `rfc8259.txt:548-550`, 12 words: "An implementation may set limits on the range and precision of numbers."
- §6 grammar `:380`, `:399`: `number = [ minus ] int [ frac ] [ exp ]`; `int = zero / ( digit1-9 *DIGIT )` — no length bound in the production.
- §9 `:543-544`: "A JSON parser MUST accept all texts that conform to the JSON grammar."; `:545`: "A JSON parser MAY accept non-JSON forms or extensions."
- §6 `:413-416` names `1E400` as a JSON number raising interoperability concerns (supports keeping `1e400` a float, per the C2 clarification).

## Verdict on (h)

**Exclusion half: correct.** NaN/Infinity fail the §6 grammar, so a manifest holding them outside a string is not a JSON text; `input_invalid` (check null, nothing evaluated) matches the RFC. Two qualifications: the RFC names only Infinity and NaN — `-Infinity` is right by derivation (minus must precede `int` digits, `:399`) but is not a quoted instance; and §9:545 lets a parser accept them as extensions, so rejecting them is lane policy within the RFC, not an RFC mandate.

**"A JSON number of any length is JSON": overstated if read as an acceptance rule.** True as grammar conformance (nothing bounds `*DIGIT`), but §6:407-408 and §9:548-550 expressly allow an implementation to set range and precision limits. A parser may therefore refuse a huge integer without violating the RFC, and (h)'s rule — accept as a number, out-of-range status ⇒ `check_invalid`, unread long number ⇒ nothing — is a lane policy *permitted* by the RFC and stricter than it, not a reading the RFC compels. Wording fix: "conforms to the JSON grammar, which bounds no length", citing §9:543-545 for the acceptance allowance; as written (h) risks the overstatement class round 37 was closed for.

**Real teeth at the base.** `scripts/robots_audit.py` at `af43a50f`, sha256 `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5` (matches the declared `944d2f51…d3e5`), calls `json.loads(text)` with no hooks (line 397) and maps any `ValueError` to `None` ⇒ `input_invalid` (398-399). Python here is 3.14.8 (GCC 16.2.1): `json.loads` of a 4301-digit integer raises `ValueError: Exceeds the limit (4300 digits) for integer string conversion` (4000 digits succeeds) and accepts `NaN`/`Infinity`/`-Infinity` as floats (exit 0). So at base a 5000-digit `robotsStatus`, or a 5000-digit number in a field the contract never reads, invalidates the whole manifest — exactly what (h) forbids — and a `NaN` status yields `check_invalid` instead of `input_invalid`.

**The 20 s bound is satisfiable but forces the right implementation.** `json.loads` with a `parse_int` hook over a 64 MiB all-digit number finished in 0.03 s (exit 0). `int()` on that literal cannot meet 20 s: measured 5 000 000 digits → 2.656 s, 20 000 000 → 9.95 s (superlinear; 64 MiB ≈ 67 M digits ⇒ minutes). Length-first or hook-based comparison passes; a full `int()` fails.

## Commands run (exit codes)

`curl -sS -L -o …` four GETs → 200, exit 0 (two byte-identical body fetches); `curl -sSI` → 200, exit 0; `sha256sum` over all saved bytes (values above); `git show af43a50f:scripts/robots_audit.py | sha256sum` → `944d2f51…d3e5`; `python3` 3.14.8 probes (4300-digit limit, NaN/Infinity acceptance, 64 MiB `parse_int`) under `timeout`/`prlimit`, all exit 0; `int()` timing runs under `timeout 60/200 prlimit --as=4G/8G`, exit 0. No process left running.

## Not verified / limits

Whether the sealed (h) cases exercise the >4300-digit and unread-long-number sub-cases (key unavailable by rule; not inspected). The 64 MiB bound end-to-end through counter v3's 20 s wall (only the parse component measured). No datatracker revision history beyond the metadata JSON above.
