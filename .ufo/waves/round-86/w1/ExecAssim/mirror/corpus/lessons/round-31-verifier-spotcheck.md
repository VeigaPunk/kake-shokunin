author: hyaku closure (non-author integrator, @m_opus)

# Round 31 non-author verification: both declared claims verify; admitted

Lane round: kake 31 (two attempts; attempt 2, L1 `KakeR31a2`, inherited attempt 1's pushed work).
Base `f1ffb81738c92c0537b99b30970143ab9419f990`; lane tip `46b94fa588e1b9c33e7ffbfb3bebb66b52a950db`;
fleet report `.ufo/reports/round-31/kake.md` at fleet commit `4155cf7ec82447df4bc1690d0a7fa62eb39357f1`
(it replaces `d085219580e678309918a354c65597397a5c8b51`). The claims were judged as declared in
`SCORECARD.md` "Round 31 — declared claims" (`a16602a`) and the strict supplement (`b801ac8`),
before any data was read.

Driver digest (`.ufo/watchdog.log`, copied):
- 2026-10-22T12:38:24-03:00 launch kake round=31 pgid=3814252 driver=hyaku-inline attempt=1
- 2026-10-22T14:30:11-03:00 lane-dead-no-report kake round=31; retry same round (omp process restart at 17:26Z)
- 2026-10-22T14:30:13-03:00 launch kake round=31 pgid=1003963 driver=hyaku-inline attempt=2
- 2026-10-22T15:44:05-03:00 complete kake round=31; hyaku-inline attempt=2

Re-check seats (read-only reviewers, this closure): `HyakuCloseKake31.VerifyC1Evidence` and
`HyakuCloseKake31.VerifyC2Entry`. The held items `KakeR31.CriticC1Counter` and
`KakeR31.CriticSandboxThreatModel` were not retried, rerouted or rephrased here, and this closure
added no seat item on their ground.

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-31/kake.md` | `kake-shokunin kake@shokunin.local 4155cf7e…` and `… d0852195…` | pass |
| SHONEN heading, one line per box | read report `## SHONEN` | 4 lines, `[~]`, one per box of `SHONEN.md` (4 boxes) | pass |
| Cited commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` for a16602a c88b97e b801ac8 fde133a 92235a0 9a7f5be 08ff06c 46b94fa f1ffb81 | all 9 `anc-ok` | pass |
| Lane pushed, clean | `jj-lane.sh state …/kake-shokunin`; `git status --porcelain` | `local=remote=46b94fa… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | pass |
| Remote branch | `git ls-remote origin refs/heads/master` | `46b94fa588e1b9c33e7ffbfb3bebb66b52a950db` | pass |
| Prompt carries template contract | `grep -n '^## ' .ufo/prompts/kake-round-31.md` vs `templates/round-prompt.md` | §1, §2, §2b, §3, §4, §5 identical headings, plus §6 hyaku addendum | pass |
| Not a marker report | report content | 8 landed commits, receipts, measurements | real report |

Defects (status-neutral): none blocking. Noted: the report's round-30 item (5) says the
`history://KakeR30.*` pointers no longer resolve, so those seat transcripts are not closure-time
evidence (§Evidence standard); the committed `partial-reports.json` is the surviving evidence.

## Claims

Re-measured here = plain commands I ran over committed bytes. Evidence-verified = the lane's own
counter/selftest receipts checked against committed hashes (§Gate standard, Closure consequence:
a sibling's gate is not executed by the integrator).

### C1 — operability repair: citing-set runner refuses five hostile shapes, 0/5 → 5/5, K1 holds

Evidence-verified (`VerifyC1Evidence`), plus a plain re-read of the runner:
- Counter identity: `git show a16602a:.ufo/waves/round-31/c1_sandbox_probes.py | sha256sum` and the
  same at `46b94fa` → both `4707cebf8831eb9a…43166d1a`, matching the declaration.
- Receipts (`jq` over `.ufo/waves/round-31/verification/c1-*.json`): `c1-before-f1ffb81` 0/5, K1
  exit 0 / 45 cases (P1 canary written, P2/P3/P5 exit 0 with no refusal, P4 timed out);
  `c1-after-c88b97e`, `c1-after-fde133a`, `c1-a2-at-92235a0` 5/5, K1 45; `c1-a2-at-9a7f5be` 5/5,
  K1 45, runner `7c95a18e…88969`.
- Runner at tip: `git show 46b94fa:scripts/citing_set_selftest.py | sha256sum` = `7c95a18e…88969`,
  equal to the `9a7f5be` receipt; `git diff --stat 9a7f5be 46b94fa -- scripts/` is empty.
- Hostile selftest receipts: `hostile-selftest-a2-at-9a7f5be.json` passed, 5/5, canary false,
  victims unchanged; `hostile-selftest-a2-base-runner.json` fails (P1 canary true, P2/P3/P5 exit 0,
  P4 timeout); `a2-fixes/*name-sham*`: the sham passes the `c88b97e` selftest 5/5 and fails the
  repaired one 0/5.
- Specs: `git ls-tree 46b94fa:scripts/fixtures/citing-set-hostile/` → P1-selftest-argv,
  P2-fixture-dot-git, P3-commit-without-init, P4-expected-json-guard, P5-symlinked-case.
- Benign: `benign-a2-at-9a7f5be.json` clean, 45 cases, 0 failed.

Ruling on the disclosed weakness (the frozen counter trusts the failure names the runner reports, so
a sham runner would score 5/5). The declared claim is about the landed runner, not about the
counter's power. I re-read the landed runner (760 lines) with
`git show 46b94fa:scripts/citing_set_selftest.py | grep -n -E 'allowlist|GIT_CEILING|O_NOFOLLOW|ELOOP|S_ISREG|1048576|\.git|is_symlink|git_init'`:
it refuses by content, not by name — argv allowlist (line 368), `.git` entry anywhere in a case
(388–391, 539), `git_commit` without earlier `git_init` (360–363), `expected.json` opened with
`O_NOFOLLOW|O_NONBLOCK|O_NOCTTY`, `S_ISREG` and a 1 MiB cap (141, 399–407), symlinked case dir
fails (534), `GIT_CEILING_DIRECTORIES` and `--git-dir/--work-tree` pins (443–450, 703–711). A grep for
case-name matching (`'h[0-9]`, `startswith('h`) finds none. With the repaired selftest's
`h0-control` (a name sham fails it) the counter's name trust does not reach the landed bytes.
**C1 verifies as declared.** The counter hole stays a routed defect (below).

### C2 — freshness (learning claim): Render web services and Blueprint entry, 0/4 → 4/4 (strict 0/5 → 5/5)

Re-measured (`VerifyC2Entry`, python over `git show` bytes only, and my own reads):
- Gate quotes S057–S060 in `corpus/lessons/round-31.md` `## Gate`: 15, 19, 13, 22 words, each an
  exact substring of `.ufo/waves/round-31/sources/S05N.txt` after whitespace collapse.
- `corpus/SOURCES.md` rows S057–S060 inside `## Registry`, `mined`, accessed 2026-10-22, used-by
  `corpus/knowledge/render-web-services.md`. Rows: `git show <r>:corpus/SOURCES.md | grep -c '^| S0'`
  → 56 at `f1ffb81`, 61 at `46b94fa`.
- `sha256sum` of each retained `.txt` equals `receipts.json` `textSha256`.
- Declared closure command: `git diff --quiet a16602a 46b94fa -- .ufo/waves/round-31/sources/receipts.json …S057–S061.txt …fetch_sources.py` → exit 0.
- Receipts: `c2-a2-at-9a7f5be.json` 4/4, control not broken, counter `de48d460…c31b8` (= committed
  bytes, unchanged a16602a → 46b94fa); `c2-strict-a2-at-9a7f5be.json` 5/5, checker `5111264f…846ad`
  (added at `b801ac8` before any C2 after-receipt, unchanged since).

Ruling on the disclosed weakness (strict C2 proves quotes are real, not that sentences are true).
I read the entry body as the declaration asked: 6 substantive sentences were sampled against the
retained text — PORT default 10000 and its mechanism (S058), secrets kept out of build args and
`.dockerignore` / secret files (S059), 15 s routing stop and 60 s restart (S060), `sync: false`
prompt-once and ignored on update (S057), `renderSubdomainPolicy` narrowing (S057), 2xx/3xx within
5 s, 15-minute deploy cancel and Host header (S060): **6/6 supported, 0 overreach, 0 wrong**, with
the wave-2 corrections already appended. The ds4cc-marketplace `render.yaml` facts rest on an
external repo (blob `d17ab7e5`) that the lane does not retain; the entry discloses this.
**C2 verifies as declared.**

### No-harm

- `git diff f1ffb81 46b94fa -- SCORECARD.md | grep -c '^-[^-]'` → 0: the round only appended; no axis
  rating moved (10 → 10 stated for both owned axes).
- `git diff --stat f1ffb81 46b94fa -- SHONEN.md SKILL.md corpus/QUALITY.md PROVINCE.md corpus/README.md LOG.md corpus/knowledge/`
  → 375 insertions, 0 deletions (append-only, SHONEN.md untouched).
- `git diff f1ffb81 46b94fa -- corpus/SOURCES.md | grep -cE '^[-+]\| S05[34]'` → 0: S053/S054 cells unchanged.
- `scripts/` changed only by the runner, the hostile selftest and the five specs; 45 benign fixtures clean.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 0/5 → 5/5, K1 holds, landed runner refuses by content |
| freshness | improved | C2 0/4 → 4/4, strict 0/5 → 5/5, 5 new tier-A rows opened 2026-10-22 |
| depth | unchanged | no claim; appended entry corrections only |
| coverage | unchanged | no claim |
| calibration | unchanged | no claim |
| adjacency | unchanged | no claim; PROVINCE append-only, no operator-owned property touched |

## Discernment spot-check

Re-opened live between 2026-10-22T18:44Z and 18:50Z with one `curl -sL` GET each (all HTTP 200); text = HTML minus
script/style/comments, tags removed, entities decoded, whitespace collapsed.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S058 Render Docs: Web Services | admit (tier A, mined) | https://render.com/docs/web-services | agree | Quote “Your web service must bind to a port on host 0.0.0.0 …” present live; "PORT is 10000" present; vendor primary for its own platform, scope stated narrowly |
| S057 Render Docs: Blueprint YAML Reference | admit (tier A, mined) | https://render.com/docs/blueprint-spec | agree | “Render ignores any environment variables with sync: false” present live; `healthCheckPath`, `dockerContext` documented as the row scope says |
| S054 NameSilo blog: custom domain to Render | reject (kept `rejected`) | https://www.namesilo.com/blog/en/dns/how-to-connect-a-custom-domain-to-rendercom | agree | The post gives apex `A … 216.24.57.1`; the Render primary S061 now states the same address live (“you can use 216.24.57.1 to point your root domain to Render's load balancer IP”), so a registrar post adds nothing a primary does not carry |
| S053 DEV Community tutorial | reject (kept `rejected`) | https://dev.to/stephengade/how-to-deploy-static-website-for-free-on-render-with-custom-domain-4efo | agree | Tutorial (Aug 5, 2023) says “Grab your CNAME and ALIAS”; S061 live names ANAME/ALIAS for root domains, and the `/index.html` rewrite is carried by S050 — nothing durable left |

Newly written row re-opened: S061 (`corpus/SOURCES.md`, lesson Gate quote “A records point to IP
addresses, and you can use 216.24.57.1 to point your root domain to Render's load balancer IP.”):
21 words (≤ 25), present verbatim in https://render.com/docs/configure-other-dns re-opened live — agree.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
→ `kake W04 S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes` (pre-existing),
`kake ok …/kake-shokunin/corpus/SOURCES.md`, exit 0.

Thin point: no screened candidate this round (the screening seat died at spawn), so the reject
side rests on the S053/S054 re-resolution, not on new rejections.

## Trend verdicts

- **expansion: improved.** New held entry `corpus/knowledge/render-web-services.md` (77 lines) on
  open Frontier ground, 5 tier-A rows (56 → 61), SKILL triage table; 6/6 sampled sentences supported.
- **quality: improved.** Routed overreaches in `render-static-sites.md` corrected append-only; runner
  containment with hostile specs; four wave-2 defects repaired at `9a7f5be`, each shown able to fail
  (fde133a runner fails P5 `.h5b`; name sham fails the repaired selftest).
- **discernment: improved.** Spot-check agrees on 2 admits and 2 rejects; S053/S054 flip conditions
  were met and correctly not flipped; both counters' limits are disclosed rather than hidden;
  QUALITY criteria that could not fail were replaced. Thin: no new screened rejects this round.

## Admission

Every declared claim verifies (C1 evidence-verified plus runner read; C2 re-measured plus truth
sampling) and no axis is harmed. **Admitted.** Status `ok`.

SHONEN (operator-owned promotion): boxes 1 (SKILL decision tables with cited sources), 3
(executable instructions) and 4 (PROVINCE accurate) look checkable by a non-author from committed
bytes; box 2's end-to-end task rests partly on an external repo blob. No `[x]` is written here.

## Routed defects (kake, next round)

1. C1 frozen counter trusts runner-reported failure names (`a2-w2/ReviewHostileSelftestCode.md` F1):
   any future containment counter must carry a benign hostile-named control as the repaired
   selftest does.
2. Git pins and mutant m3 are not probed alone (`MutRunnerGuards`: m3 survives) — add a spec that
   kills m3, shown able to fail.
3. `ReviewRunnerDiff` LOW/INFO items left unrepaired by the freeze: `OSError` from `fstat`/`read` in
   `read_expected` escapes the handler; stray regular files, FIFOs and sockets at the fixture root
   are skipped silently; option tables duplicate the gate parser by hand; symlink docstring wording.
4. C2 strict supplement certifies provenance, not truth (`ReviewC2StrictChecker`: three hollow or
   false commits score 5/5) — a truth-sampling step belongs in the next learning claim's declaration.
5. The entry's ds4cc-marketplace `render.yaml` facts rest on an unretained external blob
   (`d17ab7e5`): retain or pin it so a fresh session can re-check.
6. `history://KakeR30.*` pointers no longer resolve: never cite seat transcripts as evidence;
   commit the needed excerpt.
7. No screened candidate this round: screen at least one non-primary candidate next round so the
   reject side has new decisions.
