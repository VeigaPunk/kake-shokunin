# ReviewCounterC2 — review of the C2 counter and contract (round 89, lane-internal)

Scope: `.ufo/waves/round-89/c89_key.py` and `c2-contract.md`. Receipts, candidate sources, commands and checksums are in `.ufo/waves/round-89/w1/ReviewCounterC2/` (see `COMMANDS.md`, `SHA256SUMS`). Scratch was used for all candidate fixtures and has been deleted after the receipts were copied.

Two counter versions were tested:
- **v1** = freeze commit `08ab46a1`, `c89_key.py` sha256 `a72d5efc…`, guard `('c89_key','.ufo/waves','round-89','frozen','c2-cases','oracle')`.
- **v2** = lane HEAD, committed by `46a43e94` ("freeze v2"), sha256 `d4588d4b…`, guard `('c89_key','c89_defect_queue','c2-cases')` plus a same-line `open(`-with-`.ufo` rule.

Selftests: v1 43/43 and v2 43/43 (`selftest/`). Base reproduction: `controls/base-c2.txt` reproduced as the candidate-absent line with controls 5/5.

## Findings, by severity

### 1. [High] C2 counter edited after the dispatch marker; the frozen base receipt was rewritten
Evidence (commit times, `git log`):
- `08ab46a1` freeze, committer 18:12:25.
- `2e700b9a` "wave-1 dispatch evidence … ready marker", 18:13:04.
- `46a43e94` "freeze v2 — shortcut guard no longer refuses a docstring…", 18:16:18. It is **not** an ancestor of `2e700b9a` (checked with `git merge-base --is-ancestor`).
- At my first read (HEAD = `2e700b9a`) the same guard edit was already present as an uncommitted worktree change in `c89_key.py`.
- `21770586` rewrote `controls/base-c2.txt`: the ctl-table line changed from `source names '.ufo/waves'` (freeze) to `'c2-cases'` (HEAD). `freeze.md` names base receipts as freeze contents.

Consequences: the predicate text is unchanged, but the counter that scored the wave was edited after dispatch and its frozen receipt was regenerated. This is the R88-E pattern (freeze-after-dispatch) on the counter file. C1 item E, as `freeze.md` describes it, checks only that the freeze commit is an ancestor of the commit that first adds `w1.ready`. `08ab46a1` is, so E would pass despite the post-dispatch edit. [INFERENCE — C1 was not run at HEAD; this is read from the `freeze.md` definition.]

Suggested fix (for L1, not applied): either re-freeze before dispatch with a stated changelog, or make the check compare every counter/contract/receipt blob at HEAD with its blob at the freeze commit.

### 2. [High] The textual shortcut guard is defeated by string construction, in both versions
Each candidate below is a re-delegation to the counter's own reference, so it does not implement the contract. Each reaches `frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true`, exit 0.

| candidate (runs/) | how it reaches the target | v1 guard | v2 guard |
|---|---|---|---|
| `runtime_import` | `importlib.util.spec_from_file_location` with the counter path built from `'.u'+'fo/wa'+'ves/'+'round-'+'89/'+'c89'+'_key'+'.py'` | pass | pass |
| `aliased_import` | `sys.path.insert` + `importlib.import_module('c89'+'_key')` | pass | pass |
| `fileurl_exec2` | `urllib.request.urlopen('file://'+<same fragments>)` then `exec` of the source | pass | pass |
| `env_import` (env set) | path from `os.environ['KAKE_R89_REF']` (fails 0/16 when the variable is unset) | pass | pass |
| `hybrid_table` | 12 literal frozen key strings + JSON-list encoding for all other inputs (see finding 3) | pass | pass |
| `wave_read_pathlib` | reads `c2-contract.md` via `pathlib` with fragment-built path | pass | pass |

What the guard misses: any aliased or re-spelled import of the reference; `importlib` from a runtime-built path; `import_module` with a constructed name; environment-variable paths (the counter's `run_candidate` inherits the caller's environment and the receipt does not record it); `urllib` file reads and `exec`; any literal table; and reads of wave-tree files built from fragments. Network reads were **not** exercised (no GET was made; file:// only), but the guard is a token scanner, so an `http://` read is equally invisible to it [INFERENCE].

The guard's own docstring discloses that it is textual. The disclosure is accurate, but the guard in practice rejects only literal spellings of the forbidden tokens. The "ctl-oracle-import" and "ctl-table" controls are rejected only because they spell the token literally, which is the only case the control set tests.

The reference-copy candidate (`ref`, REFERENCE verbatim) also reaches met=true. That is an honest re-implementation of the contract, so this is expected, but it means the counter cannot distinguish an honest implementation from a copy of its oracle.

### 3. [High] Property population checks relations only; the declared encoding is checked only by 12 literal cases
The property classes assert `same`/`different` between two keys. They never assert the key string. The declared escaping, layout and member order are therefore tested only by the 12 literal key strings in `c2-cases.json`.

Evidence: `hybrid_table` (`runs/head_hybrid_table.txt`, `runs/wt_hybrid_table.txt`) uses a JSON-list encoding for every non-frozen input and a 12-entry literal table for the frozen inputs. It scores frozen 16/16, props 200/200, refuse 9/9, met=true. The contract's canonical form is not implemented for any non-frozen input.

Also: the property population is not hidden. The seed (89089) is printed in the receipt and the generator (`_rand_case`, `_props`) is in the same public file, so anyone can regenerate the 200 pairs. The freeze's statement that "a table over the committed 16 cases cannot reach it" holds only for a pure table. The hybrid defeats it.

### 4. [Medium] Refusal coverage misses two contract rules that apply to every header, not only nominated ones
The contract refuses (a) a header value containing CR or LF and (b) two header names differing only in case, with no restriction to nominated headers. The counter's frozen cases and refusal table test both only on nominated headers.
- `lf_nominated_only` (CR/LF refused only for nominated headers): met=true (`runs/head_lf_nominated_only.txt`).
- `dup_nominated_only` (case-duplicate refused only for nominated names): met=true (`runs/head_dup_nominated_only.txt`).

### 5. [Medium] The refusal check is a substring match, so wrong reasons pass
`refuse` checks exit code 1, the `invalid_input:` prefix, and that a fixed substring occurs in stderr. Substrings such as `uri`, `token`, `string` and `object` are common words.
- `composite_reason` prints one message naming all nine refusal keywords for every refusal: refuse 9/9, met=true (`runs/head_composite_reason.txt`).

### 6. [Medium] U+001D: the contract never defines the fourth separator, and the reference's escape of it is untested
- The contract says "the four separators below become %1C, %1D, %1E, %1F", but its layout names only US (U+001F), RS (U+001E) and GS (U+001C). U+001D is never named.
- The contract's GS is U+001C. In ASCII, U+001C is FS and U+001D is GS, so the name "GS" is inconsistent with ASCII usage.
- The reference escapes a raw U+001D to `%1D`. `no1d` (REFERENCE without that escape) scores met=true (`runs/head_no1d.txt`, `runs/wt_no1d.txt`). Observed outputs: REFERENCE `u\x1fa\x1ex%1Dy`; no1d `u\x1fa\x1ex\x1dy`. Both are injective because U+001D is not a structural separator in the layout.
- Resolution needed: either declare U+001D as a separator with its own role, or drop it and rename GS.

### 7. [Medium] v2 admits literal reads of the wave tree, contrary to the contract's candidate rules
The contract forbids reading "any file under `.ufo/waves/`". v1 refused the literal token `.ufo/waves`; v2 removed it and retained only a same-line `open(` check.
- `head_wave_read_literal_v1` (v1, literal path read via `pathlib`): met=false, rejected by the guard.
- `wt_wave_read_literal_v2` (v2, same candidate): met=true (`runs/wt_wave_read_literal_v2.txt`).
- The fragment-built variant passes under both v1 and v2 (`runs/head_wave_read_pathlib.txt`, `runs/wt_wave_read_pathlib.txt`). So v2 did not create the general bypass; it removed one literal check that v1 had.

### 8. [Low] Guard rejections print garbled `fail:` lines
When the guard fires, `score_candidate` returns the note string in the `fails` slot. `main()` then iterates over that string and prints `fail: s`, `fail: h`, `fail: o`, … (12 characters), so the reason is lost from the receipt. Reproduced on v1 and v2 (`runs/head_plain_import.txt`, `runs/wt_plain_import.txt`). The control lines are unaffected because they take a different path.

### 9. [Low] Contract is silent on three cases the reference accepts
- A duplicate JSON member name in `request_headers` (`{"a":"1","a":"2"}`): json keeps the last value silently; exit 0, key uses `2`.
- A NUL or other CTL (other than CR/LF) in a non-nominated header value: accepted, exit 0.
- The U+001D question in finding 6.
None of these is tested. The contract should declare each as accepted or refused.

## Question-by-question

**(a) Seven worked examples re-derived by hand.** All seven match the hand derivation. An independent implementation written from the contract prose (`meta/indep_check.py`, no shared code with REFERENCE) also matches all seven, and so does the counter's REFERENCE. The reference agrees with the contract on every worked example. Findings 6 and 9 are contract gaps the examples do not reach.

**(b) Shortcut candidate reaching 16/16, 200/200, 9/9 without implementing the contract.** Yes. See finding 2 (runtime-path import, aliased import, file read with exec, env-var path) and finding 3 (hybrid table). The guard is the only obstacle for each re-delegation candidate. For the hybrid, the guard is not an obstacle at all: the 12-entry table contains no forbidden token.

**(c) Seed stability.** Run with seeds 89089, 1, 2 and 4242.
- Reference: frozen 16/16, props 200/200, refuse 9/9, met=true at all four seeds.
- Constant-key stub: frozen 0/16, props 100/200, refuse 0/9, met=false at all four seeds. The 100 are exactly the five `same`-relation classes.
- Population size is 200 at every seed by construction (20 matched draws per class). Its content changes with seed: seed 89089 and seed 1 share only 4 of about 199 distinct left inputs.

**(d) Guard against an importlib import from a runtime-built path.** Not detected. `runtime_import` passes the v1 and v2 guards and reaches met=true (`runs/head_runtime_import.txt`, `runs/wt_runtime_import.txt`).

## Other observations (not counter defects)
- `scripts/cache_key.py` at lane HEAD (`9784ad54`, ExecKey final) passes the v1 and v2 counters, with receipts matching the committed carrier files (`carrier/`). Its shortcut-token scan found only `import json, sys`. I did not audit its logic beyond the counter; the L1 copy in `w1/L1/cache_key.py` differs by docstring text.
- My first `fileurl_exec` candidate failed for a reason of my own: `NameError: __file__`. Fixed as `fileurl_exec2`. Recorded in `runs/`; not a counter finding.

## Verification gaps and limits
- Only the counter's stated scope was tested. No claim is made about storability, freshness, reuse or serving, per the contract's own scope.
- Network-read shortcut not exercised; see finding 2.
- Environment-variable test shows dependence on the inherited environment; it does not test any particular harness.
- I did not run the C1 counter at HEAD; the C1-E observation in finding 1 is from the `freeze.md` definition.
- The counter copies are the freeze-commit (v1) and the committed HEAD (v2, sha256 `d4588d4b…`). The lane tree continues to change; these results apply to those two blobs.

## Tools and hosts
- No tools were installed or upgraded. No pacman, no `~/.local/bin` writes.
- No network GET. All URL-style candidates used `file://` on local scratch paths.
- Lane writes: only `.ufo/waves/round-89/w1/ReviewCounterC2/` and this file. The lane was read with `git show`, `git log`, `git ls-tree`, `git archive` (read-only; produced an empty tree and was discarded), `git merge-base`, and `git status`.
- Scratch `/fast/scratch/hyaku/kake-r89/ReviewCounterC2/` was deleted after the receipts were copied.

## Recommended fixes for L1 (not applied)
1. Re-freeze the counter before any further scoring, or restore the freeze-commit guard; record the change in `freeze.md`; make the C1-E check cover counter and receipt blobs changed after the dispatch marker.
2. Replace the textual guard with an execution-time check (for example, run the candidate with a sealed temporary directory and no access to the wave tree), or stop claiming it as a shortcut detector.
3. Add property classes that assert the key string for each declared form (escape, layout, member sort), or add cases for the encoding that the hybrid defeats.
4. Extend refusal coverage to every-header CR/LF and case-duplicate rules, and bind each refusal check to a specific reason string.
5. Declare U+001D, rename GS to match ASCII or declare the mismatch, and declare duplicate JSON members and non-CR/LF CTLs.
6. Fix `main()` so a guard note prints as one line.
