# ReviewS065RowTruth — every cell of SOURCES row S065 at 0a0acfb1

Attack: independently verify each cell of `corpus/SOURCES.md` row S065 (line 73)
at lane tip `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` against fresh upstream.

## Setup (all exit 0)

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r33/w2/ReviewS065RowTruth/clone` then `checkout -q 0a0acfb1…` → HEAD `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`.
- `git clone -q https://github.com/VeigaPunk/ds4cc-marketplace.git /fast/scratch/hyaku/kake-r33/w2/ReviewS065RowTruth/upstream` → HEAD `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`.
- `git -C /fast/scratch/hyaku/kake-r33/ds4cc-upstream rev-parse HEAD` → `7fc6aa2f…` (L1 clone consistent).
- `git -C ~/Projects/ds4cc-marketplace rev-parse HEAD` → `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` (read-only; no fetch).

## Cell-by-cell verdict

| cell | verdict | evidence |
|---|---|---|
| id `S065` | correct | unique row, `grep -c` = 1; under `## Registry` (SOURCES.md:5, row :73) |
| source | correct | upstream HEAD = the named full hash; URL `…/commit/7fc6aa2f…` resolves to HEAD. Exactly three `index.html` under `magga/frostbite/` exist in the commit (`index.html`, `classic/index.html`, `remastered/index.html`). "local clone … one commit behind, at 1fbdb8ed" holds now: 1fbdb8ed is `7fc6aa2f`'s parent (`git log` shows `7fc6aa2f 1fbdb8ed`); its state at author time is [INFERENCE]-consistent only. Retained set byte-identical: `git hash-object` of all 4 files under `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/` equals the upstream blob ids exactly (see below). |
| kind `code` | correct | same convention as S062 (same repo) and repo-file rows |
| tier `A` | correct | convention-consistent with S062 tier A for operator's own pinned bytes; tier is per-row judgment, not falsifiable beyond convention |
| scope | correct | wording limits claim to file content at one commit, explicitly disclaims live serving and deployment — honest scope, no overreach |
| anchor | all literals correct | `git show -s`: author+committer `2026-10-21T17:32:55Z`, subject `"magga: Frostbite — Classic & Remastered at /magga/frostbite/"` exact. `git ls-tree 7fc6aa2f`: sitemap.xml `67d8c7a50dc3a3734ce4be97ffa4810e1e257e12`, frostbite/index.html `e0d9ee29d9f1bf21faa0238e3253d4e9199304de`, classic `12c58e2dae534f6569015fa3c0ec8cde502c5119`, remastered `4e6d70ae05272e089f4564b1ed6f3c9b21a440a2` — all four match the anchor. `grep -n frostbite` on `7fc6aa2f:sitemap.xml` → lines 15,16,17; `git diff 1fbdb8ed 7fc6aa2f -- sitemap.xml` hunk `@@ -12,6 +12,9 @@` adds exactly those three locs. Canonical quote `<link rel="canonical" href="https://ds4cc.com/magga/frostbite/">` at line 9 of index.html; classic and remastered canonicals at line 12 each — line numbers and bytes verified. |
| teaches | correct | `grep -c '<loc>'`: 100 at `7fc6aa2f`, 97 at `1fbdb8ed` ("100 locs (97 at 1fbdb8ed)" exact); three added under `/magga/frostbite/`; each page's canonical string equals its sitemap loc byte-for-byte |
| status `mined` | correct | registry convention; C2 counter expects `mined` |
| opened `2026-10-22` | correct | calendar-consistent; matches S060–S066 opened dates |
| recheck `90d` | correct | identical to every S060–S066 sibling row |
| used-by | correct as stated; see residual | `corpus/knowledge/sitemap-orphan-audit.md` section `## Round-33 ds4cc source pin 7fc6aa2f` cites `(S065)` at :191 and "blob ids in S065" at :199 |

## Residual (minor, not a falsification)

`corpus/lessons/round-33.md` cites S065 five times — including Gate row :31 which
admits it as "tier A for the files' own content at that commit, status `mined`" —
and `corpus/README.md:307` names it; neither appears in used-by. Convention is
inconsistent: S002 lists `corpus/lessons/round-27.md`, yet S062's used-by omits
`corpus/lessons/round-32.md` despite nine citations. The row's stated used-by
entry is true; the cell may be incomplete depending on which convention governs
lesson admissions. The C2 counter's c2 requirement (used-by names the audit file)
is satisfied exactly.

## Not verified / limitations

- `~/Projects/ds4cc-marketplace` at-author-time state (verified only at review time, now).
- Live ds4cc.com serving: out of scope per bounds; the row correctly disclaims it.
- Tier/kind/status are convention judgments — verified against sibling-row convention, not against an external spec.

No tool installs performed. Sandbox: `/fast/scratch/hyaku/kake-r33/w2/ReviewS065RowTruth/` (clone/, upstream/, tmp/).
Report: .ufo/waves/round-33/w2/ReviewS065RowTruth.md
