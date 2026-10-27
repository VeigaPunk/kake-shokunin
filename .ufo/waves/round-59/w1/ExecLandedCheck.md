# ExecLandedCheck

Seat scope: run `scripts/landed_check.py` against the round-58 kake report and the round-58 SCORECARD section, verifying every cited hash is an ancestor of lane `master`. Read-only throughout (git show/log/ls-tree/rev-parse/diff only; no git/jj mutation in the lane; one throwaway fixture repo under scratch, deleted).

## RUN:

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/landed_check.py --help
```
→ usage: `--report REPORT --repo REPO --branch BRANCH --selftest`; "Check that every commit hash a report cites is an ancestor of a branch."

Tool selftest (tool integrity, before use):

```
python3 -B .../scripts/landed_check.py --selftest      # exit 0
```
→ `selftest 14/14` (PASS honest-report, side-branch-hash, unknown-hash, sha256-token-ignored, short-hash-ambiguity, empty-report, prose-only-report, branch-missing, hash-inside-code-fence, duplicate-hash-counted-once, non-commit-object-skipped, digest-label-ignored, report-missing, usage-error).

Primary runs (lane repo `/home/vgpnk/Projects/shokunin/kake-shokunin`; `master` = `cb685273cc9e331b51f45485793d5d1c91184b3a`, `origin/master` identical):

```
L=.../kake-shokunin/scripts/landed_check.py; R=.../kake-shokunin
python3 -B $L --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-58/kake.md --repo $R --branch master
python3 -B $L --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-58/kake.md --repo $R --branch origin/master
python3 -B $L --report $R/.ufo/waves/round-59/w1/ExecLandedCheck.scorecard-r58.md --repo $R --branch master   # section extracted to scratch
```

Exit codes were measured as the tool's own status (direct invocation, no pipe), not a pipeline's last element.

## RESULT:

**1. Round-58 report vs lane `master` — PASS (exit 0).** `cited=10 landed=10 missing=0 unknown=0`; identical under `--branch origin/master`.

| Cited hash (as written) | Subject in lane | Status |
|---|---|---|
| `9892ea4ab42d305adb408905a3f19f7b7109f095` | round-58: hand-check quarantine slice and record frozen-claim conflict | ANCESTOR |
| `8d340c15200959190ba3e894399cdc931976331f` | round-58: fidelity corrections, historical receipt-pin gate note, lesson erratum | ANCESTOR |
| `de7d96e720522ea15fba3fd9ee3ce58c42596031` | round-58: T0 measurements and C2/C3 receipts | ANCESTOR |
| `fff3eea6` | round-58: frozen contract, counters v1, base controls, retained sources, pre-append mirror | ANCESTOR |
| `cc8da167` | round-58: w1 spec/dispatch (one v2 wave, 68 seats), span helper | ANCESTOR |
| `1c0aa211` | round-58: w1 results (68 reports); counters v2 frozen before data | ANCESTOR |
| `c1e39ef3` | round-58: build — resolver fence/NUL fix, receipt ledger, S423/S424, lesson | ANCESTOR |
| `0ffbabff` | round-58: r1 residual attack dispatch, eight reviewers/critics | ANCESTOR |
| `1b009b74` | round-58: T1 C1 receipt, measured claims, scorecard and log, residual reviews | ANCESTOR |
| `0440485` (base) | round-57: hyaku run-8 orchestrator salvage of a late seat artifact | ANCESTOR |

Also checked against the round-58 closure commit `9892ea4ab42d305adb408905a3f19f7b7109f095` as branch: same 10/10 ANCESTOR, exit 0.

**2. Round-58 SCORECARD section hashes — PASS (exit 0).** Section `## Round 58 — declared and measured claims` (lane `SCORECARD.md` lines 4379–4409, the only Round 58 heading in that file) extracted verbatim to scratch and scanned: `cited=7 landed=7 missing=0 unknown=0`.

| Cited hash | Subject in lane | Status |
|---|---|---|
| `044048597d62f3199494b63b36e90dd57825e350` (base) | round-57 salvage commit | ANCESTOR |
| `fff3eea6` | round-58 frozen contract/counters v1 | ANCESTOR |
| `1c0aa211` | round-58 counters v2 frozen | ANCESTOR |
| `c1e39ef` | round-58 build | ANCESTOR |
| `8d340c15` / `8d340c15200959190ba3e894399cdc931976331f` | round-58 fidelity corrections | ANCESTOR (one commit, two forms) |
| `de7d96e720522ea15fba3fd9ee3ce58c42596031` | round-58 T0 measurements | ANCESTOR |
| `32754df` | round-57 build revision X | ANCESTOR |

The fleet-root `/home/vgpnk/Projects/shokunin/SCORECARD.md` (protocol-owned) contains **no** round-58 section — 0 matches for `round-58`/`Round 58`; the lane SCORECARD is the only scorecard holding round-58 hashes.

**3. Independent re-derivation (not trusting the tool).** A separate Python pass re-scanned both documents with an independent hex-token regex, resolved each token with `git cat-file -t`, and tested `git merge-base --is-ancestor <h> master`: report 13 token spellings → 10 distinct commits, all ancestors; SCORECARD section 8 spellings → 7 distinct commits, all ancestors. **No token under 7 hex chars in either document resolves to a lane commit** (no short-hash blind spot), no hex run >40 chars, and no `sha-1/sha256/md5/blake2/digest` label appears on any cited line (no digest-suppression).

**4. Tool behaviour probes (false-green hunting) on a scratch fixture** (`git init -b master`, toplevel asserted, commits with `-c user.name=selftest -c user.email=selftest@local`, deleted after):
- side-branch commit + two master commits in one report → `NOT-ANCESTOR` for the side commit, `cited=3 landed=2 missing=1`, **exit 1** — detection works, no false green;
- same side commit cited by 8-char prefix → `NOT-ANCESTOR`, `cited=1 landed=0 missing=1`, **exit 1**;
- blob + tree cited → `cited=0 landed=0`, **exit 2** (non-commit objects are skipped, and the tool refuses to exit 0 on zero landed);
- wrong repo (fleet root instead of lane) → `cited=13 landed=0 unknown=13`, **exit 2** — a mis-pointed `--repo` cannot produce a false pass;
- branch that does not resolve → **exit 2**.

**5. Round-58 report content corroborated against lane state (read-only):**
- "Landed changes" table commit → real lane subject: all 9 rows map to the exact commits/subjects listed in the table (`fff3eea6`…`9892ea4a`).
- Report's "final lane tip `9892ea4a` (remote `refs/heads/master` verified)": `origin/master` reflog shows `9892ea4` as the pushed tip at 21:57:03 -0300, and the fleet report commit is `8f8c5365` at 21:57:59 -0300 — the tip claim was true when written. `master` has since advanced 3 commits (`fd6303c` round-58 verifier spot-check, `45a92b6` round-59 contract, `cb68527` round-59 w1 spec); all cited hashes remain ancestors, so the check stays green. Fleet root: `git status --porcelain` empty, report file unmodified vs `HEAD`.
- Receipts exist at the cited revisions: `controls/base-c1-receipt-rewrites-v2.txt`, `base-c2-resolver-cases-v2.txt`, `base-c3-quote-truth-v2.txt` land at `8d340c15`; `after-c2-resolver-cases.txt` + `after-c3-quote-truth.txt` land at `de7d96e7`; `after-c1-receipt-rewrites.txt` lands at `1b009b74` (the C1 after-receipt was committed after its own run, exactly as the SCORECARD discloses: "The C1 receipt itself was committed after its run").
- Receipt contents match the report's before/after numbers: base `events=19 undisclosed=19 met=False` / `6/14 met=False` / `0/8 met=False`; after `undisclosed=0 … new_receipts=2 met=True` / `14/14 met=True` / `8/8 met=True`. After-receipts name the measured revisions `de7d96e7…` (C1) and `8d340c15…` (C3).
- `census-before.txt` and `census-after.txt` are byte-identical (15 lines: 14 W04 + 1 `ok`), exit files `0`/`0` — the report's "160→162 rows, same 14 W04" is consistent (registry rows at `0440485` = 160, at `8d340c15`/`de7d96e7`/now = 162).
- Wave shape: `w1-results.json` = 68 seats, role mix {executor 23, scribe 10, reviewer 9, critic 8, scout 7, mutation-tester 4, connector 3, sentinel 2, simplifier 1, revenger 1} — exactly the report's stated mix; `r1-results.json` = 8 seats {reviewer 5, critic 3} — matches "5 reviewer, 3 critic"; 68+8 = 76 = the report's total. All 8 `r1/*.md` reviewer/critic files present.
- Round-58 corpus lesson `corpus/lessons/round-50.md` cites `e80f84d…`, which is **not** an ancestor of `master` — but that is the lesson's own documented point (`remotes/origin/wip/operator-save-20261023` is unmerged by operator design, `merge-base --is-ancestor` exit 1 recorded in the text), pre-dates round-58, and is not a round-58 citation. Not counted as a defect.
- `scripts/id_resolver.py --selftest` at the current tree → `selftest: 59/59`, exit 0 — the report's stated C2 tool selftest count still holds.

**6. Wider sweep (context, not a round-58 defect).** All 238 `*.md` files under `.ufo/waves/round-58/` were scanned: 73 returned non-zero, and every one is explainable and outside the report/SCORECARD scope — 47 are mirrored corpus/lesson copies under `assimilation/` that are byte-identical to live corpus files (the one NOT-ANCESTOR there is item 5's documented operator-save pointer), 23 cite non-commit hex (sha256 of mutants, `cdnversion=…` query strings, dates) which the tool correctly does not count as commit citations, and 13 are seat reports with no commit hash at all (exit 2 = zero landed, not a false pass). No round-58 seat report contains an unresolvable *commit* citation.

## RISKS / BLIND SPOTS (disclosed, not defects in the checked documents)

- The tool only sees tokens of 7–40 hex chars; a report citing a 6-or-fewer-char hash is silently ignored. Verified absent from both round-58 documents (independent scan found no 4–6 char token resolving to a lane commit), but it remains a class for future rounds.
- A report whose only hex tokens are non-commit objects exits 2 with `cited=0`; a caller that checks only "no exit 1" could misread exit 2 as a pass. Both documents here yield cited>0.
- `--repo` must point at the lane, not the fleet root: pointing it at the fleet yields `unknown=13`, exit 2 (loud), so the misuse is not silent.
- `landed_check` proves ancestry only; it cannot detect a cited hash that is an ancestor but whose *content* differs from the claim. Section 5 addresses that for round-58 by re-deriving the numbers from the receipts at the cited revisions.

## FILES

- Report written: `.ufo/waves/round-59/w1/ExecLandedCheck.md` (this file). No other lane path written; no git/jj mutation; scratch `/fast/scratch/hyaku/kake-r59/ExecLandedCheck/` removed on completion.
- Tools installed/updated: **none**. No pacman transaction (host-wide pacman guard respected).

VERDICT: PASS — every hash cited in the round-58 kake report (10/10) and in the round-58 SCORECARD section (7/7) is an ancestor of lane `master`, landed_check exits 0 on both, and independent re-derivation plus receipt/registry/role-mix corroboration confirms the round-58 landing claims.
