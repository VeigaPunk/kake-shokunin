# Kake R35 w2 — ReviewS074Note

Attacks the appended S074 correction note at the end of corpus/SOURCES.md (corpus/SOURCES.md:174, "Round-35 correction note for S074 (routed defect 5 of the round-34 closure)"). Axis: freshness. Result: every count and structural claim in the note reproduces from the retained bytes, no S074 cell changed between 16a6b8b8 and 7deacc4629c1d05a34fb919d8095e99efc7b712f, and the note's shape matches the neighboring notes — with one low-severity labeling defect: the note attributes the decompressed body's sha256 and byte size to the `.html.gz` file itself.

## Sandbox

`/fast/scratch/hyaku/kake-r35/w2/KakeR35.ReviewS074Note/` (`clone/` cloned from the lane at 7deacc4629c1d05a34fb919d8095e99efc7b712f, HEAD verified; `tmp/` is TMPDIR). GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset for every git call. No lane file written except this report. No live requests. No tools installed (none needed); no pacman run.

## Commands run (lane files read in place; hashes/counts computed on sandbox copies)

1. `stat -c '%n %s' .ufo/waves/round-34/sources/S074.html.gz S074.txt` → exit 0; `S074.html.gz 114568`, `S074.txt 494103` bytes.
2. `sha256sum` on both → exit 0; gz `4862290952cff8c1…70533aab4`; txt `9be76fdab951f0aa007fcf6c17fcebc68c70cc171f40745e701286fa046a9554`.
3. `wc -w .ufo/waves/round-34/sources/S074.txt` → exit 0; `73876`. Note claims 73,876 — reproduced.
4. `grep -o 'og:' S074.txt | wc -l` → `0`, exit 0. Note claims → 0 — reproduced.
5. `gunzip -c S074.html.gz > tmp/S074.html`; `wc -c` → exit 0; `860230`. `gzip -l S074.html.gz` → exit 0; compressed 114568, uncompressed 860230. `sha256sum tmp/S074.html` → exit 0; `099bc4f9d7a44da589a089a8954515e3c615d4be2f3fe85b9766f1d9c9a90bbc`.
6. `grep -o 'og:' tmp/S074.html | wc -l` → exit 0; `3`. `grep -n -o 'og:[A-Za-z_-]*' tmp/S074.html` → exit 0; exactly `9:og:title`, `10:og:image`, `11:og:description`. `grep -n '<head\|</head>'` → exit 0; head spans lines 3–25, so all three og: metas are inside `<head>`. Each line is a `<meta property="og:…">`: og:title content="Telegram Bot API", og:image content="30f729d4f304e41659", og:description (tmp/S074.html:9-11). Note's "exactly three og: metas, all inside its `<head>`" and og:title value — reproduced.
7. `git -C clone diff --stat 16a6b8b8 7deacc4629… -- corpus/SOURCES.md` → exit 0; 15 insertions(+), 1 deletion(-). The deletion is the S006 row (used-by cell gained `corpus/knowledge/security-txt-publishing.md` — the declared S006 re-open, not an S074 cell); insertions are S078–S087 rows, the S074 note, and the Round-35 bounded-question paragraph (clone diff saved at `tmp/sources.diff`).
8. S074-cell check: `grep -cE '^[+-]\| S074 '` on that diff → 0 changed rows. `git show 16a6b8b8:corpus/SOURCES.md | grep -F '| S074 |'` vs the same grep on HEAD → `cmp` byte-identical (`ROW_IDENTICAL`). So no S074 cell changed between the two revisions; note's "Status, recheck and used-by cells of S074 are unchanged (`rejected`, `90d`, `—`)" matches the row at corpus/SOURCES.md:82.
9. Receipt cross-check: `.ufo/waves/round-34/sources/receipts.json:86-95` — S074 `bodySha256 099bc4f9…`, `bodyBytes 860230`, `textSha256 9be76fda…`, `textWords 73876`. The note's four numbers are exactly the receipt's body/text fields.
10. `grep "defect 5" .ufo/waves/round-34/` (grep tool, gitignore off) → no matches; the defect is named in `.ufo/waves/round-35/w1/ReviewS074Head.md:9` as `corpus/lessons/round-34-verifier-spotcheck.md` "Routed defects" item 5.

## Findings by severity

- **LOW — the note pins the body hash and size to the wrong artifact name.** Note text: "the retained page body (`S074.html.gz`, sha256 `099bc4f9…`, 860,230 bytes)". The file `.ufo/waves/round-34/sources/S074.html.gz` is 114,568 bytes with sha256 `48622909…`; `099bc4f9…`/860,230 are the *decompressed* body (finding 5; receipts.json `bodySha256`/`bodyBytes`). A verifier who pastes `sha256sum`/`stat` on the named file, as the note invites, gets a mismatch and could wrongly conclude the retained bytes drifted — in a freshness lane, the same records-overclaim class this note exists to correct. Wave-1 got this right at `.ufo/waves/round-35/w1/ReviewS074Head.md:23-26` (`zcat … | sha256sum` → `099bc4f9…`). Fix is one wording change ("decompressed body of `S074.html.gz`"); advisory only, append-only per lane rules.
- **No other defect.** Counts, head placement, unchanged-cells statement, row immutability and note placement all reproduce exactly as claimed.

## Shape check

The note matches its neighbors in the notes area: "Round-31 resolution note for S053 and S054 (routed defect 4 of the round-30 closure)" (corpus/SOURCES.md:170) and "Round-23 precision note for S030" / "Round-31 wave-2 anchor note for S059" (:168, :172) share the pattern Round-NN kind note for S0xx (attribution): scoping body, then an unchanged-cells trailer; S074's trailer even spells the cell values (`rejected`, `90d`, `—`) as :170 does. Placement — appended directly after the S059 anchor note, before the Round-35 bounded question — matches wave-1 placement guidance (`w1/ReviewS074Head.md:50-55`). Observation, no severity: the page's og:image content is a bare hex string, not a URL (tmp/S074.html:10); the note only names the meta, so its claims are unaffected.

## Residual risk / not verified

- Live core.telegram.org not fetched (owned-site/network bounds; not assigned). All numbers tie to the retained round-34 bytes only; the round-34 spot-check's independent live confirmation was cited by wave-1, not re-observed here.
- The diff's other additions (S078–S087 rows, S006 used-by change, bounded-question paragraph) were confirmed present but their content was not audited — other seats' scope.
- og: counting used grep over the decompressed body, not a full HTML parser; with 3 total occurrences all at lines 9–11 inside head (lines 3–25), scope is not in doubt for this file.
