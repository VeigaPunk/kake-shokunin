# Located-line brute-force findings

## Verdict

Confirmed globally minimal located span **6150-6154** over all allowed `(a,b)` pairs. The retained raw HTML SHA-256 is `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`; the committed extraction recipe SHA-256 is `6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405`. The raw file has 18915 lines. The recipe was loaded from a scratch copy of the committed `extract_text.py`; each candidate was rendered by its `extract()` function and tested for the frozen quote from `c64_calibration.py` lines 71-75.

The full search tested, for every `a` from 6100 through 6200, every `b` from `a` through `min(a+15, 18915)`, stopping at its first hit. The best `(b-a,a,b)` tuple was `(4, 6150, 6154)`. Removing the left endpoint (6151-6154) loses the span; removing the right endpoint (6150-6153) loses it. 6150-6156 contains the span but has width 6, so is non-minimal versus width 4.

## First-hit boundary table

`—` means no hit for that `a` within the allowed end window.

| a | first-hit b |
|---:|---:|
| 6100 | — |
| 6101 | — |
| 6102 | — |
| 6103 | — |
| 6104 | — |
| 6105 | — |
| 6106 | — |
| 6107 | — |
| 6108 | — |
| 6109 | — |
| 6110 | — |
| 6111 | — |
| 6112 | — |
| 6113 | — |
| 6114 | — |
| 6115 | — |
| 6116 | — |
| 6117 | — |
| 6118 | — |
| 6119 | — |
| 6120 | — |
| 6121 | — |
| 6122 | — |
| 6123 | — |
| 6124 | — |
| 6125 | — |
| 6126 | — |
| 6127 | — |
| 6128 | — |
| 6129 | — |
| 6130 | — |
| 6131 | — |
| 6132 | — |
| 6133 | — |
| 6134 | — |
| 6135 | — |
| 6136 | — |
| 6137 | — |
| 6138 | — |
| 6139 | 6154 |
| 6140 | 6154 |
| 6141 | 6154 |
| 6142 | 6154 |
| 6143 | 6154 |
| 6144 | 6154 |
| 6145 | 6154 |
| 6146 | 6154 |
| 6147 | 6154 |
| 6148 | 6154 |
| 6149 | 6154 |
| 6150 | 6154 |
| 6151 | — |
| 6152 | — |
| 6153 | — |
| 6154 | — |
| 6155 | — |
| 6156 | — |
| 6157 | — |
| 6158 | — |
| 6159 | — |
| 6160 | — |
| 6161 | — |
| 6162 | — |
| 6163 | — |
| 6164 | — |
| 6165 | — |
| 6166 | — |
| 6167 | — |
| 6168 | — |
| 6169 | — |
| 6170 | — |
| 6171 | — |
| 6172 | — |
| 6173 | — |
| 6174 | — |
| 6175 | — |
| 6176 | — |
| 6177 | — |
| 6178 | — |
| 6179 | — |
| 6180 | — |
| 6181 | — |
| 6182 | — |
| 6183 | — |
| 6184 | — |
| 6185 | — |
| 6186 | — |
| 6187 | — |
| 6188 | — |
| 6189 | — |
| 6190 | — |
| 6191 | — |
| 6192 | — |
| 6193 | — |
| 6194 | — |
| 6195 | — |
| 6196 | — |
| 6197 | — |
| 6198 | — |
| 6199 | — |
| 6200 | — |

## Reproduction evidence

Inputs: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html` and `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/extract_text.py` (committed source at base `1a48131577ba82c967650561be34e8dba909432a`). Frozen span: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:70-75`; search semantics: same file lines 163-182.

Executed the Python brute-force driver in the session against scratch copies under `/fast/scratch/hyaku/kake-r64/ExecLocatedRange/`: import `extract_text.py`; decode `S432.html` as UTF-8 with replacement and split lines; loop `a=6100..6200`, `b=a..min(a+15,len(lines))`; call `extract('
'.join(lines[a-1:b]).encode('utf-8'))`; record first `b` where the frozen quote is a substring. Output: `raw_sha256=63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`, `recipe_sha256=6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405`, `best=(4, 6150, 6154)`, endpoint-removal results `False, False`, nonminimal candidate `(6, True)`.

No tools installed. No repository files other than this assigned report were changed. Scratch directory was removed after the report was written.
