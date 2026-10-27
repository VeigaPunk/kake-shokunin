# ReviewerC3Derive

Scope: `.ufo/waves/round-59/derive_c59_quote_truth.py` and its output `.ufo/waves/round-59/c59_quote_truth.py`,
diffed against the round-58 counter at `45a92b64:.ufo/waves/round-58/c58_quote_truth.py` (identical blob to the
derive's own pin `1c0aa211`, sha256 `57bc3d72…`, verified). **Line numbers below are the v1 artifact** = HEAD blob
sha256 `b3aef90c…` = `contract.json` `C3.counterSha256v1`, which re-running the derive reproduces byte-for-byte
(735 lines). The worktree copy is now version 2 from concurrent w1 seats; that is noted only where it matters.

Evidence method: regenerated the counter in scratch from the derive (identical to HEAD); exec'd the **exact C9
source region (v1:621–663)** against the real base file `crawler-identity.md` plus the real retained S425/S426
bodies; swept `difflib` over all 75 insertion positions of the base file.

## FINDINGS

**F1 CRITICAL — v1:379: the C5 title floor is unsatisfiable for S425, so the frozen predicate 9/9 is unreachable.**
The line requires `units(title) >= 6` **and** `title == page_title`. S425's `<title>` prefix is
`Google Crawler (User Agent) Overview` = **5 units** (`units()` = whitespace tokens for English), and
`title` is `" — ".join(row[1].split(" — ")[1:-1])`, which must equal that string exactly. No registry cell can
satisfy both (a longer middle segment breaks `title == page_title`; a shorter one is empty and trips `not title`).
S426 is 7 units and passes. Consequence: C5 always fails for S425 → `conditions_passed == 9 of 9` never holds →
contract.md's "After: 9/9" cannot be measured. Found independently from the registry side by `ScribeRegistryGate`
(its F1); the worktree v2 already relaxes this to 3+ units. **Fix:** floor at 3 units (or derive the floor from the
title), and record the change in the derive docstring.

**F2 HIGH — v1:641: the C9 window is anchored on the stale *line*, not the bullet/paragraph end.**
`STALE_LINE` (v1:104) is line 31, the *first* line of a wrapped bullet; base lines 32–34 are that sentence's own
continuation and 35–38 open the next bullet. `s < i1 <= s + 1 + STALE_WINDOW` (s=30) accepts i1 ∈ 31..39, i.e.
insertions that **split the sentence being corrected** (31–33) or **split the next bullet's paragraph** (35–37).
Measured: insertion at i1=31 PASSES C9. **Fix:** require the insert exactly where the bullet ends (the v2 change).

**F3 HIGH — v1:641 vs contract.md:73 and the file's own precedent: a "tail" correction fails C9.**
contract.md calls the artifact "an append-only `[r59-correction 2026-10-27]` **tail** in `crawler-identity.md`", and
the file already carries its previous correction as a section at EOF (`## Quote classes (round-51 correction)`,
base lines 57–73) — the lane's stated precedent. Measured: appending the correction at EOF yields
`insert` at i1=74, outside the window, and C9 reports "no inserted line within 8 base lines after the stale
sentence carries [r59-correction 2026-10-27]" → FAIL, even though the correction is present and append-only.
**Fix:** accept an insertion at EOF as well, or amend the contract wording before measurement (contract.md is frozen,
so the counter is the thing to widen).

**F4 MEDIUM — v1:643–647: the C9 tag, citation and quote are matched over the union of inserted lines and over raw
text, not rendered prose.** `tagged` is computed and then only checked for emptiness; `block = " ".join(tails)`
(v1:646) is searched for the tag/citation/quote, so (a) a correction wholly inside one `<!-- … -->` comment PASSES —
invisible to a reader; (b) tag on one inserted line with citation+quote on another PASSES; (c) a quote inside an
inline code span PASSES; (d) a quote inside an indented code block PASSES. Measured, all four. The generated
docstring's own wording ("an inserted line … carries [tag], cites S425, and holds a double-quoted span") is not
enforced per line. **Fix:** strip HTML comments and code spans/blocks before matching and require all three signals
on the same inserted line (v2 strips comments/code spans from `block`, but its `CORRECTION_TAG not in block` check
still searches the union, so the per-line requirement stays unenforced).

**F5 MEDIUM — v1:385: the printed-revision check left the article block and now accepts any text node on the page.**
Round 58 required `in_content(...)` (article block). v1 scans `re.findall(r">([^<>]+)(?=<)", texts[sid])` over the
whole document. Measured: the test is satisfied not only by the genuine `<p>Last updated … UTC.</p>` inside
`<devsite-content-footer>` (far outside the article window, which ends at `<devsite-content-footer`), but also by a
`<template class="devsite-content-data-template">` **JSON payload** (S425 offset 40030, S426 offset 35375) — a
non-rendered blob. Necessity is real (the date is not in the article body); the breadth is not what the derive
docstring describes ("page footer text node"). **Fix:** scope to `ARTICLE_END` … `</devsite-content-footer` and
exclude template/script/style bodies (v2 excludes script/style only; `<template>` still satisfies it).

**F6 LOW–MED — the derive docstring does not justify three changes it makes.** It enumerates (a)–(g), but not:
the `page_title` separator `"_" → " | "` (v1:378); the anchor unit floor **4 → 3** (v1:396); and the *removal* of
round-58's page-uniqueness requirement for the anchor (`texts[sid].count(anchor) == 1`). Also the used-by compare
became order-insensitive (`sorted` on both sides, v1:353–354) where round 58 compared exact order. The generated
artifact's own C5 text mentions the title separator, but the derive docstring is the stated justification source.
**Fix:** add these to the docstring (the uniqueness drop is *necessary* — see W3 — so saying so is enough).

**F7 LOW — v1:677–679: `--selftest` is a stub returning 2 and the derive deletes round-58's ~120-check selftest.**
Disclosed in the derive docstring and consistent with the round-58 v1 pattern, but v1 ships with **zero** executed
checks; wave 1 must port the kill matrix before any claim is measured (`CriticC3Cheat` ran no fixtures either).

**F8 LOW — v1:412: misleading diagnostic.** The message says a span is "not a raw substring of the retained body",
but v1:368 whitespace-collapses the body before every span test, so "raw" is no longer true. Cosmetic; a reviewer
reading a failure note would look for the wrong cause.

**F9 MEDIUM (process) — the derive writes `.ufo/waves/round-59/c59_quote_truth.py` unconditionally.** The worktree
copy is now v2 (peer edits: title floor 3+, `<pre>/<code>` excluded from headings, script/style excluded from the
date test, bullet-end window, prose filter) while HEAD is v1. Any seat that runs the derive in the lane silently
reverts those fixes. **Fix:** refuse to overwrite when the target differs from the committed blob, or derive v2 from
an amended buffer.

**F10 SOUND (no action) — main() pins both revisions once.** v1:706–707 resolve `--revision` and `--base` each once
to commit ids (`rev-parse --verify --quiet <x>^{commit}`); v1:712–713 use only the pinned ids, and `--root` must
equal `rev-parse --show-toplevel` by realpath (v1:701). `clean_env()` strips inherited `GIT_*` for both `git()`
(v1:121) and `show_bytes` (v1:138) — routed defect D2 fixed forward. The derive is deterministic and pins its own
source by revision, and asserts both retained bodies against `receipts.json`.

**F11 SOUND (no action) — C9's difflib append-only test is sound in the fail direction; repeated blank lines do not
break it.** `get_opcodes()` partitions both sequences, and a base line not covered by an `equal` block necessarily
lands in `delete` or `replace`; therefore "no delete/replace" ⟺ measured = base + insertions, and a rewrite or
deletion cannot be hidden. `autojunk=False` is correctly set (the default would treat lines appearing in >1 % of a
≥200-element `b` as junk — blank lines in a large markdown file — and destabilise alignment). Measured on the real
base file: all 75 single-insertion positions produce insert-only opcodes with `i1` equal to the true position;
modifying 4 different non-blank base lines each produces `replace`; deleting a blank line produces `delete`. The
file has 19 blank lines and no repeated non-blank line; repeated blanks can only make *which* identical position an
insertion is attributed to ambiguous — bounded inside the run, i.e. inside the window — and cannot manufacture a
`delete`/`replace` (that would be a false FAIL, not a false pass). The weak part of C9 is the window and the prose
semantics (F2–F4), not the diff.

## WEAKENINGS

- **W1 collapsed whitespace instead of a raw substring (v1:368) — JUSTIFIED.** The derive docstring discloses it for
  English pages ("source HTML wraps sentences across lines") and the round's own quote rule says "a substring of ONE
  whitespace-collapsed text node". Collapsing never merges across a tag, so the one-text-node invariant holds, and
  `text.count(span) == 1` is now measured on the collapsed document, which can only *raise* the count (stricter).
- **W2 160 instead of 40 characters (v1:95) — JUSTIFIED.** 25 English whitespace tokens run to ~150+ chars and the
  round rule freezes ≤160. Residual: round 58's 40-char cap also bounded the "every double-quoted span of 2+ units"
  guard, so a 2-unit span may now be 160 chars; it must still be a real body substring. Low.
- **W3 anchor page-uniqueness dropped and floor 4 → 3 (v1:396) — NECESSARY, not a cheat, but undisclosed (F6).**
  Measured: **every** `<h2>/<h3>` on both pages occurs twice in the page (TOC + heading), so round-58's
  `count(anchor) == 1` was unsatisfiable for any real anchor. Requiring membership in the article block's h2/h3 set
  is a structural substitute; the residual loss is that a duplicated or generic 3-word heading can serve as anchor.
- **W4 date in a footer text node (v1:385) — NECESSARY but over-broad (F5).** The revision line genuinely lives in
  `devsite-content-footer`, outside the article window, so round-58's article-block scope was impossible; but the
  implementation also accepts `<template>` JSON, which the docstring does not claim.
- **W5 C9 prose semantics — WEAKER THAN ITS OWN SPEC (F4).** Comment- and code-hidden signals count; the three
  signals need not share a line.
- **W6 used-by comparison order-insensitive (v1:353–354) — harmless.** A used-by cell is a set; round-58's exact-order
  compare was incidental, and duplicates still fail.
- Round constants, article-block markers, per-row `TOPIC`, `USED_BY` (S425 = entry + `crawler-identity.md`), the
  `round59` receipt tag and the `C9` addition itself are all justified by docstring items (a)–(e), (g).

## VERDICT

V1 is faithful to the derive in every line and sound where it matters most (both revisions pinned once, D2 fixed
forward, append-only diff sound), but it is **not shippable as frozen**: its C5 title floor makes S425 unsatisfiable,
so the contract's 9/9 after-state is unreachable, and C9 admits a correction that is invisible (HTML comment), split
across lines, or spliced mid-sentence, while rejecting the "tail" placement the contract and the file's own
precedent prescribe.

VERDICT: blockers F1 (title floor ⇒ 9/9 unreachable) and F3 (contract "tail" ⇒ C9 rejects it) must be fixed and the
fixes recorded in the derive docstring (F6) before wave 1 scores C3; F2/F4 tighten C9 placement and prose; F9 keeps
the derive from reverting the in-flight v2 fixes.
