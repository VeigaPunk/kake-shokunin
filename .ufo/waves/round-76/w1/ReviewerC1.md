# ReviewerC1 — frozen-counter attack

Axes: predicate fidelity; population fidelity; resistance to receipt laundering; independent reproducibility. Recommendation only: do not treat the current counter as proving the frozen C1 sentence. No lane implementation was edited or admission issued.

Scope: base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`; reviewed the added counter in freeze revision `b758cb040d53374b1b63b89702c7128f77212d23`, not a later after-state. Retained implementation/diff/contract: `ReviewerC1/counter-source.py`, `counter.diff`, `contract-source.md`. All references below to counter lines use that retained source. LSP device unavailable: `read xd://lsp` returned `No such tool`; semantic references/definitions/diagnostics were unavailable. Findings use direct source inspection and executable counterexamples, not grep as semantic proof.

## Findings by severity

### High — correction rows can carry fabricated claims without checking them

Contract lines 11–14 say, verbatim:

> A round's claim rows stop quoting command output that no committed receipt
> contains: every claim-bearing backticked span in the effective claim rows of rounds 75–76 is a contiguous
> substring of a committed receipt, or carries an explicit elision whose fragments are contiguous, or is
> closed by a correction line that itself quotes a validated receipt line and names the defective span.

Counter lines 279–280 instead say:

```python
        if CORRECTION_RE.search(r["text"]):
            continue
```

Correction validation at line 266 accepts any one good span:

```python
        good = [sp for sp in c["spans"] if span_ok(sp, receipts, root, rev)]
```

Held-out `correction_extra_false_claim`: a correction quoting the complete receipt line `aa=1 bb=2` also asserts `fake=777`, absent from every receipt. Observed exit 0, `met=true`, no findings. The named defective original span may be a legitimate correction target, but the additional fabricated observation is not a quotation of the target and cannot inherit that exemption. Apply the predicate to correction rows' new claims too.

### High — correction validation accepts a fragment, not a receipt line

Same contract sentence, exact ending: “closed by a correction line that itself quotes a validated receipt line and names the defective span.” Target-after lines 51–52 explicitly require “appended correction rows that quote whole receipt lines.”

Counter lines 266 and 234–237 validate spans by substring, not whole-line equality:

```python
    frags = [f for f in ELIDE_RE.split(span) if f.strip()] if ELIDE_RE.search(span) else [span]
    return any(all(f in body for f in frags) for _, body in receipts)
```

Held-out `correction_partial_line`: original `zz=9`; correction quotes only `aa=1` from receipt line `aa=1 bb=2`, naming `zz=9`. Observed exit 0, `met=true`. Under the whole-line requirement this cannot close the defect. Use distinct receipt-line validation for corrections; retain substring validation for ordinary spans.

### High — assignment classification silently drops single-letter tokens

Contract lines 28–30: “A backticked span of a claim row carrying an observed-value shape: `token=value`, `exit <n>`, an `a/b` tally, or a 7–64 char lowercase hex token.”

Counter line 42, verbatim:

```python
ASSIGN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]=\S")
```

The second character class has no repetition operator; it requires an additional character. Held-out `single_letter_assignment` contains only fabricated `x=9`. Observed exit 0, `spans_checked=0`, `met=true`; contract implies T1. Recognize single-letter identifiers as well as longer tokens.

### High — commit existence substitutes for receipt evidence, including at the real base

Contract lines 39–40: “`T1` span absent from every receipt.” The main claim sentence lists receipt substring, explicit elision, and validated correction; no commit-object exception.

Counter lines 234–235, verbatim:

```python
    if HEX_RE.match(span) and commit_exists(root, rev, span):
        return True
```

Held-out `commit_without_receipt` quotes an actual fixture commit abbreviation which appears in no receipt. Observed exit 0, `met=true`. Independent base inspection also finds `6c10b433` and `ca1a2982` in the Mistakes row at `corpus/lessons/round-75.md:102`, absent from the entire receipt universe; both are skipped by this exception. They are genuine receipt-predicate defects under the frozen wording even though they are sensible revision citations. If revision citations should be exempt, that requires a terms amendment, not an unannounced implementation exception. `commit_exists()` lines 65–69 also does not establish token ancestry relative to the measured revision; it checks object existence after separately validating the measured revision.

### Medium — heading search duplicates rows and admits the wrong heading level

Contract lines 23–26, verbatim:

> Claim rows: markdown table data rows inside a `## Round <N>` section of `SCORECARD.md`
> (headers and separator rows excluded); bullets inside `## Round-<N> criterion` sections of
> `corpus/QUALITY.md`; table data rows and bullets inside `## Mistakes` / `## Gate` / `## Claims` /
> `## Corrections` of `corpus/lessons/round-<N>.md`. N ∈ {75, 76}.

Counter line 146:

```python
        if not head_re.search(title):
```

Counter line 211:

```python
            pat = re.compile(r"\bround[ -]?(?:%s)\b" % "|".join(str(n) for n in rounds), re.I)
```

`sections()` accepts headings at any level; the regex searches anywhere in the title and does not require the contract's section form. At base it matches both `## Round 75` and `### Capabilities acquired in round 75`, then traverses overlapping bodies. Rows at SCORECARD lines 4899, 4904 and 4905 are counted twice; the defective span at line 4904 becomes two findings. Held-out `wrong_heading_level` independently demonstrates inclusion of a row under standalone `### Round 76`, returning T1 despite being outside the exact level-two population. Restrict section identity and do not duplicate physical rows.

### Medium — ready-marker suffixes can launder a quote

Contract line 35: “(`*-results.json`, `*-dispatch.json`, `*-spec.json`, `swarm-registry.json`, `*.ready*`) are never receipts”.

Counter line 81:

```python
    if any(name.endswith(a) for a in DISPATCH_ARTIFACTS) or name.endswith(".ready") or "/.ready" in name:
```

Held-out `ready_marker`: fabricated `zz=9` exists only in `probe.ready.txt`; observed exit 0, `met=true`. The wildcard in the contract excludes that file. Match the actual ready-artifact glob before admitting data extensions.

### Medium — whitespace rewrite passes the historical-line protection

Contract lines 51–52: “A deletion or a rewrite is never the repair.” Kill rule (3): “The repair may not rewrite a historical line; a rewrite withdraws C1.”

Counter line 245:

```python
    return {(r["file"], re.sub(r"\s+", " ", r["text"]).strip()) for r in rows}
```

Held-out `whitespace_rewrite` changes the base row's spacing while preserving all content. Observed exit 0, `append_only=true`, `met=true`. Normalization discards the evidence of this historical-line rewrite. This is a gap against the stricter kill rule; it is not a claim that ordinary deletion controls pass.

## Independent base derivation

Command actually run for the counter (JSON retained in `ReviewerC1/base_run.json`):

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-76/c76_quote_truth.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --base a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --rounds 75,76 --json
```

Observed exit 1; rows=19, receipt_files=10452, spans_checked=30, spans_exempted=0, corrections=0, append_only=true, findings count 8, met=false. Missing round-76 lesson is reported but is not a finding. The source exists in the freeze commit, not at the base revision; the run measures the base's committed data using that source.

Independent extractor/receipt search command:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-76/w1/ReviewerC1/driver.py
```

Observed stdout: `INDEPENDENT {"rows": 16, "receipts": 10452, "spans": 25, "absent": 9}`. `ReviewerC1/independent.json` retains the entire population, spans, receipt matches, and absences. Driver reads the three base files using `git -C <lane> show <base>:<file>`, independently recognizes exact level-two sections, and independently reads committed receipt bodies with `git cat-file --batch`; it does not call counter population/classification methods. Base file snapshots are retained beside it. Independent checks are not inferred from the counter's output.

The counter's eight T1 outputs, reproduced exactly in `base_run.json`:

| Base location | Absent span | Assessment |
|---|---|---|
| SCORECARD:4892 | `files=18 mismatches=0 append_only=true met=true missing_frozen=0` | real noncontiguous quote |
| SCORECARD:4892 | `mismatches=3 classes=E3 append_only=false missing_frozen=1` | real noncontiguous quote |
| SCORECARD:4893 | `population=18 bound=18 mismatches=0 met=true missing_frozen=0` | real noncontiguous quote |
| SCORECARD:4893 | `receipt: source=committed declared_valid=true` | real noncontiguous quote |
| SCORECARD:4904 | `mismatches=0 met=true missing_frozen=0` | real noncontiguous quote |
| SCORECARD:4904 | same span again | harness duplicate, not another defective span |
| QUALITY:1499 (continued through 1515) | `files=15 append_only=false met=false` | real noncontiguous quote |
| lesson round-75:82 (continued through 85) | `files=15 append_only=false met=false` | real noncontiguous quote |

Thus findings=8 is the counter's reproducible output, not the exact contract population's defect count: seven unique reported defects plus two unreported hex-token defects yield nine under the literal frozen predicate. No finding is T2: none of these quoted spans carries an explicit elision. Contract line 49's characterization as “elided quotes” is colloquial omission, not the explicit-elision alternative the predicate permits.

Examples of the gaps, with original receipt copies retained in `ReviewerC1/original-receipts/`: `after-c1-row-truth.txt:4` inserts `classes=-` between `mismatches=0` and `append_only=true`; `after-c2-receipts.txt:5–7` separates `missing_frozen=0` onto another line and inserts `worktree=identical declared=... declared_match=false` between `source=committed` and `declared_valid=true`. These are not contiguous spans. `ctl-deletion.txt:1` inserts `mismatches=2 classes=E3` between `files=15` and `append_only=false`. No alternative matching receipt was found by the full committed-universe search.

## Held-outs and exact invocation evidence

Each fixture was initialized and committed only under `/fast/scratch/hyaku/kake-r76/ReviewerC1/fixtures/<name>`; repository top-level assertions precede staging and committing. This follows the seat's explicit tiny-fixture-repo instruction, not permission to mutate the lane. Retained input trees omit `.git`; source files, `run.json` (exact command and complete output), and `verdict.json` are under `ReviewerC1/<name>/`. The first battery is replayable from `driver.py`; its exact individual commands and outputs are also aggregated in `fixture-results.json`. The supplemental commit/whitespace attacks have separate `run.json` records containing their exact commands and base revisions. Every command uses explicit `--root`, `--revision`, `--base`, and `--rounds`; TMPDIR was the seat scratch `tmp` directory. This CLI does not use `--work` except for its selftest.

| Fixture directory | Contract implication | Observed exit / finding IDs |
|---|---|---|
| unrelated_round | pass: receipts have no round-locality restriction; I agree with that specified policy | 0 / none |
| seat_prose | fail: w1/Seat.md cannot evidence the quote | 1 / T1 |
| dispatcher_prose | fail: w1-results.json excluded | 1 / T1 |
| elision_split | fail: fragments in different receipt files | 1 / T2 |
| different_span | fail: correction names another span | 1 / T1 |
| nonreceipt_correction | fail: names target but quotes only seat prose | 1 / T4,T1 |
| fabricated_digest | fail: fabricated 64-character digest | 1 / T1 |
| pipe_span | fail: absent quoted span containing a pipe | 1 / T1 |
| newline_escape | fail: absent span containing literal backslash-n | 1 / T1 |
| indented_row | include: three-space-indented table row remains a table data row | 1 / T1 |
| round7_prefix | exclude: row says `## Round 76`, but containing heading is `## Round 7` | 0 / none, rows=0 |
| duplicate_correction | pass: duplicate valid corrections do not themselves violate contract | 0 / none, corrections=2 |
| single_letter_assignment | fail: observed-value-shaped token absent | 0 / none |
| correction_partial_line | cannot close: quote is only a receipt fragment | 0 / none |
| ready_marker | fail: never-receipt ready artifact is the only apparent support | 0 / none |
| wrong_heading_level | exclude: standalone level-three heading is not specified population | 1 / T1 |
| correction_extra_false_claim | fail: unrelated fabricated claim inside correction | 0 / none |
| commit_without_receipt | fail under literal receipt predicate | 0 / none |
| whitespace_rewrite | rewrite forbidden by kill rule | 0 / none, append_only=true |

The round-prefix probe is exclusion, not evidence that the quote is true. The pipe fixture tests textual span extraction; unescaped table delimiters are a Markdown interpretation risk, so no additional defect is asserted from it. The newline probe uses a literal escape, not a physical multiline backtick span.

## Residual risks and verification gaps

- Frozen `span_ok()` requires elision fragments in the same receipt but does not require their order. The contract does not expressly order fragments; no definite order-based defect is claimed here.
- Substring-based target naming at counter line 285 is not token-delimited. This is an inspection risk; no extra exploit is claimed as exercised.
- The selftest command `python3 -B <lane>/.ufo/waves/round-76/c76_quote_truth.py --selftest --work /fast/scratch/hyaku/kake-r76/ReviewerC1/tmp/selftest` was exercised: observed `selftest: 13/13 passed`, exit 0. However its `ok_commit` case writes `@SHORT@` before replacing that string only in the local variable after commit (counter lines 341–353). It does not actually test a committed hex span; our supplemental fixture does.
- The counter docstring still describes same-subject supersession and T5 (lines 17–21); current executable logic uses span mention and T4. Treat the frozen contract, not that stale docstring, as authoritative.
- No after-state, canonical runtime/resume implementation, unrelated tool, integration, or live network was exercised. Those are outside this C1 assignment. No installation or upgrade was performed.
- Report artifacts include deliberately false held-out inputs. They are data, not new claim instructions or valid receipt corrections.

Report: .ufo/waves/round-76/w1/ReviewerC1.md
