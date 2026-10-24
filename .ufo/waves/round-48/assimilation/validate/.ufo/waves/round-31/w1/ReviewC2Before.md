# ReviewC2Before — C2 re-measurement and source receipt recomputation (Kake R31 W1)

## What I attacked
Re-ran the C2 counter at f1ffb81 and a16602a; recomputed every S057-S061 receipt hash from
committed bytes; regenerated visible text with the fetcher's rule; verified fetcher identity.
All work read-only in the lane; derived files in /fast/scratch/hyaku/kake-r31/w1/ReviewC2Before/.
No installs were needed; no tool was installed or updated.

## Commands and exit codes
1. `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin <sandbox>/clone` → 0; clone HEAD = a16602a (log: a16602a, f1ffb81).
2. `python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision f1ffb81738c92c0537b99b30970143ab9419f990` (cwd=lane) → **exit 1**, stderr `C2 0/4 at f1ffb81…`; stdout = out-f1ffb81.json.
3. Same at a16602a961da5d6e75cfa09a1118a416ad01225b → **exit 1**, stderr `C2 0/4 at a16602a…`; stdout = out-a16602a.json.
4. `diff out-f1ffb81.json .ufo/waves/round-31/verification/c2-before-f1ffb81.json` → 0, **byte-identical** (including counterSha256 de48d460aad8645fc59e70792577d4f5a5ceb0032417f021d186e7cc6e0c31b8, equal in both my runs, the recorded receipt, and `git show a16602a:.ufo/waves/round-31/c2_quote_truth.py | sha256sum`).
5. `git show a16602a:corpus/knowledge/render-web-services.md` → **exit 128, path does not exist**; also absent from the lane working copy.
6. `git show a16602a:corpus/lessons/round-31.md` → **exit 128, path does not exist**; also absent from the working copy.
7. `git show a16602a:corpus/SOURCES.md` → 0; no `| S057 |`-`| S060 |` rows: table ends at S056 (SOURCES-a16602a.md:63-64, blank 65, `## Paths` 66). Working-copy corpus/SOURCES.md is identical there — no new rows anywhere.
8. Sandbox verifier (verify_receipts.py, reads lane bytes + `git show a16602a:…` only) → **ALL_OK, exit 0**, 5/5 sources, all 11 checks True per id.

## Receipt recomputation (all recompute == receipts.json; working copy == a16602a blob for every file)
| id | bodySha256 (recomputed == receipt) | bodyBytes | textSha256 (recomputed == receipt) | textWords | visible_text(body)==txt |
|----|-----------------------------------|-----------|-------------------------------------|-----------|-------------------------|
| S057 | 650ed15d50189ac85dd766cc0a1dd735b4f42fb052bd5ac4c522e7fb2690aab0 | 1432786 | ca8179f2098b142d5040c17763ecf205f630342d0d01a6a386a1f10e9848e51a | 8223/8223 | True |
| S058 | eaa1f028e43ac32535787c934d32fc8a21f0661193648ff101b014af63c04576 | 490595 | 983a792dc65dbbe95bf3437f1b02bfa88c4a6f009282486480f786b45aee8aee | 1817/1817 | True |
| S059 | d3ce93a75d2999af63ecdc53bfe9aac39b4ec4c78299650bcf039c403d3b8f08 | 327582 | f8e60da01b3087b31fbea6596f796746815c1ee28c735221d3c26f5d96b48618 | 1301/1301 | True |
| S060 | 70954862f322531389133c1dea2b571864abccd3533bff81cfca44939d444951 | 458065 | 1f934877247b6d636683b124da72385af8afa6ef4644ccb72e15aa2b3e065d7b | 1018/1018 | True |
| S061 | bb75fe4b0ffd65af2ee3e3f456d1cc97578ff0afadbfe0d540827de5b1a91d86 | 292139 | aa904927cf6cce3782594518c859dda5c88167e1b84ca674874acfe9c47c0c3d | 899/899 | True |

visible_text was copied verbatim from the committed fetcher (block extracted and compared
line-identical); regenerated text (incl. trailing `\n`) is byte-equal to each committed .txt.
fetcherSha256 bc66ceb0d136eab0f134dca60c3a614ee4fdb9e4090ab6242605364e079242c9 equals the
working-copy fetcher AND the a16602a committed blob; receipts.json working copy == committed blob;
all statuses 200; finalUrl == url for all five.

## Findings (severity order)
1. **HIGH (build-stage gap, C2 not yet distinguishable from base):** the counter reports 0/4 at
   BOTH revisions. At the declared claims commit a16602a none of the three integration artifacts
   exists: no SOURCES.md rows for S057-S060 (check a), no corpus/knowledge/render-web-services.md
   (check b, exit 128), no corpus/lessons/round-31.md Gate quotes (check c, exit 128); none exist
   in the working copy either. Only check d's hash precondition holds (txt sha == receipt, my
   table). So at a16602a the C2 falsifier cannot separate candidate from base; if the round closed
   here, C2 would fail its own counter. Advisory to L1: the entry file, the four registry rows
   (counter expects `mined` in cell 8, `2026-10-22` in cell 9, URL in cell 2, ≥11 cells), and the
   round-31 Gate quotes (6-25 words, curly quotes, `- S057 — ` format) are still to be landed.
2. **Green (freshness half of C2):** source opening and retention are internally sound — every
   body/text/word count and the fetcher identity recompute exactly from committed bytes (5/5,
   verifier exit 0). Receipt timing matches the declared 15:41:23Z-15:41:29Z one-GET-each window.
3. **INFO:** the before receipt is exactly reproducible (byte-identical rerun), and the counter
   script itself is unchanged f1ffb81→a16602a→working copy (de48d460…).

## Residual risk and verification gaps
- Hash recomputation proves internal consistency only; it cannot prove the bodies really came
  from render.com (no live refetch performed by me; owned-site bounds and scope kept me to
  committed bytes). The ReopenSources seat covers the live side.
- The 6-25-word control branch (control_broken) was never exercised: no id passed, so the
  counter's control is vacuously green at both revisions.
- I did not verify quote truth against page semantics, SCORECARD.md, or publish-channels.md —
  outside this slice.
- Working-copy state may move under the L1's integration; findings 1 reflect snapshot at review
  time (revisions a16602a and lane working copy, 2026-10-22).

## Artifacts (sandbox)
/fast/scratch/hyaku/kake-r31/w1/ReviewC2Before/: clone/ (lane clone at a16602a),
out-f1ffb81.json, out-a16602a.json, err-*.txt, SOURCES-a16602a.md, verify_receipts.py.
