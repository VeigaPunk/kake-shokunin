# FidelityXsdTweak — wave-2 falsification review (leaf seat)

Verdict: **faithful shortcut** — the control deliberately skips its declared work (scope comparison, W3C lastmod profile), implements no forbidden technique, and the L1 materialization is byte-for-byte faithful.

## 1. Materialization checks (all passed)
- `sha256sum` base `a3-controls/dead-w1/CtlXsdDelegate.py` = `72a614fc9adf992877cd40f24ee8d59e8bd46f4a4071ae968d5250dfaa5bfa14` (matches wave-1 report's claim).
- Fleet `a3-controls/w1a3/CtlXsdTweak.py` = `3c1b5948236753e83e39e95cf71d541b22197f4964b76d22f3565108da3e320e`; L1 scratch `/fast/scratch/hyaku/kake-r39a3w1/CtlXsdTweak/control.py` identical (`cmp` exit 0).
- `cp base.py patched.py && patch -s patched.py < l1-materialized.diff` → exit 0; `cmp patched.py control.py` → exit 0. Base + diff = control bytes.
- Report fenced diff block extracted (python `re`) and byte-compared to `l1-materialized.diff` → equal (sha `daa03820b5f2c7d9cbbed1217f0951fb3db07bc21f10250a94550e21784f4496`).
- Receipt `verification/a3/w1a3-CtlXsdTweak.json` (totals only): label=w1a3-CtlXsdTweak, passed=20, met=false, toolSha256=3c1b5948… ✓.

## 2. Shape hygiene
- No forbidden imports: no lxml/xmlschema/requests/socket/urlopen; `lxml` appears only in a docstring (control.py:216). Imports are stdlib + `subprocess`→`/usr/bin/xmllint` (libxml2 2.15.4, present).
- Diff size: 44 deleted + 2 added = 46 nonblank +/- lines — matches wave-1 report's static count.
- Skipped work really skipped: `loc_out_of_scope` appears only in docstring (control.py:12), no code path emits it; lastmod value decided solely by xmllint XSD oracle (`Oracle.value_valid`, control.py:316–329). Both declared gaps confirmed.

## 3. Disagreement runs (3 contract inputs, exit codes shown)
Setup: manifest + sitemaps in `/fast/scratch/hyaku/kake-r39a3w2/FidelityXsdTweak/cases/`. Command: `timeout 120 python3 control.py --manifest manifest.json` → exit 1 (`failed-policy`), stdout one JSON.

- **D1 scope (contract 25 vs control):** `scope.xml` loc=https://example.com/a/c/page under sitemapUrl=https://example.com/a/b/sitemap.xml. Contract ⇒ `loc_out_of_scope`; control ⇒ `"status":"clean"`. Control misses a real violation.
- **D2 lastmod over-strict:** `nosec.xml` (`2026-10-23T12:34Z`) and `off15.xml` (`2026-10-23T12:34:56+15:00`) are contract-valid (sentence 28: hh 00–23, mm 00–59, TZD allowed — no offset bound). Nonmllint against embedded schema rejects both (exit 3); oracle probes False; control reports `lastmod_invalid`. Control invents violations.
- **D3 lastmod under-strict:** `notzd.xml` (`2026-10-23T12:34:56`, no TZD) — contract-invalid (28 requires TZD when time present), XSD-valid (xmllint exit 0, oracle True); control ⇒ clean. `datetz.xml` (`2026-10-23Z`) likewise XSD-valid/contract-invalid. Control misses violations.

## Per attacked statement
- Keeps named shape (XSD-expressible rules only, 20): **holds**.
- Skips the work its shape says it skips: **holds**.
- L1 materialized seat's text byte-for-byte: **holds**.
- Control must disagree with a correct tool on 3 contract inputs: **holds** — three distinct disagreement classes demonstrated (D1–D3).

## Findings (by severity)
1. [Expected divergence, verified] Scope rule (h) unimplemented — control.py:426 comment; D1 proves clean verdict on an out-of-scope URL.
2. [Expected divergence, verified] lastmod delegated to `xsd:date|xsd:dateTime` union — control.py:94–101/199–206, 316–329; D2 proves false `lastmod_invalid` on contract-valid values; D3 proves clean verdict on contract-invalid values.

## Residual risk / gaps
- Sealed key/rows not read (bounds); counter not run; receipt rows/why not read.
- `xmllint` absent ⇒ fail-open (mode None ⇒ value_valid True) — observed statically only, not exercised.
- No tools installed (tooling directive record: none).
