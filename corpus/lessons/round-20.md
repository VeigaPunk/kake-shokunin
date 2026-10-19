# Round 20 attempt — citation-local absence evidence

Date: 2026-10-15. One interactive L1, lowest LIVE axis tie resolved to
freshness. Status: **blocked / unadmitted**; zero new verified-round credit.
The preceding headless launch counter 16 is not a completed-round count.
Round-19 history through `20d13115323fba21bb3d63204cce13425feaf399` is preserved.
See the appended round-20 reconciliation in `LOG.md` and
`plans/wwkd-round-20-citation-locality.md`.

## Trigger → action → outcome

Round 19's re-census lesson names stale publishing-tool instructions. The
inherited scanner patch addresses the cause: target-wide OR allowed a
historical note to hide an unannotated citation of the same deleted target.
The interactive L1 retained the per-citation evidence sets, simplified the
new diagnostic, and removed an incidental first-evidence ordering assertion
from the inherited regression case. Path grammar, local annotation windows,
strict mode, pins, history and publishing gates are unchanged.

The actual CLI was run against isolated publishing fixtures on both the
committed baseline and candidate. Full argv/stdout/stderr/exit records:
`.ufo/round-20/baseline-proof.json` and
`.ufo/round-20/candidate-proof.json`. Input bytes, digests and expected
findings: `.ufo/round-20/frozen/citation-locality/expected.json`.

| Case | Baseline exit | Candidate exit | Observable |
|---|---:|---:|---|
| Mixed annotation, already-pinned miss | 0 | 1 | Only `SKILL.md:3` is unannotated; no new miss-set member. |
| All occurrences annotated | 0 | 0 | Declared absence remains exit-neutral. |
| Existing target, mixed prose | 0 | 0 | Target resolves; annotation does not override existence. |
| Distant occurrences in one file | 0 | 1 | The unannotated location is `SKILL.md:9`. |
| Home-alias spellings | 0 | 1 | One canonical target, exact unannotated location. |
| Brace-expanded targets | 0 | 1 | Both expanded targets retain their unannotated originating location. |
| Strict local annotation mode | 0 | 1 | Direct historical evidence elsewhere cannot hide the unannotated occurrence. |

Human CLI smoke also reported `1 of 2 cites unannotated: SKILL.md:3` and
`VERDICT: DRIFT — §paths: 1 unannotated miss · 0 NOT in pins.pathsMissSet (exit 1, gates inert)`.
The fixture intentionally pins only the checks under study; the inert-pin
warning is retained, not removed from the evidence.

## Gate

Candidates considered:

- **Locally admitted implementation fact:** missing-target annotation
  coverage must hold at every citation location. Both controls stayed clean;
  exact finding locations are observed in the CLI evidence.
- **Locally admitted quality criterion:** a pinned missing target is not an
  exemption for a newly unannotated instruction. Added to `corpus/QUALITY.md`.
- **Rejected:** restore green by re-pinning old misses, borrowing absence
  evidence across occurrences, or declaring deleted tools executable.
  These do not address the reproduced false-green.
- **Rejected:** treat canonical plan/render success as a dispatched wave or
  native judgment. `.ufo/round-20/wave/validation.json` records 32 distinct
  scopes, 32 leading Godspeed invocations, zero native task calls, and no
  registry persistence. No route mutation or substitute dispatch occurred.

Outside spot-check: **unavailable**. No independent non-author verifier has
reviewed an admit and reject. No promotion box or discernment improvement is
claimed. The local code evidence is not full round admission.

## Named debt and unblock

- **Dispatch / host owner:** bind existing content roles to `@m_composer`,
  audit roles to `@m_grok`, connector to `@m_antigravity` with `@m_zfl`
  fallback, outside this lane's write authority. Effective observations and
  exact mismatches: `.ufo/round-20/routing-blocker.json`. Then a fresh session
  may dispatch the saved complete canonical wave; never a shortened wave.
- **Corpus / kake:** use P1's unannotated-location diagnostics to qualify or
  repair the stale recipes without blanket markers or miss-pin suppression.
  The retained local annotation heuristic still permits unrelated words
  within its ±2-line window; this round does not claim semantic freshness.
- **Publishing-source / operator:** restore or explicitly retire the deleted
  PQ-2/PQ-14 source watches. **History / operator:** restore a surviving
  history source or explicitly end the old probe-timer era. No current live
  HTTP state was measured under this local-only dispatch.
- **Static self-source proof / kake:** round-19's independent audit already
  reports a confinement-assertion weakness. It was not re-probed or repaired
  here; a passing selftest is not a complete write-free proof.
- **Receipt / integrator:** a Sighting run/session identity is known, but no
  applicable queue task/expected receipt binding has been supplied by this
  interactive dispatch. Do not invent one or call Sighting `complete`.

## Local acceptance measured after integration

`node .ufo/round-20/replay-proof.mjs` verifies every frozen input digest
before comparing the real baseline and candidate CLIs:
`CITATION_LOCALITY_PROOF: PASS (cases=7, failures=0)`, exit 0.
The isolated-HOME `--selftest` returned `selftest: 14/14 passed`, exit 0.
Full commands, complete outputs and exits: `.ufo/round-20/acceptance.json`.

The baseline program was also run against the **same candidate corpus**
(not presented as a historical corpus snapshot): exit 0, drift 0,
declaredAbsent 55. Candidate path gate: exit 1, drift 7 targets containing
26 locally unannotated locations, declaredAbsent 48, newMissing 0.
`same-surface-baseline.json`, `citation-debt.json`, and
`measured-corpus-inputs.json` under `.ufo/round-20/` carry the comparison,
actionable locations and hashes of the 43 measured markdown inputs.
These hashes describe the acceptance input surface before this bookkeeping
append, not a later unmeasured commit.

```text
VERDICT: DRIFT — §paths: 7 unannotated miss · 0 NOT in pins.pathsMissSet (exit 1)
VERDICT: DRIFT — §paths: 7 unannotated miss · 0 NOT in pins.pathsMissSet (exit 1, partial: offline)
```

Both commands exited 1. Offline explicitly suspended history and skipped
all remote armed checks; neither skip is a passed check. The red gate is
the exposed annotation debt, not a repaired source or a new miss-pin member.
The 26 heuristic locations are not asserted to equal round 19's manual
live-claim population: the scanner measures a different, explicit contract.

Receipt metadata was checked read-only in the selected Sighting manifest
row and its nested dispatch object: run/session identities exist, but no
task key, expected bag or receipt/result paths. The dispatch object has only
`argv` and `kind`; argv contents were not inspected. Evidence:
`.ufo/round-20/receipt-binding.json`. No mint or `complete` call was made.

Local axis verdicts: freshness improved, operability unchanged. Learning:
expansion unchanged, quality improved locally, discernment unchanged.
All remain provisional because no compliant wave or independent non-author
spot-check ran; this attempt is blocked, not a completed training round.

## Shape-only evidence erratum

Review rejected the initial evidence representation in
`f405166a33878cab32bff18dce3f39c9d9d3e463`: controlled fixture environment
values were serialized and echoed through captured output; the SKILL
selftest command also embedded assignments. Their lane-local origin does
not exempt them from this dispatch's shape-only rule.

A follow-up correction substitutes symbolic paths in captured output and
keeps override variable names plus isolation shape, not assigned values.
Ordinary frozen fixture metadata remains replayable. The output references
above now mean shape-sanitized output with **unchanged full verdict lines
and exit codes**, not byte-verbatim streams. Structured JSON parsing and
before/after verdict comparison passed:
`.ufo/round-20/redaction-validation.json`. No runtime program changed.

The rejected representation grounds the added `corpus/QUALITY.md` criterion.
The original commit is preserved as a recorded conformance defect, not
rewritten or asserted scrubbed. This correction earns no verified round
or independent promotion/learning attestation.


## Round-20 resume (2026-10-19, kaika campaign)

Fresh-session resume of this same round (`LOG.md:542`), not round 21. Base
`cb807bc`. The L2 swarm the 2026-10-15 attempt could not dispatch ran this
time: one batched call of 10 seats (planner, connector, scout, scribe,
reviewer, critic, 4 executors), a provider-forced executor re-dispatch, and a
3-seat post-land review (`.ufo/round-20/resume/swarm-dispatch.json`).

### Trigger → action → outcome

- **C1 freshness.** Trigger: the round-20 gate's own debt — 7 deleted targets
  cited at 26 locally unannotated locations (`.ufo/round-20/resume/paths-before.txt`).
  Action: each location annotated in place naming the exact target, its dated
  absence event (W6 2026-09-29 consolidation, W7 2026-10-12 prune, or the r15
  23:51:31Z drift event) and "historical record, not executable"; zero
  repairs (no surviving equivalent path exists); pins untouched. Outcome:
  `node scripts/freshness-sweep.mjs --section=paths` exit 1 → 0, drift 7 → 0,
  missSet 55 → 55, newMissing 0 (S014). Ledger:
  `.ufo/round-20/resume/citation-disposition.json`.
- **C2 operability.** Trigger: the r19 audit erratum (`round-19-recensus.md:44`).
  Action: `writeConfinement()` parses exact standalone markers, errors on
  unbalanced/nested/unterminated ones, covers 15 more write APIs; new case
  `e2` plants a write at every out-of-region top-level function in memory.
  Outcome: selftest 14/14 → 15/15; process-level replay
  `node .ufo/round-20/resume/confinement-mutants.mjs` → `cb807bc` killed 0/25,
  working tree killed 25/25; replay-proof still PASS (7/7). Residual
  bypasses named: aliasing, bracket access, child-process writes
  (`.ufo/round-20/resume/confinement-reviewer-recipe.txt`: execFileSync
  survives on both revisions).
- **C3 capability.** Trigger: ART dossier K1–K3 contradictions of standing
  claims. Action: `corpus/SOURCES.md` (18 opened rows), four knowledge
  entries (`ghp-served-set`, `ghp-custom-domain`, `ghp-etag-anatomy`,
  `crawl-scope-per-host`), 27 appended `r20-correction` tails across 7 files (every mention of the two
  superseded claims, not only the 9 literal lines).
  Outcome: contract census clean; superseded literals left uncorrected 9 → 0.

## Gate — round-20 resume

Admitted: the four knowledge entries above (each opens with `source:`,
`verified-at:`, `recheck:` and maps to `corpus/QUALITY.md`); seven new
`QUALITY.md` criteria; the C2 checker. Rejected: S017 (Astro's `public/CNAME`
step as the Actions custom-domain mechanism — contradicted by S005) and S018
(DebugBear's "Firefox 114" — Firefox 144.0 release notes carry
`interactionId`); re-pinning `pathsMissSet` to go green; claiming the checker
covers "every write" (child-process writes survive). Not admitted: the
scout's eight "refined/unverifiable" GHP observations
(`ghp-subpath-spotcheck.md:24-26,39-41,65-82`, `round-6.md:33-34`) — they need
a live read or a further source, so they stay frontier, not corrections.
Outside spot-check: still owed — the orchestrator re-opens ≥3 rows and one
admit/reject after landing; the post-land reviewer/critic are dispatched
subagents, not non-author verifiers.

Every new SOURCES row (contract rule 1; full records in
`.ufo/round-20/resume/sources-gate.md`):

| id | URL (accessed 2026-10-19) | quote (≤25 words) | location |
|---|---|---|---|
| S001 | https://raw.githubusercontent.com/actions/upload-pages-artifact/5f327015a708106f6f1b7c9a633901af30fe80cb/action.yml and https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml | “Include hidden files and directories (those starting with a dot) in the artifact. Excludes .git and .github regardless.” | `inputs.include-hidden-files` description, lines 17-18; archive behavior lines 37-39; main commit `5f327015a708106f6f1b7c9a633901af30fe80cb` and v4.0.0 tag commit `7b1f4a764d45c48632c6b24a0339c27f5614fb0b`. |
| S002 | https://github.com/actions/upload-pages-artifact/releases/tag/v4.0.0 and https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0 | “Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact”; “feat: add `include-hidden-files` input” | v4.0.0 release, “What's Changed”; v5.0.0 release, “Changelog”; v4 tag commit `7b1f4a764d45c48632c6b24a0339c27f5614fb0b`, v5 tag commit `fc324d3547104276b827a68afc52ff2a11cc49c9`. |
| S003 | https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site | “You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.” | “About publishing sources”; fetched 2026-10-19. |
| S004 | https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages | “compressed `gzip` archive containing a single `tar` file”; “under 10GB in size and should not contain any symbolic or hard links” | “Configuring the `upload-pages-artifact` action”; first and second paragraphs; fetched 2026-10-19. |
| S005 | https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site | “any existing `CNAME` file is ignored and is not required.” | “Configuring an apex domain,” step 4; fetched 2026-10-19. |
| S006 | https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll | “Are located in a folder called `/node_modules` or `/vendor`”; “Start with `_`, `.`, or `#`”; “End with `~`” | “Configuring Jekyll in your GitHub Pages site,” default exclusions; fetched 2026-10-19. |
| S007 | https://docs.github.com/en/rest/pages/pages | “`cname`: required, string or null”; “`protected_domain_state`: string or null”; “`build_type`: string or null” | “Get a GitHub Pages site,” response schema; fetched 2026-10-19. |
| S008 | https://cgit.git.savannah.gnu.org/cgit/tar.git/plain/doc/tar.texi?id=cfdb891bbd68c920ea75210977593f3cd08f0418 | “Default is `@option{--no-anchored}` for exclusion members”; “When wildcards match slash (the default for exclusion members)” | “Controlling Pattern-Matching,” anchored patterns and `--wildcards-match-slash`, lines 8478-8603; GNU tar master commit `cfdb891bbd68c920ea75210977593f3cd08f0418`. |
| S009 | https://raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c | `etag->value.len = ngx_sprintf(etag->value.data, "\"%xT-%xO\"", r->headers_out.last_modified_time, r->headers_out.content_length_n)` | `ngx_http_set_etag`, `src/http/ngx_http_core_module.c:1708-1710` (L1 re-verified 2026-10-19 with `grep -nF` at commit 481d28cb; the writer's 1671-1673 was wrong); release tag `release-1.28.0`, commit `481d28cb4e04c8096b9b6134856891dc52ecc68f`. |
| S010 | https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8 | “An entity tag is an opaque validator”; “A strong validator might change for reasons other than a change to the representation data” | Section 8.8.1, “Weak versus Strong,” and 8.8.3, “ETag”; RFC 9110, June 2022. |
| S011 | https://www.rfc-editor.org/rfc/rfc9309.html | “The rules MUST be accessible in a file named "/robots.txt" (all lowercase) in the top-level path of the service.”; “crawler MUST assume complete disallow” | Section 2.3, “Access Method,” and Section 2.3.1.4, “Unreachable Status”; RFC 9309, September 2022. |
| S012 | https://www.sitemaps.org/protocol.html | “The location of a Sitemap file determines the set of URLs that can be included in that Sitemap.” | “Sitemap file location”; fetched 2026-10-19. |
| S013 | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap | “unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent directory.” | “Sitemap best practices”; page last updated 2026-07-08 UTC. |
| S014 | `scripts/freshness-sweep.mjs`; command: `node scripts/freshness-sweep.mjs --section=paths` | “Annotation window = the citing line ±2 (spec), with every *citation* on the citing line blanked” | `scripts/freshness-sweep.mjs:404-411`; command selection and §paths execution at lines 1021-1044. The opened command reported 7 unannotated missing paths and exit 1 before the citation repair landed. |
| S015 | https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits | “Published GitHub Pages sites may be no larger than 1 GB.” | “Usage limits”; fetched 2026-10-19. |
| S016 | https://pages.github.com/versions.json | `"jekyll": "3.10.0", "github-pages": "232"` | JSON keys `jekyll` and `github-pages`; fetched 2026-10-19. |
| S017 | Astro Docs https://docs.astro.build/en/guides/deploy/github/; GitHub Docs cross-check https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site | “Add a `./public/CNAME` record to your project.”; “any existing `CNAME` file is ignored and is not required.” | Astro “Change your GitHub URL to a custom domain,” step 2; GitHub Docs “Configuring an apex domain,” step 4; fetched 2026-10-19. |
| S018 | DebugBear https://www.debugbear.com/blog/firefox-safari-web-vitals; Firefox release notes cross-check https://www.firefox.com/en-US/firefox/144.0/releasenotes/ | “Mozilla released version 114 of Firefox on the 14th of October 2025.”; “Firefox now supports the PerformanceEventTiming.interactionId API, allowing developers to group related input events.” | DebugBear “INP support in Firefox 114”; article updated 2026-03-19. Firefox “144.0 Firefox Release,” “Web Platform,” released 2025-10-14. |

Post-land review (dispatched reviewer, critic, mutation-tester; not
non-author verification): the mutation probe killed 9/18 checker mutants, so
`e2` was hardened before commit — every covered API name planted (31/31,
list pinned by count + sorted sha256 prefix), nested-BEGIN / lone-END /
trailing-junk marker fixtures, a suffix-named-call decoy, regions required
inside `selftest()`; all 8 re-run survivors plus a region-in-`main()` mutant
now fail the selftest (`.ufo/round-20/resume/confinement-mutation-probe.txt`).
The critic's C1 point that HTML-comment warnings vanish in rendered Markdown
was taken: the 26 notes are now visible italic tails (inside the last cell on
table rows, which also repaired the header at `drift-detection.md:73`). The
reviewer's off-line note: the `publish-queue.md:262` annotation sits on line
264, inside the ±2 window. Header and residual comments in the script now
name what the static check does not cover (aliases, bracket access,
multi-line calls, metadata/fd writes, child-process writes).

Rows touched old→new: none (all 18 rows are new this round). Pre-commit fix:
the S009 anchor was written as lines 1671-1673 (copied from the W1 lead); the
L1 re-ran `grep -nF '%xT-%xO'` at commit `481d28cb` and found 1708-1710.

## Mistakes

Mined by the scribe seat at base `cb807bc` (pointers verified with
`git show cb807bc:<path> | grep -nF`; sweep commands in
`.ufo/round-20/resume/mistakes.md`). "none" means no criterion existed at base.

| # | Class | Evidence pointer (base lines) | Captured-by | Fix |
|---|---|---|---|---|
| M1 | False green in the citation gate: target-wide OR let an absence note on one occurrence hide an unannotated instruction elsewhere | `corpus/lessons/round-20.md:12-18,28-34`; `corpus/QUALITY.md:9` | `Citation-local absence` (`corpus/QUALITY.md:9`) | C1: annotate/repair all 26 measured locations in place; `pathsMissSet` stays 55, `newMissing` stays 0 |
| M2 | Shape-only evidence violation: controlled fixture environment values serialized, then echoed through captured output | `corpus/lessons/round-20.md:124-143`; `LOG.md:544-559`; `corpus/QUALITY.md:13` | `Shape-only probe environment` (`corpus/QUALITY.md:13`) | Closed by correction `9825b2a` plus append-only erratum; C1–C3 keep symbolic output only |
| M3 | Authority inflation: 32 rendered scopes treated as a dispatched wave; launch counter 16 treated as completed rounds | `corpus/lessons/round-20.md:5,53-60`; `LOG.md:470-489`; `corpus/QUALITY.md:12` | `Admission authority` (`corpus/QUALITY.md:12`) | No dispatch in-lane; named debt, owner host owner/integrator (`routing-blocker.json`) |
| M4 | Self-source confinement: write-region scanner opened on prose/literal BEGIN tokens, so a write planted in a later function survived the selftest | `corpus/lessons/round-19-recensus.md:44`; `SKILL.md:212` (gate-registry row only) | `none` | C2: standalone marker lines plus a permanent mutation case for an out-of-region write |
| M5 | Dead-path population units conflated: 77 live citations vs 8 fleet-level hits vs 26 unannotated locations are different contracts | `corpus/lessons/round-19-recensus.md:52-53`; `corpus/lessons/round-20.md:110-111` | `none` | C1 closes only the 26-location contract; 77/8 reconciliation is named debt, owner kake |
| M6 | Stale live counts/prose beyond the named sites; "every `origin-work` cite is marked" was false | `corpus/lessons/round-19-recensus.md:48`; `SCORECARD.md:32,64` | `SKILL.md:199-203` (counts are dated measurements) | Historical-qualified (`SCORECARD.md:32`); citation half handled by C1; count repair is named debt, owner kake |
| M7 | Clock mix: journal `Starting` line written as the history `at` | `LOG.md:31-33` | `none` | Closed by append-only r14 erratum (`LOG.md:31-33`); no code change |
| M8 | "Byte-frozen" misclaim: raw sha varies per fetch via Cloudflare cfemail re-encoding | `LOG.md:42-44` | `none` | Closed by erratum naming the cfemail-normalized sha (`LOG.md:44`); no rewrite |
| M9 | Journal start-time misread: `03:32:06` recorded, `04:14:50` correct | `SCORECARD.md:74` | `none` | Closed by append-only correction; move-log row 10 records it |
| M10 | Proposed cmdProbe F1 merge guard refuted on `probe <id> --all`; corrected rather than shipped | `SCORECARD.md:72`; `corpus/handoffs/cmdProbe-merge-fix.md:5-10` | `none` | Closed by handoff/refutation record; guard was not shipped |
| M11 | No independent non-author spot-check of one admit and one reject | `corpus/lessons/round-20.md:58-60`; `SCORECARD.md:112` | `Admission authority` (`corpus/QUALITY.md:12`) | Named debt, owner host owner/operator; cannot close in-lane |
| A1 | Validator treated as identity: an ETag flip read as content change, then "refuted" by a fetch that hit another replica | `corpus/knowledge/publish-queue.md:255-261`; `LOG.md:245-247`; `corpus/lessons/round-16.md:35-38` | `none` | C3: S009/S010 rows plus `ghp-etag-anatomy`; ETag = mtime/length, never a freeze metric |
| A2 | Platform mechanism inferred from workflow shape: the served set equated with the `origin/main` tree (deploy taken as the whole tree) | `corpus/README.md:26,52-53`; `SKILL.md:227`; `corpus/lessons/round-7.md:21-25`; `corpus/knowledge/sitemap-orphan-audit.md:20-24` | `none` | C3: S001/S002/S003/S004/S006/S008 rows plus `ghp-served-set`; annotate `round-7.md` append-only |
| A3 | Repo file read as platform configuration: the repo CNAME file taken as what sets the ds4cc.com domain | `corpus/knowledge/publish-channels.md:9`; `SKILL.md:16` | `none` | C3: S003/S005/S007 rows plus `ghp-custom-domain`; correct both sites |
| A4 | Tier-B version number admitted: Firefox 114 vs Firefox 144.0 `interactionId` | `ART:322` (R3), `ART:334` (M4) | `none` | C3 registry admits tier A only; S018 rejection retained; no lane claim depends on the number |
| T1 | Index continuation silently dropped by an edit; sentence ended at "intentionally" | `corpus/README.md:60`; `dd4eabf:corpus/README.md:45`; `cd5b381:corpus/README.md:27-28` | `none` | Restored this round from `cd5b381` (worktree `corpus/README.md:61-63`, uncommitted at write time) |

New this round (L1-observed, before commit):

| # | Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|---|
| R1 | Source line anchor copied from a lead, not re-derived | S009 anchor 1671-1673 / entry 1677-1679 vs `grep -nF` → 1708 at `481d28cb` | `Replayable claim` (partly) | Anchors re-derived by grep at the pinned commit; three files corrected pre-commit |
| R2 | Append-only text altered while appending | executor added a backtick in `round-4-aggregator-audit.md:31` and dropped two table-row pipes (base `SKILL.md:227`, `corpus/README.md:26`) | none | L1 stripped-diff check (every base line survives once tails are removed) restored them; new criterion `Append-only tails` |
| R3 | Duplicate writer seat after re-dispatch | a peer-id note woke a failed citations seat, which finished while its replacement ran; both wrote `citation-disposition.json` (3 platform entries lost, one duplicated correction; it kept editing after its job was cancelled, adding 5 more tails and an indentation change at `round-7.md:12`) | none (orchestration) | Ledger rebuilt by the L1 from the tails themselves (27 base locations, 0 unmatched); the indentation change reverted; late tails labelled `[INFERENCE]` where the cited rows do not state them |
| R4 | Gate stuffing risk | critic: the sweep accepts any absence word in ±2 lines (fixture F) | `Absence annotation content` (new) | All 26 annotations name target + dated event + non-executable wording (L1 check, 0 failures) |

Criteria added this round capture M4 (Self-source confinement), M5
(Population unit named), A1 (Validator is not identity), A2–A4 (Platform
mechanism), T1 (Index continuity), R2 (Append-only tails), R4 (Absence
annotation content). M7–M10 stay historical append-only corrections.
Environment, not lane: executor seats died on provider limits
(`resource_exhausted`, then `turn_rate_limit_exceeded`) and were re-spawned;
no claim was shrunk.
