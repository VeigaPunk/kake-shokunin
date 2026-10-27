# ExecResolverOtherRoutes

Attack seat, round-59 w1. Hunted false-green / false-red routes of the **current** `scripts/id_resolver.py` beyond
K1-K14. Read-only on the lane: tool, registry and knowledge files untouched; fixtures live under
`/fast/scratch/hyaku/kake-r59/ExecResolverOtherRoutes/work*/`.

## Method

- Tool under test: lane `scripts/id_resolver.py` at HEAD `cb685273cc9e331b51f45485793d5d1c91184b3a`, byte-identical
  to base `fd6303ce5c14b3f892dec586297a942ab6e4193b` (`git diff --quiet <base> -- scripts/id_resolver.py` empty),
  snapshot sha256 `2c1b4970a652023a883a414620c07cf393f7c4b28b87053564a45302428e663a`.
- Reference parser: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (GNU Awk 5.4.1), run read-only as
  `census --root <fixture lane> <lane>` + `validate --today 2026-10-26 <lane>` over each fixture. It is the "census
  parser's rule" the tool's docstring names. 11 probe scripts, 98 fixtures; `--revision` variants committed only in
  fixture repos (toplevel asserted, `-c user.name=selftest -c user.email=selftest@local`).
- Expected-correct is grounded in the tool's docstring contract, the census parser, CommonMark (fences, HTML blocks,
  ATX headings) and the round's K8/K9 precedents.
- Live lane: base revision exit 0, `ids_cited=108`; working tree after the concurrent C3 append exit 0,
  `ids_cited=110 ids_resolved=110 dangling=0`, census 164 rows (P7 floor 106, slack 4). None of the routes below
  occurs there today (0 CRLF, 0 leading tabs, 0 non-ASCII-digit ids, 0 lookalike S, 0 URL-embedded ids, 0 ids inside
  knowledge fences/comments, headings at column 0) — all findings are latent routes.

## CASES

Classes: FALSE-GREEN (resolved/clean where the answer is dangling or not-a-registry-row), FALSE-RED (dangling where
the answer is resolved), DIVERGENCE (resolver vs census), CLOSED (no defect), CONTRACT-LIMIT, DISCLOSED-LIMIT.

1. **CRLF registry** (whole file `\r\n`, row `S901` cited). Resolver exit 0, `ids_resolved=1`. Census rows=0,
   validate exit 1, `E12 S901 row outside Registry section` (its `trim()` never strips `\r`). Expected (CommonMark):
   the row is a table row → resolves. Class **DIVERGENCE** — the docstring's "census parser's rule" claim fails for
   CRLF: a CRLF registry passes the resolver and fails the fleet census. Same for a lone-CR file.
2. **Tab-indented row** (`\t| S903 | … |`, cited) → resolver exit 1 `DANGLING S903`; census rows=0, validate exit 0.
   Expected: tab = 4 columns = code, not a row → dangling. **CLOSED** (resolver right; census silent).
3. **Tab-indented `## Registry` heading** → exit 1 `DANGLING S904`; census rows=0 + `E12`. Expected: code. **CLOSED**.
   **Tabs inside cells** (`|\tS905\t| …`) register in both tools. **CLOSED**.
4. **Row inside an HTML block** — `<pre>`, `<script>`, `<style>`, `<textarea>`, `<details>`, `<div>`, `<blockquote>`
   (7 fixtures: one real row + one hidden row, both cited). Resolver exit 0 for all 7 (`ids_resolved=2`): the hidden
   row registers. Census rows=2, validate 0 (equally HTML-blind). Expected (CommonMark HTML block; K8 precedent "a row
   hidden from markdown must not register"): hidden id dangles → exit 1. **FALSE-GREEN, open** — same class as K8, but
   K8's fixture is only `<!-- -->`. Measured: a comment-only fix variant still exits 0 on all 7; a full HTML-block
   variant exits 1 on all 7. Closing it creates a resolver/census divergence of the kind already declared for fences.
5. **HTML-comment-hidden `## Registry` reopens the section** (real `## Paths`, row, then `<!--\n## Registry\n-->`,
   row). Resolver exits 1 but registers the post-comment row (`S995` resolved); census 2 rows + `E12 S994`. Expected:
   both rows outside → both dangling. **FALSE-GREEN, open** (K8 covers a hidden *row*, not a hidden *heading*).
6. **HTML-comment-hidden `## Paths`** → resolver exit 1 `DANGLING S992` (it honours the comment-hidden heading).
   Expected: section continues → registers → exit 0. **FALSE-RED, open**; a comment-aware fix closes it (measured).
7. **`<pre>`-hidden `## Paths`** → exit 1 `DANGLING S997`; expected exit 0. **FALSE-RED, open** — comment-only fix
   leaves it red (measured), full HTML-block fix closes it.
8. **Link reference definition in the registry** (`[ref1]: https://…`) → registers no id, not a row. **CLOSED**.
9. **Registry row with a reference-style source cell** (`[the source][r1]` + definition) → id registers (correct) but
   no URL is extracted; a *sibling* row of that shape owns the id yet reports `url-match=-` although the citing file
   holds that URL. Expected `url-match=<sibling>`. **FALSE-NEGATIVE in the url-match column** (exit unaffected).
10. **Link reference definition in a knowledge file** (`[S962]: https://…`) → counted as a citation, `DANGLING S962`,
    exit 1. Expected per markdown: not a citation. **FALSE-RED** by the tool's broad documented rule (over-approximation).
11. **List item whose content is a pipe row** (`- | S919 | … |`, column 0) → exit 1 `DANGLING S919`. **CLOSED**.
    **Blockquote row** (`> | S923 | … |`) → exit 1 dangling; census rows=1. **CLOSED**.
12. **List-item continuation pipe row** (`- a note` then `  | S921 | … |`, also 3 spaces) → resolver exit 0
    (registers), census rows=2 (also registers). Expected per CommonMark: a paragraph continuation, not a table row.
    **CONTRACT-LIMIT** — P1 requires a 3-space registry row to resolve; do not "fix".
13. **Registry heading with trailing `#`s** (`## Registry ##`) → resolver exit 1 `DANGLING S924`; census rows=0 +
    `E12`. Expected (CommonMark ATX closing sequence): heading text is `Registry` → registers → exit 0.
    **FALSE-RED, open**, consistent between the lane's two parsers; the deliberate trailing-*text* rule
    (`## Registry (legacy)`) does not cover trailing `#`s. A second `## Registry ##` after a real section stays closed
    in both tools (S926/S963 dangle).
14. **Lowercase `## registry`** → dangling; census `E12` + 0 rows. Expected: not the exact heading. **CLOSED**.
15. **Cyrillic lookalike S (U+0405) in a citation** (`Cites Ѕ974`, bytes `d085…`) → exit 0,
    `ids_cited=0 dangling=0`: the citation is invisible while the file cites an unregistered source. Census does not
    read citations. **FALSE-GREEN (laundering), open, contract-ambiguous** — per the id grammar the token is not an id;
    the effect is a clean exit on a file that visibly cites a missing source. Fullwidth S (U+FF33) behaves the same.
16. **Lookalike S in a registry id cell** (`| Ѕ975 |`) → not registered, ASCII twin dangles, census `E02`.
    **CLOSED** (fails closed). **U+200B inside a registry id cell**: same, **CLOSED**.
17. **Unicode-digit ids in a registry cell** — fullwidth `S９７１`, Arabic-Indic `S٩٩١`. Python `\d` matches Unicode
    `Nd`, so the resolver registers the row and resolves the same-spelling citation (exit 0) while the lane grammar
    `S[0-9]{3,}` rejects it (census `E02`, validate exit 1). Expected: not a valid id → must not resolve.
    **FALSE-GREEN, open** — `[0-9]` in `ID_RE`/`ID_CELL_RE` closes it (measured variant).
18. **Fullwidth citation of an ASCII row** (`S９７１` cited, `S971` registered) → output line
    `DANGLING S９７１ …`, an id visually identical to the registered one. **FALSE-GREEN in report integrity** (an
    operator can read it as "S971 is dangling").
19. **U+200B inside a cited id** (`S<ZWSP>972`) → exit 0, `ids_cited=0`. **FALSE-GREEN, DISCLOSED-LIMIT** (the
    contract already lists zero-width-split ids as untested; confirmed open here).
20. **Id inside a URL in a knowledge file** (`https://e.example/p/S987`) → counted as a citation → spurious
    `DANGLING S987`, exit 1. Expected: a path segment is not a citation. **FALSE-RED, open** (live lane: 0).
21. **url-match is a whole-body substring test.** Sibling owns `S966` with URL `https://e.example/966`; the lane cites
    `https://e.example/9662` → `owners=alpha-shokunin url-match=alpha-shokunin`. Expected: no url-match.
    **FALSE-GREEN in the url-match column** (exit stays 1).
22. **Ids inside fenced blocks / HTML comments in a knowledge file** (`| S968 |` in a fence, `cites S969` in a
    comment) → two spurious danglings, exit 1. Expected: not citations. **FALSE-RED, open** — the cited side has no
    fence/HTML awareness although the registry side does (K2/K3).
23. **Indented `## Registry` (1, 2, 3 leading spaces)** → resolver exit 1 (`DANGLING S951/S952/S953`); census rows=1,
    validate exit 0 (its heading rule allows 0-3 spaces; its own selftest exercises widths 0-3). Expected: resolves.
    **FALSE-RED, open** + **DIVERGENCE**.
24. **Indented non-Registry heading ends the section** (`  ## Paths`, ` # Notes`) → resolver exit 0
    (`ids_resolved=2`: rows after the heading register); census rows=1 + `E12 S962 row outside Registry section`,
    validate exit 1. Expected: outside the Registry → dangling → exit 1. **FALSE-GREEN, open** + **DIVERGENCE**;
    reproduced at `--revision`. One regex change (0-3 spaces in `REGISTRY_HEADING_RE` and `SECTION_END_RE`) closes 23
    and 24 together.
25. **Extra line-boundary characters before the id cell** — U+2028, U+2029, U+000C, U+000B, U+0085 (5 fixtures).
    Python's `str.splitlines()` splits on all five, `gawk`/CommonMark do not, so the row is cut and the tail re-parses as
    a new row: resolver exit 0, `ids_resolved=1`; census rows=1 + `E01` (and `E02`) and validate exit 1. Expected: one
    line with an empty id cell → the id is not registered → dangling → exit 1. **FALSE-GREEN, open** + **DIVERGENCE**.
    Measured fix: `text.split("\n")` returns exit 1, matching the census, on all five; the same character after the id
    cell changes no outcome.
26. **Id inside a URL in a registry source cell** (`https://e.example/S938`) → no effect (ids come from the first cell
    only). **CLOSED**.
27. **`--revision` equivalence**: every divergence replayed through committed blobs (22 fixtures at `--revision`) — identical output and exit
    codes to working-tree mode; the divergences are not worktree-only.

Not run: no K1-K14 counter run (base 13/21 per contract; the build seat owns it), no lane build or edit, no sibling-lane
sweeps beyond the two-lane fixtures, no installs/upgrades (no need), no `pacman`.

## TOP RISKS

1. **`str.splitlines()` over-splitting — silent false green, one-line fix, no counter coverage** (case 25). Five
   characters make the resolver cut a registry row and register an id the census calls malformed (E01). A
   resolver-only gate passes a registry the lane's census gate rejects. `split("\n")` closes it and keeps CRLF working.
2. **Heading-indent asymmetry with the census** (cases 23/24). `REGISTRY_HEADING_RE`/`SECTION_END_RE` are column-0
   anchored; the census allows 0-3 leading spaces, including in its own selftest. One direction is a false red
   (indented `## Registry` → every cited id dangles), the other a false green (indented `## Paths` → rows outside the
   Registry register). One regex change fixes both; the real lane's heading is at column 0, so P7 stays green.
3. **The K8 fix must be HTML-block-shaped, not comment-shaped** (cases 4-7). All seven tags measured: a comment-only
   fix leaves rows registering in `<pre>/<script>/<style>/<textarea>/<details>/<div>/<blockquote>` and leaves
   `<pre>`-hidden headings honoured. A full HTML-block rule closes all of them but diverges from the census (which
   counts those rows) — declare it as the docstring already declares the fence divergence.
4. **Unicode id alphabet** (cases 15/17/18). `\d` accepts Unicode `Nd`: a fullwidth/Arabic-Indic-digit row registers
   and resolves a citation the lane grammar forbids, and a dangling line can print a homoglyph id that reads as a
   registered one. `[0-9]` closes the registry side; the cited side (lookalike S) is a laundering route no lane tool
   catches today.
5. **url-match over- and under-claims** (cases 9/21). `url in body` is a whole-body substring test: a sibling URL that
   is a prefix of an unrelated URL fires the match, and a reference-style sibling row loses its URL entirely. The
   counter asserts only the positive (P4); a tightening must keep P4 green.
6. **Cited-side asymmetry** (cases 10/20/22). The registry side is fence- and soon HTML-aware; the cited side counts
   every `S###` including fences, comments, link definitions and URLs → spurious danglings. Live lane has 0 such ids,
   so tightening is safe today, but `ids_cited >= 106` must hold (live 110, slack 4).
7. **Do not "fix" case 12.** A 2-3-space list-item continuation row registers; P1 requires a 3-space registry row to
   resolve, so the resolver cannot separate them without list tracking. Record as a documented limit.

Evidence retained: `.ufo/waves/round-59/w1/ExecResolverOtherRoutes.files/` (11 probe scripts, results JSONs, variant
patches). Scratch deleted. No lane file, index or jj state touched; no install or upgrade run.

VERDICT: beyond K1-K14 the current tool has 5 open false-green classes (splitlines over-splitting, HTML-block rows and
HTML-hidden headings, indented-section-end, Unicode-digit ids, url-match substring) and 4 false-red classes; the K8 fix
must be HTML-block-shaped and the heading rules must match the census's 0-3-space allowance.
