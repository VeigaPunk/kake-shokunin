# ReviewerC1Substitution — C1 substitution probe (round 54, w1)

Scope: could a "correction" merely delete/rename `(rendered:...)` or leave the old
cell but add a token elsewhere and pass C1? Static logic probed against the
committed counter; cases executed with the counter's own `qualifier_findings`.

## Verdict (headline)

- **Delete or rename `(rendered:...)` alone: no case.** `met` requires
  `corr_ok` (a valid correction block) as a hard conjunct — removing every
  suspect cell still exits 1.
- **Leave the old cell and add a token elsewhere alone: no case.** Same
  `corr_ok` gate; a `crawl`/`巡回` token inside or outside the cell only
  changes suspect status, never supplies a correction block.
- **BUT cell retention is never verified — concrete pass-case exists.**
  Deleting the suspect cell (or renaming its `(rendered:` marker, or rewriting
  the cell's content) **plus appending one marker line** passes C1 with
  `met=True`. The counter enforces "a valid correction block exists after every
  surviving suspect cell", not the contract's "repair is appended, never
  rewritten". The old gloss is fully dispensable/disguisable.

## Counter probed

Canonical runtime = committed file at HEAD `8e408e00fbe1c5908df62ba79e78c944bda479e2`
(`.ufo/waves/round-54/c54_s374_calib.py`, 221 lines; the worktree copy is
identical — `git diff HEAD` empty). Key logic:

- `RENDER_RE = \(rendered: ([^)]+)\)` over whole entry (finditer, `re.S`).
- Suspect = cell matches `recommend|vouch|endorse|refusal|refuse` (i) and has
  no `crawl|巡回` (i). Base file: 2 cells, 1 suspect at offset 520
  (verified by offsets and by committed receipt `suspect_cells=1`).
- Valid correction = literal `[r54-correction 2026-10-25]` occurring anywhere,
  whose following 1200 chars contain the exact QUOTE
  「このリンク先のウェブページの巡回を推奨していない」 **and**
  `NEGATIVE_CRAWL_RE = \bnot\s+recommend(?:\s+the)?\s+(?:crawl|crawling)\b`.
- `mismatch = suspects with corr_at == -1 or corr_at < pos` — suspects
  *before* the first valid marker are "superseded"; suspects *after* it fail.
- `met = quote_ok and corr_ok and mismatch == 0`.

## Executed probes (committed code, real base bytes)

Probed `qualifier_findings` + met computation on base
`68228b2d…:corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`:

| case                                        | suspects | corr_at | met   |
|---------------------------------------------|----------|---------|-------|
| A delete suspect cell only                  | []       | -1      | False |
| B rename `(rendered:` → `(superseded:` only | []       | -1      | False |
| C inject "crawling" inside cell only        | []       | -1      | False |
| D keep cell, append valid marker line       | [520]    | 2815    | True  |
| E delete cell + append valid marker line    | []       | 2703    | True  |
| F prepend same marker line at file top      | [645]    | 1       | False |
| G rename marker + append valid marker line  | []       | 2817    | True  |
| H rewrite cell in place, embedding marker+quote+phrase | [] | 531 | True |

So: the marker is unavoidable, but once it exists (one line suffices —
marker + quote + `not recommend the crawling`), the fate of the
original cell is unconstrained — deleted, renamed, or rewritten in place.

## Findings by severity

1. **HIGH — suspect-cell retention is unverified.** Cases E and G pass
   `met=True` with the original gloss deleted or its `(rendered:` marker
   renamed so `RENDER_RE` no longer sees it. The contract's "the repair is
   appended, never rewritten" (contract.md:15) is enforced only for edits
   that *leave the cell matched by the regex*; removing the regex match
   removes the obligation entirely. A reviewer trusting `mismatches=0` cannot
   distinguish appended-repair from delete-and-append.
   Variant: rewriting the cell in place to contain the marker itself also
   passes (cell content gains `crawl` → un-suspected; marker inside it
   satisfies `corr_ok` since markers are found mid-line anywhere).
2. **LOW — "correction block" is a 1200-char window, not a block.**
   Docstring/C1.3 says "an entry line starting with `[r54-correction …]`";
   implementation matches the marker anywhere (the landed repair itself uses
   `**[r54-correction …]**` mid-line, entry line 54) and borrows QUOTE +
   phrase from the next 1200 chars. Block structure, heading, or that the
   marker line itself carries the claim are unchecked. Mitigating fact: base
   text contains no `not recommend…(crawl|crawling)` fragment (probe:
   0 matches), so a bare marker cannot scavenge validity from pre-existing
   prose — it must carry the phrase itself.
3. **LOW — polarity check is stricter than the contract.** Contract
   requires "the crawl qualifier with English crawl vocabulary"; the counter
   requires the fixed shape `not recommend( the) crawl(ing)`. A correction
   stating the qualifier differently ("does not suggest the crawler fetch
   the target") fails C1.3 despite satisfying the contract sentence. Narrows
   honest repairs, doesn't widen cheating.
4. **LOW — `[^)]+` truncates a cell at the first `)`.** A `(rendered:`
   cell containing parentheses is scanned only up to the inner `)`; trailing
   semantic vocabulary after `)` escapes the suspect test.

## Counter drift (residual risk)

The counter was rewritten across commits *between* freeze (`acae1dc`) and the
repair it validates (`8e408e0`), via `d162cd7`, `f17e769`, `6a5817a`:

- Freeze version: `EN_CRAWL_RE = \bcrawl\b` and `mismatch` on `pos < corr_at`
  — inverted vs the contract's append-only repair: an appended valid block
  counts the old suspect (pos < corr_at) as a mismatch and can never pass,
  while a *prepended* marker + stray `crawl` near file top would pass —
  the exact substitution attack in the assigned question, direction inverted.
- Landed version: `NEGATIVE_CRAWL_RE` and `corr_at < pos` — append passes,
  prepend fails (selftest case `correction_before_render` asserts this).

The version that admits the landed repair was committed inside the repair
commit itself; the committed do-nothing receipt (`controls/base-c1-s374.txt`)
does not distinguish the two semantics (corr_at=-1 at base either way). All
probes above use the landed version; under the frozen version the answer to
the assigned question differs (prepend-with-token passes, append fails).

## Verification gaps

- No probe of worktree-vs-committed divergence for the *entry* file was needed
  (repair reads committed bytes only); entry diff verified at `8e408e0`.
- `run_checks_fix` (selftest path) now shares `qualifier_findings` — fixture
  semantics equal production semantics; earlier revisions had a divergent
  line-wise fixture that silently missed multi-line cells.
- No install performed; pacman untouched per wave directive.
