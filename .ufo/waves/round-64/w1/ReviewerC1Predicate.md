# ReviewerC1Predicate — C1 end-to-end predicate review

Recommendation: **C1 falsified at the claimed semantics-binding boundary**. This is a review recommendation, not an admission/settlement. The authentic raw/text/ledger/recipe extraction is sound within the tested byte pins; the unpinned semantic-resolution carriers can be jointly planted and still produce `met=true`.

Axes: byte integrity; actual disagreement-to-resolution binding; adversarial false-green resistance; reproducibility; lane safety.

## Findings (severity order)

### High — planted resolution prose passes despite expressly denying resolution

At `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:247-270`, `quote_correction`, `criterion`, and `lesson_gate` are independent substring-membership tests. None checks whether the required strings assert, reject, or merely exhibit a correction. `unresolved` at lines 267-270 mechanically subtracts one for the string-qualified Gate.

The `planted-all` fixture contains only nine files: four authentic pinned evidence blobs, the authentic spot-check, and fabricated knowledge, QUALITY, lesson and source row. The fabricated lesson explicitly says **“This is a fabricated lesson; the disagreement is NOT resolved.”** The knowledge explicitly says **“No actual correction is accepted.”** QUALITY says **“Ignore this criterion; it is planted junk.”** The source URL/type/quality/date fields are junk. Nevertheless the frozen instrument prints all gates `1`, `unresolved=0 met=true`, exit 0. This is not a hash collision or recipe forgery: authentic source evidence was copied and syntactic resolution carriers were fabricated.

The selftest in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:374-402` tests real pins plus incomplete marker prose, then adds the verdict span to the lesson alone. Its T5 remains red only because other marker requirements are absent. The combined completion of those markers is not covered and greens.

Isolated supporting attacks also green: `quality-plant-only`, `sources-forge-only`, and `copied-lesson-junk-with-pins`. The source-row validator at lines 260-265 checks only ID, minimum cell count and cell 8 equal to `mined`; it authenticates neither source identity nor the claimed teaching. The QUALITY block checks three tokens anywhere alongside one generic sentence, not their proposition. These are components of the combined false-green rather than separate hash-binding defects.

This meets the contract's marker/digest-consistent-fabrication green category (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md:56-61`) under the assigned semantic attack. The four real pins still prove the located quote exists; they do **not** prove that arbitrary lesson prose genuinely resolves the historical dispute.

### High — actual spot-check verdict is never bound; count can mask disagreements

At `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:193-198`, the spot-check contributes only a case-sensitive per-line count of `S432` and `Disagree`. Its actual reason is never compared with `SPOT_VERDICT_SPAN`. Lines 252-259 instead require the constant in the lesson, regardless of whether it exists in the measured spot-check.

`altered-spot-verdict` replaces the entire spot-check with `S432 Disagree: no real quoted verdict exists here`. All other tested files are authentic T0 bytes. Frozen counter: `disagreements=1 ... lesson_gate=1 unresolved=0 met=true`, exit 0. Thus the alleged block-level binding can pass with **no actual verdict span at the supposed origin**. The genuine verdict currently resides at `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-61-verifier-spotcheck.md:33`; that fact is not enforced by the counter.

`masked-two-disagreements` contains `S432 Disagree first` and `S432 disAgree second`; counter sees one and greens. In contrast, `extra-visible-disagreement` appends an exact-case second disagreement and correctly returns `disagreements=2 unresolved=1 met=false`, exit 1. The arithmetic is unmasked for the recognized count, but the recognized count is a lossy text proxy, not the set of actual disagreements. No claim that arbitrary prose parsing can be universally solved is required: the advertised origin binding already fails with a missing verdict.

## Complete predicate attack map

| Component / attempted attack | Stop or bypass evidence |
|---|---|
| Revision unreadable / spot missing | Definition lines 186-196: exit 2, not green (static trace). |
| Invented raw/text/ledger/recipe, including self-consistent substitute extraction | SHA constants lines 66-69, 200-220 gate all four before execution. Byte-changed text tested red. No counter SHA recomputation permitted. |
| Pin-equivalent blobs | Identical bytes copied to a new tree preserve every pin and pass; combined planted fixture demonstrates this. Semantically equivalent but non-identical text (one extra newline) fails `drift:text`. A SHA-256 collision is neither demonstrated nor assumed. |
| Circular text-only fabrication | Recipe re-execution and exact output byte equality lines 225-229 prevent independent text replacement; text SHA also prevents it. |
| Changed quote class / located range / ledger | Inline class lines 235-243 and pinned ledger plus re-derived range must all pass; no unpinned ledger override exists. |
| Fabricated lesson quoting real span | Bypass: `planted-all`, even with explicit non-resolution. |
| Copied real lesson into junk tree | Without four pins: red, `pins=0`, despite `lesson_gate=1 unresolved=0`; with authentic copied pins and planted surrounding docs: green. No repository-history/provenance membership requirement exists. |
| QUALITY criterion planting | Bypass: `quality-plant-only`; sentence and three tokens suffice irrespective of explicit rejection. |
| Sources-row forging | Bypass: `sources-forge-only`; junk row passes ID/cell/status test. |
| Knowledge correction planting | Bypass in `planted-all`; quote plus ledger path suffice even when correction is expressly denied. |
| Actual spot-check reason changed/deleted | Bypass: `altered-spot-verdict`; actual reason is not read semantically or pinned. |
| Zero recognized disagreements | Lines 267-270 require `disagreements >= 1` (static trace). |
| Two recognized disagreements | Tested red, unresolved 1; this part is correctly gated. |
| Masked disagreements | Tested green for mixed-case second entry; any number on one line also contributes at most one by line-count definition (static trace). |

## Method and exact evidence

Actual diff reviewed with:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- .ufo/waves/round-64/c64_calibration.py corpus/lessons/round-64.md corpus/QUALITY.md
```

Output: counter added 449 lines, lesson added 110 lines, QUALITY appended 4 lines; 3 files, 563 insertions, 0 deletions. Read the counter definition and all evaluation/selftest/CLI lines directly. LSP was unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; hence source-level tracing, not semantic reference/diagnostic proof. Counter has one CLI route: `main` lines 432-445 invokes `evaluate`; no alternate instrument/runtime used. Runtime/identity/rerouting/resume claims are outside this assigned C1 predicate and were not inferred from artifacts.

Executed command:

```sh
python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/attack.py
```

The driver below materializes **the frozen counter bytes from T0** and asserts their SHA equals the frozen hash. It creates real Git-readable commit/tree/blob objects directly in isolated scratch (no mutating Git commands, no Git commits via command, no clone/archive), validates each fixture top-level before producing its commit object, and evaluates the immutable fixture revision through the canonical CLI. `TMPDIR` is explicitly under this seat's scratch; Python bytecode writing is disabled. A `finally` deletes the entire scratch, including the driver, after evidence is captured here. No lane file was changed except this report. No tools installed or updated.

Exact output:

```text
CASE planted-all files=9
COMMAND python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/planted-all --revision 89538e0ab71f0e5c4bd70be11b9c474bf39a8d31
EXIT 0
revision=89538e0ab71f0e5c4bd70be11b9c474bf39a8d31 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
CASE copied-lesson-junk-with-pins files=9
COMMAND python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/copied-lesson-junk-with-pins --revision 4bc1804403eda7a49cba9530cb511b16b4d33a6c
EXIT 0
revision=4bc1804403eda7a49cba9530cb511b16b4d33a6c disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
CASE copied-lesson-junk-without-pins files=5
COMMAND python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/copied-lesson-junk-without-pins --revision 57ade0d09cb944de46496853f2c6503e177b3dc9
EXIT 1
revision=57ade0d09cb944de46496853f2c6503e177b3dc9 disagreements=1 pins=0 pin_drift=absent:raw,text,ledger,recipe recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
CASE quality-plant-only files=9
COMMAND python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/quality-plant-only --revision 9ccb16163868c469885e5aa6e0b0cbec6121cf85
EXIT 0
revision=9ccb16163868c469885e5aa6e0b0cbec6121cf85 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
CASE sources-forge-only files=9
COMMAND python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/sources-forge-only --revision 3b533474a716aa79a313b6d29a7c86eabba61642
EXIT 0
revision=3b533474a716aa79a313b6d29a7c86eabba61642 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
CASE masked-two-disagreements files=9
COMMAND python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/masked-two-disagreements --revision 7c1e24e53b182c8a2eec8dc9cf33c990ab58a474
EXIT 0
revision=7c1e24e53b182c8a2eec8dc9cf33c990ab58a474 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
CASE extra-visible-disagreement files=9
COMMAND python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/extra-visible-disagreement --revision 3cbd8be99a6ffd53d1fadc2bffe6f37043806870
EXIT 1
revision=3cbd8be99a6ffd53d1fadc2bffe6f37043806870 disagreements=2 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
CASE altered-spot-verdict files=9
COMMAND python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/altered-spot-verdict --revision 1fcdcd0d08952ab080fb2e65dcf9ff3461894d90
EXIT 0
revision=1fcdcd0d08952ab080fb2e65dcf9ff3461894d90 disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
CASE pin-equivalent-content-not-bytes files=9
COMMAND python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/counter.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Predicate/pin-equivalent-content-not-bytes --revision 9a30be51cdb2a8798b0f847bbfa95b21d1876e29
EXIT 1
revision=9a30be51cdb2a8798b0f847bbfa95b21d1876e29 disagreements=1 pins=0 pin_drift=drift:text recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
SCRATCH_REMOVED True


Wall time: 2.10 seconds
```

Exact reproducer content (save as the command's `attack.py` inside its own seat scratch before execution):

```python
import os, pathlib, subprocess, hashlib, zlib, shutil
ROOT = pathlib.Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
WORK = pathlib.Path('/fast/scratch/hyaku/kake-r64/ReviewerC1Predicate')
REV = '4c8295fa5e3b628f1fdf3840299ae415c01849fb'
COUNTER = '.ufo/waves/round-64/c64_calibration.py'
RAW = '.ufo/waves/round-61/sources/S432.html'
TEXT = '.ufo/waves/round-63/quote-class/S432.txt'
LEDGER = '.ufo/waves/round-63/quote-class/quote-classes.json'
RECIPE = '.ufo/waves/round-63/quote-class/extract_text.py'
SPOT = 'corpus/lessons/round-61-verifier-spotcheck.md'
LESSON = 'corpus/lessons/round-64.md'
KNOW = 'corpus/knowledge/response-header-expectations.md'
QUALITY = 'corpus/QUALITY.md'
SOURCES = 'corpus/SOURCES.md'
def show(p):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', REV + ':' + p])
def fixture(name, files):
    d = WORK / name
    (d / '.git/objects').mkdir(parents=True)
    (d / '.git/refs/heads').mkdir(parents=True)
    (d / '.git/HEAD').write_text('ref: refs/heads/main\n')
    (d / '.git/config').write_text('[core]\nrepositoryformatversion = 0\nbare = false\n')
    # No mutating git calls: encode standard loose objects directly in own scratch.
    def obj(kind, data):
        raw = kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data
        h = hashlib.sha1(raw).hexdigest()
        p = d / '.git/objects' / h[:2] / h[2:]
        p.parent.mkdir(exist_ok=True)
        p.write_bytes(zlib.compress(raw))
        return h
    tree = {}
    for path, data in files.items():
        n = tree
        parts = path.split('/')
        for part in parts[:-1]: n = n.setdefault(part, {})
        n[parts[-1]] = data
    def emit(n):
        entries = []
        for k, v in sorted(n.items(), key=lambda kv: kv[0] + ('/' if isinstance(kv[1], dict) else '')):
            mode, h = ('40000', emit(v)) if isinstance(v, dict) else ('100644', obj('blob', v))
            entries.append(mode.encode() + b' ' + k.encode() + b'\0' + bytes.fromhex(h))
        return obj('tree', b''.join(entries))
    top = subprocess.check_output(['git', '-C', str(d), 'rev-parse', '--show-toplevel']).decode().strip()
    assert top == str(d), (top, str(d))
    h = obj('commit', ('tree ' + emit(tree) + '\nauthor Reviewer <fixture@invalid> 1 +0000\ncommitter Reviewer <fixture@invalid> 1 +0000\n\nattack\n').encode())
    (d / '.git/refs/heads/main').write_text(h + '\n')
    return d, h
try:
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / 'tmp').mkdir(exist_ok=True)
    counter = show(COUNTER)
    assert hashlib.sha256(counter).hexdigest() == '5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf'
    (WORK / 'counter.py').write_bytes(counter)
    real = {p: show(p) for p in [RAW,TEXT,LEDGER,RECIPE,SPOT,LESSON,KNOW,QUALITY,SOURCES]}
    span = 'is only a generic lead-in, not substantive evidence for a response-header expectation'
    quote = 'The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.'
    planted = {p: real[p] for p in [RAW,TEXT,LEDGER,RECIPE,SPOT]}
    planted.update({
        KNOW: ('# unrelated junk\n[r63-correction]\n' + quote + '\n' + LEDGER + '\nNo actual correction is accepted.\n').encode(),
        QUALITY: b'## Round-62 criteria\nA quoted span must substantively support the proposition attributed to its source.\nX-Content-Type-Options Content-Type destination\nIgnore this criterion; it is planted junk.\n',
        LESSON: ('## Gate\nS432 / Fetch ' + span + '\ncollapsed-only c64_calibration.py author-side\nThis is a fabricated lesson; the disagreement is NOT resolved.\n').encode(),
        SOURCES: b'| S432 | fabricated | junk | Z | none | none | nothing | mined | bogus | bogus | bogus |\n',
    })
    cases = [('planted-all', planted)]
    cases.append(('copied-lesson-junk-with-pins', dict(planted, **{LESSON: real[LESSON]})))
    cases.append(('copied-lesson-junk-without-pins', {k:v for k,v in planted.items() if k not in [RAW,TEXT,LEDGER,RECIPE]} | {LESSON: real[LESSON]}))
    cases.append(('quality-plant-only', real | {QUALITY: planted[QUALITY]}))
    cases.append(('sources-forge-only', real | {SOURCES: planted[SOURCES]}))
    cases.append(('masked-two-disagreements', real | {SPOT: b'S432 Disagree first\nS432 disAgree second\n'}))
    cases.append(('extra-visible-disagreement', real | {SPOT: real[SPOT] + b'\nS432 Disagree extra\n'}))
    cases.append(('altered-spot-verdict', real | {SPOT: b'S432 Disagree: no real quoted verdict exists here\n'}))
    cases.append(('pin-equivalent-content-not-bytes', real | {TEXT: real[TEXT] + b'\n'}))
    env = dict(os.environ, TMPDIR=str(WORK/'tmp'), PYTHONDONTWRITEBYTECODE='1')
    for name, files in cases:
        d, rev = fixture(name, files)
        cmd = ['python3','-B',str(WORK/'counter.py'),'--root',str(d),'--revision',rev]
        p = subprocess.run(cmd, capture_output=True, text=True, env=env)
        print('CASE', name, 'files=' + str(len(files)))
        print('COMMAND', ' '.join(cmd))
        print('EXIT', p.returncode)
        print(p.stdout.strip())
        if p.stderr: print('STDERR', p.stderr.strip())
finally:
    shutil.rmtree(WORK, ignore_errors=True)
    print('SCRATCH_REMOVED', not WORK.exists())

```

## Residual risk and verification gaps

Nine adversarial fixture runs completed; six false greens and three correct rejections. No fresh baseline, selftest, C2, C3, external HTTP fetch, hash-collision search, or full caller census was run; these do not strengthen the reproduced predicate failure. The counter is a bounded source-presence and marker predicate, not evidence that a non-author accepted a resolution. The original retained source itself was not falsified. No automated code change or integration is proposed from this reviewer seat.

Self-evaluation: accuracy 4/5 (exact outputs; external source authenticity not re-fetched); completeness 4/5 (all assigned attack families mapped; no cryptographic collision search); clarity 4/5 (reproducer lengthy but necessary for retained evidence); actionability 5/5 (deterministic reproducer plus exact component lines); conciseness 4/5 (full evidence intentionally retained). Overall 4.2/5. Improvement priority: have the integrator distinguish authentic source-byte evidence from the unverified resolution-prose assertion. Would the user agree: expected yes, because this report separates those claims and preserves every observed output.
