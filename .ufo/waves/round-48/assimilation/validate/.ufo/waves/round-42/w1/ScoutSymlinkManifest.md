# ScoutSymlinkManifest — defect 6 recon

Axes: operability (confinement that keeps the current CLI) and freshness (round-39 contract versus tip41). Planning only. No install.

## Reproduction

tip41 and `scripts/sitemap_audit.py` match: sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`.

`timeout 60 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w1/ScoutSymlinkManifest/repro.py` → exit 0. Outside bytes were `<alien>outside-bytes</alien>`. Stderr empty on every case.

| case | `file` | exit | result |
|---|---|---|---|
| 01 absolute symlink target | `link.xml` | 1 | `root_invalid` (parsed the outside file) |
| 02 symlink target `../outside/alien.xml` | `link.xml` | 1 | `root_invalid` |
| 03 `alias` → outside directory | `alias/alien.xml` | 1 | `root_invalid` |
| 04 symlink to sibling `a.xml` | `link.xml` | 0 | clean |
| 05 absolute file value | outside path | 2 | `check_invalid` |
| 06 `..` file value | `../outside/alien.xml` | 2 | `check_invalid` |
| 07 missing / 08 directory / 09 dangling inside | | 2 | `file_unreadable` |
| 10 dangling symlink to a missing outside path | `gone.xml` | 2 | `file_unreadable` |
| 11 manifest directory is a symlink | `a.xml` | 0 | clean |
| 12 manifest file symlink, same directory | `a.xml` | 0 | clean |
| 13 chain leaves, then returns to inside `a.xml` | `link.xml` | 0 | clean |

`os.path.realpath` collapsed missing `no-such-sub/../outside/alien.xml` onto `outside/alien.xml`. Dangling-outside realpath is that outside path. Hop-back realpath is inside `a.xml`.

Follow-up: `timeout 20 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42/shared/tip41.py --manifest /fast/scratch/hyaku/kake-r42w1/ScoutSymlinkManifest/tree/14-manifest-target/a/manifest.json` → exit 0, clean. `a/manifest.json` points at `b/manifest.json`; `a/a.xml` is a sitemap and `b/a.xml` is `<alien>`. Resolution used the link's directory.

## Contract (quoted)

`.ufo/waves/round-39/c1-contract.md:7`: "behaviour on inputs these sentences do not cover is outside the contract."

`:22-24` sentence 4: a check with a `file` "that is absolute or has a `..` path segment" is `check_invalid`.

`:26-27` sentence 5: "`file` is resolved against the manifest's directory. A file that cannot be read is an error check with error `file_unreadable`."

No sentence mentions symlinks.

## Why it reads

`_file_value_invalid` (`scripts/sitemap_audit.py:357-360`) rejects only a leading `/` or a `..` segment. `_evaluate_check:386` joins that onto `dirname(abspath(manifest))` (`:430`). `_audit_file:210` `open`s the join, and `open` follows symlinks.

## Fix outline (not this round)

Keep the lexical gate. Then compare `realpath(join(base_dir, file))` to `realpath(base_dir)` (both real, so case 11 stays). If the resolved path is outside, return `check_invalid` and do not open — same family as absolute/`..`, and the same choice as `robots_audit.py` f23. Open that resolved path, not the joined path. An inside `OSError` stays `file_unreadable`.

That stops 01–03. It does not stop 13 (final path is inside). It would reclassify 10 from `file_unreadable` to `check_invalid`; nothing pins 10. Do not drop the lexical `..` check (`realpath` would turn selftest `chk_dotdot_file` `:212` clean), do not map an inside directory to `check_invalid` (`file_is_directory` `:236`), do not take `base_dir` from `dirname(realpath(manifest))` (case 14 would read the target directory), and do not `O_NOFOLLOW` every component (that also rejects inside case 04). Line 7 means the refusal needs a new numbered sentence first; the error code is not specified today.

## Fixtures

A fix with those limits touches no committed fixture. `sitemap_audit_selftest.py` has no symlink. Keep: `chk_absolute_file` `:208`, `chk_dotdot_file` `:212`, `file_unreadable` `:233`, `file_is_directory` `:236`, `file_relative_to_manifest_dir` `:239`, `out_error_item_shape` `:759`, `out_mixed_error_wins` `:762`, `out_all_statuses` `:779`. Round-41 realrun `manifest.json` and the six `sitemaps/*.xml` are regular files. `c42_count.py` symlinks are bwrap `/lib` aliases, not case files. An outside-symlink fixture and an inside-symlink fixture do not exist yet.

## Statements

- Outside symlink `file` values are read by tip41 — holds (01–03: exit 1, `root_invalid`). Stdout is findings, not the file text.
- Absolute and `..` file values are `check_invalid` — holds (05, 06).
- The round-39 contract already forbids this read — overstated (`:7`, `:22-27`).
- A containment fix must rewrite existing fixture expectations — wrong, if the lexical gates and inside `file_unreadable` stay.
