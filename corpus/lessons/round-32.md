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

Row changes logged old→new: S062 new (`—` → `mined`, recheck `90d`, used-by
`corpus/knowledge/render-web-services.md`). The first S062 recheck cell
("on ds4cc-marketplace render.yaml or Dockerfile change", `2f2f12d`) failed
the census (`E09`); it became `90d` at `285abca` before any seat read it.
S062 anchor cell old→new (round-32 wave-1 repair after `CriticC2Scope`): adds
"also retained: apps-sdk/src/server.ts blob 649726df…, .dockerignore blob d650445a…";
status, recheck and used-by unchanged.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| unobserved timestamp written as fact | The round-32 declaration (`SCORECARD.md`, commit `5b32cc7`) says "Declared at 18:58Z"; the commit's own time is `2026-10-22T15:54:19-03:00` (18:54:19Z), so the stated time is 221 s after its own commit (L1 account: the time was estimated, not read; the commit order is the only committed evidence — wave-1 `ScribeMistakeDraft`). | none: no criterion compared a stated declaration time with the declaring commit's time. | `corpus/QUALITY.md` criterion appended this round: a stated declaration time must not be later than `git show -s --format=%cI <declaring commit>`. Shown able to fail: on `5b32cc7` the check `python3 -c` comparing 18:58Z with 18:54:19Z reports a violation (`.ufo/waves/round-32/verification/declared-time-check.txt`). SCORECARD carries an appended correction. |
