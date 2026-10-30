# ReviewerC2Selftest — C2 counter selftest review

## Verdict / axes

Recommendation: no demonstrated C2 predicate failure. The unchanged frozen counter's selftest ran **11/11, exit 0**. Reviewed axes: fixture fidelity, genuine revision-bound execution, nonvacuous checks, and honest crash-path coverage. One low-severity test-fidelity finding follows; this is not an admission or a kill-rule verdict.

## Findings (severity order)

### Low — T2/T3 do not use the committed stub fixture bytes

/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py:234-246 defines an independent inline `STUB_TOOL` and derives `LYING_TOOL` by string replacement; :301-310 installs those strings, not `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/fixtures/stub_tool.py`:1-25. Byte comparison of the generated selftest fixture with `git show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/fixtures/stub_tool.py` gave:

```
T2 sha256=3b622aa5cc00cbfa267c05c07bfdcf99b4be48ceef99d26536674e283e6e9529 equals_committed_stub=False
T3 sha256=1ad894f8d43ece6a7cc2741238ca8cf9591afd6150cd7f6a19c31f059d5be7ce equals_committed_stub=False
committed_stub_sha256=7c78a05df78703044f8fe8fa02793a63b580f6353f58e8ebcee836038762edde
```

The exact comparison was `b == committed_stub`, where `b = (scratch/'fixtures'/relative/'scripts/quote_class.py').read_bytes()` and `committed_stub` was stdout of `['git','-C',str(lane),'show',f'{rev}:.ufo/waves/round-64/fixtures/stub_tool.py']`. T2's directly executed `--selftest --json` stdout is byte-identical to the committed stub's stdout (both exit 0), so this is test duplication/drift exposure, **not** a current semantic bypass. The committed fixture also contains explanatory documentation and separate imports, accounting for byte/AST differences. A future selftest should source its attack bytes from the committed fixture and derive the lying variant explicitly, rather than treating 11/11 as proof of exact committed-stub reproduction. Frozen files were not modified.

## T7: genuine E2E over real base bytes

/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py:331-344 obtains all seven blobs using `git_show(root, BASE, rel)`, commits them into a dedicated fixture, and launches the unchanged counter in a child Python process (:284-289). The production path (:147-184) checks the tool SHA, reads fixture blobs through git, materializes them, then actually runs the tool's `--selftest --json`. Its own independent classification runs at :208-223. `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py`:76-100 reads the raw/text files and derives all four cases; it does not merely print canned expectations.

I compared each generated T7 file byte-for-byte against `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 1a48131577ba82c967650561be34e8dba909432a:<relative-path>`. All comparisons were true:

```
scripts/quote_class.py: bytes=4914 sha256=431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14 equals_base=True
scripts/fixtures/quote-class/inline.raw.html: bytes=52 sha256=1ac3d2484335a998876781044be5741696c741c889fa166dc40b3502a4bf82c6 equals_base=True
scripts/fixtures/quote-class/inline.txt: bytes=45 sha256=b47cc0f104b62d4c7c30bcd68fd8e67613e287dc4ad8c310ef10cbadea9c4380 equals_base=True
scripts/fixtures/quote-class/markup.raw.html: bytes=115 sha256=5af86cbb88d7aad6a7cf93cc1a097eac44f247fe3b2a7b372acb827ad6e7f26e equals_base=True
scripts/fixtures/quote-class/markup.txt: bytes=56 sha256=415364a087053dd18c8299b4c6545a9e0cf59b2b95f23084c634401e26e621fd equals_base=True
.ufo/waves/round-61/sources/S432.html: bytes=1854393 sha256=63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b equals_base=True
.ufo/waves/round-63/quote-class/S432.txt: bytes=290480 sha256=8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69 equals_base=True
```

## Check coverage / vacuity / T5

- All eleven expectations are appended and evaluated on the successful path (:295-344); `checks` cannot stay empty on an ordinary successful invocation. Missing T7 base bytes return exit 2 (:336-339), not a green 0/0.
- T1 has two checks, T2 two, T3 one, T4 two, T5 one, T6 one, T7 two: **11 assertions, not 11 separate scenarios**.
- T2/T3 are genuine hash-rejection checks. They do not exercise rejection of lying JSON after execution, and T3's individual expectation checks only the mismatch token (not exit status). The observed T3 nevertheless exits 1 and prints `met=false`.
- T4 calls `safe_json` directly on malformed JSON and a JSON array. It is a parser-unit test, not an E2E hostile-output test. It does not establish that every nested hostile dictionary shape is handled; no production exploit is demonstrated because only the frozen tool executes.
- T5's crash script is **not executed by the counter**: production's SHA check at :153-157 returns before fixture loading or subprocess execution. T5 is consequently an early-rejection test, not coverage of the nonzero-tool-exit branch at :186-189. This limitation is honestly documented at :21-25 and :318-324, and the test is named `t5 mismatch-first`. There is no claim that the controlled crash exits 3 through production.
- T7 is the positive-path execution check, not vacuous sha-only coverage. It observed `selftest=4/4 frozen_cases=ok rederive=agree met=true`.

## Exact execution evidence

Frozen script was materialized by the read-only command:

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/c64_quote_tool.py
```

Its stdout was written only to the seat scratch counter path. SHA256 was `96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b`, matching the frozen assignment.

All Python commands below ran with cwd `/fast/scratch/hyaku/kake-r64/ReviewerC2Selftest`, explicit `TMPDIR=/fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/tmp`, and `PYTHONDONTWRITEBYTECODE=1`. The counter's fixture builder itself verifies fixture repository top-level before its first commit (:262-269). No mutating git command was issued against the lane; the requested selftest created only its own scratch fixture repositories.

```
python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/c64_quote_tool.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --selftest --selftest-work /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/fixtures
check t1 exit1: pass
check t1 present0: pass
check t2 exit1: pass
check t2 mismatch: pass
check t3 mismatch: pass
check t4 garbage: pass
check t4 notobject: pass
check t5 mismatch-first: pass
check t6 exit2: pass
check t7 exit0: pass
check t7 green: pass
selftest 11/11
exit=0; stderr empty

python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/c64_quote_tool.py --root /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/fixtures/t2-stub --revision HEAD
revision=HEAD present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
exit=1; stderr=''

python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/c64_quote_tool.py --root /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/fixtures/t3-lying --revision HEAD
revision=HEAD present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
exit=1; stderr=''

python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/c64_quote_tool.py --root /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/fixtures/t5-crash --revision HEAD
revision=HEAD present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
exit=1; stderr=''

python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/c64_quote_tool.py --root /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/fixtures/t7-real --revision HEAD
revision=HEAD present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true
exit=0; stderr=''
```

T2/committed-stub stdout equivalence was measured by executing `python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/fixtures/t2-stub/scripts/quote_class.py --selftest --json` and `python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC2Selftest/committed-stub.py --selftest --json`. Both returned exit 0; direct `stub_runs[0] == stub_runs[1]` printed `True`. The latter path contained exactly the revision's committed fixture bytes.

## Residual risk / verification gaps

The LSP device was unavailable: `read xd://lsp` returned `No such tool: xd://lsp`. No semantic references/definition/diagnostics claims are made; fallback evidence is direct source/diff inspection and the executed subprocesses. Actual diff inspected with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- .ufo/waves/round-64/c64_quote_tool.py` (new 374-line counter).

No saturation, exhaustive hostile-shape coverage, or post-pin arbitrary-tool execution coverage is claimed. This seat did not re-run the separate c63 committed-fixture differential or evaluate C1/C3: those are outside its selftest assignment. One Python runtime was used, with subprocesses explicitly required by the canonical counter. No resume path exists in the reviewed counter, so resume continuity/rerouting requirements have no affected callsite here.

No tools installed or updated. Scratch tree removed before terminal delivery; only this report is retained.

Self-evaluation: accuracy 4/5 (static branch reasoning is distinguished from execution); completeness 4/5 (separate committed c63 differential deliberately excluded); clarity 4/5 (detailed evidence retained); actionability 4/5 (specific fixture-source recommendation, no edits); conciseness 4/5 (full hashes/commands lengthen report). Overall 4.0; user-facing conclusion remains bounded to the assigned selftest.
