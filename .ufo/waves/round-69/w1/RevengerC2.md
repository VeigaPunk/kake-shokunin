# RevengerC2 — /tmp literals in scripts/freshness-sweep.mjs (read-only reconstruction)

Base `4d188f94` (lane master); lane tip `dbcfef0b` unused for measurement. Every byte below read with
`git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4d188f94:<path>`; no lane file touched. Full per-file
census (816 files) = `.ufo/waves/round-69/w1/RevengerC2/citations.tsv` (sha256 `e6f1f2e2…`), from `classify.py`.

## Introducing commits

`git log --oneline -S'/tmp/kake-r16' 4d188f94 -- scripts/freshness-sweep.mjs` → one commit: **ab87a485**.
`git log --oneline -S'/tmp/kake-r15' 4d188f94 -- scripts/freshness-sweep.mjs` → **the same commit: ab87a485**.
They co-enter because the file itself is created there (`git log --diff-filter=A` → ab87a485); base carries
3 r16 occurrences (lines 20, 182, 1204) and 2 r15 (103, 108); blame of 108/1204 = ab87a485.

Subject (verbatim, 764 bytes): “round-16: freshness 9->10 — drift detection widened from path-citations to ALL
quantified standing claims, instrumented (scripts/freshness-sweep.mjs + corpus/knowledge/freshness-pins.json +
runbook, exit 0/1/2/64, selftest 9/9, state-guard byte-identical); first complete claim sweep 160 claims -> 117
HOLD / 15 STALE / 7 UNVERIFIABLE (10 in never-swept classes: verb outcomes, journal shape, ETag, fire counts) all
fixed or re-pinned; CAUGHT plazir15-ghp 5-commits-ahead live/source drift … critic re-ruled MOVE-ELIGIBLE on both b…”

LOG.md line naming it: **LOG.md:208** — “- 2026-09-29 — round 16: freshness axis-move **9→10** — drift detection”
(LOG.md carries no sha: `git grep -n ab87a485 4d188f94 -- LOG.md` → no match).
The r15 *path* predates the script: `-S'/tmp/kake-r15'` over all paths first hits **88a4f4e2** (round-15), named by
**LOG.md:130** “- 2026-09-29 — round 15: freshness **axis-move, drift CAUGHT — SCORECARD” and cited at LOG.md:137.
Divergence: blame(line 20) = **02b6dd05** (round-20 comment rewrite); `-S` omits it because the occurrence count on
that line stayed 1, so only the count-changing commit (ab87a485) is reported.

## Citation table (every file at base citing `/tmp/kake-r`)

Group aggregates (`files / citations / executable / historical / pointer`; a citation = one line carrying the literal):

| group | files | cites | exec | hist | ptr |
|---|---|---|---|---|---|
| live prose tree (LOG, SKILL, SCORECARD, corpus/) | 27 | 123 | 3 | 8 | 112 |
| scripts/ | 1 | 5 | 2 | 0 | 3 |
| .ufo/waves/ reports+receipts | 310 | 2089 | 455 | 67 | 1567 |
| .ufo/waves/round-48..59 assimilation mirrors | 478 | 2899 | 472 | 102 | 2325 |
| **total** | **816** | **5116** | **932** | **177** | **4007** |

Live tree per file — `n(e/h/p)` = citations(executable/historical/pointer), files with no historical marker first:
`corpus/handoffs/cmdProbe-merge-fix.md 6(0/0/6)` · `corpus/README.md 1(0/0/1)` · `corpus/knowledge/freshness-sweep.md
2(0/0/2)` · `corpus/lessons/round-10.md 2` · `round-17.md 3` · `round-18.md 3` · `round-22.md 1` ·
`round-22-verifier-spotcheck.md 1` · `round-26.md 1` · `round-34-verifier-spotcheck.md 1` ·
`round-35-verifier-spotcheck.md 1` · `round-49-verifier-spotcheck.md 2` · `round-5.md 1` ·
`round-59-verifier-spotcheck.md 1` · `round-59.md 1` · `round-6-aggregator-audit.md 3` · `round-8-aggregator-box3-coldrun.md 1` (all 0/0/n).
`LOG.md 16(0/1/15)` · `SCORECARD.md 11(0/0/11)` · `SKILL.md 6(2/0/4)` · `corpus/QUALITY.md 3(0/1/2)` ·
`corpus/knowledge/free-read-verbs.md 38(0/2/36)` · `keeper-timer-inert.md 8(0/1/7)` · `probe-delta-alerting.md 1(1/0/0)` ·
`publish-queue.md 2(0/0/2)` · `corpus/lessons/round-12.md 4(0/2/2)` · `round-16.md 3(0/1/2)` ·
`scripts/freshness-sweep.mjs 5(2/0/3)`.

The requested binary (historical vs executable) leaves **4007 of 5116 citations (78 %) in neither class**: bare
provenance pointers to `/tmp/kake-r*` dirs that are on disk nowhere and are not marked absent on that line
(e.g. `LOG.md:299` “Evidence: `/tmp/kake-r16/` …”, `free-read-verbs.md:181` “Evidence: …”); forcing them into either
class would be a false classification. Executable citations (932) are commands a reader/runner is told to run
(`git clone … /tmp/kake-r24-…`, `python3 …/measure_c2.py --root /tmp/…`, `curl -o /tmp/…`, `mktemp -d /tmp/…`);
historical (177) are the lines carrying an absence marker within 50 chars of the literal (`absent`, `deleted`,
`gone`, `no longer`, `reaper`, `skipped`, `historical`).

## Consumer verdict

Question: does any committed script or wave tool, other than `scripts/freshness-sweep.mjs`, read the /tmp paths at run time?

* **For the two literals under study — no.** `git grep -l -E '/tmp' 4d188f94 -- scripts/` returns only
  `scripts/freshness-sweep.mjs`; no other lane script names `/tmp` at all, so no second reader of r15/r16 exists.
* **For the `/tmp/kake-r` family — exactly one other.** `.ufo/waves/round-50/dispatch_w1.sh:19` `SEATS=/tmp/kake-r50-seats`;
  line 24 `rm -rf "$SEATS"; mkdir -p "$SEATS"`, 46/52 write prompts and `exit-codes.tsv` there, 49 `cat "$prompt"`,
  76–89 read `exit-codes.tsv`. A wave dispatcher (mode 100644) invoked by `round-50/dispatch-command.txt`. It never
  reads r15 or r16, so C2's two sites have no second consumer; it is a separate, still-live /tmp root in wave tooling.
* **Contains the literal but does not read it:** round-23/24 `gen_w1.py`, `gen_w2.py` (literal is prompt text emitted
  into the spec JSON); round-59 `c59_axis_evidence.py` and its v1/v2/labrat copies (module docstring + fixture dict
  `OLD`; the resolver returns “absolute or home path (not committed bytes)” without any stat — line 197 of the base file).
* **Would read but nothing invokes it:** `.ufo/waves/round-48/assimilation/validate/scripts/freshness-sweep.mjs` is a
  byte-copy of the lane script at **3d07733b** (round-24) and still holds the two code literals at its lines 98/1183;
  no committed file references its path (`git grep -l 'assimilation/validate/scripts/freshness-sweep.mjs'` → none).
* **The gate's own reads:** line 108 is dereferenced only inside `if (fs.existsSync(snap))` (lines 890–892), so the
  r15 snapshot-absent branch (message `snapshot absent (expected once landed: /tmp is not durable)`) is what runs here;
  `/tmp/kake-r15` is absent on the host. Line 1204 is the `--selftest` write root; `/tmp/kake-r16/selftest` exists on
  the host (mtime 2026-11-03 15:19, fixture subdirs present) — observed, created by another process this round, not by me.

Confidence: high on commits, counts and reader census (committed bytes at 4d188f94, re-runnable from the artifact
script); medium on the 50-char absence window; the pointer class is the exact residual.
