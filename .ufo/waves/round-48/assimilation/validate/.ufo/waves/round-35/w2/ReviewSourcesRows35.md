# ReviewSourcesRows35 — attack on SOURCES.md rows S078–S087 and the S006 used-by change

Target: at 7deacc4629c1d05a34fb919d8095e99efc7b712f — 11 cells/row, pipes, tier/kind vs CORPUS.md,
anchors vs receipts.json, status/used-by vs the entry's cites, S006 change logging, census exit.

## Method

Sandbox clone `/fast/scratch/hyaku/kake-r35/w2/ReviewSourcesRows35/clone` at 7deacc4.
`git diff --stat 7deacc4 0d52173` over corpus/SOURCES.md, the entry, the lesson and
receipts.json is empty — working-copy reads equal 7deacc4. No tool installs needed
(gawk present). No live fetches made (owned-host bound; all verification is against the
round's own receipts `.ufo/waves/round-35/sources/receipts.json` and retained `S###.txt`).

## Commands run (exit codes)

1. `python3 /fast/scratch/hyaku/kake-r35/w2/ReviewSourcesRows35/tmp/check_rows.py` → rc=0
   (structure, enums, anchor-vs-receipts, sha256 of every S###.txt vs receipts, entry-cite
   consistency, S006 diff vs base 16a6b8b8). Script kept in sandbox tmp/.
2. Quote-substring check, lesson "Gate" quotes vs retained texts → rc=0.
3. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → **rc=0**
4. Same script `validate --file corpus/SOURCES.md` in the sandbox clone (7deacc4) → rc=0.
5. used-by citation cross-check for S001/S002 → rc=0.

## Per-row verdicts (rows at corpus/SOURCES.md:9,10,14,86-95)

| Row | kind/tier/status | Verdict |
|---|---|---|
| S006 L14 | docs/A/mined | PASS — vs base 16a6b8b8 exactly one cell changed (used-by): old 5-path list intact, `corpus/knowledge/security-txt-publishing.md` appended; logged old→new at corpus/lessons/round-35.md:66. Anchor still reads "fetched 2026-10-19" — see note 2. |
| S078 L86 | spec/A/mined | PASS — anchor time 2026-10-22T22:00:48Z, HTTP 200, sha 4954ddcd all match receipt; quote exact. |
| S079 L87 | docs/A/mined | PASS structurally; tier judgment below. |
| S080 L88 | docs/A/mined | PASS — 22:00:49Z, 200, sha 24054b1a; quote exact. |
| S081 L89 | community/C/rejected | PASS — community is never A respected; used-by `—`; quote exact. |
| S082 L90 | spec/A/mined | PASS — 22:00:49Z, 200, sha 0746e9da; quote exact. |
| S083 L91 | dataset/A/mined | PASS — 22:00:50Z, 200, sha aceda87b; quote exact. |
| S084 L92 | dataset/A/mined | PASS — 22:02:20Z, 200, sha 35cf4b7b; quote exact. |
| S085 L93 | dataset/A/mined | PASS — 22:02:20Z, 200, sha c7a10ffa; quote exact. |
| S086 L94 | docs/A/mined | PASS — 22:27:54Z, 200, sha 710f4781; quote exact. |
| S087 L95 | docs/C/rejected | PASS — HTTP 404 recorded, sha 1d697e89, used-by `—`; teaches has REJECTED+flip. |

All 11 rows: 11 cells (NF=13), no raw or escaped pipe in any cell; kind/tier/status/opened/recheck
enums pass; every mined used-by path exists on disk; all 11 retained `.txt` sha256 MATCH
receipts.json textSha256; all 10 new-row anchors carry receipt time + status + 8-hex sha prefix.

## Findings

1. **MINOR — used-by drift on S001/S002.** The entry cites S001 and S002 in its `source:` line
   (corpus/knowledge/security-txt-publishing.md:1) and grounds its artifact-build section on them
   (`(S001)`, `(S001, S002)` — 7 S001/S002 occurrences in the file), but the used-by cells of
   S001 (SOURCES.md:9) and S002 (SOURCES.md:10) do NOT list the entry. Before this round the
   registry was exact for knowledge entries: S001's used-by listed all 6 then-citing entries,
   S002's all 5; now both are one short. The round updated S006 for exactly this reason but
   missed S001/S002, and the lesson's old→new log (round-35.md:62-73) omits them. The census
   cannot catch it (E11 checks used-by→disk, not entry-cite→used-by), so rc=0 does not cover it.
   Fix: append the path to both cells, log old→new in the lesson (CORPUS rule 2).
2. **Not-a-defect — S006 anchor staleness.** The anchor cell still says "fetched 2026-10-19" while
   receipts.json holds the re-open (2026-10-22T22:02:19Z, 200, sha 9ddf8eb2…). CORPUS rule 2 is
   append-only: only `status`/`recheck`/`used-by` may change in place, so editing the anchor was
   forbidden; the re-open is recorded in receipts.json and the lesson Gate (round-35.md:45-66).
   Compliant as landed. (My checker's two "cited-but-rejected" flags on S081/S087 were checker
   artifacts: the entry names them only as rejected openings; used-by `—` is correct.)
3. **S079 tier — row A vs Gate draft B: judged KEEP A.** CORPUS: A = primary/authoritative for
   the scope, explicitly including "maintainer statement"; B = strong secondary (expert write-up,
   survey, textbook). securitytxt.org is the RFC authors' own project site and the scope limits
   the row to "its getting-started guidance and its format-change note" — primary for its own
   guidance; nothing in the row leans on it for the normative format (that is S078's scope). The
   deviation is disclosed with the reason and precedent (round-35.md:45, cf. S077), and the
   anchor cites Step 1 and the Recent-changes paragraph, not a bare homepage. A draft B would
   have misapplied the secondary tier to a maintainer's own page. No census violation.

## Census output (assigned command, pasted)

```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```
Exit 0. W04 names S033 (pre-existing row, warning-only, does not affect exit). Sandbox rerun at
7deacc4 gives the identical single W04 line and `ok`, exit 0 — the verdict ties to the audited
revision, not just the working copy.

## Residual risk / not verified

- Quote and anchor checks are against the round's retained texts and receipts, not the live web;
  I did not re-extract `S###.html.gz` bodies, so a poisoned retained text would pass everything
  above. The retained files' hashes do pin them to the receipts.
- S084/S085 "whole served body" anchors: verified time/status/sha and the quotes, not an
  independent field-by-field read of both bodies against the anchor's described field list.
- I did not re-run the C2 counter, judge entry truth, or touch counter-trust / sandbox-threat
  lines (holds). No subagents, no lane mutations; this report is my only lane write.

Advisory to L1: one finding (Finding 1, two used-by cells + two lesson log lines); everything
else in scope survived attack.
