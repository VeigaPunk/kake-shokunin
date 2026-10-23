# CtlTrivial — r42-controls

NOT MET — none of the 8 trivial-output controls met the C1 predicate; the kill rule is **not** activated by this seat.

Axes: **operability** (runnable cost surface of the counter). Scope: built controls in `/fast/scratch/hyaku/kake-r42w1/CtlTrivial/` and scored them with the frozen counter bytes. No repo file other than this report was written; no tools installed; no network use.

## What was built (all Python 3 stdlib, derived from the round-41 tool `50287ac6…`)

Each variant keeps the round-41 stdout format, so the only difference from `50287ac6…` is the skipped work. Witnesses are from my own fixtures (`fixture/`, `fixture2/`, `witness.py`).

| tool (path in `/fast/scratch/hyaku/kake-r42w1/CtlTrivial/`) | sha256 | work it skips | witness value where it differs from tip41 |
|---|---|---|---|
| `v1_allclean.py` | `e82f6fe0f338b1e92d2391fbe2494224866f11e71cbe4fb8b3a073339e9e26be` | reads/parses/judges **no** sitemap file (`_audit_file` returns `(None,set())`) | `http://a.example/dir/a b` → tip41 `loc_not_absolute`, v1 `clean` |
| `v2_allinvalid.py` | `f60e10cec28dd69f1e96976dc975631f8cc4fc34de789623a9e61b7ff7be0baf` | every judgement; every check answered `check_invalid` | `https://a.example/dir/ok` → tip41 no finding, v2 `check_invalid` |
| `v3_locnotabsolute.py` | `1bab55ff99da57d28f719cbef59b1c202fbb3f96d46dedb9047c80ca1ef29780` | the URL rule (kept file reading/parsing) | `https://a.example/dir/ok` → tip41 no finding, v3 `loc_not_absolute` (entry 1) |
| `v4_emptystdout.py` | `fa53cfb616f566b81703c168c7c8c9d7dad20192b44d46d6f1af2e51b65d06ef` | whole output: empty stdout, exit 0 | stdout 0 bytes vs tip41's 591-byte JSON document |
| `v5_junkbytes.py` | `4774987e396a01b0b2abc047c60ea1acbb572038799881967272d24a0615df09` | whole output: `\x00\x01not-json\xff\xfe\n`, exit 0 | same fixture: 13 junk bytes vs tip41's JSON |
| `v6_constant.py` | `9273132f4f9f79618e8716de6a688b635381443b92b4c55510ba8ec1fda5ae0e` | manifest read and every file: constant `{"version":1,"verdict":"clean","checks":[]}` | verdict `clean`/`checks:[]` vs tip41's 5-item document |
| `v7_noreader.py` | `723ca7b1fa4a13e6ff2aafd0b89e6f3298fb51e181ce14be35ccf30161607d5e` | opens **no** sitemap file; manifest-level validation kept | `http://a.example/dir/a b` → tip41 `loc_not_absolute`, v7 `clean` |
| `v8_lengthgate.py` | `51871bff62cc9781c3a2d58680bdd64c4bf27fe5743372f5731bb6a5da72dfaf` | URL check for values ≥1000 code points (length gate) | `http://a.example/dir/`+`a`×1500+` `+`b`×100 → tip41 `loc_not_absolute`, v8 none; `https://z.example/dir/`+`c`×1500 → tip41 `loc_out_of_scope`, v8 none |

## Counter receipts (frozen counter `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`)

Command per tool (exit 1 = not met): `timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-42/c42_count.py --root <repo> --tool-file <tool> --label CtlTrivial-<n> --seed <S> --out <receipt>`; receipts in `/fast/scratch/hyaku/kake-r42w1/CtlTrivial/*.json`.

| tool | seed | equalRuns | first run that caught it | ratios T1..T5 | met |
|---|---|---|---|---|---|
| v1_allclean | 42101 | **0/8** | A | 0.070, 0.073, 0.082, 0.082, 10.351 | false (T5 > 2.0) |
| v2_allinvalid | 42101 | **0/8** | A | 0.071, 0.074, 0.080, 0.086, **1.021** | false (equality) |
| v3_locnotabsolute | 42101 | **0/8** | A | 0.798, 0.815, 0.573, 0.782, 10.860 | false (T5 > 2.0) |
| v4_emptystdout | 42101 | **0/8** | A | 5.432, 2.682, 1.375, 1.228, 10.230 | false (T1,T2,T5) |
| v5_junkbytes | 42101 | **0/8** | A | 5.290, 2.817, 1.314, 1.243, 10.627 | false (T1,T2,T5) |
| v6_constant | 42101 | **0/8** | A | 0.073, 0.072, 0.084, 0.083, **0.721** | false (equality) |
| v7_noreader | 42101 | **0/8** | A | 0.062, 0.062, 0.062, 0.070, 13.037 | false (T5 > 2.0) |
| v8_lengthgate | 42101 | **5/8** | C (A,B,T3,T4,T5 equal) | 0.730, 0.754, 1.400, 1.214, 9.828 | false (C,T1,T2 + T5 > 2.0) |
| v8_lengthgate | 42102 | **5/8** | C | 0.750, 0.720, 1.369, 1.219, 9.651 | false (same) |

Secondary receipts under the in-flight counter v2 (`c42_count_v2.py`, sha256 `01d3fb8de064cd86f5ec05be4641f154bb23a7961ff36e542a3777809208808e`, 9 runs): v1_allclean 0/9, v7_noreader 0/9, v8_lengthgate 6/9 — all `met:false`.

## Findings

- **The equality clause, not the CPU clause, rejects trivial skips.** `v2_allinvalid` and `v6_constant` pass **all five** ratio tests (T5 1.021 and 0.721) and are still 0/8 on equality. Any statement that the 2.0× budget alone rules out shortcuts is **wrong**; the conjunctive predicate is load-bearing here.
- **The T5 cost is charged by the manifest-level `sitemapUrl` parse, not the `loc` path.** `v8_lengthgate` skips the URL check for every `loc` ≥1000 code points yet keeps the round-41 T5 ratio (9.83/9.65 vs the recorded do-nothing 8.87/9.35); the controls that skip the *manifest-level* check (`v2`, `v6`) drop T5 to ≈1.0/0.72. A build that only rewrites the `loc` path will not cut T5 — the build seat and the L1 need the manifest-level parse in scope.
- **Noise band for work-identical tools (7 measurements of v1/v3/v4/v5/v7/v8 with identical work).** T1 5.29–5.43, T2 2.68–2.82, T3 1.31–1.40, T4 1.21–1.24, **T5 9.65–13.04**. T5 varies ~±17 % between identical-work runs; T1/T2/T3/T4 are tight. A build measured at T5 ≤ 2.0 has margin against this band.
- **`v8_lengthgate` is the strongest trivial skip found and still fails:** it is byte-equal to tip41 on runs A, B, T3, T4, T5 (5/8, 2634 equal values) because short values take the unchanged path; it is caught by run C (long values, 1800–6000 code points) and by T1/T2, and independently by the T5 ratio.
- **No control met the predicate, under either counter version.** The scorecard's kill rule (2) is not triggered by this seat; no witness is owed for a meeting tool because none met. Every tool here is a genuine control (each differs from `50287ac6…` on a shown value), so none of them is the excluded "equivalent implementation" case.

## Checked statements

- SCORECARD.md:2959-2971 control classes "constant output; junk; all-clean or all-invalid; no-reader" — **holds** (all four built, all rejected 0/8).
- "Not a control: a tool whose judgments equal the round-41 tool's on every value" — **holds** (every variant has a shown witness).
- "a control that meets means C1 is not met" (kill rule 2) — **not triggered**: no meeting control here.
- "the CPU budget is what separates a real speed-up from cheaper tools" — **overstated/wrong** as stated: cheap tools pass the CPU clause and fail equality (measured above).
- "T5 measures the `loc` URL check" — **wrong**: T5's dominant cost is the manifest-level `sitemapUrl` parse (48 × 200,000 code points) that no `loc`-side rewrite removes.

## Reproduction

`/fast/scratch/hyaku/kake-r42w1/CtlTrivial/`: `gen_variants.py` (v1–v6, v8 from `50287ac6…`), `v7_noreader.py` (standalone), `witness.py`, `score.sh`, `score_v2.sh`, receipts `*.json`, logs `*.log`; `tip41_ref.py` = unchanged `50287ac6…`.
