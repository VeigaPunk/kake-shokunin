## Verdict

No actionable finding in the requested self-closing-tag scope. The public CLI outputs matched the verdicts derived before execution. This is a recommendation only, not an independent admission.

## Findings

None (no P0–P3 finding). In particular, no tested case produced a false `clean` where the expected canonical signal differed.

## Checked and held

- Probed exact candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc` from a no-hardlinks scratch clone; observed clone `HEAD` was `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`. The lane was at descendant `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b` when inspected; its reported dirty-path count was 11. No lane production files were changed.
- Wrote the expected-verdict matrix to `/tmp/kake-r23-FalsifyVoidSelfClose-lS4V/expected.md` before running the CLI. Fixtures and manifests are under `/tmp/kake-r23-FalsifyVoidSelfClose-lS4V/cases/`.
- Checked `scripts/canonical_audit.py` tag sets and `CanonicalHTMLParser.handle_startendtag` at candidate lines 36–40 and 285–295, then exercised the public manifest CLI. The probe manifest groups cover:
  - **Expected clean:** all six body void tags (`input`, `img`, `br`, `hr`, `source`, `wbr`); `base`, canonical `link`, and `meta` self-closing before `</head>`; uppercase tag/attribute names; quoted attribute data containing `/>`; unquoted `data=x/>` on `img` and `div` (the slash is part of the unquoted value, not an HTML self-closing flag).
  - **Expected unsupported:** `<div/>`, `<span/>`, and `<p/>` in body; `<div/>` before `</head>`; and `<img/>` before `</head>` (not a supported head child).
  - **Expected policy mismatch:** quoted and unquoted canonical `href` values ending in `/>`, which must not be truncated to the expected URL.

Exact commands and stdout/exit observations:

```text
python3 -B /tmp/kake-r23-FalsifyVoidSelfClose-lS4V/clone/scripts/canonical_audit.py --manifest /tmp/kake-r23-FalsifyVoidSelfClose-lS4V/cases/clean.json --json; printf 'exit=%s\n' "$?"
{"findings":[],"pagesChecked":5,"verdict":"clean"}
exit=0
```

```text
python3 -B /tmp/kake-r23-FalsifyVoidSelfClose-lS4V/clone/scripts/canonical_audit.py --manifest /tmp/kake-r23-FalsifyVoidSelfClose-lS4V/cases/unsupported.json --json; printf 'exit=%s\n' "$?"
{"findings":[{"id":"html_unsupported","page":"https://example.test/project/nonvoid-div.html"},{"id":"html_unsupported","page":"https://example.test/project/nonvoid-span.html"},{"id":"html_unsupported","page":"https://example.test/project/nonvoid-p.html"},{"id":"html_unsupported","page":"https://example.test/project/nonvoid-head.html"},{"id":"html_unsupported","page":"https://example.test/project/nonhead-void.html"}],"pagesChecked":5,"verdict":"could-not-evaluate"}
exit=2
```

```text
python3 -B /tmp/kake-r23-FalsifyVoidSelfClose-lS4V/clone/scripts/canonical_audit.py --manifest /tmp/kake-r23-FalsifyVoidSelfClose-lS4V/cases/policy.json --json; printf 'exit=%s\n' "$?"
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/quoted-href-suffix.html"},{"id":"canonical_mismatch","page":"https://example.test/project/unquoted-href-suffix.html"}],"pagesChecked":2,"verdict":"failed-policy"}
exit=1
```

## Limits

- No LSP device was exposed in this session's mounted tool inventory, so `lsp status`, `references`, `definition`, and `diagnostics` were unavailable; no grep result is relied on as semantic proof.
- No browser engine was run for DOM-differential checks. These are synthetic targeted public-CLI probes against the exact candidate, not a claim that every browser-repair case is covered.
- The full built-in `--selftest` was not run. No tools were installed or updated.
