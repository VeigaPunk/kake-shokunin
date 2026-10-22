# Round 29 wave 1 — critic: can the C1 counter pass while the knowledge is untrue?

Seat: KakeR29.CriticC1CounterGameable (leaf critic, freshness). Advisory input only; no verdict on the round.

## Answer

Yes. Twelve fake states each score `C1 4/4`, exit 0, `controlBroken: false`. The counter shows that a short
string is present in a retained text file whose hash matches a receipt in the same commit. It does not
show that the string is page prose, that the entry claims what the quote says, that the claim is true,
or that the retained bytes are the bytes opened at e58b66c (let alone the live page).

## Setup

- Sandbox clone of the lane at e58b66c: `/fast/scratch/hyaku/kake-r29/w1/CriticC1CounterGameable/clone`
  (TMPDIR set inside the sandbox). Each state is a commit on branch `fake/<name>` branching from e58b66c.
- Builder: `.../CriticC1CounterGameable/build_states.py` (sha256 7e9e47483466…). It adds four 11-cell
  `mined`/`2026-10-22` registry rows, an entry with an 8-line header, and a lesson `## Gate`.
- Candidate companion check: `.../CriticC1CounterGameable/check_integrity.py` (sha256 377b6b4ec8b4…).
- Counter outputs, one JSON per state: `.../CriticC1CounterGameable/out/<name>.json`.

## Commands and exit codes

- `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision HEAD` in the clone at e58b66c: exit 1, `C1 0/4`.
- `python3 -B build_states.py <clone> <out>`: exit 0. It runs the counter once per state (results below).
- `python3 -B check_integrity.py clone <rev>` on five states: results in the last section. The first run
  died with a NameError (my exec namespace lacked `__file__`); I fixed it and reran.
- My first F4b body duplicated the title, so it was not a consistent fabrication. I fixed it and rebuilt
  all states. The build is deterministic, so every other revision stayed the same.

## Attempts (counter result at each revision)

| State | What is fake | Rev | Counter |
|---|---|---|---|
| H0-honest | nothing: on-topic prose quotes, claims follow | 348e00c21eba | 4/4, exit 0 |
| F1-navigation-quotes | every Gate quote is sidebar, footer or pager text, e.g. S040 “Skip to main content Skip to content GitHub Docs Search or ask Copilot” | a89218d7b200 | 4/4, exit 0 |
| F2-gate-unrelated-false-entry | entry claims project sites are served at the host root and Vite needs no base (false); Gate quotes are true but off-topic (S040 IP logging, S042 date filter) | 5994761ff8de | 4/4, exit 0 |
| F3-see-also-only | entry body is one false claim plus `See also: S040, S041, S042, S043.`; registry used-by is `-` | 08572e605fb7 | 4/4, exit 0 |
| F4-fabricated-text-receipt | S043.txt replaced with an invented sentence (“Vite sets base to the repository name automatically”); receipts.json textSha256 recomputed; html.gz untouched | 2392173a0ce4 | 4/4, exit 0 |
| F4b-fabricated-text-body-receipt | as F4, plus an invented html.gz and bodySha256 that are mutually consistent | 73cb09c5d87a | 4/4, exit 0 |
| F5-table-cell-splice | S040 quote “Project sites Source files Must be stored in a repository named <owner>.github.io” joins a column header to the user-site cell; entry states that false claim | 2172ac9bebfa | 4/4, exit 0 |
| F6-truncated-context | S043 quote “you can remove base from the configuration, as it defaults to '/'” (the user-site case); entry applies it to project sites | 973e3337d4a3 | 4/4, exit 0 |
| F7-one-word-quotes | Gate quotes are “GitHub”, “Jekyll”, “baseurl”, “base” | 1eae665190f0 | 4/4, exit 0 |
| F8-html-comment-only | entry cites the ids only inside `<!-- -->`; all Gate lines sit inside an HTML comment, so nothing renders | e8a9663369d7 | 4/4, exit 0 |
| F9-mid-word-edges | S040 quote “ository on GitHub. Copy markdown Who can u”: both edges inside a word, spanning page chrome (from KakeR29.ConnectorSiblingOverlap, reproduced here) | a51ee4b77a8f | 4/4, exit 0 |
| F10-registry-url-superstring | registry S040 source cell cites `…/about-github-pages-2026`, a different URL that contains the receipt URL (from KakeR29.MutantsCounterC1, reproduced here) | d902bc64f83d | 4/4, exit 0 |
| N1-one-letter-changed | S042 quote “Prepond …” | 86fbca094bb5 | 3/4, exit 1 (S042 d) |
| N2-text-edited-receipt-stale | S043.txt fabricated, receipt not updated | 2709193715cd | 3/4, exit 1 (S043 d) |
| N3-26-word-quote | S040 quote of 26 words | d1256f03c45b | 3/4, exit 1 (S040 c) |

The negative controls N1 to N3 show the counter does what it is built to do: an exact quote, at most
25 words, in a text file whose hash matches its receipt.

## Why each attempt passes (code pointers in c1_quote_truth.py at d18bbf3)

- Check d (lines 107-111, `quote in text` at 111) is a plain substring test with no token edges, so a
  quote can start and end inside words (F9). chousa fixed the same gap in round 4
  (chousa-shokunin/corpus/knowledge/anchor-boundaries-r4.md:31-37, rule at :60-85). The test also runs
  on the whole visible text, which includes navigation,
  footer and cross-cell joins. fetch_sources.py:33-38 collapses tag boundaries into single spaces, so
  adjacent table cells read as one sentence (F5). Nothing ties the quote's meaning to the entry (F2, F6).
- Check c (lines 103-106) has a minimum of 1 word (F7) and reads raw lesson lines, comments included (F8).
- Check b (line 102) accepts any word match of the id after line 8 (line 91), including See-also lines
  and HTML comments (F3, F8). It does not check used-by in the registry (line 100 reads cells 1, 7, 8 only).
- Check a (line 101, `url in cells[1]`) is a substring test, so a source cell citing a longer, different
  URL passes (F10). The fix is to extract the URL token from the cell and compare it for equality
  with receipts `url`, the requested URL. For S040, `url` differs from `finalUrl`, so the row must cite
  the requested string, and limit 4 still asks for the final URL to be recorded alongside it.
  KakeR29.MutantsCounterC1 found this (their mutant 3312e3cd6032).
  Their second mutant (64348fad9b74: one word of S040.txt doctored, receipt rehashed) is the F4 class.
- The sha check (lines 109-110) compares the text file with receipts.json from the same commit. Any
  later commit can rewrite both together (F4). Neither bodySha256 nor the html.gz-to-txt derivation is
  checked (F4b).
- The control (line 113) only shows that the substring test is not constant-true. It cannot catch
  F1 to F8.

## Candidate correction tested (sandbox only, not applied)

check_integrity.py checks two things: `git diff --quiet e58b66c <rev> -- .ufo/waves/round-29/sources`,
and that each txt equals fetch_sources.visible_text(gunzip(html.gz)) with the body sha256 matching.

- H0 and F1: exit 0 (pinned, derived).
- F4: exit 1 (not pinned; S043 not derived).
- N2: exit 1 (not pinned; S043 not derived).
- F4b: exit 1, but only because of the pin; the derivation check passes on a consistent fabrication.

Token edges: `.../CriticC1CounterGameable/token_edges.py` (sha256 3064e2adad8e…; `python3 -B token_edges.py
<clone> <out>`, exit 0) applies the chousa r4 word-character rule, without its hyphen and apostrophe
clause, to every passing quote. It flags F9 S040 and nothing else. H0 keeps clean edges, so the rule does
not reject the honest state. It does not catch F1 to F8, whose quotes all start and end on word boundaries.

These are proposals only. This seat does not own the counter; applying them is for the round-29 owner.

So the smallest safe correction for provenance is the pin to e58b66c. It can run as a second counting
command next to the frozen counter, so the declared counter does not change after declaration. Add
`git diff --quiet d18bbf3 <commit> -- .ufo/waves/round-29/c1_quote_truth.py`, because the counter
runs from the working tree, not from `<commit>`. F1, F2, F3 and F5 to F8 need human review of each
Gate line against the entry claim it supports. That is a review step; no string check can do it.

## Limits the SCORECARD should state

1. C1 shows that the quote is present in the retained visible text and that the text matches its
   receipt in the same commit. It does not show that the quote is article prose rather than navigation,
   footer or a cross-cell join, that the entry claim follows from the quote, or that the claim is true.
2. Retained bytes are what the L1 saved at 2026-10-22T10:29:37Z. Unless pinned, any later commit can
   replace them. Even when pinned, nothing shows they equal what the server sent, except a re-fetch or a
   third-party archive. A fabrication made inside e58b66c itself is invisible to every offline check.
3. "Retained visible text" is not the rendered page. `<wbr>` and code spans become spaces, so S040.txt
   has `http(s):/ / <owner>.github.io/ <repositoryname>` (the raw html.gz has `<wbr>` there) and S041.txt
   has `--baseurl = ""`. The core project-site URL form cannot be quoted as a reader would see it.
4. S040 redirected: receipts.json says url `…/about-github-pages`, finalUrl `…/what-is-github-pages`,
   and the page title is "What is GitHub Pages?". The SCORECARD calls it "About GitHub Pages", and check a
   matches only the requested url. The registry row should record the final URL and title.
5. Check d is a raw substring test: a quote may begin and end mid-word (F9). A token-edge rule closes
   only that class; quotes cut at a word boundary but out of context still pass (chousa r4 names the same
   residual, anchor-boundaries-r4.md:124-130).
6. The 4/4 count is per id, not per claim. One quote per id can stand behind an entry that makes many
   uncited or false statements (F2, F3).

## Not verified

No live page was opened (this seat has no fetch grant), so nothing here compares the retained bytes
with the live pages. The real entry and lesson do not exist yet, so the landed Gate lines were not
reviewed. check_integrity.py ran only on H0, F1, F4, F4b and N2. Nothing was installed. In the lane I
wrote only this report; every other write stayed in the sandbox.
