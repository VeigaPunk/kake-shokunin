# Paste-ready `## Mistakes` row (round 61) — from SentinelC2Net, L1 ruling (d)

Add as row 4 in `.ufo/waves/round-61/w1/ScribeLessonMistakes.files/lesson.md` §`## Mistakes`, keeping the
existing table shape `Class | Evidence | Captured-by | Fix`. Factual basis is `w1/SentinelC2Net.md` F1 and
`w1/SentinelC2Net.files/{static-audit-pre-edit-eac57099.json,static-audit-current-ba10702.json,pre_excerpt.txt,dyn-probe.json,dyn-probe-current.json}`.

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| `process/tool-bytes-not-retained` | C2's 12 capture receipts (`response.json` mtimes 06:15:55–06:16:03 -0300, 2026-10-27) were written by `scripts/response_snapshot.py` at sha256 `eac57099a6e097a28638bc2b7e29ddd3dfd301b34c0caa255d8d708bcb039643`; the file in the worktree is `ba107024c770db194f0b07c806641f1674e109134f62c0eac671e5b06bde1bb7` (mtime 06:17:14). The tool is worktree-only — `git ls-tree HEAD scripts/` has no `response_snapshot.py` and `git log -- scripts/response_snapshot.py` is empty at `eaa9177e…` — so no blob identifies the producing bytes and the pre-edit bytes survive in no artifact. | `none` (no in-lane rule reads the history of a tool that wrote a receipt); manual capture: SentinelC2Net w1, which proved the delta is confined to the docstring/usage text and the `--overwrite` pre-flight (`Redirects`, `utc_now`, `fetch` through the body cap, `write_file`, `write_json`, `load_population` occur verbatim in the committed file), and that both versions behave identically. | Before a load-bearing run: `sha256sum scripts/<tool>.py` and copy the exact bytes into `<Seat>.files/`, then quote the digest on the capture line of the seat report (round-61 C2 line does this). Where the tool's identity carries a claim, commit it first and cite `git rev-parse HEAD:<path>` instead of a bare sha256. |

Notes for the scribe, so the row stays honest:

- Captured-by is `none` in the sense the other rows use: no lane rule fired. The sentinel caught it by reading both
  versions; that is a manual capture, not an instrument.
- The row is a **process** defect, not a data defect: the 12 receipts are self-consistent and re-verifiable
  (`len(body.bin)==bytes` and `sha256(body.bin)==sha256` on 12/12), and the audit's inputs are unaffected. What is
  unverifiable from artifacts is that the committed code wrote them.
- It is the same class as row 1 (`process/undisclosed-receipt-rewrite`) applied to a tool rather than a receipt: the
  difference is that this one was disclosed in prose and the residual risk was bounded by direct comparison.
- The `--overwrite` flag added after the run permits in-place receipt replacement; the guard is fail-closed by
  default, and no receipt changed (SentinelC2Net F8, `capture/` should be treated as commit-once).
