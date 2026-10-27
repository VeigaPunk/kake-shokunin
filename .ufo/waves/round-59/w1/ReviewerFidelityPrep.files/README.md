# ReviewerFidelityPrep.files — measurement receipts

Read-only receipts for the C3 fidelity reference (`reference.md`). No lane file other than the
seat report and this directory was touched.

| file | what it is |
|---|---|
| `reference.md` | the deliverable: S425 + S426 sentence lists, paraphrases, qualifiers, quotability |
| `verbatim.txt` | article-block text nodes rendered in reading order, extracted mechanically from the retained bodies |
| `nodes.txt` | per-node dump of both pages (index + stripped text), from the counter's own `text_segments` |
| `s425_render.txt`, `s426_render.txt` | block-level reading order with the text-node provenance of each block |
| `span_table.txt` | units/chars/in-node/own-count/other-count/ceiling verdict for every sentence asserted as quotable |
| `s425_frag.txt`, `s426_frag.txt` | per-sentence raw-node split and the eligible sub-span pool |
| `final_s425.txt`, `final_s426.txt`, `final_s426b.txt` | final whole-sentence quotability verdicts (whole-quotable vs split) with the eligible sub-spans |
| `validate_ref.py`, `validate_ref.out` | self-check of `reference.md`: every "Quoteable whole: N units / M chars / page-unique" claim re-measured against the counter's own code — 18 claims, 0 number mismatches, 0 unsupported/over-ceiling/unmarked; every other item is explicitly marked split, over-ceiling or not page-unique |

Method: the frozen counter `.ufo/waves/round-59/c59_quote_truth.py` was imported for `units`,
`text_segments`, `in_content`, `content_window` and `article_headings`, so every number here is the
counter's own measurement, not a re-implementation. Quotability re-confirmed with
`python3 -B .ufo/waves/round-59/span_tools.py check <S425|S426> "<span>"`.

Bodies (read-only): `sources/S425.html` 74477 bytes sha256 ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa;
`sources/S426.html` 69789 bytes sha256 8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879.

No tool installed or upgraded. Scratch `/fast/scratch/hyaku/kake-r59/ReviewerFidelityPrep` removed at exit.
