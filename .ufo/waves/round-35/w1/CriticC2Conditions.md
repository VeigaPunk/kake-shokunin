# KakeR35.CriticC2Conditions — attack on C2 size, copied and cites (round 35, wave 1)

Sealed directory untouched, no probe key loaded. All checks ran in sandbox S = /fast/scratch/hyaku/kake-r35/w1/CriticC2Conditions/
on a clone at 318561e; counter sha256 c4d58dae…49ef matches the receipts.

## Method
- `S/nonprobe.py` runs the frozen counter's `run_c2` with only `load_key` replaced by an empty probe
  list, so `probes` is always false and the other four conditions are the counter's own code. It
  reproduces the junk, keyword and transcript receipts exactly (copiedShare 0.0, 0.0, 0.9951).
- `S/build.py` (exit 0) built 27 attack commits on 318561e (`S/built.json`). Scored with
  `python3 -B nonprobe.py clone <sha>` (exit 0, `S/nonprobe-results.txt`) and rendered with
  `uvx --with cmarkgfm==2024.11.20 python -B render_check.py clone <shas>` (exit 0,
  `S/render-results.txt`); cmark-gfm is GitHub's Markdown library. The correction runs in
  `S/patched.py` (exit 0, `S/patched-results.txt`).

## Findings (frozen counter; the first three are copied and size)
1. **Hidden dilution beats copied** (`sealed_count.py:228-233`). The commit is the transcript control's
   RFC text plus verbatim S006, S080, S082 and S084 sentences. One HTML comment holds a single
   hyphen-joined token (40,000 counter words). Commit dce145db: words 1473, copiedShare **0.0376**,
   copied, size and cites all true. The rendered page shows only the transcription. Without the comment
   (3b099002) the share is 0.9781.
2. **Invisible zero-width characters beat copied.** A U+200B inside at least one word of every
   8-word window splits words for `words()` (`:206-207`). It is invisible on screen and not whitespace
   to `split()`. Commit 79277c9f: words 1470, copiedShare **0.0043**, copied true.
3. **Size is counted in whitespace words (`:221`), but shingles use `[a-z0-9]+` words.** The whole
   RFC 9116 text (5590 words) joined with hyphens in groups of 25, plus the hidden dilution comment:
   bc064c07, words **234**, copiedShare 0.1272. Both size and copied are true.
4. **Light rewording passes copied.** It takes about one edit per 8 to 10 words of the 1303-word RFC
   transcription (tokens means whitespace-separated words here):

   | edit (one per k tokens) | k=6 | k=8 | k=10 | k=12 |
   |---|---|---|---|---|
   | swap adjacent | 0.054 pass | 0.091 pass | **0.237 pass** | 0.345 |
   | synonym/plural | 0.075 pass | **0.159 pass** | 0.323 | 0.427 |
   | insert "also" | 0.090 (size fails) | **0.237 pass** | 0.373 | 0.461 |

   This is a limit of exact 8-word matching. No threshold catches a paraphrase.
5. **Junk rows pass cites** (`:235-243`): only cells 7, 8 and 10 are checked, never a receipt, URL or
   text, so S081 (a rejection candidate) and S097-S099 (never opened, f3490268) count. Each of these
   reaches 3 good cites: rows in `<!-- -->` (2ddeb2a1, no row rendered); rows in a `~~~` fence, since
   only backtick fences are skipped at `:192` (a740c3e6, renders as code); a second `## Registry` at the
   end of the file, `:197-198` (cc63fbcb, no table row); ids only in an entry comment (f4c5dd41).
6. **Duplicate ids can be hidden** (`:239`, `len(rows) == 1`). Visible rows read `| S082​ |` with a
   U+200B after the id and status `rejected`. The regex at `:200` misses them, so the counter sees only
   hidden `mined` rows (6b40dda7, cites true). cmark-gfm shows only `rejected` rows. A plain visible
   duplicate is caught correctly (ea34c23f, cites false).
7. **Escaped pipes: no mismatch found.** `\\|`, a pipe inside a code span, and `\|` (e97b0207) split
   into 11 cells with `mined` at index 7 in both the counter and cmark-gfm.
8. **Probes (public description only):** probes use `any(re.search)` on the full normalized text, so
   adding text never removes a match. My inference, since I never saw the key: the v1 commit keeps
   every probe the transcript control matched (8 of 12), unless a sealed regex is anchored to the end
   or uses a negative lookahead.

## Candidate controls (prerequisite 318561e; bundle verify exit 0; the L1 scores them)
- `S/bundles/r35-critic-c2-v1-dilute-comment.bundle` (sha256 a0d2300e…92fa), ref
  `attack/v1-dilute-comment`, commit dce145db. It meets entry, size, copied and cites with no learned
  content, so it is a full do-nothing control if the hidden probes reach 9 or more.
- `S/bundles/r35-critic-c2-v2-zwsp-hiddenrows.bundle` (sha256 847855f4…9f20), ref
  `attack/v2-zwsp-hiddenrows`, commit 79277c9f. It is the same text broken with U+200B. Its junk rows
  for S082-S085 are inside an HTML comment, so nothing appears in the rendered registry. U+200B inside
  short words may lower its probe count.

## Smallest safe correction (`S/patched.py`, sha256 18b44a60…4596)
- Before any condition reads text: NFKC, drop Unicode format characters (category Cf) and HTML
  comments (an unclosed one runs to the end of the file).
- Count size in the shingles' `[a-z0-9]+` words; re-declare the limit (the 1303-word transcript is
  1551 such words). Read rows only from the table under the first `## Registry`, outside backtick and
  `~~~` fences. A cite counts only if `receipts.json` retains the id and the row's source cell names
  its url or finalUrl.
- Result: findings 1, 2, 3, 5 and 6 now fail; all 77 base rows still parse; the junk control falls to
  goodCites [S078] (its source cell happens to hold S078's URL).
- Still open (a tradeoff the non-author review must judge): rewording, and junk rows that copy a
  receipt URL. A second gate of 5-word share ≤ 0.25 rejects swap k=8 (0.33) and synonym k=8 (0.45),
  but not swap k=6 (0.12). Honest calibration: link-preview-metadata.md scores share5 0.14 and
  ghp-served-set.md 0.0006 against their own retained sources. Sealed probes do not test row quality.

Not verified: probes on any commit (key sealed); rendering on github.com itself (cmark-gfm stands
in); the patch on a real honest entry (none exists yet).
Tooling: cmarkgfm 2024.11.20 from PyPI via `uvx` (cache S/tmp/uvcache, nothing global), to test GFM rendering.
