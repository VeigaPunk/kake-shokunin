# FixDocsEvidence — round-23 residual review

## Findings, by severity

**No actionable contradiction found in the five assigned post-wave-2 documentation/evidence fixes.** No P1/P2/P3 finding is recommended. This is a scoped review recommendation, not admission, integration, or publication approval.

Reviewed the working-tree changes relative to pre-fix commit `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`, under the frozen round-23 contract. Axes: source-pointer accuracy, solidus-rule precision, counter-authority honesty, historical recipe reproducibility, and CLI synopsis consistency. No broad lane audit was performed.

## Checked behavior and evidence

### 1. Lesson S030/S031 digests and quote URL

Paths: `corpus/lessons/round-23.md:56-65,121-125`; `corpus/SOURCES.md:38-39,67`.

Public GETs of the two primary source pages returned the exact full response-body digests corresponding to the corrected lesson prefixes:

```text
04b65bf0b4b5f3bb3815999ab499af980fa09b8832f02c1686c544ab8e79a52d  syntax.html
 a11dcf1768a76e24cdf7e16060f54bcb149c529aa8bcb9297b8d1ab633b26f13  parsing.html
```

The leading space on the second line above is formatting only. Body sizes were respectively 89,196 and 826,255 bytes. Both pages state `Living Standard — Last Updated 20 October 2026`.

A local `html.parser.HTMLParser` probe collected heading IDs and text through the next heading of equal/higher rank. After whitespace normalization:

- S030's exact quoted sentence was present inside `syntax.html#start-tags`: `On void elements, it does not mark the start tag as self-closing but instead is unnecessary and has no effect of any kind.`
- S031's exact quoted sentence was present inside `parsing.html#parsing-main-inbody`: `Insert a foreign element for the token, with SVG namespace.` The following sentence handles the token's self-closing flag.

Thus the corrected digest pairing and the lesson's quote-specific `inbody` URL agree with the fetched source. The immutable S031 registry row still links `inforeign`, but explicitly covers **both** the in-body svg/math rule and foreign-content processing. That broader registry link does not contradict the narrower lesson quote location.

### 2. Unquoted-attribute solidus caveat

Paths: `corpus/SOURCES.md:92`; `corpus/knowledge/static-canonical-preflight.md:149-151`; `corpus/lessons/round-23.md:121-125`; `scripts/canonical_audit.py:157-180,299-308`.

All three new explanations distinguish a separate trailing solidus from a slash attached to an unquoted attribute value. The primary source immediately after S030's quoted sentence says:

> For such void elements, it should be used only with caution — especially since, if directly preceded by an unquoted attribute value, it becomes part of the attribute value rather than being discarded by the parser.

Three end-to-end manifest probes against the current working-tree validator agreed with the caveat:

| HTML within the explicit head | expectedCanonical | Observed exit / result |
|---|---|---|
| `<link rel=canonical href=/x/>` | `https://example.test/x/` | `0`, clean, no findings |
| `<link rel=canonical href=/x/>` | `https://example.test/x` | `1`, failed-policy, `canonical_mismatch` |
| `<link rel=canonical href=/x />` | `https://example.test/x` | `0`, clean, no findings |

The earlier shorthand about self-closed void tags is explicitly qualified by the new clarification, including the statement that this is not XML-style self-closing. No opposing behavior was observed.

### 3. C1 counter authority limit

Paths: `corpus/lessons/round-23.md:111-115`; `corpus/QUALITY.md:145-154`; `.ufo/waves/round-23/measure_c1.py:36-95,98-122`; contract C1 limits.

The lesson now explicitly says that structure/anchors/correction placement are checked, an asserted GET/HOLD is not authenticated, a forged self-consistent receipt can pass, and seat observations plus non-author spot-check carry the evidentiary authority. QUALITY independently states the same boundary.

The actual counter's `check_unit()` reads receipt/base/current blobs and validates fields, labels, anchors, citations, corrections, reasons and the presence of a HOLD/STALE label; it does not issue the claimed surface GET or verify observation truth. Its returned counts therefore match the newly disclosed authority boundary. No counter result is treated here as proof of freshness.

A tally of **only the 17 units named by c1-population.json**, rather than all JSON files in receipts/, yielded:

```json
{"units":17,"rows":176,"verdicts":{"HOLD":79,"STALE":55,"UNVERIFIABLE":42}}
```

This agrees with the current lesson's measurement summary. The apparent 171/168 difference is also explained in the lesson: 171 wave-1 candidates, three rejected anchors, 168 admitted rows, then eight added claims = 176. The all-UNVERIFIABLE restriction is disclosed in the lesson and counter docstring, not presented here as an unchanged original contract predicate. I did not rerun the C1 counter or independently authenticate the 176 observations.

### 4. Round-22 after-runner git-show recipe

Paths: `.ufo/waves/round-22/postfix/REPRODUCE.md:19-28`; `defect-probe-after.json:1-3,122-123`; `defect-probe.py:46-114`.

The retained after receipt names the mutable lane validator path, as the new note states. Historical probes used a fresh `git clone --no-hardlinks` under the review scratch directory, not historical runner execution in the live checkout.

Observed:

```text
b539cc1 round-22: recovery fixes for wave-2 defects in canonical preflight and counter
b539cc1 IS ancestor of the cloned HEAD
b539cc1 scripts/canonical_audit.py sha256:
5de32200ea409349659180ab93d02d273c113008596d93834da94ef1c04a1c15
current working-tree scripts/canonical_audit.py sha256:
23638a87dba90f151bc65ed220983ab948989a5dfadf64f62469ceeabe45d0a4
```

The blob extracted from `b539cc1` was passed to the current retained round-22 defect probe, with temporary fixtures confined below the review scratch directory. Exact summary: **exit 0, passed true, met 8, total 8, empty stderr**. Every case had `ok:true`; actual exits were:

```text
network_path_empty_authority 1
base_empty_authority         1
repeated_manifest          64
usage_error_json           64
manifest_symlink            2
caller_prefix_control       0
clean_control               0
dotdot_after_symlink        1
```

The documented `5de32200…` and `8/8` are reproduced. `$T` is initialized in the preceding recipe block; the after section reuses it. The current worktree is correctly distinguished from the historical content address.

### 5. Current SKILL contract, help synopsis and usage errors

Paths: `SKILL.md:394-416,480-490`; `scripts/canonical_audit.py:78-81,119-134,1024-1036`.

The canonical-audit help and usage-error paths now emit the identical synopsis:

```text
usage: canonical_audit.py --manifest PATH [--json] | --selftest | -h | --help
```

Observed current CLI results:

| Arguments | Exit | Observable contract |
|---|---:|---|
| `--help` | 0 | Standard help; both aliases in synopsis/options; no publishing JSON verdict; stderr empty |
| `-h` | 0 | Identical help; stderr empty |
| no arguments | 64 | Error and same synopsis on stderr; one could-not-evaluate JSON object on stdout |
| `--bogus` | 64 | Same usage contract |
| `--selftest --json` | 64 | `--json is only valid with --manifest`; same usage contract; selftest not executed |

Exact stdout for the three usage-error probes:

```json
{"findings":[],"pagesChecked":0,"verdict":"could-not-evaluate"}
```

This agrees with SKILL's canonical-audit usage-error map. The original help-alias discrepancy in `w1/ReviewHelpSynopsis.md` is absent in the current code. As an additional synopsis-only check of the current SKILL evidence-tool row, `live_snapshot.py --help` exited 0 with `--population`, `--out`, `--reaudit` and optional `--validator`; no arguments exited 64. Neither invocation fetched or wrote a snapshot.

## Commands, probes and outputs ledger

Scratch root: `/tmp/kake-r23res-FixDocsEvidence-a1b2` (`S` below). Lane root: `/home/vgpnk/Projects/shokunin/kake-shokunin` (`R` below).

- Initial read-only discovery: `GIT_OPTIONAL_LOCKS=0 git diff 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd --stat` and scoped diffs of the assigned documentation/validator paths. No Git/JJ mutation was performed in the live lane.
- Historical clone: `git clone --no-hardlinks --quiet /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r23res-FixDocsEvidence-a1b2/clone`.
- Source captures: `curl -s --max-time 60 https://html.spec.whatwg.org/multipage/syntax.html -o /tmp/kake-r23res-FixDocsEvidence-a1b2/syntax.html` and `curl -s --max-time 120 https://html.spec.whatwg.org/multipage/parsing.html -o /tmp/kake-r23res-FixDocsEvidence-a1b2/parsing.html`, followed by `sha256sum` of both captures. Exact hashes and sizes are above.
- Historical extraction: subprocess argv `git -C "$S/clone" show b539cc1:scripts/canonical_audit.py`; captured stdout was materialized as `$S/canonical_audit_b539cc1.py` with Eval's write helper.
- Historical recipe probe: `/usr/bin/python -B "$R/.ufo/waves/round-22/postfix/defect-probe.py" --validator "$S/canonical_audit_b539cc1.py"`, with `TMPDIR="$S"`, `PYTHONDONTWRITEBYTECODE=1`, cwd `$S`; observed `0 / 8 / 8` as detailed above.
- Current CLI probes: subprocess argv `/usr/bin/python -B "$R/scripts/canonical_audit.py"` plus each argument list in the table; and `/usr/bin/python -B "$R/scripts/live_snapshot.py" --help` / no arguments. Outputs are above.
- Solidus probes: generated one HTML file and v1 manifest in a `solidus-*` temporary directory below `$S`, invoked `/usr/bin/python -B "$R/scripts/canonical_audit.py" --manifest <absolute-scratch-manifest> --json` for the three table rows, then removed those generated fixture files with the temporary-directory context. No source file was edited.
- Analytical Python Eval probes parsed the saved HTML using HTMLParser, selected sections by actual heading ID/rank, normalized whitespace and tested exact quote membership; both checks returned true. A separate population-driven receipt tally produced the 17/176/79/55/42 output above.
- Initial exploratory quote lookup assumed quoted `id="..."` attributes and failed because these source pages use unquoted IDs. That empty result was not treated as anchor absence; the successful HTMLParser probe replaced it. An initial all-files receipt tally encountered the non-object rejected-row JSON; the final tally followed the canonical population instead.

## Reviewed working-tree identities

SHA-256 observed during this review (later integrator changes are not covered):

```text
8cf96f96512f64761559adefa5b7197fb7e03ff8a13a50e5d79dbb6cd47e36ac  corpus/lessons/round-23.md
53045db04b16b60d1aba4afbcb3eacbb1a05e110bc7ea277ca5425594840f1c2  corpus/SOURCES.md
79d40b43f6e4ab9a7c66cefb0ed34e6d918bdd1db2f0da1aa001c031470766e6  corpus/knowledge/static-canonical-preflight.md
8e5a050738466212cc7606f0dda0c8a4c21f97347d919539c26c904bbbab11fa  corpus/QUALITY.md
ee4981ebd0409cb94d948524ff59b1c76ee3ff4417b97cb93823b378edc85d5c  .ufo/waves/round-22/postfix/REPRODUCE.md
e9d999967175650abb45ac8ea4568d3cdc2835ad4627702887809a9f7ee9ea66  SKILL.md
23638a87dba90f151bc65ed220983ab948989a5dfadf64f62469ceeabe45d0a4  scripts/canonical_audit.py
c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5  .ufo/waves/round-23/measure_c1.py
```

## Residual risk and verification gaps

- `read xd://lsp` returned **No such tool: xd://lsp**. No LSP server/status/references/definition/diagnostics route was available; no empty cold result was counted as absence. Literal searches located text only and are not semantic caller proof. The conclusions above rely on direct definitions, primary source bytes, and narrowly exercised behavior.
- Source fetches establish the cited bytes/date and quote locations at this review time, not future Living Standard stability. They do not authenticate the historical seat invocations.
- The C1 truth/GET/HOLD authority gap remains a disclosed limit, not a property solved by the counter. This report supplies no non-author closure for all underlying freshness claims.
- No builds, lint, formatters, full selftests, measurement suite, publishing/account operations, deployment changes, or host/package/service changes were run. Only the named targeted probes were exercised. No tool was installed or updated.
- Runtime routing/saturation, resume continuity, the rest of C2, and other lane behavior were outside this narrow assignment. No replacement for dead seats, broad review coverage, integration, or independent admission is claimed.
