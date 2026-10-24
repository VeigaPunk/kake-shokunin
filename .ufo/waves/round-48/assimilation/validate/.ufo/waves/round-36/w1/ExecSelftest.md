# ExecSelftest — independent selftest for C1's tool (round 36, wave 1)

Seat: KakeR36.ExecSelftest. Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Built from the public C1 contract only (`SCORECARD.md`, "Round 36 — declared claims", C1
contract, at `cd3212796cab7a2afa03b638dbfafe7194df9629`). The builder's tool was not read and
was not waited for.

## What I built

`/fast/scratch/hyaku/kake-r36w1/ExecSelftest/source_recheck_selftest.py` (915 lines, sha256
`9db94fec7e575c455bcb50a02dd448dd1a453672bdac6f57479b4092856cd6d3`) — to land as
`scripts/source_recheck_selftest.py`.

Shape follows `scripts/link_preview_selftest.py`: `python3 scripts/source_recheck_selftest.py
[--tool PATH]` writes fixtures into a temp dir, runs the tool as a black box, prints one JSON
summary with `passedOverTotal` and `verdict`, exits 0 only when every fixture passes, 1 on any
failure, 2 when it cannot evaluate (tool missing, fewer than 40 fixtures).

**101 fixtures** (requirement: ≥40, ≥4 per contract bullet plus verdict, exit-64 usage and
output-shape). Each fixture carries the contract sentence it tests in a `contract` field; the
sentences are quoted verbatim in the module docstring. Per bullet: (a) 8, (b) 11, (c) 10,
(d) 7, (e) 8, (f) 16, (g) 28, verdict 5, exit-64 usage 4, output-shape 4.

Judging mirrors the frozen counter (`sealed_count.py:judge`, lines 129-146): exit code, report
`verdict`, and the multiset of findings projected on (check, reason), with `target` compared
only for `moved`. `checksEvaluated` and field order are judged separately and only where the
contract pins them. The selftest also checks the report is one JSON object with `version == 1`,
that every finding has a string `reason` from the contract's reason set, and that the tool
**writes no files** (snapshot of the work tree before/after each run).

## Contract ambiguities I found, and how the selftest handles them

Three places in the public contract admit two readings. The selftest does not silently pick
one; it accepts either, and says so in its docstring:

1. **Hop `location` presence.** The manifest paragraph lists a hop as `{"status": …, "location":
   <string>}` but the prose requires a location only for a redirect hop. Every fixture carries a
   benign `"/final"` location on non-redirect hops, which satisfies both readings;
   `g19-redirect-hop-without-location` and `g28-final-hop-without-location` probe them.
2. **Hop chain shape.** "every hop but the last is a redirect and the last is not" is stated as
   a manifest rule, so violating it reads as `check_invalid`; a lenient tool would just
   evaluate the last hop. `a08-final-hop-is-a-redirect` and `g22-non-final-hop-not-a-redirect`
   accept either.
3. **Missing `--manifest` file.** "unreadable … manifest" reads as `input_invalid` (exit 2);
   a tool may treat a nonexistent path as a usage error (exit 64). `g05-manifest-file-missing`
   accepts either.

The sealed key is unaffected by these: the counter only compares exit, verdict and findings, and
these tolerances are on fixtures I wrote, not on sealed cases.

## Evidence — exact commands and exit codes

Sandbox `/fast/scratch/hyaku/kake-r36w1/ExecSelftest/`. `TMPDIR` exported there; every run
capped by `timeout 300`; no network; no process left running.

**A. The selftest passes on a contract-faithful tool.** I wrote my own reference implementation
from the contract alone (`reference.py`, mine, not the builder's) to prove the fixtures are
satisfiable — otherwise a selftest that always fails would be worthless.

```
$ timeout 300 python3 -B source_recheck_selftest.py --tool reference.py
{"cases": 101, "failed": 0, "failures": [], "passed": 101, "passedOverTotal": "101/101",
 "selftest": "kake-r36-source-recheck-selftest",
 "tool": "/fast/scratch/hyaku/kake-r36w1/ExecSelftest/reference.py", "verdict": "clean"}
exit=0
```

**B. The selftest fails, with named failures, on a deliberately wrong tool.** `toy_wrong.py`
(raw UTF-8 substring match, no HTML rules, no media-type rules, no decoding rules, no redirect
rules — it never emits `moved`).

```
$ timeout 300 python3 -B source_recheck_selftest.py --tool toy_wrong.py
verdict: failed  passedOverTotal: 42/101  failed: 59
exit=1
```

Named failures on stderr (59 cases; sample, verbatim):

```
FAIL b01-301-permanent-moved
  - exit mismatch: expected one of [1], observed 0 (stderr: )
FAIL b06-leading-permanent-run-target-is-last-permanent-hop
  - exit mismatch: expected one of [1], observed 0 (stderr: )
FAIL b10-moved-plus-final-status-outcome
  - accepted alternative mismatch: findings: expected [('"k1"', 'gone'), ('"k1"', 'moved', '"https://example.com/new"')], observed [('"k1"', 'gone')]
FAIL c01-script-contents-removed
  - exit mismatch: expected one of [1], observed 0 (stderr: )
FAIL d01-nfkc-fullwidth
  - exit mismatch: expected one of [0], observed 1 (stderr: )
FAIL e04-unsupported-media-type
  - accepted alternative mismatch: findings: expected [('"k1"', 'unsupported_type')], observed [('"k1"', 'quote_missing')]
FAIL f02-charset-windows-1252
  - exit mismatch: expected one of [0], observed 1 (stderr: )
FAIL g07-unsupported-charset-label
  - exit mismatch: expected one of [2], observed 0 (stderr: )
FAIL u02-usage-manifest-option-without-value
  - exit mismatch: expected one of [64], observed 2 (stderr: usage: toy_wrong.py [--manifest MANIFEST]
toy_wrong.py: error: argument --manifest: expected one argument)
```

Full transcript: `/fast/scratch/hyaku/kake-r36w1/ExecSelftest/toy.err`; summary
`toy.json`. The toy fails every redirect, HTML, media-type, decoding and input-fault family —
the families the round-35 controls could reach — while passing the 42 fixtures that only
exercise the plain "quote is a substring of a UTF-8 body" path.

**C. Other controls, to show the selftest discriminates and is not self-fulfilling** (each
`timeout 300 python3 -B source_recheck_selftest.py --tool <t>`):

| tool | result |
|---|---|
| `/tmp/const_clean.py` (constant clean) | failed 4/101, 97 failures |
| `/tmp/junk.py` (non-JSON stdout) | failed 0/101, 101 failures |
| `/tmp/noreader.py` (status+redirect rules only, never opens a body) | failed 48/101, 53 failures |
| `/tmp/writer.py` (writes `sidecar.txt`) | 94 failures all reading `tool wrote files: …` |
| `/tmp/mutant.py` (reference with the non-final-hop rule relaxed) | clean 101/101 — confirms the g22 tolerance path works and is not masking a defect |

**D. Default-tool-path resolution.** Copied to `scripts/` beside a `source_recheck.py`:
`timeout 300 python3 -B scripts/source_recheck_selftest.py` → `passedOverTotal 101/101`,
exit 0. So the file lands correctly as `scripts/source_recheck_selftest.py` and finds
`scripts/source_recheck.py` next to it with no arguments.

**E. Degenerate inputs.** `--tool /nonexistent.py` → `verdict could-not-evaluate`, exit 2.
`--list` prints every fixture name with its contract label.

## Fixture-to-contract map (summary)

- **(a) final status** `a01`-`a08`: 200 hold; 404 and 410 → one `gone`; 500, 204 (other 2xx),
  403 → one `http_error`; 200 with a missing quote → `quote_missing`; final-hop redirect →
  `check_invalid` (tolerant of `http_error`).
- **(b) redirects** `b01`-`b11`: 301 and 308 → one `moved` with the resolved target; 302, 303,
  307 → no `moved`; leading permanent run of two hops → target is the *last* hop of that run;
  permanent-then-temporary → only the leading run counts; leading temporary → no `moved` at
  all; relative location resolved per RFC 3986 (`/dir/page` + `other` → `/dir/other`); absolute
  location; `moved` alongside a `gone` outcome.
- **(c) HTML text** `c01`-`c10`: `script`, `style`, `template` contents removed; comments
  removed; tags removed, text kept; named, decimal and hexadecimal references decoded; `title`
  text kept; end-tag match case-insensitive; `application/xhtml+xml` uses the HTML rules.
- **(d) quote match** `d01`-`d07`: NFKC fullwidth and ligature folding; whitespace deleted from
  both sides (space, tab, newline, NBSP); case-sensitive; substring holds; absent quote →
  `quote_missing`.
- **(e) media types** `e01`-`e08`: `text/plain` body as-is (no tag stripping, no reference
  decoding); `application/json` and `image/png` → one `unsupported_type` and no quote check;
  media type ASCII case-insensitive; trimmed before `;`; `text/plain` with a charset parameter.
- **(f) decoding** `f01`-`f16`: UTF-8 BOM overrides a contradicting charset; `windows-1252`;
  `iso-8859-1`, `latin1`, `ascii`, `us-ascii` all mean windows-1252; `shift_jis` and `utf-16`
  → one `charset_unsupported` (exit 2); no BOM and no charset → UTF-8; charset value quotes
  removed; charset parameter name case-insensitive; UTF-16LE and UTF-16BE with and without BOM;
  invalid bytes → U+FFFD.
- **(g) input faults** `g01`-`g28`: non-JSON manifest, wrong version, `checks` not a list,
  non-object manifest, missing manifest file; missing/empty/non-string id; body path escaping
  the manifest directory, absolute, missing, or a directory; bad url scheme, relative url,
  empty host; empty/non-string quote; empty hops; redirect hop without location; status out of
  range; non-integer status; non-final hop not a redirect; missing body or contentType while the
  final status is 200; one invalid plus one valid check (the valid one still evaluated, and a
  second variant where the valid one also misses its quote).
- **verdict** `v01`-`v05`: clean; `failed-policy` on `unsupported_type`;
  `could-not-evaluate` on `check_invalid`, `charset_unsupported` and `input_invalid`.
- **exit-64 usage** `u01`-`u04`: no `--manifest`; `--manifest` without a value; unknown option
  with and without `--manifest`.
- **output shape** `o01`-`o04`: one JSON object; `checksEvaluated` over two clean checks; two
  findings each carrying its own check id; mixed clean and failing checks.

## Risks and blockers

- **The selftest is stricter than the sealed counter in one place**: it also judges
  `checksEvaluated`, the report `version`, the finding field types, the reason vocabulary, and
  "no files written". The contract pins all of these, and the counter deliberately does not
  compare them, so a tool can pass 28/28 sealed cases and still fail this selftest. That is
  intended for a selftest, but the L1 should not read a selftest failure as a sealed-case
  failure without checking which field is named in the message.
- **Fixture expectations for `target` on non-`moved` findings are not judged** — the contract
  does not say what `target` should be for `gone`, `http_error`, `quote_missing`,
  `unsupported_type`, `charset_unsupported`, `input_invalid` or `check_invalid`. The counter
  projects those to null and ignores them, and so does the selftest (only type is checked).
- **Three contract ambiguities remain open** (listed above). If the L1's private reference
  resolves them differently from both readings I allowed, the affected fixture will fail
  against a conforming tool. Those are `a08`, `g05`, `g22`, `g28` — 4 of 101.
- **`--manifest` with a missing value**: the contract says exit 64 on a usage error, but a tool
  built on `argparse` exits 2 by default. `u02` demands 64. The builder must map argparse's
  usage exit to 64 or the fixture fails; I flagged this because argparse's default would also
  fail the sealed cases if any exercise it.
- **Not verified**: I did not run the selftest against the builder's `scripts/source_recheck.py`
  (not yet present, and the assignment forbids reading it), so the selftest's compatibility
  with that specific implementation is unmeasured. The reference implementation I wrote is my
  own reading of the contract, not the builder's, so agreement between them is not evidence
  about the builder's tool.
- I did not touch the sealed tree at `/fast/scratch/hyaku/kake-r36/`, ran the counter, or
  modified any tracked lane file. No tool was installed or updated, so there is no install to
  record.

## Files

- `/fast/scratch/hyaku/kake-r36w1/ExecSelftest/source_recheck_selftest.py` — the deliverable
  (to land as `scripts/source_recheck_selftest.py`).
- `/fast/scratch/hyaku/kake-r36w1/ExecSelftest/toy_wrong.py` — the deliberately wrong tool used
  for the negative run.
- `/fast/scratch/hyaku/kake-r36w1/ExecSelftest/reference.py` — my contract-faithful reference,
  used only to show the fixtures are satisfiable. Not part of the deliverable.
- `/fast/scratch/hyaku/kake-r36w1/ExecSelftest/{ref.json,ref.err,toy.json,toy.err}` — run
  transcripts.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-36/w1/ExecSelftest.md` — this
  report.
