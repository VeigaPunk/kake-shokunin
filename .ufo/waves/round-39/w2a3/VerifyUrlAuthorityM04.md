# VerifyUrlAuthorityM04 — MutUrlAuthority M04 (sentence 22)

verdict: **valid control** — M04 breaks contract sentence 22 on the witness; the reference obeys it.

## Receipt (allowed fields only)
`.ufo/waves/round-39/verification/a3/w1a3-MutUrlAuthority__M04.json`:
`label=w1a3-MutUrlAuthority__M04`, `passed=24`, `met=true`,
`toolSha256=d2fd1f2f063c8482d83164172e763a71b1c0e07b30964d3fe78b5a019995b0f2`
(matches on-disk M04.py sha256). `rows`/`why` never read.

## Diff — exactly one change
`diff -u shared/reference.py MutUrlAuthority/mutants/M04.py` → diff exit 1:
reference.py:170 `if a is None:` → M04.py:170 `if a is None or "@" in urlsplit(v).netloc:`.
mutants.json:371–375 records the identical single-line mutation ("changed_line_count": 1).
sha256: reference.py `663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8`;
M04.py `d2fd1f2f063c8482d83164172e763a71b1c0e07b30964d3fe78b5a019995b0f2` (= receipt).

## Witness (matches mutants.json:389,392)
manifest.json sha256 `640811f4…2081`; sitemap.xml sha256 `b9ebb47c…c464`.
sitemap.xml body: `<urlset …><url><loc>https://u@example.test/a</loc></url></urlset>`;
check sitemapUrl `https://example.test/s.xml`.

## Runs (`prlimit --as=4000000000 -- timeout 60 python3 -B <tool> --manifest witnesses/M04/manifest.json`)
reference.py, exit 0:
`{"version": 1, "verdict": "clean", "checks": [{"id": "w", "status": "clean", "error": null, "findings": []}]}`
M04.py, exit 1:
`{"version": 1, "verdict": "failed-policy", "checks": [{"id": "w", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}`

## Contract check (c1-contract.md alone)
Sentence 22: "A `loc` must be an absolute URL whose scheme is `http` or `https`
(case-insensitive) and whose host is non-empty; otherwise `loc_not_absolute`, and
rule (h) is skipped for that entry."
`https://u@example.test/a` is absolute; scheme `https`; host `example.test` non-empty —
`u` is userinfo inside the authority component, not part of the host. No sentence in the
contract forbids userinfo. Sentences 24–25 (scope): scheme/host match, missing port = 443
both sides, path `/a` starts with sitemapUrl directory `/` → in scope. So the contract
determines clean output here; reference produces it, mutant emits `loc_not_absolute`.

## Attacked statement
mutants.json:368 `contract_sentences: [22]` / :370 "Reject an absolute loc containing
userinfo" — **holds**: the mutant adds a rejection sentence 22 does not license.

## Notes / gaps
- Kill rule (1) (witness divergence) fired correctly; seat verdict "killed" (mutants.json) reproduced.
- Residual risk: the sealed key scored M04 24/24, so the key itself has no userinfo-loc
  case covering this sentence-22 sub-rule — a key-sensitivity gap, not a witness defect.
- No `lsp` device exists in this session's tool inventory; verdict rests on the diff and
  two executed runs, not on grep. No tools installed. No forbidden paths read.
