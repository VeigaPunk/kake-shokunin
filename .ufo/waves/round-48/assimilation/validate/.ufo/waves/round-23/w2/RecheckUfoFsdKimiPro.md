## Verdict

**none** — no counterexample to this surface's C2 operability/reproducibility was found. The one fresh GET is byte-identical to the committed 612-byte body; the committed `audit.json` is independently reproduced. Important distinction: `measure_c2.py` marks the surface `pass: true` because the receipt reproduces, while the actual publisher-policy verdict is `failed-policy` (`canonical_missing`). That is a reported page-policy failure, not a failure of receipt operability.

## Findings

### P3 — The current receipt does not exercise the `expectedCanonical` value (evidence limitation, not a C2 counterexample)

- **Exact command:** `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23w2-RecheckUfoFsdKimiPro-7QI6/manifest.json --json`
- **Exact output:** `{"findings":[{"id":"canonical_missing","page":"https://ufo-fsd.kimi.pro/"}],"pagesChecked":1,"verdict":"failed-policy"}`; exit `1`.
- **Reason:** the committed head contains no `<link rel="canonical">`. In `scripts/canonical_audit.py`, `evaluate_page` returns `canonical_missing` at lines 661–662 before reaching the expected-URL comparison at lines 679–680. Thus this page/receipt cannot distinguish the selected `expectedCanonical` from another value. The frozen C2 population selects `https://ufo-fsd.kimi.pro/` with basis “no primary on record: self-canonical”; the property map also distinguishes `ufo-fsd.kimi.page` (vault) from this `.kimi.pro` SPA shell and warns that the shared Kimi website ID is not host-unique. I found no contrary primary designation, so this attack did not falsify the selected value, but the audit result itself does not validate that policy choice.
- **Impacted claim/axis:** scope of evidence for the expected-canonical *basis*; C2 operability remains reproduced.
- **Smallest fix:** no C2 implementation change indicated. If a claim that the target choice itself was independently verified is needed, retain separate authoritative policy/provenance evidence; a `canonical_missing` receipt cannot establish it.

No defect found in this surface's served/not-served classification: the fresh response and committed fetch record are 2xx `text/html`, non-truncated, and error-free, with a stored page body whose digest matches `fetch.sha256`. The counter therefore correctly takes the served branch; the `not-served` receipt path does not apply.

## Checked and held

- **Committed `fetch.json`:** `status=200`; `finalUrl=https://ufo-fsd.kimi.pro/`; `contentType=text/html; charset=utf-8`; `sha256=1df92e30ba5a76e69a863a729326949871d3d83e290935d596f6cd9b7d65ab8c`; `bytes=612`; `method=GET`; `error=null`; `truncated=false`; no redirects.
- **One fresh read-only GET command:** `D=$(mktemp -d /tmp/kake-r23w2-RecheckUfoFsdKimiPro-XXXX) && echo "scratch=$D" && curl -sS -L --max-time 30 -o "$D/fresh.html" -D "$D/headers.txt" -w 'code=%{http_code} effective=%{url_effective} ctype=%{content_type} size=%{size_download}\n' https://ufo-fsd.kimi.pro/ && sha256sum "$D/fresh.html" && grep -iE '^(HTTP/|location:|content-type:)' "$D/headers.txt"`
- **Exact output:**
  ```text
  scratch=/tmp/kake-r23w2-RecheckUfoFsdKimiPro-7QI6
  code=200 effective=https://ufo-fsd.kimi.pro/ ctype=text/html; charset=utf-8 size=612
  1df92e30ba5a76e69a863a729326949871d3d83e290935d596f6cd9b7d65ab8c  /tmp/kake-r23w2-RecheckUfoFsdKimiPro-7QI6/fresh.html
  HTTP/2 200
  content-type: text/html; charset=utf-8
  ```
  The committed body digest and byte count match the fresh body; `cmp` reported `committed-vs-fresh: identical`. Status, final URL, content type, and SHA-256 all match `fetch.json`; **no drift** (so no changed-body defect).
- **By-eye derivation before validator run:** committed `page.html` has an explicit `<head>` with charset, viewport, title `DS4CC`, module script, stylesheet, and Kimi seed script, but no canonical link. The frozen policy requires one head canonical equal to the expected URL, so the expected finding/verdict is `canonical_missing` / `failed-policy` (exit 1). `audit.json` records exactly that.
- **Independent committed-snapshot audit:** output above, exit 1; committed and fresh bodies compare identical. The working-tree validator SHA-256 is `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387`, equal to the frozen-revision digest reported by the counter.
- **Exact named counter command:** `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`
- **Counter output for this surface:** `{"id":"ufo-fsd-kimi-pro","pass":true,"problems":[],"verdict":"failed-policy"}`; overall `accepted=12`, `total=12`, exit `0`.
- **Classification attack:** `measure_c2.py` defines served as 2xx status, `error is None`, not truncated, and media type `text/html`. These conditions hold for the committed and fresh observations. `page.html` exists and its SHA-256 equals `fetch.sha256`. The stored receipt is the reproduced policy audit, not a `not-served` receipt; no not-served misclassification was found.
- **Expected-canonical attack:** the frozen population says “no primary on record: self-canonical.” The SKILL.md map identifies the `.kimi.pro` SPA shell separately from the `.kimi.page` vault and explicitly warns that the same website ID appears on both hosts, so the shared ID does not demonstrate that `.kimi.page` is this surface's primary. No counterexample to the selected local policy value was found; the missing-link result simply cannot test it.

## Limits

One public GET only; no scripts or browser-rendered DOM were fetched or executed, and no Kimi chat/account interaction was performed. No upstream publisher/source configuration or independent primary-domain authority was examined. Findings are limited to this C2 surface and the committed policy/snapshot evidence. No tools were installed or updated.