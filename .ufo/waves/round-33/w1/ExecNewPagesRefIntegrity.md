# Round 33 — Frostbite reference integrity

**Scope:** Parsed the three new pages from ds4cc-marketplace commit `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` with Python `html.parser`. For each non-empty relative or same-host `ds4cc.com` `href`/`src`, resolved against the page's canonical URL and tested the resulting path against `git ls-tree -r --name-only` at that commit; directory URLs map to `index.html`.

| Page | Line | Attribute | Value | Resolved URL | Git target | Exists |
|---|---:|---|---|---|---|---|
| `magga/frostbite/index.html` | 9 | `link.href` | `https://ds4cc.com/magga/frostbite/` | `https://ds4cc.com/magga/frostbite/` | `magga/frostbite/index.html` | yes |
| `magga/frostbite/index.html` | 180 | `a.href` | `../` | `https://ds4cc.com/magga/` | `magga/index.html` | yes |
| `magga/frostbite/index.html` | 185 | `a.href` | `../` | `https://ds4cc.com/magga/` | `magga/index.html` | yes |
| `magga/frostbite/index.html` | 207 | `a.href` | `./classic/` | `https://ds4cc.com/magga/frostbite/classic/` | `magga/frostbite/classic/index.html` | yes |
| `magga/frostbite/index.html` | 208 | `img.src` | `./covers/classic.png` | `https://ds4cc.com/magga/frostbite/covers/classic.png` | `magga/frostbite/covers/classic.png` | yes |
| `magga/frostbite/index.html` | 216 | `a.href` | `./classic/` | `https://ds4cc.com/magga/frostbite/classic/` | `magga/frostbite/classic/index.html` | yes |
| `magga/frostbite/index.html` | 220 | `a.href` | `./remastered/` | `https://ds4cc.com/magga/frostbite/remastered/` | `magga/frostbite/remastered/index.html` | yes |
| `magga/frostbite/index.html` | 221 | `img.src` | `./covers/remastered.jpg` | `https://ds4cc.com/magga/frostbite/covers/remastered.jpg` | `magga/frostbite/covers/remastered.jpg` | yes |
| `magga/frostbite/index.html` | 229 | `a.href` | `./remastered/` | `https://ds4cc.com/magga/frostbite/remastered/` | `magga/frostbite/remastered/index.html` | yes |
| `magga/frostbite/index.html` | 259 | `a.href` | `../` | `https://ds4cc.com/magga/` | `magga/index.html` | yes |
| `magga/frostbite/classic/index.html` | 12 | `link.href` | `https://ds4cc.com/magga/frostbite/classic/` | `https://ds4cc.com/magga/frostbite/classic/` | `magga/frostbite/classic/index.html` | yes |
| `magga/frostbite/classic/index.html` | 134 | `a.href` | `../` | `https://ds4cc.com/magga/frostbite/` | `magga/frostbite/index.html` | yes |
| `magga/frostbite/classic/index.html` | 154 | `script.src` | `../core.js` | `https://ds4cc.com/magga/frostbite/core.js` | `magga/frostbite/core.js` | yes |
| `magga/frostbite/classic/index.html` | 155 | `script.src` | `../shell.js` | `https://ds4cc.com/magga/frostbite/shell.js` | `magga/frostbite/shell.js` | yes |
| `magga/frostbite/classic/index.html` | 156 | `script.src` | `classic.js` | `https://ds4cc.com/magga/frostbite/classic/classic.js` | `magga/frostbite/classic/classic.js` | yes |
| `magga/frostbite/remastered/index.html` | 12 | `link.href` | `https://ds4cc.com/magga/frostbite/remastered/` | `https://ds4cc.com/magga/frostbite/remastered/` | `magga/frostbite/remastered/index.html` | yes |
| `magga/frostbite/remastered/index.html` | 200 | `a.href` | `../` | `https://ds4cc.com/magga/frostbite/` | `magga/frostbite/index.html` | yes |
| `magga/frostbite/remastered/index.html` | 232 | `a.href` | `../classic/` | `https://ds4cc.com/magga/frostbite/classic/` | `magga/frostbite/classic/index.html` | yes |
| `magga/frostbite/remastered/index.html` | 273 | `script.src` | `../core.js` | `https://ds4cc.com/magga/frostbite/core.js` | `magga/frostbite/core.js` | yes |
| `magga/frostbite/remastered/index.html` | 274 | `script.src` | `../shell.js` | `https://ds4cc.com/magga/frostbite/shell.js` | `magga/frostbite/shell.js` | yes |
| `magga/frostbite/remastered/index.html` | 275 | `script.src` | `remastered.js` | `https://ds4cc.com/magga/frostbite/remastered/remastered.js` | `magga/frostbite/remastered/remastered.js` | yes |

**Result:** 21 qualifying `href`/`src` references; 0 missing target files. All three pages carry the canonical URLs shown above. The target directory tree also contains the expected scripts and cover images.

**Base-path audit:** `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/base_path_audit.py --help` exited 0 (`usage: base_path_audit.py --manifest PATH`; manifest requires `basePath` starting/ending `/`). Base path `/` fits these root-served canonical URLs. `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/base_path_audit.py --manifest /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/manifest.json` exited 0 and printed exactly `{"findings":[],"pagesChecked":3,"referencesChecked":24,"verdict":"clean"}`. The audit checks additional attribute kinds (including `srcset`/poster), so its count is not the `href`/`src` table count.

**Commands and retained evidence:**
- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; mkdir -p /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/tmp && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/clone && git -C /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/clone checkout -q bc6c4a8d435473f3c30903210be30d9d6e3ef750 && printf 'clone_exit=0 revision=' && git -C /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/clone rev-parse HEAD` — exit 0; printed `clone_exit=0 revision=bc6c4a8d435473f3c30903210be30d9d6e3ef750`.
- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/tmp; git clone -q https://github.com/VeigaPunk/ds4cc-marketplace.git /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/upstream && git -C /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/upstream checkout -q 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 && printf 'clone_exit=0 revision=' && git -C /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/upstream rev-parse HEAD && printf '\nnew_frostbite_paths:\n' && git -C /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/upstream ls-tree -r --name-only 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 -- magga/frostbite` — exit 0; printed the requested revision and these paths: `classic/classic.js`, `classic/index.html`, `core.js`, `covers/classic.png`, `covers/remastered.jpg`, `index.html`, `remastered/index.html`, `remastered/remastered.js`, `shell.js` (under `magga/frostbite/`).
- `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/base_path_audit.py --help` — exit 0; output began `usage: base_path_audit.py --manifest PATH` and described the required `version:1` manifest with `basePath` starting/ending `/`.
  Complete help stdout:
  ```
  usage: base_path_audit.py --manifest PATH

  --help prints standard CLI help, exits 0, and emits no verdict.

  Read UTF-8 JSON manifest v1 and bounded local UTF-8 HTML only.
  The manifest is {version:1, basePath:'/…/', pages:[{file, url}]}.
  basePath starts and ends with '/'; page files are relative to the
  manifest directory; absolute paths, traversal, symlinks, and
  non-regular files are rejected. The manifest limit is 1 MiB; each
  HTML file is limited to 2 MiB. No network access or writes occur.

  Checked references: a/area/link[href], img/script/iframe/source/
  audio/video/track/embed[src], img/source[srcset], video[poster],
  form[action]. The first base element with href sets the document
  base; the base element itself is not a reference. Values that are
  empty after stripping ASCII whitespace, use a non-HTTP(S) scheme, or
  point at another site are ignored. Same site means the same host
  (case-insensitive) and the same port after default ports are folded;
  http and https on one host count as the same site, so a cross-scheme
  reference is still checked against the base path.

  Except --help, stdout is always one JSON object: verdict,
  pagesChecked, referencesChecked, findings. Each finding carries id,
  reason, page, element, attribute, value, resolved.
  Exit: 0 clean; 1 failed-policy; 2 could-not-evaluate; 64 usage.

  options:
    -h, --help       show this help message and exit
    --manifest PATH
  ```
- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/tmp; python3 -B /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/analyze_refs.py` — exit 0; output table above, ending `SUMMARY references=21 missing=0`. The script invokes `git -C /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/upstream ls-tree -r --name-only 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`.
- `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/base_path_audit.py --manifest /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/manifest.json` — exit 0; exact JSON output: `{"findings":[],"pagesChecked":3,"referencesChecked":24,"verdict":"clean"}`.
- `sha256sum /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/upstream/magga/frostbite/index.html /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/upstream/magga/frostbite/classic/index.html /fast/scratch/hyaku/kake-r33/w1/ExecNewPagesRefIntegrity/upstream/magga/frostbite/remastered/index.html` — exit 0; hashes in that order: `b7f5380afe0744849af76f8b82ef253d8ef80a696869be15d844268ca1c0d94f`, `96838f42bfba1f5b1fa1594e570bdcd9ec052c148cff45aa7dbf1dbe0d3e6f94`, `0ebfd489c938f6e88a61bb85776e44222010e2d8854bd954f5b86cb3629b3aea`.

**Risks / blockers:** Static HTML attributes only; no live HTTP, runtime-generated URLs, or CSS `url()` references were checked. No blockers. No tools installed or updated; no build, test, lint, or formatter was run.
