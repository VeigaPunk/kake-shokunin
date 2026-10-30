# ReviewerContract — round-64 contract-versus-reality audit

Verdict recommendation: **contract-fidelity divergences found; no frozen-sha mismatch found at T0**. This is a scoped review recommendation, not admission or settlement.

Axes: frozen-byte fidelity; fixture/receipt identity; predicate identity; fail-closed pin enforcement.

## Findings (severity ordered)

### Medium — the fifth named fixture is missing from the cited build manifest and builder

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md:19-26` presents five fixture revisions as built by `build_fixtures.py` with `controls/fixture-builds.txt` receipts. At receipt revision `cc8add1fa740b920ea5179a71152680ab220c70c`, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/fixture-builds.txt:1-4` contains only stub, marker, fabrication, and junk. The builder `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/fixtures/build_fixtures.py:114-142` likewise creates exactly those four repositories, not ledger-mut-repo. The four recorded revisions match the contract exactly; `5b981bd0c43dd30c1546a1966d971f4227f60973` has no entry in that manifest. Its separate `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/control-ledger-mut.txt:1-4` receipt names the revision but substitutes `<marker-repo + ledger locatedRawLines mutated 6150-6156>` and `<its HEAD>` for executable root/revision arguments. Thus the contract's common builder/manifest provenance claim does not cover every named fixture, and that control lacks the same exact-command reproducibility as the others. This does not establish that the recorded rejection is false.

### Low — the promised identical predicate sentences are not identical or present in receipt headers

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md:35-41,71-79,104-110` expressly promises identical sentences across contract, counter docstrings (C1/C2), lesson Mistakes (C3), and receipts. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:37-41` omits the command, all fixture IDs, and the explicit base ID; `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py:27-35` substitutes a builder reference for the stub revision and appends explanatory wording. These are substantively aligned outcomes, but not identical frozen sentences, even after removing Markdown and normalizing whitespace. `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-64.md:26-44` has the C3 narrative/map but not its frozen predicate sentence. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/after-c1.txt:1`, `after-c2.txt:1`, and `sweep-after.txt:1` are command headers referring to contract sections, not repeated predicates. Consequently the literal identity safeguard claimed by the contract is absent; I found no contrary success/failure outcome in those receipts.

## Successful checks and pin wiring

- Recomputed all nine full sha256 values explicitly named in the contract at T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`: four instruments, four C1 retained/derived inputs, and the C2 tool. All match. Exact executed commands/output appear below.
- All 17 distinct controls receipts named in the contract are present at `cc8add1fa740b920ea5179a71152680ab220c70c` (16 parsed `controls/*.txt` references plus the fully qualified fixture-builds receipt). After receipts explicitly identify T0 for C1/C2; sweep-after labels the tree T0 and reports offline partial OK, not remote-complete success.
- All four manifest-listed fixture revisions equal contract revisions and corresponding control receipt revisions. Ledger mutation is the exception described above, not a mismatched existing manifest row.
- C1 says pinned-sha drift makes the claim unprovable: contract lines 56-61 and counter docstring lines 9-12. It is enforced: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:200-214` compares revision blobs with `PIN_SHAS`; lines 268-270 require `pins` for `met`. Constants are at lines 62-95. `control-ledger-mut.txt:3-4` records ledger drift, pins=0, met=false, exit=1. No pin mismatch is hidden by a passing receipt.
- C2 states frozen tool sha drift is unprovable in contract lines 81-84. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py:147-157` reads the measured revision blob and returns exit 1 on mismatch before materialization/execution. `stub-c64.txt:2-3` records mismatch/met=false/exit=1; `stub-c63-defect.txt:2-3` records the same stub revision green under the old counter. The C2 kill-rule bullet alone does not repeat the sha clause, but the adjacent binding text states it and the implementation enforces it.
- C3 diff is only seven `line` increments; every `lineSha256` was already unchanged. All seven map hashes recomputed against the corresponding T0 SKILL.md line bytes match. This is consistent with restricting edits to those line/lineSha256 pairs; it does not imply all fourteen cells changed.

## Residual risk / verification gaps

- LSP unavailable: `read xd://lsp` returned `No such tool: xd://lsp` and mounted-device inventory has no lsp. Definition/reference/diagnostics requests therefore could not be made. Review uses literal committed source and git objects, not semantic-index absence claims.
- No counters, selftests, fixture builders, freshness sweeps, or alternate runtime were executed by this reviewer. Receipt bodies below are committed observations, not fresh test claims. Assignment explicitly asked byte/hash/receipt/predicate auditing; no mutating git command was used.
- `sweep-before.txt:1-10` is one unattributed stack trace with exit 2; it contains no three revision identifiers or per-revision commands. Contract lines 100-102 and lesson Mistakes attribute the same fault to three revisions, but this receipt alone does not establish all three. This is an evidence gap, not proof the historical claim is false.
- Runtime identity, rerouting, saturation, and resume-continuity preflights are not changed by these three claim instruments and are outside this contract-fidelity slice; no claims of their verification are made.
- No tools installed or updated. Only this report and own scratch directory were written; scratch removed before yield. Frozen inputs, receipts, contract, lesson, and lane working tree otherwise untouched.

## Evidence transcript

The git-show commands below were run read-only through Python subprocess, with their exact stdout captured. Line-numbered source excerpts are annotated renderings of committed blobs. Hash comparisons were initially calculated with hashlib, then the exact `git show | sha256sum` commands were also executed (exit 0 each).

```text
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/c64_calibration.py | sha256sum => 5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf; expected=5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf; match=True

git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/c64_quote_tool.py | sha256sum => 96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b; expected=96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b; match=True

git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/fixtures/build_fixtures.py | sha256sum => 7fbd8cbc67c17264096e44474a698b3f0d7702c3e1cc23f0b5bdaa26ee0271d3; expected=7fbd8cbc67c17264096e44474a698b3f0d7702c3e1cc23f0b5bdaa26ee0271d3; match=True

git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/fixtures/stub_tool.py | sha256sum => 7c78a05df78703044f8fe8fa02793a63b580f6353f58e8ebcee836038762edde; expected=7c78a05df78703044f8fe8fa02793a63b580f6353f58e8ebcee836038762edde; match=True

git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-61/sources/S432.html | sha256sum => 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b; expected=63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b; match=True; contract_contains=True

git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/S432.txt | sha256sum => 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69; expected=8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69; match=True; contract_contains=True

git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/quote-classes.json | sha256sum => 5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d; expected=5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d; match=True; contract_contains=True

git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/extract_text.py | sha256sum => 6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405; expected=6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405; match=True; contract_contains=True

git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:scripts/quote_class.py | sha256sum => 431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14; expected=431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14; match=True; contract_contains=True

git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/after-c1.txt => exit=0, bytes=447
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb (measured revision T0, contract .ufo/waves/round-64/contract.md §C1)
revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/after-c2.txt => exit=0, bytes=282
$ python3 -B .ufo/waves/round-64/c64_quote_tool.py --root . --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb (measured revision T0, contract §C2)
revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true
exit=0


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/base-c1.txt => exit=0, bytes=378
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision 1a48131577ba82c967650561be34e8dba909432a
revision=1a48131577ba82c967650561be34e8dba909432a disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/census-after.txt => exit=0, bytes=1408
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
kake	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
kake	W04	S427 duplicate url developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers across scopes
kake	W04	S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
census-after-exit=0


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/census-before.txt => exit=0, bytes=1409
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
kake	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
kake	W04	S427 duplicate url developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers across scopes
kake	W04	S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
census-before-exit=0


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/control-fabrication.txt => exit=0, bytes=434
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/l1/fixtures/fabrication-repo --revision f924538ede0d290d74af3126a40103887f4c8d46
revision=f924538ede0d290d74af3126a40103887f4c8d46 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/control-junk.txt => exit=0, bytes=461
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/l1/fixtures/junk-repo --revision 82dcba0d2f83bdd427c9566b33739af71fe84efc
revision=82dcba0d2f83bdd427c9566b33739af71fe84efc disagreements=1 pins=0 pin_drift=drift:raw,text,ledger,recipe recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/control-ledger-mut.txt => exit=0, bytes=482
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root <marker-repo + ledger locatedRawLines mutated 6150-6156> --revision <its HEAD>
ledger-mut revision 5b981bd0c43dd30c1546a1966d971f4227f60973
revision=5b981bd0c43dd30c1546a1966d971f4227f60973 disagreements=1 pins=0 pin_drift=drift:ledger recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/control-marker.txt => exit=0, bytes=429
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/l1/fixtures/marker-repo --revision 4c666e7632cb2093fbed18117e460bf37d1d14ce
revision=4c666e7632cb2093fbed18117e460bf37d1d14ce disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/selftest-c1.txt => exit=0, bytes=603
check t1 exit2: pass
check t1 token: pass
check t2 exit1: pass
check t2 disagreements: pass
check t2 pins0: pass
check t3 exit1: pass
check t3 drift: pass
check t3 nocrash: pass
check t4 exit1: pass
check t4 pins1: pass
check t4 recipe1: pass
check t4 class1: pass
check t4 located: pass
check t4 qcorr0: pass
check t4 gate0: pass
check t4 unresolved: pass
check t4 metfalse: pass
check t5 exit1: pass
check t5 gate1: pass
check t5 unresolved0: pass
check t5 metfalse: pass
check t6 guard: pass
check t6 notlist: pass
check t7 located: pass
check t8 exit2: pass
check t8 token: pass
selftest 26/26
c1=0


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/selftest-c2.txt => exit=0, bytes=275
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
c2=0


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/sidecar-repin-map.txt => exit=0, bytes=1044
sidecar re-pin map — old (pin commit 3d07733b, 2026-10-21) -> new (working tree 2026-10-30)
file line old->new  sha256(new line)  kind token
SKILL.md 364 -> 365  7070c25fb9ab6fd1220c9aa504c965290a47fb710093ae55d39124ec8baf4216  restored ~/Projects/ds4cc-marketplace
SKILL.md 445 -> 446  f08a35d9d8cb9daacc800e5841e80c5706e970ab2cc8a6053de40747abb6c29a  restored ~/Projects/ds4cc-marketplace
SKILL.md 448 -> 449  6e1baa1fa1e94c3d8da481df73d5661cb1ab4a33e676b62b3c815dbc30a48362  restored ~/Projects/ds4cc-marketplace
SKILL.md 449 -> 450  cfb08909875e4d89041654cfb43e1621cab46f39b6b79b893c2c00d210fb6f9e  restored ~/Projects/ds4cc-marketplace
SKILL.md 450 -> 451  c16c7a6a684caa3dc53763318280116126a0b2120efa04af390034f30e7a7b80  restored ~/Projects/ds4cc-marketplace
SKILL.md 423 -> 424  97576af9b60a58aa291049380cb651c4bce1199ace2b95dcb2eea2c5818cf710  restored ~/Projects/ds4cc-marketplace/burnerchrome
SKILL.md 431 -> 432  f2d75f7974459d29d55a33c03fa589ac10f1aedb1e0a97501d5f3fedb2aa4cc2  restored ~/Projects/ds4cc-marketplace/burnerchrome


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/stub-c63-defect.txt => exit=0, bytes=266
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root /fast/scratch/hyaku/kake-r64/l1/fixtures/stub-repo --revision 14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3
revision=14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/stub-c64.txt => exit=0, bytes=315
$ python3 -B .ufo/waves/round-64/c64_quote_tool.py --root /fast/scratch/hyaku/kake-r64/l1/fixtures/stub-repo --revision 14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3
revision=14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3 present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
exit=1


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/sweep-after.txt => exit=0, bytes=359
$ node scripts/freshness-sweep.mjs --offline (measured tree T0, contract §C3)
§armed
  all remote checks skipped(offline) — NOT counted as pass (complete=false)
skipped(offline): §armed (all remote checks) · §history (probe-history source absent — pin-declared) — complete=false, never counted as pass
VERDICT: OK (exit 0, partial: offline)
exit=0


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/sweep-before.txt => exit=0, bytes=809
freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:364
    at loadPathSidecar (file:///fast/scratch/hyaku/kake-r64/l1/sweep-base/scripts/freshness-sweep.mjs:386:13)
    at scanCitations (file:///fast/scratch/hyaku/kake-r64/l1/sweep-base/scripts/freshness-sweep.mjs:400:19)
    at runSections (file:///fast/scratch/hyaku/kake-r64/l1/sweep-base/scripts/freshness-sweep.mjs:1032:56)
    at main (file:///fast/scratch/hyaku/kake-r64/l1/sweep-base/scripts/freshness-sweep.mjs:1096:24)
    at file:///fast/scratch/hyaku/kake-r64/l1/sweep-base/scripts/freshness-sweep.mjs:1669:1
    at ModuleJob.run (node:internal/modules/esm/module_job:561:25)
    at async node:internal/modules/esm/loader:647:26
    at async asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:101:5)
sweep-before-exit=2


git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc8add1fa740b920ea5179a71152680ab220c70c:.ufo/waves/round-64/controls/fixture-builds.txt
1: {"name": "stub-repo", "path": "/fast/scratch/hyaku/kake-r64/l1/fixtures/stub-repo", "revision": "14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3"}
2: {"name": "marker-repo", "path": "/fast/scratch/hyaku/kake-r64/l1/fixtures/marker-repo", "revision": "4c666e7632cb2093fbed18117e460bf37d1d14ce"}
3: {"name": "fabrication-repo", "path": "/fast/scratch/hyaku/kake-r64/l1/fixtures/fabrication-repo", "revision": "f924538ede0d290d74af3126a40103887f4c8d46"}
4: {"name": "junk-repo", "path": "/fast/scratch/hyaku/kake-r64/l1/fixtures/junk-repo", "revision": "82dcba0d2f83bdd427c9566b33739af71fe84efc"}

git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- corpus/knowledge/freshness-sidecar.json
diff --git a/corpus/knowledge/freshness-sidecar.json b/corpus/knowledge/freshness-sidecar.json
index 53ae3eeb..0fa3d87a 100644
--- a/corpus/knowledge/freshness-sidecar.json
+++ b/corpus/knowledge/freshness-sidecar.json
@@ -57,7 +57,7 @@
   },
   {
    "file": "SKILL.md",
-   "line": 364,
+   "line": 365,
    "token": "~/Projects/ds4cc-marketplace",
    "lineSha256": "7070c25fb9ab6fd1220c9aa504c965290a47fb710093ae55d39124ec8baf4216",
    "kind": "restored",
@@ -66,7 +66,7 @@
   },
   {
    "file": "SKILL.md",
-   "line": 445,
+   "line": 446,
    "token": "~/Projects/ds4cc-marketplace",
    "lineSha256": "f08a35d9d8cb9daacc800e5841e80c5706e970ab2cc8a6053de40747abb6c29a",
    "kind": "restored",
@@ -75,7 +75,7 @@
   },
   {
    "file": "SKILL.md",
-   "line": 448,
+   "line": 449,
    "token": "~/Projects/ds4cc-marketplace",
    "lineSha256": "6e1baa1fa1e94c3d8da481df73d5661cb1ab4a33e676b62b3c815dbc30a48362",
    "kind": "restored",
@@ -84,7 +84,7 @@
   },
   {
    "file": "SKILL.md",
-   "line": 449,
+   "line": 450,
    "token": "~/Projects/ds4cc-marketplace",
    "lineSha256": "cfb08909875e4d89041654cfb43e1621cab46f39b6b79b893c2c00d210fb6f9e",
    "kind": "restored",
@@ -93,7 +93,7 @@
   },
   {
    "file": "SKILL.md",
-   "line": 450,
+   "line": 451,
    "token": "~/Projects/ds4cc-marketplace",
    "lineSha256": "c16c7a6a684caa3dc53763318280116126a0b2120efa04af390034f30e7a7b80",
    "kind": "restored",
@@ -192,7 +192,7 @@
   },
   {
    "file": "SKILL.md",
-   "line": 423,
+   "line": 424,
    "token": "~/Projects/ds4cc-marketplace/burnerchrome",
    "lineSha256": "97576af9b60a58aa291049380cb651c4bce1199ace2b95dcb2eea2c5818cf710",
    "kind": "restored",
@@ -201,7 +201,7 @@
   },
   {
    "file": "SKILL.md",
-   "line": 431,
+   "line": 432,
    "token": "~/Projects/ds4cc-marketplace/burnerchrome",
    "lineSha256": "f2d75f7974459d29d55a33c03fa589ac10f1aedb1e0a97501d5f3fedb2aa4cc2",
    "kind": "restored",


fixture-builds name=stub-repo revision=14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3 contract_match=True

fixture-builds name=marker-repo revision=4c666e7632cb2093fbed18117e460bf37d1d14ce contract_match=True

fixture-builds name=fabrication-repo revision=f924538ede0d290d74af3126a40103887f4c8d46 contract_match=True

fixture-builds name=junk-repo revision=82dcba0d2f83bdd427c9566b33739af71fe84efc contract_match=True

fixture-builds ledger-mut-repo present=False

C1 contract normalized predicate: at the measured revision, c64_calibration.py --root . --revision <measured> prints met=true (exit 0), and on each committed control fixture (marker-only 4c666e76, digest-consistent fabrication f924538e, junk 82dcba0d, ledger-mutation 5b981bd0) it prints met=false (exit 1), and at the base 1a481315 it prints met=false (exit 1).
C1 docstring normalized predicate: at the measured revision this counter prints met=true (exit 0); on each committed control fixture (marker-only, digest-consistent fabrication, junk, ledger-mutation) it prints met=false (exit 1); at the round-63 base it prints met=false (exit 1).
identical=False

C2 contract normalized predicate: at the measured revision, c64_quote_tool.py --root . --revision <measured> prints met=true (exit 0) over the lane tree; on the committed stub fixture (14fe2eab) it prints tool_sha=mismatch met=false (exit 1); and the round-63 counter c63_quote_tool.py run on that same stub fixture prints met=true (exit 0) — the routed round-63 defect, reproduced.
C2 docstring normalized predicate: at the measured revision this counter prints met=true (exit 0) over the lane tree; on the committed stub-fixture revision (fixture recipe .ufo/waves/round-64/fixtures/build_fixtures.py) it prints tool_sha=mismatch met=false (exit 1); and the round-63 counter c63_quote_tool.py, run on that same stub fixture, prints met=true (exit 0) — the routed round-63 defect, reproduced. (At the round-63 base the real tool already exists, so the base tree also prints met=true; the stub differential is the claim's falsifiable before/after, not the base.)
identical=False

C3 lesson Mistakes contains frozen predicate sentence=False

after-c1.txt:1 header=$ python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb (measured revision T0, contract .ufo/waves/round-64/contract.md §C1)

after-c2.txt:1 header=$ python3 -B .ufo/waves/round-64/c64_quote_tool.py --root . --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb (measured revision T0, contract §C2)

sweep-after.txt:1 header=$ node scripts/freshness-sweep.mjs --offline (measured tree T0, contract §C3)

T0 SKILL.md:365 sha256(no newline)=7070c25fb9ab6fd1220c9aa504c965290a47fb710093ae55d39124ec8baf4216 expected=7070c25fb9ab6fd1220c9aa504c965290a47fb710093ae55d39124ec8baf4216 match=True

T0 SKILL.md:446 sha256(no newline)=f08a35d9d8cb9daacc800e5841e80c5706e970ab2cc8a6053de40747abb6c29a expected=f08a35d9d8cb9daacc800e5841e80c5706e970ab2cc8a6053de40747abb6c29a match=True

T0 SKILL.md:449 sha256(no newline)=6e1baa1fa1e94c3d8da481df73d5661cb1ab4a33e676b62b3c815dbc30a48362 expected=6e1baa1fa1e94c3d8da481df73d5661cb1ab4a33e676b62b3c815dbc30a48362 match=True

T0 SKILL.md:450 sha256(no newline)=cfb08909875e4d89041654cfb43e1621cab46f39b6b79b893c2c00d210fb6f9e expected=cfb08909875e4d89041654cfb43e1621cab46f39b6b79b893c2c00d210fb6f9e match=True

T0 SKILL.md:451 sha256(no newline)=c16c7a6a684caa3dc53763318280116126a0b2120efa04af390034f30e7a7b80 expected=c16c7a6a684caa3dc53763318280116126a0b2120efa04af390034f30e7a7b80 match=True

T0 SKILL.md:424 sha256(no newline)=97576af9b60a58aa291049380cb651c4bce1199ace2b95dcb2eea2c5818cf710 expected=97576af9b60a58aa291049380cb651c4bce1199ace2b95dcb2eea2c5818cf710 match=True

T0 SKILL.md:432 sha256(no newline)=f2d75f7974459d29d55a33c03fa589ac10f1aedb1e0a97501d5f3fedb2aa4cc2 expected=f2d75f7974459d29d55a33c03fa589ac10f1aedb1e0a97501d5f3fedb2aa4cc2 match=True

$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/c64_calibration.py | sha256sum
5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf  -
exit=0

$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/c64_quote_tool.py | sha256sum
96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b  -
exit=0

$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/fixtures/build_fixtures.py | sha256sum
7fbd8cbc67c17264096e44474a698b3f0d7702c3e1cc23f0b5bdaa26ee0271d3  -
exit=0

$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/fixtures/stub_tool.py | sha256sum
7c78a05df78703044f8fe8fa02793a63b580f6353f58e8ebcee836038762edde  -
exit=0

$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-61/sources/S432.html | sha256sum
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  -
exit=0

$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/S432.txt | sha256sum
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  -
exit=0

$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/quote-classes.json | sha256sum
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  -
exit=0

$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/extract_text.py | sha256sum
6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405  -
exit=0

$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:scripts/quote_class.py | sha256sum
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  -
exit=0

T0 corpus/lessons/round-64.md:30
| survivor (a standing gate could-not-evaluate for ~8 rounds, unnoticed) | `corpus/knowledge/freshness-sidecar.json` was last re-pinned at round-24 (`3d07733b`, 2026-10-21). SKILL.md growth after that (first post-pin edits `f8438a28`/`4cb225fb`, round 56, 2026-10-25) shifted seven pinned lines by +1; `scripts/freshness-sweep.mjs --offline` then failed `paths sidecar binding invalid: SKILL.md:364` at the round-60 tip `9f671056`, the round-61 base `d2da25de`, and the round-63 base `1a481315` — receipt `.ufo/waves/round-64/controls/sweep-before.txt` (exit 2, same fault at all three; resolver table `controls/sidecar-repin-map.txt`). Rounds 56–63 landed without running the sweep, so the lane's own drift instrument could not evaluate while real rounds landed. | none at break time; after round 59 the QUALITY criterion "A frozen claim never silently turns a standing gate red" existed but no build-phase duty applied it to SKILL.md-side line shifts, and rounds 60–63 did not run the sweep at all. | This round's re-pin (7 entries, old→new recorded below) returns the sweep to exit 0 (`.ufo/waves/round-64/controls/sweep-after.txt`), and the round-64 QUALITY criterion makes a draft-phase §paths re-run a build duty for any round that edits a sidecar-pinned file. |

Named controls receipt count (including separately parsed fixture-builds.txt)=17
```

## Review self-evaluation

Accuracy 4/5: committed bytes and exact hashes support findings; receipt execution not independently rerun. Completeness 4/5: every requested contract item covered, with missing fifth-manifest entry explicitly exposed. Clarity 4/5: findings separated from evidence gaps; transcript is necessarily detailed. Actionability 4/5: exact divergent file/line locations supplied; frozen artifacts intentionally not edited. Conciseness 4/5: transcript retains commands/output requested by assignment. Overall 4.0/5. Highest-value improvement is a canonical predicate text reference and explicit fifth-fixture provenance in a later, non-frozen round.
