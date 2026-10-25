# Round 49 lesson

author: kake L1 (Kimi fresh L1)

## Gate

Admitted, re-opened 2026-10-24 (access date this round; campaign opened dates are not this lane's gate):

- S273 quote: "Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit." URL https://developers.google.com/crawling/docs/crawl-budget. Recheck prose stripped from the staged row: curl of that URL counting the shift sentence, campaign date 2026-10-23. This round's recheck cell is `180d`.
- S274 quote: "It reduces your site's crawl rate across the whole hostname" URL https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate. Recheck prose stripped from the staged row: curl counting `across the whole hostname`, campaign date 2026-10-23. This round's recheck cell is `180d`.

used-by for both rows, old staged value to new: `corpus/knowledge/crawl-budget-consequences.md` to the same path, and only that path. status old `mined` to new `mined`. opened old campaign `2026-10-23` to new `2026-10-24`.

Refused from the assimilation set:

- `corpus/knowledge/jekyll-url-baseurl-options.md` (staged S259). Reason: its URL `https://jekyllrb.com/docs/configuration/options/` is already mined as S080. A second row is an E04 duplicate URL in scope. Flip: supersede S080 in place so the url/baseurl aspect is on the held row, with no second row for that URL.
- `corpus/knowledge/ollama-openapi-contract.md` (staged S321). Reason: local model-serving API contracts are kama's province (`PROVINCE.md` Adjacent; staged `source:` is `raw.githubusercontent.com/ollama/ollama/.../docs/openapi.yaml`). Flip: the operator amends kake's province, or kama releases the surface.

Quarantine slice re-derived (12 rows: S142, S143, S148, S154, S156, S161, S178, S184, S193, S194, S195, S206). None is in the adopt set. This round did not re-fetch them; the round-48 hand-check stands as historical and is not re-verified here. No quarantined id was appended.

## Mistakes

- class: validate-before-append not re-derivable. evidence: `corpus/lessons/round-48-verifier-spotcheck.md` routed defect 1 (committed mirror byte-identical to the post-append registry). captured-by: none (tip census still exited 0). fix: a pre-append mirror and its `--file` census stdout are committed at a revision that is a strict ancestor of the append, and `c49_order.py` reads only `git show`. Shown able to fail: the same counter at base `090ce8f1` is order 0 because the proof is absent.
- class: quote counter reads worktree bytes. evidence: `corpus/lessons/round-48-verifier-spotcheck.md` routed defect 2; `c48_quote_truth.py` R4 `open(path)`. captured-by: none at round 48. fix: `c49_quote_truth.py` R4 is `git show <revision>:.ufo/waves/round-49/sources/<textPath>` and the source contains `COMMITTED_BYTES_ONLY` and no `os.path.join(root`. Shown able to fail: at base the retained blobs are absent, so both ids fail R4.

## considerthese

Mined, not edited: `considerthese/2026-10-24.md` (2026-10-24), first unimplemented proposal — track open residual-attack findings against each admitted tool so admission does not close them. Opened the pointer: `.ufo/waves/round-46/residual/CriticCitationOverreach.md` still exists, uncommitted, orchestrator-owned. Round 48 closed that file's Finding 1 (full-40 existence). This round does not claim the other residual findings closed. Criterion appended to `corpus/QUALITY.md`. The eight residual reports stay uncommitted and untouched.
