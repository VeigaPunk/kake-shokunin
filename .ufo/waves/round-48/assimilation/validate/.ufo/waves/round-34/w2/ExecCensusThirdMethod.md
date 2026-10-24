# Round 34 third-method ds4cc census

Axis: freshness, through an independent HTML parsing method.

## Result

Recounted the pinned retained archive with `html5lib` 1.1 using its HTML5 `etree` tree builder (neither the C2 `html.parser` implementation nor wave-1 `lxml`). The seven values match the census line in the entry at revision `24a16474ee73e20453f3e1be9d2f33573c5196d9`:

| Census field | Entry | html5lib |
|---|---:|---:|
| pages | 102 | 102 |
| og:title | 87 | 87 |
| og:type | 87 | 87 |
| og:image | 1 | 1 |
| og:url | 87 | 87 |
| all-four | 1 | 1 |
| og-url-equals-canonical | 87 | 87 |

The script validates the archive PAX commit, all 102 archive/tree paths, and each page's Git blob SHA-1 before counting. Its additional page-by-page differential against the C2 `HTMLParser` semantics is `per_page_parser_differences: []`; there is no differing page to report. This is a source-byte census, not a live-site or rendered-preview check.

## Reproduction and observed commands

- Initial availability probe, exit 1: `python3 -c 'import sys; print(sys.version.split()[0]); import html5lib; print("html5lib", html5lib.__version__)'`. Output: Python `3.14.8`, then `ModuleNotFoundError: No module named 'html5lib'`.
- Installed into this task's isolated sandbox venv (no host/global install): `work=/fast/scratch/hyaku/kake-r34/w2/ExecCensusThirdMethod; export TMPDIR="$work/tmp"; uv venv --python python3.14 "$work/venv" && uv pip install --python "$work/venv/bin/python" html5lib && "$work/venv/bin/python" -c 'import html5lib; print("html5lib=" + html5lib.__version__)'` — exit 0; `html5lib=1.1`. Installed packages: html5lib 1.1, six 1.17.0, webencodings 0.6.1 (transitive). Channel: `uv pip` from the configured Python package index (PyPI); reason: required third parser. uv reported hardlink fallback to copy; installation succeeded.
- Archive extraction: `work=/fast/scratch/hyaku/kake-r34/w2/ExecCensusThirdMethod; mkdir -p "$work/tmp" "$work/html"; export TMPDIR="$work/tmp"; unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 24a16474ee73e20453f3e1be9d2f33573c5196d9:.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz > "$work/html.tar.xz"; git_status=$?; printf 'git_show_exit=%s\n' "$git_status"; sha256sum "$work/html.tar.xz"; xz -dc "$work/html.tar.xz" | tar -xf - -C "$work/html"; extract_status=$?; printf 'extract_exit=%s\n' "$extract_status"; find "$work/html" -type f | wc -l; exit "$extract_status"` — `git_show_exit=0`, archive SHA-256 `818f06443470f6dcb4118cbb1ada15fd7880faeba40ac85e4418e0455d2fe7a3`, `extract_exit=0`, 102 files.
- Pinned tree and entry retrieval: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 24a16474ee73e20453f3e1be9d2f33573c5196d9:.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/tree.txt > "$work/tree.txt"` and `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 24a16474ee73e20453f3e1be9d2f33573c5196d9:corpus/knowledge/link-preview-metadata.md > "$work/entry.md"` — both exit 0. Tree SHA-256 `2d5d047ff6db6c697a587b965d31847bf6de3f9bdcf3bf45ffb0c32f5f573516`; entry SHA-256 `999175a2cc800381c67ab5df0103827e592d417fa3403459375cef6381f5d1f7`.
- Recount: `work=/fast/scratch/hyaku/kake-r34/w2/ExecCensusThirdMethod; export TMPDIR="$work/tmp"; "$work/venv/bin/python" "$work/recount.py" > "$work/recount.json"; status=$?; printf 'recount_exit=%s\n' "$status"; cat "$work/recount.json"; sha256sum "$work/recount.py" "$work/recount.json"; exit "$status"` — exit 0; output reports `archive_pages=102`, the seven matching values above, `counts_match_entry=true`, and `per_page_parser_differences=[]`.

## Evidence and scope

- Entry census: `corpus/knowledge/link-preview-metadata.md:120-132`, especially line 128; pinned entry SHA-256 above. C2 tip receipt: `.ufo/waves/round-34/verification/c2-at-24a1647.json:54-75`, SHA-256 `7b737bf42c5b77e368501ccc521569d3082ebbb7c069d939c380187e6ea12b23`.
- Retained archive and tree: `.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz` SHA-256 `818f06443470f6dcb4118cbb1ada15fd7880faeba40ac85e4418e0455d2fe7a3`; `tree.txt:1-103` SHA-256 `2d5d047ff6db6c697a587b965d31847bf6de3f9bdcf3bf45ffb0c32f5f573516`.
- Recount implementation and full machine output (including empty per-page difference list): `/fast/scratch/hyaku/kake-r34/w2/ExecCensusThirdMethod/recount.py` SHA-256 `807ddc6a8ec2277ae5a4d834155eea4c6671bd94e843242586fc4fd5a4de67b2`; `/fast/scratch/hyaku/kake-r34/w2/ExecCensusThirdMethod/recount.json` SHA-256 `958c15defdf240d2fd6a01c501584c3ca6be18c679bf9fddf01e42c93c42b3dc`.
- No network requests or other checks were run.
