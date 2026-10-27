# ExecC2Audit

Seat ExecC2Audit — round-61 kake wave w1, claim C2 (operability, capability acquisition), primary
implementation. Lane write (only one for this seat): `scripts/header_audit.py` (993 lines,
sha256 `01abd8d4ff628907713b4300adf26b5962924d85132d1f330a33b70110c1d1d4`). Evidence copies in
`.ufo/waves/round-61/w1/ExecC2Audit.files/`: `header_audit.py`, `selftest.out`,
`real-manifest-run.out`, `sha256.txt`. No tool installs or upgrades were needed (stdlib Python
only). No lane jj/Git mutation, no fleet-root write.

## DESIGN:

**CLI.** `header_audit.py --manifest PATH [--root DIR]` and `header_audit.py --selftest`.
`--help`/`-h` prints the usage block, advertises `--manifest` and `--root`, and exits 64 (the
contract's exit set is closed). `--json` is not implemented: stdout is the frozen text report only.
Repeated `--manifest`, `--manifest` + `--selftest`, a missing `--manifest`, a non-directory
`--root`, and any unknown flag are usage errors → 64.

**Manifest v1 (read).** Top level must be a JSON object with `version` exactly the integer `1`
(bool and `"1"` rejected) and `checks` a JSON array (absent is a fault). Faults raise exit 2:
unreadable, not a regular file (stat is followed, so a symlink to a regular file is accepted and a
FIFO/device is refused instead of blocking), over 8 MiB, not JSON, not an object, bad `version`,
non-array `checks`. Exit 2 therefore occurs only when no check can be evaluated. `checks: []`
reports `checks=0 findings=0` and exits 0.

**Per-check evaluation.** Each check is exactly one of clean / failed-policy /
could-not-evaluate. The audit resolves, in this fixed order, `id` (`id_invalid`), `expect`
(`expect_malformed`), `source` (`source_missing`), receipt readability (`unreadable_source`),
receipt JSON (`source_invalid_json`), receipt object (`source_not_object`), status
(`status_absent`/`status_unparseable`), headers (`headers_absent`/`headers_malformed`), and — only
when `hsts_present` is declared true — `https` (`https_unknown`); the first fault yields a single
`could_not_evaluate` line for that check, never combined with policy findings.

**Expectation classes implemented** (five contract bullets, plus the table's `field_name_syntax`):
- `content_type_present` — only when the recorded status is 2xx and no `Content-Type` field is
  recorded; detail `missing` (S433, RFC 9110 §8.3).
- `hsts_present` — only when the check declares `https: true` and `hsts_present: true` and no
  `Strict-Transport-Security` field is recorded; detail `missing` (S430, RFC 6797).
- `xcto_nosniff_value` — for each recorded `X-Content-Type-Options` whose value, after trimming
  spaces/tabs and case folding, is not `nosniff`; detail `value=<token>` (S432, WHATWG Fetch).
- `csp_present` — declared true and no `Content-Security-Policy` field; detail `missing` (S431).
- `singleton_fields` — a declared name occurring more than once, case-insensitively, among the
  recorded names; detail `duplicate:<name>` (S433). `Set-Cookie` is skipped unconditionally, so
  listing it can never fail a check.
- `field_name_syntax` — a recorded name that is not an RFC 9110 token (`[!#$%&'*+\-.^_`|~0-9A-Za-z]+`);
  detail `name=<token>` (S433). §C2's prose lists five classes but its case table H12 carries this
  one, so the table governs.

**Header/status reader.** Status accepts an integer or a three-digit decimal string in 100..599
(keys `status`, then `statusCode`, then `status_code`); JSON `null` (a transport failure) and every
other value are `status_unparseable`. Headers accept an array of `[name, value]` pairs (duplicates
preserved), an array of `{"name", "value"}` objects (the `response_snapshot.py` shape), or an object
mapping a name to a string or an array of strings; any other shape is `headers_malformed`. Names are
case-folded for matching with no OWS trimming (a stray space in a name is also a syntax finding);
values are compared after trimming only spaces and tabs.

**Source resolution.** Absolute `source` is used as given. Otherwise the first existing candidate
wins among `--root DIR`, the manifest's own directory, the current directory, and the nearest
enclosing directory holding `.git` — that last candidate is what makes the pinned lane-root-relative
capture paths (`.ufo/waves/round-61/capture/<id>/response.json`) resolve when the manifest path
alone is passed from anywhere. A candidate that exists but cannot be read as a regular file under
8 MiB is `unreadable_source`.

**Report.** One line per finding `<check-id> <class> <detail>`, then the summary
`checks=<n> findings=<k>` as the last line; nothing else on stdout. Findings follow manifest order
and, within a check, the class order content_type_present, hsts_present, xcto_nosniff_value,
csp_present, singleton_fields, field_name_syntax. `<detail>` is always a single whitespace-free
ASCII token (whitespace → `_`, non-printables dropped, 60-char cap, empty → `<empty>`), so each
finding line splits into exactly three fields. Exit 0 iff no finding line; 1 iff any finding,
`could_not_evaluate` included; 2 only for the manifest faults above; 64 usage.

**Offline by construction.** Standard library only; reads the manifest and the receipt paths it
names and nothing else; no network, no writes, no environment reads, and no subprocess in audit
mode (`subprocess` is imported and used only inside `--selftest`).

## SELFTEST:

`python3 -B scripts/header_audit.py --selftest` → `selftest: 64/64 passed`, exit 0, 1.8 s wall
(receipt: `.files/selftest.out`). It is black-box: every fixture is materialised in a fresh temp
directory and the tool is run as a subprocess on `--manifest manifest.json`; no audit function is
imported, so a CLI or exit-code break is caught.

Coverage (each line asserts exit code, the exact `(checks, findings)` summary, the class list,
and where named the detail token):
- Frozen cases H1–H18 with their contract expectations: clean 200; 200 without Content-Type;
  https without HSTS; HSTS with parameters (`max-age=…; includeSubDomains; preload`); `nosniff`;
  `NOsniff` + OWS; `sniff`; no CSP; duplicate Content-Type; duplicate Set-Cookie listed (clean);
  404 without Content-Type (clean); `X Bad Name: v` → `name=X_Bad_Name`; missing receipt →
  `could_not_evaluate source_missing` at exit 1; `version: 2` → 2; unparseable manifest → 2;
  every expectation absent → clean; OWS-padded `nosniff` → clean; empty checks → `checks=0
  findings=0` at exit 0.
- Reader/rules edges: lowercase recorded names; object-shaped headers; mapping-shaped headers with
  an array value counted as repeats; `https: false` suppresses HSTS; absent `https` derived from an
  `https://` url (finding) and from no url (`https_unknown`); status `"200"`, `"twenty"`, `null`,
  absent, and `999`; absent headers; scalar headers; receipt as a JSON array; receipt as text;
  `expect` as an array; `singleton_fields` as a string; a non-bool expectation flag; a check that
  is not an object (`check-1`); an id containing a space (`check-1`); three checks mixing
  clean/finding/non-evaluable in manifest order; a singleton name occurring three times → one
  finding; two duplicate singleton names → two findings in declared order; all checks
  non-evaluable → exit 1 with one line per check; two `X-Content-Type-Options` with one wrong; an
  OWS-only value → `value=<empty>`; two bad names → two findings; 301 with no headers; 204
  (2xx, so Content-Type is expected); an unknown `expect` key ignored; a lane-root-relative source
  under an enclosing `.git`; an absolute source; `--root` resolving a source outside the manifest
  directory; manifest missing; manifest is a directory; version `"1"`/`true`/absent; top-level
  array; `checks` not an array; four usage errors; `--help`; and the meta assertion that every
  emitted finding line has exactly three fields with the summary last.

**Real-manifest smoke run** (validation of the reader against the landed capture, not a counter
score and not a verdict on the claim): `python3 -B scripts/header_audit.py --manifest
.ufo/waves/round-61/capture/manifest.json` → exit 1, `checks=12 findings=13` — 12 ×
`csp_present missing` and 1 × `hsts_present missing` (ds4cc-primary). An independent re-read of the
same 12 receipts in a separate process reproduced exactly those 13 classes: no `content_type_present`
(all 2xx carry Content-Type), no `xcto_nosniff_value` (the three recorded values are `nosniff`), no
singleton finding (the only repeated name is `vary`, which the manifest does not declare), no syntax
fault. Receipt: `.files/real-manifest-run.out`.

## LIMITS:

1. `--root` is extra to the frozen CLI (`--manifest`, `--selftest`); added because ExecC2Counter
   pinned it and ExecC2Manifest pinned lane-root-relative sources. `--json` is deliberately absent.
2. Reading of a valid manifest whose every check is non-evaluable: exit **1**, with one
   `could_not_evaluate` line per check (H13's shape), not exit 2. Exit 2 is reserved for
   manifest-level faults. If the frozen counter reads the parenthetical "exit 2 only when NO check
   is evaluable" as covering this case, the two must be reconciled before version 1 freezes.
3. Unknown keys inside `expect` are ignored; a wrongly typed declared key makes the check
   `expect_malformed` (one line, no policy findings). Absent and `false` both mean "no expectation".
4. Only header names are syntax-checked; a value containing CR/LF/NUL is not flagged (the contract
   names only the field-name class).
5. `csp_present`, `singleton_fields` and `field_name_syntax` carry no status qualifier in the
   contract, so a 404 receipt without CSP is a finding (4 of the 12 real receipts are 404). This
   follows the frozen prose, not a judgement about 404 pages.
6. Tolerances beyond the pinned schema (status aliases `statusCode`/`status_code`, mapping-shaped
   headers, 8 MiB size cap) are lane choices; no fixture asserts them as faults.
7. Duplicate check ids are not deduplicated: each check is evaluated and reported independently, so
   two checks sharing one id yield two lines.
8. What this tool (and its selftest) does not test: whether the declaration policy is the right
   publisher policy (critic-owned), whether the capture itself is honest (sentinel-owned, receipts
   are sha256-pinned), and any live serving at audit time (offline by construction).
9. **Collision on the shared path.** `scripts/header_audit.py` already held ExecC2Audit2's
   independent 40210-byte draft (mtime 06:16) when this seat's write landed at 06:20. My copy is
   preserved at `.files/header_audit.py`; Audit2's draft cannot be recovered by me and must come
   from that seat. For the differential, L1 should compare the two `.files/` copies (or two
   extracted revisions), not the single lane path.

VERDICT: scripts/header_audit.py implemented to §C2 with all six classes, 64/64 black-box selftest, offline and network-free; real-manifest smoke run 12 checks / 13 findings recorded, not scored.
