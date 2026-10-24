Verdict: **valid control** — M10 breaks contract sentence 25, the reference obeys it; the divergence is contract-determined, evidence kill rule (1) fired correctly.

Receipt (allowed fields): `w1a3-MutUrlAuthority__M10`, passed 24/24, met true, toolSha256 `aa54ad12…53f5a41` = `sha256sum` of `mutants/M10.py`. Reference `663e051e…d69f8`.

Diff vs `/fast/scratch/hyaku/kake-r39a3w1/shared/reference.py` (`diff -u`, exit 1, exactly one line, line 149):
```diff
-    smdir = sm[3][: sm[3].rfind("/") + 1]
+    smdir = sm[3].rstrip("/")[: sm[3].rstrip("/").rfind("/") + 1]
```

Witness (hashes match mutants.json: manifest `c1d2c2c0…de1`, sitemap `fa574e60…d9`):
`{"version":1,"checks":[{"id":"w","file":"sitemap.xml","sitemapUrl":"https://example.test/maps/"}]}` +
`<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.test/a</loc></url></urlset>`

Runs (`timeout 60 prlimit --as=4000000000 -- python3 -B <tool> --manifest witnesses/M10/manifest.json`):
- reference.py → exit 1:
  `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "w", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}`
- mutants/M10.py → exit 0:
  `{"version": 1, "verdict": "clean", "checks": [{"id": "w", "status": "clean", "error": null, "findings": []}]}`

Sentence 25: "In a `urlset`, a `loc` whose scheme, host or port differs from the `sitemapUrl`'s, or whose path (an empty path read as `/`) does not start with the `sitemapUrl`'s directory — its path up to and including the last `/` — gives `loc_out_of_scope`."

Reasoning: the `sitemapUrl` path is `/maps/`; its last `/` is the trailing character, so its directory is `/maps/` itself. The loc path `/a` does not start with `/maps/` → sentence 25 requires `loc_out_of_scope` at entry 1; sentences 33–34 then require `failed-policy`, exit 1 — exactly the reference output. M10 rstrips `/` from `/maps/` to `/maps`, whose last `/` is index 0, yielding smdir `/`; every absolute loc path starts with `/`, so the scope rule never fires for directory-form sitemapUrls → `clean`, exit 0, violating sentence 25. Scheme/host/port are equal (sentence 24) and the loc is absolute (sentence 22), so the path-prefix clause is decisive and the contract fully determines the witness output. Not equivalent (outputs differ on this input); not contract-silent. The mutation is inert only when the `sitemapUrl` path lacks a trailing `/`, so this witness is the correct discriminator.
