## Verdict

No counterexample to the frozen C2 receipt rules. The selected `expectedCanonical` is supported by the local property map, and the `not-served` receipt matches the current HTTP status under the counter's explicit 2xx-HTML definition. The surface is not currently canonical-audited: the committed candidate has no `page.html` for this 404 response.

## Findings

- **P3 — Interpretation caveat, not a falsifying defect (C2 / operability).** `measure_c2.py` reports this row `pass: true` because its receipt/status checks reproduce; that does not mean the surface passed canonical policy. A GET did return a 13,409-byte HTML error body with HTTP 404. If “not-served” is read as “no HTTP body was served,” the label is imprecise; in this counter it means the response is outside the 2xx `text/html` audit path. The output retains `verdict: not-served`, so this is not a hidden clean verdict.
  - **Exact GET command** (the one GET made; temporary directory expanded to `/tmp/kake-r23w2-RecheckPlazir27Kimi-SQ4X`):
    ```sh
    d=$(mktemp -d /tmp/kake-r23w2-RecheckPlazir27Kimi-XXXX) && curl --silent --show-error --location --max-redirs 10 --dump-header "$d/headers.txt" --output "$d/body.bin" --write-out 'status=%{http_code}\nfinalUrl=%{url_effective}\ncontent_type=%{content_type}\n' 'https://plazir27.kimi.page/' && printf 'sha256=' && sha256sum "$d/body.bin" | cut -d ' ' -f 1 && printf 'bytes=' && wc -c < "$d/body.bin" && printf 'scratch=%s\n' "$d"
    ```
  - **Exact output:**
    ```text
    status=404
    finalUrl=https://plazir27.kimi.page/
    content_type=text/html; charset=utf-8
    sha256=93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966
    bytes=13409
    scratch=/tmp/kake-r23w2-RecheckPlazir27Kimi-SQ4X
    ```
    These status, final URL, content-type, and SHA-256 values match `fetch.json`; no body drift was observed. A changed body would be drift, not by itself a canonical defect.
  - **Committed snapshot check:** `git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -e 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd:.ufo/waves/round-23/live/plazir27-kimi/page.html` emitted `fatal: path '.ufo/waves/round-23/live/plazir27-kimi/page.html' does not exist in '5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd'` (exit 128). The on-disk surface directory likewise contains only `fetch.json` and `audit.json`.
  - **Policy attack:** `.ufo/waves/round-23/c2-population.json:44-47` expects `https://veigapunk.github.io/charter-ufo-fsd/`; `SKILL.md:18` labels that GHP front the canonical document and says all Kimi variants use it as `rel=canonical`. The property-map C1 receipt `property-map.json` c46 records the same policy. I found no evidence against that local expected value. However, this is policy provenance, not a live declaration: the fresh provider 404 head has `<title>404</title>` and no canonical link. The candidate `page.html` needed for the requested committed-head inspection is absent.
  - **Diagnostic, not a target-site verdict:** I copied the fresh 404 body into the temporary directory and ran `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23w2-RecheckPlazir27Kimi-SQ4X/manifest.json --json`. Exact output was `{"findings":[{"id":"canonical_missing","page":"https://plazir27.kimi.page/"}],"pagesChecked":1,"verdict":"failed-policy"}` and `audit_exit=1`. This is the result if the provider's 404 document is forced through the HTML policy; it does not show the unavailable charter mirror's canonical is wrong.
  - **Counter reproduction:** ran `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`. Exact target row from its output: `{"id":"plazir27-kimi","pass":true,"problems":[],"verdict":"not-served"}`; overall output was `accepted: 12`, `total: 12`.
  - **Smallest fix:** no classifier or `expectedCanonical` change is warranted by this evidence. Keep summaries explicit that `accepted` counts reproducible receipts, not canonical-clean pages; if desired, call this state “unavailable/non-2xx” to avoid implying that no HTTP body was returned.

## Checked and held

- `fetch.json`: status 404, final URL `https://plazir27.kimi.page/`, content type `text/html; charset=utf-8`, SHA-256 `93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966`, 13,409 bytes. `audit.json`: `verdict=not-served`, `status=404`, `exit=null`, `error=null`.
- `measure_c2.py` defines served as status 2xx, no error/truncation, and `text/html`; it requires no `page.html` and a matching not-served receipt otherwise. Thus the receipt classification matches its specified rule. The live snapshot tool likewise stores page HTML only for 2xx `text/html`.
- No redirects occurred in the fresh GET. No body drift. No change to the expected canonical is indicated.

## Limits

- The required *committed* `page.html` head cannot be inspected because it is absent at the frozen revision. The head observation and diagnostic audit above use the one fresh GET body instead.
- The 404 body is Kimi's error document, not evidence of the canonical tag that a restored charter mirror would publish. No browser-rendered behavior, Kimi publication binding, or search-engine canonical selection was tested.
- No LSP device was exposed in the available tool routes; source claims use direct file reads. No tools were installed.
