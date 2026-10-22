# CriticCounterV2 — attacks C2 counter version 2 (`sealed_count.py`, sha256 1b4d9d59…3469b) for new evasions

Verdict summary: version 2's claim that every condition reads "what a reader sees" is overstated. Two sandbox commits on 7deacc46 score `met: true` with the revealed key, while a CommonMark reader (cmark 0.31.2) sees a stub entry (commit A) or a registry with no round-35 rows (commit B). The landed C2 result at 95abec21 is not shown to be gamed: the landed entry and SOURCES.md contain none of these constructs (0 Cf characters, 0 `<!--`, 0 link reference definitions, 0 fences; the only NFKC change is U+2026 to `...`).

Oracle: `cmark --unsafe` (CommonMark reference renderer, /usr/bin/cmark, already installed), visible text = HTML text nodes. No tools were installed or updated.

## Routes (code lines are in `.ufo/waves/round-35/sealed_count.py`)
| Route | Code | Result | Verdict |
|---|---|---|---|
| 1. Unterminated `<!--` hides honest text | 202 `<!--.*?(?:-->\|\Z)` | At line start: reader and counter both hide to the end (CommonMark HTML block type 2). Mid-line or in a code span: the reader sees literal `<!--` and the text after it; the counter drops everything to the end of the file. `<!-->` is a complete comment in CommonMark 0.31, but the counter strips to the next `-->`. | OPEN, but only as an undercount (honest text lost). Not an evasion. |
| 2. NFKC and Cf folding | 200-202: folding runs before comment removal | A fullwidth `－－＞` (U+FF0D U+FF0D U+FF1E) or `--`+U+200B+`>` inside a real comment closes it early for the counter only, so hidden text is counted. Reverse case: a fullwidth `＜！－－` in visible text strips the rest of the file. Fullwidth letters fold into probe words. | OPEN, evasion (scored, commit A). |
| 3. URL substring matches a longer junk URL | 269 `url in c[1]` | A source cell `https://junk.invalid/redirect?to=<receipt URL>.attacker.invalid/x` passes. | OPEN, evasion (scored, commit B). |
| 4. Registry heading inside an HTML comment | 202 runs before 218 | A plain comment is closed: the counter ignores the heading and still sees all 87 real rows. Combined with route 2 it opens: `<!-- …－－＞` / `## Registry` / `\| S078 \| fake \|` / `-->` placed before the real heading becomes the counter's first Registry (1 row, so the real registry is ignored). The reader sees nothing of it. | Closed alone; OPEN combined with route 2 (unit check, no commit). |
| 5. Honest text inside a fence is still counted | 241 and 272: the entry is not de-fenced | Code-block text is visible to the reader (as code), so counting it is not hidden padding. | CLOSED as an evasion; tradeoff only. |
| 6. (new) Link reference definitions | 202 handles comments only | `[//]: # "…"` and `[a]: # "…"` lines are never rendered, but the counter counts their probes and cites. | OPEN, evasion (scored, commit A). |
| 7. (new) Fence closing ignores length | 210-213 | A 4-backtick block that contains two 3-backtick lines: the counter closes and reopens the fence around the rows inside, so it counts rows that the reader sees as code. This violates the docstring rule "outside backtick and tilde fences". | OPEN, evasion (scored, commit B). |
| 8. (new) S086.txt and S087.txt are unpinned | 71-81 pin only S006 and S078-S085; 250 reads whatever .txt files exist at REV | A transcription of S086.txt scores copiedShare 1.0. With S086.txt deleted at REV it scores 0.1543 (at most 0.25 passes), and pinned_ok stays true. | OPEN (unit check, no commit). |

## Sandbox commits (clone /fast/scratch/hyaku/kake-r35/w2/CriticCounterV2/clone, both on 7deacc46)
Both commits also delete `.ufo/waves/round-35/sealed/`, because the counter exits 2 while a key is visible at REV (line 300).
- A `06d7e878452d1f1729d4bf89a3f6e6cfc5379d0d` (branch critic-a): the entry is a 3-line stub plus hidden text (`entry-a.md`).
  - Score: exit 0, met true, conditions all true, words 126, copiedShare 0.0, goodCites S078 S079 S080 S082, probes 12/12.
  - cmark reader view: "Publishing security.txt / This entry is withheld pending review. / End."
  - Ablations (`ablate.py`): each route is necessary on its own. Neutralizing the fullwidth close leaves 8 probes and 2 cites; neutralizing the zero-width close leaves 8 probes; removing the link reference definitions leaves 8 probes. Each falls below the 9-probe target.
- B `add801378036000a36c493d9bd42cccb6603885f` (branch critic-b): built by `build_b.py`. It moves rows S078-S087 into a 4-backtick block using the parity trick and rewrites each source cell to a junk URL that contains the receipt URL. The entry is unchanged.
  - Score: exit 0, met true, goodCites S078 S079 S080 S082 S083 S084 S085 S086 (8), probes 12/12.
  - cmark: all ten ids sit inside `<pre>`; none are in the rendered registry.
  - Ablation: without the two inner 3-backtick lines, the counter sees 0 of the S078+ rows.

## Commands (all exit 0)
- `python3 -B routes.py`: reader view against counter view for routes 1, 2, 5, 6 and 7.
- `python3 -B <lane>/.ufo/waves/round-35/sealed_count.py c2 --root clone --revision <A|B> --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc`: exit 0 for both A and B. Outputs are in `score-<rev>.json`.
- `python3 -B ablate.py`: ablations for A and B, plus the route 4 checks.
- Inline python run against the clone at 7deacc46: the S086 copiedShare figures (1.0 and 0.1543).
- Landed-construct scan of 95abec21: entry and SOURCES.md (figures in the verdict summary).

## Impacted axes
Freshness: the "copied", "probes" and "cites" conditions can be met by text and rows a reader never sees. Operability: none (C1 not touched).

## Smallest safe correction
1. In clean(), strip comments on the raw text with CommonMark rules: block comments start at line start; inline comments only when closed; `<!-->` and `<!--->` count as closed. Do this before NFKC and Cf removal, or derive text from `cmark` output.
2. Drop link reference definition lines.
3. Close a fence only on the same character, at least the opener's length, and no info string.
4. Compare the source cell's URL token for equality with the receipt URL, not as a substring.
5. Pin every .txt named in receipts.json, including S086 and S087.

Any of these changes the counter's bytes, so it needs a version 3 and a rescore of the controls.

## Not verified
- GitHub's GFM renderer (cmark has no table extension; table rows were judged by `<pre>` placement).
- Routes 4 and 8 as scored commits (two-commit cap).
- `ENTRY in c[10]` (line 269) is also a substring test, so a used-by cell such as "not corpus/knowledge/security-txt-publishing.md" would pass. I read this from the code only; it was not run.

Deliverables: /fast/scratch/hyaku/kake-r35/w2/CriticCounterV2/{routes.py, ablate.py, build_b.py, entry-a.md, score-06d7e878452d1f1729d4bf89a3f6e6cfc5379d0d.json, score-add801378036000a36c493d9bd42cccb6603885f.json, b.html, landed-entry.md}
