# RowS052 — C2 frontier step: SOURCES.md row and lesson Gate line for S052

Lane: /home/vgpnk/Projects/shokunin/kake-shokunin
Round: 30 (kake-r30), wave 1, seat RowS052
Scope: draft only. No lane file was edited; the L1 integrates.
Artifacts: /fast/scratch/hyaku/kake-r30/w1/RowS052/row.md (sha256 0823ce896b77b89c7ffeaa030df7a8a8f8d0c52145573cf3182c33e874b5ac5d)
and /fast/scratch/hyaku/kake-r30/w1/RowS052/check_quote.py (sha256 recorded below).

## What I built

One SOURCES.md registry row for S052 (Render Docs: Custom Domains) and one lesson Gate line, both drafted
from the retained text of the source the L1 opened at 2026-10-22T11:49:45Z with HTTP 200.

Inputs read (read-only):
- .ufo/waves/round-30/sources/S052.txt (textSha256 6c1616f8…58f769, 1488 words, one line)
- .ufo/waves/round-30/sources/receipts.json key S052 (url/finalUrl https://render.com/docs/custom-domains,
  status 200, accessedUtc 2026-10-22T11:49:45Z, bodySha256 59469467…94e543, bodyBytes 371923)
- corpus/SOURCES.md rows S040-S043 as the model (header at corpus/SOURCES.md:7), S048 as today's last row
- .ufo/waves/round-30/c2_quote_truth.py, the counter that will read this row

## The row (append after S048, inside the Registry table)

| S052 | Render Docs: Custom Domains — https://render.com/docs/custom-domains | docs | A | Render's own custom-domain handling for web services and static sites, as its vendor documents it; not a general DNS, TLS or hosting standard, and not a statement about any other host | Custom Domains on Render page: the opening paragraph and the 1. Add your domain in the Render Dashboard step; page fetched 2026-10-22 | Render attaches a custom domain to a web service or a static site, issues and renews its TLS certificate automatically, redirects all HTTP on that domain to HTTPS, and keeps the onrender.com subdomain unless it is disabled | mined | 2026-10-22 | 90d | corpus/knowledge/render-static-sites.md |

Cell map (columns from corpus/SOURCES.md:7): id `S052`; source `Render Docs: Custom Domains —
https://render.com/docs/custom-domains`; kind `docs`; tier `A`; scope narrow and Render-side; anchor
`Custom Domains on Render page: the opening paragraph and the 1. Add your domain in the Render Dashboard step`;
teaches as above; status `mined`; opened `2026-10-22`; recheck `90d`; used-by
`corpus/knowledge/render-static-sites.md`. Eleven cells, matching the header count.

## The Gate line (corpus/lessons/round-30.md, inside `## Gate`)

- S052 — https://render.com/docs/custom-domains — accessed 2026-10-22, HTTP 200 — mined: Render attaches a custom domain to a web service or a static site, issues and renews TLS for it automatically, redirects HTTP on it to HTTPS, and keeps the onrender.com subdomain unless that subdomain is disabled ; quote “You can apply your own custom domains to Render web services and static sites . Services with a custom domain also keep their onrender.com subdomain.”

## Quote check

Quote: `You can apply your own custom domains to Render web services and static sites . Services with a custom domain also keep their onrender.com subdomain.`

Word count: 25 by whitespace split, 25 by a `\w+` tokenizer. The counter allows 1 to 25 inclusive
(`1 <= len(quote.split()) <= 25` at .ufo/waves/round-30/c2_quote_truth.py), so the quote sits at the ceiling.

Command (also saved as /fast/scratch/hyaku/kake-r30/w1/RowS052/check_quote.py):

    python3 - <<'PY'
    import re,hashlib,json
    base='/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/sources/'
    raw=open(base+'S052.txt','rb').read()
    rec=json.load(open(base+'receipts.json'))['S052']
    text=re.sub(r'\s+',' ',raw.decode('utf-8','replace')).strip()
    gate='- S052 — https://render.com/docs/custom-domains — accessed 2026-10-22, HTTP 200 — mined: Render attaches a custom domain to a web service or a static site, issues and renews TLS for it automatically, redirects HTTP on it to HTTPS, and keeps the onrender.com subdomain unless that subdomain is disabled ; quote “You can apply your own custom domains to Render web services and static sites . Services with a custom domain also keep their onrender.com subdomain.”'
    QUOTE=re.compile(r"“([^“”]+)”")
    q=QUOTE.findall(gate)
    quote=re.sub(r'\s+',' ',q[0]).strip() if len(q)==1 else None
    print('n_quotes', len(q))
    print('words', len(quote.split()))
    print('words_regex', len(re.findall(r"\w+", quote)))
    print('sha_ok', hashlib.sha256(raw).hexdigest()==rec.get('textSha256'))
    print('substring', quote in text)
    i=text.find(quote)
    print('offset', i)
    print('context', text[max(0,i-70):i+len(quote)+70])
    PY

Observed output (exit code 0):

    n_quotes 1
    words 25
    words_regex 25
    sha_ok True
    substring True
    offset 2708
    context  Heroku vs Render Vercel vs Render Custom Domains on Render Copy page You can apply your own custom domains to Render web services and static sites . Services with a custom domain also keep their onrender.com subdomain. Your workspace includes an amount of custom domains based on its plan

The quote sits at offset 2708 of the collapsed retained text, right after the page title
`Custom Domains on Render Copy page`, in the opening paragraph.

## Findings for the L1

- The quote keeps the tag-removal artifact the round-29 lesson already documents for S040 and S043: a space
  before the first period (`static sites .`), because the fetcher replaces each tag with one space before
  collapsing whitespace. It is an exact substring of the retained text under the receipt's stated textRule.
- The quote is exactly at the 25-word ceiling. A shorter exact-substring alternative is
  `Only web services and static sites support custom domains.` (9 words) from the
  `1. Add your domain in the Render Dashboard` step; it carries the service-kind scoping but not the
  onrender.com subdomain fact. Use it only if a stricter budget is wanted.
- The teaches cell rests on four statements present in the retained text: custom domains apply to web services
  and static sites; TLS certificates are created and renewed automatically; HTTP on a custom domain redirects
  to HTTPS; the onrender.com subdomain is kept unless disabled. The scope cell is deliberately narrow —
  Render's own vendor documentation, not a DNS/TLS standard and not a statement about GitHub Pages.
- Not present in the lane tree yet: corpus/lessons/round-30.md and corpus/knowledge/render-static-sites.md. The
  L1 must create both, insert the row, place the Gate line under `## Gate`, and cite `S052` in the knowledge
  entry body (the counter reads that file from line 9 onward for `b_entry_body_cites`).
- The used-by cell names only corpus/knowledge/render-static-sites.md, as the assignment instructed.

## Out of scope / not verified

- I did not run the C2 counter at any revision: the row, the lesson file and the knowledge entry do not exist
  in the lane tree yet, so the counter would read 0 for reasons that have nothing to do with this draft.
  My checks reproduce the counter's own gate logic on the same retained bytes and receipt.
- I did not fetch any URL. The page was opened by the L1 at 2026-10-22T11:49:45Z and I worked from the
  retained body and text only.
- No tool was installed or upgraded this seat, so there is no install to record.
- Nothing in the lane repository was mutated; this report file is the only file I wrote there.
