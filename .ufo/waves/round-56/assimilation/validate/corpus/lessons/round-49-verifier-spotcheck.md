# Round 49 verifier spot-check

author: hyaku closure (non-author integrator, Kimi fresh closure agent)

Reviewer is a fresh Kimi closure agent, not an `@m_swe` session and not a seat this lane dispatched. This file verifies; it does not improve the round. Round tip checked: `b3ae50efbca6c569720887b03f3fad7710abde8a`. Measured claim commit: `1c846ed2d67b1692ea966be064f0fc04542763c6`. Pre-append commit: `99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9`. Base: `090ce8f1cfbae2dfb8bfa65dedd2c72861c48166`. Report: fleet `5cff012cf608026faf38fcc7a0e0368481231c81`.

## Conformance

- Report commit `5cff012cf608026faf38fcc7a0e0368481231c81` is `kake-shokunin <kake@shokunin.local>`, subject `round-49: kake report`, dated 2026-10-24 21:41:16 -0300, and is an ancestor of fleet `HEAD` (`127a266909d1016dfb47eb946bcaf5f3bb489216`). It is a real report: Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, and a `SHONEN` heading with four box lines. No `[x]`.
- Lane commits `99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9`, `1c846ed2d67b1692ea966be064f0fc04542763c6`, and `b3ae50efbca6c569720887b03f3fad7710abde8a` exist, are `kake-shokunin <kake@shokunin.local>`, and `git merge-base --is-ancestor` holds against `master`. Parents are linear: `99fa9d3f^` = `090ce8f1`, `1c846ed2^` = `99fa9d3f`, `b3ae50ef^` = `1c846ed2`. `jj-lane.sh state` printed `ahead=0 behind=0 local=b3ae50ef… remote=b3ae50ef…`. `ls-remote origin refs/heads/master` equals the tip. HEAD is detached at that tip.
- Report landed after the lane tip (21:40:38 -0300, then report 21:41:16 -0300). Dispatch digest copied from `.ufo/watchdog.log`: `2026-10-24T21:22:16-03:00 launch kake round=49 pgid=2899645 driver=hyaku-inline attempt=1`; `2026-10-24T21:41:30-03:00 complete kake round=49; hyaku-inline attempt=1`.
- Prompt `.ufo/prompts/kake-round-49.md` carries the template contract: mission/axes binding, 1–3 claims, frontier step, L2 floor, report path, SHONEN heading, commit-hash citation, commit-then-push, push scope, L0 channel, and lane write scope. It does not quote an L2 route map that could contradict `MISSION.md`; routing is deferred to the host table.
- SHONEN is not fully checkable for promotion: box 2 is `[ ]`, and the other three are author `[~]`. Promotion stays operator-owned.
- Claims were re-measured by this reviewer. The lane counters are not a sibling gate; they were executed here because they are the round's own counting commands. Census was re-run. The historical `--file` census is evidence-verified from the committed stdout blob.

### Uncommitted paths (classified, not swept)

`git status --porcelain` shows 10 paths. No tracked path is modified. `jj-lane.sh state` printed `tracked=0 untracked=10`.

1. `.ufo/waves/round-46/residual/` holds eight orchestrator-owned residual reports (`CriticCitationOverreach.md`, `CriticMatrixBlindness.md`, `MutationSemanticsGap.md`, `ReviewQualityCriterion.md`, `ReviewReceiptIdentity.md`, `ReviewWitnessOracle.md`, `ScoutSiblingOverlap.md`, `SentinelBounds.md`). Mtimes are 2026-10-24 03:26–03:37 -0300, before the r49 launch at 21:22:16. Not r49 lane work. Left uncommitted on purpose. Continuing r47/r48 durability item, not lane debt.
2–10. Nine files under `.ufo/waves/round-48/assimilation/validate/` are untracked and each is larger than 1 MiB (1,283,159–4,620,210 bytes): `anchors-fixed.json`, `snap-bodies.tar.xz`, `snap-bodies-run2.tar.xz`, `cases.json`, two `xmlschema11-2.html`, `nodejs.xml`, `postgresql.xml`, `ctl_accept_table_seed4242.py`. Each is byte-identical (`cmp -s`) to the already-tracked source path. Mtimes are 2026-10-20 through 2026-10-23, before this launch. Not swept.

The handoff's "eight residual reports and nine >1MiB copies" matches these 10 porcelain paths (one directory of eight files, plus nine files). Not r49 round work.

## Claims (re-measured)

Commands were run from the lane root. The tip counters read `git show` only. Counter blobs are identical at `99fa9d3f`, `1c846ed2`, and `b3ae50ef` (`c49_order.py` `7ca940160ed4b0729e5cf110ca00b5acd807ab58`; `c49_quote_truth.py` `0808c865234a4a2bc95905622871807c5c77ee1d`). `contract.json` blob is likewise unchanged. Scores staying 10 is not the axis move; the claimed surfaces are the order proof and the quote check.

### C1 operability — re-measured, improved

```
python3 -B .ufo/waves/round-49/c49_order.py --root . --revision <commit>
```

- Base `090ce8f1…`: `C1 order 0/1 met=False`, exit 1, reasons `proof absent` and `quote counter absent`. Do-nothing control holds.
- Pre-append `99fa9d3f…`: `C1 order 0/1 met=False`, exit 1, reason `proof absent`. The mirror already exists here; the predicate still fails. Second do-nothing control holds.
- Measurement `1c846ed2…`: `C1 order 1/1 met=True`, exit 0.
- Tip `b3ae50ef…`: `C1 order 1/1 met=True`, exit 0.

Independent ancestry and committed-byte check, not only the counter:

- `git merge-base --is-ancestor 99fa9d3f 1c846ed2` and the same against the tip both exit 0. `99fa9d3f` is the parent of `1c846ed2`.
- `git show 99fa9d3f:corpus/SOURCES.md` has no `S273` or `S274` row (140 rows). The mirror at that revision has both rows.
- `order-proof.json` is absent at `99fa9d3f` and present at `1c846ed2`, naming `pre_rev` `99fa9d3f` and `adopted_ids` `["S273","S274"]`.
- Census argv blob at `99fa9d3f` is `sources-census.sh validate --file` on the mirror path. It contains `--file` and does not contain `--root`. Exit blob is `0`. Stdout has no `E03` or `E04` and ends `file ok` on the mirror.
- `c49_quote_truth.py` at the measured revision contains `COMMITTED_BYTES_ONLY` and `git show`, and `os.path.join` is absent. It does not open a worktree path.
- Mirror versus landed registry: the two row lines are identical. The only difference is one blank line before `S273` in the mirror. That does not change the rows that were validated or appended.

### C2 freshness — re-measured, improved

```
python3 -B .ufo/waves/round-49/c49_quote_truth.py --root . --revision <commit>
```

- Base: `C2 passed 0/2 met=False`, exit 1. Both ids fail with no receipt, no row, no entry, no gate quote. Do-nothing control holds.
- Pre-append `99fa9d3f`: `C2 passed 0/2 met=False`, exit 1. Receipts exist; rows, entry, and gate quotes do not.
- Measurement and tip: `C2 passed 2/2 met=True`, exit 0, both ids `all rules hold`.

Independent substring check against `git show b3ae50ef:.ufo/waves/round-49/sources/<id>.txt`:

- S273 gate quote, 21 words, exact substring of `S273.txt`, sha256 `ab4a685d7432b69e659f6d3717aeeffc66b9277e69ad54de601f72cc30d4347b` matches the receipt. Not a raw substring of `S273.raw.html`; it is a substring after whitespace collapse. Cross-wire into `S274.txt`: false.
- S274 gate quote, 10 words, exact substring of `S274.txt` and of `S274.raw.html`, sha256 `e3be028952b74702f7f06fb540e91b481ac1a026bdbe87ff035a3b566b0fcda4` matches the receipt. Cross-wire into `S273.txt`: false.

`git diff 090ce8f1… b3ae50ef… -- SCORECARD.md` is insertions only (27 lines). No owned-axis score line was reduced. No capabilities row was added. Axis ratings stay 10. The move is the claimed surface, not the number.

## Registry and frontier checks

- `corpus/SOURCES.md` at the tip: 140 → 142 rows. Added only S273 and S274. No existing row's cells changed (`diff` of the pre-live registry against the tip is those two lines). Each new row has NF=13 (11 cells), status `mined`, opened `2026-10-24`, recheck exactly `180d`, used-by exactly `corpus/knowledge/crawl-budget-consequences.md`. That path exists and opens with `source:` / `verified-at:` / `recheck:`.
- Lesson Gate records the stripped recheck prose (campaign curl, date 2026-10-23) and the used-by old→new as the same path. The staged S259 row still carries prose recheck and a backslash-escaped pipe; the adopted rows do not.
- Committed collision scratch: `reg-ids` 140 lines, `staged-ids` 121 lines, `collisions` empty. `guard-collisions` contains `S273`, so the guard is shown able to fail.
- Quarantine slice has 12 lines (S142, S143, S148, S156, S161, S193, S194, S195, S206, S154, S178, S184). None of those ids was appended. Not re-fetched this check; the lane also did not re-fetch them.
- Census re-run: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exit 0, the same twelve W04 ids (S033, S088, S092, S098, S099, S102, S110, S111, S115, S116, S117, S127), then `kake ok`.
- Coverage map `corpus/README.md` has no `crawl-budget-consequences` row. The new entry is on ground the map did not hold.

## Wave reconciliation

Committed `w49-spec.json` has 32 items. Role mix: scout 6, connector 1, executor 6, scribe 4, reviewer 5, critic 4, mutation-tester 3, sentinel 2, revenger 1. Attack roles under the addendum set (reviewer, critic, mutation-tester, labrat) are 5+4+3+0 = 12/32. Sentinel and revenger are not in that set.

Committed `settlement.json`: 23 processes with exit 0, 9 `timeout-200s`, union 32, no overlap. Report files under `w1/`: 24 markdown reports plus `swarm-registry.json`. Every exit-0 seat has a report. `ReviewUsedBy` is the only dead seat with a report. The other eight dead seats have none. No replacement names. The 9 timeout-killed seats are not credited, including `ReviewUsedBy`.

`/tmp/kake-r49-run.json`, read at this closure and not a durable pointer, has `spawn` 32 and one `taskCall` of 32 tasks, policy band 32–64, hard ceiling 256. The grant string `granted lane=kake wave=r49-w1 seats=32 live=39 pending=0 cap=256` and the `kimi --prompt` transport appear in the lane report and `LOG.md` only. `wave-slot.sh status` has no live `r49-w1` reservation. `live=39` was not re-derived. The L2 floor is met by the 23 exit-0 seats in that one batch, not by the killed seats and not by the spec alone.

## Spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S273 | admit | live `https://developers.google.com/crawling/docs/crawl-budget` (HTTP 200, 74323 bytes, 2026-10-24 21:45:53 -0300) and committed `S273.txt` | agree | 21-word quote is in the live body after whitespace collapse, and is an exact substring of the committed retained text. Not a raw-HTML substring, as the lane disclosed. Row is mined, recheck `180d`, used-by names the admitted entry. Live sha differs from the committed raw blob; the article sentence is still present. Diff after nonce normalize is analytics JSON key order, not the quote. |
| S274 | admit | live `https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate` (HTTP 200, 68787 bytes) and committed `S274.txt` | agree | 10-word quote is a raw substring of the live HTML and of the committed retained text. Same row normalization as S273. |
| S259 / `jekyll-url-baseurl-options.md` | reject | staged `shokuknow/merge/kake/SOURCES.append.md` row and `knowledge/corpus/knowledge/jekyll-url-baseurl-options.md`; held S080 | agree | Staged source and S080 both cite `https://jekyllrb.com/docs/configuration/options/`. A second row would be a within-scope duplicate URL. Flip (supersede S080, no second row) matches. Not present in the lane tree. |
| `ollama-openapi-contract.md` | reject | staged file; kake `PROVINCE.md` Adjacent; kama `PROVINCE.md` domain line | agree | Staged `source:` cites `raw.githubusercontent.com/ollama/ollama/.../docs/openapi.yaml`, and the staged ground line assigns local model-serving endpoints to kama. kake Adjacent says the same. kama's domain is local model serving and endpoint health. Out of province. Not present in the lane tree. |

Both Gate quotes are within the ≤25-word rule (21 and 10).

## Axis verdicts

- operability: improved. Order 0/1 at base and at the pre-append commit, 1/1 at the measurement commit and at the tip. The pre-append mirror is a strict ancestor; the counter reads `git show` only; the mirror validation is `--file`, not `--root`. Score stays 10.
- freshness: improved. Quote truth 0/2 → 2/2 for S273 and S274 on committed bytes, still 2/2 at the tip. Live re-open agrees. Score stays 10.
- depth: unchanged. No depth claim. SCORECARD diff is additive.
- coverage: unchanged. No coverage-score claim. The new entry is expansion, not a coverage-axis move.
- calibration: unchanged. The round disclosed the collapsed S273 quote, the heading gloss, the `--file` limit, and the empty credit for killed seats. SHONEN has no self-awarded `[x]`.
- adjacency: unchanged. Ollama was refused rather than absorbed. PROVINCE Adjacent still assigns local model serving to kama.

## Trend verdicts

- expansion: improved. One new knowledge entry on crawl-budget ground the coverage map did not hold, citing two mined rows opened this round.
- quality: improved. The order proof fails on both do-nothing controls and passes only after the ancestor append; the quote counter no longer opens worktree bytes; both new quotes re-verify, and no admitted entry failed its re-check. Rows are normalized to bare `180d` with no pipes.
- discernment: improved. This outside sample agrees on both re-opened admits and on both rejects. The lane's own `unchanged` grade was correct before this check existed; the check now agrees. Quarantine was not re-fetched.

## Routed defects

1. The grant line and the `kimi --prompt` transport are not in a durable artifact outside the lane's own report and `LOG.md`. `live=39` was not re-derived. Next round that cites the wave must commit the `wave-slot.sh` stdout and the dispatch command. Do not treat `/tmp/kake-r49-run.json` as evidence after this session.
2. The 12 quarantine ids were not re-fetched. Do not adopt them on the round-48 hand-check alone.
3. Operator, not the lane: the eight `round-46/residual/` reports and the nine `>1MiB` validate copies stay uncommitted. Do not sweep them in a closure or a later lane commit to zero a count.
