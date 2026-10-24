# Row S012 — freshness recheck (round 26)

```json
{"id":"S012","verdict":"HOLD","fetchIndex":1,"quote":"The location of a Sitemap file determines the set of URLs that can be included in that Sitemap.","anchorObserved":"Sitemap file location section, heading immediately followed by this sentence (protocol.html, after the 'Other Sitemap formats' section)","reason":"HTTP 200 re-fetch on 2026-10-21 (Last-Modified Thu, 15 Dec 2022) still carries the 'Sitemap file location' heading and the identical first sentence, followed by the same /catalog/ vs /images/ example and protocol/host restriction; scope, anchor and teaches are unchanged and remain supported.","correction":null}
```

- Living, unpinned spec page; drift test is content, not commit identity. Server Last-Modified is 2022-12-15, so bytes predate the row's 2026-10-19 mining date — no drift window.
- Fetched text view is one minified line (21,165 chars); anchor is recorded by section heading, not line number.
- Section body also states listed URLs "must use the same protocol ... and reside on the same host as the Sitemap" and illustrates cross-submission errors, which reinforces (does not narrow) the row's scope.
- Quote verified once by fixed-string search in `fetched/text/S012-1.txt`; manifest sha256 5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654, 45,292 bytes.
- No FETCH failed, no retry needed (manifest has a single S012 entry, index 1).
- No tool installs or upgrades were needed for this item.
