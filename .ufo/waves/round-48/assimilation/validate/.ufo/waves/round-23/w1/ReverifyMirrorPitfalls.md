## Verdict

C1 freshness receipt for `mirror-pitfalls`: 2 claims HOLD, 2 STALE, and 3 UNVERIFIABLE. This is scoped re-verification evidence, not independent admission. I used the frozen base `b5d599e19bead54b96f589444e9ec64cdf67c28a` for anchors; the observed lane HEAD was `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`.

## Findings

- **P2 — STALE: the no-hyphen Plazir-27 site is not currently reachable at its name-derived Kimi URL.** Exact GET command: `curl --max-time 20 --silent --show-error --location --output /dev/null --write-out 'status=%{http_code} url=%{url_effective} bytes=%{size_download}\n' 'https://plazir27runson.kimi.page/'` (same command run in the listed-URL loop under Checked and held). Exact observed output: `status=404 url=https://plazir27runson.kimi.page/ bytes=13409`. The paired hyphenated URL returned `status=200 url=https://plazir27runs-on.kimi.page/ bytes=63421`; its page title is `PLAZIR-27 — the ufo-fsd charter`. Impact: freshness of the name-to-live-site mapping. Smallest fix: retire the claim that both are currently reachable sites, or preserve it explicitly as historical and re-verify the no-hyphen mapping before using it.
- **P2 — STALE: the frozen-copy/canonical repository relationship is not present in the checked project workspace.** Exact command: `for p in /home/vgpnk/Projects/plazir-15-site/speedrun /home/vgpnk/Projects/ds4cc-marketplace/speedrun /home/vgpnk/Projects/ufo-fsd-alpha/ufofsdbeta /home/vgpnk/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review /home/vgpnk/Projects/ufofsdbeta /home/vgpnk/Projects/ufofsdbeta-kimi-review; do if test -e "$p"; then printf 'PRESENT %s\n' "$p"; else printf 'ABSENT %s\n' "$p"; fi; done`. Exact observed output for the two asserted speedrun paths: `ABSENT /home/vgpnk/Projects/plazir-15-site/speedrun` and `ABSENT /home/vgpnk/Projects/ds4cc-marketplace/speedrun`. Impact: freshness of the claimed frozen copy and canonical target. Smallest fix: retire this live-local-path assertion until the source trees are available; do not infer the `rel=canonical` relationship from the missing trees.
- **P3 — UNVERIFIABLE: the two 404 responses do not establish Kimi chat bindings.** Exact GET command: the same `curl --max-time 20 --silent --show-error --location --output /dev/null --write-out ...` command with `https://plazir15.kimi.page/` and `https://charter-ufo-fsd.kimi.page/`. Exact observed output: `status=404 url=https://plazir15.kimi.page/ bytes=13409`; `status=404 url=https://charter-ufo-fsd.kimi.page/ bytes=13409`. Impact: freshness of the no-bound-chat assertion. Smallest fix: keep only the publicly observed 404 fact; do not state the internal binding without a permitted public read-only evidence surface.
- **P3 — UNVERIFIABLE: the review snapshot's non-git status and filesystem-wide absence cannot be decided from the relative path in the entry.** Exact command: the `test -e` loop above for `/home/vgpnk/Projects/ufofsdbeta-kimi-review` and `/home/vgpnk/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review`; exact output: `ABSENT /home/vgpnk/Projects/ufofsdbeta-kimi-review`; `ABSENT /home/vgpnk/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review`. A project-root glob also returned `No files found matching pattern` for `/home/vgpnk/Projects/**/ufofsdbeta-kimi-review`. Impact: freshness of the snapshot-as-source warning. Smallest fix: state only these checked absolute roots as absent, or supply the exact canonical path before making a filesystem-wide absence/non-git claim.
- **P3 — UNVERIFIABLE: the served SDK-seed script is observable, but the full byte-rewriting/hash-comparison conclusion needs paired pre-publish bytes.** Exact GET: `https://ufo-fsd.kimi.pro/` (raw response inspected read-only). Exact observed output includes `status=200 ... bytes=612` and `<script src="https://www.kimi.com/sdk-seed.js" ... data-kimi-website-env="published"></script>`; no corresponding original source bytes were available. Impact: freshness of the byte-rewrite mechanism and digest recipe. Smallest fix: restrict the statement to the observed SDK-seed injection until a source/served byte pair can be compared.

## Checked and held

- Read the complete unit and obtained its anchor text from `git show b5d599e19bead54b96f589444e9ec64cdf67c28a:corpus/knowledge/mirror-pitfalls.md`. The unit's named source files were not present at the checked locations: `/home/vgpnk/Projects/shokunin/fleet/kimi-surface-ops.md`, `/home/vgpnk/Projects/shokunin/fleet.dedupe-report.md`, and the lane-local equivalents returned `ABSENT`; `/home/vgpnk/Projects/shokunin/local/fleet-analysis` was empty.
- `ufo-fsd.kimi.pro` (HOLD): exact public GET output was `status=200 url=https://ufo-fsd.kimi.pro/ bytes=612`. The raw HTML has `<title>DS4CC</title>`, a module script at `/assets/index-Bw9NLFv4.js`, `<div id="root"></div>`, and the published `sdk-seed.js` script, consistent with a 612-byte SPA shell.
- `ufo-fsd.kimi.page` and `ufofsd.kimi.page` (HOLD): GET outputs were respectively `status=200 url=https://ufo-fsd.kimi.page/ bytes=9966` and `status=200 url=https://ufofsd.kimi.page/ bytes=1913`. The first page title is `VEIGAPUNK — Central Vault`; the second is `ufofsd — work in progress` and says `Work in progress — the full ds4cc.com mirror lands here. ETA WINTER 2027`. These distinguish the current public representations.
- The exact GET loop used for the page measurements was: `for u in https://ufo-fsd.kimi.page/ https://ufofsd.kimi.page/ https://ufo-fsd.kimi.pro/ https://plazir15.kimi.page/ https://charter-ufo-fsd.kimi.page/ https://plazir27runson.kimi.page/ https://plazir27runs-on.kimi.page/; do printf '\n%s\n' "$u"; curl --max-time 20 --silent --show-error --location --output /dev/null --write-out 'status=%{http_code} url=%{url_effective} bytes=%{size_download}\n' "$u" || printf 'curl_exit=%s\n' "$?"; done`.

### C1 receipt

```json
{
  "unit": "mirror-pitfalls",
  "path": "corpus/knowledge/mirror-pitfalls.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "`ufo-fsd.kimi.pro` = 612B SPA shell.",
      "claim": "The public root currently serves a 612-byte HTML client SPA shell.",
      "surface": "GET https://ufo-fsd.kimi.pro/",
      "method": "GET",
      "observation": "status=200 url=https://ufo-fsd.kimi.pro/ bytes=612; raw HTML contains <title>DS4CC</title>, a module script at /assets/index-Bw9NLFv4.js, <div id=\"root\"></div>, and https://www.kimi.com/sdk-seed.js.",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "`ufo-fsd.kimi.page` = vault twin; `ufofsd.kimi.page` = frozen landing;",
      "claim": "The two named public roots currently serve distinct pages: a central vault and a work-in-progress ufofsd landing page.",
      "surface": "GET https://ufo-fsd.kimi.page/; GET https://ufofsd.kimi.page/",
      "method": "GET",
      "observation": "status=200 url=https://ufo-fsd.kimi.page/ bytes=9966; title `VEIGAPUNK — Central Vault`. status=200 url=https://ufofsd.kimi.page/ bytes=1913; title `ufofsd — work in progress`; text `Work in progress — the full ds4cc.com mirror lands here. ETA WINTER 2027`.",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "plazir15.kimi.page and charter-ufo-fsd.kimi.page have no bound chat;",
      "claim": "The two named Kimi sites have no chat bound to them.",
      "surface": "GET https://plazir15.kimi.page/; GET https://charter-ufo-fsd.kimi.page/",
      "method": "GET",
      "observation": "status=404 url=https://plazir15.kimi.page/ bytes=13409; status=404 url=https://charter-ufo-fsd.kimi.page/ bytes=13409. The public responses do not expose chat-binding state.",
      "verdict": "UNVERIFIABLE",
      "reason": "Unauthenticated public GET establishes only the current 404 responses, not the private Kimi chat-to-site binding. No authenticated API or browser operation was used."
    },
    {
      "id": "c1",
      "anchor": "plazir27runson (Night Trilogy) ≠ plazir27runs-on (charter doctrine) — different sites, hyphen matters.",
      "claim": "The no-hyphen Night Trilogy and hyphenated charter names identify two currently reachable Kimi sites.",
      "surface": "GET https://plazir27runson.kimi.page/; GET https://plazir27runs-on.kimi.page/",
      "method": "GET",
      "observation": "status=404 url=https://plazir27runson.kimi.page/ bytes=13409; status=200 url=https://plazir27runs-on.kimi.page/ bytes=63421; the latter page title is `PLAZIR-27 — the ufo-fsd charter`.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, https://plazir27runson.kimi.page/ returns HTTP 404 while https://plazir27runs-on.kimi.page/ returns HTTP 200 with title `PLAZIR-27 — the ufo-fsd charter`, so the source cannot label both as currently reachable Kimi sites."
    },
    {
      "id": "c1",
      "anchor": "`plazir-15-site/speedrun/` = frozen 3-run copy; canonical is `ds4cc-marketplace/speedrun/` (`rel=canonical` in the plazir copy confirms).",
      "claim": "The frozen three-run copy and its canonical repository path are present locally, with a rel=canonical link from the copy.",
      "surface": "test -e /home/vgpnk/Projects/plazir-15-site/speedrun; test -e /home/vgpnk/Projects/ds4cc-marketplace/speedrun",
      "method": "test -e",
      "observation": "ABSENT /home/vgpnk/Projects/plazir-15-site/speedrun; ABSENT /home/vgpnk/Projects/ds4cc-marketplace/speedrun.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, neither /home/vgpnk/Projects/plazir-15-site/speedrun nor /home/vgpnk/Projects/ds4cc-marketplace/speedrun exists under /home/vgpnk/Projects, so this workstation cannot substantiate the asserted copy or canonical link."
    },
    {
      "id": "c1",
      "anchor": "`ufofsdbeta-kimi-review/` = non-git review snapshot, never a source — **absent from FS since 2026-09-28T23:51:31Z** (r15 sweep).",
      "claim": "The named tree is a non-git review snapshot, is not a source, and has remained absent from the filesystem since the r15 sweep.",
      "surface": "test -e /home/vgpnk/Projects/ufofsdbeta-kimi-review; test -e /home/vgpnk/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review; glob /home/vgpnk/Projects/**/ufofsdbeta-kimi-review",
      "method": "test -e",
      "observation": "Both exact test -e candidates returned ABSENT; the project-root glob returned `No files found matching pattern`.",
      "verdict": "UNVERIFIABLE",
      "reason": "The unit gives only a relative directory name and makes a filesystem-wide absence/non-git assertion. The checked project-root candidates were absent, but without an exact canonical absolute path or the tree itself I cannot verify the global absence or its former git status."
    },
    {
      "id": "c1",
      "anchor": "**Bytes are rewritten.** sdk-seed.js injection + cfemail/entity rewriting",
      "claim": "Kimi's served bytes are rewritten by the listed mechanisms, making source-versus-served SHA comparison unsuitable without normalization.",
      "surface": "GET https://ufo-fsd.kimi.pro/ plus its raw response; paired pre-publish source bytes unavailable",
      "method": "GET",
      "observation": "The raw 612-byte response includes the published `https://www.kimi.com/sdk-seed.js` script; no corresponding original source bytes were found for a byte comparison.",
      "verdict": "UNVERIFIABLE",
      "reason": "The public response confirms SDK-seed injection on this page, but neither the named historical source documents nor paired pre-publish bytes are available to verify cfemail/entity rewriting or the broader digest conclusion."
    }
  ]
}
```

## Limits

- Skipped **“No directory indexes” / `dir/` 404 vs `dir/file` 200 / `href="snake/"`**: the entry gives no concrete directory/file pair or live host path to test; the named historical failure-mode source was absent, so probing a guessed route would not verify the claim.
- Skipped **one chat per publish slot, hot-swapping updates, banned fire targets, `publishedUrl` via `GetWebsiteByChatID` versus `hosts[]`, `recreate`/`rebuild` instead of `update`, and `.kimi.pro` Function-Compute/unclaimed-preview routing** except the public 404 and 612-byte shell observations above. These claims require private binding/control-plane evidence or a publish/fire mutation; neither an authenticated API nor a browser operation is permitted here.
- Skipped **the historical `cfemail`/entity rewriting details and the normalized-digest + marker + vintage recipe** beyond recording the SDK-seed script: no paired original response/source bytes were available. The claim is recorded UNVERIFIABLE.
- Skipped the **Browser/CDP lane** claims (`webzites` lease/release and one-op serialization; `t<N>` renumbering and `/json/list`; `agent-browser open --wait`; menu Enter behavior; composer selector/textarea/send-button behavior; `browser status` 401/200 retry rule; `SingletonLock`/`browser ensure`/`setsid`; chat-fire metering and preflight). The entry names no source for these bullets, and checking them would require a browser/CDP session or an account/chat operation, neither used here.
- No tools were installed or updated. No build, lint, formatter, test, browser, authentication, publishing, or fire operation was run.