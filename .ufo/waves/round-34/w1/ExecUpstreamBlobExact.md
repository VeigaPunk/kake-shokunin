# Retained ds4cc upstream-byte check

Axis: freshness. Result: retained HTML tar bytes match the specified upstream commit, and that commit was still the public default-branch head at the final lookup.

## Upstream head

- `git clone -q https://github.com/VeigaPunk/ds4cc-marketplace.git /fast/scratch/hyaku/kake-r34/w1/ExecUpstreamBlobExact/clone` — exit 0 (fresh sandbox clone).
- `git ls-remote --symref https://github.com/VeigaPunk/ds4cc-marketplace.git HEAD` — exit 0; `ref: refs/heads/main`, `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 HEAD`.
- Final repeat of the same `git ls-remote` after comparisons — exit 0; same `main` and `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`.
- `git -C /fast/scratch/hyaku/kake-r34/w1/ExecUpstreamBlobExact/clone show -s --format='commit=%H%ncommit_time=%cI%nsubject=%s' HEAD` — exit 0; commit `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`, commit time `2026-10-21T17:32:55Z`, subject `magga: Frostbite — Classic & Remastered at /magga/frostbite/`.

## Tree and retained bytes

Superseded bad-input attempt (disclosed): `git -C /fast/scratch/hyaku/kake-r34/w1/ExecUpstreamBlobExact/clone ls-tree -r --full-tree --name-only 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 -- '*.html' | wc -l` — exit 0, output `0`; this pathspec selected no HTML files. `git -C /fast/scratch/hyaku/kake-r34/w1/ExecUpstreamBlobExact/clone ls-tree -r --full-tree 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 -- '*.html' | diff -u -I '^commit ' /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/tree.txt -` — exit 2 (`diff` rejected unsupported `-I`). Using the empty path list, `git -C "$work/clone" archive --format=tar 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 "${html_paths[@]}" > "$work/upstream-html.tar"` archived the whole repository (exit 0); `xz -dc "$retained" > "$work/retained-html.tar"` exited 0; `cmp -s "$work/upstream-html.tar" "$work/retained-html.tar"` exited 1 (`DIFFERENT`). Discarded; not evidence against the retained HTML-only archive.
The corrected commands below used `work=/fast/scratch/hyaku/kake-r34/w1/ExecUpstreamBlobExact`, `retained=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz`, and `rev=7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`.

- Correct tree comparison (`rev=7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`, `tree=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/tree.txt`): `git -C /fast/scratch/hyaku/kake-r34/w1/ExecUpstreamBlobExact/clone ls-tree -r --full-tree "$rev" | while IFS= read -r entry; do path=${entry#*$'\\t'}; [[ "$path" == *.html ]] && printf '%s\\n' "$entry"; done | cmp -s - <(while IFS= read -r entry; do [[ "$entry" == commit\\ * ]] || printf '%s\\n' "$entry"; done < "$tree")` — exit 0, `MATCH`.
- Correct count command: `git -C /fast/scratch/hyaku/kake-r34/w1/ExecUpstreamBlobExact/clone ls-tree -r --full-tree --name-only "$rev" | while IFS= read -r path; do [[ "$path" == *.html ]] && printf '%s\\n' "$path"; done | wc -l` — exit 0, `102`.
- Path-list generation with that same full-tree command and `.html` suffix filter to `"$work/html-paths.txt"` — exit 0; `mapfile -t html_paths < "$work/html-paths.txt"` gave `HTML_PATH_COUNT=102`.
- `git -C "$work/clone" archive --format=tar "$rev" "${html_paths[@]}" > "$work/upstream-html.tar"` — exit 0.
- `xz -dc "$retained" > "$work/retained-html.tar"` — exit 0.
- `cmp -s "$work/upstream-html.tar" "$work/retained-html.tar"` — exit 0, `IDENTICAL`.
- `sha256sum "$work/upstream-html.tar" "$work/retained-html.tar"` — exit 0; both `71c8c34e7f3489851d7ba81507b39846cecbcfce5a65b764d8ca054769c8dd0c`. `wc -c "$work/upstream-html.tar" "$work/retained-html.tar"` — exit 0; each `13,537,280` bytes.
- PAX command: `python3 -c 'import sys,tarfile; expected="7fc6aa2fc12451dd451fed5a9ee7125f3a90e884"; ok=True` (looped over both files with `tarfile.open`, read `t.pax_headers["comment"]`, counted `.html` members, required the expected comment and 102 members) `"$work/upstream-html.tar" "$work/retained-html.tar"` — exit 0; both comments were `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`, both counts `102`.

## Evidence and scope

- Retained listing: `.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/tree.txt:1-103`; line 1 names the commit, remaining 102 entries match the upstream filtered tree. SHA-256 `2d5d047ff6db6c697a587b965d31847bf6de3f9bdcf3bf45ffb0c32f5f573516`.
- Retained archive: `.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz`; SHA-256 `818f06443470f6dcb4118cbb1ada15fd7880faeba40ac85e4418e0455d2fe7a3`.
- Rebuilt and decompressed tars are in `/fast/scratch/hyaku/kake-r34/w1/ExecUpstreamBlobExact/` as `upstream-html.tar` and `retained-html.tar`.
- No tools installed. No builds/tests were run; this assignment was an artifact-provenance comparison.
