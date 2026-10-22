# ConnectorSiblingOverlap — Kake round 29, wave 1 (read-only sibling-overlap scan)

Axes: operability, freshness. Seat: leaf connector. No sibling file, git or jj state was mutated. No network was used. No installs were needed. No sandbox files were produced; this report is the only file written.

## What I scanned

I scanned `corpus/knowledge/`, `scripts/`, `tools/`, `corpus/SOURCES.md`, `PROVINCE.md` and `SKILL.md` in all 20 sibling `*-shokunin` lanes. The search terms were: base path, baseurl, project site, relative_url, absolute_url, link check, lychee, `github.io/`, GitHub Pages, Jekyll, `vite.dev`, root-relative, urljoin, WHATWG, RFC 3986 and `docs.github.com`. All searches were `rg` and `sed` reads, and each exited 0, or 1 where there were no matches. Most hits are `baseURL` in model-provider configuration, in kagi, kama, kengaku and kumitate. Those are false positives with no web base-path content, and I list them only as "no overlap" below.

Sibling HEADs read: game-dev-3d 89dd182b7094, chousa 6c5eb1466f2b, tameshi a08e85c5d7f8, kengaku 1f3b0f1ec41e, kumitate dfa159d5152f. Kake HEAD is e58b66c203bed4e38f89afeaa9573d980344ab64.

## Overlaps, each with a boundary call

1. **game-dev-3d: a third-party project site whose path prefix moved.** `game-dev-3d-shokunin/corpus/knowledge/unreal-mcp/adaptation-kimi.md:416-440` (sha256 a2db1d283ef3…). On 2026-10-18, four `https://moonshotai.github.io/kimi-code/<page>.html` URLs returned 404 and the same URLs with `/en/` added returned 200. The cause is a locale prefix moving under an intact `/kimi-code/` base path, not a root-relative escape.
   Boundary: kake MAY cite this as a sibling observation, not as a new source ID. The URL is not a kake property, and the evidence is a live curl from 2026-10-18 that this round did not re-run. It is a different failure class from C2's `outside_base_path`.
2. **kumitate: the same site, as strings in the kimi binary.** `kumitate-shokunin/corpus/knowledge/kimi-binary-secrets.md:68,:325` points at `moonshotai.github.io/kimi-code/` and `/en/release-notes/changelog.html`.
   Boundary: kumitate owns kimi binary and route census. This is no base-path knowledge, and there is nothing for kake to reuse.
3. **chousa: a quote-truth method that is directly reusable for C1.** `chousa-shokunin/corpus/knowledge/anchor-boundaries-r4.md:31-37` records that substring matching let "a truncated or padded variant of real source text" resolve. Its r4 fix is a token-boundary rule (`:60-85`; code at `chousa-shokunin/tools/research-gate.sh:1258-1287`, `tok_word_char`, left and right boundary checks). `claim-support-states-r24.md:22` uses the same "verbatim (≤25 words)" quote table as kake's Gate.
   Boundary: chousa owns the method, per `chousa-shokunin/PROVINCE.md:5-8` and `kake-shokunin/PROVINCE.md:34-35`. Kake may apply the rule inside its own counter or falsifier, but must not import chousa's gate or claim its finding IDs.
4. **tameshi: mutation-score semantics next to C2's three constant gates.** `tameshi-shokunin/corpus/knowledge/mte-report-interop.md:1-3,162-168` holds mutation-testing-elements states and metrics, from S001, S002, S086 and S087, which are tameshi's own IDs. It contains no URL, link or base-path content.
   Boundary: C2's "three constant gates must each fail" is a counter self-control, not a mutation score. Kake must not report it as a kill rate or as an MTE report. `tameshi-shokunin/PROVINCE.md:14-16,44` says every lane's gate stays its own, so there is no overlap in substance.
5. **tabi: browser-side base URL evidence.** `tabi-shokunin/corpus/knowledge/cdp-evidence-patterns.md:75,77` shows that Chrome DevTools Protocol `DOM.getDocument` and `DOMSnapshot` return a `baseURL` key. This is the rendered document base, the runtime counterpart of C2's static `<base href>` rule (kake S024). tabi has no link crawler or link checker, and `tabi-shokunin/scripts/*` has no href or URL-join logic.
   Boundary: `tabi-shokunin/PROVINCE.md:15-16` refuses web publishing in favour of kake, and `kake-shokunin/PROVINCE.md:32-33` gives tabi browser and crawler discipline. C2 stays offline and static. Any JavaScript-rendered or browser-resolved base check is tabi's, and is out of scope for this round.
6. **kengaku: a benchmark URL grader that loosely resembles path containment.** `kengaku-shokunin/corpus/knowledge/webarena-task-spec-audit.md:41,44-45` (S062, which is kengaku's ID) documents a WebArena grader that strips the trailing slash and uses substring containment on host plus path.
   Boundary: this is a model-evaluation grader, owned by kengaku, with nothing to reuse. It is a useful contrast only. C2's interface correctly avoids that leak because `basePath` must end in `/`, so `/repo/` does not prefix-match `/repository/`. The one special case is "equals basePath without its final slash".
7. **kama: a dead static-site preview listener.** `kama-shokunin/corpus/knowledge/consumer-registry.md:239` records that the llm-wiki `README-SITE.md:15` preview on `127.0.0.1:8766` was DEAD.
   Boundary: kama owns local endpoints, per `kake-shokunin/PROVINCE.md:39`. There is no overlap.
8. **No overlap:** kagi, kama, kengaku and kumitate `baseURL` hits (model-provider configuration). mado, tabi and lore `github.io` hits are source URLs for other topics. The kotodama "link check" hit at `binding-speech-complex.md:35` is prose. The remaining lanes have no hits.

## Reusable sources, and what the fleet lacks

- **No sibling registers any C1 page.** `docs.github.com/en/pages/...` (S040), `jekyllrb.com` (S041, S042), `vite.dev` (S043) and the WHATWG URL Standard (`url.spec.whatwg.org`) appear in no sibling `corpus/SOURCES.md`. The four C1 rows are fleet-first, so there is nothing to deduplicate.
- **Other `docs.github.com` pages are registered, but cover different topics** and cannot back C1 content: kagi S047, S048 and S050 (`kagi-shokunin/corpus/SOURCES.md:54-57`), kumitate S033 (`:46`) and souji S015 (`:35`). One precedent is worth reading: `kagi-shokunin/corpus/source-fetches.tsv:90-93` labels `docs.github.com` bodies `decoded-http-body-volatile`. This supports C1's choice to pin a retained-text digest rather than a live-body digest.
- **Kake's own rows already ground the C2 interface.** These are S024 (`<base>` element), S026 (`html.parser`), S027 (`urllib.parse`) and S029 (RFC 3986), at `kake-shokunin/corpus/SOURCES.md:32-37`. Kake's own entries `crawl-scope-per-host.md:9` (project sites under `veigapunk.github.io/<repo>/`), `ghp-subpath-spotcheck.md`, `kimi-subpath-audit.md` and `sitemap-orphan-audit.md:51` are the lane's prior base-path ground that `pages-base-path.md` should link to. tabi's S082 and S095 (WHATWG HTML input) do not apply.
- Fact as of e58b66c: `kake-shokunin/corpus/SOURCES.md` has no S040 to S043 rows yet, so C1's check a is currently unmet. That is expected before the build lands.

## Proposed move: a chousa-style token-boundary falsifier for C1 check d

Evidence: `.ufo/waves/round-29/c1_quote_truth.py:111` is `quote in text` on whitespace-collapsed text. Its only control (`:66-70`, `:113`) flips the quote's first letter, so it does not detect truncation. I ran a read-only, in-memory demo:

`git show e58b66c…:.ufo/waves/round-29/sources/S040.txt | python3 -B -c '<collapse; take an 8-word span; trim 3 characters left and 2 right>'`, exit 0.

| Quote | Words | Passes `in` (check d) | Passes token boundary |
|---|---|---|---|
| `'repository on GitHub. Copy markdown Who can use'` | 8 | True | (control) |
| `'ository on GitHub. Copy markdown Who can u'` | 8 | True | False |

A glued, mid-word quote therefore counts toward C1 today, and the flip-letter control still holds. Second finding from the same demo: the retained S040 visible text contains page chrome ("Copy markdown"), so a Gate quote can span interface text rather than documentation prose. chousa names this class `EXPORT_CHROME_PRESENT` (`research-gate.sh` header).

The move:
- Keep the declared counter frozen. Add an L1-owned falsifier, or a check d′ if the L1 chooses to amend, that requires each Gate quote's collapsed occurrence to sit at token boundaries on both edges, under the chousa r4 rule.
- Add a second control: a copy of each passing quote truncated mid-token by one character must not pass.

Affected axes:
- Freshness: C1 counts only genuine quotes.
- Operability: unchanged, because C2 is untouched.

This harms no axis, because legitimate token-aligned quotes still pass.

Risks:
- chousa fails closed on non-ASCII neighbours such as `—`, `’` and `”` (`anchor-boundaries-r4.md:74-77`). A legitimate quote that abuts an em dash in GitHub Docs text would fail. Kake should treat Unicode punctuation as a boundary, or record the case.
- Editing a declared, frozen counter mid-round is a contract change. That is the L1's call, which is why I propose a separate falsifier.
- Page-chrome spans need a judgment rule, not a regex.

Verification (not run by me):
- Once the build lands, run `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision <commit>`.
- Then run the boundary falsifier against the same Gate quotes, plus one deliberately glued fixture quote. The fixture must fail, and the real quotes must still pass, in a sandbox clone.

**Reproduced by CriticC1CounterGameable** (`.ufo/waves/round-29/w1/CriticC1CounterGameable.md`, row F9, limit 5):
- At sandbox rev a51ee4b77a8f, the glued S040 quote scores C1 4/4, exit 0, `controlBroken` false.
- A whole-word probe (chousa's word-character rule, without the hyphen and apostrophe clause) flags only that fake. The honest baseline still passes.
- The probe misses the critic's other 9 fakes, because they all start and end on whole words: navigation quotes, unrelated quotes, See-also only, fabricated text plus receipt, table-cell splice, truncated context, one-word quotes and HTML comments.

The critic's final report (eleven fakes pass C1 at 4/4, and three negative controls fail as designed) pairs this move with a second check: `.ufo/waves/round-29/sources` must be unchanged since `e58b66c`. In the critic's sandbox, that check catches both fabricated-text fakes. The other nine still need someone to review each Gate line against the claim in the entry.

So this move closes truncation and gluing only. It is necessary but not enough for an honest C1. The other fakes need checks on what a quote means and where it sits on the page, which a regex cannot do.

## Not verified

- I did not run the C1 or C2 counters.
- I did not open any URL, and did not re-run game-dev-3d's 2026-10-18 curl.
- I did not test the chousa rule on Unicode edges in S040 to S043.
- I did not read sibling `corpus/lessons/` beyond the hits quoted above.

I sent one coordination message to KakeR29.CriticC1CounterGameable about the line-111 leak.
