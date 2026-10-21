## Verdict

Counterexample found: all four assigned HOLDs still hold, but the receipt omits a current-state check contradicted by the live page and omits a more operationally consequential source-gate assertion.

## Findings

### P2 — The selected claims skip a same-origin invariant that needs a current recheck

`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/vault-properties.md:43-46` says there are zero same-origin links in `PROPERTIES[]` and that the vault links only outward. This is omitted from the round-23 receipt. A fresh static GET shows that the `veigapunk` record in the veigapunk page's literal points to the page's own origin; the corresponding ufo-fsd page literal has no self-origin URL. Thus the documented cross-check is not currently true across both pages (or needs to be explicitly scoped as a 2026-09-28 historical baseline rather than left as an unqualified current property).

Exact check and output:

```sh
curl -sS --max-time 30 https://veigapunk.kimi.page/ -o /tmp/kake-r23w2-HoldVaultProperties-hvty/veigapunk.html
curl -sS --max-time 30 https://ufo-fsd.kimi.page/ -o /tmp/kake-r23w2-HoldVaultProperties-hvty/ufofsdpage.html
curl -sS --max-time 30 https://ufo-fsd.kimi.pro/ -o /tmp/kake-r23w2-HoldVaultProperties-hvty/proshell.html
S=/tmp/kake-r23w2-HoldVaultProperties-hvty node -e 'const fs=require("fs"),id="1a0acf59-c082-8794-8000-0000eaa74687";for(const [n,f,h] of [["veigapunk","veigapunk.html","veigapunk.kimi.page"],["ufo-fsd.page","ufofsdpage.html","ufo-fsd.kimi.page"]]){const b=fs.readFileSync(process.env.S+"/"+f,"utf8"),d=eval(b.match(/const PROPERTIES = (\[[\s\S]*?\]);/)[1]);console.log(n,JSON.stringify({entries:d.length,nullUrls:d.filter(x=>x.url===null).length,nonNullUrls:d.filter(x=>x.url!==null).length,lucario:/lucario/i.test(JSON.stringify(d)),siteIdOccurrences:b.split(id).length-1,sameOrigin:d.filter(x=>x.url&&new URL(x.url).host===h).map(x=>({name:x.name,url:x.url,status:x.status}))}));}const p=fs.readFileSync(process.env.S+"/proshell.html","utf8");console.log("pro",JSON.stringify({idOccurrences:p.split(id).length-1,jsRef:p.match(/src=\"([^\"]+\.js)\"/)?.[1],cssRef:p.match(/href=\"([^\"]+\.css)\"/)?.[1]}));'
```

```text
veigapunk {"entries":13,"nullUrls":3,"nonNullUrls":10,"lucario":false,"siteIdOccurrences":0,"sameOrigin":[{"name":"veigapunk","url":"https://veigapunk.kimi.page","status":"live"}]}
ufo-fsd.page {"entries":13,"nullUrls":3,"nonNullUrls":10,"lucario":false,"siteIdOccurrences":1,"sameOrigin":[]}
pro {"idOccurrences":1,"jsRef":"/assets/index-Bw9NLFv4.js","cssRef":"/assets/index-B-Hzbnm3.css"}
```

Smallest fix: add a round-23 receipt claim for this cross-check as current-state STALE (or state its historical date explicitly and separately record the live result); update the cross-check text to identify the veigapunk self-link.

### P2 — A more operationally load-bearing source gate is unverified and absent from the claim set

The unit says `sourceDir:null` is the single hard blocker and that `cmdUpdate` refuses without `sourceDir/index.html`, while `cmdRecreate` refuses when the slot serves live 200 (`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/vault-properties.md:49-51`). This governs whether the documented update/recreate recipes can execute, so it is more consequential than the selected literal counts and asset sizes. The expected source is absent locally and absent at the frozen candidate revision. A public page GET cannot establish those implementation branches; it must not be promoted to HOLD/STALE from live HTTP evidence. Add it as UNVERIFIABLE with the concrete reason that the source implementation is unavailable, or otherwise mark the recipe's source-level gate as unverified.

Exact check and output:

```sh
L=/home/vgpnk/Projects/shokunin/kake-shokunin; for p in fleet/vault-properties.json fleet/kimi-surface.mjs kimi-surface.mjs fleet.config.json; do if [ -e "$L/$p" ]; then echo "$p: PRESENT"; else echo "$p: ABSENT"; fi; done; git -C $L show 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd:fleet/vault-properties.json >/dev/null 2>&1 && echo "git@5e5afb9e fleet/vault-properties.json: PRESENT" || echo "git@5e5afb9e fleet/vault-properties.json: ABSENT"; git -C $L show 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd:fleet/kimi-surface.mjs >/dev/null 2>&1 && echo "git@5e5afb9e fleet/kimi-surface.mjs: PRESENT" || echo "git@5e5afb9e fleet/kimi-surface.mjs: ABSENT"
```

```text
fleet/vault-properties.json: ABSENT
fleet/kimi-surface.mjs: ABSENT
kimi-surface.mjs: ABSENT
fleet.config.json: ABSENT
git@5e5afb9e fleet/vault-properties.json: ABSENT
git@5e5afb9e fleet/kimi-surface.mjs: ABSENT
```

## Checked and held

- **c1 — HOLD stands.** Fresh GETs returned HTTP 200: veigapunk `10,059` bytes, SHA-256 `a0a7f33aba443a85a4952a0bf57aa52947fdf95638b5ac7aba1c7d92b87a92fb`; ufo-fsd page `9,966` bytes, SHA-256 `d93d6a0c00e773f74389ebc6d052773262052d6a0fc6b6a21581f1c12cb3920c`. Both parsed literals have 13 records, 3 null and 10 non-null URLs, and no `lucario`.
- **c6 — HOLD stands.** The exact ID `1a0acf59-c082-8794-8000-0000eaa74687` occurs once in the ufo-fsd page body and once in the ufo-fsd pro shell. The current veigapunk page has a different website ID; it is outside c6's two specified surfaces.
- **c7 — HOLD stands.** Fresh GETs returned HTTP 200: shell 612 bytes (SHA-256 `1df92e30ba5a76e69a863a729326949871d3d83e290935d596f6cd9b7d65ab8c`), JS 739,018 bytes (`bd781cd41b224da81bc8e7429760ed0158f354777d25f9ad9beb943bd2b52267`), CSS 82,871 bytes (`5831ff6a4f0392a2a04a710023e938f8389b567b4c67eb52d9c226eee83b3a64`). The shell references the exact JS and CSS paths in the claim.
- **c8 — HOLD stands as a local-presence observation.** Both expected source paths and `kimi-surface.mjs` were absent on disk and absent at the frozen revision.
- None of the four assigned receipt claims is UNVERIFIABLE; no assigned UNVERIFIABLE was incorrectly treated as live-decidable. The omitted source gate above is not decidable from a public live surface.

## Limits

Read-only checks only; no source or lane files other than this report were changed. The full 17-unit `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py` counter was not run; this review is scoped to `vault-properties`. The source-level `cmdUpdate`/`cmdRecreate` behavior and historical source evidence cannot be confirmed from the available lane tree or public GETs.
