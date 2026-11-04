# Source receipts — 2026-11-04

Both commands ran once, concurrently, with cwd `/fast/scratch/hyaku/kake-r86/ScribeAssim`. No retries or additional remote endpoints. The POST was the one authorized exception to GET-only work.

```sh
curl -sS -L --dump-header /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScribeAssim/docs.headers --output /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScribeAssim/docs.html --write-out 'http_status=%{http_code}\nurl_effective=%{url_effective}\n' https://developer.chrome.com/docs/crux/vis
```
Exit 0. stdout:
```
http_status=200
url_effective=https://developer.chrome.com/docs/crux/vis
```
Response Date: Wed, 04 Nov 2026 15:36:54 GMT. Full body SHA256 `ea17c95675c25407a7f8c717be96714f63e5b829eda5fa898b18f1223e383e78`; headers SHA256 `80b1690a77477c01bcba1a598c1f73f85469f6d08af29c2cec1ee72b2ed01040`.

Own located no-data quote, 20 words, retained docs.html line 2932, section `does_it_work_for_all_websites`:
> If your origin is not included in the CrUX dataset, there will be no data to display.

```sh
curl -sS -X POST -H 'Content-Type: application/json' --data '{"origin":"https://example.com"}' --dump-header /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScribeAssim/probe.headers --output /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScribeAssim/probe.json --write-out 'http_status=%{http_code}\nurl_effective=%{url_effective}\n' https://chromeuxreport.googleapis.com/v1/records:queryRecord
```
Exit 0 (curl did not use --fail; HTTP failure is recorded, not suppressed). stdout:
```
http_status=403
url_effective=https://chromeuxreport.googleapis.com/v1/records:queryRecord
```
Response Date: Wed, 04 Nov 2026 15:36:54 GMT. Full body SHA256 `da4b1ce0a6833588f4a9bd24350c9f16c31426d439f92b3342b43bffec6667c2`; headers SHA256 `37fb987031707316e9d069931d4450c101e451a33be565686ed4de6d3c5c2887`.

Complete probe response:
```json
{
  "error": {
    "code": 403,
    "message": "Method doesn't allow unregistered callers (callers without established identity). Please use API Key or other form of API consumer identity to call this API.",
    "status": "PERMISSION_DENIED"
  }
}
```

Fingerprint command (exit 0):
```sh
sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScribeAssim/docs.html /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScribeAssim/docs.headers /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScribeAssim/probe.json /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScribeAssim/probe.headers
```

No credentials, browser use, account changes, property measurements, tool installs, VCS mutations, counter runs, or corpus-gate runs. The source row ids S459/S460 are assigned draft references, not proof that registry rows have been appended.
