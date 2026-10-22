# RowS050 — C2 frontier step: SOURCES.md row and lesson Gate line for S050

Round 30, wave 1, seat RowS050 (scribe). Lane: /home/vgpnk/Projects/shokunin/kake-shokunin. Scope: draft only; nothing landed in the lane and no live request of any kind was made.

## What I built

1. A `corpus/SOURCES.md` registry row (11 cells, to be appended after the S048 row).
2. The `corpus/lessons/round-30.md` Gate line, in the exact required form.
3. Deliverable file: `/fast/scratch/hyaku/kake-r30/w1/RowS050/row.md`.

## The row (draft text)

| S050 | Render Docs: Redirects and Rewrites — https://render.com/docs/redirects-rewrites | docs | A | Render static-site redirect and rewrite rule matching only; not a statement about GitHub Pages or any other hosting host | Static Site Redirects and Rewrites, opening paragraph and the Rule matching and ordering section (full path-matching process); Render Docs page opened 2026-10-22T11:49:44Z, HTTP 200, retained text sha256 1c413643…52c5ed | A Render static site serves a resource that already exists at the requested path and applies no redirect or rewrite rule there, so a rule decides the response only where no resource exists | mined | 2026-10-22 | 90d | corpus/knowledge/render-static-sites.md |

Cells match the header at `corpus/SOURCES.md:7`: status `mined`, opened `2026-10-22`, recheck `90d`, used-by `corpus/knowledge/render-static-sites.md`, receipt URL in the source cell. No cell contains a pipe.

## The Gate line (draft, inside `## Gate` of `corpus/lessons/round-30.md`)

- S050 — https://render.com/docs/redirects-rewrites — accessed 2026-10-22, HTTP 200 — mined: Render's own documentation fixes how a static site resolves a path that already has a resource against a redirect or rewrite rule; quote “Render does not apply redirect or rewrite rules to a path if a resource exists at that path.”

The quote is 18 words (limit 25); the line carries exactly one curly-quoted segment and starts with `- S050 — `.

## Commands run and observed output

1. Substring and word-count check, run from the lane root (`exit 0`):

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 - <<'PY'
import re
raw=open('.ufo/waves/round-30/sources/S050.txt',encoding='utf-8').read()
text=re.sub(r'\s+',' ',raw).strip()
q="Render does not apply redirect or rewrite rules to a path if a resource exists at that path."
print('words:',len(q.split()))
print('substring:',q in text)
flip=q[:0]+('q' if q[0].lower()!='q' else 'z')+q[1:]
print('flipped control substring:',flip in text)
PY
```

   Output: `words: 18`, `substring: True`, `flipped control substring: False`. The flipped string `qender does not apply redirect or rewrite rules to a path if a resource exists at that path.` is absent from the retained text, so the counter's letter-flip control stays green.

2. End-to-end simulation of the round-30 C2 counter in the sandbox clone `/fast/scratch/hyaku/kake-r30/w1/RowS050/clone` (cloned from the lane repo at `4580c78`; the draft row, a `## Gate` stub and a stub knowledge entry were applied and committed there as `f4dda99`, inside the sandbox only):

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/c2_quote_truth.py \
  --root /fast/scratch/hyaku/kake-r30/w1/RowS050/clone --revision HEAD
```

   Exit 1. Output: `passed 1`, `total 4`, `controlBroken false`; the S050 entry is `"passed": true` with `a_row`, `b_entry_body_cites`, `c_gate_quote`, `d_quote_in_retained_text` all true and the extracted quote equal to the line above. The exit 1 comes only from S049, S051 and S052, sibling seats' surfaces not part of the simulation.

3. Reads and greps only, no side effects: `git clone -q` of the lane repo into the sandbox, `git log --oneline -1` (`4580c78`), `git status --porcelain` (lane working tree unchanged apart from this report and other seats' untracked wave files), `sha256sum`, `wc`, `cat` of the retained text.

## Gates and evidence

- Receipt `.ufo/waves/round-30/sources/receipts.json` key `S050`: url and finalUrl `https://render.com/docs/redirects-rewrites`, status 200, accessedUtc `2026-10-22T11:49:44Z`, bodyBytes 348130, bodySha256 `a57b515f120fbc71865406d9a14b3438f01d74efa640c22e441303a8135c580e`, textSha256 `1c41364393defcba006be8ad33a1b34882ef455013032135a3daf0b43d52c5ed`, textWords 854.
- Retained text `.ufo/waves/round-30/sources/S050.txt`, 5830 bytes; sha256 of the file on disk equals the receipt `textSha256` (checked, True).
- The quote comes from the article body's "Rule matching and ordering" passage; the retained text opens with the site navigation menu, so a quote from the top of the file would be meaningless.
- Form models: `corpus/SOURCES.md:7` header and rows S040-S043 (`corpus/SOURCES.md:40-43`); lesson Gate model `corpus/lessons/round-29.md:36-39`; counter rules `.ufo/waves/round-30/c2_quote_truth.py:15-25,96-118`.

## Touched surfaces and bounds

- Lane: only `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/w1/RowS050.md` (this report).
- Sandbox: only `/fast/scratch/hyaku/kake-r30/w1/RowS050/row.md` and the simulation clone.
- No edit to `corpus/SOURCES.md`, `corpus/lessons/round-30.md` or `corpus/knowledge/render-static-sites.md`; no mutating Git or jj command in the lane; no network request of any kind; no owned property contacted; no subagent dispatched.

## Out of scope and not verified

- Landing the row and the Gate line (the L1 integrates), and creating `corpus/knowledge/render-static-sites.md` and `corpus/lessons/round-30.md`; both files are absent from the lane working tree, so the C2 counter cannot pass until the L1 creates them and cites S050 by word in the knowledge body.
- The counter was never run against the lane repo itself: the base commit has no committed S050 row and neither of those two files.
- Rows and Gate lines for S049, S051 and S052 (sibling seats) were not simulated or verified here.
- No Render property was fetched, deployed or rendered, so no live behaviour is claimed.

## Findings for the L1

1. The C2 counter needs three surfaces at one revision: the registry row, the knowledge-entry citation and the lesson Gate line. Two of the three files do not exist yet in the lane.
2. The Gate line must be the only line in `## Gate` starting with `- S050 — ` and must carry exactly one curly-quoted span, because the counter takes the first matching line and requires one match of `“([^“”]+)”`.
3. The used-by cell names only `corpus/knowledge/render-static-sites.md`, as instructed. Rows S040-S043 also list the round lesson file; if the corpus convention requires that, add `corpus/lessons/round-30.md`.
4. The teaches cell asserts rule precedence over an existing resource; the quote carries that directly and the anchor names the section that carries it.
5. Alternate true substrings of the same retained text, if a different teaching is preferred: `Instructs the browser (or any other client) to switch URLs to the rule's destination via a 301 Moved Permanently response code.` (21 words); `You can't apply redirect/rewrite rules to your domain root.` (9 words); `Rewrite Does not redirect the browser. Instead, your site serves the content from the rule's destination at the original path.` (20 words).
6. Scope note: the page is one hosting vendor's own documentation. It supports statements about Render static sites only and says nothing about GitHub Pages.

## Artifacts

- `/fast/scratch/hyaku/kake-r30/w1/RowS050/row.md` (draft row, Gate line, check command, output)
- `/fast/scratch/hyaku/kake-r30/w1/RowS050/clone` (simulation clone, commit `f4dda99`)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/w1/RowS050.md` (this report)

Tooling: none installed or upgraded this seat; only python3 standard library and git were used.
