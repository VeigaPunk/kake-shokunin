## Verdict

All 12 pre-derived expected `clean` verdicts matched the public CLI: each returned exit 0 with `pagesChecked: 1` and no findings. Coverage is two representative static-page fixtures per requested family (Hugo, Jekyll, Astro, Eleventy, Next static export, and hand-written HTML). Every `page.html` includes inline SVG, self-closed `<input />` and `<img />`, a preload link, and JSON-LD; each has its own v1 `manifest.json`.

Fixtures were created under `/tmp/kake-r23-ExecRealPageFixtures-clone/fixtures/realistic-sites/` in a clone whose observed HEAD was `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`.

## Findings

None (P0–P3). The CLI's observed verdict, exit, pages checked, and findings matched the pre-run derivation for all 12 cases.

## Checked and held

Expected outcomes were derived from the explicit closed `<head>`, one canonical matching the expected URL (including Hugo's root `<base>` plus relative canonical), supported head children, and well-closed inline SVG/body void elements before execution. Expected and observed outcomes:

| Fixture | Family / page | Document URL / expected canonical | Expected | Observed CLI |
|---|---|---|---|---|
| `hugo-home` | Hugo home | `https://hugo.example.test/` | clean | clean; exit 0; 1 page; no findings |
| `hugo-article` | Hugo guide | `https://hugo.example.test/guides/choosing-a-trail/` | clean | clean; exit 0; 1 page; no findings |
| `jekyll-home` | Jekyll home | `https://jekyll.example.test/` | clean | clean; exit 0; 1 page; no findings |
| `jekyll-post` | Jekyll post | `https://jekyll.example.test/2026/10/studio-notes/` | clean | clean; exit 0; 1 page; no findings |
| `astro-home` | Astro home | `https://astro.example.test/` | clean | clean; exit 0; 1 page; no findings |
| `astro-docs` | Astro docs | `https://astro.example.test/docs/installation/` | clean | clean; exit 0; 1 page; no findings |
| `eleventy-home` | Eleventy home | `https://11ty.example.test/` | clean | clean; exit 0; 1 page; no findings |
| `eleventy-archive` | Eleventy archive | `https://11ty.example.test/archive/2026/` | clean | clean; exit 0; 1 page; no findings |
| `next-home` | Next static export home | `https://next.example.test/` | clean | clean; exit 0; 1 page; no findings |
| `next-docs` | Next static export docs | `https://next.example.test/docs/getting-started/` | clean | clean; exit 0; 1 page; no findings |
| `handwritten-home` | Hand-written home | `https://juniper.example.test/` | clean | clean; exit 0; 1 page; no findings |
| `handwritten-about` | Hand-written about | `https://juniper.example.test/about/` | clean | clean; exit 0; 1 page; no findings |

Exact command run:

```sh
for d in /tmp/kake-r23-ExecRealPageFixtures-clone/fixtures/realistic-sites/*; do if test -f "$d/manifest.json"; then printf '%s ' "${d##*/}"; python3 /tmp/kake-r23-ExecRealPageFixtures-clone/scripts/canonical_audit.py --manifest "$d/manifest.json" --json; result=$?; printf 'exit=%s\n' "$result"; fi; done
```

Exact observed output:

```text
astro-docs {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
astro-home {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
eleventy-archive {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
eleventy-home {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
handwritten-about {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
handwritten-home {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
hugo-article {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
hugo-home {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
jekyll-home {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
jekyll-post {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
next-docs {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
next-home {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
```

Fixture archive: 3,849 bytes, SHA-256 `f34a28b220999bbe7de5c01b3f81138975fcf9357a2d1f1b2a0626ee30f989e8`. It contains the 12 fixture directories, each with `page.html` and `manifest.json`.

```base64
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
```

## Limits

These are realistic-shaped synthetic static outputs, not pages built by installing or running the named framework generators; `.test` URLs are fixture-only and all CLI evaluation was offline. No framework tools or other packages were installed. This checks the candidate CLI's parser and canonical policy against the requested HTML patterns, not live HTTP availability, publishing readiness, or search-engine canonical selection. No production source files were changed; all fixture files and the archive are in `/tmp`, and the only lane write is this report.
