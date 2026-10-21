## Verdict

On 2026-10-21, one read-only GET of `https://veigapunk.kimi.page/` returned HTTP 200 at the same final URL. By eye, the page's explicit `<head>` closes at snapshot line 159 and contains no canonical declaration. Before running the audit, the frozen round-22 head-only policy therefore implied exit 1, `failed-policy`, finding `canonical_missing`; the audit returned exactly that.

`expectedCanonical=https://veigapunk.kimi.page/` is the right **local policy** on the available record: the round-23 C2 population says “no primary on record: self-canonical”; the property map identifies this URL as the vault index without naming another primary; and the live page titles itself “VEIGAPUNK — Central Vault.” The problem is the missing page declaration, not a demonstrated wrong expected URL. This says nothing about Google's selected canonical. This scout report is evidence only, not independent admission.

## Findings

### P2 — Live vault page lacks the required head canonical (C2 operability)

- **Exact GET command:** `T=$(mktemp -d /tmp/kake-r23-VaultIndexKimi-XXXX) && echo "TMP=$T" && curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D "$T/h" -o "$T/b" -w 'status=%{http_code} final_url=%{url_effective} content_type=%{content_type} num_redirects=%{num_redirects}\n' https://veigapunk.kimi.page/ && sha256sum "$T/b" && wc -c "$T/b"`
- **Exact observed output:**
  - `TMP=/tmp/kake-r23-VaultIndexKimi-EExH`
  - `status=200 final_url=https://veigapunk.kimi.page/ content_type=text/html num_redirects=0`
  - `a0a7f33aba443a85a4952a0bf57aa52947fdf95638b5ac7aba1c7d92b87a92fb  /tmp/kake-r23-VaultIndexKimi-EExH/b`
  - `10059 /tmp/kake-r23-VaultIndexKimi-EExH/b`
  - Saved response headers begin `HTTP/2 200` and `content-type: text/html`.
- **Head inspection:** the fetched document has `<title>VEIGAPUNK — Central Vault</title>` and the Kimi SDK/canary metadata before `</head>` at line 159. No canonical occurs in the head (or elsewhere in the body); there is no declared canonical for this policy to compare.
- **Pre-audit prediction:** exactly one canonical in the explicit head is required; with none present, expected finding ID `canonical_missing` and exit 1 (`failed policy`).
- **Exact audit command:** `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-VaultIndexKimi-EExH/manifest.json --json`
- **Exact observed stdout:** `{"findings":[{"id":"canonical_missing","page":"https://veigapunk.kimi.page/"}],"pagesChecked":1,"verdict":"failed-policy"}`; process exit: `1`. This matches the pre-audit prediction.
- **Smallest upstream fix (documented only; not applied):** in the authoritative page source/template, add exactly one `<link rel="canonical" href="https://veigapunk.kimi.page/">` inside `<head>`, then have the authorized operator publish and recheck. The property map says the source is “none on disk”; no source edit or publish was attempted. Its explicit warning says never fire into the mapped chat because it hot-swaps the live vault, so no Kimi chat was contacted.

## Checked and held

- Read frozen `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json`: policy is “Exactly one canonical link in explicit head per page,” with URL resolution/normalization and exact expected-value comparison. The frozen finding list includes `canonical_missing`; the manifest was version 1 with the live URL, saved body file `b`, and the C2 expected value.
- Read `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/c2-population.json`: `vault-index-kimi` has URL and `expectedCanonical` both `https://veigapunk.kimi.page/`, with basis `no primary on record: self-canonical`.
- The saved body is `/tmp/kake-r23-VaultIndexKimi-EExH/b`; manifest is `/tmp/kake-r23-VaultIndexKimi-EExH/manifest.json`. The fetch used one GET and no credentials, cookies, or write/publish action.
- Read-only lane HEAD probe returned `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`; the audit above invoked the script at the requested lane path. No git/jj mutation was made.
- C1 property-map receipt below uses anchors from `SKILL.md` at frozen base `b5d599e19bead54b96f589444e9ec64cdf67c28a`. The live URL is reverified. The “none on disk” source assertion and chat hot-swap behavior cannot be independently resolved from this public GET; no source path is named, and testing the chat warning is prohibited.

```json
{
  "unit": "property-map",
  "path": "SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "| vault index | `https://veigapunk.kimi.page/` |",
      "claim": "The property-map vault-index URL still serves a live page at its mapped URL.",
      "surface": "https://veigapunk.kimi.page/",
      "method": "GET",
      "observation": "status=200 final_url=https://veigapunk.kimi.page/ content_type=text/html num_redirects=0; sha256 a0a7f33aba443a85a4952a0bf57aa52947fdf95638b5ac7aba1c7d92b87a92fb; 10059 bytes",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "| `https://veigapunk.kimi.page/` | none on disk |",
      "claim": "The vault has no local source directory available for maintenance.",
      "surface": "/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:21",
      "method": "read",
      "observation": "| vault index | `https://veigapunk.kimi.page/` | none on disk | Kimi surface, chat `1a0c20ea-6372…` — NEVER fire into this chat, it hot-swaps the live vault |",
      "verdict": "UNVERIFIABLE",
      "reason": "The row names no concrete source path to test; the public page cannot establish whether an unregistered local source now exists, and guessing a filesystem scope would not be a bounded re-verification."
    },
    {
      "id": "c1",
      "anchor": "Kimi surface, chat `1a0c20ea-6372…` — NEVER fire into this chat, it hot-swaps the live vault",
      "claim": "Firing into the named chat can hot-swap the live vault.",
      "surface": "/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:21",
      "method": "read",
      "observation": "| vault index | `https://veigapunk.kimi.page/` | none on disk | Kimi surface, chat `1a0c20ea-6372…` — NEVER fire into this chat, it hot-swaps the live vault |",
      "verdict": "UNVERIFIABLE",
      "reason": "Verifying that side effect would require a chat operation, which is prohibited; the public page does not expose the chat-to-site binding."
    }
  ]
}
```

## Limits

This is one point-in-time GET and a static, head-only local-policy audit. It does not establish Google canonical selection, JS-rendered or HTTP-header canonical behavior, chat binding, source-directory absence, or publishing readiness. No upstream change, Kimi chat operation, or publish was performed; no tools were installed or updated.
