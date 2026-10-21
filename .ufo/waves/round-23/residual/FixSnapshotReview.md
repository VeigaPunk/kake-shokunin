# FixSnapshotReview — round 23 kake

## Scope and method

Reviewed the working-tree `scripts/live_snapshot.py` and its diff from frozen commit `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` using:

```text
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd -- scripts/live_snapshot.py
```

All runtime probes below used temporary directories and local loopback HTTP servers only; no public fetches, package installs, or source edits were made. No LSP device is mounted (`read xd://lsp` returned “No such tool”), so semantic references/definition/diagnostics were unavailable; review used the actual changed source and targeted behavior probes.

## Findings (highest severity first)

### High — a single `fetch.json` final-URL edit can turn a failed policy audit clean

At `scripts/live_snapshot.py:153-162`, `reaudit_body()` checks that metadata `url` and `method` match the population and that `finalUrl` is a safe HTTP(S) URL. It does not verify that `finalUrl` agrees with the original URL when there are no redirects, or with the recorded redirect chain. `audit()` then uses that mutable `finalUrl` as the document URL for canonical resolution (`:219`).

Reproduction on a local loopback server: it served HTML with relative canonical `href="./"` at `/start`; the population expected `/expected/`. The original capture recorded `/start`, `redirects: []`, and `failed-policy` with `canonical_mismatch`. I changed only `fetch.json.finalUrl` to `/expected/page` (kept `page.html`, its recorded length and SHA-256, original URL, method, status, and empty redirect list unchanged). `--reaudit` exited 0 and replaced the audit with verdict `clean`, no findings. Thus a one-field snapshot metadata tamper bypasses the re-audit integrity check and produces a false clean.

The metadata acceptance must bind the final URL to the original URL and a validated redirect chain (at minimum, require equality when the chain is empty). If protection against coordinated edits to the whole metadata file is required, that needs an independently authenticated capture-time binding; the current digest stored in the same editable metadata file cannot provide that.

### Low — valid JSON of the wrong shape escapes the documented inconsistent-snapshot exit path

`reaudit_body()` immediately calls `.get()` on the result of `json.loads()` at line 155, and `served()` assumes `contentType` supports `.split()` at line 67. Replacing `fetch.json` with valid JSON `[]` and running `--reaudit` produced an uncaught `AttributeError` and exit 1. The script documents exit 2 for an inconsistent snapshot (docstring lines 9-12), and `main()` does not catch `AttributeError`. Validate metadata object/field types explicitly and report the inconsistency through the normal exit-2 path.

## Confirmed behavior / verification

- Ran the requested command with absolute paths:
  `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/snapshot_probe.py --snapshot-script /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py --validator /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py`
  Result: `passed: true`, `met: 9`, `total: 9`. Normal capture and unchanged re-audit passed; symlink/hardlink `fetch.json` leaves, edited page/digest, and missing page/fetch produced exit 2; the outside sentinels remained unchanged; the blocked `file:` redirect retained the last actual HTTP URL.
- Extended local-loopback output-leaf tests for symlink and hardlink targets at each of `fetch.json`, `page.html`, `manifest.json`, and `audit.json`: all eight attempts exited 2 and every outside sentinel stayed `UNCHANGED`. A symlinked surface directory also exited 2 and left its outside directory unchanged. No outside-`--out` mutation was observed.
- Local blocked-redirect tests for status 301/302/303/307/308 with `file:` destinations sent only the initial GET to each loopback endpoint; all were recorded as `redirect refused`, with the attempted destination absent from `finalUrl` and no redirect added to the chain.
- A same-origin local chain followed and recorded five redirects. A six-redirect chain followed exactly five, then recorded the sixth as refused with the last actually fetched URL. This matches the claimed `MAX_REDIRECTS = 5` cap.
- A local cross-port redirect kept the original surface ID/directory (`surface-one`) and recorded the source and destination URLs in the redirect chain. Cross-origin HTTP(S) redirects are accepted by the code; the stated contract does not impose a same-origin restriction, so this is noted rather than raised as a finding.
- The parent and audit child use the same interpreter via `sys.executable` (`/usr/bin/python`, Python 3.14.8 in this run); no alternate runtime was observed.

## Residual risk and gaps

The false-clean final-URL metadata tamper is the primary outstanding issue. The metadata-type crash is a separate error-contract gap. Concurrency races involving external renames/writes were not exercised; all adversarial filesystem probes were static local symlink/hardlink cases. No LSP semantic checks were possible because the device was unavailable. No builds, linters, or formatters were run.