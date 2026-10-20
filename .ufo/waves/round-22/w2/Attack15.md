# Attack15 — frozen case `duplicate_different` (r22 wave2 falsification)

Seat: KakeR22.Attack15 (author-side falsifier, leaf). Lane root:
`/home/vgpnk/Projects/shokunin/kake-shokunin`.
Frozen candidate under test: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`
(`scripts/canonical_audit.py`, sha256 `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7`).
No production file was edited; writes went only to `/tmp/kake-r22-attack15/` and this report.

## Axes
- Correctness: exit/id for `duplicate_different` against the frozen contract and case table.
- Boundary sharpness: does the duplicate rule count only active canonical links inside the
  explicit `head`, and does a body duplicate get the dedicated `canonical_outside_head` id.
- Operability: public CLI is runnable, deterministic, and honors the exit map.

## Independent derivation (before observing output)
Sources: `.ufo/waves/round-22/contract.json` policy clause and exit map;
`.ufo/waves/round-22/cases.json`; `scripts/canonical_audit.py` parser/policy code.

- Contract policy: "Exactly one canonical link in explicit head per page, rel ASCII
  case-insensitive token list". Exit map: `0` clean, `1` failed policy, `2` could-not-evaluate
  input/unsupported shape, `64` usage.
- Frozen fixture `.ufo/waves/round-22/fixtures/duplicate_different/page.html` (183 bytes) has
  two `link` elements in `head`, both `rel="canonical"`, with different `href` hosts:
  `https://example.test/project/a.html` and `https://wrong.test/project/a.html`.
- `cases.json` freezes `expectedExit: 1`, `expectedFindings: ["canonical_multiple"]`, rationale
  "reject multiple canonical links even when their destinations differ".
- Candidate structure agrees: `CanonicalHTMLParser` records every canonical link seen while
  `head_open` into `head_canonicals`; `evaluate_page` checks `len(head_canonicals) > 1` and
  returns `canonical_multiple` before any href/URL comparison; `audit_manifest` maps any
  non-input finding to `failed-policy`/exit 1.

Derived expected result: stdout JSON `verdict=failed-policy`, `pagesChecked=1`,
one finding `{"id":"canonical_multiple","page":"https://example.test/project/a.html"}`,
process exit `1`.

## Frozen-case run (exact commands)
```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 .ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case duplicate_different
```
stdout (`MATRIX_EXIT=0`):
```
PASS caseId=duplicate_different exit=1 findings=canonical_multiple
SUMMARY selection=duplicate_different accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```
```
python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/duplicate_different/manifest.json --json
```
stdout (`EXIT=1`):
```
{"findings":[{"id":"canonical_multiple","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```
The same output and exit 1 were observed without `--json`. Cross-check of the integrated record
`matrix-integrated.json` (nested stdout): same PASS row, `expectedFindings`=`actualFindings`=`["canonical_multiple"]`.

## Nearest-neighbor fixture (own `/tmp` tree)
```
/tmp/kake-r22-attack15/neighbor/manifest.json  sha256 5ca6750bf00571943989846490462ca7bbcf372d1ca0c357145a1abc10971423
/tmp/kake-r22-attack15/neighbor/page.html      sha256 92e0f39bb62a68580df79c60adc5422bbfd93c757c65a571dd7001171d530f0b
```
`manifest.json` is byte-identical metadata to the frozen fixture:
`{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}`
`page.html` moves the second, differently-targeted canonical out of `head` into `body`:
```
<!doctype html><html><head><link rel="canonical" href="https://example.test/project/a.html"></head><body><link rel="canonical" href="https://wrong.test/project/a.html"></body></html>
```
Independent derivation: the explicit head still contains exactly one canonical link, so the
multiple rule must not fire; the second canonical is outside the head, so the dedicated
finding is `canonical_outside_head` (contract findingIds + `cases.json` body_link rationale),
exit 1. If the implementation counted all canonical links regardless of location it would
wrongly report `canonical_multiple`, which this probe discriminates.

```
python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack15/neighbor/manifest.json --json
```
stdout (`EXIT=1`):
```
{"findings":[{"id":"canonical_outside_head","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```
Matches the independently derived id and exit: the duplicate rule is correctly head-scoped.

## Controls
- Clean positive control in the same tree (`/tmp/kake-r22-attack15/control/`, one matching
  canonical in head): stdout `{"findings":[],"pagesChecked":1,"verdict":"clean"}`, exit 0.
  Confirms the CLI distinguishes clean from both probes without a shared failure mode.
- BEFORE revision: `git cat-file -e 7c61c8cc...:scripts/canonical_audit.py` → fatal "exists on
  disk, but not in '7c61c8cc...'" (exit 128), i.e. no lane validator at base.
- AFTER revision: `.ufo/waves/round-22/measure-after.json` records `sourceCommit`
  `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`, `deterministic: true`,
  `sameInstrumentAsBefore: true`, two runs both exit 0 with `"accepted": 32`; full integrated
  matrix is `accepted=32 total=32 executed=32 discrepancies=0 toolMissing=false`.

## Verdict
Claim **survives** for this case. Exit (1), finding id (`canonical_multiple`), verdict, page
field, and page count match the independent derivation; the head/body boundary neighbor is
classified correctly; no production bytes changed.

## Remaining unknowns
- The contract does not specify finding precedence when duplicate links also violate
  href/fragment/scheme rules. Implementation prefers `canonical_multiple` (count check first);
  defensible but an implementation-local ordering, not contract text.
- Clean output uses `findings: []`; `cases.json` expresses clean as `["clean"]`. The matrix
  runner normalizes this; representation, not a behavior gap.
- Scope remains static serialized HTML per contract limits (no JS/network/redirects/freshness).

## Tool installs
None. No pacman/uv/cargo/npm transactions; no services or credentials touched.
