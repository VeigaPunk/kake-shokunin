# ReviewCounterCode — round-35 sealed counter review (wave 1)

Target: `.ufo/waves/round-35/sealed_count.py` pinned at `318561e` (blob sha256 `c4d58dae…49ef`;
`git diff 81d9fd74 318561e -- <counter>` empty, so byte-frozen since the declaration).
Mid-review the L1 landed counter v2 at `bd14096` (v1 retained as `sealed_count_v1.py`;
tip `b1cbbc3`; v2 blob `1b4d9d59…3469b` = the working tree). Findings are marked v1
(pinned target), v2 (what will score), or both; every v1 crash finding was re-executed
against v2 and persists. I never read, listed or opened anything under
`/fast/scratch/hyaku/kake-r35/sealed/`; all runs used fake keys against sandbox copies
whose only change is three env-pin overrides (`FAKE_C1_SHA`, `FAKE_C2_SHA`, `FAKE_PINS`;
logic untouched). Sandbox: `/fast/scratch/hyaku/kake-r35/w1/ReviewCounterCode/`
(`sc.py` = patched v1, `v2s.py` = patched v2, `keys/`, `labs/`). No tools installed.

## Verified correct (observed, with rc)
- Exit contract normal paths: met → 0; condition false → 1; refusals → 2 with JSON.
- GIT_ stripping (`_env` v1:76-77): c1 run with `GIT_DIR=/nonexistent/dir
  GIT_WORK_TREE=/nonexistent GIT_INDEX_FILE=/nonexistent` → byte-identical stdout, rc 1.
- Key-visible refusal (v1:273, v2:301): rc 2, clean JSON with head. Wrong-sha key file,
  key absent at `--key-revision`, unresolved `--revision`: all rc 2, JSON.
- Timeout (v1:166-168, v2:175-177): 25s-sleep tool → case fails at 20.1s, rc 1, no traceback.
- Temp cleanup: zero leftovers in TMPDIR after 16 runs.
- Non-UTF-8 entry: `decode("utf-8","replace")` → clean JSON rc 1, no crash (v1:239, v2:242).
- Pinned texts: all nine shas match the blobs at `318561e`.
- Shingles: 8-word window → 1 shingle, 7 → 0. Escaped `\|` kept literally in the cell.
- Parser: v1 ignored ```-fenced rows but counted rows inside ~~~ fences and toggled fence
  state on 4-space-indented ```; v2 (`registry_rows` v2:205-227) recognizes both fence kinds,
  cleans comments first, and counts only the first `## Registry` section — v1's tilde hole is
  closed in v2.
- REFUTED (recorded so nobody retries): planting the entry text as an extra
  `sources/*.txt` cannot lower `copiedShare` — the ls_tree union (v1:228, v2:252) only grows
  the intersection. Identical entry scored `copiedShare` 1.0 with the planted file (met false)
  vs 0.2 without (met true). Labs: `labs/leak2` revA `8e0e7312…`, `labs/noleak2` revB `ed379ef9…`.
- v2 receipt gate works: without `receipts.json`, goodCites `[]` (cites false); with per-id
  url contained in the row's source cell → cites true, met true, rc 0, `counterVersion: 2`.

## Findings

**F1 MEDIUM (v1+v2; could change a claim's result)** — four crash paths exit 1 with a
traceback instead of exit 2 "could not evaluate"; stdout carries no JSON, so an automated
`.exit` check records a failed claim instead of an unevaluatable run:
- (a) v1:166 / v2:175 `subprocess.run(..., text=True)` decodes tool stdout strictly. A
  contract-conforming C1 tool that emits any non-UTF-8 byte on stdout (contract bullet (c)
  lets a tool handle unreadable pages; nothing forbids echoing their bytes) raises
  UnicodeDecodeError → C1 unmet wholesale. Repro: commit a tool
  `sys.stdout.buffer.write(b"\xff…")`; run c1 → rc 1, traceback, no JSON (observed v1+## v2).
- (b) v1:110 / v2:119 `json.loads(data)` after the sha pin: corrupt-but-pinned key →
  JSONDecodeError rc 1. Repro: `FAKE_C1_SHA=$(sha256sum keys/bad.json)` + `--key-file bad.json`.
- (c) v1:149 / v2:158 `key["cases"]` (and `key["probes"]` v1:245): valid JSON missing the
  array → KeyError rc 1.
- (d) v1:80 / v2:88 `git()`: git missing from PATH → FileNotFoundError rc 1.
Fix: decode tool stdout with errors="replace" (judge on bytes), wrap `json.loads` and the
key-array accesses → `{"error": …}, 2`, catch FileNotFoundError in `git()` → exit 2.

**F2 MEDIUM (v2; could change a claim's result)** — declaration/counter mismatch on size:
SCORECARD "Round 35 — declared claims" (lane-tip line 1376) still declares "≤ 1500 words"
while v2 enforces `C2_MAX_WORDS = 2200` (v2:65) counted as `[a-z0-9]+` runs (v2:243), not
whitespace tokens. An entry of 1501-2200 alnum-run words passes the scoring counter but
fails the declared claim as written. `bd14096` rescored controls but did not update the
declared-claims table. Fix: amend the SCORECARD row before C2 is scored.

**F3 LOW (v1+v2)** — the "revision does not resolve" receipt (v1:267, v2:295) prints
`{"error": …}` without the head fields (revision/counterSha256/keyPath) that every other
exit-2 path prints (v1:269-276, v2:297-303); receipt automation keying on counterSha256
sees a different shape on this one path.

**F4 LOW (v2; reasoned, not exercised)** — copied-side asymmetry: the entry is cleaned
before shingling (NFKC + Cf-strip + comment removal, v2:243) but source texts are shingled
raw (v2:252). Source passages containing Cf characters (e.g. U+200B) can never match the
cleaned entry's shingles, so copying that preserves a source's zero-width characters is
undercounted by `copiedShare`. The probes side is cleaned, so dilution is still caught
there; only the copied condition keeps the raw text.

**F5 LOW (v2)** — the new good-cite gate binds a cite to `receipts.json`
(v2:258-271: receipt url must be non-empty and contained in the row's source cell), but
`receipts.json` is not sha-pinned (PINNED_TEXTS covers only the nine .txt files). A drafter
can add a receipt entry for an unopened id (S086-S099) plus a matching registry row and
re-fabricate a good cite. Pinning `receipts.json`'s sha beside the nine texts closes it
fully; the non-author row-truth read is the current mitigation.

**F6 INFO (v1+v2)** — the key-visible refusal checks only the claim's own key path
(v1:272-274): the c1 counter measures a revision that already holds the c2 key. Matches the
per-claim receipt design; noting the exact semantics.

**F7 INFO (v1+v2)** — over-strict directions, drafter-harm only: duplicate registry rows
for one id disable that good cite (`len(rows) == 1`); a used-by cell containing `\|` never
matches ENTRY; in v2, rows inside a 4-space-indented code block still count (fence regex
caps at 3 spaces; CommonMark calls that block literal).

**F8 INFO (v2, documented design)** — size now counts words after comment removal, so text
inside HTML comments is exempt from the 2200 limit; probes run on the same cleaned text, so
hidden text cannot satisfy probes either. Consistent with the docstring "what a reader sees".

## Claim-result impact
- F1(a) is the only path that can flip a scored result on otherwise honest artifacts (C1).
- F2 makes C2's scorer looser than the declaration text; one of the two should move before scoring.
- The REFUTED planted-file attack and the v1 parser holes cannot change met/not-met for
  conforming artifacts; controls' committed receipts are unaffected by F1-F8 as observed
  (all control tools/entries produce clean UTF-8 output).

## Not verified
- Real sealed keys were never exercised (bound forbids the sealed dir); all runs used the
  fake keys in `keys/` against the two patched copies.
- TIMEOUT=20 adequacy (only that it fires and cleans up).
- F4 with an actual Cf fixture (reasoned from v2:243 vs v2:252).
- HOME/.gitconfig influence on the git subprocess (only GIT_* is stripped, v1:76-77) —
  reasoned only; quotepath behavior was observed (a non-UTF-8 filename under `sources/`
  is quotepath-quoted and silently excluded from the shingle set; no exploit, since the
  nine pins force exact names+shas).
- The C1 fake case exercised plumbing only; its expect did not match the real tool's
  verdict, so per-case semantics of the sealed 24 cases remain untested by me.
