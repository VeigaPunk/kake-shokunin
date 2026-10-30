# ExecQuoteClassMatrix

Scope: differential check of `scripts/quote_class.py` against `classify()` in `.ufo/waves/round-64/c64_calibration.py`. No source, counter, receipt, or fixture files changed. Private test files were removed after execution.

## Evidence and method

Sources inspected:
- `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py:32-37` — CLI classifier: raw membership, then text membership, else absent.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:113-119` — inline classifier has the same three ordered branches.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html:6150-6154` — retained raw target passage.

Executed a Python harness from the repo root. It loaded the retained raw HTML and flat text bytes, imported the inline `classify` from the counter, wrote the two inputs only under `/fast/scratch/hyaku/kake-r64/ExecQuoteClassMatrix/`, and for each sample launched:

`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py classify --quote <sample> --raw /fast/scratch/hyaku/kake-r64/ExecQuoteClassMatrix/raw.txt --text /fast/scratch/hyaku/kake-r64/ExecQuoteClassMatrix/text.txt`

The harness compared the CLI's `derived=CLASS` output to the inline function's returned class and recorded each CLI return code.

## Matrix

| # | Sample quote | CLI | Inline | Agree / exit |
|---:|---|---|---|---|
| 1 | `<code>X-Content-Type-Options</code>` | raw-substring | raw-substring | yes / 0 |
| 2 | `<a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑤">header</a>` | raw-substring | raw-substring | yes / 0 |
| 3 | `<dfn class="dfn-paneled" data-dfn-type="http-header" data-export id="http-x-content-type-options">` | raw-substring | raw-substring | yes / 0 |
| 4 | `data-level="3.6" id="x-content-type-options-header"` | raw-substring | raw-substring | yes / 0 |
| 5 | `<code>Content-Type</code>` | raw-substring | raw-substring | yes / 0 |
| 6 | `id="determine-nosniff"` | raw-substring | raw-substring | yes / 0 |
| 7 | `X-Content-Type-Options header` | absent | absent | yes / 0 |
| 8 | `response header can be used to require checking` | collapsed-only | collapsed-only | yes / 0 |
| 9 | `checking of a response’s Content-Type header` | absent | absent | yes / 0 |
| 10 | `Content-Type header against the destination of a request.` | absent | absent | yes / 0 |
| 11 | `The X-Content-Type-Options response header` | absent | absent | yes / 0 |
| 12 | `require checking of a response’s` | collapsed-only | collapsed-only | yes / 0 |
| 13 | `against the destination of a request.` | collapsed-only | collapsed-only | yes / 0 |
| 14 | `response’s` (U+2019) | raw-substring | raw-substring | yes / 0 |
| 15 | `response's` (U+0027) | absent | absent | yes / 0 |
| 16 | `` `X-Content-Type-Options` `` (backticks) | raw-substring | raw-substring | yes / 0 |
| 17 | `X-Content-Type-Options` (plain) | raw-substring | raw-substring | yes / 0 |
| 18 | `S432 imaginary header directive` | absent | absent | yes / 0 |
| 19 | `unicorn content sniffing exemption` | absent | absent | yes / 0 |
| 20 | `response headers are made of moonlight` | absent | absent | yes / 0 |
| 21 | `backtick token `Totally-Not-A-Header`` | absent | absent | yes / 0 |
| 22 | `the request destination is a pineapple` | absent | absent | yes / 0 |

Exact aggregate harness output: `{"count":22,"all_agree":true}`. All 22 CLI invocations returned 0; every inline result matched. The apostrophe variant is sensitive to the retained character (curly quote occurs in the raw body; straight apostrophe is absent); backtick and plain header-string variants are both raw substrings.

## Verdict

No differential found for the tested matrix. The two classifiers agree on all 22 cases, including six raw HTML fragments, collapsed-text matches, absent spans, U+2019/U+0027 variants, and the backtick/plain pair. No blocker.