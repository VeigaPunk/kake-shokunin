## Verdict

None — no counterexample was found in this probe. **Pre-run expectation:** Eleventy would build two pages with explicit, correctly matching canonical links; the audit would accept the body SVG and form controls after the closed heads and return `clean`, `pagesChecked: 2`, with no findings. The observed build and audit matched that expectation.

## Findings

None (no P0–P3 findings). This confirms operability for this generated fixture only; it is not evidence of broad generator compatibility.

## Checked and held

- Kept the project and generated pages in `/tmp/kake-r23w2-ExecRealGeneratorPages-8fEx`; did not modify production files.
- Generator: Eleventy (`@11ty/eleventy`) v3.1.2. Provisioned/resolved through `npx` using npm's official registry (`https://registry.npmjs.org/`); npm cache reported the `@11ty/eleventy` v3.1.2 tarball. Reason: exercise a real static site generator without pacman. No pacman or global install was used.
- Build command:
  ```
  npx --yes @11ty/eleventy@3.1.2 --version && npx --yes @11ty/eleventy@3.1.2 --input=src --output=site
  ```
  Exact output:
  ```
  3.1.2
  [11ty] Writing ./site/index.html from ./src/index.njk
  [11ty] Writing ./site/contact/index.html from ./src/contact/index.njk
  [11ty] Wrote 2 files in 0.02 seconds (v3.1.2)
  ```
- Read the generated `site/index.html` and `site/contact/index.html`: both contain the expected canonical link in an explicitly closed `<head>`; the home page includes an inline SVG icon and search/checkbox inputs, and the contact page includes an email input.
- Audit command:
  ```
  python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23w2-ExecRealGeneratorPages-8fEx/manifest.json
  ```
  Exact stdout:
  ```
  {"findings":[],"pagesChecked":2,"verdict":"clean"}
  ```
  The command completed successfully (clean verdict / exit 0).

## Limits

This is a two-page synthetic fixture using `example.test`; it exercises generated source HTML, not live HTTP responses, browser parsing/rendering, search-engine canonical selection, publishing readiness, or other templates/generators. No network request was made to the example domain.
