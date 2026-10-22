# RowS049 — C2 frontier step: SOURCES.md row and lesson Gate line for S049

Round 30, wave 1, seat RowS049. Lane: /home/vgpnk/Projects/shokunin/kake-shokunin.
Scope: draft only. Nothing landed in the lane; no live request was made this seat.

## What I built

1. A `corpus/SOURCES.md` registry row (11 cells, to be appended after the S048 row).
2. The `corpus/lessons/round-30.md` Gate line, in the exact required form.

## The row (draft text)

| S049 | Render Docs: Static Sites — https://render.com/docs/static-sites | docs | A | Render's own static-site service semantics as its vendor documents them: per-push rebuild, atomic deploy and CDN cache invalidation; not a statement about GitHub Pages or any other host | Features, Immediate cache invalidation section (page sections Get started, Global CDN, Custom domains); Render Docs Static Sites page, fetched 2026-10-22 | Render rebuilds and redeploys the static site on every push to the deployed branch, each build is fully atomic, and the CDN cache is invalidated right after a successful deploy | mined | 2026-10-22 | 90d | corpus/knowledge/render-static-sites.md |

Cells match the header at corpus/SOURCES.md:7: status `mined`, opened `2026-10-22`, recheck `90d`, used-by
`corpus/knowledge/render-static-sites.md`, and the receipt URL appears in the source cell.

## The Gate line (draft, inside `## Gate` of corpus/lessons/round-30.md)

- S049 — https://render.com/docs/static-sites — accessed 2026-10-22, HTTP 200 — mined: Render rebuilds and atomically deploys a static site on every push to the deployed branch, then invalidates its CDN caches ; quote “We build your site with every push to your deployed branch, and each build is fully atomic.”

Quote `We build your site with every push to your deployed branch, and each build is fully atomic.` is 17 words
(limit 25); the line carries one curly-quoted segment and starts with `- S049 — `.

## Commands run and observed output

1. Substring and word-count check, run from the lane root:

       cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 - <<'PY'
       import re,hashlib,json
       p='/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/sources/S049.txt'
       raw=open(p,'rb').read()
       rec=json.load(open('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/sources/receipts.json'))['S049']
       text=re.sub(r'\s+',' ',raw.decode('utf-8','replace')).strip()
       print('sha_ok', hashlib.sha256(raw).hexdigest()==rec['textSha256'])
       q="We build your site with every push to your deployed branch, and each build is fully atomic."
       print('words', len(q.split()))
       print('substring', q in text)
       i=text.find(q)
       print('ctx', text[i-120:i+len(q)+60])
       PY

   Exit 0. Output: `sha_ok True`, `words 17`, `substring True`, and context
   `... Immediate cache invalidation Render insulates your site against failure with zero-downtime deploys . We build your site with every push to your deployed branch, and each build is fully atomic. As soon as a build succeeds, we deploy it and immediately i`

2. Draft-shape check on /fast/scratch/hyaku/kake-r30/w1/RowS049/row.md (Gate-line prefix, quote-segment count,
   word count, row cell count, URL in source cell): exit 0. Output `gate_lines_found 1`, `starts_ok True`,
   `quote_segments 1`, `words 17`, `sha_ok True`, `quote_in_text True`,
   `cells 11 mined 2026-10-22 90d corpus/knowledge/render-static-sites.md`, `url_in_source_cell True`.

3. Baseline of the declared C2 counter (read-only, no lane mutation):

       cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B .ufo/waves/round-30/c2_quote_truth.py --root . --revision HEAD

   Exit 1. Output: `revision 4580c78cca1185d059efa6970722bbcf2f9c1b0f`, `passed 0`, `total 4`,
   `controlBroken false`, `C2 0/4 at 4580c78cca1185d059efa6970722bbcf2f9c1b0f`. This matches the declared
   before state; it is a baseline only, not a measurement of the drafts.

## Gates and evidence

- Receipt: .ufo/waves/round-30/sources/receipts.json key S049 — url and finalUrl
  `https://render.com/docs/static-sites`, status 200, accessedUtc 2026-10-22T11:49:44Z, textSha256
  `3604f8f55e5ef2a9ada6eb8685e0ff1029bffc6ac304c2aa9ecf0fba0253d6f7`, textWords 983.
- Retained text: .ufo/waves/round-30/sources/S049.txt (one line, 6700 bytes); its sha256 equals the receipt
  textSha256 (checked, True).
- The quote comes from the `Immediate cache invalidation` feature section; the neighbouring retained sentence
  carries the per-push rebuild and the cache invalidation that the teaches cell asserts.
- Form models: corpus/SOURCES.md rows S040-S043 (raw lines 48-51); lesson Gate model corpus/lessons/round-29.md:36-39.
## Touched surfaces

- Lane: only /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/w1/RowS049.md (this report).
- Sandbox: only /fast/scratch/hyaku/kake-r30/w1/RowS049/row.md (draft row, Gate line, check command, output).
- No edit to corpus/SOURCES.md, corpus/lessons/round-30.md or corpus/knowledge/render-static-sites.md; no Git
  or jj command in the lane; no network request of any kind.

## Out of scope

- Landing the row and Gate line (L1 integrates).
- Creating corpus/knowledge/render-static-sites.md and corpus/lessons/round-30.md; both are absent from the
  lane working tree, so the C2 counter cannot pass until the L1 creates them and cites S049 by word in the
  knowledge body.
- Rows and Gate lines for S050, S051, S052 (sibling seats).

## Findings for the L1

1. The C2 counter needs three surfaces at one revision: the registry row, the knowledge-entry citation and the
   lesson Gate line. Two of the three files do not exist yet.
2. The used-by cell names only `corpus/knowledge/render-static-sites.md`, as instructed. Rows S040-S043 also
   list the round lesson file; if the corpus convention requires that, add `corpus/lessons/round-30.md`.
3. The teaches cell asserts cache invalidation, which the quote alone does not carry; the next sentence in
   the same section does, and the anchor names that section. If the L1 wants a teaches cell quotable on its
   own, keep only the rebuild and atomic-build half.

## Artifacts

- /fast/scratch/hyaku/kake-r30/w1/RowS049/row.md
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/w1/RowS049.md (this report)

Tooling: none installed or upgraded this seat; no install was needed.
