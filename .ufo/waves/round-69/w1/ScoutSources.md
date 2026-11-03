# ScoutSources — round 69, W1 (attempt 1)

Seat: ScoutSources. Lane: kake (`/home/vgpnk/Projects/shokunin/kake-shokunin`). Base: `4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4`.
Scope: Frontier-step SOURCES rows S436 (Node.js `os.tmpdir()`) and S437 (Python `tempfile`). No tracked lane file written.

## Fetches — one GET each, retained

| id | final url | status | bytes | sha256 | access (UTC) |
|---|---|---|---|---|---|
| S436 | https://nodejs.org/api/os.html | 200 | 90518 | `0d31bf3c15787b15bcddd8e380dd67c9505d7d47d8892ff4ce69b2ceebb6245b` | 2026-11-03 |
| S437 | https://docs.python.org/3/library/tempfile.html | 200 | 75198 | `4a9695c51c513c70dcd4e1bd51ee836b0e5ace45ed95bc9c493b264ca019beec` | 2026-11-03 |

`curl` exit 0 both; no redirect (`url_effective` = requested url). `content-length` header byte-equal to `%{size_download}` on both, so the retained bodies are whole responses. Versions seen: Node.js v26.13.0, Python 3.15.2.

## Quote class method (declared before verdicts)

- `raw-substring` ⟺ `grep -cF '<quote>' <retained body>` > 0
- `collapsed-only` ⟺ raw = 0 AND `grep -cF '<quote>'` on body after `tr -s '[:space:]' ' '` > 0
- `absent` ⟺ raw = 0 AND collapsed = 0 → discarded, another quote chosen
- word count: `wc -w` on the quote text alone.

## S436 — Node.js `os.tmpdir()`

Anchor: `os.tmpdir()` heading (retained line 490, `id=ostmpdir` once).

Quote (23 words): "On non-Windows platforms, `<code>TMPDIR</code>`, `<code>TMP</code>` and `<code>TEMP</code>` environment variables will be checked to override the result of this method, in the described order."

Class **collapsed-only**: raw = 0, collapsed = 1. Raw fails because the sentence wraps after "checked" (lines 495-496). It is the entry's POSIX sentence naming TMPDIR, TMP, TEMP in that order, as specified.

## S437 — Python `tempfile` — MATERIAL DEVIATION

The spec's named span (the `tempfile.gettempdir()` paragraph listing TMPDIR, TEMP, TMP) is **absent**, structurally, not through a faulty collapse step:

- Three separate ordered-list items; raw separators are `variable.</p></li>`.
- Tag-inclusive span of the three items = 51 words (>25 limit).
- Rendered-prose form (24 words) scores raw = 0 **and** collapsed = 0 → `absent`. Discarded per spec; another quote chosen.

Class **collapsed-only**: raw = 0 (wraps after `<em>TMP</em>`), collapsed = 1. Contiguous, ≤25 words, names all three in order TMPDIR, TEMP, TMP.

Corroboration the `absent` is real: the first `gettempdir()` list item (17 words, names TMPDIR) is **raw-substring** (raw = 1). A same-list quote scoring raw-positive proves the parent's `absent` comes from `<li>` boundaries.

Precedence evidence retained verbatim at lines 508-513: TMPDIR, TEMP, TMP, then platform paths, then cwd — what C2's TMPDIR precedence rests on. S437's row cites the section, not a single sentence, so it does not overclaim.

## rows-draft.md — 11-column schema

Two rows at `.../w1/ScoutSources/rows-draft.md`, one per line. Exercised checks:

```
awk -F'|' 'NF==13'  → 2 lines   |  awk -F'|' 'NF!=13' → 0 lines
pipes per line      → 12 each   |  grep -cF '\|'      → 0 (no escaped pipe)
```

Semantic placement verified (`$1`/`$13` empty from leading/trailing pipe; 11 cells = `$2..$12`): id, source, kind=docs, tier=A, scope, anchor, teaches, status=mined, opened=2026-11-03, recheck=180d, used-by=corpus/lessons/round-69.md — both rows PASS.
Id guard at base: `grep -c '^| S436 |'` = 0, `grep -c '^| S437 |'` = 0. Registry rows at base = 173 → append reaches the contracted 175.

## Attacks named and verdicts

- A1 word limit: `wc -w` → 23 and 19, both ≤25. PASS.
- A2 pipe in cell: `grep -cF '\|'` → 0; 12 pipes/line. PASS.
- A3 column count: `NF==13` → 2 pass, 0 fail. PASS.
- A4 id collision: both 0 at base. PASS.
- A5 spec-quote-absent: the named S437 span is `absent`; caught and disclosed rather than rescued by switching to `stripped+collapsed`, which is **not** a declared class. VERDICT: deviation recorded.
- A6 truncation: `content-length` vs `%{size_download}` byte-equal. PASS.

Note for the L1: if the contract mandates a *gettempdir* sentence, the 17-word first list item is raw-substring and available on request — it names only TMPDIR.

## Artifacts

```
.ufo/waves/round-69/w1/ScoutSources/
├── receipt.json              (url, final url, status, bytes, sha256, access date, command, quote classes)
├── rows-draft.md             (2 rows, 13 fields, no pipes in cells)
├── quote-class-battery.txt   (class method run, raw grep counts per candidate)
└── sources/{S436-node-os.html, S437-python-tempfile.html}
```

Scratch `/fast/scratch/hyaku/kake-r69/ScoutSources` created and removed (`rm -rf`, exit 0; verified gone). No tool installs: `curl`, `sha256sum`, `awk`, `sed`, `tr`, `grep`, `wc` were already present. No git/jj mutation; lane `git status` shows only the untracked `round-69` wave path.
