# ReviewerC2RealRun

## Scope and method

Read the round-61 contract and amendments A1–A5 before testing. Independently reran the committed `scripts/header_audit.py` against the canonical committed manifest `.ufo/waves/round-61/capture/manifest.json`; no network requests or lane mutations were made. The report is relative to the lane root.

## Exact real-manifest run

Command:

```text
python3 -B scripts/header_audit.py --manifest .ufo/waves/round-61/capture/manifest.json
```

Observed exit: **1**. Exact stdout:

```text
burnerchrome-kimi csp_present missing
charter-ghp csp_present missing
charter-kimi csp_present missing
ds4cc-kimi csp_present missing
ds4cc-primary hsts_present missing
ds4cc-primary csp_present missing
lucario-ghp csp_present missing
lucario-kimi csp_present missing
plazir15-ghp csp_present missing
plazir15-kimi csp_present missing
plazir27-kimi csp_present missing
ufo-fsd-kimi-pro csp_present missing
vault-index-kimi csp_present missing
checks=12 findings=13
```

The manifest is version 1, contains 12 unique check ids, and all 12 `source` paths resolve to files. The exact findings are 12 `csp_present` findings and one `hsts_present` finding for `ds4cc-primary`.

## Independent cross-check and receipts

An independent implementation of the frozen expectation classes over the 12 recorded header lists produced the same 13 `(check, class)` pairs. Comparing that run to the archived `ExecC2HeaderRecon.files/audit.json` finding set: 13 vs 13, empty difference in both directions. Thus the predicted 13 findings are reproduced with **no finding-set divergence**.

Independently checked all 12 capture receipts against their `body.bin`: SHA-256 and byte count match; `userAgent` is `round61`; `fetchedAt` is dated 2026-10-27; `finalUrl` equals `url`; `error` is null; status is an integer; body file is `body.bin`; `headerCount` matches the recorded header list; `truncated` is false. All 12 pass. The audit tool's `--selftest` also returned exit 0 with `64/64 passed`.

## Evidence divergence / caveat

`ExecC2HeaderRecon` records an intermediate tool fingerprint (41,608 bytes, SHA-256 `282d5b04676f2de1ee80fb360629c81dfbd15e0790b2033f53e1f85d741569b2`) and reports obtaining JSON with `--json`. The current committed tool at HEAD `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f` is 48,986 bytes, SHA-256 `01abd8d4ff628907713b4300adf26b5962924d85132d1f330a33b70110c1d1d4`; it rejects `--json` (exit 64; `unrecognized arguments: --json`). Its committed CLI help exposes only `--manifest`, `--root`, and `--selftest`. The contract and C2 counter require the plain-text output, not `--json`; the plain-text finding count, lines' check/class pairs, and exit reproduce exactly. The committed tool's stdout detail token is `missing`, while the archived intermediate JSON used `missing=<field>`; check/class sets agree.

## Residual risk and verification gaps

This verifies the committed real-manifest behavior, capture receipt integrity, and the predicted finding set only. It does not validate whether the declared policy is the correct publisher policy; the contract assigns that to critics. `--json` is not part of the frozen contract/counter interface, but the recon's archived JSON claim is not reproducible from the committed tool bytes. No LSP device was available in this seat's tool routes, so no LSP status/references/definition/diagnostics check was performed.

VERDICT: The committed audit produces the predicted 13 findings (12 `csp_present`, 1 `hsts_present`) with exit 1; independent set comparison and 12/12 receipt integrity checks pass, with no finding-set divergence. The only observed discrepancy is the recon's intermediate `--json` evidence versus the committed CLI, which is outside the frozen contract/counter interface.
