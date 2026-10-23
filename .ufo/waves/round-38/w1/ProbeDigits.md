Touched sealed-tree metadata: I ran `test -d /fast/scratch/hyaku/kake-r38` (existence probe, no listing) and `stat -c %s /fast/scratch/hyaku` (parent only); nothing under the sealed dirs was listed, read, stat'ed or searched. All work stayed in my sandbox.

**Verdict.** (A) CONFIRMED — a `parse_int` that never calls `int()` above N digits parses a 64 MiB digit manifest in 0.03–0.34 s, ~15x inside the 5 s bar. (B) CONFIRMED — default `json.loads` raises `ValueError` starting at **4301** digits (4300 is accepted). (C) REFUTED — `sys.set_int_max_str_digits(0)` is **not quadratic** on this host: measured exponent **1.47–1.54**, not 2.0, because CPython 3.14 dispatches to `_pylong.int_from_string` (divide-and-conquer). It is still unbounded work: 25.0 s for one 64 MiB literal.

## Method
Host `python3 -VV` → **Python 3.14.8** (GCC 16.2.1); `sys.int_info` → `bits_per_digit=30, default_max_str_digits=4300, str_digits_check_threshold=640`; 32 cores, 30 GiB RAM.
Every measured run: `timeout 120 prlimit --as=4000000000 python3 measure.py run <variant> <digits> <n> [file]` (exit 0 ok / 2 when the variant raised by design / 124 would be timeout). In-memory document = one JSON object holding n integer literals of exactly D digits (`"7" + "0"*(D-1)`); parse timed with `perf_counter` after the bytes are in memory; best of 2–3 reps; **serial, single process, idle host**. File rows read a real 62.8/67.0 MB manifest from disk (read time reported separately, not in the parse figure).
Variants: `default` = `json.loads`; `unlimit` = `sys.set_int_max_str_digits(0)`; `guard4300`/`guard640` = `json.loads(parse_int=f)`, `int(s)` only when `len(s) <= N`, else a sentinel object; `rawstr` = `parse_int=lambda s: s` (control: no conversion at all).

## Timing table — parse_s, in-memory, 4 literals of D digits (doc = 4D bytes)
| D | default | unlimit (0 = no limit) | guard4300 | guard640 | rawstr |
|---|---|---|---|---|---|
| 10^3 | 0.016 ms ok | 0.016 ms | 0.017 ms | 0.003 ms | 0.003 ms |
| 10^4 | **0.005 ms ValueError** | 0.419 ms | 0.011 ms | 0.011 ms | 0.011 ms |
| 10^5 | **0.044 ms ValueError** | 14.273 ms | 0.094 ms | 0.092 ms | 0.092 ms |
| 10^6 | **0.435 ms ValueError** | 499.857 ms | 0.943 ms | 0.934 ms | 0.938 ms |
| 10^7 | **6.410 ms ValueError** | **14 806 ms** | 15.957 ms | 10.875 ms | 13.850 ms |

`ValueError` cells are the time to hit the *first* offending literal, not a parse. Exceptions quote: `Exceeds the limit (4300 digits) for integer string conversion: value has 4301 digits; use sys.set_int_max_str_digits()`.

## 64 MiB manifests (file mode; sha256 below)
| manifest | literals | default | unlimit | guard4300 | guard640 | rawstr |
|---|---|---|---|---|---|---|
| 62,803,391 B, 64-digit | 838,860 | 0.352 s ok | 0.297 s | 0.310 s | **0.335 s** | 0.279 s |
| 67,005,251 B, 10^5-digit | 670 | **ValueError 0.015 s** | 2.283 s | 0.031 s | **0.031 s** | 0.031 s |
| 66,793,891 B, 4300-digit (legal, just under the limit) | 15,500 | 0.780 s ok | — | 0.784 s | **0.027 s** | — |
| 67,108,864-digit **single** literal | 1 | **ValueError 0.039 s** | **24 947 ms** | — | **0.025 s** | 0.026 s |

Worst guarded column figure = 0.335 s (14.9x inside 5 s). Worst unguarded figure = 24.9 s (5x outside). `default` is *not* unusable: it parses 64 MiB of ≤4300-digit literals in 0.35–0.78 s and only dies when a single literal exceeds 4300 digits.

## The exponent (why "quadratic" is wrong)
Per-literal `unlimit` cost: 10^5 → 3.568 ms, 10^6 → 124.96 ms, 10^7 → 3701.5 ms. Slopes: 1e5→1e6 **1.544**, 1e6→1e7 **1.472**, 1e5→1e7 **1.508** (quadratic would be 2.0, i.e. 100x per decade; measured 30–35x). Direct `int()` (JSON literal shape, min of 3–10 calls): 4300→0.049 ms, 1e4→0.100 ms, 1e5→3.390 ms, 1e6→128.8 ms, 2e6→439.7 ms, 4e6→989.2 ms (1e5→4e6 slope 1.539). `python3 -c "import _pylong; print(dir(_pylong))"` exposes `int_from_string`, `str_to_int`, `str_to_int_inner` — the 3.12+ divide-and-conquer decimal→int path. Micro and JSON agree (0.049 ms x 15,500 = 0.76 s vs 0.780 s measured; 128.8 x 4 = 0.515 s vs 0.500 s; 3.39 x 670 = 2.27 s vs 2.283 s).

## The guard does what it claims (instrumented, N=640)
`guardproof.py` counts every literal handed to `parse_int`: 67 MB/10^5-digit manifest → calls=670, max_len=100000, over_N=670, **int_calls=0**, sentinel values=670, 0.041 s. 62.8 MB/64-digit manifest → calls=838,860, max_len=64, over_N=0, int_calls=838,860, 0.466 s. 4300x15,500 → calls=15,500, over_N=15,500, **int_calls=0**, 0.030 s. Peak RSS (`getrusage(RUSAGE_CHILDREN)`): guard640 on the single 64 MiB literal 267.6 MB; `unlimit` on the same 487.8 MB (both inside the 4 GB cap).

## Bearing on the C2 contract (rule (h))
Observed hook routing (`json.loads(doc, parse_int=…, parse_constant=…, parse_float=…)`): `NaN`/`Infinity`/`-Infinity` → **`parse_constant` only**; `1e400` → **`parse_float` only**; a 50-digit integer → `parse_int`. So a guard installed only in `parse_int` (a) never sees the non-JSON literals rule (h) must reject — the audit also needs `parse_constant` — and (b) satisfies "unused long numbers change nothing" by construction: skipping conversion is 25x cheaper than `unlimit` on a 64 MiB literal and removes the 4301-digit `ValueError` cliff. Threshold choice is a cost knob, not a correctness knob: N=640 keeps the worst 64 MiB case at 0.027–0.335 s; N=4300 is still inside 5 s (≤0.784 s) but 29x slower on the legal-4300-digit manifest.

## Limits / not verified
Table of record is `serial.jsonl`; the `*_grid.txt` files are 6–8-way **parallel scouts** and read up to 2x high under contention, so they are corroboration only. One early micro used all-sevens literals with 2 reps and gave 271 ms at 10^6 vs the reported 128.8 ms (min of 3, `"7"+"0"*…`); that 2x gap is unresolved and I report the shape-consistent series. No mixed-size manifest, nothing beyond 64 MiB, no `parse_float`/`parse_constant` cost sweep. I did not run any round-38 counter (no key), did not clone or touch the lane, and changed no lane file — this probe informs rule (h) but implements none of it. No network; no tool installs (host Python 3.14.8 sufficed).

## Artifacts (all under /fast/scratch/hyaku/kake-r38w1/ProbeDigits/)
`measure.py` d8daa53ab2eee5d549e83db7b33c927ad905229cf073b6d6e2e85c38fc29a262 · `serial_sweep.py` b1151b6d126872b289f7548733989185126c653a329c5242c392945b83a7f24c · `micro2.py` d5d58b81d1511bf3fd3a31219d33e03014be8a7605728eabba76c2c70b76da2d · `guardproof.py` fad99a262964a3162078bb53392da5e666dfc4f5576ce7849c039f60c57d7b76 · `rusage.py` 4b7812f4dbb14a4f18b0f8c251932aa53f3942f16d247335c164e37ed6cbc626 · `data/manifest64_d64.json` f3be932e0b6cfd4244dab05362cef228a2f0d2a4173d53f4d5204b8888bbb94a · `data/manifest64_d100000.json` f085d24e6d17bc9fffa86a2458da72fdd1dd06efadb6df11f772d31ff23e5aea · `serial.jsonl` (39 rows) 04ff75383ba63c76ec150e75e1c75288c5b6b85475cb826513a574be6406fe48 · `serial_out.txt` 1d0eaf26568442733beddb76592e53171a69663b292b6aa0a444d414d26bd5be · `group_d.txt` 67101829025178f021a64b932107c77a1c6a37a664267436246855a8488cce3f · `file_grid.txt` 3213d6014425f53318e73e8e78924f5e829e447ad800850787cdc322a788a6bc · `legal_grid.txt` 8c87f2f8ecb310db8abec3bfbbc35dfee7f5166234e87603cb9eb4282eb8b523 · `small_grid.txt` ef63a6669a71b052268c42be787664aae80fe056a22b7039f3a714ccfcee858c · `big_grid.txt` a808ce27749f30ba3543a7410c27f2d656198b2687284fb1ca40da42f12ab566 · `scale_grid.txt` 1c1057679ec5bb6393029528d30b14cd3058211245b8d6b6cb7a27ea3284a317
