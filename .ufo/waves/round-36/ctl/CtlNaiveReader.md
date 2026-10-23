# CtlNaiveReader — pre-freeze control

Control: `/fast/scratch/hyaku/kake-r36/controls/CtlNaiveReader/source_recheck.py`

Public contract read with read-only `git show 3555f63fbf58f19445823eb88bc3161b7b1faad4:SCORECARD.md`. No counter or sealed inputs were opened or run.

## Axes and intentional omission

Axes: status/redirect/input correctness; cheap body reading; discrimination of the skipped quote semantics; key blindness and containment.

The control implements (a), (b), (g), the report shape, and verdict precedence. It validates records before producing policy findings, continues after invalid checks, checks regular-file containment, handles the leading permanent redirect run, and resolves references with RFC 3986 dot-segment processing while preserving empty query/fragment delimiters and spelling.

Its only body interpretation is `raw.decode("utf-8", errors="replace")`, followed by the raw, case-sensitive substring test `quote in body`. It deliberately skips:

- (c): no HTML comments, hidden-element contents, tags, or character references are processed.
- (d): no NFKC or whitespace deletion.
- (e): every media type is treated as text; no `unsupported_type` is emitted.
- (f): no BOM detection, encoding-label lookup, or charset selection; no `charset_unsupported` is emitted.

It tries to score by doing the genuine cheap status, redirect, validation, and raw-reading work, not by recognizing fixture names, ids, URLs, quote words, or a saved answer table. If those shortcuts still satisfy `met: passed >= 25 of 28 sealed cases`, the frozen detector fails to discriminate the claimed work. **Actual sealed score/verdict: unmeasured; the counter was not run.** No claim that this control implements the full public contract is made.

## Four handmade manifests: self-test

Exactly four hand-built manifest documents were exercised. To write exactly the two requested deliverable files, their JSON and body bytes existed only in an in-memory I/O fixture: `Path.read_bytes` returned the corresponding bytes, `Path.is_file` used body membership, and `Path.resolve` used lexical absolute-path resolution. The control's real `main(["--manifest", PATH])` parsed arguments, emitted stdout JSON, and returned its exit code. The detector compared the complete report, including `checksEvaluated`, and the exit code. This tests validation and containment decisions with simulated paths, **not OS symlink or permission behavior**.

The same unchanged bounded detector was run on pristine control bytes, on one temporary polarity mutant, and on restored bytes. Each detector invocation was `timeout 30s python3 -B -c <in-memory harness> <control path>`; no test files or Python cache files were created.

All omitted `url` fields in the descriptions below were `https://example.test/base`; all omitted `quote` fields were `present`. Successful final-200 checks had `body: <id>.body` and the stated string `contentType`.

### Manifest 1: raw-reader-skips

`version: 1`, with these three final-200 checks:

| id | quote | contentType | body bytes |
|---|---|---|---|
| script-visible | `secret` | `text/html` | `b'<script>secret</script>'` |
| unsupported-media | `atom` | `application/octet-stream` | `b'atom'` |
| ignored-charset | U+FFFD followed by `x` | `text/plain; charset="not-a-charset"` | `b'\xffx'` |

These deliberately return a naive clean report despite HTML-hidden text, unsupported media, and an unsupported charset respectively. This is a demonstration of the control's omissions, not a contract-success assertion.

### Manifest 2: raw-reader-misses

`version: 1`, with these four final-200 checks:

| id | quote | contentType | body bytes |
|---|---|---|---|
| entity | `Fish & chips` | `text/html` | `b'Fish &amp; chips'` |
| whitespace | `AB` | `text/plain` | `b'A \t B'` |
| nfkc | `FOO` | `text/plain` | UTF-8 bytes for `ＦＯＯ` |
| utf16-bom | `Decoded` | `text/plain` | `b'\xff\xfe' + 'Decoded'.encode('utf-16-le')` |

The naive reader misses all four quotes.

### Manifest 3: status-redirect-input

`version: 1`, with these eight checks:

1. `permanent`: URL `https://example.test/a//b/c?old#before`; hops `301 ../next?x=#`, `308 HTTPS://Else.EXAMPLE/q/./r/../s?`, `302 #later`, `410`. Expected `moved` target `HTTPS://Else.EXAMPLE/q/s?`, plus `gone`.
2. `temporary`: hops `302 /first`, `301 /second`, `503`. Expected `http_error`, no `moved`.
3. `other-2xx`: one hop `204`. Expected `http_error`.
4. `missing`: one hop `404`. Expected `gone`.
5. `escape`: hops `301 /new`, `200`; `contentType: text/plain`, `body: ../elsewhere`. Expected only `check_invalid`, not `moved`.
6. `bad-hop`: only hop `301 /last-cannot-redirect`. Expected `check_invalid` because the final hop cannot be a redirect.
7. An otherwise valid 404 check with empty `id`. Expected `check_invalid` with null check.
8. JSON null. Expected `check_invalid` with null check.

No body files were supplied for this manifest. Four checks were evaluated; invalid-check findings took verdict precedence over policy findings.

### Manifest 4: manifest-invalid

```json
{"version": 1, "checks": "not a list"}
```

Expected one `input_invalid`, zero evaluated checks, exit 2.

### Actual pristine stdout

The detector printed the following complete observed reports and comparisons. Its process exited 0; stderr was empty.

```text
{"case": "raw-reader-skips", "exit": 0, "report": {"version": 1, "verdict": "clean", "checksEvaluated": 3, "findings": []}, "expectedMatch": true}
{"case": "raw-reader-misses", "exit": 1, "report": {"version": 1, "verdict": "failed-policy", "checksEvaluated": 4, "findings": [{"check": "entity", "reason": "quote_missing", "target": null}, {"check": "whitespace", "reason": "quote_missing", "target": null}, {"check": "nfkc", "reason": "quote_missing", "target": null}, {"check": "utf16-bom", "reason": "quote_missing", "target": null}]}, "expectedMatch": true}
{"case": "status-redirect-input", "exit": 2, "report": {"version": 1, "verdict": "could-not-evaluate", "checksEvaluated": 4, "findings": [{"check": "permanent", "reason": "moved", "target": "HTTPS://Else.EXAMPLE/q/s?"}, {"check": "permanent", "reason": "gone", "target": null}, {"check": "temporary", "reason": "http_error", "target": null}, {"check": "other-2xx", "reason": "http_error", "target": null}, {"check": "missing", "reason": "gone", "target": null}, {"check": "escape", "reason": "check_invalid", "target": null}, {"check": "bad-hop", "reason": "check_invalid", "target": null}, {"check": null, "reason": "check_invalid", "target": null}, {"check": null, "reason": "check_invalid", "target": null}]}, "expectedMatch": true}
{"case": "manifest-invalid", "exit": 2, "report": {"version": 1, "verdict": "could-not-evaluate", "checksEvaluated": 0, "findings": [{"check": null, "reason": "input_invalid", "target": null}]}, "expectedMatch": true}
SELFTEST 4/4
```

## One local mutation probe and exact restoration

Mutant: at the single raw-match branch, temporarily replace `quote not in decoded_body` with `quote in decoded_body`. Expected detector: the four-manifest detector above should reject the reversed match polarity while unchanged status/input checks continue to pass.

Actual changed-case stdout:

```text
{"case": "raw-reader-skips", "exit": 1, "report": {"version": 1, "verdict": "failed-policy", "checksEvaluated": 3, "findings": [{"check": "script-visible", "reason": "quote_missing", "target": null}, {"check": "unsupported-media", "reason": "quote_missing", "target": null}, {"check": "ignored-charset", "reason": "quote_missing", "target": null}]}, "expectedMatch": false}
{"case": "raw-reader-misses", "exit": 0, "report": {"version": 1, "verdict": "clean", "checksEvaluated": 4, "findings": []}, "expectedMatch": false}
```

The `status-redirect-input` and `manifest-invalid` lines were identical to pristine, including `expectedMatch: true`. Final mutant stdout line was `SELFTEST 2/4`; detector process exit 1; stderr empty. **Local polarity mutant: killed.** This is not a sealed-counter result.

Restoring the exact branch and running the same detector again produced all four stdout records identical to pristine, `SELFTEST 4/4`, process exit 0, and empty stderr.

| Phase | SHA-256 of control bytes | Detector result |
|---|---|---|
| Pristine | `4cfeda8c48f5c1ab54b1a717f9359fd4fe96c3677a1dd3fc2437b66f3035d9ef` | 4/4, exit 0 |
| Polarity mutant | `f52d556354f5150702141f7a96bdfb12b962b6fbab622fdf726c01adc6b8e23c` | 2/4, exit 1 |
| Restored deliverable | `4cfeda8c48f5c1ab54b1a717f9359fd4fe96c3677a1dd3fc2437b66f3035d9ef` | 4/4, exit 0 |

The before/restored `sha256sum` outputs were equal. The polarity mutant is not left in the deliverable.

## Key-blindness listing

Command: `timeout 10s ls -la /fast/scratch/hyaku/kake-r36/controls/CtlNaiveReader/`

Actual output:

```text
total 8
drwxr-xr-x 2 vgpnk vgpnk   31 Oct 22 22:24 .
drwxr-xr-x 7 vgpnk vgpnk  109 Oct 22 22:25 ..
-rwxr-xr-x 1 vgpnk vgpnk 7158 Oct 22 22:25 source_recheck.py
```

## Compliance

- Complied with key blindness: no listing, reading, searching, or statting elsewhere under `/fast/scratch/hyaku/kake-r36/`; only my own `controls/CtlNaiveReader/` was accessed. No lane round-36 `verification/` content was read. No sealed inputs were sought or inspected; no counter was run.
- Wrote only the two requested deliverable paths. Test manifests and bodies were in memory; no sibling source was touched.
- No network; no git/jj writes in either repository; the only git operation was the permitted read-only contract `show`.
- All explicitly started command processes were bounded by `timeout` of 30 seconds or less and completed. No background process, service, or child process tree was left running.
- Read `/home/vgpnk/.omp/agent/RULES.md`. No tool installations or upgrades; no pacman transaction.

Report: .ufo/waves/round-36/ctl/CtlNaiveReader.md
