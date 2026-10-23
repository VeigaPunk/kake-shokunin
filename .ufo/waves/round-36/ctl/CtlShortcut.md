# CtlShortcut — exposed-label control

## Axes and scope

- **Freshness:** the declared C1 capability; this control deliberately does not establish that a source quote survives in a recorded body.
- **Operability:** preserves the public CLI/report/exit-code shape, without claiming a second scored improvement.
- Counter discrimination is the review question, not a new lane axis. No admission or canonical judgment is made here.

Control: `/fast/scratch/hyaku/kake-r36/controls/CtlShortcut/source_recheck.py`.
Public basis: `git show 3555f63f:SCORECARD.md`, section “Round 36 — declared claims”, and the public `.ufo/waves/round-36/sealed_count.py` only.

## What it skips and how it tries to score

The control **never opens or reads a body**. It does not implement HTML comment/element/tag removal or entity decoding (c), NFKC/whitespace-normalized substring matching (d), or BOM detection/encoding selection/body decoding/replacement handling (f).

It retains inexpensive metadata work: manifest/check validation, body-path containment and regular-file checks, final statuses, leading permanent redirects with relative URL resolution, media-type recognition, and report precedence. For supported media it usually guesses that the quote holds. It guesses `quote_missing` from URL/id/file-name labels such as “case sensitive”, “mismatch”, “hidden” and “script only”, and from quote words such as “missing”, “secret” and “ghost”. Markup-looking or reference-looking quotes provide additional hints. A charset-label allowlist guesses `charset_unsupported`, unless an exposed “BOM” label suggests an override. This is classification from metadata, not decoding.

The public counter explicitly randomizes **every check id and every body file name on each run**, using extensionless random body names (`sealed_count.py:98–124`, also its docstring at lines 20–26). Thus those two predictors should be mostly useless. URL paths/queries, quotes, contentType strings and hop chains remain exposed. This control attempts to exploit that residual information; it does not inspect case directories, sibling files, keys, expected findings or counter state.

No sealed score was measured or estimated numerically. Only L1 can determine whether it reaches the frozen predicate, `passed >= 25 of 28 sealed cases`.

## Self-test actually run

Command wrapper: `timeout 45s python3 -B -c <in-memory self-test harness>`; process exit **0**, existing Python **3.14.8**.

To preserve the exactly-two-files requirement, the harness supplied handmade JSON manifests through a `Path.read_text` adapter and called the real `main(['--manifest', ...])`. Body adapters supplied the payloads below if requested; regular-file/path validation used this control's existing file. No additional manifest/body files were written. Four fixtures used three distinct manifest JSON values: the final pair deliberately has identical metadata. Assertions checked exact report objects, exits and zero body reads. Canonical expectations below are derived directly from the public contract, not from running a reference tool or the sealed counter.

| Fixture | Handmade input | Observed output | Body reads |
|---|---|---|---|
| status-and-leading-run | `301 ../one/ → 308 final → 302 later → 410` from `https://example.invalid/base/page`; another check `302 → 301 → 204` | exit 1, `failed-policy`, evaluated 2; `(c101, moved, https://example.invalid/one/final)`, `(c101, gone, null)`, `(c102, http_error, null)` | 0 |
| faults-media-and-label | missing body field; `application/pdf`; `text/plain; charset=shift_jis` at `/without-bom`; HTML quote `secret` at `/script-only` with payload `<script>secret</script>` | exit 2, `could-not-evaluate`, evaluated 3; `check_invalid`, `unsupported_type`, `charset_unsupported`, `quote_missing` on their respective checks | 0 |
| collision-visible | opaque URL, HTML quote `needle`, payload `<p>needle</p>` | exit 0, `clean`, evaluated 1, no findings | 0 |
| collision-hidden | exactly the preceding manifest, payload `<script>needle</script>` | exit 0, `clean`, evaluated 1, no findings — **intentional canonical mismatch** | 0 |

Observed harness summary: `controlShapeAssertionsPassed=4`, `intentionalCanonicalMismatches=1`. This is not a claim of four contract-correct results.

## Counterexample, evidence and smallest safe correction

The final two fixtures use this identical manifest:

```json
{"version":1,"checks":[{"id":"c9053a1","url":"https://example.invalid/opaque","quote":"needle","hops":[{"status":200}],"contentType":"text/html","body":"source_recheck.py"}]}
```

Changing only the virtual body from `<p>needle</p>` to `<script>needle</script>` must change the public-contract result from clean/exit 0 to `quote_missing`/exit 1. The control instead returned clean for both and performed zero body reads. This is a fixable implementation omission, not a harmless tradeoff: it undermines freshness and produces an operable but false-green report. Analogous body-only changes can defeat its normalization and decoding guesses. Exposed “missing”/“secret” labels can also cause false positives.

If L1 finds this hollow control nevertheless meets the predicate, the smallest safe counter correction is to remove semantic URL/quote labels and introduce body-only positive/negative contrasts with opaque, matched metadata, retaining rule coverage and the declared threshold before any build. This report does not edit the counter or substitute its own judgment. Making the control itself genuine would require implementing (c), (d) and (f), which would defeat this assigned negative control.

## Key-blindness listing

Executed exactly: `timeout 10s ls -la /fast/scratch/hyaku/kake-r36/controls/CtlShortcut/` (exit 0).

```text
total 12
drwxr-xr-x 2 vgpnk vgpnk   31 Oct 22 22:25 .
drwxr-xr-x 7 vgpnk vgpnk  109 Oct 22 22:25 ..
-rwxr-xr-x 1 vgpnk vgpnk 8351 Oct 22 22:25 source_recheck.py
```

## Compliance

I complied with key blindness: no listing, reading, searching or statting beneath `/fast/scratch/hyaku/kake-r36/` outside my own `controls/CtlShortcut/` directory; no access to `.ufo/waves/round-36/verification/`; no attempt to locate or read sealed cases; no counter execution. No network, git/jj writes, sandbox clones, other-runtime/judge calls, installs or upgrades. The operator rules were read first. Only the requested control and this report were written. Explicit child commands were capped by `timeout` (10, 20 or 45 seconds), ran synchronously and exited; no started background process tree remains. Tooling used was pre-existing Python 3.14.8 and standard system commands; installation/update record: none.

Report: .ufo/waves/round-36/ctl/CtlShortcut.md
