# KakeR31a2.ReopenS057S058 — independent re-open of S057 and S058 (C2 freshness)

Seat: KakeR31a2.ReopenS057S058 (leaf reviewer, wave 2 falsify). Review commit fde133ab48086bb9a06911b4ab045e2ad9086347 (clone verified via `git rev-parse HEAD`).

## What I attacked
C2's grounding for S057 and S058: whether the declared fetch receipts
(`.ufo/waves/round-31/sources/receipts.json`) describe real page state and
whether the Gate quotes in `corpus/lessons/round-31.md:42-43` are actually
present on the live pages ~2.4 h after the declared open (15:41Z) — i.e.
whether the receipts were fabricated, the quotes invented, or the pages changed.

## Method
- Sandbox: /fast/scratch/hyaku/kake-r31/a2-w2/ReopenS057S058/ (clone + probe + artifacts there only).
- Probe `/fast/scratch/hyaku/kake-r31/a2-w2/ReopenS057S058/reopen_s057_s058.py`
  copies `visible_text` verbatim from `.ufo/waves/round-31/fetch_sources.py` and
  issues exactly one `urllib` GET per URL, UA `kake-shokunin-round-31-falsify-reopen`,
  no redirects observed (finalUrl == requested URL both times).
- Gate quotes taken from corpus/lessons/round-31.md lines 42-43 (S057 quote
  includes the literal space before the period, `sync: false .`, matching the
  fetcher's tag-removal rule).

## Commands run (all exit 0)
1. `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin .../clone && git checkout -q fde133a…` → HEAD `fde133ab48086bb9a06911b4ab045e2ad9086347`.
2. `sha256sum clone/.ufo/waves/round-31/fetch_sources.py …/S057.txt …/S058.txt`:
   - fetcher `bc66ceb0d136eab0f134dca60c3a614ee4fdb9e4090ab6242605364e079242c9` == receipts `fetcherSha256` ✔
   - S057.txt `ca8179f2098b142d5040c17763ecf205f630342d0d01a6a386a1f10e9848e51a` == receipts `textSha256` ✔
   - S058.txt `983a792dc65dbbe95bf3437f1b02bfa88c4a6f009282486480f786b45aee8aee` == receipts `textSha256` ✔
3. `TMPDIR=…/tmp python3 -B reopen_s057_s058.py` → output below; artifacts and
   `reopen_results.json` in the sandbox.

## Re-open results (2026-10-22T18:06:16Z / 18:06:18Z)
| id | status | live textSha256 | equals receipt | quote in live text |
|----|--------|-----------------|----------------|--------------------|
| S057 | 200 | `ca8179f2098b142d5040c17763ecf205f630342d0d01a6a386a1f10e9848e51a` | YES | YES |
| S058 | 200 | `983a792dc65dbbe95bf3437f1b02bfa88c4a6f009282486480f786b45aee8aee` | YES | YES |

- Both quotes present verbatim in the live visible text and in the retained
  `.txt` copies.
- Raw body sha256 differs (S057 `8d84e8fe…` vs receipt `650ed15d…`, 43 bytes
  shorter; S058 `c074e5ef…` vs `eaa1f028…`, same length). Characterized: all
  divergences sit inside HTML tags — `data-dpl-id`/`?dpl=` deployment ids
  (`6f79ff4995` → `566dc9cb5f`) and hashed `_next/static` chunk names
  (e.g. `2q95x6ydqperz.css` → `3j5-hzy2aw5sp.css`), i.e. a Vercel redeploy
  rotated asset fingerprints between 15:41Z and 18:06Z. Visible text is
  byte-identical, so no doc-content drift.

## Finding
No falsification found on this target. Receipts are self-consistent with the
retained artifacts; the independent re-open reproduces both `textSha256`
values exactly and both Gate quotes are verifiably on the live pages.
Residual risk: this check covers only S057/S058 visible text + the two quotes;
the other mined claims in `render-web-services.md` and S059–S061 were not
re-verified by this seat (out of target scope).

## Not verified / out of scope
- S059, S060, S061; knowledge-file factual accuracy beyond quote presence.
- Whether the 15:41Z open actually used the declared fetcher (only the
  fetcher/artifact/receipt consistency was confirmed).

No tool installs needed (pacman paused; stdlib only). Sandbox artifacts:
reopen_s057_s058.py, reopen_results.json, artifacts/{S057,S058}{,.retained}.{html,txt}.
Report: .ufo/waves/round-31/a2-w2/ReopenS057S058.md
