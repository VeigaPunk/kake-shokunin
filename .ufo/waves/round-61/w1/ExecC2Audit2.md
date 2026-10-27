# ExecC2Audit2

Seat: claim C2 (operability), second independent implementation of
`scripts/header_audit.py` for differential comparison. Contract:
`.ufo/waves/round-61/contract.md` § Claim C2, read at base `9f07731a`; access date 2026-10-27.
Deliverable of record: `.ufo/waves/round-61/w1/ExecC2Audit2.files/header_audit.py` (1245 lines, sha256
`282d5b04676f2de1ee80fb360629c81dfbd15e0790b2033f53e1f85d741569b2`), retained run transcript at
`.ufo/waves/round-61/w1/ExecC2Audit2.files/evidence.txt`. I wrote my implementation to `scripts/header_audit.py`
(ready 06:11); the sibling `ExecC2Audit` then wrote its own to the same path, so the shared path today holds
**their** file: 48986 bytes, sha256 `01abd8d4ff628907713b4300adf26b5962924d85132d1f330a33b70110c1d1d4`, mtime
06:19:51 (an intermediate 46987-byte image with sha256 `b0129635…` was measured at 06:18 and is not the current
one). Both versions exist for the differential: the L1 should compare `.files/header_audit.py` (mine) against
`scripts/header_audit.py` (theirs, also preserved at `ExecC2Audit.files/`) and name the one that lands.
`scripts/response_snapshot.py`, the capture under `.ufo/waves/round-61/capture/`, the real manifest, and
`c61_header_cases.py` are other seats' files; I wrote none of them.

DESIGN:

- Two layers. `load_manifest` decides manifest-level usability only (unreadable, not JSON, not an object,
  `version` missing/not int/`!= 1`, `checks` not an array) → exit 2. Everything else is decided per check by
  `evaluate_check`, so a single bad entry never blanks the run.
- Evaluation is one pass over the recorded header pairs. Names are OWS-trimmed then ASCII-case-folded for
  matching and counting; values are OWS-trimmed (SP/HTAB only) and, for `nosniff`, ASCII-case-folded. The audit
  never fetches: no network module is imported, no subprocess, no environment read, no write.
- Classes implemented exactly as frozen, plus the two the case table forces: `content_type_present` (2xx only),
  `hsts_present` (`https: true` + declared flag), `xcto_nosniff_value`, `csp_present`, `singleton_fields`
  (`Set-Cookie` skipped even when listed), `field_name_syntax` (H12: name must be an RFC 9110 `tchar` token),
  `could_not_evaluate` (H13 and its siblings). Fixed within-check order: content_type, hsts, xcto, csp,
  singleton, field_name; checks keep manifest order. Output is `<check-id> <class> <detail>` per line then
  `checks=<n> findings=<k>`; `--json` swaps in one document carrying `verdict`, `items[]`, `findings[]`,
  `policyFindings`, `unevaluableChecks`.
- Four lane readings where the contract leaves a point open, all recorded in the tool docstring:
  1. `expect` flags gate their class; absent = false (contract H16 "declared false/absent"). `https` absent = false.
  2. A check fault (source missing/unreadable, receipt not JSON, no response object, status missing/unparseable,
     `headers` unusable, `expect`/`singleton_fields` wrong type) yields exactly one `could_not_evaluate` line for
     that check and nothing else for it; the run is exit 1, never exit 2. Exit 2 is manifest-only, i.e. the case
     where no check is enumerable, which is how the contract's parenthetical and H13's exit 1 both hold.
  3. `findings=` counts every emitted line including `could_not_evaluate`; the "0 policy findings" reading of H13 is
     available exactly as `findings=1` with `policyFindings=0` in `--json`, since the class name says which it is.
  4. `source` resolution: absolute as written → `--root` → nearest `.git`/`.jj` ancestor of the manifest (lane
     root) → each ancestor of the manifest directory nearest-first → cwd; first existing regular file wins. This
     satisfies both peer pins received during the wave: `ExecC2Manifest` (lane-root-relative
     `.ufo/waves/round-61/capture/<id>/response.json`) and `ExecC2Counter` (`--root` else manifest dirname). The
     ancestor walk makes it work without a VCS marker, so gate-built fixture roots resolve too.
- Receipt reading is liberal inside the frozen shape because the recorded-response key names are not frozen:
  `status`/`statusCode`/`finalStatus`/`httpStatus`/`code`; `headers`/`responseHeaders`/`headerPairs`/`header_pairs`
  as `[name, value]` pairs, `{"name","value"}` objects, `"Name: value"` strings, or a `{name: value|[values]}`
  object; one-level wrappers `response`/`capture`/`recorded`/`snapshot`/`receipt`. Order and duplicates survive
  every form except the single-value object form. A receipt whose first lines are `# receipt: ...`/blank before
  the JSON body parses (S1), so a receipt-grammar capture stays auditable; the raw-decode fallback is capped at
  256 attempts and all reads are bounded (8 MiB) and require a regular file, so a FIFO cannot block.
- CLI: `--manifest PATH` (also `--manifest=PATH`, and one bare positional), optional `--root DIR`, `--json`,
  `--selftest`; `--selftest` rejects any other argument with 64; anything else → 64 before any read.

SELFTEST:

Run and observed (transcript in `.files/evidence.txt` §1):

```
$ python3 -B scripts/header_audit.py --selftest
selftest: cases=29 passed=29 failed=0        # exit 0
```

29 cases: all 18 contract H-fixtures (H13 exit 1 + one `could_not_evaluate`; H14/H15 exit 2; H10 `Set-Cookie`
twice → clean; H11 404 without Content-Type → clean; H12 `X Bad Name` → one `field_name_syntax`; H17 OWS value →
clean; H18 `checks=0 findings=0`), six extra shape cases (S1 receipt header line, S2 object headers + string
status, S3 undeclared HSTS on an https check, S4 unreadable `headers`, S5 unparseable status, S6 one clean + one
missing source → exit 1 with one `could_not_evaluate`), and five CLI usage probes (empty argv, unknown flag,
missing flag value, `--selftest --manifest x`, nonexistent manifest → exit 2). Each fixture case also asserts the
summary line and that emitted finding lines == `findings=`.

Additional behaviour checks I ran (evidence §2–§5), all offline on scratch fixtures:
- lane-shaped 12-check manifest with one `Content-Security-Policy` deliberately removed, run from cwd=/tmp with no
  VCS marker: `checks=12 findings=1`, one `csp_present` finding, exit 1, zero `could_not_evaluate` → all twelve
  repo-root-relative sources resolved by the ancestor walk.
- counter-shaped manifest at fixture root: identical result with and without `--root` (`checks=1 findings=0`).
- nested wrapper `{"recorded": {...}}` with status `200.0` and a decoy top-level `status`: clean, exit 0.
- two `Content-Type` + two `Set-Cookie` with both listed as singletons: exactly one finding
  `c1 singleton_fields field=content-type count=2`, exit 1.
- corrected capture shape pinned by `ExecC2Counter`/`ExecC2Capture-2` mid-wave (headers as ordered
  `{"name","value"}` objects, `"status": null` on one check, a duplicated `X-Content-Type-Options: nosniff`,
  `headerCount`/`contentType`/`bodyFile` siblings): `checks=12 findings=1`, the null-status check reports
  `could_not_evaluate status-unparseable`, `ds4cc-primary` (duplicate nosniff) stays clean, `policyFindings=0`,
  exit 1 — the shape and the null-status rule the counter pinned, with exit 2 untouched.

Not run (never claimed): no audit of the 12 real surfaces and no R3 run. `.ufo/waves/round-61/capture/` was absent
when I first observed it this wave and exists now (other seats' writes); I read none of the real capture or manifest
and ran the tool only over my own fixtures built to the pinned shape. No `c61_header_cases.py` execution. I did not
build `scripts/response_snapshot.py`, the capture, or any counter.

LIMITS:

- `findings=` counting `could_not_evaluate` is a reading, not a frozen sentence: a counter asserting `findings=0`
  on H13 while also requiring the per-check `could_not_evaluate` line would disagree. `--json` separates the two
  counts, so the differential reader can take either. `ExecC2Counter`'s pin ("could_not_evaluate is a per-check
  finding class") matches mine.
- Gating `content_type_present` and `xcto_nosniff_value` on their declared flags is inferred, not literal: the
  contract's sentences for those two classes omit the "with X: true" clause that `hsts_present`/`csp_present`
  carry. Uniform gating is what makes H16 and H1/H2/H7 consistent; the cost is that a manifest declaring
  `xcto_nosniff_value: false` with a recorded `X-Content-Type-Options: sniff` is reported clean. Flagged for the
  w2 critic as a contract-wording ambiguity, not a code defect. The counter's mid-wave pins (header objects,
  null-status rule) do not resolve it; [INFERENCE] that its H-fixtures declare the flags true where the class must
  fire — none of H1–H18 as written discriminates.
- Recorded-response key names and the `httpStatus`-style aliases beyond `status` are my acceptance set; they are
  wider than the frozen shape, so the tool cannot fail a real manifest on key naming, but it also cannot detect a
  capture that records headers under a name none of the aliases covers — that surfaces as `headers-missing`
  (`could_not_evaluate`), never as a silent clean.
- `field_name_syntax` validates the OWS-trimmed name only; it does not reject obs-fold, non-ASCII names beyond the
  token test, or duplicate `Content-Type`-style singleton violations not declared in `singleton_fields` — the
  contract's singleton class is declaration-driven by construction.
- One `singleton_fields` finding per offending field name (not per surplus occurrence) and one
  `xcto_nosniff_value` finding per offending occurrence: a counter that counts occurrences rather than fields
  would differ on a fixture with three identical duplicates.
- No credential, token, `op://` ref or private URL is printed by the tool or retained here; the audit reports only
  check ids, class names and header field names/values as recorded, and the details are ASCII-sanitized to one line.
- The `source-missing` detail echoes the manifest's `source` string; if a producer ever puts a sensitive path
  there, it lands in the output. The frozen convention (capture-relative path) is not sensitive.
- No tool was installed or upgraded for this seat; nothing outside `scripts/header_audit.py`, this report and my
  `.files/` directory was written. Scratch `/fast/scratch/hyaku/kake-r61/ExecC2Audit2/` is removed.

VERDICT: `scripts/header_audit.py` delivered to the frozen C2 shape (offline, five policy/syntax classes plus per-check `could_not_evaluate`, 0/1/2/64, `--selftest` 29/29); real-manifest audit, R3 and the counter were out of my scope and are unrun, not passed.
