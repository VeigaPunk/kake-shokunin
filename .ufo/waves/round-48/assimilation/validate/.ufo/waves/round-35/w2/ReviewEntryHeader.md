# W2 ReviewEntryHeader — attacks the C2 entry's eight header lines (`corpus/knowledge/security-txt-publishing.md:1-8`)

Checked each header line against `.ufo/waves/round-35/sources/receipts.json`, `corpus/SOURCES.md` rows,
and the sealed counter (v1 + v2); ran the recheck instruction as written in a sandbox. Entry bytes are
identical at 95abec21 → master 7deacc46 → working copy 0d52173 (`git diff --stat` empty), so all
measurements below describe the current text.

## Findings (by severity)

**F1 — `counter:` line 8 states version 1's size cap while naming the version 2 counter (stale at landing).**
Line 8 says "≤ 1500 words"; the named file caps at `C2_MAX_WORDS = 2200` counting `[a-z0-9]+` runs
(`.ufo/waves/round-35/sealed_count.py:65,228-229`); version 1 (`sealed_count_v1.py:56` = 1500,
whitespace words) was superseded at bd14096a, an ancestor of the landing commit 95abec21
(`git merge-base --is-ancestor bd14096a 95abec21` exit 0). Measured at 95abec21: v2 words 1388, v1 words
1298 — both pass, so not verdict-changing, but the header misdescribes the contract it points to.
Fix wording: "entry present, ≤ 2200 words counted as [a-z0-9]+ runs (version 2; version 1 counted
≤ 1500 whitespace-separated words), copiedShare ≤ 0.25, ≥ 3 good cites of S078–S099, ≥ 9 of 12 sealed probes."

**F2 — the `counter:` command exits 2 on the current landed text, so `falsifier:` arm 3 cannot fire.**
At clone HEAD 0d52173 (master 7deacc46) the run exits 2 "key visible at the measured revision" with
EITHER key form — the reveal commit committed `.ufo/waves/round-35/sealed/c2-probes.json`, and
`sealed_count.py:300-302` refuses any revision containing it, `--key-file` included (both runs EXIT 2,
observed). So "a C2 run on this text reporting copiedShare above 0.25" (line 7) is structurally
unrunnable now; only the recorded pre-reveal run at 95abec21 measures this text. The header gives no
warning. Fix wording — append to `counter:`: "measurable only at revisions before the reveal
4c6be2bd (later revisions exit 2 by design: the key is visible there); entry bytes unchanged
95abec21→master, so the recorded 95abec21 run is the measurement of the current text." And in
`falsifier:`: "…or a C2 run at a pre-reveal revision of this text reporting copiedShare above 0.25."

**F3 — `counter:` sealing sentence is stale corpus prose.** "the probes are sealed and were not read"
was true only at drafting time; the probes were revealed at 4c6be2bd and are now tracked and readable
(`.ufo/waves/round-35/sealed/c2-probes.json`, sha 111bceea… pinned at `sealed_count.py:31`). A later
reader of the landed entry is told the probes are still secret. Fix wording: "Not run by the drafting
seat; the probes were sealed until the reveal 4c6be2bd and are readable since at
.ufo/waves/round-35/sealed/c2-probes.json."

**F4 — `recheck:` line 3 is runnable (verified end-to-end) but its S084 arm can never pass and its
S001/S002 arm is not covered by the named script.** Ran `fetch_sources.py` in the sandbox: EXIT 0,
11 GETs, statuses identical to retained receipts, and 10/11 visible texts byte-identical. S084
(GitHub) changed: text sha256 35cf4b7ba4…→0b6d5f622c… at the same 269 bytes; the served
`Expires: 2026-11-21T23:04:37z` equals my fetch wall-clock second (23:04:37Z) + 30 days — the
retained one was `22:02:20z` at the 22:02:20Z fetch. GitHub regenerates the file per request, so
"compare receipts.json" flags S084 on every refetch forever, and the instruction gives no rule for
separating expected churn from a contradiction (no sentence is contradicted: line "GitHub's retained
body" and row S084 are retained-bytes-scoped). Also the script's SOURCES dict holds only the 11
round-35 ids (S006, S078–S087) — S001/S002, named as a change trigger in the same line, are not
re-fetchable by it; their rows (`corpus/SOURCES.md:9-10`) say recheck "on-release" with no spelled-out
procedure. Fix wording: "…re-run fetch_sources.py in a sandbox and compare receipts.json; S084's
served Expires is regenerated per request (fetch time + 30 days), so its textSha256 is expected to
differ on every refetch — compare its field set, not its sha; S001/S002 are re-checked by fetching
their own row URLs (recheck on-release)."

**F5 — `source:` line 1 names S001/S002, but their registry used-by cells were not updated.** The
entry cites (S001, S002) in "GitHub Pages: branch build versus artifact build", and S006's row
(`corpus/SOURCES.md:14`) WAS given the used-by addition, while S001/S002 (`:9-10`) still list six
other files and not `corpus/knowledge/security-txt-publishing.md`. The counter cannot see this: its
good-cite conditions apply only to ids matching `S0(?:7[89]|8\d|9\d)` (`sealed_count.py:261`).
Fix: append the entry path to both used-by cells (owner's edit, not mine).

## Per-line verdicts

- `source:` (line 1) — PASS with F5. All named ids exist as registry rows; S081/S087 correctly
  described as opened-and-rejected (receipts: S081 HTTP 200, S087 HTTP 404; rows status `rejected`,
  used-by `—` at `corpus/SOURCES.md:89,95`).
- `verified-at:` (line 2) — PASS. receipts.json holds exactly 11 GETs; window min 22:00:48Z
  (S078/S079), max 22:27:55Z (S087); 10×200 + S087 404; all nine listed sha256 prefixes match the
  receipts and the counter's PINNED_TEXTS (`sealed_count.py:43-53`); hosts rfc-editor.org,
  securitytxt.org, jekyllrb.com, docs.github.com ×3, en.wikipedia.org, github.com, www.google.com,
  www.iana.org — none operator-owned, none in freshness-pins.json.
- `recheck:` (line 3) — PARTIAL: runnable and run (F4); 90d horizon consistent with the rows' 90d.
- `scope:` (line 4) — PASS; matches entry content, no operator-owned property claim anywhere.
- `ground:` (line 5) — PASS; retained texts + receipts.json exist at the named path, are sha-pinned
  by the counter, and body sentences carry ids with [INFERENCE] marks.
- `coverage:` (line 6) — PASS; all eight RFC 9116 registered fields with cardinality under "The
  fields" (Contact, Expires, Preferred-Languages, Canonical, Encryption, Policy, Hiring,
  Acknowledgments), plus every other listed item.
- `falsifier:` (line 7) — PARTIAL: arm 3 unrunnable (F2); arm 1 needs F4's churn rule; arms 1–2
  exercised negatively — the fresh fetch found no contradicted sentence (all cited visible texts
  unchanged except S084's request-generated timestamp).
- `counter:` (line 8) — FAIL as written (F1 stale cap, F2 unrunnable at post-reveal revisions, F3
  stale sealing sentence). The command itself does reproduce the recorded receipt at 95abec21.

## Convention comparison vs corpus/knowledge/link-preview-metadata.md

Same eight fields, same order, same 90d horizon. Round-35 improved on round-34's hedged "the logic of
fetch_sources.py" by naming a concrete tracked file (`.ufo/waves/round-35/fetch_sources.py`, tracked
at 7deacc46, runs EXIT 0). Regression: round-34's counter line states its five conditions accurately;
round-35's misstates the size condition (F1) and omits the pinned-texts-intact half of the copied
condition (minor, summary-level).

## Commands run (sandbox /fast/scratch/hyaku/kake-r35/w2/ReviewEntryHeader/, TMPDIR under it)

1. `git rev-parse HEAD` (lane, read-only) → 0d52173cb676…, parent 7deacc4629c1… (jj working copy on
   landed master) — exit 0.
2. `git merge-base --is-ancestor bd14096a 95abec21` — exit 0 (v2 counter predates the entry).
3. `git ls-tree 7deacc46 -- .ufo/waves/round-35/` — fetch_sources.py, sealed_count.py,
   sealed_count_v1.py, sealed/, sources/, verification/ all tracked — exit 0.
4. `git diff --stat 95abec21 7deacc46` and `7deacc46 0d52173`, limited to the entry, SOURCES.md,
   sealed_count.py — empty output, exit 0 (no post-landing edits).
5. `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=… python3 -B .ufo/waves/round-35/sealed_count.py c2 --root . --revision 95abec210c35eb17abffc16f8d39dbc6c6825fc5 --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc` — EXIT 0;
   met true, words 1388, copiedShare 0.0, counterVersion 2, probes 12/12, entrySha256
   0b5ac7e83a62… (reproduces `.ufo/waves/round-35/verification/c2-at-95abec21.json` exactly).
6. Same with `--revision HEAD --key-revision 4c6be2bd…` — EXIT 2, "key visible at the measured revision".
7. Same with `--revision HEAD --key-file .ufo/waves/round-35/sealed/c2-probes.json` — EXIT 2, same error.
8. `python3 -B .ufo/waves/round-35/sealed_count_v1.py c2 … 95abec21… 4c6be2bd…` — EXIT 0, words 1298, met true.
9. `cp .ufo/waves/round-35/sources/receipts.json tmp/receipts-retained.json && timeout 240 python3 -B .ufo/waves/round-35/fetch_sources.py` —
   EXIT 0; 11 GETs 23:04:35Z–23:04:38Z; S078–S087 statuses 200 except S087 404, matching retention.
10. Receipt comparison — S084 CHANGED (sha 35cf4b7ba4…→0b6d5f622c…, bodyBytes 269→269, Expires
    22:02:20z→23:04:37z); S081 body bytes differ (107491→107681) with identical visible text; other
    9/11 fully identical. Sandbox artifacts: tmp/c2-v2-at-95abec21.json, tmp/c2-head-keyrev.json,
    tmp/c2-head-keyfile.json, tmp/c2-v1-mine.json, tmp/receipts-retained.json, and the re-fetched
    clone/.ufo/waves/round-35/sources/.

## Residual risk and verification gaps

- The 12/12 probe result is the counter's own report, reproduced once at 95abec21; I did not
  hand-verify probe regexes against entry semantics (out of item; the holds bar drifting into
  counter-trust questions).
- One refetch ~1h after retention; arms 1–2 of the falsifier can only be exercised per-moment.
- S085 (Google) static in my single refetch; a CDN answer could differ from origin (one GET only).
- F4's per-request Expires conclusion rests on two samples (22:02:20Z, 23:04:37Z); plausible but not
  proven to be per-request rather than per-minute generation.
- No tools installed (none needed); no pacman use; the only lane file written is this report.
