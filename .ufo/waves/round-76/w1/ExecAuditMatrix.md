# ExecAuditMatrix — C2 frozen case matrix and its counter

Seat: `ExecAuditMatrix`, kake lane round 76, wave `w1`, attempt 1.
Lane base: `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`. Frozen terms: `contract.md` §C2 and
`amendment-2.md` (A1–A16). The case set was first derived from C2 alone, then every case class the
amendment decided (A1–A15) was re-derived under the amendment and the counter was moved to A16's
comparison rule; no case is scored under both term sets. No edits outside
`.ufo/waves/round-76/w1/ExecAuditMatrix/`; nothing committed, pushed or applied; the lane checkout was
read-only for this seat.

## 1. Delivered

| Path | sha256 |
|---|---|
| `.ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py` (29198 B) | `4958ede07559d15cfb95af57b99dcaee98883420a071847f78f02db248ad7756` |
| `.ufo/waves/round-76/w1/ExecAuditMatrix/cases/` (71 files) | aggregate `fa64d448331aa0b2ae4a851afd6e5815919320e8f1381ece0c35283d3bbd9fb5` |
| `consts/const_noop.py` | `4a3f76ee48bd2c9da3efd1c9fab67e41493302ad1bb61fd022690e4a137e6ef5` |
| `consts/const_always_clean.py` | `ebb2431f31afe2e4640f57928cc3d6430ada267af5829caa4edd834b4d2c2d7d` |
| `consts/const_report_all.py` | `d373d6185ceaceba5b5a6c5ad16bf20a3a9e26a5aa4215ffa78d7635cfd8a7bc` |
| `consts/const_empty_list.py` | `f0a4a921c899ac6d06c5af21788fd1be9f3c0d7cca523ad6635a7b00d808371c` |

The tool under test at measurement time was
`.ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py`, 59734 bytes, sha256
`0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac`.

Counter CLI (exit 0 met / 1 not met / 64 usage):

```sh
python3 -B .ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py \
  --root . --tool <path-to-hreflang-audit.py> --revision <rev> --work <dir> \
  [--cases DIR] [--consts DIR] [--min-decided N] [--timeout S] [--selftest]
```

## 2. Axes and moves

Axes, cheapest first: (A) how much of contract C2 + amendment 2 is decided by a case; (B) whether
the four degenerate constants are rejected; (C) whether the candidate tool decides the frozen cases
correctly; (D) whether any of that is reproducible byte-for-byte.

Moves kept because each improves an axis and harms none: one isolated fixture tree per case (A/C/D);
expected `{exit, ids}` multiset derived from a named contract/amendment sentence (A); the A16 report
shape as a hard precondition, so "prints nothing" can never score clean (B); one finding per
offending annotation with the A2 exceptions (C); a selftest that injects a deliberately wrong expected
verdict and a constant that passes everything (B/D).

## 3. Case set — 71 cases, 69 decided, 2 undecided

One JSON per case (`cases/<name>.json`): `name`, `decided`, `derivation` (the deciding sentence),
`manifest` v1, `files` (UTF-8 text, `{"b64": ...}` for raw bytes, `{"symlink": ...}` and `{"dir": ...}`
for the A15 path cases), `expected {exit, ids}` (ids as a multiset), and `note` when undecided.

Decided coverage (case names are literal file stems):

| Class | Cases |
|---|---|
| clean baselines | `clean-no-alternates`, `clean-reciprocal-pair`, `clean-mutual-triple`, `clean-self-only-two-tags`, `clean-http-scheme`, `clean-valid-tags-multi`, `clean-tag-case-uppercase`, `clean-xdefault-uppercase`, `clean-href-absent`, `clean-canonical-absent`, `clean-template-ignored`, `clean-math-ignored`, `clean-comment-script-ignored`, `clean-alternate-stylesheet`, `clean-entity-self`, `clean-url-normalized-self` |
| `hreflang_missing_value` | `missing-value-bare-alternate`, `missing-value-with-valid-self`, `missing-value-empty-attribute` |
| `hreflang_invalid_tag` | `invalid-tag-{underscore,trailing-dash,word,x-defaults,i-klingon,space,double-hyphen,padded,extlang,extension,sgn,grandfathered-oed,privateuse,singleton-extension,long-primary}` |
| `hreflang_relative_href` | `relative-href-{path,fragment,protocol-relative,mailto}` |
| `hreflang_duplicate_pair` | `duplicate-pair-{exact,case-folded,two-pairs,entity-decoded}` |
| `hreflang_multiple_xdefault` | `multiple-xdefault-pair` (two pages × two x-default links → four findings) |
| `hreflang_self_missing` | `self-missing-pair` |
| `hreflang_nonreciprocal` | `nonreciprocal-absent`, `nonreciprocal-different-tag` (two findings) |
| `hreflang_canonical_not_self` | `canonical-not-self`, `canonical-first-wins`, `canonical-with-hreflang` |
| `hreflang_external_target` (informational, exit 0) | `external-target-single`, `external-target-mixed`, `external-target-trailing-slash` |
| multi-finding | `multi-self-missing-and-nonreciprocal`, `multi-missing-value-and-invalid-tag` |
| scanner rules A13/A14 | `structure-rel-uppercase`, `structure-svg-selfclosed`, `structure-unquoted-attrs`, `structure-noscript` |
| input faults | `input-unreadable-missing-file`, `input-duplicate-url`, `input-url-not-absolute`, `input-two-faults`, `input-file-escapes-root`, `input-file-absolute`, `input-file-symlink`, `input-file-not-regular`, `input-shared-file`, `input-policy-and-fault`, `input-version-not-1` |

Undecided (excluded from decided/correct/wrong, never counted as a pass):

- `undecided-svg-template-crossing` — a `<template>` closed inside an `<svg>` subtree is decided by no
  contract or amendment rule (ScoutHreflangEdge row 72).
- `undecided-unreadable-undecodable` — neither C2 nor A15 states an encoding policy; `input_unreadable`
  is listed but not defined for bytes that are readable as some text, and HTML supplies a
  fallback-encoding algorithm. The contract gap is reported rather than charged to the tool.

Derivation calls that a reader should check against A2/A3/A15/A16:

- **`input-shared-file`.** A15: "Two pages may not share a `file`." The sentence sits in the
  input-fault block whose id vocabulary is closed (`input_unreadable`, `input_duplicate_url`,
  `input_url_not_absolute`); a shared file is neither a duplicate url nor a non-absolute url, so the
  fault is `input_unreadable`, emitted once for the offending (second) manifest entry under A2. The
  candidate tool and the reference both decide it exit 2 with one `input_unreadable`.
- **`hreflang_multiple_xdefault` granularity.** A2: a policy finding is emitted once per offending
  annotation, and the only once-per-page exceptions are `self_missing` and `canonical_not_self`;
  multiple_xdefault is not exempt, so every x-default link on a violating page is one finding. The
  fixture has two pages with two x-defaults each and expects four findings. ScoutHreflangEdge's §7
  skeleton phrases the same fixture as "one per page"; that phrasing conflicts with A2's exhaustive
  exception list, and A2 is the frozen text.
- **`invalid-tag-padded`.** `hreflang=" en "` fails the anchored frozen grammar (surrounding spaces),
  so it is `hreflang_invalid_tag`; A3 makes tag equality ASCII case-insensitive only, so the stripped
  form is not a duplicate of the page's `en` link.
- **`clean-url-normalized-self` / `external-target-trailing-slash`.** A3: scheme and host are
  lowercased, a trailing `/` is significant; the first is a self match, the second is outside the
  manifest and therefore informational.
- **`clean-entity-self` / `duplicate-pair-entity-decoded`.** A13 decodes character references before
  comparison; `&amp;` and `&` reach the same attribute value.
- **`canonical-first-wins` / `canonical-with-hreflang`.** A6 (first canonical in document order) and
  A7 (canonical carrying hreflang still counts) both produce a non-self canonical, so a
  last-canonical or hreflang-stripping implementation fails the case.

## 4. Counter semantics

For each case the counter builds `<work>/fixtures/<nn>-<name>/` from scratch (files, symlinks,
directories, `manifest.json`), runs the tool as

```sh
<tool> --manifest <fixture>/manifest.json --root <fixture> --json
```

with cwd `<work>/runs/<nn>-<name>/`, `TMPDIR=<work>/runs/<nn>-<name>/tmp` and
`PYTHONDONTWRITEBYTECODE=1`, then validates the A16 report object:

- parseable JSON object carrying `version`, `pages`, `findings`, `counts`, `exit`;
- `pages` is a count (or a list whose length is the count) equal to the number of manifest pages;
- `findings` is a list, `counts` is an object, `exit` is an int equal to the process exit code;
- finding ids are compared as a **multiset** (order ignored, multiplicity significant);
- **informational ids are compared**, not tolerated: A1 puts `hreflang_external_target` in `findings`
  and A16 compares finding ids, so the three external-target cases require that id while expecting
  exit 0.

A case is `correct` only when the exit, the report shape and the id multiset all match. A missing or
malformed report is a failed case. Undecided cases are skipped. Constants are run over every decided
case; `constants_failed=K/T` counts constants failing at least one decided case; a constant that passes
every decided case sets `matrix_defect=true` and `met=false`. The printed line is exactly

```
cases=N decided=M correct=C wrong=W undecided=U constants_failed=K/T met=<bool>
```

`met = (wrong == 0) and (decided >= --min-decided) and (constants_failed == T) and not matrix_defect`.

## 5. Selftest (`--selftest`)

11 checks, all green: truth-set 4/4; a stub that drops ids detected; an exit-flip stub detected; an
extra-id stub detected; a missing-id stub detected; a deliberately wrong expected verdict yields
`wrong>=1`; an undecided case is excluded and never scored; the no-op constant fails a policy case and
is not a matrix defect; an always-clean stub passes an all-clean case set and is reported as a matrix
defect; a fixture-mutating tool cannot leak into the next case's tree; two identical runs give the same
summary. Observed: `selftest 11/11 passed`, exit 0 (receipt `receipts/matrix-selftest.txt`).

## 6. Measurements

Commands and full stdout are in `receipts/`; the summary lines below are exact substrings of those
receipts.

Reference implementation (contract C2 + amendment 2, written for this seat because the wave tool did
not exist when the matrix was frozen; mirrored at `receipts/ref_hreflang_audit.py`):

```
cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true
```

exit 0 — `receipts/matrix-run-ref.txt`.

Candidate tool (the wave's `hreflang_audit.py`, sha256 `0762452f…`, 59734 bytes):

```
cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true
```

exit 0 — `receipts/matrix-run-execaudittool.txt`.

Constants, each run as the tool under test (full stdout in `receipts/const-<name>.txt`):

| Constant | Summary line | Wrong decided cases |
|---|---|---|
| `const_noop.py` | `cases=71 decided=69 correct=0 wrong=69 undecided=2 constants_failed=4/4 met=false` | 69 |
| `const_always_clean.py` | `cases=71 decided=69 correct=16 wrong=53 undecided=2 constants_failed=4/4 met=false` | 53 |
| `const_report_all.py` | `cases=71 decided=69 correct=0 wrong=69 undecided=2 constants_failed=4/4 met=false` | 69 |
| `const_empty_list.py` | `cases=71 decided=69 correct=22 wrong=47 undecided=2 constants_failed=4/4 met=false` | 47 |

Every constant is rejected. `empty_list` passes exactly the clean rows and the input-fault rows its
manifest validation covers; `always_clean` passes only the clean rows, so the two are distinguishable
on this matrix (unlike the scout's §1 warning, which applies only to a link-derived failure profile).
No constant passes the whole matrix, so `matrix_defect` is not raised.

## 7. Limits

- The matrix tests verdicts on fixtures only: no network, no live fetch, no rendering, and no claim
  about the real-input run (owned by `ExecAuditRealRun`).
- Usage-level argv (`--manifest` missing, `--selftest` without `--work`) is not exercised; those are
  tool-selftest cases, not manifest-driven fixtures.
- A16 is enforced as written, including `exit` equal to the process exit and `pages` equal to the
  manifest page count; the candidate tool satisfies this at the measured revision.
- The reference implementation is the matrix author's reading, not an independent second opinion; the
  candidate-tool run is the independent check, and both agree on all 69 decided cases.
- The two undecided classes above stay excluded; they are contract gaps, not tool defects.

## 8. Evidence index

| Receipt | Contains |
|---|---|
| `receipts/matrix-selftest.txt` | the 11 selftest checks and `selftest 11/11 passed` |
| `receipts/matrix-run-ref.txt` | full matrix stdout over the reference, summary line, exit |
| `receipts/matrix-run-execaudittool.txt` | full matrix stdout over the wave tool, its sha256/bytes, summary line, exit |
| `receipts/const-noop.txt`, `const-always-clean.txt`, `const-report-all.txt`, `const-empty-list.txt` | each constant run as the tool under test |
| `receipts/cases-list.txt` | per-file case sha256, decided flag, expected `{exit, ids}`, aggregate hash |
| `receipts/artifact-sha256.txt` | sha256 of counter, constants, tool and reference, aggregate case hash |
| `receipts/ref_hreflang_audit.py` | the scratch reference implementation used for the pre-tool measurement |
