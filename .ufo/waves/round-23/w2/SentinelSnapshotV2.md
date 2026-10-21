## Verdict

Counterexample found. At frozen revision `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`, the `--out` confinement check protects the per-surface directory but follows symlinks on the output files themselves, allowing a pre-seeded `fetch.json` symlink to overwrite an arbitrary writable file outside `--out`. `--reaudit` also accepts inconsistent snapshot files and can emit a clean receipt for bytes whose digest does not match `fetch.json`; a missing page is reported as `not-served` even when its stored response status is 200.

All HTTP requests below used a local `127.0.0.1` test server only. No external requests, builds, formatters, or lane mutations were made. Probe data is under `/tmp/kake-r23w2-SentinelSnapshotV2-DHjw`; only this report was written in the lane.

## Findings

### P1 — A symlinked output file writes outside `--out`

**Exploit path / evidence:** Pre-create the valid per-ID output directory and make its `fetch.json` a symlink to a file outside the selected output root. The script checks `realpath()` on the directory, but then opens fixed output filenames normally, following the leaf symlink.

Exact command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py --population /tmp/kake-r23w2-SentinelSnapshotV2-DHjw/pop-file-link.json --out /tmp/kake-r23w2-SentinelSnapshotV2-DHjw/out-file-link
```

Exact stdout, exit 0:

```json
{
 "surfaces": [
  {
   "id": "file-link",
   "status": 200,
   "verdict": "clean",
   "findings": []
  }
 ]
}
```

Before the run, `/tmp/kake-r23w2-SentinelSnapshotV2-DHjw/out-file-link/file-link/fetch.json` pointed to `/tmp/kake-r23w2-SentinelSnapshotV2-DHjw/outside-fetch.json`, which contained `ORIGINAL-SENTINEL`. Afterward, that outside file had been overwritten with the fetch record:

```json
{
 "bytes": 97,
 "contentType": "text/html; charset=utf-8",
 "error": null,
 "fetchedAt": "2026-10-21T07:35:10Z",
 "finalUrl": "http://127.0.0.1:35911/ok/",
 "method": "GET",
 "redirects": [],
 "sha256": "4f8f2f1576d4d9d5e2a9c99bf663433545d61597197cb3803e0f354a08a4cb50",
 "status": 200,
 "truncated": false,
 "url": "http://127.0.0.1:35911/ok/"
}
```

**Impacted claim/axis:** C2 operability and the documented guarantee that snapshot files are written only under `--out`. A caller processing an attacker-prepared or shared output tree can overwrite any file writable by the process, with the process's privileges.

**Smallest fix:** Open output leaves without following symlinks (e.g. `O_NOFOLLOW` via `os.open`, preferably relative to an opened directory fd); reject non-regular existing leaves. Apply this to `fetch.json`, `page.html`, `manifest.json`, and `audit.json`, not only the per-ID directory.

### P2 — `--reaudit` can emit receipts for altered or incomplete snapshots

**Exploit path / evidence:** The `--reaudit` branch loads `fetch.json`, checks only whether `page.html` is a regular file, and invokes the validator on the current page. It does not compare the page's bytes/length with `fetch.json`'s `sha256`/`bytes`, or validate the fetch metadata before deriving the audit URL. The command exits 0 with a receipt for data other than the captured body.

For the body-tamper probe, the local server first returned this body with no canonical:

```html
<!doctype html><html><head></head><body>original local response without canonical</body></html>
```

The capture summary was `status: 200`, `verdict: failed-policy`, finding `canonical_missing`, and `fetch.json` recorded SHA-256 `65fb09b7e7be859d515227d7a68018939660186e5a6b42c523c8dfaf93a91659`. I then replaced only `page.html` with a page containing the expected canonical (`http://127.0.0.1:35911/ok/`); its SHA-256 became `67650975a57aecc18b7ab78b329d83de900edc9ffde1f4f2bb404b3a143d1f53`.

Exact re-audit command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py --population /tmp/kake-r23w2-SentinelSnapshotV2-DHjw/pop-tamper-body-clean.json --out /tmp/kake-r23w2-SentinelSnapshotV2-DHjw/out-tamper-body-clean --reaudit
```

Exact stdout, exit 0:

```json
{
 "surfaces": [
  {
   "id": "tamper-body-clean",
   "status": 200,
   "verdict": "clean",
   "findings": []
  }
 ]
}
```

The original fetch digest remained unchanged, and the re-audit made zero HTTP requests. Independently, changing only a captured `fetch.json`'s `sha256` to 64 zeroes also produced exit 0 and a `clean` summary; the actual page digest was `4f8f2f1576d4d9d5e2a9c99bf663433545d61597197cb3803e0f354a08a4cb50`, while the stored fetch digest was `0000000000000000000000000000000000000000000000000000000000000000`.

Missing-page case: after a normal 200 capture, I removed `page.html` and ran:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py --population /tmp/kake-r23w2-SentinelSnapshotV2-DHjw/pop-reaudit.json --out /tmp/kake-r23w2-SentinelSnapshotV2-DHjw/out-reaudit-missing-page --reaudit
```

Exact stdout, exit 0:

```json
{
 "surfaces": [
  {
   "id": "reaudit",
   "status": 200,
   "verdict": "not-served",
   "findings": []
  }
 ]
}
```

The written `audit.json` was `{"error": null, "exit": null, "status": 200, "verdict": "not-served"}` despite the stored fetch record having status 200. Thus a missing captured page is indistinguishable in the summary from a non-served HTTP response. `measure_c2.py` would later reject the body/digest mismatch or missing served page, but the producer's own successful re-audit output does not disclose it.

**Impacted claim/axis:** C2 operability / receipt reproducibility. An operator can mistake a successful re-audit of edited bytes for an audit of the captured response; missing body data is also mislabeled as an HTTP outcome.

**Smallest fix:** In `--reaudit`, validate the stored record and require present page bytes to match both recorded `bytes` and `sha256` before invoking the validator. For a fetch record classified as served, missing or mismatched page data must produce an explicit input/audit error, never `not-served` or a policy verdict.

### P3 — Missing `fetch.json` aborts with an uncaught traceback

**Exploit path / evidence:** With a valid population and an existing per-ID directory but no `fetch.json`, `--reaudit` exits on `FileNotFoundError` before producing a summary or processing later surfaces.

Exact command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py --population /tmp/kake-r23w2-SentinelSnapshotV2-DHjw/pop-reaudit.json --out /tmp/kake-r23w2-SentinelSnapshotV2-DHjw/out-reaudit-missing-fetch --reaudit
```

Exact result: exit `1`, stdout empty; stderr ends with:

```text
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/kake-r23w2-SentinelSnapshotV2-DHjw/out-reaudit-missing-fetch/reaudit/fetch.json'
```

The traceback points to `live_snapshot.py:146`, outside the input-error handling at lines 126–137. This differs from the structured `audit-error` path exercised below.

**Impacted claim/axis:** C2 operability. A missing snapshot aborts the batch without machine-readable per-surface failure or final summary.

**Smallest fix:** Catch missing/unreadable/invalid fetch metadata in the re-audit loop and report a structured input error; either continue with an explicit failed row or return the documented bad-input status with a JSON error.

### P3 — A refused `file:` redirect is recorded as the final URL

**Exploit path / evidence:** A local HTTP response redirected to `file:///etc/hosts`. No file contents were fetched and the local server saw only the original GET, but `fetch.json` recorded `finalUrl: file:///etc/hosts` with status 302, no redirect-chain entry, and zero body bytes. The run still summarized it as `not-served`.

Exact command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py --population /tmp/kake-r23w2-SentinelSnapshotV2-DHjw/pop-file-redirect.json --out /tmp/kake-r23w2-SentinelSnapshotV2-DHjw/out-file-redirect
```

Exact stdout, exit 0:

```json
{
 "surfaces": [
  {
   "id": "file-redirect",
   "status": 302,
   "verdict": "not-served",
   "findings": []
  }
 ]
}
```

The resulting fetch fields were `url: "http://127.0.0.1:35911/redirect-file"`, `finalUrl: "file:///etc/hosts"`, `status: 302`, `bytes: 0`, `redirects: []`, `error: null`. The request log contained only `GET /redirect-file`; there was no file read or follow-up request.

**Impacted claim/axis:** C2 metadata/provenance accuracy. The recorded final URL implies a destination response that the tool refused to fetch. This probe did not bypass the non-HTTP redirect guard.

**Smallest fix:** On a refused redirect, keep `finalUrl` at the last HTTP response URL and record the blocked `Location` separately (or set a clear error); do not label an unfetched non-HTTP target as final.

## Checked and held

- **ID confinement:** Separate Unicode (`é`), uppercase (`A`), and 64-character IDs each exited 2 with `{"error": "unsafe surface id ..."}`; each caused zero server requests and created no output directory. The validator accepts only the intended ASCII lowercase pattern and maximum 63-character form.
- **Directory symlinks:** A symlink used as the `--out` root was canonicalized by `realpath()` and the successful output appeared under its target. A per-ID directory symlink targeting outside the canonical output root exited 2 with `{"error": "child-link: destination escapes --out"}` and created no entries in the outside target. This does not prevent the leaf-symlink overwrite above.
- **Initial userinfo URL:** Rejected with exit 2 and `{"error": "surface initial-userinfo: url must be http(s) with a host and no userinfo"}` before any local request.
- **Redirect guards:** Local userinfo, `file:`, and `ftp:` redirect probes each resulted in only the initial GET, status 302, no redirect-chain entry, and `not-served`; the userinfo destination was not contacted. Across recorded local requests the server saw only GETs, with no Cookie or Authorization headers. The `file:` case's `finalUrl` reporting issue is listed above.
- **Audit-error handling:** Re-auditing a valid local capture with an absent validator script exited 0 and emitted `verdict: audit-error`; it wrote an audit receipt with `exit: null`, zero pages checked, and a JSONDecodeError because the child interpreter emitted no JSON. The summary path itself worked.
- **No network in re-audit:** Explicitly measured zero local-server requests during both altered-page and altered-digest re-audit runs.

## Limits

- The probes establish behavior of the frozen local script using local HTTP responses and scratch output only; they do not establish behavior against public sites or other Python/OS versions.
- The missing-validator audit-error test covers invalid child stdout, not the timeout branch.
- No remediation was authorized or attempted. No tools were installed or updated.
