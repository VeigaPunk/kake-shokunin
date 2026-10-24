# W2A3 FidelityStdlibConvenience — attack of `.ufo/waves/round-39/a3-controls/w1a3/CtlStdlibConvenience.py`
Axes: operability; freshness (byte-exact materialization of wave-1 output).
Verdict: **faithful shortcut** — keeps its named shape, genuinely skips the lexical-grammar work its shape declares, and is byte-for-byte the seat's deliverable. Not a tweak: no dead-w1 base/diff applies (fresh w1a3 write).

## Shape kept — holds
- Imports `CtlStdlibConvenience.py:4-10` are stdlib only: json, sys, datetime, pathlib, urllib.parse.urlsplit, xml.etree.ElementTree, xml.parsers.expat. Grep for `urlopen|requests|socket|http\.client|Decimal|re\.|fullmatch|gzip` matched only the import lines — no network, no gzip, no lexical-grammar library (`re`/`Decimal` absent).
- Docstring `:2` declares "parser/conversion conveniences, no lexical grammar" — the assigned "stdlib conveniences only" shape is intact.

## Skips the declared work — holds (executed, not inferred)
- `:87` `return "".join(parts).strip()` — Python Unicode strip over-trims vs contract sentence 21 (only U+0020/U+0009/U+000D/U+000A may be removed).
- `:92` `:98` `datetime.fromisoformat`/`date.fromisoformat` — accepts non-W3C spellings vs sentences 28-30.
- `:106` `return 0.0 <= float(value) <= 1.0` — binary float, no xsd:decimal lexical form, no exact-decimal range vs sentence 32.
- 3 contract-derived inputs in sandbox `/fast/scratch/hyaku/kake-r39a3w2/KakeR39A3.FidelityStdlibConvenience/t/`, command `timeout 60 prlimit --as=4000000000 python3 -B CtlStdlibConvenience.py --manifest t/<case>/manifest.json` (Python 3.14.8). All three: exit 0, `verdict:clean`, `findings:[]` — where a correct tool must give `failed-policy`, exit 1:
  - `A-nbsp-loc`: loc text U+00A0-padded `https://example.com/dir/page` → contract 21-22 → `loc_not_absolute` entry 1.
  - `B-basic-date`: `<lastmod>20240229</lastmod>` → contract 28 → `lastmod_invalid` entry 1.
  - `C-priority-lexical`: `<priority>1e0</priority>` and `<priority>1.0000000000000000000000000001</priority>` → contract 32 → `priority_invalid` entries 1,2.
- Seat's own static witness executed too: `/fast/scratch/hyaku/kake-r39a3w1/CtlStdlibConvenience/t/lexical-gap/manifest.json` → exit 0, clean — matches that report's `[INFERENCE]` row (0/clean despite five contract violations); their static expectation held under execution.

## Materialization — holds
- `sha256sum`: repo control `.ufo/waves/round-39/a3-controls/w1a3/CtlStdlibConvenience.py` = `a1b61e4cb706cd477bb295bd4dbab997507814bc3bc1a13a36f4effa1c1a4501` = wave-1 deliverable `/fast/scratch/hyaku/kake-r39a3w1/CtlStdlibConvenience/control.py` (same hash; `diff` empty → L1 copied the seat's bytes verbatim).
- The seat report's fenced `exec('''…''')` literal decodes (`ast.literal_eval`) to byte-identical source, sha `a1b61e4c…` — report text encodes exactly the materialized file.
- Tweak clause N/A: `/fast/scratch/hyaku/kake-r39a3w1/CtlStdlibConvenience/l1-materialized.diff` does not exist; control differs from `dead-w1/CtlShallowStdlib.py` (239 vs 292 lines, sha `0aee6bca…`) — fresh write, no changed-line budget to count.

## Residual risk and verification gaps
- No defect found in the control beyond its declared shortcut; structural checks (root/entries/fields/scope/limits/manifest, `CtlStdlibConvenience.py:115-239`) agreed with the contract on my inputs.
- `lsp` device unavailable in this seat's tool inventory — caller/diagnostic checks were text-level; moot here (standalone control, no callers).
- Untested: error-precedence paths (encoding/doctype/xml_malformed), 50,000-entry and 50MB limits — outside my 3-input scope; the seat's fixtures cover them only as unexecuted fixtures.
- The over-trim shortcut propagates wherever `element_value` feeds `loc_too_long` and scope checks; only `loc_not_absolute` was demonstrated end-to-end.
- No tools installed or updated (host python3 3.14.8 sufficed); all child processes reaped (`subprocess.run`, nothing long-lived).
