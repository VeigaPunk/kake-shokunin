## Verdict

No actionable false-canonical-token defect found in the assigned inert-context attack surface. The candidate CLI kept title/style/script/template/textarea/iframe decoys out of the canonical count and returned `could-not-evaluate` (exit 2), not `clean`, for noscript canonical content and unsupported structural cases.

## Findings

None (P0-P3).

The apparent noscript head-close case was checked against the HTML Standard and is not a defect: in the `in head noscript` insertion mode, a `head` end tag is an “other end tag” and is ignored; the subsequent `</noscript>` returns parsing to `in head`. Thus the following canonical remains in the head in the no-scripting parse too. The tested fixture also returns clean under the candidate CLI, consistent with that rule (https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inheadnoscript).

## Checked and held

All probes used `/tmp/kake-r23-BoundaryInertContexts-Gl0A/canonical_audit.py`, extracted with `git show 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc:scripts/canonical_audit.py`; fixtures and manifests were confined to that scratch tree and invoked through the public `--manifest ... --json` CLI.

- **Positive control** (matching head canonical): command `python3 -B /tmp/kake-r23-BoundaryInertContexts-Gl0A/canonical_audit.py --manifest /tmp/kake-r23-BoundaryInertContexts-Gl0A/cases/canonical_audit.py/ctl_pos_clean/manifest.json --json` returned exactly `{"findings":[],"pagesChecked":1,"verdict":"clean"}`, exit 0.
- **Negative control** (canonical-looking token only inside title): command `python3 -B /tmp/kake-r23-BoundaryInertContexts-Gl0A/canonical_audit.py --manifest /tmp/kake-r23-BoundaryInertContexts-Gl0A/cases/canonical_audit.py/ctl_neg_title_decoy_only/manifest.json --json` returned exactly `{"findings":[{"id":"canonical_missing","page":"https://a.test/p/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}`, exit 1.
- Paired inert decoy plus one real head canonical—title, style, script, template, body textarea, body iframe, and uppercase title—each returned `{"findings":[],"pagesChecked":1,"verdict":"clean"}` (exit 0); the decoys did not cause `canonical_multiple` or a decoy mismatch.
- Noscript canonical content in head/body, head text in noscript, head textarea/iframe, and an unclosed body iframe returned `{"findings":[{"id":"html_unsupported","page":"https://a.test/p/a.html"}],"pagesChecked":1,"verdict":"could-not-evaluate"}` (exit 2). These outcomes were kept distinct from clean.
- The noscript head-close fixture `<html><head><noscript></head></noscript><link rel="canonical" href="https://a.test/p/a.html"></head></html>` returned `{"findings":[],"pagesChecked":1,"verdict":"clean"}`, exit 0. The same fixture on extracted base `b5d599e19bead54b96f589444e9ec64cdf67c28a` also returned rc 0 and the same JSON.
- Candidate `--selftest` reported `"passed":true`. The candidate-to-base diff was inspected; it adds SVG/MathML-after-head and self-closed-void handling but does not change the inert-context state logic.
- No code was edited. No builds, lint, or formatters were run. No tools were installed or updated.

## Limits

This was a public-CLI/static-source attack only; no browser engine or live page was used. The no-scripting parse behavior was checked against the HTML Standard, not an engine rendering run. No LSP device was available in the mounted tool set; no grep was used.