# AnchorCensus — kake round 21 w1 (executor)

Scope: implement `.ufo/waves/round-21/anchor-census.mjs` — a read-only
moved-reference register and byte-preservation audit for the round-21 wave.
Writes: this report plus the target script only. Tools installed: none
(node v24.21.0 and git already on host; pacman paused, nothing needed).

## Files changed

- `.ufo/waves/round-21/anchor-census.mjs` (new, 17393 bytes, executable).
  Syntax verified with `node --check` (parse only — the script itself was
  **not** executed; the assignment defers running to L1 after integration).

## Behavior implemented

1. **Target census.** `git ls-files -z` yields the tracked population, then
   exact regexes select targets:
   - `corpus/knowledge/[^/]+\.md` → 21 knowledge entries (freshness-pins.json
     correctly excluded, non-md).
   - `corpus/lessons/round-\d+(?:-recensus)?\.md` → 15 lane-authored lessons.
     Aggregator audits (`round-N-aggregator-*.md`), `round-20-verifier-
     spotcheck.md`, and `round-21.md` are excluded by shape; untracked files
     (e.g. a work-in-progress `round-21.md`) cannot appear because
     `ls-files` is the source.
2. **Base comparison.** For each target, `git show
   5009ecaa1cce10b895617a585ddd3f7c7c923a84:<path>` supplies old bytes
   (base rev verified once via `rev-parse --verify --quiet`; per-path
   failure = `presentAtBase:false`). The current buffer comes from the
   working tree.
3. **Preservation verdict.**
   - Byte-identical → `preserved:true`, uniform `offset` map, zero additions.
   - Otherwise `currentBuf.indexOf(baseBuf)` tests whole-original
     containment. Found → `preserved:true` when additions sit on clean line
     boundaries. Prefix rule: must end at `\n` (or be empty). Suffix rule:
     allowed when the original ended with `\n`; **special case — base without
     final LF** (confirmed only `corpus/lessons/round-16.md`, base last byte
     `0x2e`, and its current bytes already contain the base as a contiguous
     prefix followed by `\n\n## Gate…`): a suffix starting with a newly
     added LF is a boundary-only addition (`terminatingLfAdded:true`), not
     a changed original byte, and that LF is not counted as a new line in
     `additions.suffixLines`. Repeated containment offsets flag
     `ambiguous-placement`. Report emits `map:{offset,
     firstOriginalNewLine, lastOriginalNewLine, oldLineCount, newLineCount,
     sameBytes:true}` — every original line maps to `old + offset`,
     including the newly LF-terminated last line — plus
     `additions:{prefixLines, suffixLines}`.
   - Not found → `preserved:false`, `violation:{type:
     "original-bytes-changed", changedOriginalLines, firstChangedOriginalLine,
     baseSha256, currentSha256}`, and a greedy monotonic line map
     (`map.type:"greedy"`, per-line `old→new|null`) is emitted purely as
     diagnostics for the L1 correction register.
4. **Reference scan.** Every tracked file — targets included, lessons cite
   each other — is scanned for literal
   `filename:line[-end]` references whose basename names a census target:
   regex `(?<![\w.\-/])(?:([\w.\-~/]*)/)?(<basenames>):(\d+)(?:-(\d+))?`,
   longest-basename-first alternation, negative lookbehind prevents
   mid-path/mid-name matches. Per reference the register records
   `source:{file,line,text}`, `cited:{basename,pathPrefix,start,end}`,
   `target.file`, `resolved:{oldRange,newRange}`, `sameBytes` (byte-equality
   over the referenced line ranges via cached buffers/line tables —
   `git show` is run once per target, not per reference; a single trailing
   line terminator is normalized away so the round-16 added-LF case still
   compares equal — `rangeBytesEqual`), `staleCitation`,
   and `status`: `current | moved | moved-bytes-differ | out-of-range |
   path-mismatch | target-not-at-base | ambiguous-target |
   unresolvable-target-violation`. A stated path prefix must be a
   directory-suffix of the real target (`knowledge/x.md`,
   `corpus/knowledge/x.md`, bare `x.md` all resolve; contradictory dirs
   flag).
5. **Safety confinement.** Credential/auth-shaped paths are skipped before
   any read (`SENSITIVE_RE`: credentials/secrets/tokens/oauth/passwords/
   ssh keys/.env/.pem/.key/.p12/.pfx/.netrc/.kubeconfig/agent.db segments);
   tracked scan today contains zero such paths. NUL-containing files are
   skipped as binary. The tool writes nothing and creates no temp files;
   git subprocesses are `ls-files`, `rev-parse`, `show` only — no shell.
6. **Output.** Single JSON document on stdout: `summary` (population and
   per-class counts), `ok`, `violations[]`, `files[]` (per-target verdict
   and map), `register[]` (every found reference), `mismatches[]`
   (all anomalies). Exit 1 when any violation or mismatch exists, else 0 —
   a stale-but-resolvable citation does **not** fail the run; it is the
   register's payload, not an error. Flags: `--root` (default: repo root
   resolved from script location), `--base` (default: frozen base sha),
   `--help`.

## Evidence retained

- `node --check .ufo/waves/round-21/anchor-census.mjs` → SYNTAX-OK.
- Population verified against `git ls-files`: 21 knowledge `.md` + 15
  lane-lesson `.md` = 36 targets; 126 tracked files total.
- Mutation shapes verified by inspection: knowledge files gained the
  provenance trio + blank line as a 4-line prefix (e.g. `drift-detection.md`,
  `git diff` = 4 insertions 0 deletions); lessons gained EOF `## Gate`
  blocks (e.g. `round-16.md` tail). The containment+offset model covers
  exactly this contract.
- Round-16 no-final-LF verified at byte level: base ends `0x2e` (no `0x0a`,
  the only such target — all other 14 lessons and all 21 knowledge files
  end `0x0a`); current bytes contain the base as a contiguous prefix
  (`head -c 4391` cmp-clean) followed by `\n\n## Gate…`. The script treats
  this as `terminatingLfAdded` per the operator wrap-up instruction; the
  old→new line map still covers the newly terminated last line and no
  mismatch is invented.
- HEAD currently equals the frozen base (`git log -1` = 5009eca); all
  differences the tool will report are working-tree edits from this wave.
- Reference patterns exist in the wild: `citation-debt.json` cites
  `corpus/knowledge/drift-detection.md:73`, `corpus/lessons/round-18.md:56`,
  `SKILL.md:309` etc. (SKILL.md is not a census target — correctly ignored
  by the register since it is not subject to prefix/suffix movement).

## Risks and limitations

- **Not executed.** Script was syntax-checked only. First real run is
  post-integration; logic edge cases (multi-occurrence containment,
  unterminated base files) are covered in code but unexercised on live data.
- **Scan set is tracked files only.** Untracked `.ufo/waves/round-21/w1/*`
  sibling reports may also contain `file:line` citations; they are invisible
  until tracked. L1 may want a second pass or a follow-up scan over the
  wave report directory after staging.
- **Range form.** Only `file:N` and `file:N-M` are registered; exotic
  forms (`file:L12`, `file:12+5`) are not matched — none were observed.
- **Greedy map is diagnostic.** On a violated file the old→new map is a
  heuristic alignment, not a proof; `moved-bytes-differ` references remain
  flagged rather than silently resolved.
- **Sources inside targets are scanned at their new line numbers.** A
  citation *inside* a prefixed file is reported at its shifted source line;
  the citation's own target resolution is unaffected.
- Stale citations (`staleCitation:true`, `status:"moved"`) are expected for
  every `file:line` citation into a prefixed knowledge file; the register
  gives L1 the old→new pair needed for the correction lesson.
