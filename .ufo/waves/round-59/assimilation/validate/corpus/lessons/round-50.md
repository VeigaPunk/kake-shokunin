# Round 50 lesson

author: Kimi fresh L1

## Gate

Admitted, re-opened 2026-10-24 (access date this round; campaign opened dates are not this lane's gate):

- S286 quote: "Googlebot will scale back its crawling if it detects that your servers are having trouble" URL https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors. HTTP 200, 193275 bytes. Recheck prose stripped from the staged row: curl counting `scale back its crawling`, campaign date 2026-10-23. This round's recheck cell is `180d`. The quote is a raw substring of the retained HTML and of the collapsed text.
- S286 re-opened a second time in-round by the L1 (2026-10-24, one public GET, HTTP 200, 193275 bytes): the same 15-word span is a raw substring of the freshly fetched body and still survives whitespace collapse. The retained blob's sha256 pair is pinned in `.ufo/waves/round-50/quote-classes.json`; the live body differs from the retained blob only in per-response nonce material, not in the quoted span.
- S273 quote class is collapsed-only
- S274 quote class is raw-substring
- S286 quote class is raw-substring

used-by for S286, old staged value to new: `corpus/knowledge/crawl-error-status-table.md` to the same path, and only that path. status old `mined` to new `mined`. opened old campaign `2026-10-23` to new `2026-10-24`.

Refused from the assimilation set, re-opened this round:

- `corpus/knowledge/jekyll-url-baseurl-options.md` (staged S259). Reason: its URL `https://jekyllrb.com/docs/configuration/options/` is already mined as S080. A second row is an E04 duplicate URL in scope. Flip: supersede S080 in place so the url/baseurl aspect is on the held row, with no second row for that URL.
- `corpus/knowledge/ollama-openapi-contract.md` (staged S321). Reason: the staged `source:` is `raw.githubusercontent.com/ollama/ollama/.../docs/openapi.yaml`, and the staged ground line assigns local model-serving endpoints to kama. kake `PROVINCE.md` Adjacent says the same. kama's domain is local model serving and endpoint health. Flip: the operator amends kake's province, or kama releases the surface.

Quarantine slice re-derived this round (12 rows: S142, S143, S148, S154, S156, S161, S178, S184, S193, S194, S195, S206). S286 is not in the slice. None of the 12 was hand-checked this round, and none was appended. The round-48 hand-check is not an adoption basis.

## Mistakes

- class: wave citation without a durable grant. evidence: `corpus/lessons/round-49-verifier-spotcheck.md` routed defect 1 (grant line and `kimi --prompt` lived only in the report and LOG). captured-by: none at round 49. fix: `c50_durable.py` requires `wave-grant.txt` and `dispatch-command.txt` at a strict ancestor, and LOG at that ancestor must not contain `r50-w1`. Shown able to fail: the same counter at base `9619af67c52939daac502ca7a24c9d714f3f51db` is durable 0 because the proof is absent.
- class: quote class blurred. evidence: `corpus/lessons/round-49-verifier-spotcheck.md` (S273 collapsed-only, S274 raw substring). captured-by: none (the round-49 counter checked a substring of the collapsed blob only). fix: `c50_quote_class.py` derives the class from both blobs and fails a swapped label. Shown able to fail: `.ufo/waves/round-50/verification/blur-control.txt` records swapped S286 class `collapsed-only` equals derived `False`.

## considerthese

Mined, not edited: `considerthese/2026-10-24.md` (2026-10-24), second unimplemented proposal — watch unmerged operator-save and WIP branches by tree diff, not ancestry. Opened the pointer: `remotes/origin/wip/operator-save-20261023` is `e80f84ddb84f4120cf62128c32498edc30db38bc`. `git merge-base --is-ancestor` against `master` exited 1. Tree diff against `master` is not empty: 4 lines are in that commit and not in `master` (`freshness-pins.json` updated/round keys, two `round-42.md` lines). Not merged and not deleted. Operator-owned.

## Assimilation

Theme: crawl-error status. One entry, `corpus/knowledge/crawl-error-status-table.md`, citing S286 only. S273 and S274 stay the round-49 rows; this round records their classes and does not re-append them. Collision scratch: staged ids overlapping the registry are S273 and S274 only. Guard: an indented `S286` row produced a nonempty collisions file; the column-zero pattern produced an empty file.
