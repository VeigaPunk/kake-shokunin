# Round 33 C2 hollow-commit probe

Axes: freshness (scored); C2 counter sensitivity to hollow provenance (diagnostic).

**Finding: yes.** A commit can score 4/4 while C1 is genuinely byte-exact but the claimed source registry row and source-analysis prose are fabricated. The counter verifies C4's copied numbers against retained bytes; it does not establish that the row or narrative came from source study.

## Detector results

`c1/c2/c3/c4` are the emitted condition booleans; all detector exits below were 0.

| Construction (commit) | Conditions; met | Hollow? / observation |
|---|---|---|
| Pristine base `bc6c4a8d435473f3c30903210be30d9d6e3ef750` | F/F/F/F; 0 | No; expected baseline. |
| Exact upstream files only `6078f65289c3b972aeb2b00b2f74970cf395e1f2` | T/F/F/F; 1 | No; c1 found all four exact pinned blobs; no row or section. |
| Fake row, section has only S065+hash `27d45c55d2ee45458891487b7fe755196bf16ff6` | T/T/T/F; 3 | Yes; c2 accepted 11 junk cells; c4 rejected missing stated metrics. Output: `rowsFound=1`, `rowCells=11`, `headingCount=1`, `sitemapLocs=100`, canonical observed `clean` x3, stated values empty. |
| Fabricated row plus copied exact metrics `d1bb9b0c643b19fc00b19abac196f77373727eb4` | T/T/T/T; **4** | **Yes—full-score hollow case.** Source cell says “fabricated placeholder”; other unchecked cells are `nonsense`, `junk`, `none`, `no anchor`, `no source content`, `n/a`. Section contains only S065/hash, `sitemap-locs: 100`, and three copied `clean` verdicts. Counter output: one 11-cell row, one heading, 100 locs, all three observed/stated verdicts `clean`, `met=4`. Candidate evidence: `corpus/SOURCES.md:73`, `corpus/knowledge/sitemap-orphan-audit.md:184-191` at this revision. |
| Same junk row; pin section moved before the unrelated coverage matrix `528717b29461fc4db2ce9ea2464a2af947481d97` | T/T/T/T; **4** | **Yes.** The exact heading at `corpus/knowledge/sitemap-orphan-audit.md:12` is accepted despite its misplaced context; same 100/clean facts. |
| Duplicate exact heading `f0dc05706d74375af3c7be296a905597f3e8b67b` | T/T/F/F; 2 | No full hollow score; detector correctly reports `headingCount=2` and rejects c3/c4. |
| Two backslashes before a pipe in the junk row `8fc8ecb2be00815d2e92894f195a506b2b864eb0` | T/T/T/T; **4** | **Yes.** `corpus/SOURCES.md:73` has `nonsense \\| junk`: the pipe is a Markdown delimiter after an even backslash run, but `re.split(r"(?<!\\)\\|", ...)` treats it as escaped. The malformed 12-column row is counted as 11 cells and passes c2. |
| Restored pristine base `bc6c4a8d435473f3c30903210be30d9d6e3ef750` | F/F/F/F; 0 | Same output after restore; exit 0. |

The source bytes were not forged: upstream `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` `git ls-tree -r` reported mode `100644` and the exact four blob IDs pinned in `c2_pin_count.py:44-48`; those blobs were archived into the scratch clone. Thus this falsifies provenance/row/placement coverage, not the byte-level C1 condition.

## What remains hollow and what to catch

- **Junk S065 row (c2):** checks only 11 parsed cells plus hash substring, status, date and used-by. Validate the source identity and material registry fields (source/revision, kind/tier/scope, anchor, taught fact, recheck) against the claimed pin; field presence alone cannot prove truth, so source admission still needs explicit evidence/review.
- **Copied metrics (c3/c4):** c4 correctly re-derives the sitemap and canonical results, but exact copied results are indistinguishable from independently read results. If `met=4` is intended to certify source analysis, add a separate source-specific evidence criterion; do not treat these numeric checks as proof of research.
- **Misplaced section (c3):** `section()` scans the entire entry and requires only one exact heading. Pin an allowed location/context or required neighboring anchor.
- **Escaped-pipe row (c2):** count delimiter pipes by backslash parity (even run means delimiter) and validate row cardinality against the registry header with a proper table parser.
- **Duplicate heading:** already caught. Missing metrics are also caught (3/4 case). C1's exact blob check is appropriately strict.

## Commands and restoration evidence

Clone setup command exited 0: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; mkdir -p /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/tmp && export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/tmp && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone && git -C /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone checkout -q bc6c4a8d435473f3c30903210be30d9d6e3ef750`.
Source staging command exited 0: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/tmp; mkdir -p /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone/.ufo/waves/round-33/sources/ds4cc-7fc6aa2f && git -C /fast/scratch/hyaku/kake-r33/ds4cc-upstream archive --format=tar 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 sitemap.xml magga/frostbite/index.html magga/frostbite/classic/index.html magga/frostbite/remastered/index.html | tar -xf - -C /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone/.ufo/waves/round-33/sources/ds4cc-7fc6aa2f && git -C /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone add .ufo/waves/round-33/sources/ds4cc-7fc6aa2f && git -C /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone -c user.name=MutationTester -c user.email=mutation-test.invalid commit -m 'scratch: exact pinned upstream bytes' && git -C /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone rev-parse HEAD`.
Each scratch commit below exited 0. Exact staged paths/message; resulting HEAD:
| Paths | `git commit -m` title | HEAD |
|---|---|---|
| `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f` | `scratch: exact pinned upstream bytes` | `6078f65289c3b972aeb2b00b2f74970cf395e1f2` |
| `corpus/SOURCES.md corpus/knowledge/sitemap-orphan-audit.md` | `scratch: hollow source row without facts` | `27d45c55d2ee45458891487b7fe755196bf16ff6` |
| `corpus/knowledge/sitemap-orphan-audit.md` | `scratch: copied metrics with fabricated source row` | `d1bb9b0c643b19fc00b19abac196f77373727eb4` |
| `corpus/SOURCES.md corpus/knowledge/sitemap-orphan-audit.md` | `scratch: place source pin section before coverage matrix` | `528717b29461fc4db2ce9ea2464a2af947481d97` |
| `corpus/SOURCES.md corpus/knowledge/sitemap-orphan-audit.md` | `scratch: duplicated source pin heading` | `f0dc05706d74375af3c7be296a905597f3e8b67b` |
| `corpus/SOURCES.md corpus/knowledge/sitemap-orphan-audit.md` | `scratch: escaped-pipe row cardinality probe` | `8fc8ecb2be00815d2e92894f195a506b2b864eb0` |
Detector command for each revision, with the listed `--rev` value, exited 0: `export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/tmp; python3 -B /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone/.ufo/waves/round-33/c2_pin_count.py --repo /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone --rev <revision>`. Ran on pristine, all six scratch commits, then pristine after restoration. No build, lint, or other tests run; no tools installed.
The candidate commit command form was `git -C /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone add PATHS && git -C /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone -c user.name=MutationTester -c user.email=mutation-test.invalid commit -m TITLE && git -C /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone rev-parse HEAD`; each table row supplies the exact `PATHS` and `TITLE`; each exited 0.
Exact detector shell form: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/tmp; python3 -B /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone/.ufo/waves/round-33/c2_pin_count.py --repo /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone --rev REV; printf 'exit=%s\n' "$?"`. `REV` was each of the commits in the results table, including pristine before and after; all exits 0.

Restored with `git -C /fast/scratch/hyaku/kake-r33/w1/MutC2HollowCommit/clone switch --detach bc6c4a8d435473f3c30903210be30d9d6e3ef750` (exit 0). Final `git status --short --branch`: `## HEAD (no branch)`. Before/after SHA-256 values match exactly: counter `97a481294e9f0cd76f6a7608536b5bbeab8dbfc6191ea9437afe7005d5629ea8`; `corpus/SOURCES.md` `51ee196dc055a0a4edf0ca709f46a5408733c1ec6c9cf562a095f38bfb05b1d3`; `corpus/knowledge/sitemap-orphan-audit.md` `cab9dbe38b13336c0638c4181886baa9777c2a01e800fd2d7a0dea7c7d52d763`.