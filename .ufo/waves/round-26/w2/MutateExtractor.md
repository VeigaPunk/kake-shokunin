# Round-26 W2 — MutateExtractor

## Scoped verdict

**DISAGREE — low-severity detector-coverage finding.** Six independent extractor mutations were exercised: **5 killed, 1 survived, 0 inconclusive**. Narrowing HTML sniffing from `<html` to `<html>` survives the entire existing selftest despite changing the output for an attributed HTML opening tag without a content type.

Axes: **freshness** (faithful extraction of retained source bytes) and **operability** (the bounded selftest detects plausible extractor regressions). This is not a judgment on the complete C1 claim, the 32-row counter, or the candidate's actual HTML-sniffing implementation. The surviving defect was deliberately injected; the pristine implementation handles the demonstrated input correctly.

Candidate label supplied by the assignment: `e28312b14b076584fedd696fae2a684e460bd11e`. Tested working-file bytes are identified by SHA-256 below; no Git/index inspection or modification was performed.

## Isolation and detector

The controlling hard bounds permit only this report to be written and require scratch to remain in memory. Accordingly, both scripts were copied into isolated in-memory modules, not an on-disk `w2-scratch-*` directory. No disk scratch was created, so there was no scratch directory to delete. Original scripts, corpus, manifests, retained views, and sibling files were not edited.

Actual execution used `functions.eval(language="py")` in the existing **Python 3.14.8** interpreter. There was no shell command, subprocess, alternative model/runtime, network request, or subagent dispatch. No tools were installed or updated; the existing Python standard library was sufficient. No pacman transaction or host-service change was attempted.

The detector was the byte-identical copied `.ufo/waves/round-26/text_selftest.py`. Its original `__file__` supplied the existing ROOT/layout. The only harness substitution was its source-module loader: requests for `source_text.py` received the isolated source module. Reference-module loading, test cases, manifest/retry handling, assertions, and all retained inputs were unchanged. Bytecode writes were disabled during detector execution.

Relevant executed harness statements were:

```python
source_original = source_path.read_bytes()
selftest_original = selftest_path.read_bytes()
exec(compile(source_bytes, str(source_path), 'exec'), source.__dict__)
exec(compile(selftest_original, str(selftest_path), 'exec'), detector.__dict__)
original_loader = detector.load_module

def memory_loader(name, path):
    if Path(path) == source_path:
        return source
    return original_loader(name, path)

detector.load_module = memory_loader
exit_code = detector.main()
```

Each of six independent branches ran **pristine → one mutation → exact-byte restoration**, with restoration in `finally`, then reran the same detector. Branches ran concurrently using `ThreadPoolExecutor(max_workers=6)` in that same interpreter. A failing pristine/restored run or harness exception would have made its result inconclusive, not killed.

The unchanged detector runs 73 cases: 29 text cases, 6 normalization cases, 1 differential normalization case, 3 manifest/inventory checks, and 34 retained-fetch-view checks. Relevant code: `text_selftest.py:181-204`; retained-view checks at `text_selftest.py:135-150` and effective-fetch enumeration at `text_selftest.py:153-178`.

Actual initial output:

```text
baseline exit=0 passed=True total=73 failed=[]
```

## Mutants, expected detectors, and actual results

All paths and line numbers in this report are relative to the lane. The two script names in the tables abbreviate `.ufo/waves/round-26/source_text.py` and `.ufo/waves/round-26/text_selftest.py`.

| ID | Smallest behavior-bearing mutation | Expected detector | Actual pristine / mutant / restored exits | Mutant failures | Verdict |
|---|---|---|---|---:|---|
| M01 | `source_text.py:42`: `return normalize(decoded)` → `return normalize(__import__('html').unescape(decoded))` | Double-encoded-entity fixtures at `text_selftest.py:45-46`; plain entity passthrough at `:50-51` | `0 / 1 / 0` | 7 / 73 | killed |
| M02 | `source_text.py:7`: remove `'noscript', ` from `SKIP` | `skip_noscript`, `skip_nested_noscript_template` at `text_selftest.py:32,35` | `0 / 1 / 0` | 2 / 73 | killed |
| M03 | `source_text.py:31`: replace regex `r'\s+([,.;:)])'` with `r'\s+([,.;:)\]])'`, removing whitespace before `]` again | Bracket-spacing fixture at `text_selftest.py:73` and differential inputs at `:84-86` | `0 / 1 / 0` | 19 / 73 | killed |
| M04 | `source_text.py:22`: `self.skip -= 1` → `self.skip = 0` | Nested skip fixtures at `text_selftest.py:35-36` | `0 / 1 / 0` | 2 / 73 | killed |
| M05 | `source_text.py:35`: `errors='replace'` → `errors='ignore'` | Five invalid-UTF-8 fixtures at `text_selftest.py:59-63` | `0 / 1 / 0` | 5 / 73 | killed |
| M06 | `source_text.py:36`: `.startswith(('<!doctype', '<html'))` → `.startswith(('<!doctype', '<html>'))` | The existing sniff fixture at `text_selftest.py:58` would need an attributed opening tag; its bare `<html>` input does not distinguish the mutant | `0 / 0 / 0` | 0 / 73 | **survived** |

Every pristine, mutated, and restored invocation reached all 73 cases. Actual captured JSON summaries, projected to `passed`, `total`, and `failed` without changing their values:

```json
{"id":"M01","pristine":{"passed":true,"total":73,"failed":[]},"mutated":{"passed":false,"total":73,"failed":["entities_amp_lt_decoded_once","entities_amp_amp_decoded_once","plain_entities_and_tags_untouched","fetch_view:S012-1","fetch_view:S024-1","fetch_view:S026-1","fetch_view:S031-1"]},"restored":{"passed":true,"total":73,"failed":[]}}
{"id":"M02","pristine":{"passed":true,"total":73,"failed":[]},"mutated":{"passed":false,"total":73,"failed":["skip_noscript","skip_nested_noscript_template"]},"restored":{"passed":true,"total":73,"failed":[]}}
{"id":"M03","pristine":{"passed":true,"total":73,"failed":[]},"mutated":{"passed":false,"total":73,"failed":["normalize_square_bracket_spacing_as_accessibility_packet","normalize_matches_accessibility_packet","fetch_view:S006-1","fetch_view:S007-1","fetch_view:S010-1","fetch_view:S011-1","fetch_view:S017-1","fetch_view:S020-1","fetch_view:S023-1","fetch_view:S024-1","fetch_view:S025-1","fetch_view:S026-1","fetch_view:S027-1","fetch_view:S028-1","fetch_view:S029-1","fetch_view:S030-1","fetch_view:S031-1","fetch_view:S033-1","fetch_view:S034-1"]},"restored":{"passed":true,"total":73,"failed":[]}}
{"id":"M04","pristine":{"passed":true,"total":73,"failed":[]},"mutated":{"passed":false,"total":73,"failed":["skip_nested_noscript_template","skip_nested_template"]},"restored":{"passed":true,"total":73,"failed":[]}}
{"id":"M05","pristine":{"passed":true,"total":73,"failed":[]},"mutated":{"passed":false,"total":73,"failed":["utf8_invalid_byte_plain","utf8_overlong_and_stray_continuation","utf8_truncated_sequence","utf8_invalid_in_html","utf8_invalid_run"]},"restored":{"passed":true,"total":73,"failed":[]}}
{"id":"M06","pristine":{"passed":true,"total":73,"failed":[]},"mutated":{"passed":true,"total":73,"failed":[]},"restored":{"passed":true,"total":73,"failed":[]}}
```

Representative actual failure details, verbatim values from detector output:

```json
{"mutant":"M01","case":"entities_amp_lt_decoded_once","passed":false,"detail":{"expected":"&lt;","actual":"<","second_call":"<"}}
{"mutant":"M02","case":"skip_noscript","passed":false,"detail":{"expected":"Shown","actual":"Enable JS Shown","second_call":"Enable JS Shown"}}
{"mutant":"M03","case":"normalize_square_bracket_spacing_as_accessibility_packet","passed":false,"detail":{"expected":"x [ y ] z","actual":"x [ y] z"}}
{"mutant":"M04","case":"skip_nested_template","passed":false,"detail":{"expected":"d","actual":"c d","second_call":"c d"}}
{"mutant":"M05","case":"utf8_invalid_byte_plain","passed":false,"detail":{"expected":"a\ufffdb","actual":"ab","second_call":"ab"}}
```

Criterion-specific agreement: the amendment explicitly requires `single entity decode` and `no "]" spacing rule` (`.ufo/waves/round-26/contract-amendment.json:15`). M01 and M03 falsify exactly those requirements and are killed both synthetically and by retained-view comparisons: respectively 4 and 17 retained views disagree. Skip-tag, nesting, and invalid-UTF-8 regressions are also killed. These observations support those particular checks, not universal extractor coverage.

## Surviving mutant is behaviorally different

Exact source evidence:

- `.ufo/waves/round-26/source_text.py:36` currently uses `decoded.lstrip()[:15].lower().startswith(('<!doctype', '<html'))`. The pristine `<html` prefix includes attributed opening tags.
- `.ufo/waves/round-26/text_selftest.py:58` contains only `('sniff_html_without_content_type', b'<html><body>Hi</body></html>', None, 'Hi')` for the no-doctype HTML-sniff fixture. Both the original prefix and mutant match its bare opening tag.
- `text_selftest.py:109-114` checks two calls against the expected output. The same existing `text_case` helper was used to demonstrate the missing input, without modifying the 73-case detector.

Additional witness invocation within the assigned M06 probe:

```python
raw = b'<html lang="en"><body>Hi</body></html>'
detail = witness_test.text_case(module.text_of, raw, None, 'Hi')
actual = module.text_of(raw, None)
```

Actual outputs:

```json
{"stage":"pristine","input":"<html lang=\"en\"><body>Hi</body></html>","content_type":null,"expected":"Hi","actual":"Hi","text_case_detail":null}
{"stage":"mutated","input":"<html lang=\"en\"><body>Hi</body></html>","content_type":null,"expected":"Hi","actual":"<html lang=\"en\"><body>Hi</body></html>","text_case_detail":{"expected":"Hi","actual":"<html lang=\"en\"><body>Hi</body></html>","second_call":"<html lang=\"en\"><body>Hi</body></html>"}}
{"stage":"restored","input":"<html lang=\"en\"><body>Hi</body></html>","content_type":null,"expected":"Hi","actual":"Hi","text_case_detail":null}
```

Thus M06 is not an equivalent mutant: it leaks markup instead of extracting visible text for an input the original implementation supports. The existing full detector nevertheless returns exit 0 with all 73 cases passing.

### Minimal correction

Add one `TEXT_CASES` entry immediately after `.ufo/waves/round-26/text_selftest.py:58`:

```python
('sniff_html_with_attributes_without_content_type',
 b'<html lang="en"><body>Hi</body></html>', None, 'Hi'),
```

No production-code change or contract weakening is indicated. The witness above already exercised this input through the existing case helper and distinguished pristine/mutated/restored behavior. The fixture was **not** inserted into the authoritative selftest, and no claim is made that a modified full suite was run.

## Hashes and restoration evidence

Common pristine source hash **B**:

```text
55ae7abc52a5acfd95a86d96c27f12898c30e33ab63cfa7f383640120f57b7d6
```

For every branch, the before hash and restored hash were exactly **B**. Mutated source hashes were:

| ID | Before | Mutated SHA-256 | Restored |
|---|---|---|---|
| M01 | B | `a96b91508716385c71f1b1ba7ef6691c1e1ac6ce855003396b4d1ce6fb4c2578` | B |
| M02 | B | `dc5cced8f8464cf2e3e9312a1dbdfaf1306e5e40cfd93e5d46b5f09095d8ff70` | B |
| M03 | B | `5b1e08a350f5d1e09ebc4b1b3fa184c6744c335b49c419b04a9b5b79cca44b4c` | B |
| M04 | B | `1a724b695940c3fcec844b8fc1018d9da7d3f8a1ab90061b7fe1b80770ed0fb3` | B |
| M05 | B | `b622ac6388ff6a9c49dee5112459c6ea12cfe21f985ca7c32d10b7998cfe69b4` | B |
| M06 | B | `7e718df7c8ad073634e9eefc8f9432fd1196368da8ff4e67163d5b327aa02779` | B |

Actual on-disk before/after hash output, taken after all six full detector probes:

```json
{"before":{"source_text.py":"55ae7abc52a5acfd95a86d96c27f12898c30e33ab63cfa7f383640120f57b7d6","text_selftest.py":"6c829ceee4988f8fe241b2faca15c3dc722044ea0012fa780c617c17bb8554bb"},"after":{"source_text.py":"55ae7abc52a5acfd95a86d96c27f12898c30e33ab63cfa7f383640120f57b7d6","text_selftest.py":"6c829ceee4988f8fe241b2faca15c3dc722044ea0012fa780c617c17bb8554bb"},"exact":true}
```

All six restored detectors returned exit 0 / 73 cases / no failures. In-memory restoration was exact, and neither authoritative script needed an on-disk restoration because neither was modified. Only this report was written. The assigned mutation probe is complete; no integration or shipping action was taken.

```json
{"target":".ufo/waves/round-26/source_text.py + .ufo/waves/round-26/text_selftest.py (mutation-detector coverage)","verdict":"DISAGREE","severity":"low"}
```
