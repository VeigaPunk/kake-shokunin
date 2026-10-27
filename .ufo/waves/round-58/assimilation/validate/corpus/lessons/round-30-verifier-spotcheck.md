author: hyaku closure (non-author integrator, @m_opus)

# Round 30 non-author verification: both declared claims verify; admitted

Runtime model as exposed to this closure session: `anthropic/claude-opus-5-5`
(task route `@m_opus`; no model parameter passed). Fresh closure subagent
`HyakuCloseKake30`, dispatched by the hyaku orchestrator, not by the lane.
Base `035668132250b75b38d399e86e540b0a0371efbc`, head
`91b60bd40c07de351c54ebdc366502f33dc19412`, branch `master`. Judged on
committed bytes only. Commit `636dddd` (operator daily reflection,
`considerthese/2026-10-22.md`) is in the range and was not judged.

Three read-only reviewer seats ran beside this closure (`RunnerSandboxHold`,
`EntrySentenceSupport`, `NoHarmRangeScan`). None executed a lane script. I
re-ran their decisive points myself where this file says so.

Driver digest (copied from `.ufo/watchdog.log`, which is mutable):

```
2026-10-22T08:45:34-03:00 launch kake round=30 pgid=3763194 driver=hyaku-inline attempt=1
2026-10-22T10:33:21-03:00 complete kake round=30; hyaku-inline attempt=1
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-30/kake.md` (fleet) | `kake-shokunin <kake@shokunin.local> 54ffccb59bab136aa9a3737f136f147c4fbd5857 2026-10-22T10:32:45-03:00` | pass |
| Report filed after its commits | committer dates | lane tip `91b60bd` 10:32:03, report 10:32:45, completion 10:33:21 | pass |
| `SHONEN` heading, one line per box | read report lines 55-60 | 4 lines, all `[~]` | pass |
| Cited hashes exist and are ancestors | `git cat-file -t <h>` and `git merge-base --is-ancestor <h> master` for `4580c78 04637bd 71c6bfa 451e98f 1c7773e f80bd8f 91b60bd 636dddd 7697990 234524c` | `commit` and ancestor ×10 | pass |
| Lane pushed, nothing left over | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain \| wc -l`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 head=detached tracked=0 untracked=0`; `0`; remote `91b60bd4…` | pass |
| Prompt carries the template contract | every non-placeholder, non-empty line of `templates/round-prompt.md` searched (whitespace collapsed) in `.ufo/prompts/kake-round-30.md` | 105/105 present (fleet and canonical template); hyaku addendum §6 at prompt line 141 | pass |

## Claims

Re-measured: C2 (the lane counter re-run at base and head, plus independent
quote, hash and live checks). Evidence-verified: C1. Its counter and the
strict supplement execute the lane's gate `scripts/citing_set.py` and its
runner. Under PROTOCOL §Gate standard (Closure consequence) this closure did
not execute them. I checked the committed receipts against the head bytes and
added independent plain counts.

### C1 — operability repair: citing-set reason codes, 0/14 → 14/14 (strict 0/6 → 6/6)

- The declaration is frozen. The `4580c78:SCORECARD.md` row says before 0/14,
  after 14/14 with 3 controls holding and both constant gates below 14. The
  strict supplement was declared at `04637bd`, before any after-measurement
  (`71c6bfa` 09:40 is later than `04637bd` 09:14).
- Blob identity per commit (`git show <rev>:<path> | sha256sum`):
  - The counter is `be2a1287ab7f…` at all seven round commits.
  - The strict checker is `96e7bbcd8ec9…` from `04637bd` to `91b60bd`.
  - The gate is `d7e79ba102ff…` at base and `dbfade45e593…` from `71c6bfa`
    to `91b60bd`.
  - The runner is `3c167895c7f3…` at base, `0fc87d5b8134…` at
    `71c6bfa`/`451e98f`, `a62d4b0eaada…` at `1c7773e` and `9f2d1ecb280b…` at
    `f80bd8f`/`91b60bd`.
  - `git diff --stat f80bd8f 91b60bd -- scripts` is empty, so the `f80bd8f`
    receipts grade the head bytes.
- Receipts (`.ufo/waves/round-30/verification/`):
  - `c1-before-0356681.json`: revision `03566813…`, gate `d7e79ba1…`,
    runner `3c167895…`, `passed 0/14`, rPassed 0, fPassed 0,
    controlsHold true, constantGatesRejected true.
  - `c1-after-f80bd8f.json`: revision `f80bd8fa…`, gate `dbfade45…`, runner
    `9f2d1ecb…`, `passed 14/14`, R01–R08 and F01–F06 each `pass: true`,
    K1–K3 true, constant gates rejected. The `71c6bfa` and `1c7773e`
    receipts also read 14/14 with their own runner hashes.
  - The strict receipts read 0/6 at base and 6/6 at `71c6bfa`, `1c7773e` and
    `f80bd8f`. Each names `declaredCounterSha256 be2a1287…c53e`, which is the
    check the SCORECARD asks the closure to make.
  - Every receipt hash matches the blob hash above.
- My own counts (`git ls-tree`, `git grep` at base → head):
  - Citing-set fixture cases: 29 → 45.
  - `expected.json` files naming a `"reason"`: 0 → 16.
  - Each of the ten reason codes is named by ≥1 fixture at head and by 0 at
    base: the eight round-28 codes plus `document_duplicate_key` and
    `document_nonfinite_number`.
  - Fixtures 42–45 expect exit 64 with no findings.
  - The runner reads a finding's `reason` (`get("reason")`) 0 times at base;
    at head it compares the sorted multiset of `(id, reason)` pairs (runner
    lines 208–277).
- Scope as landed: the routed list in
  `round-28-verifier-spotcheck.md:216-220` is duplicate-key and non-finite
  JSON, `S01`-style ids, repeated options, deep corpus and `O_NOCTTY`. That is
  F01–F06. The SCORECARD measured results disclose what stays open:
  IDENTITY-PATHS, RETENTION-FRAGMENT, RETENTION-TRUST-BOUNDARY,
  C1-UNIT-OVERRIDE, the socket label, 12 of 25 codes without a fixture, four
  strict-checker holes and three runner mutants no instrument kills. The
  claim is admitted in that qualified scope, not as "all round-27 families".
- **Verdict: verifies at the declared value (14/14; strict 6/6),
  evidence-verified.** Axis operability: `improved`.

### C2 — freshness (learning claim): Render static-site entry, 0/4 → 4/4

- The counter blob is `a2cd3164f67e…` at all seven round commits; the
  exported copy's sha256 is `a2cd3164…5e7a`.
- `python3 -B c2_quote_truth.py --root <lane> --revision 035668132250…` →
  `{"passed":0,"total":4,"controlBroken":false}`, exit 1.
- The same command at `91b60bd40c07…` → `{"passed":4,"total":4,"controlBroken":false}`,
  exit 0. S049–S052 all pass.
- Declared closure checks:
  - `git diff --quiet 4580c78 91b60bd -- .ufo/waves/round-30/sources/ .ufo/waves/round-30/fetch_sources.py`
    exits 1. The only changes are 7 added files under `sources/screened/`.
  - Limited to `S049–S052.txt`, `receipts.json` and the fetcher, the same
    diff exits 0, so the retained sources the claim rests on are unchanged.
    The lane disclosed the literal miss.
  - Every receipt URL equals its registry row URL (reviewer seat, 4/4).
- Entry body read (`EntrySentenceSupport`; I re-checked the two flagged lines):
  - 4/4 retained-text sha256 match the receipts.
  - 59/59 curly-quoted spans are exact substrings after whitespace collapse.
  - Of 29 behaviour bullets, 27 are supported by a located span and 4
    statements carry `[INFERENCE]`. No sentence is unsupported.
  - Two qualifiers overreach. Line 53 says "normalized lowercase name", but
    S051 has 0 hits for "lowercase"; it says "normalized" and shows lowercase
    example keys. Line 26 says the only build-time setting besides the branch
    is dependency installation, while S049 also names the build command.
    Both are low severity and routed below.
- Live re-open (one ordinary GET each, 2026-10-22T13:37:32–33Z): the visible
  text sha256 of S050, S051 and S052, computed with the lane's text rule,
  equals the receipt `textSha256`. The bodies differ, as the lesson
  discloses (asset names and trace ids).
- **Verdict: verifies at the declared value (4/4), re-measured.** Axis
  freshness: `improved`.

### No-harm

- `git diff 0356681 91b60bd -- SCORECARD.md` is +143/−0, two appended
  round-30 sections. Axis ratings stay 10/10 and no capability row is
  self-awarded.
- Removed lines (`NoHarmRangeScan`): 64, all in `scripts/citing_set.py`,
  `scripts/citing_set_selftest.py` and fixtures 13–16. Each is a superseding
  edit. Fixtures 13–16 keep their id and exit and add a reason, and the
  iterative walk keeps the sorted order and its refusals.
- Append-only files: `corpus/SOURCES.md` +10/−0 (S001–S048 unchanged, rows
  48 → 56), `LOG.md` +26/−0, `QUALITY.md` +85/−0, `PROVINCE.md`,
  `README.md` and `SKILL.md` additive.
- `corpus/knowledge/`: one entry added and `publish-channels.md` appended
  (+25/−0). `SHONEN.md` blob unchanged; no `[x]`.
- The round-29 capability is unaffected: the `scripts/base_path_audit.py`
  blob is identical at base and head, and its fixtures are untouched.
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  prints `kake W04 S033 duplicate url …rfc9110.txt across scopes` and
  `kake ok …/corpus/SOURCES.md`, exit 0. That equals the committed
  `census-before.txt` and `census-after.txt`; the W04 predates the round.
- Wave-2 harm repairs at head (`RunnerSandboxHold`, a static read; I
  re-traced N1 and swept the committed `case.json` files myself):
  - The mixed-reason crash and the unwritable-copy crash are closed.
  - All ten sentinel probes are refused: `..` or absolute setup paths, root
    escape, FIFO overwrite, fixture hooks, `core.hooksPath` in a fixture
    config, a symlinked case and a 100k-step setup. Containment uses
    realpath on both sides.
  - The repair is narrower than its commit message.
    - N1: a case `argv` of `["--selftest"]` makes the gate delegate to the
      runner with `--root <case copy>`. The runner then executes
      `<copy>/scripts/citing_set.py` (gate `run_selftest`, lines 834–870;
      runner `resolve_paths`, lines 137–143).
    - N2: `git_commit` does not refuse a fixture `.git`; only `git_init`
      does (runner lines 374–380).
    - N3: a `git_commit` with no `git_init` would discover an enclosing
      repository.
    - N5: `expected.json` is read with no symlink or size guard.
    - N6: symlinked cases are dropped silently with `--min-cases 0`.
  - **Ruling: latent conformance defects, not a realized harm.** The eight
    committed `case.json` files use only `fifo`, `mkdir`, `git_init` followed
    by `git_commit`, and argv `--revision/--population/--ledger/--roo/--rev`.
    No fixture path contains `.git` or `scripts/`, and every tree entry is
    mode 100644. No head fixture reaches any of these paths. The code they
    could run comes from the lane's own committed tree, which already
    supplies the executed gate. They are routed below as defect 1.

Per-axis verdicts: operability `improved`; freshness `improved`; depth,
coverage, calibration and adjacency `unchanged` (not owned, not claimed).

### Round shape (25% attack share on returned seats)

- Wave 1 (`w1/swarm-registry.json`, 34 reports): reviewer 8, critic 5,
  mutation-tester 3, so 16/34 attack (47%), 0 dead.
- Wave 2 (`w2/swarm-registry.json`): 34 seats, of which the L1 reports 15
  returned and 19 cancelled. Twenty reports are committed: reviewer 7,
  critic 7, mutation-tester 4, scout 1, sentinel 1. Which 5 are partial is
  not marked.
- Worst case, counting the scout and the sentinel as returned and as
  non-attack: 13/15 attack.
- Round on returned seats: at least 29/49 (59%). Even with no wave-2 attack
  seat counted, it is 16/49 (33%). **The 25% share holds.**
- The cancelled seats' partial reports are unverified. No claim verdict here
  rests on them.

## Discernment spot-check

`corpus/lessons/round-30.md` `## Gate` records four sources mined (S049–S052),
two rejected (S053, S054), two queued (S055, S056) and one not opened (Stack
Overflow 403). My re-opens are one ordinary GET each at 2026-10-22T13:37:32–34Z,
with the lane's visible-text rule.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S050 Render Docs, Redirects and Rewrites | admit (`mined`, tier A) | https://render.com/docs/redirects-rewrites; text sha256 `1c413643…52c5ed`, identical to the receipt | agree | Vendor primary for the platform behaviour. Its quote “Render does not apply redirect or rewrite rules to a path if a resource exists at that path.” is exact, 18 words. The scope cell limits it to Render static-site rule matching |
| S052 Render Docs, Custom Domains | admit (`mined`, tier A) | https://render.com/docs/custom-domains; text sha256 `6c1616f8…f769`, identical to the receipt | agree | Vendor primary. The 25-word quote is exact (with the tag-gap space before “.”). The S054 reason says S049 names Let's Encrypt and Google Trust Services; the retained S049 text and the live S052 page both name them |
| S053 dev.to tutorial (2023) | reject (tier C) | https://dev.to/stephengade/how-to-deploy-static-website-for-free-on-render-with-custom-domain-4efo; body and text sha256 identical to the screened receipt; “Aug 5, 2023” present | agree | It is a third-party tutorial whose rewrite point S050 already carries. Its ALIAS step is correct: Render's “configure-other-dns” page names ALIAS/ANAME (7 hits). That is the row's flip, which by its own wording still adds nothing beyond S050/S052 |
| S054 NameSilo blog (dated 7/8/2026) | reject (tier C) | https://www.namesilo.com/blog/en/dns/how-to-connect-a-custom-domain-to-rendercom; text sha256 identical to the screened receipt; quote exact | agree | A registrar blog should not carry a platform IP when a vendor page exists. The reason is accurate as worded, since no *opened* primary states 216.24.57.1. However, https://render.com/docs/configure-other-dns (linked from S052, GET 13:37:34Z) reads “you can use 216.24.57.1 to point your root domain to Render's load balancer IP”. So the row's flip condition is met today; routed as defect 4 |

New `SOURCES.md` row re-opened with its quote: **S051** (Render Docs, Static
Site Headers). The live visible text sha256 is `e98982ce…a27d`, identical to
the receipt. The gate quote “The header path must be a relative path without
the domain. It will be matched with all custom domains attached to your
site.” is 23 words and an exact substring of the live text. The row's anchor
(“Header syntax” section, the “Path Effect” table) exists in the retained
text. Agree.

The spot-check agrees with the gate on both admits and both rejects.

## Trend verdicts

- **expansion: improved.** The admitted `corpus/knowledge/render-static-sites.md`
  is on ground the base `PROVINCE.md:29-30` listed as open ("Render deploy
  semantics remain open"). It has a new coverage row,
  `corpus/README.md:277` "Render static sites (r30)". Its four `source:` ids
  are `mined` rows opened this round, and its counter is 4/4.
- **quality: improved.** The existing entry `publish-channels.md` was
  re-verified and deepened by an append-only "Round-30 Render recheck". I
  confirmed it against the surface: `git -C ~/Projects/ds4cc-marketplace
  rev-parse 1fbdb8ed:render.yaml` → `d17ab7e5…`. Lines 2–7 declare the
  Docker web service; `ALLOWED_HOSTS` sits at 11–12 and the session and
  challenge keys at 15–20; the file has no `domains` key. The HOLD and ADDED
  lines are correct. No admitted entry failed its re-check. The two
  qualifier overreaches in the new entry are imprecise wording, not false
  statements left standing.
- **discernment: improved.** This outside spot-check agrees with the gate on
  two admits (S050, S052) and two rejects (S053, S054), and the S051 quote
  verifies live. The rejects come from the source gate itself, and a wave-2
  critic corrected their reasons. The round-30 `QUALITY.md` section is
  grounded in `round-29-verifier-spotcheck.md:230-248`.

## Admission

Both declared claims verify at their declared values. Their targets were
frozen in `4580c78` and the strict supplement in `04637bd`, before
measurement. No owned axis is harmed. **Admitted.** No capability row was
added, and no promotion, mint, SHONEN `[x]` or state advance is made here.

For the operator: the four SHONEN boxes look checkable by a non-author from
committed bytes. They are the SKILL "Render static-site triage — round 30"
table, the `LOG.md` round-30 entry with `r29-rerun/receipt.json`, the SKILL
"Citing-set reason-code registry — round 30" section, and PROVINCE's
round-30 section. Promotion is operator-owned.

## Routed defects (kake, next round)

1. **Runner containment is narrower than `f80bd8f` states.** Five gaps:
   - Refuse `--selftest`, and any argv outside an allowlist, in `case.json`
     (N1: it runs `<copy>/scripts/citing_set.py`).
   - Refuse a fixture `.git` for every setup op and require `git_init`
     before `git_commit` (N2).
   - Pin `GIT_CEILING_DIRECTORIES` and `--git-dir`/`--work-tree` (N3).
   - Open `expected.json` with `O_NOFOLLOW`, a regular-file check and a size
     cap (N5).
   - Count a symlinked case as a failure, not a silent skip (N6).

   Add a fixture or counter probe for each. Static evidence:
   `history://HyakuCloseKake30.RunnerSandboxHold`, runner and gate line
   references above.
2. Still open and carried by name:
   - the round-27 IDENTITY-PATHS, RETENTION-FRAGMENT,
     RETENTION-TRUST-BOUNDARY and C1-UNIT-OVERRIDE families;
   - the socket `document_unreadable` label;
   - 12 of 25 reason codes without a fixture;
   - deep corpus and `O_NOCTTY`, guarded only by round counters (no
     committed fixture);
   - the four strict-checker holes and runner mutants m2, m4, m5.
3. `corpus/knowledge/render-static-sites.md`:
   - Line 53: mark "lowercase" `[INFERENCE]` or drop it.
   - Line 26: correct "the only build-time setting … besides the branch",
     since S049 also names the build command.

   Use an appended correction, per the corpus rules.
4. Open https://render.com/docs/configure-other-dns as a primary row. It
   states 216.24.57.1 for the root domain and names ALIAS/ANAME. Then
   resolve the S053/S054 flip conditions it now meets.
5. Mark cancelled-seat reports as partial, in the report file or the wave
   registry. Wave 2 commits 20 reports for 15 returned seats, and no file
   says which 5 are partial.
6. A declared closure command should be one that can pass as written. The
   C2 `git diff --quiet 4580c78 <commit> -- sources/` exits 1 because
   `screened/` was added under the same directory. Name the exact files, or
   keep screened bodies outside the pinned directory.
