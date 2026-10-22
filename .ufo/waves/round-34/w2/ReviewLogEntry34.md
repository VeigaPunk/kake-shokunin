# ReviewLogEntry34 — LOG.md "Round 34" entry at 24a1647 (wave 2, falsify)

Method: sandbox clone at 24a1647 (`/fast/scratch/hyaku/kake-r34/w2/ReviewLogEntry34/clone`);
LOG entry is LOG.md:1414-1447. Every rerun below is mine, not a receipt read, unless noted.
No tools installed; no lane file other than this report touched.

## Per-statement verdicts

All commands run in the sandbox clone; "rerun" = I executed the named script.

1. Base `1e54c89…` — **TRUE.** `git merge-base --is-ancestor 1e54c895 d08d8de` exit 0; `git log`
   shows d08d8de's parent is 1e54c89.
2. Declaration, frozen matrix, both counters, retained sources at `d08d8de` — **TRUE.**
   `git show --stat d08d8de`: c1-matrix.json (523 ln), c1_matrix_count.py, c2_source_census.py,
   sources S067–S072 (+ds4cc-7fc6aa2f archive, receipts.json), 21 files.
3. "Frontier move off the citing-set gate (rounds 31–33 used it…)" — **TRUE for rounds 31–33**
   (LOG:1301,1323 r31 citing-set runner repairs; r32 section: C1 = hostile-selftest guard repair
   on that runner; r33 section: `c1-strict-at-*.json` strict supplement). The trailing "hyaku
   goal-file drift rule" is an external harness rule — **not verifiable from lane bytes** (gap G1).
4. Corpus held no Open Graph knowledge — **TRUE.** `git grep -i 'open graph|og:'` at base hits only
   incidental facts: corpus/knowledge/drift-detection.md:80,109, publish-queue.md:38,181,270,
   lessons/round-16.md:58; no link-preview knowledge entry, no SOURCES row at base. Same nuance is
   disclosed in w1/CriticFrontierNovelty.md.
5. Screening at `7fc6aa2f` (upstream head, unchanged since r33); OG tags on 87/102, og:image on 1 —
   **TRUE.** `git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git HEAD` →
   `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` (exit 0, live GET, github.com reads permitted);
   r33-era clone /fast/scratch/hyaku/kake-r33/ds4cc-upstream HEAD is the same commit; LOG:1394 r33
   recorded upstream at `7fc6aa2f` at round start. Census numbers independently derived by my
   c2 rerun from the retained archive: pages=102, og:title=87, og:type=87, og:image=1, og:url=87,
   all-four=1, og-url-equals-canonical=87.
6. C1 counter 0/28 → 28/28, all four constant gates rejected — **TRUE (rerun).**
   `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root <clone> --revision <rev>`:
   0/28 exit 1 at 1e54c89 and d08d8de (`toolPresent:false`); 28/28 exit 0 at 5613071 and 24a1647
   (`constantGatesAllRejected:true`, toolSha256 8dd0018248e0…d875, matrixSha256 246a6a3ba67a…ac14f7).
7. Selftest 29 fixtures, 29/29 against landed tool — **TRUE (rerun).**
   `python3 -B scripts/link_preview_selftest.py` → `"cases": 29, "failed": 0`, exit 0; matches
   verification/selftest-link-preview-at-5613071-tool.txt (29 caseNames).
8. Entry rows S067–S077 (5 mined, 4 rejected, 2 queued) at `9ef758c`; round-34 lesson there —
   **TRUE.** corpus/SOURCES.md:75-85 holds exactly 11 rows; status cells `| mined |`×5,
   `| rejected |`×4, `| queued |`×2 (grep -o count); 9ef758c diffstat adds the entry, SOURCES rows,
   corpus/lessons/round-34.md; `git diff 9ef758c 24a1647 -- corpus/SOURCES.md` empty.
9. C2 met 0/5 → 5/5 — **TRUE (rerun).** `c2_source_census.py --root <clone> --revision <rev>`:
   0/5 exit 1 at 1e54c89 (entry absent); 5/5 exit 0 at 9ef758c and 24a1647 (S067–S070 checks a–d
   all true; census passed).
10. Census "matched by an independent lxml recount and by the landed tool's real-input run" —
    **TRUE.** w1/ExecCensusIndependentRecount.md: lxml 6.1.3.0 recount agrees on all seven numbers;
    verification/real-input-at-5613071.json: 102 pages, `"agrees": true`, observed
    og:image-missing 101 / title-type-url 15 each = census.
11. Round-33 routed defects: retained at `a2fe31b`; Gate records four rejects; two checks able to
    fail; hollow shapes carried by name — **TRUE.**
    - a2fe31b diffstat: r33-c1-counterexample-489714be.bundle + 2 option-table patches.
    - round-34.md `## Gate` (lines 25-60): 4 reject bullets (S071, S072, S074, S075), each with a
      located quote/reason; 5 admits, 2 queues.
    - Reruns: `gate_reject_check.py --repo <sandbox> --rev 93359ff --lesson corpus/lessons/round-33.md`
      → exit 1 "NO MATCH…"; `--rev a2fe31b2 --lesson corpus/lessons/round-29.md` → exit 0 (found
      S044 reject at round-29.md:56). `receipt_presence_check.py --report <my tmp report with a
      Before/After table naming 93359ff> --repo <sandbox> --rev 93359ff --round 33` → exit 1
      "unreceipted hashes: 93359ff", byte-identical to verification/criterion-receipt-presence-r33-report.txt.
      (First two synthetic attempts exited 2: the check requires a header containing both "before"
      and "after" — parser at receipt_presence_check.py:93-103.)
    - Hollow shapes: retained/r34-c1-lookup-dcef39b5.bundle and r34-c2-hollow-0cce15f0.bundle exist
      at 24a1647.
12. Mistake row: C1 lookup `dcef39b5` 28/28; C2 transcription `0cce15f0` 5/5 — **TRUE.**
    Rerun `lookup_control_check.py --counter <clone>/.ufo/waves/round-34/c1_matrix_count.py
    --repo <sandbox-with-bundle-fetched> --control dcef39b5f4e8…` →
    `{"score": 28, "total": 28, "verdict": "FAIL: control reaches the full score"}`, exit 1
    (matches verification/criterion-lookup-control-c1-dcef39b.txt). C2: receipt
    verification/c2-at-critic-hollow-0cce15f.json shows met 5/5 at 0cce15f0719a… (receipt read, not
    rerun — the hollow commit lives only in the retained bundle; not independently rerun, gap G2).
13. QUALITY round-34 criterion (d) with lookup_control_check, exit 1 on frozen C1 counter — **TRUE.**
    corpus/QUALITY.md round-34 criteria, 4th bullet ("A counter scores a lookup-table control below
    its full score…") names the check and the exit-1 receipt; my rerun reproduced exit 1.
14. Seat boundary: `MutC2CounterConditions` wrote into lane corpus/SOURCES.md and removed the rows;
    restored hash equals `a2fe31b`; committed 9ef758c file holds the L1's rows — **TRUE as
    evidenced.** Self-disclosure w1/MutC2CounterConditions.md:31 states restored sha256
    `836166c3d91f66…dca`; my `git show a2fe31b:corpus/SOURCES.md | sha256sum` =
    `836166c3d91f6605507d87fca82e3b3ef83333fb9114023acd5201e617095dca` — exact match. The transient
    write itself is not re-observable (gap G3); no lane git state was harmed per disclosure.
15. Wave 1 `kake-r34-w1`: 32 seats (10 executor, 7 scribe, 5 scout, 4 reviewer, 3 critic,
    2 mutation-tester, 1 connector), all returned — **TRUE (counts); "all returned" corroborated
    only.** w1/swarm-registry.json `members` (dict, 32): executor 10, scribe 7, scout 5, reviewer 4,
    critic 3, mutation-tester 2, connector 1 — exact match, sum 32. Registry member records carry
    only {agentId, role, axes, item, milestone, kind:"spawn"} — **no return/status field**; I
    verified 32/32 committed w1/*.md reports, one per seat (incl. 7 scribes: ScribeEntryDraft,
    ScribeSourcesRows, ScribeMistakeMine, ScribeQualityCriteria, ScribeSkillTable,
    ScribeProvinceReadme, ScribeCarriedOpenNames). Named seats ExecLinkPreviewGate,
    ExecLinkPreviewSelftest, CriticFrontierNovelty, ScribeEntryDraft, MutC2CounterConditions all
    present with matching roles.

## Findings

- F1 (minor, wording): "all returned" is not decidable from the committed registry (spawns only);
  the honest reading is "32/32 seats have committed wave-1 reports". Suggest the next LOG entry
  cite report-file presence, or registry schema grow a returned field.
- F2 (nit): LOG cites the criterion scripts as `criteria/…py`; actual paths are
  `.ufo/waves/round-34/criteria/…py`. Shorthand is unambiguous in context.
- No false statement found in LOG.md:1414-1447. Numbers, hashes, role mix, and rerun scores all
  reproduce.

## Residual risk and gaps

- G1: "hyaku goal-file drift rule" — external rule, not in lane; unverified.
- G2: C2 5/5 on hollow control `0cce15f0` rests on the committed receipt plus wave-1 disclosure
  (bundle not independently replayed); C1 side I did replay (exit 1).
- G3: the MutC2CounterConditions transient lane write is evidenced by self-disclosure + exact
  restored-hash match; the event itself is in the past.
- Not verified: whether every w1 report's content is accurate (out of my seat's scope; siblings
  cover individual reports); ds4cc census derivation beyond the two agreeing counters + lxml report.

Sandbox artifacts: /fast/scratch/hyaku/kake-r34/w2/ReviewLogEntry34/ (clone at 24a1647,
tmp/LOG-at-24a1647.md, tmp/withprereq [clone + fetched lookup bundle], tmp/fake-report4.md).
