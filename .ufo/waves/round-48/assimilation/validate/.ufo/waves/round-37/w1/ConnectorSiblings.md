# Connector — sibling-overlap scan, round 37 wave 1

Scope: read-only scan of the 21 `*-shokunin` lanes for robots.txt/crawler rules, selftest-mutation and sealed-counter tooling, against the round-37 declarations at `4b089da` (C1 contract read from `git show 4b089da:SCORECARD.md`, Round 37). No network, no installs, no lane write except this report; the sealed tree `/fast/scratch/hyaku/kake-r37/` was not touched, listed or searched.

## Overlap table

| Lane | Evidence | Owns / touches | Disposition |
|---|---|---|---|
| tabi | `corpus/adjacency.tsv:6` = kake@`7c61c8c`:PROVINCE.md:30, `split-declared`; `SKILL.md:327-329`; `corpus/knowledge/external-class-fixture-v2.md:53,86-90`; `corpus/evidence/w6-tabi-b61/site-a/robots.txt` | Client-side crawler discipline: first request `/robots.txt`, a matching `Disallow:` prefix is never issued; its matcher is a 4-line prefix scan inside a loopback instrument, "not … a robots-semantics study" (`:53`) | Real surface overlap, already declared client/publisher split. No conflict if C1 stays publisher-side and never models tabi's stop rule. Do not treat tabi's matcher as an oracle. |
| kake | `PROVINCE.md:22-23` (Frontier), `:34-35` (Adjacent); `corpus/knowledge/crawl-scope-per-host.md:8-12,44-46`; no `scripts/robots*` at `4b089da` or in the worktree | Publisher-side placement and offline expectation audit; C1 is the first gate here; live status of `veigapunk.github.io/robots.txt` is named debt (`:44-46`) | Owner. |
| kotoba | `.ufo/waves/round-47/build/SrcNewAnthropicEng.md:19-20`, `.json:42-45` (wave artifact) | Records a fetched robots URL, status and one policy line as source provenance | Practice-only; no parser or committed gate. No province row needed. |
| tameshi | `PROVINCE.md:3-17`; `tools/mutate-and-run.sh:20,38,62,149`; `tools/registry-check.py:1-40` | Owns the mutation/fixture method; refuses sibling-gate ownership; a pattern is admitted from two independent lanes (`:14-16`) | Method adjacency. C2 uses the method; the counter stays kake's. Do not claim tameshi's method or ask it to edit the gate. |
| mado | `PROVINCE.md:26-27`; `tools/mado-assessment.py:63-65`; `tools/mado-evidence-audit.py:5` | "Sealed" fixture selftests and manifest-named-file containment (`resolve().is_relative_to(root)`) | Reusable containment shape. Conflict: mado refuses symlinks outright; C1 resolves them then checks containment (survivor M37), so copy the check, not the refusal. |
| mori | `PROVINCE.md:279-283`; `corpus/lessons/round-23.md:101,108,150` | "Sealed" frozen quota cases and `--selftest PASS N/N`, all in-repo | Terminology collision only: mori's "sealed" means committed frozen cases; C1's key is external and revealed later. |
| kagi / kengaku / kumitate | kagi `PROVINCE.md:51` (`--falsify` 18/18); kengaku `PROVINCE.md:19` (grader mutation battery); kumitate gates via tameshi `PROVINCE.md:8-9` | Each owns mutation/falsification of its own gate | No robots overlap; same method boundary as tameshi. |
| others | grep (tool) `robots\.txt|robotstxt|robotparser|Disallow:` over the 12 lanes below, in committed `scripts/`, `tools/`, `verifiers/` and `corpus/` | chousa, kasegi, revenger, kama, kaidoku, tsukuroi, souji, audio, game-dev-2d/3d, lore, kotodama: no matches (PROVINCE/SKILL checked separately: no robots reference) | No overlap. |

## Boundary statement

`tabi` owns client-side crawler discipline: whether a browser journey may issue an intended request, proved with a lane-authored loopback instrument. `kake` owns publisher-side placement: whether the robots file a publisher will serve allows the URLs the publisher says it should. C1 reads one local file named by a manifest, never fetches, never issues a request and says nothing about what any crawler does. The parsers are **not interchangeable**: on an RFC-shaped file, tabi's `robotsDisallowMatches` returned `/private/` for `/private/public/x` where RFC 9309's longest-match `Allow: /private/public` wins, and no match for `Disallow: /*.pdf$` on `/doc/a.pdf` (RFC: matches). Tabi's 44-byte fixture holds one simple prefix rule, so both readings agree there; that is not a conformance result.

## Traps found

- `urllib.robotparser` is not the reference: `verification/control-CtlC1NaiveReader.json` records 20/28 (met false), failing all four (b) line cases and several (e) cases.
- RFC 9309 §2.2.2 normalization is not URL resolution: reserved escapes stay encoded (`%2F` ≠ `/`), unreserved `%XX` decodes, non-ASCII becomes uppercase-hex UTF-8 octets, longest match is counted in normalized octets (`sources/S011.txt`). `canonical_audit.py` / `base_path_audit.py` use browser-style resolution and must not be imported.
- Counter identity: tabi's `measure-c3.mjs` derives `ownToken` from the repo basename; its caveat says a clone not named `*-shokunin` misbehaves (`.ufo/waves/round-17/drafts/scorecard2.md:36-37`). A reusable counter takes `--root`/`--revision`, not lane identity.
- `sealed` is overloaded (mori, mado); C1 should say "external sealed key" so a reader does not assume the cases are committed.

## Reusable patterns

- `scripts/base_path_selftest.py:1-40` + `scripts/fixtures/<topic>/<case>/expected.json`: run the tool from fixture cwd, compare exit/verdict/sorted finding tuples, exit 0/1/2. `scripts/fixtures/` already holds base-path, citing-set, citing-set-hostile and link-preview; `scripts/fixtures/robots/` fits this convention.
- `.ufo/waves/round-34/c1_matrix_count.py:1-20`: read the tool via `git show <rev>`, materialize cases in a temp dir, and make constant gates fail. Reuse the constant-gate idea as the selftest controls.
- `scripts/link_preview_audit.py:1-40`: manifest → one JSON report, reason-coded findings, exit 0/1/2/64. Reuse the report shape.
- `mado-shokunin/tools/mado-assessment.py:63-65`: containment via `resolve().is_relative_to(root)` only; its symlink refusal contradicts the C1 contract.
- `tameshi-shokunin/tools/mutate-and-run.sh:20,38,149`: inject→run→restore with before/after sha256; C2's E1/E2 dual-implementation cross-check (`.ufo/waves/round-37/c2_mutkill.py:15-25`) is the stronger independence pattern.
- `tabi-shokunin/scripts/check-adjacency.mjs:77-97,883-899`: verify a pinned line verbatim before counting it; reuse for any pinned-row counter (the sealed counter already pins case sha256).

## One move (bounded): ship a contract-edge selftest with the tool

Author `scripts/robots_audit.py` together with `scripts/robots_selftest.py` and `scripts/fixtures/robots/<case-id>/` (manifest, robots file, expected.json), reusing the `base_path_selftest.py` comparison and exit contract. Cases come from the **public** contract edges already measured as survivors in `ctl/MutRefPass.md`, not from the sealed cases: (b) 512000 boundary, SP/TAB-only trim, first `#`, CR/LF split, first colon; (c) group continuation/terminator and merge; (d) `*` matching empty, terminal `$`, first-octet start, normalized-octet length, equal-length `Allow` tie; (e) `%2F` vs `/`, hex uppercase, empty path → `/`, query, no fragment, `/robots.txt` exact; (f/g) integer-vs-bool version, UA fullmatch/alphabet, 3xx bounds, 200/599, float status, symlink containment, 64 MiB and UTF-8 manifest, `checksEvaluated`, report version. Two controls must fail the suite: a prefix-only matcher and stdlib `urllib.robotparser`. Put one docstring line in `robots_audit.py` naming tabi's matcher as a client-side instrument, not an oracle.

Why: `ctl/MutRefPass.md` (sha256 `abd21bdc…`) records 28 of 42 single-point reference mutants still scoring ≥25/28 (14 killed; pristine/restored 28/28). The sealed predicate therefore cannot be the lane's regression oracle for those edges; after the reveal the lane needs a committed pin. This changes no C1 predicate or claim and does not fetch, so it does not touch freshness.

Risks: fixtures derived from the L1's reference are not independent, so label them contract-edge and mark SHOULD/MAY lane readings; build before the reveal to avoid tuning to the key; keep one runner so the lane does not gain a fourth audit convention; if the L1 declines the in-round selftest, ship only the docstring boundary and do not claim the survivors are covered.

## Verification (commands run)

- `git -C tabi-shokunin rev-parse --short HEAD` → `e3cf4e0`, exit 0.
- `git -C kake-shokunin cat-file -t 7c61c8c…` → `commit`, exit 0; `show 7c61c8c:PROVINCE.md | sed -n '30,31p'` → the exact `split-declared` quote.
- `git -C kake-shokunin ls-tree 4b089da -- scripts/robots_audit.py` → empty, exit 0; `test -e scripts/robots_audit.py` → exit 1 (absent in the worktree).
- `python3 -B diverge.py` in `/fast/scratch/hyaku/kake-r37w1/ConnectorSiblings/` → exit 0; outputs `/private/public/x tabi= /private/`, `/private/x tabi= /private/`, `/doc/a.pdf tabi= None`, `wildcard rule tabi= None`; sha256 `4f75d42f…`.
- `sha256sum sources/S011.txt S095.txt S096.txt S097.txt` → `8e632e48…`, `a9094853…`, `d17aa81d…`, `a42aee4e…`.
- `sha256sum ctl/MutRefPass.md verification/c1-at-621fb528.json` → `abd21bdc…`, `22c446a3…`.
- Not run: the C1 counter (no key), any lane selftest or build, any network fetch, any install. I did not verify that the proposed fixtures kill the 28 survivors — that is the L1's build step.

Report: `.ufo/waves/round-37/w1/ConnectorSiblings.md`
