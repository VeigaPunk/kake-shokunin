Axes: freshness (primary) and sitemap/tree parity.

## Finding

- At `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`: 100 sitemap locs; 86/86 root or directory locs map to `index.html`; 14/14 explicit file locs map directly to tracked HTML; 100 mapped, 0 unmapped. There are 102 tracked `.html` files. Two are raw unlisted HTML; after excluding the redirect alias below, one unlisted page remains: `benchmarks/benxshitter-frontier.html`.
- At `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`: 97 sitemap locs; 83/83 root or directory locs map to `index.html`; 14/14 explicit file locs map directly to tracked HTML; 97 mapped, 0 unmapped. There are 99 tracked `.html` files. Two are raw unlisted HTML; after the same exclusion, one unlisted page remains: `benchmarks/benxshitter-frontier.html`.
- Exclusion rule: exclude an unlisted HTML file only when it has a meta-refresh target and canonical URL resolving to the same HTTPS `ds4cc.com` path, and that canonical path is itself in the sitemap. The sole excluded file is `burnerchrome.html`, aliasing `/burnerchrome/`. All explicit `.html` sitemap locs are mapped to their file path rather than incorrectly treated as directory locs.

## Evidence

- Analysis script: `/fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/sitemap_tree_parity.py` (mapping and exclusions: lines 40-62, 65-133); SHA-256 `9be7b6972e0f54b497b13ee6710105116cffd1615281796fc4921bdb1a40a4f8`.
- Exact final stdout: `/fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/sitemap_tree_parity.out`; lines 1-15 (fresh), 17-32 (baseline); SHA-256 `3554a87a54c4f4ea10cdda648e1a0ea8b440d0dafa749c0550a824e11a4248cf`.
- Fresh clone command: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && mkdir -p /fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/tmp && export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/tmp && git clone -q https://github.com/VeigaPunk/ds4cc-marketplace.git /fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/repo && git -C /fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/repo checkout -q 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 && git -C /fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/repo rev-parse HEAD` — exit 0; stdout `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`.
- Final measurement command: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/tmp && set -o pipefail && python3 -B /fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/sitemap_tree_parity.py /fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/repo | tee /fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/sitemap_tree_parity.out` — exit 0. Output is preserved verbatim at the evidence path above.
- Hash command: `sha256sum /fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/sitemap_tree_parity.py /fast/scratch/hyaku/kake-r33/w1/ExecSitemapTreeParity/sitemap_tree_parity.out` — exit 0; hashes recorded above.

No live-site requests or tool installs. No builds, tests, linters, or formatters were run. This establishes tracked-tree parity only; deployed routing was not tested. No blockers.