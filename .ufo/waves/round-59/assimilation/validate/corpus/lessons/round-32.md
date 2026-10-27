# Round 32 — m3 kill for the citing-set runner; retained ds4cc Blueprint and Dockerfile

## Claims

Declared before implementation in `SCORECARD.md` section "Round 32 — declared
claims" (commit `5b32cc7c4f6494a92912df5a19f589f04f7160a8`, which also carries
both counting commands). Base `a0b0dffcd95b2215f638a5ff7591dd4fde325d27`. Both
claims are routed repairs from `corpus/lessons/round-31-verifier-spotcheck.md`
"Routed defects".

- C1 (operability, routed item 2): mutant m3 is killed by the committed
  hostile selftest. New optional spec key `reason_contains` in
  `scripts/citing_set_hostile_selftest.py` and spec
  `scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json`
  (`git_commit` listed before `git_init`; the load-time guard must be the
  layer that refuses). Counter `.ufo/waves/round-32/c1_m3_probe.py`: killed
  0 at base, 1 at `2f2f12d` with `guard_ok` true (pristine hostile exit 0,
  45 benign cases, 0 failed; mutant fails P6 only).
- C2 (freshness, routed item 5, sourced claim on S062): the two ds4cc-marketplace
  blobs the Render entry reads offline are retained byte-identical under
  `.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/`, registered as S062 and cited
  by the entry's appended section. Counter
  `.ufo/waves/round-32/c2_retained_count.py`: met 0/3 at base, 3/3 at `2f2f12d`.

## Gate

### Source openings

| id | source | opened | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S062 | https://github.com/VeigaPunk/ds4cc-marketplace/blob/1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28/render.yaml (read through the local clone `~/Projects/ds4cc-marketplace` with `git cat-file blob d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252` and `… ee0b63819a9ce71e51469796541b9075e9676ae9`) | 2026-10-22 (L1, before 18:55Z) | “type: web name: ds4cc-marketplace-app runtime: docker dockerfilePath: ./apps-sdk/Dockerfile dockerContext: . healthCheckPath: /health” (render.yaml lines 2–7, whitespace collapsed; 12 words, count corrected by wave-1 seat `CriticS062KindTier`); second quote for the row's `sync: false` clause: “- key: OPENAI_APPS_CHALLENGE sync: false” (lines 15–16; 5 words) | admit, tier A for its own file content at that commit, status `mined` |

| S063 | https://flueframework.com/docs/ecosystem/deploy/render/ (screened by wave-1 scribe `ScribeScreenBlueprintCandidate`, GET 200 at 2026-10-22T18:59:36Z; re-opened by the L1 at 19:01Z, quote present) | 2026-10-22 | “To auto-deploy on every push, set autoDeployTrigger: commit on the service (this replaces the deprecated autoDeploy field).” (17 words) | reject, tier C: restates fields S057 already carries; its one additive claim (`autoDeployTrigger` replacing `autoDeploy`) has no tier-A row. Flip: a Render vendor page documents `autoDeployTrigger` and the deprecation. |
| S064 | https://osher.com.au/blog/how-to-host-n8n-on-render-com/ (screened by wave-1 scribe `ScribeScreenDockerCandidate`, GET 200 at 2026-10-22T19:00:21Z; re-opened by the L1 at 19:01:29Z, quote present) | 2026-10-22 | “Rewritten to reflect Render’s current pricing, the move to native Docker support, and the production patterns we run for clients.” (20 words) | reject, tier C: a prebuilt image (`runtime: image`) is outside S059's Dockerfile-build scope, its bare `healthCheckPath: /healthz` adds nothing to S060, and the page carries four different dates. Flip: a locatable Docker-service or health-check rule S059/S060 lack, with one consistent revision date. |

Screened this round (round-31 routed item 7): two non-primary candidates, both
rejected. A first candidate (`dev.to/ayushn21/deploy-rails-and-sidekiq-to-rendercom-using-yaml-346`)
returned 404 and is recorded as unopened, not as a row.

Row changes logged old→new: S062 new (`—` → `mined`, recheck `90d`, used-by
`corpus/knowledge/render-web-services.md`). The first S062 recheck cell
("on ds4cc-marketplace render.yaml or Dockerfile change", `2f2f12d`) failed
the census (`E09`); it became `90d` at `285abca` before any seat read it.
S062 anchor cell old→new (round-32 wave-1 repair after `CriticC2Scope`): adds
"also retained: apps-sdk/src/server.ts blob 649726df…, .dockerignore blob d650445a…";
status, recheck and used-by unchanged.
S062 source and scope cells old→new (after wave-1 `ReviewS062Row`): "render.yaml and apps-sdk/Dockerfile" → "render.yaml, apps-sdk/Dockerfile, apps-sdk/src/server.ts and .dockerignore"; "Blueprint file and Dockerfile" → "Blueprint file, Dockerfile, server entry and .dockerignore".
S063 and S064 new (`—` → `rejected`, recheck `90d`, used-by `—`).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| unobserved timestamp written as fact | The round-32 declaration (`SCORECARD.md`, commit `5b32cc7`) says "Declared at 18:58Z"; the commit's own time is `2026-10-22T15:54:19-03:00` (18:54:19Z), so the stated time is 221 s after its own commit (L1 account: the time was estimated, not read; the commit order is the only committed evidence — wave-1 `ScribeMistakeDraft`). | none: no criterion compared a stated declaration time with the declaring commit's time. | `corpus/QUALITY.md` criterion appended this round: a stated declaration time must not be later than `git show -s --format=%cI <declaring commit>`. Shown able to fail: on `5b32cc7` the check `python3 -c` comparing 18:58Z with 18:54:19Z reports a violation (`.ufo/waves/round-32/verification/declared-time-check.txt`). SCORECARD carries an appended correction. |

## Carried open (wave-1 sweep, not mined this round)

Wave-1 seat `ReviewMistakeSweep` (`.ufo/waves/round-32/w1/ReviewMistakeSweep.md`) lists
round-31 wave-2 findings with no lesson `## Mistakes` row. Carried here by pointer, not
judged this round:
- `.ufo/waves/round-31/a2-w2/CriticQualityCriteria.md` F1–F3 (criterion checks that cannot fail or fail the round's own wave).
- `.ufo/waves/round-31/a2-w2/ReviewProvinceReadme.md` F1 (PROVINCE "nothing live was fetched" vs five live GETs) and F2.
- `.ufo/waves/round-31/a2-w2/ReviewCensusAfter.md` F1 (census before/after transcripts byte-identical; no census-mode receipt).
- `.ufo/waves/round-31/a2-w2/ReviewHostileSelftestCode.md` F2 (NUL crash; repaired in code, no row).
- Routed item 3 sub-items (`round-31-verifier-spotcheck.md` "Routed defects" 3): `read_expected` OSError escape, silent skip of stray fixture-root entries, duplicated option tables — still open at `df31d30` (`w1/ReviewRoutedItemsStatus.md`).
- Git-pin mutants m3d, m3f, m3g survive the hostile selftest (`w1/MutM3Variants.md`).
- New, pre-existing at base and tip (`w1/ExecBenignSuiteTip.md`): the runner's default scratch path is a fixed shared directory (`scripts/citing_set_selftest.py:133`) and the gate's `--selftest` delegation cannot pass `--tmpdir`, so two concurrent `citing_set.py --selftest` runs fail falsely (4/4 at both revisions; distinct `--tmpdir` values: clean).
- C1 counter code notes (`w1/ReviewC1ProbeCode.md`, frozen counter, not changed): `killed` is not gated on `guard_ok` in code (receipts all carry guard_ok true); a timeout raises instead of exit 2; exit 1 from a crashed harness would also read as killed.
